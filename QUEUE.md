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

### Q10. ONA-MORE (rule rank 10, I = 0.04)
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
- **SPECTRUM-BRIDGE-SIM lock** (Q5 now unblocked): lock predictions from SPECTRUM_MAP (read elasticity 1/α for both estimators; K\* = 1 in OU, rising with log-span otherwise (referee: lock the continuous form, one store iff ψ·0.14(α−2)² ≲ 1, not the α = 2 knife-edge); kernel sign flip at α = 2).
- **PRIORART-LFK-ALPHA** (w 2). Forward citations of LFK 2024 and Afterman et al. 2022 for any statement of τ_m ∝ τ_E^{1−1/α}. **Largely covered by SPECTRUM-MAP-REFEREE §5:** the scaling is published in substance, and α = 2 is in Mora & Nemenman 2019. Remaining: full texts of the 6 LFK citers, Afterman/Kleptsyna citers, PLL/clock-steering loop-bandwidth literature, Scholar.
- **D3-DISCRIMINATE** (w 2, untested; new from referee R6/R7). Design and lock a statistic that separates renewal from Cox event worlds at β ≈ 0.2 (e.g. Δβ/β_orig calibrated on simulated renewal and Cox worlds matched to each repo's gap marginal, or a conditional-intensity test on lagged event counts). Show power on synthetic controls before running real repos.
- **SPECTRUM-MAP-FIXES** (w 1). Apply SPECTRUM_MAP_REFEREE §8 items 1–8 to `reviews/night2/SPECTRUM_MAP/README.md` (as a dated erratum block; locked files untouched).
- **PRIORART-SCHOLAR** (w 1). Google Scholar gap of Q1 (only via a sanctioned route; no sign-in).

### NEW (15 Nov ~10:00 AM ET, from THEORY v1.4; surprises read per rule 4)
- **ONSET-SPECTRUM-FREE-REFEREE** — DONE 15 Nov ~10:30 AM ET (pick 3, unaided slot = rule top; ledger 22–25): `reviews/night2/N12_REFEREE.md`. **CORRECTED (narrowed).** Onset exponent −1 (exact reset reads; also entropy pricing) and −(1+θ) (priced precision) confirmed at every α > 1 (wider than 1 < α < 3); the reason is degree-1 homogeneity of linear MMSE. Corrections: C1 noisy reads → −2 at small ρ with α-dependent crossover; C2 same-α premise (priced precision needs α_g − α_u < 1); C3 vigilance ρ^{−θ} only in spend units (ρ^{−1} in precision); C4 vigilance growth N^a, mixed e_u and constants depend on α (confirms V14_REVIEW). Novelty low (elementary corollary; not found stated). THEORY §2.5 / CLAIM_MAP N12 edits in a separate PR, **not merged** (v1.4.1 worker owns THEORY).
- **ONSET-NOISY-READS** (w 2, c 1; from N12 C1). Closed-form crossover ρ_c(α, σ²) and proof that noisy reads put the level in the θ = 1 class as ρ → 0; how an N2 test classifies the level's technology.
- **MIXED-ALPHA-ONSET** (w 2, c 1; from N12 C2). Prove the α_g − α_u < 1 condition and the Δ > 1 exponent −(1/Δ − b_g)/(1 − a_g).
- **EFFORT-UNITS-ERRATUM** (w 1, c 0.5; from N12 C3). Lemma 1(viii) holds only at θ = 1; dated erratum and vigilance-row units.
- **AQN-ESTIMATORS** (w 2, c 1.5). Estimators with CIs for α over a stated band, q and N from a noisy series, plus event-world versions; validated on synthetic fBm+noise, Cox and renewal truth before any lock. *Why:* the open bet (N13) needs all four inputs measured on one system; no estimator is validated (§11 process item "dry-runs on synthetic truth").
- **SAME-SYSTEM-AQN** (w 3, c 4; after AQN-ESTIMATORS). First test of N13: on one real system measure α, q, N, stakes and one design quantity (read rate, memory time or store count); lock the §2.2 prediction against fixed-budget-share and universal-½ rivals. Candidates: SPF (with LFK-ALPHA-SPF), VIX (VIX-KERNEL), E. coli (SENSE-CELL). Regime measured first.
- **ONSET-ACROSS-ALPHA-SIM** (w 2, c 3). Non-circular learners (LEARNSIM harness) in fGn worlds at two α values with one technology. Locked prediction from N12: onset exponent unchanged (−1 reset; −2 linear precision price). In-model only.
- **KERNEL-MEASURE** (w 2, c 3). Every earlier memory test measured a need hazard, never a tracking kernel (§2.2). Measure a response kernel on one system with α measured on its driver; predict survival exponent α/2 and the sign flip at α = 2. Overlaps VIX-KERNEL.
- **FROZEN-DOC-POINTERS** (w 1, c 0.5). One-line "superseded by THEORY v1.4 §2.2" pointers in frozen files that still state slope 1 or (log-span)^{2/3} (`litmap/LEFT_ON_THE_TABLE.md`, `theory/THEOREMS.md`); no content edits.
- Note on **SENSE-CELL**: by §2.5 the physics matters through θ, the price exponent of precision; measure θ and the binding ratio together.
- Note on **SPECTRUM-MAP-FIXES**: item 1 ("whatever linear predictor") applied in the v1.4 PR; items 2–8 remain.

**Pick 3 taken (ledger 24). Next pick (4) is the uniform slot: top of entry 23's stored uniform permutation (SAME-SYSTEM-AQN), or log a fresh ranking first.** Old note: log a fresh unaided order covering the items to be ranked, run the rule, then take the unaided top (rule's if the same).

### NEW (15 Nov ~11:05 AM ET, from SPF-NOISE-PROXY; surprises read per rule 4)
- **SPF-NOISE-PROXY** — DONE (pick 4, uniform slot; ledger 26–28, outcome 31): `tests/SPF_NOISE_PROXY/RESULTS.md`, lock `2f96b41`. Validated N proxy L0w (within-forecaster nowcast dispersion over the environment-implied variance; passed on synthetic truth). LFK's h = 3 dispersion-as-N **failed on proxy "horizon overidentification"** for 6 of 7 variables; contamination broad (T2 inconclusive); L0w passed known-groups marginally (T3). Post hoc: LFK S-a was an artifact; with measured noise the optimal filter under-predicts consensus CG 2.5–6×. No CLAIM_MAP change.
- **SPF-RIGIDITY-OOS** (w 2, c 3). Lock "consensus CG > optimal-filter β at measured nowcast noise" on unseen surveys/variables (ECB SPF, Livingston, other SPF variables); power first.
- **NOISE-PROXY-REFEREE** (w 2, c 1). Hostile referee of the finite-sample bias, the L0w selection and the G test; audit other dispersion-based N.
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
- **REGIME-C-GAUSSIAN-PREMISE** (w 2, c 0.5). Regime C's model size ∝ Q^{1/β} is reverse water-filling, exact for Gaussian modes; check whether it is Gaussian-only or an upper bound otherwise, and propose scope text.
- AQN-ESTIMATORS note: for a Bayes optimum in a jump world, q alone is useless (364× spread at fixed q); estimate λ and μ separately (weak evidence; no LR change).

**Pick 10 done (ledger 56). Next pick (11) is the unaided slot: log a fresh unaided order, run the rule, take Ace's unaided top (rule's if the same). Next free ledger entry: 57.**

### NEW (15 Nov ~1:45 PM ET, from AQN-ESTIMATORS; surprises read per rule 4)
- **AQN-ESTIMATORS** — DONE (pick 11, unaided slot; ledger 57–59, outcome 61): `measurement/estimators/RESULTS.md`, lock `3595c48`. Validated on synthetic truth: Whittle α, q, N (SE(α̂) ≈ 1/√M, M = frequencies below the noise crossover; ±0.1 needs M ≈ 400); corner check; HMM λ, μ, N, t_A (≳ 16 switches; SE(log λ̂) ≈ 1/√switches); premise LR (size ≤ 0.05, power 0.93–1.00); event worlds (Poisson floor, renewal flags); stakes only from exogenous error. DFA biased low under noise. Demo on proxy: DGS10 α̂ 2.00 ± 0.03 (random walk), log VIX regime not established. CLAIM_MAP N18 (DECIDED, method); no status change. Edits E-A1–E-A5 proposed, not applied.
- **AQN-REFEREE** (w 2, c 1). Hostile referee of the estimators, validation, label rules (R1 gap at α ≈ 2 without a corner) and E-A1–E-A5.
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


### NEW (15 Nov ~2:58 PM ET, from HEADLINE-PREMISE-APPLY; surprises read per rule 4)
- **HEADLINE-PREMISE-APPLY** — DONE as a PR, **not merged** (pick 13, rule slot, I = 3.2, tied with REGIME-C-GAUSSIAN-PREMISE and taken by id order; ledger 66–68 + outcome): `reviews/night2/HEADLINE_PREMISE_APPLY.md` (check in `HEADLINE_PREMISE_APPLY_checks/`). THEORY v1.4.4 / CLAIM_MAP v2.14 on branch q-pick13: P1–P8, the V143 F2 learner-class qualifier ("What changed" item 2, §10 LFK) and the line-6 CLAIM_MAP pointer. Applier tightenings T1–T5: keep hold-last-value in the reset-read premise; name only the derived jump-world exponents (adaptation time, error), with reset reads and the regression kernel unaffected; extra inputs only where the locked optimum is Bayes for a non-Gaussian world; a prereg naming no optimum is scored against the best linear one, in the causal form too. No status change. Own second hostile pass recorded; it does not satisfy Chad t1916.
- **HEADLINE-PREMISE-REVIEW** (w 2, c 0.5). A separate independent reviewer reviews the PR (sources, T1–T5, hostile pass) and merges or requests changes.
- Surprise read: none beyond the proposal's; the one design gap found (the lock would have excused tests locked before v1.4.4) is fixed in the text (T4), not a new item.

**Pick 13 done (outcome logged after the PR opened). Next pick (14) is the rule slot: log a fresh unaided order, run the rule, take the rule's top among open non-active items.**

## Done (frozen)
- HEADLINE-PREMISE-APPLY: `reviews/night2/HEADLINE_PREMISE_APPLY.md` (THEORY v1.4.4 PR, not merged; HEADLINE-PREMISE-REVIEW queued).
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
