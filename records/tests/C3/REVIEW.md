# C3 review: skeptical second pass (NOT independent)

**Read this first.** I had no way to spawn a fresh reviewer. This is a separate adversarial pass by the
same executor that ran the analysis, done after RESULTS.md was written, with independent recomputation
where possible. It is not a blind independent grade, and under the project's own rule it does not count
as one. **Ace should send PREREG.md, code/, data/ and RESULTS.md to a fresh blind reviewer before any
public use.**

## Checks performed (re-derived with separate code, not the analysis scripts)
1. σ, B and τ for 3 random repos, recomputed straight from raw issues.jsonl: σ and B match exactly. τ is a lifelines KM median, not re-derived.
2. Event counts recomputed from raw outcome.jsonl: 105 under the literal prereg rule and 137 under the analysis code's rule. Both match RESULTS.
3. The verdict logic matches PREREG §5. The code's K2 fires on the LR arm only with a ratio outside its band, which is right. LR df = 2 (3 free covariates vs 1 fixed index), also right.
4. Hash: `sha256sum PREREG.md` should still give 23240b59…; git 1a9ad7e predates every outcome file (outcome.jsonl written 16:11 ET).

## Findings
- **F1 (major, already disclosed): the verdict flips on the coding of 32 repos** (30 non-archived with their last commit before t0, plus 2 archived late). The analysis code had an unregistered rule, and the prereg text would treat dormant-before-t0 repos as survivors, which is substantively wrong. RESULTS handles this correctly by quoting the prereg text (INCONCLUSIVE) and showing the code version (MISS). A reviewer should not accept either label alone. What's robust across all three codings: β_τ ≈ 0, no interaction, B protective.
- **F2 (major): construct validity of σ.** σ is the SD of monthly user-filed items. Under Poisson inflow it is ≈ √mean, so ln σ − ln B is mostly a size measure, and σ's weak, non-significant coefficient makes the ratios r_B and r_τ unstable (bootstrap CIs span roughly ±10). The LR rejection in coding A may reflect a bad σ proxy rather than a wrong theory. The test of the index *form* is weak here. The τ null is less exposed to this, because τ's coefficient is directly estimated near zero with a reasonably tight CI.
- **F3 (moderate): τ measurement.** 21% of repos had τ capped at 546 days (KM median not reached), and τ is time-to-close, which mixes fixing with triage habits. Dropping capped repos (S4) leaves β_τ ≈ 0.06 [−0.06, 0.17], still null. Bug-only τ (S5) has 25 events, too few to say anything.
- **F4 (moderate): power.** 105–137 events. The interaction test (P2) has low power, and the CI on the interaction (±0.015 per ln-unit²) cannot exclude modest effects. The τ main effect CI's upper end (0.10–0.12) does exclude the size the index form implies when scaled from β_B. That's a fair exploratory point, but it was not preregistered as a kill.
- **F5 (minor): selection.** The ≥12-issues rule kept 905 of 2,497 repos, skewing toward bigger, issue-heavy projects. The results generalize only to those.
- **F6 (minor): dormancy proxy.** The spot check found about 3% bot-only activity among censored repos. Finished libraries may be coded as events. These errors are probably non-differential in τ, which would bias toward the null, not create one out of nothing. Treat that last point as a hypothesis.
- **F7 (fair process):** the reversal-aware analysis is correctly labeled exploratory, and the 50%-flag and linear-straddle limitation is recorded. No silent re-specification found. The prereg was not edited.

## Reviewer's bottom line
Not a hit. On this operationalization the τ (time-to-fix) term shows no detectable effect, and that holds up across codings and sensitivities. The formal label (INCONCLUSIVE vs MISS) depends on a coding choice and should be reported as "inconclusive by the prereg letter, miss by the more sensible coding." The cleanest next test is the exogenous-shock arm (adaptation lag to upstream breaking releases), which fixes F2 and F3, rather than re-slicing this panel.
