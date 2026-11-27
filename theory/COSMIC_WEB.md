# The cosmic web as a network: what resembles organizations, brains and the internet, and what does not

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/web_null.py`, `web_null.out`; and, added in v1.4.25, `reach_checks/web_hubs_sdss.py`, `web_hubs_sdss.out` (§2b). Labels as in REACH.md (DERIVED / RESTATEMENT / PRIOR ART / HYPOTHESIS / CONDITIONAL). **Updated Wednesday 18 November 2026, late evening ET (v1.4.25): the "no hubs" claim is withdrawn (reading 3, §2b); the delay-versus-link-cost prior-art sweep is in §3b; a preregistered hub-test spec is in §8.**

**The idea tested (Chad, t1955/t1956).** The cosmic web looks like a network of organizations, a brain, or the internet; the theory should say what is shared and what is different, with real published network numbers. Treated as a hypothesis, not a spec.

## 0. Reading in plain words

1. **The resemblance is real but shallow.** The web is clustered and spatially embedded, as brains' local circuits and many spatial networks are. That much is shared.
2. **It is geometry plus gravitational structure, not function.** Linking points that are near each other already gives high clustering and positive degree correlation, whatever the points are. A random point set with the same linking rule (the published "random" curve in Coutinho et al.; my check below) does much of it. The real web's excess over that proper null is clear but bounded: a clustering of about 0.60 to 0.64 against about 0.44 to 0.47 for random positions at ⟨k⟩ ≥ 8, read by eye from their Fig. 4(c). Its in-degree spread is also broader than random positions give. That excess is real, nonlinear gravitational structure, so more than geometry is going on (Chad's point, t1955). What the theory denies is narrower: that any of it is tracking or selected design.
3. **"The web has no hubs" is withdrawn (v1.4.25).** The earlier text said none had been reported and none tested. A sweep found hubs. (a) Yang & Yu 2023 (*Phys Rev Research* 5:043187; text read) report a power-law in-degree distribution, exponent −2, for tree graphs that link each subhalo to its least massive host halo in N-body and hydrodynamic simulations (FIRE2, TNG50, Bolshoi): scale-free hubs produced by gravity alone. Those graphs are halo hierarchies inside single halos, not filament networks. (b) My own computation on SDSS galaxies (§2b; an own check, not a published pipeline, not independently reviewed) gives a radius-graph degree spread far above Poisson points in the same footprint (variance/mean 6.7 against 1.1 at ⟨k⟩ = 4; top-1% degree share 0.085 against 0.027) and below a Barabási–Albert graph of the same size (0.121; maximum degree 47 against 338). Degree in a radius graph is local density (Hong & Dey 2015 use degree centrality for exactly that), and clusters are dense, so hub-like heterogeneity is what clustering gives. What stays true: the nearest-neighbour rule caps in-degree by geometry, and Coutinho et al. publish no hub statistic. Whether the web's heterogeneity exceeds a two-point-matched null is **OPEN** (my lognormal null was inadequate; §2b). Independent review 2 built a better matched null (§2c): the data's hub share sits inside its spread (within 1.6 null standard deviations for three members of the null family), so there is no sign of a hub excess, but that null also misses the ξ gate at 5 to 11 Mpc/h and the hub share moves by a factor of two across nulls with the same two-point function, so the question stays OPEN; the spec in §8 is revised accordingly.
4. **Hubs do not need a priced delay (the FKP bridge to GTAO is a HYPOTHESIS, downgraded).** A priced trade-off between delay and link cost does produce hubs (Fabrikant–Koutsoupias–Papadimitriou 2002; Ferrer i Cancho & Solé 2003, star and hub phases; Gastner & Newman 2006; the same trade-off is in organization economics, Bolton & Dewatripont 1994 and Radner 1993; §3b). But gravity, growth and plain clustering produce hubs too (item 3). So seeing hubs does not show a priced delay, and the web's heterogeneity does not conflict with the theory. N40 can only be tested by how hub concentration depends on a measured price ratio, against growth and clustering nulls, never by the presence of hubs. For the web the theory predicts only that its degree structure is accounted for by initial conditions and gravity (N39), which item 3 is consistent with and which is not a distinct prediction.
5. **What the theory derives about the web itself: nothing it does not take as input.** The web's structure comes from the initial density fluctuations plus gravity, with gas physics, star formation and feedback shaping galaxies on small scales (Bond, Kofman & Pogosyan 1996: the final web is "present in embryonic form" in the initial overdensity pattern). GTAO calls this an unselected, untracked structure. That is a negative prediction (N39), not a silence.

## 1. Published network measurements, as opened

| Quantity | Value | Source and how it was read |
|---|---|---|
| Link rule | Model "M3": each galaxy linked by a directed edge to its closest galaxies (spatial proximity only); mean degree ⟨k⟩ a free parameter | Coutinho et al. 2016, arXiv 1604.03236 (full text read) |
| Giant strongly connected component | emerges at ⟨k⟩ = 4 for simulation (Illustris) and observation (SDSS, z < 0.03); at ⟨k⟩ = 3 for random positions | same, text and Fig. 4(b) |
| In-degree variance at ⟨k⟩ = 1, **random positions** | 0.709 (Poisson would give 1); the authors infer "hubs are definitely absent" next to this number | same, text: it is "for a random galaxy distribution" (analytic, their supplementary E), **not a measurement of the web** (attribution corrected by the independent review) |
| In-degree distribution, web | simulation and observation agree, and both "deviate from the random distribution"; at ⟨k⟩ = 20 broader than Poisson and than random positions, no heavy tail visible to k_in = 30 | same, text and **Fig. 4(a) read by eye**; no hub statistic is published |
| Clustering ⟨C⟩ | simulation and observation agree with each other, about 0.60 to 0.64 at ⟨k⟩ ≥ 8; random positions about 0.44 to 0.47 | same, **read by eye from Fig. 4(c); not in the text** (numbers re-read by the independent review) |
| Assortativity r | positive in all three curves, about 0.05 to 0.3, falling with ⟨k⟩; sim and obs below random at large ⟨k⟩ | same, **read by eye from Fig. 4(d); sign visible, values approximate** |
| Slice networks, simulated web and neuronal tissue | clustering peaks at C ≈ 0.1 to 0.4; degree centrality about three to four orders of magnitude above Erdős–Rényi; web degree-centrality distributions roughly Poissonian | Vazza & Feletti 2020, Front. Phys. 8:525731 (full text read). They compared with an Erdős–Rényi network only, whose clustering is ⟨k⟩/N ≤ 2×10⁻³, not with a proximity null |
| Spatial fluctuation structure (the web's initial cause) | the final web is present in embryonic form in the initial overdensity pattern | Bond, Kofman & Pogosyan 1996 (abstract read) |

Reference networks used for the comparison, as opened:

| Network | Published figure | Source and how it was read |
|---|---|---|
| *C. elegans* neural network | C = 0.28 vs 0.05 for a random graph of the same size and degree; L = 2.65 vs 2.25 | Watts & Strogatz 1998, Nature 393:440, Table 1 (full text read) |
| Western US power grid | C = 0.080 vs 0.005; L = 18.7 vs 12.4 | same |
| Film actors | C = 0.79 vs 0.00027; L = 3.65 vs 2.99 | same |
| Scale-free degree (WWW, genetic networks) | "vertex connectivities follow a scale-free power-law distribution", produced by growth plus preferential attachment | Barabási & Albert 1999, abstract read |
| Internal e-mail network of one organization (about 1,700 employees) | community structure is self-similar | Guimerà et al. 2003, arXiv cond-mat/0211498, abstract read. The degree distribution is not in the abstract and was not read |
| Hierarchy and span of control | not a network measurement; plain arithmetic: at least ln N / ln k_max levels if no node has more than k_max reports | below (ARITHMETIC) |

I did not open a primary source for the internet's router-level degree distribution here, so no internet numbers are quoted. The scale-free statement is only Barabási & Albert's abstract on the WWW.

## 2. Null models (my check, `reach_checks/web_null.py`)

Setup: 4,000 points in a periodic unit cube, fixed seed; a radius graph tuned to mean degree about 4 for Poisson points; Neyman–Scott clustered point sets as a crude stand-in for galaxy clustering (not a cosmological simulation).

| Point set and rule | ⟨k⟩ | var/mean | max k | clustering | assortativity |
|---|---|---|---|---|---|
| Poisson points, radius graph | 4.03 | 0.99 | 13 | **0.422** | **+0.474** |
| Clustered (200 parents, s = 0.03) | 13.04 | 3.80 | 40 | 0.648 | +0.601 |
| Clustered (60 parents, s = 0.02) | 57.59 | 4.05 | 118 | 0.871 | +0.514 |
| Erdős–Rényi, same N and ⟨k⟩ | 3.99 | 0.99 | 13 | 0.0009 | −0.011 |

The radius-graph rows above are not at matched mean degree (the radius was tuned for Poisson points), so their clustering is not comparable across point sets.

Directed nearest-neighbour rule (Coutinho's M3 style): every node has out-degree k, so mean in-degree equals k, and in-degree variance/mean is 0.60 to 1.05, maximum in-degree 4 to 11 for k = 1 to 4. At k = 1 Poisson points give 0.72, which is Coutinho's random-position value (0.709). At k = 20 the independent review's check (`reach_checks/independent_review_checks.py`, part D) gives 0.58 for Poisson points against 2.1 and 4.8 for two clustered sets (maximum in-degree 32 against 48): clustering of the points broadens the in-degree, as the web's Fig. 4(a) curve does, without a hub tail. A geometric packing limit (how many points can have a given point as their nearest neighbour) caps in-degree, so **absence of hubs is partly a property of the rule**.

Hub-and-spoke contrast (arithmetic, not data): a star has r = −1; a Barabási–Albert graph (m = 2, N = 4,000) has r = −0.065, clustering 0.0095, max degree 168 at mean degree 4.

What this shows (DERIVED, simulation only):
- Clustering far above Erdős–Rényi is produced by proximity alone (0.42 vs 0.0009). So the Vazza & Feletti clustering excess over Erdős–Rényi, taken alone, is not evidence of anything specific to the web or the brain. This is a limit of their comparison, not an error; they say in plain words they compared with Erdős–Rényi.
- Coutinho et al. do use a proper null (random positions, same rule). The web exceeds it in clustering (about 0.15 to 0.17, by eye), has a broader in-degree spread, and has lower assortativity than random positions at large ⟨k⟩.
- Positive assortativity is the proximity signature. Growth with preferential attachment gives zero to negative assortativity and almost no clustering. The two signatures are different, which is why they can be told apart.

Limits of this check: Neyman–Scott is not the web; the radius graph is not Coutinho's directed M3 rule; both are nulls to show what geometry alone does, not reconstructions.

## 2b. Hub statistics of the real galaxy proximity graph against matched nulls (own computation, v1.4.25; DATA CHECK, not independently reviewed)

Code and saved output: `reach_checks/web_hubs_sdss.py`, `web_hubs_sdss.out` (about 3.5 minutes at nice 19; deterministic seeds). **Data:** the SDSS DR17 legacy main galaxy sample, `z` 0.005 to 0.03, from the public SkyServer SQL service (no sign-in; query in the script), made volume-limited (M_r − 5 log h < −17.5, comoving distance 15 to 85 Mpc/h, flat ΛCDM with Ωm = 0.3, redshift-space positions): **N = 16,535 galaxies** in a footprint mask covering 8,796 deg². **Graph:** undirected radius graph with the linking length tuned to mean degree ⟨k⟩ = 4 and 10 in each point set separately, and a directed nearest-neighbour (M3-style) in-degree as a control. **Statistics:** degree variance/mean, maximum degree, and the **top-1% share** of total degree (the hub statistic; a flat graph gives about 0.025). **Nulls:** P, Poisson points in the same footprint and distance range; LN, a lognormal-field point set whose redshift-space two-point function was set from the data's measured ξ_s(r) (Landy–Szalay, 0.5 to 20 Mpc/h), 8 realisations, each drawn to N points. Reference graphs of the same N (Barabási–Albert, Erdős–Rényi) are for scale only.

| Radius graph, tuned to ⟨k⟩ = 4 | ℓ (Mpc/h) | var/mean | max degree | top-1% share | isolated |
|---|---|---|---|---|---|
| **SDSS galaxies** | 1.39 | **6.67** | **47** | **0.085** | 0.18 |
| P: Poisson points (8 sets) | 3.26 | 1.14 ± 0.02 | 14.9 ± 1.1 | 0.0268 ± 0.0007 | 0.03 |
| LN: lognormal, two-point matched (8) | 1.28 ± 0.31 | 33 ± 30 | 115 ± 58 | 0.21 ± 0.11 | 0.39 |
| Barabási–Albert m = 2, same N (reference) | n/a | 11.4 | 338 | 0.121 | n/a |
| Erdős–Rényi ⟨k⟩ = 4, same N (reference) | n/a | 1.01 | 13 | 0.025 | n/a |

| Radius graph, tuned to ⟨k⟩ = 10 | ℓ (Mpc/h) | var/mean | max degree | top-1% share |
|---|---|---|---|---|
| **SDSS galaxies** | 2.19 | **14.3** | **95** | **0.077** |
| P: Poisson | 4.48 | 1.46 ± 0.03 | 27 ± 2 | 0.0208 ± 0.0004 |
| LN: lognormal | 2.07 ± 0.45 | 51.6 ± 49 | 184 ± 67 | 0.15 ± 0.07 |
| Barabási–Albert m = 5, same N (reference) | n/a | 17.6 | 443 | 0.105 |

| Directed nearest-neighbour in-degree, variance/mean | k = 1 | k = 4 | k = 20 | max in-degree at k = 20 |
|---|---|---|---|---|
| **SDSS galaxies** | 0.69 | 0.92 | **2.50** | 43 |
| P: Poisson | 0.72 | 0.67 ± 0.01 | 0.97 ± 0.01 | 39 ± 1 |
| LN: lognormal | 0.73 ± 0.01 | 0.94 ± 0.01 | **2.52 ± 0.06** | 48 ± 1 |

What this shows, and does not:

1. **Against a geometry-only null the excess is clear (DATA CHECK).** The real galaxies' degree spread is about six to ten times Poisson's and their top-1% share about three to four times. At a fixed linking length the variance/mean excess also holds (6.7 against 1.0 at ℓ = 1.39 Mpc/h); the top-1% share is only informative at matched mean degree, because at that ℓ Poisson points have ⟨k⟩ = 0.33. So "the web has no hubs" is wrong as a statement about heterogeneity. It is also not a BA-type hub regime: the top-1% share is about 70% of BA's and the maximum degree one seventh to one fifth of it.
2. **Against a two-point-matched null, both statistics are unresolved** *(corrected by independent review 2)*. The directed nearest-neighbour in-degree variance of the galaxies agrees with the lognormal null at k = 1, 4 and 20 (2.50 against 2.52 ± 0.06 at k = 20), while Poisson gives 0.97. But this lognormal null failed its own two-point check (below), over-clustering by 1.2 to 1.6 at 2 to 7 Mpc/h, which is the scale the k = 20 neighbours span (about 5 Mpc/h at this density), so the agreement is not evidence; and with the better null of §2c the same statistic ranges from 2.33 to 2.88 across mocks with one two-point function. So the earlier reading, that Coutinho et al.'s "broader than random positions" in-degree "is what two-point clustering alone gives", is **withdrawn: INCONCLUSIVE** (their observation stays PRIOR ART). For the radius-graph hub statistics the LN null is **INCONCLUSIVE**: after one calibration pass its two-point function was still off (mock/data ξ_s about 2.5 at 0.63 Mpc/h, 1.6 at 1 Mpc/h, 1.2 to 1.6 out to 7 Mpc/h, 1.1 at 11 Mpc/h, 1.0 at 16 Mpc/h; see the printed check), and the mocks scatter strongly from realisation to realisation (variance/mean 33 ± 30). The calibration pass was tried because the first, uncorrected mocks fell below the data by 15 to 50% in ξ_s; an earlier version of the script that iterated per-bin corrections diverged, so I kept one pass and stopped rather than tune to noise (the mock-to-mock sample variance of ξ_s is itself large, because the field's variance is about 4). All that can be said is that the over-clustered lognormal null is more heterogeneous than the data on every hub measure, so there is no sign here of a hub excess over a two-point-matched field; that is not a test.
3. **Limits.** One galaxy catalogue and one realisation; redshift-space positions without a fingers-of-God correction; fibre collisions not corrected (they remove close pairs in dense regions); no K-correction (small at z ≤ 0.03); the lognormal null has no halo structure; my mask is built from the galaxies themselves; the informal Hill tail index in the saved output is noisy and is not used. The simulated-halo arm was not run (§8).

## 2c. A better matched null (independent review 2; DATA CHECK; not a locked test)

Code and output: `reviews/reach_2026-11-18/review2_checks/hub_nulls_hm.py`, `hub_nulls_hm.out` (about 18 minutes at nice 19; same data, mask, radius-graph rule and statistics as §2b; it needs `sdss_r0.csv` from §2b's query). The public SkyServer data were re-pulled and §2b's script was re-run first: its output reproduced exactly (N = 16,535; variance/mean 6.67, top-1% share 0.0849 at ⟨k⟩ = 4).

**Why the lognormal could not be fixed.** A finer-grid lognormal (512³ cells of 0.375 Mpc/h, cell-averaged zero lag; `reviews/reach_2026-11-18/review2_checks/hub_nulls_v2.py`) needs a Gaussian variance of 6.5 to reach ξ_s ≈ 16 at 0.6 Mpc/h, and calibration then diverged (variance 6.5 → 15 → 23 in three passes). A lognormal that matches ξ at these scales is dominated by a few cells, so it cannot pass §8's validation gate. This is a property of the null family, not a bug.

**The null used ("HM", halo-model style).** Every point traces a lognormal field smoothed at 1.5 Mpc/h (Gaussian variance about 1.5, so realisations are well behaved). This field carries ξ at r ≳ 4 Mpc/h. A fraction F of points sit in Gaussian groups (sizes 0.3 to 1.2 Mpc/h) whose amplitudes are fitted to the data's small-scale excess. The two-point function fixes only the product of F and the group occupancy m, so the null is a family. Three members were run (m = 15, 30, 60 members per group after thinning; F = 0.68, 0.34, 0.17), 30 fresh mocks each, all with seeds not used in calibration.

| HM member | mock/data ξ_s, 0.6–3.3 Mpc/h | at 4.9–10.8 Mpc/h | degree scatter at fixed ℓ | S1 at ⟨k⟩ = 4 (data 0.0849) | S1 at ⟨k⟩ = 10 (data 0.0774) | kNN k = 20 var/mean (data 2.50) |
|---|---|---|---|---|---|---|
| m = 15 | 1.03–1.11 | 1.20–1.26 | 18–19% | 0.069 ± 0.015 (z = +1.1) | 0.060 ± 0.018 (z = +1.0) | 2.79 ± 0.33 |
| m = 30 | 0.96–1.02 | 1.09–1.15 | 15–18% | 0.092 ± 0.014 (z = −0.5) | 0.065 ± 0.016 (z = +0.8) | 2.88 ± 0.17 |
| m = 60 | 1.00–1.05 | 1.10–1.17 | 15–21% | 0.157 ± 0.044 (z = −1.6) | 0.082 ± 0.017 (z = −0.3) | 2.33 ± 0.12 |

**Result.** (1) The data's hub share lies inside every member's spread (|z| ≤ 1.6), so §8's H_hub rule gives "within" for all three: **no sign of a hub excess over two-point clustering**. (2) But each member fails §8's ξ gate: ξ is matched to within 11% at the scales that set the degree, and is 9 to 26% high at 5 to 11 Mpc/h. So under §8 the result is **INVALID as a test, and the question stays OPEN**. (3) At one two-point function the null's S1 at ⟨k⟩ = 4 runs from 0.069 to 0.157, more than a factor of two. Degree variance in a radius graph is a three-point quantity, so a "two-point-matched" null does not fix it. Any reading of S1 against such a null is a statement about *that* null's higher-order structure. That is why §8 now names the null family and makes N-body-based mocks the primary null. Limits as in §2b, plus: the nulls are isotropic, with no redshift-space anisotropy, and the group sizes and occupancies are choices, not fits to a halo catalogue.

## 3. Where the shared features come from, in GTAO terms

**Shared: spatial cost shapes the graph (PRIOR ART, with DERIVED bridge).** Any network whose links cost something that grows with distance, and whose nodes interact locally, is clustered and positively degree-correlated. That holds for the web, brain tissue, power grids and road networks. In GTAO's terms the link-upkeep price is the shared part. Nothing GTAO-specific is needed to explain it.

**Different: delay is priced in organizations and the internet, and not in the web.** The Fabrikant–Koutsoupias–Papadimitriou model (FKP 2002, full text read, Theorem 1): nodes arrive at random in a region; node i links to the earlier node j that minimizes λ·d_ij + h_j, where d_ij is distance (link cost), h_j the hop count to the root (delay), and λ their price ratio. Result (Theorem 1, as stated for points in the unit square; proofs not checked): if λ < 1/√2, the graph is a star; if λ = Ω(√n), the degree distribution is exponential (a dynamic Euclidean minimum-spanning-tree-like graph, high degrees exponentially rare); if λ ≥ 4 and λ = o(√n), a power-law lower bound holds for part of the degree sequence. Berger, Bollobás, Borgs, Chayes & Riordan (ICALP 2003; abstract read) prove that the overall FKP degree distribution is far from a power law: almost all nodes have degree 1, and many nodes have near-maximum degree. So the FKP regime is star-like hubs rather than a scale-free spread. Either way, **a priced delay is one route to hubs** (v1.4.25: not the only one; gravity, growth and clustering give hubs too, §2b).

**Bridge to GTAO (HYPOTHESIS).** GTAO's tracker pays a lateness cost that rises with how stale its information is: under hold-last-value reads, mean-square error ∝ q·ℓ^{α−1} (LAT-1, CM-N27, OPEN), and it pays link or read upkeep. The same two terms appear in FKP's trade-off. The mapping is by analogy, not derivation: FKP's delay is hop count, not a staleness cost in a tracked process, and FKP has no drift. If the mapping holds, GTAO predicts that cost-driven hubness should increase with the lateness price relative to link price among tracking organizations, and should be absent where nothing tracks. If an organization with a hub is shown to have it from some other cause (a founding accident, a regulation), that is not a failure; the prediction is about the dependence on prices.

**What the theory takes as input about the web (N39).** The web's morphology follows from the initial density field and gravity, with baryonic physics (gas, star formation, feedback) on small scales (Bond et al. 1996). GTAO has no tracker and no selected design in it, so it makes the negative prediction that the web's topology is unrelated to any cost the web pays. It has no such cost.

**Organizations and span of control (ARITHMETIC, not a result of the theory).** If no node can handle more than k_max direct reports, a tree over N nodes needs at least ln N / ln k_max levels. The limit k_max is an input here, not derived by the theory, and I make no claim about hub degrees in connectomes (not read).

## 3b. Prior-art sweep for N40 (delay price against link price) and the price-to-λ map (v1.4.25)

**What exists (credit, and the novelty downgrade).** The trade-off between the price of delay (path length, hops) and the price of links, with hubs or a star as the cheap-delay answer, is established in several fields:

| Source | What it shows | How read |
|---|---|---|
| Fabrikant, Koutsoupias & Papadimitriou 2002 | growth model, link λ·distance plus hop-count delay; star, exponential and partly power-law regimes | full text (above) |
| Ferrer i Cancho & Solé 2003, "Optimization in complex networks" (arXiv cond-mat/0111222) | minimizing E(λ) = λ·d + (1 − λ)·ρ (normalized mean path length against link density) gives, as λ rises: sparse exponential-like networks and then truncated scale-free networks with hubs, both below λ\*₁ ≈ 0.25 (their Fig. 3: exponential at λ = 0.01, scale-free at λ = 0.08); a star phase for λ\*₁ < λ < λ\*₂ ≈ 0.80; then dense networks, becoming clique-like above λ\*₃ ≈ 0.95 (n = 100 in the runs shown). *Phase boundaries corrected by independent review 2, which re-read the arXiv text; the earlier wording put the star phase after 0.80* | full text read (their normalizations of d and ρ not re-derived) |
| Gastner & Newman 2006, "Shape and efficiency in spatial distribution networks," *J Stat Mech* P01015 | spatial networks trade total length against route length: the minimum spanning tree minimizes length and the star minimizes route factor; the real distribution networks they study come close to optimal on both (their Table I and text) | abstract and a secondary summary in v1.4.25; arXiv full text read by independent review 2 |
| Bolton & Dewatripont 1994, "The firm as a communication network," *QJE* 109:809 | organization structure as a trade-off among processing, specialization and communication time; efficient structures are centralized and pyramidal | abstract-level (search result); paper not opened |
| Radner 1993, "The organization of decentralized information processing," *Econometrica* 61:1109 | managers as capacity-limited processors; efficiency as a trade-off between the number of processors and decision delay; hierarchical trees | abstract-level (search result); paper not opened |
| Kawasaki 2008, "Network effects, heterogeneous time value and network formation in the airline market," *Reg Sci Urban Econ* 38:388 | hub-and-spoke against point-to-point when passengers' time value differs | description-level (RePEc); paper not opened |

So **the delay-versus-link-cost mechanism for hubs is PRIOR ART, including in organizations.** What N40 would add is narrower: reading the delay price as a *staleness cost in a tracked, drifting process* (LAT-1), and the hypothesis that one price ratio sets hub concentration across tracking systems. I found no source that tests that with measured prices. That is not proof of absence: the search was a few queries, and the economics and operations-research literature on hubs is large. Novelty claim for N40: none beyond that reading.

**Price-to-λ map (OPEN: definable, not yet measurable).** In the repo's FKP notation each new node joins the existing node j that minimizes λ·d_ij + h_j (distance and hop count to the root). Reading both terms as cost rates, with a region of side L:

**λ = u·L / (W·τ_h)**, where u is the link upkeep per unit length per unit time, so u·L is the cost rate of one region-length link; τ_h is the latency one hop adds; and W is the cost rate per unit of staleness of the information served through that route (for diffusive drift, α = 2, W = the stakes times the drift variance rate w·σ² summed over the targets the route serves, since the error variance grows linearly with age). Then W·τ_h is the cost rate of one hop of delay, and λ is dimensionless. Large λ means links are dear and delay is cheap (FKP: exponential degree, tree-like); λ < 1/√2 gives a star.

- **What is measurable in principle:** u (leased-line, fibre or route cost per unit length), τ_h (per-hop forwarding latency, from traces or logs).
- **What is not yet measured for any system I know of:** W, the cost of staleness. It needs a measured curve of decision or outcome loss against information age, the quantity LAT-1 is about. No data set is identified.
- **Where it is not defined:** networks without a distance (an organization chart has no embedding), and multi-root systems, since FKP has a single root. For abstract networks the Ferrer i Cancho–Solé energy applies instead, with λ/(1 − λ) = (delay price per unit of their normalized path length) / (link price per unit of their normalized density); their normalizations must be applied and I did not re-derive them.
- **Control that any test needs:** a growth null and a clustering null. Preferential growth and clustering give hubs with no delay price (§2b), so the dependence of hub concentration on measured λ across systems is the only test; the presence of hubs is not.

Label: PRIOR ART for the mechanism; OPEN for the GTAO reading and the map (CLAIM_MAP N40, N50).

## 4. Shared and different, in one table

| Feature | Cosmic web | Organization | Brain | Internet / WWW | Source of the feature in GTAO terms | Label |
|---|---|---|---|---|---|---|
| Clustering above Erdős–Rényi | yes (but a proximity null gives about 0.42) | not measured here | yes, C = 0.28 (*C. elegans*) | not measured here | link-upkeep with distance | PRIOR ART |
| Positive degree correlation | yes (by eye) | not measured here | not measured here | not measured here | proximity | PRIOR ART |
| Hubs | hub-like heterogeneity from clustering and gravity (§2b; Yang & Yu 2023 for halo hierarchies: power law, exponent −2); Coutinho et al.'s nearest-neighbour rule caps in-degree by construction; no hub statistic against a two-point-matched null exists (OPEN) | not read here | not read here | WWW: scale-free degree (abstract) | priced delay is one route (FKP; Ferrer i Cancho & Solé; §3b); gravity, growth and clustering are others | HYPOTHESIS (dependence on the price ratio); presence of hubs is not diagnostic |
| Adaptive rewiring in response to a changing environment | none | yes (informal ties form when unexpected situations arise; Guimerà et al. abstract) | yes in development and learning (not read here) | yes (operators re-route) | tracker with upkeep and lateness | HYPOTHESIS for the dependence; the web's absence is PRIOR ART |
| Self-similar community structure | not tested here | yes (one organization) | not read | not read | scale-free demand, T7 | OPEN |

Empty cells say "not read here". They are not "no".

## 5. Plain answer

The resemblance between the cosmic web and an organization is mostly of the same kind as the resemblance between a spider web and a road map: both are networks of local links in space. The web adds real gravitational structure on top (more clustering and a broader degree spread than random positions give), so "just geometry" undersells it. But nothing in that structure needs a tracker. The theory says what is shared (link cost with distance) and what is not (a priced delay, one route to hubs, and a tracker that rewires). The sharper negative prediction is that **no feature of the cosmic web's topology depends on a cost the web pays**, because it pays none that the theory counts. Whether that is testable is limited: the web's observed topology is already explained by gravity from the initial field, which is a rival the prediction cannot beat but does not need to.

## 6. Predictions and miss conditions

| Row | Prediction | Label | Miss condition |
|---|---|---|---|
| N39 | The web's topology is accounted for by initial conditions plus gravity and baryonic physics; GTAO adds nothing. Negative prediction | PRIOR ART (consistent with Bond et al. 1996; v1.4.25: hub-like degree heterogeneity in halo networks is also gravitational, Yang & Yu 2023, §2b) | A web feature shown to depend on a tracked quantity (for example one that correlates with a cost paid by the web) rather than on initial conditions and gravity. Not expected |
| N40 | Among tracking networks (organizations, communication systems), hub degree increases with the ratio lateness price / link price; where nothing tracks, no cost-driven hubs | OPEN (HYPOTHESIS; v1.4.25: the delay-versus-link-cost trade-off is PRIOR ART in several fields, §3b, so only the staleness-cost reading and the measured-price dependence are GTAO's; presence of hubs is not diagnostic, since gravity and growth give hubs too) | A preregistered cross-section of at least a stated number of organizational or communication networks in which hub concentration (for example the top-1% degree share) is uncorrelated or negatively correlated with a measured delay-cost to link-cost ratio, with proximity-null and growth-null controls. Must meet MV1 to MV10 before a prereg locks; the price-to-λ map is now defined for single-root networks embedded in space (§3b: λ = u·L/(W·τ_h)) but its staleness-cost input W has not been measured for any system, so the prediction still cannot be run |
| (control) | A proximity-only null reproduces the clustering and positive assortativity of any spatial network | DERIVED (simulation) | Not a prediction about the theory; it is a requirement on any test: compare with a proximity null, not with Erdős–Rényi |

## 7. What would change my mind about the reading

**Partly done in v1.4.25 (§2b).** Against a geometry-only null the web's heterogeneity is clearly higher. Against a two-point-matched null both the nearest-neighbour in-degree and the radius-graph hub statistic are **unresolved** (the first reading of the in-degree as matched was withdrawn by independent review 2, because the lognormal null had failed its check). §2c's better null finds no hub excess but does not pass the §8 gate, and shows the hub share depends on the null's higher-order structure. A reanalysis with N-body-based mocks (spec in §8) is still needed. It cannot support or refute GTAO, since both outcomes are gravity.

## 8. Preregistered spec: hub statistic against a two-point-matched null (OPEN; not run; no outcome known; v1.4.25)

**Purpose and limit.** To settle whether the web's hub-like heterogeneity exceeds what two-point clustering gives (the unresolved part of §2b). This is a **control for N39 and a correction to this note's earlier "no hubs" wording. It is not a test of N40:** every outcome measures gravity, so using it as evidence about a priced delay would be a mismatched proxy (INVALID, not FAILED).

1. **Data (two arms, one code path).** (a) Simulated: a z = 0 friends-of-friends halo catalogue from a dark-matter-only box with a mass cut giving N between 20,000 and 40,000, for example IllustrisTNG TNG100-1-Dark (75 Mpc/h box). As I understand it the TNG downloads need a free account and API key; I did not create one, so I did not run this arm. A second code (Millennium or Bolshoi halos) if obtainable without a sign-in. (b) Observed: the volume-limited SDSS sample of §2b, plus one independent volume-limited redshift sample from another survey.
2. **Graph rule (fixed before looking).** Undirected radius graph, ℓ tuned so ⟨k⟩ = 4 and 10 in each point set separately. The directed nearest-neighbour (M3) in-degree is reported as a control only, since geometry caps it.
3. **Nulls** *(revised by independent review 2; see §2c)*. **Primary null: mocks built from N-body halos** (a halo-occupation model fitted to the data's ξ_s and number density, with redshift-space distortions applied in the same way as the data, and fibre collisions imposed on the mocks or corrected in the data), because the hub statistic depends on structure beyond two-point, and only a gravity-based null fixes that structure in a meaningful way. A lognormal null cannot be validated at these scales (§2c), and a halo-model-style null with free occupancy gives a factor-two spread in S1. Any secondary null must be named, with its free parameters fixed before looking. P: Poisson in the same geometry. Secondary: a Gaussian-field-based mock set whose ξ(r) matches the data's within 10% over 1 to 20 Mpc/h, checked with Landy–Szalay on at least 20 mocks that were not used for tuning, and whose mean degree at fixed ℓ scatters by no more than 30% between mocks (otherwise use a generator with less variance or a larger box, since §2b's lognormal field failed this). The null fails validation, and the test is INVALID, if either check fails.
4. **Statistic.** Primary: S1, the top-1% share of total degree. Secondary: degree variance/mean and k_max/⟨k⟩. At least 50 null sets per null.
5. **Pass/fail.** H_hub: S1(real) exceeds the LN-matched mean by more than 3 null standard deviations and by at least 25%, at both ⟨k⟩ = 4 and 10, in both arms. Then: the web's heterogeneity exceeds that of the named null (with the N-body-based null, structure the halo model does not capture). Do not read it as "beyond two-point clustering" in general, since two-point matching does not fix S1 (§2c). If S1(real) is within 3 standard deviations: accounted for by two-point clustering at this resolution. If below by more than 3: less heterogeneous than the matched field. All three agree with N39.
6. **Gates.** MV1 to MV10 before locking; power sized by a pilot; MV9's external timestamp needs Chad's go.

## References (opened)

- Berger N, Bollobás B, Borgs C, Chayes J, Riordan O 2003, "Degree distribution of the FKP network model," ICALP 2003, LNCS 2719:725–738, doi 10.1007/3-540-45061-0_57; journal version *Theor Comput Sci* 379:306–316 (2007) [abstracts read; added by the independent review]
- Barabási A-L, Albert R 1999, "Emergence of scaling in random networks," *Science* 286:509, arXiv cond-mat/9910332 [abstract]
- Bond JR, Kofman L, Pogosyan D 1996, "How filaments are woven into the cosmic web," *Nature* 380:603, arXiv astro-ph/9512141 [abstract]
- Coutinho BC, Hong S, Albrecht K, Dey A, Barabási A-L, Torrey P, Vogelsberger M, Hernquist L 2016, "The network behind the cosmic web," arXiv 1604.03236 [full text read; Fig. 4 viewed]. A 2018 related paper (Libeskind et al.) was **not** opened and is not cited.
- Fabrikant A, Koutsoupias E, Papadimitriou CH 2002, "Heuristically optimized trade-offs: a new paradigm for power laws in the internet," ICALP 2002 [full text read for the model and Theorem 1; proofs not checked]
- Guimerà R, Danon L, Díaz-Guilera A, Giralt F, Arenas A 2003, "Self-similar community structure in organisations," arXiv cond-mat/0211498 [abstract]
- Vazza F, Feletti A 2020, "The quantitative comparison between the neuronal network and the cosmic web," *Front Phys* 8:525731, doi 10.3389/fphy.2020.525731 [full text read]
- Watts DJ, Strogatz SH 1998, "Collective dynamics of 'small-world' networks," *Nature* 393:440, doi 10.1038/30918 [full text read, Table 1]
- Ferrer i Cancho R, Solé RV 2003, "Optimization in complex networks," in *Statistical Mechanics of Complex Networks*, Springer LNP 625:114–126, arXiv cond-mat/0111222 [full text read; added v1.4.25]
- Gastner MT, Newman MEJ 2006, "Shape and efficiency in spatial distribution networks," *J Stat Mech* P01015, arXiv cond-mat/0409702 [abstract and secondary summary in v1.4.25; arXiv full text read by independent review 2]
- Bolton P, Dewatripont M 1994, "The firm as a communication network," *Q J Econ* 109:809–839, doi 10.2307/2118349 [abstract-level; added v1.4.25]
- Radner R 1993, "The organization of decentralized information processing," *Econometrica* 61:1109–1146, doi 10.2307/2951495 [abstract-level; added v1.4.25]
- Kawasaki A 2008, "Network effects, heterogeneous time value and network formation in the airline market," *Reg Sci Urban Econ* 38:388–403 [description-level (RePEc); added v1.4.25]
- Hong S, Dey A 2015, "Network analysis of cosmic structures: network centrality and topological environment," *MNRAS* 450:1999, arXiv 1504.00006, doi 10.1093/mnras/stv722 [abstract; added v1.4.25]
- Yang D, Yu H-B 2023, "Graph model for the clustering of dark matter halos," *Phys Rev Research* 5:043187, arXiv 2206.05578 [abstract and the section on the FIRE2, TNG50 and Bolshoi in-degree distributions read; added v1.4.25]
- SDSS DR17 SkyServer SQL service (public, no sign-in), query in `reach_checks/web_hubs_sdss.py` [data used in §2b]
- Not opened: a Zenodo preprint on Millennium-halo percolation (found in a search, 403 on fetch; not peer reviewed as far as I can tell) and a 2015 Stanford CS224W student project on Illustris Delaunay degrees (snippet only); neither is relied on.
