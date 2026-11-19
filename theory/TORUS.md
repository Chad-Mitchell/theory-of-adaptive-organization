# The torus: where it is real, what an earlier toy test did and did not show, and what the theory does not say about the shape of the universe

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/circle_map.py`, `circle_map.out`. Labels as in REACH.md.

**The idea tested (Chad, t1955/t1956).** Revisit the torus rigorously: the idea that coupled cycles live on a torus, and that this connects to the theory. Treated as a hypothesis. One earlier test is re-read, and it was a mismatched proxy.

## 0. Verdict in plain words

1. **A torus is the right picture for two cycles.** The state of two independent repeating cycles (two phases) lives on a torus. When they are coupled, they either lock into a fixed ratio or keep drifting past each other. That is textbook mathematics (PRIOR ART), and my check reproduces the standard result.
2. **The earlier toy test that "found no torus effect" tested the wrong thing.** Its coupling restarted one loop whenever the other fired, which forces locking by construction, and its single dial changed two things at once. So it is INVALID as a test of the torus idea, not a failure of it. It also gives no support. The idea remains untested on real data.
3. **The theory's own claim about tori is a HYPOTHESIS about a trade-off, and its form is not derived.** A tracker that locks to an outside cycle saves reads, and pays a coupling price, and loses if the outside cycle's phase drifts out of its locking range. Whether the best coupling is intermediate or all-or-nothing depends on convexity that I could not derive without an assumption (§4).
4. **The theory makes no prediction about the shape of the universe.** "GTAO predicts a torus universe" is WITHDRAWN as framing (N46). What is known about cosmic topology comes from Planck, and it is stated in §5.

## 1. Where the torus provably appears (PRIOR ART; textbook, not re-derived beyond the check)

- **State space of two phases.** Two uncoupled cycles with phases θ₁, θ₂ ∈ [0, 2π) evolve on the 2-torus T². With frequency ratio irrational, a trajectory is quasi-periodic and fills the torus; with a rational ratio it closes.
- **Coupling.** The sine circle map θ ↦ θ + Ω − (K/2π)·sin 2πθ is the standard reduction of two coupled cycles. For K > 0, ranges of Ω lock to rational rotation numbers p/q (Arnold tongues); the 0:1 tongue has width K/π in Ω.
- **My check** (4,000 Ω values in [0,1), rotation number counted as locked when within 10⁻⁴ of p/q with q ≤ 12): the 0:1 tongue widths were 0.0798, 0.1593, 0.2387, 0.3182 at K = 0.25, 0.5, 0.75, 1.0 against theory K/π = 0.0796, 0.1592, 0.2387, 0.3183, with the locked share rising from 0.094 to 0.621 over the same K. A first version of the check measured half the width because it missed the wrap-around at Ω = 0 ≡ 1; the saved code counts both ends.
- **Poincaré–Hopf (textbook).** A closed orientable surface admits a nowhere-vanishing tangent flow only if its Euler characteristic is zero; of the orientable ones that is the torus alone. This is why a smooth, never-stopping, never-repeating flow "lives on a torus" and not on a sphere.
- **KAM (textbook).** Quasi-periodic motion on tori survives small perturbations when the frequency ratio is sufficiently irrational (badly approximable). The golden ratio is the extreme case, so the tori with golden-ratio frequency ratio are the last to break up. This is the real basis for "the golden ratio resists locking".

These textbook facts (Adler 1946; Pikovsky, Rosenblum & Kurths 2001; Arnold; Greene 1979) were **not opened this session**; I rely on my own check and on standard knowledge, and flag them metadata-level at best. The check is evidence that my statement of the tongue width is right, not a source.

## 2. The earlier toy test (off-repo, unpublished): invalid, not failed

An unpublished toy simulation of agents that share a store (called Test C there) was read by an independent reviewer on 13 November 2026. What was established:

- **Locking at κ > 0 was forced by the coupling definition.** The "coupling" fired one loop at the same instant as the other and reset its schedule, a stochastic phase reset. Locking is then the expected consequence. At κ = 0 the loops were independent clocks, so 0% locking only showed the detector had no false positives.
- **The accuracy result was not about locking.** The single dial set both how much agents weighted a shared error signal and how often loops triggered each other. A factorial split put the inverted U in the information weight; it persisted when loops never triggered each other.
- **The circle-map check in that toy found no staircase,** and a golden-ratio comparison gave nothing for or against (inconclusive in one variant, scored against in the other). Calibration checks of that model had also failed.

The honest status (modest wording from that review): in one unpublished toy of agents that share a store, two loops locked once each could trigger the other; the coupling forces it, so it is not evidence; accuracy depended on the weight given to shared error signals, not on locking; locking is untested on real data.

**Why INVALID rather than FAILED.** A failure requires a test whose design could have supported the idea. A trigger-and-reset coupling is not phase coupling of two oscillators; my own check in §1 shows that phase coupling gives a staircase and trigger-forcing gives locking for another reason, and the toy's staircase test used the wrong coupling. Under the repo's gates this matches a mismatched proxy (MV2, construct match): the proxy does not measure the construct. Status: INVALID (N43). Nothing here changes any CLAIM_MAP row.

## 3. What a valid test would need (so the next attempt finds out)

1. A real pair of cycles with measurable phase, and a measured coupling that is phase coupling (not reset).
2. Rotation number versus detuning across a range, so the plateau structure can be seen or not seen.
3. A null where the coupling rate is kept but the timing is unrelated to the partner loop (the toy review's own suggestion).
4. Power sized by a pilot, and MV1 to MV10 met before a prereg locks. MV9's external timestamp still needs Chad's go.

## 4. The theory's hypothesis about coupled loops (HYPOTHESIS, N45)

**Claim.** A tracker whose reads follow a cycle can lock to an outside cycle (the world's, or another loop's) over a detuning range that grows with coupling strength K (tongue width ∝ K, from §1). Locking saves reads, because they are timed to when they are needed; coupling has a price (upkeep for the link); and an outside cycle whose phase drifts out of the locked range is tracked late (LAT-1).

**What can be derived.** If both the benefit (fraction of detunings covered) and the price are linear in K, the optimum is all or nothing, with no interior peak. An interior optimum requires a convex price or a saturating benefit, and I could not derive which holds for any real system without an assumption about the price. So the hypothesis is "plateaus of locking exist in adaptive loops, and their width tracks measured coupling cost", and nothing stronger. That is a hypothesis about plateau structure, and it could be wrong, as the circle-map result says nothing about whether adaptive organizations phase-couple.

**Kill condition (N45).** In real pairs of cycles with independently measured phase coupling (the setup in §3), rotation number versus detuning shows no plateaus beyond a surrogate-null, or the plateau width is uncorrelated with the measured coupling cost across at least a preregistered number of pairs. A system whose coupling turns out to be reset-type rather than phase-type is not a test of N45 (INVALID, as in §2).

## 5. The shape of the universe (no theory prediction; the numbers are Planck's)

- **Curvature.** Planck 2018 with lensing and BAO: Ω_K = 0.0007 ± 0.0019 (68%), consistent with a spatially flat universe (Planck 2018 VI, eq. 47b).
- **Topology.** Planck 2015 searched for matched circles and fitted specific topologies. No sign of compact topology with a scale below the diameter of the last-scattering surface was found. For a cubic 3-torus (T3) the radius of the largest inscribed sphere is R_i > 0.97 χ_rec, and for a slab (T1) R_i > 0.56 χ_rec (Planck 2015 XVIII, abstract).
- **Reading.** Flatness is compatible with a 3-torus topology on a scale larger than the last-scattering surface. A 3-torus is not a donut in 3D space; that picture is an embedding of the 2D torus. The theory takes the cosmological geometry as an input, and **it predicts neither a curved nor a toroidal universe**. Nothing in §1 to §4 depends on the universe's topology.

## 6. Predictions and kill conditions

| Row | Claim | Label | Kill condition |
|---|---|---|---|
| N43 | Torus mathematics (§1): phase coupling gives Arnold tongues of width K/π (0:1) | PRIOR ART | The check's tongue widths disagree with K/π by more than the grid step (currently within 1e-4), or a standard source contradicts it |
| N44 | The earlier toy test (§2): locking forced by the coupling, accuracy effect due to the information weight | NOT EVIDENCE (INVALID as a test of the torus idea; not FAILED) | A source or rerun showing the toy's coupling was phase coupling and the factorial split does not reproduce |
| N45 | Locking plateaus in adaptive loops, width tracks coupling cost | OPEN (HYPOTHESIS) | §4 |
| N46 | "GTAO predicts a torus universe" | WITHDRAWN as framing | n/a |

## References

- Planck Collaboration 2018, "Planck 2018 results. VI. Cosmological parameters," arXiv 1807.06209 [text near eq. 47 read]
- Planck Collaboration 2016 (arXiv 2015), "Planck 2015 results. XVIII. Background geometry and topology of the Universe," A&A 594:A18, arXiv 1502.01593 [abstract read]
- Textbook sources named in §1 (Adler 1946; Pikovsky, Rosenblum & Kurths 2001; Arnold; Greene 1979): **not opened**; named as where the standard results are found.
- Off-repo: independent review of an unpublished toy (Test C stage 3), 13 November 2026, summarized above; not published.
