# REQUIREMENTS_FIRST (FOR-39): question every requirement, delete the ones the theory does not demand, then see what is left

*26 Nov 2026, written about 18:20–18:45 ET. Local note only (not committed or pushed). Repo text read at today's main `8b553c641a33` (2026-11-25 22:49 −05:00) in a fresh clone. CORE.md and THEORY.md are byte-identical to `ac92ee2`. Labels: **PIM** = proved in-model; **ELEMENTARY**; **KNOWN**; **HYP** = hypothesis; **OBSERVED** = numerical output. "open miss" marks a prediction that did not come out. Working premise (Chad, pt165u and the brief): a peak exists. It is treated as a premise to test, not as a finding.*

*Central question (from the parent's steering, 18:18): is every selecting number in today's results a coupling between the record and the world it is for? And are today's misses the result of a requirement we added, self-selection with the world removed?*

## 0. Result

1. **Win, from source (§1).** The theory claims that **one cost, given the world and its prices, sets the design**:
   - CORE.md:7 and :9 ("write the cost, find its minimum, and read off the design");
   - THEORY.md:17 ("layers matched to the time scales of the world, as many as the stakes can pay for");
   - THEORY.md:197 ("the world's measured pattern of change as the only world input");
   - README.md:13 (one curve in x = wv/(kT·a), built from the world's variance v and rate a).

   CORE.md:23 says the cost does not choose the stake, the link price or the ruin cap. The test targets we added were: select the disk; one polygon n* from the record alone; zero chosen inputs; a parameter-free lifetime; a unique attracting self-consistent fixed point. **None of these is in the theory's text.** The PR #295 thread, fetched today, contains **no text by Ace**: one comment, by the mitchell-moving account, and no reviews or review comments. So no Ace goal is quoted from it.
2. **Ledger (§2).** 34 requirements. **20 are deleted** as conveniences of our models or targets we added. Each deletion cites the line that does not demand it.
3. **Left (§3).** Six requirements:
   - the cost J = Q̇ + w·E[ℓ] with P(ruin) ≤ ε;
   - the heat floor, where proved;
   - a loss, stake and ruin cap set by the world the system acts in;
   - the world's measured statistics as the only world input;
   - the design as argmin within a named class;
   - Part 2's selection hypothesis, with its qualification rule.
4. **Positive findings (§4).** 17 results held. Together they show a structure: **the record's own geometry sets the menu and its tradeoffs; the record's coupling sets the point.**
   - The medium's noise σ sets resolution scales: n_c, n_b, 1/σ².
   - The stake sets horizons and points: T = 2/x, n* = A(⌊2/x⌋).
   - The scored task sets which geometry wins: positional tracking → disk; reaching distinguishability → polygon; antipode → tie; cap versus stake → the unsupported Pareto points.
5. **Compressed truth (§5), HYP, tested against all 14 misses and 17 positives:**

   > *Every number that selected a design today came from the record's coupling to something outside it: the medium's noise, the world's stake or price, or the scored task. With that coupling removed, the theory returns scales and tradeoff fronts, not a point. Today's misses are the requirement "select without the world", which the theory never makes.*

   This is the lead hypothesis, sharpened in two ways. (a) "World" must be split into the **medium** (σ, Γ: it sets scales) and the **task** (w, ε, ℓ: it sets the point). (b) The **form** of the loss, not only the scalar w, is a lever. The four candidate compressions fail as stated (§5.2).
6. **Routes (§7), ranked by the brief's ordering rule.**
   - **WORLD-TRACK** (the lead; ready for a pre-statement, not run). The world's drift sets σ_w, its event cost sets w, and CORE's cost (keep floor + Landauer read + stake) gives a unique interior n* ∝ √x.
   - **KELLY-TRACK:** w replaced by the world's payoff structure.
   - **TASK-LEVER:** a paper lemma, the cheapest per hour.
   - **RUIN-HORIZON.**
   - **POP-COPY.**
7. **Self-review (§8): PASS-WITH-FIXES.** The circularity finding: the lead hypothesis is close to true **by construction of J**, which takes w and the world as inputs. Its non-trivial content is only the specific map (which coupling sets which design feature), and Routes 1–3 test that map. Several "positives" (n_c, n_b) are KNOWN in substance (resolution ≈ noise), not the theory's own content.

## 1. The win, stated from source (today's main, `8b553c6`)

### 1(a) What the theory itself claims or needs

- **CORE.md:7:** "**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**"
- **CORE.md:5:** "In worked classes the minimum is computed, in closed form where the class allows, and it says what the best design looks like: how many layers, what to share, where a boundary is enough, when a shock should strengthen a system rather than harm it."
- **CORE.md:9:** "The method is the same everywhere: write the cost, find its minimum, read off the design (§2)."
- **CORE.md:23:** "It bounds a heat. It does not choose a stake, a link price, or a ruin cap."
- **CORE.md:27:** "J = Q̇ + w·E[ℓ] subject to P(ruin) ≤ ε."
- **CORE.md:29:** "w converts the loss into the currency of the heat. Temperature does not set w."
- **CORE.md:91:** "Above the stake kT a/v the minimizing cost is 2√(kT a v w) − kT a. At or below it the design is blind: heat 0, error v, cost wv."
- **THEORY.md:11:** "…judgment has one cost: holding memory, being wrong or late, and buying and sharing the information that keeps memory fresh, all without going broke. … the theory prices what staying alive takes, and says the price sets the design: where the world changes on several time scales, build in layers matched to the time scales of the world…"
- **THEORY.md:17:** "**The claim is that one cost sets how adaptive systems should be built at every scale: in layers matched to the time scales of the world, as many as the stakes can pay for and faster looking cannot replace.**"
- **THEORY.md:19:** "*Matched* means what the theory proves and no more. The count follows the world: a layer for each separated real time scale the stakes can afford…"
- **THEORY.md:197:** "**The theory's own, as far as anyone has found:** the package. A layer count priced inside one objective; the world's measured pattern of change as the only world input, with its predictive dimension capping the layers; a ruin constraint whose slack end recovers the expected-cost rules; one booking rule across substrates with a refutation condition; and predictions across scales, posed so that they can fail."
- **README.md:13:** "In the worked class every time scale lands on one curve in the stake ratio x = wv/(kT a): below x = 1 no memory pays, and above it a memory pays and its error falls as v/√x."
- **README.md:9:** "Part 1 is mathematics … Part 2 is the hypothesis about nature, and only Part 2 can miss a measurement."
- **CLAIM_MAP_v2.md:455 (N13, OPEN):** "Measured-input optimality: with α, q, N and stakes measured on one strongly selected system …, its read rate, memory time and store count lie near the THEORY §2.2 optima, at ≥ 2 scales."
- **CLAIM_MAP_v2.md:498 (N56, OPEN):** "…the number (counted by degree), memories and read rates of its layers match argmin J computed from its world's measured drift spectrum, sensing noise and prices…"
- **What the theory does not claim** (README.md:76, PHYS-CHAIN-6): "Claims nothing about deriving gravity, quantum mechanics or holography." No line of CORE.md, THEORY.md, README.md or CLAIM_MAP_v2.md asks a design to be selected by the record alone, or a continuous group to be derived from the cost. The continuum question is a repo R&D line (theory/RECORD_COST_ROUND10 §14; CLAIM_MAP RC10, an open miss), not the headline.
- **Ace's goals in the PR #295 thread.** Fetched today through the public API: the issue, all comments (1, by `mitchell-moving`, 2026-11-26 05:57 UTC = 00:57 ET), reviews (0), review comments (0), and the first 100 timeline events (all commits). **No Ace-authored text is in the thread**, so nothing from Ace is quoted. Repo text that reports Ace's requests (for example "as Ace asked on 24 November", in the #286 body) is ours, not Ace's.

### 1(b) What we added as the test target (none of these is in 1(a))

| added target | where it entered | the theory line that does not ask for it |
|---|---|---|
| select the disk (a continuous group) | ROUND10 §14 and STEPBACK §14 (repo R&D); SR-b, SR-b4 | THEORY.md:17 asks for layers matched to the world, not a group; README.md:76 claims no QM derivation |
| select one polygon n* from the record alone | SELF_HORIZON §6 | CORE.md:9 reads the design off the cost **with** the world and prices (CORE.md:23, :27) |
| zero chosen inputs | SELF_HORIZON §§1, 5, §10.6 Claim W | CORE.md:23 and :29: the stake, link price and ruin cap are inputs; N13 measures the stakes |
| parameter-free lifetime | SELF_HORIZON §§6, 8 | THEORY.md:138: keep while "need × miss cost beats upkeep", so lifetime depends on need and stake |
| unique attracting fixed point of a self-consistency loop | SELF_HORIZON §§6–11 | no self-consistency loop in CORE §§1–4 or THEORY §§1–2; the method is a minimum (CORE.md:9) |
| all inputs reduce to w (Claim W) | SELF_HORIZON §10.6 | CORE.md:23 names three separate inputs |

## 2. Requirement ledger

**Source codes:** T = the theory's text (file:line); A = Ace (no Ace text found in #295); C = Chad (owner messages pt161u, pt162u, pt165u in this session, and the brief); U = us (rnd notes).
**Kind:** P = physically required, or required by the theory's own statement; M = a convenience of our model; X = a target we added.

| # | requirement | test(s) | source / owner | kind | kept or deleted, and why |
|---|---|---|---|---|---|
| 1 | Moves are pure-state jumps | SR-b4, SH1, SH-* | U, from ROUND10 §14 (`m_round10b_poly.py`) | M | **Deleted.** With mixed intermediate states every design ties at 1/T (SR_B §11.4, PIM). No CORE or THEORY line asks for pure states |
| 2 | Polygon-plus-disk menu | all SR/SH | U (GPT menu, Janotta 2011) | M | **Deleted** as a theory requirement. It is a named class (CORE.md:13 allows classes), not a demand |
| 3 | Quadratic cost c·d² | SR-b, SH | U (ROUND10 §14) | M | **Deleted.** ROUND10 §14: "With a linear price c·d the ranking reverses". CORE.md:27's cost is heat plus stake, not transport |
| 4 | Targets M3h or antipode | SR-b4, SH | U (ROUND10 §14) | M | **Deleted** as fixed. The target is the loss ℓ, which CORE.md:27 takes from the task. §7.2 and SR-b3 show it decides the outcome |
| 5 | Discrete n | SH | U | M | **Deleted.** A design index; no theory line needs it |
| 6 | Per-horizon selection (P) rather than a fixed design (F) | SR-b4 | U (SR_B §9) | M | **Deleted.** A quantifier choice; Claim W row 3 (PIM) shows it decides the outcome |
| 7 | One record, not a population | all | U | M | **Deleted.** CORE §5 (the evolutionary route) and THEORY §3 (population proxy) cover populations |
| 8 | A fixed noise channel σ, chosen by us | SH-noise, -heat, -read | U | M | **Deleted** as chosen. In the theory, noise is the world's or the sensing noise (THEORY.md:19: "each layer's memory is set by its own mode and the sensing noise"). It should be measured or world-set |
| 9 | A single agent | all | U | M | **Deleted.** The swarm rule (README.md:42) and #292 are multi-agent |
| 10 | Stationary world | SH | U; also a class premise of THEORY §B.2 (W-a) | M (class) | **Kept as a class premise only.** Theorem P extends to drifting worlds (CLAIM_MAP T, PD1a) |
| 11 | No competitor or copier | all | U | M | **Deleted.** No theory line needs it |
| 12 | The horizon T as a free number | SR-b4, SH | U | X | **Deleted as free.** It is CT25's ruin window (THEORY.md:402), set by the world's shocks and ε. SELF_HORIZON §1 found horizon and ruin cap to be one input |
| 13 | Select the disk | SR-b4, SH1 | U (ROUND10, STEPBACK) | X | **Deleted.** §1(b) |
| 14 | Select one n* from the record alone | SH-noise, -heat, -read | U | X | **Deleted.** §1(b) |
| 15 | Zero chosen inputs | SELF_HORIZON, Claim W | U; C ("solve this", read by us as "derive everything") | X | **Deleted.** CORE.md:23, :29 |
| 16 | Parameter-free lifetime | SH-noise, -heat | U | X | **Deleted.** THEORY.md:138 |
| 17 | A unique attracting self-consistent fixed point | SH-* | U | X | **Deleted.** No such loop in CORE or THEORY; a minimum is needed (row 30) |
| 18 | Horizon reading (one written state's life versus the information's life) | SH-heat, -read | U | X | **Deleted.** The theory's lifetime is need-driven (THEORY.md:138), not a reading of a carrier |
| 19 | Claim W: all inputs reduce to w | §10.6 | U | X | **Deleted.** CORE.md:23 |
| 20 | Scale-free (log-uniform) horizon weighting | SR-b4 | U | X | **Deleted.** No theory line |
| 21 | No mixing within or across worlds | C12CG | U (C12c §11.5) | M | **Deleted.** With mixing, cap and stake coincide (Lemma A(b′); Everett 1963, KNOWN) |
| 22 | Committed (S, E) points per world | C12CG | U (the chain's locked settings) | M | **Deleted** as a requirement; bookkeeping only (C12CG §1) |
| 23 | Separate-leak carriers (P1, S1) | C12B, SH-heat keep floor | U (C12B_ORDER §8.1, §9.4) | M (class) | **Kept as a class premise.** CORE.md:78 says storage is cheap where the leak cancels |
| 24 | A long-run growth objective | compliant clue | U (CLUE_COMPLIANT §2, HYP) | M | **Kept as a candidate objective** (Route 2), not a requirement |
| 25 | The cost J = Q̇ + w·E[ℓ], P(ruin) ≤ ε | all | T: CORE.md:27 | P | **Kept** |
| 26 | Heat floor Q̇ ≥ kT × learning rate (proved classes) | SH-heat, -read | T: CORE.md:19–21, CORE.md:66; KNOWN (Horowitz–Esposito 2014) | P | **Kept**, in its classes |
| 27 | The stake w, from the task | SH-heat, -read | T: CORE.md:23, :29 | P | **Kept, world-set** (measured in Part 2, N13) |
| 28 | The ruin cap ε | C12C, SELF_HORIZON | T: CORE.md:27; THEORY CT22, CT25 | P | **Kept, world-set.** Same object as the horizon (row 12) |
| 29 | The world's statistics as the only world input | — | T: THEORY.md:197; N56 | P | **Kept** |
| 30 | Design = argmin within a named class | all | T: CORE.md:9, :13 | P | **Kept** |
| 31 | Keep while need × miss cost beats upkeep | SH-heat, -read | T: THEORY.md:138, :145; CT9 (:311), CT11 (:321), CT26 (:480) | P | **Kept**, as a rule inside row 30 (it is the argmin of a hold decision) |
| 32 | Landauer cost of erasing | SH-heat | KNOWN (Landauer 1961) | P | **Kept** |
| 33 | Read price c | SH-read | T: CT9 (THEORY.md:311) | P (a world price) | **Kept, world-set.** It is a "link price" in CORE.md:23's sense |
| 34 | Strongly selected systems sit near the minimum (qualification, THEORY §3) | — | T: CORE.md:7; THEORY.md:13 | P (Part 2) | **Kept** |

- **Count:** 34 rows; 20 deleted (rows 1–9, 11–22); 2 kept as class premises only (10, 23); 1 kept as a candidate (24); 11 kept (25–34).
- **Chad's working premise, "a peak exists",** is kept as a premise to test in Routes 1–2: does a unique interior argmin exist given the world? It is not a requirement on the record alone.
- **Ace:** no requirement is attributed to Ace (§1(a)).

## 3. What is left (the minimal surviving set)

1. **Cost:** J = Q̇ + w·E[ℓ] subject to P(ruin) ≤ ε (CORE.md:27).
2. **Floor:** Q̇ ≥ kT × the net learning rate, in the classes where it is proved (CORE.md:19–21, :66). Storage can be nearly free where the leak cancels (CORE.md:78). A keep floor applies only to separate-leak carriers (row 23).
3. **Task inputs, set by the world the system acts in:** the loss ℓ, the stake w, the ruin cap ε (equivalently the horizon, CT25), and prices such as the read price c (CORE.md:23, :29; THEORY.md:138).
4. **World input:** the world's measured statistics, its drift spectrum and noise (THEORY.md:197; N56). The medium's noise belongs here when it is measured.
5. **Method:** the design is argmin J within a named class (CORE.md:9). Keep, check or fade is the hold decision inside it (THEORY.md:138, §B.2).
6. **Part 2:** strongly selected systems sit near that minimum (CORE.md:7), tested only on qualified systems (THEORY §3; N13, N56).

What this set does **not** ask: that the record pick itself, that inputs vanish, that the continuum be selected, or that a self-consistency loop attract.

## 4. Positive findings from today (what held up, with labels and why each matters)

| # | finding | where | label | why it matters |
|---|---|---|---|---|
| P1 | The crossing scale n_c ≈ (4 ± 0.5)/(σ√(2 ln(1/σ))), β = 0.81–0.86. It survived every arm as the place where lifetime and horizon meet: primary, ⌈τ⌉, and the fade branch of SH-heat and SH-read (n_c·σ√(2 ln(1/σ)) = 3.3–4.4) | SELF_HORIZON §7.3, §9.2, §11.4 | OBSERVED; KNOWN in form (Shannon 1949; PSK; quantizer sizing) | The medium's noise sets a resolution scale robustly. It is the one number no arm moved |
| P2 | The keep, check or fade rule in its band: the map is flat (slope 0, every orbit attracted), n* = A(⌊2/x⌋) ≈ 4/x + 2, T = 2/x exactly in all HIT cells | §9.3–§9.5 | OBSERVED (141 cells; c_K = 4: 150) | The theory's own hold rule (THEORY.md:138) turned a repelling map into an attracting one. It did so by making the horizon a function of the **stake**, not of the design |
| P3 | The keep edge n_b ≈ 3.3/(σ√(4 ln(1/σ))), nearly x-free. Designs above it are kept forever (τ = ∞) | §9.2 | OBSERVED | Medium noise sets **where** the hold rule switches; the stake sets **what** is picked below it |
| P4 | With a read price (y ≥ 0.1), every check design outlasts every horizon it could serve: s* > π²/(4·d_min), minimum ratio 1.8, 8851 of 8851 | §11.2 | OBSERVED + PIM (SR-b1(f)) | A world price changes which hold mode exists; the §9 band is price-sensitive. Prices are inputs (CORE.md:23) |
| P5 | Under the antipode rule every even polygon costs at least the disk (the 4T-gon ties) | §7.2; ROUND10 §14 | PIM (ELEMENTARY) | The scored target alone decides polygon versus disk |
| P6 | SH1: the disk is never self-consistent at any finite lifetime ≥ 2 where odd or M3h-even polygons exist | SELF_HORIZON §2.3; §7, §9 | PIM | The continuum appears only under an all-horizons requirement (SR-b1(f)), never at a finite world-set horizon |
| P7 | The horizon and the ruin cap are one input (CT25 writes them as one parameter ε_r/T_h) | §1, §5; THEORY.md:402 | ELEMENTARY (an identification of text) | The horizon is not ours to choose: it is the world's ruin structure |
| P8 | With mixed intermediate states every design ties at 1/T | SR_B §11.4; HOSTILE_REVIEW_SRB4_ODD | PIM (ELEMENTARY) | The polygon/disk distinctions come from the pure-jump move rule (model), not from the cost |
| P9 | The R1 (depolarizing) and level arms give n_c ∝ 1/σ² (R1 ≈ 4/σ²; L ≈ 2φ_δ²/σ²) | §7.4, §7.5 | OBSERVED + heuristic | How the medium's noise acts (kicks versus replacement, any change versus a level) sets the exponent. The medium's form is an input |
| P10 | Kelly growth absorbs P2 (ruin cap, multiplicative ruin), P3 (horizon) and P4 (cap versus stake), and partly P1 (stake) and P16 (mixing) | CLUE_COMPLIANT §2 | HYP (with KNOWN pieces: Kelly 1956; Peters 2019) | A world with multiplicative stakes supplies the horizon, the ruin cap and the cap/stake choice from one objective |
| P11 | C12CG per-record gap: the pentagon and octagon are cap-only picks (unsupported Pareto points; margins 4×10⁻³, 8×10⁻⁴) | C12CG §§3, 9, 11; review PASS-WITH-FIXES | OBSERVED, conditional on nearest-vertex encoder optimality (HYP; 200/200 random starts and 1450+ structured encoders) | The **form** of the world's requirement (an accuracy cap or a stake) changes the pick on a discrete menu. KNOWN in general (Everett 1963; Haimes 1971) |
| P12 | A pentagon state carries ≈ 1.0204 bits (total reading), so the chain's log₂N identification fails for odd N | C12CG §11(d) | OBSERVED (a lower bound on the sup); KNOWN direction (Massar–Patra 2014 Thm 2) | An intrinsic capacity fact. Intrinsic properties exist and matter for the cost, but they do not select by themselves |
| P13 | Claim W counterexamples: the target rule and the quantifier order each change the outcome at fixed (indeed absent) w | §11.6 rows 3, 4 | PIM | The scored loss itself, not only its price, is a lever |
| P14 | The (2T+2)-gon beats the disk at every T ≥ 2 under M3h (SR-b3), plus the odd analogue | SR_B §8.6, §10–11 | PIM (reviewed PASS-WITH-FIXES) | A reach-distinguishability task selects finite polygons at every finite horizon |
| P15 | **New on paper here: positional tracking selects the disk.** For any loss that depends only on the angle between record and world, any polygon vertex path is matched by the disk through the same angles at no higher move cost, since d_poly ≥ sin(φ/2) = d_disk (§7.2's inscribed-width step, valid for every regular n-gon of circumradius 1) | this file, §4.1 | PIM (ELEMENTARY; self-checked only) | The task form decides the geometry: position → disk; distinguishability → polygon |
| P16 | #292 who copies whom: identical judges, each the other's world, do not break symmetry (T1 A ≈ 2e−8, T2 0 of 8 edges, clean miss) | `theory/stop-copying-2026-11-25/RESULTS.md` (branch, run at `1816940`) | OBSERVED (locked prereg) | When the world is a mirror of the record, the cost picks nothing asymmetric: no outside coupling, no selection |
| P17 | EVO1: selection reaches argmin J where the world is clean (Q1, Q2, Q3 SIM-PASS; Q4–Q8 mixed) | CLAIM_MAP_v2.md:635–643; CORE.md:130 | OBSERVED (in-model) | When the world and stake are given, search finds the theory's point. That is the theory's actual claim working |

### 4.1 P15, the paper argument (PIM, ELEMENTARY; self-checked)

- **Setting:** SR_B §1's pure-jump class. A world angle θ_t, and a record that must sit at a pure state. The loss per tick depends only on the angular difference between record and world, f(φ_record − θ_t). The move cost is Σ d_t².
- **Claim:** for every polygon policy there is a disk policy with the same loss and no higher move cost. So inf over designs is attained by the disk.
- *Proof.* The regular n-gon's vertices sit at angles 2πk/n on the unit circle, and these are pure states of the disk. Use the disk path through the same angles. The angular loss is identical. Each step costs sin²(φ/2) in the disk (SR_B §1), against d_poly² ≥ sin²(φ/2) in the polygon, by §7.2's step: width ≤ 2, so d(u, w) ≥ |u − w|/2. ∎
- **Strictness** is not claimed in general; the antipode is a tie for even n.
- **Scope:** no keep cost. With a keep floor the exact disk costs ∞ (§8.2), and the tradeoff is Route 1.

### 4.2 What the positives say together (the structure the theory did produce)

1. **The menu and its tradeoffs come from the record's own geometry:** distances, capacities (P12), and the pure-jump rule (P8). That geometry alone selects nothing (P8: an all-tie; P16: a mirror world, no break).
2. **Scales come from the medium's noise:** n_c (P1), n_b (P3), 1/σ² (P9). They are robust and KNOWN in form.
3. **Points come from the task's coupling:**
   - the stake → T = 2/x and n* ≈ 4/x + 2 (P2);
   - the ruin structure → the horizon (P7, P10);
   - the price → whether a hold mode exists at all (P4);
   - the loss form → which geometry wins: position → disk (P15); reach → polygon (P14); antipode → tie (P5); cap → off-hull picks (P11); quantifier → disk versus polygon (P13).
4. **Search finds these points** when they are given (P17).

**This is the theory's own structure** (CORE.md:9 + :23 + :27; THEORY.md:17, :197): cost + world → design. What today's targets demanded, a point from step 1 alone, is the one thing this structure does not provide, and the theory never says it does.

## 5. Compressed truth

### 5.1 The winner (HYP), stated in three sentences

*Every number that selected a design today came from the record's coupling to something outside it: the medium's noise set scales, and the task (stake, price, ruin horizon, and the form of the scored loss) set points. With that coupling removed, the theory returns scales and tradeoff fronts, not a point, and a self-referential loop on the record alone either repels or ties. The misses are the requirement "select without the world", which the theory never makes (CORE.md:9, :23; THEORY.md:17, :197).*

**Test against every miss** (each must be explained, not most):

| miss | explained? |
|---|---|
| SR-b4 (P): no disk under any bounded weighting | Yes. The horizon weighting is not a world coupling; with no task-set horizon, the per-T argmin is a polygon at every T (SR-b4) |
| SR-b (geometric q): no disk at q ≤ 0.995 | Yes, the same reason; the selected n moves with q, a chosen input |
| SH1 (disk never self-consistent) | Yes. The continuum needs an all-horizons requirement, i.e. an outside quantifier (P6) |
| SH-noise primary: no fixed point at 12–13 of 14 σ | Yes. Only the medium coupling was present, and it gave the scale n_c but no stable point (P1) |
| SH-noise ⌈τ⌉, R1, L | Yes. The medium's form changed the scale only (P9) |
| SH-noise E-mixed degeneracy | Yes. The antipode target ties every even polygon with the disk (P5) |
| SH-heat cells outside the band (keep → τ = ∞; fade → repelling) | Yes. Outside the band the stake no longer sets T; the medium edge n_b decides (P3) |
| SH-heat "selects per stake, not per σ" | Yes. The point came from the task coupling x (P2) |
| SH-read MISS (1344 of 1344) | Yes. A world price removed the stake-set hold mode (P4); what remained is the medium scale (P1) |
| SH-read "set by noise", e_x ≈ 0 | Yes, the same |
| Claim W false (11 F rows) | Yes. The task form and medium are separate couplings (P13), not one scalar |
| C12CG gap (cap-only picks) | Yes. The task's requirement form selected (P11) |
| #292 clean miss (mirror judges) | Yes. There is no outside coupling to break the symmetry (P16) |
| EVO1 Q4–Q8 misses (ruin gate, store noise, valleys) | Partly. They are search failures inside a given world (CORE.md:130: "stalled where the world added an obstacle"). They are not selection failures of the cost, so they are outside the compression's scope. Stated, not hidden |

All 17 positives fit the three-layer reading of §4.2. The pentagon bit count (P12) is intrinsic, and the compression allows intrinsic facts that do not select.

### 5.2 The candidates, and the evidence that rules each out as stated

- **(i) "Selection needs something external to the single record: a population, a competitor or an environment that sets the stake."**
  - The **environment** half is the winner.
  - The **population or competitor** half is ruled out as necessary. SH-heat's band selects a unique attracting point with one record and no population (P2). #292's population of identical judges selects nothing (P16).
- **(ii) "The theory fixes trade-off curves, not points; points always come from a chosen input."**
  - True with the world removed: P1, P3, P8 and P11's front.
  - False as stated: the theory's worked class gives points (CORE.md:91, a closed-form minimum), and today's band gives a point (P2).
  - "Chosen" is the error. The input is **world-set** (CORE.md:23, :29; N13 measures it), not ours.
- **(iii) "We asked 'which design' instead of 'which scaling', and the scaling n_c survived."**
  - Ruled out as the compression. The surviving scaling is KNOWN in form (P1; Shannon 1949; Gish–Pierce 1968), so it cannot be the theory's distinct prediction.
  - The theory does claim design points: counts of layers (CORE.md:92) and read rates (N56).
  - Partly right: it names P1 as robust.
- **(iv) "The missing piece is dynamics across many records (copying, replication)."**
  - Ruled out as necessary: P2 needs no population; #292 found no symmetry breaking from mutual copying; EVO1 replication reaches the same argmin as optimisation (P17).
  - Kelly absorbs P2–P4 as an **objective**, not through a population (CLUE_COMPLIANT §2).
  - Replication is a search route (CORE §5), not a source of the selecting number.
- **(v) Mine, considered and rejected: "the move rule (pure jumps) is the hidden selector".** It explains P8 and P14, but not P2 (stake-set) or P1 (noise-set).

### 5.3 Two sharpenings of the lead hypothesis that the evidence forces

- **Split "world" into medium and task.** σ in SH-* was the record's own carrier leak, a medium property, not the tracked world's drift. Medium couplings set **scales** (P1, P3, P9); task couplings set **points** (P2, P5, P11, P13, P14, P15). In the theory, the medium enters through the floor's prices (CORE.md:19–21) and the task through w, ℓ and ε (CORE.md:27).
- **The loss form is a lever, not just w.** Rows 3–4 of Claim W and P15 versus P14 show that the shape of ℓ (position versus reach) flips the geometry. CORE.md:29's w only converts a given loss. Which loss is the task's.

## 6. Does the lead hypothesis lead to a route where the world sets both stake and noise, so nothing is chosen by us?

- **Yes, in the theory's sense; not literally in a model.**
  - In a model, the world's drift σ_w and its event cost w are still numbers we set, but they are **world parameters**, not record parameters. Part 2 measures them (N13). That is exactly the theory's structure (CORE.md:23, THEORY.md:197).
  - The medium's leak Γ is a third, separate number. The keep floor's class premise (row 23) also applies. So "nothing chosen" means "nothing chosen about the record".
- **Can the stake itself come from the world's own dynamics?** Partly. Under a growth objective (Kelly), w is replaced by the payoff structure and the reserve size R/kT (P10; CLUE_COMPLIANT P1 "partly absorbed"). That is Route 2.
- **Route 1 survives the hostile review in §8,** with the caveat that its likely outcome (n* ∝ √x) is ELEMENTARY in substance (entropy-coded quantizer sizing). So it is placed first, as the brief asks, with its expected triviality stated before any pre-statement.

## 7. Next routes (built on §4's positives and §3's surviving set; ranked; none run)

*Scale as in §13 of the stepback notes: EIV = p·V_HIT + (1 − p)·V_MISS; value per hour = EIV/cost.*

### Route 1: WORLD-TRACK (lead; **ready for a pre-statement**, not run)

- **Question.** When an n-gon record tracks a world angle that drifts with the world's own σ_w, under CORE's cost (keep floor + Landauer read + the world's stake on angular error), is there a unique interior n*(x, σ_w, Γ)? Does it scale as n* ∝ √x (the master-curve exponent, README.md:13), with the read interval set by the world's drift?
- **Minimal model.**
  - World: θ_t is a wrapped Gaussian walk, step σ_w.
  - Record: an n-gon vertex, refreshed every s ticks by a read that snaps to the nearest vertex. Held between reads at the keep floor c_K·Γ·ln n per tick, in kT units (C12B premise, row 23). Each read pays Landauer kT·H, at most kT ln n.
  - Loss: x·E[(θ_t − φ_record)²] with the angle difference wrapped. The quantisation error is ≈ π²/(3n²), and the drift adds σ_w²(u + ½) at age u.
  - Menu: n ≥ 3. The disk is excluded by an infinite keep cost (PIM, §8.2), and the P15 domination statement is the check.
  - Paper optimum: n*² ≈ (2π²/3)·x/(c_KΓ + ln-read term/s*) and s* ≈ √(2·ln n*/(x·σ_w²)). The exact numeric optimum, by a 2-D integer search with exact wrapped errors, is the test.
- **HIT:** a unique interior n* at every grid point (x, σ_w, Γ); d ln n*/d ln x ∈ [0.35, 0.65] where keep dominates the cost; s* decreasing in σ_w with |d ln s*/d ln σ_w| ∈ [0.8, 1.2]; no corner solutions.
- **MISS:** corner solutions (n = 3 or the range edge), non-uniqueness, or exponents outside the windows.
- **Pre-stated triviality:** e_x ≈ ½ is the entropy-coded quantizer result. Genuine content is only if the keep floor and the read floor together give a prefactor or exponent the quantizer formula does not (for example a σ_w-dependence of n* through s*).
- **Prior art (Crossref OK, `reqfirst/crossref_req.txt`):**
  - Gish & Pierce 1968, *IEEE TIT* 14:676, 10.1109/TIT.1968.1054193;
  - Gray & Neuhoff 1998, *IEEE TIT* 44:2325, 10.1109/18.720541;
  - Sims 2003, *J. Monet. Econ.* 50:665, 10.1016/S0304-3932(03)00029-1 (rational inattention);
  - Horowitz & Esposito 2014, *PRX* 4:031015, 10.1103/PhysRevX.4.031015;
  - Landauer 1961, 10.1147/rd.53.0183.
- **Score:** p(HIT) 0.7, V_HIT 3 (a world-set peak in the theory's own cost), V_MISS 2 (the keep and read floors do not give an interior design). EIV 2.7, cost ≈ 3 h → **0.9/h**.
- **Claims moved:** an in-model analogue of N13 and N56 (design from measured world inputs); CT4 and CT7 (the first bit must pay; tracking floor); C12B's keep floor in use.

### Route 2: KELLY-TRACK

- **Question.** In Route 1's world, replace the stake by the world's payoff: each tick the agent bets its reserve R on the world's sector, and pays the heat from R. Does growth select a unique n*, set by the **world's** noise (resolution ≈ σ_w √s), with R/kT setting only whether memory pays at all (a threshold, as README.md:13's x = 1)?
- **Minimal model:** a horse race with n outcomes (the record's cells), fair odds on the world's sector, Kelly fractions. Growth per tick = I(record; world) − heat/R.
- **HIT:** unique interior n*, with |d ln n*/d ln R| ≤ 0.25 above the threshold R_c, and n*·σ_w√s* constant within a factor 1.5.
- **MISS:** n* moves with R like √R (stake-like), or no interior optimum.
- **Prior art (Crossref OK):**
  - Kelly 1956, *BSTJ* 35:917, 10.1002/j.1538-7305.1956.tb03809.x;
  - Kussell & Leibler 2005, *Science* 309:2075, 10.1126/science.1114383;
  - Donaldson-Matasci, Bergstrom & Lachmann 2010, *Oikos* 119:219, 10.1111/j.1600-0706.2009.17781.x;
  - Rivoire & Leibler 2011, *J. Stat. Phys.* 142:1124, 10.1007/s10955-011-0166-2;
  - Vinkler, Permuter & Merhav 2016, *J. Stat. Mech.* 043403, 10.1088/1742-5468/2016/04/043403;
  - Peters 2019, *Nat. Phys.* 15:1216, 10.1038/s41567-019-0732-0.
- **Score:** p 0.55, V_HIT 3.5 (the stake is absorbed into the world's payoff, so "nothing chosen about the record" holds except R), V_MISS 2. EIV 2.8, cost ≈ 4 h → **0.7/h**.
- **Claims moved:** CLUE_COMPLIANT P1–P4 (absorption made exact or not); CORE §5; README.md:13's threshold.

### Route 3: TASK-LEVER (paper)

- **Question.** In SR_B §1's class, is the selected geometry decided by the task form alone? Positional losses → the disk (P15). Reach-distinguishability → (2T+2)-gons (SR-b3). Antipode → a tie (P5). Find the exact boundary for mixed losses α·position + (1 − α)·reach.
- **Minimal model:** SR_B §1 with that mixed loss. DP as in SH, plus a paper proof of P15's strict version where it holds.
- **HIT:** a single threshold α* per T, with the disk above it and polygons below it.
- **MISS:** an interleaving of designs in α.
- **Prior art:** Janotta et al. 2011 (10.1088/1367-2630/13/6/063024, Crossref OK in C12CG review), Massar & Patra 2014 (10.1103/PhysRevA.89.052124, OK).
- **Score:** p 0.8, V_HIT 2.5, V_MISS 3. EIV 2.6, cost ≈ 1.5 h → **1.7/h**, the highest per hour.
- **Claims moved:** CLAIM_MAP RC10 (ROUND10 §14, "J does not select a continuous group"). It names the task feature that does.

### Route 4: RUIN-HORIZON

- **Question.** Set the horizon from the world's shock statistics through CT25 (B ≥ z_ε·σ√τ; THEORY.md:402), and feed it into SR-b or SH-heat. Does n* then follow the world's shock size and ε with no free T?
- **HIT:** a monotone, unique n*(σ_shock, ε).
- **MISS:** non-unique, or insensitive.
- **Prior art:** Cramér–Lundberg is credited in THEORY CT22. No new DOI.
- **Score:** p 0.6, V_HIT 1.5 (a composition), V_MISS 1.5. Cost ≈ 2 h → **0.75/h**.
- **Claims moved:** CT25, CT22; SELF_HORIZON §1's horizon = ruin.

### Route 5: POP-COPY

- **Question.** In Route 1's world, run replicator dynamics over n-types with copying (#292-style coupling). Does selection reach something other than Route 1's argmin, testing compression (iv)?
- **HIT:** a frequency-dependent selected n different from the argmin.
- **MISS:** the argmin, as P17 predicts.
- **Prior art:** Kussell & Leibler 2005 (above); #292 (repo).
- **Score:** p 0.15, V_HIT 3, V_MISS 1.5. EIV 1.7, cost ≈ 5 h → **0.35/h**.
- **Claims moved:** #292, CX2-SETTLE (README.md:78), CORE §5.

### Ranking

- The brief asked for the lead route first if it survives review. Route 1 does (§8).
- By value per hour the order is Route 3 (1.7) > Route 1 (0.9) > Route 4 (0.75) > Route 2 (0.7) > Route 5 (0.35).
- **Recommended order:**
  1. **Route 1 (ready for a pre-statement)**, with Route 3's P15 lemma as its step 0 (a 1.5 h paper check that the disk is the right exclusion);
  2. Route 3;
  3. Route 2;
  4. Route 4;
  5. Route 5.
- None of these is run here.

## 8. Self hostile review: **PASS-WITH-FIXES**

- **C1, circularity (the one Chad warned about), high.**
  - **Am I re-describing my own model's choices as the theory's findings? Partly, yes, and it is named here.**
    - (a) P1 and P3 (n_c, n_b) are properties of **our** medium model (wrapped kicks, nearest-vertex snapping) and KNOWN in form. They are listed as positives because they held. They are not the theory's own content (THEORY.md:197 lists what is), and they must not be cited as theory predictions.
    - (b) The lead hypothesis is **close to true by construction**: J = Q̇ + w·E[ℓ] takes w, ℓ and the world as inputs (CORE.md:27), so "the selecting number came from the coupling" cannot fail inside the theory's own cost. Its non-trivial content is only the specific map in §5.3 (medium → scales, task → points, loss form → geometry). That map is testable, and Routes 1–3 test it.
    - (c) Deleting "select without the world" removes today's misses by definition. The deletion is justified only because no theory line makes that requirement (§1(b)). It is **not** evidence for the theory.
  - **Fix:** carry (a)–(c) into any summary.
- **C2, high: P15 is new and self-checked only.** It relies on §7.2's step, which applies to regular n-gons inscribed in the unit circle with all effects. Strictness is not shown. **Fix:** an independent check before P15 is used as more than a route's step 0.
- **C3, medium: the "explains every miss" table has one partial row** (EVO1 Q4–Q8). Those are search failures in a given world, outside the compression's scope. That is a scope limit, not a fit.
- **C4, medium: Ace's goals.** None was found in the #295 thread. The brief expected some. Either they are elsewhere (an email thread or another PR) or they do not exist. Not searched beyond #295, by the brief's scope. **Fix:** the parent should say where Ace stated goals if they exist.
- **C5, medium: a citation correction to SELF_HORIZON.** §8.1 and §10.6 cite "CORE.md:21–23" and "CORE.md:23 (J = Q̇ + w·E[ℓ] …)". On main, the J display is **CORE.md:27**, "It bounds a heat. It does not choose a stake…" is **:23**, and "w converts … Temperature does not set w." is **:29**. The cited quotes are correct; the line numbers for J and for "w converts" are off. Logged in WORKLOG; SELF_HORIZON not edited.
- **C6, low: route scores are judgments,** on the stepback §13 scale, not measurements.
- **C7, low: wording.** The word for a rule of nature appears only in the CORE.md:7 quote. No banned words are used (checked by search). Nothing claims to derive QM, GR, holography or gravity.
- **C8, low: Route 1's "nothing chosen"** is "nothing chosen about the record". σ_w, w and Γ remain world or medium numbers in-model (§6).
- **Outcome: PASS-WITH-FIXES.** Fixes: C1's three caveats in summaries; an independent check of P15 (C2); Ace's goal source (C4); the CORE line-number correction recorded (C5).

## 9. Labels (summary)

| claim | label |
|---|---|
| The win: cost + world → design (CORE.md:7, :9, :27; THEORY.md:17, :197; README.md:13) | quoted text |
| 20 deleted requirements are not demanded by any theory line | ELEMENTARY (a reading of text; §2 cites each) |
| Positives P1–P17 | as labelled in §4 (5 PIM, 9 OBSERVED, 1 HYP, 2 ELEMENTARY or KNOWN-form) |
| P15: positional tracking selects the disk | PIM (ELEMENTARY), self-checked |
| Compressed truth (§5.1) with the medium/task split | HYP; consistent with all 14 misses (one partial, scope) and all 17 positives |
| Candidates (i)–(iv) as stated | not supported (§5.2 evidence) |
| Routes and scores | HYP / judgment |

## 10. Correction: P15 after the independent review (appended 26 Nov 2026, about 18:40 ET; governs §§0, 4, 4.1, 4.2, 5, 8, 9 where they conflict)

*Source: `rnd/review_p15/REVIEW_P15.md`, outcome PASS-WITH-FIXES. The review found no invalid step. Its fixes 1–7 are applied below, and §§0–9 above stand as written. Fix 8 concerns `WORLD_TRACK.md` and is applied there.*

### 10.1 Restated claim (fixes 1 and 6)

**Proposition P15 (PIM, ELEMENTARY; independently checked by REVIEW_P15).**

- **Class.** SR_B §1's class:
  - pure-state jumps, with staying put allowed;
  - **all effects**: every affine functional with values in [0, 1] on the state space is a measurement;
  - regular n-gons in the regular embedding (circumradius 1, concentric with the disk), plus the disk.
- **Hypotheses.**
  - The loss is **one design-independent function** of the record's embedded angle, the world and time. The same function is used for every design, and no rotation invariance is needed.
  - The per-step move cost is **any nondecreasing g(d)** of the operational distance, with weight ≥ 0. The quadratic d² is not needed.
  - There are **no design-dependent hold costs**: no keep floor, no read cost, no per-dimension price that differs between designs.
- **Conclusion.**
  - The disk's optimal value is ≤ every polygon's, per step and pointwise per path.
  - Hence the same holds at every horizon, under any horizon weighting, and in expectation under any world distribution, with adapted policies.

### 10.2 Wording (fixes 2 and 5)

- Everywhere above, "positional tracking selects the disk" and "position → disk" are replaced by: **"on a positional loss the disk is never beaten by a polygon (weak domination; ties occur)."**
  - This covers the P15 row in §4, §4.1's title, §4.2 item 3, §5.1 and §5.3, and the §9 labels table.
- **No uniqueness claim is made.**
  - REVIEW_P15 observed exact ties in 17% of 24,000 random instances. The antipode/4T-gon tie is proved in-model.
  - Strictness, where it holds, is a corollary only:
    - odd n: strict on every non-zero step;
    - even n: strict exactly on edge-normal chords.
  - These are PIM per the review. A strictly better disk also needs the optimal polygon policy to use at least one strict step.

### 10.3 P5 folded into P15 (fix 3)

- P5 (under the antipode rule every even polygon costs ≥ the disk; the 4T-gon ties) is a **special case** of P15. The antipode target for even n is a positional, design-independent loss.
- §4.2 item 3 therefore reads: **"position, including the antipode → the disk, weakly (P15, with P5 as an instance); operational reach → polygons (P14)."**
- P5 is not a separate task form, and "antipode → tie" is withdrawn as a distinct lever.

### 10.4 Why SR-b3 and SR-b4 fall outside P15 (fix 4)

- SR-b3, SR-b4 and the odd (2T+1)-gon results score an **operational, design-dependent target**: "any vertex at operational distance 1 *in that design*" (M3h), or v_{S′} at angle π − π/n (the M1 reading of the antipode rule).
- As a function of embedded angle this target changes with the design (REVIEW_P15 §3 table):
  - triangle: 120°, 240°;
  - pentagon: 144°, 216°;
  - hexagon: 120°, 180°, 240°;
  - disk: 180° only.
- So P15's hypothesis "one design-independent loss" fails there, and nothing contradicts.
- **The split is geometric (embedding) loss versus operational loss,** not "position versus distinguishability" in general. Corrected statement of the lever (HYP until WORLD_TRACK Step 0 is scored): *a geometric loss never lets a polygon beat the disk; an operational loss can.*

### 10.5 The short restriction proof (fix 7)

- **Proof.** Let K be any convex set inside the unit disk D, with all effects. Every effect of D (affine, with values in [0, 1] on D), restricted to K, is an effect of K. So d_D(u, w) = max over D-effects of |e(u) − e(w)|, which is ≤ the same maximum over K-effects, d_K(u, w), for all u, w ∈ K. Each polygon step therefore costs at least the disk step through the same two points (g nondecreasing), and the loss is the same function (by hypothesis). ∎
- This holds for any convex K ⊆ D, not only regular polygons, and needs no width computation.
- **Needs all effects:** REVIEW_P15's hexagon with a single effect pair gives d(v₀, v₁) = 0.25 < 0.5, and the step fails.
- **Credit, KNOWN in kind:** monotonicity of the gauge under inclusion (Schneider 2013, doi 10.1017/CBO9781139003858), and contraction of distinguishability under valid maps (Kimura, Nuida & Imai 2010, doi 10.1016/S0034-4877(10)00025-X). These DOIs were checked on Crossref by the review (`rnd/review_p15/crossref_p15.out`). The instance is ELEMENTARY.

### 10.6 Effect on §5's compressed truth

- §5.3's second sharpening reads: **the loss's dependence on the design's own geometry (operational versus geometric) is a lever, not just w.**
- §4.2's structure keeps its three layers. In the third layer, "loss form → which geometry wins" now reads "geometric loss → the disk, weakly; operational loss → polygons can win".
- §8 C2 (P15 self-checked only) is closed by REVIEW_P15.
