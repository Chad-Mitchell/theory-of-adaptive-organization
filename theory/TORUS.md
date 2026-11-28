# The torus: where it is real, what an earlier toy test did and did not show, and what the theory does not say about the shape of the universe

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/circle_map.py`, `circle_map.out`; price-to-K map and the shape of the optimum (§4b, v1.4.25): `reach_checks/price_maps.py`, `price_maps.out`. Labels as in REACH.md.

**The idea tested (Chad, t1955/t1956).** Revisit the torus rigorously: the idea that coupled cycles live on a torus, and that this connects to the theory. Treated as a hypothesis. One earlier test is re-read, and it was a mismatched proxy.

## 0. Reading in plain words

1. **A torus is the right picture for two cycles.** The state of two independent repeating cycles (two phases) lives on a torus. When they are coupled, they either lock into a fixed ratio or keep drifting past each other. That is textbook mathematics (PRIOR ART), and my check reproduces the standard result.
2. **The earlier toy test that "found no torus effect" could not tell.** Its preregistered staircase prediction (P7) did fail inside that toy. But its coupling fired one loop at the same instant as the other and reset its schedule at random moments, which forces coincident locking by construction; locking went to 1:1 whatever the nominal ratio; one dial changed two things at once; and its calibration checks had failed. So it is INVALID as a test of the torus idea, a judgment made after the result by the 13 November review, and it gives no support either. The idea remains untested on real data.
3. **The theory's own claim about tori is a HYPOTHESIS about a trade-off, and its form is not derived.** A tracker that locks to an outside cycle saves reads, and pays a coupling price, and loses if the outside cycle's phase drifts out of its locking range. Whether the best coupling is intermediate or all-or-nothing depends on convexity that I could not derive without an assumption (§4).
4. **The theory makes no prediction about the shape of the universe.** "GTAO predicts a torus universe" is WITHDRAWN as framing (N46). What is known about cosmic topology comes from Planck, and it is stated in §5.

## 1. Where the torus provably appears (PRIOR ART; textbook, not re-derived beyond the check)

- **State space of two phases.** Two uncoupled cycles with phases θ₁, θ₂ ∈ [0, 2π) evolve on the 2-torus T². With frequency ratio irrational, a trajectory is quasi-periodic and fills the torus; with a rational ratio it closes.
- **Coupling.** The sine circle map θ ↦ θ + Ω − (K/2π)·sin 2πθ is the standard reduction of two coupled cycles. For K > 0, ranges of Ω lock to rational rotation numbers p/q (Arnold tongues); the 0:1 tongue has width K/π in Ω.
- **My check** (4,000 Ω values in [0,1), rotation number counted as locked when within 10⁻⁴ of p/q with q ≤ 12): the 0:1 tongue widths were 0.0798, 0.1593, 0.2387, 0.3182 at K = 0.25, 0.5, 0.75, 1.0 against theory K/π = 0.0796, 0.1592, 0.2387, 0.3183, with the locked share rising from 0.094 to 0.621 over the same K. A first version of the check measured half the width because it missed the wrap-around at Ω = 0 ≡ 1; the saved code counts both ends.
- **Poincaré–Hopf (textbook).** A closed orientable surface admits a nowhere-vanishing tangent flow only if its Euler characteristic is zero; of the orientable ones that is the torus alone. So among closed orientable 2-surfaces, a smooth flow that never stops lives on a torus and not on a sphere. (In higher dimensions non-stopping flows need not live on tori; chaotic attractors are an example.)
- **KAM (textbook).** Quasi-periodic motion on tori survives small perturbations when the frequency ratio is sufficiently irrational (badly approximable). The golden ratio is the extreme case, so the tori with golden-ratio frequency ratio are the last to break up. This is the real basis for "the golden ratio resists locking".

These textbook facts (Adler 1946; Pikovsky, Rosenblum & Kurths 2001; Arnold; Greene 1979) were **not opened this session**; I rely on my own check and on standard knowledge, and flag them metadata-level at best. The check is evidence that my statement of the tongue width is right, not a source.

## 2. The earlier toy test (off-repo, unpublished): invalid as a test, though its staircase prediction failed in-toy

The in-repo record is `theory/THEOREMS.md` T9. The toy's files and its 13 November review are on the author's machine, not in this repository; the independent review of this note read that review there.

An unpublished toy simulation of agents that share a store (called Test C there) was read by an independent reviewer on 13 November 2026. What was established:

- **Locking at κ > 0 was forced by the coupling definition.** The "coupling" fired one loop at the same instant as the other and reset its schedule, a stochastic phase reset. Locking is then the expected consequence. At κ = 0 the loops were independent clocks, so 0% locking only showed the detector had no false positives.
- **The accuracy result was not about locking.** The single dial set both how much agents weighted a shared error signal and how often loops triggered each other. A factorial split put the inverted U in the information weight; it persisted when loops never triggered each other.
- **The circle-map check in that toy found no staircase,** and a golden-ratio comparison gave nothing for or against (inconclusive in one variant, scored against in the other). Calibration checks of that model had also failed.

The honest status (modest wording from that review): in one unpublished toy of agents that share a store, two loops locked once each could trigger the other; the coupling forces it, so it is not evidence; accuracy depended on the weight given to shared error signals, not on locking; locking is untested on real data.

**Why INVALID rather than FAILED, and what that judgment rests on.** P7 was preregistered in the toy and failed there; that is a fact and is not hidden. Calling it INVALID as a test of the torus idea is a later judgment (the 13 November review), so it should be read as such. The reasons: a failure counts only if the design could have supported the idea. Reset coupling is itself a kind of phase coupling (the toy review calls it "in effect a designed phase-response curve"), and pulse or reset coupling can lock and give tongues under periodic forcing. This toy's resets, though, were random coincident triggers, so locking was forced at any κ > 0 and went to 1:1 whatever the nominal ratio, which leaves no detuning plateaus to see. Its one dial also set the information weight, and its calibration checks (N1, N2) had failed. The §1 check here simulates only the sine circle map. It shows what phase coupling does, not what this toy's coupling does. Under the repo's gates this matches a mismatched proxy (MV2, construct match). Status: NOT EVIDENCE, INVALID as a test (N44). Nothing here changes any other CLAIM_MAP row.

## 3. What a valid test would need (so the next attempt finds out)

1. A real pair of cycles with measurable phase, and a measured coupling that acts on phase in a known way (a smooth phase coupling or a measured phase-response curve, not random coincident resets).
2. Rotation number versus detuning across a range, so the plateau structure can be seen or not seen.
3. A null where the coupling rate is kept but the timing is unrelated to the partner loop (the toy review's own suggestion).
4. Power sized by a pilot, and MV1 to MV10 met before a prereg locks. MV9's external timestamp still needs Chad's go.

## 4. The theory's hypothesis about coupled loops (HYPOTHESIS, N45)

**Claim.** A tracker whose reads follow a cycle can lock to an outside cycle (the world's, or another loop's) over a detuning range that grows with coupling strength K. The 0:1 (and 1:1) tongue width is ∝ K (§1); a p/q tongue grows like K^q at small K (independent review check C: local exponents 1.99 and 1.95 for 1:2, 2.92 and 2.90 for 1:3), so locking at higher ratios needs much stronger coupling. Locking saves reads, because they are timed to when they are needed; coupling has a price (upkeep for the link); and an outside cycle whose phase drifts out of the locked range is tracked late (LAT-1).

**What can be derived.** If the benefit is a fixed amount and both it and the price are linear in K, the optimum is all or nothing. (v1.4.25: §4b shows that when the benefit is instead the covered share of a spread of detunings, the optimum is interior iff the mean mismatch is no larger than the spread; it still rests on an assumed price.) I could not derive which price shape holds for any real system. So the hypothesis is "plateaus of locking exist in adaptive loops, and their width tracks measured coupling cost", and nothing stronger. That is a hypothesis about plateau structure, and it could be wrong, as the circle-map result says nothing about whether adaptive organizations phase-couple. The half that ties width to cost needs a defined map from a measured coupling price to K before it can be run: §4b now defines it, K = 2π·Z·ε(price), for systems with a measured phase-response curve and coupling cost, and finds none yet for organizations.

**Miss condition (N45).** In real pairs of cycles with independently measured phase coupling (the setup in §3), rotation number versus detuning shows no plateaus beyond a surrogate-null, or the plateau width is uncorrelated with the measured coupling cost across at least a preregistered number of pairs. A system whose coupling turns out to be reset-type rather than phase-type is not a test of N45 (INVALID, as in §2).

## 4b. A price-to-K map, and what shape the optimum has (v1.4.25; DERIVED in-model, CONDITIONAL; checked)

Code and saved output: `reach_checks/price_maps.py`, `price_maps.out`.

**The map (definable where a phase-response curve and a coupling cost are measurable).** Take a loop whose phase advances by Ω each cycle (the detuning from the locking ratio) and is nudged by a stimulus of amplitude ε per cycle through a phase-response curve Z(θ) (phase cycles per unit stimulus). The one-cycle map is θ → θ + Ω + ε·Z(θ). A fixed point (a locked state) exists iff Ω is in −ε·[Z_min, Z_max], so the locking plateau has width **ε·(Z_max − Z_min)**, exactly for this map, centred at −ε·(Z_max + Z_min)/2. *(Independent review 2:)* reading "has a fixed point" as "locked" (rotation number 0) needs the map to be a circle homeomorphism, **1 + ε·Z′(θ) > 0 for all θ** (for the sine curve, K < 1); beyond that the map folds and the rotation number need not be unique. The width and the centre were re-derived and checked for an asymmetric curve (independent review 2: locked range [−0.0334, 0.0200] against predicted [−0.0333, 0.0200] at ε = 0.1). For a sine curve of peak sensitivity Z this is the sine circle map with **K = 2π·Z·ε** and width 2εZ = K/π, which agrees with §1 (circle map, Z = 0.5: measured widths 0.0501, 0.1001, 0.2001 against 2εZ = 0.05, 0.10, 0.20 at ε = 0.05, 0.1, 0.2). The price-to-K map is therefore the composition of two measured curves: K(price) = 2π·Z·ε(price), where ε(price) is the inverse of the measured cost of delivering or sensing stimulus ε. If that cost is linear in ε then K is proportional to price, and if it is quadratic then K goes as √price.

**Where it is and is not definable.** It is definable for oscillators with a measured phase-response curve and a measured coupling cost (the type of system is, for instance, a paced or light-entrained biological or engineered oscillator; I did not search for data sets). It is **not definable for an adaptive organization yet**: what Z is for a firm's reporting cycle has no measurement. The p/q tongues for p/q ≠ 0/1 grow like K^q (§4), so their widths need the same map raised to a power.

**Shape of the optimum (assumptions A0 to A3).** A0 (added by independent review 2): the phase-response curve is symmetric, Z_max = −Z_min = Z, and 1 + ε·Z′ > 0 over the prices considered; otherwise the locking window's centre moves with ε and μ below must be measured from that moving centre. A1: the benefit is V per unit time while locked, and locked means |Ω| < a, with a = K/2π = ε·Z. A2: Ω is Normal(μ, σ²) across targets or over time. A3: the price is linear, c per unit of a. Maximize U(a) = V·P(|Ω| < a) − c·a.
- The derivative P′(a) = φ(a − μ) + φ(a + μ), the sum of two Gaussians a distance 2μ apart, which is unimodal on a ≥ 0 exactly when |μ| ≤ σ. So **U is concave on a ≥ 0, and the optimum moves continuously with the price, iff |μ| ≤ σ**: it is a\* = 0 for c ≥ c₀(μ) = 2V·φ(μ/σ)/σ (φ the standard normal density) and interior below. For |μ| > σ the benefit is convex at small a and the optimum **jumps** from no coupling to a large, still interior, coupling at a threshold price (first order). *(Wording corrected by independent review 2: the criterion is about continuity and concavity, not about whether the optimum is interior, since for |μ| > σ the post-jump optimum is interior too.)*
- For μ = 0 the optimum is **a\* = σ·√(2 ln(2V/(c·σ·√(2π))))** for prices below c₀ = 2V/(σ√(2π)), and zero above (checked numerically at six prices, to four decimals). Plateau width falls smoothly with price and vanishes at c₀.
- Numerically, with σ = 1, the largest jump of the optimum between neighbouring prices is 0.06, 0.07 and 0.12 at μ = 0, 0.5σ, 0.9σ (continuous) and 0.99, 2.0 and 3.5 at μ = 1.1σ, 1.5σ and 2.5σ (discontinuous), matching the criterion. At μ = σ exactly the onset is a fourth-root cusp: still continuous, but the grid reads it as a jump of 0.42.

So the earlier statement that linear benefit and linear price give all or nothing was too coarse. When the benefit is the *covered share of a spread of detunings* and the spread is wider than the mean mismatch, the optimum is interior. What remains an assumption is A1 to A3 themselves (a real price may not be linear, and the benefit of locking is not literally V·P). Label: DERIVED (in-model); CLAIM_MAP N49. Independently re-derived in independent review 2 (`records/reviews/reach_2026-11-18/INDEPENDENT_REVIEW_2.md`): the closed form at μ = 0 (three prices, four decimals), the jump criterion (μ = 0, 0.5, 0.9 continuous; 1.1, 1.5 jump) and the fourth-root cusp at μ = σ (a\*/(c₀ − c)^{1/4} → 2.23) all agree; A0 was missing and is added.

## 5. The shape of the universe (no theory prediction; the numbers are Planck's)

- **Curvature.** Planck 2018 with lensing and BAO: Ω_K = 0.0007 ± 0.0019 (68%), consistent with a spatially flat universe (Planck 2018 VI, §7.3 and abstract; eq. 45b in the arXiv version read by the independent review).
- **Topology.** Planck 2015 searched for matched circles and fitted specific topologies. No sign of compact topology with a scale below the diameter of the last-scattering surface was found. For a cubic 3-torus (T3) the radius of the largest inscribed sphere is R_i > 0.97 χ_rec, and for a slab (T1) R_i > 0.56 χ_rec (Planck 2015 XVIII, abstract).
- **Reading.** Flatness is compatible with a 3-torus topology on a scale larger than the last-scattering surface. A 3-torus is not a donut in 3D space; that picture is an embedding of the 2D torus. The theory takes the cosmological geometry as an input, and **it predicts neither a curved nor a toroidal universe**. Nothing in §1 to §4 depends on the universe's topology.

## 6. Predictions and miss conditions

| Row | Claim | Label | Miss condition |
|---|---|---|---|
| N43 | Torus mathematics (§1): phase coupling gives Arnold tongues of width K/π (0:1) | PRIOR ART | The check's tongue widths disagree with K/π by more than the grid step (currently within 1e-4), or a standard source contradicts it |
| N44 | The earlier toy test (§2): locking forced by the coupling, accuracy effect due to the information weight | NOT EVIDENCE (INVALID as a test of the torus idea; not FAILED) | A source or rerun showing the toy's coupling was phase coupling and the factorial split does not reproduce |
| N45 | Locking plateaus in adaptive loops, width tracks coupling cost (price-to-K map defined for systems with a measured phase-response curve, §4b; none yet for organizations) | OPEN (HYPOTHESIS) | §4 |
| N49 | Price-to-K map K = 2π·Z·ε(price) (plateau width ε(Z_max − Z_min), exact for the one-cycle map) and the shape of the optimum under A0 to A3: concave, with an optimum continuous in price, iff \|μ\| ≤ σ, with a\* = σ√(2 ln(2V/(cσ√(2π)))) at μ = 0 | PROVED (in-model); CONDITIONAL on A0 to A3 (A0, symmetric phase-response curve and an invertible map, added by independent review 2) | An algebra or numeric disagreement (checked to four decimals); or a source showing the plateau width is not ε(Z_max − Z_min) for the one-cycle map. Independently re-derived (independent review 2) |
| N46 | "GTAO predicts a torus universe" | WITHDRAWN as framing | n/a |

## References

- Planck Collaboration 2018, "Planck 2018 results. VI. Cosmological parameters," arXiv 1807.06209 [text near eq. 47 read]
- Planck Collaboration 2016 (arXiv 2015), "Planck 2015 results. XVIII. Background geometry and topology of the Universe," A&A 594:A18, arXiv 1502.01593 [abstract read]
- Textbook sources named in §1 (Adler 1946; Pikovsky, Rosenblum & Kurths 2001; Arnold; Greene 1979): **not opened**; named as where the standard results are found.
- Off-repo: independent review of an unpublished toy (Test C stage 3), 13 November 2026, summarized above; not published.
