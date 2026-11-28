# Preregistration: BICAUSAL Route A follow-up: is the two-way coupling one object, and is a link paid as heat?

*Friday 27 November 2026 (America/New_York). Branch `bicausal-a-2026-11-27`, cut from `main` `dd4c3f93d66c1c1a16f0e4ca76792c4e141ef0b7`. Locked before any scored run: this file, `PREREG.sha256`, the check scripts in `checks/`, and the outputs of their toy-input runs (`checks/toy_checks.out`, `checks/paper_approx.out`) go in one commit, which is pushed before the run (`process/PREREG_GATE.md` section 2, launch rule). Nothing scored below is computed before that commit and a committed gate read. The scored runs start from a fresh GitHub clone at the lock commit, at nice 19. `THEORY.md`, `CORE.md` and the earlier two-route locks are not edited by this file. No real-world data. Deviations go in `DEVIATIONS.md` in this folder, appended lines only.*

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

(Byte for byte from `CORE.md:7`.) Labels: **HYPOTHESIS** is a bet locked here. **OBSERVED** is on `main` at `dd4c3f93d66c1c1a16f0e4ca76792c4e141ef0b7`, with a file and line. **PAPER** is a value or identity worked out before any scored run (by hand, or by the committed script `checks/paper_approx.py` on an approximate formula that is not the scored model).

## 0. Scope, sources, and what the brief asked

The brief asked for the most assumption-deleting physics step, named as BICAUSAL Route A items A-T1 and A-T3, on the premise that if Route A holds, the link price \(L\) and the read price \(A\) become heat and only the stake \(w\) and the ruin cap stay assumed. Read against the sources:

- OBSERVED. `CORE.md:42`: \(A\) "Stays assumed as a separate summand. A continuous coupling's read is inside \(\dot Q\)." `CORE.md:43`: \(L\) "Stays assumed, and stays outside the heat-plus-stake sum." `CORE.md:155` lists deriving the stake, the link price or the ruin cap from the heat bound as open. `THEORY.md:32-33` define \(A\) (per read, per nat, or per unit precision) and \(L\) (\(\kappa_b\) per member–level link, \(d\) per member told, \(u\) per lookup). `theory/INFO_PHYSICS_ATTAINABILITY.md:41` states the physical frontier with "ruin and linking left outside".
- OBSERVED. Route A as locked does not address \(L\) or \(A\). A-T1 asks whether the two-bath account of T61, the design-level response (CA1, COAD-F3, COAD-F4) and a finite boundary are one object (`theory/two-route-2026-11-25/PREREG.md:69-79`). Its v1 iff was split into identities (A-C4) and unscored deliverables (`PREREG_2.md:33-39`); its scored successor A-T1‴ is a `boundary-hit` open miss (`RESULTS.md:38`, `:54`). A-T3 (the CL11 cold-bath lever) was retired before any run as ill-posed: with the friction lever free there is no minimizer, and with it fixed the elasticity is RI's \(-1/2\) on paper (`PREREG_2.md:41-47`, `:107`); a CL11 test needs a world whose noise is not thermal.
- So this prereg does two things. **Route A proper:** it scores the one-object question in W2 directly (BA-T1), closes the A-T1‴ next test on paper (BA-C1), and leaves A-T3 retired (no new CL11 family is proposed here). **The step the brief meant:** it puts a link inside the heat account in a named physical class and scores the one number that a free link price leaves undetermined, the member count at which a shared level beats separate trackers (BA-T2). \(A\) is not re-derived: a continuous read is already heat (`CORE.md:42`), and a priced discrete read is outside this prereg.

**Named rivals.** RI (Sims 2003, doi `10.1016/S0304-3932(03)00029-1`, `theory/two-route-2026-11-25/crossref.out`) is silent on both scored numbers (per-party RI is the Nash map, `PREREG_2.md:57`). The rivals are named per bar below.

**What this prereg does not promise.** No area cap, no holography, no quantum or gravitational claim, no force. No real system. No statement about \(w\) or the ruin cap. A hit on either bar changes a status only after an independent review.

## Gate

| ID | Label | G1 miss (honest odds) | G2 not an identity (paper attempt) | G3 rival: same quantity, its value, gap, resolution | G4 reach | G5 next step |
|---|---|---|---|---|---|---|
| BA-C1 | **CONSISTENCY_CHECK** (not run; gate: none (CONSISTENCY_CHECK)) | — | Fails G2: with the stop-copying limit added to the memory's design set, the A-T1‴ values follow from logged numbers (§1) | — | — | Logged only; the A-T1‴ next test carries about 0 information and is not locked |
| BA-C2 | **CONSISTENCY_CHECK** (run only as a code gate in BA-T2) | — | Fails G2: a level plus one linked member is a two-coordinate memory of \(X\); its total heat is at least the Kalman rate at the member's decision error (§3.3), so at \(K=1\) pooling never beats the direct infimum | — | — | Code gate: a \(K=1\) per-member cost below the direct infimum by more than \(10^{-9}\) fires `measurement/code` and BA-T2 is not scored |
| **BA-T1** | **TEST** | Miss if W2 with both bath heats, at the `PREREG_4.md` stakes, is a weighted potential game at any of \(w_x\in\{0.5,1,2\}\). Odds of a miss 0.15 | Whether the cross-partials of \(J_m\) and \(J_w\) in the designs are proportional everywhere is not computed anywhere; `PREREG_4.md:16` calls the game non-potential without a proof. No paper shortcut: \(\Sigma\) is a rational function of \((a,g,\gamma,c)\) and the cross-partials do not factor by inspection | **One-object reading** (CA1 / `CORE.md:127`: Boltzmann over designs iff the beta-scaled game is an exact potential): a weighted potential exists. The two outcomes are exclusive; resolution is exact (rational arithmetic) | (b) `CORE.md:127`; `measurement/CLAIM_MAP_v2.md:921` (BICAUSAL) | Hit: BICAUSAL gets its counterexample: W2 meets S1, S3, S4, S5 of `PREREG.md:71` and is not one object; the settling question moves to strong monotonicity (CA5), not a potential. Miss: write the potential \(\Psi\) for W2 and state BICAUSAL as a scoped theorem |
| **BA-T2** | **TEST** | Miss if \(\hat K^*(w)\notin[12,48]\) at any \(w\in\{3,10,100\}\) (§3.5). Odds: hit 0.40; miss low (below 12) 0.30; miss high (49–128) 0.15; none up to 128 at some \(w\) 0.05; mixed across \(w\) 0.10 | Exact optimum over four design numbers of a three-coordinate linear system; no closed form. PAPER (§3.4, approximate member heat): \(\hat K^*\approx 32, 24, 24\) at \(w=3,10,100\) | **Free-link reading** (the five-term display with \(L=0\)): \(\hat K^*=2\). **Copy-costs-a-read null** (a link costs a member at least the heat of reading the world at the same error): no \(K\le128\). Gaps to the band: 10 and 80 grid steps of \(K\). Resolution: one grid step, checked by a half-tolerance rerun | (b) `CORE.md:43`, `:155` | Hit: in class LINK the link is paid as heat with a derived threshold; state it in the `CORE.md` §1 table after review, then test a second class (two-state jumps). Miss low or high: report \(\hat K^*\) and the direction; the PAPER member heat was wrong in that direction; next is the exact member infimum. None up to 128: the copy-costs-a-read null stands in this class up to 128 members |

**Gate summary (self-check; a separate gate read is required before any run, §5).** Two TESTs, each against a rival that predicts the same quantity. Two identities, labeled and not scored. Reach level (b) for both TESTs, cited to `CORE.md` lines.

## 1. BA-C1: the A-T1‴ next test, on paper (CONSISTENCY_CHECK, not run)

`RESULTS.md:49` names the next test: a memory design set that includes the stop-copying limit as an attainable point. Add the blind memory \(m\equiv0\) (the limit \(\gamma\to\infty\), \(c\to0\) of W2, `RESULTS.md:38`). OBSERVED identities on W2 (`theory/two-route-2026-11-25/PREREG.md:56-62`, `PREREG_4.md:31-35`), with \(a=D=D_M=1\), \(w=w_w=10\):

- At \(m\equiv0\) the world is the equilibrium OU process: \(\Sigma_{xx}=D/a=1\) and \(\dot Q_X=a^2\mathbb E[x^2]-aD=0\) for every \(g\). So \(J_m=w+w_x\) and \(J_w=w_w+w_x\), and the world is indifferent to \(g\).
- `RESULTS.md:38` logs \(J_m=10.5035\) on the \(\ln\gamma=5\) edge and \(10.50004\) at \(\ln\gamma=9\), falling to \(10+w_x\) at \(w_x=0.5\). So at those \(g\) the blind memory is the memory's best reply, and every \((m\equiv0,g)\) in that set is a Nash point with \(J_{\mathrm{tot}}=w+w_w+2w_x\).
- PAPER: \(G=21/14.0087-1=0.4991\) at \(w_x=0.5\) and \(22/16.1186-1=0.3649\) at \(w_x=1\) (joint minima from `RESULTS.md:38`); the interior point at \(w_x=2\) is unchanged, \(G=0.0654\). The pattern is the `sensitivity-dependent` branch of `PREREG_4.md:63`.

These values follow from logged numbers, so the test carries about 0 information. It is logged here and not run. The Nash set is a continuum in \(g\), which is itself a statement about W2: once the memory stops copying, the world's copy gain is unpriced.

## 2. BA-T1 (TEST): is W2 with both bath heats one object?

**Model.** W2 exactly as locked (`theory/two-route-2026-11-25/PREREG.md:55-59`), costs exactly as `PREREG_4.md:31-35`:

\[
J_m=\dot Q_M+w\,\mathbb E[(x-m)^2]+w_x\,\mathbb E[x^2],\qquad J_w=\dot Q_X+w_w\,\mathbb E[(x-gm)^2]+w_x\,\mathbb E[x^2],
\]

with \(\dot Q_M=\gamma^2\mathbb E[(m-cx)^2]-D_M\gamma\) and \(\dot Q_X=a^2\mathbb E[(x-gm)^2]-aD\) (energy units, \(kT_X=D\), \(kT_M=D_M\)). The memory's design is \((\gamma,c)\), the world's is \(g\), on the open domain \(\gamma>0\), \(gc<1\).

**One object.** `PREREG.md:73` defines it as a design distribution \(\propto e^{-\Psi}\) for one potential \(\Psi\) built from the stationary heats and losses. Under the CA1 substitution chain that holds iff the beta-scaled game is an exact potential (`CORE.md:127`; `PREREG_2.md:37`), that is, iff the game is a weighted potential game with positive weights \((\lambda_m,\lambda_w)\) (Monderer and Shapley 1996, *Games Econ. Behav.* 14:124–143, doi `10.1006/game.1996.0044`, checked on Crossref 27 Nov 2026, `crossref.out` in this folder). For \(C^2\) costs on a simply connected domain this holds iff

\[
\frac{1}{\lambda_m}\frac{\partial^2J_m}{\partial\theta_k\,\partial g}=\frac{1}{\lambda_w}\frac{\partial^2J_w}{\partial\theta_k\,\partial g}\quad(k=\gamma,c)\ \text{everywhere}.
\]

So with \(P_m=(\partial_\gamma\partial_gJ_m,\partial_c\partial_gJ_m)\) and \(P_w\) likewise, a weighted potential needs \(\Delta=P_{m,1}P_{w,2}-P_{m,2}P_{w,1}\equiv0\) and a constant positive ratio \(P_w/P_m\).

**Scored.** For each \(w_x\in\{0.5,1,2\}\) at \(a=D=D_M=1\), \(w=w_w=10\): the outcome is `no-weighted-potential` if an exact rational point of the domain has \(\Delta\neq0\) (or a ratio that varies, or is not positive), else `potential`. The symbolic \(\Sigma\) and the test are in `checks/ba_t1_sym.py`; the scored run is `checks/ba_t1.py`. **HYPOTHESIS:** `no-weighted-potential` at all three. **Miss** if `potential` at any of them; size: which \(w_x\), and the ratio \(\lambda_w/\lambda_m\). Odds of a miss 0.15. **Reported, not scored:** \(w_x=0\); heats only (\(w=w_w=w_x=0\)); all parameters free; \(P_m\), \(P_w\) and \(\Delta\) at the logged A-T1‴ interior Nash point and at the PAPER joint minimum at \(w_x=1\).

A witness with \(\Delta\neq0\) in exact arithmetic is a proof that no positive weights exist at that setting (a computer-algebra proof, not Lean).

## 3. BA-T2 (TEST): a link paid as heat, and the member count at which a shared level pays

### 3.1 Class LINK

Linear additive-noise diffusions, every bath at one temperature, \(kT=1\); each memory coordinate's mobility is a design number, so its noise \(D_i\) is free (the convention of `theory/INFO_PHYSICS_ATTAINABILITY.md` §4, where the heat of a coordinate with force \(f_i\) is \(\dot Q_i=\mathbb E[f_i^2]/D_i+\mathbb E[\partial_if_i]\) in units of \(kT\)). The world is the exogenous equilibrium OU signal, \(f_X=-aX\), \(D_X=av\), with \(a=v=1\). A **level** \(M_0\) reads the world, \(f_0=-b_0(M_0-X)\), noise \(D_0\). A **linked member** \(M_1\) reads only the level, \(f_1=-b_1(M_1-M_0)\), noise \(D_1\). A **direct member** reads the world, \(f_1=-b_1(M_1-X)\). Gains are set to 1 without loss of generality (rescaling a coordinate rescales its noise and leaves every heat and decision error unchanged). Each member decides alone from its own state; its loss is its decision error \(\varepsilon_1=\mathbb E[\mathrm{Var}(X\mid M_1)]\) (the decision error of `theory/INFO_PHYSICS_ATTAINABILITY.md:25`). The process is bipartite (no two coordinates share a noise), so each bath's heat is that coordinate's own and the world's bath gets none (\(\dot Q_X=0\), checked).

\(K\) members share one level; members are conditionally independent given \((X,M_0)\), so the per-member cost is

\[
P_K=\frac{\dot Q_0}{K}+\dot Q_1+w\,\varepsilon_1 .
\]

The comparator is the **direct infimum**, the proved frontier over all bipartite memories of the OU signal (IP11, `theory/INFO_PHYSICS_ATTAINABILITY.md:41-47`): \(J_{\mathrm{dir}}(w)=2\sqrt{kT\,a\,v\,w}-kT\,a\) for \(w\ge kTa/v\).

**Units.** \(kT\,a\,v\,w\) has units \((\text{energy})(\text{time}^{-1})(x^2)(\text{energy}\,\text{time}^{-1}x^{-2})=(\text{energy}/\text{time})^2\), so \(J_{\mathrm{dir}}\) is an energy rate, as are \(\dot Q_0/K\), \(\dot Q_1\) and \(w\varepsilon_1\).

### 3.2 PAPER: the level's heat in closed form

With \(M_0=\int_0^\infty b_0e^{-b_0s}X_{t-s}\,ds+N_0\), \(N_0\) the level's own OU noise of variance \(D_0/b_0\), the force is \(f_0=b_0(X-S)-b_0N_0=\dot S-b_0N_0\), with \(S\) the filtered part. The OU spectrum \(2av/(\omega^2+a^2)\) gives \(\mathbb E[\dot S^2]=b_0^2av/(a+b_0)\), and \(b_0^2\mathbb E[N_0^2]=b_0D_0\), so \(\mathbb E[f_0^2]=b_0^2av/(a+b_0)+b_0D_0\) and, with \(\mathbb E[\partial_0f_0]=-b_0\),

\[
\dot Q_0=\frac{b_0^2\,a\,v}{(a+b_0)\,D_0}\qquad(kT=1;\ \text{units: }\text{time}^{-2}\cdot\text{time}^{-1}x^2/(\text{time}^{-1}\cdot x^2\text{time}^{-1})=\text{time}^{-1}).
\]

The Lyapunov value matches it at three arbitrary points to \(10^{-8}\) relative (`checks/toy_checks.out`). So a smooth level (small \(D_0\)) is expensive: its heat scales as \(1/D_0\).

### 3.3 BA-C2 (identity): one member never pays for a level

The pair \((M_0,M_1)\) is one memory of \(X\) with two coordinates. In a bipartite stationary state the coordinates' heats are each at least \(kT\) times their own information flows, and the flows of \(M_0\) and \(M_1\) add to the composite memory's learning rate (Horowitz 2015, doi `10.1088/1742-5468/2015/03/p03006`, already cited in `theory/FEEDBACK_FLOOR_2026-11-23.md:197`). That rate is at least the Kalman rate \(R\) at the composite's decision error (AT-learn, `theory/INFO_PHYSICS_ATTAINABILITY.md:33`), which is at most \(\varepsilon_1\), and \(R\) is decreasing. So \(\dot Q_0+\dot Q_1\ge R(\varepsilon_1)\) and \(P_1\ge J_{\mathrm{dir}}(w)\). Used only as a code gate.

### 3.4 PAPER: an approximate threshold

If the level's noise is small, its path is nearly smooth, and a fast member copies it at extra error \(\delta\) for heat about \(D_0/\delta\) (the random-walk infimum \(kT\sigma^2/(2\delta)\) of `CORE.md:76` with \(\sigma^2=2D_0\)); the smooth part costs a fast copy almost nothing. With \(u=D_0\) (gain 1) and the exact level heat of §3.2, the approximate per-member cost is

\[
\tilde P_K=\frac{1}{K(1+b_0)u}+\frac{u}{\delta}+w\Bigl(1-\frac{1}{(1+b_0)/b_0+(1+b_0)^2(u/b_0+\delta)}\Bigr)\quad(a=v=1).
\]

`checks/paper_approx.py` minimizes \(\tilde P_K\) (output `checks/paper_approx.out`, committed with the lock). The smallest grid \(K\) with \(\tilde P_K<J_{\mathrm{dir}}\) is 32 at \(w=3\) (ratio 0.984), 24 at \(w=10\) (0.994) and 24 at \(w=100\) (0.961); at \(K=128\) the ratio is 0.74, 0.67 and 0.62. \(\tilde P_K\) is not the scored model: the exact member pays for the smooth part at finite rate and may use a better design than a fast copy, so the exact threshold can sit on either side. Hence the band \([12,48]\) and odds of a miss 0.60.

The structural reading behind the hypothesis, stated before the run: in this class a link is not a free price. Its cost moves into the level, which must pay heat \(\propto1/D_0\) to be smooth enough to copy cheaply, so the threshold is set by heats and the stake alone.

### 3.5 Scored quantity, numerics and rules

- **Grid and stakes.** \(w\in\{3,10,100\}\); \(K\in\{1,2,3,4,6,8,12,16,24,32,48,64,96,128\}\).
- **Design and box.** \(x=(\ln b_0,\ln D_0,\ln b_1,\ln D_1)\) in \([-4,12]\times[-16,12]\times[-4,12]\times[-16,12]\). Every point of the box is an attainable design.
- **Optimizer** (`checks/ba_t2.py`). For each \((K,w)\): evaluate the cost at the 720 grid starts (\(\ln b_0\in\{-2,0,\dots,8\}\), \(\ln D_0\in\{-12,-9,\dots,3\}\), \(\ln b_1\in\{0,3,6,9\}\), \(\ln D_1\in\{-8,-5,\dots,4\}\)), at seven seeds from the PAPER optimum, and at the previous \(K\)'s optimum for that \(w\); polish the best 20 by adaptive Nelder–Mead (xatol \(2\times10^{-9}\), fatol \(2\times10^{-11}\), at most 80,000 evaluations), clipped to the box.
- **Scored.** \(\hat K^*(w)\) is the smallest \(K\ge2\) in the grid whose optimized per-member cost is below \(J_{\mathrm{dir}}(w)(1-10^{-3})\), **confirmed** by an exact rational re-evaluation of that design (design rounded to 12 significant digits, Lyapunov equation computed in rational arithmetic). If no \(K\le128\) qualifies, \(\hat K^*(w)=\) none.
- **Reading.** A confirmed design is a proof that one level with \(K\) linked members beats every direct design at that \(K\) and \(w\) (the comparator is the proved infimum). So \(\hat K^*\) is an upper bound on the true threshold; a \(K\) where no design is found is not a proof that none exists (except \(K=1\), BA-C2). This one-sidedness is locked here.
- **Box edges.** A minimizer on a box edge is still an attainable design, so it counts; edge coordinates are reported. (This replaces the boundary-hit rule of `PREREG_4.md`, which arose because a scored gap needed an attained Nash point; here only a cost comparison is scored.)
- **Resolution.** `checks/ba_t2.py --half` halves both tolerances and polishes 40 starts. If any \(\hat K^*(w)\) changes, BA-T2 is `not-resolved` (`measurement/code`), not scored.
- **HYPOTHESIS:** \(\hat K^*(w)\in[12,48]\) at all three \(w\). **Miss low** if any \(\hat K^*<12\) (size: \(\hat K^*\) and \(w\)); **miss high** if any \(\hat K^*\in\{64,96,128\}\); **none** if any \(w\) has no \(K\le128\); **mixed** (`sensitivity-dependent` open miss) if the three \(w\) fall in different classes. Location `model` unless the code gate fires or the resolution rerun disagrees.
- **Reported, not scored:** per-member cost ratios for every \(K\) and \(w\), designs, \(\varepsilon_0\), \(\varepsilon_1\), \(\dot Q_0/K\), \(\dot Q_1\).

## 4. Prior-art risk (to be checked before the results are written)

That copying costs heat, and that copying a slowly varying template is cheap, are close to known results on thermodynamic copying (Ouldridge, Govern and ten Wolde 2017, *Phys. Rev. X* 7:021004, doi `10.1103/PhysRevX.7.021004`, checked on Crossref 27 Nov 2026, `crossref.out`; its content is to be read before the results are written). A hit on BA-T2 is reported as an in-model threshold in class LINK, with that credit, not as a new mechanism. That all costs in class LINK are heats is true by construction of the class (a restatement risk, `NOTES/rnd-2026-11-26-late/stepback/NEXT_ROUTES_2026-11-26.md:21`, T1); the content of BA-T2 is the threshold value, which a free link price leaves undetermined.

## 5. Order, budget and stop rule

(0) Lock commit pushed, and `git ls-remote` shows it. (1) A gate read of the `Gate` section, committed as `gate_read.md` in this folder before any scored run. If this is a same-agent separate pass and not an independent reader, the gate read says so. (2) From a fresh clone at the lock commit: `checks/ba_t1.py`, `checks/ba_t2.py`, `checks/ba_t2.py --half`, at nice 19; outputs committed as `checks/*.out`. (3) `RESULTS.md` with one eight-field row per bar (`process/MISS_LOG_TEMPLATE.md`), deviations appended in `DEVIATIONS.md`. (4) A hostile second read against the sources before merge. No scored number is recomputed under a changed model after it is logged; a changed model is a new prereg. CPU cap: 60 minutes per scored script.

## 6. Ledger

Every outcome, hit or miss, gets one eight-field row (`prediction_id`, `locked_prediction`, `outcome`, `miss`, `location`, `stake_x_info`, `update`, `breach_check`) in `RESULTS.md`. An open miss is a miss with a diagnosis and a next test and no update yet (`CORE.md` Status words). No single test is decisive.
