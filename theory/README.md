# Theory notes

Derivations that `THEORY.md` cites, and older working drafts. `THEORY.md` governs where they disagree. Files marked *Maintained* are kept consistent with THEORY by `tools/check_consistency.py`; the rest (`THEOREMS.md`, `GENERAL_THEOREM.md`, `INTERNAL_MODEL.md`, `MATH_ATTACK.md`) are frozen history cited by section. None of this is claimed as a new theorem. Each file labels what is already known, what is a calculation or a code check, and where the argument fails.

None of these is the core. THEORY v2.4 states the core and proves its results in its own Appendix B; the notes below are the reference derivations it cites, including the reach notes (`REACH.md`, `COSMIC_WEB.md`, `WORMHOLES.md`, `TORUS.md`), which extend the core's scope and are not part of it. `core_checks/` holds the checks of v2.0's closed forms. The one-page SCALE_ENDS summary is now `../history/2026-11-18_SCALE_ENDS_SUMMARY_FOR_CHAD.md`.

| File | What it is |
|---|---|
| `MASTER_EQUATION.md`, `meq_checks/` | The master equation (THEORY v2.4 §3–§6, B.6, B.9, B.10): the Master Theorem, special-case derivations, worked example, phase diagram (`phase.png`, illustrative), dynamics and regret, and (v2.2) the cost shares, floor multiplier and temperature checks (`meq_checks/scale_free_checks.py`). `meq_checks/meq_derive.py` asserts each special case derives from the equation (run by the test suite). v2.4 adds `meq_checks/ants_cx2_checks.py` (ant trail, CX2 classification) and `meq_checks/scope_checks.py` (judgment spend CT33, exact nesting CT34, and the scope fixes of the v2.3 review), and `../figures/face_model.py`, `face_regions.py` (the face figure's regions, computed from J). |
| `LAYERS.md`, `layers_checks/` | When layers beat one flat tracker: L1–L4 with proofs and numerics (THEORY CT21, CL12). New, not yet independently reviewed. |
| `THEOREMS.md` | The application-facing theorem note (copy of the public `adaptive-memory-levels` version), with steps labeled KNOWN / PROOF / NUMERIC / ANALOGY / FAILS. |
| `theorems-checks/` | Symbolic and numeric checks for `THEOREMS.md`. |
| `GENERAL_THEOREM.md` | Broader "general theorem" draft (solvency bound, when a checked copy beats fading, temperature as a first-passage form, scale-invariance limits, and listed failures). |
| `INTERNAL_MODEL.md` | Companion draft on when a system should carry an internal model. |
| `theorem-v2-checks/` | Code checks for those two drafts. |
| `MATH_ATTACK.md` | Hostile mathematical pass: what follows from one objective, what does not, the thermodynamic floor, and proposed decisive tests. |
| `math-checks/` | Code checks for `MATH_ATTACK.md`. |
| `REACH.md`, `COSMIC_WEB.md`, `WORMHOLES.md`, `TORUS.md` | Maintained. (v1.4.23; corrected v1.4.24 after `reviews/reach_2026-11-18/INDEPENDENT_REVIEW.md`; open items worked v1.4.25; second independent review `reviews/reach_2026-11-18/INDEPENDENT_REVIEW_2.md` applied v1.4.26) Viruses and what counts as life (the cost ledger), the cosmic web as a network, wormholes (CONDITIONAL), the torus and cosmic topology, dark matter and energy as inputs, fractal time stated exactly. Labelled DERIVED / RESTATEMENT / PRIOR ART / HYPOTHESIS / CONDITIONAL. |
| `SCALE_ENDS.md`, `scale_ends_checks/` | The ends of the scale (atoms, stars, black holes, the horizon; LAT-1), cited by THEORY §2.3; independently reviewed (`reviews/night2/SCALE_ENDS_INDEP_REVIEW.md`). Maintained. |
| `BOOKENDS.md`, `bookends_checks/` | How the pieces fit, from chemistry to heat death (keep / hold / know), cited by THEORY §0; reviewed in `reviews/bookends/`. Maintained. |
| `theorems-checks/` | Checks for `THEOREMS.md`. |
| `reach_checks/` | Code and saved output for those notes: proximity-graph nulls, pooling and station-catchment checks, the sine circle map. |

Reviews of these documents live in `../reviews/`.
