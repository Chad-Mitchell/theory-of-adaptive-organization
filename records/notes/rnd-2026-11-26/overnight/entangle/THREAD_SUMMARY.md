# Entanglement thread: overnight index (2026-11-26, 00:59–01:52 EST). Private R&D, no git, nothing folded.
Files: NOTE.md (Round E + errata), PREMISE_GRAPH.md, NOTE_P.md + PREREG_P.md, NOTE_C.md + PREREG_C.md, ATTEMPTS.md,
scripts/, outputs/, crossref_entangle.txt. Labels: proved / proved-in-model (PIM) / KNOWN / observed / assumed / open miss.

**One-line state.** "A reversible entangling map exists" is **re-expressed, not derived**: E ⇔ ∃ a pure product start
and a reversible history from it in which some part tracks another. The pure start P is assumed, interpretive, and not cost-selected (PREREG_P miss,
PREREG_C). The shortest chain to two-qubit complex QT (α) assumes continuity, so U is not derived anywhere.

## Results
- **E-L0 [proved, causal GPT with the interchange identity, n parts, type-preserving σ; LT not needed].** Hypotheses:
  closed world, reversible maps (RV), all of the form (⊗g_i)∘P_σ. Then products stay products. Corollary: R + Pprod (product start, mixed allowed) + T (a correlated pair
  appears) ⇒ I (a non-trivial reversible interaction exists). Existential converse: I ⇔ ∃ a product start and an RV history with tracking. The converse "non-local ⇒ correlates"
  needs LT and the full local Aut (𝒯⊗𝒯 counterexample). Correlation can be mediated by a third system. I does not give E: classical, the
  square pyramid and square⊕square have correlating, non-entangling controlled maps.
- **Theorem E1 [proved, elementary].** Hypotheses: causal GPT; two-part closed world A⊗B; LT; NR on A (conditional
  states are states); product effects valid; RV; pure product start α⊗β; T.
  - Steps: α⊗β is pure (by E-L1; reviewer's added step). RV keeps it pure (E-L2). A correlated pure state is
    non-product, hence non-separable, with mixed marginals.
  - Conclusion: the evolution is a reversible entangling map.
  - Existential equivalence: E ⇔ ∃ pure α, β and an RV history with tracking (⇒ uses LT).
  - With a third subsystem, the map entangles A with B-plus-rest only.
- **Group-order table [observed; exact; independently reproduced by the reviewer with pycddlib + BLISS].** For
  irreducible non-classical parts with all reads, |Aut| = trivial (local ⋊ swap) in:
  - square² min/max (128);
  - square×octahedron min/max (384);
  - octahedron² min/max (4608; max has 684 extreme points);
  - square×hexagon min/max (96);
  - hexagon² min/max (288; max 552);
  - 13/13 locally symmetric intermediates.

  Controls:
  - classical triangle²: 362880 vs 72;
  - triangle×square: 3072 vs 48;
  - pyramid×square: 1024 vs 64; pyramid²: 16384 vs 128;
  - (square⊕square)×square: 32768 vs 1024;
  - all of the above have non-trivial, product-preserving maps;
  - stabilizer (restricted reads): |Aut| 23040, local subgroup 2304; under RV 11520, local 1152; entangling maps
    found (erratum E-err1).
- **E4 [proved].** All reads weakly dominate at a fixed state space. Octahedron parity task: all reads 1, Pauli-only
  2/3, qubit 1/2 + √3/6.
- **PREREG_P [observed / PIM; miss].** `PREREG_P.md`, sha256 a4e02d65af9a8ab27f82791c245e2ef06f7ff6511b938d12a77fe4aa5122bb5d.
  - The classical world needs exactly 1.000000000000 bit of start entropy to track (exhaustive, n = 2, 3); QM and
    stabilizer need 0; boxworld can't track.
  - K0, K1 and K3 tie; only the definitional K2 separates. So P is interpretive. No deviations.
- **PREREG_C [proved; as predicted].** `PREREG_C.md`, sha256 b4208391d5c695729c32d720ca195e3aa769a4996902f5a6ce38d2211c647b93.
  - P ⇒ weak completeness, which is vacuous in GPTs.
  - Weak completeness ∧ self-reference ⇏ P (classical countermodel).
  - Strong completeness ⇔ P.
  - Deviation: the word "verdict" appears in the prereg.

## Premise graph (PREMISE_GRAPH.md; `scripts/premise_graph.py`)
- The graph is acyclic. I and E are derived nodes, never assumed leaves.
- Leaves of I: {R, Pprod, T}. Leaves of E: {R, P, T, LT, NR, RV}.
- This is **dependency bookkeeping**, acyclic by construction, not evidence against circularity. The real content is
  the two existential equivalences, plus premise strength. Added leaves: Caus, PEV, Bip, Cl, Round.
- One rule RV for "reversible": T⊗id preserves every composite the theory contains, so it is relative to the theory's
  composites. For the qubit this gives SO(3) only because an entangled composite exists ((UNOT⊗id)(Bell) has min
  eigenvalue −1/2; −I is the universal NOT). "SFP for the qubit under RV" therefore imports entanglement; it is used
  only after E.
- SFP + transitivity ⇒ U (Jordan), so SFP is used only after U.

## Chains (each arrow labelled)
```
α: R + Pprod + T + Caus ─proved E-L0─▶ I ─proved, +Bip[assumed], CR[assumed: connected, transitive on composites, closed]─▶ the two bits' group interacts
     ─KNOWN MMPA 2014 Thm 1 (JMP 55:122203, 10.1063/1.4903510), +Roundness[assumed] (or balls B, stronger), LT, Tsame─▶ d = 3
     ─KNOWN Thm 2 / de la Torre et al. 2012 (10.1103/PhysRevLett.109.090403)─▶ G = adjoint SU(4) or its partial transpose (both QT):
     two-qubit complex QT; entanglement follows from I (itself a re-expression of tracking from a product start)
β: R + P[assumed, interpretive] + T + LT + NR + RV ─proved Thm E1─▶ E
     ─PIM M11, M12/(♦), disk lemma; KNOWN Al-Safi–Richens 2015 Thm 1; observed: group-order table─▶ parts ∉ that polytope class
     ─OPEN MISS: Conjecture C─▶ not a polytope ─proved, +Trans[assumed], Cl[assumed: closed group], Cartan[KNOWN]─▶ U ─proved, +Conn[assumed]─▶ U_c
     ─PIM Round 9, +JC, hSFP[assumed], cheapest bit[HYP], BMU 2014[KNOWN]─▶ complex QM within the Jordan class
```
**Bottlenecks.** α: Roundness/B and CR (continuity, composites included), plus Bip. Together they contain U. β:
Conjecture C beyond M11/M12, plus P.

## Review corrections
- **E-err1:** the stabilizer baseline. The local subgroup inside Aut is 2304 (index 10); under RV 11520 / 1152.
- **Citation fix:** the PNAS 2013 DOI in the brief is a different paper. MMPA is JMP 2014.
- **HOSTILE_REVIEW_E1.md (landed 01:43; no theorem broken; errata E-err2..E-err8 in NOTE.md):**
  - existential equivalences;
  - the pure-product step added to E1;
  - E-L0's hypotheses (causality, interchange) and its LT-dependent converse;
  - Bip, Roundness and Thm 2's partial-transpose case for α;
  - Cl for β;
  - RV made composite-relative;
  - max rows = AR15 Thm 1, so the new content is the min and intermediate rows (□², □×O, □×hexagon only);
  - the graph relabelled as bookkeeping.

  The reviewer independently reproduced every group order.

## Lean candidates (precise forms in NOTE.md §5)
- **LE1 (pure marginal ⇒ product, extreme-ray form).** Top priority; the same core as R12-M.7 L2.
- **LE2:** T '' Ω = Ω ⇒ T preserves extreme points.
- **LE0:** (⊗g_i)∘P_σ maps pure tensors to pure tensors.
- **LE5:** pure classical states are products.
- **LE4:** the exact 2/3 and 1 bounds.
- **C1:** an extreme point has only the trivial convex decomposition.
- **Control `¬ SFP (O(3)) (sphere 3)` via −I** (hostile review risk 3).

## Next (not started)
The hostile review's Conjecture C items (exact I×I and D×D, one non-symmetric family, one three-part case). Otherwise
state P openly as "ignorance is perspectival".
