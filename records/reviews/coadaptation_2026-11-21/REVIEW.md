# Independent hostile review: PR #148 (co-adaptation)

**Reviewer:** independent. Wrote none of the note or the checks. The only file added by this review is this one.
**Date:** Sunday 22 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/148
**Head reviewed:** `6038f4f13f94acf85c1c7a559e9dbb699bb92cca` on `coadaptation-2026-11-21`, base `c92886af97425102878241740b093983885a0106` (`origin/main` after `git fetch origin main`). Draft. Not merged.

**Verdict: NOT READY**

The substitution-chain theorem, the virial identity, the mismatched-strength bracket, the free-energy marginal, and the two thresholds rederive. Three sentences a reader would take as the result do not. The status cell of CX2 stays OPEN, the hypothesis sentence is byte-identical, and no locked file moves.

## What was rederived

**Kolmogorov, both directions.** Under CA-A, CA-B, CA-C and CA-E the object is the pure-profile substitution chain: one party moves along one edge, at rate \(u_i\) times the Moran fixation probability. CA-C (at most one party polymorphic) is what makes that the chain. It is not an extra algebraic step. Without it the state space contains joint polymorphisms, and simultaneous revision need not keep the Gibbs law even in an exact potential game. That limit is what Alós-Ferrer and Netzer (2010) record, and the note's excluded list cites them for it.

On that chain the fixation ratio is exactly \(\exp(-\beta_i\Delta_i J_i)\) with \(\beta_i=\alpha_i(N_i-1)\). CA-E puts the same clock on both directions of an undirected edge, so \(u_i\) cancels in every rate ratio. Single-party cycles cancel because \(J_i\) is a function of state. The content is the elementary square in two parties.

- If some \(\Psi\) matches \(\beta_i\Delta_i J_i\) on every unilateral move, then \(\pi\propto e^{-\Psi}\) satisfies detailed balance on every edge. The clocks do not enter. Irreducibility (positive fixation probabilities, connected factors) gives uniqueness. This direction holds.
- Only if the chain is reversible: set \(\Psi=-\log\pi\). Detailed balance gives \(\Psi(x')-\Psi(x)=\log(q(x'\to x)/q(x\to x'))=\beta_i\Delta_i J_i\) on every edge. Sums along paths in \(\mathcal{G}_i\) telescope, so the same identity holds for non-adjacent unilateral moves. \(\Psi\) is an exact potential for \((\beta_i J_i)\). This direction holds.

For a weighted potential \(\Delta_i J_i=\omega_i\Delta_i\Phi\), the \(\beta\)-scaled sum around the square is \((\beta_i\omega_i-\beta_j\omega_j)\) times the mixed difference of \(\Phi\) (the \(i\)-difference at the old \(x_j\) minus the \(i\)-difference at the new \(x_j\)). It vanishes for every square if and only if the products agree wherever that mixed difference is nonzero. Unequal products break reversibility. Terms of \(J_i\) that ignore \(x_i\) cancel. Corollary CA1a holds.

Line 51 states this reversible-iff theorem. The one-line display does not. That is blocker 1.

**Virial.** On the stated Itô equation, \(c_i\) constant,
\[
\mathrm d|x_i-c_i|^2=\bigl(-2v_i\beta_i(x_i-c_i)\cdot\nabla_i J_i+2v_i d_i\bigr)\mathrm dt+\text{martingale}.
\]
The quadratic-variation term is \(2v_i\) per coordinate. In stationarity the drift expectation is zero, so \(\beta_i\mathbb{E}[(x_i-c_i)\cdot\nabla_i J_i]=d_i\). The same computation on \(x_i\) gives \(\mathbb{E}[\nabla_i J_i]=0\). Finite second moments make the stochastic integral a martingale on finite horizons. The identity does not depend on \(c_i\): the difference of the two sides at \(c_i\) and at the mean is \((c_i-\mathbb{E}x_i)\cdot\mathbb{E}[\nabla_i J_i]=0\). Any constant \(c_i\) is correct. The LQ reading follows: the mean is the Nash point \(-M^{-1}m\), and \(K+K^\top\succ 0\) makes every positive diagonal speed matrix Hurwitz, because \(VKz=\lambda z\) implies \(\mathrm{Re}(z^*Kz)>0\) and \(z^*V^{-1}z>0\).

**CA3, including non-commuting \(Q\) and \(\Gamma\).** \(A=V\Gamma Q\) is similar to \((V\Gamma)^{1/2}Q(V\Gamma)^{1/2}\succ 0\) without a commuting hypothesis, so the mean is \(\arg\min J_T\). The Lyapunov map \(\mathcal L(X)=AX+XA^\top\) has inverse \(\int_0^\infty e^{-At}Ye^{-A^\top t}\,\mathrm dt\), which preserves the semidefinite order for any Hurwitz \(A\). \(\mathcal L((\gamma_{\min}Q)^{-1})=2V\Gamma/\gamma_{\min}\succeq 2V\), and likewise for \(\gamma_{\max}\) with the inequality reversed. \(\tfrac12\mathrm{Tr}(Q\Sigma)\) respects that order because \(Q\succ 0\), again without commuting. The bracket \(d/(2\gamma_{\max})\le\mathbb{E}[J_T]-J_T^\star\le d/(2\gamma_{\min})\) holds for non-commuting \(Q\) and \(\Gamma\). An independent draw of 2,990 non-commuting triples \((Q,\Gamma,V)\) had no violation.

**Free energy.** With equal strengths the \(y\)-marginal of \(e^{-\beta J}\) is \(e^{-\beta F(x)}\sum_y e^{-\beta G(y;\theta(x))}\), so the parent sees \(\mathcal F_T=-\beta^{-1}\log\sum_y e^{-\beta G}\). For \(G=J_T^\star+\tfrac12 z^\top H_T z\) the Gaussian integral is \((2\pi/\beta)^{d/2}(\det H_T)^{-1/2}\), and
\[
\mathcal F_T=J_T^\star+(2\beta)^{-1}\log\det H_T+\text{const}.
\]
The sign is the entropic one: larger curvature, higher free energy. A one-dimensional quadrature reproduced the factor to \(3\times 10^{-13}\). With \(\theta\) fixed there is no mixed term, so \(\beta_P F+\beta_T G\) is a potential at unequal strengths and the team's excess is \(d_T/(2\beta_T)\).

**F2.** \(J_i=\tfrac12(x_i+c x_{i+1})^2\) has own-gradient Jacobian \(I+cP\). Eigenvalues \(1+c\,e^{2\pi i k/3}\). The complex pair has real part \(1-c/2\). With equal \(v_i\beta_i\) the Nash point \(x=0\) (unique for \(c>0\)) is asymptotically stable if and only if \(c<2\), and exponentially unstable if and only if \(c>2\). At \(c=2\) the real part is zero. Cross-curvature is \(c\) one way and \(0\) the other, so the game is not \(\beta\)-potential. The quoted real parts \(0.25,\ 0.05,\ -0.05,\ -0.5\) match.

**F4.** For \(\dot x=-k\bigl(x(t)-g\,x(t-\tau)\bigr)\) with \(g<-1\), a root \(i\omega\) requires \(\cos(\omega\tau)=1/g\) and \(k\tau=\arccos(1/g)/\sqrt{g^2-1}\). Zero delay is stable for every \(k>0\), and this is the first crossing, so the strict inequality is asymptotic stability. At \(g=-2\), \(\arccos(-1/2)/\sqrt{3}=2\pi/(3\sqrt{3})=1.209199576156145\). The note's \(1.209\) is that number. The rerun gave amplitude ratios \(4.63\times 10^{-5}\) at \(0.8\times\) the bound and \(193\) at \(1.2\times\).

## Blockers

1. `theory/COADAPTATION.md:11`–`:13`, the display labeled "the theorem in one line." Line 51 is the theorem that was proved: the chain is reversible if and only if \((\beta_i J_i)\) is an exact potential game, and then \(\pi\propto e^{-\Psi}\). The display puts \(\pi\propto e^{-\Psi}\) on the left of the equivalence instead of reversibility.

   Every positive distribution is \(e^{-\Psi}\) for \(\Psi=-\log\pi\). F1 (`:127`) has \(\pi\) uniform at every \(\beta\), so \(\pi\propto e^{0}\), while a constant is not a potential of matching pennies. The left side of the display holds and the right side does not.

   Line 7's "Boltzmann distribution if and only if" is the same sentence in words. It is right only when "Boltzmann" means detailed balance. The display defines it as \(\pi\propto e^{-\Psi}\).

   Suggested fix: put line 51 in the display. Reversible, with \(\pi\propto e^{-\Psi}\), if and only if the difference identity. Leave the regret displays as consequences of that case.

2. `theory/COADAPTATION.md:67`. The first term of the team decomposition is the absolute gap \(J_T(x^\Psi)-\min J_T\). The parenthetical bounds that gap by \((N+1)/(2\sqrt N)\).

   CT31's price of anarchy is the ratio \(\sum_i J_i(\mathrm{Nash})/J^\star=\tfrac12\bigl(\sqrt{a/W}+\sqrt{W/a}\bigr)\le(N+1)/(2\sqrt N)\) (`THEORY.md:466`). The absolute gap in that class is \(J^\star\) times (ratio minus 1). It scales with \(J^\star\). For equal stakes and \(N=4\) the ratio bound is \(1.25\); at \(J^\star=1000\) the absolute gap is \(250\). The decomposition's trace term is unaffected: for quadratic \(\Psi\), \(\mathbb{E}[J_T]=J_T(x^\Psi)+\tfrac12\mathrm{Tr}\bigl(H_T(\nabla^2\Psi)^{-1}\bigr)\), because the Gaussian is centered at \(x^\Psi\) and the linear term averages to zero.

   Suggested fix: call the ratio CT31's price of anarchy, bounded by \((N+1)/(2\sqrt N)\) in that class, and leave the displayed term as the absolute gap, which is not that bound.

3. `THEORY.md:178`. The added sentence says coupled parties sit near a minimizer of a potential exactly when the \(\beta\)-scaled game is a potential game.

   F3 is a counterexample to the "when" direction. For \(g>0\), \(\beta_w=\beta_s/g\) makes the world-gain game an exact \(\beta\)-potential game (`theory/COADAPTATION.md:129`). For \(g>1\), \(\det(VK)\propto 1-g<0\) at every positive strength and every positive speed, and the potential is a saddle unbounded below. There is no stationary distribution and nothing to sit near.

   Where a confining quadratic potential does exist, the proved excess is \(d_i/(2\beta_i)\) for each party and \(d/2\) for \(\Psi\). That excess is small only when \(\beta_i\) is large compared with \(d_i\). The selection note's statement of the result is the formula (`theory/SELECTION_AXIOMS.md:184`). "Sit near" is stronger than the formula.

   The same sentence is the convergence claim of the CX2 paragraph. Strict monotonicity gives a stationary mean at the Nash point for every speed, potential or not (CA2a, `:99`), and `:100` records that the regret is then not \(d_i/(2\beta_i)\). Settling is not "exactly when" the game is a potential game.

   Suggested fix: state line 51, then the excess \(d_i/(2\beta_i)\), small only when that excess is small against the party's operating cost, and point the failure classes at the note. Keep "which real couplings are potential games" open. Keep CX2 OPEN.

## Should-fixes

1. `STATUS.md:3`. The paragraph now opens on CLAIM_MAP v2.72 and still says "CLAIM_MAP v2.71 (this branch, not yet merged)." v2.71 is the selection fold, merged as PR #144 onto `c92886a`. This branch is the v2.72 draft. The clause was already on `main`; this PR edited the paragraph and left it. Suggested fix: say v2.71 merged with PR #144, and that v2.72 is this draft, with CX2 still OPEN.

## Nits

1. `theory/COADAPTATION.md:128`. "Cycling" for F2. The linearization at \(c>2\) is an unstable focus: trajectories spiral out. F1 is the circulation, with a nonzero probability current. F2 has no periodic orbit in the linear model.

2. `measurement/CLAIM_MAP_v2.md:620`. S6 says the delay equation is unstable if and only if \(k\tau\) is at least the Hayes number. The note says asymptotically stable if and only if \(k\tau\) is strictly below it (`:130`). At equality the root is imaginary. Constant-amplitude oscillation is the boundary, not exponential growth. The number itself is right.

3. `theory/COADAPTATION.md:182`. The Rajab entry drops given names. Crossref has Fat-Hy O. Rajab, Olugbenga M. Anubi, and Marcos M. Vasconcelos. Every other author line in the list has given names or initials. The attribution is fair; the line is the incomplete one.

## What was checked and holds

- CA1 as stated at `:51`, including clock-independence inside the potential case and clock-dependence outside it. The rerun: matched relative error \(1.03\times 10^{-8}\), matched total-variation across clocks \(7.6\times 10^{-13}\), mismatch square-cycle log ratio \(50.91\), mismatch total variation \(0.0104\). Random games: reversibility agreed with the \(\beta\)-scaled square test on 60 of 60, and none of the 30 non-potential draws was reversible.
- CA1b's three formulas, on the Gaussian quadratic well. Per-party conditional Boltzmann because \(\Psi-\beta_i J_i\) ignores \(x_i\). Potential excess \(d/2\) at weight \(e^{-\Psi}\). Team split as in blocker 2, without the false bound. Lattice check: regrets \(0.006246\) and \(0.015609\) against \(0.00625\) and \(0.015625\), potential excess \(0.999996\) against \(1\), team excess \(0.116671\) against \(0.116671\).
- CA1c. With \(J_i=s_i J_T\), \(h_i=0\), and \(\alpha_i=\sigma_i/J_i^\star\), one gets \(\beta_i s_i=\sigma_i\nu_i/J_T^\star\). SA1c's \(N_e\) is \(\nu\), so equal \(\sigma N_e\) is the right condition, and the fractional excess is \(d/(2\sigma N_e)\). This is not a claim about census size.
- CA2 and CA2a, as in the rederivation. Lyapunov virials on the opposed linear game are \(1\) to \(10^{-15}\) while the covariance moves by \(0.29\) across speeds. Euler–Maruyama virials \(1.006\) and \(0.995\). Nonlinear virials about \(c=0\) are \(1.005\) and \(1.006\); about \(c=1\), \(0.984\) and \(0.999\).
- CA3, including non-commuting \(Q\) and \(\Gamma\). The script's 3,000 trials: no violation; equal strengths err by \(1.6\times 10^{-13}\).
- CA4. Fixed \(\theta\): team scatter \(0.0454545\) against \(1/(2\cdot 11)\). Moving curvature: free-energy marginal at total variation \(7.3\times 10^{-17}\), upkeep-only at \(0.029\).
- F1 uniform at \(\beta=1,5,20\), with currents \(0.0248,\ 0.106,\ 0.223\). F3: \(\det K=\beta_s\beta_w(1-g)\) at arbitrary positive strengths, so \(g>1\) runs away even though both costs are nonnegative. F5 quotes the Freudenberg–Looze integral and leaves the sampled-read question OPEN.
- Status words. CX2's status cell is still **OPEN** (`measurement/CLAIM_MAP_v2.md:530`). S7 is **OPEN**. `OPEN_WORK.md:59` says CX2 stays OPEN. The note says whether real coupled systems are \(\beta\)-potential games is OPEN (`:22`, `:157`). Nothing in the diff says a measured coupling is a potential game. The word "law" occurs in the new note only inside the hypothesis sentence. `check_consistency.py` reported 0 wording FAILs on 30 maintained documents.
- Part 2 sentence, byte-identical to `c92886a`, one copy each, bold markers included: `THEORY.md:41`, `CORE.md:9`, `README.md:9`, `theory/SELECTION_AXIOMS.md:13`. The new copy at `theory/COADAPTATION.md:26` is the same bytes: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.`
- Locked files. `git diff --name-only c92886a...HEAD` is the 11 PR paths. A filter for prereg, lock, hash, and results names is empty. `core/bridge_2026-11-21/PREREG.md`, `core/bridge_2026-11-21/LOCK.txt`, `prereg/WIKIDATA-BAND/LOCK.txt`, `prereg/WIKIDATA-BAND/PREREG.md`, and `tests/EVO1/PREREG_EVO.md` match the base blobs. CT31, CT32, and CT34 are outside the diff.
- Maintained-list edit. `tools/check_consistency.py:60` adds `theory/COADAPTATION.md` between `theory/INTERNAL_MODEL.md` and `theory/MATH_ATTACK.md`. The wording scan includes it. The tally block matches the counter: OPEN 86, PROVED (in-model) 101, total 337, which is the previous 330 plus S1–S6 proved and S7 open. No other status cell changes.
- Prior art. All 13 DOIs resolved on Crossref on 22 November 2026, with the title, year, container, volume, and pages stated in the note. Blume 1993 is the Gibbs stationary distribution of log-linear revision in a potential game; the note marks the fixation-chain packaging and the unequal-\(\beta\) iff as that corollary, which matches what line 51 actually adds. Alós-Ferrer and Netzer 2010 show that the Gibbs form is proved under asynchronous revision and that potential-maximizer selection fails for an exact potential game when revision is not asynchronous. The excluded-list sentence matches that paper. Rajab, Anubi, and Vasconcelos 2025 exists: IEEE Control Systems Letters 9:2741–2746, doi 10.1109/lcsys.2025.3641882. The abstract gives a closed form, for a two-player coordination game with unequal rationality, in which the stationary distribution depends on the agent-selection probabilities. "Consistent with CA1a" is the right strength.

## Commands

All repository commands were run from the repo root on head `6038f4f`, with `nice -n 19`. `python3 -m pip install --user pytest scipy sympy` was required first (numpy was already present). Versions: Python 3.12.3, numpy 2.5.5, scipy 1.18.1, pytest 9.2.0.

- `git fetch origin main`. `origin/main` moved `2eeab30..c92886a`.
- `git diff --stat c92886af97425102878241740b093983885a0106...HEAD`. 11 files, 805 insertions, 14 deletions.
- `git diff --name-only` against that base, filtered for prereg, lock, hash, and results names: empty. Blob hashes of the five locked paths above match the base.
- Hypothesis-sentence bytes compared with `git show c92886a:PATH`. Equal on the four canonical lines. The new copy matches those bytes.
- Independent recomputation (numpy/scipy, not the note's script): F2 real parts including the \(c=2\) boundary; Hayes constant \(1.209199576156145\); 2,990 non-commuting CA3 draws, 0 violations, and one explicit semidefinite-order check; virial diagonals \(1\) and \(1\) on the opposed linear game; Gaussian free-energy factor to \(3\times 10^{-13}\); \(\det K=\beta_s\beta_w(1-g)\) at unmatched strengths; absolute PoA gap \(250\) against ratio bound \(1.25\).
- Crossref `GET /works/{doi}` for the 13 DOIs in the reference list. All 13 returned the cited title, authors, year, and container. Rajab, Anubi, and Vasconcelos 2025 is among them. OpenAlex reconstructed that paper's abstract.
- `nice -n 19 python3 tools/check_fresh.py`. PASS. `STATUS.md` main is `2eeab30`; window `c92886a 2eeab30 c04cedd d34df95 a97887e`.
- `nice -n 19 python3 tools/check_consistency.py`. PASS. 0 FAIL. 30 maintained documents, 0 wording FAILs. CLAIM_MAP rows counted 337, tally total 337. Versions: THEORY v2.9, CLAIM_MAP v2.72.
- `nice -n 19 python3 tools/check_open_work.py`. PASS. 0 missing.
- `nice -n 19 python3 tools/coadaptation_checks.py`. Exit 0 in 8.3 s. Figures quoted above match the note's stated digits.
- `nice -n 19 python3 -m pytest -q tools`. 188 passed, 1 skipped, 272.12 s. The skip is `tools/test_lean.py:101`, Lean 4 / lake is not installed. The PR text says 189 passed. The skipped test is the pre-existing Lean test; the 13 new tests passed inside this run.
