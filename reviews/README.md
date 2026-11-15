Reviews of the theory notes, the tests, and the AI-memory toy. Independence is stated in each file. Chad's standing rule is that graders should be independent and blind; several of these passes do not meet that rule and say so.

| Path | What it reviews | Independence (as stated in the file) |
|---|---|---|
| `DECISIVE_F1_REVIEW.md` | The DECISIVE tests (banks, glucose, populations) and F1, with a rerun of every main analysis | Stated as an independent subagent that did not build either test. Not fully blind: the reviewer had the results and write-ups. Exploratory check scripts are in `DECISIVE_F1_review_checks/` (not preregistered). The repository scoreboard in `THEORY.md` §8 and the root `README.md` follows this review's verdict. |
| `theorems/REVIEW.md` | `THEOREMS.md` | Not independent (same executor, adversarial reread). |
| `math-attack/REVIEW.md` | `MATH_ATTACK.md` and `GENERAL_THEOREM.md`, with rerun checks | Stated as a separate hostile pass that did not write the reviewed files. |
| `architecture/REVIEW.md` | The fractal-architecture note and toy sim (the AI-memory application) | Not independent (same executor). |
| `independent-sim/REVIEW.md` | The same application math and toy, plus the reviewer's own re-derivations | Stated as an independent pass. The full sim rerun lives in the public [`adaptive-memory-levels`](https://github.com/Chad-Mitchell/adaptive-memory-levels) `review/` folder; only the review text and independent checks are copied here. |

Test-specific reviews (for example `tests/C3/REVIEW.md`) stay with those tests.
