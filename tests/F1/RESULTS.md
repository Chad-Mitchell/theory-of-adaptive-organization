# F1 results: shock × √(time to fix) ÷ buffer on US public firms (second scale)

Run 2026-11-14 (ET). Prereg: PREREG.md, sha256 6b9d0f1a…, git d656d6a (22:36 ET), committed before the
outcome file (submissions.zip, downloaded 22:36:35 ET, sha256 in raw/submissions.sha256). Code: code/.
Numbers: results.json (primary + sensitivities), results_E.json (COVID arm), exploratory.json (labelled).
No independent reviewer was available; this needs a blind review before any public use.

## Sample
4,112 firm-cohorts (2,723 unique non-financial, non-utility US filers with ≥4 years of quarterly XBRL).
C1: 2,065 firms, 77 bankruptcies (8-K Item 1.03) in 2015–2019 (3.7%). C2: 2,047 firms, 106 in 2020–2024
(5.2%). Total 183 events. Flow: data/sample_flow.txt.

## Plain words
- **Slow cost adjusters went bankrupt more, robustly.** Doubling τ raised the bankruptcy hazard ~28%
  (β = 0.35 per ln-unit, 95% CI 0.21–0.50), with shock size, buffer and size held fixed. Held in each cohort
  separately (0.37 and 0.34), with industry strata, with leverage + ROA controls (0.29, CI 0.11–0.48), with
  τ from revenue-drop quarters only, and with a cash-only buffer.
- **But that part is not new.** Cost stickiness predicting bankruptcy is published (Ntounis & Vlismas 2024;
  Econ Letters 2024; Homburg et al. 2016). This is a replication with a different τ measure.
- **And it is partly something else (exploratory, after seeing results).** Adding operating margin halves the
  τ effect and its CI crosses zero (0.15, −0.04…0.34); a loss-maker dummy cuts it to 0.17 (0.01…0.34). And the
  signal sits in the immediate non-response of costs (1 − γ, i.e. fixed-cost share / operating leverage), not
  in the correction speed λ (0.12, −0.05…0.29). So "slow error-fixer" here mostly means "costs that don't move
  with revenue at all", which overlaps operating leverage and thin margins — both known.
- **The novel interaction leaned the predicted way but missed significance.** Absolute-scale interaction
  +0.0067 (95% CI −0.0001…+0.0135, p = 0.055). Descriptively it looks exactly like the theory: slow-vs-fast
  bankruptcy-rate gap by σ/B tercile = 0.0, +4.2, +5.6 points (last two CIs exclude 0). 3×3 table below.
- **The exact √τ index form did not fit.** τ's effect is about 1.6× σ's (theory: 0.5×). σ is the weakest of
  the three (β = 0.22) and drops to 0.07 with leverage/ROA controls. Buffer behaved (β = −0.31; r_B = −1.40,
  theory −1). LR test of the index was not rejected at the 0.01 line (p = 0.024). Exploratory likelihoods put
  the best τ weight near 1, not ½ (log-lik −1330.9 at w=1 vs −1333.8 at w=½).
- **The COVID exogenous-shock arm (secondary): same direction, not significant** (interaction +0.019,
  CI −0.006…+0.045, 100 events).

## Verdict under the prereg: **INCONCLUSIVE**
No kill fired; hit criteria failed on two counts (r_τ point estimate 1.61 outside [0.25, 1]; P2 CI includes 0).

| Prediction | Result | Met? |
|---|---|---|
| β_σ > 0, CI excl. 0 | 0.22 [0.09, 0.35] | yes |
| β_B < 0, CI excl. 0 | −0.31 [−0.37, −0.24] | yes |
| β_τ > 0, CI excl. 0 | 0.35 [0.21, 0.50] | yes (not new) |
| r_B in [−2, −0.5] | −1.40 (boot CI −3.72…−0.85) | yes |
| r_τ in [0.25, 1] | 1.61 (boot CI 0.73…4.66) | **no** (point outside; CI overlaps) |
| LR index not rejected at 0.01 | p = 0.024 | yes (borderline) |
| P2 interaction > 0, CI excl. 0 | +0.0067 [−0.0001, +0.0135] | **no** (p = 0.055) |
| K1 (τ absent / too small) | — | not fired |
| K2 (index fails) | — | not fired |
| K3 (interaction ≤ 0) | — | not fired |
Proportional hazards OK (min Schoenfeld p = 0.15). β ln A = 0.07 [−0.06, 0.20].

### Bankruptcy rate (%) by σ/B tercile × τ tercile (pooled, exploratory display)
| | fast τ | mid τ | slow τ |
|---|---|---|---|
| low σ/B | 1.6 (n 371) | 0.7 (432) | 1.8 (568) |
| mid σ/B | 1.1 (465) | 4.5 (467) | 6.2 (438) |
| high σ/B | 5.2 (535) | 7.9 (471) | 12.6 (365) |
The theory's other line ("where shocks are small, slow fixing can still make failures many times more
likely") is not visible: 1.8% vs 1.6%.

## Sensitivities (preregistered, non-decisive) — β_τ [95% CI]
S1 + leverage, ROA (n 2,945, 133 ev): 0.29 [0.11, 0.48]; σ drops to 0.07. S2 τ_drop: 0.31 [0.15, 0.47].
S3 cash-only B: 0.33 [0.19, 0.48]. S4 drop τ at 1 or 20 (n 2,861): 0.44 [0.21, 0.67]. S5 logit: 0.39
[0.23, 0.54]. S6 broad distress D2 (857 events, Item 3.01 non-merger): τ 0.23 [0.15, 0.31], σ ≈ 0, P2
interaction ≈ 0 [−0.008, 0.011]. S7 τ alone: 0.28 [0.14, 0.42]. S8 C1: 0.37 [0.14, 0.60]; C2: 0.34
[0.14, 0.55]. P2 plain spec: +0.0057 [−0.0005, 0.0119].

## Exploratory (NOT preregistered, run after primary results)
Industry strata (cohort × 1-digit SIC): τ 0.33 [0.18, 0.49]. + operating margin: τ 0.15 [−0.04, 0.34].
+ loss dummy: τ 0.17 [0.01, 0.34]. τ decomposed: ln(1 + (1−γ)) 2.15 [1.50, 2.80]; ln λ 0.12 [−0.05, 0.29].
P2 by cohort: C1 +0.0096 [0.000, 0.019]; C2 +0.0041 [−0.006, 0.014].

## Deviations
1. outcome.py: zip opened once per worker (performance; first run was too slow). No logic change; diff in
   git commit 2.
2. Power simulation ignored cohort strata and firm overlap (stated in prereg).
3. COVID arm: 10 firms lacked enough industry peers, 6 dropped for pre-April-2020 events (n 2,031).
None of the decisive code or rules changed after the outcome pull.

## Caveats
- τ measure: split-half reliability 0.14–0.35; 26–28% of firms sit at τ = 1. The predictive part is the
  fixed-cost share (1−γ), not correction speed — construct validity of "time to fix" is weak.
- Margin/loss confound: τ is not cleanly separable from thin margins (exploratory).
- Shock σ is historical revenue volatility in $, not an exogenous shock (the exogenous arm is underpowered).
- Outcomes miss bankruptcies without an 8-K Item 1.03 and out-of-court distress; firms that stop filing
  are censored. Item 3.01 (D2) is a noisy distress proxy.
- 183 events: modest power for the interaction (prereg estimate ~0.5).
- Prior art: the τ main effect replicates published cost-stickiness → bankruptcy results; the novel claims are
  the √τ form (not supported: τ weight ≈ 1, not ½) and the shock/buffer interaction (directionally supported,
  not significant).
- Same-executor analysis; needs an independent blind review.

## Bottom line
Second scale, firms: not a hit, not a kill. The direction is right everywhere (slow adjusters fail more, most
of all where shocks are big relative to buffers) but the only robust piece is already known, it overlaps
operating leverage and thin margins, the √τ weight is wrong (data prefer ~τ¹), and the novel interaction is
p = 0.055. Combined with C3 (open source: τ ≈ 0), the posted prediction has 0 hits and 0 clean kills across two
scales.
