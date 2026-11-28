# Confirm: antifragility as a tested question, 22 November 2026

CONFIRM: READY

Independent read of draft PR #191 at head `7047721e0b3394778d43e88bf954d01eaeee254f` on `antifragility-turnover-2026-11-22`. That branch was not edited. Nothing was merged. This file is the only change against `main` `13eec9af0b3385f9a433d0c1f62d341c8a520e2d`. The repairs answer `reviews/antifragility_2026-11-22/HOSTILE_REVIEW.md` on `review-antifragility-2026-11-22` (PR #193), which read the earlier head `acff0820f17b83f04c336769524a0c5142f55a66`.

The numbers below were recomputed in a separate script. It does not import `theory/antifragility_checks`. The stationary law is the R-select balance from `PREREG.md` §1, in exact fractions. The mean-field cost is the formula in that section and in `PREREG_CAP.md`. The Monte Carlo is a new implementation of the locked estimator: NumPy Generator, PCG64, \(M = 50000\), the type uniform drawn first and the \(M \times 4\) alignment matrix second, \(\alpha = U^{\delta/\lambda}\), ruin when the error exceeds \(3/2\). NumPy 1.26.4 for that script.

## Protected files

`git diff origin/main 7047721 -- THEORY.md CORE.md README.md` is empty. The three files are byte-identical to `main` (165741, 18262, and 9061 bytes). SHA-256:

| file | SHA-256 |
|---|---|
| `THEORY.md` | `91a527e499f2cd074cf4761302b4d4ab113fbbcd29861345f582905bb9e3e1e4` |
| `CORE.md` | `31e227038ea2ec64679eb126b9f02681e9c22e4502a73fb73b814b8899069178` |
| `README.md` | `042de9a4a295327915c05c32eaebd1e711e902cd2914d1c4f5450ac47f226a1a` |

The hypothesis sentence is present once in each file, with the same bytes, including the bold markers:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`7047721` is a linear descendant of `13eec9a`. The note does not edit those three files.

## The four required fixes

**B1. Rebase and T43.** Done on the branch. `4041018` has parent `13eec9af0b3385f9a433d0c1f62d341c8a520e2d`, which is `origin/main`. The history from there to `7047721` is linear, seven commits. `git diff origin/main 7047721 -- OPEN_WORK.md` adds one row. Main's T41 and T42 are unchanged. The new row is T43, and it leads with the admissible identical-unit point.

GitHub still records the base of PR #191 as `holographic-memory-2026-11-22` at `819b240`. There is no `base_ref_changed` event. The page therefore counts thirteen commits and twenty-two files, because that older tip is an ancestor of `main`. Against `main` the branch adds the seven commits and fourteen files. A merge of this head into `main` is a fast-forward of those seven commits. The pull request's base ref is the older branch. This confirm does not retarget it.

**B2. Admissible comparison first.** Done in §0, in §4, and in the body of PR #191. The opening design claim is identical units at rate \(1\), cost \(15.473978\), ruin probability \(0.020940\), a margin of \(0.526022\) under the inadmissible zero at cost \(16\). The same paragraph gives the informative admissible cost \(15.566427\) and the uninformative admissible cost \(22.311716\), both above their zero-shock cost \(13\), and the quality-observed admissible cost \(15.471038\) against its own zero at \(13\). The unconstrained minimum, rate \(0.2646371727\), cost \(13.3545082433\), is named as the minimum of the cost P1–P7 score, and the official grid point of that bowl, rate \(0.3\), cost \(13.748899\), is given ruin probability \(0.473560\) in that paragraph. The sentence that the numbered predictions were scored on the unconstrained cost is present, and it says the preregistration required that scoring. P1 stays **FAILS** at the frozen cap.

**B3. Title.** Done, and the wording is the one this confirm was asked to treat as final. GitHub's rename event at 20:47:25 UTC changed the title from `Antifragility as turnover: heat, convexity, and a positive shock` to `Antifragility test: turnover, heat, and positive stress (passive memory)`. Antifragility remains the question under test. The title also names turnover, the heat, and a positive level of stress. The note's own heading is `Turnover, heat, and a positive level of stress`. Section 5 says the cost is convex on the half-line and is not antifragility in the sense of `theory/ROBUSTNESS.md` §6.

**B4. Blank design.** Done. The sentence that a design will switch the memory off before it buys this cap is absent from the branch. Section 6 now says that under the cap the blank design has error \(4\) and ruin probability \(1\), that the precision A14 would install, at most \(0.093750\), pools to \(0.375\) at full alignment, short of \(5/12\), that the unconstrained comparison of the identical-unit minimum with the blind cost \(6\) is a comparison of two designs the cap rejects, and that the turnover result is conditional on the cap being installed.

## Registration

The prediction files stay frozen, and the cap registration precedes the cap computation.

| commit | parent | author time (UTC) | what it adds |
|---|---|---|---|
| `4041018` | `13eec9a` | 2026-11-22 20:03:58 | `PREREG.md` only |
| `271842a` | `4041018` | 2026-11-22 20:08:28 | `ADDENDUM.md` only |
| `1e65378` | `271842a` | 2026-11-22 20:24:39 | the first computation |
| `f8cd781` | `1e65378` | 2026-11-22 20:41:42 | `RESULTS.md` prose only |
| `44c5f99` | `f8cd781` | 2026-11-22 20:42:13 | `PREREG_CAP.md` only |
| `32e92e5` | `44c5f99` | 2026-11-22 20:42:19 | `LOCK_CAP.txt` only |
| `7047721` | `32e92e5` | 2026-11-22 20:44:07 | the cap computation |

Author time equals committer time on the cap commits. On the first three, the committer time is the rebase at 20:40:11–20:40:22 and the author time is the original time the hostile review recorded. Each parent is the commit above it.

The blob of `PREREG.md` is `abc87b00c7a91a113fb0c989d812b5a7c15d1716` from `4041018` through `7047721`. The blob of `ADDENDUM.md` is `270304f49a279b4dec1c53f37f39f512a7097a36` from `271842a` through `7047721`. Those are the blobs the hostile review hashed. `f8cd781` changes `RESULTS.md` only. That is the admissible-lead revision the review required. It is not a prediction file.

`PREREG_CAP.md` is blob `8a6d8900d7c66ac137e1c06b593f8bb17fd8b5d4` from `44c5f99` through the head. SHA-256 `e4adc02987a0afe27cdfe80e8b8545cc6eba14e1858b8af1e655df41e49c49ef`, 6018 bytes, which is the hash and the length in `LOCK_CAP.txt`. The lock blob `1bf531d24c5953502c5f5faa7906d7057f768d03` is unchanged at the head. The tree of `32e92e5` contains neither `cap_checks.py` nor `cap_results.out`. `7047721` adds those, `CAP_RESULTS.md`, the test, and the T43 sentence about the cap grid. It does not change `PREREG.md`, `ADDENDUM.md`, `PREREG_CAP.md`, `LOCK_CAP.txt`, `RESULTS.md`, `results.out`, or `turnover_checks.py`.

## Recomputation

The locked mean-field cost at precision \(1/2\) and rate \(1\) is \(15.3972245773\). The R-select balance holds in exact fractions, and \(\mathbb{E}[k] = 3.7899088603\). On identical units the locked-coupling formula and the fixed-heat formula agree at every grid point. The maximum gap is \(0\).

**Identical units, the recorded admissible point.** Seed \(20261123\), the A1 stream, precision \(1/2\), rate \(1\). Official cost \(15.4739783996\), which is the printed \(15.473978\). Ruin probability \(0.020940\), which is \(1047/50000\). The zero-shock cost is \(16\) and its ruin probability is \(1\). The margin is \(0.5260216004\), which prints as \(0.526022\).

**Cap grid, seed \(20261130\).** The admissible official argmin is precision \(3/10\), rate \(1.5\), mean-field cost \(13.7117638337\), official cost \(13.7551074206\), ruin probability \(0.030240\) (\(1512/50000\)). Precision \(1/4\) at rate \(2\) has mean-field cost \(14.4089523586\), official cost \(14.4368692815\), ruin probability \(0.022500\) (\(1125/50000\)). It is admissible, and it is not the cheapest. The same-stream reference at precision \(1/2\) and rate \(1\) is official cost \(15.4708445545\), ruin probability \(0.019200\). That stream is a different seed from the recorded \(15.473978\). Four admissible pairs sit strictly below the recorded reference on both accountings: \((3/10,\ 1.5)\), \((3/8,\ 1.5)\), \((1/4,\ 2)\), and \((3/10,\ 2)\). The unconstrained official minimum is precision \(1/10\), rate \(0.4\), cost \(8.8865107737\), ruin probability \(1\).

**Locked coupling, seed \(20261131\).** The admissible official argmin and the admissible mean-field argmin are the same point: precision \(3/8\), rate \(1.5\), official cost \(15.4328226573\), mean-field cost \(15.3813092872\), ruin probability \(0.018480\) (\(924/50000\)). That official cost is \(0.041155\) below \(15.473978\) and \(3.682823\) above the inadmissible zero at the same precision. The zero has ruin probability \(1\). The unconstrained minimum is precision \(1/10\), rate \(0.3\), cost \(8.9464626764\), ruin probability \(1\).

**Fixed heat, seed \(20261132\).** The admissible argmin on both accountings is precision \(1/4\), rate \(2\), official cost \(15.5593525440\), mean-field cost \(15.5188578966\), ruin probability \(0.049900\) (\(2495/50000\)). That official cost is \(0.085375\) above \(15.473978\) and \(3.559353\) above its own inadmissible zero. The unconstrained minimum is precision \(1/10\), rate \(0.3\), cost \(9.0462798753\), ruin probability \(1\).

These are the printed digits in `RESULTS.md`, `CAP_RESULTS.md`, and the body of PR #191. The five points this confirm was asked to recompute agree at the printed place: rate \(1\), cost \(15.473978\), ruin probability \(0.020940\); precision \(3/10\) at rate \(1.5\), cost \(13.7551\), ruin probability \(0.030240\); precision \(1/4\) at rate \(2\), cost \(14.4369\), ruin probability \(0.0225\); locked-coupling precision \(3/8\) at rate \(1.5\), cost \(15.4328\); fixed-heat cost \(15.5594\), ruin probability \(0.0499\).

## Wording

The diff of `7047721` against `origin/main` has no added line containing `bill` or `kill`. The objective is called a cost. The substring `verdict` occurs once in the added lines, in `PREREG.md` §7, in the sentence that a puzzle is not promoted to a verdict on the hypothesis sentence. Consistency reports 0 wording failures.

## Checks at `7047721`

| Command | Result |
|---|---|
| `nice -n 19 python3 tools/check_open_work.py` | PASS. 0 missing |
| `nice -n 19 python3 tools/check_consistency.py` | PASS. 0 FAIL. 392 claim-map rows. Length warnings on THEORY (11134 words) and README (1476 words) are the pre-existing advisory |
| `nice -n 19 python3 -m pytest -q tools` | 258 passed, 1 skipped, 321.99 s |

The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed". No lake build. The two new tests, `tools/test_cap_checks.py` and `tools/test_antifragility_turnover_checks.py`, are in the 258. The tools run used pytest 9.2.0, SciPy 1.18.1, SymPy 1.14.0, and NumPy 2.5.5, because `np.trapezoid` is absent from NumPy 1.26.4 and that name is what the existing tools call. The recomputation above used NumPy 1.26.4, and the digits match the note.

## List

1. The rebase onto `13eec9a` is in the history, and the OPEN_WORK row is T43. The GitHub base ref of PR #191 is still `holographic-memory-2026-11-22`.
2. The admissible comparison leads in the note and in the PR body, with the ruin probability of the unconstrained grid minimum in the same paragraph.
3. The title is `Antifragility test: turnover, heat, and positive stress (passive memory)`. Antifragility is the tested question.
4. The blank-design sentence is replaced.
5. `44c5f99` and `32e92e5` are parents of `7047721`, in that order. No earlier prediction file changes in the cap computation.
6. The five recomputed points match the printed digits.
7. `THEORY.md`, `CORE.md`, and `README.md` are byte-identical to `main`.
8. The added lines say cost. They do not say bill or kill.
9. Open-work PASS, consistency PASS, pytest 258 passed and 1 skipped.

CONFIRM: READY
