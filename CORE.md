# The core: one cost, five yields

*Sunday 22 November 2026. Rewritten from the one-pager at `81fd1a1`. The previous text is `history/2026-11-22_CORE_before_front.md`. The picture is [`figures/derivation_map.png`](figures/derivation_map.png).*

The theory has two parts, and they are different kinds of claim. **Part 1 is mathematics:** the cost of a memory that must act before its world arrives, and the designs that minimize that cost inside a named class. Those limits hold by proof. **Part 2 is a hypothesis about nature.** Only Part 2 can miss a measurement.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Until a system qualifies under THEORY §3, the working name is a principle: one cost, and the design is what that cost selects. Inside the Gaussian and linear class the mathematical core is effectively complete. The list of what that leaves open is §6. Evidence from real systems is thin.

[`THEORY.md`](THEORY.md) is the canonical statement (v2.9 draft). It still displays the five-term sum. Where this page and `THEORY.md` disagree, `THEORY.md` governs. Putting the physics display into THEORY §3 is open work, T40 in [`OPEN_WORK.md`](OPEN_WORK.md).

## 1. The cost

In steady state the bath of a learning subsystem gives off heat at least equal to temperature times the rate at which the memory learns the world it acts on (Horowitz and Esposito 2014, doi 10.1103/PhysRevX.4.031015). The inequality is **KNOWN**:

$$\dot Q \ge kT \times \text{(learning rate)}.$$

It bounds a heat. It does not choose a stake, a link price, or a ruin cap.

Inside the class below, the cost of judgment is that heat plus a stake on the decision loss. The ruin cap stays outside the sum:

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

\(w\) converts the loss into the currency of the heat. Temperature does not set \(w\).

The five-term sum still printed in THEORY §3 is the same object when a growth maximizer is ranked by risk-neutral expected currency, the prices are linear and nonnegative, and ruin is a half-space cap (Lemma LY, **PROVED** in-model under H1–H3, `theory/GENERAL_FORM.md`). The ideal-gas comparison in that note names the extra assumptions that collapse a Pareto front to a linear formula. The lemma does not choose the vector of bads. Occupation of the front is open.

$$\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

| Term | Inside the proved class |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | The bath heat \(\dot Q\). Floor: \(kT\) times the learning rate. |
| \(hK\) | Outside the floor. A constant \(h\) still on the books is excess over the heat. |
| \(w\,\mathbb{E}[\ell]\) | Survives. \(w\) stays assumed. |
| \(A\) | Stays assumed. A continuous coupling's read is inside \(\dot Q\). |
| \(L\), the ruin cap | Stay assumed, and stay outside this \(J\). |

**The class.** An exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph. The memory does not move the signal. The loss is the mean squared error of an action of the current memory, or Hamming error on the telegraph. Proofs: `theory/INFO_PHYSICS_ATTAINABILITY.md`, `theory/INFO_PHYSICS_GENERAL.md`, consolidated in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`.

**PROVED in that class.**

- One OU signal, rate \(a\), variance \(v\), decision error \(\varepsilon\): the heat infimum is \(kT\,a(v-\varepsilon)/\varepsilon\), approached by a fast linear memory at finite heat.
- Above the stake \(kT a/v\) the minimizing cost is \(2\sqrt{kT\,a\,v\,w}-kT\,a\). At or below it the design is blind: heat \(0\), error \(v\), cost \(wv\).
- Equal-variance OU modes on a geometric ladder, each scored on its own: the number tracked is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\).
- The error in a sum of modes: one rank-one memory, gains \(1/(a_k+\mu)\), heat \(kT\mu\). Separate memories of \(K\) identical modes cost \(K\) times that heat.
- The telegraph: flow \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) nats per unit time. The heat infimum is \(kT\) times that flow.

## 2. What the minimum spends the cost on

Five uses. Each is proved in its own class. One theorem that produces all five from the action in the drift is not on this page. The synthesis is `theory/ACTING_LOOP_2026-11-22.md` §8.

**Layers.** A stack is the cheapest design when one store cannot reset every component. On the ladder above, the count has no free constant per layer. [`figures/face.png`](figures/face.png) draws, at each time scale, the cheapest of local, shared, both, or neither. Under the closed loop the conjecture is that the relevant reversion is \(a+bK\). That multi-rate plant is not solved.

**Spread.** A shared memory costs less when the decision is a combination of items. It ties or costs more when every item is read on its own (`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`). At a fixed per-site error the heat scales with the volume. When the decision names a cut, the minimum heat scales with the cut: about \(13.61\) per cut site on the worked square lattice, against a lower bound of \(13\) (`theory/HOLOGRAPHIC_2026-11-22.md`). The encoding name adds no prediction the cost equation does not already make.

**Boundary.** For a decision outside a region, the blanket is sufficient and the interior is not (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`). On the path of three the exterior variance given the blanket differs from the variance given the region alone (\(3/5\) against \(1/2\)). The matching blanket channel costs at most the Schur trace more than the channel it matches. Screening needs a local precision and a Markov world. A continuous-time heat kernel is positive at every distance, so no finite shell screens.

**Rebuild.** Identical units under the ruin cap, at rate 1, cost 15.473978 with ruin probability 0.020940, against the inadmissible zero at cost 16 (`theory/antifragility_checks/RESULTS.md`). The unconstrained grid minimum is inadmissible. The heterogeneous arm minimizes at no shock, cost 13. The puzzle at this cap: heat is proportional to precision, and the admissible points keep the more precise units. A failure time independent of the world adds nothing about the world. A failure that depends on the state cuts the variance, in the one Cox comparison that was scored, and the part is then gone.

**Acting.** World \(dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW\). With the channel unpriced, the closed loop is cheaper than sensing alone by \((q-2aP(a))\theta\), and the factor at \(q=a=1\) is 0.171572875254. With the heat floor and the probe price charged, that gap is negative at every fraction when the stake is 1, and is 0.033889928154 at stake 4 (`theory/ACTING_LOOP_2026-11-22.md`). Feedback shrinks the stock \(\tfrac12\log(v/p)\) and does not shrink the learning-rate heat. The separated gain is certainty equivalence for unconstrained linear-quadratic-Gaussian control. A tight variance cap, and a capped loss, each move the gain. An open-loop probe makes the minimized sign cost fall with volatility. The slope equals minus the probe price of the fraction over \(\theta^2\) (`theory/ACTING_MEMORY_2026-11-22.md`).

## 3. Convex payoffs

Antifragility and optionality fall out of a convex payoff. Taleb and Douady 2013 (doi 10.1080/14697688.2013.800219) define antifragility as convexity in the stressor. `theory/ROBUSTNESS.md` already applies that definition to this cost: a concave cost gains from a spread of the stressor. A naked option, premium 1 against \(\mathbb{E}[\max(X,0)]=\sqrt{\theta/(2\pi)}\), drops in level with no channel and no heat. The sign bet is a capped loss, and the financial name for that bet adds no comparison the cost does not already make.

The learning route is the other one. Fixed observation noise, a probe price that is not proportional to the variance, and a loss that at fixed fraction depends on the variance only through that fraction: the price of the fraction falls as \(1/\theta\), and that fall is the derivative of the minimized cost. A search of this repository finds both routes in the acting-memory note and finds no theorem identifying them. The synthesis of this page is that the learning heat and the option sit under one cost.

## 4. In review, and not adopted

[PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203) (branch `cursor/acting-derivation-2d99`, head `a79d7b6`) is in review. Theorem R1′ is a representation theorem: the additive form is Debreu's theorem applied to the product the axiom names. The step proved there is the \(b=0\) reduction. The effort coordinate drops out and the cost is the five-term equation, each term kept, before any minimization. The risky prediction, an ordering of two gains on a cubic plant, was met by one grid step. A stationary solve gives continuous gains 0.23 against 0, below the grid spacing. The path gate was underpowered, so meeting it is weak evidence. The proposal diff is on that branch. It is not applied. This page does not treat the pull request as merged.

## 5. How a miss is read

The full rule is THEORY §3. A class qualifies with a preregistered cost-to-fitness map, a population proxy, a band selection can resolve that excludes a named rival, and a redesign time with at least ten of them in the same world. Cities, nation-states, global economies, and the biosphere wait for a proxy. The class fixes the cost terms, the world's spectrum and noise, and the prices before measuring.

A qualifying design outside the preregistered band is a puzzle for that class. The allowance, the diagnosis, and the next test are fixed with the preregistration. A cost the list omitted is a puzzle of the same kind. So is a design that does not move with a measured change in its inputs, except where the gap that remains sits inside the redesign band at the lower bound of the preregistered redesign cost (CT41, `theory/DYNAMICS.md` §2). A field result with no recorded qualification check is not a test of the hypothesis. The bet is untested.

## 6. What remains

- Signals other than an exogenous equilibrium OU process or the telegraph, and losses other than the mean square or Hamming error. This is the non-Gaussian case, and it is open.
- A memory that changes its world.
- Deriving the stake, the link price, or the ruin cap from the heat bound. They stay assumptions.
- A real-data test of a system that qualifies.
- The fractal draft, [PR #192](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/192). This page claims no result from it.
- Adopting the acting derivation into THEORY once #203 is reviewed, and adopting the physics display (T40). Neither edit is made here.
- The integer \(5\%\) radius. It is 2 at \(\tau=1/2\) and at \(\tau=1\), ratio 1, because both crossings of the level 0.05 lie in \((1,2)\). The path of 61 sites, the next test the preregistration named, returned 2 and 2. The smooth crossing on times \(1/4\) and \(1\) is a separate statistic: ratio 2.067863694520, inside \([1.7,2.3]\).
- \(J^*(8)\) against 5. The grid value is 4.998066177768. The number 5 equals \(C(1/2)\), the heat plus the sign loss at the frozen fraction, and the diagnostic floor is 4.966383544211. The crossing is near \(\theta=7.5267\). The next test is a new preregistration scored against that floor. The acting-memory preregistration stays as locked.

## Status words

**PROVED** means proved inside the stated model. **KNOWN** means published and credited. **SYNTHESIS** means a reading that places proved pieces on one cost and does not claim one theorem. **IN REVIEW** means an open pull request. **OPEN** means not derived or not measured. A **puzzle** is a miss with a diagnosis and a next test.

The layer-count, lifetime, and local-versus-shared theorems in `THEORY.md` minimize the five-term sum. They are theorems about that sum. Adopting §9 of `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` would not re-prove them under the heat.
