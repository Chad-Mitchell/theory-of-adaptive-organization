# MATCH1 data

Included here: the locked predictions (`PREDICTIONS.md`, `PREDICTIONS.sha256`; original commit 71d8306, 22:55 ET, 14 Nov 2026), `RESULTS.md` (original commit f532a83), the chart, all analysis code, and derived curves and result files (need-odds CSVs, per-repo results, fitted curves, layer fits).

Omitted (raw third-party data, or files whose redistribution terms were not checked):

- `news/abcnews-date-text.csv` (about 61 MB): "A Million News Headlines" (ABC News), as mirrored on Hugging Face at `DeveloperOats/Million_News_Headlines`. Download it there and place it in `news/`.
- `wiki/revisions.jsonl` (about 3 MB): Wikipedia revision metadata for 400 random articles. `wiki/fetch.py` re-fetches it from the public MediaWiki API (random sampling, so a re-fetch draws different articles).
- `sources/`: the original run's local copies of
  - Antia et al. 2018 (measles antibody cohort) S1 Data and supplements, from the article's PLOS Biology supplementary files;
  - Meeter, Murre & Janssen 2005 news-recall data (`data.zip`), from the authors' published dataset;
  - the `tsiR` R package (version 0.4.3) measles data for England and Wales towns, 1944–65, from CRAN;
  - saved web pages used for prior-art notes (Challet & Lombardoni 2008; Lee, Flack & Krakauer 2024).

The code repositories in `code/` were cloned from their public GitHub homes at the heads listed in the run; `code/run.py` re-derives the need-odds curves from `git log`.

Contact strings in `openalex/fetch.py` and `wiki/fetch.py` were replaced with `research@example.invalid`. Put your own contact there before re-fetching (both APIs ask for one).

