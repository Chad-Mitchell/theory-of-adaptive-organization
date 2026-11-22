# Model S convexity for three or more modes

*Sunday 22 November 2026. Branch `diffusion-convexity-2026-11-21`, draft PR. Written by one executor for Chad Mitchell; a self-check, not an independent review. Takes up the case `theory/LAYER_CONVEXITY.md` §6 left open: convexity of \(\varepsilon_K\) for Model S at lead 0 with three or more OU modes. It does not change the Part 2 hypothesis sentence, and it does not edit a locked preregistration or hash file.*

## 0. Bottom line

**The general statement stays open.** For a Model S world with three or more distinct rates, at lead 0, convexity of \(\varepsilon_K=E_K/E_\infty-1\) is not proved, and no counterexample was found. A certified screen is below.

**A subclass is proved.** A nondegenerate two-mode world stays convex when a third mode of any fixed rate is added with small enough variance (Theorem S3). The threshold depends on the two-mode gap and on the third rate. It is not uniform in that rate, and it does not cover a third mode of comparable size. Halving, \(\varepsilon_{K+1}\le\varepsilon_K/2\), stays open and is already known to fail on a convex curve (`theory/LAYER_CONVEXITY.md` §6).

Counting modes that share a rate does not enlarge the subclass. Two components at the same rate are one OU mode, and Theorem S2 already covers every world of McMillan degree at most 2.

## 1. Theorem S3

Model S at lead 0 is the one in `theory/LAYER_CONVEXITY.md` §4: a sum of OU modes, rates \(a_j>0\), variances \(v_j>0\), seen in white noise of density \(N>0\). \(E_K\) is the best causal \(K\)-store mean squared error, and \(E_J=E_\infty\).

**Theorem S3 (PROVED in-model; lead 0).** Let \(0<a_1<a_2\) and \(v_1,v_2,N>0\), and write \(E_K^{(2)}\) for that two-mode world. Then \(E_1^{(2)}<(E_0^{(2)}+E_\infty^{(2)})/2\) and \(E_1^{(2)}>E_\infty^{(2)}\). For every \(a_3>0\) there exists \(v^\star>0\) such that if \(0<v_3<v^\star\), the three-mode world \((a_1,a_2,a_3)\), \((v_1,v_2,v_3)\) has non-increasing decrements of \(E_K\), hence of \(\varepsilon_K\), on \(K\ge 0\).

*Proof.* Degree 2 forces \(E_K^{(2)}=E_\infty^{(2)}\) for every \(K\ge 2\), and a one-store design has degree 1, so \(E_1^{(2)}>E_\infty^{(2)}\) (the strict degree gap of L2). Theorem S2 gives the other inequality, so both
\[
\gamma=E_0^{(2)}-2E_1^{(2)}+E_\infty^{(2)}>0,\qquad d_2^{(2)}=E_1^{(2)}-E_\infty^{(2)}>0.
\]
Let \(E_K(v_3)\) be the errors after the third mode is added, and write \(E_\infty(v_3)\) for the causal minimum. For \(K\ge 3\), \(E_K=E_\infty\).

**\(E_0\) and \(E_\infty\) are continuous at \(v_3=0\).** The blind error increases by \(v_3\). The spectrum increases by \(2 a_3 v_3/(a_3^2+\omega^2)\). The Yovits–Jackson integrand \(\log(1+S/N)\) is continuous and, on \(0\le v_3\le 1\), dominated by an integrable function (the one-mode integral at variance \(v_1+v_2+1\)). So \(E_\infty(v_3)\to E_\infty^{(2)}\).

**\(E_1\) is continuous at \(v_3=0\).** Let \(g(b,v_3)\) be the mean squared error of the best gain at a single rate \(b>0\). The Gram matrix is positive definite for \(N>0\), and \(g\) is continuous on \((0,\infty)\times[0,1]\). The captured variance tends to 0 as \(b\to 0\) and as \(b\to\infty\), uniformly for \(v_3\le 1\): as \(b\to\infty\) the noise term is \(Nb/2\) while the cross term stays bounded by the total variance, and as \(b\to 0\) both the cross term and the signal Gram entry are \(O(b)\) with a constant \(\sum_j v_j/a_j\) that is bounded for \(v_3\le 1\) at fixed \(a_3\). The two-mode world captures a positive amount \(G>0\) at an interior rate. Hence there is a compact interval of rates on which, for every small \(v_3\), every near-optimal rate must lie, and outside which the captured variance is less than \(G/2\). The minimum of a continuous function over that compact is continuous in \(v_3\). So \(E_1(v_3)\to E_1^{(2)}\).

**\(E_2\) is continuous at \(v_3=0\).** The two spectral-factor rates of the two-mode world, with gains reoptimised, have error continuous in \(v_3\) and equal to \(E_\infty^{(2)}\) at \(v_3=0\). The optimal two-store error is at most that, so \(\limsup E_2(v_3)\le E_\infty^{(2)}\). And \(E_2(v_3)\ge E_\infty(v_3)\to E_\infty^{(2)}\), so \(E_2(v_3)\to E_\infty^{(2)}=E_2^{(2)}\).

The decrements therefore satisfy \(d_1(v_3)\to d_1^{(2)}\), \(d_2(v_3)\to d_2^{(2)}>0\), and \(d_3(v_3)=E_2(v_3)-E_\infty(v_3)\to 0\), while \(d_k=0\) for \(k\ge 4\). The two-mode gap \(\gamma=d_1^{(2)}-d_2^{(2)}\) is positive, so for small \(v_3\) one has \(d_1\ge d_2\ge d_3\ge 0\). ∎

The same continuity shows that the set of \((a,v,N)\) with a strict convexity gap is open. It does not show that the set is everything: a third mode of size comparable to the first two is not a small perturbation, and the proof gives no number \(v^\star\) one can evaluate without a modulus of continuity.

## 2. No counterexample on the screen

`tools/model_s_j3_checks.py`. \(E_\infty\) is the error at the spectral-factor rates (Lemma P). \(E_1\) is a fine one-dimensional minimum. \(E_2\) from a log-rate grid is an upper bound on the true two-store error. Raising \(E_2\) lowers the second difference \(E_1-2E_2+E_\infty\). A positive value is therefore a certificate of \(d_2\ge d_3\), and \(d_1\ge d_2\) is the large gap on these worlds. A nonpositive value is re-optimised with multi-start Nelder–Mead before it can be called a counterexample.

Quick mode (pytest) and `--full` (96 worlds: 80 log-uniform three-mode worlds, a weak third mode, separated shapes, and a low-SNR shape; `theory/model_s_j3_checks/results_full.json`) both returned no certified negative slack. The minimum relative slack on the full screen is \(3.3\times 10^{-9}\). This is numerical evidence. It is not a proof for \(J\ge 3\).

The low-SNR shape in which halving fails (`theory/LAYER_CONVEXITY.md` §6: four modes, ratio \(0.634\)) is unchanged by this note. Theorem S3 does not touch it.

## 3. What remains open

- Model S, three or more distinct rates, lead 0, with no mode negligible next to the others. This is the audit's gap. Open.
- The same at lead \(k>0\), and for a complex pair. Open, and already marked as outside Model S.
- Halving. Open; the known miss stands.
- A causal Monge inequality, or a segment decomposition of the \(K\)-store problem. Not done. The band model still does not prove Model S (decrement-ratio Spearman \(-0.18\)).

A miss on a later screen would be a counterexample and would replace the open status. None is on record in this note.
