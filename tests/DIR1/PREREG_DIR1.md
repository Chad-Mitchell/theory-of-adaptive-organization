# DIR1 preregistration: price-free directional predictions, scored on the published record across three classes

*Saturday 21 November 2026, written by a Grok Bot executor for Chad Mitchell on branch `dir1-directional`, beside `main` `2c32ade`. Not reviewed at lock. This file, `PREDICTIONS_DIR1.json`, `search_dir1.py` and `score_dir1.py` are locked by SHA-256 in `PREREG_DIR1.sha256`, committed and pushed **before any outcome retrieval** (the commit time is the record). Nothing below is changed after retrieval; any deviation goes in `DEVIATIONS_DIR1.md` with its time (America/New_York, ET). The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." No locked file elsewhere in the repository is edited.*

## 1. Why this test, and what it can and cannot mean

Every field test so far stopped at one of two gates: qualification (THEORY §3 (a)–(e) needs a cost-to-fitness map σ, a population N_e and a redesign time that public data almost never supply) or absolute prices (*h*, *w* in fitness units; `theory/PRICE_FREE_2026-11-21.md` §1.3, `theory/REVEALED_PRICES_2026-11-21.md` §1). `core/bridge_2026-11-21/SELECTION.md` shows that if fitness cost is linear in J, weak-mutation selection concentrates on argmin J (Sella & Hirsh 2005 applied to J). What is left to ask of nature, before any band, is the weakest empirical consequence: **do real selected systems change their design in the direction argmin J says when one of J's inputs changes?** Those directions do not need prices (PRICE_FREE §1.1, "direction only").

**Honest scope, fixed now.**
- This tests a *directional corollary* of the hypothesis, under a *coarse* qualification tier (§3). It is **not** a test of the banded hypothesis of THEORY §3, and a PASS does not "earn" the hypothesis in the sense of CORE §3. It has the *two classes at different scales* structure of CORE §3 for the directional corollary only.
- PRICE_FREE §2 already says it bluntly: monotone comparative statics are predicted by almost any optimizer of the form S(𝒟) + w·E(𝒟). D1, D2 and D4 do **not** discriminate J from other cost-benefit optimizers; they discriminate only against non-adaptive rivals (no response, constant effort, constant reserve, pure upkeep minimization). D3 has low discrimination against neutral drift. D5 is the one prediction with named rivals of the **opposite** sign.
- The published record is biased toward reported effects. That bias inflates agreement. So **a PASS is weak evidence and a FAIL is strong evidence.** I record my expectation before retrieval: I expect PASS (my probability about 0.8), because the literatures for D2 (vigilance) and D4 (cash, fat) are known in broad outline to favour the predicted signs; D1 at high drift (Lemma B1) and D5 are where I expect misses.

## 2. The predictions (price-free signs derived from J)

Each sign holds for every value of the prices, under the stated conditions. IDs are the repository's (THEORY Appendix B, `theory/PRICE_FREE_2026-11-21.md`, `theory/FREEZE_PROCESS_2026-11-21.md`); no new theorem is claimed here.

| ID | Sign | Source | Conditions | Rivals and what they predict | Discrimination |
|---|---|---|---|---|---|
| **D1** | Faster world drift ⇒ higher read / sample / update / adjustment rate | CT12 (read rate ∝ (w·q/c)^{1/α}, rises with q); CT10; CT41 / CL19 (the inaction band is crossed more often as drift rises) | ruin slack; read price fixed; below the Lemma B1 (G3) collapse edge, where a bounded fallback exists | R0 no response (Calvo-type constant frequency; constant effort): no sign. R3 (design copies the world's time scale): same sign. Any S + wE optimizer: same sign | vs R0 only |
| **D2** | Higher stake of being wrong ⇒ judgment spend (vigilance, monitoring) no lower | CT33 (PF1); CT10 (G4); CT20 (ii) | ruin slack. CT33/PF2: may flip when ruin binds. A study counts as ruin-binding only if it manipulated or documented starvation or energetic stress (decided from methods, not results) | R0 constant effort: no sign. Rmin pure upkeep (energy) minimization: no sign or negative. R3 (no price dependence): no sign. Any S + wE optimizer: same sign | vs R0, Rmin, R3 |
| **D3** | Signal or stake removed (relaxed selection) ⇒ the costly tracking / sensing trait shrinks or is lost | CT4 (the first bit must pay); CT9 / CT11 (hold vs fade); the freeze limit (FREEZE_PROCESS §2, PR #137) | the trait has upkeep (κ or h > 0); enough generations | Rinert (constraint / phylogenetic inertia): no change. Rdrift (neutral mutation accumulation): same sign | **low** (drift predicts the same sign) |
| **D4** | Larger shocks ⇒ larger reserve or buffer | CT25 (buffer ∝ shock × τ^H); CT22 (B_min) | none beyond the model class; binding ruin does not flip this sign | R0 constant reserve: no sign. Rmin pure upkeep minimization: negative or none. Any precautionary optimizer: same sign | vs R0, Rmin |
| **D5** | Faster-changing world ⇒ decisions and information move from shared / central / social to local / individual | CT35 with the OU closed form X_S = ν·π·e^{−2ℓ/τ}·X_L (THEORY App. B.11, line 488; CORE §5) | the shared level adds latency ℓ > 0; equal read quality | Rrigid threat-rigidity (Staw, Sandelands & Dutton 1981): centralize under turbulence, **opposite sign**. Rcopy copy-when-uncertain: more social information under uncertainty, **opposite sign**. R0: no sign | vs opposite-sign rivals |

Dropped as low-value: "the count of layers is capped by the world's degree" (Kalman–Bucy, KNOWN; not scoreable from abstracts); the CT33 ruin-binding flip PF2 (the most distinctive sign, but prior art in Dall & Johnstone 2002 and no systematic field literature of the right form was identified; recorded as the next test, not scored here).

## 3. Coarse qualification tier QC (added tier; decided before any outcome)

THEORY §3 (a)–(e) stays the qualification rule for the banded hypothesis. QC is an **added, lower tier** that qualifies a class only for this directional corollary. It is checked at the **class level, from public facts, now**, before any outcome is seen. A result under QC is labelled "directional, QC-qualified" and never "qualified" in the THEORY §3 sense.

| Item | Rule | C: cells / microbes | A: non-human animals | F: firms / markets |
|---|---|---|---|---|
| QC1 population | many independent units compete in one world | microbial populations ≥ 10⁶ cells (fact of the class) | wild populations (not critically endangered) | ≥ 30 independent firms in the market or sample |
| QC2 time | ≥ 10 generations or redesign cycles in a stable niche | experimental evolution ≥ 100 generations, or natural strains; plastic responses are evolved reaction norms | evolved behaviour / physiology of wild species | the decision recurs at least yearly, over ≥ 10 years of market history with entry and exit |
| QC3 selection on outcome | the design variable affects survival, reproduction or firm survival / profit | growth and competition | predation, starvation, reproduction | profit and survival |
| QC4 no direct designer | the design variable is not set by a designer optimizing the same objective, by law or by mandate | engineered or synthetic strains excluded | domesticated, captive-bred and laboratory-model lines excluded | regulated variables excluded (e.g. bank capital and reserves, regulated prices); audit effort excluded because auditing standards prescribe risk-based effort |
| QC5 exogenous input | the input (drift, stake, shock, relaxation) is set by the experimenter or by the environment, not chosen by the unit | as stated in methods | as stated in methods | as stated in methods |

Anti-rescue: QC is decided before the data. A study is excluded for QC reasons only on design facts (organism, strain origin, regulated variable, who set the input), recorded with the exclusion, never because of its result. Humans as individual lab subjects are outside all three classes (QC2/QC3 fail for lab tasks).

## 4. Inclusion: a systematic search protocol

- **Engine and strings.** OpenAlex `/works`, filter `publication_year:1970-2025,type:article`, sort `relevance_score:desc`, one locked string per cell (11 cells, listed in `PREDICTIONS_DIR1.json`). Run once by `search_dir1.py` after the lock. The raw responses are hashed in `data/POOL_SHA256.json`. Abstracts are fetched in the locked order OpenAlex → Crossref → Europe PMC → Semantic Scholar and kept outside the repository (publisher text); `data/pool_index.csv` lists every screened record.
- **Screening.** For each cell, the first 20 results in rank order are screened; inclusion stops when 10 are included.
- **Include** a record iff all hold: (I1) an empirical primary study (not a review, meta-analysis, theory or simulation-only paper); (I2) its abstract reports the direction, or the absence, of the cell's design response to the cell's input, in a population of the cell's class; (I3) it passes QC (§3) and the D2 ruin-binding exclusion; (I4) it is not the same species or market *and* same dataset as an earlier-ranked included record in the cell (one system per species/market per cell).
- **No abstract available** from any of the four sources ⇒ excluded as "no abstract", recorded. A meta-analysis found in the pool is recorded as context and not counted.

## 5. Coding and scoring

- **Code** each included system from its abstract: **+1** the predicted direction is reported; **−1** the opposite direction; **0** no effect, mixed, or non-monotone (a hump is 0 unless the abstract's main result is a fall, then −1; Lemma B1 is never invoked to rescue). With several measures, the first-stated result for the design variable is coded. Each code records a locator (a short quote of at most about 25 words).
- **DOIs.** Every included DOI is checked on Crossref (title match), recorded in `data/crossref_check.json`.
- **Scoring** (`score_dir1.py`). Per class, k = count(+1), n = all included. Primary: one-sided exact binomial P(X ≥ k | n, ½) (nulls count as non-agreement, which is conservative). Sign test against R0: among nonzero codes, one-sided P(X ≥ count(+1) | n_nonzero, ½). For D5 the same sign test is the test against the opposite-sign rivals.
- **Class verdicts.** A class needs n ≥ 8 to count. It *supports* if p_primary < 0.01 and its agreement rate > 0.60. It *fails* if its rate ≤ 0.60.
- **Kill condition.** The directional version **FAILS** if the pooled agreement rate ≤ 0.60, **or** two or more classes fail. **PASS** if two or more classes support and no FAIL condition holds. Otherwise **INCONCLUSIVE**. Per-prediction rates are reported; a prediction with rate ≤ 0.50 (n ≥ 5) is recorded as a failed prediction even if the overall verdict passes.
- **Coding reliability gate.** The independent reviewer recodes 20 included systems drawn at random (seed 20261121) from the abstracts alone, without seeing my codes. Agreement < 0.80 labels the verdict UNRELIABLE CODING (not PASS or FAIL), whichever way it points.
- **Misses** are diagnosed causally (proxy, input, assumption, or the claim itself) in `RESULTS_DIR1.md`, without changing any locked prediction or rule.

## 6. What a result does to the odds (fixed before data)

- **PASS**: supports that QC-qualified selected systems respond to J's inputs in J's direction, against non-adaptive rivals in at least two classes. It does not separate J from other optimizers (except via D5). Expected effect: a small rise for the weak version; essentially none for the strong or universal versions.
- **FAIL**: the directional corollary is refuted on the published record in the QC tier; because publication bias favours agreement, this would be strong evidence against the weak version.
- **Failed D5 alone**: evidence against the CT35 mapping (fast-local, slow-shared) in the field, and for the opposite-sign rivals.
