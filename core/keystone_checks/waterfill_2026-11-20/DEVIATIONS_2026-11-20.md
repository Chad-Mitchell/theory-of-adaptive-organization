# Deviations: WF-HSV test, 20 November 2026

## D1 (before official start, before any reduced-order E_K)

**Time:** 9:56 PM ET (America/New_York).

**What changed.** The exclusion parser in `waterfill/worlds.py` (`_load_excluded`) treated `rhythm_rule.json` poles as already-complex arrays. Those files store poles as `[re, im]` pairs, which made the collision check crash (`shapes (4,) (2,2,2)`) when building predictions. The parser now accepts `[re, im]` pairs. The world *generators* (rng streams, formulas, ids) are unchanged. `PREREG.md` is unchanged (sha256 `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05`, locked 9:54:48 PM ET).

**Why this is not a rule change.** No inclusion threshold, world draw, R grid, or scoring gate was edited. The first prediction write had not completed, and no E_K optimisation had started.

## D2 (after the official result; post-result housekeeping)

**Time:** Friday 20 November 2026, about 11:55 PM ET (America/New_York), after official scoring at 11:17 PM ET and after the independent review of PR #121 (`reviews/wf_2026-11-20/REVIEW.md`, verdict READY-WITH-FIXES).

This is housekeeping, not a rule change and not a rescoring. No official count or gate is changed. Locked files (`PREREG.md`, `MATH.md`, `wf_rule.py`, `wf_predictions.json`) are not edited. `LOCK.txt`, `START.txt`, and the hashes embedded in the predictions file still record the as-run bytes.

**S1. Private workdir paths.** Newly authored, non-locked files had hardcoded box paths (`/workspace/gtao-wf/…`, and `/home/box/…` in the log). `worlds.py` now locates the repo root relative to this file (`Path(__file__).resolve().parents[3]`) so a public clone can load the exclusion inputs. `run_wf.py` uses the same repo-relative layout for the merged solver and writes its RESULTS template and output under `core/keystone_checks/waterfill_2026-11-20/`. `build_predictions.py` looks for `PREREG.md` / `MATH.md` beside itself, not in a workdir parent. `run_wf.log` path prefixes were redacted to repo-relative / package-relative forms; the warning text and run lines are otherwise unchanged. Mentions inside the hash-locked prereg, MATH.md, and `wf_rule.py` are left as historical locked text.

The as-run `worlds.py` hash remains the one recorded at prediction time (`f56ceaa3…`, post-D1). The file on this commit differs because of S1 and S2 only.

**S2. Exclusion-loader gap.** `PREREG.md` §4 says a draw within relative \(10^{-10}\) of any excluded world's \((a,v,N)\) is discarded and redrawn. The loader used for the official set only read `rhythm_rule.json`, and Model S worlds never called `_too_close`. S5 seeds 0..119, the 15 rhythm-prereg fractal worlds, and the T20 18 were not loaded. This was a procedure miss, not a contaminated set: the independent review found zero collisions of the 64 official worlds against the 21 rhythm-test worlds, S5 seeds 0..119, and the T20 18, at the prereg tolerance, and every official world has `bumps=0`. The loader is now the full prereg set (those three sources plus the 15 fractal worlds, reconstructed from the locked `scalefree_world` formula and the metadata in `imp_n60_predictions.json`), and Model S redraws on a collision with a recorded bump, for later use only. Official worlds and scores are not regenerated.

**S3. Third Lyapunov warning.** RESULTS.md's "Suspicious points" originally mentioned only the two rhythm-phase `RuntimeWarning`s. The official log also has a third, in the mixed phase, just before `mx_0006` completed. RESULTS.md now names all three. No world was flagged; no \(E\) was below the floor; not a gate change.

**S4 (documented only).** `wf_rule.predict` has a consistency fallback that is looser than locked MATH.md §7 item 5 (alternative target \(C W_c C^\top\), and a \(10\times\) tolerance). It was not used on any of the 64+3 official worlds, so no status would change. The fallback is left as it was in the locked `wf_rule.py`; this note records it. No rescoring.

