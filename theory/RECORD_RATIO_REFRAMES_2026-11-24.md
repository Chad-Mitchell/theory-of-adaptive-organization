# Record-price ratio: three reframes, none forces 1

*24 November 2026 (UTC). Preregistered and hash-locked before the grid (`theory/record_ratio_reframes_checks/PREREG.md`, sha256 `8e495b7b…fce8`, commit of that lock only). Self-check, not an independent review. `THEORY.md` is unchanged (blob `6caadae569116a94a74563398be94cebf6e99e9b`). Open-work row T76. Status words are those at `CORE.md:169`. Nothing here derives general relativity, quantum mechanics, or holography. The qubit, the dephasing channel, and the two record functionals are inputs from draft #252.*

*T75 asked whether a consistency principle forces \(\kappa_D/\kappa\) in \(J=\kappa\,I(W;M)+\kappa_D\,P_D+w\,L\). None of the four readings did. Routes A and B pointed at the endpoint \(0\) under strengthenings that are not axioms. This note asks a different question: whether a known result in a distant field, or a reframe of what is being asked, forces the ratio or shows that it stays free.*

## Answer

No. Three routes. None of them forces \(\kappa_D/\kappa=1\).

- **Route K** (Kelly doubling rate). **KNOWN** for the theorem, **NUMERICAL** for the split. The doubling rate of a fair-odds bet on \(W\) given the outcome \(M\) is \(I(W;M)\), weight \((1,0)\) on \((I,P_D)\). The Holevo bound equals \(I+P_D\) on the antipodal ensemble and does not equal it on the biased ensemble. On the biased ensemble a different pair, \((1.0033319156709788,\ 0.6581687266183737)\), tracks the bound with max residual \(0.0004213774925606595\), inside the locked bar \(0.005\). That pair is not ratio \(1\). The cost ratio stays free.
- **Route G** (gauge). **NUMERICAL**, and the corner case is the antipodal identity already in T75. On the complete-dephasing antipodal ensemble with a stake that prefers the pointer, every ratio in \([1,\infty)\) selects \(\theta=0\) and the same minimized cost. The gauge stops when the stake is zero and the ratio is exactly \(1\) (the argmin is the whole interval), when the ratio is below \(1\), and at partial dephasing with a non-commuting stake (ratio \(1\) and ratio \(100\) differ by \(0.465\) rad). Adding the same constant to both coefficients does not change the selected angle on the antipodal ensemble. It changes the angle once the ledger \(H(M)-\mathbb{E}[S(\rho)]\) depends on \(\theta\).
- **Route C** (calibration). **Puzzle.** The locked stake lists produced no interior pair, so they did not measure the ratio. A post-hoc scan, not a rescore, finds a thin band of stakes where the antipodal list would have recovered only the difference \(\kappa_D-\kappa\), and the biased list would have recovered both coefficients. The locked lists missed that band. The suggested next stakes in the preregistration sit on the corner and would miss it again.

Renormalization under the chain rule, and the rate-distortion slope, were dropped before the lock. Both rename a route already scored (`PREREG.md:21-23`).

## Route K. Doubling rate

**Claim.** Kelly's growth-rate equality, and Sharma's measurement extension of it, assign the doubling rate to \(I(W;M)\). They do not assign a second, fixed, nonzero weight to \(P_D\). The Holevo quantity is an upper bound on that rate, not the rate. On these ensembles the bound coincides with the shared-coefficient sum \(I+P_D\) only on the antipodal knife-edge.

**KNOWN.** Kelly, doi `10.1002/j.1538-7305.1956.tb03809.x`, publisher abstract: at odds consistent with the probabilities, the maximum exponential growth of capital equals the transmission rate, and the result extends to arbitrary odds. The page proof was not re-read (`PREREG.md:39`). Sharma, arXiv `1306.3791v2`, section VI.5, equations (53) and (55), read: at fair odds \(o_i=1/p_i\) and posterior bets, the doubling rate equals the mutual information of the input and the measurement, and the Holevo quantity is an upper bound. His (47)–(48) set a different gap, between two helper protocols, equal to quantum discord under uniform fair odds and eigenbasis measurements. That gap is not \(P_D\) (`PREREG.md:41`). Adopting either equality is not a sentence of A1–A8.

**Observed against the lock** (`record_ratio_reframes_checks.out:4-11`, criteria `PREREG.md:74-80`).

- Antipodal, \(\gamma=0\): \(\max|I+P_D-\chi|<10^{-16}\). The fit of \(\alpha I+\beta P_D\) to the rate \(I\) is \((1,0)\). The fit to the constant \(\chi\) is \((1,1)\). Both residuals are below \(10^{-16}\). **Matches K1.**
- Biased weights \(0.8/0.2\) on \(\pm z\), \(\gamma=0\): \(\max|I+P_D-\chi|=0.066278\), above the bar \(0.02\). The Gram determinant is \(3.835855\times 10^{1}\), so \(I\) and \(P_D\) are not collinear, and the fit to the rate \(I\) is still \((1,0)\). **Matches** those three K2 clauses.
- The same biased curve: the least-squares fit of \(\alpha I+\beta P_D\) to \(\chi\) is \((1.0033319156709788,\ 0.6581687266183737)\), max residual \(0.0004213774925606595\), and the locked net's minimum is that same residual. The bar was \(f>0.005\). **Misses K2's bound clause.**

**What it forces.** The benefit side, in the fair-odds horse race Sharma writes, prices \(I\) and does not price \(P_D\). That is weight \(0\) on the disturbance, which is the endpoint T75 already separated from the shared-coefficient sentence. It is a price of the bet, not a coefficient in \(J\). Putting it into \(J\) would be a further sentence.

The shared-coefficient reading is the pair \((1,1)\). It reproduces the Holevo bound on the antipodal ensemble, where \(H(M)=S(\bar\rho)=\ln 2\) at every \(\theta\), and it misses that bound by \(0.066\) nat on the biased ensemble. The pair that does track the bound there is not equal weights. The residual is small because both functionals are smooth functions of one angle. It is not an identity: the printed residual \(0.0004213774925606595\) is far above the gate noise. The preregistration said that if the least-squares residual itself fell to \(0.005\) or below, the route would stop and report the pair, and would not declare ratio \(1\) (`PREREG.md:80`). That is this outcome.

**What blocks a cost ratio.** Sharma's rate is \(I(W;M)\) after the measurement has been chosen. \(P_D\) does not enter (53). The Holevo bound does not choose \(\kappa_D/\kappa\). Discord, in the helper comparison he actually proves, is a third functional. None of the three is the marginal rate inside \(J\) (`theory/REPRESENTATION.md:120`).

**Model implication.** Conditional on adopting Sharma's fair-odds doubling rate as the value of the classical outcome: the exchange rate of the record, in doubling-rate units, is one nat of growth per nat of \(I(W;M)\) and zero per nat of \(P_D\). Conditional on adopting the Holevo bound as that value instead: the bound equals \(\kappa(I+P_D)\) with one \(\kappa\) only on the antipodal complete-dephasing ensemble, and on the biased ensemble the near-fit has unequal weights. Neither conditional is a derivation of the coefficient in the cost. **KNOWN** for the adopted equality. **NUMERICAL** for the split.

## Route G. Gauge

**Claim.** On the complete-dephasing antipodal ensemble, with \(\phi=0\) so the loss prefers \(\theta=0\), every ratio \(\kappa_D/\kappa\ge 1\) at \(\kappa>0\) selects the same design and the same minimized cost. The ratio is then a gauge of selected designs and of scored costs. It stops being a gauge in three places: at ratio exactly \(1\) when the loss is flat (the argmin set jumps from a point to the whole interval), for every ratio below \(1\) (the angle moves), and at partial dephasing with a non-commuting stake (ratios above \(1\) separate). A uniform shift \((\kappa,\kappa_D)\mapsto(\kappa+a,\kappa_D+a)\) is invisible to the argmin exactly while \(I+P_D\) is independent of \(\theta\).

**Observed against the lock** (`record_ratio_reframes_checks.out:12-16`, criteria `PREREG.md:82-102`).

- **G1 matches.** Nine cells, ratios \(\{1,2,10\}\), stakes \(\{0.1,1,10\}\), \(\kappa=1\). Each minimizer is the unique grid point \(\theta=0\). The minimized costs at a fixed stake agree across the three ratios to \(10^{-16}\).
- **G2 matches.** At \(w=0\) and ratio \(1\) the cost range on \(721\) points is below \(10^{-16}\) (every angle is minimal). At ratio \(2\) the unique minimizer is \(\theta=0\) and the endpoint gap is \(0.096372\), which is \(P_\chi(0)\).
- **G3 matches.** Ratio \(0\), \(w=1\): \(\theta^\star=\pi/2\). At \(w=10\): unique \(\theta=0\). This is the published side of \(w_\star=3.209014724815\). It is a check of that closed form, not a new forecast (`PREREG.md:27`, `PREREG.md:92-94`).
- **G4 matches.** Antipodal, \(\gamma=1/2\), \(\phi=\pi/4\), \(\kappa=1\), \(w=1\). Ratio \(1\) selects \(\theta=0.464694\). Ratio \(100\) selects \(\theta=0\). The gap is \(0.464694\ge 0.2\). Both minimizers are unique.
- **G5, minimizers match, cost sentence misses.** Vectors \((1,0.5)\) and \((1.5,1.0)\) share the difference \(\kappa_D-\kappa=-0.5\). At every locked stake their minimizers agree. Their minimized costs differ by \(0.048186189255\), which is half of \(P_\chi(0)=0.096372378511\), to \(10^{-16}\) (`record_ratio_reframes_checks.out:1`). The locked symbol was the full \(P_\chi(0)\). The miss is \(4.819\times 10^{-2}\). **Puzzle in the lock,** logged in `DEVIATIONS.md` D2. The sentence was not edited. The shift of the design is the part that bears on the gauge, and that part holds.

**What it forces.** On this antipodal menu, with the loss minimized at the pointer and \(w>0\), a designer who only shows the selected angle and the minimized cost does not reveal \(\kappa_D\) once \(\kappa_D\ge\kappa\). Fixing the ratio by convention, on that class, is not fixed by the designs. The convention that matches T75 Route A (keep the classical channel, allow pointer-plus-garbling) is the endpoint \(0\). The shared-coefficient sentence is the endpoint of the flat ray, ratio \(1\). G2 says those two conventions are not the same design when \(w=0\): ratio \(1\) is indifferent, and any ratio above \(1\) selects the pointer. G1 says that for \(w>0\) they select the same angle, because the loss already selects it.

**Where the gauge stops.** G4 is the sharp stop inside the same four-point ensemble. At partial dephasing the ledger \(I+P_D\) is still independent of \(\theta\) (the outcome stays fair, gate G0b), so ratio \(1\) is exactly "the stake alone." Ratio \(100\) still prices \(P_D\). They do not select the same angle. A convention that set the ratio to \(1\) because the complete-dephasing menu could not see it would be the wrong convention for this task. C3, below, is the stop for the shift symmetry: on the biased ensemble at \(w=0\), ratio \(0\) selects \(\theta=\pi/2\) and ratio \(1\) selects \(\theta=0\).

**What blocks calling the whole ratio a gauge.** Below \(1\), and off complete dephasing, the selected \(\theta\) moves. `theory/REPRESENTATION.md:177` still does not set the number. A gauge on one class is not an identification on the next class.

**Model implication.** Conditional on complete dephasing, the antipodal ensemble, \(\phi=0\), and \(w>0\): ratios in \([1,\infty)\) are indistinguishable from the selected design and from the minimized cost, and the revealed object is at most the inequality \(\kappa_D\ge\kappa\). Conditional on partial dephasing at \(\gamma=1/2\), \(\phi=\pi/4\), \(w=1\): ratio \(1\) and ratio \(100\) are distinguishable, gap \(0.465\) rad. **NUMERICAL** on the locked grid. The corner algebra is the T75 identity, checked rather than re-derived.

## Route C. Calibration

**Claim.** The ratio is a measured number when the menu makes \(I'(\theta)\) and \(P_D'(\theta)\) point different ways and the stake is varied through two interior angles. On the antipodal ensemble those derivatives stay parallel (\(I'=-P_D'\)), so every load recovers at most \(\delta=\kappa_D-\kappa\). Seeing the angle is the extension. The stake is the load.

**Observed against the lock** (`record_ratio_reframes_checks.out:17-19`, criteria `PREREG.md:104-118`).

- **C1 misses.** Plant \((1,0.5)\) on the antipodal ensemble, stakes \(\{0.5,1,2,4,8\}\). No stake has \(\theta^\star\) inside \([0.05,\pi/2-0.05]\). The determinant clause and the recovery of \(\delta\) were not reached.
- **C2 misses.** The same plant on the biased ensemble, stakes \(\{0.05,0.1,0.2,0.5,1,2,5\}\). One interior stake, \(w=0.5\), \(\theta=0.573777\). The corners are \(\pi/2\) at the three smaller stakes and \(0\) at the three larger. One angle does not determine two coefficients.
- **C3 matches.** Biased, \(w=0\), \(\kappa=1\). Ratio \(0\) selects \(\theta=\pi/2\). Ratio \(1\) selects \(\theta=0\). Both unique.

**Post-hoc, not a rescore** (`DEVIATIONS.md` D1, `posthoc_windows.out`). The locked lists straddle a thin band.

- The stakes \(\{0.2,0.3\}\) named as the next C1 step sit at \(\theta=\pi/2\) (`posthoc_windows.out:3-4`). They do not open the band.
- On the antipodal plant the moving angles run from \(w=1.40\) (\(\theta=1.311\)) to \(w=1.60\) (\(\theta=0.127\)). Inside that band the \(2\times 2\) determinant on the end interior points is \(0\), and \(\delta_{\mathrm{hat}}\) is \(-0.499989\), \(-0.500031\), and \(-0.499999\) (`posthoc_windows.out:27-30`). That is the C1 claim, on stakes the lock did not include. It is not a pass of C1.
- On the biased plant the unique interior angles run from \(w=0.480\) to \(w=0.510\). The locked inversion on the two ends returns \(\kappa=1.000444\), \(\kappa_D=0.500290\) (`posthoc_windows.out:49`). That is inside the C2 tolerance, on stakes the lock did not include. It is not a pass of C2.

**What it forces.** Nothing about the value of the ratio. The locked experiment did not pin it. The post-hoc says the experiment can pin \(\delta\) on the antipodal menu and both coefficients on the biased menu, if the loads are placed in a band whose width is a few hundredths to two tenths in \(w\), just below \(|\kappa-\kappa_D|\) times the published \(w_\star\). A factor-of-two stake grid steps over that band. The ratio is measurable inside the model. This run did not measure it.

**What blocks reading C3 as a measurement of the number.** Opposite corners show that ratio \(0\) and ratio \(1\) are different designs at zero stake. They do not return the value of an interior ratio. The first-order system needs two interior angles, and the locked list had one.

**Model implication.** Conditional on the antipodal complete-dephasing menu: designs determine \(\kappa_D-\kappa\) when the optimum is interior, and do not determine \(\kappa_D/\kappa\), because \((\kappa,\kappa_D)\) and \((\kappa+a,\kappa_D+a)\) differ by \(a\) times a \(\theta\)-independent ledger. Conditional on the biased menu, once two interior stakes are in hand: both coefficients are returned by the same linear system. The second conditional is **post-hoc**. The locked run's conditional is the weaker one: these stake lists do not pin the ratio. **Puzzle**, with the band located.

## Why the other two candidates were dropped

Composition. The chain rule writes \(I(W;M_1,M_2)=I(W;M_1)+I(W;M_2\mid M_1)\), and the entropy increase from the initial state to the final state telescopes. Pricing each increment at the same \((\kappa,\kappa_D)\) reproduces one ratio. Every ratio is a fixed point. The map that sends every ratio to an effective \(0\) is pointer measurement plus garbling, which is T75 Route A. A beta function with one jump to \(0\) is that route renamed. It was not scored (`PREREG.md:21-23`).

Rate-distortion. The slope of a rate-distortion function is a Lagrange multiplier at an operating point. On the antipodal ledger \(dI=-dP_D\), so the technical rate of transformation is \(1\), which is Route G's perfect-substitute line. It does not set the price ratio. It was not scored.

## Puzzle

K2's bound clause is the one that came out the other way. A fixed pair that is not \((1,1)\) tracks the Holevo quantity on the biased curve to better than the locked bar. The doubling rate itself stayed at \((1,0)\). The next check, as a new preregistration, is whether that pair survives a second ensemble whose ledger is not a function of a single cosine. This note does not run that ensemble.

G5's cost sentence cannot be true as both of its descriptions at once. The designs are invariant under the shift. The cost moves by half the ledger, which is what the parenthesis describes and not what the symbol says.

C1 and C2 did not reach the inversion. The post-hoc band is narrow enough that the preregistration's own next stakes miss it. A new preregistration that wants to score the inversion has to lock stakes inside the band, or lock a rule that searches for the band without using these post-hoc angles as the prediction.

The shared-coefficient sentence is still missing. Ratio \(1\) is a gauge convention on one class, a distinct design on the next class, and not the weight in the doubling rate.

## Prior art

Checked on 24 November 2026:

- Kelly, doi `10.1002/j.1538-7305.1956.tb03809.x`. Crossref returned the title, the author, *Bell System Technical Journal*, volume 35, pages 917–926, year 1956. The equality used above is the publisher abstract. The article's interior was not re-read.
- Sharma, arXiv `1306.3791v2`. Read. A Crossref query on the title did not return a journal record. No DOI is printed for it.

No claim is made that every gambling or identification theorem has been surveyed. The claim is the one in the answer: these three routes do not force the ratio.
