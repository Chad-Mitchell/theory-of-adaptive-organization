# WIKIDATA-BAND preregistration: freeze / hold / lookup on Wikipedia + Wikidata

Status: LOCK FILE. Written before any main-sample outcome was collected or computed. The timestamp of record is the git commit
time of this file on branch `prereg/wikidata-band` of the private repo `Chad-Mitchell/theory-of-adaptive-organization`
(no hand-written time in this file is authoritative). Locked together with: `props.py`, `wm.py`, `collect.py`, `classify.py`,
`analyze.py` (sha256 in `LOCK.txt`), the sampling seed, and the inference method below (per STATE.md "Lock rules").
Nothing is edited on Wikipedia or Wikidata; all access is read-only public APIs with an identifying User-Agent and throttling.

## 0. Theory provenance (required by Ace's HOLD, 8:49 AM)
- **Current THEORY.md** (`<repo>/THEORY.md`, commit 81a1a13):
  - §8, line 267: "5. The closed-form freeze/hold/lookup band, its N² widening for shared stores, and the dissolution order under
    cheap lookup." Listed as one of the theory's own (untested) results. THEORY.md does **not** restate the formulas.
  - §3, line 143 (design rules table): "Freeze-or-hold | Freeze (stop refreshing, keep the copy) when the world barely drifts and
    storage is cheap | PROOF (Theorem G ...)".
- **The formulas come from** `night1/FORMAL/THEOREMS.md` Theorem 8 (lines 280–303), the reviewed formal layer that THEORY.md §8
  cites (math review: core re-derived correct). Setting: class R1 (reset reads), quadratic loss, **one drift rate q** (Brownian),
  i.e. **Regime A** of THEORY.md §2.2 (single timescale). T8.6 gives the power-class generalization.
- **Regime.** Every closed form in T8 assumes Regime A for each item. Wikidata fact types change by occasional replacement
  (a Poisson-type single-rate process per item); whether a fact type's change is single-timescale or scale-free is **not**
  established here. The predictions below are therefore **signs and orderings** (monotonicity in drift and in N), which hold for
  T8 in Regime A and for its Poisson analogue (THEOREMS T8 "carried-over Poisson case", Cho & Garcia-Molina 2003). They do **not**
  test Regime B (power-law need, log-spaced layers; THEORY.md §2.2 lines 85–88), and no Regime-B prediction is made.
- **Possibly-outdated / not in current THEORY.md:** the local-copy vs shared-store edge with N (§2 below) is **DERIVED HERE**
  from T8's cost terms; it is not in THEORY.md or THEOREMS.md. T8.4's literal N² widening is a statement about a shared
  store vs per-use lookup from the source, which this design cannot measure (cost inputs u, c, h unmeasured), so **N² is not tested**.
  MEASUREMENT/FRAMEWORK.md §3.8, §6.6, §7(3) (written 15 Nov, current) supplies the mapping and the fair-kill rule used here.

## 1. Measurement triple (MV1)
- **Target**: the value of Wikidata property P for item Q (a fact), as displayed in the item's Wikipedia article infobox.
- **Pool**: all Wikipedia articles (any language) about Q, which can consume one shared copy (the Wikidata statement). N = number of
  Wikipedia sitelinks of Q.
- **Channels / modes** for each (article, fact) in language edition w (current revision; section 0 = text before the first heading):
  - **LOCAL** (held or frozen local copy): a value of P (current or T0 best-rank value) appears in a named parameter of an
    infobox-like template (≥ 5 named params) in section-0 wikitext (refs/comments stripped). Matching: dates by year; quantities
    by value at the displayed precision (unit conversions km²/ha/mi², m/ft; million/billion words); items by local label, alias
    or sitelink title; strings by substring.
  - **LOOKUP** (consumes the shared store): not LOCAL; the page records Wikidata statement usage of its own item
    (wbc_entity_usage aspect `C.P` or all-statements `C`/`CQR`); and the value appears in the rendered (Parsoid REST) section-0
    infobox/table text (prose paragraphs excluded).
  - **ABSENT**: neither (including local data-template stores, which this design does not measure). **AMBIG**: usage recorded but
    rendered HTML could not be fetched (excluded from primary; counted as LOOKUP in a sensitivity). UNMATCHABLE: no matchable value.
  - Among LOCAL facts whose Wikidata best-rank value changed in the window: **REFRESHED** (a new value in the local params) vs
    **STALE** (only an old value) = hold vs freeze.
- **Drift q_P** (method 1): share of sampled items with P present at both T0 = 2023-11-15 (last revision before T0) and now, whose
  best-rank value set changed (time values compared at the coarser precision; refinements are not changes), converted to a rate
  λ = −ln(1 − (k+0.5)/(n+1)) / Δt (years). Method 2 (convergent, MV5): share of items whose current statements carry a
  day-precision start/end/point-in-time/publication qualifier (P580/P582/P585/P577) inside the window, same conversion.
  Construct caveat (MV2): this is drift of the shared store's value, not of the world.

## 2. Predictions (derived from T8 cost terms; signs only)
Derivation (DERIVED HERE, not reviewed): a local copy held at interval T costs c/T + WqT/2 per page, optimum √(2cWq)
(T8.1–2), or the freeze corner c/H_l + WqH_l/2 when q < q_f = 2c/(WH_l²). Consuming one shared copy held for N pages costs
u + √(2cWq/N) per page (u = per-page integration/policy cost). Shared beats local hold iff q > u²/(2cW(1 − N^{−½})²); freeze beats
shared at q → 0 iff u > c/H_l. Hence, with u, c, W varying across wikis and properties but not systematically with q:
- **KG (MV7 known-groups, must hold for the instrument to count):** (a) P569 date of birth has λ̂ in the 3 lowest of 26 properties
  and its upper 95% bound ≤ 0.02/yr; (b) in each wiki with ≥ 10 displayed P569 facts, LOCAL share of displayed (LOCAL+LOOKUP)
  ≥ 0.5 ("birth dates frozen"). KG PASS iff (a) and (b) in ≥ ⌈2/3⌉ of eligible wikis. KG failure in a wiki = the u > c/H_l regime
  fails there (mode policy/template-driven); reported; primary analyses still use all wikis.
- **P1 (drift gradient, primary).** P(LOOKUP | LOOKUP or LOCAL) rises with log λ̂_P, beyond item-type rivals.
  Model G: logistic, wiki FE + domain FE + z(page-age rank) + z(log λ̂_P) + z(log(1+N)).
  Rival R1: same without log λ̂ and log N (domain = item-type rival). Rival R2: wiki FE + datatype FE + controls (reported).
  PASS: β_q 95% CI > 0 AND leave-one-property-out ΔAUC(G − R1) ≥ 0.02 with 95% CI lower bound > 0.
  FAIL: β_q 95% CI < 0, OR ΔAUC < 0.02 with CI including 0 (FRAMEWORK §6.6 kill). Else INCONCLUSIVE.
- **P2 (N; shared-store benefit rises with consumers).** β_N in model G: PASS if CI > 0; FAIL if CI < 0; else INCONCLUSIVE.
- **P3 (hold vs freeze).** Among LOCAL facts with a distinguishable Wikidata change, P(REFRESHED) rises with log λ̂_P
  (logistic, wiki FE + age + log λ̂). PASS CI > 0; FAIL CI < 0; else INCONCLUSIVE (also if < 5 properties or no variation).
- **P4 (replication across editions; cost vs policy).** Per wiki with ≥ 10 LOOKUP and ≥ 10 LOCAL facts (k eligible), fit G without
  wiki FE. PASS if share of wikis with β_q > 0 ≥ 5/6 and k ≥ 4; FAIL if ≤ 0.5; else INCONCLUSIVE (k < 4 → INCONCLUSIVE).
  Policy enters as the wiki intercepts; the theory predicts the gradient replicates while levels differ.
- Declared sensitivities (no verdicts): P1 β_q excluding money properties (P2139, P2131); KG-passing wikis only; AMBIG counted as
  LOOKUP; properties whose regime is A and split-half-stable, plus properties with negligible drift (λ̂ upper bound ≤ 0.02/yr, regime moot).
  Descriptive: mode counts by drift tercile; per-wiki, per-property lookup shares; KG-c (P348 software version not frozen).

## 2b. Regime first (THEORY.md v1.2 §2.5, lines 125–131; added at Ace's 9:03 AM audit, before lock)
- §2.5 rule (line 130): state the regime first, measured on the same system; a formal-layer constant computed at H = ½ is a
  regime-A prediction. §2.5 line 127: reset-read elasticities a = b = **1/(1+2H)**; √ only at H = ½.
- Per property, from the dated history in current Wikidata statements (qualifiers P580/P585/P577 since 1990; `regime.py`):
  (i) **split-half stationarity**: change events per item 2021–2025 vs 2016–2020 among items with history before 2016; stable iff
  item-bootstrap 95% CI of the ratio includes 1 and 0.5 ≤ ratio ≤ 2. (ii) **error-growth exponent** E[loss(τ)] ∝ τ^{2H}
  (quantities: mean squared log change at lags 1, 2, 4, 8 y; other types: −ln(1 − P(any change within τ)) at 0.5–8 y);
  item-bootstrap CI (B = 500). Regime A iff CI ∋ ½ and width ≤ 0.4; "not A" iff CI excludes ½; else NOT ESTABLISHED.
  Reported: H, b_pred = 1/(1+2H).
- **What depends on the regime here.** P1–P4 are sign/ordering predictions. In T8's power class (THEOREMS T8.6) holding cost
  kW^a q^b + h is increasing in q and the shared-store per-page cost kW^a q^b N^{a−1} falls with N for any a < 1, so the signs hold
  for every H (DERIVED HERE). The closed-form edges (q_f, q_c) and the N² widening are H = ½ (regime A) results and are **not tested**.
- **Status rule.** Where a property's regime is NOT ESTABLISHED, or its rates are not split-half stable, its contribution cannot
  change claim status (it already cannot: Tier 3, §4). The "regime A or moot" sensitivity is reported beside the primary.

## 3. Sample, seed, inference
- 26 properties in `props.py` (domain/datatype labels fixed); wikis en, de, fr, ru, it, ca.
- Main sample: per property, WDQS `bd:sample` of 3000 statements with seed **20261115**, items with ≥ 1 sitelink, shuffled with
  `random.Random("20261115-P")`, the first **40** with an article in ≥ 1 of the 6 wikis, excluding all pilot items.
- Inference: all fits sklearn LogisticRegression(C=10, lbfgs, max_iter=2000), z-scored continuous covariates, one-hot FE.
  Coefficient CIs: property-cluster pairs bootstrap, B = 1000 refits, percentile 95%. ΔAUC: leave-one-property-out out-of-fold
  predictions, property-cluster bootstrap B = 2000. numpy default_rng(20261115).
- Dry run on synthetic truth (`analyze.py --synthetic`): with a true drift effect P1–P4 PASS; with none P1 FAIL, P2/P3 INCONCLUSIVE.

## 4. Gates and expected tier (FRAMEWORK §2.2), declared before data
- MV1 pass (triple named). MV2 partial (drift of the store, not the world; mode is observed design). **MV3 FAIL**: u, c, h, H_l not
  measured, W not measured (pageviews dropped for rate limits); predictions are signs. MV4 pass (within-wiki, across-property and across-N comparisons). MV5 partial
  (two drift methods; one mode instrument). MV6 partial (domain, datatype, wiki, page-age rivals; pageviews dropped). MV7 = KG. MV8 (i) reported from
  bootstrap SEs, (ii) selection resolution not measurable → fail. MV9 partial (git-timestamped lock, not externally timestamped).
- **Therefore the maximum tier is Tier 3** (MV3 fails). Results are logged as weak-tier evidence and cannot change any claim's status
  to FIELD-PASS or FIELD-FAIL. Anti-rescue: the locked verdicts stand as computed; post-lock analyses are labelled POST-LOCK.

## 5. Feasibility pilot (declared)
A pilot of 4 items per property (seed 999; excluded from the main sample) was run before this lock to debug API access and
the value matcher. Rate limits forced: Wikidata old revisions via Special:EntityData?revision; Wikipedia pages via Parsoid REST
HTML (section 0 only); drift method 2 switched from edit-summary counts to dated qualifiers; pageviews control dropped; infobox parameters read from Parsoid data-mw (all because of 429 rate limits).
Pilot outputs inspected: aggregate mode counts and matcher examples only; no property-level gradient was computed.
