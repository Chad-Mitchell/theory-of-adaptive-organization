set -e
cd "$(dirname "$0")"
i=0
for c in H0_0 H0_0.25 H0_0.5 H0_1.0 H0_0_1.1587 H0_0_1.3587 R1_0.5 R2_0.5 R3_0.5 R3_0; do
  i=$((i+1)); nice -n 19 python3 power_sim.py $c 100 $((2028000+i*1000)) > power/$c.log 2>&1
done
echo ALLDONE
