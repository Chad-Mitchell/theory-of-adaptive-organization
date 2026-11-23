# Hostile review: synthesis PR (README and CORE as one argument)

*Sunday 22 November 2026, late evening (America/New_York). **Not an independent review.** The same executor that wrote the synthesis did this pass after a deliberate break, re-reading each changed sentence against its source file. No separate agent was available. Scope: the new `README.md` and `CORE.md`, `history/2026-11-22_SYNTHESIS_DECISIONS.md`, the `STATUS.md` and `OPEN_WORK.md` pointers, and the front-page edits of PRs #216 and #217, which were also self-reviewed.*

## Invariants

- Hypothesis sentence byte-identical, once each in README, CORE, and THEORY: checked by `figures/master_curve_checks.py` §9 and `theory/holographic_checks` (count 1).
- `THEORY.md` unchanged by this PR (`git diff 1dafed2 -- THEORY.md` empty), so lines 26–32 and 41 are byte-unchanged.
- No "bill", no verdict or kill language, no "solved" hype, no "theory of everything"; "law" appears only in the hypothesis sentence (`tools/check_consistency.py` wording scan, 0 FAILs).

## Findings and fixes

| # | Where | Finding | Source re-read | Fix |
|---|---|---|---|---|
| F1 | README intro | "Minimize that cost and the best design falls out" read as universal. | `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` §3: closed forms are worked-class. | Now "In worked classes, minimizing that cost yields the best design". |
| F2 | README, The cost | Heat floor stated with no class. | `theory/GENERALITY_2026-11-22.md`: bipartite chains and additive-noise diffusions. | Class added. |
| F3 | README, general item 1 | R1 stated without "at least three essential coordinates" and "finite-law". | `theory/REPRESENTATION.md` Theorem R1. | Both conditions restored. |
| F4 | README, general item 4 | Blanket sufficiency stated without its loss condition. | `theory/GENERALITY_2026-11-22.md` item 4. | Now "a decision scored on the outside". |
| F5 | README, rebuild | "replacing units" dropped "identical"; the heterogeneous arm stays at no shock. | `theory/antifragility_checks/RESULTS.md`. | "identical units"; the heterogeneous puzzle stays in CORE §4. |
| F6 | README, acting (draft) | "wins only at higher stakes" generalized from two stakes. | `theory/ACTING_LOOP_2026-11-22.md`: gap negative at every fraction at stake 1, +0.033889928154 at stake 4. | Now "loses at unit stake and wins by a small margin at stake 4". |
| F7 | README step 2 (draft) | CT34 "enters its parent exactly as upkeep" overstated; the theorem gives exactness of partial minimization and an error when it does not enter as upkeep. | `THEORY.md` CT34. | Now "folds exactly into its parent's problem". |
| F8 | README step 3 | CX1 cited as proved without its review state. | `theory/THEOREM_P_DRIFT.md` header: repairs self-checked, re-confirm pending. | "in a draft awaiting re-confirmation". |
| F9 | CORE §2 | S2/S3 conflated; S3(ii) gives "some nonzero p ≥ 0". | `theory/SHANNON_2026-11-21.md` S2, S3. | Split and worded exactly; note marked not re-reviewed. |
| F10 | CORE §4 | Stakes-to-thermal ratio stated without FLOOR.md's own limit (no design work where the floor is loose). | `core/bridge_2026-11-21/FLOOR.md` lines 24–26. | Limit added. |
| F11 | CORE §4 | CT28 stated without its class. | `THEORY.md` CT28: upkeep-free power class. | Class added. |
| F12 | CORE §5 | "the floor saying when to stop" is not a stated result. | — | Now "the floor bounding what is left to gain", which follows from a lower bound. |
| F13 | Decisions file | Two reasons asserted things not in the repo (design rules restated on the physical cost; no N57 measurement planned). | `CORE.md` status words; CLAIM_MAP N57. | Reworded to what the files say. |

## Re-derived moved claims (no change needed)

- Curve: blind at or below \(x=1\), cost \(2\sqrt{kT a v w}-kT a\) above (`GENERAL_FORM_PHYSICS` §5; `figures/master_curve.md`).
- CT4 threshold \(\kappa<-(D\circ IB)'(0^+)\) and FLOOR.md's ratio \(>1\); CT11 \(q_f=2c/(W\tau_{\mathrm{life}}^2)\), \(q_c=(\mu u-h)^2/(2cW)\) (`THEORY.md` lines of CT4, CT11).
- CX1 random-walk floor \(D\ge q/(e^{2\bar r}-1)\), Kalman equality (`theory/THEOREM_P_DRIFT.md` §0; CLAIM_MAP PD2, PD6 PROVED (in-model)).
- Layer lifetime \(T^*=\sqrt{6k/(w\sigma^2)}\) and "a stack only when layers are specialized" (`theory/LAYER_LIFETIME_2026-11-21.md` lines 9, 17).
- Bridge: \(\pi\propto\exp(-\beta J)\) under weak mutation and a linear map, excess \(d/(2\beta)\) near a quadratic minimum (`core/bridge_2026-11-21/BRIDGE.md` lines 26–27).
- Conditions: T27 P1 pass, P3 fail (`core/bridge_2026-11-21/RESULTS.md`); EVO1 W4 3/8, W4b 8/8 at the no-sharing rival, W3 INVALID, store-noise arms INCONCLUSIVE (`tests/EVO1/RESULTS_EVO.md` lines 22–26).

## PRs #216 and #217, front-page edits

- #216: "SIM-1 (T28 P1–P4 passed in-model)" matches `core/sim1_2026-11-21/RESULTS.md` (OVERALL PASS, all 3/3, in-model). "Five further results" matches the six-item list (R1 plus five). Correct.
- #217: the "Where this is going" list and lost-ideas pointers are now folded or demoted per the decisions file; the Kalman–Bucy item stays labeled open. No dead reference found in the new text (each cited path exists; checked by listing).

## Lost load-bearing content

None found. Every number dropped from README is in CORE (15.473978, 0.020940, 0.171572875254, 0.033889928154) or in `figures/master_curve.md` (217.693). The five-term sum, its table, LY, IP5, and the puzzles stay in CORE. Demoted ideas are reachable from STATUS "Further results". CORE grew (3,316 to about 3,850 words) because the folds add sentences; the true one-page summary is still owed.
