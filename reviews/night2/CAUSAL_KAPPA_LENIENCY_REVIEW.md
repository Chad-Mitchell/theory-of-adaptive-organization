# CAUSAL-KAPPA-LENIENCY-REVIEW — independent review of PR #74 (THEORY v1.4.17, pick 38)

**When:** 15 Nov 2026, about 8:16–8:19 PM ET (America/New_York). **By:** independent reviewer executor (for Ace, Chad t1914/t1916).
**Exposure:** authored none of pick 38, `CAUSAL_KAPPA_LENIENCY*`, PR #74, N6's kill text, CAUSAL-KILL-MAGNITUDE(-REVIEW) or
LAB-AKLMT-TAU. Out-of-cycle, unscored (ledger 186). Own code: `CAUSAL_KAPPA_LENIENCY_REVIEW_checks/mc_review.py` (imports
nothing from the repo or the author; seed 74074; output `mc_review_out.txt`; run at nice 19).

**Verdict: PASS-WITH-FIXES.** Merged by hand onto v1.4.16 (PR #73, same N6 cell, header and changelog) as THEORY v1.4.17 /
CLAIM_MAP v2.37 with the fixes in §4. No locked label, kill rule, κ_F range or CLAIM_MAP status changes.

## 1. Causal first-principles read
N6's kill says the design's true share r of the scaled predicted move is at least κ_F (κ_F is the tolerated overstatement of
the prediction, CAUSAL-KILL-MAGNITUDE-REVIEW). A verdict "passed" should mean the evidence establishes the same claim the kill
tests, r > κ_F. The locked rule (FAIL iff D + zσ < κ_F·P, PASS iff D − zσ > 0, FAIL takes precedence; read in
`tests/LAB_AKLMT_TAU/PREREG.md` line 39) establishes only r > 0, so "passed" and "not failed" test different hypotheses. The
mirror is the one-sided bound test against the same κ_F the kill uses. Confirmed, and one extra defect the author did not
state: under the locked rule the PASS and FAIL regions **overlap** whenever κ_F·SNR > 2z (SNR > 7.8 at κ_F = ½), so
precedence, not evidence, decides the label in those draws (own MC: both conditions true in 14% of draws at r = 0.40, SNR 9.7;
52% at SNR 20; 99.7% at r = 0.25, SNR 20). Under the mirror the regions are disjoint by construction.

## 2. Own Monte Carlo (K = 30 contrasts, OLS through origin, t residual σ, s = 0.63, 40,000 reps per cell, z = 1.96, κ_F = ½)
| true share r | SNR | FAIL | locked PASS | mirror PASS | analytic mirror PASS / FAIL |
|---|---|---|---|---|---|
| 1 | 5.6 / 9.7 / 20 | 0 | 1.00 | 0.797, 0.997, 1.000 | 0.800, 0.998, 1.000 / 0 |
| 0.63 | 5.6 / 9.7 / 20 | ≤ 0.005 | 0.94–1.00 | 0.117, 0.254, 0.739 | 0.109, 0.242, 0.739 |
| 0.53 | 5.6 / 9.7 / 20 | 0.020, 0.015, 0.007 | 0.84, 0.99, 0.99 | 0.042, 0.055, 0.095 | |
| 0.50 | all | 0.029–0.030 | 0.80–0.97 | 0.029–0.030 | 0.025 / 0.025 |
| 0.40 | 5.6 / 9.7 / 20 | 0.088, 0.172, 0.522 | 0.617, 0.827, 0.478 | 0.008, 0.002, 0.000 | |
| 0 | 5.6 / 9.7 / 20 | 0.798, 0.997, 1.000 | ≤ 0.03 | 0 | |

Averaged over designs truly below the kill line (r uniform on (0, ½)): wrong-pass 0.34 / 0.40 / 0.20 (locked) vs 0.004 /
0.002 / 0.001 (mirror) at SNR 5.6 / 9.7 / 20; false kill over r uniform on [½, 1]: 0.004 / 0.002 / 0.001, identical under both
rules (FAIL is untouched). The author's table (§3 of `CAUSAL_KAPPA_LENIENCY.md`) reproduces within MC and t-vs-normal slack.
**Fix 1:** "≤ 1%" holds at r = 0.40; as r → κ_F the mirror PASS rate rises to its one-sided size Φ(−z) = 2.5% (MC 0.029–0.030
at r = 0.50 with t-noise). Wording changed in the changelog.

**Minimal power gate.** Known scaled prediction: P(mirror PASS | r = 1) = Φ((1 − κ)SNR − z) ≥ Φ(κ·SNR − z) = P(FAIL | r = 0)
for κ ≤ ½, so the FAIL leg binds and MV10's minimal gate is unchanged (κ = ½ at SNR 5.60: 0.797 vs 0.796; κ = ¼ at SNR 11.21:
1.000 vs 0.798). Confirmed. **Fix 2:** with s·λ estimated (own plug-in, log-sd 0.3, error propagated in linear scale by the
delta method) the PASS leg can bind: P(PASS | r = 1) 0.54 / 0.70 / 0.76 vs P(FAIL | r = 0) 0.60 / 0.88 / 1.00 at SNR 5.6 / 9.7
/ 20 (the plug-in error does not shrink with n, and a high draw of P̂ raises both the PASS bar and its σ). The author's own
plug-in row (R1 PASS 0.70 at SNR 5.6) also sits below π = 0.8. Exact numbers depend on how the error is propagated; the claim
is therefore scoped to a known scaled prediction, and MV10 now says the simulation route checks both legs.

## 3. Rejected alternatives
- **κ_F tied to s·λ / κ_F = 1 with propagated error.** s·λ is already in P; tying κ_F to it double-counts. κ_F = 1 is a size
  test that kills designs inside the tolerated band: own MC at r = 0.63 kills 0.548 / 0.945 / 1.000 with s·λ known (author's
  55–100% reproduced) and 0.11 / 0.09 / 0.08 at plug-in log-sd 0.3 (the author's "with propagated error" attached to 55–100% was
  the known-s·λ case; changelog corrected); at r = 1 it falsely kills 3%. Rejection stands: it reverses the κ_F ≤ ½ ruling.
- **Level match as an AND condition.** Own MC: a 3-SE proxy level offset at r = 1, SNR 9.7 drops PASS 0.997 → 0.152 (author
  0.15). The contrast differences out fixed proxy offsets; the level has its own verdict (optimality form, named rival).
  Rejection stands; report-only level line kept.

## 4. Author's questions and scope
- **Q1 — yes.** A passed result whose share interval lies wholly below 1 carries "below the locked optimum's move" in its
  label, not only in the report: "passed" otherwise reads as "matches the optimum", which is exactly the over-reading this edit
  removes. Added to the N6 sentence.
- **Q2 — report line yes, kill no (queued).** The share line now reads "below" or "above the locked optimum's move" when its
  interval excludes 1. Whether an established share above 1/κ_F (the mirror image of the tolerated band) should be a kill is a
  kill-rule question the theory has not argued; queued as **CAUSAL-OVER-RESPONSE**, not added here.
- **Q3 — non-retroactivity is right.** Locked rules govern locked tests in both directions; relabelling N23 after its data
  would be a goalpost move even though it is the conservative direction. The author put this only in the changelog; it is now
  stated in the N6 cell ("binds preregs locked after v1.4.17; no earlier locked verdict is relabelled"), as v1.4.16 does.
  N23's re-reading stays report-only in the v2.37 note. Re-reading arithmetic checked from the locked numbers
  (`tests/LAB_AKLMT_TAU/RESULTS.md` lines 9, 30; `reviews/night2/CAUSAL_NULL_INVARIANCE.md` line 71): 0.518 − 1.96·0.048 =
  0.424 < 0.4918; 0.629 − 1.96·0.094 = 0.445 < 0.514; 0.290 − 1.96·0.029 = 0.233 > 0.175.
- **Scope.** The N6 wording stays causal-form only: N6 governs that form, and the HIT/MISS-floor and relative-band point rules
  (`PASS_RULE_SYMMETRY_AUDIT.md` §3.2–3.3) live in preregs and FRAMEWORK. The changelog points to them; they are already
  queued as HIT-ZERO-MISS-FLOOR and RELATIVE-BAND-TOST. Siblings not edited.

## 5. Goalposts
The merge touches only THEORY.md (header, N6 pass-side sentence, changelog), FRAMEWORK MV10 (one clause) and a CLAIM_MAP note.
No file under `tests/` or `prereg/` changes; no locked label, kill text, κ_F range or status changes. Vigilance (H8) OPEN.

## 6. Limits
Gaussian contrasts, one K, one plug-in model for s·λ; the plug-in result depends on the propagation scale. No field data.
Prior art: none read by this reviewer beyond the author's citation, which was not re-checked here.
