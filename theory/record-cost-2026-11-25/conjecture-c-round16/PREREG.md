# Conjecture C, round 16 (part M): icosahedron × dodecahedron with canonical exact classes, second attempt — preregistration

Written 2026-11-26 at about 05:15 EST. It is committed and pushed to the fork branch before its script runs. The lock is in `PREREG.sha256`, which hashes this file, the script and the pre-lock toy test. Labels follow the repo. A run that does not finish, crashes, or fails its validity check is reported as **not tested**, never as a hit.

## Why this round exists

- **Round 14.** H3 was not tested: its exact classes were not canonical.
- **Round 15.** H3′ was not tested: the script crashed in its product step (`AlgebraicField` has no `from_list`), before the search; see `../conjecture-c-round15/RESULTS.md`. Neither round is rerun under its own lock.
- **This round.** `r16_h3_canonical.py` differs from `r15_h3_canonical.py` only in the header comment and the class step. Values stay as field elements (sympy ANP), are multiplied in the field and are compared by their unique coefficient list.

## Disclosures

- **What is already known about this instance.** From round 13 (float), the round 14 diagnostic and round 15 (which printed per-factor classes 6 and 4 before crashing): 6 and 4 values per factor, 20 product values, and 1 row pair and 397 column pairs to try. V1 and V3 below are consistency checks with those numbers; only V2 is the test.
- **Development runs.** The script was not executed on the icosahedron/dodecahedron data before this lock; it was only byte-compiled. Every new helper (`elt`, `key`, `fmul`, `tofloat`) and the class bookkeeping were exercised before the lock on toy numbers only: `PRELOCK_toy_helpers.py` / `.stdout` gives 3 and 4 toy classes and 12 product classes, which agrees with a float count. The facet set-up and the search are unchanged from round 14, where both ran.
- **How to run.** From this directory with `PYTHONPATH=../scripts/selfref`; needs numpy, sympy and scipy. Shared 8-core box.

## The test (H3″): icosahedron × dodecahedron, exact automorphism search on max(I, D)

- *Validity check (V1).* The script prints 6 and 4 per-factor classes and 20 canonical distinct K values. Any other count is a pipeline fault and is scored not tested. Prior 95%.
- *Prediction (V2, the test).* Fixing facet 0, no automorphism sends a same-row or same-column partner to a non-partner, with 0 undecided in both searches. Every automorphism of max(I, D) is then local, so there is no entangling automorphism. Prior 95% (implied by Al-Safi–Richens Theorem 1, KNOWN). A hit is an exact certificate for this one maximal composite, labelled PROVED (in-model) and consistent with the KNOWN theorem.
- *Consistency (V3).* 1 row pair and 397 column pairs tried. Prior 80%. A mismatch is reported but does not change V2.
- *Miss.* Any automorphism found is rebuilt as an exact linear map and checked for a pipeline fault first. It is reported as a miss of V2.
- *Not tested.* Any undecided pair, a crash, a V1 failure, or no output within the time limit.
- *Time limit.* 90 minutes wall clock from launch.
