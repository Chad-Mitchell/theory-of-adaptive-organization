# Testbeds with open data: ranking (v2.57)

Written Friday 20 November 2026, after the biology route hit a data wall (SN1 0/7 scorable; F2 needs
same-cell noise and adaptation time). Goal: a system where **both** the spend on judgment (sensing, memory,
layers) and the cost of error are priced or measurable from **open** data (no sign-in, no account), and where
the GTAO prediction is not already the main rival's or prior art's.

Scores: D = distinctiveness (does GTAO say something the rival/prior art does not?), A = open-data
availability (no sign-in), R = risk (can it plainly fail?). 1 low to 3 high.

| Rank | Testbed | GTAO-distinctive prediction | Rival / prior art | D | A | R | Main blocker |
|---|---|---|---|---|---|---|---|
| 1 | **(a) Grid frequency-control layers, Continental Europe (German LFC block), GB as replication** | Count by degree (iii, CT21) and interlacing L2: reserve layers sit *between* world modes (a_j < b_j < a_{j+1}), not *at* them; with CE layer times 30 s / 300 s / 750 s the open-loop imbalance must have three separated corners, one in (30, 300) s, one in (300, 750) s, one > 750 s; a self-similar random-walk imbalance would cap it at one layer (L1) | "Set at the world's scale" (θ_j ∈ [τ_j/2, 2τ_j]); engineering history (product times chosen by technology, no relation to the spectrum) | 2 | 2 | 3 | Second-wise German NRV (open-loop proxy) is served only by an ASP.NET form-postback button; ENTSO-E API needs a token (account); netztransparenz API portal needs credentials |
| 2 | (c) Learning rate vs volatility (Behrens 2007; Nassar 2010) | Not the volatility effect (Bayes-optimal prior art). Distinctive only as **store noise** (E1): λτ\* = (1−s)/s with s measured from response variability, and the CT33 stakes result (spend rises with stakes while the number of tracked time scales may fall) | Bayes-optimal hierarchical learner (Behrens 2007); rational inattention (Sims 2003) also predicts stakes effects | 1–2 | 2 (open OSF/Github task data exist for some studies) | 2 | Stakes manipulation plus volatility in the same open dataset not found; s would have to come from trial-to-trial noise, a modeling choice |
| 3 | (d') Central-bank meeting frequency vs inflation volatility (own candidate) | CT12 read-rate rule: optimal read interval T\* ∝ (c/w)^{1/α} σ^{−2/α}, so for a random walk (α = 2) meetings per year ∝ σ (exponent 1 in σ, ½ in variance) | Fixed institutional calendars (8/yr Fed, 8/yr ECB since 2015, 12/yr before); state-dependent pricing (Calvo/menu-cost prior art gives the same √ law: Barro 1972, Dixit 1991) | 1 | 2 | 1 | Calendars barely vary; the √ law is prior art (impulse control) |
| 4 | (b) Inventory and forecasting | Price-free share (α−1 looking per 1 lost to error) generalizes EOQ (Harris 1913) and exponential smoothing (Muth 1960) | EOQ, Muth: the same results | 0–1 | 1 (firm cost data not open) | 1 | Prior art; no open holding- and stockout-cost data |
| 5 | (d) Market microstructure (market-maker quoting layers) | Number of quote-update time scales vs order-flow spectrum | Glosten–Milgrom/Kyle; latency arms-race literature | 1 | 0–1 (tick data paid; LOBSTER needs account) | 2 | Data paid or account-gated |
| 6 | (e) Weather-forecast cycles (own candidate: assimilation 6 h / ensemble 12 h / seasonal) | Interlacing of cycle times with atmospheric spectrum | Engineering history; predictability-limit literature (Lorenz 1969) | 1 | 2 | 1 | Cost of error not priced |

## Why (a) is first, and how it is made non-circular
- **Both sides priced and open:** reserve capacity and energy prices (regelleistung.net tender results,
  open CSV), imbalance prices (reBAP, netztransparenz), activated reserve volumes; GB: NESO data portal
  (DC/DR/DM auction volumes and prices, system inertia and its cost, BSUoS daily costs) and 1-s system
  frequency, all open via CKAN GET (checked: package_search lists `system-frequency-data`, `system-inertia`,
  `system-inertia-cost`, `dynamic-containment-data`).
- **Circularity.** TSOs design products and dimension reserves explicitly (ENTSO-E SOGL, probabilistic
  dimensioning), so "the layers fit the world" could be engineered in. Three defenses: (1) the prediction is
  about the *open-loop* imbalance spectrum, which the product times did not set (it is load, renewables and
  schedule steps); (2) GTAO's interlacing (layers between modes, faster than their mode) differs from what an
  engineer who targets "the" time scale would do (the "set at" rival); (3) out-of-sample across grids: the same
  rule, fixed now, is applied to GB (layers 1 s DC/DM, 10 s DR, minutes BM/Quick Reserve) whose spectrum and
  product times differ.
- **Closed loop.** Frequency and NRV contain the controllers' action. The open-loop imbalance is
  reconstructed as NRV (aFRR + mFRR activations) plus the FCR and self-regulation response implied by
  frequency (droop), with a preregistered sensitivity check (PREREG_GRID1.md).
- **Prior-art caution.** That control-loop bandwidths should be separated (cascade-control rule of thumb,
  ×3–10) is standard engineering; GTAO's added content is the tie of each layer to a world mode by degree and
  the interlacing order.

## Sources (DOIs verified on Crossref, `crossref_grid.out`)
Rydin Gorjão et al. 2020, Nat. Commun., 10.1038/s41467-020-19732-7 · Behrens et al. 2007, Nat. Neurosci.,
10.1038/nn1954 · Nassar et al. 2010, J. Neurosci., 10.1523/JNEUROSCI.0822-10.2010 · Sims 2003, J. Monet.
Econ., 10.1016/S0304-3932(03)00029-1 · Barro 1972, Rev. Econ. Stud., 10.2307/2296440 · Dixit 1991, J. Econ.
Dyn. Control, 10.1016/0165-1889(91)90037-2 · Muth 1960, JASA, 10.1080/01621459.1960.10482064 · Lorenz 1969,
Tellus, 10.3402/tellusa.v21i3.10086 · Harris 1913 (Factory, The Magazine of Management; no DOI).
