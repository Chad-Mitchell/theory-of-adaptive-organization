# PASS-RULE-SYMMETRY-AUDIT — do locked pass/fail rules let a miss still pass? (pick 39, unaided slot)

**Queue:** PASS-RULE-SYMMETRY-AUDIT (from CAUSAL-KAPPA-LENIENCY, pick 38, moderate surprise). Pick 39, UNAIDED slot: top of ledger 181; ledger 181 unaided order, 182 rule_rank, 183 claim; outcome at the end of this pick. 15 Nov 2026, about 8:03–8:15 PM ET (America/New_York). **By:** executor queue-pick39 (for Ace, Chad t1914/t1916). Exposure: authored none of CAUSAL-KAPPA-LENIENCY, its PR #74, or the locked preregs under audit.
**Scope:** report and report-only tooling. No locked result, kill line, headline, premise, math, RESULTS label or CLAIM_MAP status is moved. THEORY.md, CLAIM_MAP and FRAMEWORK rule text are not edited here (PR #73 and PR #74 are already pending review on N6). Vigilance (H8) OPEN. Results are labelled by proxy.

## 1. Question
Pick 38 found that every locked N6 causal-form prereg **PASSes against zero** (`D − zσ > 0`) while it **FAILs against a kill line** (`D + zσ < κ_F·P`). A design whose true share lies below the kill line can still read PASS. This audit asks whether the same mismatch, or any other asymmetry that lets a result miss the locked prediction and still pass, is present in the other locked preregs and in the FRAMEWORK / THEORY kill rules.

## 2. Method
Every `PREREG.md` (and addendum) under `tests/`, `prereg/` and the locked reviews in `reviews/night2/` (`CAUSAL_NULL_INVARIANCE`, `KERNEL_PROXY_PREREG`, `STAKES_REFEREE/PREREG_EIV`, `SELF`, `TELEGRAPH_LINEAR_PREMISE`, `PRIORART_LFK_ALPHA`), plus `measurement/FRAMEWORK.md` MV10 and §6 and THEORY §1 N6 / §9, was read for its pass/fail (or HIT/MISS/KILL) rule. Decision code was read where it exists (`tests/KERNEL_MEASURE/decide.py`, `tests/ONSET_ACROSS_ALPHA/verdict.py`, `tools/power_gate.py`). Own checks (`PASS_RULE_SYMMETRY_AUDIT_checks/rules_mc.py`, no imports from any locked test package) and a report-only helper (`tools/pass_rule_symmetry.py`, tests in `tools/test_pass_rule_symmetry.py`) classify each family, run a quick Monte Carlo (nice 19, 20,000 reps, seed 20261115+183, known-σ normal CIs) of the wrong-pass rate, and re-read locked numbers under a stated mirror. Locked labels are not changed.

## 3. Inventory by family

### 3.1 Causal form (PASS vs 0, FAIL vs a share or floor) — **asymmetric**
The pick-38 pattern, as encoded in `tools/power_gate.py` and FRAMEWORK MV10, and as used by:

| Rule | File | Form |
|---|---|---|
| N6 causal form (`κ_F = ½`) | THEORY.md §1 N6 (FAIL wording); implemented in preregs | FAIL: move falls short of `κ_F` of P beyond error. PASS not stated in N6; preregs use `D − zσ > 0`. |
| LAB-AKLMT-TAU | `tests/LAB_AKLMT_TAU/PREREG.md` §3 | PASS iff `D − zσ > 0` and not FAIL; FAIL iff `D + zσ < 0.4918`. |
| CAUSAL-NULL-INVARIANCE | `reviews/night2/CAUSAL_NULL_INVARIANCE/PREREG.md` | Same, kill line `0.1752`. |
| STAKES-SHIFT-CAISO | `tests/STAKES_SHIFT_CAISO/PREREG.md` | PASS iff `D − 1.96 se_tot > 0` and `D ≤` band top `0.352`; FAIL iff `D + 1.96 se_tot < 0.05` (absolute ε, not `κ_F·P`). |

STAKES-SHIFT is the same qualitative split (PASS vs 0, FAIL vs a small positive floor), plus a band cap on PASS only. The locked contrast was already INCONCLUSIVE by gates (G0, G2); `D = −0.088`, `se_tot = 0.342`, so `D ± 1.96 se_tot = [−0.76, +0.58]`. A mirror PASS (`lo > 0.05`) would still be INCONCLUSIVE. MV10 was not met (PASS region empty).

PR #74 already proposes the causal-form mirror (`D − zσ > κ_F·P`; FAIL unchanged) and a matching MV10 PASS line. This audit does not reopen that wording.

### 3.2 HIT against zero, MISS against a magnitude floor — **asymmetric, same pattern**
| Rule | File | Form |
|---|---|---|
| C3b mechanism (primary) | `tests/C3b/PREREG.md` §6 | HIT iff H1 lo > 0 and H2 lo > 0 and S9 90% lo > 0; MISS iff H1 hi < 0.15 or H2 hi < 0. |
| C3 / F1 index | `tests/C3/PREREG.md` §5, `tests/F1/PREREG.md` §6 | HIT needs each slope's CI to exclude 0 (and ratio *points* in band, plus an interaction); MISS/K1c can fire when a CI excludes a theory-sized effect (`β_τ` upper < ½·`β̂_σ` in F1; ratio CI wholly outside its band). |
| DECISIVE banks | `tests/DECISIVE/banks/PREREG.md` | HIT: P1 CI excludes 0 on the positive side **and** P3 *point* > 0 (no CI). KILL only in the `z ≥ 1.5` subset: `β_τ ≤ 0` and upper < 0.2. |

C3b has no results file yet (stage 4 not run). C3 (literal prereg text) and F1 already read INCONCLUSIVE (no HIT, no kill). Banks read **HIT** on proxy, with P1 `+0.20 [0.11, 0.29]` and P3 `+0.05 [−0.03, 0.13]` (point only). A report-only floor-mirror that required P1 lo > 0.2 (the kill's size number, applied to the full sample) would not HIT. The 0.2 figure is not a uniquely mandated mirror — the kill is subset-restricted — but the HIT is a sign test plus a point condition, and a small positive effect cannot be killed.

### 3.3 Relative band: PASS on the point estimate — **asymmetric**
| Rule | File | Form |
|---|---|---|
| LEARNSIM exponent (each arm) | `tests/LEARNSIM/PREREG.md` §6; `PREREG_2.md` §3 | PASS iff `\|ê − e_pred\| ≤ 0.15\|e_pred\|`; MISS iff not and the 95% CI excludes `e_pred`. |
| LEARNSIM V at onset | `tests/LEARNSIM/PREREG.md` §6 | PASS iff the geometric-mean ratio `V̂/V_pred` is within ×/÷ 1.15; MISS iff outside and the CI excludes 1. |
| ONSET-ACROSS-ALPHA secondary (per α, never decides the primary) | `tests/ONSET_ACROSS_ALPHA/PREREG.md` §5 | Same 15% point rule. |

The PASS leg does not require the CI to lie inside the band. When the CI half-width exceeds the band, a point inside the band still PASSes, which is a closeness claim the interval cannot support (MV10's TOST / "PASS band wider than the CI half-width" would have called the lock exploratory or not met). A natural mirror is TOST: PASS iff the CI lies inside the same band; FAIL iff it lies wholly outside. At RA's locked SE (`0.136` on a 15% band of width `0.15` around −1) that TOST PASS is almost unreachable — which is the point: the locked rule can still say PASS.

### 3.4 ONSET primary extra FAIL condition — **not a "miss yet pass"**
`tests/ONSET_ACROSS_ALPHA/PREREG.md` §5 (and `verdict.py`): **PASS** iff the 95% CI of `Δ̂` lies inside `(Δ_pred ± δ)` with `δ = 0.267`. **FAIL** iff the CI excludes `Δ_pred` **and** `|Δ̂ − Δ_pred| ≥ δ/2`. Otherwise INCONCLUSIVE, including a CI that excludes `Δ_pred` with a small point miss (declared as discreteness, not a kill).

PASS is already a TOST against the named rival margin. The extra `|Δ̂| ≥ δ/2` is a FAIL-side buffer, not a PASS-side loophole: a result whose CI lies inside the band still PASSes first, and one that misses by enough to leave the band can be INCONCLUSIVE rather than FAIL when the point is close. At the locked SE (`0.051 ≪ δ/2 = 0.134`) the buffer is nearly inert (Monte Carlo, §4). The locked primary, `Δ = +0.013 [−0.072, +0.118]`, stays PASS under either FAIL rule. The secondary 15% rules for α = 1.5 and 2.5 stay PASS under TOST as well (those CIs do sit inside the 15% band).

### 3.5 Already-symmetric closeness rules
| Rule | File | Form | Asymmetric? |
|---|---|---|---|
| KERNEL-MEASURE design 2 | `tests/KERNEL_MEASURE/PREREG.md` §5, `decide.py` | PASS iff `\|D\| + 1.96 σ_D ≤ 0.13` **and** the CI of Ŵ21 excludes rivals 0.000, 0.012, 0.725; FAIL iff `\|D\| − 1.96 σ_D > 0.13`. | **No** on the band (TOST). Rival exclusion is required only for PASS, which is stricter on PASS, not more lenient. Low-resolution label if `σ_D > 0.040`. |
| KERNEL-PROXY P1 / P2 | `reviews/night2/KERNEL_PROXY_PREREG.md` | P1: same ±0.13 TOST plus rivals (exploratory; MV10 band not met). P2: SMALL iff `\|e\| + 1.96 sd ≤ 0.065`; DISTORTS iff `\|e\| − 1.96 sd > 0.065`; else UNRESOLVED. | **No.** |
| STAKES-REFEREE R-EIV | `reviews/night2/STAKES_REFEREE/PREREG_EIV.md` | PASS iff `r_night − 1.96 σ > m`; FAIL iff `r_night + 1.96 σ < m`, with `m = r_all / 2`. | **No** (already a midpoint / one-sided bound pair, the same shape as pick 38's proposed mirror). |

### 3.6 PASS if the CI *contains* the prediction — **asymmetric (consistency, not equivalence)**
| Rule | File | Form |
|---|---|---|
| SELF P2 | `reviews/night2/SELF/PREREG.md` | PASS iff the drift-elasticity CI includes 0.5 **and** excludes 0; FAIL iff the CI excludes 0.5. |
| LFK-SPF calibration | `tests/LFK_SPF/PREREG.md` §6 | PASS needs the calibration-slope CI to contain 1 and exclude 0 (and to beat two rivals); FAIL if the slope CI excludes 1 or a rival beats G. |
| STAKES-EXOGENOUS S2 | `tests/STAKES_EXOGENOUS/PREREG.md` | "Passed" if the 95% CI of `log(k_large/k_small)` contains 0. |
| DECISIVE glucose / populations HIT | `tests/DECISIVE/glucose/PREREG.md`, `populations/PREREG.md` | HIT iff the CI is entirely on the predicted side of 0 **and contains β\***. That *blocks* a miss from counting as a HIT. KILL: point closer to 0 than to β\* and CI excludes β\* (an intermediate SIGN-RIGHT, SIZE-OFF is named). |

SELF P2, LFK's slope and STAKES S2 can PASS (or "pass" as a component) when the interval is wide enough to include the predicted value even if the point is far from it. The pick-34 referee already called S2 uninformative (CI spanning a factor of ~20). Glucose/populations HIT is the opposite design (contains β\*, so a miss cannot HIT); the separate MATH_ATTACK "closer to 0 than to −1" literal rule is a different goalpost, already discussed in those RESULTS and in THEORY §8, not a within-rule PASS/FAIL split.

SELF P2 locked: `0.30 [−0.01, 0.60]`, **INCONCLUSIVE** (CI includes 0). That label is unchanged under the locked rule. LFK-SPF was INCONCLUSIVE (MV8 failed in the pre-lock dry run). STAKES-EXOGENOUS overall was INCONCLUSIVE (S1 half-width failed); S2's component "pass" would not survive a TOST against a tight band.

### 3.7 Sign-only rules — symmetric around 0; lenient only if a *magnitude* was the prediction
WIKIDATA P2/P3, LEARNSIM T3 (nonzero predicted Δ), VIGIL-ONA H1, and many FRAMEWORK §6 kills of the form "CI excludes 0 with the wrong sign" are ordinary sign tests: PASS and FAIL are mirrors about 0. They are the right rule when the locked prediction is a sign. They are the causal-form defect when the prediction is a share or a size and FAIL has a floor that PASS does not.

Exceptions worth naming: LEARNSIM T3 with predicted `Δ = 0` adds `|Δ| < 0.1` on PASS only. WIKIDATA P4 PASSes if the share of editions with `β_q > 0` is ≥ 5/6 (`k ≥ 4`) and FAILs if ≤ 0.5 (a gap, not a miss-yet-pass). WIKIDATA P1 is strict on PASS (CI > 0 *and* ΔAUC ≥ 0.02 with lo > 0). Locked P4 (4/4) stays PASS; P1 stays INCONCLUSIVE (`ΔAUC 0.024 [−0.005, 0.058]`).

### 3.8 Other locked rules (brief)
- **D3-OOS** (`tests/D3_OOS/PREREG.md`): P1/P2 are threshold rules on a point (declared non-discriminating); P3 is a per-repo shuffle test. Not a CI PASS/FAIL split. Locked P3 failed on proxy; P1/P2 passed as declared non-discriminating.
- **TELEGRAPH-LINEAR-PREMISE** (`reviews/night2/TELEGRAPH_LINEAR_PREMISE/PREREG.md` §5): in-model numerical bands (e.g. a slope in `[0.40, 0.60]·θ`). Closeness bands, not a causal PASS-vs-0 / FAIL-vs-floor pair.
- **PRIORART-LFK-ALPHA**: a document-search rule, not a statistical pass/fail.
- **ANTS1** (`tests/ANTS1/PREREG.md`): slope and interior-minimum bands; no `RESULTS.md` in that directory at this checkout, so outcomes were not re-scored here.
- **DRIFT1, C3b addenda, ONA-MORE**: shape or gate rules; C3b addendum A3 labels the mechanism verdict underpowered if stage 4 is run at the realized n, without moving the locked HIT/MISS text.
- **FRAMEWORK §6** fair-kill specifications mostly state *kills* (e.g. §6.3: pooled upper bound of `V_obs / floor < 0.8`; §6.6: `ΔAUC < 0.02` with CI including 0). They do not, in this file, define a matching PASS against the same line. No wording is proposed here; PR #74 already touches MV10's PASS line for the causal form.

## 4. Monte Carlo (own code, nice 19; `rules_mc.json`)
20,000 draws, `D ~ Normal(μ, σ)`, CI = `D ± 1.96σ` (known σ, matching the locked normal-CI rules), seed 20261115+183. Analytic Φ formulae for the causal family match the Monte Carlo to about 0.01 or better.

**Causal form, `κ_F = ½`, P = 1.** Wrong-pass = P(PASS | true share `r` is at or below the kill line). R0 = locked rule; R1 = pick 38's mirror.

| true r | SNR 5.6 R0 / R1 PASS | SNR 9.7 R0 / R1 | SNR 20 R0 / R1 |
|---|---|---|---|
| 0 (no move) | 0.025 / 0 | 0.002 / 0 | 0 / 0 |
| 0.40 (below `κ_F`) | **0.610 / 0.006** | **0.841 / 0.002** | **0.481 / 0** |
| 0.53 (AKLMT-like) | 0.843 / 0.039 | 0.987 / 0.051 | 0.994 / 0.088 |
| 1 (true design) | 1.00 / **0.800** | 1.00 / 0.998 | 1.00 / 1.00 |

This reproduces pick 38's finding with an independent, simpler design (known-σ draws rather than K = 30 through-origin OLS): at SNR 9.7, a share 0.40 is labelled PASS 84% of the time under R0 and 0.2% under R1; a true design still PASSes at the MV10 minimum about 80% of the time under R1. FAIL rates are essentially identical for R0 and R1 (same FAIL rule).

**HIT vs 0 / MISS vs 0.15** (C3b H1 shape; σ = 0.06). Wrong-pass = P(HIT | μ in (0, 0.15)).

| true μ | locked HIT / MISS | mirror (lo > 0.15) HIT / MISS |
|---|---|---|
| 0.05 | 0.132 / 0.385 | 0.000 / 0.380 |
| 0.10 | **0.379 / 0.133** | **0.003 / 0.130** |
| 0.15 | 0.707 / 0.027 | 0.026 / 0.027 |
| 0.25 | 0.987 / 0.000 | 0.383 / 0.000 |

Same qualitative leniency: a below-floor true effect HITs 13–38% of the time; the floor-mirror almost never HITs it. MISS rates are unchanged. At this σ a true effect of 0.25 often becomes INCONCLUSIVE under the mirror (lo = 0.25 − 1.96·0.06 = 0.13, just below 0.15); that is a power cost, not a change in the kill.

**Relative 15% band, pred = −1, σ = 0.136 (RA's locked SE).** Wrong-pass ≈ P(PASS | μ outside [−1.15, −0.85]).

| true μ | point-PASS / MISS | TOST PASS / FAIL |
|---|---|---|
| −1.00 (true) | 0.732 / 0.049 | 0 / 0.002 (rest INCONCLUSIVE) |
| −0.80 (outside the band) | **0.348 / 0.315** | 0 / 0.054 |
| −0.50 (far) | 0.005 / 0.957 | 0 / 0.724 |

TOST PASS is unreachable at this σ because `1.96σ = 0.267 > 0.15`: the CI is wider than the band, so a closeness PASS is not supported. The locked point rule still PASSes 73% when the prediction is true *and* 35% when the truth is already outside the band. That is the "miss yet pass" rate for this family.

**ONSET primary, `δ = 0.267`, σ = 0.051.** PASS rates under the locked rule and under a wholly-outside-the-band FAIL are the same to Monte Carlo error (PASS is already TOST). At `μ = 0`, P(PASS) = 0.999; at `μ = δ`, P(PASS) = 0.025 (false PASS of a rival-sized miss, the usual TOST type I at the margin). The extra `|Δ̂| ≥ δ/2` clause mainly converts some INCONCLUSIVE outcomes into FAILs when the CI pokes out of the band (at `μ = 0.20`, locked FAIL 0.736 vs TOST-fail FAIL 0.001). It is not a PASS-side loophole.

**SELF-style "CI includes 0.5 and excludes 0", σ = 0.20.** At true μ = 0.30 (40% below the prediction), P(PASS) = **0.316**. At the prediction, P(PASS) = 0.678 and P(FAIL) = 0.051 (the CI can exclude 0.5). A consistency test both lets misses pass and can false-fail a true design.

**KERNEL TOST, `δ = 0.13`, σ = 0.049** (the realized, exploratory resolution). At `μ = 0`, P(PASS) = 0.511 (exactly why the lock was labelled exploratory: `σ_D > 0.040`). At `μ = 0.20 > δ`, P(PASS) = 0.0002. No material wrong-pass once the truth is outside the band.

## 5. Report-only re-reads (locked labels stay unchanged)

| Locked result (stored label) | Under the locked rule, recomputed | Under the stated mirror |
|---|---|---|
| LAB-AKLMT-TAU Exp 1, **passed on proxy** "implied persistence of h = 1 lab forecasts, AKLMT Exp 1 (MTurk)" (`D = 0.518 ± 0.048`, lo 0.424 < 0.492) | PASS | **INCONCLUSIVE** (causal R1) |
| LAB-AKLMT-TAU Exp 3, report-only (`D = 0.629 ± 0.094`, lo 0.444 < 0.514) | PASS | **INCONCLUSIVE** (causal R1) |
| CAUSAL-NULL-INVARIANCE, **passed on proxy** "MSE-payoff-selected learners…, zero-crossing t_A on a Δ = 0.01 grid" (`D = 0.290 ± 0.029`, lo 0.233 > 0.175) | PASS | PASS |
| Same, reviewer 7-replicate mean `0.347 ± 0.012` | PASS | PASS |
| STAKES-SHIFT-CAISO, **INCONCLUSIVE on proxy** (also G0, G2) | INCONCLUSIVE | INCONCLUSIVE |
| LEARNSIM PREREG_2 RA, **PASS** (`−0.736 [−1.031, −0.520]` vs `−0.759`; 15% band `[−0.872, −0.645]`) | PASS | **INCONCLUSIVE** (TOST) |
| LEARNSIM PREREG_2 AA (known-groups), **PASS** (`−1.538 [−1.770, −1.331]` vs `−1.650`) | PASS | **INCONCLUSIVE** (TOST) |
| LEARNSIM PREREG_2 AR (already MV8-failed) | INCONCLUSIVE | INCONCLUSIVE |
| LEARNSIM V RR, **PASS** (ratio 1.011 `[0.852, 1.200]`, band `[0.870, 1.15]`) | PASS | **INCONCLUSIVE** (TOST) |
| LEARNSIM V RRh, **PASS** (1.058 `[0.890, 1.258]`) | PASS | **INCONCLUSIVE** (TOST) |
| ONSET-ACROSS-ALPHA primary, **passed in-model, on proxy** "learned reset-read pooling onset in simulated fBm worlds" | PASS | PASS (either FAIL rule) |
| ONSET secondary α = 1.5 and 2.5 | PASS | PASS (TOST) |
| KERNEL-MEASURE primary, **passed on proxy**, exploratory | PASS | PASS (already TOST) |
| KERNEL-PROXY P1, **passed on proxy**, exploratory | PASS | PASS |
| STAKES-REFEREE R-EIV, **passed on proxy** "CAISO night-hour k_lin…" | PASS | PASS (already a midpoint rule) |
| DECISIVE banks, **HIT** (P1 `+0.20 [0.11, 0.29]`, P3 point > 0) | HIT (sign + point) | **INCONCLUSIVE** *if* HIT is re-read as lo > 0.2 (report-only; not a locked rule) |
| C3 (literal text), F1 | INCONCLUSIVE | INCONCLUSIVE |
| SELF P2 | INCONCLUSIVE | INCONCLUSIVE |
| STAKES-EXOGENOUS overall | INCONCLUSIVE | INCONCLUSIVE |

T1.8 ("the level's class sets the exponent") stays **NOT PASSED**: it already required AR and RA both to PASS, and AR missed MV8. The RA arm's own PASS, and the AA known-groups PASS, would read INCONCLUSIVE under TOST. Class-R vigilance at onset (V RR / RRh) would also read INCONCLUSIVE under a CI-inside-band mirror. Those are report-only re-reads of in-model labels; CLAIM_MAP G26/G27 are not moved here.

## 6. Recommendations (queue items only)
1. **Causal form / MV10 / N6.** Already proposed in pick 38 and sitting in **PR #74** (THEORY v1.4.17 / FRAMEWORK MV10 PASS line), pending a separate reviewer (CAUSAL-KAPPA-LENIENCY-REVIEW). Nothing further is added to N6 here. PR #73 (loss-lock, also N6) remains the other pending review.
2. **New item RELATIVE-BAND-TOST.** Future relative-band and ×/÷ locks (LEARNSIM 15%, V 1.15, and any copy) should PASS only when the CI lies inside the band (TOST), and should meet MV10's "PASS band wider than the CI half-width" before they are decisive. Locked labels stay as stored; the report-only re-reads are in §5.
3. **New item HIT-ZERO-MISS-FLOOR.** Future HIT/MISS rules of the C3b/F1/banks shape should not HIT against 0 while they MISS against a magnitude floor, and should not let a point-only side condition (banks P3) decide a HIT. C3 and F1 labels are already INCONCLUSIVE; C3b is not yet run; banks is a report-only re-read only. No FRAMEWORK §6 wording is drafted here (that would want its own author-only PR after this item).

No THEORY, CLAIM_MAP status, or FRAMEWORK rule text is changed in this pick.

## 7. Limits
The Monte Carlo uses known-σ normal CIs, not every prereg's bootstrap or Cox clustering; it is a check of the *decision rule*, not a re-analysis of any dataset. ANTS1 outcomes were not re-scored (no `RESULTS.md` in `tests/ANTS1` at this checkout). Fair-kill text in FRAMEWORK §6 is inventoried, not rewritten. Usage was kept lean (no new data fetches, no long jobs).

## 8. Surprise (rule 4)
**Moderate, confirmatory of pick 38, and broader than the causal form.** The same PASS-against-zero / FAIL-against-a-floor split lives in the C3b/F1/banks HIT–MISS family. A different, also material, split lives in the relative-band family: PASS is decided by the point estimate, so an in-model PASS can be a closeness claim the CI cannot support (LEARNSIM RA, AA, V RR, V RRh). KERNEL, KERNEL-PROXY and the EIV midpoint rule are already symmetric. ONSET's primary contrast is already TOST on PASS. Vigilance stays OPEN.

