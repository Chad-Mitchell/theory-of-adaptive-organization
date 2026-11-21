# Re-confirm: GTAO core piece 1 (after B1–B3 and the S5 rerun)

Reviewer: separate executor; wrote none of `CORE.md`, `core/KEYSTONE_NOTE.md`, `core/keystone_checks/S5_RESULTS.md`, `s5_rerun.py`, `OPEN_WORK.md`, `PLAN.md`, `CHANGES_SUMMARY.md`, or the earlier reviews (`/workspace/review-archive/core_REVIEW.md`, `core_CONFIRM.md`).
Friday 20 November 2026, about 5:40 PM ET (America/New_York).
Drafts in `/workspace/gtao-core`, beside `origin/main` = `a1a98aa` (PR #116 merged as v2.68; #117 is `b12af70`, v2.67; #115 is `1998a2d`, v2.66). CLAIM_MAP on that commit is v2.68: OPEN 84, PROVED (in-model) 94, MATH-CORRECTED 23, PRIOR ART 32, total 318. `python3 -m pytest --collect-only -q tools` reports **118 tests collected**. Working tree is untracked relative to `a1a98aa` (`CORE.md`, `OPEN_WORK.md`, `core/`, …). Nothing was edited, pushed, or merged in this pass, except the side-effect of the requested S5 rerun (it rewrote `s5_rerun.json` timing fields; scientific fields unchanged). Compute at nice 19.

First review: READY-WITH-FIXES (B1 CT41 wording; B2 pair-rule rescue). Confirm review: READY-WITH-FIXES (B3 hull increment is the definition of K*, not a predictive rule). This re-confirm is against those two reviews, `main` `a1a98aa`, and CLAIM_MAP v2.68, with an independent rerun of `s5_rerun.py`.

## Verdict: READY-WITH-FIXES (1 remaining textual fix)

B1–B3 are fixed. The scoped claims the confirm review required are in place: the predictive keystone is numerically supported only in Model S, given convexity, which remains unproved; the increment formula is false for rhythms; a predictive rhythm rule is OPEN; the K* = 0 hole is stated; "law" on the core page appears only in the hypothesis sentence. I independently reproduced the S5 headline numbers, and I independently recounted the rhythm-sweep empirical counts from `rhythm_rule.json`. Claim IDs cited in the four files exist in CLAIM_MAP v2.68 (or, for L1–L3 and EVO1, are correctly used as theorem names under CT21 and as a test ID). Numbers otherwise agree across files.

The remaining fix is on the one-page core, in the evidence parenthesis that was filled after S5. `CORE.md` §4 folds the 24 wide-search real-pole worlds — still on the pre-#116 solver — into "0 of 144 further OU worlds here," without the caveat the note, S5 writeup, and OPEN_WORK already make. No merged document on `a1a98aa` relies on those 24 worlds. Fix that sentence before a CORE PR merges.

## Original blockers (B1–B3) — still fixed

**B1. CT41 kill rule — FIXED**, as the confirm review found, and unchanged since. `CORE.md` §3 and §6 use the merged wording, identically: a non-move is consistent only if g < Δ_R(k_lo); a miss if g > max(the static band, Δ_R(k_hi)); INDETERMINATE between; and if the predicted gap of a non-mover is ≤ Δ_R(k_hi), the move test is NOT A TEST (CT41). This matches CLAIM_MAP CT41 on `a1a98aa` (the map says "consistent if" rather than "consistent only if"; with the miss and INDETERMINATE clauses present, the two are equivalent).

**B2. Pair-rule rescue — FIXED**, unchanged. The formula is scoped to Model S given a numerical convexity premise, and is **false** for rhythms with first-order real stores. A pair rule would predict even K* (0, 2 or 4 in the worked example); the independently confirmed argmin is 3. "Counted by degree" remains the CT21 convention for a mode, not a block-count rule.

**B3. Hull increment is definitional, not a predictive rule — FIXED.** `CORE.md` §4, `KEYSTONE_NOTE.md` §4, and OPEN_WORK W9 / T18 now say, without calling this a candidate rule or citing 189/189 as support for one:

- The predictive keystone is proved or numerically supported only in Model S, and there only given convexity, which remains unproved.
- For rhythms, the only general statement is definitional: K* is argmin_K [K + R(1+ε_K)], which always coincides with the lower-convex-hull increment test on the measured ε_K curve, including K = 0. That is not a new rule, and it is not a prediction from the world's time scales alone.
- A predictive rhythm rule (K* from the poles and the stakes, without first computing the whole ε_K curve) is **OPEN**.

`KEYSTONE_NOTE.md` §4 now includes the short identity proof the confirm review supplied, correctly framed, and reports 189/189 and 2,000/2,000 as what the identity requires, not as evidence for a new rule. The empirical findings that should stay are still there and check out (see Numbers, below).

## Remaining fix (do this before a CORE PR merges)

**CORE.md §4 evidence parenthesis over-aggregates the 24 old-solver worlds.**

The sentence is: convexity "held in every non-buggy world checked (39/40 in the #116 review; 0 of 144 further OU worlds here)."

120 + 24 = 144. The 120 are the S5 worlds, now rerun with the merged #116 solver (120/120 convex; I reproduced this). The 24 are the real-pole worlds from `convexity_wide.py` (classes A clustered OU, D smooth/low-pass, E large variance contrast). `KEYSTONE_NOTE.md` §1, `S5_RESULTS.md`, and OPEN_WORK W9 already say those 24 "still rest on the older solver" and were not part of S5. The core page does not.

Two further caveats the core page also omits, and that the note's "older solver" line only partly covers:

- `convexity_wide.py` still uses `np.minimum.accumulate` on the E_K sequence and sets E_∞ = min(YJ, E_J). That is the pre-#116 path, not only a missing Jacobi-scaled inverse.
- Class D is an OU mode through a low-pass, with a negative residue in the partial-fraction expansion, not a plain sum of OU modes. Calling all 24 (and therefore the 144) "OU worlds" / Model S is slightly loose. Wide-search seed 24 (class E) also recorded ε = [0, 0, 0, 0] and was counted as no violation.

The 39/40 + "0 of 144" pairing is also awkward: 39/40 is a success count (the 40th was the optimizer bug, not a counterexample), while "0 of 144" is a failure count, and can be misread as "held in 0 of 144."

**No merged document on `a1a98aa` relies on these 24 worlds.** I searched the tracked tree (`git grep`) for `convexity_wide`, "24 further", "24 real-pole", "144 further", and "0 of 144": no hits. `theory/HT_INDEX.md` cites the #116 review (39/40) and `face_collapse_v23.py` V2 (300 worlds), not this wide search.

Suggested replacement for the parenthesis, so the one-page core matches the note: cite the #116 review (39/40; the 40th was the optimizer bug) and the S5 rerun (120/120 with the merged solver, convexity still unproved). If the 24 are mentioned at all, say they still rest on the older solver and do not call class D a plain OU world.

## S5 rerun (nice 19) — reproduced

I ran `nice -n 19 python3 s5_rerun.py` from `core/keystone_checks/` against the merged solver at `theory/layers_checks/stores.py`. Wall time 122.2 s (6 workers; documented previous run 126.7 s / 753 s worker time; my worker time 719 s). The script overwrites `s5_rerun.json`; scientific fields are identical to those quoted in `S5_RESULTS.md`. `s5_rerun.out` was left as the previous 126.7 s log (I did not tee).

From the new JSON, all documented headlines match:

| Check | Documented | This rerun |
|---|---|---|
| Completed, all finite | 120 / 120 (50 J=3, 70 J=4) | 120 / 120 |
| Convex ε_K on K = 1..J at 10⁻⁴ and at 10⁻⁶ | 120 / 120 | 120 / 120 |
| Convex on K = 0..J at 10⁻⁴ | 120 / 120 | 120 / 120 |
| E_K below E_∞; increasing E_K | 0; 0 | 0; 0 |
| N60 = argmin, excluding the K* = 0 hole | 18,941 / 18,941 | 18,941 / 18,941 |
| K* = 0 hole | 379 / 19,320 in 39 worlds, R ≤ 1.41 | 379 / 19,320 in 39 worlds, R ∈ [0.10, 1.4125] |
| Genuine mismatches | 0 | 0 |
| ε₂/ε₁ (41 three-mode worlds with ε₁ > 10⁻³) | 6.6×10⁻⁶ to 0.3147, closest seed 100 | 6.648×10⁻⁶ to 0.314746, seed 100 |
| E_J − E_∞ | median 8.5×10⁻⁸, max 2.4×10⁻⁶; ε_J ≤ 8.9×10⁻⁷ | median 8.51×10⁻⁸, max 2.37×10⁻⁶; ε_J max 8.89×10⁻⁷ |
| Closest decrement increase on K = 1..J | −9.8×10⁻⁸, seed 62 tail | −9.84×10⁻⁸, seed 62 |
| Largest 1/(ε₀ − ε₁) | ~1.55, seed 0 | 1.551, seed 0 |
| 430 K-fits | all Nelder–Mead | all 430 Nelder–Mead |

Seed 24 (the world the old solver had overflowed to NaNs) is clean and convex, and matches the writeup to the reported digits: τ ≈ 4.205, 32.45, 368.7, 24791; v ≈ 0.0423, 14.43, 8.651, 3.503; N ≈ 0.04941; (E₀,…,E₄) ≈ (26.625, 0.216119, 0.216002, 0.215994, 0.215994); E_∞ ≈ 0.21599387; ε_{1..4} ≈ (5.81×10⁻⁴, 3.76×10⁻⁵, 1.23×10⁻⁶, 6.08×10⁻⁸). Seed 100 matches the reported τ, v, N, and ratio.

Convexity remains numerical only, unproved. The writeup says so, and does not treat the 18,941 matches as further evidence for convexity (they are what the count formula does once convexity is granted). That is the honest status.

## Numbers otherwise consistent; rhythm counts recounted

Independently recounted from `rhythm_rule.json` (21 worlds × 9 values of R = 189):

- 11 convex, 10 non-convex (all light or medium 2- and 3-oscillator worlds).
- N60 raw = argmin in 170/189. Of 19 misses, 2 are the K* = 0 hole (convex one-oscillator worlds `1osc_z0.25_N0.2` and `1osc_z1.0_N0.2` at R = 0.5); 17 are genuine, all in non-convex worlds (17/90). On convex worlds with argmin ≥ 1: 97/97.
- Even/pair matches 66/189; degree-pairs cap matches 53/189.
- Odd K* in 123/189; K* ∈ {3, 5} in 15.
- Worked example: E_∞ = 0.03788281801526715; (E₁,…,E₄) = (0.08051946, 0.07373616, 0.05183293, 0.043288); at R = 3, J = (7.376, 7.839, **7.105**, 7.428), argmin 3, N60 2, even/pair 4. At R = 50 and 100 the argmin is 6, not 4. `KEYSTONE_NOTE.md` §2 now uses these later figures (ε₄ = 0.1427, J₄ = 7.428), so the confirm review's §2 vs §4 inconsistency is gone.
- One lightly damped oscillator: `1osc_z0.02_N0.04` has K* = 3 at R = 20, then 4; `1osc_z0.02_N0.2` has K* = 3 at R = 5, then 4.
- Three light oscillators end at E₈ = 0.0626 vs E_∞ = 0.0554.

These match `KEYSTONE_NOTE.md` §4, OPEN_WORK W9 / T18, and the confirm review's recount. The confirm review's leftover J₄ typo is fixed. Adversarial climb figures (0.4625 / independent 0.461) are unchanged and still below 0.5. Field scorecard 30 NOT A TEST (10 proxy-passed, 20 proxy-failed) matches the v2.68 tally (10 + 18 + 2). Headers agree on `a1a98aa`, v2.66 / v2.67 / v2.68, and the 318 / 118 counts. Plug-in vs pole count "only at R ≤ 10³" matches `theory/HT_INDEX.md` on `a1a98aa`.

## IDs and the "law" wording rule

Hypothesis sentence is exact and unique on the core page: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." No "theory of everything," no "bill," no joules. In the four files under review, "law" appears only in that sentence and in OPEN_WORK C3 (the pending "Proposed law" label, quoting the same sentence). That C3 use remains appropriate for a work list. The confirm review's "a candidate, not a law" clause on the core page is gone.

Every CLAIM_MAP-style ID cited in `CORE.md`, `KEYSTONE_NOTE.md`, `S5_RESULTS.md`, and `OPEN_WORK.md` exists in `measurement/CLAIM_MAP_v2.md` v2.68, with a matching status and a label that fits the use:

- Load-bearing rows cited on the core page (N46, N58–N61, N63, N60, CT20–CT23, CT25, CT28, CT33–CT43, CT14, CT16, CL18, CL19, CX7, J16, and the operational gate as THEORY §3 / FRAMEWORK §9) match their map labels. N46's "Fractal, period" shorthand is the withdrawn framing already used in THEORY.md ("the theory does not say physical time is fractal"). CT28/CT34 plus "worth falling as e^{−2ℓ/τ}" at equal read quality is the OU nesting line in THEORY.md. N60 is listed among proved-in-model theorems only as "conditional on convexity, in Model S," which matches "**PROVED (in-model)** given convexity (numerical)."
- Alias rows are real rows: CT14 → B2, CL13 → F1, CL11 → K17 (OPEN_WORK T12). L1–L3 are not separate map rows; they are named in CT21 ("Layers L1–L3") and N60. The note correctly cites CT21, not L1, for the K* = 0 hole, and flags LAYERS.md's Theorem L1 ("K* = 1 for every w and h") as the overstatement. EVO1 is a test ID (PR #114, not yet on `main`), not a map row.

## Other checks that still pass

- Master equation, ruin as a cap, Landauer as a floor, "one currency," operational "strongly selected," and "predicts only through price-free structure or independently measured prices" are unchanged.
- CT20/CT33 ruin-slack qualifier, CT40's "with redesign per regime," records-as-agents (N63 OPEN; first #116 numbers withdrawn), and the ht-index demotion (N58, N59; N61 math-corrected; does not count layers) remain as previous reviews passed them.
- I did not produce a convexity proof and did not search for a new Model S counterexample beyond rerunning S5.
- I did not re-run the full pytest suite, only `--collect-only` on `tools/` (118 tests).

## Non-blocking nits

- `CORE.md`'s header still says last revised after B3 about 5:25 PM ET; the 144 figure and the S5 results were filled later (the note and OPEN_WORK headers correctly say about 5:31 PM ET). Update the stamp when the 144 sentence is fixed.
- `rhythm_rule.json`'s `note` field still says "Candidate only, not a law." That is a stale pre-B3 label in a data file, not in the reviewed prose.
- OPEN_WORK S5 is correctly marked DONE; convexity itself stays with W9, unproved. S-plan's owed re-confirm is this document.

## What would make this READY

In `CORE.md` §4, stop folding the 24 old-solver wide-search worlds into "0 of 144 further OU worlds." Cite the cleaned S5 120/120 (and the #116 39/40) as the numerical support, with convexity still unproved. If the 24 are mentioned, keep the older-solver caveat already in the note. Then this can be the one-page core.
