# Claim sources for the one-page CORE rewrite

Saturday 21 November 2026, afternoon ET (America/New_York). Branch `core-onepage-2026-11-21`, written against `main` `d34df95`, then revised after the hostile review of `2cc8d7e` (`reviews/core_onepage_2026-11-21/REVIEW.md`, verdict NOT READY). This file is a claim map, not a review and not a lock.

The previous `CORE.md` is frozen at `history/2026-11-21_CORE_before_onepage.md`. Word count of the revised `CORE.md` is 2571 by `wc -w` (2097 at `2cc8d7e`; 1888 at the freeze). The growth is the reviewer's required clauses, exact bibliographic credits, and the owner's AI/swarm sentence kept as a labeled **HYPOTHESIS**.

The review is committed separately. All nine blockers and the should-fixes were applied, with one override: the AI/swarm sentence was not deleted. It was rewritten as a labeled **HYPOTHESIS** and kept in §5 after Malone, as the theory's owner instructed.

## Malone

Malone is not elsewhere in the repository (a grep hits only Juni, Gureckis & Maloney 2016, a different author).

- Malone, T. W., Yates, J., & Benjamin, R. I. (1987). Electronic markets and electronic hierarchies. *Communications of the ACM* 30(6):484–497. DOI `10.1145/214762.214766`, resolved on the Crossref API on 21 Nov 2026: title, authors (Crossref given names: Thomas W. Malone, Joanne Yates, Robert I. Benjamin), container, volume, issue, pages, and issued date 1987-06 all match. The Crossref abstract says lower coordination costs shift activity toward markets rather than hierarchies. The page uses that sentence, plus "and toward new forms of coordination," and does not attribute the \(\sqrt{k}\) lifetime or the swarm limit to Malone.
- Malone, T. W. (2004). *The Future of Work: How the New Order of Business Will Shape Your Organization, Your Management Style, and Your Life.* Harvard Business School Press, Boston. ISBN 978-1-59139-125-8 (also 1591391253). Crossref filter `isbn:9781591391258` and `isbn:1591391253` returned zero works. No book-level DOI is given, and none was invented. The page says the book was not read for this page and is not evidence for \(T^*\) or the swarm limit. Publisher copy describes decentralized forms under falling communication costs.

## Claim-to-source mapping

Claims are in reading order. Labels on the page are those of the source unless noted. Replacement text from the review is used where given.

| Page claim | Source | Notes |
|---|---|---|
| Two-part split | Previous `CORE.md`; SHANNON §0 | |
| Hypothesis sentence, byte-identical | `CORE.md`, `THEORY.md` §3 | Once on the page. |
| Master equation and term glosses | Previous `CORE.md` §1; `THEORY.md` §3 | Definition. Notation \(\varepsilon\), not THEORY's \(\varepsilon_r\). |
| S1 floor, no layer charge, Landauer, Sagawa & Ueda, edge attainment, \(0.9574\) scoping | SHANNON §0–§3; previous `CORE.md` §2 | CX1 scope is now on the S1 sentence only, not on all of Part 1 (should-fix). |
| Both-priced least cost vs the information floor and this Kalman design is OPEN | SHANNON §3 | Restored clause. |
| Frontier is a set, not a single number like capacity; \(J^*=-\sigma(-p)\); operational least cost only if \(A=c\cdot r\) and \(L=0\); free-disposal hull of the Pareto face; Farrell split for \(C\) only; ruin cap need not preserve convexity | SHANNON S2, S3 | Restored "not a single number like capacity." |
| A binding ruin cap can raise the information floor; no formula for that rise is derived (OPEN) | SHANNON §2 | Restored clause. |
| Part 2 technical / allocative split; strongly selected operational in THEORY §3; no system has qualified | SHANNON §5; THEORY §3; STATUS; DIR1 | |
| What is claimed as new is the package (THEORY §10) | Previous `CORE.md` credit paragraph; THEORY §10 | One sentence at the end of §1, per the review. |
| No information argument forces a layer | SHANNON §2 | |
| A store pays \(h\); whether it beats a memoryless rule is that upkeep vs the drop in the other terms; no numbered theorem in these words (CT4, CT9, CT11) | Reviewer replacement for blocker 8; THEORY §6 | The previous "only when" sentence was the recorded error E1 and was removed. |
| A stack is the cheapest design only when a layer cannot, or cannot afford to, reset the whole state (PROVED in that specialized model) | Reviewer replacement; LAYER_LIFETIME §4 | "Appears" and "especially when shared information arrives late" were cut. Delay stays in §4. |
| One lumpy tracker is already optimal for a single process, including a fractal one (PROVED). Refresh \((k/(wC))^{1/(2H+1)}\); square-root lifetime is \(H=\tfrac12\) | LAYER_LIFETIME §3c; reviewer replacement for blocker 1 | The previous sentence attached \(T^*\) to a fractal process and overstated §3c. |
| One layer beats two when a joint reset costs about as little as one part (PROVED). A joint reset that costs the sum does not: the specialized stack is then never more expensive | LAYER_LIFETIME §4; reviewer replacement for blocker 2 | "Cheaper than the parts" was too broad. |
| CT21, linear-Gaussian, squared-error, counted by degree. Finitely many real modes: at most the predictive degree (L2). Non-rational spectrum: \(E_K>E_\infty\) for every finite \(K\), and \(K^*\to\infty\) only if also \(E_K\to E_\infty\) (L3). \(T^*\) does not compute \(E_K\). Layer-term floor OPEN | THEORY CT21; LAYER_LIFETIME §3c (confirm defect 3); reviewer replacement for blocker 3 | The dropped \(K^*\) proviso is restored. |
| \(T^*=\sqrt{6k/(w\sigma^2)}\) | LAYER_LIFETIME §2; FLUID_LAYERS; CL19 (a) | |
| Exact at zero discounting: Chalkley 1997, *Economics Letters* 57:189, doi 10.1016/s0165-1765(97)00222-x. Dixit 1991 is the approximation that case makes exact (RES 58:141, doi 10.2307/2298051, title "Analytical Approximations in Models of Hysteresis"; JEDC 15:657, doi 10.1016/0165-1889(91)90037-2) | Reviewer replacement for blocker 6; `theory/DYNAMICS.md` CL19 (a); Crossref 21 Nov 2026 | |
| Smooth adjustment: no discrete lifetime (CL19 (c)) | LAYER_LIFETIME §2 | |
| Brownian formula quantitatively false when \(T^*\) is not short compared with the correlation time (NUMERICAL: \(T^*/\tau\approx 0.63\) missed by 137%) | LAYER_LIFETIME §3b; reviewer should-fix | "Mis-times" was too soft. |
| Spacing ratio at equal stakes, specialized stack; not a universal geometric series | LAYER_LIFETIME §0.1, §3a | |
| Fast-local / slow-shared crossing needs shared-only latency and \(k_S<N k_L\). PROVED for Brownian fixed-period; NUMERICAL for OU. Barrier keeps the sign; variance-rate crossing is the fixed-period crossing divided by 3. Equal observation delay: floors cancel, speed does not flip the choice. \(\tau>\ell\) not sufficient; \(183\ell\), \(40\ell\), \(400\ell\) at the check prices | LAYER_LIFETIME §0.2, §5; reviewer replacement for blocker 4 | |
| Nesting factor \(e^{-2\ell/\tau}\) at equal read quality (CT28, CT34) | THEORY B.11 | The factor stays positive (blocker 5). |
| THEORY §1 class list (cells, colonies, people, firms and cities); §3 exclusions (cities, nation-states, global economies, the biosphere) until a population proxy is preregistered | THEORY §1, §3; reviewer should-fix | Brains, teams, and software agents were not the theory's list and were removed. |
| \(T^*\) shrinks as \(\sqrt{k}\) (KNOWN from the formula). As \(k\to 0\), the swarm limit (ANALOGY, not a field result) | FLUID_LAYERS; LAYER_LIFETIME | |
| Malone 1987: lower coordination costs shift activity toward markets rather than hierarchies, and toward new forms of coordination. Not \(T^*\) and not the swarm limit. Malone 2004 not read; no Crossref DOI | Reviewer replacement for blocker 7, with the owner's requested narrowing of the 1987 sentence | Abstract supports markets rather than hierarchies. |
| Since \(T^*\) scales as \(\sqrt{k}\), anything that lowers \(k\), including AI, shortens layer lifetimes, so structures should re-form more often and behave more like swarms (HYPOTHESIS; the \(\sqrt{k}\) scaling is P1, and that AI lowers \(k\) is unmeasured) | Owner override of the reviewer's should-fix to delete the AI sentence. The \(\sqrt{k}\) scaling is the page's own formula / P1; that AI lowers \(k\) is unmeasured | Kept in §5 after Malone, not in §2. Labeled **HYPOTHESIS**. |
| Assumptions table, including \(k_S<N k_L\) and the corrected equal-read-quality row | Reviewer blocker 5; LAYER_LIFETIME §5; THEORY B.11 | |
| DIR1 INCONCLUSIVE; 29/42; animals 20/27 support; firms fail the locked class gate (6/10 = 0.60; four zeros, no −1); cells \(n=5\); kill not met; D1–D4 do not discriminate; D5 unscored \(n=2\) | `tests/DIR1/RESULTS_DIR1.md` | The signs did not reverse. |
| Karim 2016 and Girod & Whittington 2017 do not identify P2 or P3 | LAYER_LIFETIME §7 | Unchanged, and the review agreed. |
| 30 earlier field rows NOT A TEST (10 passed, 20 failed on proxy) | THEORY §9; STATUS | |
| EVO1 mixed, in-model only | Previous CORE; tests/EVO1 | Compressed; does not say failed arms passed. |
| Palmer et al. 2015 test efficient coding of predictive information in the retina (doi 10.1073/pnas.1506855112). Mattingly et al. 2021 test an *E. coli* chemotaxis bound (doi 10.1038/s41567-021-01380-3). Consistent with the technical half; not preregistered or qualified here | SHANNON §0.6; reviewer should-fix | Naming the other programmes keeps them from being counted as tests of this one. |
| Layer-lifetime P1–P3, not T27's and not the *E. coli* discrimination checks. T27's P3 failed in-model and is not rescued. P2 is the §3 equal-stake formula and is not the prediction when stakes differ | LAYER_LIFETIME §7; `core/bridge_2026-11-21/`; STATUS; reviewer should-fix | Name collision stated in the lead-in. |
| Kill rule, including CT41, stays in THEORY §3 | THEORY §3 | Header points here, not to a Model S counterexample. |
| Rhythms counterexample (two oscillators, \(R=3\), formula 2, argmin 3) and failed IMP-N60 stay in `core/KEYSTONE_NOTE.md`. Convexity inside Model S is numerical (120/120), not proved. There is no Model S counterexample to N60 | `core/KEYSTONE_NOTE.md` §1–§2; reviewer replacement for blocker 9 | |
| Next: axiom-level proof of closeness. An in-model bridge already gives expected excess \(d/(2\sigma N_e)\) under weak mutation and fitness linear in \(J\); its P3 failed and is not rescued; the proof still to write does not assume that bridge | Reviewer should-fix; `core/bridge_2026-11-21/` | |
| Pointer `current to \`main\` \`d34df95\`` | `tools/brief.py` / `tools/check_fresh.py` family | STATUS and OPEN_WORK still say `a97887e`, inside the five-commit window. |

## Still-live caveats

Restored as one-clause pointers or in-place corrections, per the review:

- Rhythms counterexample, IMP-N60 failed, Model S convexity unproved (header; not "the Model S counterexample").
- The frontier is not a single number like capacity (§1).
- Achievability when memory and reads are both priced (§1, OPEN).
- A binding ruin cap can raise the floor; the rise has no formula (§1, OPEN).
- Palmer and Mattingly test other programmes (§7).
- T27 P3 failed and is not rescued; the page's P1–P3 are the layer-lifetime sketch (§7–§8).
- Chalkley 1997 is the zero-discount exactness credit (§3).

Still pointed and in force: the kill rule, including the CT41 trichotomy, in THEORY §3. P2 still requires independent prices, so the revealed-prices amendment remains unapplied. "No system has qualified" covers the dropped instruction to source *E. coli* \(\sigma\), \(N_e\), and \(T_{\rm red}\) before rescoring.

Superseded: "the directional field test is in progress." DIR1 is scored.

Still true, and not a claim this page makes: cymatics; the 24 pre-#116 worlds; N60 cannot return \(K^*=0\); the EVO1 arm scores.

## Uncertainties that remain

1. **Cost-covered persistence** is in THEORY §1 and in the planned selection-proof axioms, but it is not a numbered, refereed axiom in the merged tree. It remains in the assumptions table because the page relies on it for why selection would care about \(J\).
2. **"And toward new forms of coordination"** was added to the 1987 Malone sentence at the owner's request, next to the abstract's markets-rather-than-hierarchies wording. The abstract does not use the phrase "new forms of coordination."
3. **The AI/swarm sentence** is a labeled **HYPOTHESIS**, kept after Malone by the owner's override of the reviewer's deletion should-fix. The \(\sqrt{k}\) scaling is P1 / the formula; that AI lowers \(k\) is unmeasured, and the page says so.
