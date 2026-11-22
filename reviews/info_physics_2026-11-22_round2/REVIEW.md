# Review of draft PR #175, round 2

**Verdict: NOT-YET-SOUND.**

Independent review of the revised draft, head `433ab1bbb4cbb8b9882fc9919c12f616c0a0c0aa` on `info-physics-2026-11-22`, two commits on `origin/main` `32ffd560792eb78ffe78553eb5cc02bb42d0c1e9`. The previous review is PR #176, head `e92dcc6bb1bd0bec509a9535c3b47947a683a387`. This review does not edit either branch, does not push to them, and does not merge. No `lake build`. Sunday 22 November 2026.

The telegraph bound holds, the telegraph stake table holds, and \(J_{\mathrm{phys}}\) is labeled as a proposal. Two claims in the revision do not hold. On the linear spring the information flow is not bounded below by \(kT\,av/\varepsilon\), and at stake 2 the flow objective tracks while the heat objective is blind. The reference sensor is one 4-cycle, so Barato and Seifert 2015 already cover the uncertainty check that this revision moved to Gingrich et al. 2016 on the ground that the sensor is multicyclic.

The hypothesis sentence is unchanged. One copy, in `THEORY.md`, byte-identical to `origin/main`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

`CORE.md` is not in the diff. The master equation in THEORY is not replaced. One sentence was added, pointing at this note and saying the term list, the cap, and the linear prices stay assumptions.

Recomputation is `reviews/info_physics_2026-11-22_round2/recompute.py`. It imports nothing from `theory/info_physics_checks/`. The generator, the stationary law, the edge entropy production, the jump information flow, the Lyapunov covariance, and the Sekimoto expectation are derived in that file.

## What holds

**The telegraph.** For \(\alpha_c>\alpha_e>0\) and \(\gamma>0\), with Hamming error \(\varepsilon=(\alpha_e+\gamma)/Z\) and \(Z=\alpha_c+\alpha_e+2\gamma\),

\[
\dot Q=kT\cdot\gamma(1-2\varepsilon)\ln\frac{\alpha_c}{\alpha_e},\qquad
\dot I=\gamma(1-2\varepsilon)\ln\frac{1-\varepsilon}{\varepsilon}.
\]

Both were recomputed from the \(4\times 4\) generator and from the jump sum \(\sum p\,W\ln(p(x|m')/p(x|m))\), not from the note's closed form. On 200 random designs the two agree with the closed form to \(5\times 10^{-15}\). The signal edges contribute \(0\) to the entropy production. At fixed error the excess over the floor is exactly the quantity named in §8a,

\[
\dot Q-kT\,\dot I=kT\,\gamma(1-2\varepsilon)\ln(\rho/\rho_\star),\qquad\rho_\star=(1-\varepsilon)/\varepsilon,
\]

checked to \(3\times 10^{-15}\) at four ratios, including \(\ln\rho=40\). At \(\varepsilon=0.2\), \(\gamma=1\), \(kT=1\), the infimum is \(0.6\ln 4=0.831776616671934\), and the twelve digits \(0.831776616672\) are that value rounded. The 600-point ray that starts at \(4\times 1.0001\) has closed-form minimum \(0.6\ln(4.0004)=0.831836613672\). At \(\ln\rho=40\) the heat is \(24\). The information \(0.192744757022\) depends only on the error. Reference point \((4,0.5,1)\): error \(0.230769230769\), heat \(1.119699291674\), flow \(0.648293048483\), mutual information \(0.152943038171\).

**The telegraph fixes from PR #176, the ones that landed.** A constant upkeep does not move the stock argmin: at \(\kappa=1\), \(w=8\), upkeep \(0\) and upkeep \(10\) both select error \(0.004114465901\). The price matched to the heat argmin on the printed grid is \(\kappa=5.1346464562\). That grid is \(F\) linear on \([0.3,6]\) and \(r\) logarithmic on \([0.05,30]\), \(40\) by \(40\), with \(r=\sqrt{\alpha_c\alpha_e}\) and \(F=\ln(\alpha_c/\alpha_e)\). The heat argmin is error \(0.173927642272\) at the edge \(r=30\); the flow argmin is error \(0.167570574149\); the gap is \(0.006357068124\). The efficient-frontier errors and the stock errors \(1/(1+e^{w/\kappa})\) round to the printed table:

| Stake | Frontier | Stock at \(\kappa=5.1346464562\) |
|---|---|---|
| 2 | 0.379876354741 | 0.403835082858 |
| 8 | 0.167031420930 | 0.173927642272 |
| 20 | 0.063721549682 | 0.019935672102 |
| 50 | 0.022976142417 | 0.000059008574 |

A least-squares fit of \(\kappa I(\varepsilon)+h\) to the floor on \([0.02,0.45]\), 400 points, leaves maximum residual \(0.617160010554\).

**Lemma IP-joint in §7.** The object on the page is \(I(M;X_{\le t}\mid X_{>t})\). The proof is the chain rule plus subadditivity of \(H(M\mid\mathrm{future})\) once conditional independence given the whole trajectory has factored \(H(M\mid\mathrm{past},\mathrm{future})\). The noisy-future XOR recomputes: joint conditional information \(h(0.2)=0.500402423538\), each marginal \(0\). The sticky chain at flip probability \(0.2\), redraw probability \(0.3\), channel flip \(0.05\): past excess \(0.112693300691\), Still gap \(0.073120631082\).

**The spring heat, as a heat.** The Lyapunov covariance gives \(C_{xm}=\lambda v/(a+\lambda)\) and \(\mathbb{E}[(M-X)^2]=av/(a+\lambda)+D/\lambda\). The Stratonovich expectation of \(F\circ\mathrm dM\) with \(F=-(\lambda/D)(M-X)\) is \((\lambda^2/D)\mathbb{E}[(M-X)^2]-\lambda\). At the reference \((1,2,1,0.3)\) this is \(4.444444444444\). The seeded path, seed 7, step \(2\cdot 10^{-3}\), \(2\cdot 10^4\) steps after \(2000\) of burn-in, gives \(4.43261155339\) under NumPy 1.26.4. On that point, and on 108 other \((a,\lambda,v,D)\), 

\[
\dot Q-\dot I-\sigma
\]

is at most \(2\times 10^{-12}\), where \(\sigma=\mathbb{E}[v_m^2]/D\) is the Fokker–Planck partial entropy production and \(\dot I\) is the memory current contracted with \(\partial_M\ln(p/(p_X p_M))\). Since \(\sigma\ge 0\), \(\dot Q\ge\dot I\) on this family, with the gap equal to \(\sigma\). The page does not write that cancellation. It is why the partial entropy production can sit below the flow: near the fast limit \(\sigma\to 0\) while \(\dot I\) stays positive. At \(\lambda=10^4\), \(a=v=1\), \(\varepsilon=0.2\), the heat is \(5.00200080032\), the flow is \(4.99900039988\), and the gap is \(0.003000400441\). The sentence that this gap is \(0.003\) matches that difference. The flow is \(0.000999600\) below \(av/\varepsilon\), not above it.

For \(\varepsilon<v\) the heat formula \(\lambda\,av/(\varepsilon(a+\lambda)-av)\) decreases in \(\lambda\) and tends to \(av/\varepsilon\). The derivative has the sign of \(\varepsilon-v\). The heat-floor designs at \(a=v=1\) are the printed ones: blind at stake 2 (cost \(2\)); errors \(1/\sqrt{8}=0.353553390593\), \(1/\sqrt{20}=0.223606797750\), \(1/\sqrt{50}=0.141421356237\) at stakes 8, 20, 50, with heats \(\sqrt{w}\). Blind ties the fast spring at \(w=4a/v\), where both costs equal \(4a\) when \(v\) is the signal variance; the note's "beats when \(w\le 4a/v\)" includes that tie.

**The map is a proposal.** Section 8a, OPEN_WORK T37, IP10, and the derivation-chain link 1 all say \(J_{\mathrm{phys}}\) is a proposed replacement and not the equation in THEORY. The four correspondences, read on the heat-efficient boundary of these two models, match what was recomputed. On the telegraph, \(\dot I\) is fixed by \(\varepsilon\) and the minimum heat equals \(kT\,\dot I\). On the spring, the minimum heat at fixed \(\varepsilon<v\) is the fast limit, and on that limit \(\dot I\) meets it, so the boundary value is \(av/\varepsilon\). Separate memory baths add their heats. One shared bath has one entropy production. A read that is already inside the continuous coupling is not a second price; Sagawa and Ueda bound one measurement-and-erasure sum. The stake \(w\) is still an input. Ruin and linking are outside. None of that derives the master equation.

**Conditions 3, 4, and 5, as scoped.** Condition 3 holds for these two couplings: the telegraph's signal edges are balanced, and the spring's Sekimoto integral is the memory bath, and in both cases that heat is at least the flow. The note already says another bath can pay. Condition 5 is a scope sentence. Condition 4's bookkeeping holds inside the additive models: there is no forced constant \(h\), because an equilibrium memory has heat \(0\) and the weak drive in §7 moves one device from \(0.008275\) to \(1.897\). The uncertainty bound and the flow bound are two lower bounds on the same heat. On the telegraph their sum can exceed the heat, so they are not two terms. The note leaves a general coupling theorem open. The constant \(kT\,a\) found below is the gap between the spring's two envelopes. It is not charged at the blind corner, and it is not \(h\).

**Repo pointers that were opened.** `core/bridge_2026-11-21/FLOOR.md` records Still's one-step equality and says the repository's theorems use the inequality. `theory/SHANNON_2026-11-21.md` records the Sagawa–Ueda sum, leaves S-A as an assumption, and gives the memoryless counterexample \(K=0\) with \(I_{\mathrm{mem}}>0\). `theory/SCALE_ENDS.md` SE3 records dissipation per cycle \(0.026\,kT\) at \(\omega/\gamma=0.01\). PD7 in `theory/THEOREM_P_DRIFT.md` is the Kalman–Bucy rate \(\sigma^2/(2D)-\theta\). In the spring's units, \(\sigma^2=2av\) and \(\theta=a\), so that rate is \(a(v-\varepsilon)/\varepsilon\).

## Required fixes

1. **On the spring, \(av/\varepsilon\) is the heat floor and the upper end of the information flow. It is not the flow floor.** At fixed \(\varepsilon<v\), as \(\lambda\) runs from just above \(a(v/\varepsilon-1)\) up to infinity, the heat falls from infinity to \(av/\varepsilon\) and the information flow rises from the Kalman rate \(a(v-\varepsilon)/\varepsilon\) to the same \(av/\varepsilon\). The fast boundary is where they meet. The flow's greatest lower bound on that curve is the Kalman rate.

   At \(a=v=1\), \(\varepsilon=0.2\), \(\lambda=4\times(1+10^{-6})\), the flow is \(4+8\times 10^{-13}\) and the heat is \(5.000005\times 10^{6}\). The Kalman rate is \(4\). The fast limit is \(5\). The difference between those two envelopes is \(kT\,a=1\), constant in \(\varepsilon\):

   \[
   \frac{av}{\varepsilon}-a\frac{v-\varepsilon}{\varepsilon}=a.
   \]

   So the sentence "this spring cannot reach that inflow" does not hold. The information flow approaches the Kalman rate, and the heat diverges there.

   The heat objective and the flow objective do not select the same design.

   | Stake | Heat objective | Flow objective, using \(\inf\dot I=a(v-\varepsilon)/\varepsilon\) |
   |---|---|---|
   | 2 | blind, cost \(2\) | track, error \(1/\sqrt{2}\), flow \(\sqrt{2}-1\), cost \(2\sqrt{2}-1=1.82842712475\) |
   | 8 | error \(0.353553390593\), heat \(2.82842712475\), fast edge | same error, flow \(1.82842712475\), cost lower by \(1\), low-noise edge |
   | 20 | error \(0.223606797750\), heat \(4.47213595500\) | same error, flow lower by \(1\), low-noise edge |
   | 50 | error \(0.141421356237\), heat \(7.07106781187\) | same error, flow lower by \(1\), low-noise edge |

   Where both track, the error agrees only because the two envelopes differ by the constant \(kT\,a\). The design that attains the flow envelope is \(\lambda\downarrow a(v/\varepsilon-1)\) with \(D\downarrow 0\), where the heat diverges. The design that attains the heat envelope is \(\lambda\to\infty\). At stake 2 they do not even agree on whether to track. The printed table is the heat-floor table. Those six-digit errors and heats are right for that table. They are not the flow objective, and the blind row is not the flow objective.

   Two further sentences in the same paragraph do not hold as written. "The heat decreases in \(\lambda\) and tends to \(av/\varepsilon\)" is the case \(\varepsilon<v\). The derivative has the sign of \(\varepsilon-v\). At \(\varepsilon=v\) every spring in the family has heat \(a\), while the blind corner has heat \(0\). At \(\varepsilon>v\) the heat increases in \(\lambda\), and the small-\(\lambda\) end sits below \(av/\varepsilon\) (at \(\varepsilon=1.5\), \(\lambda=0.05\), the heat is \(0.086956521739\) against \(av/\varepsilon=2/3\)). And "the scalar error fixes the flow," in condition 2 and in OPEN_WORK T37, is true on the telegraph and not on the spring: at fixed mean squared error the flow still depends on \(\lambda\).

   The repair is to split the two envelopes, keep the printed table as the heat objective, and delete the claim that the flow objective selects it, including the decision not to track. The fast-boundary equality \(\dot Q=kT\,\dot I\to kT\,av/\varepsilon\) can stay. The identity \(\dot Q=\dot I+\sigma\) should be on the page if the inequality is marked proved; the cancellation above is a numerical identity of this Gaussian family, checked to \(2\times 10^{-12}\), not a proof written out here.

2. **The reference sensor is unicyclic, and the cycle affinity is \(2\ln(\alpha_c/\alpha_e)\), not \(\ln 8\).** The generator has four states and four undirected edges, the square \(00-01-11-10-00\). The cycle-space dimension is \(4-4+1=1\). One pass in the corrective direction has rate product \(\alpha_c\gamma\alpha_c\gamma\); the reverse has \(\alpha_e\gamma\alpha_e\gamma\). The cycle affinity is

   \[
   \ln\frac{\alpha_c^2}{\alpha_e^2}=2\ln\frac{\alpha_c}{\alpha_e}.
   \]

   At \((4,0.5)\) that is \(\ln 64=4.158883083360\). The memory-edge log-ratio \(\ln 8=2.079441541680\) is one edge force. The two signal edges contribute \(0\). Barato and Seifert, Phys. Rev. Lett. 114, 158101 (2015), prove the uncertainty relation for every network inside linear response and for a unicyclic network beyond linear response. Their multicyclic statement beyond linear response is a conjecture in that paper, later a theorem in Gingrich, Horowitz, Perunov, and England, Phys. Rev. Lett. 116, 120601 (2016), as the small-fluctuation corollary of the large-deviation bound. Gingrich et al. do cover this sensor. They are not the first theorem that covers it, and the sensor is not outside the 2015 unicyclic theorem. The net corrective current used in the check is twice the cycle current, because one cycle completion corrects both memory edges; the relative uncertainty is unchanged by that factor of two.

   The sentences to replace are the intro table, §3 ("several cycles and affinity \(\ln 8\), outside that proved set"), IP3, and the v2.83 note. Keep Gingrich et al. as the general jump-process theorem. Say that this example is the 2015 unicyclic case.

3. **The note says 37 checks. The script reports 57.** The header and §10 both say thirty-seven checks, FAILS 0. Running `theory/info_physics_checks/info_physics_checks.py` on this head prints `PASS 57  FAIL 0`. The PR body already says 57. The note should say 57.

4. **IP1 still says "joint nonpredictive information."** Section 2 defines nonpredictive information as Still's \(I(s_t;x_t)-I(s_t;x_{t+1})\). Section 7 and IP6 restrict the joint inequality to \(I(M;X_{\le t}\mid X_{>t})\) and give the noisy-future XOR. IP1 still names the joint object "nonpredictive information" and still gives only the future-free XOR, the one with joint information \(\ln 2\). Point IP1 at the same conditional mutual information and the same noisy-future example. The inequality in §7 itself is the one PR #176 asked for, and it checks.

## What is new, and what is not

The inequality \(\dot Q\ge kT\,\dot I\) for a bipartite stationary system is Horowitz and Esposito, Phys. Rev. X 4, 031015 (2014): in steady state the learning subsystem's bath satisfies \(\dot S_r\ge\dot I\). The learning-rate form used on a sensor is Barato, Hartich, and Seifert, New J. Phys. 16, 103024 (2014), already cited. Still, Sivak, Bell, and Crooks, Phys. Rev. Lett. 109, 120604 (2012), is the one-step equality and the protocol inequality for a different functional. Sagawa and Ueda, Phys. Rev. Lett. 102, 250602 (2009), equation (4) in the arXiv text, with the 2011 erratum leaving the sum in place, is one floor on measurement plus erasure. The uncertainty relation is Barato and Seifert 2015 for the unicyclic case and for linear response, and Gingrich et al. 2016 for a general Markov jump process. Lan, Sartori, Neumann, Sourjik, and Tu, Nat. Phys. 8, 422 (2012), have a different formula: in the coarse-grained adaptation model, \(\dot W\approx(c_0\sigma_a^2)\,\omega_m\ln(\varepsilon_0/\varepsilon)\). That is a logarithmic accuracy cost at fixed adaptation speed. It is not \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\), and it is not a constant \(h\). The note's "same fact" sentence is only that precision and speed cost dissipation.

Bo, Del Giudice, and Celani, J. Stat. Mech. (2015) P01014, doi 10.1088/1742-5468/2015/01/P01014, arXiv:1408.5128, bound a different functional: the information a memory holds about the past of a sensory layer beyond the present reading, by the extra entropy production of the whole device over the sensory layer. In steady state they recover a learning-rate bound of the Horowitz–Esposito type. They do not derive this telegraph excess, this stake table, or a replacement for this repository's master equation. Crossref lists the families as Bo, Giudice, and Celani.

The Kalman–Bucy rate \(a(v-\varepsilon)/\varepsilon\) is Duncan 1970 as already booked in PD7 and `theory/INTERNAL_MODEL.md`. Nothing in this note reverses that.

What this draft adds, and what the recomputation supports, is narrower than the proved labels.

- The telegraph closed form and the excess \(kT\,\gamma(1-2\varepsilon)\ln(\rho/\rho_\star)\), including the infimum \(0.6\ln 4\). That is the solution of this four-state chain. It is not in the papers named above, and it is not in PD7 or the internal-model note. The shape of the inequality is prior art.
- The telegraph stake table, the residual \(0.617160\), and the grid gap \(0.006357\): one stock price matched at one stake is not the efficient frontier at the other stakes, and no affine function of \(I(M;X)=\ln 2-h(\varepsilon)\) fits the floor. That is a calculation about this cost, not a new physical law.
- The spring heat \((\lambda^2/D)\mathbb{E}[(M-X)^2]-\lambda\), its fast limit \(av/\varepsilon\), and the constant gap \(kT\,a\) between that limit and the Kalman rate. The gap is subtraction. The direction of the flow, rising from the Kalman rate to \(av/\varepsilon\), is the part the note has backwards.
- The proposal \(J_{\mathrm{phys}}=\dot Q+w\,\mathbb{E}[\ell]\), with ruin and linking outside, as a replacement that is not adopted. The negative half is the part that is specific to this repository: \(\kappa I_{\mathrm{mem}}\), a constant \(h\) per layer, and a second read price are not forced by these two balances. That negative half was the content of PR #176, and the revision keeps it. It is not a derivation of the master equation, and the draft says so.

## DOIs

All 23 DOIs in §12 returned Crossref HTTP 200 on 22 November 2026. Year, title, container, and the family names in the note match the record, with the same ten Wolde parsing as in PR #176: on the polymer-copy paper Crossref's family field is "Rein ten Wolde". The Bo, Del Giudice, and Celani DOI above was resolved the same day and is not one of the 23; the note does not cite it.

## Checks

On head `433ab1b`:

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT: PASS. FAIL 0. Rows counted 388, tally total 388. Advisory length warnings on THEORY main text and README |
| `python3 tools/check_fresh.py` | RESULT: PASS. STATUS says `main` is `0920cb0`, inside the window `32ffd56 0920cb0 dd7efec bb6396f 3ee7f50` |
| `python3 tools/check_open_work.py` | RESULT: PASS. Union missing from OPEN_WORK.md: 0 |
| `nice -n 19 python3 theory/info_physics_checks/info_physics_checks.py` | PASS 57, FAIL 0 |
| `nice -n 19 python3 -m pytest -q tools` | 253 passed, 1 skipped, 302.60 s, exit 0. The skip is `tools/test_lean.py` (lake not installed). No lake build |

On this review branch, which is `origin/main` plus this directory: `check_consistency.py` PASS (rows 378, tally 378), `check_fresh.py` PASS, `check_open_work.py` PASS, and `nice -n 19 python3 -m pytest -q tools` is 252 passed, 1 skipped, 301.09 s, exit 0. The extra pass on the draft head is `tools/test_info_physics_checks.py`.

The author's script count is 57. The note's count is 37. NumPy for `recompute.out` is 1.26.4. SciPy 1.18.1 and SymPy 1.14.0 were installed in this environment before pytest; they are not part of the draft.
