# Review of draft PR #180

**Verdict: SOUND-WITH-FIXES.**

Independent review of head `905321682dc083e014f8b312b4e6cb8b1dacbac8` on `heat-floor-general-2026-11-22`, one commit on `origin/main` `954fc2f56683c0a018cd18398739f2508b600038`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake build`. Computations at nice 19.

The per-mode floor is the learning-rate bound for one joint memory, and a joint error covariance with the same marginals sits above it. The frontier, the blindness threshold, and the geometric count hold. The sum-loss heat infimum is the minimum of that learning-rate bound over every regular conditional, and the spring is the family that approaches it. It equals the scalar Kalman bound of the summed signal when every rate is equal. When the rates differ it is the rank-one value \(\mu\), which is smaller than the sum of the scalar bounds. The comparison with N65 is accurate, and the coupled design matches 7.999913 against 8. Four repairs are on the page: one displayed threshold, the word "correlation", two sentences in §8 that disagree with each other and with IP14, and a missing citation of the continuous-time vector sensor-design program.

The hypothesis sentence is unchanged. One copy, in `THEORY.md`, byte-identical to `origin/main`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The diff in `THEORY.md` is the claim-map version, v2.86 to v2.87. The master equation is the equation in THEORY. `CORE.md` is not in the diff. `theory/INFO_PHYSICS.md` and `theory/INFO_PHYSICS_ATTAINABILITY.md` are not in the diff. The correction record `theory/INFO_PHYSICS_CORRECTION_2026-11-22.md` is not edited. This note uses the decision-loss floor of that correction, \(kT\,a(v-\varepsilon)/\varepsilon\), and does not reuse the raw-coordinate floor \(kT\,av/\varepsilon\).

Recomputation is `reviews/heat_floor_general_2026-11-22/recompute.py`. It imports nothing from `theory/info_physics_checks/`. The Lyapunov covariance, the Sekimoto expectation, the algebraic Riccati, and both error allocations are derived in that file. NumPy for `recompute.out` is 1.26.4.

## What holds

**The learning rate of one joint conditional.** For an exogenous equilibrium diffusion with diffusion matrix \(D\) and covariance \(\Sigma\), the signal current in the joint density is \(j/p=-D\Sigma^{-1}x-Du\) with \(u=\nabla_x\ln p(x\mid m)\). The learning rate is the contraction \(L=-\langle(j/p)\cdot u\rangle\). Integration by parts under the note's regularity condition gives \(\langle x u^\top\rangle=-I\), and the Gaussian marginal cancels \(\operatorname{tr}(D\Sigma^{-1})\) against the equilibrium score, so

\[
L=\mathbb{E}[u^\top D u]-\operatorname{tr}(D\Sigma^{-1}).
\]

The Fisher matrix dominates the inverse conditional covariance, with equality for a Gaussian. The map \(S\mapsto\operatorname{tr}(D S^{-1})\) is convex, so Jensen replaces a random covariance by its mean. This bound is for the conditional the memory actually carries. It is not obtained by adding separate scalar theorems and then hoping the joint case is no worse.

For independent modes, \(D=\operatorname{diag}(a_k v_k)\) and \(\Sigma=\operatorname{diag}(v_k)\). The diagonal of an inverse dominates the reciprocal of the diagonal, by the Schur complement, so

\[
L\ge\sum_k a_k\Big(\frac{v_k}{s_k}-1\Big),\qquad s_k=\mathbb{E}[\operatorname{Var}(X_k\mid M)],
\]

with equality when the conditional is Gaussian, the conditional covariance is the constant diagonal matrix of the \(s_k\), and the action on each mode is the conditional mean. A suboptimal action has a larger decision error and a weaker bound; the infimum at a prescribed decision error uses the conditional mean. Horowitz and Esposito supply \(\dot Q\ge kT\,L\) for the memory bath. That implication is cited, as in the attainability note. The signal bath's medium heat is zero: on the three-mode Gaussian the quadratic form and the divergence are the same trace, and on the coupled pair the difference is \(4\times 10^{-16}\).

**A joint error covariance sits above the product floor.** At marginal variances \(0.3\) and \(0.4\) and \(D=\operatorname{diag}(1,2)\),

\[
\operatorname{tr}(D S^{-1})=8.333333333333
\]

on the diagonal matrix, and \(9.090909090909\) when the off-diagonal entry is \(0.1\). The Schur gaps are \(3.636364>3.333333\) and \(2.727273>2.500000\). The same trace at correlation coefficient \(0.1\), whose covariance entry is \(0.034641016151\), is \(8.417508417508\). Both sit above the diagonal value. The printed \(9.090909\) is the entry \(0.1\).

The product of shrunk springs meets the sum. Each spring has rest point \(cX\) with \(c=(v-\varepsilon)/v\), and the noise is fixed by the stationary moments so that the raw error \(\mathbb{E}[(M-X)^2]\) equals the named decision error. At \(\lambda=10^6\) the moment solution is the rational heat

\[
\frac{800000}{199999}=4.000020000100,\qquad \frac{1600000}{99998}=16.000320006400,
\]

against floors \(4\) and \(16\). The Lyapunov evaluation of the same SDEs gives \(4.000020001316\) and \(16.000320006162\), raw errors \(0.200000000000\) and \(0.100000000000\), and conditional variances \(0.199999999999\) and \(0.099999999994\). The six printed digits are those values. The path rate of one such spring, from the scalar Riccati, is \(999.503125010117\), so two copies sit at \(1999.006250\) against a learning-rate floor of \(8\). The ratio of floor to path rate is \(0.004002\).

A single rank-one Gaussian channel cannot meet both marginal targets \(0.2\) and \(0.1\) on variances \((1,0.5)\). In the zero-noise limit the two marginal inequalities require \(g_1^2\ge 2 g_2^2\) and \(g_1^2\le 0.125 g_2^2\). The per-mode loss at separated errors uses one coordinate per mode. A joint memory can meet the sum of the floors with a product of springs. It cannot undercut that sum.

**The per-mode frontier.** The cost of mode \(k\) is \(kT a_k v_k/s_k-kT a_k+w s_k\) on \(s_k\in(0,v_k]\). The second derivative is positive. The critical point is \(s_k=\sqrt{kT a_k v_k/w}\), and it lies inside the interval when \(w\ge kT a_k/v_k\). Below that stake the minimum on the interval is the prior, heat \(0\), cost \(w v_k\). At the stake itself the critical point is the prior. The tracked set in the note includes that tie; the cost is the same number either way. The minimum separates, so the frontier is the sum of the scalar frontiers.

For \(a=(1,10,100)\), \(v=1\), \(kT=1\) the recomputed costs are the printed table: \(1.500000000000\), \(5.828427124746\), \(46.228543157461\), \(289.569702822072\), with tracked counts \(0,1,2,3\).

On \(a_k=a\rho^{k-1}\) with equal variances, mode \(k\) is inside the tracked set when \(a\rho^{k-1}\le wv/(kT)\). Once the slowest mode pays, the count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) until the ladder ends, and multiplying the stake by \(\rho\) adds one mode. Counting by comparing \(10^{k-1}\) with \(w\), for \(a=v=kT=1\), gives \(0,1,1,2,3,4\) at stakes \(0.5,1,2,10,100,1000\).

**The sum loss.** The decision error of the conditional mean of \(Z=\sum_k X_k\) is \(1^\top\bar S\,1\). Law of total variance gives \(\bar S\preceq\Sigma\). Minimizing \(\operatorname{tr}(D(\bar S^{-1}-\Sigma^{-1}))\) on that set at a fixed sum-error is a convex program in the precision excess \(\Phi=\bar S^{-1}-\Sigma^{-1}\succeq 0\): the objective is linear and \(1^\top(\Sigma^{-1}+\Phi)^{-1}1\) is convex. The stationarity condition puts \(\Phi\) on the rank-one ray \(g g^\top\) with

\[
g_k=\frac{1}{a_k+\mu},\qquad \varepsilon=\sum_k\frac{a_k v_k}{a_k+\mu},
\]

and the minimum value is \(\mu\). Every coordinate of \(g\) is positive once \(\mu>0\), so the minimizing channel has no exactly blind mode. Dropping a mode and reoptimizing \(\mu\) is a different feasible point and is weakly worse, because the KKT point is the unique minimum. Four hundred random precision excesses on rates \((1,100)\), seed 19, produced no value below \(\mu\) at the same sum-error. The smallest slack was \(0.139361\).

The fast spring with that gain approaches the bound. At rates \((1,100)\), variances \((1,1)\), and target sum-error \(0.5\),

\[
\mu=\frac{101+\sqrt{11401}}{2}=103.887732673340,
\]

which is the positive root of \(\mu^2-101\mu-300=0\), and \(\sum a_k v_k/(a_k+\mu)\) returns \(0.5\). The Lyapunov spring at \(\lambda=10^6\) has heat \(103.877719378448\), learning rate \(103.856919702138\), and sum-error \(0.500076936208\). The floor at that realized error is \(103.856919445098\). The heat sits \(0.020800\) above that floor. It sits \(0.010013\) below the target \(\mu\) because the realized error is slightly worse than \(0.5\). The note prints the realized error next to the heat. The six digits \(103.877719\) and \(103.887733\) are these values rounded.

Separate memories at sum-error \(0.5\) use errors \(1/22\) and \(5/11\). The heat is \(21+120=141\) exactly. The ratio is \(141/\mu=1.357234356470\), which prints as \(1.357234\).

An equal-gain channel \(Y=g(X_1+X_2)+\xi\), the linear observation of the unweighted sum, has learning rate \(151.5\) at the same sum-error. That one channel sits above both \(\mu\) and \(141\). It is not a lower bound on every filter of the scalar series. The bound \(\mu\) already covers those filters, because it covers every regular conditional. Whether one of them reaches \(\mu\) when the rates differ is the open item in §9, and the recomputation does not close it.

When every rate equals \(a\) and every variance equals \(v\), \(dZ=-a Z\,dt+\sqrt{2a\cdot Kv}\,dW\). Then \(\mu=a(Kv-\varepsilon)/\varepsilon\), the scalar Kalman rate of \(Z\). Separate symmetric errors \(\varepsilon/K\) cost exactly \(K\) times that rate: the pairs \((K,\varepsilon)=(2,0.8),(3,1.1),(4,0.5)\) give joints \(1.5\), \(1.727272727273\), \(7\) and separate heats \(3\), \(5.181818181818\), \(28\). Equal rates and variances \((1,4)\) at sum-error \(2\) give joint floor \(1.5\) and separate heat \(2.5\), at errors \(2/3\) and \(4/3\). A memory that sees every mode, in the equal-rate case, is bounded by that scalar rate, and the constant gain meets it.

The sum-loss frontier minimizes \(kT\mu+w\varepsilon(\mu)\). The derivative at \(\mu=0\) is \(kT-w\sum v_k/a_k\), so the blind stake is \(w_0=kT/\sum(v_k/a_k)\). For three identical modes of rate \(1\) and variance \(1\), \(w_0=1/3\), and the recomputed table is the printed one, including \(\mu=3.898979485566\) at stake \(8\), joint cost \(8.797958971133\), and separate cost \(13.970562748477\). At stake \(0.5\) the joint memory tracks, cost \(1.449489742783\), and the separate memories are still blind, cost \(1.5\). At stake \(10^6\) the ratio of the optimized costs is \(1.731685\), against \(\sqrt{3}=1.732051\). The matched-error heat ratio stays \(K\).

On the infinite ladder \(a_k=\rho^k\), \(k\in\mathbb{Z}\), equal variances, the stake sum at \(\rho\mu\) is the stake sum at \(\mu\) divided by \(\rho\), so \(w(\rho\mu)=\rho\,w(\mu)\). The set \(\{k:a_k\le\mu\}\) gains one index. On the truncation \(k\in[-30,30]\), \(\rho=10\), \(\mu=50\), the stake ratio is \(10.000000000000\) and the count of included indices goes from \(32\) to \(33\). The half-tracked reading \(\varphi_k=\mu/(a_k+\mu)\ge 1/2\) is \(a_k\le\mu\). The finite ladder in §6 matches to the printed four decimals: \(\mu=0.581523,3.185140,17.051184,85.244498,729.261921\) at stakes \(2,8,40,200,2000\), with half-tracked counts \(0,1,2,2,3\) and hard counts \(0,1,1,2,3,4\) once the blind row at stake \(0.5\) is included.

**N65.** `measurement/LAYER_COUNT_RULE.md` and Theorem L2 in `theory/LAYERS.md` say what the note says they say. Observation counts in-band memory time constants by degree. Prediction takes the leftmost minimizer of \(K+R(1+\varepsilon_K)\) with \(R=w E_\infty/h\). When the decrements are non-increasing, that minimizer is the from-0 count of N64, Fox 1966. Otherwise it is the lower convex hull. N60 as written starts at \(1\) and has the \(K^\star=0\) hole. A formula in the poles and the stake alone, without \(\varepsilon_K\), is T18 and is open. The heat-floor counts do not use \(h\).

The four points of agreement hold. There is a blind regime on both sides. Both counts are nondecreasing in the stake. On the per-mode loss the heat-floor count is at most the number of modes, and it reaches that number once the stake clears the fastest threshold \(kT a_k/v_k\). L2(i)–(ii) has the same ceiling shape for a different cost: the causal filter of a sum of \(J\) OU modes has degree at most \(J\), and degree \(J\) at lead \(0\) once \(R\) is large enough. The note does not replace the joint decrements of a \(K\)-store filter by \(a_k/v_k\). It points at the recorded failure of that replacement in `core/keystone_checks/waterfill_2026-11-20/MATH.md`.

The four points of difference hold. The heat of a mode depends on its rate, and \(h\) does not. The geometric count is \(\log(w)/\log\rho\), and T18 records that N65 has no such shortcut. On the sum loss the minimizing precision excess is rank one, so the heat-optimal memory in the mode-resolved design has one coordinate at every stake above \(w_0\). L2's \(K^\star\) is the degree of a filter of the scalar series \(Z\), and that degree grows with \(R\) up to \(J\). Those are different design sets, and §7 says so. When the rates are identical, \(Z\) is one mode, the heat floor is one spring, and \(K\) separate memories cost \(K\) times the heat. Neither the heat floor nor the degree of \(Z\) selects those \(K\) memories. N65 is not amended. The claim-map diff does not change its row.

**Outside this class.** The coupled pair \(\Sigma=\bigl(\begin{smallmatrix}1&0.3\\0.3&1\end{smallmatrix}\bigr)\), \(D=\bigl(\begin{smallmatrix}0.8&0.1\\0.1&1.2\end{smallmatrix}\bigr)\), with a coordinatewise spring of rate \(10^5\) and noise level \(0.25\), has Lyapunov heat \(7.999912967993\) and learning rate \(7.999489966733\), against the static channel \(\operatorname{tr}(D)/0.25=8\). The signal Lyapunov residual is \(2\times 10^{-16}\). The note's \(7.999913\) and \(7.999490\) are these numbers. The design approaches its own static rate. The note labels it numerical and does not claim attainment for every error covariance of a coupled diffusion.

The reference linear memory \((a,v,\beta,\gamma,D)=((1,4),(1,0.5),3,(2,-1),0.4)\) has heat \(3.214285714286\), learning rate \(1.262924667651\), and gap \(1.951361046634\). The weighted spring at \(\lambda=500\), \(\mu=2\), rates \((1,4)\), has path rate \(14.831794136218\) and learning rate \(1.972390477464\).

The telegraph floor is left as the floor already proved in `theory/INFO_PHYSICS.md`. A joint jump memory of several telegraphs is marked open. A non-mean-square loss and a memory that changes \(X\) are marked open, on the same list as the attainability note.

**Bookkeeping.** IP1–IP11 keep their status words. IP12 and IP13 are PROVED (in-model). IP14 is OPEN. The tally goes from \(389\) to \(392\), PROVED (in-model) from \(133\) to \(135\), OPEN from \(96\) to \(97\). T38 gains a pointer to T39 and is otherwise the attainability answer. T37 is unchanged except that pointer's neighbor. The correction record still supersedes the merged note's attainment sentences for one OU signal and a mean-squared decision loss, and this draft does not reopen them.

## Required fixes

1. **The four-mode blind stake is \(1000/1111\), not \(100/111\).** Section 6 states the formula \(w_0=kT/\sum_k v_k/a_k\) and then, for rates \(1,10,100,1000\) and equal variance, prints \(w_0=0.900900900901\). That printed value is \(100/111\), the three-mode sum \(1+1/10+1/100=1.11\). The four-mode sum is \(1.111\), and

   \[
   w_0=\frac{1000}{1111}=0.900090009001
   \]

   to twelve decimals. The formula in G-front-sum is right. The \(\mu\) column of the four-mode table does not use the printed threshold, and those \(\mu\) values match the recomputation. The author's check compares \(w_0\) with \(1/(1+0.1+0.01)\) on the three-mode vector \((1,10,100)\), so it does not guard this sentence. Replace the displayed number.

2. **The word in §5 is the covariance entry.** "At correlation \(0.1\)" with the value \(9.090909\) is the matrix whose off-diagonal entry is \(0.1\). The correlation coefficient of that matrix is \(0.1/\sqrt{0.12}=0.288675134595\). At coefficient \(0.1\) the trace is \(8.417508417508\). The diagonal trace \(8.333333333333\) lies below both. Say "off-diagonal entry \(0.1\)".

3. **Section 8 names one equality twice, in opposite directions.** "Equality for a nonlinear potential is not attained" and "Equality in that potential is open" cannot both be the sentence. The quartic conditional in the attainability note has learning rate strictly above \(R\) of its error. The heat infimum remains \(kT\) times the Gaussian rate, because the shrunk springs attain it and G-learn puts every regular memory at or above it. The attainability note's open list is a signal that is not an equilibrium OU, a loss that is not a mean square, a memory that changes \(X\), the bath heat of the \(K\)-bin channel, equality at finite rate, the capacity-1 factor, and ruin, linking, \(w\), and H3. It does not leave a separate open row for a nonlinear potential's heat. Write those as three sentences.

4. **The driven-signal status should match §8.** Section 8 says the memory-bath reading does not survive when another bath pays, and names SE3 and the Barato–Hartich–Seifert receptor. IP14 then lists "a driven signal" inside an OPEN equality claim. State the same fact in both places. The existence claim is the one already recorded for a signal whose own bath pays. What remains open is a general rule for which bath pays, and this page does not add a new counterexample.

5. **Cite the continuous-time vector program next to the discrete one.** Tanaka, Skoglund, and Ugrinovskii, 2017 IEEE CDC, pp. 3992–3997, doi 10.1109/CDC.2017.8264246, minimize the Duncan mutual-information rate of a continuous-time vector Gauss–Markov source under the trace constraint \(\operatorname{tr}(P)\le D\). The minimum is a semidefinite program. Their constraint is the sum of the marginal mean squares. It is not \(1^\top P 1\), and the paper contains no bath heat. The citation already on the page, Tanaka, Kim, Parrilo, and Mitter, IEEE Trans. Automat. Control 62 (2017) 1896, is the discrete-time sequential rate-distortion program in directed information. Gorbunov and Pinsker, Problems of Information Transmission 9 (1973) 184 and 10 (1974) 93, and Stavrou, Charalambous, Charalambous, Loyka, and Skoglund, 2018 IEEE CDC, pp. 14–20, doi 10.1109/CDC.2018.8619725, are the nonanticipative rate, a \(\tfrac12\log\) reverse water-fill on the eigenvalues of a prediction-error covariance. One sentence that places those three next to Kolmogorov and Sims keeps §9's list from being read as the vector Duncan minimization.

## What is new, and what is not

The memory-bath inequality \(\dot Q\ge kT L\) is Horowitz and Esposito, Phys. Rev. X 4, 031015 (2014). The learning-rate form on a sensor is Barato, Hartich, and Seifert, New J. Phys. 16, 103024 (2014). Sensory capacity, and the statement that capacity \(1\) forces efficiency at most \(1/2\), is Hartich, Barato, and Seifert, Phys. Rev. E 93, 022116 (2016). Their worked example is one ligand and a two-component linear sensor. It is not a vector of independent OU modes and it is not this stake table. Sandberg, Delvenne, Newton, and Mitter, Phys. Rev. E 90, 042119 (2014), equation (46), set the implementation cost of the maximum-power Kalman–Bucy demon at \(2kT\) times the transfer-entropy rate. The same four authors' Allerton 2014 paper, doi 10.1109/ALLERTON.2014.7028503, is the port-Hamiltonian account of that implementation cost. Both price a state that keeps the path. The fast spring on this page sends the path rate to \(999.503125\) while the heat approaches the learning rate, which is the capacity going to \(0\), already computed for one mode in the attainability note.

Duncan, SIAM J. Appl. Math. 19, 215 (1970), is the path mutual information. For this equilibrium OU the Riccati identity makes that rate equal to \(a(v-P)/P\) at the filter's error variance \(P\). That scalar identification is already PD7 and the attainability note. Kolmogorov, IRE Trans. Inf. Theory 2, 102 (1956), and Sims, J. Monet. Econ. 50, 665 (2003), minimize a \(\tfrac12\log\) rate. The nonanticipatory epsilon-entropy of Gorbunov and Pinsker is the same shape of rate. The allocation on this page minimizes \(\sum a_k(v_k-s_k)/s_k\), or the single level \(\mu\), and those two functionals agree only at isolated errors.

What the recomputation supports, and what those papers do not state:

- For independent equilibrium OU modes, the learning-rate lower bound of one joint memory at per-mode decision errors \(s_k\) is exactly the sum of the scalar Kalman rates, and an off-diagonal error covariance raises it. The product of fast shrunk springs approaches the sum at finite heat. The heats \(4.000020\) and \(16.000320\) are the scalar construction, repeated.
- The per-mode frontier is the sum of the scalar frontiers. The threshold is \(kT a_k/v_k\). On a geometric ladder the tracked count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\).
- Under the sum loss, the minimum of the covariance bound is the unique \(\mu\) with \(\varepsilon=\sum a_k v_k/(a_k+\mu)\), the minimizing channel has gains \(g_k=1/(a_k+\mu)\) and rank one, and one fast memory approaches heat \(kT\mu\). For \(K\) identical modes the sum is one OU and \(K\) separate memories cost \(K\) times that heat at every matched error. At rates \((1,100)\) and sum-error \(0.5\) the separate heat is \(141\) and \(\mu=103.887732673340\). On the infinite equal-variance ladder, multiplying the stake by \(\rho\) adds one half-tracked mode.
- The comparison in §7. N65 and L2 count degree under a constant \(h\), on a filter of the scalar series. This floor has no \(h\). On the sum loss, inside the mode-resolved design, the heat-optimal degree is \(1\). The note does not change N65.
- The coupled numerical design, heat \(7.999913\) against its static rate \(8\).

The heat infimum for the sum loss is the bound above, together with Horowitz and Esposito and the attaining spring. It is not only the cost of the springs that were written down: every regular conditional is covered by G-learn and the convex program, and the spring shows the bound is approached at finite heat. The learning-rate bound is the scalar Kalman bound of \(Z\) when the memory sees every mode and the rates are equal. When the rates differ, the same memory is bounded by \(\mu\), and \(\mu\) is the quantity the rank-one gain attains.

## DOIs

All thirteen DOIs in §11 returned Crossref HTTP 200 on 22 November 2026. Year, title, container, and the family names in the note match the record. Details are in `reviews/heat_floor_general_2026-11-22/crossref.out`. The four comparison papers in that file returned HTTP 200 in the same session. Gorbunov and Pinsker 1973 and 1974 are cited, with volume and page, in the reference lists of doi 10.1109/CDC.2018.8619725 and doi 10.1109/TIT.2021.3124888. This session found no Crossref work record for either translation.

## Checks

On head `9053216`, in a detached worktree, nice 19:

| Command | Result |
|---|---|
| `python3 theory/info_physics_checks/general_checks.py` | PASS 33, FAIL 0 |
| `python3 tools/check_consistency.py` | RESULT: PASS. Rows counted 392, tally total 392. Advisory length warnings on THEORY main text and README |
| `python3 tools/check_open_work.py` | RESULT: PASS. Union missing from OPEN_WORK.md: 0 |
| `python3 -m pytest -q tools` | 255 passed, 1 skipped, 315.22 s, exit 0. The skip is `tools/test_lean.py`: `lake` is not on `PATH` and `~/.elan/bin/lake` is absent, and the test skips in that case |

Pytest was run after installing pytest 9.2.0, SciPy 1.18.1, and SymPy 1.14.0. That install pulled NumPy 2.5.5. The recomputation above was already finished on NumPy 1.26.4 and was not rerun. No `lake build`.

On this review branch, which is `origin/main` plus this directory, `check_consistency.py` reports rows 389 and tally 389, and `check_open_work.py` passes. The 392-row tally is the draft's.

## Confirm

**CONFIRMED.** Repair commit `661abc88f6ec32204f7df512abbcf5b9b3d327b5` on `heat-floor-general-2026-11-22`. This confirm does not edit that branch and does not merge. `origin/main` is still `954fc2f`. The recomputation was rerun from `reviews/heat_floor_general_2026-11-22/recompute.py`, which still imports nothing from `theory/info_physics_checks/`. NumPy for this rerun is 2.5.5. The printed heats, the ratio \(1.357234\), and the coupled heat \(7.999913\) are unchanged. No `lake build`.

The five repairs are in the note, the claim map, and OPEN_WORK T39.

1. **Four-mode blind stake.** The long division of \(1000/1111\) begins \(9000900090009000\). Rounding at the thirteenth digit, which is \(9\), gives \(0.900090009001\). The float \(1/(1+0.1+0.01+0.001)\) formats to the same twelve decimals and matches \(1000/1111\) within \(10^{-15}\). The three-mode value \(100/111\) still formats as \(0.900900900901\), and that number is no longer printed as the four-mode stake. Section 6, T39, the v2.88 note, and the changelog all say \(1000/1111\).

2. **Covariance and correlation.** At marginals \(0.3\) and \(0.4\) with \(D=\operatorname{diag}(1,2)\), the diagonal trace is \(8.333333333333\), the trace at off-diagonal entry \(0.1\) is \(9.090909090909\), and that entry has correlation coefficient \(0.1/\sqrt{0.12}=0.288675134595\). At correlation coefficient \(0.1\) the covariance entry is \(0.034641016151\) and the trace is \(8.417508417508\). Both sit above the diagonal. The proof in §5 and IP12 say this.

3. **Nonlinear potential.** Section 8 now has the three sentences. The quartic conditional has a learning rate strictly above \(R\) of its error. The heat infimum on an equilibrium OU signal remains \(kT\) times the Gaussian rate, because the shrunk springs attain it and G-learn puts every regular memory at or above it. The attainability note does not leave a separate open row for the heat of a nonlinear potential. The old pair of sentences, "not attained" and "open", is gone, and that item is gone from the open list.

4. **Driven signal.** Section 8 and IP14 say the same thing, and the status word is OPEN. The case in which the signal's own bath pays is already recorded, in SE3 and in the Barato–Hartich–Seifert receptor. This page does not add a counterexample. A general rule for which bath pays is open. The opening paragraph of the note says the same.

5. **Citations.** Tanaka, Skoglund, and Ugrinovskii, doi 10.1109/CDC.2017.8264246, returned Crossref HTTP 200 on 22 November 2026: 2017, 56th IEEE CDC, pp. 3992–3997, title "Optimal sensor design and zero-delay source coding for continuous-time vector Gauss-Markov processes", families Tanaka, Skoglund, Ugrinovskii. Stavrou, Charalambous, Charalambous, Loyka, and Skoglund, doi 10.1109/CDC.2018.8619725, returned HTTP 200: 2018, pp. 14–20, the asymptotic reverse-waterfilling title, those five families. The Crossref event string is "2018 IEEE Conference on Decision and Control (CDC)". The 2017 record is explicitly the 56th. Gorbunov and Pinsker are cited as Problems of Information Transmission 9:184 and 10:93, with no DOI. A Crossref title query on this date did not return a work record for either translation. Those opening pages are the ones in the reference list of the 2018 CDC paper (English translation, vol. 9, pp. 184–191, 1973, and vol. 10, pp. 93–109, 1974) and in doi 10.1109/TIT.2021.3124888. The note says the constraint in the 2017 CDC paper is \(\operatorname{tr}(P)\le D\), that the minimum is a semidefinite program, and that the paper contains no bath heat. The \(\tfrac12\log\) papers are placed next to Kolmogorov and Sims. The sum-loss allocation is still described as the level \(\mu\).

**Geometric count.** The note defines \(K_{\mathrm{hard}}\) as the cardinality of \(\{k:a\rho^{k-1}\le wv/(kT)\}\), and states that once \(w\ge kT a/v\), and until the ladder runs out, that cardinality is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\). Comparing rates \(10^{k-1}\) with \(w\) gives \(0,1,1,2,3,4\) at stakes \(0.5,1,2,10,100,1000\). The exact logarithm at stake \(1000\) is \(3\). The floating-point ratio \(\log(1000)/\log(10)\) is \(2.9999999999999996\), so a bare floor of that ratio plus one prints \(3\). The page states the exact expression, and the count it defines is the cardinality, which is \(4\). T39, IP12, §7, and the v2.88 note use the floor expression, with the clause that it applies once the slowest mode pays.

**New-claims list.** Section 9's five bullets are the five items in "What is new" above: the joint per-mode bound and the off-diagonal increase, with the heats identified as the scalar construction repeated; the sum of the scalar frontiers, the threshold \(kT a_k/v_k\), and the floor count; the sum-loss level \(\mu\), rank one, the factor \(K\), separate heat \(141\) against \(\mu=103.887732673340\), and the half-tracked ladder; the N65 and L2 comparison, with N65 unchanged; the coupled design at \(7.999913\) against \(8\). No sixth claim was added. The vector learning-rate identity stays in the proved list and is no longer listed as a separate addition.

**Nothing new overclaims.** No row changes status. IP12 and IP13 stay PROVED (in-model). IP14 stays OPEN. The tally stays \(392\). The hypothesis sentence is byte-identical to `origin/main`. The diff in `THEORY.md` is the claim-map version, v2.87 to v2.88. N65 is unchanged. `theory/README.md` still says the tracked-mode count scales as \(\log(w)/\log\rho\). That is the growth of the floor count.

On head `661abc8`, detached worktree, nice 19:

| Command | Result |
|---|---|
| `python3 theory/info_physics_checks/general_checks.py` | PASS 33, FAIL 0 |
| `python3 tools/check_consistency.py` | RESULT: PASS. CLAIM_MAP latest note v2.88. README, STATUS, and THEORY point at v2.88. Rows counted 392, tally total 392 |
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS.md main is `74e02e7`; window `954fc2f 74e02e7 b46bf9f 12febaf c9f02df` |
| `python3 tools/check_open_work.py` | RESULT: PASS. Union missing from OPEN_WORK.md: 0 |
| `python3 -m pytest -q tools` | 255 passed, 1 skipped, 313.67 s, exit 0. The skip is `tools/test_lean.py` |

No remaining fixes.
