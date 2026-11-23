# Hostile review of draft PR #203

Sunday 22 November 2026. Independent review of the acting-derivation draft. Head `d755e2c4c9975b839157601d286750d7c30c65ec` on `cursor/acting-derivation-2d99`. This review is cut from that head. It edits none of the draft's files. It does not push to that branch and it does not merge. No lake build.

**VERDICT: NEEDS-FIXES.**

The continuous gains on the cubic plant are \(K_E=0.2327\) and \(K_H=0\). The difference is \(0.2327\), below the preregistered number \(0.25\). The locked grid reports \(0.25\) because that is its fine spacing, and the prediction is one step of that grid. Theorem R1′ is a representation theorem. Debreu's additive form carries it. It is not a derivation from the drift.

## 1. The locked comparison is one grid step

`theory/acting_derivation_checks/PREREG.md:41`–`:45`, `:63`, `:71`. `theory/ACTING_DERIVATION_2026-11-22.md:167`. `theory/acting_derivation_checks/RESULTS.md:19`.

The grid is \(0,\ 0.25,\ 0.5,\ 0.75,\ 1,\ 1.5,\ 2,\ 3,\ 4\). The fine spacing is \(0.25\). The later gaps are \(0.5\) and \(1\). Any two distinct gains on this grid differ by at least \(0.25\). The prediction \(K_E-K_H\ge 0.25\) is the same statement as \(K_E>K_H\). The preregistration says the tolerance was chosen because it is the smallest strict separation the grid can show. That sentence is accurate, and it is the whole content of the inequality.

The locked run scores \(K_E=0.25\), \(K_H=0\), difference \(0.25\). On the protocol's own rule the prediction was met. The pass is the boundary value of a one-step rule. \(J_E\) at \(0.25\) is \(0.456944514863\), and \(J_E\) at \(0.50\) is \(0.459180113427\). Those two means differ by \(0.002236\).

### What git shows before the lock

Commit `1271eb0` (22:53:27 UTC) adds only `PREREG.md`. Commit `977810f` (22:53:31 UTC) adds only `LOCK.txt`. Commit `d755e2c` (22:57:04 UTC) adds `run_locked.py`, `RESULTS.md`, `results.out`, and the numbers in the note and in T47. The gap from the lock to the result commit is 213 seconds. The recorded runtime is 128.7 seconds.

The blob of `PREREG.md` is `847dc4174cd4dfd2a5ace7ff2538f606d6cde254` at `1271eb0`, at `977810f`, and at `d755e2c`. Its sha256 is `7f3b0034de4bea307c4510ade0edde7ccae94ef413d397b52cd9976edb6084a2`, the digest in `LOCK.txt`. At the lock, section 5 says the costs are not restated until the run has been done. No cubic trajectory, no `run_locked.py`, and no decimal gain exist in any ancestor of `977810f`. The parent `98cbfe0` already contains `closed_rates`, so the linear lemma's rate at the gate parameters is the number 2 before any trajectory. A private run before the commit is outside what the history can show. The commit order, the unchanged blob, and the absence of a cubic simulator are what the lock can show, and they hold.

The cubic ordering was at risk of a tie or a reversal. Corollary LG-K had already proved the ordering for a linear plant, and the cubic is the case that corollary does not cover. The quantitative threshold was not at risk of a gap smaller than one fine step, because this grid cannot represent one. The continuous gap below is a miss of the number \(0.25\) and a pass of this grid, because the grid can only report \(0\) or \(0.25\) in that range.

### The path estimate and its Monte Carlo error

The locked linear trajectory was rerun with `Generator(PCG64(20261122))`, the same step, and the same lengths. The path rate is `1.973637317765` again. The lemma's rate is 2. The relative difference is \(0.013181341\), which the note rounds to \(0.013181\).

The observable whose mean is \(\mathrm{Sr}_X+\mathrm{Sr}_M\) is \(2(X^2+M^2-1)\) at these parameters. The stationary covariance is the identity, and the integrated autocovariance of the exact diffusion gives a standard error \(0.1414\) on a record of length 800. The relative standard error is \(0.0707\). Twenty-four independent Euler–Maruyama runs of the same length have sample standard deviation \(0.1168\) (relative \(0.0584\)) and mean \(1.99385\). The locked draw sits \(0.02636\) below 2, about one fifth of that standard error. Eight of the twenty-four runs miss the relative tolerance \(0.05\). The gate's tolerance is inside the Monte Carlo error of the estimator. The draw that was recorded is a quiet one.

At zero gain the cubic world is an equilibrium diffusion, so the stationary \(\mathrm{Sr}_X\) is 0. The exact variance is \(\mathbb{E}[X^2]=0.467920\). The recorded path estimate \(0.050189309209\) is a fluctuation of an observable whose standard deviation, under that equilibrium, is \(4.82\).

### Continuous gains

The same costs were minimized on the stationary Fokker–Planck equation, by a Scharfetter–Gummel scheme with no-flux faces. This is a robustness check. The preregistration is unchanged. Brent's method on \(\mathbb{E}[X^2]\), tolerance \(10^{-4}\):

| cells \(N\) | half-width \(L\) | \(K_E\) | \(\mathbb{E}[X^2]\) at 0 | slope of \(J_H\) at 0 |
|---|---|---|---|---|
| 200 | 4.0 | 0.232679 | 0.467983 | 0.5998 |
| 160 | 4.0 | 0.232664 | 0.468018 | 0.6000 |
| 180 | 4.5 | 0.232400 | 0.468018 | 0.5970 |
| 160 | 4.5 | 0.232388 | 0.468044 | 0.5971 |

The four values of \(K_E\) lie in \([0.2324, 0.2327]\). \(J_H\) is increasing at 0 on each of them, and on the \(N=160\), \(L=4\) sweep it keeps rising through \(K=0.8\). The heat-aware gain is \(K_H=0\). The difference is \(0.2327\) at the finest square grid, and \(0.2324\) when the box is widened. Both are below \(0.25\). The shortfall, \(0.017\), is about fifty times the spread across these resolutions.

At \(K=0\) the same \(N=200\), \(L=4\) solve gives \(\mathbb{E}[X^2]=0.467983\) against the exact quadrature \(0.467920\). The \(N=160\), \(L=4\) bath rate \(\mathrm{Sr}_X\) is \(0.000625\) against 0. An Euler–Maruyama grid at spacing \(0.05\) and record length 8000 has a standard error near \(0.0035\) on \(\mathbb{E}[X^2]\). The well is \(0.00572\) deep. That grid does not locate the minimum. The stationary solve does.

The code is `reviews/acting_derivation_2026-11-22/robustness.py`.

**Repair.** In section 5 and in T47, keep the locked score as a score of the grid, state that \(0.25\) is one fine step, and put the continuous gains beside it. State the standard error of the gate.

## 2. The derivation is a representation theorem

`theory/ACTING_DERIVATION_2026-11-22.md:3`, `:13`–`:15`, `:31`–`:63`. `theory/REPRESENTATION.md:19`–`:25`, `:45`, `:62`, `:84`–`:96`. `THEORY.md:24`–`:26`.

R1′ is a representation theorem. It is not a physical derivation.

A1–A6 and A7′ do imply the additive shape, in the same sense that A1–A7 imply Theorem R1. The weight is Debreu's theorem on three or more essential intervals, the von Neumann–Morgenstern index under the risk neutrality already in A2, and the Cauchy lemmas C, P, and C\(_\mathbb{Z}\). A7′ changes the law under which the coordinates are evaluated, and it adds the effort coordinate when \(b\neq 0\). The drift does not produce the sum. The note's own invocation of Theorem R2 says so: storing, predicting, acting, and staying solvent still do not force it. The header "A derivation, not an adoption" and the label "PROVED HERE, from A1–A6 and A7′" describe the packaging as if it were proved from the dynamics on this page. Steps 2 through 5 are the representation note's steps, cited and not re-proved. The step that is proved here is the \(b=0\) deletion of \(z_u\).

### The \(b=0\) reduction

The reduction is exact as an equality of the cost as a function of the design, before minimization, under A8 and the extra preferential independence of the integer layer count. The note names both assumptions. The display is

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L,
\]

subject to \(P(\mathrm{ruin})\le\varepsilon_r\). All five terms are in that display. None is removed by a minimization. The effort coordinate is absent because A7′ omits it at \(b=0\). The ruin constraint stays a constraint. This matches the five-term expression inside THEORY §3. THEORY writes a \(\min\) on the left of that expression. The note says its equality is not the value at a minimizer. That distinction is right.

It is not an equality forced by A1–A6 and A7′ alone. Nonnegative prices are A8. The term \(hK\) is the extra separability assumption, which is not Debreu's theorem. The check script sums a dictionary of five numbers. That sum is not the representation.

### Both clauses of A7 at \(b=0\)

A7 in `theory/REPRESENTATION.md:62` has two clauses. The law of the world does not depend on the design, and the resource vector and the loss lottery are functions of the design against that fixed law. Effort spent changing the world's drift is not a coordinate.

At \(b=0\), with the feedback rule entering the joint generator only as the additive drift \(b\,u\), both clauses hold, and neither is weakened inside that case. The world's drift is \(F_0\), the world's diffusion does not depend on the design, the loss lottery is computed against that fixed law, and the effort coordinate is absent.

The page does not say that \(u\) is absent from the memory drift and from the diffusion coefficients. Step 1 infers "the law does not depend on \(u\)" from the drift of \(X\) alone. The joint law can depend on \(u\) through the memory. The inference is not proved. The clause-recovery claim becomes true when that sentence is added. It is not true of the text as it stands.

### The diffusion form of the Horowitz–Esposito split

Horowitz and Esposito, *Phys. Rev. X* 4, 031015 (2014), equation (10), is the split of \(\mathrm d_t I\) into the two jump currents. Equation (11) is

\[
\dot S^X_{\mathrm i}=\mathrm d_t S^X+\dot S^X_r-\dot I^X\ge 0
\]

and the same line for \(Y\). For one thermal reservoir they set \(\dot S_r=-\dot Q/T\). The last paragraph of the main text says that the continuous limit of their master equation would be a bipartite Fokker–Planck equation, and they do not carry out that limit. The note's account of what they did not prove is correct.

Lemma D's definitions,

\[
\dot I_X=\int J_X\,\partial_X\ln p(M\mid X),\qquad
\dot I_M=\int J_M\,\partial_M\ln p(X\mid M),
\]

are the diffusion transcription of their (10). The steady-state identity \(\int J_X^2/(D p)=\mathrm{Sr}_X-\dot I_X\ge 0\), with \(\mathrm{Sr}_X=\mathbb{E}[F_X^2+D\,\partial_X F_X]/D\), follows from the integration by parts on the page. The algebra was redone from the Fokker–Planck current and agrees. In the class stated just above the lemma, mobility is 1 and \(D=kT\), so the energy flow into the bath is \(D\,\mathrm{Sr}_X\). That matches their sign, \(\dot S_r=-\dot Q/T\), with the heat into the bath equal to \(T\,\mathrm{Sr}_X\).

The proof produces \(\mathrm d_t S_X\) and then sets it to zero. Equation (11) keeps that term. The steady-state case is what is proved. The displayed formula for \(\mathrm{Sr}_X\) has a stray vertical bar in front of it (`theory/ACTING_DERIVATION_2026-11-22.md:110`).

### The Gaussian-loss ordering

Corollary LG-K is correct. With \(a,b,\gamma,c,D,D_M>0\), the numerator of \(v'(K)\) is quadratic in \(K\). Its leading coefficient is \(D_M b^3 c>0\) and its constant term is \(-D b c\gamma^2<0\), so there is one positive root. The denominator of \(v\) does not vanish for \(K\ge 0\). Thus \(v'(0)<0\), \(v(K)\to\infty\), and the one critical point is a minimum \(K_E>0\). The closed moments, the bath rates, and \(\dot I_M\) reduce identically to the Lyapunov solution and to the Gaussian evaluation of Lemma D. At \(b=0\), \(\mathrm{Sr}_X=0\), \(v=D/a\), and \(\dot I_M\) equals the learning rate \(a C_{XM}^2/\det\) of `theory/INFO_PHYSICS_ATTAINABILITY.md` §4. A centered Gaussian has \(\mathbb{E}[X^4]=3v^2\), strictly increasing in \(v\), so a quartic loss inside LG-b has the same minimizer as \(v\).

The heat that enters \(J_H\) is \(D\,\mathrm{Sr}_X+D_M\,\mathrm{Sr}_M=(Dc\gamma+D_M b K)(c\gamma+b K)/(a+\gamma)\). Its derivative in \(K\) is positive for \(b>0\) and \(K\ge 0\). Combined with \(v'>0\) for \(K>K_E\) and with \(\varphi\) strictly increasing, every minimizer of \(J_H\) on \([0,\infty)\) is strictly less than \(K_E\). The page establishes monotonicity of the unweighted sum \(\mathrm{Sr}_X+\mathrm{Sr}_M\) and then uses that fact as the derivative of the weighted heat. The unweighted sum is also increasing. It is not the term in \(J_H\).

### Labels

The label rule on the page is that PROVED HERE means the argument is on the page.

| Claim | Label on the page | What the argument supports |
|---|---|---|
| Theorem R1′, additive form | PROVED HERE from A1–A6 and A7′ | STANDARD. It is Theorem R1 on the product A7′ names |
| \(b=0\) deletion of \(z_u\) | inside that same label | PROVED HERE, once \(u\) enters only as \(b\,u\) |
| Steps 2–5 | STANDARD | accurate |
| Lemma D, steady state | PROVED HERE | accurate, apart from the stray bar |
| Lemma LG closed form | PROVED HERE | the identity is true and is not proved on the page. The text points at five floating-point comparisons |
| Corollary LG-0 | PROVED HERE | accurate once Lemma LG is |
| Corollary LG-K | PROVED HERE | the ordering is true. The heat it differentiates is the weighted sum |
| Cubic ordering | CONJECTURE | accurate. Section 5 then scores a grid |

## 3. The citations

Crossref, fetched 22 November 2026. Every DOI in the note resolves. The attributed titles match.

| DOI | Crossref | What the note uses it for |
|---|---|---|
| 10.1017/ccol052123736x.010 | Debreu, "Topological methods in cardinal utility theory," in *Mathematical Economics*, pp. 120–132. `issued` is `[[null]]`. Author entries: Gerard Debreu, Gerard Debreu, Werner Hildenbrand | Additive representation on at least three essential intervals. The empty year field matches. Hildenbrand is the volume editor and is also in the author list |
| 10.1515/9781400829460 | von Neumann and Morgenstern, *Theory of Games and Economic Behavior (60th Anniversary Commemorative Edition)*, issued 2007-12-31 | The edition and the year. Risk neutrality is A2, which the note names |
| 10.1103/PhysRevX.4.031015 | Horowitz and Esposito, *Phys. Rev. X* 4, 031015 (2014), "Thermodynamics with Continuous Information Flow" | Equations (10) and (11), and the continuous limit left unproved. Matches the paper |
| 10.1103/PhysRevLett.102.250602 | Sagawa and Ueda, *Phys. Rev. Lett.* 102, 250602 (2009), the measurement-and-erasure title | Equation (4) of the arXiv version (30 May 2009) is \(W^{\mathrm M}_{\mathrm{meas}}+W^{\mathrm M}_{\mathrm{eras}}\ge k_B T I\). The letter's inequality (2) is the measurement bound, which is how the erratum cites it, so the letter's numbering matches |
| 10.1103/PhysRevLett.106.189901 | Erratum, *Phys. Rev. Lett.* 106, 189901 (2011), of that paper | The erratum's own equation (4) is a faulty entropy identity in the 16th paragraph. Correcting it withdraws the original proof of the letter's inequality (2) unless each POVM element is one operator. The sum bound is not withdrawn. The note cites the erratum by title and does not describe this restriction |
| 10.1103/PhysRevLett.104.090602 | Sagawa and Ueda, *Phys. Rev. Lett.* 104, 090602 (2010), "Generalized Jarzynski Equality under Nonequilibrium Feedback Control" | Equation (3) is \(\langle W\rangle\ge\Delta F-k_B T\langle I\rangle\). Equation (4) is \(\langle e^{-\beta(W-\Delta F)-I}\rangle=1\). Equation (6) is \(\langle e^{-\beta(W-\Delta F)}\rangle=\gamma\), and \(\gamma\) is the efficacy, summed over backward measurement probabilities. The note's statement matches, including that \(\gamma\) is not a feedback gain |

## 4. The house rules

`git diff 459e1fd HEAD -- THEORY.md` is empty. `git apply --check theory/THEORY_ACTING_PROPOSAL_2026-11-22.diff` succeeds, and the proposal is not applied. The hypothesis line in that diff is context.

The sentence "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." occurs once in `THEORY.md` and once in the note. The bytes of the sentence match.

A whole-word search of the note, the preregistration, the checks, the proposal diff, and the T47 row finds no `bill`, no `kill`, and no `verdict`. The objective is named cost. T47 is `OPEN_WORK.md:97`.

## Required fixes

**1. Section 5, the paragraph that begins "The gate held".** Replace that paragraph with:

> The locked grid scores \(K_E=0.25\) and \(K_H=0\), so the difference is \(0.25\). On the protocol's own rule the prediction was met. The fine spacing of the grid is \(0.25\), and every pair of distinct grid gains differs by at least \(0.25\), so the prediction is the same statement as \(K_E>K_H\). It is one step, which is what the preregistration says the tolerance is. A stationary solve of the same costs, left out of the preregistration, gives continuous gains \(K_E=0.2327\) and \(K_H=0\) at \(N=200\), \(L=4\). Widening the box moves \(K_E\) to \(0.2324\). The difference is below \(0.25\). The gate's path estimate \(1.973637317765\) against \(2\) has relative difference \(0.013181\). The standard error of that estimator on a record of length 800 is \(0.12\) to \(0.14\) (relative \(0.058\) to \(0.071\)). Eight of twenty-four equal-length trajectories miss the \(0.05\) gate. The recorded \(\mathrm{Sr}_X\) at zero gain, \(0.050189309209\), estimates a stationary value of \(0\).

**2. The T47 row, the sentences that begin "The linear gate held".** Replace those sentences with:

> The locked grid scores \(K_E=0.25\), \(K_H=0\), difference \(0.25\). On that grid the prediction was met. The fine spacing is \(0.25\), so the inequality is one step and is the same statement as \(K_E>K_H\). The continuous stationary gains are \(K_E=0.2327\) and \(K_H=0\), difference \(0.2327\), below \(0.25\). The gate's relative difference \(0.013181\) sits inside a relative standard error of \(0.058\) to \(0.071\).

**3. The header and the theorem label.** Replace "A derivation, not an adoption." with:

> A representation theorem, not a derivation from the drift, and not an adoption.

Replace the label **Theorem R1′ (PROVED HERE, from A1–A6 and A7′, by the steps marked).** with:

> **Theorem R1′ (a representation theorem).** The additive form is Theorem R1 applied to the product A7′ names. Debreu's theorem, the von Neumann–Morgenstern index, and the Cauchy lemmas carry that form. They are **STANDARD**. The step **PROVED HERE** is the \(b=0\) reduction: the effort coordinate drops out and the world law is the exogenous law, so the cost is Theorem R1's cost. The drift does not produce the sum.

**4. Step 1 of the proof.** Replace the step with:

> 1. **PROVED HERE**, once the generator is stated. The feedback rule \(u\) enters the joint generator only as the additive drift \(b\,u\). The drift \(F_0\), both diffusion coefficients, and the memory drift do not depend on \(u\). The design induces one law \(P^{b,u}\). At \(b=0\) that law does not depend on \(u\), the law of \(X\) does not depend on the design, and the effort coordinate is absent. Those are the two clauses of A7, and neither is weakened inside this case.

**5. The bath-rate display.** Replace `|\mathrm{Sr}_X=` with `\mathrm{Sr}_X=`.

**6. The last sentence of Lemma LG.** Replace "The algebra is the Gaussian evaluation of Lemma D. The check script compares these expressions with a direct solve of the Lyapunov system and with the expectation in Lemma D." with:

> These expressions are the Gaussian evaluation of Lemma D. They reduce identically to the Lyapunov solution and to \(\mathbb{E}[F^2+D\,\partial F]/D\). The check script compares floating-point values at five points. That comparison is not the proof.

**7. The sentence "is strictly increasing in \(K\)." under the display of \(\mathrm{Sr}_X+\mathrm{Sr}_M\).** Replace it with:

> \(\mathrm{Sr}_X+\mathrm{Sr}_M\) is strictly increasing in \(K\). The heat in \(J_H\) is \(D\,\mathrm{Sr}_X+D_M\,\mathrm{Sr}_M=(Dc\gamma+D_M b K)(c\gamma+b K)/(a+\gamma)\), and that sum is strictly increasing for \(b>0\) and \(K\ge 0\).

## Recommended fixes

**R1.** After the steady-state sentence in the proof of Lemma D, say that the integration by parts produces \(\mathrm d_t S_X\) before it is set to zero, and that Horowitz and Esposito's (11) keeps that term.

**R2.** On the Sagawa–Ueda erratum, say that its repair of the letter's inequality (2) uses the stronger assumption that each POVM element is a single operator, and that the sum bound cited as equation (4) is not the equality the erratum numbers (4).

**R3.** On the Debreu record, say that Crossref also lists Werner Hildenbrand, the volume editor, in the author array.

**R4.** The five-term check sums a dictionary. Say that, next to the check, so a passing script is not read as a proof of R1′.

**R5.** The attainability note's Sekimoto heat, at \(kT=1\) with the force equal to the drift divided by the diffusion coefficient, equals this note's \(\mathrm{Sr}\). This note's energy flow is \(D\,\mathrm{Sr}\), because mobility is 1 and \(D=kT\). One sentence will keep a later reader from adding the two heats.

## Checks

NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, pytest 9.2.0. The closed forms were reduced in SymPy: bath rates, information flow, the \(b=0\) learning rate, and the quadratic numerator of \(v'\) all simplify to the expressions above. The locked linear path estimate was reproduced to twelve decimals. `nice -n 19 python3 theory/acting_derivation_checks/acting_derivation_checks.py` prints `FAILS 0`. `nice -n 19 python3 reviews/acting_derivation_2026-11-22/robustness.py` reproduces the four gains in the table above. `nice -n 19 python3 tools/check_consistency.py` prints `RESULT: PASS`, with the pre-existing advisory length warnings on THEORY and README. `nice -n 19 python3 tools/check_open_work.py` prints `RESULT: PASS` and `union missing from OPEN_WORK.md: 0`. `nice -n 19 python3 -m pytest -q tools` prints `261 passed, 1 skipped` in 411.86s. The skip is `tools/test_lean.py`, because Lean 4 / lake is not installed. No lake build.
