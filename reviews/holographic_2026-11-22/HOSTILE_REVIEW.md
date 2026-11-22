# Hostile review of draft PR #184

**VERDICT: NEEDS-FIXES.**

Independent review of head `11647e85b33098b21cad4bd28c367e9a6d7aa06e` on `holographic-2026-11-22`, one commit on parent `6ca6b452895056372ba5f98f324baf46e196b2bf`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake` build. Computations at nice 19.

The per-site heat floor on this lattice is an identity, and it survives the changes that looked as if they might have forced the volume exponent: odd sides, a mass that shrinks as \(1/n^2\), a fractional symbol, on-site disorder, and an open boundary. A different decision does scale with area. Holding a designated cut to the same per-site tolerance costs a constant per cut site, and that cost does not grow with the depth behind the cut. That is the cost equation on the cut. It is not a bulk stored on a boundary. The headline, read as a claim about bulk per-site error inside the proved class, holds. One sentence marked **PROVED** does not: the sum-loss weight \(a_k v/(a_k+\mu)^2\) is not the learning-rate share. The \(d=3\) side where a 10% cut first beats the surface cap is \(210\), not \(212\). Against current `main` `6340b17`, PR #182 has merged and this branch does not apply.

The hypothesis sentence is one copy in each of `THEORY.md`, `CORE.md`, and `README.md`, the same bytes at head, at the parent, and at `origin/main` `6340b17`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The holographic commit does not change those three files. `git diff 6ca6b45 HEAD` and `git diff origin/main HEAD` are empty on all three.

Recomputation did not import `theory/holographic_checks/`. Scalar heat is the Lyapunov solution of the linear SDE and the Sekimoto expectation \(\mathbb{E}[f^2]/D+\partial_M f\). The path rate is the positive root of \(\gamma^2 P^2=4aD(v-P)\). Lattice eigenvalues are cosines of \(2\pi j/n\), checked against a hand-built path matrix for the open grids. NumPy 1.26.4.

## What holds

**The interface floor, in the class already proved.** For the fast shrunk spring at \(a=v=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), the rational heat is

\[
\frac{800000}{199999}=4.000020000100.
\]

The Lyapunov evaluation of the same SDE is \(4.000020002015\). The gap of \(1.9\times 10^{-9}\) is the linear-solve residual. The conditional variance is \(0.199999999999\), the learning rate is \(4.000000000020\), and the Gaussian stock is \(0.804718956219\). The Riccati path rate is \(999.503125010118\), which is \(249.874532\) times that heat, and the capacity \(L/\mathcal{T}\) prints as \(0.004002\).

The capacity-1 centered spring at \(\nu=9\), \(B=\nu^2/(\nu^2-1)\), has Lyapunov heat \(8\), conditional variance \(0.200000000000\), learning rate \(4\), and stock \(0.804718956217050=\tfrac12\ln 5\). Same stock of the present to \(2\times 10^{-12}\), twice the heat.

The centered spring held at raw error \(0.2\) has closed heat \(5\lambda/(\lambda-4)=5.000020000080\) and conditional variance \(0.166666944444\). The gap from \(4\) is \(1.000020000080\), the raw-coordinate gap \(kT a\) plus the same finite-rate remainder. The telegraph flow at Hamming error \(0.2\) is \(0.831776616672\), the stock is \(0.192744757022\), and the heat at \(\ln\rho=40\) is \(24\). An equilibrium coordinate \(dZ=-\lambda Z\,dt+\sqrt{2\lambda\,\mathrm{Var}}\,dB\) has Sekimoto power \(\lambda-\lambda=0\) at every variance. The entropy gap from variance \(1\) to \(10^6\) is \(\tfrac12\ln(10^6)=6.907755\).

**Per-site heat is exactly proportional to volume on the grids they fit.** For even \(n\) the Brillouin zone contains \(k=\pi\), so \(\lambda_{\max}=\alpha+4d\beta\) does not depend on \(n\). With \(\varepsilon=\tfrac12/\lambda_{\max}\),

\[
\dot Q=V\Big(\frac1\varepsilon-\alpha-2d\beta\Big)
\]

exactly. On all 18 cells the ratio heat\(/V\) is constant up to a relative span of at most \(2.5\times 10^{-16}\). Ordinary least squares then returns slope \(1.000000000000\), standard error at most \(8.091\times 10^{-16}\), and a standard deviation of the 18 slopes of \(1.592\times 10^{-16}\). The cross-section slopes are \(2.000000000000\) and \(1.500000000000\), standard error at most \(1.397\times 10^{-15}\). Those are the note's \(8.1\times 10^{-16}\), \(1.6\times 10^{-16}\), and \(1.4\times 10^{-15}\). They are the residual of an identity. See S2.

On odd sides, where \(\lambda_{\max}=\alpha+2d\beta\,(1+\cos(\pi/n))\) still moves, the same regression is not frozen. For \(d=1\), \(\alpha=\beta=1\), and \(n\in\{9,15,21,31,45,63\}\), heat\(/V\) runs from \(6.758770\) to \(6.995028\) toward the even-grid value \(7\), and the slope is \(1.016062\) with standard error \(4.3\times 10^{-3}\).

Half the prior mean stays extensive past the printed grids. The \(\alpha=\beta=1\) slopes \(1.000676\), \(1.016876\), and \(1.011036\) match the table. Extending \(d=1\) to \(n=1024\), \(d=2\) to \(n=48\), and \(d=3\) to \(n=20\) moves them to \(1.000396\), \(1.015741\), and \(1.008559\). The tracked fraction on the printed \(\alpha=\beta=1\) row starts at \(0.6250\) in \(d=1\).

**The surface cap, where the scan does not skip.** For the open path and the open square, the first side at which a 10% cut of \(\operatorname{tr}(\Sigma)\) exceeds \(A/\alpha\) is the printed one: \(n=44\) (need \(2.007740\), and \(n=43\) still has need \(1.9630<2\)) and \(n=156\) (need \(622.924490\), and \(n=155\) still has need \(614.9937<616\)). The \(d=3\) numbers printed at \(n=212\) are right for that side. They are not the first side. See S1.

Perfect observation of the two ends of the open path \(\alpha=\beta=1\) removes \(1+1/\sqrt{5}=1.447213595500\). At \(n=16\) the difference is \(3\times 10^{-12}\); at \(n=32\) and \(n=64\) it is a unit in the last place. The per-site gap is that constant over \(V\), so the slope \(-1\) is the same flatness.

**The ladder arithmetic that is a ratio.** At \(\rho=2\) and \(\rho=10\), four successive stake ratios on the truncation \(k\in[-80,80]\) equal \(\rho\), and three increment ratios equal \(\rho\). The ratio of weights at \(a=\mu\) and \(a=\mu\rho^2\) is \((\rho^2+1)^2/(4\rho^2)\): \(1.562500\) and \(25.502500\). Per-mode heats at the threshold of mode \(10\), \(\rho=2\), run from \(21.627417\) to \(128\), ratio \(5.918414\). The identification of the weight with the learning-rate share is B1. The ratio does not use that identification.

**Citations that were checked.** Crossref HTTP 200 for every DOI on the page, fetched again this session. Titles, years, venues, and author surnames match the reference list. Maldacena is *Int. J. Theor. Phys.* 38 (1999) 1113–1133. Susskind is *J. Math. Phys.* 36 (1995) 6377–6396. Bousso is *Rev. Mod. Phys.* 74 (2002) 825–874. Glasser, Pancotti, and Cirac are *IEEE Access* 8 (2020) 68169–68182. Eisert, Cramer, and Plenio are *Rev. Mod. Phys.* 82 (2010) 277–306.

The arXiv abstracts support the sentences that use them. Susskind: the two-dimensional description stores one discrete degree of freedom per Planck area, and the three-dimensional world is an image of data on that projection. Bousso: the area of any surface limits the information content of adjacent regions, at \(10^{69}\) bits per square meter. Pastawski, Yoshida, Harlow, and Preskill: an isometry from the bulk Hilbert space to the boundary Hilbert space. Wolf, Verstraete, Hastings, and Cirac: the information in part of a system in thermal equilibrium obeys an area law, and the classical case is included. Evenbly and Vidal: disentanglers and isometries, and scale invariance recovered at criticality. A Crossref query on the title of the 1993 essay returns other papers with similar titles, including Appelquist 1984, and does not return a work record for 't Hooft's essay. The note's statement of that absence is accurate.

The field mutual information on the massive lattice is the area law those abstracts describe, up to a small-grid slope. In \(d=1\), \(I(\mathrm{half};\mathrm{half})=0.157705\) from \(n=16\) through \(n=128\). In \(d=2\), \(I/\mathrm{cut}\) is \(0.032174\) from \(n=12\) through \(n=24\). The slope of \(\log I\) on \(\log(\mathrm{cut})\) for \(n\ge 8\) is \(0.998650\), standard error \(5.6\times 10^{-4}\). The printed slope \(0.922298\) is the fit that still contains \(n=4\).

## The negative result, and the decisions that scale differently

The per-site lower bound is the same identity as H-volume, and it does not use the Laplacian.

Let \(S=(Q+\Phi)^{-1}\) with \(\Phi\succeq 0\), and let site \(b\) have conditional variance \(S_{bb}\le\varepsilon\). For \(M=Q+\Phi\),

\[
S_{bb}=e_b^\top M^{-1}e_b\ge\frac1{e_b^\top M e_b}=\frac1{Q_{bb}+\Phi_{bb}},
\]

so \(\Phi_{bb}\ge 1/\varepsilon-Q_{bb}\). Summing the designated sites and using \(\sum_{b\in B}\Phi_{bb}\le\operatorname{tr}(\Phi)\) gives

\[
L=\operatorname{tr}(\Phi)\ge\sum_{b\in B}\Big(\frac1\varepsilon-Q_{bb}\Big),
\]

whenever \(\varepsilon<1/Q_{bb}\). On the periodic lattice \(Q_{ii}=\alpha+2d\beta\) at every site. For \(B\) the whole cube and \(\varepsilon=\tfrac12/\lambda_{\max}\le 1/\lambda_{\max}\), the bound is \(V(1/\varepsilon-\alpha-2d\beta)\), and \(S=\varepsilon I\) meets it. H-volume is this bound, not a property that appears only after a sweep. Locality, the mass gap, and criticality enter only by changing the diagonal of \(Q\).

That is why the alternatives that were supposed to rig the exponent do not.

- **Critical equilibrium field, still inside G-E.** \(\alpha_n=(2\pi/n)^2>0\). In \(d=1\), heat\(/V\) runs from \(6.038553\) at \(n=32\) to \(6.000602\) at \(n=256\), slope \(0.997098\). In \(d=2\), heat\(/V\) runs from \(12.616850\) at \(n=8\) to \(12.038553\) at \(n=32\), slope \(0.983849\). The leading term remains \(V/\varepsilon\).
- **A surface at that mass does not hold the interior.** Perfect observation of two cut sites on the critical ring removes a fraction \(0.321678\), \(0.318265\), \(0.317409\), \(0.317195\) at \(n=32,64,128,256\). The zero mode's share of the trace is \(0.318636\) down to \(0.317147\). The cut is removing the zero mode. The conditional variance of the deep site grows: \(2.323\), \(4.665\), \(9.339\), \(18.683\). On the massive ring \(\alpha=1\) the same cut removes \(1.200000\) at every size from \(32\) to \(256\), the fraction falls as \(1/n\), and the deep site's conditional variance equals its prior \(0.447214\).
- **Fractional symbol.** \(\lambda(k)=1+(2-2\cos k)^{\gamma/2}\). At \(\gamma=2\) the heat per site is \(7\) and \(I=0.157705\). At \(\gamma=0.5\) the heat per site is \(2.755479\), \(2.751757\), \(2.750442\), \(2.749976\) and the slope in \(n\) is \(0.999066\). The mutual information falls from \(0.038170\) to \(0.027509\). Long-range couplings do not turn the per-site heat into an area.
- **Disorder.** Any on-site masses with mean \(1\), periodic \(d=2\), \(\beta=1\), \(\varepsilon=0.5/9.5\), have heat per site \(1/\varepsilon-5=14\). A uniform draw recentered to mean \(1\) and a linspace with the same mean give the same \(14\) at \(n=4\) and at \(n=16\). The arrangement never enters \(\operatorname{tr}(Q)\).
- **Coarse blocks of fixed length.** Halving the conditional variance of every Fourier mode with wavelength at least \(4\), and leaving the rest blind, costs heat per site \(0.9592\), \(0.9108\), \(0.8869\), \(0.8751\) at \(n=32,64,128,256\). The count of those modes is \(17,33,65,129\). The cost tracks the number of blocks, which tracks the length.
- **Total-error budgets.** On the periodic square, \(\alpha=\beta=1\), \(\varepsilon=\tfrac12/\lambda_{\max}\). A budget \(\varepsilon V\) reproduces the volume floor (\(832\) at \(n=8\), \(13312\) at \(n=32\)). A budget \(\varepsilon A\) with \(A=n\) is heavier than the volume floor: \(8896\) against \(832\) at \(n=8\), and \(584704\) against \(13312\) at \(n=32\). Removing a fixed \(0.5\) from the total variance, which the soft modes can do, costs \(0.721016\), \(0.625771\), \(0.573741\), \(0.544655\) at \(n=16,32,64,128\). That cost stays \(O(1)\). The zero mode alone, already on the page, is the exponent-\(0\) case of the same fact.

**The decision that does scale with area.** Take the same \(\varepsilon=\tfrac12/\lambda_{\max}\) and charge it only on a cut. The bound above is \(|B|(1/\varepsilon-Q_{ii})\). In \(d=2\), \(\alpha=\beta=1\), even \(n\), this is \(13\) per cut site, against a bulk floor of \(13\) per bulk site.

Diagonal loading on one column meets the cut tolerance at a cost per site that has already flattened:

| \(n\) | bulk floor | lower bound | achieved | achieved\(/\)bulk |
|---|---|---|---|---|
| 6 | 468 | 78 | 81.662 | 0.1745 |
| 8 | 832 | 104 | 108.851 | 0.1308 |
| 10 | 1300 | 130 | 136.059 | 0.1047 |
| 12 | 1872 | 156 | 163.270 | 0.0872 |
| 16 | 3328 | 208 | 217.693 | 0.0654 |

The achieved cost per cut site is \(13.6058\) at \(n=16\). The exponent in the cut length is \(1\). The exponent in the volume is \(1/2\).

On a strip that is periodic of length \(8\) and open of width \(W\), the middle row has \(Q_{ii}=5\) for every \(W\) in \(\{4,6,8,12\}\). The lower bound stays \(104\). The achieved cost moves from \(109.374\) to \(108.847\). Depth is not a coordinate of this cost.

This is the row the table does not contain. It is area scaling of the heat, inside the proved class, at the same numerical tolerance the volume sweep uses. It is the cost equation on the sites the decision names. A memory that only has to hold what sits on the cut does not pay for the cube behind it, and the same memory does not buy a per-site gap in that cube: H-surface, the cap \(A/\alpha\), and the critical cut above all say so. Calling the cut holographic predicts a bulk encoding the cost does not have. The page already files a boundary channel \(A/\sigma^2\) as **METAPHOR**. It does not compute this bound, and the closing sentence of §5 is easy to read as if area scaling had been looked for and had failed.

## Required fixes

**B1. The sum-loss weight is not the learning-rate share.** Proposition H-share says:

> The modal share of the learning rate is \(a_k v/(a_k+\mu)^2\). At \(a=\mu\) and at \(a=\mu\rho^2\),
>
> \(\mathrm{share}(\mu)/\mathrm{share}(\mu\rho^2)=(\rho^2+1)^2/(4\rho^2)\).
>
> This equals \(1.562500\) at \(\rho=2\) and \(25.502500\) at \(\rho=10\).

G-sum in `theory/INFO_PHYSICS_GENERAL.md` sets \(g_k=1/(a_k+\mu)\) and \(\sigma^2=\sum a_k v_k g_k^2/\mu\), and the learning rate of the channel is \(\sum a_k v_k g_k^2/\sigma^2=\mu\). The summand of that learning rate is

\[
\frac{a_k v_k}{(a_k+\mu)^2\sigma^2}.
\]

On the truncation \(k\in[-80,80]\) at \((\rho,\mu)=(2,4)\), the weights \(a v/(a+\mu)^2\) sum to \(0.360674\), not to \(\mu=4\). Dividing by \(\sigma^2=0.090168\) makes them sum to \(4\). At \((10,10)\) the weights sum to \(0.043711\), \(\sigma^2=0.004371\), and the shares sum to \(10\). The ratio of two weights equals the ratio of two shares, so \(1.562500\) and \(25.502500\) stay, and a flat profile would still be \(1\). The **PROVED** sentence that equates the weight with the share does not.

Replace the identification with the share \(a_k v_k g_k^2/\sigma^2\). Say that the printed ratio is the ratio of those shares, and that the checks compare the weights. Leave the two printed values.

**S1. In \(d=3\) the cap fails at side \(210\).** The note says the bound first fails

> at \(n=212\) in \(d=3\) with \(\beta=0.5\) (cap \(267128\), need \(269747.52\), \(V=9528128\)).

The scan in the checks steps by \(4\) once \(d=3\). Every integer from \(200\) was recomputed. Side \(209\) still fits under the cap. Side \(210\) does not: need \(262195.96\), cap \(262088\), \(A=262088\), \(V=9261000\). Side \(211\) also fails. The printed triple at \(n=212\) is the right triple for \(n=212\). It is the first multiple of \(4\), not the first side. The same scan confirms \(n=44\) and \(n=156\) as the first sides in \(d=1\) and \(d=2\).

Write \(n=210\) as the first \(d=3\) side, and keep \(n=212\) only if the sentence says it is the first multiple of \(4\). The same integer is in the PR body and in the T41 row.

**S2. The twelve nines are roundoff on even grids.** Section 3, the PR body, and T41 lead with

> The exponent in the volume is \(1.000000000000\) (ordinary-least-squares standard error at most \(8.1\times 10^{-16}\) across 18 cells).

H-volume already proves the exponent is \(1\). On these 18 cells \(n\) is even, \(\lambda_{\max}\) is constant, and heat\(/V\) does not move, so a regression cannot return another slope. The odd-side slope \(1.016062\) is what the same regression does when \(\varepsilon\) is allowed to depend on \(n\). Say that the sweep is the trace identity on even grids, that the standard error is roundoff, and, if a regression is kept, give one odd-side fit beside it.

**S3. Put the cut on the table.** Section 5 ends with:

> No row is a holographic prediction that is both extra and true.

The cut at fixed per-site tolerance is an area law for the heat, exponent \(1\) in the cut and \(1/2\) in the volume on the squares above, and it does not grow with depth on the strip. The boundary-channel sentence in §3 files the phenomenon as **METAPHOR** and does not give this bound or these numbers. Add a row: minimum heat at fixed per-site error on a designated cut scales with the cut; the cost equation gives at least \(|B|(1/\varepsilon-Q_{ii})\), met here to about \(13.61\) against \(13\); the bulk per-site floor on the same \(\varepsilon\) scales with the volume; the name is **METAPHOR**. State next to it that a mass \(\alpha=(2\pi/n)^2\), a fractional symbol, a fixed block length, and an area-sized total-error budget do not turn the bulk per-site floor into an area. The first of those still has exponent \(1\). The last is heavier than the volume floor.

The headline can stay, as a statement about bulk per-site error and about names that add a prediction. It should not be readable as "area scaling of the heat was absent."

**S4. PR #182 has merged, and this branch does not apply onto current main.** The note says:

> Draft PR #182, branch `general-form-physics-2026-11-22`, is a consolidation of the same heat floor. It is open and under fix. This note does not edit that branch and does not use its OPEN_WORK id.

`main` at `6340b177bae94074d90bdbb3a2bfaad0e4915d90` contains the merge `df9fc05` and the confirm. T40 is the adoption item, and it is not applied. A merge-tree of `11647e85` with that main has one conflict, in `OPEN_WORK.md`: both sides added a row after T39. T41's sentence that #182 "uses T40 on its own branch" describes the branch as it was before the merge.

Rebase onto `6340b17`. Keep T40. Place T41 after it. Replace "open and under fix" with the merge. This note still does not adopt the proposal and still does not edit `THEORY.md`.

## Nits

**N1.** "The tracked fraction stays a positive density (at least \(0.63\) on these grids)." On the \(\alpha=\beta=1\) grids the smallest fraction is \(0.6250\), the first \(d=1\) point. Write \(0.625\).

**N2.** The shared stock is printed as \(I=0.804718956217\). That is \(\tfrac12\ln 5\), the value at conditional variance \(0.2\). The shrunk spring at rate \(10^6\) has stock \(0.804718956219\). The capacity-1 spring has the printed value. The two differ by \(2\times 10^{-12}\).

**N3.** The \(d=2\) mutual-information slope \(0.922298\) (standard error \(0.02994\), six sizes) is pulled by \(n=4\). From \(n=8\) through \(n=24\) the slope is \(0.998650\) and \(I/\mathrm{cut}\) stays \(0.032174\). The area law is in better shape than the six-point fit. Say which sizes enter the slope.

**N4.** The open-path removal \(1.447214\) is \(1+1/\sqrt{5}\). From \(n=32\) the printed digits are that constant.

**N5.** The disordered-mass sweep draws \(\alpha_i\) and then uses only their mean. Heat per site is \(14\) for every arrangement with that mean. The sentence that disorder does not turn the floor into an area is the trace identity. Say that the draw does not enter the heat.

**N6.** Two checks cannot fail. The equilibrium-bulk loop sets `heat_z = 0.0` and then requires `heat_z == 0.0`. The sum-loss degree loop sets `degree = 1` and then requires `degree == 1`. The entropy half of the first check is a real evaluation, and the degree claim is IP13. The heat half and the degree half are assignments. Either compute the Sekimoto power and the rank of \(\Phi\), or label the lines as restatements.

**N7.** Maldacena, Ryu and Takayanagi, Almheiri, Dong, and Harlow, Hayden, Nezami, Qi, Thomas, Walter, and Yang, and Eisert, Cramer, and Plenio are resolved and unused in the argument. Drop them or give each a sentence.

## Labels and scope

H-iface, H-volume, H-surface, and H-octave match the recomputation and the proofs they cite. The zero mode at heat \(1\), independent of volume, is the exponent \(0\) the page claims. The field area law is **KNOWN**, and Wolf, Verstraete, Hastings, and Cirac do include the classical thermal case the Gaussian field sits in. The numerical check is an instance. **FAILS** for bulk memory capped by the flow, for equal heat per octave, and for a MERA degree on the sum loss, matches the path rate, the factor \(\rho\), and IP13. **METAPHOR** for the interface name, for a boundary channel, and for a logarithmic count that was not produced by a coarse-graining map, matches what those names add.

H-share is the label that does not hold as written. B1 is that repair. "Nothing here is a conjecture" is compatible with the proved propositions once B1 is fixed. The half-prior slopes are a finite-grid fit; N1 is the only over-tight digit in that paragraph, and the extended grids stay extensive.

The commit does not edit `THEORY.md`, `CORE.md`, or `README.md`. It does not adopt \(J_{\mathrm{phys}}\). It does not close IP14. It does not rerun T20 or the keystone check. Misses are labeled **FAILS** or **METAPHOR**. The cost is called a cost. T41 is the right next id once T40 is on the page. This branch's `OPEN_WORK.md` has no T40 row, and it still describes #182 as open. S4 is that rebase.

## Checks run

On `11647e85`, at nice 19:

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/holographic_checks/holographic_checks.py` | 142 checks, FAILS 0 |
| `tools/check_consistency.py` | RESULT: PASS (392 claim-map rows; the length warnings on THEORY and README are the pre-existing advisory) |
| `tools/check_open_work.py` | RESULT: PASS |
| `nice -n 19 python3 -m pytest -q tools` | 255 passed, 1 skipped, 310.63 s |

The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed". No `lake` build. Pytest 9.2.0, SciPy 1.18.1, SymPy 1.14, NumPy 1.26.4, installed for this run.

The official script reproduces the note's printed heats, stocks, caps, and slopes, including the open-cube fits. The independent code reproduces the scalar heats and stocks, the 18 even-grid slopes, the half-prior slopes, the \(d=1\) and \(d=2\) caps, the ladder ratios, the mutual informations, and the disordered trace. It disagrees with the note in the two places under repair: the first \(d=3\) side, and the object H-share calls a share. The cut, the critical ring, the fractional symbol, and the total-error budgets are not in the note's script. They are the numbers above.

VERDICT: NEEDS-FIXES
