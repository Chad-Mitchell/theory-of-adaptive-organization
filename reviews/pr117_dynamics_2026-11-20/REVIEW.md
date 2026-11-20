# Independent hostile review: PR #117 (head b9fb105), theory/DYNAMICS.md v2.9

Reviewer: separate executor, did not write the PR. 20 Nov 2026, about 3:15 PM ET. Fresh clone, nice 19.
Nothing pushed, commented or merged.

## Verdict: READY-WITH-FIXES (2 blocking fixes, both in the text, must be fixed and re-confirmed before merge)

Reproduced: `tools/check_consistency.py` RESULT: PASS (0 FAIL, 21 INFO); `pytest tools/` 103 passed (9 min);
d1–d4 rerun byte-identically (git status clean after the run). Tally: +8 rows (OPEN 78→80, PROVED 84→87,
PRIOR ART 28→31, total 297→305), which is correct. No locked prereg file is touched. The only edits under `theory/measured/` are
append-only DEVIATIONS entries (ecoli +12/−0, grid +1/−0), dated with a time and branch. "Law" shows up only as "law of large
numbers". There is no "bill" and no joules. Labels: CL19–21 PRIOR ART, CT41–43 PROVED (in-model), CX9–10 OPEN. These fit, except as noted below.
Crossref: I spot-checked 6 DOIs myself (Dixit 1991 JEDC, Kalman 1964, Frankel 2014, Caballero–Engel 1999, Kussell et al. 2005
Genetics, Altman 2021), and all resolve to the named works. The PR's own crossref.out lists all 33 as OK.

## Blockers

**B1. CT41 is false as stated when an upper bound k̄ is used, and the kill-rule amendment inherits the error in the lenient direction.**
`theory/DYNAMICS.md:56-61`, `THEORY.md:53`, `measurement/FRAMEWORK.md:709`, `CLAIM_MAP_v2.md:519`, `README.md:29`.
CT41 says "it is optimal not to move whenever |Δ| < Δ_R(k̄)", with k̄ a preregistered *upper bound*. If the true k < k̄,
moving is optimal for Δ_R(k) < |Δ| < Δ_R(k̄). So the claim holds only for a *lower* bound (or a point estimate) of k.
Using an upper bound widens the excuse band in exactly the direction that rescues the hypothesis. That is the post-hoc-rescue
leak the amendment is meant to close.
Fix: excuse a non-move only when |gap| < Δ_R(k_lower), with k_lower taken from the preregistered measured k and its error budget.
A gap between Δ_R(k_lower) and Δ_R(k_upper) is indeterminate, not consistent. In the same sentence (THEORY §3, FRAMEWORK §9.5),
also require preregistration of w (the curvature), the input-process type (step lasting T, or drift with σ_d), and T or σ_d.
The drift band (∝k^{1/4}) is much wider than the step band (∝k^{1/2}) for small k, so choosing between them after the data is
a second rescue lever. DV-DYN1 (grid) already asks for the process type, but the canonical rule does not.
Also add: if Δ_R ≥ the predicted move, the move test has no power (item (d)), so it is NOT A TEST, not a pass.

**B2. The Bode verdict's "S never exceeds 1 … no waterbed" holds only for continuous observation. It is false for sampled or
periodic reads, which are in the theory's own class.** `theory/DYNAMICS.md:194-200`.
For the steady-state discrete-time Kalman predictor, the innovation map is S(z) = (z−a)/(z−a+K). There, ∫ ln|S| dω = 0 exactly,
and |S| > 1 near Nyquist. In 4 scalar AR(1) worlds, max|S| was 1.045–1.436 (`REVIEW_bode_dt.py`). Equivalently,
|S|² = (CPC′+R)/Φ_y(ω), which exceeds 1 where the signal spectrum falls below CPC′. In continuous time, |S|² = N/Φ_y ≤ 1,
so the PR's check is right for Kalman–Bucy only. THEORY prices reads per read and has read rates and read intervals
(THEORY.md:32, :87, :336, :424 "read exactly at price c"), so periodic reads are part of the present class.
Fix: restate as "OVERREACH for continuous observation (Kalman–Bucy, |S| ≤ 1). For periodic or sampled reads the predictor
satisfies a waterbed identity (∫ ln|S| = 0, |S| > 1 at high frequency), and whether that changes argmin J is OPEN."
Cite a discrete-time Bode or Sung–Hara-type result (verify the DOI first). The verdict may well survive, because |S| here is
observation-to-innovation, not a cost J pays. But the reason given ("no band where |S| > 1") does not survive.

## Should-fix

1. `DYNAMICS.md:58-61` (CT41): state the test on the post-change **gap** |x₀+Δ|, not on Δ. A design already inside the static
   band (x₀ ≠ 0) changes what a given Δ implies, and the drift band is a band on the gap anyway.
2. `DYNAMICS.md:173-174` (CT43 (iv)): "only for lumpy X; for X = 0.05 the counts coincide" is false on the PR's own grid.
   With d3's `nE_nG` over the same 600 points, the share that differs is 8% at X=0.05, 4% at 0.1, 13% at 0.2, 16% at 0.4,
   17% at 0.6 and 32% at 0.8. D3c checks X=0.05 at only three points. Say "rises with X" instead.
3. `DYNAMICS.md:128`: "differs from per-unit argmin J exactly through the shared component of variance" holds only in the
   large-population limit. For finite N, within-generation variance from independent shocks also matters, at order 1/N
   (Gillespie 1974, which the PR itself cites at :101). Add "for a large population".
4. `DYNAMICS.md:106-108` and CX10: Frankel 2014 "a proposal, untested" is too strong. Waite et al. 2016, Mol Syst Biol,
   doi 10.15252/msb.20167044 (Crossref OK; erratum 10.15252/msb.20178149) experimentally tested how chemotaxis diversity
   changes population performance. Selection on it is still untested, so say that.
5. `DYNAMICS.md:42` and `CLAIM_MAP_v2.md:518`: the fourth-root analytical approximation is Dixit's *Review of Economic Studies*
   1991 paper (doi 10.2307/2298051, Crossref OK). The cited doi 10.1016/0165-1889(91)90037-2 is the JEDC "simplified
   treatment". Cite both. Chalkley 1997, Economics Letters, doi 10.1016/s0165-1765(97)00222-x, reports that Dixit's
   quadratic-loss approximation is exact with zero discounting, which supports the undiscounted renewal derivation.
   I could not read either paper's text, so the coefficient 6 is confirmed only by my own derivation, below.
6. `DYNAMICS.md:161`: the log-reserve form W′=W·exp(−(c+wℓ)) assumes every cost, including upkeep hK, scales with the reserve.
   Say so, since that is what makes "−J exactly" true.
7. `DYNAMICS.md:166-168` (CT43 (iii)): zero drift also gives ruin → 1 (recurrence), so the constraint excludes non-positive
   growth, not just negative. Minor.
8. `DYNAMICS.md:77-78` (CX9): the reported w_up and w_down depend on the stake's volatility (0.01 sd of d ln w per period) and on
   the grid. State these. The no-cost w_down of 0.991 is one grid step from w_c, which is fine.
9. Versioning: THEORY stays "v2.4 draft", DYNAMICS and CHANGELOG say "v2.9", and CLAIM_MAP says v2.66, which collides with
   PR #115's v2.66. The PR admits the collision (`CLAIM_MAP_v2.md:77`). Whichever PR merges second must renumber the note and
   tally. Given Chad's "clusterfuck" concern, one version line would help.
10. `README.md:29`: the short form drops "only where adjustment is lumpy", and after B1 it should say "lower bound / point
    estimate". Keep all four statements (THEORY §3, §8 if separate, FRAMEWORK §9.5, README) word-consistent.

## Checks that pass (my own derivations)

- **Dixit band.** Gap is Brownian (σ²) and resets at |x|=b. E τ = b²/σ². With (σ²/2)f″ = −w x² and f(±b)=0,
  f(0) = w b⁴/(6σ²). Rate = kσ²/b² + wb²/6, so b\* = (6kσ²/w)^{1/4} and the minimum is 2√(kwσ²/6). This is correct, undiscounted,
  for loss w·x² with w = H/2. 100^{1/4} = 3.16 is right. MC gives 0.0813 ± 0.0006 against 0.0816; the small low bias is the
  usual discrete-exit effect.
- **Step threshold.** wΔ²T > k gives √(k/(wT)); discounted, √(kr/w). Correct. Convex cost gives T_red = √(κ/w) from κx″ = wx.
  Correct; numeric 2.01 against 2.00.
- **Hysteresis.** w_c = h(K+1)(K+2)/G₀ = 1. Value iteration gives 1.107 and 0.895, reproduced.
- **Bet-hedging.** The FOC gives βa₁ = q(a₁−b₁), so q\* = βa₁/(a₁−b₁) = 0.26 (independent of b₀ > 0). G(q\*) = 0.1279,
  pure robust 0.0411, per-unit means 1.235 and 1.0425. All verified by hand. The ρ-sweep model (shared with prob. ρ, otherwise
  independent, same marginal) is coded correctly. Framing of Cohen, Kussell & Leibler, Kussell et al. and Balaban is honest
  ("model-based reading, not a selection experiment"), apart from should-fix 4.
- **Time average.** The counterexample is verified: A has arithmetic mean 1.030 and geometric 0.0295; B has 1.031 and 0.0258;
  both pass P(min W < 0.3 by T=300) ≤ 0.01 (B at 0.00125, about 5 hits in 4000, small but under ε). The "bug fix" (the scan
  clipped a log that is undefined for Gaussian loss) is correct, and so is CT43 (ii).
- **Barbell.** At B = 0.49–0.505 the frontier equals its convex hull. The discrete mix of 6.555 copies needs ε to be ex ante
  (P(6) = 1.0×10⁻³ > ε = 5×10⁻⁴). Calling it LP or constrained-MDP randomization rather than a barbell is right. Coverage is
  only three B values just above B_min = 0.486, so say so.
- **Kill rule otherwise.** A cost added after a non-move is seen is already a miss (THEORY §3). Requiring the cost on the
  closed list and measured independently is the right anti-rescue structure. B1 is the remaining leak.
- **DEVIATIONS.** DV2 (ecoli) and DV-DYN1 (grid) are dated, made before data and append-only. "P1–P16 were scored under
  per-cell J" is a statement, not a change of verdict. Fine.

## Confirm review of b73de2f (20 Nov 2026, about 3:40 PM ET, America/New_York)

Reviewer: separate executor, did not write the fixes. Fresh clone at `/workspace/rev117b`, nice 19, detached at `b73de2fea8440cf759888adc0a96e24f0a721684` (rebased on main `1998a2d`). Nothing pushed, commented or merged. The clone was left clean.

**Verdict: READY**

Reproduced: `tools/check_consistency.py` RESULT: PASS (0 FAIL, 21 INFO); CLAIM_MAP rows counted 312, tally total 312. `pytest tools/` 109 passed in 599.56 s (first review was 103; the added dynamics tests, including d5, account for the rest). Official `d5_bode_discrete.py` re-run in `/tmp` was byte-identical to the committed `d5_results.json` (ALL D5 CHECKS PASS, 49/49). No locked prereg file is touched (`git diff origin/main -- prereg/` is empty). D10 in `prereg/ROBUST-SLACK/DEVIATIONS.md` is identical to main.

**Rebase.** `1597218` (#113) and `1998a2d` (#115) are both ancestors. `git log main..HEAD` is two commits only (245fa0d, b73de2f). `git diff --stat origin/main..HEAD` is 27 files, all #117's (DYNAMICS.md, dynamics_checks including new d5, test_dynamics_checks, kill-rule wording, CLAIM_MAP v2.68 note and eight new rows, append-only DEVIATIONS). Shared-file deletions are version/tally lines and the pre-amendment kill-rule sentences, replaced in place. #113/#115 content is intact: CX8 remains in THEORY Appendix C immediately before the new rows; DV-GRIDDX-A / A.1 are unchanged; CT37–CT40, CL18, CX7, v2.65 and v2.66 notes remain.

**Tally.** v2.68 note is provisional (PR #115 merged first as v2.66; draft PR #116 provisionally holds v2.67; the second of #116 and #117 to merge renumbers). On top of main's v2.66 (OPEN 80, PROVED 88, PRIOR ART 29, total 304) the eight new rows are +2 OPEN (CX9, CX10), +3 PROVED (CT41–CT43), +3 PRIOR ART (CL19–CL21) → OPEN 82, PROVED 91, PRIOR ART 32, total 312, matching the note and the consistency check.

### Blockers

**B1, resolved.** CT41 is rewritten on the post-change gap g = |x₀ + Δ|, with a preregistered interval [k_lo, k_hi] (collapsing to a point estimate when no error budget is stated). A non-move is consistent if g < Δ_R(k_lo), a miss if g > max(Δ_band, Δ_R(k_hi)), and INDETERMINATE between. w, the input-process type (step lasting T, or drift at σ_d²) and T or σ_d are preregistered; if they carry error budgets, Δ_R(k_lo) uses the narrowest combination and Δ_R(k_hi) the widest. Without those quantities the band is zero. The earlier upper-bound excuse, and the post-data choice of process type, are both named and closed.

The NOT A TEST trigger at Δ_R(k_hi) is the right choice and is not rescuing. A non-move can be scored a miss only when g > Δ_R(k_hi); if the predicted post-change gap of a non-mover is ≤ Δ_R(k_hi), the test has no power, and NOT A TEST is not a pass. Using k_lo here would be wrong (a gap in the middle is INDETERMINATE, not a miss). Because k_hi, w, process type and T or σ_d are preregistered, the band cannot be widened after the data to swallow a miss. One non-blocking completeness note: if the static band Δ_band exceeds Δ_R(k_hi), a predicted gap in (Δ_R(k_hi), Δ_band] also cannot produce a miss, and the written trigger would not label that case NOT A TEST. That is not a leak in the lenient direction; it does not excuse a miss.

**Wording.** The four-sentence block ("A band exists only where adjustment is lumpy … the rule is unchanged.") is character-identical, whitespace-normalized, in THEORY §3, THEORY §8, FRAMEWORK §9 item 5, README and DYNAMICS.md. The lead-in excuse is the same in all four places: "unless the post-change gap is inside the redesign band at the lower bound of the class's preregistered redesign cost (CT41, `theory/DYNAMICS.md` §2)." CLAIM_MAP CT41 and THEORY Appendix C are complete compressed statements of the same rule (formulas, g = |x₀+Δ|, the three-way split, NOT A TEST at Δ_R(k_hi)), not the verbatim paragraph, which is expected in a table cell. README's lead-in still drops "by the preregistered share"; the new block itself is identical. Not blocking.

**DV-DYN1.** Revised in place, with a dated note ("Text revised about 3:30 PM ET the same day, before this entry merged and before any data"), from the earlier "cost or its upper bound" wording to the lower-bound / INDETERMINATE / NOT A TEST rule, including preregistered w, process type and T or σ_d. The entry is still unmerged (this draft PR) and claims no new grid data; I compared against 245fa0d / b9fb105 and against main, and only this one line is added relative to main. E. coli DV2 is append-only vs main. No locked prereg, prediction or verdict file changed vs main.

**B2, resolved.** The Bode verdict is split: OVERREACH for continuous observation (Kalman–Bucy, |S|² = N/Φ_y ≤ 1); OPEN for periodic or sampled reads, which are in THEORY's class. I independently re-derived the discrete claim. For the steady-state one-step predictor, S(z) = [1 + C(zI−A)^{-1}K]^{-1} = det(zI−A)/det(zI−A+KC) (scalar output), S(∞) = 1. Zeros are eig(A) and poles are eig(A−KC); both are Schur when the world is stationary and the predictor is at steady state. Jensen's formula then gives (1/2π)∫_{-π}^{π} ln|S(e^{iω})| dω = 0 exactly. If S is not identically 1, |S| > 1 on a positive-measure set. The spectral identity |S|² = (CPC′+R)/Φ_y follows because the innovation is white with variance CPC′+R. I re-computed the reviewer's four scalar AR(1) worlds with S = (z−a)/(z−a+K), independently of d5's code path: max|S| = 1.133014, 1.436049, 1.045186, 1.394666 (all at Nyquist), integral 0 to 10^{-17}, identity to 10^{-15}, matching both the first review and the committed d5 results. An independent 40-world re-run at d5's seed 1988 reproduced max|S| = 1.0390–1.8911; an alternate seed (999) gave 1.0252–1.9215; in all 80, A and A−KC were Schur, |S| > 1, the integral was 0 to 10^{-16}, the det and inverse forms agreed, and the maximum was at Nyquist. "Always at Nyquist" is a fact about the checked class (positive AR(1) modes, low-pass spectra), and the text correctly says "every world checked." Whether this changes argmin J is rightly left OPEN: S maps observations to innovations and is not a cost J pays.

### Should-fixes

1. Post-change gap |x₀+Δ|: done (CT41).
2. CT43(iv) numbers: independently recomputed on the same 600-point grid (4×5×6×5, nothing skipped). Counts: 510 same, 90 G_more, 0 G_fewer, max extra copies 1 (15%). Share by X: 8%, 4%, 13%, 16%, 17%, 32% at X = 0.05, 0.1, 0.2, 0.4, 0.6, 0.8. The 3-vs-4 toy and 0.6% J-gap also match. The text now says "broadly rises with X" and flags the earlier three-point mistake. CLAIM_MAP CT43 matches.
3. Gillespie 1/N: "for a large population" is in the G(π) definition, in CT42(ii), and in the placement sentence; finite-N within-generation variance at order 1/N is attributed to Gillespie 1974. DOI 10.1093/genetics/76.3.601 resolves on Crossref to Gillespie, Genetics 76, "NATURAL SELECTION FOR WITHIN-GENERATION VARIANCE IN OFFSPRING NUMBER." I did not re-read the paper's text.
4. Waite et al. 2016: credited at CL20 and CX10 as an experimental test of how chemotaxis diversity changes population performance; selection on it still untested. DOI 10.15252/msb.20167044 resolves to Waite, Frankel, Dufour, Johnston, Long, Emonet, *Mol Syst Biol* 2016, "Non-genetic diversity modulates population performance." Erratum 10.15252/msb.20178149 resolves to the 2018 erratum of the same article.
5. Dixit 1991 / Chalkley 1997: both cited at CL19. 10.2307/2298051 resolves to Dixit, *Review of Economic Studies* 1991, "Analytical Approximations in Models of Hysteresis." 10.1016/0165-1889(91)90037-2 resolves to Dixit, *JEDC* 1991, "A simplified treatment of the theory of optimal regulation of Brownian motion." 10.1016/s0165-1765(97)00222-x resolves to Chalkley, *Economics Letters* 1997, "An explicit solution for dynamic menu costs with zero discounting." I did not read either paper's text; the coefficient 6 stands on the renewal derivation already checked in the first review.
6. Log-reserve scaling assumption (every cost, including upkeep, scales with the reserve): stated at CT43(i).
7. Zero-drift ruin → 1 (constraint excludes non-positive growth): stated at CT43(iii).
8. CX9 volatility (sd 0.01 of d ln w per period) and 400-point log grid over w ∈ [0.5, 20]: stated; no-cost w_down 0.991 kept.
9. Versioning: THEORY is v2.9 draft; CLAIM_MAP is provisionally v2.68, with the collision and the #116/#117 renumbering rule stated in the note.
10. README keeps "only where adjustment is lumpy"; the four canonical statements are word-consistent, as above.

**Sung & Hara 1988.** DOI 10.1080/00207178808906338 resolves on Crossref to Sung & Hara, *International Journal of Control* 48 (1988), "Properties of sensitivity and complementary sensitivity functions in single-input single-output digital control systems." That is the right type of discrete Bode citation. The predictor integral itself is the Jensen argument above, which I checked independently.

No remaining blockers. READY to merge once whoever is authorized to merge does so; this confirm does not merge, comment or push.
