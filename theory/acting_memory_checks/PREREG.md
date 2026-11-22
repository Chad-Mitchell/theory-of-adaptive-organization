# PREREG: memories that probe, and when volatility lowers the cost

Written Sunday 22 November 2026, before any script in this directory and before any numerical evaluation of the costs below. The only file this commit adds is this preregistration. No grid minimum, no decimal expansion of a closed form, and no tail probability is recorded here. The algebra that pins a prediction is part of the lock. A later script may only evaluate it.

The hypothesis under test is a hypothesis, not a specification. Antifragility, read as an expected cost that falls as environmental volatility rises, arises exactly when two things hold: (a) each probe has a capped cost, and (b) the probe carries information about the drifting world, so the learning rate rises with volatility. If that information's value grows faster in volatility than the heat plus the losses, the cost falls (and, on this wording, the cost is then concave in volatility, so the payoff is convex). Without (a) or without (b), the system is fragile or robust and is not antifragile. The capped downside with an open upside is optionality in Taleb's sense.

`theory/ROBUSTNESS.md` §6 already applies Taleb and Douady's convexity definition to this cost: a cost concave in the stressor gains from variation in the stressor, and, with the error affine in the volatility scale, a higher level of that scale does not lower the best cost (R4(a), CT40). Draft PR #191, which is not merged and is not recomputed here, found an interior minimum for identical units only through realignment, and found that its heterogeneous arm did not lower the cost, because a failure carried no information about the world beyond the precision already charged as heat. This file does not edit those results. It changes the question from the shock rate to the volatility, and it gives the probe a channel.

This is an in-model check. It does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not change the hypothesis sentence. T43 is reserved for #191. This work does not use that number.

## 1. Two definitions, scored separately

The stressor is the stationary variance \(\theta\) of one exogenous equilibrium Ornstein–Uhlenbeck signal. It is not a shock added to a payoff, and it is not the reversion \(a\).

- **Level.** A cost is level-antifragile on an interval when it is strictly decreasing there. More volatility then lowers the expected cost.
- **Variation.** A cost is variation-antifragile at a point when it is strictly concave there. This is the repository's reading of Taleb and Douady: the payoff is convex in the stressor, so a mean-preserving spread of \(\theta\) lowers the expected cost. A cost that is strictly convex is fragile to that spread.

The hypothesis sentences treat a falling cost as a concave cost. The two definitions are scored separately. A pass on one is not a pass on the other.

## 2. Class AM

**AM-X.** The world is exogenous. \(dX=-a X\,dt+\sqrt{2 a \theta}\,dW\), with \(a>0\) and \(\theta>0\). The stationary variance is \(\theta\). No action appears in this equation. A memory that changes the drift of \(X\) is outside this class.

**AM-Y.** The action is an intensity \(u\ge 0\). The channel is \(dY=X\,dt+u^{-1/2}\,dV\) for \(u>0\), with \(V\) a Wiener process independent of \(W\). At \(u=0\) there is no observation. The steady error \(p=\mathbb{E}[(X-m)^2]\) of the conditional mean \(m\) solves
\[
u p^2+2 a p-2 a \theta=0\qquad(u>0),\qquad p=\theta\qquad(u=0).
\]
The positive root is \(p=(-a+\sqrt{a^2+2 a \theta u})/u\). Write \(r=p/\theta\in(0,1]\). Then
\[
u=\frac{2 a(1-r)}{\theta r^2}\qquad(r<1).
\]
The learning rate of this Gaussian conditional is the rate already used for this signal,
\[
L=a\Bigl(\frac{\theta}{p}-1\Bigr)=a\frac{1-r}{r}=\frac{u p}{2}.
\]
Differentiating the closed form \(L=(-a+\sqrt{a^2+2 a \theta u})/2\) gives \(\partial L/\partial u=a\theta/(2\sqrt{a^2+2 a \theta u})>0\). A larger intensity is a strictly more informative channel. That is the sense in which the action decides what is observed.

**AM-H.** The heat is charged at the floor \(kT\,L\). The shape \(\dot Q\ge kT\) times the learning rate is Horowitz and Esposito, as already used in this repository, and it is not re-proved. Attainment of the floor by a finite-rate spring is proved in this repository for a mean-squared decision loss on this signal. It is not re-proved for the sign loss below. Every cost in this file charges the floor. A physical memory whose heat sits above the floor by a gap that grows with \(\theta\) is outside the scored costs.

**AM-S (sign).** The decision names the sign of \(m\). For the centered Gaussian pair \((X,m)\), \(\mathrm{Corr}(X,m)=\sqrt{1-r}\), and
\[
\psi(r)=\frac{1}{\pi}\arccos\sqrt{1-r},\qquad r\in(0,1],
\]
with \(\psi(1)=1/2\). The loss rate is \(w\,\psi(r)\). One decision loses either \(0\) or \(w\).

**AM-Q (square).** The loss rate is \(w p\).

**AM-C (capped probe price).** The probe costs \(\alpha u\) per unit time, with \(\alpha>0\) deterministic. The cost does not depend on \(\theta\) except through the channel.

**AM-U (uncapped probe price).** The probe costs \(\alpha u\,\theta\). The price of a given intensity scales with the variance.

**AM-N (noise that scales).** The channel is \(dY=X\,dt+\sqrt{\theta/u}\,dV\). The noise density scales with \(\theta\). The probe price stays \(\alpha u\).

**AM-0 (uninformative).** The agent pays \(\alpha u\) and the conditional stays at the prior: \(p=\theta\), \(L=0\). The payment does not measure \(X\).

**AM-O (naked option).** No channel and no heat. The payoff is \(\max(X,0)\) for \(X\sim\mathcal N(0,\theta)\), whose expectation is \(\sqrt{\theta/(2\pi)}\), bought at a premium \(c\) that does not depend on \(\theta\). The cost is \(c-\sqrt{\theta/(2\pi)}\). The premium is capped. The payoff is not.

**Accounting.** In the master equation the heat stands in the place of the memory term, the probe price stands in the place of the read term \(A\), the loss rate is \(w\,\mathbb{E}[\ell]\), there is no layer upkeep and no link term, and ruin is a constraint rather than a summand. That placement is this file's. It does not adopt a new equation into THEORY.

**Ruin.** One decision per unit time. Ruin on that decision means the gross loss exceeds a reserve \(B\). A design is admissible when that probability is at most \(\varepsilon_r\). The sign loss is in \(\{0,w\}\). The squared loss is \(w(X-m)^2\).

## 3. Frozen point

| symbol | value |
|---|---|
| \(a\), \(kT\), \(w\) | \(1\), \(1\), \(16\) |
| \(\theta_0\) | \(1\) |
| \(\alpha\) | \((4-\pi)/(6\pi)\) |
| \(B\), \(\varepsilon_r\) | \(16\), \(1/20\) |
| naked premium \(c\) | \(1\) |
| passive intensity held fixed | \(u=4\) |
| spread half-width \(\delta\) | \(1/10\) |
| monotonicity grid | \(\{1/8,1/4,1/2,1,2,4,8\}\) |

\(\alpha\) is not a fitted number. Section 4 derives it as the unique intensity price that places a critical point at \(r=1/2\) when \(\theta=1\).

## 4. Locked algebra

**Sign probability.** \(m\sim\mathcal N(0,\theta-p)\) and \(\mathbb{E}[(X-m)\mid m]=0\), so \(\mathbb{E}[\mathrm{sign}(m)\,X]=\mathbb{E}[|m|]\) and \(\mathrm{Corr}(X,m)=\sqrt{1-r}\). For a centered pair with correlation \(\rho\), the origin splits the plane into opposite-sign wedges of angle \(\arccos\rho\), so \(P(Xm<0)=\arccos(\rho)/\pi\). At \(r=1/2\), \(\rho=1/\sqrt{2}\), the angle is \(\pi/4\), and \(\psi=1/4\).

**Critical point.** With the capped price and the fixed-noise channel,
\[
J(r,\theta)=\alpha\cdot\frac{2a(1-r)}{\theta r^2}+kT\,a\frac{1-r}{r}+w\,\psi(r).
\]
Write \(A(r)=\alpha\cdot 2a(1-r)/r^2\) and \(C(r)=kT\,a(1-r)/r+w\,\psi(r)\), so \(J=A/\theta+C\). The derivative of \((1-r)/r^2\) is \((r-2)/r^3\). The derivative of \(\psi\) is \(1/(2\pi\sqrt{r(1-r)})\). At \(a=kT=1\), \(w=16\), \(r=1/2\),
\[
A'=-24\alpha,\qquad C'=-4+\frac{16}{\pi}.
\]
Setting \(A'+C'=0\) gives \(\alpha=(4-\pi)/(6\pi)\). The second derivative of \((1-r)/r^2\) at \(1/2\) is \(80\), so \(A''=160\alpha\). The second derivative of \((1-r)/r\) at \(1/2\) is \(16\). The derivative of \(\sqrt{r(1-r)}\) vanishes at \(1/2\), so \(\psi''(1/2)=0\). Therefore
\[
\partial_r^2 J(1/2,1)=160\alpha+16>0,
\]
since \(\pi<4\) makes \(\alpha>0\). The critical point is a strict local minimum. At that point \(u=4\), the heat equals \(1\), the sign loss equals \(4\), and
\[
J\Bigl(\tfrac12,1\Bigr)=5+\frac{2(4-\pi)}{3\pi}.
\]
The blind cost is \(w/2=8\). The inequality \(J(1/2,1)<8\) is \(2(4-\pi)<9\pi\), i.e. \(8<11\pi\), which holds because \(\pi>8/11\).

**Level derivative at the point, intensity held fixed.** At fixed \(u\),
\[
\frac{\partial H}{\partial\theta}=kT\,a\frac{1-r}{\theta r(2-r)},\qquad
\frac{\partial(w\psi)}{\partial\theta}=-w\frac{\sqrt{r(1-r)}}{2\pi(2-r)\theta}.
\]
The probe price does not depend on \(\theta\) at fixed \(u\). At the frozen point the heat derivative equals \(2/3\) and the sign derivative equals \(-8/(3\pi)\), so
\[
\frac{\partial J}{\partial\theta}=\frac{2}{3}-\frac{8}{3\pi}.
\]
This is negative because \(\pi<4\). The learning-rate derivative equals the heat derivative because \(kT=1\). The heat rises. The sign loss falls by more.

**Envelope.** Where \(r^*(\theta)\) is a unique interior minimizer, \(\mathrm d J^*/\mathrm d\theta=\partial J/\partial\theta\) at that \(u\). At \(\theta=1\) the local minimum is the candidate, so the same negative number is the predicted slope of the minimized cost. The script's minimization has to land on this critical point. A second basin with a lower cost is a miss of that identification, not a quiet replacement of the point.

**Re-optimized second derivative.** With \(A(1/2)=4\alpha\) and \(C'=16/\pi-4\),
\[
\frac{\mathrm d^2 J^*}{\mathrm d\theta^2}\Big|_{\theta=1}
=8\alpha-\frac{(16/\pi-4)^2}{160\alpha+16}.
\]
Clearing the positive factor \((4-\pi)/(\pi)\) reduces the sign of this expression to the sign of \(44+\pi\), which is positive. The frozen minimized cost is locally strictly convex: level-antifragile and variation-fragile at the same point.

**Global level drop, capped sign, fixed noise.** For each fixed \(r\in(0,1)\), \(\partial J/\partial\theta=-A(r)/\theta^2<0\). As \(r\to 0\), \(J\to\infty\). As \(r=1-\varepsilon\) with \(\varepsilon\downarrow 0\), the gap below the blind cost is \(-w\sqrt{\varepsilon}/\pi\) plus terms of order \(\varepsilon\), so for every \(\theta>0\) some \(r\) undercuts \(w/2\). A minimum is attained, and for \(\theta_2>\theta_1\)
\[
J^*(\theta_2)\le J(r^*(\theta_1),\theta_2)<J(r^*(\theta_1),\theta_1)=J^*(\theta_1).
\]
So \(J^*\) is strictly decreasing on \((0,\infty)\). It is bounded below by \(\inf_r C(r)\), and \(C(1/2)=5\), so the floor is at most \(5\). As \(\theta\to 0\), any fixed \(r<1\) sends \(A(r)/\theta\to\infty\), and the undercut of the blind cost forces \(r^*\to 1\), so \(J^*\to 8\) from below.

**Not concave on an unbounded ray.** Suppose \(J^*\) were concave on \((\theta_1,\infty)\). Concave means difference quotients fall as the right point moves right. The quotient \((J^*(s)-J^*(\theta_1))/(s-\theta_1)\) at any \(s>\theta_1\) is some \(\delta<0\), and concavity then gives \(J^*(t)\le J^*(s)+\delta(t-s)\) for \(t>s\), which runs to \(-\infty\). That contradicts the finite floor. So \(J^*\) is not variation-antifragile on any unbounded right ray. A falling cost and a concave cost are not the same statement.

**Fixed-\(r\) spread.** At \(r=1/2\), \(A=2(4-\pi)/(3\pi)\) and \(\theta=1\),
\[
\tfrac12\bigl(J(1-\delta)+J(1+\delta)\bigr)-J(1)=\frac{A\delta^2}{1-\delta^2}>0
\]
for the frozen \(\delta=1/10\). This is the spread of the slice. The re-optimized spread is a separate number. The prediction is that it too is positive at this \(\delta\). A nonpositive re-optimized spread is a miss of local convexity at a finite width, and the local second derivative above stays on the record either way.

**Squared loss.** \(\partial J/\partial\theta\big|_u=(w+kT\,u/2)\,a/(a+u p)>0\) for every finite \(u\ge 0\). At \(u=0\), \(J=w\theta\) and the derivative is \(w>0\). The minimized unconstrained cost is therefore strictly increasing. On the admissible set \(p\le p_{\mathrm{cap}}\), with \(p_{\mathrm{cap}}\) fixed by \(B\), \(w\), and \(\varepsilon_r\), either the unconstrained minimizer is feasible, or the constraint binds at \(p=p_{\mathrm{cap}}\) and
\[
\frac{\partial J}{\partial\theta}\Big|_{p=p_{\mathrm{cap}}}
=\alpha\cdot\frac{2a}{p_{\mathrm{cap}}^2}+kT\cdot\frac{a}{p_{\mathrm{cap}}}>0.
\]
In both regions the admissible squared cost is strictly increasing wherever it is finite. It is not level-antifragile.

**Uncapped price.** Replace \(\alpha u\) by \(\alpha u\theta\). Then \(\alpha u\theta=\alpha\cdot 2a(1-r)/r^2\), which does not depend on \(\theta\). Neither does \(C(r)\). The minimized sign cost is constant in \(\theta\). The derivative is \(0\). Robust, not level-antifragile.

**Noise that scales.** With noise density \(\theta/u\), the Riccati at \(r=p/\theta\) becomes \(u=2a(1-r)/r^2\), independent of \(\theta\). Heat, sign loss, and probe price then depend on \(\theta\) only through \(r\). The minimized cost is constant in \(\theta\). The learning rate at the minimizer does not rise with \(\theta\). This is the control in which a real observation fails (b).

**Uninformative.** \(L=0\) and \(p=\theta\). The sign cost is \(\alpha u+w/2\), minimized at \(u=0\) with value \(8\), derivative \(0\). The squared cost is \(\alpha u+w\theta\), minimized at \(u=0\) with derivative \(w>0\). Neither falls because of the payment.

**Passive fixed intensity, sign loss.** The same partial derivative as the frozen point, at \(u=4\). Negative at \(\theta=1\). The prediction at \(\theta=4\), same fixed \(u\), is that the partial derivative is positive: the heat, which grows like the square root of \(\theta\) at fixed \(u\), overtakes the bounded sign saving. Passive sign observation is locally level-decreasing at the frozen point and is not monotone.

**Naked option.** \(\mathrm d/\mathrm d\theta\bigl(1-\sqrt{\theta/(2\pi)}\bigr)=-1/(2\sqrt{2\pi\theta})<0\) at every \(\theta>0\). No channel, no heat, no learning rate. A capped premium and a payoff that is convex in \(X\) are enough for a level drop.

**Ruin at the frozen sign point.** The loss is \(0\) or \(16\), and \(B=16\), so \(P(\mathrm{loss}>B)=0\le 1/20\). The operating point is admissible. At the same \((u,p)=(4,1/2)\) the squared loss exceeds \(B\) with probability \(P(|Z|>\sqrt{2})=\mathrm{erfc}(1)\). The prediction is \(\mathrm{erfc}(1)>1/20\), so that squared point is inadmissible. The admissible comparison is the sign cost, not that squared point.

**Informativeness of a failure that ignores \(X\).** If a part's failure time is independent of \(X\) given the part's quality, the conditional law of \(X\) given the failure time and the quality equals the conditional law given the quality alone. The failure adds no information about \(X\). That is the uninformative arm, and it is the reading this file gives of the heterogeneous arm of draft PR #191. It is not a recomputation of that draft.

## 5. Predictions

Scored after the script, in this order. A later line does not edit an earlier score. "Level-antifragile" means strictly decreasing, as in §1.

**P1. Admissible level drop.** At the frozen point the capped sign cost equals \(5+2(4-\pi)/(3\pi)\), the minimizer the script returns is \(r=1/2\), the intensity is \(u=4\), and the slope equals \(2/3-8/(3\pi)<0\). The ruin probability is \(0\). The heat slope equals \(2/3>0\).

**P2. The falling cost is locally convex.** The second derivative in §4 is positive, and the re-optimized spread at \(\delta=1/10\) is positive. The fixed-\(r\) spread equals \(A\delta^2/(1-\delta^2)\) with \(A=2(4-\pi)/(3\pi)\).

**P3. Global shape.** On the frozen monotonicity grid, \(J^*\) is strictly decreasing, every value is strictly below \(8\), and the rightmost value is strictly above \(5\). The cost falls toward a finite floor and is not concave on \((0,\infty)\).

**P4. Squared control, must not be level-antifragile.** Unconstrained and admissible, the squared cost is strictly increasing in \(\theta\). The squared point at \((u,p)=(4,1/2)\) is inadmissible.

**P5. Uninformative control, must not.** Sign minimized cost \(8\), slope \(0\). Squared minimized slope \(w>0\).

**P6. Uncapped price, must not.** Sign cost independent of \(\theta\), slope \(0\).

**P7. Scaled noise, must not.** Sign cost independent of \(\theta\), and the learning rate at the minimizer is independent of \(\theta\). Clause (b), read as a learning rate that rises with volatility, fails on this arm, and the level drop fails with it.

**P8. Passive observation.** Squared, fixed \(u\) or optimized: strictly increasing. Must not be level-antifragile. Sign, fixed \(u=4\): slope negative at \(\theta=1\) and positive at \(\theta=4\).

**P9. Naked option.** Slope \(-1/(2\sqrt{2\pi})\) at \(\theta=1\), negative. No measurement. This arm is level-antifragile with (a) and without (b).

**P10. The action raises the learning rate.** \(\partial L/\partial u>0\) at the frozen \((u,\theta)\). On the two-point menu \(\{0,4\}\) the minimized sign cost at \(\theta=1\) selects \(u=4\), where \(L=1\), against \(u=0\), where \(L=0\).

## 6. What would count as a miss

- Any equality or sign in P1–P3 that the script's evaluation of §4 contradicts, beyond a relative tolerance of \(10^{-9}\) on a closed form, or an absolute tolerance of \(10^{-9}\) on a grid minimum against the closed form. The script may polish a grid point by Newton. It may not move \(\alpha\), \(w\), \(a\), \(kT\), \(B\), or \(\varepsilon_r\).
- P4, P5, P6, or P7 producing a strictly negative slope. Those four are the controls that must not be level-antifragile.
- P8's passive sign slope failing to be negative at \(\theta=1\) or failing to be positive at \(\theta=4\).
- P9 producing a nonnegative slope.
- A coding error in the Riccati root (residual of \(u p^2+2ap-2a\theta\) worse than \(10^{-12}\)), in the hash of this file against `LOCK.txt`, or in the local-minimum second derivative (a nonpositive \(\partial_r^2 J\)). The formulas are then fixed in a dated deviation that does not change this file.

The hypothesis's "exactly when (a) and (b)" is not given a pass condition. P4 says (a) and (b) together are not sufficient for the repository's mean-square loss. P9 says (b) is not necessary for a level drop once a capped premium buys a payoff that is convex in \(X\). P6 and P7 say that dropping (a), or dropping the rise of the learning rate, removes the level drop inside the sign-tracking cost. P2 says the level drop at the frozen point is not the variation reading. Those four sentences are the scored reading of the hypothesis. A miss of any one of them is a puzzle: the note keeps the numbers, names which clause broke, and does not rewrite this file to fit the output.

P8's passive sign slope is the clause the word "passive" does not settle. A negative slope at \(\theta=1\) means a fixed informative channel with a capped intensity price already has a local level drop, so choosing the intensity is not what produces that local sign. A positive slope at \(\theta=4\) means the fixed channel does not keep the drop. Both numbers stand. Neither is rescued by changing \(u\).

## 7. Labels the write-up may use

**PROVED** for an argument in §4 that the script's evaluation matches. **KNOWN** only for a source fetched on Crossref in the results commit, or already fetched in this repository, and only for what that source states. **MISSES** for a sentence in §6 that the scored arm contradicts, reported with the numbers and a diagnosis. **CONJECTURE** for a mechanism named and not run. **METAPHOR** for a biological or financial name that adds no comparison the cost does not already make. **OPEN** for a case this class does not contain.

A miss is not a verdict on the hypothesis sentence. The word for the objective remains cost. The write-up does not call this a theory of everything.

## 8. What the computation is allowed to be

One script, `theory/acting_memory_checks/acting_checks.py`, run after this file is committed and after `LOCK.txt` records its sha256. The script checks that hash before it evaluates a cost. It may print only the quantities named in §4 and §5, the Riccati residual, and the hash check. A diagnostic print is labelled diagnostic and is not a score.

Prior art to be fetched with the results, not used as a premise of the algebra: Taleb and Douady on the convexity definition; Horowitz and Esposito on the heat floor; one source each from active inference, from information-directed sampling, and from optimal experiment design. A DOI is cited only if Crossref returns it. The repository's own R4, the heat floor, and the record of draft PR #191 are already the local reading.

The case this file does not score, and that a later preregistration would have to lock separately: a failure intensity that depends on \(X\) (a Cox clock), a finite-rate spring whose heat is not the floor, and a probe that changes the drift of \(X\).
