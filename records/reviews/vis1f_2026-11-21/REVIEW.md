# Independent hostile review: PR #130 (VIS-1F drop under the written pre-Pass-1 rule)

**Reviewer:** independent (wrote none of the PR, `theory/VIS1F_DROP_2026-11-21.md`, or the OPEN_WORK T29 rewrite).
**Date:** Saturday 21 November 2026, started 3:38 AM ET, finished 3:45 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/130
**Clone:** fresh `/tmp/gtao-pr130` at head `04a1988f46f171e229d9887c7e876304ef0db9da` (branch `vis1f-2026-11-21`), merge-base `e2bfc2ba730cee102c612ed8da20bfde0a1aafc3`. `origin/main` at review is the same `e2bfc2b` (PR #129 merged). Clean tree at review start. Nothing merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The drop is honest and not premature. Both sides of the written pre-Pass-1 rule in `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md` actually fire, and the note does not overstate them. No lock was taken, no official Pass 1 fit was run, and no locked row is re-scored. `CORE.md` is byte-identical to `origin/main`. The law-of-adaptive-organization hypothesis sentence is unchanged. Candidate 2 is correctly named as the next unlocked Pass 1 attempt, with the shortlist's collapse risk left in place.

The drop can stand. Three should-fixes belong in this PR before merge: a wrong author on a Crossref-verified DOI that was not opened (S1), a broken OPEN_WORK T29 table row (S2), and the general lesson about fitness-unit prices, which is not yet stated where it belongs and must not be overclaimed (S3). None of these moves the drop rule or invents a price.

---

## What was checked

- Fresh clone at the stated head/base; diff `e2bfc2b..04a1988` (one commit, 2 files, +101 / −2): new `theory/VIS1F_DROP_2026-11-21.md` and an OPEN_WORK as-of / T29 rewrite. No other path is touched.
- The written drop rule and the operational (h, w) / L3 / priced-cutoff stops in the shortlist (§0 of the ranking page, and §5 of the still-unlocked outline), applied as written, not loosened.
- Every DOI in the note's §6 queried on `https://api.crossref.org/works/{doi}` this session; all four returned a works record. The three no-account PDFs named in the table were re-fetched, hashed, and opened with `pdftotext`. Quoted numbers were checked against those files. THEORY L3 / CT21 (line 81), Lemma B2 (B.3, line 347), FRAMEWORK §3.3 and §3.5, and SN1 were checked against the current tree.
- A short search for a defensible fitness-unit w (an error-cost curve, not knockout extremes) that could make the drop premature.
- CORE.md / law sentence / re-score: `CORE.md` SHA-256 `aee235cb…284a7a` is identical on this branch and on `origin/main`. The two-file diff does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, any locked results file, or the shortlist itself.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; frozen-record INFO hits only; soft length WARNs already on main). `python3 -m pytest tools/ -q`, with `~/.elan/bin` on `PATH`, at nice 19: **146 passed** in 2:37. Full `tools/check_lean.sh` (`lake build`) was not re-run; the PR does not touch `formal/lean/`, and the Lean source tests are inside that 146.

---

## 1. Does the written drop rule fire on both sides, and does the note overstate?

The shortlist, after review and confirm of PR #129, kept candidate 1 first only as a Pass 1 attempt and wrote (exact quote, ranking page):

> If Pass 1 cannot source (h, w) independently of the design, or if L3 leaves both a finite K\* and a priced cutoff undefined, candidate 1 is dropped and not locked.

The unlocked outline (§5) makes the same stops operational and forbids a price-free structural-claim path. The note quotes that rule accurately and does not loosen it. Official Pass 1 scoring of traces was not started, as the task required. The shortlist file itself is unchanged.

**(h, w) side — fires, not overstated.** FRAMEWORK §3.5 defines upkeep h as "the existence cost per tracker per unit time, independent of reading," and at cell scale operationalizes it as "expression and maintenance cost of a receptor or pathway (protein burden), from fitness cost of expressing it in a constant environment." FRAMEWORK §3.3 defines stakes w as "the cost per unit time per unit of loss of tracking error," estimated from "the outcome cost as a function of tracking error, from natural or designed variation in error (an error-cost curve)." Those quotes check. The shortlist requires both prices, independently of the measured kernels, cutoffs, or layer counts, and in commensurate units. Niven 2007 dark cost is correctly treated as a metabolic stand-in for h in ATP units, incurred with no light-driven signalling and not taken from a kernel or cutoff, and correctly refused as FRAMEWORK's fitness operationalization. Laughlin's and Niven's cost-per-bit and light-adapted totals are correctly refused as independent prices, because they are computed from information rates (and, in Laughlin, from signal and noise spectra) of the same cells whose bandwidth would be the predicted design. w is not sourced. Markow & Manning 1980 is opened and correctly not used as w: it is presence-or-absence of receptor classes, and FRAMEWORK §3.3 lists "Loss measured only at the extremes" as a failure mode for stakes. The conclusion, "(h, w) cannot both be sourced independently of the design," is therefore right, including in fitness units. A metabolic h without a commensurate w still cannot price a design. The sentence "This is not a test of the hypothesis, because a price-free structural claim can be fitted to the data" follows the written rule and is not a claim that the law failed.

**L3 / priced-cutoff side — also fires, not overstated.** THEORY line 81 (Master Theorem (iii) / CT21) is exactly: "A continuum of time scales has no exact finite design (L3)." Lemma B2 at THEORY B.3, line 347, matches the note's paraphrase: error \(q^{1/\alpha}\sigma_n^{2(1-1/\alpha)}/\sin(\pi/\alpha)\); memory time \(\propto (\sigma_n^2/q)^{1/\alpha}\) (Wiener/Kalman bandwidth); precision effort with a linear price \(\propto w^{\alpha/(2\alpha-1)}q^{1/(2\alpha-1)}\); "the number of stores grows with the span of time scales and with stakes over upkeep away from \(\alpha = 2\) (rate conjectural)." The note did not run an official corners-versus-continuum fit, and it does not need to: it uses the shortlist's already-recorded van Hateren description ("γ here close to 1," mild deviation below 0.1–1 Hz, not a fitted real pole). Under that description, L3 leaves a finite K\* undefined, and inventing one would have been the overstep. The priced-cutoff fallback in the outline is available "only if (h, w) have been sourced independently and a cutoff is well-defined under the priced continuous-sensing problem (Lemma B2 / CT21)." That fails on both parts, and the note's reasons check:

- (h, w) were not both sourced.
- Lemma B2's memory time is set by observation-noise density and by the world, not by upkeep h. SN1_RESULTS.md records the *Drosophila* photoreceptor arm as INVALID because "photon shot noise (exogenous) is the noise source." Calling that "Model S is the right noise class" is an inference, not a verbatim SN1 sentence (the PR #129 review already accepted the same inference). With \(\sigma_n\) exogenous, that Kalman bandwidth is the SNR-determined bandwidth efficient coding already uses, not a priced deviation from whitening.
- Lemma B2's "precision effort" is a spend quantity, not a frequency cutoff.
- Growth of store count with stakes over upkeep is marked "rate conjectural." L3 says there is no exact finite design. The locked in-model water-filling state-count rule (T25, WF-HSV) already failed and is correctly not re-scored. The note is right not to invent a conjectural cutoff in order to keep the candidate alive.
- "γ here close to 1" puts \(\alpha\) at or outside the open interval on which the B2 error formula is stated (\(\sin(\pi/\alpha)\) vanishes as \(\alpha \to 1\)). That is already in the shortlist. The continuous-sensing problem is not in the proved regime for this world, even before prices.

The phrase "L3 leaves both a finite K\* and a priced cutoff undefined" is slightly compressed: the priced-cutoff failure is L3 plus missing prices plus B2 not defining a proved priced cutoff in this regime. That is what the written fallback rule asks. It is not an overclaim.

---

## 2. Numbers, DOIs, and Markow & Manning

All four listed DOIs resolve on Crossref. Issued dates in the table match Crossref's `issued` date-parts: 10.1038/236 (1998-05), 10.1371/journal.pbio.0050116 (2007-03-20), 10.1016/s0163-1047(80)90612-3 (1980-06), 10.1242/jeb.001040 (2007-08-01). The three opened PDFs re-fetched this session match the claimed sizes and SHA-256 values exactly:

| Source | Bytes | SHA-256 |
|---|---:|---|
| Laughlin et al. 1998, Princeton author PDF | 97,243 | `df7c2e2476daf60d5ceda07fce160c291f8be836196fb277be6852751a7359c0` |
| Niven et al. 2007, PLOS printable PDF | 721,474 | `d806c8d58d1397b9a3a7420ca3e404d17051bd3bc8642845e4d8be8c529a8f06` |
| Markow & Manning 1980, Markow lab author PDF | 277,499 | `bf63182761fb5470bc4cd41458140f07279f10cd51b126ac6d36f195e3ac259c` |

**Laughlin, de Ruyter van Steveninck & Anderson 1998.** Every numbered claim checks against the opened PDF: five photoreceptors at \(10^6\) effective photons per receptor per second; \(E_m = -33 \pm 6\) mV; input resistance \(7.1 \pm 1.8\) MΩ; mean total conductance 141 nS; ATP consumption \(7.5 \times 10^9\) molecules per second from the membrane model; information rate 1,000 bits per second under those fully light-adapted conditions, with the paper's own caveat that natural signals contain correlations not present in the random stimuli and that lower rates are expected under natural conditions; metabolic cost \(7 \times 10^6\) ATP molecules per bit, stated as a lower bound; chemical synapse \(2 \times 10^4\) to \(6 \times 10^4\) ATP molecules per bit at 55 bits per second; 240 vesicles released per second; "roughly \(2 \times 10^5\)" ATP molecules per synapse per second (the note's "about" is fair); abstract \(10^4\) ATP molecules per bit at a chemical synapse and \(10^6\)–\(10^7\) for graded signals in an interneuron or a photoreceptor, or for spike coding. Species is blowfly (*Calliphora*), as stated.

**Niven, Anderson & Laughlin 2007 (PLOS).** Homologous R1–6 photoreceptors of *D. melanogaster*, *D. virilis*, *Calliphora vicina*, and *Sarcophaga carnaria*, driven by the same stimuli, check. Dark cost is "the rate at which ATP is hydrolysed to maintain the cell's resting potential in the dark"; the factory-rent sentence is a mid-sentence excerpt and is accurate. Fixed cost "~20% of a photoreceptor's maximum consumption" is in the abstract. Dark consumption "approximately \(2 \times 10^9\) ATP molecules s\(^{-1}\)" in *Calliphora* and *Sarcophaga* R1–6, "approximately twenty times less, \(1 \times 10^8\)" in *D. melanogaster* R1–6, checks. The species difference is attributed primarily to dark input resistance (more than an order of magnitude), not to the (up to 10 mV) differences in dark resting potential. Highest rates at bright daylight: ~200 bits s\(^{-1}\) in *D. melanogaster* to ~1,000 in *S. carnaria*. At the brightest stimuli: *Calliphora* \(955 \pm 70\) (n = 3), *Sarcophaga* \(1{,}130 \pm 67\) (n = 11), *D. virilis* \(512 \pm 26\) (n = 21). Signalling cost as the light-induced increase (total minus dark, given the fixed-cost accounting), unit cost falling as rate rises because the fixed dark cost is spread over more bits, and the cross-species diminishing-returns pattern, all check. One consistency nit: the same sentence in the paper gives *D. melanogaster* as "~200 bits s\(^{-1}\) … (\(197 \pm 31\), n = 26)." The note quotes n and SE for the other three species and leaves melanogaster as "about 200." The rounding is the paper's own and is not false; quote the parenthetical for consistency (Nit 1).

**Markow & Manning 1980** is correctly not used as w. Female-choice experiments in *D. melanogaster*, Canton-S wild-type males competing with mutants that eliminate function in R1–6, in R7, or (norpA) the receptor potential of the entire eye, check. The paper's own abstract says an intact visual system, especially R1–6, is important for male mating success, with a small but significant role for R7 when R1–6 are absent. That is presence-or-absence of receptor classes, not an error-cost curve versus tracking error or versus a filter cutoff. Table 1 percentages are correctly not converted into a w.

**S1. Wrong author on 10.1242/jeb.001040.** The note attributes *J. Exp. Biol.* "VISION COSTS," doi 10.1242/jeb.001040, to Niven, Anderson & Laughlin 2007. Crossref lists a single author, Matthew Cobb, title "VISION COSTS," *J. Exp. Biol.* 210(15): vii–vii, issued 2007-08-01. It is a one-page Outside JEB note, not the PLOS research article. The note claims every DOI was queried on Crossref this session, so the author field was available without opening the PDF. The publisher PDF was not opened (the note records HTTP 403) and no number is taken from it, so the drop does not depend on this error. Fix the author in §2.2 and in the §6 table.

---

## 3. Quotes of THEORY, FRAMEWORK, and SN1

Already checked in §1. L3 / CT21 at THEORY line 81 is verbatim. Lemma B2 at line 347 is a fair, accurate paraphrase of the cited clauses (the omitted forgetting-kernel clause is not used). FRAMEWORK §3.3 and §3.5 quotations are accurate. SN1's exogenous photon-shot-noise reading is accurately cited; "Model S is the right noise class" is an inference, not a quote (Nit 2; no fix required).

---

## 4. Is the drop honest and not premature?

Honest: no lock, no SHA-256 of a PREREG, no official score, no claimed numerical gap versus R2, R3, or whitening, no digitizing of traces for a Pass 1 decision, qualification still not shown (no σ, no T_red; Sung et al. 2016 N_e is left as a species-wide default and is not used in a verdict). Locked rows named as not re-scored (P1, P3, P4, P13, P25, SN1, BIO1) are not touched. Candidate 2 is not sold as a shown discriminator; the shortlist's warning about collapse into Ni et al. 2020 and Honda et al. 2022 is left in place and not reopened.

Not premature. This review searched quickly for a published error-cost curve that would supply a defensible FRAMEWORK §3.3 w: fitness, survival, mating success, or foraging return as a continuous function of dipteran photoreceptor or LMC tracking error, or of cutoff, or of kernel time constants. No such curve was found in a form that can be placed in a ratio with h without inventing a map.

- Markow & Manning 1980, and later categorical mating papers (screening-pigment or other visual mutants versus wild type), remain loss measured at the extremes.
- Optomotor, landing, and gaze-stabilization papers give behavioral performance versus contrast or temporal frequency, not fitness.
- Niven & Laughlin 2008 (*J. Exp. Biol.* 211, 1792, "Energy limitation as a selective pressure on the evolution of sensory systems") is the obvious follow-on review. It argues qualitatively for a cost-benefit trade-off. It does not supply an error-cost curve in fitness units for dipteran tracking error. The drop note did not have to list every paper that fails to provide w.
- Niven 2007's remark that the *Calliphora* dark current is about 2% of a blowfly's total resting metabolic rate is still a metabolic, h-like conversion, not w, and is correctly unused as stakes.

Inventing a map from ATP per bit, or from mutant mating-success extremes, onto w is rightly forbidden. I did not quickly find a fitness cost of expressing the pathway in a constant environment either, so h is also unsourceable in FRAMEWORK's fitness units.

Even if a defensible w were later found, the written rule is an *or*. Side 2 would still fire for this world: under the already-recorded near-1/f description, L3 leaves finite K\* undefined, and Lemma B2 does not supply a proved priced cutoff at \(\alpha \approx 1\). The drop is therefore not contingent on a slightly more thorough w search.

---

## 5. The general lesson about fitness-unit prices

Independently sourcing fitness-unit prices (h, w) may be the binding obstacle for most field tests of the law. That is a fair lesson from this check. It is not stated where it belongs, and it must not be overclaimed.

STATUS.md already says "Stakes w have never been measured validly, and no tracked world's drift spectrum has been measured validly." That is related and already on the record, but it is narrower: it names only w, and it is a historical statement about past tests, not a process lesson that independent *fitness-unit* prices (both h and w, commensurate) may be what blocks most field tests of the law. This drop adds a sharper point: even a carefully opened metabolic stand-in for h is not enough, because FRAMEWORK wants fitness units and a commensurate w, and a price-free structural claim is not a test.

That sentence is not in OPEN_WORK.md and not in `process/QUEUE.md`. Add it carefully to OPEN_WORK (the T29 State, or a short process note linked from T29), scoped as *may be* the binding obstacle, from this check plus the existing STATUS sentence — not a completed survey of every field test, and not a change to CORE.md, to the law sentence, or to any locked row (S3).

---

## 6. Locked rows, CORE, checkers, pytest

`CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`). The hypothesis sentence in CORE.md §3 and in THEORY.md, "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment," is unchanged. CLAIM_MAP, locked E. coli and grid files, SN1, BIO1, and the shortlist are not in the diff. `main` is still `e2bfc2b`; the branch has no merge conflict with current main.

`python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL). `python3 -m pytest tools/ -q`: **146 passed**.

**S2. T29 is a four-column row in a five-column table.** The live OPEN_WORK table is `| ID | Item | State | Gate | Where |`. T28 and the neighbouring T-rows have five fields. T29 has four: the drop narrative sits in Item, Gate is `in progress-able`, and State is missing. The gate token itself is used elsewhere and is acceptable once candidate 2 is the next attempt. Restore five columns. Put a short Item and a State that says VIS-1F is dropped under the written rule, no lock, no official Pass 1 fit, and that the next unlocked Pass 1 attempt is shortlist candidate 2 (still not a shown discriminator).

---

## Numbered issues

### Should-fix (before merge; none of these reopens the drop)

1. **S1. Wrong author on doi 10.1242/jeb.001040.** Crossref lists Matthew Cobb, "VISION COSTS," *J. Exp. Biol.* 210(15): vii–vii (2007-08-01), not Niven, Anderson & Laughlin. The PDF was not opened and no number was used. Correct §2.2 and the §6 table. The PLOS paper (10.1371/journal.pbio.0050116) remains the Niven, Anderson & Laughlin 2007 source.

2. **S2. Restore the five-column OPEN_WORK T29 row.** Item / State / Gate / Where, with Gate `in progress-able` (or a more precise gate if this PR itself is what is waiting on review) and a State that records the drop and points at candidate 2 without selling it as a discriminator.

3. **S3. State the general lesson in OPEN_WORK, without overclaiming.** Independently sourcing fitness-unit prices (h, w) may be the binding obstacle for most field tests of the law. Scope it as a lesson from this check plus the existing STATUS.md sentence on w, not as a completed survey, and do not edit CORE.md or the law sentence.

### Nits (do not block)

1. **Nit 1.** Quote Niven 2007's *D. melanogaster* brightest-stimulus rate as \(197 \pm 31\) bits s\(^{-1}\) (n = 26), in line with the other three species, rather than only "about 200."

2. **Nit 2.** "Model S is the right noise class" is an accurate inference from SN1, not a quote. No fix required.

---

No must-fix. The drop rule fires on both sides, the numbers that were opened check, Markow & Manning is correctly unused as w, THEORY / FRAMEWORK / SN1 citations are accurate, the drop is not premature, and nothing locked was moved. Apply S1–S3, then this is ready for a confirm review and a merge. This review does not merge the PR.
