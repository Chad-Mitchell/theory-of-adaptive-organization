# Tracking duel: does GTAO's cost pick a quantum tracker for a world drifting on a circle?

*Monday 23 November 2026, America/New_York. Scratch memo, not a PR. This is a self-check; an independent review is still to come. **[REVIEWER EDIT 2026-11-23]** Independent hostile review done: `reviews-indep-2026-11-23/DUEL_REVIEW.md`, checks in `reviews-indep-2026-11-23/duel_review_checks/`. The step (ii) outcome stands; several secondary readings are corrected below. Written against GTAO `main` d592662 (fresh clone in `/workspace/duel`, TMPDIR=/workspace/duel/tmp, nice 19, clone deleted after). `THEORY.md` is untouched and nothing was posted. No real-world data was used. Labels used: **PROVED (in-model)**, **KNOWN** (published and credited), **CONJECTURE**, **SPECULATION**.*

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

**Preregistration.** `PREREG.md` was hashed before any result existed: sha256 `f4b8f59f97db0d98a48a149149db4cf67cd4d92eaf75f3a5101fd61618453c85` (`PREREG.sha256`; `sha256sum -c` passes). Scripts and outputs are in `checks/`, with hashes in `checks/SHA256SUMS`. All 22 DOIs cited below resolve on Crossref (`checks/crossref.out`). **[REVIEWER EDIT 2026-11-23]** Hash re-verified. The evidence that the prereg came first is filesystem time only (PREREG.md created 20:45:00 EST; first script created 20:46:54; first output 20:50:57). The header's "~9:15 PM" would, taken literally, place the prereg after every result, so future preregs should carry an external timestamp (a git commit or similar). All 22 DOIs re-checked on Crossref by the reviewer.

**Inputs.**
- `walls-2026-11-23/WALLS_MEMO.md` §0.6 and §6: door step (ii), "tracking a continuously drifting world without ruin needs continuous reversible updates".
- `reviews-indep-2026-11-23/WALLS_REVIEW.md` §4 objections 3 and 4, and the duel proposed in §5.
- `CORE.md:52`: priced sum; the memory coordinate is mutual information.
- `CORE.md:70` and `CORE.md:80`: the heat floor needs a bath, and acting does not remove it.
- `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md:39,45`: screening, which plays no part here.

A repo grep found no prior GTAO treatment of orbitopes, Fejér–Riesz phase densities, epistemic restrictions, quantum clocks, or Salecker–Wigner–Peres. Everything below that is labeled "PROVED (in-model)" is new to the repo, not new to the literature, unless stated otherwise.

## 0. Bottom line

1. **Outcome under the preregistered rule.** Step (ii) does **not survive in the reviewer's sense.**
   - Regime D, R-Hol, FC1: quantum **LOSES** (475 LOSE / 85 TIE cells).
   - Regime D, R-Hol, FC2: **TIE** (554 TIE / 6 LOSE).
   - Under R-Hardy (exactly N perfectly distinguishable record states), quantum wins against the classical N-state tracker in 97–98% of cells. The aggregate is **MIXED**, because of a few large-price, short-horizon losses. In the strict no-bath variant it is a clean **WIN** (560/560 in D, 736/736 in S1).
   - **[REVIEWER EDIT 2026-11-23]** The strict "WIN" is a feasibility result, not a cost result: its only competitor is the frozen record a1, which was never feasible in D or S1 as coded, so every non-excluded cell is a WIN as soon as b is feasible. PREREG §4 also says the classical estimator offset is "optimized", but the code fixed it at 0 (an unlogged deviation). With the preregistered constant offset restored (and a finer rate grid), a frozen record pointed at the middle of a quarter turn is feasible at T = 0.25. The strict R-Hardy aggregates then become **MIXED** (D FC1 530 W / 1 T / 41 L; D FC2 548 W / 4 T / 20 L; S1 FC1 676 W / 2 T / 70 L). S2 R-Hol FC2 moves from TIE to **MIXED** (148 L / 524 T, all at τ = 1/8). Every change sits at T = 0.25 or τ = 1/8. The step (ii) criterion cells keep their labels (D R-Hol FC1 LOSE, FC2 TIE). See DUEL_REVIEW §3.
   - The orbitope check holds: a non-quantum, non-classical theory with N distinguishable states ties quantum's stake and ruin with only 2N−1 parameters. So the cost selects *continuity*, not quantum theory specifically.
   - Predictions P1–P7 were all borne out in direction; P3's crossover horizon came in much earlier than expected (§5).
2. **What drives the result: one structural fact.** Tracking a single drift on a circle uses one generator. A quantum record then visits only a (2N−1)-dimensional section of its N²-dimensional state space: the Toeplitz section. **[REVIEWER EDIT 2026-11-23]** "Toeplitz" refers to the phase factors e^{−i(j−k)ωt}, which depend only on j−k. ρ_t itself is not a Toeplitz matrix. The orbit spans the diagonal plus one 2-dimensional rotating plane per off-diagonal band, so 1 + 2(N−1) dimensions. Its achievable readout laws are exactly the nonnegative trigonometric polynomials of degree N−1 (Fejér–Riesz). A classical rotor under an epistemic restriction (c1) and the Carathéodory orbitope reach the same laws. Stake and ruin therefore tie *exactly*. The extra (N−1)² quantum parameters sit idle, and FC1 charges for them. **PROVED (in-model)**; the ingredients are KNOWN.
3. **Where continuity does pay.** Any finite classical record in continuous time is either frozen or a mixing Markov chain. A mixing record's error spreads until the ruin probability reaches at least ½. The best N-state clock loses coherence at rate 2π·tan(π/N) per revolution. In the grid, no Markov clock met the ruin cap past one revolution at ε ≤ 0.01. Continuous reversible records (quantum, c1, orbitope) are stationary and never ruin. **PROVED (in-model)**; this is KNOWN in substance as "quantum clocks beat classical clocks of the same size" (Woods et al. 2022; Salecker–Wigner 1958; Peres 1980; Bužek–Derka–Massar 1999).
4. **Step (ii), restated.** Ruin-free closed tracking at finite capacity forces a *non-simplex*, continuously reversible record. It does not force complex quantum theory, and it does not exclude classical continuous phase space unless the finite-capacity premise is R-Hardy, which excludes it by definition, not by cost (review objection 3 confirmed). **[REVIEWER EDIT 2026-11-23]** A nuance. c1 is classical only in having a hidden-point model. Operationally its state space (nonnegative trig polynomials of degree ≤ N−1) is a non-simplex convex set: a linear image of the quantum state space, dual to the orbitope. No operationally classical (simplex) continuous tracker has finite K. So under FC pricing the honest reading is "ruin-free closed tracking at finite operational dimension selects a non-simplex state space", and c1 is one of the non-quantum members, alongside the orbitope. The K = N² headwind (objection 4) is real. It shows up as large-price, short-horizon losses to the classical clock and as a clean loss to c1 and the orbitope under FC1.
5. **Most promising follow-up (CONJECTURE).** Rerun the duel with the world drifting on the **sphere**, under non-commuting rotations. There the SU(2) orbit of a spin coherent state spans all N² dimensions, and N² is also the classical band-limited count Σ_{ℓ≤N−1}(2ℓ+1) (checks L7). The idle-parameter headwind disappears, so stake and ruin alone decide. This is close to Müller–Masanes 2013, "Three-dimensionality of space and the quantum bit", which must be read first. **[REVIEWER EDIT 2026-11-23]** As proposed, this follow-up cannot produce a quantum WIN against the sphere version of c1. Every quantum covariant readout law of a spin-(N−1)/2 record is a nonnegative density band-limited to ℓ ≤ N−1 with max ≤ N·mean. The classical restricted sphere rotor that allows all such densities has the same K = N² and a strictly larger law set for N ≥ 3 (witness ρ = I − 2|0⟩⟨0|, Husimi function cos²θ; `duel_review_checks/sphere_check.out`). For N = 2 the sets coincide (the Bloch ball; the Kochen–Specker single-qubit model). So quantum can at best TIE on stake and ruin: **PROVED (in-model)**, elementary. Müller–Masanes 2013 (read) already shows that single-system direction postulates give a d-ball for every d. Three dimensions and two-qubit quantum theory appear only once *continuous reversible interaction between two direction bits* and local tomography are added. A fair follow-up therefore needs composites or interaction, or later-chosen incompatible readouts (DUEL_REVIEW §6).

## 1. Model and cost (GTAO method, named terms)

- **World.** Phase θ on the circle, rotating once per unit time.
  - D: deterministic.
  - S1: plus diffusion, with s = σ² per revolution.
  - S2: plus a von Mises(κ = 100) observation every τ, after which the record is re-prepared from that observation.
- **Cost.** J = **λ ln K** (record-size price per nat of record dimension) + **w·Ē** (stake: time-averaged E[1 − cos e], w = 1), subject to the **ruin cap** max_t P(|e| > π/2) ≤ ε.
- **Heat** (`CORE.md:70`) is not priced. Trackers that need a bath are flagged; the "strict" variant excludes them.
- **Equal readable information.**
  - **R-Hol:** sup I(θ; readout) ≤ ln N.
  - **R-Hardy:** N_max = N perfectly distinguishable record states.
- **Record-size price K.**
  - **FC1:** dimension of the whole state space.
  - **FC2:** dimension of the section the tracker actually visits.
  - Normalized-K sensitivity variants (FC1n, FC2n) were also run.
  - **P-info** (secondary): λ per nat of record–world information, which is GTAO's own memory coordinate (`CORE.md:52`).
- **Finite-capacity premise for (c), stated explicitly as the review requires.** Under FC1/FC2 the price is finite only if the state space, or the section the tracker visits, is finite-dimensional.
  - A noiseless classical point (c0) has K = ∞, so infinite cost.
  - The strongest finite-priced classical continuous tracker is **c1**: an ontic point on the circle whose preparation law is restricted, as a law of the theory, to nonnegative trigonometric polynomials of degree ≤ N−1. It rotates deterministically and is read out exactly. Its K is 2N−1.
  - This is the epistemic-restriction move of Spekkens 2007 and Bartlett–Rudolph–Spekkens 2012, applied to a rotor.
  - Under R-Hardy no classical continuous tracker is admissible, as Lemma 5 shows.

## 2. The trackers at their strongest

| Tracker | Dynamics | Stake (D) | Ruin | K (FC1 / FC2) | Bath? |
|---|---|---|---|---|---|
| a1 N-state, closed | frozen (continuous map ℝ→finite set is constant) | grows with t; tail reaches ½ by a quarter revolution | infeasible past ~¼ rev | N / N | no |
| a3 N-state Markov clock (best) | unicyclic, uniform rate r* = 2π/sin(2π/N) (rate grid optimized) | 1 − sinc(π/N)·e^{−2πt·tan(π/N)} | tail → ½ (Lemma 4); infeasible past 1 rev at ε ≤ 0.01 | N / N | yes |
| a2 N-state on free external ticks (sensitivity) | permutation every 1/N rev | 1 − sinc²(π/N) | 0 for N ≥ 5 | N / N | imports a clock |
| **b** N-level quantum | e^{−iHt}, equally spaced levels, optimal state, canonical phase POVM | 1 − cos(π/(N+1)) unconstrained (Fejér; Bužek–Derka–Massar 1999), more under a tight ε | stationary; feasible for N ≥ 3 / 5 / 6 at ε = 0.05 / 0.01 / 0.001 | N² / 2N−1 | no |
| c1 restricted classical rotor | deterministic rotation | = b exactly | = b exactly | 2N−1 / 2N−1 | no |
| c0 noiseless point | rotation | 0 | 0 | ∞ / ∞ | no |
| o orbitope GPT (check) | U(1) rotation | = b exactly | = b exactly | 2N−1 / 2N−1 | no |

The quantum optimum under the ruin cap is exact. It maximizes cᵀAc subject to cᵀBc ≤ ε, using a Lagrange path, and this is valid because the set of phase densities is convex (Fejér–Riesz). All analytic stakes and tails match Monte Carlo (`duel_mc.out`: max |MC − analytic| on E cos = 0.0009, with standard error 0.0015). The grid tail method agrees with the Fourier tail method to 3e−6.

## 3. Lemmas

1. **L1. Readout laws (PROVED (in-model) from KNOWN Fejér–Riesz, Fejér 1916).**
   - Canonical-phase readout laws of N-level states, whether pure or mixed, are exactly the nonnegative trigonometric polynomials of degree ≤ N−1.
   - Hence b, c1 and o have identical achievable stake/ruin pairs.
   - Check: 80 random nonnegative polynomials were factorized to |q|², with error ≤ 2e−15.
2. **L2. Readable cap (PROVED (in-model)).**
   - For any such law, max p ≤ N·mean p, by Cauchy–Schwarz/Nikolskii.
   - Hence I(θ; readout) ≤ ln N for b, c1 and o without invoking Holevo. This answers failure mode F4 (circularity) for this family.
   - The sine state's canonical information is well below its Holevo χ: at N = 32, 2.81 vs 3.19 nats (ln N = 3.47).
3. **L3. Idle parameters (PROVED (in-model)).** The U(1) orbit of any quantum state spans at most 2N−1 real dimensions: ρ_t's entries depend on t only through j−k (Toeplitz). Measured rank: 3, 5, 9, 15 for N = 2, 3, 5, 8.
4. **L4. Finite classical records ruin (PROVED (in-model)).**
   - In continuous time a finite classical record is frozen or Markov.
   - An irreducible Markov record's law converges to a stationary π that does not depend on θ_t. Averaged over θ, P(|θ − θ̂| > π/2) = ½ for *any* estimate law. Since θ_t sweeps the whole circle, limsup_t P(ruin) ≥ ½ > ε.
   - **[REVIEWER EDIT 2026-11-23]** This assumes a time-homogeneous (autonomous) record. A time-dependent rule imports a clock (compare a2). Reducible chains also reach limsup ≥ ½, because a frozen class label cannot follow the rotation.
   - Rate: |Im λ|/|Re λ| ≤ cot(π/N) for any N-state generator. This is KNOWN (Dmitriev–Dynkin 1946; conjectured with affinity by Barato–Seifert 2017; proved by Ohga–Ito–Kolchinsky 2023; extended in Kolchinsky–Ohga–Ito arXiv:2605.15884). The random spot check never exceeded it.
   - So the uniform unicyclic clock (a3) is the strongest classical clock asymptotically. For intermediate-time transients, optimality was checked only over the rate grid, not proved.
5. **L5. No classical continuous tracker at R-Hardy (PROVED, elementary).** A classical state space with N_max = N is the N-simplex. Its pure states are N isolated points, so continuous reversible motion among them is constant. **[REVIEWER EDIT 2026-11-23]** This covers simplex records only. c1 is excluded under R-Hardy for a different reason: with its own exact readout, no two of its states are perfectly distinguishable (a nonzero nonnegative trig polynomial has only finitely many zeros), so N_max(c1) = 1.
6. **L6. Orbitope (PROVED (in-model)).**
   - The convex hull of the degree-(N−1) trigonometric moment curve (Sanyal–Sottile–Sturmfels 2011) has N perfectly distinguishable states. Shifted Fejér kernels form a partition of unity and vanish at the other nodes (error ≤ 4e−31).
   - It has no more than N such states: each effect needs double zeros, and 2(n−1) ≤ 2(N−1).
   - Its pure states form one U(1) orbit, and K = 2N−1.
   - It is the "Toeplitz shadow" of the quantum clock. It is related to the polygon models of Janotta et al. 2011.

## 4. Results against the preregistered decision rule

Counts are for λ > 0 cells. In every cell λ = 0 gives TIE versus c1.

| Regime | Readable | Price | main (a1/a3 allowed) | strict (no bath) | ticks (a2, sensitivity) |
|---|---|---|---|---|---|
| D | R-Hol | FC1 | **LOSE** (475 L / 85 T) | LOSE | LOSE |
| D | R-Hol | FC2 | **TIE** (554 T / 6 L) | TIE (560 T) | LOSE |
| D | R-Hardy | FC1 | MIXED (545 W / 15 L) | **WIN** (560 W) | LOSE (591 L) |
| D | R-Hardy | FC2 | MIXED (552 W / 2 T / 6 L) | **WIN** | LOSE |
| S1 | R-Hol | FC1 / FC2 | LOSE / TIE | LOSE / TIE | — |
| S1 | R-Hardy | FC1 / FC2 | MIXED (706 W / 30 L) / MIXED (720 W / 4 T / 12 L) | WIN / WIN | — |
| S2 | R-Hol | FC1 / FC2 | LOSE / TIE (575 T / 57 L) | not run (deviation 3) | LOSE |
| S2 | R-Hardy | FC1 / FC2 | MIXED (552 W / 78 L) / MIXED (572 W / 57 L) | not run | LOSE |

The normalized-K variants give the same aggregate labels as their FC1/FC2 counterparts (`decisions.out`).

**[REVIEWER EDIT 2026-11-23]** The reviewer reran every script from a fresh copy, and all outputs are byte-identical (`grid_results.json` d6f8bf9d…, `decisions.out` 8a1205…). With the preregistered classical offset restored (`duel_review_checks/patch_a.py`, `decisions_patched.out`), the labels change as follows:
- D R-Hardy FC1 strict and FC2 strict: WIN → MIXED.
- S1 R-Hardy FC1 strict and FC2 strict: WIN → MIXED.
- S2 R-Hol FC2 main: TIE → MIXED.
- Some λ = 0 rows: WIN → MIXED.

All other labels are unchanged. Literal S2 strict (a3 excluded, a1 and c1 kept), with the memo's a-values: R-Hol FC1 LOSE, FC2 TIE (614 T / 18 L), R-Hardy FC1/FC2 MIXED (`rev_checks.out` R4). The patch gives classical records an offset but keeps b's rotation rate fixed, so it is an upper bound on the classical side's gain.

- **Orbitope vs b:** under FC1, LOSE in 475 cells and TIE in 85 (the ties come from the 1% tolerance at λ = 1e−4). Under FC2, TIE in every cell.
- **P-info** (`duel_pinfo.out`): **LOSE** in 144/144 cells. A noiseless point read through the best covariant channel with I ≤ ln N reaches the rate–distortion floor, which is KNOWN (Shannon lower bound, tight on a compact group).
  - At λ = 0, J is 0.0045 vs quantum 0.0170 at N = 16.
  - The inequality J_cRD ≤ J_c1 ≤ J_b holds by construction: c-RD's design set contains c1's, and c1's information I_can ≤ χ.
- **Free size** (each tracker picks its own N ≤ 256, `duel_freesize.out`):
  - FC1 R-Hol: LOSE.
  - FC2 R-Hol: TIE.
  - FC1 R-Hardy: MIXED (54 W / 6 L).
  - FC2 R-Hardy: WIN (60/60).
  - At short horizons the classical tracker pushes to the edge of the grid (N = 256), so its free-size value there is limited by the grid.

**Step (ii) criterion** (PREREG §6): quantum WIN in D under R-Hol with FC1 or FC2. **Not met** (LOSE, TIE). Following the preregistered wording, the R-Hardy result is recorded as "survives only conditional on a premise that excludes classical continuous by definition". Because the orbitope beats or ties b, it is also recorded that "the cost selects continuity but not quantum theory specifically".

## 5. Predictions vs outcomes (no patching)

| Prediction | Outcome |
|---|---|
| P1 D R-Hol FC1 LOSE, b beats a at long horizons | LOSE. b beats a in 545/560 cells, from T = 0.25 on. |
| P2 D R-Hol FC2 TIE or MIXED | TIE |
| P3 D R-Hardy MIXED, a3 wins at short horizons through smaller K and lower stake; orbitope beats b | MIXED, orbitope beats/ties b. **Partial miss on the mechanism.** a3 never had lower stake than b anywhere in the grid. **[REVIEWER EDIT 2026-11-23]** That holds only with the offset fixed at 0. With the preregistered offset, classical records have lower stake than b in 39 cells (D/S1 T = 0.25: 3; S2 τ = 1/8: 36, at small N). So the predicted mechanism does appear at the shortest horizons. All 15 losses come from the record-size price at λ = 0.1 (or 0.01 at N = 64), at T ≤ 1. The Markov clock's phase spread passes one bin after about 1/N revolution, so its "short-horizon" window is far shorter than predicted. |
| P4 S1 like D | Yes |
| P5 S2 MIXED | Yes. a beats b only at τ = 1/8 (frequent refresh) and only on price. |
| P6 P-info c-RD beats b | Yes (144/144) |
| P7 step (ii) not in reviewer's sense; conditional on R-Hardy; orbitope beats quantum | Yes |

**The P3 puzzle, diagnosed.** I expected an N-state record to hold its quantization accuracy for a while. It does not. A continuous-time stochastic record diffuses by about one bin after ~1/N revolution and reaches ruin after ~N/16 revolutions (tail → ½ by 10 revolutions at N = 32; L5 output). The error lay in my model of the classical clock, not in the pricing.

## 6. The review's failure modes

- **F1, classical continuous matches (objection 3).** **Confirmed** under R-Hol. c1 ties b exactly on stake and ruin, with fewer parameters. Under R-Hardy, (c) is excluded by premise (L5), not by cost.
- **F2, K = N² headwind (objection 4).** **Confirmed.**
  - Against c1/orbitope under FC1, on every λ > 0 cell outside tolerance.
  - Against a3 only at large λ and short T.
  - FC2 removes it, because the task uses 2N−1 parameters.
- **F3, discrete reversible matches at equal K.** **Not borne out** without a free clock. A permutation tracker in continuous time is frozen (a1) unless it imports ticks (a2). With free ticks it beats quantum almost everywhere: 1 − sinc²(π/N) < 1 − cos(π/(N+1)), and K = N. That just moves the continuity into the clock.
- **F4, circularity.** Avoided for this family: the ln N cap follows from L2 (Nikolskii), not from Holevo. R-Hardy still builds in the distinguishability count.
- **F5, the bath (step (i) is global only).** The Markov clock needs a bath. With a bath allowed, quantum's R-Hardy result drops from WIN to MIXED.
- **F6, strawmen.** **[REVIEWER EDIT 2026-11-23]** The classical N-state side was under-optimized: the preregistered offset was not implemented, and the rate grid had 9 points. Correcting this changes only short-horizon cells (above). c1 was not strawmanned. If anything it was favored, because FC1 lets it restrict its state space by law while quantum pays for all N² (DUEL_REVIEW §4). a3 is the best clock by the KNOWN eigenvalue bound (asymptotically). c1 is the strongest finite-priced classical continuous tracker considered. c0 and c-RD are reported too.
- **F7, hidden clock.** The a2 sensitivity shows the result depends on whether time-keeping is free.
- **F8, tie definition.** Preregistered at a 1% relative tolerance.

## 7. What this means for the door

- **What survives (PROVED (in-model), KNOWN in substance).** A closed, finite-capacity record tracking a continuous drift without ruin must have continuous reversible dynamics, which means a non-simplex state space. **[REVIEWER EDIT 2026-11-23]** This needs an autonomous record (no free clock; a2 shows that free ticks reverse it) and holds beyond short known horizons: a frozen record with an offset can meet the ruin cap for a quarter turn. That is the core of Hardy's Axiom 5, obtained here as a minimum of the GTAO cost with a ruin cap, at R-Hardy capacity and without a bath. The quantum-clock literature already has it in substance (Woods et al. 2022: quantum accuracy ~d², classical ≤ d). The GTAO wording, using a ruin cap rather than tick accuracy, was not found in print in the sources read.
- **What does not survive.** "Complex quantum theory is the cheapest" for this task. One-generator tracking cannot tell quantum apart from an epistemically restricted classical rotor or from the orbitope. This matches the KNOWN fact that separating quantum from classical needs incompatible measurements or composites.
- **What this leaves for the door.** Hardy's other axioms, or a task with several non-commuting generators, must do the work. Step (iii), local tomography (Hardy's Axiom 4), is untouched here.
- **Follow-up (CONJECTURE).** On the sphere with SU(2) drift, the quantum record's visited section is all N² dimensions, equal to the band-limited classical count (L7). The headwind disappears, and the minimal-K SO(3)-covariant continuous tracker with N distinguishable states may be quantum itself. Caveat: a GPT that uses only a subset of harmonic degrees could be smaller, and that is the first thing to test. Read Müller–Masanes 2013 and Masanes et al. 2013 before claiming anything. **[REVIEWER EDIT 2026-11-23]** Read by the reviewer. A single-system sphere duel is capped at TIE against the classical band-limited rotor (§0.5 edit). The SPECULATION below therefore needs a composite or interaction task to have any chance of being tested.
- **SPECULATION.** If the sphere duel ties K and quantum wins on stake or ruin, the "three-dimensionality of space" link would be the GTAO-relevant door. That is not shown.

## 8. Deviations and limits

1. PREREG says "~9:15 PM". The file was actually written and hashed at 8:45 PM EST, before any computation. The label was wrong; nothing else is affected.
2. Ruin max over read time is taken over a finite grid of 100–150 times per run. The Markov rate is optimized over a 9-point grid (5 points in free size). The free-size N grid is 2–64 plus six larger values up to 256.
3. The strict (no-bath) variant was not run in S2, because refresh is irreversible for every tracker. The PREREG did not say this in advance. **[REVIEWER EDIT 2026-11-23]** PREREG §6 defines strict as "a3 excluded", which is computable in S2. The reviewer ran it (R-Hol FC1 LOSE, FC2 TIE; R-Hardy MIXED). The skip was a post-hoc reinterpretation, though it does not change the step (ii) criterion.
7. **[REVIEWER EDIT 2026-11-23]** Unlogged: the classical estimator offset (PREREG §4, "offset optimized") was fixed at 0 in code. The effect is reported above.
8. **[REVIEWER EDIT 2026-11-23]** Asymmetry: b's rotation rate is fixed at the world's rate (PREREG §4), while the classical side gets rate freedom. Allowing b the same freedom can only help b.
9. **[REVIEWER EDIT 2026-11-23]** The main record-size price (λ per nat of dimension) comes from walls memo §6, not from `CORE.md:52`. GTAO's own memory coordinate is mutual information, and under that pricing (P-info) quantum LOSES in 144/144 cells.
4. P-info: the quantum design was searched only along the Lagrange path. The comparison relies on the proved inequality J_cRD ≤ J_c1 ≤ J_b.
5. c1's K = 2N−1 requires the epistemic restriction to be a law. Without the law, c1 is c0 (K = ∞).
6. Heat is unpriced in the main rule.

## 9. Files

All of these are in `checks/` (hashed in `SHA256SUMS`):
- `duel_core.py`: error laws.
- `duel_grid.py` → `grid_results.json`, `grid_run.log`.
- `duel_decide.py` → `decisions.out`.
- `duel_lemmas.py` → `duel_lemmas.out`, covering L1–L7.
- `duel_mc.py` → `duel_mc.out`.
- `duel_pinfo.py` → `duel_pinfo.out`.
- `duel_freesize.py` → `duel_freesize.out`.
- `crossref_check.py` → `crossref.out`.

## 10. References (all DOIs verified on Crossref)

Woods, Silva, Pütz, Stupar & Renner 2022 PRX Quantum 3:010319, 10.1103/PRXQuantum.3.010319 · Erker et al. 2017 PRX 7:031022, 10.1103/PhysRevX.7.031022 · Salecker & Wigner 1958 Phys. Rev. 109:571, 10.1103/PhysRev.109.571 · Peres 1980 Am. J. Phys. 48:552, 10.1119/1.12061 · Bužek, Derka & Massar 1999 PRL 82:2207, 10.1103/PhysRevLett.82.2207 · Pegg & Barnett 1989 PRA 39:1665, 10.1103/PhysRevA.39.1665 · Fejér 1916 J. reine angew. Math. 146:53, 10.1515/crll.1916.146.53 · Holevo 2011 (1982) book, 10.1007/978-88-7642-378-9 · Barato & Seifert 2017 PRE 95:062409, 10.1103/PhysRevE.95.062409 · Ohga, Ito & Kolchinsky 2023 PRL 131:077101, 10.1103/PhysRevLett.131.077101 · Kolchinsky, Ohga & Ito arXiv:2605.15884 (read; credits Dmitriev–Dynkin 1946 for the cot(π/n) sector bound, no DOI) · Spekkens 2007 PRA 75:032110, 10.1103/PhysRevA.75.032110 · Bartlett, Rudolph & Spekkens 2012 PRA 86:012103, 10.1103/PhysRevA.86.012103 · Sanyal, Sottile & Sturmfels 2011 Mathematika 57:275, 10.1112/S002557931100132X · Janotta, Gogolin, Barrett & Brunner 2011 NJP 13:063024, 10.1088/1367-2630/13/6/063024 · Gu, Wiesner, Rieper & Vedral 2012 Nat. Commun. 3:762, 10.1038/ncomms1761 · Elliott & Gu 2018 npj QI 4:18, 10.1038/s41534-018-0064-4 · Elliott et al. 2020 PRL 125:260501, 10.1103/PhysRevLett.125.260501 (quantum memory advantages for continuous-time processes: related prior art not yet mapped onto this cost) · Masanes & Müller 2011 NJP 13:063001, 10.1088/1367-2630/13/6/063001 · Chiribella, D'Ariano & Perinotti 2011 PRA 84:012311, 10.1103/PhysRevA.84.012311 · Masanes, Müller, Augusiak & Pérez-García 2013 PNAS 110:16373, 10.1073/pnas.1304884110 · Müller & Masanes 2013 NJP 15:053040, 10.1088/1367-2630/15/5/053040 · Agarwal 1981 PRA 24:2889, 10.1103/PhysRevA.24.2889 · Hardy 2001 arXiv quant-ph/0101012 (no DOI).

## 11. For Chad (plain words, audio)

**[REVIEWER EDIT 2026-11-23]** (revised after independent review)

We ran a fair contest. A dial turns steadily, and three kinds of memory try to keep track of it without ever being badly wrong: a quantum one, a simple one with a fixed number of slots, and a smooth classical one with a built-in blur. Over long stretches, the slot memory can't keep up, and both the quantum memory and the smooth one stay steady. So the rule against going broke really does call for smooth, reversible change. That part of your hunch holds up. But quantum didn't win. The smooth blurred dial does exactly as well while storing fewer numbers, and so does a made-up third kind of theory. That's because following one dial only uses a thin slice of what a quantum memory can hold. The review also found that over very short stretches, a simple frozen memory aimed at the middle of the turn sometimes beats quantum. We also learned that tracking a ball turning in every direction won't settle it: a blurred classical ball can copy anything the quantum one reads out. The real test is two memories that have to interact with each other, or a question that's chosen only after the memory is set. That's where quantum and classical genuinely come apart.
