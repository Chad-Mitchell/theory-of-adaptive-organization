# Addendum A3 (2026-11-15 ~6:35 PM ET): FRAMEWORK MV10 status at the real pre-shock n, before stage 4

Written by an executor for Ace (queue pick 31, item C3B-GATE-ADDENDUM, ledger 144), as required by PREREG §5 ("Real n ...
will be recorded in a dated addendum after the pre-shock screen and before stage 4") and by the CAUSAL-POWER-GATE audit
(`reviews/night2/CAUSAL_POWER_GATE.md` §5). PREREG.md, A1 and A2 are unchanged (hashes in PREREG.sha256 still hold).
Nothing in the hypotheses, models, SESOI or verdict rules changes.

**Data state when written.** Stages 1 (PyPI screen, done 2026-11-14 23:18 ET) and 2 (repo resolution and pre-shock
commit window, done 23:50 ET) are complete; stages 3 (exposure), 4 (fix window / tau), 5 (outcomes) and 6 have **not** been
run. Only stage-1/2 pre-shock files were read for this addendum (`data/candidates_resolved.csv`, `data/commits_pre.jsonl`
in the working copy at <local>/gtao/tests/C3b; no post-shock, tau, latency, star or outcome data exist or were fetched).

## 1. Real n
Arm P rows passing rules 1–4 after the dedupe (one row per repo × shock): **2,294** (numpy 1,063, pandas 532, pydantic 362,
sqlalchemy 166, urllib3 171; 2,116 distinct repos; 86 in the Valiev subset used by S10). The A1 cap (5,000) does not bind.
Rules 5 (exposure, stage 3) and 6 (alive at L, post-shock) are not yet applied, so **2,294 is an upper bound** on the
analysed n. Code: `reviews/night2/C3B_GATE_checks/count_n.py` (dedupe tie-break approximated as latest pre-shock upload,
then package name).

## 2. MV10 status of the mechanism verdict (primary)
Own simulation of the locked §6 rules (HIT = H1 95% lo > 0 and H2 95% lo > 0 and S9 90% lo > 0; MISS = K1 or K2), on PREREG
§5's own assumed covariate structure, 400 reps per cell (`reviews/night2/C3B_GATE_checks/gate_sim.py`, own code; MC SE ≤ 0.025):

| n | P(HIT \| β_τ 0.25, int 0.03) | P(MISS \| β_τ 0, int 0) | binding |
|---|---|---|---|
| 1,000 | 0.56 | 0.32 | both |
| 1,500 | 0.69 | 0.51 | both |
| **2,294 (upper bound)** | **0.86** | **0.65** | FAIL side |
| 5,000 (not reachable) | 0.99 | 0.93 | met |

Without PREREG §5's latent-activity confounder the sides swap: at 2,294, P(HIT) 0.75 (S9 binds: latency is nearly
collinear with tau) and P(MISS | null) 0.93. At the SESOI (β_τ 0.15) P(HIT) is 0.51. Closed-form cross-check
(`tools/power_gate.py contrast --effect 0.25 --sigma 0.046 --fail-eps 0.15`, H1/K1 only, no confounder): P(PASS) 0.9997,
P(FAIL | null) 0.90, gate met for H1/K1 alone; the simulated K1 rate (0.925 at SE 0.0447) agrees. The confounder biases
β̂_τ by about +0.045 under the null, which an absolute margin (K1's 0.15) cannot absorb (MV10's absolute-margin clause).

**Status: MV10 NOT MET at the real n.** Both probabilities rise with n and the analysed n cannot exceed 2,294, so under
the prereg's own assumptions at least one side stays below π = 0.8 at every reachable n (FAIL side 0.65 with the
confounder; PASS side 0.75 without). Meeting it would need roughly n ≈ 3,500–4,000 (interpolated, not simulated) with
the confounder present.

## 3. Reading rule (added now, before stage 4)
If stage 4 is run, the mechanism verdict is still computed and reported exactly as locked, but it is labelled
**exploratory (MV10 not met at lock)**: an INCONCLUSIVE means "gate not met", a MISS is not a kill of the C3/F1 line, and a
HIT is first-scale evidence only, as PREREG §8 already says. No CLAIM_MAP status changes on the mechanism verdict alone.
The index verdict (K3, bootstrap ratios) was not simulated here and carries the same label.

Limits: the simulation uses PREREG §5's assumed covariate distributions (event rate 0.30, its confounder), not real
data; plain (non-clustered) SEs (2,116 repos for 2,294 rows; clustering can only widen CIs, which lowers both
probabilities); landmark and exposure attrition are unknown and can only lower n.
