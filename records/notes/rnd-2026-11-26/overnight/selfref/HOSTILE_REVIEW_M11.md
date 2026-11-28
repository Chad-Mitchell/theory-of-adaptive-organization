# Hostile review: Theorem M11 (Round 11, part M)

Reviewer: fresh-context referee (2026-11-26, about 01:00–01:30 EST). I did not write M11.
Material read: NOTE.md "Round 11 (part M)" R11-M.1 to R11-M.6, Round 12 R12-M.1/M.2 for context,
`scripts/m_round11*.py`, `outputs_m.txt` (Round 11-M), `crossref_round11_m.txt`, and the Al-Safi–Richens full text
(arXiv:1508.03491, HTML).
New files: `scripts/hostile_m11_rerun.py`, `hostile_m11_star.py`, `hostile_m11_reflect.py`, `hostile_m11_reflect2.py`,
`hostile_m11_tight.py`, `hostile_m11_newparts.py`. All printed output is in `hostile_m11_outputs.txt`. No existing
file was edited except for one appended line in WORKLOG.md.

## Overall finding

**M11 survives with amended hypotheses.** Its mathematical core holds: an Aut(S)-invariant quadratic form, the Schur
block form, Lemma 1 on all of max, Lemma 2, and the strict-maximum argument. I found no counterexample. The
amendments mostly make implicit hypotheses explicit. Three statements around the theorem need correcting:
- the list of parts that satisfy (★) is too small;
- the stated reason (★) fails ("some n·v = 0") is wrong for several of the listed polytopes;
- the claim about what is new relative to Al-Safi–Richens overstates the open part for max products.

## Per-step table

| # | Step | Status | Notes |
|---|---|---|---|
| 0 | Setting | **holds with added hypotheses** | Make explicit: (a) local tomography: S sits in the normalized slice of V_A⊗V_B; (b) S is closed and convex; (c) G_X = Aut(P_X), with absolute irreducibility, not just irreducibility (see step 2); (d) Euclidean coordinates are the G-invariant ones. |
| 1 | Löwner ellipsoid: unique, Aut(S)-invariant, correct centre | **holds** (citation gap, minor) | Detail below. John is not even needed. |
| 2 | Schur block form q = \|a\|²/β + \|b\|²/γ + ‖C‖²_F/δ | **holds with an added hypothesis**: the irreps are absolutely irreducible (the NOTE says this; the claim as relayed says only "irreducibly") | No cross or linear terms. Detail below. |
| 3 | Lemma 1: ‖C‖_F ≤ R_A R_B | **holds** on every S ⊆ max | The norm is Frobenius in G-invariant orthonormal coordinates, the same norm Schur gives. Uses only positivity of product effects, so it holds for every composite between min and max. "\|n\| fixed" is implied by pointwise (★). Tight in every case checked. |
| 4 | Lemma 2 plus strict maximum, so T keeps product pure states product | **holds** (not circular) | Lemma 2 holds in any composite inside max where the part with the pure marginal has all effects. Detail below. |
| 5 | Characterizing (★) | **holds with corrections** | The pointwise form of (★) is exactly "centrally symmetric 2-level". The parts covered are more than hypercubes and cross-polytopes. "Some n·v = 0" is false for the octagon, 12-gon, icosahedron and dodecahedron. Detail below. |
| 6 | Composite assumptions | **holds with an added hypothesis** (state it) | "Local reversible maps stay reversible", i.e. (G_A⊗G_B)(S) = S, carries real weight in step 2 and does not follow from min ⊆ S ⊆ max. Whether it is necessary is unknown; my search found no counterexample without it. Transitivity and no-restriction are both used. |
| 7 | Literature | **holds with corrections** | The DOIs are correct and the paraphrase of Al-Safi–Richens is accurate. But on max products, M11 is already a special case of their Thm 1, for *every* non-classical centrally symmetric polytope, not only regular ones. John 1948 is the wrong sole source for uniqueness. |

### Step 1 in detail (Löwner ellipsoid)
- S has nonempty interior in the slice, because min ⊆ S and the products span. S is bounded because S ⊆ max and max is
  bounded.
- A reversible T satisfies T(S) = S. Since S spans V and sits in {u = 1}, u∘T = u. So T is an affine bijection of the
  slice, with |det| = 1 there (it preserves vol S). It therefore maps the minimum-volume ellipsoid to a minimum-volume
  ellipsoid containing S, and uniqueness gives T(E) = E.
- The centre is fixed by G_A⊗G_B. Each ρ_X is nontrivial and irreducible, since −I ∈ G_X by central symmetry. So the
  only fixed point is (1,0,0,0).
- Uniqueness is Danzer–Laugwitz–Lenz 1957 and Zaguskin 1958. Güler–Gürtuna (arXiv:0709.0707) say it "follows from" John
  1948, "although he does not state it explicitly".
- John is not needed at all. Aut(S) is a compact group (a closed subgroup of GL(V) preserving a convex body), so averaging
  any inner product over it gives an Aut(S)-invariant form. For polytopes, Aut(S) is finite and the vertex second moment
  Σvvᵀ, which is the certificate's own leverage, already does the job.

### Step 2 in detail (Schur block form)
- No cross terms: ρ_A⊗1, 1⊗ρ_B and ρ_A⊗ρ_B are pairwise inequivalent as G_A×G_B representations (compare their
  restrictions to G_A and to G_B). No linear terms, because the centre is (1,0,0,0).
- If both parts were irreducible of complex type, ρ_A⊗ρ_B would split over R and the C-block could carry two weights.
  Lemma 1's Frobenius bound would then not control q.
- Sufficient condition: one part absolutely irreducible. The hyperoctahedral group on R^m is absolutely irreducible, and
  for O×O and cube⊕cube I checked that the commutant has dimension 1.
- A larger Aut(S) is harmless. A smaller one, where local maps are not reversible, is outside the hypotheses.

### Step 4 in detail (Lemma 2 and the strict maximum)
- Why Lemma 2 holds: conditional states lie in that part's state cone, and a pure ray does not decompose.
- Under restricted reads, conditional states can leave the state cone. In the stabilizer control, though, the step that
  fails is Lemma 1 and S ⊄ max, not Lemma 2.
- The argument covers *every* extreme point of S other than a product of pure states, including extreme points of S that
  are not extreme in max, because Lemma 2 applies to every state in max. The NOTE's phrase "entangled extreme point" should
  be read that way.
- Products of pure states are extreme in S (also by Lemma 2). They are the strict maximisers of q among the extreme
  points of S, and T preserves q and extremality. No assumption is made about which points lie on ∂E.

### Step 5 in detail (which parts satisfy (★))
- Pointwise (★), "\|n·v\| = 1 for all n, v", is exactly "centrally symmetric 2-level". It is affine-invariant.
- It is equivalent to R²\|n\|² = m in invariant coordinates, by the second moment Σnnᵀ = (N\|n\|²/m)I.
- Octahedron×octahedron and cube⊕cube in R^6 satisfy every M11 hypothesis exactly, and neither is a cube or a
  cross-polytope.

## Checks run this round (exact unless marked float)

**Reruns with the original library** (`hostile_m11_rerun.py`, 0.8 s). All match `outputs_m.txt`.

| composite | extreme points (product / entangled) | outcome |
|---|---|---|
| max □□ | 24 (16/8), 2 classes | CERTIFIED |
| max □O | 48 (24/24) | CERTIFIED |
| intermediate: min+PR[0,3] | 18 | CERTIFIED |
| intermediate: min+all PR at λ = 3/4 | 24 | CERTIFIED |
| intermediate: min+PR0 at 3/5, PR1 at 1 | 18, 6 classes | CERTIFIED |
| stabilizer control | 60 (36/24), 1 class | **entangling automorphism found**; the exact linear map reproduces it on all 60 points |

- In the stabilizer control, the found map sends the product (1,0,0,1)⊗(1,0,0,1) to the state with XX = 1, YY = −1,
  ZZ = 1.
- The stabilizer polytope's minimum over its vertices and the all-effect product facets is −2 for the unnormalised
  (1 ± …)(1 ± …), i.e. −1/2 normalized. This matches R10b-M.2c: it is not inside max.
- Independent check of the inequalities the ellipsoid step needs (\|a\| < R_A, \|b\| < R_B, ‖C‖_F ≤ R_A R_B on every
  extreme point other than a product of pure states): 0 violations in all five composites. The max ratio of ‖C‖²/(R_A R_B)²
  is 1 (tight); it is 9/16 for the λ = 3/4 composite.

**(★) table** (`hostile_m11_star.py`)
- Cubes and cross-polytopes, m = 1..7 (exact): R²\|n\|² = m and all \|n·v\| = 1. **Holds.**
- Regular polygons (float):

  | n | R²\|n\|² | min \|n·v\| |
  |---|---|---|
  | 6 | 1.333333 | 0 |
  | 8 | 1.171573 | **0.414214** |
  | 10 | 1.105573 | 0 |
  | 12 | 1.071797 | **0.267949** |
  | 14 | 1.052095 | 0 |

  So (★) fails for every even n ≥ 6. But n·v = 0 occurs only for n ≡ 2 (mod 4).
- Icosahedron and dodecahedron (float): R²\|n\|² = 1.583592 vs 3, with min \|n·v\| = **0.236068**, so no n·v = 0.
- 24-cell: R²\|n\|² = 2 vs 4, and n·v = 0 does occur.
- **Correction.** The NOTE's sentence "Regular polygons with ≥ 6 sides, the icosahedron, the dodecahedron and the 24-cell:
  some n·v = 0" is false for the octagon, the 12-gon, the icosahedron and the dodecahedron. The correct reason is "some
  \|n·v\| < 1", equivalently R²\|n\|² < m. Their exclusion from M11 stands. (Odd polygons are not centrally symmetric,
  so they are outside the hypotheses anyway.)
- Ball: \|n\| = R = 1 gives 1 ≠ m for m ≥ 2. The singlet has C = −I with ‖C‖² = 3 > 1. **Holds** as stated.
- Stabilizer: its *parts* are octahedra with restricted Pauli reads, normals ±e_i. That gives R²\|n\|² = 1 ≠ 3, with
  n·v = 0 present, and its composite is not inside max. **Holds** as stated, but note that (★) is a property of a part with
  given reads, not of "the stabilizer polytope".

**New parts that satisfy every M11 hypothesis** (exact)
- **Octahedron × octahedron** (R^6, 36 vertices, 16 facets): R² = 2, \|n\|² = 3, R²\|n\|² = 6 = m, all \|n·v\| = 1.
- **Cube ⊕ cube** (free sum; R^6, 16 vertices, 36 facets): R² = 3, \|n\|² = 2, product 6 = m, all \|n·v\| = 1.
- For both: the cdd facet list equals the listed normals, (B₃ × B₃) ⋊ S₂ acts transitively on vertices, and the
  commutant has dimension 1 (absolutely irreducible).
- Exact tightness in max(O×O, □): x = (1, 0, 0, [v₁ v₂]) with v₁ = (e₁, e₁) and v₂ = (e₂, e₂) has all product-facet
  values ≥ 0 (minimum 0). It has ‖C‖²_F = 4 = R_A²R_B², and a float LP says it is not in min.
- So M11's covered class is strictly larger than "hypercubes and cross-polytopes". That is good news for M11, but the
  NOTE's R11-M.3 and R11-M.5 understate it.
- Plausibly the class includes more symmetric Hanner-type products and free sums. Products and free sums preserve
  2-levelness, but I checked only these two cases.
- Exact lrs runs of max(O×O, □) and max(cube⊕cube, □) were started (`hostile_m11_newparts.py`). Neither had finished
  after about 20 minutes on a loaded box (load average about 12), so no certificate is claimed for them.

**Counterexample search outside M11** (does local symmetry matter? `hostile_m11_reflect*.py`, float LP)
- Ansatz: an involution T(w) = w − φ(w)(p₀ − B), with φ(p₀) = 1 and φ(B) = −1. Then T² = I, u∘T = u and T p₀ = B. If
  T(min) ⊆ max, then S = conv(min ∪ T min) would be a composite between min and max with an entangling reversible map.
- Infeasible for every entangled max vertex B in □□ (8), □O (24) and OO (648).
- Also infeasible for 3992 non-product mixtures B = λ·PR_k + (1−λ)·X in □□, with X a product, the centre, or another PR
  box.
- So no entangling map turned up even without local symmetry, but this is only one ansatz. Conjecture C for
  non-symmetric composites remains an open miss.

**Counterexample to M11 itself: none.** I see no route to one: the proof has no gap under the amended hypotheses.

## Literature check
- Crossref (re-queried this round): all six R11-M DOIs resolve with matching title, authors, venue and pages:
  - Al-Safi–Richens NJP 17:123001;
  - Gross–Müller–Colbeck–Dahlsten PRL 104:080402;
  - Al-Safi–Short J. Phys. A 47:325303;
  - Bremner et al. LMS JCM 17:565–581;
  - Avis–Fukuda DCG 8:295–313;
  - John, in *Traces and Emergence of Nonlinear Programming* (2013 reprint), 197–215.
- **Uniqueness attribution (gap, minor).** Add these, verified on Crossref:
  - Danzer, Laugwitz, Lenz 1957, Arch. Math. 8:214–219, 10.1007/bf01899996;
  - Henk 2012, "Löwner–John ellipsoids", Documenta Math. Optimization Stories 95–106, 10.4171/dms/6/15;
  - Güler–Gürtuna, arXiv:0709.0707, read this round: the "does not state it explicitly" remark, and their Thm 4.5,
    Aut(K) ⊆ Aut(CE(K)), which they credit to Danzer et al. A Crossref search also returned Güler–Gürtuna, Optim.
    Methods Softw. 2012, 10.1080/10556788.2011.626037, under a different title; I did not confirm it is the same paper,
    so cite the arXiv version.
  - Zaguskin 1958 (Uspekhi Mat. Nauk 13(6):89–93) is cited in those sources; I did not check it on Crossref.
- **Al-Safi–Richens 2015, matched against the full text.**
  - Thm 1 (max products of non-classical dichotomic systems: all reversible maps trivial), Thm 2 (reducible subsystem),
    Thm 3 (odd polygons) and Conjectures 1 and 2 are paraphrased correctly. So is the "minor assumptions … number of pure
    states is finite" quote.
  - **Correction to R11-M.4.** The NOTE says the max-product case "is open for non-regular … polytopes". But every
    centrally symmetric polytope with all effects is dichotomic. For a facet effect e = (1 − n·r)/2, u − e = (1 + n·r)/2 is
    the opposite facet effect, which is also ray-extreme. Their Discussion even notes that Thm 1 needs only "the unit
    effect can be decomposed in two distinct ways as a sum of two ray-extreme effects".
  - So on max products, C (and M11) holds for every non-classical centrally symmetric polytope, by Thm 1, with the
    stronger conclusion "trivial". Their Discussion also credits Gross et al. 2010 with a simple proof that reversible maps
    of Boxworld max products permute pure product states.
  - **What is new in M11 is only the intermediate, locally symmetric composites.**
  - Terminology clash: Al-Safi–Richens' "irreducible" means the cone is not a direct sum, a geometric notion. M11's
    "irreducibly" means representation irreducibility. The NOTE should keep the two apart.
- Bremner et al. 2014 is used correctly. The vertex permutations preserving K_ij = v_iᵀ(Σvvᵀ)⁻¹v_j are exactly the
  linear automorphisms permuting the (homogeneous) vertices, and colour-refinement classes are automorphism-invariant, so
  the certificate is sound.

## Corrected statement (Theorem M11′)

**Parts.** Let A and B be GPT systems with all consistent effects (no restriction). Their normalized state spaces are
centrally symmetric polytopes P_A ⊂ R^{m_A} and P_B ⊂ R^{m_B} centred at 0. Let G_X = Aut(P_X) (linear, since it fixes
0). Assume, for X = A, B:
1. G_X is transitive on the vertices of P_X.
2. G_X acts absolutely irreducibly on R^{m_X}. One absolutely irreducible part suffices.
3. P_X is 2-level: n·v ∈ {−1, +1} for every facet n·r ≤ 1 and every vertex v. Equivalently, in G_X-invariant Euclidean
   coordinates, R_X²\|n_X\|² = m_X.

**Composite.** Let S be a closed convex set in the normalized slice of V_A⊗V_B (local tomography) with
min(A,B) ⊆ S ⊆ max(A,B) and (g⊗h)(S) = S for all g ∈ G_A, h ∈ G_B.

**Conclusion.** Every linear bijection T with T(S) = S permutes the product pure states {v⊗w}. In particular, S has no
reversible entangling map.

**Covered parts.** Hypercubes and cross-polytopes in every dimension, plus at least octahedron×octahedron and cube⊕cube
in R^6 (checked exactly).

**Scope.** For S = max this is already implied by Al-Safi–Richens Thm 1. The new content is the intermediate composites.

**Not covered** (still open misses): parts that are not 2-level (even polygons with n ≥ 6, icosahedron, dodecahedron,
24-cell, prisms), composites that are not locally symmetric, and three or more parts. Round 12's M12 addresses the first.

## Lean-able steps (precise statements)
1. **(★) equivalence, finite form.**
   - Data: finite V ⊂ R^m with \|v\|² = R² for all v, finite N with Σ_{n∈N} nnᵀ = cI, and \|n\|² = s for all n.
   - Then (∀n, v: \|n·v\| ≤ 1) ⇒ [(∀n, v: \|n·v\| = 1) ⟺ R²s = m].
   - Elementary finite sums.
2. **Lemma 1, general finite form** (generalizes the landed `cube_corr_bound`).
   - Data: Σ_{n∈N_A} nnᵀ = (\|N_A\|s_A/m_A)I and Σ_{k∈N_B} kkᵀ = (\|N_B\|s_B/m_B)I, with \|nᵀCk\| ≤ 1 for all n, k.
   - Then ‖C‖²_F ≤ m_A m_B/(s_A s_B).
   - Trace algebra.
3. **Max positivity ⇒ \|nᵀCk\| ≤ 1**, from the four product-facet inequalities. Linear arithmetic.
4. **Strictness.** A point of conv(V) with V on the sphere of radius R, and not in V, has norm < R. This is strict
   convexity of the Euclidean norm (Mathlib's StrictConvexSpace).
5. **Lemma 2** (already landed abstractly as `pure_marginal_product`).
6. **Averaging instead of John, for polytopes.** For a finite group Γ ≤ GL(V), Σ_{g∈Γ} gᵀMg is Γ-invariant and positive
   definite when M is. This replaces Löwner uniqueness when S is a polytope, so Aut(S) is finite.
7. **Final assembly.** If q is T-invariant, positive definite, and strictly larger at products of pure states than at
   every other extreme point, then T permutes the products of pure states. Trivial.
8. **Schur step** (heavier). G-invariant symmetric bilinear forms on an absolutely irreducible real representation are
   scalar, and equivariant maps between inequivalent irreducibles vanish. Mathlib has Schur's lemma for simple modules,
   but the real, absolutely irreducible packaging is work.
9. **Not Lean-ready.** Löwner uniqueness for general convex bodies, and the compact-group (Haar) version for
   non-polyhedral S.
