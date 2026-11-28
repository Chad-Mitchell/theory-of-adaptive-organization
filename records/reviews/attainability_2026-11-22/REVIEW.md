# Review of draft PR #178

**Verdict: SOUND-WITH-FIXES.**

Independent review of draft PR #178, head `0c9422b530d7b1263a4b34472ad360f43ac478e2` on `attainability-2026-11-22`, one commit on `origin/main` `12febaf3d0fe5feb455c08d20342e845e1014117`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake build`. Computations at nice 19.

The learning-rate bound is a bound on the learning rate. The shrunk spring attains the printed heat. The frontier arithmetic holds. The constant \(kT\,a\) on the centered spring is the gap between the Kalman rate of the conditional error and the Kalman rate of the raw coordinate error. `theory/INFO_PHYSICS.md` still states the attainment as open, and the \(K\)-bin column is a learning rate labeled as a heat. Those are the fixes.

The hypothesis sentence is unchanged. One copy, in `THEORY.md:41`, byte-identical on this head and on `origin/main`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`CORE.md` is not in the diff. The master equation in THEORY is not replaced. The diff in `THEORY.md` is the claim-map version in the header.

Recomputation is `reviews/attainability_2026-11-22/recompute.py`. It imports nothing from `theory/info_physics_checks/`. The Lyapunov covariance, the Sekimoto expectation, the learning rate, and the path mutual-information rate are derived in that file. SymPy checks the algebra. The author's script, run separately on this head, reports 28 checks and FAILS 0.

## What holds

**The learning rate, and which object it is.** For the equilibrium signal \(dX=-aX\,dt+\sqrt{2av}\,dW\), the probability current satisfies \(j_X/p=-ax-av\,\partial_x\ln p(x\mid m)\). Horowitz and Esposito's contraction of that current against \(\partial_x\ln(p/(p_X p_M))\) and Hartich, Barato, and Seifert's learning rate \(-\int j_X\,\partial_x\ln p(x\mid m)\) differ by \(\langle(j_X/p)(x/v)\rangle\). For this equilibrium law that term is \(a-a=0\), so the two definitions are the same number. On 20 random linear joints the common value matches \(a(v/s-1)\), the memory-current contraction, and \(-\dot I_X\), with absolute gap at most \(3\times 10^{-15}\). In steady state this is the learning rate the memory's own transitions supply. The second law quoted by Horowitz and Esposito then puts the memory bath's entropy production at least at that rate. The signal's own Stratonovich power, diffusion \(av\) times \(\mathbb{E}[F^2]+\partial_X F\) with \(F=-X/v\), is identically 0. The signal bath does not pay the learning rate. Assumption A-X is the non-reciprocal coupling already used for the centered spring: the force on \(X\) does not depend on \(M\).

Fisher's inequality and Jensen's inequality on \(1/s\) give

\[
L=a\big(v\,\mathbb{E}[F(X\mid M)]-1\big)\ge a\Big(\frac{v}{\varepsilon_{\mathrm{MMSE}}}-1\Big)=R(\varepsilon_{\mathrm{MMSE}}),
\]

with equality when every conditional is Gaussian and the conditional variance is constant. Any action \(g(M)\) has mean squared error at least \(\varepsilon_{\mathrm{MMSE}}\), and \(R\) decreases on \((0,v]\), so \(L\ge R(\varepsilon)\) at that action's error. The raw coordinate error \(\mathbb{E}[(M-X)^2]\) is the conditional error plus \(\mathbb{E}[(M-\mathbb{E}[X\mid M])^2]\), so the same lower bound covers it. Assumption A-R is the right hypothesis for the integration by parts \(\langle xu\rangle=-1\): positive smooth conditionals, finite Fisher information, boundary terms gone. A hard bin is outside that hypothesis, as the note says.

Duncan's theorem, SIAM J. Appl. Math. 19:215–220 (1970), is the path mutual information of the causal filter. For the observation obtained by removing the known \(-\beta M\,dt\) from \(dM\), that rate is \(\gamma^2 P/(4D)\). The scalar Riccati \(\gamma^2 P^2=4aD(v-P)\) converts it into \(R(P)=a(v-P)/P\). The path error \(P\) is at most the error \(s\) given \(M_t\) alone, so the path rate is at least the learning rate, and the two agree when the state is a sufficient statistic of its path. The lower bound proved in §3 is the learning-rate bound. The path rate is a larger number on the designs that attain the heat floor.

At the printed shrunk spring, \(a=v=kT=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), the learning rate is \(4.000000000020\) and the path rate is \(999.503125\). Sensory capacity \(L/\mathcal T\) is \(0.004002\). Along the same family the capacity is \(0.774\) at \(\lambda=6\), \(0.841\) at \(\lambda=20\), and then \(0.407\), \(0.128\), \(0.040\), \(0.004\) at \(\lambda=10^2,10^3,10^4,10^6\). The limit that brings the heat to \(R(\varepsilon)\) sends the capacity to 0. That is the regime in which Hartich, Barato, and Seifert's factor \(2\) does not apply. Their factor \(2\) is the capacity-1 tradeoff, and the centered spring meets it.

**The shrunk spring.** SymPy gives raw error exactly \(\varepsilon\) and heat exactly

\[
\dot Q=a(v-\varepsilon)\frac{\rho}{\rho(v+\varepsilon)-v},\qquad\rho=\frac{\lambda}{a+\lambda},
\]

for \(\lambda>av/\varepsilon\). The ratio to \(R(\varepsilon)\) is \(\rho\varepsilon/(\rho(v+\varepsilon)-v)\). At \(a=v=1\), \(\varepsilon=0.2\) the ratios are the exact fractions in the note: \(6\), \(4/3\), \(20/19\), \(200/199\), \(2000/1999\), and \(200000/199999\). The heat at \(\lambda=10^6\) is

\[
\frac{800000}{199999}=4.0000200001000005\ldots
\]

The printed \(4.000020\) is that value rounded to six digits after the decimal point. The conditional variance there is \(0.199999999999200\) and the regression gain \(\mathbb{E}[X\mid M]/M\) is \(1.000001000001\). At \(\lambda=6\) the same formulas give heat \(24\), learning rate \(4.645161290323\), conditional variance \(0.177142857143\), and gain \(1.2\). Calibration is the limit. At finite rate the optimal action is still a multiple of \(M\), and that multiple is not yet \(1\).

The centered spring at the same raw error \(0.2\) and \(\lambda=10^6\) has heat \(5.00002000\), conditional variance \(0.16666694\), and learning rate \(4.99999000\). The heat meets \(R(s)\) at \(s=v\varepsilon/(v+\varepsilon)\) and exceeds \(R(0.2)\) by \(1.00002000\). The identity

\[
\frac{av}{\varepsilon}-a\frac{v-\varepsilon}{\varepsilon}=a
\]

is that difference. Holding the decision error at \(0.2\) on the centered spring means holding the raw coordinate error at \(v\varepsilon/(v-\varepsilon)=0.25\). At \(\lambda=10^6\) that design has conditional variance \(0.20000032\), heat \(4.00001200\), and gain \(0.80000048\). The action \(g(M)=\mathbb{E}[X\mid M]\) is a function of the current memory state, which is what A-B already allows, and it meets the same heat and the same decision error as the shrunk spring. Moving the rest point to \(cX\) with \(c=1-\varepsilon/v\) puts that gain into the force, so the coordinate itself becomes the estimate. Both spend the memory-bath heat on the error \(R\) prices. Comparing the two at the same raw \(\mathbb{E}[(M-X)^2]\) charges the centered coordinate for an estimate it is not using. Section 4 says this. The column in §7 is the centered heat at the same numerical raw error.

Hartich, Barato, and Seifert, Phys. Rev. E 93, 022116 (2016), equation (47) without the memory coordinate is the centered spring \(\dot r=-\omega_r(r-x)+\xi\). Their (52), (53), and (54) match the learning rate, the transfer entropy, and the entropy production on and off the capacity-1 noise, to \(10^{-12}\) relative. At \(\nu=9\), \(B=\nu^2/(\nu^2-1)\), the conditional error is \(0.2\) and the heat is \(8\), twice \(R(0.2)\). Their (63) is \(\sigma=2l+\tilde\sigma\) and (64) is \(\eta\le 1/2\), under the fictitious-memory step their §V states and the note leaves in the open list. On the centered family the efficiency increases with the noise and its supremum is \(\nu/(1+\nu)\), which is below \(1\). The factor-1 limit is the shrunk gain, outside that one-parameter family.

**The frontier.** Minimizing \(kT\,R(\varepsilon)+w\varepsilon\) on \((0,v]\) gives \(wv\) for \(w\le kT a/v\), and \(2\sqrt{kT\,a\,v\,w}-kT a\) above that threshold. The two expressions agree at the threshold, both equal to \(kT a\). At \(a=v=kT=1\) the critical points and costs are

| Stake | Error | Heat | Cost |
|---|---|---|---|
| 0.5 | 1 | 0 | 0.5 |
| 1 | 1 | 0 | 1 |
| 2 | 0.707106781187 | 0.414213562373 | 1.828427124746 |
| 3 | 0.577350269190 | 0.732050807569 | 2.464101615138 |
| 8 | 0.353553390593 | 1.828427124746 | 4.656854249492 |
| 20 | 0.223606797750 | 3.472135955000 | 7.944271909999 |
| 50 | 0.141421356237 | 6.071067811865 | 13.142135623731 |

The rows at 2, 8, 20, and 50 match §7 to the printed digits. The centered raw-error objective, minimizing \(av/\varepsilon+w\varepsilon\), has minimum cost \(2\sqrt{avw}\). That cost sits above the blind cost \(wv\) at stakes 2 and 3 (\(2.828427\) and \(3.464102\)). Stake 3 lies between \(kT a/v=1\) and \(4kT a/v=4\), so the two heat objectives disagree on whether to track. Where both track, the minimizing error agrees because the floors differ by the constant \(kT a\).

**The other checks.** The reference point \((a,\lambda,v,D)=(1,2,1,0.3)\) has raw error \(29/60=0.483333333333\), Sekimoto heat \(40/9=4.444444444444\), and learning rate \(1.194029850746\). Thirty stable two-memory linear systems from seed 19, the box in the author's checks, all have heat above their learning rate. The closest heat in that draw is \(1.615570\) times \(R\) of its conditional error. The draw is not a minimization. Embedding the shrunk spring at \(\lambda=10^4\), \(\varepsilon=0.2\), next to an equilibrium second coordinate leaves the heat at \(4.0020010005\), the one-coordinate value.

A fine quadrature of the soft \(K\)-bin channel (Newton quantiles, 12001-point trapezoid on \([-12,12]\)) reproduces the retuned learning rates to \(1.4\times 10^{-4}\):

| \(K\) | This grid | Draft |
|---|---|---|
| 8 | 4.471197 | 4.471064 |
| 16 | 4.157908 | 4.157870 |
| 32 | 4.058752 | 4.058746 |
| 64 | 4.022937 | 4.022937 |

The parent's six-digit table matches the draft at \(K=2\) and moves in the sixth digit at larger \(K\), because the draft's bin edges are a `searchsorted` inverse CDF. The PR body's four rounded heats, \(4.471\), \(4.158\), \(4.059\), \(4.023\), are the right rounding of either grid. The quartic conditional on the author's \(801\times 1201\) grid reproduces MMSE \(0.120383\), Fisher \(11.019370\), and excess \(2.712561\). A \(1601\times 2401\) grid keeps the MMSE and moves the Fisher to \(11.016660\), excess \(2.709851\). The sign and a gap near \(2.7\) hold. The note already says those digits are not a closed form.

## Required fixes

1. **`theory/INFO_PHYSICS.md` still gives the answer this draft withdraws, and it needs a dated correction record.** The centered-family calculations in §8a stand. Along \(dM=-\lambda(M-X)\,dt\), at fixed raw error below the signal variance, the heat falls toward \(kT\,av/\varepsilon\) and the flow rises from \(R(\varepsilon)\) to the same value, and the raw-coordinate heat objective is blind at stake 2, cost 2. That is what `reviews/info_physics_2026-11-22/REVIEW.md` and `reviews/info_physics_2026-11-22_round2/REVIEW.md` scored. Those reviews stay correct for that family and that loss. T37 and IP10 in this draft already point the open question at IP11.

   Four sentences are not scoped to that family. For an exogenous equilibrium OU signal under mean squared error they still state the attainment as open:

   - The opening answer, line 17: the bound "is not tight on the linear spring" and "\(kT\) times the flow is not, in general, the tangent of the physical frontier."
   - Section 8a, line 280, the same claim.
   - Line 310: "They do not exhibit a coupling that attains the Kalman rate at finite heat equal to that bound. This note does not construct one either. Whether a nonlinear potential, or a different bath, closes the gap is OPEN."
   - Line 360, and §11 line 395: "Whether any coupling attains the Kalman rate at finite heat equal to \(kT\) times that rate is OPEN. The spring does not."

   A linear change of the rest point, and a linear readout of the centered coordinate, both close that gap for this signal and this loss. The correction should say so, name the attainability note, and keep the centered raw-error stake table as the table of that coordinate. The same paragraph should label the §7 column "centered spring, raw coordinate held at this error." At a matched decision error the centered heat meets \(kT\,R\).

2. **The printed attaining point has path rate \(999.503\) and capacity \(0.004002\), and the limit sends the capacity to 0.** Section 5 says the fast shrunk spring has \(C<1\). That inequality is true and much stronger than a near miss. Next to the capacity-1 cost of \(8\), the sentence should carry the path rate at \(\lambda=10^6\), so the factor-1 heat is read as the learning-rate regime. Hartich's factor \(2\) covers the sufficient statistic. This design attains the floor with a state that keeps almost none of the path information.

3. **The \(K\)-bin heats are learning rates of the bin posterior.** `attainability_checks.py` computes \(a(v\mathbb{E}[F]-1)\) and does not integrate a bath heat for a \(K\)-state memory. Section 6 equates the two in the fast-equilibrium limit. That limit is proved for the telegraph and, by the rational gap in §4, for the linear spring. It is not derived for this channel. The table should be labeled as learning rates, with the heat equality stated as the same limit, still unproved for the bins. The attainment of the floor is the shrunk spring's Sekimoto heat.

4. **The signal-bath check does not evaluate the power.** In `test_identity_and_signal_bath` the assertion is `near(1.0 - 1.0, 0.0)`. The identity \(av\cdot\mathbb{E}[X^2]/v^2+av\cdot(-1/v)=0\) is true, and it is the proof in §3. The check that carries the name of that proposition should evaluate the expression.

## What is new, and what is already published

The inequality "memory-bath entropy production at least the learning rate" is Horowitz and Esposito, Phys. Rev. X 4, 031015 (2014), and the learning-rate form on a sensor is Barato, Hartich, and Seifert, New J. Phys. 16, 103024 (2014). The capacity-1 tradeoff \(\eta\le 1/2\), with equality on the tuned bare sensor, is Hartich, Barato, and Seifert, Phys. Rev. E 93, 022116 (2016), equations (63)–(64) and the bare-sensor point \(B=\nu^2/(\nu^2-1)\). Their centered family does not reach efficiency 1 at a positive learning rate. Duncan 1970 is the path mutual information. Bo, Del Giudice, and Celani, J. Stat. Mech. (2015) P01014, bound information a memory holds about the sensory past beyond the present reading. Crossref lists the families as Bo, Giudice, and Celani.

Mitter and Newton, J. Stat. Phys. 118, 145–176 (2005), doi 10.1007/s10955-004-8781-9, define information supply, storage, and dissipation for the Kalman–Bucy filter and give a statistical-mechanical analogy in which the filter returns signal energy to the bath without an entropy increase, because of the information supply. That analogy is not a lower bound on the bath heat of a physical memory, and it is not a spring that meets \(kT\,R(\varepsilon)\). Horowitz and Sandberg, New J. Phys. 16, 125007 (2014), are the second-law inequalities already booked in `theory/INTERNAL_MODEL.md` with Mitter and Newton. The shape "heat at least \(kT\) times an information flow" is that literature. The identity of the greatest lower bound with \(R(\varepsilon)\) for every regular conditional is the Fisher argument in §3.

Sandberg, Delvenne, Newton, and Mitter, Phys. Rev. E 90, 042119 (2014), doi 10.1103/PhysRevE.90.042119, build a Kalman–Bucy demon whose nonequilibrium implementation cost is \(2kT\) times the transfer-entropy rate (their equation (46), \(\dot W_{\mathrm{impl}}=2kT\,\dot I_c\)). The Allerton paper, doi 10.1109/ALLERTON.2014.7028503, records that this passive implementation sits at least a factor 2 above the Landauer comparison they use, and leaves the best power lower bound open. That factor 2 is the capacity-1 cost. It is the cost of a state that keeps the path information. It is not the infimum of the learning-rate heat over memories whose state is not a sufficient statistic.

What this draft adds, and what the recomputation supports:

- The identity \(L=a(v\,\mathbb{E}[F]-1)\) for every regular conditional of this exogenous equilibrium OU signal, and the consequence \(L\ge R(\varepsilon)\) at the error of any action of the current state. Each piece is prior art or textbook. The combination, as a lower bound on the learning rate of every regular memory of this signal, is the argument on the page.
- The shrunk spring, with the raw error held at \(\varepsilon\) and the heat approaching \(kT\,R(\varepsilon)\) at finite values, and the centered spring plus the conditional-mean readout, which meets the same pair. Hartich's centered family does not.
- The reading of the constant \(kT\,a\) as \(R(s)-R(\varepsilon)\) on the unshrunk coordinate. Continuity, one degree of freedom, and causality do not force it. The capacity-1 constraint forces a factor 2 on a different design.
- The frontier \(wv\) below \(w=kT a/v\) and \(2\sqrt{kT\,a\,v\,w}-kT a\) above it, including the stake interval between \(kT a/v\) and \(4kT a/v\), where the raw-coordinate heat objective is blind and this frontier tracks.
- The \(K\)-bin learning rates, the quartic Fisher excess, and the two-memory draw, as numerics. The \(K\)-bin heat label is fix 3.

The master equation is not this frontier. The note says so. H3, the stake, ruin, and linking stay outside.

## DOIs

All six DOIs in §11, and the three this review adds, returned Crossref HTTP 200 on 22 November 2026. Year, title, container, and the family names match the record.

| DOI | Year | Container | Families |
|---|---|---|---|
| 10.1103/PhysRevX.4.031015 | 2014 | Physical Review X | Horowitz; Esposito |
| 10.1088/1367-2630/16/10/103024 | 2014 | New Journal of Physics | Barato; Hartich; Seifert |
| 10.1103/PhysRevE.93.022116 | 2016 | Physical Review E | Hartich; Barato; Seifert |
| 10.1088/1367-2630/16/12/125007 | 2014 | New Journal of Physics | Horowitz; Sandberg |
| 10.1137/0119020 | 1970 | SIAM J. Appl. Math. 19, pages 215–220 | Duncan |
| 10.1088/1742-5468/2015/01/P01014 | 2015 | J. Stat. Mech. | Bo; Giudice; Celani |
| 10.1007/s10955-004-8781-9 | 2005 | J. Stat. Phys. | Mitter; Newton |
| 10.1103/PhysRevE.90.042119 | 2014 | Physical Review E | Sandberg; Delvenne; Newton; Mitter |
| 10.1109/ALLERTON.2014.7028503 | 2014 | Allerton Conference | Sandberg; Delvenne; Newton; Mitter |

Duncan's title on the record is "On the Calculation of Mutual Information." The note's citation matches the pages. On the Bo paper, Crossref's family field for the second author is Giudice, as the note says.

## Checks

On head `0c9422b`, from `/tmp/pr178`:

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT: PASS. FAIL 0. Rows counted 389, tally total 389. Advisory length warnings on THEORY main text and README |
| `python3 tools/check_open_work.py` | RESULT: PASS. Union missing from OPEN_WORK.md: 0 |
| `nice -n 19 python3 theory/info_physics_checks/attainability_checks.py` | PASS 28, FAIL 0 |
| `nice -n 19 python3 -m pytest -q tools` | 254 passed, 1 skipped, 308.95 s, exit 0. The skip is `tools/test_lean.py` (lake not installed). No lake build |

On this review branch, which is `origin/main` plus this directory: `check_consistency.py` PASS (rows 388, tally 388, claim map v2.84), `check_open_work.py` PASS, and `nice -n 19 python3 -m pytest -q tools` is 253 passed, 1 skipped, 304.42 s, exit 0. The extra pass on the draft head is `tools/test_attainability_checks.py`. NumPy for `recompute.out` is 1.26.4. SymPy 1.13.3 was used for the algebra; the recomputation does not import SciPy. Pytest was run after upgrading to NumPy 2.2.6 and SciPy 1.15.3, because the repository calls `np.trapezoid`, which NumPy 1.26 does not provide. A first pytest on NumPy 1.26 stopped in `np.trapezoid` and is an environment failure, not a result about this draft.

## Confirm

Checked head `bd53b5929c97b8c18654642c6d87e3df93c3e3fc` on `attainability-2026-11-22`. The recomputation is the same `recompute.py`, re-run at nice 19, and it still imports nothing from the author's checks. The draft branch was not edited. Nothing was merged. The hypothesis sentence is byte-identical to `origin/main`.

**The required fixes are in. One sentence remains.**

1. **Correction record.** `theory/INFO_PHYSICS_CORRECTION_2026-11-22.md` is dated 22 November 2026. It keeps the centered spring \(dM=-\lambda(M-X)\,dt\), scored by \(\mathbb{E}[(M-X)^2]\), as the family the reviews of PR #175 scored, including the blind heat objective at stake 2. It names the four passages that stated no coupling attains the Kalman rate at finite heat, and supersedes them for an exogenous equilibrium OU signal when the loss is the mean squared error of an action of the current memory state. Pointers with that scope sit at the top of `theory/INFO_PHYSICS.md`, under the opening answer, under the §8a spring paragraph, at the close of §8a, and on the §11 attainment bullet. The superseded sentences are kept in the file.

2. **Decision loss.** Section 0 defines \(\varepsilon=\mathbb{E}[(g(M)-X)^2]\), with the minimum at \(g(M)=\mathbb{E}[X\mid M]\), and says every \(\varepsilon\) is that decision error unless the sentence says raw coordinate error. A-R defines regular: a positive smooth density, finite Fisher information, and \(\int x\,\partial_x p\,dx=-1\). A hard bin is outside it. A-L is that decision error.

3. **Centered readout.** The same script gives, at \(a=v=1\), \(\lambda=10^6\), raw coordinate error held at \(0.25\): conditional variance \(0.200000319999\), heat \(4.00001200004\), gain \(0.80000048\). The printed \(0.20000032\) and \(4.00001200\) are those values. The shrunk spring at decision error \(0.2\) has heat \(800000/199999=4.000020000100\).

4. **The learning-rate proof.** The displays give \(L=-\langle(j_X/p)\,u\rangle=a(v\,\mathbb{E}[F]-1)\). The marginal contraction is \(-a+a=0\). Fisher and Jensen give \(L\ge R(\varepsilon_{\mathrm{MMSE}})\), and \(R\) decreasing gives \(L\ge R(\varepsilon_{\mathrm{MMSE}})\ge R(\varepsilon)\). Duncan is stated as the path rate \(R(P)\), equal to the learning rate only when \(P=s\). The signal-bath check now evaluates the power at \(a=1.7\), \(v=0.4\), which is \(0\) to \(10^{-15}\).

5. **Capacity.** On the shrunk spring the script gives path rate \(999.503125\) and capacity \(0.00400199\) at \(\lambda=10^6\), and the sequence \(0.774194\), \(0.841240\), \(0.407408\), \(0.128116\), \(0.040188\), \(0.004002\). The note's four-decimal capacities match. The centered readout at the same rate has path rate \(999.502125\) and capacity \(0.00400198\). Both limits sit at capacity \(0.004\).

6. **Citations.** Crossref on this run returned HTTP 200 for 10.1007/s10955-004-8781-9 (2005, J. Stat. Phys., Mitter and Newton) and 10.1103/PhysRevE.90.042119 (2014, Physical Review E, Sandberg, Delvenne, Newton, and Mitter). In the journal text, equation (46) is \(\dot W_{\mathrm{impl}}=2kT\,\dot I_c\). The note's description of Mitter and Newton as the analogy, and of Sandberg's equation (46) as that implementation cost, matches those sources. The new-claims list in §9 is the five items in this review: the Fisher bound, the shrunk spring and the centered readout, the scoring gap \(kT\,a\), the frontier including the stake interval, and the numerics with the \(K\)-bin figures labeled as learning rates.

7. **\(K\)-bin and the rows.** Section 6 is headed "NUMERICAL, learning rates" and says the bath heat of the channel is not computed. T37 scopes the blind stake-2 objective to the centered spring at raw coordinate error and points the decision loss at T38. T38 uses the decision error, the heat \(4.000020\), the readout figures \(0.20000032\) and \(4.000012\), path rate \(999.503\), capacity \(0.004\), and the learning-rate label. IP9's status is unchanged and its note says the row is the centered raw-coordinate spring. IP11 states the decision loss, both heats, the path rate, the capacity, Sandberg's factor, the frontier, and the learning-rate label, still PROVED (in-model). Tally stays 389. No new row.

The quartic disclaimer is unchanged: the check locks the sign, and the printed Fisher is the coarse grid.

**The sentence that remains.** Proposition AT-learn, lines 75 and 107, says the Horowitz–Esposito information flow of the signal current and the learning rate are the same number. The displays define

\[
\dot I_X=\Big\langle\frac{j_X}{p}\,(u+x/v)\Big\rangle,\qquad L=-\Big\langle\frac{j_X}{p}\,u\Big\rangle.
\]

The marginal contraction vanishes, so \(\dot I_X=-L\). The learning rate is minus the signal-current flow. In steady state the memory's own flow supplies \(L\), which the next sentence already says. Lines 75 and 107 should say that. The inequality \(L\ge R(\varepsilon)\) is the one the expansion proves, and it is unaffected.

On head `bd53b59`: `check_consistency.py` PASS (rows 389, tally 389, claim map v2.86), `check_fresh.py` PASS (STATUS names `c9f02df`, inside the window that contains `origin/main` `12febaf`), `check_open_work.py` PASS, `attainability_checks.py` PASS 31, FAIL 0. No lake build.

`nice -n 19 python3 -m pytest -q tools` on this head: 254 passed, 1 skipped, 308.05 s, exit 0. The skip is `tools/test_lean.py`.
