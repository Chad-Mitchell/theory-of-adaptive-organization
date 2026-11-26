# Conjecture C, round 14: results against the pushed lock

Lock: `PREREG.md`, sha256 `523dfb533dfb88eaf25c1ae7fb13c24c38b5f6a766cd846d236318593d787532`, pushed in commit 4e189c6 at about 03:54 EST on 2026-11-26. The hashes in `PREREG.sha256` were re-checked before the runs. All five runs started at 03:55:07 EST, in parallel, from the pushed tree, on the shared 8-core box. An earlier launch at 03:54:58 failed before any Python ran (`LAUNCH_FAIL_0355.txt`). Scoring uses the script outputs as printed; a run that did not give a valid test is scored **not tested**.

| Test | Output | Score |
|---|---|---|
| H5, three squares, three non-symmetric PR placements | `r14_h5.stdout`: 3 of 3 CERTIFIED (colour refinement separates products from the rest), 9 s | **hit** (exact certificate for each of the 3 composites) |
| H4, square × hexagon, 23 composites | `r14_h4.stdout`: 23 of 23 CERTIFIED, 6 s | **hit** (exact certificate for each composite) |
| H3, icosahedron × dodecahedron, exact facet-grid search | `r14_h3.stdout`: finished in 60 min; 413 "exact" K classes; no automorphism found, none undecided | **not tested** (pipeline fault, below) |
| H1, icosahedron², vertex enumeration of max | pending | |
| H2, dodecahedron², vertex enumeration of max | pending | |

**H4 caveat.** In the 20 random composites, separation is cheap because random subsets break almost all symmetry. The three "max minus one" composites keep much more symmetry (143 extreme points, 46 to 77 classes) and are the stronger part of the test.

**H3 pipeline fault.** The printed outcome matches the prediction, but the run is not a valid test. Round 13 found 20 K values in floating point, with a gap of 1.1e-3 between them. The round-14 script found 413 "exact" classes because sympy's `radsimp` does not give a canonical form in Q(√5). A post-run diagnostic (`postrun_diag_h3_classes.py` / `.stdout`; not part of the lock) shows this: the icosahedron's factor Gram has 58 symbolic forms for 6 values, and the dodecahedron's has 6 forms for 4 values. Over √5 these reduce to 6 and 4, and their products take 20 values. Classes that are too fine can only rule out candidate maps, so "none found" is not a certificate. H3 is scored not tested. It is not rerun under this lock; a corrected run (values written as p + q√5 with p and q rational) would need a new, pushed preregistration.

## Final scorecard (added 2026-11-26, about 06:03 EST; the "pending" rows above are superseded)

| Test | Output | Score |
|---|---|---|
| H1, icosahedron², float vertex enumeration of max(I, I) | `r14_IxI.stdout`: no output; `timeout 120m` ended it (exit 124, logged at 06:01:45 EST) | **not tested** (time limit) |
| H2, dodecahedron², float vertex enumeration of max(D, D) | `r14_DxD.stdout`: no output; ended by the timeout (exit 124, logged at 06:01:45 EST) | **not tested** (time limit) |
| H3, icosahedron × dodecahedron | pipeline fault (above) | **not tested** |
| H4, square × hexagon, 23 composites | 23 of 23 certified | **hit** |
| H5, three squares, 3 composites | 3 of 3 certified | **hit** |

- **Totals.** 2 hits, 0 misses, 3 not tested. Neither H1's nor H2's value sub-prediction was reached.
- **Clock note.** The wall-clock span from the START line (03:55:07) to EXIT (06:01:45) is about 126.6 minutes, against the 120-minute `timeout`. At 05:56:33 `ps` reported an elapsed time of 1:54:50 for both processes, which puts the process start at about 04:01:43 by the later clock. The box clock appears to have stepped by about 6.6 minutes after the 03:20 restart. The limit was enforced by `timeout`, and nothing was extended.
- **Follow-up outside this lock.** The H3 fix was preregistered and run separately: round 15 was not tested (the script crashed), and round 16 was a hit. See `../conjecture-c-round15/RESULTS.md` and `../conjecture-c-round16/RESULTS.md`.
