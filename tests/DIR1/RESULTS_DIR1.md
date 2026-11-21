# DIR1 results: price-free directional predictions on the published record

*Saturday 21 November 2026 (America/New_York). Scored by the locked `score_dir1.py` from `data/coded.csv` after the lock at `47c8594` (13:16:55 ET; `sha256sum -c PREREG_DIR1.sha256` OK). Not yet independently reviewed; the coding-reliability gate (blind recode of 20 systems) is pending. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." This is a directional, QC-tier test (PREREG §1, §3), not a test of the banded hypothesis.*

## Verdict: **INCONCLUSIVE** (reliability gate pending)

The FAIL condition was reachable and was not met: pooled agreement 35/46 = 0.76 (> 0.60), and no class failed. The PASS condition needed two supporting classes; only animals supported. Cells and firms each agreed at about 0.73–0.75 but had too few qualifying studies for p < 0.01.

| Class | n | +1 | 0 | −1 | Agreement | p (binomial vs ½, nulls count against) | p (sign test vs R0, nonzero only) | Locked class verdict |
|---|---|---|---|---|---|---|---|---|
| C cells / microbes | 8 | 6 | 2 | 0 | 0.75 | 0.145 | 0.016 | neither supports nor fails |
| A non-human animals | 27 | 21 | 4 | 2 | 0.78 | 0.0030 | 3.3 × 10⁻⁵ | **supports** |
| F firms / markets | 11 | 8 | 3 | 0 | 0.73 | 0.113 | 0.0039 | neither supports nor fails |
| **Pooled** | 46 | 35 | 9 | 2 | 0.76 | 2.7 × 10⁻⁴ | 5.1 × 10⁻⁹ | not FAIL |

By prediction (reported, not gated except the ≤ 0.50 rule at n ≥ 5): D1 (drift → reading) 7/9; D2 (stakes → vigilance) 7/9; D3 (relaxed selection → loss) 10/13; D4 (shocks → buffer) 11/13; **D5 (fast-local / slow-shared) 0/2, both 0** — n below 5, so not a failed prediction, but the one prediction with opposite-sign rivals got no support either way. No prediction failed.

By cell: C1 3/4, C3 2/3, C4 1/1; A1 0/1 (one −1), A2 7/9, A3 8/10, A4 6/7 (one −1), A5 0/0; F1 4/4, F4 4/5, F5 0/2. Every code with its quote is in `data/coded.csv`; every included DOI matched its Crossref title (45/45; one record has no DOI, DEVIATIONS 3), in `data/crossref_check.json`.

**Where the systems came from.** 220 records screened (20 per cell); 46 included. The locked OpenAlex strings worked for vigilance, island tameness, avian fat and price-change frequency, and badly for storage polymers (C4: 1 of 20 usable), sampling vs variability (A1: 1), social vs individual learning (A5: 0, all theory), and decentralization (F5: 2). That, not disagreement, is why cells and firms are underpowered.

## The two misses and the nine nulls, diagnosed (no locked rule changed)

- **A1, Antarctic fur seals (−1).** Less updating (multi-year site fidelity) where prey shifts are *less predictable*. *Cause: input and the claim's own exception.* "Less predictable" is not "faster drift"; and under J itself, Lemma B1 (G3) says reading collapses once the world decorrelates faster than reads pay and a fallback exists. The prereg said G3 would not rescue a miss, and it does not. It does show D1 is not a universal sign of J, which weakens D1 as a test.
- **A4, curve-billed thrashers (−1).** Same mean food, variable daily amounts: birds lost mass and drew down fat. *Cause: an assumption in the locked condition.* CT25 gives the buffer a system *needs*; it does not say the buffer can be *funded* when intake is capped. I locked "binding ruin does not flip this sign" for D4; this case contradicts that wording. The correct statement (needed buffer rises; held buffer can fall when the energy budget binds) is the CT33/PF2 mechanism, now recorded as a correction for any future lock, not applied here.
- **Nulls (0):** two retain antipredator behaviour without predators (pitvipers; rayaditos' nest defence) — the inertia / multipredator rival's prediction; elk males (vigilance serves another function); one non-significant trend (mannikins); one microalga whose plasticity "did not match simple theoretical predictions"; Myxococcus (retained in some environments, lost in others); one null cash-volatility effect (Indonesia); IT governance first decentralizes, then **re-centralizes** as uncertainty keeps rising (a hump, partly the threat-rigidity rival's sign); Mexican firms that changed structure but kept a functional mindset (a lag).

## Discrimination: what this does and does not show

- Against the **no-response rival R0** (constant effort, constant frequency, constant reserve, pure upkeep minimization), the sign test is decisive in every class (p ≤ 0.016) and pooled (5 × 10⁻⁹). Selected systems do move with J's inputs, in J's direction, 35 times to 2.
- Against **any cost-benefit optimizer** (Topkis / S + wE; menu-cost, precautionary-cash and starvation-risk models are each such optimizers), D1–D4 **do not discriminate** (PREDICTIONS §D1–D4; PRICE_FREE §2). D3 also matches neutral drift's sign; one Lenski study (C3 rank 7) attributes the loss to mutation accumulation (drift's mechanism), one yeast study (C3 rank 8) to selection on cost (J's mechanism).
- **D5**, the only prediction with opposite-sign rivals, could not be scored (n = 2). The firm-level evidence closest to it is a *performance* result (Aghion, Bloom, Lucking, Sadun & Van Reenen, F5 rank 11: decentralized firms did better in turbulence), which is a fitness ordering, not a design response, and was excluded by I2.

## Post-hoc sensitivity (labelled post hoc; does not change the verdict)

Dropping the three BORDERLINE +1 codes (C1 ranks 6 and 13, A4 rank 11) and the no-DOI record (F4 rank 14): C n = 6 (below n_min), A 20/26 (p = 0.0047, still supports), F 7/10 (p = 0.17), pooled 31/42 = 0.74. Still INCONCLUSIVE; still not FAIL.

## Threats

1. **Publication bias** inflates agreement; the prereg says a PASS would be weak evidence and a FAIL strong. Here neither happened.
2. **Abstract-only coding by an interested coder.** Mitigated by locked rules, quotes for every code, a published exclusion reason for all 174 exclusions, and the pending blind recode.
3. **Pseudo-replication** across studies of related taxa (several Podarcis lizards, several tits) is not modelled.
4. **QC is coarse.** It establishes large, long-selected, competing populations without a designer, not σ, N_e or bands. Nothing here qualifies a system under THEORY §3.

## What this does to the odds

The test could fail and did not. But it mostly confirms that selected systems are optimizers of *some* cost of J's form, which almost every rival optimizer also predicts, and the one discriminating prediction went unscored. A fair update is small: the weak version up by about 0–3 points (to roughly 72–80%), the strong and universal versions unchanged. A PASS on cells or firms with D5 scored, or a field result that separates J from other optimizers, is what would move the strong version.
