# C3 preregistration: shock × √(time to fix) ÷ buffer, PyPI/GitHub field test

Written 2026-11-13 (ET), before any outcome data was pulled. Author: Grok Bot (executor for Ace/Chad).
Only data touched before writing: the Valiev et al. 2018 sample frame file `package_urls.csv`
(package name → GitHub URL, as of Jan 2018) and a GraphQL schema check. No repo-level activity,
issue, or outcome data has been read.

## 0. Claim under test (posted wording, X_TEXT_v9_final)
"Where shocks are large relative to buffers, slow error-fixers fall apart faster than fast ones, with
risk tracking shock size × √(time to fix) ÷ buffer." Spec follows HYPOTHESES_CORE_v2_reviewed.md C3
(review-fixed version): Primary 1 = index restriction; Primary 2 = interaction on the absolute-risk
scale; a positive Cox interaction is NOT support (the toy model predicts a negative one on the
relative scale). Prior art: σ/B → exit via buffer depletion is known (Lundmark et al. 2020); the bet
here is the τ term.

## 1. Why this dataset
- Public, free, already pulled once in the literature (Valiev, Vasilescu, Herbsleb 2018, FSE), and
  their frame was fixed in Jan 2018, years before our outcome window, so the frame is not selected
  on survival. (Current download rankings would be.)
- GitHub REST/GraphQL via the box's authenticated `gh` CLI (read-only, public data, 5,000 req/h).
- The cleaner exogenous-shock arm (adaptation lag to upstream major releases) is NOT run in this
  pass: detecting "first release that supports upstream vX" needs per-version requirement parsing
  that is noisy (most packages do not pin upper bounds). Recorded as a limitation, not a deviation.

## 2. Units, windows, sample
- Unit: one GitHub repository (deduplicated across packages) from the Valiev frame.
- Measurement window W: 2021-01-01 to 2021-12-31 (τ closures observed until 2022-06-30).
- Gap: 2022-07-01 to 2023-06-30 (12 months, nothing measured except the alive check).
- Risk period: t0 = 2023-07-01 to tend = 2025-10-31 (dormancy needs ≥12 months of silence before
  the Nov 2026 pull).
- Inclusion (all from pre-risk data, except the archive date rule which is mechanical):
  1. repo resolves via API, not a fork, created before 2020-01-01;
  2. ≥ 12 default-branch commits in 2021;
  3. ≥ 1 default-branch commit in 2022-07-01..2023-06-30, and not archived before t0;
  4. ≥ 12 non-PR, non-bot issues opened in 2021;
  5. σ > 0 and B > 0 (defined below).
- If more than 2,500 repos pass rules 1–3, draw a simple random sample of 2,500 with
  numpy seed 20261113 before pulling issues (budget).

## 3. Measures (all from window W)
Bots: user.type == "Bot", login ending in "[bot]", or login in {dependabot, dependabot-preview,
renovate, pre-commit-ci, pyup-bot, greenkeeper, codecov, allcontributors, github-actions, stale,
mergify, imgbot, snyk-bot}. Bot-authored items are dropped from every count.
- σ (shock size): SD (ddof=1) over the 12 months of 2021 of the monthly count of issues + PRs
  opened by non-core accounts (author_association ∈ NONE, CONTRIBUTOR, FIRST_TIMER,
  FIRST_TIME_CONTRIBUTOR, MANNEQUIN). (TEMPERATURE_MEASURE §1.3.)
- B (buffer): mean monthly count, over 2021, of issues + PRs closed (closed_at in 2021), any author
  except bots. Same units as σ (items/month): the team's processing capacity.
- τ (time to fix): Kaplan–Meier median days from open to close of non-PR, non-bot issues opened in
  2021, administratively censored at 2022-06-30. Any close counts as the event (primary). If the KM
  median is not reached, τ = 546 days (cap) and the repo is flagged.
- Outcome (dormancy/exit): event time = earliest of (a) archivedAt, if in [t0, tend]; (b) date of the
  last default-branch commit, if that date is in [t0, tend] (i.e. no commits after it up to the
  pull). Otherwise censored at tend. Duration measured in days from t0. Binary D = event by tend.
- Controls (secondary models only): ln(repo age in days at 2021-01-01), ln(1 + commits 2021),
  owner is an Organization.

## 4. Predictions (direction fixed now)
Primary 1, index restriction (Cox PH, Efron ties, covariates ln σ, ln B, ln τ, no controls):
- β_σ > 0, β_B < 0, β_τ > 0.
- r_B = β_B/β_σ in band [−2, −0.5]; r_τ = β_τ/β_σ in band [0.25, 1.0] (theory: −1 and ½).
- Likelihood-ratio test of the restricted model (single covariate ln σ − ln B + ½ ln τ) against the
  free 3-covariate model (2 df) does not reject at p < 0.01.
- Ratio CIs: nonparametric bootstrap, 1,000 resamples, seed 20261113, percentile 95%.
Primary 2, absolute scale (linear probability model of D, HC1 robust SEs):
- D ~ c(ln τ) + c(ln σ/B) + c(ln τ)·c(ln σ/B) (c = mean-centered). Predict interaction > 0.
- Descriptive: within terciles of σ/B, risk difference in D between τ above vs below the sample
  median τ; predict RD rising across terciles, near zero in the lowest. If a tercile's event rate
  exceeds 50% it is flagged as the near-certain-failure regime (theory: absolute effect shrinks).
Reported, labeled as shape check, not support: Cox interaction ln(σ/B) × ln τ (toy predicts < 0).

## 5. Verdict rules
- MISS (kill) if any of:
  K1 β_τ point estimate ≤ 0, or the bootstrap 95% CI of r_τ lies entirely outside [0.25, 1];
  K2 the bootstrap 95% CI of r_B lies entirely outside [−2, −0.5], or the LR test rejects the
     restriction at p < 0.01 with a ratio point estimate outside its band;
  K3 the Primary 2 interaction 95% CI lies entirely ≤ 0.
- HIT if no K fires AND β_σ > 0, β_B < 0, β_τ > 0 each with 95% CI excluding 0, both ratio point
  estimates in band, LR not rejected at 0.01, AND the Primary 2 interaction > 0 with 95% CI
  excluding 0.
- INCONCLUSIVE otherwise. If β_σ's CI includes 0 the ratios are unstable; then the verdict can be
  MISS (via K1 sign, K2 LR, K3) or INCONCLUSIVE, not HIT.

## 6. Sensitivity analyses (reported, not decisive)
S1 controls added; S2 discrete-time (yearly) logit instead of Cox; S3 τ with "not_planned" closes
treated as censored; S4 drop τ-capped repos; S5 τ from bug-labeled issues only (repos with ≥5);
S6 proportional-hazards check (Schoenfeld) on the primary model.

## 7. Alternatives and confounds (named now)
- Size: σ (≈√volume under Poisson inflow) and B (∝ volume) both scale with project size, so σ/B
  falls with size by construction (Stanley et al. 1996 analogue). Small projects die more for many
  reasons. This can produce β_σ, β_B signs without the mechanism. The τ term is less exposed.
- Collinearity of ln σ and ln B (expected r > 0.8) widens ratio CIs.
- τ reflects tracker habits (stale bots, issue triage culture, issues used as forum), not only fix
  speed. Stale bots make τ short without fixing anything.
- Reverse causation: handled by the 12-month gap (W ends ≥12 months before t0). A decline already
  under way in 2021 is still possible.
- Dormancy ≠ death: finished, stable libraries stop committing; bot-only commits (dependabot,
  pre-commit) keep dead repos "alive"; repos moved off GitHub look dead.
- Survivorship: the sample conditions on being active in 2021 and alive in mid-2023.
- σ here is endogenous demand (users file more issues for popular projects); it is not an
  exogenous shock. The exogenous-shock arm is not run.
- One scale only. The theory's own kill rule needs two scales; a hit here would be first-scale
  evidence, not confirmation.
