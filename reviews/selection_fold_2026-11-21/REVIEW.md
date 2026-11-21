# Independent hostile review: PR #144 (selection fold)

**Reviewer:** independent. Wrote none of the fold. The only file added by this review is this one.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/144
**Head reviewed:** `710565a981919ee01458cdde6d2779f26f3aed89` on `selection-fold-2026-11-21`, base `2eeab306ce1e50a3d8a8e658906b7e2401310998` (`origin/main`). Draft. Not merged.

**Verdict: NOT READY**

The bridge exponents, the holdability cuts, the Sella & Hirsh credit, the hypothesis sentence, and the locked T27 files are in the state the PR describes. The fold into `CORE.md` §8 and `THEORY.md` §4 is not. Two sentences a reader would take as the result are stronger than the note, or they use symbols this file already defines as something else.

## Cuts in `theory/SELECTION_AXIOMS.md`

`wc -w`: 4,988 on `2eeab30`, 4,671 on this head. The difference is 317 words. Nothing substantive was lost. Each cut is one of the eight named in `reviews/selection_axioms_2026-11-21/CONFIRM.md` §3, or the stale "the bridge still writes \(\beta=\alpha(N_e-1)\)" sentence that this PR had to replace. Where the substance had to remain, it is still in the note.

| Cut | Still in the note |
|---|---|
| §0's last sentence ("If a reviewer reads only the formulas") | The packaging sentence immediately before it is still there (`theory/SELECTION_AXIOMS.md:9`). |
| §3 "The bridge writes the fractional form with \(\beta=\alpha(N_e-1)\)" | Corollary SA1c still separates absolute \(d/(2\beta)\) from fractional \((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\), and still says \(\alpha(N_e-1)\) is the Moran exponent only when \(N_e\) is census size (`:81`). |
| Two repeated sentences in "Closeness under the formula," plus "Formal Axiom 7's tolerance \(\varepsilon\) has a scale" | \(\sigma N_e\gg d\) and "THEORY §3's operational meaning of strongly selected is unchanged" are in §0 (`:7`). The theorem-is-the-formula sentence and the same \(\sigma N_e\gg d\) sentence are in §10 (`:184`). Axiom 7 is still in §2 (`:33`): it assumes near-minimization and is not a premise; the point is to derive a scale for \(\varepsilon\). The \(d/20\) ratio and the Lynch credit stayed. |
| §5 Lande and Bürger page-and-DOI parentheticals | Author and year stayed (`:143`). The reference list still has both DOIs and both JSTOR DOIs (`:198`, `:204`). The "DOIs verified, formulas not re-derived" limit stayed. Dixit and Chalkley in §4 were not cut (`:109`). |
| §7's three "see §5 / see §6" bullets | Lande, Bürger & Lynch, and Mustonen & Lässig, with "this note uses none of their constants," are in §5 (`:143`). Price 1970, including "does not give the distance to the minimum," is in §6 (`:151`). Orr 1998 and Fisher 1930, including "neither result is the stationary excess \(d/(2\beta)\)," are in §6 (`:153`). |
| §8 repeats: monotone and linear birth, the strong-mutation list, finite time, T27, the empirical bet | A2-M and the linear birth rate are in §0 (`:7`) and §2 (`:27`–`:29`). Frequency dependence, strong mutation, and a binding ruin constraint are in §2 (`:33`). A2-P is still excluded (`:29`). Standing polymorphism is in §7 (`:162`). Finite time and valley-blocked graphs are Proposition SA4 (`:147`–`:150`). T27's P3 is in the header (`:3`) and §11 (`:188`). The empirical bet is in §0 (`:9`) and §10 (`:184`). |
| §8's "this note does not edit THEORY" | Replaced, and the replacement is required: this PR does edit THEORY. The new clause (`:174`) says the hypothesis sentence and the locked factor of 10 are unchanged, and that the in-model derivation is now also stated in THEORY §4. The three bullets CONFIRM said to keep are still there: not a physical law and not a theory of everything (`:171`), not kelvin (`:172`), ruin cap not inside \(\pi\) (`:173`). |
| §12 compressed to the two filenames and **NUMERICAL** | The moment-versus-density limit is in §4 (`:128`). |

The six SA2 conditions are in both SA2-C and Theorem SA2 (`:109` and `:111`): discount rate zero; between redesigns the lumpy coordinate is not a site of the origination–fixation chain; the optimum moves only in that coordinate; a reset changes that coordinate only; the pair \(N\mu\ll 1\) and \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\); \(d=\dim y\). §0's sentence that THEORY §3's meaning of strongly selected is unchanged is at `:7`. §10's sentence that the theorem is the formula is at `:184`.

Sella & Hirsh are still credited for the stationary weight only. §7 (`:159`) is the required sentence: equations 11–13 are the fixed-drift load for fitness uniform on \((0,1)\), mean fitness \((\nu+1)/(\nu+2)\), load about \(1/\nu\); \(d/(2\beta)\) is equipartition under that weight. The SA1 proof still says it does not use Iwasa (`:60`).

## Blockers

1. `CORE.md:100`, the §8 paragraph. Two false readings in the new text.

   "Near-minimization is derived in-model under those assumptions" takes its antecedent from the previous sentence. That sentence's assumptions are the extra ones for the drifting-world sum: additive costs, zero discount, the lumpy coordinate outside the substitution chain, timescale separation. The stationary excess is derived under A1, A2-L, \(N\mu\ll 1\), and SA1–SA1b. The list in the previous sentence is what lets the CL19 lag be added. "The empirical bet is whether real systems meet them" inherits the same antecedent, so the bet is attached to the lag's extra assumptions.

   The gloss on \(\nu\) is the other defect in the same paragraph: "with \(N_e\) equal to Sella and Hirsh's \(\nu\) (haploid Moran \(\alpha(N-1)\); diploid Wright–Fisher \(\alpha(2N-1)\))". The parenthetical is attached to \(\nu\), and it writes \(\beta\). For the haploid Moran process \(\nu=N-1\) and \(\beta=\alpha(N-1)\). For diploid Wright–Fisher with multiplicative fitness, \(\nu=2N-1\) and \(\beta=\alpha(2N-1)\), and that factor is an approximation (`core/bridge_2026-11-21/SELECTION.md:29`; `theory/SELECTION_AXIOMS.md:51`). CORE states \(\alpha(2N-1)\) with no approximation.

   Suggested fix: use the note's gloss, and point "derived" at the excess, not at the lag's extra assumptions. `with \(N_e\) equal to Sella and Hirsh's \(\nu\) (haploid Moran \(\beta=\alpha(N-1)\); diploid Wright–Fisher \(\beta=\alpha(2N-1)\), an approximation)`. Then: `The excess \(d/(2\beta)\) is derived in-model under A1, A2-L, \(N\mu\ll 1\), and SA1–SA1b, and that excess is small only when \(\sigma N_e\gg d\) (THEORY §4; `theory/SELECTION_AXIOMS.md` §10). The empirical bet is whether real systems meet those assumptions with parameters that make the remainder small, tested by SA-P1, which is not locked.` Leave the drifting-world sentence as the sentence about the lag.

2. `THEORY.md:71`. "Near-minimization is derived in-model under A1, A2-L (a log-linear copying map), weak mutation \(N\mu\ll 1\), and SA1–SA1b" is stronger than the note this sentence cites. `theory/SELECTION_AXIOMS.md:184`, which this PR left in place, says the theorem is the formula for the excess, and that the formula plus \(\sigma N_e\gg d\) is what puts a qualifying class near the minimum. The same assumptions cover the bridge's low-\(\beta\) regime, where the mass spreads and the mean stays above \(J^\star\) (`core/bridge_2026-11-21/SELECTION.md:49`). Deriving \(d/(2\beta)\) is not deriving that the excess is small.

   The empirical clause in the same sentence, and again at `THEORY.md:209`, says the bet is "whether real systems meet those assumptions, tested by SA-P1". §10 of the note says the remaining claim is that real systems in a qualifying class satisfy those assumptions with parameters that make the remainder small. SA-P1 (`theory/SELECTION_AXIOMS.md:178`) compares a lag-corrected fractional excess with \(d/(2\sigma N_e)\). It is a test of that excess. Appendix A.1 states the distance \(d/(2\beta)\), which is the right object, and then uses the shortened empirical sentence.

   The same two sentences also reuse symbols Appendix A.2 already assigned. The header at `THEORY.md:214` says one symbol, one meaning, throughout this file, and that the table governs. \(d\) at `:229` is the price of telling one member. \(\nu\) at `:231` is the failure hazard. \(N\) at `:236` is the number of members. \(\beta\) is not in the table. Appendix B's A1 at `:257` is "the world is exogenous," and the selection note's A1 is "persistence has a cost." A reader who applies the table reads \(d/(2\beta)\) as a telling price and reads \(N_e\) as equal to a hazard. The \(\sigma\) in \(d/(2\sigma N_e)\) is §3's cost-to-fitness elasticity, which is the right \(\sigma\) for that formula; the table's shock-scale \(\sigma\) at `:239` is already §3's collision, and these sentences do not gloss it.

   What this paragraph does not do: it does not say real systems have been shown to sit near the minimum ("Whether real systems obey it is untested, not refuted"). It does not call the hypothesis a law ("until then what is established is a principle, not a law"). It does not treat SA-P1 as locked ("which is not locked").

   Suggested fix: replace the new clauses in §4 and the Selection bullet in A.1 with the note's §10, in words that do not reuse this file's \(d\), \(\nu\), or \(N\). `Under the selection note's A1 (persistence is costly) and A2-L, which are not Appendix B's A1–A5, the derived in-model result is that note's excess formula. The excess is small only when the note's \(\sigma N_e\) is large compared with the number of soft coordinates. The empirical bet is the note's §10: qualifying systems meet those assumptions with parameters that make the remainder small. SA-P1 tests that excess. It is not locked.` Keep "a principle, not a law."

## Should-fixes

1. `THEORY.md:184`. "That selection holds designs near the optimum is assumed (Alchian 1950)" is still the canonical file's present tense, in the same file that §4 and A.1 now treat as an in-model derivation. Suggested fix: credit Alchian 1950 as the prior-art assumption, and point the status at §4: the in-model excess is the selection note's formula; the field claim is untested.

2. `reviews/selection_axioms_2026-11-21/CONFIRM.md:117`. The dated note's `\beta` and `\alpha` are not in the file. Six bytes are `\x08` and `\x07`, three times: `\b` and `\a` were taken as backspace and bell. The sentence does not render the formulas it claims to record. Suggested fix: rewrite that paragraph with the literal two-character sequences used everywhere else in the file. In the same paragraph, say that THEORY §4 and Appendix A.1 were edited in this pass. As the file stands, `:59` ("This note does not edit that section") is the last intact sentence about THEORY.

## Nits

1. `measurement/CLAIM_MAP_v2.md:603`, R1's Why cell: "diploid WF \(\alpha(2N-1)\)" has no "an approximation". The claim cell of the same row has "Sella–Hirsh approximation". The v2.71 note at `:86` has it. The Why cell is the current pointer.

2. `measurement/CLAIM_MAP_v2.md:88`, the v2.70 note, still says the bridge "still writes \(\beta=\alpha(N_e-1)\)" in the present tense. The note is dated, and the v2.71 note corrects the bridge. A reader who stops on the v2.70 paragraph gets the pre-fold claim.

3. `theory/SELECTION_AXIOMS.md:188`. "the same per-model exponents (haploid Moran \(\alpha(N-1)\); diploid Wright–Fisher \(\alpha(2N-1)\), an approximation)" omits \(\beta=\). The approximation is there. §0 (`:9`) writes \(\beta=\alpha(N-1)\) and \(\beta=\alpha(2N-1)\) and is the accurate sentence.

## What was checked and holds

- Bridge (`core/bridge_2026-11-21/SELECTION.md`). The general factor \(\beta=\alpha(N_e-1)\) is withdrawn at `:3`. Haploid Moran is \(\beta=\alpha(N-1)\) (`:27`). Diploid Wright–Fisher with multiplicative fitness is Sella and Hirsh's approximation \(\beta=\alpha(2N-1)\), their weight \(f^{2N-1}\) (`:29`). Haploid Wright–Fisher \(2(N-1)\) is named and unused. The weak-mutation regime is \(N\mu\ll 1\) (`:19`). Absolute excess \(\mathbb{E}[J]-J^\star=d/(2\beta)\) and fractional excess \((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\) are separate (`:43`–`:45`). With \(N_e=\nu\), \(\beta=\alpha N_e=\sigma N_e/J^\star\) when \(\sigma\) is evaluated at \(J^\star>0\), and the ratio of that fractional excess to the band \(\varepsilon=10/(\sigma N_e)\) is \(d/20\). \(\alpha(N_e-1)\) is restricted to the haploid Moran exponent when \(N_e\) is census size (`:47`). The official T27 line is still \(N=201\), \(\beta=\alpha(N-1)\).
- No current formula outside a dated note, a withdrawn-factor sentence, or the census-size qualifier still offers \(\beta=\alpha(N_e-1)\) as the general factor. `history/2026-11-21_CORE_before_onepage.md` still has the old "population size times the fitness scale" sentence; that file is the pre-one-page snapshot.
- The Part 2 hypothesis sentence is byte-identical to `2eeab30`, one copy each, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`
- Locked prereg and hash files are unchanged against `origin/main` `2eeab30`. `git diff --stat origin/main...HEAD` is the 11 files in the PR, 34 insertions and 34 deletions. A path filter for `PREREG`, `LOCK`, `hash`, `SHA`, `predictions.json`, and `RESULTS.md` is empty. `core/bridge_2026-11-21/PREREG.md` is 10047 bytes, SHA-256 `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994`. `predictions.json` is 2246 bytes, SHA-256 `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3`. Both match `LOCK.txt`. Local `refs/heads/main` on this machine was `c04cedd` until `git fetch origin main`; the comparison above is against fetched `origin/main` `2eeab30`.
- CLAIM_MAP: version pointers in README, STATUS, THEORY, and `tools/test_brief.py` say v2.71. The diff of the map changes the v2.71 note, the R1 Why cell, the section-R heading, and the tally heading. No status cell changes. The tally block is still 330. R1 remains PRIOR ART, R2 PROVED (in-model), R3 OPEN.
- T27's P3 is still a failed official test in the header, §11, CORE §8, and the v2.71 note.

## Commands

All of these were run from the repo root, on head `710565a`, with `nice -n 19`.

- `git fetch origin main`. `origin/main` moved `c04cedd..2eeab30`. First-parent window: `2eeab30 c04cedd d34df95 a97887e 0726423`.
- `git diff --stat origin/main...HEAD`. 11 files, 34 insertions, 34 deletions. Lock/prereg/hash filter empty.
- `wc -w` on `theory/SELECTION_AXIOMS.md`: 4988 at `2eeab30`, 4671 at HEAD.
- SHA-256 of `PREREG.md` and `predictions.json` as above; both match `LOCK.txt`.
- `python3 tools/check_fresh.py`. `STATUS.md main is 2eeab30; window: 2eeab30 c04cedd d34df95 a97887e 0726423`. `RESULT: PASS`. Exit 0.
- `python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.71; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 330; process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10533 words, README 1468), not failures. `RESULT: PASS`. Exit 0.
- `python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `python3 -m pytest -q tools`. `175 passed, 1 skipped in 251.96s`. Exit 0. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed`. The other test in that file passed. This environment did not have pytest, SciPy, or SymPy at the start; those were installed for the run. NumPy after that install is 2.5.5. The PR text's "176 passed" is this suite with the lake test also running. It is not a failure of the diff.
