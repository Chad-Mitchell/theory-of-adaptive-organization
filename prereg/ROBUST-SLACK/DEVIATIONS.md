# ROBUST-SLACK deviations from the lock (`PREREG.md`, commit `a0e97cb`)

Each entry is dated, written before any data for this item were opened, downloaded or looked at, and follows
independent review 30 of PR #115 (READY-WITH-FIXES; the reviewer's notes are outside the repository). `PREREG.md` is
not edited; where an entry and `PREREG.md` disagree, the entry governs. Times are America/New_York.

## D1–D9 (Friday 20 November 2026, about 2:50 PM ET; branch `v2.7-robust`; one executor for Chad; no data opened)

**D1. RS-2a is replaced by a test with a calibrated null (review 30, must-fix 1).** *Why:* r_i = B_obs/(z·σ̂_i)
with σ̂_i from the system's own n_i windows. Because 1/σ̂ is right-skewed and noisier for short records, a class in
which every system holds a constant multiple of its true σ (the rival R-fixed) still shows Spearman ρ(ln r, ln F) > 0.
Under heavy tails the locked rule (Fisher/bootstrap lower bound > +0.10) then passes R-fixed: in the simulation below,
P(PASS | R-fixed) = 0.115 (t₄, 200 systems), 0.38 (t₄, 1000), 0.21 (t₃, 200), 0.75 (t₃, 1000). So PREREG §3's "RS-2a
PASS beats R-fixed" was false as written.
*New rule (RS-2a′).*
1. Standardize each system's shocks by its median and MAD (× 1.4826); fit a Student t with location 0 to the pooled
   standardized shocks by maximum likelihood: ν̂ (clipped to [2.05, 200]).
2. Null: M = 1000 replicates of the class in which system i has n_i shocks drawn from t_ν̂ and holds a constant
   multiple of its true scale; compute ρ\*_b = Spearman(−ln σ̂\*_i, ln F_i) in each. Let q₉₇.₅ and ρ̄₀ be the null's
   97.5% point and mean (rng seed 20261120).
3. Observed ρ with its 95% bootstrap interval over systems (B = 4000, as locked).
4. **PASS** iff the lower bound > q₉₇.₅ + κ; **FAIL** iff the upper bound < ρ̄₀ − κ (no more slope than a constant
   safety factor gives mechanically); else INCONCLUSIVE. κ = 0.10 as locked.
*Simulation* (`rs2a_null_sim.py`, output `rs2a_null_sim.json` and `.out`; reviewer's setup: n_i log-uniform on
[5, 40]; Fisher interval as a cheap stand-in for the bootstrap; 200 simulated classes per cell, 100 at 1000 systems):

| Shocks | Systems | ν̂ (mean) | P(PASS), locked rule | **P(PASS), RS-2a′** | P(FAIL), RS-2a′ |
|---|---|---|---|---|---|
| Gaussian | 200 | 5.3 | 0.01 | **0.000** | 0.015 |
| Gaussian | 1000 | 5.1 | 0.02 | **0.00** | 0.00 |
| t₄ | 200 | 2.9 | 0.115 | **0.000** | 0.000 |
| t₄ | 1000 | 2.9 | 0.38 | **0.00** | 0.00 |
| t₃ | 200 | 2.4 | 0.21 | **0.000** | 0.000 |
| t₃ | 1000 | 2.4 | 0.75 | **0.00** | 0.00 |

Under R-fixed RS-2a′ never passed: 0 of 200 per cell at 200 systems, so the rate is below about 1.5% (rule of
three), and 0 of 100 at 1000 systems, below about 3%. The stated design rate is at most 2.5%, the null's upper tail
before the κ margin. The MAD-standardized fit underestimates ν (5 for Gaussian shocks, 2.9 for t₄, 2.4 for t₃). That
makes the null heavier-tailed than the truth, which is conservative for PASS and costs power. Not simulated: shocks
outside the Student-t family (skewed, regime-switching). A class whose shocks are clearly skewed is scored with a
skew-t null fitted the same way, or else marked INCONCLUSIVE for RS-2a′.

**D2. Power and the minimum number of systems (must-fix 8f).** Same simulation, t₄ shocks, the alternative "every
system holds F_i^γ times its plug-in buffer":

| Systems | γ = 1 (full predictive buffer) | γ = 0.5 (half the effect) |
|---|---|---|
| 20 | 0.02 | 0.005 |
| 50 | 0.22 | 0.01 |
| 200 | 0.995 | 0.095 |
| 1000 | 1.00 | 0.98 |

At the locked minimum of 20 systems, RS-2a would almost never decide (the Spearman interval is about ±0.45).
**New minimum: 200 qualifying systems** with n_i spanning at least a factor of 4. Below 200, RS-2a′ is **UNTESTED**,
not INCONCLUSIVE. 200 systems detect only an effect near the full predictive buffer; a half-size effect needs about
1000. A PASS at 200 therefore means a large effect; a non-PASS at 200 says little about small ones.

**D3. Age confound (should-fix 8a).** Record length tracks age, and young firms and banks hold more reserve for
reasons unrelated to estimation risk: financing constraints and growth options (Almeida, Campello & Weisbach 2004, doi
10.1111/j.1540-6261.2004.00679.x; Bates, Kahle & Stulz 2009, already cited). New named rival **R-age**: r falls with
age through constraints, not through record length.
- Support now needs RS-2a′ PASS **and** a within-system test. For systems with at least 3 measurement dates, regress
  ln r on ln F within system (system fixed effects), with log size and one class-specific financing-constraint proxy
  as controls. The proxy is fixed in the class qualification file before data; for firms the default is a
  dividend-payer indicator.
- The within-system slope is scored against its own calibrated null, built as in D1 by re-estimating σ̂ as the
  simulated record lengthens. Same PASS/FAIL rule.
- If RS-2a′ passes and the within-system test does not, the label is INCONCLUSIVE (R-age not excluded).

**D4. No outcome-selected cut (should-fix 8b).** PREREG §1's rule that scores regulated systems only when B_obs > 1.05
× the regulatory minimum is withdrawn as the primary analysis, because it selects on the outcome. All systems are
scored. The 1.05 cut is reported only as a sensitivity analysis. R-reg is assessed as the share of systems within 5%
of the minimum.

**D5. Failure, ε and survivorship (should-fix 8c).**
- Each class's qualification file defines a *failure* before data, from a survivorship-free source. Defaults: banks,
  FDIC failure or assisted merger; firms, bankruptcy filing or delisting for performance reasons (per the exchange's
  delisting codes).
- ε is pooled over every system-window in which a system was alive at the window's start, failed systems included.
- RS-1 and RS-2a′ score every system alive at the measurement date. Failed systems' last pre-failure ratios are
  reported separately. Pooling only surviving systems is not allowed.

**D6. Hill estimator and RS-3 (should-fixes 8d, 8e).**
- RS-2b uses the Hill estimator only for systems with at least k = 10 upper order statistics in the top 10%, so
  n_i ≥ 100; other systems are UNTESTED for RS-2b. The class needs at least 50 such systems, or RS-2b is UNTESTED.
- RS-3 horizon: ε is per window, so the copy rule uses a one-window horizon (ε₁ = ε in CT37's notation).
- RS-3 share rule: the 80% criterion is scored on the 95% Wilson interval of the share with n_obs ≥ n_plug. PASS iff
  the lower bound ≥ 0.80; FAIL iff the upper bound < 0.50; else INCONCLUSIVE.
- RS-3's Spearman part is scored against a calibrated null built as in D1: systems hold the true-p count, k_i is
  drawn from Binomial(m_i, p̂_i), and the D1 PASS/FAIL rule applies.

**D7. PREREG §5 (GB) wording is corrected (must-fix 3).** Replace §5's last three sentences with:
- Copies and buffers (CT37, CT38) add no layers at new speeds.
- GRID-DX B1's count assumed ruin slack, while GB's ruin binds; by CT22 a binding constraint moves the design toward
  the survival-optimal end.
- The layer count under binding ruin, or under uncertainty, is not computed (CX7, OPEN).
- GB's gap of three layers is therefore neither explained nor shown to be waste.

A missing speed–endurance cost remains one further candidate, to be added publicly before any future test.

**D8. Prior art added (must-fix 2).** RS-2a′'s normative prescription, more capital than the plug-in when parameters
are estimated, is known:
- Gerrard & Tsanakas 2011, doi 10.1111/j.1539-6924.2010.01549.x;
- Bignozzi & Tsanakas 2016, doi 10.1111/jori.12075;
- for copies, Apostolakis & Kaplan 1981, doi 10.1016/0143-8174(81)90019-6.

What this prediction adds is only the empirical claim that *selected* systems follow it at a given estimated risk.
PREREG §4 is read with these added.

**D9. Lock evidence (review item 9).** `a0e97cb`'s time (1:45:43 PM ET) is local author time. It and the theory
commit `7c1dc22` first reached GitHub in one push (1:52:22 PM ET), so the lock-before-theory order is
**self-attested**, not independently timestamped. No data were involved. PREREG's references to CT37–CT40 point to
a file (`theory/ROBUSTNESS.md`) that was committed after the lock, in the same push. This file is likewise
self-attested, and is pushed on its own before the revision of the theory text.
