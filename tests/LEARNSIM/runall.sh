#!/bin/bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 NPROC=3
cd /workspace/gtao/night2/LEARNSIM
nice -n 19 python3 run_onset.py results_es.jsonl es 16 all > logs/onset_es.log 2>&1
nice -n 19 python3 run_onset2.py results_ext.jsonl > logs/onset_ext.log 2>&1
echo ALLDONE >> logs/onset_ext.log
