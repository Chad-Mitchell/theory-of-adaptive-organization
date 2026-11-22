# PREREG: antifragility as turnover of capacity-limited units

Written Sunday 22 November 2026, before any script in this directory and before any numerical evaluation of the cost below. The only file this commit adds is this preregistration. No argmin, no grid value, and no Monte Carlo estimate is recorded here.

The hypothesis under test is Chad's, and it is a hypothesis, not a specification. Fragile parts, replaced, with selection on the parts, can make the whole cheaper to run under some stress than under none. The repository already has a different reading. In `theory/ROBUSTNESS.md` §6, Taleb and Douady's definition is applied to the cost of judgment: a cost concave in the stressor gains from variation in that stressor, and, with no adaptation rule, a higher level of volatility does not lower the best cost (R4(a), CT40). K7, stress that strengthens up to a ceiling, is open. `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md` §4 prices capacity-limited units (precision cap \(c\), heat equal to that precision, upkeep per unit, pool versus copy, ruin cap) and records that the split's cost is convex in the failed fraction, so under the repository's reading the split is fragile to variation in failures. This file does not recompute those results. It adds failure, rebuild, and selection, and it asks whether the long-run cost then falls at a positive stress.

This is an in-model check. It does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not change the hypothesis sentence.

## 1. Class AF

One exogenous equilibrium Ornstein–Uhlenbeck signal, variance \(v\), reversion \(a\). The decision estimates that signal. The loss is the mean square. The stake is \(w\). The checks set \(kT = 1\) except where a formula writes \(kT\) so the floor stays visible. The heat floor used here is the one already proved for this signal and this loss: \(kT\) times the learning rate (`theory/INFO_PHYSICS_ATTAINABILITY.md`). For a unit that contributes precision \(\varphi\) on this prior, the learning rate is \(a v \varphi\) and the error of a pool with total precision \(\Phi\) is
\[
\varepsilon = \frac{v}{1 + v \Phi},
\]
the same channel as the capacity-limited pool in the holographic note. Precisions add. A copy reader is not reopened.

Ruin is a constraint, not a summand, as in the master equation. A design is admissible when \(P(\varepsilon > \varepsilon_{\mathrm{cap}}) \le \varepsilon_r\). The cost whose argmin the predictions name is the unconstrained long-run average. The admissible argmin is reported beside it. A minimum that exists only because \(\sigma_s = 0\) is inadmissible is not an interior minimum of the cost.

**Units.** \(n\) units. Unit \(i\) has intrinsic quality \(q_i \in \{q_L, q_H\}\), with \(0 < q_L \le q_H \le 1\), and age \(A_i \ge 0\). Alignment is \(\alpha_i = e^{-\delta A_i}\). The staleness rate is \(\delta\). The world-drift arm sets \(\delta = a\). The static arm sets \(\delta = 0\), which forces \(\alpha_i = 1\) at every age. Installed precision is \(\varphi_i = c\, q_i\), with cap \(c > 0\). Effective precision is \(\varphi_i^{\mathrm{eff}} = c\, q_i\, \alpha_i\). The pool is \(\Phi = \sum_i \varphi_i^{\mathrm{eff}}\).

**Heat and upkeep.** A living unit pays heat \(kT \cdot a \cdot v \cdot c \cdot q_i\) for as long as it is up, including when alignment has decayed. Staleness is a mis-aim, not a sensor that has been switched off. Upkeep is \(h\) per living unit. The installed pair \((n, c)\) is frozen. It is not re-optimized along the stress grid. The blind cost \(w v\), no units, is printed as a reference and is not a point on the stress grid.

**Shocks.** Failures are independent Poisson processes. The intensity of a unit of quality \(q\) is
\[
\lambda(q) = \sigma_s \left(\eta + (1-\eta)\frac{q_H}{q}\right), \qquad \sigma_s \ge 0,\ \eta \in [0,1].
\]
At \(\eta = 1\) the rate does not depend on quality (uninformative failure). At \(\eta = 0\) the rate scales as \(1/q\) (weaker units fail faster).

**Rebuild.** In the primary class replacement is instantaneous: the count stays \(n\). Each failure pays
\[
B(q_{\mathrm{new}}) = b + kT \cdot \tfrac12 \log(1 + v\, c\, q_{\mathrm{new}}),
\]
with the logarithm in nats. The second term is the Gaussian stock of the new unit. The first term is a build cost. Shocks are free only if \(b = 0\) and the stock term is waived, so that \(B = 0\). The frozen primary point has \(b > 0\) and keeps the stock. A one-time initial build is not in the long-run rate.

**Replacement rules.**

- **R-refresh.** Age resets to 0. Quality is drawn from the prior, \(P(q_H) = \pi\), independent of which unit failed.
- **R-select.** Age resets to 0. With probability \(m\) quality is drawn from the prior (mutation). With probability \(1-m\) quality is copied from a unit chosen uniformly among the other \(n-1\) units.
- **R-keep.** Age resets to 0. Quality stays the quality of the unit that was replaced.

**Type chain.** Let \(k\) be the number of units with quality \(q_H\). Write \(\lambda_H = \lambda(q_H)\) and \(\lambda_L = \lambda(q_L)\).

R-refresh:
\[
\begin{aligned}
k &\to k-1 &&\text{at rate } k\,\lambda_H\,(1-\pi),\\
k &\to k+1 &&\text{at rate } (n-k)\,\lambda_L\,\pi.
\end{aligned}
\]

R-select:
\[
\begin{aligned}
k &\to k-1 &&\text{at rate } k\,\lambda_H\left[m(1-\pi) + (1-m)\frac{n-k}{n-1}\right],\\
k &\to k+1 &&\text{at rate } (n-k)\,\lambda_L\left[m\pi + (1-m)\frac{k}{n-1}\right].
\end{aligned}
\]

At \(\sigma_s = 0\) there are no transitions. The type law stays at the initial draw: \(k \sim \mathrm{Binomial}(n, \pi)\). For \(\sigma_s > 0\), \(m \in (0,1)\), and \(\pi \in (0,1)\), the chain on \(\{0,\ldots,n\}\) is irreducible and has one stationary distribution. Both families of rates scale linearly with \(\sigma_s\), so that stationary distribution does not depend on the scale \(\sigma_s\). It does depend on \(\eta\) through the ratio \(\lambda_L/\lambda_H\).

**Ages.** Conditional on quality, failure is memoryless, so in stationarity the age of an up unit of quality \(q\) is exponential with rate \(\lambda(q)\). Therefore, for \(\delta > 0\) and \(\lambda(q) > 0\),
\[
\mathbb{E}[\alpha \mid q] = \frac{\lambda(q)}{\lambda(q)+\delta}.
\]
If \(\lambda(q) = 0\) and \(\delta > 0\), then \(\mathbb{E}[\alpha \mid q] = 0\): the unit is never rebuilt and alignment decays to nothing. If \(\delta = 0\), then \(\alpha = 1\).

Because both death rates scale with \(\sigma_s\), the type law is constant on \((0,\infty)\) while the mean alignment is not, whenever \(\delta > 0\). Selection can improve the mix at every positive stress and still leave a tradeoff against the build rate.

**Mean-field cost.** With \(\mathbb{E}\Phi\) computed from the stationary type law and the mean alignments,
\[
J_{\mathrm{mf}} = \mathbb{E}\Big[\sum_{i=1}^{n}\big(kT\, a\, v\, c\, q_i + h\big)\Big] + \mathbb{E}[\text{build rate}] + w\, \frac{v}{1 + v\, \mathbb{E}\Phi}.
\]
The build rate is the stationary expectation of \(\sum_i \lambda(q_i)\, B(q_{\mathrm{new},i})\), summed exactly over \(k\). The map \(\Phi \mapsto v/(1+v\Phi)\) is convex, so \(J_{\mathrm{mf}}\) uses a loss at most the expected loss.

**Official cost.** Heat, upkeep, and build rate are the exact stationary values. The loss is the Monte Carlo estimate of \(\mathbb{E}[\varepsilon]\) in §3. Official
\[
J = \text{heat} + \text{upkeep} + \text{build rate} + w\, \widehat{\mathbb{E}}[\varepsilon].
\]
Claims about an interior minimum are scored on \(J\), with \(J_{\mathrm{mf}}\) as the closed-form control where a closed form is stated.

## 2. Homogeneous mean-field lemma (algebra, not a run)

One quality \(q\), \(\lambda = \sigma_s\), \(B\) constant, \(\delta > 0\), instantaneous replacement. Let \(\Gamma = v\, n\, c\, q\) and \(Q = kT\, a\, v\, c\, q\). Then
\[
J_{\mathrm{mf}}(\sigma) = n(Q + h + \sigma B) + w\, \frac{v}{1 + \Gamma\, \sigma/(\sigma+\delta)}.
\]
Change variable \(u = \sigma/(\sigma+\delta)\in (0,1)\), so \(\sigma = \delta u/(1-u)\). Differentiating gives
\[
\frac{d J_{\mathrm{mf}}}{d\sigma}\bigg|_{\sigma=0} = n\left(B - \frac{w v^{2} c q}{\delta}\right).
\]
The unique critical point in \((0,1)\), when it exists, is
\[
u^\star = \frac{\sqrt{w v \Gamma} - \sqrt{n B \delta}}{\Gamma \sqrt{n B \delta} + \sqrt{w v \Gamma}}, \qquad \sigma^\star = \delta\, \frac{u^\star}{1-u^\star},
\]
and it lies in \((0,1)\) if and only if \(0 < B < w v^{2} c q / \delta\). In that case \(J_{\mathrm{mf}}(\sigma)\to\infty\) as \(\sigma\to\infty\) and \(\sigma^\star\) is a minimum. If \(\delta = 0\), alignment is identically 1, the error does not depend on \(\sigma\), and \(d J_{\mathrm{mf}}/d\sigma = n B\). For \(B > 0\) that derivative is positive.

The checker recomputes the derivative at 0 from a finite difference of this formula and recomputes \(\sigma^\star\) from the display. It does not treat a grid search as this lemma.

**Scale lemma.** If \(\delta = 0\), then \(\alpha \equiv 1\) and \(\varepsilon\) depends on the types only. The stationary type law is independent of the scale \(\sigma_s\) for every \(\sigma_s > 0\). The build rate is proportional to \(\sigma_s\). Therefore \(J\) is strictly increasing on \((0,\infty)\) whenever \(B > 0\). A drop from the \(\sigma_s = 0\) binomial law down to the selected law, with \(J\) increasing after that drop, is a purge. It is not an interior minimum.

## 3. Estimator, grid, and the word "interior"

Frozen grid
\[
G = \{0,\ 0.05,\ 0.1,\ 0.15,\ 0.2,\ 0.3,\ 0.4,\ 0.5,\ 0.7,\ 1,\ 1.5,\ 2,\ 3,\ 4,\ 6,\ 8,\ 12,\ 20\}.
\]
The same grid is the menu of deliberate turnover rates \(\tau\).

Monte Carlo, per grid point and arm: \(M = 50000\) draws. NumPy Generator, PCG64, seed \(20261122 + s_{\mathrm{arm}}\), with \(s_{\mathrm{arm}}\) the arm number in §4. Common random numbers across the grid of one arm: one matrix \(U\in (0,1)^{M\times n}\) and one vector \(U_k\in (0,1)^M\). Types: invert the exact stationary cdf of \(k\) at \(U_k\). Alignments: if \(\beta(q) = \lambda(q)/\delta > 0\), then \(\alpha = U^{1/\beta(q)}\); if \(\delta = 0\), then \(\alpha = 1\); if \(\lambda(q) = 0\) and \(\delta > 0\), then \(\alpha = 0\). Report the mean of \(\varepsilon\) and the standard error of that mean.

A grid point \(\hat\sigma \in G\setminus\{0, 20\}\) is an **interior minimum** of an arm when all three hold.

1. \(J(\hat\sigma)\) is strictly smaller than \(J\) at every other point of \(G\).
2. The bracketing points \(\hat\sigma/4\) and \(2\hat\sigma\), even if they are not in \(G\), satisfy \(J(\hat\sigma/4) > J(\hat\sigma)\) and \(J(2\hat\sigma) > J(\hat\sigma)\). These two points are part of the arm, not a later choice.
3. On the Monte Carlo arms, each of those two gaps, and the gap \(J(0) - J(\hat\sigma)\) when \(0\) is feasible to evaluate, exceeds twice the paired standard error of the gap under the common random numbers. If the mean-field arm has an interior minimum and the Monte Carlo gaps do not clear this bar, the Monte Carlo score is **INCONCLUSIVE**, and it does not rescue or refute the mean-field score.

A minimum attained only at \(0\) or only at \(20\) is not interior. A function that jumps down at the first positive point and rises after that, with the bracketing point \(\hat\sigma/4\) still below the first positive grid point and already cheaper, is a purge when the scale lemma applies, and the score says purge rather than interior minimum.

**Noise unit.** For \(n = 1\), \(q = 1\), \(\sigma = 1\), \(\delta = 1\), and the frozen \(v, c\), the integral
\[
\mathbb{E}[\varepsilon] = \int_0^1 \frac{v}{1 + v c q\, x}\, \beta x^{\beta-1}\, dx, \qquad \beta = \sigma/\delta,
\]
is computed by a 256-point Gauss–Legendre rule on \((0,1)\) (NumPy only: nodes of the Legendre polynomial). The Monte Carlo mean at seed \(20261122\) must lie within three standard errors of that integral. A miss here invalidates the Monte Carlo arms and is reported before any claim is scored.

**Second difference.** At a mean-field minimizer \(\sigma^\star > 0\), the checker reports
\[
\Delta_2 = \tfrac12\big(J_{\mathrm{mf}}(\sigma^\star/2) + J_{\mathrm{mf}}(3\sigma^\star/2)\big) - J_{\mathrm{mf}}(\sigma^\star).
\]
This is the mean-preserving spread that tests the repository's concavity reading at the operating point. It is not the same question as whether \(\sigma^\star > 0\).

## 4. Frozen numbers and arms

These numbers are taken from the worked cap in the holographic note where that note has them: \(v = 4\), \(c = 1/2\) (below \(\mu_\star = v/\varepsilon_{\mathrm{cap}} - 1 = 5/3\)), \(h = 1/2\), \(w = 3/2\), \(\varepsilon_{\mathrm{cap}} = 3/2\), \(\varepsilon_r = 1/20\). The rest are fixed here and are not moved after the run.

| symbol | value |
|---|---|
| \(kT, a\) | \(1,\ 1\) |
| \(v, n, c, h, w\) | \(4,\ 4,\ 1/2,\ 1/2,\ 3/2\) |
| \(q_H, q_L, \pi, m\) | \(1,\ 1/4,\ 1/2,\ 1/4\) |
| \(b\) | \(1/2\) |
| \(\delta\) on / off | \(1\) / \(0\) |
| \(\eta\) informative / uninformative | \(0\) / \(1\) |
| repair rate in the downtime arm | \(4\) (mean down-time \(1/4\)) |

Design D4 is this table. Design D1 is the same table with \(n = 1\). Claims are scored on D4. D1 is a replication at one unit, where selection has nothing to copy. If D4 and D1 disagree on a qualitative claim, both stand, and the claim is not rewritten to follow the one that matches.

| arm | what is held fixed | policy |
|---|---|---|
| A0 | D4, one quality \(q = 1\), \(\delta = 1\), frozen \(b\), stock kept | mean-field lemma, shock rate \(\sigma\) |
| A1 | same as A0 | official \(J\), Monte Carlo |
| A2 | D4, both qualities, \(\eta = 0\), R-select, \(\delta = 1\), frozen \(b\) | shock. This is the region in the hypothesis |
| A3 | D4, \(q_L = q_H = 1\), \(\delta = 1\), frozen \(b\) | shock. Homogeneous control. Same object as A0/A1 |
| A4 | D4, both qualities, \(\eta = 1\), R-refresh, \(\delta = 1\), frozen \(b\) | shock. Uninformative control |
| A5 | D4, both qualities, \(\eta = 0\), R-select, \(\delta = 0\), frozen \(b\) | shock. No drift |
| A6 | D4, both qualities, \(\eta = 1\), R-refresh, \(\delta = 0\), frozen \(b\) | shock. Uninformative and no drift |
| A7 | A0 with \(B = 0\) (the \(b = 0\) and stock-waived point) | mean-field. Free shocks |
| A8 | D4, both qualities, \(\sigma = 0\), \(\delta = 1\), R-keep, types frozen at the binomial | deliberate turnover at rate \(\tau\in G\), quality-blind |
| A9 | D4, \(\sigma = 0\), \(\delta = 1\); every replacement installs \(q_H\) | deliberate turnover at rate \(\tau\in G\), quality observed |
| A10 | the argmins of A2, A8, A9, and the homogeneous schedule obtained by putting \(\tau\) into A0 in place of \(\sigma\) | comparison only |
| A11 | A0 and A2 with downtime | secondary, defined below |
| A12 | the mean-field minimizer of A0, if it exists | the spread \(\Delta_2\) |

**Downtime (A11 only).** A failed unit is absent for an exponential time of rate \(4\), then returns under the same replacement rule. While absent it contributes no precision and pays no heat and no upkeep. The build cost is paid at the failure. For exponential up and down times the stationary probability of being up is \(4/(4+\lambda(q))\), and the age while up is exponential of rate \(\lambda(q)\). Mean alignment while up is \(\lambda/(\lambda+\delta)\) when \(\delta > 0\). This arm does not score P1–P5. It says whether the primary shape survives a repair delay.

**Homogeneous schedule in A10.** The formula of A0 with the symbol \(\sigma\) read as a chosen turnover rate \(\tau\). No shock. This is the scheduled-replacement policy a designer can run when every unit has the same quality.

## 5. Predictions

Scored after the run, in the order written. A later arm is not used to edit an earlier score.

**P1. Level.** On A2, official \(J\) has an interior minimum at some \(\sigma_s > 0\), at the frozen \(b = 1/2\) with the stock kept. This is the claim that some stress lowers the long-run cost relative to no stress, in the region where quality is heterogeneous, failure is faster for the weaker units, replacement copies survivors with mutation, the world drifts, and rebuild is not free.

**P2. Controls.** On A3 and on A4, \(J\) is monotone nondecreasing in \(\sigma_s\) along \(G\) together with the two bracketing points of any candidate. No interior minimum. The homogeneous mean-field lemma is applied to A3 before this score. If that lemma's hypothesis \(0 < B < w v^{2} c q/\delta\) holds at the frozen numbers, the lemma already says A3 is not monotone, and P2 is then refuted for A3 by the algebra, with A1 as the expected-loss check. A4 is not that one-type formula; it is scored from its own \(J\).

**P3. No drift.** On A5, \(J\) has no interior minimum. The scale lemma says \(J\) is strictly increasing on \((0,\infty)\). The comparison of \(J\) at the smallest positive grid point with \(J(0)\) is reported as a purge if it is a drop, and it is not relabelled as an interior minimum.

**P4. Joint control.** On A6, \(J\) is strictly increasing on \(G\), including from \(0\). Uninformative R-refresh at \(\delta = 0\) leaves both the alignment and the prior type law unchanged, and \(B > 0\) adds a positive build rate.

**P5. Not free.** A7, where \(B = 0\), has no finite interior minimum: with the build term gone, \(J_{\mathrm{mf}}\) is nonincreasing in \(\sigma\) and its smallest value on \(G\) is at the right endpoint. P1 is refuted if the only interior minimum among A0–A7 sits on a \(B = 0\) arm.

**P6. Schedule against shocks.** Let \(J_{\mathrm{sel}}\) be the minimum of A9 on \(G\) under the interior-minimum rule, or the best point of \(G\) if none is interior. Let \(J_{\mathrm{blind}}\) be that minimum for A8, and \(J_{\mathrm{shock}}\) the minimum for A2. Predict \(J_{\mathrm{sel}} \le J_{\mathrm{shock}}\). Predict that the homogeneous schedule in A10 attains a mean-field cost no higher than A0's shock cost at A0's \(\sigma^\star\), at the same rate menu: the exponential clock is the shock, and the deliberate policy is allowed any rate in \(G\) plus the exact \(\sigma^\star\). The gap \(J_{\mathrm{shock}} - J_{\mathrm{blind}}\) is reported and is not given a sign here. If \(J_{\mathrm{shock}} \ge J_{\mathrm{blind}}\), the stress is a substitute for a missing maintenance policy. If \(J_{\mathrm{shock}} < J_{\mathrm{blind}}\), informative failure is doing something a quality-blind schedule does not. Either outcome is a result. Neither is rescued by moving \(b\), \(m\), or \(\eta\).

**P7. Concavity is a different question.** If A0 has an interior minimizer \(\sigma^\star\), then \(\Delta_2 \ge 0\). A positive level of stress that minimizes the cost sits in a locally convex bowl. Under the repository's reading, a cost concave in the stressor is the object that gains from variation. P7 says the level effect and that concavity reading come apart at \(\sigma^\star\): the spread around the best stress raises the mean-field cost. P7 does not say the system is antifragile in the sense of R4.

## 6. What would refute the hypothesis

- P1 fails on D4: no interior minimum of official \(J\) on A2 under §3, or the Monte Carlo is inconclusive and \(J_{\mathrm{mf}}\) on A2 likewise has none.
- The only interior minimum found in A0–A7 is A7, or appears only after setting \(B = 0\).
- P6's inequality \(J_{\mathrm{sel}} \le J_{\mathrm{shock}}\) fails. That failure does not by itself refute P1. It says observation of quality, plus a chosen turnover, was not enough to beat unchosen informative shocks, and the note has to say why.
- A coding error in the noise unit, the stationary distribution (mass not 1, or detailed balance worse than \(10^{-12}\)), or the finite-difference check of the homogeneous derivative (relative error worse than \(10^{-9}\) against the closed form) invalidates the scores. The formulas are then fixed in a dated deviation that does not change this file, and the arm is rerun. A parameter is not changed in order to produce an interior minimum.

P2 failing is a refutation of the control sentence, not of P1. If the homogeneous drifting arm has an interior minimum at \(B > 0\), then heterogeneity and informative failure are not necessary for the level effect in this class. The note says that, and it does not add a further condition after the fact to restore the control.

## 7. Labels the write-up may use

**PROVED** (this class, algebra, code-checked) for the homogeneous derivative, the location of \(\sigma^\star\), and the scale lemma, if the checker agrees. **KNOWN** only for a source fetched on Crossref in the results commit, or already fetched in this repository, and only for what that source states. **FAILS** for a prediction in §5 that the scored arm refutes. **CONJECTURE** for a mechanism named and not run. **METAPHOR** for a biological name that adds no comparison the cost does not already make.

A miss that is not a clean refutation of one numbered prediction is a puzzle: the note gives the numbers, says what is unresolved, and names the next check. It does not promote the puzzle to a verdict on the hypothesis sentence. The word for the objective remains cost. The write-up does not call this a theory of everything, and it does not edit the hypothesis sentence.

## 8. What the computation is allowed to be

One script, `theory/antifragility_checks/turnover_checks.py`, run after this file is committed. It may print only the arms in §4, the noise unit, the stationary-distribution checks, and the derivative check. It may not search a parameter outside the frozen table and then score that search as P1. A diagnostic print must be labelled diagnostic and is not a score.

Prior art to be fetched with the results, not used as a premise of the algebra: Taleb and Douady on convexity; a hormesis review; a synaptic-pruning paper; Kerr, Wyllie, and Currie on apoptosis. A DOI is cited only if Crossref returns it. The repository's own R4 and K7 are already the local reading.
