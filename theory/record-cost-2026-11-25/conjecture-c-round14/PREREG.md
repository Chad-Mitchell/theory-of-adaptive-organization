# Preregistration: Conjecture C, round 14 (part M)

Written 2026-11-26 at about 03:30 EST. It is committed and pushed to the fork branch before any of its scripts runs. The lock is in `PREREG.sha256`, which hashes this file and the three scripts. Labels follow the repo: PROVED (in-model), OBSERVED (numerical), KNOWN, HYPOTHESIS, open miss. A run that does not finish is reported as **not tested**, never as a hit.

## 0. Disclosures

- **Round 13.** The round 13 preregistration (`PREREG_ROUND13_SESSION.md`, sha256 `35c19ee9251ac8ccbca92761f90bc922e890c06db48cb26f03e1fe14dad29e1b`, an identical copy) was hash-locked in the session notes at 01:47 EST, before its runs. It was not pushed before them, so it counts only as a local lock.
  - Its results were H3, H4 and H5 hits, and H1 and H2 not tested.
  - The H2 value sub-prediction was a miss: an LP-ascent search found a maximum Φ of −0.233437 at non-zero marginals, against the predicted −0.444582.
  - The H2 prediction below uses that search value. That is a disclosed look at the data.
- **Development runs.** None of the three round 14 scripts was executed before this lock; they were only byte-compiled (`py_compile`). Earlier versions of the same tests were run in round 13. Those were the float-classified version of H3, a hexagon² family for H4, and the symmetric three-square composite for H5. The round 14 instances are new: exact classes for H3, square × hexagon for H4, and non-symmetric three-square composites for H5.
- **How to run.** From this directory with `PYTHONPATH=../scripts/selfref` (for `m_round11_lib` and `m_round12_parts`); needs numpy, sympy, networkx, scipy, pycddlib and lrslib (`lrs`, `redund`).
- **Box.** The box has 8 cores and is shared with other workers. A time limit is part of each test.

Notation: Φ(x) = m_A m_B (‖C‖² − 1) − m_A (1 − |a|²) − m_B (1 − |b|²), in invariant Euclidean coordinates with circumradius 1. Condition (♦) is "Φ ≤ 0 at every non-product extreme point" (§16 of the round 10 note).

## H1: icosahedron², condition (♦) on max(I, I)

- *Script.* `r14_h1h2_enum.py IxI`: full float vertex enumeration with pycddlib. The 20 largest-Φ non-product vertices are then re-checked exactly in Q(√5): each must be feasible, with tight rank 16.
- *Time limit.* 120 minutes.
- *Predictions.*
  - (a) The enumeration finishes in time. Prior 30%.
  - (b) If it finishes, (♦) holds and max Φ = −2.541438 ± 1e-5 at a = b = 0. Prior 70%.
- *Miss.* Any non-product vertex with Φ > 1e-9, or a failed exact re-check.

## H2: dodecahedron², condition (♦) on max(D, D)

- *Script.* `r14_h1h2_enum.py DxD`.
- *Time limit.* 120 minutes.
- *Predictions.*
  - (a) The enumeration finishes. Prior 50%.
  - (b) (♦) holds, and max Φ = −0.233437 ± 1e-5 at non-zero marginals. Prior 70%; this uses the round 13 search, see §0.
- *Miss.* As for H1.

## H3: icosahedron × dodecahedron, exact automorphism search

- *Script.* `r14_h3_exact.py`. This is the facet-grid search of round 13, with the K-value classes computed exactly in Q(√5).
- *Prediction.* Fixing facet 0, no automorphism sends a same-row or same-column partner to a non-partner. Every automorphism of max(I, D) is then local, so there is no entangling automorphism. Prior 95% (Al-Safi–Richens Theorem 1 implies it).
- *Time limit.* 90 minutes.

## H4: a new non-symmetric family, square × hexagon

- *Script.* `r14_h4h5.py h4`, exact.
- *Family.* 23 composites in all:
  - S = conv(min ∪ R), with R a random k-subset of the non-product vertices of max(□, hexagon), k ∈ {2, 4, 6, 10}, 5 seeds each (20 composites);
  - a near-symmetric stress case: max(□, hexagon) minus one non-product vertex, 3 seeds.
- *Prediction.* No entangling automorphism in any of the 23. Prior 85%. An UNDECIDED (search limit) result counts as not tested for that composite.
- *Time limit.* 120 minutes.

## H5: new three-part composites without full symmetry

- *Script.* `r14_h4h5.py h5`, exact.
- *Composites.* Three squares with:
  - the PR boxes placed only on the pair AB (with every pure C);
  - PR boxes on AB and BC only;
  - a single PR box on AB.
- *Prediction.* No entangling automorphism in any of the 3, meaning no linear automorphism maps a product pure state to a non-product extreme point. Prior 90%.
- *Time limit.* 60 minutes.

## What would count against Conjecture C

An automorphism found in H3, H4 or H5 would be rebuilt as an exact linear map and reported first as a counterexample. That would be a counterexample to C without local symmetry for H4 and H5, and a pipeline fault for H3. A non-product vertex with Φ > 0 in H1 or H2 would mean (♦) fails there, so M12 says nothing for those parts. It would not be a counterexample to C.
