#!/usr/bin/env bash
# Regenerates every *.out in this folder. Needs numpy, scipy, sympy (venv at ../.venv).
set -e
cd "$(dirname "$0")"
. ../.venv/bin/activate
for f in fpt_checks jumps_checks objective_checks coarse_grain_checks c3_diagnostics toy_reversal_check; do
  python "$f.py" > "$f.out"; echo "ok $f"
done
