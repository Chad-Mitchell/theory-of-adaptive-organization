# COLLAPSE1 predictions: memory timescale vs world timescale across substrates

Written Saturday 2026-11-14, ~22:50 ET, BEFORE any per-item numbers for this test were extracted.
Committed and sha256-hashed before extraction (PREDICTIONS.sha256, git log).

## Honesty note (what the author already knows)
- BIO1 already extracted 8 antibody half-lives from Amanna, Carlson & Slifka 2007 (measles 3014 y,
  mumps 542, rubella 114, VZV 50, EBV 11552, vaccinia 92, tetanus 11, diphtheria 19), the
  influenza protection half-lives of Ranjeva 2019 (H3N2 4.1 y, H1N1pdm 6.4 y) and Bedford 2014 drift
  rates. Those are IN-SAMPLE for this test. The immune predictions below are scored only on
  antigens NOT in Amanna 2007 (out-of-sample), with the 8 reported separately.
- Known in outline beforehand: Fairhall 2001 / Wark 2009 (neural adaptation time ~ switching
  period), Kussell & Leibler 2005, EOQ/Baumol-Tobin square-root laws, the general idea that
  "antigen multivalency/replication drives antibody durability" (Slifka & Amanna; Bachmann &
  Zinkernagel). Vague prior belief that firm inventories scale sublinearly with sales.
  No per-antigen half-lives beyond the 8 above, no inventory slopes, and no other collapse-system
  numbers have been looked up for this test.

## The physics, sharpened (what is new in this test)
T1 gives two DIFFERENT scaling classes, and that difference is the theory's content beyond the
"faster world, faster memory" story:
- **Class C (checked/refreshed copy, fixed cost per check, staleness loss):** T* = sqrt(2c/(w sigma^2)).
  With the world timescale tau_e = eps^2/sigma^2 (time to drift one tolerance), T* ∝ tau_e^(1/2)
  at fixed cost ratio. The same 1/2 holds for rare Poisson jumps (check rate ~ sqrt(lambda), THEOREMS
  T1 jump case) and for EOQ (order interval ∝ D^(-1/2)). **Predicted log-log slope 1/2.**
- **Class S (passive memory/switching tuned to a stationary or switching world with correlation
  time tau_c, no per-check cost):** optimal memory or switching time ∝ tau_c (Kussell-Leibler;
  Wiener filter at fixed SNR). **Predicted slope 1.** (Random walk observed through noise, Kalman:
  memory ∝ sqrt(r/q), slope 1/2 in tau_e = r/q; classed C-like.)
- **Class D (deterministic renewal, e.g. a resource that refills at a fixed interval):** optimal
  revisit ≈ renewal interval. **Predicted slope 1.**
- **Class F (frozen: upkeep ≈ 0, e.g. information written into a structure that persists without
  maintenance):** lifetime decouples from world timescale. **Predicted slope 0** (no relation), and
  lifetimes may exceed the holder's horizon (lifespan/generation) by arbitrary factors.
- **Horizon corollary (new reading of freeze-or-hold, hypothesis):** once a memory's lifetime exceeds
  the holder's horizon, further lifetime is invisible to selection/optimization, so values beyond the
  horizon are unconstrained (scatter over decades) while values inside it are tuned.

### Null models
- **N1 (dimensional/proportional):** memory time = k x world time, slope 1 everywhere. Any
  "faster world, faster memory" story with no second scale gives this. Theory differs from N1
  ONLY in class C (slope 1/2) and class F (slope 0).
- **N0 (mechanism-set lifetimes):** memory timescales are set by substrate chemistry/defaults and
  are unrelated to the world timescale: no band, slope ~0 everywhere.
- A pooled cross-substrate plot spanning many decades will look like slope ~1 under N1 and under
  the theory alike (units come from each system's own clock). **The pooled plot is therefore NOT
  diagnostic; within-system slopes by class are.** Stated now so the chart cannot be oversold.

## Predictions and kill criteria

### A. Immune memory (cross-antigen), out-of-sample antigens only
Half-life = the longest-term reported serum antibody half-life (late/plateau phase, data at least
2 y after last dose where available) from a fetched primary source or review table. If a source
gives only early-phase decay, the antigen is excluded. "Horizon" = 50 y.
- **A1 (cue/freeze model, the theory's reading):** the immune system cannot observe a pathogen's
  drift or lethality at encoding; it implements rule 2 through cues correlated over evolutionary time
  with "real, transmissible, will return": replicating agent, or particulate multivalent antigen
  (whole virion, VLP). Predicted class per antigen:
  - LONG (half-life > 50 y): yellow fever 17D (live); HPV L1 VLP; hepatitis A inactivated whole
    virus; hepatitis B HBsAg particle (risky); IPV polio (inactivated virion); rabies inactivated
    virion; Japanese encephalitis inactivated virion; live measles vaccine; natural SARS-CoV-2
    infection (risky); natural influenza infection; dengue natural infection.
  - SHORT (< 50 y): acellular pertussis; Hib conjugate; pneumococcal polysaccharide (PPSV23);
    meningococcal conjugate; inactivated split/subunit influenza vaccine; SARS-CoV-2 mRNA vaccine;
    recombinant zoster (gE subunit); typhoid Vi polysaccharide; anthrax AVA.
  - **SUPPORTS if ≥ 80% of scored antigens (min 8 scored) are classed correctly. KILLS the cue model
    if < 65%.**
- **A2 (drift-only rule 2):** Spearman(half-life, drift rate) ≤ −0.5. **Prediction: fails**
  (|rho| < 0.3, or untestable because drift is ~0 for most antigens).
- **A3 (severity-only rule 2):** Spearman(half-life, untreated case-fatality) ≥ +0.5.
  **Prediction: fails (|rho| < 0.3).** If rho ≥ +0.5, the cue reading is wrong and severity-rule-2
  wins.
- **A4 (horizon scatter, exploratory, small n):** among all antigens with half-life > 50 y, SD of
  log10 half-life ≥ 0.7 (scatter over decades); reported descriptively, no kill.

### B. Cross-substrate collapse
Systems sought (each needs a fetched memory/adaptation timescale AND a fetched world timescale):
retinal/neural adaptation vs stimulus switching (class S); yeast/bacterial switching vs
environment period (S); hummingbird flower revisit vs refill interval (D); scrub-jay/nutcracker
cache memory vs cache perishability/use horizon (S/D); ant pheromone lifetimes vs food-source or
trail persistence (S); influenza protection vs antigenic drift time (S); firm inventory cycles (C);
plus any others found with real numbers (web/DNS caching, citations, language, law).
- **B1 (band):** for held systems (classes C, S, D), log10(tau_m / tau_e) lies in [−2, +0.5] for
  ≥ 80% of points. **Kill if < 60%.** (N0 predicts no band.)
- **B2 (class slopes, the diagnostic):** within-system log-log slopes: class S and D 0.7–1.3;
  class C 0.35–0.65. **Theory beats N1 only if at least one class-C system has slope within
  0.35–0.65 and CI excluding 1. Kill the class distinction if every measured class-C slope has a CI
  containing 1 and excluding 0.5.**
- **B3 (frozen):** class F points show no relation to tau_e (|slope| < 0.3) and can sit far above
  the band.

### C. Firm scale: square-root law in inventories (computed from SEC XBRL frames API)
Data: us-gaap InventoryNet and CostOfGoodsAndServicesSold (or CostOfRevenue), fiscal-year frame
CY2023 (instant CY2023Q4I for inventory), US filers. Positive values only. Industry = 2-digit SIC
from SEC submissions API; industries with ≥ 30 firms.
- **C1:** within-industry OLS slope of log inventory on log COGS: median across industries in
  [0.5, 0.9]. Theory (EOQ cycle + sqrt safety stock) gives 0.5 for a fixed product line; SKU count
  growing with size pushes toward 1. **Kill if median ≥ 0.95 (proportional, N1).**
- **C2 (rule 7, buffer vs shock):** within industry, log(inventory/COGS) rises with log of
  year-to-year COGS volatility (CY2019–CY2023 frames, ≥ 4 years): partial slope > 0 with p < 0.05.
  **Kill if ≤ 0.**

### D. Freeze-or-hold across the dataset
Held points track tau_e (B2); frozen points do not (B3); immune LONG class is the frozen class.
Reported jointly; no separate kill beyond A1/B3.

## What would count as genuinely new
Not "memory tracks drift" (prior art). New would be: (i) the class C vs S slope split confirmed in
data across substrates; (ii) the cue/horizon reading predicting antibody durability out of sample
better than drift or severity; (iii) a firm-scale square-root law tied to the same equation.
Every number must come from a fetched source saved in sources/ with a link; secondhand values are
marked.
