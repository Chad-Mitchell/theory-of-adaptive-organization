#!/bin/bash
# Exact even-n curves (dpeven.c), validated against sr_b exact LP DP at n=6..2400 (max diff < 1e-15).
cd "$(dirname "$0")"
NS="1002 1202 1402 1602 1802 2002 2202 2402 2602 2802 3002 3202 3402 3602 3802 4002 4402 4802 5002 5602 6002 7002 8002 9002 10002 3000 4000 5000 6000 8000 10000 12002"
echo $NS | tr ' ' '\n' | xargs -P 4 -I{} sh -c 'test -s curves/{}.txt || ./dpeven {} > curves/{}.txt'
echo done
