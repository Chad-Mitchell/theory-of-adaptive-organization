# BOOKENDS: how the pieces of GTAO fit together, from chemistry to heat death, and what follows at each level *if* the theory is right

**Revision 2.** Wednesday 18 November 2026, about 7:30 to 9:00 PM ET (America/New_York). Revision 1 was written about 5:40 to 7:00 PM ET. Written by a Grok Bot executor for Chad Mitchell, via Ace, on branch `bookends` (Chad, t1943, t1944, t1945, t1946). Nothing was posted or sent.

**What revision 2 changes.** Three independent reviews of revision 1 were held outside the repo:
- MATH_LOGIC: FAIL, fixable;
- PHYSICS: PASS-WITH-FIXES;
- BIO_PRIORART: PASS-WITH-FIXES.

Every blocker, major and high finding is addressed here. The disposition, finding by finding, is kept with the reviews. The main changes:
1. "Response" and "action" are now separate terms (§2.0).
2. The pre-heredity tier is now *survival-relevant (semantic) information*, not a "model". It has an explicit test that flames, dunes, hurricanes and galaxies are expected to fail.
3. "Model" now means the internal-model-principle sense: proportional feedback holds no model, and integral feedback is the minimal one.
4. Theorem P gets a finite-horizon form and an explicit mapping lemma.
5. The onset order is a HYPOTHESIS.
6. The physics corrections: the second law is the backbone but not the only principle; Landauer applies to erasure; galaxies, hurricanes and the carbonate–silicate cycle are reclassified; black-hole read delay follows Hayden & Preskill; light delay binds only off-planet.
7. The planet's information sits in the biosphere; humans make Earth forecast ahead.
8. Credit is restored for "shared fate" and for missing prior art.
9. The proposals are renamed BK-P1…BK-P14.

**Status of this file.** This is a derivation and synthesis file. It **does not edit** THEORY.md, `theory/SCALE_ENDS.md`, CLAIM_MAP or THEOREMS. Its proposals (§6) are **listed, not applied**. Its own synthesis is **unreviewed in revision 2** and is not self-certified. If it disagrees with THEORY.md, THEORY.md governs.

**What kind of claim.** GTAO is a falsifiable causal theory. It is not a "law" and not a theory of everything. In the field it is **untested, not refuted** (FRAMEWORK §2.3; no row has FIELD-PASS or FIELD-FAIL).

**Labels.**
- **PROVED (in-model):** a CLAIM_MAP theorem inside the model. It says nothing about nature by itself.
- **DERIVED:** follows from the theory's own results plus stated mappings or published physics. Where the derivation is new here, it is marked **[BK, new, unreviewed]**.
- **PRIOR ART:** published by others and credited.
- **HYPOTHESIS:** a real-system claim with a stated kill.
- **OPEN:** not settled.
- **IMPOSTER:** sounds like it follows from GTAO but does not. Rejected.
- **ANALOGY:** a borrowed formula whose premises do not hold, used for direction only.
- **CLASSIFICATION (not a prediction):** a placement that no data could fail.
- Labels quoted from a source file are kept exactly as that file states them: PROOF, KNOWN, NUMERIC, ELEMENTARY, FAILS, CONJECTURE, PROOF + NUMERIC, MATH-CORRECTED, WITHDRAWN.

**Identifiers.** IDs are prefixed with their file: SE- for SCALE_ENDS (SE-E1…SE-E4, SE9), GT- for GENERAL_THEOREM (GT-P0…GT-P3), IM- for INTERNAL_MODEL (IM-I5), CM- for CLAIM_MAP rows (CM-N25, CM-H8), TH- for `theory/THEOREMS.md` (TH-T3a, TH-T7), and H- for the local hypothesis file. This file's own items are BK-….

**Sources read.**
- Repo: THEORY.md v1.4.19 (status block, §0, §2.1–§2.3, §3–§7, §10); `theory/SCALE_ENDS.md` (all); `theory/GENERAL_THEOREM.md` §0–§2 and §5; `reviews/night1/formal/AXIOMS.md`; `theory/THEOREMS.md` T3 and T7; `theory/MATH_ATTACK.md` §3.2–§3.6; `measurement/CLAIM_MAP_v2.md` (rows cited); `measurement/FRAMEWORK.md` §1, §2, §3.10, §3.11; `BRIEF.md`; `litmap/LITMAP.md`, `PRIOR_ART.md`, `THREATS.md`.
- Local: the hypothesis files (H1, H2, H8, H9, H37, H80, and C13 in the reviewed core file). No personal content is reproduced.
- The 12 Nov X post supplies the spine.
- Primary sources opened by this author are listed under References. Each is marked "abstract", "page" or "metadata only".

---

## 0. Bottom line

1. **The spine.** Everything obeys the second law: total entropy rises, though local order can grow when it exports entropy. That law, together with gravity, the speed of light, quantum and gravitational physics, conservation laws, and the universe's unusually low-entropy start, sets the stage. GTAO adds no new physics. Its content is about **judgment under the second law**. Some structures last only by running free energy through themselves while staying matched to a world that changes and can ruin them. For those, once acting late is costly, carrying a model and acting ahead can pay (12 Nov post; GT §1: "k > 0 is acting late is costly").
2. **Four separate things, not one word "model".** This file separates:
   - (a) **correlation**: any mutual information with the world, which nearly every driven system has (Still et al. 2012);
   - (b) **survival-relevant (semantic) information**: correlation whose scrambling shortens persistence (Kolchinsky & Wolpert 2018);
   - (c) **a model** in the internal-model-principle sense: error feedback that contains the dynamics of the outside signal. Integral feedback is the minimal case, the model of a constant world (Francis & Wonham 1976; Yi et al. 2000 for bacterial chemotaxis). Proportional feedback holds none;
   - (d) **a selected model**: (c) whose design is shaped by selection (Axiom 7), which is where GTAO's design predictions live.

   Revision 1 blurred (a), (b) and (c). That blur is why it made flames and hurricanes look like "models".
3. **Corrections to the chat.**
   - "Models start at cells" was **wrong**. Selected models switch on with heredity below Eigen's threshold, which is below the cell (CM-N28 OPEN). Survival-relevant information, and even integral-feedback structure, are not excluded before heredity.
   - "Feedback isn't a model" was **wrong as stated**. Integral feedback on an outside variable is the minimal model. Proportional feedback, and feedback on one's own state, are not models of the world in this file's definitions. Excluding self-feedback is a **definitional choice**: Rosen 1985 counts "a predictive model of itself and/or its environment" (litmap).
   - "A planet would need selection between versions to have a model" was **wrong as stated**. Selection is needed for a *selected* model (Axiom 7), not for (b) or (c).
4. **The onset of knowing is graded and only partly ordered (HYPOTHESIS).** Correlation, survival-relevant information, minimal models, heredity and acting ahead are separately measurable. They need not arrive in that order: an entrained oscillator can act ahead without heredity.
5. **Frozen memory has a job.** Knowers are built from frozen structures, inherit through near-frozen stores (genomes: low-upkeep, repaired, updated across generations), read frozen records, and spend upkeep only on what drifts (the freeze edge of the T8 band; CM-F13 PROVED (in-model)). Black holes are the limit of keeping and predict nothing (CM-N26 PROVED (in-model), conditional; its conditions need rewording, §2.0.4). Most of the entropy now present in the observable universe is in supermassive black holes (Egan & Lineweaver 2010).
6. **Layers and governance follow from the same spine (§3).** A level is a shared model of a common driver (TH-T3a: PROOF, sufficient condition only). Architecture is self-similar only where the world is scale-free (TH-T7: PROOF (conditional); unconditional claim FAILS). Parts under-watch when failure costs do not reach them (MATH_ATTACK §3.4, PROOF). That is cured by **shared fate or enforcement** (J9 stays OPEN). Signal delay forces federation, and light delay is the floor that binds off-planet (CM-N27 OPEN).
7. **Planets and consciousness.** Earth's information sits in its biosphere, not its rock. Since humans, part of it forecasts ahead (climate models, asteroid tracking). GTAO has no variable for experience, so "GTAO shows a planet is or is not conscious" is an **IMPOSTER** claim. The question itself is out of scope.
8. **Status changes.** No status label in CLAIM_MAP would change under the proposals. Three rows would change their wording or stated conditions: CM-N25, CM-N26 and CM-N28 (§2.0.4, §6). §2.0.4 shows why the labels survive.
9. **Repo inconsistencies flagged (three).**
   - SCALE_ENDS labels its no-model class "H80's thermostat tier", though H80's thermostat tier tracks an outside target.
   - SCALE_ENDS and THEORY say "models switch on only with heredity" while Theorem P carries no selection premise. Under the Axiom-7 reading of "action" this is consistent, but the wording hides the choice (MATH_LOGIC's verdict, accepted).
   - `theory/THEOREMS.md` T7(iii) keeps the withdrawn L^{2/3} level count, where L is the log-span.

   Two smaller ones: THEORY §6 cites MATH_ATTACK "§3.5" for under-watching, but the result is in §3.4. GENERAL_THEOREM defines z = σ√τ/B, the inverse of THEORY's z = B/(σ√τ).

---

## 1. The picture in plain words

Everything runs downhill. Fuel burns, heat spreads, and the total disorder of the universe goes up. That is the second law. It does not mean order can't grow: crystals form, stars clump and living things build themselves, but always by pushing more disorder out somewhere else. The second law is the backbone of this picture. Gravity, the speed of light, and the fact that the universe started out unusually orderly set the rest of the stage. GTAO adds no new physics. It asks one question: **what does it take to last while everything runs downhill?** There are three answers.

**Keep.** Some things settled long ago into states almost nothing can knock loose: atoms, crystals and, at the extreme, black holes. They pay nothing to last. They carry traces of where they came from, but none of those traces helps them last, because nothing they do depends on getting the world right.

**Burn.** Some things last only by running energy through themselves: a star, a candle flame. They steady themselves. If a star's core runs hot, it expands, cools and burns slower. But they steady only themselves, and nothing outside has to be known for them to keep going. Storms burn too. A hurricane is a heat engine between warm sea and cold sky, and it dies when the water under it cools or it hits land. Its state follows the world but holds nothing about it. Whether that counts as "knowing" anything is an open question with a test (§2.2).

**Know.** Some things last only by running energy through themselves *and* staying matched to an outside world that changes and can kill them: a cell whose food moves, an animal, a company, a city. Knowing comes in steps:
- **Notice.** Many things merely follow the world. That is correlation, and it is everywhere.
- **Need it.** Some things would die sooner if that match were scrambled. Now the information matters for survival.
- **Hold a set point.** The simplest real model is a feedback loop that keeps adding up its error until the error is gone. A bacterium does this when it re-sets its sensitivity after a change in smell (integral feedback). That loop carries a tiny model of the world: "it will stay like this." A loop that only pushes back in proportion to the error, without adding up, does not.
- **Act ahead.** When the world arrives faster than you can react, you need a model of how it moves, such as a clock for a daily cycle. Then you act before it gets there. That is judgment. It is not a new principle, just a way of staying alive under the old one.
- **Pay for it.** Knowing is never free. Every knower has to balance **what to keep, what to check, and what to let go**. GTAO's bet is that the balance is set by how fast your world changes and how much a mistake costs you. That bet is testable and untested.

**How the three depend on each other.** Knowers are *built* from keepers: atoms, bonds, and DNA that is cheap to keep and repaired as it goes. They are *fed* by burners: a star's light, and heat and chemistry from a planet's interior. They *record* themselves in keepers: rocks, fossils, books. A good knower freezes whatever does not change and spends effort only on what does. Frozen memory is the cheap foundation knowing stands on.

**Knowing came on gradually (an idea, not a finding).** Chemistry first followed its surroundings, then depended on them, then perhaps held simple set points, then copied itself well enough for improvements to pile up, and then acted ahead. These steps may have come in a different order. The cell is the first place we know of where they were all packaged together.

**When many knowers face the same world, they share a model.** One trail, one price, one rulebook or one brain serves many parts. That is where layers come from. Shared knowledge goes stale unless each part bears the cost of the whole failing. That can happen in two ways: the parts share one fate (worker ants mostly can't breed, so the colony's success is their success), or someone enforces upkeep (a monitor, a rule, an owner). Ants also police each other, so even they mix both. And because no signal is instant, nothing large can know everything centrally. Big things federate. On Earth, slow people and slow wires set that limit. The speed of light is the hard floor, and it matters only off-planet.

**Where the bookends sit.** At the bottom, atoms have nothing to know. At the top, black holes keep the most for their size and predict nothing. Most of the disorder now in the observable universe is inside them. The universe is still far below its maximum disorder, and that gap is what makes every star and living thing possible. As it closes, knowing can last only as long as the last usable source of energy, which may be black holes slowly leaking long after the stars are gone. In an accelerating universe even that is finite.

**What it would mean if this is right.** The same few relations would hold from the first self-copying chemistry to cities: how often to look, how long to remember, when to share a model, when someone has to be in charge. Each would be set by how fast that level's world changes and what a mistake costs. You could look at an organization's world and say how it should be built. That is a bet, not a finding. §4 lists how to break it at each level. The top and bottom bookends (atoms, stars, galaxies, black holes, the cosmos) are **classifications, not predictions**: they place things in the picture, but no data could fail them.

---

## 2. The answers, with status

### 2.0 Definitions and the formal pieces revision 2 adds [BK, new, unreviewed unless labelled]

**2.0.1 Response vs action.**
- A **response** is any state-dependent physical effect of a structure on its own loss: A_t = π(M_t), with M_t its internal state. It needs no selection. A response is enough for Theorem P's information bound (GT-P0/GT-P1 use A1, A2, A5 and, implicitly, A4).
- An **action** is a response alternative over which a selection, learning or design process operates (Axiom 7; the reading THEORY §2.3 uses for "action"). Actions are needed for every *optimization* statement: GT-G2 (hold vs fade), Theorem 8, GT-P3 ("pays"), and all design predictions.
- Throughout, "pays", "optimal" and R\* need actions. "Required for persistence" needs only responses.

**2.0.2 Four notions of "knowing", kept apart.**

| Notion | Definition | Who has it | Test |
|---|---|---|---|
| Correlation | I(M; X) > 0, including predictive I_pred > 0 | almost every driven system (Still et al. 2012: a system "responding to a stochastic driving signal" retains information, "a fraction" of it predictive) | none needed; nearly universal |
| **Survival-relevant (semantic) information** | correlation whose scrambling, at fixed energy and matter fluxes, lowers viability (Kolchinsky & Wolpert 2018; viability = "ability to keep itself in a low entropy state", or a stated persistence time) | candidates: driven chemistry, storms, cells | **BK-SEM test:** scramble the state–drive correlation with a dose-matched sham; viability must drop. **Kill (non-model):** a drive-matched structure whose viability does *not* drop under scrambling at fixed fluxes holds correlation only |
| **Model (structural)** | error feedback containing a reduplicated model of the outside signal's dynamics (internal model principle, Francis & Wonham 1976). Minimal case: integral feedback, the model of a constant/step world; it gives robust perfect adaptation (Yi et al. 2000: chemotaxis; "integral control … necessary" for robustness). Proportional or leaky feedback holds no internal model; it leaves a steady error that shifts with the drive. A clock entrained to a cycle is an internal model of a periodic world | bacterial chemotaxis (integral); circadian clocks (oscillator) | **BK-IMP test:** after a sustained step in the drive, the regulated variable returns to its prior value, robustly to parameter changes. Flames, dunes and hurricanes are expected to fail (their state shifts with the drive) |
| **Selected model** | a structural model whose design is shaped by selection with resolution ε (Axiom 7) | cells and above, under strong selection | GTAO's design predictions (CM-N13, CM-J6, OPEN) |

"Feedback on own state only is not a model" is a definitional choice of this file, made so that the model concept stays about an exogenous world. Rosen 1985 (litmap; book not fetched) defines anticipatory systems to include "a predictive model of itself". Under Rosen's reading a star's core regulation would still not qualify, because its restoring force is proportional (no integrator) and it acts on no prediction.

**2.0.3 Theorem P on real structures: finite horizon and the mapping lemma.**
- **Finite-horizon corollary (DERIVED, elementary; i.i.d. or martingale-difference increments) [BK, new, unreviewed].** Let a blind structure (I_pred = 0) have reserve increments with mean −δ < 0 (δ = r_∞ − (y − c̄)) and |ΔR + δ| ≤ b. Survival to T implies R_T > 0. By Azuma–Hoeffding, **P(blind survives to T) ≤ exp(−(δT − B)²/(2b²T)) for T > B/δ**. Survival well past B/δ is therefore evidence, at stated confidence, that I_pred > 0. The bound was checked by Monte Carlo and holds, loosely (`theory/bookends_checks/finite_horizon.py`, `.out`: at T = 1600 the simulated survival is 0.003 against a bound of 0.17). **Limit:** in a Markov world the increments are dependent, and the exponent must be divided by a mixing-time factor. That version is not derived here (OPEN). GT-P1's original statement is infinite-horizon and cannot classify any observed structure alone (MATH_LOGIC finding 3, accepted).
- **Mapping lemma (DERIVED under stated premises) [BK, new, unreviewed].** For a non-replicating dissipative structure:
  - M_t is its internal state, declared before data;
  - A_t = π(M_t) is its response;
  - the reserve R_t is its stock of usable free energy, or a stated viability margin;
  - the influx depends on the world, y = y(X_t). Fold it into the loss as ℓ′(a, x) = ℓ(a, x) − (y(x) − ȳ), with ȳ = E[y(X)]. Then D(·) is computed for ℓ′, and ℓ′ must be bounded (A5);
  - **premises, checked one by one:** A1 (exogenous world) fails if the structure alters its own feed. A2 (stationarity) holds only in the stationary regime. A4 (one currency) holds when every term is free energy. A5 holds for bounded fluxes.

  **What the lemma gives:** a *floor* on I_pred. **What it does not give:** that the structure holds a model. If M is declared to be the coupled state itself, the floor is met automatically (MATH_LOGIC finding 2, accepted). So Theorem P supplies the *amount* of information persistence requires. BK-SEM decides whether that information is causally used. BK-IMP decides whether a model structure carries it.

**2.0.4 CM-N25 and CM-N26 under the two-term reading (re-derivation).**
- **CM-N25 (atoms).** Its CLAIM_MAP statement ("no action whose payoff depends on the world ⇒ Φ = 0 …; blind-viable + E1 ⇒ R\* = 0") is an optimization statement. It is true *as written* under the Axiom-7 reading it states, so its PROVED (in-model) label is unaffected. Under the response reading the parallel conclusion follows from SE-E2 alone, which is non-definitional. Atomic persistence is blind-viable: a Boltzmann factor of about 10^−228.5 for hydrogen ionization at 300 K, so D(0) ≤ y − c̄ and GT-P1 allows I_pred = 0. Its ionization hazard is set by the bath temperature, not by the correlation between the atom's own state and the bath, so scrambling that correlation leaves viability unchanged: semantic information 0 (DERIVED; physical argument, not computed). It holds no integrator on any external variable, so it has no model. **Wording change proposed (BK-P6). Label unchanged.**
- **CM-N26 (black holes).** Its condition (i), the Axiom-7 reading, can be replaced by SE-E2 plus SE-E4. Nothing outside threatens a hole's persistence, whose lifetime is set by its own leak, so persistence is blind-viable. Scrambling correlations between (M, J, Q) and the surroundings does not change that lifetime: semantic information 0. The "past every tracker's lookup edge" half is about *other* trackers using a hole as memory, and they are selected, so the Axiom-7 reading applies to them anyway. **Condition (ii) needs narrowing (PHYSICS F5, accepted).** For a hole before its Page time, information comes back no sooner than about the Page time ≈ 0.54 t_ev. That includes every astrophysical hole today, since they are colder than the CMB, absorb more than they emit, and have not begun net evaporation, so for them the delay is effectively unbounded. After the Page time, newly deposited information comes back after about the scrambling time, but only to someone holding essentially all the earlier radiation and paying a decoding cost (Hayden & Preskill 2007, abstract via SCALE_ENDS; the exponential decoding cost is Harlow–Hayden's conjecture). All of this assumes unitary evaporation. For post-Page holes the lookup-edge conclusion therefore rests on the collection and decoding cost, not on delay alone. **Wording change proposed (BK-P7). Label PROVED (in-model) (classification, conditional) unchanged; its conditions are restated.**

### 2.1 Pre-cellular knowing: where between atoms and cells does it appear?

**Answer: there is no single switch. There are five separately measurable quantities. Their historical order is a HYPOTHESIS (H2-type) and only a partial order. CM-N28 concerns only selected models.**

| Quantity | First carriers (candidates) | What GTAO says | Status |
|---|---|---|---|
| Q0 Correlation | atoms (spin, speed, level populations correlate with temperature and fields; SE-E3(c)) | present, not needed for persistence (SE-E2) | DERIVED (§2.0.4) |
| Q1 Self-maintenance on a flow | dissipative chemistry; reflexively autocatalytic sets; the chemoton; autopoiesis | held structure; needs disequilibrium D > 0 | PRIOR ART (Prigogine 1978; Kauffman 1986; Hordijk, Hein & Steel 2010, metadata only; Gánti's chemoton and Maturana & Varela's autopoiesis, classics, not fetched) |
| Q2 Survival-relevant information | a self-maintaining system whose viability drops when its match to a drifting feed is scrambled | Theorem P (mapping lemma, §2.0.3) gives the floor on how much is required. BK-SEM decides whether it is used | **Synthesis, not new in substance:** Still et al. 2012; Kolchinsky & Wolpert 2018; Di Paolo 2005 ("adaptivity … allows organisms to regulate themselves with respect to their conditions of viability", abstract); England 2015 / Perunov, Marsland & England 2016 (dissipative adaptation; litmap). **New here is only the mapping onto Theorem P [BK, new, unreviewed]** |
| Q3 Minimal model (integral feedback) | any chemistry with robust perfect adaptation | IMP-structural model. Possible without heredity in principle; no prebiotic case known | OPEN (BK-IMP) |
| Q4 Heredity with cumulative selection | template replicators below Eigen's threshold (εL ≲ ln σ). Compartmentalized networks with multiple viable cores show "limited heredity and selectability" before templates (Vasas et al. 2012, abstract); simple compositional genomes lack evolvability (Vasas et al. 2010) | selected models become possible (Axiom 7). *Strong* cumulative design points to templates; weak pre-template selection is possible. Pross's dynamic kinetic stability applies here, to replicators | PRIOR ART (Eigen 1971; Vasas 2010, 2012; Pross 2011; England 2013's heat bound on replication); CM-N28 OPEN |
| Q5 Acting ahead (realized lead k > 0) | entrained oscillators with phase lead (no heredity needed); circadian clocks (Woelfle et al. 2004); microbial anticipation (Mitchell et al. 2009; Tagkopoulos et al. 2008; litmap) | acting ahead is *viable* only within the predictability horizon (GT-P2: k ≤ k_max, a ceiling set by the world and the budget). It *pays* only where lateness costs exceed upkeep (GT-P3, with actions) | PROOF (GT-P2, GT-P3); PRIOR ART for the data; H2 stays HYPOTHESIS |

**What changes relative to the record.**
- **CM-N28 needs a wording change; its status stays OPEN.** Its text says "a model switches on only with heredity …". Under this file's definitions that is true of *selected* models (Q4) and false for Q2–Q3 as a matter of definition. Revision 1's claim that "N28 stands as written" is withdrawn (MATH_LOGIC finding 6, accepted). The same sentence in THEORY §2.3 (the "ends of the scale" bullet) needs the same change, or THEORY would contradict itself (BK-P5).
- **SCALE_ENDS §3.3** put all pre-hereditary chemistry in "held, no model". Under §2.0 that stays right for "model". The structures can still carry survival-relevant information, which SCALE_ENDS did not separate.

**Testable consequence (HYPOTHESIS BK-G2, redesigned per PHYSICS F11 and BIO finding 9).** *This is a test of the mapping in a designed system, not evidence about natural prebiotic chemistry.*
- **System:** compartmentalized light-sensitive Belousov–Zhabotinsky droplets (Ru(bpy)₃-catalysed; light-pulse phase control and frequency locking are routine per Petrov, Ouyang & Swinney 1997, per PHYSICS F11; this author checked metadata only). Each droplet consumes a reagent that arrives in pulses and is usable only within a phase window, so mistiming depletes it.
- **Viability (ruin) defined:** time until oscillation amplitude falls below a preregistered threshold after the feed switches to pulsed and depleting.
- **Arms:**
  - (T) phase-resetting light pulses that keep the oscillator's phase matched to the reagent pulses;
  - (S) **sham pulses**: identical dose and count, randomly timed;
  - (C) **rhythmless matched-mean control**: an aperiodic feed with the same mean reagent supply, where no phase information can help.
- **Prediction:** viability T > S, and S ≈ C.
- **Kill:** T ≤ S within the preregistered minimum detectable effect, or T > S by the same margin under C-type aperiodic feed.
- **Caveat (accepted from PHYSICS F11a):** the phase dependence is engineered, so a pass shows only that the mapping (§2.0.3) and the scrambling test (BK-SEM) work as instruments. It is not evidence that nature built such systems. Status: HYPOTHESIS, design OPEN until the minimum detectable effect and power are computed (MV10).

### 2.2 Is feedback the simplest model? (revised)

**Decision [BK, new, unreviewed; resting on PRIOR ART].**
1. **Integral feedback on an exogenous variable is the minimal model** (Francis & Wonham 1976; Yi et al. 2000). It holds the integrated error, a model of a constant/step world, and returns the regulated variable to its set point.
2. **Proportional (or leaky) feedback is not a model** in this sense. It carries correlation, and possibly survival-relevant information, but it leaves a steady error that shifts with the drive.
3. **Feedback on own state only is not a model of any world.** This is a definitional choice (§2.0.2). A star's core balance is a proportional restoring effect: if the core heats, it expands, cools and burns slower.
4. **Revision 1's "lowest rung of a model = zero-order hold, exactly class R1" is withdrawn** (MATH_LOGIC finding 11; BIO finding 4). Axiom 3's R1 is discrete, costly, exact periodic reads. Continuous noisy feedback is at most analogous to R1 in the limit of frequent reads, and its cost class must be assigned separately.
5. **The repo inconsistency stands.** SCALE_ENDS §2 labels its no-model class "(H80's thermostat tier)", and §4.1 calls the star's balance "H80's feedback tier". But H80's thermostat rung is a *predictor* of an outside target. BK-P1 (approved by MATH_LOGIC) deletes the label.
6. **Two orders, not one ladder.** H80 orders rungs by **cost**: constant predictor, timer, threshold/thermostat, small model, large model. The K axis (§2.7) orders by **structure and lead**: correlation, then survival-relevant information, then integral model, then dynamic model with lead. A timer is cheap (low in H80) but acts ahead (high on K). Revision 1 merged the two orders, which contradicted its own sequence (MATH_LOGIC finding 10; BIO finding 7).
7. **"Frozen" has three senses, now named:**
   - **frozen structure** (persistence mode, h = 0);
   - **frozen store** (a T8 memory tier: a stored fact with I > 0 that decays at H_l);
   - **constant predictor** (H80's bottom rung: a fixed prediction with I_pred = 0, the "blind" agent of GT-P1).

**Where hurricanes, flames, dunes and galaxies land** (expected results, not measured; CLASSIFICATION pending tests):
- **Correlation:** all have it (Still et al. 2012).
- **Survival-relevant information (BK-SEM):** OPEN for each. For drive-slaved structures whose relaxation is much faster than the drive changes, the expected result is no drop, because the scrambled state relaxes back within one relaxation time.
- **Model (BK-IMP):** expected **no** for all four. A flame's size shifts with oxygen supply, a dune migrates with the wind, and a hurricane's intensity tracks sea-surface temperature. A galaxy's gas reservoir in the gas-regulator ("bathtub") model is a **leaky** integrator: star formation "is instantaneously regulated by the mass of gas in a reservoir", and the sSFR "is set to the specific accretion rate" (Lilly et al. 2013, abstract). That is tracking with a shifting state, not perfect adaptation.
- **Kill for this expectation:** any of them shows robust perfect adaptation of a regulated variable after a sustained step in its drive.

### 2.3 Why frozen memory exists in the grand scheme

GTAO gives roles inside its budget and the physical conditions behind them. It gives no purposes. **Three roles (DERIVED; revision 1's roles 1 and 4 merged per BIO finding 10):**
1. **Scaffold and freeze edge.** Knowers are built from frozen structures (nuclei, atoms, covalent frameworks, minerals) whose lifetime is set by a barrier, a conservation law or a horizon (SE-E4). Within a knower's own memory, anything drifting slower than q_f = 2c/(W H_l²) should sit in a frozen store (Theorem 8; CM-F13 PROVED (in-model)). H9's "paid systems are built out of frozen parts earlier flows left behind" is the plain form. H8's note that frozen things formed in earlier non-equilibrium flows is consistent with this and was not checked here.
2. **Heredity in a near-frozen store.** A genome is **near-frozen, not frozen**. It is held at low upkeep (continuous repair within a lifetime), copied rather than tracked, and updated only across generations, with its length capped by copying fidelity (Eigen 1971). Crick's "frozen accident" (classic, not fetched) is the classic credit for heredity as freezing. In T8 terms it is the store for features drifting slower than a generation. The lower edge of the hold band is where "write it in the genome" gives way to "sense it" (CM-N28's S3; Kussell & Leibler 2005).
   - **HYPOTHESIS (O5/BH-1 on cellular tiers; CM-F13's field form is OPEN):** across DNA, chromatin marks, mRNA and protein modification, the denser and costlier-to-read the tier, the slower the drift of its content.
   - **Validity condition (BIO finding 9, accepted):** "drift of what each tier holds" must be measured *independently of the tier's own turnover*, for example as the rate at which the corresponding environmental variable changes, fixed in the prereg. Otherwise the test passes by construction.
3. **Records.** Frozen stores serve as memory for *later* knowers: zircons, fossils, ice cores, archives, append-only histories. Reading one is a T8 "freeze read" (SCALE_ENDS §3.1).

**Black holes as the frozen extreme (CM-N26 PROVED (in-model), conditional; conditions restated in §2.0.4).** A black hole has maximal memory for its size at the Bekenstein-minimum energy per nat, no upkeep, readable state (M, J, Q), and a leak lifetime of about 1.2×10⁶⁷ yr × (M/M☉)³ (photons and gravitons only). Three massless neutrino species would give about 1.5×10⁶⁶ yr (PHYSICS F17), but massive neutrinos are not emitted at T_H ≪ m_νc²/k. The clock starts only once the CMB is colder than T_H.

**The entropy picture, corrected (PHYSICS F7).** Egan & Lineweaver 2010 (abstract opened) find:
- S_obs = 3.1 (+3.0/−1.7)×10¹⁰⁴ k for the observable universe, with supermassive black holes "the largest contributor";
- the current cosmic event horizon's S_CEH = 2.6 ± 0.3×10¹²² k, "dwarfing the entropy of its interior, S_CEH,int = 1.2 (+1.1/−0.7)×10¹⁰³ k".

The like-for-like gap is therefore S_CEH,int ≈ 10¹⁰³ against S_CEH ≈ 10¹²². SCALE_ENDS's S_obs vs S_dS comparison mixes two volumes. "Most of the entropy now present in the observable universe is in SMBHs" is what Egan & Lineweaver estimate. Revision 1's "most of the running-down so far is stored in black holes" conflated entropy content with production history and is withdrawn. Their sentence that the uncapped increase "is the reason dissipative processes are ongoing and that life can exist" refers to the gap below the holographic bound (as PHYSICS F7 reports from their introduction; this author read only the abstract). **Caveat:** an entropy gap is not usable free energy by itself. Structures draw on local gradients (fusion, gravitational contraction, chemical disequilibrium), and the low-entropy start is what makes those gradients possible. **IMPOSTER:** "black holes exist *in order to* store entropy." GTAO has no teleology. The only published selection-based role for black holes is Smolin's cosmological natural selection (PRIOR ART, under observational pressure; SE12: GTAO adds no test).

### 2.4 Stars

**Classification: held, self-regulated, no model (CLASSIFICATION; SE9).** The reason is restated per PHYSICS F9: **no response of the star has a payoff that depends on getting an exogenous variable right.** External bodies can change its fate. More than 70% of massive stars will exchange mass with a companion (Sana et al. 2012, page summary), and binary interaction may affect the evolution of most massive stars. But the star cannot act on them, its core regulation is a proportional restoring effect with no integrator on any outside variable, and the scrambling test is expected to show no survival-relevant information. Convection, dynamos and pulsation are driven by internal gradients and do not change the class.
- **Withdrawn from revision 1:** "its ruin is fixed by its own mass and composition", which holds only for isolated stars.
- **Withdrawn:** "upkeep h = L". L is the star's **free-energy throughput**, not a maintenance cost. A star that stops fusing contracts and heats, and white dwarfs persist with no flux.
- **Stellar generations** pass on composition, a frozen record, with no selection over designs.
- **Kill (SE9):** a star whose persistence depends on tracking an external drift through a response it can vary. Stars remain an MV7 calibration case for "held but not modelling". **Galaxies are removed from that known group** (PHYSICS F3): their classification is K1 by the expected BK-IMP result, but OPEN.

### 2.5 Planets and Gaia

**First name the persisting entity and its ruin variable (PHYSICS F2, accepted). Then classify.**

| Entity | Ruin variable | Classification | Basis |
|---|---|---|---|
| The rocky body | disruption (practically none) | frozen structures plus held, self-regulated convection; blind-viable (Venus persists) | CLASSIFICATION |
| **Abiotic climate regulation** (carbonate–silicate weathering) | habitability, which is a variable that matters only to life | feedback in which a CO₂ reservoir integrates outgassing minus temperature-dependent weathering (Walker, Hays & Kasting 1981, metadata only: "a negative feedback mechanism for the long-term stabilization of Earth's surface temperature"). It is structurally **integrator-like**, so it is a **candidate structural model without any selection** | OPEN (BK-IMP: degree of perfect adaptation of surface temperature to solar brightening); [BK, new, unreviewed] |
| **The biosphere** | extinction of life | a population of knowers. Its regulation (Gaia) is carried by organisms under organism-level selection. In Daisyworld the coupling comes from competing daisy types (Watson & Lovelock 1983, litmap). Doolittle 2014 argues the same for real Gaian traits | selected models *within* it (class 3); planet-scale regulation is a by-product, **unselected at planet scale** |
| **Planet-scale persistence filtering** | — | Lenton et al. 2018 (abstract): "sequential selection", where destabilizing systems "are short-lived and result in extinctions and reorganizations until a stable attractor is found", plus "selection by survival alone". That phrase is Doolittle 2014's (page read): "differential survival of non-competing and non-reproducing individuals will also result in increasing frequencies of survival-promoting 'adaptations' among survivors". He predicts *accumulation* of persistence-promoting traits even at n = 1, mostly fixed by lower-level selection (his note 3). Bouchard 2008 and 2011 and Bourrat 2014 are part of this debate (named via Doolittle and BIO; not opened) | PRIOR ART. **HYPOTHESIS (revision 1 asserted it):** a persistence filter at n = 1 has a large design resolution ε, so GTAO's *optimality* predictions do not apply at planet scale. Doolittle's accumulation claim is compatible with that, since accumulation is not optimality, but the ε is unquantified (OPEN) |
| **Atmosphere, oceans, soils** | — | a **shared slow store and drift reducer**: life reshapes its world so it changes less (THEORY §5; Lee, Flack & Krakauer 2024, "Constructing stability: optimal learning in noisy ecological niches", whose preprint calls niche construction "outsourced memory"; Lenton et al. 2018) | PRIOR ART; also a commons (§3) |
| **The technosphere** | — | since humans, Earth forecasts ahead (climate models, asteroid tracking): **K3 components at planet scale**. Frank, Grinspoon & Walker 2022 (abstract) treat "intelligence as a planetary scale process" and technological intelligence as a transition that happens "to a planet" | PRIOR ART framing; CLASSIFICATION |

**Rival framing (credited).** Rubin, Parr, Da Costa & Friston 2020 (abstract) formalize Gaia with a Markov blanket. The biosphere's metabolic rates are the internal states, solar radiation the external states, greenhouse and albedo changes the active states, and ocean-driven temperature the sensory states. This is the free-energy principle's specific planetary claim and a **rival** to this file's more restrictive criteria (§2.0.2). The disagreement is testable only once both sides fix an intervention (BK-SEM, BK-IMP) in advance.

**Earlier chat claim corrected again.** Revision 1 said Daisyworld's regulation is "a model of the lowest, reactive kind … unselected". Under §2.0 it carries correlation and, at the daisy level, selected responses. Whether its feedback is integral (a model) depends on the model's equations, and it is **selected at the daisy level, unselected at planet scale**.

**Why would life outlast humans? (ANALOGY plus PRIOR ART; not PROVED.)** Revision 1 used THEORY §4's pooling rule z′ = z√(N/(1+(N−1)ρ)) and called it "DERIVED from PROVED (in-model) rules". Both labels were wrong. MATH_ATTACK labels §3.2 "PROOF + NUMERIC", and the rule needs a pooled, fungible buffer (its condition C2), which lineages do not share (MATH_LOGIC finding 7; PHYSICS F12). What stands:
- **The direction:** many weakly correlated lineages make a whole that fails only under shocks correlated across nearly all of them. This is the insurance hypothesis (Yachi & Loreau 1999, abstract: "many species provide greater guarantees that some will maintain functioning even if others fail"). It is a redundancy (parallel-survival) argument, which the repo does not derive (OPEN).
- **The evidence** is empirical: the biosphere has re-established after mass extinctions. That is standard paleontology and is not cited here. Recovery takes millions of years, so "fast" means fast relative to geological forcing, not to human time.
- **The long-run end** is a ρ ≈ 1 exogenous drift (solar brightening; Caldeira & Kasting 1992 per PHYSICS F12, metadata only), consistent in direction with the argument.

**"Is a planet conscious?"** GTAO's quantities (correlation, survival-relevant information, model structure, lead k, selection resolution ε) are **not measures of consciousness**, and GTAO has no variable for experience. So the question is **out of scope**, and any claim that *GTAO shows* a planet is, or is not, conscious is an **IMPOSTER**.

### 2.6 Implications at every level: see §4 (table).

### 2.7 One coherent picture in technical terms: three axes

**[BK, new, unreviewed synthesis.]**
- **Axis P (persistence):**
  - *frozen structure*: h = 0; lifetime set by a barrier, a conservation law or a horizon;
  - *held*: free-energy throughput; needs D > 0.
- **Axis K (knowing; §2.0.2):**
  - K0: correlation only;
  - K1: response without model (self-regulation, proportional or leaky feedback, drive-slaved), possibly with survival-relevant information (written K1s when BK-SEM is positive);
  - K2: minimal structural model (integral feedback; perfect adaptation);
  - K3: dynamic model with realized lead k > 0 (oscillator or clock, predictive model).
- **Axis S (selection):** none; persistence filter (survival of the stable; Doolittle's selection through survival; Lenton's sequential selection); weak pre-template selection (Vasas 2012); cumulative selection with heredity, learning or design, with resolution ε (Axiom 7).

**How they depend on each other.**
- **K2 and K3 require P = held.** An integrator or clock holds memory beyond the instantaneous correlation, and holding memory about a drifting variable costs dissipation (SCALE_ENDS SE-E3, l.62). K0 and K1 do not require upkeep: passive coupling can approach zero cost (SE-E3(c)). Revision 1's "K ≥ K2 requires held" is replaced with this (MATH_LOGIC finding 5, accepted).
- **The three-cost accounting** applies everywhere (Axiom 5; CM-J16 OPEN).
- **Theorem P** (with §2.0.3) gives the information floor wherever responses exist and blind is not viable.
- **Design predictions** need actions: S cumulative with the prize above ε.
- **Thermodynamic floors:**
  - Erasure costs at least kT ln 2 per bit (Landauer). A measure-and-reset cycle costs at least kT × the mutual information acquired (Sagawa & Ueda 2009), and measurement alone can in principle be reversible.
  - Still et al.'s bound assumes a single heat bath, Markov dynamics, an equilibrium start and no back-action on the drive (PHYSICS F8, from their setup). Stars, storms and planets violate these, so the bound is used for them only as an **analogy**. The same scope note applies to SCALE_ENDS SE-E3(c)'s "driven systems" clause (BK-P11).

| Structure | P | K (expected; tests in §2.0.2) | S | Design predictions? |
|---|---|---|---|---|
| Atom, nucleus, crystal | frozen | K0 | none | no (CM-N25) |
| Black hole | frozen (extreme) | K0 | none (Smolin's hypothesis aside) | no (CM-N26) |
| Star | held | K1 | none | no (SE9) |
| Galaxy (gas regulator) | held | K1 (leaky integrator), OPEN | none | no |
| Flame, dune, hurricane | held; hurricanes and flames transient | K1; K1s OPEN | none | no; hurricanes are outside GT-P's long-run statement |
| Driven chemistry, autocatalytic networks | held | K1 or K1s (BK-SEM); K2 OPEN | filter to weak cumulative (OPEN) | no |
| Template replicator, protocell | held | K1s–K2 | cumulative if below Eigen's threshold | in principle (CM-N28 OPEN) |
| Cell | held | K2–K3 | cumulative, strong | yes (CM-N24 INCONCLUSIVE; CM-N13 OPEN) |
| Brain, person | held | K3 | learning plus evolution | yes, moderate ε |
| Colony, firm, city | held | K2–K3 with levels | moderate to weak | yes, gated by ε |
| Earth system | mixed (§2.5) | abiotic thermostat: K2 candidate; biosphere: K2–K3; technosphere: K3 | filter at planet scale; cumulative within | not at planet scale |
| Universe | — | not a tracker | — | IMPOSTER to say otherwise |

In one line: **knowing is held structure that frozen structure lets accumulate and burning structure pays for, and judgment is the part of knowing that acts ahead.**

---

## 3. Layers and governance, from the same spine

Each step keeps its source label and states where it fails.

1. **Persistence needs a throughput. Where lateness is costly, a model can pay** (GT §1, GT-P3 with actions). Models cost upkeep, reads and error (Axiom 5; one currency within an organization, A4).
2. **Shared drivers favour shared models.** TH-T3a (**PROOF; elementary; a sufficient condition, not a cutoff**): nesting is cheaper whenever √N·√(2cwq_u)·[√N(√(1+ρ) − 1) − √ρ] > h. At h = 0 this is N > (√(1+ρ)+1)²/ρ. In the formal layer the level's sensing class sets the onset exponent (CM-B3, CM-B9 PROVED (in-model)), and shared drift centralizes while private drift decentralizes (CM-C1 PROVED (in-model)). A level is a shared model of a common driver (THEORY §6). Flack 2012 and 2017 on slow, coarse-grained collective variables are the prior art for levels as shared slow variables (litmap). **Fails:** with no shared drift (nesting loses by its upkeep); below N\* (the bound says nothing there); when the driver is seen only through the facts (then it is an approximation).
3. **Separate clocks buy little and need separated time scales.** TH-T3b (**KNOWN**; Roundy 1985): at most 29% saving for two levels. TH-T3c (**NUMERIC; principle KNOWN**: Simon–Ando, Tikhonov, Borkar): decoupled nesting is near-optimal only when time scales separate. **Fails:** collapsed or inverted time scales.
4. **Self-similar only where the world is.** TH-T7 (**PROOF (conditional); the unconditional claim FAILS**). Testable forms (i)–(iii). **Flag:** T7(iii)'s "number of levels grows as L^{2/3}" (L = log-span) predates THEORY v1.4. The (log-span)^{2/3} count is withdrawn (CM-K12 MATH-CORRECTED). The store count is now ∝ ln(span)·ln(stakes/upkeep) away from α = 2, with its rate marked conjectural in THEORY N4. BK-P8 (approved by MATH_LOGIC) adds the pointer. **Fails:** characteristic times, fixed setup costs, or different loss forms across levels.
5. **A whole is a knower like its parts only under strict conditions.** MATH_ATTACK §3.4 (**PROOF + NUMERIC**): a representative agent exists only under a Gorman-type condition, c_i/(w_iσ_i²) equal across parts. MATH_ATTACK §3.6: form invariance holds iff C1–C4 hold, and **the strong form is FALSE**. So "the same pattern at every level" is about relations measured level by level (CM-J6 OPEN). **Fails:** heterogeneous costs, non-fungible buffers, heterogeneous fix times, correlated shocks.
6. **Parts under-watch when the whole's failure cost does not reach them.** MATH_ATTACK §3.4 (**PROOF**): watching is too low by √(Λ_i/Λ_whole) when each part counts only its own Λ_i. This is the standard externality result in this cost form (public-goods prior art; Ostrom 2010, litmap; Ostrom 1990, classic, credited in THEORY §6). The source states it for a part's own failure hazard. **Reading it as "parts under-watch shared memory" is an extension [BK, new, unreviewed].** Lee, Flack & Krakauer 2024: stabilization is a public good, and when resources are shared "niche destructors" can evolve (as BIO reports from the published abstract).
7. **The remedy is shared fate or enforcement (HYPOTHESIS; J9 OPEN; not a consequence).** MATH_ATTACK §3.4 names the routes: the failure cost is internalized "by incentives, **shared fate** or a central controller". Shared fate needs no one in charge. Sterile workers in social insects share the colony's fate through relatedness, so Λ_i ≈ Λ_whole. Enforcement is the other route: Frank 1995 (abstract) shows mutual policing and "repression of competition" are needed to explain how "small, individual replicators formed cooperative groups", and the same problem recurs in insect and human societies. Worker policing is Ratnieks 1988 (metadata only). The qualitative claim is **PRIOR ART** (Ostrom; Frank 1995). GTAO's own part is the √(Λ_i/Λ_whole) scaling and the predicted placement. CM-J8 ("no one in charge, at every level") stays **WITHDRAWN**. CM-J7 (fractal vigilance, qualitative) is **PRIOR ART**, and its quantitative version is untested on a valid instrument. Revision 1's identification of CM-E6 with fractal vigilance is withdrawn (MATH_LOGIC finding 12). **Flag:** THEORY §6's example "as with ants on a trail they themselves follow" for "privately rewarded" is **shaky**. Workers are mostly sterile, so their "private reward" is colony-level fitness (shared fate), and ants also police each other. BK-P10 proposes rewording it. **Fails:** if enforcement is as common where shared memory is privately rewarded or fate is shared, or if staleness does not rise with users per maintainer.
8. **Signal delay forces federation; light delay is the floor.** LAT-1 (**CM-N27 OPEN**; the bound is elementary): with hold-last-value reads, a tracker of extent L holds a target only if q·ℓ^{α−1} is below tolerance, where ℓ ≥ L/c. On Earth, ℓ is set by processing, conduction and decision time. Light crossing half of Earth's circumference takes about 0.07 s (PHYSICS F15), so **c binds only off-planet**. **Fails:** if at fixed q the central share does not depend on ℓ. **Weighting:** spacecraft autonomy is engineered against light delay, so a pass there is weak (confirmation by design), and geo-distributed firms carry more weight.

**How this follows from the spine.** The second law forces upkeep. Upkeep makes duplicate models wasteful, so shared drivers get shared models. Shared models are commons, so they need shared fate or enforcement. Signal delay caps how far one model reaches, so wholes federate. Every step is an economy of knowing under a physically forced budget. None adds a new physical principle. **Downward:** the first "level" was likely a compartment shared by cooperating replicators, which is exactly Frank 1995's opening case (PRIOR ART).

---

## 4. Implications if GTAO is right, level by level

"If right" means: strongly selected systems sit near the optima once α, q, N and stakes are measured on the same system, with the same relations at every level (CM-N13, CM-J6, OPEN). **Rows marked CLASSIFICATION are not predictions.**

| Level | Placement (§2.7) | What follows if right | Testable consequence (status; weaknesses) |
|---|---|---|---|
| **Chemistry** | held; K1→K1s/K2; filter→weak cumulative | Survival-relevant information can precede heredity. Design optimization starts with heredity | **BK-G2** (designed-system test of the mapping; HYPOTHESIS, design OPEN). **BK-IMP in chemistry:** robust perfect adaptation in a non-hereditary network (OPEN). Whether the Landauer floor binds before the cell is **OPEN**; the bacterial margin (CM-N28) says nothing about prebiotic systems (PHYSICS F8c) |
| **Cell** | K2–K3; strong selection | Read rate, memory time and store count near the §2.2 optima. The floor shapes exponents, not existence | **SENSE-CELL-MATCHED** (CM-J11 OPEN; CM-N24 INCONCLUSIVE). **O5/BH-1 on cellular tiers**, with drift measured independently of tier turnover (HYPOTHESIS) |
| **Organism, brain** | K3; learning | Energy per stimulus tracks predictable information. Higher levels track slower causes | **H4** (HYPOTHESIS; must be positioned against the existing repetition-suppression vs expectation literature, which BIO names and this author did not open). **H80 tier test** on a named system: the Intel Berkeley Research Lab sensor traces named in C13 (HYPOTHESIS) |
| **Colony, society** | levels; moderate selection | Levels where shared drift is large for its N. Shared fate or enforcement where memory is a public good | **TH-T3a/CM-C1 factorial** (FRAMEWORK §6.4; OPEN). For ants specifically: THEORY's own species-by-patchiness test (THEORY N2; OPEN). Policing intensity rises as relatedness falls is PRIOR ART (Ratnieks; Frank), not a GTAO test |
| **Firm** | levels; weak–moderate selection | Watching rises with stakes. Drift reduction substitutes for watching. Under-watching scales as √(Λ_i/Λ_whole) | **SAME-SYSTEM-AQN** (first CM-N13 test; OPEN). The contract-length vs volatility prediction (THEORY §5) needs a transaction-cost literature check before it counts as GTAO's (OPEN) |
| **City** | levels; weak selection | Monitoring sublinear and tiered | **CM-I14** (OPEN). z ∝ N^{b−H−θ/2} (MATH_ATTACK §3.5, CONJECTURE) |
| **Civilization** | levels at planetary extent | Federation forced by latency (light only off-planet) | **LAT-1** (CM-N27 OPEN), weighted toward geo-distributed firms |
| **Planet** | mixed (§2.5) | Earth regulates through its biosphere and an abiotic integrator-like cycle. Life reduces the drift it tracks. The technosphere adds forecasting | **Microcosm substitution (HYPOTHESIS, redesigned per BIO finding 9):** externally manipulate drift (buffered vs fluctuating medium) across replicate evolving lines, and predict lower investment in sensing and regulation in buffered lines at matched stakes. A pass is weak, because loss of unused regulation under relaxed selection is known (Mitchell et al. 2009). **BK-IMP on the carbonate–silicate cycle** (OPEN). No test at planet scale for design predictions (n = 1) |
| **Star** | held; K1 | — | CLASSIFICATION. SE9 kill; MV7 calibration case |
| **Galaxy** | held; K1 (OPEN) | — | CLASSIFICATION, pending BK-IMP on gas-regulator models. Not a calibration case |
| **Black hole** | frozen extreme | Nobody's usable memory | CLASSIFICATION. BH-1 = O5 is tested only in ordinary storage hierarchies (HYPOTHESIS) |
| **Cosmos, heat death** | gap closing | Knowing can last no longer than the last usable gradient, which may be black-hole evaporation long after the stars. In an accelerating universe the total recoverable information is finite and "life cannot be eternal" (Krauss & Starkman 2000, via SCALE_ENDS). Dyson-style hibernation does not rescue indefinite computation, by Krauss & Starkman's argument | CLASSIFICATION; PRIOR ART relabelled (SE14). Revision 1's ordering "knowing ends first, burning next, keeping last" is withdrawn (PHYSICS F13) |

---

## 5. Prior art credited

- **Thermodynamics and information:** Prigogine 1978; Landauer 1961; Sagawa & Ueda 2009; Still, Sivak, Bell & Crooks 2012; England 2013 (replication heat bound, Q4); England 2015 and Perunov, Marsland & England 2016 (dissipative adaptation, Q2).
- **Semantic information and adaptivity:** Kolchinsky & Wolpert 2018; Di Paolo 2005; autopoiesis (Maturana & Varela; classic, not fetched).
- **Internal models:** Francis & Wonham 1976 (internal model principle); Yi, Huang, Simon & Doyle 2000 (integral feedback in chemotaxis); Conant & Ashby 1970 (good regulator; the "model" is only a homomorphism, per GENERAL_THEOREM §2's notes); Rosen 1985 (anticipatory systems; litmap).
- **Origins:** Eigen 1971; Kauffman 1986; Hordijk, Hein & Steel 2010 (metadata only); Gánti (chemoton; classic, not fetched); Vasas, Szathmáry & Santos 2010; Vasas, Fernando, Santos, Kauffman & Szathmáry 2012; Pross 2011 (dynamic kinetic stability, for replicators).
- **Acting ahead:** Woelfle et al. 2004; Mitchell et al. 2009; Tagkopoulos et al. 2008; Sterling 2012 (allostasis; litmap).
- **Gaia:** Lovelock & Margulis 1974; Watson & Lovelock 1983; Lenton et al. 2018; Doolittle 2014; Rubin, Parr, Da Costa & Friston 2020 (rival); Frank, Grinspoon & Walker 2022; Walker, Hays & Kasting 1981 (metadata only).
- **Niche construction:** Lee, Flack & Krakauer 2024. **Biodiversity insurance:** Yachi & Loreau 1999.
- **Levels and governance:** Simon 1962; Roundy 1985; Gorman 1953 (as in MATH_ATTACK); Flack 2012 and 2017; Ostrom 1990 and 2010; Frank 1995; Ratnieks 1988 (metadata only); Beer and Mintzberg (THEORY §6).
- **Astrophysics and cosmology:** Lilly et al. 2013; Sana et al. 2012; Egan & Lineweaver 2010; Hayden & Preskill 2007; Smolin 1992 and 2004; Krauss & Starkman 2000.
- **Rival:** the free-energy principle (Friston 2010, 2013; Friston et al. 2023; Rubin et al. 2020). The critique that it is "trivially true or ill-defined at scale" (Aguilera et al. 2022; Bruineberg et al. 2022; litmap THREATS) applies equally to any GTAO definition of "model" that every driven system satisfies. §2.0.2's tests exist to avoid that.
- **Litmap conflict, acknowledged (BIO finding 3).** litmap/LITMAP.md files dissipative adaptation (England 2015; Perunov et al. 2016) as CONTRADICTS: "a rival physical route needs no prediction". Under revision 1 those systems became "models", which dissolved the threat by redefinition. Under revision 2 they are K1 or K1s (correlation or survival-relevant information, no structural model). The threat stands: dissipative adaptation is a route to drive-matched persistence without a model. BK-P12 proposes a THREATS entry that says so.

---

## 6. Proposed changes to canonical wording: listed, NOT applied

Each needs an independent review before it is applied. MATH_LOGIC approved BK-P1 and BK-P8. **No CLAIM_MAP status label changes. The wording or conditions of CM-N25, CM-N26 and CM-N28 change (§2.0.4).**

- **BK-P1 (approved) — SCALE_ENDS §2 class table, class 2.** Replace "**Held structure, no model** (H80's thermostat tier) … 0 (feedback on its own state only)" with "**Held structure, self-regulated**: feedback on its own state only; no exogenous target". In §4.1, replace "H80's feedback tier" with "self-regulation (a proportional restoring effect); not H80's thermostat rung, which predicts an exogenous target".
- **BK-P2 — SCALE_ENDS §2: define the K distinctions without a new "model" class.** Add a note after the class table: "Held structures may carry (a) correlation, (b) survival-relevant information (Kolchinsky & Wolpert test), (c) a structural model (internal model principle; integral feedback minimal), or (d) a selected model (Axiom 7). Classes 2 and 3 are split by (c), and design predictions need (d). Candidates for (b) without (c): driven chemistry, storms. A candidate for (c) without (d): the carbonate–silicate cycle." This replaces revision 1's class "2b", which is withdrawn.
- **BK-P3 — SCALE_ENDS §2: class 3 condition.** Replace "and **selection over designs** (Axiom 7: heredity)" with "a structural model of an exogenous drifting target (internal model principle) and, for GTAO's design predictions, selection over designs (Axiom 7)".
- **BK-P4 — SCALE_ENDS §3.3 and SE4 (a pre-data revision, logged with its reason, per BIO finding 13).** Replace "These need only D > 0. They are class 2 in §2" with "They need D > 0. They are class 2 unless they hold a structural model. Whether they carry survival-relevant information is tested by BOOKENDS BK-SEM". Replace SE4's kill ("a persistent structure that holds a model without a flux, or without heredity") with **two** kills, at least as sharp as the old one:
  - (i) a structure holding survival-relevant information about a drifting variable with no flux;
  - (ii) a structure showing robust perfect adaptation to an exogenous step (BK-IMP) with no flux.

  *Reason:* SCALE_ENDS IR-FIX10 already found the heredity clause near-definitional.
- **BK-P5 — THEORY §2.3 ("ends of the scale" bullet) and CLAIM_MAP CM-N28 text.** Replace "Models switch on only with heredity, a world-dependent action, drift inside the hold band, and a first nat that pays" with "*Selected* models (design optimization) switch on only with heredity, a world-dependent action, drift inside the hold band, and a first nat that pays; survival-relevant information and minimal (integral-feedback) models are not excluded earlier (`theory/BOOKENDS.md` §2.1)". The CM-N28 status stays OPEN.
- **BK-P6 — CLAIM_MAP CM-N25 note (label unchanged).** Add: "Under a response (unselected) reading the conclusion follows from SE-E2 alone: blind persistence viable, so Theorem P allows I_pred = 0, and semantic information is 0 (BOOKENDS §2.0.4)."
- **BK-P7 — CLAIM_MAP CM-N26 and THEORY §2.3 conditions (label unchanged).** Replace condition (i) with "SE-E2 + SE-E4 (or the Axiom-7 reading)". Replace condition (ii) with "for pre-Page-time holes (all astrophysical holes today), retrieval delay ≥ ~t_Page; for post-Page-time holes, new information returns after ~the scrambling time only to a holder of the earlier radiation at a decoding cost (Hayden & Preskill 2007; Harlow–Hayden conjectural); unitary evaporation assumed". Make the matching edit to THEORY's sentence "Everything else returns only after about the Page time".
- **BK-P8 (approved) — `theory/THEOREMS.md` T7(iii).** Add: "the L^{2/3} level count (L = log-span) predates THEORY v1.4; see CLAIM_MAP K12 (MATH-CORRECTED) for the current store count".
- **BK-P9 — Spine sentence for THEORY §0 or BRIEF §1 (Chad's call).** "Everything obeys the second law; together with gravity, the speed of light and the universe's low-entropy start, it sets the stage. Atoms and crystals carry information but have no use for a model; stars hold themselves up on a flow but track nothing outside; cells, people, firms and cities last only by staying matched to a world that changes and can ruin them, and once acting late is costly, carrying a model and acting ahead can pay. That is judgment: not a new law, but a way of staying alive under the old one."
- **BK-P10 — THEORY §6 example.** Replace "(each contributor's own use pays for its deposits, as with ants on a trail they themselves follow)" with "(each contributor's own use pays for its deposits). Social insects mostly fit the other routes: sterile workers share the colony's fate, and workers also police (Frank 1995; Ratnieks 1988)". Also fix THEORY §6's "MATH_ATTACK §3.5" to §3.4 for the under-watching result.
- **BK-P11 — SCALE_ENDS SE-E3(c) and §0 item 1.** Replace "A read … costs at least kT ln 2 per bit erased" with "erasure costs at least kT ln 2 per bit; a measure-and-reset cycle at least kT × the information acquired (Sagawa & Ueda); measurement alone can be reversible". Add Still et al.'s scope (single bath, Markov, no back-action). Remove galaxies from SE9's known-negative group.
- **BK-P12 — litmap/THREATS.md: new entry.** "Dissipative adaptation (England 2015; Perunov et al. 2016) gives drive-matched persistence without a structural model. GTAO's criteria (BOOKENDS §2.0.2) classify such systems as K1/K1s, so the threat stands and is not removed by definition."
- **BK-P13 — CLAIM_MAP: new rows proposed** (IDs assigned at application; not N-numbered here):
  - BK-a, "four notions of knowing and the response/action split": DERIVED definitions, OPEN;
  - BK-SEM and BK-IMP: HYPOTHESIS tests, OPEN;
  - BK-G2: HYPOTHESIS, design OPEN;
  - BK-finite-horizon corollary: DERIVED, Markov form OPEN;
  - BK-c, "Earth = biosphere-carried regulation, selected within, filtered at planet scale; abiotic integrator candidate; technosphere K3": CLASSIFICATION on PRIOR ART;
  - BK-microcosm: HYPOTHESIS, OPEN.
- **BK-P14 — `tools/check_consistency.py`.** After review, add `theory/BOOKENDS.md` to MAINTAINED. Separately (a tooling nit reported by MATH_LOGIC), avoid `sys.exit` on import so pytest can collect it.

---

## 7. Open questions

1. **The mapping lemma (§2.0.3).** Is it sound, especially when the structure alters its feed (A1 fails)? It needs an independent mathematical referee, and the Markov-dependent form of the finite-horizon bound is still owed.
2. **Operational BK-SEM.** A scrambling intervention at fixed fluxes with a dose-matched sham, for storms, galaxies or planets. It is probably infeasible outside designed systems, so those placements stay CLASSIFICATION.
3. **A persistence filter as selection.** Doolittle 2014 argues qualitatively that it is selection, and that persistence-promoting traits accumulate even at n = 1. Nobody has given it an Axiom-7 resolution ε. The claim that its ε is large is a HYPOTHESIS here.
4. **Density versus readability.** Gravity guarantees only that the densest possible store (a black hole) is unreadable on useful time scales. Below that limit no physical principle links density to read cost. DNA is very dense and read routinely. O5/BH-1 is an empirical hypothesis about selected storage hierarchies.
5. **The t1908 disagreement** (is the physics decorative?) stays OPEN. SENSE-CELL-MATCHED is the test.
6. **Theorem P's stochastic internal-model conjecture** (GENERAL_THEOREM §2). If proved, it would tie Theorem P's *amount* of information to the IMP's *structure*, closing the gap between §2.0.2's rows.
7. **A redundancy-aggregation result** that gives "fragile only to correlated shocks" without fungible buffers (for the biosphere argument).
8. **Consciousness:** out of scope.
9. **Field status:** every real-system row in §4 is untested. GTAO stays **untested, not refuted**.

---

## References

Marks: (abstract), (page) or (metadata only) = opened by this author this session; (litmap) or (via SCALE_ENDS) = DOI already in the repo.

- Caldeira K, Kasting JF 1992, "The life span of the biosphere revisited," *Nature* 360:721–723, doi 10.1038/360721a0 (metadata only; named per PHYSICS F12)
- Di Paolo EA 2005, *Phenom Cogn Sci* 4:429, doi 10.1007/s11097-005-9002-y (abstract)
- Doolittle WF 2014 (online 2013), "Natural selection through survival alone, and the possibility of Gaia," *Biol Philos* 29:415–423, doi 10.1007/s10539-013-9384-0 (page: abstract and notes)
- Egan CA, Lineweaver CH 2010, *ApJ* 710:1825, doi 10.1088/0004-637X/710/2/1825 (abstract, arXiv 0909.3983)
- Eigen M 1971, *Naturwissenschaften* 58:465, doi 10.1007/BF00623322 (via SCALE_ENDS)
- England JL 2013, *J Chem Phys* 139:121923, doi 10.1063/1.4818538 (abstract); England 2015, *Nat Nanotechnol* 10:919, doi 10.1038/nnano.2015.250 (litmap); Perunov N, Marsland R, England JL 2016, *PRX* 6:021036, doi 10.1103/PhysRevX.6.021036 (litmap)
- Francis BA, Wonham WM 1976, "The internal model principle of control theory," *Automatica* 12:457, doi 10.1016/0005-1098(76)90006-6 (litmap; title verified)
- Frank AA, Grinspoon D, Walker SI 2022, "Intelligence as a planetary scale process," *Int J Astrobiol* 21:47, doi 10.1017/S147355042100029X (abstract)
- Frank SA 1995, "Mutual policing and repression of competition in the evolution of cooperative groups," *Nature* 377:520, doi 10.1038/377520a0 (abstract)
- Friston K 2010, doi 10.1038/nrn2787; 2013, doi 10.1098/rsif.2013.0475 (litmap); Friston K et al. 2023, doi 10.1016/j.plrev.2023.08.016 (via SCALE_ENDS)
- Hayden P, Preskill J 2007, *JHEP* 09:120, doi 10.1088/1126-6708/2007/09/120 (via SCALE_ENDS)
- Hordijk W, Hein J, Steel M 2010, "Autocatalytic sets and the origin of life," *Entropy* 12:1733–1742, doi 10.3390/e12071733 (metadata only)
- Kauffman SA 1986, doi 10.1016/S0022-5193(86)80047-9 (via SCALE_ENDS)
- Kolchinsky A, Wolpert DH 2018, *Interface Focus* 8:20180041, doi 10.1098/rsfs.2018.0041 (abstract)
- Krauss LM, Starkman GD 2000, *ApJ* 531:22, doi 10.1086/308434 (via SCALE_ENDS)
- Kussell E, Leibler S 2005, doi 10.1126/science.1114383 (via SCALE_ENDS)
- Lee, Flack & Krakauer 2024, "Constructing stability: optimal learning in noisy ecological niches," *Proc R Soc B* 291:20241606, doi 10.1098/rspb.2024.1606 (litmap)
- Lenton T, Daines S, Dyke J, Nicholson A, Wilkinson D, Williams HTP 2018, *Trends Ecol Evol* 33:633–645, doi 10.1016/j.tree.2018.05.006 (abstract)
- Lilly SJ, Carollo CM, Pipino A, Renzini A, Peng Y 2013, "Gas regulation of galaxies," *ApJ* 772:119, doi 10.1088/0004-637X/772/2/119 (abstract; authors per Crossref)
- Lovelock JE, Margulis L 1974, doi 10.3402/tellusa.v26i1-2.9731; Watson AJ, Lovelock JE 1983, doi 10.3402/tellusb.v35i4.14616 (litmap; abstract not available)
- Mitchell A et al. 2009, *Nature* 460:220, doi 10.1038/nature08112; Tagkopoulos I, Liu Y-C, Tavazoie S 2008, *Science* 320:1313, doi 10.1126/science.1154456 (litmap)
- Ostrom E 2010, *AER* 100:641, doi 10.1257/aer.100.3.641 (litmap); Ostrom 1990 (classic; THEORY §6)
- Flack JC 2012, doi 10.1098/rstb.2011.0214; Flack 2017, doi 10.1098/rsta.2016.0338 (litmap)
- Prigogine I 1978, doi 10.1126/science.201.4358.777 (via SCALE_ENDS)
- Pross A 2011, *J Syst Chem* 2:1, doi 10.1186/1759-2208-2-1 (abstract)
- Ratnieks FLW 1988, "Reproductive harmony via mutual policing by workers in eusocial Hymenoptera," *Am Nat* 132:217–236, doi 10.1086/284846 (metadata only)
- Rosen R 1985, *Anticipatory Systems* (litmap; book not fetched)
- Rubin S, Parr T, Da Costa L, Friston K 2020, "Future climates: Markov blankets and active inference in the biosphere," *J R Soc Interface* 17:20200503, doi 10.1098/rsif.2020.0503 (abstract)
- Sagawa T, Ueda M 2009, *PRL* 102:250602, doi 10.1103/PhysRevLett.102.250602 (via SCALE_ENDS)
- Sana H et al. 2012, "Binary interaction dominates the evolution of massive stars," *Science* 337:444, doi 10.1126/science.1223344 (page summary)
- Smolin L 1992, doi 10.1088/0264-9381/9/1/016; 2004, arXiv hep-th/0407213 (via SCALE_ENDS)
- Sterling P 2012, *Physiol Behav* 106:5, doi 10.1016/j.physbeh.2011.06.004 (litmap)
- Still S, Sivak DA, Bell AJ, Crooks GE 2012, *PRL* 109:120604, doi 10.1103/PhysRevLett.109.120604 (litmap; wording and setup as quoted by PHYSICS F1/F8)
- Vasas V, Szathmáry E, Santos M 2010, *PNAS* 107:1470, doi 10.1073/pnas.0912628107 (abstract)
- Vasas V, Fernando C, Santos M, Kauffman S, Szathmáry E 2012, "Evolution before genes," *Biol Direct* 7:1, doi 10.1186/1745-6150-7-1 (abstract)
- Walker JCG, Hays PB, Kasting JF 1981, *J Geophys Res* 86:9776, doi 10.1029/JC086iC10p09776 (metadata only)
- Woelfle MA et al. 2004, doi 10.1016/j.cub.2004.08.023 (via SCALE_ENDS)
- Yachi S, Loreau M 1999, "Biodiversity and ecosystem productivity in a fluctuating environment: the insurance hypothesis," *PNAS* 96:1463, doi 10.1073/pnas.96.4.1463 (abstract)
- Yi T-M, Huang Y, Simon MI, Doyle J 2000, "Robust perfect adaptation in bacterial chemotaxis through integral feedback control," *PNAS* 97:4649, doi 10.1073/pnas.97.9.4649 (abstract)
- Petrov V, Ouyang Q, Swinney HL 1997, "Resonant pattern formation in a chemical system," *Nature* 388:655–657, doi 10.1038/41732 (metadata only; named per PHYSICS F11)
- Project files as cited by path and section.
