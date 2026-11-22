# Independent confirmation of draft PR #194

**Verdict: CONFIRM**

Head `c55cd8782de62c2cbe2075d4064ea8828e236392` on `boundary-sufficiency-2026-11-22`. This note was written from the repository only. The arithmetic below is from `reviews/boundary_sufficiency_2026-11-22/recompute.py`, which does not import `theory/boundary_checks/boundary_checks.py`. It was run as `nice -n 19 python3 reviews/boundary_sufficiency_2026-11-22/recompute.py` (Python 3.12.3, NumPy 2.5.5, SciPy 1.18.1). An earlier run on NumPy 1.26.4, before SciPy was installed, produced the same twelve crossing digits.

Discrepancies: none. Every load-bearing figure matches the note at the precision the note prints.

## Load-bearing numbers

| Quantity | Note / preregistration | Recomputed |
|---|---|---|
| Exterior law given the blanket, and given the region and the blanket | both \(1/2\) | both \(1/2\). The conditional mean of \(X_2\) puts weight \(0\) on \(X_0\) and weight \(1/2\) on \(X_1\) |
| Exterior variance given the region alone | \(3/5\) | \(3/5\) |
| Cross-term channel trace, interior diagonal \(0.1\), cross entry \(1\), blanket diagonal \(10\) | \(10.1\) | \(101/10\) |
| Matching blanket-channel trace | \(10.5\) | \(21/2\) |
| Excess against the Schur cap | \(2/5 \le 1/2\) | \(2/5 \le 1/2\). The same \(2/5\) is \(\operatorname{tr}(K(0))-\operatorname{tr}(K(\Phi))-\operatorname{tr}(\Phi_{II})\) |
| Exterior variance of either channel | \(13/25\) | \(13/25\), and the blanket posterior variance is \(2/25\) |
| Gasket Schur traces, generations \(2\) through \(5\) | \(1.234848484848\), \(1.290266004092\), \(1.290954813099\), \(1.290954956476\) | \(1.234848484848485\), \(1.290266004092370\), \(1.290954813099131\), \(1.290954956476226\). Each rounds to the printed twelve decimals. Generation \(5\) rounds to \(1.290955\) |
| Interior variance floor against the tolerance | \(1/5 > 1/18\) | \(1/5 - 1/18 = 13/90 > 0\). Path of three: \(1/2\). Path of five: \(1/3\) |
| Conditional information, long-range \(\gamma=1\), equicorrelated covariance, and MA(1) | \(\tfrac12\ln(9/8)\) | the same value, \(0.058891517828192\), which rounds to the note's \(0.058891517828\). Squared partial correlations are \(1/9\). Signed correlations are \(+1/3\), \(+1/3\), and \(-1/3\). At \(\gamma=0\) the conditional information is \(0\) |
| One-statistic pool | six units, cost \(9.537667428571\) | six is the smallest count in \(\{1,\ldots,8\}\). \(P(K\ge 3)\) is \(2944/3125\) at five units and \(15360/15625 = 3072/3125\) at six. Expected decision variance \(470459/875000\). Heat plus upkeep is \(9\). Cost \(8345459/875000 = 9.537667428571\), which rounds to \(9.537667\) |
| Log-linear crossing of \(\Delta(r)/\Delta(0)\) through \(0.05\), path of \(61\), times \(1/4\) and \(1\) | \(0.710059035942\), \(1.468305301389\), ratio \(2.067863694520\), inside \([1.7, 2.3]\) | full values \(0.710059035941582\) and \(1.468305301389145\), ratio \(2.067863694519544\). Rounded to twelve decimals they are the printed triple, and the ratio is inside \([1.7, 2.3]\) |

The crossing was computed three ways for the matrix exponential (symmetric eigendecomposition, scaling-and-squaring Taylor, and SciPy's Padé exponential) and two ways for \(\Delta(r)\) (the principal precision block of the unseen sites, and the covariance regression). The two variance formulas agree to about \(10^{-16}\). All three exponentials agree through the twelve printed digits.

## Other printed figures that were recomputed

These are in the note and were not in the requested list. They match as well.

| Quantity | Note | Recomputed |
|---|---|---|
| \(I(X_0;X_2)\) on the path of three | \(0.020410997260\) | \(0.020410997260128\), and \(I(X_0;X_2\mid X_1)=0\) |
| Gasket holding bounds | blanket \(26\); region \(54, 171, 522, 1575\) | the same integers, from degrees: two glue vertices of degree \(4\), and inside the region one degree-\(2\) vertex with the rest degree \(4\). No region–exterior edge |
| Gasket interior minima, generations \(2\) and \(5\) | \(0.227272727273\), \(0.247979948223\) | \(0.227272727272727\), \(0.247979948223363\) |
| Open square, side \(8\) | bounds \(106\) and \(326\); interior minimum \(0.234882445959\) | bounds \(106\) and \(326\); minimum \(0.234882445959072\). Sizes \(24\), \(8\), \(32\), and no region–exterior edge |
| Integer \(5\%\) radius, paths of \(31\) and \(61\), \(\tau=1/2\) and \(\tau=1\) | \(2\) and \(2\), ratio \(1\), a puzzle | \(2\) and \(2\) on both paths. At \(\tau=1/2\), \(\Delta(1)/\Delta(0)=0.05282632\) and \(\Delta(2)/\Delta(0)=0.00135088\). At \(\tau=1\), \(0.15690153\) and \(0.01364853\). The level \(0.05\) sits between radius \(1\) and radius \(2\) at both times |
| Relative gap of the crossing ratio from \(2\) | \(0.033932\) | \(0.03393184726\), which rounds to \(0.033932\) |
| Bracket densities in the crossing preregistration's evaluation | \(\rho(1)=0.014713\) at \(\tau=1/4\); \(\rho(1)=0.156902\), \(\rho(2)=0.013649\) at \(\tau=1\) | \(0.01471349139\), \(0.15690153469\), \(0.01364852543\) |

The integer-radius ratio \(1\) is below the locked band \(1.05\). The preregistration says that comparison is a puzzle and does not fail the script. The note labels it **OPEN** and a puzzle. That wording matches the recomputed radii.

## Preregistration order

Both files have the stated sha256, and neither blob changes after its lock commit.

| File | sha256 | Git blob | Lock commit |
|---|---|---|---|
| `theory/boundary_checks/PREREG.md` | `58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c` | `82d4f04e66b3dfbb72dae5088fe3ca1ba0a022f4` | `f5a930e64d28df57145f4b56d0f32a442c27367a` |
| `theory/boundary_checks/PREREG_CROSSING.md` | `05f4d12445092d90ff48cbf20985b0e358c1d46ea17e74d1f294f1064cb40ae2` | `56bc0091b5ed1589efad15c95d75bf916135b93a` | `8afc11fb4b26279b8b404f8378e90b037b787ea8` |

`git diff 8afc11f HEAD -- theory/boundary_checks/PREREG.md theory/boundary_checks/PREREG_CROSSING.md` is empty. The same preregistration blob is in every commit from `f5a930e` through `c55cd87`. The crossing blob is the same from `8afc11f` through `c55cd87`.

Parent chain on this branch, with author date and committer date:

1. `f5a930e64d28df57145f4b56d0f32a442c27367a`, parent `b6e351eeb6b6a676c0f5e1ad83a03cfc15883b6c`. Author `2026-11-22T20:43:10Z`, committer `2026-11-22T21:10:43Z`. Adds only `theory/boundary_checks/PREREG.md`. The tree has no check script and no results note.
2. `0e8abc674ac410558d5a8c6789671dd572602b39`, parent `f5a930e`. Author `2026-11-22T20:54:51Z`, committer `2026-11-22T21:11:16Z`. Adds the note, `boundary_checks.py`, and the gasket figure `1.290955`. `git log -S 1.290955` first hits this commit. The T44 row in this commit says a log-linear crossing is a separate preregistration. It does not contain `0.710059035942`.
3. `8afc11fb4b26279b8b404f8378e90b037b787ea8`, parent `0e8abc6`. Author and committer `2026-11-22T21:11:32Z`. Adds only `PREREG_CROSSING.md`. The check-script blob is still the one from `0e8abc6` (`be5c678273c465ffd484649a36a3d016c2108a94`). `git grep` of `0.710059` and `log_linear_crossing` at this commit is empty.
4. `c55cd8782de62c2cbe2075d4064ea8828e236392`, parent `8afc11f`. Author and committer `2026-11-22T21:18:41Z`. `git log -S 0.710059035942` first hits this commit. It edits the note, the script, `LOCK.txt`, and `OPEN_WORK.md`. It does not edit either preregistration.

The original lock object is still in the database: `93084b06da8b6b9b8cb66f671c19368ff3255a48`, parent `13eec9af0b3385f9a433d0c1f62d341c8a520e2d`, author and committer `2026-11-22T20:43:10Z`. It adds only `PREREG.md`, and that blob is the same object as at `f5a930e`. It is not an ancestor of `HEAD` (`git merge-base --is-ancestor` exits \(1\)); the rebase onto `b6e351e` rewrote the commit id and the committer date and kept the bytes. Author dates stay in order: lock `20:43:10Z`, first results `20:54:51Z`, crossing lock `21:11:32Z`, crossing results `21:18:41Z`. Committer dates on the rebased chain stay in that same order.

## Checks

All of these were `nice -n 19` from the repo root on `c55cd87`. No `lake` build.

| Command | Result |
|---|---|
| `python3 theory/boundary_checks/boundary_checks.py` | exit \(0\). `PASS 107  FAIL 0  PUZZLES 1`, `FAILS 0`, `ALL BOUNDARY SUFFICIENCY CHECKS PASS`. The puzzle line is `PUZZLE  P9 radius ratio  r(1/2)=2 r(1)=2 ratio 1.000000`. The crossing line is `PASS  C1 log-linear crossing ratio  r(1/4)=0.710059035942 r(1)=1.468305301389 ratio 2.067863694520` |
| `python3 tools/check_open_work.py` | `RESULT: PASS`. Missing ids: \(0\) |
| `python3 tools/check_consistency.py` | `RESULT: PASS`. `FAIL: 0`. Advisory length warnings on `THEORY.md` (11134 words) and `README.md` (1476 words). This pull request does not edit those files |
| `python3 tools/check_fresh.py` | `RESULT: PASS`. `STATUS.md` main is `13eec9a`, inside the five-commit window |
| `python3 -m pytest -q tools` | `259 passed, 1 skipped in 363.64s`. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed` |

## Hypothesis sentence

The sentence is one copy, the same bytes, in `CORE.md:9`, `THEORY.md:41`, `README.md:9`, the note at line 9, `PREREG.md:11`, and `PREREG_CROSSING.md:9`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

Each of those lines is that sentence wrapped in `**`. `git rev-parse b6e351e:CORE.md` equals `HEAD:CORE.md`, and the same holds for `THEORY.md` and `README.md`.

## Wording

The new lines use **cost**. `git diff -U0 b6e351e...HEAD` adds no `bill` and no `kill`.

The zero pattern of \(Q\) is labeled **KNOWN**, credited to Speed and Kiiveri, with Besag named for the Hammersley–Clifford theorem. The block argument for this \(Q\) is the part marked **PROVED**.

The claim "this is AdS/CFT or the Bekenstein–Hawking area law" is labeled **METAPHOR**. The note says no such map is shown, and that the cost here is \(\operatorname{tr}(\Phi)\) on the sites of a graph.

The integer \(5\%\) radius is labeled **OPEN** and a puzzle. The recomputed ratio is \(1\).

`OPEN_WORK.md` has row T44.
