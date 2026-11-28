# Blind confirm: PR #146 after the fix and the merge of main (CONFIRM2)

**Confirmer:** independent. Wrote none of the note, the simulator, the claim-map rows, the pointer edits, the fix commit `9a92c3d`, `REVIEW.md`, or `CONFIRM.md`.
**Date:** Saturday 21 November 2026, 8:48 PM (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/146
**Head confirmed:** `cdcbe703e56f08f40b7102b15f6ee6c1e5128e32` on `drift-selection-2026-11-21`. Parents: `9a92c3d0b0a88a62a0c7caed53e58bf82edaedda` (the fix, before the merge) and `dc7d731e465e24507b84de9e7b553675ebbf1312` (`origin/main`, merge of PR #147). Draft. Not merged.

**Verdict: READY**

No blocker. `CONFIRM.md` (head `a79bcd9`, verdict NOT READY) had one false identification at `theory/DRIFT_SELECTION.md:105` and two nits, at `:23` and `:116`, and at `:128`. The fix commit `9a92c3d` changes only that file, four lines, and each of those sentences is now the statement the arithmetic supports. The merge of `dc7d731` does not disturb the version pins, the claim-map tally, or the drift-selection rows.

## Blocker — resolved

`theory/DRIFT_SELECTION.md:105`. The appositive that equated \(2NL_{\rm ad}=D/(2D_m)\) with the tracking term of DS1(b) now says that quantity "is \(\beta\) times the tracking term \(D/(2\beta D_m)\) of DS1(b) (their load is in scaled units)."

DS1(b) in one coordinate is \(1/(2\beta)+D/(2\beta D_m)\). Line 99 names the second term, \(D/(2\alpha(N-1)D_m)\). Line 33 sets \(\beta=\alpha(N-1)\), so that term is \(D/(2\beta D_m)\). Multiplying by \(\beta\) gives \(D/(2D_m)\). The same factor takes the static excess \(1/(2\beta)\) to Held's equilibrium load \(2NL_{\rm eq}\simeq 1/2\).

Re-read of arXiv:1403.1803, source `qtad_Arxive.tex`, on 22 November 2026 (UTC). The macroevolutionary line of the equation labeled `lambdastat` (displayed as 33) adds \(\upsilon\,\tau_{\rm eq}(c)\,w(c)/2\) to \(\langle\lambda^2\rangle_{\rm eq}\). The equation labeled `eq:fullload` (displayed as 52) sets \(2NL_{\rm ad}\) equal to \(c\) times that excess. The defining formula for \(\tau_{\rm eq}\) is \(1/(\mu+c\,\tilde\tau^{-1}(c))\), and the macro/micro prose states \(\tau_{\rm eq}(c)\approx 2N/(\langle\delta\rangle c)=\tilde\tau/c\) for \(c\gg 1\). With \(w(c)\to 1\), \(2NL_{\rm ad}=\upsilon\tilde\tau/2\). With the note's identifications \(D_m=\langle\Delta\rangle/(2N)\) and \(D=\upsilon_0\), \(\tilde\tau=E_0^2/D_m\) and \(\upsilon=D/E_0^2\), so \(\upsilon\tilde\tau/2=D/(2D_m)\). The displayed case of the \(\tau_{\rm eq}\) definition writes \((c\tilde\tau)^{-1}\), which is not \(\tilde\tau/c\); the fraction and the later prose are what enter the load, and they give \(\tilde\tau/c\). The macroevolutionary line of the equation labeled `adaptiveload` (displayed as 54) is \(\upsilon\tilde\tau\), twice \(\upsilon\tilde\tau/2\). The sentence's "twice that value (it drops the \(1/2\))" refers to that scaled load, not to twice the unscaled tracking term. "That value from equations 33 and 52 is DS1" is the coefficient claim the first confirm left standing. The fast-driving line \(cr^2\) is unchanged.

## Nits — resolved

1. `theory/DRIFT_SELECTION.md:23` and `:116`. Both now say a tau-leaping simulation of the lattice Moran chain, with exact Moran fixation probabilities. Line 23 adds "at most one substitution per step." The code does that: `moran_phi` is \((1-e^x)/(1-e^{Nx})\), rates are \((N/(2d))\varphi\), and a replicate steps once when a uniform draw falls under \(1-e^{-R\Delta t}\) (`tools/drift_selection_checks.py:105`–`:140`). "Exact chain" remains at `:21` and `:120` for the continuous-time process DS2 is proved for.

2. `theory/DRIFT_SELECTION.md:128`. The \(D/D_m=50\) run is the documented one: \(N=100\), \(h=1\), \(\beta h=0.02\), \(\delta=1\) (`:133` and `tools/drift_selection_checks.py:214`–`:216`). For Brownian \(Q=D\) and \(H=h\), \(\mathbb{E}[L^2]=(1+D/D_m)/(\beta h)=2550\), so the rms lag is \(\sqrt{2550}\approx 50.5\) lattice spacings. The sentence says "an rms lag of about 50 lattice spacings on that run." The table's formula on that row is 1275, which is \((1/(2\beta))(1+50)\), and \(\varepsilon_{\mathrm{lat}}=0.02\times 51=1.02\), matching the printed 1.02. "Hundreds" is gone.

The fix introduces no further claim. `git show 9a92c3d` is those four substitutions and nothing else.

## Merge of main

`cdcbe70` merges `9a92c3d` with `dc7d731`. The only path both sides changed since `c92886a` is `OPEN_WORK.md`. Against `9a92c3d` the merge changes T19 and nothing else in that file. Against `dc7d731` it changes T11 and nothing else. T11 keeps the diffusion formula and "faster than \(v_{\max}\)" (`OPEN_WORK.md:58`). T19 is main's row, including "the hypothesis at the top of CORE.md" (`OPEN_WORK.md:66`). No drift-selection sentence was dropped and no lean sentence was dropped.

Version pins. `THEORY.md:3`, `README.md:33`, `STATUS.md:3`, `STATUS.md:13`, and the v2.72 note all name CLAIM_MAP v2.72. THEORY v2.9 is unchanged. v2.71 is described as merged with PR #144; v2.72 is this branch and not merged. `STATUS.md:3` still says `main` is `c92886a`. That commit is the second of the five first-parent commits of `origin/main` `dc7d731` (`dc7d731 c92886a 2eeab30 c04cedd d34df95`). `check_fresh` passes on that window. The pointer does not call v2.72 merged and does not call v2.71 this branch.

Tally. The v2.72 note's step from v2.71 is PRIOR ART 33→34, PROVED (in-model) 95→96, OPEN 85→87, total 330→334, which is S1–S4 and no other status change. The counts table sums to 334. Lean-core added no claim-map rows. `check_consistency` reports 334 rows and tally total 334. Section S is S1 PRIOR ART, S2 PROVED (in-model) for \(|v_k|>v_{\max}\) once the lag bound is nonnegative, S3 OPEN, S4 OPEN. CX1 stays OPEN.

`check_open_work`: union missing from `OPEN_WORK.md` is 0.

## Part 2 sentence and locked files

The sentence is byte-identical to `dc7d731`, one copy each, 107 bytes including the bold markers: `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`. Text: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.` `theory/DRIFT_SELECTION.md` has zero copies (`:172`). `theory/SELECTION_AXIOMS.md` is unchanged against `dc7d731`. THEORY's only change against `dc7d731` is the claim-map pointer v2.71 to v2.72; README's only change is the same pointer; CORE adds one pointer sentence at `:102`.

`git diff --name-only dc7d731 HEAD` has no path matching `PREREG`, `LOCK`, `.sha256`, `SHA256`, `predictions.json`, or `RESULTS.md`.

## Commands and results

All from the repo root, on `cdcbe70`, with `nice -n 19`, after `git fetch origin main` (`origin/main` is `dc7d731`). NumPy 2.5.5, SciPy 1.18.1, pytest 9.2.0. SciPy, pytest, and SymPy were not installed at the start; installing them moved NumPy from 1.26.4 to 2.5.5. The quick-mode runs below are on 2.5.5. `--full` was not re-run; `results_full.json` is untouched by `9a92c3d` and by the merge.

- `nice -n 19 python3 tools/check_fresh.py`. `STATUS.md main is c92886a; window: dc7d731 c92886a 2eeab30 c04cedd d34df95`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.72; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 334 (tally total 334); process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10569 words, README 1468). `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/check_open_work.py`. `items.json not-DONE: 62; QUEUE.md not-DONE: 90; union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `nice -n 19 python3 tools/drift_selection_checks.py` (quick mode, not `--full`). Lyapunov agreement to the \(10^{-9}\) tolerance on all 20 random trials; fast-world limit and curvature cancellation OK; DS2 \(v=5\) lag slope 0.0004; DS2 \(v=12\) lag slope 2.176 against bound 2. `ALL DS CHECKS PASS`. Exit 0.
- `nice -n 19 python3 -m pytest -q tools`. `179 passed, 1 skipped in 263.04s`. Exit 0. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed`. The other test in that file passed (no forbidden token in the Lean sources, including the files the merge brought in).

## Residuals (do not block)

1. `STATUS.md:3`. `main` is named as `c92886a`. `origin/main` is `dc7d731`, one first-parent commit later. The named commit is inside the five-commit window, and the version clauses are right.
2. `OPEN_WORK.md:66`. T19 still says the lean-core extension is a draft PR, not merged, with no independent review yet. That sentence is `dc7d731`'s own text. PR #147 is that merge, and `reviews/lean_core_2026-11-21/CONFIRM.md` on it is READY. Ordinary header lag from main. It does not change section S, the tally, or T11.

## Conclusion

READY. The scaled load \(D/(2D_m)\) is \(\beta\) times the tracking term, the simulation is described as tau-leaping, and the \(D/D_m=50\) width is the rms of about 50 lattice spacings. The merge of `dc7d731` leaves the v2.72 pins, the 334-row tally, and the section S claims consistent. The Part 2 sentence matches main. Locked paths are absent from the diff. This confirm does not merge.
