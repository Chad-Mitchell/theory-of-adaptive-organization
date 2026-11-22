# Review of draft PR #175

**Verdict: SOUND-WITH-FIXES.**

Independent review of draft PR #175, head `3e44033982cbaca4202c66eb4b6a65c7cab7e56d` on `info-physics-2026-11-22`, one commit on `origin/main` `32ffd560792eb78ffe78553eb5cc02bb42d0c1e9`. Sunday 22 November 2026. This review does not edit that branch, does not push to it, and does not merge. No `lake build`.

The two-state inequality is right, the printed operating points recompute, and the master equation is not recovered from the second law. Four fixes belong in the note before the status words are read as settled: the heat floor has a closed form and the twelve-digit claim-map value is a grid minimum; the tangent witness uses one price vector, and a different price matches that one stake; Lemma IP-joint bounds a different functional from Still's gap; Barato and Seifert 2015 did not prove the uncertainty relation for this multicyclic sensor.

The hypothesis sentence is unchanged. One copy, in `THEORY.md:41`, byte-identical to `origin/main`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`CORE.md` is not in the diff.

## What holds

Recomputation is `reviews/info_physics_2026-11-22/recompute.py`. It imports nothing from `theory/info_physics_checks/`. Rates, the stationary mass, the edge entropy production, and the information flow are derived in that file. The author's script, run separately, reports 37 checks and FAILS 0.

**The bound.** For \(\alpha_c>\alpha_e>0\) and \(\gamma>0\), with \(Z=\alpha_c+\alpha_e+2\gamma\) and Hamming error \(\varepsilon=(\alpha_e+\gamma)/Z\),

\[
\dot Q=kT\cdot\gamma(1-2\varepsilon)\ln\frac{\alpha_c}{\alpha_e},\qquad
\dot I=\gamma(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon}.
\]

The prefactor identity \(\gamma(\alpha_c-\alpha_e)/Z=\gamma(1-2\varepsilon)\) holds on 200 random designs to \(10^{-12}\), and the information flow from the jump definition \(\sum p\,W\ln(p(x|m')/p(x|m))\) matches the closed form to the same tolerance. Therefore \(\dot Q\ge kT\,\dot I\), with equality when \(\alpha_c/\alpha_e=(1-\varepsilon)/\varepsilon\). That limit is \(\gamma/\alpha_e\to 0\) at fixed error, which is the slow-signal limit the note names. At fixed rates and \(\gamma\to 0\) the ratio also tends to 1, and both rates tend to 0. Reference point \((4,0.5,1)\): error \(0.230769230769\), heat \(1.119699291674\), flow \(0.648293048483\), mutual information \(0.152943038171\). Slow ratio at \(\gamma=10^{-4}\): \(0.999915852256\). Fast ratio at \(\gamma=5\): \(0.236831127602\).

**Fixed error, no ceiling.** At \(\varepsilon=0.2\), \(\gamma=1\), \(kT=1\), the heat is exactly \(0.6\ln\rho\) and the flow is exactly \(0.6\ln 4\) on every design with that error. The infimum is

\[
0.6\ln 4=0.831776616671934.
\]

At \(\ln\rho=40\) the heat is \(24\) exactly. The information \(0.192744757022\) depends only on the error. The author's grid minimum \(0.831836613672\) recomputes; it sits above the infimum because the grid starts at \(\rho=(1-\varepsilon)/\varepsilon\times 1.0001\).

**The two bounds do not add.** The net corrective current has mean \(0.538461538462\). A five-point eigenvalue stencil gives variance per unit time \(0.603095155\) and a Barato–Seifert number \(0.961509393\), against the printed \(0.961509400505\). At \(\gamma=0.05\) the heat is \(0.079109189086\), the flow is \(0.075955854202\), and the uncertainty number is \(0.05995000\), against the printed \(0.059950010756\). The sum \(0.13591\) is above the heat. Each inequality holds. Their sum is a different claim, and the witness is the right one.

**Still's one-step identity, checked against the paper.** Still, Sivak, Bell, and Crooks, arXiv:1203.3271 (the text of PRL 109, 120604). Definitions \(I_{\mathrm{mem}}(t)=I[s_t;x_t]\) and \(I_{\mathrm{pred}}(t)=I[s_t;x_{t+1}]\). Equation (14) is the equality \(\beta\langle W_{\mathrm{diss}}[x_t\to x_{t+1}]\rangle=I_{\mathrm{mem}}(t)-I_{\mathrm{pred}}(t)\), and the footnote derives it as \(H[s_t|x_{t+1}]-H[s_t|x_t]\). Equation (18) is \(I_{\mathrm{mem}}-I_{\mathrm{pred}}\le\beta\langle W_{\mathrm{diss}}\rangle\le\beta\langle W_{\mathrm{ex}}\rangle\), with the relaxation contribution nonnegative. The abstract states the results far from equilibrium, under no feedback. The note's §2 matches those two displays. On the binary example, gap \(1.5\,kT\), flip probability \(0.3\): the difference is \(0.185466009664\) and equals \(h(\varepsilon_{\mathrm{next}})-h(q)\). The quench-and-relax heat \(0.3\cdot 1.5\cdot\tanh(0.75)=0.285817028574\) is the total heat of a flip-and-relax cycle. Equation (18) says that total sits above the one-step identity. The note's separation of the two functionals matches the paper.

**Sagawa and Ueda.** PRL 102, 250602 (2009), arXiv:0809.4098, equation (4): \(W_{\mathrm{meas}}+W_{\mathrm{eras}}\ge k_BT\,I\). The paragraph under that equation says there is a lower bound on the sum, and that measurement alone and erasure alone need not each carry one. The erratum, PRL 106, 189901 (2011), repairs the measurement inequality under the stronger assumption that each POVM element is a single operator, so the apparatus reads out what was transferred. It re-proves that measurement inequality under the stronger assumption. It does not withdraw the sum. For a classical memory that stores the outcome, the note's "one floor on the sum" is the 2009 equation (4) as the erratum leaves it.

**Layers, the numerical half.** Two copies of the reference sensor dissipate \(2.239398583348\) and hold joint information \(0.230742185240\), an increment of \(0.077799147069\) on top of \(0.152943038171\). The sum-tracker at \((6,0.4,0.5)\) dissipates \(1.896910753224\) at squared error \(0.238985868662\); two specialized sensors dissipate \(2.049335287321\) at squared error \(0.243243243243\). The weak drive \((1.2,1.0,0.5)\) dissipates \(0.008275328830\). One device moves from \(0.008275\) to \(1.897\) with the drive. A constant upkeep does not.

**Ornstein–Uhlenbeck.** Cross covariance \(2/3\), mean squared error \(0.483333333333\), mutual information \(0.392869983694\), partial entropy production \(3.250414593698\). Three independent modes sum to entropy production \(10.793807098391\) and information \(0.855418580327\). Two redundant memories: partial entropy productions \(3.696780893043\) each, joint information \(0.457209911969\) against one memory's \(0.392869983694\). The equilibrium memory has partial entropy production \(0\). The Stratonovich expectation of the memory's Sekimoto heat is \((\lambda^2/D)\mathbb{E}[(M-X)^2]-\lambda=4.444444444444\). The note's path, seed 7, \(2\cdot 10^4\) steps, reproduces \(4.43261155\). The note already says the path integral and the Fokker–Planck partial entropy production are not the same number. The gap is this expectation, \(4.444\ldots\) against \(3.250\ldots\).

**Sticky stock.** Past stock \(0.152224143034\), instantaneous \(0.112651473425\), predictive \(0.039530842344\), past excess \(0.112693300691\), Still gap \(0.073120631082\). Lemma IP-chain's equality is the chain rule plus \(I(M;\mathrm{future}\mid\mathrm{past})=0\). The proof's conditional-independence sentence is that hypothesis. The first-order collapse \(I(M;X_{\ge t+1})=I(M;X_{t+1})\) is the second sentence of the proof.

**CT7 arithmetic.** \(\sigma\sqrt{2kTw}\) at \(\sigma=1.7\), \(w=2.5\), \(kT=1\) is \(3.801315561750\). The note's grid prints \(3.80131557\) against \(3.80131556\).

**Author script.** `theory/info_physics_checks/info_physics_checks.py` on this head: PASS 37, FAIL 0.

## Findings

1. **The floor at error \(0.2\) is \(0.6\ln 4\). The claim map's twelve digits are the grid minimum.** `measurement/CLAIM_MAP_v2.md` IP3 says the floor is \(0.831836613672\). That is the minimum of the note's 600-point ray, which starts at \(\rho=(1-\varepsilon)/\varepsilon\times 1.0001\). The infimum, attained as the memory rates diverge at the minimal affinity, is \(0.831776616671934\). `theory/INFO_PHYSICS.md` §4 states a positive infimum and proves the absence of a ceiling. The proof does not exhibit the lower bound. The identity above is the bound: at fixed \(\varepsilon\), \(\dot Q=kT\,\gamma(1-2\varepsilon)\ln\rho\) for every \(\rho>(1-\varepsilon)/\varepsilon\), so the infimum is \(kT\,\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) and the heat at \(\ln\rho=40\) is \(24\,kT\gamma(1-2\varepsilon)\), which is \(24\) at the printed point. The PR body's \(0.832\) rounds both the infimum and the grid minimum. The twelve-digit row should carry the closed form.

2. **The tangent witness is one price vector on one stake. A different price matches that stake, and the flow objective is the frontier.** Same grid, same stake \(w=8\), same coordinates \((\dot Q,\varepsilon)\): the note's comparison is on one feasible set. \(\kappa I(M;X)+h+w\varepsilon\) at \(\kappa=1.5\), \(h=0.4\) selects error \(0.004749003213\), heat \(5.94301196144\), and the cheapest heat at no worse error is \(5.79970450991\), a ratio \(1.0247\). Those digits match §8.

   On this family \(I(M;X)=\ln 2-h(\varepsilon)\) and \(h\) is constant, so \(h\) does not move the argmin. \(\kappa=1\), \(h=0\) and \(\kappa=1\), \(h=10\) select the same error, \(0.004114465901\). Setting \(\kappa=kT=1\) moves the stand-in further from the heat argmin than \(\kappa=1.5\) does. The continuous stand-in has derivative zero at \(\varepsilon=1/(1+e^{w/\kappa})\).

   The heat argmin on the printed grid is error \(0.173927642272\), heat \(1.05346454035\), at drive \(F=1.615384615385\) and speed \(r=30\), the top edge of the speed grid. Its flow is \(1.016069512896\), so the excess heat over the floor is \(0.0374\). The price \(\kappa=w/\ln((1-\varepsilon)/\varepsilon)=5.134646\), with any \(h\), selects that same grid point. One stake, one grid, and a calibrated \(\kappa\) agree.

   That \(\kappa\) does not travel. The efficient frontier, \(r\to\infty\), minimizes \(\dot Q_{\min}(\varepsilon)+w\varepsilon\) with \(\dot Q_{\min}(\varepsilon)=(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\). Its errors are \(0.379876\) at stake \(2\), \(0.167031\) at stake \(8\), and \(0.063722\) at stake \(20\). The stock objective at the \(\kappa\) matched to the grid point of stake \(8\) selects \(0.403835\), \(0.173928\), and \(0.019936\) at those three stakes. A least-squares fit of \(\kappa I(\varepsilon)+h\) to \(\dot Q_{\min}(\varepsilon)\) on \(\varepsilon\in[0.02,0.45]\) leaves a maximum residual \(0.617\). The stock saturates at \(\ln 2\). The floor diverges as \(\varepsilon\to 0\).

   The corrected objective \(kT\,\dot I+w\varepsilon\) equals \(\dot Q_{\min}(\varepsilon)+w\varepsilon\) on this family, because \(\dot I=\dot Q_{\min}/kT\). It is the Lagrangian of the efficient frontier. On the printed grid, which stops at \(r=30\), it selects error \(0.167570574149\) (heat \(1.171174438768\), excess \(0.105\)), next to the continuous frontier error \(0.167031\) and not next to the heat argmin \(0.173928\). The heat objective charges the excess. The flow objective does not, so inside a grid that has not reached the floor the two argmins differ by \(0.00636\). Reaching the floor, which is the equality case the note already proves, makes them the same objective.

   IP5's refusal, that dissipation does not produce the term list, the cap, and the linear prices, stands on §5 and §6. The sentence that the witness is the pair of errors \(0.1739\) and \(0.00475\) shows that \((\kappa,h)=(1.5,0.4)\) is not the supporting price. Replacing the witness with the shape residual and the three-stake table is what shows that no fixed \((\kappa,h)\) is the frontier.

3. **Lemma IP-joint is the right inequality for its conditional mutual information. The Still floor is a further identification.** Under conditional independence given the trajectory, \(H(M\mid\mathrm{past},\mathrm{future})=\sum_i H(M_i\mid\mathrm{past},\mathrm{future})\) and \(H(M\mid\mathrm{future})\le\sum_i H(M_i\mid\mathrm{future})\), so

\[
I(M;X_{\le t}\mid X_{>t})\le\sum_i I(M_i;X_{\le t}\mid X_{>t}),
\]

with equality when the layers are independent given the future. That is the proof in §7.

   Drop conditional independence and the inequality reverses. Fair bits with \(Z=M_1\oplus M_2\) have joint mutual information \(\ln 2\) and marginals \(0\), as the note computes. The same law with a future: \(M_2=M_1\oplus Z\), and \(Y\) a binary channel of \(Z\) with flip probability \(0.2\). Then \(I(M_1,M_2;Z\mid Y)=h(0.2)=0.500402423538\) and each marginal conditional mutual information is \(0\). Still's gap on that law, \(I(M;Z)-I(M;Y)\), equals the same \(0.500402423538\) against a marginal sum of \(0\).

   Still's instantaneous gap is \(H(M\mid X_{t+1})-H(M\mid X_t)\). Conditional independence given \(X_t\), which is stronger than conditional independence given the whole trajectory when the memories are sticky, gives \(H(M\mid X_t)=\sum_i H(M_i\mid X_t)\) and therefore Still's gap at most the sum, by subadditivity of \(H(M\mid X_{t+1})\). The note's hypothesis is the trajectory one. A sticky pair (flip probability \(0.25\), redraw \(0.35\), crossover \(0.08\)) kept the joint Still gap below the sum, \(0.12302259\) against \(0.14840523\), and kept the lemma's conditional mutual information below its sum, \(0.18657816\) against \(0.21814480\). Split-time sensors, one copying \(X_t\) and one copying \(X_{t-1}\), did the same at every \((p_{\mathrm{flip}},q)\) tried. I do not have a reversal of Still's gap under trajectory conditional independence.

   Section 7 then says a joint Still floor is at most the sum of the separate floors. The sticky chain in §2 already separates the two functionals: past excess \(0.112693\), Still gap \(0.073121\). The "so" in that sentence needs the identification, or it should say the conditional mutual information, which is what was proved. A lower information floor is not a lower heat, which the same paragraph already says.

4. **The uncertainty relation on this sensor is the 2016 theorem. The 2015 paper proved a narrower case.** Barato and Seifert, PRL 114, 158101 (2015), arXiv:1502.05944. The abstract states that an uncertainty \(\varepsilon\) costs at least \(2k_BT/\varepsilon^2\), independent of the time. The body proves \(Q\ge 2k_BT\) for any network inside linear response, proves it for a unicyclic network beyond linear response, and checks multicyclic networks numerically. The reference sensor has several cycles and affinity \(\ln 8\), outside that proved set. Gingrich, Horowitz, Perunov, and England, PRL 116, 120601 (2016), arXiv:1512.02212: "While the thermodynamic uncertainty relation was not proven in general," and, as a small-fluctuations corollary of their large-deviation bound for Markov jump processes, "we derive a recently-conjectured uncertainty bound." The note's "tighten the large-deviation side" covers the large-deviation inequality. The general steady-state current bound on this chain is the corollary. The numerical check in the note is a check of that relation. The prior-art line should name Gingrich et al. for the general Markov-jump case and Barato and Seifert for the unicyclic and linear-response theorems and the constant \(2\).

5. **Several negative sentences are already in the repository, and two nearby results bound the same gap from the other side.** The note says the ingredients are not new and the assembly is the claim. That split is right for the list below, which the note cites in part.

   - Still's equality and the protocol inequality: `core/bridge_2026-11-21/FLOOR.md` and `theory/THEOREMS.md` T6.
   - Heat at least \(kT\) times an information flow, for the Kalman–Bucy filter, with the random-walk limit \(\sigma^2/(2D)\): `theory/INTERNAL_MODEL.md` (Mitter and Newton 2005; Horowitz and Sandberg 2014) and THEORY CT7. The two-state closed form is not in those notes.
   - Measurement and erasure as one sum, and S-A left as an assumption: `theory/SHANNON_2026-11-21.md` and `CORE.md`.
   - Gross stock, predictive information, and Still's difference as different functionals, and the stock ruled out as the viability coordinate when the variance diverges: `theory/GENERAL_FORM.md` and PD6.
   - No proved upkeep inside the information floor: the Shannon note's memoryless counterexample.
   - The cap and the term list as inputs: GF3, GB5, `theory/GROWTH_BRIDGE.md`.
   - The support function: Theorem S2.
   - One tracker for one process, and a joint reset against a stack: `CORE.md` and `theory/LAYER_LIFETIME_2026-11-21.md`. The note points at both.

   Two results sit next to the efficiency paragraph and are not named. Barato, Hartich, and Seifert, New J. Phys. 16, 103024 (2014), arXiv:1405.7241: a conditional-entropy learning rate is bounded by the entropy production, and in their adaptation model a bacterium whose environment changes on a very slow time scale dissipates much more than it learns. Their second model also has a nonzero learning rate with no dissipation inside the cell, because the external process pays. `theory/SCALE_ENDS.md` SE3, with the review counterexample: a two-state receptor holds about \(0.18\) nats while the dissipation per cycle falls with the drive, to \(0.026\,kT\) at \(\omega/\gamma=0.01\). The note's ray is the other direction at fixed \(\gamma\): the heat has no ceiling at fixed error. The slow-signal equality is the direction SE3 already has, and the floor in the proposition is at fixed \(\gamma>0\). Naming those two keeps the ray in its place.

   Lan, Sartori, Neumann, Sourjik, and Tu, Nat. Phys. 8, 422 (2012): adaptive processes are dissipative, and the energy–speed–accuracy relation in the coarse-grained model has higher dissipation for faster or more accurate adaptation. The error–energy form in that paper is exponential in the dissipation at fixed speed. The prefactor is correctly left uncopied. "The same fact the uncertainty relation makes quantitative" is a qualitative sentence. The functional forms differ.

   Horowitz and Esposito, Phys. Rev. X 4, 031015 (2014), equation (11): the subsystem entropy production is \(\dot S_i^X=\mathrm d_t S^X+\dot S_r^X-\dot I^X\ge 0\). In steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\). The note's sensor puts that bath on the memory, because the signal edges have equal forward and backward rates. The Barato–Hartich–Seifert receptor is the case where the outside bath pays instead.

## What physics can carry, and what would make it the tangent

On this family the defensible replacement for \(\kappa I_{\mathrm{mem}}+hK+A\) is the medium heat of the mechanisms that implement the memory. Its floor is one term,

\[
\dot Q\ge kT\,\dot I(\varepsilon)=kT\,\gamma(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon},
\]

with equality on the fast-memory boundary \(\rho\downarrow(1-\varepsilon)/\varepsilon\). A separate rental on the stock \(I(M;X)\), a constant \(h\), and a second read price on the same nats are not forced by this balance. Sagawa and Ueda's sum is the floor on one measurement-and-erasure operation. In the continuously coupled sensor that operation is already inside \(\dot Q\).

The Lagrangian of the efficient frontier is \(kT\,\dot I(D)+wD\), with \(w\) supplied. On this family it equals \(\min(\dot Q+wD)\), because every error is achievable at the floor and lowering the affinity lowers the heat at fixed error. That is the sense in which the corrected objective matches the heat-plus-error optimum. The printed grid stops at \(r=30\), short of the floor, and on that grid the two argmins differ by \(0.00636\), as finding 2 records.

For \(kT\,\dot I+wD\) to be the tangent of the physical frontier beyond this telegraph, the following have to be proved.

1. **Equality at the operating design.** The inequality gives an outer bound. The support function of the achievable set uses \(\dot Q\). It equals \(kT\,\dot I+wD\) on the boundary where \(\dot Q=kT\,\dot I\), and elsewhere the excess is a free coordinate. The ray shows the excess can be arbitrarily large at fixed error and fixed mutual information. A proof has to put every minimizer of \(\dot Q+wD\) on that boundary, or name the class of drives where the excess is identically zero.
2. **One coordinate.** Here \(\dot I\) is a function of the Hamming error, so the frontier is a curve. For a general loss, the stake has to price a statistic that fixes \(\dot I\), or the frontier is a higher-dimensional set and one scalar \(w\) does not support it.
3. **Which bath pays.** Horowitz and Esposito charge \(\dot I\) to the learning subsystem's entropy production. Barato, Hartich, and Seifert's receptor learns while the cell's own dissipation is zero. A memory price equal to \(kT\,\dot I\) needs a proof that the memory's bath is the one that pays.
4. **Layers.** Separate baths add their heats. One joint mechanism has one entropy production. Lemma IP-joint bounds a conditional mutual information. The sum-tracker numbers are one comparison. A theorem that the joint frontier lies below the sum of the marginal frontiers is a coupling argument, still open past that comparison.
5. **Reads.** A separate acquisition term is an operation whose bath is not already in \(\dot Q\). Sagawa and Ueda bound one operation's sum. They do not add a second price on the same mutual information.
6. **The stake stays an input.** \(kT\) does not set \(w\). P-L already says so.
7. **Ruin and linking stay outside** until a reserve, or a copy that is actually made, is part of the physical model. Ouldridge, Govern, and ten Wolde (Phys. Rev. X 7, 021004, 2017) bound the dissipation of a computational copy by the mutual information when that correlation is not used to extract work, and their biochemical network sits above the bound for general input. Ouldridge and ten Wolde (Phys. Rev. Lett. 118, 158103, 2017) give three costs of separating a persistent polymer copy from its template: template binding does not drive the separated copy, specificity costs work, and mixing copies reduces the stored free energy. A design that does not copy does not pay those costs. Neither paper supplies a linear linking price on every design.
8. **The extension.** The bipartite balance is Horowitz and Esposito. The closed form stops at the sensor, the sum-tracker, and the Gaussian, which is what §11 says. Equality on the fast-memory boundary has to be proved for that extension.

Under those eight, a lineage that minimizes dissipation plus weighted error, at equality, on these coordinates, with H3 for those coordinates and with no ruin cap, sits on the physical tangent. That is the note's closing sentence of §9, and it is the right sentence. It is this objective. It becomes the master equation only through the coordinate identification §8 already lists and does not prove.

## DOIs

All 23 DOIs in §12 returned Crossref HTTP 200 on 22 November 2026. Title, year, container, and the family names in the note match the record. Page citations that name the first page match the start of the Crossref page range (Landauer 183–191, Schnakenberg 571–585, Duncan 215–220, Lan 422–428, Mehta 17978–17982, Parrondo 131–139, Tatikonda 1549–1561). PRL and PRX records have no page field; the article numbers in the note match the DOIs. Crossref lists Pieter Rein ten Wolde on the polymer-copy paper as "Rein ten Wolde, Pieter." That is the same author. Anthony J. Bell is the third author of Still et al. 2012. Yuhai Tu is the fifth author of Lan et al. 2012.

Papers read for the claims in findings 2–5 and in the prior-art section: Still et al. arXiv:1203.3271; Sagawa and Ueda arXiv:0809.4098 and the erratum text of PRL 106, 189901; Horowitz and Esposito arXiv:1402.3276; Barato and Seifert arXiv:1502.05944; Gingrich et al. arXiv:1512.02212; Barato, Hartich, and Seifert arXiv:1405.7241; Mehta and Schwab arXiv:1203.5426; Lan et al. via the PMC copy of Nat. Phys. 8, 422; Sartori et al. arXiv:1404.1027; Ouldridge, Govern, and ten Wolde arXiv:1503.00909; Ouldridge and ten Wolde arXiv:1609.05554.

## Checks

On head `3e44033`, from `/tmp/ip175`:

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT: PASS. FAIL 0. Rows counted 385, tally total 385. Two advisory length warnings (THEORY main text, README 1476 words) |
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS says `main` is `0920cb0`, inside the five-commit window `32ffd56 0920cb0 dd7efec bb6396f 3ee7f50` |
| `python3 tools/check_open_work.py` | RESULT: PASS. Union missing from OPEN_WORK.md: 0 |
| `nice -n 19 python3 -m pytest -q tools/` | 253 passed, 1 skipped, 304.96 s, exit 0. The skip is `tools/test_lean.py` (lake not installed). No lake build |

`nice -n 19 python3 theory/info_physics_checks/info_physics_checks.py`: PASS 37, FAIL 0.

On this review branch, which is `origin/main` plus this directory: `check_consistency.py` PASS (rows 378, tally 378), `check_fresh.py` PASS, `check_open_work.py` PASS, and `nice -n 19 python3 -m pytest -q tools/` is 252 passed, 1 skipped, 304.83 s, exit 0. The extra pass on the draft head is `tools/test_info_physics_checks.py`. NumPy for `recompute.out` is 2.5.5. The seed-7 path value \(4.43261155\) also matched under NumPy 1.26.4.
