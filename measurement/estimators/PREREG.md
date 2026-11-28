# PREREG — AQN-ESTIMATORS: estimators for α, q, N, stakes, and jump rate / jump size, validated on synthetic truth; locked real-data demo

Executor `queue-pick11` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York, branch `q-pick11-aqn`. Queue: post-protocol pick 11, unaided slot (ledger 57 unaided order, 58 rule_rank, 59 pick). **The lock is the git commit that adds this file** together with `aqn.py`, `validate.py`, `summarize.py`, `demo.py`, the synthetic results in `results/` and the prior-art notes in `priorart/`. No real data had been fetched or looked at for this item when the lock was committed (`data/` does not exist at the lock).

## 0. Source in THEORY.md v1.4.3, premise, regime (stated before any data)
- **What needs these inputs.** §2.1: "Three quantities set the tracking optimum in time: the slope α, the high-frequency drift level q (S = q|ω|^−α), and the sensing noise N, together with stakes w and the prices of reads, precision and stores." §0 and §1 N6 / CLAIM_MAP N13 (the open bet) need all four measured on the same system. §2.4 Net: "The first job is measurement (QUEUE AQN-ESTIMATORS, SAME-SYSTEM-AQN)."
- **Premise (THEORY v1.4.3 §2.2 Regime A premise bullet; §2.5 premise list; CLAIM_MAP N16, N17).** The §2.2 noisy-sensing rows (error, precision effort, memory time, kernel) hold for a Gaussian world or for the best linear tracker in any world; for those, the second-order inputs (α, q, N) are sufficient. For the Bayes-optimal tracker of a switching world they are not: jump rate λ and jump size μ enter separately (at fixed q and N the two-state Bayes error spans 364× across splits of q, `reviews/night2/HEADLINE_PREMISE_SCOPE_checks/check.out`). So every estimate below is labelled with the optimum it feeds:
  - Spectral estimates (α̂, q̂, N̂; Whittle) feed the **linear** optimum, in any world with those second moments.
  - Switching-world estimates (λ̂, μ̂, N̂; HMM) feed the **Bayes** optimum of the symmetric two-state world (t_A, MSE of N16) and, via q = 4λμ², the linear one.
  - Which optimum a later test compares against is fixed in that test's prereg (lock guard, HEADLINE-PREMISE-SCOPE P-lock), not chosen after seeing data. The premise test of §2 below is a tool for that choice; it decides only "two-state switching vs Gaussian Markov", nothing wider.
- **Event worlds.** Rate-modulated (Cox) counts: the Poisson floor of the count spectrum is the sensing noise (N = mean rate) and the rate spectrum gives α, q. Renewal worlds are a different class (N17 failed pure renewal on code edits on proxy); the count spectrum alone cannot separate renewal from Cox (Lowen & Teich 1993), so the floor test and N17's gap-order statistic are reported with every event-world estimate. The Bayes optimum for event-sensed jump worlds is not derived (QUEUE POISSON-SENSING-JUMP), so MMPP estimates (λ̂, rates) feed no derived optimum yet.
- **Stakes.** w is the slope of cost on squared tracking error (§2.1 quadratic loss; FRAMEWORK §3.3). It cannot be read from the tracked series. Inferring w from the system's own design (inverting the optimum) is circular for N13 and is excluded.
- **Regime.** This item is measurement, not a test of a GTAO prediction: nothing here can change N13 or any CLAIM_MAP status. Regime labels are outputs of the estimators (corner check, band consistency, premise test), never assumptions.
- **Adjustment lag:** not applicable.

## 1. Estimators (`aqn.py`)
| Input | Estimator | Feeds |
|---|---|---|
| α, q, N (continuous target + white noise) | Parametric Whittle on increments with exact aliasing, f(ω) = (4 sin²(ω/2)/2π)[q Σ_k |ω+2πk|^−α + s2], N = s2·Δt; optional band; Wald SEs from the expected Whittle information | linear optimum |
| regime check | (i) corner check: LR of a corner model q(ω²+ω0²)^−α/2 vs the pure power law (threshold 6.63 locked from validation §3); (ii) band consistency z of α̂ on periods > 20 steps vs ≤ 20 steps | regime label |
| comparators | DFA-1 (Peng et al. 1994) and variogram with nugget (FRAMEWORK §3.1 procedure) | none (reported) |
| λ, μ, N (two-state switching + white noise) | Gaussian HMM MLE (scaled forward algorithm), Wald SEs from the numerical Hessian; t_A and its delta-method SE | Bayes optimum (N16) |
| premise | LR of the HMM vs AR(1)+noise (OU sampled; same autocovariance class), parametric bootstrap under the fitted Gaussian null, B = 39 | which optimum is plausible |
| event α, q, N | Whittle on binned counts, f = (q ω^−α + s2)/2π over a band; free floor (s2/mean ≠ 1 flags non-Poisson sensing) and fixed floor s2 = mean | linear optimum (Poisson sensing) |
| event λ, rates | two-state MMPP HMM on binned counts | no derived optimum yet |
| renewal check | consecutive log-gap Spearman vs shuffle null (as in `tests/D3_OOS`) | class label |
| stakes w | slope of cost on e² (OLS) and, with a replicate error measurement, IV slope Cov(cost, e_rep²)/Cov(e², e_rep²); pairs bootstrap CI | all optima (independent of the series) |

## 2. Synthetic validation (done before the lock; seeds 20261115 + 1000·condition-offset + rep; `validate.py`, summaries `results/summary_*.txt`)
See RESULTS.md §1 for the numbers. Acceptance rules used to label an estimator "validated in condition X": |median bias| ≤ 0.05 in α (≤ 0.1 in log q, log s2, log λ, log μ, log t_A) **and** 95% Wald coverage in [0.88, 0.99] (Monte Carlo SE ≈ 0.02 at 100 reps). Conditions failing either are reported as identifiability limits.

## 3. Locked real-data demo (`demo.py`; runs only after this commit)
- **Data:** FRED daily DGS10 (10-year Treasury constant-maturity yield, %) and VIXCLS (CBOE VIX close, analysed as log VIX), public CSV `fredgraph.csv?id=…`, window 1990-01-02 to 2026-10-30, missing days dropped, business days as equal steps (declared distortion: weekends and holidays are not modelled). SHA-256 of each raw file recorded in `results/demo.json`.
- **Proxy labels:** "daily published value as the drifting target; published value = target + white sensing noise; business days as equal steps". Any statement from the demo is "on proxy …". Neither series has a measured design quantity or stakes here, so **no N13 test** is possible and none is attempted.
- **Outputs (all reported, none selected):** full-band Whittle (α̂, log q̂, log ŝ2 with SEs, crossover ω_c), low-band and high-band α̂ and band z, corner LR and corner-model α, DFA α, variogram-nugget (α, q, s2), excess kurtosis of increments, premise LR and bootstrap p (B = 39, seed 20261115 + 777), HMM (λ̂, μ̂, ŝ2, κ̂, t̂_A) and OU fits.
- **Pre-declared reading rules.** (R1) Regime label B ("scale-free over the band") only if corner LR ≤ 6.63, |band z| ≤ 2 and α̂ not at a bound; "A" if the corner model is preferred with corner-model α within 0.15 of 2; else "not established". (R2) N̂ is reported as a value only if ω_c < π/2 (noise visible inside the band); otherwise only as an upper bound (validation: s2 unidentified when ω_c > π). (R3) Premise: p ≤ 0.05 → "two-state switching preferred over Gaussian Markov on proxy …"; this does **not** establish a two-state world (only that class pair is compared). (R4) If DFA and Whittle disagree by > 0.3 with ω_c < π/2, the noise-robust Whittle value is reported and DFA's bias is noted (validation §1.A).

## 4. Run notes (declared before the lock)
- Blocks S and E first ran with multithreaded BLAS (load ~19); A, B, C, P, and E were then run single-threaded at `nice -n 19`. Results depend only on the seeds.
- Block C crashed once (`log` of an OU q̂ = 0 when φ̂ → 1); logs were guarded (`_lg`, returns None) and C was rerun in full with the same seeds.
- Block E's stored truth had a 2π normalisation error in q (RESULTS §1.E); fixed in `validate.E_truth`, recomputed by `summarize.py`; estimates unchanged.
- Raw results are gzipped (`results/*.json.gz`); `summarize.py` reproduces `results/summary_*.txt` byte for byte from them (checked).
