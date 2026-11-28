# Independent hostile review: PR #153 (chain-to-diffusion and three-mode convexity)

**Reviewer:** independent. Wrote none of the notes, the solvers, the claim-map rows, or the pointer edits. The only file added by this review is this one.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/153
**Head reviewed:** `3c597203b9e0912d7177b4beca590ed58910168d` on `diffusion-convexity-2026-11-21`, base `d1a6de448bbaca2e2e0f18d4dc2ce9c3972308a5` (`main`, merge of PR #150). Draft. Not merged.

**Verdict: NOT-READY**

N67 is a real theorem, and N68 is honestly open. N66's static Gibbs bound and the Brownian defect identity are real. The passage that the claim map stamps **PROVED (in-model)** is not closed on the page. Theorem CD2, as displayed, is false. Theorem CD4, as displayed, is false. The \(O(\delta^2)\) argument cites the false bound and does not prove the uniform moment it uses. Ornstein–Uhlenbeck, constant velocity, and a non-diagonal Hessian are sketches inside a proved label.

## Blockers

1. `theory/CHAIN_DIFFUSION.md:108`–`:112`, copied into the why-cell at `measurement/CLAIM_MAP_v2.md:481`. Theorem CD2 says that on \(|Nx_\pm|\le 1\),

   \[
   |R(L)|\le C_N D_m(\beta h\delta)^2\bigl(1+(\beta h)L^2\bigr)\bigl(1+L^2\bigr)
   \]

   for a constant \(C_N\) that depends only on \(N\).

   No such \(C_N\) exists. At \(L=0\) the linear Moran map produces \(R=-a\delta^2/2\) with \(a=D_m\beta h\), so \(|R|=\tfrac12 D_m\beta h\delta^2\). The displayed shape at \(L=0\) is \(C_N D_m(\beta h\delta)^2\). The ratio is \(1/(2 C_N\beta h)\). At \(N=5\), \(\beta=10^{-4}\), \(h=0.1\), \(D_m=1\), \(\delta=0.02\), one has \(|Nz|=2.5\times 10^{-9}\le 1\) and the inequality already demands \(C_N\ge 5\times 10^4\). Shrinking \(\beta h\) raises the required constant without bound. The Cauchy lemma on \(f-f_{\mathrm{lin}}\) does not see this term: it is present when \(f\) is replaced by \(f_{\mathrm{lin}}\).

   CD3 (`:126`–`:136`) chooses \(\eta\) from this bound. That choice is not available until the constant is allowed to depend on \(\beta\) and \(h\), and until the resulting estimate is actually derived. The lemma is not that derivation.

2. `theory/CHAIN_DIFFUSION.md:134`–`:136` and `:118`–`:121`. For each fixed small \(\delta\), with \(D>0\), a stationary law exists and is unique. Off the bulk the restoring speed is at least \((D_m/\delta)(1-e^{-\eta/2})\), so \(G(L^2)\le -v_{\mathrm{rest}}|L|+C_1\) outside a finite interval, and the Brownian piece is strong Feller and irreducible on \(\mathbb{R}\). That half of Foster–Lyapunov does not use CD2.

   The \(O(\delta^2)\) theorem needs a moment bound that stays finite as \(\delta\to 0\), because the bulk grows like \(1/\delta\). The note's entire argument for that is the sentence that the same drift beats \(\cosh(\lambda L)\) and therefore \(\mathbb{E}[\cosh(\lambda L)]\le M\) uniformly in small \(\delta\). The negative speed of size \(1/\delta\) starts only at \(L_B=\eta/(\beta h\delta)\), which leaves the window. Inside that window the chain has to be shown close to the Langevin drift, uniformly in small \(\delta\), before the exponential moment is uniform. That comparison is not written. Identity (I) then gives an \(O(\delta^2)\) excess only after \(\mathbb{E}[R]=O(\delta^2)\). The order is measured below. It is not proved.

3. `theory/CHAIN_DIFFUSION.md:152` and `:158`–`:159`. Theorem CD4 says the lag converges weakly in Skorokhod space for any tight sequence of initial laws with a uniform second moment. Tightness of the initials is the wrong hypothesis for convergence. The sequence that alternates between a point mass at \(0\) and a point mass at \(1\) is tight and has a uniform second moment, and the path laws alternate between two different Langevin laws. Convergence needs the initial laws themselves to converge.

   The generator input is also mis-cited. CD2 bounds the defect of the single test function \(L^2\). Corollary 8.7 needs \(\|G_\delta f-\mathcal{L}f\|_\infty\to 0\) for every \(f\) in a core. On \(C_c^\infty\) that limit is true by Taylor expansion of the jumps, because both generators vanish outside a fixed neighbourhood of the support, which is what the stopped form of the corollary uses. The note does not give that expansion. Compact containment (`:159`) is the same unproved uniform Lyapunov, integrated up to time \(T\).

   The citation itself points at the right place. Chapter 4 of Ethier and Kurtz is *Generators and Markov Processes*. Theorem 8.2 and Corollary 8.7 of §8 are the generator-convergence theorems for cadlag paths; the proof of Corollary 8.7 stops the martingale and calls Theorem 8.2(c), and "Theorem 4.8.2" is the same statement. Well-posedness of the linear Lipschitz martingale problem (`:160`) is the right third input. The three names are the right names. The note does not check the three hypotheses it lists.

4. `theory/CHAIN_DIFFUSION.md:144`–`:148` and `theory/DRIFT_SELECTION.md:62`, and the same three centres in `measurement/CLAIM_MAP_v2.md:481` and in the v2.77 note at `:86`. Brownian motion in one coordinate is the case with a written identity. For an Ornstein–Uhlenbeck centre the state is the pair \((L,\theta^\star)\). The world's piece of the generator is exact. The jump piece also defects the cross moment \(L\theta^\star\), by \(\delta(r_+-r_-)+a L\) times \(\theta^\star\). That defect is \(O(\delta^2)\) on the same bulk where the expansion of \(\varphi\) is valid, and it is a different function from \(R(L)\). The sentence "the only defect is the same \(R(L)\)" does not cover it. Constant velocity and a non-diagonal \(H\) are one paragraph each, both of which call CD2. The checker never leaves a Brownian centre. Those three extensions belong in the open list, or the estimates have to be written, before the row can stay **PROVED (in-model)** for every centre the row names.

## Should-fixes

1. `theory/CHAIN_DIFFUSION.md:106`. Substituting the linear map \(f_{\mathrm{lin}}(z)=1-((N-1)/(2N))z\) leaves \(R=-a\delta^2/2\), independent of \(L\). Checked by direct expansion and by evaluating the generator: at \(N=2\), \(\beta=h=D_m=1\), \(\delta=0.1\), the linear-map defect is \(-5\times 10^{-3}\), which is \(-a\delta^2/2\). The quadratic coefficient in the lemma is right, \(f''(0)/2=(N-1)(N-2)/(12N^2)\), and on \([-1,1]\) the remainder bound \(\tfrac1{12}z^2+3.4|z|^3\) holds (the ratio stays below \(0.96\) for \(N\le 100\)). \(|f|<3.4\) on \(|z|=2\) holds as well (the maximum found is \(2.30\) at \(N=100\); the minimum of \(|\sinh|\) on the unit circle is \(\sin 1\)). The false sentence is the one that says this linear piece produces the Langevin generator with no remainder.

2. `theory/CHAIN_DIFFUSION.md:112`. From \(|\varphi|\le 1\) the tail estimate is \(|R|\le (2ND_m/\delta)|L|+2ND_m+2aL^2+2D_m\). The displayed factor \(h\) in the first term is not in that estimate. A log sweep in \(L\) up to \(10^8\), for \(h\in\{10^{-3},10^{-2}\}\), \(N\in\{2,5,20\}\) and \(\delta\in\{0.05,0.2,1\}\), kept \(|R|\) under the displayed bound (the largest ratio was \(0.999998\)). The \(O(\delta^2)\) tail only needs some multiple of \(|L|/\delta\) times an exponential moment. Replace the display with the estimate the sentence actually proves.

3. `theory/DRIFT_SELECTION.md:64`. Section 0 of the new note keeps the two limits apart, and does it honestly. Weak mutation is \(N\mu_{\mathrm{gen}}\to 0\) in generation time, assumed and not proved (`theory/CHAIN_DIFFUSION.md:9`). The diffusion limit is \(\delta\to 0\) in chain time with \(\beta\), \(D_m\) and \(D/D_m\) fixed, which sends the chain's \(\mu=2d D_m/\delta^2\) to infinity (`:10`–`:16`). A generation is a different clock from a substitution. The new sentence in the drift note says the diffusion limit is "lattice steps compared with the scatter." That is the geometric ratio \(\delta^2/\mathrm{Var}(L)\), which the same note at `:62` has already separated from \(\varepsilon_{\mathrm{lat}}\). Point the sentence at the fitness step.

4. `tools/chain_diffusion_checks.py:162`–`:166`. The static assertion is `gap <= bound * (1+1e-9) + 1e-14`. At \(a=0.4\), \(\beta=2.5\), the logged gap is \(5.551\times 10^{-17}\) and the logged bound is \(2.923\times 10^{-20}\), and the assertion still passes. High precision (mpmath, 50 decimals) gives a positive gap below the bound: at \(a=0.4\), \(\beta=1\), the gap equals \((4\pi^2/(\beta a))\rho = 3.65364287977\times 10^{-20}\), and the displayed bound is twice the leading term. The float rows with \(a\le 0.4\) do not test CD1. The row \(a=2.025>1\) is outside the hypothesis \(a_k\le 1\); the bound happens to hold there too. The rows that the float sum can see (\(a=0.81\), \(a=0.9\), \(a=2.025\)) match the leading term.

5. `theory/MODEL_S_J3.md:25`. Continuity of \(E_\infty\) is true for each fixed \(a_3\), by dominated convergence. The parenthetical dominate is not. No single Ornstein–Uhlenbeck spectrum of variance \(v_1+v_2+1\) sits above the sum of the spectra at rates \(1\), \(100\), \(10000\) with unit variances, at both \(\omega=0\) and \(\omega=10^4\). The spectrum at third-mode variance \(1\), with \(a_3\) held fixed, is an integrable dominate. The constant \(\sum_j v_j/a_j\) in the \(E_1\) localisation (`:27`) blows up as \(a_3\to 0\), which is why the modulus depends on the third rate.

6. `theory/MODEL_S_J3.md:37`–`:39`, `theory/LAYER_CONVEXITY.md:91`, and `measurement/CLAIM_MAP_v2.md:483`. The screen is 96 worlds, the minimum relative slack is \(3.2680601715354446\times 10^{-9}\), and there is no negative. Re-running `--full` reproduced the stored rows exactly. N68 is labelled **OPEN**, and the note says the screen is not a proof. That label is right.

   The figure \(3.3\times 10^{-9}\) is the wrong scale for "how close." It is world 83: rates about \(0.0067\), \(0.011\), \(0.050\), variances about \(7.68\), \(0.012\), \(0.036\), noise \(0.0067\). One mode carries the cost. \(E_0=7.723\), and \(E_1\), \(E_2\), \(E_\infty\) agree at \(0.02672344\). The second difference that realises the minimum is \(E_1-2E_2+E_\infty=2.524\times 10^{-8}\), and \(d_3/d_2\approx 0\). A one-store design has already reached the causal floor; the decrements after \(K=0\) are small against \(E_0\). An independent Yovits–Jackson quadrature of that world sits \(6.7\times 10^{-10}\) under the spectral-factor value, which moves the second difference by much less than its size.

   The closest stored decrement ratio is world 45, \(d_3/d_2=0.885\). A finer two-store optimisation (grid 60, 20 Nelder–Mead starts, no clipping) brings that ratio to \(0.023\), with second difference \(1.10\times 10^{-4}\). The spectral-factor \(E_\infty\) is \(4.7\times 10^{-8}\) above the quadrature. The grid was pessimistic, in the direction the note claims for \(d_2\ge d_3\). State the minimiser as an almost one-mode world, and quote a decrement ratio, so \(3.3\times 10^{-9}\) is read as a normalisation.

7. `tools/chain_diffusion_checks.py:207` and `tools/model_s_j3_checks.py:147`–`:148`. The identity check evaluates both sides on one density. It tests whether that density is stationary for \(L^2\). The comparison of the same excess to the closed form \(\frac1{2\beta}(1+D/D_m)\) is the check of the limit formula. Say so in the docstring. In the three-mode curve, clipping \(E_2\) into \([E_\infty,E_1]\) can manufacture a monotone triple. On world 83 the unclipped values match the stored ones, so this run did not use the clip to change the sign. A high grid value of \(E_2\) inflates \(E_0-2E_1+E_2\). The certificate the note describes is one-sided for \(E_1-2E_2+E_\infty\) only.

## Per-claim table

| Claim | Rating |
|---|---|
| N66, static chain exactly Gibbs, excess below \(d/(2\beta)\) by at most \(\sum_k 8\pi^2/(\beta a_k)\exp(-2\pi^2/a_k)\) when each \(a_k\le 1\) | **FAITHFUL** |
| N66, Brownian identity \(\mathbb{E}[J]-\mathrm{DS1}=\mathbb{E}[R]/(4 D_m\beta)\) on \(L^2\) | **FAITHFUL** |
| N66, CD2 display: \(C_N\) depends only on \(N\), and that bound is what the Cauchy lemma gives | **WRONG** |
| N66, Foster–Lyapunov: one stationary law for each small \(\delta\), when \(D>0\) | **FAITHFUL** |
| N66, uniform exponential moments as \(\delta\to 0\) | **WEAKER** |
| N66, Brownian stationary excess equals DS1 plus \(O(\delta^2)\) | **WEAKER** |
| N66, the same \(O(\delta^2)\) for an Ornstein–Uhlenbeck centre, constant velocity, or a non-diagonal Hessian | **WEAKER** |
| N66, path measures converge by Ethier–Kurtz Chapter 4 §8, Theorem 8.2 and Corollary 8.7, under the hypotheses the note lists | **WEAKER** |
| N66, weak mutation and the lattice limit kept as two clocks | **FAITHFUL** |
| N67, a nondegenerate two-mode world stays convex for a third mode of any fixed rate, once the variance is small enough, and the smallness depends on that rate | **FAITHFUL** |
| N68, labelled open; halving stays a separate open condition and already fails on a convex low-SNR curve | **FAITHFUL** |
| N68, 96-world screen, minimum relative slack \(3.3\times 10^{-9}\), read as the margin by which convexity almost failed | **WEAKER** |

## What was checked and holds

**CD1.** Detailed balance is \(\varphi(x)/\varphi(-x)=e^{-(N-1)x}\). With symmetric proposals the stationary weight is \(e^{-\beta J}\), and the quadratic weight is summable, so the stationary law is unique. Poisson summation was recomputed at 50 decimals for \(a\in\{0.4,0.81,1,2.025\}\). The gap equals \((4\pi^2/(\beta a))\rho\) with the note's \(\rho\), it is positive, and it sits under \((8\pi^2/(\beta a))q\). The lattice excess sits below \(1/(2\beta)\). The factor \(8\) is twice the leading term, which is what the estimate \(1+8q^3\le 2\) produces. At \(a=0.81\), \(\beta=1\), gap and leading term agree at \(1.271690882\times 10^{-9}\).

**Identity (I).** For \(J-J^\star=\tfrac12 h L^2\) and \(a=D_m\beta h\), stationarity of \(L^2\) rearranges to the displayed factor \(1/(4 D_m\beta)\). An independent grid (spacing \(\delta/4\), \(12\) standard deviations, normalisation on a central row) reproduced the author's excesses: \(1.034662\) against the stored \(1.034670\) at \(N=20\), \(\delta=0.5\), and relative error over \(\varepsilon_{\mathrm{lat}}\) equal to \(0.0943\) at \(N=5\), \(\delta=0.25\), which is the stored maximum \(0.094\). On that grid the identity residual matches the excess gap on every row, including \(h=0.2\) and \(\beta=0.2\). Across \(\delta\in\{0.50,0.25,0.18\}\) at \(N=20\), \(D/D_m=1\), the ratio stays \(0.069\). The chain sits above the diffusion value. These runs measure a finite \(C\) for this Brownian family. They are the content of the numerical section, and the note already says they are not a substitute for CD3.

**N67.** Degree 2 gives \(E_K=E_\infty\) for \(K\ge 2\) and a strict gap \(E_1>E_\infty\). Theorem S2 gives \(\gamma=E_0-2E_1+E_\infty>0\). For a fixed third rate, \(E_0\) jumps by \(v_3\), and \(E_\infty\), \(E_1\), and \(E_2\) are continuous at \(v_3=0\) by the argument on `:25`–`:29` once the dominate is corrected as above. The two-mode gaps are strict, so they stay ordered for small \(v_3\), and \(d_k=0\) for \(k\ge 4\). The threshold is allowed to depend on \(a_3\). It is not a number computed in the note. On the worked world \((a,v,N)=((1,30),(1,0.4),0.1)\), convexity survived for \(v_3\) up to \(1\) at third rates from \(10^{-4}\) to \(10^6\). On a near-degenerate pair of rates \(1\) and \(1.05\), it survived for \(v_3\) up to \(0.5\) at third rates from \(10^{-6}\) to \(10^6\). Those runs are consistent with "small enough" being allowed to be large. They do not evaluate \(v^\star\).

**N68 and halving.** The open sentence is the general statement. The low-SNR halving miss remains the four-mode example in `theory/LAYER_CONVEXITY.md` §6 (ratio \(0.634\), convex). The new checker records a three-mode ratio and does not claim that draw as the miss.

**Scope.** The Part 2 hypothesis sentence is byte-identical to `d1a6de4`, one copy each, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.` The diff of `THEORY.md` and `README.md` against that base is the claim-map pointer v2.76 to v2.77. `CORE.md` and `theory/SELECTION_AXIOMS.md` are unchanged. Neither new note restates the sentence. The word does not appear as a name for N66, N67, or N68.

## Commands

All of these were run from the repo root at nice 19, on head `3c59720`. NumPy 2.5.5, SciPy 1.18.1, mpmath 1.4.1. `lake build` was not run.

- `python3 tools/chain_diffusion_checks.py --full`. `64 checks, 0 failed`. The rewritten `results_full.json` matched the stored file; it was restored.
- `python3 tools/model_s_j3_checks.py --full`. `n=96`, `min_rel=3.2680601715354446e-09`, `negatives=0`, row-for-row equal to the stored JSON; restored.
- `python3 -m pytest -q tools/test_chain_diffusion_checks.py tools/test_model_s_j3_checks.py`. `2 passed`. The suite of 247 was not rerun.
- Independent mpmath and grid scripts, not imported from `tools/chain_diffusion_checks.py` for the Poisson sum, the Cauchy circle, the linear-map defect, or the stationary solve. The three-mode recomputes called `tools/model_s_j3_checks.py` for the Gram matrix and then compared \(E_\infty\) with a separate Yovits–Jackson quadrature.
