# Placements on the face figure (`figures/face.png`): notes and sources

**Every position is a hypothesis.** No system has valid measured stakes (GAPS G3), so none has a measured R, and the regions are those of one made-up model world (`theory/meq_checks/phase.py`: two time scales 1 and 100, noise 0.05, federation overhead 20h, income 200h). A circle says "if this system's dimensionless coordinates were about here, this model world would call its design X". The circles are drawn about ±0.3–0.5 decades wide on purpose; they are probably too narrow.

Axes: x = R = w·Var/h (stakes over upkeep, any currency); y = ℓ/τ_fast (how late a reading arrives, over the fastest time scale the system tracks). Dotted contours (10%, 30%, 50%): the share of the optimal cost spent on upkeep, which equals d ln J*/d ln h (THEORY CT24). It is the one measurable, currency-free number on the map.

Where there is a source it is for a **time scale**, not for R. R is a guess in every row.

| System | Centre (R, ℓ/τ_fast) | Basis | Source / "guess" |
|---|---|---|---|
| E. coli chemotaxis | R ≈ 9, ℓ/τ ≈ 0.3 | The signalling latency from stimulus to motor response is about 0.2 s; the fastest tracked scale is the 0.5–1 s of CheY-P turnover and runs, so ℓ/τ_fast is a few tenths. Adaptation (about 10–15 s) is the slow scale. The machinery visibly pays (sustaining it costs roughly 3×10⁴ kT/s, 5–10% of the energy to drive a flagellar motor), so R is above the one-layer threshold of about 1.3 in the model; its size is a guess. | Latency: Segall, Manson & Berg 1982, Nature 296:855, doi:10.1038/296855a0. Adaptation time and energy: Lan, Sartori, Neumann, Sourjik & Tu 2012, Nature Physics 8:422, doi:10.1038/nphys2276. Cost of a step response about 10% of sustaining the pathway: Sartori, Granger, Lee & Horowitz 2014, PLoS Comput Biol 10:e1003974, doi:10.1371/journal.pcbi.1003974. **R: guess.** |
| small team (5–10 people) | R ≈ 35, ℓ/τ ≈ 0.04 | Everyone is in one room or one chat, so reports arrive far faster than the fastest thing tracked (days); stakes over the upkeep of a shared tracker (a board, a standing meeting) are modest. | **Guess.** |
| immune system | R ≈ 140, ℓ/τ ≈ 0.1 | Innate response (hours) and adaptive response (days to weeks) are two separated time scales; cells and signals take a modest fraction of the fast scale to reach a site. Stakes (survival) over upkeep (a large standing repertoire) are high. | **Guess** on both axes; the two time scales are textbook knowledge, not looked up here. |
| ant colony | R ≈ 45, ℓ/τ ≈ 9 | A foraging trail's pheromone lasts about 47 minutes (Lasius niger), against a fast scale of seconds to minutes for an ant's choices; foragers are spread over many metres, so a central reading would be late by many fast time scales, and the colony is a federation of local trackers. The 47 minutes is the evaporation scale, not R. | Trail lifetime: Beckers, Deneubourg & Goss 1993, J Insect Behav 6:751, doi:10.1007/bf01201674. **R and ℓ/τ: guess.** |
| firm | R ≈ 280, ℓ/τ ≈ 1.6 | Stakes are large against the upkeep of one more layer of management; reports take about as long to reach the top as the fastest thing the firm tracks (days to weeks of orders and incidents). | **Guess.** |
| city | R ≈ 700, ℓ/τ ≈ 14 | Large stakes, and the distance from a district to the centre is many fast time scales of what a district tracks (hours): a federation of local trackers. The model world's income cap puts the red region at about R = 1000, so the circle sits against it; that is an artefact of the model's income number. | **Guess.** |

What the figure does and does not say:

- It says where the model world's optimal-design regions lie in dimensionless coordinates, and shows how a measurable share could be read on the same chart. That much is a result in a model.
- It does not say any real system sits where its circle is. The placements are hypotheses to be replaced by measurements (the first valid ones would be R from a measured stake, upkeep and variance, and ℓ/τ from a measured delay and fast time scale; GAPS G3).
- Real systems are not this model world: they have other spectra, noise and overheads, so the region boundaries would move. The order of the regions (no model, one layer, two layers, then federation or not viable as stakes and latency rise) is the part that follows from the theorems in every world (THEORY §5 (ii), Theorem P).
- Regenerate with `nice -n 19 python3 figures/face.py` (about 3 seconds).
