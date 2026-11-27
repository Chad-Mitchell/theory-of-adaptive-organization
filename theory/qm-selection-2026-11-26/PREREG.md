# Preregistration: frozen premise list for the QM-selection chain, and the round 9 counterexample search

*Thursday 26 November 2026 (America/New_York). Branch `forge-rnd-record-cost-2` (PR #295). Written after a fresh-context hostile review of the foundations (session file `HOSTILE_REVIEW_FOUNDATIONS.md`, risk 2: "premise accretion that selects quantum theory by filter"). This file, `PREREG.sha256` and the search script go in their own commit. Results go append-only in `RESULTS.md`; changes to this file go in `DEVIATIONS.md` and never edit it. `THEORY.md`, `CORE.md` and locked blobs are not touched.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The sentence is copied byte for byte from `CORE.md:7`. Labels: **PROVED (in-model)**, **OBSERVED (numerical)**, **KNOWN**, **HYPOTHESIS**, **OPEN**, **open miss**.

## 0. Prior knowledge, disclosed (read this first)

- The author is the agent applying the hostile-review fixes to PR #295. It did not write rounds 9 and 10, but it read them and the review before this lock.
- **Before this lock the author sketched the analytic reduction in §3 and ran a development version of `search_u2_sp1sp1.py` once, and saw its outcome (no hit).** The script was then edited only for output wording, a duplicate-point count and the removal of dead code; no candidate, premise or rule changed after that run. So the search below is **not blind**. Its value is (i) to freeze the premise list now, so that every later premise has to be logged as a deviation together with the counterexample that prompted it, and (ii) to put the search and its certificates on record. By G2 of `process/PREREG_GATE.md` the search outcome is close to a `CONSISTENCY_CHECK`: it is fixed by known theorems (the maximal torus theorem) plus the arguments in §3, which are not yet independently checked.
- No separate gate reader read this file before the run. That is a deviation from `process/PREREG_GATE.md` §2, stated here up front, not after the fact. The search outcome should be treated as unreviewed until an independent reader checks §2–§3.

## 1. The frozen premise list for the QM-selection chain (rounds 8–10)

These are the premises the chain from the cost to complex quantum theory uses, as of round 10 (`theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §5–§8, `theory/RECORD_COST_ROUND10_2026-11-25.md` §8, `theory/RECORD_COST_ERRATA_2026-11-26.md`). Each is a premise (HYPOTHESIS) unless marked otherwise. **From this lock on, any new premise, or any change to one below, is logged in `DEVIATIONS.md` with its date and the counterexample that prompted it.**

| id | premise | where it was added | what it excludes |
|---|---|---|---|
| P1 | **State space.** A record's normalized state space is a compact convex body K of finite affine dimension d, with all affine effects 0 ≤ e ≤ 1 allowed (no-restriction). | chain note; round 10 §15 for no-restriction | restricted theories such as stabilizer theory |
| P2 | **Transitivity.** The reversible group acts transitively on the pure states (extreme points), and there are at least two. | chain note | non-homogeneous bodies |
| P3 | **U.** The reversible group is infinite ("tracking never finishes"). With P2 and compactness it has positive dimension. Not derived (README row RECORD-COST-U). | round 4 | polytopes (finite groups) |
| P4 | **Group rule (new, from the review).** "Reversible" means the identity component G₀ of the compact affine symmetry group of K, and P2 is required of G₀. The same rule applies to every candidate. | this lock | the O(3) loophole: with full O(3) the qubit fails SFP (−I) |
| P5 | **hSFP.** For K and for every face F of K with at least two extreme points, every element of the identity component of the setwise stabilizer of F in G₀ fixes at least one extreme point of F. | rounds 7–9 (SFP), round 8 (heredity) | real QM (disk faces), even balls, C1 |
| P6 | **Cost: the cheapest bit and the dimension price.** Among bodies that satisfy P1–P5, with capacity N (the largest number of perfectly distinguishable states), a smaller affine dimension d is cheaper. Every bit face of a higher-rank body is the cheapest bit. The dimension price is not derived from additivity (chain note `:98`). | chain note S5; round 8 | quaternionic, octonionic, odd balls of dim ≥ 5 |
| P7 | **Jordan class** (or strong symmetry, Barnum–Hilgert). K is the state space of a Euclidean Jordan algebra. | round 8 | every non-Jordan body by fiat |
| P8 | **Lattice route only (round 10 §8):** records form an irreducible, atomistic, orthocomplemented lattice with the covering property ("orthocomplement = perfectly distinguishable from"). Not used by the search below. | round 10 | reducible or non-covering lattices |

Known consequences, recorded so they are not mistaken for extra content: P2 + P5 on finitely many pure states is impossible (Jordan's theorem), so P5 + P2 imply P3; and P7 does most of the selection, since in the Jordan class "the bit is the 3-ball" already picks complex quantum theory (errata §1).

## 2. The search, and what counts as a hit (Gate)

Round 9 named the next search (rounds 4–9 note §9 item 6; session note R9.4 item 2): non-Jordan transitive bodies in affine dimension 4–8 for other compact groups, for example U(2) and Sp(1)×Sp(1). The question it answers: **do P1–P6 select complex quantum theory without P7, at least for these two groups in dimensions 4–8?**

**Candidates.** Every orbitope K = conv(G·v) where G is U(2) or Sp(1)×Sp(1) acting by a real representation, v any vector, and the affine dimension of K is between 4 and 8. (A body whose pure states form one orbit of a compact group is the orbitope of that orbit.)

**Gate.**
- **G1. Hit.** A candidate that satisfies P1–P5 under P4, is not affinely isomorphic to a Jordan-algebra state space, and has capacity N with d < N² − 1 (complex quantum theory's dimension at capacity N) is a **HIT**: then P1–P6 do not select quantum theory without P7. d = N² − 1 is a **TIE** and is reported as a hit for P6 (the cost does not separate it). Otherwise **MISS**. Honest odds of a hit before the development run: low, about 1 in 10, the risk being an error in the reduction of §3; after it, see §0.
- **G2. Not an identity.** The outcome depends on a classification statement (§3) that was not proved before tonight; it is fixed once §3 is accepted. Label: close to `CONSISTENCY_CHECK` (§0).
- **G3. Rival.** "P7 is needed": the round 9 orbitope C1 (spin-1+2, dim 8, capacity 4) passes SFP and beats quantum theory on dimension, so outside the Jordan class plain SFP already admits a body cheaper than quantum theory. The rival predicts that some U(2) or Sp(1)×Sp(1) body passes hSFP too.
- **G4. Reach.** Level (a), a toy classification. A miss narrows the role of P7 for these groups; a route to (b) is a general classification of hSFP orbitopes.
- **G5. Next step.** Hit: log the body as a counterexample to "P1–P6 select QM", keep P7 as load-bearing, and test it against the chain note's composite rules. Miss: P7 is not needed for U(2) and Sp(1)×Sp(1) in dimensions 4–8; the next search is groups of rank ≥ 2 with larger dimension (SU(3), Sp(2), G₂) and dimensions 9–15.

## 3. Method (locked)

1. **Reduction (PROVED (in-model) from KNOWN theorems).** By the maximal-torus criterion (rounds 4–9 note §5, Hopf–Samelson), SFP for a connected compact G on G/H requires H to contain a maximal torus, so some point of the orbit is fixed by the standard maximal torus T: v may be taken in the zero-weight space of T. The centre lies in every maximal torus, so v is fixed by the centre.
   - U(2): the irreducible representations are Sym^k ⊗ det^m with central character z^(k+2m); a zero weight exists iff k + 2m = 0, i.e. the representation factors through SO(3) with spin k/2. So every SFP orbit of U(2) is an SO(3) orbit of a zonal vector in a sum of integer-spin representations.
   - Sp(1)×Sp(1): a zero weight of V_j1 ⊗ V_j2 exists iff j1 and j2 are both integers, so the group acts through SO(3)×SO(3); in real dimension ≤ 8 the only such irreducibles are (j, 0) and (0, j). So every SFP orbit is a product of SO(3) zonal orbits, and its orbitope is a product of bodies.
   - Candidates in affine dimension 4–8 are therefore: Z2 (spin-2 zonal, = real QM d = 3, dim 5), Z3 (spin-3 zonal, dim 7), the family K_θ (spin-1 ⊕ spin-2 zonal, dim 8, θ ∈ (0, π/2); C1 is tan θ = √(2/3)), B3 × B3 (dim 6), B3 × Z2 (dim 8), and B4 (the defining representation, which fails SFP). Spin-1 ⊕ spin-1 zonal orbits have dimension 3.
2. **hSFP failure certificate.** An exposed face that is the convex hull of a circle of distinct pure states on which an SO(2) in G₀ acts by rotation fails P5. For K_θ and Z2 the invariant functional (0, −Y20) is maximized exactly on the equator (the function −P2(cos ϑ) has its unique maximum at ϑ = π/2), giving such a face.
3. **hSFP pass argument.** If a proper face F has a positive-dimensional stabilizer, it is invariant under an SO(2); averaging an exposing functional over that SO(2) stays in F's normal cone, which is pointed, so it is non-zero and exposes an SO(2)-invariant face containing F. For Z3 the only invariant functionals are ±Y30, maximized only at the poles, so F is a point. For B3 × B3 faces are products of faces of balls.
4. **Capacity.** A centrally symmetric body has capacity 2: for e = c + ℓ ≥ 0, e(x_i) = 1 ≤ c + max ℓ ≤ 2c, and the constants of a measurement sum to 1. Z3 (odd degree) and B3 × B3 are centrally symmetric. LP attempts on grid points are run as a numerical check.
5. **Numerical checks** in `search_u2_sp1sp1.py` (seed 20261126): weight counts and a torus fixed-space check; affine dimensions; the circle faces; the Z3 pole uniqueness; LP capacity attempts; generic orbits failing SFP.

The output is `search_u2_sp1sp1.out`. The script's sha256 is in `PREREG.sha256`.
