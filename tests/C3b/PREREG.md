# C3b preregistration: adaptation lag to exogenous upstream breaking releases, PyPI/GitHub

Written 2026-11-14 (ET), before any post-shock or outcome data were pulled. Author: Grok Bot (executor for Ace/Chad).
Data touched before writing: (a) the Valiev et al. 2018 frame `package_urls.csv` (package -> GitHub URL, Jan 2018), reused
from C3; (b) PyPI JSON for the five upstream libraries only (release dates and version lists); (c) python.org page for
the 3.12.0 date. No dependent-package data of any kind had been read. A simulation-only power analysis (code/power.py,
output power_output.txt) was run before writing. All analysis and pull code is in code/ and is committed with this file.

## 0. Claim under test and why C3b
Posted wording (X_TEXT v9): "where shocks are large relative to buffers, slow error-fixers fall apart faster than fast
ones, with risk tracking shock size x sqrt(time to fix) / buffer." C3 found no tau effect, but its shock (SD of user
demand) was mostly project size and its tau (time to close issues) mixed fixing with triage. C3b replaces both:
- Shock: an upstream breaking major release the dependent did not choose (exogenous to the dependent).
- Error: the dependent's own last pre-shock release declares a requirement that excludes every final release of the new
  major ("pinned out"). Its users cannot combine its latest release with the new upstream. This is a concrete, dated,
  mechanically detectable incompatibility.
- tau: days from the upstream release to the dependent's first final PyPI release that admits the new major or drops
  the dependency. This is a fix, not triage.

## 1. Shocks (PyPI upload time of the first final X.0 release, verified 2026-11-14)
| lib | R (UTC) |
|---|---|
| SQLAlchemy 2.0.0 | 2023-01-26 22:58 |
| pandas 2.0.0 | 2023-04-03 14:10 |
| urllib3 2.0.0 | 2023-04-26 17:21 |
| pydantic 2.0 | 2023-06-30 16:27 |
| numpy 2.0.0 | 2024-06-16 13:06 |
Secondary Arm W: CPython 3.12.0, 2023-10-02 (distutils removed, C-API changes; compiled packages must ship new wheels).
setuptools is not used as a shock (no single breaking release; the 3.12 distutils removal is covered by Arm W).

## 2. Units, sample, windows
Unit: (GitHub repository, shock). Frame: the 71,903 Valiev packages (fixed Jan 2018, so not selected on later survival),
minus the five upstream libraries.
Windows per shock: pre-shock [R-730d, R) for releases, [R-365d, R) for commits; fix window [R, L], L = R+365d;
alive check (L-180d, L]; outcome window [2025-11-14, pull time] (pull 2026-11-14/15). For numpy, L = 2025-06-16.
Inclusion, Arm P (primary), all decided from pre-shock data except rule 6 (landmark):
1. Package on PyPI; its last final (non-pre, non-yanked) release before R was uploaded in [R-730d, R).
2. That release's `requires_dist` (PyPI per-version JSON) is present and has an unconditional requirement on the lib
   (no `extra` marker; other markers evaluated for CPython 3.11 / Linux). "Pinned out" = the intersection of the applicable
   specifiers admits no final release of the lib's major 2 (all major-2 finals to date). Not pinned out = Arm Q (placebo).
3. GitHub repo resolves today (redirects followed), is not a fork, was created >= 365 d before R, was not archived before R.
4. >= 1 human (non-bot) default-branch commit in [R-365d, R).
5. Exposure measurable: the pre-shock release's sdist (else first wheel) has >= 1 counted .py file.
6. Landmark: alive at L = a final PyPI release or a human default-branch commit in (L-180d, L].
Dedupe: one row per (repo, shock, arm): the package with the latest pre-shock release, ties alphabetical.
Arm P: no cap. Arm Q: simple random sample of <= 2,000 rows; Arm W: <= 2,500 rows (seed 20261114), drawn before any
GitHub call. A repo may appear under several shocks; SEs are clustered by repo.
Arm W inclusion: last final release before 2023-10-02 uploaded in the prior 730 d, ships a `-cp311-` wheel and no `abi3`
wheel; rules 3, 4, 6 as above (no exposure term).

## 3. Measures
Bots: login/name/email containing "[bot]", ending "-bot", in the list in code/common.py, or dependabot/renovate/pre-commit/
github-actions emails. Bot commits never count.
- tau (time to fix), days, clipped to [1, 365]. Arm P: first final release in [R, L] whose requires_dist (known) admits a
  major-2 final or no longer requires the lib. Releases with missing metadata are skipped (counted). None by L ->
  tau = 365, unfixed = 1. Arm W: first upload of any `-cp312-` file (upload <= L; earlier than R -> 1).
- E (shock exposure, Arms P/Q): share of shipped .py files (excluding tests/, test/, testing/, docs/, examples/,
  benchmarks/, .github/, test_*.py, *_test.py, conftest.py, setup.py) that import the lib's module (regex in
  code/exposure.py), smoothed E = (k + 0.5)/(n + 1).
- B (buffer): distinct human commit authors on the default branch in [R-365d, R) (login, else email), from up to 1,000
  commits (cap flagged).
- Controls: lcommits = ln(1 + human commits in [R-365d, R)) (estimated from the fetched share if capped);
  lrel = ln(1 + final releases in [R-730d, R)); lage = ln(repo age at R in days); shock fixed effects.
- latency (specificity control): days from R to the first final release of any kind in [R, L], clipped [1, 365].
- cad_days = 730 / max(1, releases in [R-730d, R)).
- Outcome D (primary, binary): 1 iff (no PyPI file upload and no human default-branch commit in [2025-11-14, pull]) OR
  (repo archived or gone, with no PyPI upload after archivedAt; gone -> after 2025-11-14). Otherwise 0.
- Secondary outcome (user attention): ln(1 + stars gained in [L, L+365d)) - ln(1 + stars gained in [R-365d, R)), repos
  with <= 10,000 stars. Downloads: pypistats.org exposes only the last 180 days and BigQuery is not available, so no
  download-history outcome is used (no pre-shock baseline possible).

## 4. Hypotheses (directions fixed now), all on Arm P with alive_L == 1
- H1 (direct mechanism, relative scale): logit D ~ ln tau + ln E + ln B + lcommits + lrel + lage + shock FE, cluster-robust
  SE by repo. Predict beta_tau > 0.
- H2 (interaction, absolute scale): LPM D ~ c(ln tau) * c(ln E - ln B) + lcommits + lrel + lage + shock FE (c = centred),
  cluster-robust. Predict interaction > 0. Descriptive: risk difference (tau above vs at/below the median) within terciles
  of ln(E/B); predict RD rising across terciles.
- H3 (index form): logit D ~ ln E + ln B + ln tau + shock FE (no controls). Predict beta_E > 0, beta_B < 0, beta_tau > 0,
  r_B = beta_B/beta_E in [-2, -0.5], r_tau = beta_tau/beta_E in [0.25, 1.0] (theory -1 and 1/2). LR test (2 df) of the
  restricted model (single covariate z = ln E - ln B + 0.5 ln tau, plus FE) vs the free model; ratio CIs by repo-cluster
  bootstrap, 1,000 resamples, seed 20261114, percentile 95%.
- S9 specificity: H1 plus ln latency. If tau only proxies general release activity, beta_tau should vanish here.
- Placebo (Arm Q, not pinned out): logit D ~ ln latency + ln E + ln B + controls + FE. Reported for comparison: how much
  of a "slow-release" effect exists without a declared incompatibility.

Smallest effect of interest (SESOI): beta_tau = 0.15 per ln-day on the logit scale (odds ratio 1.11 per doubling of tau).
Rationale: if risk is a monotone function of the index sigma*sqrt(tau)/B with logit elasticity about 0.5 (C3's |beta_B| was
0.47-0.57), beta_tau would be about 0.25; 0.15 is 60% of that.

## 5. Power (simulation, code/power.py, 300 reps; assumed covariate structure incl. a latent activity confounder)
P(H1 95% CI > 0) at beta_tau = 0.25: n=150 0.40, n=300 0.65, n=600 0.92, n=1200 0.99. At beta_tau = 0.15: 0.14, 0.31,
0.60, 0.89. Interaction (0.03 per ln^2 unit, absolute): 0.40, 0.62, 0.89, 0.99. Under beta_tau = 0 with the simulated
confounder, P(H1 CI > 0) = 0.06-0.13 (confounding false positives, hence S9) and P(K1 fires) = 0.06, 0.13, 0.23, 0.44,
i.e. the kill can only fire reliably with a large n. Real n is unknown at writing; it will be recorded in a dated
addendum after the pre-shock screen (stages 1-3, no post-shock data) and before stage 4.

## 6. Verdict rules
Mechanism verdict (primary):
- MISS if K1: H1 beta_tau 95% CI upper bound < 0.15 (rules out a theory-sized effect, includes clearly negative), or
  K2: H2 interaction 95% CI upper bound < 0.
- HIT if H1 beta_tau 95% CI lower bound > 0 AND H2 interaction 95% CI lower bound > 0 AND S9 beta_tau 90% CI lower > 0.
- INCONCLUSIVE otherwise. "Partial" is flagged when H1 and S9 pass but H2 does not (still INCONCLUSIVE).
Index verdict (co-primary, reported separately):
- MISS if K3: r_tau bootstrap CI entirely outside [0.25, 1], or r_B CI entirely outside [-2, -0.5], or H3 beta_tau upper
  < 0.15, or LR rejects at p < 0.01 with a ratio point estimate outside its band.
- HIT if beta_E > 0, beta_B < 0, beta_tau > 0 each with CI excluding 0, both ratio points in band, LR p >= 0.01.
- INCONCLUSIVE otherwise.
If Arm P has fewer than 150 rows after the landmark, both verdicts are reported with the label "underpowered".
The rules are implemented literally in code/analyze.py (tested end-to-end on synthetic data); if text and code
disagree, the text governs and the discrepancy is a deviation.

## 7. Sensitivity (reported, not decisive)
S1 H1 without controls; S2 fixed rows only (unfixed dropped); S3 unfixed indicator instead of ln tau; S4 no landmark
(all rows that pass rules 1-5); S5 per-shock H1; S6 secondary star outcome (H1 and H2 forms, OLS); S7 tau relative to
pre-shock cadence (ln tau - ln cad_days); S8 H1 as LPM. Arm W: H1 without E, and with ln latency.

## 8. Alternatives and confounds (named now)
- Reverse causation / decline already under way: projects losing maintainers both fix slowly and go dormant. Mitigated
  (not removed) by pre-shock buffer and activity controls, the landmark, and S9/placebo. tau is not randomized; a
  positive H1 is consistent with the theory but does not prove fixing causes survival.
- Precautionary pins: many upper bounds are pre-emptive (the code may work with major 2). A pin lift may be a one-line
  change, so tau partly measures release attentiveness. S9 targets this.
- Mechanical link: the fix release itself is release activity and can satisfy alive_L; unfixed rows need other activity.
  The outcome window starts >= 5 months after L for every shock, so the fix release never counts toward D = 0.
- Dormancy != death (finished libraries); moved repos look dead unless they keep releasing on PyPI (counted as alive).
- Survivorship: repos deleted or made unresolvable before the pull are excluded at rule 3; this hides some deaths (bias
  toward fewer events, not toward a tau effect). Counts reported.
- E is a crude exposure: an import count is not the breaking surface; pins may be transitive-driven.
- Shocks differ in severity; shock FE absorb mean differences only.
- One scale only; a hit would be first-scale evidence, not confirmation.
