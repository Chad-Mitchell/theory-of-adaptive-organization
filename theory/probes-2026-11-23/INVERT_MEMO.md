# Inverting the problem: which cost is physics the minimum of?

*Monday 23 November 2026, America/New_York. Written against `main` `d592662` (read-only shallow clone, deleted after). Scratch memo, not a PR. `THEORY.md` untouched. No real-world data. A self-check, not an independent review. Labels: **PROVED (in-model)** inside a named class; **KNOWN** published and credited; **ELEMENTARY** a short consequence of a known result; **CONJECTURE**; **SPECULATION**. Every DOI below was resolved on api.crossref.org today (`checks/crossref.out`). Check scripts and outputs: `checks/` (hashes in `checks/SHA256SUMS`).*

> **[REVIEWER EDIT 2026-11-23]** Independent hostile review: `/workspace/gtao/reviews-indep-2026-11-23/INVERT_REVIEW.md`. Net changes: Theorem INV-E relabelled **KNOWN** (it is the Donsker–Varadhan / Holland / Fleming–Sheu variational formula for the principal eigenvalue, read in Nelson's variables); the real-time condition corrected; the repo-grep claim corrected (Ortega–Braun and Donsker–Varadhan are already cited in the repo); Prop. R relabelled KNOWN in substance; prior art added; the "6 digits" claim scoped. All five checks reproduce byte-identically; all 19 DOIs resolve.

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

## 0. Bottom line (plain words)

- **The inversion works, but only in imaginary time.** Take a noisy particle. Charge \(\hbar\) per nat for steering it away from free diffusion, and charge its potential energy as the stake. The cheapest long-run way to run it then costs exactly the quantum ground-state energy \(E_0\), and the cheapest design is Nelson's ground-state process (Theorem INV-E). **[REVIEWER EDIT 2026-11-23]** This is **KNOWN**, not new: it is the variational formula for the principal eigenvalue of \(-\tfrac{\hbar^2}{2m}\Delta+U\) (Donsker–Varadhan 1975; Holland 1978; Fleming 1977; Sheu 1984), written in Nelson's 1966 variables; the stationary version is the long-run (ergodic) control problem whose value is the principal eigenvalue (Sheu 1984). The "6 digits" compares \(E_0\) with \(\langle T\rangle+\langle U\rangle\) computed from the *same* eigenvector, so it is a consistency check of the grid, not a test; the independent check is the SDE time average, which agrees to about 1% (C2). Nothing selects \(\hbar\): any price \(\lambda\) with \(\sigma^2=\lambda/m\) gives the ground energy of the same operator with \(\lambda\) in place of \(\hbar\). \(\lambda=\hbar\) is a matching choice. On a finite horizon the same cost is Kappen–Todorov control, and its minimum is a free energy, \(-\hbar\ln Z\) (KNOWN). In the zero-noise limit it is classical least action in its Euclidean (imaginary-time) form (KNOWN).
- **Real time does not map.** ~~Ordinary least action is a minimum only when the potential is bounded above, and only before the first conjugate time.~~ **[REVIEWER EDIT 2026-11-23]** Corrected: by Jacobi's theorem, Hamilton's action is a minimum along a path only up to the first conjugate point (Gray & Taylor 2007). Bounded-above \(U\) is neither necessary (the harmonic well is unbounded above, yet its action is a true minimum for \(T<\pi/\omega\)) nor sufficient (\(U=\cos x\) is bounded above and has a conjugate point at \(\pi\) about its minimum; review check R3). Bounded-above \(U\) is what makes the real-time stake \(-U\) bounded below, i.e. what GTAO's nonnegative-term form (`THEORY.md:474`) needs; it is not a minimality condition. For a harmonic well the "cost" has no minimum after half a period (check C4). Real-time quantum mechanics (Nelson, Guerra–Morato) is a *stationary* point of an action whose osmotic term has the wrong sign to be a relative entropy. Any minimum of this cost is a positive reweighting of the reference process, so it can never show interference. The missing piece is exactly the factor \(i\) of the Wick rotation. That is known physics, not a gap we found.
- **GTAO's physical heat term is not the term that maps.** A particle held in a harmonic trap at equilibrium gives off zero heat, so GTAO's heat floor charges nothing. Its path relative entropy against free diffusion is still \(\omega/4\) per unit time (check C5b). **[REVIEWER EDIT 2026-11-23]** In general \(\omega/(4\gamma)\); C5b sets \(\gamma=1\). The number depends on the choice of reference: against the trap's own law it is 0. `CORE.md:80` already records the vanishing heat; only the KL contrast is added here. The term that maps is GTAO's *priced information* form (`CORE.md:52`, R1). Even there the coordinate differs: control pays KL to a fixed reference, while GTAO pays mutual information. The two are equal only when the reference is the average controlled law (golden formula, check C5a, KNOWN).
- **New vs relabel.** Every physics identity here is known: Kappen 2005, Todorov 2009, Nelson 1966, Yasue 1981, Zambrini 1986, Frieden 1989, Reginatto 1998, Onsager–Machlup 1953, Léonard 2014, Chen–Georgiou–Pavon 2021. Closest framing prior art: Ortega and Braun 2013, "Thermodynamics as a theory of decision-making with information-processing costs". **[REVIEWER EDIT 2026-11-23]** Ortega–Braun is already credited in the repo as "the same Lagrangian, framed thermodynamically" (`theory/GENERAL_THEOREM.md:157,376`; `theory/NOVELTY_NOTE_2026-11-21.md:23`; `reviews/master-equation_2026-11-19/REVIEW.md:97`). Prior art framing ground states and quantum dynamics as optimal stochastic control, missing above: Fleming 1977; Holland 1978; Fleming–Mitter 1982; Guerra–Morato 1983 (title: "Quantization of dynamical systems and stochastic control theory"); Sheu 1984; Fleming–Sheu 1985; Dai Pra 1991; Pavon 1995; Chetrite–Touchette 2015 (conditioned processes = KL-optimal control). Three things are new to the repo (not to the literature):
  1. The term-by-term dictionary, with the places it fails (§3).
  2. **Proposition R:** a ruin cap \(P(\text{ruin})\le\varepsilon\) costs at least \(\lambda\,d(1-\varepsilon\,\|\,p)\) in nats, where \(p\) is the passive survival chance. Feedback reaches this exactly. It is ELEMENTARY, from Csiszár's I-projection, and checked by simulation (C3). **[REVIEWER EDIT 2026-11-23]** KNOWN in substance: a two-point I-projection (Csiszár 1975) plus Doob conditioning as the KL-optimal control (Fleming 1977 for \(-\lambda\ln p\) as a control value; Chetrite–Touchette 2015). Re-verified exactly on a discrete chain (review check R2: KL = \(d(1-\varepsilon\|p)\) to 10 digits). New only as GTAO bookkeeping: it prices the ruin cap that `theory/NOVELTY_NOTE_2026-11-21.md:23` lists as absent from Ortega–Braun.
  3. The split "heat floor ≠ steering KL" (C5b).

  None of the three is new physics.
- **What this does to the circularity** (`theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176`: "The cost, as written, already assumes a system, a world, a bath, and a temperature"). The inversion removes the bath and the temperature, since \(\hbar\) takes \(kT\)'s place as the information price. It still presupposes a reference measure (free diffusion at \(\sigma^2=\hbar/m\)), a noise scale, and a potential. The circularity moves; it is not removed.
- **A consequence that could fail** (§6). In the class, no stationary design may beat \(E_0\), and none may hold ruin below \(\varepsilon\) for less than \(d(1-\varepsilon\|p)\) nats. As a reading of the hypothesis: a strongly selected steering system with a time-independent stake should carry no stationary circulation in its steered coordinate, because circulation is pure excess cost (INV-E (i)). **[REVIEWER EDIT 2026-11-23]** Scope: this holds only inside KC-S (additive isotropic noise, KL to a reversible reference, stake a function of position, \(d\ge2\); in 1D a stationary \(v\) is forced to 0). The math (the optimum is reversible) is KNOWN; it becomes a GTAO prediction only once the reference and \(\lambda\) are identified independently of the data.

## 1. Repo check before calling anything new

- Grep on `d592662` for Kappen, Todorov (path-integral), Schrödinger bridge, Nelson (stochastic mechanics), Feynman–Kac, Guerra, Léonard, Onsager–Machlup, Zambrini, ~~Ortega/Braun,~~ Girsanov, Euclidean, Wick: **no hits as used here**. **[REVIEWER EDIT 2026-11-23]** Not so for Ortega/Braun, which is credited at `theory/GENERAL_THEOREM.md:157,376`, `theory/NOVELTY_NOTE_2026-11-21.md:23`, `theory/DERIVATION_CHAIN.md:157`. Donsker–Varadhan 1975 is cited at `theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:54,243` (relative-entropy variational formula, not the eigenvalue use). Todorov appears only as Todorov–Jordan motor control (`theory/ACTING_LOOP_2026-11-22.md:109`). "Nelson" appears only as Cohen–Kaplan–Nelson (`theory/TRANSPORT_BARRIER_2026-11-23.md:47`). "Least action" appears only as an analogy that the reviews advised dropping (`theory/MASTER_EQUATION.md:9-11`; `reviews/master-equation_2026-11-19/REVIEW.md:137-141`).
- Already in the repo, and reused here: the Lagrangian "loss plus a price on information" is credited prior art (Sims 2003; Tishby & Polani 2011; `THEORY.md:283`). CT24, "cost share = price elasticity", includes a **virial identity** (`THEORY.md:474`). Under feedback, "net learning rate = information used to steer", and a conservative trap of the plant has vanishing heat (`CORE.md:80`).
- The target: Level 4, "physics as the minimum-cost way for a universe to keep track of itself", is SPECULATION (`theory/PHYSICS_CHAIN_2026-11-23.md:86-87`). The physical cost is \(J=\dot Q+w\,\mathbb{E}[\ell]\) s.t. \(P(\text{ruin})\le\varepsilon\) (`CORE.md:27`; `theory/GENERAL_FORM_PHYSICS_2026-11-22.md:25-29`), with \(\dot Q\ge kT\times\) learning rate (`CORE.md:70`).

## 2. The GTAO method, run on the inverted question

1. **Cost, named terms.** Class KC: \(dX=(b+u)\,dt+\sigma\,dW\) on \(\mathbb{R}^d\), with \(\sigma\) constant and invertible and \(u\) a Markov feedback satisfying Novikov. The reference ("world") is \(P\), the law with \(u=0\); the design ("judge") is \(u\); \(Q\) is the controlled law.
   \[J_\lambda[u]=\underbrace{\lambda\,\mathrm{KL}(Q\|P)}_{\text{price}\times\text{information}}+\underbrace{\mathbb{E}_Q\Big[\int_0^T V(X_t)\,dt+\phi(X_T)\Big]}_{\text{stake}\times\text{loss}}\quad\text{s.t. }Q(\text{ruin})\le\varepsilon.\]
   Girsanov gives \(\mathrm{KL}(Q\|P)=\mathbb{E}_Q\int_0^T\tfrac12|\sigma^{-1}u|^2dt\), so \(\lambda\,\mathrm{KL}\) is Kappen's control energy with \(R=\lambda(\sigma\sigma^\top)^{-1}\).
2. **Minimum.** By the Gibbs (Donsker–Varadhan) variational principle, \(\min J_\lambda=-\lambda\ln\mathbb{E}_P e^{-S/\lambda}\) with \(S=\int V+\phi\), attained by \(dQ^*/dP=e^{-S/\lambda}/Z\), with \(u^*=\sigma\sigma^\top\nabla\ln Z\). For any \(Q\), \(J_\lambda[Q]-J^*=\lambda\,\mathrm{KL}(Q\|Q^*)\). **KNOWN** (Kappen 2005; Todorov 2009; Donsker–Varadhan 1975; Mitter–Newton 2003 for the estimation dual).
3. **Design.** The optimal judge is a Doob \(h\)-transform of the world: steer along \(\nabla\ln Z\). A stationary optimum has no circulation (INV-E). A ruin cap becomes an \(h\)-transform mixing the "survive" and "ruin" conditionings (Prop. R).
4. **Scope.** Additive Gaussian noise. The information is a path KL to a *fixed* reference, not a mutual information about an external world. Real \(\lambda>0\), and stake bounded below.
5. **Measurements.** Numerical checks only (§5). No real-world data.

## 3. The dictionary: what maps, what does not

| GTAO term | Physical term (Euclidean / KL-control class) | Status |
|---|---|---|
| information price (\(kT\) in the heat floor, \(\kappa\) in the five-term sum) | \(\lambda=\hbar\) (Euclidean QM). Thermal Langevin: \(\lambda=kT\) with \(R=\gamma/2\). Consistent dictionary \(kT\leftrightarrow\hbar\), \(\gamma/2\leftrightarrow m\), \(2kT/\gamma\leftrightarrow\hbar/m\); each thermal quantity is the quantum one per unit time (total cost in energy vs action) | KNOWN in substance (Nelson 1966: \(\nu=\hbar/2m\); Feynman–Kac; Zambrini 1986) |
| information (learning rate × time) | path relative entropy \(\mathrm{KL}(Q\|P)=\mathbb{E}\int\tfrac{m}{2\hbar}|u|^2\) to the free reference | **Partial.** Same form as GTAO's priced-information term (`CORE.md:52`). **Not** GTAO's heat: equilibrium trap, heat 0, KL rate \(\omega/4\) (C5b). Not mutual information unless the reference = average controlled law (C5a) |
| stake × loss \(w\,\mathbb{E}[\ell]\) | Euclidean: \(+U\), potential energy. Real-time action: \(-U\) | Euclidean maps when \(U\) is bounded below. Real time: a minimum only before the first conjugate point (C4); bounded-above \(U\) only makes the stake \(-U\) bounded below **[REVIEWER EDIT 2026-11-23]** (it is neither necessary nor sufficient for a minimum; review R3). Coulomb \(U\) is unbounded below, so it is outside the nonnegative-price form (CT24 needs \(\varphi_i\ge0\), `THEORY.md:474`). There the minimum still exists, but by stability of matter, as in T66 (`theory/TRANSPORT_BARRIER_2026-11-23.md:97`) |
| ruin cap | killing set / absorbing wall (\(V=+\infty\)); nodal surfaces of excited states | Maps; priced by Prop. R. An excited state is the ground state of its nodal domain with ruin walls on the nodes, and the cost does not choose those walls |
| minimum \(J^*\) | free energy \(-\lambda\ln Z\); long-run rate = \(E_0\) | KNOWN (Feynman–Kac, Rayleigh–Ritz) |
| cost shares = elasticities (CT24) | quantum virial theorem \(\langle T\rangle=\tfrac k2\langle U\rangle\) (Hellmann–Feynman in \(\hbar\)) | Relabel: CT24's own virial identity (`THEORY.md:474`) applied to this class |
| zero-noise limit | Euclidean least action \(\int\tfrac m2|\dot x-b|^2+V\); Onsager–Machlup/Freidlin–Wentzell action (OM's \(\tfrac12\nabla\!\cdot b\) term is \(O(\lambda)\) and drops out) | KNOWN |
| "judge" when the system is the universe | the whole drift field: deviation from free diffusion | SPECULATION as a reading |
| "world" when the system is the universe | the reference measure (free Brownian motion at \(\hbar/m\)) | presupposed, not derived |
| learning *about* an external world | no counterpart: no bipartite memory/world split, nothing is learned, the KL prices self-steering | **does not map** |

## 4. Statements

**Theorem INV-E (Euclidean equivalence; PROVED in-model from KNOWN pieces).** Class KC-S, on \(\mathbb{R}^d\):
- Stationary Markov designs \(dX=u(X)\,dt+\sigma\,dW\) with \(\sigma^2=\hbar/m\).
- A stationary density \(\rho\) with finite Fisher information.
- Reference \(P\): driftless Brownian motion with the same \(\sigma\) and initial law.
- \(U\) continuous, bounded below and confining, so that \(H=-\tfrac{\hbar^2}{2m}\Delta+U\) has a ground state \(\psi_0>0\).

The long-run cost rate is \(j[u]=\hbar\lim_T\tfrac1T\mathrm{KL}(Q_T\|P_T)+\mathbb{E}_\rho U=\mathbb{E}_\rho[\tfrac m2|u|^2+U]\). Then:
- (i) Write \(u=u_{os}+v\), with \(u_{os}=\tfrac{\sigma^2}2\nabla\ln\rho\) and \(\nabla\!\cdot(\rho v)=0\) (Fokker–Planck stationarity). The cross term \(\int\nabla\rho\cdot v=\int\nabla\ln\rho\cdot(\rho v)=-\int\ln\rho\,\nabla\!\cdot(\rho v)=0\). So \(j=\tfrac{\hbar^2}{2m}\int|\nabla\sqrt\rho|^2+\int U\rho+\tfrac m2\int\rho|v|^2\).
- (ii) Rayleigh–Ritz then gives \(j\ge E_0\), with equality iff \(v=0\) and \(\rho=\psi_0^2\). That is \(u^*=\tfrac\hbar m\nabla\ln\psi_0\), Nelson's ground-state process.
- (iii) If \(v=\tfrac\hbar m\nabla S\), then \(j=\langle\Psi|H|\Psi\rangle\) with \(\Psi=\sqrt\rho\,e^{iS/\hbar}\). This is Nelson's/Yasue's energy, now read as cost.
- (iv) If \(U\) is homogeneous of degree \(k\), the information share at the minimum is \(k/(k+2)\).
- (v) Every minimizer is a positive tilt of \(P\). Excited and interfering states are not minima. Nodal states arise only with imposed ruin walls.

Proof sketch: (i) by Girsanov and the computation above; (ii) as stated; (iii) from \(|\nabla\Psi|^2=|\nabla\sqrt\rho|^2+\rho|\nabla S|^2/\hbar^2\); (iv) by virial/CT24; (v) by Perron–Frobenius positivity of the Feynman–Kac kernel.

**Status:** each step is KNOWN (Nelson 1966; Yasue 1981; Frieden 1989; Reginatto 1998; Zambrini 1986). Only the assembly is in GTAO's terms. **[REVIEWER EDIT 2026-11-23]** The assembly is KNOWN too: (i)–(ii) is the Donsker–Varadhan rate function of Brownian motion, \(I(\rho)=\tfrac{\sigma^2}{2}\int|\nabla\sqrt\rho|^2\), in its control representation (Fleming 1977; Holland 1978; Sheu 1984; Chetrite–Touchette 2015), plus Rayleigh–Ritz. Label: **KNOWN** (re-derived and checked in-model by the reviewer), not PROVED (in-model) as a new result. Derivation re-done independently: signs, the cross-term cancellation, the factor \(\hbar^2/2m\) and (iv) \(k/(k+2)\) (dilation: \(-2\,s_{\rm info}+k\,s_U=0\), CT24's virial identity at `THEORY.md:474`) all check.

**Proposition R (ruin cap in nats; ELEMENTARY, PROVED in-model).** For any reference law \(P\), survival event \(A\) with \(p=P(A)<1-\varepsilon\):
\[\min\{\mathrm{KL}(Q\|P):Q(A^c)\le\varepsilon\}=d(1-\varepsilon\|p)=(1-\varepsilon)\ln\tfrac{1-\varepsilon}{p}+\varepsilon\ln\tfrac{\varepsilon}{1-p}.\]
- The lower bound comes from data processing onto \(1_A\), plus monotonicity of \(d(\cdot\|p)\) on \([p,1]\).
- The bound is attained by \(Q^*=(1-\varepsilon)P(\cdot|A)+\varepsilon P(\cdot|A^c)\) (Csiszár 1975).
- For a diffusion, \(Q^*\) comes from Markov feedback \(u=\sigma\sigma^\top\nabla\ln h\), with \(h=aq+b(1-q)\), \(q(t,x)=P(A|X_t=x)\), \(a=(1-\varepsilon)/p\), \(b=\varepsilon/(1-p)\).
- At \(\varepsilon=0\) the price of guaranteed survival is \(\lambda\ln(1/p)\).

This is GTAO's ruin cap turned into a price-free number of nats. It does not depend on the dynamics beyond \(p\).

**Finding N (non-maps; KNOWN, checked).**
- (a) Real-time Hamilton's principle with stake \(-U\): for the harmonic oscillator the Hessian of the action loses positivity at \(T=\pi/\omega\), so the cost has no minimum after that (Gray & Taylor 2007).
- (b) Guerra–Morato's real-time stochastic action has \(\tfrac m2(|v|^2-|u_{os}|^2)\). The minus sign means it is not a relative entropy. The Schrödinger equation is its stationary point, not its minimum. **[REVIEWER EDIT 2026-11-23]** The reviewer could not read the 1983 text; the \(v^2-u^2\) form is the standard reading (\(\tfrac m2 DX\cdot D_*X\)) but is unverified here. Yasue's 1981 action has \(+u^2\). The conclusion does not depend on which: in real time the potential enters as \(-U\), and the quantum dynamics is a stationary point, not a minimum, in every formulation (Pavon 1995).
- (c) GTAO's heat \(\dot Q\) and \(kT\cdot\)path-KL are different objects (C5b).

## 5. Checks (`checks/`, run at nice 19; seeds fixed)

| Check | What | Result |
|---|---|---|
| C1 `c1_kappen_lq.py` | LQ KC: Riccati value vs \(-\lambda\ln Z\) (Feynman–Kac MC) vs simulated optimal cost; Girsanov; Gibbs gap | 1.000000 vs 1.0011±0.0011 vs 1.0000±0.0015; \(\mathbb{E}\ln dQ/dP\) 0.8685 vs 0.8677; gaps \(J-J^*\) 0.0988±0.0019 / 0.0771±0.0013 vs \(\lambda\mathrm{KL}(Q\|Q^*)\) 0.1018 / 0.0764 (parameters make \(P(t)\) constant; noted) |
| C2 `c2_euclid_qm.py` | INV-E: grid \(E_0\) vs \(\hbar\)KL-rate + \(\mathbb{E}U\); virial shares; SDE time averages; 2D circulation penalty | harmonic 0.499999 = 0.249999+0.249999, share 0.50000; quartic 0.667985 = 0.445319+0.222661, share 0.66667 (=4/6); \(|x|\) 0.808614, share 0.33333 (=1/3); SDE rates 0.504 / 0.670 / 0.809; 2D: \(c=0.8\) costs 1.326 vs formula 1.320, \(a\ne1\) costs more, minimum 1.003 ≈ \(E_0=1\) |
| C3 `c3_ruin_cap.py` | Prop. R, BM from 1, wall at 0, \(T=1\), \(\varepsilon=0.05\) | \(p=0.682689\), predicted 0.221508; \(h\)-transform: ruin 0.0506, KL 0.2204±0.0007; constant drift at same ruin: KL 0.9216 |
| C4 `c4_real_time.py` | Hessian of the discretized real-time action | harmonic: positive to \(T=3.1\), negative from 3.2 (\(\pi\)); inverted potential (\(V\ge0\)): positive for all \(T\) |
| C5 `c5_golden_trap.py` | golden formula; equilibrium trap | identity to \(10^{-10}\); trap heat \(+0.0012\) (0), KL rate 0.2496 (\(\omega/4\)) |

**[REVIEWER EDIT 2026-11-23]** All five checks rerun at nice 19 from a fresh copy: outputs byte-identical to `checks/*.out`, hashes OK. Caveat on C2: the 6-digit agreement uses the eigenvector itself (tautological up to grid error); the SDE averages are the real check (harmonic 0.5043 vs 0.5, about 0.9% Euler bias). Strongest check: C2. Three potentials, two independent methods (grid diagonalization and SDE time averages) agree on \(E_0\) and on the virial shares. Weakest: C3 sits 1.5 s.e. below the prediction (Euler and bridge-crossing discretization). That is consistent, not tight.

## 6. What would be new, what is a relabel, and how it could fail

- **Relabel (KNOWN):** **[REVIEWER EDIT 2026-11-23]** add: the ground-state energy as the value of an ergodic KL-control problem (Holland 1978; Sheu 1984), i.e. Theorem INV-E as a whole; Prop. R in substance (Csiszár 1975; Chetrite–Touchette 2015). KL control = free energy; the Euclidean dictionary \(\lambda=\hbar\), \(\sigma^2=\hbar/m\); ground state = minimum; Fisher information = quantum kinetic energy; CT24 shares = virial; the classical limit = Euclidean/Onsager–Machlup action. The thesis "decision with information costs is thermodynamics" is Ortega & Braun 2013.
- **New to the repo, modest:** the dictionary with explicit failures; Prop. R; the heat-vs-KL split.
- **Model implications, stated plainly:**
  - If one reads physics as "the minimum of a cost of judgment", that reading holds for imaginary-time physics: ground states, equilibrium statistical mechanics, and Schrödinger bridges. In that reading \(\hbar\) is the price of a nat of steering.
  - It does not give real-time dynamics, interference, or why the price is \(\hbar\). This is **not** a derivation of quantum mechanics. The Schrödinger equation enters through Feynman–Kac in imaginary time and through Nelson's assumptions in real time. GR and holography are not touched.
- **Could fail (in-model):** a stationary design in KC-S with cost rate below \(E_0\); a Markov design holding \(Q(\text{ruin})\le\varepsilon\) with KL below \(d(1-\varepsilon\|p)\). Either would mean an error in INV-E or Prop. R.
- **Could fail (hypothesis reading, for later, no data used):** in class KC, a strongly selected steering system with a time-independent stake should show no stationary circulation in the steered coordinate. In KC-S its long-run stake and steering shares should follow \(k/(k+2)\) for a power-law loss, once \(\lambda\) is identified independently. A persistent circulating current in a stationary task would be a puzzle.
- **Open:**
  - Whether GTAO's *learning-rate* heat (bipartite, about an external world) has any variational counterpart in real-time physics. Nothing here supplies one.
  - Whether a complex price \(i\hbar\) can be given any cost meaning. As far as this memo goes, the answer is no: a complex number cannot be a cost.
  - Whether the reference measure itself can be selected by a cost rather than presupposed.

## 7. Sources (Crossref-verified 23 Nov 2026, `checks/crossref.out`)

- Schrödinger 1931, *Sitzungsber. Preuss. Akad. Wiss., Phys.-Math. Kl.* 144–153. The original has no DOI. English translation and commentary: Chetrite, Muratore-Ginanneschi & Schwieger 2021, *Eur. Phys. J. H* 46:28, doi 10.1140/epjh/s13129-021-00032-7.
- Nelson 1966, *Phys. Rev.* 150:1079, doi 10.1103/PhysRev.150.1079.
- Guerra & Morato 1983, *Phys. Rev. D* 27:1774, doi 10.1103/PhysRevD.27.1774.
- Léonard 2014, *Discrete Contin. Dyn. Syst.* 34:1533, doi 10.3934/dcds.2014.34.1533.
- Chen, Georgiou & Pavon 2021, *SIAM Rev.* 63:249, doi 10.1137/20M1339982.
- Kappen 2005, *Phys. Rev. Lett.* 95:200201, doi 10.1103/PhysRevLett.95.200201.
- Todorov 2009, *PNAS* 106:11478, doi 10.1073/pnas.0710743106.
- Onsager & Machlup 1953, *Phys. Rev.* 91:1505, doi 10.1103/PhysRev.91.1505.
- Zambrini 1986, *J. Math. Phys.* 27:2307, doi 10.1063/1.527002.
- Yasue 1981, *J. Funct. Anal.* 41:327, doi 10.1016/0022-1236(81)90079-3.
- Frieden 1989, *Am. J. Phys.* 57:1004, doi 10.1119/1.15810.
- Reginatto 1998, *Phys. Rev. A* 58:1775, doi 10.1103/PhysRevA.58.1775.
- Ortega & Braun 2013, *Proc. R. Soc. A* 469:20120683, doi 10.1098/rspa.2012.0683.
- Tishby & Polani, "Information Theory of Decisions and Actions", in *Perception-Action Cycle* 601–636, doi 10.1007/978-1-4419-1452-1_19. Crossref dates this 2010; the repo cites it as 2011.
- Csiszár 1975, *Ann. Probab.* 3:146, doi 10.1214/aop/1176996454.
- Donsker & Varadhan 1975, *Commun. Pure Appl. Math.* 28:1, doi 10.1002/cpa.3160280102.
- Mitter & Newton 2003, *SIAM J. Control Optim.* 42:1813, doi 10.1137/S0363012901393894.
- Gray & Taylor 2007, *Am. J. Phys.* 75:434, doi 10.1119/1.2710480.
- **[REVIEWER EDIT 2026-11-23] added prior art, Crossref-verified today:** Fleming 1977, *Appl. Math. Optim.* 4:329, doi 10.1007/BF01442148. Holland 1978 (not 1977), *Commun. Pure Appl. Math.* 31:509, doi 10.1002/cpa.3160310406. Fleming & Mitter 1982, *Stochastics* 8:63, doi 10.1080/17442508208833228. Sheu 1984, *Stochastics* 11:191, doi 10.1080/17442508308833285. Fleming & Sheu 1985, *Appl. Math. Optim.* 13:193, doi 10.1007/BF01442207. Dai Pra 1991, *Appl. Math. Optim.* 23:313, doi 10.1007/BF01442404. Pavon 1995, *J. Math. Phys.* 36:6774, doi 10.1063/1.531187. Chetrite & Touchette 2015, *J. Stat. Mech.* P12001, doi 10.1088/1742-5468/2015/12/P12001.
- Touchette & Lloyd 2000, *Phys. Rev. Lett.* 84:1156, doi 10.1103/PhysRevLett.84.1156 (context, not used in a proof).
