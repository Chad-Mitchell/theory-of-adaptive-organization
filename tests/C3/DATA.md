# C3 data

Included here: the analysis dataset, measures, sample lists, outcome JSONL, results, and code. See also `DATA_NOTES.md`.

Omitted (large or readily re-downloaded):

- `data/package_urls.csv` and `data/valiev_min.zip`, the Valiev, Vasilescu & Herbsleb 2018 sample frame. Source: Zenodo record [1297925](https://zenodo.org/records/1297925), file `dataset_minimal_Jan_2018.zip`.
- `data/screen.jsonl` and `data/issues.jsonl`, the GitHub GraphQL/REST pulls. `code/screen.py` and `code/issues.py` rebuild them from the frame, using the `gh` CLI (public repo metadata only).

`download_frame.sh` in this folder fetches the Zenodo zip and extracts `package_urls.csv`.
