#!/bin/bash
set -euo pipefail
cd <local>/gtao/night2/LEARNSIM
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONHASHSEED=0
echo "START analyze2 $(date)"
nice -n 19 python3 analyze2.py results_es.jsonl results_ext.jsonl PREDICTIONS_2.json > /tmp/learnsim_ref/ANALYSIS_2_rerun.json
echo "DONE analyze2 $(date)"
echo "START analyze $(date)"
nice -n 19 python3 analyze.py results_es.jsonl THEORY_PREDICTIONS.json MEASURED_AB.json > /tmp/learnsim_ref/ANALYSIS_1_rerun.json
echo "DONE analyze $(date)"
echo "START postlock $(date)"
nice -n 19 python3 postlock_fixes.py > /tmp/learnsim_ref/POSTLOCK_FIXES_rerun.json
echo "DONE postlock $(date)"
echo "START pop $(date)"
nice -n 19 python3 analyze.py results_pop_dedup.jsonl THEORY_PREDICTIONS.json > /tmp/learnsim_ref/ANALYSIS_POP_rerun.json
echo "DONE pop $(date)"
