# Confirm: acting loop, 22 November 2026

Verdict: **CONFIRM**

Independent recomputation of draft PR #201 at head `97052cff87eba1963074db34278baa3786222df8` on `cursor/acting-loop-f7b1`. This branch was cut from that head. The pull-request branch was not pushed to and was not merged. The arithmetic is `reviews/acting_loop_2026-11-22/recompute.py`. It does not import `theory/acting_loop_checks` or `theory/acting_memory_checks`. Closed forms were differentiated and solved here. The priced gaps were also evaluated from the state cost \(qv+\rho K^2 s+kT\,L+\alpha u_o\). The sign grid was minimized from \(A(r)/\theta+C(r)\). The Cox variance and lifetime were integrated as well as reduced to the closed forms. NumPy 2.5.5, SciPy 1.18.1, SymPy 1.14.0, and mpmath 1.3.0. Run at `nice -n 19`.

No discrepancy. Every printed 12-digit value below is the rounding of the recomputed value. The largest absolute distance from a recomputed value to the note's printed decimal is \(3.95\times 10^{-13}\), on the stake-4 gap. That is inside half a unit in the 12th place and inside the preregistration tolerance \(10^{-9}\).

## Numbers

| Quantity | Note | Recomputed |
|---|---|---|
| Full-information factor at \(a=1\), \(q=1\) | \(0.171572875254\) | \(0.171572875254\) |
| Factor at \(a=1/2\) | \(0.381966011250\) | \(0.381966011250\) |
| Factor at \(a=2\) | \(0.055728090001\) | \(0.055728090001\) |
| Priced gap at stake \(1\), \(r=1/2\) | \(-1.096373258863\) | \(-1.096373258863\) |
| Minimizing fraction at stake \(4\) | \(0.856768708291\) | \(0.856768708291\) |
| Priced gap at that fraction | \(+0.033889928154\) | \(+0.033889928154\) |
| State variance at \(K=\sqrt{2}-1\), \(p=1/2\) | \(0.853553390593\) | \(0.853553390593\) |
| Mutual-information stock, no feedback | \(0.346573590280\) | \(0.346573590280\) |
| Mutual-information stock, with feedback | \(0.267399998370\) | \(0.267399998370\) |
| Separated gain | \(\sqrt{2}-1\) | \(\sqrt{2}-1\) |
| Tight-cap gain | \(4\) | \(4\) exactly, and \(v(4)=3/5\) |
| Capped-loss derivative at the Riccati gain | \(0.189957517375\) | \(0.189957517375\) |
| Quadratic derivative at that gain | \(0\) | \(0\) |
| Tail \(P(X^2>16)\) | \(0.000014940159\) | \(0.000014940159\) |
| Second derivative at fixed \(u_o=4\) | \(-0.321714500038\) | \(-0.321714500038\) |
| Threshold where a quadratic gap flips it | \(0.160857250019\) | \(0.160857250019\) |
| Sign-grid gap at \(\theta=8\) | \(0.031682633557\) | \(0.031682633557\) |
| Sign loss under feedback | \(4.439079197657\) | \(4.439079197657\) |
| Cox posterior variance | \(1/2\) | \(1/2\) exactly |
| Cox mean lifetime | \(0.655679542419\) | \(0.655679542419\) |
| Minimum at \(b=0\) | \(J=q\theta+\gamma_1\theta\) | the same identity |

The three factors are \(3-2\sqrt{2}\), \((3-\sqrt{5})/2\), and \(1-4/(2+\sqrt{5})\), each equal to \(1-2a/(a+\sqrt{a^2+1})\) at \(q=1\), and each positive. The direct state cost reproduces both priced gaps. At stake \(1\) the bracket as \(r\to 1\) is negative, and the gap on a 199-point grid in \((0,1)\) stays negative. At stake \(4\) the cubic root is the unique root in \((0,1)\), NumPy's companion matrix agrees, and the closed-loop cost is lower at that fraction than at either neighbor. The separated-gain stationarity condition does not contain \(p\) or \(\theta\).

The mutual-information stock is \(\tfrac12\log(v/p)\) in nats. The uncontrolled value is \(\tfrac12\log 2\). The controlled value is \(\tfrac12\log(1+2^{-1/2})\). The estimate variance used for \(v\) is the Lyapunov value \(s=a(\theta-p)/(a+bK)\), which follows once the Riccati is substituted and the state-error cross moment is zero.

The capped-loss derivative was also taken by a central difference of \(\mathbb{E}[\min(X^2,1)]+K^2 s(K)\). A high-precision quadrature of that expectation agrees with the normal-cdf reduction. The tail agrees between `erfc` and SciPy's survival function, and it is below \(1/20\), so \(B=16\) does not bind.

The fixed-intensity slope recomputed with the same cost is \(1.552284749831\). The spread at half-width \(1/10\), \(\tfrac12\bigl(J(1-\delta)+J(1+\delta)\bigr)-J(1)\), is \(-0.001612560843\). SymPy's derivative of the primitive cost agrees with both. The curvature factor on the learning rate is positive and the learning rate is concave, so this fixed-intensity slice is concave for every \(\theta>0\). \(Q_{\mathrm{fin}}\) at \(r=1/2\) and memory rate \(20\) is the rational \(10/9\), and the formula does not contain \(K\).

The sign floor recomputed by minimizing \(C\) is \(4.966383544211\). \(J^*(8)\) is \(4.998066177768\). Their difference is the gap. On \(\{1/8,1/4,1/2,1,2,4,8\}\) every minimized cost is strictly above the floor and the column decreases. The sensing-alone sign loss at correlation \(1/\sqrt{2}\) is \(4\). The old sign slope plus \(1/10\) is \(-0.082159696490\), and plus \(1/2\) is \(0.317840303510\).

The Cox posterior, reweighted by \(1+x^2\) against \(\mathcal N(0,1/3)\), has variance \(1/2\) by the Gaussian moment ratio and by quadrature. The independent arm leaves the variance at \(1\). The lifetime \(\sqrt{\pi/2}\,e^{1/2}\,\mathrm{erfc}(2^{-1/2})\) agrees with a quadrature of \(\mathbb{E}[1/(1+X^2)]\), and it is larger than \(1/2\).

At \(b=0\) the variance identity \(v=\theta\) holds for every finite gain. The channel price and the actuation price are nonnegative and are zero at \(u_o=0\), \(K=0\). The minimum is \(q\theta+\gamma_1\theta\). A numerical minimization at \(q=4\), \(\theta=2\), \(\gamma_1=1/10\) lands on that value, and every sampled positive intensity or gain sits strictly above it.

## Wording

The note and T46 call the 33 lines in §5 of the preregistration evaluations of the expressions in §4, or a restatement of a sign §4 already gives, and both say this run contained no prediction that could miss. The checker has 33 `predict` calls, all named P1–P10, and it prints `CHECKS 36`, `FAILS 0`, `PREDICTION-MISSES 0`.

The extended cost is labeled a conjecture in the note and in `theory/MASTER_EQUATION_ACTING_PROPOSAL_2026-11-22.md`. Both say Theorem R1 does not carry over under A7-act. The \(b=0\) minimum is stated as the stake term \(q\theta\) when \(\gamma_1=0\), and as \(J=q\theta+\gamma_1\theta\) in general. The proposal says this is not Theorem R1 applied at \(b=0\).

\(Q_{\mathrm{fin}}\) is labeled a property of the exogenous-spring formula in Proposition AT-attain. The sentence says that formula does not cover a controlled plant.

Separation is attributed to Wonham, doi 10.1137/0306023, and the two breaks to Bar-Shalom and Tse, doi 10.1109/TAC.1974.1100635. Crossref returned HTTP 200 for both on 22 November 2026. Wonham's record is "On the Separation Theorem of Stochastic Control", SIAM Journal on Control, May 1968, no abstract. Bar-Shalom and Tse's record is "Dual effect, certainty equivalence, and separation in stochastic control", IEEE Transactions on Automatic Control, October 1974, no abstract. The note cites both for the title.

The integer \(5\%\) radius is a puzzle again. In `theory/BOUNDARY_SUFFICIENCY_2026-11-22.md` the radius-ratio row is marked **OPEN**, a puzzle, and the log-linear crossing is the next row: passed as its own statistic, with the sentence "This row is not the integer-radius puzzle." T44 says the integer ratio of \(1\) is a puzzle and that the preregistered smooth crossing is a separate statistic.

`git diff main HEAD -- THEORY.md CORE.md README.md` is empty. The hypothesis sentence is byte-identical to "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." It occurs once in `THEORY.md`, `CORE.md`, `README.md`, the acting-loop note, and the proposal. In the three maintained files those bytes are wrapped in bold markers.

`theory/acting_loop_checks/PREREG.md` is byte-identical to commit `774e88f` and still byte-identical at `d77f448`. Its sha256 is `fdf494e9b7f85ca24d9d877ea1610cbaf539dc50127a45106285165b925259a0`, which is the hash in `LOCK.txt`. `LOCK.txt` is byte-identical to `d77f448`. The lock commit is six seconds after the preregistration commit. `theory/boundary_checks/PREREG.md` is byte-identical to `f5a930e`, sha256 `58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c`. Commit `93084b0` is not an object in this clone; the note says the same bytes are `f5a930e` after the rebase, and those bytes match. `theory/boundary_checks/PREREG_CROSSING.md` is byte-identical to `8afc11f`, sha256 `05f4d12445092d90ff48cbf20985b0e358c1d46ea17e74d1f294f1064cb40ae2`.

The acting-loop note, the proposal, the acting-loop preregistration, and T46 use cost. They do not use bill, kill, or verdict. T46 is present in `OPEN_WORK.md`.

## Checks

All of these were run at `nice -n 19` from the repo root on head `97052cf`. No lake build.

| Command | Result |
|---|---|
| `python3 theory/acting_loop_checks/acting_loop_checks.py` | `CHECKS 36`, `FAILS 0`, `PREDICTION-MISSES 0`, exit 0 |
| `python3 tools/check_consistency.py` | `RESULT: PASS`. Wording FAILs 0. Two advisory length warnings (THEORY main text, README) |
| `python3 tools/check_open_work.py` | `RESULT: PASS`. Union missing from `OPEN_WORK.md`: 0 |
| `python3 -m pytest -q tools` | 261 passed, 1 skipped, 315.54 s, exit 0. The skip is `tools/test_lean.py` because lake is not installed |

A pytest launched at the repo root, rather than in `tools`, stops during collection on `reviews/night2/CAUSAL_NULL_INVARIANCE/run_test.py`, which imports `numba`. That file is not part of the maintained suite. The suite above is the one this repository's confirms run.
