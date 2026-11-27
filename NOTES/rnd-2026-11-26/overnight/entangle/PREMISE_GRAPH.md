# Premise graph for the entanglement chains (Round E, 2026-11-26, 01:20–01:31 EST)

Written in response to the hostile review (`rnd/HOSTILE_REVIEW_FOUNDATIONS.md` items (b), (c), (g); risk 1).
Machine check: `scripts/premise_graph.py` → `outputs/premise_graph.txt` (acyclic; I, E, Ic never appear as a leaf
premise of any conclusion). Arrow labels: **proved** (general, pen and paper), **PIM** (proved in model / a stated
class), **KNOWN** (published theorem, DOI Crossref-checked), **assumed**, **open miss**.

## One rule for "reversible" (RV), applied to every candidate
RV: a reversible map of a system is an affine bijection T of its state space onto itself that is an allowed
transformation of the theory *and extends to composites*: T⊗id maps every composite state space in the theory onto
itself. (This is the GPT analogue of complete positivity.)
- Polytope parts in min, max and locally symmetric intermediate composites: every linear symmetry of the part
  satisfies RV there (min, max and those composites are invariant under G_A×G_B by construction), so E1/E1b test the
  full symmetry group. For an *absence* claim ("no non-trivial interaction"), testing the largest allowed group is the
  strong direction: a subgroup of a trivial group is trivial.
- Qubit ball: the point reflection −I (transpose / time reversal) fails RV (the partial transpose sends the Bell state
  out of the two-qubit state space), so the RV group is SO(3)-type, and SFP holds under RV. Under the full affine group
  O(3), SFP fails. Hostile review (c).2 is right that SFP is a property of (state space, group) pairs. Nothing in the
  chains below uses SFP except node CQM_J (Round 9), which sits *after* U.
- **SFP + transitivity ⇒ U** (Jordan's theorem: a transitive group on n ≥ 2 points has a fixed-point-free element;
  `SFP.lean:41`). So SFP is never independent of U. In chain β, hSFP is used only after U has been reached.
- MMPA's continuity premise (CR) is a premise about the RV group: every element lies on a one-parameter subgroup.

## Leaves (premises and cited theorems)
| node | status | content |
|---|---|---|
| CP | assumed | cost hypothesis (CORE.md:7) |
| R | assumed | the closed world evolves by reversible maps (RV) |
| P | assumed | the interacting closed system starts in a **pure** product state |
| Pprod | assumed | the closed world starts in a product state (mixed allowed); weaker than P |
| T | assumed (theory core) | some part comes to be correlated with another part (records are created) |
| Tsame | assumed | the tracking pair are two systems of the same type |
| LT | assumed, cost-motivated | local tomography (link price, composition Q1b: "motivation, not new structure") |
| NR | assumed, cost-favoured at fixed state space | every consistent read of a part is allowed (E4 below) |
| Trans | assumed | parts' reversible groups are transitive on pure states |
| Conn | assumed | parts' pure-state sets are connected |
| B | assumed | bits are Euclidean balls |
| CR | assumed | MMPA continuous reversibility, composites included |
| JC, hSFP, CB | assumed / assumed / HYPOTHESIS | Round 9 inputs |
| CC | **open miss** | Conjecture C beyond the M11/M12 class |
| MMPA14, dlT12, AR15, BMU14, Cartan | KNOWN | see crossref_entangle.txt |
| M11M12 | PIM | selfref R11-M, R12-M |

## Derived nodes (inputs → node, arrow label)
| node | inputs | arrow |
|---|---|---|
| Cond (conditional states are states) | NR | proved |
| L_E1 (pure marginal ⇒ product) | LT, Cond | proved, any GPT |
| L_E2 (reversible ⇒ pure to pure) | RV | proved |
| L_E0 (local maps + swaps keep products product) | R, Pprod | proved, any GPT, any number of parts |
| **I** (a non-trivial reversible interaction exists) | L_E0, T | proved |
| **E** (a reversible map sends a pure product to a pure non-product) | R, P, T, L_E1, L_E2 | proved (Theorem E1) |
| Ic (identity component interacts) | I, CR | proved |
| QT2 (d = 3, two-qubit complex QT; entanglement follows) | Ic, Tsame, B, LT, MMPA14, dlT12 | KNOWN theorems applied |
| NotPolyClass | E, NR, RV, M11M12, AR15 | PIM |
| NotPolyAll | E, NR, CC | **open miss** |
| U | NotPolyAll, Trans, Cartan | proved given inputs |
| Uc | U, Conn | proved (standard) |
| CQM_J | Uc, JC, hSFP, CB, BMU14 | PIM within Jordan class |

## Is "an interaction / entangling map exists" upstream of a conclusion?
- **As an assumed premise: no** (mechanical check). I and E are *derived* nodes. Their leaves are {R, Pprod, T} and
  {R, P, T, LT, NR, RV}. No node downstream of U or MMPA feeds back into I or E.
- **The loop the review warns about** ("entangling map ⇒ U ⇒ balls ⇒ MMPA ⇒ entanglement derived") does not occur.
  Chain α reaches MMPA with B and CR *assumed*, not obtained from E. Chain β reaches U from E, and E comes from
  Theorem E1, not from MMPA.
- **What the honest residue is (important).** Theorem E1 is an **equivalence**, not a free derivation. In a two-part
  world with R, LT, NR and RV: *a reversible entangling map exists ⇔ some closed history that starts pure and product
  contains tracking (a correlated pair).* (⇐ is Theorem E1. ⇒: start at the pure product and apply the map.) Likewise
  *I ⇔ some product-start closed history contains tracking.* So the premise has been **re-expressed in the theory's own
  terms** (tracking, plus "the closed whole starts pure"), not removed. The new load-bearing premise is **P**. P is not
  derived from the cost: a classical world with a mixed global state satisfies every cost premise (composition Q3,
  selfref C5). Candidate independent source for P (HYPOTHESIS only): "no unheld distinctions". A mixed global state is
  a label that no part of a closed world holds, and the cost principle prices every held distinction.
- Labels to use: chain α = "two-qubit complex QT **proved in model given** R, Pprod, T, Tsame, LT, B, CR (MMPA 2014)".
  Chain β = "U **proved in model given** R, P, T, LT, NR, RV, Trans **and Conjecture C (open)**". For any statement
  that drops P: "**form derived given that an interaction exists**".

## Errata (HOSTILE_REVIEW_E1.md, applied ~01:50 EST)
- Relabel: this is **dependency bookkeeping**. It is acyclic by construction, so "I/E not a leaf" cannot fail, and it is
  not evidence against circularity. The substantive points are:
  - (i) the two equivalences, stated existentially: E ⇔ ∃ a pure product start and an RV history with tracking;
    I ⇔ ∃ a product start and an RV history with tracking;
  - (ii) premise strength: B (or Roundness) + CR already give a continuous transitive group;
  - (iii) RV is relative to the theory's composites; for the qubit it presupposes an entangled composite.
- Added leaves:
  - Caus (causal GPT, interchange identity);
  - PEV (product effects valid);
  - Bip (the interaction acts on A⊗B; chain α);
  - Cl (closed group; chain β);
  - Round (MMPA Roundness; B is a stronger substitute).

  Re-run: `outputs/premise_graph.txt`.
- QT2 now names Thm 2's three outcomes: local / adjoint SU(4) / partial transpose (the last two are QT).
- The leaf "CR" means MMPA's axiom: connected; transitive on every system, composite included; S, H closed.
