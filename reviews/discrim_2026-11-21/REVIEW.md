# Independent hostile review: PR #129 (discriminating-candidates shortlist)

**Reviewer:** independent (wrote none of the PR, `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md`, the OPEN_WORK T29 row, or the VIS-1F outline).
**Date:** Saturday 21 November 2026, started 2:47 AM ET, finished 3:00 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/129
**Clone:** fresh `/tmp/rev129/repo` at head `2a154a3f9cee4b9b32ba475020c79efa8d077e91` (branch `discrim-2026-11-21`), merge-base `ac079ea0b2724cec34f30d83e3b3c551c6877c07`. `origin/main` at review is `ecf6e77172797585bf199e184bf19997455bd094` (PR #128 merged 2:34:20 AM ET). Clean tree at review start. Nothing pushed or merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

This is an unlocked shortlist and a draft outline, not a lock, and it does not re-score P1, P3, P4, P13, P25, or any other locked row. CORE.md and the law-of-adaptive-organization sentence are unchanged. The note is mostly careful about collapses, about E. coli P1/P3 already containing R3, and about not locking until a precomputed gap exists. That stance is the right one.

It is not mergeable onto current main as it stands: OPEN_WORK.md conflicts with the already-merged PR #128 (M1). In the scientific content, the top candidate's "fetched world facts" misidentify the species of van Hateren's intensity series (M2). Those two should be fixed before merge. The CT12 1/α arm is derived in THEORY, and it does differ from R2 when α ≠ 2, but it is the wrong theorem class for continuous dipteran filtering, and the fetched spectrum is likely at or outside the proved α range (S1). The Pass 1 gate is the right idea and is not yet operationally specified (S2).

---

## What was checked

- Fresh clone at the stated head/base; diff `ac079ea..2a154a3` (one commit, 2 files, +192 / −1): new `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md` and OPEN_WORK T29 plus an as-of rewrite.
- Mergeability against `origin/main` `ecf6e77`: `git merge-tree` and `git rebase origin/main` both conflict, only in `OPEN_WORK.md`. The new theory file applies cleanly. A local test rebase (not pushed) resolved OPEN_WORK by keeping main's W14 / T3 GRID-CROSS rows, inserting T29, and updating the as-of line, then ran checkers and pytest.
- Every DOI in §6 queried on `https://api.crossref.org/works/{doi}` this session; all 17 returned a works record. Public full texts were opened where a no-account URL worked. Quoted numbers were checked against those files and against the current tree (Sung Table 1, MEASURE_RESULT, THEORY B.3 / B.4, MASTER_EQUATION, SN1_RESULTS, FRAMEWORK §9). Unverifiable items are flagged below.
- CT12 derivation and premises in THEORY.md Appendix B.3; comparison to R2 (FRAMEWORK §9 item 6), to Lemma B2 continuous-sensing elasticities, and to van Hateren / Atick / Laughlin efficient-coding statements in the 1997 paper and the surrounding literature.
- Ranking honesty, collapsed-class list, and a short look through TESTBEDS, QUEUE, BIO1/SN1, and the vision prior art for a missed stronger candidate.
- *D. melanogaster* qualification against FRAMEWORK §9 and the draft VIS-1F outline, including whether the Pass 1 gate and its error band are well-defined.
- CORE.md / law sentence / re-score: `CORE.md` blob is identical on `pr129`, `ac079ea`, and `ecf6e77`. The two-file diff does not touch CORE.md, THEORY.md, CLAIM_MAP, or any locked results file.
- After the local rebase: `python3 tools/check_open_work.py` PASS; `python3 tools/check_consistency.py` PASS (0 FAIL; the new note is a frozen dated record; "law of adaptive organization (hypothesis)" is allowed by the hypothesis exception). `python3 -m pytest tools/ -q --ignore=tools/test_lean.py`: 144 passed. `test_lean_sources_have_no_sorry`: 1 passed, 1 deselected. Full Lean compile was not re-run, to avoid filling the disk; that matches recent reviews. 144 + the two Lean tests would be 146, consistent with main after PR #128.

---

## 1. Mergeability

The branch was cut from `ac079ea` (PR #127) and was not rebased onto the already-merged PR #128. PR #128 landed on main at 2:34:20 AM ET; this commit is dated 2:46:39 AM ET, twelve minutes later, and still calls PR #128 "open" and `main` `ac079ea`. The only conflict is OPEN_WORK.md (as-of line, plus main's W14 GRID-CROSS row and the updated T3 text, versus this branch's T29 row). The shortlist file itself has no conflict.

A purely mechanical merge that dropped W14 or reverted T3 would be a regression. The fix is a rebase that keeps the GRID-CROSS rows, adds T29, and restates that `main` is `ecf6e77` and that PR #128 is merged, official comparison not run, P25 still UNTESTED. Checkers and pytest pass on that resolution (this review's local test rebase only).

---

## 2. Numbers and citations

All 17 listed DOIs resolve on Crossref. Issued years in the table match Crossref's `issued` date (including Juusola issued 2000-12-12 / print 2001-01-01, and Ni issued 2019-12-23 / print 2020-01-07, which the note already distinguishes). Byte sizes that could be re-fetched this session match the table exactly:

| Source | Claimed | This session |
|---|---:|---:|
| van Hateren 1997 author PDF (Groningen `pure.rug.nl` …/1997VisionResvHateren.pdf) | 1,201,248 | 1,201,248 |
| Mora & Nemenman arXiv 1908.04057 | 467,938 | 467,938 |
| Mayer et al. arXiv 1511.08836 | 1,055,586 | 1,055,586 |
| Zi, Liebermeister & Klipp 2010 PLOS PDF | 1,709,329 | 1,709,329 |
| Lisevich et al. 2025 publisher PDF | 1,631,945 | 1,631,945 |
| Ni 2020 Europe PMC XML PMC6955288 | 112,913 | 112,913 |
| Honda 2022 Europe PMC XML PMC9478672 | 137,351 | 137,351 |
| Sung 2016 Europe PMC XML PMC4978911 | 156,410 | 156,410 (from the same Europe PMC URL, already on the machine and re-checked) |

**Sung et al. 2016, Table 1, N_e in units of 10^6.** Every printed value in the shortlist table matches the XML of Table 1, including *D. melanogaster* 0.86 (8.6 × 10^5) and *E. coli* 179.60 (1.7960 × 10^8). The note's table is a subset: it omits *Mesoplasma florum* (1.07), *Arabidopsis thaliana* (0.29), and *Mus musculus* (1.77) without saying so (Nit). Large N_e is correctly not treated as qualification.

**E. coli τ\* box.** Locked Arm B τ\* ∈ [1.093, 1.171] s and R3 τ_v = 1.160 s are exactly as in `MEASURE_RESULT_2026-11-21.md`. Honda SI and Ni datasets returning HTTP 403 was reproduced for a Ni SI PDF URL.

**van Hateren 1997 quotes that check.** "20.48 sec" sections of a "45 minute stretch"; "γ here close to 1"; "for frequencies lower than 0.1-1 Hz, the power spectra deviate somewhat from a strict power-law behaviour"; "Part of this adaptation is very fast, with a significant change in gain within a few tens of milliseconds."; "The power spectra for the LMC (traces c and d) do not follow the 1/f^γ behaviour: these spectra become almost flat"; intensity and photoreceptor spectra still show 1/f behaviour. "Low-pass limited to 100 Hz" is also in the Methods ("data were low-pass filtered to 100 Hz (by block averaging)").

**van Hateren 1997 fact that does not check (M2).** The intensity *time series* were not "from the blowfly." They were measured with an optical device "worn on a headband by a freely walking person," with a field of view "comparable with … single human foveal cones," then "presented to the visual system of the blowfly (*Calliphora vicina*) by playing them back … on a [LED]." The paper says explicitly that fly-in-habitat series would be ideal and were not obtained with sufficient accuracy, and that the human series are only "expected to be roughly equivalent" (with listed differences in acceptance angle, speed, and object distance). The note's disclosure, "the natural-scene measurements fetched below are from the blowfly, not from *Drosophila*," is therefore wrong in the first clause. The mismatch is three-way: human-walking world, *Calliphora* responses, *D. melanogaster* N_e. "Photoreceptors and LMCs of flying Diptera, acting in natural light-intensity time series" overstates what was measured.

**Ni 2020, Honda 2022, Mora 2019, Hog1 2010.** The quoted phrases that could be opened check, including Ni's "investment in motility in proportion to the reproductive fitness advantage…," "occurs even when nutrient gradients are absent," WT "almost twice as fast as Δ*cheY*" on ribose, "no significant difference" on glucose, and signaling cost "negligible compared to the overall cellular energy budget" in stirred culture; Honda's ∼4.4-fold change, "compensate for reduction in cell size," flagella per cell "nearly independent of growth rate," and "increased growth rate by up to 18%"; Mora's geometric random walk with time τ, δc/c ∼ (Dacτ)^{−1/4} "in stark contrast with" Berg–Purcell (DacT)^{−1/2}, and a network that "adapts the kinetics of signaling as a function of the square root of the sensed concentration"; Zi et al. "activation time … about 1 min" and periodic square pulses. Lisevich's rich-medium saturation and below-maximal expression in minimal / carbon-limited growth are fairly paraphrased ("tracks carbon quality / benefit" is a smoothing of "might correlate with the potential benefit" / poor carbon sources).

**Wording error (S4).** "the Δ*cheY* advantage vanished in stirred culture" reads as if the mutant had the advantage. The paper's finding is the opposite: a WT (chemotaxis) advantage on ribose that vanishes when the culture is stirred. Surrounding sentences are correct; the phrase should be repaired.

**Honda 4.4-fold (Nit).** The note attributes the 4.4-fold figure to "the preprint." The same ∼4.4-fold statement is in the published 2022 XML that this session (and the note) fetched. The published SI Fig. S2E is cited in the main text for the 18% claim; the main-text number is still sourced.

**Not re-opened this session, so not independently re-verified:**

- Honda bioRxiv PDF (claimed 2,463,587 bytes): 429 / 403 from biorxiv.org.
- Dornhaus et al. 2006 author PDF (claimed 338,189 bytes): OUP article-PDF 403; Unpaywall `is_oa` false, no OA location. Crossref has no abstract. The "no significant effect" of colony size was not checked in a file this review could open.
- Beekman, Sumpter & Ratnieks 2001 full text: PMC HTML is now a reCAPTCHA wall; Europe PMC XML returned HTTP 500 (the table's "Europe PMC XML 500" is almost certainly that status, and should be written as such); publisher PDFs 403. Crossref abstract confirms a first-order, hysteretic transition from disordered to organized foraging in small versus larger colonies, but does *not* contain "600" or "0.0052." Those two numbers are therefore unverified here (S5). They should not be used as if re-checked until a copy is opened again.
- Juusola & Hardie full text: publisher PDF 403, as the note says. The 50 → 10 ms bump-duration figure is correctly located in `theory/measured/SN1_RESULTS.md` and was not re-extracted. SN1's INVALID / exogenous photon-shot-noise reading for *Drosophila* is accurately cited; calling that "Model S" is a fair inference, not a quote from SN1.

**Internal math that checks.** N\*(ρ) = (√(1+ρ)+1)²/ρ at ρ = 1 is ≈ 5.83 (the note's 5.8). The small-ρ sketch 4/ρ ≈ 600 ⇒ ρ ≈ 0.007 is arithmetic, and the note correctly refuses to treat it as a prediction or a miss. The 7–15× "faster than the mode" range is the slow-store band 90/11.9 to 90/6.2 from `meq_roots.out` / the MASTER_EQUATION §1a table (0.16–2.6 and 6.2–11.9 days); §2's worked point is 1.5 and 6.9 days, so the "§2" pointer is slightly loose (Nit). CT12's "σ^{−2/α} in the usual scaling" matches T\* ∝ (c/(w q))^{1/α} with q written as σ², as already in TESTBEDS.

Unlisted but named works (Atick & Redlich 1990, Fairhall et al. 2001, Wark et al. 2009, Barro 1972, Dixit 1991, Senders 1964, Sims 2003, Muth 1960, Harris 1913, Tjalma & ten Wolde 2024) are used as already-in-the-repo pointers, not as newly fetched numbered claims. That is acceptable for a shortlist, except for the vision prior-art gap in S3.

---

## 3. Is CT12's 1/α actually derived, and does it really differ from R2 and from whitening?

**Derived, with an explicit line.** THEORY.md Appendix B.3, *Setting for CT12–CT13* and **CT12 (the read-rate rule)**, lines 335–339:

> A drifting world (W-b): Gaussian with stationary increments, E(X_{t+τ} − X_t)² = q·τ^{α−1}, **1 < α < 3**. Exact reads at price c that reset the copy; the last value is held in between; squared-error loss at stake w.
>
> The optimal read interval is T\* = [α·c/((α − 1)·w·q)]^{1/α}, so the read rate is ∝ (w·q/c)^{1/α} … stakes and drift elasticities a = b = 1/α.

The proof is the one-line convex minimization of J(T) = c/T + w·q·T^{α−1}/α. The main-text table (line 87) and the prediction table (line 164) restate it. MASTER_EQUATION.md §1a reports numerical T\* to 6 digits at α = 1.3, 1.6, 2, 2.5, 2.9, so "numerical checks start at α = 1.3" is true, but that is not the proved interval. The proved open interval is 1 < α < 3. The note slightly conflates the two.

**It differs from R2 when, and only when, α ≠ 2.** R2 is "every read interval ∝ the world's time scale with exponent ½" (FRAMEWORK §9 item 6). At α = 2, CT12 is T\* = √(2c/(w σ²)), which THEORY already credits as Harris 1913 / Reis 2006, and TESTBEDS already flags as prior art (Barro, Dixit, Senders, Sims). Mora & Nemenman 2019 is correctly treated as the α = 2 sensing case already on the record. Candidate 3's 1/α = 0.667 or 0.400 versus 0.500, at locked α = 1.5 or 2.5, is the right contrast *for a discrete exact-reset read rate*. That does not automatically transfer to candidate 1.

**It does not, by itself, differ from van Hateren / Atick whitening.** Those predictions are about a continuous transfer function: given a natural spectrum and SNR, the filter should whiten the output at high SNR and become more low-pass as SNR falls (Atick & Redlich 1990, 1992; van Hateren 1992a, cited inside the 1997 paper; Laughlin 1981 on static contrast coding). CT12 is about how often to take a costly exact reset read. Filter *shape* agreeing with whitening is, as the note itself says, a collapse into efficient coding, not a pass for the hypothesis. No numerical cutoff or K\* gap versus whitening was computed. That honesty is appropriate. The remaining distinctive content, if any, has to come from a priced discrete upkeep h (or a declared structural claim) moving the cutoff or the layer count away from the SNR-whitening design. Until that is computed, candidate 1 is a hope, not a shown discriminator.

**Two further problems with advertising CT12 as the VIS-1F arm (S1).**

1. *Wrong theorem class.* Dipteran photoreceptors and LMCs are continuous analogue filters, not exact reset reads with hold-last-value. THEORY Lemma B2 (line 347) already gives a different continuous-sensing scaling: precision effort with a linear price ∝ w^{α/(2α−1)} q^{1/(2α−1)}, and memory time ∝ (σ_n²/q)^{1/α}. At α = 2 that elasticity is 2/3, not R2's ½ and not CT12's ½. A VIS-1F elasticity arm should say which theorem is in force, and should not default to 1/α unless a discrete read is operationalized.
2. *α likely out of range.* For a process with PSD ∝ 1/f^γ, the structure function scales as E(ΔX)² ∝ τ^{γ−1} (with a logarithmic special case at γ = 1). Mapping onto E(ΔX)² = q τ^{α−1} gives α = γ. Van Hateren has γ "close to 1." CT12 requires 1 < α < 3 and has no interior minimum at α = 1 (the error term becomes age-independent, and (α−1) in the denominator of T\* blows up). The note flags that the spectrum "may be *too close to α = 1* to sit inside CT12's proved range" and says the CT12 arm is dropped if α ≤ 1 or outside a later premise interval. That flag is right and is in tension with ranking this system as the place to test 1/α versus ½.

THEORY L3 / CT21 (line 81) is also on point and is under-used: "A continuum of time scales has no exact finite design (L3)." A near-1/f world may not furnish a finite K\* at all. Interlacing (L2) is already correctly restricted to a full-rank Model S optimum with separated real modes. The distinctive GTAO object for this system, if there is one, is a priced deviation of cutoff or count from whitening, not CT12 and not a default finite K\*.

---

## 4. Is the ranking honest? Are the 'collapsed' verdicts right? Was a stronger candidate missed?

The ranking rule (distinctive prediction, then a pre-lock gap, then qualification prospect, then fetched data) is the right order, and it is mostly applied honestly. The collapsed list in §3 is blunt in the right places:

- "Memory tracks the world's time scale" is R3 / BIO1 prior art, and E. coli P1/P3 is the cautionary case. Right.
- Immune lifetime versus drift is BIO1-contradicted and Mayer et al. 2016 prior art. Right not to revive T8 as a distinctive test.
- Whole-proteome allocation collapsing into Scott et al. 2010; motility investment already stated by Ni 2020 (with Honda and Lisevich occupying the same ground); sensory slope ≈ 1 already called non-discriminating in BIO1. Right.
- Grids / GRID-CROSS as a gradient diagnostic, not a hypothesis test, with P25 UNTESTED. Right, and consistent with the PR #128 review.
- N51 cheap but not a qualifying class. Right.
- SN1 still 0/7 scorable. Right.

Candidate 2's "high risk of collapse" into Ni, and candidate 4's warning that comparing Beekman's worker-count 600 to GTAO's N\*(ρ) is a category error, are both the correct hostile readings. Candidate 5's Kalman / Wiener collapse risk is also already in THEORY §10. Candidate 3 is correctly ranked below 1 because no qualifying public (α, rates, prices) dataset was fetched.

The generosity is in putting candidate 1 first. By the stated criterion (i)–(ii), a GTAO prediction that a named rival does not already make has *not* been shown for this system, and no gap has been computed. The note says that. What 1 uniquely has, this session, is a fetched non-OU spectrum and an exogenous-noise (Model S) reading already on the record. That is a reason to *attempt Pass 1*, not a reason to imply that 1/α versus ½ is already in reach. The recommendation "do not lock tonight" and "if Pass 1 finds no gap, do not lock" saves the ranking from being a misleading claim. After M2, the fetched spectrum is also a human-walking spectrum, which further weakens "best next field class."

**TESTBEDS items not disposed (S6 / Nit).** The intro says TESTBEDS was searched. Grids, inventory, and N51-like lab tasks are handled. TESTBEDS #2 (learning rate vs volatility; Behrens / Nassar), #3 (central-bank calendars), and #6 (weather-forecast cycles) are not explicitly retired in §3. None looks like a stronger *hypothesis* test (#2 and #3 are weak on qualification or collapse into prior art; #6 has open spectra but unpriced error and no class N_e). They should still be named and dropped, or the "searched TESTBEDS" claim is slightly incomplete.

No clearly stronger public-data, plausibly qualifying, already-discriminating candidate jumped out of the repo or a short look at the literature. Fly early vision is the classic efficient-coding testbed, which is why the collapse risk is high and why Pass 1 is mandatory. *Chlamydomonas* (Sung N_e = 4.331 × 10^7) and *C. elegans* are in the Sung table and have sensory literature; they were reasonably not shortlisted without a fetched distinctive prediction and a spectrum. I would not swap the top pick for them on what was opened here.

---

## 5. Does the *D. melanogaster* qualification case stand, and is the Pass 1 gate well-defined?

**N_e stands as a sourced species-wide number, and nothing else does.** 0.86 × 10^6 from Sung Table 1 is correctly read. σ and T_red are correctly reported as missing. "The class is **not shown to qualify**" is the right verdict. "A result on this system can test the *filter/layer prediction* in a plausibly selected organ; it becomes a test of the hypothesis only after (a)–(e) are recorded" is consistent with FRAMEWORK §9 and CORE.md §7 ("No system has yet been shown to qualify"). The draft's refusal to argue 10 T_red from a general impression that "vision is old" is also right.

Calling 0.86 × 10^6 a "conservative" default needs a direction: a smaller N_e *widens* ε = 10/(σ·N_e), which is conservative for a kill and anti-conservative for a pass. Other *D. melanogaster* N_e estimates in the literature are often of the same order or larger; the draft should say "Sung Table 1 default, replaced if a sourced visual-lineage or species-wide estimate is smaller" and not lean on "conservative" without that.

After M2, using *Drosophila* N_e to qualify a test whose world series are human-walking and whose kernels would start from *Calliphora* is weaker than the already-intended blowfly / *Drosophila* split. The outline already says the species split is a listed limitation and that a miss in a class not shown to qualify is not a field kill. That language should be extended to the human world source.

**The gate is the right idea and is not yet well-defined (S2).** The lesson ("do not lock unless, before lock, both designs are computed on the same quantity and at least one rival lies outside the pre-written measurement-error band") is exactly what E. coli P1/P3 failed, and it should stay. Gaps:

- The error band is said to be "pre-written" but is not written, and the outline does not require it to be written *before Pass 1 computation begins*. If Pass 1 both fits γ and then inspects gaps, a band chosen after seeing the traces is circular. The band rule (coverage, how error in γ, kernels, and prices propagates into design units) needs to be on the page before digitizing or fitting.
- The γ → α map is promised ("with the mapping written down") and is not written. It matters, because α ≈ γ ≈ 1 is the boundary of CT12.
- Predicted K\* or cutoff "under a price rule that uses only independently sourced or preregistered (h, w) or a declared price-free structural claim" leaves a loophole. Without sourced (h, w), and given L3, a "price-free structural claim" can be made to fit. The price rule, or an explicit statement that Pass 1 will stop if (h, w) cannot be sourced independently of the design, should be fixed before Pass 1.
- Qualification item (d) "decided only after Pass 1" is fine; item (e) T_red before Pass 2 is fine; FRAMEWORK §9 item 8 is correctly flagged as a placeholder that must be finalized before any K count.

For an unlocked draft, these are should-fix items, not a reason to withhold the shortlist, provided no one treats the outline as ready to lock.

---

## 6. Overclaim, re-score, CORE.md, law sentence

No overclaim of a locked gap, of qualification, or of a field result. "This is **not** a locked gap," "no numerical gap was computed," "not a lock," and "No prediction in this file is registered" are all kept. P1, P3, P4, P13, P25, SN1, and BIO1 are not re-scored. CORE.md is bit-identical to main. The hypothesis sentence in CORE.md §3 is untouched. The shortlist's use of "the law of adaptive organization (hypothesis)" is labeled as a hypothesis and is allowed by `check_consistency.py`; "√ law" and "power-law" are ordinary scientific uses. Cities, nation-states, and the biosphere remain excluded pending a class N_e, as FRAMEWORK requires.

The stale "open PR #128" / `main` `ac079ea` line is a status error at commit time, not a scientific overclaim (M1).

---

## 7. Checkers and pytest after rebase on `ecf6e77`

Unrebased: not mergeable (OPEN_WORK conflict). After a local resolution that keeps PR #128's OPEN_WORK rows and adds T29: `check_open_work.py` PASS; `check_consistency.py` PASS (0 FAIL); `pytest tools/ --ignore=tools/test_lean.py` 144 passed in 2:04; `test_lean_sources_have_no_sorry` passed. That is enough to say the package will pass once the author rebases; it is not a substitute for that rebase on the PR branch.

---

## Issues

### Must-fix before merge

**M1. Rebase onto `ecf6e77` and resolve OPEN_WORK.md.** Keep main's W14 and the GRID-CROSS update to T3. Add T29. Update the as-of line so that `main` is `ecf6e77` and PR #128 is described as merged (official comparison not run; P25 still UNTESTED), not "open." Do not drop GRID-CROSS rows in the merge.

**M2. Correct the van Hateren 1997 world source.** The intensity series were recorded from a freely walking human and played back to *Calliphora vicina*. They are not "from the blowfly." Disclose a three-way split (human world / blowfly responses / *Drosophila* N_e), and tone down "flying Diptera, acting in natural light-intensity time series." This is the central empirical description of the top candidate and should not ship wrong.

### Should-fix in the note (before it is used as the basis of a lock or of Pass 1)

**S1. Do not advertise CT12's 1/α as the VIS-1F prediction without choosing the right theorem and writing the α map.** CT12 (THEORY B.3, lines 335–339) is exact reset reads, 1 < α < 3. Continuous early vision is Lemma B2 / CT21, with a different elasticity. γ ≈ 1 likely puts α at or outside the CT12 interval. The primary arm should be a priced cutoff or count versus whitening, with CT12 dropped unless a discrete read is defined and α is shown to be in range.

**S2. Specify the Pass 1 error band, the γ → α map, and the (h, w) rule *before* any fitting.** "Pre-written" is not yet written. Close the "declared price-free structural claim" loophole. Record that L3 may make a finite K\* undefined on a continuum, in which case Pass 1 stops.

**S3. Credit the efficient-coding papers that van Hateren 1997 itself sits on:** Laughlin 1981, Atick & Redlich 1990 *and* 1992, and van Hateren 1992a (spatiotemporal filtering / theoretical LMC fields). Atick 1990 is already named; the others are not. This is prior-art hygiene for the top candidate, not a new numbered claim.

**S4. Repair "the Δ*cheY* advantage vanished in stirred culture."** It was a WT advantage that vanished when stirred.

**S5. Write "Europe PMC XML HTTP 500" for Beekman, and do not lean on 600 and 0.0052 until a full text is opened again.** This review could not re-open Beekman or Dornhaus. Crossref's Beekman abstract supports the qualitative transition, not those two numbers.

**S6.** Briefly dispose of TESTBEDS #2 (learning-rate), #3 (central-bank calendars), and #6 (weather cycles) in §3, since the intro claims that ranking was searched.

### Nits

- The Sung Table 1 excerpt should say it is a subset (three species omitted).
- Honda's ∼4.4-fold figure is in the published 2022 XML, not only the preprint.
- N\*(ρ) is proved as CT14 (square-root technology); CT16 is the telling price. "CT16, Result 4" is the main-text bundle, slightly loose.
- The 7–15× store-versus-mode range is the §1a / `meq_roots.out` band, not the §2 point estimate (1.5 and 6.9 days).
- "Conservative" N_e should state the direction (smaller N_e widens ε).

---

## Recommendation

Fix M1–M2, then merge as an unlocked shortlist and OPEN_WORK T29. Do not lock VIS-1F, and do not start official Pass 1 scoring, until S1–S2 (and the corrected species split) are on the page. Nothing here changes a locked result.
