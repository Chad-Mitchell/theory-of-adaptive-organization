# The Kalman rate is a heat floor, and a linear spring attains it

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. No locked preregistration file is edited. Checks: `theory/info_physics_checks/attainability_checks.py`, run at `nice -n 19` (28 checks, FAILS 0). DOIs resolved on the Crossref API on 22 November 2026 are listed in `theory/info_physics_checks/attainability_crossref.out`.*

Labels: **PROVED** (a proof is on this page, under the assumptions named with it), **PROVED (in-model)** (the same, inside a stated model), **PRIOR ART** (published, credited, not claimed here), **NUMERICAL**, **OPEN**. A lower bound is not a derivation of the cost.

This note answers the question left open in `theory/INFO_PHYSICS.md` §8a and OPEN_WORK T37: whether \(kT\) times the optimal causal information rate is attainable at finite heat for a continuous signal. It does not replace the centered-spring statements in that note. Those statements are about one family, scored by the raw coordinate error.

## 0. The question, and the answer

The signal is the equilibrium Ornstein–Uhlenbeck process

\[
dX=-a X\,dt+\sqrt{2av}\,dW,
\]

variance \(v\), temperature of the memory bath \(T\). The error \(\varepsilon\in(0,v)\) is a mean squared error of an action that is a function of the current memory state. The Kalman–Bucy information rate at that error, in these units, is

\[
R(\varepsilon)=a\frac{v-\varepsilon}{\varepsilon}.
\]

Duncan's theorem identifies \(R(\varepsilon)\) as the mutual-information rate of the causal filter that holds error \(\varepsilon\). PD7 already books that rate. This note proves it is also the greatest lower bound on the learning rate of any regular memory of this signal, and that the memory-bath heat can meet \(kT\,R(\varepsilon)\) in a limit where the heat stays finite.

**Answer.** Over bipartite memories of this signal, the infimum of the memory-bath heat at fixed error \(\varepsilon\) is \(kT\,R(\varepsilon)\). A one-dimensional linear spring whose rest point is \(cX\), with \(c=1-\varepsilon/v\), approaches that infimum as its rate goes to infinity. At rate \(10^{6}\), error \(0.2\), \(a=v=kT=1\), the heat is \(4.000020\), against \(R=4\). The centered spring of INFO_PHYSICS, rest point \(X\), has heat floor \(kT\,av/\varepsilon\). At the same raw error that floor exceeds \(R(\varepsilon)\) by \(kT\,a\). The excess is the gap between \(R\) at the conditional error and \(R\) at the raw error. Continuity, a single degree of freedom, and causality do not force it.

Demanding sensory capacity \(1\), in the sense of Hartich, Barato, and Seifert, is a stronger requirement than the error. Their theorem then puts the heat at least twice the learning rate. The centered spring meets the factor \(2\) at their tuned noise. At conditional error \(0.2\) that design costs \(8\), and the floor for the error is \(4\).

The resulting frontier, ruin and linking left outside, is

\[
J_{\mathrm{phys}}^{\star}(w)=\min_{\varepsilon\in(0,v]}\left(kT\,a\frac{v-\varepsilon}{\varepsilon}+w\,\varepsilon\right).
\]

It equals \(wv\) when \(w\le kT a/v\), and \(2\sqrt{kT\,a\,v\,w}-kT a\) when \(w\ge kT a/v\). At \(a=v=kT=1\) and stake \(2\) this frontier tracks, cost \(2\sqrt{2}-1\). The centered-spring heat objective is blind at that stake, cost \(2\), because it minimizes a higher floor.

## 1. Scope

- **A-X.** \(X\) is exogenous. Its drift and diffusion do not depend on the memory. This is P-X of INFO_PHYSICS. A memory that moves its world is outside this note.
- **A-E.** The signal is the equilibrium OU above. Its own medium heat is zero (proved in §3). A driven signal, whose bath can pay, is the case SE3 and Barato, Hartich, and Seifert already separate, and is outside.
- **A-B.** The memory is a bipartite Markov process on the same probability space: a diffusion, a jump process, or a mixture, with one or more degrees of freedom, coupled to baths at temperature \(T\). The action is a function of the current memory state. The checks set \(kT=1\).
- **A-R.** Conditionals \(p(x\mid m)\) are positive smooth densities with finite Fisher information, so the integrations by parts in §3 apply. A hard bin of \(X\), whose conditional drops discontinuously at a finite edge, is outside A-R. Section 6 says what the soft \(K\)-state channel does instead.
- **A-L.** The loss is a mean square. A loss that does not fix a mean square is the vector-loss question INFO_PHYSICS left open, and it stays open.

## 2. What is already proved, or already published

Nothing in this list is claimed as new.

- **Horowitz and Esposito (2014)**, *Phys. Rev. X* 4:031015, doi 10.1103/PhysRevX.4.031015. In steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\). The shape \(\dot Q\ge kT\) times the learning rate is theirs. INFO_PHYSICS uses it for the telegraph and the centered spring.
- **Barato, Hartich, and Seifert (2014)**, *New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024. The learning rate is at most the entropy production of the learning subsystem. CT7 is the random-walk case, already in the repository: holding error \(D\) on a walk of variance rate \(\sigma^2\) dissipates at least \(kT\,\sigma^2/(2D)\). With \(q=2av\) held fixed and \(a\to 0\), \(R(\varepsilon)\to q/(2\varepsilon)\). The \(-a\) in \(R\) is the OU correction and vanishes in that limit. CT7 is not re-derived.
- **Hartich, Barato, and Seifert (2016)**, *Phys. Rev. E* 93:022116, doi 10.1103/PhysRevE.93.022116. Sensory capacity is the learning rate divided by the transfer-entropy rate, \(C=l/\mathcal T\in(0,1]\). If \(C=1\), their equations (63)–(64) give efficiency \(\eta=l/\sigma\le 1/2\), with equality available for a bare sensor. Their bare sensor, equation (47) without the memory coordinate, is the centered spring. Their equations (52), (53), and (54) are the learning rate, the transfer entropy, and the entropy production of that spring. This note recomputes those three from the Lyapunov equation and the Riccati, on and off their capacity-1 locus, and does not re-prove the tradeoff.
- **Horowitz and Sandberg (2014)**, *New J. Phys.* 16:125007, doi 10.1088/1367-2630/16/12/125007. Second-law inequalities with an information flow. Hartich, Barato, and Seifert attribute the linear-Langevin transfer entropy to this paper. The Riccati calculation in §5 reproduces the number Hartich, Barato, and Seifert print.
- **Duncan (1970)**, *SIAM J. Appl. Math.* 19:215, doi 10.1137/0119020, as booked in PD7 and `theory/INTERNAL_MODEL.md`. The information rate of the Kalman–Bucy filter at error \(\varepsilon\) is \(R(\varepsilon)\). This note does not re-prove Duncan, and it does not re-prove the Gaussian causal rate-distortion theorem. The heat bounds the learning rate. The identification of the minimum learning rate with \(R(\varepsilon)\) is the argument in §3.
- **Bo, Del Giudice, and Celani (2015)**, *J. Stat. Mech.* P01014, doi 10.1088/1742-5468/2015/01/P01014. Crossref lists the families as Bo, Giudice, and Celani. They bound the information a memory holds about the past of a sensory layer, beyond the present reading, by the extra entropy production of the whole device over the sensory layer. That extra is the gap \(C<1\) measures: the trajectory carries information the instantaneous state does not. They do not derive \(R(\varepsilon)\), the shrunk spring, or this frontier.
- **INFO_PHYSICS §8a**, centered spring. At fixed raw error \(\varepsilon<v\), the heat falls toward \(kT\,av/\varepsilon\) as the memory rate rises, and the information flow rises from \(R(\varepsilon)\) to the same value. The flow meets \(R(\varepsilon)\) where the heat diverges. Those sentences stand. They describe the spring whose rest point is \(X\), with the loss \(\mathbb{E}[(M-X)^2]\). Section 4 puts the same formulas next to the conditional error.

The telegraph equality, the stake table, and the proposal \(J_{\mathrm{phys}}=\dot Q+w\,\mathbb{E}[\ell]\) stay in INFO_PHYSICS. This note is the continuous-signal step that proposal named and left open.

## 3. The learning rate is at least the Kalman rate

**Proposition AT-learn (PROVED, under A-X, A-E, A-R).** Let the memory state \(M\) be anything on which the conditional densities \(p(x\mid m)\) exist and are regular in the sense A-R. In steady state the learning rate the memory must supply is

\[
L=a\big(v\,\mathbb{E}[F(X\mid M)]-1\big),
\]

where \(F(X\mid m)=\int(\partial_x\ln p(x\mid m))^2\,p(x\mid m)\,dx\) is the Fisher information of the conditional. Hence

\[
L\ge a\Big(\frac{v}{\varepsilon_{\mathrm{MMSE}}}-1\Big)=R(\varepsilon_{\mathrm{MMSE}}),
\]

with \(\varepsilon_{\mathrm{MMSE}}=\mathbb{E}[\mathrm{Var}(X\mid M)]\). Equality holds when every conditional is Gaussian and the conditional variance is almost surely constant. If an action \(g(M)\) has mean squared error \(\varepsilon\), then \(\varepsilon_{\mathrm{MMSE}}\le\varepsilon\), so \(L\ge R(\varepsilon)\). The same bound holds when the loss is the raw coordinate error \(\mathbb{E}[(M-X)^2]=\varepsilon\), because that error is the MMSE plus \(\mathbb{E}[(\mathbb{E}[X\mid M]-M)^2]\).

*Proof.* The signal is exogenous, so its marginal is the equilibrium Gaussian of variance \(v\), and its probability current is

\[
\frac{j_X}{p}=-ax-av\,\partial_x\ln p(x\mid m).
\]

The information flow carried by that current is the Horowitz–Esposito contraction

\[
\dot I_X=\Big\langle\frac{j_X}{p}\,\partial_x\ln\frac{p}{p_X p_M}\Big\rangle.
\]

The score of the equilibrium marginal is \(-x/v\), so the second factor is \(\partial_x\ln p(x\mid m)+x/v\). Write \(u=\partial_x\ln p(x\mid m)\). Then

\[
\dot I_X=\big\langle(-ax-av\,u)(u+x/v)\big\rangle=-2a\langle xu\rangle-(a/v)\langle x^2\rangle-av\,\mathbb{E}[u^2].
\]

For each regular conditional, \(\int x\,\partial_x p(x\mid m)\,dx=-1\), so \(\langle xu\rangle=-1\). Also \(\langle x^2\rangle=v\) and \(\mathbb{E}[u^2]=\mathbb{E}[F]\). Therefore \(\dot I_X=a-av\,\mathbb{E}[F]\). In steady state the learning rate is \(L=-\dot I_X\).

Fisher's inequality gives \(F(X\mid m)\ge 1/\mathrm{Var}(X\mid m)\), with equality exactly for a Gaussian. Jensen's inequality on \(1/s\), which is convex for \(s>0\), gives \(\mathbb{E}[1/\mathrm{Var}]\ge 1/\varepsilon_{\mathrm{MMSE}}\), with equality when the conditional variance is constant. The mean squared error of any action \(g(M)\) is at least \(\varepsilon_{\mathrm{MMSE}}\), with equality when \(g(M)=\mathbb{E}[X\mid M]\). \(R\) decreases in its argument on \((0,v]\). ∎

**Proposition AT-signal (PROVED, under A-X and A-E).** The medium heat of the signal bath is identically zero. The signal does not pay \(L\).

*Proof.* The equilibrium force is \(F_X=-X/v\), the mobility satisfies \(D_X=av\), and the drift is \(D_X F_X\). The Stratonovich power into the signal is \(D_X\mathbb{E}[F_X^2]+D_X\partial_X F_X\). The first term is \(av\cdot\mathbb{E}[X^2]/v^2=a\). The second is \(av\cdot(-1/v)=-a\). The sum is zero. The force does not depend on \(M\), which is A-X. ∎

Horowitz and Esposito then put the memory-bath heat at least at \(kT\,L\), hence at least at \(kT\,R(\varepsilon)\), for every bipartite memory whose entropy flow is the one their theorem bounds. That implication is theirs. The linear family in §4 does not rely on it: the Sekimoto heat is computed directly and shown to lie above \(L\).

## 4. One linear degree of freedom meets the floor

**Model (PROVED (in-model) for the formulas in this section).** 

\[
dM=(-\beta M+\gamma X)\,dt+\sqrt{2D}\,dB,\qquad \beta>0,\; D>0.
\]

The centered spring is \(\beta=\gamma=\lambda\). The force on the memory is the drift divided by \(D\), at \(kT=1\). The Sekimoto heat into the memory bath, in the sign INFO_PHYSICS uses, is

\[
\dot Q=\frac{\mathbb{E}[f^2]}{D}+\partial_M f=\frac{av\gamma^2}{D(a+\beta)},
\]

where \(f=-\beta M+\gamma X\). The stationary moments are \(C_{XM}=\gamma v/(a+\beta)\) and \(C_{MM}=D/\beta+\gamma^2 v/(\beta(a+\beta))\). The conditional variance is \(s=\det/C_{MM}\), with \(\det=v C_{MM}-C_{XM}^2\), and the learning rate of this Gaussian joint is \(L=a(v/s-1)=a C_{XM}^2/\det\).

**Proposition AT-gap (PROVED (in-model)).** On this family

\[
\dot Q-L=\frac{a^2\gamma^2 v\big(D(a+\beta)+\gamma^2 v\big)}{D(a+\beta)\big(D(a+\beta)^2+a\gamma^2 v\big)}\ge 0.
\]

The numerator and the denominator are positive. Forty random parameter points match this expression with relative residual \(1.7\times 10^{-15}\).

**Proposition AT-attain (PROVED (in-model)).** Fix \(\varepsilon\in(0,v)\) and set \(c=(v-\varepsilon)/v\). For every memory rate \(\lambda>av/\varepsilon\), the choice

\[
\beta=\lambda,\qquad \gamma=c\lambda,\qquad D=\lambda\sigma^2,
\]

\[
\rho=\frac{\lambda}{a+\lambda},\qquad \sigma^2=(v-\varepsilon)\Big(\rho\frac{v+\varepsilon}{v}-1\Big)
\]

has raw error \(\mathbb{E}[(M-X)^2]=\varepsilon\) and heat

\[
\dot Q=a(v-\varepsilon)\,\frac{\rho}{\rho(v+\varepsilon)-v}.
\]

The ratio to the Kalman rate is

\[
\frac{\dot Q}{kT\,R(\varepsilon)}=\frac{\rho\,\varepsilon}{\rho(v+\varepsilon)-v}>1,
\]

and the ratio tends to \(1\) as \(\lambda\to\infty\). The conditional variance tends to \(\varepsilon\) along the same limit, so the coordinate is calibrated: \(M\) and \(\mathbb{E}[X\mid M]\) meet. The heat at every finite \(\lambda\) in the range is finite.

*Proof of the limit.* Substitute the moments of §4. The algebra gives the displayed heat and the exact raw error \(\varepsilon\). Since \(\rho<1\), the denominator \(\rho(v+\varepsilon)-v=\rho\varepsilon-v(1-\rho)\) is smaller than \(\rho\varepsilon\), so the ratio exceeds \(1\). As \(\rho\to 1\) the denominator tends to \(\varepsilon\) and the heat tends to \(a(v-\varepsilon)/\varepsilon\). Positivity of \(\sigma^2\) is \(\rho>v/(v+\varepsilon)\), which is \(\lambda>av/\varepsilon\). ∎

At \(a=v=1\), \(\varepsilon=0.2\), \(R=4\), the ratio is exactly \(6\) at \(\lambda=6\), \(4/3\) at \(\lambda=20\), \(20/19\) at \(\lambda=100\), \(200/199\) at \(\lambda=10^3\), \(2000/1999\) at \(\lambda=10^4\), and \(200000/199999=1.000005000025\) at \(\lambda=10^6\). The conditional variance at \(\lambda=10^6\) is \(0.199999999999\). The infimum over this family is therefore \(R(\varepsilon)\), approached at finite heat, and Proposition AT-learn says no regular memory has a learning rate below \(R(\varepsilon)\). Inside the linear family the Sekimoto heat cannot go below the learning rate, so the infimum of the heat is the Kalman rate.

**The centered spring, scored two ways (PROVED (in-model)).** Keep \(\beta=\gamma=\lambda\) and \(D=\lambda(\varepsilon-av/(a+\lambda))\), which holds the raw error at \(\varepsilon\) for \(\lambda>a(v/\varepsilon-1)\). As \(\lambda\to\infty\) the heat tends to \(av/\varepsilon\), the conditional variance tends to \(s=v\varepsilon/(v+\varepsilon)\), and the learning rate tends to \(R(s)=av/\varepsilon\). The heat meets the learning rate of the error the coordinate actually supports. The difference from the Kalman rate of the raw error is

\[
\frac{av}{\varepsilon}-a\frac{v-\varepsilon}{\varepsilon}=a,
\]

which is \(kT\,a\) with the temperature restored. At \(a=v=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), the raw error is \(0.20000000\), the heat is \(5.00002000\), the conditional variance is \(0.16666694\), and the heat exceeds \(R(0.2)=4\) by \(1.00002000\).

The constant \(kT\,a\) is that difference. It is the excess of charging \(R\) at \(\mathbb{E}[(M-X)^2]\) when the conditional error is the smaller number \(s\). The fast centered spring is thermodynamically tight against \(R(s)\). Shrinking the readout to \(\mathbb{E}[X\mid M]\), or moving the rest point to \(cX\) as above, spends the same physical heat on the error \(R\) prices. The centered family with an unshrunk coordinate does not.

## 5. Causality, sensory capacity, and the factor two

The path of \(M\) can carry more information about \(X_t\) than the value \(M_t\). The transfer-entropy rate of the linear memory is the Duncan rate of estimating \(X\) from that path. The scalar Riccati for the path error \(P\) is \(\gamma^2 P^2=4aD(v-P)\), and

\[
\mathcal T=a\frac{v-P}{P}=\frac{\gamma^2 P}{4D}.
\]

The two expressions agree to \(10^{-9}\) relative on the forty random designs of §4. Because \(R\) decreases in the error and the path error cannot exceed the error given \(M_t\) alone, \(\mathcal T\ge L\), with equality when \(P=s\). Sensory capacity in the sense of Hartich, Barato, and Seifert is \(C=L/\mathcal T\).

On the centered spring their closed forms reproduce this calculation. With \(\nu=\lambda/a\) and \(B=D/(av)\),

\[
L=a\frac{\nu^3}{\nu^2+B(1+\nu)^2},\qquad
\dot Q=a\frac{\nu^2}{B(1+\nu)},\qquad
\mathcal T=\frac a2\Big(\sqrt{1+\frac{\nu^2}{B}}-1\Big).
\]

Checked to \(10^{-9}\) at the capacity-1 noises \(B=\nu^2/(\nu^2-1)\) for \(\nu=2,4,10\), and off that locus at \((\nu,B)=(10,0.3)\), \((3,1.5)\), \((20,2)\), and \((1.5,0.4)\). At \(B=\nu^2/(\nu^2-1)\) one has \(P=s\), \(C=1\), and \(\dot Q=2L\). For \(\nu=9\), \(a=v=1\), the conditional error is \(0.2\) and the heat is \(8\), which is \(2R(0.2)\).

The factor \(2\) is their tradeoff, attained by this sensor: a state that carries the whole trajectory pays at least twice the learning rate, and this parameter choice pays exactly twice. It is a real excess, and it sits above the error floor. At conditional error \(0.2\) the capacity-1 design costs \(8\) and the shrunk spring approaches \(4\).

The error constraint does not ask for \(C=1\). The action reads the current state. Information that is only in the path, and not in the state, is not available to the action. The fast shrunk spring delivers conditional error \(\varepsilon\) at heat approaching \(kT\,R(\varepsilon)\), with \(C<1\): the path is the more informed object, and the state is the object the loss scores. Bo, Del Giudice, and Celani bound that unused past information by extra entropy production. Raising \(C\) to \(1\) is where the factor \(2\) enters. Leaving \(C\) below \(1\) is how the heat stays at one times \(R(\varepsilon)\).

Causality in the sense "the action is a causal function of the memory" is already the hypothesis A-B, and the floor \(kT\,R(\varepsilon)\) includes it. Causality in the stronger sense "the state is a sufficient statistic of its own path" is the capacity-1 constraint, and it prices a second copy of the learning rate. The gap \(kT\,a\) is neither of those. It is the raw-versus-conditional gap of the centered spring.

## 6. Other implementations

**Nonlinear potentials.** Proposition AT-learn is strict unless the conditional is Gaussian with constant variance. A fast equilibrium in a non-quadratic potential has a non-Gaussian conditional, so its learning rate lies above \(R\) of its own MMSE, and the Horowitz–Esposito inequality puts the heat at least there. **NUMERICAL.** A fast equilibrium in \(V=(m-x)^4/(4\,w^4)\) at \(w=0.45\), \(v=1\), on the grid in the checks, has MMSE \(0.120383\), Fisher information \(11.019370\), and \(1/\mathrm{MMSE}=8.306810\). The learning rate is \(10.019370\), against the Kalman rate \(7.306810\) of that error. The check locks the sign of the excess, not these digits as a closed form.

**Several degrees of freedom.** The Fisher bound uses the conditional of \(X\) given the whole memory state. Extra coordinates can lower the conditional variance, which raises \(R\), or they can sit at equilibrium and add nothing. They do not open a heat below \(kT\,R(\varepsilon)\). **NUMERICAL.** Embedding the shrunk spring at \(\lambda=10^4\), \(\varepsilon=0.2\), next to an equilibrium second coordinate, gives total heat \(4.00200100\), equal to the one-coordinate heat. Thirty other stable two-memory linear systems, drawn from the box in the checks, all sit above their own learning rate. The closest heat in that draw is \(1.615570\) times the Kalman rate of its conditional error. The draw is not a minimization. The minimizing design is the one coordinate of §4.

**A \(K\)-state channel.** **NUMERICAL.** Quantize the Gaussian channel \(Y=X+\sigma\xi\), which has MMSE \(v\sigma^2/(\sigma^2+v)\), into \(K\) equal-probability bins. The bin index is a \(K\)-state memory. In the fast-equilibrium limit the heat equals the learning rate of the posterior of \(X\) given the bin. For the parent channel with \(\sigma=1/2\) and \(v=1\), whose own MMSE is \(0.2\) and whose Kalman rate is \(4\):

| \(K\) | MMSE | learning rate | \(R(\mathrm{MMSE})\) | ratio |
|---|---|---|---|---|
| 2 | 0.490704 | 1.260226 | 1.037888 | 1.214222 |
| 4 | 0.311557 | 2.553460 | 2.209689 | 1.155575 |
| 8 | 0.243971 | 3.340692 | 3.098849 | 1.078043 |
| 16 | 0.217779 | 3.712237 | 3.591804 | 1.033530 |
| 32 | 0.207370 | 3.874749 | 3.822309 | 1.013719 |
| 64 | 0.203125 | 3.944925 | 3.923079 | 1.005569 |

Retuning \(\sigma\) so the bin index has MMSE \(0.2\), the fast-limit heat is \(4.471064\) at \(K=8\), \(4.157870\) at \(K=16\), \(4.058746\) at \(K=32\), and \(4.022937\) at \(K=64\), against \(R(0.2)=4\). The ratio falls with \(K\). The heat stays finite. A hard partition, with a conditional that vanishes outside a bin and jumps at the edge, is outside A-R: the Fisher integral of a discontinuous density is not the finite integral used in §3, and a bipartite process cannot keep \(M\) a deterministic function of \(X\) at finite rates. The soft bins are the discretization that approaches the floor.

**Non-equilibrium cycles and feedback onto the memory.** A futile cycle adds a nonnegative term to the entropy production. The telegraph ray in INFO_PHYSICS §4 is that term at fixed error: the heat rises with the excess affinity and the error does not. Feedback of \(X\) into the memory drift is already allowed. The learning rate in §3 depends on the conditional law of \(X\), not on the form of the memory drift. A drive that changes \(X\) leaves A-X, and then Proposition AT-signal need not hold.

## 7. The frontier

Minimize \(kT\,R(\varepsilon)+w\varepsilon\) on \(\varepsilon\in(0,v]\). The derivative \(-kT\,av/\varepsilon^2+w\) vanishes at

\[
\varepsilon^{\star}=\sqrt{\frac{kT\,av}{w}},
\]

which lies in \((0,v]\) when \(w\ge kT a/v\). The second derivative \(2kT\,av/\varepsilon^3\) is positive there. The minimum value is \(2\sqrt{kT\,a\,v\,w}-kT a\). When \(w\le kT a/v\) the derivative is negative on the whole interval, the minimum is at \(\varepsilon=v\), the heat is \(0\), and the cost is \(wv\). The blind memory, force \(-\lambda M\) and no drive, has heat \(0\) by the equilibrium cancellation INFO_PHYSICS already records, and \(\mathbb{E}[(0-X)^2]=v\).

At the threshold \(w=kT a/v\) the two expressions agree, both equal to \(kT a\). The centered spring, minimizing \(kT\,av/\varepsilon+w\varepsilon\) instead, tracks when \(w\ge 4kT a/v\) and is blind below that. The thresholds differ by the factor \(4\) because the centered floor is \(R(\varepsilon)+kT a\) on the raw error, and a constant shifts the comparison with the blind cost \(wv\).

At \(a=v=kT=1\):

| Stake \(w\) | Error | Heat | Cost | Centered-spring heat at the same error |
|---|---|---|---|---|
| 2 | 0.707106781187 | 0.414213562373 | 1.828427124746 | 1.414213562373 |
| 8 | 0.353553390593 | 1.828427124746 | 4.656854249492 | 2.828427124746 |
| 20 | 0.223606797750 | 3.472135955000 | 7.944271909999 | 4.472135955000 |
| 50 | 0.141421356237 | 6.071067811865 | 13.142135623731 | 7.071067811865 |

The errors at stakes \(8\), \(20\), and \(50\) are the errors INFO_PHYSICS prints for the centered heat objective, \(1/\sqrt{w}\). The heats are lower by \(kT a=1\). The costs are lower by the same constant. At stake \(2\) the attainable frontier tracks. The centered heat objective is blind, because \(2\sqrt{2}>2\), while \(2\sqrt{2}-1<2\). Where both objectives track, the constant \(kT a\) does not move the minimizing error. It does move the decision between tracking and the blind memory, on the stake interval between \(kT a/v\) and \(4kT a/v\).

The design that attains the heat column is the fast shrunk spring of §4, at finite heat. It is the same error the flow objective of INFO_PHYSICS selects, including the decision to track at stake \(2\). On the centered family that flow objective is reached only where the heat diverges. Once the rest point may sit at \(cX\), the heat objective reaches the same error at the finite heat \(kT\,R(\varepsilon)\).

## 8. What the frontier depends on

For this signal and this loss,

\[
J_{\mathrm{phys}}^{\star}(w)=\min_{\text{designs}}\big(\dot Q+w\,\mathbb{E}[\ell]\big)
\]

equals the scalar minimum in §7. Every design in the class pays at least that. The amount above it is the design: a centered unshrunk coordinate pays an extra \(kT a\) on the raw error; a finite rate pays the factor \(\rho\varepsilon/(\rho(v+\varepsilon)-v)\); a capacity-1 state pays a factor \(2\) on the learning rate; a non-Gaussian conditional pays the Fisher excess; a futile cycle pays its affinity. The floor itself depends on the signal through \(a\) and \(v\), and on the loss through \(\varepsilon\) and \(w\).

It is not a floor for every signal. A different spectrum has a different rate. The random-walk limit is CT7, and \(kT a\) tends to \(0\) there, so the constant is not an upkeep charged for every world. It is not \(h\).

The shape is the one a Carnot quantity has inside its class: a floor fixed by the signal and the error, and an excess that belongs to the machine. Equality is a limit of diverging internal rate at finite heat, as on the telegraph frontier, where the infimum \(0.6\ln 4\) is approached as the memory rates diverge and is not attained at finite rates.

\(w\) is still an input. \(kT\) does not set it. Ruin and linking stay outside \(J_{\mathrm{phys}}\), as INFO_PHYSICS condition 5 says. If H3 holds for the heat and the error, Lemma LY puts a growth-maximizing lineage on the non-dominated part of that front. H3 is still an assumption. This frontier is not the master equation, and this note does not edit that equation.

## 9. Proved, numerical, open

**Proved on this page.**

- The learning rate of a regular memory of an exogenous equilibrium OU signal is at least \(R(\varepsilon_{\mathrm{MMSE}})\), hence at least \(R(\varepsilon)\) at decision error \(\varepsilon\).
- The signal bath has medium heat \(0\).
- On the linear family, the Sekimoto heat exceeds the learning rate by the displayed rational function, and the shrunk spring approaches \(kT\,R(\varepsilon)\) at finite heat with the raw error held at \(\varepsilon\).
- On the centered spring the fast heat equals \(R(s)\) at \(s=v\varepsilon/(v+\varepsilon)\), and exceeds \(R(\varepsilon)\) by \(kT a\).
- The path information rate of the linear memory is \(R(P)\), and it meets the Hartich–Barato–Seifert bare-sensor formulas. At their capacity-1 noise the heat is twice the learning rate.
- The frontier and the stake table.

**Numerical, in the checks.**

- The factored heat gap on 40 random linear designs, relative residual \(1.676\times 10^{-15}\).
- The reference centered spring: error \(0.483333333333\), Sekimoto heat \(4.444444444444\).
- The \(K\)-bin table and the retuned heats \(4.471064\), \(4.157870\), \(4.058746\), \(4.022937\).
- The quartic conditional, excess Fisher \(2.712561\).
- Thirty two-memory systems, and the equilibrium embedding at heat \(4.00200100\).

**Open.**

- A signal that is not an equilibrium OU, including a signal whose own bath pays.
- A loss that is not a mean square.
- A memory that changes \(X\). Proposition AT-signal uses A-X.
- A coupling outside the bipartite Markov class. The learning-rate floor is proved for regular conditionals; the heat inequality for a general memory is the Horowitz–Esposito theorem, applied here and not re-proved.
- Equality at finite memory rate. The infimum is a limit, as on the telegraph.
- Whether a capacity-1 design can pay less than twice the learning rate. Hartich, Barato, and Seifert prove it cannot for a bipartite process, under the fictitious-memory step in their §V. This note does not extend that theorem.
- Ruin, linking, the stake \(w\), and H3. The master equation remains the equation in THEORY.

## 10. Checks

`theory/info_physics_checks/attainability_checks.py`. 28 checks, FAILS 0. The numbers in §§4–7 are the numbers it prints.

## 11. References

Duncan, T. E. 1970. On the calculation of mutual information. *SIAM J. Appl. Math.* 19:215. doi 10.1137/0119020.

Horowitz, J. M., and Esposito, M. 2014. Thermodynamics with continuous information flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.

Horowitz, J. M., and Sandberg, H. 2014. Second-law-like inequalities with information and their interpretations. *New J. Phys.* 16:125007. doi 10.1088/1367-2630/16/12/125007.

Barato, A. C., Hartich, D., and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.

Bo, S., Del Giudice, M., and Celani, A. 2015. Thermodynamic limits to information harvesting by sensory systems. *J. Stat. Mech.* P01014. doi 10.1088/1742-5468/2015/01/P01014. Crossref lists the families as Bo, Giudice, and Celani.

Hartich, D., Barato, A. C., and Seifert, U. 2016. Sensory capacity: an information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116.
