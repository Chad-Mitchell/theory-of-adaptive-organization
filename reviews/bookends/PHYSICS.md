# Independent hostile review: PHYSICS (thermodynamics, nonequilibrium stat mech, astrophysics, planetary science)

**Target:** `theory/BOOKENDS.md` on branch `bookends` (PR #86), commit 98b7168, cross-checked against `theory/SCALE_ENDS.md`, `THEORY.md` v1.4.19 and `measurement/CLAIM_MAP_v2.md` (N25–N28). The repo has no top-level `CLAIM_MAP.md`; I used `measurement/CLAIM_MAP_v2.md`.
**Reviewer:** an independent Grok Bot executor. I did not write any of the files reviewed. Wednesday 18 Nov 2026, about 5:50–7:00 PM ET.
**Method:** a fresh clone into `/tmp/rev-phys`. Primary sources were opened this session (listed in §S). I did not rely on memory for any number. Numerics were run at nice 19. Nothing was pushed, commented or posted.

## Verdict: **PASS-WITH-FIXES** (the fixes are blocking for P2, P3, P4 and P9)

The file labels itself honestly. It defers to THEORY.md, keeps PROVED (in-model) apart from claims about nature, and rejects teleology and consciousness claims explicitly. Most of the numbers check out against primary sources:
- Egan & Lineweaver's S_obs ≈ 3.1×10¹⁰⁴ k, dominated by supermassive black holes;
- S_CEH = 2.6×10¹²² k against the asymptotic de Sitter value 3.3×10¹²²;
- a BH stores 2kT_H per nat and saturates the Bekenstein bound;
- the evaporation time is 1.2×10⁶⁷ yr (M/M☉)³, which I recomputed from Page 2005 eq. 19;
- the Page time is about 0.54 t_ev;
- the Lenton 2018 quotes are accurate.

**But the file's main new contribution, the K1/K2 boundary ("feedback on own state" vs "feedback on an exogenous, ruin-relevant variable"), is not physically operational as written.** Applied consistently, it moves galaxies, hurricanes, flames and Earth's *abiotic* weathering thermostat into K2. That breaks the §2.7 table and the planet decomposition. Several plain-words spine sentences are also physically wrong or decorative. None of this touches a PROVED (in-model) status. It does mean the proposed canonical changes P2–P4 and P9 should not be applied until findings 1–6 are fixed.

---

## Findings

### F1 — MAJOR. The K2 criterion "I_pred > 0 about an exogenous variable" is satisfied by essentially every driven dissipative structure, so it does not separate K1 from K2
- **Location:** §2.7 Axis K (line 149, "K2: reactive coupling (I_pred > 0 …)"); §2.2 bullet 1 (line 89); P2.
- **Source opened:** Still, Sivak, Bell & Crooks 2012, arXiv 1203.3271 (abstract and setup). "A system responding to a stochastic driving signal can be interpreted as computing … an implicit model of the environmental variables. The system's state retains information about past environmental fluctuations, and a fraction of this information is predictive." Also Kolchinsky & Wolpert 2018 (abstract), whose semantic information is the *causally necessary* part of the correlation, established by a scrambling intervention.
- **Problem:** By Still et al., any system with a nonzero response to a stochastic drive has I_mem > 0 and generically I_pred > 0. So the I_pred > 0 test is met by:
  - a hurricane (its intensity tracks SST);
  - a candle flame (fuel and O₂ supply);
  - a galaxy (F3);
  - Earth's silicate-weathering thermostat (F4);
  - a passive receptor (SCALE_ENDS E3(c));
  - an atom's speed distribution (SCALE_ENDS: 0.08 nats about the bath temperature).
  
  The file switches back and forth between "I_pred > 0" (Theorem P / Still sense) and "semantic information > 0" (Kolchinsky & Wolpert sense), as in §2.1 G2, §2.2 and P2. These are different quantities. The first is cheap and nearly universal. The second needs a counterfactual intervention and a viability function. A physicist would call the current K2 definition sloppy.
- **Fix:** Define K2 *only* by Kolchinsky & Wolpert semantic information > 0. Persistence time must fall under a scrambling intervention that conserves the energy and matter fluxes, relative to a stated viability function. State explicitly that I_pred > 0 alone is necessary but not sufficient (Still et al.: every driven system has it). Then re-derive every K entry in the §2.7 table under that single test, and mark each OPEN unless the intervention is defined.

### F2 — MAJOR. Theorem P "necessity" is invoked for entities whose persistence does not require the information (planet, Daisyworld)
- **Location:** §2.5 table row "Planetary regulation (Gaia)"; "Earlier chat claim corrected" (line 131); P2 examples.
- **Sources opened:** Lenton et al. 2018 abstract; Daisyworld as summarized via Wood et al. 2008 (Wikipedia extract opened; the Watson & Lovelock 1983 abstract is elided by the publisher). Regulation arises from "competition between the two daisy populations", and the temperature held is "an optimum for daisy growth".
- **Problem:** In Daisyworld the variable at risk of ruin is the *daisies'* habitability, not the planet's persistence. The planet persists blind, as the file itself says of Venus. So Theorem P forces nothing at planet scale. The information sits in a population that *is* under organism-level selection (black vs white daisies compete). Calling this "class 2b: coupled, unselected" puts the selection in the wrong place: it is unselected at planet scale but selected at the daisy level, which is exactly where the regulation comes from. Whether the planet carries a model then depends on which persistence criterion you choose, which the file never states.
- **Fix:** In §2.5 and P2, name the persisting entity and its ruin variable before assigning a class. Suggested wording: "Daisyworld regulation is carried by a population under organism-level selection (class 3 at daisy level). Its planet-scale effect is unselected at that scale. The planet as a body is blind-viable." Remove Daisyworld from the 2b examples, or mark it 'depends on the chosen persistence criterion'.

### F3 — MAJOR. "Galaxy: self-regulated star formation is class 2 / K1" is contradicted by standard gas-regulator ("bathtub") models, and fails the file's own criterion
- **Location:** §2.7 table row "Star, galaxy's star formation … K1"; §4 row **Galaxy**; SCALE_ENDS §2 class table.
- **Source opened:** Lilly et al. 2013, ApJ 772:119, arXiv 1303.5059 (abstract). In it, star formation "is instantaneously regulated by the mass of gas in a reservoir" and "the sSFR is set to the specific accretion rate of the galaxy". The regulator responds to an *exogenous*, drifting inflow (cosmological accretion). Quenching, the galaxy's "ruin" as a star-former, is environment-driven (strangulation, ram-pressure stripping).
- **Problem:** Under §2.2's rule, feedback on an exogenous, ruin-relevant variable makes a system K2. By that rule galaxies are K2, not K1. "Self-regulated" in the astrophysics sense means regulated *relative to an external supply*.
- **Fix:** Reclassify the galaxy as "K1 or K2, OPEN under the F1 test". Or drop galaxies from the known-negative group. Do not use them as an MV7 calibration case.

### F4 — MAJOR. "Rocky body = class 2, no model" vs "Gaia = 2b" ignores the abiotic carbonate–silicate thermostat
- **Location:** §2.5 table, row "The rocky body"; §4 row **Planet**.
- **Source opened:** Walker, Hays & Kasting 1981, JGR 86:9776, "A negative feedback mechanism for the long-term stabilization of Earth's surface temperature" (metadata and title via Semantic Scholar; abstract elided by publisher). The mechanism is a weathering rate that rises with temperature and draws down CO₂ as solar luminosity rises.
- **Problem:** This is abiotic feedback on an *exogenous drifting forcing* (the brightening Sun). By the file's own rule it is the same rung as Daisyworld. So the partition into "rock = self-regulated, no model" and "Gaia = coupled" does not follow from the stated criterion. "Venus persists too" shows only that the *rock* is blind-viable. It says nothing about whether the climate regulation is K1 or K2.
- **Fix:** Add a fifth component to §2.5, "abiotic climate regulation (carbonate–silicate cycle)", with the same 2b candidacy as Gaia. Or state that rock persistence and climate regulation are separate entities with separate ruin variables (see F2).

### F5 — MAJOR. Black-hole read latency: "everything else returns only after about the Page time" is not general
- **Location:** §2.3 "Black holes as the frozen extreme" (line 107); inherited from THEORY §2.3 and N26 condition (ii).
- **Source opened:** Hayden & Preskill 2007, arXiv 0708.4025 (abstract). "If the evaporation … has already proceeded past the 'half-way' point … additional quantum information deposited in the black hole is revealed in the Hawking radiation very rapidly. Information deposited prior to the half-way point remains concealed until the half-way point." Also Page 2005 (eqs 19–21) and Page 2013 (via SCALE_ENDS).
- **Problems:**
  - (a) For a post-Page-time hole, the retrieval delay for newly deposited information is short: the scrambling time, assuming unitarity, fast mixing and possession of the earlier radiation. N26's condition "read latency ≥ Page time" is therefore false for old holes.
  - (b) Every astrophysical BH today is colder than the CMB and *absorbs*. Evaporation has not started, so for present holes the latency is effectively unbounded, which makes the conclusion stronger, not weaker.
  - (c) The return of information assumes unitary evaporation. That is widely held, but the information problem is not settled, so it should be stated as an assumption.
  - The conclusion (BHs are useless memory) survives. The stated reason is imprecise.
- **Fix:** Replace the sentence with: "For a hole before its Page time, which includes every astrophysical hole today, since they are still colder than the CMB and not yet evaporating, information comes back no sooner than about the Page time ≈ 0.54 t_ev. After the Page time, newly deposited information comes back after about the scrambling time, but only to someone holding the earlier radiation and paying a decoding cost (Hayden & Preskill 2007; Harlow–Hayden is conjectural). This assumes unitary evaporation." Narrow N26 condition (ii) to match.

### F6 — MAJOR (spine). "The second law … is the only physical principle this picture leans on" is false within the file itself
- **Location:** §1 first paragraph (line 39); P9 ("One principle runs from atoms to the cosmos, the second law").
- **Problem:** The document leans on at least five other principles:
  - gravity, specifically the negative heat capacity of self-gravitating systems (§2.4);
  - the speed of light (LAT-1, §3 item 8);
  - general relativity plus quantum field theory (Hawking temperature, the Bekenstein bound, the Page time);
  - the low-entropy initial condition (the "gap" is not supplied by the second law; it is the past hypothesis / low gravitational entropy of the early universe, which Egan & Lineweaver discuss as "gravitational entropy" caveats);
  - conservation laws (proton stability, E4).
  
  "Order wears away" is also wrong as a general statement. Local order increases all the time under the second law: crystallization (which the same section uses as "Keep"), gravitational clumping, and dissipative structures. Physicists will read this as decorative.
- **Fix:** "Everything obeys the second law: total entropy rises, though local order can grow when it exports entropy. That law, together with gravity, the speed of light, and the universe's unusually low-entropy start, sets the stage. GTAO adds no new physics." Make the same change in P9.

### F7 — MODERATE. Comparing S_obs with S_dS mixes regions, and the "funding" claim is attributed loosely
- **Location:** §2.3 "The entropy gap as the funding" (line 109); §1 "Where the bookends sit" (line 56).
- **Source opened:** Egan & Lineweaver 2010, arXiv 0909.3983 (abstract and introduction PDF).
  - S_obs (observable universe, out to the particle horizon) = 3.1 (+3.0/−1.7)×10¹⁰⁴ k.
  - S_CEH = 2.6±0.3×10¹²² k.
  - The *interior* of the CEH holds 1.2 (+1.1/−0.7)×10¹⁰³ k.
  
  The quoted sentence ("is the reason dissipative processes are ongoing and that life can exist") is real. It refers to the gap below the *holographic bound* S_max ~10¹²³ k (Frampton et al. 2009), not specifically to the de Sitter horizon.
- **Problem:** The like-for-like comparison is S_CEH,int against S_CEH. Line 56's "black holes … the most entropy that region can hold" holds only for a region whose boundary is the hole's own horizon. "Most of the running-down that has happened so far is stored in BHs" conflates entropy *content* with entropy *production history*. The first is what E&L estimate.
- **Fix:** Quote the uncertainties. Compare S_CEH,int ≈ 1.2×10¹⁰³ k with S_CEH ≈ 2.6×10¹²² k, or state that S_obs and S_dS refer to different volumes. Attribute the funding sentence as E&L wrote it, against the holographic bound. Replace "running-down … stored" with "most of the entropy now present in the observable universe is in SMBHs".

### F8 — MODERATE. Landauer and Still et al. are applied outside their stated conditions
- **Location:** BOOKENDS §4 Chemistry row ("The Landauer floor does not prevent the switch-on"); SCALE_ENDS §0 item 1 ("A read … costs at least kT ln 2 per bit erased") and E2 ("the cost of a read is never 0"), on which BOOKENDS' atom and star placements rest.
- **Sources opened:**
  - Bennett 2003, arXiv physics/0210005: the cost attaches to logically *irreversible* operations, and reversible operations can in principle be thermodynamically reversible. So measurement can be free; erasure is not.
  - Sagawa & Ueda 2009, PRL 102:250602 (abstract): the bound is on measurement plus erasure together. For asymmetric memories, "the bound indicates the breakdown" of Landauer's form.
  - Still et al. 2012: discrete-time Markov dynamics, a *single heat bath at temperature T*, the system starting at equilibrium, and no feedback from the system to the signal.
- **Problems:**
  - (a) "Read cost ≥ kT ln 2" is wrong as phrased. It is the erase-and-reset cycle that is bounded.
  - (b) Stars, hurricanes, planets and galaxies are not single-bath isothermal Markov systems, and hurricanes and planets feed back on their drivers. So the Still et al. bound, which SCALE_ENDS E3(c) cites for "driven systems" generally, does not directly apply to anything in §2.4–§2.5.
  - (c) The Chemistry-row claim about the Landauer floor rests on N28's *bacterial* E_gen ≈ 10¹¹–10¹² kT. It carries no information about prebiotic chemistry, where per-"generation" energy budgets are unknown.
- **Fix:**
  - (a) Rephrase as "a measure-and-reset cycle costs at least kT × (mutual information) (Sagawa & Ueda)".
  - (b) Add a scope sentence: "Still et al. assume a single heat bath, Markov dynamics and no back-action on the drive. Stars, storms and planets violate these, and the bound is used here only as an analogy."
  - (c) Change the Chemistry row to "whether the Landauer floor binds before the cell is OPEN; the bacterial margin (N28) says nothing about prebiotic systems".

### F9 — MODERATE. Stars: "ruin fixed by own mass and composition; no outside variable enters" is false for most massive stars
- **Location:** §2.2 bullet 2 (line 90); §2.4 (lines 111–119), especially "Binaries and accretion".
- **Source opened:** Sana et al. 2012, *Science* 337:444, doi 10.1126/science.1223344 (abstract). "More than 70% of all massive stars will exchange mass with a companion, leading to a binary merger in one-third of the cases … binary interaction dominates the evolution of massive stars."
- **Problem:** For the majority of O stars, the outcome (lifetime, end state) is set by an external body. The *classification* survives: the star has no response whose payoff depends on tracking the companion, so the scrambling test (F1) would show no semantic information, and "held, self-regulated, no model" is defensible. Convection, dynamos and pulsation do not change this, because each is driven by internal gradients. Two parts of the stated *reason* are wrong, though:
  - "Its ruin is fixed by its own mass and composition" holds only for isolated stars.
  - "Upkeep h = L" is decorative. L is a radiative loss set by the interior–space gradient. It is not a maintenance cost in any control sense: a star that stops fusing does not dissolve. It contracts and *heats* (negative heat capacity), and white dwarfs persist on degeneracy pressure with no flux at all. The plain-words line "A star that swells cools and contracts again" also conflates the core thermostat (core heating leads to core expansion, which leads to a lower fusion rate) with the envelope.
- **Fix:**
  - Replace the reason with "no response of the star whose payoff depends on getting an exogenous variable right; external bodies (companions in most massive stars, Sana et al. 2012) can change its fate, but it cannot act on them."
  - Call L "the star's free-energy throughput", not "upkeep".
  - Reword the plain line: "If the core runs hot it expands, cools, and burns slower."

### F10 — MODERATE. Hurricanes are misfiled in the plain-words "Burn" paragraph
- **Location:** §1 "Burn" (line 43): "nothing outside has to be known … burns until its fuel is gone"; compare §2.2 (2b candidate) and §2.7 (K1, K2 OPEN).
- **Source opened:** Emanuel 1986, J. Atmos. Sci. 43:585, "An Air-Sea Interaction Theory for Tropical Cyclones" (metadata only; abstract elided).
- **Problem:** A hurricane is a heat engine running between the warm sea surface and the cold tropopause. It does not end by using up internal fuel. It decays when it is advected over cold water or land, or into shear: exogenous variables it cannot steer toward or away from. Put another way, it is not blind-viable, and it is transient. So it falls under caveat (c) ("transients outside P"), not under "nothing outside matters". The file is internally inconsistent here.
- **Fix:** In §1, list only star and flame (with a candle, fuel *is* the limit) under "Burn". Add: "Storms burn too, but they die when the world under them changes. Whether that makes them 'know' anything is open." Mark the hurricane "transient; outside Theorem P's long-run statement" in §2.7.

### F11 — MODERATE. BK-G2 is feasible as an apparatus but not yet diagnostic as specified
- **Location:** §2.1 "Testable consequence (HYPOTHESIS BK-G2)" (line 83); §4 Chemistry row.
- **Source opened:** Petrov, Ouyang & Swinney 1997, *Nature* 388:655, doi 10.1038/41732 (abstract), and Lin et al. 2004, PRE 69:066217 (abstract). Periodic optical forcing of the light-sensitive Ru(bpy)₃-catalyzed BZ reaction in a continuously fed reactor gives frequency-locked (Arnold-tongue) regimes. So entrainment and light-pulse phase control of a non-replicating chemical oscillator are routine.
- **Problems:**
  - (a) In a CSTR the oscillator "persists" as long as the experimenter's feed and parameters sit inside the oscillatory region. Phase relative to the drive does not enter its viability, so the predicted effect has no mechanism unless the system is *engineered* so that a reagent arrives in pulses and is usable only at a particular phase. If it is engineered that way, the result is built in.
  - (b) "Scramble the state–feed correlation while holding energy influx fixed" requires perturbations (light pulses or reagent injections) that themselves inject free energy or quench oscillations. The sham control must match dose and timing statistics, and the protocol does not specify it.
  - (c) The constant-feed control is degenerate: with no feed phase there is nothing to scramble, so "no drop" is guaranteed and not diagnostic.
  - (d) "Persistence time" and "ruin" (amplitude death? leaving the oscillatory branch?) are undefined.
- **Fix:**
  - Specify a viability function, for example time until oscillation amplitude falls below a threshold after the feed becomes pulsed and depleting.
  - Use BZ droplets or compartments that consume a pulsed reagent, with phase-resetting light pulses (treatment) against randomly timed pulses of identical dose (sham).
  - Replace the constant-feed control with an *aperiodic feed of the same mean* (blind control), where no phase information can help.
  - Preregister the effect size and the minimum detectable effect.
  - Label it "a test of the G2 mapping in a designed system, not evidence about natural prebiotic chemistry".

### F12 — MODERATE. "Life outlasts humans because many loosely correlated lineages": the borrowed formula's premises fail, and the conclusion is already established empirically
- **Location:** §2.5 "Why would the biosphere survive human extinction?" (line 133).
- **Problem:** The formula z′ = z√(N/(1+(N−1)ρ)) is the variance of a mean of correlated variables. It assumes a *pooled, fungible reserve*. The file's own §3 item 5 lists "non-fungible buffers … correlated shocks" as conditions under which coarse-graining fails, so the biosphere case violates its premise by the file's own rules. The physical claim (the biosphere survived repeated mass extinctions, and its long-run limit is a perfectly correlated slow drift: solar brightening drives CO₂ drawdown and water loss on a roughly Gyr timescale, per Caldeira & Kasting 1992, *Nature* 360:721; I opened only the metadata, not the text) is standard and needs no GTAO formula.
- **Fix:** Label this ANALOGY, not "DERIVED from PROVED rules". Cite the empirical record of survival through mass extinctions as the evidence. Note that the ultimate end of the biosphere is a ρ≈1 exogenous drift, consistent with the direction of the claim. Remove the formula, or add "premise (fungible pooled reserve) does not hold".

### F13 — MINOR. The heat-death ordering "knowing ends first, burning next, keeping last" is not established
- **Location:** §1 "Where the bookends sit"; §4 row **Cosmos, heat death**.
- **Source opened:** Krauss & Starkman 1999/2000, arXiv astro-ph/9902189 (abstract). In a Λ-dominated universe "the total information recoverable by any civilization … is finite, and … life cannot be eternal."
- **Problem:** Knowers can run on any gradient, including BH Hawking radiation long after stellar "burning" has ended (Adams & Laughlin's black-hole era). The file classes BHs as *frozen*, so a knower powered by an evaporating frozen store breaks the stated order. Krauss & Starkman also argue against Dyson-style hibernation rescuing indefinite computation, and the file's "hibernation … alarm clock" line should say so.
- **Fix:** "Knowing can last no longer than the last usable gradient, which may be black-hole evaporation, long after the stars. In an accelerating universe the total is finite (Krauss & Starkman)."

### F14 — MINOR. "Densest stores are hardest to read" is a black-hole-limit fact, not a general physical rule
- **Location:** §7 Q4; §2.3 role 2 (O5/BH-1 hypothesis).
- **Problem:** Holographic and Bekenstein bounds say the *maximal*-density store is a BH. They imply no monotone link between density and read cost below that limit. DNA is among the densest stores known and is read routinely by the cell. The file correctly leaves this OPEN. It should not be described as "borrowed from gravity" as if gravity implied it in general.
- **Fix:** "Gravity guarantees only that the densest possible store is unreadable on any useful timescale. Below that limit no physical law links density to read cost. O5/BH-1 is an empirical hypothesis about selected storage hierarchies."

### F15 — MINOR. LAT-1: light delay is not the binding latency for anything terrestrial
- **Location:** §1 ("because signals cannot travel faster than light, nothing large can know everything centrally"); §3 item 8; §4 Civilization row.
- **Numbers (computed):** light crossing half of Earth's circumference ≈ 0.067 s. Milky-Way-disk crossing (about 30 kpc) ≈ 1.0×10⁵ yr, so the file's "about 10⁵ yr" is correct.
- **Problem:** For firms, states and the planet, latency is set by processing, conduction and human decision time, which are orders of magnitude larger than L/c. The physics (c) binds only for interplanetary operations, where Mars one-way delay is several to about 20 minutes, and above. So "federation is forced by light" is decorative for terrestrial civilization. The real, testable claim is the general latency ℓ, which N27 already uses. The bound itself is elementary and fine.
- **Fix:** "Any signal delay forces federation; light speed sets the absolute floor, which binds only off-planet (spacecraft operations are the clean test)."

### F16 — MINOR. "Compositional heredity is too inaccurate … cumulative design needs template heredity" overstates Vasas et al. 2010
- **Location:** §2.1 table, row G3 (line 73).
- **Source opened:** Vasas, Fernando, Santos, Kauffman & Szathmáry 2012, *Biology Direct* 7:1, doi 10.1186/1745-6150-7-1, "Evolution before genes" (abstract). It shows that "accumulation of adaptations in chemical reaction networks can occur" when networks contain multiple viable cores in compartments: "a poor man's natural selection … prior to genetic templates".
- **Fix:** "Simple autocatalytic sets lack evolvability (Vasas et al. 2010). Compartmentalized networks with multiple viable cores can show limited heredity and selectability (Vasas et al. 2012). Strong cumulative design still points to template heredity." This also strengthens the file's own graded-onset story.

### F17 — NIT. Small accuracy points
- The 1.2×10⁶⁷ yr (M/M☉)³ figure counts photons and gravitons only. Recomputed from Page 2005 eq. 19, I get 1.16×10⁶⁷ yr. Adding three massless neutrino species gives 1.5×10⁶⁶ yr. Note "massive neutrinos are not emitted at T_H ≪ m_ν c²/k". Note also that the clock starts only once the CMB is colder than T_H.
- "The present entropy … is dominated by supermassive black holes": add E&L's uncertainty, "+3.0/−1.7".
- Kolchinsky & Wolpert's viability criterion is "the system's ability to keep itself in a low entropy state" (abstract), not "persistence time". BK-G2 and K2 should use one of the two consistently.

---

## What survives the physics check (no change needed)
- The BH information density at 2kT_H per nat and the saturation of the Bekenstein bound (checked algebraically).
- Page time ≈ 0.54 t_ev (Page 2013, via SCALE_ENDS).
- SMBH dominance of S_obs (E&L 2010).
- The 3.3×10¹²² asymptotic de Sitter value, distinguished from the current S_CEH (SCALE_ENDS line 202).
- Stars as held, self-regulated and non-modelling, once F9's reasoning is fixed. Dynamos, convection and pulsation are internally driven and do not change the class.
- The rejection of teleology ("black holes exist *in order to*…") and of GTAO-based consciousness claims.
- The Lenton et al. 2018 quotations, which match the abstract verbatim.
- The caveat that the entropy gap is not itself usable free energy.

## §S Sources opened this session
- Egan & Lineweaver 2010, arXiv 0909.3983: abstract and introduction (PDF).
- Still, Sivak, Bell & Crooks 2012, arXiv 1203.3271: abstract and problem setup (PDF).
- Hayden & Preskill 2007, arXiv 0708.4025: abstract.
- Page 2005, arXiv hep-th/0409024: eqs 19–21 (PDF); lifetime recomputed.
- Krauss & Starkman, arXiv astro-ph/9902189: abstract.
- Bennett 2003, arXiv physics/0210005: abstract.
- Sagawa & Ueda 2009, PRL 102:250602: abstract (Semantic Scholar).
- Lilly et al. 2013, arXiv 1303.5059: abstract.
- Sana et al. 2012, *Science* 337:444, doi 10.1126/science.1223344: abstract.
- Lenton et al. 2018, *TREE* 33:633, doi 10.1016/j.tree.2018.05.006: abstract.
- Kolchinsky & Wolpert 2018, *Interface Focus* 8:20180041: abstract.
- Vasas et al. 2012, *Biology Direct* 7:1: abstract.
- Walker, Hays & Kasting 1981, JGR 86:9776: title and metadata only.
- Emanuel 1986, JAS 43:585: metadata only.
- Caldeira & Kasting 1992, *Nature* 360:721: metadata only.
- Watson & Lovelock 1983: abstract elided by publisher; Daisyworld mechanism taken from the Wikipedia summary of Wood et al. 2008 (secondary).
- Petrov, Ouyang & Swinney 1997, *Nature* 388:655: abstract; Lin et al. 2004, PRE 69:066217: abstract.

---

# Round 2 (revision at head 49bd64cb4871c55cf8828fd0f29fe34858031f0a)

**Reviewer:** the same independent physics reviewer. Wednesday 18 Nov 2026, about 6:10–6:45 PM ET. Fresh `git fetch` in `/tmp/rev-phys`, checkout of the head above, read of `theory/BOOKENDS.md` (419 lines) and `<local>/gtao/reviews-bookends/DISPOSITION.md`. Nothing was pushed, commented or posted.

## Round-2 verdict: **PASS-WITH-FIXES (minor)**

All 17 round-1 findings are fixed in substance. The new physics text has one moderate error, the BK-G2 treatment arm (R2-1). That error partly comes from my own round-1 F11 wording. It also has five minor or nit items. None affects a CLAIM_MAP label.

- **Safe to apply as written:** BK-P1, P3, P5, P7, P8, P9, P10 (physics-neutral; biology is not my remit), P12 and P14.
- **Safe after a one-line edit:** BK-P2, P4, P6, P11 and P13 (see table below).
- **BK-G2 should not be preregistered** until R2-1 is fixed.

## Round-1 findings: verification

| F | Fixed? | Where checked / note |
|---|---|---|
| F1 | **Yes** | §0.2 and §2.0.2 separate correlation, semantic information (BK-SEM), structural model (IMP; BK-IMP) and selected model. I_pred > 0 is explicitly "nearly universal". K axis rebuilt in §2.7. |
| F2 | **Yes** | §2.5 table names entity and ruin variable first. Daisyworld is "selected at the daisy level, unselected at planet scale". |
| F3 | **Yes** | Galaxy is K1 (leaky integrator), OPEN, and removed from MV7/SE9 (§2.4, §2.7, §4, BK-P11). The Lilly 2013 quote is accurate (nit R2-6). |
| F4 | **Yes** | Carbonate–silicate row added as a candidate structural model without selection. Physically sound: the CO₂ reservoir integrates outgassing minus weathering, so if weathering depended on T alone the steady state would fix T. See R2-5 for scope. |
| F5 | **Yes** | §2.0.4 and BK-P7 match Hayden & Preskill 2007 (abstract re-read in round 1): pre-Page-time holes (all astrophysical holes, colder than the CMB) vs post-Page holes (scrambling time, needs the early radiation, decoding cost), with unitarity assumed. Correct. |
| F6 | **Yes** | §0.1, §1 and BK-P9. "Order can grow when it exports entropy" is correct. |
| F7 | **Yes** | §2.3 numbers and error bars match the Egan & Lineweaver abstract exactly. Like-for-like gap S_CEH,int vs S_CEH. Holographic-bound attribution. "Running-down stored" withdrawn. |
| F8 | **Yes** | §2.7 floors (Landauer for erasure; Sagawa–Ueda for measure plus reset; reversible measurement), Still et al. scope note, Chemistry row OPEN. |
| F9 | **Yes** | §2.4: Sana 2012, "h = L" and "ruin fixed by own mass" withdrawn, core-thermostat line correct. |
| F10 | **Yes, one wording slip** | Hurricane moved out of steady "Burn" and marked transient, outside GT-P. See R2-2 for the slip. |
| F11 | **Partly** | Viability, sham, rhythmless control and MDE are all added. The treatment arm is still wrong (R2-1). |
| F12 | **Yes** | Relabelled ANALOGY plus PRIOR ART. Yachi & Loreau quote verified against the Europe PMC abstract (scope nit R2-7). |
| F13 | **Yes** | Ordering withdrawn. I checked the Krauss & Starkman text this round (arXiv astro-ph/9902189, PDF): it argues that hibernation "will fail not only in a cosmological constant dominated universe, but in any ever-expanding universe" (alarm clocks dissipate; finite CMB photons). The file's statement is supported. |
| F14 | **Yes** | §7.4 wording is correct. |
| F15 | **Yes** | §1, §3.8 and §4. 0.07 s is correct. Weighting the spacecraft case as weak is a good addition. |
| F16 | **Yes** | §2.1 Q4, matching the Vasas et al. 2012 abstract. |
| F17 | **Yes** | Lifetime caveats (photons plus gravitons, neutrinos, CMB clock), E&L uncertainties and K&W viability wording all present. The hydrogen ionization Boltzmann factor 10^−228.5 at 300 K is correct (13.6 eV / 0.02585 eV = 526; e^−526 ≈ 10^−228.5). |

## New findings (round 2)

**R2-1 — MODERATE. BK-G2's treatment arm injects the phase information from outside, so it no longer tests whether the droplet holds any.**
- **Location:** §2.1 BK-G2, arm (T): "phase-resetting light pulses that keep the oscillator's phase matched to the reagent pulses".
- **Problem:** In arm T the *experimenter's controller* tracks the feed and forces the droplet's phase. A T > S result would show that externally imposed phase-matching helps an engineered droplet. It would not show that the droplet's *own* state carries information whose scrambling shortens persistence, which is the Kolchinsky & Wolpert test the file says BK-G2 instruments. My round-1 F11 fix ("phase-resetting light pulses (treatment) vs randomly timed pulses (sham)") invited this. I withdraw that wording.
- **Fix:**
  - (T) Let droplets entrain *on their own* to the pulsed reagent. Light pulses at the same dose are delivered only in the phase-insensitive part of the measured phase-response curve, so they do not move the phase.
  - (S, the scrambling arm) Use the same dose, delivered at random phases so that it resets the droplet's phase relative to the feed. This is the K&W intervention.
  - (C) Keep the rhythmless matched-mean control as written.
  - Prediction: T > S and S ≈ C. Also preregister a check that light at the matched dose does not by itself change amplitude decay under the C feed.
  - Physical premise to verify before prereg: the forcing must sit inside a measured Arnold tongue (Petrov, Ouyang & Swinney 1997; Lin et al. 2004), or there is no natural entrainment to scramble.

**R2-2 — MINOR. A hurricane "follows the world but holds nothing about it" contradicts §2.0.2.**
- **Location:** §1, "Burn".
- **Problem:** Following the world *is* correlation, which §2.0.2 says hurricanes have.
- **Fix:** "Its state follows the world, so it carries a correlation with it, but as far as anyone knows nothing in it uses that correlation to last longer."

**R2-3 — MINOR. "K2 and K3 require held" rests on a weaker argument than is available.**
- **Location:** §2.7, "How they depend on each other".
- **Problem:** SE-E3's "memory costs dissipation" does not by itself cover predictive memory. Still et al.'s bound is on *non*-predictive information. The claim is still right, and there is direct prior art for it:
  - Lan, Sartori, Neumann, Sourjik & Tu 2012, *Nat Phys* 8:422, doi 10.1038/nphys2276 (abstract opened): "adaptive processes are necessarily dissipative, and continuous energy consumption is required to stabilize the adapted state";
  - Cao, Wang, Ouyang & Tu 2015, *Nat Phys* 11:772, doi 10.1038/nphys3412 (abstract opened): phase coherence of biochemical oscillations scales with free energy dissipated per period.
- **Fix:** Cite both as the basis for "K2 (integral, perfect adaptation) and K3 (accurate oscillator) need throughput". Lan et al. also directly support BK-P4's new kill (ii).

**R2-4 — MINOR. §0.4 states as fact that "an entrained oscillator can act ahead without heredity".**
- **Problem:** A forced passive oscillator can settle with a phase lead. That a non-hereditary chemical system acts ahead in the file's sense (a realized lead that improves viability) is not shown, and it is exactly what BK-G2 would test.
- **Fix:** "may be able to act ahead (phase lead) without heredity; untested (BK-G2)". The same hedge applies to §2.1 Q5's "no heredity needed".

**R2-5 — MINOR. Scope of the carbonate–silicate row.**
- **Problems:**
  - (a) With "habitability, which matters only to life" as its ruin variable, the abiotic cycle is not a persisting entity in Theorem P's sense. So only BK-IMP (structural) applies, not BK-SEM. Say so.
  - (b) Earth's actual weathering feedback is strongly biologically mediated (land plants, soils) and also depends on pCO₂, not on T alone. Perfect adaptation is therefore not expected even in principle, and "abiotic" refers to the idealized or pre-vegetation cycle.
  - (c) The model test is cleaner on models (Walker et al.-type box models) than on Earth data, where n = 1 and the forcing is slow.
- **Fix:** Add one sentence covering (a) to (c). The "candidate, OPEN" label is right.

**R2-6 — NIT. Lilly et al. condition dropped.** The abstract's "sSFR is set to the specific accretion rate" holds "if the SFR efficiency and wind mass loading are constant". Add the condition. "Pending BK-IMP on gas-regulator models" is odd: the regulator *model* already gives a leaky steady state (gas mass scales with inflow). Write "K1 per the Lilly 2013 regulator model; an observational BK-IMP form is not defined (OPEN)".

**R2-7 — NIT. Yachi & Loreau's scope.** Their model concerns the temporal mean and variance of *ecosystem productivity* under environmental fluctuation, driven by asynchrony of species responses (Europe PMC abstract). It does not concern lineage survival through extinction shocks. Say "extended here by analogy". Also, "standard paleontology … not cited here" should carry at least one opened citation before it goes into a canonical file.

## Proposals BK-P1…BK-P14: application safety (physics view)

| Proposal | Verdict | Required edit |
|---|---|---|
| BK-P1 | **Safe** | — |
| BK-P2 | Safe with edit | Say "candidate" for galaxies-as-K1 as well. Note that under the new split the carbonate–silicate cycle would sit in class 3 (structural model) if BK-IMP passed. State that class 3 then includes unselected systems, or split class 3 into 3 and 3-selected. |
| BK-P3 | **Safe** | — |
| BK-P4 | Safe with edit | Cite Lan et al. 2012 for kill (ii). Kill (i) should read "with no flux (not merely a vanishing one; passive quasi-static coupling, SE-E3(c), is excluded)". |
| BK-P5 | **Safe** | — |
| BK-P6 | Safe with edit | "Semantic information is 0" should read "is expected to be 0 (physical argument, not computed)", matching §2.0.4's own label. |
| BK-P7 | **Safe** | Physics correct as written. |
| BK-P8 | **Safe** | — |
| BK-P9 | **Safe** | Optional: add "quantum physics" to match §0.1. |
| BK-P10 | Safe (physics-neutral) | Biology to be judged by the BIO reviewer. |
| BK-P11 | Safe with edit | Add "Still et al. formalize this for isothermal Markov systems; elsewhere it is an analogy" where SE-E3(c) cites Still for "driven systems". |
| BK-P12 | **Safe** | — |
| BK-P13 | Safe with edit | BK-G2 row should read "HYPOTHESIS, design OPEN pending R2-1". |
| BK-P14 | **Safe** | — |

## Required before merge into canonical files
1. R2-1: redesign BK-G2 arms; block its prereg until done.
2. One-line edits to BK-P2, P4, P6, P11 and P13 as tabled.
3. R2-2 to R2-7 wording, which are low effort.

## Sources opened in round 2
- Krauss & Starkman, arXiv astro-ph/9902189 (full PDF, hibernation passage).
- Lan et al. 2012, *Nat Phys*, doi 10.1038/nphys2276 (abstract).
- Cao et al. 2015, *Nat Phys*, doi 10.1038/nphys3412 (abstract).
- Yachi & Loreau 1999, *PNAS* 96:1463, doi 10.1073/pnas.96.4.1463 (Europe PMC abstract).
- Round-1 sources re-used: Hayden & Preskill, Egan & Lineweaver, Lilly et al., Sana et al., Petrov et al.
