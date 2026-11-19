# BRIEF: A Theory of Adaptive Organization (GTAO), the whole record in plain words

**Written:** Wednesday 18 November 2026, about 3:55 PM ET (America/New_York), by a Grok Bot executor for Chad Mitchell, via Ace, in the repo consistency audit (branch `docs/consistency-audit-2026-11-18`). Nothing was posted or sent by that work.

**Checked against:** THEORY.md v1.4.28 (v1.4.22 plus the Reach notes, the fixes from their independent review, the v1.4.25 open-item work (one status change, N38), the v1.4.26 fixes from a second independent review (no status change) the v1.4.27 lock-pass fixes and the v1.4.28 fixes from its independent review (no status change)), CLAIM_MAP v2.47, `theory/BOOKENDS.md`, `measurement/FRAMEWORK.md`, `theory/SCALE_ENDS.md`, `reviews/night2/SCALE_ENDS_INDEP_REVIEW.md`, `reviews/night2/SYNTHESIS_2026-11-15.md`, `QUEUE.md`. Every statement below names the file and section it comes from. **If this brief and THEORY.md disagree, THEORY.md governs**; if a status here and CLAIM_MAP disagree, CLAIM_MAP governs. `python3 tools/check_consistency.py` checks the version pointers in this file and the CLAIM_MAP statuses it quotes.

**Why this file exists.** Chad (18 Nov, pt1928u) asked that nothing about the theory live only in an agent's memory or in off-repo notes. This file replaces Ace's off-repo briefs (`<local>/gtao/CURRENT_BRIEF.md`, `<local>/gtao/STATE.md`, `<local>/gtao-video/MEMORY_BRIEF.md`), which are now marked as stale pointers to this repo. A verbatim snapshot of CURRENT_BRIEF (written before PR #80) is kept in `history/2026-11-18_CURRENT_BRIEF.md` for provenance only.

---

## 1. The claim

- GTAO is a **falsifiable causal theory** of any adaptive organization. It is a theory, never a "law", and **not a theory of everything** (THEORY header and §0; CLAIM_MAP J3 WITHDRAWN by decision).
- One budget at every scale: the cost of holding memory, the loss from prediction error (including acting late), and the cost of the reads or effort that keep memory current, plus ruin risk. Only the implementation and the currency change (THEORY §0).
- The map from a world's drift spectrum (slope α, drift level q, sensing noise N, stakes) to design exponents is **classical** (optimal filtering and approximation theory plus a price on effort) and credited, not claimed as new (THEORY §0, §2.2, §10; CLAIM_MAP K13 MATH-CORRECTED). For reset reads with Hurst H the stakes and drift elasticities are a = b = **1/(1+2H) = 1/α** (formal Lemma 1(i); CLAIM_MAP N7 PROVED (in-model)); the square-root rules are the H = ½ (α = 2, Markov) case. Prior art: Kalman/Muth; Mora & Nemenman 2019 for a sensing cell; Lee, Flack & Krakauer 2024 as an application with an energy cost (THEORY §0, "What changed in v1.4" item 2).
- These exponents hold for a Gaussian world, or for the **best linear tracker** in any world. Outside a Gaussian world the best linear tracker is not the best possible one: the Bayes tracker of a switching world needs jump rate and size separately (THEORY §2.2 Regime A premise bullet; CLAIM_MAP N16 MATH-CORRECTED (in-model)).
- **The open bet is empirical and untested:** real, strongly selected systems sit near these optima once α, q, N and stakes are measured on the same system, with the same relations (not constants) at every level (THEORY §0, §1 N6; CLAIM_MAP N13 OPEN, J6 OPEN).
- **Regime first (binding):** every prediction names its section and its regime (A α = 2; B scale-free with measured α; C many modes with β; or not established), measured on the same system, before stating a number (THEORY §2.5; QUEUE rule 2).

## 2. Scope: atoms to the cosmos (Chad, t1927, 18 Nov 2026)

The three costs are physically priced at every scale. What changes along the scale is whether a model is worth carrying (THEORY §2.3 "The ends of the scale"; `theory/SCALE_ENDS.md`; independent referee PASS-WITH-FIXES).

| Claim | Status (CLAIM_MAP) | What it does and does not say |
|---|---|---|
| **Atoms are frozen.** With no action whose payoff depends on the world, Φ = 0 and holding never beats fading (E1); blind persistence is viable (E2; H ionization Boltzmann factor ≈ 10^−228.5 at 300 K) | N25 PROVED (in-model) | The "no move to make" step rests on the Axiom-7 reading of action and is **partly definitional**. Atoms **do** carry physical information (hyperfine spin ln 4 ≈ 1.39 nats; one atom's speed carries ≈ 0.08 nats about 300 K vs 600 K); that is physics, not a model. A model would cost at least kT ln 2 per bit erased and buy nothing. |
| **Stars are held with no model** (third class): they burn fuel and track nothing outside | part of SE4, PRIOR ART in substance (inside N25's row) | Three-class split credited to Prigogine 1978 and Pross 2011 (with Krakauer et al. 2020 related); Kolchinsky & Wolpert 2018 credited for semantic information only. |
| **Black hole = the extreme of the frozen class:** maximal memory for its size (Bekenstein-minimum energy per nat), no upkeep, readable state (M, J, Q), the rest returned scrambled only after about the Page time (≈ 0.54 t_ev), if evaporation is unitary, for pre-Page-time holes (all astrophysical holes today); leak lifetime ≈ 1.2×10⁶⁷ yr × (M/M☉)³ | N26 PROVED (in-model), conditional | Scope: pre-Page-time holes. Conditional on (i) the Axiom-7 reading of action, or SE-E2 + SE-E4, (ii) read latency counted as prediction error (lateness), and (iii) unitary evaporation. Post-Page-time holes rest on a conjectural decoding cost (Harlow–Hayden) and are outside the PROVED scope. With read cost priced as energy alone it fails. A classification given published physics, not a derivation of black-hole physics. |
| **Not claimed:** why black holes exist, the area law, the Page curve; "black holes think"; the universe as a tracker | N29 WITHDRAWN (as framing) | GTAO has no gravitational content. |
| **Light-delay federation (LAT-1):** a tracker of extent L with hold-last-value reads holds a target only if q(L/c)^{α−1} is below tolerance, so L_max = c(D\*/q)^{1/(α−1)}; large organizations federate | N27 OPEN | The bound is elementary and derived for hold-last-value reads; its real-system form is untested. Prior art in substance: Simon 1962; Abadi 2012 (PACELC). |
| **Switch-on of *selected* models:** heredity below Eigen's threshold, a world-dependent action, drift inside the hold band, a first nat that pays; for a bacterium E_gen ≈ 10¹¹–10¹² kT, so the Landauer floor does not bind | N28 OPEN (HYPOTHESIS) | Heredity and action overlap under the Axiom-7 reading; the non-circular content is the drift band, the energy inequality and Eigen's threshold. Survival-relevant information and minimal (integral-feedback) models are not excluded earlier; SCALE_ENDS SE4 kill (iii) tests the heredity clause (`theory/BOOKENDS.md` §2.1). |
| **Cosmic horizon:** memory cap ≈ 3.3×10¹²² nats; price of erasing a bit ≥ kT_dS ln 2 ≈ 2.1×10⁻⁵³ J (Landauer, in a bath at the de Sitter temperature) | SE13, DERIVED from PRIOR ART | Gibbons & Hawking 1977; Egan & Lineweaver 2010. Smolin's cosmological natural selection is credited; GTAO adds no support to it (SCALE_ENDS §4.4). |

FRAMEWORK §1.2 item 4 (the scope question left to Chad) is resolved by t1927 in Chad's direction; SCALE_ENDS shows the two readings agree (costs everywhere; design predictions where selection makes a model pay).

## 2a. Reach: viruses and life, the cosmic web, wormholes, the torus (v1.4.23, corrected in v1.4.24 after `reviews/reach_2026-11-18/INDEPENDENT_REVIEW.md`, open items worked in v1.4.25, 18 Nov 2026; `theory/REACH.md` and three companion notes)

- **Virus (a restatement with a common ledger; not new content).** A virus particle is frozen and pays nothing, while an infected cell and the viral lineage are alive, so GTAO says a virus is alive as a lineage, not as a particle, and treats "alive" as a ledger of who pays for what (a restatement of published views; `theory/REACH.md` §1). Ledger: U (upkeep), F (fidelity of the record), T (tracking), each of which can be paid by someone else; a virion is frozen, an infected cell is a held structure paid by the host, the lineage is a selected model. Close prior art, not an exact match (Forterre's virocell; Koonin & Starokadomskyy; Dupré & Guttinger); new only as one scale with the theory's own costs. CLAIM_MAP N36 PRIOR ART, N37 PRIOR ART, N38 PRIOR ART (v1.4.25: the K-V3 prediction was withdrawn after a prior-art sweep found every ingredient published, two with the opposite sign).
- **Cosmic web** (`theory/COSMIC_WEB.md`; N39 PRIOR ART, N40 OPEN). Real resemblance to other networks, part geometry and part gravity: a proximity null on random points already gives clustering about 0.42 and positive assortativity, the real web adds more clustering and a broader degree spread (real gravitational structure), and v1.4.25 withdrew "no hubs reported": hub-like degree heterogeneity exists in halo networks (Yang & Yu 2023) and in an own SDSS check (far above Poisson, below Barabási–Albert), and whether it exceeds a two-point-matched null is OPEN (N48). A better matched null in the second independent review found no hub excess, but it failed its two-point check at 5–11 Mpc/h, and the hub share depends on the null's higher-order structure; the spec now calls for N-body-based mocks. Hubness is tied by hypothesis to a priced delay, a mechanism that is prior art in several fields, so the presence of hubs is not diagnostic (N40; price-to-λ map N50 defined, staleness cost unmeasured). The web tracks nothing; its structure is initial conditions plus gravity and baryonic physics.
- **Wormholes** (`theory/WORMHOLES.md`; N41 PROVED (in-model), CONDITIONAL; N42 OPEN; N47 PROVED (in-model), CONDITIONAL, v1.4.25, independently re-derived in v1.4.26: unreliable throats raise the price of pooling, and where shortcuts act as a uniform faster medium reach grows only if β < α − 1). For reach, open versus finite is the first split: finite throats with a per-hop delay act as a faster medium (v_eff ≤ Λ/τ) and LAT-1 survives, while open throats remove the distance limit. For centralization: latency, capacity, shared drift and dissemination price, upkeep, reliability and chronology. Zero latency alone does not force centralization (central beats local at zero latency iff d/c < 1 − 1/N). The ceiling is the holographic bound. NASA's 2012 "X-points" are magnetic reconnection sites, not wormholes. No claim that wormholes exist.
- **Torus** (`theory/TORUS.md`; N43 PRIOR ART, N44 NOT EVIDENCE, N45 OPEN, N49 PROVED (in-model), CONDITIONAL; a price-to-K map is defined for oscillators with a measured phase-response curve). The torus is the state space of two phases and Arnold tongues are textbook (checked). The earlier toy test was INVALID as a test (coupling forces locking); its staircase prediction did fail in-toy, and the INVALID judgment came after the result. No prediction about the shape of the universe.
- **Dark matter, dark energy, fractal time** (`theory/REACH.md` §3, §4; N46 WITHDRAWN as framing). Inputs, not outputs; fractal only where the world is scale-free (T7).

## 3. Measurement (`measurement/FRAMEWORK.md`)

- A prediction X follows from theory T plus measurement mapping M plus auxiliaries A. **A failed X refutes the conjunction T∧M∧A**; it moves blame to T only if M and A were validated first (FRAMEWORK §1.1).
- **Gates MV1–MV10** (§2.2), **three tiers** (Tier 1 decisive = every gate; Tier 2 = MV1–MV4 and MV8; Tier 3 otherwise), and the **anti-rescue (admissibility) rule**: a test that passes MV1–MV8 counts fully, win or lose.
- **The gates are treated as binding from 18 November 2026, on Chad's instruction to proceed without his sign-off (t1927)** for every new prereg (CLAIM_MAP M2, v2.40 note); this is a working decision, not a formal approval. MV9's external timestamp is an outside act and still needs Chad's go for each lock, so no Tier-1 result can exist until that go is given.
- The re-audit of every past field test found **no FIELD-PASS and no FIELD-FAIL**: the theory is **untested in the field, not refuted** (FRAMEWORK §2.3, §4 "Net position"). No Tier-1 test has run.
- **Proxy results do not count as field results.** A proxy fail is a valid fail *of that mapping* and narrows where the theory can live; it is not a refutation of the theory (FRAMEWORK §1.2 item 2, §2.3). Report every field result as "passed / failed on proxy X".
- **Vigilance is OPEN** (CLAIM_MAP H8 OPEN; the nomination-network rows N1 and N2 are PROXY-PASS (downgraded) and N3 is OPEN). The onset value at zero upkeep is 1 + (1+ρ)^{−1/2}, between 1 and 2; "≥ 2" is wrong as stated (THEORY status block).
- **Next real test:** SAME-SYSTEM-AQN, the first test of N13 (SYNTHESIS §7; QUEUE), on a system whose stakes can be estimated.

## 4. The freeze / hold / lookup band

- **Theorem G** (GENERAL_THEOREM; THEORY §3 "Freeze-or-hold" row): a checked copy beats fading iff drift × check cost < Φ. PROOF.
- **Theorem 8 / T8** gives the closed-form band: freeze edge, lookup edge, and a hold band **iff μuH_l > 2c + hH_l**, with N² widening for shared stores (CLAIM_MAP F13 PROVED (in-model)). A band need not exist.
- Field readings: measles freeze-or-hold passed on proxy (H9 PROXY-PASS; the proxy measured use rate μ, not antigenic drift q); WIKIDATA-BAND N19 OPEN (known-groups check failed), N20 PROXY-PASS (weak); immune strategies PRIOR ART (Mayer et al. 2016 show the best strategy depends on pathogen frequency and timescale; mapping those strategies onto freeze, hold and lookup is ours; CLAIM_MAP I4).

## 5. Wording rules

"Theory", never "law" or "theory of everything". Field results are "passed / failed on proxy X". No field kills. Proof-level corrections are MATH-CORRECTED; locked simulation failures are SIM-FAIL. Repo is public as of 18 November 2026; posts and other outside acts still need Chad's go (STATUS "Standing rules").

## 6. Corrections to earlier agent memory found in this audit

| Earlier belief | What the files say |
|---|---|
| "The freeze/hold band is Theorem G" | Theorem G is the hold-vs-fade condition; the closed-form band is Theorem 8 (T8; CLAIM_MAP F13). Both are in-model results. |
| "Gates MV1–MV10 await Chad's sign-off" (superseded) | Treated as binding from 18 November 2026, on Chad's instruction to proceed without his sign-off (t1927; CLAIM_MAP M2). MV9's external timestamp still needs Chad's go per lock. |
| "Proxy fails don't count against the theory" | They do not refute it, but each kills the tested mapping and narrows the theory (FRAMEWORK §1.2 item 2). |
| "Laughlin: synapses pay 10⁵ × kT ln 2" | Laughlin et al. 1998 give about 10⁴ ATP per bit at a chemical synapse (2–6×10⁴ in the text) and 10⁶–10⁷ for graded signals and spikes; at ΔG_ATP ≈ 20 kT (our conversion) that is **at least about** 3×10⁵ × kT ln 2 (THEORY §2.3). |
| "England 2013 = dissipative adaptation" | England 2013 is the self-replication heat bound. Dissipative adaptation is England 2015 (*Nat Nanotechnol* 10:919) and Perunov, Marsland & England 2016 (*PRX* 6:021036): related prior art and a possible rival route with no model, not a rival to the N28 switch-on conditions (THEORY §10; LITMAP; THREATS). |
| "The market (VIX) test measured all the inputs" | KERNEL-MEASURE measured α, q and N on one system and compared one stakes-free design quantity; it did not measure stakes, and it compares against the best linear tracker (THEORY §2.4). |
| "Black hole: the rest comes back after ~10⁶⁷ years" | For a hole of one solar mass; the time scales as (M/M☉)³ (SCALE_ENDS §0 item 3; erratum note in SCALE_ENDS). |
| "The theory is silent on black holes / nothing keeps score at the cosmic scale" (superseded) | Wrong (SCALE_ENDS §8). See §2 above. |
| "ANTS1 is unfinished" | Finished 15 Nov; `reviews/night1/ANTS1_WRITEUP.md`; CLAIM_MAP G13–G17. |
| "Measles freeze-or-hold passed" | Passed on proxy only: H9 PROXY-PASS. |

## 7. Off-repo notes and where their content now lives

| Off-repo file | Status | Where the content is in the repo |
|---|---|---|
| `<local>/gtao/CURRENT_BRIEF.md` (18 Nov, before PR #80) | Stale; pointer banner added | This file; snapshot in `history/2026-11-18_CURRENT_BRIEF.md`. Its §8 file conflicts are resolved in §8 below. |
| `<local>/gtao/STATE.md` (15 Nov; says THEORY v1.2) | Stale; pointer banner added | `STATUS.md` |
| `<local>/gtao-video/MEMORY_BRIEF.md` (cites main 77dd71c, CM v2.37) | Stale; pointer banner added | This file |
| `<local>/gtao/longform/HYPOTHESES.md` (raw log, 11 Nov; not imported because it mixes in personal context) | Frozen history; relabel banner added | **H1** ("black holes: maximal storage, not organizers"; unaudited) is superseded by CLAIM_MAP **N26** (PROVED (in-model), conditional); it survives as a derived output, not a scope exclusion. **H8/H9** (free vs paid persistence; "freeze or hold") live on as the three persistence classes (N25/SE4) and the T8 band (F13). **H2** (origin of life) is superseded by **N28** (OPEN). **H7** ("upkeep near zero means they never fade") is narrowed by E4: frozen stores have finite lifetimes set by a barrier, a conservation law or a leak. |

## 8. Conflicts listed in CURRENT_BRIEF §8, and how they stand on main

| Conflict | Resolution |
|---|---|
| README pointed to THEORY v1.4.3a and CLAIM_MAP v2.12 | Fixed; checked by `tools/check_consistency.py` |
| ANTS1 "unfinished" in README, tests/README, applications/README | Fixed |
| THEORY §8 said measles "passed" | Fixed: "passed on proxy" (H9 PROXY-PASS); other field verdicts in §4, §8, §8b also labelled |
| FRAMEWORK §6.10 said the spectrum map was owed | Note added: derived in THEORY §2.2; N13 stays OPEN |
| M2 gates "need Chad's sign-off" (superseded) | Treated as binding from 18 November 2026, on Chad's instruction to proceed without his sign-off (t1927; v2.40) |
| THEORY §2.3 named SENSE-CELL as the open test | Note added: ran, N24 INCONCLUSIVE; disagreement stays open |
| Black holes: H1 vs Chad's view | Resolved by SCALE_ENDS (N26) |
| CLAIM_MAP counts header (194 rows) not recomputed | Still stated as not recomputed (CLAIM_MAP "Counts"); left as is |
| `queue/items.json` statuses lag STATUS/LEDGER | Not changed in this audit (the queue files are the scored ledger's inputs) |
| THEORY status block and §0 still read "15 November" and "from cells to cities" for the empirical bet | DONE: headline text merged (THEORY v1.4.19) |
| Public X post of 12 Nov says atoms have "nothing to maintain" | Superseded; archived verbatim in `history/2026-11-12_X_POST.md` with what changed |

## 9. Pending

- DONE: the headline/status-block update to THEORY (dated status block naming the ends of the scale and binding gates; §0 scope sentence) was reviewed and merged as v1.4.19.
- SAME-SYSTEM-AQN; SENSE-CELL-MATCHED; the SG referee and SG scoring (QUEUE Q0, SG-SCORE). C3b is blocked: MV10 power gate not met at the largest n the frame supplies (`reviews/night2/C3B_GATE_ADDENDUM.md`), so it cannot give a verdict as preregistered.
