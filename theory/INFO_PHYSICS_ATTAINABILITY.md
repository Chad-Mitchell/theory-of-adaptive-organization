# The Kalman rate is a heat floor, and a linear spring attains it

*Sunday 22 November 2026. Draft. A self-check, not an independent review. Repaired after the review of draft PR #178 (`reviews/attainability_2026-11-22/REVIEW.md`). The hypothesis sentence is unchanged. The master equation in THEORY is unchanged. No locked preregistration file is edited. Checks: `theory/info_physics_checks/attainability_checks.py`, run at `nice -n 19` (31 checks, FAILS 0). DOIs resolved on the Crossref API on 22 November 2026 are listed in `theory/info_physics_checks/attainability_crossref.out`. The dated correction of the merged note is `theory/INFO_PHYSICS_CORRECTION_2026-11-22.md`.*

Labels: **PROVED** (a proof is on this page, under the assumptions named with it), **PROVED (in-model)** (the same, inside a stated model), **PRIOR ART** (published, credited, not claimed here), **NUMERICAL**, **OPEN**. A lower bound is not a derivation of the cost.

This note answers the question left open in `theory/INFO_PHYSICS.md` §8a and OPEN_WORK T37: whether \(kT\) times the optimal causal information rate is attainable at finite heat for a continuous signal. It does not replace the centered-spring statements in that note. Those statements are about one family, scored by the raw coordinate error.

## 0. The question, and the answer

The signal is the equilibrium Ornstein–Uhlenbeck process

\[
dX=-a X\,dt+\sqrt{2av}\,dW,
\]

variance \(v\), temperature of the memory bath \(T\).

**The loss.** The action \(g\) is a function of the current memory state \(M\), which is A-B. The decision error is the mean square of that action,

\[
\varepsilon=\mathbb{E}[(g(M)-X)^2].
\]

The smallest such error, over choices of \(g\), is the conditional error \(\varepsilon_{\mathrm{MMSE}}=\mathbb{E}[\mathrm{Var}(X\mid M)]\), attained at \(g(M)=\mathbb{E}[X\mid M]\). Every \(\varepsilon\) in this note is that decision error, unless the sentence says raw coordinate error. The raw coordinate error \(\mathbb{E}[(M-X)^2]\) is the decision error of the particular action \(g(M)=M\). It equals \(\varepsilon_{\mathrm{MMSE}}+\mathbb{E}[(M-\mathbb{E}[X\mid M])^2]\). Scoring the centered coordinate's raw error, when the decision is the conditional mean, charges an error the action is not using.

The Kalman rate at a decision error \(\varepsilon\in(0,v)\), in these units, is

\[
R(\varepsilon)=a\frac{v-\varepsilon}{\varepsilon}.
\]

Duncan's theorem is the mutual-information rate of a path observation. It equals \(R(\varepsilon)\) when the filter state is a sufficient statistic of that path and holds error \(\varepsilon\). PD7 already books the filter rate. Section 3 proves that the learning rate of any regular memory is at least \(R(\varepsilon)\) at the decision error, and §4 shows that the memory-bath heat meets \(kT\,R(\varepsilon)\) in a limit where the heat stays finite. On that limit the path rate is larger than \(R(\varepsilon)\).

**Answer.** Over bipartite memories of this signal, the infimum of the memory-bath heat at fixed decision error \(\varepsilon\) is \(kT\,R(\varepsilon)\). Two linear designs approach it. One is a spring whose rest point is \(cX\), with \(c=1-\varepsilon/v\), so the coordinate itself is the estimate. At rate \(10^{6}\), decision error \(0.2\), \(a=v=kT=1\), its Sekimoto heat is \(4.000020\), against \(R=4\). The other is the centered spring of INFO_PHYSICS, rest point \(X\), read out by \(g(M)=\mathbb{E}[X\mid M]\). Holding its raw coordinate error at \(v\varepsilon/(v-\varepsilon)=0.25\) holds the decision error at \(0.2\). At the same rate its heat is \(4.000012\), the conditional variance is \(0.20000032\), and the regression gain is \(0.80000048\). The two designs meet in the limit: one puts the gain in the force, the other puts it in the action. Both spend the memory-bath heat on the error \(R\) prices.

The constant \(kT\,a\) is what appears when the centered coordinate is scored by its raw error. At raw error \(0.2\) the fast centered heat is \(5.000020\), the conditional error is \(0.16666694\), and \(5-R(0.2)=1\). That is \(R(s)-R(\varepsilon_{\mathrm{raw}})\) with \(s=v\varepsilon_{\mathrm{raw}}/(v+\varepsilon_{\mathrm{raw}})\). Continuity, a single degree of freedom, and causality do not force it. The loss has to be the decision.

Sensory capacity \(1\), in the sense of Hartich, Barato, and Seifert, asks for a state that keeps the path information. Their factor \(2\) is that demand. The centered spring meets it at their tuned noise and costs \(8\) at decision error \(0.2\). The designs that meet the floor do not. At rate \(10^{6}\) the shrunk spring has path rate \(999.503125\) and capacity \(0.004002\). The limit sends the capacity to \(0\). Hartich's factor \(2\) does not apply there. Sandberg, Delvenne, Newton, and Mitter (2014) give \(2kT\) times the transfer-entropy rate as the implementation cost of a Kalman–Bucy demon that keeps that path information. That is the capacity-1 cost.

The resulting frontier, ruin and linking left outside, is

\[
J_{\mathrm{phys}}^{\star}(w)=\min_{\varepsilon\in(0,v]}\left(kT\,a\frac{v-\varepsilon}{\varepsilon}+w\,\varepsilon\right).
\]

It equals \(wv\) when \(w\le kT a/v\), and \(2\sqrt{kT\,a\,v\,w}-kT a\) when \(w\ge kT a/v\). At \(a=v=kT=1\) and stake \(2\) this frontier tracks, cost \(2\sqrt{2}-1\). The centered-spring heat objective is blind at that stake, cost \(2\), because it minimizes a higher floor.

## 1. Scope

- **A-X.** \(X\) is exogenous. Its drift and diffusion do not depend on the memory. This is P-X of INFO_PHYSICS. A memory that moves its world is outside this note.
- **A-E.** The signal is the equilibrium OU above. Its own medium heat is zero (proved in §3). A driven signal, whose bath can pay, is the case SE3 and Barato, Hartich, and Seifert already separate, and is outside.
- **A-B.** The memory is a bipartite Markov process on the same probability space: a diffusion, a jump process, or a mixture, with one or more degrees of freedom, coupled to baths at temperature \(T\). The action is a function of the current memory state. The checks set \(kT=1\).
- **A-R.** A conditional \(p(x\mid m)\) is regular when it is a positive smooth density on the line, its Fisher information is finite, and the boundary terms in \(\int x\,\partial_x p(x\mid m)\,dx\) vanish, so that integral equals \(-1\). A hard bin of \(X\), zero outside a finite interval and discontinuous at the edge, is not regular. Section 6 uses soft bins, whose posteriors are regular.
- **A-L.** The loss is the decision error of §0, a mean square of an action of the current state. A loss that does not fix a mean square is the vector-loss question INFO_PHYSICS left open, and it stays open.

## 2. What is already proved, or already published

Nothing in this list is claimed as new.

- **Horowitz and Esposito (2014)**, *Phys. Rev. X* 4:031015, doi 10.1103/PhysRevX.4.031015. In steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\). The shape \(\dot Q\ge kT\) times the learning rate is theirs. INFO_PHYSICS uses it for the telegraph and the centered spring.
- **Barato, Hartich, and Seifert (2014)**, *New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024. The learning rate is at most the entropy production of the learning subsystem. CT7 is the random-walk case, already in the repository: holding error \(D\) on a walk of variance rate \(\sigma^2\) dissipates at least \(kT\,\sigma^2/(2D)\). With \(q=2av\) held fixed and \(a\to 0\), \(R(\varepsilon)\to q/(2\varepsilon)\). The \(-a\) in \(R\) is the OU correction and vanishes in that limit. CT7 is not re-derived.
- **Hartich, Barato, and Seifert (2016)**, *Phys. Rev. E* 93:022116, doi 10.1103/PhysRevE.93.022116. Sensory capacity is the learning rate divided by the transfer-entropy rate, \(C=l/\mathcal T\in(0,1]\). If \(C=1\), their equations (63)–(64) give efficiency \(\eta=l/\sigma\le 1/2\), with equality available for a bare sensor. Their bare sensor, equation (47) without the memory coordinate, is the centered spring. Their equations (52), (53), and (54) are the learning rate, the transfer entropy, and the entropy production of that spring. This note recomputes those three from the Lyapunov equation and the Riccati, on and off their capacity-1 locus, and does not re-prove the tradeoff.
- **Horowitz and Sandberg (2014)**, *New J. Phys.* 16:125007, doi 10.1088/1367-2630/16/12/125007. Second-law inequalities with an information flow. Hartich, Barato, and Seifert attribute the linear-Langevin transfer entropy to this paper. The Riccati calculation in §5 reproduces the number Hartich, Barato, and Seifert print.
- **Duncan (1970)**, *SIAM J. Appl. Math.* 19:215, doi 10.1137/0119020, as booked in PD7 and `theory/INTERNAL_MODEL.md`. Duncan's theorem is the path mutual information. For the linear memory it equals \(R(P)\) at the path error \(P\), and it equals the learning rate only when the state is a sufficient statistic of the path. This note does not re-prove Duncan.
- **Mitter and Newton (2005)**, *J. Stat. Phys.* 118:145, doi 10.1007/s10955-004-8781-9. Information supply, storage, and dissipation in the Kalman–Bucy filter, and a statistical-mechanical analogy in which the filter returns signal energy to the bath without an entropy increase, because of the information supply. The analogy is not a lower bound on the bath heat of a physical memory, and it is not a spring that meets \(kT\,R(\varepsilon)\). Already named, with Horowitz and Sandberg, in `theory/INTERNAL_MODEL.md`. Used here only as that analogy.
- **Sandberg, Delvenne, Newton, and Mitter (2014)**, *Phys. Rev. E* 90:042119, doi 10.1103/PhysRevE.90.042119. Their equation (46) sets the nonequilibrium implementation cost of a Kalman–Bucy demon at \(2kT\) times the transfer-entropy rate. That is the capacity-1 cost: a state that keeps the path information. It is not the infimum of the learning-rate heat over memories whose state is not a sufficient statistic.
- **Bo, Del Giudice, and Celani (2015)**, *J. Stat. Mech.* P01014, doi 10.1088/1742-5468/2015/01/P01014. Crossref lists the families as Bo, Giudice, and Celani. They bound the information a memory holds about the past of a sensory layer, beyond the present reading, by the extra entropy production of the whole device over the sensory layer. That extra is the gap \(C<1\) measures: the trajectory carries information the instantaneous state does not. They do not derive \(R(\varepsilon)\), the shrunk spring, or this frontier.
- **INFO_PHYSICS §8a**, centered spring. At fixed raw error \(\varepsilon<v\), the heat falls toward \(kT\,av/\varepsilon\) as the memory rate rises, and the information flow rises from \(R(\varepsilon)\) to the same value. The flow meets \(R(\varepsilon)\) where the heat diverges. Those sentences stand. They describe the spring whose rest point is \(X\), with the loss \(\mathbb{E}[(M-X)^2]\). Section 4 puts the same formulas next to the conditional error.

The telegraph equality, the stake table, and the proposal \(J_{\mathrm{phys}}=\dot Q+w\,\mathbb{E}[\ell]\) stay in INFO_PHYSICS. This note is the continuous-signal step that proposal named and left open.

## 3. The learning rate is at least the Kalman rate

**Proposition AT-learn (PROVED, under A-X, A-E, A-R).** Let the memory state \(M\) carry regular conditionals in the sense A-R. Write \(u=\partial_x\ln p(x\mid m)\) and \(F(X\mid m)=\int u^2\,p(x\mid m)\,dx\). For this equilibrium signal the Horowitz–Esposito information flow of the signal current and the Hartich–Barato–Seifert learning rate are the same number, because the contraction against the marginal score cancels. That number is

\[
L=a\big(v\,\mathbb{E}[F(X\mid M)]-1\big).
\]

Fisher's inequality and Jensen's inequality then give \(L\ge R(\varepsilon_{\mathrm{MMSE}})\), and a decision error \(\varepsilon\) gives \(L\ge R(\varepsilon_{\mathrm{MMSE}})\ge R(\varepsilon)\).

*Proof.* The signal is exogenous, so its marginal is the equilibrium Gaussian of variance \(v\), score \(-x/v\), and its probability current is

\[
\frac{j_X}{p}=-ax-av\,u.
\]

Horowitz and Esposito contract that current against \(\partial_x\ln(p/(p_X p_M))=u+x/v\):

\[
\dot I_X=\Big\langle\frac{j_X}{p}\,(u+x/v)\Big\rangle.
\]

Hartich, Barato, and Seifert's learning rate, the rate at which the signal current raises the conditional entropy, is

\[
L=-\Big\langle\frac{j_X}{p}\,u\Big\rangle.
\]

The two differ by the marginal contraction

\[
\Big\langle\frac{j_X}{p}\,\frac{x}{v}\Big\rangle=\big\langle(-ax-av\,u)(x/v)\big\rangle=-(a/v)\langle x^2\rangle-a\langle xu\rangle.
\]

Regularity gives \(\langle xu\rangle=-1\), and \(\langle x^2\rangle=v\), so the contraction is \(-a+a=0\). The information flow and the learning rate are the same number. Expanding the learning rate,

\[
\Big\langle\frac{j_X}{p}\,u\Big\rangle=\langle(-ax-av\,u)\,u\rangle=-a\langle xu\rangle-av\,\mathbb{E}[u^2]=a-av\,\mathbb{E}[F],
\]

and \(L=a(v\,\mathbb{E}[F]-1)\). In steady state the memory's own transitions supply this \(L\), because the mutual information is constant.

Fisher's inequality gives \(F(X\mid m)\ge 1/\mathrm{Var}(X\mid m)\), with equality exactly for a Gaussian. Jensen's inequality on \(1/s\), convex for \(s>0\), gives \(\mathbb{E}[1/\mathrm{Var}]\ge 1/\varepsilon_{\mathrm{MMSE}}\), with equality when the conditional variance is constant. Therefore

\[
L\ge a\Big(\frac{v}{\varepsilon_{\mathrm{MMSE}}}-1\Big)=R(\varepsilon_{\mathrm{MMSE}}).
\]

Any action \(g(M)\) has decision error at least \(\varepsilon_{\mathrm{MMSE}}\), with equality at \(g(M)=\mathbb{E}[X\mid M]\). \(R\) decreases on \((0,v]\), so a decision error \(\varepsilon\) implies \(L\ge R(\varepsilon_{\mathrm{MMSE}})\ge R(\varepsilon)\). The raw coordinate error is \(\varepsilon_{\mathrm{MMSE}}+\mathbb{E}[(M-\mathbb{E}[X\mid M])^2]\), so the same chain covers a loss that scores the coordinate. Charging \(R\) at that larger number, when the decision error is \(\varepsilon_{\mathrm{MMSE}}\), is the scoring gap of §4. ∎

Duncan's theorem is not this bound. It is the mutual-information rate between the signal path and an observation path. For the linear memory of §4, after the known \(-\beta M\,dt\) is removed from \(dM\), that path rate is \(\gamma^2 P/(4D)\). The Riccati \(\gamma^2 P^2=4aD(v-P)\) converts it into \(R(P)\). The path error \(P\) is at most the error \(s\) given \(M_t\) alone, so the path rate is at least the learning rate. The two agree only when \(P=s\), that is when \(M_t\) is a sufficient statistic of the path of \(M\). The inequality proved here is the learning-rate bound. On the designs that attain the heat floor, the path rate is the larger number.

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

The constant \(kT\,a\) is that difference. It is a scoring gap: the loss was charged at the raw coordinate error, and the decision the conditional mean would have made is the smaller error \(s\). The fast centered spring is thermodynamically tight against \(R(s)\).

**The same spring, scored on the decision (PROVED (in-model)).** Hold the raw coordinate error at \(v\varepsilon/(v-\varepsilon)\). For \(\varepsilon=0.2\) and \(v=1\) that raw error is \(0.25\). At \(\lambda=10^6\) the conditional variance is \(0.20000032\), the Sekimoto heat is \(4.00001200\), and the regression gain \(C_{XM}/C_{MM}\) is \(0.80000048\). The action \(g(M)=\mathbb{E}[X\mid M]\) is a function of the current state, which A-B already allows, and its decision error is \(0.20000032\) at that heat. The shrunk spring at decision error \(0.2\) and the same rate has heat \(4.000020\). The two meet as \(\lambda\to\infty\): moving the rest point to \(cX\) with \(c=1-\varepsilon/v\) puts the gain into the force, so the coordinate itself becomes the estimate. Comparing them at the same raw \(\mathbb{E}[(M-X)^2]\) charges the centered coordinate for an estimate it is not using.

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

The factor \(2\) is their tradeoff, attained by this sensor: a state that carries the whole trajectory pays at least twice the learning rate, and this parameter choice pays exactly twice. Sandberg, Delvenne, Newton, and Mitter (2014), equation (46), write the same factor as an implementation cost, \(\dot W_{\mathrm{impl}}=2kT\,\dot I_c\), for a Kalman–Bucy demon whose state keeps the path information. Mitter and Newton (2005) is the analogy in which that filter returns signal energy without an entropy increase. It is not this heat bound, and it is not the shrunk spring. At decision error \(0.2\) the capacity-1 design costs \(8\) and the shrunk spring approaches \(4\).

The decision loss does not ask for \(C=1\). The action reads the current state. On the shrunk spring at \(a=v=1\), \(\varepsilon=0.2\), the capacity \(L/\mathcal T\) is \(0.7742\) at \(\lambda=6\), \(0.8412\) at \(\lambda=20\), then \(0.4074\), \(0.1281\), \(0.0402\), and \(0.0040\) at \(\lambda=10^2,10^3,10^4,10^6\). At \(\lambda=10^6\) the learning rate is \(4.000000000020\) and the path rate is \(999.503125\). The limit that brings the heat to \(R(\varepsilon)\) sends the capacity to \(0\). Hartich's factor \(2\) covers the sufficient statistic. It does not apply to this design. The state that attains the floor keeps almost none of the path information.

Bo, Del Giudice, and Celani bound that unused past information by extra entropy production. Raising \(C\) to \(1\) is where the factor \(2\) enters. The gap \(kT\,a\) is neither that factor nor a cost of continuity. It is the scoring gap of the unshrunk coordinate.

## 6. Other implementations

**Nonlinear potentials.** Proposition AT-learn is strict unless the conditional is Gaussian with constant variance. A fast equilibrium in a non-quadratic potential has a non-Gaussian conditional, so its learning rate lies above \(R\) of its own MMSE, and the Horowitz–Esposito inequality puts the heat at least there. **NUMERICAL.** A fast equilibrium in \(V=(m-x)^4/(4\,w^4)\) at \(w=0.45\), \(v=1\), on the grid in the checks, has MMSE \(0.120383\), Fisher information \(11.019370\), and \(1/\mathrm{MMSE}=8.306810\). The learning rate is \(10.019370\), against the Kalman rate \(7.306810\) of that error. The check locks the sign of the excess, not these digits as a closed form.

**Several degrees of freedom.** The Fisher bound uses the conditional of \(X\) given the whole memory state. Extra coordinates can lower the conditional variance, which raises \(R\), or they can sit at equilibrium and add nothing. They do not open a heat below \(kT\,R(\varepsilon)\). **NUMERICAL.** Embedding the shrunk spring at \(\lambda=10^4\), \(\varepsilon=0.2\), next to an equilibrium second coordinate, gives total heat \(4.00200100\), equal to the one-coordinate heat. Thirty other stable two-memory linear systems, drawn from the box in the checks, all sit above their own learning rate. The closest heat in that draw is \(1.615570\) times the Kalman rate of its conditional error. The draw is not a minimization. The minimizing design is the one coordinate of §4.

**A \(K\)-state channel.** **NUMERICAL, learning rates.** Quantize the Gaussian channel \(Y=X+\sigma\xi\), which has MMSE \(v\sigma^2/(\sigma^2+v)\), into \(K\) equal-probability bins. The checks compute \(a(v\,\mathbb{E}[F]-1)\) for the posterior of \(X\) given the bin. They do not integrate a bath heat for a \(K\)-state memory. The fast-equilibrium identification of that learning rate with the heat is proved for the telegraph and, by the rational gap in §4, for the linear spring. It is not derived for this channel. The attainment of the floor is the shrunk spring's Sekimoto heat, and the centered spring's Sekimoto heat at the matched decision error. The numbers below are learning rates. For the parent channel with \(\sigma=1/2\) and \(v=1\), whose own MMSE is \(0.2\) and whose Kalman rate is \(4\):

| \(K\) | MMSE | learning rate | \(R(\mathrm{MMSE})\) | ratio |
|---|---|---|---|---|
| 2 | 0.490704 | 1.260226 | 1.037888 | 1.214222 |
| 4 | 0.311557 | 2.553460 | 2.209689 | 1.155575 |
| 8 | 0.243971 | 3.340692 | 3.098849 | 1.078043 |
| 16 | 0.217779 | 3.712237 | 3.591804 | 1.033530 |
| 32 | 0.207370 | 3.874749 | 3.822309 | 1.013719 |
| 64 | 0.203125 | 3.944925 | 3.923079 | 1.005569 |

Retuning \(\sigma\) so the bin index has decision error \(0.2\), the learning rate is \(4.471064\) at \(K=8\), \(4.157870\) at \(K=16\), \(4.058746\) at \(K=32\), and \(4.022937\) at \(K=64\), against \(R(0.2)=4\). The ratio falls with \(K\). A hard partition is outside A-R. Whether a physical \(K\)-state bath meets these learning rates remains open. The soft-bin calculation is a numerical approach of the learning rate to \(R\), not a second proof that the heat meets \(R\).

**Non-equilibrium cycles and feedback onto the memory.** A futile cycle adds a nonnegative term to the entropy production. The telegraph ray in INFO_PHYSICS §4 is that term at fixed error: the heat rises with the excess affinity and the error does not. Feedback of \(X\) into the memory drift is already allowed. The learning rate in §3 depends on the conditional law of \(X\), not on the form of the memory drift. A drive that changes \(X\) leaves A-X, and then Proposition AT-signal need not hold.

## 7. The frontier

Minimize \(kT\,R(\varepsilon)+w\varepsilon\) on \(\varepsilon\in(0,v]\). The derivative \(-kT\,av/\varepsilon^2+w\) vanishes at

\[
\varepsilon^{\star}=\sqrt{\frac{kT\,av}{w}},
\]

which lies in \((0,v]\) when \(w\ge kT a/v\). The second derivative \(2kT\,av/\varepsilon^3\) is positive there. The minimum value is \(2\sqrt{kT\,a\,v\,w}-kT a\). When \(w\le kT a/v\) the derivative is negative on the whole interval, the minimum is at \(\varepsilon=v\), the heat is \(0\), and the cost is \(wv\). The blind memory, force \(-\lambda M\) and no drive, has heat \(0\) by the equilibrium cancellation INFO_PHYSICS already records, and \(\mathbb{E}[(0-X)^2]=v\).

At the threshold \(w=kT a/v\) the two expressions agree, both equal to \(kT a\). The centered spring, minimizing \(kT\,av/\varepsilon+w\varepsilon\) instead, tracks when \(w\ge 4kT a/v\) and is blind below that. The thresholds differ by the factor \(4\) because the centered floor is \(R(\varepsilon)+kT a\) on the raw error, and a constant shifts the comparison with the blind cost \(wv\).

At \(a=v=kT=1\):

| Stake \(w\) | Decision error | Heat | Cost | Centered spring, raw coordinate held at this error |
|---|---|---|---|---|
| 2 | 0.707106781187 | 0.414213562373 | 1.828427124746 | 1.414213562373 |
| 8 | 0.353553390593 | 1.828427124746 | 4.656854249492 | 2.828427124746 |
| 20 | 0.223606797750 | 3.472135955000 | 7.944271909999 | 4.472135955000 |
| 50 | 0.141421356237 | 6.071067811865 | 13.142135623731 | 7.071067811865 |

The errors at stakes \(8\), \(20\), and \(50\) are the errors INFO_PHYSICS prints for the centered heat objective, \(1/\sqrt{w}\). The heats are lower by \(kT a=1\). The costs are lower by the same constant. At stake \(2\) the attainable frontier tracks. The centered heat objective is blind, because \(2\sqrt{2}>2\), while \(2\sqrt{2}-1<2\). Where both objectives track, the constant \(kT a\) does not move the minimizing error. It does move the decision between tracking and the blind memory, on the stake interval between \(kT a/v\) and \(4kT a/v\).

The design that attains the heat column is the fast shrunk spring of §4, and, at the same decision error, the centered spring read out by the conditional mean. Both have finite heat. The column "centered spring, raw coordinate held at this error" is the higher floor \(kT\,av/\varepsilon\), which is the table INFO_PHYSICS prints for that coordinate. At a matched decision error the centered heat meets \(kT\,R\): at decision error \(0.2\) it is \(4.000012\), not the \(5\) of the raw-error column. On the centered family scored by the raw coordinate, the flow objective of INFO_PHYSICS is reached only where the heat diverges. Scored on the decision, the heat objective reaches the same error at the finite heat \(kT\,R(\varepsilon)\).

## 8. What the frontier depends on

For this signal and this loss,

\[
J_{\mathrm{phys}}^{\star}(w)=\min_{\text{designs}}\big(\dot Q+w\,\mathbb{E}[\ell]\big)
\]

equals the scalar minimum in §7. Every design in the class pays at least that. The amount above it is the design: a centered unshrunk coordinate pays an extra \(kT a\) on the raw error; a finite rate pays the factor \(\rho\varepsilon/(\rho(v+\varepsilon)-v)\); a capacity-1 state pays a factor \(2\) on the learning rate; a non-Gaussian conditional pays the Fisher excess; a futile cycle pays its affinity. The floor itself depends on the signal through \(a\) and \(v\), and on the loss through \(\varepsilon\) and \(w\).

It is not a floor for every signal. A different spectrum has a different rate. The random-walk limit is CT7, and \(kT a\) tends to \(0\) there, so the constant is not an upkeep charged for every world. It is not \(h\).

The shape is the one a Carnot quantity has inside its class: a floor fixed by the signal and the error, and an excess that belongs to the machine. Equality is a limit of diverging internal rate at finite heat, as on the telegraph frontier, where the infimum \(0.6\ln 4\) is approached as the memory rates diverge and is not attained at finite rates.

\(w\) is still an input. \(kT\) does not set it. Ruin and linking stay outside \(J_{\mathrm{phys}}\), as INFO_PHYSICS condition 5 says. If H3 holds for the heat and the error, Lemma LY puts a growth-maximizing lineage on the non-dominated part of that front. H3 is still an assumption. This frontier is not the master equation, and this note does not edit that equation.

## 9. What this note adds

The memory-bath inequality \(\dot Q\ge kT\,L\) is Horowitz and Esposito. The learning-rate form on a sensor is Barato, Hartich, and Seifert (2014). The capacity-1 tradeoff is Hartich, Barato, and Seifert (2016). Duncan is the path mutual information. Bo, Del Giudice, and Celani bound information about the sensory past beyond the present. Mitter and Newton (2005) is the analogy in §2. Sandberg, Delvenne, Newton, and Mitter (2014) are the \(2kT\) transfer-entropy cost of a state that keeps the path. None of those is redone.

What this note adds:

- The identity \(L=a(v\,\mathbb{E}[F]-1)\) for every regular conditional of this exogenous equilibrium OU signal, and the consequence \(L\ge R(\varepsilon)\) at the decision error of any action of the current state. Each piece is prior art or textbook. The combination, as a lower bound on the learning rate of every regular memory of this signal, is the argument in §3.
- The shrunk spring, with the decision error held at \(\varepsilon\) and the Sekimoto heat approaching \(kT\,R(\varepsilon)\) at finite values, and the centered spring plus the conditional-mean readout, which meets the same pair. Hartich's centered family, scored on its own coordinate, does not.
- The reading of the constant \(kT\,a\) as \(R(s)-R(\varepsilon)\) on the unshrunk coordinate. Continuity, one degree of freedom, and causality do not force it. The capacity-1 constraint forces a factor \(2\) on a different design.
- The frontier \(wv\) below \(w=kT a/v\) and \(2\sqrt{kT\,a\,v\,w}-kT a\) above it, including the stake interval between \(kT a/v\) and \(4kT a/v\), where the raw-coordinate heat objective is blind and this frontier tracks.
- The \(K\)-bin learning rates, the quartic Fisher excess, and the two-memory draw, as numerics. The \(K\)-bin figures are learning rates. The bath heat of that channel is not computed.

**Proved on this page, inside that list.** The learning-rate identity and \(L\ge R(\varepsilon_{\mathrm{MMSE}})\ge R(\varepsilon)\). The signal bath's medium heat is \(0\), evaluated in the checks at \(a=1.7\), \(v=0.4\). The linear-family gap \(\dot Q-L\) and the shrunk spring. The centered spring at raw error \(0.25\), decision error \(0.20000032\), heat \(4.00001200\). The path rate \(R(P)\), the capacity sequence, and the frontier.

**Numerical.** The factored gap on 40 designs, relative residual \(1.676\times 10^{-15}\). The reference spring, raw error \(0.483333333333\), Sekimoto heat \(4.444444444444\). The \(K\)-bin learning rates \(4.471064\), \(4.157870\), \(4.058746\), \(4.022937\). The quartic excess Fisher \(2.712561\). Thirty two-memory systems, and the equilibrium embedding at heat \(4.00200100\).

**Open.**

- A signal that is not an equilibrium OU, including a signal whose own bath pays.
- A loss that is not a mean square of an action of the current state.
- A memory that changes \(X\).
- The bath heat of the \(K\)-state channel. The learning rates are computed. The heat equality is not.
- Equality at finite memory rate. The infimum is a limit, as on the telegraph. At finite rate the shrunk coordinate is not yet the conditional mean: at \(\lambda=6\) the gain is \(1.2\).
- Whether a capacity-1 design can pay less than twice the learning rate. Hartich, Barato, and Seifert prove it cannot for a bipartite process, under the fictitious-memory step in their §V. This note does not extend that theorem.
- Ruin, linking, the stake \(w\), and H3. The master equation remains the equation in THEORY.

## 10. Checks

`theory/info_physics_checks/attainability_checks.py`. 31 checks, FAILS 0. The numbers in §§4–7 are the numbers it prints.

## 11. References

Duncan, T. E. 1970. On the calculation of mutual information. *SIAM J. Appl. Math.* 19:215. doi 10.1137/0119020.

Mitter, S. K., and Newton, N. J. 2005. Information and entropy flow in the Kalman–Bucy filter. *J. Stat. Phys.* 118:145. doi 10.1007/s10955-004-8781-9.

Sandberg, H., Delvenne, J.-C., Newton, N. J., and Mitter, S. K. 2014. Maximum work extraction and implementation costs for nonequilibrium Maxwell's demons. *Phys. Rev. E* 90:042119. doi 10.1103/PhysRevE.90.042119.

Horowitz, J. M., and Esposito, M. 2014. Thermodynamics with continuous information flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.

Horowitz, J. M., and Sandberg, H. 2014. Second-law-like inequalities with information and their interpretations. *New J. Phys.* 16:125007. doi 10.1088/1367-2630/16/12/125007.

Barato, A. C., Hartich, D., and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.

Bo, S., Del Giudice, M., and Celani, A. 2015. Thermodynamic limits to information harvesting by sensory systems. *J. Stat. Mech.* P01014. doi 10.1088/1742-5468/2015/01/P01014. Crossref lists the families as Bo, Giudice, and Celani.

Hartich, D., Barato, A. C., and Seifert, U. 2016. Sensory capacity: an information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116.
