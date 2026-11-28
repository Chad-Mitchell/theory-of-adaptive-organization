# Is computation missing from the cost of judgment?

*First written Friday 27 November 2026, about 11:55 PM ET; revised the same night after an independent read (see 'Corrections after review' below). Grok Bot executor, for Chad. Read against a fresh clone of `main` at `52898e7e77ddb4c33df3d646a890e3af1dc524a4` (committed 10:42 PM ET). README.md (143 lines), CORE.md (170) and THEORY.md (603) were read in full. Line citations are to that commit. The algebra, citations and references were read by an independent reader, and the scope edits that reader required are made below. Line citations are to `52898e7`; since then `#306` moved frozen trees under `records/` and results under `theory/` (`main` is now `f6610917e02aa7a0490d073f55566c337d36ea9a`), and the cited lines of `CORE.md`, `README.md` and `THEORY.md` are byte-identical there except `CORE.md:138`, which differs only in a moved-path link. Compute ran at nice 19. No Lean was needed, so `/tmp/gtao-lean` was not used. Scripts and outputs are in this folder: `findings_checks/` in this folder: `derive.py`/`derive.out`, `speed_heat.py`, `speed_heat2.py`, `sim_check.py`/`sim_check.out`, `crossref.out`, `arxiv_abstracts.txt`. The test that section 5 proposed is `PREREG.md` and `RESULTS.md` in this folder.*

Labels: **PROVED (in-model)**, **KNOWN**, **OPEN**, **CONJECTURE**, **SPECULATION**, as in `CORE.md:165`.

## 0. Answer in plain words

- **Reading.** The heat cost of computing is **absent as a term** from the cost CORE governs. Three parts of it are covered under other names:
  - the *time* computation takes, because lateness counts as error (`THEORY.md:31`);
  - the *information* it creates or erases, through the learning-rate floor and Landauer (`CORE.md:70`, `THEORY.md:36`);
  - the rest, which can only be soaked up by **assumed** prices: the read price A, layer upkeep h, the redesign lump k, and "compute" named as a currency (`CORE.md:42`, `THEORY.md:30`, `THEORY.md:182`, `THEORY.md:36`, `README.md:23`).
- **The prior memo is mostly right, with two errors.** Search cost has no designated term. It does not "sit in A", because A is *acquisition* spend (`THEORY.md:32`). And "physics gives no floor" is false once time is finite.
- **The sharper statement:** the theory prices information **at unlimited speed**. What it doesn't price is **speed**. Every floor CORE quotes is reached only by a memory that is infinitely fast ("a fast copy", `CORE.md:74`; "a fast spring", `CORE.md:76`; "a fast linear memory", `CORE.md:90`). Physics (finite-time Landauer bounds, speed limits, optimal transport, TURs) says doing anything in finite time, with finite mobility, costs heat beyond the information. So the missing half isn't really "computation versus information". It is **finite-time dissipation**, and it applies to updating memory, to reads, and to search alike.
- **Two derivations in this memo:**
  - **D1, PROVED (in-model):** CORE's own worked class (one OU signal, one linear one-pole memory), with that memory's relaxation rate capped at g.
    - For a **one-pole** memory (one linear coordinate with one relaxation rate g), error has a wall: ε > a v/(a+g). The wall is not general: an independent reader found a two-pole linear memory with both rates ≤ g at ε = 0.1504, below the one-pole wall 0.1667 at g = 5 (heat 161.0, far above the floor). So the cap is a cap on one relaxation rate of a one-pole memory, not on "memory speed" in the class.
    - Within that one-pole family the heat floor rises by an exact factor.
    - Within it the minimized cost becomes J* = 2√(kT a v w · g/(a+g)) − kT a + w v a/(a+g).
    - Within it the "when memory pays" threshold moves from x = 1 to x = 1 + a/g.
    - So the cap moves the design, not just the price level, **inside the one-pole family**. Whether it does for a memory of any form with every rate ≤ g is OPEN.
  - **D2, PROVED (in-model):** a Brownian computer of logical depth N that must finish in time τ dissipates at least 2kT·N·asinh(N/(2ντ)), **inside the nearest-neighbour chain whose per-step geometric-mean rate is ν** (not a speed cap, see §3.2). Traded against lateness, its minimized cost is 2N√(kT μ_d w q/ν). That is linear in **depth**, so under stated assumptions J can tell a deep conclusion from a shallow one.
- **The read price A.** It gets a heat **floor**, kT·f·I_read + kT·(ℓ²/D_r)·f² per register, but it is not *derived*: real reads sit far above it (`THEORY.md:183`). So #305's open item narrows but doesn't close.
- **Assessment.**
  - It's a real gap and a modest, probably partly known, extension.
  - As a route to the deeper physics link: **low odds, about 1 in 20 or less**. The one concrete mathematical bridge it touches is known: the minimum-dissipation protocol solves a kinetic least-action problem (Benamou–Brenier; Aurell et al. 2011).
  - Run: `PREREG.md` / `RESULTS.md` in this folder (outcome Y within n ≤ 4, one-sided; the diffusion class is not tested).

## 1. The reading from the source, arguing both sides

### 1.1 What the cost is, verbatim

- CORE defines the object as "being wrong or late plus the cost of holding, acquiring, and sharing information, under a cap on the chance of ruin" (`CORE.md:5`). THEORY says the same: "holding memory, being wrong or late, and buying and sharing the information" (`THEORY.md:11`). Neither definition contains a word for processing or inference steps.
- The adopted display is \(J=\dot Q+w\,\mathbb E[\ell]\) s.t. \(P(\text{ruin})\le\varepsilon\) (`CORE.md:27`, `README.md:21`). \(\dot Q\) is "the heat the memory's bath gives off" (`README.md:23`), with floor \(\dot Q_M\ge kT\,\dot I_M\), "where \(\dot I_M\) is the net information flow of the memory's own transitions" (`CORE.md:70`).
- The five-term sum's leftover terms: A "Stays assumed as a separate summand. A continuous coupling's read is inside \(\dot Q\)" (`CORE.md:42`). In THEORY, A is "information-acquisition spend, priced per read (Σ c_k f_k …), per nat acquired (λ), or per unit of precision" (`THEORY.md:32`). L is "link, telling and lookup costs" (`THEORY.md:33`), and h·K is layer upkeep (`THEORY.md:30`).
- The act is a free function of memory: "actions A_t = π(M_t)" (`THEORY.md:208`). CT1's proof uses only data processing, "A_t is a function of M_t" (`THEORY.md:265`). No cost attaches to evaluating π.

### 1.2 The case that computation is covered (the hostile reading, taken seriously)

1. **Memory dynamics are computation, and they are charged.** In the physical class the "memory's own transitions" (`CORE.md:70`) are the physical process that updates the estimate. In the worked class the optimal filter *is* that process: a spring, or a two-state copy (`CORE.md:74`, `CORE.md:76`, `CORE.md:90`). For these systems, updating the estimate is the memory relaxing, and its heat is \(\dot Q\).
2. **Erasure is charged.** THEORY's price floors include "at least kT per nat acquired or erased by a measuring tracker, and kT·(I_mem − I_pred) for memory that does not predict: Landauer 1961, Still et al. 2012" (`THEORY.md:36`). By Landauer and Bennett, erasure is the only *unconditional* thermodynamic cost of computing. So the theory already charges the one cost physics guarantees.
3. **Time is charged.** "Lateness counts as error, because a prediction that arrives after the moment to act buys nothing" (`THEORY.md:31`), with latency as a design limit in CT19 (`THEORY.md:412`). Slow thinking already costs through \(w\,\mathbb E[\ell]\).
4. **"Compute" is named as a currency.** "One currency per system (heat, attention, money, compute)" (`THEORY.md:36`), and "what binds there is the same term priced in the system's own currency: attention, money, compute" (`README.md:23`). Above the cell the terms are explicitly priced in compute.
5. **Deliberation as information is credited prior art.** THEORY credits "information-theoretic bounded rationality (Ortega & Braun 2013)" and "hierarchies that arise from information-processing costs (Genewein … 2015)" (`THEORY.md:195`). In that framework deliberation is priced as a KL divergence in nats, so "computation = information processing" is a respectable, published position.
6. **Assumed lumps can absorb it.** The redesign cost k (CL19, `THEORY.md:182`; "The cost of redesign is still open", `CORE.md:108`) is literally the cost of computing a new design. Upkeep h, read price A and lookup price u are assumed and could carry processing. A "price on speed (upkeep h0 + h1/τ, h1 > 0)" already appears once (`THEORY.md:19`).
7. **The repo already found one non-information cost.** T68 says "A gap in the heat floor. The floor at `CORE.md:70` charges kT times the learning rate. That charge is zero for a world that changes predictably", and it prices the clock with the TUR (`theory/CLOCK_TERM_2026-11-23.md:11`, independently reviewed twice). T63 prices repairing a leaky record (`theory/RECORD_REPAIR_FLOOR_2026-11-23.md:11`). Costs of keeping time and correcting errors are being added class by class, which is the theory's stated method (`CORE.md:144`).

### 1.3 The case that it is missing

1. **Information-plus-erasure is blind to depth.** Points 1–2 charge only the nats that flow or are erased. Two memories that end with the same information pay the same floor, however many intermediate steps one of them needed. MEMO Proposition 2 is right that "learning one constant bit costs at most ln 2 nats" (`/workspace/proofs-gtao/MEMO.md:51`, not in repo). Under Bennett, a reversible search adds no forced heat at *zero speed*, so point 2 is complete only at zero speed.
2. **Every floor CORE quotes is reached at unlimited speed.** "The design that approaches it is a fast copy at the minimal affinity" (`CORE.md:74`). "A fast spring at the same error reaches the infimum" (`CORE.md:76`). "approached by a fast linear memory at finite heat" (`CORE.md:90`). The rates are free design variables with no price, so the quoted minima assume infinitely fast computation. D1 (§3.1) shows this changes the minimum and the design.
3. **Point 3 gives the time side but not the heat side.** Lateness charges slow thinking. Nothing charges *fast* thinking. Physics says faster costs more heat (§2), so with only lateness priced, the theory's optimum always says to think infinitely fast.
4. **Points 4–6 are assumptions, not terms.** A currency name doesn't make a quantity. No term in J has *steps*, *depth* or *duration of computing* as its argument. CORE itself lists the stake, link price and ruin cap as unexplained assumptions (`CORE.md:155`). A, h and k are in the same position: what they cost isn't explained, and nothing there scales with how hard the inference is.
5. **The theory says a missing term matters.** "A wrong or missing cost breaks the theory: no regret bound covers a cost J cannot book" (`THEORY.md:73`). "A cost the list omitted is a miss of the same kind" (`CORE.md:138`).
6. **T68 and T63 are not in CORE.** `rg -i "clock|T68" CORE.md` returns nothing. T63 appears only as a rung of the physics chain (`CORE.md:149`). CORE's display has no non-information heat term today.

### 1.4 Reading of the source

| Part of computing | Status in CORE/THEORY | Lines |
|---|---|---|
| Information learned (net flow) | Covered, with a floor | `CORE.md:70` |
| Information erased, nostalgia | Covered as a price floor in frozen THEORY. Not in CORE's display | `THEORY.md:36`, `THEORY.md:283` |
| Time taken | Covered, through lateness | `THEORY.md:31`, `THEORY.md:412` |
| Heat of doing it in finite time (speed) | **Absent.** Every quoted floor is reached at unlimited rate | `CORE.md:74`, `CORE.md:76`, `CORE.md:90` |
| Depth or steps of inference or search | **Absent.** It can only be absorbed into assumed A, h, k or "compute" prices | `CORE.md:42`, `THEORY.md:30`, `THEORY.md:36`, `CORE.md:108` |
| Evaluating the act π(M) | **Absent.** Free by assumption | `THEORY.md:208`, `THEORY.md:265` |
| Clock precision, repair | In notes outside CORE (T68, T63) | `theory/CLOCK_TERM_2026-11-23.md:11`, `CORE.md:149` |

**Claim tested** ("the theory prices information, not computation; the heat floor charges kT per nat learned (`CORE.md:70`), and search cost sits in the read price A, assumed with no floor (`CORE.md:42`)"):
- **Half 1, the floor charges kT per nat learned (`CORE.md:70`):** accurate.
- **Half 2, search cost sits in A:** this is an interpretation the source doesn't support. A is acquisition (`THEORY.md:32`), and search has *no* designated term.
- **"No floor" (the memo also says physics gives none):** true of A in CORE, false of physics. §2 gives the conditional finite-time floors.

**Why the theory still looks so precise about memory, layers and swarms:** its worked classes are linear-Gaussian or two-state (`CORE.md:86`). In those classes the Bayes act is a linear readout or a copy, with depth O(1), and the inference *is* the memory's own relaxation. Computation is negligible there by the choice of class, apart from speed. The gap shows up where the optimal act is hard: nonlinear filtering, planning, search, proof. That is outside every worked class.

## 2. What physics says computation must cost (citations checked on Crossref or arXiv tonight; see `crossref.out`, `arxiv_abstracts.txt`)

1. **Erasure, KNOWN.** Logically irreversible operations cost at least kT ln 2 per bit erased. Landauer 1961, *IBM J. Res. Dev.* 5:183, doi 10.1147/rd.53.0183. Measurement plus erasure together cost at least kT per nat of information acquired: Sagawa & Ueda 2009, *PRL* 102:250602, doi 10.1103/PhysRevLett.102.250602 (arXiv:0809.4098).
2. **Reversibility, KNOWN.** Any computation can be made logically reversible (compute, copy, uncompute), so no heat is forced per step in the zero-speed limit: Bennett 1973, doi 10.1147/rd.176.0525. The price moves into time and space: Bennett 1989, *SIAM J. Comput.* 18:766, doi 10.1137/0218053. A Brownian computer's dissipation per step falls as it is driven more slowly, and ballistic computers need error correction against noise: Bennett 1982, doi 10.1007/BF02084158. **No floor per logical step holds for every implementation.**
3. **Finite time, KNOWN.**
   - *Overdamped dynamics:* a process taking a distribution p₀ to p_τ in time τ, with diffusion D = μkT, produces entropy \(\Sigma\ge W_2(p_0,p_\tau)^2/(D\tau)\). This is the optimal-transport refined second law, with equality on a Benamou–Brenier geodesic: Aurell et al. 2011, *PRL* 106:250601, doi 10.1103/PhysRevLett.106.250601; Aurell et al. 2012, *J. Stat. Phys.* 147:487, doi 10.1007/s10955-012-0478-x; Benamou & Brenier 2000, doi 10.1007/s002110050002; Nakazato & Ito 2021, *PRR* 3:043093, doi 10.1103/PhysRevResearch.3.043093.
   - *Erasing one bit in time τ:* this costs kT ln 2 plus a positive excess that falls as 1/τ at long times: Proesmans, Ehrich & Bechhoefer 2020, *PRL* 125:100602, doi 10.1103/PhysRevLett.125.100602 (arXiv:2006.03242). A bound that holds for any hardware obeying detailed balance, as a function of duration and reset error: Zhen et al. 2021, *PRL* 127:190602, doi 10.1103/PhysRevLett.127.190602 (arXiv:2106.00580). The excess grows sharply for highly irreversible fast operations: Lee et al. 2022, *PRL* 129:120603, doi 10.1103/PhysRevLett.129.120603 (arXiv:2204.07388). Quantum case: Van Vu & Saito 2022, *PRL* 128:010602, doi 10.1103/PhysRevLett.128.010602.
   - *Markov jump processes:* the speed of a state change is bounded by entropy production times dynamical activity: Shiraishi, Funo & Saito 2018, *PRL* 121:070601, doi 10.1103/PhysRevLett.121.070601. This is unified with discrete optimal transport and the TUR in Van Vu & Saito 2023, *PRX* 13:011013, doi 10.1103/PhysRevX.13.011013 (arXiv:2206.02684).
   - *Slow driving:* excess work is at least the squared thermodynamic length over τ: Salamon & Berry 1983, doi 10.1103/PhysRevLett.51.1127; Sivak & Crooks 2012, doi 10.1103/PhysRevLett.108.190602; Schmiedl & Seifert 2007, doi 10.1103/PhysRevLett.98.108301.
4. **Precision, KNOWN (TUR).** For any current in a nonequilibrium steady state, Var/mean² ≥ 2/Σ: Barato & Seifert 2015, doi 10.1103/PhysRevLett.114.158101; Gingrich et al. 2016, doi 10.1103/PhysRevLett.116.120601; review Horowitz & Gingrich 2020, *Nat. Phys.* 16:15, doi 10.1038/s41567-019-0702-6. A computation that must finish on time with relative timing error ε_r pays Σ ≥ 2/ε_r², whatever its depth.
5. **Stochastic thermodynamics of computation, KNOWN.**
   - Entropy production splits into a Landauer cost, a *mismatch* cost (from running a device built for one input distribution on another) and a residual: Kolchinsky & Wolpert 2017, doi 10.1088/1742-5468/aa7ee1; Wolpert 2019 review, *J. Phys. A* 52:193001, doi 10.1088/1751-8121/ab0850 (arXiv:1905.05669).
   - Circuits whose topology restricts which variables can couple carry extra, architecture-dependent costs: Wolpert & Kolchinsky 2020, *NJP* 22:063047, doi 10.1088/1367-2630/ab82b8 (arXiv:1806.04103).
   - Turing machines: Kolchinsky & Wolpert 2020, *PRR* 2:033312, doi 10.1103/PhysRevResearch.2.033312. Overview: Wolpert et al. 2024, *PNAS* 121:e2321112121, doi 10.1073/pnas.2321112121.
   - This is the closest published framework to "how you compute changes what it costs".
6. **Error correction and reliability, KNOWN.**
   - Kinetic proofreading buys accuracy with dissipation: Hopfield 1974, doi 10.1073/pnas.71.10.4135; Bennett 1979, doi 10.1016/0303-2647(79)90003-0.
   - A second-law expression links copy error to entropy production: Sartori & Pigolotti 2015, *PRX* 5:041039, doi 10.1103/PhysRevX.5.041039.
   - Copying with a persistent copy: Ouldridge, Govern & ten Wolde 2017, doi 10.1103/PhysRevX.7.021004.
   - Energy, speed and accuracy in adaptation: Lan et al. 2012, *Nat. Phys.* 8:422, doi 10.1038/nphys2276.
   - The repo's own repair floor, T63 (`CORE.md:149`).
7. **Quantum speed limit, KNOWN.** The rate of distinguishable state changes is bounded by energy, at most 2E/(πħ) operations per second (Margolus & Levitin 1998, doi 10.1016/S0167-2789(98)00054-2; Lloyd 2000, doi 10.1038/35023282). It bounds energy *held*, not heat dissipated.

**Answer to "does physics give a floor on computation done in finite time with finite error?"** Yes, but only conditionally:
- **Under three conditions there is one:** a dissipative implementation (Markov jump with detailed balance, or overdamped Langevin), finite mobility or activity, and finite duration. The excess heat is then at least kT times a squared transport distance over the duration, and finite error adds the Landauer and proofreading terms.
- **Without those conditions there isn't one:** a ballistic or coherent machine with perfect isolation has no such floor (Bennett 1982).

## 3. Computation in the theory's own terms, and candidate terms for J

**Definition.** A judgment step maps (memory, observation) to (new memory, act): \(\Phi:(M_t,Y_t)\mapsto(M_{t^+},A_t)\). Its cost has five physical coordinates:

| Coordinate | Symbol | Units | In CORE? |
|---|---|---|---|
| Net information learned | \(\dot I_M\) | nats/time | yes (`CORE.md:70`) |
| Entropy discarded (logical irreversibility of Φ) | \(\Delta H_\Phi\) | nats per step | only as a THEORY price floor (`THEORY.md:36`) |
| Logical depth: sequential elementary steps the implementation must pass through | \(N\) | dimensionless | no |
| Duration of one judgment | \(\tau\) | time | only through lateness (`THEORY.md:31`) |
| Implementation speed: bare step rate, or memory relaxation rate | \(\nu\) or \(g\) | 1/time | no; it is free in every quoted infimum |

Units follow CORE: kT is an energy; \(\dot Q\) and J are energy per unit time; v, ε and q are loss units (q per unit time). w has no units line in CORE. It is inferred from `CORE.md:91` as energy per unit time per unit loss (the same inference as MEMO §1).

### 3.1 D1: CORE's worked class with a finite relaxation rate of a one-pole memory (PROVED in-model; sympy, `speed_heat.py`, `speed_heat2.py`, `derive.py`; Monte Carlo, `sim_check.py`)

**Class.**
- Signal: \(dx=-a x\,dt+\sqrt{2av}\,dW_1\), exogenous, with rate a and variance v.
- Memory: one overdamped coordinate \(dm=\mu(-\kappa m+\lambda x)dt+\sqrt{2\mu kT}\,dW_2\), from the potential \(U=\kappa m^2/2-\lambda m x\), with local detailed balance on the memory bath.
- Memory relaxation rate \(g=\mu\kappa\). This caps the bandwidth of the one pole. It does not cap the coupling \(\lambda\) (so \(s\) is unbounded), so the wall below is a bandwidth wall, not a cap on the rate of heat.
- Decision error ε = Var(x | m), the MMSE.
- Heat into the memory bath: \(\dot Q=\mu\langle F^2\rangle-kT\mu\kappa\) (Sekimoto).

**Results.**
- Steady state (Lyapunov solution): \(\dot Q=kT\,a g s/(a+g)\) with \(s=\kappa(\lambda/\kappa)^2v/kT\). Monte Carlo at g = 5, s = 1.6: 1.3356 ± 0.0134 against 1.3333 (`sim_check.out`).
- **One-pole speed–accuracy wall:** \(\varepsilon>\varepsilon_{\min}(g)=a v/(a+g)\) at any heat, for a one-pole memory only.
- **One-pole heat floor at relaxation rate g** (within this family only): \(\dot Q_{\min}(\varepsilon;g)=kT\,a\,\dfrac{v-\varepsilon}{\varepsilon}\cdot R,\quad R=\dfrac{1}{1-\varepsilon_{\min}(g)/\varepsilon}\). As g → ∞ this is CORE's infimum \(kT a(v-\varepsilon)/\varepsilon\) (`CORE.md:90`). At large g the excess falls as 1/g, the same 1/τ scaling as the finite-time results in §2.3.
- **Minimized cost:** \(J^*(g)=2\sqrt{kT\,a v w\,\dfrac{g}{a+g}}-kT\,a+w v\,\dfrac{a}{a+g}\). This matches brute-force minimization (6.440169 at kT = a = v = 1, w = 10, g = 5), against CORE's g → ∞ value of 5.324555 (`CORE.md:91`).
- **Threshold:** memory pays iff \(x=wv/(kT a)>1+a/g\). That replaces x > 1 (`README.md:17`, `CORE.md:91`).

**Scope.** This holds for one-dimensional linear memories with one relaxation rate g, and for no wider family. The wall is **not general**: an independent reader (Lyapunov solution and Nelder–Mead search, a = v = kT = 1, g = 5) found a two-dimensional gradient linear memory with both relaxation rates ≤ g (5.0 and 1.857) reaching ε = 0.1504 < 0.1667 at heat 161.0 (a lead-compensator: x ≈ m₁ + m₁′/g, built from two poles at rates ≤ g). At ε = 0.25 the two-pole optimum collapsed onto the one-pole curve (heat 8.9993 against 9.0000); nothing is shown about optimality anywhere, and a search at ε = 0.10 was inconclusive. So the threshold shift 1 + a/g and J*(g) are results for the one-pole family; they may move once any multi-pole memory with all rates ≤ g is allowed. Whether a nonlinear or multi-dimensional memory with every rate ≤ g beats the one-pole heat floor is **OPEN**. The speed cap is the one added assumption.

**Prior art, and how short the search was.** The components are classical (the first-order lag error \(va/(a+g)\) is Wiener–Kalman material), and the closest published work I found is Barato, Hartich and Seifert 2014, "Efficiency of cellular information processing" (*New J. Phys.* 16:103024, doi 10.1088/1367-2630/16/10/103024) and Hartich, Barato and Seifert 2016, "Sensory capacity: an information theoretical measure of the performance of a sensor" (*Phys. Rev. E* 93:022116, doi 10.1103/PhysRevE.93.022116; both resolve on Crossref), which give entropy production and learning rate for linear Langevin sensors following an external signal; the repo already cites Barato, Hartich and Seifert 2014 at `THEORY.md:295` (CT7). In this class the ratio \(\dot Q/(kT\dot I_M)=R\) is the efficiency those groups study, so a version of the closed form may exist there. I found no paper stating \(J^*(g)\) or the \(1+a/g\) threshold, but the search was short (three queries, not exhaustive): components known, combination not found. **The repo already states a finite-rate "implementation excess"** (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:66`, `:140`, `:171`), so D1's novelty over `main` is lower than the first draft of this memo said. Lan et al. 2012 (adaptation networks) is adjacent and not a pointer for this closed form.

### 3.2 D2: depth N in finite time (PROVED in-model for the Brownian chain; `derive.py`)

**Class.** A computation is a chain of N logically distinct states traversed in order, with forward and backward rates \(\nu e^{\pm b/2}\) (detailed balance, driving b per step). The rate \(\nu\) is the **geometric mean** of the forward and backward rates, so the forward rate \(\nu e^{b/2}\) is not bounded. (The step rate is called \(\nu\), not k, because k is the redesign lump at `THEORY.md:182` and kT is the thermal energy.) Finishing on average by τ needs \(2\nu\sinh(b/2)\tau=N\), and the heat is kT·N·b:

$$Q_{\rm comp}(N,\tau)=2kT\,N\,\operatorname{asinh}\!\Big(\frac{N}{2\nu\tau}\Big)\;\approx\;kT\,\frac{N^2}{\nu\tau}\quad(\nu\tau\gg N).$$

**Scope of "at least".** The formula is a lower bound inside the nearest-neighbour chain with a fixed geometric-mean rate \(\nu\) per step (with per-step biases \(b_i\), the heat \(kT\sum b_i\) is convex in the per-step time, so the uniform chain is the optimum by Jensen's inequality). It is not a bound on "an N-step computation" in general, and \(\nu\) is not a speed cap. The slow form is the Brownian-computer scaling (Bennett 1982, dissipation per step proportional to speed) and the optimal-transport scaling. The growth "only logarithmic in speed" at large \(N/(\nu\tau)\) holds only because the forward rate \(\nu e^{b/2}\) is allowed to grow exponentially. Under a hard cap K on the largest rate, the entropy per step at net step rate \(v=N/\tau\) per step is \(\ln(K/(K-v))\), which **diverges at \(v=K\)** and exceeds \(2\,\mathrm{asinh}(v/2K)\) (at \(v/K=0.5\): 0.693 against 0.495). So D2 is correct for the bare step rate as defined and is not a speed-limit result. It is also a statement about the mean finishing time only: the relative variance of the first-passage time is \(1/(N\tanh(b/2))\), which can exceed 1 in the slow regime, so a deadline "by τ" needs the TUR term of §2.4 on top.

**Candidate term in J.** Judgments occur at rate \(\mu_d\), each needs depth N, and the world is a random walk whose error grows by qτ during the computation (lateness, `THEORY.md:31`):

$$J=\dot Q_M+\mu_d\,Q_{\rm comp}(N,\tau)+w\big(\mathbb E[\ell]+q\tau\big).$$

**Results in the slow regime.**
- \(\tau^*=N\sqrt{kT\mu_d/(\nu\,w q)}\), and \(J^*_{\rm comp}=2N\sqrt{kT\,\mu_d\,w q/\nu}\).
- The ratio to CT7's information floor \(\sigma\sqrt{2kTw}\) (`THEORY.md:295`, with σ² = q) is \(N\sqrt{2\mu_d/\nu}\). **Computation dominates once depth exceeds \(N_c=\sqrt{\nu/(2\mu_d)}\).** For example, a step rate of 10³/s and one judgment per second give N_c ≈ 22. This is an illustration with no system qualified.
- The slow regime holds iff \(wq\ll4\nu\,kT\,\mu_d\). Outside it, use the asinh form.
- **What it means:** under these assumptions J charges logical **depth**, so it can tell a deep conclusion from a shallow one (contrast `/workspace/proofs-gtao/MEMO.md:171`, not in repo). Parallel hardware divides the N² term by the number of independent chains P, but each chain costs upkeep. That trade is CONJECTURE, not derived.

### 3.3 Does this turn A into heat? Partly: a floor, not a derivation

Treat a discrete read as writing a register and then resetting it, in time \(\tau_r\le1/f\) for one register.
- **Information part:** at least \(kT\,I_{\rm read}\) per read (Sagawa–Ueda; already a THEORY price floor, `THEORY.md:36`, `THEORY.md:95`).
- **Finite-time reset:** at least \(kT\,\ell_r^2/(D_r\tau_r)\), with \(W_2=\ell_r\) for the reset transport (Aurell 2012; Proesmans 2020 for one bit).
- **Together:** \(A\ge kT\,f\,I_{\rm read}+kT\,(\ell_r^2/D_r)\,f^2\) per register.
- **Effect on CT12 at α = 2** (`THEORY.md:338`): a price per read that rises with the read rate changes the read rate's stake elasticity from 1/2 to 1/3 once the rate term dominates. That is a **CONJECTURE** as a field signature, because real read costs sit 10⁵–10⁶ times above the floor (`THEORY.md:183`).
- **For #305:** this gives the "priced discrete read" a heat floor in a stated class. The price itself stays assumed, the same status \(\dot Q\) has above the cell.
- **Exact reads** (CT11, CT12, "exact reset reads", `THEORY.md:321`, `THEORY.md:336`) would need infinite information about a continuous state, so they aren't physical.

### 3.4 Assumptions this adds (exactly)

- **B1.** The implementation is dissipative: a Markov jump process with local detailed balance, or overdamped Langevin. Ballistic, Hamiltonian and coherent quantum machines are excluded.
- **B2.** A bounded speed: relaxation rate g of one pole (D1), bare geometric-mean step rate ν (D2; not a cap on the largest rate), or register diffusion D_r (§3.3).
- **B3 (D2 only, load-bearing).** The computation must pass through N distinct intermediate states. A protocol that transports directly from input to output would pay only \(W_2(p_0,p_\tau)^2/(D\tau)\). For a fixed circuit architecture, intermediate states are forced (Wolpert & Kolchinsky 2020).
- **B4.** Computing time is lateness, via `THEORY.md:31`.
- **B5.** The computation's heat and the memory-bath heat add, with no shared degrees of freedom. Not checked beyond these classes.
- **B6.** Every result is a floor. None of it says what real systems pay.

## 4. Honest assessment

- **Real gap, restatement, or framing error?** A real gap with a framing correction.
  - *The gap:* CORE's display has no finite-time term, so every quoted minimum assumes unlimited speed. Charging speed moves designs (the D1 threshold and one-pole error wall, in the one-pole family only; the D2 depth–lateness trade, in the stated chain).
  - *The framing error:* "information versus computation". Physically, computation's only unconditional cost *is* information erased, which the theory has. The missing variable is **time**, and it applies to memory, reads and search alike.
  - *The restatement part:* the physics in §2 is all known, and D1 is probably known in substance.
- **Odds.**
  - That a reviewed version of D1/D2 survives as an in-model extension of CORE's floor: better than even, since it is short algebra with numeric and Monte Carlo checks.
  - That it leads to the physics link Chad hopes for: **low, roughly 1 in 20 or less.** The one real mathematical bridge it touches is known: the minimum-dissipation finite-time protocol is a Benamou–Brenier geodesic, a stationary point of a kinetic action (Aurell et al. 2011). That ties the cost of fast judgment to a least-action problem in the space of distributions. It is *not* the mechanical action of the separate least-action check. Identifying the two would be a new claim, unshown, and is labeled SPECULATION.
- **Wording discipline.** Nothing here derives gravity, quantum mechanics or forces.

## 5. The single next discriminating test

**Bounded-activity telegraph floor.** Prereg first, locked before any computation.
- **Claim H:** for every finite-state bipartite memory tracking the telegraph at rate r (CORE's tightest class, `CORE.md:74`) with every memory transition rate ≤ g_max (this prereg, in `PREREG.md`, uses an exit-rate cap and an edge cap; see there):
  - \(\dot Q_M\ge kT\,r\,L(\varepsilon)\,R_T(g_{\max}/r)\), with \(R_T>1\), and \(R_T\to1\) as \(g_{\max}\to\infty\);
  - \(\varepsilon\ge\varepsilon_{\min}(g_{\max}/r)>0\). (This second line holds for the two-state copy, \(r/(G+2r)\); the reader's two-pole result shows a wall of one family need not hold for a richer memory, so `PREREG.md` does not score it.)
- **Rival:** some bounded-rate memory reaches \(kT\,r\,L(\varepsilon)\) (R_T = 1). In that case D1's excess is an artifact of the linear family, and speed is not a cost of judgment.
- **Method:** exact for the symmetric two-state copy (closed form, sympy), then numerical optimization over n = 2, 3, 4 state memories with rates capped. If H holds, attempt a proof via the Shiraishi–Funo–Saito / Van Vu–Saito speed limit, with Lean for the two-state identity.
- **Why this test:** it decides cheaply, inside a class CORE already calls tight, whether "speed is the missing half" is physics of J or a design artifact.

## 6. What I did not do

- The first draft did not edit the repo. This revised copy lives in `theory/speed-cost-2026-11-27/`; `CORE.md`, `README.md` and `THEORY.md` are not edited. The test of section 5 was run as `PREREG.md` / `RESULTS.md` in this folder.
- D1's optimality over all bounded-rate memories is OPEN (it is a one-pole result). D2 is one chain class, with a geometric-mean rate that is not a cap.
- The prior-art search for D1's closed form was not exhaustive.
