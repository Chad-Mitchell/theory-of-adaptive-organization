# GTAO work queue (live; executable)

Canonical copy. Ace's working folder holds only a pointer to this file. Updated by small PRs to `main`; the git history is the timestamp of every choice.

## How the queue runs (binding)

1. **Read at use.** Before taking an item, read `THEORY.md` (status block, §2.2, §2.5 and the section the item tests) and `STATUS.md`. Do not work from a summary.
2. **Regime first.** Every prereg names the regime (A single-pace / B scale-free with measured H or α / C many modes with β / not established), measured on the same system, then derives the prediction from `THEORY.md`, quoting the section and the premise checks (THEORY §2.5). Field results are labelled "passed / failed on proxy X". Never "law".
3. **Order by SURPRISE-GUIDED-SEARCH.** Before each pick:
   a. Write Ace's unaided order of the open items into `queue/LEDGER.jsonl` (kind `unaided_order`) **before** running the rule.
   b. Update `queue/items.json` (w, untested or surprise + age_days, v, L, c; definitions in `queue/sg_rank.py`), run `python3 queue/sg_rank.py queue/items.json`, and log the order (kind `rule_rank`) with a seeded uniform pick (seed 20261115 + entry number).
   c. Take the rule's top item, except that every third pick takes Ace's unaided top item if it differs (so both rankings get outcomes). Log the pick (kind `pick`, with `by`: rule or ace).
   d. When an item finishes, log kind `outcome`: did any `measurement/CLAIM_MAP_v2.md` row change status (yes/no, which rows), usage spent.
4. **Iterate.** Every result is read for surprises: a number off its prediction by > 1 SE, a referee flag, a broken premise, a dormant topic reawakening. Each surprise becomes a new item (or raises the LR of an existing one) in `items.json` before the next pick. Items are never deleted; finished ones are marked DONE with paths.
5. **Budget.** Heavy compute at `nice -n 19`, few heavy jobs at once. Continue autonomously up to 90% of weekly usage (Chad, t1914); no check-ins needed, but log everything.
6. **Score SG** after ≥ 15 completed items (item Q0).
7. **Privacy and outside acts.** Repo stays private. No posts, emails or messages. Looper README wording needs Chad's approval; reversible Looper code changes do not.

## Items, in the current rule order (ledger entry 1, 15 Nov 2026 ~08:58 AM ET)

Q0 is always on and sits above the ranking because it is the rule itself (Chad, t1915).

### Q0. SURPRISE-GUIDED-SEARCH (always on)
- **Tests:** THEORY §2.5, Proposition SG (derivation and check: `reviews/night2/AUDIT_DIVERGENCE.md` §6, `reviews/night2/AUDIT_checks/sg_check.py`).
- **Regime:** B assumed for this research environment (γ = 0.4 from SELF P1b, the only in-environment estimate; regime not established, flagged).
- **Data:** `queue/LEDGER.jsonl`.
- **Locked prediction:** the rule's index ranks completed items by "changed a CLAIM_MAP status" with AUC > 0.5 and ≥ the AUC of Ace's unaided rank.
- **Kill / pass, on proxy "claim-status change":** after ≥ 15 completed items, kill if rule AUC ≤ 0.5 or more than 0.1 below Ace's; pass if rule AUC > 0.5 with bootstrap CI excluding 0.5 and ≥ Ace's. Otherwise inconclusive.
- **Also owed:** a hostile referee of Proposition SG (math + prior art), as part of Q1.

### Q1. PRIORART-SWEEP (rule rank 1, I = 3.15)
- **Tests:** THEORY §1 and §8b novelty statements; Proposition SG's prior art.
- **Regime:** n/a.
- **Data:** OpenAlex / Semantic Scholar / Crossref APIs (Google Scholar was blocked): forward citations of Marschak & Radner 1972 ch. 7 §5, Van Zandt & Radner 2001, Veldkamp & Wolfers 2007, Bimpikis & Markakis 2016, Abolhassani 2024; queries for decreasing-hazard / renewal-process monitoring and Whittle-index scheduling with bursty sources.
- **Prediction sketch:** none of the six §8b items is stated in an earlier source; SG's regime-conditional clock is likely found.
- **Kill / pass:** any source stating an item → relabel PRIOR ART in CLAIM_MAP (with the passage read). Not a proxy test.

### Q2. SPECTRUM-MAP-DERIVE (rule rank 2, I = 3.00) — the headline
- **Tests:** THEORY §2.2, §2.4 (largest gap), §2.5 "what is missing"; FRAMEWORK §6.10.
- **Regime:** A, B and C, jointly.
- **Data:** none (math), with sympy / numerical checks in `theory/` and a hostile math referee afterwards.
- **Derive:** (i) optimal read-rate exponent under fBm(H) with the optimal linear predictor (not hold-last-value); (ii) the joint optimum of number and spacing of memory stores and read rate for S(f) ∝ f^−α with per-store upkeep and per-read price; (iii) the map α → forgetting exponent, and whether it explains MATCH1 D3's opposite sign.
- **Kill / pass:** pass if it yields a prediction that a named rival (fixed budget share; approximation theory without a price; universal kernel) does not, with a stated discriminating test. If it reduces to "power law follows power law" or approximation theory plus a price, demote the headline in THEORY.md and tell Chad plainly.

### Q3. LEARNSIM (rule rank 3, I = 2.40; running)
- **Tests:** formal T1.8 (level's class sets the onset exponent), FRAMEWORK §6.1.
- **Regime:** A by design (Brownian), declared.
- **Data:** designed simulation, `tests/LEARNSIM/` (branch `learnsim-prereg`), output `results_es.jsonl` in Ace's folder.
- **Locked:** PREREG_2 rules (AR/RA arms vs members'-class rival; MV7 known groups; MV8 power).
- **Status label:** in-model only (SIM-PASS / SIM-FAIL), never field.

### Q4. SELF-2 (rule rank 4, I = 0.75)
- **Tests:** THEORY §2.5 (regime first; Proposition SG) and §6 (a shared driver calls for a level).
- **Regime:** to be measured from **source** change times, not statement times.
- **Data:** Looper store and git history; read-only change times from calendar, Gmail and Drive revisions; new Looper instrumentation (reversible code change): `outcomes.jsonl` (used / ignored / late per return), a miss record with mechanism code, a read log.
- **Locked prediction sketch (origin post hoc, declared):** at equal read budget over the 2 weeks after lock, a topic-level surprise trigger (reread every item of a topic when any source or Chad touches it) gives lower stakes-weighted staleness than uniform, √(drift × stakes) and recency schedules.
- **Kill / pass, on proxy "staleness vs source-change time":** kill if the trigger's loss ratio vs uniform has a CI excluding 1 on the high side; pass if below 1 with CI excluding 1. Use the referee's observer-schedule null for any burstiness claim.

### Q5. SPECTRUM-BRIDGE-SIM (rule rank 5, I = 0.68; after Q2)
- **Tests:** THEORY §2.2 regimes A vs B; §2.5 bridge.
- **Regime:** designed: OU (one pace), fBm H ∈ {0.25, 0.5, 0.75}, 1/f superposition over 3 decades.
- **Data:** simulation; learners optimize realized payoff by ES and choose read interval, estimator (hold vs predictor) and number/rates of stores (K ≤ 8); never given the cost function.
- **Locked prediction:** from Q2, before any run.
- **Kill:** learned read exponent does not move with H (slope CI includes 0), or learned store count is not larger in 1/f worlds than in OU worlds. In-model only.

### Q6. GITHUB-UPSTREAM (rule rank 6, I = 0.30; data pull running)
- **Tests:** FRAMEWORK §6.7 (drift matching), §6.3 (vigilance), §6.9.
- **Regime:** gate added before outcomes: `reviews/night2/GITHUB_ADDENDUM_REGIME.md` (Allan-factor Ĥ of the weekly change series).
- **Data:** public GitHub Actions scheduled runs (read-only `gh`).
- **Locked:** PREREG (branch `prereg/github-upstream`) + addendum. Tier-2 ceiling.
- **Kill / pass, on proxy "event-frequency drift; cron read rate":** as PREREG, with the band 1/(1+2Ĥ) ± 0.15 if regime is not A, and no status change if the regime is unestablished.

### Q7. SENSE-CELL (rule rank 7, I = 0.18)
- **Tests:** THEORY §2.3 (Chad's physics position), FRAMEWORK §3.4, §3.11.
- **Regime:** set by designed stimulus statistics (exact).
- **Data:** Keegstra et al. 2017 source data; Lan et al. 2012 energy–speed–accuracy relation (to be fetched and verified).
- **First:** derive one physical-unit bound for E. coli adaptation; then lock the predicted class and binding ratio.
- **Kill / pass:** specified at prereg; proxy named per FRAMEWORK gates.

### Q8. WIKIDATA-BAND (rule rank 8, I = 0.15; pilot only, not locked)
- **Tests:** formal T8 (freeze / hold / lookup band, N widening), FRAMEWORK §6.6.
- **Regime / premise gate (before lock):** per-property split-half change-rate Spearman ≥ 0.3 (stable rate, the premise SELF P3a failed); properties failing it are excluded and counted.
- **Data:** Wikidata statement histories; `wblistentityusage`; ≥ 2 language editions.
- **Kill:** FRAMEWORK §6.6 (closed form no better than item type, ΔAUC < 0.02 with CI including 0).

### Q9. IMMUNE (rule rank 9, I = 0.08)
- **Tests:** formal T8 applied to immune memory (credit Mayer et al. 2016); THEORY §2.2 regime.
- **Step 1:** measure H / regime of antigenic drift per lineage from Bedford et al. 2014 HI data (Dryad doi 10.5061/dryad.rc515).
- **Prediction / kill:** locked only after step 1.

### Q10. ONA-MORE (rule rank 10, I = 0.04)
- Tier 3 by construction; cannot change vigilance's status. Take only if a dataset with tenure, real reporting units and a shared-environment vs own-task question appears (referee fixes, `reviews/night2/REFEREE/REPORT.md` §6).

## Done (frozen)
- MEASURE-SELF: `reviews/night2/SELF/` (refereed; re-read under THEORY §2.5 in §8c).
- VIGIL_ONA: `prereg/vigil-ona/` (refereed).
- Night-2 referee: `reviews/night2/REFEREE/`.
- Divergence audit: `reviews/night2/AUDIT_DIVERGENCE.md`.
