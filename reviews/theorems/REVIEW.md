# REVIEW of THEOREMS.md (skeptical-physicist pass)

Date: Friday 2026-11-13, about 2:50 PM ET.

**Independence: NOT independent.** This pass was done by the same executor that wrote THEOREMS.md. It was a separate, adversarial reread, with every number re-derived from `checks/check_all.out`. No tool for launching a separate reviewer was available in this run.

Chad's standing rule is that graders must be independent and blind, with no self-grading, and this pass does not meet that rule. **Before any public use, an independent reviewer should redo this review**, ideally someone trained in statistical physics.

## Framing used
"I am a statistical physicist who suspects this is relabeled operations research dressed up as physics. Show me (1) every place physics language outruns physics content, (2) every claimed theorem that is really a definition or an identity, (3) every result presented as new that is in a textbook, and (4) every number I cannot reproduce."

## Findings and fixes

| # | Finding | Severity | Fix applied |
|---|---|---|---|
| R1 | T3a called the nested cost an "upper bound" while assuming that one fact's check reveals the driver. If the driver is seen only through the facts, residual errors contaminate the driver check, so it is not a bound | Math error | Added the assumption that the driver is readable from its own source at cost c_g, and said explicitly that without it the expression is an approximation, not a bound |
| R2 | T7c invoked α-stable closure while talking about variance, which is infinite for α < 2 | Imprecise | Restricted the variance statement to the Gaussian case; noted the scale grows as n^{1/α} and that the quadratic cost must change |
| R3 | T9: Kuramoto is a gradient flow only for identical frequencies, in the co-rotating frame. With distinct ω it is a gradient flow on ℝᴺ, not on the torus | Imprecise | Qualified |
| R4 | T6: the per-step equality is near-definitional once F_neq is defined. A physicist will say this, so it should not be sold as deep | Framing | Already stated; kept |
| R5 | T6 and the theory: Looper acts back on its "signal" (the person), which violates Still et al.'s no-feedback condition, so the theorem does not cover the very system the theory is about | Important limit | Already stated in T6(b); Sagawa–Ueda named as the relevant framework; marked as not worked through |
| R6 | "Fractal" (T7) could read as proved. It is proved only conditionally, and the conditions are about the world | Overclaim risk | The bottom line and T7 both say the unconditional claim fails and that the architecture inherits the world's scale structure |
| R7 | T3 as a whole: "nested beats flat when time scales separate" is not one theorem | Overclaim risk | The section opens by saying so; T3c is labeled NUMERIC |
| R8 | Novelty: T3a (compression threshold) may exist in hierarchical forecasting (top-down vs bottom-up reconciliation), multi-echelon inventory or factor-model monitoring. Not searched thoroughly | Novelty uncertain | Labeled NEW? with "may well be known"; recommend a literature search before claiming |
| R9 | T2b (escalation) is a one-line substitution into EOQ. Calling it new is generous | Novelty | Labeled NEW? (elementary) |
| R10 | T7b's equal-width optimality and the K\* formula are in the spirit of Roundy and the power-of-two literature, and may be published | Novelty | Labeled "Roundy-type, known in substance" |
| R11 | Every number re-checked against `check_all.out`: T1 Monte Carlo (≤ 3%), T1c (1.0617 / 1.7584), T3a N\* values, T3b savings, T3c table, T4 exponents, T5 f\* values, T6 to 6 decimals, T7 1.0201 / 0.0607, T8 thresholds | — | All match |
| R12 | Torus: claims that vortex rings are energy *maxima* (Benjamin 1976) and the statement of Arnold's structure theorem were verified this pass by search. Taylor/Woltjer, Poincaré–Hopf and Liouville–Arnold/KAM are standard, not re-verified | — | Kept; sources named |
| R13 | Physics vocabulary: "temperature" appears only as σ√τ/B, explicitly not physical. No claim that systems minimize energy or free energy; no information = energy. Landauer and Still are the only physics, and both are stated with their conditions | — | Consistent with the prior withdrawals (H17; energy-minimization wording) |

## What a physicist would still object to (unresolved)
1. **Most of this is operations research and estimation theory, not physics.** The honest headline is "cost-efficient memory design follows EOQ/Kalman-type rules at every level". The physics enters only through Still et al. and Landauer, and only for physical systems.
2. **No result is tested on real data.** Every check here is internal consistency: algebra, toy simulations and textbook limits.
3. **The model class is narrow:** quadratic loss, random-walk drift and perfect checks. Fat tails, reflexive drift and non-stationary rates change the exponents (DRIFT_MATCHING §6).

## Verdict
The mathematics is correct within its stated assumptions, after fixes R1-R3. The novelty is modest and partly unconfirmed. The torus section correctly separates real mathematics from analogy. **Safe to share only as "known results assembled, with a few elementary new conditions", and only after an independent review.**
