# Review of the growth bridge (draft PR #166)

*Independent review of draft PR #166, branch `growth-bridge-2026-11-22`, head `0d50e2f`. The reviewer wrote none of `theory/GROWTH_BRIDGE.md`, section X, or `tools/growth_bridge_checks.py`. Same bot family, so a second reader, not a blind human grader. The PR branch was not edited. Every displayed number below was recomputed with a separate script (Newton on the B9 numerator, exact moments, Crossref fetched again). The author's suite was then run, and it agrees.*

## Verdict

**READY-WITH-FIXES.** No blocker.

The statuses can stand: GB1 and GB4 **PROVED (in-model)**, GB2, GB3, GB5, and GB6 **FALSE**, GB7 **OPEN**. The master equation remains an assumption. The fixes below are local: one broken proof chain, one mislabeled example, and counterexamples that answer a different question from H3. None of them flips a row.

**The sentence.** On a finite menu whose expected-offspring gap stays fixed as the noise scale goes to zero, growth selection and expected-offspring selection pick the same design, and that design minimizes a linear cost only when the cost is already the form of the offspring mean, while the diffusion limit ranks by \(\mu-\sigma^2/2\), an interior stake separates the two argmaxes, and neither limit produces the term list or the ruin cap, so the master equation remains an assumption outside that scoped ranking.

The replacement "the master equation is the weak-selection limit of growth selection when costs enter offspring linearly with a fixed gap; it fails at finite stakes (Kelly)" identifies the equation with the ranking. The ranking is what that limit returns. The term list and the cap are not in it, and the diffusion limit is a second failure of risk-neutral ranking even after the step has gone to zero.

## Blockers

None.

## Should-fixes

1. **`theory/GROWTH_BRIDGE.md:142`.** The Galton–Watson chain does not prove the asymptotic it is attached to. The expansion of \(f(1-s)\) gives \(s=ms-(\beta_2/2)s^2+O(s^3)\), hence \(s(m-1)=(\beta_2/2)s^2+O(s^3)\), hence \(s\sim 2(m-1)/\beta_2\). The displayed predecessor \(s=(m-1)s+\beta_2 s^2/2+O(s^3)\) is a different equation, and the "hence" does not follow from it (that equation rearranges to \(s(2-m)=\beta_2 s^2/2\)). The "hence" line itself is the correct identity, and the final display is the correct asymptotic. At criticality \(\beta_2=\mathrm{Var}(W)\) is right, because \(f''(1)=\mathrm{Var}(W)+m^2-m\). Poisson ratios against \(2(m-1)\), recomputed, are \(0.998668\), \(0.986821\), and \(0.937018\), which round to the printed \(0.9987\), \(0.9868\), and \(0.9370\). Repair the chain before that clause is cited as proved by this text. GB4 stays **PROVED**: the formula is the standard one, the ratios confirm it, and the birth-death, Feller, Brownian, and B9 arguments do not use this line.

2. **`theory/GROWTH_BRIDGE.md:102`, `measurement/CLAIM_MAP_v2.md:710`, `tools/growth_bridge_checks.py:125`.** The heading "equal means" sits on a law with \(\mathbb{E}[X]=0.05\), not \(0\). The arithmetic is a different, true fact: mean excess \(0.01\), growth \(\lambda_B=-0.010274369557\). Expected offspring picks B and growth picks A. The equal-mean, unequal-second-moment ranking is Gillespie's 1977 principle and is not this example (at \(\varepsilon=0.2\), \(X=\pm 1\) with equal probability has growth \(-0.020411\)). The claim-map clause that both that case and the third-moment tie "are tied by the truncated criterion" cannot be true of one truncation: the second-order truncation ties the third-moment pair and separates the equal-mean pair; the first-order truncation ties both. GB3 stays **FALSE** on the diffusion sign flip and the Kelly pair, which recompute exactly. The green check asserts `mean_b > 0.009`, so the suite does not police the heading.

3. **`theory/GROWTH_BRIDGE.md:225`–`233` and `measurement/CLAIM_MAP_v2.md:713`.** Retarget the resource witnesses. H3, Lemma LY (`theory/GENERAL_FORM.md:48`), is the partial: offspring strictly decreasing in each coordinate of the chosen bad vector, the other coordinates held fixed. The memory, acquisition, attention, and learning-loss counterexamples let the benefit move. They are total derivatives. They leave the partial untouched. GB6 stays **FALSE** for "from first principles." The table should stop saying those four examples are why H3 fails. Per-coordinate verdicts are in the section below.

4. **`theory/GROWTH_BRIDGE.md:70`.** A stray `|` opens the displayed GB-diff identity. The identity without the bar is what the proof gives and what GB1 states: \(\mathbb{E}[\log W]=\mathbb{E}[W-1]-\mathrm{Var}(W)/2+O((\Delta t)^{3/2})\).

5. **`theory/GROWTH_BRIDGE.md:98`.** The menu proof divides by \(\varepsilon\) and says the result tends to \(\gamma\). That uses a bound on \(\mathbb{E}[X_i^2]\) independent of \(\varepsilon\). Lyapunov's inequality gives it from the stated hypothesis: \(\mathbb{E}[X_i^2]\le M^{2/3}\). One sentence closes the proof. The theorem is true.

6. **`theory/GROWTH_BRIDGE.md:272`.** "What this note adds" lists the Kelly stake, the extinction and hitting formulas, and the Taylor expansion among the additions. Those are Kelly 1956, Haldane 1927, Feller 1951, the Cramér–Lundberg diffusion formula, Gillespie 1977, and Taylor's theorem, and §7 already says so. The addition is the separation of the two limits as answers about this equation, the squared-mean obstruction, \(\tau_G\) and the split cap on the published path, and the coordinate audit.

7. **`measurement/CLAIM_MAP_v2.md:711`.** "Each level set is a half-space in the exponent coordinate" drops the note's own caveat at line 144: the Galton–Watson half-space in \((m-1,\beta_2)\) exists after the linear approximation. Birth-death, Feller, and Brownian are exact half-spaces, and the B9 preimage in \(\tau\) is a bounded interval. The note already says this. The row should say it.

8. **`OPEN_WORK.md:81`.** T33's parenthetical groups GB2 with "the term list, the cap, and H3 remain assumptions." GB2 is a false unscoped identity. The assumptions that remain are the term list, the cap, and H3.

## GB3, against GB1

Weak selection with a fixed gap does give a legitimate derivation of a ranking. It does not give a derivation of the master equation.

Theorem GB-menu is proved. On \(W_i=1+\varepsilon X_i\) with \(\varepsilon|X_i|\le 1/2\), a uniform third-moment bound, and a unique mean leader ahead by a fixed \(\gamma>0\), small \(\varepsilon\) makes \(\arg\max\lambda=\arg\max\mathbb{E}[W]\). The second-moment term is order \(\varepsilon^2\) and cannot flip a gap of order \(\varepsilon\). If, in addition, the offspring mean is already an affine decreasing function of a linear cost, the common argmax is the minimizer of that cost. The cost in that sentence is an input. Corollary LY-c and the exponential map \(W=\exp(-\varepsilon C)\) are the same input: \(\lambda=-\varepsilon\mathbb{E}[C]\) exactly, because the logarithm has been undone, and the term list was supplied from outside.

Two other limits do not return that ranking.

- Diffusion scaling keeps the penalty at the same order as the drift. For \(\mu=0.2\) and \(\sigma^2=0.5\) the limiting growth rate is \(-0.05\). At \(\Delta t=10^{-4}\) the realized rate is \(-0.049998250\). Doing nothing, rate \(0\), beats the risky design on growth and loses on expected offspring. Sending the step to zero does not remove the disagreement: both pieces are order \(\Delta t\) per step and order \(1\) per unit time. A design-independent variance rate would leave the ranking equal to the drift ranking. The row denies the universal claim, and the universal claim is false.
- An interior stake is Kelly's criterion. Even money, win probability \(0.6\), \(f\in[0,0.99]\): \(\lambda'(f)=0\) at \(f^\star=0.2\), \(\lambda(0.2)=0.020135513551\), and \(\mathbb{E}[W-1]=0.2f\) is maximized at \(f=0.99\). Replacing the factor by \(1+\varepsilon f\xi\) with \(f\in[0,1]\) puts both argmaxes at the corner \(f=1\) once \(\varepsilon<0.2\), because the Kelly stake \(0.2/\varepsilon\) has left the box. Restoring the box to \([0,1/\varepsilon]\) separates them at \(0.2/\varepsilon\) and \(1/\varepsilon\) for every \(\varepsilon\). Vanishing exposure recovers expected-offspring selection by pushing the growth maximizer out of the feasible set.

GB3's sentence is "diffusion scaling, or an interior stake, reduces maximization of \(\lambda\) to risk-neutral expected currency." Both disjuncts fail. **FALSE** is the right label. The row does not deny GB1. A reader of the table alone can miss that. Should-fix 2's repair should add one clause: the weak-selection menu of GB1 is a different limit.

GB1's **PROVED** label is earned. The expansion, the Lagrange bound \(|R_2|\le(8/3)|X|^3\) on \(|X|\le 1/2\), and the diffusion limit were recomputed. On a grid of \(|x|\le 1/2\) the remainder stays inside the bound; the largest ratio of remainder to bound on that grid is about \(0.20\). For symmetric \(Z=\pm 1\), \(\mathrm{Var}(W)=\sigma^2\Delta t\) exactly. The note's \(O((\Delta t)^2)\) (line 67) is a true and loose bound. Nit.

## GB6, per coordinate

H3 is the partial. Memory, acquisition, and attention, read as resources spent at fixed task performance, are the left-hand column of the table: a budget map. That map is an assumption. A positive marginal price makes offspring strictly decreasing. A zero price makes it weakly decreasing, so H3's strictness fails for a free resource. A side benefit that is not among the coordinates held fixed can reverse the sign. Copying does not supply the map. "From first principles" is false for every coordinate below, and the row stays **FALSE**. The right-hand column does not always witness the partial.

| Coordinate | Verdict |
|---|---|
| Memory | At fixed loss path, \(\log W=-\kappa I-\ell\) has partial \(-\kappa\). The counterexample \(W=\exp(-e^{-2I})\) has total derivative \(2e^{-2I}>0\) because the loss falls, and partial derivative \(0\) in \(I\) once that loss is held fixed. Offspring does rise from \(0.367879441171\) to \(0.873423018493\). That rise is the benefit. It does not refute the partial. The strict partial is the budget assumption. |
| Acquisition | Same structure. \(\log W=-r-4e^{-r}\) has partial \(-1\) in \(r\) at fixed loss term, and total derivative \(-1+4e^{-r}\), positive on \([0,\log 4)\). The rise from \(0.018315638889\) to \(0.084456576466\) is the total derivative. The partial at fixed task loss is the budget assumption, strict when the read has a positive price. |
| Task loss | This coordinate is the performance bad, so "holding task loss fixed" is not the question about it. Pathwise \(W=\exp(-w\,\ell)\) decreases in \(\ell\) by the map that was put in. Expected loss fails H3, and LY-1 is the right witness: resource and error \((1,0)\) with offspring \(4\) and \(0.05\) has \(\lambda=-0.804718956\); \((2,0.4)\) with offspring \(1.1\) has \(\lambda=0.095310180\). The smaller expected-bad vector has the smaller growth rate, and both offspring numbers are positive. The learning pair, loss \(0\) with offspring \(1.1\) against loss \(1\) with offspring \(3\), lets the loss buy a later return. It is a total derivative and is the wrong witness for a pure loss. |
| Ruin | The scalar \(P(\mathrm{ruin})\) is a functional of the law, not a coordinate of \(W(\omega)\). Holding the ruin event fixed leaves no separate probability to differentiate. \(W\equiv 1.2\) at probabilities \(0.01\) and \(0.20\) does not move offspring. \(W=0\) on the ruin event sends \(\mathbb{E}[\log W]\) to \(-\infty\) and breaks \(W>0\). No reasonable budget model creates a pathwise strict decrease in the scalar. This witness is the right one. GF2 already says the master equation's cap is a modelling choice and is not H3. |
| Attention | THEORY §3 names attention as one currency ("heat, attention, money, compute"). GF2 already says a fifth peer coordinate repeats that currency. H3 on attention as a peer is the wrong question. If attention is instead a resource at fixed task loss, the budget partial is \(-c_a\), and \(\log W=-4e^{-a}\) is again a total derivative through a falling loss. The rise from \(0.018315638889\) to \(0.229576777100\) does not refute the partial. |

The left-hand column is the honest positive statement: each decreasing model adds a pure-waste map or an exponential map. That is why H3 is not derived. The right-hand column, for four of the five coordinates, changes the question.

## GB5, the four points

The four numbers are right, by an independent Newton solve on the numerator of \(\theta'\), not by the note's bisection. There is one sign change of that numerator on the positive-margin interval \((0.0513167019495,\,1.9486832980505)\).

| Point | Recomputed | Printed |
|---|---|---|
| \(\tau_S\) | \(0.236207526722077\) | \(0.236207526722\) |
| \(\tau_G\) | \(0.302668099260496\) | \(0.302668099260\) |
| \(\tau_{\mathrm{cap}}\) | \(0.299049733488227\) | \(0.299049733488\) |
| \(\tau_E\) | \(0.316227766016838\) | \(0.316227766017\) |
| \(\tau_{\mathrm{lo}}\) | \(0.183706411069500\) | \(0.183706411069\) |
| \(\tau_J\) | \(0.309679835107737\) | \(0.309679835108\) |
| \(\theta_{\mathrm{req}}\) | \(13.815510557964274\) | \(13.815510557964\) |

\(\tau_G\) solves \(\tau^4+\tau^2-0.1=0\). The residual is \(4\times 10^{-17}\). \(J(\tau_E)=\tau_E\), \(J(\tau_{\mathrm{cap}})=0.316721136799\), \(J(\tau_S)=0.329782030747\).

The four points are optima of different problems. They show an objective gap, and they show a cap.

- Slack cap, any requirement at most \(\theta(\tau_E)=13.601868698785\): both unconstrained points are feasible, and they differ by \(0.013560\). \(\phi(\tau_G)=0.633847>\phi(\tau_E)=0.633502\).
- Published cap, \(\varepsilon_r=10^{-3}\), \(B=0.5\): \(\tau_G\) and \(\tau_E\) both lie to the right of \(\tau_{\mathrm{cap}}\). On the feasible interval \(J\) is still decreasing (\(J'(\tau_{\mathrm{cap}})=-0.0591\)) and \(\phi\) is still increasing (\(\phi'(\tau_{\mathrm{cap}})=+0.0144\)), so both constrained criteria sit on \(\tau_{\mathrm{cap}}\). This cap hides the objective gap. \(\tau_S\) stays inside and is a third criterion.
- Split cap, the midpoint of \(\theta(\tau_G)\) and \(\theta(\tau_E)\): \(\tau_G\) remains feasible, expected cost prefers \(\tau_J\), and \(J(\tau_J)=0.316297<J(\tau_G)=0.316532\).

So the master equation on this path, minimize \(J\) inside a cap on \(\theta\), is a different criterion from diffusion-limit growth, maximize \((y-J)-s^2/2\). The difference survives a slack cap and a split cap. It is not only a difference of caps. The published cap is the special case in which the two constrained optima coincide. The note says this at lines 206–208, and the claim-map row cites the slack cap and the split cap. That is the right evidence for **FALSE**.

\(\phi\) is the diffusion limit of a multiplicative factor with this path's margin and variance rate. The note says so, and says the additive reserve's drift is \(y-J\). The B9 table is that diffusion comparison. The finite-stake gap is the Kelly example in §3, a separate counterexample, and it also stands.

The level sets that were actually derived are half-spaces in \((m-1,\beta_2)\) after linearization, in \((\log b,\log d)\), in \(\alpha/\beta\), and in \(\theta=2\mu/\sigma^2\). They are not half-spaces in memory, acquisition, task loss, and attention. The birth-death threshold at extinction probability \(0.05\) from \(z=20\) founders is \(b/d\ge 1.161586349642\), a threshold on a growth ratio. The Feller generator residual on \(\exp(-\alpha z/\beta)\) is \(0\), and the Brownian generator residual on \(\exp(-2\mu x/\sigma^2)\) is \(0\).

## Prior art

Nothing in the Taylor expansion, the menu comparison, \(\mu-\sigma^2/2\), Kelly's \(f^\star=0.2\), the equal-mean variance ranking, Haldane's factor \(2(m-1)\), the Feller extinction formula, or the Brownian ruin formula is new. §7 credits them, and the credit matches the papers. The overclaim is should-fix 6: the same items reappear under "what this note adds."

The separation the note does make is the right one, and DYNAMICS already supports the Gillespie half of it. Gillespie 1974, as DYNAMICS line 163 uses it, is an \(O(1/N)\) within-generation correction and vanishes for an infinite population. The penalty here is the infinite-population Lyapunov correction and remains at infinite \(N\). Gillespie 1977 is the geometric-mean ranking. Lande's weak-selection gradient is already SA3. Cohen 1966 is already CL20. Lundberg on the published path, \(\tau_S\) against \(\tau_E\), is already V2. PD6 is a statement about a mutual-information stock. The three rankings on \((\mu,\sigma^2)\) were recomputed: \((0.30,0.40)\) against \((0.20,0.10)\) has drift, diffusion growth, and Lundberg picking first, second, and second; \((0.30,0.20)\) against \((0.16,0.08)\) has diffusion growth and Lundberg picking opposite designs.

The third-moment gap is \(1.905984\times 10^{-5}\) against the cubic prediction \(2.083333\times 10^{-5}\). The difference, \(1.773\times 10^{-6}\), is the quartic term for \(\Delta\mathbb{E}[X^4]=1.25\), which is \(-1.953\times 10^{-6}\), plus a fifth-moment piece of about \(2\times 10^{-7}\). The check's tolerance of \(2\times 10^{-6}\) is that quartic. There is no hidden algebra error. The coin, the CT43 pair, and the birth-death extinction probability \(0.148643628024\) match to the printed digits.

## Labels

| Row | Label in the draft | After recomputation |
|---|---|---|
| GB1 | PROVED (in-model) | Stands. Ranking agreement on a gapped finite menu, and \(\mu-\sigma^2/2\) under diffusion scaling. Repair the stray bar and name the second-moment bound. |
| GB2 | FALSE | Stands. Deterministic \(W=1.2\) is inside the disk \(\|X\|\le 1/2\): \(\log 1.2=0.182321556794\), and the dropped term \((\mathbb{E}[W-1])^2/2=0.02\) is larger than the cubic piece \(0.002\overline{6}\). The scoped remainder does not rescue an identity that drops the squared mean. |
| GB3 | FALSE | Stands, for diffusion scaling and for an interior stake. The weak-selection ranking is GB1 and is not this row. Repair the equal-means clause. |
| GB4 | PROVED (in-model) | Stands for the formulas and for the B9 interval. The Galton–Watson chain has to be rewritten before that one clause is cited as proved by the display. |
| GB5 | FALSE | Stands. The hitting geometry is a penalty and a level set in the exponent coordinate. The objective inside a cap is whichever criterion is optimized there. Slack and split caps separate \(\tau_G\) from expected cost. |
| GB6 | FALSE | Stands for "from first principles." The resource counterexamples do not show that the partial fails at fixed task loss. |
| GB7 | OPEN | Stands. No locked preregistration. |

The package sentence in §6, "maximizing \(\lambda\) in a small-noise limit yields the master equation," is false as a package. Each of the stake counterexample, the diffusion sign flip, the third-moment tie, and the split cap is enough to stop the identification of the two objectives. The term list and the cap remain inputs. That is the right strength. It does not undersell the ranking theorem, which §0 and GB1 state, and it does not oversell the equation into a theorem.

`THEORY.md:39` points at this note and states the same split: weak selection ranks a gapped finite menu with expected offspring, the diffusion scaling keeps the penalty, the level set on the published path is a bounded interval of refresh time, and the term list and the cap remain assumptions. That paragraph matches the recomputation.

The v2.81 tally arithmetic is \(371\to 378\), which is the seven new rows: PROVED \(124\to 126\), OPEN \(93\to 94\), FALSE \(0\to 4\). The note's parenthesis says "FALSE 4" where the other counts use an arrow. Nit. `tools/check_consistency.py` counts 378 rows and the tally matches. The four FALSE rows are GB2, GB3, GB5, and GB6.

## Hypothesis sentence

The sentence in `theory/GROWTH_BRIDGE.md:11`, `THEORY.md:41`, and `CORE.md:9` is one and the same byte string, once in each file:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

The note contains no `bill`, no `kill`, no `verdict`, and no `theory of everything`. The checker's scan of the note agrees.

## DOIs

All thirteen DOIs were resolved on the Crossref API in this review, with a different user agent from the note's script. Title, year, and authors match §7 and match `theory/growth_bridge_checks/crossref.out`. The Cramér DOI returns the collected-works issue, year 1994, title "Collective risk theory: A survey of the theory from the point of view of the theory of stochastic processes." The note discloses that year. Lundberg's 1903 thesis is cited with no DOI. No mismatch.

## Commands

Run from the repository root on `growth-bridge-2026-11-22` at `0d50e2f`, after `git fetch origin main`. `origin/main` is `2d9a812`. The merge-base of the PR head with `origin/main` is `2d9a812`; the branch is one commit on top. Lake was not built. Pytest was absent in the image; `pytest`, `numpy`, `scipy`, and `sympy` were installed for the suite only.

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | `RESULT: PASS`, FAIL 0, 378 rows, tally 378 |
| `python3 tools/check_fresh.py` | `RESULT: PASS`. STATUS's `main` is `01e4415`, inside the window `2d9a812 01e4415 2dd04fa 37794bb f84997c` |
| `python3 tools/check_open_work.py` | `RESULT: PASS` |
| `nice -n 19 python3 tools/growth_bridge_checks.py` | `FAILS 0`, `ALL GROWTH-BRIDGE CHECKS PASS` |
| `nice -n 19 python3 -m pytest -q tools` | `252 passed, 1 skipped in 305.74s`. The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed." |

## Nits

- `theory/GROWTH_BRIDGE.md:67`. For \(Z=\pm 1\) with equal probability, \(\mathrm{Var}(W)=\sigma^2\Delta t\) exactly.
- `tools/growth_bridge_checks.py:156`. The "gapped menu" check is \(\log 1.01>0\). It does not exercise a rival design.
- `measurement/CLAIM_MAP_v2.md:86`. Write FALSE \(0\to 4\), in line with the other arrows.
- `STATUS.md:3`. The one-line summary states the menu agreement and that the equation remains an assumption. The diffusion limit, which keeps the penalty, is the fact a one-line reader most needs beside those two.
