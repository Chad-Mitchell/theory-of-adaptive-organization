# Preregistration: cost on a fractal world

*Sunday 22 November 2026. Locked before any diagonalization, any graph assembly, and any heat evaluation on these graphs. The check script is not in this commit. Predictions below are closed forms or arithmetic on closed forms. A later note may report what the code returned. This file is not edited after that.*

The question: on a world whose sites form a Sierpiński gasket or a Sierpiński carpet, does the minimum cost of judgment scale with the Hausdorff dimension or the spectral dimension, rather than with the number of sites?

This is a question about the geometry of the world. It is not the repository's fractal-time question. `theory/HT_INDEX.md`, the conditional statement T7, the withdrawn framing N46, and the T20 check are about the spectrum of a scalar process in time. None of those files contains a Sierpiński graph, a Hausdorff dimension of a domain, or a spectral dimension of a Laplacian. A search of the tree for those geometric terms, before this file, returned no model of a fractal domain.

## 0. What was fetched before this lock

Crossref API, 22 November 2026, HTTP 200, work record `10.1038/s41567-024-02551-8`. Type journal-article. Title: "Topological edge and corner states in bismuth fractal nanostructures." Container: Nature Physics. Issued 2024-07-01. Volume 20, issue 9, pages 1421–1428. Publisher: Springer Science and Business Media LLC. Authors, in the record's order: R. Canyellas, Chen Liu, R. Arouca, L. Eek, Guanyong Wang, Yin Yin, Dandan Guan, Yaoyi Li, Shiyong Wang, Hao Zheng, Canhua Liu, Jinfeng Jia, C. Morais Smith. The Crossref record contained no abstract.

arXiv API, the same day, HTTP 200, `2309.09860v2`, published 2023-09-18. Title on that record: "Topological edge and corner states in Bi fractals on InSb." The same author list. The abstract says that topological edge and corner modes arise in fractals formed by depositing thin layers of bismuth on an indium antimonide substrate, and that scanning tunnelling microscopy shows nearly zero-energy modes at the corners of Sierpiński triangles and outer and inner edge modes at higher energies. No sentence in the fetched abstract says that the cost of a decision scales with a dimension. That silence is the gap this preregistration is about. Nothing in this file is cited from a page that was not fetched.

The cost equation this prediction uses is already in the repository: the memory-bath heat floor is \(kT\) times the learning rate (`theory/INFO_PHYSICS_ATTAINABILITY.md`, IP11; `theory/INFO_PHYSICS_GENERAL.md`, IP12), and on a designated cut the same floor is at least the sum over the named sites (`theory/HOLOGRAPHIC_2026-11-22.md`, the cut bound of 13 per site on the even \(d=2\) lattice, met at about 13.61).

The hypothesis sentence is unchanged:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

## 1. Class and model

**Class F.** An exogenous equilibrium Gaussian field on a finite undirected graph. The precision is \(Q=\alpha I+\beta L\), with \(L=D-A\) the combinatorial Laplacian. The signal is

\[
dX=-QX\,dt+\sqrt{2}\,dW.
\]

The diffusion matrix is the identity, so \(Q\) and the prior covariance \(Q^{-1}\) share an eigenbasis. Each eigenmode is an equilibrium Ornstein–Uhlenbeck process with rate \(\lambda_k\) and variance \(1/\lambda_k\). Throughout, \(kT=\alpha=\beta=1\), except the small-mass arm in §5, where \(\alpha=10^{-8}\) and \(\beta=1\).

**Floor, all modes (IP12, not a new derivation).** If \(0<\varepsilon\le 1/\lambda_{\max}(Q)\), the heat floor of holding every mode at conditional variance \(\varepsilon\) is

\[
\sum_k\Bigl(\frac1\varepsilon-\lambda_k\Bigr)=\frac{N}{\varepsilon}-\operatorname{tr}(Q)=N\Bigl(\frac1\varepsilon-\alpha\Bigr)-\beta\sum_i\deg(i).
\]

**Floor, named sites (the cut bound of the holographic note).** If the conditional variance on each site of a set \(B\) is at most \(\varepsilon\), then any memory precision \(\Phi\succeq 0\) added to \(Q\) satisfies

\[
\operatorname{tr}(\Phi)\ge\sum_{b\in B}\Bigl(\frac1\varepsilon-Q_{bb}\Bigr),
\]

whenever each term is positive. The code will also compute the smallest uniform diagonal load on \(B\) that meets the tolerance, the same construction as `uniform_diagonal_load` in `theory/holographic_checks/holographic_checks.py`. That load is an achieved cost. It is not claimed to be the greatest lower bound.

**Matched tolerance.** The fixed tolerance is \(\varepsilon=1/18\). On any graph of maximum degree 4, \(\lambda_{\max}(L)\le 8\), so \(\lambda_{\max}(Q)\le 9\) and \(1/18<1/9\). The tolerance is feasible for every graph in §2. The code checks \(\lambda_{\max}(Q)\le 18\) anyway. The number \(1/18\) is the even \(d=2\) lattice value from the holographic note (\(\lambda_{\max}=9\), half the smallest prior variance).

**Graphs, definitions the code must follow.**

*Gasket \(G_g\), \(g=0,1,\ldots,6\).* \(G_0\) is a triangle: 3 vertices, 3 edges, corners \((0,1,2)\) in cyclic order. \(G_{g+1}\) is three copies of \(G_g\). With corners \((c_0,c_1,c_2)\) in cyclic order on each copy, the outer corners of the new graph are copy 0's \(c_0\), copy 1's \(c_1\), and copy 2's \(c_2\). The identified pairs are copy 0's \(c_1\) with copy 1's \(c_0\), copy 1's \(c_2\) with copy 2's \(c_1\), and copy 2's \(c_0\) with copy 0's \(c_2\). No other vertices are identified.

*Carpet cell graph \(C_n\), \(n=1,2,3,4\).* Cells are the unit squares of the standard carpet inside a \(3^n\times 3^n\) grid: at each level the open central ninth is deleted. Two kept cells are adjacent when they share a side. The outer boundary is the set of kept cells with a side on the outer perimeter of the big square. Spectrum and uniform load are required for \(n=1,2,3,4\). The degree-sum identity is required for the same range. \(n=5\) (\(N=32768\)) is outside this lock.

*Controls.* The periodic path and the periodic square, combinatorial Laplacian, sides \(n\in\{4,8,16,32,64\}\) for the gap formula and sides \(n\in\{4,8,16\}\) for the all-mode heat. The open square grid, sides \(n\in\{4,8,12,16\}\), for the boundary bound. Lattice eigenvalues used as controls are the closed form \(2-2\cos(2\pi j/n)\) and, in two dimensions, sums of two such terms. They are not fitted.

## 2. Counts that follow from the definitions

These are combinatorics. The code's graphs are wrong if they miss them.

**Gasket.** \(N(g)=\tfrac32(3^g+1)\). Values: \(g=0,\ldots,6\) give \(N=3,6,15,42,123,366,1095\). Three corners have degree 2. Every other vertex has degree 4. The degree sum is \(4N-6\). The graph distance between two corners is \(2^g\).

Hausdorff dimension of this construction: three copies, linear scale 2, so \(d_f=\log 3/\log 2=1.584962500721\). The outer boundary is the three corners at every generation, so the boundary count is \(B=3\) and the boundary dimension in that count is \(d_b=0\). Then

\[
\frac{d_b}{d_f}-1=-1.
\]

**Carpet.** \(N(n)=8^n\). Values: \(n=1,2,3,4\) give \(N=8,64,512,4096\). The number of edges is \(\tfrac85(8^n-3^n)\), so the degree sum is \(\tfrac{16}5(8^n-3^n)\) and the mean degree tends to \(16/5=3.2\). Derivation, locked with the formula: the level-1 cell graph is an 8-cycle (8 edges); level \(n+1\) joins 8 copies along 8 interfaces of length \(3^n\), and \(E(n)=\tfrac85(8^n-3^n)\) is the closed form of that recurrence. Outer-boundary count \(B(n)=4(3^n-1)\): \(8,32,104,320\).

Hausdorff dimension: eight copies, linear scale 3, so \(d_f=\log 8/\log 3=1.892789260714\). The outer boundary scales as the perimeter, \(d_b=1\), and

\[
\frac{d_b}{d_f}-1=\frac{\log 3}{\log 8}-1=-0.471679166426.
\]

The four geometric corners have degree 2. A non-corner cell on one outer side has degree 2 if its inward neighbour was deleted and degree 3 if that neighbour was kept. The inward-kept pattern on one side is three copies of the previous side. The resulting degree sum on the outer boundary is \(32\cdot 3^{n-1}-16\).

**Spectral dimension, as a candidate constant, not as a measured input.** The candidate uses

\[
d_s=\frac{2\log 3}{\log 5}=1.365212388972,\qquad \frac{d_s}{2}=\frac{\log 3}{\log 5}=0.682606194486,\qquad \frac{d_s}{2}-1=-0.317393805514.
\]

No fetched paper in §0 states this number. It enters only as the candidate named in the question. The decimation ratio that produces it is 5: linear size doubles, diffusion time multiplies by 5. The carpet has no such locked ratio. A fitted carpet exponent, if one is printed, is a measurement. It is not a target and it is not a factor in any locked cost.

## 3. Prediction (a): every site, fixed tolerance

**Claim A (the volume law).** At \(\varepsilon=1/18\),

| Graph | Heat, exactly | Per site, large-size limit |
|---|---|---|
| Gasket \(G_g\) | \(13N+6\) | 13 |
| Carpet \(C_n\) | \(\tfrac{69}{5}N+\tfrac{16}{5}\,3^n\) | \(69/5=13.8\) |
| Periodic square, degree 4 | \(13N\) | 13 |
| Periodic path, degree 2 | \(15N\) | 15 |
| Open square, side \(n\) | \(13n^2+4n\) | 13 |

Gasket row, the seven heats: \(45, 84, 201, 552, 1605, 4764, 14241\). Per site at \(g=6\): \(14241/1095=13.005479452055\). The excess over 13 is \(6/N\).

Carpet row: \(n=1,2,3,4\) give heats \(120, 912, 7152, 56784\). Per site: \(15, 14.25, 13.96875, 13.86328125\). The excess over 13.8 is \(3.2\,(3/8)^n\).

Open square: sides \(4,8,12,16\) give heats \(224, 864, 1920, 3392\).

**Why the dimension does not appear.** The floor is \(N/\varepsilon-\operatorname{tr}(Q)\), and the trace is \(\alpha N\) plus \(\beta\) times the degree sum. The gasket's degree sum differs from the 4-regular lattice by 6, the three corners. The carpet's limit \(13.8\) differs from the lattice's \(13\) by \(4-3.2=0.8\), the missing bonds in the holes. Both differences are degree sums. Replacing 13 by \(13\cdot d_s/2=8.873880528318\) or by \(13\cdot d_f/2=10.302256254688\) moves the per-site cost by more than 2. The same comparison at the carpet's \(13.8\) is the same kind of miss.

**Gates for (a), all required.** Relative error below \(10^{-9}\) against every displayed heat, on every locked size. At gasket \(g=6\), \(|\mathrm{heat}/N-13|>2\) against either dimension-scaled alternative, and \(|\mathrm{heat}/N-13|<0.01\). At carpet \(n=4\), \(|\mathrm{heat}/N-13.8|<0.01\) and the gap from \(13.8\cdot d_s/2\) and from \(13.8\cdot(\log 8/\log 3)/2\) exceeds 2. Ordinary-least-squares slope of \(\log(\mathrm{heat})\) on \(\log N\), gasket generations \(3\) through \(6\): the closed-form slope on those four heats is \(0.996878303620\). The code's slope on the same four points lies within \(10^{-9}\) of that number. A slope near \(d_f\), \(d_s\), or \(d_s/2\) fails this gate.

## 4. Prediction (b): only the outer boundary

**Lower bounds, exactly, at \(\varepsilon=1/18\).**

Gasket corners, every generation: each corner has \(Q_{bb}=3\), three corners, bound \(3(18-3)=45\). Then

\[
\frac{\mathrm{bound}}{N}=45\,N^{-1}=45\,N^{d_b/d_f-1}.
\]

The coefficient on the right is 45, not a spectral dimension.

Carpet outer boundary: bound \(172\cdot 3^{n-1}-52\). Values: \(120, 464, 1496, 4592\) at \(n=1,2,3,4\). Per named site: \(15, 14.5, 14.384615384615, 14.35\). And

\[
\frac{\mathrm{bound}}{3^n}=\frac{172}{3}-52\cdot 3^{-n},
\]

with \(172/3=57.333333333333\). Since \(3^n=N^{d_b/d_f}\), the ratio \(\mathrm{bound}/N\) is \(\bigl(172/3-52\cdot 3^{-n}\bigr) N^{d_b/d_f-1}\). The power is the boundary count. The prefactor is \(1/\varepsilon\) minus the boundary degrees.

Open square, side \(n\ge 2\): bound \(56n-52\). Values at the locked sides: \(172, 396, 620, 844\). Here \(d_b/d_f=1/2\), and \(\mathrm{bound}/n\to 56\).

**Achieved uniform load, two locked numbers and one tolerance.**

On \(G_0\) the three corners are the whole graph. The uniform load \(\varphi\) solves

\[
\frac{1/3}{1+\varphi}+\frac{2/3}{4+\varphi}=\frac1{18},
\]

so \(\varphi=(13+3\sqrt{33})/2=15.116843969807\) and the achieved cost is \(3\varphi=(39+9\sqrt{33})/2=45.350531909421\). The ratio to the bound is \(1.007789597987\). The code matches this to absolute error \(10^{-9}\) before any larger graph is believed.

On every locked gasket, carpet, and open square, the achieved uniform-load cost \(C\) satisfies \(C\ge\mathrm{bound}\). The tolerance, not a theorem: \(C/\mathrm{bound}<1.15\). The \(G_0\) ratio and the holographic column ratio of about \(13.61/13\) are why 1.15 was chosen. A graph that exceeds 1.15 is a puzzle. The next test is the optimal non-uniform diagonal load on the same sites, which cannot cost more than the uniform load. The scaling gates below use the bound, which does not depend on that load.

**Scaling gates for (b).**

- Gasket: the bound is 45 at all seven generations, so bound\(/N\) at \(g=6\) is \(45/1095=0.041095890411\). The achieved \(C(g)\), if it stays under \(1.15\times 45=51.75\), is \(O(1)\) while the all-site heat is 14241. Slope of \(\log C\) against \(\log N\) on \(g=2,\ldots,6\), if every \(C\) is positive and finite: absolute value below \(0.20\). A volume slope of 1, or a slope \(d_f\) or \(d_s\), misses this gate.
- Carpet: the four bound values are required exactly. On \(n=1,\ldots,4\) the ordinary-least-squares slope of \(\log(\mathrm{bound})\) on \(\log B\) is \(0.988226953947\), not 1, because bound\(/B\) moves from 15 to 14.35. The code reproduces that slope to absolute error \(10^{-9}\). The asymptotic power is still the boundary count: bound\(/B\) stays between 14 and 15. Slope of \(\log(C/N)\) on \(\log N\) for \(n=2,3,4\) lies within \(0.05\) of \(-0.471679166426\), provided the 1.15 tolerance held. The same regression on the bound itself, which does not depend on the load, has slope \(-0.448845678075\) and already lies inside that window. If the tolerance missed, the achieved-cost slope is not scored and the puzzle in the previous paragraph is the record.
- Open square: the four bounds match \(56n-52\). That formula is \(56 N^{-1/2}-52 N^{-1}\), so the leading power is \(d_b/d_f-1=-1/2\) and the second term is still visible on these sides. The ordinary-least-squares slope of \(\log(\mathrm{bound}/N)\) on \(\log N\) for the four locked sides is \(-0.425058011513\), standard error \(0.010972348964\), which is \(0.07494\) away from \(-1/2\). The code reproduces that slope to absolute error \(10^{-9}\). A gate that demanded a slope within \(0.02\) of \(-1/2\) on these four sides would reject the exact bound. It is not the gate.

The exponent \(d_b/d_f-1\) is the exponent of \(B/N\). It is not an extra multiplier on the per-site floor.

## 5. Prediction (c): spectral dimension, aggregate, layers

Three decisions, scored separately. (c0) is an aggregate. (c1) is the counting function of slow modes. (c2) is the layer count.

**(c0) Spatial mean. Exact, every graph in §2, both values of \(\alpha\).** The combinatorial Laplacian kills the constant vector, so \(Q\mathbf 1=\alpha\mathbf 1\). The spatial mean is an Ornstein–Uhlenbeck process of rate \(\alpha\) and variance \(1/(\alpha N)\). Holding it at half its prior variance costs heat \(\alpha\). At \(\alpha=1\) the cost is 1, at every \(N\). The normalized constant mode at error \(1/(2\alpha)\) costs the same 1. A cost that grew like \(N^{d_f/2}\) or \(N^{d_s/2}\) would not be 1. Gate: absolute error below \(10^{-9}\) on the gasket at \(g=0\) and \(g=6\), on the carpet at \(n=1\) and \(n=4\), and on the periodic square at \(n=16\).

**(c1) Slow modes, and the per-site cost.** The heat of holding a set of modes at \(\varepsilon=1/18\) equals the partial sum of \((1/\varepsilon-\lambda_k)\). Gate: on \(G_6\), for the modes with Laplacian eigenvalue in \((0,0.2]\), the partial sum matches that identity to relative error \(10^{-9}\). No factor \(d_s\) or \(d_f\) is inserted.

The counting function is where \(d_s\) can still enter. Let \(\lambda_1(g)\) be the smallest positive Laplacian eigenvalue of \(G_g\). Primary spectral gate, the decimation ratio, not a cost:

\[
\bigl|\lambda_1(g)/\lambda_1(g+1)-5\bigr|\le 0.05\qquad\text{for }g=3,4,5.
\]

Ordinary-least-squares slope of \(\log\lambda_1\) on the generation index, using \(g=3,4,5,6\): within \(0.05\) of \(-\log 5=-1.609437912434\).

Lattice control, same definition of slope, from the closed form \(2-2\cos(2\pi/n)\) at \(n=16,32,64,128\). The four gaps are \(0.152240934977\), \(0.038429439194\), \(0.009630546656\), \(0.002409087590\). The slope of \(\log(\mathrm{gap})\) on \(\log n\) is \(-1.994169933238\), standard error \(0.002137858734\), against the Euclidean target \(-2\), which is the square of the side ratio and is not 5. The code reproduces the slope to absolute error \(10^{-12}\). Doubling a gasket generation is a ratio near 5. Doubling a lattice side is a ratio near 4. Those are different numbers. Neither number multiplies the all-site heat of §3.

Secondary, and not required for the cost claim: on \(G_6\), ordinary-least-squares slope of \(\log\#\{k:0<\lambda_k\le\Lambda\}\) on \(\log\Lambda\) at \(\Lambda\in\{5^{-4},5^{-3},5^{-2},5^{-1}\}\), using only values of \(\Lambda\) whose count is at least 2, and only if at least three such values remain. Target \(0.682606194486\), tolerance \(0.15\). On the periodic square, exact eigenvalue enumeration at sides \(32,64,128\), slope of the cumulative count at \(\Lambda\in\{0.05,0.1,0.2,0.4\}\), target \(1\), tolerance \(0.15\), same minimum-count rule. A miss of this secondary fit is a puzzle. The next test is a larger generation and a window tied to \(\lambda_1\), not a change to §3.

**(c2) Layer count. Two formulas, locked arithmetic, then a spectrum score.**

The equal-variance ladder with rate ratio \(\rho=5\), which is IP12's count and the candidate as stated in the question:

\[
K_U(R)=\Bigl\lfloor\frac{\log R}{\log 5}\Bigr\rfloor+1.
\]

This equilibrium field has variance \(1/a_k\), so the stake at which mode \(k\) stops being blind is \(w=a_k^2\), not \(w=a_k\). A factor 5 in the rate is a factor 25 in the stake:

\[
K_E(R)=\Bigl\lfloor\frac{\log R}{\log 25}\Bigr\rfloor+1.
\]

Locked table. The code checks these integers before it reads a spectrum.

| Stake ratio \(R\) | \(K_U\) | \(K_E\) |
|---|---|---|
| 5 | 2 | 1 |
| 25 | 3 | 2 |
| 125 | 4 | 2 |
| 625 | 5 | 3 |
| 3125 | 6 | 3 |
| 15625 | 7 | 4 |

**Massive field, \(\alpha=1\), generation 6.** Thresholds of modes with Laplacian eigenvalue \(\lambda\) are \((1+\lambda)^2\). From the blind edge \(w=1\) out to \(w=1.44=1.2^2\), the stake ratio is \(1.44\), so \(K_U(1.44)=1\) and \(K_E(1.44)=1\). The Laplacian window those modes occupy is \((0,0.2]\). Let \(n_{\mathrm{bins}}\) be the number of intervals \([5^{-j},5^{-j+1})\) that contain at least one positive Laplacian eigenvalue \(\le 0.2\). Prediction: \(n_{\mathrm{bins}}\ge 3\), and the number of tracked modes \(M=\#\{k:a_k\le 1.2\}\) satisfies \(M\ge 20\). Both layer formulas return 1. They do not count the modes, and they do not count the decimation bins, because \(\alpha=1\) compresses a hierarchy of Laplacian eigenvalues into a narrow band of rates. Gate on the heat of those \(M\) modes: it equals \(\sum(1/18-a_k)\) to relative error \(10^{-9}\), with no \(d_s\) factor. If \(M<20\) or \(n_{\mathrm{bins}}<3\), the compression claim is a puzzle and the next test is to print the full list of eigenvalues below 0.2.

**Small-mass arm, \(\alpha=10^{-8}\), \(\beta=1\), generation 6 only.** Rates \(a=\alpha+\lambda\). Let \(\lambda_{\mathrm{lo}}=\lambda_1\) and \(\lambda_{\mathrm{hi}}=0.2\), and set the stake ratio \(R=(( \alpha+\lambda_{\mathrm{hi}})/(\alpha+\lambda_{\mathrm{lo}}))^2\). Let \(n_{\mathrm{bins}}\) now count nonempty ratio-5 bins that meet \([\lambda_{\mathrm{lo}},\lambda_{\mathrm{hi}}]\). Predictions: \(|n_{\mathrm{bins}}-K_E(R)|\le 2\), and \(K_U(R)-n_{\mathrm{bins}}\ge 2\). The equilibrium square, \(K_E\), is the one that can match the bin count. The unsquared candidate \(K_U\) overshoots. If instead \(|n_{\mathrm{bins}}-K_U|\le 2\) and \(K_E\) misses by 2 or more, the square correction is the puzzle and the next test is to recompute the thresholds with the equal-variance formula on the same eigenvalues, as a comparison column, not as a replacement of this arm. If both miss by more than 2, neither layer formula is the bin count; the next test is to plot \(\log\lambda\) against the decimation index and read the gaps off that plot. The heat of the tracked modes remains the partial sum either way.

## 6. Refutation, and what a miss is

The candidate "the cost scales with \(d_s\) or \(d_f\) rather than with the sites the decision names" is refuted in class F if every gate in §3 and §4 that is marked required comes out as locked, the (c0) cost is 1, and the (c1) partial-sum identity holds. Under those gates the dimension enters only by changing which sites exist and which eigenvalues the Laplacian has. It does not multiply the floor after that count is made. The secondary counting-function slope may still match \(d_s/2\). That match would describe the list of eigenvalues. It would not by itself put \(d_s\) into the heat.

A required gate that misses is a puzzle. The note that reports it names the next test in the paragraph of that gate. It does not apply a pass-or-fail word to the hypothesis sentence, and it does not edit this file. A tolerance that was labelled as a tolerance, and that misses, is the same kind of puzzle.

Labels used when the results are written, and not before: **PROVED** (class F, and the arithmetic checked by the script), **KNOWN** (a fetched statement, not a result of this model), **CONJECTURE** (a reading the gates did not close), **FAILS** (a counterexample among the locked gates), **METAPHOR** (a dimension word that restates a count the cost equation already makes). The all-site floor scaling with \(N\) is the claim expected to be PROVED. The boundary floor scaling with \(B\) is the claim expected to be PROVED as the named-site bound, and METAPHOR if it is called a fractal-dimension law. The unsquared layer count \(K_U\) on this equilibrium field is the claim expected to FAIL on the two arms of §5. Nothing in that list is a result until the script has been run.

## 7. What this lock does not do

It does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not adopt a cost into the master equation. It does not treat a non-Gaussian field, a directed graph, or a continuum diffusion on the gasket. It does not identify the bismuth experiment with this Gaussian cost: the fetched abstract is about electronic modes on a material fractal, and this file is about a heat floor on a graph. The word for the quantity is cost. No other household word is used for it.
