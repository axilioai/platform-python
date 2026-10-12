"""Fix two behaviours of Fern's generated client runtime after a regen.

* Retries. Fern resends every request after a 5xx (and a 409), POSTs included.
  The API takes no idempotency keys, so a create that succeeded but answered
  500 runs twice: a second webhook endpoint (and the first one's one-time
  secret is lost), or every run booked twice. After the fix a 429 or 408, which
  the server refused before acting, is resent for any method; a 5xx only for a
  method that is safe to repeat (RFC 9110 9.2.2). The same goes for a dropped
  connection: Fern resends after any ConnectError or RemoteProtocolError, but
  only a ConnectError means the request never reached the server. A connection
  that drops after the request went out is resent only for a method that is
  safe to repeat. The Go SDK's retrier does the same.
* repr(). Pydantic prints every field, so logging a create or rotate response
  wrote its one-time secret to the log. After the fix repr() and str() print
  "[redacted]" for webhook signing secrets, API key values, sign-in tokens, and
  the session URLs that carry a token (live view, control, telemetry). The
  attributes and model_dump() are unchanged.

The argus client is left alone: its POSTs read a screenshot and change nothing.

Run by the regen workflow after every generation. Idempotent, and exits non-zero
when the generated code no longer has the shape this expects, so a generator
change surfaces as a failed regen instead of a fix that silently stopped
applying. tests/test_generated_runtime.py checks the behaviour.
"""

from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
CORE = REPO / "src" / "axilio" / "core"

RETRY_FILE = CORE / "http_client.py"
RETRY_GENERATED = """def _should_retry(response: httpx.Response) -> bool:
    return response.status_code >= 500 or response.status_code in [429, 408, 409]
"""
RETRY_FIXED = """def _should_retry(response: httpx.Response) -> bool:
    # Rewritten by scripts/fix_generated_runtime.py: a 5xx can follow a request
    # that took effect, and the API takes no idempotency keys, so only a method
    # that is safe to repeat is resent after one.
    if response.status_code in (429, 408):
        return True
    return response.status_code >= 500 and response.request.method in _IDEMPOTENT_METHODS


_IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})


def _should_retry_transport_error(error: httpx.TransportError, method: str) -> bool:
    # Added by scripts/fix_generated_runtime.py: a ConnectError means the
    # request never reached the server, so any method is resent. A connection
    # that dropped after the request went out may have taken effect.
    return isinstance(error, httpx.ConnectError) or method.upper() in _IDEMPOTENT_METHODS
"""

# Both HttpClient.request and AsyncHttpClient.request catch dropped connections.
TRANSPORT_GENERATED = """        except (httpx.ConnectError, httpx.RemoteProtocolError):
            if retries < max_retries:
"""
TRANSPORT_FIXED = """        except (httpx.ConnectError, httpx.RemoteProtocolError) as exc:
            if retries < max_retries and _should_retry_transport_error(exc, method):
"""
TRANSPORT_COUNT = 2

REPR_FILE = CORE / "pydantic_utilities.py"
REPR_GENERATED = "class UniversalBaseModel(pydantic.BaseModel):\n"
REPR_FIXED = """class UniversalBaseModel(pydantic.BaseModel):
    # Added by scripts/fix_generated_runtime.py: repr() and str() never print
    # these one-time secrets. The attributes and model_dump() still hold them.
    def __repr_args__(self) -> Any:
        for name, value in super().__repr_args__():
            if name in _REDACTED_FIELDS and value is not None:
                value = "[redacted]"
            yield name, value

"""
REPR_CONSTANT = """

_REDACTED_FIELDS = frozenset(
    {"secret", "key_value", "token", "live_view_url", "control_url", "telemetry_url"}
)


class UniversalBaseModel(pydantic.BaseModel):
"""


def fix(path: pathlib.Path, generated: str, fixed: str, name: str, count: int = 1) -> bool:
    src = path.read_text(encoding="utf-8")
    if src.count(fixed) == count:
        print(f"{name}: already fixed")
        return True
    if src.count(generated) != count:
        print(
            f"fix_generated_runtime: {path.relative_to(REPO)}: the generated {name} code "
            "changed shape - update this fix",
            file=sys.stderr,
        )
        return False
    path.write_text(src.replace(generated, fixed), encoding="utf-8", newline="\n")
    print(f"{name}: fixed")
    return True


def main() -> int:
    ok = fix(RETRY_FILE, RETRY_GENERATED, RETRY_FIXED, "retry")
    ok = (
        fix(RETRY_FILE, TRANSPORT_GENERATED, TRANSPORT_FIXED, "transport retry", TRANSPORT_COUNT)
        and ok
    )
    # The constant goes above the class, then the method inside it.
    ok = fix(REPR_FILE, "\n\n" + REPR_GENERATED, REPR_CONSTANT, "repr constant") and ok
    ok = fix(REPR_FILE, REPR_GENERATED, REPR_FIXED, "repr") and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
