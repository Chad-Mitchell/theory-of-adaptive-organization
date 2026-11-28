# Confirm of draft PR #166

**Verdict: CONFIRMED-WITH-NITS.**

**Confirmer:** independent of the note, of section X, and of the READY-WITH-FIXES review. Wrote none of `theory/GROWTH_BRIDGE.md`, `tools/growth_bridge_checks.py`, or `reviews/growth_bridge_2026-11-22/REVIEW.md`.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/166
**Head confirmed:** `4d0b418c85889ba12596ef5445e5db19cd9ca41e` on `growth-bridge-2026-11-22`. The repair commit is `4d0b418` on top of `0d50e2f`, which is the head PR #167 reviewed. This branch does not edit that head. Do not merge.

The hostile review (PR #167, `reviews/growth_bridge_2026-11-22/REVIEW.md` on `review-pr166-2026-11-22`) returned READY-WITH-FIXES with eight should-fixes and no blocker. The checklist below was read off the files at `4d0b418`, not off the PR description. Every displayed number named in the confirm request was recomputed separately, at 80 decimal places, before the author's suite was run.

Two nits, both in the checker. Neither one restores a should-fix, flips a row, or changes a printed digit. They are listed at the end.

---

## What was read

`theory/GROWTH_BRIDGE.md` at `4d0b418`, CLAIM_MAP section X and the v2.81 note, the tally table, `OPEN_WORK.md` T33, `STATUS.md`, `THEORY.md` (the version pointer, the growth-bridge paragraph, and the hypothesis sentence), `CORE.md` (the hypothesis sentence), `reference/CHANGELOG.md` (the two v2.81 bullets), `tools/growth_bridge_checks.py`, and `git diff origin/main...4d0b418`. The READY-WITH-FIXES review was read in full from `origin/review-pr166-2026-11-22`.

`origin/main` after `git fetch origin main` is `2d9a8125f7f55eb55416a1af2680edabc5046c81`. `lake build` was not run.

---

## Recomputation

Independent of `tools/growth_bridge_checks.py`. Decimal arithmetic at 80 places. The B9 roots are Newton on the numerator of \(\theta'\), and again Newton on \(\theta(\tau)-\theta_{\mathrm{req}}\). Poisson extinction probabilities are Newton on \(\eta=\exp(m(\eta-1))\), then checked against the script's own 100,000-step iteration. A printed value below is the correct rounding of the recomputed value to the printed scale.

**Galton–Watson chain.** Drop the \(O(s^3)\) term. The displayed chain is

\[
f(1-s)=1-ms+\frac{\beta_2}{2}s^2,
\qquad
s=ms-\frac{\beta_2}{2}s^2,
\qquad
s(m-1)=\frac{\beta_2}{2}s^2.
\]

For \(s\neq 0\) the last display is \(s=2(m-1)/\beta_2\). Substituting that value back into \(s=ms-(\beta_2/2)s^2\) leaves a residual of \(0\) (checked at \(m=1.01\), \(\beta_2=1.7\)). The predecessor the review rejected, \(s=(m-1)s+(\beta_2/2)s^2\), leaves a nonzero residual at the same point. At \(m=1\), \(f''(1)=\mathbb{E}[W(W-1)]=\mathrm{Var}(W)+m^2-m\) collapses to \(\mathrm{Var}(W)\), so \(\beta_2=\mathrm{Var}(W)\) at criticality.

Poisson survival over \(2(m-1)\), Newton:

| \(m\) | Ratio | Rounds to |
|---|---|---|
| \(1.001\) | \(0.998668220506\) | \(0.9987\) |
| \(1.01\) | \(0.986820521980\) | \(0.9868\) |
| \(1.05\) | \(0.937018370729\) | \(0.9370\) |

The script's iteration reaches the same four decimals (`theory/GROWTH_BRIDGE.md:162`).

**Mean gap, equal-mean growth, Kelly.**

| Quantity | Recomputed | Printed |
|---|---|---|
| \(\lambda_B=0.525\log 1.2+0.475\log 0.8\) | \(-0.01027436955742\ldots\) | \(-0.010274369557\) |
| \(\mathbb{E}[X_B]=2\cdot 0.525-1\) | \(0.05\) | \(0.05\) |
| mean excess \(\varepsilon\mathbb{E}[X_B]\) at \(\varepsilon=0.2\) | \(0.01\) | \(0.01\) |
| \(\tfrac12\log 0.96\) | \(-0.020410997260\ldots\) | \(-0.020411\) |
| Kelly derivative at \(f=0.2\) | \(0\) exactly | \(f^\star=0.2\) |
| \(\lambda(0.2)=0.6\log 1.2+0.4\log 0.8\) | \(0.0201355135507\ldots\) | \(0.020135513551\) |

The derivative identity \(0.6/(1+f)=0.4/(1-f)\) is \(f=0.2\) with no remainder. For \(Z=\pm 1\) with equal probability, \(\mathrm{Var}(W)=\sigma^2\Delta t\) exactly, because the cross term with \(\mathbb{E}[Z]\) vanishes and \(\mathbb{E}[Z^2]=1\). At \(\Delta t=10^{-4}\), \(\mu=0.2\), \(\sigma^2=0.5\), the realized growth rate is \(-0.04999824998\ldots\), which rounds to the printed \(-0.049998\). The limit is \(-0.05\).

**Truncations, checked as arithmetic.** First order, \(\varepsilon\mathbb{E}[X]\): the equal-mean pair (design \(X=0\) against \(X=\pm 1\)) and the third-moment pair (both means \(0\)) are ties; the mean-gap pair is ranked by the excess \(0.01\). Second order, \(\varepsilon\mathbb{E}[X]-(\varepsilon^2/2)\mathbb{E}[X^2]\): the equal-mean pair separates (\(0\) against \(-\varepsilon^2/2\)), and the third-moment pair ties because both second moments equal \(1\). The masses \(4/9,4/9,1/9\) on \(-1,1/2,2\) have mean \(0\), second moment \(1\), and third moment \(1/2\) as exact fractions. The growth gap is \(1.90598441269\ldots\times 10^{-5}\), which rounds to the printed \(1.905984\times 10^{-5}\).

**Rises.** Each is \(\exp\) of the printed log-offspring.

| Map | From | To |
|---|---|---|
| \(W=\exp(-e^{-2I})\), \(I=0\to 1\) | \(0.36787944117144\ldots\) | \(0.87342301849312\ldots\) |
| \(\log W=-r-4e^{-r}\), \(r=0\to 1\) | \(0.01831563888873\ldots\) | \(0.08445657646560\ldots\) |
| \(\log W=-4e^{-a}\), \(a=0\to 1\) | \(0.01831563888873\ldots\) | \(0.22957677710030\ldots\) |

All six round to the printed twelve digits. The acquisition derivative \(-1+4e^{-r}\) is positive on \([0,\log 4)\), and \(\log 4>1\), so the step from \(r=0\) to \(r=1\) is still on the rising side. The learning cell names offspring \(1.1\) at loss \(0\) and offspring \(3\) at loss \(1\). It prints no third number.

**Tau table.** User order is increasing \(\tau\): \(\tau_S\), \(\tau_{\mathrm{cap}}\), \(\tau_G\), \(\tau_J\), \(\tau_E\).

| Label | Newton / closed form | Printed |
|---|---|---|
| \(\tau_S\) | \(0.23620752672208\ldots\) | \(0.236207526722\) |
| \(\tau_{\mathrm{cap}}\) | \(0.29904973348823\ldots\) | \(0.299049733488\) |
| \(\tau_G\) | \(0.30266809926050\ldots\) | \(0.302668099260\) |
| \(\tau_J\) | \(0.30967983510774\ldots\) | \(0.309679835108\) |
| \(\tau_E=\sqrt{0.1}\) | \(0.31622776601684\ldots\) | \(0.316227766017\) |

\(\tau_G\) is the positive root of \(\tau^4+\tau^2-0.1=0\). The residual at the closed form \(\sqrt{(-1+\sqrt{1.4})/2}\) is \(0\) at this precision. \(\phi'(\tau_G)=0\), and \(\phi''<0\) on \(\tau>0\), so it is the maximum. The numerator of \(\theta'\) changes sign once on the positive-margin interval \((0.0513167019495,\,1.9486832980505)\). \(J(\tau_J)<J(\tau_G)\) and \(\phi(\tau_G)>\phi(\tau_J)\). Under the published requirement \(\theta\ge\log(1000)/0.5=13.815510557964\ldots\), both \(\tau_G\) and \(\tau_E\) lie to the right of \(\tau_{\mathrm{cap}}\), and \(\tau_S\) lies inside \([\tau_{\mathrm{lo}},\tau_{\mathrm{cap}}]\).

---

## The eight should-fixes

1. **Galton–Watson chain.** `theory/GROWTH_BRIDGE.md:142–160`. The proof now runs \(f(1-s)=1-ms+(\beta_2/2)s^2+O(s^3)\), then \(s=ms-(\beta_2/2)s^2+O(s^3)\), then \(s(m-1)=(\beta_2/2)s^2+O(s^3)\), then \(s\sim 2(m-1)/\beta_2\). Line 160 states the criticality identity. The quadratic truncation gives that asymptotic exactly, as recomputed above. GB4 stays **PROVED (in-model)**.

2. **Mean-gap label.** `theory/GROWTH_BRIDGE.md:102–108`, `measurement/CLAIM_MAP_v2.md:710`, `tools/growth_bridge_checks.py:125–144`. The heading is "a mean gap". The cell states \(\mathbb{E}[X]=0.05\), excess \(0.01\), \(\lambda_B=-0.010274369557\), and the separate equal-mean growth \(-0.020411\). The same paragraph states the two truncations as recomputed above, and says the weak-selection menu of Theorem GB-menu is a different limit. The checker asserts \(\mathbb{E}[X]=0.05\), the excess, the twelve-digit growth, and \(\tfrac12\log 0.96\). GB3 stays **FALSE**.

3. **H3 is the partial.** `theory/GROWTH_BRIDGE.md:237–251` and `measurement/CLAIM_MAP_v2.md:713`. The table's left column holds the other bads fixed. Memory, acquisition, and attention have partials \(-\kappa\), \(-c\), and \(-c_a\), strict at a positive price. The three rises sit in the total-derivative column and match the recomputation. The learning step from offspring \(1.1\) to offspring \(3\) is in that same column (`:247`). Expected task loss is LY-1, \(\tfrac12\log 0.2=-0.804718956\) against \(\log 1.1=0.095310180\), both of which round correctly. A scalar ruin probability is described as a functional of the law (`:248`): constant \(W=1.2\) does not move with the probability, and \(W=0\) breaks positivity. Line 251 keeps "from first principles" false. GB6 stays **FALSE**.

4. **No leading bar.** `theory/GROWTH_BRIDGE.md:70` is the line `\mathbb{E}[\log W]`. The display at `:69–72` is \(\mathbb{E}[\log W]=\mathbb{E}[W-1]-\mathrm{Var}(W)/2+O((\Delta t)^{3/2})\). Line 67 states \(\mathrm{Var}(W)=\sigma^2\Delta t\) exactly for \(Z=\pm 1\).

5. **Second-moment bound.** `theory/GROWTH_BRIDGE.md:98`. The proof names \(\mathbb{E}[X_i^2]\le(\mathbb{E}|X_i|^3)^{2/3}\le M^{2/3}\). Lyapunov's inequality is that comparison of \(L^p\) norms. The difference of growth rates is then at least \(\varepsilon\gamma-\varepsilon^2 M^{2/3}-(16/3)\varepsilon^3 M\): the \(\varepsilon^2\) coefficient is \(|\mathbb{E}[X_1^2]-\mathbb{E}[X_j^2]|\le 2M^{2/3}\), and the two Lagrange remainders contribute at most \((16/3)\varepsilon^3 M\). Dividing by \(\varepsilon\) sends the correction to \(0\). The bound is valid, and the theorem follows.

6. **Prior art stays prior art.** `theory/GROWTH_BRIDGE.md:273–290`. The list under "Known, and not claimed as new" contains Kelly's stake, Taylor's theorem (`:278`), and the extinction and hitting formulas (Haldane, Feller, Iglehart, Cramér, `:283–286`). The additions paragraph names the separation of the two limits, the squared-mean obstruction, \(\tau_G\) and the split cap, and the coordinate audit, and then says the Kelly stake, the Taylor expansion, and the extinction and hitting formulas are the prior art in §7.

7. **Half-space caveat on GB4.** `measurement/CLAIM_MAP_v2.md:711`. The row says birth-death, Feller, and Brownian level sets are exact half-spaces, that the Galton–Watson half-space in \((m-1,\beta_2)\) exists only after the linear approximation, and that the B9 preimage in \(\tau\) is a bounded interval. The note says the same at `:162` (linear approximation), `:170` (birth-death half-space), `:182` (Feller), `:194` (Brownian), and `:218–221` (bounded interval \([\tau_{\mathrm{lo}},\tau_{\mathrm{cap}}]\)). The recomputed interval is that one. GB4 stays **PROVED (in-model)**.

8. **T33.** `OPEN_WORK.md:81`. The assumptions sentence is "The term list, the cap, and H3 remain assumptions." The next sentence is "GB2 is a false unscoped identity." GB2 is outside the assumptions list. GB7 is described as not a preregistration and not a lock.

---

## Labels

Read from the status column at `4d0b418`.

| Row | Line | Status | Matches the proof |
|---|---|---|---|
| GB1 | `measurement/CLAIM_MAP_v2.md:708` | **PROVED (in-model)** | Menu ranking and \(\mu-\sigma^2/2\), with the second-moment bound named |
| GB2 | `:709` | **FALSE** | Deterministic \(W=1.2\): \(\log 1.2=0.182321556794\), dropped term \(0.02\) |
| GB3 | `:710` | **FALSE** | Diffusion sign flip and the Kelly pair; the mean-gap example is labeled as a mean gap |
| GB4 | `:711` | **PROVED (in-model)** | Chain, exact half-spaces, linearised Galton–Watson plane, bounded \(\tau\) interval |
| GB5 | `:712` | **FALSE** | Slack cap leaves \(\tau_G\neq\tau_E\); split cap leaves \(\tau_J\neq\tau_G\) |
| GB6 | `:713` | **FALSE** | Partials are the budget map; the rises and the learning step are total derivatives |
| GB7 | `:714` | **OPEN** | No locked preregistration (`theory/GROWTH_BRIDGE.md:296`) |

The v2.81 note (`measurement/CLAIM_MAP_v2.md:86`) states the same seven statuses. The tally arithmetic there is \(371\to 378\), PROVED \(124\to 126\), OPEN \(93\to 94\), FALSE \(0\to 4\). The table at `:720–738` sums to \(378\): OPEN \(94\), PROVED \(126\), FALSE \(4\), and the remaining statuses. `tools/check_consistency.py` counts \(378\) rows and the same tally.

---

## Master equation, prior art, version, hypothesis, barred words

**The master equation is not claimed as derived.** The places that name a derivation say the opposite. `theory/GROWTH_BRIDGE.md:39`: "This note does not derive it either." `:259`: "The master equation is not derived, and it is not derived in either limit." `:265` stamps the package sentence false. `:9` says the term list and the cap are inputs, so the equation remains an assumption outside the scoped ranking. `THEORY.md:39` points at the note and repeats that split. `measurement/CLAIM_MAP_v2.md:86` and `:704` say the equation stays an assumption. `reference/CHANGELOG.md:5` says the master equation is not that limit. `OPEN_WORK.md:81` keeps the term list, the cap, and H3 as assumptions.

What §3 and Theorem GB derive is the argmax agreement on a gapped finite menu, and the limit \(\mu-\sigma^2/2\). Line 216 calls \(\phi\) the diffusion limit of a multiplicative factor with the path's margin and variance rate, and says the additive reserve's drift is \(y-J\). That sentence is about \(\phi\), and the following sentences keep the master equation as a further input.

**Textbook results are credited.** Section 7 heads the list "Known, and not claimed as new." The additions paragraph (`:290`) puts the Kelly stake, Taylor's theorem, and the extinction and hitting formulas back into that section. The new sentences are the separation of the two limits, the squared-mean obstruction, \(\tau_G\) and the split cap, and the coordinate audit.

**CLAIM_MAP v2.81 matches STATUS.** `STATUS.md:3` and `:13`, `THEORY.md:3`, and `measurement/CLAIM_MAP_v2.md:86` all name v2.81. The STATUS sentence, the section X preamble (`:704`), and `THEORY.md:39` use the same four clauses: on a gapped finite menu, weak selection recovers the ranking only; the diffusion limit keeps \(\mu-\sigma^2/2\); an interior stake separates the argmaxes; the term list and the cap are inputs. T33 adds that H3 remains an assumption, which is also `theory/GROWTH_BRIDGE.md:263` and the GB6 row.

**Hypothesis sentence.** One occurrence in each file, and the three occurrences are the same byte string:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`theory/GROWTH_BRIDGE.md:11`, `THEORY.md:41`, `CORE.md:9`.

**Barred words.** The note contains no `bill`, no `kill`, no `verdict`, and no `theory of everything` (substring scan, and the checker's scan). The new sentences in T33, the v2.81 note, section X, the STATUS growth-bridge sentence, and the two changelog bullets contain none of those four. The THEORY header line that moved from v2.80 to v2.81 still carries the pre-existing clause "verdict NOT READY" (`THEORY.md:3`). That clause was already on the line. This PR's edit of the line is the version number.

---

## Commands

Run from the repository root on `growth-bridge-2026-11-22` at `4d0b418`, after `git fetch origin main`. `origin/main` is `2d9a812`. Pytest was not installed in the image; `pytest`, `scipy`, and `sympy` were installed for the suite only. The repository files were not changed by that install. Lake was not built.

| Command | Result |
|---|---|
| `git fetch origin main` | exit 0. `origin/main` is `2d9a8125f7f55eb55416a1af2680edabc5046c81` |
| `python3 tools/check_consistency.py` | `RESULT: PASS`, FAIL 0, 378 rows, tally 378 |
| `python3 tools/check_fresh.py` | `RESULT: PASS`. STATUS's `main` is `01e4415`, inside the window `2d9a812 01e4415 2dd04fa 37794bb f84997c` |
| `python3 tools/check_open_work.py` | `RESULT: PASS` |
| `python3 tools/growth_bridge_checks.py` | `FAILS 0`, `ALL GROWTH-BRIDGE CHECKS PASS`, exit 0 |
| `nice -n 19 python3 -m pytest -q tools` | `252 passed, 1 skipped in 301.78s`, exit 0. The skip is `tools/test_lean.py:101`, "Lean 4 / lake is not installed." |

---

## Nits

Neither nit is a wrong digit, a wrong label, or an open should-fix.

1. `tools/growth_bridge_checks.py:165–168`. The check named "gapped menu" asserts \(\log 1.01\in(0.009,0.01)\). It compares no second design. The review listed this. The repair left it. The menu argument that carries the theorem is the proof at `theory/GROWTH_BRIDGE.md:98`.

2. `tools/growth_bridge_checks.py:372–373`, `:387–388`, `:391`, `:400`, and `:407–408`. The acquisition partial check is `-1.0 < 0`, the learning check is `3.0 > 1.1`, the ruin check is `1.2 == 1.2`, and the attention partial check is `-0.4 < 0`. The memory partial check evaluates a finite difference the test itself wrote. Any of these passes if the corresponding sentence in the note is changed. The rises (`:368`, `:382`, `:405`) and LY-1 (`:396`) are real comparisons, and they match the recomputation. `theory/GROWTH_BRIDGE.md:303` says the script checks the budget partials. Those five checks do not read the partial sentences. The partials in the note are the derivatives of \(-\kappa I-\ell\), \(-cr-\ell\), and \(-c_a a-\ell\).
