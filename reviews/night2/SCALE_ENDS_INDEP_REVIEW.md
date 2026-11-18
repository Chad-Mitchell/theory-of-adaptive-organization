# SCALE_ENDS_INDEP_REVIEW: independent hostile referee (physics and mathematics) of PR #80, `theory/SCALE_ENDS.md`

Wednesday 18 November 2026, about 12:28 PM to 1:20 PM ET (America/New_York). QUEUE SCALE-ENDS-INDEP-REVIEW, out of cycle and unscored (ledger 195 claim, 196 outcome). Private. Nothing was posted, sent or made public.

**Independence.** This referee is a fresh Grok Bot executor launched by Ace. It wrote none of `theory/SCALE_ENDS.md`, `theory/SCALE_ENDS_SUMMARY_FOR_CHAD.md`, `theory/scale_ends_checks/`, or the self-review `reviews/night2/SCALE_ENDS_REVIEW.md` (which its own author disclosed as not independent). All numbers below come from new code in `reviews/night2/SCALE_ENDS_INDEP_checks/` (`physics_indep.py`, `band_indep.py`, outputs `.out` beside them), which does not import or copy the author's scripts. It uses a different route: Planck units, Page's per-species greybody coefficients (Page 2005, *New J Phys* 7:203, eqs 19–21, PDF read), numerical integration, the Saha equation, and exact fBm sampling.

**Read in full:** SCALE_ENDS.md (branch head 1bd2dd7), the plain summary, both check scripts and outputs, the self-review and its checks; THEORY.md v1.4.17 (status block, §0, §2.3 including the t1908 open disagreement at line 126, §2.5, §3 freeze-or-hold row, Theorem G); `reviews/night1/formal/THEOREMS.md` Theorem 8; `measurement/FRAMEWORK.md` §1.2 item 4, MV1–MV10, §3.11; `measurement/CLAIM_MAP_v2.md` statuses and section N.

**Scope (Chad, t1927, binding).** The three costs apply from atoms to the cosmos, and the theory should say what black holes are. Scope was not re-litigated here. Truth was.

## Verdict: PASS-WITH-FIXES

Every published number checks out. One headline lifetime is a non-physical bracket edge, and one ionization figure is mislabelled. Two load-bearing arguments are wrong as written, and both can be repaired without changing the bottom line:
1. **The atomic "state entropy ≈ 10⁻¹⁷¹ nats" argument (self-review's E3(d)) is false.** An atom carries real information about its surroundings.
2. **"Black hole = frozen corner via Theorem 8 with c → ∞" is a misapplication.** In Theorem 8, c → ∞ selects *lookup*, not freeze. And if c is priced as energy per bit (GTAO's own β_phys convention), a black hole is the *cheapest* read there is, so the band does not close at all. The conclusion survives only through GTAO's lateness term, which the budget does count. That makes the derivation *native* to GTAO, but it has to be stated that way.

The three-class split and LAT-1 are prior art in substance and must be credited. Fixes IR-FIX1 to IR-FIX12 below are applied on the branch as separate commits. With them, §9 (the THEORY §2.3 bullet and rows N25–N29) is supported in amended form.

## 1. Numbers, re-derived independently

| Item | SCALE_ENDS | Independent value (`physics_indep.out`) | Verdict |
|---|---|---|---|
| H ionization factor, 300 K | E_b/kT = 526, 10^−228.5 | 525.99, 10^−228.4 | OK as a **Boltzmann factor** |
| H ionization, 5,800 K | 27.2, 10^−11.8 | 27.21, 10^−11.8 Boltzmann. The **Saha** ionized fraction at n = 10²³ m⁻³ is **1.3×10⁻⁴** (10^−114.4 at 300 K, 1 bar) | **IR-FIX5**: "ionization odds / ruin factor" must be labelled a Boltzmann factor. The equilibrium fraction differs by about 10⁸ at 5,800 K, because of the free electron's phase space |
| Atom's state entropy | "≈ 4e^{−395} ≈ 10^−171 nats" | n = 2 *occupancy* 10^−170.7. Electronic-excitation *entropy* ≈ 10^−168.1 nats. **Hyperfine spin entropy ln 4 = 1.386 nats**, even at 2.7 K. Translational entropy ≈ 13.1 nats (300 K, 1 bar) | **IR-FIX1 (major)** |
| Information an atom carries about its surroundings | "cannot carry information about its surroundings" | One atom's speed carries **0.079 nats** about whether the bath is at 300 K or 600 K. Its electron spin carries 6×10⁻⁷ nats about B ∈ {0, 1 T} at 300 K. Small, but > 0 | **IR-FIX1**: false as stated. Atoms are passive sensors, which is why they make thermometers, magnetometers and clocks, and why the 21-cm line exists |
| Landauer floor | 2.9×10⁻²¹ J = 0.018 eV | 2.871×10⁻²¹ J = 0.01792 eV | OK |
| Proton Bekenstein capacity | 36 bits | 25.12 nats = 36.24 bits | OK |
| Eigen threshold | εL < ln σ | L_max = ln σ/ε: 230 at ε = 10⁻², σ = 10; 2.3×10⁴ at 10⁻⁴ | OK (KNOWN) |
| Bacterial E_gen | 10¹¹–10¹² kT | 1.4×10¹¹ to 6.3×10¹¹ kT (0.9–2.7×10¹⁰ ATP × 40–60 kJ/mol at 310 K) | OK. Lynch & Marinov's coefficient was not re-read by this referee (DOI and abstract verified) |
| T_H, S (1 M☉) | 6.17×10⁻⁸ K; 1.05×10⁷⁷ nats | 6.170×10⁻⁸ K; 1.049×10⁷⁷ nats (1.513×10⁷⁷ bits) | OK |
| 2kT_H per nat; Bekenstein saturated | stated | Mc²/(kT_H S) = 2.000000; dE/(T dS) = 1.000000; 2πR E/(ħc) at R = r_s equals S_BH exactly | OK |
| **Evaporation time** | "10⁶⁶–10⁶⁷ yr × (M/M☉)³"; 2.1×10⁶⁷ (photons only), 2.2×10⁶⁶ (Page) | Naive photon blackbody, no greybody: 2.096×10⁶⁷. **Photons + gravitons with greybody factors: 1.159×10⁶⁷ yr** (α = 3.7474×10⁻⁵, Page 2005 eq 19). Page 1976 two massless ν: 2.159×10⁶⁶. Three massless ν: 1.535×10⁶⁶ | **IR-FIX4**: kT_H reaches 0.05 eV only at 1.1×10⁻¹⁰ M☉. A solar-mass hole therefore emits no neutrinos until the last ~10⁻³⁰ of its life. The physical value is **≈ 1.2×10⁶⁷ yr × (M/M☉)³**. The 2.2×10⁶⁶ figure is a historical massless-neutrino case, and 2.1×10⁶⁷ has no greybody factors. Ignoring CMB absorption, which delays the start by ~3×10¹¹ yr |
| Page time | 0.538 t_ev | γ + graviton: S_rad/\|dS_BH\| = 1.4848, Page time **0.5381** t_ev. With massless ν: 0.5155–0.5140. The half-entropy-radiated point is 0.6464 | OK. The 0.538 value belongs to the γ + graviton case, so it matches 1.16×10⁶⁷ yr, **not** the 2.2×10⁶⁶ bracket (IR-FIX4) |
| Scrambling time | 3.5 ms; 4.9 h | 3.494 ms; 4.89 h | OK |
| 1 kg BH bits | 3.827×10¹⁶ | 3.827×10¹⁶ (Lloyd 2000 PDF line 511: "3.827 × 10¹⁶ bits") | OK |
| Horizon entropy | 3.3×10¹²² nats | 3π/(Λℓ_p²) = 3.307×10¹²² (H₀ 67.4, Ω_Λ 0.685); 3.263×10¹²² (67.66, 0.6889) | OK. "~3×10¹²²" is robust |
| T_dS, price per bit | 2.2×10⁻³⁰ K; 2×10⁻⁵³ J | 2.198×10⁻³⁰ K; 2.10×10⁻⁵³ J | OK |
| Hawking read bandwidth (new) | — | Emitted entropy rate for 1 M☉ (γ + graviton) ≈ **284 nats/s**, against a 10⁷⁷-nat store | Used in IR-FIX3 |
| L_max formula | c(D\*/q)^{1/(α−1)} | fBm, exact Cholesky, 3,000 paths: MSE vs ℓ slopes 0.502, 1.002, 1.498 for α = 1.5, 2, 2.5 (predicted 0.5, 1, 1.5). MSE(ℓ = 0.4) within 0.5% of qℓ^{α−1}. A linear extrapolator at α = 2.5 cuts the penalty by 20% | OK (hold-last-value), as SCALE_ENDS states |

Ledger and stamps (minor): the author's file header and ledger entry 194 carry times later than their commits (header "to 1:30 PM", entry 194 "12:45", both before 12:38 PM). They are left as written and noted here.

## 2. The key logical step: does "black hole = limit of the frozen corner" follow?

**What Theorem 8 actually says** (`reviews/night1/formal/THEOREMS.md`). It compares hold, min_T[c/T + WqT/2] + h, with freeze (the corner T = H_l) and lookup (μu). As c → ∞, q_f = 2c/(WH_l²) → ∞, so freeze beats *interior holding*. But freezing costs at least c/H_l, which exceeds μu, so the **optimum is lookup** at every drift, including q → 0 (`band_indep.out` A). SCALE_ENDS §4.2 item 3 half-says this ("even freezing loses to direct lookup"). Yet §1's "key point" ("the frozen corner is where the optimum goes as … read cost goes to ∞"), §0 item 3 and the "Succeeds" bullet present c → ∞ as putting the black hole *in* the frozen corner. **That is wrong.** Theorem 8 puts an infinitely costly store beyond the lookup edge: nobody uses it.

**What does put it in the frozen class.** E1 (no selected action, the Axiom-7 reading), E2 (blind-viable: nothing outside threatens it on any relevant time) and E4 (lifetime set by its own leak) apply to the black hole *as a persisting structure*: h = 0, R\* = 0. The word "limit" (most memory per size, lowest energy per nat for its size, longest leak lifetime per mass) comes from **physics** (Bekenstein saturation, H_l ∝ M³), not from GTAO. So the defensible statement has two parts. As a structure, a black hole is the extreme member of the frozen class. As memory for anyone else, it sits beyond the lookup edge.

**Is "read cost = information-return time" reasonable, and what breaks if read cost is defined differently?**
- *Energy pricing (the β_phys convention, FRAMEWORK §3.11).* A Hawking quantum costs about kT_H ≈ 8.5×10⁻³¹ J per nat for 1 M☉, by far the cheapest read in nature. With c that small, Theorem 8's band is **wide open** (`band_indep.out` B: modes reached are freeze and hold). **Under energy-only pricing the conclusion fails.**
- *Time pricing (lateness).* THEORY §0 counts lateness inside prediction error. A read that is ℓ old adds W·q·ℓ^{α−1} to the error, and reading more often cannot remove it (§5 of SCALE_ENDS, confirmed above). Lookup then wins once q > (μu − h)/(Wℓ^{α−1}) (`band_indep.out` C; the analytic and numeric edges agree).
  - For a young hole, Page (1993) puts the return of infallen information at the Page time, ~6×10⁶⁶ yr for 1 M☉.
  - For an old hole, Hayden–Preskill's return after t\* is available only to a collector that has gathered essentially all earlier radiation, emitted over at least the Page time, and can decode it (Harlow–Hayden: conjectured exponential). The cost moves into collection and decoding, but the collector must still have been present for ≥ t_Page.
  - Bandwidth is ~3×10² nats/s.
  - **So the mapping is reasonable, and it is GTAO's own:** lateness, not a per-read c. It must be stated through the lateness term, and the derivation labelled conditional on it.
- *A third definition: read cost as the number of readable degrees of freedom.* (M, J, Q) are cheap and timely to read (orbits, ringdown), and astronomers do read them as a frozen record of accretion. The black hole is a usable frozen store of **three numbers**, and an unusable store of the other ~10⁷⁷ nats. SCALE_ENDS says this; it should keep saying it.

**Conclusion on the step.** With IR-FIX2 and IR-FIX3, "a black hole is the extreme of the frozen class, and unusable as anyone's memory" follows from E1, E2 and E4 plus the lateness term, given published physics. It is a **derived classification, conditional on two mappings**: the Axiom-7 reading of "action", and lateness ≥ the Page time. It is not a derivation of black-hole physics. SCALE_ENDS §0 item 4 and SE11 already say the latter correctly.

## 3. Switch-on conditions and the three classes: circularity and analogy creep

- **S1/S2 overlap (circularity, moderate; IR-FIX10).** Under R-FIX4, an "action" is an alternative over which selection operates. Then S2 (a world-dependent action) already presupposes selection, and with it the heredity of S1. "Models switch on only with selection" is therefore close to definitional. The non-circular content is S3 (drift inside the hold band, with Woelfle et al. 2004 and Kussell & Leibler 2005 as qualitative support), S4 (the energy inequality) and Eigen's quantitative threshold. §3.4 and §6b now say so. The fix SCALE_ENDS already proposes (an operational pre-data test for a *selected* response, e.g. heritable variation in the response map) is the right one, and it stays open.
- **SE4's kill is decided by definitions.** Candidate challenge: periodically forced, entrained chemical oscillators (a textbook phenomenon, not cited here). They hold phase information about an external drive, with a flux and without heredity. Whether that is a "model" depends on whether they have stakes and an action, so it is again E1. SE4's kill ("a structure that holds a model without heredity") is not testable until "action" is defined before data. That is noted, not fatal.
- **Stars as class 2 (no analogy creep found).** This rests on a non-definitional fact: a main-sequence star's ruin hazard does not depend on any external drifting variable it could respond to (E2 relative to externals), and h = L is measurable. That is fine. "Thermostat" (H80's tier) is an analogy for self-regulation through negative heat capacity. It is labelled as a tier, not as a model, which is acceptable.
- **Atoms (analogy and definition creep; IR-FIX1).** After the E3(d) withdrawal, the atom case rests on E2 (non-definitional) plus E1 under the Axiom-7 reading (definitional). That is honest only if stated, and it is now stated.

## 4. Prior-art sweeps (IR-FIX8)

**Three-class split (frozen / held structure / held model).** Not new in substance; credit required:
- Prigogine's equilibrium structures (crystals) vs dissipative structures (Nobel lecture 1977; *Science* 1978, already cited).
- Pross's thermodynamic stability vs dynamic kinetic stability of replicators (Pross 2011, *J Syst Chem* 2:1, doi 10.1186/1759-2208-2-1).
- **Kolchinsky & Wolpert 2018**, "Semantic information, autonomous agency and non-equilibrium statistical physics," *Interface Focus* 8:20180041, doi 10.1098/rsfs.2018.0041 (abstract read). It defines the value of a system's information about its environment by its causal necessity for the system's continued existence, explicitly for "a rock, a hurricane, a bacterium." That is close prior art for E1/E2's viability-based value of information and for the three classes.
- Friston, Da Costa, Sakthivadivel, Heins, Pavliotis, Ramstead & Parr 2023, "Path integrals, particular kinds, and strange things," *Phys Life Rev* 47:35–62, doi 10.1016/j.plrev.2023.08.016 (arXiv 2210.12761 abstract read). It sorts particles into conservative vs dissipative, inert vs active, and ordinary vs strange. It is a **rival** at the atomic end: the free-energy-principle reading grants inference-like dynamics to broad classes of particles, whereas GTAO's E1/E2 give R\* = 0 where nothing is selected. The two disagree in wording and not testably as stated. The difference should be stated.
- Krakauer, Bertschinger, Olbrich, Flack & Ay 2020, "The information theory of individuality," *Theory Biosci* 139:209–223, doi 10.1007/s12064-020-00313-7 (abstract read). Organismal, colonial and driven individuality, measured by information propagated from past to future. Their "driven" form, dependent on environmental input, is a neighbor of class 2.
- England 2013, Kauffman 1986 and Smolin are already cited.

**Light-delay federation limit (LAT-1).** The elementary bound is not new in substance; credit:
- Simon 1962, "The architecture of complexity," *Proc Am Philos Soc* 106:467–482 (near-decomposability: fast local and slow global dynamics; PDF text seen via search).
- Flack 2017, "Coarse-graining as a downward causation mechanism," *Phil Trans R Soc A* 375:20160338, doi 10.1098/rsta.2016.0338 (slow variables at higher levels).
- Abadi 2012, "Consistency tradeoffs in modern distributed database system design," *Computer* 45(2):37–42, doi 10.1109/MC.2012.33 (PACELC: latency vs consistency under geo-replication).
- Bailis et al. 2012 (PBS, already cited).
- Tatikonda & Mitter 2004, "Control under communication constraints," *IEEE TAC* 49:1056–1068, doi 10.1109/TAC.2004.831187.
- Lloyd 2000 (PDF read: communication time vs flip time, t_com/t_flip; computation "highly serial" at the black-hole limit).
- Olson 2022, "A causal limit to communication within an expanding cosmological civilization," arXiv 2208.07871 (horizon limits on a cosmological-scale civilization's internal signalling).
- No published statement of L_max = c(D\*/q)^{1/(α−1)} in exactly this form was found in this sweep. The form is elementary, and **novelty is not claimed** (as SCALE_ENDS already says).
- Krakauer: beyond the individuality paper and Flack 2017, no Krakauer paper on relativistic coordination limits was found.

**'t Hooft 1993** was fetched: arXiv gr-qc/9310026, "Dimensional reduction in quantum gravity" (essay for Abdus Salam). Abstract: observable degrees of freedom are "Boolean variables defined on a two-dimensional lattice." The reference is corrected from "not fetched" (IR-FIX9).

## 5. Citations

All 42 DOIs in SCALE_ENDS.md were resolved through Crossref this session, and author, journal, volume, pages and year match. That includes the five DOIs containing parentheses (Harlow–Hayden, Penington, Almheiri et al., Kauffman 1986, Margolus–Levitin), which were checked URL-encoded. The new DOIs (Page 2005, Kolchinsky–Wolpert, Krakauer et al., Abadi, Pross, Tatikonda–Mitter, Flack, Friston et al.) also resolve.

Content spot-checks against primary text:
- Page 1976 abstract (2×10⁻⁴; 81/17/2%).
- Page 2013 abstract (53.81%; 1.4847).
- Page 2005 eqs 19–21 (PDF).
- Egan & Lineweaver 2010 (2.6 ± 0.3×10¹²² k; 3.1 (+3.0, −1.7)×10¹⁰⁴ k; the "not yet been capped … life can exist" quote, PDF lines 43–46).
- Smolin 2004 §6.3 quote (PDF lines 1309–1314; the paraphrase is fair: the heavy star would refute Bethe–Brown and thereby CNS).
- Krauss & Starkman 2000 ("Statistically all alarm clocks eventually fail").
- Lloyd 2000 (3.827×10¹⁶ bits; serial at the BH limit).
- Rosenband 2008 (α̇/α = (−1.6 ± 2.3)×10⁻¹⁷ /yr, Europe PMC abstract).
- 't Hooft 1993 (fetched).

Not re-read by this referee: the Lynch & Marinov coefficient, Fonseca/Romani/Isi abstract numbers beyond their DOI metadata, and Woelfle's results. These are well-known values, and the self-review read them. **No miscitation was found.**

## 6. The two video lines

- **Opening, as drafted:** "An atom never has to guess. Physics holds it together for free, so a model would cost something and buy nothing. The bill for knowing comes due only when a changing world can ruin you."
  - "Never has to guess" and "cost something and buy nothing": accurate (E1 + E2).
  - "Holds it together for free": accurate for a ground state (h = 0).
  - **"The bill … comes due only when …" is inaccurate.** It implies the cost appears only then, which contradicts SCALE_ENDS's own point (and Chad's) that the costs are present at every scale. It also drops the second condition, a move that depends on the world (E1).
  - **Accurate replacement:** "An atom never has to guess. Physics holds it together for free, and nothing it could do would change its fate. So a model would cost it something and buy it nothing. Knowing starts to pay only when a changing world can ruin you, and you have a move to make."
- **Closing, as drafted:** "At the far end is the black hole: the most memory the universe allows, almost none of it readable. It remembers everything that fell in and predicts nothing. Everything that has to keep up lives in between."
  - **"The most memory the universe allows"** is wrong as worded. The holographic bound is per region (the cosmic horizon holds more), so it should be "for its size."
  - **"Remembers everything that fell in"** assumes unitarity. That is the mainstream view, supported by Page-curve calculations, but it is not settled, so soften it to "keeps a scrambled record."
  - "Almost none of it readable" and "predicts nothing": accurate (three numbers readable now; E1 + E2).
  - **Accurate replacement:** "At the far end is the black hole: the most memory physics allows in a space that size, and almost none of it readable. Three numbers show on the outside. The rest comes back scrambled, over some ten-to-the-sixty-seven years. It keeps a record of what fell in, and predicts nothing. Everything that has to keep up lives in between."

## 7. Fixes (all applied on `q-scale-ends` as separate commits, marked [IR-FIXn] in the text)

| Fix | Severity | Change |
|---|---|---|
| IR-FIX1 | major | Withdraw the atomic E3(d) application ("≈ 10⁻¹⁷¹ nats; cannot carry information about its surroundings"). Atoms carry real information (hyperfine ln 4 nats; 0.08 nats of temperature information in one atom's speed). They are passive sensors (E3(c)). The atom case rests on E2 + E1 (Axiom-7 reading), stated as partly definitional. §0.2, §2 E3, §3.2, SE5, §10 and the summary are updated |
| IR-FIX2 | major | Theorem 8's c → ∞ selects lookup, not freeze. Fix §1's key point, §0.3, §4.2 item 3 and the "Succeeds" bullet. Frozen-class membership comes from E1, E2 and E4. Theorem 8 says the hole is beyond every tracker's lookup edge |
| IR-FIX3 | major | Route the read cost through the lateness term (THEORY §0), not c. State that energy pricing alone opens the band (cheapest read in nature), and that time closes it (Page-time latency, collection plus decoding for old holes, ~3×10² nats/s). SE10 becomes conditional on two mappings |
| IR-FIX4 | moderate | Physical lifetime ≈ 1.16×10⁶⁷ yr × (M/M☉)³ (γ + graviton, greybody). The 2.2×10⁶⁶ and 2.1×10⁶⁷ figures are labelled as the massless-ν and no-greybody cases. Page time 0.538 is tied to γ + graviton |
| IR-FIX5 | minor | Ionization numbers are Boltzmann factors. Saha fractions are added (10⁻¹¹⁴ at 300 K; 10⁻⁴ at photosphere conditions) |
| IR-FIX6 | minor | SE10 "h ≤ 0" → "h = 0" (consistent with R-FIX6) |
| IR-FIX7 | moderate | "Most memory / lowest energy per bit" must say "for its size" (summary, video) |
| IR-FIX8 | moderate | Prior art: the three-class split (Prigogine; Pross 2011; Kolchinsky & Wolpert 2018; Friston et al. 2023 as rival; Krakauer et al. 2020), and LAT-1 (Simon 1962; Flack 2017; Abadi 2012; Tatikonda & Mitter 2004; Lloyd 2000; Olson 2022). SE4 relabelled "PRIOR ART in substance" |
| IR-FIX9 | minor | 't Hooft 1993 fetched; reference corrected. New references added with DOIs |
| IR-FIX10 | moderate | Note S1/S2 circularity under the Axiom-7 reading. The non-circular content is S3, S4 and Eigen. SE4's kill is decided by the definition of "action" |
| IR-FIX11 | minor | §0.6: "the Landauer floor never prevents the switch-on" is a HYPOTHESIS. Derived only for the bacterial numbers under the premises |
| IR-FIX12 | minor | Summary and video lines replaced with the accurate versions in §6. Labels in the summary are tightened |

**§9 decision.** Supported in amended form. The THEORY §2.3 bullet is applied as v1.4.18, without "Theorem 8 with c → ∞". It names the lateness mapping, the ≈ 10⁶⁷ yr lifetime and the prior art. CLAIM_MAP v2.39 adds rows N25–N29 with statuses from the v2 list:
- N25: SE1, SE2 (+ SE5 application), PROVED (in-model)
- N26: SE10, PROVED (in-model), conditional on two mappings; nothing about nature beyond the physics it assumes
- N27: LAT-1, OPEN
- N28: SE7, OPEN
- N29: SE11 + §7 imposters, WITHDRAWN (as framing)

Not applied (outside this repository): re-labelling H1 in `HYPOTHESES_CORE_v2_reviewed.md`, which lives in Ace's working folder.

## 8. Plain-language summary for the video script (each claim tagged)

1. The three costs exist at every scale: keeping a memory, being wrong or late, and paying to look. Erasing a bit costs at least kT ln 2. That is about 3×10⁻²¹ J at room temperature, and an experiment has come close to it. **[prior art: Landauer 1961; Bérut et al. 2012]**
2. An atom doesn't keep a model. Not because a model would be free, but because nothing threatens it (at room temperature thermal ionization is suppressed by a factor of 10⁻²²⁸) and it has no move to make. A model would cost something and buy nothing. **[derived: E1 + E2, given Boltzmann/Saha physics; E1 rests on defining an "action" as something selection acts on]**
3. Atoms do carry a little information about their surroundings. That is why they make thermometers, magnetometers and clocks. But that is physics, not a model. **[prior art: statistical physics; derived label]**
4. Stars burn fuel to persist, but they track nothing outside themselves: held, but with no model. **[derived classification; prior art in substance: Prigogine's dissipative structures]**
5. Models are worth having only when four things line up: copying good enough to keep what works (Eigen's limit), a move whose payoff depends on the world, a world that changes at a trackable pace, and a first bit worth its price. For a bacterium the energy floor is nowhere near binding: a division costs about 10¹¹–10¹² kT. **[hypothesis, with stated kill; Eigen is prior art]**
6. A black hole holds the most information physics allows in a region its size, at the lowest energy per bit for that size. It pays nothing to stay a black hole, and it leaks away over about 10⁶⁷ years × (mass in suns)³. **[prior art: Bekenstein, Hawking, Page]**
7. In the theory's terms, a black hole is the extreme of the frozen class. As anyone's memory, it is useless: three numbers are readable now, and the rest comes back scrambled only after ~10⁶⁷ years. Any tracker would look at the world instead. It records the past and predicts nothing. **[derived classification, given published physics, conditional on counting lateness as error and on the definition of "action"]**
8. The theory does not explain why black holes exist, the area law, or the Page curve. Saying it does would be false. **[stated limit]**
9. At the top, the cosmic horizon caps memory near 3×10¹²² nats and sets a permanent floor price of about 2×10⁻⁵³ J per bit. **[prior art: Gibbons & Hawking 1977; Egan & Lineweaver 2010]**
10. Light delay means a structure L across can centrally track only what changes slowly compared with L/c, so big systems must federate. The formula is elementary and testable on Earth (spacecraft, geo-distributed firms and databases). **[derived bound; hypothesis for real systems; prior art in substance: Simon 1962, PACELC]**
11. Smolin's idea that universes reproduce through black holes is the one published place where selection acts at cosmic scale. Heavy neutron stars put it under pressure, and the theory adds no new test of it. **[prior art, credited]**

## References added by this review (Crossref-resolved this session unless noted)

- Abadi D 2012, *Computer* 45(2):37–42, doi 10.1109/MC.2012.33
- Flack JC 2017, *Phil Trans R Soc A* 375:20160338, doi 10.1098/rsta.2016.0338
- Friston K et al. 2023, *Phys Life Rev* 47:35–62, doi 10.1016/j.plrev.2023.08.016 [arXiv 2210.12761 abstract read]
- Kolchinsky A, Wolpert DH 2018, *Interface Focus* 8:20180041, doi 10.1098/rsfs.2018.0041 [abstract read]
- Krakauer D, Bertschinger N, Olbrich E, Flack JC, Ay N 2020, *Theory Biosci* 139:209–223, doi 10.1007/s12064-020-00313-7 [abstract read]
- Olson SJ 2022, arXiv 2208.07871 [arXiv API record read]
- Page DN 2005, "Hawking radiation and black hole thermodynamics," *New J Phys* 7:203, doi 10.1088/1367-2630/7/1/203 [arXiv hep-th/0409024 PDF read, eqs 19–21]
- Pross A 2011, *J Syst Chem* 2:1, doi 10.1186/1759-2208-2-1
- Simon HA 1962, *Proc Am Philos Soc* 106(6):467–482 [no DOI; journal PDF text seen via search]
- Tatikonda S, Mitter S 2004, *IEEE Trans Autom Control* 49:1056–1068, doi 10.1109/TAC.2004.831187
- 't Hooft G 1993, "Dimensional reduction in quantum gravity," arXiv gr-qc/9310026 [fetched]
