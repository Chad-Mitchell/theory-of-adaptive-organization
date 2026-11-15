#!/bin/sh
# Re-runs every check; outputs go to the matching .out files. Python env: ../.venv (sympy 1.14, numpy 2.5.4, scipy 1.18.1)
cd "$(dirname "$0")"
for f in c1_staleness_holdfade c2_ruin_temperature c3_lundberg_persistence c4_why_tau_vanishes c5_scaling_universality c6_persistence_bound c7_rules_counterexamples c8_merton_and_index_ratio i1_internal_model i2_maintenance_sdpi i3_throughput_scaling i4_nonstationary_datarate; do
  ../.venv/bin/python $f.py > $f.out 2>&1 && echo "ok $f" || echo "FAIL $f"
done
