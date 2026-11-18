#!/bin/bash
# blobless full-history clones into $1 (scratch, outside the repo)
D=${1:-<local>/scratch/d3oos_git}; mkdir -p $D
for r in $(cat repos.txt reserve.txt); do n=${r/\//_}; [ -d $D/$n ] || git clone -q --filter=blob:none --no-checkout https://github.com/$r $D/$n || echo "CLONE-FAIL $r"; done
