# ADDENDUM to the antifragility turnover preregistration

Written Sunday 22 November 2026, after commit `74e9b197e26a2b70d72503a3c1693f78ec7380c8` (the file `PREREG.md` only) and before any script, grid value, or Monte Carlo estimate. `PREREG.md` is not edited. The predictions below are scored with the arms already frozen there. No parameter in that file is moved.

Three questions are added. They do not replace P1–P7. A biological or physical name with no computed consequence in class AF is **METAPHOR**. A citation is **KNOWN** only for what a fetched source states. A mechanism that is not derived inside class AF is **CONJECTURE**.

## A. Heat: three different rates

The locked accounting in `PREREG.md` §1 charges every living unit the heat of its installed precision, \(kT \cdot a \cdot v \cdot c \cdot q_i\), whether or not alignment has decayed, and it charges the Gaussian stock \(kT \cdot \tfrac12 \log(1 + v c q_{\mathrm{new}})\) once per rebuild. That continuous heat does not depend on \(\alpha\). The questions below keep that accounting as the one inside \(J\), and they name two other rates so they are not silently substituted for it.

**Installed heat inside \(J\).** For a homogeneous unit, \(Q = kT\, a\, v\, c\, q\) each, continuous heat \(n Q\), stock rate \(n \sigma \cdot kT \cdot \tfrac12 \log(1+v c q)\). Their sum is
\[
H_J(\sigma) = n\, kT\, a\, v\, c\, q + n\sigma \cdot kT \cdot \tfrac12 \log(1 + v c q).
\]
On \((0,\infty)\) the heterogeneous continuous heat is constant as well: the stationary type law does not depend on the scale \(\sigma_s\) (`PREREG.md` §1), so \(\mathbb{E}[q]\) does not, and the expected stock per failure does not. The failure rate does. \(H_J\) on A2 means continuous heat plus expected stock rate, with the non-heat build cost \(b\) left out of \(H_J\).

**Realized learning flow.** At the mean-field error \(\varepsilon = v/(1+v\,\mathbb{E}\Phi)\),
\[
Q_{\mathrm{flow}} = kT\, a\, \frac{v-\varepsilon}{\varepsilon} = kT\, a\, v\, \mathbb{E}\Phi.
\]
This is \(kT\) times the learning rate of the effective channel. For the homogeneous mean-field pool at the cap, \(\mathbb{E}\Phi = \Gamma\, \sigma/(\sigma+\delta)\) with \(\Gamma = v n c q\), so
\[
Q_{\mathrm{flow}}(\sigma) = kT\, a\, \Gamma\, \frac{\sigma}{\sigma+\delta}.
\]

**Matched-error installed heat.** Hold the error at the fully aligned mean-field error and scale the installed precision. Homogeneous, common alignment \(r = \sigma/(\sigma+\delta)\): the cap pool has effective precision \(\Gamma r\), and the installed heat that produces effective precision \(\Gamma\) (the fully aligned pool) is the cap heat divided by \(r\),
\[
Q_{\mathrm{match}}(\sigma) = kT\, a\, \Gamma\, \frac{\sigma+\delta}{\sigma}, \qquad \sigma > 0.
\]
Heterogeneous: let \(\Phi_{\mathrm{full}}\) be \(\mathbb{E}\Phi\) at \(\alpha = 1\) with the stationary type law, and let \(H_{\mathrm{cap}}\) be the continuous installed heat of that law. Then \(Q_{\mathrm{match}}(\sigma) = H_{\mathrm{cap}}\, \Phi_{\mathrm{full}} / \mathbb{E}\Phi(\sigma)\) for \(\sigma > 0\).

**Re-optimized precision (arm A14, mean-field, homogeneous, not a rescore of P1).** Installed precision \(\varphi \in [0, c]\) per unit is chosen at the mean alignment \(r\), instead of being frozen at \(c\). Effective precision \(n r \varphi\), heat \(kT\, a\, v\, n\, \varphi\), mean-field loss \(w v / (1 + v n r \varphi)\). Upkeep and build are not in this arm. Uncapped interior stationary point:
\[
\varphi^\star(r) = \frac{1}{v n r}\left(\sqrt{\frac{w v r}{kT a}} - 1\right),
\]
defined when the square root exceeds 1, and heat
\[
H^\star(r) = \sqrt{\frac{kT a\, w v}{r}} - \frac{kT a}{r}.
\]
The cap projection is \(\varphi = \min(c, \max(\varphi^\star, 0))\). Differentiating the uncapped heat gives
\[
\frac{d H^\star}{dr} < 0 \quad\text{exactly when}\quad r > \frac{4 kT a}{w v},
\]
and \(H^\star = 0\) (blind) when \(r \le kT a / (w v)\). Between those two alignments the uncapped heat rises with alignment. Where the cap binds, heat equals the cap heat and does not fall any further.

## B. Predictions on the heat

**P8.** On A0, \(H_J(\sigma)\) is strictly increasing in \(\sigma\) and the continuous part is constant. On A2, for every \(\sigma > 0\), continuous heat is constant in \(\sigma\) and \(H_J\) is strictly increasing. Shock-driven turnover in the locked accounting does not lower the long-run heat. It raises the stock rate. The term that falls in P1, if P1 holds, is the loss, not \(H_J\).

**P9.** On A0, \(Q_{\mathrm{flow}}\) is strictly increasing in \(\sigma\) and \(Q_{\mathrm{match}}\) is strictly decreasing on \((0,\infty)\). The same monotonicity is predicted for A2's \(Q_{\mathrm{flow}}\) and \(Q_{\mathrm{match}}\). "Re-aligned units need less learning flow" is true of \(Q_{\mathrm{match}}\) and false of \(Q_{\mathrm{flow}}\). The locked heat inside \(J\) is neither of those two curves.

**P9b.** On A14, with the frozen \(kT, a, w, v, n, c\), uncapped heat is zero for \(r \le kT a/(w v)\), rises with \(r\) until \(r = 4 kT a/(w v)\), and falls with \(r\) after that, until the cap binds. The checker prints the two thresholds from the display and the smallest \(r\) at which \(\varphi^\star(r) \ge c\), if any, on a grid \(r = i/200\) for \(i = 1,\ldots,199\). A14 is not used to score P1.

## C. Convexity, and where Jensen points

Convexity of a cost is not a gain from volatility. In `theory/ROBUSTNESS.md` §6 a cost concave in the stressor gains from variation (Jensen: \(\mathbb{E}[J(\sigma)] \le J(\mathbb{E}\sigma)\)). A convex cost does the opposite. The predictions name the sign of the second derivative and the Jensen direction separately.

Homogeneous mean-field, constants of `PREREG.md` §2, \(r(\sigma) = \sigma/(\sigma+\delta)\), \(\Gamma = v n c q\):
\[
J_{\mathrm{mf}}''(\sigma) = \frac{2 w v \Gamma \delta}{(1+\Gamma r(\sigma))^2 (\sigma+\delta)^3}\left(1 + \frac{\Gamma \delta}{(1+\Gamma r(\sigma))(\sigma+\delta)}\right)
\]
for \(\sigma \ge 0\). Every factor is positive at the frozen numbers, so this second derivative is positive on \([0,\infty)\). The loss term carries the whole second derivative; \(n B \sigma\) is linear. Therefore \(J_{\mathrm{mf}}\) is strictly convex on \([0,\infty)\). For any non-degenerate law of \(\sigma\) on that half-line,
\[
\mathbb{E}[J_{\mathrm{mf}}(\sigma)] > J_{\mathrm{mf}}(\mathbb{E}\sigma).
\]
There is no subinterval on which homogeneous \(J_{\mathrm{mf}}\) is concave, and no Jensen gain for that cost.

The same composition makes the mean-field loss strictly convex. The realized flow is the opposite shape:
\[
Q_{\mathrm{flow}}''(\sigma) = kT\, a\, \Gamma \cdot \frac{-2\delta}{(\sigma+\delta)^3} < 0,
\]
so \(Q_{\mathrm{flow}}\) is strictly concave on \([0,\infty)\) and a mean-preserving spread lowers it. That lowering is a loss of average alignment, because \(\sigma/(\sigma+\delta)\) is concave. It is not a fall in \(H_J\) and not a fall in \(J_{\mathrm{mf}}\).

Matched-error heat on A0:
\[
Q_{\mathrm{match}}''(\sigma) = kT\, a\, \Gamma \cdot \frac{2\delta}{\sigma^3} > 0 \quad (\sigma > 0).
\]
A spread raises average \(Q_{\mathrm{match}}\). No Jensen gain there either.

**P10.** The checker evaluates the closed \(J_{\mathrm{mf}}''\) at \(\sigma = 0\) and at 64 points \(\sigma = 10^{-4} \cdot (20/10^{-4})^{i/63}\) for \(i = 0,\ldots,63\), and a central finite difference of step \(10^{-6}\) at the same points. Relative error worse than \(10^{-8}\), or any nonpositive closed second derivative, refutes the display. Second differences of A2's mean-field \(J\) on \(\sigma = i/20\) for \(i = 1,\ldots,400\) are nonnegative up to an absolute tolerance \(10^{-9}\); a more negative value refutes convexity on \((0,\infty)\) and the location is reported. Convexity is not claimed for A2 on any set that includes \(\sigma = 0\), because the type law at 0 is the binomial draw and the type law on \((0,\infty)\) is the selected one (`PREREG.md` §1). The checker prints \(J_{\mathrm{mf}}(0)\), the limit of \(J_{\mathrm{mf}}\) at \(10^{-6}\), and the two heats, and does not call a jump an interior minimum.

Frozen Jensen checks, equal two-point spreads, no other pairs promoted to a score:

| object | spread | prediction |
|---|---|---|
| A0 \(J_{\mathrm{mf}}\) | \(\{1,2\}\) and \(\{0,2\}\) | average strictly above the cost at the mean |
| A0 \(Q_{\mathrm{flow}}\) | \(\{1,2\}\) and \(\{0,2\}\) | average strictly below the flow at the mean |
| A0 \(Q_{\mathrm{match}}\) | \(\{1,2\}\) | average strictly above the matched heat at the mean |
| A2 \(J_{\mathrm{mf}}\) | \(\{1,2\}\) | average strictly above the cost at the mean |
| A2 \(J_{\mathrm{mf}}\) | \(\{0,2\}\) | reported, sign not predicted (the point 0 sits on the other side of the type jump) |
| A2 \(Q_{\mathrm{flow}}\) | \(\{1,2\}\) | average strictly below the flow at the mean |

P7 remains the spread around \(\sigma^\star\) only. P10 is the shape on the half-line. If P1 holds and P10 holds, the interior minimum sits in a convex bowl: a positive level of stress can lower the cost, and variation around any point, including that minimum, raises the mean-field cost.

## D. Informative failure is not a fluctuation theorem

**Arm A13.** At each \(\sigma \in G\) for A2, let \(\bar\lambda(\sigma)\) be the stationary mean failure rate per unit. A4 fails every unit at rate \(\sigma'\). The matched point is \(\sigma' = \bar\lambda(\sigma)\), including values off \(G\). Compare continuous heat, \(Q_{\mathrm{flow}}\), mean-field loss, and \(J_{\mathrm{mf}}\).

**P11.** On A2 the exact stationary \(\mathbb{E}[k]\) is strictly greater than \(n\pi\). On A4, uninformative R-refresh, the stationary law is \(\mathrm{Binomial}(n,\pi)\), so \(\mathbb{E}[k] = n\pi\). At every matched pair, A2's continuous installed heat is therefore strictly higher than A4's. The sign of \(J_{\mathrm{mf}}^{\mathrm{A2}}(\sigma) - J_{\mathrm{mf}}^{\mathrm{A4}}(\bar\lambda(\sigma))\) is not predicted: extra quality raises heat and lowers loss, and the frozen \((n,c)\) is not asserted to lie where extra precision pays. The official Monte Carlo gap at the A2 grid argmin, if there is one, and at \(\sigma = 1\), is printed beside the mean-field gap. A sign read off after the run is a result, not a new prediction.

No identity in this script is a fluctuation theorem. The hazard \(\lambda(q)\) is an assumption of class AF. It is not derived from a dissipation-biased generator. The statement "nonequilibrium driving that rewards better-aligned units is why \(J\) has an interior minimum" has no computed consequence that is a theorem of that literature. As an account of class AF it is **METAPHOR**. The statement "some generator in that literature induces both this hazard and this heat floor" is **CONJECTURE**, and this check does not test it.

Hormesis, synaptic pruning, and apoptosis are names for P1 and for A9 only if a computed curve is identified with a measured dose or a measured cell. No such measurement is in this check. The names are **METAPHOR** here. They are **KNOWN** only as descriptions of the fetched sources, in the results note, and only after Crossref returns the DOI. Sources named for that fetch, not yet cited: Taleb and Douady 2013 on convexity (already the definition in `theory/ROBUSTNESS.md` §6); a hormesis review; a synaptic-pruning paper; Kerr, Wyllie, and Currie on apoptosis; Perunov, Marsland, and England, "Statistical physics of adaptation," *Physical Review X* (2016). A DOI that Crossref does not return is not cited. Nothing in those sources is a premise of P8–P11.

## E. What would refute the addendum

- P8 fails if \(H_J\) falls anywhere on the A0 closed form or on the A2 fine grid of P10.
- P9 fails if \(Q_{\mathrm{flow}}\) falls or \(Q_{\mathrm{match}}\) rises on those grids.
- P9b fails if the uncapped \(H^\star\) does not change monotonicity at \(4 kT a/(w v)\), up to the grid spacing \(1/200\).
- P10 fails if the closed second derivative is nonpositive anywhere on its grid, if the finite difference disagrees at the stated tolerance, or if an A2 second difference on \((0,\infty)\) is below \(-10^{-9}\).
- A Jensen row in the table with a predicted direction that comes out the other way refutes that row.
- P11's ordering \(\mathbb{E}[k] > n\pi\), or the heat ordering at matched rate, failing refutes P11's ordering. It does not create a fluctuation theorem.

A miss is a puzzle when it is not one of these refutations. The objective remains a cost. This addendum does not edit `PREREG.md`, `THEORY.md`, `CORE.md`, or `README.md`.
