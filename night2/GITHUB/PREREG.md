# GITHUB-UPSTREAM — preregistration (FRAMEWORK.md §7 decisive test #2)

Private working file for Chad Mitchell (via Ace). Nothing public. Read-only GET calls on public GitHub data via the authenticated `gh` CLI; no issues, comments or writes on GitHub. The lock time is the git commit time of this file on branch `prereg/github-upstream` of the private repo Chad-Mitchell/theory-of-adaptive-organization; no time is written by hand inside this file (STATE.md lock rules).

## 0. What was seen before the lock (declared)
- **Pilot** (`code/pilot*.py`, `pilot/`): 4 code-search queries (first page each), 129 workflow files parsed, 12 workflows' scheduled-run histories probed. Used **only** for feasibility: (i) cron values are heavily quantized (of 110 files with crons, ~96 were exactly weekly (1/wk) or daily (7/wk)); (ii) run records go back ~1 year with conclusions and head SHAs; (iii) 47 distinct git upstreams in 129 files. **No relation between read rate and stakes, drift, scope or level status was computed.** The pilot files overlap the main frame.
- **Frame search** (stage 1 of `code/pull.py`) was running while this file was written; it yields repo/path/blob-sha only (no outcome variables).
- **Synthetic dry run** of the locked estimator (`dryrun_synthetic.json`): recovers (a,b) = (.5,.5) → (.55,.62); floor (.5,0) → b .11, CI [−.07,.26]; ceiling (.5,1) → b 1.11; (0,.5) → a .00, b .60. Known small upward bias (~+0.1) of the disattenuated b̂ is declared. Decomposition known-groups dry run: true ρ ≈ 0 / 0.5 / 2 → ρ̂ = −0.002 / 0.33 / 1.52 (declared downward bias ~30%, which makes the vigilance floor slightly *higher*, i.e. harder to pass).

## 1. Measurement triple (MV1)
- **Target x_i**: whether downstream repo i's code passes its own CI when built against the *development HEAD* of a named external upstream U (binary weekly compatibility state).
- **Pool**: all flat downstream repos in the frame whose scheduled workflow installs U from git without a pin.
- **Channel set (named, incomplete)**: scheduled GitHub Actions runs of the workflow that installs U@HEAD. Unobserved channels (humans reading upstream changelogs, issue trackers, push-triggered runs) are **not** counted; this is declared as a partial MV2 failure.

## 2. Frame and eligibility
- Frame: union of REST code-search results for `"git+https://github.com" cron path:.github/workflows` × extension {yml,yaml} × 10 size shards (≤1000 hits each). Forks excluded.
- Tracking workflow: has ≥1 cron line; nominal schedule 1–168 runs/week; installs ≥1 **external** (owner ≠ host owner) upstream via `git+https://github.com/owner/name` with no ref or a branch ref in {main, master, develop, dev, trunk, head, nightly, devel, development}. Workflows whose only external git upstreams are pinned (tag/sha/other ref) form the **pinned known-group**.
- Repo not archived; ≥8 weeks with a completed (success/failure) scheduled run in WINDOW = 2025-11-16..2026-11-14 (52 weeks).
- Unit = repo. **Level** = repo with a tracking workflow that checks out ≥2 other repositories (`actions/checkout` `repository:` values excluding host and upstreams) = one tracker whose result is consumed by ≥2 member codebases. All others are **flat**.

## 3. Quantities
- **E (effort/read rate)** = sum of nominal cron runs/week over the repo's tracking workflows (cap 168). Quantization handled by **interval regression** on ln E with cut points at geometric midpoints of observed distinct values; lowest and highest bins open-ended.
- **q (drift)** = smoothed rate of state changes of the weekly binary state (state = conclusion of the last completed scheduled run in each week; failure=1) over adjacent observed weeks: (k+0.5)/(m+1) per week, from the repo's most-run tracking workflow. Equal sampling (one state per week) for every unit. Measurement error corrected by **split-half (alternating weeks) partial reliability, Spearman–Brown**, dividing the interval-regression coefficient (primary).
- **W (stakes)** = stargazers+1 (primary); forks (convergence only, not independent).
- Controls (MV6): ln(default-branch commits in WINDOW + 1) (generic activity); ln(median scheduled-run wall minutes) (price proxy; for public repos compute is free to maintainers, so the per-read price is mainly attention — declared MV2 weakness for price).
- **ρ** = mean excess (over circular-shift null, shifts 13/26/39 weeks) covariance of weekly **change indicators** |Δx| (centred per unit; signed binary increments desynchronize and cannot show shared change — found in dry run before lock) among flat pairs sharing an upstream with different owners, ÷ (mean increment variance − that covariance).
- **κ** = −slope of ln(variance component) on ln(scope size) across nested scopes {repo (n=1, private), owner (same owner & shared upstream; n = mean frame workflows per owner among owners with ≥2), upstream (different owners sharing an upstream; n = mean frame trackers of the unit's primary upstream), global (different owners, no shared upstream; n = frame total)}; positive components only, ≥3 scopes. Measurement only (GTAO does not predict κ's value); feeds P5.

## 4. Predictions, rules (class R: each run is a reset read of upstream HEAD at a per-run price → a = b = ½)
Inference everywhere: cluster bootstrap (clusters = primary upstream for regressions; repo for decomposition; level for raw V), B = 999 (299 for secondary/adjusted, 199 for decomposition), percentile 95% CI, SEED = 20261115.
- **P1 drift matching (§6.7)**: b̂ (disattenuated elasticity of E on q, flat units). PASS-condition: point in [0.35,0.65] and CI lower > 0. KILL-condition: CI entirely outside [0.35,0.65]. Else INCONCLUSIVE. Rival: b = 0 (convention-set crons).
- **P2 stakes (§3.4)**: â, same band and rules.
- **P3 a = b**: CI of â − b̂ includes 0 → consistent with class R; else class ≠ R.
- **P5 rank gradient (§6.9)**: among levels, slope of ln E on ln(n members) = â − κ̂b̂ ± 0.15. Analysed only if ≥10 levels and ≥4× range in members.
- **P6 vigilance (§6.3)**: V = level's nominal reads/week ÷ flat comparators' (same upstream, ≥3, not the level's members). Primary = adjusted (interval regression on all units with level dummy + ln W, ln q, activity, price); secondary = raw same-upstream ratio. Floor = 1 + (1+ρ̂)^−½. KILL-condition: upper CI / floor < 0.8, or upper CI < 1 with â ≥ b̂. PASS-condition: lower CI / floor ≥ 0.8 and lower CI > 1. Analysed only if ≥10 levels have ≥3 comparators; else NOT ANALYSED.
- Secondary (convergent, not decisive): b̂ with leave-one-out upstream drift (mean q of other flat trackers of the same upstream) in place of own q.

## 5. Gates and tier (FRAMEWORK §2.2; anti-rescue clause binding)
- MV1 named (channel set incomplete, declared). MV2 partial (one automated channel; price ≠ maintainer's price). MV3 inputs measured in-system. MV4 flat comparator for V. MV5: Spearman(q_own, q_LOO) and Spearman(q_own, upstream commits/week) reported; pass if either ≥ 0.3. MV6 activity/price controls. MV7: (i) pinned-upstream workflows must show lower q than unpinned (ratio CI upper < 1); (ii) nominal vs actual recent scheduled runs Spearman ≥ 0.7. MV8: (i) SE(b̂) ≤ 0.18; (ii) selection gate: prize = (k+1/k)/2−1 with k = exp(0.5·SD(ln q)) must exceed ε̂ = (k+1/k)/2−1 with k = exp(0.674·σ̂_residual). MV9: this lock.
- **Tier rule**: because MV2 is at best partial, the ceiling is **Tier 2** (DISFAVORED / supportive), never FIELD-PASS/FAIL. If MV8 (power or selection gate) or MV7 fails, P1–P3 are **Tier 3, logged only**. A Tier-2 failure counts as half of a Tier-1 failure (FRAMEWORK §2.2).
- No post-lock change to code, seed, inference or rules. Any post-lock analysis is labelled EXPLORATORY.
