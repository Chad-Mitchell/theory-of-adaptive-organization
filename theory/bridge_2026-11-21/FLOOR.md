# Thermodynamic floor: what is already proved, and one explicit corollary

*21 November 2026 (America/New_York). Package `theory/bridge_2026-11-21/`. This note does not change `CORE.md` or the hypothesis sentence. It does not re-derive results already in the repository.*

## Already in the repository (not new)

- **Floors on the prices** (THEORY, the “one currency” paragraph; CORE.md line 16): at least \(kT\) per nat acquired or erased by a measuring tracker (Landauer 1961, doi 10.1147/rd.53.0183), and \(kT\cdot(I_{\mathrm{mem}}-I_{\mathrm{pred}})\) for memory that does not predict (Still, Sivak, Bell & Crooks 2012, doi 10.1103/PhysRevLett.109.120604). Still et al. formalize this for isothermal Markov systems with a single bath and no back-action on the drive; elsewhere it is an analogy (SCALE_ENDS E3 / SE3, with the [BK] scope note). In their setting the dissipated work at a signal change satisfies \(\beta\langle W_{\mathrm{diss}}[x_t\to x_{t+1}]\rangle = I_{\mathrm{mem}}(t)-I_{\mathrm{pred}}(t)\) (nats; \(\beta=1/kT\)). The repository’s looser “at least” form is the one used in theorems.
- **The bound is often loose.** Real systems typically dissipate far above the Landauer floor. FRAMEWORK §3.11 defines the binding ratio \(\beta_{\mathrm{phys}}\) (actual cost of a read or held bit divided by its thermodynamic floor). Near 1, physics constrains the design; \(\gg 1\), the floor is non-binding and the niche sets the prices. Firms are expected \(\gg 1\); the cell value is computed but INCONCLUSIVE. No theorem in the linear-Gaussian class currently uses a physical floor as a design constraint (FRAMEWORK §3.11; SCALE_ENDS §8).
- **First bit must pay** (CT4, PROVED in-model): with the predictive information-bottleneck curve \(\mathrm{IB}(I)=\sup\{I(M;X_{t+k}):I(M;\mathrm{past})\le I\}\), a model is carried iff \(\kappa < -(\mathrm{D}\circ\mathrm{IB})'(0^+)\). The Lagrangian is prior art (Sims 2003; Tishby & Polani 2011); deriving the information bottleneck from the dissipation bound is known (Still 2020, doi 10.1103/PhysRevLett.124.050601). Predictive information itself is Bialek, Nemenman & Tishby 2001, doi 10.1162/089976601753195969, already cited in the THEORY §9 conjecture on causal states (Crutchfield & Young 1989).
- **Scale ends** (`theory/SCALE_ENDS.md`): atoms sit at the frozen corner because blind persistence is viable (E2) and there is no selection over actions (E1, partly definitional). A model would still cost at least \(kT\ln 2\) per bit erased per refresh, and its selected benefit is zero. Switch-on of *selected* models needs heredity, a world-dependent action, drift inside the hold band, and a first nat that pays (S1–S4). With Kelly-type fitness the Landauer part of S4 is \(E_{\mathrm{gen}}>\beta_{\mathrm{phys}}\cdot kT\) (SE7); for a bacterium \(E_{\mathrm{gen}}\approx 10^{11}\)–\(10^{12}\,kT\), so the floor does not bind existence. The binding conditions are heredity and drift, not the floor.

## Corollary, not a new theorem (explicit stakes / \(kT\) ratio)

CT4 plus the Landauer floor on \(\kappa\) already imply a dimensionless control. Write \(\nu\) for the update (erasure) rate and measure memory in nats, so

**Assumption:** a measuring tracker’s memory price is at least the floor, \(\kappa \ge \kappa_{\mathrm{floor}} = kT\cdot\nu\). (If memory is counted in bits, the same floor is \(kT\ln 2\cdot\nu\).) This is the “\(\kappa\) has a physical floor \(\sim kT\ln 2\) times the update rate” statement; it is Landauer plus an accounting convention, not a new bound.

**Corollary (CT4 + floor).** Let \(\Delta\ell_1\) be the drop in expected loss bought by the first nat, and let the stakes per update be \(w\Delta\ell_1\). The first nat pays only if \(w\Delta\ell_1 > \kappa/\nu \ge kT\), i.e. only if the stakes-to-thermal ratio

$$\rho \;=\; \frac{w\,\Delta\ell_1}{\nu\,kT}$$

is strictly greater than 1 (nats). When \(\rho\le 1\), \(K^\star=0\): no model pays. This is CT4’s threshold \(\kappa < -(\mathrm{D}\circ\mathrm{IB})'(0^+)\) with \(\kappa\) replaced by its physical floor. It is the same content as SCALE_ENDS S4 / SE7, written as a single ratio.

**Scale-end reading.** Where the typical stake of an update is itself of order \(kT\) (thermal energy is the scale of the exchange), \(\rho=O(1)\) and the floor says \(K^\star=0\). That is a sufficient condition, and it applies even if one imagines a selected use. For actual atoms the repository’s load-bearing argument is stronger and different: E2 + E1 make the *benefit* of the first bit zero, not merely comparable to \(kT\). The ratio is useful as a scale-end *statement*, not as a new reason atoms have no model.

**Where the bound is loose, the ratio does no design work.** Once \(\beta_{\mathrm{phys}}\gg 1\), the relevant threshold is the niche price, not \(kT\), and \(\rho\) computed with the floor is a large number that does not decide \(K^\star\). The floor then matters only as this scale end, exactly as FRAMEWORK §3.11 and SCALE_ENDS §8 already say.

**Theorem / assumption / loose, in one list.**

| Claim | Status |
|---|---|
| Erasure costs \(\ge kT\ln 2\) per bit (Landauer) | Known theorem of stochastic thermodynamics, under its stated conditions; experimentally supported (Bérut et al. 2012 is already cited in SCALE_ENDS) |
| Dissipation \(\ge kT\times\) nonpredictive information (Still et al. 2012) | Known, in their isothermal, no-feedback, Markov setting; an analogy outside it (SCALE_ENDS) |
| \(\kappa_{\mathrm{floor}}=kT\cdot\nu\) (nats) | Accounting convention on Landauer, assumption that updates are erasure-type |
| First nat pays iff \(\kappa < -(\mathrm{D}\circ\mathrm{IB})'(0^+)\) | CT4, proved in-model |
| \(\rho\le 1\Rightarrow K^\star=0\) | Corollary of CT4 + the floor assumption |
| Real systems sit at the floor | Not claimed; typically false (\(\beta_{\mathrm{phys}}\gg 1\)) |
