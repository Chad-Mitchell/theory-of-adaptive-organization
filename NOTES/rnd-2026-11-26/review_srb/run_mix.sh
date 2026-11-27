#!/bin/bash
cd "$(dirname "$0")"
xargs -P 5 -I{} ./dpmix {} < nlist.txt > mix_raw.txt
echo done
