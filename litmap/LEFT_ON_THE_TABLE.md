# LEFT_ON_THE_TABLE: connections nobody seems to have made, ranked

Sat 2026-11-14 ET. **Every idea here is a hypothesis.** Speculation is labelled. None has been run. "Not found" means not found in this sweep (see `LITMAP.md`), not proven new. Citations are in `LITMAP.md`.

**Ranking.** Score = novelty × testability × payoff, each scored 1–5:
- **Novelty:** how far from anything found.
- **Testability:** free data plus a clean competitor.
- **Payoff:** what it does for the theory if it holds, *or* if it fails.

Preregistration rules for every test are the same as in MATH_ATTACK §5: fix measures before pulling outcomes, hash the plan, name a competitor that predicts differently, and get a blind review.

| # | Idea | N | T | P | Score |
|---|---|---|---|---|---|
| 1 | Power-law forgetting is nested memory tuned to a scale-free world | 4 | 4 | 5 | **80** |
| 2 | A √N law for shared memory: ant trails, languages, wikis | 4 | 4 | 4 | **64** |
| 3 | The temperature is the safety factor: an iso-risk exchange rate (B ∝ σ√τ) plus the fixed-spread sign that reinterprets critical slowing down | 3 | 5 | 4 | **60** |
| 4 | T3a as the condition for a new level: ant trails, Levin's light cone, shared code | 4 | 3 | 4 | **48** |
| 5 | Knowledge depreciation tracks drift, and refresh effort rises then falls (law, medicine, R&D) | 3 | 5 | 3 | **45** |
| 6 | Rosen + Still + lateness: anticipation lead time ≈ the time it takes to act | 3 | 3 | 4 | **36** |
| 7 | The missing lever: reduce the world's drift (niche construction, contracts, homeostasis) instead of tracking it | 3 | 2 | 5 | **30** |
| 8 | Free riders on stigmergy: shared memory goes stale in proportion to users per maintainer | 3 | 3 | 3 | **27** |
| 9 | Lumps and levels: count the levels (K ∝ L^{2/3}, withdrawn in THEORY v1.4; see CLAIM_MAP K12) in body-mass lumps and social layers | 3 | 3 | 3 | **27** |
| 10 | A Landauer ladder: the efficiency gap c_eff/kT at each scale, and a drift barrier for organizations | 3 | 2 | 4 | **24** |

---

## 1. Power-law forgetting is nested memory tuned to a scale-free world (score 80)

**Fields joined, which have not been joined as one claim:**
- Anderson & Schooler 1991: the need probability in the environment is a power law in recency, and so is human retention.
- Fusi, Drew & Abbott 2005; Drew & Abbott 2006; Benna & Fusi 2016: power-law forgetting and adaptation come from a cascade of exponential stores with **geometrically spaced** time constants.
- Shankar & Howard 2013: geometric (log-spaced) memory bins are optimal for power-law-correlated signals.
- Fairhall et al. 2001; Wark et al. 2009: neural adaptation time scales *linearly* with the switching period.
- Huybers & Curry 2006; Vasseur & Yodzis 2004; Inchausti & Halley 2001: environmental variability is a power-law continuum (red/1/f) across scales.
- Candia et al. 2019: biexponential collective forgetting, i.e. two nested stores.
- GTAO T7b: geometric levels iff drift is scale-free.

**The claim** *(hypothesis)*. These are one phenomenon. A self-maintaining system in a world whose drift has no characteristic time builds a geometric ladder of exponential stores (T7b). Seen from outside, that ladder *is* a power-law forgetting curve. The forgetting exponent is set by the environment's spectral exponent. Where the environment has a characteristic time, the curve should bend into an exponential at that time.

**Why it matters now (a problem in BIO1).**
- BIO1 read the neural slope of about 1 (Fairhall, Wark) as fitting "T1's jump-switching form".
- On THEOREMS T1's own formulas, the jump world gives a check rate ≈ √(μWλ/2c), so the interval scales as τ_E^{1/2}. T1b gives memory ∝ √(r/q).
- Lee, Flack & Krakauer 2024 derive the same ½: τ_m\* ∼ τ_E^{1/2}.
- So **slope 1 is not what the single-exponential theory predicts. It is what a scale-invariant (power-law) memory predicts**: with no internal timescale, the adaptation time can only scale with the stimulus timescale.
- If this reading is right, BIO1 P5 supports the scale-free branch (T7), not T1. That needs an independent check.

**Concrete test (free data).**
- **Environment:** for N ≥ 2,000 Wikipedia entities, take the daily news-mention series from GDELT (free). Estimate each entity's spectral exponent β_env over 1 day to 5 years.
- **System:** take the entity's Wikipedia pageviews (Wikimedia REST API, free). Estimate the attention response kernel after exogenous news shocks: the decay exponent α of the pageview impulse response, fit on a held-out period.
- **Prediction (to be fixed before analysis):**
  - α falls monotonically as β_env rises (redder drivers give longer-tailed memory).
  - The functional form comes from the optimal linear predictor of a fractionally integrated process. For example, ARFIMA(0,d,0) predictor weights decay as k^{−1−d}. *[mapping to be derived and checked before preregistration]*
- **Competitors:**
  - (a) a universal kernel independent of the driver (Candia's biexponential with shared parameters);
  - (b) a single exponential matched to the driver's mean correlation time (T1 alone).
- **Second scale, same logic:** Supreme Court precedent citation decay (CourtListener, free) against how fast each area of law drifts (amendment counts for the governing US Code titles, from US Code release points, free).
- **Third scale:** BIO1's neural data are not public, so use published retention exponents and environmental need exponents (Anderson & Schooler's own analyses) as a check that does not need new data.
- **Kill:** α unrelated to β_env (|ρ| < 0.1 with a tight CI) at two scales.

**Payoff.**
- If it holds, it is the cleanest evidence that "memory matches the world" *quantitatively* across scales.
- It ties T7's "fractal iff the world is" to an observable.
- It answers Chad's "same principle at every scale" with a measurable exponent, not an analogy.

## 2. A √N law for shared memory: ant trails, languages, wikis (score 64)

**Fields joined:**
- GTAO T4: the optimal fade of a shared trace rises as √N with N independent depositors.
- Bromham et al. 2015: larger Polynesian populations *gain* basic words faster and smaller ones *lose* words faster.
- Lieberman et al. 2007: irregular-verb half-life ∝ √frequency.
- Pagel et al. 2007: frequent words change more slowly.
- Beekman et al. 2001: trails exist only above about 600 ants.
- Henrich 2004; Kline & Boyd 2010.

**The claim** *(hypothesis)*. Lieberman's √ and T4's √ have the same source: averaging N independent samples cuts error as 1/√N. They appear with **opposite signs in two regimes**:
- **Stable target (drift ≈ 0):** more use means less sampling error, so a form persists longer (Lieberman: half-life ∝ √use).
- **Drifting target:** more independent contributors make it optimal to *turn over faster* (T4: fade ∝ √N), because the pooled estimate can afford to forget old evidence.

**Prediction:** the sign of the usage or population effect on turnover flips with how fast the underlying target drifts.

**Concrete tests (free data).**
- **Languages.** Use the Austronesian Basic Vocabulary Database (ABVD, free) and Bromham's population sizes.
  - Fit log(gain rate) on log(speaker population).
  - **T4 predicts slope ≈ 0.5** in the small-gain regime.
  - **Competitor:** neutral substitution (Kimura 1968, Nature 217:624; a textbook result, not in LITMAP). The fixation rate of neutral variants is independent of N, so slope 0. A per-capita innovation model with no fixation filter predicts slope 1.
  - **Kill:** a CI excluding 0.5 and including 0 or 1.
- **Sign flip.** In Google Books Ngram (free), compare replacement rates of words for drifting referents (technology nouns, for example the names of communication devices) against stable meanings (Swadesh-list items), each against frequency.
  - Prediction: the frequency effect on replacement is negative for stable meanings (Pagel/Lieberman) and attenuated or positive for drifting referents.
- **Wikipedia.** Take statements in articles about fast-drifting topics (live sports rosters, company executives) against stable topics. Track replacement rate against the number of active editors N, at matched topic drift.
  - Prediction: slope ≈ 0.5 in the drifting class, ≈ 0 or negative in the stable class.
- **Wet-lab arm (cheap, not free data).** In *Physarum* or ants with **independent depositors** (T4's required condition), vary group size and source drift, and measure the evaporation or tube-decay rate that maximizes tracking.

**Payoff.** T4 is GTAO's most plausibly original result. Language data could test it within days, with a competitor (neutral theory) that predicts a different exponent.

## 3. The temperature is a safety factor: the iso-risk exchange rate and the fixed-spread sign (score 60)

**Fields joined:**
- Inventory safety stock (SS = zσ√L).
- Galbraith 1974 and Thompson 1967 (slack vs information processing).
- Merton 1974.
- Chevin, Lande & Mace 2010 (critical rate of change).
- Scheffer et al. 2009 (critical slowing down).
- Di Paolo 2005 (distance to the viability boundary).
- Rumyantsev & Netessine 2007 (inventory elasticity to lead time ≈ 0.11–0.13).
- MATH_ATTACK §2 (identity and sign).

**Two claims** *(hypotheses; the first is a design claim and needs selection to be strong)*.
- **(a) Iso-risk design.** Units that hold a target risk choose B ∝ σ√τ. Galbraith's substitution of slack against speed then has a **fixed exchange rate**: halving the time to fix lets you cut the buffer by 1/√2.
  - Rumyantsev & Netessine's elasticity of 0.11–0.13 is far below 0.5. It is the first data point, and it is unfavourable (but it mixes cycle stock with safety stock).
- **(b) The fixed-spread sign reinterprets critical slowing down.**
  - The early-warning literature says a longer recovery time means danger, because at fixed innovation the spread widens.
  - GTAO's identity says that at a **fixed observed spread**, a longer return time means *fewer* boundary crossings (ε_τ = −1).
  - Both are true, and they separate cleanly. Nobody in that literature appears to condition on spread. This is a sharp, model-free sign.

**Concrete tests (free data).**
- **(a) Banks.** FFIEC call reports, 2001–2007, before the outcome period.
  - Regress log(equity/assets − 2%) on log σ_ROA and log τ (capital-recovery time).
  - **Prediction:** coefficients 1 and 0.5.
  - **Competitor:** the regulatory floor plus noise, which predicts a coefficient ≈ 0 on τ.
  - This is a design test. It complements MATH_ATTACK's failure test D1 on the same data.
- **(b) Populations.** GPDD (D3 in MATH_ATTACK).
  - Add the reading that splits critical slowing down: compute the CSD indicator (rising lag-1 autocorrelation) both unconditionally and conditional on spread.
  - **Prediction:** the CSD sign holds unconditionally and reverses at fixed spread.

**Payoff.** It turns the temperature from "Merton relabelled" into a two-sided, falsifiable statement that critical-slowing-down users can check on their own data.

## 4. T3a as the condition for a new level: ants, Levin's light cone, shared code (score 48)

**Fields joined:**
- GTAO T3a (a shared-driver model pays when N > (√(1+ρ)+1)²/ρ).
- Beekman et al. 2001 (trail threshold at about 600 ants, with hysteresis).
- Planqué et al. 2010 (recruitment mode set by colony size).
- Levin 2019 (the cognitive light cone widens when cells integrate).
- Flack 2017 (a level consolidates when estimates converge).
- Maynard Smith & Szathmáry (transitions create shared information).
- Kauffman 1986 (an autocatalytic threshold).

**The claim** *(hypothesis; bold)*. A new level (a shared model, a trail network, a "self" with a wider light cone) should appear when group size crosses N\*(ρ). Here ρ is the ratio of drift that members share to drift that is their own. It predicts **where the transition sits, not just that one exists**: lower N\* when shared drift dominates.

**Concrete tests.**
- **Software (free).**
  - Use GitHub organizations (GH Archive, free) and package release histories (PyPI/npm, free).
  - For each org, take the repositories that share an upstream dependency.
  - ρ = (variance rate of upstream-induced changes) ÷ (variance rate of repo-specific churn), measured on a first block.
  - **Outcome:** whether the org creates a shared internal wrapper or common package for that dependency in a later block.
  - **Prediction:** the adoption hazard rises sharply near N\*(ρ), and it rises *earlier* for high-ρ dependencies.
  - **Competitor:** a fixed size threshold, independent of ρ.
- **Ants (literature-plus-data).**
  - Compile colony size and recruitment mode across species, plus a food-patchiness index as a proxy for ρ (clumped, persistent sources give high shared drift).
  - **Prediction:** the size at which mass recruitment appears falls as patchiness rises.
  - *(The compilation sources were not verified this pass.)*

**Payoff.** It gives "atoms as agents" and Levin's light cone a cost condition, which neither tradition has.

## 5. Knowledge depreciation tracks drift; refresh effort rises then falls (score 45)

**Fields joined:**
- Argote's learning-curve depreciation (Argote & Epple 1990; Darr et al. 1995).
- Landes & Posner 1976 (specific precedents depreciate faster) and Black & Spriggs 2013.
- Li & Hall 2020 (R&D depreciation by industry: computers 36%, pharma 11%, and so on).
- Shojania 2007 (systematic reviews go stale).
- Sørensen & Stuart 2000.
- Lehman 1980.
- Rule 2 and rule 7 (T5: rise, then a cliff).

**The claim** *(hypothesis)*. Across law, medicine and industry:
- the depreciation rate of codified knowledge ∝ (drift of its domain)^{k}, with k fixed by regime (½ diffusive);
- refresh *effort* (update frequency) rises with drift, then collapses to a fallback ("rewrite" or "living review") past a cliff.

**Concrete tests (free data).**
- **Medicine.**
  - Drift = the rate of new RCTs per year in each Cochrane review's topic (PubMed counts by MeSH; free).
  - Refresh = the interval between published versions (Cochrane version DOIs via PubMed/Crossref; free).
  - **Prediction:** the interval falls as drift^{−½} at low to mid drift. In the top drift decile, reviews are either abandoned or converted to living reviews.
  - **Competitor:** Cochrane's own fixed-interval policy (flat).
- **Industry.**
  - Li-Hall depreciation rates against patent-citation obsolescence (PatentsView backward-citation age; free).
  - Industry R&D intensity as refresh effort: an inverted U is predicted.
- **Law.** Precedent citation decay by area (CourtListener, free) against the statutory amendment rate (US Code release points, free).

## 6. Rosen + Still + lateness: anticipation lead ≈ time to act (score 36)

**Fields joined:**
- Rosen 1985 (anticipation).
- Still et al. 2012 (prediction has a thermodynamic floor).
- Sterling 2012 (allostasis).
- Mitchell et al. 2009 and Tagkopoulos et al. 2008 (microbes anticipate and lose it when cues decouple).
- Tjalma et al. 2023 (prediction cost in cells).
- GTAO rule 1 (a late prediction buys nothing).

**The claim** *(hypothesis)*. Anticipation is worth its predictive-memory cost only for the part of the future that falls inside the system's *response latency*. Two consequences:
- **(a)** The optimal anticipation lead time ≈ the time it takes to mount the response. Predicting further ahead pays for I_pred that cannot be used.
- **(b)** When the cue stops predicting, anticipation decays at a rate set by its upkeep (rule 2).

**Rosen has no cost, Still has no lateness, Sterling has no information measure.** Joining them was not found.

**Concrete test (free data).**
- Use circadian transcriptomes (public diel expression atlases for cyanobacteria and plants; *data portals not verified this pass*).
- For genes that peak before dawn, regress anticipation lead (peak time before dawn) on the protein's synthesis and assembly time (from published half-lives and complex sizes).
- **Prediction:** slope ≈ 1.
- **Competitor:** leads clustered at a single phase.
- **Second scale:** firms' order lead times before seasonal demand peaks, against supplier lead time.

## 7. The missing lever: reduce drift instead of tracking it (score 30, high payoff)

**Fields joined:**
- Lee, Flack & Krakauer 2024 (stabilizing niche construction = outsourced memory).
- Thompson 1967 (buffering, smoothing and anticipating the environment).
- Gaia / Daisyworld and Lenton 2018.
- Sagawa & Ueda (feedback thermodynamics).
- Homeostasis.
- Long-term contracts in economics.

**The claim** *(not a test yet; a theory change)*. Every GTAO rule treats drift σ as given. Real adaptive organizations spend heavily on *lowering* σ:
- contracts, regulation, homeostasis;
- routines, calendars;
- trails that make the world predictable.

The objective J should include a control on σ with its own cost. That predicts a substitution: memory spend vs drift-reduction spend, with drift reduction favoured when its benefits are private (Lee 2024).

**One testable form.** Firms facing higher demand volatility shift toward longer customer contracts when they can capture the benefit. Data: the SEC EDGAR full-text search on contract-term disclosures (free) against sales volatility from XBRL frames (free). *(Speculative.)*

## 8. Free riders on stigmergy (score 27)

**The claim** *(hypothesis)*. Shared memory (trails, wikis, open-source docs) is a public good (Lee 2024; Ostrom). Its staleness should rise with users per maintainer.

**Test.** Libraries.io dependents ÷ active maintainers, against documentation staleness (days since the docs last changed after an API change). GitHub, free.

**Payoff.** It directly tests rule 6's "no one in charge" claim, which MATH_ATTACK §3.4 already weakened.

## 9. Lumps and levels: count the levels (score 27; speculative mapping)

**The claim** *(hypothesis)*. If T7b is right and the levels are cost-driven, the number of levels grows as (log-span)^{2/3} *(withdrawn in THEORY v1.4; the current store count is in THEORY §1 N4 and CLAIM_MAP K12)*. Check this against:
- the lumps in Holling's body-mass distributions (count against log mass range across faunas; mammal body-mass compilations such as MOM, *not fetched*);
- the social-layer counts of Zhou-Dunbar and Hamilton.

**Caution.** The mapping from "clocks with a per-level cost" to "body-mass lumps" is loose. LSM trees show that geometric levels also come from pure storage cost, with no drift at all.

## 10. A Landauer ladder and an organizational drift barrier (score 24; speculative)

**The claim** *(hypothesis)*.
- Measure c_eff/kT, the cost per nat actually paid for tracking (O1 in MATH_ATTACK), at each rung. The cell rung is near Landauer (Kempes 2017); then come neurons, computers and firms.
- Borrow Lynch's drift barrier: how close a level gets to its floor should scale with selection strength (effective number of competing units). That predicts firms in more competitive industries pay less per decision-relevant bit. *(Very speculative; the measurement at firm scale is not defined.)*

---

### What I would run first
- **#2 on ABVD.** Days, free, with a competitor exponent from neutral theory.
- **#3(a) on FFIEC** alongside D1.
- **#1 on GDELT + Wikipedia pageviews.** The biggest payoff, and it also fixes the BIO1 reading.

Each needs a preregistration and a blind reviewer before results are believed.
