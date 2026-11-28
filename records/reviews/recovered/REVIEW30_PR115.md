# Hostile independent review: PR #115 (branch v2.7-robust, head 7c1dc22; prereg commit a0e97cb)

Reviewer: independent executor (math, prior art, statistics). Date: Fri 20 Nov 2026, about 2:30 PM ET.
Clone: /workspace/gtao-review115 at 7c1dc22. Nothing pushed or merged. Reviewer scripts are in /workspace/rev115
(indep.py, r1a.py, r34.py, prereg_sim.py, prereg_sim2.py, cr.py). They were written from the text, not copied from
theory/robust_checks.

**Verdict: READY-WITH-FIXES.** The math is correct, and every number I recomputed reproduces. The PR has two kinds of
problem. Several "new here" items, and two PROVED labels, are prior art. The preregistration's key test RS-2a can
PASS under its own named rival R-fixed through a mechanical estimation bias. Both are fixable before any data. The
prereg fix must go into a dated `prereg/ROBUST-SLACK/DEVIATIONS.md` committed before any dataset is opened. Re-review
the must-fix items before merging.

## Tooling
- `tools/check_consistency.py`: RESULT: PASS (FAIL 0, INFO 21).
- `pytest tools/`: 99 passed (284 s).
- Prereg file unchanged between a0e97cb and 7c1dc22 (verified with `git diff`).

## Independent recomputation (all reproduced unless noted)
| Claim | Reviewer result |
|---|---|
| R1-a n_E closed form | Exact against first-difference optimality on 20,000 random cases: 0 mismatches. "Pays iff wΔp(1−p) > h": J(2) < J(1) iff that holds. "Some p iff wΔ/4 > h" holds because max p(1−p) = 1/4. Log slope is 1/ln(1/p). Non-monotone in p: for wΔ/h = 100, n_E = 1, 1, 2, 4, 6, 10, 22, 1, 1 at p = .001 … .999 (there is a cliff from 22 to 1 near p = 0.99). |
| R1-b n_R example | ε₁ = 1.0005e-6, ln ε₁/ln 0.1 = 5.9998, so n_R = 6. n* = max(n_E, n_R) holds by discrete convexity. |
| R1-d proof | Correct. κ_n − κ_{n_E} = t(n−n_E)h + (p^n − p^{n_E})(e^{tX}−1) ≥ t[J(n) − J(n_E)] ≥ 0 for n < n_E, and a pointwise larger convex κ through 0 has a smaller positive root. No violation of θ_n ≤ θ_{n_E} in 17,715 random checks. Worked case θ_n (n = 1..14) = .69, 1.71, 2.57, 3.34, 4.02, 4.57, 4.85, 4.74, … gives n* = 7, 5, 3, 3 at B = 1.5, 2, 3, 5. |
| R2-a elasticity | sympy gives −a/(8Ax+3a), in (−1/3, 0). The bounds (1+u)^{2/3} ≤ ratio ≤ 1+u hold on u ∈ (0, 5]. Ratio is 1.826 at u = 1 (worst-case objective: 1.458). Fitted ruin chance is 1.04e-4 and 1.78e-6 at u = 0.2, 0.5. |
| R2-b | Factors 2.543, 1.458, 1.187, 1.067, 1.016 for n = 5–200. Plug-in exceedance at n = 20 is 3.55e-3 (3.6×). |
| R2-c | 8 and 17 (and 7/7/7) reproduce. The MLE count "6" for 1 in 10 sits exactly on the boundary 0.1⁶ = ε₁; in floating point it gives 7 (nit). |
| R2-d | 3.090, 3.270, 4.565, 5.897. Cantelli √999 = 31.61, which is 10.2× Gaussian. Matches El Ghaoui et al. 2003 and Calafiore & El Ghaoui 2006. |
| R2-e / R3 | Own grid optimizer: B_min 0.4864, B_slack 0.5079. σ-margin is 0, 0, 0, 2.61%, 16.2%, 49.1%, 103.5% at B = .49 … 5. Bound ratio 1.0570 at B = 0.5, σ +1%. B_min 0.4864 → 0.4891 → 0.4917, τ 0.3162 → 0.3028. |
| R4 | Error variance has the closed form aλ/(λ+b) + bN/2, which matches the Lyapunov solution. J*(0.5) = 0.5 (blind), J*(4.5) = 2.171, J*(2.5) = 1.631, redesign 1.336, an 18.1% saving. Note: much of the saving comes from switching judgment *off* in the calm regime. |

## DOIs
All 21 DOIs in the PR (18 in ROBUSTNESS.md, 3 in the PREREG) resolve on Crossref. Titles, authors and years match the
citations. The cited papers say what is claimed: El Ghaoui/Calafiore give the √((1−ε)/ε) moment worst case, Dufresne &
Gerber give diffusion-perturbed compound-Poisson ruin, Carlson & Doyle give HOT, Gu et al. give duplicate-gene
buffering, and Opler et al. and Bates et al. give precautionary cash. Minor: Barlow & Proschan is a fair general
reliability reference, but the canonical common-cause-failure model is the beta-factor/Marshall–Olkin line. Consider
adding a CCF reference.

## MUST-FIX
1. **RS-2a can PASS under the named rival R-fixed (mechanical bias).** r_i = B_obs/(z·σ̂_i). Because 1/σ̂ is
   right-skewed and noisier for short records, short-record systems get inflated r even when every system holds a
   constant multiple of its *true* σ, which is R-fixed. Reviewer simulation (prereg_sim*.py: n_i log-uniform over
   5–40, Spearman with a Fisher CI as a bootstrap stand-in) gave these results under R-fixed:
   - Gaussian shocks: mean ρ = +0.06 to +0.09, just under the +0.10 margin. P(PASS) ≤ 4%.
   - Student-t ν = 4: mean ρ ≈ +0.16. P(PASS) = 13% (200 systems) and 42% (1000 systems).
   - Student-t ν = 3: mean ρ ≈ +0.19. P(PASS) = 20% and 75%.

   Real cash-flow and charge-off shocks are heavy-tailed, so "RS-2a PASS beats R-fixed" (PREREG §3) is false as
   written. Fix in DEVIATIONS.md before any data, with either of these:
   - (a) Calibrate the null. Under R-fixed, simulate ρ by parametric bootstrap from each system's own n_i and fitted
     tail, and require the observed interval to clear that null's 97.5% point plus κ.
   - (b) Estimate σ for B_plug out of sample, from windows not used for the reserve-level comparison, or from a
     class-pooled scale model.
2. **Prior art mislabeled as PROVED/new (relabel; no math change).**
   - **R2-c (CT38 part)** is the *state-of-knowledge correlation* result from nuclear PSA: Apostolakis & Kaplan 1981,
     "Pitfalls in risk calculations", Reliability Engineering 2:135–145, doi 10.1016/0143-8174(81)90019-6 (Crossref
     OK). Identical redundant parts share parameter uncertainty, so E[p^n] > (Ep)^n and plug-in means understate
     redundant-system failure. ASME/ANS PSA standards and NUREG-1855 require it. Move it to PRIOR ART (CL18). The
     "copy-count reading" is a trivial inversion, not new.
   - **R2-b and the 3.6× figure** are exactly Gerrard & Tsanakas 2011, "Failure probability under parameter
     uncertainty", Risk Analysis 31:727–744, doi 10.1111/j.1539-6924.2010.01549.x (Crossref OK). For capital they are
     Bignozzi & Tsanakas 2016, J. Risk Insur. 83:949, doi 10.1111/jori.12075 (Crossref OK). Cite both in R2-b and in
     PREREG §4 via DEVIATIONS. The "distinct content" of RS-2a is an empirical claim about selected systems; the
     normative prescription is known.
   - **R1-a/R1-b "new here: closed form; log growth" and §0's "(CT37, new here)"**: the least-cost parallel
     redundancy and the reliability-floor count n ≥ ln(1−R)/ln p are textbook. See Kettelle 1962, Oper. Res.
     10:249–265, doi 10.1287/opre.10.2.249 (Crossref OK), and Kuo & Prasad 2000, already cited. Log growth follows
     immediately. Keep PROVED (in-model) only for "inside J", and say "known in substance". Stake-independence of n_R
     holds by construction (all-down = ruin, so no buffer can help); call it an assumption, not a finding.
3. **Cross-PR contradiction about the GB "3 extra layers".**
   - PR #113's P24 row says the gap "may be unmodelled redundancy, `theory/ROBUSTNESS.md`".
   - PR #115 §8 and PREREG §5 say robustness, as proved, produces copies and buffers at one time constant and "does
     not rescue the three extra layers"; PREREG §5 adds "in-model, unsupported for the count".
   - Both overreach in opposite directions. B1's K* was computed with ruin slack. GB ruin binds. CT22 says a binding
     constraint moves the design toward the survival-optimal end, and CX7 (robust layer count) is OPEN. So the honest
     common wording is: "copies and buffers (CT37/38) do not add distinct layers. Whether binding ruin or uncertainty
     changes K* for GB is not computed (OPEN). The gap is neither explained nor shown to be waste."
   - Reconcile both PRs before either merges. PREREG §5 is locked, so correct it via DEVIATIONS.md.
   - Note for the parent: the earlier message to Chad ("Those 3 'extra' layers may be redundancy, not waste") is not
     supported by this PR's in-model results either. It stays an open possibility only through binding-ruin K*, which
     is uncomputed.

## SHOULD-FIX
4. **CT40(a) misstates Taleb.** Taleb's technical antifragility is *convexity* of the response to a stressor (Taleb &
   Douady 2013, Quant. Finance 13:1677, doi 10.1080/14697688.2013.800219, Crossref OK), not a falling level. A concave
   J*(a) (convex −J*) with redesign *is* antifragile to variation in a in Taleb's sense; that is the content of (c).
   Reword (a) as "no gain in level from more volatility", drop "cannot produce Taleb-style antifragility", and cite
   Taleb & Douady.
5. **CT40(c) prior art:** the Oi–Hartman–Abel effect, where a firm that re-optimizes per state gains from price
   variability by convexity. Oi 1961, Econometrica 29:58, doi 10.2307/1907687 (Crossref OK). Cite it next to the
   real-options sentence.
6. **R3 "jump of size above B ⇒ P(ruin by T) ≥ 1−e^{−λT}" is false as stated.** In CT22's model B is the *initial*
   reserve, and with positive drift the reserve grows above B. The bound holds only for a jump larger than any reserve
   the path reaches, or with the reserve capped at B (dividend barrier). Restate it. r3_lean.py only evaluates
   1−e^{−λT}; it does not check the claim.
7. **R3/CT39 wording:** "voids the certificate" refers to the Lundberg *upper bound* failing, not to a proof that
   ruin exceeds ε. Say so. "Zero margin" is complementary slackness; label it elementary.
8. **PREREG, other statistical gaps.** All of these go in DEVIATIONS.md before data:
   - (a) **Age confound.** Record length tracks firm or bank age. Young firms hold more cash because of financing
     constraints and growth options (Almeida, Campello & Weisbach 2004, doi 10.1111/j.1540-6261.2004.00679.x, Crossref
     OK; Bates et al. 2009 already cited). Name a rival, R-age, and add a within-system test: the same system's r as
     its record lengthens, with a size or financing-constraint control.
   - (b) **Truncation.** Scoring regulated systems only when B_obs > 1.05 × the minimum selects on the outcome, which
     inflates RS-1 and distorts RS-2a. Score all systems, and run that cut as a sensitivity check.
   - (c) **ε definition.** What counts as a "failure", and whether failed systems' windows enter the pooled frequency,
     is undefined. Pooling "scored" (surviving) systems builds in survivorship.
   - (d) **Hill estimator.** It runs on the upper 10% of as few as 5 windows. Set a minimum tail count k (for example
     ≥ 10) or mark the system UNTESTED for RS-2b.
   - (e) **RS-3.** "Same interval rule" is ambiguous for the 80% criterion: is it a point estimate or a CI on the
     share? Also, the PREREG's per-window ε does not match ε₁ in CT37's n_R; state the horizon.
   - (f) **Power.** At the 20-system minimum, the Spearman CI is about ±0.45, so RS-2a will almost always be
     INCONCLUSIVE. Either state that, or set a power-based minimum.
9. **Lock evidence.** a0e97cb's 1:45:43 PM ET time is local author time. Both commits first reached GitHub together,
   in one push at 1:52:22 PM ET (activity API, 18:52:22Z), so there is no independent timestamp separating the lock
   from the theory. No data were involved, so this is harmless, but "locked at a0e97cb before any data" should say it
   is self-attested. The PREREG also cites CT37–CT40 in a file that did not exist at its own commit.
10. **R1-d labeling.** State that the ordering is under the Lundberg certificate, as in CT22. Note that it is an
    elementary consequence of pointwise ordering of cumulant functions, which is standard in actuarial ordering of
    adjustment coefficients. "Not searched exhaustively" is honest; keep it.

## NITS
- R2-c example: 1 failure in 10 at the MLE sits exactly on 0.1⁶ = ε₁. Pick an off-boundary example or say "6 (at the
  boundary)".
- R1-a assumes n ≥ 1. J(0) = wE₀ (dropping the layer) is K = 0, handled elsewhere; say so.
- The n_E cliff from 22 to 1 near p → 1 is worth one sentence ("copies stop paying abruptly").
- §0: "exactly as safe as ε under the model, and no safer" reads as general before it is qualified by "whenever ruin
  binds". Reorder.
- Versioning: ROBUSTNESS/CHANGELOG say v2.7, but THEORY.md's title and README still say v2.4 draft.
- `r2_ambiguity.py` docstring says "exact t law". Use "t distribution". Repo rule: "law" only in the hypothesis
  sentence; "power laws" in the HOT paper title is fine.
- No "bill", no joules for firms, no "theory of everything" found. "Fail-proof" appears only in quotes or scoped.
  Good.

## CLAIM_MAP numbering (mechanical)
PR #115 says v2.66 with a tally of 301 on top of v2.64 (294). PR #113 (open, head 315e620) says v2.65 with a total of
297, and retypes 30 rows. The two branches conflict in 8 hunks (`git merge-tree`). Whichever merges second must
rebase:
- renumber the notes;
- recompute the tally from the union. Expected OPEN 80, PROVED 88, PRIOR ART 29 (plus any must-fix relabels: R2-c
  part moves to PRIOR ART but CT38 stays one row), total 304. Recompute with check_consistency rather than trusting
  this;
- update the STATUS, README and THEORY pointers.

## Labels: earned?
- CT37: PROVED (in-model) is earned for the math. Must-fix 2 means the novelty must be relabeled.
- CT38: R2-a and R2-e are earned. R2-c is PRIOR ART (SOKC).
- CT39: earned but elementary. Fix item 6.
- CT40 (a)–(c): the math is earned. The Taleb framing is wrong (item 4) and the prior art (Oi) is missing.
- CL18: correct as PRIOR ART.
- CX7, CX8: OPEN, fine.

---

## CONFIRM ROUND (head 23b6f12; deviations 6532d24), Fri 20 Nov 2026, about 2:50 PM ET

**Push order.** Verified with the GitHub activity API:
- 6532d24 (DEVIATIONS D1–D9) was pushed alone at 2:18:28 PM ET.
- 23b6f12 was pushed after it, at 2:32:47 PM ET.

So the deviation was public before the theory revision. Between 6532d24 and 23b6f12, DEVIATIONS.md changed only in its
header time typo ("2:50" became "about 2:15, committed 2:18"), and that change is disclosed. PREREG.md is untouched.

**Tooling.**
- `check_consistency`: RESULT: PASS (FAIL 0).
- `pytest tools/`: 99 passed (656 s, nice 19, box load about 30).

**RS-2a′ (D1), independently re-implemented from the text** (`rs2a_mine.py`):
- My own MLE ν̂ on MAD-standardized pooled shocks.
- Heterogeneous true σ (log-normal) across systems.
- Calibrated null with M = 300 per class (fewer than D1's 1000, to save compute).
- Fisher CI, plus one cell with the locked-style bootstrap at B = 1000.

| Shocks | Systems | Reps | Mine P(PASS \| R-fixed) | Author |
|---|---|---|---|---|
| Gaussian | 200 / 1000 | 100 / 40 | 0.000 / 0.000 (P(FAIL) 0.01 / 0) | 0.000 / 0.00 |
| t₄ | 200 / 1000 | 100 / 40 | 0.000 / 0.000 | 0.000 / 0.00 |
| t₃ | 200 / 1000 | 100 / 40 | 0.000 / 0.000 | 0.000 / 0.00 |
| t₃, bootstrap B = 1000 | 200 | 30 | 0.000 | — |

Mean ν̂ is 5.2, 2.9 and 2.45 for Gaussian, t₄ and t₃, matching the author's 5.3, 2.9 and 2.4. The ν̂ underestimate makes
the null heavier than the truth: conservative for PASS, and it raises ρ̄₀, so FAIL is slightly easier. Under R-fixed
that is the right verdict (P(FAIL) = 0.01 at Gaussian/200).

Power (t₄, mine vs author):

| Systems | γ = 1 | γ = 0.5 |
|---|---|---|
| 20 | 0.02 vs 0.02 | — |
| 50 | 0.23 vs 0.22 | 0.01 vs 0.01 |
| 200 | 1.00 vs 0.995 | 0.07 vs 0.095 |
| 1000 | — | 0.975 vs 0.98 |

The D2 table and the 200-system minimum are confirmed.

**Must-fixes.**
1. **RS-2a.** Fixed by D1 and D2; confirmed above.
2. **Relabels.**
   - Confirmed: R2-c moved to PRIOR ART (CL18), and CT38's row now covers only R2-a and R2-e.
   - Confirmed: R2-b and the 3.6× figure are credited to Gerrard & Tsanakas and Bignozzi & Tsanakas.
   - Confirmed: CT37 is "known in substance" (Kettelle). n_R's stake-independence is now stated as an assumption. The
     "new here" wording is removed, including from §0.
   - The new R2-c example (1 failure in 12) is off the boundary: 6 / 8 / 14 recomputed.
3. **GB wording.** D7, ROBUSTNESS §8 and PR #113's P24 (head d3c4838) now agree: "neither explained nor shown to be
   waste" (PR #113's version: "not shown to be excess, no mechanism established"). Confirmed.

**Should-fixes.**
- **4. CT40 Taleb–Douady framing.** Correct. Concave cost means antifragile to *variation* in a; (a) is restated as
  "no gain in level".
- **5. Oi–Hartman–Abel.** Cited. **Abel 1984 JEDC as a substitute is OK.** Crossref confirms "The effects of
  uncertainty on investment and the expected long-run capital stock", JEDC 7:39–53. It is a Hartman–Abel convexity
  paper. Abel 1983 AER is the more canonical cite but optional.
- **6. CT39 capped-reserve jump bound.** Correct as restated: with the reserve capped at B_cap < X, every jump ruins,
  so P ≥ 1 − e^{−λT}. The no-cap caveat is stated. The MC (0.867 vs floor 0.865) and its test assertion check out.
- **7. Certificate wording.** Fixed ("Lundberg upper bound exceeds ε; ruin above ε not proved"). "Elementary" added.
- **8a–f.** Addressed by D3–D6 and D2:
  - R-age rival, with a within-system fixed-effects test against its own null;
  - the outcome cut withdrawn and kept only as a sensitivity check;
  - failure defined from survivorship-free sources, with failed systems pooled into ε;
  - Hill needs k ≥ 10 and ≥ 50 systems;
  - RS-3 uses a Wilson-interval rule, ε₁ = ε, and a calibrated null;
  - power is stated.
- **9.** Lock evidence is declared self-attested (D9, CX8).
- **10.** R1-d is scoped to the Lundberg certificate and labeled probably known.

**Nits.** All done:
- versions read v2.7 across THEORY, README and STATUS;
- "t law" is gone;
- §0 is reordered;
- the n ≥ 1 note and the 22 → 1 cliff are added;
- the Marshall–Olkin CCF reference is added.

**DOIs.** 10 new DOIs, all resolving on Crossref with matching titles, authors and years: Kettelle 1962, Apostolakis &
Kaplan 1981, Gerrard & Tsanakas 2011 (online 2010), Bignozzi & Tsanakas 2016 (online 2015), Oi 1961, Hartman 1972,
Abel 1984, Marshall & Olkin 1967, Taleb & Douady 2013, Almeida et al. 2004. With the earlier 21, that makes 31, matching
the author's count.

**Repo rules.** No new "law" (beyond paper titles) and no "bill" or joules.

**Remaining (non-blocking).**
- (i) PR #113 and PR #115 still conflict in 8 hunks of CLAIM_MAP/STATUS/README/THEORY. Whichever merges second renumbers
  its note and recomputes the tally with `check_consistency`.
- (ii) RS-2a′ is not simulated outside the Student-t family. D1 already routes skewed classes to a skew-t null or
  INCONCLUSIVE.
- (iii) "Margin only by accident of the buffer, not by design" (§0) is slightly editorial. Optional.

**CONFIRM VERDICT: READY.**
