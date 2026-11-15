# Tests

Each included test keeps its locked prediction or preregistration file (and sha256 where one was written), the analysis code, and the results that exist. Large raw downloads, cloned git histories, published-paper PDFs, and full-text extracts are not stored here. See each test's `DATA.md` (and `sources/INDEX.md` where present) for how to obtain excluded files.

The headline scoreboard is in the repository `README.md`.

| Folder | Status in this tree |
|---|---|
| `BIO1/` | Finished literature test. Local paper PDFs and extracts omitted; `sources/INDEX.md` lists what was used. |
| `COLLAPSE1/` | Finished. Paper PDFs/extracts omitted; SEC frame JSONs omitted; derived tables, the plot, and code are here. |
| `C3/` | Finished. Large GitHub pulls and the Valiev frame zip omitted; analysis dataset and results are here. |
| `C3b/` | Prereg locked; results not yet written. Large screening dumps omitted. |
| `F1/` | Finished, inconclusive under the prereg. SEC `companyfacts.zip` / `submissions.zip` (~3 GB) omitted; hashes and derived datasets are here. |
| `DRIFT1/` | Finished for public domains. Raw pull files omitted. Person-scale arm withheld (`REDACTION.md`). |
| `ANTS1/` | Prereg locked; run incomplete; `results.pkl` is a partial artifact; no RESULTS.md. |
| `DECISIVE/` | Three locked preregs (banks, glucose, populations), each now with a `RESULTS.md` and `SUMMARY.md` at the top (written after the prereg commit; not independently reviewed). Raw and clinical data omitted. |
| `MATCH1/` | Finished. Locked predictions (sha256 checked), results, chart, code and derived curves. Raw headlines, Wikipedia revision dump and source files omitted (`DATA.md`). |

Not included: earlier Looper/AI-memory experiment notes that are not these tests.

Several analysis scripts still contain absolute paths from the machine they were run on (`/workspace/gtao/tests/...`). They will need those paths pointed at a local `data/` or `raw/` directory after a download.
