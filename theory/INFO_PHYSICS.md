# Dissipation bounds the cost of a model, and does not produce the master equation

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. No locked preregistration file is edited. Checks: `theory/info_physics_checks/info_physics_checks.py`, run at `nice -n 19` (37 checks, FAILS 0). DOIs below were resolved on the Crossref API on 22 November 2026 (`theory/info_physics_checks/crossref.out`).*

Labels: **PROVED** (a proof is on this page, under the assumptions named with it), **PROVED (in-model)** (the same, inside a stated model; it says nothing by itself about nature), **PRIOR ART** (published, credited, not claimed here), **CONJECTURE**, **OPEN**. A lower bound is not a derivation of the cost.

## 0. The question, and the answer

The master equation is

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\qquad\text{subject to}\quad P(\mathrm{ruin})\le\varepsilon .
\]

Selection does not produce that list, the cap, or the linear prices. Lemma LY gives Pareto in a bad vector that is handed to it. The growth bridge keeps a variance penalty and still takes the term list as an input. The question here is whether the physics of a system that stores a model and acts on it forces the terms instead.

**Answer.** Physics forces a lower bound on the free-energy rate, in coordinates that are not the master equation's coordinates. In the model solved below, the bound is tight in a slow-signal limit and can be missed by an arbitrarily large factor at fixed task error and fixed mutual information. The master equation is not that bound, and it is not the tangent of the physical frontier, except after assumptions this note does not remove.

What is forced, and what is not:

| Object | Status | Price, where one exists |
|---|---|---|
| Nonpredictive information \(I(s_t;x_t)-I(s_t;x_{t+1})\), per signal update | **PRIOR ART** (Still, Sivak, Bell and Crooks 2012). One-step equality in their accounting; the sum over a protocol is a lower bound | \(kT\) per nat of that difference, per update |
| Information-flow rate of a driven memory | **PROVED (in-model)** for the two-state sensor below. The shape, a subsystem entropy balance modified by a mutual-information rate, is **PRIOR ART** (Horowitz and Esposito 2014) | \(kT\) per nat per unit time of the flow. A rental \(\kappa\) on a stock needs a turnover time, the accounting step already in `core/bridge_2026-11-21/FLOOR.md` |
| Measurement work and erasure work | **PRIOR ART** (Sagawa and Ueda 2009, erratum 2011). They bound the sum | one floor on the sum, not two stacked prices |
| Precision of a steady current | **PRIOR ART** (Barato and Seifert 2015). Checked on the sensor | total entropy production at least \(2k/\varepsilon_{\mathrm{rel}}^2\) over the window that defines the relative uncertainty. Not a constant per layer |
| Task error against predictive information | **PRIOR ART** already in the repository (CT4, Theorem S1, PD1, CT7) | the stake \(w\) converts error into the energy currency. \(kT\) does not set \(w\) |
| Gross stock \(I(M_t;X_{\le t})\), constant upkeep \(h\) per layer, a separate read price stacked on erasure, a linking term in every design, the ruin cap | not forced | none of these is a theorem of the bounds above |

## 1. Setup

Class P is the class the theorems below talk about.

- **P-X.** The world \(X\) is an exogenous stationary Markov process. The memory does not act back on \(X\). This is the repository's standing exogenous world, and it is Still's no-back-action hypothesis. Worlds the system moves are CX2, **OPEN**, and are outside this note.
- **P-B.** The memory \(M\) is either a finite-state continuous-time Markov chain or a linear diffusion, coupled to one heat bath at temperature \(T\). A memory jump obeys local detailed balance: the logarithm of the rate ratio is the entropy the bath receives, in units of \(k\). The checks set \(kT=1\) and report nats.
- **P-S.** The joint process is stationary.
- **P-L.** The action is a function of \(M\). The task loss \(\ell\) is not assumed to be a thermodynamic work. A weight \(w\) that puts \(\ell\) in energy units is an input.
- **P-J.** Where a layer statement needs it: the coordinates of \(M=(M_1,\ldots,M_K)\) are conditionally independent given the trajectory of \(X\). The note says when this is dropped.
- **P-R.** There is no reserve and no ruin constraint in the physical model.

The entropy production used for a stationary Markov chain is the edge sum

\[
\dot\Sigma=\sum_{i\neq j}p_i k_{ij}\ln\frac{k_{ij}}{k_{ji}},
\]

which equals \(\sum (p_i k_{ij}-p_j k_{ji})\ln(k_{ij}/k_{ji})\) over undirected pairs. Each pair is nonnegative because \((a-b)\ln(a/b)\ge 0\). This is the steady-state entropy production of Schnakenberg (1976) and of the stochastic-thermodynamics framework in Seifert (2012). It is not re-derived as a new principle. For a diffusion, the partial entropy production of a coordinate is \(\langle j^2/(Dp)\rangle\), with \(j\) the probability current of that coordinate. That definition is applied to a Gaussian in §4. It is not claimed to equal a particular stochastic-integral convention; the path check in §10 is a sign check.

## 2. Two informations that share a name

The repository uses \(I_{\mathrm{mem}}\) for more than one functional. They are not interchangeable, and the physics bound picks one of them.

**Still's instantaneous pair** (their definitions, quoted from the 2012 paper, arXiv:1203.3271):

\[
I_{\mathrm{mem}}(t):=I(s_t;x_t),\qquad I_{\mathrm{pred}}(t):=I(s_t;x_{t+1}).
\]

The nonpredictive information in that paper is the difference \(I_{\mathrm{mem}}(t)-I_{\mathrm{pred}}(t)\). Their one-step result, under the hypotheses of that paper, is the identity

\[
\beta\big\langle W_{\mathrm{diss}}[x_t\to x_{t+1}]\big\rangle=I_{\mathrm{mem}}(t)-I_{\mathrm{pred}}(t),
\]

because the dissipated work of the signal step, in their nonequilibrium-free-energy accounting, equals \(H(s_t\mid x_{t+1})-H(s_t\mid x_t)\). Summed over a protocol, relaxation steps add a further nonnegative piece, and the published inequality is

\[
I_{\mathrm{mem}}-I_{\mathrm{pred}}\le\beta\langle W_{\mathrm{diss}}\rangle\le\beta\langle W_{\mathrm{ex}}\rangle.
\]

`core/bridge_2026-11-21/FLOOR.md` already records the one-step equality and says the repository's theorems use the inequality. This note does not call either new. Deriving the information bottleneck from that bound is Still (2020), already cited there.

**The past stock** used by Theorem S1 and the Shannon note is \(I(M_t;X_{\le t})\). It is larger than \(I(M_t;X_t)\) when the memory keeps a trace the present does not summarize.

**Lemma IP-chain (PROVED).** Let \(M_t\) be generated from \(X_{\le t}\) and from noise independent of \(X\), and let \(X\) be Markov and exogenous. Then \(M_t\) is independent of \(X_{\ge t+1}\) given \(X_{\le t}\), and

\[
I(M_t;X_{\le t})=I(M_t;X_{\ge t+1})+I(M_t;X_{\le t}\mid X_{\ge t+1}).
\]

If the chain is first-order, \(I(M_t;X_{\ge t+1})=I(M_t;X_{t+1})\).

*Proof.* The chain rule splits the past-and-future mutual information into the future piece and the past given the future. Causal coupling and the Markov property give the conditional independence: given \(X_t\), the future does not depend on the past that built \(M_t\). Given \(X_{t+1}\), the later future does not depend on \((X_{\le t},M_t)\). □

The second term is nonnegative. It is the part of the past stock that the next step of \(X\) does not carry. It is not Still's instantaneous difference, which uses \(I(M_t;X_t)\) rather than \(I(M_t;X_{\le t})\). A sticky memory in §10 holds \(I(M;X_{t-1},X_t)=0.152224\) against \(I(M;X_t)=0.112651\), and the excess of the past stock over \(I(M;X_{t+1})\) is \(0.112693\), against Still's gap \(0.073121\) on the same chain.

## 3. Prior art, with the statements that are used

Resolved on Crossref, 22 November 2026. Nothing in this list is claimed as new, and nothing here is copied beyond the statement needed to say what the bound is.

- **Landauer (1961)**, *IBM J. Res. Dev.* 5:183, doi 10.1147/rd.53.0183. Erasure of one bit of a symmetric memory dissipates at least \(kT\ln 2\). Already the erasure floor on \(\kappa\) in THEORY and in FLOOR.md.
- **Still, Sivak, Bell and Crooks (2012)**, *Phys. Rev. Lett.* 109:120604, doi 10.1103/PhysRevLett.109.120604, arXiv:1203.3271. The statements in §2. Isothermal Markov dynamics, one bath, no back-action. The repository's "at least \(kT(I_{\mathrm{mem}}-I_{\mathrm{pred}})\)" is their protocol inequality, not a new bound.
- **Still (2020)**, *Phys. Rev. Lett.* 124:050601, doi 10.1103/PhysRevLett.124.050601. Thermodynamic cost and benefit of memory; the information bottleneck from the dissipation bound. Already in FLOOR.md.
- **Sagawa and Ueda (2009)**, *Phys. Rev. Lett.* 102:250602, doi 10.1103/PhysRevLett.102.250602, arXiv:0809.4098, and the **erratum (2011)**, *Phys. Rev. Lett.* 106:189901, doi 10.1103/PhysRevLett.106.189901. Lower bounds on the work of measurement and of erasure. The Shannon note already records the consequence used here: the sum is bounded by \(kT\) times the mutual information of the measurement, and that is not a second price stacked on a Landauer floor for the same nats.
- **Sagawa and Ueda (2012)**, *Phys. Rev. Lett.* 109:180602, doi 10.1103/PhysRevLett.109.180602. Fluctuation theorem with information exchange. Cited as part of that line, not re-used as a formula.
- **Parrondo, Horowitz and Sagawa (2015)**, *Nat. Phys.* 11:131, doi 10.1038/nphys3230. The review that puts Landauer, measurement, erasure, and feedback in one frame. This note does not add an inequality from the review.
- **Esposito and Van den Broeck (2011)**, *EPL* 95:40004, doi 10.1209/0295-5075/95/40004. Landauer far from equilibrium. Still's 2012 result is already stated far from equilibrium; this citation is the same caution, not a new floor.
- **Horowitz and Esposito (2014)**, *Phys. Rev. X* 4:031015, doi 10.1103/PhysRevX.4.031015, arXiv:1402.3276. For a bipartite Markov process the joint system obeys the second law, and the entropy balance of one subsystem is modified by a mutual-information rate. CT7 already excludes the feedback case by citing this paper. The two-state inequality in §4 is that shape, proved from the rates of that sensor.
- **Barato and Seifert (2015)**, *Phys. Rev. Lett.* 114:158101, doi 10.1103/PhysRevLett.114.158101, arXiv:1502.05944. In a steady state, a relative uncertainty \(\varepsilon_{\mathrm{rel}}\) in a time-integrated current costs at least \(2k_BT/\varepsilon_{\mathrm{rel}}^2\), independent of the time used to produce that uncertainty. Equivalently \(\dot\Sigma\ge 2 j^2/D_{\mathrm{var}}\) with \(D_{\mathrm{var}}=\lim\mathrm{Var}(X_t)/t\). Gingrich, Horowitz, Perunov and England (2016), doi 10.1103/PhysRevLett.116.120601, tighten the large-deviation side; the check below uses the 2015 inequality only.
- **Barato, Hartich and Seifert (2014)**, *New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024. The learning-rate bound behind CT7. CT7 is **PRIOR ART** in this note: holding mean squared error \(D\) on a random walk of variance rate \(\sigma^2\) dissipates at least \(kT\,\sigma^2/(2D)\), and with stake \(w\) the sum is at least \(\sigma\sqrt{2kTw}\). The square root is rechecked as arithmetic (\(3.80131557\) against \(3.80131556\) at \(\sigma=1.7\), \(w=2.5\), \(kT=1\)). It is not re-derived.
- **Lan, Sartori, Neumann, Sourjik and Tu (2012)**, *Nat. Phys.* 8:422, doi 10.1038/nphys2276. An energy-speed-accuracy tradeoff in sensory adaptation. The prefactor is not copied. The shape is the same fact the uncertainty relation makes quantitative: precision and speed cost dissipation. It is not a constant \(h\).
- **Sartori, Granger, Lee and Horowitz (2014)**, *PLoS Comput. Biol.* 10:e1003974, doi 10.1371/journal.pcbi.1003974, arXiv:1404.1027. Adaptation costs tracked by the information the sensor holds about its environment. Same family. Not re-derived.
- **Mehta and Schwab (2012)**, *PNAS* 109:17978, doi 10.1073/pnas.1207814109, arXiv:1203.5426. For a two-component Berg–Purcell network, learning a concentration requires breaking detailed balance, and more learning costs more energy. The abstract's qualitative statement is what is used. No formula is taken from the paper.
- **Govern and ten Wolde (2014)**, *Phys. Rev. Lett.* 113:258102, doi 10.1103/PhysRevLett.113.258102. Energy dissipation and noise correlations in biochemical sensing.
- **Ouldridge, Govern and ten Wolde (2017)**, *Phys. Rev. X* 7:021004, doi 10.1103/PhysRevX.7.021004. Thermodynamic cost of computational copying. **Ouldridge and ten Wolde (2017)**, *Phys. Rev. Lett.* 118:158103, doi 10.1103/PhysRevLett.118.158103. Costs of making and destroying persistent polymer copies. A copy has a floor. A design that does not copy does not pay it.
- **Schnakenberg (1976)**, *Rev. Mod. Phys.* 48:571, doi 10.1103/RevModPhys.48.571, and **Seifert (2012)**, *Rep. Prog. Phys.* 75:126001, doi 10.1088/0034-4885/75/12/126001. The entropy-production sum in §1.
- **Duncan (1970)**, *SIAM J. Appl. Math.* 19:215, doi 10.1137/0119020. The continuous-time information rate behind PD7. Not re-used.
- **Tatikonda, Sahai and Mitter (2004)**, doi 10.1109/TAC.2004.834430, and the rate-distortion line already in Theorem S1 and PD1. Causal reading of the world. Not re-derived.
- **Ito and Sagawa (2013)**, *Phys. Rev. Lett.* 111:180603, doi 10.1103/PhysRevLett.111.180603. Information thermodynamics on causal networks. The joint-versus-marginal caution: a bound on a part is not a bound on the sum. Used only at that level.

CT4, CT7, Theorem S1, PD1–PD7, and FLOOR.md stay as they are. This note assembles them with the layer question. The assembly is the claim. The ingredients are not.

## 4. The two-state sensor

**Model (PROVED (in-model) from here through the closed forms).** \(X\in\{0,1\}\) flips at rate \(\gamma\) each way. The memory \(M\in\{0,1\}\) flips toward \(X\) at rate \(\alpha_c\) and away from \(X\) at rate \(\alpha_e\), with \(\alpha_c>\alpha_e>0\). The four-state chain is lumpable by symmetry. With \(Z=\alpha_c+\alpha_e+2\gamma\),

\[
P(M\neq X)=\frac{\alpha_e+\gamma}{Z},\qquad
P(X{=}0,M{=}0)=\frac12\frac{\alpha_c+\gamma}{Z}.
\]

The medium entropy-production rate of the memory edges is

\[
\dot Q=kT\cdot\frac{\gamma(\alpha_c-\alpha_e)}{Z}\ln\frac{\alpha_c}{\alpha_e}.
\]

*Proof.* The net corrective flux on one memory pair is \((\gamma/2)(\alpha_c-\alpha_e)/Z\). Two pairs, each contributing that flux times \(\ln(\alpha_c/\alpha_e)\), give the display. The signal edges have equal forward and backward rates, so they add nothing to this sum. The generator's stationary mass matches the display to \(10^{-12}\) at \((\alpha_c,\alpha_e,\gamma)=(4,0.5,1)\). □

**Information flow (PROVED (in-model)).** Memory jumps change \(I(M;X)\) at rate

\[
\dot I=\frac{\gamma(\alpha_c-\alpha_e)}{Z}\ln\frac{\alpha_c+\gamma}{\alpha_e+\gamma}.
\]

*Proof.* \(I(M;X)=\ln 2-h(\varepsilon)\) with \(\varepsilon=P(M\neq X)\) and \(h\) the binary entropy in nats. A correction multiplies the odds \((1-\varepsilon)/\varepsilon\) into the posterior; an error multiplies the reciprocal. The difference of the two one-way fluxes is the net corrective flux above, and \((1-\varepsilon)/\varepsilon=(\alpha_c+\gamma)/(\alpha_e+\gamma)\). □

**Proposition IP-flow (PROVED (in-model)).** \(\dot Q\ge kT\,\dot I\), with equality in the limit \(\gamma/\alpha_e\to 0\) at fixed \(\alpha_c/\alpha_e>1\).

*Proof.* The prefactors match, and \(\alpha_c/\alpha_e\ge(\alpha_c+\gamma)/(\alpha_e+\gamma)\) because \((\alpha_c/\alpha_e)\cdot(\alpha_e+\gamma)/(\alpha_c+\gamma)-1=\gamma(\alpha_c-\alpha_e)/(\alpha_e(\alpha_c+\gamma))\ge 0\). The ratio of the logarithms tends to 1 as \(\gamma\to 0\). □

At \((4,0.5,10^{-4})\) the ratio \(\dot I/\dot Q\) is \(0.999915852256\). At \((4,0.5,5)\) it is \(0.236831127602\). At the reference point \((4,0.5,1)\), \(\dot Q=1.11969929167\), \(\dot I=0.64829304848\), \(\varepsilon=0.230769230769\), \(I(M;X)=0.152943038171\).

**Proposition IP-ray (PROVED (in-model)).** Fix \(\gamma>0\) and a Hamming error \(\varepsilon\in(0,1/2)\). On the designs that achieve that error, \(\dot Q\) has a positive infimum and no finite supremum. \(I(M;X)=\ln 2-h(\varepsilon)\) is constant on that set.

*Proof.* Set \(\rho=\alpha_c/\alpha_e>(1-\varepsilon)/\varepsilon\) and \(\alpha_e=\gamma(1-2\varepsilon)/(\varepsilon(\rho+1)-1)\). The error identity is then \(\varepsilon\), by algebra. As \(\rho\to\infty\), \(\alpha_c\to\gamma(1-2\varepsilon)/\varepsilon\) and \(\alpha_e\to 0\), so

\[
\dot Q\sim kT\cdot\frac{\gamma\alpha_c}{\alpha_c+2\gamma}\ln\rho\to\infty.
\]

The mutual information of a symmetric binary channel depends on the error alone. □

At \(\varepsilon=0.2\), \(\gamma=1\), \(kT=1\), the coefficient of \(\ln\rho\) is \(0.6\). At \(\ln\rho=40\) the heat is \(24\), and the grid minimum on the same ray family is \(0.831836613672\). The information is \(0.192744757022\) at both ends.

This is the efficiency gap in one line. Write \(\eta=Q_{\min}(D)/Q\le 1\). On this family \(\eta\) can be driven below any positive number at fixed distortion and fixed mutual information, by a futile affinity: rare spontaneous errors, a large log rate ratio, and the same Hamming error. A lower bound does not determine the cost. The distance from the floor is the binding ratio \(\beta_{\mathrm{phys}}\) already defined in FRAMEWORK §3.11. This model is a case where that ratio is not bounded.

**TUR, checked, not re-proved.** On the reference sensor the net corrective current has mean \(0.53846154\) (matches the flux) and variance per unit time \(0.603095\). The uncertainty bound is \(0.961509400505\), below the heat \(1.11969929167\). At \(\gamma=0.05\) the heat is \(0.079109189086\), the flow is \(0.075955854202\), and the uncertainty bound is \(0.059950010756\). The sum of the flow and the uncertainty bound is \(0.1359\), above the heat. Both inequalities are true. Their sum is not a lower bound. The forced combination is the maximum of the applicable bounds, unless a decomposition writes the entropy production as a sum of nonnegative pieces that are bounded one by one.

**Still's identity is not this heat.** For an equilibrated binary memory of gap \(\varepsilon=1.5\,kT\) and a signal that flips with probability \(0.3\), Still's difference is \(0.185466009664\) and equals \(h(\varepsilon_{\mathrm{next}})-h(q)\), as the chain rule requires. The quench-and-relax heat, paid only on flips, is \(0.3\cdot\varepsilon\cdot\tanh(\varepsilon/2)=0.285817028574\). Same sensor family, two different functionals. The one-step Still identity is an identity inside their free-energy split. It is not the housekeeping heat of the continuous-time sensor, and this note does not pretend the numbers coincide.

## 5. What is forced, in physical units

**Theorem IP-bound (PROVED (in-model) for class P restricted to the two-state family; the named inequalities are PRIOR ART).**

For every design in the family, with \(kT\) restored,

\[
\dot Q\ \ge\ kT\cdot\dot I,
\]

and \(\dot Q\) is at least the Barato–Seifert bound on any current of that chain. The task error obeys \(\mathbb{E}[\ell]\ge D_{\mathrm{IB}}(I_{\mathrm{pred}})\) by CT4 and Theorem S1, which are not re-proved. The combined lower bound on a sum of dissipation and task loss is therefore

\[
\dot Q+w\,\mathbb{E}[\ell]\ \ge\ \inf\big(kT\cdot\dot I+w\,D\big),
\]

where the infimum is over pairs \((\dot I, D)\) the family can reach, and \(w\) is supplied. CT7 is the random-walk case of the same pattern, with \(\dot I\) replaced by the rate \(\sigma^2/(2D)\) a tracker must buy to hold the error, and with the price per nat set to \(kT\).

The prices this theorem supports:

- \(kT\) per nat per unit time of information flow, in this model, as a floor on \(\dot Q/kT\).
- \(kT\) per nat of Still's instantaneous nonpredictive information, per signal update, as published.
- \(kT\) per nat on the sum of measurement and erasure for one measurement operation, as published by Sagawa and Ueda, not as a second term.
- \(2kT/\varepsilon_{\mathrm{rel}}^2\) of integrated dissipation for a current held to relative uncertainty \(\varepsilon_{\mathrm{rel}}\).

A rental \(\kappa I_{\mathrm{stock}}\) with \(\kappa\ge kT/\tau\) is the FLOOR.md accounting convention once a turnover time \(\tau\) is chosen. The second law does not choose \(\tau\). In a world whose variance diverges, PD6 already shows that the raw stock cannot be the viability term. Nothing here reverses that.

## 6. What is not forced

**Separate acquisition \(A\).** Sagawa and Ueda bound measurement and erasure together. Adding a Landauer price on erasure and a second price \(c\ge kT\) on the same nats double-counts. The Shannon note already marks S-A, the inequality \(A\ge c\cdot r\), as an assumption. This note agrees, and does not derive S-A. At the reference sensor the heat rate is \(1.12\,kT\) per unit time while \(I(M;X)\) is \(0.153\) nats. Those are a rate and a stock. Charging \(kT\) times the stock every unit of time, and charging \(kT\) times the flow on top, is not a theorem. The check that flow plus the uncertainty bound already overshoots the heat is the rate-against-rate version of the same refusal.

**Linking \(L\).** Ouldridge, Govern and ten Wolde, and Ouldridge and ten Wolde, give a floor for a physical copy. The floor applies when a copy is made. It does not put \(L\) into the cost of a design that does not share, and it does not fix a linear price on a sharing coordinate for every design. **Conditional floor. Not a universal summand.**

**The ruin cap.** None of these inequalities is a statement about a reserve hitting zero. A large-deviation bound on a current is a different object from the lifetime-ruin constraint. THEORY already separates CT22 and CT25. The cap stays an assumption, as GF3 (R-b) and GB5 say.

**The gross stock as the thing with price \(\kappa\).** Lemma IP-chain and the sticky-memory numbers: the past stock and Still's instantaneous memory differ. The ray proposition: even \(I(M;X)\), which is Still's instantaneous memory for this symmetric sensor, does not determine \(\dot Q\).

**A constant \(h\) per layer.** Section 7.

## 7. Layers, one joint memory

Chad's question: analyze layers one by one, or all together through the joint information. The bound uses the joint state. A per-layer price appears only when the mechanisms are thermodynamically separate, and then it is not a constant.

**Lemma IP-joint (PROVED).** Let \(M=(M_1,\ldots,M_K)\). If the \(M_i\) are conditionally independent given the trajectory of \(X\), then

\[
I(M;X_{\le t}\mid X_{>t})\ \le\ \sum_{i=1}^K I(M_i;X_{\le t}\mid X_{>t}),
\]

with equality if and only if the \(M_i\) are independent given the future.

*Proof.* The conditional mutual information is \(H(M\mid\mathrm{future})-H(M\mid\mathrm{past},\mathrm{future})\). Conditional independence given the whole trajectory factors the second entropy into a sum. Subadditivity of entropy given the future, \(H(M\mid\mathrm{future})\le\sum H(M_i\mid\mathrm{future})\), bounds the first. □

Drop conditional independence and the inequality can reverse. If \(Z=M_1\oplus M_2\) with \(M_1,M_2\) independent fair bits, then \(I(M_1,M_2;Z)=\ln 2\) and each marginal mutual information is \(0\) (computed, not assumed). A joint memory can hold information no layer holds alone. Summing per-layer informations is then too small, not too large. The joint object is the one that enters Still's difference and the information flow, because both are functionals of the memory state that is actually coupled to the bath.

**Separate mechanisms add heat (PROVED (in-model)).** Two conditionally independent copies of the reference sensor, on one signal, dissipate \(2.23939858335\), twice one sensor. The joint information is \(0.23074218524\), below \(2\times 0.152943038171\). The second copy adds \(0.077799147069\) nats and a full extra heat of \(1.11969929167\). Redundant trackers of one process pay twice for a sublinear information increment.

The same split on a linear diffusion, three coordinates \((X,M_1,M_2)\) with a common signal and two independent baths: the partial entropy productions add (\(3.696780893\) each, sum \(7.393561786\)), and the joint information \(0.457209911969\) is below twice the one-memory information \(0.392869983694\). Three independent worlds, three independent memories, with modes \((a,\lambda,v,D)=(0.5,1,1,0.2)\), \((1.5,3,0.8,0.4)\), \((4,2,1.2,0.5)\): entropy production \(10.7938070984\) and information \(0.855418580327\), each the sum of the three single-mode values. Addition of the cost is the independence of the mechanisms. Addition of the information is the independence of the worlds.

**One tracker of a sum (PROVED (in-model), one comparison).** Two independent telegraphs, loss the squared error of an estimate of the sum. One ternary memory driven toward the sum, at \((\alpha_c,\alpha_e,\gamma)=(6,0.4,0.5)\), dissipates \(1.89691075322\) at mean squared error \(0.238985868662\). Two specialized binary sensors at the same rates dissipate \(2.04933528732\) at mean squared error \(0.243243243243\). Weakening the joint drive to \((1.2,1.0,0.5)\) drops that one layer's heat to \(0.008275328830\). So:

- A constant \(h\) is not the heat of a layer. One and the same \(K=1\) device moves from \(0.0083\) to \(1.90\) with the drive.
- Separate mechanisms add. A joint mechanism that can write the statistic the loss actually depends on pays once. That is CORE's sentence, read on this generator: one tracker is the right object for a single process; a second mechanism pays when it carries a component the first cannot write. LAYER_LIFETIME's joint-reset inequality is about lump costs \(k_i\) and is not re-derived. The information version proved here is Lemma IP-joint: under conditional independence the joint nonpredictive information is at most the sum of the layer values, so a joint Still floor is at most the sum of the separate floors. A lower floor is not a lower heat. The heat comparison is the numerical point above, not a general dominance theorem.

**What replaces \(hK\), if anything.** Not a constant. If each layer is its own driven mechanism, the forced object is \(\sum_i \dot Q_i\), and each \(\dot Q_i\) is at least that mechanism's information flow and at least its uncertainty bound. Those floors depend on the precision and the speed of that mechanism. If the layers are coordinates of one joint mechanism, there is one entropy production and one joint information. Replacing \(hK\) by either of those is a different cost from the master equation. Keeping \(hK\) is an assumption about a maintenance charge that does not vary with precision. The sensor does not have that charge.

## 8. The tangent, and why \(J\) is not it

**Proposition IP-tangent (PROVED (in-model)).** Let \(\mathcal F\) be the set of \((\dot Q, D)\) attained by the two-state family as the drive \(F=\ln(\alpha_c/\alpha_e)\) and the speed \(r\), with \(\alpha_c=r e^{F/2}\) and \(\alpha_e=r e^{-F/2}\), range over a grid (\(F\in[0.3,6]\), \(r\in[0.05,30]\), 40 by 40, \(\gamma=1\)). The support function \(\inf_{(\dot Q,D)\in\mathcal F}(\dot Q+w D)\) selects a point on that set. At \(w=8\) the selected error is \(0.173927642272\) and the heat is \(1.05346454035\).

On the same grid, \(\kappa I(M;X)+h+w D\) at \(\kappa=1.5\), \(h=0.4\), \(w=8\) selects error \(0.004749003213\), heat \(5.94301196144\), information \(0.663003156857\). The cheapest heat among grid points with error no worse than that is \(5.79970450991\). The master-equation stand-in picks a different design. At the design it picks, the heat happens to sit \(2.5\%\) above the floor of that error. The large gap is the ray of §4, not this particular grid point: at error \(0.2\) the heat runs from \(0.832\) up without a ceiling, while \(I\) does not move.

**What "\(J\) is the tangent of the physical frontier" would mean, and why it is not proved.** If the achievable set of (dissipation, task loss) is convex and free disposal is allowed, every supported point minimizes \(\dot Q+w\,\mathbb{E}[\ell]\) for some \(w\ge 0\). That is the support-function fact already in Theorem S2, applied to these two coordinates. It is **PROVED (in-model)** as that convex-analysis statement, and it is not a new theorem. It becomes the master equation only if, in addition:

1. the coordinates are \(I_{\mathrm{mem}}\), \(K\), \(\mathbb{E}[\ell]\), \(A\), and \(L\), rather than information flow, Still's difference, and the mechanism entropy productions;
2. the design achieves the floor (\(\eta=1\)), or the prices are inflated to the actual spend, which is an empirical binding ratio and not fixed by the rates;
3. \(w\) is the conversion the system's books use;
4. ruin is a half-space cap rather than a traded coordinate.

None of (1)–(4) is a consequence of §4 or §5. **FALSE**, as a claim about this \(J\): "the master equation is the Lagrangian of the physical frontier." The witness is the pair of argmin errors \(0.1739\) and \(0.00475\).

## 9. Selection, and what is still assumed

Physics cuts the feasible set. It says which \((\dot Q, D)\) cannot occur. Lemma LY, under H1–H3, puts a growth-maximizing lineage on the Pareto front of a bad vector that the lemma does not choose. GF2 already says a floor that mentions a slot does not make retention decrease in that slot. A dissipation floor is a floor. H3, the partial of offspring in that coordinate with the other coordinates held fixed, is still a budget assumption. GB6 stays **FALSE** for "from first principles."

The combination that yields the master equation is exactly this, and no shorter:

1. An outer bound on dissipation, in the coordinates of §5, with efficiency \(\eta\le 1\) and, in the sensor, \(\eta\) able to be arbitrarily small. **This note.**
2. A conversion \(w\) from task loss into the same currency. **Assumed** (P-L).
3. Selection on the non-dominated part of whichever bad vector enters offspring. **Lemma LY, assumed H1–H3.** If the map is log-linear, corollary LY-c gives a nonnegative linear cost in growth units. That cost is not expected currency. V2.
4. Still assumed, and not supplied by (1)–(3): the master equation's coordinates, linear prices at or above the floors, risk-neutral expectation, and the half-space ruin cap. GF3 (R-a), (R-b), (R-c). The term list is not a fourth clause of that iff. It remains an input, as the growth bridge says.

**The derivation chain's weakest links are not removed.** Link 1, the objective, is still the objective. What this route adds is a refusal: the second law does not fill that objective in. Links 2 through 7 are untouched. H3 is untouched. The exogenous-world link is the hypothesis P-X this whole note sits inside; it is not discharged. Joint achievability of the information floor (Shannon §3, efficiency \(0.9574\) on one Gauss–Markov world) is a different gap, between an information floor and a Kalman design. It is not the thermodynamic efficiency \(\eta\) of §4.

A selected lineage that minimizes dissipation plus weighted error, at \(\eta=1\), on the coordinates of §5, with H3 true for those coordinates and with no ruin cap, would sit on the physical tangent. That sentence assumes the coordinate list, the efficiency, the weight, and H3. It is not the master equation.

## 10. Checks

`theory/info_physics_checks/info_physics_checks.py`. Thirty-seven checks, FAILS 0. The numbers in §§2–8 are the numbers the script prints.

Ornstein–Uhlenbeck, one mode, \(a=1\), \(\lambda=2\), signal variance \(1\), memory diffusion \(0.3\), \(kT=1\):

\[
C_{xm}=\frac{\lambda v}{a+\lambda},\qquad
\mathbb{E}[(M-X)^2]=\frac{a v}{a+\lambda}+\frac{D}{\lambda}=0.483333333333,
\]

partial entropy production \(3.25041459370\), mutual information \(0.392869983694\). An equilibrium memory, force \(-\lambda M\) and variance \(D/\lambda\), has partial entropy production \(0\) by algebra: the drift and the score cancel. A path simulation (seed 7, step \(2\cdot 10^{-3}\), \(2\cdot 10^4\) steps) gives Sekimoto heat rate \(4.43261155339\) for the driven memory and \(-0.008333582889\) for the equilibrium memory. The path integral and the Fokker–Planck partial entropy production have the same sign. They are not claimed to be the same number. The exogenous signal makes the stochastic-integral convention a separate hypothesis, and this note does not add it.

The Gaussian mutual information \({\textstyle\frac12}\ln(C_{xx}C_{mm}/\det C)\) is the usual formula for two jointly normal scalars. It is not Duncan's theorem and not a new identity.

## 11. Open, and what was not proved

- **IP7, OPEN.** Whether any system that qualifies under THEORY §3 has a binding ratio near 1, so that these floors rather than niche prices set the design. FRAMEWORK §3.11 and OPEN_WORK T10 already own that measurement. This row is not a preregistration and not a lock.
- The two-state family and the linear diffusion are the models. A general bipartite chain has the Horowitz–Esposito shape; the closed form is not claimed past the sensor, the sum-tracker, and the Gaussian.
- Equality of Sekimoto heat and the partial entropy production for an exogenous diffusion is not proved.
- No theorem here covers a system that changes its world.
- The ruin cap, \(L\) as a universal summand, a constant \(h\), and a stacked read price remain assumptions. Calling them open problems would overstate how close the physics came. They are absent from the bound, not half-derived.
- **CONJECTURE, not used.** A turnover time measured from the memory's correlation might turn the flow floor into a rental on Still's instantaneous memory, inside a factor that stays bounded for efficient sensors. The ray proposition says the factor is not bounded for inefficient ones. The conjecture is only about the minimizing branch. It is not a theorem, and \(J\) would still need the coordinate identification of §8.

## 12. References

Landauer, R. 1961. Irreversibility and heat generation in the computing process. *IBM J. Res. Dev.* 5:183. doi 10.1147/rd.53.0183.

Schnakenberg, J. 1976. Network theory of microscopic and macroscopic behavior of master equation systems. *Rev. Mod. Phys.* 48:571. doi 10.1103/RevModPhys.48.571.

Duncan, T. E. 1970. On the calculation of mutual information. *SIAM J. Appl. Math.* 19:215. doi 10.1137/0119020.

Sagawa, T., and Ueda, M. 2009. Minimal energy cost for thermodynamic information processing: measurement and information erasure. *Phys. Rev. Lett.* 102:250602. doi 10.1103/PhysRevLett.102.250602.

Sagawa, T., and Ueda, M. 2011. Erratum. *Phys. Rev. Lett.* 106:189901. doi 10.1103/PhysRevLett.106.189901.

Esposito, M., and Van den Broeck, C. 2011. Second law and Landauer principle far from equilibrium. *EPL* 95:40004. doi 10.1209/0295-5075/95/40004.

Still, S., Sivak, D. A., Bell, A. J., and Crooks, G. E. 2012. Thermodynamics of prediction. *Phys. Rev. Lett.* 109:120604. doi 10.1103/PhysRevLett.109.120604.

Sagawa, T., and Ueda, M. 2012. Fluctuation theorem with information exchange. *Phys. Rev. Lett.* 109:180602. doi 10.1103/PhysRevLett.109.180602.

Lan, G., Sartori, P., Neumann, S., Sourjik, V., and Tu, Y. 2012. The energy–speed–accuracy trade-off in sensory adaptation. *Nat. Phys.* 8:422. doi 10.1038/nphys2276.

Mehta, P., and Schwab, D. J. 2012. Energetic costs of cellular computation. *PNAS* 109:17978. doi 10.1073/pnas.1207814109.

Seifert, U. 2012. Stochastic thermodynamics, fluctuation theorems and molecular machines. *Rep. Prog. Phys.* 75:126001. doi 10.1088/0034-4885/75/12/126001.

Ito, S., and Sagawa, T. 2013. Information thermodynamics on causal networks. *Phys. Rev. Lett.* 111:180603. doi 10.1103/PhysRevLett.111.180603.

Barato, A. C., Hartich, D., and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.

Govern, C. C., and ten Wolde, P. R. 2014. Energy dissipation and noise correlations in biochemical sensing. *Phys. Rev. Lett.* 113:258102. doi 10.1103/PhysRevLett.113.258102.

Horowitz, J. M., and Esposito, M. 2014. Thermodynamics with continuous information flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015.

Sartori, P., Granger, L., Lee, C. F., and Horowitz, J. M. 2014. Thermodynamic costs of information processing in sensory adaptation. *PLoS Comput. Biol.* 10:e1003974. doi 10.1371/journal.pcbi.1003974.

Tatikonda, S., Sahai, A., and Mitter, S. 2004. Stochastic linear control over a communication channel. *IEEE Trans. Automat. Control* 49:1549. doi 10.1109/TAC.2004.834430.

Barato, A. C., and Seifert, U. 2015. Thermodynamic uncertainty relation for biomolecular processes. *Phys. Rev. Lett.* 114:158101. doi 10.1103/PhysRevLett.114.158101.

Parrondo, J. M. R., Horowitz, J. M., and Sagawa, T. 2015. Thermodynamics of information. *Nat. Phys.* 11:131. doi 10.1038/nphys3230.

Gingrich, T. R., Horowitz, J. M., Perunov, N., and England, J. L. 2016. Dissipation bounds all steady-state current fluctuations. *Phys. Rev. Lett.* 116:120601. doi 10.1103/PhysRevLett.116.120601.

Ouldridge, T. E., Govern, C. C., and ten Wolde, P. R. 2017. Thermodynamics of computational copying in biochemical systems. *Phys. Rev. X* 7:021004. doi 10.1103/PhysRevX.7.021004.

Ouldridge, T. E., and ten Wolde, P. R. 2017. Fundamental costs in the production and destruction of persistent polymer copies. *Phys. Rev. Lett.* 118:158103. doi 10.1103/PhysRevLett.118.158103.

Still, S. 2020. Thermodynamic cost and benefit of memory. *Phys. Rev. Lett.* 124:050601. doi 10.1103/PhysRevLett.124.050601.
