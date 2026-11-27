# Tests

Each included test keeps its locked prediction or preregistration file (and sha256 where one was written), the analysis code, and the results that exist. Large raw downloads, published-paper PDFs, full-text extracts, and clinical or personal data are not stored here. See each test's `DATA.md` (and `sources/INDEX.md` where present) for how to obtain excluded files. Hashed preregistration and prediction files have not been modified.

The headline scoreboard is in the repository `README.md`. For DECISIVE and F1 it follows the independent review in `reviews/DECISIVE_F1_REVIEW.md`.

**Local git histories.** These tests were preregistered in local, unpushed git repos. Their histories are recorded here so the original commit dates and SHAs are preserved, but the first external timestamp is the commit that adds them to this repository (14 November 2026; the repository was private then and has been public since 18 November 2026). Each test folder with a local history has a `history.txt` receipt (commit SHAs, dates, messages, and file lists with blob SHAs; no file contents). A `history.bundle` is included where the original commits can be shipped without reintroducing excluded data:

- Full bundles (original tip and all earlier commits): `ANTS1/`, `C3b/`, `F1/`.
- Prefix bundles (preregistration / locked-prediction commits only): `BIO1/`, `C3/`, `COLLAPSE1/`, `DRIFT1/`. Later commits in those repos contain publisher PDFs, large raw pulls, or withheld person-scale statistics.
- Receipt only (no bundle): `DECISIVE/` (every original commit contains clinical glucose data and other omitted raw inputs) and `MATCH1/` (the predictions commit already includes omitted source files).

Clone a bundle with `git clone history.bundle <dir>`. Author dates inside the bundles are self-attested.

| Folder | Status in this tree |
|---|---|
| `BIO1/` | Finished literature test. Local paper PDFs and extracts omitted; `sources/INDEX.md` lists what was used. |
| `COLLAPSE1/` | Finished. Paper PDFs/extracts omitted; SEC frame JSONs omitted; derived tables, the plot, and code are here. |
| `C3/` | Finished. Large GitHub pulls and the Valiev frame zip omitted; analysis dataset and results are here. |
| `C3b/` | Prereg locked; results not yet written. MV10 power gate not met at the largest n the frame supplies (`reviews/night2/C3B_GATE_ADDENDUM.md`), so it cannot give a reading as preregistered. Large screening dumps omitted. |
| `F1/` | Finished. Independent review: inconclusive, not a theory-specific hit; τ mostly measures fixed-cost share. SEC `companyfacts.zip` / `submissions.zip` (~3 GB) omitted; hashes, derived datasets, and a full `history.bundle` are here. |
| `DRIFT1/` | Finished for public domains. Raw pull files omitted. Person-scale arm withheld (`REDACTION.md`). |
| `ANTS1/` | Prereg locked; run finished 15 Nov 2026 (final analysis 01:54 ET). No RESULTS.md here; the write-up is `reviews/night1/ANTS1_WRITEUP.md` (CLAIM_MAP G13–G17: NOT EVIDENCE by construction, three SIM-FAILs). |
| `DECISIVE/` | Three locked preregs (banks, glucose, populations), each with a `RESULTS.md` and a `SUMMARY.md` at the top (written after the prereg commit). Independent review in `reviews/DECISIVE_F1_REVIEW.md`: banks are sign-only, not a HIT (CLAIM_MAP H11 PROXY-FAIL); the MATH_ATTACK literal joint miss condition fires on these proxies for populations on any reading and for glucose on the full sample (CLAIM_MAP H12, H13 PROXY-FAIL; proxy fails, not field misses). Raw and clinical data omitted; no `history.bundle` (those blobs are in every original commit); `history.txt` records the SHAs and dates. |
| `MATCH1/` | Finished. Locked predictions (sha256 checked), results, chart, code and derived curves. Raw headlines, Wikipedia revision dump and source files omitted (`DATA.md`). |
| `DIR1/` | Prereg locked `47c8594` (before retrieval). Directional, QC-tier literature test; reading INCONCLUSIVE (pooled 29/42; animals support; firms fail) after the coding corrections. Independent review: `reviews/dir1_2026-11-21/REVIEW.md` (READY-WITH-FIXES). Abstracts kept off-repo (publisher text); hashes in `DIR1/data/POOL_SHA256.json`, every code and exclusion with its quote or reason in `DIR1/data/coded.csv`. |

Not included: earlier Looper/AI-memory experiment notes that are not these tests.

Several analysis scripts still contain absolute paths from the machine they were run on (`<local>/gtao/tests/...`). They will need those paths pointed at a local `data/` or `raw/` directory after a download.
