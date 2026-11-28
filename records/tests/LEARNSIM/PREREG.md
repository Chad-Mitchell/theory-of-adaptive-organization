# LEARNSIM preregistration: a non-circular learning-agent test of GTAO's surviving in-model results

Private. Written Sunday 15 Nov 2026, finished 08:16 ET (lock time is the commit time, not this line), by a Grok Bot executor for Chad (via Ace). Nothing public. Locked by sha256 (below) and a commit to a branch of the private repo before Stage A or any onset run.

## 0. Why this test exists
The physics/stats review (night1/REVIEW/physstat/REPORT.md, issue #2) found every earlier simulation pass circular: learners minimised the simulator's own expected-cost formula, so the onset slope was fixed before any learner existed, and "measured" sensing exponents read back the trackers' own cost rule. This test removes those specific circularities:
- The simulator (`world.py`, `run_lone.py`, `run_onset.py`) contains **no expected-cost formula**. Costs exist only as realized money spent + realized squared error × stakes on simulated paths.
- Trackers never receive the cost function. They learn their policy by a noisy (1+1) evolution strategy on realized episode payoffs, starting from a uniformly random policy over 3–9 decades.
- Tech A trackers tune their smoothing gain α from their own observations only (minimising squared innovation); neither truth nor payoff enters α.
- Theory predictions are computed separately in `theory.py` from GTAO's continuous-time closed forms (T1, T1.8, T3, T5 / math-review exact V, P10). The simulator never imports it.
- Fresh code. Nothing is imported from POOLSIM, SENSING, SENSING2 or any earlier simulator.

**What remains (stated now so it can't be hidden later):** any learner that reliably minimises realized cost approaches the world's true optimum, so a pass shows "GTAO's continuous-time algebra correctly predicts what selection on realized payoffs finds in this discrete, noisy, learned world". It is **not evidence about nature**. Discreteness (integer read intervals, discrete-time Kalman, finite episodes), learning noise, self-tuned gains and bundled realized loss are the departures from the theory's idealisation; a miss would mean the theory's predictions do not survive them.

## 1. World (world.py)
- Discrete time. Shared driver g: Brownian, variance q_g per step. Private u_i: Brownian, variance q_u per step. Member target x_i = g + u_i. Stakes w = 1 per member per step, quadratic loss.
- **Tech R (complete reads):** a read costs C_R = 800 and returns the current value exactly; estimate held until the next read. Policy = integer interval T ∈ [1, 2000], random phase.
- **Tech A (averaging):** each step the tracker buys k units of sample rate at C_A = 1 per unit and sees y = x + √(SIG2/k)·z, SIG2 = 10⁴; estimate x̂ += α(y − x̂). Policy = k ∈ [0.01, 10⁷]; α self-tuned (golden section on ln α ∈ [−9, 0], own innovations only).
- **Flat organisation:** each member tracks its own x_i with the member technology.
- **Levelled organisation:** one level tracks g with the level technology (stakes N, because its error enters all N members' loss); each member tracks its own u_i (component readability, Axiom 4) with the member technology. Member loss is **bundled**: (e_g + e_u)². Upkeep h per step for the level in arm RRh.
- **Arms:** RR (R level, R members, h = 0), RRh (same, h = 40 = one member-cost unit, h′ = 1), AA (A/A), AR (A level over R members), RA (R level over A members).

## 2. Learning (no cost function anywhere)
- (1+1)-ES on log effort: 300 episodes; even episodes re-run the incumbent (running mean), odd episodes try a mutant (step s, reflecting bounds, mutant must be a different policy); accept if mutant's realized cost < incumbent's running mean; s ×e^0.8 on success, ×e^−0.2 on failure, s ∈ [0.1, 2]. Episodes: R = max(400, 20T) steps on a fresh path; A = 4000 steps on a fresh path (first 1000 not scored).
- The level learns on its own realized share of team cost (spend + N × realized g-error²). This assumes the level can attribute that share; the cross term with members' errors is not in its learning signal (it is in the evaluation).
- Members learn individually (16 flat-members and 16 residual-members per run, each its own ES).
- **Robustness learner (pop):** population selection — every grid policy lives through one long common realized path; the realized cheapest survives. Run on all scan arms with 8 seeds if time allows; never decides a verdict.
- Learner behaviour checked before lock (selftest.py, and a lone-ES spot check): ES medians within ~5–18% of the discrete optimum with sd(ln effort) ≈ 0.2–0.35. One ES pathology (stuck at an integer rounding boundary, 1/200) was found and fixed before lock (step floor 0.1, re-centre on integer).

## 3. Stage A ("measure one member, predict the group")
Lone trackers learn (ES) on a stakes × drift grid — R: W ∈ {0.25, 1, 4, 16}, q ∈ {0.03, 0.1, 0.3, 1}; A: W ∈ {1, 4, 16, 64, 256}, same q — 8 seeds each; realized cost measured on fresh long paths; (â, b̂) = OLS elasticities of ln realized cost on ln W, ln q, seed-cluster bootstrap CI. Locked in MEASURED_AB.json (sha256 + commit) **before any onset run**. Measured prediction: e_g,meas = −(1 − b̂_L)/(1 − â_L) using the **level's** technology.

## 4. Stage B (emergent onset)
- ρ grid {0.01, 0.02, 0.04, 0.08, 0.16, 0.32} (q_u = 1, q_g = ρ), 1.5 decades. 16 seeds per (arm, ρ).
- N grid per (arm, ρ): 17 points, centre × 2^((j−8)/2), centre = theory N* (GRID_CENTERS.json; used **only** to place a ×/÷16 grid; an emergent onset outside it is reported as invalid, not forced).
- Per (arm, ρ, seed): learn 16 flat members, 16 residual members, and one level per N. Then evaluate on a fresh path, 400,000 counted steps after 2,500 warm-up, 64 members, common random numbers between flat and levelled (two designs competing in the same world). Per-member realized cost: flat; levelled = (level spend + h)/N + mean e_g² + 2·mean(e_g·ē_u) + member residual costs. D_rel(N) = (flat − levelled)/flat. A second, independent-path flat evaluation (32 members) gives D_rel_ind (no common random numbers).
- **Factorial (T3, T1.7):** arms RR, RRh, AR, RA at base (q_g, q_u) = (0.04, 1) and cells shared×2, private×2, both×2; 16 seeds, same seeds across cells (paired).
- Smoke test before lock: one RR and one AA job on an out-of-design cell (ρ = 0.5); only timing and output structure were looked at.

## 5. Predictions (theory.py → THEORY_PREDICTIONS.json, locked)
| Arm | Theory e_g over the ρ window | Asymptote | Rival (members' tech) | Rival (tech-independent) |
|---|---|---|---|---|
| RR | −0.963 | −1 | −1 | −1 |
| RRh | −0.970 | −1 | −1 | −1 |
| AA | −1.925 | −2 | −2 | −1 |
| AR (A level / R members) | −1.944 | −2 | −1 | −1 |
| RA (R level / A members) | −0.950 | −1 | −2 | −1 |
(The window value is recomputed over whichever ρ are valid.)
- **V at onset** (level effort / flat member effort; R effort = reads/step, A effort = k): RR 1 + (1+ρ)^−½ = 1.995 … 1.870 (math review exact, h = 0); RRh (h′ = 1, math-review §4 formula) 2.724 … 2.517; AA 903 … 31 (theory, ∝ 9/ρ asymptotically).
- **T3 factorial** Δln N*: RR shared −0.674, private +0.683, both 0.000; RRh −0.678, +0.551, both −0.134 (T1.7); AR −1.358, +1.025, both −0.347; RA −0.668, +0.911, both +0.231. **Signs** are the test; magnitudes reported.
- **Findability (pre-registered directions):** F1 (from POOLSIM): perception noise on the adoption decision biases the fitted slope steeper (|ê| up) until the onset becomes unfindable. F2 (P10): under "adopt only if the saving exceeds ε", no adoption at any N when ρ ≤ (1−ε)^{−1/b} − 1 (R: 0.0060, 0.0203, 0.0628 at ε = 0.3%, 1%, 3%). F2 is weak (it nearly follows from bounded savings) and is labelled so.

## 6. Locked estimators and verdict rules (analyze.py)
- N̂*(ρ): seed-mean D_rel(N) → isotonic fit (PAVA) → upward zero crossing interpolated in ln N. Valid if the crossing exists in ≥ 90% of 2,000 seed-bootstrap replicates.
- ê: OLS slope of ln N̂* on ln ρ over valid ρ; 95% CI = percentile seed bootstrap. Needs ≥ 4 valid ρ spanning ≥ 1 decade, else INCONCLUSIVE.
- **Exponent verdict (each arm):** PASS if |ê − e_pred| ≤ 0.15|e_pred|; MISS if not, and the CI excludes e_pred; otherwise INCONCLUSIVE.
- **C1 technology contrast (rival: exponent independent of sensing technology):** ê_AA − ê_RR, paired-by-replicate bootstrap. Rival killed if the CI upper bound < −0.4. Theory missed if the CI excludes the predicted difference and |diff − pred| > 0.3.
- **C2 level-vs-member technology (T1.8; rival: members' technology sets e_g):** AR and RA each judged by the exponent rule; the rival is killed in an arm if its CI excludes the rival value and |ê − rival| > 0.3. T1.8 PASSES overall only if both arms PASS and the rival is killed in both.
- **V:** V̂(ρ) = level effort at N̂* (local log-linear fit of the level's learned effort over the 9 grid points nearest N̂*, pooled seeds) / geometric-mean flat-member effort. Per arm: geometric-mean ratio V̂/V_pred over valid ρ. PASS if within ×/÷1.15; MISS if outside and its CI excludes 1; else INCONCLUSIVE.
- **T3 / T1.7:** Δln N̂* per cell vs base, paired bootstrap. PASS if the CI excludes 0 with the predicted sign; MISS if the CI excludes 0 with the wrong sign; otherwise INCONCLUSIVE. For a predicted Δ = 0 (RR both×2): PASS if the CI includes 0 and |Δ| < 0.1; MISS if the CI excludes 0. The contingency-theory rival (same sign for shared and private volatility) is killed in an arm if both shared and private cells PASS.
- **Measured-(a,b) prediction:** the exponent rule applied with e_g,meas from Stage A.
- **Secondary (never decide a verdict):** level ratio Π = N̂*/N*_theory per ρ; logistic N50 slope; no-CRN slopes; pop-learner slopes; F1/F2.
- Estimator dry run on synthetic truth with no simulator (dryrun_synth.py): true −1 recovered as −1.015 [−1.078, −0.898]; true −2 as −2.074 [−2.154, −2.014]. Known small steep bias from noise at the smallest ρ (+1.5% and +3.7% here), inside the 15% tolerance; disclosed.

## 7. What each outcome would mean
- PASS on RR/AA and C1 rival killed: inside this non-formula learned world, the onset exponent is set by the sensing technology, as GTAO's algebra says.
- C2 PASS: the level's technology, not the members', sets e_g (the contrast SENSING2 never ran cleanly).
- MISS anywhere: the continuous-time prediction does not survive learning/discreteness for that claim; it is reported as a miss, not re-explained away.
- None of this is evidence about real organisations.

## 8. Resource rules
nice 19, OPENBLAS/OMP single-threaded, 3 worker processes, total RSS target < 1.5 GB, one heavy job at a time. Box is shared with another agent's ONA job; runs may be slowed.
