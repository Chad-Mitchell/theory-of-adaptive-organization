# PREREG_CAP: admissible precision and turnover

Written Sunday 22 November 2026, after the hostile review of draft PR #191 and before any evaluation of the grid below. `PREREG.md` and `ADDENDUM.md` are not edited. This file does not rescore P1–P11. P1 stays **FAILS** at the frozen cap \(c = 1/2\), as a puzzle whose diagnosis is the coupling of quality to heat. `THEORY.md`, `CORE.md`, and `README.md` are not edited. The hypothesis sentence is unchanged.

## Disclosed prior knowledge

The scored run already printed, and the review repeated: identical units at precision \(1/2\) and rate \(1\) have official cost \(15.473978\) and ruin probability \(0.020940\), against the inadmissible zero at cost \(16\). The mean-field cost of that same pair, printed on the identical-unit grid, is \(15.3972245773\). The review's diagnostic, which is not a score of this file, reported a mean-field cost \(14.408952\) at precision \(1/4\) and rate \(2\), with a ruin probability about \(0.024\) on \(120000\) draws, and a fixed-heat admissible cost about \(16.17\). Those diagnostics are not copied onto this grid as results. No pair \((c, \sigma)\) in the script of this file has been evaluated.

## Class

The class is AF in `PREREG.md` §1, with three changes of menu and none of price.

The installed precision \(c > 0\) is a coordinate of the grid, not the single frozen value \(1/2\). The turnover rate \(\sigma \ge 0\) is the other coordinate. Drift \(\delta = 1\), \(kT = a = 1\), \(v = 4\), \(n = 4\), \(h = 1/2\), \(w = 3/2\), \(b = 1/2\), \(m = 1/4\), \(\pi = 1/2\), \(q_H = 1\), \(q_L = 1/4\), \(\eta = 0\) on the heterogeneous arms, \(\varepsilon_{\mathrm{cap}} = 3/2\), \(\varepsilon_r = 1/20\). Those prices stay where the first run froze them.

**Locked coupling.** A living unit of quality \(q\) pays heat \(kT\, a\, v\, c\, q\) and, on replacement, stock \(\tfrac12\log(1 + v\, c\, q_{\mathrm{new}})\). Effective precision is \(c\, q\, \alpha\).

**Fixed heat.** Every living unit pays heat \(kT\, a\, v\, c\), and every replacement pays stock \(\tfrac12\log(1 + v\, c)\), whatever \(q\) is. Quality scales the aim, \(c\, q\, \alpha\), and the hazard \(\lambda(q)\), and nothing else in the cost.

Identical units have \(q = 1\). On that arm the two pricings are the same formula. A code that gives them different costs at any identical-unit grid point is invalid, and no question is scored.

Heterogeneous units use R-select from `PREREG.md` §1. The birth-death rates do not depend on \(c\) or on which pricing is used. The stationary type law is computed once, at any positive rate.

At rate \(0\) and \(\delta > 0\), alignment is \(0\), the error is \(4\), and the build rate is \(0\).

## Grid

Frozen before evaluation. Precision
\[
c \in \left\{\tfrac{1}{10},\ \tfrac{1}{8},\ \tfrac{1}{6},\ \tfrac{1}{5},\ \tfrac{1}{4},\ \tfrac{3}{10},\ \tfrac{3}{8},\ \tfrac{1}{2},\ \tfrac{5}{8},\ \tfrac{3}{4},\ 1\right\}.
\]
Rate, the same menu as the first preregistration,
\[
\sigma \in \{0,\ 0.05,\ 0.1,\ 0.15,\ 0.2,\ 0.3,\ 0.4,\ 0.5,\ 0.7,\ 1,\ 1.5,\ 2,\ 3,\ 4,\ 6,\ 8,\ 12,\ 20\}.
\]
The point \(c = 1/10\) lies below \(5/48\). Four fully aligned units at the A14 precision \(0.093750\) pool to \(0.375\), and the cap requires pool \(5/12\). The grid reaches above \(5/48\) so a precision that cannot meet the cap is not the only menu. No precision and no rate are added after the first printed table.

## Admissibility, and what is not a pass

A draw ruins when its error exceeds \(3/2\), which is pool \(\Phi < 5/12\). Official ruin probability is the fraction of \(M = 50000\) draws. A grid point is admissible when that fraction is at most \(1/20\). Equality is admissible.

Monte Carlo: NumPy Generator, PCG64. Arm seeds \(20261130\) (identical), \(20261131\) (heterogeneous, locked coupling), \(20261132\) (heterogeneous, fixed heat). One matrix of uniforms per arm, shared across every \((c, \sigma)\). Heat, upkeep, and build rate are the exact stationary values. Official cost is those three plus \(w\) times the sample mean of the error.

**An unconstrained interior minimum whose ruin probability is above \(1/20\) is not a pass.** It may be printed. It does not answer Q1, Q2, or Q3. A point that is cheapest only because every cheaper point is inadmissible is the admissible argmin, and it is the object those questions score.

## Questions

Reference R, already printed, not recomputed as a new claim: precision \(1/2\), rate \(1\), mean-field cost \(15.3972245773\), official cost \(15.473978\), ruin probability \(0.020940\).

**Validity.** At that pair the new mean-field code matches \(15.3972245773\) within \(10^{-9}\). If it does not, the run stops and no question is scored.

**Q1.** On the identical-unit arm, does any admissible pair have mean-field cost strictly below \(15.3972245773\)? Does any admissible pair have official cost strictly below \(15.473978\), by more than twice the paired standard error of the gap against the same-stream point \((1/2,\ 1)\)? Each accounting is its own answer. A pair that fails admissibility does not count, whatever its cost.

**Q2.** Heterogeneous units, locked coupling. The admissible argmin is the admissible grid point of lowest official cost, and, separately, the admissible grid point of lowest mean-field cost. Report both, with their ruin probabilities. Compare each official cost with \(15.473978\) and with the zero-shock cost at the same precision. The zero-shock point is a reference. It is not admissible.

**Q3.** The same report under fixed heat.

No sign is predicted for Q2 or Q3. The heat term and the loss term move differently when quality changes, and this file does not assert which wins inside the cap.

## What the computation may be

One script, `theory/antifragility_checks/cap_checks.py`, written after this file is committed and after `LOCK_CAP.txt` records the hash of this file. The script prints the three grids, the validity check, and Q1–Q3. It does not search a precision or a rate outside the menus above.
