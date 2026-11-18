> **SUPERSEDED SNAPSHOT (archived 18 Nov 2026, consistency audit).** Verbatim copy of Ace's off-repo `<local>/gtao/CURRENT_BRIEF.md` (written 18 Nov, about 12:20 PM ET, before PR #80 merged). Several statements here are now stale (e.g. "the gates await Chad's sign-off", "no black-hole content in the repo", README version pointers). Use `BRIEF.md`, `STATUS.md` and `THEORY.md` instead. Kept for provenance only; not maintained and not checked by `tools/check_consistency.py`.

# CURRENT_BRIEF: A Theory of Adaptive Organization (GTAO), reread from the sources

Written Wed 18 Nov 2026, early afternoon ET, by an executor for Ace (Chad's request pt1926u). I reread the sources for this brief; no summary or memory brief was used as a source. `<local>/gtao-video/MEMORY_BRIEF.md` was read only to find what is stale in it (§7).
No repo edits. Nothing was sent or posted.

**Citation keys** (repo = `<repo>`, main = `4b7a6a1`, PR #79, 18 Nov 07:20 ET). Note: during this reread another agent checked the shared clone out to branch `q-scale-ends` (`bb14154`, 12:17 PM ET: "SCALE-ENDS: claim ledger 191 (out-of-cycle, unscored)"). That commit differs from main only by one `queue/LEDGER.jsonl` line, and there is an untracked `theory/scale_ends_checks/`, the black-hole/cosmos deep pass in progress, which I did not read. Every doc cited here is identical on main:
- THEORY = repo `THEORY.md` (v1.4.17).
- FW = `measurement/FRAMEWORK.md`.
- CM = `measurement/CLAIM_MAP_v2.md` (v2.38).
- STATUS = `STATUS.md`. QUEUE = `QUEUE.md`.
- SYN = `reviews/night2/SYNTHESIS_2026-11-15.md`.
- SCR = `prereg/SENSE-CELL/RESULTS.md`. SCREV = `reviews/night2/SENSE_CELL_REVIEW.md`. SCP = `prereg/SENSE-CELL/PREREG.md`.
- AUD = `reviews/night2/AUDIT_DIVERGENCE.md`.
- LIT = `litmap/LITMAP.md`. THR = `litmap/THREATS.md`.
- HYP = `<local>/gtao/longform/HYPOTHESES.md` (frozen raw log, 11 Nov). HC2 = `<local>/gtao/longform/HYPOTHESES_CORE_v2_reviewed.md` (frozen).
- Video files: VS = `<local>/gtao-video/main/script.py`, TS = `teaser/script.py`, VD = `DESIGN.md`, VF = `FACTCHECK.md`, VDESC = `DESCRIPTIONS.md`, VPY = `main/video.py`.

Precedence: THEORY governs where files disagree (THEORY:6). Everything in `<local>/gtao` outside the repo is frozen history (STATUS:16; `<local>/gtao/STATE.md`).

---

## 0. Answer to Chad's point (pt1926u), in plain words

- **He is right that the measurement framework exists.**
  - It was built on 15 Nov, about 08:10–08:20 ET, in direct response to Chad's t1908 point that "the theory never said how its quantities are measured" (FW:3, FW:5).
  - It defines measurement triples, ten validity gates (MV1–MV10), three tiers, an anti-rescue rule and a new status vocabulary (FW:64–99).
  - It re-audited every past field test (FW §4, FW:418–551).
- **What that re-audit found:**
  - Every field "kill" and "hit" so far was a result about a proxy. No result reaches Tier 1, so there is "no FIELD-FAIL and no FIELD-PASS anywhere".
  - GTAO's distinctive real-world content is "untested, not refuted" (FW:551; CM:96; THEORY:14–15, THEORY:144).
- **So "failed on proxy" does not mean the theory failed in the real world.**
  - Under T∧M∧A ⇒ X, a failed prediction refutes only the conjunction of theory, measurement mapping and auxiliaries (FW:26–31).
  - None of the past tests validated M or A first.
  - Proxy fails still carry information: they kill that particular mapping (FW:35–41).
- **What has not happened yet:**
  - No decisive, framework-compliant (Tier 1) test of the core bet has been run.
  - The gates themselves "become binding only once Chad signs off on them" (CM:329 M2; CM:393). I found no record of that sign-off.
  - FW is "not independently reviewed" (FW §8, FW:685–691).
  - The first job is measurement on one system (SAME-SYSTEM-AQN; QUEUE:120; SYN:104–112).
- **What the video got wrong on this point:**
  - It says "failed on proxies: several" (VS:20).
  - It never says why those fails do not count against the theory, and it never mentions that the framework exists.
  - That is the understatement Chad flagged (see §6, item V1).

---

## 1. Core theory, plain words and math

**Plain words.**
- A cell, an immune system, an ant colony, a person, a firm or a city persists by holding information about a world that keeps changing.
- It pays one budget for this:
  - holding memory;
  - error, including being late;
  - the reads that keep memory current;
  - plus the risk of ruin.
- Only the implementation and the currency change with scale (THEORY:33, THEORY:72–76; FW:11).
- It is a falsifiable causal theory: "never a law" (CM:281 J3 WITHDRAWN; QUEUE:8) and "not a theory of everything" (THEORY:35; README:3).

**Objective (THEORY:72).** J = upkeep + w·E[loss] + lateness + Λ·hazard (+ drift-reduction cost), minimized subject to staying solvent.
- Theorem P: solvency needs at least R(y − c̄) bits (THEORY:74).

**Causal chain (THEORY:76; CM:294 J15 OPEN).**
1. The world's change destroys the information the system holds.
2. Re-buying it costs reads, precision or upkeep.
3. Error and lateness cost stakes.
4. Selection or design keeps the cheapest allocation that stays solvent.

**The world is described by its spectrum**, S(f) ∝ f^−α (THEORY:72–76). The design rules below are classical and credited, not new (THEORY:82–99, THEORY:116):
- **Regime A (α = 2, a random walk).** The √ rule, T* = √(2c/(wσ²)) (Harris 1913 EOQ; Reis 2006); one exponential store (Kalman, Muth); sensing (Mora & Nemenman 2019); application (Lee, Flack & Krakauer 2024). "All KNOWN" (THEORY:82–87).
- **Regime B (scale-free, 1 < α < 3)** (THEORY:90–99):
  - read rate ∝ (w·q/c)^{1/α}, with 1/α = 1/(1+2H);
  - precision effort ∝ w^{α/(2α−1)} q^{1/(2α−1)};
  - memory time ∝ (N/q)^{1/α};
  - kernel weight ∝ τ^{−(1+α/2)}, exponential only at α = 2;
  - store count K* ≈ (ln 8R/2π²)·ln(stakes/upkeep), with span- and model-dependent constants.
- **Regime C (modes λ_i ∝ i^−β)** (THEORY:108–112):
  - model size ∝ Q^{1/β};
  - an interior minimum exists iff β < 1;
  - survival tax F = Σ log₂|a_i| (Nair & Evans), which gives a minimum viable size.

**Premises.**
- A Gaussian world or the best *linear* tracker (THEORY:88).
- In a two-state switching world, the Bayes adaptation time is a single log: t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1] (CM N16 MATH-CORRECTED).
- Squared-error loss: a = b = 1/α holds only at p = 2 (THEORY:118; v1.4.16). "The optimum depends on the loss" was the biggest finding of 15 Nov (SYN:81–100).

**Not predicted** (THEORY:101–104):
- no adaptation slope of 1 (Fairhall is outside the map);
- need hazards are a different object from the kernel (THEORY:106, two memory objects).

**Binding rule: regime first.** With no measured α (or β), q and N on the system itself, there is no GTAO exponent prediction (THEORY:114, THEORY:153; QUEUE:8).

**The open bet (THEORY:33, THEORY:59; CM:351 N13 OPEN; CM:284 J6 OPEN).**
- **Claim.** Real, strongly selected systems sit near these optima once α, q, N and stakes are measured on the same system, with the same *relations* (not the same constants) at every level.
- **Status.** It is untested (THEORY:144; README:22). It is credible only if one relation holds in the same form in two or more very different substrates measured independently, and that has not happened (THEORY:8).
- **Kill rule** (THEORY:59, THEORY:318–329):
  - two strongly selected systems at different scales miss, while a named rival (fixed budget share, or universal ½) fits better;
  - a causal form via κ_F;
  - the pass rule mirrors the kill rule (v1.4.17);
  - the prereg locks the optimum, the loss and the rival family (v1.4.16).

**Formal layer** (proved in-model with corrections; THEORY:16, THEORY:150–154, THEORY:279–296):
- Bridge: a = b = 1/(1+2H) (N7).
- Pooling-onset exponent: −1 for reset reads and −(1+θ) for priced precision, at every α (N12 MATH-CORRECTED).
- Onset threshold N* = (√(1+ρ)+1)²/ρ.
- Vigilance floor 1+(1+ρ)^{−1/2}. The old "≥ 2" is wrong (THEORY:16).
- Ordering threshold κ*.
- Freeze/hold/lookup band (T8; CM:179 F13 PROVED):
  - a hold band exists iff μuH_l > 2c + hH_l;
  - freeze edge q_f = 2c/(WH_l²);
  - lookup edge q_c = (μu−h)²/(2cW);
  - a shared store widens the band by N² (FW:316).
- Theorem G: a checked copy beats fading iff drift × check cost < Φ (THEORY:164–172).
- Six items are candidates for the theory's own content (THEORY:290–296). Forward-citation sweeps are owed before any public novelty claim (THEORY:298).
- Design rules: bet-hedging FAILS "every system pays for a model" as stated (Kussell & Leibler; THEORY:164–172; CM:319 K18 MATH-CORRECTED).

---

## 2. Scope: atoms to the cosmos. What the docs say, Chad's positions, and the unresolved disagreement

**Physics, as THEORY §2.3 records it.**
- **Literal floors.** For example, kT·σ²/(2D) to track a random walk to error D; inflow ≥ (1−η)·I bits (Mitter & Newton; Horowitz & Sandberg) (THEORY:122).
- **Not literal above the cell.** Synapses run about 10⁵ × kT ln 2 per bit (Laughlin 1998) (THEORY:123). The 10⁵ figure is flagged as not re-verified (SCREV §5 item 7).
- **Same at every scale.** Growth ≤ disequilibrium + information − house take; no-arbitrage (THEORY:124).
- **Night-1 referee.** The physics is decorative in the formal layer (THEORY:125).

**OPEN DISAGREEMENT (Chad, t1908; THEORY:126).**
- Chad's position: "the physics is not decorative. The same three costs (holding a memory, predicting, upkeep) apply at every level from atoms to cities; the thermodynamic floor binds tightly at the cell and constrains less at firm scale."
- VFE = TFE holds only in a special case (CM:302 K1′ OPEN; the general identity K1 is WITHDRAWN).
- What would settle it: FW §3.11 β_phys, SENSE-CELL.
- Scale invariance holds only if one currency dominates (Theorem S, THEORY:127).

**CLAIM_MAP rows on this.**
- J10′ (CM:289) OPEN: "Physics applies at every level as a floor; it constrains design only where β_phys ≈ 1". The physics is "idle in the proofs, not false".
- J16 (CM:295) "same three costs" OPEN. In the model it is Axiom 5, so the model cannot test it. In the real world it is testable via J6: it fails if a fourth cost is needed or if design does not respond to measured prices (FW:402).
- K3 (CM:304) "judgment = staying alive under the second law" OPEN (framing).
- J10 (CM:288) "energy governs above the cell" WITHDRAWN.

**FW's scope proposal (FW:42), which is still unresolved and explicitly Chad's call.**
- "The cost accounting, including physical floors… applies from atoms up. The design predictions… need Axiom 7 (selection). An atom or a crystal has physics but no selection over tracking designs."
- Proposed scope: floors at every scale, and design predictions wherever there is selection, "from cells (and arguably self-replicating chemistry) upward".
- FW calls this "a scope disagreement worth Chad's call, not a correction". I found no record of Chad's decision.

**β_phys by scale (FW §3.11, FW:390–400).**

| Scale | β_phys |
|---|---|
| Cell | INCONCLUSIVE (N24: 5–21 vs the preset band [1, 10]) |
| Neurons | ~10⁵ |
| Ant, person, firm, city | astronomically > 1: "physics is a floor, not a constraint" |
| AI | ≫ 1 |

FW:46: "physics is not decorative in the theory's scope. It is idle in its current proofs."

**Atoms, persistence, freeze or hold** (frozen history, 11 Nov):
- **HYP:12, H8 (Chad's refinement).** Two kinds of persistence:
  - free: conservation or topology, as in the proton or a Skyrmion;
  - paid.
  - Free things formed in a past non-equilibrium flow (hadronization, baryogenesis, Sakharov 1967) and then froze: "formed in a flow, then either frozen (free) or held (paid)". Status: open, with a check for analogy creep.
- **HYP:18–23, H9 "Freeze or hold"** (Chad: "that locks it"). The tradeoff applies only to the held part. In Looper, the Git history is the frozen part and the store is the held part (this matches Looper README R4, `<private-app-repo>/README.md:22`, v0.16).
- **HC2:178–227, C6.**
  - It is the core bet that carries this.
  - The reviewer's warning (HC2:214): "the physics half (protons, crystals) is illustration only. The theory claims nothing about how physical structure froze."
  - The coverage table (HC2:747) says the same: "illustration with no test, by design".
  - HC2:218 credits the pattern to Chad's refinement.
- **The tension.** C6's "illustration only" (a reviewer, 11 Nov) sits against Chad's later t1908 "physics is not decorative" (THEORY:126). It is unresolved.
- **The formal successor of C6.** T8, the freeze/hold/lookup band (CM:179 F13 PROVED in-model). Its field tests:
  - measles: PROXY-PASS, substance PRIOR ART (CM:240 H9);
  - WIKIDATA-BAND: N19 OPEN / N20 PROXY-PASS weak;
  - immune: PRIOR ART, Mayer 2016 (CM:260 I4).

**Black holes and the cosmos.**
- THEORY, FW, CM and LIT contain no black-hole or cosmological content (grep of the repo: 0 hits).
- The only black-hole text is in the frozen hypothesis logs:
  - **HYP:5, H1:** "Black holes: maximal storage, not organizers. Kill: any black hole showing anticipation… Source: scope condition (only paid persistence carries models). Status: unaudited."
  - **HC2:712:** H1 was filed as background: "a scope condition. Its kill… is not a test anyone expects to run."
- Related:
  - HYP:104 H37: particles have laws, not models; "particles predict" is a flagged imposter (HC2:714).
  - HC2:729: "a universe choosing", "the proton containing the universe" and similar were retired as imposters.
- **Chad's current position** (t1923, recorded in shared memory, 18 Nov; not yet in any repo doc): the three costs apply from atoms to the cosmos, and the theory should directly predict what black holes are.
- **This is unresolved.**
  - The docs' only stance (H1) was written as an unaudited scope condition, and its "maximal storage, not organizers" reading runs against Chad's t1923 view.
  - A deep pass is in progress (`<local>/scale_ends/`, which has Smolin source files and no written output yet).
  - No doc derives a black-hole prediction.
  - Do not say the theory is "silent". Say: "the only written stance is unaudited hypothesis H1; Chad holds the theory should predict black holes directly; that derivation is open."

**Public record that conflicts with Chad's current view.**
- `<local>/gtao/v5/X_TEXT_v9_final.txt:4` (posted 12 Nov) says: "One principle runs from atoms to cities, the second law… Atoms and molecules follow it on average, settling and reacting with nothing to maintain."
- That treats atoms as having no upkeep, while THEORY:126 (Chad, t1908) says the same three costs apply at every level from atoms.
- The X correction post is blocked on Chad (SYN:118–127).

**Prior-art threats at the bottom end.**
- England's dissipative adaptation CONTRADICTS "judgment is the way" and SUPPORTS physics being literal at the bottom (LIT:20–35).
- It threatens "atoms as agents" (THR:86).
- Literal physics is fine for floors and risky for point predictions (THR:113–115).
- `litmap/LEFT_ON_THE_TABLE.md:127–153`: T3a as the level condition gives "atoms as agents" a cost condition.

---

## 3. The measurement framework (FW, 15 Nov). It exists, and here is what it does

**Why it exists.** Chad, t1908: "every field 'kill' and 'hit' so far tested a proxy whose validity nobody had checked… the single largest methodological gap" (FW:5).

**The logic: T∧M∧A ⇒ X** (FW:26–31).
- A failed prediction refutes only the conjunction of theory, measurement mapping and auxiliaries.
- The measles "pass" loses standing in the same way the Enron "kill" does.
- Pushback (FW:35–41):
  - math kills stay dead (MATH-CORRECTED / WITHDRAWN);
  - SIM-FAIL is not a proxy result;
  - a proxy fail carries information, because it kills that mapping;
  - the relabel is honest only if the gates are fixed now and every result is counted (anti-FEP).

**What a valid test needs** (FW:51–57): the empirical content is relations between independently measured quantities. A valid test measures at least two quantities independently in the same system.

**Quantities, and how each is measured** (FW §3, FW:116–414):
- **§3.0 (FW:116–135): target, pool and level, per scale.** The scales are cell, immune, ant, person, team/firm, city and AI (FW:106–112). There is no atom or cosmos scale. A "level" is a tracker consumed by at least two members, not a job title.
- **§3.1 (FW:137–164): q, H and α.**
  - Measured by variogram over at least 1.5 decades.
  - Need is not drift. P1, MATCH1 and measles conflated them.
  - Known groups: measles q ≈ 0 vs H3N2.
  - Validated estimators: a Whittle fit needs ≳ 250 Fourier frequencies; an HMM needs ≳ 16 switches (`measurement/estimators/RESULTS.md` §0).
  - DFA is biased under noise.
- **§3.2: ρ.** A factor model. κ is a hidden auxiliary in vigilance.
- **§3.3: stakes.** Read from the error-cost curve, using natural or designed variation.
- **§3.4: sensing class (a, b).** Measured separately for members and for the level. The class R a = b = ½ written there is an α = 2 instance (FW §3.4; AUD:16).
- **§3.5:** upkeep h.
- **§3.6:** the vigilance V formula, with a flat comparator.
- **§3.7:** onset N*.
- **§3.8:** the T8 band (FW:316), with a per-scale table: immune is Mayer 2016 (FW:328); AI weights = freeze (FW:333).
- **§3.9:** κ, the sharing decay. Enron must not be rescued after the fact (FW:353).
- **§3.10:** the selection-resolution gate ε (Axiom 7), computed before outcomes. Selection is strong for cells and weak for cities.
- **§3.11:** β_phys (§2 above).
- **§3.12 (FW:404–414): self-application to this bot.** A stale shared store is the predicted failure when the refresh rate falls below the drift. This is an anecdote, not a test. **That is exactly what happened to Ace's memory**, and it is the same root cause AUD found on 15 Nov (AUD:9–13: "I answered from copies").

**Validity gates and tiers** (FW:64–99).
- A measurement triple is target, pool and channel set (MV1).
- Gates MV1–MV10. MV9 needs an external timestamp, which needs Chad's go. MV10 is a power gate at lock.
- Tiers:
  - Tier 1 passes all gates;
  - Tier 2 passes MV1–4 and MV8;
  - Tier 3 is everything else.
- Anti-rescue admissibility rule: two Tier-2 fails in different systems count as one Tier-1 (FW:87).

**Status vocabulary** (FW:90–99; CM:79–94):
- PROVED (in-model), MATH-CORRECTED, PROXY-FAIL/PASS, SIM-FAIL/PASS/INCONCLUSIVE, OPEN, PRIOR ART, NOT EVIDENCE, WITHDRAWN, DECIDED, INCONCLUSIVE.
- FIELD-FAIL and FIELD-PASS are reserved for Tier 1, and "no row currently has either".
- Fair kills by tier (§6, FW:576–653): Tier 1 can kill; Tier 2 can only DISFAVOR; Tier 3 is logged only.

**How it changed every result** (FW §4, FW:418–551):

| Test | Before | Under FW |
|---|---|---|
| P1 news recall | — | PROXY-FAIL, the strongest; fails MV2, 3, 5, 7 (FW:436) |
| A1 | — | PROXY-FAIL; the weak form is PRIOR ART (FW:442) |
| MATCH1 measles | "hit" | PROXY-PASS, substance PRIOR ART (Mayer 2016); it measured use rate μ, not drift (FW:457, FW:541; CM:240) |
| VIGIL P1 | — | PROXY-PASS + Mintzberg prior art; P2, P3 OPEN; P4 NOT EVIDENCE (FW:472–475) |
| Enron | — | PROXY-FAIL (FW:490) |
| LANG1 | — | PROXY-FAIL, out of domain (FW:500) |
| τ / temperature tests (C3, F1, DECISIVE) | — | PROXY-FAIL **and out of scope for the structural core**, because failure rates are first-passage physics (FW:509, FW:515) |
| Simulations | — | NOT EVIDENCE / SIM-FAIL (FW:529–533) |

Net: no FIELD-FAIL and no FIELD-PASS (FW:551).

**Decisive tests it designed** (FW §7, FW:657–681): AI mixed-technology onset; GitHub read rate; the Wikidata band; plus a physics route, E. coli β_phys. Ranking (FW §5, FW:555–572): designed AI (21), GitHub (18), Wikipedia/Wikidata (18), influenza (14), chemotaxis (14, "best route to Chad's physics point").

**Limits** (FW:685–691; CM:393):
- FW was written in under an hour and is not independently reviewed.
- The gates are DECIDED but bind only after Chad signs off (CM:329). I found no sign-off.

**Tests run since FW**, all labelled under it:
- KERNEL-MEASURE VIX: passed on proxy, exploratory (THEORY:141).
- SENSE-CELL N24: INCONCLUSIVE (§4 below).
- N21 and N22 CAISO: INCONCLUSIVE.
- N23 lab forecasters: weak PROXY-PASS at the boundary.
- N19/N20 Wikidata: OPEN / weak PROXY-PASS.

None of these is Tier 1.

---

## 4. Claim map, item by item

- **Source:** CM v2.38.
- **Tally** (CM:368–379; covers the 167 v2 rows only): PROVED 41 · MATH-CORRECTED 20 · PROXY-FAIL 12 · PROXY-PASS 2 · OPEN 43 · PRIOR ART 19 · SIM-FAIL 6 · NOT EVIDENCE 13 · WITHDRAWN 9 · DECIDED 2.
- **Bottom line:** "untested, not refuted" (CM:96).
- **The full table** of every row (file line, id, claim, exact status label, reason, with long text truncated at "...") is in **`<local>/gtao/_cm_rows.md`**. It has 198 rows, extracted mechanically from CM:103–362.

**Key rows:**

| Row | Claim | Status | Reason |
|---|---|---|---|
| J3 (CM:281) | "law" | WITHDRAWN | — |
| J6 (CM:284) | cross-substrate same relations | OPEN | the real cross-substrate content |
| J10 (CM:288) | energy governs above the cell | WITHDRAWN | — |
| J10′ (CM:289) | physics is a floor everywhere; it constrains where β_phys ≈ 1 | OPEN | — |
| J11 (CM:290) | — | OPEN | — |
| J14 (CM:293) | title | DECIDED (keep; t1908) | — |
| J15 (CM:294) | causal chain | OPEN | — |
| J16 (CM:295) | same three costs | OPEN | — |
| K1 / K1′ (CM:301–302) | VFE = TFE general / special case | WITHDRAWN / OPEN | — |
| K3 (CM:304) | second-law framing | OPEN | — |
| K4 (CM:305) | τ joint kill | PROXY-FAIL | "a proxy fail, not a field kill" (THEORY:263) |
| K12, K13 | spectrum core | MATH-CORRECTED | — |
| K18 (CM:319) | "every system pays for a model" | MATH-CORRECTED | Kussell & Leibler bet-hedging |
| H1 (CM:232) | — | PROXY-FAIL | — |
| H8 (CM:239) | vigilance in firms | **OPEN** | fair-kill spec FW §6.3 |
| H9 (CM:240) | measles freeze-or-hold | **PROXY-PASS** | MV2, 3, 5, 6, 7, 9 fail; substance PRIOR ART |
| H11–H15 | τ / temperature | PROXY-FAIL | out of scope |
| F13 (CM:179) | T8 band | PROVED (in-model) | — |
| I4 (CM:260) | immune freeze/hold/lookup | PRIOR ART | Mayer 2016 |
| M1 / M2 / M4 | method rows | PROVED / DECIDED (needs Chad's sign-off) / OPEN | M4 is the bot self-application (CM:329, CM:331) |
| N1, N2 | — | PROXY-PASS (downgraded) | — |
| N3, N13, N15, N19 | — | OPEN | N13 is the core bet (CM:351) |
| N5 | — | PROXY-FAIL (scope) | — |
| N10 | — | PROXY-PASS (non-discriminating) | — |
| N11 | — | PRIOR ART | — |
| N12, N16 | — | MATH-CORRECTED | — |
| N14, N17 | — | PROXY-FAIL | — |
| N18 | — | DECIDED | — |
| N20 | — | PROXY-PASS (weak) | — |
| N21, N22 | CAISO | INCONCLUSIVE | gates failed |
| N23 (CM:361) | lab forecasters | PROXY-PASS (weak, boundary) | D = 0.518 vs kill line 0.492 |
| N24 (CM:362) | SENSE-CELL | INCONCLUSIVE (Tier 3) | see below |
| G rows | — | SIM-FAIL: G6, G9, G15–17, G20; SIM-INCONCLUSIVE: G23, G25 (T1.8 not passed), G28 | — |

**SENSE-CELL, the cell test** (SCR:3, SCR:11–14; SCREV:7, SCREV:12–13, SCREV:63, SCREV:79–81):
- **H2.** The locked rule output FAIL, but on a *mismatched proxy*: Keegstra 2017, the whole Tar/Tsr array, at 500 µM, where accuracy is limited by methylation-site saturation and not by energy. That output is not counted against the theory.
- **Like-for-like β:**
  - Lan wild-type: 11 [7.4, 20.5];
  - Tar anchor: 6.2 [4.6, 8.7], which is circular. Lan's "99%" is a Tar *model output* at an assumed 20% efficiency, not a measurement.
- **H1 is INCONCLUSIVE.** θ_eff = 0.24–0.53 leans per-nat.
- **H3 is INCONCLUSIVE. H4 is a data gap.**
- **The "15–40×" line is withdrawn.**
- **Supported:** energy cost rises with the log of accuracy.
- **Before the lock**, the author predicted H2 INCONCLUSIVE and H1 PASS (SCP:12).
- **No outcome changes N6 or N13** (SCP:43).
- **What a matched test needs:** Tar-only FRET, a small step, an energy readout and an ε0 control. None is public (SCREV:63).

---

## 5. Queued and blocked

**Rules.**
- Proposition SG orders the queue (THEORY:154).
- "Read at use… Do not work from a summary" (QUEUE:7).
- Continue up to 90% of weekly usage, at nice 19 (QUEUE:16; t1914).
- Privacy rules (QUEUE:18).
- Next pick is 40, the uniform slot (QUEUE:443). The LEDGER's last entry is 190 (18 Nov 07:20).

**Top tests** (SYN:104–112; QUEUE):
1. SAME-SYSTEM-AQN, the first real test of N13 (QUEUE:120).
2. BAYES-LINEAR-LAB, **blocked on Chad** (QUEUE:402).
3. STAKES-SHIFT-MULTIYEAR (QUEUE:250).
4. KERNEL-DECISIVE-RV (QUEUE:351).
5. SENSE-CELL, now DONE (QUEUE:77).

**Other open items:**
- ONSET-ACROSS-ALPHA-PRICED (QUEUE:375)
- MIXED-ALPHA-ONSET (QUEUE:117)
- RELATIVE-BAND-TOST and HIT-ZERO-MISS-FLOOR (QUEUE:440–441; top of the open-only sg rank at 2.8 and 2.4)
- Q9 IMMUNE (QUEUE:90)
- FROZEN-DOC-POINTERS (QUEUE:123)

**Blocked on Chad:**
- SENSE-CELL-MATCHED (QUEUE:444; contacting authors needs Chad).
- SENSE-CELL-EFFORT (QUEUE:446).
- BAYES-LINEAR-LAB.
- From SYN:118–127:
  - contacting data authors or participants;
  - the X correction post;
  - making the repo public;
  - Looper README wording.
- Also: sign-off on the M2 gates (CM:329), MV9 external timestamps (FW:685–691), and the FW:42 scope call (atoms / selection).
- The black-hole and cosmos derivation is in progress, with no output yet.

---

## 6. Video v4 vs the current docs

The video files are VS (main narration, v2 text, unchanged in v3/v4 per VF:118), TS, VD, VF and VDESC. Final render: `final/gtao_explainer.mp4` (11:01 ET).

| # | Video claim | Current doc | Correction |
|---|---|---|---|
| V1 | Score: "Failed on proxies: several, reported as they came out… Confirmed in the field: nothing yet. Refuted… nothing yet" (VS:20; TS:7 "A few proxy tests passed, several failed") | The fails are proxy fails because no test measured GTAO's quantities validly; FW exists, re-audited every test, and found 0 Tier-1 results. "Untested, not refuted" (FW:5, FW:26–31, FW:551; THEORY:14) | Say why: no past test measured the theory's quantities validly; a measurement framework now defines valid tests; none decisive has run yet. This is Chad's exact point |
| V2 | The video never mentions the measurement framework, its gates and tiers, or that the first job is measurement (whole script) | FW:64–99; THEORY:144 "first job is measurement" | Add a scene: "how we will measure it" (triple, gates, tiers; what a fair test needs) |
| V3 | Firms: "The theory's specific structure failed on that proxy" (VS:15) | τ/temperature tests are PROXY-FAIL **and out of scope** for the structural core: failure rates are first-passage physics (FW:509, FW:515); "a proxy fail, not a field kill" (THEORY:263) | Say the bank test checked a side prediction (shock × √time-to-fix ÷ buffer), outside the core, on a proxy |
| V4 | Brains: "Tests on people so far are mixed. A news recall prediction failed on its proxy" (VS:14), next to brain-energy content; VD:44 puts a FAILED ON PROXY chip in the brains scene | P1 fails gates MV2, 3, 5, 7: need was proxied by headline-word recurrence (FW:436). It is about people's recall, not brain energetics | Separate the two, and say the proxy itself was invalid |
| V5 | Hook/bet/payoff: "from chemistry to cities" (VS:8, VS:22; VD:17); teaser "from cells to cities" (TS:5) | Chad: same three costs "from atoms to cities" (THEORY:126, t1908); now "atoms to the cosmos" (t1923, memory). FW:42: floors from atoms up, design predictions only where there is selection (unresolved, Chad's call) | Use Chad's range and state the open scope question; make main and teaser consistent |
| V6 | Physics: "where the theory expects the thermodynamic floor to bind most tightly… above the cell it constrains less" (VS:17) | This is Chad's stated position in an *open disagreement* with the night-1 referee's "decorative" verdict (THEORY:125–126); FW:46 "not decorative in scope, idle in current proofs"; J10′ OPEN | Present it as a disagreement with a defined test (β_phys) |
| V7 | No freeze/hold content anywhere | H8/H9 (Chad's): frozen vs held persistence; C6; T8 band PROVED in-model (CM:179); measles PROXY-PASS (CM:240) | Add it. It is Chad's bridge from physics (frozen) to life (held) |
| V8 | No black-hole or cosmos end | Only H1 (unaudited, HYP:5); Chad says the theory should predict black holes (t1923) | Do not imply the scope stops at chemistry; mark the cosmic end as open, under derivation |
| V9 | Markets: "the index leans on old readings about as much as the best possible tracker would" (VS:16) | "the best **linear** tracker computed from the driver's spectrum"; it "tests the linear optimum's map, not Bayes vs linear"; proxy validity "consistent, not certified" (THEORY:141) | Say "best linear tracker" |
| V10 | Score: "Proved inside the model: the math, after hostile review and corrections" (VS:20) | The formal layer is proved in-model with corrections, but THEORY is "not independently reviewed as a whole" (THEORY:4); much of it is classical or prior art (THEORY:116); novelty is unswept (THEORY:298); M1/M3 are self-checked (CM:393) | Say "the formal math holds inside the model; much of it is classical; the rest is unreviewed for novelty" |
| V11 | Bet: "Now, the part that is new" means the empirical bet only (VS:8) | GTAO adds the bet **and** the formal layer: six candidate own-content items, including the vigilance floor, onset and the freeze/hold band (THEORY:116, THEORY:290–296) | Mention the formal results as candidates |
| V12 | Cells: "A model is kept only while it pays" (VS:11) | K18 "every system pays for a model" MATH-CORRECTED; bet-hedging can beat sensing (Kussell & Leibler; THEORY:164–172; CM:319). Mitchell 2009 is not in THEORY (it is in LIT/PRIOR_ART) | Add the caveat or soften |
| V13 | Origin: "first systems to persist would be those whose memory was worth its upkeep" (VS:10), labelled hypothesis | Not in THEORY; H2 is unaudited (HYP:6). England's dissipative adaptation is a named rival that contradicts "judgment is the way" (LIT:20–35; THR:86) | Name the rival if the segment stays |
| V14 | Sink: "measured properly" (VS:21) | "Properly" means Tier 1 under FW gates, which Chad has not signed (CM:329) | Tie "properly" to the framework |
| V15 | Next tests: "in markets and in bacteria" (VS:21) | FW §7's decisive tests are AI onset, GitHub and Wikidata; SYN:104–112 puts SAME-SYSTEM-AQN first; the bacteria matched test is blocked on Chad (QUEUE:444) | Update the list |
| V16 | Brains on screen: "synapse ~10,000 ATP per bit" (VF:110) vs THEORY:123 "~10⁵ × kT ln 2" | Different units, both cited; the 10⁵ figure is not re-verified (SCREV §5 item 7) | OK, but note the unit difference |
| V17 | VF:3 / VD:5 call THEORY v1.4.17 and CM v2.38 current | Correct for the repo. THEORY:6 itself still says CM v2.37 | Fine |
| V18 | Cellslot (VS:19) | Matches the SCREV approved wording and N24 INCONCLUSIVE | OK |
| V19 | VIX 0.26 vs 0.28 "passed on proxy, exploratory, not decisive" (VS:16) | THEORY:141 | OK |
| V20 | Ants SIM-FAIL "narrows the claim" (VS:13) | CM G15; N1 limited to linear readouts | OK; it is simulated ants, not real ants |

---

## 7. Corrections for Ace's memory

1. **The measurement framework exists.**
   - FW was built 15 Nov at Chad's t1908 request. It holds triples, gates MV1–10, tiers and an anti-rescue rule.
   - It re-audited all tests and found 0 FIELD-FAIL and 0 FIELD-PASS (FW:5, FW:64–99, FW:551).
   - Never say "no measurement framework". Say: "the framework exists; no Tier-1 test has been run; the gates await Chad's sign-off" (CM:329, CM:393).
2. **"Failed on proxy" is not a real-world failure.** It is T∧M∧A (FW:26–31). Under FW, measles moves from "passed" to PROXY-PASS / PRIOR ART (CM:240), even though THEORY:258 still says "passed". Report both.
3. **Scope is not "chemistry/cells to cities".** Chad: atoms to cities (THEORY:126), now atoms to the cosmos (t1923). FW:42's selection-scoped proposal is unresolved and his call. Never say atoms' bills are "zero".
4. **Black holes.** The only written stance is unaudited hypothesis H1 (HYP:5; HC2:712). Chad wants a direct prediction. It is open and in progress. Never say the theory is silent.
5. **Physics is an open disagreement, not settled.** Chad: not decorative (THEORY:126). FW:46: idle in the proofs, not false (J10′ OPEN). SENSE-CELL did not settle it (N24 INCONCLUSIVE).
6. **Freeze vs hold** (H8/H9, Chad's): free/frozen persistence vs paid/held persistence; the formal T8 band is PROVED in-model (CM:179). C6 called the physics half illustration (HC2:214); that is in tension with Chad.
7. **The τ / temperature results** (banks, C3, F1, glucose) are PROXY-FAIL and out of scope for the core (FW:509, FW:515). They are not failures of the theory's structure.
8. **Vigilance (H8) is OPEN** (CM:239). The floor is 1+(1+ρ)^{−1/2}, not ≥ 2 (THEORY:16).
9. **Theory, not law** (CM:281). Not a theory of everything (THEORY:35). "Every system pays for a model" is MATH-CORRECTED (CM:319).
10. **The Looper README is v0.16, not "contract 0.15"** (`<private-app-repo>/README.md:3`; commits 2d1ffbb/9c49188, 12 Nov, approved by Chad). R4 encodes freeze vs hold (README:22).
11. **MEMORY_BRIEF.md is stale.**
    - It cites main 77dd71c and CM v2.37 (MEMORY_BRIEF:3); the current state is 4b7a6a1 / v2.38.
    - It omits FW entirely.
    - It says "measles freeze-or-hold passed" (MEMORY_BRIEF:65), but CM H9 says PROXY-PASS.
12. **Pointer files are stale.** `<local>/gtao/STATE.md` still says THEORY v1.2 at main db6ee2d. Read THEORY/STATUS at use. AUD:9–13 records the same failure on 15 Nov.

---

## 8. Conflicts between files (listed, not resolved)

- **Version pointers:**
  - README:11, README:90 say THEORY v1.4.3a; THEORY:1 says v1.4.17.
  - README:37, README:54 say CM v2.12.
  - THEORY:6 says CM v2.37; STATUS:10 says v2.38.
- **CM counts:** the header (CM:364) says 194 rows; the N rows now run to N24.
- **ANTS1:** "unfinished" in README:83, README:103, `tests/README.md:23` and `applications/README.md:24`; THEORY:260 says "finished 15 Nov, 3 locked in-model failures".
- **Measles:** THEORY:258 says "passed"; CM:240 and FW:457, FW:541 say PROXY-PASS / PRIOR ART.
- **Spectrum map:** FW §6.10 (FW:653) says the spectrum → exponent mapping is "owed… OPEN"; THEORY §2.2 now derives it (THEORY:90–99).
- **Class R:** FW §3.4 states class R a = b = ½, an α = 2 instance (AUD:16).
- **Queue:** `queue/items.json` has SENSE-CELL and CAUSAL-KAPPA-LENIENCY-REVIEW still open, while STATUS and LEDGER say done; SENSE-CELL-MATCHED and SENSE-CELL-EFFORT are missing from it.
- **M2:** marked DECIDED, but it needs Chad's sign-off (CM:329). None found.
- **SENSE-CELL text:** the RESULTS body text is superseded by its banner (SCR:3).
- **THEORY:126** still names SENSE-CELL as the test that would settle the physics disagreement; it has run, and the result is inconclusive.
- **Physics and scope:** C6 "physics half is illustration only" (HC2:214) vs Chad's "not decorative" (THEORY:126) vs FW:42 (selection scope).
- **Public post vs Chad:** the 12 Nov post says atoms have "nothing to maintain" (X_TEXT_v9_final:4); Chad says the same three costs apply from atoms (THEORY:126).
- **Black holes:** HYP H1 "maximal storage, not organizers" vs Chad's t1923 "theory should directly predict what black holes are".
