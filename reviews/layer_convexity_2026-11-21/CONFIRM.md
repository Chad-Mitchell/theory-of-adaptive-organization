# Blind confirm: PR #145 (layer convexity)

**Confirmer:** independent. Wrote none of `theory/LAYER_CONVEXITY.md`, the checks, the claim-map row, the pointer edits, or `REVIEW.md`. The only file added by this confirm is this one.
**Date:** Sunday 22 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/145
**Head confirmed:** `9070f20bcc408b911e5280ae7c91521897e90e1b` on `layer-convexity-2026-11-21`. The review was of `a318981`. Current `origin/main` is `dc7d731e465e24507b84de9e7b553675ebbf1312`. Draft. Not merged.

**Verdict: READY**

No blockers. No should-fixes. The exactness theorem is the from-0 count on a finite domain, for every \(R\ge 0\), and the same statement is in the note, the v2.72 note, row N64, W9, and the keystone status table. Lemma Z now assumes \(W\ge 0\). Model S at \(J\ge 3\), and any real system, stay unproved.

## 1. Exactness

`REVIEW.md` said the note identified the wrong count and then printed a bare "iff". At `9070f20` the count is

\[
K^\star_0(R)=\#\{K\ge 1: R\,d_K>1\},\qquad d_K=\varepsilon_{K-1}-\varepsilon_K,
\]

on a finite domain \(K\in\{0,\ldots,K_{\max}\}\).

| Required piece | Where it is stated |
|---|---|
| Formula, finite domain, all \(R\ge 0\) | `theory/LAYER_CONVEXITY.md:11`, `:35`, `:37` |
| Non-increasing \(d_K\) ⇒ leftmost argmin | `:11`, `:21`, `:37`–`:38` |
| Converse only for positive, pairwise distinct decrements | `:11`, `:37`–`:38` |
| \(d=(-2,-1)\) kills a bare iff | `:11`, `:40` |
| N60 as written in `core/KEYSTONE_NOTE.md` returns 1 on \(\varepsilon=(1,0.4,0)\) at \(R=1\) | `:42`; keystone hole also at `core/KEYSTONE_NOTE.md:33` and `:61` |
| Same theorem in the v2.72 note | `measurement/CLAIM_MAP_v2.md:86` |
| Same theorem in N64's claim and Why | `measurement/CLAIM_MAP_v2.md:469` |
| Same theorem in W9 | `OPEN_WORK.md:21` |

N60's own row is still the from-1 formula, **PROVED (in-model) given convexity (numerical)** (`measurement/CLAIM_MAP_v2.md:465`). That is the row the review said to leave alone.

**Forward direction, rederived.** \(J(K)=K+R(1+\varepsilon_K)\) gives \(J(K)-J(K-1)=1-R\,d_K\). For \(R\ge 0\) and non-increasing \(d_K\), the differences are non-decreasing, so the strict drops are a prefix. At \(R=0\), \(J(K)=K\) and \(K^\star_0(0)=0\). For \(R>0\), \(K^\star_0(R)\) is the last strict drop, which is the leftmost minimizer. Ties (\(R\,d_K=1\)) stay flat, and the strict inequality keeps the leftmost index.

**Converse, rederived.** If \(d_m<d_{m+1}\), then \(\varepsilon_m\) sits strictly above the chord from \(m-1\) to \(m+1\) by \((d_{m+1}-d_m)/2\), so \(J(m)>\min(J(m-1),J(m+1))\) for every \(R>0\). Index \(m\) is never a minimizer. If the decrements are positive and pairwise distinct, order them \(d_{(1)}>\cdots>d_{(K_{\max})}>0\). Any \(R\in(1/d_{(m)},1/d_{(m+1)})\) has exactly \(m\) decrements above \(1/R\), so the count returns \(m\). Two thousand random positive sequences with an ascent all did this: the count equalled the ascent index, and that index was not the minimizer. The parenthetical weakening (distinctness plus \(d_{(m)}>0\)) is the same construction when the tail of the order statistics is allowed to be non-positive.

**The two witnesses.** \(\varepsilon=(1,0.4,0)\), \(d=(0.6,0.4)\), \(R=1\) gives \(J=(2,2.4,3)\), leftmost argmin 0, from-0 count 0, from-1 count 1. \(d=(-2,-1)\), \(\varepsilon=(-3,-1,0)\) is not convex, \(R\,d_K>1\) never holds, and \(J(0)=-2R\) is the unique minimizer for every \(R\ge 0\). Both are in `tools/test_layer_convexity_checks.py`.

Under non-increasing decrements, \(1+\#\{k\ge 2: R\,d_k>1\}\) equals \(K^\star_0(R)\) when that count is at least 1, and equals 1 when \(K^\star_0(R)=0\). `theory/LAYER_CONVEXITY.md:42` says "under non-increasing". The v2.72 note, N64, and W9 put the same relation in the parenthesis that follows the non-increasing hypothesis. The "\(\ge 1\)" half is not an identity for a general sequence: \(d=(0.1,2)\) at \(R=1\) has from-0 count 1 and from-1 count 2. That sequence is outside the hypothesis those sentences are under.

## 2. Lemma Z, rederived with \(W\ge 0\)

**Statement** (`theory/LAYER_CONVEXITY.md:63`). If \(W\ge 0\) and \(W\) is non-increasing, then \(w(i,k)-w(j,k)\le z(i)-z(j)\) for \(i\le j\le k\), where \(w\) is the weighted within-interval variance and \(z(x)=\int_{[x,\infty)}W^2\,d\mu\).

**Proof.** Let \(A=[i,j)\) and \(B=[j,k)\). If \(\mu_B=0\), then \(w(j,k)=0\) and the constant level 0 on \(A\) costs \(\int_A W^2\,d\mu=z(i)-z(j)\), which is an upper bound on \(w(i,k)\). If \(\mu_B>0\), keeping \(B\)'s mean \(m_B\) on \(A\) costs \(w(j,k)+\int_A(W-m_B)^2\,d\mu\), an upper bound on \(w(i,k)\). Non-increasing \(W\) puts every value on \(A\) at least as large as every value on \(B\), so \(W\ge m_B\) on \(A\). Non-negative \(W\) puts \(m_B\ge 0\). Then \(W^2-(W-m_B)^2=m_B(2W-m_B)\ge 0\), so \((W-m_B)^2\le W^2\) and the integral over \(A\) is at most \(z(i)-z(j)\).

**The hypothesis is necessary.** \(W=(0,-1)\) with equal weights is non-increasing and not non-negative. \(w(AB)-w(B)=1/2\) and \(z(0)-z(1)=0\). `seg_cost_matrix` returns the same pair, \(0.5\) and \(0\). Two thousand random non-negative non-increasing draws, some with a zero mass, had 0 violations. Inside 𝓑, \(W=1/(1+N/S)\ge 0\), so the hypothesis holds.

## 3. The other fixes

**Lemma X, \(t=1\).** `theory/LAYER_CONVEXITY.md:66`–`:67`. On a finite grid the breakpoint set is finite, so an optimal path exists. \(P=(p_0,\ldots,p_K)\) has \(K-1\) free bands and \(Q=(q_0,\ldots,q_{K+2})\) has \(K+1\), with sentinels \(p_K=q_{K+2}=\infty\) and every earlier breakpoint finite. The crossing time \(t=\min\{t\in\{1,\ldots,K\}: q_{t+1}\le p_t\}\) exists because \(q_{K+1}<\infty=p_K\). For \(t=1\), \(p_0\le q_1\) is \(0\le q_1\), not a consequence of minimality. For \(t\ge 2\), minimality gives \(p_{t-1}<q_t\). With monotonicity, \(p_{t-1}\le q_t\le q_{t+1}\le p_t\). The swapped paths each have \(K+2\) breakpoints, hence \(K\) free bands. The cost change is \([c(p_{t-1},q_{t+1})+c(q_t,p_t)]-[c(p_{t-1},p_t)+c(q_t,q_{t+1})]\). For \(t<K\) all four ends are finite and Lemma M applies. For \(t=K\), \(c(p_{K-1},\infty)=z(p_{K-1})\) and \(c(q_K,\infty)=z(q_K)\), which is Lemma Z. So \(2E_K\le E_{K-1}+E_{K+1}\).

**Infinity sentinel.** `theory/LAYER_CONVEXITY.md:58`. \(c(x,y)=w(x,y)\) for finite \(y\), and \(c(x,\infty)=z(x)\). On a grid \(\{0,\ldots,M\}\) a free band that ends at \(M\) still pays the within-band variance; the terminal pays \(z\).

**Theorem B.** `theory/LAYER_CONVEXITY.md:69`. Finite grids are Lemmas M, Z, and X. Convexity passes to a pointwise limit of grid costs, which is what "pass to the infimum" uses for a continuous measure. The sentence is about \(E^B_K\), not Model S's causal \(E_K\). Section 6 says so again.

**Third decrement.** `theory/LAYER_CONVEXITY.md:85` now says 0.179, 0.578, 0.226. From `core/KEYSTONE_NOTE.md:105`, \(E_\infty=0.03788281801526715\) and \((E_1,\ldots,E_4)=(0.08051946,0.07373616,0.05183293,0.043288)\) give decrements 0.17906, 0.57818, 0.22556, which round to those three figures. The keystone table's 0.2256 is the same number to four decimals.

**Halving screen.** `theory/LAYER_CONVEXITY.md:17` and `:92`, and the S5 block in `tools/layer_convexity_checks.py`. Screened at \(\varepsilon_K>10^{-4}\): S5 is 120/120 with max ratio 0.3375 (the note's 0.34); the 24 fresh \(J=5\) worlds in `theory/layer_convexity_checks/models_j5.json` have max ratio 0.4380 (the note's 0.44). Together, 144/144. Unscreened, S5 has 17 ratios above \(1/2\) and the \(J=5\) file has 19, including seed 16 at \(K=4\) with \(\varepsilon_K=1.83\times 10^{-6}\) and ratio 0.781. The adversarial file's maximum is 0.462526 (the note's 0.4625), at \(\tau=1,\,2.605,\,4.058\times 10^7\).

The low-SNR example was recomputed. \(J=4\), \(a=(1,10^{-3},10^{-6},10^{-9})\), \(v_j=10^{-6.5}\sqrt{a_j}\), \(N=1\). Each mode has the same leading variance reduction \(v_j^2/(2a_j N)=5\times 10^{-14}\). Polishing the store rates from the subset Kalman poles gives \(\varepsilon_1=4.750\times 10^{-7}\), \(\varepsilon_2=3.014\times 10^{-7}\), ratio 0.634, and decrements \(1.95,\,1.74,\,1.51,\,1.50\times 10^{-7}\), which are non-increasing. The printed 4.75, 3.01, and 0.634 are those figures. Halving fails and convexity holds.

## 4. What is still open

Nothing in the note, N64, or W9 says Model S at \(J\ge 3\) has been proved, and nothing says a real system has been proved.

- `theory/LAYER_CONVEXITY.md:17`, `:28`, `:91`. \(J\ge 3\) is OPEN. The numerical line is 144/144. The halving conjecture is OPEN. Lead \(k>0\), non-Gaussian worlds, and the predictive rhythm rule stay open (`:94`).
- `measurement/CLAIM_MAP_v2.md:86` and `:469`. \(J\ge 3\) stays numerical. N60 keeps **PROVED (in-model) given convexity (numerical)**.
- `OPEN_WORK.md:21`. **Still open:** Model S with \(J\ge 3\), halving screened at \(\varepsilon_K>10^{-4}\), and a causal analogue. T15 (`OPEN_WORK.md:62`) is still the placeholder for a layer count on real systems.
- `core/KEYSTONE_NOTE.md:5`, `:61`, `:66`, `:72`, `:107`. The table is the review's sentence: proved for \(J\le 2\) at lead 0, and for \(J\ge 3\) numerical only, with the from-1 hole still there. The three later sentences attach "for \(J\ge 3\)" to the unproved premise. The field-test row is still "None" (`:64`).

Theorem S2 (`theory/LAYER_CONVEXITY.md:79`) is \(J\le 2\) at lead 0. The Cauchy–Schwarz step for general \(J\) is a \(1/J\) share, and the note calls it a bound, not convexity (`:81`). The check's fresh two-mode worst excess share is 0.3044, and the smallest one-store share is 0.6727.

## 5. Merge, the Part 2 sentence, locked files

`git merge-tree --write-tree origin/main HEAD` exits 0 against `dc7d731`. The only overlapping path is `OPEN_WORK.md`, and git auto-merges it. The merged W9 cell still has the from-0 sentence, \(d=(-2,-1)\), and \(\varepsilon=(1,0.4,0)\) at \(R=1\). No conflict markers. This confirm did not merge the branch.

The Part 2 sentence is byte-identical to `origin/main`, one copy each, including the bold markers:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`.

`git diff --name-only c92886a HEAD` has no path matching `PREREG`, `LOCK`, `hash`, `predictions.json`, or `.sha256`. `origin/main` since `c92886a` is the lean-core merge (`dc7d731`); it does not touch those paths either.

## Residual wording

These understate \(J\le 2\). They do not say \(J\ge 3\) or a real system is proved.

- `core/KEYSTONE_NOTE.md:66`. The line says the premise "remains unproved for \(J\ge 3\)", and then, in the next sentence, that the single-store count formula is "in-model, unproved" with no \(J\le 2\) exception.
- `OPEN_WORK.md:101` and `:107`. Outside the W9 cell, "convexity itself remains unproved" and "Convexity remains unproved (W9)" have no \(J\ge 3\) limit. The W9 cell at `:21` has the limit.
- `CORE.md:113`. Unchanged from the base: "Convexity inside Model S is numerical (120/120), not proved." That is now too broad for \(J\le 2\). The review had already accepted `CORE.md` as untouched, and this confirm did not edit it.

## Commands

All from the repo root on `9070f20`, numerics and tests at `nice -n 19`. NumPy 2.5.5 and SciPy 1.18.1 were installed for the rerun (the image had NumPy 1.26.4 and no SciPy). SymPy 1.14.0 was installed so `tools/test_robust_checks.py` could collect. The layer-convexity run rewrote `theory/layer_convexity_checks/layer_convexity_checks.json` with the same bytes (SHA-256 `88430672592fbcce7d0c2838295bd27ffd1fcc0fbcaff68d472d63788f5a0fc6`). The work tree was clean apart from this confirm.

- `python3 tools/check_fresh.py`. `STATUS.md main is 2eeab30; window: dc7d731 c92886a 2eeab30 c04cedd d34df95`. `RESULT: PASS`. Exit 0.
- `python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.72; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 331; process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10569 words, README 1468). `RESULT: PASS`. Exit 0.
- `python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `python3 tools/layer_convexity_checks.py`. `ALL LAYER CONVEXITY CHECKS PASS`. Exit 0. The lines match `theory/layer_convexity_checks/layer_convexity_checks.out`, including the screened S5 halving line `120/120` with max ratio 0.3375 on `J4_K1`.
- `python3 -m pytest -q tools`. `182 passed, 1 skipped in 256.64s`. Exit 0. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed. The two new tests are the from-0 / \(d=(-2,-1)\) cases and the \(W=(0,-1)\) failure of Lemma Z.
