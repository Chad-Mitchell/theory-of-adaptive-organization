# Confirm of draft PR #161

**Verdict: CONFIRMED-WITH-NITS.**

**Confirmer:** independent of the note and of the NOT-READY review. Wrote none of `theory/GENERAL_FORM.md`, section W, or `reviews/general_form_2026-11-22/REVIEW.md`.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/161
**Head confirmed:** `6600eb8c1e5c2b5b360e6d23cfd153cbe0caad9f` on `general-form-2026-11-22`. Parent is `a6a7c7c` (the head PR #163 reviewed). This branch does not edit that head. Do not merge.

The hostile review (PR #163, `reviews/general_form_2026-11-22/REVIEW.md`, head `a6a7c7c`) returned NOT-READY on two blockers and five should-fixes. The repair commit `6600eb8` answers those points. The checklist below was read off the files at that commit, not off the PR description. The description on GitHub still summarizes the pre-repair draft (CLAIM_MAP v2.79, and retention-maximizing designs placed on the front). That text is not in the tree at `6600eb8`.

Two nits, neither of which restores a blocker. They are listed at the end.

---

## What was read

`theory/GENERAL_FORM.md` at `6600eb8`, CLAIM_MAP section W and the v2.80 note, the V5 row, `OPEN_WORK.md` T32, `STATUS.md`, `THEORY.md` (the version pointer, the hypothesis sentence, and CT14–CT16), `README.md`, `theory/SELECTION_AXIOMS.md` (the hypothesis sentence), `reference/CHANGELOG.md` (the v2.80 and v2.79 bullets), `tools/general_form_checks.py`, and `git diff origin/main...6600eb8`. The NOT-READY review was read in full from `origin/review-pr161-2026-11-22`.

`origin/main` after `git fetch origin main` is `37794bbb269027fb7ef5b18b7908bc42d989fbba`. `lake build` was not run.

---

## 1. Lemma LY, the corollary, the trichotomy, occupation

**The lemma is proved.** H1–H3 are stated at `theory/GENERAL_FORM.md:48`. Lemma LY (`:52–54`) says that \(z\le z'\) and \(z\neq z'\) imply \(\lambda(z)>\lambda(z')\), and that every maximizer of \(\lambda\) is Pareto.

The comparison is the chain of one-coordinate decreases. H3 says that for almost every environment, offspring is strictly decreasing in each coordinate and \(W>0\). If the vectors differ in several coordinates, each one-coordinate step is a strict decrease on a conull set, the intersection of finitely many conull sets is conull, and at least one step is strict, so \(W(z,\omega)>W(z',\omega)\) almost surely. The written sentence names a single coordinate. The chain is what makes the several-coordinate case the same inequality. \(\log W(z)-\log W(z')\) is then nonnegative and not almost surely zero. H2 makes both logarithms integrable, so the difference is integrable, and the expectation of a nonnegative integrable random variable that is not almost surely zero is positive. A strictly dominated design therefore has a strictly smaller exponent and cannot maximize \(\lambda\).

Existence is a separate sentence (`:56`): on a nonempty compact design set, a continuous \(\lambda\) attains its maximum, and that maximizer is Pareto. Finiteness of the design set is not used for the comparison. Compactness of the image is F-0, and GF-1(i) (`:93`) keeps it separate.

**The corollary is a linear cost in growth units.** Corollary LY-c (`:58–62`) assumes \(\log W=-\langle c(\omega),z\rangle\) with \(c(\omega)\ge 0\) almost surely and \(\mathbb{E}[c_i]>0\) on each charged coordinate, and concludes \(\lambda(z)=-\langle\mathbb{E}[c],z\rangle\). Nonnegative \(c_i\) with finite means are integrable, so the interchange is linearity of expectation. Lines 11, 64, and 66 say this cost is in growth units and is not the master equation. Line 66 says the corollary may look like a derivation of \(J=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb{E}[\ell]+A+L\), and that it is a derivation of \(\langle\mathbb{E}[c],z\rangle\) for a \(z\) supplied from outside. Risk-neutral currency and the half-space cap stay in GF3. The lineage under this map minimizes one priced point (`:64`). It does not sit on an unranked front.

One sentence in that paragraph overreaches. It is Nit 1. It does not turn the corollary into the master equation.

**The trichotomy is correct** (`:81–85`).

1. Under H1–H2, \(\lambda\) is a complete preorder and the selected set is \(\arg\max\lambda\), which may be one point.
2. Under H1–H3, \(\lambda\) satisfies S-M+. An observer who knows the values selects \(\arg\max\lambda\). An observer who knows only S-M+ cannot rule out a Pareto point. The witness \(\lambda(z^\star)=0\) and \(\lambda(z)=-1-\sum_i\exp(z_i)\) for every other feasible \(z\) satisfies S-M+ and selects \(z^\star\). If \(a\le b\) and \(a\neq b\): the case \(b=z^\star\) does not arise, because a Pareto point is undominated; the case \(a=z^\star\) gives \(0>\lambda(b)\); if neither is \(z^\star\), the constant cancels and the exponential sum is strictly larger at \(b\), because the exponential is strictly increasing and at least one coordinate has increased. The front is the union of those argmax sets. A deterministic \(W=\exp(r)\) realizes the witness as an exponent on a finite feasible set. The same construction, applied to a dominated point, would violate S-M+. The note restricts it to Pareto points.
3. S-P produces the viable set and does not rank designs inside it.

**Occupation is not claimed as proved.** Line 9, line 84, line 87, and line 261 say occupation of the front is not a theorem under H1–H3, and that H3 is not derived from copying. GF1's claim cell and Why cell (`measurement/CLAIM_MAP_v2.md:693`) say the same. The FALSE list (`theory/GENERAL_FORM.md:109`) does not stamp "selection alone forces a complete preorder" false. It scopes that sentence to the exogenous regime, where it is \(\lambda\), and to frequency-dependent copying, where LY-2 and the cycle apply.

---

## 2. Recomputation

Independent of `tools/general_form_checks.py`, with `Decimal` at 50 places and exact fractions.

**LY-1.** Two states, probability \(1/2\). Design L has offspring \(4\) and \(0.05\). Design H has offspring \(1.1\) and \(1.1\).

\[
\lambda_L=\tfrac12\ln(0.2)=\tfrac12\ln(4\cdot 0.05)=-0.804718956217\ldots
\]

which rounds to nine decimals as \(-0.804718956\).

\[
\lambda_H=\ln 1.1=0.095310179804\ldots
\]

which rounds to nine decimals as \(0.095310180\).

The absolute gaps to the printed nine-decimal values are about \(2.2\times 10^{-10}\) and \(2.0\times 10^{-10}\). Both sit inside the script's tolerance \(5\times 10^{-10}\). L's expected bads \((1,0)\) are strictly smaller than H's \((2,0.4)\), and \(\lambda_L<\lambda_H\). Both offspring numbers are positive. The state-contingent log-offspring vectors \((\ln 4,\ln 0.05)\) and \((\ln 1.1,\ln 1.1)\) are incomparable: the first coordinate favors L and the second favors H.

**LY-2.** Row payoffs: A against A is \(1\), A against B is \(0\), B against A is \(3\), B against B is \(1/2\). At frequency \(x\) of B,

\[
f_A=1-x,\qquad f_B=3(1-x)+\tfrac12 x=3-\tfrac52 x,\qquad f_B-f_A=2-\tfrac32 x.
\]

The printed expression \(2-1.5x\) is that difference. It equals \(2\) at \(x=0\) and \(1/2\) at \(x=1\), and it is at least \(1/2\) on \([0,1]\). The replicator derivative of \(x\) is \(x(1-x)(f_B-f_A)\), which is positive on \((0,1)\). The strictly dominated type B goes to fixation. The invasion gap at \(x=0\) is \(2\).

**The cycle.** If A beats B, B beats C, and C beats A, each by a strict margin when the loser is common, three real numbers \(\lambda_A,\lambda_B,\lambda_C\) cannot represent those invasions: a cycle of strict inequalities cannot hold among three reals. The regime is nonempty. The payoff matrix with rows \((0,1,-1)\), \((-1,0,1)\), \((1,-1,0)\) has A invading B, B invading C, and C invading A. The note's remark is this impossibility. It does not assign a frequency-independent scalar, and it does not claim that the exogenous case fails to emit \(\lambda\).

---

## 3. The relaxation certificate

The false inference is gone from the three places the repair had to clear.

- `theory/GENERAL_FORM.md:210` says excess over the relaxation does not certify a miss of the achievable set, and that a miss needs an achievable dominator or a bound proved tight. The rigid shift at `:222` is the counterexample: a translate by \(0.4\) nats sits inside the relaxation and is undominated in itself. Line 226 says the sketch does not treat excess over the relaxation as a miss. GF5 stays a sketch.
- CLAIM_MAP GF5 (`measurement/CLAIM_MAP_v2.md:697`) is **OPEN**. The cell says excess over the Gauss–Markov relaxation does not certify a miss, and quotes the same rigid-shift reason. The worked point is arithmetic.
- `OPEN_WORK.md:80` says GF5 is not a relaxation certificate, not a preregistration, and not a lock.

The v2.79 changelog bullet (`reference/CHANGELOG.md:5`) still summarizes that superseded draft, including interiority against a computed front. The v2.80 bullet directly above it says the repair replaces that claim and that excess over the relaxation is not a miss. The live rows do not carry the certificate.

---

## 4. The five should-fixes

| Fix | Where it stands |
|---|---|
| Floors separated from bads; V5 stays OPEN | `theory/GENERAL_FORM.md:111–133`. A floor mentions a slot. Retention decreases in a slot only under H3, and that decrease is not proved. Attention is not a derived bad (`:127`). Layer count is a bad only under an extra monotonicity (`:129`). V5 stays OPEN (`:113`, `:133`). The V5 row (`measurement/CLAIM_MAP_v2.md:684`) is still **OPEN**. GF2 (`:694`) states the same split and the same open status. |
| \(N^\star(\rho)\) on the scalar-cost list, with the drift ratio | The row is in the second table of §6 (`theory/GENERAL_FORM.md:202`), under "Needs a stake, a price ratio, or a scalar cost" (`:188`). The cell says \(\rho=q_g/q_u\), shared drift intensity over private drift intensity, and that the telling threshold \(d/c\) of CT16 is a different ratio. This matches `THEORY.md:351` and the square-root formula \(N^\star=(\sqrt{1+\rho}+1)^2/\rho\) at `THEORY.md:353`. GF4's cell (`measurement/CLAIM_MAP_v2.md:696`) names the same ratio. |
| Unweighted Chebyshev is weakly monotone | `theory/GENERAL_FORM.md:161`. \(\max(0.6,0.6)=\max(0.6,0.5)\). The S-M+ witness on the three-point set is \(r(C)=0\), \(r(A)=r(B)=-1\). On that set no pair is ordered by the product order, so every ranking satisfies S-M+. The augmented score is stated for larger sets. The script checks the weak-monotonicity equality (`tools/general_form_checks.py:246–247`). |
| Barred phrase gone | `theory/GENERAL_FORM.md` does not contain the barred name. The diff of `origin/main...6600eb8` does not add it. The ideal-gas comparison at `:22` is a comparison of extra assumptions with a linear formula. |
| T32 does not say the form is derived | `OPEN_WORK.md:80`. The status cell says the lemma is proved in-model, occupation of the front is not proved, and GF5 is not a preregistration. The state column is "needs reviewer". The word "Derived" is not in the row. |

---

## 5. Overclaim scan

Added lines in `git diff -U0 origin/main...6600eb8` were scanned for a claim that selection forces or derives the Pareto front, or that the master equation is derived.

What remains is scoped.

- The opening heading is "The derived form" (`theory/GENERAL_FORM.md:7`), and the header says the note derives the weaker object of which the additive equation is a special case (`:3`). The next paragraphs condition that object on H1–H3, call the front an identified set, and say occupation is not proved (`:9`). Line 87 says H3 is not derived from copying. Line 255 says the packaging is not a derivation of additive \(J\) from persistence.
- "S-P forces the Pareto front" is stamped false, with the viable pair (`:109`).
- The changelog's v2.80 bullet says Lemma LY replaces the claim that selection forces the Pareto front (`reference/CHANGELOG.md:3`).
- STATUS's new sentence says v2.80 adds the Lyapunov lemma (`STATUS.md:3`). It does not say selection occupies the front.

No added line says the master equation is derived. The places that name it say it is a further special case under risk-neutral expected currency, a half-space cap, and linear nonnegative prices (`theory/GENERAL_FORM.md:13–20`, `:137`; CLAIM_MAP `:689` and GF3).

The GitHub description of PR #161 was not updated. It still says CLAIM_MAP v2.79 and that coordinatewise strict monotone retention puts every retention-maximizing design on the Pareto front. The head does not say that. The description is not a file in `6600eb8`.

---

## 6. Labels, version, hypothesis sentence, barred words

| Row | Status | What the text at `6600eb8` proves |
|---|---|---|
| GF1 | PROVED (in-model) | Lemma LY under H1–H3, the log-linear cost in growth units, the trichotomy as a classification, and LY-1, LY-2, and the cycle. Occupation is excluded in the same cell. |
| GF2 | PROVED (in-model) | The mention-audit and the negative claims. The decrease of retention is stated as not proved. V5 stays OPEN. |
| GF3 | PROVED (in-model) | The conditional reduction to nonnegative additive \(J\) with a ruin cap. The dent, Kelly, and Lundberg are the witnesses that each extra assumption is doing work. |
| GF4 | PROVED (in-model) | A scope list. No new inequality. \(N^\star\) is charged to \(\rho=q_g/q_u\). |
| GF5 | OPEN | Antitone-cloud arithmetic, the rigid shift, and a sketch. Not a certificate and not a lock. |
| V5 | OPEN | Unchanged. Hypothesis F. |

The v2.80 note (`measurement/CLAIM_MAP_v2.md:86`) says no row outside section W changes status, the five status words are unchanged, the claims are narrowed, and the tally stays 371. `tools/check_consistency.py` counted 371 rows and matched the tally. STATUS, THEORY, README, `theory/README.md`, `tools/test_brief.py`, and the changelog all point at v2.80. THEORY stays v2.9.

The hypothesis sentence is 103 bytes, one copy each, byte-identical, in `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`, and `theory/GENERAL_FORM.md:24`:

`The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`

`theory/GENERAL_FORM.md` contains neither "bill" nor "kill", and it does not contain the barred name. Section W and the T32 row do not contain them. The diff does not add them.

---

## Nits

**Nit 1.** `theory/GENERAL_FORM.md:64` says the Pareto front is the set of points that some nonnegative price vector could have selected. Every minimizer of a nonnegative nonzero price is weakly Pareto. The converse needs a supporting price. Section 5 (`:149–161`) says convexity produces that price, and that \(C=(0.6,0.6)\) is Pareto on \(\{A,B,C\}\) and minimizes no nonnegative inner product: the two ratio bounds are \(p_1/p_2\le 2/3\) and \(p_2/p_1\le 2/3\), and \((2/3)^2=4/9<1\). So \(C\) is on the front and no nonnegative price selects it. The displayed equality \(\lambda(z)=-\langle\mathbb{E}[c],z\rangle\), the statement that this cost is in growth units, and the statement that it is not the master equation are unaffected. GF1's claim cell does not repeat the equality. The repair is to restrict that one sentence to the convex case, or to call the price-selected set the supported subset of the front.

**Nit 2.** `theory/GENERAL_FORM.md:269` says `tools/general_form_checks.py` checks the S-M+ ranking that selects \(C\). The script checks that \(C\) uniquely minimizes unweighted Chebyshev (`:118–119`) and that unweighted Chebyshev is weakly monotone (`:246–247`). It does not evaluate \(r(C)=0\), \(r(A)=r(B)=-1\). The ranking itself is correct on \(\{A,B,C\}\): no pair is ordered by the product order, so S-M+ holds for every assignment, and this assignment selects \(C\).

---

## Commands and results

Run from `/agent/repos/theory-of-adaptive-organization` at `6600eb8`, after `git fetch origin main`. `origin/main` is `37794bbb269027fb7ef5b18b7908bc42d989fbba`. `nice -n 19` was used. `lake build` was not run.

| Command | Result |
|---|---|
| `git fetch origin main` | `origin/main` = `37794bb`. STATUS's `eddf64e` is the fourth first-parent commit of that tip. |
| `nice -n 19 python3 tools/check_consistency.py` | `FAIL: 0`. Tally 371. `RESULT: PASS`. Exit 0. Advisory length warnings on THEORY and README, not failures. |
| `nice -n 19 python3 tools/check_fresh.py` | Window `37794bb f84997c 32cc8e0 eddf64e 886d69b`. `RESULT: PASS`. Exit 0. |
| `nice -n 19 python3 tools/check_open_work.py` | Union missing from `OPEN_WORK.md`: 0. `RESULT: PASS`. Exit 0. |
| `nice -n 19 python3 -m pytest -q tools` | `251 passed, 1 skipped` in 302.38s. Exit 0. |
| `nice -n 19 python3 tools/general_form_checks.py` | `FAILS 0`. `ALL GF CHECKS PASS`. Exit 0. Printed growth `lam_L=-0.804718956217`, `lam_H=0.095310179804`. Invasion gaps `[2.0, 1.625, 1.25, 0.875, 0.5]`. |

The two blockers from PR #163 are closed on this head. The five should-fixes are in the note and in section W. The two nits above are local. They do not return the occupation claim or the relaxation certificate.
