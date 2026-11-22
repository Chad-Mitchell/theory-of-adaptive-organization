# Dissipation bounds the cost of a model, and does not produce the master equation

*Sunday 22 November 2026. Draft. A self-check, not an independent review. The hypothesis sentence is unchanged. No locked preregistration file is edited. Checks: `theory/info_physics_checks/info_physics_checks.py`, run at `nice -n 19` (37 checks, FAILS 0). DOIs below were resolved on the Crossref API on 22 November 2026 (`theory/info_physics_checks/crossref.out`).*

Labels: **PROVED** (a proof is on this page, under the assumptions named with it), **PROVED (in-model)** (the same, inside a stated model; it says nothing by itself about nature), **PRIOR ART** (published, credited, not claimed here), **CONJECTURE**, **OPEN**. A lower bound is not a derivation of the cost.

## 0. The question, and the answer

The master equation is

\[
J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\qquad\text{subject to}\quad P(\mathrm{ruin})\le\varepsilon .
\]

Selection does not produce that list, the cap, or the linear prices. Lemma LY gives Pareto in a bad vector that is handed to it. The growth bridge keeps a variance penalty and still takes the term list as an input. The question here is whether the physics of a system that stores a model and acts on it forces the terms instead.

**Answer.** Physics forces a lower bound on the free-energy rate, in coordinates that are not the master equation's coordinates. In the telegraph solved below, the bound is the information flow, tight when the memory is fast at the minimal affinity, and missable by an arbitrarily large factor at fixed task error. The proposed cost is the medium heat, with that floor, plus \(w\) times the loss. Ruin and linking stay outside. The master equation is not that cost. Section 8a states the five conditions under which the floor is the tangent, and which of them are proved.

What is forced, and what is not:

| Object | Status | Price, where one exists |
|---|---|---|
| Nonpredictive information \(I(s_t;x_t)-I(s_t;x_{t+1})\), per signal update | **PRIOR ART** (Still, Sivak, Bell and Crooks 2012). One-step equality in their accounting; the sum over a protocol is a lower bound | \(kT\) per nat of that difference, per update |
| Information-flow rate of a driven memory | **PROVED (in-model)** for the two-state sensor below. The shape, a subsystem entropy balance modified by a mutual-information rate, is **PRIOR ART** (Horowitz and Esposito 2014) | \(kT\) per nat per unit time of the flow. A rental \(\kappa\) on a stock needs a turnover time, the accounting step already in `core/bridge_2026-11-21/FLOOR.md` |
| Measurement work and erasure work | **PRIOR ART** (Sagawa and Ueda 2009, erratum 2011). They bound the sum | one floor on the sum, not two stacked prices |
| Precision of a steady current | **PRIOR ART**. Barato and Seifert 2015 proved it inside linear response and for unicyclic networks. This sensor is multicyclic with affinity \(\ln 8\), so the relation used on it is Gingrich, Horowitz, Perunov and England 2016 | total entropy production at least \(2kT/\varepsilon_{\mathrm{rel}}^2\) over the window. A lower bound on the same heat, not a constant per layer |
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
- **Barato and Seifert (2015)**, *Phys. Rev. Lett.* 114:158101, doi 10.1103/PhysRevLett.114.158101. They prove that a relative uncertainty \(\varepsilon_{\mathrm{rel}}\) costs at least \(2k_BT/\varepsilon_{\mathrm{rel}}^2\) inside linear response for any network, and for a unicyclic network beyond linear response. The constant \(2\) is theirs. The reference sensor has several cycles and affinity \(\ln(\alpha_c/\alpha_e)=\ln 8\), outside that proved set.
- **Gingrich, Horowitz, Perunov and England (2016)**, *Phys. Rev. Lett.* 116:120601, doi 10.1103/PhysRevLett.116.120601. The uncertainty relation for a general steady-state Markov jump process, as the small-fluctuation corollary of their large-deviation bound. The numerical check below is a check of that corollary. It is not a re-proof.
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

CT4, CT7, Theorem S1, PD1–PD7, and FLOOR.md stay as they are. The two-state closed forms in §4, the stake table in §8, and the linear-spring floor in §8a are the calculations made here. The refusals are older, and this note points at them:

- Still's equality and the protocol inequality: `core/bridge_2026-11-21/FLOOR.md`.
- Heat at least \(kT\) times an information flow, for the Kalman–Bucy filter, with the random-walk limit \(\sigma^2/(2D)\): `theory/INTERNAL_MODEL.md` (Mitter and Newton 2005; Horowitz and Sandberg 2014) and CT7. The two-state formula is not in those notes.
- Measurement and erasure as one sum, and S-A left as an assumption: `theory/SHANNON_2026-11-21.md` and `CORE.md`.
- The gross stock ruled out as the viability coordinate when the variance diverges, and Still's difference distinguished from that stock: `theory/GENERAL_FORM.md` and PD6.
- No proved constant upkeep inside the information floor: the Shannon note's memoryless counterexample, \(K=0\) with \(I_{\mathrm{mem}}>0\).
- The cap and the term list as inputs: GF3, GB5, `theory/GROWTH_BRIDGE.md`.
- One tracker for one process, and a joint reset against a stack: `CORE.md` and `theory/LAYER_LIFETIME_2026-11-21.md`.
- A slow drive whose dissipation per cycle falls while the memory still holds information: `theory/SCALE_ENDS.md` SE3, to \(0.026\,kT\) at \(\omega/\gamma=0.01\). That is the quasi-static direction. The ray in §4 is the other direction, at fixed \(\gamma>0\): no ceiling. Barato, Hartich and Seifert 2014 is the same pair of facts for a bacterium, and their receptor can learn while the cell's own dissipation is zero because another bath pays. Horowitz and Esposito 2014, their subsystem balance, is what makes "which bath" a hypothesis rather than a slogan.

The assembly of those refusals with the two-state floor and the stake table is the claim. The ingredients listed above are not.

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

At \(\varepsilon=0.2\), \(\gamma=1\), \(kT=1\), every design with that error has heat \(0.6\ln\rho\) and flow \(0.6\ln 4\). The infimum, attained as the memory rates diverge at the minimal affinity \(\rho\downarrow 4\), is

\[
0.6\ln 4=0.831776616672\,kT
\]

per unit time. At \(\ln\rho=40\) the heat is \(24\). The information \(0.192744757022\) depends only on the error. A 600-point ray that starts at \(\rho=4\times 1.0001\) has minimum \(0.831836613672\), above the infimum. That grid minimum is not the floor.

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

**Lemma IP-joint (PROVED).** Let \(M=(M_1,\ldots,M_K)\). The object is the conditional mutual information \(I(M;X_{\le t}\mid X_{>t})\), not Still's instantaneous gap. If the \(M_i\) are conditionally independent given the trajectory of \(X\), then

\[
I(M;X_{\le t}\mid X_{>t})\ \le\ \sum_{i=1}^K I(M_i;X_{\le t}\mid X_{>t}),
\]

with equality if and only if the \(M_i\) are independent given the future.

*Proof.* The conditional mutual information is \(H(M\mid\mathrm{future})-H(M\mid\mathrm{past},\mathrm{future})\). Conditional independence given the whole trajectory factors the second entropy into a sum. Subadditivity of entropy given the future bounds the first. □

Drop conditional independence and the inequality reverses, future included. Let \(M_2=M_1\oplus Z\) with \(M_1,Z\) independent fair bits, and let \(Y\) be a binary channel of \(Z\) with flip probability \(0.2\). Then \(I(M_1,M_2;Z\mid Y)=h(0.2)=0.500402423538\), and each marginal conditional mutual information is \(0\).

Still's gap on the sticky chain of §2 is a different functional: past excess \(0.112693\), Still gap \(0.073121\). Conditional independence given the present \(X_t\), which is stronger than conditional independence given the whole trajectory when the memories are sticky, would give \(H(M\mid X_t)=\sum_i H(M_i\mid X_t)\) and therefore Still's gap at most the sum, by subadditivity of \(H(M\mid X_{t+1})\). That identification is not the hypothesis of the lemma. This note does not claim that a joint Still floor is at most the sum of the layer Still gaps. It claims the conditional-mutual-information inequality above. A lower information number is not a lower heat.

Drop conditional independence and the inequality can reverse. If \(Z=M_1\oplus M_2\) with \(M_1,M_2\) independent fair bits, then \(I(M_1,M_2;Z)=\ln 2\) and each marginal mutual information is \(0\) (computed, not assumed). A joint memory can hold information no layer holds alone. Summing per-layer informations is then too small, not too large. The joint object is the one that enters Still's difference and the information flow, because both are functionals of the memory state that is actually coupled to the bath.

**Separate mechanisms add heat (PROVED (in-model)).** Two conditionally independent copies of the reference sensor, on one signal, dissipate \(2.23939858335\), twice one sensor. The joint information is \(0.23074218524\), below \(2\times 0.152943038171\). The second copy adds \(0.077799147069\) nats and a full extra heat of \(1.11969929167\). Redundant trackers of one process pay twice for a sublinear information increment.

The same split on a linear diffusion, three coordinates \((X,M_1,M_2)\) with a common signal and two independent baths: the partial entropy productions add (\(3.696780893\) each, sum \(7.393561786\)), and the joint information \(0.457209911969\) is below twice the one-memory information \(0.392869983694\). Three independent worlds, three independent memories, with modes \((a,\lambda,v,D)=(0.5,1,1,0.2)\), \((1.5,3,0.8,0.4)\), \((4,2,1.2,0.5)\): entropy production \(10.7938070984\) and information \(0.855418580327\), each the sum of the three single-mode values. Addition of the cost is the independence of the mechanisms. Addition of the information is the independence of the worlds.

**One tracker of a sum (PROVED (in-model), one comparison).** Two independent telegraphs, loss the squared error of an estimate of the sum. One ternary memory driven toward the sum, at \((\alpha_c,\alpha_e,\gamma)=(6,0.4,0.5)\), dissipates \(1.89691075322\) at mean squared error \(0.238985868662\). Two specialized binary sensors at the same rates dissipate \(2.04933528732\) at mean squared error \(0.243243243243\). Weakening the joint drive to \((1.2,1.0,0.5)\) drops that one layer's heat to \(0.008275328830\). So:

- A constant \(h\) is not the heat of a layer. One and the same \(K=1\) device moves from \(0.0083\) to \(1.90\) with the drive.
- Separate mechanisms add. A joint mechanism that can write the statistic the loss actually depends on pays once. That is CORE's sentence, read on this generator: one tracker is the right object for a single process; a second mechanism pays when it carries a component the first cannot write. LAYER_LIFETIME's joint-reset inequality is about lump costs \(k_i\) and is not re-derived. Lemma IP-joint bounds \(I(M;X_{\le t}\mid X_{>t})\), not Still's gap. The heat comparison is the numerical point above, not a general dominance theorem.

**What replaces \(hK\), if anything.** Not a constant. The bookkeeping is in §8a: separate baths add their heats, one bath has one flow, and a TUR bounds a bath's heat without becoming a second term.

## 8. The tangent, and why the master equation is not it

On this family \(I(M;X)=\ln 2-h(\varepsilon)\) depends only on the error, and a constant upkeep does not move an argmin. At stake \(w=8\) and \(\kappa=1\), the stock objective selects error \(0.004114465901\) whether the constant is \(0\) or \(10\). \(\kappa=1.5\) is not \(kT\). Setting \(\kappa=kT=1\) moves the stock objective further from the heat argmin, not onto it.

The heat argmin on the printed grid (\(F\in[0.3,6]\), \(r\in[0.05,30]\), 40 by 40) is error \(0.173927642272\), heat \(1.05346454035\), flow \(1.016069512896\), at the top edge \(r=30\). The price \(\kappa=w/\ln((1-\varepsilon)/\varepsilon)=5.1346464562\), with any constant upkeep, selects that same grid point. One stake, one grid, and a calibrated \(\kappa\) agree. That \(\kappa\) does not travel.

The efficient frontier, rates diverging at the minimal affinity, minimizes \(\dot Q_{\min}(\varepsilon)+w\varepsilon\) with \(\dot Q_{\min}(\varepsilon)=(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\). A least-squares fit of \(\kappa I(\varepsilon)+h\) to that floor on \(\varepsilon\in[0.02,0.45]\) (400 points) leaves a maximum residual \(0.617160\). The stock saturates at \(\ln 2\). The floor diverges as \(\varepsilon\to 0\). No fixed stock price plus a constant upkeep is the frontier.

| Stake \(w\) | Frontier error | Stock error at \(\kappa=5.134646\) |
|---|---|---|
| 2 | 0.379876 | 0.403835 |
| 8 | 0.167031 | 0.173928 |
| 20 | 0.063722 | 0.019936 |
| 50 | 0.022976 | 0.000059 |

At stake 20 the frontier sits at \(0.063722\) and the stock price matched to stake 8 sits at \(0.019936\).

The corrected objective \(kT\,\dot I+w\varepsilon\) equals \(\dot Q_{\min}+w\varepsilon\) on this family, because the flow is the floor. It is the Lagrangian of the efficient frontier. On the printed grid, which stops at speed 30, the flow objective selects error \(0.167570574149\) and the heat objective selects \(0.173927642272\). The gap is \(0.006357\). The heat objective charges the excess over the floor. The flow objective does not. Reaching the floor, which §4 already proves is available, makes them the same objective.

**FALSE**, as a claim about the master equation: it is the Lagrangian of the physical frontier. The witness is the residual \(0.617\) and the stake table, not the single pair of errors at \((\kappa,h)=(1.5,0.4)\). That pair only shows that one price vector is not the supporting price. The pair is still computed: at \(w=8\), \(\kappa=1.5\), \(h=0.4\), the stock objective selects error \(0.004749003213\).

## 8a. The physics-derived cost

Define, with ruin and linking left outside,

\[
J_{\mathrm{phys}}=\dot Q+w\,\mathbb{E}[\ell],\qquad \dot Q\ge kT\,\dot I,
\]

where \(\dot Q\) is the medium heat rate of the memory's bath and \(\dot I\) is the information flow into that memory. The floor objective \(kT\,\dot I+w\,\mathbb{E}[\ell]\) is a tangent of the physical frontier only under the five conditions below. Each is labeled with what is proved.

**Condition 1, equality at the operating design (PROVED for two families; the excess is named).** The support function of the achievable set uses \(\dot Q\). It equals \(kT\,\dot I+wD\) only on the boundary where \(\dot Q=kT\,\dot I\). Off that boundary the excess is a free coordinate, and §4 shows it can be arbitrarily large at fixed error and fixed mutual information.

*Telegraph.* At fixed error, \(\dot Q=kT\,\gamma(1-2\varepsilon)\ln\rho\) for every \(\rho>(1-\varepsilon)/\varepsilon\), so the infimum is the flow, attained as the rates diverge at the minimal affinity. Every minimizer of \(\dot Q+w\varepsilon\), in that closure, sits on the boundary. A finite-speed design pays the excess \(kT\,\gamma(1-2\varepsilon)\ln(\rho/\rho_\star)\).

*Linear spring on an Ornstein–Uhlenbeck world (PROVED (in-model)).* \(dX=-a X\,dt+\sqrt{2av}\,dW\), \(dM=-\lambda(M-X)\,dt+\sqrt{2D}\,dB\), \(kT=1\). The force on the memory is \(F=-(\lambda/D)(M-X)\). The Stratonovich heat rate into the memory's bath is

\[
\dot Q=\frac{\lambda^2}{D}\mathbb{E}[(M-X)^2]-\lambda.
\]

*Proof of the expectation.* The Ito drift contributes \(\lambda(\lambda/D)\mathbb{E}[(M-X)^2]\). The quadratic covariation of the force with \(dM\) contributes \(-\lambda\). At the reference \((a,\lambda,v,D)=(1,2,1,0.3)\) this is \(4.444444444444\). The path at seed 7 gives \(4.43261155\). The information flow at that point is \(1.194029850746\). The Fokker–Planck partial entropy production, \(3.25041459370\), is a third functional and can fall below the flow; it is not the heat used here.

At fixed error \(\varepsilon\), eliminate \(D\). The heat is \(\lambda\, a v/(\varepsilon(a+\lambda)-av)\), which decreases in \(\lambda\) and tends to \(av/\varepsilon\). The information flow of the same design has the same limit (the covariance calculation; the gap at \(\lambda=10^4\), \(a=v=1\), \(\varepsilon=0.2\), is \(0.003\)). So the fast-memory boundary is again \(\dot Q=kT\,\dot I\), and the floor is \(kT\,av/\varepsilon\), not the Kalman rate. PD7 and `theory/INTERNAL_MODEL.md` give the Kalman–Bucy inflow \(a(v-\varepsilon)/\varepsilon\) in these units. The difference is \(kT\,a\). This spring cannot reach that inflow. Equality is relative to the implementation.

Switching the spring off, \(M\) independent of \(X\), has heat \(0\) and error \(v\). That corner beats the spring when \(w\le 4a/v\). Both the heat floor and the flow floor see the same corner, so they still select the same design.

| Stake \(w\) | Ornstein–Uhlenbeck error, \(a=v=1\) | Heat floor |
|---|---|---|
| 2 | 1, the blind corner | 0 |
| 8 | 0.353553 | 2.828427 |
| 20 | 0.223607 | 4.472136 |
| 50 | 0.141421 | 7.071068 |

Minimizing \(kT\,(av/\varepsilon)+w\varepsilon\) and minimizing the heat floor plus \(w\varepsilon\) are the same arithmetic on this table. That is the numerical check the linear-Gaussian case adds: the two objectives trace one frontier, including the decision not to track.

**Condition 2, one stake (PROVED for these scalar errors; OPEN for a vector loss).** On the telegraph the flow is a function of \(\varepsilon\) alone, at fixed \(\gamma\). On the spring the floor \(av/\varepsilon\) is a function of \(\varepsilon\) alone. One \(w\) supports that curve. For \(K\) independent scalar errors and a loss that is their sum, the Lagrangian separates and the same \(w\) prices every mode. A loss that is not a function of the statistics that fix the flows is not covered. That case is **OPEN**.

**Condition 3, the memory's bath pays (PROVED for these two implementations; not for every coupling).** On the telegraph the signal edges have equal forward and backward rates, so the whole medium entropy production is on the memory edges. On the spring the Sekimoto integral is the memory bath, and it is at least the flow, with equality in the fast limit. SE3 and the Barato–Hartich–Seifert receptor are the other case: information can be held while this subsystem's dissipation falls toward zero, because another bath pays. A memory price equal to \(kT\,\dot I\) needs the memory's bath to be the one in the balance. That is an assumption about the wiring, discharged here only for the two models.

**Condition 4, layers (PROVED for the bookkeeping; the general coupling is OPEN).** Separate baths add their heats. On the efficient boundary,

\[
J_{\mathrm{phys}}=\sum_{i=1}^{K}\Big(kT\,\dot I_i(D_i)+w D_i\Big),
\]

with the blind corner available in each term, as in the table. One joint mechanism has one heat and one joint flow, and Lemma IP-joint does not turn that flow into a sum of Still gaps. No constant per layer survives. A TUR on a nonzero current of one bath is another lower bound on that bath's heat (Gingrich et al. for a jump process; the reference sensor is the check). It does not add a second price on top of the flow, and it is not \(h\). For \(K\) independent jump-process sensors the bound on the total is the sum of the per-sensor bounds, because the heats add. For one shared bath the same currents give only a maximum, not a sum. A theorem that a joint frontier lies below the sum of the marginal frontiers, past the additive case and the one sum-tracker comparison in §7, is **OPEN**.

**Condition 5, ruin and linking stay outside (a scope, not a derived cost).** \(J_{\mathrm{phys}}\) has no reserve and no copy. Ouldridge, Govern and ten Wolde, and Ouldridge and ten Wolde, bound the dissipation of a copy that is actually made. A design that does not copy does not pay them, and neither paper supplies a linear linking price on every design. The ruin cap is not a statement about this heat. Both stay out until a reserve, or a real copy, is in the model.

**How the master equation sits on \(J_{\mathrm{phys}}\).** This is a proposed replacement, recorded in OPEN_WORK. It is not a change to the equation in THEORY.

| Master-equation term | What physics puts in its place |
|---|---|
| \(\kappa I_{\mathrm{mem}}\) | \(kT\,\dot I\) on the efficient boundary: \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) for the telegraph, \(av/\varepsilon\) for the spring. Still's \(I(s_t;x_t)-I(s_t;x_{t+1})\) is the per-update functional, not this rate. The gross past stock is not the coordinate |
| \(hK\) | No constant. \(K\) separate baths contribute the sum above. One bath contributes one flow. A TUR precision cost, where the 2016 theorem applies, bounds that heat and does not survive as a second term |
| Read price inside \(A\) | Folded into the same heat for the continuously coupled sensor. A separate measurement-and-erasure operation is the Sagawa–Ueda sum, once, not a second price on the same nats |
| \(w\,\mathbb{E}[\ell]\) | Unchanged. \(w\) is still an input. \(kT\) does not set it |
| \(L\), and \(P(\mathrm{ruin})\le\varepsilon\) | Outside \(J_{\mathrm{phys}}\) |

**What physics plus Lemma LY now gives.** The frontier in \((\dot Q, \mathbb{E}[\ell])\), and at equality the scalarization \(kT\,\dot I+w\,\mathbb{E}[\ell]\). If H3 holds for those two coordinates, a growth-maximizing lineage sits on the non-dominated part of that frontier. That is \(J_{\mathrm{phys}}\) at equality. It is not \(\kappa I_{\mathrm{mem}}+hK+A+L\) under a ruin cap.

**What is still assumed.** H3. The stake \(w\). That the implementation in use is the efficient boundary, or that the books carry the excess rather than the floor. That the memory's bath is the one that pays, outside the two models. Risk-neutral expected currency rather than growth (V2). Ruin and linking, until they are modeled. The master equation's coordinates.

## 9. Selection, and what is still assumed

Physics cuts the feasible set. It says which \((\dot Q, D)\) cannot occur. Lemma LY, under H1–H3, puts a growth-maximizing lineage on the Pareto front of a bad vector that the lemma does not choose. GF2 already says a floor that mentions a slot does not make retention decrease in that slot. A dissipation floor is a floor. H3, the partial of offspring in that coordinate with the other coordinates held fixed, is still a budget assumption. GB6 stays **FALSE** for "from first principles."

The combination that yields the master equation is exactly this, and no shorter:

1. An outer bound on dissipation, in the coordinates of §5, with efficiency \(\eta\le 1\) and, in the sensor, \(\eta\) able to be arbitrarily small. **This note.**
2. A conversion \(w\) from task loss into the same currency. **Assumed** (P-L).
3. Selection on the non-dominated part of whichever bad vector enters offspring. **Lemma LY, assumed H1–H3.** If the map is log-linear, corollary LY-c gives a nonnegative linear cost in growth units. That cost is not expected currency. V2.
4. Still assumed, and not supplied by (1)–(3): the master equation's coordinates, linear prices at or above the floors, risk-neutral expectation, and the half-space ruin cap. GF3 (R-a), (R-b), (R-c). The term list is not a fourth clause of that iff. It remains an input, as the growth bridge says.

**The derivation chain's weakest links are not removed.** Link 1 is the master equation, and \(J_{\mathrm{phys}}\) is a proposed replacement, not that equation. The proposal is in OPEN_WORK. Links 2 through 7 are untouched. H3 is untouched. The exogenous-world link is the hypothesis P-X this whole note sits inside. Joint achievability of the information floor (Shannon §3, efficiency \(0.9574\) on one Gauss–Markov world) is a different gap. It is not the thermodynamic efficiency of §4.

A selected lineage that minimizes dissipation plus weighted error, at equality in conditions 1 and 3, on the coordinates of §8a, with H3 true for those coordinates and with no ruin cap, would sit on the physical tangent. That sentence assumes the wiring, the efficiency, the weight, and H3. It is \(J_{\mathrm{phys}}\). It is not the master equation.

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
- Condition 2 for a loss that is not a function of the statistics that fix the flows. **OPEN.**
- Condition 4 past the additive case and the one sum-tracker comparison. **OPEN.**
- A diffusion uncertainty relation as a per-layer price. The 2016 theorem is for jump processes. It is not applied to the spring.
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
