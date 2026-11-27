# Misses ledger, through 26 November 2026 (Forge)

*Written Thursday 26 November 2026, about 19:30 ET. Append-only from here. One row per miss or open miss: what was predicted or targeted, the lock (hash and where it lives), the score, the cause, and what it taught us. "Not tested" rows are process misses: the prediction was never scored. Labels: proved-in-model (PIM), observed, hypothesis (HYP). Paths under `rnd-2026-11-26/` are relative to `NOTES/rnd-2026-11-26/`. The status of record for any claim is `measurement/CLAIM_MAP_v2.md`.*

Counts: 58 rows. 42 research misses or open misses (§1 11, §2 13, §3 16, §7 2), 9 not-tested or process misses on locked tests (§4), 7 process slips (§5).

## 1. Locked tests in the repo (pushed locks)

| # | test | lock (sha256, commit) | score | cause | lesson |
|---|---|---|---|---|---|
| M1 | Composite contest (#253): composite beats rivals under the Hardy price | PREREG_4 in `theory/composite-contest-2026-11-24/` (`composite_contest_checks/SHA256SUMS`) | TIE under PREREG_4; WIN only with a hand-restricted Gmax | The win came from a restriction we chose, not from the cost | A win that needs a hand-picked menu is a statement about the menu |
| M2 | Two-route A-T2 (#287): memory heat falls with the world's copy gain (ρ ≤ 0.9) | `theory/two-route-2026-11-25/` PREREG `9e42fe0a…9e54` and successors | miss, +0.145 (ρ = 1.0453) | Memory heat rises with copy gain in Route A's world | The rival (RI, ρ = 1) was closer than our bar; size bars against the rival, not against hope |
| M3 | Two-route A-T1‴: sized Nash gap G ≥ 0.10 at three w_x | PREREG_4a `c9fb4fb9…c937` | boundary-hit open miss (best replies end on the ln γ = 5 box edge) | The search box, not the model, set the answer | Put the box edge in the prereg as its own outcome |
| M4 | Hutter Prize budget P2 (#290) | `501a82de…1a77` (`4a0d5e9`) | miss, +0.0192 | Record's allocation differs from the predicted share | Real-data bars need the measurement defined before the source is opened |
| M5 | Hutter Prize budget P4 | same | miss, ≥ +0.0141 | same | same |
| M6 | Hutter overall | same | open miss, not DATA-ONE; P1 hit only under the locked allocation fallback | The locked quantity (runtime RAM share) is not what the record exposes | Lock a quantity you can read |
| M7 | Who copies whom T1, two judges (#292) | PREREG_5 `b7850655…3e07` (run at `1816940`, lock `df114b6`) | clean miss ×5 (A ≈ 2e-8) | Identical judges that are each other's world have nothing outside to break symmetry | A mirror world selects nothing (fits X13's coupling reading) |
| M8 | Who copies whom T2, eight-judge ring | same | clean miss ×5 (0 of 8 edges broken) | same | same |
| M9 | QM-selection 1: a U(2)/Sp(1)×Sp(1) counterexample to the premise list | `c4a529c7…95f0` (`06f07e6`) | MISS: 0 hits, 0 ties | No counterexample exists in the range; the FIX36 review classes the run as a consistency check whose value is the proof | Ask before locking whether a miss can carry information |
| M10 | QM-selection 3: a body that ties or beats complex QT without the Jordan premise | `6137e3a1…e1b6` (`e496428`) | INCONCLUSIVE: 0 HIT, 0 TIE, 1 TARGET, 11 OPEN, 915 MISS | 11 bodies left OPEN by the locked decision rule | 80 minutes of compute bought a mostly-MISS table; open bodies need a pre-stated follow-up rule |
| M11 | Round 13-M H2 value: D² best Φ near zero at zero marginals | `35c19ee9…9e1b` (box lock, `rnd-2026-11-26/overnight/selfref/`) | sub-prediction miss (best Φ −0.233 at nonzero marginals, still < 0) | The optimum sits at nonzero marginals | Value predictions on optimizers need the location stated too |

## 2. Box-locked or pre-stated tests (hash logged before computing, not pushed)

| # | test | lock | score | cause | lesson |
|---|---|---|---|---|---|
| M12 | G3-1b: record-range intensivity in the random world | NOTE.md section `0575b2ea…2f05` (`overnight/forces-gravity/`) | failed as written (P1 all; P2/P3 Haar world; P4 small N) | The Haar world has no stable record range; the eigenstate world passes | A world that is random by construction tests nothing about records |
| M13 | G4-1: a horizon from capacity alone, basis-free | `504704d9…f8b` | open miss | Record modes have ~1/r tails, so there is no cut | A boundary needs a locality price; capacity alone does not give one |
| M14 | G4 H3: temperature–price link | same | failed (precision ceiling) | Design flaw: tolerance below attainable precision | Check attainable precision before locking a tolerance |
| M15 | G5 m = 0 reference ring | `419a6a68…d6` | setup miss (tolerance unattainable; the ring held 300 particles with a staggered zero mode, not 298) | Setup error | Recount the setup in the review, not only the result |
| M16 | PREREG_P: the cost selects a pure start | `a4e02d65…bb5d` (`overnight/entangle/`) | miss for cost-selection, as predicted (K0/K1/K3 tie; only K2, P restated, separates) | P is interpretive; the cost is indifferent | Entanglement through E1 needs P as a premise; say so plainly |
| M17 | PREREG_C: self-reference + completeness implies P | `b4208391…7b93` | weak form vacuous, strong form is P renamed | Renaming, not deriving | Test whether a new premise is a rename before running it |
| M18 | SR-b4 (P): a scale-free horizon weighting selects the disk | pre-statement in `stepback/SR_B.md` §9.0; logged hash `061c1d54…a16c` is SR_B before §9, not the block | open miss, PIM for every H ≥ 2 under both target rules | For every H some polygon is strictly cheaper at every T ≤ H | The weighting is our input; the disk was our target, not the theory's |
| M19 | SH-noise: noise alone gives one self-consistent record size n*(σ) | §6 block `917f7849…83f4` | MISS (no self-consistent polygon at 12–13 of 14 σ; repelling crossings) | Lifetime grows exponentially with resolution, so the loop overshoots; the scale n_c is "resolution ≈ noise" (KNOWN in form) | A self-consistency loop was our requirement (REQUIREMENTS_FIRST row 17) |
| M20 | SH-heat: the theory's keep/check/fade rule gives n*(σ) | §8 block `5011235d…f38b` | MISS, every arm (141 HIT-like / 294 MISS / 6 OPEN of 448 cells, but the HIT band's n* ≈ 4/x + 2 is set by the stake, not by σ) | The band makes the horizon a function of the stake | The selecting number came from the task; that turned out to be the finding |
| M21 | SH-read: a per-check price changes the overshoot into settling | §10 block `f1b738cb…ab74` | MISS, 1344 of 1344 cells | With any real read price every checked design outlasts every horizon it could serve | Prices decide which hold modes exist |
| M22 | Claim W: every free input reduces to the stake | same §10 block | false in-model: 11 of 14 inputs do not reduce; two PIM counterexamples (target rule; order of quantifiers) | Several couplings, not one scalar | I told Chad "everything reduces to w" an hour before this test; do not report a generalization before its test |
| M23 | WORLD_TRACK Step 0 secondary: α*·λ in [1, 3] | `645e5857…b105` | open miss, 0 of 24 (observed ≈ 10–25) | The heuristic held the (2T+2)-gon fixed; the best polygon moves to larger n | Heuristics that freeze the argmin are fragile |
| M24 | WORLD_TRACK Step 1 S3: regime crossover in ≥ 75% of rows | file hash after appending `ab799c39…6b0e64` | open miss, 5 of 8 rows | The tick (fastest look) binds in 150 of 432 cells | The fastest look is an input; it should be a measured sensor statistic |

## 3. Exploratory notes and reviews (no lock; misses found on paper or by a reviewer)

| # | item | where | score | cause | lesson |
|---|---|---|---|---|---|
| M25 | G2 R2.1: "record area scaling forced by cost" | `overnight/forces-gravity/HOSTILE_REVIEW_G2.md` | overclaimed; withdrawn | The bound was built into the MPS format; χ* bounded in N is a hypothesis | I told Chad at 01:03 that area scaling follows from the cost and corrected it at 01:14 |
| M26 | G2 R2.5 table | same | partly broken (missed Al-Safi–Richens Thm 1 coverage; "best Φ = 0" rows were product states) | Prior art not checked before the table | Check the obvious theorem first |
| M27 | Deriving entanglement (E1 chain) | `overnight/entangle/THREAD_SUMMARY.md` | open miss: reduces to premise P, not derived | See M16 | Stop a derivation thread once its residue is a premise |
| M28 | Step-back Draft D (C11, lead-time boundary) | `stepback/GATE_READ_STEPBACK.md` | gate FAIL; converted to a PIM lemma (upper bound only) | Outcome fixed by Lieb–Robinson plus the definition; input renamed, not removed | My own route scored 1.76/h before the gate read and 0.72/h after |
| M29 | Step-back Draft A (C2) and A2 | `GATE_READ_STEPBACK.md`, `GATE_READ_STEPBACK2.md` | gate FAIL (true by definition or set by parameter count; A2 "LT merges into P6" false as stated) | Relabelling, premise count unchanged | A redesign that only renames a premise is not a test |
| M30 | Step-back Draft C3 / C3v2 Arm 2 | `GATE_READ_STEPBACK2.md`, `stepback/LEMMA_R.md` | C3 gate FAIL; C3v2 Arm 2 theorem-fixed by Lemma R + RC15 (do not run) | Random composites are forced rigid by symmetry breaking | A paper lemma can make a run pointless; look for it first |
| M31 | C4 Draft C "fixed by theorem"; C4′ placement | `stepback/C4_RECORD_ORDER.md`, `review_c4/` | Draft C claim withdrawn (open miss in design); C4′ open miss (no repo cost acts on placement boost-invariantly) | The exponent, not the prefactor, is what Draft C measures | Name the observable the theorem constrains |
| M32 | C12c Lemma A(b) as first stated | `review_c12c/HOSTILE_REVIEW_C12C.md` | false as stated (2-point counterexample); restated as strong duality under convexity | Hull-vertex case missed | Test a lemma on a 2-point menu before using it |
| M33 | C12c: minimum bits under a chance cap | `stepback/C12C_ONSET.md` §11 | open miss | Class-A closed forms beaten by tail-flag memory | Closed forms in a class are upper bounds until optimality is shown |
| M34 | C12b: the Γ/r ordering of track vs keep | `stepback/C12B_ORDER.md` §9.1 | open miss in the stated form | Mixed a same-channel track class with a separate-leak keep class | Keep one carrier class per comparison |
| M35 | C1 SP layer test | `stepback/C1.md` | open miss 4/4; checkerboard reading and stationarity withdrawn | X shapes, not checkerboards; first-order condition holds on the addition side only | Look at the picture before naming it |
| M36 | C12CG chain: log₂N bits per record for odd N | `stepback/C12CG.md` §11(d) | open miss (pentagon ≈ 1.0204 bits > 1, total reading) | Intrinsic capacity differs from log₂N for odd N | Intrinsic facts matter for cost but do not select alone |
| M37 | C12c-G‴: nearest-vertex encoder optimal | `stepback/C12CG.md` §12 | not shown (Fourier bound 0.155 vs needed 0.1715); parked at ≈ 0.27/h | Missing cyclic-monotonicity lemma (HYP) | Park when value per hour falls below the next route |
| M38 | Compliant-mechanism structural collapse | `stepback/CLUE_COMPLIANT.md` | no collapse (growth objective absorbs ~3 of 16 parts) | The clue maps onto known pieces | A clue is a lead, not a result |
| M39 | Selecting the disk at all (SR-b, SH1) | `stepback/SR_B.md`, `stepback/SELF_HORIZON.md` §2.3 | open miss; SH1 (PIM): the disk is self-consistent only at infinite lifetime | The continuum appears only under an all-horizons quantifier | "Select the disk" was not in the theory's text (REQUIREMENTS_FIRST §1(b)) |
| M40 | SH-heat/SH-read hold-mode band as a design selector | `SELF_HORIZON.md` §§9, 11 | band conditional on horizon = one written state's life and Landauer-only restore cost; vanishes at a read price y ≥ 0.1 | Two readings we chose | List reading choices as inputs before computing |

## 4. Locked tests that were not tested (process misses)

| # | test | lock | what happened | lesson |
|---|---|---|---|---|
| P1 | Round 13-M H1 (I² ♦) | `35c19ee9…9e1b` | not tested: Q(√5) coordinates, float enumeration stalled on a loaded box | Exact arithmetic needs its own toy test |
| P2 | Round 13-M H2 (D² ♦) | same | not tested (same) | same |
| P3 | Round 14 H1 (icosahedron², vertex enumeration) | `523dfb53…7532` (`4e189c6`) | not tested: 120-minute timeout, exit 124 | Budget limits from a measured toy run, not a guess |
| P4 | Round 14 H2 (dodecahedron²) | same | not tested (same) | same |
| P5 | Round 14 H3 (I × D, exact facet-grid search) | same | not tested: 413 non-canonical "exact" classes vs 20 true values (`radsimp` non-canonical in Q(√5)) | Validate canonical forms before the search |
| P6 | Round 15 H3′ | `470bd905…8457` (`ed1ceef`) | not tested: crash (`AlgebraicField` has no `from_list`) before the search | Every helper exercised on toy inputs before the lock (adopted for round 16, which hit) |
| P7 | QM-selection 2 | `4cd2f0ea…4abd` (`641c695`) | not run: gate read FAIL (A1–A10) | A gate read before the lock would have saved a lock |
| P8 | Round 14 first launch | same as P3 | failed before Python ran (`/usr/bin/time` missing, exit 127), relaunched unchanged, logged | Check the launcher on the box first |
| P9 | QM-selection 1 lock push | `c4a529c7…95f0` | lock and result pushed together (02:49 ET); lock box-attested only | Push the lock before the run, every time |

## 5. Process slips (no score changed)

| # | slip | where recorded | lesson |
|---|---|---|---|
| S1 | Round 14 "clock stepped" explanation withdrawn (box pause hypothesis instead) | `theory/RECORD_COST_ERRATA_R1316_2026-11-26.md` | Do not explain a timing oddity before checking GitHub's clock |
| S2 | Rounds 15–16 run tree fetched from a local folder, not a fresh GitHub clone | same | Process rule adopted: launch only from a GitHub clone after `ls-remote` shows the lock |
| S3 | C12CG §8 "before computing" not verifiable (outputs 10:43, §8 says 10:45); §10 heading time wrong | `stepback/C12CG.md` §11 | Log the block's own SHA-256 and the time in the WORKLOG before computing (rule adopted 11:36) |
| S4 | SR_B §9.0 ordering not independently verifiable | `stepback/SR_B.md` §10.3 | Same rule |
| S5 | SELF_HORIZON "13:40" stamp was a planned time (actual ≈ 13:07); WORLD_TRACK header "18:35" vs actual 18:31 | WORKLOG 13:59, 18:31 | Stamp with the clock, never a plan |
| S6 | A WORKLOG line said 199f1e5 was pushed; the push had been skipped | WORKLOG 04:47 (correction line) | Read `ls-remote` before writing "pushed" |
| S7 | Gate read v5 of #292's PREREG_5 was not independent of its author | `theory/stop-copying-2026-11-25/RESULTS.md`; FIX36 review | Gate reads come from a fresh reviewer |

## 6. What the misses say together (hypothesis)

From `rnd-2026-11-26/stepback/REQUIREMENTS_FIRST.md` §5, after the P15 review (§10):

- Every number that selected a design on 26 November came from the record's coupling to something outside it: the medium's noise set scales, and the task (stake, price, ruin horizon, and whether the loss is geometric or operational) set points. With that coupling removed, the cost returns scales and tradeoff fronts, not a point, and a self-referential loop on the record alone repels or ties.
- Most afternoon misses (M18–M22, M39, M40) are the requirement "select without the world", which no line of the theory makes. That reading is close to true by construction of J, so it is not evidence for the theory; its testable content is which coupling sets which design feature, which WORLD_TRACK (M23, M24) began to test.
- The overnight physics misses (M12–M17, M25–M27) share a different cause: targets imported from physics (area scaling, horizons, a pure start) that the theory's text does not claim, and outcomes fixed by the inputs we chose.

## 7. Added at the snapshot (WORLD_TRACK Step 2, logged 19:05–19:08 ET)

| # | test | prereg hash | score | cause | lesson |
|---|---|---|---|---|---|
| M41 | WORLD_TRACK Step 2 INFO-BUDGET (CORE's OU class, Gaussian looks priced at the information they gain) | file after the pre-statement `ed403d82…30b4` (WORKLOG 19:05) | MISS by the pre-stated rule (B3 failed: R-regime slopes 0.337 and −0.288 vs [0.2, 0.3] and [−0.6, −0.4]); B1, B2 failed as predicted; B4 passed (63 cells, median 0.9999). Pre-stated p(MISS) 0.20. Observed | The primary configuration pinned the look interval at the sensor's limit s_min = 1 (432 of 432 cells), the same tick effect as M24. Post hoc (not a rescore): with u ≤ 0.1, or in the other 11 configurations, the slopes are the predicted ones | When a sensor limit bound in the previous step, do not make that limit the primary configuration of the next one |
| M42 | WORLD_TRACK §2.4 paper formula for nats per look | same | open miss: predicted ½ ln(1 + 2√c) = 0.245 / 0.549 / 0.996; observed ≈ ln(1 + 2√c) = 0.490 / 1.099 / 1.992 at c = 0.1 / 1 / 10. Not traced | A factor of 2 in the paper algebra | Check paper predictions numerically on one cell before the pre-statement is hashed |

Later results (WORLD_TRACK Step 3 STORED-PEAK, pre-stated 19:09 ET, p(HIT) 0.8; TRACKING_FIRST T1 BLANK-PRICE, pre-stated about 19:13 ET) were not scored at the snapshot. Their rows go in `INDEX-2026-11-27.md` §3.1 when they land.


## 8. Added after the 19:20 ET snapshot (26 November, late)

The count in the header (58 rows) is as of the snapshot and is not rewritten. This section adds two research misses and one unscored, pre-stated run.

| # | test | lock | score | cause | lesson |
|---|---|---|---|---|---|
| M43 | WORLD_TRACK Step 3 STORED-PEAK (unique stored-information peak across classes) | file after the pre-statement `084ea69e409645ba1a3a5069ff77a4bc99bb442adf465be9c86a33487779b473` (WORKLOG 19:09); results §3.6–3.14 `949aee6dd7df582f56f1e4fb37c9d12e3cbec229fb85410ea32b109c92ef2b01` at 20:01:48 ET | MISS (pre-stated p(HIT) 0.8 was wrong). U1 greater than 1% in G at c = 0 in all four configurations (12–52%), from flatness in the look interval; register s_min = 1, c = 0.1 was 1.39%, from adjacent integer s. U2 worst 96.8%. Continuous-look convexity: proved-in-model, elementary. Observed | Without a price per look the cost is flat in the look interval, so near-ties appear | A unique peak, even where it holds, sits inside W1/W2 (the world bounds a cost and does not produce a decision; only price ratios predict). The re-pose was dropped at about 20:05 ET for that reason |
| M44 | TRACKABLE_WORLD route A: which world properties are necessary for bounded trackers at finite cost | pre-statement block `a22962467bfb2b1df1c33d512a39cb783ab81bd86a7686b681a6fa9475f3fec6` (WORKLOG 20:18:37); file after results `7ad194c983f87382697fa0acc38d91ea871e8a5dc923b0dab5b85f3bbecdf9e2` (20:20:12) | MISS (pre-stated p(HIT) 0.10). Necessary in-class: finite drift, finite record lifetime, net positive inflow under an unbounded horizon; all known (Bialek, Landauer, ruin theory); the first two have price-set thresholds. Locality and a conserved quantity are not implied. Observed / proved-in-model (elementary) for the in-class rows | The necessary rows were already known; the route could not fail against the world (NEXT_ROUTES §5 R2) | Tracker existence gives only known information-theory and ruin conditions. This is the W15-reverse proposal. Necessity, not origin |
| U1 | TRACKING_FIRST T1 BLANK-PRICE | pre-statement at 19:13 ET, file `edd9bb00866cfd5d127d8b62c4921301929f23a83bd2680f6e6c65c484e3497f`; run log at 19:22 ET (`trackfirst/t1/t1_run.log`, complete 154-line `t1_run.jsonl` in the late folder) | not scored (paused) | Flagged beside W11 and W5 after the walls rebuild; likely failure is competitive exclusion, next to #292 | A pre-stated run is left unscored when the route is found to sit at a known wall; do not score it later without a new, written decision |

- M9 (27 Nov 2026): relabeled CONSISTENCY_CHECK per `theory/qm-selection-2026-11-26/RESULTS.md:36`; not counted as a research miss (count 42 → 41).

## 9. Corrections (27 Nov 2026; rows above unchanged)
- M2 lesson: RI's value is ρ_RI = 0.877 (inside the hit band), not 1 (`theory/two-route-2026-11-25/DEVIATIONS.md:12`); A-T2 did not separate the hypothesis from RI.
- M3 cause: the scored location is `model` (`RESULTS.md:38`); the box edge is where the solver saw it; the interior point at w_x = 2 is below the bar (G = 0.0654).
- M9: CONSISTENCY_CHECK, not a research miss.
- Scope: this ledger covers 25–26 Nov only and records misses only; hits and earlier misses are in each test's RESULTS/DEVIATIONS and the CLAIM_MAP headline ledger. §4–§5 process rows are carried into `process/FAILURES.md`: P5, P6 and P8 as `TOY-1`, P9 as `GATE-REPEAT-4`, S7 as `GATE-REPEAT-3`, and P1–P4, P7 and S1–S6 in the rows added 27 Nov 2026 that name their number here (`NOTTESTED-13M` to `PUSHCLAIM-1`).

## 10. Added 27 Nov 2026 (Lean memory rule, branch `lean-memory-rule-2026-11-27`)

| # | item | where | score | cause | lesson |
|---|---|---|---|---|---|
| M45 | GROK_BOT_MEMORY §4 per-item cost: one symbol `w` carries two units, and the public reply repeats it | `applications/GROK_BOT_MEMORY_2026-11-23.md:44-57, 69-70` as printed at `de15ab9` (corrected in PR #301); copies at `applications/MEMORY_MISS_COST_BOUNDS_2026-11-24.md:52-54` (corrected in PR #301), `NOTES/rnd-2026-11-26-late/stepback/TRACKABLE_WORLD.md:46` and `NOTES/rnd-2026-11-26-late/context/MEMORY_CHALLENGE.md:38` (hash-locked; errata note `NOTES/rnd-2026-11-26-late/ERRATA_M45.md`); public reply [2126422798096646198](https://x.com/i/status/2126422798096646198) | miss (units), found on paper while formalizing, confirmed by independent review (`reviews/pr301_2026-11-27/UNITS_REVIEW.md`). The printed reading is not consistent: under §4's own definitions the drift weight is forced to `a = w p / g²`. The printed worked example reverses (hold, not drop: 1.82 < 2). `T*` and the band carry the need rate: `T* = √(6kg²/(wpσ²))`, `b* = (6kσ²g²/(wp))^{1/4}`. The public reply's keep and band lines are wrong as stated (need belongs inside the root and in the band). Its role-bot √ line holds, assuming the same check cost and drift for the bot and the whole | §4 defines `w_i` as the stake on being wrong when the item is needed and `p_i` as the need rate, so `w_i p_i` is a loss per unit time; the drift term `w_i σ_i² T_i/6` used `w_i` as a loss per unit squared gap per unit time, the meaning of `w` in `theory/LAYER_LIFETIME_2026-11-21.md:38`. No check reads units, and the formula went public without one (`process/FAILURES.md` `UNITS-PUBLIC-1`) | Check the units of every symbol in an application before a formula goes public. The Lean theorems take a separate drift weight `a`; `fixed_hold_rule`, `printed_example_flips` and `corrected_example` (`formal/lean/GTAO/MemoryRule.lean`) check the corrected rule and both examples |
