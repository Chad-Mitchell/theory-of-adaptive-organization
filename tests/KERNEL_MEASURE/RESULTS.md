# RESULTS — KERNEL-MEASURE (QUEUE pick 28, uniform slot; ledger 130–132 + outcome)

Executor `queue-pick28` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York. Lock `6d235ed` (PREREG.md, code, data hashes, MV10 gate output; pushed to `origin/q-pick28` at about 6:05 PM ET before the VIX kernel regression). Locked run `decide.py run` about 6:06 PM ET (`results.json`, `results.out`). Not independently refereed (new item KERNEL-MEASURE-REFEREE).

## 0. Bottom line
**PASSED on proxy "Parkinson range variance as driver, 2 ln VIX as tracker, survival at 21 business days of the 504-day binned projection kernel", exploratory, not decisive.** It is the first tracking kernel measured in any GTAO test, with α, q, N measured on the same system's driver.
- Measured survival at one horizon Ŵ21 = **0.260** (block-bootstrap SE 0.041; 95% CI 0.178–0.341) vs the theory kernel's **0.277** (σ_pred 0.026 from the driver's α̂, q̂, N̂). D = −0.017, 95% CI −0.114 to 0.079, inside the locked ±0.13 band. All three named rivals excluded: α = 2 Kalman/EWMA (exponential forgetting) 0.000, flat 1/5/22-day averages 0.012, "matching" survival exponent α − 1 0.725.
- **Why not decisive (pre-declared):** the lock is decisive only if the realized σ_D ≤ 0.040 (the resolution at which MV10's P(PASS | true) ≥ 0.8 holds). Realized σ_D = **0.049**: VIX carries tracker noise of about r ≈ 0.4–0.5 of the forecast sd (between the simulated r = 0.35 and 0.5 cells), where the gate gave P(PASS | true) 0.76–0.33. So the PASS stands as the locked rule's verdict but is exploratory.
- **Fragile to the noise treatment of α̂ (pre-declared sensitivity):** with the in-band free-noise α̂ = 1.19 ± 0.10 the prediction is 0.318 ± 0.059 and the verdict is **INCONCLUSIVE** (CI of D −0.200 to 0.083). Block length 252: PASS (Ŵ21 0.262 ± 0.038).
- **Not a test of Bayes vs linear** (own-observation-type projection, THEORY §2.5) and not of N16. It tests the §2.2 spectrum → kernel map for the linear optimum, on proxy, on one system.
- **The tail exponent α/2 itself is not resolvable here.** Design 1 (kernel family (τ+c)^−(1+s)) gives ŝ = 0.62 (95% bootstrap 0.28–0.79) against raw α̂/2 = 0.63 and the like-with-like 0.58, but it failed MV10 before lock (a flat 1/5/22-day kernel reads ŝ ≈ 0.52); the bin-based tail slope is undefined in 83% of bootstrap draws.

## 1. Regime first (driver only; PREREG §2)
Regime B over periods 21 d – 37 y: in-band α̂ 1.24 ± 0.45 (21–126 d) vs 1.15 ± 0.30 (> 126 d), z = −0.16; corner LR 2.26. Locked α̂ = 1.2587 ± 0.0429 (noise fixed at the full-band ŝ2 = e^−0.90; own Brownian-range floor 0.34–0.39 vs 0.41). AQN's R1 as written labels the driver "not established" because its fixed 20-day split puts a noise-dominated high band (α̂ 2.83 ± 0.51) against the signal band; declared, and the band chosen before any VIX regression (new item AQN-R1-NOISE-BAND).

## 2. The locked numbers (`results.json`)
| | Ŵ21 | boot SE | W21_pred | D [95% CI] | σ_D | rivals excluded | verdict |
|---|---|---|---|---|---|---|---|
| primary (blocks 126) | 0.260 | 0.041 | 0.277 | −0.017 [−0.114, 0.079] | 0.049 (> 0.040: exploratory) | yes | **PASS** (exploratory) |
| free-noise α̂ 1.19 | 0.260 | 0.041 | 0.318 | −0.059 [−0.200, 0.083] | 0.072 | yes | INCONCLUSIVE |
| blocks 252 | 0.262 | 0.038 | 0.277 | −0.015 [−0.106, 0.076] | 0.046 | yes | PASS (exploratory) |
n = 9 276 driver days (1990-01-02 … 2026-10-30), 3 VIX days missing, 8 694 regression rows (69 blocks).

## 3. POST HOC, descriptive (after the locked run; `posthoc_bins.py/.json`; not part of any decision)
Share of kernel weight by age bin, VIX vs the theory kernel (same estimator on a 200 000-day noiseless simulation):

| ages (business days) | 0 | 1 | 2–4 | 5–9 | 10–20 | 21–41 | 42–83 | 84–167 | 168–335 | 336–503 |
|---|---|---|---|---|---|---|---|---|---|---|
| VIX | 0.164 | 0.117 | 0.183 | 0.133 | 0.143 | 0.100 | 0.072 | 0.084 | 0.028 | −0.024 |
| theory | 0.136 | 0.099 | 0.184 | 0.153 | 0.140 | 0.098 | 0.070 | 0.050 | 0.034 | 0.036 |

The measured kernel tracks the theory's through about 4 months; beyond about 8 months VIX's weight falls to zero (last bin negative) where the theory keeps 0.036. Candidate reasons, untested: mean reversion of variance at multi-year scales (the log-VIX corner at about 3 years in the AQN demo; no corner detected in the driver band, LR 2.26), a variance-risk-premium term, or noise (single bins are imprecise). The summed slope is 0.75, not 1: VIX moves less than one-for-one with the theory forecast (also seen pre-lock: Var(2 ln VIX) 0.49 < Var(forecast) 0.64). The long-sim theory survival at 21 days is 0.288 vs the planned-n mean 0.277 (finite-sample bias of the estimator, ≈ 0.01; the lock used the planned-n value, like with like).

## 4. Surprises read (QUEUE rule 4)
1. **Weak-moderate:** the kernel shape matches the spectrum-derived kernel over ages 0–167 d with no fitted kernel parameters; the theory's own optimum reproduces the market's weights through 4 months on proxy. Exploratory and fragile to α̂'s noise treatment; needs a referee and a decisive design (new items KERNEL-MEASURE-REFEREE, KERNEL-DECISIVE-RV).
2. **Weak:** the kernel's tail exponent α/2 is not resolvable from 36 years of daily data with a range proxy; a flat 1/5/22-day kernel mimics a power-law fit (design 1). VIX-KERNEL as written (tail ≈ τ^−(1+α/2)) needs a different statistic or intraday data (note added there).
3. **Weak:** AQN R1's fixed 20-day band split mislabels a noise-crossover-inside-band series as "not established" (new item AQN-R1-NOISE-BAND).
4. **Weak (post hoc):** VIX weight vanishes beyond ~8 months where the theory keeps 3–4%; a corner or premium term (new item KERNEL-LONG-LAG).

## 5. What changes
No CLAIM_MAP status change (exploratory; K13 stays MATH-CORRECTED). THEORY §2.2's sentence "no kernel has been measured in any GTAO test" and the §2.4 evidence table are now out of date: proposed edit in a separate PR, **DO NOT MERGE without separate reviewer PASS** (Chad t1916). No locked prereg's goalposts move. H8 vigilance stays OPEN.

## 6. Prior art
None read this session; nothing new credited. THEORY's existing credits for the noiseless kernel (Gatheral, Jaisson & Rosenbaum 2018 among them) are unchanged and were not re-read. The flat 1/5/22-day rival is named descriptively, not credited.

## 7. Files
`PREREG.md` (lock), `klib.py`, `decide.py`, `gate.py`/`gate.out`, `power_sim.py`/`power/` (design 1), `power_sim2.py`/`power2/` (design 2), `coverage.out`, `check_kernel.py/.json`, `driver_spectrum.py/.json`, `driver_band.py/.json`, `range_floor.py/.json`, `results.json`/`results.out`, `posthoc_bins.py/.json`, `data/` (GSPC_ohlc.csv, VIXCLS.csv, raw Yahoo JSON), `SHA256SUMS`.
