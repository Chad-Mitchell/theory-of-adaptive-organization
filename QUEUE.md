# GTAO work queue (live; executable)

Canonical copy. Ace's working folder holds only a pointer to this file. Updated by small PRs to `main`; the git history is the timestamp of every choice.

## How the queue runs (binding)

1. **Read at use.** Before taking an item, read `THEORY.md` (status block, §2.2, §2.5 and the section the item tests) and `STATUS.md`. Do not work from a summary.
2. **Regime first.** Every prereg names the regime (A α = 2 Markov / B scale-free with measured α over a stated band / C many modes with β / not established), measured on the same system, then derives the prediction from `THEORY.md`, quoting the section and the premise checks (THEORY §2.5). Field results are labelled "passed / failed on proxy X". Never "law". Before lock, every prereg meets the feasibility / power gate `measurement/FRAMEWORK.md` MV10 (run `tools/power_gate.py` or simulate the locked decision code on the planned data; paste the output in the prereg): PASS and FAIL each reachable with a stated probability, each firing at its own best-case data.
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

### Q6. GITHUB-UPSTREAM (rule rank 6, I = 0.30) — DONE 15 Nov ~11:21 AM ET (started pre-protocol, out of cycle, unscored; ledger 36; `night2/GITHUB/RESULTS.md`)
- **Tests:** FRAMEWORK §6.7 (drift matching), §6.3 (vigilance), §6.9.
- **Regime:** gate added before outcomes: `reviews/night2/GITHUB_ADDENDUM_REGIME.md` (Allan-factor Ĥ of the weekly change series).
- **Data:** public GitHub Actions scheduled runs (read-only `gh`).
- **Locked:** PREREG (branch `prereg/github-upstream`) + addendum. Tier-2 ceiling.
- **Kill / pass, on proxy "event-frequency drift; cron read rate":** as PREREG, with the band 1/(1+2Ĥ) ± 0.15 if regime is not A, and no status change if the regime is unestablished.
- **Result (as locked):** P1 b̂ = −0.06 [−0.24, 0.17] and P2 â = −0.10 [−0.17, −0.04]: KILL-CONDITION under the original band, the addendum's P1-R band ("Regime B" by ΔAIC 115; weak, mixture confound) and main's Allan band (Ĥ 0.61 [0.57, 0.66] → [0.30, 0.60]; implemented post-outcome). **Failed on proxy "weekly CI-state change rate vs nominal cron reads/week"**, Tier 3 logged only (MV5, MV7(i), MV8(ii) failed: q does not track upstream drift; pinned ≈ unpinned). P3 consistent but non-discriminating; P5/P6 not analysed (5 levels, 0 with comparators): vigilance OPEN. CLAIM_MAP N14–N15. Interpretation: binary CI state = switching world; for exact reset reads the √ rule still applies at qT ≪ 1 (DERIVED HERE, unreviewed; Conti & Mora's ln τ concerns noisy-sensing memory time), so the failure is the drift instrument's. Predictions were locked under THEORY v1.1/v1.2.

### Q7. SENSE-CELL (rule rank 7, I = 0.18)
- **Tests:** THEORY §2.3 (Chad's physics position), FRAMEWORK §3.4, §3.11.
- **Regime:** set by designed stimulus statistics (exact).
- **Data:** Keegstra et al. 2017 source data; Lan et al. 2012 energy–speed–accuracy relation (to be fetched and verified).
- **First:** derive one physical-unit bound for E. coli adaptation; then lock the predicted class and binding ratio.
- **Kill / pass:** specified at prereg; proxy named per FRAMEWORK gates.

### Q8. WIKIDATA-BAND (rule rank 8, I = 0.15) — DONE 15 Nov ~1:55 PM ET (locked `7cffd93` + addendum `28a0f21`; out of cycle, unscored; ledger 65; `prereg/WIKIDATA-BAND/RESULTS.md`)
- **Tests:** formal T8 (freeze / hold / lookup band, N widening), FRAMEWORK §6.6.
- **Regime / premise gate (before lock):** per-property split-half change-rate Spearman ≥ 0.3 (stable rate, the premise SELF P3a failed); properties failing it are excluded and counted.
- **Data:** Wikidata statement histories; `wblistentityusage`; ≥ 2 language editions.
- **Kill:** FRAMEWORK §6.6 (closed form no better than item type, ΔAUC < 0.02 with CI including 0).

### Q9. IMMUNE (rule rank 9, I = 0.08)
- **Tests:** formal T8 applied to immune memory (credit Mayer et al. 2016); THEORY §2.2 regime.
- **Step 1:** measure H / regime of antigenic drift per lineage from Bedford et al. 2014 HI data (Dryad doi 10.5061/dryad.rc515).
- **Prediction / kill:** locked only after step 1.

### Q10. ONA-MORE (rule rank 10, I = 0.04) — DONE 15 Nov ~4:00 PM ET (pick 16, uniform slot; ledger 79–82): **gate not met** (`reviews/night2/ONA_MORE_GATE.md`)
- Tier 3 by construction; cannot change vigilance's status. Take only if a dataset with tenure, real reporting units and a shared-environment vs own-task question appears (referee fixes, `reviews/night2/REFEREE/REPORT.md` §6).

### NEW (15 Nov 09:26 ET, from SPECTRUM_MAP; surprises read per rule 4)
- **SPECTRUM-MAP-REFEREE** — DONE 15 Nov 09:40 AM ET (pick 1, ledger 13/14): `reviews/night2/SPECTRUM_MAP_REFEREE.md`. Items 1–2 confirmed; 3 confirmed/KNOWN but its inference withdrawn; 4 prior art plus a price, α = 2 a knife-edge; 5 correct in-model but valid only at fixed variance and prior art in substance (τ ∝ (N/q)^{1/α}; α = 2 in Mora & Nemenman 2019); 6 lock verified, pass reproduced, explanation wrong (estimator mismatch), D3S non-discriminating vs Cox. CLAIM_MAP v2.2: K12, K13, H19 → MATH-CORRECTED; N10, N11 added. Headline demotion endorsed and strengthened (§7).
- **THEORY-2.2-REWRITE** — DONE 15 Nov ~10:00 AM ET (pick 2, rule slot; ledger 15–18). THEORY.md v1.4: §0 headline demoted per referee §7 (tracking layer = classical filtering + approximation theory + a price, credited; open bet = measured-input optimality at every scale, CLAIM_MAP N13/J6); §2.2 rewritten by regime with premises; K12, K13, H19, N7, N10, N11, G23–G29 applied; new elementary §2.5 result N12 (formal onset exponent α-independent: −1 reset reads, −(1+θ) priced precision; self-checked, not refereed). CLAIM_MAP v2.3. Chad-visible wording.
- **LFK-ALPHA-SPF** — DONE 15 Nov ~10:20 ET (manual unscored pick; ledger 10, outcome 19; `tests/LFK_SPF/RESULTS.md`). Redesigned before lock (commit b2a17f7) per the referee: tests N13 with N11 τ ∝ (N/q)^{1/α}, q from each variable's spectrum, N from SPF dispersion; τ_E slope kept as secondary S1. **Primary INCONCLUSIVE** (n = 6 after gates; MV8 failed in the pre-lock dry run; Tier 3); no CLAIM_MAP change. Post hoc surprise: UNEMP, HOUSING, TBILL CG coefficients within 0–25% of the optimal-filter prediction, α = 2 rival 2–10× high (n = 3, not evidence).
- **SPF-AQN-POWERED** (w 3, from LFK-ALPHA-SPF S-a). Powered N13 test on forecasters: monthly series for α near the crossover, more surveys (ECB SPF, Livingston) or individual panels; power dry run first (MV8).
- **SPF-NOISE-PROXY** (w 2, from S-b). Long yields: β̂ ≈ 0 vs predicted 2.8; dispersion is not signal noise for market-priced variables. Need an independent N proxy before any SPF N13 test.
- **LAB-AKLMT-TAU** (w 2). Afrouzi et al. 2023 lab forecasts of AR(1) series with set persistence (replication data doi 10.7910/dvn/3q6bhc): known DGP, test the fixed-variance τ_E slope (N11 at α = 2) and memory vs optimum.
- **VIX-KERNEL** (w 2, untested). Kernel of implied log-variance on past realized log-variance: tail ≈ τ^{−(1+α/2)} with α measured from realized variance (≈ 1.2 if H ≈ 0.1), positive weights. Public CBOE/FRED VIX and index returns.
- **D3-TWO-EXPONENT-OOS** (w 2, untested). Locked out-of-sample version of D3S on ≥ 20 new repos and Wikipedia: renewal-implied β tracks measured β (Spearman > 0.3), gap-shuffle Δβ median ≤ 0.05. **Referee (15 Nov): as written this cannot discriminate (a pure Cox world gives Δβ ≈ 0.045 at β ≈ 0.2; Cox also gives positive Spearman(β, a)). Replace with D3-DISCRIMINATE.**
- **SPECTRUM-BRIDGE-SIM lock** (Q5 now unblocked): lock predictions from SPECTRUM_MAP (read elasticity 1/α for both estimators; K\* = 1 in OU, rising with log-span otherwise (referee: lock the continuous form, one store iff ψ·c(α−2)² ≲ 1, not the α = 2 knife-edge; pick 26: c is model- and span-dependent, not 0.14; pick 27 / THEORY v1.4.8: 0.005–0.11 in the c3 model by span, ≈ 0.18 with no free short-lag memory, so the lock computes c for its own store model, `reviews/night2/STORE_COEF_REVIEW.md`); kernel sign flip at α = 2).
- **PRIORART-LFK-ALPHA** (w 2). Forward citations of LFK 2024 and Afterman et al. 2022 for any statement of τ_m ∝ τ_E^{1−1/α}. **Largely covered by SPECTRUM-MAP-REFEREE §5:** the scaling is published in substance, and α = 2 is in Mora & Nemenman 2019. Remaining: full texts of the 6 LFK citers, Afterman/Kleptsyna citers, PLL/clock-steering loop-bandwidth literature, Scholar.
- **D3-DISCRIMINATE** (w 2, untested; new from referee R6/R7). Design and lock a statistic that separates renewal from Cox event worlds at β ≈ 0.2 (e.g. Δβ/β_orig calibrated on simulated renewal and Cox worlds matched to each repo's gap marginal, or a conditional-intensity test on lagged event counts). Show power on synthetic controls before running real repos.
- ~~**SPECTRUM-MAP-FIXES**~~ (w 1) — DONE 15 Nov ~5:45 PM ET (pick 26, RULE slot: top of entry 121, I = 1.8; Ace's unaided rank 22 of 46; ledger 120 unaided order, 121 rule_rank, 122 claim, 123 outcome). Items 2–8 applied as dated errata in `reviews/night2/SPECTRUM_MAP/README.md`; own checks A–D; the referee's one-store constant 0.14 is an unpolished-fit artifact (c ≈ 0.03–0.11 in-model; the two-store claim at |α−2| = 0.05, ψ ≈ 10⁴ survives); `checks/d3s_shuffle_repro.py` bit-reproducible, S1 PASS reproduces. THEORY N4 / §2.2 store-row numeric: separate PR #51, DO NOT MERGE without separate reviewer PASS (`reviews/night2/SPECTRUM_MAP_FIXES.md`).
- ~~**STORE-COEF-REVIEW**~~ — DONE 15 Nov ~5:50 PM ET (pick 27, unaided slot; ledger 125–126, 128 + outcome): **PASS-WITH-FIXES**, PR #51 merged, THEORY v1.4.8 (`reviews/night2/STORE_COEF_REVIEW.md`). Own code reproduced every author number. Rulings: no universal constant in THEORY; it states the (α−2)² scaling, names c as set by span and store model (exact no-free-memory value π²/32 − 1/8 ≈ 0.18; four-tap model 0.005–0.11 by span), requires a prereg to compute its own c, and gives the two-store threshold by model and span. No locked prereg moves.
- **PRIORART-SCHOLAR** (w 1). Google Scholar gap of Q1 (only via a sanctioned route; no sign-in).

### NEW (15 Nov ~10:00 AM ET, from THEORY v1.4; surprises read per rule 4)
- **ONSET-SPECTRUM-FREE-REFEREE** — DONE 15 Nov ~10:30 AM ET (pick 3, unaided slot = rule top; ledger 22–25): `reviews/night2/N12_REFEREE.md`. **CORRECTED (narrowed).** Onset exponent −1 (exact reset reads; also entropy pricing) and −(1+θ) (priced precision) confirmed at every α > 1 (wider than 1 < α < 3); the reason is degree-1 homogeneity of linear MMSE. Corrections: C1 noisy reads → −2 at small ρ with α-dependent crossover; C2 same-α premise (priced precision needs α_g − α_u < 1); C3 vigilance ρ^{−θ} only in spend units (ρ^{−1} in precision); C4 vigilance growth N^a, mixed e_u and constants depend on α (confirms V14_REVIEW). Novelty low (elementary corollary; not found stated). THEORY §2.5 / CLAIM_MAP N12 edits in a separate PR, **not merged** (v1.4.1 worker owns THEORY).
- ~~**ONSET-NOISY-READS**~~ (w 2, c 1; from N12 C1) — DONE 15 Nov ~6:20 PM ET (pick 29, RULE slot: top of entry 135, I = 1.6, tied with STAKES-REFEREE and taken by sg_rank's id-order tie-break; Ace's unaided rank 23 of 46; ledger 134 unaided order, 135 rule_rank, 136 claim, 138 outcome). In-model, own code (`reviews/night2/ONSET_NOISY_READS/REPORT.md`): at small ρ the onset collapses to N\*ρ = X_α(σ²/ρ); a noise-limited level is the θ = 1 class (−2 at every α); closed crossover ρ_c = σ² C_α α^{−α/(α−1)} (≈ 2.7, 4.8, 8.4 σ² at α = 1.5, 2, 2.5; 27√2/8 σ² at α = 2); N12 referee c3 slopes reproduced (−1.28/−1.40/−1.58). Derived with one assumed analytic input (dense-sampling asymptote g_α, checked numerically). N2 classification: an intermediate slope does not identify θ; curvature, z_L or the σ²/ρ collapse does. THEORY v1.4.11 / CLAIM_MAP v2.29 in author-only PR #60, **not merged** (DO NOT MERGE without separate reviewer PASS). No status change; no locked prereg moves.
- **MIXED-ALPHA-ONSET** (w 2, c 1; from N12 C2). Prove the α_g − α_u < 1 condition and the Δ > 1 exponent −(1/Δ − b_g)/(1 − a_g).
- ~~**EFFORT-UNITS-ERRATUM**~~ (w 1, c 0.5; from N12 C3) — DONE 15 Nov ~5:25 PM ET (pick 25, RULE slot: top of entry 117, I = 1.8, tied with SPECTRUM-MAP-FIXES and taken by sg_rank's id-order tie-break; Ace's unaided rank 24 of 47; ledger 116 unaided order, 117 rule_rank, 118 claim, 119 outcome). C3 confirmed with own code; dated errata in formal THEOREMS L1(viii) and T5 Definition, FIXES G1; CLAIM_MAP v2.23 unit qualifiers (A5, E9, E10), no status change; THEORY.md already unit-correct, not edited; no locked prereg moves (`reviews/night2/EFFORT_UNITS_ERRATUM.md`).
- **AQN-ESTIMATORS** (w 2, c 1.5). Estimators with CIs for α over a stated band, q and N from a noisy series, plus event-world versions; validated on synthetic fBm+noise, Cox and renewal truth before any lock. *Why:* the open bet (N13) needs all four inputs measured on one system; no estimator is validated (§11 process item "dry-runs on synthetic truth").
- **SAME-SYSTEM-AQN** (w 3, c 4; after AQN-ESTIMATORS). First test of N13: on one real system measure α, q, N, stakes and one design quantity (read rate, memory time or store count); lock the §2.2 prediction against fixed-budget-share and universal-½ rivals. Candidates: SPF (with LFK-ALPHA-SPF), VIX (VIX-KERNEL), E. coli (SENSE-CELL). Regime measured first.
- **ONSET-ACROSS-ALPHA-SIM** (w 2, c 3). Non-circular learners (LEARNSIM harness) in fGn worlds at two α values with one technology. Locked prediction from N12: onset exponent unchanged (−1 reset; −2 linear precision price). In-model only.
- ~~**KERNEL-MEASURE**~~ (w 2, c 3) — DONE 15 Nov ~6:10 PM ET (pick 28; see NEW section from KERNEL-MEASURE). Every earlier memory test measured a need hazard, never a tracking kernel (§2.2). Measure a response kernel on one system with α measured on its driver; predict survival exponent α/2 and the sign flip at α = 2. Overlaps VIX-KERNEL.
- **FROZEN-DOC-POINTERS** (w 1, c 0.5). One-line "superseded by THEORY v1.4 §2.2" pointers in frozen files that still state slope 1 or (log-span)^{2/3} (`litmap/LEFT_ON_THE_TABLE.md`, `theory/THEOREMS.md`); no content edits.
- Note on **SENSE-CELL**: by §2.5 the physics matters through θ, the price exponent of precision; measure θ and the binding ratio together.
- Note on **SPECTRUM-MAP-FIXES**: item 1 ("whatever linear predictor") applied in the v1.4 PR; items 2–8 applied in pick 26.

**Pick 3 taken (ledger 24). Next pick (4) is the uniform slot: top of entry 23's stored uniform permutation (SAME-SYSTEM-AQN), or log a fresh ranking first.** Old note: log a fresh unaided order covering the items to be ranked, run the rule, then take the unaided top (rule's if the same).

### NEW (15 Nov ~11:05 AM ET, from SPF-NOISE-PROXY; surprises read per rule 4)
- **SPF-NOISE-PROXY** — DONE (pick 4, uniform slot; ledger 26–28, outcome 31): `tests/SPF_NOISE_PROXY/RESULTS.md`, lock `2f96b41`. Validated N proxy L0w (within-forecaster nowcast dispersion over the environment-implied variance; passed on synthetic truth). LFK's h = 3 dispersion-as-N **failed on proxy "horizon overidentification"** for 6 of 7 variables; contamination broad (T2 inconclusive); L0w passed known-groups marginally (T3). Post hoc: LFK S-a was an artifact; with measured noise the optimal filter under-predicts consensus CG 2.5–6×. No CLAIM_MAP change.
- ~~**SPF-RIGIDITY-OOS**~~ — DONE 15 Nov ~5:15 PM ET (pick 20): **MV10 gate not met**; no prereg locked, no outcome (`tests/SPF_RIGIDITY_OOS/RESULTS.md`). Follow-on: SPF-RIGIDITY-LIVINGSTON.
- ~~**NOISE-PROXY-REFEREE**~~ — DONE 15 Nov ~5:20 PM ET (pick 22): PASS-WITH-FIXES (`reviews/night2/NOISE_PROXY_REFEREE.md`).
- **SPF-NOTE-EDITS** (w 1, c 0.5). Proposed THEORY §2.4/§8c and FRAMEWORK §3 notes from SPF-NOISE-PROXY; independent review before merge.
- Note on **SPF-AQN-POWERED**: its S-a rationale is withdrawn (surprise → none); any powered version uses L0w and the horizon check.

**Pick 4 done (ledger 31).**

### NEW (15 Nov ~11:20 AM ET, from PRIORART-LFK-ALPHA; surprises read per rule 4)
- **PRIORART-LFK-ALPHA** — DONE (pick 5, rule slot; ledger 32–35): `reviews/night2/PRIORART_LFK_ALPHA/REPORT.md`, lock `44e1963`. N11 PRIOR ART (in substance) → **PRIOR ART (stated in mapped form)**: Bialek, Callan & Strong 1996 state the smoothing scale ξ ∼ (ℓ^{2α_B−D}/NQ)^{1/2α_B}, i.e. (N/q)^{1/α} and ℓ^{1−1/α} with α = 2α_B. Afterman 2022 / Kleptsyna 2020 state only the error rate. Surprise: Bayes-optimal adaptation to a switching world scales ∝ ln τ, not √τ (Conti & Mora 2022; reproduced in-model). THEORY edits E1–E3 proposed, not applied.
- **TELEGRAPH-LINEAR-PREMISE** (w 3, c 1.5). The spectrum sets memory-time exponents only for Gaussian worlds or linear trackers; derive event-world exponents under the Bayes optimum; audit event-world tests.
- **PRIORART-CREDIT-EDITS** (w 1, c 0.5). Apply E1/E3 credit edits after independent review.
- **PRIORART-ENGINEERING-READ** (w 1, c 1). Banerjee PLL bandwidth, a clock-steering primary, Tsybakov; unread citers.

**Pick 5 done (ledger 35). Next pick (6) is the rule slot again (cycle rule, rule, unaided, uniform restarts at pick 5): rule's top among open non-active items (log a fresh unaided order first).**

### NEW (15 Nov ~11:30 AM ET, from TELEGRAPH-LINEAR-PREMISE; surprises read per rule 4)
- **TELEGRAPH-LINEAR-PREMISE** — DONE (pick 6, rule slot; ledger 37–40): `reviews/night2/TELEGRAPH_LINEAR_PREMISE/REPORT.md`, lock `4d55366`. All locked rules met (in-model, regime A, two-state jump world). Bayes-optimal adaptation after a switch ≈ (N/2μ²) ln(2μ²/λN) (single log; 0.508θ per e-fold), error ≈ 2λN ln(2μ²/λN) (elasticity 0.85–0.92 in λ and N vs linear ½); q alone does not set them. Unaffected: exact reset reads (agrees with GITHUB-UPSTREAM's interpretation note), projection kernels. **Surprise (strong):** Conti & Mora 2022's ln² (eq. 36) is reproduced only by their eq. (20) read as Itô, which omits a drift term; the exact filter gives one log. CLAIM_MAP N16 (v2.8). THEORY edits E2′, E4–E6 proposed, not applied. Audit: AQN-ESTIMATORS and SAME-SYSTEM-AQN NEEDS-PREMISE; GITHUB-UPSTREAM measurement note (count-process Ĥ vs target variogram).
- **TELEGRAPH-REFEREE** (w 3, c 1). Hostile referee of the above incl. the C&M diagnosis and a Wonham-asymptotics literature search.
- **TLP-EDITS-REVIEW** (w 2, c 0.5). Independent review, then apply E2′, E4–E6 (supersedes E2).
- **JUMP-WORLD-ONSET** (w 2, c 2). N12 pooling onset for Bayes trackers of additive jump drifts (sketch: −1 if ρ is a rate ratio).
- **JUMP-STORES** (w 2, c 3). Bayes "store count" = sufficient-statistic dimension; multi-state and 1/f-superposition jump worlds.
- **GITHUB-VARIOGRAM-CHECK** (w 1, c 1). Post-lock descriptive: variogram exponent of the binary target vs the addendum's Allan-factor Ĥ (interpretive only; GITHUB-UPSTREAM is Tier 3).
- **CM-PUBLISHED-CHECK** (w 1, c 0.5). Read the published PRE text of Conti & Mora for corrections (no paywall sign-in, no author contact).

**Pick 6 done (ledger 40). Next pick (7) is the unaided slot: Ace's unaided top (rule's if the same), after a fresh unaided order and rule run. Next free ledger entry: 41.**

### NEW (15 Nov ~11:48 AM ET, from TELEGRAPH-REFEREE; surprises read per rule 4)
- **TELEGRAPH-REFEREE** — DONE (pick 7, unaided slot = rule top, I = 3.6; ledger 41–44): `reviews/night2/TELEGRAPH_REFEREE/REPORT.md` (independent code in `checks/`). Premise finding and C&M diagnosis **confirmed** (deterministic quadrature + own MC; C&M's own cross-correlation t_A is single-log too). **Corrected:** adaptation constant −0.7 → −(γ+1), t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1]; "any projection kernel cannot discriminate" narrowed to regressions on the tracker's own observations (Bayes kernel on the true driver differs, rel. L2 0.61); precision vs effort label. **New:** exact MSE = μ²·2K₀(κ)/(K₀+K₁); C&M eqs. (41) α/4 and (42) α ln²α also come from the dropped drift (exact: (α/4)[ln(4/α) − γ], K₀/(K₀+K₁)); published PRE text unchanged. **Prior art:** leading-order error (Khasminskii & Zeitouni 1996; Golubev 2000; continuous time per Chigansky 2005); single-log delay is the quickest-detection form (Shiryaev; Tartakovsky & Veeravalli 2005). N16 → MATH-CORRECTED (v2.9). E2′/E4/E5/E6 verdicts in §4 (accept with changes); TLP-EDITS-REVIEW unblocked.
- **CM-PUBLISHED-CHECK** — DONE (covered by TELEGRAPH-REFEREE; not separately picked).
- **KERNEL-INPUT-DISCRIMINATE** (w 2, c 1.5). Bayes vs linear kernel on the true driver: shape, κ-scaling, and a discriminating design for KERNEL-MEASURE / VIX-KERNEL / SENSE-CELL. In-model first.
- **WONHAM-PRIORART-FULLTEXT** (w 1, c 0.5). Read Khasminskii & Zeitouni 1996, Golubev 2000, Wonham 1964, Liptser–Shiryaev ch. 9, Shiryaev 1963 in full via a sanctioned route; check whether 2K₀/(K₀+K₁) and γ + 1 are stated.
- **POISSON-SENSING-JUMP** (w 2, c 2). Bayes exponents for a switching world sensed through Poisson events (event data); check Peskir & Shiryaev 2002 and point-process filtering first.
- Notes added to TLP-EDITS-REVIEW, KERNEL-MEASURE, VIX-KERNEL, SAME-SYSTEM-AQN.

**Pick 7 done (ledger 44). Next pick (8) is the uniform slot: log a fresh unaided order, run the rule, take the top of that entry's stored uniform permutation (skip DONE/active per the pre-declared rule). Next free ledger entry: 45.**

### NEW (15 Nov ~12:35 PM ET, from D3-TWO-EXPONENT-OOS; surprises read per rule 4)
- **D3-TWO-EXPONENT-OOS** — DONE (pick 8, uniform slot; ledger 45–48): `tests/D3_OOS/RESULTS.md`, lock `83aba94` (prereg, code, lists, seeds, decision rules and a synthetic power check committed before any data). Out of sample (27 new GitHub repos, 5 Wikipedia category groups): **pure renewal failed on proxy "within-file consecutive log-gap correlation, binary daily edit series"** (M_w above its within-file-shuffle null in 27/27 and 5/5; median 0.225 vs null ≈ −0.01; renewal controls 0–0.10, R6 Cox 1.00); Δβ > 0 detected (Wilcoxon p = 0.00027, median 0.046). The item's own P1/P2 passed again and are non-discriminating (as the referee said). D3's positive sign replicated (+0.645; expected under both worlds). Post hoc: survives trimming each file's first year and the repo's last year (27/27). Does not separate Cox, trend and Hawkes. CLAIM_MAP N17 (v2.10); no existing row changed status. One post-lock code fix (A1, UTF-8 decode; no statistic affected).
- **D3-DISCRIMINATE** — DONE (covered by D3-TWO-EXPONENT-OOS P3; not separately picked).
- **EDIT-MODULATION-SOURCE** (w 2, c 2). Edit gaps are not renewal; separate shared rate modulation (Cox; cross-file co-modulation within a repo, cf. THEORY §6 "a shared driver calls for a level") from per-file self-excitation (Hawkes) and life-cycle trend. Design and synthetic power before any real run.
- **NEG-DELTA-BETA** (w 1, c 1; weak surprise). lodash and Wikipedia dog breeds have Δβ ≈ −0.11 with high M_w; no power-check world gave negative Δβ. Find the mechanism.

**Pick 8 done (ledger 48). Next pick (9) is the rule slot: log a fresh unaided order, run the rule, take the rule's top among open non-active items. Next free ledger entry: 49.**

### NEW (15 Nov ~12:45 PM ET, from TLP-EDITS-REVIEW; surprises read per rule 4)
- **TLP-EDITS-REVIEW** — DONE (pick 9, rule slot = unaided top, I = 3.6; ledger 49–52): `reviews/night2/TLP_EDITS_REVIEW.md` (own checks in `TLP_EDITS_REVIEW_checks/`). THEORY **v1.4.3**: E2′, E4, E5, E6 applied as the referee corrected them (premise "Gaussian world, or the best linear tracker"; jump-world t_A with γ + 1, Bessel closed-form error, elasticities 1/ℓ, 1 − 1/ℓ, −2 + 2/ℓ; kernel sentence "regressed on its own observations"; N12 homogeneity caveat; §10 credits labelled read / not read), five reviewer changes C1–C5, §2.4 D3 pointer to N17. Pass 1 (review + apply) and pass 2 (fresh hostile re-read of the full diff, same executor; nine fixes H1–H9) both recorded and passed. §0, §1, §2.1 untouched. CLAIM_MAP v2.11 (no status change).
- **HEADLINE-PREMISE-SCOPE** (w 2, c 0.5). §0, the status block, §2.1 and §1 N6 / CLAIM_MAP N13 state the noisy-sensing exponents and their inputs (α, q, N, stakes) without the premise "Gaussian world, or the best linear tracker". Minimal premise clause; touches the headline, so an independent reviewer applies it (Chad t1916).

**Pick 9 done (ledger 52). Next pick (10) is the unaided slot: log a fresh unaided order, run the rule, take Ace's unaided top (rule's if the same). Next free ledger entry: 53.**

*Correction (ledger 53):* the line above is wrong about the slot. The cycle (rule 3c) is rule, rule, unaided, uniform from pick 1, and pick 9 was a rule slot at cycle position 1, so pick 10 was the **rule** slot. Pick 10 followed the protocol, not that line.

### NEW (15 Nov ~12:47 PM ET, from HEADLINE-PREMISE-SCOPE; surprises read per rule 4)
- **HEADLINE-PREMISE-SCOPE** — DONE (pick 10, rule slot, I = 3.2; ledger 53–56): `reviews/night2/HEADLINE_PREMISE_SCOPE.md` (check in `HEADLINE_PREMISE_SCOPE_checks/`). **Proposal only; THEORY.md not edited** (Chad t1916). P1–P8 give exact old → new text putting "for a Gaussian world, or for the best linear tracker in any world" where §0, the status block, §2.1 and §1 N6 state the exponents or the inputs, with a lock guard (the optimum compared, best linear or Bayes, is fixed in the prereg; a miss against it counts). Check: at fixed q and N, splitting q into jump rate and size moves the linear tracker's error by 2% and the Bayes tracker's by 364× (two-state world, closed form confirmed by quadrature). No CLAIM_MAP status change.
- **HEADLINE-PREMISE-APPLY** (w 2, c 0.5). An independent reviewer reviews and applies P1–P8, with a second hostile pass before merge (Chad t1916).
- **REGIME-C-GAUSSIAN-PREMISE** — DONE (see NEW ~4:50 PM ET below). (w 2, c 0.5). Regime C's model size ∝ Q^{1/β} is reverse water-filling, exact for Gaussian modes; check whether it is Gaussian-only or an upper bound otherwise, and propose scope text.
- AQN-ESTIMATORS note: for a Bayes optimum in a jump world, q alone is useless (364× spread at fixed q); estimate λ and μ separately (weak evidence; no LR change).

**Pick 10 done (ledger 56). Next pick (11) is the unaided slot: log a fresh unaided order, run the rule, take Ace's unaided top (rule's if the same). Next free ledger entry: 57.**

### NEW (15 Nov ~1:45 PM ET, from AQN-ESTIMATORS; surprises read per rule 4)
- **AQN-ESTIMATORS** — DONE (pick 11, unaided slot; ledger 57–59, outcome 61): `measurement/estimators/RESULTS.md`, lock `3595c48`. Validated on synthetic truth: Whittle α, q, N (SE(α̂) ≈ 1/√M, M = frequencies below the noise crossover; ±0.1 needs M ≈ 400); corner check; HMM λ, μ, N, t_A (≳ 16 switches; SE(log λ̂) ≈ 1/√switches); premise LR (size ≤ 0.05, power 0.93–1.00); event worlds (Poisson floor, renewal flags); stakes only from exogenous error. DFA biased low under noise. Demo on proxy: DGS10 α̂ 2.00 ± 0.03 (random walk), log VIX regime not established. CLAIM_MAP N18 (DECIDED, method); no status change. Edits E-A1–E-A5 proposed, not applied.
- **AQN-REFEREE** (w 2, c 1). Hostile referee of the estimators, validation, label rules (R1 gap at α ≈ 2 without a corner) and E-A1–E-A5. — DONE (see NEW ~5:25 PM ET below; pick 21).
- **STAKES-EXOGENOUS** (w 3, c 2). Find a system with exogenous error variation and estimate stakes with a CI; gate for SAME-SYSTEM-AQN.
- **ALPHA-ESTIMATE-AUDIT** (w 1, c 1). Re-estimate earlier α/H values (DFA, Allan factor, nugget-free variograms) with the validated Whittle and corner check.
- **PREMISE-TEST-WIDEN** (w 2, c 1.5). Premise test beyond two-state vs Gaussian Markov (multi-state, heavy-tailed jumps, fBm null).
- Notes added: SAME-SYSTEM-AQN (stakes binding; record-length rules), SPF-AQN-POWERED (quarterly n ≈ 240 too short for ±0.1), VIX-KERNEL (log VIX has a corner; use realized variance), HEADLINE-PREMISE-APPLY (V143 F2 learner-class qualifier also for the status-block "What changed" item 2 and the §10 LFK entry).

**Pick 11 done (ledger 61). Next pick (12) is the uniform slot: log a fresh unaided order, run the rule, take the top of the new entry's stored uniform permutation that is open and not active.**

### NEW (15 Nov ~1:55 PM ET, from WIKIDATA-BAND; surprises read per rule 4)
- **WIKIDATA-BAND** — DONE (pre-existing locked test, out of cycle, unscored; ledger 65): `prereg/WIKIDATA-BAND/RESULTS.md`, lock `7cffd93` (THEORY v1.2-era T8 signs), addendum `28a0f21`. Full locked sample collected (2,693 pages, 0 AMBIG); analysis code unchanged; rerun from committed data byte-identical. **KG FAIL** (instrument does not count; Tier 3). P1 drift gradient INCONCLUSIVE (β_q 0.58 [0.21, 0.99]; ΔAUC vs item type 0.024 [−0.005, 0.058]); P2 INCONCLUSIVE; P3 INCONCLUSIVE (n = 83); **P4 passed on proxy** (4/4 wikis, k = 4). Item-level stability gate: 4 STABLE / 3 UNSTABLE / 19 not assessable; sensitivity refits not run. Optimum compared: reset-read cost optimum, premise-invariant (N16). Data event-like: scheduled series H < ½, leadership replacements rate-unstable (cf. N17). CLAIM_MAP N19 (OPEN), N20 (PROXY-PASS), v2.13. THEORY not edited (RESULTS §5).
- **KG-FEASIBILITY-GATE** (w 1, c 0.5). Known-groups / moot bounds must be shown attainable at the planned n before lock (WIKIDATA-BAND's KG(a) was unattainable at n = 40).
- **WIKIDATA-BAND-2** (w 1, c 2.5). Rerun with correction-filtered drift, n ≥ 63 per slow property, more properties, wiki template policy as a rival.

**Pick 11 done (ledger 61); WIKIDATA-BAND outcome logged out of cycle (ledger 65; entries 62–64 are q-pick12's, in flight). Next pick (12) is the uniform slot, as before.**

### NEW (15 Nov ~2:55 PM ET, from STAKES-EXOGENOUS; surprises read per rule 4)
- **STAKES-EXOGENOUS** — DONE (pick 12, uniform slot: top of entry 63's stored uniform permutation, nothing skipped; ledger 62–64, outcome 70, renumbered from 66 at the q-pick13 merge): `tests/STAKES_EXOGENOUS/RESULTS.md`, lock `27bbe72` (prereg, code, seeds, decision rules and a synthetic validation committed and pushed before any analysis data). **INCONCLUSIVE on proxy "CAISO DA load-forecast error; cost = error × (FMM − DA hub price)"**: ŵ 2025 = 7.8 [1.8, 12.6] × 10⁻⁴ $/(MW²·h): positive with CI excluding 0, but half-width 0.70ŵ > the locked 0.5 (S1 failed); exogeneity incremental R² 0.029 (pass); quadratic-loss shape passed (weak power); 2024 replication 3.2 [1.4, 5.1] × 10⁻³ (pass). Two declared post-lock amendments (A1 fetch timeout; A2 report-only subgroup rows used w_quad, fixed; verdict byte-identical). CLAIM_MAP N21 (v2.14); no status change; THEORY.md not edited.
- **STAKES-PRECISION** (w 2, c 1.5; from S1 fail). New lock to reach ±50%: pooled years with year effects, net-load error, 5-min prices, a second ISO. Gate for SAME-SYSTEM-AQN.
- **STAKES-SHIFT-CAISO** (w 3, c 3; weak surprise, unlocked): stakes fell ~4× from 2024 to 2025 (CIs do not overlap). THEORY §1 N6 causal form: pick a CAISO design quantity, fix the adjustment lag as a number, lock the direction, test on unseen years.
- **CAISO-PROXY-DEFS** (w 1, c 0.5). DA forecast 1.76 GW (7%) below "actual" on average; check the two series' public definitions.
- **STAKES-REFEREE** (w 2, c 1). Hostile referee of STAKES-EXOGENOUS.
- Note added to SAME-SYSTEM-AQN: CAISO is a candidate system once STAKES-PRECISION passes.

**Pick 12 done (ledger 64; outcome 70, written as 66, renumbered because q-pick13 had already used 66–68). Next pick (13) is the rule slot (cycle restarts: rule, rule, unaided, uniform): log a fresh unaided order, run the rule, take the rule's top among open non-active items. Next free ledger entry: 67.**

### NEW (15 Nov ~2:58 PM ET, from HEADLINE-PREMISE-APPLY; surprises read per rule 4)
- **HEADLINE-PREMISE-APPLY** — DONE as a PR, **not merged** (pick 13, rule slot, I = 3.2, tied with REGIME-C-GAUSSIAN-PREMISE and taken by id order; ledger 66–68, outcome 69; PR #37): `reviews/night2/HEADLINE_PREMISE_APPLY.md` (check in `HEADLINE_PREMISE_APPLY_checks/`). THEORY v1.4.4 / CLAIM_MAP v2.14 on branch q-pick13: P1–P8, the V143 F2 learner-class qualifier ("What changed" item 2, §10 LFK) and the line-6 CLAIM_MAP pointer. Applier tightenings T1–T5: keep hold-last-value in the reset-read premise; name only the derived jump-world exponents (adaptation time, error), with reset reads and the regression kernel unaffected; extra inputs only where the locked optimum is Bayes for a non-Gaussian world; a prereg naming no optimum is scored against the best linear one, in the causal form too. No status change. Own second hostile pass recorded; it does not satisfy Chad t1916.
- **HEADLINE-PREMISE-REVIEW** (w 2, c 0.5). A separate independent reviewer reviews the PR (sources, T1–T5, hostile pass) and merges or requests changes.
- Surprise read: none beyond the proposal's; the one design gap found (the lock would have excused tests locked before v1.4.4) is fixed in the text (T4), not a new item.

**Pick 13 done (PR #37 open, not merged; outcome ledger 69). Next pick (14) is the rule slot: log a fresh unaided order, run the rule, take the rule's top among open non-active items.**

### NEW (15 Nov ~3:40 PM ET, from HEADLINE-PREMISE-REVIEW; surprises read per rule 4)
- **HEADLINE-PREMISE-REVIEW** — DONE (pick 14, rule slot, I = 3.2, tied with REGIME-C-GAUSSIAN-PREMISE and taken by id order; ledger 71 unaided order (Ace's verbatim; HEADLINE-PREMISE-APPLY dropped as DONE, HEADLINE-PREMISE-REVIEW appended), 72 rule_rank, 73 pick, 74 rule_change, 75 outcome): `reviews/night2/HEADLINE_PREMISE_REVIEW.md` (checks in `HEADLINE_PREMISE_REVIEW_checks/`). Independent review **PASS** with three narrow fixes (R1 precision-effort exponent listed among those that differ; R3 heading time; R4 LFK pointer). **PR #37 merged** (92fc632): THEORY v1.4.4 and CLAIM_MAP v2.15/v2.16 are on main. No status change.
- **CAUSAL-KILL-INPUTS** (w 2, c 0.5). Review finding R2, proposed only: §1 N6 / §9 causal kill should cover the further inputs of a Bayes-locked test, §9 should match N6 ("does not move in the predicted direction"), and the adjustment lag should be a number fixed in the prereg. Separate applier + independent reviewer (kill conditions; Chad t1916).
- **Scorer bug (declared, fixed):** `queue/sg_rank.py score` sorted bootstrap AUCs before dropping NaN, garbling the CI (rule 0.679 "CI 0.727–0.943"). Declared at ledger 74 (rule_change, no parameter change), then fixed. Corrected at 19 outcomes: rule 0.679 [0.375, 0.943], unaided 0.635 [0.375, 0.875], uniform 0.276 [0.071, 0.536] → Q0 reads **INCONCLUSIVE** (the bug would have shown PASS). N9 stays OPEN.
- Surprise read: the T2 rationale in HEADLINE_PREMISE_APPLY.md wrongly said the jump-world precision-effort exponent was not derived (N16 has it); fixed in text by R1 (weak; no LR change). Monte Carlo t_A at κ = 10⁻³ sits 0.05 (≈ 4 SE) above the leading-order formula: o(1)/step-size, no new item.

**Pick 14 done (PR #37 merged; outcome ledger 75). Next pick (15) is the unaided slot: log a fresh unaided order, run the rule, take Ace's unaided top (rule's if the same) among open non-active items. Next free ledger entry: 76 (recheck all pushed branches).**

### NEW (15 Nov ~4:00 PM ET, from ONA-MORE; surprises read per rule 4)
- **ONA-MORE** — DONE (pick 16, UNIFORM slot: top of entry 80's stored perm, seed 20261195; rule rank 41 of 41, I = 0.035; Ace's unaided rank 40 of 41). Gate check with criteria fixed before searching: no public dataset has tenure, real reporting units and a shared-environment vs own-task question (Netzschleuder 811 nets, networkdata 990, 3 web searches; table in the report). No data analysed; H8 vigilance OPEN; no status change. Surprise: none (expected by the item's own note).
- **ONA-INSTRUMENT-DRAFT** (w 1, c 0.5, untested). Draft and lock the two-generator ONA instrument, analysis code (QAP primary, HKSJ pool, tenure covariates) and a power curve on synthetic data only, so primary collection could run if Chad chooses. No contact with anyone.

### NEW (15 Nov ~4:12 PM ET, from CAUSAL-KILL-INPUTS; surprises read per rule 4)
- **CAUSAL-KILL-INPUTS** — DONE (pick 17, rule slot, I = 3.2, tied with REGIME-C-GAUSSIAN-PREMISE and taken by id order; ledger 83 unaided order, 84 rule_rank, 85 pick, 86 outcome; PR #41). Author note `reviews/night2/CAUSAL_KILL_INPUTS_AUTHOR.md`. Separate independent review `reviews/night2/CAUSAL_KILL_INPUTS_REVIEW.md` (own checks in `CAUSAL_KILL_INPUTS_REVIEW_checks/`, including a Wonham-filter Monte Carlo): **PASS-WITH-FIXES**, with fixes to the changelog and pointer only. **Merged:** THEORY v1.4.5 is on main. N6's causal kill now also fires on the further inputs of a Bayes-locked prereg and is scored by the direction the locked optimum predicts from inputs before and after the change. The lag is a number fixed in the prereg, and §9 is aligned with N6. STAKES-SHIFT-CAISO is unaffected. No status change.
- **CAUSAL-NULL-INVARIANCE** (w 2, c 1). Review Q1. Decide whether a move beyond error under a predicted null should count as a miss. This is an invariance claim, so a separate applier and reviewer are needed. It is also a Bayes-vs-linear discriminator: a split q change leaves Bayes t_A fixed, while the linear optimum predicts −29.5%.
- **CAUSAL-KILL-PRICE** (w 1, c 0.5). Review Q2. The effort price is an input of every §2.2 optimum but is not in the causal trigger list. Proposal only.
- ~~**CAUSAL-KILL-MAGNITUDE**~~ — DONE 15 Nov ~5:40 PM ET (pick 24, uniform slot): symmetric band rejected; explicit bounded share κ proposed in PR #48 (DO NOT MERGE without separate reviewer PASS) (`reviews/night2/CAUSAL_KILL_MAGNITUDE.md`).
- Surprise read (weak): R2's claim that a linear-locked optimum moves under any input change holds only for single-input changes. The joint-change null is recorded in the v1.4.5 changelog. No LR change.

**Pick 17 done (PR #41 merged; outcome ledger 86). Next pick (18) is the rule slot. Next free ledger entry: 87; recheck all pushed branches, because q-pick15 holds 76–78.**

### NEW (15 Nov ~4:40 PM ET, from STAKES-SHIFT-CAISO; surprises read per rule 4)
- **STAKES-SHIFT-CAISO** — DONE (pick 15, unaided slot: Ace's unaided top in entry 76, open and not active, nothing skipped; rule rank 27 in entry 77; ledger 76 unaided order (Ace's verbatim, matched the 41 open ids exactly), 77 rule_rank, 78 pick, outcome 91): `tests/STAKES_SHIFT_CAISO/RESULTS.md`, lock `874576f` (pushed 3:14 PM ET before any outcome data). First locked N6 causal-form test (best linear tracker, α = 2, lag 12 months: stakes 2024→2025 predict DA forecast precision 2026 vs 2025). **INCONCLUSIVE on proxy "CAISO DA-vs-RTD forecast MSE (q-adjusted by seasonal naive), stakes = k_lin on the same error"**, by gates: on the like-for-like error the stakes fall is only −0.41 [−0.88, +0.07] in log (G0 fail) and the seasonal-naive MSE rose ×2.17 (G2 fail, Sep–Oct 2026 heat). D = −0.09 vs predicted +0.14; with year noise s_yr 0.32 neither rule was attainable. α̂ 2.10 ± 0.09. CLAIM_MAP N22 (v2.19); N21 pointer. Amendment A1 fetch-only.
- **CAISO-PROXY-DEFS** — DONE inside pick 15 (before its lock; unscored): mean (actual − DA) is solar-shaped (~0 at night, +4–6 GW at noon): "actual" is gross of BTM solar, the forecasts net of it (secondary source; CAISO's page not found). Use RTD − DA.
- **CAUSAL-POWER-GATE** (w 1, c 0.5). Causal-form preregs must show their PASS and FAIL rules are attainable at the expected effect and year-to-year noise before lock.
- **STAKES-SHIFT-MULTIYEAR** (w 3, c 3). Powered N6 causal test: many stakes changes (archived CAISO prices 2019–2023, or an ISO panel), like-for-like error, lag 12 months, q control, power gate met.
- Surprise read: **weak** — N21's 4× stakes fall shrinks to ~34% on the like-for-like error (likely attenuation by BTM-definition noise) → note on STAKES-REFEREE and STAKES-PRECISION; the naive-MSE jump is weather (diagnostic), no item.

**Pick 15 done (outcome ledger 91; PR from q-pick15-merge). Next pick in cycle after 18 is unchanged; next free ledger entry: 92 (recheck all pushed branches).**

### NEW (15 Nov ~4:50 PM ET, from CAUSAL-POWER-GATE; surprises read per rule 4)
- **CAUSAL-POWER-GATE** — DONE (pick 19, unaided slot: Ace's unaided top in entry 92, open and not active, nothing skipped; rule rank 4 in entry 93; ledger 92 unaided order, 93 rule_rank, 94 pick, 95 outcome): `reviews/night2/CAUSAL_POWER_GATE.md`, tool `tools/power_gate.py` (+ tests), FRAMEWORK **MV10**, QUEUE rule 2. Gate: |b|·S ≥ (z₁₋α/₂ + z_π)·σ/min(1, κ) (2.80σ at α 0.05, π 0.8); an absolute FAIL margin ε needs σ ≤ ε/2.80 whatever the input change. Pick 15 re-checked: PASS region empty (band top 0.352 < 1.96·0.342), P(FAIL | no response) 0.035; both rules at 0.8 need ×17.8 stakes in one year (×7.5 = coin-flip PASS, the item's "~7×"), or K ≥ 49 contrasts of |Δlog w| 0.41. Process only; THEORY not edited.
- **KG-FEASIBILITY-GATE** — DONE, merged into CAUSAL-POWER-GATE (same rule; best-case form `power_gate.py zero-events` reproduces WIKIDATA-BAND's 0.031/yr and n ≥ 63). Open-prereg audit: C3b fails MV10 on its own power output (locked before the gate; unchanged).
- **CAUSAL-POWER-GATE-N6** (w 1, c 0.5). Optional N6/§9 pointer to MV10; kill-condition text, separate author + independent reviewer.
- ~~**C3B-GATE-ADDENDUM**~~ (w 1, c 0.5) — DONE 15 Nov ~6:40 PM ET (pick 31, UNAIDED slot; ledger 142–144 + outcome 152): `tests/C3b/PREREG_ADDENDUM_A3.md`, `reviews/night2/C3B_GATE_ADDENDUM.md`. Real pre-shock Arm P n ≤ 2,294; MV10 **not met** (P(HIT | theory) 0.86, P(MISS | null) 0.65 on PREREG §5's data; 0.75/0.93 without its confounder); any stage-4 verdict labelled exploratory.
- STAKES-SHIFT-MULTIYEAR note gains the gate numbers (K ≥ 49 at the observed change; κ-relative FAIL margin). **v1.4.7 (CAUSAL-KILL-MAGNITUDE-REVIEW):** at N6's κ_F ≤ ½ the gate needs **K ≥ 193** contrasts of |Δlog w| = 0.41 at κ_F = ½ (×317 for one contrast), before s·λ scaling; K ≥ 49 was at κ = 1, now outside N6's range.
- Surprise read: **weak** — pick 15's PASS rule was empty by construction and its FAIL rule unreachable at any stakes change; no theory row moves.

**Pick 19 done (outcome ledger 95). Next pick (20) is the uniform slot (cycle position 4). Next free ledger entry: 96 or above (recheck all pushed branches, incl. the PR #42 reviewer's).**

### NEW (15 Nov ~4:50 PM ET, from REGIME-C-GAUSSIAN-PREMISE; surprises read per rule 4)
- **REGIME-C-GAUSSIAN-PREMISE** — DONE (pick 18, rule slot; ledger 87 unaided order, 88 rule_rank, 89 pick, 90 author outcome, 99 review outcome; PR #42 merged after independent review PASS-WITH-FIXES). THEORY v1.4.6: Regime C premise (independent modes of one shape; size means bits); Q^{1/β} derived for sub-Gaussian shapes at any β and finite-variance shapes at β > 1; zero-bit cutoff (w/κ)λ_i ≤ 1/(2v*); not derived: dependent modes, β ≤ 1 with non-sub-Gaussian shapes (so the interior minimum is sub-Gaussian only), drifting-world rate. §0 says "for Gaussian modes (wider scope … in §2.2)". Author note `reviews/night2/REGIME_C_PREMISE.md`; review `reviews/night2/REGIME_C_PREMISE_REVIEW.md`.
- **REGIME-C-DEPENDENT-MODES** (w 2, c 2). Bits exponent for uncorrelated but dependent modes (natural images need it).
- **REGIME-C-HEAVY-TAIL-LOWBETA** (w 2, c 1.5). Small-u rate asymptotics for Laplace / Student t; review heuristic: Student-t with ν ≤ 2/β may break Q^{1/β} at β ≤ 1 (decisive case).
- **REGIME-C-DRIFT-NONGAUSS** (w 2, c 1.5). Drifting-world rate Q^{min(½,1/β)} off Gaussian innovations.
- **REGIME-C-PRIORART-USTAR** (w 1, c 0.5). Prior art for the D_max slope 1/(2v*) (KKT / Gibbs-channel conditions; read before crediting).
- **REGIME-C-PREREG-CASE-N6** (w 1, c 0.5). Default scoring for a Regime C prereg that states no case; kill-condition text, separate author + reviewer.
- Surprise read: **moderate, untested** — heavy polynomial tails at β ≤ 1 may break the size exponent outright (heuristic only); no row moves.

**Pick 18 done (review outcome ledger 99; 96–98 held by unmerged q-pick20). Next free ledger entry: 100 or above (recheck all pushed branches).**

### NEW (15 Nov ~5:15 PM ET, from SPF-RIGIDITY-OOS; surprises read per rule 4)
- **SPF-RIGIDITY-OOS** — DONE (pick 20, UNIFORM slot: top of entry 97's stored perm, seed 20261212; rule rank 32 of 43, I = 0.4; Ace's unaided rank 19 of 43). Unseen set = the 9 SPF variables never CG-regressed here (NGDP, PGDP, CPROF, RGDP, RCONSUM, RNRESIN, RRESINV, RFEDGOV, CPI); K_L0w, β^G and planned-n sampling sd computed before any outcome; planned pooled multiple c (H_R 2.5 vs H_0 1): best P(PASS|2.5) 0.62 and P(FAIL|1) 0.60 (PGDP carries 85% of the information and its β^G CI spans ×100); 0.71/0.72 even with sd × 0.8. **Gate not met**; nothing locked; N13 OPEN; no status change.
- **SPF-RIGIDITY-LIVINGSTON** (w 2, c 3). Livingston Survey and/or ECB SPF: validate a noise instrument for their horizon design on synthetic truth, then run the MV10 power simulation (`tests/SPF_RIGIDITY_OOS/power.py`) on planned data; lock only if both rules reach 0.8.
- Surprise read: **weak** — quarterly growth/inflation series are near-white at the 3-quarter horizon, so the optimal filter's CG coefficient (0.13–0.35) is buried in planned sd 0.3–0.7; only the SPF level series carry usable CG precision.

**Pick 20 done (ledger 96–98 + outcome). Next pick (21) is the rule slot. Recheck all pushed branches before any ledger write.**

### NEW (15 Nov ~5:25 PM ET, from AQN-REFEREE; surprises read per rule 4)
- **AQN-REFEREE** — DONE (pick 21, rule slot: rule's top in entry 101, I = 2.4, tied with NOISE-PROXY-REFEREE and taken by id order; Ace's unaided rank 1 of 47; ledger 100 unaided order, 101 rule_rank, 102 pick, outcome 107): `reviews/night2/AQN_REFEREE.md`, independent code in `reviews/night2/AQN_REFEREE_checks/` (`ownlib.py` does not import `aqn.py`). **PASS-WITH-FIXES** for the estimators: the Whittle model, aliasing, D1 constant, information SEs and the DGS10 demo (2.004 ± 0.026, log q −5.70) were reproduced exactly, and Wald SEs held on DGS10 against block dispersion. Corrections: (1) SE(α̂) ≈ 1/√M understates the SE by 1.5–2.3× when the noise floor is above Nyquist; (2) **the premise test rejected 0 of 24 jump-diffusion random walks** (kurtosis flagged 24 of 24), so **E-A2 FAILS** and is replaced by E-A2′; (3) R1 mislabels a random walk as B, so R1′ is proposed (DGS10 → A on proxy); (4) the plug-in t_A is 1.14–1.89× short of the exact discrete filter at block C's 0.6–14-step t_A; (5) the replicate IV for stakes is biased by 1/(1 + c²) under multiplicative error; also, "validated once M ≳ 250" fails at α 1.4 with heavy noise (coverage 0.81). E-A1 and E-A3 pass with fixes; E-A4 and E-A5 pass with a wording fix (not applied). No CLAIM_MAP change.
- **AQN-EDITS-APPLY** (w 1, c 0.5). Apply E-A1 (fixed), E-A2′ and E-A3 (fixed) to FRAMEWORK, and add R1′ as a dated addendum in `measurement/estimators/`. A separate applier makes the THEORY pointer edits E-A4 and E-A5.
- **DISCRETE-TA** (w 2, c 1). Bayes adaptation time of the sampled two-state filter vs per-sample SNR and λ; settle the definition against N16; independent check before any N16 field test on sampled data. → DONE (pick 23; block below).
- PREMISE-TEST-WIDEN: referee flag, L 2 → 3 (must include jump-diffusion alternatives and a GARCH null). Notes added to SAME-SYSTEM-AQN and SPF-AQN-POWERED (the SE rule is optimistic when the floor is above Nyquist; use the information-matrix SE, MV10).
- Surprise read: **moderate** (referee flag: the premise test is blind to the most natural non-Gaussian class for prices); weak (SE rule; discrete t_A). No theory row moves.

**Pick 21 done (outcome ledger 107; 104–106 are held by q-pick22, which claimed NOISE-PROXY-REFEREE as pick 22, rule slot). Next pick after 22 is pick 23, the unaided slot. Recheck all pushed branches before any ledger write.**

### NEW (15 Nov ~5:20 PM ET, from NOISE-PROXY-REFEREE; surprises read per rule 4)
- **NOISE-PROXY-REFEREE** — DONE (pick 22, RULE slot: rule's top AQN-REFEREE is active on q-pick21, so the next, I = 2.4 tied, id order; Ace's unaided rank 6 of 47; uniform rank 33 of 47; ledger 104–106 + outcome 111). **PASS-WITH-FIXES on proxy "SPF within-forecaster nowcast dispersion".** Own time-domain code reproduces K̂_L0w (7/7) and β^G (3 decimals). Consensus-nowcast-variance branch check confirms the lower branch for 6 of 7; **RSLGOV not identified** (leans upper, β^G ≈ 7), so post hoc S-1 narrows to UNEMP, HOUSING, TBILL. Estimator fine below the validated K range (to 0.001). A common public signal gives G ≤ 0 and true β ≤ β^G, so it explains neither T1 nor S-1. Erratum: ≥ 3 null SDs in 5 of 7, not 6. Audit: no other live dispersion-based N; SPF-RIGIDITY-OOS inherits wide PGDP/CPI K ranges. No status change; N13 OPEN.
- Notes added to SPF-RIGIDITY-LIVINGSTON (branch check + validated K range) and SPF-NOTE-EDITS (edit 1 has no target in THEORY v1.4.6; edit 2 endorsed with additions).
- Surprise read: **weak**. New items: none.

**Pick 22 done (ledger 104–106 + outcome 111; 107 = pick 21 outcome, 108–110 pick 23). Next pick (23) is the unaided slot. Recheck all pushed branches before any ledger write.**

### NEW (15 Nov ~5:40 PM ET, from DISCRETE-TA; surprises read per rule 4)
- **DISCRETE-TA** — DONE (pick 23, UNAIDED slot: Ace's top in entry 108; rule rank 6 of 48, I = 1.4; uniform rank 48 of 48; ledger 108 unaided order, 109 rule_rank, 110 pick, 127 outcome; `reviews/night2/DISCRETE_TA/REPORT.md`, `tools/discrete_ta.py`). In-model. Referee Q1 answered: the referee's discrete t_A is N16's quantity for the *quiet* pre-switch law (resting law after a long quiet spell; N16's derivation law); a switch at a typical time uses the stationary law at a switch, which differs by O(κ ln 1/κ) (< 0.5% at κ ≤ 10⁻³; 1.5–11% shorter at the referee's κ). Linear tracker: exact closed form cosh(βΔ) = cosh(aΔ) + ρ sinh(aΔ); within 1% of the continuous memory time at ≥ 2 samples. Bayes: t_A,grid = T(κ) + 0.5826√(ΔN)/μ + ≈ 0.25Δ (C₁ = −ζ(½)/√(2π) by optional stopping + Broadie–Glasserman–Kou overshoot, read; c₂ fitted); the quiet-law grid value is within 10% of the plug-in only at ≥ 10–27 samples per t_A (κ = 10⁻⁶ … 10⁻²) and within 5% at ≥ 30–122. Lattice vs independent MC: χ² 12.9 on 20 df. Referee V8 ratios revised to 1.16–1.89× (0.6–14 steps) and 1.06–1.08× (56–151 steps). No THEORY or CLAIM_MAP edit merged; N16 scope sentence authored in PR #53, marked DO NOT MERGE without separate reviewer PASS.
- ~~**DISCRETE-TA-N16-REVIEW**~~ — DONE 15 Nov ~6:02 PM ET (out-of-cycle, unscored: continuation of pick 23's author PR per t1916 independent-review rule; ledger 133): **PASS-WITH-FIXES**, PR #53 merged, THEORY v1.4.9, CLAIM_MAP v2.26 (`reviews/night2/DISCRETE_TA_N16_REVIEW.md`). Own code confirms the linear closed form, the thresholds, both laws and the BGK constant (read). Found: the grid √Δ coefficient is κ-dependent (0.567 at κ = 10⁻², 0.547 at 3·10⁻²; C₁ only as κ → 0), so "0.58" is hedged; clock origin stated (switch inside the interval moves thresholds); both laws named, not locked.
- **DISCRETE-TA-INTEGRATED** (w 2, c 1). Integrate-and-dump sampling of a continuous switching world (switch inside an interval) and asymmetric/multi-state worlds; needed before an N16 field test on binned data.
- **DISCRETE-TA-SECOND-ORDER** (w 1, c 1). Prove the mean-time version of the C₁ overshoot correction and derive c₂ (κ-dependent residual at κ = 10⁻², ρ = 0.0025 unresolved). *Updated by DISCRETE-TA-N16-REVIEW:* the 4.5% residual was a lattice artifact, but c(κ) is genuinely below C₁ by O(κ ln 1/κ) (2.6% at κ = 10⁻²); a barrier-shift heuristic explains about 80%; derive c(κ).
- Notes added to AQN-EDITS-APPLY (replace the "≳ 20 steps" rule with the DISCRETE-TA thresholds) and CAUSAL-NULL-INVARIANCE (the grid term moves under the λ ×2.65, μ² ×0.75 null: +1.2% of t_A at 20 samples).
- Surprise read: **weak-moderate** — the Bayes grid correction decays only as r^{−1/2} (linear: r^{−2}), and on a grid it carries linear-looking N and μ elasticities (½, −1), so sampled Bayes-vs-linear exponent tests must be grid-corrected; and "t_A" has two O(κ ln 1/κ)-different meanings that a prereg must fix. No theory row moves.

**Pick 23 done (ledger 108–110 + outcome 127; written after picks 24–26 merged). Recheck all pushed branches before any ledger write.**

## Done (frozen)
- NOISE-PROXY-REFEREE: `reviews/night2/NOISE_PROXY_REFEREE.md`, `reviews/night2/NOISE_PROXY_REFEREE_checks/` (PASS-WITH-FIXES; no status change).
- DISCRETE-TA: `reviews/night2/DISCRETE_TA/REPORT.md` (+ `checks/`), `tools/discrete_ta.py` (sampled-grid t_A; in-model; no status change; N16 scope text in PR #53, not merged).
- AQN-REFEREE: `reviews/night2/AQN_REFEREE.md` (+ `AQN_REFEREE_checks/`; independent referee of AQN-ESTIMATORS; PASS-WITH-FIXES, E-A2 fails; no status change).
- SPF-RIGIDITY-OOS: `tests/SPF_RIGIDITY_OOS/` (MV10 gate not met; no prereg locked; no outcome computed).
- REGIME-C-GAUSSIAN-PREMISE: `reviews/night2/REGIME_C_PREMISE.md`, `reviews/night2/REGIME_C_PREMISE_REVIEW.md` (independent review PASS-WITH-FIXES; THEORY v1.4.6; PR #42 merged).
- CAUSAL-POWER-GATE (+ KG-FEASIBILITY-GATE merged): `reviews/night2/CAUSAL_POWER_GATE.md`, `tools/power_gate.py` (FRAMEWORK MV10; process; no status change).
- STAKES-SHIFT-CAISO: `tests/STAKES_SHIFT_CAISO/` (lock 874576f; not refereed; N22 INCONCLUSIVE on proxy; CAISO-PROXY-DEFS settled inside it).
- CAUSAL-KILL-INPUTS: `reviews/night2/CAUSAL_KILL_INPUTS_REVIEW.md` (independent review PASS-WITH-FIXES; THEORY v1.4.5; PR #41 merged).
- ONA-MORE: `reviews/night2/ONA_MORE_GATE.md` (gate not met; no data analysed).
- HEADLINE-PREMISE-REVIEW: `reviews/night2/HEADLINE_PREMISE_REVIEW.md` (independent review PASS with R1, R3, R4; PR #37 merged; R2 → CAUSAL-KILL-INPUTS).
- HEADLINE-PREMISE-APPLY: `reviews/night2/HEADLINE_PREMISE_APPLY.md` (THEORY v1.4.4; merged after independent review, PR #37).
- STAKES-EXOGENOUS: `tests/STAKES_EXOGENOUS/` (lock 27bbe72; not refereed; N21 INCONCLUSIVE on proxy; STAKES-REFEREE queued).
- WIKIDATA-BAND: `prereg/WIKIDATA-BAND/` (locked v1.2-era test; not refereed; N19, N20).
- AQN-ESTIMATORS: `measurement/estimators/` (lock 3595c48; not refereed; AQN-REFEREE queued).
- HEADLINE-PREMISE-SCOPE: `reviews/night2/HEADLINE_PREMISE_SCOPE.md` (proposal P1–P8; not applied; HEADLINE-PREMISE-APPLY queued).
- TLP-EDITS-REVIEW: `reviews/night2/TLP_EDITS_REVIEW.md` (THEORY v1.4.3; two passes recorded).
- D3-TWO-EXPONENT-OOS: `tests/D3_OOS/` (locked out-of-sample test; not refereed; N17).
- TELEGRAPH-REFEREE: `reviews/night2/TELEGRAPH_REFEREE/` (referee of TELEGRAPH-LINEAR-PREMISE; N16 MATH-CORRECTED v2.9).
- TELEGRAPH-LINEAR-PREMISE: `reviews/night2/TELEGRAPH_LINEAR_PREMISE/` (refereed by TELEGRAPH-REFEREE: corrected; TLP-EDITS-REVIEW queued).
- GITHUB-UPSTREAM: `night2/GITHUB/` (locked v1.1-era test; not refereed; interpretation note feeds TELEGRAPH-LINEAR-PREMISE).
- PRIORART-LFK-ALPHA: `reviews/night2/PRIORART_LFK_ALPHA/` (not refereed; credit edits queued).
- SPF-NOISE-PROXY: `tests/SPF_NOISE_PROXY/` (not refereed; NOISE-PROXY-REFEREE queued).
- MEASURE-SELF: `reviews/night2/SELF/` (refereed; re-read under THEORY §2.5 in §8c).
- VIGIL_ONA: `prereg/vigil-ona/` (refereed).
- Night-2 referee: `reviews/night2/REFEREE/`.
- Divergence audit: `reviews/night2/AUDIT_DIVERGENCE.md`.
- PRIORART-SWEEP (gap-fill) and SPECTRUM-MAP-DERIVE: `reviews/night2/SPECTRUM_MAP/` (refereed: `reviews/night2/SPECTRUM_MAP_REFEREE.md`).
- SPECTRUM-MAP-REFEREE: `reviews/night2/SPECTRUM_MAP_REFEREE.md` + `reviews/night2/SPECTRUM_MAP_REFEREE_checks/`.
- LEARNSIM: `tests/LEARNSIM/`, referee `reviews/night2/LEARNSIM_REFEREE.md` (T1.8 NOT PASSED; no existing CLAIM_MAP status change; rows G23–G29 added in v2.3).
- THEORY-2.2-REWRITE: `THEORY.md` v1.4, `measurement/CLAIM_MAP_v2.md` v2.3, `reviews/night2/THEORY14_checks/`.

### NEW (15 Nov ~5:40 PM ET, from CAUSAL-KILL-MAGNITUDE; surprises read per rule 4)
- **CAUSAL-KILL-MAGNITUDE** — DONE (pick 24, UNIFORM slot: first id of entry 113's stored permutation, seed 20261228, open and not active, nothing skipped; rule rank 19 of 47, I = 0.8; Ace's unaided rank 15 of 47; ledger 112 unaided order, 113 rule_rank, 114 pick, outcome 115). Proposal only, own Monte Carlo (`reviews/night2/CAUSAL_KILL_MAGNITUDE_checks/`). A symmetric elasticity band as a kill false-kills 85–100% under ordinary partial adjustment or input noise: rejected. The sign-only reading has only its size (5–6%) as power against N6's named rival (no move), so MV10 FAIL rules already carry a per-prereg κ that N6 does not constrain. Proposed: kill iff the measured move excludes a share κ (0 < κ ≤ ½, fixed in the prereg) of the locked optimum's predicted move, scaled by measured adjustment share and input reliability; author-only PR #48, **DO NOT MERGE without separate reviewer PASS**. Surprise: moderate. No status change; vigilance OPEN.
- ~~**CAUSAL-KILL-MAGNITUDE-REVIEW**~~ — DONE 15 Nov ~5:50 PM ET (out-of-cycle, unscored: continuation of pick 24's author PR per t1916 independent-review rule; ledger 124): **PASS-WITH-FIXES**, PR #48 merged, THEORY v1.4.7 (`reviews/night2/CAUSAL_KILL_MAGNITUDE_REVIEW.md`). Table reproduced with own code. Rulings: no κ ≤ ¼ cap (a Bayes-switching design under a linear lock is killed whenever κ_F > 2/ℓ with enough data, so no fixed cap is safe; the kill is legitimate under the v1.4.4 lock rule); estimating s, λ adds ≤ ~1 point of false kills at κ_F ≤ ½ (up to 7 with a short lag and τ known within a factor e; propagation removes it); v1.4.7. Fixes: symbol κ_F; one-sided 'falls short … beyond measurement error'; s, λ not from the design's response to the inputs under test; zero predicted move unscored; power_gate default κ = ½; MV10 pointer.
- **LOCK-SENSITIVITY-REPORT** (w 1, c 0.5). From CAUSAL-KILL-MAGNITUDE-REVIEW §4: MV10 reporting line + `power_gate.py` option — each linear-locked causal prereg reports, at its κ_F on its planned data, the kill probability under the Bayes-switching alternative at its measured (or a stated range of) jump inputs. Joins PREMISE-TEST-WIDEN.

**Pick 24 done (outcome ledger 115; 108–110 are held by q-pick23, DISCRETE-TA active). Pick 24 closed the cycle (21 rule, 22 rule, 23 unaided, 24 uniform); next pick is 25, the rule slot. Recheck all pushed branches before any ledger write.**

### NEW (15 Nov ~6:10 PM ET, from KERNEL-MEASURE; surprises read per rule 4)
- ~~**KERNEL-MEASURE**~~ — DONE (pick 28, UNIFORM slot: first id of entry 131's stored permutation, seed 20261246, open and not active, nothing skipped; rule rank 35 of 47, I = 0.333; Ace's unaided rank 26 of 47; ledger 130 unaided order, 131 rule_rank, 132 claim, outcome after 136). `tests/KERNEL_MEASURE/RESULTS.md`, lock `6d235ed`. **Passed on proxy** "Parkinson range variance as driver, 2 ln VIX as tracker, survival at 21 business days of the 504-day binned projection kernel", **exploratory** (realized σ_D 0.049 > locked 0.040; inconclusive with the free-noise α̂ 1.19): Ŵ21 = 0.260 ± 0.041 vs the linear optimum's 0.277 ± 0.026 from the driver's measured α̂ = 1.26 ± 0.04 (Regime B over periods ≥ 21 d), q, N; α = 2 EWMA, flat 1/5/22-day and matching-exponent kernels excluded. Design 1 (kernel-family exponent) failed MV10 before lock. First measured tracking kernel; not Bayes vs linear. THEORY v1.4.10 evidence edit: PR #58, DO NOT MERGE without separate reviewer PASS. No CLAIM_MAP status change.
- **KERNEL-MEASURE-REFEREE** (w 2, c 0.5). Independent referee of the above with own code; pass/fail PR #58. *PR #58 part DONE 15 Nov ~6:20 PM ET (out-of-cycle, unscored; ledger 139): **PASS-WITH-FIXES**, merged as THEORY v1.4.10 / CLAIM_MAP v2.28 (`reviews/night2/KERNEL_MEASURE_REVIEW.md`). All key numbers reproduce with own code; the author's free-noise INCONCLUSIVE moved α alone (consistent refits 0.276–0.278; full-band inputs 0.256), so it does not bear on the verdict; still exploratory (bootstrap SE 0.041 > 0.040). Remaining: proxy validity only (variance risk premium, log of expectation, overnight variance, jumps).*
- **KERNEL-DECISIVE-RV** (w 2, c 3). Decisive kernel test: intraday RV or second N proxy, tighter α, or a second system; MV10 at the measured tracker noise. *Review note (ledger 139): a tighter α is not needed; the bootstrap SE of Ŵ21 is the binding constraint.*
- **AQN-R1-NOISE-BAND** (w 1, c 0.5). AQN R1's fixed 20-step split mislabels series whose noise crossover is inside the band; crossover-relative split, validated.
- **KERNEL-LONG-LAG** (w 1, c 1). Post hoc: VIX weight beyond ~8 months is zero where the optimum keeps 3–4%; corner or premium explanation first.
- Note added to **VIX-KERNEL**: tail exponent not resolvable at daily resolution; survival at one horizon measured in KERNEL-MEASURE.

### NEW (15 Nov ~6:20 PM ET, from ONSET-NOISY-READS; surprises read per rule 4)
- ~~**ONSET-NOISY-READS-REVIEW**~~ (w 2, c 1) — DONE 15 Nov ~6:27 PM ET (pick 30, RULE slot: top of entry 146, I = 1.8; Ace's unaided rank 7 of 49; ledger 145 unaided order, 146 rule_rank, 147 claim, 148 outcome; first numbered 139–141 on q-pick30, renumbered after a collision with main's 139 and q-pick31's 142–144). **PASS-WITH-FIXES**, PR #60 merged as THEORY v1.4.11 / CLAIM_MAP v2.29 (`reviews/night2/ONSET_NOISY_READS_REVIEW.md`). Every THEORY number reproduces with own code; the author's assumed dense-sampling asymptote is derived from the Kolmogorov–Szegő formula (Szegő ratio 1.00001 at α = 1.25, z = 10⁶); fixes: constants scoped to negligible member read noise, −2 limit in the ratio sense, curvature test only on ρ windows straddling ρ_c. No status change. Original item: Separate reviewer of PR #60 (THEORY v1.4.11 N12 premise (ii); CLAIM_MAP v2.29): re-derive the collapse, g_α, C_α and ρ_c with own code; check the uniform-convergence step, the α = 1.25 numerics and the curvature-classification claim; settle v1.4.10/v2.28 numbering against PR #58.

- **ONSET-SLOPE-POINTWISE** (w 1, c 0.5; from pick 30). Derive z f′(z)/f(z) → 1 − 1/α from the Szegő form so the pointwise local slope −2 is derived, not numerical.
- **N2-CURVATURE-POWER** (w 2, c 1; from pick 30). Power of onset curvature for classifying the level's technology at realistic noise and ρ windows, before any N2 prereg relies on it.

**Pick 30 done (ledger 148).** 

**Pick 29 done (ledger 138). Next pick (30) is the rule slot (cycle position 2): rule's top among open non-active items (log a fresh unaided order first).**

### NEW (15 Nov ~6:40 PM ET, from C3B-GATE-ADDENDUM; surprises read per rule 4)
- Surprise read: **weak** — real n (≤ 2,294) is ~5× the audit's 300–500, so H1/K1 alone would meet the gate; the binding constraints are the conjunctive HIT (S9's latency control nearly collinear with tau) and the assumed confounder's +0.045 bias against K1's absolute 0.15 margin.
- **C3B-STAGE4-DECIDE** (w 2, c 2). Before any C3b stage 3–6 run: run as exploratory (A3 labels it) or redesign before outcomes (sixth exogenous shock / wider frame to n ≈ 4,000; κ-relative K1 margin; S9 control not collinear with tau) in a dated addendum with its own MV10 output.

**Pick 31 done (unaided slot; ledger 142–144 + outcome 152; pick 30's entries were renumbered to 145–148 and merged; pick 32 (uniform slot) holds 149–151 on q-pick32). Next pick (33) is the rule slot (cycle position 1). Recheck all pushed branches before any ledger write.**
