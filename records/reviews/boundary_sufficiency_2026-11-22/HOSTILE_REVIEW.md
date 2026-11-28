# Hostile review of draft PR #194

**VERDICT: NEEDS-FIXES.**

Independent review of head `888406f5279fb77a911f3d531605ec45ce3c59dc` on `boundary-sufficiency-2026-11-22`, two commits on parent `13eec9af0b3385f9a433d0c1f62d341c8a520e2d`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake` build. Computations at nice 19.

The screening statement is the right one, and the arithmetic behind it recomputes. In the equilibrium Gaussian field, the exterior given the blanket has the same conditional law as the exterior given the blanket and the region, the decision loss of a channel of those sites is a function of the blanket posterior, and a perfect blanket leaves every interior variance at least \(1/5\), above the tolerance \(1/18\). The Schur trace on the gasket settles at \(1.290955\) while the region grows from \(4\) sites to \(121\). The holding bounds are \(26\) on the two glue vertices and \(54, 171, 522, 1575\) on the region. The path-of-three channel with a cross term reaches exterior variance \(13/25\) at trace \(10.1\), and the blanket-only match costs \(10.5\). The long-range edge, the equicorrelated covariance, and the MA(1) each leave \(\tfrac12\ln(9/8)\). The discrete excesses are \(1/16\), \(1/256\), and \(1/4096\). The pool of six units costs \(8345459/875000\), and every copy stops at variance \(7/12\).

Two summary sentences say something the propositions do not. The opening says a channel of the whole region costs more than a blanket channel, by at most the Schur trace. The proposition, the path of three, and the pull-request body say the matching blanket channel is the one that costs more. The same opening, the pull-request body, and the new OPEN_WORK row say the conditional law given the region equals the law given the blanket. On the path of three those variances are \(3/5\) and \(1/2\). The \(5\%\) radius ratio is a real puzzle, the path length is not the cause, and the sentence that both a factor \(\sqrt{2}\) and a factor \(2\) are invisible to the integer is too strong for the factor \(2\). The new row is numbered T43. Draft PR #191 already uses T43 for a different question. Main's T41 and T42 are untouched.

The hypothesis sentence is one copy in each of `THEORY.md`, `CORE.md`, and `README.md`, the same bytes at head and at `origin/main` `13eec9af`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`git diff 13eec9af 888406f` is empty on all three.

Recomputation did not import `theory/boundary_checks/`. Conditional covariances are Schur complements of \(\Sigma=Q^{-1}\). The Schur trace is \(\operatorname{tr}(Q_{BI}Q_{II}^{-1}Q_{IB})\). The radius profile is the quadratic form \(w_{\mathrm{out}}^\top Q_{\mathrm{out}}^{-1}w_{\mathrm{out}}\) with \(w\) the center row of \(e^{-\tau Q}\), and \(e^{-\tau Q}\) is the symmetric eigendecomposition. Modified Bessel weights are the power series. The pool, the path-of-three channel, and the finite-speed coefficients are exact fractions. The gasket is the corner-gluing locked in the preregistration. NumPy 1.26.4. The script is `reviews/boundary_sufficiency_2026-11-22/checks/recompute.py`.

## The lock

The preregistration precedes the computation, the hash matches, and the file was not edited.

| | |
|---|---|
| Preregistration commit | `93084b06da8b6b9b8cb66f671c19368ff3255a48`, 2026-11-22 20:43:10 +0000 |
| Parent | `13eec9af0b3385f9a433d0c1f62d341c8a520e2d` (`origin/main`) |
| Files in that commit | `theory/boundary_checks/PREREG.md` only |
| Computation commit | `888406f5279fb77a911f3d531605ec45ce3c59dc`, 2026-11-22 20:54:51 +0000 |
| Blob of `PREREG.md` at both commits | `82d4f04e66b3dfbb72dae5088fe3ca1ba0a022f4` |
| sha256 of the file bytes | `58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c` |

The computation commit adds the note, the checks, the lock file, the Crossref log, the test wrapper, and one OPEN_WORK row. It does not touch `PREREG.md`. The gap is 11 minutes 41 seconds. The git record cannot see an uncommitted scratch run. What it can see is that the lock commit contains no precision matrix, no inversion, and no script, and that the file at head is the file that was hashed.

## What holds

**The exterior screening identity.** On the path of three, \(\operatorname{Var}(X_2\mid X_1)=\operatorname{Var}(X_2\mid X_0,X_1)=1/2\), \(\operatorname{Var}(X_2\mid X_0)=3/5\), \(\operatorname{Var}(X_0\mid X_1)=1/2\), and \(I(X_0;X_2)=\tfrac12\ln(25/24)=0.020410997260\). The conditional covariance of the two ends given the middle is diagonal. Proposition BS-screen is this identity: \(X_R\perp X_E\mid X_B\), and both conditional covariances of the exterior equal \(Q_{EE}^{-1}\).

On the gasket the largest entrywise gap between the two exterior conditional covariances is \(2.8\times 10^{-17}\) at generation 5, and the cross block \(Q_{RE}\) is the zero matrix. On the open square of side 8 the same gap is \(2.8\times 10^{-17}\). Interior conditional variances match the diagonal of \(Q_{RR}^{-1}\) to \(3\times 10^{-16}\).

**The Schur trace, and the bounds.** Generations 2 through 5, one subcopy with its two glue vertices removed:

| Generation | \(\lvert R\rvert\) | \(\operatorname{tr}(K)\) | Blanket bound | Region bound | Blanket load | Region load | Interior minimum |
|---|---|---|---|---|---|---|---|
| 2 | 4 | \(1.234848484848\) | 26 | 54 | \(28.605907\) | \(60.427399\) | \(0.227272727273\) |
| 3 | 13 | \(1.290266004092\) | 26 | 171 | \(28.582453\) | \(196.372369\) | \(0.247717180997\) |
| 4 | 40 | \(1.290954813099\) | 26 | 522 | \(28.581910\) | \(604.222673\) | \(0.247979893160\) |
| 5 | 121 | \(1.290954956476\) | 26 | 1575 | \(28.581910\) | \(1827.773585\) | \(0.247979948223\) |

Vertex counts are \(15, 42, 123, 366\), which is \(\tfrac32(3^g+1)\). Each glue vertex has degree 4. Inside the region, one vertex has degree 2 and the rest have degree 4, so the region bound is \(13\lvert R\rvert+2\). The trace \(1.290954956476\) rounds to the note's \(1.290955\). From generation 3 to generation 5 it moves by \(6.9\times 10^{-4}\). At generation 5 the region load is \(63.9486\) times the blanket load, which prints as \(63.95\), against the site ratio \(121/2=60.5\).

The same trace on a path whose blanket is the two sites next to a growing middle saturates at \(0.763932\) from length 15 through length 61. On the open square it is \(1.998117\), with blanket bound \(106\), region bound \(326\), blanket load \(117.184595\) (\(14.648074\) per site), and interior minimum \(0.234882445959\). The excess over a channel of the region stays a boundary quantity on these graphs while the holding bound of the region tracks the region.

**The path of three.** The update with interior diagonal \(1/10\), cross entry \(1\), and blanket diagonal \(10\) is positive semidefinite of rank one. Its trace is \(10.1\). The posterior variances are \(2/25\) on the blanket site and \(13/25\) on the exterior site. The blanket-only precision that matches the blanket variance is \(21/2=10.5\). The excess is \(2/5\), and \(\operatorname{tr}(Q_{BI}Q_{II}^{-1}Q_{IB})=1/2\). A diagonal split of the same trace goes the other way: precision \(2\) on the blanket leaves exterior variance \(9/16\), precision \(1\) on each site leaves \(11/19\), and the gap is \(5/304\). Forty channels drawn as \(A^\top A\) with normal scale \(0.4\) and seed 7 stay under the cap. The largest excess is \(0.082158737532\). Thirty channels on the path of five, seed 11, stay under \(2/3\). The largest excess is \(0.034554\).

**The interior floor.** \(\operatorname{Var}(X_i\mid X_B)\ge 1/Q_{ii}\). With \(\alpha=\beta=1\) and degree at most 4, \(Q_{ii}\le 5\), so the conditional variance is at least \(1/5\). Since \(1/5>1/18\), perfect observation of the blanket misses the interior tolerance. On the path of three the interior variance given the blanket is \(1/2\). On the path of five, \(\operatorname{Var}(X_2\mid X_1,X_3)=1/3\). The gasket and square minima above all sit above \(1/5\).

**The three leakages.** Each conditional information is \(\tfrac12\ln(9/8)=0.058891517828\).

- Long-range, \(\gamma=1\): the conditional precision of the ends given the middle is \(\begin{pmatrix}3&-1\\-1&3\end{pmatrix}\), partial correlation \(1/3\). At \(\gamma=0\) the conditional information is \(0\).
- Equicorrelated, unit variance and covariance \(1/2\): conditional correlation \(1/3\).
- MA(1), \(X_t=\xi_t+\xi_{t-1}\): unconditional correlation of lag 2 is \(0\), conditional correlation \(-1/3\).

**Discrete thickening.** On the infinite line the range-1 kernel puts mass \((1/4)^H\) at distance \(H\) after \(H\) steps and mass \(0\) beyond it. The excess conditional variance is the square: \(1/16\), \(1/256\), \(1/4096\) at horizons \(1, 2, 3\). Range 2 puts mass \(1/6\) at distance 2 after one step and mass \(1/36\) at distance 4 after two steps. The excesses are \(1/36\) and \(1/1296\), and the second cutoff is distance 4.

**Continuous time.** The walk kernel \(e^{-2t}I_d(2t)\), summed through distance 40 by the power series, has second moment \(1.000000000000\) at \(t=1/2\) and \(4.000000000000\) at \(t=2\), and mass \(1\) at both. The regression kernel \(e^{-3\tau}I_d(2\tau)\) at distance 15 and \(\tau=1/2\) is \(5.289218\times 10^{-18}\). On the path of 31 every \(\Delta(r)\) for \(r<15\) is positive at both times, the smallest values are \(1.908\times 10^{-33}\) and \(1.853\times 10^{-27}\), and \(\Delta(15)=0\).

**The pool.** Prior variance of the blanket site \(1/2\). Precision \(\Phi\) leaves exterior variance \(\tfrac12+\tfrac14\cdot\tfrac1{2+\Phi}\). The tolerance \(0.55=11/20\) needs \(\Phi\ge 3\). The best up-state of a copy is one survivor at the cap \(c=1\), variance \(7/12\), at every count. A pool needs three survivors. The chance of three or more is \(2944/3125=0.94208\) at five units and \(15360/15625=0.98304\) at six. Six is the smallest count in \(\{1,\ldots,8\}\). The expected decision variance is \(470459/875000\). Heat plus upkeep is \(9\). The cost is \(8345459/875000=9.537667428571\).

On the path of five the sum of the two end variances is \(1\) given both blanket sites and \(121/110\) given only their sum. The pooled statistic is higher by \(1/10\). For \(Z=X_0+X_4\) both posterior variances equal \(1\).

## Screening, and the physics names

The proved sentences are a screening claim. BS-screen and BS-loss say the exterior's conditional law, and therefore an exterior mean-square loss, is fixed once the blanket posterior is fixed. BS-interior says the same blanket leaves the interior above \(1/18\). The holding bound on the blanket is the cut bound of the holographic note, summed over the blanket sites, and on this gasket that sum stays \(26\) while the region bound runs into the thousands. Calling that memory a hologram, a bulk reconstruction, or a Bekenstein–Hawking bound adds a prediction the cost equation does not make. The note marks those names **METAPHOR**. It constructs no bulk metric, no conformal boundary, and no isometry from a bulk Hilbert space onto a boundary space. The cost it computes is \(\operatorname{tr}(\Phi)\) on the sites of a graph.

That framing is the honest one. It is the framing of BS-screen, BS-loss, BS-cap, and BS-interior. The opening paragraph of §0 says two further things, and those two are the sentences under repair below. They are slips of summary inside the screening argument. The page builds no bulk metric, no conformal boundary, and no horizon-area formula.

Wolf, Verstraete, Hastings, and Cirac are left as **KNOWN** for the field's mutual information. The checks here do not recompute it. The arXiv abstract of `0704.3906` says the information in part of a system in thermal equilibrium obeys an area law, that this comes from the laws of classical and quantum physics, and that the maximal information per unit area depends classically on the number of microscopic degrees of freedom. The note's clause "including the classical thermal case" matches that abstract. The field's mutual information is a different quantity from this heat, which is what the holographic note already says.

## The radius

The locked radius is the smallest integer \(r\) with \(\Delta(r)\le 0.05\,\Delta(0)\). It is \(2\) at \(\tau=1/2\) and \(2\) at \(\tau=1\). The ratio is \(1\), which is below the locked band \(1.05\), so the preregistration files a puzzle and names one next test: the same definition on a path of \(61\). That path returns \(2\) and \(2\) again. The normalized profile through radius 4 agrees between length 31 and length 61 to a relative gap below \(10^{-9}\). The path length was not the cause. Filing the ratio as a puzzle, and refusing to replace the locked cutoff after seeing it, is the right handling of a tolerance.

The level really does sit between radius 1 and radius 2 at both times.

| \(\tau\) | \(\Delta(0)\) | \(\Delta(1)/\Delta(0)\) | \(\Delta(2)/\Delta(0)\) |
|---|---|---|---|
| \(1/2\) | \(1.5456\times 10^{-2}\) | \(0.052826\) | \(0.001351\) |
| \(1\) | \(8.0049\times 10^{-3}\) | \(0.156902\) | \(0.013649\) |

The integer is therefore \(2\) at both times, and it cannot display \(\sqrt{2}\). A continuous crossing of the same level is a different fact, and it moves. Linear interpolation in \(r\) puts the crossing at \(1.0549\) and \(1.7462\). Log-linear interpolation in the ratio puts it at \(1.0150\) and \(1.4683\). The log-linear ratio is \(1.447\), near \(\sqrt{2}=1.414\). Neither interpolation was locked. Neither is a result.

A factor \(2\) applied to a crossing near \(1.05\) lands past \(2\): \(2.030\) on the log-linear crossing and \(2.110\) on the linear crossing. The first integer at which the curve is under \(0.05\) would then be \(3\). The observed \(\Delta(2)/\Delta(0)\) at \(\tau=1\) is \(0.0136\), under \(0.05\), so that doubling did not happen. The sentence in §5 that a square-root factor and a linear factor are both smaller than the gap, and that the integer can show neither, overstates the blindness to the factor \(2\).

The walk second moment \(2t\) is the diffusive identity, and it holds. Doubling the root-mean-square distance of that kernel takes a factor four in time. The \(5\%\) integer is a coarser statistic of a different object, the conditional variance of the future mean. The preregistration's path-of-61 test has answered the question it was asked.

The next preregistration should lock a continuous crossing before any new evaluation. Define \(r_{0.05}(\tau)\) as the log-linear crossing of \(\Delta(r)/\Delta(0)\) through \(0.05\), on a path of length 31 or 61. Use a pair of times other than \((\tfrac12, 1)\), because that pair's profile, including the crossings above, has been inspected. Predict that the ratio of crossings equals the square root of the ratio of the times, inside a band that excludes \(1\) and excludes the time ratio itself. Do not enter \(1.447\) as a pass. A finer threshold on the same inspected pair would be a re-read, and the preregistration already forbids substituting one.

## Citations

Crossref HTTP 200 for every DOI below, fetched again this session. Titles, years, venues, page fields, and author surnames match the preregistration and the reference list, except the one sentence in F5.

| DOI | Record | Abstract in the record |
|---|---|---|
| `10.1214/aos/1176349846` | Speed and Kiiveri, *Ann. Statist.* 14:138–150 (1986) | Zeros of the inverse characterise the conditional independencies. Matches the note. |
| `10.1111/j.2517-6161.1974.tb00999.x` | Besag, *J. R. Statist. Soc. B* 36:192–225 (1974) | An alternative proof of Hammersley–Clifford, used for binary and Gaussian schemes. Matches the note. |
| `10.2307/2528966` | Dempster, *Biometrics* 28:157 (1972) | None. The note says so. The page field in the record is the first page. |
| `10.1093/oso/9780198522195.001.0001` | Lauritzen, *Graphical Models* (1996) | Describes the monograph, including Markov properties of graphs. It does not state the block formula. Matches the note. |
| `10.1201/9780203492024` | Rue and Held, *Gaussian Markov Random Fields* (2005) | None. The note says so. |
| `10.1007/978-0-387-30164-8_509` | "Markov Blanket", *Encyclopedia of Machine Learning* (2011), p. 639 | No authors and no abstract. The preregistration says no definition is taken. The note's reference list omits the entry. |
| `10.1103/PhysRevD.7.2333` | Bekenstein, *Phys. Rev. D* 7:2333–2346 (1973) | None. No entropy formula is used. |
| `10.1007/BF02345020` | Hawking, *Commun. Math. Phys.* 43:199–220 (1975) | None. No entropy formula is used. |
| `10.1103/PhysRevLett.100.070502` | Wolf, Verstraete, Hastings, and Cirac, *Phys. Rev. Lett.* 100 (2008) | None in the Crossref record. The arXiv abstract supports the classical clause, as above. |
| `10.1023/A:1026654312961` | Maldacena, *Int. J. Theor. Phys.* 38:1113–1133 (1999) | None. See F5. |
| `10.1103/RevModPhys.74.825` | Bousso, *Rev. Mod. Phys.* 74:825–874 (2002) | None. The note does not paraphrase one. |

A bibliographic query for "Hammersley Clifford 1971 Markov fields finite graphs lattices" returned `total-results` \(1515788\), the same count as `theory/boundary_checks/crossref.out`. The first page does not contain a work record for the 1971 manuscript. The DOIs listed in that file are on the page. A later item on the page I fetched, Chandgotia, *Trans. Amer. Math. Soc.* (2017), doi `10.1090/tran/6899`, is a different paper that names the theorem. The note's statement of the manuscript's absence is accurate.

## OPEN_WORK

Main at `13eec9af` ends the numbered rows at T42. This branch inserts one row after T42 and changes nothing else in the file. T41 and T42 are byte-identical to main.

The inserted id is T43. Draft PR #191, branch `antifragility-turnover-2026-11-22`, head `7047721e0b3394778d43e88bf954d01eaeee254f`, is also one insertion after T42, and that row is a different T43: shock-driven replacement of capacity-limited units. The two drafts collide on the id and on the line. The next free id is T44.

## Wording

The note, the preregistration, the checks, the lock file, and the new OPEN_WORK row use cost. The words bill and kill are absent from those files. The radius ratio, which is the one locked tolerance, is filed as a puzzle in §0, §5, §8, and the T43 row. The checker counts it as a puzzle (`PUZZLE` on the radius, then `PASS 107`, `FAIL 0`, `PUZZLES 1`). The sentences the preregistration predicted would miss — pure blanket support, interior sufficiency, the long-range edge, the equicorrelated covariance, the MA(1), a finite shell in continuous time, and one sum for a per-site loss — are labeled **FAILS**, which is the label the preregistration told the results note to apply after the checks. That split matches the instruction.

## Required fixes

**F1. The opening reverses the heat comparison.** Section 0 says:

> The heat of a channel that sees the whole region exceeds the heat of a channel that sees only the blanket by at most the trace of one Schur complement, and that trace stays near \(1.291\) on the gasket while the region grows from \(4\) sites to \(121\).

BS-cap says the opposite direction, and the path of three is the witness. The matching blanket channel has trace \(10.5\). The channel with the cross term has trace \(10.1\). The excess \(2/5\) is at most the cap \(1/2\). The trace values on the gasket are right, and the pull-request body already has the direction of BS-cap.

Write the sentence as BS-cap has it: for each channel supported on the region and the blanket, the blanket-only update that matches that channel's posterior precision of the blanket costs at most \(\operatorname{tr}(Q_{BI}Q_{II}^{-1}Q_{IB})\) more than the channel it matches, and on the gasket that trace settles at \(1.290955\) while the region grows from \(4\) sites to \(121\). In the label table and in the T43 row, replace "any region channel" with "the channel it matches."

**F2. The law given the region alone is a different law.** Section 0, the pull-request body, and the T43 row say the conditional law of the exterior given the region equals the law given the blanket, and that the decision loss is the same.

BS-screen says \(X_R\perp X_E\mid X_B\): the conditional covariance of the exterior given the blanket equals the conditional covariance given the region and the blanket, and both equal \(Q_{EE}^{-1}\). Conditioning on the region alone drops the blanket. On the path of three, \(\operatorname{Var}(X_2\mid X_0)=3/5\) and \(\operatorname{Var}(X_2\mid X_1)=1/2\). The decision loss of a perfect reading of the region is the first of those. The decision loss of a perfect reading of the blanket is the second.

Write that sentence, in all three places, as the proposition has it. Keep \(3/5\) beside \(1/2\) so the summary and §2 say the same thing.

**F3. The integer radius is blind to \(\sqrt{2}\) and had room to show a factor \(2\).** Section 5 says the level \(0.05\) sits in the gap between radius 1 and radius 2 at both times, so the integer cannot move, and that a square-root factor \(\sqrt{2}\) and a linear factor \(2\) are both smaller than that gap.

The first clause is right, and the table above is the evidence, on a path of 31 and again on a path of 61. A \(\sqrt{2}\) thickening of a crossing near \(1.05\) stays inside \((1,2)\), so the integer stays \(2\). Doubling that crossing lands at \(2.03\) or \(2.11\), and the integer would have become \(3\). Replace the sentence that both factors are smaller than the gap with that distinction. Keep the ratio \(1\) as a puzzle. Keep the second-moment identity as the diffusive statement that passed.

The path-of-61 test named in the preregistration has been run. The next preregistration is the continuous crossing in the radius section above: log-linear in \(\Delta(r)/\Delta(0)\) through \(0.05\), a time pair other than \((\tfrac12,1)\), prediction equal to the square root of the time ratio, band excluding \(1\) and excluding the time ratio. The interpolated ratio \(1.447\) on the inspected pair stays out of the note.

**F4. The new row collides with draft PR #191.** Renumber it from T43 to T44. Leave T41 and T42 as they stand on main. The antifragility row keeps T43.

**F5. The Maldacena sentence cites an abstract the saved record does not contain.** Section 7 says the holographic note already says what the fetched abstract supports, a large-\(N\) limit with a supergravity sector on anti-de Sitter space inside a conformal field theory.

The Crossref record for `10.1023/A:1026654312961`, fetched again this session and saved in `theory/boundary_checks/crossref.out`, has title, author, *Int. J. Theor. Phys.* 38 (1999) 1113–1133, and no abstract. Write that the record resolved and contained no abstract, and that the AdS sentence is the sentence already in `theory/HOLOGRAPHIC_2026-11-22.md`. Keep the **METAPHOR** label. Bekenstein 1973 and Hawking 1975 are already described the way their records read: titles, pages, no abstract, no formula taken.

## Nits

**N1.** The label "PROVED as the bounds and the loads" mixes the identity with the bisection. The bounds are \(13\lvert R\rvert+2\) once the region has one degree-2 vertex and the rest degree 4, which the graph has at all four generations. The loads are the uniform diagonal bisection, and they sit above the bounds. Say the bounds are the proof and the loads are the achieved costs.

**N2.** Generation 3's region load prints as \(196.372369\). The bisection value is \(196.37236877\), which rounds to that. Generation 5's blanket load prints as \(28.581910\). The bisection value is \(28.58190991\), which rounds to the same six decimals as generation 4. Both printings are the right rounding. No change is required if the sentence stays at six decimals.

## Checks run

At nice 19, from independent code, NumPy 1.26.4. No SciPy. No `lake` build. The author's checker was executed as a separate process, not imported:

| Command | Result |
|---|---|
| `nice -n 19 python3 reviews/boundary_sufficiency_2026-11-22/checks/recompute.py` | The tables in this review |
| `nice -n 19 python3` on the checker blob at `888406f` (`theory/boundary_checks/boundary_checks.py`) | `PASS 107`, `FAIL 0`, `PUZZLES 1`, exit 0 |

Pytest, `tools/check_consistency.py`, and `tools/check_open_work.py` were not rerun.

VERDICT: NEEDS-FIXES
