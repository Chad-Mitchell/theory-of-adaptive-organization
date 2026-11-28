# Independent hostile review: PR #146 (drift selection)

**Reviewer:** independent. Wrote none of the note, the simulator, the claim-map rows, or the pointer edits. The only file added by this review is this one.
**Date:** Saturday 21 November 2026 (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/146
**Head reviewed:** `93db78340f20a015e2af04c48aeb5485328633aa` on `drift-selection-2026-11-21`, base `c92886af97425102878241740b093983885a0106` (`origin/main`, merge of PR #144). Draft. Not merged.

**Verdict: NOT READY**

DS1, rederived below from the Moran fixation expansion through the Lyapunov trace, is the formula in the note. The diffusion coefficient, the noise \(2D_m\), the cross term \(-2Q\), and the factors of \(1/2\) all come out as written. The lattice-chain runs reproduce the documented fits exactly. The factor of 2 against Held, Nourmohammad and Lässig (2014) is a typo in their equation 54, not in DS1. DS2's speed bound is right, and an optimum strictly faster than \(v_{\max}\) does outrun the chain. The theorem as displayed does not: the cost inequality is false, and the proof's second Jensen step does not give it.

## Blockers

1. `theory/DRIFT_SELECTION.md:120` and `:122`, copied at `measurement/CLAIM_MAP_v2.md:616`. Theorem DS2 is marked **PROVED (in-model)** and states, for \(|v_k|\ge v_{\max}\),

   \(\mathbb{E}[|L_k(t)|]\ge(|v_k|-v_{\max})t-|L_k(0)|\), so \(\mathbb{E}[J-J^\star]\ge\tfrac12\lambda_{\min}\bigl((|v_k|-v_{\max})t-|L_k(0)|\bigr)^2\), and the time-averaged excess grows without bound.

   The speed bound in the first sentence is proved: each coordinate's drift is strictly below \(v_{\max}=N\mu\delta/(2d)\), because the Moran fixation probability is strictly below 1 for every finite fitness step, so \(|\mathbb{E}[\theta_k(t)-\theta_k(0)]|<v_{\max}t\).

   The cost inequality does not follow, and it is false. \(\mathbb{E}[L_k^2]\ge(\mathbb{E}|L_k|)^2\) turns a lower bound on \(\mathbb{E}|L_k|\) into a lower bound on the cost only when that lower bound is nonnegative. When \((|v_k|-v_{\max})t<|L_k(0)|\) the right-hand side of the lag bound is negative. Squaring it is not a lower bound. At equality \(|v_k|=v_{\max}\) the lag bound is \(-|L_k(0)|\), which does not grow, so the written estimate also does not prove that the time average diverges.

   Counterexample, same chain as §2, run for this review at nice 19 (2,000 replicates, \(\Delta t=0.002\), seed 0). \(N=20\), \(\alpha=0.05\), \(h=1\), \(\delta=\mu=d=1\), so \(v_{\max}=10\). Constant velocity \(v=v_{\max}\), deterministic start with the lineage ahead by \(L(0)=+10\). The displayed bound says \(\mathbb{E}[J]\ge 50\) at every \(t\). Measured \(\mathbb{E}[J]\) is 50 at \(t=0\), 0.66 at \(t=0.8\), and 1.73 at \(t=1.0\). The optimum catches the lineage and the cost collapses. (After that the mean cost climbs again. That is consistent with a sublinear runaway at exact \(v_{\max}\), which this estimate does not prove.)

   The strict case is in better shape. For \(|v_k|>v_{\max}\) and \(t\ge|L_k(0)|/(|v_k|-v_{\max})\), the upper bound on \(\mathbb{E}[L_k]\) is negative, \(\mathbb{E}|L_k|\) is at least a positive multiple of \(t\), and \(\mathbb{E}[J]\) grows like \(t^2\), so the time average diverges. The documented run at \(v=12>v_{\max}=10\) (slope 2.22 against the bound 2) is that case. The bottom line at `:21` already says "faster than", which is the right hypothesis. `OPEN_WORK.md`'s T11 sentence says "faster than" as well.

   Suggested fix: keep the strict speed bound. Replace the second sentence of the theorem with the large-\(t\) statement under \(|v_k|>v_{\max}\), and square only after the lag lower bound is nonnegative. Drop \(|v_k|=v_{\max}\) from the unbounded-growth claim, or give a separate argument for it. In the proof, write the sign: \(\mathbb{E}[\theta_k(t)]<\theta_k(0)+v_{\max}t\) makes \(\mathbb{E}[L_k]\) largely negative only once \(t\) exceeds \(L_k(0)/(|v_k|-v_{\max})\) when the lineage starts ahead. Apply the same sentence, with the opposite sign, to \(v_k<0\). Point S2's claim cell at the same restriction. The \(v=5\) and \(v=12\) simulation sentences can stay; they are the strict cases.

## Should-fixes

1. `theory/DRIFT_SELECTION.md:23` and `:105`, and the same "unresolved factor of 2" clause in the v2.72 note and in S1 (`measurement/CLAIM_MAP_v2.md:86` and `:615`). The coefficient in DS1 is the one in Held, Nourmohammad and Lässig (2014). Their equation 54 is the line that does not follow from their own equations 33 and 52. Record that, and retire "unresolved". The mapping is in the next section. Suggested sentence in place of the unresolved clause: `Their equation 54's slow-driving line is twice the value implied by their equations 33 and 52. That value is DS1. The fast-driving line of equation 54 matches DS1(d).`

2. `theory/DRIFT_SELECTION.md:21`. The fast-fluctuation sentence says the excess over the instantaneous minimum tends to \(\tfrac12\mathrm{Tr}(HQ/\gamma)\). Theorem DS1(d) at `:80` is the accurate statement: the tracking term tends to that, and the excess tends to \(d/(2\beta)+\tfrac12\mathrm{Tr}(HQ/\gamma)\), at fixed \(Q/\gamma\). The static scatter does not go away. Section 8 (`:160`) already treats \(\tfrac12\mathrm{Tr}(HQ/\gamma)\) as the piece the chain cannot remove, which is the right reading. Suggested fix: `its excess over the instantaneous minimum tends to \(d/(2\beta)+\tfrac12\mathrm{Tr}(HQ/\gamma)\), and the second term is the cost of not tracking.`

3. `theory/DRIFT_SELECTION.md:46` and `:52`. \(\varepsilon_{\mathrm{lat}}=\delta^2\beta\lambda_{\max}(1+\mathrm{tr}\,Q/(d D_m))\) is the squared fitness step at a typical lag: \((N|x_e|)^2\sim\varepsilon_{\mathrm{lat}}\) in one coordinate with \(Q=DI\). It is the right small parameter for the linearization of \(\varphi\). It is not the lattice spacing over the scatter. That ratio is \(\delta^2/\mathrm{Var}(L)=\varepsilon_{\mathrm{lat}}/(1+D/D_m)^2\), which gets smaller as \(D\) grows, while \(\varepsilon_{\mathrm{lat}}\) gets larger. The sentence that equates "steps small compared with the scatter" to \(\varepsilon_{\mathrm{lat}}\ll 1\), and the parenthetical that the world's move per substitution is included in \(\varepsilon_{\mathrm{lat}}\), are two further identifications the definition does not earn. The claim that the formula staying within 3% up to \(\varepsilon_{\mathrm{lat}}\approx 1\) makes \(\varepsilon_{\mathrm{lat}}\ll 1\) conservative (`:128`) is a statement about this fitness-step quantity. At \(D/D_m=50\) the cloud is still hundreds of lattice spacings wide. Suggested fix: define \(\varepsilon_{\mathrm{lat}}\) as the fitness-step quantity, and write the geometric ratio next to it.

4. `STATUS.md:3`. The opening clause now says CLAIM_MAP v2.72. The same sentence still says `CLAIM_MAP v2.71 (this branch, not yet merged)`. v2.71 is the selection fold, merged as `c92886a`. This branch is v2.72, and it is the one that is not merged. `main` is `2eeab30` in that sentence; `origin/main` is `c92886a`. `check_fresh` still passes, because `2eeab30` is inside the five-commit window (`c92886a 2eeab30 c04cedd d34df95 a97887e`). Suggested fix: say v2.72 is this branch and not merged, and move the `main` pointer to `c92886a`.

## Nits

1. `theory/DRIFT_SELECTION.md:99`. SA3's Brownian load \(\mathbb{E}[w L^2]=\sigma_\theta^2/(4\alpha V_G)\) is the tracking load of an infinite population. The comparison with \(D/(2\alpha(N-1)D_m)\) is the tracking term of DS1(b). DS1(b) itself is that term plus \(1/(2\beta)\). The curvature cancellation and the \(V_G\leftrightarrow(N-1)D_m\) remark are right once the sentence names the tracking term. The identification \(\sigma_\theta^2=2D\) matches A3's variance rate to the \(\sqrt{2D}\) convention. Suggested fix: `The tracking term of DS1(b) in one coordinate is \(D/(2\alpha(N-1)D_m)\).`

2. `tools/drift_selection_checks.py:103`. The fixation probability and the quadratic \(\Delta J\) are the exact chain. The time step is tau-leaping: at most one substitution per \(\Delta t\), with probability \(1-e^{-R\Delta t}\). The note's \(\Delta t=0.05\) versus \(0.01\) comparison is the right disclosure. "Exact chain" in the docstring and in §7 means exact \(\varphi\), not an exact continuous-time trajectory.

## The factor of 2

Held, Nourmohammad and Lässig, arXiv:1403.1803 (the source of the equations the note cites; Crossref confirms the journal item, doi 10.1088/1742-5468/2014/09/P09029). Fitness \(f=f^\star-c_0(E-E^\star)^2\), stabilizing strength \(c=2NE_0^2 c_0\).

Their Fokker–Planck operator for the trait mean has diffusion coefficient \(\langle\Delta\rangle/(2N)\) in front of \(\partial_\Gamma^2\). The variance rate is \(\langle\Delta\rangle/N\). In the note's convention the variance rate is \(2D_m\), so
\[
D_m=\langle\Delta\rangle/(2N).
\]
That is the identification the note makes, and it is the right one. The peak's Langevin noise is \(\langle\eta(t)\eta(t')\rangle=2\upsilon E_0^2\,\delta(t-t')\) with \(\upsilon=\upsilon_0/E_0^2\), so the variance rate is \(2\upsilon_0\). In the note's convention that rate is \(2D\), so \(D=\upsilon_0\). That identification is right as well. The factor of 2 is not a diffusion-convention mismatch.

Their covariance (equation 30) gives, for strong selection, equilibrium lag variance \(E_0^2/(2c)\) and, in the slow-driving expansion,
\[
\langle\lambda^2\rangle=\langle\lambda^2\rangle_{\rm eq}+\upsilon\,\tau_{\rm eq}(c)\,w(c)/2,
\]
which is their equation 33. Equation 52 defines the scaled adaptive load as \(c\) times that excess. For \(c\gg 1\), \(\tau_{\rm eq}=\tilde\tau/c\) and \(\tilde\tau=2NE_0^2/\langle\Delta\rangle=E_0^2/D_m\), so
\[
2NL_{\rm ad}=\upsilon\tilde\tau/2=D/(2D_m).
\]
Equation 54's macro-evolutionary line writes \(\upsilon\tilde\tau\), without the \(1/2\). That is the whole discrepancy. Equation 54's micro-evolutionary line \(cr^2\) does follow from equation 33, and it is DS1(d): with the Boltzmann match \(\beta h/2=2Nc_0\), the scaled load \(\beta\cdot\tfrac12 h\,\mathrm{Var}(\theta^\star)\) equals \(2Nc_0\) times the peak variance.

DS1(b)'s tracking term, multiplied by \(\beta\), is \(D/(2D_m)\). Same coefficient. The fast limit matches, as the note says. The slow-driving coefficient matches equations 33 and 52, and it matches a direct integration of the diffusion whose stationary variance is their \(E_0^2/(2c)\) (drift \(-2c_0\langle\Delta\rangle L\), noise variance rate \(\langle\Delta\rangle/N\)). Their appendix Langevin writes the drift as \(-\langle\Delta\rangle(2c/E_0^2)L\), which is \(2N\) times that drift, because equation (25) puts \(c/E_0^2=2Nc_0\) into the quadratic term where the fitness (15) has \(c_0\). Integrating the printed Langevin does not recover equation 33 or the equipartition \(2NL_{\rm eq}\simeq 1/2\). It is not a second reading of equation 54.

The coefficient used in the note is the one derived in §4 and checked on the lattice chain. It is also Held's coefficient, once equation 54 is corrected by equations 33 and 52.

## What was checked and holds

DS1, rederived for this review.

- Moran \(\varphi(x)=(1-e^x)/(1-e^{Nx})\), \(x=\alpha\Delta J\), expands as \(\varphi(x)=\tfrac1N\bigl(1-\tfrac{N-1}{2}x+O(N^2x^2)\bigr)\). Pairing \(\pm e\) in the generator, with neutral jump rate \(\mu/(2d)\) along each ray, gives drift \(-D_m\beta\nabla J\) and diffusion coefficient \(D_m\) in front of \(\Delta\), with \(D_m=\mu\delta^2/(2d)\). The neutral substitution rate, summed over \(2d\) rays, is \(\mu\). The Itô noise is \(\sqrt{2D_m}\,dW\): variance rate \(2D_m\). Equation (L) is that Langevin.
- Lag \(L=\theta-\theta^\star\), \(A=D_m\beta H\). For the OU centre, \(\mathrm{d}L=-AL\,\mathrm{d}t+\gamma\theta^\star\mathrm{d}t+\sqrt{2D_m}\,\mathrm{d}W-\sqrt{2Q}\,\mathrm{d}B\). The cross variation of \(L\) and \(\theta^\star\) is \(-2Q\). Stationarity gives \(C=-(A+\gamma I)^{-1}Q\) and \(D_m\beta\,\mathrm{Tr}(HP)=d D_m+\mathrm{Tr}\bigl[A(A+\gamma I)^{-1}Q\bigr]\). Dividing by \(2D_m\beta\) produces
  \[
  \overline{J-J^\star}=\frac{d}{2\beta}+\frac12\mathrm{Tr}\bigl[H(D_m\beta H+\gamma I)^{-1}Q\bigr].
  \]
  Brownian \(\gamma=0\): \(d/(2\beta)+\mathrm{Tr}(Q)/(2\beta D_m)\), and \((d/(2\beta))(1+D/D_m)\) when \(Q=DI\). The Hessian cancels. Constant velocity: mean lag \(-A^{-1}v\), fluctuation \(d/(2\beta)\), tracking cost \(v^\top H^{-1}v/(2\beta^2 D_m^2)\). The general-\(M\) trace \(d/(2\beta)+\mathrm{Tr}(M^{-1}Q)/(2\beta)\) follows by whitening \(L\). The velocity condition \(|v|\ll D_m/\delta=\mu\delta/(2d)\) is \(N\alpha\delta|H\bar L|\ll 1\) at the mean lag, up to \(N/(N-1)\).
- `analytic_checks` on this machine: the closed form matches `solve_continuous_lyapunov` to the \(10^{-9}\) tolerance on all 20 random trials (5 draws, \(\gamma\in\{0,0.3,4\}\), plus anisotropic \(M\)). The fast-world limit and the curvature cancellation both returned OK.

The simulator is the origination–fixation chain, not a numerical integral of DS1. Rates are \((N\mu/(2d))\varphi(\alpha\Delta J)\) with the exact quadratic increment and the exact Moran \(\varphi\). Optimum increments are the Brownian increment or the exact OU transition. Documented full-mode cases, rerun at nice 19 with the seeds in `tools/drift_selection_checks.py`, numpy 2.5.5, match `theory/drift_selection_checks/results_full.json` to every printed digit:

| Case | seed | rerun mean \(\pm\) SE | JSON |
|---|---|---|---|
| BM \(d=1\), \(D/D_m=0\) | 10 | \(25.12988815196078\pm 0.15610732256183107\) | same |
| velocity \(v=0.05\) | 405 | \(38.46404285910527\pm 0.2690895067317643\) | same |
| OU \(\gamma=0.01\), \(D=D_m\) | 310 | \(37.46965590642485\pm 0.1987140767095811\) | same |
| DS2 \(v=5\) | 605 | slope \(-2.1902832615047192\times 10^{-7}\), lag at \(T\) \(14.679999998927705\) | same |
| DS2 \(v=12\) | 612 | slope \(2.2203418149995096\), lag at \(T\) \(698.2674999928051\) | same |

Inside the stated conditions the relative errors in the JSON are the ones the note prints (at most \(+2.6\%\) at \(\Delta t=0.05\), \(+0.4\%\) at \(\Delta t=0.01\)). Those three reruns sit on the formula by \(+0.5\%\), \(+2.6\%\), and \(-0.08\%\).

Scope and wording.

- CX1 stays **OPEN**. The status cell is untouched. The Why cell at `measurement/CLAIM_MAP_v2.md:506` adds a pointer and says section S is not the information floor. S1 is PRIOR ART, S2 PROVED (in-model), S3 and S4 OPEN. No other status cell changes. Tally 334 matches the table (OPEN 87, PROVED 96, PRIOR ART 34, and the unchanged rows).
- The Part 2 hypothesis sentence is byte-identical to `c92886a`, one copy each, in `THEORY.md`, `CORE.md`, `README.md`, and `theory/SELECTION_AXIOMS.md`: `The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.` The new note does not restate it (`theory/DRIFT_SELECTION.md:172`). THEORY §4 is not edited; the THEORY diff is the claim-map version pointer. CORE gains one pointer sentence. The note does not call DS1 a law. Section 8 labels the layer reading as an interpretation.
- Locked prereg and hash files are unchanged against `c92886a`. `git diff --stat c92886a` is the 12 files in the PR, 776 insertions and 13 deletions. A path filter for `PREREG`, `LOCK`, `hash`, `SHA`, `predictions.json`, and `RESULTS.md` is empty.
- Prior art. All 19 DOIs in §5 returned a Crossref work on 22 November 2026 (UTC). Authors, year, container, and pages match the note. Bürger and Lynch 1995 are paraphrased, not mistitled (Crossref title: "Evolution and extinction in a changing environment: a quantitative-genetic analysis"). The equipartition credit is Held's own: their text assigns \(2NL_{\rm eq}\simeq d/2\) to Hartl and Taubes 1998, Poon and Otto 2000, and Tenaillon, Silander, Uzan and Chao 2007, which are their references 42–44. The note reports that attribution and does not edit R1. Sella and Hirsh stay the credit for the stationary weight. Calling the equilibrium-plus-adaptive split prior art, and the \(d\)-dimensional trace a packaging of it, matches what is in that paper.

## Commands

All of these were run from the repo root, on head `93db783`, with `nice -n 19`, after `git fetch origin main` (`origin/main` moved `2eeab30..c92886a`).

- `git diff --stat c92886af97425102878241740b093983885a0106`. 12 files, 776 insertions, 13 deletions. Lock/prereg/hash filter empty.
- `python3 tools/check_fresh.py`. `STATUS.md main is 2eeab30; window: c92886a 2eeab30 c04cedd d34df95 a97887e`. `RESULT: PASS`. Exit 0.
- `python3 tools/check_consistency.py`. THEORY v2.9; CLAIM_MAP latest note v2.72; version pins OK; wording FAILs 0 on 29 maintained docs; section N mismatches 0; tally 334; process-rule FAILs 0; core-rule FAILs 0. Two advisory length warnings (THEORY main text 10569 words, README 1468). `RESULT: PASS`. Exit 0.
- `python3 tools/check_open_work.py`. `union missing from OPEN_WORK.md: 0`. `RESULT: PASS`. Exit 0.
- `python3 -m pytest -q tools`. `179 passed, 1 skipped in 265.13s`. Exit 0. The skip is `tools/test_lean.py:101`, `Lean 4 / lake is not installed`. The other test in that file passed. The PR text's "180 passed" is this suite with the lake test also running. It is not a failure of the diff. This environment did not have pytest, SciPy, or SymPy at the start; those were installed for the run. NumPy after that install is 2.5.5. The documented fits reproduced on that NumPy.
- Crossref `GET https://api.crossref.org/works/<doi>` for the 19 DOIs in §5. All HTTP 200. Seven of the calls were retried after HTTP 429; all seven then returned 200.
- Independent DS2 counterexample, parameters above. Not part of `tools/drift_selection_checks.py`.
