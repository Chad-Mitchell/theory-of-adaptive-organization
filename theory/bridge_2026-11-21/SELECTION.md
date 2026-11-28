# Selection as a thermal search: the stationary law and the spread

*21 November 2026 (America/New_York). Package `theory/bridge_2026-11-21/`. This is the part of the package that is actually new. It does not change the hypothesis sentence, or the locked qualification rule of THEORY §3 / FRAMEWORK §9. Evening of the same day, branch `selection-fold-2026-11-21`: the general factor \(\beta=\alpha(N_e-1)\) is withdrawn. The exponents are now stated per population model, consistent with `theory/SELECTION_AXIOMS.md`. The official T27 Moran run, \(N=201\) and \(\beta=\alpha(N-1)\), is unchanged. No locked prereg or hash file is edited.*

## Already in the repository (not new)

THEORY §3 and FRAMEWORK §9 already define “strongly selected” operationally: a cost-to-fitness map \(\sigma\) (fractional change in growth, survival or reproduction rate per fractional change in \(J\)), a population proxy \(N_e\), and a band \(\varepsilon=10/(\sigma N_e)\) that is at least as wide as ten times the drift barrier \(s N_e\approx 1\) (Lynch et al. 2016, doi 10.1038/nrg.2016.104; the factor of 10 is a conservative choice made there, not Lynch’s). A class qualifies only if that band, plus measurement error, excludes a named rival, and if at least ten redesign times have been spent in one world. EVO1 already tested whether in-silico evolution *reaches* \(\arg\min J\) where small steps lead there.

What was missing was a stationary *distribution* over designs, and a predicted typical *distance* from the minimum, not only a band that can exclude a rival.

## Assumption (fitness map)

Malthusian fitness is taken to be linear in the cost, \(m(\mathcal D)=-\alpha J(\mathcal D)\), with Wrightian birth rates \(r=\exp(m)\). This is an assumption, not a theorem. Real maps can be nonlinear or frequency-dependent; the results below are for this map.

Under that map, \(\sigma=\lvert\mathrm{d}\log r/\mathrm{d}\log J\rvert=\alpha J\) at an operating point \(J\), so \(\alpha=\sigma/J^\star\) at the minimum.

## Theorem (standard population genetics, applied to \(J\))

In the weak-mutation regime \(N\mu\ll 1\) the population is typically monomorphic, and substitution is an origination–fixation chain on the design graph (Sella & Hirsh 2005, doi 10.1073/pnas.0501865102; they also write a free-fitness Lyapunov function \(G=\langle\ln f\rangle+(1/v)S\), following Iwasa 1988, doi 10.1016/s0022-5193(88)80243-1).

For a haploid Moran process of size \(N\), with *equal mutation clocks on each undirected edge* (so that there is no degree bias), detailed balance gives

$$\frac{\pi_i}{\pi_j}=\left(\frac{r_i}{r_j}\right)^{N-1}.$$

Substituting \(r=\exp(-\alpha J)\) yields the Boltzmann law

$$\pi(\mathcal D)\;\propto\;\exp\bigl(-\beta J(\mathcal D)\bigr),\qquad \beta=\alpha(N-1).$$

For diploid Wright–Fisher with multiplicative fitness within a locus, Sella and Hirsh's approximation gives \(\beta=\alpha(2N-1)\) (their weight \(f^{2N-1}\)). Haploid Wright–Fisher in the same table is \(2(N-1)\), which this note does not use. The official T27 simulation uses the haploid Moran case with \(N=201\) and \(\beta=\alpha(N-1)\). That Moran factor, and the official run results, were not changed.

This is not a new mathematical theorem. What is new is the application to the reduced cost \(J\) and the consequences below.

**Infinite-population limit (known geometry).** Fisher’s fundamental theorem and the Shahshahani metric (Shahshahani 1979, doi 10.1090/memo/0211) say that, at infinite \(N\), selection is gradient ascent of mean fitness — equivalently gradient descent of mean \(J\) — in that metric. That is the \(\beta\to\infty\) limit of the same picture. Finite \(N\) replaces the point mass at the minimum by the Boltzmann spread. The geometry is credited; it is not used as a derivation of \(\pi\).

## Consequences (the new quantitative content)

1. **“Strongly selected” is low temperature.** Large \(\beta\) (large \(N_e\alpha\)) concentrates \(\pi\) at \(\arg\min J\). This is the same idea as THEORY §3, now as a distribution rather than only as a qualification check.
2. **Equipartition near a quadratic minimum.** If \(J(\theta)=J^\star+\tfrac12(\theta-\theta^\star)^\top H(\theta-\theta^\star)\) in \(d\) continuous design coordinates, and \(\pi\propto e^{-\beta J}\), then

   $$\mathbb{E}[J]-J^\star \;=\; \frac{d}{2\beta}.$$

   Distance from the minimum scales as \(1/\)selection strength. “Real systems lag” is then a predicted, measurable spread, not by itself a refutation, provided the lag is of this order and the fitness map is as assumed.
3. **Consistency with the existing qualification band.** The absolute excess is the equipartition quantity \(\mathbb{E}[J]-J^\star=d/(2\beta)\). The fractional excess is a separate statement. Under the linear map, \(\beta=\alpha\nu\) with \(\nu\) the Sella–Hirsh exponent of the process just named (haploid Moran \(N-1\); diploid Wright–Fisher \(2N-1\), an approximation). The \(N_e\) in THEORY §3's drift barrier is this \(\nu\) (\(s N_e\approx 1\) matches their scale \(\nu s\approx 1\)), so \(\beta=\alpha N_e=\sigma N_e/J^\star\) at leading order when \(J^\star>0\) and \(\sigma\) is evaluated at \(J^\star\). Then the typical *fractional* excess is

   $$\frac{\mathbb{E}[J]-J^\star}{J^\star}\;\approx\;\frac{d}{2\sigma N_e}.$$

   The form \(\alpha(N_e-1)\) is the haploid Moran exponent when \(N_e\) is census size. It is not the diploid exponent. The FRAMEWORK §9 band is \(\varepsilon=10/(\sigma N_e)\), a *fractional* difference in \(J\) used to exclude a named rival (a one-dimensional comparison). The ratio of the typical fractional excess to that band is \(d/20\). For a few soft design coordinates the expected scatter sits well inside the conservative band; for large \(d\) it need not. These uses are different, and this package does **not** change the locked factor of 10. A later refinement, if one is wanted, would be to size a “contains most of the stationary mass” band by a chi-squared quantile, which scales as \(d/(\sigma N_e)\). That is a note, not a patch.

The official T27 test (preregistered in `PREREG.md` before any official run) checks (1) and (2) in Model S, plus the low-\(\beta\) statement that the mass spreads and the mean stays above \(J^\star\). Official numbers are in `RESULTS.md`.

## Two temperatures, not one

See `BRIDGE.md` for the distinction between this selection temperature \(1/\beta\) and the existing ruin-constraint “temperature” \(z=B/(\sigma\tau^H)\) of THEORY (iv), CT18/CT25. They are different quantities. The \(\sigma\) in \(z\) is the **CT18 shock scale**, not the cost-to-fitness map \(\sigma\) of THEORY §3 / FRAMEWORK §9 used in the band and the consistency note above. No identification in kelvin is claimed for either, beyond the Landauer floor on the *prices* in \(J\).

## What is not shown

- The ruin cap \(P(\mathrm{ruin})\le\varepsilon\) is not built into \(\pi\propto e^{-\beta J}\). Feasibility is a hard constraint on the design set; a large-deviation rate function for lifetime ruin is listed as missing math, not as a derived identification with \(\beta\).
- Strong mutation, standing polymorphism, frequency dependence, and a nonlinear map \(m(J)\) are outside the theorem as stated.
- EVO1’s reachability failures (fitness valleys, W4/W4b; W4's creation valley met the D2b bar (4/4); W4b's D1b bar was not met (2/4)) are compatible: the Boltzmann law assumes the mutation graph can traverse the space. A disconnected, or valley-blocked, graph is a different process.
