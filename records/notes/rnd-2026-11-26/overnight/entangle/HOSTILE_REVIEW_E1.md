# Hostile review of Round E (E-L0, Theorem E1, the RV rule, the E1/E1b tables, chains α/β, the premise graph)

*Thu 26 Nov 2026, 01:31–01:43 EST. Fresh-context referee pass. I did not write the audited material. No git, no
posting, no email. I did not edit any audited file; my own files are in `rnd/entangle/review_e1/`.*

**Read:** `NOTE.md` (as of 01:31, plus the E-err1 erratum appended at 01:41), `PREMISE_GRAPH.md`, `ATTEMPTS.md`,
`crossref_entangle.txt`, `scripts/*`, `outputs/*`, `../HOSTILE_REVIEW_FOUNDATIONS.md`, `../selfref/HOSTILE_REVIEW_M11.md`,
the MMPA 2014 text (`../forces-gravity/mmpa2014.txt`, arXiv:1111.4060v4, lines 1–60, 560–665, 838–880, refs 3830–3880),
and the Al-Safi–Richens 2015 text (`../forces-gravity/review_g2/asr2015_arxiv1508.03491v1.txt`, abstract and Thm 1/2
statements).

**Re-ran (independent pipeline, not the authors' code):** I enumerated vertices with pycddlib, which is not the lrs
the authors used. Its float output was snapped to rationals and then certified exactly: every vertex is feasible, its
tight rows have rank D, and no vertex repeats. I computed the exact Gram invariant K = V Q⁻¹ Vᵀ in sympy. I computed
the automorphism group with igraph/BLISS on a bit-layered edge-coloured graph, not the authors' stabiliser chain.
Every BLISS generator was checked to preserve K exactly. Files: `review_e1/indep_aut.py`, `indep_more.py`,
`indep_stab.py`, `rv_checks.py`; outputs are in `indep_run.txt`, `indep_stab.txt` and `rv_checks.txt`. I also
re-queried Crossref (`review_e1/crossref_review.txt`).

*Reviewer's own slip, recorded:* my first run used float cdd without snapping and gave |Aut(hexagon² max)| = 2. That
cannot be right, because the 288 local maps are automorphisms by construction. Inexact Gram values were the cause.
After exact snapping and certification it gives 288. The authors' lrs pipeline is exact and did not have this problem.

Status words: **holds**, **holds with added hypothesis / relabel**, **overclaimed**, **broken**.

---

## Per-claim table

| # | claim | status | key data / reason |
|---|---|---|---|
| 1a | E-L0 forward: with only (⊗gᵢ)∘P_σ, product states (pure or mixed) stay product | **holds** (with stated framework hypotheses) | One line: (⊗gᵢ)P_σ(⊗ωᵢ) = ⊗gᵢω_{σ⁻¹(i)}. Needs a causal GPT (unique unit effect, so marginals and "product" are defined), parallel composition obeying the interchange identity (g⊗h)(a⊗b) = ga⊗hb, and type-preserving σ. LT is **not** needed. |
| 1b | Corollary: Pprod ∧ T ⇒ I | **holds** | The contrapositive of 1a. |
| 1c | "the converse holds too" / "local maps and swaps cover all non-interacting dynamics" | **holds with added hypothesis + relabel** | True if "non-interacting" means "sends *every* product state, mixed included, to a product" **and LT holds** (rank-one-preserver argument below), with the local factors ranging over the full affine automorphism groups Aut(Ω_A), Aut(Ω_B). It is false if the local group is smaller. Exact counterexample: in a world of exactly two qubits, the full transpose 𝒯⊗𝒯 maps the 2-qubit state space onto itself (min eigenvalue of the image over 2000 random states is +5e-06), preserves products, and is not in SO(3)⊗SO(3). It fails RV once a third qubit exists: min eigenvalue of (𝒯⊗𝒯⊗id)(Bell_AC⊗\|0⟩_B) is −0.5. It is also false if "non-interacting" means "pure products to pure products": the controlled maps in the E1b rows (triangle², pyramid², (□⊕□)×□) do that and still correlate mixed products. |
| 1d | "correlated" for mixed parts; multipartite T | **holds with relabel** | ω_AB ≠ ω_A⊗ω_B is well defined given causality. T is pairwise. Correlation between A and B can be **mediated** with no interaction on A⊗B (see 5e). This does not affect E-L0, but it does affect chain α. |
| 2a | Lemma E-L1 (pure marginal ⇒ product) | **holds** | The proof is correct. It needs: NR on **A only** (Cond via bipolar duality); e⊗f and e⊗(u−f) valid effects; pointed cone (the p ∈ {0,1} case); and LT. The p = 0 case is handled correctly. The Lean LE1 reportedly landed (WORKLOG 01:39); I did not rebuild it. |
| 2b | Lemma E-L2 (RV maps keep pure states pure) | **holds** (trivial) | An affine bijection of Ω onto Ω preserves extreme points. |
| 2c | Theorem E1 forward | **holds with a missing line + relabel** | Missing step: α⊗β (α, β pure) is pure in Ω_AB. This follows from E-L1: split α⊗β = λω₁ + (1−λ)ω₂, then the marginals force ω₁ = α⊗β. With that line added, the proof is complete. **It is elementary.** "Correlated pure ⇒ entangled" is **not** a definition, but it is a one-line lemma: the extreme points of conv{a⊗b} lie in the compact set of products, so a pure non-product state is non-separable. If P is phrased as "starts in a pure state of Ω_AB that is a product", the forward direction needs neither LT nor NR. |
| 2d | Converse "E ⇔ P ∧ T" (NOTE §3, §6 item 1) | **overclaimed (logic type error)** | E is a property of the theory (∃ a map). P ∧ T is a property of one history. E does not imply that the actual world starts pure. Correct form: **E ⇔ ∃ a pure-product initial state and an RV history from it that contains tracking**. The ⇒ direction needs LT, so that "non-product" implies a correlation visible to local reads. PREMISE_GRAPH.md:67–70 already states the correct existential form; NOTE.md:156 and §6.1 do not. The same applies to "I ⇔ Pprod ∧ T". |
| 3a | RV: −I fails for the qubit in QT | **holds** | (UNOT⊗id)(Bell) has min eigenvalue **−0.5** exactly. Every element of O(3)∖SO(3) is antiunitary (transpose∘unitary), so none of them is CP. The RV group is SO(3) ≅ PU(2). |
| 3b | the wording "−I (transpose / time reversal)" | **relabel** | −I is the universal NOT, σ_y(·)ᵀσ_y. The transpose itself acts as diag(1, −1, 1) on the Bloch ball. Both are non-CP. |
| 3c | RV is a property of the part | **overclaimed** | RV depends on the composite. If the only 2-qubit composite were min (separable states only), −I⊗id would preserve it, and in a 2-qubit-only world 𝒯⊗𝒯 passes (see 1c). So "the qubit's RV group is SO(3)" presupposes an entangled composite, and "SFP holds under RV" for the ball imports entanglement. That is harmless where it is used, which is after E in chain β, but it must be stated. |
| 3d | RV applied consistently | **overclaimed in one row (now erratum E-err1)** | The polytope min/max/locally symmetric rows are consistent: full local Aut ⊆ RV there, and Aut(S) is the strong direction for absence. The stabilizer control row used the **full** Aut(S) (23040, half of it non-CP) and the baseline 48²·2 = 4608, which includes maps such as −I⊗id that are **not** automorphisms of the stabilizer polytope. |
| 4a | group orders, NR polytopes | **holds (reproduced exactly)** | Independent results: □² min/max 16/24 ext, 128 = trivial. Hexagon² min/max 36/**552** ext, 288 = trivial. **Octahedron² max: 684 ext, 54 distinct Gram values, \|Aut\| = 4608 = 48²·2**, and every generator permutes the 36 product pure states. Pyramid² 25/33 ext, 16384 vs 128. Triangle×□ 12/12 ext, 3072 vs 48. All match `outputs/e1.txt`. |
| 4b | stabilizer control | **overclaimed / wrong baseline → corrected** | \|Aut\| = **23040** (reproduced). The local subgroup *inside* Aut(S) is **2304**, index **10**, not "4608, ratio 5". Under RV (Choi-PSD): \|Aut_CP\| = **11520** (Clifford mod phases), CP-local **1152**, index **10**. Entangling elements: **10368 of 11520** CP maps (90%) and 20736 of 23040 overall. "56 of 70 coset reps" is an artefact of the stabiliser chain with no group meaning. The qualitative conclusion "entangling found" survives. |
| 4c | "no interaction at all" for irreducible non-classical NR polytopes | **holds as observed, scope relabel** | The max rows for □, octahedron and hexagon are already **AR15 Thm 1** (KNOWN: max tensor product of non-classical *dichotomic* systems has only trivial reversible maps; text line 383), so they re-confirm it. The new observed content is the min rows plus 13 random locally symmetric intermediates, and those cover **only** □², □×O and □×hexagon, not O² or hexagon². |
| 4d | correctness and completeness of the Aut computation | **holds** | The Bremner et al. 2014 Gram criterion is complete for linear symmetries of a full-dimensional vertex set, and every such map preserves u. NR makes effect preservation automatic. The stabiliser chain is exhaustive backtracking over equitable refinements, and a discrete refinement implies a trivial pointwise stabiliser. Classifying the generators as "product-preserving" or "local/swap" is valid for the whole group, because both properties are closed under composition. |
| 5a | MMPA 2014 citation | **holds** | Crossref (this round): 10.1063/1.4903510 is Masanes; Müller; Pérez-García; Augusiak, *Entanglement and the three-dimensionality of the Bloch ball*, J. Math. Phys. 55, 122203 (2014). The NOTE's correction of the brief (the PNAS DOI 10.1073/pnas.1304884110 is the information-unit paper) is right. Thm 2 is credited in MMPA to their ref. 21, de la Torre–Masanes–Short–Müller, PRL 109, 090403 (2012), Crossref OK. |
| 5b | MMPA assumptions as stated | **holds with relabel** | MMPA's axioms are Tomographic Locality, **Roundness** (strict convexity of the bit) and Continuous Reversibility (CR). The ball shape is *derived* from Roundness + CR (text 852–880), so B is a sufficient but stronger premise. CR is "in each type of system", so it includes transitivity on the **composite's** pure states: the pure states are {G(â⊗â)} (text 604–606). The `premise_graph.py` gloss "parts transitive" understates this. MMPA also assume S and H are **topologically closed** (text 758), Ĥ×Ĥ ≤ G, and the consistency condition (7)/(8) on product effects. Thm 1 is stated for H ≠ SO(3) from Table IV A, with conclusion G ⊆ SO(d)^×SO(d)^. Thm 2 has **three** outcomes: local, adjoint SU(4), or its partial transpose, the last being equivalent to QT. The chain diagram drops the partial-transpose case, though NOTE §1 has it. |
| 5c | QT2 arrow "entanglement follows (it is not assumed)" | **overclaimed → relabel** | Entanglement follows from I. By E-L0, I is a re-expression of "Pprod ∧ T possible". MMPA's own abstract says entanglement ⇔ interaction is the minimal assumption. |
| 5d | Ic "proved" | **holds (immediate)** | Under CR the group is connected, so G = G₀. |
| 5e | chain α, missing hypothesis | **holds with added hypothesis (Bip)** | E-L0 gives *some* interaction *somewhere* in the closed world. MMPA needs an interaction inside the group of the **two identical gbits**. Exact mediated example (classical): A is a uniform bit, B = 0 is a bit, C = 0 is a trit. Step 1 is c ↦ c + a (mod 3), acting on A⊗C. Step 2 is b ↦ b ⊕ [c = 1], acting on C⊗B. Then I(A:B) = 1 bit, and no step acts non-locally on A⊗B. Tsame does not exclude this. Add **Bip**: the closed world is A⊗B, or the correlating map lies in G_AB. |
| 5f | chain β, "U: proved given inputs" | **holds with added hypothesis (Cl)** | Cartan's closed-subgroup step needs the reversible group to be **closed**. An infinite non-closed group need not be a positive-dimensional Lie group, although its closure is. MMPA assume closedness; chain β's leaves do not. |
| 5g | AR15 citations | **holds** | AR15 Thm 1 covers max products of non-classical dichotomic systems. Thm 2 says a reducible subsystem gives non-trivial reversible maps in max. The square-pyramid cone is reducible (cone over □ ⊕ the apex ray), so citing Thm 2 for the pyramid is correct. |
| 5h | DOIs | **holds** | All 10 re-queried DOIs returned matching title, authors, venue and pages: MMPA14, dlT12, AR15, PNAS13, Bremner14, BMU14, Tsirelson80, PR94, BW92, GMCD10. The earlier 429 failures in `crossref_entangle.txt` were rate limits and were retried OK. |
| 6 | premise-graph acyclicity | **holds, but trivially; not a substantive check** | The edges are hand-entered and I, E, Ic are declared derived nodes, so "I/E not a leaf" cannot fail. The script verifies the authors' declared dependencies, not the proofs. The real circularity risks are not cycles: (i) **equivalences**, E ⇔ ∃(P ∧ T) and I ⇔ ∃(Pprod ∧ T), which mean the premise is re-expressed rather than removed (the authors say so); (ii) **premise strength**: in chain α, B + CR already give a continuous transitive group at part level, and RV-for-balls presupposes an entangled composite (3c); (iii) **missing leaves**: causality/unit effect, Bip, Cl, product effects valid, NR-on-A-only. After adding them the graph stays acyclic, which shows the check does not discriminate. Relabel it "dependency bookkeeping". |

---

## Detail on the points that change wording

### 1c. Converse of E-L0 (proof sketch, 2 parts, LT)
Let T be a linear bijection of V_A⊗V_B (LT) that maps every product state a⊗b (a ∈ Ω_A, b ∈ Ω_B) to a product.
(a⊗b) ↦ T(a⊗b) is bilinear, and "rank ≤ 1" is a set of polynomial equations (2×2 minors). These equations vanish
on Ω_A × Ω_B, and Ω_A × Ω_B spans and has non-empty relative interior, so the minors vanish on all of V_A × V_B. So T
preserves rank-one tensors. By the classical linear rank-one-preserver theorem (cited via Westwick, *Transformations
on tensor spaces*, Pacific J. Math. 23 (1967) 613–620, 10.2140/pjm.1967.23.613, which Crossref resolves; **I did not
read the paper this round, so this is the standard statement as usually cited**), T = g⊗h, or (g⊗h)∘SWAP when
dim V_A = dim V_B. Normalisation gives u_A∘g ∝ u_A. Marginals of states are states, so g(Ω_A) ⊆ Ω_A, and applying the
same argument to T⁻¹ gives equality: g ∈ Aut(Ω_A). In the swap case, g: V_B → V_A maps Ω_B onto Ω_A, so the parts
are isomorphic. Therefore **an RV map outside (Aut(Ω_A)⊗Aut(Ω_B))⋊swap sends some product state to a correlated
state.** The gap between Aut(Ω_A) and the theory's local reversible group is exactly what the 𝒯⊗𝒯 example exploits. The
n-part version uses the multipartite form of the same theorem (Westwick 1967; not re-derived here).

### 4b. Stabilizer control, exact breakdown (`review_e1/indep_stab.txt`)
I built the 60 states from commuting signed-Pauli pairs, not by Clifford closure. 36 of them are products. Of the 23040
elements of Aut(S):

| kind | CP | non-CP |
|---|---|---|
| local g⊗h | 576 | 576 |
| (g⊗h)∘swap | 576 | 576 |
| entangling | 10368 | 10368 |

So |Aut| = 23040, the local subgroup has order 2304 (index 10), |Aut_CP| = 11520, and the CP-local subgroup has order
1152 (index 10). This agrees with E-err1, which was appended to NOTE.md at 01:41 from this working data.

---

## Overall finding

The mathematics in Round E is correct and the group-order numerics reproduce exactly through an independent pipeline.
Nothing is broken at the level of theorems. The problems are in labelling and logic:

1. The stabilizer-control baseline was wrong ("4608, ratio 5"). The correct figures are 2304 and index 10, or 1152
   and index 10 under RV. This is now corrected as E-err1.
2. The two-sided "E ⇔ P ∧ T" and "I ⇔ Pprod ∧ T" statements are a type error. They need the existential form.
3. Chain α lacks the hypothesis **Bip**: correlation can be mediated by a third system. Chain β lacks **Cl**: the
   reversible group must be closed.
4. RV is composite-relative. For the qubit, it presupposes an entangled composite.
5. Theorem E1 is elementary. Its value is bookkeeping: it moves the entanglement premise onto **P** ("the closed
   whole can start pure"). The authors already say this, and it is accurate.
6. The premise-graph acyclicity is true by construction and should not be cited as evidence against circularity.

## Corrected statements (drop-in)

- **E-L0.** In a causal GPT whose parallel composition obeys the interchange identity, every map (⊗gᵢ)∘P_σ, with σ
  type-preserving, sends product states (pure or mixed) to product states. *Corollary:* if a closed reversible world
  starts in a product state and some pair becomes correlated, its reversible group contains a map outside
  {(⊗gᵢ)P_σ}. *Converse (LT):* any reversible map outside (⊗Aut(Ω_i))⋊Perm_types sends some product state to a
  correlated one. If the local groups are smaller than Aut(Ω_i), the converse can fail: 𝒯⊗𝒯 in a 2-qubit-only world.
- **Theorem E1.** Assume causality, LT, NR on A, and RV. Suppose a closed world A⊗B evolves by RV maps from α⊗β with
  α, β pure. Then α⊗β is pure (by E-L1). If at some time ω ≠ ω_A⊗ω_B, then ω is pure, non-separable and has mixed
  marginals, and the composite evolution is a reversible entangling map. *Equivalence:* **E ⇔ there exist pure α, β
  and an RV history from α⊗β that contains a correlated pair** (⇒ uses LT). It is not "E ⇔ P ∧ T".
- **RV.** The reversible maps are the affine automorphisms T such that T⊗id preserves every composite *that the
  theory contains*. For the qubit in QT this gives SO(3) (UNOT⊗id on the Bell state has eigenvalue −1/2). The result
  depends on the composite containing an entangled state.
- **Stabilizer row.** |Aut| = 23040 (CP: 11520). The local subgroup in Aut(S) has order 2304 (CP: 1152), index 10.
  Entangling elements: 10368 of the 11520 CP maps.
- **NR-polytope rows.** Every listed min/max composite of □, octahedron and hexagon, and 13 sampled locally symmetric
  intermediates of □², □×O and □×hexagon, has only local∘swap automorphisms (observed). The max rows are covered by AR15
  Thm 1.
- **Chain α.** Two-qubit complex QT (G = adjoint SU(4) or its partial transpose) is proved in model given R, Pprod, T,
  Tsame, **Bip**, LT, Roundness (or B), and CR (connected, transitive on every system including the composite, closed
  S and H), via MMPA 2014 Thm 1 and Thm 2 (Thm 2 from de la Torre et al. 2012). Entanglement follows from the
  interaction I, which is a re-expression of tracking from a product start.
- **Chain β.** U is proved in model given R, P, T, LT, NR, RV, Trans, **Cl**, and Conjecture C (open).
- **Premise graph.** Relabel it as dependency bookkeeping: acyclic by construction. Add the leaves causality, Bip, Cl
  and product-effects-valid, and annotate the two equivalences.

*Not re-audited here:* the Lean LE0–LE5 build (WORKLOG 01:39 says it landed), E4 and Route 1 numbers, NOTE_P.md and
PREREG_P.md (new at 01:33–01:36), and the earlier rounds beyond what the two context reviews cover.
