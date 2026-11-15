# DRIFT1 redaction

The locked preregistration (`PREREG.md`, left unchanged so its sha256 still matches) named a person-scale arm that used a private personal journal. That journal is not in this repository, and it will not be.

In the copies of the results and code here:

- The person-scale row is removed from `RESULTS.md`. A placeholder notes that the arm was run and is withheld.
- Summary statistics for that arm are removed from `results.json`, `supp_results.json`, `analysis_output.txt`, and `supp_output.txt`.
- `analyze.py` and `supp.py` no longer read any journal path. They print a redaction notice instead.

The public-domain arms (GitHub, Wikipedia, EDGAR, NYC 311) are unaltered. The prereg file still describes the person-scale plan, because changing it would break the hash.
