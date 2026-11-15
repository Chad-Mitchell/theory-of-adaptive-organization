# HEADLINE-PREMISE-REVIEW — independent review of PR #37 (THEORY v1.4.4, CLAIM_MAP v2.15)

Executor queue-pick14 (for Ace; Chad t1914, t1916), Sunday 15 Nov 2026, about 2:58–3:35 PM ET (America/New_York). Queue pick 14, **rule slot** (ledger 71 unaided order, 72 rule_rank, 73 pick; 74 rule_change for the scorer bug, see §6; outcome 75). Private repo; nothing posted or sent. GTAO is a theory; no "law". Vigilance stays OPEN.

**Independence.** This executor authored none of `reviews/night2/HEADLINE_PREMISE_SCOPE.md` (pick 10), `HEADLINE_PREMISE_APPLY.md` / PR #37 (pick 13), CLAIM_MAP N16 / `TELEGRAPH_LINEAR_PREMISE` / `TELEGRAPH_REFEREE`, or `V143_INDEPENDENT_REVIEW.md`. Reviewed: the full diff origin/main..q-pick13 at `c76e4fc` (THEORY, CLAIM_MAP, review files), against SCOPE, APPLY, the THEORY §2.2 Regime A premise bullet and Regime B premises column, N16, the V143 review (F2) and `PRIORART_LFK_ALPHA/REPORT.md`.

**Verdict: PASS with three narrow fixes** (R1, R3, R4, applied by this reviewer on q-pick13 before merge, §4), then merged. A fourth finding (R2, the causal kill's inputs and lag) touches the theory's kill conditions and is **proposed only**, for a separate applier and reviewer (new item CAUSAL-KILL-INPUTS), per Chad t1916. No CLAIM_MAP status changes. No headline or core rewrite: §0's bet, J16 sentence and Regime C sentence are unchanged in meaning.

## 1. First-principles check of the premise (is it exact?)

The causal chain (§2.1): change destroys information; re-buying it costs reads/precision/upkeep; selection keeps the cheapest allocation. The tracker class decides which features of the world's law price that cost.

- **Best linear tracker, any world:** its error is a functional of second moments (and the noise density) only, so (α, q, N, stakes, prices) is a complete input list. **Confirmed** — numerics §3(1): at fixed q = N = 1 the linear error moves 2.0% across a 1000× split of q into (λ, μ).
- **Gaussian world:** Bayes = linear, same list. Standard.
- **Bayes tracker, non-Gaussian world:** more of the law can enter. One case derived (two-state switching; N16, refereed): λ and μ enter separately (Bayes error moves 363.8× across the same split). **Confirmed** by an independent route (scipy Bessel, and Monte Carlo of the Wonham filter in log-odds form, §3(3)).
- **What is unaffected in that world:** exact reset reads (two-state is Markov; E[x(t+s)|x(t)] = x(t)e^{−2λs} is linear in the last exact read, so the Bayes and linear predictors coincide; error = OU's) and a kernel regressed on the tracker's own observations (iterated projections). Both stated in PR text. **Confirmed.**
- **Hold-last-value (T1):** its squared error depends on second moments only, so the reset-read exponent holds in any world with those second moments (formal Lemma 1(i); §2.2 Regime B row). The status block keeps it. **Confirmed; T1 is necessary** (without it the clause would have narrowed a PROOF result).

So the clause "for a Gaussian world, or for the best linear tracker in any world (premises per row in §2.2)" is the exact scope of the derivations, with "need not hold / can differ" outside it and the derived case named. It neither claims failure outside the class nor withdraws any confirmed row.

## 2. Tightenings T1–T5 and the escape-hatch audit

| | Judgement |
|---|---|
| T1 hold-last-value kept | **Correct, required.** |
| T2 name only derived exponents | **Text correct; rationale partly wrong.** APPLY §1 says "the precision-effort exponent of a Bayes jump tracker is not derived". N16 (refereed row) gives precision elasticities 1/(θ+η), η/(θ+η), 2(1−η)/(θ+η) (effort ×θ). The status block therefore under-listed what differs, while §0 lists a precision-effort exponent. **Fix R1.** |
| T3 condition on the optimum compared, not on "the system's tracker may not be linear" | **Correct, required.** A clause about the system's tracker is exactly the rescue route ("it missed, so it runs another tracker"); conditioning on the locked optimum is not. |
| T4 default: a prereg naming no optimum is scored against best linear | **Correct.** Every earlier locked test was derived from §2.2's linear rows, so it is scored as derived; no test can be excused by the new clause. A Bayes-locked test needs λ, μ measured on the same system before data; if they cannot be measured, the test must lock the linear optimum. "Exactly one optimum ... scored" applies to N6's optimality claim; tests whose aim is to discriminate tracker classes (e.g. KERNEL-INPUT-DISCRIMINATE) are separate claims and are not blocked. |
| T5 "can enter" | **Correct** (for reset reads in the two-state world the Bayes tracker uses second moments only). |

Escape-hatch audit beyond T1–T5 (causal form): N6's causal kill and §9's causal bullet named only α, q, N, stakes. For a Bayes-locked jump-world test, (a) λ and μ can change at fixed q, moving the Bayes optimum, and a design that stays put would not have counted (a hole, i.e. a hatch); (b) a q change split between λ and μ can leave the Bayes optimum nearly fixed, so §9's "stays put" would mis-fire. Also §9 ("stays put") was weaker than N6 ("does not move in the predicted direction"), and N6's "after its adjustment lag" had no lock in THEORY (V141 review asked that it be a number fixed in each prereg), leaving a "we did not wait long enough" rescue. **Proposal R2** closes all three. It is not applied here: it edits the kill conditions (N6, §9), and the reviewer would be both author and reviewer of it. It is not urgent: no locked test is Bayes-locked, and no causal-form test is locked yet, so neither hole can be used before R2 is reviewed. Until then, any Bayes-locked or causal-form prereg must itself list its inputs (including λ, μ) and fix its lag as a number.

## 3. Reviewer's own numerics (`HEADLINE_PREMISE_REVIEW_checks/review_check.py`, output `.out`; nice 19; routes differ from both earlier check.py files)

1. Fixed q = N = 1, λ = 10⁻⁵…10⁻²: linear error by scipy's CARE solver 0.980–1.000 (spread **1.0202×**); Bayes by scipy Bessel K₀/K₁ 4.351·10⁻⁴…0.1583 (spread **363.8×**). Reproduces SCOPE/APPLY's 2% / 364×.
2. Precision optimum in the Bayes jump world (μ = 1, λ = 10⁻³, θ = 1, minimise w·MSE(N = 1/p) + c·p numerically): d ln p*/d ln w = **0.552** (linear world 2/3); N16's constant-η formula 1/(θ+η) gives 0.542 with local η = 0.844 — first-order in the slowly varying η, adequate; d ln p*/d ln λ = 0.448 vs η/(θ+η) = 0.458; the two sum to 1 as they must. Confirms precision-effort exponents differ (R1).
3. Monte Carlo of the Wonham filter, log-odds SDE dL = (2μ/N)dy + λ(e^{−L} − e^{L})dt (Euler), μ = N = 1:
   - κ = 10⁻²: MSE 0.08990 vs closed form 0.09019 (linear 0.1810); mean zero-crossing time after a switch **1.862 ± 0.006** (33,254 switches) vs (N/2μ²)[ln(2μ²/λN) − γ − 1] = **1.861**.
   - κ = 10⁻³ (dt 0.02): MSE 0.01378 vs 0.01395 (−1.2%, Euler bias at the coarser step; linear 0.0613); t_A **3.063 ± 0.012** vs 3.012 (+0.05, ≈ 4 SE: o(1) and step-size terms; the single-log growth, 1.20 per decade vs 1.15, is confirmed to leading order).
   Verdict on quoted numbers: **confirmed** (single log; separate λ, μ; error closed form).

## 4. Fixes applied on q-pick13 (R1, R3, R4; narrow; second hostile pass §5) and proposal R2 (not applied)

- **R1** status block: "the adaptation-time and error exponents under noisy sensing differ" → "the adaptation-time, error and precision-effort exponents under noisy sensing differ" (source N16; §3(2)).
- **R2 (PROPOSED, NOT APPLIED; CAUSAL-KILL-INPUTS)** §1 N6 causal form: trigger list gains "(or, for a Bayes-locked prereg, the further inputs that optimum needs)"; "after its adjustment lag" gains "(a number fixed in the prereg; `reviews/night2/V141_REVIEW.md`)". §9 causal bullet: "the design quantity stays put while ... change" → "does not move in the direction its locked optimum predicts (§1 N6), after the adjustment lag fixed in its prereg, while the system's measured spectrum, drift level, noise or stakes (or, for a Bayes-locked test, the further inputs of §1 N6) change". Every change widens or sharpens a kill; none narrows one. For linear-locked tests any change in α, q, N or stakes moves the optimum, so "stays put" is a special case of the new wording.
- **R3** status-block heading time: "(15 November 2026, about 10:00 AM ET; premise clause added in v1.4.4, about 3:30 PM ET)".
- **R4** LFK pointer "`PRIORART_LFK_ALPHA/REPORT.md` §4" → ", verdict item 4" (three places; the report has no §4 heading; the cited text is verdict item 4).
- Bookkeeping (applied): THEORY header pointer → CLAIM_MAP v2.16; v1.4.4 changelog records this review; CLAIM_MAP v2.16 note (no status change).

Checked and left as is: §0's added ~95 words (APPLY residual (c)): the lock in §0's parenthesis is the guard against the hatch at the place the bet is stated; keep it. Regime C's Q^{1/β} lacks a Gaussian scope (REGIME-C-GAUSSIAN-PREMISE, open; not this PR's scope). Sources and credits: no citation added or removed; the LFK qualifier repeats V143 F2 and matches `PRIORART_LFK_ALPHA/REPORT.md` verdict item 4 (Conti & Mora's telegraph log vs OU √; LFK's τ_E^{1/2} on a telegraph world is their learner class).

## 5. Second hostile pass (reviewer, on the full post-fix diff origin/main..q-pick13)

1. Weakens a confirmed claim? No: hold-last-value, regression-kernel and reset-read results kept; no status changed. ✔
2. Opens an escape? The PR's text does not; the causal-form holes in §2 pre-date it for linear-locked tests' lag and become relevant only once a Bayes-locked or causal-form test is locked (none is). R2 is queued to close them. ✔
3. New mechanism or parameter? None. ✔
4. Numbers in THEORY: none new. ✔
5. Headline meaning: unchanged; §0 text unchanged by the fixes. ✔
6. Labels: no "law"; vigilance untouched; results untouched. ✔
7. Independence caveat: R1, R3, R4 are this reviewer's own and were second-checked by the same reviewer (recorded as such): R1 completes a list from a refereed row, R3 and R4 are a time stamp and a pointer. R2 was withdrawn from the PR for that reason.

## 6. Side finding: sg_rank.py score bootstrap bug (declared, fixed)

`cmd_score` sorted bootstrap AUCs **before** dropping NaN resamples (2 of 2,000 had no positive or no negative item). Python's `sorted()` on a list with NaN returns a garbled order, so the printed percentiles were wrong: rule AUC 0.679 with "CI 0.727–0.943", outside its own point estimate. Declared as ledger 74 (kind rule_change; no parameter changed) before the one-line fix (drop NaN, then sort). Corrected output at 19 outcomes (6 positive): rule 0.679 [0.375, 0.943]; unaided 0.635 [0.375, 0.875]; uniform 0.276 [0.071, 0.536]. Under the bug the locked Q0 rule would have read **PASS**; corrected, it reads **INCONCLUSIVE** (rule CI includes 0.5; rule ≥ unaided). N9 stays OPEN. No file had quoted the buggy CI.
