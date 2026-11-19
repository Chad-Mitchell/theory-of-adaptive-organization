# Wormholes: what LAT-1 does, and does not, do if shortcuts exist

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/wormhole_checks.py`, `wormhole_checks.out`; the independent review's checks, `reach_checks/independent_review_checks.py` (parts A and B); throat reliability and endogenous drift (§4c, v1.4.25), `reach_checks/wormhole_reliability.py`, `wormhole_reliability.out`. **Everything here is CONDITIONAL on traversable wormholes (or some other zero-or-short-latency link) existing.** The theory does not predict that they exist, and nothing here is evidence for or against them.

**The idea tested (Chad, t1955/t1956).** If instant travel between places were possible, the theory's limit on how far one tracker can reach (LAT-1) would change: split the cases into open and finite wormholes, and say what happens to organization. Treated as a hypothesis. The split turned out not to be the right one (§3).

## 0. Verdict in plain words

1. **For whether to centralize, latency is only one of several things that decide the design.** The others are how many bits a throat can carry, how much of the drift is shared between places, the price of telling a place versus looking at it, whether throats stay open (derived in §4c: failures and outages act as lost deliveries or as added mean latency), whether the world's drift itself speeds up once shortcuts exist (derived in §4c: it does not change whether to centralize at zero latency, but it shrinks the tolerable latency, and the reach grows only if the world's drift speeds up more slowly than the signals do), and whether the shortcut can create causal loops. Zero latency alone does **not** force one central tracker (§2: with a dissemination price equal to the read price, the local design still wins at zero latency).
2. **Open versus finite decides how far one tracker can reach (corrected after the independent review).** If throats have a finite reach Λ and each hop costs a latency τ > 0, a chain of hops (a "tube map") is a faster medium with effective speed v_eff ≤ Λ/τ, and LAT-1 still holds with c replaced by v_eff: beyond v_eff·(D*/q)^{1/(α−1)} a system must still federate (§4b). If throats are open (any mouth to any mouth in one hop), or τ = 0 on a connected throat network, the distance limit disappears. So Chad's split is the right first split for reach. It is not enough for whether to centralize, which turns on the quantities in item 1. The most basic question is still whether the link is a real shortcut at all.
3. **The best-studied theoretical traversable wormholes do not, as far as I could read, give a shortcut.** Gao, Jafferis & Wall (2016) find that their traversable wormhole "cannot be used to violate causality" (abstract). Maldacena, Stanford & Yang (2017, introduction) state that in general relativity "we cannot send a signal through the wormhole faster than we can send it through the outside". If traversal never beats the outside light path, LAT-1 is unchanged. That is Case A below.
4. **If a real shortcut existed, the theory says: pool what is shared, federate what is private, and the ceiling is the entropy bound.** A single store at the holographic bound would itself be a black hole.
5. **The "X-points" NASA reported in 2012 are not spacetime wormholes.** They are magnetic reconnection sites (§6).

## 1. What LAT-1 says (existing theory, CM-N27, OPEN)

For a tracker that reads a drifting target and holds the last value, with drift spectrum slope α, drift level q and a tolerable error D*, the error grows with read lateness ℓ as MSE ∝ q·ℓ^{α−1}. So the farthest target one tracker can serve at light speed c is L_max = c·(D*/q)^{1/(α−1)}, and beyond it the system must be federated: separate trackers, each with its own reads. This used light-time as the only latency. A shortcut changes the latency, and only the latency.

## 2. Pooling with a dissemination price (DERIVED; checked numerically)

Setup (α = 2, diffusive drift, hold-last-value reads; w·σ² is the drift variance rate common to all N targets; c the price of one read; d the price of telling one target an update; local trackers sit at their targets, so local reads have no latency). **In this section c is the read price; in §1 and §4 c is the speed of light.**

- **Local design:** each of N targets read at its own best interval T* = √(2c/(wσ²)); cost rate N·√(2c·wσ²).
- **Central design (fully shared drift):** one read serves all N, then N tellings per update; best interval from minimizing (c+N·d)/T + N·wσ²·T/2; cost rate √(2(c+Nd)·N·wσ²), plus N·wσ²·ℓ for staleness ℓ at delivery.

Results (closed forms, checked against brute-force minimization in `wormhole_checks.py`, to tolerance 10⁻³ relative):

- **Zero latency:** central wins iff d/c < 1 − 1/N.
- **With latency ℓ:** central wins iff ℓ < T*_local · (1 − √((1 + N·d/c)/N)).

Examples (saved output): N = 16, d/c = 0: local 22.63, central 5.66, central wins up to ℓ = 0.75 T*; N = 16, d/c = 1: local 22.63, central 23.32, **local wins even at zero latency**; N = 100, d/c = 0.05: central wins up to ℓ = 0.755 T*.

Reading. The benefit of pooling is a square-root saving in reads, √N versus N, so it is large when N is large and the dissemination price is small. It disappears when telling costs as much as looking. **Zero latency is necessary for nothing here; low dissemination price is.** This is risk pooling in the textbook sense. **"Fully shared" here is T3a's ρ → ∞**: T3a writes ρ = q_g/q_u, the ratio of shared to private drift rates, and its modeling of the shared driver is guaranteed cheaper when N > N\*(ρ) = (√(1+ρ)+1)²/ρ (a sufficient condition, not a cutoff).

**Partial sharing with a dissemination price (DERIVED by the independent review; checked).** With x_i = g + u_i as in T3a, a hybrid design (one central read of the shared driver, told to all N; local reads of each residual) costs √(2(c+Nd)·N·w·q_g) + N·√(2c·w·q_u) against N·√(2c·w·(q_g+q_u)) for all-local. At zero latency the hybrid is cheaper iff

**d/c < 1/N\*(ρ) − 1/N.**

At d = 0 this is exactly T3a (N > N\*). As ρ → ∞ (N\* → 1) it is the rule above. With latency ℓ on the shared part, add N·w·q_g·ℓ to the hybrid. Checked against brute-force minimization in 180 of 180 cases (`reach_checks/independent_review_checks.py`, part A). Like T3a, this compares one feasible hybrid with all-local, so it is a sufficient condition for centralizing the shared part.

Label: DERIVED (in-model; PROVED as algebra, simulation as a check), CONDITIONAL on the model.

## 3. The case split, by the quantities that decide it (HYPOTHESIS for the grouping, DERIVED within each case)

| Quantity | Meaning | Source |
|---|---|---|
| Π1 = τ_eff / T*, where τ_eff is the best latency a shortcut gives | Is it a shortcut at all, and how big compared with the best read interval | LAT-1; §2 |
| Π2 = throat capacity B relative to demand N·b / T (b bits per update) | Can the throat carry the traffic | queueing; Bousso 2002 (area limits information, 10⁶⁹ bits per m²); Maldacena, Stanford & Yang 2017: gravitational backreaction "limits the amount of information we can send through the wormhole" (abstract) |
| Π3 = (ρ, d/c) | Shared fraction of drift; price of telling versus looking | T3a; §2 |
| Π4 = link upkeep per mouth | Does keeping a throat open cost a continuing price | the theory's link-upkeep term (§3 of COSMIC_WEB.md); no physical number is known |
| Π5 = chronology | Can the shortcut create closed timelike curves | Morris, Thorne & Yurtsever 1988; Hawking 1992 |
| Π6 = reliability | Do throats stay open, or open and close (latency becomes a random variable and the hold band must cover outages) | added by the independent review; **derived in §4c (v1.4.25)** |
| Π7 = endogenous drift | If shortcuts exist for everyone, rivals and hazards move faster too, so the drift q a tracker faces may rise | added by the independent review; **derived in §4c (v1.4.25), with the speed-up exponent β left as a measured input** |

The grouping into cases below is a checklist, not a result proved complete. Reach (how far one tracker can serve) is decided first by topology (§4, §4b); whether to centralize is decided by Π2 to Π7.

Cases:

- **Case A. No shortcut (τ_eff ≥ the outside light-time).** LAT-1 unchanged. Federation beyond L_max. Includes the case that GJW-type wormholes are not faster than the outside route (CONDITIONAL on that reading).
- **Case B. Shortcut, few mouths.** Station coverage (§4). The reach grows from a light ball to a union of light balls around mouths; partial centralization of the shared drift near mouths, federation elsewhere.
- **Case C. Shortcut, many mouths, throats with ample capacity, ρ high, d/c small.** §2: pool the shared component within covered regions. Private drift (the residuals u_i) still federates, because pooling cannot help what is not shared (§2, partial sharing). The upper limit on any store is the holographic bound.
- **Case D. Shortcut that allows loops.** Then ℓ can be zero or negative for some pairs, and the model's staleness term (ℓ ≥ 0) is no longer defined. Morris, Thorne & Yurtsever (1988) showed wormholes can become time machines (title: "Wormholes, Time Machines, and the Weak Energy Condition"); Hawking (1992) conjectures that physics prevents it (making closed timelike curves would need a violation of the averaged weak energy condition on a compactly generated Cauchy horizon, and back-reaction would prevent them; I read a summary of the abstract). Under that conjecture Case D does not occur. If it did, the theory would not give a prediction, and that is stated as a limit, not hidden.

**Is Chad's open versus finite split right?** For reach, yes, and it is the first split (§4b, corrected after the independent review; the first version of this note called it secondary). Finite throats with a per-hop latency leave LAT-1 in place with a faster effective speed. Open throats remove the distance limit. For whether to centralize, it is incomplete: capacity (Π2), shared drift and the telling price (Π3), upkeep (Π4), reliability (Π6) and causality (Π5) are independent of it. Two systems with the same topology can sit in different cases.

## 4. Station catchment: how far a shortcut network reaches (DERIVED; simulated)

Mouths ("stations") as a Poisson process of density ν, **each one hop from the tracker** (a star of throats, or an open network); a target is served if some station is within light-distance c·(ℓ* − τ), where ℓ* = (D*/q)^{1/(α−1)} is the tolerable latency (so L_max = cℓ*) and τ the hop latency through the throat. Then the fraction of targets with a station in reach is

1 − exp(−(4π/3)·ν·(c(ℓ* − τ))³),

united with the direct light ball of radius cℓ* around the tracker. The simulation matches this formula to within 0.005 absolute at the nine (ν, r) points checked (e.g. ν = 100, r = 0.1: 0.347 simulated, 0.342 formula; ν = 1000, r = 0.05: 0.408 and 0.408). Coverage reaches 95% when ν ≳ 0.72/(c(ℓ* − τ))³ (from −ln 0.05 = 3.0 divided by 4π/3).

Findings (saved output, part c): with ν = 0 the coverage is the light ball alone (0.030 for ℓ* = 0.2); at ν = 100 it is 0.967 for τ = 0, 0.365 for τ = 0.1 and 0.030 for τ = 0.19. **Hop latency eats the budget:** a shortcut whose hop latency is nearly the whole budget adds nothing. Dependence on τ is cubic through (ℓ* − τ)³, so it is steep.

## 4b. Finite throats: the tube map (DERIVED by the independent review; simulated)

Now let a throat join only mouths within a distance Λ of each other, with hop latency τ, and let signals cross between mouths at light speed. Reaching a target at distance D takes at least about (D/Λ)·τ, so a chain of hops behaves like a medium with effective speed **v_eff ≤ Λ/τ** (the bound is reached as mouths get dense; transfers between mouths slow it). Then LAT-1 holds with c replaced by v_eff: **L_max = v_eff·(D\*/q)^{1/(α−1)}**, and beyond it a system must still federate.

Simulation (`reach_checks/independent_review_checks.py`, part B; mouths of density 2 in a box of side 10, c = 1). The slope of latency against distance was 1.000 with light only; 0.138 for Λ = 1, τ = 0.1 (bound 0.100); 0.447 for Λ = 1, τ = 0.3 (bound 0.300); 0.057 for Λ = 2, τ = 0.1 (bound 0.050). With open throats (any to any, τ = 0.1) it was −0.001, and with τ = 0 on a percolating throat network −0.003, so no distance limit.

Reading. A finite tube map is a faster medium: the theory's federation result survives with a bigger constant. An open network, or instant hops on a connected network, removes the distance limit, and then only the economics (§2, §3) decide the design. Label: DERIVED (in-model), CONDITIONAL on shortcuts existing.

## 4c. Throat reliability and endogenous drift (DERIVED in-model; checked by simulation; v1.4.25)

Same setup as §2 (α = 2, diffusive drift, error variance of a target = w·σ² times the **age** of its last delivered reading, read price c, telling price d per attempt, N targets, update interval T). Everything here is CONDITIONAL on shortcuts existing, and on the cost model. Code and saved output: `reach_checks/wormhole_reliability.py`, `wormhole_reliability.out`.

**(a) Independent delivery failure.** Let s = (1 − p)^h be the probability that one telling reaches a target in one cycle (per-hop failure p, h hops, no retry within the cycle). A failed target stays stale until a later cycle succeeds, so the mean age is **T(2 − s)/(2s)** instead of T/2 (Monte Carlo of the age process, 400,000 cycles: 0.6105 against 0.6111 at s = 0.9; 3.4905 against 3.5000 at s = 0.25). The central cost rate is √(2(c + N·d)·N·w·σ²·g) with **g = (2 − s)/s = 2(1 − p)^{−h} − 1** (about 1 + 2hp for small p), so at zero extra latency **central wins iff d/c < 1/g − 1/N**. With retry until acknowledged (attempts per target 1/s, age unchanged, retry latency ignored) **central wins iff d/c < s·(1 − 1/N)**. Brute force over T against both closed forms: 0 disagreements in 979 cases (N = 4, 16, 100; s = 1 to 0.5; d/c from 0 to 1; cases within 10⁻³ of a boundary skipped). Examples at N = 16: reliable throats d/c < 0.9375; p = 0.1, h = 1 (s = 0.9, g = 1.22): d/c < 0.756 without retry and 0.844 with retry; s = 0.5: 0.271 and 0.469. Unreliable throats make pooling cost more, and the loss compounds with hops.

**(b) Outages (throats that open and close).** Model the throat as an alternating up/down process with up-fraction A and down times X (mean θ, squared coefficient of variation CV²), with queued updates delivered newest-first at reopening. By renewal-reward the mean age is **T/2 + (1 − A)·E[X²]/(2E[X]) = T/2 + (1 − A)·θ·(1 + CV²)/2**. This is exactly the §2 latency rule with ℓ equal to that extra term. So with a cost linear in age, **only the mean matters, and random outages act as an added mean latency**, larger for heavy-tailed outages than for exponential ones at the same mean. Simulation (T = 1, up mean 10, θ = 2): exponential 0.8304 against formula 0.8318; gamma (CV² = 0.25) 0.7084 and 0.7084; constant 0.6663 and 0.6663; a heavy-tailed lognormal (CV² = 3.2) 1.1836 against 1.2058 (1.8% below; sampling noise from about 3×10⁵ cycles of a heavy tail). Caveat: if the design has a hard error cap D\* (LAT-1's constraint form) rather than a linear cost, the **tail** of the outage law matters, not just the mean (for exponential outages the chance an outage exceeds a budget b is e^{−b/θ}; stated, not simulated). It also assumes outages are independent of the drift.

**(c) Reach with unreliable throats.** For stations that are one hop from the tracker (§4), independent throat failure p thins the Poisson station process, so coverage is **1 − exp(−(4π/3)·(1 − p)·ν·(c(ℓ\* − τ))³)**, the §4 formula with ν → (1 − p)·ν (simulation: 0.250 against 0.254 and 0.158 against 0.154 at ν = 100, r = 0.1, p = 0.3 and 0.6; four more points in the output). For the tube map of §4b with throats failing independently (quenched), failures can only remove edges, so v_eff ≤ Λ/τ still holds as a bound and latency can only rise. Simulation (box 10, mouths density 2, Λ = 1, τ = 0.1, 3 realisations per p): latency slope against distance 0.150, 0.173, 0.188 at p = 0, 0.3, 0.6; then 0.442, 0.686 and 0.847 at p = 0.8, 0.9, 0.95; and 1.000 (light only) at p = 1. So the tube map degrades slowly until about 60% of throats fail and then falls toward light speed, consistent with the throat network losing percolation; I did not compute the threshold. (The slope at p = 0, 0.150, differs a little from §4b's 0.138 because of seeds and realisations.)

**(d) Endogenous drift (Π7).** Let the world's drift rate rise once signals speed up by a factor m, q = q₀·m^β (β ≥ 0, a **measured input**; the theory does not predict it). Then:

- **The zero-latency rule is invariant.** Both designs scale as √q, so central beats local iff d/c < 1 − 1/N, unchanged by a common acceleration of the drift. (Brute force at q = 0.25 to 16.)
- **Tolerable latency shrinks as q^{−1/2}.** ℓ_crit = T\*_local·(1 − √((1 + N·d/c)/N)) and T\*_local = √(2c/q), so ℓ_crit·√q is constant (1.0607, 0.3536 and 1.0678 across q = 0.25 to 16, for the three cases in the output).
- **Reach.** With LAT-1's L_max = v·(D\*/q)^{1/(α−1)} and v = m·c: **L_max ∝ m^{1 − β/(α−1)}**. So shortcuts extend reach only if **β < α − 1**. At α = 2: β = 0.5 gives √m, **β = 1 gives no gain at all** (a Red Queen case: the world speeds up exactly as fast as the signals), and β = 1.5 shrinks the reach as m^{−1/2}. At α = 3 a gain survives unless β ≥ 2. Table in the saved output.
- **Partial sharing.** 1/N\*(ρ) = (√(1 + ρ) − 1)/(√(1 + ρ) + 1) (identity checked), which rises with ρ. So if the acceleration falls on the **shared** drift (ρ up) the range of d/c over which pooling wins widens, and if it falls on the **private** drift (ρ down) it narrows.

Label: DERIVED (in-model; the closed forms are algebra and were checked by simulation or brute force to the tolerances stated), CONDITIONAL on shortcuts existing and on the cost model; CLAIM_MAP N47. No claim about whether β is above or below α − 1 in any real system. **I have not had these derivations independently checked.**

## 5. The ceiling (PRIOR ART for the bound; DERIVED for its use here)

No store can hold more than the holographic bound allows: the area of any surface limits the information in the adjacent spacetime region, at 1.4×10⁶⁹ bits per square metre (Bousso 2002, abstract). A central store pooling the world's shared drift therefore has a maximum size, and one at the bound is a black hole (class frozen, in this theory's classes). So even Case C is not "one infinite brain": it is bounded by capacity and by the Landauer floor on erasure (THEORY §2.3, SCALE_ENDS). I do not claim a number for the bound at any particular store.

## 6. Physics check, and a correction

- **Exotic matter.** Traversable wormholes of the Morris–Thorne kind need matter that violates the weak energy condition (the title of Morris, Thorne & Yurtsever 1988). I read the abstract only here and cite the titles and the abstract-level claims; no such matter is known.
- **Quantum traversable wormholes.** Gao, Jafferis & Wall (2016) obtain a traversable BTZ wormhole in AdS from a coupling that produces negative average null energy; they note it "cannot be used to violate causality"; Maldacena, Stanford & Yang (2017) discuss teleportation-like traversal and limits on the information. These live in anti-de Sitter space and are not claims about our universe.
- **NASA "X-points" (2012).** Science@NASA's own piece, "Hidden Magnetic Portals Around Earth" (ScienceCast, 28 June 2012), used the word "portals". It describes "X-points or electron diffusion regions" (Jack Scudder, from Polar spacecraft data), where Earth's magnetic field connects to the Sun's by magnetic reconnection, and says THEMIS and Cluster observations suggest they "open and close dozens of times each day". They are magnetic-field connections that let solar particles into the magnetosphere, not wormholes in spacetime. Primary source cited from its transcript as returned by a web search; a short secondary news page was also read. Nothing in the theory depends on them.

## 7. Predictions and kill conditions

| Row | Claim | Label | Kill condition |
|---|---|---|---|
| N41 | The pooling and coverage forms in §2 and §4 (including the partial-sharing rule d/c < 1/N\*(ρ) − 1/N and the tube-map speed v_eff ≤ Λ/τ, §4b); the case grouping in §3 is a checklist, not part of this label | PROVED (in-model) for the closed forms; CONDITIONAL on the cost model and on shortcuts existing | An algebra or sampling error (checked here to 10⁻³ and 0.005); or a shown inconsistency with the T3a form at d = 0 |
| N42 | In ordinary networks with a latency shortcut (a relay, content-delivery node, a fast fibre or microwave link), centralized pooling of a shared signal beats local reads iff d/c < 1 − 1/N at zero latency | HYPOTHESIS (testable with real systems; no data collected) | A system with measured read cost c, dissemination price d, shared drift ρ ≈ 1 and N, where d/c < 1 − 1/N holds and the local design is still cheaper after adding latency, with ρ and N measured independently. Must meet MV1 to MV10 before a prereg locks |
| N47 | Reliability and endogenous drift (§4c): per-cycle delivery failure s = (1−p)^h gives central wins iff d/c < 1/g − 1/N with g = (2−s)/s, or d/c < s(1 − 1/N) with retry; outages with up-fraction A add a mean latency (1−A)·θ(1+CV²)/2 to the §2 latency rule; independent station failure thins ν to (1−p)ν; the zero-latency rule is invariant to a common drift acceleration, the tolerable latency scales as q^{−1/2}, and reach scales as m^{1−β/(α−1)} for q = q₀m^β | PROVED (in-model) for the closed forms; CONDITIONAL on shortcuts existing and on the cost model; β is an unmeasured input | An algebra, simulation or brute-force disagreement beyond the stated tolerances; or an independent re-derivation that differs. No independent check yet |
| N46 | "GTAO predicts that wormholes exist or that distance will not matter" | WITHDRAWN as framing | n/a |

## References (opened)

- Bousso R 2002, "The holographic principle," *Rev Mod Phys* 74:825, arXiv hep-th/0203101 [abstract]
- Gao P, Jafferis DL, Wall AC 2017 (arXiv 2016), "Traversable wormholes via a double trace deformation," *JHEP*, arXiv 1608.05687 [abstract]
- Hawking SW 1992, "Chronology protection conjecture," *Phys Rev D* 46:603, doi 10.1103/PhysRevD.46.603 [abstract summary read; paper not]
- Maldacena J, Stanford D, Yang Z 2017, "Diving into traversable wormholes," *Fortschr Phys*, arXiv 1704.05333 [abstract]
- Morris MS, Thorne KS 1988, "Wormholes in spacetime and their use for interstellar travel," *Am J Phys* 56:395, doi 10.1119/1.15620 [metadata only]
- Morris MS, Thorne KS, Yurtsever U 1988, "Wormholes, time machines, and the weak energy condition," *Phys Rev Lett* 61:1446, doi 10.1103/PhysRevLett.61.1446 [metadata (title) only]
- Azriel M, 2012-07-05, "X-point portals connect Earth to Sun," Space Safety Magazine [short secondary news page read]
- Science@NASA 2012-06-28, "ScienceCasts: Hidden Magnetic Portals Around Earth," NASA Science (video; transcript as returned by a web search)
- Maldacena, Stanford & Yang 2017 [introduction read for the general-relativity statement, added by the independent review]
