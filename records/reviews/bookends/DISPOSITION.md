# DISPOSITION: reviews of PR #86 (theory/BOOKENDS.md), revision 2

Date: Wed 18 Nov 2026, ~9 PM ET. Branch `bookends`, commit 49bd64c (PR #86). Section numbers are revision 2's.

Key:
- **A** = accepted and done.
- **A-partial** = accepted; part of it is deferred, with the reason.
- **R** = rejected, with the reason.

## MATH_LOGIC (FAIL, fixable)

| # | Sev | Finding | Disp. | Where and how |
|---|---|---|---|---|
| 1 | BLOCKER | "Action" used in two meanings | A | §2.0.1: response (physical, enough for GT-P0/P1) vs action (Axiom 7; needed for "pays", "optimal", design predictions). Used consistently throughout. |
| 2 | BLOCKER | "Model" redefined so the conclusion is automatic; flames and hurricanes became models; l.43 and l.166 contradiction | A | §2.0.2: four notions (correlation, semantic, IMP-structural, selected). Mapping lemma (§2.0.3) states that a Theorem-P floor does not imply a model. BK-SEM and BK-IMP kills; flames, dunes, hurricanes and galaxies expected K1 (§2.2). Class "2b" withdrawn. Both contradictions removed. |
| 3 | MAJOR | Need a finite-horizon corollary, or drop the "persists" test | A | §2.0.3: Azuma bound P(blind survives to T) ≤ exp(−(δT−B)²/(2b²T)), with a Monte Carlo check in `theory/bookends_checks/finite_horizon.{py,out}`. Markov mixing form marked OPEN. |
| 4 | MAJOR | G2 mapping does not fit P's hypotheses (y depends on X, A only via M, A4 omitted) | A | §2.0.3 mapping lemma: M declared, A = π(M), ℓ′ = ℓ − (y(x) − ȳ) bounded, D recomputed for ℓ′, and A1, A2, A4 and A5 each checked with failure conditions. |
| 5 | MAJOR | "K ≥ K2 requires held" contradicts SE-E3(c) | A | §2.7: only held memory beyond the instantaneous correlation (K2 integrator, K3 clock or model) needs upkeep. K0 and K1 do not. |
| 6 | MAJOR | N28 and THEORY l.128 contradiction | A | §2.1: "N28 stands as written" withdrawn; N28 needs a wording change and stays OPEN. BK-P5 rewords THEORY §2.3 and N28 together ("*Selected* models … "). |
| 7 | MAJOR | Biosphere case used the wrong pooling rule | A | §2.5: relabelled ANALOGY + PRIOR ART (Yachi & Loreau insurance). C2 failure stated; redundancy result listed OPEN (§7.7). |
| 8 | MAJOR | Onset sequence not derived; "pays"; realized k vs k_max | A | §0.4 and §2.1: HYPOTHESIS, partial order only (entrained oscillators can act ahead without heredity). "Viable" vs "pays" separated; realized k used, with k_max only as the ceiling. |
| 9 | MAJOR | "Shared fate" dropped; J9 turned into a consequence | A | §3.7: "shared fate or enforcement"; "Hypothesis:"; J9 OPEN; the shared-memory reading tagged [BK, new]. |
| 10 | MINOR | Ladder order vs K axis; "frozen" senses | A | §2.2 items 6–7: two orders (cost vs structure and lead); three named senses of "frozen". |
| 11 | MINOR | R1 is not "exactly" feedback | A | §2.2 item 4: at most analogous in the limit of frequent reads; cost class assigned separately. |
| 12 | MINOR | Labels (Theorem P, K12, E6) | A | GT-P labels quoted as PROOF; K12 "rate conjectural" added in §3.4; E6 identification withdrawn (§3.7). |
| 13 | MINOR | ID collisions | A | File-prefixed IDs (SE-, GT-, IM-, CM-, TH-); proposals renamed BK-P1…BK-P14. |
| 14 | MINOR | "Two places" should be three | A | §0.9 now lists three inconsistencies, including T7(iii). |
| — | note | P1 and P8 approved; P2–P5 and P7 blocked; P6 incomplete; P9 inherits finding 2 | A | P1 and P8 kept unchanged. P2–P5 and P7 rewritten. P6 and P7 now cover N25 and N26 under both readings (§2.0.4). P9 uses the corrected spine. P12–P14 are new. |
| — | nit | pytest INTERNALERROR (sys.exit on import) | A-partial | Listed in BK-P14. Not fixed in this PR: the tooling is outside the brief's scope. |

## PHYSICS (PASS-WITH-FIXES)

| # | Sev | Finding | Disp. | Where and how |
|---|---|---|---|---|
| F1 | MAJOR | Define K2 by K&W semantic info; I_pred > 0 is not sufficient | A | §2.0.2: semantic info is its own tier (K1s), and the model tier is IMP-structural. Done both ways, per the convergent request. |
| F2 | MAJOR | Daisyworld information lives in the daisies; name the entity and its ruin variable | A | §2.5 table opens with entity and ruin variable; selected at daisy level, unselected at planet scale. |
| F3 | MAJOR | Galaxies are a gas regulator (Lilly 2013); not an MV7 case | A | §2.2, §2.4, §2.7, §4: K1 (leaky integrator), OPEN; removed from calibration (BK-P11). |
| F4 | MAJOR | Abiotic carbonate–silicate component | A | §2.5 row: integrator-like candidate structural model without selection, OPEN (Walker, Hays & Kasting 1981). |
| F5 | MAJOR | Black-hole read delay: Hayden–Preskill, colder than CMB, unitarity; narrow N26 (ii) | A | §2.0.4 and BK-P7. |
| F6 | MAJOR | The second law is not the "only" principle | A | §0.1, §1, BK-P9: backbone plus gravity, c and the low-entropy start; "no new physics". |
| F7 | MODERATE | Entropy comparisons and attribution | A | §2.3: S_obs, S_CEH and S_CEH,int with error bars (E&L abstract opened); "most entropy now present is in SMBHs"; holographic-bound wording; the gap is not free energy. |
| F8 | MODERATE | Landauer vs measurement; Still's scope; Landauer before the cell | A | §2.7 floors; BK-P11; §4 chemistry row: OPEN. |
| F9 | MODERATE | Stars: binaries, throughput, plain line | A | §2.4 (Sana 2012); "h = L" and "ruin fixed by own mass" withdrawn; §1 plain core-thermostat line. |
| F10 | MODERATE | Hurricanes are transient and die when their world changes | A | Moved out of "Burn" as a steady burner in §1. Transient; outside GT-P's long-run statement (§2.7). |
| F11 | MODERATE | Redesign BK-G2 | A | §2.1: pulsed reagent, phase-resetting vs sham pulses, rhythmless matched-mean control, defined ruin, preregistered effect size; labelled a test of the mapping in a designed system; design OPEN. |
| F12 | MODERATE | Biosphere as ANALOGY; ρ≈1 end | A | §2.5. |
| F13 | MINOR | Heat-death ordering; Krauss–Starkman; hibernation | A | §1 and the §4 cosmos row. |
| F14 | MINOR | Gravity guarantees only that the densest store is unreadable | A | §7.4. |
| F15 | MINOR | Light delay binds only off-planet | A | §1, §3.8, §4. |
| F16 | MINOR | Vasas 2012 | A | §2.1 Q4, §5, refs (abstract opened). |
| F17 | NIT | Lifetime value; neutrinos; E&L uncertainty; K&W viability wording | A | §2.3, §2.0.2. |

## BIO_PRIORART (PASS-WITH-FIXES)

| # | Sev | Finding | Disp. | Where and how |
|---|---|---|---|---|
| 1 | HIGH | Doolittle 2014 makes "nothing published" false; filter ⇒ large ε is a hypothesis | A | §2.5 (Doolittle page read; quoted), §7.3. Bouchard and Bourrat credited as named via Doolittle and BIO, not opened. |
| 2 | HIGH | Pross applies to replicators; credit G1 properly | A | §2.1: Pross and England 2013 moved to Q4. Q1 credits Prigogine, Kauffman, Hordijk–Hein–Steel, Gánti and autopoiesis. |
| 3 | HIGH | G2 is a synthesis; add a non-model kill; litmap conflict; dunes and hurricanes candidates only | A | §2.1 Q2 "synthesis, not new in substance"; BK-SEM kill; §5 conflict acknowledged; BK-P12 THREATS entry (proposed, not applied: the brief forbids editing canonical files). |
| 4 | HIGH | IMP wording; Yi 2000; Rosen | A | §2.0.2, §2.2 (Yi abstract opened; Rosen definitional choice). |
| 5 | MED-HIGH | Ostrom, Flack, Frank 1995, Ratnieks; qualitative claim is PRIOR ART; §3.5→§3.4 | A | §3.2, §3.6–3.7, BK-P10. Ratnieks: Crossref metadata only. |
| 6 | MEDIUM | Rubin 2020; FGW 2022; technosphere K3; consciousness out of scope | A | §2.5 (both abstracts opened); §0.7. |
| 7 | MEDIUM | Two ladder orders | A | §2.2 item 6. |
| 8 | MEDIUM | Vasas 2012; autocatalytic S = filter → weak cumulative (OPEN) | A | §2.1, §2.7 table. |
| 9 | MEDIUM | Weak per-level tests | A-partial | Bookend rows marked CLASSIFICATION; O5 needs an independent drift measure; H4 must be positioned against the repetition-suppression literature; ants use THEORY N2's test; firm contracts need a transaction-cost check; LAT-1 spacecraft down-weighted; microcosm manipulates drift externally, with Mitchell 2009 named as making a pass weak; chemistry Landauer and IMP marked OPEN. **Deferred:** actually doing the H4 and transaction-cost literature reviews, and naming a natural non-replicating system with phase-dependent ruin (none known; the design is marked OPEN). Reason: these need new literature work outside this revision. |
| 10 | MED-LOW | Genome near-frozen with repair; merge roles 1 and 4; Crick | A | §2.3: three roles; Crick credited as a classic, not fetched. |
| 11 | — | Daisyworld coupling from lower-level selection; Kirchner 2003 | A-partial | Lower-level selection: done (§2.5). **Kirchner 2003 not cited:** not opened by this author, and not in litmap with a DOI (no-invented-citations rule). |
| 12 | — | Spine overstatement | A | Same as PHYSICS F6. |
| 13 | — | P4 kill rewrite to be logged as a pre-data revision | A | BK-P4 logged with its reason; two kills, each at least as sharp as the old one. |
| 14 | — | England 2013 to G3; LFK published title and wording; Yachi & Loreau; "fast" repair is relative; Rosen, Sterling, Mitchell, Tagkopoulos in §5 and G4 | A | Done (§2.1, §2.3, §2.5, §3.6, §5; LFK title via Crossref). |
| 15 | PASS | Ants OK; caution on THEORY §6's ant example | A | §3.7 flag + BK-P10. |

## Rejections
Nothing was rejected outright. Partial deferrals are listed above:
- BIO 9: the literature reviews are deferred;
- BIO 11: Kirchner 2003 is uncited because no source was opened;
- BIO 3 and BK-P12: the THREATS entry is proposed, not applied;
- MATH nit: the pytest fix is proposed, not applied.

## Checks run
- `python3 tools/check_consistency.py` → PASS (FAIL 0).
- `python3 tools/test_check_consistency.py` → PASS (8 planted errors caught).
- Scratch run with `theory/BOOKENDS.md` added to MAINTAINED (copy in `tools/`, deleted) → PASS; 158 N-refs, 0 mismatches.

---

# Round 2 disposition (revision 3, commit 341a4ed; Wed 18 Nov 2026, evening ET)

All Round 2 items are accepted and fixed. Nothing is rejected. The proposals BK-P1…BK-P14, as amended, are applied to the canonical files in the same PR (per Ace's instruction; theory decisions delegated by Chad at t1927).

| Review | Item | Fix (BOOKENDS section / canonical file) |
|---|---|---|
| MATH | R2-1 | §2.0.3: conditional mean ≤ −δ given the past (supermartingale); "evidence" sentence placed under that condition; τ_mix caveat with the reviewer's counterexample; Markov form OPEN. CLAIM_MAP N33 carries the caveat. |
| MATH | R2-2 | Class 2 = "no structural model (self-regulation or proportional/drive-slaved response)"; class-3 condition reads "a *response* with world-dependent payoff"; class 3s = selected (SCALE_ENDS §2). |
| MATH | R2-3 | N26 PROVED (in-model) scope = pre-Page-time holes; post-Page holes outside it, conditional on Harlow–Hayden (CLAIM_MAP N26, THEORY §2.3 and status block, SCALE_ENDS §0.3/§4.2/SE10, BRIEF, README). |
| MATH | R2-4 | N25 note: "expected 0 (physical argument, not computed)". |
| MATH | R2-5 | §1 hurricane wording. |
| MATH | R2-6 | Λ_i ≈ r·Λ_whole; under-watching ≈ √r (§3.7, THEORY §6). |
| MATH | R2-7 + nits | Clock described as "IMP-like"; D_ℓ′ = D_ℓ exactly; same time index; H8 and J9 prefixed. |
| PHYS | R2-1 | BK-G2: natural chemical entrainment; dose-matched light in the phase-insensitive window (T) vs random-phase light (S); C; light-alone check (L); Arnold-tongue and phase-response premises (Petrov 1997; Lin et al. 2004); not preregistered. |
| PHYS | R2-2 | Hurricane wording. |
| PHYS | R2-3 | Lan 2012 and Cao 2015 as the basis for "K2 and K3 need throughput"; Lan cited in SE4 kill (ii). |
| PHYS | R2-4 | §0.4 and Q5 hedged ("may", untested, BK-G2). |
| PHYS | R2-5 | Carbonate–silicate scope (a)–(c); now a regulator without stakes. |
| PHYS | R2-6 | Lilly condition added; "K1 per the regulator model; observational test not defined". |
| PHYS | R2-7 | Yachi & Loreau "extended by analogy"; the paleontology claim carries Chen & Benton 2012 (metadata only) and is not carried into canonical files. |
| PHYS | proposal edits | P2 (galaxy candidate; class 3 may be unselected, 3s split), P4 (kill (i) "no flux, not merely vanishing"; Lan for (ii)), P6, P9 (+ quantum physics), P11 (Still scope), P13 (G2 row). |
| BIO | R2-1 | K2 requires a model of the entity's own ruin variable, else "regulator without stakes" (§2.0.2, §2.7, SCALE_ENDS note, CLAIM_MAP N30/N34). |
| BIO | R2-2 | Shared fate is partial (r); Frank's "not sufficient"; "some bees, wasps and ants police"; BK-P10 "partly share" (THEORY §6). |
| BIO | R2-3 | BK-IMP (a) step return, (b) robust to parameters, (c) structural check; Ma 2009, Barkai & Leibler 1997, Briat 2016 (metadata only). |
| BIO | R2-4 | Same as PHYS R2-1. |
| BIO | R2-5 | SE4 kill (iii): a non-hereditary, non-learning design nearer a GTAO optimum than unselected controls. |
| BIO | L1–L3 | Ratnieks content no longer stated (metadata only); Rosen clause trimmed; high-gain proportional note. |
