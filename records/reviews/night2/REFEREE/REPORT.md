# Blind, hostile, independent referee report: VIGIL_ONA and MEASURE-SELF (night 2)

Referee: an independent referee subagent. Claimed 2026-11-15 08:20 EST. Private working file; nothing posted or sent.
Procedure: I checked lock integrity and reproduced every key number with my own code (`ona_ref.py`, `ona_robust.py`,
`self_ref.py`; outputs `ona_ref_main.json`, `ona_robust.json`, `self_ref.json` in this folder) **before** opening either
`RESULTS.md`. Then I compared my results with the authors' write-ups (§4). Wording follows STATE.md: labels are proxy-aware
("passed/failed on proxy X"), and nothing here is called a "law".

## 0. Bottom line
| Test | Authors' headline | Referee verdict |
|---|---|---|
| VIGIL_ONA H1 (direction: higher rank seeks more outside its unit; RR 1.94) | PASS | **DOWNGRADED.** Correct under the locked fixed-effect rule, but heterogeneity is significant (Q≈10, p≈0.02). A random-effects/HKSJ pool includes 0 (−0.54 to 2.25 log). Manufacturing's effect comes entirely from 4 top managers. Direction is prior art (Mintzberg). |
| VIGIL_ONA H2 (outward tilt beyond status; OR 2.47) | PASS, "survives a status control" | **DOWNGRADED.** Locked rule met (jackknife CI lower bound +0.08, so barely). It is 82% one law firm, and it does not survive seniority/age controls (0.72 ± 0.51). The Lazega advice item measures private-task advice, not sampling of a shared driver. |
| VIGIL_ONA H3 (growth with span; ε = 0.39 "in the 0.3–0.7 band") | PASS | **OVERTURNED as a span test → INCONCLUSIVE.** In Cross & Parker, "pooled N" is a deterministic function of level, so H3 re-tests H1. On the only measured spans (Krackhardt), ε = −0.05 ± 0.19. Without 4 manufacturing managers, ε = 0.06 ± 0.15. The locked instrument band was 0 < ε ≤ 0.7, not 0.3–0.7. |
| VIGIL_ONA overall label | CONSISTENT-GTAO-SPECIFIC (Tier 3); vigilance stays OPEN | **Label follows the locked rules; UPHELD as a rule application. The chat summary "passes all three locked predictions" is DOWNGRADED.** Accurate summary: "direction passed on nomination proxies, Lazega-driven; beyond-status tilt not robust to seniority; no valid span test." Vigilance stays OPEN. |
| SELF P1 (item change is bursty) | PASS | **DOWNGRADED.** It passes the locked homogeneous-Poisson null. But a null that places events at the times Chad actually told Ace anything gives a 95% band of 0.60–0.92 around the observed 0.82. The burstiness is explained by the observer's conversation schedule, not by item drift. |
| SELF P1b | INCONCLUSIVE | **UPHELD.** |
| SELF P2 (attention ∝ √(drift·stakes)) | INCONCLUSIVE; deadline rival wins | **UPHELD, with added problems.** The verdict is seed-sensitive: my bootstrap CI was [0.002, 0.59], which would be PASS. log-drift and log-recency correlate at −0.88, and with recency added the drift elasticity is −0.19. The stakes elasticity of 2.0 (CI 0.6–6.2) **excludes the predicted 0.5**. "Attention VALID" should read "valid log of a rule-coded routine". |
| SELF P3a (drift is a stable item property) | FAIL | **UPHELD in substance, relabel**: "NOT PASS (precondition unmet on statement-time proxy)". The prereg defined only a PASS rule for P3a. |
| SELF P3b (√-allocation beats uniform out of sample) | FAIL | **UPHELD as locked; DOWNGRADED in meaning.** Reproduced G/U = 1.19 [1.00, 1.37], with the CI's lower edge on 1.00 at two budgets. The theorem's premise (stationary, known drift) failed in P3a, so this is a scope failure on a push-only proxy, not a refutation of the read-frequency result. |
| SELF P4a (closed items freeze) | PASS | **DOWNGRADED to "consistent, non-discriminating".** 0/21; exact 95% CI 0–16% spans the locked 15% FAIL line; every rival predicts it. |
| SELF P5 (miss mechanisms; "the policy was right, doing it failed") | exploratory | **DOWNGRADED.** Unblinded, self-coded, and the second coder was written by the same author after reading the texts. It can't support the causal sentence. |

## 1. Lock integrity

### VIGIL_ONA
- **Hashes:** LOCK.txt hashes match the working files and the committed blobs in `52a624a` for FAIR_MEASURE.md, PREREG.md,
  ona_analyze.py and the raw-data manifest. Every raw file matches the manifest (`sha256sum -c`: all OK).
- **Timing (server-side, not self-attested):** GitHub's repository activity log records the `prereg/vigil-ona` branch creation
  at 13:13:03Z (08:13:03 EST) for 52a624a. The real run's output files (`real.err` created 08:13:10.96, `real.out` and
  `results_real.json` 08:13:12) come after that. The results commit ea372ac was pushed at 08:14:22 EST. That ordering is good.
- **Data before lock:** the raw data was downloaded 07:51–07:53, **before** FAIR_MEASURE.md (mtime 07:54:25) and PREREG.md
  (08:12:48). The prereg's §0 discloses this, and what was touched (node attributes, reports-to structure, file heads). I found
  no box-side artifact showing an outcome statistic computed before the lock. The background terminal logs from 07:50–08:13
  show only a catalog scan, power simulations and an edit to the SE-inflation constant (1.2 → 1.3, calibrated on synthetic data).
  **Limit:** the author's interactive tool calls aren't logged on the box, so "no outcome looked at before the lock" is
  self-attested plus consistent with the evidence. It isn't proven. FAIR_MEASURE was never committed on its own before the download.
- **Was the fair-measure spec tailored?** It wasn't tailored to the outcomes, which weren't seen. It was tailored to the *availability*
  of these datasets: the Tier-1/2 thresholds (≥150 people, ≥20 leads, reporting lines) guarantee every public dataset is
  Tier 3, and Tier-3 results "do not change the claim map". So by design **no outcome of this test could hurt the claim**,
  while a pass was reported to Chad as "your hunch held". That asymmetry is a forking path in reporting, not in analysis. Fix:
  pre-state what a Tier-3 *pass* is allowed to be called in chat (e.g. "direction consistent on a weak proxy").
- **Unit/threshold choices** (office×practice, ≥3 and ≥4 cut-offs) were fixed before the outcome. The sensitivity checks below show they matter.

### MEASURE-SELF
- PREREG.md is byte-identical to the committed `4a651d0` blob. GitHub logs the branch creation at 08:15:34 EST.
- **The analysis code was not locked.** `analyze.py` is mtime 08:16:20, after the lock, and `results.json` is 08:16:29. Choices outside
  the prereg text (bootstrap seed, percentile method, the window-repeat parser for the deadline rival) were made after the lock.
  P2's verdict depends on the bootstrap seed (§3), so this matters.
- RESULTS.md says "Run ~8:15–8:45 AM ET", but it was committed at 08:19:01. That's a time in the future at the moment of writing,
  the same class of timestamp inconsistency the night-1 physics review flagged.
- The journal (`journal.jsonl`, mtime 07:16) wasn't modified after the lock. Its data cutoff of 08:00 is before the lock. Good.
- The prereg honestly discloses that P5 was unblinded and that Ace designed both the system and the test.

## 2. VIGIL_ONA: reproduction and re-analysis (own code)

### 2.1 Reproduced (matches the authors to rounding)
- H1 pooled logRR 0.654 (RR **1.92**), per dataset Krackhardt 0.02, Lazega 0.66, consulting 1.16, manufacturing 2.24.
- H2 pooled β 0.905 (OR **2.47**), Lazega 1.10 (two-way SE 0.32), consulting 0.17, manufacturing 0.39, Krackhardt −1.38.
- H3 ε 0.394 (HC1 SE 0.145).

### 2.2 Statistical validity
- **Clustering / SEs:** two-way (ego, alter) cluster SEs on Lazega (0.32) understate the leave-one-node-out jackknife SE (0.49).
  With jackknife SEs the pooled H2 is 0.95, CI [0.08, 1.82]. It still clears 0, but only barely. The prereg's ×1.3 inflation
  (decision CI) was calibrated on a synthetic DGP with no seniority structure, so it is a lower bound on the needed correction.
- **Permutation check (ego rank permuted, status terms kept):** Lazega p < 0.005 (0/200), consulting 0.41, manufacturing 0.41,
  Krackhardt 0.85. Only Lazega carries signal.
- **Identification:** with two ranks (Lazega, Krackhardt), `a_hi` and `a_eq` are collinear given ego and alter FEs. The 1e-6 ridge
  splits them arbitrarily. β is unaffected, but "controls for status matching *and* advice flowing up" is really one identified
  status term in those datasets.
- **Heterogeneity:** H1 Q ≈ 10 on 3 df (p ≈ 0.02). Fixed-effect pooling is not appropriate under that. DerSimonian–Laird
  τ² = 0.36: RE estimate 0.85, CI [0.13, 1.58]. With the Hartung–Knapp correction (k = 4), CI **[−0.54, 2.25]**.
  H2 shows no heterogeneity (τ² = 0), and HKSJ gives a CI of [0.02, 1.91].
- **Power:** pooled power ≈ 0.8 at β = 0.5 is almost entirely Lazega's. Every other dataset has power ≤ 0.5 even at β = 0.69.
- **Multiplicity / forking:** there are 4 primary tests plus about 15 secondary layers and thresholds. The overall label needs H1 and H2,
  which is fine. But the threshold sensitivity is large. Consulting H2 is 0.74 / 0.17 / −0.13 at cut-offs 2 / 3 / 4. Manufacturing is
  0.71 / 0.89 / 0.39 / −0.27 at 2 / 3 / 4 / 5. The sign flips at stricter "frequent" thresholds, which is the opposite of what a
  frequency-of-sampling theory wants.

### 2.3 Confounds
- **Lazega seniority/age (the decisive issue).** corr(partner, years with firm) = 0.76. Partners have a median of 17.5 years and
  associates 3. Dyadic H2 with ego years × outside, ego age × outside and an alter-more-senior indicator gives β = 0.72 ± 0.51
  (ego-clustered). With the status×boundary terms as well, it's 0.56 ± 0.61. Age×outside alone is 0.41 ± 0.22. The authors' post-hoc
  numbers (0.81 ± 0.52, 0.71 ± 0.51) match.
  - **Discriminating check (mine, post-hoc):** *within* partners there is no formal level difference, so GTAO predicts no gradient,
    while seniority predicts one. More-senior partners lean outward 0.38 ± 0.32 per SD. The direction favors seniority, but the
    result is not significant.
  - **Counterpoint, for balance:** the node-level H1 in Lazega *grows* with seniority controls (0.66 → 1.03 ± 0.23 with years,
    1.07 with years and age). So the partner/associate gap in outside-seeking *rate* isn't explained by tenure alone. What
    tenure absorbs is the *beyond-status dyadic tilt* (H2).
- **Work-assignment rival (new).** Lazega partners also *co-work* outside their unit more (cowork layer β = 0.63 ± 0.36). Partners
  staff cross-office and cross-practice cases. Advice following one's caseload across offices is a task-routing mechanism, not
  vigilance over a shared driver.
- **Unit definition:** Lazega β is 1.10 with office×practice, 0.76 with office only and 0.98 with practice only. Lazega himself says the
  firm has "three offices, no departments", so office×practice is not a reporting unit.
- **Manufacturing "outside" is partly inside the lead's pool.** The global department manager's pool spans all sites, so his
  cross-site nominations go to his own pool. Dropping the 4 top managers turns manufacturing H1 from 2.24 ± 0.64 into
  −0.88 ± 1.09. That's a mechanical span-of-responsibility effect, not outward sampling.
- **Krackhardt**, the only dataset with measured reporting units, shows nothing. The outside rate is 0.44 for VPs and 0.47 for managers.

### 2.4 Measurement validity (does a nomination measure vigilance?)
- The Lazega item is "basic professional advice … make sure you are handling a case right". That's advice on the ego's **own case**
  (the private driver u_i), not sampling of the unit's shared environment g. By FAIR_MEASURE §4's own exclusion ("external"
  that is really a counterparty of the private task), the instrument that carries 82% of the weight is questionable.
- The manufacturing item ("provides you with information you use") is closer to *receipt* than *seeking*. FAIR_MEASURE §2.2
  asks for sampling.
- Nominations measure breadth of sources on a fixed roster, not sampling frequency, which the authors also note. The threshold
  sensitivity in §2.2 shows that the "frequent" ties don't carry the effect.
- **Verdict:** these are proxies for "who has cross-boundary work relationships", which is a plausible *correlate* of vigilance.
  They aren't validated measures of effort spent tracking a shared driver. Label: "passed on a cross-boundary-nomination proxy".

### 2.5 H3 specifically
- In consulting and manufacturing, `N` = (# below)/(# at level), which is one number per level. The elasticity is then just a
  re-scaled rank effect (H1). Only 11 dataset×level cells identify it. Cell-clustered SE 0.145, with the same point estimate.
- On the only measured spans (Krackhardt subtree sizes 2, 3, 4, 7 and the CEO's 20, though the CEO isn't an ego), ε = **−0.05 ± 0.19**.
- Without manufacturing levels 1–2 (4 people), ε = 0.06 ± 0.15, so the CI includes 0. The authors' post-hoc analysis agrees.
- The prereg's own H3 expectation for this instrument was 0 < ε ≤ 0.7, and the 0.3–0.7 band applies to *frequency*. Saying "inside
  the predicted 0.3–0.7" (as in the chat summary) compares a binary-breadth slope to a frequency band the prereg said not to use.

## 3. MEASURE-SELF: reproduction and re-analysis (own code, written from the PREREG text)
Reproduced: P1 S = 0.822 (Poisson null 97.5% = 0.76); P1b slope −0.392; P2 drift el. 0.304, stakes el. 2.04, AIC D 60.6 vs G 150.8;
P3a ρ = −0.06 [−0.36, 0.25]; P3b G/U = 1.19 [1.001, 1.37] at 7 days (my analytic T/2 lag vs the authors' 200 random phases agrees
to 1%); P4a 0/21. Counts match: 24 items in P1, 71 in P2, 42 in P3, 1,454 item-days.

- **P1, observer confound (the "item-change-when-told" question).** Change events are statement times, and 17 of 30 calendar
  days carry all 80 daily events. When I place each item's interior events at random among the actual times anything was told
  (keeping the endpoints), the null band is 0.60–0.92 and the observed 0.82 sits inside it. A null that enforces the 60-minute
  merge gap barely moves the locked band (0.44–0.74). Conclusion: P1 measures the burstiness of **Chad's conversations with Ace**,
  not drift of the items. It "passed on a statement-time proxy whose burstiness is explained by the observer schedule."
  Day fixed effects in P1b give a slope of −0.56 ± 0.14 (post-hoc, not counted).
- **P2, deadline rival and identifiability.** The morning-return routine is *coded* to surface windowed items. D wins by roughly 90 AIC points,
  so P2 tests the routine's code, not an adaptive allocation. log-drift and log-recency correlate at −0.88 (both come from
  version timestamps), so drift isn't separately identified: with D and recency, the drift elasticity is −0.19 ± 0.21. The
  overdispersion is 3.1. The drift CI straddles 0 depending on the bootstrap seed (authors [−0.015, 0.60], mine [0.002, 0.59]), so
  the locked verdict flips between INCONCLUSIVE and PASS by chance. The **stakes elasticity's CI excludes 0.5**, so the stakes half of
  the √(drift·stakes) prediction fails on this proxy. The authors reported the number but didn't flag that.
- **P3a/P3b:** reproduced. Period-1 "drift" for many items comes from the Oct 16 09:50 archive import, when 32 versions share one
  timestamp. The counterfactual pull policy can't detect a change that exists only when Chad states it, so a "check" has no
  source to read for push-only items. P3b is therefore a FAIL on an incoherent proxy for most items. Because P3a shows
  non-stationary drift, the premise of the √ result is violated: scope, not refutation.
- **P4a:** a non-discriminating pass. Done/cancelled items in a to-do store are rarely reopened under any theory. n = 21 can't
  separate 5% from 15%.
- **Self-selection:** Ace built Looper from GTAO-derived rules and wrote the test, as disclosed. Any P2 pass would have been circular.

## 4. Comparison with the authors' write-ups (read only after §1–3)
**VIGIL_ONA/RESULTS.md is mostly honest.** It discloses the Lazega dependence, leave-one-out (H2 0.05 without Lazega), the
seniority post-hoc, H3 resting on four managers, and that vigilance stays OPEN. Where it overreaches, and what to fix:
1. "This is the first real-data result in GTAO's direction that survives a status control." It survives *rank-matching* controls,
   not seniority, and only one status term is identified. **Rewrite:** "survives alter-popularity and rank-matching controls; does
   not survive seniority/age controls (Lazega)."
2. Tagging H3 as "PASS (GTAO band 0.3–0.7)". **Rewrite:** "H3 locked rule met, but N is a function of level in 2 of 3 datasets.
   On measured spans ε = −0.05 ± 0.19. Not a span test → INCONCLUSIVE."
3. H1 heterogeneity (p ≈ 0.02) is reported, but the decision still uses fixed-effect pooling. **Add** the RE/HKSJ interval.
4. Missing: the measurement critique of the Lazega item (private-case advice), the cowork/work-assignment rival, the threshold
   sign-flips, and the manufacturing top-4 dependence of **H1** (not only H3).
5. The chat summary to Chad ("your hunch held … passes all three locked predictions … slope inside the predicted 0.3–0.7") is
   stronger than the RESULTS.md text and should be corrected (see §5).

**SELF/RESULTS.md is candid on limitations but over-reads three things:**
1. P1 is listed under "Supported here: the drift is bursty". It should be: "statement times are bursty, and that is explained by the
   conversation schedule (referee null)". The authors' own E1 ("bursts come from conversation, not deadlines") points the same way.
2. P2 "Attention VALID (exact log)". It should be "valid log of a deadline-coded routine; tests the routine's design". Add that the stakes
   elasticity excludes 0.5, and that the verdict is seed-sensitive.
3. P5's "The policy was right; doing it was what failed" and the "≈ 28% fewer documented misses at 90% compliance" target are not
   supported by unblinded single-author coding. Keep them as hypotheses for the instrumented before/after test (their recommendation 6,
   which I endorse).
4. Relabel P3a from FAIL to "NOT PASS (no FAIL rule locked)", and P4a to "consistent, non-discriminating".
5. Fix the "8:15–8:45" run-time line (it was committed at 08:19).

## 5. Per-claim verdicts (for CLAIM_MAP_v2)
| Claim | Verdict | Proxy-aware label |
|---|---|---|
| ONA-H1 direction | **Downgraded** | Direction consistent on cross-boundary nomination proxies (FE pool); not robust to heterogeneity (RE/HKSJ includes 0); prior art. |
| ONA-H2 beyond-status tilt | **Downgraded** | Passed the locked rule on nomination proxies, Lazega-driven (82%); not robust to seniority/age; Lazega item measures own-case advice. |
| ONA-H3 growth with span | **Overturned → inconclusive** | No valid span measure; measured spans (n = 4 VPs) give ε ≈ 0. |
| ONA overall / vigilance status | **Upheld: OPEN** | Tier 3, as locked. |
| SELF-P1 bursty drift | **Downgraded** | Passed vs Poisson on a statement-time proxy; explained by observer schedule. |
| SELF-P1b | **Upheld** | Inconclusive. |
| SELF-P2 √ attention | **Upheld (inconclusive)** + stakes half fails on keyword proxy | Routine is deadline-coded; drift not identified separately from recency. |
| SELF-P3a | **Upheld (relabel)** | Not passed: drift not stable on statement-time proxy. |
| SELF-P3b | **Upheld as locked; downgraded in meaning** | Failed on a counterfactual push-only proxy; premise violated (scope). |
| SELF-P4a | **Downgraded** | Consistent, non-discriminating. |
| SELF-P5 | **Downgraded** | Exploratory hypothesis only. |

## 6. Concrete fixes (ordered by value)
1. **Lock code, not just text.** For SELF and any future test, hash and commit the analysis script *and* the RNG seed and bootstrap
   method before running. Prefer BCa or a fixed 10,000-draw bootstrap so a verdict can't flip with the seed.
2. **Pre-register the chat wording for Tier-3 outcomes** (both pass and fail), so that a pass doesn't get reported more strongly than a fail would.
3. **ONA, next data:** make tenure or seniority a *locked* covariate (ego tenure × outside, alter-more-senior). Use reporting units, not
   offices. Exclude ties inside the lead's own pool from "outside". Use a *shared-environment* item ("who do you go to about changes
   in customers/markets/regulation/other units") separate from a *task* item ("help with your own work"). GTAO predicts the rank
   tilt on the first and not the second, which gives a within-instrument discriminating contrast. Pre-specify a random-effects pool
   with HKSJ. Use a node-permutation (QAP-style) test as the primary inference.
4. **H3:** don't use level-derived N. Require measured subtree sizes with ≥ 20 leads. Until then, drop H3 from the summary.
5. **SELF:** (a) Instrument read logs (what Ace actually reads per judgment) and an outcome log, as the authors propose. (b) Measure
   drift against *source* changes, which have real change times (calendar edits, email threads, Drive revisions), not statement times.
   That's the only way to get a drift measure not confounded with Chad's conversation schedule. (c) Use the session-schedule null
   (this report, `self_ref.py`) as the locked null for any burstiness claim. (d) Test attention on a pull process that isn't
   hard-coded to deadlines, or add D and recency as locked covariates and state the identifiability limit.
6. **Lazega within-partner test** (seniority gradient among same-level partners) is a cheap discriminating test. Pre-register it
   for any partnership dataset with tenure.

## 7. Files
`ona_ref.py` (main reproduction: H1, H2 with two-way and jackknife SE, seniority, permutation), `ona_robust.py` (units, status×boundary,
within-partner, placebo, thresholds, H3), `self_ref.py` (P1 with three nulls, P1b with day FE, P2 with rivals, P3, P4a), and JSON outputs.
