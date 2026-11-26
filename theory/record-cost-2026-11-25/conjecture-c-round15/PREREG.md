# Conjecture C, round 15 (part M): icosahedron × dodecahedron with canonical exact classes — preregistration

Written 2026-11-26 at about 05:15 EST. It is committed and pushed to the fork branch before its script runs. The lock is in `PREREG.sha256`, which hashes this file and the script. Labels follow the repo: PROVED (in-model), OBSERVED (numerical), KNOWN, HYPOTHESIS, open miss. A run that does not finish, crashes, or fails its own validity check is reported as **not tested**, never as a hit.

## Why this round exists

Round 14's H3 (`../conjecture-c-round14/RESULTS.md`) was scored not tested: its "exact" value classes were not canonical (413 classes; sympy's `radsimp` is not a normal form in Q(√5)). Round 14 is not rerun under its own lock. This round repeats the test with a different script under a new lock.

## Disclosures

- **What is already known about this instance.** The round 13 float run found 20 K values (gap 1.1e-3) and tried 1 row pair and 397 column pairs, finding no automorphism. The round 14 post-run diagnostic (`../conjecture-c-round14/postrun_diag_h3_classes.stdout`) found 6 and 4 values per factor and 20 product values after reducing over √5. So V1 and V3 below are consistency checks with known numbers, not independent predictions. Only V2 is the test.
- **Development runs.** `r15_h3_canonical.py` was not executed before this lock; it was only byte-compiled. The canonical-form helper (`QQ.algebraic_field(sqrt5).from_sympy`) was tried on three unrelated toy numbers ((1+√5)², 6+2√5, 1/(3−√5)) and nothing else. Lines 4–27 (setup and facets) and lines 44–88 (the search) are lines 3–26 and 34–78 of `../conjecture-c-round14/r14_h3_exact.py`, unchanged. Only the class computation changed.
- **How to run.** From this directory with `PYTHONPATH=../scripts/selfref`; needs numpy, sympy and scipy. Shared 8-core box.

## The test (H3′): icosahedron × dodecahedron, exact automorphism search on max(I, D)

- *Script.* `r15_h3_canonical.py`. Every K value is mapped into the number field Q(√5) and compared by its unique coefficient pair (p, q) of p + q√5.
- *Validity check (V1).* The script prints 20 canonical distinct K values (and 6 and 4 per factor). If it prints any other count, the run is a pipeline fault and is scored not tested. Prior that it prints 20: 95%.
- *Prediction (V2, the test).* Fixing facet 0, no automorphism sends a same-row or same-column partner to a non-partner, with 0 undecided in both searches. Every automorphism of max(I, D) is then local, so there is no entangling automorphism. Prior 95% (Al-Safi–Richens Theorem 1 implies it, KNOWN). A hit makes this an exact certificate for this one maximal composite, labelled PROVED (in-model), consistent with the KNOWN theorem.
- *Consistency (V3).* 1 row pair and 397 column pairs tried, as in round 13. Prior 80%. A mismatch is reported but does not change the V2 score.
- *Miss.* An automorphism found would first be rebuilt as an exact linear map. If it is genuine and entangling, it contradicts the KNOWN theorem, so a pipeline fault would be checked first. In either case it is reported as a miss of V2.
- *Not tested.* Any undecided pair (search limit), a crash, a V1 failure, or no output within the time limit.
- *Time limit.* 90 minutes wall clock from launch.
