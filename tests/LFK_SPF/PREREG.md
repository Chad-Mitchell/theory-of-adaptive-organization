# PREREG — LFK-ALPHA-SPF: do professional forecasters track each variable's measured spectrum like the optimal noisy filter?

Locked by executor `lfk-spf` (for Ace; Chad t1914), Sunday 15 Nov 2026, America/New_York. Branch `lfk-spf-prereg`. The lock is the
git commit that adds this file; no outcome (no CG coefficient, no prediction for real SPF data, no environment fit of real data)
had been computed when it was committed. Seen before lock: row counts of the assembled files and the means of forecasts and actuals
(unit check, `build_data.py` output); the synthetic dry runs below. Queue: out-of-cycle manual pick by Ace, unscored for Q0 (ledger entry 10).

## 0. What is being tested, and the dependency on the referee (read first)
- **Source:** THEORY.md v1.3 §2.5 bullet "Spectrum map derived", item (v), and `reviews/night2/SPECTRUM_MAP/README.md` Prop. 5 /
  §4 P-LFKα (τ_m ∝ τ_E^{1−1/α}).
- **Referee (PR #10, `reviews/night2/SPECTRUM_MAP_REFEREE.md` §0 row 5), received before this lock:** τ_m ∝ τ_E^{1−1/α} holds only when
  the environment's variance is held fixed as τ_E moves; at a fixed high-frequency level q the slope is 0. The choice-independent form
  is τ_m ∝ (N/q)^{1/α}, which is **prior art** (Afterman, Chigansky, Kleptsyna & Marushkevych 2022, SIAM J. Control Optim. 60(3);
  Kleptsyna, Marushkevych & Chigansky 2020, Autom. Remote Control 81(3)); the α = 2 case is Mora & Nemenman, PRL 2019 (as cited by
  the referee; not re-opened here). So a τ_E-only slope test only tests the fixed-variance assumption. **This prereg was redesigned
  before lock to follow that:** the primary test estimates q (from each variable's spectrum) and N (from forecaster dispersion) per
  variable and tests the optimal-filter prediction for the forecasters' memory, i.e. "closeness to optimum". The τ_E slope is kept as a
  secondary (S1), labelled as a test of the fixed-variance assumption.
- **Novelty:** none claimed. A pass would say that a KNOWN filtering result describes SPF consensus forecasts across variables. The
  closest empirical prior art: Coibion & Gorodnichenko 2015 (AER 105(8):2644–2678; the CG coefficient, noisy-information reading);
  Bordalo, Gennaioli, Ma & Shleifer 2020 (AER 110(9):2748–82; consensus underreaction, individual overreaction, structural estimation
  that links CG coefficients to each series' persistence and forecaster noise); Afrouzi, Kwon, Landier, Ma & Thesmar 2023 (QJE 138(3):
  1713–1764; overreaction stronger for less persistent processes, lab). These were found by search this session (abstracts read),
  not read in full. GTAO's only increment here is the α-dependence (non-Markov spectra), tested by the α-specific sub-verdict.
- **Dependency:** if a later referee overturns the spectrum map's filtering results (SPECTRUM_MAP Thm 2 / Prop. 5 as re-scoped), the
  attribution of this test to GTAO is void; the in-model mapping here is computed numerically from the exact Wiener filter, so the
  numbers stand as a test of "optimal noisy filtering of the measured spectrum".

## 1. Regime first (THEORY §2.5 rule)
Regime is measured per variable from its own latest-vintage quarterly series, 1960Q1 (or first available)–2019Q4, by a Whittle fit
of S(ω) = s²[(1−φ)·Matérn(τ_E, α) + φ] (aliased, unit-variance Matérn with corner 1/τ_E and slope α above it, plus a white share φ).
Labels: A (Markov) if the 95% parametric-bootstrap interval of α contains 2; B (scale-free above the corner, measured α) otherwise.
The prediction is computed for each variable's own measured (τ_E, α, φ), so it does not require a common regime.

## 2. Measurement triple (MV1)
- **Target:** each SPF variable's value in quarter t+3 (growth variables: annualized q/q growth 100((X_q/X_{q−1})^4−1) computed from
  the forecast levels; CPI and other rates: SPF's annualized rates; levels: unemployment, housing starts, T-bill, Aaa, 10-year).
- **Pool:** SPF panel (consensus = mean forecast, `meanLevel.xlsx`; individuals, `SPFmicrodata.xlsx`), surveys whose target ≤ 2019Q4.
- **Channel:** the forecasters' revisions between surveys t−1 and t of the same target.
- **Actuals:** latest vintage (Philadelphia Fed RTDSM, last column; H.15 for TB 3-month secondary market, 10-year CMT, Moody's Aaa/Baa).
  FRED/ALFRED were unreachable from the box (connection reset), so first-release actuals are not used; revisions to data add noise,
  not bias, under standard assumptions — stated, not tested.
- **Candidates (21):** NGDP, PGDP, CPROF, UNEMP, EMP, INDPROD, HOUSING, TBILL, BOND, BAABOND, TBOND, RGDP, RCONSUM, RNRESIN, RRESINV,
  RFEDGOV, RSLGOV, CPI, CORECPI, PCE, COREPCE. Excluded a priori: RCBI, REXPORT (chained-dollar levels with base years that differ between
  survey and latest vintage).

## 3. Model (in-model instrument; `model.py`)
Unit-variance world with spectrum S (above). Each forecaster sees y_i = x + v_i, v_i white with variance K (in units of var x); each
uses the exact causal Wiener forecaster; the consensus of n_f forecasters (median panel size of that variable) is H*(x + v̄), var v̄ = K/n_f.
In-model moments: CG coefficient β(S,K,n_f) = Cov(x_{t+3} − F_t, F_t − F_{t−1}) / Var(F_t − F_{t−1}); dispersion ratio
D/vf = K(1−1/n_f)·mean|H₃|² / mean((S+K/n_f)|H₃|²). D/vf is strictly increasing in K (checked on 60 and 84 environments; no exception).
Dry-run checks (`checks_model.py`, `results/checks_model.out`): AR(1) noisy-information β = (1−G)/G reproduced to 4 decimals; the CG
coefficient's slope on log τ_E at fixed variance converges to 1−1/α (0.385/0.519/0.582/0.629 vs 0.333/0.5/0.6/0.667 at τ_E 200–1600;
MV7 known-groups for the instrument); at fixed q it is ≈ 0 (−0.006, −0.024), the referee's result.

## 4. Data → numbers (per variable)
1. Environment (stage `env`, run and committed before stage `outcome`): Whittle fit (τ̂_E, α̂, φ̂); α fixed at 2 fit (rival R-M);
   100 parametric-bootstrap refits each; pre-1990 fit (robustness R3).
2. SPF moments: β̂ = OLS slope of (actual − F_t) on (F_t − F_{t−1}) with a constant (Newey–West SE, 4 lags); D = mean over surveys of
   the robust cross-sectional variance (IQR/1.349)² of individual forecasts of the same target (surveys with ≥ 10 forecasters);
   vf = time variance of F_t over the same surveys. Joint uncertainty: circular block bootstrap over surveys (block 8; 100 draws).
3. **Prediction (GTAO / optimal filter):** K̂ solves D/vf(K) = D̂/v̂f in the measured spectrum; β^G = β(Ŝ, K̂, n_f).
   **Rivals:** R-S static noisy information β^S = D̂/v̂f (spectrum ignored; exact in the static limit); R-M same as GTAO with α forced to 2
   (Markov / Mora–Nemenman / LFK world); R-N leave-one-out median of the other variables' β̂ (no information).

## 5. Gates (exclusion; computed before outcomes except E4, which uses only the precision of β̂)
- E1: ≥ 80 surveys with a complete (error, revision) pair and ≥ 10 forecasters, targets ≤ 2019Q4.
- E2: 1.05 < α̂ < 5.9 (α identified, not at the bound).
- E3: τ̂_E < n_env/4 (corner inside the sample).
- E4: NW SE(β̂) ≤ 0.5 (CG coefficient estimable).
- n ≥ 8 included variables, else INCONCLUSIVE. If more than 1/3 of included β̂ ≤ 0: INCONCLUSIVE (noisy-information premise unmet).
  β̂ ≤ 0.02 enters logs as 0.02 (not excluded).

## 6. Inference and decision rule (proxy "SPF consensus CG coefficient, dispersion-identified noise, latest-vintage actuals")
MAE_X = mean over included variables of |ln β̂ − ln β^X|. Pairs bootstrap over variables (B = 2000, seed 20261115+2), each resampled
variable taking one joint draw (block-bootstrap β̂* and D/vf*, paired with a parametric environment draw). Calibration slope = OLS of ln β̂
on ln β^G.
- **PASSED on proxy** iff CI(MAE_G − MAE_S) < 0 and CI(MAE_G − MAE_N) < 0 and the calibration-slope CI contains 1 and excludes 0.
- **FAILED on proxy** iff the calibration-slope CI excludes 1, or CI(MAE_G − MAE_S) > 0, or CI(MAE_G − MAE_N) > 0.
- Otherwise **INCONCLUSIVE**.
- α-specific sub-verdict (GTAO's increment over the Markov prior art): CI(MAE_G − MAE_M) < 0 → "α-dependence helps"; > 0 → "hurts"; else
  inconclusive.
Secondary, no verdict: S1 OLS slope of ln β̂ on ln τ̂_E vs mean(1−1/α̂), ½ (LFK), 1 (§2.2 B), 0 (fixed q) — a test of the
fixed-variance assumption only; S2 slope of ln K̂ on ln q̂ (q̂ = (1−φ̂)c_α τ̂_E^{1−α̂}): 0 if noise ∝ variance, ≈ 1 if noise ∝
short-timescale volatility; robustness R1 full sample to 2026, R2 SD instead of IQR dispersion, R3 pre-1990 environment (point only).

## 7. Validity gates (FRAMEWORK §2.2) and the expected tier — stated before the outcome
- MV1 named (§2). MV2 partial: β̂ is the model's memory quantity only under noisy information; BGMS 2020 report individual overreaction,
  which this model does not have; dispersion includes model heterogeneity, not just signal noise. MV3 yes (q, α from the series; N from
  dispersion; neither uses β̂). MV4 yes (rivals are explicit). MV5 no (one method per input). MV6 partial (R-S, R-M, R-N).
  MV7 yes in-model (§3). **MV8 fails by the pre-lock dry run:** synthetic SPF data generated by the exact model (`synth_check.py`,
  `results/synth_T_7.out`, `synth_W_8.out`; n = 200 quarters, 35 forecasters, 24 random worlds) leave 5–6 of 24 variables after E2–E4
  (α unidentified at quarterly resolution when τ_E is a few quarters; β̂ SE > 0.5), and the α sub-test cannot tell the true model (arm T,
  CI(MAE_G − MAE_M) = [−0.92, 0.87]) from forecasters who ignore α (arm W, [−0.47, 0.97]). MV9: git lock, code in repo, raw-data
  sha256 in `data/RAW_SHA256.txt`, dry run on synthetic truth done; not externally timestamped (waived by Chad).
- **So this is Tier 3 and is expected to be INCONCLUSIVE by power.** It is run because it is cheap and its secondaries (S1, S2) answer
  the referee's normalization question on real data. **No CLAIM_MAP status may change from it.**

## 8. Files and seeds
`build_data.py` (assembly), `model.py`, `analysis.py` (`env`, `outcome`, `robust`), `checks_model.py`, `synth_check.py`; seeds 20261115+k.
Run: `nice -n 19 python3 analysis.py env && nice -n 19 python3 analysis.py outcome && nice -n 19 python3 analysis.py robust`.
Raw data on the box: `<local>/lfk_spf/` (Philadelphia Fed SPF and RTDSM xlsx, H.15 package; downloaded 15 Nov 2026 09:29–09:50 ET).
VIX-KERNEL (optional in the brief) is not done here; it stays a separate queue item.
