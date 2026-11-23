# Preregistration: cubic ordering under feedback heat

Sunday 22 November 2026. This file is the protocol. It does not contain the costs, the gains the grid selects, or the numerical value of the linear bath rate. A later script may only carry out this protocol.

The prediction is an ordering on a cubic plant. It is not an evaluation of Lemma LG in `theory/ACTING_DERIVATION_2026-11-22.md`. That lemma is the validity gate for the path estimator. The parent of this commit already contains the lemma and `closed_rates` in `acting_derivation_checks.py`. This file does not copy the formula.

## 1. Plant

Parameters, all equal to 1: linear coefficient, cubic coefficient, feedback strength \(b\), memory rate \(\gamma\), coupling \(c\), diffusion coefficients \(D\) and \(D_M\), stake on \(X^2\).

Cubic drift, for each gain \(K\) on the grid:

\[
\begin{aligned}
dX &= (-X - X^3 - b K M)\,dt + \sqrt{2D}\,dW_X,\\
dM &= (-\gamma M + \gamma c X)\,dt + \sqrt{2 D_M}\,dW_M.
\end{aligned}
\]

The partial derivative of the \(X\) drift with respect to \(X\) is \(-(1+3X^2)\). The partial derivative of the \(M\) drift with respect to \(M\) is \(-\gamma\).

## 2. Costs

Euler–Maruyama, left-point drift, step \(dt=0.0002\). Initial state \((X,M)=(0,0)\). Discard the first \(40\) time units. Record the next \(800\) time units. One trajectory per gain.

At each recorded state, before the update,

\[
\begin{aligned}
\mathrm{Sr}_X &= \mathrm{mean}(F_X^2 + D\,\partial_X F_X)/D,\\
\mathrm{Sr}_M &= \mathrm{mean}(F_M^2 + D_M\,\partial_M F_M)/D_M.
\end{aligned}
\]

\[
J_E = \mathrm{mean}(X^2), \qquad J_H = \mathrm{mean}(X^2) + \mathrm{Sr}_X + \mathrm{Sr}_M.
\]

\(J_E\) omits a heat that does not depend on \(K\). Adding the same constant at every grid point would not move its argmin. No such constant is added, and no \(K\)-dependent exogenous formula is added.

Grid, in this order, indices \(0\) through \(8\):

\[
0,\ 0.25,\ 0.5,\ 0.75,\ 1,\ 1.5,\ 2,\ 3,\ 4.
\]

NumPy `Generator(PCG64(20261122 + index))`. Each step draws two standard normals, \(X\) then \(M\). Float64.

\(K_E\) is the grid gain with the smallest \(J_E\). \(K_H\) is the grid gain with the smallest \(J_H\). If two means compare equal, the smaller gain is taken.

## 3. Linear gate

Same integrator, same step, same lengths, same seed rule with index \(0\), at \(K=1\), on the linear plant whose \(X\) drift is \(-X-bKM\) and whose \(\partial_X F_X\) is \(-1\). The memory equation is unchanged.

Let \(\mathrm{Sr}_{\mathrm{LG}}\) be \(\mathrm{Sr}_X+\mathrm{Sr}_M\) from Lemma LG at these parameters, through `closed_rates` in the parent. The gate holds when

\[
|\widehat{\mathrm{Sr}}-\mathrm{Sr}_{\mathrm{LG}}| / |\mathrm{Sr}_{\mathrm{LG}}| \le 0.05.
\]

## 4. Prediction and miss rule

**Prediction.** The gate holds, and \(K_E - K_H \ge 0.25\).

**Met.** Both parts hold.

**Miss.** The gate holds and \(K_E - K_H < 0.25\), which includes an equal pair and a reversal.

**Measurement puzzle.** The gate does not hold. The cubic ordering is reported beside it and is not scored as met.

The tolerance \(0.25\) is one step of the fine part of the grid. It was chosen because it is the smallest strict separation that grid can show. It was not chosen by running the cubic plant.
