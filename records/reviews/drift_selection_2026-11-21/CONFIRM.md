# Blind confirm: PR #146 (drift selection)

**Confirmer:** independent. Wrote none of the note, the simulator, the claim-map rows, or the pointer edits. The findings below were checked against the files at `a79bcd9`, against arXiv:1403.1803, and against a rerun of the review's counterexample. `reviews/drift_selection_2026-11-21/REVIEW.md` (head `93db783`, verdict NOT READY) was the list of items to clear.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/146
**Head confirmed:** `a79bcd9bd40c2272695c9b668c3293f4eff0dbae` on `drift-selection-2026-11-21`. Base `c92886af97425102878241740b093983885a0106` (`origin/main`, merge of PR #144). Draft. Not merged.

**Verdict: NOT READY**

One coefficient sentence added in the fix is false. The DS2 restriction, the fast-fluctuation excess, the \(\varepsilon_{\mathrm{lat}}\) definition, and the STATUS pointers are in place, and the review's equality-case counterexample is no longer a claim of the revised theorem.

## Blockers

1. `theory/DRIFT_SELECTION.md:105`. The new Held paragraph says equation 33, with the scaled adaptive load of equation 52, implies \(2NL_{\rm ad}=D/(2D_m)\) for slow driving, "which is the tracking term of DS1(b)."

   The number \(D/(2D_m)\) is what equations 33 and 52 give (below). It is not the tracking term of DS1(b). DS1(b) in one coordinate is \(1/(2\beta)+D/(2\beta D_m)\), and line 99 of the same note defines that tracking term as \(D/(2\alpha(N-1)D_m)\). Since \(\beta=\alpha(N-1)\), that is \(D/(2\beta D_m)\). The scaled load equals \(\beta\) times this term:
   \[
   \beta\cdot\frac{D}{2\beta D_m}=\frac{D}{2D_m}.
   \]
   The sentence asserts the two are the same quantity. They differ by \(\beta\).

   The factor-of-two claim in the same sentence is a different statement, and it is right: equation 54's slow-driving line is \(\upsilon\tilde\tau\), twice \(\upsilon\tilde\tau/2\). "That value from equations 33 and 52 is DS1" is the review's sentence for the coefficient, and the fast-driving line \(cr^2\) does match DS1(d) once the cost is scaled by \(\beta\) under \(\beta h/2=2Nc_0\). Those parts can stand. The appositive that equates \(2NL_{\rm ad}\) with the unscaled tracking term cannot.

## What was checked and holds

DS2, the review's blocker. `theory/DRIFT_SELECTION.md:120` and the proof at `:122`, copied at `measurement/CLAIM_MAP_v2.md:616` and in the v2.72 note at `:86`.

- The speed bound stays strict: \(|\mathbb{E}[\theta_k(t)-\theta_k(0)]|<v_{\max}t\) with \(v_{\max}=N\mu\delta/(2d)\). Moran \(\varphi(x)<1\) for every finite \(x\) and \(N>1\), so each coordinate's drift is strictly below \(v_{\max}\).
- The cost and divergence bounds are stated only for \(|v_k|>v_{\max}\), and only for \(t\ge|L_k(0)|/(|v_k|-v_{\max})\), where \(B=(|v_k|-v_{\max})t-|L_k(0)|\) is nonnegative. Squaring is applied only after that. The equality case \(|v_k|=v_{\max}\) is dropped in the theorem, in the v2.72 note, and by the strict inequality in S2's claim cell.
- The sign argument holds. For \(v_k>v_{\max}\), \(\mathbb{E}[\theta_k(t)]<\theta_k(0)+v_{\max}t\) gives \(\mathbb{E}[L_k]<L_k(0)-(v_k-v_{\max})t\), and \(\mathbb{E}|L_k|>B\) once \(B\ge0\). For \(v_k<-v_{\max}\), \(\mathbb{E}[\theta_k(t)]>\theta_k(0)-v_{\max}t\) gives \(\mathbb{E}[L_k]>L_k(0)+(|v_k|-v_{\max})t\ge B\). Then \(\mathbb{E}[L_k^2]\ge(\mathbb{E}|L_k|)^2\ge B^2\) and \(\mathbb{E}[J-J^\star]\ge\tfrac12\lambda_{\min}B^2\). A lower bound that grows as \(t^2\) has a time average that diverges.
- The parenthetical "ahead of a receding optimum \((L_k(0)<0)\)" at `:122` names the right initial condition for \(v_k<0\) and the wrong direction of motion: with \(L=\theta-\theta^\star\) and \(v_k<0\), \(L_k(0)<0\) puts the lineage ahead of an optimum that is still approaching. The inequality written after that parenthetical is the one derived above.

Counterexample from the review, rerun here at nice 19 (2,000 replicates, \(\Delta t=0.002\), seed 0, NumPy 2.5.5), same tau-leaping chain as `tools/drift_selection_checks.py`. \(N=20\), \(\alpha=0.05\), \(h=1\), \(\delta=\mu=d=1\), so \(v_{\max}=10\). Constant velocity \(v=v_{\max}\), deterministic start \(L(0)=+10\).

| \(t\) | \(\mathbb{E}[J]\) | review |
|---|---|---|
| 0 | 50 | 50 |
| 0.8 | 0.6645 | 0.66 |
| 1.0 | 1.728 | 1.73 |

The old display claimed \(\mathbb{E}[J]\ge50\) at every \(t\). The revised theorem's hypothesis is \(|v_k|>v_{\max}\), so this run is outside the claim. S2, the v2.72 note, the bottom line at `:21`, and `OPEN_WORK.md`'s T11 sentence all say "faster than" or \(|v_k|>v_{\max}\).

A strict-case spot check with the same chain, \(v=12\), \(L(0)=+10\), threshold \(t=5\): at \(t=1\) (bound not yet claimed) \(\mathbb{E}[J]=5.65\), while squaring the still-negative lag bound would have said \(\ge32\); at \(t=6\), \(B=2\), \(\mathbb{E}|L|=33.5\ge2\) and \(\mathbb{E}[J]=569\ge2\). The documented \(v=5\) and \(v=12\) sentences are the strict cases and can stay. Quick-mode `drift_selection_checks.py` reports lag slope 2.176 against the bound 2 at \(v=12\).

Held, Nourmohammad and Lässig, arXiv:1403.1803 (the version the note cites; PDF equation numbers, matched to `qtad_Arxive.tex`). Equation 33's macroevolutionary line is \(\langle\lambda^2\rangle_{\rm eq}+\upsilon\,\tau_{\rm eq}(c)\,w(c)/2\). Equation 52 sets \(2NL_{\rm ad}=c\) times the excess of \(\langle\lambda^2\rangle\). For \(c\gg1\), \(w(c)\to1\) and \(\tau_{\rm eq}=\tilde\tau/c\), so \(2NL_{\rm ad}=\upsilon\tilde\tau/2\). With \(D_m=\langle\Delta\rangle/(2N)\) and \(D=\upsilon_0\), that is \(D/(2D_m)\). Equation 54's macroevolutionary line is \(\upsilon\tilde\tau\), without the \(1/2\). Equation 54's microevolutionary line is \(cr^2\). Under \(\beta h/2=2Nc_0\), \(\beta\cdot\tfrac12 h\,\mathrm{Var}(\theta^\star)=cr^2\), which is DS1(d)'s fast tracking term. The paragraph does not call equation 54 a typo or an error. The diffusion identifications are the right ones. The blocker above is the one false identification in that paragraph.

Fast-fluctuation excess. `:21` says the excess over the instantaneous minimum tends to \(d/(2\beta)+\tfrac12\mathrm{Tr}(HQ/\gamma)\), and that the second term is the cost of not tracking. That is the \(\gamma\to\infty\) limit of DS1(a): the tracking term in DS1(d) at `:80` tends to \(\tfrac12\mathrm{Tr}(HQ/\gamma)\), and the static piece \(d/(2\beta)\) remains. Section 8 at `:160` still treats \(\tfrac12\mathrm{Tr}(HQ/\gamma)\) as the piece the substitution chain cannot remove.

\(\varepsilon_{\mathrm{lat}}\). `:46` defines \(\varepsilon_{\mathrm{lat}}=\delta^2\beta\lambda_{\max}(1+\mathrm{tr}\,Q/(d D_m))\) as the squared fitness step at a typical lag, \((N|x_e|)^2\sim\varepsilon_{\mathrm{lat}}\) for \(Q=DI\), and writes the geometric ratio \(\delta^2/\mathrm{Var}(L)=\varepsilon_{\mathrm{lat}}/(1+D/D_m)^2\). For Brownian \(Q=DI\) and \(H=\lambda\), \(\mathrm{Var}(L)=(1+D/D_m)/(\beta\lambda)\), so the ratio is that formula. `:62` keeps \(\varepsilon_{\mathrm{lat}}\ll1\) as the fitness-step condition and says the geometric condition is a different one. The world's move per substitution is no longer folded into \(\varepsilon_{\mathrm{lat}}\).

STATUS. `:3` says `main` is `c92886a` (PR #144), that v2.71 is merged with that PR, and that v2.72 is this branch and not yet merged. `origin/main` is `c92886af97425102878241740b093983885a0106`. CX1 at `measurement/CLAIM_MAP_v2.md:506` stays **OPEN**. No status cell in section S changes class: S1 PRIOR ART, S2 PROVED (in-model), S3 and S4 OPEN.

SA3 at `:99` names the tracking term of DS1(b), \(D/(2\alpha(N-1)D_m)\), which is the second term of DS1(b) and not the whole of DS1(b). The simulator docstring and §7 (`tools/drift_selection_checks.py:105`–`:110`, `theory/DRIFT_SELECTION.md:133`) say exact Moran \(\varphi\) and exact quadratic \(\Delta J\), with tau-leaping at probability \(1-e^{-R\Delta t}\). The code does that: one neighbour step when a uniform draw falls under \(1-e^{-R\Delta t}\).

Scope. The Part 2 sentence is byte-identical to `c92886a`, one copy each, in `THEORY.md:41`, `CORE.md:9`, `README.md:9`, and `theory/SELECTION_AXIOMS.md:13`, including the bold markers: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.` `theory/DRIFT_SELECTION.md` does not restate it (`:172`). THEORY's only change against `c92886a` is the claim-map pointer v2.71 to v2.72, and the same pointer in `README.md`. THEORY §4 is untouched. Locked prereg, hash, and `RESULTS.md` paths are absent from `git diff --name-only c92886a`.

## Nits

1. `theory/DRIFT_SELECTION.md:128`. At the documented \(D/D_m=50\) run (\(N=100\), \(\beta h=0.02\), \(h=1\)), \(\mathrm{Var}(L)=(1+50)/(\beta h)=2550\) and the rms lag is \(\sqrt{2550}\approx50.5\) lattice spacings. "Hundreds of lattice spacings wide" overstates that rms. The geometric ratio on the same run is \(1/2550\), so the contrast with \(\varepsilon_{\mathrm{lat}}\approx1.02\) is real. A span of a few standard deviations is about 200.

2. `theory/DRIFT_SELECTION.md:23` and `:116` still say "a simulation of the exact lattice Moran chain." Section 7 and the docstring now say the integrator is tau-leaping. The theorem DS2 is proved for the continuous-time chain; that use of "exact chain" at `:21` and `:120` is the process, not the integrator.

## Commands and results

All from the repo root, on `a79bcd9`, with `nice -n 19`, after `git fetch origin main` (`origin/main` is `c92886a`). NumPy 2.5.5, SciPy 1.18.1. SciPy, pytest, and SymPy were not installed at the start of this run; installing SciPy moved NumPy from 1.26.4 to 2.5.5.

- `git diff --stat c92886af97425102878241740b093983885a0106` (before this file):

```
 CORE.md                                         |   2 +
 OPEN_WORK.md                                    |   2 +-
 README.md                                       |   2 +-
 STATUS.md                                       |   4 +-
 THEORY.md                                       |   2 +-
 measurement/CLAIM_MAP_v2.md                     |  25 +-
 reviews/drift_selection_2026-11-21/REVIEW.md    | 109 +++++++++
 theory/DRIFT_SELECTION.md                       | 172 +++++++++++++
 theory/README.md                                |   1 +
 theory/drift_selection_checks/results_full.json | 220 +++++++++++++++++
 tools/drift_selection_checks.py                 | 308 ++++++++++++++++++++++++
 tools/test_brief.py                             |   4 +-
 tools/test_drift_selection_checks.py            |  52 ++++
 13 files changed, 890 insertions(+), 13 deletions(-)
```

  Path filter for `PREREG`, `LOCK`, `.sha256`, `SHA256`, `predictions.json`, and `RESULTS.md`: no matches.

- Hypothesis sentence: `git show c92886a:<file>` against the working tree. One line each in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`. Line bytes equal the base in all four (107 bytes, bold markers included). `theory/DRIFT_SELECTION.md` has zero copies.

- `nice -n 19 python3 tools/check_fresh.py`. `STATUS.md main is c92886a; window: c92886a 2eeab30 c04cedd d34df95 a97887e`. `RESULT: PASS`. Exit 0.

- `nice -n 19 python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.72; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 334 (tally total 334); process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10569 words, README 1468). `RESULT: PASS`. Exit 0.

- `nice -n 19 python3 tools/check_open_work.py`. `items.json not-DONE: 62; QUEUE.md not-DONE: 90; union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.

- `nice -n 19 python3 tools/drift_selection_checks.py` (quick mode, not `--full`). Lyapunov agreement to the \(10^{-9}\) tolerance on all 20 random trials; fast-world limit and curvature cancellation OK; DS2 \(v=5\) lag slope 0.0004; DS2 \(v=12\) lag slope 2.176 against bound 2. `ALL DS CHECKS PASS`. Exit 0.

- `nice -n 19 python3 -m pytest -q tools`. `179 passed, 1 skipped in 263.12s`. Exit 0. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed`.

- Independent counterexample, parameters above. Not part of `tools/drift_selection_checks.py`.
