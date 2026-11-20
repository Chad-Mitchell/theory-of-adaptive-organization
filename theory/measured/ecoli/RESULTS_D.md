# ECOLI-MEM follow-up D results: the remaining factor of about 4

Friday 20 November 2026. Rules locked in `PREREG_D.md` (`fc83d62`) before `d/d_calc.py` was written; outputs in
`d/d_results.json`. The prereg discloses that likely outcomes were anticipated on paper before lock. Self-checked.

| Candidate | Prediction for the slow memory (or test quantity) | Locked verdict |
|---|---|---|
| **D1** Drift/uptake objective, no noise (Celani & Vergassola 2010 maximin) | 1/λ_CV = 0.58 s (λ_CV = 2σ with σ = Mattingly's λ) or 0.375 s (their own τ_r ≈ 1 s, λτ_r = 8/3) | **DOES NOT EXPLAIN** (makes the gap worse: ×17–26 short) |
| **D2** Up-gradient drift with Model S+ noise, gain bounded | 1.86–3.58 s, identical to the tracking optimum (maximizing drift at fixed activity variance is maximizing corr(a, u)) | **NEITHER** (as for the tracking rerun) |
| **E2** Speed-priced upkeep from measured dissipation | required ρ = k·\|d ln corr/d ln τ\| at 9.9 s: 0.14–0.28 (k = 1), 0.28–0.56 (k = 2); measured ρ = (dissipation ÷ budget) ÷ benefit = 5×10⁻⁵ to 0.21 | **CONSISTENT** (k = 1), **MARGINAL** (k = 2) |
| **H** Slow habitat mode (diagnostic) | 9.9 s needs a slow mode of 20–30 s holding about 6–10% of u's variance (e.g. 20 s, 8–10%: 7–14 s; 30 s, 6–7%: 5–16 s across g) | no verdict; **no field data found** |

## Reading these honestly
- **D1** removes the drift objective in its noiseless maximin form: that optimum has a memory shorter than the swim
  decorrelation time, the opposite direction. The objective matters for the kernel's *shape* (zero integral, two lobes,
  which Mattingly's fitted form also has), not for making the memory long.
- **D2** shows that switching the objective from tracking error to drift changes nothing once the motor's range bounds
  the gain: both are maximized by the same correlation. So the objective is not the cause in the linear, gain-bounded
  regime. A nonlinear-motor objective (Flores et al. 2012 find noise *enhances* drift) is untested.
- **E2** passes the locked overlap rule only at the corner of the box: dissipation ×3 (3×10³ ATP/s), the slowest growth
  budget (7×10⁵ ATP/s) and the smallest benefit (2% of growth) give ρ = 0.21 against a required 0.14 or more. At central
  values (10³ ATP/s, 2×10⁶ ATP/s, 10%) ρ ≈ 0.005, 30–60× short. So the speed price is **not excluded**, but it can carry
  the remaining factor only if E. coli's chemotaxis is worth about 2% of growth in the conditions that set its memory
  and adaptation costs at the top of Lan's estimate. Lan et al. also show that adaptation slows as cells de-energize, a
  direction E2 predicts (a higher energy price gives a longer memory). That is a qualitative match, read after lock, and not scored.
- **H** is a live alternative: a world mode of 20–30 s carrying under a tenth of the signal variance is enough. Gosztolai
  & Barahona 2020 (doi 10.1038/s42005-020-0312-8) argue that longer memory helps in rugged landscapes (prior art for the
  direction). I found no measurement of chemoattractant time scales in E. coli's habitats.

## Status in the required form
Remaining factor of about 4: **drift objective ruled out as the cause within the linear, gain-bounded regime** (D1 DOES NOT EXPLAIN, opposite direction; D2 NEITHER, identical to tracking; a nonlinear-motor objective is untested). Two
causes remain, both untested by direct measurement: **speed-priced upkeep** (consistent only at the cheap-benefit corner)
and **slow habitat modes** (needs a 20–30 s mode with 6–10% of the variance). **Discriminating test (Y4, preregistered in `PREREG_Y4.md` before any data were looked for):** de-energization (Lan et al.)
does not discriminate, because a starved cell slows mechanically under either cause. Benefit does discriminate. E2 says a
larger benefit of chemotaxis buys a faster memory at the same energy price; H says the memory follows the world, not the
benefit. Ni et al. 2020 vary the benefit by carbon source, from near zero on glucose to large in poor carbon.

## Y4 (locked `1db68db`): **UNTESTED**
No open source found that measures E. coli's adaptation time in ≥ 3 growth conditions with the same method (searched FRET
and motor-assay literature; Ni et al. 2020 measure motility investment and benefit, not adaptation time). The
measurement that would score Y4: FRET step responses in cells grown in Ni et al.'s carbon sources.


**Dated note (v2.61, 20 Nov 2026, review 27 item M2): a candidate not considered in PREREG_D.** Tjalma & ten Wolde 2024 (Phys. Rev. Research 6, 033049, doi 10.1103/PhysRevResearch.6.033049, CC BY; DOI verified on Crossref; read in full as arXiv:2402.05825v1, because the journal PDF returned 403 to curl, so the published text may differ in detail) study the same quantity with the same input statistics (Mattingly et al. 2021: τv = 1/0.86 s, σ²vx = 157 µm² s⁻²). Their objective differs from ours. The network predicts the future concentration change v(t0 + τ) (forecast interval τ = τv in their figures), and the error has two parts: a sampling error (readout counts, plus methylation noise in the receptor clusters, whose variance does not average out with τm, their Eq. 21) and a dynamical error. The optimal adaptation time comes from that trade-off. It shortens with more resources and scales approximately as 1/g with gradient steepness (their Eq. 29). With their MWC resource estimates (XT = 10⁴, RT = 8, Nr = 12), the measured τm ≈ 10 s (τm/τv ≈ 8) is "close to optimal" **in performance** for g ≲ 4 mm⁻¹ (their Fig. 3c). Their optimum scales as 1/g, so it sits near 10 s only around g ≈ 4 mm⁻¹. At the lab gradients of our locked box (0.1–0.4 mm⁻¹), their optimum is **longer** than 10 s. They call 10 s close to optimal because performance there is already near the bound ("the improvement in shallow gradients is only very minor"). The result rests on RT = 8, which the authors themselves flag as uncertain: other data suggest RT ∼ 10²–10³, and they say the small value is "conceivable" as a critical-point domain count. **Consequence here:** the ×8.5 F1/P1 FAIL stands as preregistered, but it reflects our choice of objective (estimate the current u at lead 0, with the measured noise treated as exogenous sensing noise). A published account, with a prediction objective and internal noise that does not average out, makes the measured 10 s close to optimal in performance for g ≲ 4 mm⁻¹ under RT = 8 (flagged as uncertain by its authors). Its optimum is longer than 10 s at shallower gradients. With that qualifier, it may explain the remaining factor. Note the direction: at lab gradients their optimum lies beyond the measured 10 s, not on it (corrected v2.62, review 27 R2-1). I have not reproduced their calculation. Their 1/g scaling is an analytic statement of F1's predicted direction, by a mechanism different from Vladimirov et al. 2008. It is still not a measurement.
