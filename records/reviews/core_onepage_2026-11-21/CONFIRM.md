# Confirm of the one-page core (PR #142)

Blind confirm of `core-onepage-2026-11-21`. The incoming head was `9b464324da826c23b163a5c4c987351684085202`. This pass wrote none of that commit. It did push the wording fixes listed below, after checking them against `THEORY.md`, `theory/LAYER_LIFETIME_2026-11-21.md`, `theory/LAYERS.md`, `theory/SHANNON_2026-11-21.md`, `theory/DYNAMICS.md` CL19, `theory/FLUID_LAYERS_2026-11-21.md`, `core/KEYSTONE_NOTE.md`, `core/bridge_2026-11-21/SELECTION.md` and `RESULTS.md`, and `tests/DIR1/RESULTS_DIR1.md`. No locked prereg, `.sha256`, or `LOCK` file is in the diff. Same bot family as the other passes; not a human expert.

**READY.** At `9b46432` the nine blockers and the should-fixes were on the page, and four sentences were still stronger than their sources. Those four are corrected in this commit. The hypothesis sentence is unchanged.

## Fixes pushed in this confirm

1. Malone 1987. Dropped "and toward new forms of coordination." The Crossref abstract does not say it.
2. L3. `K^*\to\infty` **if** also `E_K\to E_\infty`, and that limit is conditional. The reviewer's "only if" reverses `theory/LAYERS.md` Theorem L3 and THEORY CT21.
3. The bridge quantity is a typical *fractional* excess of about `d/(2\sigma N_e)`. `SELECTION.md` gives `\(\mathbb{E}[J]-J^\star=d/(2\beta)\)` and `\((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\)`.
4. The five-sentence block now carries the specialized-model label, the Brownian/OU scope, and separates the known lifetime scaling from the swarm hypothesis. The opening no longer says every Part 1 sentence holds by proof. §5 states the `\(\sqrt{k}\)` scaling once. P1 is the untested field check of that exponent, not the formula. The AI sentence stays, and it is a **HYPOTHESIS**. "Smooth companion" is now the Ornstein–Uhlenbeck companion, so it is not read as CL19 (c).

`CORE.md` is 2719 words by `wc -w` (2487 before `## References`).

## 1. Blockers and should-fixes

| Item | At `9b46432` | After this confirm |
|---|---|---|
| B1. Fractal tracker. One lumpy tracker is optimal, including a fractal; refresh \((k/(wC))^{1/(2H+1)}\); square-root lifetime is \(H=\tfrac12\). | Fixed. Matches LAYER_LIFETIME §3c. \(T^*\) is no longer the fractal refresh. | Unchanged. |
| B2. One layer beats two when a joint reset costs about as little as one part. A joint reset that costs the sum does not: the specialized stack is then never more expensive. | Fixed. Matches §4, including the inequality direction. | Unchanged. |
| B3. CT21 scope, L2 degree bound, and the \(K^*\) clause. | The scope and L2 clause match. The clause said "only if," which is the wrong direction. | Fixed. "If also \(E_K\to E_\infty\)" matches CT21 and LAYERS L3. "That limit is conditional" is LAYERS's label. |
| B4. Shared-only delay and \(k_S<N k_L\); Brownian fixed-period **PROVED**, OU **NUMERICAL**; barrier keeps the sign; crossing divided by 3; equal delay cancels; \(183\ell\), \(40\ell\), \(400\ell\). | Fixed. Matches §0.2 and §5. | Unchanged. The five-sentence line now carries the Brownian/OU scope as well. |
| B5. Equal read quality does not flip the sign of \(e^{-2\ell/\tau}\). New row \(k_S<N k_L\). | Fixed. The factor is positive at equal read quality (THEORY B.11). | Unchanged. |
| B6. Chalkley 1997 exact at zero discount; Dixit 1991 the approximation. | Fixed in substance. Journal, title, and DOIs sit in `## References`. | Unchanged. Titles checked on Crossref, below. |
| B7. Malone 1987 is markets rather than hierarchies, not \(T^*\) and not the swarm limit. Malone 2004 is not evidence. | The markets sentence and the "not evidence" clause were in. The page also said "and toward new forms of coordination," which the abstract does not say. | Fixed. The 2004 ISBN and "not read" details stay in `CLAIM_SOURCES.md`. The page does not use the book as evidence. |
| B8. A store pays \(h\); no numbered "only when" theorem. CT4, CT9, CT11. | Fixed. The E1 "only when" sentence is gone. | Unchanged. |
| B9. Kill rule in THEORY §3. No Model S counterexample to N60. Rhythms counterexample (two oscillators, \(R=3\), formula 2, argmin 3) and failed IMP-N60 in `core/KEYSTONE_NOTE.md`. Convexity 120/120, not proved. | Fixed. Matches KEYSTONE_NOTE §1–§2. CT41's trichotomy is inside the §3 kill rule this sentence points at. | Unchanged. |
| Also: a stack is the cheapest design only when a layer cannot, or cannot afford to, reset the whole state (**PROVED** in that specialized model). Delay is not in that sentence. | Fixed in §2. The five-sentence line had dropped the model label. | The five-sentence line now has the label. |
| S1 scope (stationary; CX1) is on the S1 sentence only. | Fixed. | Unchanged. |
| Frontier is a set, not a single number like capacity. Ruin cap can raise the floor, no formula (**OPEN**). Both-priced least cost versus the floor and this Kalman design is **OPEN**. | Fixed. The both-priced sentence sits on the floor paragraph, which is the claim it qualifies. Sources: SHANNON §0.4, §2, §3. | Unchanged. |
| Brownian formula quantitatively false (**NUMERICAL**: \(T^*/\tau\approx 0.63\), missed by 137%). | Fixed. Matches §3b. | Unchanged. |
| Class list is THEORY §1 (cells, colonies, people, firms and cities) and the §3 exclusions. | Fixed. Brains, teams, and software agents are not on the page. | Unchanged. |
| Delete the unsourced AI sentence. | Not deleted. The owner kept a labeled hypothesis, and this confirm was told the sentence must stay labeled **HYPOTHESIS**. At `9b46432` the label was there, and the sentence also called the \(\sqrt{k}\) scaling P1 and treated AI as something that does lower \(k\). | Kept, still **HYPOTHESIS**. The scaling is **KNOWN**; P1 is the field check; that AI lowers \(k\) is unmeasured. |
| Firms fail the locked class gate (6/10 = 0.60; four zeros, no −1). | Fixed. `RESULTS_DIR1.md`: firms \(n=10\), +1 = 6, 0 = 4, −1 = 0, verdict fails. | Unchanged. |
| Palmer and Mattingly test other programmes; not preregistered; not qualified here. | Fixed. DOIs are in `## References`. | Unchanged. Abstracts and titles below. |
| Layer-lifetime P1–P3 are not T27's and not the *E. coli* checks. T27's P3 failed and is not rescued. P2 is the equal-stake §3 formula and is not the prediction when the stakes differ. | Fixed. Matches LAYER_LIFETIME §7 and `core/bridge_2026-11-21/RESULTS.md` (P3 failed 3/3, no rescue). | Unchanged. |
| The next-step bridge sentence. | Present, but "expected excess \(d/(2\sigma N_e)\)" dropped "fractional." | Fixed. See fix 3. |
| **OPEN** and **ANALOGY** are in the status-word list. The page uses both. | Fixed. | Unchanged. |
| End of §1: what is claimed as new is the package (THEORY §10). | Fixed. It is the previous core's sentence with "only input" and "the structure of its minimizer" left off. §10's own wording is the measured pattern of change as the world input. The shorter sentence is not a stronger theorem. | Unchanged. |

The support-function sentence, the free-disposal hull, the pair "gap 4.26%" and "costs 4.45% more," the factor 3, and \(183\ell\), \(40\ell\), \(400\ell\) are still on the page.

## 2. Exactness

The hypothesis sentence is byte-identical in `CORE.md` and in `THEORY.md`, once on the page: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." "Bill" and "theory of everything" are absent. "Minimize" is THEORY's word; "come close" and "sit near" are the band in THEORY §1 and §3, not a stronger claim.

**In five sentences.** The cost list matches the master equation (memory, layer upkeep, error including lateness, reads and sharing, ruin cap). "Sharing" is THEORY's name for the link, telling, and lookup term. The stack sentence is now no stronger than §4. The lifetime is the known zero-discount formula, and a lower re-form cost shortens it at fixed stake and drift; swarm-like behavior is the hypothesis, not part of the formula. Fast-local / slow-shared tracking needs shared-only delay and \(k_S<N k_L\), proved for the Brownian fixed-period case and numerical for OU. Those are the §5 conditions, not a claim that \(\tau>\ell\) is enough.

**\(T^*\) credit.** Chalkley 1997 is the exact zero-discount credit. Dixit 1991 is the approximation. That matches CL19 (a) and the Crossref titles. The coefficient 6 was not re-read from either PDF in this pass. `theory/DYNAMICS.md` already says it was not re-checked against the papers' text.

**Local versus shared.** Shared-only delay and \(k_S<N k_L\) are both required for the crossing. Equal delay cancels the floors, and speed does not flip the choice. The barrier crossing is the fixed-period crossing divided by 3. \(\tau>\ell\) is not sufficient at the check prices.

**Malone 1987.** The page now says what the abstract says: lower coordination costs shift activity toward markets rather than hierarchies. It does not attribute \(T^*\) or the swarm limit to Malone. Malone 2004 is named and not used as evidence.

**AI / swarm.** The \(k\to 0\) picture stays an **ANALOGY**. The sentence that AI lowers \(k\), and that structures then behave more like swarms, stays a **HYPOTHESIS**.

Other checked sentences, not stronger than the source: S1 floor, no layer charge, Landauer on the erasure part of \(\kappa\), Sagawa & Ueda 2009 on the sum of measurement and erasure, edge attainment, \(J_{\rm floor}/J=0.9574\) (gap 4.26%; the design costs 4.45% more) at one Gauss–Markov world; S2/S3 dual, operational least cost only when \(A=c\cdot r\) and \(L=0\), free-disposal hull, Farrell split for \(C\) only, ruin cap need not preserve convexity; spacing ratio at equal stakes; DIR1 inconclusive, 29/42, animals 20/27 support, cells \(n=5\) do not count, two class fails required, D1–D4 do not discriminate, D5 unscored at \(n=2\); 30 earlier field rows, 10 passed and 20 failed on proxy (THEORY §9); EVO1 mixed does not say the failed arms passed (Q5 and Q6 are SIM-FAIL); Karim 2016 and Girod & Whittington 2017 do not identify P2 or P3. Header SHAs `0726423`, `a97887e`, `1cb1ac2`, and `d34df95` are ancestors of this branch. `origin/main` at the start of this pass is `d34df95`.

### DOIs on Crossref, 21 Nov 2026

Every DOI in `## References`, plus the Malone DOI in the body.

| Item | DOI | Result |
|---|---|---|
| Chalkley 1997 | 10.1016/s0165-1765(97)00222-x | Resolves. *Economics Letters* 57(2):189–195, issued 1997-12. Title: "An explicit solution for dynamic menu costs with zero discounting." No abstract on the API. |
| Dixit 1991 RES | 10.2307/2298051 | Resolves. *The Review of Economic Studies* 58(1):141, issued 1991-01. Title: "Analytical Approximations in Models of Hysteresis." |
| Dixit 1991 JEDC | 10.1016/0165-1889(91)90037-2 | Resolves. *Journal of Economic Dynamics and Control* 15(4):657–673, issued 1991-10. Title: "A simplified treatment of the theory of optimal regulation of Brownian motion." The page cites the start page. |
| Palmer, Marre, Berry & Bialek 2015 | 10.1073/pnas.1506855112 | Resolves. *PNAS* 112(22):6908–6913. Abstract: retinal neurons close to maximally efficient at separating predictive information; efficient coding of predictive information. |
| Mattingly, Kamino, Machta & Emonet 2021 | 10.1038/s41567-021-01380-3 | Resolves. *Nature Physics* 17(12):1426–1431, issued 2021-11-25. Title: "Escherichia coli chemotaxis is information limited." No abstract on the API. |
| Malone, Yates & Benjamin 1987 | 10.1145/214762.214766 | Resolves. *Communications of the ACM* 30(6):484–497, issued 1987-06. Abstract: reducing coordination costs shifts activity toward markets rather than hierarchies. |

## 3. Holdability

A smart non-specialist can hold the five sentences after one read, and should not be asked to hold more than that:

1. One cost — memory, upkeep, error including lateness, reads and sharing — under a ruin cap.
2. The limits are mathematics; closeness is the hypothesis.
3. A stack is cheapest only when a layer cannot reset the whole state, and that is proved in that specialized model.
4. Lifetime scales as the square root of re-form cost (known, zero discount). Behaving more like a swarm is a hypothesis.
5. Fast local and slow shared needs delay on the shared channel only, and a shared lump cheaper than \(N\) local ones.

What will not stick, and should stay where it is:

- Do not cut \(J^*(p)=-\sigma(-p)\) or the free-disposal hull. A shorter version of that paragraph was the false one. The five sentences do not have to carry it.
- Do not cut the factor 3 or \(183\ell\), \(40\ell\), \(400\ell\). They are what stop "\(\tau>\ell\) means share."
- Do not collapse 4.26% and 4.45% into one number.
- Do not merge the **KNOWN** scaling, the **ANALOGY** at \(k\to 0\), and the **HYPOTHESIS** about AI into one sentence. That merge is what made the five-sentence line stronger than the formula. The duplicate statement of the scaling in §5 was the merge worth making, and it is made: the scaling is said once, then P1 is named as the field check.

The page is 2719 words. One read holds the five sentences. §1 is the receipt.

## Checks

| Command | Result |
|---|---|
| `python3 tools/check_fresh.py` | PASS. STATUS `main` is `a97887e`; window `d34df95 a97887e 0726423 1cb1ac2 2c32ade` |
| `python3 tools/check_consistency.py` | PASS (0 FAIL, 24 INFO) |
| `python3 tools/check_open_work.py` | PASS |
| `python3 -m pytest -q tools` | 169 passed, 1 skipped, 253.04 s. Skip: `tools/test_lean.py`, Lean 4 / lake is not installed. pytest 9.2.0, scipy 1.18.1, sympy 1.14 |

## Not a defect, and still open elsewhere

- The coefficient 6 was not re-read from the Chalkley or Dixit PDFs. The titles match the credit. DYNAMICS already records the gap.
- Mattingly's Crossref record had no abstract. The title matches the sentence.
- P2 still requires independently measured prices. The revealed-prices amendment is not applied.
- *E. coli* \(\sigma\) and \(T_{\rm red}\) are still missing in STATUS. "No system has qualified" covers that. It is not a claim this page newly makes.
