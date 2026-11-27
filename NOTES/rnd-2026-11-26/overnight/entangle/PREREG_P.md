# PREREG_P: is premise P ("the closed whole starts pure") selected by a cost? Written 2026-11-26 ~01:40 EST, BEFORE any run.
Lock: sha256 of this file is stored in PREREG_P.sha256 at write time. Any later change is logged in DEVIATIONS (end of
NOTE_P.md), never by editing this file.

## Setting (fixed)
- Closed world W of n parts, each with capacity N = 2 (at most 2 perfectly distinguishable states). Theories:
  classical bits (reversible maps = permutations of the 2^n configurations); QM qubits (unitaries); stabilizer
  (Cliffords); boxworld max(□,□) (its reversible group, |Aut| = 128, E1). Rule RV as in PREMISE_GRAPH.md.
- Start: a product state (Pprod; records are created, not inherited). Pure start = P. Mixed start allowed for the
  comparison.
- **Tracking task Θ(h, ε):** after one reversible step g, there is a read r_A on part A whose outcome has Shannon entropy
  ≥ h = 1 bit (novelty: not predictable from the law), and some read on part B predicts it with success ≥ 1 − ε.
  ε ∈ {0, 0.01}.
- **Repeated task Θ_T:** T rounds, each adds 1 fresh bit of novelty at a source and a retained record of it in a part
  distinct from the source. The measured quantity is the minimal number of N = 2 parts.

## Cost models (fixed in advance)
- **K0 (existing terms only):** J0 = c·Σ log₂N_i + q·(1 − success). No global term.
- **K1 (the brief's rule, operationalised):** J1 = J0 + κ·U1, where U1(ω) = max(0, S(ω) − max H(X)). The max runs over
  complete local sharp reads X that leave ω unchanged (non-disturbing), and X's label is "held" by the parts. S is the
  Shannon or von Neumann entropy of the start state.
- **K2 (global randomness priced, Landauer-like):** J2 = J0 + κ·S(ω_start). Flagged in advance as **definitional**: it
  prices exactly ¬P, so a K2 gap cannot count as cost-selection of P.
- **K3 (capacity for repeated tracking):** the minimal number of parts for Θ_T, classical mixed start vs QM pure
  start. It is non-definitional: it uses capacity only, an existing term.

## Predictions (derived analytically before the run)
- **Pr1.** Classical: the minimal S(W) for Θ(1, 0) is exactly 1 bit, because H(W) is conserved and H(W) ≥ H(A) ≥ 1. A
  pure classical start is infeasible (E2a). QM and stabilizer: pure start feasible, S = 0 (CNOT|+0⟩). Boxworld:
  infeasible from any product start (trivial dynamics, products stay products; success = 1/2).
- **Pr2.** U1 = 0 on every product start, classical or QM (spectral decomposition gives a non-disturbing local read with
  H(X) = S). So K1 ties classical and QM: ΔJ1 = 0.
- **Pr3.** K0 ties: same capacity, same success. ΔJ0 = 0.
- **Pr4.** K2 separates by exactly κ·1 bit per tracked bit, in favour of the pure start (definitional).
- **Pr5.** K3: both need 2T parts. Classical: T uniform source bits + T blank records (lower bound: disjoint sets
  with H ≥ T each). QM: Holevo bounds the records at ≥ T qubits and the sources need entropy T. Tie.

## Falsifiers (any one refutes the stated prediction)
- F1: classical minimal S < 1 bit at ε = 0.
- F2: QM or stabilizer pure start fails Θ(1, 0).
- F3: some product start has U1 > 0.
- F4: K0 or K3 counts differ between classical and QM.
- F5: boxworld succeeds from a product start.

## Decision rule (fixed)
- **"P cost-selected (in this model)"** iff some non-definitional pricing (K0, K1 or K3) gives a strict cost gap in
  favour of the pure start, at equal capacity and equal task success.
- **"P an interpretive premise (in this model)"** iff K0, K1 and K3 all tie, and only K2 (definitional) separates.
- Anything else is reported as-is. This includes a gap favouring the mixed classical start.
- Expected outcome on the analytic predictions: **interpretive premise** (a miss for cost-selection). The run checks
  this. Reported honestly either way.

## Runs (fixed)
`scripts/p1_track.py`:
- classical n = 2, 3, exhaustive over all permutations, with product starts on an exact rational grid (p_i ∈
  {0, 1/4, 1/2, 3/4, 1}) plus a fine float grid for ε = 0.01;
- QM n = 2: CNOT and random-unitary sampling (10⁴), pure starts;
- stabilizer n = 2: all 60 pure states reachable from |00⟩;
- boxworld: from E1's trivial group;
- U1 on all starts used;
- K3 for T = 1, 2 (classical exhaustive for n ≤ 4; QM constructive + Holevo bound).

Output: `outputs/p1.txt`.
