# Hostile review: C12CG.md §§0–9 (C12c-G′ and C12c-G″), with `c12cg/` scripts and outputs

*26 Nov 2026, 10:50–11:10 EST. Local note only (no commits, no pushes, no email). The reviewer did not write the target. Repo text was read from a fresh clone of `mitchell-moving/theory-of-adaptive-organization`, branch `forge-rnd-record-cost-2`, head `a57f1f7` (confirmed with `git ls-remote`). The target read `ac92ee2`; `git diff --stat ac92ee2 a57f1f7` touches only Lean and qm-selection-3 files, so RECORD_COST_CHAIN, `r2_record_pricing.py`, `nocloning/polygons.py` and PREREG_ADDENDUM_1 are identical at both commits. The review's own scripts and outputs are in this folder (`rv_*.py`, `rv_*.out/.log/.json`). Nothing under `c12cg/`, C12CG.md, THEORY.md or CORE.md was edited.*

## Overall: **PASS-WITH-FIXES**

The numbers hold up. Independent code reproduces every error and every spend to all printed digits. R1 and R2 are correct. The hull and gap computation uses the right objects in the right direction. No better encoder was found: the best of 1,450+ structured and free-boundary attempts ties the nearest-vertex encoder to within 2×10⁻⁹, and the octagon would need 8.0×10⁻⁴. **Under the per-record reading, the pentagon and octagon are cap-only picks on the committed nine-world menu (OBSERVED).**

What does **not** pass as written is the step from that instance to Ace's public wording (H1). The note's surviving sentence is the "on the convex hull of the menu" wording that C12C_ONSET §11 has already withdrawn. The instance also lives only in the column the lock does not use. The general point (an accuracy cap is a stake only when the menu is convex or there is no duality gap) is KNOWN and was already established without this menu (C12C_ONSET §11, V6). The menu adds an instance in our own rounds, not the general claim. There are also process and prior-art fixes (M1–M4) and lows.

---

## Checks done (all OBSERVED unless marked)

**1. Errors re-derived (`rv_err.py` → `rv_err.out`).** Separate code path: effect-polytope vertices by `scipy.spatial.HalfspaceIntersection` (not the brute-force 3-constraint solve), exact circular arc overlaps, and P(correct) = ½ + (1/4π²)∫dφ max_e Σᵢ e(vᵢ)wᵢ(φ), on φ grids of 2×10⁵ and 8×10⁵ points (they agree to 10⁻⁸).

| world | C12CG | review | closed form (identified to ≥ 8 digits) |
|---|---|---|---|
| square | 0.125000 | 0.12500000 | 1/8 |
| pentagon | 0.176393 | 0.17639320 | (4 − √5)/10 = 0.1763932023 |
| hexagon | 0.166667 | 0.16666667 | 1/6 |
| octagon | 0.172335 | 0.17233496 | (7 − 3√2)/16 = 0.1723349571 |
| disk/ball | 1/2 − 1/π | (not recomputed) | 0.1816901138 |

The closed forms for the pentagon and octagon are new identifications (OBSERVED match to machine precision for the octagon, 10⁻¹⁰ for the pentagon). They are not proofs, but they make the numbers easy to check.

**2. Spends re-derived (`rv_spend.py` → `rv_spend.out`; `rv_k5.py` → `rv_k5_n*.log`).**
- An independent LP (scipy `linprog`) over the effect-polytope vertices, exhaustive over k = 2 encodings, gives square 2.000000, pentagon 1.118489, hexagon 1.188722, octagon 1.127571, with the same optimal encodings as `prec_n*.json`.
- **R2 stress test:** adding 400 random interior directions of the effect cone to the LP never raises the value (equal to 10⁻⁶ for all four). That is what subadditivity predicts.
- **k = 5** (local search, 300 random starts plus lifted k = 4 optima): pentagon 1.118489184, hexagon 1.188721876, octagon 1.12757066. No change. Convergence in k now extends to k ≤ 5 (still OBSERVED, not proved).
- **Hexagon value is KNOWN:** Massar–Patra 2014 (Protocol 3, n even) reads one bit perfectly and the other with P = 1 − cos(2π/n)/2. For n = 6 that gives I = 1 + (1 − h(¾)) = 1.188722 exactly (`rv_massar_patra.out`). For n = 8 their protocol gives 1.062798, below the 1.127571 found here, so the octagon value is a strict improvement on that protocol (a lower bound on the sup, OBSERVED optimal at k ≤ 5).

**3. Hull and gap (`rv_hull_check.out`).** Objects and direction are right.
- The stake rule minimises S + qE, q ≥ 0. Its winners are the vertices of the lower-left convex hull of the (S, E) points. A Pareto point is unsupported iff its E lies strictly above the hull's E at the same S.
- `gap.py` takes the hull from the stake winners and measures the vertical margin in error units at fixed spend. That is correct.
- By hand: the hull edge from ball (1, 0.181690) to hexagon (1.188722, 0.166667) gives E = 0.172258 at the pentagon's spend and 0.171535 at the octagon's. Margins: **pentagon 0.004135, octagon 0.000800**. Both match `gap2.out`.
- Cap windows: in [0.172335, 0.176393) the cheapest feasible world is the octagon (1.1276 < hexagon 1.1887). In [0.176393, 0.181690) it is the pentagon (1.1185). Both correct.
- Ties are handled harmlessly. At q = 0 every S = 1 world ties, including classical N = 2, which is listed as a "stake winner" there although it is not Pareto. This does not touch the gap.

**4. Better encoder (`rv_encoder_search.py` → `rv_encoder_n{5,6,8}.json`; `rv_encoder_struct.py` → `rv_encoder_struct.out`).** No encoder beat nearest-vertex. The octagon needs ≥ 8.0×10⁻⁴ and the pentagon ≥ 4.1×10⁻³ to join the hull.
- (A) n arcs in cyclic order with free boundaries, Powell from 30 perturbed starts: best = NV to within 2×10⁻⁹ (n = 5, 6, 8).
- (B) 60 random label sequences with n+1 to 2n arcs and free boundaries: never below NV (octagon best 0.174857).
- (C) Every vertex subset and order (octagon: 1,128 structured encoders; pentagon: 64), with optimised arcs: the best is the full NV encoder. The next octagon encoder, using 7 vertices, gives 0.178659.
- (D) Grid alternating optimisation from 200 random starts (no NV start), M = 1440: 200/200 land within 10⁻⁴ of NV. The few grid values just below NV (e.g. octagon 0.1723334) are discretisation artefacts. Re-evaluated exactly as arcs, the same encoder gives 0.17233566, above NV.
- Why this is the right search space: for a fixed decoder the error is linear in the encoded state, and for a fixed encoder it is linear in the effect. So the optimum is a deterministic vertex-valued encoder with an extreme-effect decoder. The relaxed problem is a convex maximisation, so the optimum is at an extreme point, and local searches can miss it. Global optimality therefore stays **OBSERVED**, as the note says.

**5. R1 and R2 (paper re-check): PASS.**
- R1: the channel x ↦ p(y | X_j = x) is linear in the tuple of encoded states. I is convex in the channel at a fixed input distribution. Supremum over reads and sum over j keep convexity. A convex function on a product of polygons is maximised at a product of vertices. Correct.
- R2: I(X;Y) = Σ_y φ(e_y), with φ convex and positively homogeneous (a perspective of relative entropy), hence sublinear. Splitting into extreme rays of the dual cone can only raise the sum, and merging same-ray outcomes is free. The LP has 3 equality constraints, so ≤ 3 non-zero λ. Correct.
- R2 uses the **no-restriction hypothesis** (every element of the dual cone below u is an allowed effect). That is standard for Janotta et al.'s polygon models and is what the committed `extreme_effects` also assumes, but it should be stated (L2).
- `prec.py` itself was checked: its rays are the facet normals (V[i]×V[i+1], scaled so max = 1), the BFS enumeration is complete for subsets of size ≤ 3, and the φ formula matches I(X;Y).

**6. Crossover side finding (12.56 vs 12.4): CONFIRMED, with one sharpening.**
- Committed rounded errors with committed binary spends: the first rival to beat the ball is the pentagon, at 0.070431/(0.1817 − 0.176) = **12.356** → the chain's "12.4".
- Precise errors: the hexagon first at 0.188722/(0.181690 − 1/6) = **12.562**. Pentagon 13.296 with the binary spend, **22.37 with the exact spend** (never on the hull). Octagon 13.636.
- The upper end, 17.64 = 1/(0.181690 − 0.125), is a **pairwise** square-vs-ball crossover. On the full menu the square takes over from the hexagon only at **19.47** (L5). "Rivals win again above ≈ 12.6" stays true in substance. The named rival and the lower end move.

**7. Prior art and DOIs (`rv_crossref.txt`, Crossref API this session).**
- Everett 1963, Oper. Res. 11:399–417, 10.1287/opre.11.3.399: OK (Hugh Everett).
- Geoffrion 1968, J. Math. Anal. Appl. 22:618–630, 10.1016/0022-247X(68)90201-1: OK.
- Geoffrion 1974, "Lagrangean relaxation for integer programming", 10.1007/BFb0120690: OK, pp. 82–114. Crossref types it as a book chapter (ISBN 978-3-642-00739-2) and gives **no volume**; "Math. Prog. Studies 2" is from the volume, not Crossref.
- Ehrgott 2005, *Multicriteria Optimization*, 10.1007/3-540-27659-9: OK, 2005, ISBN 3540213988. Crossref gives no author or edition field; the note discloses this correctly.
- Pawłowski et al. 2009, Nature 461:1101–1104, 10.1038/nature08400 (used for the ball/disk spend of 1 bit): OK.
- **Missing, should be credited (M2):** Massar & Patra 2014, "Information and communication in polygon theories", Phys. Rev. A 89:052124, 10.1103/PhysRevA.89.052124 (Crossref OK; arXiv:1403.2509 read). Haimes, Lasdon & Wismer 1971, the ε-constraint method, IEEE Trans. SMC SMC-1:296–297, 10.1109/TSMC.1971.4308298 (Crossref OK, no author field; authors from the paper). Janotta et al. 2011, NJP 13:063024, 10.1088/1367-2630/13/6/063024 (Crossref OK) is the polygon model source and is already cited elsewhere in the repo.

**8. "Written before computing" discipline (§8): NOT VERIFIABLE, and the stated time conflicts with file times (M1).**
- File mtimes (EST): `prec.py` and `crosscheck.py` 10:43:07; `prec_n4..n8.log/.json` 10:43:19–10:43:32; `gap2.py` 10:45:30; `gap2.out/.json` 10:45:36; C12CG.md 10:46:24 (only the last write is visible).
- §8 says "written 26 Nov 2026 about 10:45 EST, before any C12c-G″ computation". The C12c-G″ computation had finished at 10:43:32. Either the time in the heading is wrong or §8 was written after the numbers.
- WORKLOG has no entry between 10:40 (C12c-G′ done, "Next C12c-G″") and 10:46 (C12c-G″ done, "spec before compute"). No hash or separate write of §8 exists. `prec.py` (10:43:07) already cites "spec C12CG.md §8", which is weak evidence that §8 existed or was planned by then.
- Mitigation: §8 was declared "exploratory, not hash-locked". Its decision rule (gap survives if a margin is > 10⁻⁵ with converged spends) sits far from the realised margins (4×10⁻³, 8×10⁻⁴). So the decision is not sensitive to when the rule was written. But "spec before compute" cannot be claimed as discipline.

---

## Findings

### High

**H1. The step from this menu to Ace's public wording overreaches, and the note's surviving sentence uses withdrawn wording.**
- (a) C12CG §4 says the sentence "needs 'on the convex hull'", and §9.5 says *"a required accuracy acts as a stake on the convex hull of the menu"* is the version that survives. C12C_ONSET §11 (which governs) **withdrew** "on the convex hull of the menu" as too loose (H1 of HOSTILE_REVIEW_C12C: the two-point counterexample). The restated wording is: *"a required accuracy acts as a stake when the menu is convex (mixtures allowed) or there is no duality gap at the required accuracy."*
  - For a finite no-mixing menu, the exact statement is Lemma G: *a cap-selected world is stake-selectable iff it is a supported (lower-hull) Pareto point.*
- (b) The claim at stake, "an accuracy cap is not a stake in disguise unless the menu is convex", is **KNOWN mathematics** (Everett 1963; the integer-programming duality gap; supported vs unsupported points; V6's three-point set). It does not rest on this menu.
  - What C12CG adds is an **instance in our own rounds**. Under the per-record column, two worlds are cap-only picks on named D-windows (OBSERVED).
  - Under the locked total reading, the sentence holds only trivially, because one world dominates.
  - Public wording must not present the menu as evidence for the general sentence. It also must not say "our worlds show accuracy ≠ stake" without "under the alternative per-record column, which the locked definition does not use".
- (c) Suggested replacement for §9.5's surviving sentence (a suggestion for Ace's Friday wording, not an edit): *"A required accuracy acts as a stake when the menu is convex (mixtures allowed) or there is no duality gap. On a finite menu without mixing it acts as one only for supported Pareto points. In our own single-system menu, under the per-record column only, the pentagon and octagon are cap-only picks (margins 0.004 and 0.0008 in error units; errors OBSERVED, not proved optimal)."*

### Medium

**M1. §8 "before computing" is unverifiable, and the heading time contradicts file times** (check 8). Fix, append-only: state that §8's time is uncertain and that the C12c-G″ outputs are stamped 10:43:19–32. Drop "spec before compute" from the WORKLOG claim, or qualify it as "not verifiable; rule insensitive (margins ≫ 10⁻⁵)". Future specs: write and hash them, with a WORKLOG line, before running.

**M2. Prior art missing on the spend side and the cap side.**
- Massar–Patra 2014 already study information causality (the per-record sum at m = 2) in polygon theories.
  - Their Protocol 3 attains the hexagon's 1.188722 exactly. So the hexagon spend is KNOWN as a lower bound, and C12CG's contribution there is the OBSERVED optimality at k ≤ 5.
  - They conjecture the m = 2 value falls monotonically from 2 (n = 4) to 1 (n → ∞) for even n. Square 2 > hexagon 1.1887 > octagon 1.1276 fits that conjecture.
  - Their Theorem 2 (odd n has classical capacity > 1 bit) bears on M3.
- Haimes–Lasdon–Wismer 1971 (ε-constraint) is the standard source for "a cap recovers every Pareto point, including unsupported ones". That is the cap half of Lemma G. Credit it next to Geoffrion and Ehrgott.
- Novelty: still none in the method. The spend values for the pentagon and octagon at all finite-outcome reads have no prior source that this review found. That is not proof that none exists.

**M3 (side finding for the chain; does not change C12CG's result). The total-reading spend of odd polygons is understated.**
- The total reading is sup_M I(W;M), the classical capacity of one state. Massar–Patra Theorem 2 gives a capacity > 1 bit for odd n.
- A numerical maximisation here (`rv_capacity.py` → `rv_capacity.out`: input distribution by Nelder–Mead, best read by the R2 LP, a lower bound on the sup) gives **pentagon ≈ 1.0204 bits**. The checks: square 1.000000, hexagon 1.000000 (Theorem 1), triangle 1.584963 = log₂3.
- So the chain's total column "pentagon 1.70" (1 + 4·0.176) should be ≈ 1.72. PREREG_ADDENDUM_1 §C's "D equals the capacity price log₂N", already marked as not re-proved, fails for odd polygons.
- C12CG's total-reading result is unchanged: the square (1, 0.125) still dominates every polygon. Flag for Ace's cleanup; do not edit any committed file.

**M4. Evidence wording for the errors.**
- C12CG §3 and §9.4 say the alternating optimiser "converges to the nearest-vertex value as the grid refines… from random starts". The committed `later_question_error` takes the minimum over 8 starts, **and start 0 is the nearest-vertex encoder**. So the committed reruns cannot show that random starts reach NV.
- The random-start evidence is now supplied by this review (check 4D: 200/200 within 10⁻⁴), together with the failed structured and free-boundary searches (4A–C).
- The label stays **OBSERVED**. Add these as the evidence, and keep "global optimality not proved". The C12c-G‴ certificate remains the way to upgrade it.

### Low

- **L1 (chain side).** Classical N = 3: the per-record sup found is **1.5 at k = 2…5** (`rv_triangle_k45.out`; C12CG §9.2(a) found it at k ≤ 3). That is below log₂3 = 1.585.
  - So `r2_record_pricing.py`'s docstring ("classical N-simplex: P_rec = log₂N") and PREREG_ADDENDUM_1 §B's "its supremum over encodings agrees with the capacity log N wherever information causality holds" are not right for N = 3.
  - A sketch of why: equality in Σⱼ I(Xⱼ;V) ≤ H(V) needs subcube fibres, hence dyadic probabilities. HYP for all k.
  - No effect on the gap (N = 3 is dominated either way). Flag for Ace's cleanup.
- **L2.** State R2's no-restriction hypothesis.
- **L3.** §§3–4 still state "margins 3–8×10⁻⁴" and "conditional on the hexagon's P_rec being tight", and §7 still ranks C12c-G″ as open. §9 supersedes these but there is no pointer. Add one line at the top of §9 (append-only): "§9 governs where it conflicts with §§3–7."
- **L4.** The header says "about 10:45–11:10 EST", but the file was last written at 10:46:24. Fix the header time.
- **L5.** 17.6 is pairwise (square vs ball). The menu-level square onset is 19.47. Say which one the chain means.
- **L6.** The result is relative to the chain's nine-world menu, with one later-question task and per-world capacity prices (spend is a property of the world, not of the design used). Other tasks or polygons change the errors. Say "on this menu and task".
- **L7.** The disk/ball error 1/2 − 1/π is not proved optimal here. A lower true disk or hexagon error only **raises** the margins, so this direction is safe. Say so.
- **L8.** k-convergence now holds for k ≤ 5 (local search), not only k ≤ 4.
- **L9.** Geoffrion 1974: give the volume as "Math. Prog. Studies 2 (from the volume; Crossref has no volume field)".

---

## Corrected labels

| item | C12CG label | corrected label |
|---|---|---|
| Lemma G (cap = Pareto, stake = supported, gap = unsupported) | ELEMENTARY, KNOWN in substance | same; credit Haimes–Lasdon–Wismer 1971 for the cap half |
| R1 (vertex encodings suffice) | PROVED (in-model) | **PROVED (in-model)**, paper, hostile-reviewed PASS |
| R2 (≤ 3-outcome reads; LP over rays) | PROVED (in-model) | **PROVED (in-model)** under the no-restriction hypothesis; hostile-reviewed PASS |
| exact LP spends per k | OBSERVED | OBSERVED (independently reproduced) |
| sup_k = k ≤ 4 value | HYP | **HYP** (OBSERVED stable for k ≤ 5) |
| hexagon spend 1.188722 | OBSERVED | **KNOWN as attained** (Massar–Patra 2014 Protocol 3); optimality OBSERVED (k ≤ 5) |
| precise errors (nearest-vertex) | OBSERVED | OBSERVED; closed forms (4 − √5)/10 and (7 − 3√2)/16 OBSERVED to ≥ 10 digits |
| global optimality of the NV encoder | HYP | **HYP** (no improvement found in 1,450+ structured and free-boundary attempts, nor from 200 random starts) |
| per-record gap {pentagon, octagon}, margins 0.0041 / 0.0008 | OBSERVED | **OBSERVED**, conditional only on NV-encoder optimality |
| total-reading no-gap | OBSERVED / ELEMENTARY | same; holds also with the corrected pentagon capacity ≈ 1.0204 (M3) |
| §8.5 admissibility (per-record = alternative column only) | HYP reading | **fair as a reading** of the chain's own lock (it mirrors RECORD_COST_CHAIN:64 and Addendum B). The gap is an open miss for the unqualified sentence **in the alternative column only** |
| "§8 written before computing" | stated | **not verifiable**; heading time conflicts with output mtimes (M1) |
| surviving wording "on the convex hull of the menu" | ELEMENTARY | **withdrawn wording** (C12C_ONSET §11). Use "convex menu (mixtures) or no duality gap", or, for finite menus, "supported Pareto points" (H1) |
| crossover 12.56 (hexagon) vs chain's 12.4 (pentagon, rounded errors, binary spend) | OBSERVED | **OBSERVED, confirmed**; 17.6 is pairwise, menu-level square onset 19.47 |
| Open miss | the unqualified "accuracy = stake" sentence, per-record only | same, plus: the instance is not evidence for the general sentence, which is KNOWN on its own |

## For Ace's Friday cleanup (flags only; nothing edited)
1. RECORD_COST_CHAIN §4 table: "q ≈ 12.4" (pentagon, rounded errors, binary spend) → ≈ 12.56 (hexagon) with precise errors and exact spends. 17.6 is pairwise.
2. Committed per-record pentagon spend 1.070431 is a binary-read lower bound; the all-reads value is 1.118489.
3. Total-reading pentagon spend: capacity ≈ 1.0204 > 1 (Massar–Patra Thm 2); PREREG_ADDENDUM_1 §C's log₂N identification fails for odd polygons.
4. Classical N = 3 per-record value 1.5 (k ≤ 5), not log₂3: `r2_record_pricing.py` docstring and Addendum B's "agrees with the capacity wherever IC holds".
5. Public wording: use H1(c), not "on the convex hull of the menu".
