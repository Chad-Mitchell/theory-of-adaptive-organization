# Layer lifetime as a stack rule: spacing, a layer floor, and local vs shared

*Saturday 21 November 2026, written about 2:30 PM ET (America/New_York), first stacked on PR #139 (`theory/FLUID_LAYERS_2026-11-21.md`); revised after the independent hostile review of `3b94aef`, about 2:40 PM ET; rebased onto main after #139 merged as `0726423`. Checks: `theory/layerlife_checks/layerlife_checks.py` (output `layerlife_checks.out`; run by `tools/test_layerlife_checks.py`). Labels: **PROVED** (a proof is given here or cited, inside the stated model), **KNOWN** (published, credited), **NUMERICAL** (computed, not proved), **ANALOGY**, **OPEN**, **FALSE** (a stated claim that does not hold). Proved in-model says nothing by itself about nature. Not a lock. Not yet independently reviewed when first written. The hypothesis sentence is unchanged: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."*

## 0. Bottom line, in plain words

The shared-layer lifetime in the fluid-layers note,

$$\tau_{\text{layer}}=T^*=\sqrt{6k/(w\sigma^2)},$$

is the right refresh rule for a lumpy layer, and it belongs with the core, not as a footnote. Applied recursively, it does two things cleanly and fails to do a third.

1. **Spacing (PROVED, in a specialized stack).** If each layer can reset only its own component of a drifting world, and the loss is quadratic in the total error, the layers' lifetimes stand in the exact ratio
   \(T_i^*/T_j^*=\sqrt{(k_i/k_j)\,(\sigma_j^2/\sigma_i^2)}\)
   (equal stakes). That is a spacing rule. It is not a universal geometric series: the ratios are set by the costs and the drifts, and they collapse or invert when those inputs do.
2. **Local vs shared (PROVED for a Brownian common driver, fixed-period refreshes, latency on the shared observation only; NUMERICAL for OU).** The same cost, with delay \(\ell>0\) on the shared observation and none on the local ones, gives the fast-local / slow-shared sign. The fixed-period crossing is the \(\sigma^{2*}\) in §5. The optimal barrier under the same observation delay keeps the sign and divides that crossing by 3. An equal delay on local updates cancels the floor, and there is again no switch. "Slower than the latency" is not enough: at the prices in the checks the OU crossing is about \(183\ell\), so shared still lost at \(\tau=40\ell\) and won at \(\tau=400\ell\).
3. **A computable floor on the number of layers (mostly FALSE as hoped).** The lifetime rule does not close the gap left in PR #139 — "the fewest layers that reach accuracy \(D\) in this world." One lumpy tracker, refreshing at \(T^*\), is already optimal for a single process, including a fractal (power-law) one. A stack appears only when layers are *specialized* (a layer cannot reset the whole state). Under that restriction there is a simple count lower bound, but it comes from the components' variances, not from \(T^*\). In Model S the fewest-stores floor remains the existing numerical \(E_K\); \(T^*\) is a different object (a reset interval, not a store time constant), and the two spacing ratios do not match. No \(T^*\)-converse was recovered. The layer-count converse already in the repository is CT21 (L3): a continuum of time scales has no exact finite design (a non-rational spectrum has no finite exact store set).

So the formula is core as a *timing* rule for lumpy layers, and as the cost that also decides local vs shared. It is not a substitute for a layer-count limit.

## 1. Could it fail? (checked before each piece)

- **Spacing from a recursive \(T^*\).** It could fail if layers are not specialized, if one action can reset several components cheaply, if the target is mean-reverting on the scale of \(T^*\), or if adjustment is smooth rather than lumpy. Those failures are demonstrated below. It could also have been only a restatement of Roundy's integer-ratio lot schedules. The formula here is a ratio of optimal lifetimes, not a claim that integer-ratio *clocks* are within a stated percent of a joint schedule.
- **A layer-count floor from the same rule.** It could fail, and in the unrestricted design class it does: one joint reset of the sum beats a stack when that reset is not much dearer than a single part. A fractal spectrum does not, by itself, force many layers. This was the main hope, and it should be scored as not met.
- **D5 from the same inequality.** It could fail if shared updates have no latency (then amortization alone makes shared cheaper at every drift, or never, with no switch), or if the same delay sits on local updates (the floors cancel). It could fail in the field: threat-rigidity (Staw, Sandelands & Dutton 1981) predicts constriction of control under threat, and Karim, Carroll & Long 2016 report less business-unit recombination during industry dynamism — the opposite of the menu-cost frequency prediction, but not by itself the opposite of the fast-local sign. The derivation is not a field result.
- **Prior art.** The square-root lifetime is Dixit's. Barro 1972's random-walk object is a fourth-root inaction band; the square-root lifetime is the mean exit time of that band, which is how `theory/measured/TESTBEDS.md` already uses him, and a deterministic inflation menu cost is a cube-root interval. Claiming the exponent \(\tfrac12\) as new would be false. The assembly — layer lifetime as the design variable, the specialization caveat, and D5's crossing from the same cost — is what can be new, and only that.

## 2. The single-layer rule (KNOWN)

CL19 (a), after Dixit (1991, *Review of Economic Studies* and *JEDC*; Chalkley 1997 notes that the quadratic-loss approximation is exact at zero discounting, which is the case used here): a gap that drifts as Brownian motion with variance rate \(\sigma^2\), costs \(w\,x^2\) per unit time, and is reset to zero at lump cost \(k\), is left alone until \(|x|\) hits \(b^*=(6k\sigma^2/w)^{1/4}\). The expected time between resets is \(b^{*2}/\sigma^2\), which is \(T^*=\sqrt{6k/(w\sigma^2)}\). The excess cost rate is \(2\sqrt{kw\sigma^2/6}\). This is the formula in `theory/FLUID_LAYERS_2026-11-21.md` and is re-checked in `layerlife_checks.py` §1 (grid minimizer, scaling, identities).

The same scaling with a different coefficient holds for a *fixed-period* refresh (the EOQ / Regime A cousin already in THEORY: \(T_{\text{fix}}^*=\sqrt{2k/(w\sigma^2)}\), cost \(\sqrt{2kw\sigma^2}\)). The barrier lifetime is \(\sqrt{3}\) times the fixed-period lifetime and is cheaper, because it does not reset when the gap is still small. The exponent \(\tfrac12\) in \(k\) and in \(1/\sigma^2\) is the same for the coefficient 6 and the coefficient 2. The factor 3 in §5 uses both: the barrier excess equals the fixed-period excess divided by \(\sqrt{3}\), and the variance-rate crossing is the fixed-period crossing divided by 3.

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

**What is FALSE.** Without the specialization premise, the bound is false, and so is any claim that a power-law or fractal spectrum forces many lumpy layers. If one action can take a perfect (or cheap) observation of the *sum* and reset a single estimate, the residual starts at zero and a short enough hold meets any \(D>0\) with \(K=1\). Two full-reset layers on one Brownian motion cannot beat the cheaper layer alone (checks §5). For a single fractal process with increment variance \(\propto\tau^{2H}\), the fixed-period balance \(k/T+w C T^{2H}/(2H+1)\) (mean square over the hold is \(C T^{2H}/(2H+1)\); the omitted factor does not change the exponent) gives one refresh time \(T^*\propto(k/(wC))^{1/(2H+1)}\) (and \(H=\tfrac12\) recovers the square-root rule). That is still one layer.

**Model S is a different design class.** There the layers are continuous leaky stores behind white sensing noise, priced by upkeep \(hK\), and the fewest stores that reach a given error is the existing numerical \(E_K\) (`theory/layers_checks/stores.py`). On a two-mode world the optimal store rates interlaced the world rates, as THEORY already states (L2). The Dixit lifetime ratio of the two modes, at equal \(k,w\), was 10; the ratio of the optimal store time constants was about 47. They are not the same spacing rule, and \(T^*\) does not compute \(E_K\). No \(T^*\)-converse was recovered. The layer-count converse already in the repository is CT21 (L3): a continuum of time scales has no exact finite design (a non-rational spectrum has no finite exact store set). L3 says \(E_K>E_\infty\) for every finite \(K\) on that spectrum, and \(K^*\to\infty\) only if also \(E_K\to E_\infty\) (THEORY.md, CT21). That is a statement about Model S's \(E_K\), and \(T^*\) does not compute \(E_K\). The layer-term floor of PR #139 stays **OPEN**.

## 4. Where a recursive stack is the wrong design

- **Joint reset cheaper than the parts (PROVED).** If a single action can reset the sum at cost \(\min(k_1,k_2)\) (or any cost not much larger than one part), one layer beats two. If instead a joint reset costs the *sum* \(k_1+k_2\), specialization is never more expensive: \(\sqrt{(k_1+k_2)(\sigma_1^2+\sigma_2^2)}\ge\sqrt{k_1\sigma_1^2}+\sqrt{k_2\sigma_2^2}\), with equality iff \(k_i/\sigma_i^2\) are equal (checks §3). So whether a stack pays depends on how the lump costs add when scopes merge. That has to be measured, not assumed.
- **Smooth adjustment.** No discrete \(T^*\) (CL19 (c)).
- **OU on a long lifetime.** The Brownian \(T^*\) mis-times the refresh (checks §4).
- **Already in the repository.** Span invariance of store spacing failed in-model (LAYERS1 P2, CLAIM_MAP G20, SIM-FAIL). Geometric clocks remain proved in the shared-clock model (CL12); they were not withdrawn. A holographic count (layers growing with the log of the scale range, at roughly equal value each) failed in-model (`core/KEYSTONE_NOTE.md` §5). Those were Model S tests, not Model LS, but they are a warning against treating "fractal time \(\Rightarrow\) a stack with geometric lifetimes" as a theorem.

A stack of lumpy lifetimes is the right object when re-forming is lumpy *and* a layer cannot (or cannot afford to) rewrite the whole state: a team tweak versus an org-chart rewrite, a local estimate versus a shared grouping, a shallow edit versus a deep redesign. That is a scope restriction, close in spirit to Simon's near-decomposability, not a consequence of \(T^*\) alone.

## 5. Local vs shared (D5) from the same cost

The fast-local / slow-shared sign is already in the repository: at equal read quality, \(X_S=\nu\cdot\pi\cdot e^{-2\ell/\tau}X_L\) (THEORY B.11, OU closed forms; `figures/face_placements.md`, nesting CT28 and CT34). CT35 is the subadditivity map theorem, not this factor. DIR1 (PR #138, merged to main as `1cb1ac2`) states the same sign as D5, attributing it to CT35 with the B.11 factor; D5 went unscored (\(n=2\)).

**Question.** Does the same sign fall out of the lifetime cost?

**Brownian common driver, fixed-period refreshes, latency \(\ell\) on the shared observation (PROVED).** \(N\) units, common variance rate \(\sigma^2\), local lump \(k_L\), shared lump \(k_S\), stake \(w\) per unit. Local total cost \(N\sqrt{2k_L w\sigma^2}\). Shared cost \(\sqrt{2k_S(Nw)\sigma^2}+Nw\sigma^2\ell\) (the second term is the delay floor). Shared can win at \(\ell=0\) iff \(k_S<N k_L\). With \(\ell>0\) there is a single crossing

$$\sigma^{2*}=\Biggl(\frac{\sqrt{2k_L w}-\sqrt{2k_S w/N}}{w\ell}\Biggr)^2,$$

provided the numerator is positive. Below \(\sigma^{2*}\), shared is cheaper; above it, local is cheaper. The checks recover the crossing to machine precision and confirm: no switch when \(\ell=0\).
This \(\sigma^{2*}\) is the fixed-period, shared-only-delay object. For the optimal barrier on the delayed gap the floor \(Nw\sigma^2\ell\) is unchanged, the excess cost is \(2\sqrt{kw\sigma^2/6}\) rather than \(\sqrt{2kw\sigma^2}\), the sign is unchanged, and the crossing is this value divided by 3. If local updates carry the same observation delay, both sides have the floor \(Nw\sigma^2\ell\). The floors cancel. The gap that remains is \(\sqrt{\sigma^2}\bigl(\sqrt{2k_S Nw}-N\sqrt{2k_L w}\bigr)\) for fixed-period refreshes, and that gap divided by \(\sqrt{3}\) for the barrier. The sign is the same at every \(\sigma^2\), so there is no switch.

**OU companion (NUMERICAL).** The same prices and \(\ell=0.5\): local won at \(\tau=0.05\) (shared's optimum was the blind cost \(Nw v\)); shared still lost at \(\tau=20=40\ell\); shared won at \(\tau=200=400\ell\). The crossing at these prices is about \(183\ell\), against the Brownian fixed-period prediction \(2v/(\sigma^{2*}\ell)\approx 185\). Those multiples move with \(k_S/(N k_L)\) and with \(k/(wv\ell)\). The sign agrees with the OU factor in B.11. The naive rule "share once \(\tau>\ell\)" is **FALSE** at these prices.

**Rivals.** Threat-rigidity (Staw, Sandelands & Dutton 1981) predicts restriction of information processing and constriction of control under threat, defined there as impending harm, with influence concentrated at higher levels. That paper does not state a sign in \(\sigma^2\). A no-response rival predicts no switch.

This does not replace the OU factor in B.11 (CT28, CT34). It is the lumpy, delayed-observation companion, and it makes the lifetime rule and the fast-local / slow-shared sign the same cost.

## 6. Prior art: what is known, and what is new

| Piece | Status | Credit |
|---|---|---|
| Inaction band, \(b^*\propto k^{1/4}\), lifetime \(T^*\propto\sqrt{k/\sigma^2}\) | **KNOWN** | Dixit 1991 (RES and JEDC); Chalkley 1997 (undiscounted exactness); CL19 in `theory/DYNAMICS.md` |
| Square-root refresh / menu-cost frequency | **KNOWN** | Barro 1972 (random-walk fourth-root band; square-root lifetime is the exit-time corollary; deterministic menu costs are cube-root); Regime A / CT12 in THEORY; already marked prior art in `theory/measured/TESTBEDS.md` (central-bank meetings) |
| Aggregation of lumpy units | **KNOWN** | Caballero & Engel 1999; CL19 (d) |
| Integer-ratio / multi-level replenishment schedules | **KNOWN** | Roundy 1985 (98%-effective integer-ratio lot-sizing, *Management Science* 31:1416). A *schedule* constraint (nested integer ratios) is a different claim from the lifetime ratio in §3a |
| Near-decomposability; slow variables at higher levels | **KNOWN** | Simon 1962 (no DOI; *Proc. Am. Philos. Soc.* 106:467–482; credited in THEORY §10); Simon & Ando 1961 |
| Multiresolution / multi-rate estimation | **KNOWN** | Willsky 2002; in this repository also Kiebel, Daunizeau & Friston 2008 and the Model S store results |
| Information priced as a flow constraint | **KNOWN** | Sims 2003 (rational inattention). That paper does not give \(T^*=\sqrt{6k/(w\sigma^2)}\). Its abstract says a finite Shannon capacity can resemble a signal-extraction problem or an adjustment cost. It is not the Dixit band |
| Fast-local, slow-shared at equal read quality | **KNOWN here** | THEORY B.11, the OU factor \(e^{-2\ell/\tau}\); `figures/face_placements.md`, nesting CT28 and CT34. CT35 is the subadditivity map theorem |
| Layer lifetime as the CL19 design variable, exponent \(\tfrac12\) in the re-forming cost | already claimed | `theory/FLUID_LAYERS_2026-11-21.md` (dated 21 Nov 2026, not locked) |

**New in this note, and only this.** (i) The exact spacing ratio in Model LS, and the proof that the same recursive rule does *not* supply a Shannon-style layer floor once specialization is dropped or the design class is Model S. (ii) The explicit D5 crossing \(\sigma^{2*}\) from the delayed lumpy cost, the necessity of \(\ell>0\), and the numerical finding that \(\tau>\ell\) is not sufficient. (iii) The testability map in §7. None of this is a field result.

## 7. Testability (draft prereg sketch; not locked; no outcome data retrieved)

**Could it fail in the world?** Yes. Frequency versus volatility at a single level is the menu-cost sign (Barro, Dixit) and would not discriminate. Karim, Carroll & Long 2016 report that 46 U.S. medical-device and pharmaceutical firms reduced business-unit recombination during industry dynamism, and also when top-management-team size grew. The paper reads that as decision avoidance and delay. The negative coefficient is the opposite of the menu-cost frequency prediction. It is not a local-versus-shared contrast: there is no local margin, no latency, and no variance rate of the structure being tracked. The negative coefficient is not, by itself, the opposite of the fast-local sign. Girod & Whittington (Crossref issued 2016-07-11, print 2017) regress Tobin's Q and ROA on restructuring and reconfiguration, with Dess–Beard dynamism, the standard error of industry-sales growth, as a moderator. That is a fitness ordering. Their counts (about four reconfigurations a year, restructurings about every six years, 1985 Fortune 50 industrials through 2004) are not a regression of frequency on \(\sigma^2\). Any serious test can lose on the sign, on the exponent, or by being the wrong class (smooth adjustment, no measurable \(k\), \(\ell\approx 0\)).

**What would discriminate.**

- **P1 (exponent in \(k\), already dated in the fluid-layers note).** In a class of groups that form and dissolve, with an independent measure of re-forming cost \(k\) moved by an outside shift, \(\log\) median lifetime against \(\log k\) has slope near \(\tfrac12\) at fixed drift. Kill: a preregistered band around \(\tfrac12\) (for example \([0.25,0.75]\)) is missed, or lifetimes do not move when \(k\) moves by more than \(10\times\). Fixed-period and barrier policies share this exponent; a rival with no lump predicts no discrete lifetimes; a fixed-calendar rival predicts no dependence on \(k\).
- **P2 (spacing in a measured stack).** Where a system has at least two lumpy layers with independently measured \((k_i,\sigma_i^2,w_i)\), the lifetime ratio matches the formula of §3a inside a preregistered factor (for example 2). Kill: the predicted order of lifetimes is reversed, or the ratio is off by more than the factor, in a class that qualifies under THEORY §3. This is the test that is actually about the recursive rule.
- **P3 (D5 sign).** When a shared update has measurable latency, faster drift of the common driver shifts weight from shared to local. Kill: a qualifying class moves the other way (more shared as drift rises) at \(n\) above a preregistered floor. Conditions: latency on the shared channel only, not equally on local updates; \(k_S<N k_L\) so shared is even on the table; the mid-scale warning of §5 is respected (do not treat \(\tau\gtrsim\ell\) as the crossing).

**Best real starting points, without fetching outcomes.** (1) Firm business-unit recombination and whole-firm restructuring series already collected for other questions (Karim et al. 2016; Girod & Whittington 2017): not identifiable as P2 or P3. A locked map from industry-sales dynamism onto \(\sigma^2\) would be a rescue lever. The series contain neither the variance rate of the tracked gap, nor a re-forming cost \(k\), nor a shared-update latency \(\ell\). Girod's two counts could support a frequency comparison only after those prices are measured independently. They do not identify P3. Performance stays out of the score. A fair measure would need an independent re-forming cost \(k\), the variance rate of the tracked structure, latency on the shared channel, and the \(N\)-local-versus-one-shared distinction. (2) Project teams, chat channels, or open-source working groups, as already named in the fluid-layers dated prediction, if \(k\) can be moved by a tool or policy shift. (3) Fission–fusion animal groups (Aureli et al. 2008 is credited in the fluid-layers note; not re-resolved here) only if re-forming cost and drift of who should associate can be measured independently — that is the hard part, and it may not be available. Cells are a poor first try: a "layer lifetime" is easy to over-read into protein-complex or circuit turnover, and an independent \(k\) is rarely published.

**Not locked.** This section is a sketch. No hash, no scoring, no outcome retrieval.

## 8. Checks

`theory/layerlife_checks/layerlife_checks.py` (26 checks, ALL PASS; tautological comparisons are labelled identities and are not in the pass count). Identities and the Model LS spacing against a brute-force barrier grid; the joint-reset counterexample and the two-layer domination argument (the dearer full reset is never used); OU accuracy and failure regimes, including the case \(k>wv/(2a)\) where tracking need not pay; a short-hold \(K=1\) bound on a Brownian sum; the specialized covering count (stated as an identity); the D5 crossing and the OU mid-scale miss (crossing about \(183\ell\) at the check prices); Model S store rates from `theory/layers_checks/stores.py` compared with \(T^*\). DOIs in `dois.txt` were resolved on Crossref on 21 November 2026 (`crossref.out`); Dixit 1989 was listed and unused, and is dropped from that list.

## References (DOIs resolved on Crossref, 21 Nov 2026, unless marked)

Dixit 1991, Rev. Econ. Stud. 58:141, doi 10.2307/2298051. Dixit 1991, J. Econ. Dyn. Control 15:657, doi 10.1016/0165-1889(91)90037-2. Chalkley 1997, Econ. Lett. 57:189, doi 10.1016/s0165-1765(97)00222-x. Caballero & Engel 1999, Econometrica 67:783, doi 10.1111/1468-0262.00053. Barro 1972, Rev. Econ. Stud. 39:17, doi 10.2307/2296440. Roundy 1985, Manage. Sci. 31:1416, doi 10.1287/mnsc.31.11.1416. Sims 2003, J. Monet. Econ. 50:665, doi 10.1016/S0304-3932(03)00029-1. Willsky 2002, Proc. IEEE 90:1396, doi 10.1109/jproc.2002.800717. Staw, Sandelands & Dutton 1981, Admin. Sci. Q. 26:501, doi 10.2307/2392337. Karim, Carroll & Long 2016, Acad. Manage. J. 59:791, doi 10.5465/amj.2012.0409. Girod & Whittington 2017 (Crossref issued date 2016; print volume 38, 2017), Strat. Mgmt J. 38:1121, doi 10.1002/smj.2543. Not re-resolved this pass: Simon 1962, Proc. Am. Philos. Soc. 106:467–482 (no DOI; already in THEORY §10); Simon & Ando 1961; Aureli et al. 2008, Curr. Anthropol. 49:627 (credited in the fluid-layers note); Kiebel, Daunizeau & Friston 2008 (already in the repository).
