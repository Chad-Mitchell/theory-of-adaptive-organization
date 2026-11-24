# Thermodynamic lift of the drifting information floor

*Monday 23 November 2026 (America/New_York). The next step named in `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md` §7, after a re-confirm of `theory/THEOREM_P_DRIFT.md`. One explicit physical implementation, not a change to `THEORY.md` or the hypothesis sentence. Open-work row T58 (T57 is on main, PR #229). A self-check, not an independent review. DOIs below were checked on the Crossref API the same day (`theory/drift_heat_lift_checks/crossref.out`).*

Labels follow the repo: **PROVED (in-model)** is a result inside a named class. **KNOWN** is published and credited, only for what that source states. **ELEMENTARY** is a direct consequence of a proved or known inequality. **SKETCH** is an argument with a stated gap. **OPEN** is not derived. A lower bound is not a derivation of the cost.

The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

## 0. Bottom line

Take a linear drifting world with no restoring drift — a random walk \(dX=\sigma\,dW_X\) — and couple it to one overdamped memory coordinate whose noise satisfies the Einstein relation of a bath at temperature \(T\). In the long run the mean squared error \(\varepsilon\) stays finite while the world's variance grows.

On this implementation the memory-bath heat and the EQ-heat learning rate have the closed forms, at \(kT=1\) in the display and restored below,

\[
\dot I_M=\frac{\sigma^2}{2\varepsilon},\qquad
\dot Q_M=kT\,\dot I_M\Bigl(1+\frac{\sigma^2}{2D_M}\Bigr),
\]

where \(D_M\) is the Fokker–Planck noise intensity of the memory. The learning rate equals the sampled PD7 floor of `theory/THEOREM_P_DRIFT.md`. The EQ-heat inequality \(\dot Q_M\ge kT\,\dot I_M\) holds, and is **PROVED (in-model)** for this class as an instance of Proposition EQ-heat (`theory/GENERALITY_2026-11-22.md`).

One parameter choice realises the Kalman–Bucy filter of the walk as a physical spring: \(D_M=\sigma^2/2\), rate \(\lambda=\sigma^2/\varepsilon\). For that choice the current state is a sufficient statistic of the memory's path (sensory capacity \(1\)), the discrete-time inflow of PD1 satisfies

\[
\lim_{\Delta t\to0}\frac1{\Delta t}\,I(X_{t+\Delta t};M_{t+\Delta t}\mid M_t)=\dot I_M,
\]

and the bath heat is exactly \(2kT\,\dot I_M\). So the thermodynamic lift of PD1, through an implementation that identifies \(\bar r\) with \(\dot I_M\), carries a factor of two: \(\dot Q_M=2kT\,\bar r\) in continuous-time units. That factor is **PROVED (in-model)** for this implementation, and is the same accounting already **KNOWN** for a path-sufficient or capacity-one device (Sandberg, Delvenne, Newton, and Mitter 2014, *Phys. Rev. E* 90:042119, equations (42) and (47) of arXiv:1402.1010v2; Hartich, Barato, and Seifert 2016).

A fast, noisier spring, with \(D_M\to\infty\) at fixed \(\varepsilon\), drives the heat down to the infimum \(kT\,\sigma^2/(2\varepsilon)\). That infimum is **PROVED (in-model)** for this spring family, and it matches the already-proved Ornstein–Uhlenbeck heat floor (`theory/INFO_PHYSICS_ATTAINABILITY.md`). On those designs the short-time PD1-style inflow \(I(X_t;M_{t+\Delta t}\mid M_t)/\Delta t\) is larger than \(\dot I_M\), and the identification needed to lift PD1 does not hold. The factor-one infimum is a heat floor at fixed error, not a lift of the information inflow.

## 1. The cost, with named terms

The method is the same as everywhere in the theory: write the cost, find its minimum, and read off the design. Whether a real system sits near that minimum is Part 2, and is not decided here.

Inside the physics display of `CORE.md` §1 and `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md` §1, the cost of judgment is the memory-bath heat plus a stake on the decision loss, with the ruin cap outside the sum:

\[
J=\dot Q_M+w\,\mathbb{E}[\ell]\qquad\text{subject to}\qquad P(\mathrm{ruin})\le\varepsilon_{\mathrm{ruin}}.
\]

Named terms:

- \(\dot Q_M\) is the energy flow into the bath that implements the memory's transitions, in energy per unit time, as a long-run average.
- \(kT\) is Boltzmann's constant times that bath's temperature.
- \(\dot I_M\) is the EQ-heat information flow of those same memory transitions, \(\int J\,\partial_M\ln p(X\mid M)\), in nats per unit time.
- \(\bar r\) is the long-run mean of the PD1 inflow \(r_t=I(X_t;M_t\mid M^{t-1})\), in nats per step. In continuous time the rate is the step divided by the step length.
- \(\ell\) is the squared error of an action \(A=f(M)\) aimed at the current world state, and \(d=\mathbb{E}[\ell]\). The letter \(\varepsilon\) below is that mean squared error, not the ruin cap.
- \(w\) converts the loss into the currency of the heat. Temperature does not set \(w\).

A lower bound on \(\dot Q_M\) at fixed \(d\) is a lower bound on \(J\) at that \(d\).

## 2. The implementation

**World (PD-C, scalar, no restoring drift).** \(dX=\sigma\,dW_X\). This is the linear drifting world \(X_{t+\mathrm{dt}}=aX_t+W_t\) at \(a=1\) in continuous time, or \(\theta=0\) in the notation of PD7. Variance grows as \(\sigma^2 t\). The signal is exogenous: the memory does not move it (PD-A).

**Memory.** One overdamped coordinate with Einstein noise, mobility not necessarily one,

\[
dM=-\lambda(M-X)\,dt+\sqrt{2D_M}\,dW_M,
\]

with \(W_M\) independent of \(W_X\), \(\lambda>0\), and \(D_M>0\). The force is a spring whose rest point is the current world state. This is the centered spring of `theory/INFO_PHYSICS.md`, now coupled to a world that has no stationary law. Proposition EQ-heat applies: the drift is smooth, the noise is additive and constant, and the memory bath is the one in the balance. In a non-steady state the identity is \(\Sigma_M=\mathrm{Sr}_M-\dot I_M+\mathrm d_t S_M\ge0\). For this design \(\mathrm{Var}(M)\) grows like \(\sigma^2 t\), so \(S_M=\tfrac12\log(2\pi e\,\mathrm{Var}(M))\) grows only as \(\tfrac12\log t\), and the long-run average of \(\mathrm d_t S_M\) vanishes. The long-run average heat therefore obeys \(\dot Q_M=kT\,\mathrm{Sr}_M\ge kT\,\dot I_M\).

**Kalman–Bucy matching.** The Kalman–Bucy filter of this walk, driven by an observation \(dY=X\,dt+\sqrt{s}\,dW_Y\), is \(dM=K(dY-M\,dt)\) with gain \(K=P/s\) and steady error \(P=\sigma\sqrt{s}\). That SDE is the spring above at \(\lambda=K\) and \(\sqrt{2D_M}=K\sqrt{s}\), which forces \(D_M=\sigma^2/2\) and \(\lambda=\sigma^2/\varepsilon\).

## 3. Derivation

**Error and rates (PROVED (in-model), linear Gaussian).** Write \(E=M-X\). Then \(dE=-\lambda E\,dt+\sqrt{2D_M}\,dW_M-\sigma\,dW_X\). The error is a stationary Ornstein–Uhlenbeck process, even though \(X\) and \(M\) wander:

\[
\varepsilon=\mathbb{E}[E^2]=\frac{\sigma^2+2D_M}{2\lambda}.
\]

The joint law of \((X,M)\) remains Gaussian. The EQ-heat flow and the medium production, computed from the late-time second moments in `theory/drift_heat_lift_checks/drift_heat_lift_checks.py`, collapse to

\[
\dot I_M=\frac{\lambda\sigma^2}{\sigma^2+2D_M}=\frac{\sigma^2}{2\varepsilon},\qquad
\dot Q_M=kT\,\frac{\lambda\sigma^2}{2D_M}=kT\,\dot I_M\Bigl(1+\frac{\sigma^2}{2D_M}\Bigr).
\]

The first identity is PD7 at \(\theta=0\), attained, not just bounded. The second is the heat. The ratio is at least one, with equality only in the limit \(D_M\to\infty\).

**Identification at the Kalman–Bucy point (PROVED (in-model)).** At \(D_M=\sigma^2/2\), the ratio is exactly \(2\), and \(\lambda=\sigma^2/\varepsilon\) holds the error at \(\varepsilon\). The path of \(M\) is an observation of \(X\) with effective noise intensity \(2D_M/\lambda^2\). The Kalman filtering error given that path equals \(\varepsilon\), so the current state is a sufficient statistic of the path and the sensory capacity of Hartich, Barato, and Seifert is \(1\). The Duncan path rate equals \(\dot I_M\). For the exact Gaussian transition over a step \(\Delta t\),

\[
\frac1{\Delta t}\,I(X_{t+\Delta t};M_{t+\Delta t}\mid M_t)\;\longrightarrow\;\dot I_M
\]

as \(\Delta t\to0\), checked at \(\Delta t=10^{-2},10^{-3},10^{-4}\) in the script. That is the identification of the PD1 inflow, in continuous-time units, with \(\dot I_M\). Therefore \(\dot Q_M=2kT\,\bar r\) on this implementation.

**The short-time inflow off the Kalman–Bucy point (PROVED (in-model), this family).** For a general linear spring the same short-time expansion gives \(I(X_t;M_{t+\Delta t}\mid M_t)/\Delta t\to\lambda^2\varepsilon/(4D_M)\). This equals \(\dot I_M=\lambda\sigma^2/(\sigma^2+2D_M)\) if and only if \(D_M=\sigma^2/2\). On the fast family that approaches the heat infimum, the short-time inflow is larger than \(\dot I_M\) (at \(D_M=10^6\) and \(\varepsilon=0.2\), more than a hundred times larger). Those designs cannot be used to lift PD1 by substituting \(\bar r\) for \(\dot I_M\).

**The factor-one infimum (PROVED (in-model), this family; already known for a stationary Ornstein–Uhlenbeck world).** Holding \(\varepsilon\) and sending \(D_M\to\infty\) (with \(\lambda=(\sigma^2+2D_M)/(2\varepsilon)\)) yields \(\dot Q_M\downarrow kT\,\sigma^2/(2\varepsilon)\). The same fast-spring limit is the proved heat floor of `theory/INFO_PHYSICS_ATTAINABILITY.md` in the stationary class, where a shrunk spring at rate \(10^6\), error \(0.2\), and \(a=v=kT=1\) has heat \(4.000020\) against \(R=4\), not \(8\). The path rate on that design is large and the capacity is near \(0\). The factor two of Sandberg and of Hartich covers a state that keeps the path. It does not apply to that design, and it does not apply to the fast random-walk spring either.

## 4. What this says about the factor-of-two question

The Kalman–Bucy minimum-power factor-of-two question, as `CORE.md` §3 and `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md` §2 frame it, is an implementation-accounting question, already distinguished from the learning-rate heat infimum in the proved Ornstein–Uhlenbeck class.

This note answers it for one explicit implementation in a drifting world:

- If the implementation is the Kalman–Bucy-matched Einstein spring, the PD1 inflow identifies with \(\dot I_M\), and the memory-bath heat is \(2kT\,\bar r\). That is the lift.
- If the implementation is a fast spring at the same error, the heat approaches \(kT\) times the PD7 rate, which is the infimum of the bath heat at that error, and the PD1 identification does not hold.

Both statements are **PROVED (in-model)** inside the named class. Neither is a general prefactor for every physical realisation of a filter, and neither is adopted into `THEORY.md`. A nonlinear memory, a discrete-time (not sampled) physical update, and a world with a nonzero restoring or unstable drift, where the Kalman–Bucy SDE carries a copy of the world drift that is not obviously a bath force, are not derived here.

## 5. Numerical checks (NUMERICAL)

`theory/drift_heat_lift_checks/drift_heat_lift_checks.py`, run at nice 19, and locked by `tools/test_drift_heat_lift_checks.py`.

| Check | Result |
|---|---|
| Stationary OU spring: \(\dot I_M\) and \(\dot Q_M\) match the known linear-memory formulas of `theory/info_physics_checks/attainability_checks.py` | agree to \(10^{-12}\) |
| Random-walk Kalman–Bucy match at \(\sigma=1\), \(\varepsilon=0.2\) | \(\dot I_M=2.5=\sigma^2/(2\varepsilon)\); \(\dot Q_M=5=2kT\dot I_M\); path error \(=\varepsilon\); capacity \(=1\) |
| Closed-form ratio \(1+\sigma^2/(2D_M)\) | equals \(2\) at \(D_M=\sigma^2/2\); falls toward \(1\) as \(D_M\) grows (1.25, 1.05, 1.005, 1.00005, 1.0000005 at \(D_M=2,10,100,10^4,10^6\)) |
| Short-time inflow equals \(\dot I_M\) only at the Kalman–Bucy noise | identity holds at \(D_M=\sigma^2/2\); fails, as required, on the rest of the family |
| Discrete Gaussian inflow of the matched spring, late time, \(\Delta t=10^{-2},10^{-3},10^{-4}\) | approaches \(2.5\) (absolute errors \(6.0\times10^{-2}\), \(6.2\times10^{-3}\), \(6.5\times10^{-4}\)) |
| EQ-heat inequality \(\dot Q_M\ge kT\dot I_M\) on a grid of centered random-walk springs | holds |
| Fast shrunk spring on a stationary OU, rate \(10^6\), error \(0.2\) | heat \(4.000020\) against \(R=4\), matching the attainability note |

## 6. What remains open

- A discrete-time physical update that is not the sampling of this continuous spring, including a Landauer-style cycle for one Kalman step.
- Worlds with a nonzero restoring or unstable drift: the Kalman–Bucy SDE then contains a copy of the world drift. Treating that term as work rather than bath heat is **SKETCH**, not written out. The stationary Ornstein–Uhlenbeck case is already covered by the existing heat floor; the random walk is the drifting case in which the force is a pure spring.
- Whether every implementation that identifies \(\bar r\) with \(\dot I_M\) must have sensory capacity one, and therefore pay at least \(2kT\,\dot I_M\) by Hartich, Barato, and Seifert's capacity-one bound. That would make the factor two general among identifying implementations. It is not proved here outside the linear Einstein spring.
  - **Amendment, 23 November 2026 (PR for T68; `theory/CLOCK_TERM_2026-11-23.md`).** This question has a published answer, with one qualification.
    - **Diffusions (KNOWN).** For an overdamped memory obeying the Einstein relation, Ito, Maekawa, Nagayama, Dechant and Yoshimura 2026 (*Phys. Rev. E*, doi 10.1103/19nl-c8fl; arXiv:2512.22890) prove \((\dot I^X)^2\le\dot\Sigma^X I^{\mathrm{Fisher};X}\) (their eq. 30, with eq. 31) and hence \(\sigma^X\ge(\dot I^X)^2/I^{\mathrm{Fisher};X}+\dot I^X\) (their eq. 34). In a steady state that is \(\dot Q_M\ge kT\,\dot I_M(1+\dot I_M/N)\), where \(N=D_M\,\mathbb E[(\partial_m\ln p(x\mid m))^2]\) is the rate at which the memory's own noise erases what it knows. Ito et al. credit the relation to Matsumoto, Sasa and Dechant 2025 (*J. Stat. Mech.* 093202, doi 10.1088/1742-5468/adf4be). Since \(\dot I_M=\mathbb E[(f-\mathbb E[f\mid m])\partial_m\ln p(x\mid m)]-N\) and the short-time inflow is \(\bar r=\mathbb E\,\mathrm{Var}(f\mid m)/(4D_M)\), Cauchy–Schwarz gives \(\dot I_M\le2\sqrt{\bar rN}-N\). So \(\bar r=\dot I_M\) forces \(\dot I_M=N\) and therefore \(\dot Q_M\ge2kT\,\dot I_M\) (ELEMENTARY from the two known pieces).
    - **Linear class (PROVED in-model).** For every jointly Gaussian world–memory pair both Cauchy–Schwarz steps are tight, so \(\dot Q_M=kT\,\dot I_M(1+\dot I_M/N)\) exactly. This note's \(1+\sigma^2/(2D_M)\) is the case \(\dot I_M/N=\sigma^2/(2D_M)\), and Kalman–Bucy matching (factor two) is \(\dot I_M=N\). Checked to \(2\times10^{-11}\) on 2000 random linear pairs in the independently reviewed way-in memo (23 November 2026, off-repo).
    - **Jump processes (KNOWN, with a qualification).** Hartich, Barato and Seifert 2016 §V.B (eqs. 61–64): imposing \(l_y=\bar{\mathcal T}_{x\to y}\), the one-step inflow \(I(y_{t+dt};x_t\mid y_t)/dt\) (their eq. 17), gives \(\sigma_y=2l_y+\tilde\sigma_y\), so efficiency \(\le1/2\) and heat \(\ge2kT\,l_y\). That needs no appeal to capacity one **for the one-step inflow**, which is the quantity computed in §3 above. **Qualification:** with the history-conditioned definition of \(\bar r\) in §1 (conditioned on \(M^{t-1}\)), the inflow is the true transfer entropy \(\mathcal T\le\bar{\mathcal T}\). Identifying it with \(\dot I_M\) is then capacity one by definition (\(C=l_y/\mathcal T\)), and the factor two needs HBS's full \(C=1\Rightarrow\mathcal T=\bar{\mathcal T}\) step, which rests on their stated fictitious-memory assumption. Both readings are recorded; neither is new mathematics here.
- The items already open in PD8, T48, T49, and the general learning-rate–distortion function \(\Phi\) of `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md`. This note does not close those.

The Part 2 hypothesis sentence is unchanged and is not restated beyond the header. CX1 stays **OPEN**.

## 7. References

DOIs checked on Crossref, 23 November 2026, America/New_York. The log is `theory/drift_heat_lift_checks/crossref.out`. No citation is invented.

- Horowitz, J. M. and Esposito, M. 2014. Thermodynamics with Continuous Information Flow. *Phys. Rev. X* 4:031015. doi 10.1103/PhysRevX.4.031015. Proposition EQ-heat is the diffusion form of their split, already in `theory/GENERALITY_2026-11-22.md`.
- Barato, A. C., Hartich, D. and Seifert, U. 2014. Efficiency of cellular information processing. *New J. Phys.* 16:103024. doi 10.1088/1367-2630/16/10/103024.
- Sandberg, H., Delvenne, J.-C., Newton, N. J. and Mitter, S. K. 2014. Maximum work extraction and implementation costs for nonequilibrium Maxwell's demons. *Phys. Rev. E* 90:042119. doi 10.1103/PhysRevE.90.042119. Equations (42) and (47) of the arXiv version (1402.1010v2): the implementation cost of a demon that keeps the path is \(\dot W_{\mathrm{impl}}=2kT\,\dot I_c\). The Allerton short version, *Proc. Allerton* 550–555, doi 10.1109/ALLERTON.2014.7028503, records the same factor-of-two implementation cost; this note does not rely on that proceedings' equation numbering.
- Ito, S., Maekawa, Y., Nagayama, R., Dechant, A. and Yoshimura, K. 2026. Geometric decomposition of information flow for overdamped Langevin systems and optimal transport in subsystems. *Phys. Rev. E*. doi 10.1103/19nl-c8fl (arXiv:2512.22890; eqs. 30, 31, 34 read in v1 and v2). Crossref log: `theory/clock_term_checks/crossref.out`.
- Matsumoto, K., Sasa, S. and Dechant, A. 2025. Learning rate matrix and information-thermodynamic trade-off relation. *J. Stat. Mech.* 093202. doi 10.1088/1742-5468/adf4be (Crossref log: `theory/clock_term_checks/crossref.out`).
- Hartich, D., Barato, A. C. and Seifert, U. 2016. Sensory capacity: An information theoretical measure of the performance of a sensor. *Phys. Rev. E* 93:022116. doi 10.1103/PhysRevE.93.022116. When sensory capacity is \(1\), efficiency is at most \(1/2\).
- Duncan, T. E. 1970. On the Calculation of Mutual Information. *SIAM J. Appl. Math.* 19:215–220. doi 10.1137/0119020. The continuous-time Kalman–Bucy information rate; PD7's equality.
- Tatikonda, S., Sahai, A. and Mitter, S. 2004. Stochastic Linear Control Over a Communication Channel. *IEEE Trans. Automat. Control* 49:1549–1561. doi 10.1109/TAC.2004.834430.
- Kostina, V. and Hassibi, B. 2019. Rate-Cost Tradeoffs in Control. *IEEE Trans. Automat. Control* 64:4525–4540. doi 10.1109/TAC.2019.2912256.

Already in the repository: `theory/THEOREM_P_DRIFT.md` (PD1, PD7; re-confirmed 23 November 2026); `theory/GENERALITY_2026-11-22.md` (EQ-heat); `theory/INFO_PHYSICS_ATTAINABILITY.md` and `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` (the factor-one infimum and the capacity-one factor two, in the stationary class); `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md` (the attempt this lift sits under; T57).
