# Layer lifetime as a stack rule: spacing, a layer floor, and local vs shared

*Saturday 21 November 2026, written about 2:30 PM ET (America/New_York), stacked on PR #139 (`theory/FLUID_LAYERS_2026-11-21.md`) beside `shannon-core-2026-11-21`. Checks: `theory/layerlife_checks/layerlife_checks.py` (output `layerlife_checks.out`; run by `tools/test_layerlife_checks.py`). Labels: **PROVED** (a proof is given here or cited, inside the stated model), **KNOWN** (published, credited), **NUMERICAL** (computed, not proved), **ANALOGY**, **OPEN**, **FALSE** (a stated claim that does not hold). Proved in-model says nothing by itself about nature. Not a lock. Not yet independently reviewed when first written. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."*

## 0. Bottom line, in plain words

The shared-layer lifetime in the fluid-layers note,

$$\tau_{\text{layer}}=T^*=\sqrt{6k/(w\sigma^2)},$$

is the right refresh rule for a lumpy layer, and it belongs with the core, not as a footnote. Applied recursively, it does two things cleanly and fails to do a third.

1. **Spacing (PROVED, in a specialized stack).** If each layer can reset only its own component of a drifting world, and the loss is quadratic in the total error, the layers' lifetimes stand in the exact ratio
   \(T_i^*/T_j^*=\sqrt{(k_i/k_j)\,(\sigma_j^2/\sigma_i^2)}\)
   (equal stakes). That is a spacing rule. It is not a universal geometric series: the ratios are set by the costs and the drifts, and they collapse or invert when those inputs do.
2. **Local vs shared (PROVED for a Brownian common driver with latency; NUMERICAL for OU).** The same cost, with a delay \(\ell>0\) on a shared update, gives DIR1's D5 sign: fast drift is handled locally, slow drift is shared. There is an explicit crossing \(\sigma^{2*}\). Without latency there is no switch. "Slower than the latency" is not enough; at the prices in the checks, shared still lost at \(\tau=40\ell\) and won at \(\tau=400\ell\).
3. **A computable floor on the number of layers (mostly FALSE as hoped).** The lifetime rule does not close the gap left in PR #139 — "the fewest layers that reach accuracy \(D\) in this world." One lumpy tracker, refreshing at \(T^*\), is already optimal for a single process, including a fractal (power-law) one. A stack appears only when layers are *specialized* (a layer cannot reset the whole state). Under that restriction there is a simple count lower bound, but it comes from the components' variances, not from \(T^*\). In Model S the fewest-stores floor remains the existing numerical \(E_K\); \(T^*\) is a different object (a reset interval, not a store time constant), and the two spacing ratios do not match.

So the formula is core as a *timing* rule for lumpy layers, and as the cost that also decides local vs shared. It is not a substitute for a layer-count limit.

## 1. Could it fail? (checked before each piece)

- **Spacing from a recursive \(T^*\).** It could fail if layers are not specialized, if one action can reset several components cheaply, if the target is mean-reverting on the scale of \(T^*\), or if adjustment is smooth rather than lumpy. Those failures are demonstrated below. It could also have been only a restatement of Roundy's integer-ratio lot schedules. The formula here is a ratio of optimal lifetimes, not a claim that integer-ratio *clocks* are within a stated percent of a joint schedule.
- **A layer-count floor from the same rule.** It could fail, and in the unrestricted design class it does: one joint reset of the sum beats a stack when that reset is not much dearer than a single part. A fractal spectrum does not, by itself, force many layers. This was the main hope, and it should be scored as not met.
- **D5 from the same inequality.** It could fail if shared updates have no latency (then amortization alone makes shared cheaper at every drift, or never, with no switch). It could fail in the field: threat-rigidity and copy-when-uncertain predict the opposite sign, and a published firm study already reports *less* business-unit recombination during industry turbulence (Karim, Carroll & Long 2016). The derivation is not a field result.
- **Prior art.** The square-root lifetime is Dixit's; the menu-cost read-rate cousin is Barro's and is already in `theory/measured/TESTBEDS.md`. Claiming the exponent \(\tfrac12\) as new would be false. The assembly — layer lifetime as the design variable, the specialization caveat, and D5's crossing from the same cost — is what can be new, and only that.

## 2. The single-layer rule (KNOWN)

CL19 (a), after Dixit (1991, *Review of Economic Studies* and *JEDC*; Chalkley 1997 notes that the quadratic-loss approximation is exact at zero discounting, which is the case used here): a gap that drifts as Brownian motion with variance rate \(\sigma^2\), costs \(w\,x^2\) per unit time, and is reset to zero at lump cost \(k\), is left alone until \(|x|\) hits \(b^*=(6k\sigma^2/w)^{1/4}\). The expected time between resets is \(b^{*2}/\sigma^2\), which is \(T^*=\sqrt{6k/(w\sigma^2)}\). The excess cost rate is \(2\sqrt{kw\sigma^2/6}\). This is the formula in `theory/FLUID_LAYERS_2026-11-21.md` and is re-checked in `layerlife_checks.py` §1 (grid minimizer, scaling, identities).

The same scaling with a different coefficient holds for a *fixed-period* refresh (the EOQ / Regime A cousin already in THEORY: \(T_{\text{fix}}^*=\sqrt{2k/(w\sigma^2)}\), cost \(\sqrt{2kw\sigma^2}\)). The barrier lifetime is \(\sqrt{3}\) times the fixed-period lifetime and is cheaper, because it does not reset when the gap is still small. Nothing in the rest of this note depends on using 6 rather than 2; the exponent \(\tfrac12\) in \(k\) and in \(1/\sigma^2\) is the same.

CL19 (c): if adjustment is smooth (convex cost, no lump), there is no discrete lifetime, only a decay time \(T_{\text{red}}=\sqrt{\kappa/w}\). A recursive "lifetime stack" is then **FALSE**.

## 3. A specialized stack (Model LS)

**Premises.** The world is \(\theta=\sum_i\theta_i\) with independent components. Layer \(i\) can observe and reset only component \(i\), at lump cost \(k_i\). The loss is \(w(\theta-\hat\theta)^2\), so the mean-square error adds across independent components. Ruin is slack. This is the design class in which a stack can be the answer rather than a mistake.

**Could it fail?** If any of those premises is dropped, the conclusions below need not hold. Section 4 lists the failures.

### 3a. Spacing (PROVED in Model LS)

Each layer is its own CL19 problem. For Brownian components,

$$T_i^*=\sqrt{6k_i/(w\sigma_i^2)},\qquad
\frac{T_i^*}{T_j^*}=\sqrt{\frac{k_i}{k_j}\cdot\frac{\sigma_j^2}{\sigma_i^2}}.$$

The total cost is the sum of the layer costs, \(J^*=\sum_i 2\sqrt{k_i w\sigma_i^2/6}\). A brute-force grid over each barrier recovers the same \(J^*\) (checks §2). Equal costs and geometrically spaced drifts give geometrically spaced lifetimes, with ratio \(\sqrt{\lambda}\) if the variance rates themselves sit in ratio \(\lambda\). That is a corollary, not a separate law of spacing.

### 3b. When the Brownian \(T^*\) is only approximate (NUMERICAL)

If component \(i\) is Ornstein–Uhlenbeck with rate \(a_i\) and stationary variance \(v_i\), the short-time variance rate is \(\sigma_i^2=2a_i v_i\), and the Brownian formulae apply when \(T^*\ll\tau_i=1/a_i\). In the checks, a case with \(T_{\text{bm}}/\tau\approx0.0045\) had the exact fixed-period optimum within 0.3% of \(T_{\text{bm}}\). A case with \(T_{\text{bm}}/\tau\approx0.63\) missed by 137%. In that regime the mean-square error has begun to saturate at \(v_i\), and a lumpy layer may barely beat (or lose to) staying blind at cost \(w v_i\). **The formula is false as a quantitative rule once \(T^*\) is not short compared with the component's correlation time.**

### 3c. A lower bound on the number of layers

**Hope.** That \(T^*\) applied along a drift spectrum \(\sigma^2(\tau)\) would give a closed form for the fewest layers that reach accuracy \(D\), and so close the layer-term gap of `theory/SHANNON_2026-11-21.md`.

**What is actually proved, and only in Model LS.** For OU components, an untracked component contributes its full stationary variance \(v_i\). To have total MSE \(\le D\), every component with \(v_i>D\) must be tracked, so

$$K\ge\#\{i:v_i>D\}.$$

That bound is computable from the world's component variances and the target \(D\). It does not use \(T^*\), and it does not use the prices. It is a covering bound on a specialized partition, not a layer-term converse in Shannon's sense.

**What is FALSE.** Without the specialization premise, the bound is false, and so is any claim that a power-law or fractal spectrum forces many lumpy layers. If one action can take a perfect (or cheap) observation of the *sum* and reset a single estimate, the residual starts at zero and a short enough hold meets any \(D>0\) with \(K=1\). Two full-reset layers on one Brownian motion cannot beat the cheaper layer alone (checks §5). For a single fractal process with increment variance \(\propto\tau^{2H}\), the fixed-period balance \(k/T+w C T^{2H}\) gives one refresh time \(T^*\propto(k/(wC))^{1/(2H+1)}\) (and \(H=\tfrac12\) recovers the square-root rule). That is still one layer.

**Model S is a different design class.** There the layers are continuous leaky stores behind white sensing noise, priced by upkeep \(hK\), and the fewest stores that reach a given error is the existing numerical \(E_K\) (`theory/layers_checks/stores.py`). On a two-mode world the optimal store rates interlaced the world rates, as THEORY already states (L2). The Dixit lifetime ratio of the two modes, at equal \(k,w\), was 10; the ratio of the optimal store time constants was about 47. They are not the same spacing rule, and \(T^*\) does not compute \(E_K\). The layer-term floor of PR #139 stays **OPEN**.

## 4. Where a recursive stack is the wrong design

- **Joint reset cheaper than the parts (PROVED).** If a single action can reset the sum at cost \(\min(k_1,k_2)\) (or any cost not much larger than one part), one layer beats two. If instead a joint reset costs the *sum* \(k_1+k_2\), specialization is never more expensive: \(\sqrt{(k_1+k_2)(\sigma_1^2+\sigma_2^2)}\ge\sqrt{k_1\sigma_1^2}+\sqrt{k_2\sigma_2^2}\), with equality iff \(k_i/\sigma_i^2\) are equal (checks §3). So whether a stack pays depends on how the lump costs add when scopes merge. That has to be measured, not assumed.
- **Smooth adjustment.** No discrete \(T^*\) (CL19 (c)).
- **OU on a long lifetime.** The Brownian \(T^*\) mis-times the refresh (checks §4).
- **Already in the repository.** Geometric store spacing was withdrawn as unconditional (LAYERS1 P2, SIM-FAIL). A holographic count (layers growing with the log of the scale range, at roughly equal value each) failed in-model (`core/KEYSTONE_NOTE.md`). Those were Model S tests, not Model LS, but they are a warning against treating "fractal time \(\Rightarrow\) a stack with geometric lifetimes" as a theorem.

A stack of lumpy lifetimes is the right object when re-forming is lumpy *and* a layer cannot (or cannot afford to) rewrite the whole state: a team tweak versus an org-chart rewrite, a local estimate versus a shared grouping, a shallow edit versus a deep redesign. That is a scope restriction, close in spirit to Simon's near-decomposability, not a consequence of \(T^*\) alone.

## 5. Local vs shared (D5) from the same cost

DIR1's D5: fast-changing information is handled locally, slow-changing information is shared. It was the only directional prediction with opposite-sign rivals, and it went unscored (n = 2). The existing in-model source is CT35, via \(X_S=\nu\cdot\pi\cdot e^{-2\ell/\tau}X_L\) at equal read quality (THEORY B.11): latency kills a shared layer as \(\tau\to 0\).

**Question.** Does the same sign fall out of the lifetime cost?

**Brownian common driver, fixed-period refreshes, latency \(\ell\) on the shared observation (PROVED).** \(N\) units, common variance rate \(\sigma^2\), local lump \(k_L\), shared lump \(k_S\), stake \(w\) per unit. Local total cost \(N\sqrt{2k_L w\sigma^2}\). Shared cost \(\sqrt{2k_S(Nw)\sigma^2}+Nw\sigma^2\ell\) (the second term is the delay floor). Shared can win at \(\ell=0\) iff \(k_S<N k_L\). With \(\ell>0\) there is a single crossing

$$\sigma^{2*}=\Biggl(\frac{\sqrt{2k_L w}-\sqrt{2k_S w/N}}{w\ell}\Biggr)^2,$$

provided the numerator is positive. Below \(\sigma^{2*}\), shared is cheaper; above it, local is cheaper. The checks recover the crossing to machine precision and confirm: no switch when \(\ell=0\).

**OU companion (NUMERICAL).** The same prices and \(\ell=0.5\): local won at \(\tau=0.05\) (shared's best option was to stay blind); shared still *lost* at \(\tau=20=40\ell\); shared won at \(\tau=200=400\ell\). The sign agrees with CT35. The naive rule "share once \(\tau>\ell\)" is **FALSE**.

**Rivals.** Threat-rigidity (Staw, Sandelands & Dutton 1981) predicts constriction of control, i.e. more central, under threat or turbulence. Copy-when-uncertain predicts more social / shared use as uncertainty rises. Both have the opposite sign in \(\sigma^2\) (or in \(1/\tau\)). A no-response rival predicts no switch.

This does not replace CT35. It is the lumpy, delayed-observation companion, and it makes the lifetime rule and D5 the same cost.

## 6. Prior art: what is known, and what is new

| Piece | Status | Credit |
|---|---|---|
| Inaction band, \(b^*\propto k^{1/4}\), lifetime \(T^*\propto\sqrt{k/\sigma^2}\) | **KNOWN** | Dixit 1991 (RES and JEDC); Chalkley 1997 (undiscounted exactness); CL19 in `theory/DYNAMICS.md` |
| Square-root refresh / menu-cost frequency | **KNOWN** | Barro 1972; Regime A / CT12 in THEORY; already marked prior art in `theory/measured/TESTBEDS.md` (central-bank meetings) |
| Aggregation of lumpy units | **KNOWN** | Caballero & Engel 1999; CL19 (d) |
| Integer-ratio / multi-level replenishment schedules | **KNOWN** | Roundy 1985 (98%-effective integer-ratio lot-sizing, *Management Science* 31:1416). A *schedule* constraint (nested integer ratios) is a different claim from the lifetime ratio in §3a |
| Near-decomposability; slow variables at higher levels | **KNOWN** | Simon 1962 (no DOI; already in THEORY §8); Simon & Ando 1961 |
| Multiresolution / multi-rate estimation | **KNOWN** | Willsky 2002; in this repository also Kiebel, Daunizeau & Friston 2008 and the Model S store results |
| Information priced as a flow constraint | **KNOWN** | Sims 2003 (rational inattention). That programme does not give \(T^*=\sqrt{6k/(w\sigma^2)}\); it is closer to a Kalman filter with a bit-rate cap than to lumpy re-formation |
| Fast-local, slow-shared at equal read quality | **KNOWN here** | CT35 / THEORY B.11, the OU factor \(e^{-2\ell/\tau}\) |
| Layer lifetime as the CL19 design variable, exponent \(\tfrac12\) in the re-forming cost | already claimed | `theory/FLUID_LAYERS_2026-11-21.md` (dated 21 Nov 2026, not locked) |

**New in this note, and only this.** (i) The exact spacing ratio in Model LS, and the proof that the same recursive rule does *not* supply a Shannon-style layer floor once specialization is dropped or the design class is Model S. (ii) The explicit D5 crossing \(\sigma^{2*}\) from the delayed lumpy cost, the necessity of \(\ell>0\), and the numerical finding that \(\tau>\ell\) is not sufficient. (iii) The testability map in §7. None of this is a field result.

## 7. Testability (draft prereg sketch; not locked; no outcome data retrieved)

**Could it fail in the world?** Yes. Frequency versus volatility at a single level is the menu-cost sign (Barro, Dixit) and would not discriminate. Karim, Carroll & Long 2016 already report that firms in the U.S. medical-device and pharmaceutical sectors *reduced* business-unit recombination during industry turbulence — the threat-rigidity / delay sign, not D5's. Girod & Whittington 2017 measure reconfiguration and restructuring frequency in large U.S. firms, and performance by environmental dynamism, which is a fitness ordering (the reason DIR1 excluded a similar firm result), not a design-response test unless the prereg asks only about frequencies and says so. Any serious test can lose on the sign, on the exponent, or by being the wrong class (smooth adjustment, no measurable \(k\), \(\ell\approx 0\)).

**What would discriminate.**

- **P1 (exponent in \(k\), already dated in the fluid-layers note).** In a class of groups that form and dissolve, with an independent measure of re-forming cost \(k\) moved by an outside shift, \(\log\) median lifetime against \(\log k\) has slope near \(\tfrac12\) at fixed drift. Kill: a preregistered band around \(\tfrac12\) (for example \([0.25,0.75]\)) is missed, or lifetimes do not move when \(k\) moves by more than \(10\times\). Fixed-period and barrier policies share this exponent; a rival with no lump predicts no discrete lifetimes; a fixed-calendar rival predicts no dependence on \(k\).
- **P2 (spacing in a measured stack).** Where a system has at least two lumpy layers with independently measured \((k_i,\sigma_i^2,w_i)\), the lifetime ratio matches the formula of §3a inside a preregistered factor (for example 2). Kill: the predicted order of lifetimes is reversed, or the ratio is off by more than the factor, in a class that qualifies under THEORY §3. This is the test that is actually about the recursive rule.
- **P3 (D5 sign).** When a shared update has measurable latency, faster drift of the common driver shifts weight from shared to local. Kill: a qualifying class moves the other way (threat-rigidity / Karim sign) at \(n\) above a preregistered floor. Conditions: \(\ell>0\); \(k_S<N k_L\) so shared is even on the table; the mid-scale warning of §5 is respected (do not treat \(\tau\gtrsim\ell\) as the crossing).

**Best real starting points, without fetching outcomes.** (1) Firm business-unit recombination and whole-firm restructuring series already collected for other questions (Karim et al. 2016; Girod & Whittington 2017): usable for P3 or for a frequency-vs-volatility check only after a locked mapping from "turbulence" / "dynamism" to \(\sigma^2\), and after an independent \(k\) for incremental versus pervasive change if P1 or P2 is attempted. Performance outcomes stay out of the score. (2) Project teams, chat channels, or open-source working groups, as already named in the fluid-layers dated prediction, if \(k\) can be moved by a tool or policy shift. (3) Fission–fusion animal groups (Aureli et al. 2008 is credited in the fluid-layers note; not re-resolved here) only if re-forming cost and drift of who should associate can be measured independently — that is the hard part, and it may not be available. Cells are a poor first try: a "layer lifetime" is easy to over-read into protein-complex or circuit turnover, and an independent \(k\) is rarely published.

**Not locked.** This section is a sketch. No hash, no scoring, no outcome retrieval.

## 8. Checks

`theory/layerlife_checks/layerlife_checks.py` (33 checks, ALL PASS). Identities and the Model LS spacing against a brute-force barrier grid; the joint-reset and two-layer-on-one-BM counterexamples; OU accuracy and failure regimes; the specialized count bound; the D5 crossing and the OU mid-scale miss; Model S store rates from `theory/layers_checks/stores.py` compared with \(T^*\). DOIs in `dois.txt` were resolved on Crossref on 21 November 2026 (`crossref.out`).

## References (DOIs resolved on Crossref, 21 Nov 2026, unless marked)

Dixit 1991, Rev. Econ. Stud. 58:141, doi 10.2307/2298051. Dixit 1991, J. Econ. Dyn. Control 15:657, doi 10.1016/0165-1889(91)90037-2. Chalkley 1997, Econ. Lett. 57:189, doi 10.1016/s0165-1765(97)00222-x. Caballero & Engel 1999, Econometrica 67:783, doi 10.1111/1468-0262.00053. Dixit 1989, J. Polit. Econ. 97:620, doi 10.1086/261619. Barro 1972, Rev. Econ. Stud. 39:17, doi 10.2307/2296440. Roundy 1985, Manage. Sci. 31:1416, doi 10.1287/mnsc.31.11.1416. Sims 2003, J. Monet. Econ. 50:665, doi 10.1016/S0304-3932(03)00029-1. Willsky 2002, Proc. IEEE 90:1396, doi 10.1109/jproc.2002.800717. Staw, Sandelands & Dutton 1981, Admin. Sci. Q. 26:501, doi 10.2307/2392337. Karim, Carroll & Long 2016, Acad. Manage. J. 59:791, doi 10.5465/amj.2012.0409. Girod & Whittington 2017 (Crossref issued date 2016; print volume 38, 2017), Strat. Mgmt J. 38:1121, doi 10.1002/smj.2543. Not re-resolved this pass: Simon 1962, Proc. Am. Philos. Soc. 106:467 (no DOI; already in THEORY); Simon & Ando 1961; Aureli et al. 2008, Curr. Anthropol. 49:627 (credited in the fluid-layers note); Kiebel, Daunizeau & Friston 2008 (already in the repository).
