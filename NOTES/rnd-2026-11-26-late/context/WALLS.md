# WALLS: earlier attempts to connect information and physics, and where each stopped

*Built 26 Nov 2026, about 19:15–19:29 EST, from primary records only: a fresh clone of `Chad-Mitchell/theory-of-adaptive-organization` main at `8b553c641a333e6ddfb8b0789f8808fa2400677a` (in `/workspace/gtao-fresh/repo`), the GitHub REST list of PRs #1–#295 (bodies saved in `/workspace/gtao-fresh/prbodies/`), our notes under `/workspace/gtao-notes`, the Ace email thread "Re: GTAO open PRs" (`c9017c80…`, last 50 of 88 messages saved to `/workspace/gtao-fresh/ace_thread_50.txt`), and Chad's public posts on X. Local note; nothing committed, pushed, posted or emailed.*

**Labels:** observed (a record says so, or a script printed it) · hypothesis · proved-in-model (PIM). "Re-hit today" means a 26 Nov route ran into the same wall, and the 26 Nov note does not cite the earlier record.

**What could not be read.** Transcripts of this bot's earlier sessions and of other bots (Atlas, El Capitan) were not reachable: `SearchTranscripts` returned "no record" for this run and refused the ids tried. The Ace message of 24 Nov 04:39 UTC (`14229820`, "I stepped back over the whole physics line tonight, at Chad's request …") is older than the 50-message read limit. Only its search snippet was read, so its content is **not** used below. Walls that Chad and Ace hit in chat but never wrote into the repo or notes are missing from this file. That gap is real.

**Today's five findings, checked against every wall** (sources in `WORKING_CONTEXT.md` §2):
- F1: the world (the task: stake, price, ruin horizon, form of the loss) sets the design points.
- F2: the medium (noise σ, leak Γ) sets the scales.
- F3 (narrowed by `rnd/review_worldtrack/REVIEW_WORLDTRACK.md` §0, §6, §8): only J ∝ σ_w√x is shown to carry across the register and Gaussian classes, and that scaling is CORE.md:91's own limit (ELEMENTARY, known). "The selected object is a stored-information budget that survives a change of class" is a **hypothesis**, contradicted for ideal coding (Kipnis–Goldsmith–Eldar, per the review). Step 2 INFO-BUDGET scored a MISS: with no per-look price the look rate sits at the sensor limit s_min (WORLD_TRACK.md:442–522; REVIEW_WORLDTRACK §11).
- F4: a supply of low-entropy (blank) cells cannot be dropped (TRACKING_FIRST.md:74, :300).
- F5: the core leans on thermodynamics in its displayed cost, and much less in its structure (TRACKING_FIRST.md:37; T0 audit HIT, TRACKING_FIRST.md:394; WORKLOG.md:302).

---

## W1. Physics bounds the cost; it does not produce it
- **Tried (22 Nov, PRs #175–#181):** whether the physics of a memory that stores a model and acts forces the cost's terms. `theory/INFO_PHYSICS.md:17`.
- **Wall:** only a floor is forced. "The information flow is a lower bound on that heat … Ruin and linking stay outside. The master equation is not this cost." (`INFO_PHYSICS.md:19`). §6 (`:212–222`) lists what is not forced: separate acquisition, linking, the ruin cap, the gross stock, a constant upkeep per layer. §9 (`:372–385`): physics cuts the feasible set; the weight w, H3, the coordinates and the linear prices stay assumed (`:374`, paraphrased). `CORE.md:23`: "It bounds a heat. It does not choose a stake, a link price, or a ruin cap." `CORE.md:29`: "Temperature does not set \(w\)."
- **Why:** dissipation inequalities are bounds on a heat. They contain no reserve, no loss and no exchange rate to a task.
- **Today:** **re-hit.** SH-heat found that the selected design is set "by **x alone**" (the stake; `SELF_HORIZON.md:533`, :562). Claim W (`SELF_HORIZON.md:668–690`) tested whether every free input reduces to w. REQUIREMENTS_FIRST's compressed truth (`REQUIREMENTS_FIRST.md:174` onward) is this wall stated again. None of the four 26 Nov stepback notes cites `INFO_PHYSICS.md` (grep count 0, except WORLD_TRACK for the OU formula). F1 confirms the wall in a new class; it does not move it.

## W2. Prices are free; the theory predicts only through price-free structure or measured prices
- **Tried (21 Nov):** `theory/PRICE_FREE_2026-11-21.md` and `theory/REVEALED_PRICES_2026-11-21.md`, after field tests stalled on prices (h, w) that could not be measured independently of the design.
- **Wall:** "J has free prices, so it predicts only through price-free structure or independently measured prices" (`PRICE_FREE_2026-11-21.md:7`). THEORY.md:36: "only dimensionless ratios matter". THEORY.md:71 (the principle's scope). "Stakes w have never been measured validly" (the retired STATUS.md, as quoted at `PRICE_FREE_2026-11-21.md:24`).
- **Why:** the cost is a sum of priced terms. Its minimizer depends on price ratios, and the theory supplies none.
- **Today:** **re-hit.** F1 ("the world sets the point") is this wall. REQUIREMENTS_FIRST §5.2(ii) relabels "chosen" as "world-set", which is the repo's existing position (THEORY.md:35, :197). Neither PRICE_FREE nor REVEALED_PRICES is cited in today's notes (grep count 0). F1 adds nothing to the wall except one more class where it holds.

## W3. The cost presupposes a system, a world, a bath and a temperature
- **Tried (23 Nov):** the physics reading in `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176` ("a face of how physics itself keeps records"), and PHYSICS_CHAIN Level 4: "Physics as the minimum-cost way for a universe to keep track of itself (SPECULATION)" (`theory/PHYSICS_CHAIN_2026-11-23.md:90`).
- **Wall:** "The cost, as written, already assumes a system, a world, a bath, and a temperature." (`FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176`.) PHYSICS_CHAIN keeps Level 4 as SPECULATION (`:90`).
- **Why:** each floor's class premise (local detailed balance, the Einstein relation; `CORE.md:70`) is physics put in.
- **Today:** this is the wall Chad's 26 Nov message (t168u) points at, and TRACKING_FIRST is aimed at it, but TRACKING_FIRST does not cite `FREEZE_OR_HOLD_FLOOR:176`. **F5 and F4 narrow it** (hypothesis): energy and kT look removable as premises, because kT enters designs only through price ratios (T0 HIT). The world, the system and the blank supply remain. That is a sharper list of what stays presupposed. It is not a removal.

## W4. Every physics link borrows physics; the inversion "the cost of a distinction is the primitive, and k_B is a conversion factor"
- **Tried (25 Nov evening, with Chad):** `rnd/SESSION_NOTES.md:4` ("every physics link borrows physics as input (Landauer heat floor, k_B, hbar set by hand), so deriving physics back is circular"). `:5`: "Inversion (Chad): make the cost of keeping a distinction the primitive. Landauer then becomes how that cost shows up in our units; k_B is a conversion factor." `:15`: working claim, "the constants are the exchange rates that keep that pattern consistent" (hypothesis). Also on main (24 Nov): `theory/constants-exchange-2026-11-24/MEMO.md` (T70). "The cost alone is dimensionless … Once the cost is coupled to physics, dimensional constants may enter as exchange rates" (`MEMO.md:5`). The tracking floors carry only k_B; ħ, c and G enter only through imported ceilings (results table).
- **Wall:** the routes that followed (no-cloning, composition, self-reference) reached synthesis-level results under stated premises (W10). No route produced a constant's value.
- **Today:** **re-hit, close to verbatim.** TRACKING_FIRST §1.2 drops kT and keeps "the counting form" of Landauer's bound (`TRACKING_FIRST.md:55–60`, table row at :60). That is SESSION_NOTES:5 again. The T0 audit's HIT ("kT enters designs only via price ratios") repeats T70's result. TRACKING_FIRST cites neither SESSION_NOTES nor T70 (grep count 0). The parent's message to Chad presented this as a new direction.

## W5. "Temperature is the price of information" is already established as a form, not as a physical value
- **Tried:** the selection temperature π ∝ e^{−βJ} (`CORE.md:122`; `core/bridge_2026-11-21/SELECTION.md`; PR #122, T27, official result FAIL on P3, the low-β mass floor). The credits at THEORY.md:195 (rational inattention, Ortega & Braun). Overnight 25–26 Nov: forces-gravity G2, "KNOWN, applied: exp(−β·cost) from the selection price D(s‖p0)" (`rnd/forces-gravity/THREAD_SUMMARY.md:7`), and G3-2's Gibbs identity F_K(ρ′) − F_K(ρ) = T·D(ρ′‖ρ). STEPBACK §1a, 26 Nov 06:16 (`rnd/stepback/STEPBACK.md:17`, row T2): "This is the 'temperature = price of information' identity, and it is established."
- **Wall:** it proves a form, not a value. "It does **not** fix the *value* of any physical temperature" (`STEPBACK.md:21`). The Gibbs form follows only **given** a KL selection price, linear cost and uniform p0; a χ² price gives a linear form (`THREAD_SUMMARY.md`, hostile-review correction 3).
- **Today:** **re-hit risk, high.** The parent's reply to Chad (t172) said a temperature-like price "should appear on its own" and that this is "exactly what the tracking-first work is testing". The form is already in hand. TRACKING_FIRST knows the relabel risk (`TRACKING_FIRST.md:29`) and requires Z0 under selection, not a planner. But it does not cite G2, G3-2 or STEPBACK §1a. T1 BLANK-PRICE adds nothing unless O3 (Z0 under selection) and O6 (a non-relabel prediction) both hold.

## W6. A physical (modular or Unruh-type) temperature from a capacity price
- **Tried (25–26 Nov overnight, preregistered G4 and G5):** does a per-site capacity price κ set a lattice vacuum's modular temperature, T_c ∝ κ^{1/2} (`rnd/forces-gravity/THREAD_SUMMARY.md` rows G4 and G5; `STEPBACK.md:19`)?
- **Wall:** open miss. Basis-free capacity pricing makes no horizon (`THREAD_SUMMARY.md:43`). "T_c ≈ c/R is not something the cost supplies" (`:48`): the cost supplies only a stopping radius R(κ), and the step from R to T is the vacuum's (Bisognano–Wichmann, an input). What stays input: locality, the vacuum, relativity, T = a/2π, G.
- **Today:** not re-run. TRACKING_FIRST's O5 ("reduces to kT … a consistency check") would meet the same wall if pushed to a value.

## W7. The arrow of time comes from a blank-memory boundary
- **Tried:** SESSION_NOTES:7 ("arrow of time from record bookkeeping", 25 Nov). Forces-gravity G1 (overnight): "PIM: Page–Wootters record formation orders clock ticks; the direction comes from the blank-memory boundary" (`THREAD_SUMMARY.md:6`).
- **Wall:** the low-entropy boundary is an input. Nothing produces it.
- **Today:** **re-hit; the same finding again.** F4 (TRACKING_FIRST §5 H2, `:300`: "the low-entropy source is physics in disguise") is G1's conclusion, reached again without citing G1. Today's version adds one thing: the source cannot be dropped under P-rev and P-leak (`:324`). The parent reported it to Chad as new.

## W8. Holography and the area law
- **Tried (22–23 Nov):** PR #184 ("No non-metaphorical holographic structure in the heat floor"); T41 and T42 (`theory/HOLOGRAPHIC_2026-11-22.md`, `theory/HOLOGRAPHIC_MEMORY_2026-11-22.md`); T44; T62 (`theory/AREA_LAW_PROBE_2026-11-23.md:11–17`); T63 (`theory/RECORD_REPAIR_FLOOR_2026-11-23.md`); T67 (`theory/LEARNING_RATE_THRESHOLD_2026-11-23.md`, MIXED, 3 of 4 cells EQUAL).
- **Wall:** the area always came from a physical input (boundary channel capacity, shed flux q, hoop, localization), never from the cost. Frozen storage costs zero ongoing heat, so it packs by volume (`AREA_LAW_PROBE:11–15`). Classical self-correcting media evade T63's cap in 2D and 3D (`PHYSICS_CHAIN:70–72`). T67 came out MIXED and supplies no new constant (`PHYSICS_CHAIN:109`, paraphrased). The cost contains neither G, ħ nor c (`PHYSICS_CHAIN:77`, citing `AREA_LAW_PROBE:17, 135`). Ace, 25 Nov: "T62, T63, T64, T65 and T67 each got the area from physical inputs (shed flux, hoop, localization), not from the cost" (email `14924942`).
- **Today:** not re-run. F2 fits the wall: scales come from the medium.

## W9. Gravity, the Jacobson step
- **Tried:** T64 (`theory/GRAVITY_BARRIER_PROBE_2026-11-23.md`), T65 (`theory/BARRIER_MASS_FIELD_THEORY_2026-11-23.md`), T66 (`theory/TRANSPORT_BARRIER_2026-11-23.md`); PHYSICS_CHAIN Link 3d (`:82–85`).
- **Wall:** a barrier costs gravitating mass only under input A1, which fails in the destruction channel and stays open in the transport channel. The Unruh floor reproduces the known Bekenstein-plus-hoop route; the Hawking floor is circular (`PHYSICS_CHAIN:105–107`). Ace's ordering (email `14924942`): a Jacobson step comes last, because "T64 and T65 already showed that the naive versions rename a cutoff or assume area scaling."
- **Today:** not re-run.

## W10. Quantum records: selected only under a drift premise, and the stake decides at zero drift
- **Tried (24–26 Nov):** T71 (information causality, relabel, PR #250); T73 and T74 (`theory/QUANTUM_RECORD_PRICE_2026-11-24.md:9`, "No unique quantum-record price"); T75 and T76 (#257: ratios 0 and 1 are boundary fixed points, and the ratio is set outside the cost). No-cloning, composition and self-reference (`rnd/SESSION_NOTES.md:18–60`). RC1 and RC2 (`theory/RECORD_COST_CHAIN_2026-11-25.md`, merged #294).
- **Wall:** "cost selects quantum-like records under drift", and "Without drift …" (`RECORD_COST_CHAIN:13`, :92). The stake is a convention: "The stake \(q=4\) is the session's convention, not derived" (`:62`). Open miss 1's next test: "Compute the stake \(q\) strongly selected systems face" (`:92`). "Polygons pay an irreversibility cost the disk does not" (`:13`, S3) rests on definitions NA3 and NA4 ("The disk pays 0" is a definition, `:75`).
- **Today:** **re-hit.** The whole SR_B, SELF_HORIZON and C12CG line (disk against polygons) continues S3 and open miss 1. Its result, "the stake decides, and the theory does not set the stake" (SH-heat), is open miss 1's existing diagnosis. P15 (no polygon beats the disk under one fixed angle-only loss, with ties common) is new in-model content (REVIEW_P15 PASS-WITH-FIXES). The stake wall stands.

## W11. Closure: judges that are each other's world or bath
- **Tried (25 Nov):** Ace's framing (email `15079233`, 25 Nov 13:08 EST, thread file line 604; paraphrased): every bridge on main takes the world's rules, its bath and its temperature as inputs, so the cost can only re-price them; the part that goes past information theory is closure, where judges are each other's bath (BICAUSAL). #287 Route A: A-T2 open miss of +0.145 (PR #287 body); A-T1‴ open miss at a boundary. #292 who-copies-whom: "identical judges … do not break symmetry (T1 A ≈ 2e−8, T2 0 of 8 edges, clean miss)" (`REQUIREMENTS_FIRST.md:150`, citing `theory/stop-copying-2026-11-25/RESULTS.md` on the PR branch). Its paper check already leaned to a miss (PR #292 body).
- **Wall:** a mirror world gives no outside coupling to break symmetry, so the cost picks nothing asymmetric.
- **Today:** **partial re-hit risk.** TRACKING_FIRST T1 BLANK-PRICE (several trackers on one blank pool, looking for a common price under selection) is a closure-type model. Its named likely failure, competitive exclusion (`TRACKING_FIRST.md:246`), sits beside #292's symmetric result. TRACKING_FIRST lists #292 as a requirement (`:199`), not as a wall to design around.

## W12. Selection and growth rank designs; they do not produce the cost
- **Tried:** `theory/GROWTH_BRIDGE.md:259` ("The master equation is not derived, and it is not derived in either limit"); Lemma LY (`CORE.md:31`: it "does not choose the vector"); T27 (#122, FAIL on P3).
- **Wall:** growth on a gapped menu recovers a ranking, and the term list stays an input.
- **Today:** **re-hit risk.** REQUIREMENTS_FIRST Route 2 KELLY-TRACK and TRACKING_FIRST T2 SELECTION-PRICE (persistence as the currency) head toward this wall. Neither cites GROWTH_BRIDGE (grep count 0). The cost's term list will not come out of growth; at most w gets replaced by a payoff structure, which is REQUIREMENTS_FIRST's own reading (`:230`).

## W13. Self-reference and self-consistency: the input moves; it is not removed
- **Tried:** SESSION_NOTES:26 (Chad, "another path, between the walls"); RC open miss 5 ("Self-reference alone does not force no-cloning", `RECORD_COST_CHAIN:96`); S9 ("True in classical probability too", `:43`). Today: SELF_HORIZON's horizon fixed point.
- **Wall:** a self-referential condition is either a tautology or needs one outside parameter (SELF_HORIZON §0 item 2, `:8`). "the input moves; it is not removed" (SELF_HORIZON §0 item 4; again at `:73`).
- **Today:** the same structural wall as RC open miss 5, met again in the horizon setting. Persistence as the stake (the SELF_HORIZON reframe) was already SESSION_NOTES:12 ("persistence is the selector, so there's no outside judge").

## W14. Acting systems: no memory-only floor
- **Tried:** T61 (`theory/FEEDBACK_FLOOR_2026-11-23.md:17`); CL11 (drift reduction) is open.
- **Wall:** when the memory steers its world, there is no design-independent floor on memory heat alone.
- **Today:** not re-run. Any tracking-first model where trackers change the pool they share (T1) is in T61's territory.

---

## Flags: routes re-run on 26 Nov without knowing they had been tried

| 26 Nov route | earlier record it repeats | how close |
|---|---|---|
| TRACKING_FIRST §1.2 "drop kT, keep counting Landauer" | SESSION_NOTES:4–5 (Chad's inversion, 25 Nov); T70 MEMO | same move |
| TF T0 currency audit HIT | T70 MEMO results table (only k_B in the tracking floors) | same result in other words |
| "low-entropy supply can't be dropped" | forces-gravity G1 (blank-memory boundary sets the arrow) | same finding |
| "a temperature-like price should appear on its own" (message to Chad) | STEPBACK §1a T2; forces-gravity G2 and G3-2; THEORY:195 | form already established; value not reachable that way |
| SH-heat / Claim W "the stake decides" | INFO_PHYSICS §6, §9; CORE:23, :29; RECORD_COST_CHAIN open miss 1 | same wall |
| REQUIREMENTS_FIRST compressed truth | PRICE_FREE; REVEALED_PRICES; THEORY:35, :71, :197 | repo's standing position |
| SELF_HORIZON "the stake is the system's own persistence" | SESSION_NOTES:12 | same idea |
| KELLY-TRACK / SELECTION-PRICE (proposed) | GROWTH_BRIDGE:259; T27 | heading into a known wall |
| T1 BLANK-PRICE (proposed) | #292 clean miss; W5 relabel | partial |

## What today's findings change
- **Unchanged:** W1, W2, W5, W6, W8, W9, W10, W12, W14.
- **Narrowed (hypothesis):** W3. The presupposed list shrinks to world, system and blank supply, with energy and kT as exchange rates (F4, F5, T70).
- **Sharpened:** W7. The blank supply is necessary under reversibility plus leak (F4).
- **Not changed by F3:** the narrowed F3 is ELEMENTARY and known (REVIEW_WORLDTRACK §8). It moves no wall.

---

## Proposed walls (appended 26 November 2026, after the 19:29:18 EST hash; proposals only)

The text above is unchanged (SHA-256 `475c129405a0ed264a57a3d35039ee9087325188ad019cc2ce8a39011dfe8276`, logged 2026-11-26T19:29:18-05:00). The three items below are proposals only (hypothesis, from later 26 Nov notes). They are not added to the W1–W14 list, and they do not change any earlier score.

### W15-reverse (proposal; TRACKABLE_WORLD route A, scored MISS)

- **Source:** `rnd/stepback/TRACKABLE_WORLD.md` §2 (file SHA-256 `7ad194c983f87382697fa0acc38d91ea871e8a5dc923b0dab5b85f3bbecdf9e2`, WORKLOG 2026-11-26T20:20:12-05:00). Pre-statement block `a22962467bfb2b1df1c33d512a39cb783ab81bd86a7686b681a6fa9475f3fec6`.
- **Proposal:** tracker existence gives only known information-theory and ruin conditions: finite drift, finite record lifetime, net positive inflow; locality and conserved quantities are not implied.
- **Label:** hypothesis, from CORE's class as tested; the necessary rows were already known (Bialek, Landauer, ruin theory). Route A could not fail against the world (NEXT_ROUTES §5 R2).

### Locality stays an input (proposal; named W15-candidate in NEXT_ROUTES §4)

- **Source:** `rnd/forces-gravity/THREAD_SUMMARY.md:10`, `:42–43` (as cited in `NEXT_ROUTES_2026-11-26.md` §4 and in the TRACKABLE_WORLD header).
- **Proposal:** locality stays an input; basis-free capacity gives no cut (partner modes with ~1/r tails).
- **Label:** observed in the forces-gravity record; not re-tested here. TRACKABLE_WORLD R5 (locality not implied; OU counterexample) is consistent with this proposal.

### Zero-cost self-tracker (proposal; named W16-candidate in NEXT_ROUTES §4)

- **Source:** `rnd/composition/NOTE.md:367` (as cited in `NEXT_ROUTES_2026-11-26.md` §4).
- **Proposal:** a reversible discrete classical world is a zero-cost self-tracker.
- **Label:** observed in the composition record; not touched by TRACKABLE_WORLD (no self-tracking was used).

Numbering note: NEXT_ROUTES used "W15-candidate" for locality and "W16-candidate" for the zero-cost self-tracker, written before route A was scored. TRACKABLE_WORLD then proposed "W15-reverse" for its MISS. The three proposals are kept under those names so the two notes still match. They are not assigned a single new index here.
