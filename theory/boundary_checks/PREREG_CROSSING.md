# Preregistration: log-linear crossing of the conditional radius

*Sunday 22 November 2026. Locked before any evaluation of \(\Delta(r)\) at the times named below. `theory/boundary_checks/PREREG.md` is not edited. The check that prints these crossings is not in this commit.*

The integer \(5\%\) radius on the path of \(31\) and the path of \(61\), at \(\tau=1/2\) and \(\tau=1\), was \(2\) at both times. That pair is not recomputed here, and it is not the prediction. A crossing that sits near \(1.05\), doubled, would pass \(2\) and the integer radius would become \(3\). The integer bin on \((1/2,1)\) hid \(\sqrt{2}\). It does not show that a factor \(2\) is invisible. This file asks the continuous crossing, on a different time pair, whether the radius scales with the square root of the time ratio.

The hypothesis sentence is unchanged:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. Definition

Path of \(n=61\) sites, indices \(0,\ldots,60\), center \(30\). Precision \(Q=I+L\) with \(L\) the open-path combinatorial Laplacian, the same field as class B. Present \(X\sim N(0,Q^{-1})\). Let \(w\) be row \(30\) of \(e^{-\tau Q}\). For integer \(r=0,1,\ldots,30\),

\[
\Delta(r)=\operatorname{Var}(w\cdot X\mid X_{\{|i-30|\le r\}}).
\]

Times \(\tau_a=1/4\) and \(\tau_b=1\). The time ratio is \(4\). This pair is not \((1/2,1)\).

Let \(\rho(r)=\Delta(r)/\Delta(0)\). The log-linear crossing of level \(0.05\) is the first integer \(k\ge 0\) with \(\rho(k)\ge 0.05>\rho(k+1)\), and

\[
r_\star=k+\frac{\ln\rho(k)-\ln 0.05}{\ln\rho(k)-\ln\rho(k+1)}.
\]

Natural log. The same formula at both times.

## 2. Prediction

\[
\frac{r_\star(1)}{r_\star(1/4)}=2,
\]

the square root of the time ratio. A pass is a ratio in \([1.7,2.3]\), which is a relative error of at most \(0.15\). The code prints both crossings and the ratio to twelve digits. It does not print a fitted exponent in place of this target.

Both crossings must exist, with \(0\le k\le 28\) so that \(k+1\) is on the path. \(\Delta(30)=0\) is the full conditioning and is not the crossing.

## 3. What a miss is

If either crossing is missing, or the ratio lies outside \([1.7,2.3]\), the square-root reading is a puzzle. The script does not fail on that miss. The next test, not run in this lock, is the same definition at times \(1\) and \(4\), on a path of \(121\) sites, center \(60\). The target there is again the square root of the time ratio, which is \(2\).

The integer radii are not a target. A factor-\(2\) move of a crossing near \(1.05\) would change an integer. This file scores the continuous crossing.

No line here is an AdS/CFT statement or a black-hole entropy.
