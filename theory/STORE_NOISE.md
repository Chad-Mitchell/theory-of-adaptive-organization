# STORE_NOISE: an extension of Model S for noise a store makes itself (E1) and upkeep priced by speed (E2)

Friday 20 November 2026, Grok Bot executor for Chad Mitchell, branch `v2.5-measure`. Self-checked, **not independently
reviewed**. Checks: `theory/store_noise/checks.py` (all pass; output in `checks.json`).

**Why this exists.** This is an extension found because a measured test failed (`theory/measured/ecoli/`, CLAIM_MAP P1).
It is **not a patch**: P1's preregistered verdict stays **PROXY-FAIL on that setup**, and nothing below changes any locked
prediction. The extension states, as theory, the term the failure pointed to, says what it changes in the Master Theorem,
and makes fresh predictions (preregistered in `theory/measured/PREREG_SN1.md` before any new system's data are read).

## 1. The gap
Model S (`theory/LAYERS.md` §1) and the Master Theorem's class 𝓜_LG (THEORY.md B.9) take all noise as exogenous: the
world is sensed through white noise of fixed density N, and a layer costs a fixed upkeep h whatever its speed. A real
store is a physical object. Its state is held by molecules, people or records that turn over, so (E1) the store adds noise
of its own whose size can depend on how long it remembers, and (E2) keeping a fast store can cost more than a slow one
(Lan et al. 2012, doi 10.1038/nphys2276: adaptation dissipation grows with adaptation speed). In E. coli the binding noise
is the store's own (τn ≈ τ2; Berg–Purcell counting noise is 10⁻⁶–2×10⁻⁴ of it), so the gap was decisive there.

## 2. Model S+ (one mode)
World: one OU mode u, rate λ, variance σ². A store with memory τ holds z = LP_τ u + ξ, LP_τ = 1/(1+sτ). The store's own
noise, referred to its input, has variance V(τ) = V0 (τ0/τ)^{2−2s} and the store's correlation time; equivalently the
noise on the store's output (activity) has variance ∝ τ^{2s}. **s is a measured property of the store:**
s = 1/2 is fixed noise density into the store (variance grows with memory), s = 0 is fixed stationary variance (a
copy-number limit). Read-out: the best static linear read of the store(s). Cost: J = Σ h(τ_k) + w·E, E the mean squared
error on u, with h(τ) = h0 + h1/τ (E2; h1 = 0 recovers Model S's fixed upkeep).

## 3. Results (in-model)
**E1-a (memory set by the noise exponent).** With one store, explained variance EV(τ) = (σ²A)²/(σ²A + V(τ)),
A = 1/(1+λτ). At low SNR (V ≫ σ²A, E. coli's case) EV ∝ τ^{2−2s}/(1+λτ)², so

  **λτ\* = (1 − s)/s.**

The store is slower than its mode iff s < 1/2, matches it at s = 1/2, and is faster iff s > 1/2. Higher SNR shortens the
memory (checks §1, §1b: closed form within 1% of the full optimum at seven values of s).

**E1-b (equivalence at s = 1/2).** For one store, store noise of fixed density N on the store's state has, referred to the
input, the spectrum N/(1 + ω²τ²): exactly that of sensing noise of density N on the input (checks §2). So self-generated
noise of fixed density changes nothing in Model S's one-store results; the store's own noise matters only through
s ≠ 1/2 and through copies (E1-c).

**E1-c (copies, not new time constants).** Independent store noise makes redundancy pay: two stores for one mode nearly
double EV at low SNR (×1.96–1.98 at s = 0.1, 0.31, 0.5 at E. coli's numbers), and the best pair is **two copies at one time
constant**, not two time scales (checks §3; numerical, three values of s, one gradient, three optimizer starts). Shared
sensing noise gives copies nothing; independent store noise does. So with store noise the number of *distinct time
constants* still follows the world (numerically, here), but the *size* of a layer (its copy number) becomes a priced design
variable that rises with stakes, like a read rate.

**E2 (speed-priced upkeep lengthens memory).** At low SNR, with x = λτ and a = 2 − 2s,
J(x) = const − W·x^a/(1+x)² + H/x, W = wσ⁴/(V0 (λτ0)^a), H = h1·λ. The interior optimum solves

  **H/W = x^{a+1} [2x − a(1+x)] / (1+x)³,**

so any h1 > 0 puts the memory beyond E1-a's value (x\* > (1−s)/s). For s < 1/2 any price gives a finite memory; for
s = 1/2 the right side tends to 1, and at H/W ≥ 1 the best design is not to track (K\* = 0) (checks §4).

**What E. coli implies (post hoc, not a test).** With the measured s = 0.31 [0.24, 0.37] (F2, `theory/measured/ecoli/f2/`),
E1-a gives 1.9–3.6 s against the measured 9.9 s: the store's own noise closes about 37% of the log gap between Model S's
1.1 s and 9.9 s. Explaining the rest by E2 alone needs H/W ≈ 0.67–0.74 (speed price comparable to the whole value of
tracking at that gradient). E1-a alone would need s ≈ 0.10. Neither number is measured; both are stated so they can be.

## 4. What changes in the Master Theorem (proposed; THEORY.md is not edited by this note)
- **Scope.** 𝓜_LG's premises "exogenous noise" and "fixed upkeep per layer" are now named as premises, not defaults.
- **(iii) interlacing.** "At the full optimum every layer is faster than its mode" holds in 𝓜_LG. In Model S+ it holds
  for a one-store layer iff s ≥ 1/2 at h1 = 0 (E1-a); with s < 1/2 or h1 > 0 the optimal store is **slower** than its mode.
  Interlacing is a property of exogenous noise and speed-free upkeep, not of layering. (E. coli: λτ2 = 8.5.)
- **(iii) count.** "One real mode ⇒ K\* ∈ {0, 1}" must read "one distinct time constant": with independent store noise,
  copies of the one layer pay at high enough stakes (E1-c). That the distinct-time-constant count stays capped by the
  world's degree under store noise is **checked numerically for one mode only, not proved**; for many modes it is open.
- **(ii) comparative statics.** Unchanged in form (CT33 needs no model class): judgment spend, now including copies and
  speed, never falls as w/h rises with ruin slack. New corollary of E2: at fixed w, a higher speed price (h1) never
  shortens the memory, and a higher w never lengthens it (E2's right side rises in x for s < 1/2).
- **(iv), (v).** Unchanged; the read-rate rule (CT12) is untouched because reads, not stores, are priced there.

## 5. What would refute the extension (fixed now)
For any new system with s, λ and τ measured on the same store, E1+E2 predict λτ ≥ (1−s)/s at low SNR when h1 ≥ 0. A
memory clearly faster than that (below a third of it, CI wholly below) refutes E1+E2 for that system. The full rule,
rivals and candidate systems are locked in `theory/measured/PREREG_SN1.md`.

## 6. Prior art (search done 20 Nov 2026; all DOIs resolved on Crossref, `measured/crossref_priorart.out`)
**No novelty is claimed for E1 or E2.** The core idea is established: an optimal integration (memory) time arises from a
trade-off between a dynamical error that grows with memory and a noise error that shrinks with it, and where that
optimum sits depends on how the noise scales with the integration time, i.e. on which resource limits.
- Optimal filtering of the E. coli response: Andrews, Yi & Iglesias 2006 (doi 10.1371/journal.pcbi.0020154); Wiener–
  Kolmogorov filtering by signalling networks: Hinczewski & Thirumalai 2014 (doi 10.1103/PhysRevX.4.041017); prediction
  and E. coli's integration time as a response-speed/noise trade-off: Becker, Mugler & ten Wolde 2015 (doi
  10.1103/PhysRevLett.115.258103); trajectory information: Tostevin & ten Wolde 2009 (doi 10.1103/PhysRevLett.102.218101).
- **Closest prior art for E1:** Malaguti & ten Wolde 2021 (doi 10.7554/eLife.62574) derive the optimal integration time
  for time-varying signals in a push–pull network and show that it depends on which resource is limiting. It tends to
  zero when readout copy number limits, equals the signal time when power limits, and is set by sampling vs dynamical
  error when receptors limit. Govern & ten Wolde 2014 (doi 10.1073/pnas.1411524111; doi 10.1103/PhysRevLett.113.258102)
  give the resource classes. E1's exponent s is a one-parameter summary of the same dependence. Their results concern the
  fast receptor-integration time (tens to hundreds of ms), not the methylation memory tested here.
- Adaptation's own noise growing with the adaptation time (σ² ∝ τ_m, the s = ½ case): Sartori & Tu 2011 (doi
  10.1007/s10955-011-0169-z). The fluctuation–response coupling measured in E. coli: Park et al. 2010
  (doi 10.1038/nature09551); single-cell kinase noise from adaptation enzymes: Keegstra et al. 2017 (doi 10.7554/eLife.27455).
- E2: the energy–speed–accuracy relation is Lan et al. 2012 (doi 10.1038/nphys2276). Limits on suppressing intrinsic
  noise and their cost: Lestas, Vinnicombe & Paulsson 2010 (doi 10.1038/nature09333). Noise can enhance drift (a nonlinear
  effect outside Model S+): Flores et al. 2012 (doi 10.1103/PhysRevLett.109.148101).
- Stochastic resonance (noise-aided detection in threshold systems) was checked and is a different effect; it does
  not give an optimal memory. Bialek's *Biophysics: Searching for Principles* (Princeton UP, 2012) treats the
  Berg–Purcell and filtering trade-offs in general; I did not find the power-law form there (book not read in full).
- The closed form λτ\* = (1−s)/s was not found stated in this form in the sources checked. It is an elementary consequence
  of minimizing a power-law noise term against a first-order lag, so it is credited to that literature as an instance
  rather than claimed. What this repo adds is only the mapping into the theory's cost J and the Master Theorem's scope.
