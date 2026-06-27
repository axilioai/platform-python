#!/usr/bin/env bash
# Regenerate a generated client package from a committed OpenAPI spec.
#
# Usage: scripts/regen.sh [production] [backend|argus]
#        (defaults: production backend)
#
# Production is the only supported environment: the public SDK is generated
# from the live production spec, and staging specs are not tracked in this
# repo (they carry unreleased/internal surface — see regen.yml).
#
# The backend's deploy pipeline commits
# specs/{environment}/{openapi,argus-openapi}.json on each deploy and fires
# repository_dispatch ({openapi,argus}-spec-updated), which kicks off
# .github/workflows/regen.yml. That workflow invokes this script per client.
#
# Developers can also run it locally to preview changes — useful when
# debugging codegen drift or trying out a generator config.
#
# What it does:
#   1. Runs openapi-python-client against specs/{env}/openapi.json.
#   2. Replaces src/axilio/_generated/ with the freshly generated
#      package. Internal imports inside the generated code use
#      relative paths (`from ...client import ...`), so we keep the
#      whole package intact rather than picking apart api/ and models/.
#
# What it does NOT do:
#   - Bump the version in pyproject.toml.
#   - Commit anything. The receiver workflow handles commit + PR; local
#     runs are for inspection only.

set -euo pipefail

ENVIRONMENT="${1:-production}"
CLIENT="${2:-backend}"

# Production-only: staging specs are not tracked in this public repo, and the
# SDK must reflect what's live behind api.axilio.ai.
if [[ "$ENVIRONMENT" != "production" ]]; then
  echo "error: unsupported environment '$ENVIRONMENT' (only 'production' is supported)" >&2
  exit 1
fi

# Two specs feed two generated packages in this repo:
#   backend → specs/{env}/openapi.json        → src/axilio/_generated
#   argus   → specs/{env}/argus-openapi.json  → src/axilio/_generated_argus
# The backend's deploy pipeline publishes each + fires a distinct
# repository_dispatch (openapi-spec-updated / argus-spec-updated);
# regen.yml calls us per client.
case "$CLIENT" in
  backend)
    SPEC_PATH="specs/${ENVIRONMENT}/openapi.json"
    GENERATED_DEST="src/axilio/_generated"
    ;;
  argus)
    SPEC_PATH="specs/${ENVIRONMENT}/argus-openapi.json"
    GENERATED_DEST="src/axilio/_generated_argus"
    ;;
  *)
    echo "error: unknown client '$CLIENT' (expected: backend | argus)" >&2
    exit 1
    ;;
esac

if [[ ! -f "$SPEC_PATH" ]]; then
  echo "error: spec not found at $SPEC_PATH" >&2
  echo "       The backend's deploy pipeline populates this on each deploy." >&2
  echo "       Has a deploy for $ENVIRONMENT happened yet?" >&2
  exit 1
fi

if ! command -v openapi-python-client >/dev/null 2>&1; then
  echo "error: openapi-python-client not on PATH" >&2
  echo "       Install with: pip install -e '.[dev]'" >&2
  exit 1
fi

TMP_OUT=$(mktemp -d)
trap 'rm -rf "$TMP_OUT"' EXIT

openapi-python-client generate \
  --path "$SPEC_PATH" \
  --output-path "$TMP_OUT" \
  --overwrite

# The generator derives the project + package name from the spec's
# info.title ("Axilio API" → "axilio-api-client" / "axilio_api_client").
# We rehome the package's *contents* into src/axilio/_generated/ —
# that name change is invisible to internal `from .` / `from ..` /
# `from ...` imports inside the generated code.
GENERATED_PACKAGE=$(find "$TMP_OUT" -mindepth 1 -maxdepth 1 -type d -name "*_client" | head -1)
if [[ -z "$GENERATED_PACKAGE" || ! -d "$GENERATED_PACKAGE" ]]; then
  echo "error: could not find generated package under $TMP_OUT" >&2
  ls -la "$TMP_OUT" >&2
  exit 1
fi

rm -rf "$GENERATED_DEST"
mkdir -p "$GENERATED_DEST"
cp -a "$GENERATED_PACKAGE/." "$GENERATED_DEST/"

echo "regenerated $GENERATED_DEST/ from $SPEC_PATH"
echo "  - $(find "$GENERATED_DEST/api" -name '*.py' ! -name '__init__.py' 2>/dev/null | wc -l) operation modules"
echo "  - $(find "$GENERATED_DEST/models" -name '*.py' ! -name '__init__.py' 2>/dev/null | wc -l) model modules"

# Sync generator runtime deps into our parent pyproject.toml's
# `dependencies` array. We build a wheel from the generator output
# (using whichever build backend its pyproject declares — poetry-core
# today) and let scripts/sync_codegen_deps.py read the wheel's
# canonical PEP 508 Requires-Dist headers from METADATA. This avoids
# hand-parsing Poetry's ^/~ operators ourselves: pip itself sees
# exactly these strings at install time, so what the build backend
# emits into the wheel IS the right translation by construction.
#
# Class of bug prevented: generator adds a new transitive dep (e.g.
# attrs), regen lands the new code, but our pyproject still ships
# the old list — wheel installs but `from axilio import Client`
# raises ModuleNotFoundError. This guards the regression where 0.1.1
# shipped without attrs / python-dateutil declared.
echo "building wheel from generator output to extract canonical PEP 508 deps"
python3 -m build --wheel --outdir "${TMP_OUT}/wheel" "${TMP_OUT}" 2>&1 \
  | grep -E '^(Successfully|\* )' || true

GENERATOR_WHEEL=$(find "${TMP_OUT}/wheel" -maxdepth 1 -name '*.whl' | head -1)
if [[ -z "$GENERATOR_WHEEL" || ! -f "$GENERATOR_WHEEL" ]]; then
  echo "error: python -m build did not produce a wheel under ${TMP_OUT}/wheel/" >&2
  ls -la "${TMP_OUT}/wheel" >&2 2>/dev/null || true
  exit 1
fi

python3 scripts/sync_codegen_deps.py \
  --wheel "$GENERATOR_WHEEL" \
  --target pyproject.toml
