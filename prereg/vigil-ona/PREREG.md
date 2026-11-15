# VIGIL_ONA — preregistration: do higher formal levels source information from outside their unit more than lower levels, beyond status? (public ONA nomination data)

Status: to be LOCKED by sha256 (LOCK.txt) and committed to the private repo branch `prereg/vigil-ona` **before** any
outcome (nomination) statistic is computed. Private. Nothing posted, emailed or made public.
Fair-measure grading: see FAIR_MEASURE.md (written first). **Every dataset here is Tier 3** (small, units are
offices/departments rather than measured reporting units except Krackhardt, no named driver, no flat comparator).
By FAIR_MEASURE §3, results here are logged as consistent / inconsistent / inconclusive and **do not by themselves
change vigilance's claim-map status (OPEN)**.

## 0. What was touched before the lock (disclosure)
- Downloaded (sha256 in data/SHA256SUMS_raw.txt): Krackhardt (1987) high-tech managers (CoMuNeLab GitHub mirror,
  ODbL); Lazega law firm (Snijders' SIENA page `LazegaLawyers.zip`, plus CoMuNeLab mirror); Cross & Parker (2004)
  consulting and manufacturing (Netzschleuder `cross_parker`, distributed by T. Opsahl); Krebs IT department
  (Netzschleuder). Also scanned the Netzschleuder catalog for other organizational networks.
- Tabulated **node attributes only** (level × unit counts) and the Krackhardt **formal reports-to** layer (structure,
  used for pooled N: VP subtree sizes 3, 7, 2, 4; CEO 20). Read file headers/first lines of edge files to learn the
  format. No degree, tie count, density or cross-tab of nominations was computed.
- Already known to me from catalog text/literature before lock (non-directional for these hypotheses): total edge
  counts (Krackhardt advice 190, Lazega advice 892); Lazega's published finding that advice flows toward partners
  and seniors (status rival); Krackhardt's "advice flows to a few central managers" reputation. I have not seen any
  inside/outside-unit-by-rank statistic for any of these data.
- Wrote `ona_analyze.py`; ran it only in `synth`/`dryreal` modes, which replace every nomination with simulated
  ties (known β) on the real node attributes. Dry run recovered β (pooled 0.41 for true 0.5 in one draw; power
  study in power/).
- **Krebs IT department dropped before lock:** the only rank information is "executive" (3 people, whose pool is the
  whole department, so they have no outside-of-pool alters) and the executives' CUSTOMER answers are truncated in
  the source. No within-unit rank variation remains among eligible egos. Thurman office (15 people, formal +
  undirected multiplex only), Kapferer tailor shop (job prestige, not reporting rank), sawmill (undirected,
  thresholded, roles only in labels) and SocioPatterns office (proximity, no rank) were judged unsuitable.

## 1. Theory → measurable quantities
GTAO (claim map E6–E8, corrected): a level that tracks its pool's shared driver g samples g more than a flat member
would: V(N\*) ≥ 1 + (1+ρ)^(−1/2) (in (1, 2) at zero upkeep), growing as N^a (a ≈ ½) above onset; nested members
sample g less. Fractal: each lead's "shared" environment is what its own pool shares.
ONA mapping (structural proxy, FAIR_MEASURE §2.3–2.4):
- **Sampling g** ↔ the ego's information/advice *seeking* nominations to alters **outside the ego's own unit**
  (the unit's shared environment: other departments/offices/practices, higher levels outside the unit).
- **Comparator** ↔ lower-ranked people in the same organization (nested members; Issue 10 means this tests
  direction/specificity only, never the size floor).
- **Pooled N** ↔ subtree size (Krackhardt, measured) or level pyramid proxy (Cross & Parker: people below ÷ people
  at level; consulting's distribution is not a pyramid, so its proxy is weak). Lazega has no pooled N.
Units: Krackhardt = department (CEO excluded as ego: no outside); Lazega = office × practice; consulting and
manufacturing = location (office). Rank among eligible egos scaled to [0, 1] (bottom → top).

## 2. Hypotheses (primary layer = advice/information nominations)
Layers: Krackhardt "go to for advice"; Lazega "basic professional advice"; consulting "turned to for information or
advice" tie = frequency ≥ 3 ("sometimes" or more); manufacturing "provides information you use to accomplish your
work" tie = ≥ 4 on 1–6 (closest to Chad's "important to getting your work done").
- **H1 direction** (Mintzberg also predicts it): rate of outside-unit seeking per available outside alter rises
  with rank. Node Poisson, offset ln(# outside alters), HC1; per-dataset logRR top-vs-bottom; inverse-variance
  pooled. Also **H1-spec**: stacked inside/outside rates, rank × outside interaction (controls generic activity).
- **H2 GTAO-discriminating (beyond status)**: dyadic logit of tie i→j with **ego fixed effects** (absorbs each
  ego's activity), **alter fixed effects** (absorbs alter popularity/status), alter-higher-rank and alter-equal-rank
  indicators (status matching / advice flowing up), outside-unit main effect, and the key term
  **β = ego rank × outside-unit**. Two-way (ego, alter) cluster-robust SE. Pooled by inverse variance.
  GTAO: β > 0. Status rival (advice flows up, peers sought): β ≈ 0 once alter rank and matching are controlled.
- **H3 growth (GTAO-specific)**: elasticity of outside-unit seeking (Poisson, offset ln # outside alters, dataset
  FE) on ln(1 + pooled N), pooled over Krackhardt, consulting, manufacturing. GTAO band 0.3–0.7 in *frequency*;
  binary nominations from a fixed roster attenuate it (breadth, capped), so the instrument expectation is
  0 < ε ≤ 0.7. Secondary: frequency-weighted version (Cross & Parker weights).
- **H4 placebo**: friendship layer (Krackhardt, Lazega) β should be smaller than advice β (descriptive).

## 3. Rivals
- **R-status** (Blau 1955; Lazega & van Duijn 1997): in-degree rises with rank, out-degree falls or is flat; outward
  tilt only via status-matched alters (absorbed in H2). Descriptive check reported.
- **R-generic activity**: higher levels have more ties of every kind → H1 passes but H1-spec/H2 null.
- **R-Mintzberg monitor** (qualitative): predicts H1 direction; no prediction for H2-beyond-status magnitude or H3
  slope. An H1 pass alone is prior art.
- **R-null**: no rank effect.

## 4. Decision rules (on this instrument; Tier 3)
- H1: PASS if pooled logRR CI lower > 0; NOT SUPPORTED if point ≤ 0; INCONSISTENT if CI upper < 0.
- H2: PASS if pooled β CI lower > 0; INCONSISTENT if CI upper < 0; **GTAO-size excluded** if CI upper < 0.5
  (the log-odds target corresponding to V ≈ 1.65, below the ρ ≤ 1 floor of 1.71); otherwise INCONCLUSIVE.
- H3: PASS if CI lower > 0 and point ≤ 0.7; NOT SUPPORTED if CI includes 0 and excludes 0.3; FLAG if > 0.7;
  otherwise INCONCLUSIVE.
- Overall label: **CONSISTENT-GTAO-SPECIFIC** if H2 PASS and H1 PASS; **CONSISTENT-PRIOR-ART-ONLY** if H1 PASS and H2
  not PASS; **INCONSISTENT** if H2 or H1 INCONSISTENT; **NULL** if H2 GTAO-size excluded with point ≤ 0; else
  **INCONCLUSIVE**. Per FAIR_MEASURE, none of these moves vigilance off OPEN by itself; an INCONSISTENT or NULL is
  recorded as evidence against at Tier 3.
- Decision CIs use the inflated SE (§5). Heterogeneity: per-dataset results, Cochran's Q and leave-one-out pooled estimates reported; a pooled pass driven by one dataset is labeled so.
- Secondary (reported, not decisive): other layers (Lazega cowork, consulting "value", manufacturing "awareness",
  union of work layers, any-frequency thresholds, weighted), friendship placebo, status descriptives.

## 5. Power (simulation, `power/`; real node attributes, simulated ties with sender/receiver heterogeneity sd 1,
same-unit +1, alter-higher +0.5, densities 0.2 and 0.4)
300 simulations per cell (power/b*_d*.json; v2_* after the pooling fix):
| true β (H2) | Krackhardt power | Lazega | consulting | manufacturing | pooled |
|---|---|---|---|---|---|
| 0 (type I, one-sided) | 0.08 | 0.05 | 0.05 | 0.05 | 0.06 |
| 0.5 | 0.17–0.19 | 0.86 | 0.27 | 0.27–0.31 | 0.92–0.98 (nominal SE) |
| 0.69 (V ≈ 2) | 0.24 | 0.99 | 0.41 | 0.50 | 0.99 |
| 1.0 | 0.38 | 1.00 | 0.65 | 0.80–0.85 | 0.99 |
Per-dataset SEs: Krackhardt ≈ 0.8 (useless alone, occasional separation), Lazega ≈ 0.16, consulting ≈ 0.44,
manufacturing ≈ 0.35; pooled ≈ 0.13 nominal. Nominal CIs under-cover (pooled 0.88–0.91); after adding a separation
filter (|β| > 5 or SE > 3 → excluded from pooling, reported) the pooled empirical SD is 0.177 vs mean SE 0.133, so
**decision CIs use SE × 1.3** (`lo_dec`, `hi_dec`); nominal CIs are also reported. With inflation, pooled power ≈ 0.8
at β = 0.5 and ≈ 0.97 at β = 0.69. **The pooled test is dominated by Lazega (≈ 2/3 of the weight)**, whose rank
is partner/associate — a pooled pass/fail is reported together with the leave-Lazega-out estimate.
H1 pooled SE in the dry run ≈ 0.10 (MDE ≈ 0.29 log RR at 80%). H3 is not separately powered; with 143 nodes and
dataset FE its SE in the dry run was ≈ 0.05 (nominal; Poisson HC1).

## 6. Known weaknesses (stated before results)
Tier 3 throughout: n = 21/71/46/77; units are offices (consulting, manufacturing) or office × practice (Lazega), not
reporting units; partners/managers may lead cross-office practices; nominations measure breadth, not frequency;
cross-sectional (selection: people who source widely may be promoted); 1980s–2000s data; no named driver; no flat
comparator; Lazega's "rank" is partner vs associate in a partnership, not a span hierarchy. Same analyst wrote the
prereg and runs it (no blind analyst available tonight).
