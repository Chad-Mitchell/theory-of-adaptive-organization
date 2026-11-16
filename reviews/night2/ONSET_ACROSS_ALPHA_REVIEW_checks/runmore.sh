#!/bin/bash
# post hoc extension (declared after seeing grid.jsonl INCONCLUSIVE): seeds 17-48, grid learner, author's C, both alpha
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for s in $(seq 17 48); do for r in 0.01 0.02 0.04 0.08 0.16 0.32; do
  echo "grid 1.5 $r $s 84.3 grid_more.jsonl"; echo "grid 2.5 $r $s 6072 grid_more.jsonl"; done; done |
  xargs -P 6 -n 6 sh -c 'nice -n 19 python3 sim.py $0 $1 $2 $3 $4 $5'
echo DONE
