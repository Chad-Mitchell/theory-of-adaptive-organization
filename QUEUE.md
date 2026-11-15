# GTAO work queue (live; executable)

Canonical copy. Ace's working folder holds only a pointer to this file. Updated by small PRs to `main`; the git history is the timestamp of every choice.

## How the queue runs (binding)

1. **Read at use.** Before taking an item, read `THEORY.md` (status block, §2.2, §2.5 and the section the item tests) and `STATUS.md`. Do not work from a summary.
2. **Regime first.** Every prereg names the regime (A α = 2 Markov / B scale-free with measured α over a stated band / C many modes with β / not established), measured on the same system, then derives the prediction from `THEORY.md`, quoting the section and the premise checks (THEORY §2.5). Field results are labelled "passed / failed on proxy X". Never "law".
3. **Order by SURPRISE-GUIDED-SEARCH (protocol v2, from ledger entry 6; entries 0–5 are pre-protocol and not scored).** The full protocol is the docstring of `queue/sg_rank.py`. Before each pick:
   a. Commit an `unaided_order` entry covering exactly the items to be ranked, **before** running the rule (same commit, earlier timestamp).
   b. Update `queue/items.json` and run `python3 queue/sg_rank.py log queue/items.json <entry> <unaided_entry>`. It stores the numeric index and P per item, the unaided ranks, the items-file hash, a full uniform permutation (`random.Random(20261115 + entry).shuffle(sorted(ids))`) and γ-sensitivity orders (0.2, 0.8).
   c. Pick cycle: picks 1–2 rule's top; pick 3 unaided top (rule's if the same); pick 4 top of the stored uniform permutation; repeat. Log kind `pick` with `by`.
   d. When an item finishes, log kind `outcome` with `item`, `status_changed` (true/false), `rows` and usage spent.
4. **Iterate.** Every result is read for surprises: a number off its prediction by > 1 SE, a referee flag, a broken premise, a dormant topic reawakening. Each surprise becomes a new item (or raises the LR of an existing one) in `items.json` before the next pick. Items are never deleted; finished ones are marked DONE with paths.
5. **Budget.** Heavy compute at `nice -n 19`, few heavy jobs at once. Continue autonomously up to 90% of weekly usage (Chad, t1914); no check-ins needed, but log everything.
6. **Score SG** with `python3 queue/sg_rank.py score` after ≥ 15 post-protocol outcomes (item Q0). The predictor is each item's first-seen post-protocol score; a pass tests the operational rule (including the judgment factors w, v, L, c), not the bare SG clock, which is scored only on items with non-flat P (n ≥ 8).
7. **Privacy and outside acts.** Repo stays private. No posts, emails or messages. Looper README wording needs Chad's approval; reversible Looper code changes do not.

## Items, in the current rule order (ledger entry 1, 15 Nov 2026 ~08:58 AM ET)

Q0 is always on and sits above the ranking because it is the rule itself (Chad, t1915).

### Q0. SURPRISE-GUIDED-SEARCH (always on)
- **Tests:** THEORY §2.5, Proposition SG (derivation and check: `reviews/night2/AUDIT_DIVERGENCE.md` §6, `reviews/night2/AUDIT_checks/sg_check.py`).
- **Regime:** B assumed for this research environment, modelled as a Lomax hazard (a modelling choice). γ = 0.4 rounds SELF P1b's −0.39, which was INCONCLUSIVE on a statement-time proxy; sensitivity orders at γ = 0.2 and 0.8 are logged with every ranking. Regime not established.
- **Data:** `queue/LEDGER.jsonl`.
- **Locked prediction (protocol v2, scoring starts after ledger entry 6):** the rule's index ranks completed items by "changed a CLAIM_MAP status" with AUC > 0.5 and ≥ the AUC of Ace's unaided rank.
- **Kill / pass, on proxy "claim-status change":** after ≥ 15 completed items, kill if rule AUC ≤ 0.5 or more than 0.1 below Ace's; pass if rule AUC > 0.5 with bootstrap CI excluding 0.5 and ≥ Ace's. Otherwise inconclusive.
- **Also owed:** a hostile referee of Proposition SG (math + prior art), as part of Q1.

### Q1. PRIORART-SWEEP (rule rank 1, I = 3.15) — DONE 15 Nov 09:26 ET (gap-fill only; `reviews/night2/SPECTRUM_MAP/priorart/NOTES.md`)
- **Outcome:** night 1 had already swept the main seeds (`/workspace/gtao/night1/REVIEW/priorart/SWEEP.md`). Added: forward citations of Bimpikis & Markakis 2016 (72) and Abolhassani 2024 (16): no statement of O1 or O5. SG's regime-conditional clock is anticipated in substance by Ferragut, Rodríguez & Paganini 2018 (Queueing Systems 88:207–241): relabel SG's novelty "application". Google Scholar not swept (PRIORART-SCHOLAR). No CLAIM_MAP status applied (referee first).
- **Tests:** THEORY §1 and §8b novelty statements; Proposition SG's prior art.
- **Regime:** n/a.
- **Data:** OpenAlex / Semantic Scholar / Crossref APIs (Google Scholar was blocked): forward citations of Marschak & Radner 1972 ch. 7 §5, Van Zandt & Radner 2001, Veldkamp & Wolfers 2007, Bimpikis & Markakis 2016, Abolhassani 2024; queries for decreasing-hazard / renewal-process monitoring and Whittle-index scheduling with bursty sources.
- **Prediction sketch:** none of the six §8b items is stated in an earlier source; SG's regime-conditional clock is likely found.
- **Kill / pass:** any source stating an item → relabel PRIOR ART in CLAIM_MAP (with the passage read). Not a proxy test.

### Q2. SPECTRUM-MAP-DERIVE (rule rank 2, I = 3.00) — the headline — DONE 15 Nov 09:26 ET, NOT refereed (`reviews/night2/SPECTRUM_MAP/README.md`)
- **Outcome:** passes the letter (predictions the named rivals lack: τ_m ∝ τ_E^{1−1/α} vs LFK's ½; kernel sign flip at α = 2; effort elasticities α/(2α−1), 1/(2α−1) under noisy sensing) but is mostly KNOWN filtering + approximation theory plus a price. Demotion of the headline recommended; minimal THEORY v1.3 pointer applied, §2.2 rewrite queued. D3 explained; locked D3S gap-shuffle PASSED on proxy.
- **Tests:** THEORY §2.2, §2.4 (largest gap), §2.5 "what is missing"; FRAMEWORK §6.10.
- **Regime:** A, B and C, jointly.
- **Data:** none (math), with sympy / numerical checks in `theory/` and a hostile math referee afterwards.
- **Derive:** (i) optimal read-rate exponent under fBm(H) with the optimal linear predictor (not hold-last-value); (ii) the joint optimum of number and spacing of memory stores and read rate for S(f) ∝ f^−α with per-store upkeep and per-read price; (iii) the map α → forgetting exponent, and whether it explains MATCH1 D3's opposite sign.
- **Kill / pass:** pass if it yields a prediction that a named rival (fixed budget share; approximation theory without a price; universal kernel) does not, with a stated discriminating test. If it reduces to "power law follows power law" or approximation theory plus a price, demote the headline in THEORY.md and tell Chad plainly.

### Q3. LEARNSIM (rule rank 3, I = 2.40) — DONE 15 Nov 09:17 ET (referee report merged)
- **Tests:** formal T1.8 (level's class sets the onset exponent), FRAMEWORK §6.1.
- **Regime:** A by design (Brownian), declared.
- **Data:** `tests/LEARNSIM/`; referee `reviews/night2/LEARNSIM_REFEREE.md`.
- **Locked:** PREREG_2 rules (AR/RA arms vs members'-class rival; MV7 known groups; MV8 power).
- **Outcome (in-model only, never field):** T1.8 **NOT PASSED** (RA mixed-arm PASS confirmed and robust; AR INCONCLUSIVE on MV8). C1 locked-rule kill **DOWNGRADED** as fragile. V at onset (class R) locked PASS confirmed. No existing CLAIM_MAP_v2 row changed status.

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

### NEW (15 Nov 09:26 ET, from SPECTRUM_MAP; surprises read per rule 4)
- **SPECTRUM-MAP-REFEREE** — DONE 15 Nov 09:40 AM ET (pick 1, ledger 13/14): `reviews/night2/SPECTRUM_MAP_REFEREE.md`. Items 1–2 confirmed; 3 confirmed/KNOWN but its inference withdrawn; 4 prior art plus a price, α = 2 a knife-edge; 5 correct in-model but valid only at fixed variance and prior art in substance (τ ∝ (N/q)^{1/α}; α = 2 in Mora & Nemenman 2019); 6 lock verified, pass reproduced, explanation wrong (estimator mismatch), D3S non-discriminating vs Cox. CLAIM_MAP v2.2: K12, K13, H19 → MATH-CORRECTED; N10, N11 added. Headline demotion endorsed and strengthened (§7).
- **THEORY-2.2-REWRITE** — DONE 15 Nov ~10:00 AM ET (pick 2, rule slot; ledger 15–18). THEORY.md v1.4: §0 headline demoted per referee §7 (tracking layer = classical filtering + approximation theory + a price, credited; open bet = measured-input optimality at every scale, CLAIM_MAP N13/J6); §2.2 rewritten by regime with premises; K12, K13, H19, N7, N10, N11, G23–G29 applied; new elementary §2.5 result N12 (formal onset exponent α-independent: −1 reset reads, −(1+θ) priced precision; self-checked, not refereed). CLAIM_MAP v2.3. Chad-visible wording.
- **LFK-ALPHA-SPF** (w 3, untested). Locked public-data test of P-LFKα: SPF forecaster gains (Coibion–Gorodnichenko measure) across CPI, unemployment, T-bill, GDP growth vs each variable's τ_E and α (FRED). Regime measured first. Kill: slope CI excludes 1−1/α and includes ½. **Referee (15 Nov): the τ_E form holds only at fixed variance; at fixed q the slope is 0. Lock the normalisation-free form τ_m ∝ (N/q)^{1/α} with q (high-frequency level) and N (forecast-noise proxy) measured per variable, or the test is of a normalisation.**
- **VIX-KERNEL** (w 2, untested). Kernel of implied log-variance on past realized log-variance: tail ≈ τ^{−(1+α/2)} with α measured from realized variance (≈ 1.2 if H ≈ 0.1), positive weights. Public CBOE/FRED VIX and index returns.
- **D3-TWO-EXPONENT-OOS** (w 2, untested). Locked out-of-sample version of D3S on ≥ 20 new repos and Wikipedia: renewal-implied β tracks measured β (Spearman > 0.3), gap-shuffle Δβ median ≤ 0.05. **Referee (15 Nov): as written this cannot discriminate (a pure Cox world gives Δβ ≈ 0.045 at β ≈ 0.2; Cox also gives positive Spearman(β, a)). Replace with D3-DISCRIMINATE.**
- **SPECTRUM-BRIDGE-SIM lock** (Q5 now unblocked): lock predictions from SPECTRUM_MAP (read elasticity 1/α for both estimators; K\* = 1 in OU, rising with log-span otherwise (referee: lock the continuous form, one store iff ψ·0.14(α−2)² ≲ 1, not the α = 2 knife-edge); kernel sign flip at α = 2).
- **PRIORART-LFK-ALPHA** (w 2). Forward citations of LFK 2024 and Afterman et al. 2022 for any statement of τ_m ∝ τ_E^{1−1/α}. **Largely covered by SPECTRUM-MAP-REFEREE §5:** the scaling is published in substance, and α = 2 is in Mora & Nemenman 2019. Remaining: full texts of the 6 LFK citers, Afterman/Kleptsyna citers, PLL/clock-steering loop-bandwidth literature, Scholar.
- **D3-DISCRIMINATE** (w 2, untested; new from referee R6/R7). Design and lock a statistic that separates renewal from Cox event worlds at β ≈ 0.2 (e.g. Δβ/β_orig calibrated on simulated renewal and Cox worlds matched to each repo's gap marginal, or a conditional-intensity test on lagged event counts). Show power on synthetic controls before running real repos.
- **SPECTRUM-MAP-FIXES** (w 1). Apply SPECTRUM_MAP_REFEREE §8 items 1–8 to `reviews/night2/SPECTRUM_MAP/README.md` (as a dated erratum block; locked files untouched).
- **PRIORART-SCHOLAR** (w 1). Google Scholar gap of Q1 (only via a sanctioned route; no sign-in).

### NEW (15 Nov ~10:00 AM ET, from THEORY v1.4; surprises read per rule 4)
- **ONSET-SPECTRUM-FREE-REFEREE** (w 3, c 1). Hostile math + prior-art referee of THEORY §2.5 / CLAIM_MAP N12: the formal onset exponent is −1 for reset reads and −(1+θ) for precision-priced sensing at every α (self-check `reviews/night2/THEORY14_checks/onset_classes.out`). *Why:* a surprise in the rewrite (the spectrum drops out of the formal exponents); it changes what an N2 test measures (technology, not world).
- **AQN-ESTIMATORS** (w 2, c 1.5). Estimators with CIs for α over a stated band, q and N from a noisy series, plus event-world versions; validated on synthetic fBm+noise, Cox and renewal truth before any lock. *Why:* the open bet (N13) needs all four inputs measured on one system; no estimator is validated (§11 process item "dry-runs on synthetic truth").
- **SAME-SYSTEM-AQN** (w 3, c 4; after AQN-ESTIMATORS). First test of N13: on one real system measure α, q, N, stakes and one design quantity (read rate, memory time or store count); lock the §2.2 prediction against fixed-budget-share and universal-½ rivals. Candidates: SPF (with LFK-ALPHA-SPF), VIX (VIX-KERNEL), E. coli (SENSE-CELL). Regime measured first.
- **ONSET-ACROSS-ALPHA-SIM** (w 2, c 3). Non-circular learners (LEARNSIM harness) in fGn worlds at two α values with one technology. Locked prediction from N12: onset exponent unchanged (−1 reset; −2 linear precision price). In-model only.
- **KERNEL-MEASURE** (w 2, c 3). Every earlier memory test measured a need hazard, never a tracking kernel (§2.2). Measure a response kernel on one system with α measured on its driver; predict survival exponent α/2 and the sign flip at α = 2. Overlaps VIX-KERNEL.
- **FROZEN-DOC-POINTERS** (w 1, c 0.5). One-line "superseded by THEORY v1.4 §2.2" pointers in frozen files that still state slope 1 or (log-span)^{2/3} (`litmap/LEFT_ON_THE_TABLE.md`, `theory/THEOREMS.md`); no content edits.
- Note on **SENSE-CELL**: by §2.5 the physics matters through θ, the price exponent of precision; measure θ and the binding ratio together.
- Note on **SPECTRUM-MAP-FIXES**: item 1 ("whatever linear predictor") applied in the v1.4 PR; items 2–8 remain.

**Next pick (3) is the unaided slot:** log a fresh unaided order covering the items to be ranked, run the rule, then take the unaided top (rule's if the same).

## Done (frozen)
- MEASURE-SELF: `reviews/night2/SELF/` (refereed; re-read under THEORY §2.5 in §8c).
- VIGIL_ONA: `prereg/vigil-ona/` (refereed).
- Night-2 referee: `reviews/night2/REFEREE/`.
- Divergence audit: `reviews/night2/AUDIT_DIVERGENCE.md`.
- PRIORART-SWEEP (gap-fill) and SPECTRUM-MAP-DERIVE: `reviews/night2/SPECTRUM_MAP/` (refereed: `reviews/night2/SPECTRUM_MAP_REFEREE.md`).
- SPECTRUM-MAP-REFEREE: `reviews/night2/SPECTRUM_MAP_REFEREE.md` + `reviews/night2/SPECTRUM_MAP_REFEREE_checks/`.
- LEARNSIM: `tests/LEARNSIM/`, referee `reviews/night2/LEARNSIM_REFEREE.md` (T1.8 NOT PASSED; no existing CLAIM_MAP status change; rows G23–G29 added in v2.3).
- THEORY-2.2-REWRITE: `THEORY.md` v1.4, `measurement/CLAIM_MAP_v2.md` v2.3, `reviews/night2/THEORY14_checks/`.
