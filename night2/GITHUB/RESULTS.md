# GITHUB-UPSTREAM — results (as locked, then interpretation)

Sunday 15 November 2026, about 11:30 AM ET (America/New_York). Grok Bot executor for Chad Mitchell (via Ace). Private repo; nothing posted, sent or made public. Read-only public GitHub data.

## 0. Provenance and what was run
- Locks: PREREG + analysis code + seed + bootstrap `71281cf` (08:37 ET); declared post-lock I/O fix to `pull.py` (rate-limit wait only) `69e1ef9` (08:50 ET); ADDENDUM (theory provenance + Regime A/B conditional rule P1-R, `code/addendum.py`) `46f7ad9` (09:27 ET). A second pre-outcome regime gate exists on main: `reviews/night2/GITHUB_ADDENDUM_REGIME.md` (Allan-factor Ĥ, commit `bb7b571`, 09:02 ET), text only, no code. Both are reported (§2).
- Predictions were locked under THEORY.md v1.1 (commit `b13f734`; the addendum cites v1.1 §2.2) and the v1.2 regime gate. THEORY is now v1.4.2; see §4.
- The original worker was interrupted after the pull finished (data pulled 08:37–10:10 ET by `code/pull.py` into Ace's box folder `/workspace/gtao/night2/GITHUB/data/`; no outcome statistic had been computed: no `results_real.json` existed). This executor copied the data unchanged into `data/`, verified that `code/analyze.py`, `code/pull.py`, `code/addendum.py`, `PREREG.md`, `ADDENDUM.md` and `data/search_hits.json` match the sha256 values in `LOCK.txt` / `LOCK_ADDENDUM.txt`, and ran, at nice 19:
  `python code/analyze.py real` → `results_real.json`; `python code/addendum.py` → `results_addendum.json`. No locked code was edited.
- Data: 2,709 workflow files; 1,261 downstream repos; 1,380 eligible workflows' scheduled-run histories (34 returned HTTP 404, i.e. workflow deleted; none failed for rate limits); 505 upstreams (10 missing). `data/runs.json` is committed gzipped (`runs.json.gz`; `gunzip -k data/runs.json.gz` before rerunning); hashes in `data/SHA256SUMS`.
- Post-lock code (clearly separate, `postlock/`): `allan_gate.py` (implements main's text-only Allan-factor gate; written **after** P1/P2 were read; declared choices inside), `descriptives.py` (exploratory, no verdicts).

## 1. As-locked verdicts (PREREG §4–§5)
Sample: 381 units (376 flat, 5 levels). Read rate E is heavily quantized: 81% of flat units sit at exactly 1 or 7 runs/week.

| Prediction | Estimate [95% cluster-bootstrap CI] | Locked rule outcome | Label |
|---|---|---|---|
| P1 drift matching, b ∈ [0.35, 0.65] | b̂ = −0.056 [−0.240, 0.167] (naive −0.049; split-half reliability 0.87) | KILL-CONDITION (CI entirely below the band) | **failed on proxy "weekly CI-state change rate (drift) vs nominal cron reads/week (effort)"** |
| P2 stakes, a ∈ [0.35, 0.65] | â = −0.104 [−0.166, −0.043] | KILL-CONDITION | **failed on proxy "stargazers (stakes) vs nominal cron reads/week"** |
| P3 a = b (class R) | â − b̂ CI [−0.274, 0.138] | CONSISTENT | consistent on the same proxies, but non-discriminating (both ≈ 0, the convention rival's prediction) |
| P5 rank gradient | — | NOT ANALYSED (5 levels < 10) | — |
| P6 vigilance | — | NOT ANALYSED (0 levels with ≥ 3 same-upstream flat comparators) | vigilance stays **OPEN** |
| Secondary b̂ with leave-one-out upstream drift | 0.028 [−0.381, 0.575], n = 170 | convergent only | uninformative (CI covers 0 and ½) |
| ρ (shared/private drift) | 0.103 [−0.029, 0.378] | measurement | — |
| κ (scope slope) | 0.82 [0.50, 1.49], 3 scopes | measurement only | — |

**Gates (§5) and tier.**
- MV5 (drift convergent validity, pass if either ≥ 0.3): Spearman(q_own, q_LOO) = 0.073; Spearman(q_own, upstream commits/week) = 0.041 → **FAIL**.
- MV7(i) pinned-upstream workflows must show lower drift: ratio 1.10 [0.87, 1.41], n_pinned = 97 → **FAIL** (pinned and unpinned workflows flip state equally often, so q is not measuring upstream drift).
- MV7(ii) nominal vs actual recent runs Spearman 0.87 ≥ 0.7 → pass.
- MV8(i) SE(b̂) = 0.104 ≤ 0.18 → pass. MV8(ii) selection gate: prize 0.134 < ε̂ 0.457 → **FAIL** (drift varies too little across units, relative to residual noise in E, for selection to be expected to set E by drift).
- Tier rule: MV7 and MV8 failed, so **P1–P3 are Tier 3, logged only**. They cannot change any claim's status beyond PROXY-FAIL / OPEN.

## 2. Regime-conditional rules (locked before outcomes)
- **ADDENDUM 46f7ad9 (P1-R, geometric vs zeta spell durations).** 641 uncensored spells, mean 4.14 weeks; zeta exponent 1.75; ΔAIC(geom − zeta) = +115.1 → **"Regime B" on this diagnostic**; P1-R band [0.75, 1.25] → **KILL-CONDITION**. Per-unit check (descriptive): 11 of 25 testable units reject a single geometric (KS p < 0.05). Declared confound (in the addendum): a mixture of single-pace units also gives heavy-tailed pooled spells, so the "Regime B" call is weak.
- **Main's Allan-factor gate (bb7b571; implemented post-outcome, see §0).** Ĥ = 0.61 [0.57, 0.66] (median AF 0.67, 0.83, 1.0, 1.0, 1.25 at T = 1, 2, 4, 8, 13 weeks) → **not regime A**; band 1/(1+2Ĥ) ± 0.15 = [0.30, 0.60] → P1 **KILL-CONDITION**, P2 **KILL-CONDITION**.
- All three bands (original, P1-R, Allan) give the same outcome; the verdict does not depend on which regime rule is applied.

## 3. Exploratory descriptives (POST-LOCK; no verdicts; `postlock/descriptives.json`)
Median q = 0.05 state changes/week (the floor of the smoothed estimator for a year with no change); 48% of flat units had **no** state change in 52 weeks; median 1 change per unit; 43% of spells last one week (single-week blips, consistent with flaky tests or transient breakage); Spearman(E, q) = −0.07.

## 4. Interpretation (separate from the verdicts; THEORY.md v1.4.2 on main, `reviews/night2/PRIORART_LFK_ALPHA/REPORT.md`)
1. **Which optimum the test compared against.** P1/P2 encode the reset-read (class R) √ rule, a = b = ½ (THEORY v1.4.2 §2.2 Regime A, A1: EOQ / Reis 2006; KNOWN), i.e. the optimum for exact periodic reads of a drifting target at a per-read price. P1-R's b = 1 came from v1.1 Regime B "adaptation time slope 1", which THEORY v1.4 **withdrew** (CLAIM_MAP K13). The Allan band used the Gaussian (fBm) map 1/(1+2H), with an event-count Ĥ standing in for a Gaussian Hurst exponent.
2. **Is this an event/switching world?** Yes, by construction: the target is a binary weekly state (CI passes/fails), i.e. a two-state switching (telegraph-type) process. The data add that switches are clustered (Allan Ĥ > ½; spell durations heavier-tailed than one geometric), consistent with heterogeneous or rate-modulated switching. It is not a Gaussian world, so the §2.2 Regime B α-map (and the 1/(1+2Ĥ) band) does not apply on its stated premises (v1.4.2 §2.2; PRIORART report §4, proposed premise "Gaussian world or linear tracker").
3. **Does Conti & Mora 2022's ln τ result change the relevant optimum here?** Probably not for this design (DERIVED HERE, elementary, not reviewed). Conti & Mora's ln τ is the Bayes-optimal *adaptation (memory) time* under noisy continuous sensing of a switching mean. This test concerns the *read rate* of *exact* reset reads. For exact reads of a two-state switching target with leaving rate q, the probability of being stale t after a read is ≈ qt for qt ≪ 1, so the average cost c/T + wqT/2 gives T\* = √(2c/(wq)): the same √ rule as Regime A (the Poisson analogue of formal T8; cf. Cho & Garcia-Molina 2003 on freshness). Here qT ≤ 0.05 for nearly all units, deep in that limit. So the locked ½ band was the right optimum for exact reads, **if** CI runs were exact reads of upstream compatibility and q measured upstream drift. The ln τ caveat becomes relevant only if reads are noisy (flaky tests: 43% one-week spells suggest they often are), in which case the comparison should be with a Bayes filter on a noisy switching signal, not with EOQ.
4. **What the failure is about.** The instrument failed: q does not track upstream drift (MV5, MV7(i)), and nearly half the units never changed state. E looks convention-set (81% at weekly or daily crons; E unrelated to q, slightly negative in stars). The data fit the PREREG's rival (b = 0, convention-set crons), but because q failed validation this cannot discriminate between "maintainers ignore drift" and "this q is not drift". Labels stay "failed on proxy"; no field kill.
5. **Version note.** The predictions were locked under THEORY v1.1/v1.2. Under v1.4.2 §2.2 ("Not established": no exponent prediction for a system whose α, q and N have not been measured on that system), this test would not have produced a locked exponent prediction at all without a validated drift measure; it is not a test of CLAIM_MAP N13.

## 5. Proposed THEORY.md edits (not applied; need independent review per the standing rule)
- **§8c (Night 2):** add a GITHUB-UPSTREAM line: "Locked (v1.1-era) a = b = ½ for scheduled CI reads of unpinned upstreams: failed on proxy 'weekly CI-state change rate vs nominal cron rate' (b̂ −0.06 [−0.24, 0.17], â −0.10 [−0.17, −0.04]); Tier 3 (MV5, MV7(i), MV8(ii) failed: q does not track upstream drift); vigilance not analysed (no levels with comparators). No status change." 
- **§2.2 Regime A, with the E2 premise edit from PRIORART-LFK-ALPHA:** distinguish the *read rate of exact reset reads* from the *memory time of noisy sensing*: for exact reads of a switching world the √ read interval still holds when qT ≪ 1 (EOQ/Poisson freshness), whereas the Bayes-optimal memory time under noisy sensing is ∝ ln τ (Conti & Mora 2022). DERIVED HERE; should go to the TELEGRAPH-LINEAR-PREMISE referee before any edit.
- **§2.4 / §11:** a field read-rate test needs a drift measure that passes a pinned-vs-unpinned (or equivalent known-groups) check before any exponent is scored.

## 6. Unresolved
- Two regime gates were locked before outcomes (46f7ad9 on the branch, bb7b571 on main); the branch addendum does not mention main's. Both are reported; they agree.
- The Allan gate's code was written after P1/P2 were seen (text rule locked, implementation choices declared).
- The 5 "levels" are too few for P5/P6; a level-rich frame (e.g. org-wide integration-test repos) would be needed.
