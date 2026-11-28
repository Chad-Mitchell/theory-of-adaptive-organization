# Hostile review of draft PR #197

Sunday 22 November 2026. Independent review of https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/197. Head `733d732f1ce30880bd674f333cf523cfddfe0466` on `acting-memory-2026-11-22`, branched from `13eec9af`. The pull request is open against `main` at `b6e351ee`. The diff against the branch point is eight files: `theory/ACTING_MEMORY_2026-11-22.md`, `theory/acting_memory_checks/PREREG.md`, `theory/acting_memory_checks/LOCK.txt`, `theory/acting_memory_checks/acting_checks.py`, `theory/acting_memory_checks/results.out`, `theory/acting_memory_checks/crossref.out`, `tools/test_acting_memory_checks.py`, and one row, T45, in `OPEN_WORK.md`. This review edits none of them. It does not merge the draft. No lake build.

The arithmetic recomputes. The level drop is real inside the locked class, and it is signal-to-noise scaling: a larger signal against noise that does not grow with the signal makes a given look cheaper. The cost is convex in the variance, so a spread of the variance raises the cost. On the repository's reading of Taleb and Douady, that spread is the variability score, and this point fails it. The grid comparison against 5 is a puzzle, and the diagnosis in the note is the right one. The scored action does not enter the world equation. The next preregistration has to put an action in the drift and a failure rate on the world.

## The level effect and the variability effect

`theory/ACTING_MEMORY_2026-11-22.md:9`, `:86`–`:90`, `:108`–`:112`. `theory/acting_memory_checks/PREREG.md:15`–`:16`. `theory/ROBUSTNESS.md:198`–`:200`. The T45 row is `OPEN_WORK.md:94` on `733d732`.

The stressor is the stationary variance \(\theta\) of one exogenous Ornstein–Uhlenbeck signal. The error fraction is \(r=p/\theta\). With a probe price \(\alpha u\) and fixed observation noise, the cost in the fraction is
\[
J(r,\theta)=\frac{A(r)}{\theta}+C(r),
\]
where \(A(r)=\alpha\cdot 2a(1-r)/r^2\) is the probe price of holding \(r\), and \(C\) is the heat plus the sign loss. Both pieces of \(C\) depend on \(\theta\) only through \(r\).

At an interior minimum the envelope theorem gives
\[
\frac{\mathrm d J^*}{\mathrm d\theta}=-\frac{A(r^*)}{\theta^2}.
\]
At the frozen point \(a=kT=1\), \(w=16\), \(\theta=1\), \(r=1/2\), the price \(\alpha=(4-\pi)/(6\pi)\) was chosen so that this \(r\) is critical. Then \(A(1/2)=2(4-\pi)/(3\pi)\) and
\[
J^*=5.182159696490,\qquad \frac{\mathrm d J^*}{\mathrm d\theta}=-0.182159696490.
\]
Those two numbers are the critical point the price was built to sit on. The slope is negative because \(\pi<4\), which is the same condition that makes \(\alpha\) positive. The result that is not that normalization is the locked global statement: for every \(\alpha>0\), \(J^*\) is strictly decreasing on \((0,\infty)\), because raising \(\theta\) discounts \(A(r)\) and the minimizing fraction can be reused at the higher \(\theta\).

The heat slope \(2/3\) is the partial derivative of the heat at fixed intensity \(u=4\). At that same fixed intensity the sign loss contributes \(-8/(3\pi)\), and the sum equals the envelope slope. That is a split of one derivative along a path that refuses to retune \(u\). Along the path the minimizer actually takes, \(r\) moves. At \(\theta=1\) the three along-path derivatives are

| piece | derivative along \(r^*(\theta)\) |
|---|---|
| probe price | \(-0.130861161564\) |
| heat | \(+0.187741986525\) |
| sign loss | \(-0.239040521451\) |
| cost | \(-0.182159696490\) |

The heat does rise along \(r^*\). On the locked grid it rises from \(0.489783491207\) at \(\theta=1/8\) to \(1.219277153061\) at \(\theta=8\), while \(J^*\) falls from \(5.911577251205\) to \(4.998066177768\). The number \(2/3\) is the other path's heat slope. Pairing \(2/3\) with the minimized-cost slope, in the opening and in T45, reads as one derivative's two pieces. They sum only in the fixed-intensity split.

Both paths are signal-to-noise. The process-noise intensity is \(2a\theta\) and the observation-noise density is \(1/u\). Raising \(\theta\) against noise that stays put raises the signal relative to the noise. At fixed \(u\), the error fraction falls, the bounded sign loss falls, and the heat rises like \(\sqrt{\theta}\). At fixed \(r\), the intensity that holds the fraction scales as \(1/\theta\), so a probe price that is not itself proportional to \(\theta\) falls as \(1/\theta\). The whole first-order fall in the minimized cost equals that fall in the probe price. A bigger signal against fixed noise makes looking cheaper.

The variability score is the other definition, and the preregistration already separates them. Taleb and Douady, as `theory/ROBUSTNESS.md` §6 reads them, make the cost antifragile to a stressor when the cost is concave in the stressor, so a mean-preserving spread lowers the expected cost. At \(\theta=1\),
\[
\frac{\mathrm d^2 J^*}{\mathrm d\theta^2}=0.313020858054>0.
\]
The algebraic reduction of that sign to \(44+\pi\) holds. A fixed-fraction spread of half-width \(1/10\) raises the cost by \(0.001839996934\). The re-optimized spread at the same width raises it by \(0.001577268119\). Retuning shrinks the Jensen gap and leaves it positive. On a sweep of \(\theta\) from \(1/4\) to \(39/4\) in steps of \(1/4\), the second derivative stayed positive. That sweep is a check, not a proof of convexity on the whole half-line. The proof the note gives is the right one for the ray: a strictly decreasing cost that is bounded below cannot be concave on any \((\theta_1,\infty)\), because a negative slope that keeps falling runs to \(-\infty\). \(J^*\) is cheaper at a higher level of \(\theta\) and dearer under a spread of \(\theta\).

R4(a) in the robustness note is the case where the error is affine in the variance scale, so the best cost cannot fall as the level rises. The departure here is the bounded sign loss together with a probe price that scales as \(1/\theta\). It is a different loss and a different price. It is the same stressor, read at its level and at its spread, which the preregistration already defined as two scores.

**Repair.** In §0, in the fixed-intensity paragraph of §4, and in T45, write the envelope identity \(\mathrm d J^*/\mathrm d\theta=-A(r^*)/\theta^2\), label \(2/3\) as the fixed-intensity heat partial, and give the three along-path derivatives. Say the level effect is the probe price of a given fraction falling as \(1/\theta\). Say the positive second derivative and the positive re-optimized spread are the variability score, and that this is the concave-cost reading already in `theory/ROBUSTNESS.md` §6. Say that \(5.182159696490\) and \(-0.182159696490\) are the critical point built by \(\alpha\).

## The naked option, and the "exactly when" puzzle

`theory/ACTING_MEMORY_2026-11-22.md:11`, `:128`, `:132`, `:150`, `:152`, `:154`, `:156`, `:158`. `theory/acting_memory_checks/PREREG.md:5` and `:186`.

The hypothesis under test said that a falling cost arises exactly when the probe price is capped and the probe's information makes the learning rate rise with volatility, and that the cost is then concave. The preregistration scored that sentence as four separate claims and called a miss a puzzle. The evaluation keeps the numbers and does not edit the preregistration. That is the right handling. The grid clause is the one locked sentence the numbers contradict, and the diagnosis is right. The learning-rate sentence is the one the controls do not identify.

**The grid clause.** P3 predicted that \(J^*\) at \(\theta=8\) would sit strictly above \(5\). It is \(4.998066177768\), short by \(0.001933822232\). \(C(1/2)=5\) is the heat plus the sign loss at the frozen fraction. The locked algebra already says the floor is at most \(5\), because the floor is \(\inf C\) and \(C(1/2)\) is one value of \(C\). The diagnostic minimum of \(C\) is \(4.966383544211\) at \(r=0.441594095399\). \(J^*\) crosses \(5\) at \(\theta\approx 7.5267230646\). Re-optimizing \(r\) as \(A(r)/\theta\) shrinks pulls the cost toward that floor, and by \(\theta=8\) the pull has crossed \(5\). The slope, the decrease, and the convexity do not use the comparison. The banner `ALL ACTING MEMORY CHECKS PASS` counts the 54 formula checks. The miss is the separate line `PREDICTION-MISS`, which the test requires. That accounting matches the lock.

**What the controls actually remove.** The uncapped price \(\alpha u\theta\) cancels the \(1/\theta\) in the intensity that holds \(r\). The scaled noise, density \(\theta/u\), makes that intensity independent of \(\theta\). In this parameterization the two leave the same function of \(r\), and at the frozen \(\alpha\) that function is the constant \(5.182159696490\). Each control removes the \(1/\theta\) scaling of the price of a fraction. On both arms the minimizing fraction does not move with \(\theta\), so the learning rate at the minimizer does not move either. The learning-rate rise on the fixed-noise arm is the comparative static of the cheaper probe: as \(\theta\) rises, \(r^*\) falls toward the minimizer of \(C\), and \(L=a(1-r)/r\) rises because \(r\) falls. The controls do not isolate that rise from the price scaling.

A rising learning rate can sit next to a rising cost. At fixed \(u=4\) and \(\theta=4\), the fraction is \(0.296535165409\), the learning rate is \(2.372281323269\), and the slope is \(+0.177466031352\). The learning rate is higher than its value \(1\) at \(\theta=1\), and the cost slope has turned positive, because the heat grows like \(\sqrt{\theta}\) while the sign saving is bounded. The note says the second half of that. The sentence in "what stands," that removing the rise of the learning rate removes the drop, makes the correlate into the cause.

**Two routes, with different bookkeeping.**

The measurement route is the identity above. Fixed observation noise, a probe price not proportional to \(\theta\), and a loss that at fixed \(r\) does not grow with \(\theta\). The sign loss is \(w\) times a function of \(r\). The mean-square loss is \(w r\theta\), which grows with \(\theta\), and the admissible squared costs on \(\theta\in\{1/2,1,2,4\}\) are \(5.316961792302\), \(8.000711319618\), \(13.186217779633\), \(23.557230699662\), strictly increasing. Clauses (a) and (b) together are present on that arm, and the cost rises. The cap and the channel are not sufficient for the repository's mean-square loss.

The option route has no channel. \(\mathbb{E}[\max(X,0)]=\sqrt{\theta/(2\pi)}\) for \(X\sim\mathcal N(0,\theta)\). The cost \(1-\sqrt{\theta/(2\pi)}\) has slope \(-1/(2\sqrt{2\pi\theta})\), equal to \(-0.199471140201\) at \(\theta=1\) and \(-0.099735570100\) at \(\theta=4\). The premium does not depend on \(\theta\). The expectation grows with \(\sqrt{\theta}\). A capped premium on a payoff whose expectation grows with the stressor is enough for a level drop, with no measurement. That is the sense in which (b) is not necessary.

"Capped downside plus a payoff that grows with the stressor" is the option. The tracker is a price that shrinks and a loss that stays a function of the fraction. Treating the shrinking price as a growing payoff runs the two routes together. Measurement is one route. Optionality is the other.

The option's cost is convex in \(\theta\). The second derivative of \(-\sqrt{\theta/(2\pi)}\) at \(\theta=1\) is \(0.099735570100\). A higher level of \(\theta\) lowers that cost, and a spread of \(\theta\) raises it. Convexity of \(\max(X,0)\) in the shock \(X\) is a third statement: the expectation grows with the scale of \(X\) because the payoff is convex in \(X\). The note already separates the three. The financial name on the sign bet is a metaphor in the note's own sense. The sign loss lies in \(\{0,w\}\), so the saving against a blind guess cannot exceed \(w/2\). The option's expectation has no finite ceiling.

**Repair.** In §5, state the passive point \((u,\theta)=(4,4)\) with its learning rate \(2.372281323269\) and its positive slope, and say a rising learning rate is present there while the level drop is absent. Say the uncapped price and the scaled noise each remove the \(1/\theta\) scaling of the price of \(r\). State the two routes as a shrinking price of a bounded loss, and as a capped premium on an expectation that grows with \(\theta\). Leave the grid comparison against \(5\) as the puzzle it is. The diagnosis stays.

## What was checked and holds

### The lock

Commit `06976862` (2026-11-22 20:55:49 UTC) adds only `theory/acting_memory_checks/PREREG.md`. Commit `4d74bd52` (20:55:53 UTC) adds only `LOCK.txt`. Commit `733d732` (21:16:00 UTC) evaluates the costs. The blob of `PREREG.md` is `198e5e90653e154df9131242370415945c81a8b8` at all three commits. Its sha256 is `bdf86e0379297c84f59856261419e66286c8c3b3f48ce24e8e22fd7812ddd4b8`, the digest in `LOCK.txt`. The preregistration contains closed forms and signs. It contains no decimal expansion of a cost, no grid minimum, and no tail probability. The script checks the hash before it evaluates a cost. A private computation before the commit is outside what the history can show. The commit order, the unchanged blob, and the absence of decimal results are what the lock can show, and they hold.

`git diff 13eec9af 733d732 -- THEORY.md CORE.md README.md` is empty. The hypothesis sentence at `THEORY.md:41`, `CORE.md:9`, and `README.md:9` is

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

### Recomputation

Independent Decimal arithmetic, with its own Machin formula for \(\pi\), its own arccosine, a 4000-point scan plus Newton, finite differences of the Riccati at fixed intensity, and its own series for \(\mathrm{erfc}\). Nothing was imported from `acting_checks.py`. The note's digits are on the left. The derivatives along \(r^*\) are new splits of the same slope.

| Claim | Independent value |
|---|---|
| Cost at \(r=1/2\), \(\theta=1\) | \(5.182159696490\) |
| Minimizer the scan returns | \(r=1/2\), one sign change of \(\partial J/\partial r\) |
| Slope, envelope and fixed \(u=4\) | \(-0.182159696490\) |
| Fixed-intensity heat slope | \(2/3\) |
| Fixed-intensity sign slope | \(-8/(3\pi)\) |
| Second derivative | \(0.313020858054\) |
| Re-optimized spread, half-width \(1/10\) | \(0.001577268119\) |
| Fixed-fraction spread | \(0.001839996934\) |
| \(J^*\) on \(\{1/8,1/4,1/2,1,2,4,8\}\) | \(5.911577251205\), \(5.584150440609\), \(5.343143969081\), \(5.182159696490\), \(5.083843454099\), \(5.028073368003\), \(4.998066177768\) |
| Fractions \(r^*\) on that grid | \(0.671238475860\), \(0.597650549677\), \(0.540374322719\), \(1/2\), \(0.474155421441\), \(0.458964128271\), \(0.450597167920\) |
| Floor of \(C\) | \(4.966383544211\) at \(r=0.441594095399\) |
| Admissible squared costs | \(5.316961792302\), \(8.000711319618\), \(13.186217779633\), \(23.557230699662\) |
| Squared slopes at \((u,\theta)=(0,1)\), \((4,1)\), \((1/2,2)\) | \(16\), \(6\), \(9.381941874331\) |
| \(\mathrm{erfc}(1)\) | \(0.157299207050\) |
| Passive sign slope at \(\theta=4\), \(u=4\) | \(+0.177466031352\) |
| Naked-option slopes at \(\theta=1\) and \(\theta=4\) | \(-0.199471140201\), \(-0.099735570100\) |
| \(\partial L/\partial u\) at \(u=4\), \(\theta=1\) | \(1/6\) |

The Riccati residual at \((u,p,\theta)=(4,1/2,1)\) is \(0\). The positive root returns \(p=1/2\). The sign probability at \(r=1/2\) is \(1/4\). The uninformative sign cost is minimized at \(u=0\) with value \(8\) and slope \(0\). The uninformative squared slope is \(w=16\). The uncapped price and the scaled noise are each the constant \(5.182159696490\).

`nice -n 19 python3 theory/acting_memory_checks/acting_checks.py` exits 0. The stdout is byte-identical to the committed `results.out`: 54 checks, `FAILS 0`, and one `PREDICTION-MISS`. `nice -n 19 python3 tools/check_consistency.py` prints `RESULT: PASS`. `nice -n 19 python3 tools/check_open_work.py` prints `union missing from OPEN_WORK.md: 0` and `RESULT: PASS`. `nice -n 19 python3 -m pytest -q tools` prints `257 passed, 1 skipped`. The skip is `tools/test_lean.py`, because Lean 4 / lake is not installed. No lake build.

### Ruin

The locked definition is a gross loss that exceeds the reserve \(B=16\). The sign loss is \(0\) or \(16\), so \(P(\mathrm{loss}>16)=0\), which is within \(1/20\). That probability is what the algebra says. The probability of losing the whole reserve is the sign-error probability \(1/4\). Admissibility uses the strict exceedance at \(B=w\).

At the same \((u,p)=(4,1/2)\) the squared loss exceeds \(16\) with probability \(P(|Z|>\sqrt{2})=\mathrm{erfc}(1)=0.157299207050>1/20\). That point is inadmissible, as locked.

The cap \(p\le p_{\mathrm{cap}}\) uses \(P(|Z|>z_\Phi)=1/20\), so \(z_\Phi=\Phi^{-1}(0.975)=1.959963984540\) and
\[
p_{\mathrm{cap}}=\frac{B}{w z_\Phi^2}=0.260317771627.
\]
The script's printed \(z\) is \(\mathrm{erfcinv}(1/20)=1.385903824350=z_\Phi/\sqrt{2}\), and it computes \(B/(w\cdot 2 z^2)\). The two expressions are the same cap. The note's formula is the normal-quantile one. The log's symbol is the complementary-error-function one. A reader who inserts the printed \(z\) into the note's formula doubles the cap.

On \(\theta\in\{1/2,1,2,4\}\) the unconstrained squared minimizer is feasible only at \(\theta=1/2\) (\(p^*=0.225413164108<p_{\mathrm{cap}}\)). At \(\theta=1,2,4\) it lies above the cap and the minimum sits on the cap. The four costs increase.

### Citations

Each DOI was fetched from `https://api.crossref.org/works/<doi>` on 22 November 2026. All eight returned HTTP 200. The titles, years, and author lists match the note and `crossref.out`.

- Taleb and Douady, doi 10.1080/14697688.2013.800219, 2013, "Mathematical definition, mapping, and detection of (anti)fragility," N. N. Taleb and R. Douady. No abstract. The note cites the title and takes the concave-cost reading from `theory/ROBUSTNESS.md` §6. That is the right scope.
- Horowitz and Esposito, doi 10.1103/PhysRevX.4.031015, 2014, "Thermodynamics with Continuous Information Flow." No abstract. Cited as the source of the shape the repository already uses. The note does not re-prove it.
- Friston, FitzGerald, Rigoli, Schwartenbeck, and Pezzulo, doi 10.1162/NECO_a_00912, 2017. The abstract says action selection can be explained by minimizing variational free energy, and it asks whether neuronal responses can be described as a gradient descent on variational free energy. The note's sentence puts "described" on action selection. The rest of the paragraph is in scope: this note minimizes heat, probe price, and the sign loss, and it does not identify the intensity with their gradient.
- Russo and Van Roy, doi 10.1287/opre.2017.1663, 2018. The abstract says each action is sampled to minimize the ratio of squared expected single-period regret to the mutual information between the optimal action and the next observation. The note drops "single-period." The intensity here is a static price. That contrast holds.
- Chaloner and Verdinelli, doi 10.1214/ss/1177009939, 1995. The abstract is a decision-theoretic review of Bayesian experimental design. "One decision problem" is the note's gloss of that framing.
- MacKay, doi 10.1162/neco.1992.4.4.590, 1992. The abstract discusses objective functions that measure the expected informativeness of candidate measurements. The note's sentence matches.
- Lindley, doi 10.1214/aoms/1177728069, 1956, title only, no abstract. Cited for the title.
- Bar-Shalom and Tse, doi 10.1109/TAC.1974.1100635, 1974, title only, no abstract. Cited for the title. The note calls an open-loop intensity a dual effect a metaphor. The Riccati variance does not depend on the path of \(Y\), so the optimal intensity on this channel is open-loop. That label is the right one.

### Wording, the row, and the merge

Searched the note, the preregistration, the checks, and the T45 row for "bill." None. The note has no "kill" and no "verdict." The preregistration uses "verdict" once, to forbid treating a miss as a judgment on the hypothesis sentence, and it calls a miss a puzzle. The note uses the locked label **MISSES**, keeps the numbers, names the clause, and does not rewrite the preregistration. The word for the objective is cost.

T45 is the right row. T43 is on `main` (`40232f6`, the merge of PR #191). T44 is the open boundary draft, PR #194, and it is not on `main`. `git merge-tree --write-tree origin/main origin/acting-memory-2026-11-22` exits 0, and the merged table has T43 and then T45. The same merge with `origin/boundary-sufficiency-2026-11-22` exits 0 and orders T43, T44, T45.

The preregistration's sentence that PR #191 is not merged was true at 20:55:49 UTC. The merge of #191 is 21:03:02 UTC. The note was committed at 21:16:00 UTC and still says "not merged." T45 still calls #191 a draft. The note does not rescore that work. The preregistration stays as locked.

### The world stays exogenous

`theory/ACTING_MEMORY_2026-11-22.md:23`, `:29`, `:68`, `:173`.

AM-X puts no action in the equation for \(X\). The action chooses the observation intensity and pays for it. Because the posterior variance does not depend on the path, the choice is open-loop: a precommitted probe, not a probe that reacts to what was seen, and not an action that moves the drift. That is active sensing. The failure-time argument in §5 is the same boundary. A failure time independent of \(X\) given quality leaves the conditional law of \(X\) unchanged, so the failure adds nothing about \(X\). The note proves that. A Cox intensity that depends on \(X\) would make the failure a measurement. It would still leave the action out of the drift.

The opening can be read as a result about acting under volatility. The object that was scored is a priced observation channel on a world the action does not enter. Section 1 and section 3 already say so. Section 0 and T45 do not.

The note's proposed next lock freezes a Cox intensity, a finite-rate excess, and a grid scored against \(\inf C\). The Cox clock and the excess are two of the three open cases. The probe that changes the drift is the third, and it is the one that would make the action more than sensing. A finite-rate gap that grows with \(\theta\) remains able to reverse the level drop, because every scored cost charges the floor \(kT\,L\).

## Required fixes

1. In §0, in §4, and in T45, write \(\mathrm d J^*/\mathrm d\theta=-A(r^*)/\theta^2\). Label \(2/3\) as the heat slope at fixed intensity \(u=4\). Give the along-path derivatives at \(\theta=1\): probe \(-0.130861161564\), heat \(+0.187741986525\), sign \(-0.239040521451\). Say the level effect is signal-to-noise scaling, a probe price of a given fraction falling as \(1/\theta\). Say the second derivative \(0.313020858054\) and the re-optimized spread \(0.001577268119\) are the variability score, and that a spread raises the cost on the repository's reading of Taleb and Douady. Say that \(5.182159696490\) and the slope \(-0.182159696490\) are the critical point built by the choice of \(\alpha\).

2. In §5, state that at fixed \(u=4\) and \(\theta=4\) the learning rate is \(2.372281323269\) and the slope is \(+0.177466031352\). Say the uncapped price and the scaled noise each remove the \(1/\theta\) scaling of the price of \(r\), and that the learning-rate rise is the comparative static of that scaling. State the two routes separately: a shrinking price of a loss that depends on \(\theta\) only through \(r\), and a capped premium on a payoff whose expectation grows with \(\theta\). Leave the comparison of \(J^*(8)\) with \(5\) as a puzzle. The diagnosis stands: \(C(1/2)=5\) is an upper bound on the floor, \(\inf C=4.966383544211\), and the crossing is near \(\theta=7.5267230646\).

3. In the opening and in T45, put \(P(\mathrm{loss}=16)=1/4\) beside \(P(\mathrm{loss}>16)=0\). Name both thresholds for the squared cap: \(\Phi^{-1}(0.975)=1.959963984540\) in the note's formula, and the log's \(\mathrm{erfcinv}(1/20)=1.385903824350\), with \(p_{\mathrm{cap}}=0.260317771627\) under either expression. \(\mathrm{erfc}(1)=0.157299207050\) stays the squared point's ruin probability.

4. In §1 and in T45, say PR #191 is on `main` at `40232f6` and that this note does not rescore it. Leave the preregistration untouched. In §0, say the scored action is an open-loop intensity and that the world equation contains no action.

5. In §6, attribute to Friston and coauthors the abstract's split: action selection explained by minimizing variational free energy, and neuronal responses asked about as a gradient descent. Restore "single-period" in the Russo and Van Roy ratio.

## Recommended next test

A new preregistration. This file's `PREREG.md` stays locked.

Freeze the class before any cost is evaluated, and score level and variability separately, as this preregistration already does.

1. **A probe that changes the world.** Put the action in the drift, \(dX=-aX\,dt+b u_a\,dt+\sqrt{2a\theta}\,dW\), with a price on \(u_a\). Score three arms: the action only, the observation channel only, and both. The exogenous Riccati of this note is the observation-only control. If the minimized cost falls in \(\theta\) with the observation channel shut, the drop is the action changing the world. If it falls only with the channel open, the drop remains sensing. This is the open case CX2.

2. **A failure rate that depends on the world.** A Cox intensity \(\lambda(X)\), so the failure time carries information about \(X\) and the part is then gone. Score it against a failure time that is independent of \(X\) given quality, at the same mean rate. The quality-only arm is the one this note already shows adds nothing about \(X\).

3. **A heat gap that can grow with \(\theta\).** Charge \(kT\,L+\gamma(\theta)\) with the form of \(\gamma\) frozen in the preregistration and increasing in \(\theta\). Every cost in the present file charges the floor, and the note says a growing gap could reverse the level drop.

Score the sign grid against \(\inf C\), whose value on this class is \(4.966383544211\), and record a spread of \(\theta\) as its own number. A Cox clock alone still leaves the action out of the drift. The drift probe is the arm that answers whether acting is more than sensing.
