#!/bin/bash
# pilot (alpha = 2, outside the locked contrast): noise of the exponent estimator at the planned design
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for s in $(seq 1 16); do for r in 0.01 0.02 0.04 0.08 0.16 0.32; do echo "2.0 $r $s"; done; done | \
  xargs -P 3 -n 3 sh -c 'nice -n 19 python3 run.py $0 $1 $2 pilot_alpha2.jsonl'
echo DONE
