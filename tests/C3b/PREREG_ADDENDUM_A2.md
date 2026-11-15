# Addendum A2 (2026-11-14 ~22:55 ET): response to independent math review, before any post-shock or outcome data

Source: /workspace/gtao/attack/math/REVIEW.md (C3 section, G1), relayed by Ace at 22:49 ET. PREREG.md and A1 were already
hashed, so nothing in them changes. The items below are added as labeled SECONDARY analyses, not decisive, and do not alter
any primary hypothesis, model, SESOI or verdict rule. Stage 1 (pre-shock PyPI screen) was ~65% done; no post-shock, tau,
GitHub or outcome data had been fetched.

1. Convention pinned. z = B / (sigma * sqrt(tau)); large z = cold (safe), small z = hot. In C3b, E plays sigma, so
   ln z = ln B - ln E - 0.5 ln tau. PREREG H3's index z_PREREG = ln E - ln B + 0.5 ln tau is exactly -ln z; predicted
   risk rises as z falls. Same model, sign convention now explicit.

2. Fix-time distribution and predicted hazard ratios. C3b has one adapt time per (repo, shock), so a per-project
   distribution exists only for repos hit by several shocks (too few to fit). Added instead:
   - S11: the distribution of tau across dependents (Kaplan-Meier with censoring at 365 d; KM vs exponential-fit
     quartiles; CV and sd(ln tau) of fixed times; Hill tail index of the top 10% of fixed times; note the 365 d window
     truncates the tail, so the Hill index is biased upward, i.e. toward lighter tails).
   - S12: H1 re-fit with a complementary log-log link (interval-censored proportional hazards), giving a hazard ratio per
     doubling of tau, HR = 2^beta_tau, with 95% CI.
   - Predicted HR per doubling by fix-time type (from REVIEW G1, single-tau renewal model pinned to C3's regime):
     deterministic ~11; exponential ~3.0; lognormal sd(ln)=1 ~2.1; Pareto kappa=1.5 ~1.5; Pareto 1.2 / lognormal
     sd(ln)=2 ~1.2-1.26. Rule written now: classify the S11 shape as near-deterministic (CV < 0.5), exponential-like
     (0.5 <= CV <= 1.5 and sd(ln) < 1.5), or heavy-tailed (CV > 1.5 or sd(ln) >= 1.5); report whether the S12 HR CI covers
     that class's predicted HR (deterministic 11, exponential 3.0, heavy-tailed 1.2-1.5). Caveats stated in advance:
     these predictions assume C3's regime (h*tau ~ 0.009) and an exogenous single-tau renewal process; C3b's units
     (dormancy over a fixed window, tau = adapt time to one shock) are not the same clock, so a mismatch is evidence
     against the mapping as much as against the mechanism. Secondary, not a kill.

3. Endogeneity and survivorship guards.
   - Endogeneity (tau chosen in response to risk): no valid instrument is available; this is declared, not solved. Guards
     already registered: pre-shock B, activity and cadence controls, S7 (tau relative to cadence), S9 (latency control),
     placebo Arm Q. Interpretation rule added: if tau were tuned to hold z fixed, the cross-sectional beta_tau is biased
     toward negative values (down to elasticity -1); so a negative or null beta_tau is not by itself proof the causal
     effect is zero, and a positive one is not proof it is causal. Both will be stated.
   - Survivorship / never-adapters: unfixed dependents are NOT dropped: they stay in the primary sample with tau = 365 and
     unfixed = 1 (PREREG 3); S3 uses the unfixed indicator; S4 keeps dependents that went dormant inside the fix window
     (no landmark); S2 (fixed-only) is reported only as a contrast. Repos deleted before the pull are counted by arm.
