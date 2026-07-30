"""Every generated-client attribute the hand-written layer touches, checked.

The hand-written layer (``platform/``, ``drivers/`` — see ``src/axilio/.fernignore``)
is coupled to generated code it does not control, and regen updates one side
without the other. In the Go SDK that coupling is compiled, so a renamed method
is a build error. Here nothing checks it: mypy excludes the generated packages,
and Python resolves attributes at call time, so drift waits for a user to hit an
``AttributeError``.

That is not hypothetical. The ``/files`` -> ``/uploads`` rename regenerated both
SDKs; Go failed to compile immediately, Python passed green and shipped 0.9.0
with ``client.files.upload`` raising ``AttributeError`` on first use.

``tests/test_files.py`` closed that instance by exercising the file helpers
against a mocked transport, and ends with a hand-written list of attributes to
check. This closes the *class*: it reads the hand-written sources, extracts
every generated-client attribute chain it can see, and asserts each one still
resolves. A new wrapper is covered the moment it is written, with nothing to
remember and no list to maintain — which matters, because the failure mode here
is precisely that someone forgets.

Deliberately static rather than a smoke test: it does not need a transport, a
fixture, or knowledge of what any helper is *for*. It only answers "does the
thing this code calls still exist", which is the whole of the drift question.

Known blind spot: ``_FilesNamespace.__getattr__`` forwards arbitrary names to
the generated client, and no static check can resolve a name that is only known
at runtime. Those paths need the behavioural tests in ``test_files.py``. It is
also the reason the ticket (AXI-1459) wants those namespaces typed against the
generated client rather than ``typing.Any``.
"""

from __future__ import annotations

import ast
import pathlib
import typing

import pytest

from axilio.platform import Client

# Hand-written trees, straight from .fernignore. _mode.py and argus/ are also
# fern-ignored but do not call the generated client, so they contribute
# nothing and are not searched.
_HANDWRITTEN = ("platform", "drivers")

# The two ways this codebase reaches the generated client:
#
#   self._api.<namespace>.<method>     the client the wrapper holds
#   <expr>.raw.<namespace>.<method>    the public escape hatch
#
# Both are attribute chains rooted at a name we can recognise, which is what
# makes them statically resolvable.
_ROOTS = ("_api", "raw")

_SRC = pathlib.Path(__file__).resolve().parent.parent / "src" / "axilio"


class _Reference(typing.NamedTuple):
    """One generated-client attribute chain found in hand-written source."""

    namespace: str
    attribute: str
    where: str

    def __str__(self) -> str:  # pragma: no cover - test IDs only
        return f"{self.namespace}.{self.attribute} ({self.where})"


def _chain(node: ast.Attribute) -> list[str] | None:
    """Flatten an attribute chain into its parts, innermost first.

    ``self._api.uploads.create`` -> ``["self", "_api", "uploads", "create"]``.
    Returns None for chains rooted in a call or subscript, which are not
    statically resolvable and are not what this looks for.
    """
    parts: list[str] = []
    current: ast.expr = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    parts.append(current.id)
    return list(reversed(parts))


def _references() -> list[_Reference]:
    """Every generated-client attribute chain in the hand-written trees."""
    found: list[_Reference] = []
    for tree_name in _HANDWRITTEN:
        tree = _SRC / tree_name
        if not tree.exists():
            continue
        for path in sorted(tree.rglob("*.py")):
            module = ast.parse(path.read_text(), filename=str(path))
            for node in ast.walk(module):
                if not isinstance(node, ast.Attribute):
                    continue
                parts = _chain(node)
                if parts is None:
                    continue
                for root in _ROOTS:
                    if root not in parts:
                        continue
                    i = parts.index(root)
                    # Need <root>.<namespace>.<attribute> to say anything.
                    if len(parts) < i + 3:
                        continue
                    # Private chains (``_client_wrapper``) are Fern internals,
                    # not the generated public surface. They are pinned
                    # individually below, where the fragility can be spelled out.
                    if parts[i + 1].startswith("_"):
                        continue
                    found.append(
                        _Reference(
                            namespace=parts[i + 1],
                            attribute=parts[i + 2],
                            where=f"{path.relative_to(_SRC.parent.parent)}:{node.lineno}",
                        )
                    )
    # Deduplicate on the pair being checked; keep the first site for the message.
    seen: dict[tuple[str, str], _Reference] = {}
    for ref in found:
        seen.setdefault((ref.namespace, ref.attribute), ref)
    return sorted(seen.values())


_REFERENCES = _references()


@pytest.fixture
def client() -> Client:
    """No network: nothing here issues a request, it only reads attributes."""
    return Client(api_key="axl_test", base_url="https://api.test.invalid")


def test_extraction_found_something() -> None:
    """Guard against this whole file silently becoming a no-op.

    If the wrapper is refactored to reach the generated client some other way,
    the extraction stops matching, every assertion below trivially passes, and
    the drift check quietly protects nothing — the same shape of failure it
    exists to catch.
    """
    assert _REFERENCES, (
        "no generated-client references found in "
        f"{_HANDWRITTEN} — the extraction patterns {_ROOTS} are probably stale"
    )


@pytest.mark.parametrize("ref", _REFERENCES, ids=str)
def test_generated_attribute_still_exists(client: Client, ref: _Reference) -> None:
    """The hand-written layer calls it, so the generated client must have it."""
    namespace = getattr(client.raw, ref.namespace, None)
    assert namespace is not None, (
        f"generated client lost the '{ref.namespace}' namespace, "
        f"still referenced at {ref.where}"
    )
    assert hasattr(namespace, ref.attribute), (
        f"generated {ref.namespace} client lost .{ref.attribute}(), "
        f"still called at {ref.where}"
    )


def test_private_generated_internals_still_exist(client: Client) -> None:
    """The one place the wrapper reaches past the public generated surface.

    ``Client.close()`` uses ``self._api._client_wrapper.httpx_client`` to shut
    the transport down. Fern owns that name and it is private, so it can change
    on any regen with no deprecation and no public-surface diff to notice. The
    extraction above deliberately does not chase private chains; this pins the
    single one that exists so it fails here rather than in a user's teardown.
    """
    wrapper = getattr(client.raw, "_client_wrapper", None)
    assert wrapper is not None, (
        "generated client lost ._client_wrapper — Client.close() depends on it"
    )
    assert hasattr(wrapper, "httpx_client"), (
        "generated _client_wrapper lost .httpx_client — Client.close() depends on it"
    )
