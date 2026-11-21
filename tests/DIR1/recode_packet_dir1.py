#!/usr/bin/env python3
"""Build the blind-recode packet for the reviewer: titles and abstracts for data/recode_sample.json,
fetched with the same fallback order as search_dir1.py, WITHOUT the lead executor's codes.
Usage: python3 recode_packet_dir1.py > packet.md   (keep the packet outside the repository)"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from search_dir1 import abstract_for, get  # noqa: E402
S = json.load(open(Path(__file__).resolve().parent / 'data' / 'recode_sample.json'))
print('# DIR1 blind recode packet\n\nCode each item +1 / 0 / -1 per PREREG_DIR1.md section 5 for the cell rule shown. Do not open coded.csv first.\n')
for i, it in enumerate(S['items'], 1):
    w = get('https://api.openalex.org/works/' + it['openalex'].split('/')[-1])
    a, src = abstract_for(w)
    print(f"## {i}. {it['cell']} (prediction {it['prediction']}) — {it['title']}\nDOI {it['doi']}\n\n+1 means: {it['plus_means']}\n\n[{src}] {a}\n")
