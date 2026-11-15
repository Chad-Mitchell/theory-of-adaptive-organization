# ONSET-ACROSS-ALPHA-SIM preregistration (pick 32, uniform slot; ledger 151)

Private. Written Sunday 15 Nov 2026 about 6:50 PM ET by a Grok Bot executor for Chad (via Ace). Lock = the commit that adds this file and its sha256, pushed to branch q-pick32 **before any design cell (α = 1.5 or 2.5) is run**. Nothing public.

## 0. Claim under test (THEORY v1.4.11 §2.5, CLAIM_MAP N12, narrowed form per `reviews/night2/N12_REFEREE.md`)
For exact reset reads the pooling-onset exponent is −1 at every α > 1: it measures the level's technology, not the world's spectrum. §9's sink: "across systems with the same sensing technology …, the same α for shared and private drift within each system, and different measured α, the pooling-onset exponent moves with α." This test runs that comparison **in-model**, with learners that are never given a cost function.

Narrowed premises, all built in: same α for shared and private drift; exact reads at the level and the members (read noise 0); stated ρ window {0.01, 0.02, 0.04, 0.08, 0.16, 0.32} (1.5 decades); architecture 𝒜₁ (one level over N members, bundled quadratic loss), no per-member broadcast cost, upkeep h = 0; same technology (reset reads) at level and members.

Scope: **reset-read arm only.** The precision-priced arm (−2) is not run here (cost; the self-tuned EWMA is not the best linear tracker at α ≠ 2); it is queued as a new item.

## 1. World (`world.py`, `run.py`; fresh code, imports nothing from earlier simulators)
- Discrete time. Drift = discrete fBm, Var(x[t+τ] − x[t]) = q τ^{α−1} (H = (α−1)/2), exact Davies–Harte circulant embedding. Shared g with q_g = ρ, private u_i with q_u = 1, member target x_i = g + u_i, stakes 1 per member per step.
- Reset read: cost C, returns the current value exactly; estimate held until the next read; integer interval T on a 90-point log grid 1…600; random phase.
- C per α is a unit choice set so a lone member's learned T is near 40: C = 84.3 (α = 1.5), 800 (α = 2, pilot only), 6072 (α = 2.5). Theory says the exponent does not depend on C.
- **Learners (no cost function anywhere):** selection on realized payoffs. Every T on the grid lives through the same realized training path (2^18 steps); the realized cheapest (C/T + stakes × realized mean squared error) is kept. Flat members (16) learn on their own x_i path; residual members (16) on their own u_i path; the level learns on its own g path with stakes N, for every N on the grid. LEARNSIM's "pop" learner, here primary (its ES learner's onset noise made LEARNSIM's exponents inconclusive; MV10 needs the lower noise). What remains circular: any learner that minimizes realized cost approaches the world's optimum, so a pass says the continuous-time algebra predicts what selection on realized payoffs finds in this discrete learned world; **not evidence about nature**.
- Evaluation on fresh test paths (2^18 steps), common random numbers: flat cost per member = C/T_f + realized mean (x_i − x̂_i)²; levelled cost per member = C/(N T_g) + realized mean (e_g + e_u,i)² (cross term included) + C/T_u. D_rel(N) = (flat − levelled)/flat on 161 N points log-spaced over ×/÷16 around the theory N\* (`theory.py`, used only to place the grid; an onset outside it makes the cell invalid).
- Design: α ∈ {1.5, 2.5} × 6 ρ × 16 seeds, independent RNG streams (`default_rng([100α, 10⁴ρ, seed, 32])`).

## 2. Theory predictions (`theory.py`, continuous time; the simulator never imports it)
Onset solves N^{1/α−1} ρ^{1/α} = (1+ρ)^{1/α} − 1. Window exponents (OLS of ln N\* on ln ρ over the six ρ): **−0.9624 (α = 1.5), −0.9625 (α = 2), −0.9626 (α = 2.5)**; predicted Δ = e(2.5) − e(1.5) = −0.0002 (recomputed over whichever ρ are valid). Asymptote −1 at both.

## 3. Named rival and margin
Rival: the onset exponent moves with α by as much as the §2.5 exponents that **do** depend on α move over the same pair: vigilance growth a = 1/α and the mixed-technology private-drift exponent θ + 1 − 1/α both change by **0.267** from α = 1.5 to 2.5. Margin δ = 0.267.

## 4. Pilot and MV10 power gate (before lock)
Pilot at α = 2 (outside the locked contrast; 6 ρ × 16 seeds; `pilot_alpha2.jsonl`): ê = −0.935, bootstrap SE 0.035 (theory −0.9625; this is the only outcome looked at before lock). Planned SE(Δ̂) = √2 × 0.035 = 0.050 (check on the pilot data duplicated as both α: 0.049); gate run at a conservative σ = 0.075 (×1.5, for possible extra noise from long memory at α = 2.5). `tools/power_gate.py contrast --form optimality --effect 0.267 --sigma 0.075`: SNR 3.56 ≥ 2.80, **gate met** (P(PASS | prediction) 0.945, P(FAIL | rival) 0.945; `POWER_GATE.json`). Exact two-sided rules below at σ = 0.075: P(PASS | Δ = 0) 0.89, P(FAIL | Δ = δ) 0.945; both rules fire on their own best-case data. Verdict code checked on pilot data duplicated as both α (PASS, CI ±0.096): mechanics only.

## 5. Locked estimators and verdict rules (`analyze.py`, `verdict.py`)
- N̂\*(ρ): seed-mean D_rel(N) → isotonic (increasing) fit → upward zero crossing interpolated in ln N. Valid if a crossing exists in ≥ 90% of 2,000 seed-bootstrap replicates. ê(α): OLS slope of ln N̂\* on ln ρ over valid ρ (needs ≥ 4 valid ρ spanning ≥ 1 decade, else INCONCLUSIVE); CI = percentile seed bootstrap.
- **Primary (contrast):** Δ̂ = ê(2.5) − ê(1.5), bootstrap independent across α. **PASS** iff the 95% CI lies inside (Δ_pred − δ, Δ_pred + δ). **FAIL** (prediction killed in-model) iff the CI excludes Δ_pred **and** |Δ̂ − Δ_pred| ≥ δ/2. Otherwise **INCONCLUSIVE** (including a CI that excludes Δ_pred with |Δ̂ − Δ_pred| < δ/2: a small α-dependence, attributable to discreteness, reported, not a kill). If realized SE(Δ̂) > δ/2.80 = 0.095 the verdict is labelled exploratory.
- **Secondary (per α, never decide the primary):** PASS if |ê − e_pred| ≤ 0.15|e_pred|; MISS if not and the CI excludes e_pred; else INCONCLUSIVE.
- Label: "passed / failed / inconclusive **in-model, on proxy 'learned reset-read pooling onset in simulated fBm worlds'**". No field claim; no CLAIM_MAP status change from this alone (N12 stays MATH-CORRECTED unless a separate reviewer says otherwise).

## 6. Resources
nice 19, single-threaded BLAS, 3 workers, background; ~200 jobs × ~3 s.
