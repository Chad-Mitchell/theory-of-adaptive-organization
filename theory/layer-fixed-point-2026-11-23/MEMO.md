# MEMO: CT34 nesting fixed point

*24 November 2026. The claim is a **CONJECTURE**. `THEORY.md` is not edited. Nothing here is compared to a measured physical constant.*

## Why this approach

The conjecture, `MIRROR_MEMO.md` §6 on `ace-probe-memos-2026-11-23` at `e3e0e701` (not merged; the review leaves the row **CONJECTURE, untested**), is that a fixed point of CT34 nesting would be a dimensionless number in the sense of Feigenbaum's δ. The clock-term onsets 4 and 6 are scale-symmetry onsets, a different mechanism, and are contrast only.

CT34 (`THEORY.md` line 497) is partial minimization: the parent's problem is \(F(x)\) plus the team's optimized cost. The dyadic reading, declared as the period-doubling analogue and not as a theorem, adds the same scalar cost at the parent's time and at that time divided by \(b\). The scalar cost is CT22 (`THEORY.md` line 442): \(J=c/\tau+\alpha\tau\) with \(\alpha=w\sigma^2/2\). Currency and time are removed by the argmin and by dividing by the minimum, which is the operator in `PREREG.md` §1. Lemma A of that file says every \(At+B/t\) is sent to \(t+1/t\) in one step, so a number has to live off that family. Three Rayleigh quotients are the smallest set that can tell one rate from a menu. The unit and choice gate then refuses a candidate that moves when the units are stretched or when \(b\), the mode, the window, or the cap is swapped.

## What was learned

No number is yielded. The locked cell is **MODE_DEPENDENT**. The unit and choice gate is **FAIL_CHOICE**.

The candidate a SUPPORT cell would have quoted, the mean of the three slack quotients at \(b=2\), is 1.20021282055. Stretching cost and time together by 4 moves it by \(1.9\times 10^{-13}\). Swapping \(b=2\) for \(b=3\) moves it by 4.022. The three deformations at \(b=2\) spread by 3.352. The other fit window moves it by 0.0042, and the two caps move it by \(4\times 10^{-6}\), both inside the locked tolerance 0.02. The raw minimizer and the raw minimum are not invariant: \(t_0\) goes from 1.41421356237 to 0.353553390593, and \(F_0\) goes from 4.24264068712 to 16.9705627485, each by the factor the stretch puts in. The gate fires on those, and it fires on the candidate because of \(b\) and the mode.

**Result.** This operator does not produce one dimensionless number from the cost alone.

**Hand account, written after run 1, not a yield.** On a pure log-mode \(t^k+t^{-k}\), the slack operator multiplies that mode's coefficient by \(\cosh(k\ln(b)/2)/\cosh(\ln(b)/2)\) and then normalizes. For \(b=2\) the factor is \(3/2\) on mode 3 and \(11/4\) on mode 5. The printed quotients sit slightly below those factors because a finite window overlaps the gauge mode \(t+1/t\). Swapping \(b\) or the mode changes the factor. Quoting \(3/2\) or \(11/4\) would fail the choice arm, so neither is reported as the number. **Model implication:** the dependence is structural, and it is carried by the nesting ratio and the mode order, both choices. This is the reading Ace's working conjecture allows (a structural fact, not a constant). One operator does not establish that conjecture.

Prior odds, a judgment in `PREREG.md` §0 and not a result: about 1 in 10 of SUPPORT. The cell was not SUPPORT.

## Results

| Check | Value | Outcome |
|---|---|---|
| S1, \(\max\|Tf_*-f_*\|\) | \(1.78\times 10^{-15}\) | pass |
| S2, family residual | \(\le 2.7\times 10^{-15}\) | pass |
| Lemma B, \(F_0\) at \(b=2\) | 4.24264068712 \(= 3\sqrt{2}\) | pass |
| Cell | mode spread 3.35211337112 | MODE_DEPENDENT |
| \(\rho\), \(b=2\), \(\varphi_1,\varphi_2,\varphi_3\) | 1.45735693345, 2.74769744966, \(-0.604415921464\) | not one number |
| Same, \(s=10^{-5}\) | 1.45755367369, 2.74837748607, \(-0.604438662292\) | agrees inside 0.02 |
| Same, window \((3,96)\) | mean 1.20445021574 against 1.20021282055 | inside 0.02 |
| \(b=3\), same three | 2.26681080169, 6.76937700018, \(-0.398452155647\) | choice arm fails |
| Cap \(q=0.5\) and \(q=2\) | mean move \(4.4\times 10^{-6}\) | inside 0.02 |
| Unit stretch \((\mu,\gamma)=(4,4)\) | mean move \(1.9\times 10^{-13}\) | unit arm passes |
| Raw \(t_0\), \(F_0\) under that stretch | 0.353553390593, 16.9705627485 | gate fires |
| Gate | | FAIL_CHOICE, yielded none |

\(b=3\) is not part of the locked cell. It is part of the choice arm.

## Checkpoints

**1. Before any run** (`PREREG.md` §4, not rewritten). Still the right question: yes, an eigenvalue, not an EOQ share. Not built in: normalization is currency and time, \(b=3\) cannot flip the cell, a window-moving \(\rho\) is CUTOFF. Cheaper test: Lemma A is S2; three quotients are the minimum that separate one number from mode-dependent rates.

**2. After run 1, before the unit arm.** Still the right question: yes. The cell says the three rates disagree, and the open point is whether any one of them is forced by the cost rather than by a choice. Not built in: \(b=2\) was put in as the doubling analogue, so a rate that exists only at \(b=2\) is not a yield. Cheaper: the \(b\) and mode comparisons were already printed; the new work is the unit stretch.

**3. At the end.** Still the right question: the conjecture asked for one number, and on this operator the gate says there is none. Not built in: the gate was committed before the unit arm, and no quotient was picked after the fact. Cheaper: another operator, built so that \(b\) or the mode cancels, would be a search for a number the gate would reject unless the cancellation were forced. That search is not the next cheap step.

## Deviations

- Run 1 was executed before `PREREG_ADDENDUM.md` and before `PREREG_ADDENDUM_2.md`. The locked predictions were not edited. The choice arm reads the run 1 record. The unit arm ran after addendum 2 was committed (`8977f8f`).
- Comparing function values cannot place this minimum to the locked \(10^{-12}\): the curvature is below double precision. The argmin is finished by Newton on a complex-step derivative. That is the same critical point, not a different operator.
- A golden section that crosses the feasible boundary can leave the feasible set. The binding polish is restricted to the feasible run the scan found. That is the argmin the operator names.
- `mean` had to take a list. The scorer returned early while S1 was failing, so the bug showed up only after the argmin was accurate enough for S1 to pass.

## Files

`PREREG.md`, `PREREG_ADDENDUM.md`, `PREREG_ADDENDUM_2.md`, `criteria.json`, `crossref.out`, `nest_map.py`, `nest_map.out`, `unit_choice_gate.py`, `unit_choice_gate.out`, `RUN_LOG.md`.
