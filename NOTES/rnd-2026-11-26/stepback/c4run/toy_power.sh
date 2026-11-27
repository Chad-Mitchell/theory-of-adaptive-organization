#!/bin/bash
# NON-SCORED toy runs (seeds 1..999 only). Planted-effect power at toy size N0=1e6 (rho=2e6, T=1).
cd "$(dirname "$0")"; mkdir -p toy
for cp in 1.00 1.02 1.05 1.10 1.20 1.96; do
  for s in $(seq 1 160); do echo "$cp $s"; done
done | xargs -P 6 -n 2 sh -c './c4r_sprinkle 1 2000000 $0 $1' > toy/planted_N1e6.txt
# separate control pool (seeds 501..660) for comparisons
seq 501 660 | xargs -P 6 -I{} ./c4r_sprinkle 1 2000000 1.00 {} > toy/control_N1e6.txt
# toy lattice (seeds 1..16, T=4000) for variance and shape
seq 1 16 | xargs -P 6 -I{} ./c4r_lattice 4000 {} > toy/lattice_T4000.txt
