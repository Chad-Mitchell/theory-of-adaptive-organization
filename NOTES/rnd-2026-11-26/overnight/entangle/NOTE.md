# Round E: can "a reversible entangling map exists" come out of the theory? (private R&D note, not a PR)

Date: Thu 26 Nov 2026, 00:59–01:31 EST. No git, nothing pushed, posted or emailed, no repo files edited.
Files: `scripts/` (e1_interaction.py, e1b_controls.py, e2_pureworld.py, premise_graph.py, crossref.py), `outputs/`
(e1.txt, e1b.txt, e2.txt, premise_graph.txt), `crossref_entangle.txt` (every DOI below returned OK on the Crossref API),
`PREMISE_GRAPH.md` (circularity check requested by the hostile review), `ATTEMPTS.md`.
Labels: **observed** (numerics in the stated toy), **hypothesis**, **proved-in-model (PIM)**, **proved** (pen and paper,
any GPT satisfying the stated premises), **KNOWN** (published, DOI checked), **open miss**.
The CORE.md:7 sentence is unchanged ("The law of adaptive organization (hypothesis): strongly selected systems minimize the
cost of judgment."). Nothing here derives QM; every result is "proved in model under premises X".

## 0. Plain summary
We asked whether "two parts can become entangled" has to be assumed. Answer: it can be traded for two things in the
theory's own language, though it can't be removed. (1) If a closed world tracks itself at all (one part comes to carry
information about another), then some genuine interaction between parts must exist. This holds in any world, and the
proof is short. (2) If, in addition, the closed world starts in a definite ("pure") state, that interaction must
create entanglement. Both statements also run backwards, so they are re-expressions, not free derivations. The one new
assumption doing the work is "the closed whole starts pure", and the cost principle does not supply it. With those
pieces, the shortest honest chain to two-qubit complex quantum theory goes through a known theorem (Masanes, Müller,
Pérez-García, Augusiak 2014). It still assumes ball-shaped bits and continuous reversibility, so it does **not** derive
U. The other chain aims at U. It still needs Conjecture C for general polytopes.

## 1. Citation correction (relay to parent)
The brief cites "Masanes–Müller–Augusiak–Pérez-García 2013 PNAS 'Entanglement and the three-dimensionality of the
Bloch ball'". Crossref says otherwise. 10.1073/pnas.1304884110 is **"Existence of an information unit as a postulate
of quantum theory"** (PNAS 110:16373, 2013). The Bloch-ball paper is **Masanes, Müller, Pérez-García, Augusiak, J. Math.
Phys. 55:122203 (2014), 10.1063/1.4903510** (arXiv:1111.4060; full text at `../forces-gravity/mmpa2014.txt`). Cite it as
"MMPA 2014".

**What MMPA 2014 actually assumes** (read, lines 580–665 of the text). Parts are d-dimensional Euclidean balls.
*Continuous reversibility*: every reversible map lies on a one-parameter subgroup, so the group is connected, and the
pure states of the composite are one orbit G(â⊗â). Local tomography also holds. **Thm 1:** for d ≠ 3, every such G is
local (no interaction, no entanglement). **Thm 2** (proved in de la Torre et al. 2012, PRL 109:090403): for d = 3, G is
local, the adjoint action of SU(4), or its partial transpose. So "interaction ⇔ QT" inside the ball family. This lives
entirely **after U**: balls plus connected groups are continuity. It cannot produce U, and using it to "derive"
entanglement and then feeding that entanglement into the U route would be the loop the hostile review flags (g).

## 2. Results

### E-L0 [proved, any GPT, any number of parts]. Without interaction, nothing ever tracks anything.
Let a closed world W = A₁⊗…⊗A_n evolve by reversible maps from the trivial set Triv = {(g₁⊗…⊗g_n)∘P_σ} (local maps
and subsystem permutations). Then every product state ω₁⊗…⊗ω_n (pure or mixed) stays a product forever:
(⊗g_i)P_σ(⊗ω_i) = ⊗ g_i ω_{σ⁻¹(i)}. Every pair is uncorrelated at every time.
**Corollary (I).** In a closed reversible world that starts uncorrelated (Pprod), if any part ever comes to be correlated
with another part (T: a record is created), then the world's reversible group contains a non-trivial interaction (I).
This is the "cost of a world with no interactions": such a world can never form a record of anything, so any tracking
task has the maximal error. Converse: if I holds via a correlating map, a product-start history with tracking exists.
For classical parts it is the controlled shift.
**What it does not give:** I does not give entanglement. Exact counterexamples (E1/E1b): classical parts (triangle²,
|Aut| = 9! = 362880 versus 72 trivial); a reducible transitive non-classical part, square⊕square, × square (|Aut| =
32768 versus 1024 trivial, min and max); the square pyramid (AR15 Thm 2; 1024 versus 64; pyramid² 16384 versus 128).
Every non-trivial map there preserves product pure states: it is controlled (CNOT-like) and correlating, not entangling.

### Theorem E1 [proved, any GPT with LT, NR on parts, RV]. In a pure closed world, tracking forces a reversible entangling map.
- *Lemma E-L1 (pure marginal ⇒ product).* Assume LT, and that conditional states are states (Cond, implied by NR).
  If ω ∈ Ω_AB and ω_A is pure, then ω = ω_A⊗ω_B.
  *Proof.* For an effect f of B with p = ω(u⊗f) ∈ (0,1), ω_A = p·ω_A^f + (1−p)·ω_A^{u−f}. Purity gives
  ω_A^f = ω_A, so ω(e⊗f) = ω_A(e)ω_B(f) for all e and f (also when p ∈ {0,1}). LT then gives ω = ω_A⊗ω_B. ∎
  Observed check (E2b): the LP maximum of |X − (1,v)(u_Aᵀ X)| over max(A,B) with a pure A-marginal is 0.000e+00 for
  square², square×octahedron, octahedron², hexagon², hexagon×octahedron. This is the general form of R12-M.7 L2.
- *Lemma E-L2.* A reversible map (RV) is an affine bijection of Ω onto itself, so it sends extreme points to extreme
  points.
- *Theorem.* W = A⊗B evolves by RV maps from a pure product α⊗β. If at some time ω_AB ≠ ω_A⊗ω_B, then ω is pure (L2)
  and not a product, so the map taking α⊗β to ω is a reversible entangling map (E), and ω_A is mixed (L1). ∎
  Converse: E gives such a history, so **E ⇔ "a pure-start closed history contains tracking"**. With a third
  subsystem R, the map entangles A with BR, not necessarily A with B. In that case M11/M12 apply only if BR's state
  space is in their class (caveat).
- Exact illustrations (E2a):
  - QM or stabilizer, CNOT|+0⟩: Tr ρ² = 1, S(A) = 1 bit, I(A:B) = 2 bits.
  - Classical 2-bit world: all 24 reversible maps × 4 pure starts give I = 0, checked exhaustively. Classical tracking
    needs a mixed world: a uniform A with a CNOT gives I = 1 bit = log₂N.
  - Boxworld max(□,□): |Aut| = 128 = |D₄|²·2, every map is trivial, so I = 0 from any product start, pure or mixed.

### E1 / E1b tables [observed, exact group orders via Gram invariant + stabiliser chain; Bremner et al. 2014 criterion]
| composite (all reads on parts) | ext pts | Aut(S) | trivial | ratio | non-trivial maps are |
|---|---|---|---|---|---|
| triangle² (min = max) | 9 | 362880 | 72 | 5040 | controlled (classical) |
| triangle×square min / max | 12 / 12 | 3072 | 48 | 64 | controlled |
| square² min / max | 16 / 24 | 128 | 128 | 1 | none |
| square×octahedron min / max | 24 / 48 | 384 | 384 | 1 | none |
| octahedron² min / max | 36 / 684 | 4608 | 4608 | 1 | none |
| square×hexagon min / max | 24 / 144 | 96 | 96 | 1 | none |
| hexagon² min / max | 36 / 552 | 288 | 288 | 1 | none |
| pyramid×square min / max | 20 / 28 | 1024 | 64 | 16 | controlled |
| pyramid² min / max | 25 / 33 | 16384 | 128 | 128 | controlled |
| (square⊕square)×square min / max | 32 / 48 | 32768 | 1024 | 32 | controlled |
| 13 locally symmetric intermediates (□², □×O, □×hexagon) | 16–72 | = trivial | | 1 | none |
| **control:** 2-qubit stabilizer polytope (restricted reads) | 60 | 23040 | 4608 | 5 | **entangling** (56 of 70 coset reps) |

Reading: for irreducible non-classical NR polytopes, every tested composite between min and max has **only** trivial
reversible maps. That is stronger than "no entangling map" (M11/M12), and on min/intermediate composites it goes beyond
AR15 Thm 1 (max only). Observed, not proved, for the listed cases. The hostile review (g) is right that this tests the
*absence* of I in polytopes, not its presence. Presence comes from E-L0.

### E4 [proved; exact example]. Restricting reads is costly at a fixed state space.
For a fixed state space Ω, the read set E ⊆ Ω* (all consistent reads) gives every task a score ≥ that of any
restricted read set, at the same affine dimension (positivity on the larger set is the constraint, R10b-M M3a form).
Strict on some task whenever the restricted set is a proper subset of the dual's extreme rays (choose the task "apply a
missing extreme read"). Exact example: octahedron states, uniform over the 6 vertices, task "is the state in {+x,+y,+z}
or {−x,−y,−z}?". All reads give **1** (cube effect b = (1,1,1)). Pauli-only reads (stabilizer) give **2/3**: the slopes
satisfy |β|₁ ≤ 1/2. The qubit ball gives **1/2 + √3/6 = 0.78868…**.
**Limit.** This favours NR only at a fixed state space. For composites the trade is between local NR and composite
entangled states: the stabilizer Bell state scores −0.5 on a product of local all-reads (R10b-M M2c). So NR is
cost-favoured but not forced, and it stays an assumed premise.

### Route 1 (tracking cost: compare composites on one task) [KNOWN numbers + observed]
| composite | mutual information from one reversible step, pure start | CHSH coordination win | reversible tracking possible? |
|---|---|---|---|
| classical | 0 (needs a mixed world; then ≤ log₂N = 1 bit) | 3/4 | yes (controlled maps) |
| stabilizer (restricted reads) | 2 bits | 3/4 (max CHSH value 2 over 60 states × Pauli settings) | yes |
| quantum | 2 bits = 2 log₂N | (2+√2)/4 = 0.853553390593… (Tsirelson 1980) | yes |
| boxworld max(□,□) | 0 | 1 (PR box, Popescu–Rohrlich 1994) | **no** (all maps trivial) |
- An entangled pure record holds 2 log₂N bits of correlation. Classically the bound is log₂N. Superdense coding
  (Bennett–Wiesner 1992) turns that into half the communication cost for updating a partner's record. So **when
  entanglement is available, the cost prefers it** (KNOWN). That is a preference, not an existence proof.
- The coordination cost alone picks boxworld (1 > 0.854). Boxworld cannot track reversibly (E-L0 + E1). Combining
  "coordination is cheap" with "records are created reversibly" removes boxworld and classical, but needs both tasks
  in the battery (hypothesis).

### Route 2 (purification / dilation)
- R + P gives "every mixed part-state that actually arises is a marginal of a pure state of the closed world"
  (dynamical purification, proved, trivially). Full CDP purification (every mixed state, with uniqueness) is not
  needed.
- No-free-erasure / Landauer pricing does **not** force P: a classical dilation with a mixed ancilla prices erasure
  identically (composition Q3, selfref C5). Open miss.

### Route 3 (interaction ⇒ MMPA): see §1 and the chains below. "Trackers must interact" is proved (E-L0). Feeding it
into MMPA needs B and CR, which already contain U.

## 3. Chain diagram (best current routes; one rule RV for "reversible"; full graph in PREMISE_GRAPH.md)

```
                     [assumed] R: closed world evolves reversibly (RV)
                     [assumed, theory core] T: some part becomes correlated with another
        ┌────────────[assumed] Pprod: starts as a product            [assumed] P: starts pure product
        │                                                                     │  + [assumed] LT, NR (Cond)
        ▼  proved (E-L0)                                                      ▼  proved (Theorem E1, via L_E1, L_E2)
  I: a non-trivial reversible interaction exists              E: a reversible entangling map exists
        │                                                                     │
  CHAIN α (shortest; does NOT derive U)                    CHAIN β (aims at U)
        │ + [assumed] CR (MMPA continuity, composites incl.)                   │ + NR, RV
        ▼ proved: G connected ⇒ identity component interacts                   ▼ PIM: M11, M12/(♦), disk lemma; KNOWN AR15 Thm 1;
  Ic                                                                           │       observed: E1/E1b ratio-1 tables
        │ + [assumed] B: bits are balls; Tsame; LT                             ▼ parts ∉ (★)/(♦) NR polytopes
        ▼ KNOWN: MMPA 2014 Thm 1 (d ≠ 3 ⇒ local)                               │ OPEN MISS: Conjecture C for all polytopes
  d = 3                                                                        ▼
        │ KNOWN: Thm 2 / de la Torre et al. 2012                         not a polytope
        ▼                                                                      │ + [assumed] Trans; KNOWN Cartan; PIM M1a
  G = adjoint SU(4): two-qubit complex QT;                                     ▼
  entanglement follows (it is not assumed)                               U (infinite compact group, positive dim)
                                                                               │ + [assumed] Conn → proved: U_c
                                                                               ▼ + [assumed] JC, hSFP, [HYP] cheapest bit; KNOWN BMU 2014
                                                                         complex QM within the Jordan class (PIM, Round 9)
```
- No arrow feeds MMPA's conclusion back into I or E. `premise_graph.py` checks this mechanically.
- **Honest residue.** E ⇔ (P ∧ T) given R, LT, NR, RV, and I ⇔ (Pprod ∧ T) given R. Both entanglement premises are
  re-expressed in the theory's own terms. The load-bearing new premise is P, "the closed whole starts pure", which is
  not derived. Candidate source, HYPOTHESIS only: "no unheld distinctions". A mixed global state is a label held by no
  part, and the cost principle prices every held distinction.
- SFP note (hostile review (c)): SFP + transitivity ⇒ U (Jordan). SFP depends on the group (the qubit passes under
  SO(3) and fails under O(3)). Under RV the qubit group is SO(3)-type, because −I is not completely positive. SFP
  appears only after U, in chain β's last step.

## 4. Key numbers
- Aut orders: square² 128 = trivial; octahedron² max (684 ext) 4608 = trivial; hexagon² max (552 ext) 288 = trivial;
  13/13 locally symmetric intermediates = trivial.
- Controls: stabilizer 23040 vs 4608 (entangling found); classical 362880 vs 72; square⊕square 32768 vs 1024; pyramid
  1024 vs 64 (non-trivial, non-entangling).
- E2: QM pure-start I = 2 bits; classical pure-start I = 0 (exhaustive); CHSH 3/4, 3/4 (stabilizer, value 2),
  0.8535533906, 1.
- E4: octahedron parity task: all reads 1, Pauli-only 2/3, qubit 0.7886751346.

## 5. Lean candidates (precise statements for the Lean worker)
- **LE1 (pure marginal ⇒ product, extreme-ray form).** dA dB : ℕ; X : Matrix (Fin dA) (Fin dB) ℝ; B's effect cone is
  generated by f : Fin l → (Fin dB → ℝ), with u_B = ∑ λ_q f_q and λ_q > 0, and the f_q span ℝ^dB. ΩA ⊆ ℝ^dA is convex.
  Hypotheses: for each q, X·f_q ∈ cone(ΩA) (that is, ∃ c ≥ 0, ∃ w ∈ ΩA, X f_q = c • w), and x := X·u_B is an extreme
  point of ΩA. Conclusion: ∃ y, X = x ⬝ yᵀ (Matrix.vecMulVec x y). Same core as R12-M.7 L2, so it gets the same
  priority, now raised: Theorem E1 rests on it.
- **LE2.** For T : V ≃ₗ[ℝ] V with T '' Ω = Ω: T '' (Ω.extremePoints ℝ) = Ω.extremePoints ℝ.
- **LE0.** For finite types and σ : Equiv.Perm (Fin n), the map (⊗ g_i) ∘ P_σ sends a pure tensor ⊗ω_i to the pure
  tensor ⊗ g_i ω_{σ⁻¹ i}. A finite-dimensional version via PiTensorProduct; a 2-part version via TensorProduct.map and
  TensorProduct.comm suffices first.
- **LE5 (classical control).** On Fin m × Fin n, the deterministic states δ_(i,j) are exactly the extreme points, and
  each is a product δ_i ⊗ δ_j. So a pure classical world never contains a correlated pair (finite check).
- **LE4 (exact numbers).** For β : Fin 3 → ℚ with ∑|β_i| ≤ 1/2: ∑ β_i ≤ 1/2, so the success 1/2 + (1/3)∑β ≤ 2/3; and
  b = (1,1,1) gives 1/2 + (1/3)(3/2) = 1.

## 6. Foldable into PR #295 later (after Ace's review and a fresh-clone rerun; nothing edited now)
1. Result entry (proved, general): E-L0 and Theorem E1 with both converses, worded as **re-expressions**:
   "I ⇔ Pprod ∧ T; E ⇔ P ∧ T (given R, LT, NR, RV)".
2. Observed table E1/E1b. Wording: "every tested min/max/locally symmetric composite of irreducible non-classical
   NR polytopes has only trivial reversible maps". Include the controls.
3. Citation fix: MMPA 2014 is JMP 55:122203, 10.1063/1.4903510, not the PNAS 2013 paper.
4. Chain α as a conditional remark: "two-qubit complex QT proved in model given R, Pprod, T, Tsame, LT, B, CR via
   MMPA 2014". Not a derivation of U.
5. Open-miss entries: P (pure start) not derived; Conjecture C beyond M11/M12; NR forced only at a fixed state space.
6. RV rule and the "SFP + transitivity ⇒ U" sentence (hostile review (c), risk 3).

## 7. Sharpest next step
Attack **P** directly in a toy. Formalise "no unheld distinctions" as a cost term: a global mixture over k labels
costs log k unless some part holds the label. Then test whether a classical closed world that tracks (it needs a
mixed global state) pays strictly more than a QM world doing the same task from a pure start, at equal capacity. A
clean gap would make P cost-selected. No gap would make P an irreducible interpretive premise, and that should be said
plainly. In parallel, the hostile review's Conjecture C items (exact I×I, D×D; one tripartite case) remain the
bottleneck for chain β.

## Errata (append-only; 2026-11-26 01:41 EST)
- **E-err1 (stabilizer control row).** "23040 vs 4608, ratio 5" compares against |G_oct|²·2, where G_oct is the
  octahedron's group *with all reads*. That is the wrong baseline for a restricted-read polytope. The reviewer's
  independent BLISS run (`review_e1/indep_stab.txt`; this is working data, the review itself has not landed) gives:
  - the local maps that are actually automorphisms of the stabilizer polytope form a subgroup of order 2304 (index 10
    in Aut = 23040);
  - under RV (maps that extend to composites, CP), Aut = 11520 and its local part is 1152 (index 10);
  - 10368 of the 11520 CP maps are entangling.

  Corrected row: "stabilizer: |Aut| = 23040 (CP: 11520); local subgroup 2304 (CP: 1152); index 10; entangling maps
  found". The control's conclusion is unchanged.
- The reviewer's independent counts reproduce, exactly: square² min/max 128, hexagon² min/max 288 (max: 552 ext),
  pyramid² 16384, triangle×square 3072, octahedron² max 684 ext / 4608 (pycddlib + BLISS).
- HOSTILE_REVIEW_E1.md had not landed at 01:41 EST. Its corrections are to be appended here when it does.

## Errata from HOSTILE_REVIEW_E1.md (append-only; applied 2026-11-26 ~01:50 EST). No theorem is broken; these are wording, logic-type and hypothesis fixes.
- **E-err2 (equivalences: a type error).** Replace "E ⇔ P ∧ T" everywhere (§2 Theorem E1, §3 residue, §6.1) with:
  **E ⇔ there exist pure α, β and an RV history from α⊗β that contains a correlated pair.** The ⇒ direction uses LT.
  Likewise **I ⇔ there exist a product start and an RV history from it that contains a correlated pair.** E and I are
  properties of the theory. P and T are properties of one history.
- **E-err3 (missing step in Theorem E1).** Add: α⊗β (α, β pure) is pure in Ω_AB. Proof: if α⊗β = λω₁ + (1−λ)ω₂, the
  marginals force ω₁, ω₂ to have pure marginals α and β, so by E-L1, ω₁ = ω₂ = α⊗β. Also add: a pure non-product state
  is non-separable, because the extreme points of conv{a⊗b} lie in the compact product set. If P is phrased as "starts
  in a pure state of Ω_AB that is a product", the forward direction needs neither LT nor NR. The theorem is elementary;
  its value is bookkeeping (it moves the premise onto P).
- **E-err4 (E-L0 hypotheses and converse).**
  - E-L0 needs a causal GPT (unique unit effect), parallel composition with the interchange identity, and
    type-preserving σ. It does not need LT.
  - The converse ("a non-local map correlates some product state") needs LT, and the local factors must range over
    the full Aut(Ω_i). The reviewer gives a rank-one-preserver sketch citing Westwick 1967, Pacific J. Math. 23:613,
    10.2140/pjm.1967.23.613 (Crossref OK per review_e1; not read by either of us).
  - Counterexample when the local groups are smaller: 𝒯⊗𝒯 in a world of exactly two qubits.
  - Correlation can be **mediated** by a third system with no interaction on A⊗B. The reviewer's classical example
    uses a trit C.
- **E-err5 (chain α).**
  - Add the hypothesis **Bip**: the closed world is A⊗B, or the correlating map lies in G_AB.
  - MMPA's axiom is **Roundness** (strict convexity of the bit). Balls are derived from Roundness + CR, so B is a
    sufficient but stronger premise.
  - CR includes transitivity on the composite's pure states, and closed S and H.
  - Thm 2 has three outcomes: local, adjoint SU(4), or its partial transpose (equivalent to QT).
  - "Entanglement follows (not assumed)" becomes "entanglement follows from I, which is a re-expression of tracking
    from a product start".
- **E-err6 (chain β).** Add the hypothesis **Cl**: the reversible group is topologically closed. Cartan's step needs it.
- **E-err7 (RV is relative to the theory's composites).** RV = affine automorphisms T such that T⊗id preserves every
  composite *the theory contains*.
  - For the qubit, SO(3) results only because an entangled composite exists: (UNOT⊗id)(Bell) has min eigenvalue
    −1/2.
  - So "SFP holds for the qubit under RV" imports entanglement. That is harmless where it is used, after E in chain β.
  - Wording: −I is the universal NOT σ_y(·)ᵀσ_y. The transpose itself is diag(1, −1, 1). Both are non-CP.
- **E-err8 (scope and graph).**
  - The max rows of the group-order table re-confirm AR15 Thm 1. The new observed content is the min rows plus 13
    locally symmetric intermediates of □², □×O and □×hexagon only, not O² or hexagon².
  - "56 of 70 coset reps" has no group meaning. Use 10368 of 11520 CP maps entangling.
  - The premise graph is **dependency bookkeeping**, acyclic by construction; it is not evidence against circularity.
    The real circularity content is the two equivalences, plus premise strength (B + CR contain U).
- Reviewer's own slip (float cdd gave 2 for hexagon²) was fixed by them. It does not concern our pipeline.
