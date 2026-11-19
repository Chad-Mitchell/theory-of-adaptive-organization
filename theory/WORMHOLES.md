# Wormholes: what LAT-1 does, and does not, do if shortcuts exist

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/wormhole_checks.py`, `wormhole_checks.out`. **Everything here is CONDITIONAL on traversable wormholes (or some other zero-or-short-latency link) existing.** The theory does not predict that they exist, and nothing here is evidence for or against them.

**The idea tested (Chad, t1955/t1956).** If instant travel between places were possible, the theory's limit on how far one tracker can reach (LAT-1) would change: split the cases into open and finite wormholes, and say what happens to organization. Treated as a hypothesis. The split turned out not to be the right one (§3).

## 0. Verdict in plain words

1. **Latency is only one of five things that decide the design.** The others are how many bits a throat can carry, how much of the drift is shared between places, the price of telling a place versus looking at it, and whether the shortcut can create causal loops. Zero latency alone does **not** force one central tracker (§2: with a dissemination price equal to the read price, the local design still wins at zero latency).
2. **Open versus finite is a secondary split.** "How many mouths, how far apart" is a station-density question (§4), and it matters. But the decisive splits are the five quantities above, and the most basic is whether the link is a real shortcut at all.
3. **The best-studied theoretical traversable wormholes do not, as far as I could read, give a shortcut.** Gao, Jafferis & Wall (2016) find that their traversable wormhole "cannot be used to violate causality" (abstract; I read only the abstract, so I do not claim to know the full statement). If traversal never beats the outside light path, LAT-1 is unchanged. That is Case A below.
4. **If a real shortcut existed, the theory says: pool what is shared, federate what is private, and the ceiling is the entropy bound.** A single store at the holographic bound would itself be a black hole.
5. **The "X-points" NASA reported in 2012 are not spacetime wormholes.** They are magnetic reconnection sites (§6).

## 1. What LAT-1 says (existing theory, CM-N27, OPEN)

For a tracker that reads a drifting target and holds the last value, with drift spectrum slope α, drift level q and a tolerable error D*, the error grows with read lateness ℓ as MSE ∝ q·ℓ^{α−1}. So the farthest target one tracker can serve at light speed c is L_max = c·(D*/q)^{1/(α−1)}, and beyond it the system must be federated: separate trackers, each with its own reads. This used light-time as the only latency. A shortcut changes the latency, and only the latency.

## 2. Pooling with a dissemination price (DERIVED; checked numerically)

Setup (α = 2, diffusive drift, hold-last-value reads; w·σ² is the drift variance rate common to all N targets; c the price of one read; d the price of telling one target an update):

- **Local design:** each of N targets read at its own best interval T* = √(2c/(wσ²)); cost rate N·√(2c·wσ²).
- **Central design (fully shared drift):** one read serves all N, then N tellings per update; best interval from minimizing (c+N·d)/T + N·wσ²·T/2; cost rate √(2(c+Nd)·N·wσ²), plus N·wσ²·ℓ for staleness ℓ at delivery.

Results (closed forms, checked against brute-force minimization in `wormhole_checks.py`, to tolerance 10⁻³ relative):

- **Zero latency:** central wins iff d/c < 1 − 1/N.
- **With latency ℓ:** central wins iff ℓ < T*_local · (1 − √((1 + N·d/c)/N)).

Examples (saved output): N = 16, d/c = 0: local 22.63, central 5.66, central wins up to ℓ = 0.75 T*; N = 16, d/c = 1: local 22.63, central 23.32, **local wins even at zero latency**; N = 100, d/c = 0.05: central wins up to ℓ = 0.755 T*.

Reading. The benefit of pooling is a square-root saving in reads, √N versus N, so it is large when N is large and the dissemination price is small. It disappears when telling costs as much as looking. **Zero latency is necessary for nothing here; low dissemination price is.** This is risk pooling in the textbook sense, and the theory's own T3a (pool when N > (√(1+ρ)+1)²/ρ for shared fraction ρ) is the partial-sharing version. The dissemination-price extension is new in this note. I did not simulate ρ < 1 beyond T3a.

Label: DERIVED (in-model; PROVED as algebra, simulation as a check), CONDITIONAL on the model.

## 3. The case split, by the quantities that decide it (HYPOTHESIS for the grouping, DERIVED within each case)

| Quantity | Meaning | Source |
|---|---|---|
| Π1 = τ_eff / T*, where τ_eff is the best latency a shortcut gives | Is it a shortcut at all, and how big compared with the best read interval | LAT-1; §2 |
| Π2 = throat capacity B relative to demand N·b / T (b bits per update) | Can the throat carry the traffic | queueing; Bousso 2002 (area limits information, 10⁶⁹ bits per m²); Maldacena, Stanford & Yang 2017: gravitational backreaction "limits the amount of information we can send through the wormhole" (abstract) |
| Π3 = (ρ, d/c) | Shared fraction of drift; price of telling versus looking | T3a; §2 |
| Π4 = link upkeep per mouth | Does keeping a throat open cost a continuing price | the theory's link-upkeep term (§3 of COSMIC_WEB.md); no physical number is known |
| Π5 = chronology | Can the shortcut create closed timelike curves | Morris, Thorne & Yurtsever 1988; Hawking 1992 |

Cases:

- **Case A. No shortcut (τ_eff ≥ the outside light-time).** LAT-1 unchanged. Federation beyond L_max. Includes the case that GJW-type wormholes are not faster than the outside route (CONDITIONAL on that reading).
- **Case B. Shortcut, few mouths.** Station coverage (§4). The reach grows from a light ball to a union of light balls around mouths; partial centralization of the shared drift near mouths, federation elsewhere.
- **Case C. Shortcut, many mouths, throats with ample capacity, ρ high, d/c small.** §2: pool the shared component within covered regions. Private drift (the 1−ρ part) still federates, because pooling cannot help what is not shared. The upper limit on any store is the holographic bound.
- **Case D. Shortcut that allows loops.** Then ℓ can be zero or negative for some pairs, and the model's staleness term (ℓ ≥ 0) is no longer defined. Morris, Thorne & Yurtsever (1988) showed wormholes can become time machines (title: "Wormholes, Time Machines, and the Weak Energy Condition"); Hawking (1992) conjectures that physics prevents it (making closed timelike curves would need a violation of the averaged weak energy condition on a compactly generated Cauchy horizon, and back-reaction would prevent them; I read a summary of the abstract). Under that conjecture Case D does not occur. If it did, the theory would not give a prediction, and that is stated as a limit, not hidden.

**Is Chad's open versus finite split right?** It is incomplete. "Finite" fits Case B (few mouths) and "open", read as unlimited mouths and capacity, fits Case C. But capacity (Π2), the telling price (Π3) and causality (Π5) are independent of that count. Two systems with the same number of mouths can sit in different cases.

## 4. Station catchment: how far a shortcut network reaches (DERIVED; simulated)

Mouths ("stations") as a Poisson process of density ν; a target is served if some station is within light-distance c·(ℓ* − τ), where ℓ* = (D*/q)^{1/(α−1)} is the tolerable latency (so L_max = cℓ*) and τ the hop latency through the throat. Then the fraction of targets with a station in reach is

1 − exp(−(4π/3)·ν·(c(ℓ* − τ))³),

united with the direct light ball of radius cℓ* around the tracker. The simulation matches this formula to within 0.01 absolute at the nine (ν, r) points checked (e.g. ν = 100, r = 0.1: 0.347 simulated, 0.342 formula; ν = 1000, r = 0.05: 0.408 and 0.408). Coverage reaches 95% when ν ≳ 0.72/(c(ℓ* − τ))³ (from −ln 0.05 = 3.0 divided by 4π/3).

Findings (saved output, part c): with ν = 0 the coverage is the light ball alone (0.030 for ℓ* = 0.2); at ν = 100 it is 0.967 for τ = 0, 0.365 for τ = 0.1 and 0.030 for τ = 0.19. **Hop latency eats the budget:** a shortcut whose hop latency is nearly the whole budget adds nothing. Dependence on τ is cubic through (ℓ* − τ)³, so it is steep.

## 5. The ceiling (PRIOR ART for the bound; DERIVED for its use here)

No store can hold more than the holographic bound allows: the area of any surface limits the information in the adjacent spacetime region, at about 10⁶⁹ bits per square metre (Bousso 2002, abstract). A central store pooling the world's shared drift therefore has a maximum size, and one at the bound is a black hole (class frozen, in this theory's classes). So even Case C is not "one infinite brain": it is bounded by capacity and by the Landauer floor on erasure (THEORY §2.3, SCALE_ENDS). I do not claim a number for the bound at any particular store.

## 6. Physics check, and a correction

- **Exotic matter.** Traversable wormholes of the Morris–Thorne kind need matter that violates the weak energy condition (the title of Morris, Thorne & Yurtsever 1988). I read the abstract only here and cite the titles and the abstract-level claims; no such matter is known.
- **Quantum traversable wormholes.** Gao, Jafferis & Wall (2016) obtain a traversable BTZ wormhole in AdS from a coupling that produces negative average null energy; they note it "cannot be used to violate causality"; Maldacena, Stanford & Yang (2017) discuss teleportation-like traversal and limits on the information. These live in anti-de Sitter space and are not claims about our universe.
- **NASA "X-points" (2012).** Press coverage in July 2012 described "portals" in Earth's magnetic field found with THEMIS, Polar and Cluster data. These are intermittent magnetic reconnection connections that let solar particles into the magnetosphere, not wormholes in spacetime. I read a short secondary news page (the primary NASA article was not retrievable here) and a search summary identifying them as reconnection sites. Nothing in the theory depends on them.

## 7. Predictions and kill conditions

| Row | Claim | Label | Kill condition |
|---|---|---|---|
| N41 | The pooling and coverage forms in §2 and §4 | PROVED (in-model); CONDITIONAL on the cost model and on shortcuts existing | An algebra or sampling error (checked here to 10⁻³ and 0.01); or a shown inconsistency with the T3a form at d = 0 |
| N42 | In ordinary networks with a latency shortcut (a relay, content-delivery node, a fast fibre or microwave link), centralized pooling of a shared signal beats local reads iff d/c < 1 − 1/N at zero latency | HYPOTHESIS (testable with real systems; no data collected) | A system with measured read cost c, dissemination price d, shared drift ρ ≈ 1 and N, where d/c < 1 − 1/N holds and the local design is still cheaper after adding latency, with ρ and N measured independently. Must meet MV1 to MV10 before a prereg locks |
| N46 | "GTAO predicts that wormholes exist or that distance will not matter" | WITHDRAWN as framing | n/a |

## References (opened)

- Bousso R 2002, "The holographic principle," *Rev Mod Phys* 74:825, arXiv hep-th/0203101 [abstract]
- Gao P, Jafferis DL, Wall AC 2017 (arXiv 2016), "Traversable wormholes via a double trace deformation," *JHEP*, arXiv 1608.05687 [abstract]
- Hawking SW 1992, "Chronology protection conjecture," *Phys Rev D* 46:603, doi 10.1103/PhysRevD.46.603 [abstract summary read; paper not]
- Maldacena J, Stanford D, Yang Z 2017, "Diving into traversable wormholes," *Fortschr Phys*, arXiv 1704.05333 [abstract]
- Morris MS, Thorne KS 1988, "Wormholes in spacetime and their use for interstellar travel," *Am J Phys* 56:395, doi 10.1119/1.15620 [metadata only]
- Morris MS, Thorne KS, Yurtsever U 1988, "Wormholes, time machines, and the weak energy condition," *Phys Rev Lett* 61:1446, doi 10.1103/PhysRevLett.61.1446 [metadata (title) only]
- Azriel M, 2012-07-05, "X-point portals connect Earth to Sun," Space Safety Magazine [short secondary news page read]
