# Confirm: holographic heat floor, 22 November 2026

CONFIRM: READY

Independent read of draft PR #184 at head `efa47c9005b833810e0ed53c3b444ac659b2e4e6` on `holographic-2026-11-22`. The base of that pull request is `main` `6340b177bae94074d90bdbb3a2bfaad0e4915d90`. That branch was not edited. This file is the only change against `main`. The text reviewed is `theory/HOLOGRAPHIC_2026-11-22.md` at `efa47c9`, together with the T41 row in `OPEN_WORK.md` and `theory/holographic_checks/`. The repairs answer `reviews/holographic_2026-11-22/HOSTILE_REVIEW.md` on `review-holographic-2026-11-22` (PR #185), which read the earlier head `11647e85b33098b21cad4bd28c367e9a6d7aa06e`.

The numbers below were recomputed in a separate script. It does not import `theory/holographic_checks/`. Path eigenvalues are \(2-2\cos(\pi k/n)\), checked against a hand-built path Laplacian. Periodic rates are the cosine symbol. The cut cost is a bisection on a precision matrix built for this read. Ordinary least squares is a separate implementation. NumPy 1.26.4 for that script and for the note's own script.

## Protected files

`git diff origin/main efa47c9 -- THEORY.md CORE.md README.md` is empty. The three files are byte-identical to `main` (165741, 18262, and 9061 bytes). The hypothesis sentence is present once in each file, with the same bytes, including the bold markers:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The same bytes appear once in the note. The note does not edit `THEORY.md`. `efa47c9` has parents `11647e8` and `6340b17`, so current `main` is in the branch. The merge of PR #182, `df9fc05`, is an ancestor.

## Listed items

**B1.** Fixed. The learning-rate share is \(a_k v_k g_k^2/\sigma^2\), with \(g_k=1/(a_k+\mu)\) and \(\sigma^2=\sum a_k v_k g_k^2/\mu\). The weight \(a_k v_k/(a_k+\mu)^2\) is the numerator. On \(k\in[-80,80]\), \(a_k=\rho^k\), \(v_k=1\):

| \((\rho,\mu)\) | weight sum | \(\sigma^2\) | share sum | share ratio | closed form \((\rho^2+1)^2/(4\rho^2)\) |
|---|---|---|---|---|---|
| \((2,4)\) | \(0.360673760240\) | \(0.090168440060\) | \(4\) | \(1.562500000000\) | \(1.5625\) |
| \((10,10)\) | \(0.043711336500\) | \(0.004371133650\) | \(10\) | \(25.502500000000\) | \(25.5025\) |

The printed \(0.360674\), \(0.090168\), \(0.043711\), and \(0.004371\) are those values rounded. The weight ratio equals the share ratio at both points. The two printed ratios stand.

**S1.** Fixed. A \(10\%\) cut of \(\operatorname{tr}(\Sigma)\) on the open cube first exceeds the surface cap \(A/\alpha\) at side \(210\) in \(d=3\), \(\alpha=1\), \(\beta=0.5\). Every integer from \(190\) through \(220\) was recomputed, and sides \(100\) and \(150\) sit under the cap (need/cap \(0.484\) and \(0.719\)).

| side | need | cap | \(A\) | \(V\) | fits |
|---|---|---|---|---|---|
| \(209\) | \(258473.610962\) | \(259586\) | \(259586\) | \(9129329\) | yes |
| \(210\) | \(262195.958285\) | \(262088\) | \(262088\) | \(9261000\) | no |
| \(212\) | \(269747.523946\) | \(267128\) | \(267128\) | \(9528128\) | no |

Side \(212\) is the first multiple of \(4\) past that crossing. The same scan gives the first sides \(44\) in \(d=1\) (need \(2.007740\), cap \(2\); side \(43\) need \(1.963018\)) and \(156\) in \(d=2\) (need \(622.924490\), cap \(620\); side \(155\) need \(614.993726\), cap \(616\)).

**S2.** Fixed. On the eighteen even-sided cells, \(\lambda_{\max}=\alpha+4d\beta\) is independent of \(n\), and the heat is \(V(1/\varepsilon-\alpha-2d\beta)\). The eighteen slopes run from \(1-2\times 10^{-16}\) to \(1+2\times 10^{-16}\), standard deviation \(1.592\times 10^{-16}\), largest standard error \(8.091\times 10^{-16}\). The note's twelve nines are that roundoff, and the page says so. On odd sides \(n\in\{9,15,21,31,45,63\}\), \(d=1\), \(\alpha=\beta=1\), heat per site is \(3+4\cos(\pi/n)\), from \(6.758770\) to \(6.995028\). The slope is \(1.016062\), standard error \(4.315\times 10^{-3}\).

**S3.** Fixed. The cut row is in the table in §5. For \(\alpha=\beta=1\), \(d=2\), \(\varepsilon=1/18\), the bound is \(13\) per cut site. A uniform diagonal load on one line of the periodic square meets the tolerance from above:

| \(n\) | cost per cut site | total | bound |
|---|---|---|---|
| \(6\) | \(13.610380\) | \(81.662\) | \(78\) |
| \(8\) | \(13.606308\) | \(108.850\) | \(104\) |
| \(10\) | \(13.605851\) | \(136.059\) | \(130\) |
| \(12\) | \(13.605796\) | \(163.270\) | \(156\) |
| \(16\) | \(13.605788\) | \(217.693\) | \(208\) |

The printed sequence \(13.6104\), \(13.6063\), \(13.6059\), \(13.6058\), \(13.6058\) is that column rounded. At \(n=16\) the bulk floor is \(3328\). The exponent of this load against cut length is \(0.999690\), standard error \(1.381\times 10^{-4}\). On the strip of length \(8\), the interior row at \(y=W/2\) has \(Q_{ii}=5\), so the bound stays \(104\). The achieved cost is \(109.374223\), \(108.898356\), \(108.852703\), \(108.846858\) at widths \(4,6,8,12\). The page's \(109.374\) and \(108.847\) are the ends of that list.

The row's label is **PROVED** as the cost equation on the sites the decision names, and **METAPHOR** as a holographic encoding. The inequality \(L=\operatorname{tr}(\Phi)\ge |B|(1/\varepsilon-Q_{ii})\) is the linear-algebra bound on the page. The figure \(13.61\) is the load that meets the tolerance, and the text says it meets the tolerance from above. Depth is absent from that cost. §0 and the closing sentence of §5 say the same thing: area scaling of this cost is the cost equation on the named sites.

**S4.** Fixed. T40 is on the page, and T41 follows it. T41 says PR #182 has merged, T40 is the adoption item and is not applied, and this note does not adopt the proposal. `git diff origin/main efa47c9 -- OPEN_WORK.md` is the addition of that one row. The note's §1 says the same.

## Labels

**PROVED** on H-iface, H-volume, H-surface, H-octave, the zero mode, the disordered trace, and H-share matches a derivation that is on the page. H-share now names the share \(a_k v_k/((a_k+\mu)^2\sigma^2)\) and treats the weight as the numerator. The ratio identity is algebra; the truncation sums are the checks above. **FAILS** stays on path-keeping, the raw coordinate, futile affinity, a surface memory for the bulk gap, equal heat per octave, and a MERA degree. **KNOWN** stays on the field mutual information, with the lattice numbers marked as a numerical check. **METAPHOR** stays on the interface name, the boundary channel, the logarithmic count, and the holographic reading of the cut. "Nothing here is a conjecture" is compatible with those labels. The half-prior slopes remain a finite-grid fit, and the smallest tracked fraction on the \(\alpha=\beta=1\) grids is \(0.6250\).

## Wording

The diff of `efa47c9` against `origin/main` has no added line containing `bill`, `verdict`, or `theory of everything`. The substring `kill` occurs only inside the surname Preskill. The note calls the quantity a cost. Consistency reports 0 wording failures.

## One residual

The mutual-information sentence says that from \(n=8\) through \(n=24\), \(I/\mathrm{cut}\) stays \(0.032174\). On the sizes the script actually fits, \(\{8,10,12,16,20,24\}\), the ratios are \(0.032226\), \(0.032180\), \(0.032174\), \(0.032174\), \(0.032174\), \(0.032174\). The constant holds from \(n=12\). The slope \(0.998901\), standard error \(5.398\times 10^{-4}\), is the regression on those six sizes, and it is what the script prints. The review's \(0.998650\) is the same regression with \(n=10\) left out. The slope in the note matches the script.

The review also asked for a sentence on a mass \(\alpha=(2\pi/n)^2\), a fractional symbol, a fixed block length, and an area-sized total-error budget. Those four cases are absent from the note and from the script. The page does not claim them. The cut row that the review required is present, numbered, and labeled as above.

## Checks at `efa47c9`

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/holographic_checks/holographic_checks.py` | 175 checks, FAILS 0. NumPy 1.26.4 |
| `python3 tools/check_consistency.py` | PASS. 0 FAIL. 392 claim-map rows. Length warnings on THEORY and README are the pre-existing advisory |
| `python3 tools/check_open_work.py` | PASS. 0 missing |
| `nice -n 19 python3 -m pytest -q tools` | 255 passed, 1 skipped, 311.83 s |

The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed". No lake build. The tools run used pytest 9.2.0, SciPy 1.18.1, SymPy 1.14.0, and NumPy 2.5.5, because `np.trapezoid` is absent from NumPy 1.26.4 and that name is what the existing tools call. The holographic script does not call it. Its 175 checks were already green on NumPy 1.26.4, and the recomputed digits above match that run.

CONFIRM: READY
