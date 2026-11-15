# RESULTS — AQN-ESTIMATORS (QUEUE pick 11, unaided slot; ledger 57–59, outcome 61+)

Executor `queue-pick11` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York. Lock `3595c48` (authored 13:40 ET as `3595c48`, pushed to origin before any data fetch, then rebased onto main unchanged; PREREG.md, code, seeds and all synthetic validation committed before any real data was fetched). Demo run after the lock, about 13:42 ET. **Measurement infrastructure, not a test of GTAO:** no CLAIM_MAP status changes; THEORY.md not edited (edits proposed in §4). Not independently refereed (new item AQN-REFEREE).

## 0. Bottom line
1. **α, q, N (Gaussian world or the best linear tracker): validated.** A parametric Whittle fit on increments, with exact aliasing and an explicit white-noise term, recovers α, q and N without bias and with nominal 95% coverage once the record has **M ≳ 250 Fourier frequencies below the signal–noise crossover**; SE(α̂) ≈ 1/√M (Robinson's local-Whittle rate, applied). For a ±0.1 interval on α, M ≈ 400: about 8 000 steps when noise crosses over at ω_c = 0.5 rad/step, about 130 000 at ω_c = 0.05. N is identifiable only when the noise floor is visible inside the band; otherwise only an upper bound exists.
2. **Common shortcuts are biased.** DFA under sensing noise underestimates α by 0.17–1.5; a single corner inside the band biases a pure power-law fit low (single OU: 1.87, not 2). The locked corner check (LR > 6.63: size ≤ 0.02, power 0.94–1.00 at n ≥ 8192) catches the corner.
3. **Switching worlds: λ and μ separately, validated.** A two-state HMM recovers jump rate, jump size, noise and the Bayes adaptation time t_A of THEORY v1.4.3 §2.2 (N16) with nominal coverage once the record holds ≳ 16 switches. **SE(log λ̂) ≈ 1/√(number of switches)**, nearly independent of per-sample SNR. q is recovered equally well by the Gaussian route, so the linear optimum needs no HMM; the Bayes optimum does.
4. **Premise test works for the class pair it covers.** HMM vs Gaussian-Markov LR with a parametric bootstrap: size 0.00–0.05, power 0.93–1.00 down to per-sample SNR 0.11. It decides only "two-state switching vs Gaussian Markov".
5. **Event worlds.** Cox counts: α̂ and q̂ are unbiased with nominal coverage at ≥ 5 events per bin, and the free floor recovers the Poisson floor (N = mean rate). A renewal world masquerades as a 1/f Cox world in the count spectrum (α̂ ≈ 0.5, as Lowen & Teich 1993 predict). Two flags catch it: the floor sits at 0.33–0.39 of the Poisson floor, and the gap-order test is null.
6. **Stakes are the binding input.** An error-cost slope is unbiased only if the error varies **exogenously**. Measurement noise in the error attenuates it (fixed by a replicate measurement and IV), but self-selected error (high-stakes units track better) biases it 3× low, and IV does not help. **No series-only method gives stakes.** SAME-SYSTEM-AQN needs a system with designed or natural-experiment error variation.
7. **Locked demo (FRED, on proxy).** DGS10, the daily 10-year yield, 1990–2026: α̂ = 2.00 ± 0.03, no corner (LR 2.75), bands agree (z 0.48), N below detection (crossover above Nyquist), premise p = 0.95 (Gaussian Markov not rejected). **On proxy "daily published value as target", the 10-year yield behaves as a random walk at daily-to-decade scales: THEORY's α = 2 case.** log VIX: corner detected (LR 32, ω0 ≈ 0.008 rad/business day, about a 3-year period) and band slopes disagree (1.59 vs 1.94, z −2.97), so the regime is **not established** under the locked rule. The locked label rule R1 has a flaw: it labels DGS10 "B" because it gave no label to α ≈ 2 without a corner. Declared in §3, not re-labelled after the fact.

## 1. Synthetic validation (before the lock; identical to the locked `RESULTS_validation.md`)

All numbers from `results/summary_{A,B,C,E,P,S,asym}.txt` (code `validate.py`, `summarize.py`; 50–300 reps per condition; Monte Carlo SE of a 95% coverage ≈ 0.02 at 100 reps, 0.03 at 50).

### 1.A Power-law Gaussian worlds: Whittle α, q, N (block A; fBm with α ∈ {1.4, 2.0, 2.6}, white noise set by the crossover ω_c = (q/s2)^{1/α} ∈ {0.05, 0.5, 3} rad/step, n ∈ {512 … 32768})
- **Validated** (|median bias| ≤ 0.05 in α, coverage 0.88–0.99) whenever the number of Fourier frequencies below the crossover, **M = n·min(ω_c, π)/2π, is at least ≈ 250**: e.g. α = 2, ω_c = 0.5, n = 8192 (M ≈ 650): bias −0.006, RMSE 0.047, coverage 0.94; α = 2.6, ω_c = 0.05, n = 8192 (M ≈ 65): bias −0.005, coverage 0.94. log q and log s2 behave the same way (coverage 0.88–0.98).
- **Sample length rule (from the expected Whittle information, `summary_asym.txt`, matched by Monte Carlo):** SE(α̂) ≈ 1/√M. A ±0.1 interval on α (SE 0.05) needs M ≈ 400: n ≈ 8 000 steps if noise crosses over at ω_c = 0.5, n ≈ 130 000 at ω_c = 0.05, n ≈ 500 000 at ω_c = 0.005. This is Robinson's (1995) local-Whittle variance 1/(4m) for d, with α = 2d, so it is a known rate, applied: sensing noise does not change the rate in this long-span setting, it only removes the frequencies above ω_c. (Under infill asymptotics with fixed noise the optimal rate is slower, n^{−1/(4H+2)}, Gloter & Hoffmann 2007; that setting does not apply when the span grows.)
- **Identifiability limits.** (i) M ≲ 30 (n = 512 at ω_c = 0.05): α at the bound in 13–22% of runs, SEs meaningless. (ii) α = 1.4 with heavy noise: bias +0.10 (n = 8192, M ≈ 65, coverage 0.80) and +0.04 (n = 32768, coverage 0.86): a shallow signal separates poorly from white noise; needs M ≳ 1000. (iii) **N is unidentified when noise is negligible** (ω_c > π): log ŝ2 has median bias near 0 but RMSE 0.3–9 and absurd SEs at n ≤ 2048; only an upper bound on N is meaningful then.
- **Comparators.** DFA-1 is biased low under sensing noise by 0.17–1.5 in α (e.g. −0.39 at α = 2, ω_c = 0.5, n = 8192; −1.50 at α = 2.6, ω_c = 0.05) and is fine only without noise (≤ 0.03). The variogram with a nugget (FRAMEWORK §3.1's procedure) is roughly unbiased for α but has 1.5–3× Whittle's RMSE, and its N estimate is poor when noise is small. **Consequence:** any earlier or future α from DFA or from a nugget-free variogram on a noisy series is biased toward smaller α (redder worlds look whiter).

### 1.B Misspecified Gaussian worlds (block B)
- **1/f superposition of 60 OU processes** (corners 10⁻⁴–10 rad/step, nominal α = 1.5; truth = Whittle pseudo-true over the band [0.002, π], α* = 1.48): bias ≤ 0.013, coverage 0.96–0.99 at n = 2048–32768. A band slope is recoverable from a mixture.
- **Single OU (corner 0.01 rad/step; Regime A above the corner), pure power law fitted over the full band:** α̂ ≈ 1.87 (pseudo-true 1.86–1.88), **not 2**: a corner inside the band biases the band slope low. The corner model recovers α ≈ 1.98–2.01 and ω0 ≈ 0.009–0.010.
- **Corner check** (LR, corner model vs pure power law): size at LR > 2.71 is 0.05–0.11 on pure fBm; at the locked threshold **6.63 the size is 0.00–0.02** and the power against the single OU is 0.17 (n = 2048), 0.94 (8192), 1.00 (32768). Locked rule: report the corner-model α when LR > 6.63.

### 1.C Switching world: HMM λ, μ, N, t_A (block C; levels ±1, σ ∈ {0.5, 1.5, 3}, λ ∈ {0.002, 0.01}, κ = λN/μ² from 0.0005 to 0.09, n ∈ {2048, 8192, 32768})
- **Validated whenever the record holds ≳ 16 expected switches** (λn ≥ 16): every condition with λn ≥ 16 has |median bias| ≤ 0.04 in log λ, log μ, log s2, log t_A and log q, and coverage 0.88–1.00 (the two 0.88 cells are at 50 reps).
- **The precision of λ̂ is set by the number of switches:** SE(log λ̂) ≈ 1/√(λn) (0.25 at 16 switches, 0.11 at 82, 0.06 at 328), almost independent of the per-sample SNR (0.11–4). μ̂ and N̂ are much more precise (SE 0.003–0.04 in log). The Bayes adaptation time t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1] inherits λ only through the log: SE(log t̂_A) 0.01–0.12 at λn ≥ 16.
- **Limit:** with ≈ 4 expected switches (n = 2048, λ = 0.002) log λ̂ has RMSE 0.6–1.3 and log μ̂ occasional failures (RMSE 1.6 at σ = 0.5; median fine).
- **Both routes recover q** in a switching world: HMM q̂ = 4λ̂μ̂² and the Gaussian (OU) fit's q̂ have similar bias and RMSE (e.g. 0.27 vs 0.30 at σ = 1.5, λn = 16). So a q measured by any second-order method is valid for the linear optimum in a jump world; only λ and μ separately need the HMM. (In-model check of THEORY v1.4.3 §2.2's premise bullet, not new.)

### 1.D Premise test: two-state switching vs Gaussian Markov (block P; LR of HMM vs AR(1)+noise, parametric bootstrap B = 39 under the fitted Gaussian null, reject at p ≤ 0.05; 40 series per cell)
- **Size** under OU + noise worlds with the same autocovariance as the switching worlds: 0.00, 0.00, 0.00 (n = 8192) and 0.05 (n = 2048).
- **Power** against two-state switching: 1.00 at n = 8192 even at per-sample SNR μ²/σ² = 0.11 with 16 expected switches; 0.93 at n = 2048 with only ≈ 4 expected switches.
- Scope: this compares one non-Gaussian class (symmetric two-state) with one Gaussian class (Markov, α = 2). It does not test multi-state, power-law-jump or fBm-Gaussian alternatives (new item PREMISE-TEST-WIDEN).

### 1.E Event worlds (block E)
- **Cox counts** (rate Λ̄(1 + z), z the 1/f mixture with sd 0.3; band [0.002, π]): at Λ̄ = 5 per bin, α̂ bias ≤ 0.01, coverage 0.94–0.95 (n = 8192: SE 0.14; n = 32768: 0.07); log q̂ coverage 0.92–0.95. At Λ̄ = 0.5 per bin the rate signal is mostly buried in shot noise (SE(α̂) 0.45; coverage 0.90–0.91): event worlds need many events per correlation time. The free floor estimates the Poisson floor: ŝ2/mean = 1.00 (5–95%: 0.96–1.03). Fixing the floor at the mean (Poisson premise) gives the same α̂ with ≈ 8% smaller SEs.
- **Truth-normalisation bug found and fixed during validation:** the first E run stored a pseudo-true q that was 2π too large (density vs 2π·density). Detected because log q̂ coverage was 0.00–0.05 while α̂ was fine; `validate.E_truth` corrected and `summarize.py` recomputes the truth; estimates unchanged. Recorded here, not hidden.
- **MMPP (rates 1 and 3 per bin):** log λ̂ bias ≤ 0.07 (median ≤ 0.05), coverage 0.96–0.98 at 16–82 expected switches; rates recovered to < 1%.
- **Renewal control (Lomax gaps, shape 1.5, mean 1 per bin):** the count spectrum is 1/f-like and the free-floor Whittle reports α̂ ≈ 0.52 (Lowen & Teich 1993: D = 2 − shape = 0.5), i.e. **a renewal world masquerades as a rate-modulated one in the count spectrum.** Two flags catch it: the free floor sits far below the Poisson floor (ŝ2/mean median 0.33–0.39, 5–95% 0.0–0.69, vs 0.96–1.03 for Cox), and the gap-order test is null (z > 1.96 in 2–4% of runs, vs 98–100% for Cox at Λ̄ = 5 and only 50% at Λ̄ = 0.5).

### 1.S Stakes from an error-cost curve (block S; w = 2, quadratic loss, cost noise sd 0.5)
- Exogenous error, measured exactly: OLS slope unbiased, coverage 0.94 (n = 100 and 1000).
- Error measured with noise (noise/error sd ratio 0.5, 1): **OLS attenuates w by the reliability ratio** (median 1.29, 0.50 vs 2; coverage 0.00–0.07). With a second, independent error measurement, the IV slope is unbiased (2.01–2.03) with coverage 0.90–0.98.
- **Self-selected error** (high-stakes units track better, e ∝ w^{−1/2}, w log-normal): OLS gives 0.66 for a true mean w of 2 (coverage 0.00) and the replicate-measurement IV does not fix it (0.66). Stakes are identified only from variation in error that is exogenous to w (a designed perturbation or natural experiment), per FRAMEWORK §3.3. A cross-sectional error-cost regression across self-optimizing units is not a valid stakes estimator.

## 2. What each estimate feeds (premise, THEORY v1.4.3 §2.2 / §2.5; CLAIM_MAP N16, N17)
| Estimate | Valid for | Not valid for |
|---|---|---|
| Whittle α̂, q̂, N̂ | the linear optimum (memory time τ ∝ (N/q)^{1/α}, error, precision effort, kernel) in any world with these second moments; exact reset-read optimum (read rate ∝ (wq/c)^{1/α}) | the Bayes optimum of a non-Gaussian world |
| HMM λ̂, μ̂, N̂, t̂_A | Bayes optimum of the symmetric two-state world (N16: t_A, MSE 2μ²K₀/(K₀+K₁)); also q = 4λμ² for the linear optimum | multi-state or power-law-jump worlds (not derived) |
| Premise LR | choosing between those two optima, **fixed in the prereg before outcome data** (HEADLINE-PREMISE-SCOPE lock guard) | any wider class decision |
| Count Whittle α̂, q̂ (floor = mean) | linear optimum under Poisson sensing of a Cox rate | renewal or self-exciting worlds (check the floor and gap order first) |
| MMPP λ̂, rates | description only; the event-sensed Bayes optimum is not derived (POISSON-SENSING-JUMP) | — |
| Stakes ŵ (IV, exogenous error) | every optimum | cross-sections of self-optimizing units; inversion of the system's own design (circular for N13) |

## 3. Locked demo, read by the pre-declared rules (`demo.py`, `results/demo.json`; raw CSVs in `data/`, SHA-256 in the JSON)
Proxy for both: "daily published FRED value as the drifting target; published value = target + white sensing noise; business days as equal steps". No design quantity or stakes measured: **not an N13 test.**

| | DGS10 (10-y yield, %) | log VIXCLS |
|---|---|---|
| n (1990-01-02 … 2026-10-30) | 9 214 | 9 307 |
| Whittle full band α̂ ± SE | 2.004 ± 0.026 | 1.813 ± 0.027 |
| log q̂ ± SE (per business day) | −5.70 ± 0.04 (q ≈ 0.0033 %²/day) | −5.48 ± 0.04 |
| ω_c (signal = noise) | 8 640 rad/step (> π: N not identified; R2 → upper bound only) | 4 020 (> π: N not identified) |
| low band (periods > 20 days) / high band α̂ | 2.12 ± 0.07 / 2.07 ± 0.08; z = 0.48 | 1.59 ± 0.08 / 1.94 ± 0.08; **z = −2.97** |
| corner LR (threshold 6.63); ω0; corner-model α | 2.75; —; 2.00 | **32.4**; 0.0082; 1.81 |
| DFA α; variogram α | 1.99; 1.99 | 1.63; 1.59 |
| excess kurtosis of increments | 2.4 | 6.7 |
| premise LR (HMM − OU), bootstrap p (B = 39) | −54 485, p = 0.95 | −21 249, p = 0.40 |
| **R1 regime label as locked** | "B" (scale-free over the band, α̂ = 2.00) | **not established** (corner and band disagreement) |

Reading:
- **DGS10.** R1 as locked gives "B" because the rule gave α ≈ 2 without a corner no label of its own. THEORY §2.2 calls that case Regime A ("a random walk with white increments"). Correct reading, declared here as a flaw in R1: **α = 2 over the full band (3.7 decades of frequency, periods 2 days to 37 years) on proxy, i.e. Regime A's random-walk form**, q ≈ 0.0033 %² per business day, N below detection at daily resolution. (Rounding to 0.01% implies s2 ≥ 8 × 10⁻⁶, which puts the crossover near ω ≈ 20 > π, consistent with N not being identified.) Fat-tailed increments (kurtosis 2.4) do not make the two-state model preferable (p = 0.95). FRAMEWORK §3.1 step 4 ("detect jumps via the kurtosis of increments") would have flagged jumps here. The LR test does not.
- **log VIX.** It is mean-reverting at multi-year scales (corner ≈ 3 years) and has no single slope across bands, so the regime is not established and there is **no GTAO prediction for it** (THEORY §2.2 "Not established"). DFA and the variogram track the low band (≈ 1.6). This bears on VIX-KERNEL, whose α is meant to come from realized variance, not from implied variance; noted there.
- R4 did not fire (|DFA − Whittle| = 0.02 and 0.19 < 0.3).

## 4. Proposed edits (not applied; independent review first)
- **E-A1 (FRAMEWORK §3.1, procedure).** Primary estimator: parametric Whittle on increments with an aliased power law plus white noise (`measurement/estimators/aqn.py`), corner check and band-consistency z. Variogram-with-nugget becomes a convergent check. DFA is not used on noisy series. Replace the power rule "≥ 1.5 decades with ≥ 30 independent increments" with "**SE(α̂) ≈ 1/√M**, M = Fourier frequencies below the crossover; ±0.1 needs M ≈ 400".
- **E-A2 (FRAMEWORK §3.1 step 4).** Replace "detect jumps via the kurtosis of increments" with the HMM-vs-Gaussian LR and parametric bootstrap, its scope stated. DGS10 shows that kurtosis alone over-flags.
- **E-A3 (FRAMEWORK §3.3, stakes).** Add: the error must vary exogenously (designed perturbation or natural experiment); use a replicate error measurement and IV for errors-in-variables; never estimate stakes by cross-sectional regression across self-optimizing units, or by inverting the system's own design.
- **E-A4 (THEORY §2.4 Net, last sentence; wording only).** "The first job is measurement (QUEUE AQN-ESTIMATORS, SAME-SYSTEM-AQN)" → "The first job is measurement: estimators for α, q, N and, in switching worlds, jump rate and size are validated on synthetic truth (`measurement/estimators/`, not yet refereed); stakes need exogenous error variation (QUEUE SAME-SYSTEM-AQN)."
- **E-A5 (THEORY §11 item 2, "estimator dry-runs on synthetic truth before locking").** Add a pointer: "done for α, q, N, λ, μ, event-world rates and stakes (`measurement/estimators/RESULTS.md`)".
- No change to §0, §1 or §2.2 content is proposed.

## 5. Surprises (read per QUEUE rule 4) and new items
- **Stakes, not spectra, are the binding input for N13** (§1.S). It is not a numeric surprise against a locked prediction, but it re-prioritises SAME-SYSTEM-AQN: candidate systems must offer exogenous error variation. → new item **STAKES-EXOGENOUS**.
- **DFA and nugget-free variogram α̂ are biased low under noise** (by up to 1.5). Earlier α/H estimates in the repo that used such methods may be biased (e.g. Allan-factor Ĥ in GITHUB-UPSTREAM's addendum, a count-process statistic). LFK-ALPHA-SPF used a Matérn + white Whittle fit, which is fine. → new item **ALPHA-ESTIMATE-AUDIT**.
- **The premise test covers one class pair only.** → new item **PREMISE-TEST-WIDEN** (multi-state and fBm-Gaussian nulls; power-law jumps).
- **The R1 label rule had a gap at α ≈ 2 without a corner** (DGS10). → folded into **AQN-REFEREE** (hostile referee of the estimators, the validation, the label rules and the demo reading).
- **Sample-length rule M ≳ 400** means quarterly SPF series (n ≈ 240) cannot give α to ±0.1. That is consistent with LFK-ALPHA-SPF's wide α intervals and the failed MV8. Note added to SPF-AQN-POWERED and SAME-SYSTEM-AQN.
- **Weak (demo, on proxy):** log VIX has a multi-year corner and band-dependent slope. Note on VIX-KERNEL: measure α on realized variance, with the corner check.

## 6. Files
`PREREG.md` (lock), `aqn.py` (estimators), `validate.py` (synthetic worlds, seeds), `summarize.py`, `results/summary_*.txt` (+ gzipped raw), `demo.py`, `results/demo.json`, `data/` (FRED CSVs as fetched), `priorart/NOTES.md` (what was read; abstracts only).
