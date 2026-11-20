# Measured placements: the first measured system on the map, and the first real test of a layer's memory

*Branch `v2.5-measure` off `b8e8d5b`, Friday 20 November 2026 (America/New_York). Written by a Grok Bot executor for
Chad. A self-check, **not** independently reviewed. THEORY.md is not edited except its CLAIM_MAP version pointer; CLAIM_MAP gains section P (v2.54; F2, Model S+ and SN1 added in v2.55; prior art, SN1 run and follow-up D in v2.56).*

**In one paragraph.** E. coli chemotaxis is the best-measured strongly selected sensing system, and every number the
theory needs for its slow (methylation) layer has been published by one lab under one set of conditions
(Mattingly et al. 2021). I preregistered what the theory says that layer's memory should be, with a rival, then computed
it. **It failed on this setup:** with the cell's measured noise treated as the theory's exogenous sensing noise, the
optimum memory is 1.09–1.17 s; the cell's is 9.9 ± 0.3 s, 8.5× longer. The rival "memory is set at the world's time
scale" fails by the same factor. The structural prediction (a degree-2 world gets two stores) passes, weakly. The
diagnosis is specific: the noise that binds the cell is produced by its own memory store (noise correlation time
11.75 s ≈ memory 9.9 s; physical counting noise is at most 0.02% of it), and the theory's Model S has no term for a store's
own noise. If a store's noise has a fixed stationary variance (a copy-number limit), the same cost puts the optimum at
16–62 s in the lab's gradients and at 9.9 s for gradients of 0.65 mm⁻¹, and predicts the optimum shortens as 1/g; a
published, data-calibrated simulation finds exactly that 1/g law, by a different mechanism, and no measurement yet
decides it. So: **failed on this proxy/setup; diagnosed cause: a missing internal-noise term (the store's own noise);
next test: how kinase noise scales when the adaptation time is changed (F2).** No kill condition is met: this is not a
qualifying test of the class (no closed cost list, no fitness map). The human-scale arm is **untested**: no dataset
measures both judgment spend and the cost of being wrong.

**Update (v2.55, after F2 was scored).** The decisive premise is now measured, and it splits the difference: E. coli's
store noise grows with its memory as σ ∝ τ^0.31 (95% CI 0.24–0.37; Park et al. 2010, nine conditions; a single-cell
FRET check from Keegstra et al. 2017 agrees but is weak), so **neither** locked noise model holds (F2: INCONCLUSIVE by
its rule). Rerunning the test with the measured exponent puts the optimum at 1.9–3.6 s: the store's own noise closes
about 37% of the log gap, and the cell's 9.9 s memory captures about 72% of the best store's explained variance
(37% under exogenous noise). The term the miss exposed is now theory: **Model S+** (`../STORE_NOISE.md`), whose
closed form λτ\* = (1−s)/s says a store runs slower than its mode exactly when its own noise grows more slowly than
fixed density, and that upkeep priced by speed lengthens memory further. P1 stays **failed on this setup**; diagnosed
cause: store noise (part, measured) plus an open remainder (×4, candidates: speed-priced upkeep, objective, habitat,
strain); next tests: kinase noise vs τ at fixed a0, an estimate of the speed price, and SN1 on new systems, locked
before their data (`PREREG_SN1.md`). Details: `ecoli/RESULTS_F2.md`.

**Update (v2.56).** *Prior art:* the optimal-memory trade-off is known (Malaguti & ten Wolde 2021 and others,
`../STORE_NOISE.md` §6); no novelty is claimed. *Out of sample:* SN1 could not be scored on any of its seven systems:
no open source measures how a store's own noise scales with its memory outside E. coli (`SN1_RESULTS.md`). The
discriminating follow-up on a counting-noise-limited relative was INVALID by its premise: V. ordalii's fitted noise is
6.6× the counting bound. *E. coli's remaining factor of about 4* (`ecoli/RESULTS_D.md`):
- a drift/uptake objective does not explain it (the noiseless maximin memory is 0.4–0.6 s, and with noise and a bounded
  gain the drift optimum equals the tracking one);
- a speed price from Lan et al.'s measured dissipation is consistent only at the corner of the input box (central
  estimate 30–60× short);
- a slow habitat mode of 20–30 s carrying 6–10% of the signal variance would do it, but no field data exist.

The test that separates the last two (Y4, adaptation time across benefit levels) is preregistered but untested. **The
keystone is therefore not yet in hand:** the extended model has no out-of-sample verdict, and the in-sample miss is
reduced and diagnosed but not closed.

## 1. Which systems, and why
| Candidate | Theory quantities measurable from published data? | Used |
|---|---|---|
| **E. coli chemotaxis** | World spectrum (velocity autocorrelation in the gradient), the response kernel (both layers' times), noise amplitude and correlation time, gain, latency, cost of the machinery, fitness benefit: all measured, most in one paper | **Yes: ECOLI-MEM** |
| Firms in a competitive industry | Spend on information work is measured (Porat 1977: 46% of 1967 US GNP); the cost of being wrong is not, and the theory's share is look ÷ (look + error), not ÷ GNP | No: **untested** (§H) |
| Plant / cyanobacterial circadian clock (rhythmic world) | Period and damping measured; fitness of period matching measured (resonance experiments); read noise of light/temperature in the field not found | Designed, not run (§R) |
| Vertebrate immune system | No innate vs adaptive cost split with a matched world spectrum found | No |

## E. ECOLI-MEM (`ecoli/`)
### E.1 Preregistration (`ecoli/PREREG.md`, locked at commit `6903de9`, 8:19 AM ET, before any prediction was computed)
Disclosed before lock: the outcome τ2 = 9.9 s and every input had been read; a mental back-of-envelope suggested FAIL.
The test is therefore **not blind to the outcome**; it is blind to the predicted numbers, which depend on noise referrals
and box corners not computed before lock.
- **World.** Along the swim, x = ln c and u = dx/dt = g·v_x is OU with rate λ = 0.862 s⁻¹ (τ_v = 1.16 s) and variance
  g²·a_v (a_v = 157.1 µm²/s²): an integrated OU, McMillan degree 2. Target: the current u (Mattingly's "relevant bits").
- **Arm A** (read noise at the Berg–Purcell floor, Kalman–Bucy for (x, u)). **Arm B** (measured kinase noise referred to
  the signal as white noise; Model S, one OU mode: τ\* = 1/(λ√(1+SNR))). **Arm C** (diagnostic only: store noise of fixed
  stationary variance). **Rival R1:** memory = τ_v.
- **Rules.** PASS iff τ2 ± 2 s.e. ⊂ [L/2, 2U] (and τ_v outside, else PASS-NONDISCRIMINATING); FAIL iff wholly outside
  [L/3, 3U]. Arm A INVALID if the noise is the store's own (|ln τn/τ2| ≤ ln 1.5) or Berg–Purcell < 10% of it.

### E.2 Results (`ecoli/results.json`, `ecoli/run.out`; one deviation: a numerical cross-check, `ecoli/DEVIATIONS.md`)
| Quantity | Prediction (range over the locked box) | Measured | Verdict |
|---|---|---|---|
| Slow memory, arm B (measured noise as exogenous) | **1.09–1.17 s** (SNR 0.004–0.10, so ≈ τ_v) | **9.9 ± 0.3 s** | **FAIL (on this proxy/setup)**, conditional on store noise not depending on store speed |
| Slow memory, arm A (Berg–Purcell floor) | 0.10–0.42 s (complex poles: high SNR at 100 µM) | 9.9 s | FAIL computed, **INVALID** as a test: premise fails (Berg–Purcell is 1×10⁻⁶ to 2×10⁻⁴ of the noise variance; τn/τ2 = 1.19) |
| Rival R1: memory = world time scale | 1.16 s | 9.9 s (×8.5) | **FAIL** |
| Layer count (CT21/L2): degree-2 world → 2 stores | 2 | 2 (kernel G e^{−t/τ2}(1−e^{−t/τ1}), n = 442 cells) | **PASS (structural)**; non-discriminating vs R1, discriminates only against one store |
| Arm C (diagnostic, no verdict) | 62, 31, 21, 16 s at g = 0.1, 0.2, 0.3, 0.4 mm⁻¹ | 9.9 s | — |

Cross-checks. The arm-A poles agree between the quartic and the Riccati solution to 10⁻¹³. A post hoc unit check of arm
B's noise referral reproduces Mattingly's information rate to within 1.4× (0.16 vs 0.225 ± 0.03 bits/s/mm⁻²; theirs uses
the OU-shaped noise spectrum, so a white referral should come out lower): `ecoli/posthoc/inforate_check.out`.
One more thing the exact optimum shows: for target u read through x with white read noise, the optimal kernel from u is
L₂/((s+p₁)(s+p₂)); when its poles are real (low SNR) that is **exactly** the form Mattingly fitted,
G e^{−t/τ2}(1 − e^{−t/τ1}) with 1/τ2 = p₁ and 1/τ1 = p₂ − p₁ (at the Berg–Purcell floor in the lab the poles are complex,
so the optimum would ring instead). The form is right; the times are not.

**How costly is the miss? (post hoc, `ecoli/posthoc/flatness.out`; no verdict.)** A single store at the measured 9.9 s
captures **36–37%** of the explained variance of u that the arm-B optimum captures, so under exogenous noise the
miss is costly, not a flat optimum. Under arm C it captures **86–97%** (g = 0.1–0.4 mm⁻¹): near the minimum. Which of the
two the cell lives in is exactly F2.

### E.3 Diagnosis of the miss (causal, before concluding anything)
| Candidate cause | Evidence | Weight |
|---|---|---|
| (i) Proxy: is τ2 the slow layer's memory, is u the target? | τ2 is the kernel's slow pole by definition; Mattingly's rate-distortion result says u is the relevant variable. | Unlikely to be the cause |
| (ii) Measured inputs | Inputs are one lab's, tight (±1–3%). The info-rate check reproduces their β. The lab gradients (0.1–0.4 mm⁻¹, 100 µM) are not the habitat. | Possible contributor (sets SNR) |
| **(iii) A model assumption: the noise model** | The binding noise has the store's own time constant (τn/τ2 = 1.19) and physical counting noise is ≤ 0.02% of it: the noise is made by the memory, not read from the world. Model S assumes exogenous read noise. Colin et al. 2017 split it: about half from methylation, about half from slow receptor-array fluctuations (34 s without adaptation). Under fixed-variance store noise (arm C) the same cost gives 16–62 s, bracketing 9.9 s within 1.6–6× on the long side. | **Most likely cause** |
| (iii′) A model assumption: loss / world | Clark & Grant 2005: steady-state accumulation needs the negative lobe; the habitat has slow modes the lab lacks. A post hoc slow-nuisance world (34 s array mode) gives ≥ 34 s, not 9.9 s (`ecoli/posthoc/nuisance_mode.out`): that rescue does not work. | Open |
| (iv) Selection condition | Lab strain historically selected in semisolid agar (Mattingly's caveat); tumble rate already off-optimum by 2×. | Possible contributor |
| (v) The claim itself | Cannot be concluded: the decisive premise (how store noise scales with speed) is unmeasured. | Not concluded |

**The theory gap this exposes (new to this repo; the underlying trade-off is prior art, see `../STORE_NOISE.md` §6).** Model S prices the sensing noise but has no
noise that the memory itself generates. When the store is the noise source and its noise has a fixed stationary variance,
longer memory is the way to buy precision, so the optimum memory exceeds the exogenous-noise optimum by a factor set by
internal ÷ external noise. The same shape may explain the repo's human-scale post hoc pattern (SPF consensus forecasts
2.5–6× more rigid than the optimal noisy filter at measured nowcast noise, CLAIM_MAP v2.21/v2.22 notes): costly internal
processing plays the role of store noise. That is a hypothesis for THEORY (a new cost term, κ-like, for a store's own
noise), not a result.

### E.4 Follow-ups, each preregistered fresh before its data were looked for
- **F1** (`ecoli/PREREG_F1.md`, commit `c402814`): arm-C optimum shortens with gradient as g^−0.97; rival R1 slope 0.
  *Result:* no measurement of the best adaptation time across gradients was found (Waite et al. 2016 measured tumble bias,
  not adaptation time). A data-calibrated simulation (Vladimirov, Løvdok, Lebiedz & Sourjik 2008, doi
  10.1371/journal.pcbi.1000242) finds "the optimal adaptation rate rises in proportion with the gradient steepness", i.e.
  slope −1, and Frankel et al. 2014 (doi 10.7554/eLife.03526) "steep gradients required fast adaptation time". **Consistent
  in model; untested by measurement.** Hostile note: their mechanism is the motor's operating range, not noise, so the
  slope does not discriminate mechanisms.
- **F2** (`ecoli/PREREG_F2.md`, commit `f18fdfd`): fixed-variance store noise (σn independent of τ, arm C) vs fixed-density
  (σn ∝ τ^½, arm B). *Result (v2.55, `ecoli/RESULTS_F2.md`):* **neither arm.** Park et al. 2010 Fig. 4c (digitized; nine
  CheR/CW-bias conditions, τ 0.9–15 s) gives s = 0.31 (CI 0.24–0.37); the paper's own line through the origin reads as
  arm B, but a free log-log slope does not. Keegstra et al. 2017 source data (70 wild-type cells) give 0.28 (CI −0.28 to
  0.88). Colin et al. 2017 (doi 10.7554/eLife.26796) decompose the noise but do not vary τ. Still owed: kinase-level noise
  vs τ at fixed a0.
- **Rerun with the measured s (diagnostic, `ecoli/f2/rerun_measured_s.py`):** optimum 2.4–2.6 s at s = 0.31 (1.9–3.6 s over
  the CI); locked thresholds for reference: FAIL at the point, NEITHER over the CI. Cannot rescore P1.
- **Model S+** (`../STORE_NOISE.md`, CLAIM_MAP P9): the extension found because this test failed; predictions for new
  systems locked in `PREREG_SN1.md` (commit `d99eade`) before their data.

### E.5 E. coli's coordinates (`measured.json`, from `coords.py`; replaces the guess logR = 1.0, loglat = −0.5)
| Coordinate | Value | How |
|---|---|---|
| **log₁₀(ℓ/τ_fast)** | **−0.76 [−1.47, −0.58]** (ℓ/τ = 0.17 [0.03, 0.26]) | ℓ = stimulus-to-motor latency 0.23 ± 0.07 s (Segall, Manson & Berg 1982, doi 10.1038/296855a0) down to 0.07 ± 0.03 s (photorelease, Jasuja et al. 1999, doi 10.1016/S0006-3495(99)77329-7); τ_fast = 1/λ = 1.16 s, measured |
| **log₁₀ R (proxy)** | **[−0.3, 1.9]** in poor carbon; R < 1 on glucose | PROXY, not w·Var/h: fitness benefit of chemotaxis (Ni et al. 2020, doi 10.1073/pnas.1910849117: exceeds the several-percent cost of motility in poor carbon; "almost twice as fast" in one ribose phase; none on glucose) ÷ proteome share of the signalling machinery 1.3–3.7% (copy numbers Li & Hazelbauer 2004, doi 10.1128/JB.186.12.3687-3694.2004; lengths UniProt; total protein per cell 2–4 million × 300 aa **assumed**) |
| Layers | 2 measured; world degree 2 | Mattingly kernel; §E.2 |
| Raw dimensionless inputs for the universal map | λτ2 = 8.5 [7.9, 9.2]; τ1/τ_v = 0.19 (fit) or 0.015 (kinase); τn/τ2 = 1.19; SNR (arm B) = 0.004–0.10 ∝ g²; Berg–Purcell share of noise 10⁻⁶–2×10⁻⁴; upkeep shares: proteome 1.3–3.7%, adaptation power ≈ 3×10⁴ kT/s ≈ 5–10% of one motor (Lan et al. 2012, doi 10.1038/nphys2276) | all in `measured.json` |

On the current face map (14-scale 1/f world), this point reads "central, 1 layer", but the map's model world is not
E. coli's (degree 2), so the colour under the dot is not a prediction for E. coli. The universal-axes map should place it
from the raw inputs above.

### E.6 Hostile review of my own result
1. Not blind: the outcome was read before lock (disclosed). Only the predicted numbers were unknown.
2. The decisive arm (B) is conditional on an unmeasured premise; I did not get to choose the noise model after the fact,
   but arm C was named as a diagnostic in advance, and it is the one that comes close. Arm C was **not** a scored prediction
   and must not be read as a pass.
3. The 1/g law in F1 is shared with a rival mechanism, so its agreement is weak evidence even if measured.
4. The R coordinate is a proxy spanning two decades, with an assumed total proteome; benefit numbers were read from text,
   not figures. The x-axis placement is the weakest number here.
5. Lab strain, lab ligand (MeAsp, non-metabolizable), lab gradients: the selection condition (strongly selected in *this*
   world) is not met; the test asks whether the cell is optimal for a world it did not evolve in.
6. Prior art covers most of the ingredients: optimal filtering in chemotaxis (Andrews, Yi & Iglesias 2006; Strong et al.
   1998; Celani & Vergassola 2010; Becker, Mugler & ten Wolde 2015), the information limit and the irrelevant-information
   cost of long memory (Mattingly et al. 2021), the noise sources (Colin et al. 2017), the energy–speed–accuracy cost
   (Lan et al. 2012), the 1/g optimum (Vladimirov et al. 2008). **What this repo adds (no novelty claimed for the physics):** scoring the theory's general rule against those
   measurements with a stated rival and verdict rules; the observation that the measured kernel's *form* matches the
   Kalman optimum's form for target u while its *times* do not (likely implicit in Andrews et al. 2006 and Becker et al.
   2015); and mapping the internal-noise trade-off (prior art: Sartori & Tu 2011; Malaguti & ten Wolde 2021) into the
   theory's cost.

## H. Human scale: untested
No dataset found measures, for a strongly selected human-scale class, both the spend on judgment and the cost of being
wrong in one currency, so the theory's currency-free share (look ÷ (look + error), CLAIM_MAP N57) cannot be computed.
Porat's 46% of GNP (25.1% primary + 21.1% secondary information sector, 1967; *The Information Economy*, US Office of
Telecommunications, ERIC ED142205) looks close to N57's 50% at α = 2, **but the denominator is GNP, not look + error**:
reading it as a hit would be a proxy mismatch (INVALID). What would qualify: a competitive industry with firm turnover and
measured forecasting/monitoring spend **and** measured forecast-error losses (inventory write-downs plus stockout losses,
e.g. retail panels), with the demand spectrum measured from the same firms' sales.

## R. Rhythmic world (designed, not run)
The theory's sharpest rhythm claim is "a rhythm counts two layers (degree 2)" and "matched, not set at": the internal
oscillator runs at the world's period (detuning second-order in its damping) and is more damped than the world, by the
noise. All known circadian clocks are oscillators (degree ≥ 2), so the count is non-discriminating; the detuning is not:
quadratic-loss tracking predicts free-running periods within a fraction ζ²/2 of 24 h, while clocks are routinely detuned
by 1–5%. That would fail unless a cost of entrainment (phase-angle stability) is added; it needs field read-noise data
and a preregistered band before any period table is opened.

## Files
`ecoli/PREREG.md`, `LOCK.txt`, `ecoli_calc.py`, `results.json`, `run.out`, `DEVIATIONS.md`, `PREREG_F1.md`,
`PREREG_F2.md`, `posthoc/` (labelled post hoc; no verdicts), `coords.py`, `measured.json`, `SOURCES.md`,
`crossref.py`, `crossref.out` (all 22 DOIs resolved on Crossref, 20 Nov 2026).

**Update (v2.57).** Testbed ranking with open data (`TESTBEDS.md`); GRID-1 (CE reserve layers vs open-loop imbalance spectrum) preregistered at `4820d91`, not yet run: the German second-wise NRV file is behind a form postback (`grid/RESULTS_GRID1.md`).
