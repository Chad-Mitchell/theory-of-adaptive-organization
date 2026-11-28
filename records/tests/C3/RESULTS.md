# C3 results: shock × √(time to fix) ÷ buffer on 896 PyPI/GitHub projects

Run 2026-11-13 (ET). Prereg: PREREG.md (sha256 23240b5993…, git commit 1a9ad7e, 14:34 ET, before outcome data). Code: code/. Raw numbers: results.json, deviation_results.json, literal_boot.json.

## Plain-words summary for Chad
- **The novel part, the time-to-fix (τ) term, did not show up.** Projects that took longer to close issues in 2021 were not detectably more likely to go dormant in mid-2023 to late 2025 once shock size and buffer were accounted for. The τ coefficient is about zero in every version of the analysis.
- **The predicted interaction (slow fixing hurts most where shocks are big relative to buffers) did not show up either.** Flat, near zero.
- **The buffer part worked, but that's the known part** (Lundmark et al. 2020). Projects with more closing capacity (B) were much less likely to go dormant. Shock size (σ) pointed the right way but was not significant.
- **Formal verdict depends on one coding detail** (see D0 below): under the exact prereg text it is **INCONCLUSIVE**; under the analysis code as written before the outcome pull it is a **MISS** (index form rejected). Either way it is **not a hit**, and the τ term is unsupported here.
- My honest read: a miss for the τ term on this first scale, with real measurement caveats (σ is user demand, not an exogenous shock; τ partly measures issue-tracker habits). Worth saying publicly as a dated result if we post anything.

## D0: one coding discrepancy found after the run (stated up front)
37 repos made their last default-branch commit in the gap (before t0 = 2023-07-01). PREREG.md says an event needs a last commit (or archive) inside [t0, 2025-10-31], so non-archived ones would be **censored** (treated as survivors), although they never committed in the risk period. `analyze.py` (written before outcome data was pulled, but not hashed) instead coded the 30 non-archived ones as **events at t0**. I report both. The prereg text is the authority for the verdict; the code's coding is arguably more faithful to "dormant".

| Version | n | events | β ln σ [95% CI] | β ln B | β ln τ | r_B (theory −1, band −2…−0.5) | r_τ (theory ½, band 0.25…1) | LR test of index, p | P2 interaction [95% CI] | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **L: literal prereg** | 896 | 105 | 0.28 [−0.10, 0.66] | −0.47 [−0.74, −0.19] | 0.001 [−0.09, 0.10] | −1.68 (boot CI −11.5…9.4) | 0.003 (boot CI −1.1…1.2) | 0.017 | −0.008 [−0.021, 0.004] | **INCONCLUSIVE** (no kill fires; hit criteria fail) |
| A: code as run | 896 | 137 | 0.24 [−0.10, 0.57] | −0.57 [−0.82, −0.33] | 0.03 [−0.05, 0.12] | −2.44 (boot CI −16.8…12.9) | 0.13 (boot CI −1.4…2.0) | 0.00015 | 0.001 [−0.014, 0.017] | **MISS** via K2 (LR rejects at p<0.01, ratios outside band) |
| D2: drop the 37 | 859 | 102 | 0.35 [−0.04, 0.74] | −0.55 [−0.84, −0.27] | 0.01 [−0.09, 0.11] | −1.56 | 0.03 | 0.008 | −0.009 [−0.022, 0.005] | would be MISS via K2 (deviation, not decisive) |

Cox coefficients are per unit of natural log; HR per doubling = exp(0.693·β). For τ: HR per doubling ≈ 1.00 (L) to 1.02 (A).

## Pass/fail per preregistered prediction (L = literal prereg; A = code as run)
| Prediction | L | A |
|---|---|---|
| β_σ > 0 (CI excludes 0) | point yes, CI no → not met | not met |
| β_B < 0 (CI excludes 0) | **met** | **met** |
| β_τ > 0 (CI excludes 0) | **not met** (≈0) | **not met** (≈0) |
| r_B in [−2, −0.5] | met (−1.68) | not met (−2.44) |
| r_τ in [0.25, 1] | **not met** (0.003) | **not met** (0.13) |
| Index restriction not rejected at p<0.01 | met (p=0.017, borderline) | **failed** (p=0.00015) |
| P2: absolute-scale interaction > 0 | **not met** (≈0, slightly negative) | **not met** (≈0) |
| Tercile risk differences rise across σ/B terciles | no clear pattern (A: +2.3, +5.2, +0.9 pp; all CIs span 0) | same |
| Shape check: Cox interaction < 0 (labeled not-support) | — | −0.05 [−0.18, 0.08], uninformative |
| Kill K1 (τ absent) | not fired (point 0.001 > 0; ratio CI too wide) | not fired |
| Kill K2 (index fails) | not fired | **fired** |
| Kill K3 (no interaction) | not fired (CI spans 0) | not fired |

Event rates by σ/B tercile (A): 9.0%, 14.8%, 22.1%. No tercile above 50%, so the near-certain flag never triggered.

## Sensitivity (preregistered, non-decisive; on coding A)
- S1 + controls (age, commits, org): β_τ 0.06 [−0.03, 0.15]; B still protective; older repos safer.
- S2 yearly discrete-time logit: same pattern, r_τ = 0.14.
- S3 not_planned closes censored: identical (state_reason rarely present for 2021 closes).
- S4 drop 189 τ-capped repos (n=707): β_τ 0.06 [−0.06, 0.17].
- S5 τ from bug-labeled issues (n=304, 25 events): β_τ 0.01 [−0.18, 0.21]; underpowered.
- S6 proportional hazards: no violation (Schoenfeld p = 0.24–0.50).

## Exploratory (NOT preregistered; labeled)
- τ alone predicts dormancy (β 0.10 [0.02, 0.19]), but that vanishes once σ/B is in the model (0.04 [−0.05, 0.12]). Slow fixers are mostly small, thin-buffered projects (corr ln τ vs ln σ/B = 0.26); τ adds nothing beyond that.
- Magnitude check: if the index form held, β_τ should be about ½·β_σ ≈ 0.12–0.14, or ½·|β_B| ≈ 0.23–0.29. The literal-prereg CI for β_τ (upper 0.10) excludes both, and coding A's (upper 0.12) excludes the B-scaled value. So the data are not just noisy on τ; they fit a smaller τ effect than the model implies.
- Reversal-aware analysis (added after the parent's note on the peak/reversal, before P2 results were seen): τ risk difference by σ/B quintile (A): −0.4, +9.9, +1.6, +1.3, −1.4 pp; the second quintile is the only positive bump, CI −1.1…+20.9 pp. A quadratic interaction LPM finds nothing (p = 0.41–0.53). A hump could be hiding in the noise, but there's no evidence for it.

## Deviations from the prereg (all recorded)
1. **D0 coding discrepancy** (above). Both codings reported; verdict quoted on the prereg text.
2. 3 of 2,500 sampled repos excluded for incomplete issue data (GitHub page-100 pagination limit); prereg did not anticipate it.
3. The issue puller was restarted twice (rate-limit handling, then more threads); finished repos were not re-pulled, and 2 rate-limit-truncated pulls were re-pulled in full.
4. Literal-version bootstrap done in a separate script (literal_boot.py), same seed and resamples.

## Known limitations (some named in the prereg, some flagged afterwards)
- **Flagged by a parallel audit after hashing:** Primary 2's linear interaction runs across the whole σ/B range, and the 50% "near-certain" flag is crude. The toy model's absolute effect peaks around σ/B ≈ 0.21 and reverses near 0.31 (for τ 4→16; both shift with the τ pair), so a linear term can straddle the reversal and dilute the test. The empirical σ/B here is in items/month, not the toy's units, so where the reversal sits in this data is unknown. The quintile look above is the exploratory answer.
- σ is endogenous user demand (SD of monthly non-core issues and PRs), not an exogenous shock. Under Poisson inflow σ ≈ √volume, so σ/B mostly measures size. The exogenous-shock arm (upstream breaking releases) was not run.
- τ (time to close issues) mixes fixing speed with triage culture, stale bots and issues used as a forum.
- Dormancy ≠ death: finished libraries stop committing. Moved repos look dead. Bot commits can keep a dead repo looking alive (spot check ~3%).
- Survivorship: the sample is active in 2021 and alive in mid-2023. Only 105–137 events, so power for an interaction is modest.
- One scale only. The theory's own kill rule needs two scales.

## Bottom line
The C3 bet as posted is that slow fixing multiplies shock damage (√τ). On 896 Python projects, buffers mattered (known) and slow fixing did not add risk once size and buffers were accounted for. Formally INCONCLUSIVE (prereg text) or MISS (code as run). Substantively, the τ term failed its first real-data test, with caveats on how well these proxies measure shock and fix speed. The next honest step is the exogenous-shock arm (adaptation lag to upstream major releases) or a second scale, not re-slicing this data.
