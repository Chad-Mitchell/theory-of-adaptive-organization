# WORKING_CONTEXT: the live working set for the GTAO physics work

*Rebuilt 26 Nov 2026, about 19:15–19:29 EST, from primary records only (sources listed in `WALLS.md` header; repo main `8b553c6`). Hard cap: 300 lines. Every item carries a pointer and a label: **observed** (a record says so, or a script printed it), **hypothesis**, **PIM** (proved in-model), **known** (prior art), **elementary**. Anything not here is in `FADED.md` as a one-line pointer. When this file and a primary record disagree, the record governs, and this file gets fixed.*

## 0. How this file is kept (the theory applied to its own reader)
- **Hold rule** (`applications/GROK_BOT_MEMORY_2026-11-23.md` §4, rule 1): an item stays only if stake × need rate beats the full cost of holding it (lines here plus re-checking). Need rate here means: will the next decision on the physics route use it? Stake: re-hitting a wall or misstating a result to Chad.
- **Re-check rule** (same file, rule 2 and §5): re-check a held item against its source when its drift is high. Today's notes change hourly, so: **open the pointed file before quoting any number from this file to Chad** (Chad's post 2125364046077510087, 24 Nov: "check before every answer").
- **Fade rule** (THEORY App. B.2 / CT11 freeze–hold–look up): low-need items are frozen as pointers in `FADED.md`, not paraphrased.
- Size now: see §9.

## 1. The goal, in Chad's words
- Chad, private chat, 26 Nov 2026 (t168u): "it seems that the core currently sits on top of thermodynamics … we're trying to remove that need and have thos theory show how physics arises at all / ie the judgement concept and hypothesis that physics is the universes way of keeping track of itself". (Quoted as written.)
- Chad, t171u: "Yes! Information. Why? What is going on here? Physics is derivative of this thing we're looking for at the peak…" and t172u: "I could be wrong . Just thinking".
- Chad, t164u: "Start from the requirements. Delete dumb requirements … There is a way to do what we're trying to do."
- Repo direction (README.md:64, Chad 25 Nov): "physics comes first. The mission is to find the physics; real systems are downstream checks. Results are reported row by row against named rivals."
- Repo hypothesis (CORE.md:7): "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
- **Label:** "physics is derivative of tracking" is a **hypothesis** (PHYSICS_CHAIN_2026-11-23.md:90, Level 4, SPECULATION). Nothing in the repo or notes shows it.

## 2. The repo's stance on information and physics (as written; not today's view)
- **Physics → cost, as a floor only.** "It bounds a heat. It does not choose a stake, a link price, or a ruin cap." (CORE.md:23). "Temperature does not set \(w\)." (CORE.md:29). Observed.
- The cost: \(J=\dot Q + w\,\mathbb E[\ell]\) subject to \(P(\text{ruin})\le\varepsilon\) (CORE.md:25–27). Its heat term is a floor from Horowitz–Esposito 2014 (CORE.md:19–21, known in its classes).
- "Ruin and linking stay outside. The master equation is not this cost." (theory/INFO_PHYSICS.md:19). Observed.
- Constants as exchange rates (T70, theory/constants-exchange-2026-11-24/MEMO.md:5): the cost alone is dimensionless; dimensional constants enter only when it is coupled to physics. Hypothesis.
- Ace's mission line (email 15077233, 25 Nov 13:05 EST, thread file line 549, quoted): "The hypothesis is that the cost of judgment is a law for adaptive systems and that physics grounds it."
- **Tension to keep in view (observed):** the repo's stated direction is physics grounds the cost (CORE.md:23; Ace). Chad's 26 Nov aim is the reverse: tracking first, with physics arising from it (t168u). PHYSICS_CHAIN Level 4 is the only repo text in that direction, and it is labeled SPECULATION. Any result in the reverse direction is new ground and must be labeled hypothesis until proved in a model.

## 3. What held up today (26 Nov), narrowed by the independent reviews
| # | result | label | source |
|---|---|---|---|
| H1 | The world (stake, price, ruin horizon, loss form) sets design **points**; the medium (noise, leak) sets **scales**; with the world coupling removed the theory returns scales and fronts, not a point | hypothesis (tested against 14 misses, 17 positives) | `rnd/stepback/REQUIREMENTS_FIRST.md` §5.1, :174 onward |
| H2 | For any loss that is the same function of angle for every design, the disk weakly dominates every polygon path (P15). Weak domination, not selection; ties common (17%) | PIM, elementary | `rnd/review_p15/REVIEW_P15.md` §0 (PASS-WITH-FIXES) |
| H3 | Step 0 TASK-LEVER: 60 of 60 cells show one switch from polygon to disk as the loss mixes reach and position scoring. **α\* values, "α\* falls with λ" and "α\*·λ → 12" are set by the menu cap**, not the class (3× menu triples α\* at λ = 1000) | observed (single crossing, subset); α\* values are menu artifacts | `rnd/review_worldtrack/REVIEW_WORLDTRACK.md` §0 item 3, §3.1, §9 fix 1 |
| H4 | Step 1 WORLD-TRACK: unique optimum in all 432 cells. Its R-regime content is **one elementary scaling identity**: ρ\* = 0.607, H\* ≈ 1.107 nats per read, n\*x^{−1/4}σ_w^{1/2} = 2.888, equal read/loss split, J\* ∝ σ_w√x, with J\*/(σ_w√x) → 1.2675 (not 1.244). Prior art Berger 1970 (D(R) = 2σ²/(π²R)), read via Kipnis–Goldsmith–Eldar | observed HIT; content PIM to leading order, elementary; Berger known | REVIEW_WORLDTRACK §0 item 4, §8 table, §9 fixes 4–5 |
| H5 | "Beyond Gish–Pierce" is true only because Gish–Pierce has no time in it. Not informative | observed | REVIEW_WORLDTRACK §0 item 4, §5 |
| H6 | **Only J ∝ σ_w√x carries across the register and Gaussian classes, and that is known** (the minimized cost \(2\sqrt{kT\,a\,v\,w}-kT\,a\) at CORE.md:90, mapped to σ_w√x; WORLD_TRACK.md:516 moved the mapping to elementary). "The information budget survives a change of class" is **unsupported**: hypothesis, contradicted under ideal coding (KGE). Step 2 INFO-BUDGET scored **MISS**: with no per-look price the look rate sits at the sensor limit | hypothesis (class claim); observed MISS | REVIEW_WORLDTRACK §0 item 5, §6, §8, §11; `rnd/stepback/WORLD_TRACK.md`:442–522 |
| H7 | kT enters every design and threshold only through price ratios; physics beyond price sits in floor class premises (local detailed balance, the Einstein relation) and relative coefficients | PIM (elementary, sympy-checked on 5 items, rest by inspection) | `rnd/stepback/TRACKING_FIRST.md` §8, :394; WORKLOG.md:302. Same result as T70 (`theory/constants-exchange-2026-11-24/MEMO.md`) |
| H8 | A tracking-first route cannot remove the low-entropy (blank) source under reversibility plus leak | elementary (known in substance: Landauer, Bennett) | TRACKING_FIRST.md:74, :300, :324. Same finding as forces-gravity G1 (`rnd/forces-gravity/THREAD_SUMMARY.md:6`) |
| H9 | In the SH-heat keep band the stake fixes the horizon at T = 2/x and the design at n\* ≈ 4/x + 2, independent of σ | observed (in that class) | `rnd/stepback/SELF_HORIZON.md`:533, :562 |
| H10 | The disk is self-consistent only if its own lifetime is infinite; a self-consistent horizon needs one outside parameter or is a tautology ("the input moves; it is not removed") | PIM | SELF_HORIZON.md §0 items 2–4, :73 |

**Messages to Chad that the reviews correct (observed):** "below it polygons win, above it the disk does" needs the menu qualifier (REVIEW_WORLDTRACK §9 fix 2). "That goes beyond the standard quantizer result, because the design depends on the world's drift" overstates: the drift dependence is known in kind (§0 item 4, Outcome). "What the world selects is an information budget" in the core's class is the unsupported class claim (H6). "Physics is derivative" was never shown; it is a hypothesis (§1).

## 4. Proved results on main that the physics route builds on (pointers only)
- Heat floor \(\dot Q \ge kT\)·(learning rate) in bipartite Markov and additive-noise classes: known (CORE.md:19–21).
- Worked class (OU world, Gaussian memory) minimizers: PIM (CORE.md §4; theory/INFO_PHYSICS_ATTAINABILITY.md:44–47).
- Lemma LY: a growth maximizer is Pareto in a chosen bad vector; it does not choose the vector: PIM (CORE.md:31; theory/GENERAL_FORM.md).
- Record cost under drift, RC1 (quantum-like records selected only under drift): PIM steps, merged #294 (theory/RECORD_COST_CHAIN_2026-11-25.md:13).
- Lean: #294 (62 theorems, merged); #295 open (192 theorems; rounds 4–10; pushed tip 96d7fa7 per WORKLOG 09:24). Local Lean in `rnd/lean/`.

## 5. Open misses (each with size and place; do not rescore)
| miss | size / place | source |
|---|---|---|
| SR-b4: no disk under any bounded horizon weighting | per-T argmin a polygon at every T | REQUIREMENTS_FIRST §5.1 table |
| SH-noise: no fixed point | 12–13 of 14 σ | same |
| SH-read MISS | 1344 of 1344 | same |
| Claim W (every input reduces to w) | false, 11 F rows | SELF_HORIZON.md:668–690 |
| Step 0 secondary prediction | 0 of 24 | REVIEW_WORLDTRACK §2 |
| Step 1 S3 | 5 of 8 rows fail | REVIEW_WORLDTRACK §2 |
| Step 1 corner rule relaxed before computing | tick s\* = 1 binds in 150 of 432 cells (35%); under Route 1 wording H-d would arguably fail | REVIEW_WORLDTRACK §1 |
| Step 2 INFO-BUDGET | MISS (B3; the tick binds) | WORLD_TRACK.md:464, :522 |
| RC open miss 1: zero drift | the stake q = 4 is a convention; classical can be cheaper | RECORD_COST_CHAIN:62, :92 |
| G4/G5 modular temperature from capacity price | open miss; T_c ≈ c/R not supplied by the cost | forces-gravity/THREAD_SUMMARY.md:43, :48 |
| #292 who copies whom | identical judges do not break symmetry (A ≈ 2e−8; 0 of 8 edges) | REQUIREMENTS_FIRST.md:150 |
| T27 selection bridge | FAIL on P3 (0/3) | PR #122 body |
| T67 learning-rate threshold | MIXED (3 of 4 EQUAL) | theory/LEARNING_RATE_THRESHOLD_2026-11-23.md:9 |

## 6. Walls (full list with sources in `WALLS.md`)
W1 physics bounds, does not produce, the cost · W2 prices free · W3 the cost presupposes system, world, bath, T · W4 every link borrows physics; Chad's inversion (SESSION_NOTES:4–5) · W5 temperature = price of information is an established form, not a value · W6 no physical temperature from capacity price · W7 the arrow of time comes from a blank boundary · W8 area law always from physical inputs · W9 Jacobson step: naive versions rename a cutoff · W10 quantum records only under drift; stake decides at zero drift · W11 closure without outside coupling picks nothing asymmetric · W12 growth ranks designs, does not produce the cost · W13 self-reference moves the input · W14 no memory-only floor when acting.
**Re-hit today without citing the earlier record:** W1, W2, W4, W5, W7, W10, W13 (table at the end of `WALLS.md`).

## 7. In flight now (do not duplicate; read before acting)
- WORLD_TRACK Step 3 STORED-PEAK: pre-statement hashed 19:09 (`084ea69e…`), no result yet (WORLD_TRACK.md:543 onward).
- TRACKING_FIRST T1 BLANK-PRICE: pre-statement in §10 (:450 onward); likely failure is competitive exclusion (:246), which sits beside W11.
- REVIEW_WORLDTRACK §9 fixes 1–9 are append-only and not yet applied to WORLD_TRACK.md.

## 8. Hard rules (each with its source)
1. No commits, pushes, posts or email in this pass (task brief). Ace merges tomorrow from the handoff (Chad t169u).
2. Wording: "theory", not "law", except quoting CORE.md:7 or others. Never "solved", "kill", "dead", "verdict", "puzzle" (task brief; Chad's correction post 2125343814428557450: "I shouldn't have said 'solved.'").
3. Never claim to derive GR, QM, holography or physical constants (Ace standing alignment item 4, email 15077233, thread line 552; README Ranked gaps PHYS-CHAIN-6).
4. Report results row by row against named rivals; never judge the whole theory from one test or one day (README.md:64; Ace 15072293, 25 Nov 12:58 EST).
5. Any line steering away from physics needs Chad's sign-off (Ace standing alignment item 3, thread line 551). DATA-ONE stays parked (README Ranked gaps).
6. Pre-state and hash before computing; log hash times to the second (REVIEW_WORLDTRACK §9 fix 8).
7. Every claim keeps its label; a miss is logged with size and place and drives an update (process/PROCESS.md:24; Ace 15072293).
8. Check the open source before answering (Chad 24 Nov post; §0 above).
9. Before proposing a route, check `WALLS.md` for it (this rebuild's reason).

## 9. Size of this working set
Whole file: 88 lines (cap 300), 10 held results, 13 open misses, 14 walls by name, 3 in-flight items, 9 rules. Everything else is a pointer in `FADED.md`.
