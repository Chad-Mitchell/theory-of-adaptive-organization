# F1 data

Included here: prereg, results, analysis code, derived analysis datasets (`data/analysis_dataset.csv`, `data/analysis_dataset_E.csv`, measures, outcomes, sample flow), and power summaries.

Omitted (large raw SEC bulk files, about 3 GB total):

- `raw/companyfacts.zip`
- `raw/submissions.zip`
- `data/extract_C1.jsonl`, `data/extract_C2.jsonl`
- `power/sim_dataset.csv`

SHA-256 hashes of the two zip files, as used in the original run, are in `raw/companyfacts.sha256` and `raw/submissions.sha256`.

SEC bulk archives (as of 2026; confirm on the SEC site if a URL moves):

- https://www.sec.gov/files/companyfacts.zip
- https://www.sec.gov/files/submissions.zip

SEC requires a descriptive User-Agent identifying the requester. The preregistration used `Looper research research@example.invalid`. `download_sec.sh` in this folder uses that placeholder; replace the contact if you are the one downloading.

The extract and outcome scripts still point at `/workspace/gtao/tests/F1/raw/...`. Point them at this folder's `raw/` after the download.
