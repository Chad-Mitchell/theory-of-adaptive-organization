# Preregistration: does a speed-capped memory pay more than CORE's telegraph floor, or is the excess an artifact of the two-state copy?

*Friday 27 November 2026 (America/New_York). Branch `speed-cost-2026-11-27`, cut from `main` `f6610917e02aa7a0490d073f55566c337d36ea9a` (#306, layout move: frozen trees under `records/`, results under `theory/`). Locked before any scored run: this file, `LOCK.txt`, the scripts in `checks/`, and the outputs of their toy-input runs (`checks/toy_checks.out`, `checks/toy_run_and_score.out`, `checks/paper_two_state.out`) go in one commit, which is pushed before the run (`process/PREREG_GATE.md` section 2, launch rule). Nothing scored below is computed before that commit and a committed gate read. The scored runs start from a fresh GitHub clone at the lock commit, at nice 19. `CORE.md`, `README.md`, `THEORY.md` and every locked or pinned file are not edited. No real-world data. Deviations go in `DEVIATIONS.md` in this folder, appended lines only.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels: **HYPOTHESIS** is a bet locked here. **OBSERVED** is on `main` at `f6610917e02aa7a0490d073f55566c337d36ea9a`, with a file and line. **PAPER** is a value worked out before any scored run, by the committed script `checks/paper_two_state.py` (closed form, no search). **TEST** passed the gate; **CONSISTENCY_CHECK** did not (`process/PREREG_GATE.md` section 3).

## 0. What this tests, and where it comes from

- OBSERVED. The telegraph floor: \(\dot Q_M\ge kT\,r\,L(\varepsilon)\), \(L(\varepsilon)=(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon}\), for any finite memory, tight at the symmetric two-state copy, "approached by a fast copy at the minimal affinity" (`CORE.md:74`; `CORE.md:70` for \(\dot Q_M\ge kT\dot I_M\)). The heat infimum is approached "as the memory rates diverge" and is not attained at any finite rate; a finite affinity pays an excess (`theory/GENERAL_FORM_PHYSICS_2026-11-22.md:66`). So **CORE already says the floor is a limit.** What `main` does not state is how the best memory of any form pays as the rate is capped.
- The question (from `FINDINGS.md` in this folder, section 5, which came first): with the memory's transition rates capped at \(g\), does the best capped memory, of any form we can search, still pay strictly more than \(kT\,r\,L(\varepsilon)\)? Or does some design reach the floor at finite \(g\), so that the excess seen for a one-pole linear memory (D1) and for the two-state copy is an artifact of the family?
- **Known case, recorded before the lock.** An independent reader of `FINDINGS.md` (notes outside the repo, `/workspace/rev-comp-gtao/REVIEW.md`) found, in the *linear diffusion* class (one OU signal, \(a=v=kT=1\), \(g=5\)), a two-pole memory with every relaxation rate \(\le g\) reaching error \(0.1504\), below the one-pole wall \(a v/(a+g)=0.1667\), at heat \(\dot Q=161.0\) (rates 5.0 and 1.857). So the one-pole wall in error is not general even in that class, and **this prereg does not assume any wall of the two-state copy is general**. In the jump class below the two-state copy has \(\varepsilon_{\min}=r/(G+2r)\); no bar scores the smallest reachable error, and every scored point sits at \(\varepsilon_0\ge1.25\,r/(G+2r)\), so a lower reachable error for \(n>2\) cannot change the scored quantity's definition. That counterexample is in a different class (continuous diffusions) and at a heat (161.0) far above the learning-rate floor \(kT\,a(v-\varepsilon)/\varepsilon\approx5.6\) at that error (my arithmetic from the reader's numbers); it neither supports nor contradicts the excess scored here, and it is why the search below includes multi-state designs.

## Gate

| ID | Label | G1 miss (honest odds) | G2 not an identity | G3 rival: same quantity, its value, gap, resolution | G4 reach | G5 next step |
|---|---|---|---|---|---|---|
| **SC-B1** | **TEST** | Miss if at any of the 13 grid points of arm A some design with \(n\le4\) states has excess \(E\le\tau=2\times10^{-4}\), i.e. reaches the floor. Odds of a miss 0.10 | Passes for \(n=3,4\): no closed form, the optimum is searched. The \(n=2\) part is a **CONSISTENCY_CHECK** (closed form, PAPER) | **Floor-reachable reading** (the excess is an artifact): some capped design has \(E\approx0\). **Cap reading**: no design does. Smallest PAPER two-state excess on the grid is \(1.6\times10^{-3}\), eight times \(\tau\); resolution of the search is about \(10^{-7}\) relative in heat (section 5) | (a) toy class we built; carries to (b) `CORE.md:74` as a scoped statement about the speed cost of the tight class | Hit: speed stays a missing term in the telegraph class; next is a proof attempt (speed-limit bound) for \(n\) arbitrary. Miss: the floor is reachable at a finite cap in this class; the D1 excess is a family artifact and the speed claim is withdrawn there |
| **SC-B2** | **TEST** (headline) | Miss if at any grid point of arm A a 3- or 4-state design removes more than 10% of the best two-state excess: \(Q_{\rm frac}>0.10\) (section 3). Odds of a miss 0.40 | Passes: whether an \(n=3,4\) design beats the two-state copy at fixed error under an exit cap has no closed form here and is not fixed by `CORE.md:70-74`, which bound from below only | **Two-state-is-the-answer reading**: \(Q_{\rm frac}\approx0\) (the excess is that of the symmetric copy, PAPER values in section 2). **Artifact reading**: \(Q_{\rm frac}\) near 1. The partial outcome \(0.10<Q_{\rm frac}\) with B1 hit is separate. Gap between readings 0.1 to 1; resolution about \(10^{-6}\) in \(Q_{\rm frac}\) at a reproduced optimum | (a) toy; (b) `CORE.md:74` | Hit: the two-state excess is the excess of the best design searched; state D1's speed term for the telegraph class as a scoped result and try a proof. Miss: report \(Q_{\rm frac}\) and where; the two-state value overstates the excess by that share, and the design that does it is the next object |
| SC-B3 | **CONSISTENCY_CHECK** (gate: none (CONSISTENCY_CHECK)) | — | Fails G2: if B2 hits, the best excess lies in \([0.9E_2,E_2]\) and the ratio \(E(100)/E(1000)\) lies in \([9.05,12.14]\) from the PAPER values \(10.06\) to \(10.93\) (checked in `paper_two_state.out`), inside the band \([8,12.5]\) | — | — | Reported only: the scaling \(E\propto1/G\) |
| SC-B4 | **CONSISTENCY_CHECK** (gate: none (CONSISTENCY_CHECK)) | — | Fails G2, and was seen before the lock (section 7): with an edge cap each of \(n\) redundant states carries its own cap, so total speed grows with \(n\) | — | — | Arm B (edge cap) reported as a reading check: it shows that a per-edge cap is not a speed cap |

**Gate summary (self-check; a separate gate read is required before any run, section 8).** Two TESTs, both at reach (a) with a scoped route to (b). Two consistency checks, labeled. The search is one-sided: a design that reaches the floor proves existence; "no design found" is evidence, not a proof of none.

## 1. The model (every assumption is listed in section 6)

- World: symmetric telegraph \(x\in\{0,1\}\), flips at rate \(r\) each way. \(r=1\) sets the time unit, so \(G=g/r\).
- Memory: \(n\) states \(i\in\{1..n\}\), bipartite (only memory transitions change the memory). Memory transition rates \(W[x,i,j]\ge G\cdot10^{-9}\) for \(i\ne j\), possibly depending on \(x\). A stationary state is solved exactly on the \(2n\) joint states.
- Heat per unit time over \(kT\): \(\sum_{x,i\ne j}p[x,i]\,W[x,i,j]\,\ln\frac{W[x,i,j]}{W[x,j,i]}\) (local detailed balance on the memory's own transitions).
- Error: Hamming error of the best decoder \(\lambda:\{1..n\}\to\{0,1\}\) (searched over the decoder classes below). Achieved error is \(\varepsilon_{\rm ach}\).
- **Cap (arm A, primary): exit cap.** \(\sum_{j\ne i}W[x,i,j]\le G\) for every \((x,i)\): the memory leaves any state at total rate at most \(g\). **Arm B (secondary): edge cap.** Each \(W[x,i,j]\le G\).
- Excess of one design: \(E_d=\dot Q/(r\,L(\varepsilon_{\rm ach}))-1\), at its own achieved error. \(E(n)\) is the minimum of \(E_d\) over designs of \(n\) states found with \(\varepsilon_{\rm ach}\le\varepsilon_0+10^{-7}\) and cap violation \(\le10^{-7}\) (called admissible).
- Proved floor for any finite memory (T60 section 4; `CORE.md:74`): \(E_d\ge0\). A design with \(E_d<-10^{-6}\) is a code error (section 4).

## 2. PAPER values (closed form, before the lock)

Two-state copy, toward-rate at the cap \(G\), away-rate \(a_-=(\varepsilon G-r(1-2\varepsilon))/(1-\varepsilon)\): \(\dot Q/kT=r(1-2\varepsilon)\ln(G/a_-)\), feasible iff \(\varepsilon>r/(G+2r)\). Large-\(G\) excess \(E_2\approx r(1-2\varepsilon)/(\varepsilon G\ln\frac{1-\varepsilon}{\varepsilon})\). This strict excess is a CONSISTENCY_CHECK, because `GENERAL_FORM_PHYSICS_2026-11-22.md:66` already states a finite-rate excess. Grid A, 13 points: \(G\in\{5,20,100,1000\}\times\varepsilon_0\in\{0.05,0.1,0.2,0.3\}\), keeping \(\varepsilon_0\ge1.25\,r/(G+2r)\) (so \(G=5\): \(\{0.2,0.3\}\); \(G=20\): \(\{0.1,0.2,0.3\}\); \(G=100,1000\): all four).

| G | ε₀ | E₂ (PAPER) |
|---|---|---|
| 5 | 0.2 / 0.3 | 0.660964 / 0.366052 |
| 20 | 0.1 / 0.2 / 0.3 | 0.232487 / 0.117233 / 0.081427 |
| 100 | 0.05 / 0.1 / 0.2 / 0.3 | 0.067399 / 0.037949 / 0.021972 / 0.015842 |
| 1000 | 0.05 / 0.1 / 0.2 / 0.3 | 0.006169 / 0.003656 / 0.002167 / 0.001575 |

## 3. The bars, stated exactly

**The prediction that separates the outcomes.** Let \(E_{\rm best}\) be the lowest admissible excess found over \(n\in\{2,3,4\}\) and all decoder classes, at each of the 13 points, and \(Q_{\rm frac}=\max(0,\,1-\min(E(3),E(4))/E(2))\).

- **Outcome Y (the speed-capped optimal memory of the searched forms pays strictly more than CORE's floor, and the two-state copy sets the excess):** \(E_{\rm best}>\tau\) at all 13 points (B1 hit) **and** \(Q_{\rm frac}\le0.10\) at all 13 points (B2 hit).
- **Outcome P (excess persists, the two-state family overstates it):** B1 hit and \(Q_{\rm frac}>0.10\) at some point.
- **Outcome N (floor reachable, the excess is an artifact of the family):** \(E_{\rm best}\le\tau\) at some point (B1 miss).

**B1 (TEST).** HYPOTHESIS: \(E_{\rm best}>\tau=2\times10^{-4}\) at all 13 points. A miss is any point with \(E_{\rm best}\le\tau\).
**B2 (TEST, headline).** HYPOTHESIS: \(Q_{\rm frac}\le0.10\) at all 13 points. A miss is any point above 0.10, and its size is the largest \(Q_{\rm frac}\) and its location.
**B3 (CONSISTENCY_CHECK, reported).** \(E_{\rm best}(G{=}100)/E_{\rm best}(G{=}1000)\in[8,12.5]\) at each of the four \(\varepsilon_0\).
**B4 (CONSISTENCY_CHECK, arm B, reported).** At \((G,\varepsilon_0)=(20,0.1)\), edge cap, \(n\le4\): share of the two-state excess removed \(\ge0.20\). Secondary points \((100,0.1)\) and \((5,0.3)\).

Scoring is `checks/sc_score.py`, which applies these rules; nothing is scored by hand. A bar is not scored if a code gate fails (section 4).

## 4. Code gates (a failure is `measurement/code`, not a scored miss)

1. \(n=2\) numeric optimum equals the closed form of section 2 within \(10^{-6}\) relative in heat, at every point.
2. Every admissible design satisfies \(\varepsilon_{\rm ach}\le\varepsilon_0+10^{-7}\) and cap violation \(\le10^{-7}\).
3. \(n=3,4\) best heat is not worse than the \(n=2\) best by more than \(10^{-5}\) relative (the embedded start guarantees it up to the \(10^{-9}\) rate floor; a toy run showed \(3\times10^{-7}\)).
4. No admissible design has \(E_d<-10^{-6}\) (below the proved floor).

## 5. Search space, seeds, stopping rule

- \(n\in\{2,3,4\}\). Decoder classes: for each \(n\), \(k\) memory states decoded as 0 and the rest as 1, for \(k=1..\lfloor n/2\rfloor\) (symmetry removes the rest): one class for \(n=2,3\), two for \(n=4\).
- Rates are searched as \(W=G\,e^{z}\), \(z\in[\ln10^{-9},0]\), each \(W[x,i,j]\) free per world state \(x\) (so nonlinear, world-dependent, asymmetric and multi-state designs are all in the space). SLSQP (scipy), objective heat, constraints error \(\le\varepsilon_0\) and the cap, `ftol` \(10^{-14}\), `maxiter` 400, then one polish pass from the end point.
- Starts per (point, \(n\), decoder class): \(n=2\): 20 random plus 1 embedded; \(n=3\): 150 random plus 1; \(n=4\): 100 random plus 1. The embedded start is clones of the closed-form two-state optimum.
- Master seed 20261127; per-start generator `np.random.default_rng([20261127, arm, pointindex, n, classindex, start])`, arm 0 for A and 1 for B. Arm B points in order: \((5,0.3)\), \((20,0.1)\), \((100,0.1)\).
- **Stopping rule:** fixed counts. No adaptive stopping, no extra starts after seeing a result. If a run is interrupted, scoring uses only what completed and the interruption is logged in `DEVIATIONS.md`. CPU cap: 3 hours per arm; 6 worker processes.
- Reproducibility flag: reported per point, per \(n\): number of designs within \(10^{-6}\) relative of the best. Fewer than 3 is labeled `search-limited`. This does not change any bar.

## 6. Assumptions added (all of them, so none is silent)

1. Dissipative bipartite jump memory with local detailed balance; heat is the memory's own transitions only.
2. The cap is on the total exit rate of every memory state, per world state (arm A). An edge cap (arm B) is a different reading and is reported separately because redundancy defeats it.
3. Every rate is at least \(10^{-9}G\) (every transition reversible, so heat is finite). It introduces a \(\sim10^{-7}\) relative error floor.
4. Hamming error of the best decoder, in the steady state; heat is a steady-state average.
5. \(n\le4\) memory states; the continuous-state or many-state limit is not searched.
6. The telegraph class only, symmetric, equal flip rates; no real system.
7. The memory is read out at the decoder; no cost of reading the decoder is charged.
8. The search is local and one-sided (section 5).

## 7. Disclosures before the lock

- The PAPER two-state table (section 2) was computed before this file.
- \(n=3\) and \(n=4\) timing runs were made at the off-grid point \((G,\varepsilon_0)=(7,0.35)\); only run times and counts of admissible designs were looked at.
- **Leak, logged in `DEVIATIONS.md`.** An earlier version of the toy mode of `checks/sc_run.py` ran the scored grid with one random start per (point, \(n\le3\)), and I read its table before the lock. What I saw: arm A, \(n=3\) was equal to or slightly above \(n=2\) at all 13 points (largest relative gap in \(E\) about \(2\times10^{-3}\)), never below. Arm B at \((20,0.1)\): \(n=3\) removed 30% of the two-state excess; at \((5,0.3)\) and \((100,0.1)\) 0%. That output was deleted; toy mode now uses off-grid points. Effect: B4 was already confirmed in sampled form, so it is labeled CONSISTENCY_CHECK above, and the odds of a B2 miss were lowered from about 0.5 to 0.40 after the glimpse of arm A (one random start only; the scored search uses up to 150).
- The reader's two-pole result (section 0) was known before the lock; it is about diffusions and is not a bar.

## 8. Order of work

(0) Lock commit pushed, and `git ls-remote` shows it. (1) A gate read of the `Gate` section, committed as `gate_read.md` in this folder before any scored run. It will be a separate pass by the same agent that wrote this file and will say so; it is not an independent reader. (2) From a fresh clone at the lock commit, with the hashes of `LOCK.txt` verified first: `nice -n 19 python3 checks/sc_run.py --arm A`, then `--arm B`, then `checks/sc_score.py`; outputs committed. (3) `RESULTS.md`, one row per bar, outcome reported plainly whether it is a yes or a no. (4) Independent read before merge; the PR is not merged by the author.
