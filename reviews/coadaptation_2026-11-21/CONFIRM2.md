# Blind confirm 2: PR #148 fixes at 93add78

**Confirmer:** independent. Wrote none of the note, the checks, `REVIEW.md`, or `CONFIRM.md`. The limit below was rederived from the Moran fixation ratio and from an independent generator, then compared with the files at `93add78`.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/148
**Head confirmed:** `93add78db5778cbac631e15fb4d67364e45326a6` on `coadaptation-2026-11-21`. Parent `db47139f3674467efd07441510bf0f79ed29f4b9` (the first confirm). The first confirm reviewed `c098e456d5b9226e2c3ec9d988eb23ecfee20527`. Draft. Not merged.

**Verdict: READY**

No blockers. No should-fixes. No nits. The should-fix and the three nits in `reviews/coadaptation_2026-11-21/CONFIRM.md` are fixed at `93add78`, and the fix adds nothing else.

## Items

1. **Confirmed. Barrier-held scale-separation limit.** `theory/COADAPTATION.md:168`–`:180`, the bottom line at `:9`, the check line at `:206`, and S9 (`measurement/CLAIM_MAP_v2.md:623`). No correction.

   States \((x_1,j)\) with \(J(1,j)=\varepsilon j\), \(J(0,0)=\Delta\), \(J(0,j>0)=B\). Party \(i\) moves its own coordinate, and the haploid Moran fixation ratio on a cost step \(\Delta J\) is \(\varphi(\Delta J)/\varphi(-\Delta J)=\exp(-\gamma_i\Delta J)\). Inside a fixed row, party 2 is a birth-death chain with that ratio. On row 1 the step ratio is \(\exp(-\gamma_2\varepsilon)\). On row 0 the step from \(j=0\) to the barrier is \(\exp(-\gamma_2(B-\Delta))\), and the barrier states are neutral with each other. Send \(\varepsilon\to 0\) and \(\gamma_2\to\infty\) with \(\gamma_1\varepsilon\ll 1\ll\gamma_2\varepsilon\) at fixed \(\gamma_1\), \(\Delta\), and \(B\). Then \(\gamma_2(B-\Delta)\to\infty\) as well, both rows pin at \(j=0\), and the mass on every other state vanishes. The remaining edge is party 1's move between \((1,0)\) (cost 0) and \((0,0)\) (cost \(\Delta\)), so
   \[
   \mathbb{E}_\pi[J]\longrightarrow\frac{\Delta e^{-\gamma_1\Delta}}{1+e^{-\gamma_1\Delta}}.
   \]
   The matched Gibbs law at \(\gamma_1\) keeps the barrier states. At \(\varepsilon=0\),
   \[
   E_{\mathrm{Gibbs}}(\gamma_1)=\frac{\Delta e^{-\gamma_1\Delta}+B(m-1)e^{-B\gamma_1}}{m+e^{-\gamma_1\Delta}+(m-1)e^{-B\gamma_1}},
   \]
   and as \(m\to\infty\) this tends to \(B e^{-B\gamma_1}/(1+e^{-B\gamma_1})\). At \(\gamma_1=1\), \(\Delta=0.5\), \(B=10\) the ratio of those two limits is \(415.813208405\), which is \(415.8\) to one decimal. The same value is what `s7c` stores as `entropic_ratio_m_inf_barrier_held`. Along the closed forms the ratio rises from \(36.7506\) at \(m=64\) to \(415.536\) at \(m=10^6\) and \(415.8129\) at \(m=10^9\), and stays below the limit.

   The expression \((m+e^{-\gamma_1\Delta})/(1+e^{-\gamma_1\Delta})\) is that ratio when the barrier states are removed: the Gibbs denominator is then \(m+e^{-\gamma_1\Delta}\) and the numerator is \(\Delta e^{-\gamma_1\Delta}\). It is also that ratio when \(B\to\infty\) with \(m B e^{-\gamma_1 B}\) negligible beside \(\Delta e^{-\gamma_1\Delta}\). That product bound makes the barrier's share of the Gibbs numerator negligible, and the barrier's share of the denominator is smaller by the factor \(\Delta/B\). An independent deleted-barrier chain at \(m=8\), \(\varepsilon=10^{-8}\), \(c_2=10^9\) has ratio \(5.35706\) against the arrow \(5.357215\). At \(B=10\) the product is not negligible for large \(m\) (at \(m=64\) it is \(0.0958\) times \(\Delta e^{-\gamma_1\Delta}\); at \(m=10^6\) it is \(1.50\times 10^3\) times that target), and the note states the arrow only in the regime where the product is negligible.

   The finite chain at the printed point \(m=64\), \(\varepsilon=10^{-5}\), \(c_1=1\), \(c_2=10^6\), \(B=10\), \(N=10\), clocks \((1,1)\) has ratio \(34.6350508\), which rounds to \(34.64\). An independent Grassmann–Taksar–Heyman solve of an independent generator gives the same ratio to those digits. The checker's `s7c` row is \(E=0.1887650068\), Gibbs \(0.0054501149\), ratio \(34.6350508\). The ideal barrier-aware ratio at this \(m\) is \(36.7506\); the note prints \(34.64\) for the finite chain and \(415.8\) for the limit of the limits, and keeps the two apart. \(34.64>1\), so the bracket is false on this chain.

2. **Confirmed. \(a_2/\mathrm{Var}=-0.01130\).** `theory/COADAPTATION.md:162` and `:206`. No correction.

   On \(J=\begin{pmatrix}0.867&0.2\\0.063&0.058\end{pmatrix}\) at \(\gamma=12.946561340217954\), clocks \((3.9406248608293835,\ 10.771274476091913)\), \(N=10\), an independent solve of \(Lh=\tilde J\) gives \(a_2=-1.5592963843\times 10^{-5}\), \(\mathrm{Var}=1.3804418840\times 10^{-3}\), and \(a_2/\mathrm{Var}=-0.011295632235\). Rounded to five decimals that is \(-0.01130\). The checker's `local_a2_over_var` is \(-0.011295632235\), the same value, and \(\sum_i a_i=\mathrm{Var}\) to \(10^{-18}\). A centered difference of \(\partial\mathbb{E}[J]/\partial\gamma_2\) matches \(-a_2\) to relative \(7.5\times 10^{-9}\) at step \(10^{-4}\). The excesses of \(\mathbb{E}[J]\) over \(E_{\mathrm{Gibbs}}(\gamma)\) at \(\varepsilon=0.01,\ 0.1,\ 0.5\) are \(1.560\times 10^{-7}\), \(1.566\times 10^{-6}\), and \(7.960\times 10^{-6}\), the digits already printed on `:162`.

3. **Confirmed. S9 credits Freidlin–Wentzell for the tree theorem.** `measurement/CLAIM_MAP_v2.md:623`, Why cell. No correction.

   The cell reads: "Tree theorem (Freidlin–Wentzell Ch. 6; compare Candogan, Ozdaglar & Parrilo 2013 for near-potential Markov comparisons)". The proof at `theory/COADAPTATION.md:154` cites the same chapter for the tree sum, and the caveat at `:155` says "compare" Candogan, Ozdaglar, and Parrilo for near-potential Markov comparisons. The Why cell now says that.

4. **Confirmed. S11 uses \(\mathrm{Tr}(Q_{ii})/(v_i d_i)\).** `measurement/CLAIM_MAP_v2.md:625`. No correction.

   The refuted factor is \(d_i/(2\beta_i)\bigl(1+\mathrm{Tr}(Q_{ii})/(v_i d_i)\bigr)\). The same factor is the statement of CA7(4) at `theory/COADAPTATION.md:226`. The symbol \(D_i\) does not appear in S11 or in `theory/COADAPTATION.md`. The pre-existing docstring at `tools/coadaptation_checks.py:902` still writes \(D_i\); `93add78` does not touch that line, and for the scalar parties in `s8b` the computed factor \(Q_{ii}/v_i\) equals \(\mathrm{Tr}(Q_{ii})/(v_i d_i)\).

## Diff, hypothesis sentence, locked files

`git show --stat 93add78` is four files, 52 insertions and 14 deletions: `theory/COADAPTATION.md`, `measurement/CLAIM_MAP_v2.md`, `tools/coadaptation_checks.py`, `tools/test_coadaptation_checks.py`. Those are the should-fix and the three nits. `git diff --name-only c098e45 93add78` adds one further path, `reviews/coadaptation_2026-11-21/CONFIRM.md`, committed at `db47139` before the fix. A name filter of that range for prereg, lock, sha256, hash, and result is empty. The range diff contains the word "cost" and does not contain the word "bill".

The hypothesis sentence is byte-identical, bold markers included, one copy each:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`THEORY.md:41`, `CORE.md:9`, `README.md:9`, and `theory/SELECTION_AXIOMS.md:13` match `c098e45` and match `c92886a`. The copy at `theory/COADAPTATION.md:28` matches those bytes and matches `c098e45`. `93add78` does not edit that line.

## Commands and results

All repository commands were run from the repo root on `93add78`, with `nice -n 19`. `python3 -m pip install --user pytest scipy sympy` pulled NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0, and SymPy 1.14.0 (the image's NumPy was 1.26.4). Python 3.12. The limit arithmetic used `decimal` at 80 digits and an independent Moran generator; it did not import `tools/coadaptation_checks.py` until the checker run below.

- `git fetch origin main`. `origin/main` is `8e829e561aff27bcc3db0f69efd62620111f787d`.
- `nice -n 19 python3 tools/check_fresh.py`. `STATUS.md main is c92886a; window: 8e829e5 fda5557 dc7d731 c92886a 2eeab30`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP v2.72; wording FAILs 0 on 30 maintained documents; rows counted 342, tally total 342. `RESULT: PASS`. Exit 0. Two advisory length warnings (THEORY main text 10703 words, README 1468), not failures.
- `nice -n 19 python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/coadaptation_checks.py`. Exit 0 in 16.8 s. The s7c figures quoted above are that run.
- `nice -n 19 python3 -m pytest -q tools`. 198 passed, 1 skipped, in 270.20 s. Exit 0. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed. The new assertions sit inside the existing s7c test.

`git merge-tree --write-tree HEAD origin/main` reports content conflicts in `OPEN_WORK.md`, `README.md`, `STATUS.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, and `tools/test_brief.py`. The same six conflicts are reported for `c098e45` against this `origin/main`. They come from later merges on main (`fda5557`, `8e829e5`) after the first confirm's clean merge against `dc7d731`. `93add78` does not add a conflict. This pass does not rebase, and it does not merge.

## Blockers

None.

## Should-fixes

None.

## Nits

None.
