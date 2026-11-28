# DECISIVE data

Three locked preregistrations, one per scale. Raw inputs are not stored here.

## Banks (D1)

Predictors: FDIC BankFind Suite API, `https://api.fdic.gov/banks/financials`, quarterly filings 2001Q1–2007Q4.

Outcomes: FDIC failed-bank records, `https://api.fdic.gov/banks/failures`, RESTYPE = FAILURE, FAILDATE 2008-01-01 through 2014-12-31, matched by CERT.

Pullers: `banks/code/pull_predictors.py` and the outcome calls in `banks/code/analyze.py`. Omitted here: `financials_2001_2007.csv`, `predictors.csv`, `failures.csv`, and related raw tables.

Each arm has a machine-written `results.json` (and an `exploratory.json` where one was produced) written after that arm's preregistration commit. There is no `RESULTS.md` and no review. The code's own verdict labels in those files are **not** the official score. Do not score any arm until it is written up.

## Glucose (D2)

Clinical continuous-glucose recordings. **Not included** (privacy and license: use the official sources, and do not commit individual traces).

Sources named in the preregistration:

- ShanghaiT1DM/T2DM: Zhao et al. 2023, *Scientific Data* 10:35, CC BY 4.0. Figshare 20444397; a CC-BY-4.0 re-archive is Zenodo record 18604027.
- REPLACE-BG: Aleppo et al. 2017, *Diabetes Care*; Jaeb Center public-use release (acknowledgement required); same Zenodo record in the original run.
- Colas et al. 2019, *PLOS ONE* S1 data, CC BY. Used only in the planned cross-cohort collapse.
- OhioT1DM was not used (data-use agreement).

`glucose/code/load.py` and `features.py` expect the raw recordings under `glucose/data/`. First-block predictors and the second-block file are also omitted, so the outcome cannot be computed from this tree alone.

## Populations (D3)

Global Population Dynamics Database, official CSVs from KNB, doi:[10.5063/F1BZ63Z8](https://doi.org/10.5063/F1BZ63Z8). GPDD terms ask for citation. The `data/knb/` dump, GPDD `.rda` files, predictors, and the outcome block are omitted.

`populations/code/features.py` rebuilds predictors from a local KNB download.
