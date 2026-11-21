# Independent hostile review: PR #124 (E. coli qualification literature check)

**Reviewer:** independent (wrote none of this PR, the qualification file, the CLAIM_MAP pointer notes, THEORY §3, FRAMEWORK §9, or the E. coli test package).
**Date:** Saturday 21 November 2026, started 12:33 AM ET, finished 12:45 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/124
**Clone:** fresh `/tmp/rev124/repo` at head `f33d26f5dd77e271cf1876cde8a0fc6d29786889` (branch `ecoli-qual-2026-11-21` / `pr124`), base `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c` (merge-base equals base). Clean tree. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The literature check does what it claims: it records THEORY §3 / FRAMEWORK §9 items (a)–(e) for *E. coli* from Crossref-verified sources, decides each item **NOT ESTABLISHED**, and does not re-score P1, P3, P4 or P13. The label is the right one (not NOT QUALIFIED). Quoted values that could be checked against open-access full text or official abstracts are in the cited sources at the cited tables, figures, or abstracts. One CLAIM_MAP wording issue should be fixed before merge; it does not change any status or the qualification verdict. Checkers pass; `pytest tools/` is 125 passed.

---

## What was checked

- Fresh clone at the stated head/base; diff `4398bbd..f33d26f` (one commit, two files: `theory/measured/ecoli/QUALIFICATION_2026-11-21.md` added, four pointer sentences in `measurement/CLAIM_MAP_v2.md`).
- THEORY.md §3 (the operational definition of “strongly selected”) and FRAMEWORK.md §9 item 1 (about line 705) and items 2–7, plus the §2.2 status vocabulary for NOT A TEST, read as written and compared to every verdict in the qualification file.
- Commit order and CLAIM_MAP cell diffs for P1, P3, P4 and P13: status column, claim text, and historical proxy labels versus base `4398bbd`.
- Every DOI in the source table (and Rocha 2018, sought and not used) re-queried on the Crossref API this review (21 November 2026). Open-access full texts fetched as NCBI PMC JATS XML for Honda, Ni, Schavemaker & Lynch, Lisevich, Sung, Bobay & Ochman, Lapierre, and Gibson; Bobay Additional file 1 / Table S1 fetched as the journal ESM xlsx. Official abstracts / front matter for Berg, Ghalayini, Poulsen, and Hartl (publisher blocks full-text XML). Mori 2021 full text also retrieved (the PR did not). Honda SI Appendix and Ni Datasets S1–S4 were sought and not retrieved (PNAS SI PDF returned 403, as the file says).
- Every quoted sentence and every reported table value checked against those sources.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `nice -n 19 python3 -m pytest tools/ -q`.
- DEVIATIONS.md DV2 (named objective) against the file’s preamble.

---

## Integrity and commit order

- One commit on the branch: `f33d26f` “Record E. coli qualification literature check before any re-score,” AuthorDate / CommitDate Saturday 21 November 2026, 12:32:32 AM EST. The file header (“about 12:30 AM ET”) is consistent with that stamp. The stated base SHA `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c` is exact.
- The qualification file and the CLAIM_MAP pointer notes are in the same commit. There is no later commit, and no re-score of P1, P3, P4 or P13: statuses, claim wording, and historical proxy labels are byte-identical to base except for one appended sentence on each of those four rows.
- Appended sentence (identical on P1, P3, P4, P13): “That literature check is now recorded in `theory/measured/ecoli/QUALIFICATION_2026-11-21.md` (21 November 2026; written and committed before any re-score). This row’s status is unchanged.”
- Statuses on HEAD, unchanged from `4398bbd`:
  - P1: **NOT A TEST (qualification not established; proxy: failed)**
  - P3: **NOT A TEST (qualification not established; proxy: failed)**
  - P4: **NOT A TEST (qualification not established; proxy: passed)**
  - P13: **NOT A TEST (qualification not established; proxy: failed)**
- No other CLAIM_MAP rows changed. Locked ECOLI-MEM calculations are not reopened. The “before any re-score” claim holds on this branch.
- DV2 is honoured: the file names the objective (per-cell growth rate through σ / per-cell J, the same objective under which P1–P16 were scored) before the literature is used, and states that lineage growth G and bet-hedging are not the objective of this record. The compared statistic is correctly marked unused, because no design is scored.
- The selection-temperature note (`thermo-bridge-2026-11-21`) is correctly scoped out of every verdict.

---

## DOI and bibliographic checks (Crossref, this review)

All fifteen DOIs resolve. Authors, title, year, journal, volume, and issue match the file. Pages / article numbers match, with one style note that is not a wrong paper.

| Source as cited | DOI | Crossref (this review) | Match |
|---|---|---|---|
| Honda et al. 2022, *PNAS* 119(37): e2110342119 | 10.1073/pnas.2110342119 | Honda, Cremer, Mancini, Zhang, Pilizota, Hwa; 2022 (print 13 Sep; online 6 Sep); vol 119(37); art e2110342119 | Yes |
| Ni et al. 2020, *PNAS* 117(1): 595–601 | 10.1073/pnas.1910849117 | Ni, Colin, Link, Endres, Sourjik; print 7 Jan 2020, online 23 Dec 2019; 117(1): 595-601 | Yes (the file already notes both dates) |
| Schavemaker & Lynch 2022, *eLife* 11: e77266 | 10.7554/eLife.77266 | 2022 (26 Jul); art e77266 | Yes |
| Lisevich et al. 2025, *Nat. Commun.* 16: 1731 | 10.1038/s41467-025-56980-x | Lisevich, Colin, Yang, Ni, Sourjik; 2025 (18 Feb); art 1731 | Yes |
| Sung et al. 2016, *G3* 6(8): 2583–2591 | 10.1534/g3.116.030890 | Sung, Ackerman, Dillon, Platt, Fuqua, Cooper, Lynch; 2016; 6(8): 2583-2591 | Yes (XML fpage 2583 / lpage 2591 confirmed) |
| Bobay & Ochman 2018, *BMC Evol. Biol.* 18: 153 | 10.1186/s12862-018-1272-4 | 2018 (online 12 Oct); art 153 | Yes |
| Lapierre et al. 2016, *Mol. Biol. Evol.* 33(7): 1711–1725 | 10.1093/molbev/msw048 | Lapierre, Blin, Lambert, Achaz, Rocha; 2016; 33(7): 1711-1725 | Yes |
| Hartl, Moriyama & Sawyer 1994, *Genetics* 138(1): 227–234 | 10.1093/genetics/138.1.227 | 1994; 138(1): 227-234 | Yes (DOI / record only, as stated) |
| Berg 1996, *Genetics* 142(4): 1379–1382 | 10.1093/genetics/142.4.1379 | Otto G. Berg; 1996; 142(4): 1379-1382 | Yes |
| Ghalayini et al. 2018, *Appl. Environ. Microbiol.* 84(6): e02377-17 | 10.1128/AEM.02377-17 | Ghalayini, Launay, Bridier-Nahmias, Clermont, Denamur, Lescat, Tenaillon; 2018; art e02377-17 | Yes |
| Gibson, Wilson, Feil & Eyre-Walker 2018, *Proc. R. Soc. B* 285(1880): 20180789 | 10.1098/rspb.2018.0789 | 2018; 285(1880): 20180789 | Yes |
| Poulsen, Licht, Rang, Krogfelt & Molin 1995, *J. Bacteriol.* 177(20): 5840–5845 | 10.1128/jb.177.20.5840-5845.1995 | 1995; 177(20): 5840-5845 | Yes |
| Lynch et al. 2016, *Nat. Rev. Genet.* 17(11): 704–714 | 10.1038/nrg.2016.104 | Lynch, Ackerman, Gout, Long, Sung, Thomas, Foster; 2016; 17(11): 704-714 | Yes (DOI verified, not quoted, as stated) |
| Mori et al. 2021, *Mol. Syst. Biol.* 17: e9536 | 10.15252/msb.20209536 | Mori et al.; 2021; vol 17; Crossref article-number MSB20209536 | DOI / authors / year / journal / volume yes. Elocation: Europe PMC pageInfo is `e9536` (as cited); Crossref uses `MSB20209536`. Same article, two labels. Cited only as Honda’s ref. 11; not used as a primary source. |
| Rocha 2018 (sought, not used) | 10.1093/molbev/msy078 | Rocha; *Mol. Biol. Evol.* 35(6): 1338–1347; 2018 | Yes (correctly unused; not OA here) |

---

## Quoted values versus sources

Unless noted, the quoted sentence or table value is in the cited place. Ellipses are honestly used. Unretrieved SI / datasets are disclosed and not invented.

**Honda et al. 2022 (PMC9478672, full text).** The “up to 18%” sentence is verbatim in the main-text narrative immediately before Discussion (the PNAS JATS has no titled Results section; the paragraph is a direct child of `<body>`). It cites SI Appendix Fig. S2E. This review also failed to retrieve that SI PDF (publisher 403), so the condition-wise values remain unread, as the file says. The Discussion proteome sentences (∼3.0% / ∼0.7% citing ref. 11; 2.3% “saving”; ∼0.06 1/h per proteome-percent; ∼0.14 1/h) are verbatim. They are correctly not used as σ.

**Ni et al. 2020 (PMC6955288, full text).** Both long quotations are verbatim, including the paper’s own wording “the cost the chemotactic signaling was negligible.” They sit in “Results > Relative Fitness Cost of Motility Depends on Carbon Source” and in Discussion, as cited. 72 h and the 1:1 start are in that Results section and in the Fig. 1 caption. No single numerical growth-rate cost or selection coefficient appears in the main text; figure / SI values were not read off. Confirmed.

**Schavemaker & Lynch 2022 (PMC9323006, full text).** The energy-budget paragraph is verbatim in “Results > Bacteria – cost of the E. coli flagellum.” Table 1 gives relative construction 5.0%, operating 5.2%, total 10.2%; construction 7.88 × 10^8 ATP cell^–1; operating 8.08 × 10^8 ATP per cell cycle; total cell cost 1.59 × 10^10 ATP; division time 1.0 h; 3.4 flagella per cell. The 3.8-fold mismatch sentence, including the “variability of E. coli cell volume” / “not continuously rotating” clause, is verbatim. Correctly treated as energy-budget fractions, not σ.

**Lisevich et al. 2025 (PMC11836070, full text).** The 2–8% Introduction sentence is verbatim. Correctly labelled a secondary summary.

**Sung et al. 2016 (PMC4978911, full text), Table 1 row *Escherichia coli* (Ec):** θ_s or π_s = 0.071; N_e (× 10^6) = 179.60; u_bs (× 10^−10) = 2.00 with footnote e = Lee et al. (2012). The rewrite N_e = 1.7960 × 10^8 is just that table entry. The formula θ_s = 2 N_e u_bs is in the paper (haploids; diploids are 4 N_e u_bs). Table θ_s = 0.071 is a rounding of 2 × 179.60 × 10^6 × 2.00 × 10^−10 = 0.07184; the file reports the table’s N_e, not a recomputed one. Fine.

**Bobay & Ochman 2018 (PMC6186134, full text; ESM xlsx).** The 10^8–10^9 sentence is verbatim in “Results > Variation of Ne across bacterial phyla and lifestyles,” with JATS superscripts running as 108–109, as the file notes. Additional file 1, Table S1, row “Escherichia coli”: 400 strains; lifestyle “commensal”; universal-gene N_e (column J, under the 0.1 < dS < 0.3 header group) = 416911778.112; core-gene N_e (column O) = 374704250.0. Exact match to 416,911,778.112 (4.169 × 10^8) and 374,704,250.0 (3.747 × 10^8).

**Lapierre et al. 2016 (PMC4915353, full text).** Table 2 caption is “Parameters for E. coli Populations Used in the Simulations.” Row: “Effective population size (Ne) | 1.8 × 10^8 | Hartl et al. (1994).” Text: “The effective population size of the species is estimated at >10^8 (Hartl et al. 1994; Lynch 2006).” Verbatim. The 1.8 × 10^8 figure is correctly attributed to Lapierre’s table, not read from Hartl. Hartl full-text XML is publisher-blocked (confirmed this review). Lynch 2006 not retrieved, as stated.

**Berg 1996 (official abstract).** The quoted abstract, including the 10^5–10^8 range and the colony-versus-species N_e distinction, matches the official abstract. The typography “(10)5 and (10)8” is the Europe PMC / front-matter rendering of 10^5 and 10^8.

**Ghalayini et al. 2018 (official abstract / front matter, PMC5835743).** Both quotations are verbatim, including “N_e of ≈500 to 1,700” and the Importance sentence on a “very limited effective population size.” Full text XML is publisher-blocked, as stated.

**Gibson et al. 2018 (PMC6015860, full text), Table 1, row *Escherichia coli*:** accumulation rate 1.44 × 10^−7; mutation rate 2.54 × 10^−10; DT (h) (s.e.) = 15 (7.7); laboratory DT (h) = 0.33; ratio = 45. The Results sentence “E. coli can double every 20 min in the laboratory but we estimate that it only doubles every 15 h in the wild” and the Introduction “divide every 20 min … under aerobic, nutrient-rich conditions” are verbatim. 0.33 h is 20 min. The two stated assumptions (mutation rate per generation the same in wild and lab; all wild mutations neutral) are the paper’s; “is not very important” is the authors’ phrase for the neutrality assumption. The file correctly refuses to put “may include quiescence” in quotes (the Discussion does mention periods of quiescence, but that exact phrase is not in the paper).

**Poulsen et al. 1995 (official abstract).** The 40–80 min mucus / static luminal two-population sentence is verbatim. Correctly scoped as a streptomycin-treated mouse model, strain BJ4.

**Values not independently verifiable from sources retrieved here (all disclosed in the file, none used as a unique σ, N_e or T_red):** Honda SI Fig. S2E condition-wise growth-rate costs; Ni Fig. 1C–E and Datasets S1–S4 numerical fitness values; Hartl 1994’s own tables (1.8 × 10^8 is Lapierre’s attribution); Ghalayini and Poulsen full methods (abstracts only); Mori 2021’s raw proteome shares (Honda’s 3.0% / 0.7% quotation was not re-read from Mori; this review retrieved Mori’s main text and did not find those two percentages stated there — they may sit in datasets. Not material: those shares are not used as σ). No invented numbers were found.

---

## Verdicts versus FRAMEWORK §9 / THEORY §3

The blockquote in §1 is a fair abridgement of THEORY §3, with ellipses. FRAMEWORK §9 item 1 is the protocol for the same five items, not the same wording (the cell-scale parenthetical and the Lynch DOI live in THEORY). That is a nit, not a misapplication.

All five items must hold, with the evidence recorded, for the class to qualify. A class that does not qualify “is not evidence either way.” The file applies that rule and does not invent unique values to force a pass.

- **(a) NOT ESTABLISHED — correct, and not too strict.** σ is “the fractional change in … growth, survival or reproduction rate *per fractional change in J*.” The cell-scale parenthetical (“the measured growth-rate cost of the design variable”) names the empirical ingredient, not a substitute for the elasticity. Honda’s “up to 18%” is a measured finite-difference growth-rate cost of deleting the motility regulon; it is not σ unless J’s units and ΔJ/J for the same perturbation are preregistered. “No map, no qualification” is the THEORY text. Energy-budget and proteome shares are correctly refused. Not computing a unique σ is the right refusal, not a dodge.
- **(b) NOT ESTABLISHED — correct, and not too strict.** “Cells and microbes: measured” does not mean any published N_e may be plugged in. The definition is “independent lineages competing in the same world per redesign time.” Species-wide diversity N_e (~10^8–10^9), Berg’s 10^5–10^8 range, and Ghalayini’s within-host ≈500–1,700 are real measurements of different quantities (Berg already says so). No class-specific choice was preregistered. Picking 10^8–10^9 because it is “very large” would have been too lenient.
- **(c) NOT ESTABLISHED — correct.** ε = 10/(σ·N_e) cannot be computed without a unique σ and a unique N_e. The orientation arithmetic (order 10^−6 with 0.18 and N_e ~ 10^8; order 0.06 with N_e ~ 10^3; possibly order 1 if the unread Honda lower end is much smaller and N_e ~ 500) recomputes and is clearly labelled “not as a qualification value.” It does, for scale only, treat the 18% knockout cost as if it were σ (implicitly ΔJ/J = 1). That is acceptable only because it is not used as a band. See N1.
- **(d) NOT ESTABLISHED — correct.** Power requires a recorded design-unit band, with measurement error, that excludes at least one named rival (R1–R3). No such band or δ_meas is recorded. The file correctly refuses to convert locked ECOLI-MEM numbers into a power calculation, which would have been a re-score.
- **(e) NOT ESTABLISHED — correct, and not too strict.** T_red may be “measured or preregistered from the class’s turnover.” Generation times were recorded and could later support a preregistered proxy; they are not T_red until so preregistered. No 1 − 1/e closing time of the motility / chemotaxis design was found. The methylation-layer ~10 s time is correctly rejected as T_red. The 10 T_red same-world requirement is therefore not shown.

**NOT ESTABLISHED versus NOT QUALIFIED is the right label.** FRAMEWORK §2.2 reserves “not qualified” for a class *shown not to qualify*, and “qualification not established” for a missing or unrecorded check. Nothing here demonstrates that the class fails on substance (for example, that ε cannot exclude a rival, or that N_e is undefined as it is for cities). The evidence is incomplete or non-unique. Calling the class NOT QUALIFIED would have been too harsh and would have closed a door the definition still leaves open. The overall “NOT ESTABLISHED,” and the unchanged CLAIM_MAP statuses **NOT A TEST (qualification not established; …)**, follow the vocabulary as written.

The check is retrospective relative to the original E. coli scoring, and is honestly framed as recorded before any *re-score*, not before the original measurement. That is the only honest path given the history.

---

## Checkers and tests

- `python3 tools/check_open_work.py`: **PASS** (union of not-DONE items.json / QUEUE.md missing from OPEN_WORK.md = 0).
- `python3 tools/check_consistency.py`: **PASS** (0 FAIL; advisory THEORY.md / README.md length warnings only, already present on base).
- `nice -n 19 python3 -m pytest tools/ -q`: **125 passed** in 105.23 s. (The 126-test tally belongs to the unmerged selection-temperature branch, not to this base.)

---

## Issues

### S1. CLAIM_MAP prospect notes still say “N_e is very large” after the check found that is not established

The four pointer sentences are accurate, and the statuses are unchanged, as required. But they are appended to the existing “Qualification prospect” text, which still reads, as a present-tense judgement, that the class is “plausibly qualifiable,” that “N_e is very large,” and that “T_red comes from generation time.” The new file is the check those sentences called for, and it finds that N_e is not a single proxy (published values run from ≈500–1,700 to 10^8–10^9), that T_red is not generation time until preregistered as such, and that all five items are NOT ESTABLISHED.

A reader who stops at the CLAIM_MAP cell can take “N_e is very large” as still current. That is the opposite of what the recorded check shows. The prospect block is labelled “reviewer judgment, not a verdict,” but it is now stale.

**Fix (does not change any status, and must not become a re-score):** after the existing prospect text, or in the new pointer sentence, add a short clause that the recorded check decided items (a)–(e) all NOT ESTABLISHED, and that unique σ, N_e and T_red were not obtained. Leave P1 / P3 / P4 / P13 statuses untouched.

### N1. Orientation ε quietly treats 0.18 as σ

In §4, “Honda’s upper growth-rate cost 0.18” is inserted into ε = 10/(σ·N_e). That is a scale sketch, clearly not a qualification value, but it is the identification the file otherwise refuses (ΔJ/J = 1 for a complete motility knockout). One clarifying clause would remove the only place the file comes close to computing σ.

### N2. “The same wording is the protocol in FRAMEWORK.md §9”

It is the same protocol, not the same wording. Harmless if read charitably.

---

## Recommendations only: a concrete path to establish each item

These are not required for merge. They are the measurements or preregistered proxies that would later let the class qualify, if the evidence supports it. All of them must be locked before any re-score of P1, P3, P4 or P13.

1. **σ (item a).** Preregister (i) the units and terms of J for this class, (ii) the perturbation whose growth-rate (or competition-fitness) change will be used, and (iii) how ΔJ/J is measured for that same perturbation. Then retrieve Honda SI Fig. S2E for the condition-wise Δr/r of the *flhD* deletion, and/or Ni Datasets S1–S4 to convert 72 h coculture fractions into a selection coefficient per generation. The honest estimator is a slope near the wild-type design (a titration of *flhDC* or of flagellar investment), not a single knockout treated as ΔJ/J = 1 unless that identification is locked in advance. Do not use Schavemaker energy shares or proteome fractions as σ. Record one map, with error, and its source.

2. **N_e (item b).** Preregister, before choosing a number, which operational meaning of “independent lineages competing in the same world per redesign time” will be used, and name that world. Three live options, which are not interchangeable (Berg 1996): (i) species-wide silent-site / dN/dS N_e (Sung, Bobay, Lapierre/Hartl: order 10^8–10^9) if the world is the species’ shared environment over T_red; (ii) within-host N_e of a colonizing clone, after retrieving Ghalayini’s full text to confirm the ≈500–1,700 method, if the relevant competition is inside one host; (iii) a new census: the number of independently founded, co-circulating lineages in a named habitat over one T_red. Lock one proxy, and report the others only as sensitivity. The N_e world and the T_red world must be the same world.

3. **ε (item c).** Once unique σ and N_e are locked, compute ε = 10/(σ·N_e). If a range remains, take the largest ε (the FRAMEWORK rule that a worse measurement cannot make qualification easier). That number is then the minimum width of the prediction band.

4. **Power (item d).** Preregister the map from a fractional J-gap to a design-unit band, {𝒟 : J(𝒟) ≤ (1 + ε + δ_meas)·J*}, with H from this class’s own J (THEORY §3, “From a cost band to a design band”). Name at least one rival among R1–R3 (ECOLI-MEM already named memory = τ_v, which is R3). Show that the band plus δ_meas excludes that rival’s design. Any use of the locked ECOLI-MEM numbers for this comparison is a separately preregistered re-score, not an addendum to the present file.

5. **T_red and 10 T_red (item e).** Either measure the 1 − 1/e closing time of the motility / chemotaxis design after a documented step change in prices or in the world’s statistics (for example, experimental evolution of flagellar investment after a change in nutrient regime, fitted to the new argmin), or preregister a turnover proxy T_red = k × (a named generation time), with k fixed in advance. Name which generation time — laboratory 20 min, Gibson’s wild 15 (s.e. 7.7) h, Poulsen’s 40–80 min in mucus, or a new measurement in the habitat used for N_e — and then show that the lineage faced that same world for at least 10 T_red. Do not use the methylation-layer adaptation time (~10 s) as T_red.

---

## Conclusion

The work is a genuine pre-re-score qualification record, not a quiet relabelling of the E. coli tests. The sources check out, the five item verdicts follow the definition as written, and NOT ESTABLISHED is the right label. Fix S1 before merge; N1 and N2 are optional. Then this can merge as a literature record that leaves P1, P3, P4 and P13 untouched.
