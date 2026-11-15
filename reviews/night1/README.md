# Night 1 (14–15 November 2026, America/New_York): formal layer, tests and hostile reviews

Private. These files are copied as-is from the working area on the agent box (`/workspace/gtao/night1/`). Paths inside them, such as `night1/POOLSIM/RESULTS.md`, refer to that working area. Simulation code, raw outputs and test folders were **not** copied.

| File | What it is |
|---|---|
| `CLAIM_MAP_FINAL.md` | **The current claim map.** Every claim has exactly one status: PROVED (in-model), PASSED (real data), KILLED, CIRCULAR/NOT EVIDENCE, OPEN, or PRIOR ART. It also has the "what is genuinely ours" section, the next-test programme (including a fair-kill vigilance spec), lock-integrity notes and open decisions. **This file supersedes the statements in `formal/`.** |
| `REVIEW_MATH.md` | Independent hostile mathematics referee: major revision, not rejection. **T5.6 "V ≥ 2" is wrong as stated** and is replaced by an exact formula. T1.8's sign claim holds only at small ρ. Several "iff" claims are downgraded. The T4 proof is a sketch. |
| `REVIEW_PHYSSTAT.md` | Independent physics and statistics referee: no GTAO-specific real-data support; simulation passes are circular; the exponents are not universal; the energy framing is decorative; lock audit. |
| `ANTS1_WRITEUP.md` | The only write-up of the ANTS1 simulation (by the physics/statistics referee): 3 locked in-model failures. |
| `REVIEW_PRIORART.md` | Independent prior-art referee: a synthesis with elementary new corollaries, not a new theory. Credits owed to Marschak & Radner 1972, Van Zandt & Radner 2001, Veldkamp & Wolfers 2007 and others. Title collision with Dessein & Santos 2006. |
| `formal/` | AXIOMS, THEOREMS, EXTENSIONS and FIXES **as reviewed**, i.e. *before* the referees' corrections. Read them together with `CLAIM_MAP_FINAL.md`. |
| `vfloor.py` | Numerical re-check (20,000 draws) of the math referee's exact vigilance formula, and of its floor V(N\*) ≥ 1 + (1+ρ)^(−1/2). |
