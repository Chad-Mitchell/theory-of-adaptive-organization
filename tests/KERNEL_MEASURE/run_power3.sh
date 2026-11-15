set -e
cd "$(dirname "$0")"
i=0
for c in R1_0.25 R2_0.25 R3_0.25 H0_0.35; do
  i=$((i+1)); nice -n 19 python3 power_sim2.py $c 100 $((2029000+i*1000)) > power2/$c.log 2>&1
done
echo ALLDONE
