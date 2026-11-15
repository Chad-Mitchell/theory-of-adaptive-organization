# GITHUB-UPSTREAM addendum: regime gate (pre-outcome)

Written Sunday 15 November 2026, about 09:05 AM ET, by a Grok Bot executor for Chad (via Ace), as part of `AUDIT_DIVERGENCE.md` §5. **Before any outcome:** at writing, `night2/GITHUB/data/` held only `search_hits.json`, `files.json` and `repos.json`; scheduled-run histories (the outcome inputs) had not been pulled. The commit time of this file in the private repo is its lock time. The original PREREG.md, code, seed and rules are unchanged and remain primary; this addendum only adds a gate and an interpretation rule.

**Why.** PREREG §4 sets the drift-matching band b ∈ [0.35, 0.65] from class R with a = b = ½. Under THEORY.md v1.2 §2.5 that is the regime-A (H = ½) instance. For reset-type reads with Hurst exponent H, formal Lemma 1(i) gives a = b = 1/(1+2H). Drift here is measured as an event frequency (a declared proxy; FRAMEWORK §3.1 lists it as a failure mode), so the regime must be checked on the same series before the band is read.

**Gate (computed by a separate script before `analyze.py`'s P1/P2 output is read; same SEED 20261115, B = 999 cluster bootstrap over primary upstreams).**
1. For every flat unit, take the weekly change-indicator series |Δx| already defined in PREREG §3.
2. Allan-factor slope: for block sizes T ∈ {1, 2, 4, 8, 13} weeks, compute the Allan factor of block counts; pool across units by median at each T; fit ln AF on ln T. Ĥ = (slope + 1)/2 (count-process proxy for H).
3. Rules:
   - Ĥ CI includes 0.5 and has width ≤ 0.4 → **regime A on this proxy**: PREREG P1/P2 bands and P6 floor apply as locked.
   - Ĥ CI excludes 0.5 → **not regime A**: P1/P2 are scored against b = a = 1/(1+2Ĥ) ± 0.15 in place of [0.35, 0.65], with the PREREG's PASS/KILL wording otherwise unchanged; the original-band verdicts are also reported. P6 is reported for direction only (V > 1 iff a ≥ b, which does not depend on H for R1); its numeric floor is not scored.
   - CI width > 0.4 → **regime not established**: P1/P2/P6 verdicts are reported as "on the event-frequency proxy, regime unestablished" and cannot change any CLAIM_MAP status.
4. Everything here stays inside the PREREG's Tier-2 ceiling.
