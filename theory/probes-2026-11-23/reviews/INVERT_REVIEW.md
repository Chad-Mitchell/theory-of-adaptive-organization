# Independent hostile review: INVERT_MEMO (inverting the problem)

*Monday 23 November 2026, America/New_York. Reviewer did not write the memo. Reviewed `/workspace/gtao/invert-2026-11-23/INVERT_MEMO.md` and `checks/` against GTAO `main` `d592662` (fresh clone in `/workspace/revinvert`, TMPDIR there, nice 19, deleted after). `THEORY.md` untouched. No PR. Memo fixed in place; edits are marked **[REVIEWER EDIT 2026-11-23]** (14 marks). Independent checks: `invert_review_checks/` (r1–r3, outputs and hashes).*

Labels: **PROVED (in-model)**, **KNOWN**, **CONJECTURE**, **SPECULATION**.

## Summary

| # | Claim | Math | Label in memo | Correct label | Pass? |
|---|---|---|---|---|---|
| 1 | INV-E: long-run min cost = \(E_0\), attained by Nelson's ground-state process; finite horizon = Kappen–Todorov, \(-\lambda\ln Z\); noise→0 = Euclidean least action | correct | PROVED (in-model) from known pieces | **KNOWN** (Donsker–Varadhan 1975; Holland 1978; Fleming 1977; Sheu 1984; Kappen 2005; Todorov 2009) | **PASS on math; FAIL on novelty label (fixed)** |
| 2 | Real-time action a minimum only for bounded-above U before conjugate time; real-time Nelson/Guerra–Morato a stationary point; osmotic sign; positive reweightings, no interference; missing Wick \(i\) | mostly correct | KNOWN | KNOWN | **PASS with one correction**: "bounded above" is neither necessary nor sufficient for a minimum (fixed). GM sign form unverified from the paper text (softened). |
| 3 | Heat floor (`CORE.md:70`) does not map; trap heat 0 vs path KL ω/4; priced-information form (`CORE.md:52`) maps up to KL-vs-MI; equal when reference = average law | correct | new to repo | KNOWN pieces; contrast new to repo only | **PASS** (ω/4 needs γ=1; reference-dependent; `CORE.md:80` already has the zero-heat trap) |
| 4 | Dictionary kT↔ħ, γ/2↔m; CT24 shares = virial, k/(k+2) | correct | relabel | relabel (KNOWN) | **PASS** |
| 5 | Prop R: ruin ≤ ε costs ≥ λ d(1−ε‖p), attained by Doob h-transform | correct, exact | ELEMENTARY | **KNOWN in substance** (Csiszár 1975 I-projection; Doob conditioning as KL-optimal control: Fleming 1977, Chetrite–Touchette 2015) | **PASS on math; novelty only as GTAO bookkeeping** |
| 6 | Circularity moves, not removed | correct, and understated | — | — | **PASS** (sharpened: nothing selects ħ) |

## 1. Theorem INV-E

**Re-derivation (independent).** Stationary \(dX=u\,dt+\sigma dW\), \(\sigma^2=\hbar/m\), reference driftless BM with the same σ and initial law. Girsanov: KL rate \(=\mathbb{E}_\rho|u|^2/(2\sigma^2)\), so \(\hbar\times\) rate \(=\tfrac m2\mathbb{E}_\rho|u|^2\). Stationary Fokker–Planck \(\nabla\cdot(\rho u)=\tfrac{\sigma^2}2\Delta\rho\) gives \(u=u_{os}+v\), \(u_{os}=\tfrac{\sigma^2}{2}\nabla\ln\rho\), \(\nabla\cdot(\rho v)=0\). Cross term \(m\int\rho\,u_{os}\cdot v=\tfrac{m\sigma^2}{2}\int\nabla\rho\cdot v=-\tfrac{m\sigma^2}{2}\int\ln\rho\,\nabla\cdot(\rho v)=0\) (boundary terms vanish under the memo's finite-Fisher, confining assumptions). \(\tfrac m2\int\rho|u_{os}|^2=\tfrac{\hbar^2}{8m}\int|\nabla\rho|^2/\rho=\tfrac{\hbar^2}{2m}\int|\nabla\sqrt\rho|^2\). So \(j=\langle\sqrt\rho|H|\sqrt\rho\rangle+\tfrac m2\int\rho|v|^2\ge E_0\), equality iff \(v=0\), \(\rho=\psi_0^2\), i.e. \(u^*=\tfrac\hbar m\nabla\ln\psi_0\). Signs: Euclidean stake \(+U\) (Lagrangian \(T+U\)) is right; real-time is \(T-U\). Memo `INVERT_MEMO.md` §4 (i)–(v) all check. Note: in 1D, \(\nabla\cdot(\rho v)=0\) with decay forces \(v=0\), so the circulation statement is a \(d\ge2\) statement.

**Is "exactly \(E_0\)" known? Yes, plainly.** \(\tfrac{\sigma^2}{2}\int|\nabla\sqrt\rho|^2\) is the Donsker–Varadhan level-2 rate function of Brownian motion (DV 1975, doi 10.1002/cpa.3160280102), and \(E_0=\inf_\rho[\hbar I(\rho)+\int U\rho]\) is the DV/Feynman–Kac variational formula for the principal eigenvalue. Its stochastic-control form, "principal eigenvalue = optimal long-run cost of a quadratic-cost steering problem", is Holland 1978 (CPAM 31:509, doi 10.1002/cpa.3160310406; memo-era citations of "1977" refer to the tech report) and Sheu 1984 (Stochastics 11:191, doi 10.1080/17442508308833285), using Fleming's log transform (Fleming 1977, AMO 4:329, doi 10.1007/BF01442148). The \(v\)-term (non-reversible part costs extra) is the standard decomposition used in Nelson's energy and in the control representation of conditioned processes (Chetrite–Touchette 2015, J. Stat. Mech. P12001, doi 10.1088/1742-5468/2015/12/P12001). Finite horizon \(-\lambda\ln Z\) is Kappen 2005 / Todorov 2009 / Fleming–Mitter 1982 (doi 10.1080/17442508208833228). Zero noise → Euclidean action is Schilder/Freidlin–Wentzell. **The whole theorem is KNOWN; the only addition is GTAO vocabulary.** Memo relabelled (memo §0 and §4 status line).

**Hostile point the memo underplays.** Nothing in INV-E selects \(\hbar\). For any price λ with \(\sigma^2=\lambda/m\), the minimum is the ground energy of \(-\tfrac{\lambda^2}{2m}\Delta+U\). The same mathematics holds for a thermal Brownian particle with λ = kT. So INV-E is a statement about diffusions and their Feynman–Kac operators; "ħ is the price of a nat" is a matching, not an output. This is a model implication, labelled as such, and the memo now says so (§0).

**Checks.** C2's "6 digits" compares \(E_0\) with \(\langle T\rangle+\langle U\rangle\) computed from the same eigenvector: a grid consistency check, not a test. The independent evidence is the SDE time average (harmonic 0.5043 vs 0.5, ~0.9% Euler bias; quartic 0.6698 vs 0.6680; |x| 0.8085 vs 0.8086) and the 2D circulation family (c=0.8: 1.3258 vs formula 1.3200). Reviewer check r1: 2000 random trial densities in the quartic well, min \(j-E_0=+0.0073\) (never negative).

## 2. Real time (Finding N)

- Jacobi: Hamilton's action is a minimum only up to the first conjugate point (Gray & Taylor 2007, doi 10.1119/1.2710480). C4 reproduces (sign change between T=3.1 and 3.2, π).
- **Correction.** The memo's "a minimum only when the potential is bounded above" (`INVERT_MEMO.md` §0 bullet 2, §3 table) is wrong as a minimality condition. Reviewer check r3: harmonic \(U=x^2/2\) (unbounded above) is a true minimum for \(T<\pi\); \(U=\cos x\) (bounded above) has a conjugate point at π about its minimum. Bounded-above \(U\) only makes the real-time stake \(-U\) bounded below, which CT24's \(\varphi_i\ge0\) form (`THEORY.md:474`) needs. Fixed.
- Guerra–Morato \(\tfrac m2(v^2-u^2)\): the reviewer could not read the 1983 paper (Crossref title verified: "Quantization of dynamical systems and stochastic control theory"). It is the standard reading (\(\tfrac m2 DX\cdot D_*X\)), but Yasue 1981 uses \(+u^2\). The conclusion (stationary point, not a minimum) holds in every formulation because the potential enters as \(-U\) (Pavon 1995, doi 10.1063/1.531187). Softened.
- Positivity/no interference: correct (Perron–Frobenius; \(dQ^*/dP>0\)). "Missing Wick \(i\)": correct and KNOWN (Zambrini 1986's Euclidean quantum mechanics is built on exactly this). Plainly: a real nonnegative cost cannot produce signed amplitudes; this is a known barrier, not a GTAO discovery.

## 3. Heat floor vs priced information

- `CORE.md:70` (heat ≥ kT × net learning rate, bipartite) and `CORE.md:52` (priced sum; memory coordinate is mutual information) read as quoted.
- C5b: equilibrium OU trap, heat rate +0.0012 (0), path-KL vs free BM 0.2496. Analytic rate is \(\omega/(4\gamma)\); C5b has γ=1. The KL is reference-dependent (0 against the trap's own law). `CORE.md:80` already states that a conservative trap has vanishing ongoing heat, so the only addition is the KL contrast. PASS.
- C5a golden formula \(\mathbb{E}_\theta\mathrm{KL}(Q_\theta\|P_0)=I+\mathrm{KL}(\bar Q\|P_0)\): identity to 1e-10; KNOWN (Tishby–Polani; rate–distortion). PASS.
- Substantive point (kept in memo §6 "Open"): what maps is a KL of self-steering against a fixed reference. GTAO's distinctive term, information *about* an external world, has no counterpart. So the inversion does not reach the part of the cost of judgment that is GTAO's own.

## 4. Dictionary and virial

- Overdamped Langevin, λ = kT, \(\sigma^2=2kT/\gamma\): \(kT\,u^2/(2\sigma^2)=\tfrac\gamma4u^2\); quantum: \(\hbar\,u^2/(2\hbar/m)=\tfrac m2u^2\). So \(m\leftrightarrow\gamma/2\), \(\hbar/m\leftrightarrow2kT/\gamma\). Consistent. KNOWN in substance (Nelson's ν = ħ/2m vs Einstein D = kT/γ).
- Virial: dilation \(x\to sx\) scales the Fisher term as \(s^{-2}\) and \(U\) as \(s^k\); CT24's identity \(\sum a_i\,\text{share}_i=0\) (`THEORY.md:474`) gives \(-2s_{\rm info}+k s_U=0\), so \(s_{\rm info}=k/(k+2)\). Matches the quantum virial theorem \(2\langle T\rangle=k\langle U\rangle\). C2: 0.50000, 0.66667, 0.33333. PASS; relabel, as the memo says. CT24's \(\varphi_i\ge0\) requires \(U\ge0\).

## 5. Proposition R

- Proof: data processing onto \(1_A\) gives \(\mathrm{KL}(Q\|P)\ge d(Q(A)\|p)\); \(d(\cdot\|p)\) increases on \([p,1]\), so the minimum is at \(Q(A)=1-\varepsilon\); the mixture of conditionals attains it. h-transform \(h=aq+b(1-q)\) is the martingale \(\mathbb{E}[dQ^*/dP\mid\mathcal F_t]\). Correct.
- Reviewer check r2: lazy walk, absorbing 0, exact computation: KL of the h-transform = 0.5041136665 = \(d(1-\varepsilon\|p)\); \(Q(\text{ruin})=0.0500000000\). C3 (diffusion, MC) 0.2204±0.0007 vs 0.2215, 1.5 s.e. low with ruin 0.0506 > 0.05: discretization, consistent.
- **New?** Not to anyone working in large deviations or KL control. It is a two-point I-projection (Csiszár 1975) plus Doob conditioning as the KL-optimal control (Fleming 1977 gives \(-\lambda\ln p\) as a control value; Chetrite–Touchette 2015 in general). New only to the repo, where it usefully prices the ruin cap that `theory/NOVELTY_NOTE_2026-11-21.md:23` says Ortega–Braun lacks. Relabelled KNOWN in substance.

## 6. Circularity

`theory/FREEZE_OR_HOLD_FLOOR_2026-11-23.md:176` and `theory/PHYSICS_CHAIN_2026-11-23.md:86-87` read as quoted. Agree: the bath and temperature are swapped for a reference measure, a noise scale and a potential, and ħ is put in by matching. The circularity moves; it is not removed. PASS.

## 7. Repo-grep claim (memo §1)

**FAIL, fixed.** The memo says Ortega/Braun has no hits. It is credited at `theory/GENERAL_THEOREM.md:157,376`, `theory/NOVELTY_NOTE_2026-11-21.md:23`, `theory/DERIVATION_CHAIN.md:157`, `reviews/master-equation_2026-11-19/REVIEW.md:97`. Donsker–Varadhan 1975 is at `theory/NON_GAUSSIAN_FLOOR_2026-11-23.md:54,243`. The other terms (Kappen, Feynman–Kac, Guerra, Zambrini, Girsanov, Wick, stochastic mechanics) do have no relevant hits. Other cited lines check: `CORE.md:7,27,52,70,80`; `THEORY.md:283,474`; `theory/TRANSPORT_BARRIER_2026-11-23.md:47,97`; `theory/ACTING_LOOP_2026-11-22.md:109`; `theory/MASTER_EQUATION.md:9-11`; `reviews/master-equation_2026-11-19/REVIEW.md:137-141`.

## 8. Checks and DOIs

- `checks/SHA256SUMS` all OK. C1–C5 rerun at nice 19: outputs **byte-identical**.
- All 19 memo DOIs resolve on api.crossref.org with matching titles, authors, venues and years (Nelson 1966; Guerra–Morato 1983; Léonard 2014; Chen–Georgiou–Pavon 2021; Kappen 2005; Todorov 2009; Onsager–Machlup 1953; Zambrini 1986; Ortega–Braun 2013; Reginatto 1998; Gray–Taylor 2007; Csiszár 1975; Tishby–Polani (Crossref 2010); Donsker–Varadhan 1975; Yasue 1981; Mitter–Newton 2003; Frieden 1989; Touchette–Lloyd 2000; Schrödinger 1931 EPJ H translation by Chetrite, Muratore-Ginanneschi & Schwieger 2021, vol. 46; Crossref shows no page or article number, so "46:28" is not confirmed there).
- Added prior art, verified: Fleming 1977 (10.1007/BF01442148); Holland 1978 (10.1002/cpa.3160310406); Fleming–Mitter 1982 (10.1080/17442508208833228); Sheu 1984 (10.1080/17442508308833285); Fleming–Sheu 1985 (10.1007/BF01442207); Dai Pra 1991 (10.1007/BF01442404); Pavon 1995 (10.1063/1.531187); Chetrite–Touchette 2015 (10.1088/1742-5468/2015/12/P12001).

## 9. Verdict

**Relabel, with a modest corollary. Not a way in.** Every physics statement is correct and known. Framing quantum ground states, and quantum dynamics, as optimal stochastic control has a 45-year literature (Fleming, Holland, Sheu, Guerra–Morato, Yasue, Zambrini, Pavon, Dai Pra, Chen–Georgiou–Pavon). GTAO's cost, restricted to "KL to a reference + potential stake", *is* that control problem, so of course its minimum is \(E_0\). What is useful for the repo: (a) a clean map of where the dictionary fails (real time, the factor \(i\), and, most important for GTAO, information about an external world has no counterpart); (b) Prop. R as a price-free number for the ruin cap. Neither reaches past known physics. Model implication, stated plainly: if physics is read as the minimum of a cost of judgment, the reading works only for imaginary-time and equilibrium physics, and the price ħ is put in, not derived. Open puzzles worth keeping: whether any real cost can carry the phase (the literature says no for real nonnegative costs), and whether the reference measure can be chosen by a cost.

## 10. For Chad (plain words, audio)

The inverted idea checks out mathematically, but it's already known. If you charge a jiggling particle for steering it away from pure randomness, the cheapest way to run it costs exactly the quantum ground-state energy. Mathematicians showed this between 1975 and 1985, and the physics follows from Nelson's work in 1966. So our cost reproduces known physics instead of finding a new door. It also stops at three walls. It works only in imaginary time, not in the real time where quantum interference lives. It doesn't explain why the price is Planck's constant, because any price works the same way. And it never touches the part that's really ours, which is information about an outside world. The one small piece worth keeping is a clean price for the ruin cap, counted in bits, and even that is textbook. This is a map of the walls, not a way through them.
