#!/bin/bash
# EVO1 locked run plan: 8 test worlds x seeds 0-7 (even = low start, odd = high start), null (drift) seeds 100-103 per world.
# nice 19; 4 jobs at a time, 2 numba threads each.  Outputs: runs/*.json (+ _snaps.npz).
cd "$(dirname "$0")"
mkdir -p runs logs
jobs_list=()
for w in PC W1 W3 W4b W2 W4 S031 S07; do
  for s in 0 1 2 3 4 5 6 7; do jobs_list+=("$w $s"); done
  for s in 100 101 102 103; do jobs_list+=("$w $s --null"); done
done
printf '%s\n' "${jobs_list[@]}" | xargs -P 4 -I{} bash -c 'set -- {}; f=runs/$1_s$2$([ "$3" = "--null" ] && echo _null).json; [ -f "$f" ] && exit 0; NUMBA_NUM_THREADS=2 nice -n 19 python3 evo.py {} --out runs > logs/$1_$2$3.log 2>&1'
