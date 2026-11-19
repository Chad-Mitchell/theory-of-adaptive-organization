# The cosmic web as a network: what resembles organizations, brains and the internet, and what does not

Wednesday 18 November 2026, evening ET. Companion to [`REACH.md`](REACH.md) (§5). Code and saved output: `reach_checks/web_null.py`, `web_null.out`. Labels as in REACH.md (DERIVED / RESTATEMENT / PRIOR ART / HYPOTHESIS / CONDITIONAL).

**The idea tested (Chad, t1955/t1956).** The cosmic web looks like a network of organizations, a brain, or the internet; the theory should say what is shared and what is different, with real published network numbers. Treated as a hypothesis, not a spec.

## 0. Verdict in plain words

1. **The resemblance is real but shallow.** The web is clustered and spatially embedded, as brains' local circuits and many spatial networks are. That much is shared.
2. **It is mostly geometry, not function.** Linking points that are near each other already gives high clustering and positive degree correlation, whatever the points are. A random point set with the same linking rule (the published "random" curve in Coutinho et al.; my check below) does much of it. The excess of the real web over that proper null is modest (a clustering of about 0.55 to 0.6 against about 0.4 for random positions, read by eye from their Fig. 4(c)).
3. **The big difference is hubs.** Organizations, the internet and the web graph have hubs (some nodes with enormous degree). The published cosmic-web networks have none: the in-degree variance is below the Poisson value. Part of that is built into the nearest-neighbour link rule they used (my check below), so it is not a finding about the universe alone.
4. **Why hubs appear elsewhere, in this theory's terms (HYPOTHESIS).** A hub is what you get when the price of delay is high compared with the price of a link (the Fabrikant–Koutsoupias–Papadimitriou trade-off, Theorem 1). GTAO's own two costs (link upkeep and lateness) are the same trade-off. The web pays for neither: it tracks nothing, so nothing in it is penalized for being late. So the theory predicts no cost-driven hubs in the web, and that is what is published.
5. **What the theory derives about the web itself: nothing it does not take as input.** The web's structure comes from the initial density fluctuations plus gravity (Bond, Kofman & Pogosyan 1996: the final web is "present in embryonic form" in the initial overdensity pattern). GTAO calls this an unselected, untracked structure. That is a negative prediction (N39), not a silence.

## 1. Published network measurements, as opened

| Quantity | Value | Source and how it was read |
|---|---|---|
| Link rule | Model "M3": each galaxy linked by a directed edge to its closest galaxies (spatial proximity only); mean degree ⟨k⟩ a free parameter | Coutinho et al. 2016, arXiv 1604.03236 (full text read) |
| Giant strongly connected component | emerges at ⟨k⟩ = 4 for simulation (Illustris) and observation (SDSS, z < 0.03); at ⟨k⟩ = 3 for random positions | same, text and Fig. 4(b) |
| In-degree variance at ⟨k⟩ = 1 | 0.709 (Poisson would give 1) | same, text: "hubs are definitely absent" |
| Clustering ⟨C⟩ | simulation and observation agree with each other, about 0.55 to 0.6 at ⟨k⟩ ≳ 8; random positions about 0.4 | same, **read by eye from Fig. 4(c); not in the text** |
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

Directed nearest-neighbour rule (Coutinho's M3 style): every node has out-degree k, so mean in-degree equals k, and in-degree variance/mean is 0.60 to 1.05, maximum in-degree 4 to 11 for k = 1 to 4. A geometric packing limit (how many points can have a given point as their nearest neighbour) caps in-degree, so **absence of hubs is partly a property of the rule**.

Hub-and-spoke contrast (arithmetic, not data): a star has r = −1; a Barabási–Albert graph (m = 2, N = 4,000) has r = −0.065, clustering 0.0095, max degree 168 at mean degree 4.

What this shows (DERIVED, simulation only):
- Clustering far above Erdős–Rényi is produced by proximity alone (0.42 vs 0.0009). So the Vazza & Feletti clustering excess over Erdős–Rényi, taken alone, is not evidence of anything specific to the web or the brain. This is a limit of their comparison, not an error; they say in plain words they compared with Erdős–Rényi.
- Coutinho et al. do use a proper null (random positions, same rule), and the web exceeds it modestly, in clustering by eye, and has lower assortativity than random positions at large ⟨k⟩.
- Positive assortativity is the proximity signature. Growth with preferential attachment gives zero to negative assortativity and almost no clustering. The two signatures are different, which is why they can be told apart.

Limits of this check: Neyman–Scott is not the web; the radius graph is not Coutinho's directed M3 rule; both are nulls to show what geometry alone does, not reconstructions.

## 3. Where the shared features come from, in GTAO terms

**Shared: spatial cost shapes the graph (PRIOR ART, with DERIVED bridge).** Any network whose links cost something that grows with distance, and whose nodes interact locally, is clustered and positively degree-correlated. That holds for the web, brain tissue, power grids and road networks. In GTAO's terms the link-upkeep price is the shared part. Nothing GTAO-specific is needed to explain it.

**Different: delay is priced in organizations and the internet, and not in the web.** The Fabrikant–Koutsoupias–Papadimitriou model (FKP 2002, full text read, Theorem 1): nodes arrive at random in a region; node i links to the earlier node j that minimizes λ·d_ij + h_j, where d_ij is distance (link cost), h_j the hop count to the root (delay), and λ their price ratio. Result (Theorem 1, as stated for points in the unit square; proofs not checked): if λ < 1/√2, the graph is a star; if λ = Ω(√n), the degree distribution is exponential (a dynamic Euclidean minimum-spanning-tree-like graph, high degrees exponentially rare); if λ ≥ 4 and λ = o(√n), the degrees follow a power law. So **hubs are the signature of a priced delay**.

**Bridge to GTAO (HYPOTHESIS).** GTAO's tracker pays a lateness cost that rises with how stale its information is: under hold-last-value reads, mean-square error ∝ q·ℓ^{α−1} (LAT-1, CM-N27, OPEN), and it pays link or read upkeep. The same two terms appear in FKP's trade-off. The mapping is by analogy, not derivation: FKP's delay is hop count, not a staleness cost in a tracked process, and FKP has no drift. If the mapping holds, GTAO predicts that cost-driven hubness should increase with the lateness price relative to link price among tracking organizations, and should be absent where nothing tracks. If an organization with a hub is shown to have it from some other cause (a founding accident, a regulation), that is not a failure; the prediction is about the dependence on prices.

**What the theory takes as input about the web (N39).** The web's morphology follows from the initial density field and gravity (Bond et al. 1996). GTAO has no tracker and no selected design in it, so it makes the negative prediction that the web's topology is unrelated to any cost the web pays. It has no such cost.

**Organizations and span of control (ARITHMETIC, not a result of the theory).** If no node can handle more than k_max direct reports, a tree over N nodes needs at least ln N / ln k_max levels. The limit k_max is an input here, not derived by the theory, and I make no claim about hub degrees in connectomes (not read).

## 4. Shared and different, in one table

| Feature | Cosmic web | Organization | Brain | Internet / WWW | Source of the feature in GTAO terms | Label |
|---|---|---|---|---|---|---|
| Clustering above Erdős–Rényi | yes (but a proximity null gives about 0.42) | not measured here | yes, C = 0.28 (*C. elegans*) | not measured here | link-upkeep with distance | PRIOR ART |
| Positive degree correlation | yes (by eye) | not measured here | not measured here | not measured here | proximity | PRIOR ART |
| Hubs | no (in-degree variance 0.709 at ⟨k⟩ = 1; partly built in) | not read here | not read here | WWW: scale-free degree (abstract) | priced delay (FKP) | HYPOTHESIS |
| Adaptive rewiring in response to a changing environment | none | yes (informal ties form when unexpected situations arise; Guimerà et al. abstract) | yes in development and learning (not read here) | yes (operators re-route) | tracker with upkeep and lateness | HYPOTHESIS for the dependence; the web's absence is PRIOR ART |
| Self-similar community structure | not tested here | yes (one organization) | not read | not read | scale-free demand, T7 | OPEN |

Empty cells say "not read here". They are not "no".

## 5. Plain answer

The resemblance between the cosmic web and an organization is of the same kind as the resemblance between a spider web and a road map: both are networks of local links in space. The theory says what is shared (link cost with distance) and what is not (a priced delay, which produces hubs, and a tracker that rewires). The sharper negative prediction is that **no feature of the cosmic web's topology depends on a cost the web pays**, because it pays none that the theory counts. Whether that is testable is limited: the web's observed topology is already explained by gravity from the initial field, which is a rival the prediction cannot beat but does not need to.

## 6. Predictions and kill conditions

| Row | Prediction | Label | Kill condition |
|---|---|---|---|
| N39 | The web's topology is fully accounted for by initial conditions plus gravity; GTAO adds nothing. Negative prediction | PRIOR ART (consistent with Bond et al. 1996) | A web feature shown to depend on a tracked quantity (for example one that correlates with a cost paid by the web) rather than on initial conditions and gravity. Not expected |
| N40 | Among tracking networks (organizations, communication systems), hub degree increases with the ratio lateness price / link price; where nothing tracks, no cost-driven hubs | OPEN (HYPOTHESIS) | A preregistered cross-section of at least a stated number of organizational or communication networks in which hub concentration (for example the top-1% degree share) is uncorrelated or negatively correlated with a measured delay-cost to link-cost ratio, with proximity-null and growth-null controls. Must meet MV1 to MV10 before a prereg locks; the mapping from a measured price to λ is not yet defined, and without it the prediction cannot be run |
| (control) | A proximity-only null reproduces the clustering and positive assortativity of any spatial network | DERIVED (simulation) | Not a prediction about the theory; it is a requirement on any test: compare with a proximity null, not with Erdős–Rényi |

## 7. What would change my mind about the verdict

A reanalysis of the cosmic-web networks against a proximity null, with a published hub statistic, that shows heavy-tailed degree in the real web beyond the nearest-neighbour cap, would remove point 3 of the verdict. Longer, thicker redshift surveys could do it. I did not find one.

## References (opened)

- Barabási A-L, Albert R 1999, "Emergence of scaling in random networks," *Science* 286:509, arXiv cond-mat/9910332 [abstract]
- Bond JR, Kofman L, Pogosyan D 1996, "How filaments are woven into the cosmic web," *Nature* 380:603, arXiv astro-ph/9512141 [abstract]
- Coutinho BC, Hong S, Albrecht K, Dey A, Barabási A-L, Torrey P, Vogelsberger M, Hernquist L 2016, "The network behind the cosmic web," arXiv 1604.03236 [full text read; Fig. 4 viewed]. A 2018 related paper (Libeskind et al.) was **not** opened and is not cited.
- Fabrikant A, Koutsoupias E, Papadimitriou CH 2002, "Heuristically optimized trade-offs: a new paradigm for power laws in the internet," ICALP 2002 [full text read for the model and Theorem 1; proofs not checked]
- Guimerà R, Danon L, Díaz-Guilera A, Giralt F, Arenas A 2003, "Self-similar community structure in organisations," arXiv cond-mat/0211498 [abstract]
- Vazza F, Feletti A 2020, "The quantitative comparison between the neuronal network and the cosmic web," *Front Phys* 8:525731, doi 10.3389/fphy.2020.525731 [full text read]
- Watts DJ, Strogatz SH 1998, "Collective dynamics of 'small-world' networks," *Nature* 393:440, doi 10.1038/30918 [full text read, Table 1]
