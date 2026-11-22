# Admissible precision and turnover

*Sunday 22 November 2026. In-model. A self-check, not an independent review. Preregistration `44c5f9978dc00a03f432c04e2b609e899cd46852`, hash lock `32e92e5f1450bd35907df5bf8938526f8a99cdce`, both before this computation. `PREREG.md`, `ADDENDUM.md`, and `PREREG_CAP.md` are not edited. `THEORY.md`, `CORE.md`, and `README.md` are not edited. The hypothesis sentence is unchanged.*

Checks: `theory/antifragility_checks/cap_checks.py`, run at `nice -n 19`. Machinery FAILS 0. The grid is the one locked in `PREREG_CAP.md`. A point with ruin probability above \(1/20\) is not a pass.

## The answer

Yes. On identical units, admissible pairs beat precision \(1/2\) at rate \(1\). The lowest official cost is precision \(3/10\) at rate \(1.5\): cost \(13.7551074206\), ruin probability \(0.030240\), mean-field cost \(13.7117638337\). The recorded reference is official cost \(15.473978\) and mean-field cost \(15.3972245773\). The same-stream reference, a different seed, is official cost \(15.4708445545\), ruin probability \(0.019200\). The gap from the new point to that same-stream point is \(1.715737\), paired standard error \(0.000353\).

Four admissible pairs sit strictly below the recorded reference on both accountings: \((3/10,\ 1.5)\), \((1/4,\ 2)\), \((3/8,\ 1.5)\), and \((3/10,\ 2)\). Precision \(1/4\) at rate \(2\), the pair a diagnostic had named, is on this grid: mean-field cost \(14.4089523586\), official cost \(14.4368692815\), ruin probability \(0.022500\). It is admissible and it is not the cheapest.

The unconstrained minima of all three arms sit at precision \(1/10\), ruin probability \(1\). Those points are not a pass.

## Q1. Identical units

**Answered yes** on the mean-field cost and **answered yes** on the official cost.

| precision | rate | mean-field cost | official cost | ruin probability |
|---|---|---|---|---|
| \(3/10\) | \(1.5\) | \(13.7117638337\) | \(13.7551074206\) | \(0.030240\) |
| \(1/4\) | \(2\) | \(14.4089523586\) | \(14.4368692815\) | \(0.022500\) |
| \(3/8\) | \(1.5\) | \(15.0532200217\) | \(15.0944714729\) | \(0.008160\) |
| \(3/10\) | \(2\) | \(15.3824008700\) | \(15.4094313748\) | \(0.005620\) |
| \(1/2\) | \(1\) | \(15.3972245773\) | \(15.4708445545\) | \(0.019200\) |

The last row is the reference pair, recomputed on this stream. It does not count as a pair that beats itself.

Validity: the mean-field code returns \(15.3972245773\) at precision \(1/2\) and rate \(1\). Locked coupling and fixed heat agree on identical units, maximum gap \(0\).

## Q2. Heterogeneous units, locked coupling

Admissible official argmin: precision \(3/8\), rate \(1.5\), cost \(15.4328226573\), ruin probability \(0.018480\). That is \(0.041155\) below the recorded identical-unit official cost \(15.473978\), and \(3.682823\) above the inadmissible zero-shock cost at the same precision. The zero has ruin probability \(1\).

Admissible mean-field argmin: the same pair, cost \(15.3813092872\), which is \(0.015915\) below \(15.3972245773\), and \(3.631309\) above its own zero-shock mean-field cost.

No sign was predicted. The admissible point is below the identical-unit reference and above its own inadmissible zero.

## Q3. Heterogeneous units, fixed heat

Admissible official argmin: precision \(1/4\), rate \(2\), cost \(15.5593525440\), ruin probability \(0.049900\). That is \(0.085375\) above \(15.473978\), and \(3.559353\) above its own inadmissible zero.

Admissible mean-field argmin: the same pair, cost \(15.5188578966\), which is \(0.121633\) above \(15.3972245773\).

Quality here scales aim and hazard only. Every unit pays the heat of the installed precision. At the admissible argmin the cost is above the identical-unit reference.

## What was not a pass

| arm | unconstrained official minimum | ruin probability |
|---|---|---|
| identical | precision \(1/10\), rate \(0.4\), cost \(8.8865107737\) | \(1\) |
| locked coupling | precision \(1/10\), rate \(0.3\), cost \(8.9464626764\) | \(1\) |
| fixed heat | precision \(1/10\), rate \(0.3\), cost \(9.0462798753\) | \(1\) |

Each of these is cheaper than every admissible point and is outside the cap. The preregistration barred them.

## Checks

`cap_checks.py`. Machinery FAILS 0. Run at `nice -n 19`. The full grid is `cap_results.out`.
