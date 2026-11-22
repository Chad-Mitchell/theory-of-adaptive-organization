# The heat floor for several modes

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. No locked preregistration file is edited. Checks: `theory/info_physics_checks/general_checks.py`, run at `nice -n 19` (33 checks, FAILS 0). DOIs resolved on the Crossref API on 22 November 2026 are listed in `theory/info_physics_checks/general_crossref.out`.*

Labels: **PROVED** (a proof is on this page, under the assumptions named with it), **PROVED (in-model)** (the same, inside a stated model), **PRIOR ART** (published, credited, not claimed here), **NUMERICAL**, **OPEN**. A lower bound is not a derivation of the cost. This note does not assume a per-layer constant \(h\).

The scalar case is `theory/INFO_PHYSICS_ATTAINABILITY.md`. For one exogenous equilibrium Ornstein–Uhlenbeck signal and a mean-squared decision loss, the memory-bath heat infimum at decision error \(\varepsilon\) is \(kT\,R(\varepsilon)\) with \(R(\varepsilon)=a(v-\varepsilon)/\varepsilon\), approached at finite heat by a fast shrunk spring or by the centered spring read at its conditional mean. The frontier is \(wv\) for \(w\le kT a/v\) and \(2\sqrt{kT\,a\,v\,w}-kT a\) above that stake. Those statements stay. This note is the vector step.

## 0. The question, and the answer

The signal is a vector of exogenous equilibrium Ornstein–Uhlenbeck modes,

\[
dX_k=-a_k X_k\,dt+\sqrt{2 a_k v_k}\,dW_k,
\]

independent of each other, variances \(v_k\), memory baths at temperature \(T\). The repository's multi-scale world is the scalar sum of such modes. Two decision losses are named, because they do not have the same minimizer.

**Per-mode loss.** The action reads the current memory and the decision error of mode \(k\) is \(s_k=\mathbb{E}[(g_k(M)-X_k)^2]\). The total error is \(\varepsilon=\sum_k s_k\).

**Sum loss.** The action estimates \(Z=\sum_k X_k\), and \(\varepsilon=\mathbb{E}[(g(M)-Z)^2]\). This is the loss of one scalar world that is a sum of modes.

**Answer.** On the per-mode loss, the infimum of the memory-bath heat at errors \((s_k)\) is \(kT\sum_k R_k(s_k)\), with \(R_k(s)=a_k(v_k-s)/s\). That sum is the steady Kalman–Bucy information rate of a product filter whose error variances are the \(s_k\). It is also the learning-rate bound. A product of fast shrunk springs approaches it at finite heat. A joint error covariance with the same marginal variances cannot undercut it. The frontier at one stake \(w\) on \(\varepsilon\) is the sum of the scalar frontiers. Mode \(k\) is tracked when \(w\ge kT a_k/v_k\) and is blind otherwise. For rates in a geometric ladder \(a,\,a\rho,\,a\rho^2,\ldots\) and equal variances, the number of tracked modes is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) once the slowest mode pays, and \(0\) below that stake.

On the sum loss, one memory coordinate is enough. Its heat infimum at error \(\varepsilon\) is \(kT\,\mu(\varepsilon)\), where \(\mu\) solves \(\varepsilon=\sum_k a_k v_k/(a_k+\mu)\). That \(\mu\) is the Kalman–Bucy rate of the optimal linear channel at that error, and it is the learning-rate bound. For \(K\) identical modes the sum is itself one Ornstein–Uhlenbeck signal, the floor is the scalar floor of that signal, and \(K\) separate memories cost exactly \(K\) times as much heat at every matched error. No mode is set exactly blind once \(\mu>0\). Modes with \(a_k\gg\mu\) keep almost their whole prior variance in the sum. On an infinite geometric ladder of equal variances, multiplying the stake by \(\rho\) raises the count of modes whose sum-error contribution is at least halved by exactly one.

The layer-count rule in `measurement/LAYER_COUNT_RULE.md` (N65, T15) is a different object. It counts poles of a measured kernel, and it predicts \(K^\star=\arg\min(K+R(1+\varepsilon_K))\) with \(R=w E_\infty/h\). Section 7 states where the two counts agree and where the formulas differ. N65 is unchanged.

Past this class, the quartic conditional has a learning rate strictly above \(R\) of its error, and the heat infimum on an equilibrium OU signal remains the Gaussian rate. A general rule for which bath pays is open. The case in which the signal's own bath pays is already recorded. The telegraph floor stays the one already proved. A non-quadratic loss, a memory that moves its world, and a signal that is not an equilibrium diffusion stay open.

## 1. Scope

- **G-X.** Each mode is exogenous. Its drift and diffusion do not depend on the memory. This is A-X of the attainability note. A memory that moves \(X\) is outside.
- **G-E.** Each mode is the equilibrium scalar above, or, where the sentence says so, one coupled equilibrium diffusion \(dX=-D\Sigma^{-1} X\,dt+\sqrt{2}\,dW_D\) whose diffusion matrix \(D\) is symmetric and positive and whose stationary covariance is \(\Sigma\). The signal bath's medium heat is zero. A driven signal, whose own bath can pay, is the case SE3 and Barato, Hartich, and Seifert already separate.
- **G-B.** The memory is a bipartite Markov process on the same probability space, one bath or several, at temperature \(T\). The action is a function of the current memory state. The checks set \(kT=1\).
- **G-R.** A conditional \(p(x\mid m)\) is regular when it is a positive smooth density, the Fisher information matrix is finite, and the boundary terms in the integrations by parts below vanish. A hard bin is not regular.
- **G-L.** The loss is one of the two mean squares in §0. A loss that is not a mean square of an action of the current state stays open, as in the scalar note.

No term in this note is a constant \(h\) per layer. Where a comparison writes \(h\), it is the upkeep in N65, quoted as that rule's input.

## 2. What is already proved, or already published

Nothing in this list is claimed as new.

- **Kalman and Bucy (1961)**, *J. Basic Eng.* 83:95, doi 10.1115/1.3658902. The linear filter and its error covariance. The scalar content of L1 is already booked as known.
- **Duncan (1970)**, *SIAM J. Appl. Math.* 19:215, doi 10.1137/0119020, as booked in PD7 and in the attainability note. The path mutual information. For the linear memory it equals \(R(P)\) at the path error \(P\). It equals the learning rate only when the state is a sufficient statistic of the path.
- **Horowitz and Esposito (2014)**, *Phys. Rev. X* 4:031015, doi 10.1103/PhysRevX.4.031015. In steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\). The shape \(\dot Q\ge kT\) times the learning rate is theirs.
- **Barato, Hartich, and Seifert (2014)**, *New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024. The learning rate is at most the entropy production of the learning subsystem.
- **Hartich, Barato, and Seifert (2016)**, *Phys. Rev. E* 93:022116, doi 10.1103/PhysRevE.93.022116. Sensory capacity \(C=l/\mathcal T\). If \(C=1\), efficiency is at most \(1/2\). The scalar note recomputes that tradeoff and does not re-prove it.
- **Sandberg, Delvenne, Newton, and Mitter (2014)**, *Phys. Rev. E* 90:042119, doi 10.1103/PhysRevE.90.042119. Their equation (46) sets the implementation cost of a Kalman–Bucy demon that keeps the path information at \(2kT\) times the transfer-entropy rate. That is the capacity-1 cost. It is not the infimum of the learning-rate heat.
- **Mitter and Newton (2005)**, *J. Stat. Phys.* 118:145, doi 10.1007/s10955-004-8781-9. The statistical-mechanical analogy for the filter. Not a lower bound on the bath heat of a physical memory.
- **Horowitz and Sandberg (2014)**, *New J. Phys.* 16:125007, doi 10.1088/1367-2630/16/12/125007. Second-law inequalities with an information flow.
- **Kolmogorov (1956)**, *IRE Trans. Inf. Theory* 2:102, doi 10.1109/TIT.1956.1056823. The rate-distortion function of a stationary Gaussian source is reverse water-filling on the spectrum: a water level on \(\tfrac12\log(S(f)/\theta)\). The rate in that theorem is \(\tfrac12\log\), not \(a(v-\varepsilon)/\varepsilon\).
- **Sims (2003)**, *J. Monet. Econ.* 50:665, doi 10.1016/S0304-3932(03)00029-1. The same reverse water-filling under a mutual-information price. Already the prior-art side of the repository's water-filling note.
- **Tanaka, Kim, Parrilo, and Mitter (2017)**, *IEEE Trans. Automat. Control* 62:1896, doi 10.1109/TAC.2016.2601148. The discrete-time sequential rate-distortion function of a vector Gauss–Markov source, in directed information, is a semidefinite program. This note does not re-solve that program. The scalar causal rate used below is Duncan's, as already booked.
- **Tanaka, Skoglund, and Ugrinovskii (2017)**, *56th IEEE CDC*, pp. 3992–3997, doi 10.1109/CDC.2017.8264246. They minimize the Duncan mutual-information rate of a continuous-time vector Gauss–Markov source under \(\operatorname{tr}(P)\le D\). The minimum is a semidefinite program. The constraint is the sum of the marginal mean squares. It is not \(1^\top P 1\), and the paper contains no bath heat.
- **Gorbunov and Pinsker (1973, 1974)**, *Problems of Information Transmission* 9:184 and 10:93. The nonanticipative epsilon-entropy. Crossref returned no work record for either translation on 22 November 2026. Both volumes and pages are cited in the reference lists of doi 10.1109/CDC.2018.8619725 and doi 10.1109/TIT.2021.3124888.
- **Stavrou, Charalambous, Charalambous, Loyka, and Skoglund (2018)**, *57th IEEE CDC*, pp. 14–20, doi 10.1109/CDC.2018.8619725. An asymptotic \(\tfrac12\log\) reverse water-fill for the nonanticipative rate-distortion function of a vector Gauss–Markov source under mean squared error, on the eigenvalues of a prediction-error covariance.
- **Tatikonda, Sahai, and Mitter (2004)**, doi 10.1109/TAC.2004.834430. Causal rate constraints for linear control. Already PD1b's prior art.
- **Fox (1966)**, *Manage. Sci.* 13:210, doi 10.1287/mnsc.13.3.210. Marginal analysis for a discrete convex allocation. N64's exactness argument. Used here only as that citation, already on the layer-count page.
- **The attainability note**, for one mode. **INFO_PHYSICS** for the telegraph floor, the centered raw-error spring, and the bookkeeping that separate baths add their heats. **`core/keystone_checks/waterfill_2026-11-20/MATH.md`** for the recorded distinction between a price per nat, a constant \(h\) per state, and a count of frequency peaks. That test stays a recorded failure. This note does not rescore it.
- **N60, N64, N65, T15.** The operational count and the from-0 identity. Section 7 quotes them and does not change them.

## 3. The learning rate of a vector equilibrium diffusion

**Proposition G-learn (PROVED, under G-X, G-E, G-R).** Let the memory state \(M\) carry a regular conditional of the equilibrium diffusion, with diffusion matrix \(D\) and covariance \(\Sigma\). Write \(u=\nabla_x\ln p(x\mid m)\) and \(F(m)=\int u u^\top p(x\mid m)\,dx\). The learning rate is

\[
L=\mathbb{E}[\operatorname{tr}(D F)]-\operatorname{tr}(D\Sigma^{-1}).
\]

If \(\bar S=\mathbb{E}[\operatorname{Cov}(X\mid M)]\), then \(L\ge\operatorname{tr}\big(D(\bar S^{-1}-\Sigma^{-1})\big)\), with equality when every conditional is Gaussian with covariance \(\bar S\). For independent modes, \(D=\operatorname{diag}(a_k v_k)\) and \(\Sigma=\operatorname{diag}(v_k)\), and

\[
L\ge\sum_k a_k\Big(\frac{v_k}{s_k}-1\Big)=\sum_k R_k(s_k),
\]

where \(s_k=\mathbb{E}[\operatorname{Var}(X_k\mid M)]\), with equality when the conditional is Gaussian, the conditional covariance is constant and diagonal, and \(s_k\) is that diagonal.

*Proof.* The signal is exogenous and stationary at its equilibrium, so the probability current of the signal coordinates in the joint density is \(j/p=-D\Sigma^{-1}x-Du\). The learning rate is \(L=-\langle(j/p)\cdot u\rangle\). The marginal contraction against the equilibrium score vanishes by the same integration by parts as in the scalar proof: \(\langle x\,u^\top\rangle=-I\) under G-R, and \(\langle x^\top\Sigma^{-1} D\Sigma^{-1}x\rangle=\operatorname{tr}(D\Sigma^{-1})\) for the Gaussian marginal, so the two terms cancel and \(L=\mathbb{E}[u^\top D u]-\operatorname{tr}(D\Sigma^{-1})\). The Fisher matrix of a regular conditional dominates the inverse conditional covariance in the Loewner order, with equality for a Gaussian. The map \(S\mapsto\operatorname{tr}(D S^{-1})\) is convex on positive definite matrices because inversion is operator convex and \(\operatorname{tr}(D\,\cdot\,)\) is linear and monotone for \(D\) positive semidefinite. Jensen's inequality gives the expectation bound. For a diagonal \(D\), \((S^{-1})_{kk}\ge 1/S_{kk}\), with equality when the \(k\)-th mode is conditionally uncorrelated with the others. A second Jensen step, on \(1/S_{kk}\), replaces the random conditional variance by \(s_k\). ∎

Duncan's theorem is not this bound. It is the mutual-information rate of a path observation. For a linear observation of this equilibrium diffusion, the steady Kalman–Bucy error covariance \(P\) satisfies the Riccati equation, and the Duncan rate equals \(\operatorname{tr}(D(P^{-1}-\Sigma^{-1}))\). The algebra is the trace of the Riccati against \(P^{-1}\): with drift \(-D\Sigma^{-1}\) and process-noise intensity \(2D\), the observation term that remains is twice the Duncan rate, and the drift terms produce \(2\operatorname{tr}(D\Sigma^{-1})\). So the Kalman–Bucy rate at error covariance \(P\) and the Gaussian learning rate at the same covariance are one number. The path rate of a memory whose state is not a sufficient statistic of its path is larger, as in the scalar note.

**Proposition G-signal (PROVED, under G-X and G-E).** The medium heat of the signal bath is zero.

*Proof.* The equilibrium force is \(F_X=-\Sigma^{-1}X\) and the diffusion matrix of the Fokker–Planck operator is \(D\). The Stratonovich power is \(\mathbb{E}[F_X^\top D F_X]+\nabla\cdot(D F_X)\). The divergence is \(-\operatorname{tr}(D\Sigma^{-1})\). The quadratic term equals the same trace for a Gaussian of covariance \(\Sigma\). The checks evaluate the difference at \((a,v)=((1.7,0.4,3.0),(0.4,1.1,0.7))\), where both terms are \(5.1\), and on one coupled pair. ∎

Horowitz and Esposito then put every bipartite memory's bath at least at \(kT\,L\). That implication is theirs. The linear family below computes the Sekimoto heat directly.

## 4. One linear memory of independent modes

**Model (PROVED (in-model) for the formulas in this section).** Modes as in §0, and

\[
dM=\Big(-\beta M+\sum_k\gamma_k X_k\Big)dt+\sqrt{2D}\,dB,\qquad\beta>0,\;D>0.
\]

The force on the memory is the drift divided by \(D\), at \(kT=1\). The Sekimoto heat, in the sign the scalar notes use, is

\[
\dot Q=\sum_k\frac{a_k v_k\gamma_k^2}{D(a_k+\beta)}.
\]

*Proof.* Exogeneity keeps \(\mathbb{E}[X_i X_j]=\delta_{ij}v_i\). The Lyapunov equation for \(c_i=\mathbb{E}[X_i M]\) is \((a_i+\beta)c_i=v_i\gamma_i\). The equation for \(C_{MM}\) is \(\beta C_{MM}=\sum_i\gamma_i c_i+D\). The drift is \(f=-\beta M+\gamma\cdot X\), so

\[
\mathbb{E}[f^2]=\beta D+\sum_i\frac{a_i v_i\gamma_i^2}{a_i+\beta}.
\]

Then \(\mathbb{E}[f^2]/D-\beta\) is the display. Forty random designs, \(K\) from 1 to 4, match this expression with relative residual \(4.5\times 10^{-15}\). ∎

**Proposition G-gap (PROVED (in-model)).** On this family \(\dot Q\ge L\). With \(q_k=a_k v_k\gamma_k^2/(a_k+\beta)^2\) and \(N=\sum_k q_k\),

\[
\dot Q-L=\frac{1}{D}\sum_k a_k q_k+\frac{\beta N^2}{D(D+N)}\ge 0.
\]

*Proof.* The conditional covariance of \(X\) given \(M\) is the rank-one downdate \(\Sigma-cc^\top/C_{MM}\). Its precision excess is rank one, and the Gaussian learning rate collapses to \(L=\beta N/(D+N)\). Subtracting from the closed form for \(\dot Q\) gives the display. Both terms are nonnegative. The same forty designs match the difference with relative residual \(1.3\times 10^{-14}\). At \((a,v,\beta,\gamma,D)=((1,4),(1,0.5),3,(2,-1),0.4)\) the heat is \(3.214285714286\), the learning rate is \(1.262924667651\), and the gap is \(1.951361046634\). ∎

**Proposition G-fast (PROVED (in-model)).** Fix a gain \(g\) and a noise level \(\sigma^2>0\). Set \(\beta=\lambda\), \(\gamma=\lambda g\), and \(D=\lambda\sigma^2\). As \(\lambda\to\infty\),

\[
\dot Q\to\frac{1}{\sigma^2}\sum_k a_k v_k g_k^2,
\]

and the sum-error tends to the error of the static Gaussian channel that observes \(g\cdot X\) in noise of variance \(\sigma^2\),

\[
\varepsilon\to V-\frac{(\sum_k v_k g_k)^2}{\sigma^2+\sum_k v_k g_k^2},\qquad V=\sum_k v_k.
\]

The limiting heat equals the learning rate of that channel. At every finite \(\lambda\) the heat is finite.

*Proof.* Substitute \(\gamma_k=\lambda g_k\) and \(D=\lambda\sigma^2\) into the closed form. Each term is \(a_k v_k g_k^2\,\lambda/(\sigma^2(a_k+\lambda))\), which tends to \(a_k v_k g_k^2/\sigma^2\). The covariances \(c_k=v_k\lambda g_k/(a_k+\lambda)\) tend to \(v_k g_k\), and \(C_{MM}\) tends to \(\sigma^2+\sum v_k g_k^2\). The sum-error \(V-(\sum c_k)^2/C_{MM}\) tends to the static formula. A static Gaussian observation \(Y=g\cdot X+\xi\) has precision update \(gg^\top/\sigma^2\) and learning rate \(g^\top D_{\mathrm{diff}} g/\sigma^2\), which is the same limit. ∎

The path rate does not follow this limit down. On two fast shrunk springs, each at \(a=v=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), the scalar formula gives path rate \(999.503125\) apiece. The learning-rate floor of the pair is \(8\). The ratio of floor to path rate is \(0.004002\). Sensory capacity in that limit is the same small number as in the scalar note. Hartich's factor \(2\), and Sandberg's factor \(2\) on the transfer entropy, cover a state that keeps the path. They do not apply to this design.

## 5. Per-mode decisions

**Proposition G-trace (PROVED (in-model)).** Fix per-mode decision errors \(s_k\in(0,v_k]\). Over regular memories,

\[
\inf\dot Q=kT\sum_k R_k(s_k).
\]

The infimum equals \(kT\) times the steady Kalman–Bucy information rate of the product filter at those error variances. It is approached at finite heat by a product of shrunk springs, one per mode, each built as in the scalar note.

*Proof.* Proposition G-learn gives \(L\ge\sum R_k(s_k)\), hence \(\dot Q\ge kT L\) is at least the display wherever Horowitz and Esposito apply. On the product of scalar shrunk springs the baths are separate, the heats add, and each heat tends to \(kT R_k(s_k)\) by the scalar attainability theorem. The Kalman–Bucy identification is the Riccati trace in §3, applied to a block-diagonal observation. A joint conditional with the same marginal variances has \((S^{-1})_{kk}\ge 1/S_{kk}\), so its learning-rate bound is at least as large, and strictly larger when some off-diagonal entry of \(S\) is nonzero. At marginal variances \(0.3\) and \(0.4\), with \(D=\operatorname{diag}(1,2)\), the diagonal value of \(\operatorname{tr}(D S^{-1})\) is \(8.333333333333\). The same trace with off-diagonal entry \(0.1\) is \(9.090909090909\). That entry is a correlation coefficient of \(0.1/\sqrt{0.12}=0.288675134595\). At correlation coefficient \(0.1\), the covariance entry is \(0.034641016151\) and the trace is \(8.417508417508\). Both sit above the diagonal value. ∎

At \(\lambda=10^6\), a shrunk spring at \((a,v,\varepsilon)=(1,1,0.2)\) has heat \(4.000020\), and one at \((4,0.5,0.1)\) has heat \(16.000320\). The floors are \(4\) and \(16\).

**Proposition G-front-trace (PROVED).** Minimize \(\sum_k kT R_k(s_k)+w\sum_k s_k\) on \(s_k\in(0,v_k]\). The minimum separates. Mode \(k\) is blind, \(s_k=v_k\), heat \(0\), when \(w\le kT a_k/v_k\). Otherwise \(s_k=\sqrt{kT a_k v_k/w}\) and the mode contributes \(2\sqrt{kT a_k v_k w}-kT a_k\). Therefore

\[
J^\star_{\mathrm{trace}}(w)=\sum_k J_1(a_k,v_k,w),
\]

where \(J_1\) is the scalar frontier. The tracked set is \(\{k:w\ge kT a_k/v_k\}\).

*Proof.* The derivative of mode \(k\)'s cost in \(s_k\) is \(-kT a_k v_k/s_k^2+w\), and the second derivative is positive. The blind corner of that mode is admissible and has heat \(0\), by the equilibrium cancellation already in INFO_PHYSICS. Comparing it with the critical point gives the threshold. ∎

For rates \(a_k=a\rho^{k-1}\) and equal variances \(v\), with \(\rho>1\), the tracked count is

\[
K_{\mathrm{hard}}(w)=\#\{k:a\rho^{k-1}\le wv/(kT)\}.
\]

Once \(w\ge kT a/v\), and until the ladder runs out, the count is exactly

\[
\left\lfloor\frac{\log(wv/(kT a))}{\log\rho}\right\rfloor+1.
\]

It is \(0\) below the slowest threshold. Multiplying the stake by \(\rho\) adds one mode.

Three modes, \(a=(1,10,100)\), \(v=1\), \(kT=1\):

| Stake \(w\) | Tracked modes | Cost |
|---|---|---|
| 0.5 | none | 1.500000000000 |
| 2 | the slowest | 5.828427124746 |
| 20 | the two slowest | 46.228543157461 |
| 200 | all three | 289.569702822072 |

The ordering is by \(a_k/v_k\). A fast mode with the same variance is blind at a stake where a slow mode is tracked. That is the layer-count statement this loss supports: one memory coordinate per tracked mode, and none on a mode below its threshold.

## 6. The sum of the modes

The decision error is now \(\varepsilon=\mathbb{E}[(g(M)-Z)^2]=1^\top\bar S\,1\), with \(Z=\sum_k X_k\).

**Proposition G-sum (PROVED for the bound; the spring attains it).** The minimum of \(\operatorname{tr}(D(\bar S^{-1}-\Sigma^{-1}))\) over conditional covariances with \(1^\top\bar S\,1=\varepsilon\) and \(0\prec\bar S\preceq\Sigma\) is the unique \(\mu\ge 0\) such that

\[
\varepsilon=\sum_k\frac{a_k v_k}{a_k+\mu},
\]

and the minimum value is \(\mu\). The minimizing channel observes \(\sum_k g_k X_k\) with \(g_k=1/(a_k+\mu)\). A fast linear memory with that gain approaches heat \(kT\mu\) at that sum-error.

*Proof.* Write \(\Phi=\bar S^{-1}-\Sigma^{-1}\succeq 0\), so the objective is \(\operatorname{tr}(D\Phi)\). The derivative of \(1^\top\bar S\,1\) with respect to \(\Phi\) is \(-(S1)(S1)^\top\). Stationarity against a positive semidefinite increment requires \(D-\lambda uu^\top\succeq 0\) with \(u=S1\), and \(\Phi\) supported where equality holds. Cauchy–Schwarz in the \(D\) inner product puts the kernel of that pencil on the span of \(D^{-1}u\), at \(\lambda=1/(u^\top D^{-1}u)\). Thus \(\Phi\) is rank one. Solving \(S^{-1}u=1\) on every coordinate with \(g=D^{-1}u\) gives \(g_k=1/(a_k+\mu)\) for a single \(\mu\ge 0\). Set the observation noise to \(\sigma^2=\sum_k a_k v_k g_k^2/\mu\). Then \(1-\mu g_k=a_k g_k\), so

\[
\sum_k v_k g_k-\mu\sum_k v_k g_k^2=\sum_k a_k v_k g_k^2=\mu\sigma^2.
\]

The static sum-error is \(V-(\sum v_k g_k)^2/(\sigma^2+\sum v_k g_k^2)\). The identity just written says the subtracted term equals \(\mu\sum v_k g_k\), and \(\sum v_k-\mu\sum v_k g_k=\sum a_k v_k/(a_k+\mu)\). The learning rate of the channel is \(\sum a_k v_k g_k^2/\sigma^2=\mu\). Dropping a mode replaces its contribution \(a_k v_k/(a_k+\mu)\) by the larger prior \(v_k\) at the same \(\mu\), which raises the error. Every mode stays in the channel for \(\mu>0\). Proposition G-fast, with this \(\sigma^2\), is the attaining spring. ∎

At \(a=(1,100)\), \(v=(1,1)\), and sum-error \(0.5\), \(\mu=103.887732673340\). The weighted spring at \(\lambda=10^6\) has heat \(103.877719\), learning rate \(103.856920\), and sum-error \(0.500077\). Separate memories at the same sum-error have heat \(141\), ratio \(1.357234\), at per-mode errors \(0.045455\) and \(0.454545\).

**Identical modes (PROVED).** If every \(a_k=a\) and every \(v_k=v\), then \(Z\) is the scalar equilibrium Ornstein–Uhlenbeck signal of rate \(a\) and variance \(Kv\). The sum-loss floor is the scalar floor \(kT\,a(Kv-\varepsilon)/\varepsilon\). Separate memories, each held to error \(\varepsilon/K\), have total heat exactly \(K\) times that floor, for every \(\varepsilon\in(0,Kv)\).

*Proof.* The sum of the stochastic differentials is \(dZ=-a Z\,dt+\sqrt{2a\cdot Kv}\,dW\). The scalar theorem applies to \(Z\). Separate errors are uncorrelated, so the sum-error is \(\sum s_k\). The symmetric point \(s_k=\varepsilon/K\) is feasible, since \(\varepsilon/K\le v\), and its heat is \(K a(Kv/\varepsilon-1)=K\cdot a(Kv-\varepsilon)/\varepsilon\). The checks record the identity at \((K,\varepsilon)=(2,0.8)\), \((3,1.1)\), and \((4,0.5)\): joints \(1.5\), \(1.727272727273\), \(7\), and separate heats \(3\), \(5.181818181818\), \(28\). ∎

Equal rates and unequal variances still make \(Z\) one Ornstein–Uhlenbeck signal, so the joint floor is still the scalar floor. Separate heat is then strictly larger for \(K>1\), but the factor is no longer \(K\). At rates \((1,1)\), variances \((1,4)\), and sum-error \(2\), the joint floor is \(1.5\) and the separate heat is \(2.5\), at errors \(0.666667\) and \(1.333333\).

**Proposition G-front-sum (PROVED).** Minimize \(kT\mu+w\sum_k a_k v_k/(a_k+\mu)\) on \(\mu\ge 0\). The derivative at \(\mu=0\) is \(kT-w\sum_k v_k/a_k\). When \(w\le w_0\) with

\[
w_0=\frac{kT}{\sum_k v_k/a_k},
\]

the minimum is the blind cost \(w\sum_k v_k\), and \(\mu=0\). Above \(w_0\), \(\mu\) solves

\[
\sum_k\frac{a_k v_k}{(a_k+\mu)^2}=\frac{kT}{w},
\]

and \(J^\star_{\mathrm{sum}}(w)=kT\mu+w\,\varepsilon(\mu)\). For \(K\) identical modes this is the scalar frontier of the summed signal,

\[
J^\star_{\mathrm{sum}}(w)=wv_{\mathrm{tot}}\quad(w\le kT a/(Kv)),\qquad 2\sqrt{kT\,a\,Kv\,w}-kT a\quad(w\ge kT a/(Kv)).
\]

*Proof.* The second derivative \(2w\sum a_k v_k/(a_k+\mu)^3\) is positive. The sign of the first derivative at \(0\) is the blind test. The identical reduction is the scalar frontier applied to variance \(Kv\). ∎

At \(K=3\), \(a=v=kT=1\), \(w_0=1/3\):

| Stake \(w\) | \(\mu\) | Sum-error | Joint cost | Separate cost |
|---|---|---|---|---|
| 0.2 | 0 | 3 | 0.600000000000 | 0.600000000000 |
| 0.5 | 0.224744871392 | 2.449489742783 | 1.449489742783 | 1.500000000000 |
| 2 | 1.449489742783 | 1.224744871392 | 3.898979485566 | 5.485281374239 |
| 8 | 3.898979485566 | 0.612372435696 | 8.797958971133 | 13.970562748477 |

The separate column is the per-mode frontier used on the sum-error, which is blind for each mode while \(w<kT a/v=1\). On the interval between \(w_0=kT a/(Kv)\) and \(kT a/v\), the joint memory tracks and the separate memories are blind. Above \(kT a/v\), both track, and the separate cost is larger. As \(w\to\infty\) the ratio of those optimized costs tends to \(\sqrt{K}\), because the leading terms are \(2K\sqrt{kT a v w}\) and \(2\sqrt{K}\,\sqrt{kT a v w}\). The heat ratio at a matched error stays \(K\), which is the sharper comparison. The optimized costs differ by less than \(K\) because the two designs sit at different errors.

One coordinate implements the sum-loss floor. Extra coordinates do not lower the learning-rate bound, because the minimizing \(\Phi\) is rank one. They can meet it. They cannot beat it.

**What "blind" means on this loss.** For \(\mu>0\) every gain \(g_k=1/(a_k+\mu)\) is positive. The contribution of mode \(k\) to the sum-error is \(a_k v_k/(a_k+\mu)=v_k\big(1-\varphi_k\big)\) with \(\varphi_k=\mu/(a_k+\mu)\). A mode with \(a_k\gg\mu\) has \(\varphi_k\) near \(0\): its prior variance remains in the sum. The count of modes with \(\varphi_k\ge 1/2\) is \(\#\{k:a_k\le\mu(w)\}\).

**Proposition G-scale (PROVED, for an infinite ladder).** Let \(a_k=a\rho^k\) for \(k\in\mathbb{Z}\), \(\rho>1\), and \(v_k=v\). The sum that defines the stake at a given \(\mu\) converges. If \(w(\mu)\) is that stake, then \(w(\rho\mu)=\rho\,w(\mu)\). Raising the stake by a factor \(\rho\) moves \(\mu\) by a factor \(\rho\) and adds exactly one mode to \(\{k:a_k\le\mu\}\).

*Proof.* The general term at \((\mu,k)\) and the term at \((\rho\mu,\,k+1)\) differ by the factor \(1/\rho\). The whole sum scales by \(1/\rho\), so the stake, which is proportional to the reciprocal of the sum, scales by \(\rho\). The set \(\{a_k\le\mu\}\) gains the single index that crosses the new level. On the truncated ladder \(k\in[-30,30]\), \(\rho=10\), \(\mu=50\), the computed ratio is \(10.000000000000\). ∎

A finite ladder has a blind threshold \(w_0>0\), because \(\sum v_k/a_k\) is finite, and it has edge effects when \(\mu\) sits near the slowest or the fastest rate. The bulk of a long ladder is the infinite scaling. Four modes at rates \(1,10,100,1000\), equal variance, \(kT=1\), \(w_0=1000/1111=0.900090009001\):

| Stake \(w\) | \(\mu\) | Half-tracked count | Hard per-mode count |
|---|---|---|---|
| 0.5 | 0 | 0 | 0 |
| 2 | 0.5815 | 0 | 1 |
| 8 | 3.1851 | 1 | 1 |
| 40 | 17.0512 | 2 | 2 |
| 200 | 85.2445 | 2 | 3 |
| 2000 | 729.2619 | 3 | 4 |

The half-tracked count lags the hard count by at most one on this grid. Both increase as \(\log_{10} w\). They are not the same integer at every stake. The hard count is the per-mode loss of §5. The half-tracked count is a reading of the sum loss, on which no mode is exactly blind.

A memory that can see only the unweighted sum, \(g_k\) all equal, is a narrower channel. It is optimal when the rates are equal, because then \(g_k=1/(a+\mu)\) is constant and \(Z\) is the right scalar signal. When the rates differ, the optimal gain is larger on the slower mode, and the unweighted sum is a different design. The floor in this section is the mode-resolved gain.

## 7. Where this meets the layer-count rule

N65, in `measurement/LAYER_COUNT_RULE.md`, is the operational rule for T15. The observation side counts distinct in-band memory time constants by degree. The prediction side sets \(K^\star\) equal to the leftmost minimizer of \(K+R(1+\varepsilon_K)\), with stake ratio \(R=w E_\infty/h\). When the decrements of \(\varepsilon_K\) are non-increasing, that minimizer is the from-0 count \(K^\star_0(R)=\#\{K\ge 1:R(\varepsilon_{K-1}-\varepsilon_K)>1\}\) (N64, Fox 1966). Otherwise the prediction uses the lower convex hull. N60 is the same count under a convexity premise, with the \(K^\star=0\) hole of the from-1 formula left on the record. A closed form in the poles and the stake alone, without the curve \(\varepsilon_K\), is T18, and it remains open. The constant \(h\) is an input of that rule.

The heat-floor counts of §5 and §6 do not use \(h\).

They agree on four points.

- There is a blind regime. Below a stake threshold the heat-optimal design holds no information about the signal, and the cost is \(w\) times the prior variance. N65's minimizer is \(K^\star=0\) when no decrement pays for one unit of \(R\).
- The count is nondecreasing in the stake. Raising \(w\), or raising \(R\) at fixed \(h\) and \(E_\infty\), cannot drop a mode that already paid, and cannot drop a layer whose decrement still clears \(1/R\).
- The count is at most the number of separated real modes of this world, for a per-mode memory on the per-mode loss. That is the same ceiling shape as L2's \(K^\star\le J\) at the full optimum, which is a statement about degree in the linear-Gaussian class and is not re-proved here.
- Slow content comes first when variances are equal. On the per-mode loss the threshold is exactly \(kT a_k/v_k\), so the smallest rate is tracked at the smallest stake. N64's from-0 count, when the decrements are the per-mode variance shares and they are ordered that way, has the same qualitative order. The repository already records that the joint decrements of a \(K\)-store filter of one scalar are not the isolated modal variances (`core/keystone_checks/waterfill_2026-11-20/MATH.md`, the recorded failure of the isolated rule). This note does not replace those decrements by \(a_k/v_k\).

They differ on four points.

- The price of a tracked mode here is the heat \(kT a_k(v_k-s_k)/s_k\), which is zero at \(s_k=v_k\) and whose derivative there is \(kT a_k/v_k\). N65 prices the \(K\)-th degree at \(h\), whatever the rate of the pole. A fast mode and a slow mode of equal variance have different heat thresholds and the same \(h\).
- The timescale ratio enters the per-mode count as \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) once the slowest mode pays. It enters N65 only by shaping the measured curve \(\varepsilon_K\). There is no formula in N65 that multiplies the stake by \(\rho\) and adds one layer, and T18 says no such shortcut is on the books.
- On the sum loss the heat-optimal memory has one coordinate at every stake above \(w_0\). Its degree does not grow with \(w\). The half-tracked mode count does. N65's \(K^\star\) is a degree, and for a store library on one scalar observation that degree grows with \(R\), up to the degree of the world. Those are different design sets: a mode-resolved gain \(g_k=1/(a_k+\mu)\) on the vector, against a degree-\(K\) filter of the single series \(Z\).
- When the rates are identical, \(Z\) is one mode. The heat floor is one spring. A degree count of \(Z\) is \(0\) or \(1\). Separate per-mode memories use \(K\) coordinates and \(K\) times the heat, which neither the heat floor nor the degree of \(Z\) selects.

Kolmogorov's reverse water-filling and Sims's mutual-information price are the \(\tfrac12\log\) allocation. Gorbunov and Pinsker (1973, 1974) and Stavrou, Charalambous, Charalambous, Loyka, and Skoglund (2018) are the nonanticipative rate of that same shape, a \(\tfrac12\log\) reverse water-fill on the eigenvalues of a prediction-error covariance. Tanaka, Kim, Parrilo, and Mitter (2017) is the discrete-time sequential rate-distortion program in directed information. Tanaka, Skoglund, and Ugrinovskii (2017) minimize the Duncan mutual-information rate of a continuous-time vector Gauss–Markov source under the trace constraint \(\operatorname{tr}(P)\le D\). That minimum is a semidefinite program. Their constraint is the sum of the marginal mean squares. It is not \(1^\top P 1\), and the paper contains no bath heat. The allocation in §5 minimizes \(\sum a_k(v_k-s_k)/s_k\), and the sum-loss allocation in §6 is the single level \(\mu\). Those functionals agree with \(\tfrac12\log\) only at isolated errors. The repository's water-filling note already says that a price per nat and a constant \(h\) per state are different regularizers, and that a count of frequency peaks of \(S(\omega)\) is the wrong object for a sum of Ornstein–Uhlenbeck spectra, which are unimodal at \(\omega=0\). Nothing here revises that. The mode count in §5 is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\) on a geometric ladder of equal variances, once the slowest mode pays. It is a count of rates below \(wv/(kT)\), not a count of peaks of \(S(\omega)\).

## 8. What survives past this class

**A non-Gaussian conditional of an equilibrium Ornstein–Uhlenbeck signal.** The quartic conditional in the attainability note has a learning rate strictly above \(R\) of its error. The heat infimum remains \(kT\) times the Gaussian rate, because the shrunk springs attain it and G-learn puts every regular memory at or above it. The attainability note does not leave a separate open row for the heat of a nonlinear potential.

**The telegraph.** INFO_PHYSICS §4 already proves the floor \(kT\,\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) and the attainment in the fast-affinity limit. That floor is not \(R(\varepsilon)\). Separate telegraphs add their heats, which is the separate-bath bookkeeping already there. Whether one joint jump memory of a sum of telegraphs beats \(K\) separate telegraphs by a factor \(K\), the way identical Ornstein–Uhlenbeck modes do, is **OPEN**. The factor \(K\) used the linear structure of \(Z\).

**A driven signal.** The case in which the signal's own bath pays is already recorded, in SE3 and in the Barato–Hartich–Seifert receptor. This page does not add a new counterexample. A general rule for which bath pays is **OPEN**.

**A coupled equilibrium diffusion that is not a product of scalar modes.** The learning-rate bound \(\operatorname{tr}(D(\bar S^{-1}-\Sigma^{-1}))\) is Proposition G-learn, and the signal bath still cancels. **NUMERICAL.** One coupled pair, covariance \(\Sigma=\bigl(\begin{smallmatrix}1&0.3\\0.3&1\end{smallmatrix}\bigr)\) and diffusion \(D=\bigl(\begin{smallmatrix}0.8&0.1\\0.1&1.2\end{smallmatrix}\bigr)\), with a fast spring of rate \(10^5\) and noise level \(0.25\) on each coordinate, has heat \(7.999913\) and learning rate \(7.999490\), against the static value \(8\). That is one design approaching its own static rate. It is not a proof that every error covariance of a coupled diffusion is attainable at finite heat.

**A non-quadratic loss, and a memory that changes \(X\).** Open, on the same grounds as the scalar note.

## 9. What this note adds

The memory-bath inequality \(\dot Q\ge kT L\) is Horowitz and Esposito. The scalar floor and the shrunk spring are the attainability note. Duncan is the path rate. The Kalman–Bucy filter is Kalman and Bucy. Kolmogorov and Sims, Gorbunov and Pinsker, and Stavrou, Charalambous, Charalambous, Loyka, and Skoglund minimize a \(\tfrac12\log\) rate. Tanaka, Kim, Parrilo, and Mitter are the discrete-time sequential program in directed information. Tanaka, Skoglund, and Ugrinovskii are the continuous-time vector Duncan minimization under a trace constraint, with no bath heat. Fox is the marginal count already cited for N64. None of those is redone.

What this note adds:

- For independent equilibrium OU modes, the learning-rate lower bound of one joint memory at per-mode decision errors \(s_k\) is the sum of the scalar Kalman rates, and an off-diagonal error covariance raises it. The product of fast shrunk springs approaches the sum at finite heat. The heats \(4.000020\) and \(16.000320\) are the scalar construction, repeated.
- The per-mode frontier is the sum of the scalar frontiers. The threshold is \(kT a_k/v_k\). On a geometric ladder the tracked count is \(\lfloor\log(wv/(kT a))/\log\rho\rfloor+1\).
- Under the sum loss, the minimum of the covariance bound is the unique \(\mu\) with \(\varepsilon=\sum a_k v_k/(a_k+\mu)\), the minimizing channel has gains \(g_k=1/(a_k+\mu)\) and rank one, and one fast memory approaches heat \(kT\mu\). For \(K\) identical modes the sum is one OU and \(K\) separate memories cost \(K\) times that heat at every matched error. At rates \((1,100)\) and sum-error \(0.5\) the separate heat is \(141\) and \(\mu=103.887732673340\). On the infinite equal-variance ladder, multiplying the stake by \(\rho\) adds one half-tracked mode.
- The comparison in §7. N65 and L2 count degree under a constant \(h\), on a filter of the scalar series. This floor has no \(h\). On the sum loss, inside the mode-resolved design, the heat-optimal degree is \(1\). The note does not change N65.
- The coupled numerical design, heat \(7.999913\) against its static rate \(8\).

**Proved on this page.** G-learn, G-signal, the heat formula, G-gap, G-fast, G-trace, G-front-trace, G-sum, the identical-mode factor \(K\), G-front-sum, and G-scale.

**Numerical.** Forty designs, relative residuals \(4.5\times 10^{-15}\) and \(1.3\times 10^{-14}\). The weighted spring at sum-error \(0.5\): heat \(103.877719\) against \(\mu=103.887733\). Separate heat \(141\), ratio \(1.357234\). The coupled spring, heat \(7.999913\). The weighted spring at \(\lambda=500\), path rate \(14.831794\) against learning rate \(1.972390\). The finite ladder in the table of §6.

**Open.**

- A joint jump memory of several telegraphs, against \(K\) separate telegraph floors.
- A general rule for which bath pays. The case in which the signal's own bath pays is already recorded, in SE3 and in the Barato–Hartich–Seifert receptor. This page does not add a counterexample.
- Attainment for every error covariance of a coupled equilibrium diffusion. One numerical design approaches its static rate.
- A loss that is not a mean square of an action of the current state.
- A memory that changes \(X\).
- Whether a degree-\(K\) filter of the scalar series \(Z\) alone, with no mode-resolved gain, can meet the sum-loss floor when the rates differ. The floor in §6 uses the mode-resolved gain. The unweighted sum is optimal when the rates are equal, because then \(Z\) is one Ornstein–Uhlenbeck signal.
- Ruin, linking, the stake \(w\), and H3. The master equation remains the equation in THEORY.

## 10. Checks

`theory/info_physics_checks/general_checks.py`. 33 checks, FAILS 0. The numbers in §§4–8 are the numbers it prints.

## 11. References

Kalman, R. E., and Bucy, R. S. 1961. New results in linear filtering and prediction theory. *J. Basic Eng.* 83:95. doi 10.1115/1.3658902.

Duncan, T. E. 1970. On the calculation of mutual information. *SIAM J. Appl. Math.* 19:215. doi 10.1137/0119020.

Kolmogorov, A. N. 1956. On the Shannon theory of information transmission in the case of continuous signals. *IRE Trans. Inf. Theory* 2:102. doi 10.1109/TIT.1956.1056823.

Fox, B. 1966. Discrete optimization via marginal analysis. *Manage. Sci.* 13:210. doi 10.1287/mnsc.13.3.210.

Tatikonda, S., Sahai, A., and Mitter, S. 2004. Stochastic linear control over a communication channel. *IEEE Trans. Automat. Control* 49:1549. doi 10.1109/TAC.2004.834430.

Sims, C. A. 2003. Implications of rational inattention. *J. Monet. Econ.* 50:665. doi 10.1016/S0304-3932(03)00029-1.

Mitter, S. K., and Newton, N. J. 2005. Information and entropy flow in the Kalman–Bucy filter. *J. Stat. Phys.* 118:145. doi 10.1007/s10955-004-8781-9.

Horowitz, J. M., and Esposito, M. 2014. Thermodynamics with continuous information flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.

Horowitz, J. M., and Sandberg, H. 2014. Second-law-like inequalities with information and their interpretations. *New J. Phys.* 16:125007. doi 10.1088/1367-2630/16/12/125007.

Barato, A. C., Hartich, D., and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.

Sandberg, H., Delvenne, J.-C., Newton, N. J., and Mitter, S. K. 2014. Maximum work extraction and implementation costs for nonequilibrium Maxwell's demons. *Phys. Rev. E* 90:042119. doi 10.1103/PhysRevE.90.042119.

Hartich, D., Barato, A. C., and Seifert, U. 2016. Sensory capacity: an information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116.

Tanaka, T., Kim, K. K. K., Parrilo, P. A., and Mitter, S. K. 2017. Semidefinite programming approach to Gaussian sequential rate-distortion trade-offs. *IEEE Trans. Automat. Control* 62:1896. doi 10.1109/TAC.2016.2601148.

Tanaka, T., Skoglund, M., and Ugrinovskii, V. 2017. Optimal sensor design and zero-delay source coding for continuous-time vector Gauss–Markov processes. *56th IEEE Conference on Decision and Control*, pp. 3992–3997. doi 10.1109/CDC.2017.8264246.

Gorbunov, A. K., and Pinsker, M. S. 1973. *Problems of Information Transmission* 9:184. Gorbunov, A. K., and Pinsker, M. S. 1974. *Problems of Information Transmission* 10:93. Crossref returned no work record for either translation on 22 November 2026. The volumes and pages are the ones cited by doi 10.1109/CDC.2018.8619725 and doi 10.1109/TIT.2021.3124888.

Stavrou, P. A., Charalambous, T., Charalambous, C. D., Loyka, S., and Skoglund, M. 2018. Asymptotic reverse-waterfilling characterization of the nonanticipative rate distortion function of vector-valued Gauss–Markov processes with MSE distortion. *57th IEEE Conference on Decision and Control*, pp. 14–20. doi 10.1109/CDC.2018.8619725.
