# LEARNSIM PREREG_2: level-class vs member-class mixed-arm test, with the measurement framework's validity gates

Private. Added Sunday 15 Nov 2026 after PREREG.md was locked (commits 820b224 / 41f297c, Stage A c95f3c6) and **before any onset run produced output** (results_es.jsonl was empty when this file was written; an earlier launch died before finishing any job). Requested via Ace from night2/MEASUREMENT/FRAMEWORK.md (test #1). PREREG.md is unchanged and its verdicts stay primary for its own claims; this file adds a separately locked, gated analysis.

## 1. What is added
- **Level class measured on the level alone** (framework §3.4 step 3; `run_levelclass.py`, output LEVEL_CLASS.json): a tracker of the shared driver learns by ES from realized payoffs only, at level-like stakes and drift (R: W ∈ {16, 64, 256, 1024}; A: W ∈ {300, 3e3, 3e4, 3e5}; q ∈ {0.01, 0.04, 0.16}; 8 seeds). Class = OLS elasticities of **learned effort** on ln W and ln q (primary, as the framework defines effort), with realized-cost elasticities as the convergent method.
  - Level R: a = 0.506 (SE 0.013), b = 0.513 (0.019) → −(1−b)/(1−a) = −0.985. Cost-elasticity method: (0.470, 0.476).
  - Level A: a = 0.675 (0.014), b = 0.321 (0.020) → −2.089. Cost method: (0.648, 0.296).
- **Member class** on lone member-range units (Stage A rows, already locked): R effort (0.491, 0.483) → −1.014; A effort (0.680, 0.370) → −1.969. Cost method: R (0.491, 0.489), A (0.657, 0.315).
- **Predictions from measured inputs only** (`prereg2_predict.py` → PREDICTIONS_2.json): measured cost laws φ̂ = e^{c0} W^a q^b (level law from the level-alone runs, member law from Stage A) give N*(ρ) by root-finding; the predicted exponent is the slope over the gated ρ set. **Rival (members' class sets e_g):** the same with the level's law replaced by the member technology's law. No theory constant enters.

| Arm | Gated ρ | e_pred (measured level class, window) | e_rival (members' class, window) | Asymptotes: level / member class |
|---|---|---|---|---|
| AR (A level, R members) | 0.04, 0.08, 0.16, 0.32 | −1.912 | −0.933 | −2.089 / −1.014 |
| RA (R level, A members) | 0.16, 0.32, 0.64, 1.28 | −0.759 | −1.650 | −0.985 / −1.969 |
| RR (known-groups, MV7) | 0.04 … 0.32 | −0.933 | same | −0.985 |
| AA (known-groups, MV7) | 0.16 … 1.28 | −1.650 | same | −2.089 |

## 2. Validity gates applied (framework §2.2), fixed now
- **MV1** triple: target = the shared driver g; pool = the N members whose loss contains g; channel = the tracker's own reads (R) or purchased sample rate (A); nothing else exists in the world. Pass by design.
- **MV2** construct: effort = the tracker's chosen sampling (reads/step, samples/step); drift = increment variance per step; a level = a tracker whose estimate enters all N members' bundled loss. Pass by design.
- **MV3** independent inputs: (a_L, b_L), (a_m, b_m), ρ, q and the cost laws are measured in the same world by procedures that never see D_rel or adoption. Pass.
- **MV4** comparator: flat organisation as comparator; the onset grid must contain N both below and above N̂* (enforced by the crossing-validity rule).
- **MV5** convergent: effort-elasticity and cost-elasticity class estimates must agree within 0.1 on a and on b for each tech and role. Current gaps: level R 0.036/0.037, level A 0.027/0.025, member R 0.000/0.006, member A 0.023/0.055. Pass. (The prediction uses the cost laws; the asymptotes use effort elasticities.)
- **MV6** discriminant: rivals named in advance — members' class sets e_g; fixed group size (e = 0); technology-independent −1.
- **MV7** known-groups: RR and AA must reproduce their own measured-class predictions under this gated rule; if either MISSes, the AR/RA verdicts are reported but flagged "instrument failed known-groups".
- **MV8(i)** power: the bootstrap SE of ê must be ≤ |e_pred − e_rival|/2.8 (AR: ≤ 0.35; RA: ≤ 0.32), else the arm is INCONCLUSIVE whatever the point estimate.
- **MV8(ii)** selection gate (framework §3.10, computed before outcomes): ε̂ = cosh(median |ln-effort residual|) − 1 of Stage A lone members = 1.47% (R members), 3.77% (A members). Prize = b_m·ρ of member tracking cost. Only ρ with b_m ρ > ε̂ are analysed: ρ > 0.030 (R members), ρ > 0.120 (A members). Because only two main-scan ρ pass for A-member arms, **two extra ρ (0.64, 1.28) are run for AA and RA** (`run_onset2.py`, the locked `run_onset.job` unchanged; grid centres in GRID_CENTERS_2.json from theory.py only to place the ×/÷16 grid). Large ρ is far from the asymptote, which is why the predictions use the window slope.
- **MV9** process: sha256 + private-repo commit. Not externally timestamped (that needs Chad's go). Estimator unchanged from PREREG (dry-run on synthetic truth done); analyze2.py smoke-run on the synthetic file only.

## 3. Verdict rules (analyze2.py)
- Gated scan per arm with the PREREG estimator; needs ≥ 3 valid ρ spanning ≥ 0.6 decade, else INCONCLUSIVE.
- PASS if |ê − e_pred| ≤ 0.15|e_pred|; MISS if not and the 95% CI excludes e_pred; else INCONCLUSIVE; overridden to INCONCLUSIVE if MV8(i) fails.
- Members'-class rival killed in an arm if its CI excludes e_rival and |ê − e_rival| > 0.3.
- **T1.8 (level class sets the exponent): PASS only if AR and RA both PASS and the rival is killed in both; MISS if either arm MISSes; otherwise NOT PASSED.**
- Secondary: level of N̂* vs the measured-input N* (Π ratio); asymptotic-class values are reported, not judged (the gated window is not asymptotic).
