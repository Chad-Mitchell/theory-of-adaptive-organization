# Independent hostile review: Shannon core (PR #139)

Reviewer: separate executor. Did not write `CORE.md`, `theory/SHANNON_2026-11-21.md`, `theory/FLUID_LAYERS_2026-11-21.md`, or `tests/LOCK1/`. Saturday 21 November 2026. Tree: `shannon-core-2026-11-21` at `7d8690ce9d58992a27c838f31fdaf61965118474`. Compute at nice 19. Nothing was edited, committed, pushed, or merged. Locked prereg files were not touched. Every DOI below was resolved on Crossref in this session.

## Verdict: NOT READY

The scalar information floor is real, the Kalman arithmetic checks out, and the 4.2% gap reproduces. The page still labels three false statements **PROVED**: the layer charge inside S1, “J* is the support function” in S2, and the Farrell product in S3 as they define it. `CORE.md` repeats the first and drops load-bearing caveats the previous one-page core was revised to carry. Fix the blockers and re-review before merge.

What survives, so the repairs stay local:

- For squared error on a scalar Gauss–Markov source, \(r \ge \tfrac12 \ln(a^2 + Q/P)\) is the sequential rate–distortion function of the current-state mse \(P\), in nats. Tatikonda, Sahai and Mitter (IEEE TAC 49:1549–1561, 2004, doi 10.1109/TAC.2004.834430) compute that SRD on the uncontrolled dynamics and state that \(\log\) is base 2. Tanaka, Kim, Parrilo and Mitter (IEEE TAC 62:1896–1910, 2017, doi 10.1109/TAC.2016.2601148) show a linear-Gaussian sensor plus a Kalman filter attains it. Stavrou, Tanaka and Tatikonda (IEEE TAC 65:2245–2249, 2020, doi 10.1109/TAC.2019.2941444) restate the scalar formula as \(\max\{0,\tfrac12\log(A^2+\Sigma_w/D)\}\). The lead-\(k\) map \(D = a^{2k}P + V(1-a^{2k})\) is algebraically right and is this note’s step. The Kalman identity \(\tfrac12\ln(P_{\mathrm{prior}}/P) = \tfrac12\ln(a^2+Q/P)\) matches the checks to \(10^{-9}\).
- The 4.2% figure is the gap of one Kalman design to that information lower bound. It is not a grid artifact.
- S3(i), read as “a minimizer at strictly positive prices is undominated,” is the standard weighted-sum fact. The Farrell arithmetic attached to it is not.
- LOCK1’s hash, lock order, and fail/pass table match the prereg and `lock1.json`.
- The fluid-layer lifetime formula matches CL19’s band and exit time. The novelty sentence over-claims a one-line corollary.
- The hypothesis sentence is verbatim in the new core and in the frozen copy.

## Blockers

**B1. S1’s layer charge is false, and a memoryless read undercuts the stated floor.**
`theory/SHANNON_2026-11-21.md:33`, `:37`, `:41`; repeated at `:7` and `CORE.md:22`.

The proof says “Any memory carrying information needs a store, so \(K \ge 1\) when \(I_{\mathrm{mem}} > 0\).” The setting defines \(M_t\) as any causal function of \(Y^t\) and sets \(A_t = g(M_t)\). Then \(M_t = Y_t\) is allowed, \(I(M_t; X^t) > 0\), and a memoryless gain is not a tracking store. \(K = 0\) is available in CT21. Their own `floor_cost` then sits strictly above this design.

Counterexample on their scalar world \(a = 0.9\), \(Q = 1\), \(k = 2\), read noise \(s^2 = 0.2\). Memoryless error \(P = 0.193\), \(I_{\mathrm{mem}} = 1.654\) nats, channel directed information \(r = 0.950\) nats, lead-2 loss \(D = 1.936\). At \(h = 1\), \(\kappa = 0.1\), \(c = 0.1\), \(w = 1\), with \(A = c\,r\) and \(L = 0\),

\[
J = 2.197 < J_{\mathrm{floor}} = 3.187.
\]

Same design at lead 0: \(J = 0.453 < 1.417\). The 36/36 check never builds a \(K = 0\) design. At \(c = 0\), `theory/shannon_checks/shannon_checks.py:114–116` sets the design cost equal to the floor.

The stock/flow split that does survive is: \(I_{\mathrm{mem}} \ge \tfrac12\ln(V/P)\) and \(r \ge \tfrac12\ln(a^2+Q/P)\) may be added, because both are lower bounds for a design that achieves \(P\). Kalman meets the second and misses the first (excess \(0.159\) nats at the worst grid point). That is why both prices open a gap. Directed information is the right causal read currency for this bound (Massey; Tatikonda; Tanaka 2017). It is not, by itself, a physical sensor bill.

Replacement for `theory/SHANNON_2026-11-21.md:31–41`:

> **Theorem S1 (information floor).** Under S-A and \(L \ge 0\), every design satisfies
>
> \[
> J(\mathcal D)\ge \kappa I_{\mathrm{mem}}+c\,r+w D\ge \min_{I,r}\{\kappa I+c\,r+w\max(D_{\mathrm{IB}}(I),D_{\mathrm{seq}}(r))\}.
> \]
>
> *Proof.* \(D\ge D_{\mathrm{IB}}(I_{\mathrm{mem}})\) and \(D\ge D_{\mathrm{seq}}(r)\) by definition of those two functions, so \(D\ge\max\). \(hK\ge 0\). Minimize over \((I,r)\). ∎
>
> The closed form on the scalar Gauss–Markov world is the same bound along the jointly tight curve \(I=\tfrac12\ln(V/P)\), \(r=\tfrac12\ln(a^2+Q/P)\), \(D=a^{2k}P+V(1-a^{2k})\):
>
> \[
> J\ge \min_P\Big\{\tfrac{\kappa}{2}\ln(V/P)+\tfrac{c}{2}\ln(a^2+Q/P)+w\big(a^{2k}P+V(1-a^{2k})\big)\Big\}.
> \]
>
> The cited SRD formula is the rate for mse \(P\) of \(x_t\) (Tatikonda, Sahai & Mitter 2004; Tanaka et al. 2017). The lead-\(k\) map is the Gauss–Markov calculation above. There is no proved \(h\cdot 1[I>0]\) term. A memoryless rule \(M_t=Y_t\), \(K=0\), has \(I_{\mathrm{mem}}>0\) and undercuts any floor that adds \(h\) (example: \(a=0.9\), \(Q=1\), \(k=2\), \(s^2=0.2\), \(h=1\), \(\kappa=c=0.1\), \(w=1\), \(J=2.197<3.187\)).

Replacement for the layer clause in `CORE.md:22`:

> memory pays for the predictive information it holds (CT1, CT4), and reads pay for at least the sequential rate–distortion rate of the accuracy reached. A layer price \(h\) is not part of that floor: a memoryless read has \(K=0\) and still carries information.

**B2. S2 calls a concave cost function the support function, and positive prices do not recover \(\mathrm{conv}\,\mathcal F_W\).**
`theory/SHANNON_2026-11-21.md:60`. `CORE.md:25` repeats “the frontier’s support function.”

In convex analysis the support function is \(\sigma_F(p)=\sup_{z\in F}\langle p,z\rangle\), and it is convex. The note defines \(J^*(p)=\min_{z\in\mathcal F_W}\langle p,z\rangle\), says this “is the support function,” and says in the same sentence that \(J^*\) is concave. Those cannot hold together. The correct identity is \(J^*(p)=-\sigma_{\mathcal F_W}(-p)\).

Positive prices recover less than the convex hull. For \(F=\{(1,1),(3,3)\}\) and \(F'=\{(1,1)\}\), \(J^*(p)=p_1+p_2\) for every \(p>0\). The dominated point is invisible. The half-spaces \(\langle p,z\rangle\ge J^*(p)\) for \(p\ge 0\) describe the free-disposal hull of the Pareto face.

The one-resource slice (directed information versus loss) is already the rate–cost function of Kostina and Hassibi (IEEE TAC 64:4525–4540, 2019, doi 10.1109/TAC.2019.2912256). The table credits that. The theorem sentence does not.

§3 of the checks tests second differences of \(J_{\mathrm{floor}}\) in \(w\). It does not test the envelope claim that the slope equals optimal loss.

Replacement for `theory/SHANNON_2026-11-21.md:60`:

> **Theorem S2.** For \(p=(\kappa,c,h,w)\) and \(J^*(p)=\inf_{z\in\mathcal F_W}\langle p,z\rangle\), one has \(J^*(p)=-\sigma_{\mathcal F_W}(-p)\), where \(\sigma\) is the support function \(\sigma(u)=\sup_z\langle u,z\rangle\). \(J^*\) is concave and positively homogeneous. Its one-sided derivative in a price, where it exists, is the optimal amount of that coordinate (envelope). Knowing \(J^*\) on the positive orthant recovers the free-disposal hull of the Pareto face of \(\mathrm{conv}\,\mathcal F_W\). It does not recover dominated points, and it does not recover \(\mathrm{conv}\,\mathcal F_W\). Equality \(J^*=\min\langle p,z\rangle\) needs \(A=c\,r\) and \(L=0\); S-A is only \(A\ge c\,r\). The read-versus-loss slice is the rate–cost function of Kostina & Hassibi 2019.

**B3. The Farrell identity, as defined, is false on the reported example.**
`theory/SHANNON_2026-11-21.md:69–73`.

Line 69 defines \(\eta_T=\min\{\theta:(\theta z,D)\text{ is reachable}\}\). The check’s radial factor is \(\theta=0.6979\). The check then sets \(\eta_T=J_{\mathrm{tech}}/J=0.9910\) and \(\eta_A=J_{\mathrm{floor}}/J_{\mathrm{tech}}=0.9943\), and reports \(\eta_C=0.9854\). The product of the cost ratios is an algebra identity. The product the definition requires is

\[
\theta\cdot\eta_A=0.6939\neq 0.9854=\eta_C.
\]

\(J=h+\kappa I+c\,r+wD\) does not scale by \(\theta\): loss is held fixed and \(h\) is not shrunk. Farrell’s product is for the cost of the inputs. On this example the input cost \(C=\kappa I+cr\) does satisfy it: \(C_{\mathrm{act}}=0.5680\), \(C_{\min}=0.3892\), technical efficiency \(\theta=0.6979\), allocative efficiency \(0.9818\), and \(\theta\times 0.9818=0.6852=C_{\min}/C_{\mathrm{act}}\).

The ruin sentence (`:77`) does not inherit (i)–(ii). A minimizer under \(P(\mathrm{ruin})\le\varepsilon\) is undominated inside the ruin-feasible set. Radial efficiency on the uncapped \(\mathcal F_W\) can be below 1 when the cheap point has a heavier tail. Part (ii) needs that restricted set to be convex. The cap is not a function of \((I,r,K,D)\) alone, and a shadow price on ruin is not one of \((\kappa,c,h,w)\). “Both statements hold within the feasible set” skips both gaps. `CORE.md:25` then drops the feasible-set qualifier.

Replacement for `theory/SHANNON_2026-11-21.md:69–77`:

> - **Technical efficiency** \(\eta_T=\theta=\min\{\theta:(\theta\cdot z,D)\text{ is reachable}\}\) (Debreu 1951; Farrell 1957).
> - **Input-cost efficiency** \(\eta_C=C_{\min}(D)/C(z)\) for \(C=\kappa I+c\,r\), the part of \(J\) that scales with those inputs.
> - **Allocative efficiency** \(\eta_A=\eta_C/\theta\).
>
> Then \(\eta_C=\theta\cdot\eta_A\) for this \(C\). It is not true of \(J_{\mathrm{floor}}/J\), because \(wD\) and an unscaled \(h\) do not shrink with \(\theta\). Worked point (`shannon_checks.py` §5): \(\theta=0.698\), \(J_{\mathrm{floor}}/J=0.985\), and \(0.698\times 0.994=0.694\neq 0.985\). On input cost, \(C_{\min}/C=0.685=\theta\times 0.982\).
>
> **Theorem S3.** (i) A design that minimizes the linear cost at strictly positive prices is undominated on that feasible set, and therefore \(\theta=1\) on that set. (ii) If the feasible set is convex, every undominated point minimizes the linear cost for some nonzero \(p\ge 0\). *Proof.* (i) A dominating design would have strictly smaller cost. (ii) Supporting hyperplane. ∎
>
> The ruin cap raises the minimum and never lowers it. (i) and (ii) apply to the ruin-feasible set only. \(\theta\) on the uncapped frontier can be below 1. (ii) needs convexity of that restricted set, which \(P(\mathrm{ruin})\le\varepsilon\) does not give, and ruin is not determined by the mean loss.

Replacement for `CORE.md:25`, second sentence of the efficiency paragraph:

> Minimizing the linear cost at strictly positive prices implies radial technical efficiency 1 on the feasible set. Under a binding ruin cap that set is the ruin-feasible set, and the cap need not preserve convexity.

**B4. The thermodynamic floors are not two separate \(kT\) charges.**
`theory/SHANNON_2026-11-21.md:29` and `:45`; `CORE.md:22`.

Sagawa and Ueda (PRL 102:250602, 2009, doi 10.1103/PhysRevLett.102.250602) prove \(W_{\mathrm{meas}}+W_{\mathrm{eras}}\ge k_BT\,I\) for one measurement’s mutual information. Measurement alone need not cost \(kT\,I\); erasure alone need not, once free-energy changes are allowed. The 2011 erratum is doi 10.1103/PhysRevLett.106.189901. Charging \(\kappa\ge kT\cdot\nu\) for erasure and \(c\ge kT\) for the read prices the sum twice. The parenthetical “for a measure-and-reset tracker, \(c\ge kT\)” is the sum, relocated onto the read price. “The only free price left is \(w\)” does not follow. S-A as “\(A\ge c\,r\) for some price \(c\)” can stay an assumption. It is not this theorem.

Replacement for the parenthetical in `theory/SHANNON_2026-11-21.md:29` and the physics paragraph at `:45`:

> **Assumption S-A:** \(A\ge c\,r\) for a price \(c\) per nat of directed information. This is an assumption, not a sensor law. Sagawa & Ueda 2009 bound the sum of measurement work and erasure work by \(kT\) times the mutual information of that measurement (erratum, 2011). They do not give a second floor \(c\ge kT\) on top of a Landauer floor on \(\kappa\).

Replacement for the physics clause in `CORE.md:22`:

> Landauer floors the erasure part of \(\kappa\). Sagawa & Ueda 2009 floor the sum of measurement and erasure work, not a separate read price stacked on that floor.

## Should-fixes

**S1. The bottom line gives lateness to this note after §1 has given it back.**
`theory/SHANNON_2026-11-21.md:13`.

Replacement:

> **What this note adds to the causal rate–distortion program is a price per layer and the ruin cap, both still without a formula for the limit.** Lateness is already the reason the rate is sequential (Neuhoff & Gilbert 1982; Tatikonda, Sahai & Mitter 2004).

**S2. “36/36 with \(\kappa=0\)” does not match the grid, and the free-read edge is assigned.**
`theory/SHANNON_2026-11-21.md:43` and `:51`; `theory/shannon_checks/shannon_checks.py:114–116`.

The grid is \(4\times 3\times 3=36\). Nine points have \(\kappa=0\). Twelve have \(c=0\), and those set \(J_{\mathrm{design}}=J_{\mathrm{floor}}\) in code. The \(\kappa=0\), \(c>0\) Kalman points do hit ratio 1.

Replacement for `:51`:

> **Memory free (\(\kappa=0\), \(c>0\)).** The Kalman filter with tuned read noise attains the read term exactly (checked to \(10^{-9}\)). On the nine \(\kappa=0\) prices the ratio is 1.0000, of which the three with \(c=0\) are assigned rather than simulated. **KNOWN** (Tanaka, Kim, Parrilo & Mitter 2017).

**S3. Scope the 4.2% before it reaches the one-page core.**
`theory/SHANNON_2026-11-21.md:53` is adequately scoped. `CORE.md:22` is not.

The rerun matches `shannon_checks.out` with an empty diff. Worst point: \(\kappa=1\), \(c=1\), \(w=1\), \(h=0.1\), \(a=0.9\), \(Q=1\), \(k=2\), efficiency \(0.9585\), gap \(4.15\%\). A 20,000-point grid gives \(0.95852\). The gap equals \(\kappa\) times excess memory (\(0.1587\) nats against \(J_d-J_f=0.1594\)). At \(h=0\) the same prices give efficiency \(0.9574\). “Within 0.3% at \(w\ge 10\)” matches the file (worst such point \(0.9978\)). Eighteen of the 36 prices have both \(\kappa>0\) and \(c>0\). One world, one lead, one \(h\).

Replacement for the last sentence of `CORE.md:22`:

> On one scalar Gauss–Markov world (\(a=0.9\), \(Q=1\), lead 2, \(h=0.1\)), the best one-layer Kalman design on a 36-point price grid stays within 4.2% of this information floor (worst point \(\kappa=c=w=1\); numerical). That is not a bound over worlds.

**S4. Put the dropped load-bearing caveats back on the page people will quote.**
The five headlines asked about are still present, in shortened form. See the comparison below. These ones are not.

`CORE.md:3`. Replacement for the “nothing was withdrawn” clause:

> The previous text is frozen at `history/2026-11-21_CORE_before_shannon.md`. Omissions from this page are compressions, not withdrawals; the operational kill rule and the Model S counterexample stay in force in the files cited below.

`CORE.md:32`, append:

> Worked rhythms counterexample: two oscillators at \(R=3\), argmin \(3\), formula \(2\); paying for a rhythm as a pair does not restore \(K^*\) (`core/KEYSTONE_NOTE.md`). The formula cannot return the \(K^*=0\) that CT21 allows. The 120/120 convexity count excludes 24 wide-search worlds still on the pre-#116 solver. IMP-N60 failed its gates (PRIMARY 58/189 cost, 51/189 composition) and is not rescued.

`CORE.md:34`, replace “Fast scales go local and slow ones shared.” with:

> At equal read quality, with shared upkeep measured in local layers, a shared layer’s worth falls as \(e^{-2\ell/\tau}\), so fast scales go local and slow ones shared (CT28, CT34). Joint value can be superadditive.

`CORE.md:47`, replace the non-move clause with the frozen rule:

> So is a design that does not move when its inputs change: a non-move is consistent only if the post-change gap \(g<\Delta_R(k_{\mathrm{lo}})\); a miss if \(g>\max(\)the static band, \(\Delta_R(k_{\mathrm{hi}}))\); INDETERMINATE between; and if the predicted gap of a non-mover is at most \(\Delta_R(k_{\mathrm{hi}})\), the move test is NOT A TEST (CT41).

`CORE.md:53`, append:

> No system has yet been shown to qualify. E. coli is the best candidate, and its \(\sigma\), \(N_e\) and \(T_{\mathrm{red}}\) are to be sourced before any rescoring.

**S5. The lifetime exponent is CL19’s arithmetic.**
`theory/FLUID_LAYERS_2026-11-21.md:13`.

CL19 (`theory/DYNAMICS.md:43–51`) already has \(b^*=(6k\sigma^2/w)^{1/4}\) and exit time \(b^2/\sigma^2\). Then

\[
\tau=b^{*2}/\sigma^2=\sqrt{6k/(w\sigma^2)}.
\]

The renewal derivation gives the same constant: accumulated loss per cycle \(w b^4/(6\sigma^2)\), average cost \(k\sigma^2/b^2+wb^2/6\), minimizer \(b^4=6k\sigma^2/w\). A cost \(100\times\) lower shortens lifetime \(10\times\), which is \(\sqrt{100}\) and is consistent with CL19’s statement that the band narrows only about \(3.2\times\). Dixit’s two 1991 papers resolve on Crossref (doi 10.2307/2298051; doi 10.1016/0165-1889(91)90037-2). CL19 says the coefficient was not re-checked against those texts. This review did not re-check them either. The formula matches CL19. It is not a new band.

Replacement for `:13`:

> **Is it more than a restatement?** The band and the exit time are CL19’s, and \(\tau_{\mathrm{layer}}=b^{*2}/\sigma^2\) is that product, so the exponent \(1/2\) is not a new derivation. The step that is new is the identification: the drifting coordinate is who shares a layer. CT14’s onset plus this lifetime is a dated prediction. A rival with no inaction band predicts no discrete re-formations; a fixed-period rival predicts no dependence on \(k\).

**S6. Prior-art table: one missing source, one mis-grouping.**
`theory/SHANNON_2026-11-21.md:12` and the sequential-RD row of the table at `:90`.

Tanaka et al. 2017 say the scalar closed form was already in the literature and that Gorbunov and Pinsker studied the closely related quantity in the early 1970s. The table starts the scalar formula at 1982/2004. Palmer et al. 2015 (doi 10.1073/pnas.1506855112) do test efficient coding of predictive information: the Crossref abstract says retinal groups are “close to maximally efficient at separating predictive information from the nonpredictive background.” Mattingly et al. 2021 (doi 10.1038/s41567-021-01380-3) say, in the Nature abstract, that cells “climb gradients at speeds within a factor of two of the theoretical bound” given the rate at which they acquire information. That is a chemotaxis performance bound. It is not Barlow’s efficient coding.

Replacement for `:12`:

> Palmer et al. 2015 test efficient coding of predictive information. Mattingly et al. 2021 test a chemotaxis bound set by information the cell acquires (within a factor of two, their abstract). Both are consistent with the technical half. Neither was preregistered here, and neither qualifies under THEORY §3.

Add to the sequential-RD row of the table: “Scalar formula older: Gorbunov & Pinsker; Bucy; restated as Tatikonda’s scalar result by Stavrou, Tanaka & Tatikonda 2020, doi 10.1109/TAC.2019.2941444.”

The rest of the table is fair. Shoval et al. 2012 (doi 10.1126/science.1217405) fit a Pareto front to phenotypes. Computing the front from the world’s statistics is a real difference, and the table says so. Sims 2003 (doi 10.1016/S0304-3932(03)00029-1) is one information price plus expected loss. Farrell 1957 (doi 10.2307/2343100) is the technical/allocative split. The package claim in `CORE.md:62` matches that reading. The sentence that does not is `:13`, fixed in S1 above.

## Nits

- Tatikonda’s \(\log\) is base 2. The note’s \(\ln\) is the nat form. Say “nats” next to the displayed formula.
- `tests/LOCK1/RESULTS.md:7` says frequencies “off by 3–66%.” The smallest relative error in `lock1.json` is \(0.0255\).
- D2 is B1 at \(K_c=0.6\) by the prereg’s own rule. The table lists it as a separate fail. The note discloses this.
- `shannon_checks.out` reports median efficiency \(1.0000\). Half the grid is an edge (\(\kappa=0\) or \(c=0\)).
- Aureli et al. 2008 is marked not re-resolved. Leave it that way.
- The PR body says `pytest tools` gave 148 passed. This environment: 147 passed, 1 skipped (`tools/test_lean.py:101`, Lean 4 / lake absent).

## Caveats: new core against `history/2026-11-21_CORE_before_shannon.md`

The required sentence is byte-for-byte in both files:

> The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.

| Asked item | On the new page? |
|---|---|
| Model S convexity is conditional and unproved | Kept (`CORE.md:32`, `:58`) |
| IMP-N60 failed | Kept as “failed its gates”; 58/189 and 51/189 dropped |
| Predictive rhythm rule open | Kept (`:32`, `:58`) |
| 30 field rows NOT A TEST (10 passed, 20 failed on proxy) | Kept (`:53`) |
| Refereed at most once, one bot family, no human | Kept (`:53`) |

Dropped from the page, still load-bearing, restored by should-fix S4: the CT41 lower-bound trichotomy; the \(R=3\) rhythm counterexample and the failed pair rescue; the formula’s inability to return \(K^*=0\); the 24 pre-#116 worlds; the equal-read-quality premise on fast/slow (CT28, CT34) and superadditivity; “no system has qualified” and the E. coli parameter hold. Cymatics (aggregate pass, 3 of 7 worlds fail) is also gone. T27 P3’s in-model failure is kept (`:39`). The revealed-prices amendment is still marked proposed, not applied (`:47`).

## LOCK1

`tests/LOCK1/PREREG.sha256` is `2f9dd21891abe4a32200876c5c12f03dc5135bb52d4ec0aba2bc2ff587e58935`. That is the sha256 of the current `PREREG.md` and of the blob in `5f9f5be` (2026-11-21 13:29:14 −0500). `git diff 5f9f5be HEAD` on the prereg is empty. That commit contains only `PREREG.md` and `PREREG.sha256`. `lock1.py` asserts the hash before scoring. Results land in `7d8690c` (13:39:21 −0500).

Scoring against the locked rules, using `lock1.json`:

| Row | Rule | JSON | Reported |
|---|---|---|---|
| A1, A2 | every matched frequency and the ratio within 5% | max errors 0.66, 0.21, 0.37; ratio errors 0.37, 0.31, 1.37 | FAIL |
| B1 | mean distance to \(p/q\), \(q\le 4\), exceeds \(r_0\) at each \(K_c\) | 0.0456, 0.0338, 0.0307 vs 0.0494 | FAIL, and closer |
| B2 | Diophantine mean at least \(1.10\times r_0\) at each \(K_c\) | +22%, +7%, +37% | FAIL at \(K_c=0.6\) |
| B3 | golden share \(\ge 0.24\), expected to fail | 0.093, 0.113, 0.000 | FAIL |
| B4 | roughness in \([0.8,1.25]\) at \(\alpha=1.0,1.4\) | 1.090, 1.053 | PASS |
| D1 | resonant frequency within 5% of 1 | 0.697 | FAIL |
| D2 | same statistic as B1 at \(K_c=0.6\) | fails | FAIL |

B4’s roughness ratio is the Part A statistic in `theory/spacing_checks/antilock.py`, rerun at the locked alphas. `osc_world` sets the pole real part to \(\zeta\omega\) with \(\zeta=0.05\), which is the locked “\(\alpha=0.05\cdot\omega\).”

`RESULTS.md:21` says the coordinating agent withdrew cases (a) and (c) after the run as unable to fail informatively, and that the rows were not withdrawn. No separate message from that agent is in the repo. The git order is consistent with the claim: the lock commit has no runner and no results; the results commit is ten minutes later; the fails are still in the table. “Unable to fail informatively” here means an optimizer shortfall was not ruled out (`RESULTS.md:20`), which is the right weakness, and they left the fails scored.

## Checks

| Command | Result |
|---|---|
| `nice -n 19 python3 theory/shannon_checks/shannon_checks.py` | exit 0, stdout identical to `shannon_checks.out`, `ALL PASS`. Minimum efficiency \(0.9585\). |
| `nice -n 19 python3 tools/check_consistency.py` | `RESULT: PASS` (0 fails; 23 frozen-record INFO) |
| `nice -n 19 python3 tools/check_open_work.py` | `RESULT: PASS` (union missing from `OPEN_WORK.md`: 0) |
| `nice -n 19 python3 -m pytest tools -q` | 147 passed, 1 skipped (`test_lean.py:101`, Lean 4 / lake not installed). Scipy and sympy were installed in this environment first; the skip is the missing Lean binary. |

## DOIs resolved on Crossref for this review

Tatikonda, Sahai & Mitter 2004, 10.1109/TAC.2004.834430. Tanaka, Kim, Parrilo & Mitter 2017, 10.1109/TAC.2016.2601148. Kostina & Hassibi 2019, 10.1109/TAC.2019.2912256. Stavrou, Tanaka & Tatikonda 2020, 10.1109/TAC.2019.2941444. Sagawa & Ueda 2009, 10.1103/PhysRevLett.102.250602. Sagawa & Ueda erratum 2011, 10.1103/PhysRevLett.106.189901. Farrell 1957, 10.2307/2343100. Shoval et al. 2012, 10.1126/science.1217405. Palmer, Marre, Berry & Bialek 2015, 10.1073/pnas.1506855112. Mattingly, Kamino, Machta & Emonet 2021, 10.1038/s41567-021-01380-3. Sims 2003, 10.1016/S0304-3932(03)00029-1. Dixit 1991, 10.2307/2298051 and 10.1016/0165-1889(91)90037-2.
