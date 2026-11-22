# Co-adaptation: when coupled cost-of-judgment minimizers jointly sit near a minimizer (T12, CX2)

*Saturday 21 November 2026, about 7:40 PM America/New_York. Branch `coadaptation-2026-11-21` off `main` `c92886a`; draft PR; written by one executor for Chad. A self-check, not independently reviewed. It does not change the Part 2 hypothesis sentence, any locked file, or the status of CX2, CT31, CT32 or CT34. Checks: `tools/coadaptation_checks.py`, run by `tools/test_coadaptation_checks.py`.*

## 0. Bottom line

**In plain words.** Take several systems ("parties"), each a population selected on its own cost of judgment \(J_i\), where each party's cost depends on the others' designs (they compete, collaborate, or one is the other's world). Under the selection note's assumptions applied to each party separately (A1, A2-L, rare mutation), the joint long-run distribution of designs is a Boltzmann distribution **if and only if** the game whose costs are \(\beta_iJ_i\) is an exact potential game. Then the joint distribution is \(\pi\propto e^{-\Psi}\), and the selection note's excess lifts with no change of form: conditional on the others, each party is exactly Boltzmann in its own cost at its own \(\beta_i\), so its expected **regret** (its cost above its best reply to the others) is \(d_i/(2\beta_i)\). What the group sits near is the minimizer of the potential, which is a Nash equilibrium, not the joint optimum. The two coincide when costs are aligned shares of one team cost, and then the selection note's fractional excess \(d/(2\sigma N_e)\) returns for the team if every party has the same \(\sigma N_e\). Outside potential games there is no Boltzmann form, but an exact per-party identity still holds in the diffusion model (CA2), and five failure classes have minimal counterexamples (§6).

**The theorem in one line (CA1 + CA1b).** With \(\beta_i=\alpha_i\nu_i\) (selection note, SA1c),

\[
\pi(x)\propto e^{-\Psi(x)}\iff \beta_i\bigl[J_i(x_i',x_{-i})-J_i(x_i,x_{-i})\bigr]=\Psi(x_i',x_{-i})-\Psi(x_i,x_{-i})\ \ \forall i,x,x_i',
\]

and then, for quadratic own wells in whitened coordinates,

\[
\mathbb{E}\bigl[J_i(x)-\min_{y}J_i(y,x_{-i})\bigr]=\frac{d_i}{2\beta_i},\qquad
\mathbb{E}[\Psi]-\Psi^\star=\frac{d}{2},\qquad d=\textstyle\sum_i d_i .
\]

**Status.** CA1–CA4 and the counterexamples of §6 are **PROVED (in-model)**. The Boltzmann form for potential games under logit revision is **KNOWN** (Blume 1993). What is new is the packaging: the origination–fixation chain of the selection note used as the revision rule, the "if and only if" with unequal selection strengths, the per-party regret reading, the team split, the bracket for mismatched strengths (CA3), and the lift of CT34 (CA4). Whether real coupled systems are β-potential games is **OPEN**; nothing here is a field result. CX2 stays **OPEN**: no near-minimization theorem holds for arbitrary coupling (CT32, and §6 here).

**The hypothesis sentence is unchanged.** It is, byte for byte,

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. Status words

As in `theory/SELECTION_AXIOMS.md` §1. **PROVED (in-model)** means proved inside the stated model, which says nothing by itself about nature. **NUMERICAL** means computed. **KNOWN** means published and credited. **OPEN** means not derived or not tested, not refuted.

## 2. Setup

There are \(n\) parties. Party \(i\) is a population of size \(N_i\) whose designs \(x_i\) live on a finite connected undirected design graph \(\mathcal{G}_i\) (in the quadratic statements, a uniform lattice in \(d_i\) whitened coordinates, as in SA1b). The joint state is \(x=(x_1,\dots,x_n)\). Party \(i\) bears the cost rate \(J_i(x_i,x_{-i})\ge 0\). "Acting on the world" is the case where one party is the world: a non-selected process that relaxes on its own cost (§6, F3).

- **CA-A (per party: the selection note's A1 and A2-L).** Party \(i\)'s Wrightian fitness is \(r_i=\exp(m_{0,i}-\alpha_iJ_i)\) with \(\alpha_i>0\) constant on the graph.
- **CA-B (no within-party frequency dependence).** A mutant's cost depends on the other parties' fixed designs and not on its own population's composition. If the "parties" are individuals in one population, this fails and the evolutionary-game case (ESS) applies instead; that case is not covered.
- **CA-C (joint weak mutation).** At most one party is polymorphic at a time: each party's origination rate \(N_i\mu_i\) times the longest fixation time is \(\ll 1\). Substitutions then arrive one party at a time (asynchronous revision).
- **CA-E (equal clocks).** Within party \(i\), every undirected edge of \(\mathcal{G}_i\) carries the same mutation clock \(u_i\). The clocks may differ between parties.

Then the joint fixed state is a continuous-time Markov chain whose moves change one party's design along one edge, at rate \(u_i\varphi_i(x_i\to x_i'\mid x_{-i})\), with \(\varphi_i\) the haploid-Moran fixation probability. From SA1's algebra,

\[
\frac{\varphi_i(x_i\to x_i'\mid x_{-i})}{\varphi_i(x_i'\to x_i\mid x_{-i})}=\exp\bigl(-\beta_i[J_i(x_i',x_{-i})-J_i(x_i,x_{-i})]\bigr),\qquad \beta_i=\alpha_i(N_i-1)
\]

(diploid Wright–Fisher: \(\beta_i=\alpha_i(2N_i-1)\), an approximation). Only this ratio is used below. Any revision rule with the same ratio gives the same results: logit (Glauber) revision as in Blume (1993), Metropolis, or a physical relaxation at inverse temperature \(\beta_i\). Selection, learning, and relaxation are interchangeable here.

## 3. The exact discrete result

**Theorem CA1 (Boltzmann in the β-scaled potential; PROVED (in-model)).** Under CA-A, CA-B, CA-C and CA-E the joint chain has a unique stationary distribution. It is reversible if and only if the game with costs \(\beta_iJ_i\) is an exact potential game (Monderer & Shapley 1996), that is, if some \(\Psi\) satisfies \(\Psi(x_i',x_{-i})-\Psi(x_i,x_{-i})=\beta_i[J_i(x_i',x_{-i})-J_i(x_i,x_{-i})]\) for every party and every unilateral change. Then \(\pi(x)\propto e^{-\Psi(x)}\), whatever the clocks \(u_i\).

*Proof.* Moran fixation probabilities are positive and the product of connected graphs is connected, so the chain is irreducible and \(\pi\) is unique. (If) For a move of party \(i\) along an edge, \(\pi(x')/\pi(x)=e^{-[\Psi(x')-\Psi(x)]}=e^{-\beta_i\Delta J_i}=q(x\to x')/q(x'\to x)\); the clock \(u_i\) cancels. Detailed balance holds on every edge. (Only if) If the chain is reversible with \(\pi\), set \(\Psi=-\log\pi\). On every edge move of party \(i\), \(\Psi(x')-\Psi(x)=\log[q(x'\to x)/q(x\to x')]=\beta_i\Delta J_i\). For non-adjacent \(x_i,x_i'\), sum along a path in \(\mathcal{G}_i\) with \(x_{-i}\) fixed; both sides telescope. So \(\Psi\) is an exact potential for \((\beta_iJ_i)\). □

**Corollary CA1a (weighted potential games).** If \((J_i)\) is a weighted potential game with weights \(\omega_i>0\), \(\Delta_iJ_i=\omega_i\Delta_i\Phi\) (CT31's shared-driver class, \(\omega_i=w_i\)), and \(\beta_i\omega_i=\gamma\) for all \(i\), then \(\pi\propto e^{-\gamma\Phi}\). If \(\beta_i\omega_i\ne\beta_j\omega_j\) and \(\Phi\) has a nonzero mixed difference in \((x_i,x_j)\) somewhere, the chain is **not** reversible. *Proof.* The β-scaled sum around an elementary square in \((x_i,x_j)\) equals \((\beta_i\omega_i-\beta_j\omega_j)\) times the mixed difference of \(\Phi\), and reversibility needs it to vanish (Kolmogorov 1936). Terms of \(J_i\) that depend only on \(x_{-i}\) cancel in every \(i\)-move. □

So matching strengths is not a technicality. Even when every party bears a share of one team cost, unequal \(\beta_i s_i\) break the Boltzmann form (CA3 bounds what is left).

**Theorem CA1b (the selection note's excess, lifted; PROVED (in-model)).** Assume CA1's conclusion.

1. *Per party.* \(\pi(x_i\mid x_{-i})\propto e^{-\beta_iJ_i(x_i,x_{-i})}\) exactly, because \(\Psi-\beta_iJ_i\) does not depend on \(x_i\). If each \(J_i(\cdot,x_{-i})\) is a quadratic well in \(d_i\) whitened coordinates (SA1b's conditions, for every \(x_{-i}\)), the expected regret \(R_i=J_i(x)-\min_yJ_i(y,x_{-i})\) is \(\mathbb{E}[R_i]=d_i/(2\beta_i)\).
2. *Potential.* If \(\Psi\) is a quadratic well in \(d=\sum_id_i\) coordinates, \(\mathbb{E}[\Psi]-\Psi^\star=d/2\); with CA1a, \(\mathbb{E}[\Phi]-\Phi^\star=d/(2\gamma)\).
3. *Team.* Let \(J_T=\sum_iJ_i\), quadratic with Hessian \(H_T\), and \(x^\Psi=\arg\min\Psi\). Then
\[
\mathbb{E}[J_T]-\min J_T=\underbrace{J_T(x^\Psi)-\min J_T}_{\text{potential-to-team gap}\ \ge 0}+\tfrac12\mathrm{Tr}\bigl(H_T(\nabla^2\Psi)^{-1}\bigr).
\]
The first term does not shrink with selection strength. It is the price-of-anarchy gap of CT31 when \(x^\Psi\) is the potential-minimizing Nash point (bounded by \((N+1)/(2\sqrt N)\) in CT31's class). The second term is the scatter, \(O(1/\beta)\).

*Proof.* (1) For a fixed \(x_{-i}\), \(\pi(\cdot\mid x_{-i})\) is SA1's Boltzmann measure for the single cost \(J_i(\cdot,x_{-i})\); apply SA1b and average over \(x_{-i}\). (2) is SA1b for \(\Psi\) at \(\beta=1\). (3) Write \(x=x^\Psi+\delta\) with \(\delta\sim\mathcal N(0,(\nabla^2\Psi)^{-1})\); \(J_T\) is quadratic, so \(\mathbb{E}[J_T]=J_T(x^\Psi)+\tfrac12\mathrm{Tr}(H_T\,\mathrm{Cov}\,\delta)\). □

**Corollary CA1c (aligned shares recover the single-system formula).** If \(J_i=s_iJ_T+h_i(x_{-i})\) with \(s_i>0\) (CT31's stake-proportional cost shares are this with \(s_i=w_i/W\)), the potential is \(J_T\) and the Nash points are the stationary points of \(J_T\). When \(h_i=0\) and \(\sum_is_i=1\), the parties' summed cost is \(J_T\), so the potential-to-team gap is zero. The Boltzmann form needs \(\beta_is_i=\gamma\). With \(h_i=0\) and A2-L, \(\alpha_i=\sigma_i/J_i^\star\) and \(J_i^\star=s_iJ_T^\star\), so \(\beta_is_i=\sigma_i\nu_i/J_T^\star\). **The condition is equal \(\sigma N_e\) across parties**, with each elasticity measured at that party's own operating cost. Then \(\gamma=\sigma N_e/J_T^\star\) and
\[
\frac{\mathbb{E}[J_T]-J_T^\star}{J_T^\star}=\frac{d}{2\sigma N_e},\qquad d=\textstyle\sum_id_i,
\]
which is SA1c's form with the team's total number of soft coordinates.

*Checks (NUMERICAL; labels are sections of the check script).* s1: on a 6×5 two-party grid with Moran fixation and \(\beta_i\omega_i\) matched, the exact stationary vector equals \(e^{-\gamma\Phi}\) to a relative \(10^{-8}\) for clock ratios 1, 1/20 and 20, and is clock-independent to \(8\times10^{-13}\) in total variation; with a 3× mismatch the square-cycle log ratio is 50.9 and the stationary vector moves with the clocks (total variation 0.010). s1c: on 60 random three-party games, reversibility agreed with the β-scaled exact-potential test 60/60. s2: a two-party quadratic potential game on a 0.01 lattice gives regrets 0.006246 and 0.015609 against \(d_i/(2\beta_i)=0.00625\) and 0.015625, potential excess 0.999996 against 1, and a team excess of 0.116671 against 0.116671 (gap 0.0585 plus scatter 0.0582). s3: explicit Moran populations (\(N=8\) each, every mutant's fate simulated birth by death) over 200,000 mutation attempts land at total variation 0.018 from \(e^{-\gamma\Phi}\).

## 4. Beyond potential games: an exact identity in the diffusion model

The discrete chain has no closed form outside potential games. Its continuum limit does have an exact identity.

**Model CA-D (diffusion limit; an assumption).** On a lattice of spacing \(\epsilon_i\) with \(\epsilon_i\beta_i|\nabla_iJ_i|\ll 1\), the substitution chain is approximated by
\[
\mathrm dx_i=-v_i\beta_i\nabla_iJ_i(x)\,\mathrm dt+\sqrt{2v_i}\,\mathrm dW_i,
\]
with \(v_i=\bar q_i\epsilon_i^2\), where \(\bar q_i\) is the edge rate's symmetric part. This follows from the rate ratio \(e^{-\beta_i\epsilon_i\partial J_i}\): drift \(\epsilon(q_+-q_-)\approx-\bar q\epsilon^2\beta\partial J\), variance rate \(\epsilon^2(q_++q_-)\approx 2\bar q\epsilon^2\). The speed \(v_i\) carries the mutation supply. Stationary distributions of the chain do not depend on it in potential games (CA1); here they can.

**Theorem CA2 (per-party virial identity; PROVED (in-model)).** Under CA-D, suppose a stationary distribution with finite second moments exists. Then for every party \(i\) and every constant point \(c_i\),
\[
\mathbb{E}[\nabla_iJ_i(x)]=0,\qquad \beta_i\,\mathbb{E}\bigl[(x_i-c_i)\cdot\nabla_iJ_i(x)\bigr]=d_i,
\]
for any coupling, any speeds, and any \(J_i\), potential or not. *Proof.* Itô on \(x_i\) and on \(|x_i-c_i|^2\): \(\mathrm d\,\mathbb{E}|x_i-c_i|^2/\mathrm dt=-2v_i\beta_i\mathbb{E}[(x_i-c_i)\cdot\nabla_iJ_i]+2v_id_i\), which is zero in stationarity (the stochastic integral has mean zero under finite second moments). The first identity is the same computation for \(\mathbb{E}x_i\). □

In words, on average every party sits at its own first-order condition, so the stationary mean is a Nash point "in mean". Its own-gradient scatter carries exactly \(d_i/\beta_i\), as if it were alone. This is the virial (equipartition) identity of a stationary diffusion, read per party. It is a standard Itô computation; the game reading is the packaging.

**Corollary CA2a (linear–quadratic coupling).** Let \(\nabla_iJ_i=(Mx+m)_i\), \(B=\mathrm{diag}(\beta_i)\), \(V=\mathrm{diag}(v_i)\) (blockwise), and \(K=BM\).
1. A stationary distribution exists iff \(-VK\) is Hurwitz. It is Gaussian, with mean equal to the Nash point \(-M^{-1}m\) and covariance \(\Sigma\) solving \(VK\Sigma+\Sigma K^\top V=2V\). The virial identity reads \(\mathrm{Tr}_i(K\Sigma)=d_i\) blockwise, so \(\mathrm{Tr}(\tfrac12(K+K^\top)\Sigma)=d\).
2. If \(K+K^\top\succ 0\) (the β-scaled game is strictly monotone: Rosen's (1965) diagonal strict convexity with weights \(\beta_i\); "stable games" in Hofbauer & Sandholm 2009, with the sign reversed), the coupled adaptation is stable **for every choice of speeds**. *Proof.* If \(VKz=\lambda z\), then \(z^*Kz=\lambda z^*V^{-1}z\), and the real part of the left side is positive. This is the standard sufficient condition for D-stability (the notion is Arrow & McManus 1958). □
3. If \(K\) is symmetric (the β-potential case), \(\Sigma=K^{-1}=(\nabla^2\Psi)^{-1}\) for every \(V\), which recovers CA1 and CA1b. If \(K\) is not symmetric, \(\Sigma\) depends on the speeds and the per-party regret is not \(d_i/(2\beta_i)\) in general.

**Theorem CA3 (one team cost, mismatched strengths; PROVED (in-model)).** Let \(J_i=s_iJ_T\) with \(J_T=\tfrac12x^\top Qx\), \(Q\succ 0\), and \(\gamma_i=\beta_is_i\) (constant on party \(i\)'s block). For **every** choice of speeds,
\[
\frac{d}{2\gamma_{\max}}\;\le\;\mathbb{E}[J_T]-J_T^\star\;\le\;\frac{d}{2\gamma_{\min}},
\]
and both bounds equal \(d/(2\gamma)\) when all \(\gamma_i=\gamma\) (CA1c). *Proof.* \(A=V\Gamma Q\) with \(\Gamma=\mathrm{diag}(\gamma_i)\) is similar to \((V\Gamma)^{1/2}Q(V\Gamma)^{1/2}\succ 0\), so it is stable and the mean is \(\arg\min J_T\). Let \(\mathcal L(X)=AX+XA^\top\), with \(\mathcal L(\Sigma)=2V\). For \(\Sigma_0=(\gamma_{\min}Q)^{-1}\), \(\mathcal L(\Sigma_0)=2V\Gamma/\gamma_{\min}\succeq 2V\). Since \(\mathcal L^{-1}(Y)=\int_0^\infty e^{-At}Ye^{-A^\top t}\mathrm dt\) preserves order, \(\Sigma\preceq\Sigma_0\), and the lower bound follows the same way. Then \(\tfrac12\mathrm{Tr}(Q\Sigma)\) is bracketed by \(\tfrac12\mathrm{Tr}(Q\Sigma_0)=d/(2\gamma_{\min})\) and \(d/(2\gamma_{\max})\). □

So an aligned team with unequal \(\sigma N_e\) still settles at the team optimum, and its excess is set by its weakest-selected and strongest-selected members, whatever their speeds. *Checks (NUMERICAL).* s5a: a potential LQ game gives \(\Sigma=(\nabla^2\Psi)^{-1}\) at speed ratios 0.1, 1 and 10 to \(2\times10^{-16}\). s5b: opposed coupling (\(J_1=\tfrac12x_1^2+1.5x_1x_2\), \(J_2=x_2^2-1.5x_1x_2\)) gives Lyapunov covariances that move with the speed ratio (spread 0.29) while the virial identity holds to \(10^{-15}\); Euler–Maruyama gives virials 1.006 and 0.995. s5g: in a nonlinear non-potential game the Monte Carlo virials are 1.005 and 1.006 about \(c=0\), and 0.984 and 0.999 about \(c=1\). s5c: 3,000 random teams (\(d=2\)–4, \(\gamma_i\in[0.2,5]\), random speeds) gave no violation of the bracket, and equal strengths gave \(d/(2\gamma)\) to \(2\times10^{-13}\).

## 5. The parent's upkeep, lifted (CT34 under selection)

CT34 says that a team's optimized cost enters the parent exactly as upkeep when the parent sees the team only through quantities fixed before the team optimizes. Under co-selection, with parent design \(x\), team design \(y\), \(J=F(x)+G(y;\theta(x))\), the parent selected on \(J\) at strength \(\beta_P\) and the team on \(G\) at \(\beta_T\), the game is an exact potential game with potential \(J\) (weights 1, 1).

**Theorem CA4 (PROVED (in-model)).**
1. *Fixed \(\theta\) (CT34 (ii)).* \(J=F(x)+G(y)\) has no mixed term, so the β-scaled game has potential \(\beta_PF+\beta_TG\) for **any** \(\beta_P,\beta_T\). The stationary distribution is the product \(e^{-\beta_PF(x)}e^{-\beta_TG(y)}\), and for quadratic wells \(\mathbb{E}[J]=F^\star+d_P/(2\beta_P)+J_T^\star+d_T/(2\beta_T)\). **The team enters the parent as upkeep \(J_T^\star+d_T/(2\beta_T)\)**: CT34's upkeep plus the team's own selection scatter, a constant.
2. *\(\theta(x)\), equal strengths \(\beta\).* \(\pi\propto e^{-\beta J}\), and the parent's marginal is \(\propto\exp(-\beta[F(x)+\mathcal F_T(\theta(x))])\) with the team's free energy \(\mathcal F_T(\theta)=-\beta^{-1}\log\sum_ye^{-\beta G(y;\theta)}\). For a quadratic team well, \(\mathcal F_T=J_T^\star(\theta)+(2\beta)^{-1}\log\det H_T(\theta)+\text{const}\). The parent sees the team through its free energy, not its optimized cost. The correction moves the parent's argmin only if the team's curvature depends on what the parent passes down, and it is \(O(1/\beta)\).
3. *\(\theta(x)\), unequal strengths.* Reversibility fails (CA1a). In the LQ diffusion model only own gradients enter, and \(\nabla_yG=\nabla_yJ\), so this is CA3 with \(s=1\): the mean is \(\arg\min J\), and \(d/(2\beta_{\max})\le\mathbb{E}[J]-J^\star\le d/(2\beta_{\min})\).

*Proof.* (1), (2) by CA1 and integration over \(y\); the Gaussian integral gives the \(\log\det\). (3) as stated. □

*Check (NUMERICAL, s5h).* With \(h(x)=1.5+0.8\tanh x\), the parent's exact marginal matches the free-energy form to \(7\times10^{-17}\) in total variation, against 0.029 for "team as upkeep only". With \(\theta\) fixed and \(\beta_T=11\), the team's expected scatter is 0.045455 against \(1/(2\beta_T)=0.045455\).

## 6. Failure classes, each with a minimal counterexample (PROVED (in-model))

Each is a place where the near-minimizer conclusion does not follow. None is a verdict on the hypothesis; each says which condition to check in a real system.

- **F1. Non-potential coupling with no pure equilibrium: permanent cycling.** Matching pennies with costs in \(\{0,1\}\): \(J_1=\mathbf 1[x_1\ne x_2]\), \(J_2=\mathbf 1[x_1=x_2]\), binary designs, equal clocks and sizes. Every state has one downhill and one uphill exit, and in-rates equal out-rates, so \(\pi\) is uniform at **every** \(\beta\). Then \(\mathbb{E}[J_i]=\tfrac12\) while each best reply costs 0: regret does not shrink with selection. A probability current circulates (0.025, 0.106, 0.223 at \(\beta=1,5,20\); check s4).
- **F2. Cycling in J's class (costs ≥ 0, a unique Nash point).** Three parties, \(J_i=\tfrac12(x_i+cx_{i+1})^2\) (indices mod 3), each chasing the next. The game Jacobian is \(I+cP\), with eigenvalues \(1+c\,e^{2\pi ik/3}\). With equal \(v_i\beta_i\), the unique Nash point \(x=0\) is unstable, through a complex pair (an oscillating arms race), iff \(c>2\) (min real part 0.25, 0.05, −0.05, −0.5 at \(c=1.5,1.9,2.1,3\); check s5d). Not β-potential: the cross-curvatures are \(c\beta_i\) one way and 0 the other.
- **F3. A system whose action moves its own world at least one-for-one.** System cost \(J_s=\tfrac12(x-\theta)^2\ge 0\); the world relaxes on \(J_w=\tfrac12(\theta-gx)^2\), so it copies the design with gain \(g\). For \(g>0\) this is a weighted potential game (\(\beta_w=\beta_s/g\) makes it β-potential), but \(\det\nabla^2\Psi\propto 1-g\). For \(g>1\) the potential is a saddle and unbounded below. With any strengths and speeds, \(\det(VK)\propto 1-g<0\), so the coupled system runs away even though every cost is ≥ 0 (check s5e). This is where CL11/K17's open lever (drift reduction g changes the world) bites: the existing theorems hold the world fixed.
- **F4. Acting faster than the feedback can be tracked (delay).** \(\dot x=-k\,(x(t)-g\,x(t-\tau))\) with \(k=v\beta\), the system seeing a world that pushes back with gain \(g<-1\) after delay \(\tau\). Without delay it is stable for every \(k\). With delay it is stable iff \(k\tau<\arccos(1/g)/\sqrt{g^2-1}\) (Hayes 1950; 1.209 at \(g=-2\); the amplitude ratio is \(5\times10^{-5}\) at 0.8× the bound and 193 at 1.2×; check s5f). **Stronger selection or faster origination (larger \(k\)) can destabilize**, so with delayed feedback "strongly selected" does not imply "near the minimizer".
- **F5. Bode / feedback limits move the minimum, not the gap.** When the coupled loop acts on a world with open-loop unstable poles \(p_k\), every stabilizing design with an open loop of relative degree at least two obeys \(\int_0^\infty\ln|S(i\omega)|\,\mathrm d\omega=\pi\sum_k\mathrm{Re}\,p_k\) (Freudenberg & Looze 1985; Seron, Braslavsky & Goodwin 1997). That is a floor inside \(J^\star\), so it raises the minimum. Selection then brings \(J\) near a minimum that already includes the floor. Whether the sampled-read waterbed of `theory/DYNAMICS.md` §5 enters \(\arg\min J\) is unchanged and **OPEN**. F4 is where feedback limits do break the near-minimizer conclusion: through the adaptation dynamics, not through \(J^\star\).
- **Excluded (assumptions, not counterexamples).** Within-party frequency dependence (CA-B). Simultaneous revision: CA-C delivers one-at-a-time revision, and without it the Boltzmann form and potential-maximizer selection need not hold even in exact potential games (Alós-Ferrer & Netzer 2010). Copying that is only monotone in cost (A2-M; no Boltzmann form, as in the selection note). Non-quadratic wells (Laplace approximations only). Mismatched strengths in the discrete chain (non-reversible; only the LQ bracket CA3 is proved).

## 7. Prior art and what is new

| Piece | Status | Source |
|---|---|---|
| Logit (log-linear) revision in a potential game has a Boltzmann stationary distribution in the potential | KNOWN | Blume 1993; potential games, Monderer & Shapley 1996; a textbook treatment of stochastic stability and logit dynamics is Sandholm 2010 (book, no Crossref DOI found) |
| The weak-mutation fixation ratio \(\exp(-\beta\Delta J)\), \(\beta=\alpha\nu\) | KNOWN | Sella & Hirsh 2005; the selection note SA1 |
| Reversibility iff cycle products balance | KNOWN | Kolmogorov 1936; Kelly 1979 (book) |
| Gibbs form and potential-maximizer selection depend on asynchronous revision | KNOWN | Alós-Ferrer & Netzer 2010 |
| Unequal rationality parameters make the stationary distribution depend on revision probabilities (2-player coordination, closed form) | KNOWN | Rajab, Anubi & Vasconcelos 2025, consistent with CA1a |
| Strict monotonicity implies stability of weighted gradient play; D-stability | KNOWN | Rosen 1965; Hofbauer & Sandholm 2009; Arrow & McManus 1958 |
| Delay stability bound | KNOWN | Hayes 1950 |
| Bode integral with unstable poles | KNOWN | Freudenberg & Looze 1985; Seron et al. 1997 |
| Virial / equipartition identity for a stationary diffusion | KNOWN technique (Itô) | standard |
| CA1 with the origination–fixation chain as the revision rule and unequal \(\beta_i\), as an iff | PROVED (in-model); new packaging, an immediate corollary of the above | this note |
| CA1b per-party regret \(d_i/(2\beta_i)\); team split into potential-to-team gap plus scatter; CA1c equal \(\sigma N_e\) condition | PROVED (in-model); new packaging | this note |
| CA2 read per party for games; CA2a speed-free iff potential | PROVED (in-model); new packaging | this note |
| CA3 bracket for one team cost with mismatched strengths | PROVED (in-model); not found in the sources searched (a short search, not a review) | this note |
| CA4 lift of CT34: upkeep plus scatter; free energy; bracket | PROVED (in-model); new packaging of standard statistical mechanics | this note |

A prior-art search on 21 November 2026 found no source stating CA3 or CA4. That search was short, so "new" here means "not found", and any expert reader may know a source.

## 8. What is open

- **Which real couplings are β-potential games.** Shared-driver and aligned-share classes are (CT31, CA1c). Predator–prey, arms races and pursuit are not. A measurement test needs the cross-curvature symmetry \(\beta_i\,\partial^2J_i/\partial x_i\partial x_j=\beta_j\,\partial^2J_j/\partial x_j\partial x_i\), which is checkable in principle but has not been measured anywhere.
- **A near-minimizer bound for nonlinear, non-potential, strictly monotone games** (beyond CA2's identity and the LQ case).
- **Mismatched strengths in the discrete chain** (CA3 is LQ-diffusion only).
- **Dual control** (acting to learn, Bar-Shalom & Tse 1974) is listed in `reviews/widenet_2026-11-20/SCAN.md` and is not treated here.
- **Whether Bode or the sampled-read waterbed changes \(\arg\min J\)** (DYNAMICS §5) stays OPEN; F5 only places it.
- **Drifting worlds under co-adaptation** (the selection note's SA2 with coupling) is not attempted.

## 9. Numerical checks

`tools/coadaptation_checks.py` (about 12 s), run by `tools/test_coadaptation_checks.py` (13 tests). **NUMERICAL.**

## References

Verified on Crossref, 21 November 2026, America/New_York, unless marked as a book.

- Alós-Ferrer, C. & Netzer, N. 2010, *Games and Economic Behavior* 68:413–427, doi 10.1016/j.geb.2009.08.004, "The logit-response dynamics."
- Arrow, K. J. & McManus, M. 1958, *Econometrica* 26:448, doi 10.2307/1907624, "A Note on Dynamic Stability."
- Bar-Shalom, Y. & Tse, E. 1974, *IEEE Transactions on Automatic Control* 19:494–500, doi 10.1109/TAC.1974.1100635, "Dual effect, certainty equivalence, and separation in stochastic control."
- Blume, L. E. 1993, *Games and Economic Behavior* 5:387–424, doi 10.1006/game.1993.1023, "The Statistical Mechanics of Strategic Interaction."
- Freudenberg, J. & Looze, D. 1985, *IEEE Transactions on Automatic Control* 30:555–565, doi 10.1109/tac.1985.1104004, "Right half plane poles and zeros and design tradeoffs in feedback systems."
- Hayes, N. D. 1950, *Journal of the London Mathematical Society* s1-25:226–232, doi 10.1112/jlms/s1-25.3.226, "Roots of the Transcendental Equation Associated with a Certain Difference-Differential Equation."
- Hofbauer, J. & Sandholm, W. H. 2009, *Journal of Economic Theory* 144:1665–1693, doi 10.1016/j.jet.2009.01.007, "Stable games and their dynamics."
- Kelly, F. P. 1979, *Reversibility and Stochastic Networks*, Wiley (book; no Crossref DOI used).
- Kolmogoroff, A. 1936, *Mathematische Annalen* 112:155–160, doi 10.1007/bf01565412, "Zur Theorie der Markoffschen Ketten."
- Monderer, D. & Shapley, L. S. 1996, *Games and Economic Behavior* 14:124–143, doi 10.1006/game.1996.0044, "Potential Games."
- Rajab, Anubi & Vasconcelos 2025, *IEEE Control Systems Letters* 9:2741–2746, doi 10.1109/lcsys.2025.3641882, "Log-Linear Learning for Coordination With Heterogeneous Bounded Rationalities."
- Rosen, J. B. 1965, *Econometrica* 33:520, doi 10.2307/1911749, "Existence and Uniqueness of Equilibrium Points for Concave N-Person Games."
- Sandholm, W. H. 2010, *Population Games and Evolutionary Dynamics*, MIT Press (book; no Crossref DOI found).
- Sella, G. & Hirsh, A. E. 2005, *Proceedings of the National Academy of Sciences* 102:9541–9546, doi 10.1073/pnas.0501865102, "The application of statistical physics to evolutionary biology."
- Seron, M. M., Braslavsky, J. H. & Goodwin, G. C. 1997, *Fundamental Limitations in Filtering and Control*, Springer, doi 10.1007/978-1-4471-0965-5.
