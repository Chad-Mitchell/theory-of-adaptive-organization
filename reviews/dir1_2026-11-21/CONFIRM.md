# Confirm review of DIR1 (draft PR #138, head b32be6f)

*21 Nov 2026, about 2:22 PM ET (America/New_York). Blind confirm. This reviewer did not write the PR or `reviews/dir1_2026-11-21/REVIEW.md`. Read only: no commit, no push, no edit of locked files, no file written into the repo. Head `b32be6f774044d41d2edc01fbfe94eb5b995b2ff` on `dir1-directional`. Working tree clean after rerunning the locked scorer.*

**Verdict: READY-WITH-FIXES. No blockers.** The locked scorer reproduces INCONCLUSIVE on the corrected codes. Pooled 29/42. Animals 20/27 support. Firms 6/10 = 0.60 fail. Cells n = 5, below 8. One failing class does not meet the kill. S1–S14 and the named nits landed in unlocked files. The four locked blobs match the lock commit. The remaining defects are stale sentences. They do not move a code or the verdict.

## Blockers

None.

## Should-fixes

1. `tests/DIR1/RESULTS_DIR1.md:18`. Replace `every included DOI matched its Crossref title (45/45; one record has no DOI, DEVIATIONS 3)` with `every DOI still included matched its Crossref title (41/41; the pre-correction check was 45/45, and four of those DOI rows were later excluded under I2). One included record has no DOI (F4 rank 14, DEVIATIONS 3)`. The 41 DOIs still included all match in `data/crossref_check.json`. The four dropped matches are C1 ranks 6 and 13, C4 rank 7, and F4 rank 2.

2. `tests/DIR1/DEVIATIONS_DIR1.md:10` (item 6). Replace `The blind recode of 20 systems by the independent reviewer (PREREG §5 reliability gate) is owed; until it is done the verdict carries "reliability gate pending".` with `The independent reviewer recoded 20 included systems (seed 20261121). Agreement was 19/20, above the 0.80 gate, so the verdict is not labelled UNRELIABLE CODING.`

3. `tests/DIR1/DEVIATIONS_DIR1.md:9` (item 3). Replace `the post-hoc sensitivity in RESULTS drops it.` with `it is coded 0 and kept in the score. The old sensitivity that dropped it is described in the past tense in RESULTS; it is not the current score.`

4. `tests/DIR1/DEVIATIONS_DIR1.md:11` (item 7). That paragraph still speaks as if the current file had F4 rank 2 coded +1 and the pool at 35/47. Replace `the committed data/coded.csv is the first session's` with `the then-committed data/coded.csv was the first session's`. Replace the F4 rank 2 parenthesis so it ends `then-committed: +1; item 8 now excludes this row under I2`. Replace the 8/12 and 35/47 sentence with `On that pre-correction sheet, the second coder's F codes gave F 8/12 (p = 0.19) and pooled 35/47 = 0.74. Those figures are not the current score.`

5. `STATUS.md:8`. Replace `scored on 46 systematically searched studies` with `scored on 42 studies after the coding corrections (220 screened; 46 included at first scoring)`. Replace `Independent review and the blind recode gate are owed (`tests/DIR1/RESULTS_DIR1.md`).` with `Independent review is `reviews/dir1_2026-11-21/REVIEW.md` (READY-WITH-FIXES, no blockers). Blind recode 19/20, above the 0.80 gate.`

6. `OPEN_WORK.md:28`. Replace `220 records screened, 46 included.` with `220 records screened; 46 included at first scoring; 42 included after the coding corrections.` Replace the gate cell `needs reviewer (independent hostile review plus blind recode of 20 systems, then confirm)` with `needs confirm (hostile review in `reviews/dir1_2026-11-21/REVIEW.md`, READY-WITH-FIXES; blind recode 19/20)`.

## Nits

- `tests/README.md:26` still says the DIR1 review is pending. Point it at `reviews/dir1_2026-11-21/REVIEW.md` and the corrected verdict (INCONCLUSIVE, pooled 29/42, animals support, firms fail).
- Two included locators still exceed the prereg's about-25-word quote. `data/coded.csv:102` (A3 rank 1, 28 words) and `data/coded.csv:216` (F5 rank 15, 30 words). Shorten the quotes. Do not change included or code. The three longest pre-fix locators were shortened: C3 rank 7 (33 to 24), F1 rank 4 (33 to 21), F4 rank 14 (32 to 19).
- `data/coded.csv:93` (A2 rank 12) still has bracketed glosses inside the quotation. The nit named A4 rank 12, and that gloss is now outside the quotation (`coded.csv:133`).

## Lock and score

`sha256sum -c tests/DIR1/PREREG_DIR1.sha256` at this head:

- `5c405316e35eb2ec70fb66e9f57807b4b3ef85b10e3380414a56490918c58e48  PREREG_DIR1.md`
- `75b911b7080d278bb435cc0cf992537ed7beeaec0ea0264501c48dd2cb654522  PREDICTIONS_DIR1.json`
- `e7acb45a7b02c49250124520fbe321d8f77d2777e201f15ee788153dd8986b20  search_dir1.py`
- `a638a1c57f1b28f1ff09122dd25ddc3c57fe7048e19288af79b1ee0454d1a1bf  score_dir1.py`

All four OK. Each file is byte-identical to `47c8594a0f9662649c33e917631018e3123c1610`. `git log 47c8594..HEAD` is empty for those four paths. `CORE.md` and `THEORY.md` match `2c32ade`. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."

`python3 score_dir1.py` printed `INCONCLUSIVE` and wrote `ANALYSIS_DIR1.json` byte-identical to the committed file. Re-derived from the locked rules (`n ≥ 8`, `p < 0.01` and rate `> 0.60` to support, rate `≤ 0.60` to fail, FAIL if pooled rate `≤ 0.60` or two classes fail, PASS if two classes support):

| Slice | Re-derived | Locked rule | RESULTS |
|---|---|---|---|
| Pooled | 29/42, p = 0.00976, sign p = 2.31e-7 | not FAIL (0.690 > 0.60) | 29/42, p = 0.0098 |
| Animals | 20/27, p = 0.00958, supports | supports | supports, p = 0.0096 |
| Firms | 6/10 = 0.60, p = 0.377, fails | fails | fails, p = 0.38 |
| Cells | n = 5, plus 3 | does not count | does not count |
| Classes | 1 supports, 1 fails | INCONCLUSIVE | INCONCLUSIVE |

By prediction: D1 5/7, D2 7/9, D3 10/13, D4 7/11, D5 0/2. No prediction has rate ≤ 0.50 at n ≥ 5. By cell the prose matches `ANALYSIS_DIR1.json`.

The fix commit `b32be6f` changes only `OPEN_WORK.md`, `STATUS.md`, `REVIEW.md` (added), `ANALYSIS_DIR1.json`, `DEVIATIONS_DIR1.md`, `RESULTS_DIR1.md`, `data/coded.csv`, and `theory/NOVELTY_NOTE_2026-11-21.md`.

## S1–S14 and the nits

S1–S6, `coded.csv` lines 7, 14, 48, 132, 183, 195: C1 ranks 6 and 13 and C4 rank 7 excluded under I2; A4 rank 11 and F4 rank 14 recoded +1 to 0 and kept; F4 rank 2 excluded under I2. F1 rank 10 (line 171) and F4 rank 3 (line 184) stay excluded. The scorer was rerun.

S7. RESULTS lines 5–7, the class table, and the by-cell counts use 29/42, animals 20/27 support, cells n = 5, firms 6/10 fail. The leftover on that same line is should-fix 1.

S8. The fur-seal −1 is the cell's own input (less predictable prey, site fidelity is less sampling). The Lemma B1 rescue is gone. The sentence that remains says the prereg scores a fall as −1.

S9. The thrasher −1 stays. RESULTS states that "binding ruin does not flip this sign" does not follow from CT25 or CT22.

S10. The "0–3 points (to roughly 72–80%)" sentence is deleted. The odds paragraph says the locked section is silent on INCONCLUSIVE, that these data leave the probability that systems minimize J rather than any other S + wE where it was, because D1–D4 are that class's comparative statics and D5 is unscored, and that no percentage is added. "About 0.8" is labeled as the author's probability that the test would PASS. A repo grep for `0-3 points`, `0–3`, `72–80`, and `80%` hits only the quotations of that deleted sentence in `REVIEW.md` lines 50 and 70.

S11. DEVIATIONS items 8–12 append the code corrections, the CT41 width-versus-rate note (width widens with σ; the reset rate rises; the prereg's "crossed more often" is the sign), the two meanings of R3, the Staw title, and the captive-bird QC reading. Crossref this session: 10.2307/2392337 is *Threat Rigidity Effects in Organizational Behavior: A Multilevel Analysis*, Administrative Science Quarterly, December 1981, Staw, Sandelands, and Dutton. THEORY.md line 488 has `X_S = ν·π·e^(−2ℓ/τ)·X_L`. CORE.md line 46 is the single row CT14, CT16, CT35, CT36, CT28, CT34. Items 3, 6, and 7 were not updated and are should-fixes 2–4.

S12. The novelty note leaves "Modest synthesis, not a new result" as the bottom line and attributes "a genuine but elementary contribution" to the later paragraph that begins "What I did not find stated together" (`reviews/master-equation_2026-11-19/REVIEW.md` line 98). That is where the review says it.

S13. The Lee, Flack & Krakauer row uses the Crossref title *Constructing stability: optimal learning in noisy ecological niches* (10.1098/rspb.2024.1606). Confirmed on Crossref this session.

S14. The extra `| DONE |` cell on the W2 row is gone. That row has five cells. The 35/46 sentence in OPEN_WORK line 28 and STATUS line 8 is replaced by the corrected counts. The lead-in "46 included" / "scored on 46" and the "review is owed" gate are should-fixes 5 and 6.

Nits that landed: A4 rank 12's gloss is outside the quotation; A2 rank 1 says the ram contrast carries the +1 and that group size estimates risk by vigilance; the CORE citation is recorded as the single row at CORE.md line 46; the package quotation in the novelty note includes "and predictions across scales, posed so that they can fail," which is the clause on THEORY.md line 196.

## Six recoded rows, against the abstracts

Fetched this session from OpenAlex. A4 rank 11 has an OpenAlex work and a null `abstract_inverted_index`; the abstract below is Semantic Scholar, the fourth source in the locked search order.

1. C1 rank 6, 10.1098/rspb.2014.1486, *Plasticity predicts evolution in a marine alga*. "We have previously shown that populations from more variable environments are more plastic (Schaum et al. 2013 …), and here we use experimental evolution with a marine microbe to learn that plastic responses predict the extent of adaptation." Exclusion I2 matches.
2. C1 rank 13, 10.1111/jeb.14178. Clones "evolved higher environmental variation in fluctuating environments than in constant environments," and that variation "decreased the visibility of genetic variation to selection." Exclusion I2 matches. This is not a rise in regulation or plasticity.
3. C4 rank 7, 10.1111/1462-2920.16539. "The pulse-treated LNA bacteria contained more proteins and polysaccharides … than the continuous-treated LNA." Polyphosphate is in the LNA-versus-HNA path. Exclusion I2 matches. Proteins and polysaccharides are not the cell's named storage polymers.
4. A4 rank 11, 10.1016/j.anbehav.2018.06.015. "Both groups of birds increased their dawn body mass … However, no differences in either foraging behaviour or dawn body mass emerged between the groups." Included, code 0. The abstract also says "Sixteen captive starlings."
5. F4 rank 2, 10.1111/j.1540-6261.2010.01558.x, *Cash Holdings and Corporate Diversification*. Lower cross-divisional correlations in investment opportunity "correspond to lower cash holdings, even after controlling for cash flow volatility." Exclusion I2 matches. The volatility coefficient is not the reported result.
6. F4 rank 14, OpenAlex W2761342761, *Cash Holdings and Cash Flow Uncertainty* (2017, no DOI). "Firms hold more (less) cash when their cash flows are more volatile at relatively better (poorer) earnings." Included, code 0. Mixed matches the locked rule.

## Checks

- `python3 tools/check_consistency.py`: RESULT PASS (0 FAIL; 23 frozen-record INFO hits; the existing length warnings on THEORY.md and README.md).
- `python3 tools/check_open_work.py`: RESULT PASS.
- `python3 -m pytest -q tools`, Lean absent: 146 passed, 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake is not installed), 124s.

The PR description says 147 passed. This run is 146 passed and 1 skipped.

The should-fixes and nits listed above were applied in the next commit.
