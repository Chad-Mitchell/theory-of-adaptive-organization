#!/bin/sh
# Crossref check of every DOI cited in theory/CLOCK_TERM_2026-11-23.md and the litmap/DRIFT amendments.
for d in 10.1103/PhysRevLett.114.158101 10.1103/PhysRevLett.116.120601 10.1103/PhysRevX.6.041053 10.1103/PhysRevLett.128.130606 10.1103/rpls-mp8z 10.1038/nphys3412 10.1103/PhysRevX.7.031022 10.1103/PhysRevX.11.021029 10.7554/eLife.37624 10.1103/PhysRevE.97.032405 10.1088/1478-3975/13/3/035005 10.1038/s41467-018-03826-4 10.1038/s41567-019-0701-7 10.1145/1807048.1807053 10.1103/PhysRevLett.102.250602 10.1103/19nl-c8fl 10.1088/1742-5468/adf4be 10.1103/PhysRevE.93.022116 10.1109/cdc.1997.657776 10.1103/PhysRevLett.95.200201 10.1073/pnas.0710743106 10.24033/bsmf.1494 10.1103/PhysRevX.4.031015; do
  for t in 1 2 3; do r=$(curl -s -m 30 "https://api.crossref.org/works/$d"); printf "%s" "$r" | grep -q "\"message\"" && break; sleep 3; done
  echo "$d | $(printf "%s" "$r" | python3 -c 'import sys,json
try:
  m=json.load(sys.stdin)["message"]; a=m.get("author",[]); print((a[0].get("family","") if a else ""), "et al" if len(a)>1 else "", "|", m.get("title",[""])[0][:100], "|", (m.get("container-title") or [""])[0][:45], "|", m.get("issued",{}).get("date-parts",[[None]])[0][0])
except Exception as e: print("NOT FOUND")')"
done
