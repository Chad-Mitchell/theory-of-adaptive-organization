# OPEN_WORK: every open item, one line each (rewritten, not appended)

**As of:** Friday 20 November 2026, evening ET (America/New_York), installed at the repository root by the hygiene PR. Earlier drafts of this page were revised from about 4:35 PM ET through the S5 Model-S rerun about 5:31 PM ET. `main` at the branch point is `a1a98aa` (PR #113 merged 2:33 PM ET; #115 merged as `1998a2d`, v2.66; #117 merged as `b12af70`, v2.67; #116 merged as `a1a98aa`, v2.68; CLAIM_MAP tally OPEN 84 / PROVED (in-model) 94 / MATH-CORRECTED 23 / PRIOR ART 32 / total 318; 118 tests).
**Rule:** an item leaves this page only when it is DONE (with a link to where it landed) or explicitly DROPPED (with the reason and who decided). Anything in flight that is not on this page is a bug in this page. `STATUS.md` says where the theory stands; this page says what is still open. Claim statuses stay in `measurement/CLAIM_MAP_v2.md`; this page links to rows and does not restate them.

**Gates:** `in progress` (work running) · `needs reviewer` (independent review owed) · `needs Chad` (a decision or an outside act; nothing outside the repo happens without Chad's go) · `needs data` (blocked on a source that is not open or not found) · `needs partner` (a lab, IRB or collaborator) · `parked` (deliberately paused; says what restarts it).

## 1. In flight (branches and PRs)

| ID | Item | State | Gate | Where |
|---|---|---|---|---|
| W1 | v2.7 robustness: CT37–CT40, CL18, CX7, CX8; ROBUST-SLACK prereg | **DONE.** Merged as `1998a2d`, CLAIM_MAP v2.66 | DONE | [PR #115](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/115), `theory/ROBUSTNESS.md` |
| W2 | EVO1 designed-world in-silico evolution test | Prereg locked `70fcbad`. Interim (not yet committed to this repository): PC, W1, W2 PASSED; W3 INVALID (ruin gate); W4 FAILED 3/8, W4b FAILED 8/8 (fitness valleys, see W10); S031, S07 PENDING. Cannot express bet-hedging (one design per genome). Runs, logs, diagnostics and analysis not yet committed | in progress, then needs reviewer | [PR #114](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/114), `tests/EVO1/` |
| W3 | v2.8 fractal structure / ht-index (N58–N63) | **DONE.** Merged as `a1a98aa`, CLAIM_MAP v2.68 (optimizer fix, N63 first numbers withdrawn and redone as arm D2, MF-DFA corrected, baselines, N60 "proved given convexity, numerical only") | DONE | [PR #116](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/116), `theory/HT_INDEX.md` |
| W4 | v2.9 dynamics: J_R, inaction band (CL19), amended kill rule (CT41), lineage bet-hedging (CT42, CL20), time average (CT43, CL21), CX9–CX10; Bode overreach for continuous observation, open for sampled reads | **DONE.** Merged as `b12af70`, CLAIM_MAP v2.67, after READY-WITH-FIXES. Confirm review was READY; the leftover "await confirmation" flag is dropped. CT41 is the lower-bound rule: non-move consistent if g < Δ_R(k_lo); miss if g > max(static band, Δ_R(k_hi)); INDETERMINATE between; NOT A TEST if the predicted gap of a non-mover is ≤ Δ_R(k_hi) | DONE | [PR #117](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/117), `theory/DYNAMICS.md` |
| W5 | Wide-net antifragility / optimal-design scan (source of W4; records the two OVERREACH verdicts: Bode "conservation of fragility", barbell) | **DONE** in this hygiene PR | DONE | `reviews/widenet_2026-11-20/` |
| W6 | Independent review reports for PRs #111–#117 (reviews 26–30 and the #113/#115/#116/#117 rounds) | **Partly done** in this hygiene PR. Committed: review 28 (`reviews/pr111_map_2026-11-20/REVIEW28.md`); PR #113 including the confirm round (`reviews/pr113_griddx_2026-11-20/REVIEW.md`); PR #115 round 1 (`reviews/pr115_robust_2026-11-20/REVIEW.md`); PR #116 (`reviews/pr116_htindex_2026-11-20/REVIEW.md`); PR #117 (`reviews/pr117_dynamics_2026-11-20/REVIEW.md`); core-page reviews of unmerged drafts (`reviews/core_2026-11-20/`). **Not found on the box, so not in the repository:** reviews 26, 27 and 29, and a #115 re-review. They remain cited only in CHANGELOG and CLAIM_MAP notes | residual: locate 26, 27, 29 and the #115 re-review, or leave the CHANGELOG note standing | `reviews/` |
| W7 | Synthesis: one core page and a reorganization | `CORE.md` and `core/KEYSTONE_NOTE.md` are drafted but not in this repository yet (pending a CORE PR). Piece 1 review: READY-WITH-FIXES (`reviews/core_2026-11-20/REVIEW.md`); both blockers applied in those drafts (CT41 restated as merged; pair-rule rescue removed). Confirm and re-confirm reports are in the same folder. Remaining should-fixes: §5 below. Re-confirm before a CORE PR merges | needs reviewer (piece 1 re-confirm, then pieces 2–8) | pending CORE PR |
| W8 | Merge order and numbering | Settled as: #115 v2.66 (done) → #117 v2.67 (done) → #116 v2.68 (done, `a1a98aa`) → #114 v2.69 (open) → this hygiene PR (no CLAIM_MAP bump; still v2.68) → CORE (next) → reorganization v3.0. The finishing plan that numbered hygiene as v2.70 is not in this repository | owner of each merge | this page |
| W9 | Keystone premise (N60: ε_K convex in K) and the predictive rhythm rule | The predictive keystone (layers from time scales, counted by degree) is numerically supported only in Model S, given convexity, which remains unproved; no counterexample after the optimizer fix, including the S5 rerun of the 120-world search with the merged #116 solver (120/120 convex at 10⁻⁴ and 10⁻⁶; N60 matches argmin on all comparisons with argmin ≥ 1; K*=0 hole 379/19320, as predicted; pending CORE PR, `core/keystone_checks/S5_RESULTS.md`). The 24 wide-search real-pole worlds still rest on the older solver; the #116 review was 39/40 (the 40th was the optimizer bug). In 𝓜_LG with rhythms: the increment formula is **false** (two oscillators, R = 3, formula 2, argmin 3). A pair-rule rescue predicts even K* and does not recover 3 (66/189). The only general rhythm statement is definitional: K* = argmin J, which equals the lower-convex-hull increment test for any ε_K sequence (pending CORE PR, `core/KEYSTONE_NOTE.md` §4, with the short proof). A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) is **OPEN** (T18). No pole-count or pair-count shortcut on the 189-comparison grid recovered it. N60 adjacent missed 17/90 non-convex cases. | needs reviewer (piece 2) | pending CORE PR, `core/KEYSTONE_NOTE.md` |
| W10 | EVO1 reachability finding | W4/W4b FAILED by fitness valleys (diagnosis D1–D2): selection found argmin J only where small steps reach it. A diagnosis, not a prereg patch; links to the keystone premise (convex = no valley in K) and to CT36/CL13 (complements) | needs reviewer (with W2) | `tests/EVO1/RESULTS_EVO.md` (interim; not yet in this repository; see PR #114) |

## 2. Repo hygiene owed now (found in the 20 Nov audit)

| ID | Item | Gate | Where |
|---|---|---|---|
| H1 | `STATUS.md` called v2.4 "an unmerged delta (PR #109)" and kept a stale "Next" list | **DONE** in this hygiene PR: the unmerged-delta line is gone; "Next" points here | `STATUS.md` |
| H2 | THEORY header and README said "v2.4 draft"; later merges already pointed them at v2.9 / CLAIM_MAP v2.68 on `main` at `a1a98aa`. This PR leaves those version lines (no CLAIM_MAP bump) and adds the missing #113 CHANGELOG entry (H3) | **DONE** (no new version number invented) | `THEORY.md`, `README.md`, `reference/CHANGELOG.md` |
| H3 | No CHANGELOG entry for PR #113 (v2.6-griddx), though it changed THEORY §3 (qualification gate) and the status words | **DONE** in this hygiene PR | `reference/CHANGELOG.md` |
| H4 | THEORY §8 "Where it stands" counted "15 field rows failed on proxy and 7 passed on proxy" | **DONE** in this hygiene PR: 30 NOT A TEST rows (10 passed on proxy, 20 failed on proxy), counted from CLAIM_MAP | `THEORY.md` §8 |
| H5 | ~~Per-row qualification-prospect notes missing~~ **False alarm, closed 20 Nov ~3:20 PM ET:** all 30 NOT A TEST rows on `main` carry a "Qualification prospect (reviewer judgment, not a verdict)" note (merged with #113, `1597218`; `grep -c prospect` = 32). The 20 Nov audit, and the message to Chad that called it a mistake, were wrong | DONE (nothing to fix; correct the record to Chad) | `measurement/CLAIM_MAP_v2.md` |
| H6 | `process/QUEUE.md` was listed as "live work" but its ledger stops at 19 Nov 12:57 AM ET; 62 of 117 items are not DONE and nothing since v2.1 went through it | **FROZEN** in this hygiene PR (banner added; content kept). The 62 not-DONE items are still in the frozen queue and have not been folded into this page line by line (S8 remainder) | `process/QUEUE.md`, `process/queue/items.json` |
| H7 | Q0 / SG-SCORE: the queue rule's locked prediction is owed a score (≥ 15 post-protocol outcomes). `sg_rank.py score` crashed with `KeyError: 'status_changed'` because ledger entry 156 recorded `claim_map_status_changed` instead | **Crash fixed** in this hygiene PR (`tools/test_sg_rank.py`). The official score is still owed: applying the Ace re-read of entries 65 and 171 (logged false, to be read as true) needs a `rule_change` ledger entry before the first official score. A mechanical dry run on the logged booleans (alias accepted) is reported in the hygiene PR | `process/queue/sg_rank.py` |
| H8 | README bullet: the s = ½ boundary wording (at s = ½, λτ\* = 1 at low SNR, equal, not faster); caption citation nit (both from review 29) | **Wording fixed** in this hygiene PR in README and in the matching THEORY sentence. The caption citation nit was not applied: review 29 was not found on the box (W6) | `README.md`, `THEORY.md` |
| H9 | Stale remote branches (listed below). Live work branch is only `v2.6-evo` (PR #114). `v2.7-robust`, `v2.9-dynamics` and `v2.8-htindex` are merged (their remotes were deleted with the merges). **Delete nothing**; deleting branches needs Chad. The 62 not-DONE queue items are not absorbed yet (H6) | needs Chad (deletion only) | GitHub branches |

## 3. Tests and theory still open

| ID | Item | State | Gate | Where |
|---|---|---|---|---|
| T1 | E. coli qualification check: σ (cost-to-growth), N_e, T_red from the literature, and name the lineage objective (W4's bet-hedging; persisters) **before** any rescoring | Not started; best candidate to become the first qualifying field test | in progress-able now | `theory/measured/ecoli/`, THEORY §3 |
| T2 | E. coli open arms: Y4 (adaptation time across conditions) untested; habitat mode (P16) open; nonlinear-motor objective untested | Prereg Y4 written, not run | needs data | `theory/measured/ecoli/PREREG_Y4.md`, CLAIM_MAP P15–P16 |
| T3 | Cross-grid comparison (GRID-DX Part C, P25) | Rank test UNTESTED: n = 1 grid with a full distance; Hawaii UNTESTED; AEMC and EirGrid sources MISSING (HTTP 403); no grid qualifies as scored | needs data (spectra), and a class with competing lineages | CLAIM_MAP P25, `theory/measured/grid/RESULTS_GRIDDX.md` |
| T4 | GRID-4b (P22) | UNTESTED: the lock needs 2019/20 MFR holdings; open NESO MFR holdings were found only from 2022-23 on, so it cannot run as locked; a re-lock on later years would be a new prereg | needs data / new prereg | `theory/measured/grid/PREREG_GRID4b.md` |
| T5 | GRID-DX Part B (P24): GB's three extra layers neither explained nor shown waste; the count under binding ruin was never derived | INCONCLUSIVE; needs the ruin-binding layer count (ties to W1 CX7) | in progress-able | CLAIM_MAP P24 |
| T6 | The killing tests N56 (layers match argmin J) and N57 (cost shares), and N13 SAME-SYSTEM-AQN | OPEN; no system has spectrum, stakes and upkeep measured (GAPS G1, G3; STAKES-PRECISION) | needs data | CLAIM_MAP N13, N56, N57 |
| T7 | Designed-world lab experiment (human tracking task ~100 participants, or E. coli F2/Y4 at a chemotaxis lab) | Specified; outreach draft kept outside the repo, unsent | needs partner + IRB, needs Chad | `theory/measured/SYNTHESIS.md` (end) |
| T8 | N48 cosmic-web matched-null hub test | Specified, not run | needs data (simulated halo mocks + a second survey) | CLAIM_MAP N48, `theory/COSMIC_WEB.md` §8 |
| T9 | C3b | Blocked: MV10 power gate not met | needs data | `reviews/night2/C3B_GATE_ADDENDUM.md` |
| T10 | SENSE-CELL-MATCHED (physics binding ratio, N24 follow-up) | Open | in progress-able | this page |
| T11 | Theorem P for drifting worlds (CX1) | Open math | in progress-able | CLAIM_MAP CX1 |
| T12 | CX2 co-adaptation (compete / collaborate / organize; system acts on its world). Bode / feedback limits apply here (CL11 → K17 is one case); dual control (act to learn) is the same open front and is **not yet named in the repo** | Open math; the most important open theorem | in progress-able | CLAIM_MAP CX2, K17 |
| T13 | Other open conjectures: CX3–CX6; CX7 (robust layer count, diversity against common mode; in W1); CX8 ROBUST-SLACK; CX9–CX10 (in W4) | Open | follows W1, W4 | CLAIM_MAP |
| T14 | K7 hormesis ("stress strengthens up to a ceiling"): the ceiling half has an in-model piece (CT25); "strengthens" needs an adaptation rule (W4's redesign-between-regimes result may supply it) | Open | in progress-able | CLAIM_MAP K7 |
| T15 | Layer-counting rule for real systems (by degree, distinct memory time constants): still a placeholder to finalize before any N56 test | Open | in progress-able | THEORY §3 |
| T16 | Whole-theory independent review, ideally by a human expert; every theorem has been refereed at most once, by the same bot family | Not started | needs Chad (who to ask) | THEORY §8 |
| T17 | The 78 other OPEN rows of the claim map | Open; untested, not refuted | see map | `measurement/CLAIM_MAP_v2.md` (tally) |
| T18 | Predictive rhythm rule: K* from the poles and the stakes, without first computing the whole ε_K curve | **OPEN.** The hull increment is the definition of K* (equals argmin J for any ε_K sequence), not a prediction from time scales. No pole-count or pair-count shortcut recovered K* on the 21-world grid (pair rule 66/189; odd K* in 123/189, including {3, 5} in 15; one light oscillator can have K* = 3 or 4; N60 adjacent misses 17/90 non-convex) | in progress-able now | pending CORE PR, `core/KEYSTONE_NOTE.md` §4, W9 |

## 4. Waiting on Chad (decisions and outside acts)

| ID | Item | State |
|---|---|---|
| C1 | X correction / map post: the live post (https://x.com/torusflow/status/2123631750223945917) is behind the theory (gate, map, robustness) | Draft text needs Chad's approval of the exact words; nothing posted |
| C2 | Outreach to a chemotaxis lab for T7 | Draft kept outside the repo, unsent; needs Chad's go |
| C3 | "Proposed law" label for the hypothesis sentence (now "The law of adaptive organization (hypothesis)"; CLAIM_MAP J3) | Awaiting Chad's decision |
| C4 | Explainer video | On hold (Chad) |
| C5 | EVOSIM | Parked; EVO1 (W2) is the live in-silico test |
| C6 | Branch cleanup (H9). The QUEUE freeze (H6) is done in this hygiene PR | Branch deletion still needs Chad |

## 5. Remaining should-fixes from the 20 Nov core review

Including the confirm-review items still owed: the **predictive rhythm rule** (T18 / W9, OPEN). The **S5 Model-S rerun** is done (pending CORE PR, `core/keystone_checks/S5_RESULTS.md`); convexity itself remains unproved and stays with W9.

The first review (`reviews/core_2026-11-20/REVIEW.md`) was READY-WITH-FIXES; blockers B1 (CT41 wording) and B2 (pair-rule rescue) are applied in the pending CORE drafts (`CORE.md` and `core/KEYSTONE_NOTE.md`, not in this repository yet). The confirm review (`reviews/core_2026-11-20/CONFIRM.md`) was READY-WITH-FIXES; blocker B3 (hull increment is the definition of K*, not a predictive rule) is applied in the same drafts. The re-confirm is `reviews/core_2026-11-20/RECONFIRM.md`. Should-fixes applied in this pass: S1 (drop stale #117 confirmation), S2 / S10 (K* = 0: cite CT21, "at most one layer"), S3 (fast/slow IDs are CT28 and CT34, with the latency premise), S4 (obsolete: #116 has merged as `a1a98aa`, v2.68; status lines updated), S6 (adversarial climb recorded as finished, max ε₂/ε₁ = 0.4625 / independent 0.461), S7 (section-O recount: 74 section-O rows, not 59 plus a double count), S8 staleness in W3–W5, W8, H1, H9, and the missing-§5 pointer. The rest, still open:

| ID | Item | State |
|---|---|---|
| S5 | Model-S rerun of the 120-world convexity search with the merged #116 solver and the reviewer multi-start. **DONE.** 120/120 convex at 10⁻⁴ and 10⁻⁶ (also on K=0..J); N60 = argmin in 18,941/18,941 comparisons with argmin ≥ 1; K*=0 hole 379/19,320 in 39 worlds, R ≤ 1.41; no E_K below E_∞; no counterexample. The earlier search had hidden a NaN world (seed 24) inside “0 violations”; that world is now clean and convex. Convexity remains unproved (W9). The local `stores.py` is still the pre-#116 copy; the rerun imported `theory/layers_checks/stores.py` under a unique name | **DONE.** pending CORE PR: `core/keystone_checks/S5_RESULTS.md`, `s5_rerun.py`, `s5_rerun.json` |
| S9a | Traceability: "Gate (#113)" was not a CLAIM_MAP id — now THEORY §3 / FRAMEWORK §9 | applied |
| S9b | "A missing cost kills the theory" is J16, not CT23 — split on the core page | applied |
| S9c | PLAN §0 "every sentence names a row ID or a file" — relaxed: load-bearing sentences, with pointers in §1–§2 | applied |
| S9d | N58's 1.0 vs 2.0 distinction — "under head/tail breaks 1.0" added | applied |
| S9e | Gerrard & Tsanakas 2011 booked mainly on CL18; CORE now says so | applied |
| S8 remainder | The queue is frozen (H6), but the 62 not-DONE items are still only in `process/QUEUE.md` and have not been folded into this page line by line | residual | `process/QUEUE.md` |
| S-plan | The pending CORE draft treats the predictive rhythm rule as OPEN and the hull increment as the definitional identity, not a candidate rule (B3). Piece 1 needs a re-confirm after these fixes, before a CORE PR merges | needs reviewer |

## 6. Stale remote branches (listed, not deleted)

Counted on Friday 20 November 2026 against `origin/main` at `a1a98aa`. Deleting any of these needs Chad. This page only lists them.

**Live (1):**

| Branch | Note |
|---|---|
| `v2.6-evo` | live; open draft PR #114. Do not delete. |

**Unmerged and superseded (5).** These tips are not in `main`; do not treat a delete as a no-op.

| Branch | Note |
|---|---|
| `n12-referee` | superseded by later N12 work; not merged as this tip |
| `wip/master-equation` | holds drafts not in main; superseded by `theory/MASTER_EQUATION.md` |
| `prereg/github-upstream` | superseded by later GitHub-upstream results on main |
| `q-pick15` | superseded by later q-pick work; a `q-pick15-merge` branch is already merged |
| `q-pick20` | superseded by later q-pick work; a `q-pick20-merge` branch is already merged |

**Merged into `origin/main` and still on the remote (102, `main` itself omitted).** Their remotes can be deleted once Chad says so. `v2.7-robust`, `v2.9-dynamics` and `v2.8-htindex` are already absent (deleted with their merges).

`audit-referee`, `audit-referee-fixes`, `bookends`, `checker-r6-r8`, `cold-read-fixes`, `core-claims-fixes`, `core-v2`, `core/v1.4.19-headline-scope`, `docs-eod-synthesis-2026-11-15`, `docs-v141-readme-status`, `docs/consistency-audit-2026-11-18`, `docs/public-scrub`, `docs/readme-author-line`, `final-should-fixes`, `front-door`, `github-times-fix`, `github-upstream-results`, `independent-review-2-2026-11-18`, `independent-review-lock`, `learnsim-prereg`, `learnsim-results-referee`, `lfk-spf-prereg`, `lock-pass-2026-11-18`, `lock-pass-date-fix`, `n12-referee-v2`, `n12-theory`, `night1-scoreboard`, `night2-audit-divergence`, `night2-measurement`, `night2-measurement-times`, `night2-referee`, `night2-self-prereg`, `prereg/vigil-ona`, `prereg/wikidata-band`, `q-pick-1150`, `q-pick10-aqn`, `q-pick12`, `q-pick13`, `q-pick14`, `q-pick15-merge`, `q-pick16`, `q-pick17`, `q-pick18`, `q-pick19`, `q-pick20-merge`, `q-pick21`, `q-pick22`, `q-pick22-merge`, `q-pick23`, `q-pick23-n16`, `q-pick23-n16-merge`, `q-pick23-n16-times`, `q-pick24`, `q-pick24-theory`, `q-pick25`, `q-pick26`, `q-pick26-theory`, `q-pick27`, `q-pick27-merge`, `q-pick28`, `q-pick28-theory`, `q-pick29`, `q-pick29-theory`, `q-pick30`, `q-pick31`, `q-pick32`, `q-pick32-theory`, `q-pick33`, `q-pick33-theory`, `q-pick34`, `q-pick35`, `q-pick35-theory`, `q-pick36`, `q-pick37`, `q-pick37-theory`, `q-pick38`, `q-pick38-theory`, `q-pick39`, `q-pick9-tlp`, `q-scale-ends`, `q-sensecell`, `q-sensecell-referee`, `queue-claim-q1q2`, `queue-pick4`, `queue-pick5`, `queue-pick6`, `reach-notes-2026-11-18`, `reach-open-items-2026-11-18`, `readme-post-arc`, `spectrum-map`, `spectrum-map-referee`, `spectrum-map-referee-timefix`, `spf-noise-proxy`, `telegraph-referee`, `telegraph-referee-times`, `theory-v1.4`, `v14-review`, `v141-fixes`, `v2.1-master-equation`, `v2.2-audit-fixes`, `v2.3-rules-centralize-phase`, `v2.4-ants-cx2-face`
