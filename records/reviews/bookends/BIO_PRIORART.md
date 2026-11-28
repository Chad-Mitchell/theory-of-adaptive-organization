# Hostile review: theory/BOOKENDS.md (origin of life, biology, complex systems, prior art)

Reviewer: independent Grok Bot executor, Wednesday 18 Nov 2026, about 5:50–7:30 PM ET (America/New_York).
Object: branch `bookends`, commit 98b7168 (PR #86), cloned fresh into /tmp/rev-bio. Nothing pushed, commented or posted.
Cross-checked: THEORY.md §6 (lines 212–240), theory/SCALE_ENDS.md (§2 table, §3.3–3.4, SE4, IR-FIX10), measurement/CLAIM_MAP_v2.md (G13–G17, N1, N2), theory/MATH_ATTACK.md §3.4, litmap/LITMAP.md and litmap/PRIOR_ART.md.
Working files (Crossref / Semantic Scholar / Europe PMC dumps): <local>/gtao/reviews-bookends/bio_work/.

## Verdict: **PASS-WITH-FIXES**

The file is honest about status. Nothing is labelled field evidence. The theory is never called a law. It makes no claim that GTAO explains ants. The planetary-consciousness call is right in substance. The quotes I could check (Lenton 2018, Kolchinsky & Wolpert 2018, Pross 2011, Woelfle 2004) are accurate.

But the parts this file calls **new** are, in substance, mostly published. Some credit the repo's own litmap already holds is dropped. One source is misattributed (Pross). One "nothing published was found" statement is false (Doolittle 2014). The widened "feedback = model" class (2b) risks making "has a model" true of almost anything that is driven and persists. The file must not move into THEORY or SCALE_ENDS until findings 1–6 are fixed.

## Sources opened this session (what I actually saw)

- **Abstracts read:**
  - Lenton et al. 2018, TREE 33:633 (Semantic Scholar). The quotes in §2.5 match word for word.
  - Kolchinsky & Wolpert 2018, Interface Focus 8:20180041.
  - Pross 2011, J Syst Chem 2:1.
  - Vasas, Szathmáry & Santos 2010, PNAS 107:1470 (Europe PMC).
  - Vasas et al. 2012, *Biol Direct* 7:1, doi 10.1186/1745-6150-7-1.
  - England 2013, J Chem Phys 139:121923.
  - Perunov, Marsland & England 2016, PRX 6:021036.
  - Lee, Flack & Krakauer 2024, Proc R Soc B 291:20241606. The published title is "Constructing stability: optimal learning in noisy ecological niches".
  - Rubin, Parr, Da Costa & Friston 2020, *J R Soc Interface* 17:20200503, doi 10.1098/rsif.2020.0503.
  - Frank, Grinspoon & Walker 2022, *Int J Astrobiol* 21:47, doi 10.1017/S147355042100029X.
  - Di Paolo 2005, *Phenom Cogn Sci* 4:429, doi 10.1007/s11097-005-9002-y.
  - Woelfle et al. 2004, Curr Biol 14:1481 (Europe PMC).
  - Yi, Huang, Simon & Doyle 2000, *PNAS* 97:4649, doi 10.1073/pnas.97.9.4649.
  - Frank 1995, *Nature* 377:520, doi 10.1038/377520a0.
  - Huang, Isidori, Marconi, Mischiati, Sontag & Wonham 2018, IEEE CDC, doi 10.1109/CDC.2018.8619624.
  - Francis & Wonham 1976, Automatica 12:457 (abstract via ACM DL search snippet).
- **More than an abstract:**
  - Doolittle 2014 (online 2013), *Biol Philos* 29:415, doi 10.1007/s10539-013-9384-0. I read the Springer abstract page, including its footnotes.
  - Pross & Pascal 2013, Open Biol 3:120190, and Pross 2011, Entropy 13:518. I saw only search-result excerpts, which define DKS.
  - Wikipedia, "Good regulator theorem" (on the homomorphism caveat and Baez's critique).
  - Wonham 2018 IMP note (search excerpt only).
- **Title and metadata only (Crossref; not read):**
  - Hordijk, Hein & Steel 2010, *Entropy* 12:1733.
  - Bourrat 2014, *Biol Philos* 29:517, doi 10.1007/s10539-013-9383-1.
  - Ratnieks 1988, *Am Nat* 132:217, doi 10.1086/284846.
  - Lenton 1998, *Nature* 394:439, doi 10.1038/28792.
  - Kirchner 2003, *Climatic Change* 58:21.
  - Yachi & Loreau 1999, *PNAS* 96:1463.
  - Ostrom 1990, *Governing the Commons*, CUP.
  - Pross & Khodorkovsky 2004, *J Phys Org Chem* 17:312.
  - Gánti 2003, *Chemoton Theory*.
  - Smith & Morowitz 2016 (DOI resolves).
  - Conant & Ashby 1970 (DOI resolves).
- **Not opened:** Rosen 1985, Eigen 1971 full text, Kauffman 1986 full text, Beer, Simon 1962, Flack 2012/2017 (I relied on the litmap's own summaries for these).

## Findings

### 1. HIGH. A false "nothing published" claim; credit for persistence-as-selection is missing
- **Location:** §7 Q3 ("Nothing published was found here"), §2.5 "Is there any selection…", §2.7 S-axis.
- **Source:** Doolittle 2014, *Biol Philos* 29:415 (abstract read). Its argument: "differential survival of non-competing and non-reproducing individuals will also result in increasing frequencies of survival-promoting 'adaptations' among survivors, and thus is also a kind of natural selection", and "natural selection through survival could reconcile Gaia with evolutionary theory". The footnotes cite Bouchard 2008/2011 ("differential persistence"), Dawkins 1976 ("survival of the stable"), Okasha and Godfrey-Smith as critics, and Lenton 1998. Lenton et al. 2018's phrase "selection by survival alone" is Doolittle's. Bourrat 2014 is a direct reply (title only).
- **Problem:** Doolittle also predicts *accumulation* of persistence-enhancing traits in a single unit (n = 1). That is what BOOKENDS denies when it says a filter "finds *a* stable state, not the cheapest one". BOOKENDS asserts this without argument.
- **Fix:**
  - Credit Doolittle 2014 (and Bouchard, Bourrat) in §2.5, §5 and §7 Q3.
  - Reword Q3 as "Doolittle argues yes, qualitatively; no one has given it an Axiom-7 ε".
  - Label "filter ⇒ large ε" a HYPOTHESIS, not a derivation.

### 2. HIGH. Pross's dynamic kinetic stability is misattributed to non-hereditary chemistry
- **Location:** §2.1 G1 row ("PRIOR ART (… Pross 2011 …)"), §2.7 S-axis ("persistence filter only (Pross's dynamic kinetic stability…)"), §5.
- **Source:** Pross & Pascal 2013 and Pross 2011 (Entropy) say DKS is "applicable solely to persistent replicating systems" and characterizes "populations of replicators". The J Syst Chem 2011 abstract is about extending *Darwinian* theory via DKS.
- **Fix:**
  - Move Pross to G3, as a replicator-based stability selection.
  - Keep Pross's "one single physicochemical process" quote only as support for a graded onset.
  - Credit G1 instead to Prigogine, Kauffman / Hordijk–Steel RAF sets, Gánti's chemoton, and autopoiesis (Maturana & Varela; classic, not fetched).

### 3. HIGH. G2 / class 2b is less new than claimed and risks trivializing "model"
- **Location:** §2.1 G2 row ("DERIVED [BK, new]"), "What is new here is G2", §2.2 class 2b, §6 P2/P4.
- **Prior art in substance (credit missing):**
  - Still, Sivak, Bell & Crooks 2012 (in the litmap as GTAO's "physics anchor"). Driven systems with memory carry predictive information about their drive, and non-predictive memory costs dissipation.
  - England 2015 and Perunov, Marsland & England 2016 (PRX abstract read). "Self-organization into states formed through exceptionally reliable absorption and dissipation of work" from the drive. This is drive-matched structure with no heredity.
  - Di Paolo 2005 (abstract read). Adaptivity is "regulat[ing] themselves with respect to their conditions of viability" as a step beyond autopoiesis. This is, almost exactly, BOOKENDS's G1→G2 (K1→K2) line.
  - Kolchinsky & Wolpert, which BOOKENDS already credits.
- **Internal conflict:** litmap/LITMAP.md line 25 files dissipative adaptation as **CONTRADICTS** ("a rival physical route needs no prediction"). Under BOOKENDS's new definition the same systems become class 2b "models". The threat disappears by redefinition, and the file never says so.
- **Hostile case:** a dune shaped by the wind, a river meander or a hurricane (already listed) all persist only while matched to an outside drive. Their state correlates with it, so they would be K2 "models". That is the Aguilera et al. 2022 critique of the FEP (in the litmap's own THREATS) turned on GTAO.
- **Fix:**
  - Relabel G2 as "a synthesis of Still 2012, Kolchinsky & Wolpert 2018, Di Paolo 2005, and England 2015/Perunov 2016, mapped onto Theorem P". The only new part is the mapping.
  - Add an explicit non-model kill to class 2b: a drive-matched structure whose persistence does *not* drop under the K&W scrambling intervention at fixed influx is K1, not K2.
  - Add a THREATS entry that reconciles the litmap's dissipative-adaptation row.
  - Keep hurricanes, dunes and Daisyworld listed as *candidates only*.

### 4. HIGH. "Feedback is the simplest model": right in spirit, but the sharper published criterion is missing
- **Location:** §2.2, §0 item 3, §6 P7.
- **Sources:**
  - Francis & Wonham 1976 (abstract): robust regulation must "incorporate in the feedback path a suitably reduplicated model of the dynamic structure of the disturbance and reference signals".
  - Yi et al. 2000 (abstract): bacterial chemotaxis achieves robust perfect adaptation through integral feedback, and "integral control in some form is necessary".
  - Huang et al. 2018 (CDC tutorial on the IMP in biology).
  - Conant & Ashby: the model is only a homomorphism, and critics say the proof does not support the title (Wikipedia, citing Baez 2016).
- **Problem:** "What the feedback is about" is not enough. Under the IMP, plain proportional feedback has no internal model of the outside world. It leaves a steady error. *Integral* feedback is the minimal internal model, of a constant/step exosystem. That is exactly "tomorrow will be like now".
- **Fix:**
  - State the rung as "error feedback containing the exosystem's modes (an integrator for a constant world) is the simplest model", crediting the IMP.
  - Note that pure proportional feedback counts as a model only in the weak mutual-information sense (I(M;X_t) > 0).
  - Cite Yi et al. 2000 as the cellular instance.
  - Also note that Rosen's definition, which BOOKENDS does not cite but the litmap does, counts "a predictive model of itself and/or its environment". The "self-feedback is not a model" line is therefore a GTAO definitional choice and should say so.
  - Settle the ladder ordering (see finding 7).

### 5. MEDIUM–HIGH. Layers and governance credit is dropped, including credit THEORY §6 itself gives
- **Location:** §3 items 2 and 6–7, §5, §3 "Where it reaches down".
- **Sources:**
  - Ostrom 1990/2010. THEORY §6 credits Ostrom and the litmap says "commons need rules"; BOOKENDS never names Ostrom.
  - Flack 2012/2017 "slow variables". The litmap says this "ANTICIPATES … the *origin* of levels", which is BOOKENDS's "a level is a shared model of a common driver". BOOKENDS credits Flack only through LFK 2024.
  - Frank 1995 (abstract read). Self-restraint is insufficient; "mutual policing and enforcement of reproductive fairness are also required", from replicators forming the first cells through to insect and human societies. This is published prior art for §3 items 6–7 *and* for the sub-cellular "first level = compartment" in §3.
  - Ratnieks 1988 worker policing (title only).
  - The under-watching factor √(Λ_i/Λ_whole) is the standard externality / public-goods result in this cost form. Credit the public-goods literature (Olson 1965, Ostrom).
- **Fix:**
  - Add Ostrom, Flack, Frank 1995 and Ratnieks to §3 and §5.
  - Label the claim "enforcement appears where shared memory is a public good" as PRIOR ART qualitatively. GTAO's own contribution is the scaling form only.
  - Small cross-doc error: THEORY §6 cites MATH_ATTACK "§3.5" for under-watching, but the result is in §3.4 (BOOKENDS is right).

### 6. MEDIUM. The planet section misses the closest rival and the technosphere
- **Location:** §2.5, §2.7 "Earth system K2 at planet scale", §4 Planet row, §0 item 7.
- **Sources:**
  - Rubin, Parr, Da Costa & Friston 2020 (abstract read) formalize Gaia as a Markov blanket whose internal states are "actively inferring external states", calling it "planetary autopoiesis". This is the FEP's specific planetary claim. BOOKENDS mentions the FEP only in general terms.
  - Frank, Grinspoon & Walker 2022 define "planetary intelligence" as "the acquisition and application of collective knowledge operating at a planetary scale".
- **Problem:** with humans, Earth already has lead-time forecasting (climate models, asteroid tracking). Under BOOKENDS's own axes, that is K3 at planet scale now, not K2. This bears directly on Chad's "survive human extinction" question.
- **Consciousness call:** labelling GTAO-based consciousness claims IMPOSTER is the right call. GTAO has no variable for experience. But the sentence "by those measures planetary regulation sits low" will be heard as a "no". Say plainly that (I_pred, k, ε) are not measures of consciousness.
- **Fix:**
  - Cite both papers.
  - Change the Earth row to "K2 (pre-technological); K3 components since the technosphere".
  - Keep IMPOSTER only for the claim "GTAO shows a planet is or is not conscious", and say "out of scope" for the question itself.

### 7. MEDIUM. Two orderings of the ladder contradict each other
- **Location:** §2.1 (acting ahead is G4, last, after heredity) vs §2.2 last bullet and §1 (constant, then clock, then react: the timer/clock rung sits *below* reacting).
- **Fix:** say explicitly that §2.2 orders rungs by cost and §2.1 by a hypothesized history. Mark the historical order HYPOTHESIS: anticipation without heredity, such as a phase-leading entrained oscillator, is not excluded and is H2's very conjecture.

### 8. MEDIUM. Vasas 2010 is over-generalized
- **Location:** §2.1 G3 row, §2.7 autocatalytic row ("filter").
- **Source:** the 2010 abstract concerns GARD-type "compositional genomes / composomes". Vasas et al. 2012 (same group, with Kauffman) found that networks with multiple "viable cores" in compartments give "limited heredity and selectability", "a poor man's natural selection … prior to genetic templates".
- **Fix:** cite Vasas 2012. Change "cumulative design needs template heredity" to "*strong* cumulative design needs template heredity; limited pre-template selection is possible (Vasas 2012)". Mark the autocatalytic row S = "filter to weak cumulative (OPEN)".

### 9. MEDIUM. The per-level table: several tests are weak, possibly circular, or already known
- **Chemistry (BK-G2):**
  - The test is concrete and can fail. But a BZ-type oscillator does not *die* when out of phase with its feed, so "persistence time" is undefined for the flagship example.
  - A flow-reactor autocatalytic system with washout risk would work, but that is replication in Pross's sense, which blurs G2 and G3.
  - Fix: name a non-replicating system whose ruin is phase-dependent, or call the test design-OPEN.
  - The N28 kill ("energy-limited at existence margin") is not operational.
- **Cell (O5 tiers):**
  - It is already textbook that DNA, chromatin, mRNA and protein modifications turn over at increasing rates. Unless the "drift of what each tier holds" is measured *independently of the tier's own lifetime*, the test passes by construction.
  - Fix: specify an independent drift measure in the prereg.
- **Organism (H4):** this must be positioned against the existing repetition-suppression vs expectation literature (Summerfield & Egner 2009 TICS, title only). The H80/C13(c) "public sensor traces" test names no organism or system.
- **Colony:** both listed tests come from software or firms (J9 is packages per maintainer). Use THEORY N2's own ant-species-by-patchiness test, or relabel the row.
- **Firm:** "contract length rises with volatility" has a transaction-cost literature. Do a literature check before calling it a GTAO prediction.
- **Civilization (LAT-1):** spacecraft autonomy versus light delay is engineered on purpose, so a pass there is weak (confirmation by design). Weight geo-distributed firms instead.
- **Planet (microcosm):**
  - The test is concrete and can fail, but "communities that lower drift" are self-selected.
  - Fix: manipulate drift externally (buffered vs fluctuating medium, evolved replicate lines) and predict lower investment in sensing.
  - Note that loss of unused regulation and anticipation under relaxed selection is already known (Mitchell et al. 2009, in the litmap), so a pass is weak.
- **Star, galaxy, black hole, cosmos:** no tests, as the file admits. Say in the plain-words section that the bookend rows are *classifications, not predictions*.

### 10. MEDIUM-LOW. The frozen-memory roles are fine, but the genome is not frozen
- **Location:** §2.3 roles 1–2.
- **Problem:** "Covalent bonds … keeping cost 0" and "genome … copied rather than tracked" misstate the genome. DNA needs continuous energy-paid repair within a lifetime and is updated by selection across generations, so it is *held* with low upkeep, not frozen (textbook; no citation fetched). Roles 1 and 4 are also the same T8 argument stated twice.
- **Fix:** merge roles 1 and 4. Call the genome "near-frozen: low upkeep (repair), updated only across generations".
- **Credit:** credit Crick's "frozen accident" (classic, not fetched) for heredity as freezing. Optionally check Pattee on rate-independent constraints (not verified here).

### 11. LOW–MEDIUM. Daisyworld's coupling comes from lower-level selection
- **Location:** §2.5 correction paragraph, §6 P2 examples.
- **Problem:** Daisyworld's regulation arises from differential growth of heritable daisy types, which is organism-level selection. Doolittle 2014's footnote 3 argues the same for real Gaian traits, and Lenton 1998 is titled "Gaia and natural selection" (title only). So it is not a clean "unselected" 2b case.
- **Fix:** say "unselected *at planet scale*; the coupling is a by-product of selection within the biosphere". Note the Kirchner 2003 critique (title only).

### 12. LOW–MEDIUM. The spine's "only physical principle" claim is overstated
- **Location:** §1, first paragraph ("the only physical principle this picture leans on").
- **Problem:** §3 item 8 and §4 use the light-speed limit, §2.3 uses GR/Bekenstein, and G3 uses Eigen's chemistry kinetics.
- **Fix:** "the main principle; signal speed and known physics enter as inputs".

### 13. LOW–MEDIUM. Kill criteria are rewritten before any test
- **Location:** §6 P4 (SE4's "holds a model … without heredity" kill becomes an expected class).
- **Assessment:** this is legitimate, since SCALE_ENDS IR-FIX10 had already flagged S1/S2 as near-definitional. But it is driven by an argument, not data.
- **Fix:** log it as a pre-data revision with that rationale, and make sure the replacement kill (P4's "semantic information without a flux") is as sharp as the one it replaces.

### 14. LOW. Smaller items
- England 2013 is a replication bound, so it belongs at G3, not "G1/G3".
- LFK 2024: "outsourced memory" is the preprint's wording, and the published abstract says "niche destructors evolve" when resources are shared. Cite the published title.
- The biosphere pooling argument (§2.5) is the portfolio / insurance effect. Credit Yachi & Loreau 1999 (title only).
- "Fast local repair (re-diversification)" takes millions of years after mass extinctions, so "fast" is relative and should say relative to what.
- Rosen 1985 (the litmap says it "ANTICIPATES 'judgment = acting ahead' by 41 years"), Sterling 2012 (allostasis), and Mitchell 2009 / Tagkopoulos 2008 (microbial anticipation) are all in the litmap but missing from §5 and §2.1 G4.

### 15. PASS. Ants
BOOKENDS never mentions ants or claims ant evidence. CLAIM_MAP G13–G14 (NOT EVIDENCE) and G15–G17 (SIM-FAIL) stand untouched.

Caution for THEORY §6's illustration ("as with ants on a trail they themselves follow" = "privately rewarded"): workers are mostly sterile. Their "private reward" is colony-level inclusive fitness, so ants fit the theory's *other* branch: Λ_i ≈ Λ_whole through relatedness. Social insects also *do* show enforcement (worker policing: Ratnieks 1988; Frank 1995). Reword the example so that a chat or video line saying "ants show no one needs to be in charge" doesn't overstate it.

## What must happen before anything moves into the canonical files
Fix 1–6 (credit, the Pross misattribution, the false "nothing published", the 2b non-model kill, IMP wording, the planetary rivals). Then rerun an independent math check of the G2 mapping (§7 Q1). The verdict becomes PASS once those are done and findings 7–9 are reflected in the table.

---

## Round 2 (revision 2, head 49bd64cb4871c55cf8828fd0f29fe34858031f0a; DISPOSITION.md read)

Reviewer: same, Wed 18 Nov 2026, about 6:10–7:00 PM ET. Fresh `git fetch` and checkout in /tmp/rev-bio. Nothing pushed, commented or posted.

### Verdict: **PASS-WITH-FIXES (minor)**

All 15 round-1 findings are fixed or acceptably deferred. Every new citation I checked is accurate. Revision 2 is much stronger: the four notions of knowing (§2.0.2), the IMP-based model tier, the restored credit and honest CLASSIFICATION labels.

Five new issues remain (R2-1 to R2-5 below). Two of them make BK-P3 and BK-P4 unsafe to apply as written. The other proposals are safe on the biology and prior-art side, either now or after small edits (table at the end).

### Round-1 findings, re-checked

| # | Status | Evidence in rev 2 |
|---|---|---|
| 1 Doolittle / "nothing published" | FIXED | §2.5 row, §2.7 S-axis, §7.3. The quote matches the Springer page. Filter ⇒ large ε is now HYPOTHESIS. |
| 2 Pross | FIXED | Moved to Q4, "for replicators". Q1 credits Prigogine, Kauffman, Hordijk–Hein–Steel, Gánti and autopoiesis. |
| 3 G2 novelty / non-model kill / litmap | FIXED | Q2 is "synthesis, not new in substance". BK-SEM kill added. Class 2b withdrawn. §5 says plainly that the threat stands; BK-P12. |
| 4 IMP / Yi / Rosen | FIXED | §2.0.2, §2.2. Proportional feedback holds no model; integral feedback is minimal; Rosen is flagged as a definitional choice. (One nit at R2-L2.) |
| 5 Governance credit | FIXED | §3.2 Flack; §3.6–3.7 Ostrom, Frank 1995, Ratnieks; qualitative claim marked PRIOR ART; §3.4 cross-ref flagged. (Substance issue at R2-2.) |
| 6 Planet rivals / technosphere | FIXED | Rubin 2020 is credited as a rival and FGW 2022 is cited. Technosphere is K3. Consciousness is out of scope, and IMPOSTER is limited to "GTAO shows". |
| 7 Ladder orders | FIXED | §2.2 item 6 separates the cost order from the structure order. |
| 8 Vasas 2012 | FIXED | Q4; the S-axis reads "filter to weak cumulative (OPEN)". |
| 9 Weak tests | FIXED, with acceptable deferrals | O5 independent-drift condition, microcosm with external drift, LAT-1 weighting, ants on N2, CLASSIFICATION rows. The H4 and transaction-cost literature checks are deferred and openly marked OPEN, which is acceptable. (New BK-G2 issue at R2-4.) |
| 10 Genome near-frozen; merge roles | FIXED | §2.3 |
| 11 Daisyworld lower-level selection | FIXED | Leaving Kirchner 2003 uncited is acceptable under the no-invented-citations rule. |
| 12 Spine | FIXED | §0.1, §1 |
| 13 Kill rewrite logged | FIXED as logged, but see R2-5 |
| 14 Small items | FIXED | England 2013 moved to Q4; LFK published title; Yachi & Loreau; "fast" made relative; Rosen, Sterling, Mitchell and Tagkopoulos in §5. |
| 15 Ants | FIXED | BK-P10 flags THEORY §6's example. Still no ant-evidence claim; CM G13–G17 untouched. |

### New citations, spot-checked against Crossref metadata and the abstract or page

All of these check out: DOI, authors, venue, volume and pages match, and every quoted phrase appears in the source.
- Doolittle 2014, Biol Philos 29:415–423: the quote matches the page.
- Rubin, Parr, Da Costa & Friston 2020, JRSI 17:20200503: the summary of internal, external, active and sensory states matches the abstract.
- Frank, Grinspoon & Walker 2022, Int J Astrobiol 21:47–61: "to a planet" appears in the abstract.
- Vasas et al. 2012, Biol Direct 7:1: "limited heredity and selectability" appears in the abstract.
- Di Paolo 2005, PCS 4:429–452: the quote is exact.
- Yachi & Loreau 1999, PNAS 96:1463–1468: "many species provide greater guarantees that some will maintain functioning even if others fail" is exact (Europe PMC abstract).
- Frank 1995, Nature 377:520–522: the quotes are exact.
- Francis & Wonham 1976, Automatica 12:457–465.
- Yi, Huang, Simon & Doyle 2000, PNAS 97:4649–4653: "integral control … necessary" matches.

Two caveats:
- **Ratnieks 1988** (Am Nat 132:217–236): title, venue and pages are correct. Crossref lists no author, so "Ratnieks FLW" comes from general knowledge (it is correct). More important: the author marks the source "metadata only" yet states its content (§4 colony row: "policing intensity rises as relatedness falls"). See R2-L1.
- Also confirmed accurate: Walker, Hays & Kasting 1981 (JGR 86:9776); Lilly et al. 2013 (ApJ 772:119); Petrov, Ouyang & Swinney 1997 (Nature 388:655); Caldeira & Kasting 1992 (Nature 360:721); Sana et al. 2012 (Science 337:444); Mitchell et al. 2009; Tagkopoulos et al. 2008; Hordijk, Hein & Steel 2010.

### New findings (round 2)

**R2-1. MEDIUM. A "model" with no stakes (carbonate–silicate cycle).**
- **Location:** §2.5 abiotic row, §2.7 Earth row ("K2 candidate"), BK-P2, BK-P3.
- **Problem:**
  - The file's own ruin column says the cycle's regulated variable, habitability, "matters only to life". The cycle itself is not ruined if it fails.
  - So under the spine in §1 ("Know" means staying matched to a world that can kill *you*), the cycle is not a knower. Yet under §2.0.2's purely structural IMP test it would be a K2 "model".
  - Revision 2 has decoupled "model" from the entity's persistence. That reopens a small version of the round-1 trivialization: abiotic mass-balance integrators, such as carbonate compensation, would be models too.
- **Physics note:** the cycle is integral-like only to the extent that weathering depends on temperature alone. Its known direct pCO₂ and runoff dependences give imperfect adaptation, so "integrator-like" is defensible but it is a degree, not a yes/no.
- **Fix:**
  - Add a clause to the K2 definition: "a structural model *of the entity's own ruin variable*". Otherwise call it a **regulator without stakes**: IMP structure, but outside GTAO's knowing.
  - Reword BK-P2's example and the §2.7 Earth row to match.

**R2-2. MEDIUM. "Shared fate needs no one in charge" contradicts the source cited for it.**
- **Location:** §3.7, §1 ("the colony's success is their success"), BK-P10.
- **Source:** Frank 1995's abstract says "Self-restraint, which evolves according to the kin-selection coefficient of relatedness, is **not sufficient**: mutual policing and enforcement … are also required".
- **Problem:**
  - Relatedness gives Λ_i ≈ r·Λ_whole with r < 1, not Λ_i ≈ Λ_whole.
  - Worker policing in Hymenoptera arises exactly where relatedness asymmetries make fate *not* fully shared.
- **Fix:**
  - Write Λ_i ≈ r·Λ_whole.
  - State that shared fate is usually partial, and that Frank's model says it is insufficient on its own for higher-level units.
  - In §1, say "some ants, bees and wasps police". Worker policing is best documented in bees and wasps and is not universal in ants.
  - Change BK-P10's wording to "sterile workers *partly* share the colony's fate (relatedness), and workers also police".

**R2-3. MEDIUM. BK-IMP's behavioural test does not identify integral feedback.**
- **Location:** §2.0.2 BK-IMP, §2.2 kill for hurricanes, flames, dunes and galaxies; §4 chemistry row.
- **Source:** Ma, Trusina, El-Samad, Lim & Tang 2009, *Cell* 138:760–773, doi 10.1016/j.cell.2009.06.013 (abstract read). Searching all three-node topologies, "only two major core topologies" achieve adaptation: "a negative feedback loop with a buffering node and an **incoherent feedforward loop** with a proportioner node".
- **Problem:** "Returns to its prior value after a step" can therefore be passed by feedforward circuits that are not error-feedback internal models.
- **Credit missing:** Barkai & Leibler 1997, *Nature* 387:913, doi 10.1038/43199 (metadata only), the original robustness result that Yi et al. explain; and Briat, Gupta & Khammash 2016, *Cell Syst* 2:133, doi 10.1016/j.cels.2016.02.010 (metadata only), antithetic integral feedback.
- **Fix:**
  - BK-IMP needs (a) perfect adaptation that is *robust to parameter perturbation*, which IFFLs generally lack, and (b) a structural check that the integrated quantity is the error.
  - Cite Ma 2009, and add Barkai & Leibler as prior art.

**R2-4. MEDIUM. BK-G2's treatment arm supplies the information from outside.**
- **Location:** §2.1, arm (T).
- **Problem:**
  - In arm T, the *experimenter's* light pulses keep the oscillator in phase with the reagent pulses. A T > S result then shows only that experimenter-imposed alignment helps, which is engineered in.
  - It does not show that the droplet's *own* state carries survival-relevant information, which is what Kolchinsky & Wolpert's intervention is meant to test.
- **Fix:**
  - Let the droplet entrain to the reagent pulses chemically (natural coupling, arm T).
  - Use light pulses only to *scramble* that phase (arm S), against a dose-matched sham light pulse at the entrained phase.
  - Keep arm C.

**R2-5. LOW–MEDIUM. BK-P4 removes the heredity kill without replacing it.**
- **Problem:**
  - The two new kills are both about flux. Nothing now tests the surviving claim, CM-N28 as BK-P5 rewords it: "*selected* models switch on only with heredity".
  - IR-FIX10 found the old clause near-definitional *under the Axiom-7 reading*. Under the new response/action split it can be made non-definitional.
- **Fix:** add kill (iii): "a non-hereditary structure whose design sits measurably nearer a GTAO optimum than unselected controls (design prediction met without heredity or learning)".

**Low items.**
- **R2-L1.** Ratnieks's content is stated from metadata only. Mark it "content per textbook kin-selection theory; source not read", or open the paper.
- **R2-L2.** §2.0.2: under Rosen's definition the reason a star fails is "acts on no prediction". Its "proportional restoring force" is irrelevant to Rosen, so drop that clause.
- **R2-L3.** The IMP's necessity result is for *asymptotic, structurally stable* regulation. Saying "proportional feedback holds no model" is fine in IMP terms, but note that high-gain proportional loops approximate adaptation. That is why BK-IMP must test robustness (see R2-3).

### Are BK-P1 to BK-P14 safe to apply? (biology and prior-art view; defer to PHYSICS on P6, P7 and P11)

| Proposal | Judgement |
|---|---|
| BK-P1, BK-P5, BK-P8, BK-P12, BK-P14 | **Safe now** |
| BK-P9 | Safe; Chad's call |
| BK-P6 | Safe on the bio side; physics content defers to PHYSICS |
| BK-P7, BK-P11 | No bio objection; PHYSICS decides |
| BK-P2 | **Safe after R2-1**: relabel the carbonate–silicate example "regulator without stakes / IMP candidate" |
| BK-P10 | **Safe after R2-2**: say "partly share", add Frank's insufficiency caveat |
| BK-P13 | **Safe after R2-1 and R2-3**: make BK-c's "abiotic integrator candidate" and BK-IMP's test definition match |
| BK-P3 | **NOT safe yet**: as worded, a structural model alone admits abiotic stake-free integrators into class 3 ("held model", "cells and every level above"). Needs the R2-1 clause. |
| BK-P4 | **NOT safe yet**: needs kill (iii) (R2-5) |

**Required before canonical application:** R2-1, R2-2 and R2-5 (wording), and R2-3 (test definition). R2-4 is required before BK-G2 is preregistered, not before the text is applied. Once these are done the verdict becomes PASS. No further round is needed if the edits are made as stated.
