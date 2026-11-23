# The core: one cost, five yields

*Sunday 22 November 2026. Rewritten from the one-pager at `81fd1a1`. The previous text is `history/2026-11-22_CORE_before_front.md`. The picture is [`figures/master_curve.png`](figures/master_curve.png) (claims and sources: `figures/master_curve.md`); the earlier derivation map is `figures/derivation_map.png`.*

Thermodynamics tells an engineer two things about any engine: the best it could possibly do, and how far a real one falls short. This theory aims to do the same for adaptive systems: cells, colonies, brains, teams, firms, AI and robot systems, anything that must act before its world arrives. Its object is one cost, the cost of judgment: holding memory, being wrong or late, and acquiring and sharing information, under a cap on the chance of ruin. Part of the floor is general: a memory's bath gives off at least \(kT\) times the rate at which it learns, for bipartite chains and additive-noise diffusions. In worked classes the minimum is computed, in closed form where the class allows, and it says what the best design looks like: how many layers, what to share, where a boundary is enough, when a shock should strengthen a system rather than harm it. If the hypothesis below holds, any adaptive system can be measured against its minimum, and the gap says where it wastes and what would close it.

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

Some of the mathematics holds in general: a representation theorem for every system that meets the axioms, and four results that need no Gaussian or linear step. Each design result (layers, holographic sharing, boundaries, rebuilding, acting) is proved in a worked model. That they come from one minimum, and that strongly selected systems sit near it, is the hypothesis.

**First evidence.** In simulations of the authors' own worlds, selection converged to the predicted minimum in clean worlds: the positive control, W1 and W2 of EVO1 (`tests/EVO1/RESULTS_EVO.md`), the high-β Moran arm of SIM-1 (T28 P4), the high-β mode of the selection bridge (T27 P1; its low-β prediction failed); LEARNSIM's learners matched its regime-A level-class prediction (CLAIM_MAP G26). Where the world put something in the way, selection stalled or the run did not count: a creation valley (EVO1 W4), a ruin gate (W3, INVALID), store noise (two INCONCLUSIVE arms), and a nonlinear readout (ANTS1, locked in-model fails). Real-data attempts so far did not qualify: every scored field result is NOT A TEST (30 rows) or INCONCLUSIVE. The real-system test is next: qualify a strongly selected system, preregister and hash-lock the prediction, and measure whether its design sits at the minimum.

The theory has two parts, and they are different kinds of claim. **Part 1 is mathematics:** the cost of a memory that must act before its world arrives, and the designs that minimize that cost inside a named class. Those limits hold by proof. **Part 2 is a hypothesis about nature.** Only Part 2 can miss a measurement.

Until a system qualifies under THEORY §3, the working name is a principle: one cost, and the design is what that cost selects. The heat floor and its minimizers are proved in the class named in §1. The telegraph is in that class. Other Gaussian systems stay open, and other linear systems stay open. The list of what stays open is §6. No system has been shown to qualify.

[`THEORY.md`](THEORY.md) is the canonical statement (v2.9 draft). It still displays the five-term sum. Where this page and `THEORY.md` disagree, `THEORY.md` governs. Putting the physics display into THEORY §3 is open work, T40 in [`OPEN_WORK.md`](OPEN_WORK.md).

## 1. The cost

In steady state the bath of a learning subsystem gives off heat at least equal to temperature times the rate at which the memory learns the world it acts on (Horowitz and Esposito 2014, doi 10.1103/PhysRevX.4.031015). The inequality is **KNOWN**:

$$\dot Q \ge kT \times \text{(learning rate)}.$$

It bounds a heat. It does not choose a stake, a link price, or a ruin cap.

Inside the class below, the cost of judgment is that heat plus a stake on the decision loss. The ruin cap stays outside the sum:

$$J = \dot Q + w\,\mathbb{E}[\ell] \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

\(w\) converts the loss into the currency of the heat. Temperature does not set \(w\).

The five-term sum is the display THEORY §3 still prints. It is a different object from the heat-plus-stake sum. Lemma LY, proved in-model under H1–H3 (`theory/GENERAL_FORM.md`), says a growth maximizer is Pareto in a chosen bad vector. It does not choose the vector. The five-term sum is the special case in which a Pareto front is ranked by risk-neutral expected currency, the prices are linear and nonnegative, and ruin is a half-space cap. Growth and that currency have different argmins. The ideal-gas comparison in that note is this list of extra assumptions. Occupation of the front is open. IP5, the claim that the master equation is the physical frontier, is false (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §2).

In that display, \(\kappa\) is the price of one nat of memory \(I_{\mathrm{mem}}\), \(h\) is the upkeep of one layer, \(K\) is the number of layers, \(A\) is the price of a read, and \(L\) is the price of a link. The stake \(w\) and the expected loss \(\mathbb{E}[\ell]\) are the same quantities as in the heat-plus-stake sum.

$$\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L \qquad\text{subject to}\qquad P(\text{ruin})\le\varepsilon.$$

| Term | Inside the proved class |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | Replaced by the bath heat \(\dot Q\). Floor: \(kT\) times the learning rate. The stock rental is not the coordinate. |
| \(hK\) | Outside the floor. A constant \(h\) still on the books is excess over the heat. |
| \(w\,\mathbb{E}[\ell]\) | Survives. \(w\) stays assumed. |
| \(A\) | Stays assumed as a separate summand. A continuous coupling's read is inside \(\dot Q\). |
| \(L\) | Stays assumed, and stays outside the heat-plus-stake sum. The five-term display still prints it. |
| Ruin cap | Stays assumed, and stays outside both. |

**The class.** An exogenous equilibrium Ornstein–Uhlenbeck signal, independent signals of that kind, or the two-state telegraph. The memory does not move the signal. The loss is the mean squared error of an action of the current memory, or Hamming error on the telegraph. Proofs: `theory/INFO_PHYSICS_ATTAINABILITY.md`, `theory/INFO_PHYSICS_GENERAL.md`, consolidated in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md`.

**PROVED in that class.**

- One OU signal, rate \(a\), variance \(v\), decision error \(\varepsilon\): the heat infimum is \(kT\,a(v-\varepsilon)/\varepsilon\), approached by a fast linear memory at finite heat.
- Above the stake \(kT a/v\) the minimizing cost is \(2\sqrt{kT\,a\,v\,w}-kT\,a\). At or below it the design is blind: heat \(0\), error \(v\), cost \(wv\).
- Equal-variance OU modes on a geometric ladder, each scored on its own: the number tracked is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\).
- The error in a sum of modes: one rank-one memory, gains \(1/(a_k+\mu)\), heat \(kT\mu\). Separate memories of \(K\) identical modes cost \(K\) times that heat.
- The telegraph: flow \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) nats per unit time. The heat infimum is \(kT\) times that flow.

## What holds in general

These hold without a Gaussian or linear step. The first is a theorem about any system that meets the representation axioms A1–A7 (`theory/REPRESENTATION.md`). The others hold under the conditions stated with each (`theory/GENERALITY_2026-11-22.md`).

1. **The cost is a priced sum.** For any system that meets A1–A7, on at least three essential interval coordinates, a continuous cost that represents its preferences is an additive price sum, up to one positive scale and one additive constant, and its memory coordinate is finite-law Shannon information (Theorem R1; a differential mutual information of a Gaussian plant is the extension A6 already names). R1 does not choose the coordinate list (A6 fixes only which information is the memory coordinate), so it does not derive the five terms of THEORY §3. Nonnegative prices are a further assumption, A8, and the integer layer count \(hK\) needs an extra separability assumption.
2. **Memory costs heat.** A bipartite memory's bath gives off at least \(kT\) times the information flow of its own transitions, for bipartite chains and for additive-noise diffusions.
3. **Higher stakes buy more judgment.** On a menu that does not depend on the stake, for a cost \(S+wE\) with ruin slack or absent, judgment spend does not fall as the stake rises, and the error does not rise.
4. **A boundary can be enough.** A joint law that factorizes across a cut screens the two sides. The expected loss is a function of the blanket posterior when the loss depends on the world only through the exterior and the decision is a function of the screened side.
5. **Convex payoffs gain from shocks, and caps can reverse it.** An uncapped convex payoff has expectation at least the payoff of the mean; a cap can reverse that comparison.

If the control enters the generator only as an additive drift \(b\,u\), and the martingale problem for the uncontrolled generator is unique, the process at \(b=0\) is the uncontrolled process. The closed forms in §1 and §2 (the holographic-memory factor, the turnover rate, the gains) are worked examples in clean classes. Whether real systems sit near the minimum is the open hypothesis.

## 2. What the minimum spends the cost on

Five uses. Each is proved in its own class. One theorem that produces all five from the action in the drift is not on this page. The synthesis is `theory/ACTING_LOOP_2026-11-22.md` §8.

**Layers.** A stack is the cheapest design when one store cannot reset every component. On the ladder above, the count has no free constant per layer. The older placement view, [`figures/face.png`](figures/face.png), draws at each time scale the cheapest of local, shared, both, or neither; the master picture is `figures/master_curve.png`. Under the closed loop the conjecture is that the relevant reversion is \(a+bK\). That multi-rate plant is not solved.

**Holographic memory.** In the storage sense (many items in one shared state), a shared memory costs less when the decision is a combination of items, ties or costs more when every item is read on its own, and a random code is beaten by an aligned readout when the decision is known (`theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`). In the field sense, at a fixed per-site error the heat scales with the volume, and scales with a cut only when the decision names a cut: about \(13.61\) per cut site on the worked square lattice, against a lower bound of \(13\) (`theory/HOLOGRAPHIC_2026-11-22.md`). Holographic memory is not a separate assumption: the one cost equation predicts when it wins.

**Boundary.** For a decision outside a region, the blanket is sufficient and the interior is not (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`). On the path of three the exterior variance given the blanket differs from the variance given the region alone (\(3/5\) against \(1/2\)). The matching blanket channel costs at most the Schur trace more than the channel it matches. Screening needs a local precision and a Markov world. A continuous-time heat kernel is positive at every distance, so no finite shell screens.

**Rebuild.** Identical units under the ruin cap, at rate 1, cost 15.473978 with ruin probability 0.020940, against the inadmissible zero at cost 16 (`theory/antifragility_checks/RESULTS.md`). The unconstrained grid minimum is inadmissible. The heterogeneous arm minimizes at no shock, cost 13. The puzzle at this cap: heat is proportional to precision, and the admissible points keep the more precise units. A failure time independent of the world adds nothing about the world. A failure that depends on the state cuts the variance, in the one Cox comparison that was scored, and the part is then gone.

**Acting.** World \(dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW\). With the channel unpriced, the closed loop is cheaper than sensing alone by \((q-2aP(a))\theta\). At unit stake, unit drift, and unit variance that gap is 0.171572875254, against a sensing-alone cost of 1. With the heat floor and the probe price charged, that gap is negative at every fraction when the stake is 1, and at stake 4 the gap at the minimizing fraction is 0.033889928154 (`theory/ACTING_LOOP_2026-11-22.md`). Feedback shrinks the stock \(\tfrac12\log(v/p)\) and does not shrink the learning-rate heat. The separated gain is certainty equivalence for unconstrained linear-quadratic-Gaussian control. A tight variance cap, and a capped loss, each move the gain. An open-loop probe makes the minimized sign cost fall with volatility. The slope equals minus the probe price of the fraction over \(\theta^2\) (`theory/ACTING_MEMORY_2026-11-22.md`).

## 3. Gaining from shocks, a side note

Antifragility and optionality fall out of a convex payoff. Taleb and Douady 2013 (doi 10.1080/14697688.2013.800219) define antifragility as convexity in the stressor. `theory/ROBUSTNESS.md` already applies that definition to this cost: a concave cost gains from a spread of the stressor. A naked option, premium 1 against \(\mathbb{E}[\max(X,0)]=\sqrt{\theta/(2\pi)}\), drops in level with no channel and no heat. The sign bet is a capped loss, and the financial name for that bet adds no comparison the cost does not already make.

The learning route is the other one. Fixed observation noise, a probe price that is not proportional to the variance, and a loss that at fixed fraction depends on the variance only through that fraction: the price of the fraction falls as \(1/\theta\), and that fall is the derivative of the minimized cost. A search of this repository finds both routes in the acting-memory note and finds no theorem identifying them. The synthesis of this page is that the learning heat and the option sit under one cost.

## 4. Acting derivation, merged and not adopted

[PR #203](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/203) is merged (OPEN_WORK T47). Theorem R1′ is a representation theorem, and the cubic ordering is a conjecture. The proposal diff is not applied. This page does not adopt it into THEORY.

## 5. How a miss is read

The full rule is THEORY §3. A class qualifies with a preregistered cost-to-fitness map, a population proxy, a band selection can resolve that excludes a named rival, and a redesign time with at least ten of them in the same world. Cities, nation-states, global economies, and the biosphere wait for a proxy. The class fixes the cost terms, the world's spectrum and noise, and the prices before measuring.

A qualifying design outside the preregistered band is a puzzle for that class. The allowance, the diagnosis, and the next test are fixed with the preregistration. A cost the list omitted is a puzzle of the same kind. So is a design that does not move with a measured change in its inputs, except where the gap that remains sits inside the redesign band at the lower bound of the preregistered redesign cost (CT41, `theory/DYNAMICS.md` §2). A field result with no recorded qualification check is not a test of the hypothesis. The bet is untested.

## 6. What remains

In priority order:

1. **Continuous-information proof of the A6 extension (next proof).** Prove the continuous mutual-information extension of A6 as the limit of discrete partitions (Gelfand–Yaglom–Dobrushin). Expected to carry the discrete results over without changing them.
2. **Non-Gaussian closed forms.** Derive closed forms for heavy tails, switching, and rare shocks (signals other than exogenous equilibrium OU or telegraph, losses other than mean square or Hamming error, and a memory that changes its world): sharper numbers for later real-data tests, not a change to the theory.
3. **The decisive evidence (real-data test).** Measure one real strongly selected system against the axioms (qualified before scoring) and test whether it sits near the predicted minimum, preregistered and hash-locked.
4. **Existing open items and puzzles:**
   - Deriving the stake, the link price, or the ruin cap from the heat bound. They stay assumptions.
   - The fractal draft, [PR #192](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/192). This page claims no result from it.
   - Adopting the acting derivation into THEORY (T47 is merged; the proposal is not applied), and adopting the physics display (T40). Neither edit is made here.
   - The integer \(5\%\) radius. It is 2 at \(\tau=1/2\) and at \(\tau=1\), ratio 1, because both crossings of the level 0.05 lie in \((1,2)\). The path of 61 sites, the next test the preregistration named, returned 2 and 2. The smooth crossing on times \(1/4\) and \(1\) is a separate statistic: ratio 2.067863694520, inside \([1.7,2.3]\).
   - \(J^*(8)\) against 5. The grid value is 4.998066177768. The number 5 equals \(C(1/2)\), the heat plus the sign loss at the frozen fraction, and the diagnostic floor is 4.966383544211. The crossing is near \(\theta=7.5267\). The next test is a new preregistration scored against that floor. The acting-memory preregistration stays as locked.

## Status words

**GENERAL** means it holds without a Gaussian or linear step. **EXAMPLE** means a worked form in a named class. **PROVED** means proved inside the stated model. **KNOWN** means published and credited. **SYNTHESIS** means a reading that places proved pieces on one cost and does not claim one theorem. **OPEN** means not derived or not measured. A **puzzle** is a miss with a diagnosis and a next test.

The layer-count, lifetime, and local-versus-shared theorems in `THEORY.md` minimize the five-term sum. They are theorems about that sum. Adopting §9 of `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` would not re-prove them under the heat.
