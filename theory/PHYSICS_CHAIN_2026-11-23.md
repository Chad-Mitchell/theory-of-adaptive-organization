# From the cost of judgment toward physics: roadmap of the chain

*Monday 23 November 2026 (America/New_York). Written against `main` `c67bc0b` (after PR #236, T62; PR #237, T48; and PR #238, T49; the T63 record-repair heat-floor draft is in flight). This is a roadmap of what is proved, what is hypothesized, what remains open, and what is speculation. It does not edit `THEORY.md`, `theory/SCALE_ENDS.md`, or the hypothesis sentence, and it adds no new theorem or CLAIM_MAP row.*

Labels follow `CORE.md:168` and `theory/AREA_LAW_PROBE_2026-11-23.md:5`: **PROVED (in-model)** is a result inside a named class. **KNOWN** is published and credited, only for what that source states. **CONJECTURE** is a named bet, not a result. **HYPOTHESIS** is a claim about nature, not a theorem. **SPECULATION** is neither proved nor preregistered. **OPEN** is not derived or not measured. **IMPOSTER** (`theory/IIT_PATH_2026-11-23.md:5`) is a claim that sounds as if it follows from the theory when it does not.

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

---

## 1. The GTAO method on this chain

The method is the same at every link (`CORE.md:9, 48, 64`):

1. **Write the cost.** In the physical class (`CORE.md:27, 66`), the long-run rate is \(J = \dot Q_M + w\,\mathbb{E}[\ell]\) subject to \(P(\mathrm{ruin})\le\varepsilon_{\mathrm{ruin}}\) (memory-bath heat plus stake times expected decision loss; separate from `THEORY.md` §3's five-term sum, `CORE.md:31-44`, `OPEN_WORK.md:91`). When the memory acts on the world (`theory/FEEDBACK_FLOOR_2026-11-23.md:56`), the world-bath actuation heat \(\dot Q_X\) enters as \(J = \dot Q_M + \dot Q_X + w\,\varepsilon_{\mathrm{task}}\). Temperature does not fix the stake \(w\) (`CORE.md:29`).
2. **Find the minimum.** Under a thermodynamic floor \(\dot Q_M \ge kT\,\dot I_M \ge kT\,\Phi(d)\) (`CORE.md:68-70`), minimize \(kT\,\Phi(d) + w\,d\) over attainable distortion \(d\), or minimize total heat plus stake in the feedback class (`theory/FEEDBACK_FLOOR_2026-11-23.md:33-35`).
3. **Read off the design.** Freeze static degrees of freedom at zero ongoing heat (`CORE.md:78`), route boundary learning flux only to changing degrees of freedom that the decision uses (`theory/AREA_LAW_PROBE_2026-11-23.md:127`), use fast or aligned memories where tracking pays (`CORE.md:74, 76`), and respect boundary channel capacity (`theory/AREA_LAW_PROBE_2026-11-23.md:107-109`).
4. **State scope and open measurement.** In-model bounds hold only inside their named classes (`CORE.md:11, 60`). Whether real systems sit near the minimum (`CORE.md:68`), non-MSE / feedback extensions of T49 (`theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:28`), leaky-record repair heat (T63, in flight), and gravitational inputs (`theory/AREA_LAW_PROBE_2026-11-23.md:145`) remain open or empirical.

---

## 2. Level 1 — PROVED (in-model): the heat floor across classes

- **Thermodynamic floor \(\dot Q_M \ge kT\,\dot I_M\) (`CORE.md:70`).** **KNOWN** for bipartite Markov jumps (Horowitz and Esposito 2014, doi `10.1103/PhysRevX.4.031015`) and **PROVED (in-model)** for additive-noise diffusions (`EQ-heat`). The bound prices the *net* learning rate of memory transitions, not unsigned jump traffic.
  - *What would break it:* Non-local-detailed-balance protocols or non-Einstein noise, or coupling to an auxiliary bath that pays the dissipation externally (`theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md:55`, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:17`).
  - *Next proof:* Generalize \(\Phi(d)\) via quantitative mixing or amplification inequalities (`theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md:15`).
- **Continuous A6 coordinate (T48, `theory/CONTINUOUS_A6_2026-11-23.md:13-28`, `OPEN_WORK.md:99`).** **KNOWN** + **PROVED (in-model)** packaging: on standard Borel spaces with finite mutual information, A6's memory stock \(I(M_t;X^t)\) is the Gelfand–Yaglom–Dobrushin supremum of discrete mutual informations, equal to \(D_{\mathrm{KL}}(P_{X,Y}\|P_X\otimes P_Y)\) and to differential mutual information when densities exist. Theorem R1 is unchanged; the gross stock \(I(M_t;X^t)\) stays distinct from the net learning rate \(I_{\mathrm{alt}}\) (`:28`).
  - *What would break it:* Infinite mutual information (`:26`), where R1 is not applied, or conflating differential entropy with finite-law Aczél–Forte–Ng uniqueness (`:26`).
  - *Next proof:* None for A6; non-Gaussian floors for exogenous MSE are T49 (`theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:13-28`, `OPEN_WORK.md:100`).
- **Drifting continuous worlds (T58, `theory/DRIFT_HEAT_LIFT_2026-11-23.md:16-30, 78-94`, `OPEN_WORK.md:109`).** **PROVED (in-model)** for an overdamped Einstein spring tracking a random walk: \(\dot I_M = \sigma^2/(2\varepsilon)\); a Kalman–Bucy-matched spring (sensory capacity \(1\)) pays \(2kT\,\bar r\) (matching Sandberg et al. 2014, doi `10.1103/PhysRevE.90.042119`, and Hartich et al. 2016, doi `10.1103/PhysRevE.93.022116`), while a fast noisier spring approaches the factor-one infimum \(kT\,\sigma^2/(2\varepsilon)\).
  - *What would break it:* Non-linear dynamics, discrete-time updates, or restoring/unstable drifts where the filter copy is work rather than bath heat (`theory/DRIFT_HEAT_LIFT_2026-11-23.md:105, 123-124`).
  - *Next proof:* General capacity-one factor-two accounting outside linear Einstein springs (`CORE.md:82`, `theory/DRIFT_HEAT_LIFT_2026-11-23.md:125`).
- **Frozen vs. changing two-state worlds (T59, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:15-27, 76-85, 144-146`, `OPEN_WORK.md:110`).** **PROVED (in-model)** for a telegraph world and leaky two-state memory under local detailed balance: leak rate \(\Gamma\) cancels in the net flow, giving \(\dot Q_M \ge kT\,r\,L(\varepsilon)\). At \(r=0\) (frozen world), a static bias is at equilibrium with zero ongoing heat at a finite Boltzmann error; a high barrier buys lifetime \(\sim 1/\Gamma\), not a steady heat floor.
  - *What would break it:* An irreversible (non-LDB) refresh protocol that enforces a per-reset Landauer cost (`:17, 172`), which is the entry point for T63.
  - *Next proof:* Non-LDB record-repair heat floor (T63, in flight).
- **Connected finite-state worlds (T60, `theory/GENERAL_FLOOR_FINITE_2026-11-23.md:18-29, 89`, `OPEN_WORK.md:111`).** **PROVED (in-model)** for exogenous steady Markov-jump worlds: \(I_{\mathrm{alt}} = \sum_{x\neq x'}\pi(x)W_X(x\to x')D_{\mathrm{KL}}(p(M\mid x)\,\|\,p(M\mid x'))\). Strongly connected occupied flux graphs force \(I_{\mathrm{alt}}>0\) whenever Bayes error beats chance (one direction for \(\ge 3\) states), giving the world-only Path-Pinsker bound \((\varepsilon_0-\varepsilon)^2/K_X\), pairwise \(L\) bound, and telegraph bound \(r\,L(\varepsilon)\) for any finite memory. Disconnected recurrent classes still allow zero ongoing heat by holding a class label (`:21`).
  - *What would break it:* Disconnected occupied flux (`:21`) or a world whose rates depend on \(M\).
  - *Next proof:* A closed form for \(\Phi_X\) on general irreducible kernels (`:29`).
- **Feedback / acting worlds (T61, `theory/FEEDBACK_FLOOR_2026-11-23.md:15-37, 56`, `OPEN_WORK.md:112`).** **PROVED (in-model)** in the named classes: `JP-heat` and `EQ-heat` still hold under feedback (\(I_{\mathrm{alt}}=-I^X\)), but the T60 exogenous identity and any design-independent positive floor on \(\dot Q_M\) alone fail (`:17`). Conservative traps or conservative couplings stay at equilibrium with vanishing ongoing heat (`:21-22`). Under additive linear feedback at fixed process noise, compensated Kalman–Bucy keeps the exogenous learning rate and factor-two memory heat while pushing the regulation cost into world-bath actuation heat \(\dot Q_X\), which diverges as regulated variance \(v\to p\) (`:27-33`).
  - *What would break it:* Conservative actuation menus (`:21-22`) or designs outside the additive-noise linear family (`:35`).
  - *Next proof:* Dual control and the closed-form infimum of total heat \(\dot Q_M+\dot Q_X\) at fixed variance (`theory/FEEDBACK_FLOOR_2026-11-23.md:35`, `CORE.md:80`).
- **Non-Gaussian exogenous worlds under MSE (T49, `theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:13-28`, `OPEN_WORK.md:100`).** **PROVED (in-model)** (PR #238): heavy-tailed or smooth diffusive worlds satisfy \(kTD(1/\varepsilon-\mathcal I(\pi))\); volatility-switching worlds add a regime-tuned copy \(\varepsilon_s\propto\sqrt{D_s}\); rare reset shocks at rate \(\lambda\) scale logarithmically as \(\lambda[\tfrac32\ln(v/\varepsilon)-\gamma_E-\ln 2]\) with a core-plus-reserve design.
  - *What would break it:* Hidden-regime tracking, non-MSE losses, diffusive ruin caps, or feedback (`theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:28`).
  - *Next proof:* Hidden-regime label tracking, tight local-shock constants, and diffusive ruin caps (`:28`).

---

## 3. Level 2 — HYPOTHESIS (needs real-system data)

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

- **Evolutionary bridge (`CORE.md:120-128`).** Weak-mutation selection gives stationary distribution \(\pi\propto\exp(-\beta J)\) and excess \(\mathbb{E}[J]-J^*=d/(2\beta)\) near a quadratic minimum under strong selection, a resolvable band, and enough redesign times (`CORE.md:122-128, 134`). Today **no real system has been shown to qualify** under `THEORY.md` §3 (`CORE.md:13, 68, 138`).
- *What would break it:* A qualified, preregistered, hash-locked strongly selected system whose design sits outside the predicted band without an omitted cost or redesign-band diagnosis (`CORE.md:138`).
- *Next proof / test:* Qualify, preregister, and hash-lock one real strongly selected system (`CORE.md:148, 156`, `OPEN_WORK.md:47, 51`).

---

## 4. Level 3 — OPEN chain to holography and gravity

Each step below separates what is proved in-model from the open conjectures and external physical inputs needed to travel from the cost of judgment to spacetime geometry.

1. **Link 3a — Tracked boundary flux scales with area (PROVED in-model, given a channel packing input; T62, T41, T42, T44).**
   In class AL (`theory/AREA_LAW_PROBE_2026-11-23.md:107-109`, `OPEN_WORK.md:113`), \(\dot I_M \le C_B \le \varphi A\): sustainable tracked learning rate is capped by boundary channel capacity \(C_B\) and scales at most with boundary area \(A\) given a per-area capacity density \(\varphi\). This builds on `T41` (`theory/HOLOGRAPHIC_2026-11-22.md:40, 68, 96`, `OPEN_WORK.md:92`: the floor is the interface learning rate `H-iface`, bulk per-site tracking is volume `H-volume`, surface observation removes at most \(A/\alpha\) `H-surface`) and `T44` (`theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39, 45, 105`, `OPEN_WORK.md:95`: the Markov blanket screens exterior decisions `BS-screen`/`BS-loss`, not interior ones `BS-interior`). Shared storage (`T42`, `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md:46, 52`, `OPEN_WORK.md:93`) compares sum-readout vs. per-item readout and is not Bekenstein–Hawking entropy. Crucially, `AL-stock-free` (`theory/AREA_LAW_PROBE_2026-11-23.md:11, 111`) proves that equilibrium static-bias records have zero ongoing heat and still pack by volume even after a bounded-rate write (`AL-write`, `:115`), while tracking a volumetric changing world remains a volume cost (`AL-volume-track`, `:117-125`).
   - *What would break Link 3a:* Volume-distributed read channels bypassing the boundary, or unbounded channel packing density \(\varphi\).
   - *Next proof:* Extend class AL beyond bipartite Markov/Langevin cuts to quantum channels (`theory/AREA_LAW_PROBE_2026-11-23.md:145`).

2. **Link 3b — Leaky-record repair heat exits through the surface (CONJECTURE; T63 in progress).**
   Records that must outlast their source sit in metastable wells with Kramers leak \(\Gamma>0\) (`theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:16, 40`). Under `theory/AREA_LAW_PROBE_2026-11-23.md:143` (and `OPEN_WORK.md:113`), if a non-LDB refresh heat floor \(\ge kT\,\Gamma\,g(\varepsilon)\) per record holds (`T59` leaves this **OPEN**, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:17, 172`), \(N_V\) refreshed bulk records generate volume-proportional repair heat; paired with a stated physical input that heat sheds only through the boundary at bounded flux per unit area, refreshed stock is capped by area times shed flux over \(kT\,\Gamma\,g(\varepsilon)\), without Planck units (`theory/AREA_LAW_PROBE_2026-11-23.md:143`).
   - *What would break Link 3b:* Passive error-correcting media whose logical leak rate drops with block size at vanishing ongoing repair heat (`theory/AREA_LAW_PROBE_2026-11-23.md:143`), or failure of a non-LDB refresh floor to hold.
   - *Next proof:* **T63 (record-repair heat floor, in flight)** — prove or refute the non-LDB repair floor and test passive error correction against it.

3. **Link 3c — Horizon-temperature input fixes the coefficient without supplying \(G\) (CONJECTURE).**
   The cost of judgment contains neither \(G\), \(\hbar\), nor \(c\) (`theory/AREA_LAW_PROBE_2026-11-23.md:17, 135`). Supplying one external physical input — that a horizon sheds heat at the Unruh or Hawking temperature (Unruh 1976, doi `10.1103/PhysRevD.14.870`; Hawking 1975, doi `10.1007/BF02345020`; `theory/AREA_LAW_PROBE_2026-11-23.md:39, 43, 145`) — could fix the temperature and shed-flux scale in a T63-type cap without the cost itself generating \(G\) or Planck units. Until then, `theory/SCALE_ENDS.md:180-188, 192, 247, 254` and `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:182-188` keep black holes as the extreme of the frozen class with the area law and Page curve as **inputs**, not outputs.
   - *What would break Link 3c:* If the stock cap comes entirely from the gravitational or causal input (Bekenstein 1973, doi `10.1103/PhysRevD.7.2333`; Bousso 2002, doi `10.1103/RevModPhys.74.825`; Casini 2008, doi `10.1088/0264-9381/25/20/205021`) while the cost of judgment adds only a relabeling (`theory/AREA_LAW_PROBE_2026-11-23.md:145`), or if T63 fails to yield a volume-repair-to-surface-shedding cap.
   - *Next proof (queued):* **After T63, run a horizon-temperature input test** (`theory/AREA_LAW_PROBE_2026-11-23.md:145`) stating the Unruh/Hawking temperature and shed-flux input explicitly and testing whether T63's cap recovers \(S\propto A\) (and whether any prefactor matches) without circularly assuming \(S\le A/(4\ell_p^2)\).

4. **Link 3d — From an area law plus thermodynamics to Einstein's equations (KNOWN, prior art — Jacobson 1995).**
   Jacobson (1995, *Phys. Rev. Lett.* **75**:1260–1263, doi `10.1103/PhysRevLett.75.1260`, verified on Crossref) shows that local Rindler horizons, the Unruh temperature, the Clausius relation \(\delta Q = T\,dS\), and an area-proportional entropy \(S \propto A\) yield the Einstein equation as an equation of state (`theory/AREA_LAW_PROBE_2026-11-23.md:17, 51, 137`). That is the known link *from* an area law *to* gravity; GTAO does not produce general relativity.
   - *What would break Link 3d:* A repair-heat area cap that fails to satisfy the Clausius relation on local causal horizons, or breakdown of Jacobson's local-equilibrium / equivalence-principle premises for the repair budget.
   - *Next proof:* Check whether any post-T63 horizon-input cap meets the Clausius premise of Jacobson 1995 rather than matching area proportionality alone.

---

## 5. Level 4 — SPECULATION (and the IIT / consciousness path pointer)

- **Physics as the minimum-cost way for a universe to keep track of itself (SPECULATION).**
  Extending Wheeler's "it from bit" program (Wheeler 1992, doi `10.1111/j.1749-6632.1992.tb17083.x`; `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:120, 176`), the physics hypothesis asks whether physical record-keeping itself reflects this cost (`theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176-178`). Today the cost already presupposes a world, a system, a bath, and a temperature (`:176`), and `THEORY.md` and `CORE.md` make no claim at this level.
  - *What would break it:* Failure of Level 2 or Level 3 (e.g., T63 refuted by passive error correction, the horizon-temperature test adding no non-circular constraint, or a physical record-keeping system whose persistence cost is unrelated to this cost, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:180`).
  - *Next proof:* Deferred until Links 3b–3c are settled.

- **IIT / consciousness path pointer (SPECULATION / CONJECTURE; T56, `theory/IIT_PATH_2026-11-23.md`, `OPEN_WORK.md:107`).**
  Cost-based irreducibility \(I_J\) (extra expected tracking cost across the cheapest partition of a shared layer, `theory/IIT_PATH_2026-11-23.md:15, 25-45`) has IIT's min-over-cuts shape (**ANALOGY**, `:63`) while differing from Tononi's \(\varphi_s\) on stakes, external drivers, and exclusion (`:17, 61-69`). Identifying a paying shared layer with a conscious episode is a **CONJECTURE / SPECULATION** (`:19, 77`); `theory/BOOKENDS.md:74, 254, 407` keeps experience out of scope of proved GTAO and marks "GTAO shows X is conscious" as an **IMPOSTER**. Orch-OR is not implied (`theory/IIT_PATH_2026-11-23.md:101-109`).
  - *What would break it:* Preregistered misses of candidate tests C-IIT-1–4 or the weak-programme PCI-vs-stakes test (`theory/IIT_PATH_2026-11-23.md:89-97`), e.g., exclusion holding over overlapping paying layers or PCI failing to move with stakes at fixed wiring.
  - *Next proof:* Compute \(I_J\) beyond flat cuts (`theory/IIT_PATH_2026-11-23.md:117`) and decide whether to lock a weak-programme preregistration (`:79, 116`).

---

## 6. Queued next steps

1. **In flight:** T63 (record-repair heat floor for leaky records, `theory/AREA_LAW_PROBE_2026-11-23.md:143`).
2. **Queued next after T63:** a **horizon-temperature input test** (`theory/AREA_LAW_PROBE_2026-11-23.md:145`), combining T63's repair-heat cap with an explicit Unruh/Hawking horizon-temperature input and checking against Jacobson 1995 without assuming \(S\le A/(4\ell_p^2)\).
3. **In parallel (Level 2):** qualify, preregister, and hash-lock one real strongly selected system (`CORE.md:148, 156`, `OPEN_WORK.md:47`).

---

## 7. Sources

- **Jacobson, T. 1995.** Thermodynamics of Spacetime: The Einstein Equation of State. *Phys. Rev. Lett.* **75**:1260–1263. doi `10.1103/PhysRevLett.75.1260` (verified on Crossref API `api.crossref.org/works/10.1103/PhysRevLett.75.1260`, 23 November 2026).
- Other primary physics DOIs cited above (`Horowitz & Esposito 2014`, `Sandberg et al. 2014`, `Hartich et al. 2016`, `Unruh 1976`, `Hawking 1975`, `Bekenstein 1973`, `Bousso 2002`, `Casini 2008`, `Wheeler 1992`) are already Crossref-verified in `theory/area_law_probe_checks/crossref.out` and `theory/drift_heat_lift_checks/crossref.out`.
- Internal citations follow `main` at `c67bc0b`: `CORE.md`, `OPEN_WORK.md`, `theory/SCALE_ENDS.md`, `theory/BOOKENDS.md`, `theory/HOLOGRAPHIC_2026-11-22.md`, `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`, `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md`, `theory/GENERAL_FLOOR_ATTEMPT_2026-11-23.md`, `theory/DRIFT_HEAT_LIFT_2026-11-23.md`, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md`, `theory/GENERAL_FLOOR_FINITE_2026-11-23.md`, `theory/FEEDBACK_FLOOR_2026-11-23.md`, `theory/CONTINUOUS_A6_2026-11-23.md`, `theory/NON_GAUSSIAN_FLOOR_2026-11-23.md`, `theory/AREA_LAW_PROBE_2026-11-23.md`, and `theory/IIT_PATH_2026-11-23.md`.
