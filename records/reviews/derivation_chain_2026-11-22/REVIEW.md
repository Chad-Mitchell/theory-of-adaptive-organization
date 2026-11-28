# Review of draft PR #169

**Verdict: READY-WITH-FIXES.**

Head `93047edaca2790f336be43b39182885db7a865e0` on `derivation-chain-2026-11-22`, three commits on `origin/main` `5fa4b8c`. Diff against that main: `theory/DERIVATION_CHAIN.md` plus pointer lines in `OPEN_WORK.md`, `CORE.md`, `theory/SELECTION_AXIOMS.md`, `theory/README.md`, `theory/DIRECTIONS_2026-11-22.md`, and `STATUS.md`. No `CLAIM_MAP` diff. No `lake build`. This review does not edit that branch.

No blocker. No claim-map status word in the chain's tables is the wrong word. The should-fixes are local: a wrong family name, two wrong row attachments, a Lean hypothesis attached to the wrong declaration, an iff that picks up a fourth assumption, a diagram that does not use the row words, one failure-table witness taken from a different limit, and two pointer sentences that are not true of `origin/main`. An outside reader who uses the tables and the cited notes will not be told that an open row is proved. An outside reader who trusts the diagram, the lifetime parenthetical, or the disagreements section will be told something the source does not say.

## What holds

Checked against `measurement/CLAIM_MAP_v2.md` at v2.81 and the cited notes.

- R1 **PRIOR ART**, R2 **PROVED (in-model)**, R3 **OPEN**. The stationary weight, \(\beta=\alpha\nu\), haploid \(\nu=N-1\), diploid \(\nu=2N-1\) as an approximation, \(d/(2\beta)\), and the fractional form with \(N_e=\nu\) match section R and `theory/SELECTION_AXIOMS.md` §2–§4. The factor 10 is the repository's choice, not Lynch's, in THEORY §3 and the selection note §3.
- GF1–GF5, GB1–GB7, and V1, V2, V4, V5, V6 carry the status words in the map. The published digits match the rows: LY-1 \(\lambda=-0.804718956\) and \(0.095310180\) on designs \((1,0)\) and \((2,0.4)\); invasion gap 2; Kelly \(q^\star=0.26\) against \(1.235\) and \(1.0425\); \(\tau_S=0.2362\), \(\tau_E=0.3162\); the GB4 quartet and the interval \([0.183706411069,\,0.299049733488]\); \(\tau_J=0.309679835108\); \(\lambda_B=-0.010274369557\); stake \(0.2\) against \(0.99\); diffusion limit \(-0.05\) at \(\mu=0.2\), \(\sigma^2=0.5\); dent \(C=(0.6,0.6)\); shares \(0.528\) and \(0.472\) summing in elasticity to \(1.147\); quartic mean \(1/(4\beta)\); efficiency \(J_{\mathrm{floor}}/J=0.9574\).
- CT1, CT4, CT7, CT8 (alias of K6), CT9, CT10, CT11, CT12 (alias of N7), CT14 (alias of B2), CT19, CT20, CT21, CT22, CT24, CT25, CT26, CT27, CT30, CT33, CL1, CL19, N60, N64, N67, N68, P9, PD1a, PD2–PD5, PD1b, PD6, PD7, PD8, CX1, CX2, J3, J6, N13, N27, N51, N52, N54–N57, K4, K7, U6, U7 match the status column. K4's full label **NOT A TEST (qualification not established; proxy: failed)** is the map's label. J3 **WITHDRAWN** is stated as the map states it: the theory as a whole is not called a law.
- Lean names that exist and are scoped as the chain says: `Equipartition.gibbs_excess_quadratic`, `LayerLifetime.barrier_band_identities` (the identity, not the input clause), `FiniteDesignMenu.J`, `LocalShared.switch_iff` (iff \(\ell>0\) and \(k_S<N k_L\)), `N60Exact` for the from-0 direction and the converse under positive distinct decrements. The "not formalized" list in `formal/lean/README.md` covers SA1, the per-process \(\beta\), the well-supported approximation, SA2 as a selection statement, the fractional form, CT21, CT22's multiplier, \(f^\star\) in \(w/c\), CT1, CT7, CT8, CT9, the hypothesis, and Model S convexity. No viability declaration is in that file.
- Theorem GF-3 does say nonnegative additive \(J\) with a half-space cap is the special case **exactly when** (R-a), (R-b), and (R-c) hold (`theory/GENERAL_FORM.md` §5). Occupation of the front is outside GF1's proved claim. V5 stays **OPEN**. GB5 and GB6 are **FALSE**. The master equation is THEORY §3's statement of the problem. The five-part qualification (a)–(e), the band \(\varepsilon=10/(\sigma N_e)\), and the exclusion of cities, nation-states, global economies, and the biosphere match THEORY §3. "No system has yet been shown to qualify" is CORE §7.
- Master Theorem (iii) is in the chain as the CT21 row (the world caps the layers, counted by degree). It is not labeled "(iii)". The prose that says parts (ii) and (iii) were restated is THEORY §5.

## Blockers

None.

## Should-fixes

1. `theory/DERIVATION_CHAIN.md:205`. The lifetime row says CL19 **PRIOR ART**, which is the right status, and then "the formula is the Brownian case of CT25's family." That family phrase occurs nowhere else in the repository. CT25 is the per-window buffer \(B\ge z_\varepsilon\sigma\tau^H\), **PROVED (in-model)**. \(T^\star=\sqrt{6k/(w\sigma^2)}\) is the minimizer of the average cost \(k/T+w\sigma^2 T/6\), prior art as CL19 (Dixit, Chalkley). `theory/GENERAL_FORM.md` §6 lists the same assumptions the chain lists and does not derive \(T^\star\) from CT25. Drop the family clause. The Lean sentence on that row is right: the unique minimizer of the given average cost is machine-checked, and the stochastic derivation is an input.

2. `theory/DERIVATION_CHAIN.md:178`. "Antitone front | V6 **PROVED (in-model)**; S2 in `theory/SHANNON_2026-11-21.md`." V6's antitone claim is the definition of Pareto (`theory/GENERAL_FORM.md` §6; `theory/REPRESENTATION.md` §7). Theorem S2 is the support function \(J^\star(p)=-\sigma_{\mathcal{F}}(-p)\). The chain says that correctly at line 186. S2 is not the antitone theorem. Take S2 off the antitone row.

3. `theory/DERIVATION_CHAIN.md:179`. "A Pareto point exists | F-0, inside the general-form note; V6." F-0 is the compactness argument in `theory/GENERAL_FORM.md` §3 and the price-free line of GF4. The V6 row does not state it. Cite GF4. Do not cite V6.

4. `theory/DERIVATION_CHAIN.md:50`. `LayerLifetime.barrier_band_identities` proves \(w b^{\star 2}/6=\sqrt{kw\sigma^2/6}\) from \(k,w,\sigma^2>0\) and \(b^{\star 2}=\sqrt{6k\sigma^2/w}\) (`formal/lean/GTAO/LayerLifetime.lean`, the theorem comment and the statement). It does not take the average-cost expression as an input. That input belongs to the \(T^\star\) minimizer, which line 206 already states correctly. Line 50 should say the identity is algebraic in \(b^\star\).

5. `theory/DERIVATION_CHAIN.md:122`. "Four further assumptions" and then "exactly when they hold." Theorem GF-3's iff is three clauses: (R-a), (R-b), (R-c). The fourth item in the table, the term list, is an input (selection note §2, growth bridge §6, GF2). V4 and V5 stay **OPEN**. The table is right. The sentence that says "exactly when" is not. Restrict the iff to the three clauses.

6. `theory/DERIVATION_CHAIN.md:74`. "H1 is representation A7 and THEORY's standing exogenous world (S-W)." S-W is A7: the law of the world does not depend on the design (`theory/GENERAL_FORM.md` §2; `theory/REPRESENTATION.md` A7). H1 is that, plus ergodicity, plus offspring depending only on the design and the environment. H3 is the vector form of A2-M, which the chain does not say. Say H1 includes S-W. Do not identify them.

7. `theory/DERIVATION_CHAIN.md:112`. Theorem GB-menu requires \(\varepsilon|X_i|\le 1/2\) almost surely and a finite third moment, plus a unique mean leader and a fixed gap (`theory/GROWTH_BRIDGE.md` §3; GB1). The chain states the leader and the gap, and puts \(|W-1|\le 1/2\) only on the diffusion line, where it is also required. Put the menu bound and the third-moment hypothesis on the menu sentence.

8. `theory/DERIVATION_CHAIN.md:48`. The fractional form is given as needing \(J^\star>0\) and \(N_e=\nu\). `theory/GENERAL_FORM.md` §6 also requires the zero of the cost fixed. V1 says the fractional excess moves with the additive constant. Add that hypothesis. The same paragraph's R2 sentence names SA2-A, SA2-B, and SA2-C and then "including zero discount and the lumpy coordinate off the substitution chain." Theorem SA2 also requires that the optimum move only in that coordinate, that a reset change only that coordinate, and that some mutation rate satisfy both \(N\mu\ll 1\) and \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\). The note says that if no mutation rate satisfies both, SA2 is not claimed (`theory/SELECTION_AXIOMS.md` §4). Those clauses are part of the claim, not optional color.

9. `theory/DERIVATION_CHAIN.md:238`. The condition is "the menu gap is not large next to \(\varepsilon\), or the noise is not small," and the witness is GB3's mean excess \(0.01\) and the stake \(f=0.2\) against \(0.99\). Both digits are in the GB3 row. GB3, and `theory/GROWTH_BRIDGE.md` §3, say the weak-selection menu of GB1 is a different limit: the gap stays fixed while \(\varepsilon\to 0\), and the second-moment term cannot flip it. The \(0.01\) pair has \(\mathbb{E}[X]=0.05\) and is not that menu. The stake pair is the interior-stake separation, which is the next sentence of the chain's own §5, not a small-noise failure of GB1. The menu that agrees at small \(\varepsilon\) and flips at larger \(\varepsilon\) is the three-design check in `theory/GROWTH_BRIDGE.md` §9. Point the GB1 failure at that check. Leave the \(0.01\) pair and the stake on the GB3 rows, where line 239 already puts the diffusion limit \(-0.05\).

10. `theory/DERIVATION_CHAIN.md:60` and `:305`. Section 2 cites `theory/SCALE_ENDS.md` §6b for a persistence-only version of Theorem P. That is the bullet in §6b. Disagreements item 4 cites §3.4 for the same open item. §3.4 is the switch-on threshold under Kelly-type fitness. The selection note's A2-P points at §6b, not §3.4. Change item 4 to §6b. Separately, "the counterexample in the row" at line 60 for scores \((1,0.2)\) and \((0.5,0.2)\) is the counterexample in `theory/GENERAL_FORM.md` §3 (iv). The GF1 row's named counterexamples are the \(\lambda\) pair and the invasion gap. The pair, the ruin probabilities, and the dominance claim match (iv). Attribute them to (iv).

11. `theory/DERIVATION_CHAIN.md:13–37`. The diagram's status words do not match the rows.
    - VK says "GF1 derived." LY and TR say "GF1 proved in-model." The row is **PROVED (in-model)**. Closeness open is A2-P / §6b, not a second status of GF1. Use one status word on all three nodes.
    - GB says "GB1 limit" and "GB5 and GB6 false." GB1 and GB4 are **PROVED (in-model)**. GB2, GB3, GB5, and GB6 are **FALSE**. GB7 is **OPEN**. "Limit" is the document's label for GB1, not the row's status word. The false rows that are named are named correctly.
    - IN says "assumed, V1 V2 GF3." The inputs are assumed. V1, V2, and GF3 are **PROVED (in-model)** classifications. A reader of the figure alone will take those rows as assumptions.
    - The edge AX → LY draws Lemma LY as a consequence of the selection axioms. The lemma's premises are H1–H3. The general-form note starts by refusing A1 and A2-L, which already take a scalar \(J\). H3 is related to A2-M. It is not a theorem of the selection package. Drop that edge, or start LY from H1–H3.

12. `theory/DERIVATION_CHAIN.md:258`. "Every theorem from §7 on uses" the objective (term list, risk-neutral currency, linear prices, half-space cap). Section 9.1's price-free lines do not: the antitone front, existence, the information floors, CT8, CT25's buffer shape, and L3's \(E_K>E_\infty\). The objective is still the right first link for the master equation, the stake-or-ratio theorems, and the rules that minimize \(J\). Narrow the sentence. The order can stay. See below.

13. `theory/DERIVATION_CHAIN.md:188`. "PD1a–PD5 **PROVED (in-model)**; PD1b and PD7 **PRIOR ART**." PD1a and PD2, PD3, PD4, PD5 are **PROVED (in-model)**. PD1b is **PRIOR ART**, and a dash range from PD1a to PD5 is the usual way to include it. The exception is in the same sentence, so a careful reader is safe. Write "PD1a and PD2–PD5" so the range does not swallow PD1b. PD6 **PROVED (in-model)** and PD8 **OPEN** are already right. CX1 **OPEN** is right. The section T header in the claim map still says the confirm is pending; the chain's disagreements item 6 already says OPEN_WORK T11 was left stale. Do not promote those rows while saying that.

14. `theory/DERIVATION_CHAIN.md:317`. "STATUS already pointed at `main` `5fa4b8c`." `origin/main` is `5fa4b8c`, and `git show origin/main:STATUS.md` still says `main` is `2d9a812` (PR #165). This PR is the edit that changes STATUS to `5fa4b8c` (PR #168). The SHA is the right one. The word "already" is not. Say this pass updates STATUS.

15. `theory/DIRECTIONS_2026-11-22.md:6`. The sentence still opens "Finish the classical math now in review" and marks only PR #154 as merged. PR #153 is merged as `f84997c` (confirm #159 `37794bb`). PR #155 is merged as `886d69b` (confirm #160 `eddf64e`). This same PR's OPEN_WORK T19 already says #155 is merged. Item 1 cannot stay "now in review" for those two. V5 **OPEN** on line 16 is unchanged and correct. §1.1's "likely a special case" is still the directions text, and the chain's disagreements item 2 quotes it fairly. §1.2's bullets do match GF4's stake split and GF3's cap. That part of item 2 holds.

16. `theory/DERIVATION_CHAIN.md:295`. "the safety-factor ratio is credited to inventory (CL4, CT25, THEORY §10)." THEORY §10 says the ratio \(z\) is the inventory safety factor, and that first passage is Black and Cox. CL4 is that first-passage formula, **PRIOR ART**, credited to Black and Cox. CT25's row credits Black and Cox for the same passage. Cite THEORY §10 for the inventory sentence. Do not cite CL4 as the inventory credit.

17. `theory/DERIVATION_CHAIN.md` §1 and §8. A3 says the world may drift. The drifting excess the chain develops is R2's lumpy band, with the lumpy coordinate off the substitution chain. CORE §8 sends a moving optimum in the soft coordinates to `theory/DRIFT_SELECTION.md`. That note is section S: S1 (DS1) **PRIOR ART**, S2 **PROVED (in-model)**, S3 and S4 **OPEN**. N66 **PROVED (in-model)** is the one-coordinate lattice-to-diffusion bound DS1 uses, and it does not cover an OU centre. The chain does not mis-state these rows. It skips them. One sentence, with those status words, stops a reader from taking the lumpy band as the whole drifting excess. Do not call S1 proved.

## Weakest links

The order is defensible. I would not reorder it.

The stated rule is how much of the derivation hangs on the assumption, and how little is known in its favor. Rank 1 is the objective. V2, GB3, and GB5 are proved separations, so the support for reading this \(J\) as the output of growth is those separations. That is the right first place, once sentence 258 is narrowed to the master equation, the stake-or-ratio theorems, and the rules. Rank 2 is H3. It carries Lemma LY, the identified front, and the refusal of a dominated design. It is not an input to \(J\) once §6 is granted, and GB6 is **FALSE** for "from first principles." Rank 3 is A2-L plus the identification of this \(J\) inside that map. The weight is R1 once the map is granted, and the map is not derived. Rank 4 is the five-part definition of strong selection. It gates every sentence about nature, and CORE §7 is right that no system has been shown to qualify. It does not gate the in-model derivation. Putting it under the mathematical assumptions matches the document's own job. Rank 5, the exogenous world, is a standing assumption with CX2 **OPEN**; the floors and H1 hang on it, and a great deal is already proved under it, so it belongs below the assumptions that are known to fail. Rank 6 is right to confine convexity to the closed-form count: \(K^\star=\arg\min J\) does not need it, N60 is conditional, N68 is **OPEN**, N67 is only the weak third mode, and the two-oscillator counterexample (\(R=3\), formula 2, argmin 3) already breaks the increment formula. Rank 7 is right: joint achievability moves a numerical efficiency (\(0.9574\)) and does not rewrite \(J\). The S-A footnote is right: \(A\ge c\cdot r\) is an assumption in Shannon §2, load-bearing for the assembled floor, and narrower than rank 1.

If the audience is only the hypothesis about nature, strong selection would sit second, ahead of H3, because H3 never reaches a prediction about a real system and the qualification gate does. That is a different ranking rule from the one the section states. I would not make that swap a fix.

## Ours versus known

Checked against `theory/NOVELTY_NOTE_2026-11-21.md`, THEORY §10, `litmap/PRIOR_ART.md` (14 Nov 2026, plus the 21 Nov cache row), Shannon §6, the selection note §0 and §7, `theory/REPRESENTATION.md` §0 and §10, `theory/GENERAL_FORM.md` §8, and `theory/GROWTH_BRIDGE.md` §7.

The two review sentences are in `reviews/master-equation_2026-11-19/REVIEW.md`: "Modest synthesis, not a new result" (item 2) and "a genuine but elementary contribution" (the paragraph that begins "What I did not find stated together"). The novelty note quotes both. The chain is right to keep both, and right that "not found" is the word THEORY §10 uses. The search is not exhaustive. That limit is in the chain.

Spot checks that match the notes' own citations: Aubin, doi 10.1007/978-0-8176-4910-4, issued 2009, for the viability kernel. Debreu 1954, doi 10.1073/pnas.40.7.588, for supporting prices, kept separate from the additive-representation reprint doi 10.1017/ccol052123736x.010. Sella and Hirsh 2005; Tenaillon, Silander, Uzan and Chao 2007, from Hartl and Taubes 1998 and Poon and Otto 2000, for \(d/(2\beta)\). The R1 row's own parenthetical is "Credit (v2.74)." Gillespie 1977 for selection on offspring-number variance, and Gillespie 1974 kept as the \(O(1/N)\) term. Lewontin and Cohen 1969, Haldane 1927, Feller 1951, Iglehart 1969, and Cramér's survey as the growth bridge §7 lists them. Kelly 1956. Aczél, Forte and Ng for the nonnegative cone generated by the Shannon and Hartley entropies (representation A6). Lynch et al. 2016 for the drift-barrier scale only. Alchian 1950 is THEORY §9, where the chain puts it. Farrell 1957, Debreu 1951, and Shoval et al. 2012 are Shannon §6. Neuhoff and Gilbert, Tatikonda, Sahai and Mitter, Tanaka et al., and Kostina and Hassibi are the same section. PRIOR_ART's bottom line does say rules 1–7, taken one by one, are prior art. The cache row is grade 0 and points at `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md`, which says the cache-domain level count, geometric spacing, and fixed shares are novelty 0. The chain's sentence on Chow is that claim, not a claim that T20(A) was already in Chow. The note itself refuses that stronger claim. The chain does not make it.

The pending-list gloss "square-root evaporation rule" is PRIOR_ART's "T4 √N evaporation rule." The temperature item in PRIOR_ART also says "fix-mechanism universality classes," which the chain drops. Neither slip reopens a row. The CL4 mis-cite in should-fix 16 is the one that should change.

The packaging paragraph matches GENERAL_FORM §8 and GROWTH_BRIDGE §7: the Lyapunov comparison, the trichotomy, the split between a mentioned slot and H3, and the false sentence that a small-noise limit yields the master equation. Shannon §0 and §7 do say the added pieces are a price per layer and the ruin cap, still without a formula for the fewest layers. The chain does not claim a new theorem there.

## Pointer cleanups

`git diff origin/main...93047ed -- measurement/CLAIM_MAP_v2.md` is empty. No row status moved.

- OPEN_WORK header: `main` `5fa4b8c`, CLAIM_MAP v2.81, v2.71 merged with PR #144 (`c92886a`). Those SHAs are on `origin/main`. T19 changes one clause, from draft PR #155 not merged to merged as `886d69b` with confirm #160 `eddf64e`. The rest of the T19 cell is the previous text. The axiom-audit count and the list of what is not formalized are untouched.
- CORE header and close: `d34df95` to `5fa4b8c` (PR #168). The convexity sentence now says N67 is proved for a weak third mode and N68 stays open. N67 is **PROVED (in-model)** for that weak third mode. N68 is **OPEN**. The old sentence, "Convexity inside Model S is numerical (120/120), not proved," was the broader claim and was stale after N67. The 120/120 figure remains in the N68 row. This reports the existing rows. It does not change them. CORE's legend, two lines above, still defines PROVED as proved inside the stated model.
- Selection-axioms header: the THEORY §4 fold merged with PR #144. The body already had \(\beta=\alpha\nu\). The hypothesis sentence at line 13 is untouched.
- `theory/README.md`: "THEORY v2.9 draft" matches the THEORY title. The new index row says the chain adds no claim.
- Directions: V5 stays **OPEN**. The §1 header now says PR #154 merged (`fb6c17f`, confirm #157 `797b14b`), which is true. Should-fix 15 is the leftover "now in review."
- The chain's list of what was left stale is true. OPEN_WORK T11 still says draft PR #149 is not merged. PR #149 is on main. `theory/GENERAL_FORM.md` line 3 still says branch `general-form-2026-11-22`. The note is on main (PR #161, confirm #164). OPEN_WORK T32 still says it needs a reviewer.

The hypothesis sentence is byte-identical, one copy each, bold markers included, in `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and `theory/DERIVATION_CHAIN.md:7`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

The same bytes appear in `theory/GENERAL_FORM.md`, `theory/GROWTH_BRIDGE.md`, `theory/COADAPTATION.md`, and, inside quotation marks, in `theory/DIRECTIONS_2026-11-22.md`. This PR does not change any of those lines. `git diff origin/main...93047ed` does not touch the sentence.

`theory/DERIVATION_CHAIN.md` contains no "bill," no "kill," no "verdict," and no "theory of everything." The pointer diff does not add those words. CORE line 115, whose last clause this PR rewrote, still begins with the pre-existing "operational kill rule." The selection-axioms header still contains "verdict NOT READY," which this PR did not write. Both are the repository's existing terms for the miss rule and for an earlier review. They are not in the chain.

## Readability

A mathematically literate outsider can follow the spine: the hold-this paragraph, then each link's statement and status, then the failure table. The status tables are the part that will survive a hostile reading. Three obstacles are real and are not, by themselves, fixes:

- The row prefixes (GF, GB, V, CT, PD) are not glossed once. The disagreements section's warning that selection A1–A3, representation A1–A8, and Appendix B's A1–A5 are different alphabets arrives at item 5, after the chain has used all three. That warning is correct. It belongs next to the first use.
- The hold-this sentence "picks one argmax" is a set. Section 4 says the set may be one point. "Never keeps a dominated design" is the maximizer claim under H1–H3; the sentence's "when" clause states H3 and not H1 or H2. Section 3 states the lemma correctly, including LY-2.
- The twelve-decimal constants are computed outputs of the notes, not closed forms. They match. A reader who has not opened the notes cannot see that.

I would send this to an outside reviewer after the should-fixes, not before. I would not ask them to reconstruct the chain from the diagram alone.

## Commands

`git fetch origin main` moved `origin/main` from `2eeab30` to `5fa4b8ca6b14fe99cb35452e2f43c203e8692d74`. Merge-base with HEAD is that commit. The PR is the three commits `e2173c2`, `733a40e`, `93047ed`.

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT PASS. Exit 0. FAIL: 0. Soft length warnings on THEORY.md and README.md, not failures. |
| `python3 tools/check_fresh.py` | RESULT PASS. Exit 0. STATUS main is `5fa4b8c`. Window: `5fa4b8c f3a8fd0 2d9a812 01e4415 2dd04fa`. |
| `python3 tools/check_open_work.py` | RESULT PASS. Exit 0. items.json not-DONE 62; QUEUE.md not-DONE 90; union missing from OPEN_WORK.md: 0. |
| `nice -n 19 python3 -m pytest -q tools` | 252 passed, 1 skipped, 303.41s. Exit 0. |

The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed." No `lake build`. This environment had no pytest at the start. pytest 9.2.0, NumPy 2.5.5, SciPy 1.18.1, and SymPy 1.14.0 were installed for the run and were not committed. The PR body's "252 passed, 1 skipped" matches this run.
