# Blind confirm: PR #144 (selection fold)

**Confirmer:** independent. Wrote none of the fold and none of `REVIEW.md`. The findings below were written from `git diff 2eeab30..HEAD` and from the files themselves. `reviews/selection_fold_2026-11-21/REVIEW.md` was read only after that verdict.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/144
**Head confirmed:** `df84b830ea05a67eec362ab27a2edb93d85e76a5` on `selection-fold-2026-11-21`. Base `2eeab306ce1e50a3d8a8e658906b7e2401310998`. Draft. Not merged.

**Verdict: READY**

No blockers. No should-fixes.

The stationary absolute excess is stated as an in-model result, \(\mathbb{E}[J]-J^\star=d/(2\beta)\), under A1 (persistence costly), A2-L (log-linear copying map), weak mutation \(N\mu\ll 1\), and SA1–SA1b. \(\beta=\alpha(N-1)\) for haploid Moran and \(\beta=\alpha(2N-1)\) for diploid Wright–Fisher, and the diploid factor is an approximation. The excess is small only when \(\sigma N_e\gg d\). Whether real systems meet those assumptions with parameters that make the remainder small is the empirical bet, tested by SA-P1, which is not locked. Sella and Hirsh are credited for the stationary weight. \(d/(2\beta)\) is equipartition under that weight. The framing in THEORY §4 is a principle, not a law.

## Checks

1. **No file claims real systems are proven near-minimal, and none calls the hypothesis a law.** THEORY §4 (`THEORY.md:71`) says real systems are untested, not refuted, and that what is established is a principle, not a law. Appendix A.1 (`:209`) points the empirical bet at the note's §10 and says SA-P1 is not locked. CORE §8 (`CORE.md:100`) states the same bet and says SA-P1 is not locked. `theory/SELECTION_AXIOMS.md:171` says the note does not make the hypothesis a physical law. `:184` says the formula plus \(\sigma N_e\gg d\) is what puts a qualifying class near the minimum, and that this is not yet a field result. STATUS still calls the principle untested, not refuted. The word "law" in the Part 2 sentence is the hypothesis label required by check 5. `tools/check_consistency.py` reported 0 wording FAILs on 29 maintained docs.

2. **No flat "near-minimization is derived" without \(\sigma N_e\gg d\), in the five named files.**
   - `CORE.md:100`. The lag stays in its own sentence (additive costs, zero discount, the lumpy coordinate outside the substitution chain, timescale separation). The next sentence is the excess: derived under A1, A2-L, \(N\mu\ll 1\), and SA1–SA1b, and small only when \(\sigma N_e\gg d\). The empirical sentence names those assumptions and the parameters that make the remainder small.
   - `THEORY.md:71` and `:209`. The derived in-model result is the selection note's excess formula, under the note's A1 and A2-L (explicitly not Appendix B's A1–A5), weak mutation, and SA1–SA1b. The excess is small only when the note's \(\sigma N_e\) is large compared with the number of soft coordinates. The empirical bet is the note's §10. SA-P1 tests that excess and is not locked.
   - `theory/SELECTION_AXIOMS.md:7` states the distance \(d/(2\beta)\) and that \(\sigma N_e\gg d\) makes the fractional remainder small. `:184` separates the formula from nearness.
   - `core/bridge_2026-11-21/SELECTION.md:40` states \(\mathbb{E}[J]-J^\star=d/(2\beta)\). `:47` says that for large \(d\) the scatter need not sit inside the band. It does not say real systems have been shown to sit at the minimum.
   - `measurement/CLAIM_MAP_v2.md:86` states the excess formula under A1, A2-L, weak mutation, and SA1–SA1b, and that the excess is small only when \(\sigma N_e\) is large compared with the number of soft coordinates. SA-P1 is not locked. No status cell changes. R3 stays OPEN.

3. **\(\beta\) factors agree, and the diploid factor is an approximation.** Haploid Moran is \(\beta=\alpha(N-1)\) (`core/bridge_2026-11-21/SELECTION.md:27`, `theory/SELECTION_AXIOMS.md:48`, `CORE.md:100`). Diploid Wright–Fisher with multiplicative fitness is Sella and Hirsh's approximation \(\beta=\alpha(2N-1)\) (`SELECTION.md:29`, `SELECTION_AXIOMS.md:51`, CORE, CLAIM_MAP R1's claim cell and Why cell). Haploid Wright–Fisher \(2(N-1)\) is named and unused. With \(N_e\) equal to \(\nu\), \(\beta=\alpha N_e\). \(\alpha(N_e-1)\) is only the Moran exponent when \(N_e\) is census size (`SELECTION.md:47`, `SELECTION_AXIOMS.md:81`). The general factor \(\beta=\alpha(N_e-1)\) is withdrawn at `SELECTION.md:3`. The v2.70 note's old present-tense claim is qualified in the same sentence: later corrected in the v2.71 note (`CLAIM_MAP_v2.md:88`).

4. **No symbol clash with Appendix A.2's \(d\), \(\nu\), and \(N\).** A.2 (`THEORY.md:213`–`:236`) assigns \(d\) to the price of telling one member, \(\nu\) to the failure hazard, and \(N\) to the number of members, and says one symbol, one meaning, throughout the file. The new sentences at `:71` and `:209` do not use \(d\), \(\nu\), or \(N\). They say "that note's excess formula" and "the number of soft coordinates," and they attribute \(\sigma N_e\) to the note. The selection note's A1 is distinguished from Appendix B's A1–A5.

5. **The Part 2 sentence is byte-identical to `2eeab30`.** One copy each, same bytes, including the bold markers: `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`. The sentence is `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

6. **`git diff 2eeab30 --stat` does not touch a locked prereg, a hash file, or a T27 result.** The twelve paths are `CORE.md`, `OPEN_WORK.md`, `README.md`, `STATUS.md`, `THEORY.md`, `core/bridge_2026-11-21/SELECTION.md`, `measurement/CLAIM_MAP_v2.md`, `reference/CHANGELOG.md`, `reviews/selection_axioms_2026-11-21/CONFIRM.md`, `reviews/selection_fold_2026-11-21/REVIEW.md`, `theory/SELECTION_AXIOMS.md`, and `tools/test_brief.py`. A name filter for `PREREG`, `sha256`, `hash`, `LOCK`, `T27`, and `RESULTS` on that diff is empty. The bridge text says the official Moran run, \(N=201\) and \(\beta=\alpha(N-1)\), was not changed, and that P3 failed and is not rescued.

7. **Commands.** All from the repo root, with `nice -n 19`, on `df84b83`. Results below.

## REVIEW.md blockers

`REVIEW.md` reviewed `710565a`, verdict NOT READY. This confirm is of `df84b83` (`Apply selection-fold review: two blockers and should-fixes`).

1. **Fixed.** `CORE.md:100`. The excess, not the lag's extra assumptions, is what the paragraph says is derived, and the premises are A1, A2-L, \(N\mu\ll 1\), and SA1–SA1b, with the excess small only when \(\sigma N_e\gg d\). The parenthetical on \(\nu\) now writes \(\beta=\alpha(N-1)\) and \(\beta=\alpha(2N-1)\), an approximation. The empirical bet includes the parameters that make the remainder small, and SA-P1 is not locked. This is the review's suggested sentence.

2. **Fixed.** `THEORY.md:71` and the Selection bullet at `:209`. Neither says near-minimization is derived under those assumptions. Both say the derived result is the note's excess formula, that the excess is small only when the note's \(\sigma N_e\) is large compared with the number of soft coordinates, and that the empirical bet is the note's §10 (assumptions plus parameters that make the remainder small). SA-P1 tests that excess and is not locked. Neither sentence reuses Appendix A.2's \(d\), \(\nu\), or \(N\). "A principle, not a law" remains at `:71`. The added clause "together with weak mutation and SA1–SA1b" names the premises the note actually uses; it does not import \(N\).

The review's two should-fixes are also fixed. `THEORY.md:184` credits Alchian (1950) as the prior-art assumption and points the in-model excess at §4; the field claim is untested. `reviews/selection_axioms_2026-11-21/CONFIRM.md:117` renders \(\beta\) and \(\alpha\) as the file's usual two-character escapes (0 bell bytes, 0 backspace bytes in that file) and says THEORY §4 and Appendix A.1 were edited in that pass.

The review's three nits are fixed. R1's Why cell (`CLAIM_MAP_v2.md:603`) says the diploid factor is an approximation. The v2.70 note (`:88`) says the bridge's \(\beta=\alpha(N_e-1)\) was later corrected in the v2.71 note. `theory/SELECTION_AXIOMS.md:188` writes \(\beta=\alpha(N-1)\) and \(\beta=\alpha(2N-1)\), an approximation.

## Blockers

None.

## Should-fixes

None.

## Commands and results

- `git diff 2eeab30 --stat`

```
 CORE.md                                        |  2 +-
 OPEN_WORK.md                                   |  2 +-
 README.md                                      |  2 +-
 STATUS.md                                      |  4 +-
 THEORY.md                                      |  8 +--
 core/bridge_2026-11-21/SELECTION.md            | 10 +--
 measurement/CLAIM_MAP_v2.md                    | 10 +--
 reference/CHANGELOG.md                         |  2 +
 reviews/selection_axioms_2026-11-21/CONFIRM.md |  8 +++
 reviews/selection_fold_2026-11-21/REVIEW.md    | 85 ++++++++++++++++++++++++++
 theory/SELECTION_AXIOMS.md                     | 26 +++-----
 tools/test_brief.py                            |  2 +-
 12 files changed, 125 insertions(+), 36 deletions(-)
```

  Path filter for `PREREG`, `sha256`, `hash`, `LOCK`, `T27`, and `RESULTS`: no matches.

- Hypothesis sentence: `git show 2eeab30:<file>` against the working tree. One line each in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`. Line bytes equal the base in all four.

- `nice -n 19 python3 tools/check_fresh.py`. `STATUS.md main is 2eeab30; window: 2eeab30 c04cedd d34df95 a97887e 0726423`. `RESULT: PASS`. Exit 0.

- `nice -n 19 python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.71; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 330 (tally total 330); process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10569 words, README 1468), not failures. `RESULT: PASS`. Exit 0.

- `nice -n 19 python3 tools/check_open_work.py`. `items.json not-DONE: 62; QUEUE.md not-DONE: 90; union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.

- `nice -n 19 pytest -q tools`. The first invocation exited 127 (`pytest` was not on `PATH`). After `python3 -m pip install --user pytest numpy scipy sympy`, the same command reported `175 passed, 1 skipped in 252.64s`. Exit 0. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed` (confirmed with `pytest -q tools/test_lean.py -rs`).
