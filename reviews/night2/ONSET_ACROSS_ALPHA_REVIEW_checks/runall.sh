#!/bin/bash
# reviewer runs: nice 19, single-threaded BLAS, 6 workers, background
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{
for s in $(seq 1 16); do for r in 0.01 0.02 0.04 0.08 0.16 0.32; do
  echo "grid 1.5 $r $s 84.3 grid.jsonl"; echo "grid 2.5 $r $s 6072 grid.jsonl"
  echo "es 1.5 $r $s 84.3 es.jsonl";     echo "es 2.5 $r $s 6072 es.jsonl"
  echo "grid 1.5 $r $s 2000 commonC.jsonl"; echo "grid 2.5 $r $s 2000 commonC.jsonl"
done; done
} | xargs -P 6 -n 6 sh -c 'nice -n 19 python3 sim.py $0 $1 $2 $3 $4 $5'
echo DONE
