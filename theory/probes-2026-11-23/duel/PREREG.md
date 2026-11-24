# PREREG: GTAO tracking duel (quantum vs discrete vs classical-continuous tracker on a drifting circle)

*Written Monday 23 November 2026, ~9:15 PM EST, before any computation or simulation for this duel. Inputs: `/workspace/gtao/walls-2026-11-23/WALLS_MEMO.md` (reviewer-edited) §0.6 and §6; `/workspace/gtao/reviews-indep-2026-11-23/WALLS_REVIEW.md` §4 (objections 3, 4) and §5 ("the one next derivation"); GTAO `main` d592662 `CORE.md:52,70,80`, `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`. This file is hash-locked in `PREREG.sha256`. Nothing below is changed after the hash; any deviation is logged in DUEL_MEMO.md as a deviation.*

## 1. Question

Does GTAO's cost (price λ per nat of record size + stake on phase error + ruin cap) favor an N-level quantum tracker with continuous unitaries (b) over (a) an N-state classical/permutation tracker and (c) a classical continuous-phase tracker priced the same way, at equal readable information, when a world drifts on a circle? This is step (ii) of the walls-memo door: "tracking a continuously drifting world without ruin needs continuous reversible updates (Hardy's Axiom 5)".

## 2. Model

- **World.** Phase θ_t on the circle, θ_0 ~ uniform. Units: ω = 2π (one revolution per unit time); T is in revolutions.
  - Regime **D**: dθ = ω dt (deterministic, rate known to the designer).
  - Regime **S1**: dθ = ω dt + σ dW, record closed (no inputs). Grid s = σ² per revolution ∈ {0.001, 0.01}.
  - Regime **S2**: as S1, plus an outside observation y ~ vonMises(θ, κ_o = 100) every τ revolutions, τ ∈ {1/8, 1, 8}; the record is re-prepared from y alone at each observation (memoryless refresh, same for every tracker); the read time is uniform on [0, τ); s ∈ {0.001, 0.01}.
- **Record and readout.** The record evolves under its class's allowed dynamics. At a read time t one readout of the record gives an estimate θ̂_t (one shot; quantum readout may be destructive, so each read is a fresh copy of the protocol). Error e_t = wrap(θ_t − θ̂_t) ∈ (−π, π].
- **Readable information (two definitions, both reported).**
  - **R-Hol:** sup over the record's allowed preparations and readouts of I(θ; readout) ≤ ln N (Holevo-type cap).
  - **R-Hardy:** the record's state space has exactly N perfectly distinguishable states (N_max = N).

## 3. Cost (GTAO method: named terms)

J = **λ·ln K** (record-size price, λ per nat of record dimension, walls memo §6) + **w·Ē** (stake on phase error, w = 1, Ē = time-average over read time of E[1 − cos e_t], over [0, T] in D/S1 and over [0, τ) in S2) subject to the **ruin cap** max_t P(|e_t| > π/2) ≤ ε (else infeasible, J = ∞). The heat term (`CORE.md:70`) is not priced in the main rule; a tracker that needs a bath (irreversible record dynamics) is flagged, and a strict-closed variant (premise (i): no bath) excludes it.

**Record-size price K (finite-capacity premises, stated explicitly).**
- **FC1 (full state space):** K = dimension of the real linear span of the record's whole state space (Hardy's K, unnormalized). Classical N-state: N. Quantum N-level: N². A classical continuous phase space whose states are all probability measures on the circle: K = ∞, so λ ln K = ∞ for λ > 0. A classical continuous rotor *with an epistemic restriction as a law of the theory* (preparations restricted to nonnegative trigonometric polynomials of degree ≤ N−1, "c1"): K = 2N−1.
- **FC2 (task-used section):** K = dimension of the real span of the record states the tracker actually visits.
- **P-info (secondary):** price λ per nat of record–world mutual information (quantum: Holevo χ), GTAO's own memory coordinate (`CORE.md:52`).
- **Sensitivity:** normalized K (N−1, N²−1, 2N−2).
- **Finite-capacity premise for (c), stated as the reviewer asks:** under FC1/FC2 the price is finite only if the record's state space (or visited section) is finite-dimensional. A noiseless classical point (c0) is therefore infinitely priced; the strongest finite-priced classical continuous tracker is c1. Under R-Hardy, any classical (simplex) state space with N_max = N has exactly N pure states, so a classical *continuous* tracker with N_max = N does not exist (to be proved in the memo); under R-Hardy (c) has no admissible member, and that exclusion is by premise, not by cost.

## 4. Trackers (strongest fair version of each)

- **(a) N-state classical/permutation record.** a1: closed deterministic in continuous time. a3: best stochastic N-state Markov clock (unicyclic uniform rate r, rate optimized; random rate-matrix spot check for N = 3..5 for anything better); needs a bath. a2: jumps on free external ticks: **sensitivity only** (it imports a continuous clock; excluded from the main rule). Estimator θ̂ = 2πk/N + offset, offset optimized.
- **(b) N-level quantum.** H with equally spaced levels (period 1), pure state c optimized (subject to the ruin cap), canonical covariant phase POVM. Mixed states included via Fejér–Riesz (to be shown).
- **(c) classical continuous phase.** c0 noiseless point (K = ∞); c1 epistemically restricted rotor (ontic point φ, preparation law = nonneg trig poly of degree ≤ N−1 centered on θ, deterministic rotation, readout φ); c-RD: noiseless point read through a covariant channel of capacity ln N (P-info only).
- **(o) outside-the-three check:** the Carathéodory orbitope GPT (convex hull of the trigonometric moment curve of degree N−1, U(1) rotations), K = 2N−1. Reported, not part of the three-way rule.

## 5. Grid

N ∈ {2,3,4,5,6,8,12,16,24,32,48,64}; λ ∈ {0, 1e-4, 1e-3, 1e-2, 1e-1}; ε ∈ {0.05, 1e-2, 1e-3}; T ∈ {0.25, 1, 10, 100, 1000} (D, S1). S2 as in §2. Secondary free-size: each tracker picks its own N ∈ [2, 256] to minimize J.

## 6. Decision rule

Per cell, b vs competitor X: b feasible & X infeasible → b WINS; b infeasible & X feasible → b LOSES; both infeasible → cell excluded. Both feasible: ΔJ = J_X − J_b; WIN if ΔJ > tol, LOSE if ΔJ < −tol, TIE otherwise, tol = 0.01·max(J_b, J_X) + 1e-12. Cell outcome vs the set of admissible competitors: WIN iff WIN vs all; LOSE iff LOSE vs any; else TIE.
Aggregate per (regime × readable definition × pricing): over non-excluded cells with λ > 0: **WIN** if ≥ 90% WIN-cells and no LOSE-cells; **LOSE** if ≥ 50% LOSE-cells; **TIE** if ≥ 90% TIE-cells; else **MIXED**. λ = 0 cells reported separately.
Admissible competitors: R-Hol: best of {a1, a3} and c1 (c0, c-RD infinite-priced under K pricing; c-RD admissible under P-info). R-Hardy: best of {a1, a3}; (c) none (by premise). Strict-closed variant: a3 excluded.

**Step (ii) criterion.** Step (ii) "survives in the reviewer's sense" iff quantum **WINS** in regime D under R-Hol with FC1 or FC2 (the cells where a classical continuous competitor is admissible). If quantum wins only under R-Hardy, record "survives only conditional on a premise that excludes classical continuous by definition". If (o) beats (b) under the same rule, record "the cost selects continuity but not quantum theory specifically".

## 7. Predictions (written before computing; no patching)

P1 (D, R-Hol, FC1): b LOSES to c1 for every λ > 0 (equal stake and ruin, K = 2N−1 < N²); TIE at λ = 0. b beats a at long horizons. Aggregate LOSE.
P2 (D, R-Hol, FC2): b TIES c1 (K_used = 2N−1 for both, equal stake). Aggregate TIE or MIXED, not WIN.
P3 (D, R-Hardy, FC1): b beats a3 at long horizons (a3's error diffuses; ruin eventually for any finite classical Markov record), loses to a3 at short horizons (a3 has smaller K and quantization stake 1 − sinc(π/N) below b's 1 − cos(π/(N+1))). Aggregate MIXED, horizon crossover. Orbitope beats b everywhere b is feasible (same stake, K = 2N−1).
P4 (S1): like D with an extra common factor; same aggregates.
P5 (S2): frequent refresh favors a (smaller K, lower stake); long refresh intervals favor b over a3. MIXED.
P6 (P-info): c-RD reaches the rate–distortion floor and beats b.
P7: step (ii) does not survive in the reviewer's sense; it survives only conditional on R-Hardy, and there the orbitope beats quantum.

## 8. Failure modes from the review, checked explicitly

F1 classical continuous phase space matches quantum (step (ii) selects nothing without finite capacity). F2 K = N² headwind at equal readable information. F3 a discrete reversible tracker matches at equal K. F4 circularity: R-Hol presupposes the Holevo cap step (ii) was meant to deliver. F5 (i) only global: a3 uses a bath. F6 strawmen: a must include the best stochastic clock; c must include the epistemically restricted rotor. F7 hidden clock (a2). F8 tie definition.

## 9. Outputs

`checks/` scripts + outputs + `checks/SHA256SUMS`; DUEL_MEMO.md with labels PROVED (in-model) / KNOWN / CONJECTURE / SPECULATION. Clone deleted after.
