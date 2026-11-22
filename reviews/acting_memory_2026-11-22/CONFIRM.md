# Confirm: acting memory, 22 November 2026

**CONFIRM WITH NITS**

Independent recomputation of draft PR #197 at head `33f9acaf8a59f64b2405f818497d4c96cf6b35f8` on `acting-memory-2026-11-22`. That branch was not pushed to, and nothing was merged. The recomputation is `reviews/acting_memory_2026-11-22/recompute.py`. It does not import `theory/acting_memory_checks/acting_checks.py`. It was run with `nice -n 19` and printed `ALL_MATCH`.

Every load-bearing number in the note matches this recomputation at the digits the note prints. The one nit is the commit ids named by the lock. `LOCK.txt`, the note, and OPEN_WORK row T45 name preregistration `06976862` and lock `4d74bd52`. Those objects are absent from this repository. The commits that are present put the preregistration and the lock before the first result commit, and the bytes of `PREREG.md` are the locked bytes.

## Numbers

The cost is the capped sign cost in the note and in `PREREG.md` §4,

\[
J(r,\theta)=\alpha\cdot\frac{2a(1-r)}{\theta r^2}+kT\,a\frac{1-r}{r}+w\psi(r),
\]

with \(\psi(r)=\arccos\sqrt{1-r}/\pi\), \(a=kT=1\), \(w=16\), and \(\alpha=(4-\pi)/(6\pi)\). Pi is the Brent–Salamin AGM, and it agrees with \(4\arctan 1\) through 40 digits. Each reported minimum was found by bisection of \(\partial J/\partial r\) and, at the same \(\theta\), by a derivative-free golden search. The two agree through 30 digits on the locked grid, at the spread points \(\theta=0.9\) and \(\theta=1.1\), and at \(\theta=1\). The along-path split is the derivative of \(A(r)/\theta\), of the heat, and of \(w\psi(r)\) through \(r^*(\theta)\). Those analytic derivatives agree with a Richardson finite difference through 20 digits, and their sum is \(-A(r^*)/\theta^2\).

`erfc(1)` is the power series for the error function. It agrees with `mpmath.erfc(1)` through 30 digits. \(\Phi^{-1}(0.975)\) was obtained by Newton on that series, and it equals \(\sqrt{2}\,\mathrm{erfcinv}(1/20)\) and `mpmath`'s \(\sqrt{2}\,\mathrm{erfinv}(0.95)\) through 25 digits. The admissible squared costs were minimized from the derivative in \(p\) and checked by a golden search on the same closed interval \(p\le\min(\theta,p_{\mathrm{cap}})\).

The note's printed digits are the rounding of the longer value. The difference column is recomputed minus the note, at the note's printed place.

| quantity | note | recomputed | difference |
|---|---|---|---|
| \(J(1/2,1)\) | 5.182159696490 | 5.182159696490108457 | \(+1.1\times 10^{-13}\) |
| \(\mathrm d J^*/\mathrm d\theta=-A(r^*)/\theta^2\) | −0.182159696490 | −0.182159696490108457 | −1.1×10⁻¹³ |
| along-path probe | −0.130861161564 | −0.130861161564238662 | −2.4×10⁻¹³ |
| along-path heat | +0.187741986525 | +0.187741986525379694 | +3.8×10⁻¹³ |
| along-path sign | −0.239040521451 | −0.239040521451249489 | −2.5×10⁻¹³ |
| \(J^*(\theta=1/8)\) | 5.911577251205 | 5.911577251205079685 | +8.0×10⁻¹⁴ |
| \(J^*(\theta=8)\) | 4.998066177768 | 4.998066177767839751 | −1.6×10⁻¹³ |
| \(\mathrm d^2 J^*/\mathrm d\theta^2\) | 0.313020858054 | 0.313020858054347120 | +3.5×10⁻¹³ |
| re-optimized spread, half-width 1/10 | 0.001577268119 | 0.001577268119290591 | +2.9×10⁻¹³ |
| admissible squared, \(\theta=1/2\) | 5.316961792302 | 5.316961792302381049 | +3.8×10⁻¹³ |
| admissible squared, \(\theta=1\) | 8.000711319618 | 8.000711319618255211 | +2.6×10⁻¹³ |
| admissible squared, \(\theta=2\) | 13.186217779633 | 13.186217779632865694 | −1.3×10⁻¹³ |
| admissible squared, \(\theta=4\) | 23.557230699662 | 23.557230699662086659 | +8.7×10⁻¹⁴ |
| naked-option slope at \(\theta=1\) | −0.199471140201 | −0.199471140200716339 | +2.8×10⁻¹³ |
| \(\mathrm{erfc}(1)\) | 0.157299207050 | 0.157299207050285131 | +2.9×10⁻¹³ |
| learning rate at \(u=4\), \(\theta=4\) | 2.372281323269 | 2.372281323269014330 | +1.4×10⁻¹⁴ |
| \(\inf C\) | 4.966383544211 | 4.966383544210638638 | −3.6×10⁻¹³ |
| crossing of 5 | 7.5267230646 | 7.526723064585407051 | rounds to the quoted ten digits |
| \(p_{\mathrm{cap}}\) | 0.260317771627 | 0.260317771627005669 | +5.7×10⁻¹⁵ |
| \(\Phi^{-1}(0.975)\) | 1.959963984540 | 1.959963984540054236 | +5.4×10⁻¹⁴ |
| \(\mathrm{erfcinv}(1/20)\) | 1.385903824350 | 1.385903824349677945 | −3.2×10⁻¹³ |

The note's "near \(\theta=7.5267\)" is the same root to four decimals. At that root, \(J^*=5\) to the working precision. The slope at fixed \(u=4\) and \(\theta=4\) is \(+0.177466031352467229\), which is positive, and the fraction there is \(0.296535165408626791\).

Two identities hold exactly, to the series precision. \(\psi(1/2)=1/4\), so one decision loses 16 with probability \(1/4\). The loss is in \(\{0,16\}\), so \(P(\mathrm{loss}>16)=0\). The fixed-intensity heat slope at \((u,\theta)=(4,1)\) is the fraction \(2/3\). The second-derivative sign reduces to \((4-\pi)(44+\pi)>0\).

The rest of the locked grid matches the same way: \(r^*\) and \(J^*\) at \(\theta\in\{1/4,1/2,2,4\}\) round to the note's table, the fixed-fraction spread rounds to \(0.001839996934\), the diagnostic location of \(\inf C\) rounds to \(0.441594095399\), and the shortfall \(5-J^*(8)\) rounds to \(0.001933822232\).

No number in this table disagrees with the note.

## Preregistration order

`PREREG.md` at HEAD has sha256 `bdf86e0379297c84f59856261419e66286c8c3b3f48ce24e8e22fd7812ddd4b8`. The same digest is the blob at the preregistration commit, at the lock commit, at the result commit, and at HEAD. `git diff 0f452d5 HEAD -- theory/acting_memory_checks/PREREG.md` is empty. The sentence in §5 P3 is still there: the rightmost grid value is strictly above 5.

The parent chain of `33f9aca` is:

| order | commit | author date | what it adds |
|---|---|---|---|
| preregistration | `0f452d5cf5bb2a9ff5ff4566cf980dbb9116ef47` | 2026-11-22T20:55:49Z | `PREREG.md` only |
| lock | `e95b6be76f7b560cfc883a8b1623733322f039c4` | 2026-11-22T20:55:53Z | `LOCK.txt` only |
| first result | `dbec42668fd5ecdb3d0ef3f2897b17bb5aa5ab01` | 2026-11-22T21:16:00Z | the note, the script, `results.out`, `crossref.out`, the test, the T45 row |
| wording | `33f9acaf8a59f64b2405f818497d4c96cf6b35f8` | 2026-11-22T21:43:10Z | the note and the T45 row |

The result commit is a descendant of the lock, which is a descendant of the preregistration. The preregistration and the lock are above the first result in that chain.

`git cat-file -t 06976862d850363c4f2fc5690c8fc4f20e3c984d` fails, and `4d74bd52` is not a commit. No commit in `git log --all` has either prefix. `LOCK.txt` still says the preregistration commit is `06976862d850363c4f2fc5690c8fc4f20e3c984d`. The note's preamble and OPEN_WORK T45 repeat `0697686` and `4d74bd5`. The author dates are in the order above. The committer dates of `0f452d5`, `e95b6be`, and `dbec426` are the same later instant, 2026-11-22T21:36:40Z, which is the mark of a rewrite that left the names inside `LOCK.txt` behind.

The miss is reported and the prediction is unchanged. The result commit's note already contains the heading "The grid clause against 5. MISSES." with the value \(4.998066177768\), the shortfall \(0.001933822232\), and the diagnosis that \(C(1/2)=5\) is an upper bound on \(\inf C\). The later commit keeps that miss. `results.out` prints `PREDICTION-MISS  P3 rightmost grid cost above 5`. A fresh run of `acting_checks.py` at `nice -n 19` prints the same line, then `CHECKS 54`, `FAILS 0`. The test `tools/test_acting_memory_checks.py` requires that line.

## Wording

The note's opening states the scored action: "The scored action is an open-loop intensity. The world equation contains no action." Assumption AM-X repeats that no action enters \(dX=-aX\,dt+\sqrt{2a\theta}\,dW\).

The level drop is given as two routes. Section 0 separates "a shrinking price for a loss that depends on \(\theta\) only through the error fraction \(r\)" from "a capped premium on an expectation that grows with \(\sqrt{\theta}\), with no channel." Section 5's "Two routes" keeps the same split: the envelope identity for the probe price of a fraction, and a capped premium on \(\mathbb{E}[\max(X,0)]\) with no channel and no heat.

The variability sentence is present twice: "a random spread of the variance hurts."

A whole-word search of the note for `kill`, `verdict`, and `bill` is empty. OPEN_WORK row T45 is present, and that row is empty of those three words. The objective is named cost throughout.

The hypothesis sentence is byte-identical in `CORE.md`, `THEORY.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`, one copy each, including the bold markers:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`git diff b6e351e HEAD` does not touch those four files. `b6e351e` is the parent of the preregistration commit.

Friston, FitzGerald, Rigoli, Schwartenbeck, and Pezzulo, doi `10.1162/NECO_a_00912`, Crossref HTTP 200, title "Active Inference: A Process Theory". The abstract's premise is that all neuronal processing and action selection can be explained by minimizing variational free energy, and the abstract asks whether neuronal responses can be described as a gradient descent on that free energy. The note reports that split and says this page minimizes heat, probe price, and the sign loss.

Russo and Van Roy, doi `10.1287/opre.2017.1663`, Crossref HTTP 200, title "Learning to Optimize via Information-Directed Sampling". The abstract says each action is sampled to minimize the ratio between squared expected single-period regret and the mutual information between the optimal action and the next observation. The note keeps the word single-period.

The other six DOIs also returned HTTP 200 on 22 November 2026, with the titles the note uses. Horowitz and Esposito, `10.1103/PhysRevX.4.031015`, "Thermodynamics with Continuous Information Flow". Taleb and Douady, `10.1080/14697688.2013.800219`, "Mathematical definition, mapping, and detection of (anti)fragility". Chaloner and Verdinelli, `10.1214/ss/1177009939`, "Bayesian Experimental Design: A Review"; the abstract presents the design problem as one decision-theoretic problem. MacKay, `10.1162/neco.1992.4.4.590`, "Information-Based Objective Functions for Active Data Selection"; the abstract discusses objective functions that measure the expected informativeness of candidate measurements. Lindley, `10.1214/aoms/1177728069`, "On a Measure of the Information Provided by an Experiment", no abstract in the record. Bar-Shalom and Tse, `10.1109/TAC.1974.1100635`, "Dual effect, certainty equivalence, and separation in stochastic control", no abstract in the record.

## Checks

Run at `nice -n 19` from this head. No `lake` build.

| command | result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT: PASS. FAIL 0. Claim-map rows 392, tally 392. Advisory length warnings on THEORY and README |
| `python3 tools/check_open_work.py` | RESULT: PASS. Missing from OPEN_WORK: 0 |
| `python3 theory/acting_memory_checks/acting_checks.py` | CHECKS 54, FAILS 0, and the P3 line is `PREDICTION-MISS` |
| `python3 -m pytest -q tools` | 259 passed, 1 skipped, 395.41 s, exit 0. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed |

The tools run used pytest 9.2.0, NumPy 2.5.5, SciPy 1.18.1, and SymPy 1.14.0. The recomputation's Gaussian-tail cross-check used mpmath 1.3.0. The digits in the table are the series and the closed forms.

## Nit

The content lock holds: the sha256 of `PREREG.md` is the digest in `LOCK.txt`, and that file is unchanged from the preregistration commit through this head. The commit ids in `LOCK.txt`, in the note's preamble, and in OPEN_WORK T45 do not resolve. Replacing those three names with `0f452d5` and `e95b6be` would make the lock point at the commits that are actually in the history. That edit is a new line in the lock's own terms, so it is left as a nit rather than done here.
