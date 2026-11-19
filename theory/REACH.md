# REACH: what the theory says about viruses and life, the cosmic web, wormholes, the torus, dark matter and energy, and fractal time

Wednesday 18 November 2026, evening ET (America/New_York). Written by a Grok Bot executor for Chad Mitchell, via Ace (the author's requests t1953 to t1956). Nothing was posted or sent by this work. Companion notes: [`COSMIC_WEB.md`](COSMIC_WEB.md), [`WORMHOLES.md`](WORMHOLES.md), [`TORUS.md`](TORUS.md). Code checks: `reach_checks/` (outputs saved beside the code). Self-review (not independent): `reviews/reach_2026-11-18/REVIEW.md`. Independent review: `reviews/reach_2026-11-18/INDEPENDENT_REVIEW.md` (READY-WITH-FIXES; its fixes are applied in v1.4.24).

**What this file is.** A derivation file that `THEORY.md` §2.3 points to. It applies the theory's *own existing machinery* (the three classes in `SCALE_ENDS.md` and `BOOKENDS.md`, the switch-on conditions S1–S4, LAT-1, T7, T9) to questions that were asked of it. It changes no existing status, no locked prediction and not the spine. Where Chad's framing (t1953 to t1956) was treated as an idea to test, the verdict is stated plainly, including where the idea does not hold up.

**Labels used.** DERIVED (follows from the theory's definitions and results, premises stated), RESTATEMENT (the theory's words for something already published), PRIOR ART (published; credited), HYPOTHESIS (a claim with a kill condition, untested), CONDITIONAL (true only if a stated physical assumption holds). CLAIM_MAP rows N36 to N46 carry the repo's own status words. Every source cited below was opened this session at the level stated; the list at the end says how much of each was read ("abstract", "full text read", "metadata only").

---

## 0. In plain words

**Everything that lasts has to pay.** The second law says the total disorder of the universe goes up. A structure can stay ordered anyway, but only by pushing disorder out somewhere else. GTAO's one budget is the bill for that: keeping the structure up, keeping its record of itself intact, and (for things in a changing, dangerous world) staying matched to that world. Different things pay different parts of the bill, and some pay none of it.

**Virus: alive as a lineage, not as a particle.** This is the main result here.
- A virus *particle* pays nothing. It does not burn fuel, repair itself or sense anything. It lasts the way a crystal or a seed in a deep freeze lasts, until chemistry wears it out. Under the theory's classes it is *frozen*.
- An *infected cell* is a different object. It is a held structure that burns the host's fuel, and the virus's genes direct it. The virus does not pay the upkeep; the host does.
- The *lineage* (every particle and infection descended from one another) has heredity, is selected, and tracks a host immune system that keeps changing. That is the same rung of the theory's ladder (a selected model) that a cell lineage occupies, without paying its own upkeep. So a virus is alive in the one sense the theory cares about (its information is selected to stay matched to a changing world) and not alive in the sense of paying its own bills.
- The sharper way to say it: **"alive" is not one yes-or-no switch. It is a ledger of who pays for what.** A cell pays for nearly everything itself. A virus pays for almost nothing itself and borrows the rest from a host. A seed or a tardigrade in a freezer is, for as long as it is dormant, the same kind of thing as a virus particle. A hurricane pays but has no record to keep, so it is not alive. The ledger puts all of these on one scale.
- **What is new and what is not.** The pieces of the "alive as a lineage, not as a particle" verdict are already in the literature: Forterre's virocell (the infected cell is the viral organism, and viruses should not be confused with their virions); Koonin & Starokadomskyy (2016), who call the yes-or-no question "without substance" and put viruses on a continuum of replicators; Dupré & Guttinger (2016), who treat viruses as processes; and the committee behind the NASA working definition, whose word "system" lets a virus be alive without individually exemplifying life (Benner 2010). What GTAO adds is the cost ledger, its tie to the second law, a place for seeds, spores, endogenous retroviruses and obligate intracellular bacteria on the same scale, and a few predictions that can fail (§1.5). It does not redefine life. It reframes an old question as one the theory can price.

**Cosmic web.** The web of galaxy filaments really is a network, and it really is clustered. A plain proximity rule on random points gives much of that clustering, and the real web adds more (about 0.6 against 0.45) plus a broader degree spread: that excess is real gravitational structure. No hubs have been reported, unlike organization networks, though nobody has tested for them with a hub statistic. The theory's cost terms suggest why there would be none: hubs appear when delay is priced against link cost, and nothing in the cosmic web pays for delay. So the resemblance is real, part geometry and part gravity. It does not show function. (`COSMIC_WEB.md`; corrected after the independent review)

**Wormholes.** Traversable wormholes would need matter that violates the standard energy conditions; none is known. IF they existed, the theory's light-delay bound (LAT-1) would relax, but not to "everything centralizes". For how far one tracker can reach, open versus finite is the first split: a finite "tube map" of throats with a per-hop delay is a faster medium, and LAT-1 still holds with a bigger effective speed; open throats remove the distance limit (`WORMHOLES.md` §4b, added after the independent review). For whether to centralize, more things still bind: how many bits a throat can carry, how well the target's drift is shared across places, the price of telling versus looking, and whether throats stay open. NASA's 2012 "X-points" are magnetic reconnection sites, not spacetime wormholes. (`WORMHOLES.md`)

**Torus.** Two cycles that do not lock live on a torus, and under coupling they lock inside "Arnold tongues". That is textbook mathematics. The earlier toy simulation that "showed no torus effect" was not a valid test (its random coincident resets force locking by construction), so it is INVALID as a test; its preregistered staircase prediction did fail inside the toy, and the INVALID judgment came after the result. Real timing data have not been tried. Nothing in the theory says the universe is a torus; Planck's data constrain that on their own. (`TORUS.md`)

**Dark matter and dark energy.** Inputs, not outputs. The theory does not explain them. Dark energy sets the cosmic horizon, which already caps memory and the price of erasing a bit (§3).

**Fractal time.** The theory does not say time is fractal. It says that, *given* measured inputs, the best design is computed; and that the best architecture is self-similar only where the world's change has no characteristic time scale, which is true for some data and false for others (§4).

---

## 1. Virus: which costs does it pay itself?

### 1.1 The ledger (the theory's own terms)

The three costs from `THEORY.md` §0, split so that each can be paid by someone else:

| Line | Meaning | Where it comes from in the theory |
|---|---|---|
| **U** (upkeep) | free-energy flow that holds the structure against decay | held vs frozen (SCALE_ENDS §3.3; growth inequality, THEORY §2.3) |
| **F** (fidelity) | copying and repairing the record, above the error threshold | S1, Eigen threshold εL ≲ ln σ (SCALE_ENDS §3.4) |
| **T** (tracking) | reads of, and responses to, a world that drifts and can ruin the entity | hold band, S2 and S3 (SCALE_ENDS §3.4; THEORY §2.2) |

And a column for **who selects the design** (Axiom 7): the entity itself, a lineage, or nothing. The classes:

- **Frozen** (class 1): U = F = T = 0 paid by the entity; lifetime set by a barrier (SCALE_ENDS §3.1, E4).
- **Held, no structural model** (class 2): pays U, nothing selected (stars, flames).
- **Selected model** (class 3s): heredity above the Eigen threshold, a world-dependent action, drift in the hold band, a first nat that pays (S1 to S4; BOOKENDS §2.0.2).

### 1.2 Placing the viral objects

| Object | U | F | T | Class (GTAO) | Verdict | Status |
|---|---|---|---|---|---|---|
| **Virion** | none (no metabolism: Forterre 2017 puts the viral organism in the infected cell, and says viruses "should not be confused with their virions") | none (no repair) | none beyond receptor binding | frozen; a *product* of selection, not a participant | not alive as a particle | RESTATEMENT + DERIVED |
| **Infected cell (virocell)** | paid by host | polymerase fidelity partly the virus's own, repair partly the host's | the virus's regulatory decisions, executed on the host's machinery | held structure with a selected design | alive in Forterre's sense (organism for part of its cycle) | RESTATEMENT |
| **Viral lineage** | host | virus-encoded plus host | selected response rules (for example the lysis or lysogeny decision, Erez et al. 2017) | selected model (S1 to S4 met at lineage level) | alive as a lineage | DERIVED (conditional on S1 to S4 holding) |
| **Dormant seed, spore, tardigrade tun** | near zero while dormant | repair deferred to revival | none while dormant | frozen, then held at revival | the same as a virion while dormant; alive as an organism after | DERIVED |
| **Endogenous retrovirus (ERV)** | none | host's genome copying and repair | none | a lineage riding the host's germ line (Stoye 2012) | a fossil lineage unless it is still expressed | RESTATEMENT |
| **Obligate intracellular or reduced symbiont** | partly outsourced to host | mostly own | reduced | selected model, with part of the ledger on the host (McCutcheon & Moran 2012: "retain only the most essential functions, often including a considerable fraction of genes that serve the hosts") | alive, with a shorter self-paid ledger than a free-living cell | RESTATEMENT |
| **Giant virus (Mimivirus)** | none | encodes components of all DNA repair pathways and several translation components (aminoacyl-tRNA synthetases, factors); no ribosome is listed in the abstract (Raoult et al. 2004) | none known | virion frozen; virocell held | nearer to the cell end of the ledger than a small virus, but the particle still pays no U | DERIVED |
| **Viroid** | host | none beyond the host's RNA polymerases (Gago et al. 2009: replication mediated by host RNA polymerases and, in some cases, hammerhead ribozymes; Flores et al. 2014: no protein-coding ability) | none | a bare replicator at the edge of the threshold: mutation rate 1/400 per site in one viroid, the highest reported (Gago et al. 2009) | a lineage with the shortest ledger; sits at the Eigen limit | DERIVED (conditional) |
| **Prion** | host (it converts host PrP) | the template is a conformation, not a sequence | none | has heredity and selection without a nucleic-acid genome (Li et al. 2010: "subject to mutation and selective amplification") | a replicator lineage with a protein template; whether S1 applies is open (§1.6) | HYPOTHESIS |
| **Hurricane or flame** (contrast) | yes | no record | none | held, no model | not alive: no heredity | PRIOR ART in substance (BOOKENDS) |

Notes on the least certain rows. (i) "None" for the virion's U, F and T is the standard picture of a virion as an inert package; the theory's contribution is only the accounting. A virion shown to burn energy to repair itself outside a host would break the frozen verdict for that particle (kill K-V1 below). (ii) Prions are edge-case: Li et al. 2010 is the evidence that heredity and selection exist without a nucleic acid; whether the Eigen-type threshold has a prion form is not known. (iii) The viroid in Gago et al. 2009 is chrysanthemum chlorotic mottle viroid, 398–399 nucleotides (Navarro & Flores 1997, abstract; added by the independent review), so the "order one per genome" statement in §1.4 holds: εL ≈ 399/400 ≈ 1.0.

### 1.3 Derivation, step by step (from the classes, no outside premise)

1. **The virion is frozen.** It has no response whose alternatives are selected during its own life. Selection acts on the *design* of virions only through the lineage that makes them. So under Axiom 7's reading of "action" the particle has Φ = 0 (SCALE_ENDS SE1), and E4 gives it a barrier-set lifetime. This is the same reasoning that places a seed in cold storage, and it is partly definitional in the same way (SCALE_ENDS §3.2 item 3). DERIVED, partly definitional.
2. **The virocell is held.** It needs D > 0, supplied by the host, and the virus does not pay it. The Landauer floors apply to the host's machinery.
3. **The lineage is where the switch-on conditions are tested.** S1 (heredity below the error threshold): a replicator keeps its information only if εL ≲ ln σ (Eigen 1971). For viruses the sharper published form is lethal mutagenesis: extinction is expected when e^{−U_d}·R_max < 1, where U_d is the deleterious mutations per genome per replication and R_max the infectious progeny per infection. **Source check:** the abstract of Bull, Sanjuán & Wilke (2007) states the sufficient condition in words (each genotype produces on average fewer than one progeny that goes on to infect a new cell) and says the threshold has an ecological component and cannot be calculated from the mutation rate alone. The e^{−U_d}·R_max form is the standard deterministic mutation-load (Haldane–Muller) form, which I did not find in the opened text. So a lineage that persists, in that deterministic model, has U_d ≤ ln R_max; this is a bound under that model, not the paper's full threshold. S2 (a world-dependent action): temperate phages decide between lysis and lysogeny, and some use a peptide signal produced in earlier infections to do so (Erez et al. 2017). S3 (drift in the hold band): the lineage tracks a host immune landscape that moves (§1.5). S4 (the first nat pays): E_gen > β_phys·kT (SCALE_ENDS §3.4), where E_gen is the energy per infection cycle, supplied by the host, so the Landauer floor is not the binding term.
4. **The verdict follows.** The particle is frozen, the infection is held, the lineage is a selected model. "Alive" is therefore a question about which row you are asking about, and the ledger answers it row by row.

### 1.4 Evidence and what it says about the thresholds (opened)

- **Drake's rule (DNA microbes).** The genome-wide mutation rate varies about 2.5-fold around 0.0033 per replication across organisms whose genome size varies about 6,500-fold, so the per-base rate is inversely proportional to genome size (Drake 1991, abstract). That is the Eigen threshold seen in the data: bigger genomes need lower per-site error.
- **Viruses.** Substitution rates per nucleotide per cell infection run 10⁻⁸ to 10⁻⁶ for DNA viruses and 10⁻⁶ to 10⁻⁴ for RNA viruses. A negative correlation between mutation rate and genome size appears among RNA viruses "but this result requires further experimental testing" (Sanjuán et al. 2010, abstract). So a Drake-type rule for RNA viruses is *not* established, and GTAO does not claim it.
- **The extreme.** A hammerhead viroid has a mutation rate of 1/400 per site, "the highest reported for any biological entity", which "can only be tolerated by extremely simple genomes" (Gago et al. 2009, abstract). With a genome of 398–399 nucleotides (Navarro & Flores 1997) the product εL is about one per replication, which is the Eigen limit for modest selective advantage.
- **All of this is PRIOR ART.** GTAO restates the Eigen threshold as condition S1. It does not improve on lethal mutagenesis theory.

### 1.5 Predictions

| ID | Prediction | Label | Kill condition |
|---|---|---|---|
| **K-V1** | **Particle is frozen.** Infectivity of a purified virion outside a host decays by barrier-type kinetics with no energy-dependent self-repair. Any "no-upkeep" virion should classify as h = 0 in the known-groups check (FRAMEWORK MV7) | HYPOTHESIS (known-groups calibration; expected to pass, so a pass is weak) | A virion shown, outside a host, to consume free energy to repair or maintain itself at a rate that changes its decay |
| **K-V2** | **Lineage viability bound.** A viral lineage persisting over many generations has U_d ≲ ln R_max; at the viroid extreme εL ≈ 1 | PRIOR ART (Eigen 1971; Bull et al. 2007) restated as S1 | A lineage kept long-term with a measured U_d well above ln R_max and no compensating mechanism (for example high multiplicity of infection, which complementation can mask). The published threshold is broader (it has an ecological part), so this row inherits only the deterministic-load bound |
| **K-V3** | **The lineage tracks the host's immune landscape, and the landscape's speed is partly set by the lineage itself.** At matched mutation supply and matched structural constraint, lineages facing broader and longer-lasting population immunity should fix antigenic changes faster. Needs: antigenic cartography per lineage (Smith et al. 2004 is the method), seroprevalence by age and waning rates | HYPOTHESIS (OPEN; the prior-art sweep of immune-driven antigenic evolution is owed, so no novelty claim) | Non-positive rank correlation between antigenic drift rate and immunity durability × attack rate across at least a preregistered number of lineages, with mutation supply and functional constraint measured. Rival: constraint on the receptor-binding site alone |
| **K-V4** | **Heredity without nucleic acid.** If S1 is the criterion, a prion strain population should show a conformational-switching error threshold analogous to εL ≲ ln σ | HYPOTHESIS; **no kill is defined until ε and the information per template are defined** | Not yet definable |

K-V3 is the only prediction here that is specific to GTAO. K-V1 and K-V2 are checks that the classification is coherent. Neither the classification nor K-V3 has been tested on data.

**Honesty about the immune side.** An earlier immune cue guess in this repository ("replicating or particulate antigen, therefore long immune memory") scored 5 of 8 and was killed on proxy, below its locked 65% line (COLLAPSE1 A1; CLAIM_MAP H18 PROXY-FAIL, MV5). BIO1's naive "immune memory time tracks pathogen drift" also does not hold as measured (H16 OPEN), because a measured half-life depends on when it is measured (COLLAPSE1: for a power-law decay, half-life ≈ age at measurement × 0.69/m). Nothing in §1 uses either result. BIO1's "drift erodes how well old memory protects" survives (P3b). The immune system is the host-side tracker; K-V3 is about the *virus-side* tracker.

### 1.6 Edge cases, one at a time

- **Prions.** They have heredity and selection (Li et al. 2010) but a protein template. By S1 to S4 they are a lineage that pays no U, F or T of its own. Whether the threshold has a prion form is open (K-V4). We make no claim beyond this.
- **Viroids.** The shortest ledger of any lineage that has heredity; consistent with the Eigen limit (§1.4). The "RNA-world relic" reading is Flores et al. 2014's; GTAO takes no position.
- **Giant viruses.** Mimivirus carries repair pathways and translation components (Raoult et al. 2004), so the *lineage's* F line is partly self-paid. The particle's U and T are still zero. It moves toward the cell end of the ledger without reaching it. Forterre (2017) calls the intracellular state the organism.
- **Endogenous retroviruses.** The lineage is carried by the host's germ line (Stoye 2012), so its U and F are the host's. A silenced ERV is a record, a fossil. An ERV that still replicates, or that benefits the host (Stoye 2012: inherited retroviruses "can also confer benefits"), is a lineage selected at host level.
- **Obligate intracellular and reduced symbionts.** These are cells (own heredity, repair and response) with a ledger partly outsourced (McCutcheon & Moran 2012). They show that the virus/cell boundary is a gradient in the ledger, not a wall.
- **Seeds, spores, tardigrade tuns.** A date seed dated to the first century CE germinated (Sallon et al. 2008); an Antarctic tardigrade frozen for 30.5 years revived and reproduced (Tsujimoto et al. 2016). Dormant, they have no measured upkeep and wait; revived, they are held. This is the "frozen, then held" case, and it is the cleanest reason that "alive" must be asked of the *stage*, not of the species.
- **Lysogeny and latency.** A prophage or a latent genome is held by the host. The lineage still carries its response rule (Erez et al. 2017: progeny phages measure a peptide concentration and lysogenize if it is high). The sign of that rule across environments is not derived here, and the opened sources do not settle it.

### 1.7 What is new, what is not (the claim to make about it)

- **Not new:** that a virus particle is not alive and a viral lineage or infected cell is (close prior art, not an exact match: Forterre 2013/2017 give the virocell as the viral organism and separate it from the virion; Koonin & Starokadomskyy 2016 call the question itself "without substance" because the answer depends on an arbitrary definition, and place viruses on a selfishness–cooperativity continuum of replicators; Dupré & Guttinger 2016 treat viruses as living processes; Moreira & López-García 2009 take the opposite side, "strong evidence against the notion that viruses are alive"). The particle, infected-cell and lineage split here is Forterre's plus a lineage level, put on one ledger. Benner (2010) reports that the committee behind the NASA working definition used "system" so that entities such as "a cell, virus, or a single rabbit" can be alive without individually exemplifying life.
- **New in GTAO terms (labelled):** (1) the ledger: *the same three costs* that price a firm's memory price what an entity pays to be alive, and each can be paid by someone else (a restatement with a common currency, not a result); (2) one scale that puts virion, seed and tun together, and virocell, prophage and ERV together, by their ledger signatures (DERIVED, partly definitional); (3) K-V3 (HYPOTHESIS); (4) a tie to the spine: staying matched under the second law is paid by someone, and the virus is the case where the payer is the host.
- **What it does not do:** it does not settle "is X alive" as a yes-or-no (the point of the ledger is that the question has parts), and it does not predict that viruses exist, or any viral mechanism.

---

## 2. What counts as life, in the theory's terms

**Statement (RESTATEMENT with the ledger).** A thing is alive to the degree that it (U) runs free energy through itself to hold its structure, (F) copies and repairs its own record above the error threshold, and (T) keeps a selected response matched to a world that changes and can ruin it. Where it pays only some of these, the rest is carried by a host, a lineage or a population, and "alive" applies to the stage or the lineage that carries the part.

**Substrate-neutral, and what that costs (added after the independent review).** Nothing in U, F or T mentions chemistry. Read as a scale, the ledger therefore puts a firm (which pays upkeep, keeps records and tracks a market, with routines that are copied and selected), a computer-virus lineage or a self-copying program on the same scale as a cell. The NASA working definition avoids that with the word "chemical". So "alive" in the ledger's sense is not the same as biological life: biological life is the ledger plus a chemical substrate. This is a deliberate choice, made so the theory's costs apply across scales, and it is why the ledger is offered as a measurement scheme and not as the definition. One more edge case: a mule or a sterile worker ant pays U, F (repair) and T as an organism but carries no lineage of its own; the ledger calls it alive as an organism, while its lineage is its parents'.

**Prior art, and how this differs.**
- *Working definition.* Life as a "self-sustaining chemical system capable of Darwinian evolution" came from a NASA exobiology working group in the 1990s and was written up by Joyce in 1994; NASA calls it non-binding (NASA Science page; Benner 2010; Mix 2026 on the history). GTAO's F and T lines are the "Darwinian" part; U is the "self-sustaining" part.
- *Dynamic kinetic stability.* Pross (2011) extends Darwinian evolution to chemistry through the persistence of replicating populations by continual turnover. The theory's held class and Q4 (heredity) are this, already credited in BOOKENDS §2.1.
- *Autonomy and open-ended evolution.* Ruiz-Mirazo, Peretó & Moreno (2004) require a semi-permeable boundary, an energy-transduction apparatus and two kinds of functionally interdependent macromolecules (catalysts and records). That is a checklist for the same ledger; their "records" are F.
- *Whether any definition can be right.* Cleland & Chyba (2002) argue that "interminable controversy over the definition of life is inescapable" until a theory of living systems exists, as with water before molecular theory. GTAO is a candidate for that theory only if its bet holds. The ledger is offered as a measurement scheme, not as the definition.
- *Viability.* Kolchinsky & Wolpert (2018) are credited in the repo for semantic information, defined through viability, and nothing more.

**New:** the cost ledger as one scale, with kill conditions K-V1 to K-V4 and the lineage-versus-stage split. **No new testable content beyond K-V1 to K-V4 and N28** (the selected-model switch-on). The statement is a definition and is labelled RESTATEMENT.

---

## 3. Dark matter and dark energy

- **Dark matter: an input. DERIVED: nothing.** The theory takes the matter content as given. Planck's final results give a dark matter density Ω_c h² = 0.120 ± 0.001 and Ω_m = 0.315 ± 0.007 in base ΛCDM (Planck 2018 VI, abstract). Gravity acting on dark matter builds the cosmic web (`COSMIC_WEB.md`), which is where it matters here.
- **Dark energy: an input that sets the horizon.** With H₀ = 67.4 km/s/Mpc and Ω_Λ = 0.685 (the numbers `SCALE_ENDS.md` §4.5 uses), the de Sitter horizon caps the memory of anything in our causal patch at about 3.3×10¹²² nats and sets a floor of kT_dS ln 2 ≈ 2×10⁻⁵³ J on the price of erasing a bit (Gibbons & Hawking 1977, metadata only; the numbers are SCALE_ENDS §4.5's, not recomputed here). It also sets the top of LAT-1: no tracker extends past the event horizon.
- **Is any further consequence derivable?** **None.** The horizon cap, the erasure floor and the finite lifetime of any operating structure are already in the repo (SE13; Krauss & Starkman 2000 as credited in SCALE_ENDS §4.5). The theory neither explains why the cosmological constant has its value, nor what dark matter is, nor does it connect the two. Any claim that it does is withdrawn as framing (CLAIM_MAP N46).

---

## 4. Fractal time, stated exactly

What the repository establishes and what it does not, so the claim can be made accurately.

1. **It does not say that time is fractal.** The theory's claims are about the *spectrum of change of the world a system tracks*, not about the nature of physical time. "Time is fractal" as a framing is withdrawn (N46).
2. **Given the inputs, the best design is computed (in-model).** For a world with drift slope α, drift level q, sensing noise N, stakes and prices, the best read rate, memory time, forgetting kernel and number of stores follow from optimal filtering and approximation theory plus a price on effort (THEORY §0, §2.2). These are classical for a Gaussian world or for the best *linear* tracker in any world, and they are credited, not new. Which regime applies (α = 2, scale-free with measured α, or many modes) must be named before a number is stated (§2.5). So the answer to "does the theory say exactly how to design the optimal system" is: **yes inside the model, conditional on measuring five things and naming the regime; no as a statement about real systems, because that part is an untested bet** (CLAIM_MAP N13, J6 OPEN; no valid Tier-1 test has run).
3. **Fractal only where the world is.** T7 (`THEOREMS.md`: PROOF of three conditional propositions, FAILS as an unconditional claim; CLAIM_MAP K12, MATH-CORRECTED): the optimal architecture inherits the scale structure of the world. It is self-similar (geometrically spaced levels) *only if* the drift is scale-free, the costs are power laws in size and the loss has the same form at every level. Fixed setup costs break it; mean reversion, seasonality and regime lengths break it. The unconditional claim fails. The earlier "(log-span)^{2/3} number of levels" is withdrawn.
4. **The number of stores.** Away from α = 2, the number of separately timed memory stores grows like ln(span)·ln(stakes/upkeep); the rate is conjectural (numerically supported within about 10 to 25%) (K12, MATH-CORRECTED; THEORY §2.2 "Number of stores", K* ≈ (ln 8R/2π²)·ln(stakes/upkeep)). Whether strongly selected real systems carry about that many is part of the open empirical bet.
5. **Evidence on whether worlds are scale-free (DRIFT1, H20 OPEN).** The test measured event-rate distributions, not target drift q, so it does not meet MV2 for T7's condition. Results as measured: NYC 311 per-item request rates spread evenly over about 2.5 decades (SCALE_FREE after dequantization; about 4 decades for the 185 complaint types, post hoc) but its hourly series has a break near one day; Wikipedia articles have a characteristic edit rate (a single peak near one edit per 160 days) while the aggregate stream is a single 1/f^0.34 spectrum over 3.6 decades; SEC filings bunch at a regulated cadence with a broken spectrum. So some worlds look scale-free over a span and others do not, which is exactly what the conditional statement predicts.
6. **Why "layers of agents" are the best design for some classes of systems.** Where the world is scale-free over a span, geometric levels are optimal by T7b; where it has characteristic times, the levels sit at those times. Both are the same rule, "the architecture inherits the world's scale structure." That rule is PRIOR ART in substance (near-decomposability, Simon 1962, credited in THEORY §10).

---

## 5. The others, in two sentences each (details in the companion notes)

- **Cosmic web (`COSMIC_WEB.md`).** Published network measurements of the web show high clustering, a giant component from mean degree about 4, a degree spread broader than random positions give, no reported hubs (none tested for), and positive degree correlation; a plain proximity rule on random points reproduces much of that, and gravity adds the rest. The theory predicts that cost-shaped features (clustering, no hubs where delay is not priced) are shared with other spatial networks, and that model-shaped features (rewiring in response to a drifting environment) are absent from the web. The web is structurally like other networks and functionally unlike them.
- **Wormholes (`WORMHOLES.md`, CONDITIONAL throughout).** IF traversable wormholes existed, LAT-1's latency term would shrink: finite throats with a per-hop delay keep LAT-1 with a faster effective speed v_eff ≤ Λ/τ, and open throats remove the distance limit (§4b). What remains (throat capacity, drift correlation, price of telling versus looking, upkeep, and the chronology constraints that physics may impose) decides the architecture. In-model closed forms are checked in `reach_checks/wormhole_checks.py`.
- **Torus and cosmic topology (`TORUS.md`).** Torus = state space of two unlocked cycles (KNOWN); the theory's prediction about locking and the price of coupling is HYPOTHESIS and untested on real data. The theory makes no prediction about the shape of the universe (Planck 2018: spatial curvature Ω_K = 0.0007 ± 0.0019; Planck 2015: no compact topology below the size of the last-scattering surface).

---

## 6. Prediction register (all new rows; none changes an existing status)

| Row | Item | Label | Kill |
|---|---|---|---|
| N36 | The cost ledger and the virion / virocell / lineage verdict | PRIOR ART in substance (RESTATEMENT + DERIVED, partly definitional) | K-V1 |
| N37 | Lineage viability bound U_d ≲ ln R_max (S1 for viruses) | PRIOR ART | K-V2 |
| N38 | Lineage-side antigenic tracking tied to host immunity (K-V3) | OPEN (HYPOTHESIS) | K-V3 |
| N39 | Cosmic web tracks nothing; no adaptive design beyond gravity and baryonic physics acting on the initial field | PRIOR ART (consistent with published peak theory); negative prediction | `COSMIC_WEB.md` §6 |
| N40 | Hubness set by the price of delay relative to link cost; cosmic web no hubs reported (none tested for); organizations hubs | OPEN (HYPOTHESIS) | `COSMIC_WEB.md` §6 |
| N41 | Wormhole closed forms (pooling, partial sharing, coverage, tube-map speed); the case grouping is a checklist, not part of the label | PROVED (in-model), CONDITIONAL on traversable wormholes | `WORMHOLES.md` §7 |
| N42 | In ordinary networks with a latency shortcut, central pooling beats local reads iff d/c < 1 − 1/N at zero latency | OPEN (HYPOTHESIS; testable with real systems) | `WORMHOLES.md` §7 |
| N43 | Torus mathematics: Arnold tongues from phase coupling (width K/π, checked) | PRIOR ART | `TORUS.md` §6 |
| N44 | The earlier toy test of the torus idea (its staircase prediction failed in-toy; judged INVALID afterwards) | NOT EVIDENCE: INVALID as a test (coupling forces locking), not FAILED | `TORUS.md` §6 |
| N45 | Coupled loops: lock versus torus, coupling price | OPEN (HYPOTHESIS) | `TORUS.md` §4 |
| N46 | "GTAO predicts a torus universe, explains dark matter or energy, predicts wormholes exist, or says time is fractal" | WITHDRAWN (as framing) | n/a |

---

## 7. Left open (so the next reader does not have to guess)

- A prior-art sweep of immune-driven antigenic evolution (K-V3), and of delay-versus-link-cost network growth in organizations (N40).
- The prion threshold (K-V4).
- Measurement under the MV gates for K-V3 and N40 (inputs, mapping and power) before any prereg is locked; MV9's external timestamp still needs Chad's go.
- Real timing logs for N45.

---

## References (opened this session; "read" notes how much)

Virus and life
- Benner SA 2010, "Defining life," *Astrobiology* 10:1021–1030, doi 10.1089/ast.2010.0524 [abstract and PMC full text read]
- Bull JJ, Sanjuán R, Wilke CO 2007, "Theory of lethal mutagenesis for viruses," *J Virol* 81:2930, doi 10.1128/jvi.01624-06 [abstract read; not the full text]
- Cleland CE, Chyba CF 2002, "Defining 'life'," *Orig Life Evol Biosph* 32:387–393, doi 10.1023/a:1020503324273 [abstract]
- Drake JW 1991, "A constant rate of spontaneous mutation in DNA-based microbes," *PNAS* 88:7160–7164, doi 10.1073/pnas.88.16.7160 [abstract]
- Dupré J, Guttinger S 2016, "Viruses as living processes," *Stud Hist Philos Biol Biomed Sci* 59:109–116, doi 10.1016/j.shpsc.2016.02.010 [abstract]
- Eigen M 1971, *Naturwissenschaften* 58:465–523, doi 10.1007/bf00623322 [metadata only; credited in SCALE_ENDS]
- Erez Z et al. 2017, "Communication between viruses guides lysis–lysogeny decisions," *Nature* 541:488–493, doi 10.1038/nature21049 [abstract]
- Flores R, Gago-Zachert S, Serra P, Sanjuán R, Elena SF 2014, "Viroids: survivors from the RNA world?" *Annu Rev Microbiol* 68:395–414, doi 10.1146/annurev-micro-091313-103416 [abstract]
- Forterre P 2013 (online 2012), "The virocell concept and environmental microbiology," *ISME J* 7:233–236, doi 10.1038/ismej.2012.110 [metadata only]; Forterre P 2017, "Viruses in the 21st century: from the curiosity-driven discovery of giant viruses to new concepts and definition of life," *Clin Infect Dis* 65 (suppl 1):S74 [journal-page text read]
- Gago S, Elena SF, Flores R, Sanjuán R 2009, "Extremely high mutation rate of a hammerhead viroid," *Science* 323:1308, doi 10.1126/science.1169202 [abstract]
- Koonin EV, Starokadomskyy P 2016, "Are viruses alive? The replicator paradigm sheds decisive light on an old but misguided question," *Stud Hist Philos Biol Biomed Sci* 59:125–134, doi 10.1016/j.shpsc.2016.02.016 [abstract]
- Li J, Browning S, Mahal SP, Oelschlegel AM, Weissmann C 2010, "Darwinian evolution of prions in cell culture," *Science* 327:869–872, doi 10.1126/science.1183218 [abstract]
- McCutcheon JP, Moran NA 2012 (online 2011), "Extreme genome reduction in symbiotic bacteria," *Nat Rev Microbiol* 10:13–26, doi 10.1038/nrmicro2670 [abstract]
- Mix LJ 2026, "The origin, extension, and future of the 'NASA definition' of life," *Astrobiology* 26:66–74, doi 10.1177/15311074251412317 [title and abstract on the publisher page]; NASA Science, "Life on other planets: what is life and what does it need?" (non-binding working definition) [page read]
- Navarro B, Flores R 1997, "Chrysanthemum chlorotic mottle viroid: unusual structural properties of a subgroup of self-cleaving viroids with hammerhead ribozymes," *PNAS* 94:11262, doi 10.1073/pnas.94.21.11262 [abstract; added by the independent review]
- Moreira D, López-García P 2009, "Ten reasons to exclude viruses from the tree of life," *Nat Rev Microbiol* 7:306–311, doi 10.1038/nrmicro2108 [abstract]
- Pross A 2011, "Toward a general theory of evolution: extending Darwinian theory to inanimate matter," *J Syst Chem* 2:1, doi 10.1186/1759-2208-2-1 [metadata and abstract summary only]
- Raoult D et al. 2004, "The 1.2-megabase genome sequence of Mimivirus," *Science* 306:1344–1350, doi 10.1126/science.1101485 [abstract]
- Ruiz-Mirazo K, Peretó J, Moreno A 2004, "A universal definition of life: autonomy and open-ended evolution," *Orig Life Evol Biosph* 34:323–346, doi 10.1023/b:orig.0000016440.53346.dc [abstract]
- Sallon S et al. 2008, "Germination, genetics, and growth of an ancient date seed," *Science* 320:1464, doi 10.1126/science.1153600 [abstract]
- Sanjuán R, Nebot MR, Chirico N, Mansky LM, Belshaw R 2010, "Viral mutation rates," *J Virol* 84:9733–9748, doi 10.1128/jvi.00694-10 [abstract]
- Smith DJ et al. 2004, "Mapping the antigenic and genetic evolution of influenza virus," *Science* 305:371–376, doi 10.1126/science.1097211 [abstract]
- Stoye JP 2012, "Studies of endogenous retroviruses reveal a continuing evolutionary saga," *Nat Rev Microbiol* 10:395–406, doi 10.1038/nrmicro2783 [abstract]
- Tsujimoto M, Imura S, Kanda H 2016, "Recovery and reproduction of an Antarctic tardigrade retrieved from a moss sample frozen for over 30 years," *Cryobiology* 72:78–81, doi 10.1016/j.cryobiol.2015.12.003 [abstract]

Cosmology
- Gibbons GW, Hawking SW 1977, *Phys Rev D* 15:2738, doi 10.1103/physrevd.15.2738 [metadata only; credited in SCALE_ENDS]
- Planck Collaboration 2018, "Planck 2018 results. VI. Cosmological parameters," arXiv 1807.06209 [abstract; §7.3 and eq. 47 read]

Repository sources used: THEORY §0, §2.2, §2.3; `SCALE_ENDS.md` §3, §4.5, §5; `BOOKENDS.md` §2; `THEOREMS.md` T7, T9; `tests/BIO1`, `tests/COLLAPSE1`, `tests/DRIFT1`; CLAIM_MAP rows N25–N35, H16, H18, H20.
