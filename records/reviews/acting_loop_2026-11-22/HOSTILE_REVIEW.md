# Hostile review of draft PR #201

**VERDICT: NEEDS-FIXES.**

Independent review of head `7e45e3d57ad5624b3db487cb31476f507726c647` on `cursor/acting-loop-f7b1`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake` build. Computations at nice 19. The author's script was not imported.

The arithmetic in the locked expressions recomputes. The variance identity at \(b=0\) is exact. The house rules hold: the hypothesis sentence is byte-identical, `THEORY.md` is unchanged, the new prose says cost, and OPEN_WORK has row T46. What does not hold is the use those numbers are put to. Zero misses out of 33 is the result the preregistration told the script to produce. The extended cost does not follow from Theorem R1 plus one new assumption. The reduction at \(b=0\) is the stake term of the quadratic problem under conditions the summaries drop. The negative second derivative is the curvature of a fixed intensity the same note shows is dearer than doing nothing. The integer \(5\%\) radius is still the puzzle the boundary scorer files.

The hypothesis sentence is one copy in each of `THEORY.md`, `CORE.md`, and `README.md`, the same bytes at head and at `main` `ad4756c`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`git diff ad4756c 7e45e3d` is empty on all three. The same sentence is the one copy in the acting-loop note, the proposal, and the preregistration.

Recomputation is `reviews/acting_loop_2026-11-22/checks/recompute.py`. Stationary moments are the scalar Riccati and the Lyapunov equation. The platform math library supplies `erf`, `erfc`, and `acos`. Every locked decimal below agrees to within \(5\times 10^{-13}\), which is the rounding of the printed twelve digits.

## The lock

The preregistration precedes the script, the hash matches, and the file was not edited. The decimals precede the lock as well. They are in the file the lock hashes.

| | |
|---|---|
| Preregistration commit | `774e88fdda46720d933157ee586da3d197235b42`, 2026-11-22 22:10:42 +0000 |
| Parent | `2d15d12e940e2430d6c56d58b4556328ca2ec43e` |
| Files in that commit | `theory/acting_loop_checks/PREREG.md` only |
| Lock commit | `d77f448d2dc00e00516752dee62a3c038060d958`, 2026-11-22 22:10:48 +0000 |
| Files in the lock commit | `theory/acting_loop_checks/LOCK.txt` only |
| Computation commit | `41dd3fdb3175d697ded18b785d97ac5353ccc1b1`, 2026-11-22 22:15:30 +0000 |
| Blob of `PREREG.md` at the preregistration, the lock, and head | `79df745d6f5bb8b1b54fb043dc6040714633df4d` |
| sha256 of the file bytes | `fdf494e9b7f85ca24d9d877ea1610cbaf539dc50127a45106285165b925259a0` |

The gap from the preregistration to the lock is six seconds. The parent already contains `theory/acting_memory_checks/acting_checks.py`, the published floor \(4.966383544211\), the published cost \(J^*(8)=4.998066177768\), and the envelope slope \(2/3-8/(3\pi)\). A search of that parent for the new twelve-digit strings is empty. Those strings appear for the first time inside `PREREG.md`, in the same commit as the closed forms.

The preregistration says so. Section 4 writes the closed forms. Section 5 writes their decimals. The opening sentence is: "The decimals are the values of the expressions written here. No design was searched to produce them. A later script may only evaluate these expressions." The miss rule in §6 is a disagreement between the script and §4. A script that implements §4 and does not mistype a radical cannot miss.

The acting-memory grid had a line that could miss, and it did: \(J^*(8)=4.998066177768\) against a locked threshold of \(5\). Nothing in P1–P10 has that shape. Compare a prediction that locks a sign before the decimal exists with a file that arrives containing both.

## The thirty-three lines

Zero of the thirty-three are risky predictions. Twenty-two are exact evaluations of expressions written in §4 before the lock. Eleven are tautologies of those definitions: the sign of a closed form §4 already signed, an identity the script compares to itself, or a quantity the formula does not depend on. The count of `predict` calls in `acting_loop_checks.py` is 33. The count of `check` calls that the script prints is 36. Both numbers are real. The second is not evidence about the first.

| # | Line as scored | Class | Why |
|---|---|---|---|
| 1 | P1 factor at \(a=1\), \(0.171572875254\) | (b) | §4 gives \(3-2\sqrt{2}\) |
| 2 | P1 factor at \(a=1/2\), \(0.381966011250\) | (b) | §4 gives \((3-\sqrt{5})/2\) |
| 3 | P1 factor at \(a=2\), \(0.055728090001\) | (b) | §4 gives \(1-4/(2+\sqrt{5})\) |
| 4 | P1 each factor positive | (c) | the same three closed forms are positive by \(\sqrt{2}<3/2\), \(\sqrt{5}<3\), and \(\sqrt{5}<5/2\), and §4 already says so |
| 5 | P2 gap at \(r=1/2\), \(-1.096373258863\) | (b) | §4 gives \(\tfrac12(3-2\sqrt{2}-2-8\alpha)\) |
| 6 | P2 dearer at \(r=1/2\) | (c) | the sign of line 5, stated in §4 |
| 7 | P2 bracket as \(r\to 1\) is negative | (b) | §4 gives \(3-2\sqrt{2}-1-2\alpha<0\), then concludes no fraction in \((0,1)\) is cheaper because the bracket increases in \(r\) |
| 8 | P3 root \(0.856768708291\) | (b) | Newton on the cubic written in §4. Existence of one root in \((0,1)\) is the sign change and one turning point. The decimal was computed before the lock |
| 9 | P3 gap \(+0.033889928154\) | (b) | \(\Delta\) at that root. The sign is in §4 of the same commit |
| 10 | P4 variance \(0.853553390593\) | (b) | \((2+\sqrt{2})/4\) |
| 11 | P4 learning rate unchanged and equal to \(1\) | (c) | \(L=a(\theta/p-1)\) has no \(K\). The script sets `L_off = L_on` |
| 12 | P4 finite-rate heat \(10/9\), unchanged | (c) | AL-H defines the expression without \(K\), and at \(r=1/2\), \(\lambda=20\), \(a=1\) it is the fraction \(10/9\). The script computes it once |
| 13 | P4 stock \(0.346573590280\to 0.267399998370\) | (b) | \(\tfrac12\ln 2\) and \(\tfrac12\ln(1+2^{-1/2})\) |
| 14 | P5 gain \(\sqrt{2}-1\), independent of \(p\) | (c) | `K_of(1,1)` is \((-1+\sqrt{2})\). The function takes no \(p\), and the script calls it twice |
| 15 | P5 cap selects gain \(4\) | (c) | §4 writes \(K_{\mathrm{cap}}=(\theta-p)/(3/5-p)-1=4\) |
| 16 | P5 derivative \(0.189957517375\) | (b) | the normal formula written in §4, evaluated before the lock |
| 17 | P5 derivative not zero | (c) | \(\tfrac14(1-\varphi'(v))>0\) for a non-degenerate Gaussian, because the cap binds with positive probability |
| 18 | P5 reserve does not bind | (b) | the locked test is a tail bound. §4 already has \(4/\sqrt{v}>4\). The printed tail \(0.000014940159\) is `erfc` of that threshold and was not itself a twelve-digit prediction |
| 19 | P6 slope \(1.552284749831\) | (b) | \((4\sqrt{2}-1)/3\) |
| 20 | P6 second derivative \(-0.321714500038\) | (b) | \(4(2\sqrt{2}-5)/27\) |
| 21 | P6 spread \(-0.001612560843\) | (b) | three evaluations of the fully specified \(J\). No radical is written for this one line. The twelve digits are still in the preregistration, so the value was computed before the hash |
| 22 | P6 threshold \(0.160857250019\) | (b) | \(2(5-2\sqrt{2})/27\) |
| 23 | P6 witness \(\gamma_2=1\) flips the sign | (c) | \(1\) exceeds the threshold in line 22 |
| 24 | P7 every grid cost above the floor | (c) | §4 proves \(J^*=A(r^*)/\theta+C(r^*)>\inf C\) for every finite \(\theta\), from \(A>0\). The grid cannot fail if that algebra is implemented |
| 25 | P7 gap at \(\theta=8\), \(0.031682633557\) | (b) | \(4.998066177768-4.966383544211\), both published in the acting-memory note before this preregistration |
| 26 | P7 floor matches \(4.966383544211\) | (b) | re-minimizing the cost the acting-memory checks already minimized |
| 27 | P8 sign loss \(4.439079197657\) | (b) | \(16\arccos(\sqrt{\sqrt{2}-1})/\pi\) |
| 28 | P8 correlation falls | (c) | \(\sqrt{\sqrt{2}-1}<1/\sqrt{2}\) is \(\sqrt{2}-1<1/2\) |
| 29 | P9 posterior variance \(1/2\) | (b) | §4's fraction: \(\sigma^2=1/3\), then \(\sigma^2(\lambda_0+3\beta\sigma^2)/(\lambda_0+\beta\sigma^2)=1/2\) |
| 30 | P9 independent variance stays \(1\) | (c) | the script checks `Decimal(1) == 1`. It does not form the independent-arm posterior |
| 31 | P9 mean lifetime \(0.655679542419\) | (b) | the erfc integral written in §4. The comparison with \(1/2\) is Jensen's inequality for \(1/\lambda(X)\) |
| 32 | P10 slope plus \(1/10\), \(-0.082159696490\) | (b) | the published acting-memory slope plus \(1/10\) |
| 33 | P10 slope plus \(1/2\), \(0.317840303510\) | (b) | the same slope plus \(1/2\) |

Lines 25, 26, 32, and 33 are re-reads of the acting-memory lock. Line 24 is the algebra that makes the re-read automatic. A hit on the difference \(4.998066177768-4.966383544211\) restates the earlier miss against \(5\).

## The numbers

Direct cost, with the channel priced: learning rate \(L=a(\theta/p-1)\), probe price \(\alpha u\), state penalty \(qv\), actuation price \(\rho K^2 s\), with \(p\) from the Riccati and \((s,v)\) from the Lyapunov equation. Sensing alone, for the quadratic loss, is the blind cost \(q\theta\). The gap is that cost minus the closed loop. This is not the author's `delta_priced` function. It returns the same decimals.

| Quantity | Recomputed | Locked |
|---|---|---|
| Factor at \(a=1,1/2,2\) | \(0.171572875254\), \(0.381966011250\), \(0.055728090001\) | same |
| Gap at stake \(1\), \(r=1/2\) | \(-1.096373258863\) | same |
| Stake \(4\) root and gap | \(0.856768708291\), \(+0.033889928154\) | same |
| State variance | \(0.853553390593\) | same |
| Mutual information | \(0.346573590280\to 0.267399998370\) | same |
| Finite-rate expression | \(10/9\) | same |
| Separated gain | \(\sqrt{2}-1\) | same |
| Tight cap | \(4\) | same |
| Capped-loss derivative | \(0.189957517375\) | same |
| Tail \(P(X^2>16)\) | \(0.000014940159\) | same |
| Slope, second derivative | \(1.552284749831\), \(-0.321714500038\) | same |
| Spread, threshold | \(-0.001612560843\), \(0.160857250019\) | same |
| Sign-grid gap | \(0.031682633557\) | same |
| Sign loss under feedback | \(4.439079197657\) | same |
| Cox variance, mean lifetime | \(1/2\), \(0.655679542419\) | same |

The slope and the second derivative are the derivatives of
\[
J=(5-2\sqrt{2})\,p(\theta)+2(\sqrt{2}-1)\,\theta
\]
at fixed \(u_o=4\), \(q=1\), \(a=1\), plus a constant. Here \(p=(-1+\sqrt{1+8\theta})/4\). At \(\theta=1\) the derivatives are \((4\sqrt{2}-1)/3\) and \(4(2\sqrt{2}-5)/27\). A one-step finite difference at \(h=10^{-6}\) and \(h=10^{-5}\) is coarser than the twelve digits. The three-point spread, which evaluates \(J\) and does not difference it, matches the locked spread on its own.

The same \(J\) has a negative second derivative at \(\theta\in\{1/4,1/2,1,2,4,8\}\). The closed form is negative for every \(\theta>0\), because \(p\) is concave and its coefficient \(5-2\sqrt{2}\) is positive. The spread result is not an artifact of half-width \(1/10\).

A Simpson quadrature of the Cox posterior, likelihood \((1+x^2)e^{-(1+x^2)}\) times a standard normal prior at time \(1\), returns variance \(0.500000000000\). The lifetime quadrature of \(\mathbb{E}[1/(1+X^2)]\) returns \(0.655679542419\). The Gaussian tail is `erfc`. The capped-loss derivative from `erf` matches; a Simpson derivative of the same objective agrees to about \(5\times 10^{-5}\), which is the grid.

At \(b=0\), \(p=1/2\), \(\theta=1\), the Lyapunov variance is \(1\) at gains \(0\), \(1\), \(4\), and \(100\).

On a grid of step \(0.001\), the stake-\(1\) gap is negative at every fraction. The largest value on that grid is \(-9.2\times 10^{-4}\).

## The derivation

The proposal does not follow from the repository's axioms plus the one new assumption that the action enters the drift.

Theorem R1 in `theory/REPRESENTATION.md` assumes A1–A7. Its proof, step 1, uses A7 to get a lottery from a design: the world law is fixed. A7's own sentence does two things. The law of the world does not depend on the design, and effort spent changing the world's drift is not one of the coordinates. A7-act drops the first and adds a coordinate, \(\rho\,\mathbb{E}[u_a^2]\), of the kind A7 excludes. "Nothing else in A1–A6 or A8 is changed" is true of those six axioms and of A8. It is not a re-proof of R1.

The file mostly does not claim the re-proof. Adoption of AL-J is labeled **CONJECTURE**. The sentence that slips is "The additive shape is R1's shape." Under A7-act, R1's hypotheses are not the hypotheses in force. The sum is a specification inside class AL. Labeling that specification **PROVED** as an accounting identity is accurate and empty: once the coordinates are chosen, their sum is their sum.

The other labels in the proposal match the arguments they sit on, with the exceptions in F3 and F4.

- A1–A7, A8, the ruin constraint, and the exogenous clause are **STANDARD**, and they match `REPRESENTATION.md` and THEORY §3.
- The heat floor as a bound, distinct from attainment, matches the proposal's own split. Equality for a plant whose drift depends on the estimate is **CONJECTURE**. That label is the right one. The learning rate \(L=u_o p/2\) really is independent of \(K\), because the control cancels in the error equation. The bound can use that \(L\). Attainment cannot be imported from the exogenous spring.
- The night-1 Axiom 5 citation is the one-budget sum in `reviews/night1/formal/AXIOMS.md`. It is not a second derivation. The sentence is unlabeled.
- "Storing, predicting, acting, and staying solvent do not force the additive form" is Theorem R2, described as R1's companion. The description is fair. The name R2 is the accurate label.
- The independent-failure sentence is the proposition the acting-memory note labels **PROVED**. The citation is right and unlabeled.
- Booking the Cox observation's price inside the acquisition coordinate is a specification. It is unlabeled.
- "At \(b=0\) it is A7" is true of the law of \(X\). It is not true of the coordinate list, which still carries an actuation price A7 does not list. The minimum sets that price to zero.

The algebra of Proposition AL-reduce is exact inside class AL for the quadratic regulation cost. Substitute \(b=0\) into \(v=p+a(\theta-p)/(a+bK)\). For every finite \(K\), \(v=\theta\). The map \(K\mapsto \rho K^2(\theta-p)\) has derivative \(2\rho K(\theta-p)\), zero at \(K=0\) and positive for \(K>0\). The channel cost is positive at every \(u_o>0\) at the frozen positive prices, so the minimum over intensity is \(u_o=0\), where \(L=0\). The value there is
\[
J=q\theta+\gamma_1\theta.
\]
At \(\gamma_1=0\) this is the stake term, with the channel, the actuation, the layer upkeep, and the link term all zero because the minimum set them to zero.

That is not, by itself, the five-term master equation. The master equation prices memory at \(\kappa I_{\mathrm{mem}}\) and acquisition at \(A\). The corollary restores a loss that can use an observation, puts the heat where \(\kappa I_{\mathrm{mem}}\) stands, puts the probe price where \(A\) stands, and sets the other two terms to zero. The paragraph after the corollary says this is a specialization of the sum and not a proof that the coordinates are forced. The sentence that overshoots is "That is the master equation in this scalar class." T46 and the pull-request body drop even the corollary's conditions. They say the extended cost reduces to the scalar master equation.

The finite-rate formula is Proposition AT-attain of `theory/INFO_PHYSICS_ATTAINABILITY.md`:
\[
\dot Q=a(v-\varepsilon)\frac{\rho}{\rho(v+\varepsilon)-v},
\]
with \(\rho=\lambda/(a+\lambda)\), for an exogenous equilibrium Ornstein–Uhlenbeck signal. At \(v=\theta\), \(\varepsilon=p\), this is the preregistration's \(Q_{\mathrm{fin}}\). It replaces \(kT\,L\). It is not added to it. At the frozen point \(L=1\), so the heat and the ratio \(\dot Q/(kT\,L)\) are both \(10/9\). Those two numbers come apart as soon as \(L\neq 1\). AL-H and the note say "plus the finite-rate factor." The proposal says "replaced." The checks charge \(kT\,L\) in \(J\) and report \(Q_{\mathrm{fin}}\) beside it. They do not add them. The scored gap, slope, and spread are the floor-charged cost. The prose says something the score does not do.

## Acting and the stock

The stock identity is right, and the body is more careful than the section title.

For the scalar Kalman pair, \(I(X;m)=\tfrac12\ln(v/p)\). At the frozen point that is \(\tfrac12\ln 2=0.346573590280\) with no gain, and \(0.267399998370\) at \(K=\sqrt{2}-1\). The learning rate \(L=a(\theta/p-1)\) equals \(1\) on both sides, because \(p\) does not depend on \(K\). The heat the checks charge at that learning rate does not move. Calling that heat a memory of the action is the comparison the note marks **METAPHOR**. That part is stated correctly and is not overclaimed.

Two limits belong in the same paragraph. The stock \(\tfrac12\ln(v/p)\) is the mutual information of the current state with the current estimate. A6's memory coordinate is the path stock \(I(M_t;X^t)\). The note does not equate them. The finite-rate heat staying at \(10/9\) is the exogenous expression evaluated at the same \(r\) and the same open-loop \(a\). Under feedback the signal the spring would track is the controlled state. Proposition AT-attain does not cover that state. The proposal already says so. Proposition AL-stock labels the invariance of \(Q_{\mathrm{fin}}\) as **PROVED**. The invariance that is proved is \(L\)'s.

The title "Acting is memory" is a slogan for a result whose careful sentence is the opposite on the heat. The identity to keep is the one the body already gives: feedback shrinks the information stock, and the learning-rate heat stays fixed.

## The spread, and the acting-memory result

The negative second derivative is interpreted correctly as a statement about one function, and incorrectly as the pair to the acting-memory result.

`theory/ACTING_MEMORY_2026-11-22.md` scores the minimized sign cost. Its second derivative at \(\theta=1\) is \(+0.313020858054\). The fixed-fraction spread at half-width \(1/10\) is \(+0.001839996934\). The re-optimized spread is \(+0.001577268119\). A spread of \(\theta\) raises that cost. Proposition AM-not-concave says a cost that is strictly decreasing and bounded below on a half-line cannot be concave there. The sign cost is that kind of cost.

The closed-loop number \(-0.321714500038\) is \(\mathrm d^2 J/\mathrm d\theta^2\) at stake \(1\), fixed intensity \(u_o=4\), and \(\gamma_2=0\). On that function a mean-preserving spread lowers the expected cost, and the three-point spread \(-0.001612560843\) agrees. The reading in `theory/ROBUSTNESS.md` §6, a concave cost against a convex payoff, fits this function. The mechanism the note gives is the right one for this function: \(p(\theta)\) and \(L(\theta)\) are concave, and at the separated gain they enter with positive weights.

That function is not the cost the hypothesis minimizes at stake \(1\). P2 says the closed loop is dearer than sensing alone at every fraction. The minimizing design is the blind cost \(q\theta\). Its second derivative is \(0\). A spread does not lower it. Re-optimizing the direct cost on \(\theta\in\{0.9,1.0,1.1\}\) selects the blind endpoint at stake \(1\), and the spread of those three values is \(0\).

At stake \(4\) the minimizing fraction is interior, and the minimized cost lies below \(4\theta\). On the same three points its spread is about \(-0.003507\). That number is not locked, and it is not \(-0.321714500038\). The note's comparison, "the closed loop does the other pair," sets a dominated slice beside the acting-memory minimum.

The parenthetical "concave, then convex" is not a phrase in `THEORY.md`, `theory/ROBUSTNESS.md`, or the acting-memory note. The payoff \(-J\) is concave for the sign cost and convex for the fixed-intensity closed loop. That is §6 of the robustness note applied to two different costs. It is not a property one cost has in sequence.

## Citations

Crossref HTTP 200 for every DOI in the acting-loop note, the proposal, and the acting-memory note, fetched again this session. Titles and authors match. Abstracts match the paraphrases that quote them. MacKay and Bar-Shalom were refused once with HTTP 429 and returned 200 on the retry.

| DOI | Record | What the note may say |
|---|---|---|
| `10.1115/1.3662552` | Kalman, *J. Basic Engineering* (1960) | The abstract says filtering is the dual of the noise-free regulator. The note says that, and no more. |
| `10.1115/1.3658902` | Kalman and Bucy (1961) | The abstract derives the Riccati equation and states the duality principle. "Not a separation theorem" is the right boundary. |
| `10.1137/0306023` | Wonham, *SIAM J. Control* (1968), "On the Separation Theorem of Stochastic Control" | No abstract. **KNOWN** for the title is accurate. The scalar calculation is the scalar case of that theorem. |
| `10.1038/nn963` | Todorov and Jordan, *Nature Neuroscience* (2002) | No abstract. The note does not identify the gain with a motor law. The title is the claim they decline. |
| `10.1103/PhysRevLett.104.090602` | Sagawa and Ueda, *Phys. Rev. Lett.* (2010), "Generalized Jarzynski Equality under Nonequilibrium Feedback Control" | No abstract. The heat in this file is not that equality. The nickname "the feedback equality" is this paper's generalized Jarzynski equality. |
| `10.1103/PhysRevX.4.031015` | Horowitz and Esposito, *Phys. Rev. X* (2014), "Thermodynamics with Continuous Information Flow" | No abstract. The shape attribution is the one this repository already uses. This note does not re-prove it. |
| `10.1162/NECO_a_00912` | Friston, FitzGerald, Rigoli, Schwartenbeck, and Pezzulo, *Neural Computation* (2017) | The abstract says action selection can be explained by minimizing variational free energy, and it asks whether neuronal responses are a gradient descent on that free energy. The note's paraphrase matches, and the note does not minimize a free energy. |
| `10.1080/14697688.2013.800219` | Taleb and Douady, *Quantitative Finance* (2013) | No abstract. The title names a mathematical definition. The note says that. |
| `10.1287/opre.2017.1663` | Russo and Van Roy, *Operations Research* (2018) | The abstract's sampling rule is the ratio of squared expected single-period regret to the mutual information between the optimal action and the next observation. The acting-memory paraphrase matches. |
| `10.1214/ss/1177009939` | Chaloner and Verdinelli, *Statistical Science* (1995) | The abstract is a decision-theoretic review of Bayesian experimental design. "One decision problem" is that framing. |
| `10.1162/neco.1992.4.4.590` | MacKay, *Neural Computation* (1992), "Information-Based Objective Functions for Active Data Selection" | The abstract discusses objective functions that measure the expected informativeness of candidate measurements. The paraphrase matches. |
| `10.1214/aoms/1177728069` | Lindley, *Ann. Math. Statist.* (1956) | No abstract. Cited for the title. |
| `10.1109/TAC.1974.1100635` | Bar-Shalom and Tse, *IEEE Trans. Automat. Control* (1974), "Dual effect, certainty equivalence, and separation in stochastic control" | No abstract. The acting-memory note cites the title and does not restate the theorem. The acting-loop note breaks certainty equivalence without citing this paper. |

No DOI in these three files failed, and no author or title was reassigned.

## How the pieces fit

Section 8 labels itself a synthesis. The layer, store, boundary, and turnover paragraphs each mark a prior theorem and then a **Conjecture**. The tying paragraph says each clause except the acting identities and the \(b=0\) reduction is a conjecture or a theorem from a class that did not contain the action. That labeling is the right one for those clauses.

The section calls the separation statement, and its two breaks, something proved here. The gain's independence of \(p\) is certainty equivalence for unconstrained linear-quadratic-Gaussian control. Wonham's title is that theorem. A cap on the variance, and a loss whose marginal value of variance is not the constant \(q\), are the standard boundary of the same theorem. Bar-Shalom and Tse's title is that boundary, and the acting-memory note already names it. The full-information gap \((q-2aP(a))\theta\) is the scalar linear-quadratic average cost. The frozen decimals are a calculation. They are not a new law, and §8 should not list them as one.

The \(b=0\) sentence in §8 is closer to the corollary than T46 is: it names the heat floor as the memory price and it restricts the proof to the quadratic regulation cost. It still omits \(\gamma_1=0\) and the fact that the quadratic minimum throws the channel away.

## The integer radius

The original preregistrations are untouched. `theory/boundary_checks/PREREG.md` has sha256 `58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c` at `main` and at head, the same blob. `theory/boundary_checks/PREREG_CROSSING.md` has sha256 `05f4d12445092d90ff48cbf20985b0e358c1d46ea17e74d1f294f1064cb40ae2` at both. Commit `7e45e3d` edits the boundary note and the T44 row only.

The rounding diagnosis is right. On \(\tau=1/2\) and \(\tau=1\), \(\Delta(1)/\Delta(0)\) is \(0.05283\) and \(0.1569\), and \(\Delta(2)/\Delta(0)\) is \(0.001351\) and \(0.01365\). The level \(0.05\) sits in \((1,2)\) at both times, so the smallest integer radius is \(2\) at both times and the integer ratio is \(1\). The path of \(61\) returns \(2\) and \(2\) again. The preregistration's next test did not clear the puzzle.

The smooth crossing is a different statistic, on times \(1/4\) and \(1\), and its ratio \(2.067863694520\) lies inside \([1.7,2.3]\). That prediction held. The note already says the integer radius moves from \(1\) to \(2\) on that pair. The integer was able to show a factor \(2\). It did not show one on the locked pair, because both crossings fell in the same bin.

The preregistration's rule is that a ratio \(\le 1.05\) is a puzzle, and that the claim stays a puzzle until a new preregistration of that test. `theory/boundary_checks/boundary_checks.py` still implements the rule: `in_band` requires \(1.05<\mathrm{ratio}<1.7\), and a ratio of \(1\) increments `PUZZLES`. The note's header, §0, §5, the label table, §9, and T44 now say the integer comparison is resolved. The checker was not changed. A later measurement of a different functional explains the miss. It does not convert the miss into a pass.

## House rules

The author's `theory/acting_loop_checks/acting_loop_checks.py`, at nice 19, prints `CHECKS 36`, `FAILS 0`, `PREDICTION-MISSES 0`. `tools/check_consistency.py` prints `RESULT: PASS` (`FAIL: 0`). `tools/check_open_work.py` prints `RESULT: PASS` (union missing from OPEN_WORK: 0). The image had no `pytest` module. After installing it, `python3 -m pytest` on `tools/test_acting_loop_checks.py`, `tools/test_acting_memory_checks.py`, `tools/test_check_consistency.py`, and `tools/test_check_open_work.py` passed 7 tests.

T46 is the new row. T43 and T44 on this branch are the rows already on `main`. T45 is the acting-memory row. The new id does not collide.

The acting-loop note, the proposal, the preregistration, the checks, the lock, the boundary-note edit, and the new OPEN_WORK rows use cost. The words bill, kill, and verdict do not occur in that diff. Older OPEN_WORK rows still carry the historical kill-rule wording. This branch does not add to it.

## Required fixes

Do not edit `theory/acting_loop_checks/PREREG.md`, `theory/boundary_checks/PREREG.md`, or `theory/boundary_checks/PREREG_CROSSING.md`.

**F1. The thirty-three lines are evaluations of §4.** In the acting-loop note's header and in §9, replace "33 predictions, misses 0" with this:

> 36 checks, FAILS 0. The 33 lines in §5 of the preregistration evaluate the expressions in §4 of that file, or restate a sign §4 already gives. The preregistration says the decimals are the values of those expressions and that a later script may only evaluate them. The lock is six seconds after the commit that contains the decimals. Misses 0 is agreement with that arithmetic.

In T46, add the same sentence after the hash. In the pull-request body, replace "All hit." with the same sentence. Keep the decimals.

**F2. The second derivative \(-0.321714500038\) is not the acting-memory variability score.** In §5 of the acting-loop note, keep Proposition AL-shape as a statement about the fixed intensity \(u_o=4\). Add to it: this \(J\) is not the minimum at stake \(1\). Replace the paragraph that begins "The capped sign cost minimized in the acting-memory note" and the following payoff paragraph with:

> The acting-memory variability score is the second derivative of the minimized sign cost, \(0.313020858054\). The fixed-fraction spread at half-width \(1/10\) is \(0.001839996934\) and the re-optimized spread is \(0.001577268119\). A spread of \(\theta\) raises that minimized cost. The second derivative \(-0.321714500038\) is the closed-loop cost at stake \(1\) and fixed intensity \(u_o=4\). P2 says that intensity is dearer than sensing alone. The minimizing design at stake \(1\) is the blind cost \(q\theta\), whose second derivative is \(0\), so a spread does not lower the cost the hypothesis minimizes at that stake. The fixed-intensity slice is concave for every \(\theta>0\). That concavity belongs to a design the cost does not select. This note does not score the spread of the minimizing closed loop.

**F3. \(Q_{\mathrm{fin}}\) replaces \(kT\,L\).** In §1 of the acting-loop note, replace "plus the finite-rate factor \(Q_{\mathrm{fin}}\)" with "or, when the finite-rate spring is charged, the Sekimoto heat \(Q_{\mathrm{fin}}\) in place of \(kT\,L\)". State that both equal \(10/9\) at the frozen point only because \(L=1\). In §3, label the independence of \(L\) from \(K\) as **PROVED**, and label the absence of \(K\) from \(Q_{\mathrm{fin}}\) as a property of the exogenous formula in Proposition AT-attain. The physical heat of a spring tracking the controlled state stays the conjecture the proposal already states. Add one sentence that AL-H's word "plus" has the wrong relation to that proposition and stays in the locked file. The checks charge \(kT\,L\) and report \(Q_{\mathrm{fin}}\) beside it.

**F4. The sum is not R1's shape under A7-act.** In §2 of the proposal, replace "The additive shape is R1's shape, with the memory coordinate priced at the heat rather than at \(\kappa I_{\mathrm{mem}}\)." with:

> The sum below is a specification inside class AL. Theorem R1 does not apply to it. R1 assumes A7, and A7 says both that the world law does not depend on the design and that effort spent changing the drift is not a coordinate. A7-act drops the first and adds the second. The memory coordinate is priced at the heat rather than at \(\kappa I_{\mathrm{mem}}\) by this specification.

Leave the adoption labeled **CONJECTURE**. Leave "PROVED as an accounting identity" only if the sentence says the identity is the sum of the coordinates just chosen.

**F5. Say what the \(b=0\) minimum equals.** In the proposal's corollary, replace "That is the master equation in this scalar class, on an exogenous world." with:

> At \(\gamma_1=0\) the quadratic minimum equals the stake term \(q\theta\), because the minimum has set the channel, the actuation, the layer upkeep, and the link term to zero. Restoring a loss that uses the observation, and pricing memory at the heat and acquisition at the probe, is this proposal's scalar special case of the sum. It is not Theorem R1 applied at \(b=0\).

In §8 of the acting-loop note, in T46, and in the pull-request body, replace "reduces to the scalar master equation" with that statement. Keep the variance identity \(v=\theta\), which is exact for every finite gain.

**F6. Separation is the scalar linear-quadratic-Gaussian theorem.** In §4, after the display of \(K^\star\), write that this independence of \(p\) is certainty equivalence for unconstrained linear-quadratic-Gaussian control, the scalar case of Wonham, doi `10.1137/0306023`, and that a cap on \(v\) or a loss whose marginal value of variance is not \(q\) is the boundary named by Bar-Shalom and Tse, doi `10.1109/TAC.1974.1100635`, already cited by title in the acting-memory note. In §8, replace "the separation and its two breaks" as items "proved here" with: the separation statement and its two breaks are that theorem and that boundary, evaluated at the frozen point. The full-information gap is the scalar linear-quadratic average cost, evaluated at three values of \(a\). The frozen decimals are the calculation.

**F7. The integer \(5\%\) radius stays a puzzle.** In the boundary note's header, §0, §5, the label table, §9, and in T44, replace "resolved as a measurement" with a puzzle. Use this table cell:

> **OPEN**, a puzzle. The locked integer ratio is \(1\), on paths of \(31\) and \(61\). Both crossings of the level \(0.05\) on \((\tau=1/2,\tau=1)\) lie in \((1,2)\), so the whole-step radius is \(2\) at both times. The path of \(61\) was the next test named in the preregistration, and it returned \(2\) and \(2\). The preregistered smooth crossing is a different statistic: ratio \(2.067863694520\), inside \([1.7,2.3]\), so that doubling prediction held. The checker still files P9 as a puzzle. The original preregistrations are not edited.

Keep the sentence that a doubling of a crossing near \(1.05\) would have moved the integer to \(3\). Keep the smooth-crossing row as a pass of its own band.

## Recommended fixes

**R1.** Retitle §3 of the acting-loop note. The sentence to lead with is the one the body already proves: feedback shrinks \(\tfrac12\ln(v/p)\), and the learning-rate heat stays fixed. Keep the **METAPHOR** mark on calling that heat a memory of the action.

**R2.** If a payoff sentence stays in §5, cite `theory/ROBUSTNESS.md` §6 and apply it to the function just differentiated. Delete the parenthetical "concave, then convex." It does not occur elsewhere in the repository, and it does not change the acting-memory result.

**R3.** In the checks, form the independent-arm posterior and vary \(p\) in the gain. `Decimal(1) == 1` and two calls of `K_of(1,1)` do not test those sentences. Do this in the script only. Do not edit the preregistration to create a new prediction after the fact.

**R4.** Name Sagawa and Ueda's paper as the generalized Jarzynski equality under feedback, which is its title, wherever the note says "the feedback equality."

**R5.** The unlabeled citations in the proposal — night-1 Axiom 5, Theorem R2, and the acting-memory independence proposition — should carry **STANDARD** or the name of the proposition. "At \(b=0\) it is A7" should say the law of \(X\) is A7 and the coordinate list still contains the actuation price. Booking the Cox price in the acquisition coordinate should be labeled as a specification.

**R6.** A spread of the minimizing closed loop is a new preregistration, not a patch on this note. At stake \(4\), on \(\theta\in\{0.9,1.0,1.1\}\), this review's minimization of the direct cost gives a spread of about \(-0.003507\). That number was not locked. Leave it out of the note.
