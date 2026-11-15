#!/bin/bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
cd /workspace/gtao/night2/LEARNSIM
nice -n 19 python3 run_pop_r.py >> logs/pop.log 2>&1
echo POPDONE >> logs/pop.log
