# DIR1 results: price-free directional predictions on the published record

*Saturday 21 November 2026 (America/New_York). Scored by the locked `score_dir1.py` from `data/coded.csv` after the lock at `47c8594` (13:16:55 ET; `sha256sum -c PREREG_DIR1.sha256` OK). Codes corrected per the independent review of 21 November 2026 (`reviews/dir1_2026-11-21/REVIEW.md`); locked files untouched; scorer rerun. Blind recode 19/20. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." This is a directional, QC-tier test (PREREG §1, §3), not a test of the banded hypothesis.*

## Verdict: **INCONCLUSIVE** (codes corrected per the independent review; blind recode 19/20)

The FAIL condition was reachable and was not met: pooled agreement on the corrected codes is 29/42 = 0.69 (> 0.60), and one class fails, not two. The PASS condition needed two supporting classes; only animals supported. Cells are below n = 8.

| Class | n | +1 | 0 | −1 | Agreement | p (binomial vs ½, nulls count against) | p (sign test vs R0, nonzero only) | Locked class verdict |
|---|---|---|---|---|---|---|---|---|
| C cells / microbes | 5 | 3 | 2 | 0 | 0.60 | 0.50 | 0.125 | does not count |
| A non-human animals | 27 | 20 | 5 | 2 | 0.74 | 0.0096 | 6.1 × 10⁻⁵ | **supports** |
| F firms / markets | 10 | 6 | 4 | 0 | 0.60 | 0.38 | 0.016 | **fails** |
| **Pooled** | 42 | 29 | 11 | 2 | 0.69 | 0.0098 | 2.3 × 10⁻⁷ | not FAIL |

By prediction (reported, not gated except the ≤ 0.50 rule at n ≥ 5): D1 5/7, D2 7/9, D3 10/13, D4 7/11, D5 0/2. No prediction has rate ≤ 0.50 at n ≥ 5.

By cell: C1 1/2, C3 2/3, C4 0; A1 0/1 (−1), A2 7/9, A3 8/10, A4 5/7 (one −1, one 0), A5 0; F1 4/4, F4 2/4, F5 0/2. Every code with its quote is in `data/coded.csv`; every included DOI matched its Crossref title (45/45; one record has no DOI, DEVIATIONS 3), in `data/crossref_check.json`.

**Where the systems came from.** 220 records screened (20 per cell); 42 included after the coding corrections (46 at first scoring; four later excluded under I2). The locked OpenAlex strings worked for vigilance, island tameness, avian fat and price-change frequency, and badly for storage polymers (C4: 0 of 20 usable after the correction), sampling vs variability (A1: 1), social vs individual learning (A5: 0, all theory), and decentralization (F5: 2). Cells remain below n = 8. Firms reach n = 10 and fail.

## The two misses and the eleven nulls, diagnosed (no locked rule changed)

- **A1, Antarctic fur seals (−1).** Multi-year prey is less predictable and the seals keep foraging sites. The cell's plus is more sampling where the environment is more variable, and site fidelity is less sampling, so −1 is the code. Lemma B1 does not move it: the prereg scores a fall as −1 and does not rescue it.
- **A4, curve-billed thrashers (−1).** Same mean food, variable daily amounts: the birds lost mass and drew down fat. The −1 stays. CT25 is the buffer the system needs (shock × τ^H). The locked sentence "binding ruin does not flip this sign" does not follow from CT25 or CT22, and this abstract contradicts it. That wording is a correction for a future lock. It does not reclassify this −1.
- **Nulls (0):** two retain antipredator behaviour without predators (pitvipers; rayaditos' nest defence) — the inertia / multipredator rival's prediction; elk males (vigilance serves another function); one non-significant trend (mannikins); one microalga whose plasticity "did not match simple theoretical predictions"; Myxococcus (retained in some environments, lost in others); one null cash-volatility effect (Indonesia); IT governance first decentralizes, then **re-centralizes** as uncertainty keeps rising (a hump, partly the threat-rigidity rival's sign); Mexican firms that changed structure but kept a functional mindset (a lag); starlings, no dawn-mass or foraging difference between predictable-cue and unpredictable-cue groups (both gained mass); cash-flow volatility that flips sign with earnings (mixed, F4 rank 14).

## Discrimination: what this does and does not show

- Against the no-response rival R0, the sign test on the corrected nonzero codes is small where the class has nonzero codes (animals 6.1×10⁻⁵; firms, 6 of 6, p = 0.016; pooled 2.3×10⁻⁷). That is evidence against no response. D1–D4 are also what any minimizer of S + wE predicts (PRICE_FREE §2).
- Against **any cost-benefit optimizer** (Topkis / S + wE; menu-cost, precautionary-cash and starvation-risk models are each such optimizers), D1–D4 **do not discriminate** (PREDICTIONS §D1–D4; PRICE_FREE §2). D3 also matches neutral drift's sign; one Lenski study (C3 rank 7) attributes the loss to mutation accumulation (drift's mechanism), one yeast study (C3 rank 8) to selection on cost (J's mechanism).
- **D5**, the only prediction with opposite-sign rivals, could not be scored (n = 2). The firm-level evidence closest to it is a *performance* result (Aghion, Bloom, Lucking, Sadun & Van Reenen, F5 rank 11: decentralized firms did better in turbulence), which is a fitness ordering, not a design response, and was excluded by I2.

## Coding corrections (review of 21 Nov 2026; unlocked files only)

C1 ranks 6 and 13 and C4 rank 7 are excluded under I2. A4 rank 11 and F4 rank 14 are recoded +1 → 0. F4 rank 2 is excluded under I2. Dropping those rows from the denominator, which is what the old sensitivity did for the three borderline +1s and the no-DOI record, left firms at 7/10. Scoring the sign-flip as 0 and removing the volatility-as-control row puts firms at 6/10 = 0.60, which the locked rule calls a class fail. The kill needs two class fails. It is not met.

## Threats

1. **Publication bias** inflates agreement; the prereg says a PASS would be weak evidence and a FAIL strong. Here neither happened.
2. **Abstract-only coding by an interested coder.** Mitigated by locked rules, quotes for every code, a published exclusion reason for every exclusion, and a blind recode that agreed 19/20.
3. **Pseudo-replication** across studies of related taxa (several Podarcis lizards, several tits) is not modelled.
4. **QC is coarse.** It establishes large, long-selected, competing populations without a designer, not σ, N_e or bands. Nothing here qualifies a system under THEORY §3.

## What this does to the odds

The locked odds section assigns a change to PASS and to FAIL and is silent on INCONCLUSIVE. These data leave the probability that systems minimize J, rather than any other S + wE, where it was: D1–D4 are that whole class's comparative statics, and D5 is unscored (n = 2). The prereg's "about 0.8" is the author's probability that the test would PASS, not a prior on the hypothesis. No percentage is added here.
