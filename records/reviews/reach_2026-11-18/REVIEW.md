# Review: REACH notes (`theory/REACH.md`, `COSMIC_WEB.md`, `WORMHOLES.md`, `TORUS.md`) and CLAIM_MAP v2.42 rows N36–N46

Wednesday 18 November 2026, night ET (America/New_York). One review pass, written after the notes and edits were committed on branch `reach-notes-2026-11-18` (commit d57669d) and before the PR.

## Independence (read this first)

**This pass is not independent.** The executor that wrote the notes had no way to start a separate reviewer in this environment, so it re-read its own work adversarially, from the committed files, and re-checked every source against the source itself instead of its own notes. Treat it as a second reading by the same author, not a blind grader. The same bot family wrote and reviewed. What it can and cannot show:
- It can show: citations resolve and say what they are cited for; numbers match the saved code output and the repo files; wording rules hold.
- It cannot show: that the logic is the right logic. The wormhole algebra, the lock-versus-drift hypothesis and the reading of the cosmic-web numbers still need a reader who did not write them. That is listed under "Left open".

## What was checked, and how

1. **All 29 DOIs** in the four notes were re-resolved against Crossref on 18 Nov 2026 (title, year, journal, volume, pages, first author). All 29 resolve and match.
2. **Abstract-level claims** quoted in the notes were re-read in the abstract (Europe PMC / arXiv): Li 2010, McCutcheon & Moran 2012, Stoye 2012, Cleland & Chyba 2002, Koonin & Starokadomskyy 2016, Dupré & Guttinger 2016, Moreira & López-García 2009, Sanjuán 2010, Gago 2009, Erez 2017, Raoult 2004, Sallon 2008, Tsujimoto 2016, Drake 1991, Ruiz-Mirazo 2004, Bull 2007, Mix 2026, Gao–Jafferis–Wall, Maldacena–Stanford–Yang, Bousso 2002, Barabási–Albert, Guimerà et al., Bond–Kofman–Pogosyan, Planck 2015 XVIII. Benner 2010's "cell, virus, or a single rabbit" sentence was found in the PMC full text (it is not in the abstract).
3. **Planck 2018**: Ω_c h² = 0.120 ± 0.001 and Ω_m = 0.315 ± 0.007 (abstract); Ω_K = 0.0007 ± 0.0019 (eq. 47b). **FKP Theorem 1** constants (1/√2, Ω(√n), α ≥ 4 and o(√n), unit square): re-read in the paper text. **Watts & Strogatz** Table 1 values: re-read in the paper text. **Coutinho Fig. 4**: viewed (clustering and assortativity read by eye; stated as such).
4. **Repo cross-references** were re-checked against the repo: DRIFT1 numbers (NYC 311, Wikipedia, EDGAR), COLLAPSE1 A1 (5 of 8 = 62.5%, kill line 65%), H16/H18/H20 statuses, SCALE_ENDS horizon numbers, T3a, T7, K12, MV2/MV7 definitions.
5. **Code**: the three check scripts were rerun at `nice -n 19`; each output is byte-identical to the saved `.out` file. `check_consistency.py` PASS, `test_check_consistency.py` PASS, `pytest tools/` 50 passed (before and after the fixes below).
6. **Wording rules**: no "law" or "theory of everything" used of GTAO; every field-result verdict near BIO1, COLLAPSE1 or DRIFT1 carries a proxy or label word (`check_consistency.py` wording scan: 0 FAILs on the 22 maintained docs, now including the four new notes).
7. **Scope and privacy**: nothing from the private Looper repo is used; Test C is described only in the wording its own review allows (an unpublished toy, off-repo), with no personal data; no existing status, locked prediction or the spine changed (the diff touches only the new rows and pointers).

## Findings and dispositions

BLOCKER = an unsupported attribution or a wrong claim a reader could be misled by. SHOULD-FIX = a wrong pointer, label or overstatement. All were fixed in the same branch before the PR.

| # | Class | Finding | Fix |
|---|---|---|---|
| 1 | BLOCKER | `COSMIC_WEB.md` §3 presented "levels = ln N / ln k_max" as "the theory's own derived result" for hierarchy span. The repo does not contain it; it is plain arithmetic with k_max an input. It was also used to argue connectome hubs are limited, with no source read | Relabelled ARITHMETIC (not a result of the theory); the connectome claim removed; the table row changed to match |
| 2 | BLOCKER | `REACH.md` §0, §1.7, CLAIM_MAP N36 and BRIEF said the "alive as a lineage, not as a particle" verdict is already published and cited Koonin & Starokadomskyy and Dupré & Guttinger for it. Their abstracts do not say that: Koonin & Starokadomskyy call the yes-or-no question "without substance" and give a replicator continuum; Dupré & Guttinger treat viruses as processes. Only Forterre's virocell is close to the split | Reworded everywhere to "close prior art, not an exact match", naming what each source actually says; the split is credited as Forterre's plus a lineage level on one ledger |
| 3 | BLOCKER | The lethal-mutagenesis bound e^{−U_d}·R_max < 1 was attributed to Bull, Sanjuán & Wilke 2007. The abstract states a different, verbal sufficient condition (fewer than one progeny that infects a new cell) and says the threshold "cannot be calculated from the mutation rate alone" | Stated the abstract's condition; the e^{−U_d}·R_max form is labelled the standard deterministic mutation-load bound, not found in the opened text; K-V2 and N37 reworded to inherit only that bound; the source note says abstract only |
| 4 | SHOULD-FIX | The number-of-stores statement cited "N4, MATH-CORRECTED". N4 is a different row (SELF P1, OPEN) | Now K12 (MATH-CORRECTED) and THEORY §2.2 "Number of stores" |
| 5 | SHOULD-FIX | T7 was given as "CLAIM_MAP T7 PROOF (conditional)"; T7's status is in `THEOREMS.md` and the CLAIM_MAP row is K12 | Reworded to the actual sources |
| 6 | SHOULD-FIX | The torus note called the toy test's proxy mismatch "MV5". MV5 is convergent validity; the gate that fits is MV2 (construct match) | Changed to MV2 in `TORUS.md` and N44 |
| 7 | SHOULD-FIX | Mimivirus "not the ribosome" and viroid "host polymerases" were attributed to sources whose abstracts do not say that | Reworded to what the abstracts say (Raoult: repair pathways and translation components, no ribosome listed; Gago: host RNA polymerases and ribozymes; Flores: no protein-coding ability) |
| 8 | SHOULD-FIX | `WORMHOLES.md` described T3a as "pool when N > …". T3a is a sufficient condition, not a cutoff | Reworded to "guaranteed cheaper when", and stated as a sufficient condition |
| 9 | SHOULD-FIX | "does most of it" for how much a proximity null reproduces of the web's clustering (0.42 of about 0.6) overstated | "does much of it" |
| 10 | SHOULD-FIX | Source-status labels: Forterre 2013 (metadata only) and Mix 2026 (journal and volume) | Marked and completed |

Checked and found correct (no change): the 29 DOIs; the pooling closed forms (rerun to 10⁻³ relative, with the exact identity asserted in code); the station-catchment formula against simulation (within 0.005 at all nine points; the notes first said 0.01, which was loose, and now say 0.005); the circle-map tongue widths (within 1e-4 of K/π); the Benner/NASA "system" claim; the Planck numbers; the DRIFT1 numbers; the FKP constants.

## Remaining weaknesses (not fixed; stated in the notes)

- **Not independent.** See the first section.
- **The wormhole model is a sketch of an idea, not a model of a throat.** Fully shared drift (ρ = 1) is used for the closed forms; ρ < 1 relies on T3a, not on a new derivation. Hop latency is a single number τ. The dissemination price d is an input with no physical estimate.
- **The cosmic-web clustering and assortativity values come from reading a figure by eye.** The sign of the assortativity and the ordering (web above random for clustering) are clear; the numbers are approximate. A 2018 paper (Libeskind et al.) was not opened.
- **The torus lock-versus-drift hypothesis (N45) has no derived optimum.** A linear benefit and price give all-or-nothing, which the note says; the hypothesis is therefore about plateau structure only.
- **The cost ledger is partly definitional**, as the notes say. K-V1 is a calibration check and its pass would be weak; K-V3 is the only prediction specific to GTAO, and it is untested with a prior-art sweep owed.
- **Metadata-only or abstract-only sources** are marked in each reference list. Textbook sources for the circle map (Adler, Pikovsky et al., Arnold, Greene) were not opened.

## Verdict

PASS-WITH-FIXES, all applied. The notes make no claim beyond what their labels allow; no existing status changed. A separately run reviewer is still owed for the logic (not the citations).
