# DRIFT1 data

Included: prereg, code, derived results (with the person-scale arm redacted; see `REDACTION.md`).

Omitted raw pulls (re-fetch with the `fetch_*.py` scripts):

- NYC 311 (Socrata dataset `erm2-nwe9`): complaint-type × community-board counts for 2025, and hourly counts 2020–2025.
- SEC EDGAR: a sample of filers from `company_tickers.json` and their recent filing dates (EDGAR submissions JSON).
- English Wikipedia: revision timestamps for a random sample of main-namespace articles (MediaWiki API).
- C3 GitHub issue/commit inputs, which live in the omitted C3 raw pulls; derived C3 lists included under `../C3/data/` may be enough for some reruns.

SEC and Wikipedia APIs want a descriptive User-Agent. Copies of the fetch scripts in this repo use `research@example.invalid` in place of the original research contacts.
