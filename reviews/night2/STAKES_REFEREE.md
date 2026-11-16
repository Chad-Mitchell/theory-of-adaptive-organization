# STAKES-REFEREE — hostile referee of STAKES-EXOGENOUS (N21), with pick 15's errors-in-variables flag

Queue item STAKES-REFEREE, pick 34 (rule slot; ledger 159 unaided order, 160 rule_rank, 161 claim; outcome entry in the ledger). Referee: executor
queue-pick34, who authored none of STAKES-EXOGENOUS, STAKES-SHIFT-CAISO (pick 15) or their amendments. All numbers below are from this referee's own
code in `reviews/night2/STAKES_REFEREE/` (`ref_n21.py`, `eiv.py`, `extra.py`; outputs `*.out`, `*.json`). Data: the committed N21 hourly panels
(`tests/STAKES_EXOGENOUS/data/panel_{2024,2025}.csv.gz`) plus CAISO OASIS `SLD_FCST` RTM/RTD (CA ISO-TAC) for 2024–2025, re-fetched by this referee
from the public API (48 files, no login; `fetch_rtd.py`; raw not committed). One locked check (R-EIV) was preregistered and locked at `1635e28`
before any RTD file was fetched; everything else is a referee re-derivation or report-only diagnostic.

## Verdict: PASS-WITH-FIXES
The locked rules were applied correctly and N21's verdict, **INCONCLUSIVE on proxy "CAISO DA load-forecast error; cost = error × (FMM − DA hub
price)"**, stands. No CLAIM_MAP status changes (N21 and N22 stay INCONCLUSIVE; N13 OPEN; H8 vigilance OPEN). Eight fixes, mostly to what the
numbers may be read as; F6/F7 settle pick 15's mechanism claim.

## Reproduction
- k_lin 2025 = 7.780 × 10⁻⁴, 2024 = 3.2134 × 10⁻³ (own FE code on the panels; = results.json). Identity k_lin = Σ_g k_g V_g / Σ_g V_g holds to
  1e-16 (the e²-weighted mean of stratum stakes, as PREREG says). 31% (2025) and 19% (2024) of the 288 strata have k_g < 0.
- Amendments verified: `git diff 27bbe72` shows A1 (curl in the fetch) and A2 (subgroup rows w_quad → k_lin) only; primary, winsorized,
  exogeneity and the S1–S4 verdict are identical in `results.json` and `results_lockedcode.json`; only the tercile and quarter rows differ.
- The committed panels were written after the lock (not by locked code) but reproduce the locked primary to all printed digits.

## Fixes
**F1. S3 tests predictability, not exogeneity of the slope.** k_lin is the causal stakes only if the other drivers of the spread are
uncorrelated with e within stratum, E[ν e] = 0 where ν = spread − k e. S3 (incremental R² of e on D−2 errors) checks whether e could have been
forecast at issue time. That is neither necessary nor sufficient for E[ν e] = 0. Weather that surprises load also surprises solar, wind and imports,
which move the spread directly. PREREG declares the estimate reduced form (limit ii), which is honest. But the w in THEORY §2.2's optimum is the cost a
*better load forecast* would save, and that is not the reduced-form slope unless the correlated supply surprises are partialled out. Own re-checks
of S3: adding the D−1 morning mean error (hours 1–9, known before DAM closes) leaves R² at 0.029 (2025) and 0.060 (2024). The D−1 same-hour error,
mostly *not* known at issue, gives an upper bound of 0.20 and 0.22. k on the part of e that the D−1/D−2 errors cannot forecast is 7.19 × 10⁻⁴ and
3.19 × 10⁻³, against 7.78 × 10⁻⁴ and 3.21 × 10⁻³ on all of e: the forecastable part does not drive k. *Fix:* relabel S3 "unpredictable at issue time
(passed)". Read ŵ as "reduced-form cost of a load surprise", not as §2.2's w, until supply surprises are controlled for (new item
STAKES-CAUSAL-CONTROLS).

**F2. Payment versus resource cost (estimand factor ~2).** C = e·(P_RT − P_DA) is what load that bought at the DA forecast pays. With a locally
linear real-time supply response (spread = k e), the redispatch resource cost of an error e is the triangle ½ k e². The other ½ k e² is a transfer to
or from inframarginal suppliers. So the system's stakes per squared error are ≈ ½ k_lin, while a load-serving entity's are k_lin. This cancels in
Δlog w (N6 causal form, pick 15). It does not cancel in any level use (SAME-SYSTEM-AQN compares w against read and upkeep prices). *Fix:* any prereg
that uses N21 or N22 stakes in levels must declare whose loss it is, before the data.

**F3. The price proxy is not the load settlement price, and it carries operator adjustments.** These two facts come from CAISO sources this
referee read. (a) DMM's 2023 Annual Report says real-time imbalance uplift was "caused by load settling on an average real-time price that can differ
significantly from the real-time market prices on which generating resources are settled". So load does not settle on the FMM price alone. (b) DMM's
February 2024 board memo says operators adjust the hour-ahead and 15-minute load forecasts upward ("imbalance conformance"), mostly in the evening net
load ramp. It also says the 15-minute adjustment is much larger than the 5-minute one, and the 15-minute price is much higher than the 5-minute price
in those hours, so "load-serving entities buy this extra load at the higher 15-minute market price and then sell it back at the lower 5-minute market
price". CAISO's Q2 2026 market-performance presentation says real-time conformance averaged about 1,400 MW in peak hours in Jan–Feb 2025 and 50 MW in
Jan–Feb 2026 (pilot). So part of the FMM − DA spread is operator policy that varies by year. That is a candidate cause of the year-to-year stakes
change, unrelated to forecasting. *Fix:* N21/N22 stakes are "on the FMM price"; recompute with the 5-minute RTD price and the published conformance
series (new item STAKES-SETTLEMENT-PRICE). Whether OASIS `SLD_FCST` RTD values include conformance was **not** established here.

**F4. Bootstrap coverage holds for 2025 and is somewhat low for 2024, where the estimate rests on one heat week.** This was simulated with the real
FE residuals, permuted by whole week (keeping the heavy tails and within-week dependence), true k = k̂, and 150 reps × 200 draws. The locked
week-block percentile CI covers 0.97 (2025) and 0.90 (2024). Four-week blocks cover 0.93 and 0.88. Block length barely changes the CI (2025
half-width/ŵ: day 0.66, week 0.70, 2-week 0.69, 4-week 0.69; so S1 fails at every block length). The week jackknife SE agrees with the bootstrap
(2025 3.1 vs 2.9 × 10⁻⁴; 2024 1.16 vs 0.98 × 10⁻³). **2024 is concentrated:** ISO week 2024-30 alone contributes 1.01 × 10⁻³ of 3.21 × 10⁻³
(31%), and the top 1% of hours carry 53% of the numerator Σ ẽs̃. k with the spread winsorized at 1/99% is 1.97 × 10⁻³, and 1.82 × 10⁻³ after
dropping hours above the 99th percentile of |spread|. It stays positive, so S4's sign survives, but its size is fragile. In 2025 the top 1% of hours
carry 20% of the numerator. *Fix:* report S4 as "sign replicated; size driven by one July 2024 week".

**F5. S2 "passed" is uninformative here.** The CI of log(k_large/k_small) spans a factor of about 20 in both years. The synthetic power of 1.0 was
against arm D's severe convexity only. *Fix:* read S2 as "not informative on real data", not as support for the quadratic-loss premise.

**F6. Pick 15's mechanism claim (errors-in-variables from behind-the-meter solar): PASSED on proxy "CAISO night-hour k_lin, ACTUAL vs RTD
reference error"** (locked R-EIV, `PREREG_EIV.md`, lock `1635e28`). The MV10 gate was computed blind before r_night was printed:
σ_n = 0.063, r_all = −0.965, midpoint m = −0.483, SNR 7.7, met. Pooled 2024–2025 (17,466 h; night 6,556 h):
**r_night = ln k_night(e_act) − ln k_night(e_rt) = −0.20 [−0.32, −0.08] > m → PASS.** At night, when there is no BTM solar, about 79% of the
all-hours log gap closes (per year: night −0.17 and −0.25 vs all-hours −0.62 and −1.52). So N21's small k, and its "4×" fall, come mostly from the
ACTUAL series' definition. This is consistent with pick 15 and with the N21 row's pointer. My k on e_rt reproduces pick 15's 5.37 × 10⁻³ and
3.54 × 10⁻³. N21 Interpretation 2 ("stakes moved about 4×") should be read as withdrawn. On N21's own error the own-code Δlog k is −1.42
[−2.91, −0.40], but that is the contaminated error.

**F7. The mechanism is non-classical, and a small non-BTM wedge remains** (report-only, post hoc). If the part of e_act not explained by e_rt
were uncorrelated with the spread (classical errors-in-variables), k_act/k_rt would equal the reliability λ = Cov(e_act, e_rt)/Var(e_act). It does at
night (0.82 vs λ 0.70) but not in the daytime, hours 10–16 (0.15 vs λ 0.42). The daytime wedge co-moves with something that lowers the spread. The
natural candidate is an unexpected solar output (more BTM *and* more utility solar → lower real-time prices), so attenuation is stronger than
classical. The night residual, −0.20 with a CI excluding 0 and a wedge sd of 294 MW, is a second, non-BTM definition difference that is not
identified here. By band, k_rt is ×10⁻³ 6.6/4.2/3.9/8.2 (2024) and 4.2/2.9/3.6/3.2 (2025) for night/morning/midday/evening ramp. It is largest in
the 2024 evening ramp, where F3's conformance acts.

**F8. A linear bias × premium cost sits outside k_lin** (report-only, post hoc; weak surprise). On the like-for-like error the DA forecast averages
0.89 GW (2024) and 0.90 GW (2025) *above* RTD. The mean of e_rt·spread, $3,393/h (2024) and $2,372/h (2025), splits into a between-strata
bias × premium term of $1,100/h and $1,102/h and a within-strata k·Var term of $2,293/h and $1,269/h. So 32% and 46% of the mean error cost is
linear in a systematic offset, not quadratic in a surprise. The quadratic premise (THEORY §2.1) covers only the within-stratum part. Whether the
0.9 GW offset is a definition gap (cf. F3 conformance) or a real DA bias is open (new item STAKES-BIAS-TERM).

## Not checked / owed
- Within-stratum effort selection: forecasters may try harder on days they expect to be tight. If so, the e²-weighting under-weights high-stakes days
  and k_lin is biased low. Not testable with these data.
- Supply-surprise controls (F1), RTD prices and conformance (F3), and the night wedge (F7).
- No referee of `validate_synth.py` beyond reading it. Its arms omit F1's correlated supply surprise and F7's correlated wedge, the two failure modes
  found here.

## Questions for a separate reviewer
1. Is the blind gate legitimate when r_all is a data quantity (the rival's prediction is measured, not derived)? I used it because pick 15 had
   published r_all's sign and rough size before this lock.
2. Does F2's ½ hold with CAISO's real-time supply curve? It is exact only for a locally linear response.
3. Night = OPR_HR 1–5 and 21–24: in June hour-ending 21 has twilight, and BTM output is small but not zero. Dropping HE21 should be checked.

## Sources read for F3 (read this session; quoted passages above)
- CAISO Department of Market Monitoring, *2023 Annual Report on Market Issues and Performance* (caiso.com/documents/2023-annual-report-on-market-issues-and-performance.pdf), load forecast adjustments and real-time imbalance offset sections.
- CAISO DMM, *Department of Market Monitoring update* board memo, Feb 2024 (caiso.com/documents/departmentofmarketmonitoringupdate-feb2024.pdf), "Real-time market load adjustment".
- CAISO, *Market Performance and Planning Forum* presentation, 27 Apr 2026 (caiso.com/documents/presentation-market-performance-planning-forum-q2-apr-27-2026.pdf), "Load conformance – Summary".
(Full PDFs downloaded with curl and converted with pdftotext on 15 Nov 2026 ~7:10 PM ET; each quoted passage checked in the text: annual report lines ~981 and ~1816–1827 of the text dump, memo p. ~4 "Real-time market load adjustment", presentation "Load conformance – Summary". Not committed.)
