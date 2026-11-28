# Theorem P for drifting worlds (CX1): the information floor as a flow

*Saturday 21 November 2026, evening, America/New_York; review fixes the same night; CE7 stock repair the same night; merged to `main` as PR #149 (`e88b692`, 21 November 2026, 21:36 ET). Written by one executor for Chad Mitchell. Independent review of head `12cf955` returned READY-WITH-FIXES (`records/reviews/theorem_p_drift_2026-11-21/REVIEW.md`); blind confirm of `9489486` returned NOT READY (`records/reviews/theorem_p_drift_2026-11-21/CONFIRM.md`, CE7 stock blocker plus should-fixes); those fixes were applied in `1861432` and confirmed READY in `records/reviews/theorem_p_drift_2026-11-21/CONFIRM2.md`. A further independent re-confirm of the live `main` text (`62603b4`, blob `c419e3c`, identical to the CE7-repaired note) on 23 November 2026 returned READY; only stale pending-confirm wording was updated. Attacks CLAIM_MAP CX1: does Theorem P (CT1–CT4, THEORY Appendix B.1) extend to worlds with stationary increments (random walk, fBm)? It does not change the Part 2 hypothesis sentence, THEORY §4, or any locked preregistration or hash file. CORE gets a one-line pointer.*

## 0. Bottom line

**In plain words.** In a drifting world, a memory's grip on the world loosens every step. The floor is a **flow**, measured in nats per step, not a stock of bits held. For a world that moves linearly with independent shocks (\(X_{t+1}=AX_t+W_t\), any shock law with a density), and any design whatsoever, the system has to take in new information at least as fast as the drift wears the old information away: the long-run mean squared error \(D\) and the long-run inflow \(\bar r\) satisfy

\[
\bar r\;\ge\;\log\lvert\det A\rvert+\frac n2\log\!\Bigl(1+\frac{N_W}{\lvert\det A\rvert^{2/n}\,D/n}\Bigr),
\qquad\text{scalar: }\;\bar r\ge\tfrac12\log\!\Bigl(a^2+\frac{q}{D}\Bigr),
\]

where \(N_W\) is the entropy power of the shock (its variance \(q\) if Gaussian). For a random walk (\(a=1\)) this says \(D\ge q/(e^{2\bar r}-1)\). The Kalman filter meets it with equality. In continuous time, for an Ornstein–Uhlenbeck world \(\mathrm dX=-\theta X\,\mathrm dt+\sigma\,\mathrm dB\), the inflow rate must be at least \(\sigma^2/(2D)-\theta\): the drift relative to the precision held, less the world's own forgetting.

For **any** exogenous world with a density, linear or not, Markov or not (fBm included), a weaker floor holds: \(D\ge n\,N_{\rm inn}\,e^{-2\bar r/n}\), with \(N_{\rm inn}\) the entropy power of the world's one-step innovation.

**What this gives Theorem P in a drifting world.** Each CT1–CT4 statement gets a drifting-world twin:
- the persistence bound (PD2);
- a model is necessary at every income when the loss is unbounded (PD3: acting blind never survives a random walk);
- a lead-time cap that holds even with unlimited information (PD4: \(k_{\max}<(y-\bar c)/(wq)\) for a random walk);
- the first bit always pays (PD5: no price threshold, unlike CT4). The optimal cost has a closed form, and its continuous-time limit is exactly CT7's square-root form \(\sigma\sqrt{2wc}\), with the price per nat \(c\) in place of \(kT\). No thermodynamic assumption is needed.

**What fails, and so changes in the cost.** The master equation is unchanged: \(J=\kappa I_{\rm mem}+hK+w\mathbb E[\ell]+A+L\), and \(\kappa\) is already a price per nat per unit time. Theorem S1 sets \(I_{\rm mem}=I(M_t;X^t)\) only under stationarity, beside a separate \(c\cdot r\). In a Gaussian world whose variance diverges, every uniformly accurate design has \(I(M_t;X_t)\to\infty\) (CE1), so that stock cannot be the viability term there. The divergent piece \(\tfrac\kappa2\log\mathrm{Var}\) is common to every such design; \(-\tfrac\kappa2\log D\) still ranks designs at a fixed time. Booking a rate is already what `theory/INTERNAL_MODEL.md` §4 and CT7 do, and PD5's limit \(\sigma\sqrt{2wc}\) matches CT7 with \(c\) in place of \(kT\). The stationary definition stays right on its domain (an OU filter keeps \(I\) finite). A renormalized stock is **OPEN**. A world can have vanishing mean inflow while the raw stock still diverges (CE7), so the information term is not forced to be a flow.

**Status, honestly.** The sharp floor is **PRIOR ART**: Tatikonda, Sahai & Mitter (2004) for the scalar Gaussian case, and Kostina & Hassibi (2019) for the vector, non-Gaussian entropy-power converse (stated for control, and by separation for causal compression of additive-noise Markov sources). The general-world floor is an elementary Shannon-lower-bound step, likely known; no novelty is claimed for it. The continuous-time OU rate is Duncan's (1970) Kalman–Bucy identity. **New is the packaging:** Theorem P's four statements proved for drifting worlds; the stock divergence (PD6) and the booking options it leaves open; the time-varying-inflow (Jensen) form; and CT7's square-root form recovered as an information floor. CLAIM_MAP CX1 is **left OPEN, with a partial-resolution pointer**. The flow form of CT1–CT4 is proved here. The raw stock is shown to fail as a viability term when variance diverges. A renormalized stock, tightness beyond the Markov-linear class, and almost-sure ruin without ergodicity are still open.

## 1. Status words

As in `theory/SELECTION_AXIOMS.md` §1: **PROVED (in-model)**, **SKETCH** (argument with a stated gap), **NUMERICAL**, **PRIOR ART / KNOWN**, **OPEN** (not derived or not tested; not refuted). Logarithms are natural; information is in nats unless marked bits.

## 2. Setting

**World.** \(X_t\in\mathbb R^n\), \(t=0,1,2,\dots\), with a joint density.

**Design.** Memory \(M_t\) formed causally from observations of the world and private randomness; action \(A_t=f(M_t)\) aimed at \(X_{t+k}\) (lead \(k\ge0\)); loss \(w\lVert A_t-X_{t+k}\rVert^2\). Write \(M^t=(M_0,\dots,M_t)\).

**PD-A (exogenous, nonanticipative world).** Given the world's past \(X^t\), the design's history \(M^t\) is independent of the world's future \(X_{t+1},X_{t+2},\dots\). The design sees only the past, through channels whose noise is independent of the world's future, and it does not move the world. (CX2, a world the system shapes, is excluded; see CE4.)

**PD-B (general world).** The one-step innovation has entropy bounded below: \(h(X_{t+1}\mid X^t)\ge h_{\rm inn}>-\infty\) for all \(t\). Write \(N_{\rm inn}=e^{2h_{\rm inn}/n}/(2\pi e)\). For a Gaussian scalar world this is the one-step prediction-error variance from the full past. For stationary-increment Gaussian worlds (fBm), its limit is the Kolmogorov–Szegő innovation variance of the increments.

**PD-C (linear world, the sharp tier).** \(X_{t+1}=AX_t+W_t\), with \(W_t\) i.i.d., with a density and finite entropy, and independent of \((X^t,M^t)\). Write \(N_W=e^{2h(W)/n}/(2\pi e)\le\mathrm{tr}\,\Sigma_W/n\), with equality iff \(W\) is white Gaussian, and \(\alpha=\lvert\det A\rvert^{2/n}\). \(A\) may be stable, marginal (random walk, \(A=I\)) or unstable. Stationarity is not assumed.

**Inflow.** \(r_t=I(X_t;M_t\mid M^{t-1})\): new information about the current state that the latest memory update carries, beyond the memory's history. Two facts relate it to the repository's other currencies (chain rule and data processing):
- \(r_t\le I(X^t;M_t\mid M^{t-1})\), the per-step increment of Massey's directed information, which is the read currency \(r\) of Theorem S1;
- \(r_t\le I(X_t;Y_t\mid M^{t-1})\) when \(M_t\) is a function of \((M^{t-1},Y_t)\) and private noise.

So every floor below in terms of \(\bar r\) also holds with the directed-information rate in place of \(\bar r\). Also \(r_t\le H(M_t\mid M^{t-1})\le\log(\#\text{states written})\) for a discrete update. Write \(\bar r=\limsup_T\frac1T\sum_{t=1}^T r_t\) and \(D_k=\liminf_T\frac1T\sum_{t=1}^T\mathbb E\lVert A_t-X_{t+k}\rVert^2\).

**Two lemmas used throughout (KNOWN).**
- (L1, maximum entropy / Shannon lower bound) For any estimator \(f\), \(\mathbb E\lVert X-f(M)\rVert^2\ge n\,N(X\mid M)\), where \(N(X\mid M)=e^{2h(X\mid M)/n}/(2\pi e)\). The reason: \(h(X\mid M)=h(X-f(M)\mid M)\le h(X-f(M))\le\frac n2\log(2\pi e\,\mathbb E\lVert X-f(M)\rVert^2/n)\).
- (L2, conditional entropy-power inequality) If \(W\) is independent of \((X,M)\), then \(e^{2h(X+W\mid M)/n}\ge e^{2h(X\mid M)/n}+e^{2h(W)/n}\). Apply the EPI (Stam 1959) for each value of \(M\). The map \(s\mapsto\frac n2\log(e^{2s/n}+c)\) is convex, so Jensen carries the inequality through the average over \(M\).

## 3. The floors (PD1)

**Theorem PD1 (information floor in a drifting world).**

(a) *General tier (PROVED (in-model); elementary).* Under PD-A and PD-B, \(D_0\ge n\,N_{\rm inn}\,e^{-2\bar r/n}\). With lead \(k\), \(D_k\ge n\,e^{2h_k/n}/(2\pi e)\) for any \(h_k\le\inf_t h(X_{t+k}\mid X^t)\), whatever the inflow.

(b) *Sharp tier (PRIOR ART in substance: Tatikonda, Sahai & Mitter 2004; Kostina & Hassibi 2019; proof given here in this notation).* Under PD-A and PD-C, with \(h(X_0\mid M_0)>-\infty\):
- if \(\bar r\le\log\lvert\det A\rvert\), then \(D_0=\infty\);
- otherwise \(D_0\ge n\,N^\star(\bar r)\) with \(N^\star(r)=\dfrac{N_W\,e^{-2r/n}}{1-\alpha e^{-2r/n}}\), equivalently the rate inequality displayed in §0.

With lead \(k\): \(D_k\ge n\bigl[\alpha^kN^\star(\bar r)+N_W\sum_{j<k}\alpha^j\bigr]\). The scalar Gaussian case is tight: the steady Kalman filter with a Gaussian observation channel meets \(D_0=q/(e^{2r}-a^2)\) with equality at every observation-noise level.

*Proof of (a).* By PD-A, \(h(X_t\mid M^{t-1})\ge h(X_t\mid X^{t-1},M^{t-1})=h(X_t\mid X^{t-1})\ge h_{\rm inn}\). Conditioning reduces entropy, so \(h(X_t\mid M^t)=h(X_t\mid M^{t-1})-r_t\ge h_{\rm inn}-r_t\). L1 gives \(\mathbb E\lVert A_t-X_t\rVert^2\ge nN_{\rm inn}e^{-2r_t/n}\). Average over \(t\le T\), use convexity of \(e^{-2r/n}\) (Jensen), and take \(\liminf\); since \(\bar r_T\le\bar r+o(1)\), the bound follows. For lead \(k\), \(h(X_{t+k}\mid M^t)\ge h(X_{t+k}\mid X^t)\) by PD-A, and L1 applies. □

*Proof of (b).* Let \(u_t=\frac2n h(X_t\mid M^t)-\log 2\pi e\), so \(N(X_t\mid M^t)=e^{u_t}\). By PD-C and L2, with \(h(AX\mid M)=h(X\mid M)+\log\lvert\det A\rvert\):
\(e^{\frac2n h(X_{t+1}\mid M^t)}/(2\pi e)\ge\alpha e^{u_t}+N_W\).
As in (a), \(h(X_{t+1}\mid M^{t+1})=h(X_{t+1}\mid M^t)-r_{t+1}\). Hence

\[
u_{t+1}\;\ge\;-\tfrac2n r_{t+1}+\varphi(u_t),\qquad \varphi(u)=\log(\alpha e^{u}+N_W),
\]

and \(\varphi\) is increasing and convex. Suppose \(D_0<\infty\); otherwise there is nothing to prove. Take \(T_j\to\infty\) along which \(\frac1{T_j}\sum_{t\le T_j}\mathbb E\lVert A_t-X_t\rVert^2\le C\). By L1, \(e^{u_t}\le\mathbb E\lVert A_t-X_t\rVert^2/n\), so \(e^{u_{T_j}}\le T_jC/n\) and \(\limsup_j u_{T_j}/T_j\le0\). Write \(S'_T=\frac1T\sum_{t=1}^Tu_t\) and \(\delta_T=(u_T-u_0)/T\). Summing the recursion and applying Jensen to \(\varphi\) gives \(S'_T\ge-\frac2n\bar r_T+\varphi(S'_T-\delta_T)\), with \(\limsup_j\delta_{T_j}\le0\); since \(\varphi\) is increasing, a negative \(\delta\) only strengthens the inequality. Along the subsequence, \(S'_{T_j}\le\log(C/n)\) by concavity of \(\log\). So every limit point \(s\in[-\infty,\log(C/n)]\) satisfies \(g(s)\ge-\frac2n\bar r\) with \(g(s)=s-\varphi(s)\), and \(g\) is increasing (\(g'=N_W/(\alpha e^s+N_W)>0\)) with supremum \(-\log\alpha\). If \(\bar r\le\frac n2\log\alpha=\log\lvert\det A\rvert\), no \(s\) qualifies, contradicting \(D_0<\infty\). Otherwise \(s\ge g^{-1}(-\frac2n\bar r)=\log N^\star(\bar r)\), and by L1 and Jensen, \(\frac1T\sum\mathbb E\lVert A_t-X_t\rVert^2\ge n\frac1T\sum e^{u_t}\ge n\,e^{S'_T}\). For lead \(k\), iterating L2 gives \(N(X_{t+k}\mid M^t)\ge\alpha^ke^{u_t}+N_W\sum_{j<k}\alpha^j\), which is affine and increasing in \(e^{u_t}\), so the same averaging applies. Tightness: for \(x'=ax+w\), \(y=x+v\) with Gaussian \(v\), the steady posterior and prior variances satisfy \(P_{\rm pr}=a^2P+q\), and \(r=\frac12\log(P_{\rm pr}/P)\) gives \(e^{2r}=a^2+q/P\) exactly. □

**Reading: drift against forgetting.** The scalar floor splits as \(\bar r\ge\log\lvert a\rvert+\tfrac12\log\bigl(1+q/(a^2D)\bigr)\): an instability term (the data-rate theorem; Nair & Evans 2004; Tatikonda & Mitter 2004), plus the information that one step of drift erases from a memory of precision \(D\). In continuous time, sampling an OU world at step \(\mathrm dt\) (\(a=e^{-\theta\mathrm dt}\), \(q=\sigma^2(1-a^2)/(2\theta)\)) and dividing by \(\mathrm dt\) gives

**PD7 (PRIOR ART: Duncan 1970 for Kalman–Bucy; the limit of PD1(b) for sampled designs).** The inflow rate is at least \(\rho\ge\sigma^2/(2D)-\theta\). The Kalman–Bucy filter meets it with equality, since its information rate is \(P/(2s)\) and its Riccati equation gives \(P/(2s)=\sigma^2/(2P)-\theta\). The drift \(\sigma^2\) relative to twice the held precision \(D\) must be covered, less the world's own relaxation rate \(\theta\). No inflow is needed once \(D\) reaches the world's stationary variance \(\sigma^2/(2\theta)\). An unstable world (\(\theta<0\)) adds \(\lvert\theta\rvert\). The PD1(b) bound holds at every \(\mathrm dt\). A proof for non-sampled continuous-time designs is not written out here (SKETCH).

**Relation to CT6 (upkeep is a flow).** CT6's strong data-processing bound is empty for unconstrained Gaussian kernels (\(\eta=1\)). PD1(b) is the Gaussian and linear replacement: \(I_{\rm obs}\ge r\ge\tfrac12\log(a^2+q/D)\).

## 4. Theorem P in a drifting world (PD2–PD6)

Throughout, \(y\) is income per step, \(\bar c\) the policy's other costs per step, and \(\mathcal F(r)\) the PD1 floor in force (general or sharp tier) at lead \(k\).

**PD2 (persistence bound; CT1's twin; PROVED (in-model)).** Under PD-A and PD-B or PD-C, every design's long-run mean loss is at least \(w\,\mathcal F(\bar r)\). If \(y-\bar c<w\,\mathcal F(\bar r)\), the expected reserve drifts to \(-\infty\). If, in addition, the reserve increments are stationary and ergodic, ruin is certain, by CT1's ergodic argument. That holds, for example, for any time-invariant linear design tracking a linear Gaussian world in steady state. *Proof.* Linearity of expectation and PD1; the ergodic step is CT1's. □ Almost-sure ruin for designs whose loss increments are not ergodic is **OPEN**.

**PD3 (a model is necessary at every income; CT2's twin; PROVED (in-model)).** If the world's variance grows without bound in some direction \(u\) (\(\mathrm{Var}(u^\top X_t)\to\infty\); random walks and fBm qualify), and the loss is \(w\lVert A_t-X_{t+k}\rVert^2\), then a blind design (\(M\) independent of \(X\)) has mean loss at least \(w\,\mathrm{Var}(u^\top X_{t+k})\to\infty\). So acting blind is not viable at any finite income. Variance growth alone does not force \(\bar r>0\). The rate claim holds only under PD-C: a design with bounded mean squared error must have \(\bar r>\log\lvert\det A\rvert\) (PD1(b)); for a random walk that threshold is 0. *Proof.* For blind \(A_t\), \(\mathbb E\lVert A_t-X_{t+k}\rVert^2\ge\mathrm{Var}(u^\top X_{t+k})\). The rate statement is PD1(b). □ Contrast CT2, where blind action can be viable. In a drifting world with unbounded stakes it never is. **CE2** shows the unbounded loss is needed. **CE7** shows that outside the linear class a persistent design can have \(\bar r=0\).

**PD4 (lead-time cap; CT3's twin; PROVED (in-model)).** CT3 uses \(I(X_t;X_{t+k})\), which is undefined or infinite when \(X\) has no stationary law. The drifting replacement is a loss cap that information cannot remove. Under PD-C, even at unlimited inflow (\(N^\star\to0\)), \(D_k\ge n N_W\sum_{j<k}\alpha^j\). For a random walk that is \(knN_W\), which is \(kq\) for scalar Gaussian shocks. So persistence requires \(k<(y-\bar c)/(w\,n N_W)\). Under PD-B in general, \(D_k\ge n e^{2h_k/n}/(2\pi e)\) caps the lead the same way. For fBm, \(h_k\) is set by the \(k\)-step prediction-error variance from the full past, which grows with \(k\). *Proof.* PD1 at \(\bar r=\infty\). □ Example (`tools/theorem_p_drift_checks.py`): \(q=w=1\), margin 3.5 gives \(k_{\max}=3\).

**PD5 (the first bit always pays; CT4's twin; PROVED (in-model)).** Price inflow at \(c\) per nat (Theorem S1's read price). Under PD-C with \(\alpha\ge1\) (a marginal or unstable world), \(J\ge w\,nN^\star(\bar r)+c\,\bar r\to\infty\) as \(\bar r\downarrow\log\lvert\det A\rvert\). So the optimal inflow exceeds \(\log\lvert\det A\rvert\) at every finite \(c\): there is no price threshold, unlike CT4's \(\kappa<2\ln2\,a^2\mathrm{Var}\). For a scalar random walk the bound is \(\min_r\{wq/(e^{2r}-1)+cr\}\), which the Kalman filter with a priced Gaussian read attains. The minimizer is

\[
e^{2r^\star}=1+x+\sqrt{x^2+2x},\qquad x=\frac{wq}{c}.
\]

In continuous time (\(q=\sigma^2\mathrm dt\), cost per unit time), the minimum tends to

\[
J^\star\;\to\;\sigma\sqrt{2wc},
\]

which is exactly CT7's \(\sigma\sqrt{2kT\,w}\) with \(kT\) per nat replaced by the price \(c\) per nat. *Proof.* Set the derivative to zero: \(2wq\,z=c(z-1)^2\) with \(z=e^{2r}\). As \(\mathrm dt\to0\), \(D=\sigma^2\mathrm dt/(e^{2r}-1)\) with \(r=\rho\,\mathrm dt\) gives \(D\to\sigma^2/(2\rho)\). The per-step objective is \(wD+cr\), so the cost per unit time is \(wD+c\rho\); the numerical check implements this as `price_optimum_rw(σ² dt, w, c/dt)`. Minimizing gives \(\min_\rho\{w\sigma^2/(2\rho)+c\rho\}=\sigma\sqrt{2wc}\). □ So CT7's tracking floor is an information floor priced per nat. Thermodynamics enters only if \(c\) is set to \(kT\) (Barato, Hartich & Seifert, as in CT7). As CT7 already says, dimensional analysis forces \(\sigma\sqrt{cw}\), so only the \(\sqrt2\) is informative.

**PD6 (the raw stock fails as a viability term; PROVED (in-model)).** In a Gaussian world with \(\mathrm{Var}(u^\top X_t)\to\infty\), every design with uniformly bounded mean squared error \(D\) has \(I(M_t;X_t)\ge h(u^\top X_t)-\tfrac12\log(2\pi e\,D)=\tfrac12\log(\mathrm{Var}(u^\top X_t)/D)\to\infty\). Instantiating \(I_{\rm mem}\) as \(I(M_t;X_t)\) then makes the holding-cost rate unbounded for every uniformly accurate design, so the raw stock cannot be the viability term against a finite income. It still ranks designs at a fixed time. At each finite \(t\), in the Gaussian equality case, \(\kappa I(M_t;X_t)=\tfrac\kappa2\log\mathrm{Var}(u^\top X_t)-\tfrac\kappa2\log D\): the first term is common to every uniformly accurate design and diverges; the second term still ranks designs. What fails is comparing the unregularized cost with a finite income. *Proof.* \(I(M;X)\ge I(M;u^\top X)\) by data processing, and \(I(M;u^\top X)=h(u^\top X)-h(u^\top X\mid M)\), bounded below using L1 in one dimension. □ **CE1** (numerical): for a steady Kalman tracker of a unit random walk, \(I(M_t;X_t)=\tfrac12\log(t/P)\) grows by \(\tfrac12\log10\) per decade (1.39, 2.54, 3.69, 4.85 nats at \(t=10^1\ldots10^4\)), while the inflow stays at 0.481 nats per step. **Consequence for the cost of judgment.** The master equation is not rewritten; \(\kappa\) is already a price per nat per unit time. Theorem S1's \(I_{\rm mem}=I(M_t;X^t)\) stays right on its stationary domain: an OU filter keeps \(I(M_t;X_t)\) finite, and \(\kappa I_{\rm mem}\) still ranks designs there. When that mutual information diverges, stop using it as the viability term. For the linear random walk, booking a rate is already what `theory/INTERNAL_MODEL.md` §4 and CT7 do, and PD5's limit \(\sigma\sqrt{2wc}\) matches CT7 with \(c\) in place of \(kT\); Theorem S1's \(c\cdot r\) is that rate term, and under stationarity it sits beside a finite \(\kappa I_{\rm mem}\). A renormalized stock such as \(I(M_t;X_t)-\tfrac12\log\mathrm{Var}(X_t)\) is finite for the Kalman filter and would let \(\kappa\) keep a stock reading; which renormalization is right (information about the increments, about \(X_t\) relative to a reference, or the predictive part only) is **OPEN**. Both the flow and a renormalized stock are live options: CE7 has bounded error and \(\bar r=0\) while \(I(M_t;X_t)\to\infty\), so the information term is not forced to be a flow. The other terms (\(hK\), \(w\mathbb E[\ell]\), \(A\), \(L\)) are untouched.

## 5. Minimal counterexamples: where each assumption bites

- **CE1 (stock pricing diverges).** PD6, above.
- **CE2 (bounded loss: blind can survive).** With loss \(\min(w(a-x)^2,L)\) in a random walk, a blind design's mean loss tends to \(L\), so blind action is viable whenever \(y-\bar c>L\). PD3 needs unbounded stakes. This is the "bounded fallback" already noted in `theory/INTERNAL_MODEL.md` §4.
- **CE7 (vanishing mean inflow outside the linear class).** Variance growth alone does not force \(\bar r>0\). Let \(Z\sim N(0,1)\), \(G_t\) i.i.d. \(N(0,1)\), and \(X_t=tZ+G_t\). Then \(\mathrm{Var}(X_t)=t^2+1\to\infty\), and the one-step innovation variance is at least 1, so PD-B holds with \(N_{\rm inn}\ge1\). Observe \(Y_t=X_t+N_t\) with \(N_t\sim N(0,1)\) only at \(t=2^k\), and between looks act with \(A_t=t\,\mathbb E[Z\mid\text{looks so far}]\). Through \(T=2^{16}\) (17 looks) the mean squared error stays at most 7.00, the total inflow is 16.8 nats, and the mean inflow is \(2.56\times10^{-4}\) nat/step, so \(\bar r=0\). Blind mean squared error at that \(T\) is \(T^2+1\approx4.29\times10^9\). Because the posterior variance \(v_t\) is deterministic, the memory state driving the policy is the posterior mean \(M_T=\mu_T=\mathbb E[Z\mid\text{looks so far}]\). Since \(Y_T=TZ+G_T+N_T\) enters \(\mu_T\), \(G_T\) correlates with \(Z-\mu_T\) (\(\mathrm{Cov}(Z-\mu_T,G_T)=-T v_{\rm post}/2\)), making \(\mathbb E[(X_T-T\mu_T)^2]=1\) identically and \(\mathrm{Var}(X_T\mid\mu_T)=1-(T v_{\rm post}/2)^2/(1-v_{\rm post})\approx1\). Thus the raw stock still diverges: \(I(\mu_T;X_T)=\tfrac12\log((T^2+1)/\mathrm{Var}(X_T\mid\mu_T))=11.090\) nats at \(T=2^{16}\) (matching \(\tfrac12\log(T^2+1)\) to \(10^{-10}\)). If instead memory keeps the full look record \(Y=(Y_{2^0},\dots,Y_{2^K})\), the Schur complement gives \(\mathrm{Var}(X_T\mid Y)=(T^2 v_{\rm pre}+1)/(T^2 v_{\rm pre}+2)\approx7/8\) and \(I(Y;X_T)=11.157\) nats. PD1(a) is untouched, because at \(\bar r=0\) it only requires \(D\ge N_{\rm inn}\). PD1(b) is untouched, because this world is not \(X\mapsto AX+W\) with i.i.d. \(W\). The construction is checked in `tools/theorem_p_drift_checks.py`.
- **CE3 (no density: the floor is vacuous, not false).** A \(\pm1\) lattice walk has \(h=-\infty\), so the density floors read 0. A memory that writes one bit per step (the sign of the step) tracks it with zero error at \(r=\ln2\) (`tools/theorem_p_drift_checks.py`). The right currency there is the discrete entropy of the step, \(H=\ln2\), not a density bound.
- **CE4 (a system that moves its world).** If the design sets or foresees the next shock (\(M_t\) contains \(W_t\)), PD-A fails: \(h(X_{t+1}\mid M_t)=-\infty\), and lead-1 error can be zero with no inflow about \(X_{t+1}\). Tracking turns into control. The known analog there is Kostina & Hassibi's rate–cost bound for LQR, not proved here. This is CX2 territory.
- **CE5 (the general tier is loose when drift accumulates).** For a random walk, the ratio of the sharp floor to the general floor is \(e^{2r}/(e^{2r}-1)\to\infty\) as \(r\to0\) (1.2, 5.5, 50.5, 500.5 at \(r=1,0.1,0.01,0.001\)). Accumulation of drift, which the sharp tier uses through \(\alpha\), is what makes low inflow hopeless. A sharp tier for non-Markov worlds such as fBm is **OPEN**.
- **CE6 (the vector bound is loose for uneven errors).** PD1(b) uses \(\det\), so with \(A=I\) and \(\Sigma_W=\mathrm{diag}(1,\epsilon)\), the bound is driven by \(N_W=\sqrt\epsilon\) and is far from the per-mode optimum. It is valid but not tight. The exact multidimensional Gaussian sequential rate–distortion function is an SDP (Tanaka, Kim, Parrilo & Mitter 2017; Stavrou, Tanaka & Tatikonda 2020) and is not re-derived here.

## 6. Numerical checks (NUMERICAL)

`tools/theorem_p_drift_checks.py` (quick mode run by `tools/test_theorem_p_drift_checks.py`; `--full` writes `theory/theorem_p_drift_checks/results_full.json`), run at nice 19.

| Check | Result |
|---|---|
| PD1(b) tightness: steady Kalman filter, \(a\in\{0.5,0.9,1,1.2,2\}\), four observation-noise levels | \(D\) equals the floor; largest relative gap \(2.2\times10^{-15}\) |
| PD1(b) against uniform quantized trackers (random walk and \(a=0.9\); best of 29 step sizes; \(r\le\) bits·ln 2) | \(D\) / floor = 1.75, 2.05, 2.49 (random walk, 1–3 bits); 1.65, 2.04, 2.41 (\(a=0.9\)). All above. Fixed-range quantizers diverge in unstable worlds, so \(a>1\) is not used |
| PD1(a) on fBm, \(H\in\{0.3,0.5,0.7\}\), noisy observations, full-history memory, every \(t\le160\) | min over \(t\) of \(D\)/floor = 1.03–1.63. Never below 1; close to 1 at low observation noise |
| PD1(b) with time-varying inflow (alternating observation noise) | mean \(D=0.458\ge\) floor(mean \(r\)) \(=0.172\) |
| CE1 stock growth (steady Kalman, unit random walk) | \(I(M_t;X_t)\) = 1.39, 2.54, 3.69, 4.85 nats at \(t=10,\dots,10^4\); inflow constant at 0.481 nats/step |
| PD5 closed form vs numerical minimization (4 price settings) | agree to \(10^{-8}\) |
| PD5 continuous-time limit (\(\sigma^2=1\), \(w=1\), \(c=0.3\)) | \(J^\star\) = 0.7267, 0.7696, 0.7741, 0.7746 at \(\mathrm dt=10^{-1},\dots,10^{-4}\); \(\sigma\sqrt{2wc}=0.7746\) |
| PD7 Kalman–Bucy (\(\theta=0.7\), three noise levels) | information rate \(=\sigma^2/(2P)-\theta\) to \(10^{-12}\); sampled bound converges |
| CE3 lattice walk | zero error at one bit per step |
| PD4 lead cap (\(q=w=1\), margin 3.5) | \(k_{\max}=3\) |
| CE5 sharp/general ratio at \(r=1,0.1,0.01,0.001\) | 1.2, 5.5, 50.5, 500.5 |
| CE7 sparse looks on \(X_t=tZ+G_t\), through \(T=2^{16}\) | MSE \(\le 7.00\); total inflow 16.8 nats over 17 looks; mean inflow \(2.56\times10^{-4}\) nat/step; blind MSE \(4.29\times10^9\); \(I(\mu_T;X_T)=11.090\) nats (posterior mean; full look record \(I(Y;X_T)=11.157\) nats) |

## 7. Prior art, and what is packaging

Every DOI below was checked on Crossref on 21 November 2026 (America/New_York). No citation is invented.

- **Tatikonda, Sahai & Mitter (2004)**, *IEEE TAC* 49:1549–1561, doi 10.1109/TAC.2004.834430, "Stochastic Linear Control Over a Communication Channel." The scalar Gauss–Markov sequential rate–distortion formula \(R(D)=\tfrac12\log(a^2+q/D)\) (base 2 in their paper). PD1(b) scalar.
- **Kostina & Hassibi (2019)**, *IEEE TAC* 64:4525–4540, doi 10.1109/TAC.2019.2912256, "Rate-Cost Tradeoffs in Control." The entropy-power converse for vector, non-Gaussian noise with a density: \(\log\lvert\det A\rvert+\frac n2\log(1+\dots N(V)\dots)\). They state it for LQR control, and by separation for causal compression of additive-noise Markov sources. PD1(b) is that converse in tracking form; the proof here is ours, and the structure is theirs.
- **Tatikonda & Mitter (2004)**, *IEEE TAC* 49:1056–1068, doi 10.1109/TAC.2004.831187; **Nair & Evans (2004)**, *SIAM J. Control Optim.* 43:413–436, doi 10.1137/S0363012902402116; **Nair, Fagnani, Zampieri & Evans (2007)**, *Proc. IEEE* 95:108–137, doi 10.1109/JPROC.2006.887294. The data-rate theorem (\(r>\sum\log\lvert\lambda_i^{\rm unstable}\rvert\)). PD1(b)'s threshold uses \(\log\lvert\det A\rvert\), which is weaker when \(A\) also has stable modes.
- **Tanaka, Kim, Parrilo & Mitter (2017)**, *IEEE TAC* 62:1896–1910, doi 10.1109/TAC.2016.2601148; **Stavrou, Tanaka & Tatikonda (2020)**, *IEEE TAC* 65:2245–2249, doi 10.1109/TAC.2019.2941444; **Derpich & Østergaard (2012)**, *IEEE Trans. Inf. Theory* 58:3131–3152, doi 10.1109/TIT.2012.2184669; **Silva, Derpich & Østergaard (2011)**, *IEEE TAC* 56:1886–1899, doi 10.1109/TAC.2010.2098070. Multidimensional and stationary sequential/causal rate–distortion, and average data-rate design. Context for CE6.
- **Duncan (1970)**, *SIAM J. Appl. Math.* 19:215–220, doi 10.1137/0119020, "On the Calculation of Mutual Information." Continuous-time information rate of the Kalman–Bucy filter; PD7's equality.
- **Stam (1959)**, *Information and Control* 2:101–112, doi 10.1016/S0019-9958(59)90348-1 (EPI); **Cover & Thomas**, *Elements of Information Theory*, 2nd ed., Wiley 2005, doi 10.1002/047174882X (maximum entropy, Shannon lower bound, chain rules).
- Already in the repository: Massey (1990, directed information); CT1–CT7 and Theorem S1; `theory/INTERNAL_MODEL.md` §4 (data-rate route, many-mode random walk priced per nat of flow).

**Split.** *Prior art:* the sharp floor and its tightness (PD1(b)), the data-rate threshold, and the continuous-time OU rate with Kalman–Bucy equality (PD7). *Elementary, likely known, not claimed:* the general-world floor PD1(a). *Done here (packaging):* the time-varying-inflow form via Jensen; CT1–CT4's drifting twins PD2–PD5; the raw-stock viability failure (PD6) and the booking options it leaves open; CT7's \(\sigma\sqrt{2wc}\) recovered as the continuous-time limit of a priced information floor; and the counterexample list CE1–CE7 tied to the assumptions.

## 8. What remains open

- A renormalized memory stock for drifting worlds that can carry \(\kappa\) as the stationary \(I_{\rm mem}\) does (PD6).
- A sharp tier for non-Markov worlds with stationary increments (fBm), and a tight vector floor for uneven error (CE5–CE6).
- Almost-sure ruin when loss increments are not ergodic (PD2).
- Continuous-time designs not obtained by sampling (PD7).
- Worlds the system moves (CX2; CE4).
- Ruin-capped or nonquadratic losses beyond power losses: the Shannon-lower-bound route should extend to difference distortions with a convex \(h\)-dual, but it is not written out (SKETCH).
- How memory leakage of the store itself (as opposed to the world's drift) enters the floor. SKETCH: in the scalar Kalman case, store noise of variance \(\epsilon\) per step acts like added drift; not proved.

The Part 2 hypothesis sentence is unchanged and is not restated here.
