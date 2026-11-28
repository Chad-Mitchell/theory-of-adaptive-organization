# Blind confirm of draft PR #153

**Confirmer:** independent. Wrote none of `theory/CHAIN_DIFFUSION.md`, `theory/MODEL_S_J3.md`, the checkers, the claim-map rows, or `reviews/diffusion_convexity_2026-11-21/REVIEW.md`. The author's summary and that review were not treated as authority. The only file added by this confirm is this one. No theory file was edited. The draft branch was not merged.

**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/153
**Head confirmed:** `f70ee71840c2ef258ec966eb7a2a8c14934ca48d` on `diffusion-convexity-2026-11-21`.

**Verdict: CONFIRMED-WITH-NITS**

No blocker. N66 (a)–(c), as narrowed on this head, are true, and the claim-map labels match that narrowing. N67 is the weak-third-mode theorem and the screen numbers recompute. N68 stays open. Five nits are below. None of them makes a displayed theorem false.

## Blockers

None.

## What was checked, and what holds

### N66 (a) — static chain, CD1

Detailed balance is the identity \(\varphi(x)/\varphi(-x)=e^{-(N-1)x}\). A step that changes \(J\) by \(\Delta\) has rate ratio \(e^{-\beta\Delta}\) against its reverse, with symmetric proposal clocks, so the unique stationary law on the irreducible lattice is \(\pi\propto e^{-\beta J}\). Diagonal \(H\) separates the coordinates. Poisson summation is applied in the standard Gaussian form, and
\[
\frac1{2\beta}-\mathbb{E}[J]=\frac{4\pi^2}{\beta a}\rho,\qquad
\rho=\frac{q+4q^4+9q^9+\cdots}{1+2q+2q^4+\cdots},\quad q=e^{-2\pi^2/a}.
\]
For \(a\le 1\), \(\rho\le q+8q^4\le 2q\), which is the factor \(8\pi^2\). The lattice excess sits strictly below \(d/(2\beta)\). With \(\pi\) computed at 80 decimal places, \(\mathrm{gap}/\mathrm{lead}\) is \(0.99999999465\) at \(a=1\), \(\beta=1\), and the gap is positive and at most twice the leading term at \(a\in\{0.4,0.9,1\}\).

### N66 (b) — Brownian one coordinate, CD2 and CD3

The generator identity on \(L^2\) is exact:
\[
\mathbb{E}[J-J^\star]-\frac1{2\beta}\Bigl(1+\frac{D}{D_m}\Bigr)=\frac{\mathbb{E}[R]}{4 D_m\beta},
\]
whenever the stationary second moment is finite. The linear Moran map leaves \(R=-a\delta^2/2\) for every \(L\), with \(a=D_m\beta h\). Recomputed at four \((N,\beta,h,\delta,L)\) points, the residual against \(-a\delta^2/2\) is at most \(3\times 10^{-15}\). A constant that depends only on \(N\) cannot absorb this term: at \(L=0\), \(|R|=D_m\beta h\delta^2/2\), which is larger than \(D_m(\beta h\delta)^2\) by \(1/(\beta h)\). The displayed CD2 bound keeps the factor \(\beta h\).

On \(|z|=2\), \(\min|\sinh|= \sin 1\) and \(\max|f|\le 2.30<3.4\) for \(N\in\{2,3,5,20,100\}\). The quadratic coefficient matches \((N-1)(N-2)/(12N^2)\). The remainder ratios on \([-1,1]\) are at most \(0.006\) against \(3.4|z|^3\) and \(0.14\) against \(10.2 z^2\). Over 7,179 bulk points (several \(N\), \(\beta\), \(h\), \(\delta\), and fractions of the bulk), \(\max|R|/\mathrm{bound}=0.0010\), with no violation. The sum piece the proof bounds by 80 is at most \(0.165\). The constants are loose and they hold, including the \(\beta h\) dependence.

The stationary gap divided by \(\delta^2\), at \(N=20\), \(\beta=h=D_m=D=1\), is \(0.1387, 0.1385, 0.1383, 0.1382, 0.1382, 0.1382\) for \(\delta\in\{0.50,0.35,0.25,0.18,0.12,0.08\}\). The two sides of (I) differ by at most \(10^{-12}\). At \(\beta=0.05\), \(N=10\), the same ratio is \(0.1528\) at \(\delta\in\{0.40,0.20,0.10\}\). For fixed \(\beta,h,D_m,D\) the difference is \(O(\delta^2)\), and the constant moves when \(\beta h\) moves, as CD2 says it must. Ornstein–Uhlenbeck, constant velocity, and a non-diagonal Hessian are marked sketches in the note, the claim row, and the drift note, and they are not used in CD3.

The drift comparison that the exponential moment needs is true on the whole bulk, not only in a small \(\eta\)-ball. On 157,413 points with \(N\in\{2,\ldots,30,50,100,200,1000\}\) and \(\varepsilon=\beta h\delta^2\le 0.2\),
\[
\max\frac{|\mu+aL|}{a|L|}=0.035
\]
(at \(N=6\), \(u=\beta h\delta L=0.732\), \(\varepsilon=0.2\)). For \(N=2\) and \(\varepsilon=0\) the ratio is closed form: \(\tanh(s/4)/(s/4)\ge\tanh(1/4)/(1/4)>0.979\) on the bulk \(s\in(0,1]\). So \(|\mu|\ge(a/2)|L|\) holds out to radius \(1/\delta\). Off that radius the uphill fixation bound gives a restoring speed of order \(D_m/\delta\). With those two drifts, \(V=\cosh(\lambda L)\) for small fixed \(\lambda\) satisfies \(GV\le -V+K\) outside a compact that does not grow with \(\delta\), and \(K\) does not depend on small \(\delta\). The exponential moment is uniform in \(\delta\). The \(O(\delta^2)\) bound on \(\mathbb{E}[R]\) then follows from CD2 on the bulk (using \(\mathbb{E}[L^4]\le M\)) and from the exponential tail beyond radius \(1/\delta\), which beats every positive power of \(\delta\).

### N66 (c) — path measure, CD4

Ethier and Kurtz, Chapter 4, §8, was read against the 1986 statement (DOI checked below).

- **Generator convergence.** For \(f\in C_c^\infty\), both generators vanish off a \(\delta\)-neighbourhood of the support. On the remaining fixed compact, \(|Nx_\pm|=O(\delta)\). Taylor expansion with a bounded third derivative, paired with the linear map, gives drift \(-aL+o(1)\) and diffusion coefficient \(D_m+D+o(1)\), uniformly. So \(\|Gf-\mathcal{L}f\|_\infty\to 0\).
- **Compact containment.** For any fixed radius \(R\), small \(\delta\) puts \(|L|\le R\) inside the region where the \(\eta\)-estimate already gives \(G(L^2)\le -aL^2+C_R\), with \(C_R\) independent of \(\delta\). Stopping at \(\tau_R\) and using the uniform second moment of the initial laws is the standard estimate. The \(1/\delta\) tail is not required.
- **Well-posedness and the core.** The limit is a linear stochastic differential equation with Lipschitz coefficients, so it has one strong solution and the martingale problem has one solution per initial law. The transition law is Gaussian, so the semigroup is Feller on \(C_0(\mathbb{R})\) and \(C_c^\infty\) is a core: it is an algebra that separates points, and the closure of the Langevin operator on it is the generator. That is the hypothesis Theorem 8.2 places under Corollary 8.7. Compact containment is (7.9) of their Chapter 3. Condition (f) of Corollary 8.7 holds with \(f_n=f\) and \(g_n=Gf\), because the convergence is uniform on \(\mathbb{R}\) for each compactly supported \(f\).

The note's sentence that finite-horizon convergence does not give convergence of stationary means is right. That convergence is CD3.

### N67 and N68

Theorem S3 uses the strict two-mode gap from Theorem S2 and the degree gap (two positive residues, Lemma P). \(E_0\) jumps by \(v_3\). \(E_\infty\) is continuous at \(v_3=0\) for fixed \(a_3\) by dominated convergence: the dominate is the two-mode spectrum plus one OU spectrum of variance 1 at that rate, and the note correctly refuses a single OU spectrum of variance \(v_1+v_2+1\) as a dominate for every rate. \(E_1\) stays on a compact of rates for small \(v_3\), with the modulus depending on \(a_3\). \(E_2\) is squeezed to \(E_\infty^{(2)}\) by the two-mode spectral-factor design. The decrements stay ordered for small \(v_3\), and the smallness is allowed to depend on the third rate. Comparable modes are not claimed.

The screen's certificate is one-sided and in the right direction: a grid value of \(E_2\) is an upper bound, clipping it up to \(E_\infty\) makes \(E_1-2E_2+E_\infty\) smaller, and a positive certificate implies \(d_2\ge d_3\). It does not certify \(d_1\ge d_2\).

Independent recomputation, own Gram matrix and own spectral-factor polynomial, seed 7 regenerated:

| Quantity | Stored | Recomputed |
|---|---|---|
| Worlds | 96 | 96, parameters of worlds 0, 45, and 83 match |
| Minimum of \((E_1-2E_2+E_\infty)/E_0\) | \(3.2680601715354446\times 10^{-9}\) at world 83 | same index and same value; slack \(2.524055187\times 10^{-8}\), \(E_0=7.723404878\) |
| World 83, \(E_1-E_\infty\) | \(2.524055\times 10^{-8}\) | \(2.524100\times 10^{-8}\) from an independent one-store minimum against the spectral-factor \(E_\infty=0.0267234425247711\) |
| World 83 rates, variances, noise | about \(0.0067, 0.011, 0.050\); \(7.68, 0.012, 0.036\); \(0.0067\) | \(0.006733, 0.011024, 0.050117\); \(7.67587, 0.011950, 0.035581\); \(0.006687\) |
| Negative certificates | 0 | 0 |
| Largest stored \(d_3/d_2\) | 0.885 at world 45 | \(0.884776\) at world 45, from the stored decrements \((6.1267\times 10^{-5},\, 5.4208\times 10^{-5})\) |

World 45's stored ratio is the coarse grid. An independent multi-start minimum gives \(E_1=2.554914740\), \(E_2=2.554801899\), \(E_\infty=2.554799265\), so \(d_3/d_2=0.0233\). The sentence in the note says "stored". The certificate \(d_2\ge d_3\) still holds, and the true ratio on that world is smaller. N68 remains open. The \(3.3\times 10^{-9}\) figure is an almost one-mode world whose decrements after \(K=0\) are already at the floor. It is not a near failure of convexity.

### Labels, sentence, wording, DOI

`measurement/CLAIM_MAP_v2.md` row N66 is **PROVED (in-model)** for the static Poisson bound, the Brownian identity and \(O(\delta^2)\) excess, and Skorokhod convergence under converging initial laws with a uniform second moment. OU, constant velocity, and non-diagonal \(H\) are outside the row. N67 is **PROVED (in-model)** for a weak third mode, with the threshold allowed to depend on the rate. N68 is **OPEN**. S1 stays **PRIOR ART**. N64 stays **PROVED (in-model)**. The tally move \(357\to 360\) is \(+2\) proved and \(+1\) open. `check_consistency.py` reports 360 rows and 0 section-N mismatches.

The hypothesis sentence is one copy in each of `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`, and the bytes are

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

No new note uses `bill`. The only `kill` in the diff is the pre-existing phrase `SANITY 7/8 (kill)` inside the long W9 cell. It is not a verdict on N66, N67, or N68. Wording FAILs from the consistency check: 0.

Crossref, 22 November 2026, DOI `10.1002/9780470316658`: Ethier, Stewart N. and Kurtz, Thomas G., *Markov Processes*, subtitle *Characterization and Convergence*, Wiley, issued 21 March 1986. Chapter 4 is a part of that monograph (`10.1002/9780470316658.ch4`). The citation in `theory/CHAIN_DIFFUSION.md` matches.

The drift paragraph in `theory/DRIFT_SELECTION.md` now says the diffusion limit is the fitness step \(\varepsilon_{\mathrm{lat}}\to 0\), and it keeps \(\delta^2/\mathrm{Var}(L)\) as a different condition. That matches the scaling in CD3.

## Nits

1. **`theory/CHAIN_DIFFUSION.md:144–148` and `:156`, and the summary at `:168`.** The \(\eta\)-estimate produces \(|\mu+aL|\le(a/2)|L|\) only on \(|\beta h\delta L|\le\eta\). The next sentence asserts the same bound for \(1\le|L|\le L_B\), where \(|\beta h\delta L|\) is of order 1. The displayed Cauchy constants do not bridge that gap: with \(|f'''|\le 20.4\) the triangle inequality allows an error many times \(a|L|\) at the edge of the bulk. The bound is nevertheless true. The fixation map gives \(|\mu+aL|\le 0.035\, a|L|\) on the net above, and for \(N=2\), \(\varepsilon=0\), the ratio is \(\tanh(s/4)/(s/4)\). The exponential moment and the \(O(\delta^2)\) excess stand once that comparison is used in place of the \(\eta\)-sentence. The same jump appears in "CD2 and the choice of \(\eta\) give \(R\le(a/2)L^2+K_0\)" and the following "thus" out to \(L_B\): the quartic piece of CD2 exceeds \((a/2)L^2\) once \(|\beta h\delta L|>1/\sqrt{2000}\). The drift comparison, not that quartic, is what controls \(G(L^2)\).

2. **`measurement/CLAIM_MAP_v2.md:86`, `theory/DRIFT_SELECTION.md:62`, `theory/README.md:13`.** These three summaries say the path measure converges when the initial laws converge. CD4 and row N66 also require a uniform second moment. The counted row is the accurate one. The summaries drop a hypothesis.

3. **`theory/CHAIN_DIFFUSION.md:192–194`.** Corollary 8.7 sits on Theorem 8.2, whose hypothesis is that the closure of the operator generates a strongly continuous contraction semigroup, on a domain that contains an algebra separating points. The note discharges well-posedness by unique strong existence, which is the hypothesis of their Theorem 8.10, and it never says that \(C_c^\infty\) is a core. Both facts hold for this linear diffusion, and compact containment and generator convergence are proved. The citation should name the core.

4. **`theory/MODEL_S_J3.md:39` and world 45.** The largest stored \(d_3/d_2\) is \(0.884776\), which rounds to the printed \(0.885\). A refined two-store minimum on the same world gives \(0.0233\). The word "stored" is accurate. It should not be read as the optimised margin.

5. **`theory/MODEL_S_J3.md:19` and `tools/model_s_j3_checks.py:139–141`.** "The strict degree gap of L2" points at the wrong label: in `theory/LAYER_CONVEXITY.md` the row L2 is the halving lemma. The fact used is Lemma P, two positive residues, and \(E_1>E_\infty\) is right. Separately, `curve` sorts the rate vector and does not permute the variances with it. The fixed low-SNR triple is therefore not the pairing \(v_j\propto\sqrt{a_j}\). It is not world 83, and the note does not use it as the halving miss. The miss remains the four-mode example in `theory/LAYER_CONVEXITY.md`.

`STATUS.md:3` still contains the sentence "CLAIM_MAP v2.76 (this branch, not yet merged)" after the header was moved to v2.77. v2.76 is the parent merge `d1a6de4`. The consistency check does not read that clause. It is stale, and it does not change a claim label.

## Commands and results

`lake build` was not run. `tools/test_lean.py` skipped the build because `lake` is not on the path; the source scan for forbidden tokens did run.

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | PASS. THEORY v2.9; CLAIM_MAP latest note v2.77; wording FAILs 0 on 30 maintained docs; section N 68 rows (N1..N68), 0 mismatches; tally 360 = 360; core index 74 = 74; process-rule FAILs 0; core-rule FAILs 0. Length warnings are the pre-existing advisory ones (THEORY main text 10948 words, README 1476). |
| `python3 tools/check_fresh.py` | PASS. `STATUS.md` main is `b16193d`; window `b421b22 98ff384 d1a6de4 b16193d e88b692` (`origin/main` fetched 22 Nov 2026). |
| `python3 tools/check_open_work.py` | PASS. items.json not-DONE 62; QUEUE.md not-DONE 90; union missing from OPEN_WORK.md 0. |
| `nice -n 19 python3 -m pytest -q tools` | `247 passed, 1 skipped` in 298.50s. The skip is the Lean build. |
| Own CD audit, `/tmp` (not committed) | CD1 high-precision gaps as above. Linear defect residuals \(\le 3\times 10^{-15}\). CD2: 7179 points, 0 violations, max ratio \(0.0010\). Drift-error max \(0.03497\). Stationary \(\mathrm{gap}/\delta^2\) flat, as above. |
| Own N67 audit, `nice -n 19`, own Gram and spectral factor | Minimum relative one-sided slack \(3.2680601715354446\times 10^{-9}\) at world 83. Largest stored \(d_3/d_2=0.884776\) at world 45. Refined world-45 ratio \(0.02334\). No negative certificate in 96 worlds. |
