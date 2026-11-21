# Independent hostile review: PR #127 (E. coli qualification measurement plan and computation)

**Reviewer:** independent (wrote none of this PR, the measurement plan, the result file, the QUALIFICATION literature check, CLAIM_MAP pointer notes, THEORY §3, FRAMEWORK §9, or the E. coli test package).
**Date:** Saturday 21 November 2026, started 1:50 AM ET, finished 2:07 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/127
**Clone:** fresh `/workspace/gtao-rev127` at head `62fdf24bda83c1dc30116bca9e9eb3d595eab40b` (branch `ecoli-measure-2026-11-21` / `pr127`). Stated base `75b58fec282c102efa31b57477301636c6f551fb` is exact (merge-base equals base). Current `origin/main` is `54a45629280edc9dfe0275d04eaf19626aa4523d` (PR #126 tidy, including the `tools/test_lean.py` `os.access` fix). Clean tree at review start. Nothing pushed or merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The plan is locked in its own earlier commit, before any computation under it. The later computation follows that lock: overall **NOT ESTABLISHED**, item (b) *N_e* **ESTABLISHED** (conservative 1.7960 × 10^8, Sung et al. 2016; locked-set range to 4.169 × 10^8), and (a), (c), (d), (e) **NOT ESTABLISHED**. That is not NOT QUALIFIED, and not a re-score. P1, P3, P4 and P13 statuses are unchanged. CORE.md and the law-of-adaptive-organization sentence are unchanged. Quoted numbers that could be checked against retrieved public texts, including the bioRxiv Fig. S1D rates that were reported and correctly unused, check out. DOIs re-verify on Crossref. Excluding the preprint growth rates as the qualification σ is correct under the locked source rule. The R3 power point is right, and it does mean P1/P3 as a rival-discrimination test are untestable as specified (plain statement in §5 below). The PR does not currently merge cleanly onto `54a4562`; that is a mechanical OPEN_WORK header conflict only. After a local rebase that resolved that one conflict, `check_open_work.py` and `check_consistency.py` passed, and `pytest tools/` was 129 passed. Fix M1 before merge. S1 does not change any verdict.

---

## What was checked

- Fresh clone at the stated head/base; two commits, five files (`MEASURE_PLAN_2026-11-21.md` and a QUALIFICATION landing note in `6667afd`; `MEASURE_RESULT_2026-11-21.md`, OPEN_WORK T1, and four CLAIM_MAP pointer suffixes in `62fdf24`).
- Commit order, author/committer timestamps, and `git show` / `git diff 6667afd 62fdf24 -- MEASURE_PLAN…` (the plan file is byte-identical after the lock).
- THEORY §3 operational definition of “strongly selected,” FRAMEWORK §9 items 1 and 6, FRAMEWORK §2.2 status vocabulary, QUALIFICATION_2026-11-21.md (especially §8), and DEVIATIONS.md DV2, compared to the plan’s estimators and decision rules and to every verdict in the result file.
- CLAIM_MAP P1, P3, P4, P13 status column, claim text, and historical proxy labels versus base `75b58fe` and versus current `main`. CORE.md / THEORY.md / the law sentence versus `origin/main`.
- Every DOI in the plan’s §10, plus the two added in the result (Honda bioRxiv; Plague et al. 2017), plus Rocha 2018 (already unused), re-queried on the Crossref API this review (21 November 2026).
- Independent retrieval and quoting: Sung et al. 2016 Table 1 (NCBI PMC / eutils JATS, PMC4978911); Bobay & Ochman 2018 Additional file 1 Table S1 (journal ESM xlsx); Lapierre et al. 2016 Table 2 (Europe PMC JATS, PMC4915353); Ghalayini et al. 2018 full text (PMC HTML, PMC5835743); Gibson et al. 2018 Table 1 (eutils JATS, PMC6015860); Plague et al. 2017 (eutils JATS, PMC6002858); Honda et al. 2022 main text (Europe PMC JATS, PMC9478672); Honda et al. bioRxiv PDF (2,463,587 bytes, `%PDF-1.4`, 27 pages; Fig. S1D rendered and read). Hartl 1994 and Berg 1996 full texts were again not retrieved. Honda published SI Appendix and Ni Datasets S1–S4 were sought on `pnas.org` and returned Cloudflare 403 “Just a moment…”, as the result file says. No Dryad / Figshare / SID alternative for those files was found in the published Honda JATS.
- Locked ECOLI-MEM `results.json` Arm B `tau_range` and `tau_v`.
- Mergeability against current `origin/main` `54a4562`: GitHub `mergeable: false`, `rebaseable: false`, `mergeable_state: dirty`. Local `git merge-tree` and a local rebase onto `54a4562`. Checkers and `nice -n 19 python3 -m pytest tools/ -q` after that rebase (OPEN_WORK as-of line resolved locally only, not pushed).

---

## 1. Commit order and leakage

Plan commit `6667afd9e89ec0b03cdafe070dadead4b407d37a`, AuthorDate and CommitDate Saturday 21 November 2026, 01:39:17 −0500 (“Lock E. coli qualification measurement plan before any computation”). Result commit `62fdf24bda83c1dc30116bca9e9eb3d595eab40b`, 01:49:40 −0500 (“Compute E. coli qualification under the locked measurement plan”), 10 minutes 23 seconds later. Parent of the plan commit is `75b58fe`, as stated. The second commit does not touch the plan file (`git diff 6667afd 62fdf24 -- theory/measured/ecoli/MEASURE_PLAN_2026-11-21.md` is empty). OPEN_WORK, CLAIM_MAP pointers, and the result file appear only in the later commit. The QUALIFICATION landing note is in the plan commit and does not record computed values.

The plan already contains numbers that were on record before this lock: Honda’s main-text “up to 18%”; Sung *N_e* = 1.7960 × 10^8, Bobay 416,911,778.112 and 374,704,250.0, Lapierre/Hartl attribution 1.8 × 10^8; locked Arm B τ\* ∈ [1.093, 1.171] s and τ_v = 1.160 s. Those are disclosed in the plan’s “Already seen” preamble, taken from the 21 November qualification check and from locked `results.json`. They are not results of the later computation. The plan does not contain the later-computed material: bioRxiv / 10.1101/2021.05.12.443892, Fig. S1D, the printed rates 0.49/0.58, 0.66/0.76, 0.89/0.97, Cloudflare 403, or Plague et al. 2017. No verdict from the computation is written back into the lock.

The header times (“about 1:40 AM ET” on the plan, “about 1:50 AM ET” on the result) are consistent with the commit stamps. The “before any computation under this plan” claim holds on this branch.

---

## 2. Estimators and qualification rule versus FRAMEWORK §9 / QUALIFICATION §8

The plan turns QUALIFICATION §8’s recommended path into locked estimators, and it does so before the computation. The five-item rule, the vocabulary (ESTABLISHED / NOT ESTABLISHED / FAILS), and the overall QUALIFIED / NOT QUALIFIED / NOT ESTABLISHED rule match THEORY §3 and FRAMEWORK §9 item 1. A class that is not shown to qualify “is not evidence either way.” Energy-budget and proteome shares are excluded from σ. Conservative choices run in the direction the framework requires (smallest positive σ, minimum *N_e*, largest ε, largest *k*, slower *T*_gen): a worse measurement cannot make qualification easier.

Item (b) moving from NOT ESTABLISHED in the 21 November literature check to ESTABLISHED here is not a silent loosening of that earlier file. QUALIFICATION left (b) unset because the world and the proxy had not been locked. The plan locks them first: the world is the species’ shared natural environment over one redesign time, and the proxy is published Lynch-style species-wide silent-site or dN/dS *N_e*. Within-host Ghalayini values remain sensitivity only and are not used to shrink ε. That is one of the three options QUALIFICATION §8 named, chosen on the grounds that the class and the drift-barrier formula are species-level, and explicitly “not locked because it is large.” The already-known sizes of those published numbers are disclosed. The historical QUALIFICATION verdicts are not rewritten; a landing note only points at the new plan.

Identification I1 (complete *flhD* / *flhC* deletion as Δ*J*/*J* = 1) is locked in advance, as §8 required, and was not applied, because the published fallback data were not retrieved. *k* is not set to 1 and is not taken from a 1/*N_e* fixation time. The compared statistic is per-cell values (DV2), named before the computation. Re-score of P1, P3, P4 and P13 is forbidden on this branch and remains forbidden unless a later, separate PR finds all five items ESTABLISHED.

No post-hoc loosening of a decision rule after seeing the computation is visible. One internal tension in the locked power rule is noted as S1; the computation’s current (d) label still follows a clause that was already in the lock.

---

## 3. Source tracing and Crossref

All 15 plan DOIs, the two result-only DOIs, and Rocha 2018 (unused) resolve on Crossref this review. Authors, title, year, journal, volume, and article or page numbers match the files. Ni et al.’s Crossref issued year is 2019 (online 23 December 2019; print 7 January 2020, volume 117 issue 1), as the result already notes. Honda bioRxiv is Crossref type `posted-content`, issued 12 May 2021. Mori et al. 2021 is again Crossref article-number `MSB20209536` / journal elocation `e9536`; cited only as not-σ.

**Sung et al. 2016, Table 1, row *Escherichia coli* (Ec).** Headers: θ_s or π_s; *N_e* (× 10^6); *u*_bs (× 10^−10 events per site per generation). Values: θ_s = 0.071, *u*_bs = 2.00 with footnote e = Lee et al. (2012), *N_e* × 10^6 = 179.60, i.e. 1.7960 × 10^8. Pages 2583–2591 confirmed in the JATS. The paper sets θ_s = 2 *N_e* *u*_bs in haploids; 2 × 179.60 × 10^6 × 2.00 × 10^−10 = 0.07184, reported as 0.071. The result uses the table’s *N_e*, not a recomputed one.

**Bobay & Ochman 2018, Additional file 1 Table S1, row *Escherichia coli*.** 400 strains; lifestyle “commensal”; column J (universal-gene *N_e*) = 416911778.112; column O (core-gene *N_e*) = 374704250.0. Exact match.

**Lapierre et al. 2016, Table 2.** “Effective population size (N_e)  1.8 × 10^8  Hartl et al. (1994).” Text: “The effective population size of the species is estimated at >10^8 (Hartl et al. 1994; Lynch 2006).” Hartl’s own full text was again not retrieved (PMC HTML is front matter plus a “PDF (799.1 KB)” link; the PDF URLs returned challenge or interstitial HTML, not a PDF). The 1.8 × 10^8 figure is used only as Lapierre’s attribution, as locked. It is not accepted here as a number read from Hartl.

**Conservative *N_e* and range.** Locked set {1.7960 × 10^8, 416,911,778.112, 374,704,250.0, 1.8 × 10^8}. Minimum 1.7960 × 10^8 (Sung). Maximum 4.169 × 10^8 (Bobay universal). Median of the four values: (1.8 × 10^8 + 3.747 × 10^8) / 2 = 2.7735 × 10^8, reported as 2.774 × 10^8. Correct. The result reports min, max, and median, as the plan’s uncertainty table required.

**Ghalayini et al. 2018**, sensitivity only. Full text confirms the official abstract and the method: Watterson’s θ_w from chromosomal point polymorphisms; θ_w = 2 *N_e* *L* μ_g; θ_w = 1.93 ± 1.13, 1.54 ± 0.96, and 1.15 ± 0.78 at days 0, 211 and 315; μ_g from 0.89 × 10^−10 to 3.12 × 10^−10 per base per generation; “we estimated a range of effective population size (N_e) between 500 and 1,700”; “equivalent to an idealized population of constant size N_e of ≈500 to 1,700 individuals”; one dominant clone (ED1a) in one healthy human gut. Quoted faithfully. Not used as the locked proxy.

**Honda et al. 2022** main text: “increased growth rate by up to 18% compared to the WT strain,” citing SI Appendix Fig. S2E. Confirmed. The published SI PDF was not retrieved (publisher 403), so condition-wise published values remain unread.

**Honda bioRxiv PDF** (doi 10.1101/2021.05.12.443892): size, PDF version, and page count match the result exactly. The Fig. S1D caption is verbatim as quoted. The figure itself prints, under the three bars:

- mannose: WT 0.49 /hr, flhD− 0.58 /hr
- fructose: WT 0.66 /hr, flhD− 0.76 /hr
- glucose: WT 0.89 /hr, flhD− 0.97 /hr

σ_fd = (r_KO − r_WT) / r_WT: 0.09/0.49 = 0.18367… (reported 0.184), 0.10/0.66 = 0.1515… (0.152), 0.08/0.89 = 0.089887… (0.0899). Correct at the precision of the printed two-decimal rates. The measurements are two-repeat averages, as the caption says; no printed standard deviation.

**Gibson et al. 2018, Table 1**, *E. coli*: DT (h) (s.e.) = 15 (7.7); laboratory DT = 0.33 h. Conservative *T*_gen = 15 + 2 × 7.7 = 30.4 h is correctly computed and, as locked, unused without a *k*.

**Plague et al. 2017:** 4,000-generation shaking-culture experiment; a 274 bp deletion inactivating *flhDC* “uncovered [in] generation 303, when it comprised 2% of the population, and it became fixed by generation 1305”; “From generation 303 to 1200, the wildtype’s fitness was 0.991 relative to the mutant, so this mutation conferred ~1% fitness advantage.” Quotes check out. Correctly not used as *k* or as E1: it is a fixation trajectory of one knockout allele, not a 1 − 1/e, half-change, or fitted closing time of the class’s typical design after a step.

**Locked τ\* box and τ_v**, from `theory/measured/ecoli/results.json`: Arm B `tau_range` = [1.0931927432524053, 1.1711376350471687], reported as [1.093, 1.171] s; `tau_v` = 1.160092807424594, reported as 1.160 s. 1.1600928 lies inside [1.0931927, 1.1711376] even at full precision. The R3 screen is therefore right at ε = 0.

No number used as a qualification value was accepted from an unverifiable source. The only second-hand figure in the locked *N_e* set is Lapierre’s attribution of Hartl, labelled as such; the conservative minimum does not depend on it (Sung is smaller and was read from the paper).

---

## 4. Excluding the bioRxiv growth rates

Correct under the lock.

The locked Honda source for estimator B is “SI Appendix Fig. S2E or … any public SID / source-data file of this paper.” The additional-source search may add “a published paper or its public supplement,” not a preprint. Fig. S1D is the submitted version’s panel, with different numbering from the published S2E, and it is not a SID file of the PNAS paper. The plan’s NOT ESTABLISHED rule for (a) already names the case that “Honda SI Fig. S2E and Ni Datasets S1–S4 remain unavailable, so that only the main-text upper bound ‘up to 18%’ is on record.”

Reporting the printed rates and then not using them as conservative σ is the right behaviour: the numbers are not hidden, and they are not promoted into the qualification value. Reason (i) is the lock. Reason (ii) — that the three carbons in S1D are not established as the lower end of the published condition set, so using 0.0899 would risk a σ that is too large and an ε that is too small — is conservative and is supported by the preprint’s own main text (aspartate and rich conditions are discussed; S1D shows only mannose, fructose, and glucose). Calling both reasons “written into the lock” slightly overstates (ii); the lock requires a conservative lower end of a retrieved published range, and it does not mention aspartate by name. That is wording, not a verdict error.

A complete *flhDC* titration with numeric growth rates near wild type was also not obtained as numbers (the preprint titration reports swimming speed, motile fraction, and flagellar number). Estimator A is correctly unused.

---

## 5. The R3 power point, plainly

The arithmetic is right: the locked rival R3, τ_v = 1.160 s, already sits inside the locked Arm B prediction τ\* ∈ [1.093, 1.171] s. A positive ε can only widen the band. R3 cannot be excluded at ε = 0. R1, R2, and the P4 one-store rival were not scorable without inventing a price or a mapping (no *J*(one-store) versus *J*(two-store) comparison is sitting in the locked ECOLI-MEM / LAYERS files as a ready design-unit gap for this class). The result therefore leaves (d) **NOT ESTABLISHED**, not FAILS, citing both that (c) is not established and that no other rival was scorable. That follows the plan’s more specific NOT ESTABLISHED clause. It is not a re-score of measured τ2 = 9.9 s, which was not used.

What this means, plainly: **P1 and P3, as a test that the theory’s memory-time prediction excludes the “set at the world’s time scale” rival, are untestable as specified.** The theory’s own locked box already contains the rival’s point. No later band can separate them. A later comparison of measured τ2 to the τ\* box is a different question (data versus the box, not box versus R3), and it is not allowed until the class is QUALIFIED. Under this plan, qualification itself requires power against a named rival. With R3 undiscriminating and no other rival scorable, item (d) is on course to **FAIL** once σ and ε are eventually established, and the class would then be **NOT QUALIFIED**. In that sense P1 and P3 remain effectively NOT A TEST as specified, unless a later lock finds another scorable rival that the band can exclude.

The result already states that R3 cannot be excluded at ε = 0. It should say the implication above equally plainly (S1). The current overall label, NOT ESTABLISHED rather than NOT QUALIFIED, should stand: (c) is not established, and the plan’s FAILS clause for (d) is in tension with its NOT ESTABLISHED clause (see S1). This review does not flip (d) to FAILS on that wording collision.

---

## 6. No re-score, no status change, no overclaim

CLAIM_MAP changes are four identical pointer suffixes on P1, P3, P4 and P13 only. Status column, claim text, and historical proxy labels are byte-identical to base `75b58fe` and to current `main`:

- P1: **NOT A TEST (qualification not established; proxy: failed)**
- P3: **NOT A TEST (qualification not established; proxy: failed)**
- P4: **NOT A TEST (qualification not established; proxy: passed)**
- P13: **NOT A TEST (qualification not established; proxy: failed)**

CORE.md and THEORY.md have no diff versus `origin/main`. The law sentence is unchanged: “The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.” QUALIFICATION_2026-11-21.md’s item verdicts are not rewritten; the file only gains a landing note. The result does not call the class QUALIFIED or NOT QUALIFIED, does not compute a qualification ε from 0.18 or 0.0899, and does not treat the computation as a test of P1, P3, P4 or P13. That is the right level of claim.

---

## 7. Mergeability, rebase, checkers, and tests

GitHub reports `mergeable: false`, `rebaseable: false`, `mergeable_state: dirty`. Local `git merge-tree` against `54a4562` shows one real conflict: `OPEN_WORK.md` (the **As of** line). `QUALIFICATION_2026-11-21.md` is changed on both sides but merges cleanly (main’s PR #122 wording tidy is in a different place from this PR’s landing note). CLAIM_MAP, the plan, and the result have no conflict.

A local rebase of the two PR commits onto `54a4562` confirmed that: commit `6667afd` applied cleanly; commit `62fdf24` conflicted only in the OPEN_WORK as-of header. T1 from this PR is the right text (main did not change T1). After resolving that header locally (not pushed), `python3 tools/check_open_work.py` PASSED, `python3 tools/check_consistency.py` PASSED (0 FAILs; the usual soft length WARNs on THEORY.md and README.md), and `nice -n 19 python3 -m pytest tools/ -q` was **129 passed**. The `test_lean.py` `os.access` failure present on `75b58fe` is gone once the branch carries `54a4562`.

M1 is therefore mechanical and is required before merge.

---

## Issues

### M1. The PR does not merge or rebase cleanly onto current main (`54a4562`)

Only `OPEN_WORK.md` conflicts, and only in the as-of paragraph. Main at `54a4562` records the PR #125 blind confirm (`reviews/sim1_2026-11-21/CONFIRM2.md`) and the `test_lean` fix; this PR’s as-of still says `main` is `75b58fe` and omits that confirm. T1 should stay this PR’s text (plan locked, computation recorded, (b) ESTABLISHED, (a)/(c)/(d)/(e) not, no re-score).

**Fix (no result or status change):** rebase or merge onto `54a4562` and write one as-of line that includes both the measurement (`6667afd` / `MEASURE_RESULT_2026-11-21.md`) and PR #126. Then re-run the two checkers and `pytest tools/`. This review already did that locally; 129 passed.

### S1. Plan §4.4’s FAILS and NOT ESTABLISHED clauses collide, and the result should say plainly that P1/P3 cannot discriminate R3

§4.4 says (d) is NOT ESTABLISHED “if no named rival is scorable … (including the case that R3 cannot be excluded and no other rival can be scored without inventing a price or a mapping).” It also says (d) FAILS “if every scorable named rival’s design lies inside the design-unit band,” and that the R3 screen “becomes a FAILS only if no other scorable rival is excluded.” After a search that finds no other scorable rival, those sentences point both ways.

The computation followed the more specific NOT ESTABLISHED clause, and (c) is in any case not established, so the overall verdict should remain NOT ESTABLISHED. Do not “fix” this by declaring the class NOT QUALIFIED on this branch.

**Fix (post-result housekeeping; no official verdict change):** tighten §4.4 so the R3-undiscriminating, no-other-rival-scorable case is labelled one thing, and state in the result (and, briefly, in OPEN_WORK T1 if it will still fit) that P1/P3 as a rival-discrimination test are untestable as specified, and that once ε is established (d) will FAIL unless another scorable rival is excluded.

---

## Conclusion

The lock-then-compute order is real, the estimators match the definition, the sourced numbers check out, the bioRxiv rates were rightly kept out of σ, and the claim level is honest. The R3 overlap is correctly computed and has a sharper consequence than the result quite says: P1 and P3 cannot, as specified, tell the theory’s memory-time prediction from the world’s-time-scale rival, and without another scorable rival the class will not qualify through this plan once ε exists. Rebase onto `54a4562` (M1), tighten the §4.4 wording and say that consequence plainly (S1), and this can merge as a computation under a lock that still leaves P1, P3, P4 and P13 untouched.
