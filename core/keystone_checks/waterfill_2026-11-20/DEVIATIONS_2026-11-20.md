# Deviations: WF-HSV test, 20 November 2026

## D1 (before official start, before any reduced-order E_K)

**Time:** 9:56 PM ET (America/New_York).

**What changed.** The exclusion parser in `waterfill/worlds.py` (`_load_excluded`) treated `rhythm_rule.json` poles as already-complex arrays. Those files store poles as `[re, im]` pairs, which made the collision check crash (`shapes (4,) (2,2,2)`) when building predictions. The parser now accepts `[re, im]` pairs. The world *generators* (rng streams, formulas, ids) are unchanged. `PREREG.md` is unchanged (sha256 `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05`, locked 9:54:48 PM ET).

**Why this is not a rule change.** No inclusion threshold, world draw, R grid, or scoring gate was edited. The first prediction write had not completed, and no E_K optimisation had started.
