# NEXT_ROUTES (26 Nov 2026): candidate next routes toward "physics arises from tracking", checked against the walls

*Private R&D note, append-only. Written 26 Nov 2026 about 20:05–20:25 EST. No compute was run for this note (paper only; Crossref lookups only). Nothing committed, pushed, emailed or posted.*

**Re-grounded from primary records first** (read this session, not from chat memory): `rnd/context/WORKING_CONTEXT.md`, `WALLS.md`, `MEMORY_CHALLENGE.md`, `FADED.md`; repo main `8b553c641a333e6ddfb8b0789f8808fa2400677a` (checked equal to `git ls-remote` HEAD at about 20:08 EST) in `/workspace/gtao-fresh/repo`: `CORE.md`, `README.md` (Ranked gaps), `measurement/CLAIM_MAP_v2.md` (rows CL10, CX4), `theory/PHYSICS_CHAIN_2026-11-23.md` §5–§6, `theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176–180`, `THEORY.md:197`; notes `rnd/SESSION_NOTES.md`, `rnd/stepback/{STEPBACK,TRACKING_FIRST,REQUIREMENTS_FIRST}.md`, `rnd/forces-gravity/{THREAD_SUMMARY,NOTE}.md`, `rnd/composition/NOTE.md:355–370`; `WORKLOG.md` tail; the lessons in `/workspace/handoff-1127/NOTES/DECISION-LOG.md:243–256`.

**Labels:** observed (a record says so) · hypothesis · proved-in-model (PIM) · known (published; DOI checked on Crossref this session, `nextroutes/crossref_nr.txt` and `crossref_nr_retry.txt`, 19 of 19 OK).

**Still missing from the wall record (observed):** Ace's 24 Nov message `14229820` ("I stepped back over the whole physics line tonight …"). It is outside the 50-message read window; two keyword searches this session returned only its first line and the first line of `14230706` ("the cost is dimensionless (nats times stakes), and those constants carry units…"). Walls written only in that message are not checked below.

---

## 0. Goal and tension, as written

- Goal (Chad, 26 Nov, quoted in `WORKING_CONTEXT.md:12–13`): "have thos theory show how physics arises at all / ie the judgement concept and hypothesis that physics is the universes way of keeping track of itself", and "Physics is derivative of this thing we're looking for at the peak…". **Label: hypothesis.** The only repo text in that direction is PHYSICS_CHAIN Level 4, "Physics as the minimum-cost way for a universe to keep track of itself (SPECULATION)" (`PHYSICS_CHAIN_2026-11-23.md:90`).
- Tension (observed): `CORE.md:23` says "It bounds a heat. It does not choose a stake, a link price, or a ruin cap." `CORE.md:29`: "Temperature does not set \(w\)." The repo direction is physics → cost floor. The goal runs cost/tracking → physics.
- The structural fact behind every wall (observed, my reading of W1–W14 together): the theory's selection acts on **systems inside a given world** (CORE.md:7 hypothesis is about "strongly selected systems"). The world's rules are always an input (`THEORY.md:197`: "the world's measured pattern of change as the only world input"). `rnd/composition/NOTE.md:364` records that nothing in the theory says the world's rules are selected (paraphrased). So a route can only reach "physics arises" by (a) constraining the world from the existence of trackers (necessity, not production), or (b) adding a new premise that puts the world's rules under the cost. Every candidate below is one of these two, or is dropped.

## 1. Bars fixed before listing (apply to every candidate)

- **Triviality bar (any one makes a result a restatement):** (T1) a known theorem said in cost words; (T2) the result holds for every cost of the form "a price per nat plus a task term", so the cost's own structure (stake × need vs upkeep, keep/check/fade, the ruin cap) does no work; (T3) the output is a form, not a value or a structural selection (W5's rule); (T4) the input moves and is not removed (W13's rule); (T5) the answer depends on a free price ratio (W2's rule).
- **Novelty bar (all needed for "new"):** (N1) not found in the prior art listed per candidate, after a search this session; (N2) the cost's specific structure is used (fails T2); (N3) the output is a feature physics has, stated price-free.
- **Scoring:** EIV = p(HIT)·V_HIT + (1 − p)·V_MISS, per hour of agent time, then a 40% discount on my own unreviewed score (DECISION-LOG lesson 6, `:252`: "A ~40% discount on unreviewed self-scores matched the day"). Lesson 5 (`:251`, read the owner's intent) and lesson 9 (`:255`, "Imported physics targets need a line in the theory first") are applied in the drop decisions.

---

## 2. Candidates

### A. TRACKABLE-WORLD: what must a world be like for bounded trackers to exist at a finite cost? (necessity ledger, paper)

- **Question:** If CORE's hypothesis is not idle (bounded trackers exist and sit near a finite minimum), which properties must the world's dynamics have, and which of those are properties physics has?
- **Method (paper):** a ledger, one row per candidate condition, each marked PIM-in-repo / known / open, and "is it a physics feature?" Seed rows:
  1. Copying is not free (Chad's inversion, `SESSION_NOTES.md:21`: "strongly selected systems exist, therefore copying isn't free"). Already done; cited, not re-run.
  2. A low-entropy (blank) supply is needed (W7; `TRACKING_FIRST.md:74`, :300, :324). Already done; cited, not re-run.
  3. Finite predictive information at each scale; the forecast miss equals the predictive information not carried (CL10, `CLAIM_MAP_v2.md:550`, PIM, "Probably folklore in parts"; CX4 `:578`, open). Known in kind: Bialek, Nemenman & Tishby 2001 (10.1162/089976601753195969); Still et al. 2012 (10.1103/PhysRevLett.109.120604).
  4. Fixed-size lossless summaries (sufficient statistics of fixed dimension) exist only for exponential families, i.e. the Gibbs form with additive sufficient statistics (Koopman 1936, 10.1090/S0002-9947-1936-1501854-3; Pitman 1936, 10.1017/S0305004100019307; known, for i.i.d. sampling under regularity conditions; Markov analogue **not checked**). Beside W5: a second route to the Gibbs **form**, not to any value.
  5. Predictable or conserved coordinates are the cheapest records: the heat floor is zero for predictable change (T68, `PHYSICS_CHAIN_2026-11-23.md:110`), and slow coordinates carry the predictive information (Creutzig, Globerson & Tishby 2009, 10.1103/PhysRevE.79.041925). Open: whether the cost's hold rule makes **conserved additive** quantities necessary (not just cheap) for a tracker population.
  6. Locality: hypothesis that it is **not** necessary. Counterexample to check on paper: an all-to-all world with a low-dimensional mean is cheap to track.
- **Walls nearby and the specific difference:**
  - W1 (`WALLS.md:18`): W1 walls physics → cost. A takes the hypothesis as input and outputs constraints on the world; no physics floor is used. Difference: direction.
  - W4 (`WALLS.md:36`): W4 walls physics links that borrow physics, and the k_B-as-conversion inversion. A borrows no physics constant. Risk kept: the routes after the inversion reached "synthesis-level results under stated premises" (`WALLS.md:38`); A's rows 1–2 are exactly such results.
  - W3 (`WALLS.md:30`): A still presupposes a system and a split; it removes the world's rules from the input list only in the sense of constraining them. Partial.
  - W5 (`WALLS.md:41`): row 4 gives a form only. Inside W5 for row 4; scored as known.
  - W7 (`WALLS.md:51`): row 2 is W7 itself; cited, not re-run.
  - W13 (`WALLS.md:81`): no self-reference used. Clear.
- **Prior art to beat (all Crossref-checked):** Müller 2020, Quantum 4:301 (10.22331/q-2020-07-20-301): observer states first, an external world emerges via algorithmic probability; no cost or stake. Wheeler 1992 (10.1111/j.1749-6632.1992.tb17083.x). Bialek et al. 2001; Still et al. 2012; Koopman 1936; Pitman 1936; Kolchinsky & Wolpert 2018 (10.1098/rsfs.2018.0041). Observer-selection (anthropic) arguments are a known argument type; no citation checked here, so none given.
- **Triviality bar for A:** "trackers need a predictable world" (Bialek); "lossless fixed summaries need exponential families" (Koopman–Pitman); "trackers need a low-entropy source" (W7). Any row that is one of these is T1.
- **Novelty bar for A:** one row where the cost's own structure (the hold rule \(w p > c + 2\sqrt{k w\sigma^2/6}\), `MEMORY_CHALLENGE.md:38`, or the ruin cap) makes a world property **necessary**, that property is one physics has, and it is not in Müller 2020 or the information-theory sources.
- **HIT:** at least one row meets the novelty bar, proved in a model (PIM), stated as necessary-not-sufficient.
- **OPEN:** a row is necessary only under an added premise that is itself not a physics feature (e.g. a stationary world).
- **MISS:** every row is known or is not a physics feature. Then the honest statement is "the theory constrains worlds only as information theory already does", and it becomes a new wall (W15, reverse direction), which stops future circling on this question.
- **Score:** p(HIT) 0.15, V_HIT 4, V_MISS 1.5 (a reverse-direction wall has real value). EIV 1.88; about 3 h paper → 0.63/h; **discounted 0.38/h**. Usage: low (reading and writing only).
- **Hypothesis label on the whole route:** even a HIT shows necessity ("if trackers, then X"), not that physics arises from tracking.

### B. STAKE-FREE CUT: does the cost pick the split between tracker and world without being told it?

- **Question:** For a closed system given with no tracker/world split (and, in the strong form, no preferred coordinates), is there a split that minimizes the cost for **every** stake w? A stake-free cut would be price-free structure the theory produced (the only kind W2 allows).
- **Walls nearby and the difference:**
  - W3 (`WALLS.md:30`): W3 says the cost presupposes the system. B makes the system an output. Specific difference: the cut is the unknown.
  - W2 (`WALLS.md:24`): B targets price-free structure, the one exit W2 leaves; if the cut moves with w, B lands inside W2 (that is the MISS).
  - W11 (`WALLS.md:71`): a symmetric closed system may pick no cut ("the cost picks nothing asymmetric"). B must use a system with heterogeneous rates; then W13's question applies: is the asymmetry just the input moved? Partial.
  - W13 (`WALLS.md:81`): a cut defined by self-consistency per stake would be a tautology; B requires one cut across all stakes, which is a test, not a fixed point.
- **Prior art (Crossref-checked unless noted):** in the linear-Gaussian class this is the Gaussian information bottleneck: the optimal projection directions are fixed eigenvectors and the trade-off parameter only sets how many are used (Chechik, Globerson, Tishby & Weiss 2005, JMLR 6:165; **no DOI**, existence checked at jmlr.org this session). So in that class a HIT is T1. Also: Carroll & Singh 2021 (10.1103/PhysRevA.103.022213, factorization chosen by quasi-classical dynamics); Zanardi 2001 (10.1103/PhysRevLett.87.077901) and Zanardi, Lidar & Lloyd 2004 (10.1103/PhysRevLett.92.060402, subsystems induced by the accessible observables); Krakauer et al. 2020 (10.1007/s12064-020-00313-7, individuality as an information-optimal boundary); Kolchinsky & Wolpert 2018.
- **Triviality bar:** the selected cut is the weakest-coupling or slowest-mode cut (Carroll–Singh, Krakauer, Gaussian IB). **Novelty bar:** outside linear-Gaussian, a stake-independent cut that differs from those, and uses the ruin cap or the hold rule.
- **HIT:** a non-Gaussian class where one cut is optimal for all w (PIM) and differs from the minimum-coupling cut. **OPEN:** stake-free only on a band of w. **MISS:** the cut moves with w (inside W2), or it is the known cut (T1).
- **Score:** p 0.10, V_HIT 4, V_MISS 1.0. EIV 1.30; about 8 h (paper then a small computation) → 0.16/h; **discounted 0.10/h**. Usage: moderate.

### C. LOCALITY-FROM-LINKS: does a link price make the trackers' network low-dimensional on a world with no geometry? — **mostly inside a record; dropped**

- **Question:** With a price per link and a world with no built-in geometry, does the cost-minimizing link graph have a price-free dimension? (Origin: `SESSION_NOTES.md:9`, "locality from the cost of copying records far away".)
- **Why dropped:** the forces-gravity round already found "basis-free capacity gives partner modes with ~1/r tails and no cut" and listed "per-site pricing = locality" as chosen (`forces-gravity/THREAD_SUMMARY.md:10`, :42–43; observed). That record is not one of the 14 walls but it is the same wall in kind (locality stays input), and W8 (`WALLS.md:56`) took locality as input. Prior art predicts the generic case fails: generic spectra rarely admit a local tensor-product structure (Cotler, Penington & Ranard 2019, 10.1007/s00220-019-03376-w); geometry from entanglement takes the state as input (Cao, Carroll & Michalakis 2017, 10.1103/PhysRevD.95.024031). If the world is local, the graph inherits it (T4). Graph density moves with the link price (T5).
- **Score for the record:** p 0.05, V_HIT 5, V_MISS 0.5, about 12 h → 0.06/h, discounted 0.04/h. Below every other line. Revisit only if A's row 6 finds locality necessary.

### D. WORLD-RULES REQUIREMENT AUDIT: what new premise would put the world's rules under the cost, and does any version survive the walls? (paper)

- **Question:** Of the three known ways to make the world's rules themselves selected — (i) selection among worlds (Smolin 1992, 10.1088/0264-9381/9/1/016, cosmological natural selection; no cost or stake), (ii) self-consistency with tracker = world (PHYSICS_CHAIN Level 4; TRACKING_FIRST T4), (iii) observer-first probability (Müller 2020) — does any version, with the cost added, avoid W11, W13 and the composition record below, without being one of the three in new words?
- **Walls nearby and the difference:**
  - (ii) is **inside W11 + W13** as posed: `composition/NOTE.md:366–367` (observed): "If tracker = world, the drift premise becomes 'the world's own change is continuous'. A reversible discrete classical world is a zero-cost self-tracker." That record is not among the 14 walls; it should be (see §4). TRACKING_FIRST T4 (`:280–288`, p 0.1) also states its own relabel risk (Creutz/DY2000/Jaynes). Dropped as a route; kept only as a row to audit.
  - (i) avoids W11/W13 (selection is outside the world) but needs reproduction of worlds and a cost-to-fitness map at that scale: inputs from physics (W1/W4), and the repo's own review calls it the one published place where selection acts at that scale (`reviews/night2/SCALE_ENDS_INDEP_REVIEW.md:159`). Risk T1.
  - (iii) avoids W1 (no physics input) but adding a cost to Müller's measure is a relabel unless the stake does work (T2).
- **Lesson 9 applies:** none of (i)–(iii) has a line in the theory. CORE.md:7's hypothesis is about systems, not about the world's rules. Running D as more than a written audit needs **Chad's sign-off** on a scope change (and THEORY.md/CORE.md are not to be edited by me in any case).
- **Triviality bar:** a version that is Smolin, Müller or Wheeler with the word "cost" added. **Novelty bar:** a version where the stake or the hold rule changes which world-rules are selected, compared with the same version without the cost.
- **HIT:** one version passes the novelty bar on paper and has a stated test that can fail. **OPEN:** a version passes only with an extra premise named. **MISS:** all three are inside walls or prior art; then the note states the exact new requirement (as in §3), which is what Chad asked to know.
- **Score:** p 0.10, V_HIT 5, V_MISS 1.0 (most of the MISS content is already in §3 of this note). EIV 1.40; about 2 h → 0.70/h; **discounted 0.42/h**. Usage: low. Needs Chad's OK before it goes beyond the audit.

### Dropped without a full write-up (inside walls; observed in the records cited)

| route | inside | record |
|---|---|---|
| T1 BLANK-PRICE (paused) | beside W11 and W5; likely failure is competitive exclusion | `WALLS.md:105`, `TRACKING_FIRST.md:246` |
| KELLY-TRACK / T2 SELECTION-PRICE | W12 | `WALLS.md:79`, `GROWTH_BRIDGE.md:259` |
| T3 RUIN-EXCHANGE | W2 (θ is a price) and CT18 Buckingham π (T1) | `TRACKING_FIRST.md:262–270` |
| T4 SELF-TRACK | W11 + W13 + `composition/NOTE.md:367` | `TRACKING_FIRST.md:280–288` |
| Horizon-temperature rung (PHYSICS_CHAIN §6 item 2) | W6, W9 | `WALLS.md:46`, :61 |
| Stored-information uniqueness re-pose | W1/W2; cancelled 26 Nov | `WORLD_TRACK.md` §3.6–3.14; WORKLOG 20:01:48 |
| FREEZE_OR_HOLD falsifier (Arrhenius lifetimes) | W1: it checks physics against the floor, physics in | `FREEZE_OR_HOLD_FLOOR_2026-11-23.md:180` |
| BICAUSAL (repo rank 1) | not dropped from the repo; not a route to **this** goal (closure with fixed noise; W11, W14 nearby) | `README.md:74` |

---

## 3. Honest summary: does any candidate clear the walls?

- **A and D clear the walls by changing direction**, not by breaking a wall: A asks for necessity (trackers ⇒ world features), D asks what premise is missing. B clears W3 in form but most likely lands in W2 or in the Gaussian-IB prior art. C is mostly inside a record. **No candidate is expected to show physics arising** (hypothesis, my reading; p ≤ 0.15 for any HIT, before discount).
- **The new requirement, stated now (hypothesis):** for "physics arises from tracking" to be testable at all, the theory needs a premise it does not have: **the world's rules are inside the cost's domain** — either a selection that acts on worlds (with a reproduction and fitness map), or a closure condition with an outside asymmetry named and priced (to escape W11/W13 and the zero-cost reversible self-tracker). Without that premise, the theory can at most say what a world must be like for trackers to exist (A), which is necessity, not origin. Adding it is a scope change to CORE.md:7's hypothesis and needs Chad's decision (lesson 9).
- **Also needed:** Ace's 24 Nov message `14229820` in full, to finish the wall record before any run.

## 4. Pick

- **Top pick: A (TRACKABLE-WORLD), paper only, about 3 h, low usage.** Reasons: it is in the theory's present scope (uses CORE.md:7 as input, needs no new premise); it uses no physics constant, so it does not re-enter W1/W4; it turns Chad's "physics is derivative" into a checkable necessity claim; and its likely MISS still yields a reverse-direction wall (W15) that stops the circling Chad flagged. Discounted 0.38/h.
- **Then D's audit (0.42/h discounted, 2 h)** only after Chad says whether a world-rules premise is in scope. D scores slightly higher per hour on my own numbers, but those numbers are unreviewed and D cannot proceed past paper without his decision, so A goes first.
- **Proposed wall additions (for WALLS.md, not applied here):** W15-candidate "locality stays input; basis-free capacity gives no cut" (`forces-gravity/THREAD_SUMMARY.md:10`, :42–43); W16-candidate "a reversible discrete classical world is a zero-cost self-tracker" (`composition/NOTE.md:367`).
