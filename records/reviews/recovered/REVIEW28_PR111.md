# Final independent check of PR #111 (head 3ce9751, branch v2.5-map)

Independent referee; I did not author any of it. Fresh clone `/workspace/gtao-review28` (checked out at 3ce9751; nothing pushed to the PR branch; `/workspace/looper` untouched; compute at nice 19). Written 20 Nov 2026, 12:20-12:55 PM ET. Prior reviews: `/workspace/gtao-review26/REVIEW.md` (NOT READY) and `REVIEW2.md` (READY-WITH-FIXES at dfe9d0b).

## Verdict: READY-WITH-FIXES

Every REVIEW2 must-fix and should-fix is genuinely resolved in text, code and all four PNGs. The map is correct: all 19 dots, their shapes and their solidity reproduce from the frozen inputs, and the per-system summaries match the dots. I found no false sentence in the four figures' claims. Two things block a merge as-is, and a few smaller things are worth fixing at the same time:

- `face_square.png` has its first footer line cut off at both edges (item 1).
- **`main` moved at 12:30 PM ET, after this head was cut.** PR #110 was merged (merge commit `e1be66e`). PR #111 now conflicts with main in `measurement/CLAIM_MAP_v2.md`, and several sentences still say "do not merge before PR #110" / "not yet merged" (item 2).

## Numbered items

### Must fix before merge
1. **`figures/face_square.png`: the first footer line is clipped on both sides.** It reads "U model, other things equal: fast scales go local, slow ones shared. If two layers are worth more together than apart, both can win outside the top-righ". The "O" of "OU" and the "t" and "." of "top-right." are cut off (dark pixels at the left and right image border; `face.png`, `face_all.png` and `face_collapse.png` have none). Cause: `figures/face.py:188`, `fig.text(0.5, 0.03, ...)` at 11.5 pt is wider than the 1200 px canvas. Fix: split it over two lines (as `face.py` already does for `face.png`) or shorten it; regenerate.
2. **Main moved; the PR no longer merges cleanly, and some text is stale.**
   - PR #110 merged into main at 12:30:50 PM ET (`e1be66e`, its commit title still says "do not merge"). A trial merge of 3ce9751 onto `e1be66e` conflicts in `measurement/CLAIM_MAP_v2.md` (3 hunks: the dated notes, which keep both sides, and the status tally block).
   - In a scratch merge (`/workspace/gtao-review28-merge`, not pushed) I kept both notes and set the tally to the rows' real counts: OPEN 77, PROVED 84, total 294. `check_consistency` then returns PASS, and `test_face_map.py`, `test_check_consistency.py` and `test_measured_ecoli.py` give 32 passed. A merge commit still has to be made by the author, followed by the full suite.
   - Stale wording to update at that point: `face_placements.md` lines 231, 254, 304 and 328 ("do not merge before PR #110", "which is not yet merged"); the comment at `face_systems.py:19`. Editing comments in `face_systems.py` changes its SHA, so re-freeze it (item 9) or put the wording only in the `.md`.

### Should fix
3. **Two leader lines in `face.png` cross other markers.** `FIX_MAIN` is empty, so the automatic label placement is used.
   - The "5b" label sits directly above the solid square 4c, and its leader runs through that square to reach the hollow square 5b below.
   - The "6c" label sits beside the diamond 6b. Its horizontal leader crosses the diamond to reach the lower square 6c, and the "6b" leader ends on the diamond's lower vertex, so the two lines form a "+" on the diamond.
   - In `face_square.png` the 6c/6b pair has the same crossing (5b is fine there).
   - The 1b/2a problem from REVIEW2 is gone (verified: 1b at X_S = 316, 2a at 89; it went away because 2a moved when ρ was reverted, not by a label change). Use `FIX_MAIN` offsets for 5b, 6b and 6c, as the square layout already does for 5b.
4. **`face_all.png`.**
   - Every panel's strip note "shared layer: stakes / upkeep < 10⁻³" is overstruck by the thick vertical axis line, so the "-3" is hard to read.
   - The "*" in "5 city*", "6 nation-state*" and "7 global economy*" is not explained on this figure (it is on `face.png` and `face_square.png`).
   - `face_placements.md:339` says "font ≥ 9", but the strip note is 8.1 pt and the E. coli tick labels 8.7 pt.
   - The exponent in the `face.png` footer formula (e^{−2 delay/time scale}) is about 8 px high at native size. It is legible only when zoomed.
5. **CT36 gloss is not equivalent to the stated condition.** `THEORY.md:482` and `face_placements.md:70`: "the shared store is correlated with the local estimates' errors more than with the target" is given as what the positivity condition means. The condition itself (r_LS < 0 or r_LS > 2r_L r_S/(r_L²+r_S²)) is right: I checked it against `excess_fixed` on 123,268 valid random correlation triples, with no mismatch. The gloss is only an intuition. Example: r_L = r_S = 0.5, r_LS = 0.8. The shared estimate's correlation with the local estimate's noise (0.635) beats its correlation with the target (0.5), yet the excess is −0.22, so there is no value. Reword to "roughly", or state the condition without the gloss.
6. **Stale or inconsistent statements** (none changes a result):
   - `face_placements.md:221` says the ellipses are "1σ (main figure) or 2σ (face_all.png)". `face.png` draws no ellipses (`face()` calls `draw_map` with `ell_sigma = 0`).
   - README:27, THEORY:67 and `face.py:2` label the figure "v2.5.1", while the PR, CHANGELOG and THEORY:59 say v2.5.2.
   - CHANGELOG v2.5.2 is stamped "about 12:30 PM ET", but the commits are 12:17 PM and 12:20 PM ET.
7. **The three-scale greedy miss (seed 40) cannot be reproduced from the repo.** `face_placements.md:141-144` and THEORY:488 report it ("reproduced here with the guarded optimizer, 12 starts"), but the world's parameters are in no committed file or test. I reproduced it from review 26's world (`review_work/d_greedy_partial.jsonl`) with the PR's guarded `best_fast`, 12 starts. Costs: (2,3) 4280.549 and (3,2) 4281.731 match; (3,0) 4298.892 matches; (3,3) 4282.509 against 4282.459, which is start-dependent and not cited. Commit the world as a regression case next to counterexamples A and B.
8. **Per-system layer counts on `face.png` are centre-design counts without a caveat.** 9 of 19 dots are hollow, and the key says nothing about it (`face_all` titles do: "(1 hollow)"). Optional: append "(n hollow)" to the key as `reading()` already can.

### Note (no change needed to merge, but record it)
9. **Freeze point.** The freeze is a SHA-256 plus a test inside the same unmerged PR. After merging, record the merge commit as the freeze commit in `face_placements.md` §4 step 9. A comment-only edit changes the SHA (the test is strict), which is conservative.

## A. REVIEW2 must-fix / should-fix: status at 3ce9751
| REVIEW2 item | Status | Evidence |
|---|---|---|
| M1 hollow legend | **Resolved** | `face.py:128`: "hollow: no design wins ≥ 65% of its input draws" (`NEAR = 0.65`). On `face.png`, `face_square.png` and `face_all.png` (legend added). md §5 line 223 also says solid dots can change design. The 9 hollow dots are exactly those with max share < 0.65 (checked from `face_dots.json`). |
| M2 shading sentence | **Resolved** | "Outside the top-right, shading = cheapest design when two layers are worth no more together than apart (B.11)" on `face.png` (and in the same sense on the square and `face_all` legends); README:27 and THEORY:67 also limited. Checked against CT35: true outside the top-right under subadditivity, which the dots satisfy (all κ ≤ 1). |
| M3 ν gloss | **Resolved** | `face.png` footer: "ν = all local layers' upkeep / the shared layer's upkeep". Matches ν = n·h_l/h_c (`face_map.py`, `face_systems.py` nu = n/hc). |
| M4 1b/2a labels | **Resolved** | Dots separated (1b X_S 316, 2a X_S 89). Native-resolution crop: 1b leader to the hollow square, 2a leader to the solid diamond, in `face.png` and `face_square.png`. Residual label crossings are item 3. |
| M5 ant ρ reverted + disclosed | **Resolved** | `face_systems.py` patch ρ = (0.0, 0.3); the numeric inputs of the whole file are identical to v2.5 (`6966a2a`; only comments differ). Disclosure at md lines 272-276 and table row 235. I verified the figures it quotes from `dfe9d0b`'s `face_dots.json`: X_S 392 → 89, shares with ρ 0.3–0.9 both 70.5%, shared 27%, local 2%, and now both 70%, local 16%, shared 13%, none 2%. The false "not tuned afterward" is gone, replaced by "not preregistered until the freeze". |
| M6 CT36 sign + "necessary, not sufficient" | **Resolved** | THEORY:482, CLAIM_MAP CT36 row, `face_map.excess_fixed` docstring, md lines 65-72, all with the r_L, r_S ≥ 0 convention and the necessity argument (G_L(b*) ≤ G_L^opt etc.), which I re-derived: sound. The counterexample (−0.032) is stated. Gloss caveat: item 5. |
| S7a classify before merge | **Resolved** | md §4 step 3 ("Classify, then merge… never merged, however close, so 'both' stays observable"), step 6; THEORY:59 (4). |
| S7b pole-to-dot assignment | **Resolved** | md §4 step 7: τ range widened ×3 at each end, nearest centre in log τ, unmatched pole = miss. |
| S7c freeze | **Resolved** | SHA `00f6f25d…5377` equals `sha256sum figures/face_systems.py` and is in md §4; `test_inputs_frozen`. |
| S7d degree-1 only | **Resolved** | md §4 step 7; THEORY:59 (7); E. coli reported, not scored. |
| S8 conditioning guard + Lyapunov recheck | **Resolved** | `face_hybrid.py`: `GAP` (stores ≥ 1% apart via `_rates`), `COND_MAX = 1e10` with truncated `pinv` (checked: it can only understate the value, and the error it reports is exact for those weights), `confirm()` at 6-significant-digit rates with `max`. `test_conditioning_guard_review26_seed34`. Seed 34 now agrees between `mse_fast` and `mse`. |
| S9 one-stream scope | **Resolved** | THEORY:488 "Tested scope only", md lines 134-147, the `face_collapse.png` footer. Seed-40 numbers reproduced (item 7 for the gap). |
| S10 "of total cost" | **Resolved** | No "of value" left in THEORY, README, code, CLAIM_MAP (grep). |
| S11 E. coli inset | **Resolved** | White inset, no shading or edge; caption "proxy: motility benefit / signalling proteome share (not X_L; the map's edges do not apply)" on `face.png`, `face_square.png`, `face_all.png`. |
| S12 CT35 premises | **Resolved** | G_L, G_S > 0 and gains independent of stake and upkeep, in THEORY:480, md §1, `face_map.py` docstring; the priced-reading exception is stated. |
| S13 Grüter 2011 | **Resolved** | "2011 (online 2010)" in `face_systems.py` and the md table. Crossref: issued 20 Jul 2010 online. The only new DOIs in this diff (Grüter, Beckers) resolve; Horst 1941, Conger 1974 and Widrow 1975 rechecked on Crossref and match. |

## B. Every sentence on every figure, checked against THEORY B.11, CT35/CT36, `face_map.py`, `face_placements.md`
**`face.png` and `face_square.png`**
- "Each dot: one time scale of a system, at the centre of its input ranges": true. The centre is the log-midpoint of every range (ρ linear), n rounded (`face_place.coords`, u = 0.5).
- "Shading: which layer would pay on its own": true by definition (X_L > 1, X_S > 1). Quadrant labels match.
- "Shape: the cheapest design": true. I recomputed all 19 centres with my own code (closed-form G_L, G_S; G_B from the Lyapunov `best()` with a different seed and 8 starts; argmax rule). X_L, X_S, κ_L, κ_S and the design match `face_dots.json` for all 19, with 0 mismatches. All 19 have κ ≤ 1 (subadditive), so shading and shape agree outside the top-right, as the subtitle says.
- Footer: "Shared layer's stakes / upkeep = ν × pooling gain × e^(−2 delay/time scale) × local layer's stakes / upkeep (OU model, same read quality…)": true; it is X_S = ν·π·e^(−2ℓ/τ)·X_L, derived from the closed forms and checked.
- "So, other things equal, fast scales go local and slow ones shared": true as the ratio statement; the data follow it in every system (ops local, management both, strategy shared, and so on).
- "If two layers are worth more together than apart (e.g. a shared layer as a reference…), both can win outside the top-right": true by CT35 (only-if) and CT36. "No dot here has that in its model": true, `joint_share` = 0 for all 20 entries.
- "Survival is a separate gate", "* selection weak or unknown" (city, nation-state, global economy), "Layer = tracking store, not org-chart level": consistent with md §2-3 and the star flags in the data.
- Key lines "→ 1 local + 2 shared layers" etc., checked against the dots: immune innate local, adaptive shared, memory shared = 1 + 2 ✓; ant patch both, food supply shared = 1 + 2 ✓; team tasks and goals shared = 0 + 2 ✓; firm local, both, shared = 2 + 2 ✓; city local, shared, shared = 1 + 2 ✓; nation-state local, both, shared = 2 + 2 ✓; global economy local, both, shared = 2 + 2 ✓.
- Marker positions, shapes and solidity checked on the actual `face.png` pixels (axes transform): all 19 are at their coordinates, in the right colour; solid/hollow as the data say (4c's centre is covered by 5b's leader line, item 3). The four strip dots (1a, 5a, 6a, 7a) have X_S below 10⁻³ (innate 3.9×10⁻⁴, services 1.3×10⁻⁸, local 1.0×10⁻⁷, markets 3.8×10⁻¹¹⁹), so they belong in the strip; 4a (firm operations, X_S = 3.2×10⁻³) is correctly on the map.
- E. coli inset: log range −0.26 to 1.89, centre 6.5, caption true; it is explicitly not X_L.

**`face_all.png`**: panel titles' counts and "(n hollow)" match the dots (1, 0, 1, 1, 2, 2, 2). Legend and shading sentence true. Ellipses are 2σ log-space covariances of the 400 draws (as the title says). Issues: item 4 only.

**`face_collapse.png`** (checked against `face_collapse_v1.json`, `_v1b.json`, `_v23.json`, `face_subadd.json`)
- (b) "100% of 3000; κ ≤ 1 in all": agree = 1.0, max κ_L 0.99999999972, max κ_S 0.9897.
- (c) "both iff κ_L X_L > 1 and κ_S X_S > 1": checked on the data: in the 1665 upper-right worlds, 0 mismatches. Outside the upper right the quadrant equals brute force in 1335/1335. Legend counts (0, 553, 311, 801) match.
- (d) "κ > 1 in 119 of 1500; quadrant rule ≠ best design in 0": JSON `superadditive` 119, `quadrant_wrong` 0; legend counts 272/740/257/231 match `frac`. (The sample rarely sits near an edge, which the md says; counterexample A in the tests shows the flip can happen.)
- Footer: 99.8% (= 0.9975), 100.0%, worst regret 2.2×10⁻⁵ of total cost, "a 3-scale world defeats the look-ahead": all match the JSON and the seed-40 reproduction.

## C. Theory text
- Exact rule max(0, X_L−1, (X_S−1)/ν, (1+1/ν)(X_B−1)): re-derived by hand (an identity). CT35 if/only-if proofs: re-derived and sound (premises stated). CT36 formula, WLOG sign convention, the independent-given-target special case, and the necessity-at-optimized-rates argument: correct (formula vs `excess_fixed` on 123,268 random valid triples: no mismatch). One gloss: item 5.
- CT35 text, CLAIM_MAP rows CT35/CT36/CX6, THEORY B.11 and `face_map.py` docstrings agree with each other.

## D. Words
- **"law"**: the only use that names GTAO is the hypothesis sentence (THEORY:41, README:7: "The law of adaptive organization (hypothesis): …"). The other hits are other senses: "second law", "power-law", "stable-law", "has the law of λ^H X(t)", "growth law" (a bacterial-physiology comment in `face_systems.py`), CLAIM_MAP's withdrawn row J3, and CHANGELOG records. The added lines in the PR (diff against main) contain none that name GTAO. None of the four PNGs contains the word (the text is generated from the checked code). `tools/check_consistency.py`'s wording rule passes (0 wording FAILs).
- **"theory of everything"**: appears only as negations ("not a theory of everything") in `history/` and `reference/` (frozen records) and in the `measurement/FRAMEWORK.md` wording rule; nowhere in the PR's text or figures.

## E. Mechanical checks
- `python3 tools/check_consistency.py` on 3ce9751: **PASS** (FAIL 0, 21 INFO).
- `pytest -q tools` on 3ce9751: **84 passed** (5 min 50 s, nice 19; the two new tests `test_inputs_frozen` and `test_conditioning_guard_review26_seed34` pass).
- Regeneration in a clean worktree at 3ce9751 (`/workspace/gtao-review28-regen`): `face_place.py` (4 min), `face.py`, `face_collapse.py`, `face_table.py`. `face_dots.json`, `face.png`, `face_square.png`, `face_all.png` and `face_collapse.png` are **byte-identical** to the committed files (md5), and also to `/workspace/gtao-face/*.png`. The table produced no diff.
- Reruns of the check scripts (summary JSON compared to committed, excluding timings): `face_collapse_v1.py 3000` identical (summary and all worlds); `face_subadd.py 1500` identical summary; `face_collapse_v23.py 300 800` identical summary; `face_collapse_v1b.py 1500` identical summary.
- Merge trial against `e1be66e`: item 2.

## F. Legibility at native resolution
- `face.png` (1600×1000): all text legible (smallest: footer 11 pt ≈ 15 px; key lines ≈ 15 px; the exponent in the footer formula ≈ 8 px, item 4). Nothing clipped. The "firm … 2 local + 2 shared layers" key line ends about 5 px from the right edge.
- `face_square.png` (1200×1200): footer line 1 clipped (item 1); rest legible.
- `face_all.png` (2400×1440): legible; item 4.
- `face_collapse.png` (1260×1080): legible; the footnote fits to the edge with no clipping.

## G. Not done
- I did not re-verify the 18 DOIs beyond the new and 3 re-sampled ones (REVIEW2 checked all 18 earlier and none changed).
- Beckers' 47 min and Amanna's half-lives remain unchecked against full texts (the PR says so).
- I did not re-run the 3- to 4-scale greedy scan (92 worlds), only seed 40.
