# COLLAPSE1 data

Included here: `collapse_data.csv`, `collapse.png`, `plot.py`, firm-level derived tables (`firm/firm_panel.csv`, `firm/industry_slopes.csv`, `firm/summary.json`, `firm/sic.json`), code-need outputs, and the locked prediction files.

Omitted:

- `sources/` PDFs, HTML, and full-text extracts of published papers (copyrighted). See `sources/INDEX.md` for the public URLs and DOIs.
- `firm/raw/` SEC XBRL frame JSON (re-fetchable). The fetch script is `firm/fetch.py`. SEC requires a descriptive User-Agent; the copy in this repo uses `research@example.invalid` (replace with a real contact if you are pulling from SEC). Endpoint pattern:
  `https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json`
  and the submissions / SIC lookup used in `firm/sic.py`.
- Cloned git histories of numpy, django, and rails. `code_need/repo_heads.txt` records the heads that were analyzed; `code_need/need.py` walks a local clone.

Code histories: clone the public repos at the recorded heads and rerun `code_need/need.py`.
