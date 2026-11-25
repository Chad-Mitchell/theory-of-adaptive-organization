# Turnover, heat, and a positive level of stress

*Sunday 22 November 2026. In-model. A self-check, not an independent review. Rebased onto `main` `13eec9a`. The preregistration is commit `4041018f8ec127b5b686f202858d7944d57b962d`. The addendum is commit `271842a26ad391419b2b2d219160bb8d581d7ecc`. Both are parents of the computation. `PREREG.md` and `ADDENDUM.md` are not edited. `THEORY.md`, `CORE.md`, and `README.md` are not edited. The hypothesis sentence is unchanged. Revised after the hostile review of draft PR #191: the admissible comparison leads, and the row is T43.*

Checks: `theory/antifragility_checks/turnover_checks.py`, run at `nice -n 19`. Machinery FAILS 0. The numbers below are the numbers it prints. DOIs are in `crossref.out`.

Labels: **PROVED** (this class, algebra, code-checked), **KNOWN** (a fetched source, for what that source states), **FAILS** (a numbered prediction the arm refutes), **CONJECTURE** (named, not derived here), **METAPHOR** (a name with no computed consequence in this class).

## 0. The answer

Under the ruin cap, identical units at rate \(1\) cost \(15.473978\) with ruin probability \(0.020940\), against the inadmissible zero at cost \(16\), a margin of \(0.526022\). The unconstrained minimum of the cost that P1–P7 score is at rate \(0.2646371727\), cost \(13.3545082433\). The official grid point of that bowl, rate \(0.3\), cost \(13.7488993918\), has ruin probability \(0.473560\). The informative admissible point costs \(15.566427\) and the uninformative admissible point costs \(22.311716\), both above their zero-shock cost \(13\). The quality-observed admissible point costs \(15.471038\) against its own zero at \(13\). Those numbered predictions were scored on the unconstrained cost, which the preregistration required.

The heat inside the cost does not fall. Continuous heat is \(8\), constant in the shock. The stock paid at each rebuild rises with the shock. What falls, inside the unconstrained bowl, is the loss, because replacement re-aligns units that had gone stale. That bowl is convex. A spread of the shock around the mean-field minimum raises the cost by \(0.2232577182\). A positive level of stress and a Jensen gain are different statements. The admissible point above is a positive level. The spread is the second statement, and it raises the cost.

The heterogeneous arm, at the frozen cap, is an open miss. Quality varies, weaker units fail faster, and replacement copies survivors. The minimum on the grid is at no shock, cost \(13\). Selection keeps the more precise units, and heat is proportional to precision, so the cost jumps as soon as the shock is turned on. A local bowl on the selected branch, at rate \(0.25\), cost \(13.1627010412\), stays above \(13\). P1 stays **FAILS** at this cap. The diagnosis is that coupling, not a claim about every cap.

A quality-blind schedule at a chosen rate matches the identical-unit shock and beats the informative shock on the unconstrained cost. Where that unconstrained gain exists, it is a maintenance rate. The shock is a substitute for a schedule the designer was not allowed to run.

## 1. The locked class, in one paragraph

Four units, precision cap \(1/2\), prior variance \(4\), stake \(3/2\), upkeep \(1/2\), build cash \(1/2\), drift rate \(1\), \(kT = a = 1\). Heat of a living unit is \(kT\, a\, v\, c\, q\), paid whether or not alignment has decayed. A failure pays \(b + \tfrac12\log(1+v c q_{\mathrm{new}})\). At the frozen point that stock makes \(B = 1.0493061443\) for a unit of quality \(1\). Alignment of a unit with failure rate \(\lambda\) is \(\lambda/(\lambda+1)\) in expectation. The pool adds precisions. The blind reference, no units, is \(w v = 6\). It is not a point on the stress grid. Design D1 is the same table with one unit.

## 2. Identical units

**Lemma (PROVED).** For one quality \(q = 1\),
\[
J'(0) = n\left(B - \frac{w v^{2} c q}{\delta}\right) = -43.802775422664.
\]
The threshold is \(12\). Since \(0 < B < 12\), there is one critical point,
\[
u^\star = 0.2092593658, \qquad \sigma^\star = 0.2646371727,
\]
and it is a minimum: \(J(\sigma^\star) = 13.3545082433 < J(0) = 16\). The exact finite difference of the loss piece at step \(10^{-12}\) matches \(-48\), which is the loss half of \(J'(0)\). A float difference at step \(10^{-8}\) sits at relative error \(9.668\times 10^{-8}\), which is roundoff on a gap of size \(4\times 10^{-7}\), and is not the scored difference.

**P2 on this arm. FAILS.** The control said the cost is monotone in the shock when units are alike. The derivative is negative. Monotonicity is refuted by the algebra, and the expected-loss check agrees: official \(J\) on the grid is minimized at rate \(0.3\), cost \(13.7488993918\), with both brackets and the gap against zero above twice the paired standard error (left gap \(1.036764\), standard error \(0.004073\); right gap \(0.436720\), standard error \(0.002363\); gap against zero \(2.251101\), standard error \(0.004817\)).

**P5. The minimum is not an artifact of a free shock.** With \(B = 0\) the mean-field cost falls on the whole grid, from \(16\) at rate \(0\) to \(10.6961325967\) at rate \(20\). The minimum is the right endpoint. The interior minimum of the lemma uses \(B = 1.0493061443 > 0\).

**P6, identical units.** Reading the shock rate as a chosen turnover rate gives the same formula. The schedule at \(\sigma^\star\) costs \(13.3545082433\), equal to the shock. The gain is the rate. An exponential clock that the designer did not choose is a substitute for a schedule at that rate. It does not beat the schedule.

**One unit, the replication.** The same lemma with \(n = 1\) has \(\sigma^\star = 0.7939115180\), cost \(6.5158811825\), against \(8.5\) at no shock. The qualitative result does not depend on using four units. Both minima are above the blind reference \(6\). The turnover tradeoff is inside a design that, at this cap, costs more than tracking nothing. That comparison was not a score. It is the reason §6 asks for a joint choice of the cap and the rate.

**Downtime, not a score.** A mean repair delay of \(1/4\) leaves a minimum on the grid, at rate \(0.5\), cost \(12.5345418146\), against \(16\) at no shock.

## 3. Heterogeneous units

Stationary count of high-quality units, informative failure, copy-with-mutation: \(\mathbb{E}[k] = 3.7899088603\), against \(n\pi = 2\) for the prior and for uninformative replacement. The ordering was predicted and holds. Continuous heat on that selected law is \(7.6848632904\). Continuous heat on the prior is \(5\). At matched mean failure rate the informative arm pays the higher heat, as predicted, because heat is proportional to quality.

**P1. FAILS** under the locked definition. Official \(J\) and the mean-field cost on the grid are both minimized at rate \(0\), cost \(13\). Turning the shock on jumps the cost to \(15.6848198582\) at rate \(10^{-6}\), because the type law jumps to the selected one and the alignment has not yet moved, so the loss is still \(4\) while the heat has risen from \(5\) to \(7.6848632904\). On the selected branch the fine grid has a lowest point at rate \(0.25\), cost \(13.1627010412\), which is above \(13\). A local bowl that does not beat no shock is not an interior minimum of the grid. P1 stays **FAILS** at this frozen cap. The miss is open. The diagnosis is the coupling written before the search: installed precision is \(c q\), and the heat is that precision, so keeping the stronger units raises the heat before alignment has moved.

**P2 on uninformative failure. FAILS.** Uninformative replacement with drift is not monotone. The mean-field cost is minimized at rate \(0.3\), cost \(10.8369375047\), and the brackets hold (left \(11.7110816668\), right \(11.1894029598\)). Official \(J\) is minimized at rate \(0.4\), cost \(11.262060\). The same curve is the quality-blind schedule: replacement that keeps each unit's quality and only resets its age. The two policies are the same object when failure does not depend on quality and the type law is the prior.

**P3. No interior minimum without drift.** With alignment fixed at \(1\), official \(J\) is minimized at rate \(0\), cost \(8.075425\), and the next grid point is higher by \(2.538938\). The mean-field gap is \(2.6040867611\). There is no purge. Selection raises heat by more than it cuts the loss, so the selected law is the more expensive one even though every unit is already aligned. The scale lemma holds: on \((0,\infty)\) the loss does not depend on the rate and the build rate is proportional to it.

**P4.** Uninformative replacement and no drift: official \(J\) is strictly increasing on the grid. The smallest step is \(0.1752039\).

**P6, the three policies.** Official best costs on the grid: informative shock \(13\), quality-observed schedule \(13\), quality-blind schedule \(11.2576037038\). The inequality "observed quality is no worse than the informative shock" holds because both are best at rate \(0\). The content is the third number. The blind schedule, which does not select, is cheaper by \(1.7423962962\). Informative failure is not doing work the schedule cannot do. It is doing work the schedule refuses, and the cost rises.

At shock rate \(1\), matched to the same mean failure rate, the mean-field gap (informative minus uninformative) is positive across the grid, and the official gap is \(2.702254\) with standard error \(0.003213\). The sign was not predicted. The result is that rewarding the stronger units raises the cost at this cap.

## 4. The ruin cap

Under the cap \(P(\varepsilon > 1.5) \le 0.05\), identical units at rate \(1\) cost \(15.473978\) with ruin probability \(0.020940\), against the inadmissible zero at cost \(16\). The informative admissible point costs \(15.566427\) and the A4 uninformative admissible point costs \(22.311716\), both above their zero-shock cost \(13\). The quality-observed admissible point costs \(15.471038\) against its own zero at \(13\). The unconstrained minimum that P1–P7 score has ruin probability \(0.473560\) at the official grid point, rate \(0.3\). The cap is a constraint, not a term in \(J\). A minimum that exists only because rate \(0\) is inadmissible is not an interior minimum of the cost. Rate \(0\) with drift has error \(4\), so every such arm has ruin probability \(1\). The numbered predictions were scored on the unconstrained cost, which the preregistration required.

| arm | unconstrained grid min | ruin probability there | admissible grid min |
|---|---|---|---|
| identical units, official | rate \(0.3\), cost \(13.748899\) | \(0.473560\) | rate \(1\), cost \(15.473978\), probability \(0.020940\) |
| informative, official | rate \(0\), cost \(13\) | \(1\) | rate \(1\), cost \(15.566427\), probability \(0.027440\) |
| A4 uninformative | rate \(0.4\), cost \(11.262060\) | \(0.638600\) | rate \(4\), cost \(22.311716\), probability \(0.040260\) |
| quality observed | rate \(0\), cost \(13\) | \(1\) | rate \(1\), cost \(15.471038\), probability \(0.019980\) |

A4 and the quality-blind schedule A8 share a mean-field curve. A8's own admissible point costs \(22.311377\) with probability \(0.041580\). Both admissible costs exceed \(13\). Meeting the cap on that arm takes enough turnover that the build rate overshoots the loss it saves. The cap and the unconstrained bowl are different designs.

## 5. Heat, convexity, and the names

Three rates were locked so they would not be substituted for each other.

**Heat inside \(J\). PROVED, and it does not fall.** For identical units the continuous heat is \(8\) at every shock. The sum of that heat and the stock rate runs from \(8.1098612289\) at rate \(0.05\) to \(51.9444915467\) at rate \(20\). On the informative arm the continuous heat is constant on \((0,\infty)\), at \(7.6848632904\), and the same sum is strictly increasing. Shock-driven turnover does not lower the long-run heat in the locked accounting. It raises the stock. The term that falls in the identical-unit minimum is the loss.

**Realized learning flow. PROVED, and it rises.** \(Q_{\mathrm{flow}} = kT\, a\, v\, \mathbb{E}\Phi\) is the floor of the effective channel. For identical units it runs from \(0.3809523810\) at rate \(0.05\) to \(7.6190476190\) at rate \(20\). Re-alignment increases the learning rate about the signal. The sentence "re-aligned units need less learning flow" is false of this rate.

**Matched-error installed heat. PROVED, and it falls.** The installed heat that holds the fully aligned error, divided by mean alignment, runs from \(168\) at rate \(0.05\) to \(8.4\) at rate \(20\). The same sentence is true of this rate. It is not the heat inside \(J\). \(J\) installs the cap and lets the error move.

**Re-optimized precision, arm A14, not a rescore of P1. PROVED as a shape.** Uncapped heat is zero for alignment at or below \(kT a/(w v) = 1/6\), rises until alignment \(4 kT a/(w v) = 2/3\), and falls after that. The cap \(1/2\) never binds on the grid \(r = i/200\): the largest installed precision on that grid is \(0.093750\), and the heat at the grid point next to \(2/3\) is \(1.499998\). The frozen cap \(1/2\) is above the precision this stake would install at every alignment on the grid. That is why a policy which keeps high-\(q\) units raises the heat by more than it cuts the loss.

**Where the cost is convex. PROVED.** For the identical-unit mean-field cost the second derivative equals the addendum display, and both equal
\[
J''(\sigma) = \frac{864}{(9\sigma+1)^3}
\]
at these numbers. It is positive on the locked log grid, smallest value \(0.0001457062\). There is no subinterval of concavity. An exact second difference of step \(10^{-6}\) matches it, maximum relative error \(8.100\times 10^{-11}\). The informative mean-field cost on \((0,\infty)\), grid step \(1/20\), has nonnegative second differences down to the tolerance \(10^{-9}\). Convexity is not claimed across rate \(0\) on that arm: the type law jumps.

Jensen follows the second derivative, not the existence of a minimum.

| object | spread | \(\mathbb{E}[\cdot] - (\cdot)(\mathbb{E})\) |
|---|---|---|
| identical-unit \(J\) | \(\{1,2\}\) | \(+0.0392014519\) |
| identical-unit \(J\) | \(\{0,2\}\) | \(+2.2736842105\) |
| identical-unit \(Q_{\mathrm{flow}}\) | \(\{1,2\}\) | \(-0.1333333333\) |
| identical-unit \(Q_{\mathrm{flow}}\) | \(\{0,2\}\) | \(-1.3333333333\) |
| identical-unit \(Q_{\mathrm{match}}\) | \(\{1,2\}\) | \(+0.6666666667\) |
| informative \(J\), on \((0,\infty)\) | \(\{1,2\}\) | \(+0.0393731901\) |
| informative \(Q_{\mathrm{flow}}\) | \(\{1,2\}\) | \(-0.1276642073\) |
| informative \(J\), across the jump | \(\{0,2\}\) | \(+0.9146086423\) (reported, not a predicted sign) |

A spread raises \(J\) everywhere this table scores it. A spread lowers \(Q_{\mathrm{flow}}\), because \(\sigma/(\sigma+1)\) is concave, so the average alignment falls. That is less learning, not a cheaper way to hold the error. **P7** at the identical-unit minimum: the spread \(\{\sigma^\star/2,\ 3\sigma^\star/2\}\) raises the cost by \(0.2232577182\).

The repository's reading, already in `theory/ROBUSTNESS.md` §6, is that a cost concave in the stressor gains from variation. The cost here is convex in the shock on the whole half-line. The interior minimum is a statement about the level. It is not antifragility in that sense. Calling the convex bowl a Jensen gain would reverse the inequality.

**Names.**

Taleb and Douady, title fetched, DOI `10.1080/14697688.2013.800219`. **KNOWN** as the paper whose title names a mathematical definition of antifragility. No abstract was in the Crossref record. The concave-cost reading used above is the one already in `theory/ROBUSTNESS.md` §6.

Calabrese and Baldwin, DOI `10.1146/annurev.pharmtox.43.100901.140223`. **KNOWN**: hormesis, as they state it, is low-dose stimulation and high-dose inhibition. The identical-unit cost falls and then rises. That shape is what their sentence describes. Calling this cost hormesis adds no comparison the curve does not already make. **METAPHOR** for the name, inside this class.

Paolicelli and coauthors, DOI `10.1126/science.1202529`. **KNOWN**: microglia engulf synaptic material during postnatal pruning in mice. Kerr, Wyllie, and Currie, DOI `10.1038/bjc.1972.33`. **KNOWN**: apoptosis, as they propose it, is controlled deletion, a complementary but opposite role to mitosis. The quality-observed schedule is deliberate deletion of the weak units. At this cap it does not lower the cost. The biological names are **METAPHOR** here.

Perunov, Marsland, and England, DOI `10.1103/PhysRevX.6.021036`. **KNOWN** for the fetched abstract: a finite-time free energy for driven matter, and an argument that driven systems tend toward states which reliably absorb and dissipate work. The hazard in this class is an assumption. It is not that free energy. The statement that their driving is why \(J\) has the shape it has is **METAPHOR**. The statement that some generator in that literature induces both this hazard and this heat floor is **CONJECTURE**, and this check does not test it. The computed consequence of "reward the stronger units" at the frozen cap is a higher cost, by \(2.702254\) at rate \(1\).

## 6. What this does not settle

P1 stays **FAILS** at the frozen cap. That miss is open. The diagnosis is the locked coupling: a weak unit is weak because its installed precision is small, and that precision is what the heat charges, so selection keeps units past the heat this stake pays for. The cap was taken from the holographic note (\(c = 1/2\), below the one-unit copy threshold \(5/3\)) and was not re-optimized in the scored arms. Arm A14, which ignores the cap, installs at most \(0.093750\). Four fully aligned units at that precision pool to \(0.375\), short of \(5/12\).

Under the cap, the blank design has error \(4\) and ruin probability \(1\). The unconstrained comparison of the identical-unit minimum with the blind cost \(6\) is a comparison of two designs the cap rejects. The turnover result is conditional on the cap being installed.

No parameter was moved after the preregistration. The informative arm was not rescued.

## 7. Checks

`turnover_checks.py`. Machinery FAILS 0, including the stationary balance, the Gauss–Legendre noise unit (quadrature \(2.1972245773\), Monte Carlo \(2.1938321155\), standard error \(0.0031763983\)), the derivative, and the second-derivative identity. Run at `nice -n 19`.
