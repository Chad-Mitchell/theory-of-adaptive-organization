# Preregistration — Round 13 (part M): hostile-review follow-ups on Conjecture C
Written 2026-11-26 01:47 EST, before any of the runs below. Locked by sha256 (PREREG_ROUND13_M.md.sha256, WORKLOG line).
Labels as usual. A run that does not finish is reported as "not tested", never as a hit.

Notation: Φ(x) = m_A m_B(‖C‖² − 1) − m_A(1 − |a|²) − m_B(1 − |b|²), invariant Euclidean coords, circumradius 1.
"Entangling automorphism" = linear automorphism of S mapping some product pure state to a non-product extreme point.

## H1 — icosahedron², maximal composite (♦)
Prediction: ♦ holds on every extreme point of max(I,I): max Φ over non-product extreme points < 0, and equals the
zero-marginal LP value −2.541438 to within 1e-5 (the maximiser has a = b = 0). Prior: 70% for ♦, 55% for the value.
Method: vertex enumeration (coordinates are in Q(√5), so lrs cannot run on them directly; float cdd/lrs-on-scaled data,
each reported vertex re-verified exactly in Q(√5) where feasible). Miss: any non-product vertex with Φ > 1e-9.

## H2 — dodecahedron², maximal composite (♦)
Prediction: ♦ holds on max(D,D); max Φ = −0.444582 ± 1e-5 at a = b = 0. Prior: 60% for ♦, 50% for the value.
Same method and miss criterion as H1.

## H3 — icosahedron × dodecahedron, direct automorphism search on max(I,D)
Prediction: no entangling automorphism; the colour-refinement classes separate product pure states from all other
extreme points, or the backtracking search exhausts with none found. Prior: 95% (Al-Safi–Richens Thm 1 implies it; this
is a check of the pipeline on a case where ♦ fails, Φ = +2.05).

## H4 — a non-symmetric composite family (no local symmetry assumed)
Family: hexagon × hexagon with the exact rational affine hexagon; S = conv(min ∪ R), R a random k-subset of the
non-product extreme points of max (k = 1, 2, 3, 5, 8; 6 seeds each = 30 composites), plus the same with each chosen
point mixed with the maximally mixed state at weight 1/4 (30 more). Test: for every colour class of product pure
states, search an automorphism to every non-product extreme point sharing a class.
Prediction: no entangling automorphism in any of the 60 composites. Prior: 90%.
Miss: one found (then rebuilt as an exact linear map and reported as a counterexample to C without local symmetry).

## H5 — a three-part case
Composite: three squares (boxworld bits), S3 = conv(min(□,□,□) ∪ {PR_k ⊗ v placed on each of the 3 pairs; k = 1..8,
v a vertex of the third square}). Test as in H4 (all product classes).
Prediction: no entangling automorphism; product pure states are separated by colour refinement. Prior: 90%.
Secondary prediction (HYP): the orbit argument of M12 extends to n parts with Φ_n = Σ over non-empty subsets of
weighted (norm² − 1) terms, and ♦_n holds for S3. Prior: 60%. Only reported if worked out.

## What would count against the M-thread
A hit on any miss criterion in H3–H5 is a counterexample or a pipeline fault and would be reported first.
