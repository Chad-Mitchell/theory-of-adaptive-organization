# Hostile review of forces-gravity Round 2 (G2)

Date: Thu 26 Nov 2026, 01:05–01:15 EST. Reviewer: hostile referee (stat mech / lattice gauge / tensor networks). Private R&D note. No git, no posting, no email. The worker's files were not edited. The only other file touched is one appended line in `WORKLOG.md`.

Material reviewed: `NOTE.md` (Round 1 Q1–Q4 for context; Round 2 R2.0–R2.7), `ATTEMPTS.md`, `crossref_forces_gravity.txt`, `scripts/r2_*.py`, `outputs/r2_*.txt`, `outputs/q5_platonic_lp_rerun.txt`, `j2016.txt` (Jacobson 2016, full text), `mmpa2014.txt` (Masanes et al. 2014, full text), `/workspace/fresh-11/THEORY.md:392` (CT18), `/workspace/fresh-11/theory/GENERALITY_2026-11-22.md` §1.2 (JP-heat), and `/workspace/gtao-notes/rnd/selfref/NOTE.md` Rounds 5, 11-M and 12-M. I also read Al-Safi–Richens 2015 (arXiv:1508.03491v1, statement of Thm 1), which the R2.5 coverage table needs.

My files are in `review_g2/`:
- `hr_checks.py` / `hr_checks_out.txt`: tracker format, JP-heat dE scan, SU(2) vs SU(3) readout, χ² selection, Hessian.
- `hr_underdamped.py` / `hr_underdamped_out.txt`: independent variance estimates and the CT18 one-group test.
- `hr_crossref.py` / `hr_crossref_out.txt`: all DOIs re-queried.
- `reruns/*.rerun.txt`: the worker's scripts re-run unchanged.
- `asr2015_arxiv1508.03491v1.txt`: the Al-Safi–Richens text.

Labels used: **[OBS]** observed numerically; **[HYP]** hypothesis; **[PIM]** proved in model; **[KNOWN]** published, DOI verified.

## 0. Reruns (all five R2 scripts, unchanged, outputs to `review_g2/reruns/`)
| script | result |
|---|---|
| `r2_selection_gibbs.py` | byte-identical to `outputs/r2_selection.txt` |
| `r2_jpheat_equality.py` | byte-identical to `outputs/r2_jpheat.txt` |
| `r2_tracker_scaling.py` | identical |
| `r2_underdamped.py` | identical (seeded) |
| `r2_tracker.py` | identical except that three `0.0000` entries print as `-0.0000` (float sign; no numeric change) |

The worker's numbers are reproducible. The disputes below are about what they show.

## Per-claim table
| # | claim (worker) | worker label | status | corrected label |
|---|---|---|---|---|
| 1 | Record content ≤ ∣∂A∣·log2 χ*, and this area scaling is **forced** by per-bond memory cost + local reads, with χ* independent of N; "the gap comes out for the record" | PIM | **Overclaimed** | The bound is a property of the chosen MPS format [PIM, trivial]. That χ* is N-independent is a [HYP], observed only for Haar worlds at χ ≤ 4, N ≤ 14, and contradicted by the script's own J. FNW gap: [HYP] for these records |
| 2 | min E_s[q·cost] + λD(s‖p0) is Gibbs with β = q/λ; δE = (λ/q)δS; "the same identity Jacobson uses" | PIM | **Holds with relabel** | [KNOWN] Gibbs/Donsker–Varadhan variational principle, applied. Forced *given* KL as the selection price and a cost linear in s. The Jacobson match is in form only (his eqs. 14–16). The second-order sign does **not** clash for the Gibbs step |
| 3 | JP-heat equality ⇔ memory/world rate → ∞; any rate price keeps it strict | PIM + OBS | **Holds (in model), minor corrections** | [PIM] exact steady states for the two-state telegraph with LDB. Stronger [OBS]: sup over dE of the efficiency is g/(g+r) |
| 4 | Interference readout → 1 − ½Re tr U (fundamental SU(2)); fidelity readout → adjoint | PIM + OBS | **Math holds; the representation is chosen** | [PIM], exact for **every** probe state in SU(2), not just on Haar average. "Fundamental" is put in by the probe representation and by a readout linear in U. Summary and foldable wording must say "given" |
| 5 | Underdamped thermal-time temperature σ²/(2γ), "reduces to CT18" | PIM + OBS | **Holds with added hypothesis** | Temperature: [KNOWN] Einstein relation. CT18 hazard form ν = F(z)/τ only for γ/ω → ∞ [OBS: ν·τ varies 25×]. The KMS check is circular |
| 6 | Coverage table (MMPA 2014 scope; Hanner PIM) | mixed | **Partly broken** | The MMPA reading is accurate. Hanner ⇒ (★) is backed by a real two-line proof (R12-M.4) [PIM]. But the rows "ball(d)×ball(d′)", "ball×polytope", I×D and "3+ parts" ignore Al-Safi–Richens Thm 1, which covers them for S = max [KNOWN]. The "best Φ = 0" row reports product states |

## Claim 1: area scaling of the record (R2.1)

**What is asserted.** NOTE.md R2.1 says: "[PIM] For a local task the cost per site, κ·log2 χ + q·ε_loc(χ), does not depend on N, so χ* doesn't either. Any tensor-network record then has S_rec(A) ≤ |∂A|·log2 χ*: area scaling of the record is forced by (per-bond capacity cost + local reads)". R2.0 adds: "the boundary scaling and a finite correlation length come out of the cost; they no longer have to be assumed."

**Circularity: yes, the bound is built in by the format.**
- S_rec(A) ≤ (number of cut bonds)·log2 χ holds for *every* MPS with bond cap χ, whatever the cost. It is the Schmidt-rank bound.
- The record was declared an MPS, priced per bond (`r2_tracker.py`: `cap=sum(np.log2(b))`). Its entanglement is then area-scaling by construction once χ is bounded.
- The only content the cost could add is "χ* stays bounded as N → ∞". That is not proved. The [PIM] step assumes ε_loc(χ) is N-independent, which is exactly the point at issue.
- "Any tensor-network record" is also false as stated. The bound |∂A|·log2 χ needs the network's bond graph to be the lattice graph (MPS/PEPS).
  - A MERA record with fixed χ has a min cut that grows like log l in 1D (Vidal 2007, 10.1103/PhysRevLett.99.220405, verified; this is the known MERA property, not re-derived here).
  - In random tensor networks the entropy tracks the graph's min cut at large bond dimension (Hayden et al. 2016), so a network graph with non-local bonds gives volume-scaling cuts at fixed χ.
  - So the choice of a *local* network is a second input, and the note does list it under **Chosen**.
- Local reads do not even require a global pure state. A list of the N−1 two-site marginals answers every local query with zero error at O(N) memory, and "record entanglement" is then undefined. The area scaling belongs to the format, not to the task.

**Is χ* independent of N? Not under the worker's own cost.**
- `r2_tracker.py` uses J = κ·Σ_b log2 χ_b + q·(**mean** local error). Capacity is extensive and error is intensive.
- In my A2 (`hr_checks_out.txt`), take a Haar world. A χ ≤ 4 record (next-nearest Bell pairs) has capacity ≈ N−1 bits. The χ = 1 record has error → 3/4.
- The crossover is κ_c = 0.75/capacity: 6.25e-2 at N = 12, 7.5e-3 at N = 100, 7.5e-4 at N = 1000.
- So at any fixed κ the optimum goes to the **product record χ* = 1** once N ≳ 0.75/κ. Area scaling then holds only vacuously (S_rec = 0).
- With an extensive error term (q·Σ local errors, as the PIM sentence implicitly uses), the crossover is N-independent. The script and the PIM sentence use different J. Fix: state one J and rerun the optimum against N. Only fixed-χ errors were scanned against N; χ* was never computed against N.

**Do the observed numbers support it? Weakly, and only for Haar worlds.**
- Haar world, truncated-SVD record, N = 8/10/12/14 (`outputs/r2_tracker_scaling.txt`, reproduced):
  - χ = 2: local error 0.357/0.415/0.415/0.414 (flat from N = 10).
  - χ = 4: 0.150/0.196/0.205/0.204 (flat from N = 12).
  - χ = 8: 0.024/0.079/0.096/0.107, **still rising**.
- Quench world: χ = 2: 0.079/0.127/0.140/0.158; χ = 4: 0.025/0.069/0.087/0.097; χ = 8: 0.003/0.018/0.039/0.055. All **still rising** at N = 14.
  - The quench is the only physically motivated world here, and saturation is not observed for it.
- At N = 12 the local task at κ = 0.01 picks χ* = 32 with record S(6) = 4.84 against the world's 5.28 (`outputs/r2_tracker.txt`). The bound log2 32 = 5 is near the 6-bit maximum. At N = 12 the data cannot separate area scaling from volume scaling.
- Truncated SVD is not the cost-optimal record for local reads. My next-nearest Bell-pair record with max bond χ = 4 has mean local error 0.0973/0.0264/0.0063 at N = 8/12/16. The SVD χ = 4 record has 0.150/0.205 at N = 8/12. (My Bell-record error equals the true marginals' distance from I/4, which decays with N.)
  - This *helps* the hypothesis for Haar worlds (a bounded-χ record with vanishing local error exists).
  - But it shows the reported χ* values are optima over the SVD family, not over records.
  - It also shows the cheap record can be a fake world that matches only "maximally mixed marginals". The note itself warns of this ("a property of the record, not the world").

**FNW claim.** "[KNOWN, FNW 1992] … So the gap comes out for the record."
- FNW's unique-gapped-ground-state result is for translation-invariant, injective (pure) finitely correlated states (the note's own parenthesis).
- The records here are open-boundary truncated-SVD MPS of random states. They are not translation-invariant, and injectivity was not checked.
- Relabel: "[HYP] if the record is (uniformly) injective, it has a gapped parent Hamiltonian".

**Forced vs chosen.** The note says "forced"; actually **chosen**: the MPS/local-network format, per-bond pricing, and local reads. Saturation of ε_loc in N is a **hypothesis**.

**Status: overclaimed.** Corrected statement:
> "[PIM, trivial] A bond-capped MPS record has S_rec(A) ≤ (#cut bonds)·log2 χ. [HYP] With local reads and an extensive error term, the cost-optimal χ* is N-independent if the per-site local error at fixed χ saturates in N. [OBS] Saturation is seen for Haar worlds at χ ≤ 4 (N ≤ 14), not for the quench or for χ = 8. Area scaling of the record is then a consequence of the format plus that hypothesis, not of the cost alone."

Also fix the R2.0 summary sentence "the boundary scaling and a finite correlation length come out of the cost; they no longer have to be assumed".

## Claim 2: selection cost ⇒ Gibbs, δE = (λ/q)δS, and Jacobson 2016 (R2.2, R2.3)

**Math: holds; it is the standard Gibbs (Donsker–Varadhan) variational principle.**
- min_s {E_s[f] + λD(s‖p0)} = −λ ln E_{p0} e^{−f/λ}, attained at s ∝ p0 e^{−f/λ}. The rerun gives max |s_opt − Gibbs| = 2.44e−6 and J_opt = 0.750020 = −λ ln Z.
- The first-order identity is stationarity on the simplex. With uniform p0, D = ln n − S, so qδE = λδS. With non-uniform p0 the identity is δE = −(λ/q)δD(s‖p0), not Shannon δS.
- The "three random directions agree to 1e−6" is a finite-difference check of a tautology.
- The note does name the principle in R2.3. But R2.0 and R2.6 present it as something "the theory's own selection cost reproduces". Relabel: **[KNOWN], applied**.

**"Forced: the exponential form."** Forced only given (i) KL as the selection price, and (ii) a cost linear in s with additive prices.
- Counter-example (`hr_checks_out.txt` D): same Z₃ plaquette, q = 1, λ = 0.7, χ² divergence in place of KL. The optimum has weights per cost level (0, 3) = (2.4286, 0.2857)·p0, linear in cost. Gibbs gives (2.9196, 0.0402).
- In this framework KL is not arbitrary: selfref R5.1 derives D(s‖p0) as the minimum destruction for selection (data processing; far-from-equilibrium Landauer, KNOWN).
- But that derivation:
  - is a *lower bound* (an actual selection process may pay more);
  - is binary;
  - uses S(μ) − S(ω) = D(ω‖μ), which needs a uniform μ.
- **Citation error:** the note attributes D(s‖p0) to "NA4". In the repo (`theory/RECORD_COST_CHAIN_2026-11-25.md:75`) NA4 is "'The disk pays 0' is a definition". The destruction-cost reading is the *proposed amendment* in selfref R5.5, not repo text.
- Corrected label: "[PIM] given selection priced at its minimum destruction D(s‖p0) with uniform p0, and additive prices".

**Jacobson 2016 analogy: honest in form, and the sign worry is unfounded at the Gibbs step.** Jacobson's route (from `j2016.txt`):
- ρ = Z⁻¹e^{−K/T}, T = ħ/2π (eq. 14). "Because ρ in (14) has the form of a thermal state, it minimizes the modular free energy F_K = ⟨K⟩ − TS … δS = (2π/ħ)δ⟨K⟩" (eqs. 15–16).

This is the same minimum-free-energy argument as ours, with the same sign (a minimum). Jacobson also frames the MVEH itself as free-energy minimization at fixed volume with zero energy: "Helmholtz free energy F = E − TS is minimized at fixed volume. The MVEH is analogous, but with the additional feature that the energy vanishes" (and App. C: "minimization of dS free energy is thus equivalent to the maximization of entropy").

Our optimum is a strict minimum of qE + λD: the Hessian on the simplex tangent is λ·diag(1/s), smallest non-zero eigenvalue 19.42 in the Z₃ example. Equivalently, S is maximal at fixed ⟨cost⟩. So the R2.2 row "At second order the sign could clash [MISS, untested]" and R2.7 test 3 can be **closed for the Gibbs step: no clash**.

What remains an open miss is different:
- The MVEH maximum is over joint geometry + state variations at fixed *volume*, with the UV term ηδA. The selection functional has no geometry and no area term, so the full second-order comparison is undefined here.
- Jacobson himself flags finite variations: coherent states change energy without changing entanglement.

Three relabels the R2.2 row needs:
- "It is the same identity Jacobson uses" → "same form (the first-order identity δS = βδ⟨cost⟩ of any Gibbs state). Here β = q/λ is a free price ratio, not 2π/ħ, and the cost is not a local boost generator."
- The S in our identity is the Shannon entropy of the selection share over link configurations, not the entanglement entropy of a region. Identifying them, or linking them to S_rec of R2.1, is a separate hypothesis.
- Minor: the note's "(Hislop–Longo; Casini–Huerta–Myers)" is placed under "from the text". Jacobson 2016 cites Hislop–Longo [29] for K = H_ζ, not Casini–Huerta–Myers 2011 (his [31] is Casini–Galante–Myers). CHM 2011 is a correct outside citation for the CFT ball modular Hamiltonian (DOI verified); I did not read CHM.

**Status: holds with relabel** ([KNOWN] applied; forced given KL + linear cost; Jacobson match in form only; no second-order sign clash at the Gibbs step).

## Claim 3: JP-heat equality only in the fast-memory limit (R2.2)

**Definitions check.**
- The script's information flow is the Horowitz–Esposito form ln[p(m′|x)p(m)/(p(m|x)p(m′))]. JP-heat's I_alt (GENERALITY §1.2) is ln[π(m′|x)/π(m|x)].
- The extra marginal term Σ J_{m→m′} ln(p(m)/p(m′)) vanishes in the steady state, because only memory jumps change the memory marginal, so its net flux is 0.
- I recomputed with JP-heat's exact form and got the same efficiency (e.g. g = 0.5, dE = 1: 0.2366).
- LDB is correctly implemented: wrong→right rate g, right→wrong g·e^{−dE}. Heat into the bath is dE × the net wrong→right flux.
- Efficiency = kT·I_alt/Q̇ = 1 − σ_M/Q̇. This is consistent with JP-heat's Q̇ = σ_M + I_alt.
- I_alt = r·L(ε) to 4 digits in every row. This matches the CORE.md:74 telegraph floor (T59/T60).

**Numbers (rerun identical):**
- At dE = 1, efficiency is 0.2366, 0.5472, 0.8549, 0.9831, 0.9983, 0.9998 for g = 0.5, 2, 10, 10², 10³, 10⁴.
- At the cost optimum, efficiency is 0.9853, 0.9561, 0.8721, 0.6522 at c = 1e−4 … 0.1.

**Attack on "⇔": are there other routes to equality?**
- I scanned dE at fixed g (`hr_checks_out.txt` B). The efficiency decreases monotonically in dE over dE ∈ [1e−3, 30]. Its supremum, as dE → 0, is g/(g+r): 0.3332/0.6666/0.9090 against 1/3, 2/3, 10/11 for g = 0.5, 2, 10.
- So neither weak nor strong bias gives equality at finite g. **Equality ⇔ g/r → ∞ survives in this model** ([OBS] over the scanned grid; the bound efficiency ≤ g/(g+r) is a [HYP] worth a proof).

**Corrections:**
- "The gap σ_M ≈ 0.79/g" is true only at dE = 1 (7.68e−3·100 = 0.768; 7.94e−5·10⁴ = 0.794). At dE = 3 it is ≈ 17/g (1.71e−2·10³).
- "Efficiency 1.0000 at c = 0" is the grid-edge value g* = 10⁵. The optimum is the limit g → ∞, outside the grid. The note says so; keep that wording.
- "So the framework supplies 'equilibrium' exactly as a timescale-separation limit": σ_M = 0 on the memory edges of a *driven* steady state is not Jacobson's local equilibrium of a horizon. The mapping is [HYP] (analogy), not a supplied input.

**Status: holds in model (two-state world, two-state memory, LDB).** Corrected label: "[PIM] exact steady states; [OBS] monotone in dE with sup g/(g+r); the link to Jacobson's equilibrium is [HYP]."

## Claim 4: interference readout → fundamental SU(2), fidelity readout → adjoint (R2.3)

**Math: verified, and stronger than stated.**
- Fidelity readout: E_Haar|⟨ψ|U|ψ⟩|² = (|tr U|² + tr UU†)/(d(d+1)) = (|tr U|² + 2)/6 for d = 2. So the cost is (4 − |tr U|²)/6 = (3 − χ_adj)/6 with χ_adj = |tr U|² − 1. ✔ For U = e^{iθ n·σ} this is (2/3) sin²θ.
- Interference readout: for U ∈ SU(2), U = cos θ·I + i sin θ·n·σ, so ⟨ψ|U|ψ⟩ = cos θ + i sin θ⟨n·σ⟩. Hence Re⟨ψ|U|ψ⟩ = cos θ = ½Re tr U **for every ψ**, with no averaging.
  - Check (`hr_checks_out.txt` C): over 2e4 Haar states, min = max = +0.077492 = Re tr U/2.
  - That is why the note's "exact to the sampled digits (0.5585, 1.8975, 0.7032)" is exact: the 1e5-sample average is unnecessary.
- For SU(3) the same readout is **state-dependent**. Re⟨ψ|U|ψ⟩ ranged from −0.053 to +0.982 around Re tr U/3 = 0.331. The fundamental character needs a Haar-averaged (or maximally mixed) probe: an added hypothesis for N ≥ 3.
- The copyable record is the ancilla outcome of a Hadamard test, with P(outcome 1) = (1 − Re⟨ψ|U|ψ⟩)/2. The error rate of the copyable record is half the "interference cost" quoted. This is a normalization issue only.
- The centre: U = −1 gives fidelity cost 0 and interference cost 2. ✔

**Is choosing the interference readout putting the answer in by hand? Yes, in two places.**
- The probe is a spinor, so the fundamental representation is put in by the probe.
- A readout linear in U averages to a fundamental character. A readout bilinear in U, Ū sees U ⊗ Ū = adjoint ⊕ trivial. The representation is fixed by the readout's degree in U.
- The coherent controlled transport also needs a non-copyable amplitude superposition (probe went round / did not), which the records-only premise does not supply.
- The body of R2.3 does say "Chosen [HYP]: that the cost uses that readout". But the R2.0 summary ("gives the full SU(2) force term, centre included") and R2.6 "Strongest: … interference readout ⇒ fundamental" read as results.

**Status: math holds (PIM); the representation is chosen.** Corrected foldable line:
> "Given a coherent fundamental probe and a readout linear in its amplitude (both chosen), the loop cost is 1 − ½Re tr U for SU(2) for every probe state, and for SU(N) on Haar average. A copyable fidelity readout gives the adjoint (3 − χ_adj)/6."

## Claim 5: underdamped thermal-time temperature σ²/(2γ) and CT18 (R2.4)

**Derivation: correct and textbook.**
- dv = (−γv − ω²x)dt + σdW has stationary ρ ∝ exp[−(2γ/σ²)(v²/2 + ω²x²/2)]. This is the Einstein relation kT = σ²/(2γ) [KNOWN].
- K = −ln ρ = βH, so the Hamiltonian flow of K with parameter s is the H-flow with t = βs.
- "Thermal-time temperature = 1/β" is then a restatement of the Einstein relation. It adds no content beyond the Gibbs form.
- It also needs a chosen symplectic structure: (x, v) canonical with unit mass, and the split of the drift into H-flow plus friction. The Hamiltonian flow is not the actual dissipative dynamics. The note lists "inertia" as chosen; the symplectic split is part of that choice.

**Estimator.**
- The script sets β_v = Σ⁻¹_vv ≈ 1/⟨v²⟩ and then reports "KMS ⟨v²⟩ = 0.4878" next to "1/β = 0.4878". The "classical KMS ⟨{x,v}⟩ = β⟨v²⟩" check is therefore **circular** (an identity of the estimator).
- The non-trivial check is equipartition ω²⟨x²⟩ = ⟨v²⟩, which is the static FDT for this model. Worker: 0.4938/0.4878, 1.0623/1.0669, 0.3633/0.3732. The x-side s.e. was not reported.
- My independent estimate (400 independent chains × 150 time units, dt = 0.002; `hr_underdamped_out.txt` (a)), ⟨v²⟩ and ω²⟨x²⟩ against σ²/(2γ):

| case (γ, ω, σ) | ⟨v²⟩ | ω²⟨x²⟩ | σ²/(2γ) |
|---|---|---|---|
| (1, 1, 1) | 0.4985 ± 0.0029 | 0.4978 ± 0.0042 | 0.5 |
| (0.3, 2, 0.8) | 1.0716 ± 0.0109 | 1.0722 ± 0.0111 | 1.0667 |
| (3, 0.5, 1.5) | 0.3789 ± 0.0013 | 0.3842 ± 0.0079 | 0.375 |

  - The third ⟨v²⟩ is 2.9 s.e. high. I attribute it, unverified, to O(γ·dt) bias of the symplectic-Euler scheme.
  - The worker's x-side 0.3633 is 1.5 of my s.e. below 0.375.
  - Static FDT: consistent at the ~1% level. Dynamic FDT is exact for a linear Gaussian equilibrium Langevin model [KNOWN] and was not tested by the worker.

**"Reduces to CT18": only in the overdamped limit.**
- The script prints z² = B²/(σ_x²τ) = U(B)/kT = 3.1250 for all three parameter sets, including γ/ω = 0.15. That equality is an algebraic identity of the definitions τ := γ/ω², σ_x := σ/γ, valid at any γ. It is not a check that the dynamics reduces.
- CT18 (THEORY.md:392) asserts ν = F(z)/τ, one dimensionless group. The underdamped model has a second group, γ/ω.
- Test (`hr_underdamped_out.txt` (b)): MFPT to |x| ≥ B from x = 0 with thermal v, kT = 1, ω = 1, z² = 2 held fixed, 3000 particles. Results:

| γ/ω | ν·τ |
|---|---|
| 0.25 | 0.0074 |
| 1 | 0.0427 |
| 4 | 0.1261 |
| 16 | 0.1880 |

  - That is a 25× variation at fixed z (MFPT s.e. ≤ 1.8%).
  - So CT18's form holds only for γ/ω → ∞. This is consistent with Kramers 1940 (10.1016/S0031-8914(40)90098-2): the energy-diffusion regime at low friction differs from the Smoluchowski regime.

**Status: holds with added hypothesis.** Corrected label:
> "[KNOWN] the stationary state is Gibbs at kT = σ²/(2γ), and the thermal-time temperature equals it given the chosen symplectic structure. [PIM] z² = U(B)/kT identically. [OBS] CT18's hazard form ν = F(z)/τ holds only in the overdamped limit γ/ω → ∞; at finite γ/ω a second group enters."

Drop the "classical KMS" check or replace it with the equipartition/FDT check.

## Claim 6: the coverage table (R2.5)

**Masanes et al. 2014: scope correctly read.**
- Assumptions, verified in `mmpa2014.txt`:
  - two parts, each a d-dimensional Euclidean ball;
  - Continuous Reversibility "in each type of system" (which makes the local group transitive on the sphere, §IV A);
  - Tomographic Locality.
- Result: "except for the quantum two-qubit state space, none of them contains entangled states. Equivalently … interacting dynamics is impossible".
- Open, in their Conclusions: "non-three-dimensional Euclidean balls display some type of multipartite entanglement. Or the existence of interacting dynamics between Euclidean balls of different dimension".
- The R2.5 paraphrase is accurate.
- But the row "ball(d)×ball(d), d ≠ 3: Yes, KNOWN" covers Conjecture C only when the composite's reversible group is continuous. A discrete reversible entangling map on an intermediate composite is not covered. The note's "premise mismatch" row says this; the "Yes" row must carry it. Relabel: "Yes under continuous reversibility + local tomography (MMPA 2014)".

**Missing KNOWN coverage (a real error in the table).**
- Al-Safi–Richens 2015 (NJP 17, 123001; 10.1088/1367-2630/17/12/123001, verified) states: "Theorem 1. All reversible transformations on a max tensor product of non-classical, dichotomic systems are trivial."
  - The proof is written for N parts, with no requirement that the parts be identical (Thm 3 is the one restricted to identical odd polygons).
  - Dichotomic systems include "all d-dimensional ball systems", even polygons, the d-cube, the d-octoplex (cross-polytope), and the regular 3- and 4-polytopes except simplices.
- So for **S = max** the rows below are covered, and R2.5 marks them "No [MISS]":
  - ball(d)×ball(d′), d ≠ d′;
  - ball × dichotomic polytope;
  - icosahedron × dodecahedron (selfref R12-M.9 already says this);
  - "3+ parts" for dichotomic parts.
- The open miss is the **intermediate composites** min ⊊ S ⊊ max and non-dichotomic parts (odd polygons with other parts, cuboctahedron, reducible parts).
- The table must be split by composite (max vs intermediate).

**"Hanner polytopes proved in model": backed.**
- R12-M.4 gives the proof. Hanner polytopes are generated from segments by products and polar duals (equivalently products and free sums, since P ⊕ Q = (P°×Q°)°).
  - A product has facet normals (n,0), (0,m), so |⟨(n,0),(v,w)⟩| = |n·v| = 1.
  - Polarity swaps vertices and normals.
  - So every Hanner polytope satisfies |⟨n,v⟩| = 1 (★).
- I checked the induction and it holds.
- M11 also needs |n| fixed. That follows automatically: with an absolutely irreducible vertex-transitive group, the vertex second moment is (R²/m)·I. Then 2-levelness gives |n|²R²/m = 1 for every facet.
- Caveats:
  - It is pen-and-paper, not machine-checked, and not independently reviewed. The R12-M.7 Lean items cover L1/L2, not the Hanner induction.
  - The family it covers is small: vertex-transitive Hanner polytopes with absolutely irreducible groups (cubes, cross-polytopes, and wreath-type iterates such as oct×oct). Products of different factors (e.g. cube×octahedron) have reducible groups and are not covered.
- Status: **[PIM]** as stated.

**The "Not certified … best Φ = 0 for I×I, D×D, CO×CO" row reports product states.**
- `outputs/q5_platonic_lp_rerun.txt` gives every "best Φ = +0.000000" at |a|² = |b|² = ‖C‖² = 1. That is a pure product state, where Φ = 0 by definition.
- So it says nothing about entangled extreme points, which is what ♦ needs.
- The relevant numbers are R12-M.9's entangled-point searches: I×I −2.54, D×D −0.44, CO×CO −1.5 (search, not proof).
- Also, max(I,I) and max(D,D) are already trivial by ASR Thm 1 (KNOWN).

**Status: partly broken** (missing ASR coverage; the Φ = 0 row is misreported). MMPA reading and Hanner: hold.

## Where "forced" is really chosen
1. R2.1 "area scaling of the record is **forced** by (per-bond capacity cost + local reads)": the MPS/local-network format and per-bond pricing are chosen, and the bound follows from them. N-independence of χ* is a hypothesis, and fails under the script's own J.
2. R2.0 "boundary scaling and a finite correlation length come out of the cost; they no longer have to be assumed": they come from the chosen format plus a hypothesis.
3. R2.1 "the gap comes out for the record" (FNW): needs translation invariance and injectivity, neither present nor checked.
4. R2.3 "**Forced:** the exponential form": forced given KL as the selection price (selfref R5.1, a lower bound with uniform base) and linear additive costs. Under χ² the optimum is not exponential.
5. R2.0/R2.6 "interference readout ⇒ fundamental", presented as a result: the representation is chosen through the probe and the readout's degree in U.
6. R2.4 "Match: yes" (CT18): an algebraic identity of definitions. The dynamics match only for γ/ω → ∞.
7. Round 1 Q1 "A connection is forced once comparisons per drift period exceed 1" was reviewed for context only and is not re-adjudicated here. It is forced only given the chosen bit-count cost.

## DOIs and cited statements
- All 31 cited DOIs re-queried on Crossref this round (`review_g2/hr_crossref_out.txt`): **31 OK**, metadata matching `crossref_forces_gravity.txt`.
- The guessed 10.1103/PhysRevD.24.2208 again returns 404. It is not cited, correctly.
- Al-Safi–Richens 10.1088/1367-2630/17/12/123001: OK.

Statement checks:

| citation | statement in NOTE | check |
|---|---|---|
| Jacobson 2016 | MVEH; δS = ηδA + δS_IR; δS_IR = (2π/ħ)δ⟨K⟩ from min modular free energy; K = H_ζ for CFTs; first-order; nonconformal needs a conjecture | ✔ (j2016.txt lines 8–12, 262–330, 334–345, 500–512). Caveats: CHM 2011 is not Jacobson's citation for K = H_ζ (he cites Hislop–Longo); the second-order "sign could clash" is not supported by his text (see Claim 2) |
| Masanes et al. 2014 | assumptions, result, open problems | ✔ (Claim 6); "Yes" row needs the continuity hypothesis |
| FNW 1992 | injective TI MPS ⇒ finite correlation length, gapped parent Hamiltonian | statement OK as a known result; misapplied to non-TI, unchecked records |
| Osterwalder–Seiler 1978 | reflection positivity of the Wilson action | ✔ (standard content; title/venue verified) |
| Hislop–Longo 1982 | modular structure for the free massless field (conformal) | ✔ title verified; cited by Jacobson [29] for this |
| Casini–Huerta–Myers 2011 | CFT ball modular Hamiltonian | DOI ✔; content not re-read by me |
| Horowitz–Esposito 2014; JP-heat | information-flow split; Q̇ = σ_M + I_alt | ✔ (script equivalent to JP-heat form, Claim 3) |
| Kramers 1940 | barrier crossing | ✔; also the reason CT18's form fails at finite γ/ω |
| Henderson–Vedral 2001 | J(A\|Ā) = S(A) for pure states | ✔ standard |
| Wolf–Verstraete–Hastings–Cirac 2008 | thermal mutual information area scaling | ✔ standard |

## Corrections to make in NOTE.md (append-only, worker's call)
1. R2.1 and R2.0: replace "forced" with the corrected statement under Claim 1. State one J (extensive error), compute χ* against N, and add a non-SVD record to the comparison. Relabel the FNW sentence [HYP].
2. R2.2 row 1: "same form as Jacobson's eqs. 14–16 (first-order identity of a Gibbs state); β = q/λ is a free price ratio". Close the second-order sign item for the Gibbs step (both are minima of a free energy, i.e. entropy maxima at a fixed constraint). Keep as open miss: the fixed-volume geometric variation and the UV area term.
3. R2.3: relabel "[KNOWN] Gibbs/Donsker–Varadhan, applied; forced given KL selection price". Fix "NA4": cite selfref R5.1/R5.5, since repo NA4 is "the disk pays 0".
4. R2.3 (c): the interference result is exact per probe state for SU(2) (Re⟨ψ|U|ψ⟩ = ½Re tr U). Add that SU(N ≥ 3) needs a Haar-averaged probe, and the ½ normalization of the Hadamard outcome. In R2.0/R2.6 write "given a coherent fundamental probe and a readout linear in U".
5. R2.2 row 2: "σ_M ≈ 0.79/g" at dE = 1 only (≈ 17/g at dE = 3). Add the dE scan (sup efficiency = g/(g+r)). Mark the Jacobson-equilibrium link as [HYP].
6. R2.4: remove "classical KMS … holds", which is circular. Report the equipartition check with s.e. for both sides. Replace "Match: yes" with "z² = U/kT identically; CT18's hazard form only for γ/ω → ∞" (ν·τ = 0.0074 → 0.188 for γ/ω = 0.25 → 16 at z² = 2).
7. R2.5:
   - Split rows by composite. For S = max, ASR 2015 Thm 1 [KNOWN] covers non-classical dichotomic parts of any types and any number (balls of any dims, even polygons, cube, octahedron, icosahedron, dodecahedron).
   - Mark the open miss as intermediate composites and non-dichotomic parts.
   - Replace "best Φ = 0" with the entangled-point values from R12-M.9.
   - Add "continuous reversibility" to the MMPA "Yes" row.

## Overall
- Two of the six claims survive as stated in substance: JP-heat equality in the fast-memory limit, and the Hanner part of the coverage table.
- Three survive after relabelling: the Gibbs/Jacobson form, the interference readout, and the underdamped temperature.
- The headline R2.1 claim (area scaling of the record forced by cost) is overclaimed. The bound comes from the chosen format. The N-independence of χ* is a hypothesis, which the script's own cost contradicts and which the data support only for Haar worlds at χ ≤ 4.
- The coverage table misses known Al-Safi–Richens coverage for max composites.
- Nothing here derives gravity, the Unruh value or the gauge group. The R2.6 foldable list should drop R2.1, and reword the R2.3 lines as conditionals, before any fold.
