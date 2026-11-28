#!/bin/bash
# locked design run (alpha 1.5 and 2.5); launched only after PREREG.md is committed and pushed
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for s in $(seq 1 16); do for a in 1.5 2.5; do for r in 0.01 0.02 0.04 0.08 0.16 0.32; do echo "$a $r $s"; done; done; done | \
  xargs -P 3 -n 3 sh -c 'nice -n 19 python3 run.py $0 $1 $2 results.jsonl'
nice -n 19 python3 verdict.py > VERDICT.json
echo DONE
