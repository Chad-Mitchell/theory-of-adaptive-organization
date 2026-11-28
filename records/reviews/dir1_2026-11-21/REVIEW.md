# Independent hostile review: PR #138 (DIR1 directional test)

*21 Nov 2026 (ET). A separate cloud agent, told to break the verdict. Read only: no commit, no push, no edit of locked files, no file written into the repo. Heavy steps at nice 19. Every DOI below was read from Crossref or OpenAlex in this session.*

**Verdict: READY-WITH-FIXES. No blockers.** The locked scorer reproduces INCONCLUSIVE, and the corrected codes are still INCONCLUSIVE. Firms, on the corrected codes, fail the locked class rule (6/10 = 0.60). One failing class does not meet the kill. The blind recode agrees 19/20.

## Verified clean

- Lock commit `47c8594` at 13:16:55 ET (GitHub author and committer `2026-11-21T18:16:55Z`). Pool manifest `retrieved: 2026-11-21 13:21:43 EST`. Data commit `61bdb65` at 13:34:20 ET. The four locked blobs are identical at the lock and at HEAD `0aad420`. `sha256sum -c tests/DIR1/PREREG_DIR1.sha256` OK for all four files.
- Same-day re-query of the eleven locked OpenAlex strings matched the ranked DOI or title on 220/220 rows. Raw pool JSON is off-repo, so the stored SHA-256 values were not recomputed.
- `score_dir1.py` on `data/coded.csv` is byte-identical to `ANALYSIS_DIR1.json`. Committed verdict INCONCLUSIVE: 35/46, p = 2.678e-4; animals 21/27 support; cells p = 0.145; firms p = 0.113; D5 n = 2.
- Inclusion cap: only A3 ranks 17–20 are "not screened," after the tenth inclusion at rank 16.
- Crossref: 45/45 included DOIs match the pool title (44 at similarity 1.0, F4 rank 15 at 0.994). The no-DOI row is OpenAlex W2761342761, 2017, DOI empty, abstract matching the locator.
- Novelty-note DOIs all resolve to the named papers (titles and first authors checked). Staw, Sandelands & Dutton 1981 is Crossref 10.2307/2392337, ASQ, December 1981.
- `CORE.md` and `THEORY.md` are unchanged versus `2c32ade`. The hypothesis sentence is unchanged. STATUS merge SHAs for #114 and #133–#137 match the log.
- `check_consistency.py` PASS. `check_open_work.py` PASS. `pytest tools -q`: 146 passed, 1 skipped (Lean not installed), 123 s.

## Blind recode

Seed 20261121 on included rows in file order matches `data/recode_sample.json`. Abstracts fetched in the locked source order. Agreement **19/20 = 0.95** (κ = 0.89). The gate is 0.80 on simple agreement. The verdict is not UNRELIABLE CODING.

The disagreement is A4 rank 11 (starlings): reviewer 0, author +1. The between-cue contrast is null; both groups gained mass under the same irregular deprivation. The author's locator already says "no cue effect."

RESULTS had named six of the twenty before the codes were opened (the starling borderline, the thrasher −1, Lenski, Myxococcus, the IT-governance hump, rayaditos, pitvipers). Five of those matched. The other thirteen were not named there, and all thirteen matched.

## Codes the abstracts do not support

Correct these in `coded.csv`, then rerun the locked scorer. Locked files stay as they are.

1. C1 rank 6 (line 7). Exclude, I2. The quoted clause cites Schaum et al. 2013. This paper's result is that plasticity predicts the extent of CO2 adaptation.
2. C1 rank 13 (line 14). Exclude, I2. "Higher environmental variation" is the variance that hides genetic differences from selection, not more plasticity or a faster read.
3. C4 rank 7 (line 48). Exclude, I2. Pulse versus continuous is proteins and polysaccharides. Polyphosphate is an LNA-versus-HNA path.
4. A4 rank 11 (line 132). Recode +1 to 0. Keep it included.
5. F4 rank 2 (line 183). Exclude, I2. The sentence continues "even after controlling for cash flow volatility." The second coder was right. The committed locator stops before that clause.
6. F4 rank 14 (line 195). Recode +1 to 0. The abstract says firms hold more cash when volatility is high at better earnings and less cash at poorer earnings. Mixed is 0.

F1 rank 10 stays excluded. The mid-1960s shortening is not stated as the inflation effect; "changes in rigidity" is tied to inflation and to policy together. F4 rank 3 stays excluded. Volatility is a named regressor and is absent from the results. An omitted coefficient is not a reported zero.

Corrected counts: pooled 29/42 = 0.690 (p = 0.00976); animals 20/27 (p = 0.00958, still supports); cells n = 5; firms 6/10 = 0.60 (p = 0.377, **fails**). One class fails. The kill needs two, or a pooled rate ≤ 0.60. Headline verdict stays INCONCLUSIVE.

If C1 ranks 6 and 13 were coded 0 and kept, cells would be 4/8 = 0.50 and would fail too, and the kill would fire. The abstracts support dropping them under I2, so that is not the correction. It is recorded so a later recode cannot do it quietly.

## Predictions

- D1. CT12 gives read rate rising in q, at fixed read price, inside that model. CL19's band width (6kσ²/w)^(1/4) widens with drift; the time between resets falls as 1/σ, so the adjustment rate rises. The prereg's "crossed more often" is the derived sign. The JSON's "narrows" is the wrong verb for the width. CT10 is the stakes theorem and does not yield D1.
- D2. CT33 gives spend no lower as stakes rise when ruin is slack. That is the locked sign. R3 in D2 ("no price dependence") is a different rival from R3 in D1 ("copies the world's time scale").
- D3. CT4 and CT9 give loss of a trait that no longer pays. FREEZE_PROCESS §2 cites relaxed-selection loss as known biology. The low discrimination against drift is correctly labelled. The Lenski code +1 is right, and the mechanism in the abstract is mutation accumulation.
- D4. CT25 is the buffer required, shock × τ^H. The locked sentence "binding ruin does not flip this sign" does not follow from CT25 or CT22. The thrasher abstract (lost mass at the same mean intake) contradicts that sentence. The −1 stays in the score. The diagnosis is a note for a future lock, and it does not reclassify the miss.
- D5. THEORY.md line 488 is the cited formula, and CORE.md line 46 states the fast-local sign. Staw et al. 1981, as titled on Crossref, is threat-rigidity, and the prereg restates it as centralize under turbulence. Rcopy has no citation. D5 is unscored (n = 2). The fast-local sign is in the repository. The claim that it is the prediction with clean opposite-sign rivals is stronger than the citations.
- D1–D4 do not separate J from any minimizer of S + wE. PRICE_FREE §2 already says so, and the prereg repeats it. The results paragraph that then moves "the weak version" to "roughly 72–80%" has no prior percentage anywhere in the repo. The prereg's 0.8 is the author's probability that the test would PASS. The locked odds section is silent on INCONCLUSIVE.

The fur-seal −1 stands. "Less predictable" is the cell's variability input, and multi-year site fidelity is less sampling. Lemma B1 is not available as a rescue under the prereg.

QC. The class table is inside the lock and therefore predates the 13:21:43 EST retrieval. Study-level exclusions in `coded.csv` are design reasons (review, no abstract, wrong input, one domestication). A4 ranks 7 and 11 are captive birds, and QC1's animal cell says wild populations. Record that reading in the deviations.

## Novelty note

THEORY.md line 196, in §10, does say "The parts are known and the claim built from them is new," and the package list that precedes it matches the note's quotation through "kill condition." PRIOR_ART's two phrases match. The master-equation review's bottom line, item 2, is "Modest synthesis, not a new result." "A genuine but elementary contribution" is a later sentence in that review, not the verdict line. The Lee, Flack & Krakauer DOI is the paper titled *Constructing stability: optimal learning in noisy ecological niches*; the abstract states a sublinear scaling of optimal memory with environmental persistence.

## Should-fixes

S1–S6 in `coded.csv` lines 7, 14, 48, 132, 183, and 195, as specified in the review report of this date, then rerun `score_dir1.py`.

S7. RESULTS lines 5–7, the class table, and line 18: replace the committed 35/46, "no class failed," and 6/8 and 8/11 with the corrected counts above, and say firms fail.

S8. RESULTS line 25: the fur-seal −1 is the cell's own input. Delete the Lemma B1 rescue.

S9. RESULTS line 26: the thrasher −1 stays. State that "binding ruin does not flip this sign" does not follow from CT25.

S10. RESULTS line 47: delete "0–3 points (to roughly 72–80%)." State that the likelihood ratio of these data for J against any S + wE minimizer is about one, because D5 is unscored, and that the locked odds section gives no number for INCONCLUSIVE.

S11. DEVIATIONS: append the code corrections, the CT41 width-versus-rate note, the two meanings of R3, the Staw title, and the captive-bird QC reading.

S12. NOVELTY_NOTE line 14: attribute "elementary contribution" to the later paragraph, and leave "Modest synthesis, not a new result" as the bottom line.

S13. NOVELTY_NOTE line 27: use the Crossref title *Constructing stability: optimal learning in noisy ecological niches*.

S14. OPEN_WORK.md line 14: delete the extra `| DONE |` cell on the W2 row. Line 28 and STATUS.md line 8: replace the 35/46 sentence with the corrected counts.

## Nits

A4 rank 12's bracketed gloss sits inside the quotation. Three locators exceed about 25 words. A2 rank 1's group-size result estimates risk by vigilance; the ram contrast is what carries the +1. The CORE citation "CT14...CT34" is the single row at CORE.md line 46. The package quotation omits the clause "and predictions across scales, posed so that they can fail" without an ellipsis.
