# Conjecture C, round 15: result against the pushed lock

Lock: `PREREG.md`, sha256 `470bd9053cb8cd5622ed474b99f8ece313bd8a617d70f02285eb4329803f8457`, pushed in commit ed1ceef at 05:09 EST on 2026-11-26. The lock was re-checked, and the run was launched at 05:09:19 EST from a fresh clone at ed1ceef.

**Correction to PREREG.md (the file is not edited).** It says it was written "at about 05:15 EST". It was in fact written at about 05:08 EST and pushed at 05:09 EST, before the run.

| Check | Output (`r15_h3.stdout`) | Score |
|---|---|---|
| V1, class counts | per factor 6 and 4 (as disclosed); the product count of 20 was never printed | not reached |
| V2, the test | the script crashed at 05:10:16 EST before the search: `AttributeError: 'AlgebraicField' object has no attribute 'from_list'` in the product step `fmul` | **not tested** (crash) |
| V3 | not reached | not tested |

The disclosed toy check exercised `from_sympy` but not `from_list`, which this sympy version does not have on the field object. Under this lock the run is not repeated. A corrected script would need a new, pushed preregistration, with every helper exercised on toy inputs before the lock.
