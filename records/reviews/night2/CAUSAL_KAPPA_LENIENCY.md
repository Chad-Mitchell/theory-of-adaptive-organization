# CAUSAL-KAPPA-LENIENCY — is N6's causal form too lenient at κ_F = ½? (pick 38, rule slot)

**Queue:** CAUSAL-KAPPA-LENIENCY (from `tests/LAB_AKLMT_TAU/RESULTS.md` surprise 1, pick 36). Pick 38, RULE slot: top of
ledger 178 (I = 1.8); ledger 177 unaided order (176 void, numbering collision), 178 rule_rank, 179 claim; outcome at the
end of this pick. 15 Nov 2026, about 7:51–8:00 PM ET (report written 7:58 PM ET). **By:** executor queue-pick38 (for Ace, Chad t1914/t1916). Exposure:
authored none of LAB-AKLMT-TAU, CAUSAL-KILL-MAGNITUDE(-REVIEW), PREREG-LOSS-LOCK or the N6 text.
**Scope:** proposal and analysis only; no data outcome, so no prereg. The THEORY edit it recommends (N6 causal form) is in a
separate author-only PR marked **DO NOT MERGE without separate reviewer PASS** (Chad t1916). No locked result, kill condition
or CLAIM_MAP status is moved here. Vigilance (H8) OPEN.

## 1. Question
LAB-AKLMT-TAU: lab forecasters whose level at ρ = 0 is 0.45 against an optimum of 0.02, and whose move with ρ is 0.53 of the
feasible optimum's (CI 0.43–0.62, ~10 SE below 1), **passed** the N6 causal form at κ_F = ½. Item: should the causal kill be
paired with a level/optimality check, or should κ_F be tied to the measured s·λ?

## 2. First principles
The causal form reads a share r = (measured move)/(locked optimum's predicted move, scaled by adjustment share s and input
reliability λ). Under the theory, r = 1 up to the bias in the scaled prediction; CAUSAL-KILL-MAGNITUDE-REVIEW §2 showed κ_F is
exactly that tolerated bias (a true design is safe from the kill while the prediction overstates its move by < 1/κ_F), which is
why κ_F ≤ ½. So the kill already encodes the claim "r ≥ κ_F". The defect is not the kill but the **PASS rule**, which is not
the mirror of the kill:

- current (N6 text silent; every locked causal prereg, MV10 and `tools/power_gate.py`): FAIL iff D + zσ < κ_F·P; **PASS iff
  D − zσ > 0**; else INCONCLUSIVE.

So "passed" means *direction established and r ≥ κ_F not excluded*. A design whose true share lies in (0, κ_F), i.e. inside
the region the kill is meant to catch, is labelled PASS most of the time at ordinary SNR (§3, r = 0.40: 82% at SNR 9.7). That
is the leniency. Its source is an asymmetry in the decision rule, not the value of κ_F.

The two proposed remedies, read causally:
1. **Tie κ_F to measured s·λ.** s·λ is already in P (N6, v1.4.7). Making κ_F depend on it as well counts the same nuisance
   twice. The defensible version, κ_F = 1 with the s·λ error carried into the decision (rule R2 below), is a test of size.
   It kills a true design whenever the prediction is biased by more than its standard error: 55–100% for a 1.6× overstatement
   (§3), which is what CAUSAL-KILL-MAGNITUDE-REVIEW already rejected. **Rejected.**
2. **Pair with a level check (AND).** The level is read on the proxy's absolute scale; the causal contrast differences out
   any fixed proxy offset (the VIX premium, CAISO's BTM definition), which is its point. Requiring a level match before a PASS
   imports exactly the offsets the contrast removes: a true design with a 0.15 level offset (3 SE) passes 15% instead of 94% (§3).
   The level already has its own verdict, N6's optimality form, which needs a named rival and is scored separately. **Rejected as
   a condition; kept as a mandatory report** (the optimum's level at both input values is computed anyway to get P).

**Proposal (mirror PASS).** PASS iff D − zσ > κ_F·P (the move is *established* above the same share the kill uses); FAIL
unchanged; else INCONCLUSIVE. Plus two report-only lines: the share D/P with its CI ("below the locked optimum's move" when the
CI excludes 1), and the design's level vs the optimum's at each input value. This is the standard one-sided test against a
pre-set bound (the lower leg of Schuirmann's two one-sided tests; Lakens 2017, read: §"Equivalence tests", and its four-outcome
reading of NHST + bound test). KNOWN statistics; only its use for N6 is new here.

**Cost in power: none at κ_F ≤ ½.** P(PASS | r = 1) = Φ((1 − κ_F)·SNR − z), P(FAIL | r = 0) = Φ(κ_F·SNR − z). For κ_F ≤ ½ the
FAIL leg binds, so MV10's minimal gate |b|·S ≥ (z + z_π)σ/κ_F is unchanged (at κ_F = ½ the two legs are equal: SNR ≥ 5.6).
Every prereg that met MV10 at κ_F ≤ ½ has P(mirror PASS | true) ≥ π already.

## 3. Numerical checks (own code, `CAUSAL_KAPPA_LENIENCY_checks/`; no repo imports in `rules_mc.py`)
`rules_mc.py`: K = 30 contrasts, OLS through the origin, s = 0.63, 20,000 reps per row, seed 20261115+179; z = 1.96, κ_F = ½;
SNR = P/se (realized SNR printed; within 0.3 of nominal except the λ = 0.8 row at nominal 20, where errors-in-variables noise
caps it at 10.8). Rates are FAIL / PASS (INCONCLUSIVE = rest). R0 = current rule, R1 = mirror, R2 = κ_F = 1 with s·λ error
propagated, L = R1 PASS AND level match.

| true share r (scenario) | SNR | R0 F / P | R1 F / P | R2 F / P | L PASS |
|---|---|---|---|---|---|
| 1 (true, s·λ known) | 5.6 / 9.7 / 20 | 0 / 1.00 | 0 / 0.78, 0.99, 1.00 | 0.03 / 0.97 | 0.74, 0.94, 0.95 |
| 1 (s·λ plug-in, log-sd 0.3) | 5.6 / 9.7 / 20 | ≤0.005 / ≥0.995 | ≤0.005 / 0.70, 0.91, 0.97 | ≤0.006 / 0.87–0.96 | 0.67–0.92 |
| 1 (level proxy offset 0.15 = 3 SE) | 9.7 | 0 / 1.00 | 0 / 0.99 | 0.03 / 0.97 | **0.15** |
| 0.63 (prediction overstated 1.6×, tolerated) | 5.6 / 9.7 / 20 | 0.005 / 0.92–1.00 | ≤0.005 / 0.12, 0.26, 0.72 | **0.55, 0.92, 1.00** / — | 0.12–0.68 |
| 0.53 (AKLMT-like) | 5.6 / 9.7 / 20 | 0.02 / **0.82, 0.98, 0.99** | 0.02 / 0.04, 0.05, 0.10 | 0.73–1.00 / — | ≤0.09 |
| 0.40 (below κ_F) | 5.6 / 9.7 / 20 | 0.09, 0.17, 0.52 / **0.60, 0.82, 0.48** | same F / ≤0.009 | ≥0.90 | ≤0.009 |
| 0.25 | 5.6 / 9.7 / 20 | 0.30, 0.67, 0.99 / 0.30, 0.32, 0.01 | same F / ≤0.001 | ≥0.97 | 0 |
| 0 (named rival: no move) | 5.6 / 9.7 / 20 | 0.78, 0.99, 1.00 / ≤0.03 | same F / 0 | ≈1 | 0 |

Analytic Φ((r − κ_F)SNR − z) for R1 PASS and Φ((κ_F − r)SNR − z) for FAIL match the Monte Carlo within the t-vs-normal slack
of K = 30 (e.g. r = 1, SNR 5.6: analytic 0.800, MC 0.778; r = 0.40, SNR 20: 0.516 vs 0.517).

Readings: (i) R0 labels a design whose true share is *below* the kill line PASS 48–82% of the time; R1 does so ≤ 1%. (ii) R1
keeps R0's FAIL exactly and its false-kill rate (≤ 0.5%), and at the MV10 minimum still passes a true design ≈ 0.78–0.80.
(iii) The price of R1 is honest: a true design whose prediction is overstated by up to 1/κ_F (tolerated by the kill) now
reads INCONCLUSIVE more often (12–72% PASS) instead of PASS; it is never killed. (iv) R2 and L fail for the reasons in §2.

`reread_and_gate.py` (report-only re-reading of locked results under R1; **locked labels are not changed**; plus a gate
check against `tools/power_gate.py`):

| locked causal-form result | D ± σ | scaled P | kill line | D − 1.96σ | share [CI] | locked label (R0) | under R1 |
|---|---|---|---|---|---|---|---|
| LAB-AKLMT-TAU Exp 1 (N23) | 0.518 ± 0.048 | 0.984 | 0.492 | 0.424 | 0.53 [0.43, 0.62] | PASS | INCONCLUSIVE |
| LAB-AKLMT-TAU Exp 3 (report-only R3) | 0.629 ± 0.094 | 1.027 | 0.514 | 0.444 | 0.61 [0.43, 0.79] | PASS | INCONCLUSIVE |
| CAUSAL-NULL-INVARIANCE (in-model) | 0.290 ± 0.029 | 0.350 | 0.175 | 0.232 | 0.83 [0.66, 0.99] | PASSED | PASSED |
| STAKES-SHIFT-CAISO (absolute ε margin, not N6's form) | — | — | — | — | — | INCONCLUSIVE | not applicable |

Gate check: at κ_F = ½, SNR 5.6 gives P(mirror PASS | true) = P(FAIL | null) = 0.7995 and `power_gate.py` says met; at 0.9 ×
that SNR both are 0.71 and the tool says not met; at κ_F = ¼ the FAIL leg binds (mirror PASS ≈ 1). The report-only
`mirror_pass` block added to `tools/power_gate.py` reproduces these (`tools/test_power_gate.py`, 23 pass).

## 4. Recommendation (for a separate reviewer; THEORY v1.4.17 author-only PR, DO NOT MERGE)
1. **N6 causal form, pass side (new sentence):** a causal-form test reads *passed* only when the measured move exceeds, in the
   predicted direction and beyond measurement error, the same share κ_F of the scaled predicted move that its kill uses;
   a move established in direction but not above κ_F reads INCONCLUSIVE. Every causal-form result reports the share with its CI
   (and "below the locked optimum's move" when the CI excludes 1) and the design's level against the optimum's level at each
   input value; the level is a verdict only under the optimality form, locked with its named rival. κ_F is not tied to s·λ.
2. **No change to the kill** (N6 kill column and §9): FAIL rule, κ_F range and scaling unchanged.
3. **Not retroactive:** applies to preregs locked after merge; LAB-AKLMT-TAU's locked PASS (N23) stands with the R1
   re-reading noted (report-only). No status change.
4. **FRAMEWORK MV10:** P(PASS | true) for a causal-form test is Φ((1 − κ)·SNR − z); the minimal gate is unchanged for κ ≤ ½.
5. Reviewer questions: (Q1) should a "passed" causal result whose share CI excludes 1 carry the qualifier in its label, not
   only in the report? (Q2) should over-response (share CI above 1/κ_F) get a symmetric report line? (Q3) is the "not
   retroactive" ruling right for N23, given its locked rule was written before the mirror rule existed?

## 5. Limits
Gaussian contrasts, one K, first-order adjustment; s·λ error modelled as log-normal plug-in; the level-pairing row uses one
offset size. No field data analysed. Prior art read: Lakens (2017), *Soc Psychol Personal Sci* 8(4):355–362,
doi 10.1177/1948550617697177 (TOST, one-sided bound tests, four outcomes); Schuirmann (1987) is cited there, **not read here**.

## 6. Surprise (rule 4)
**Moderate:** the leniency is a PASS/FAIL asymmetry present in every locked causal prereg since v1.4.7 (PASS against 0, FAIL
against κ_F), not a wrong κ_F; the symmetric fix costs no power at κ_F ≤ ½. Under it, N23's PASS (and its Exp 3 replicate) would
read INCONCLUSIVE; the only other locked causal pass (CAUSAL-NULL-INVARIANCE) survives.
