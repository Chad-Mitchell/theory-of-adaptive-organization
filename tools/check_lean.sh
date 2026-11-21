#!/usr/bin/env bash
# Build the Lean 4 formalization of the GTAO core (OPEN_WORK T19).
# Run from the repo root:  tools/check_lean.sh
# Exit 0 = lake build succeeded and no `sorry` occurs in formal/lean/**/*.lean.
# Exit 2 = Lean / lake is not installed.
# Exit 1 = build failed or a `sorry` was found.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LEAN_DIR="$ROOT/formal/lean"

if [[ -f "${HOME}/.elan/env" ]]; then
  # shellcheck disable=SC1091
  source "${HOME}/.elan/env"
fi
if [[ -d "${HOME}/.elan/bin" ]]; then
  export PATH="${HOME}/.elan/bin:${PATH}"
fi

if ! command -v lake >/dev/null 2>&1; then
  echo "check_lean.sh: lake/elan not found. Install Lean 4 via elan, then rerun." >&2
  exit 2
fi

if ! command -v rg >/dev/null 2>&1; then
  SORRY_HITS="$(grep -R -n --include='*.lean' -E '(^|[^A-Za-z_])sorry([^A-Za-z_]|$)' "$LEAN_DIR" || true)"
else
  SORRY_HITS="$(rg -n --glob '*.lean' '(^|[^A-Za-z_])sorry([^A-Za-z_]|$)' "$LEAN_DIR" || true)"
fi
if [[ -n "${SORRY_HITS}" ]]; then
  echo "check_lean.sh: \`sorry\` is present in the Lean sources:" >&2
  echo "${SORRY_HITS}" >&2
  exit 1
fi

cd "$LEAN_DIR"
echo "check_lean.sh: lake exe cache get"
nice -n 19 lake exe cache get
echo "check_lean.sh: lake build"
nice -n 19 lake build
echo "check_lean.sh: OK"
