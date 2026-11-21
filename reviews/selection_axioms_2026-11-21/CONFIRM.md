# Confirm of the selection-axioms note (PR #143)

Blind confirm of `selection-axioms-2026-11-21`. The incoming head was `0b71516e7c9d90e9f10b561615a340ff3917bc79`. This pass wrote none of that commit. It did push the wording and portability fixes listed below, after checking them against `theory/SELECTION_AXIOMS.md`, `tools/selection_axioms_checks.py`, `measurement/CLAIM_MAP_v2.md` rows R1–R3, `CORE.md` §8, `THEORY.md` §4, `core/bridge_2026-11-21/SELECTION.md`, and `theory/DYNAMICS.md` CL19. No locked prereg, hash, or `LOCK` file is in the diff. Same bot family as the other passes; not a human expert.

**READY.** At `0b71516` the six blockers and the nine should-fixes were in the note. Four sentences were still stronger than the bridge file, the path simulation, or Fisher’s theorem, and the Green-function integral crashed on NumPy 1.26. Those are corrected in this commit. The hypothesis sentence is unchanged.

## Fixes pushed in this confirm

1. Occupation. The note said the checks file recovers the Dixit occupation by simulating the reset process. The simulation checks two moments. It does not histogram \(\rho(x)=(b-|x|)/b^2\). The Green-function block plugs in that closed form. The sentence now says so.
2. Bridge attribution. Corollary SA1c, §0, §3, §11, the `CORE.md` §8 pointer, and row R1 said the \(\nu\) identification was already the bridge’s. `core/bridge_2026-11-21/SELECTION.md` still writes \(\beta=\alpha(N_e-1)\) as the general factor. The note now says that, and uses \(\beta=\alpha\nu\) in its own corollary. The bridge file was not edited.
3. Fractional excess. The ratio to the qualification band is the ratio of the typical *fractional* excess to that fractional band, \(d/20\).
4. Shahshahani and Fisher. The metric is Shahshahani’s. Fisher’s fundamental theorem is the infinite-population variance statement. Neither is a derivation of \(\pi\).
5. NumPy. `np.trapezoid` is NumPy 2. This environment had 1.26.4, which has `np.trapz`. The integral uses whichever name exists. Row R1’s graph is the note’s graph: connected, undirected, equal mutation clocks.

`theory/SELECTION_AXIOMS.md` is 4,988 words by `wc -w` (4,905 at `0b71516`).

## 1. Blockers and should-fixes

| Item | At `0b71516` | After this confirm |
|---|---|---|
| B1. Sella & Hirsh eqs. 11–13 are the fixed-drift load for fitness uniform on (0,1), not \(d/(2\beta)\). | Fixed. The §7 bullet is the required sentence. | Unchanged. Checked against the PNAS text: eq. 12 is mean fitness \((\nu+1)/(\nu+2)\); the sentence after eq. 13 says the load is approximately \(1/\nu\); multidimensional Fisher’s geometric model is deferred. |
| B2. Moran \(\alpha(N-1)\); diploid multiplicative \(\alpha(2N-1)\), an approximation; haploid Wright–Fisher \(2(N-1)\) unused; \(N\mu\ll 1\); absolute excess \(d/(2\beta)\) separate from the fractional form; \(N_e\) is \(\nu\). | The formulas match the required sentences. Row R1 has both excesses and \(N_e=\nu\). The header still said the corrected corollary was already in the bridge. | The formulas are unchanged. The note, the core pointer, and row R1 now say the bridge file still writes \(\alpha(N_e-1)\). |
| B3. “Strongly selected” is not defined as the smallness of the remainder. The theorem is the formula. The core pointer does not list premises under which the formula is false as if they gave \(d/(2\beta)\). | Fixed. §0, §10, and `CORE.md` §8 match the required text, except the core’s “bridge’s corollary, with \(N_e\) equal to \(\nu\)” still read as a claim about the bridge file. | §0 and §10 unchanged. The core pointer now separates the bridge’s formula from the factor the bridge file still writes. THEORY §4 still states near-minimization as a principle. |
| B4. SA2-A–C and the theorem name one process: zero discount, lumpy coordinate off the substitution chain, optimum moves only in that coordinate, reset of that coordinate only, \(N\mu\ll 1\) together with \(t_{\mathrm{mix}}(y)\ll b^{\star 2}/\sigma^2\), and \(d=\dim y\). | Fixed. Both the assumption and the theorem carry the list. The failure list in “When SA2 is not claimed” matches. Row R2’s **PROVED (in-model)** is the conditional sum. | Unchanged. The duplicated list is load-bearing. See holdability. |
| B5. SA-P1 kills on both sides, and on a non-positive remainder, with a preregistered count. The factor of three is a placeholder. Two points are not a kill. | Fixed. §9 has the required kill, with “(Corollary SA1c)” where the review said “(blocker 2)”. Row R3 is **OPEN** and states the two-sided kill, the non-positive remainder, \(n_{\min}\), the slope interval, and the placeholder. | Unchanged. |
| B6. The occupation is not derived by drawing from the density the check assumes. | The inverse-CDF docstring is the required label. The prose then said the file recovers the occupation by simulation. | Fixed. The prose matches the two moment checks. |
| S1. No leading bar before \(\mathbb{E}\) in the SA2 display. | The reviewed `align*` used `&` before `\;=`. Neither that commit nor `0b71516` has a bar before `\mathbb{E}`. The current displays are the expectations the proof uses. | Unchanged. |
| S2. A birth rate linear in cost does not give the exponential weight. \(\alpha\) is constant on the graph. Local linearity is SA1b only. The fractional form needs \(J^\star>0\). | Fixed in A2-L. | Unchanged. |
| S3. Quote \(d/(2\beta)\) in uniform-lattice coordinates, or whiten. T27’s raw log-rate grid did not give the excess. | Fixed in SA1b. The trace identity is correct. | Unchanged. |
| S4. For quadratic \(J\), the mean Malthusian gradient equals the gradient at the mean. Lande’s gradient of log mean Wrightian fitness carries \(1/(1+2\alpha w V_P)\). \(V_G\) is not \(V_P\). \(\sigma_\theta\) is a diffusion coefficient; A3’s \(\sigma^2\) is a variance rate. | Fixed in the SA3 proof. The Gaussian factor matches the integral of \(r=\exp(-\alpha w(\theta-\theta^\star)^2)\) against a normal phenotype. | Unchanged. |
| S5. Price 1970 is the discrete covariance identity plus transmission. The Malthusian limit used here does not give the distance to the minimum. | Fixed. | Unchanged. |
| S6. Orr 1998 is the distribution of factors fixed. The dimensional fall in the chance a mutation is beneficial is Fisher 1930. Neither is \(d/(2\beta)\). Fisher 1930 has no Crossref DOI. | Fixed. | Unchanged. |
| S7. Chalkley, M., with the title. JEDC title and pages beside the DOI. Coefficient 6 was not checked against the printed equations. | Fixed in §4 and the reference list. | Unchanged. |
| S8. Mustonen & Lässig 2010 is a fitness-flux theorem. This note uses none of their constants. | Fixed. | Unchanged. |
| S9. The SA1 proof is detailed balance. Iwasa 1988 is the free-fitness Lyapunov function, and the proof does not use it. | Fixed. | Unchanged. |

## 2. Exactness

The hypothesis sentence is byte-identical in `theory/SELECTION_AXIOMS.md`, `CORE.md`, and `THEORY.md`:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

“Bill” does not appear in the note or on the core page. “Theory of everything” appears once, as a negation.

**Exponents.** Sella & Hirsh Table 1 and the paragraph containing their eq. 5 set \(\nu_{\mathrm{Moran}}=N-1\), \(\nu_{\mathrm{WFh}}=2(N-1)\), and \(\nu_{\mathrm{WFd}}=2N-1\) for diploid Wright–Fisher with multiplicative fitness within a locus. Their Wright–Fisher fixation formula is an approximation. The introduction’s regime is \(N\mu\ll 1\). The note’s Moran algebra gives \(\varphi_{j\to i}/\varphi_{i\to j}=\rho^{N-1}\) and \(\beta=\alpha(N-1)\). The diploid line is their approximation, and the note does not use haploid Wright–Fisher. Corollary SA1c then sets \(N_e=\nu\), so \(\beta=\alpha N_e\), and says \(\alpha(N_e-1)\) is the Moran exponent only when \(N_e\) is census size.

**Absolute and fractional.** SA1b is \(\mathbb{E}[J]-J^\star=d/(2\beta)\). The fractional statement is \((\mathbb{E}[J]-J^\star)/J^\star\approx d/(2\sigma N_e)\), with \(\sigma\) evaluated at \(J^\star>0\). The \(d/20\) ratio is that fractional excess over the fractional band \(\varepsilon=10/(\sigma N_e)\).

**Sella & Hirsh credit.** \(d/(2\beta)\) is equipartition under their stationary weight. It is not the load in eqs. 11–13.

**SA2.** The sum is linearity of expectation on one process, under the list in B4. The operational term is \(\sqrt{kw\sigma^2/6}\). The long-run rate including lumps is twice that. Both displays are those expectations. The coefficient 6 is CL19’s renewal value. This pass did not re-read it from Dixit’s or Chalkley’s equations. The note already says that.

**SA-P1.** Kill if the lag-corrected fractional excess is above \(3\times d/(2\sigma N_e)\) in more than the preregistered count, or below one third of the target, or not positive. The log–log slope’s preregistered interval kills the scaling when it misses \([-1.5,-0.5]\). The factor of three is not the locked factor of 10. Status **OPEN**.

**Dixit occupation.** A path of driftless Brownian motion, reset to 0 at exit from \([-b,b]\), with a Brownian-bridge exit correction, gave \(\mathbb{E}[x^2]=0.681\) against \(b^2/6=0.667\) (relative error 0.022) and \(\mathbb{E}[|x|]\) with relative error 0.011, at \(b=2\), \(\sigma^2=1\), \(dt=4\times 10^{-4}\), \(3\times 10^6\) steps. That is a moment check. Many densities share those two moments. The Green jump uses the closed-form derivatives, so it cannot fail independently of the formula that was plugged in.

T27’s official record is untouched: P1 3/3, P2 3/3, P3 0/3, not rescued. Locked `PREREG.md` SHA-256 `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994`, 10047 bytes. `predictions.json` SHA-256 `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3`, 2246 bytes. Both match `LOCK.txt`.

THEORY §4 still calls near-minimization a principle, untested and not refuted. This note does not edit that section.

### Runs

- `nice -n 19 python3 tools/selection_axioms_checks.py`: `ALL SA CHECKS PASS (28)`. Exit 0. The 28 lines are five isotropic equipartition Monte Carlos, three trace identities, six closed-form Green-function identities, two reset-process moments, one labeled inverse-CDF moment, three CL19 identities, the first-order condition at \(b^\star\), the SA2 sum of means, the SA3 cancellation, and five Moran fixation ratios.
- `python3 tools/check_fresh.py`, `tools/check_consistency.py`, `tools/check_open_work.py`: each `RESULT: PASS`. Consistency tally 330, wording FAILs 0 on the 29 maintained docs.
- `python3 -m pytest -q tools`: 175 passed, 1 skipped, in 251.36 s, on NumPy 2.5.5 after the shim. The skip is `tools/test_lean.py`, Lean 4 / lake not installed. The review’s 173 passed was the suite before the two occupation tests added in `0b71516`.

### DOIs on Crossref, 21 November 2026

Every DOI printed in the note. Eighteen resolve. Titles, years, and page starts match. Pairs that share a paper (Lande, Bürger & Lynch, Orr, each with a `10.2307` JSTOR DOI) are the same articles. Fisher 1930 is a book and has no Crossref DOI, as the note says.

| Item | DOI | Result |
|---|---|---|
| Sella & Hirsh 2005 | 10.1073/pnas.0501865102 | *PNAS* 102:9541–9546. Title matches. Abstract: steady-state distribution of fixed genotypes, and the load. |
| Lynch et al. 2016 | 10.1038/nrg.2016.104 | *Nature Reviews Genetics* 17:704–714. Title matches. Crossref gives Thomas’s name as W. Kelley; the note’s “W. K.” is that initial. |
| Shahshahani 1979 | 10.1090/memo/0211 | *Memoirs of the AMS* 17, no. 211. Title matches. |
| Dixit 1991 *RES* | 10.2307/2298051 | *The Review of Economic Studies* 58:141. Title matches. |
| Dixit 1991 *JEDC* | 10.1016/0165-1889(91)90037-2 | *Journal of Economic Dynamics and Control* 15:657–673. Title matches. |
| Chalkley 1997 | 10.1016/s0165-1765(97)00222-x | Author Martin Chalkley. *Economics Letters* 57:189–195. Title: “An explicit solution for dynamic menu costs with zero discounting.” |
| Lande 1976 | 10.1111/j.1558-5646.1976.tb00911.x | *Evolution* 30:314–334. |
| Lande JSTOR | 10.2307/2407703 | Same article, page start 314. |
| Bürger & Lynch 1995 | 10.1111/j.1558-5646.1995.tb05967.x | *Evolution* 49:151–163. |
| Bürger & Lynch JSTOR | 10.2307/2410301 | Same article, page start 151. |
| Ohta 1973 | 10.1038/246096a0 | *Nature* 246:96–98. Title matches. |
| Kimura 1968 | 10.1038/217624a0 | *Nature* 217:624–626. Title matches. |
| Monderer & Shapley 1996 | 10.1006/game.1996.0044 | *Games and Economic Behavior* 14:124–143. Title: “Potential Games.” |
| Iwasa 1988 | 10.1016/s0022-5193(88)80243-1 | *Journal of Theoretical Biology* 135:265–281. Title matches. |
| Mustonen & Lässig 2010 | 10.1073/pnas.0907953107 | *PNAS* 107:4248–4253. Abstract: the fitness-flux theorem generalizes Fisher’s theorem to processes that include mutations, genetic drift, and time-dependent selection. |
| Orr 1998 | 10.1111/j.1558-5646.1998.tb01823.x | *Evolution* 52:935–949. Title is the distribution of factors fixed during adaptive evolution. |
| Orr JSTOR | 10.2307/2411226 | Same article, page start 935. |
| Price 1970 | 10.1038/227520a0 | *Nature* 227:520–521. Title: “Selection and Covariance.” |

## 3. Holdability

The sentence a reader can hold is the plain-words paragraph of §0, together with four numbers: absolute excess \(d/(2\beta)\), fractional excess \(d/(2\sigma N_e)\) with \(N_e=\nu\), operational lag \(\sqrt{kw\sigma^2/6}\) and total rate twice that, and a two-sided placeholder kill. The rest is the proof, the credit, and the same caveat said again.

Cuts that lose no honesty, not made in this pass:

1. Do not cut the six SA2 conditions out of either SA2-C or the theorem. They are the same list twice, about 80 words, and both copies are what makes the sum a claim about one process. Cutting one reopens B4.
2. Do not cut the §10 sentence that the theorem is the formula, or §0’s sentence that THEORY §3’s meaning of strongly selected is unchanged. Both were required.
3. §7’s three “see §5 / see §6” bullets (Lande, Bürger & Lynch, Mustonen; Price; Orr). 42 words. The claims stay in §5 and §6.
4. The last sentence of §0, beginning “If a reviewer reads only the formulas.” 24 words. It is tone. The sentence before it, that the packaging is what is new, stays.
5. In §8, the bullets that only repeat §0, §2, §6, or §11: monotone and linear birth (40), the strong-mutation list (20), finite time (17), T27 (14), and the empirical bet (24). Keep the kelvin bullet, the negation that this is not a theory of everything, the ruin-cap bullet, and a short clause that the note does not edit THEORY.md. About 115 words.
6. §3’s “Closeness under the formula” repeats two sentences already in §0 and §10 (“the formula plus \(\sigma N_e\gg d\)”, and the operational meaning unchanged). About 30 words. Keep the \(d/20\) ratio and the Lynch credit.
7. §12 can be the two filenames and the word **NUMERICAL**. About 37 words. The moment-versus-density limit now sits in §4.
8. In §5, the Lande and Bürger page-and-DOI parentheticals duplicate the reference list. About 60 words. Leave author and year. Do not cut the §4 Dixit and Chalkley parenthetical: should-fix 7 required it there.

Those cuts are about 310 words, from 4,988 to about 4,680. They do not make the note something one holds in one head. The part that can be held is §0’s plain-words paragraph, Corollary SA1c, the two SA2 displays, and the SA-P1 kill. Sections 5 through 8 and the reference list are the credit and the limits, and they earn their place as a supplement, not as a second statement of the result.

## 4. Open items

- `core/bridge_2026-11-21/SELECTION.md` still says the diploid line follows by the same argument and that \(\beta\) is population size times \(\alpha\), and it still writes \(\beta=\alpha(N_e-1)\). T27’s Moran run, \(N=201\) and \(\beta=\alpha(N-1)\), is the right Moran factor and was not touched. This note now disagrees with the bridge’s general sentence on purpose, and says so. Editing the bridge was left for a later pass.
- The reset-process moment sits 2.2% above \(b^2/6\), inside a 3% band. A histogram of \(\rho\) is not part of the check.
- The holdability cuts above are not applied.

## Dated note (21 November 2026, evening ET, America/New_York; branch `selection-fold-2026-11-21`)

The first open item is addressed in this later pass: `core/bridge_2026-11-21/SELECTION.md` now states the population model explicitly (haploid Moran \(eta=lpha(N-1)\); diploid Wright–Fisher \(eta=lpha(2N-1)\), an approximation; haploid Wright–Fisher \(2(N-1)\) unused). The official T27 Moran run, \(N=201\) and \(eta=lpha(N-1)\), was not touched, and no locked prereg or hash file was edited. The holdability cuts named in §3 were applied in the same pass. The reset-process histogram remains open.
