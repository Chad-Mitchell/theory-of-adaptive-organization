# The predict-act-correct loop

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. `THEORY.md`, `CORE.md`, and `README.md` are not edited. The master equation is not edited. The acting-memory preregistration is not edited. T45 is that note. This note's open-work row is T46. The preregistration is `theory/acting_loop_checks/PREREG.md`, commit `774e88f`, sha256 `fdf494e9b7f85ca24d9d877ea1610cbaf539dc50127a45106285165b925259a0`, locked by `d77f448` before this computation. Checks: `theory/acting_loop_checks/acting_loop_checks.py`, run at `nice -n 19` (36 checks, FAILS 0, 33 predictions, misses 0). DOIs resolved on the Crossref API on 22 November 2026 are in `theory/acting_loop_checks/crossref.out`.*

Labels: **PROVED** (the argument is on this page, in the class named with it, and the arithmetic is in the checks), **PROVED (in-model)** (the same, at the frozen point), **KNOWN** (published, fetched this session, and only for what that source states), **CONJECTURE** (named, not proved), **METAPHOR** (the name adds no comparison the cost does not already make).

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 0. The answer

Closed-loop acting is strictly cheaper than sensing alone when the channel is not priced, by
\[
\Delta_{\mathrm{full}}(\theta,a)=(q-2aP(a))\,\theta,
\]
with \(P(a)=-a+\sqrt{a^2+q}\) at unit control price and unit action gain. At stake \(q=1\) the factor is \(0.171572875254\) at \(a=1\), \(0.381966011250\) at \(a=1/2\), and \(0.055728090001\) at \(a=2\).

With the heat floor and the probe price charged, the gap at fraction \(r\) is
\[
\Delta(\theta,a,r)=(1-r)\Bigl[(q-2aP(a))\,\theta-\frac{a}{r}-\frac{2\alpha a}{\theta r^2}\Bigr].
\]
At \(q=a=\theta=1\) this gap is negative at every \(r\in(0,1)\). At \(r=1/2\) it equals \(-1.096373258863\): the closed loop is dearer by that amount. At stake \(q=4\) the minimizing fraction is \(0.856768708291\) and the gap is \(+0.033889928154\).

Acting cuts the variance of the state and the stock of mutual information. It does not cut the learning-rate heat. The separated gain does not depend on the error variance. A tight variance cap, and a capped loss, each move that gain. The fixed-intensity closed loop is concave in \(\theta\). The capped sign cost of the acting-memory note is convex in \(\theta\). A quadratic heat gap above \(0.160857250019\) flips the closed loop's second derivative.

## 1. The class

**AL-X.** \(dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW\). At \(b=0\) the world is the exogenous signal of the acting-memory note.

**AL-Y.** \(dY=X\,dt+u_o^{-1/2}\,dV\). The error variance \(p\) solves the Riccati \(u_o p^2+2ap-2a\theta=0\). The action cancels in the error equation.

**AL-K.** \(u_a=-Km\). The state variance is \(v=p+a(\theta-p)/(a+bK)\). The learning rate \(L=a(\theta/p-1)\) does not depend on \(K\).

The scored regulation cost is heat plus the probe price plus \(q v+\rho K^2 s\), with \(s=v-p\). The heat is \(kT\,L\), plus \(\gamma_1\theta\), plus the finite-rate factor \(Q_{\mathrm{fin}}\) at memory rate \(20\). At error fraction \(1/2\) that factor equals \(10/9\). Ruin is a constraint. The frozen point is \(a=b=\rho=kT=\theta=1\), \(\alpha=(4-\pi)/(6\pi)\), \(B=16\), \(\varepsilon_r=1/20\).

In the master equation the heat stands where the memory term stands, the probe price where the read term stands, and the actuation price where effort on the drift stands. Layer upkeep and the link term are zero. That placement is this note's. The reduction at \(b=0\) is the proposal `theory/MASTER_EQUATION_ACTING_PROPOSAL_2026-11-22.md`. It does not edit the equation.

Three arms, one regulation cost. Action alone is a constant \(u_a\) and no observation. Observation alone is \(K=0\). Both together is the separated gain and \(u_o>0\).

## 2. Which arm is cheaper

**Proposition AL-arms (PROVED, under AL-X, AL-Y, AL-R).** For a zero-mean state, a constant action does not cut the variance, and an observation that is not acted on does not either. Both of those arms minimize at doing nothing, with cost \(q\theta\). They are equal.

**Proposition AL-full (PROVED).** With the state observed and the channel not priced, the gap against that common cost is \(\Delta_{\mathrm{full}}(\theta,a)\) above. It is strictly positive for \(q>0\), \(\theta>0\), \(a>0\). The three factors in §0 are that expression at \(q=1\).

**Proposition AL-priced (PROVED (in-model)).** With the floor and the probe price, \(\Delta(\theta,a,r)\) is the gap. At stake \(1\) and \((a,\theta)=(1,1)\) the bracket decreases as \(r\) falls, and its limit at \(r\to 1\) equals \(3-2\sqrt{2}-1-2\alpha<0\). No closed loop is cheaper. The direct cost at \(r=1/2\) exceeds \(q\theta\) by \(1.096373258863\). At stake \(4\) the unique interior stationary point of the gap solves \(K^2 r^3+(2\alpha-1)r-4\alpha=0\), lies at \(0.856768708291\), and the gap there is \(0.033889928154\).

*Proof.* The variance identities are §4 of the preregistration. The checks match the priced gap to the direct cost \(qv+\rho K^2 s+kT\,L+\alpha u_o\) at both stakes, and they match a Lyapunov evaluation of the estimate variance to \(s\). ∎

The answer to the first question is the pair of formulas. Full information, channel not priced: strictly cheaper, by \(\Delta_{\mathrm{full}}(\theta,a)\). Heat and probe priced: strictly cheaper only when the stake covers the first bit of observation. At the frozen price \(\alpha\) that happens at stake \(4\) and not at stake \(1\).

## 3. Acting is memory

**Proposition AL-stock (PROVED).** At fixed error variance,
\[
v(K)-p=\frac{a}{a+bK}(\theta-p).
\]
For \(bK>0\) the right-hand side is strictly smaller than \(\theta-p\). The mutual information \(\tfrac12\log(v/p)\) falls with \(K\). The learning rate does not, and neither does \(Q_{\mathrm{fin}}\).

At \(p=\theta/2\) and \(K=\sqrt{2}-1\), the state variance is \(0.853553390593\) against the uncontrolled value \(1\). The stock falls from \(0.346573590280\) to \(0.267399998370\). The learning rate is \(1\) on both sides. The finite-rate heat is \(10/9\) on both sides.

That is the formal link. Acting is memory in the stock: the variance that has to be carried, and the mutual information of the estimate with the state, shrink because the drift depends on the estimate. Acting is not memory in the heat: the innovation rate is fixed by the process noise and the observation noise, and feedback cancels out of it. Calling the heat a memory of the action would add a comparison the two numbers do not make. That name is **METAPHOR**. The identity is the statement.

## 4. Separation, and where it stops

**Proposition AL-ce (PROVED).** The gain that minimizes \(qv+\rho K^2 s\) at fixed \(p\) is
\[
K^\star=\frac{-a+\sqrt{a^2+qb^2/\rho}}{b}.
\]
It does not depend on \(p\), on \(u_o\), or on \(\theta\). At \(q=\rho=b=a=1\), \(K^\star=\sqrt{2}-1\). This is certainty equivalence for this quadratic, unconstrained, linear-Gaussian problem.

**Proposition AL-cap (PROVED (in-model)).** The reserve \(B=16\) at this operating point gives \(P(X^2>16)=0.000014940159\), inside \(1/20\). The cap does not bind. The tight cap \(v\le 3/5\) at \(p=1/2\) selects gain \(4\), not \(\sqrt{2}-1\). The gain then depends on the observation, through the cap. Separation does not survive that cap.

**Proposition AL-capped-loss (PROVED (in-model)).** For \(\varphi(v)=\mathbb{E}[\min(X^2,1)]\), the derivative of \(\varphi(v(K))+K^2 s(K)\) at the Riccati gain equals \(0.189957517375\). The quadratic derivative at the same gain is \(0\). The gain is not stationary for the capped loss, so certainty equivalence does not extend to it.

The break has one shape in both cases. The quadratic unconstrained cost separates because the best linear gain is a function of \((a,b,q,\rho)\) alone. A cap on \(v\), or a loss whose marginal value of variance is not the constant \(q\), makes the stationarity condition depend on \(p\).

## 5. Level and variability

The two scores stay apart, as in the acting-memory preregistration. Level is the sign of \(\mathrm d J/\mathrm d\theta\). Variability is the sign of \(\mathrm d^2 J/\mathrm d\theta^2\). On the reading in `theory/ROBUSTNESS.md` §6, a concave cost is the one that gains from a spread of \(\theta\).

**Proposition AL-shape (PROVED (in-model)).** At fixed \(u_o=4\), stake \(1\), and no quadratic gap, the slope is \(1.552284749831>0\) and the second derivative is \(-0.321714500038<0\). The spread at half-width \(1/10\) is \(-0.001612560843\). A higher level of \(\theta\) raises the cost. A spread of \(\theta\) lowers it. A linear gap \(\gamma_1\theta\) moves only the slope.

The witness \(\gamma(\theta)=\theta^2\) adds \(2\) to the second derivative. The threshold is \(0.160857250019\). Above it the second derivative is positive, and the witness lies above it.

The capped sign cost minimized in the acting-memory note is convex in \(\theta\) (second derivative \(0.313020858054\) there). The closed-loop regulation cost at fixed intensity is concave. The condition for that flip is the loss: a quadratic state penalty under the separated gain, rather than the capped sign loss. The concavity is the concavity of the Kalman error \(p(\theta)\) and of the learning rate \(L(\theta)\), each with a positive weight. It is not the capped-downside route. That route, in the acting-memory note, is a loss that at fixed fraction does not grow with \(\theta\), together with a probe price that falls as \(1/\theta\). Its cost can fall in the level, and the cost is convex, so a spread hurts. The closed loop does the other pair: the level rises, and a spread helps, until a convex heat gap overcomes the concavity of \(p\) and \(L\).

Read on the payoff \(-J\), the same pair is a concave payoff for the sign cost and a convex payoff for the closed loop. The parenthetical "concave, then convex" matches that payoff reading. The scored variability number remains the second derivative of the cost.

A linear gap of \(1/10\) leaves the old sign slope negative, at \(-0.082159696490\). A linear gap of \(1/2\) makes it positive, at \(0.317840303510\). The gap reverses that level drop and does not change its convexity. On the closed loop the same linear gap steepens a slope that is already positive.

## 6. The sign floor, feedback, and the Cox clock

**Sign grid (PROVED (in-model)).** On \(\theta\in\{1/8,1/4,1/2,1,2,4,8\}\) the minimized capped-sign cost lies strictly above \(4.966383544211\). The gap at \(\theta=8\) is \(0.031682633557\). The algebra is \(J^\star=A(r^\star)/\theta+C(r^\star)\) with \(A>0\), so the cost sits strictly above \(\inf C\) at every finite \(\theta\). The comparison of \(J^\star(8)\) with \(5\) remains the puzzle recorded in the acting-memory note. This file does not edit that preregistration. The diagnosis there stands: \(5\) is the heat plus the sign loss at the frozen fraction, and the floor is lower.

**Feedback on the sign (PROVED (in-model)).** At the same error variance \(1/2\), the separated gain lowers the correlation from \(1/\sqrt{2}\) to \(\sqrt{\sqrt{2}-1}\). The sign loss rises from \(4\) to \(4.439079197657\). For this loss the closed loop is dearer than sensing alone. Shrinking the state shrinks the signal the sign is read from.

**Cox (PROVED (in-model)).** At \(\lambda(x)=1+x^2\), \(v=1\), and a failure at time \(1\), the posterior variance is \(1/2\). An independent failure at the same mean intensity leaves the variance at \(1\). The mean lifetime is \(0.655679542419\), against \(1/2\) for the constant intensity \(2\). A failure that depends on \(X\) is a measurement, and the part is then gone. A failure that ignores \(X\) adds nothing about \(X\). That second sentence is the one already proved for the acting-memory class. The numbers here are the first sentence, at one frozen law.

## 7. What the literatures state

Fetched this session. Crossref HTTP 200 for each DOI. An abstract is quoted only as far as the record prints it. A record with no abstract is cited for the title.

- Kalman, title and abstract fetched, doi 10.1115/1.3662552. The abstract derives the covariance equation of the optimal linear filter and states that filtering is the dual of the noise-free regulator. **KNOWN** for that duality. The scalar Riccati in §1 is this plant's variance equation.
- Kalman and Bucy, title and abstract fetched, doi 10.1115/1.3658902. The abstract derives the Riccati equation for the filtering error. **KNOWN** for that equation. Not a separation theorem.
- Wonham, title fetched, doi 10.1137/0306023. No abstract in the record. **KNOWN** for the title. The separation proved in §4 is the calculation for this scalar quadratic problem. It is not a restatement of that paper.
- Todorov and Jordan, title fetched, doi 10.1038/nn963. No abstract in the record. **KNOWN** for the title. This note does not identify the separated gain with a motor law.
- Sagawa and Ueda, title fetched, doi 10.1103/PhysRevLett.104.090602. No abstract in the record. **KNOWN** for the title, as the feedback equality. The heat charged here is the learning-rate floor plus a gap. It is not that equality.
- Horowitz and Esposito, title fetched, doi 10.1103/PhysRevX.4.031015. **KNOWN** as the source of the shape already used in this repository. Not re-proved.
- Friston, FitzGerald, Rigoli, Schwartenbeck, and Pezzulo, abstract fetched, doi 10.1162/NECO_a_00912. The abstract says action selection can be explained by minimizing variational free energy, and it asks whether neuronal responses can be described as a gradient descent on that free energy. **KNOWN** for that split, as related work. This note minimizes the regulation cost above. It does not minimize a free energy, and it does not identify the gain with their gradient.

## 8. How the pieces fit

This section is a synthesis. It is not a proof of one theorem that produces every layer, every shared store, every boundary, every turnover rate, and every action. What is proved is named as proved. The rest is a conjecture about how those proved pieces sit on one cost.

The cost is the one in the master equation: memory, error, acquisition, and sharing, under a ruin cap. Limited fragile parts restrict the feasible set. A part holds a finite precision and it fails. That restriction is the same kind of object as the ruin cap. It is not a fifth summand. The new assumption, used only in the proposal, is that the action enters the drift. When the coefficient of that action is zero, the proposal's cost reduces to the master equation in the scalar class, with the memory price at the heat floor. That reduction is **PROVED** for the quadratic regulation cost. It is the content of the proposal, and it is not an edit of the equation.

**Layers, the time axis. Proved earlier, for an exogenous world.** A stack is the cheapest design only when one store cannot reset every component, and a lumpy store's lifetime is set by its re-forming cost against the drift it faces. Those are the layer theorems already in the repository. **Conjecture:** under the closed loop the relevant reversion is \(a+bK\) rather than \(a\), so the same cost spaces the stores on the closed-loop rates. This note does not solve a multi-rate plant.

**Spread, the shared store. Proved earlier in the Gaussian class, and one identity proved here.** A shared memory costs less when the decision is a sum of items, and it does not when every item is read alone. That is the holographic-memory note. The identity proved here is that feedback shrinks the stock \(\tfrac12\log(v/p)\) and does not shrink the heat. **Conjecture:** the store that remains worth sharing is the residual \(v(K)-p\), not the uncontrolled variance \(\theta\). The identity is the reason the conjecture is cheap to state. It is not a proof that the shared-store minimum moves.

**Boundary. Proved earlier for the Gaussian Markov field.** For a decision outside a region, the blanket is sufficient, and the interior is not. That is the boundary note. **Conjecture:** a feedback that damps the interior lowers the holding bound on that blanket. This note does not recompute a field.

**Turnover. Proved earlier inside its own class, and one comparison proved here.** Replacement of capacity-limited units can lower the long-run cost under the ruin cap for identical units, and the heterogeneous arm in that draft minimized at no shock. A failure time independent of \(X\) adds nothing about \(X\). The Cox calculation proved here is the other arm: at the frozen law the failure cuts the variance from \(1\) to \(1/2\), and the part is then gone. **Conjecture:** if the hazard rises with \(X^2\), shrinking \(X\) by feedback lowers the rate at which fragile parts fail, and the cost-minimizing turnover moves. The variance cut is proved. The move in the turnover rate is not computed.

**Acting. Proved here, in class AL.** The gap formulas, the stock identity, the separation and its two breaks, and the convexity flip are §2 through §5.

The conjecture that ties them is this. Under one cost, with parts that cannot hold an arbitrary precision and that fail, and under a ruin cap, the minimum spends control to shrink the variance a fragile part would otherwise have to carry, keeps a store only for the residual the control cannot see, shares that residual when the decision is a sum, screens it at the boundary when the decision is outside, and replaces the part when holding it is dearer than the failure. Each clause except the acting identities and the \(b=0\) reduction is a conjecture, or a theorem already proved in a class that did not contain the action. The hypothesis sentence is the bet that a strongly selected system sits near that minimum. This page does not test that bet.

## 9. Checks

`theory/acting_loop_checks/acting_loop_checks.py`. 36 checks, FAILS 0. Predictions P1–P10, 33 hits, misses 0. The locked numbers are the numbers the script prints.

## 10. What this note does not do

It does not edit `THEORY.md`, `CORE.md`, `README.md`, the hypothesis sentence, or the master equation. It does not edit the acting-memory preregistration. It does not rescore T43 or T45. It does not call a self-check an independent review.
