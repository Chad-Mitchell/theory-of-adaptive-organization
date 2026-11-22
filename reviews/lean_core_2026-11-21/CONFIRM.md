# Blind confirm: PR #147 at 6d9af6a

**Confirmer:** independent. Wrote none of the PR, the `formal/lean/` library, `tools/check_lean.sh`, the OPEN_WORK T19 edit, the fix commit, or `REVIEW.md`.
**Date:** Sunday 22 November 2026.
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/147
**Head confirmed:** `6d9af6af9d6583f6f000d6df2f49435419c90d36` on `lean-core-2026-11-21`. Parent `dc5ee743d4bc9753fbfa5928ee7486f4f9e26e89` (the review). Base `c92886af97425102878241740b093983885a0106` (`main`; `origin/main` matches that SHA). Draft. This confirm does not merge.

**Verdict: READY**

No blocker. `REVIEW.md` (head `40e99ea`, verdict READY-WITH-FIXES) required two documentation fixes before the mapping table could be treated as the claim. `6d9af6a` applies both. That commit edits comments and prose only. The new Lean statements are unchanged. T19 stays **PARTIAL**. The Part 2 hypothesis sentence is byte-identical to `c92886a`. Locked paths are absent from the diff.

Three section-pointer nits remain. They are listed at the end. They do not put a proved row on the wrong section, and they do not call the hypothesis proved.

---

## Should-fix 1 — resolved

`REVIEW.md` item 1: the quadratic excess was sourced to “CORE §3, THEORY §4”. Current CORE §3 (`CORE.md:44-56`) is the layer lifetime `T* = √(6k/(wσ²))`. It does not state `E[J] − J* = d/(2β)`.

`6d9af6a` retargets every `d/(2β)` citation to CORE §8:

- `formal/lean/GTAO/Equipartition.lean:4` — `(CORE §8, THEORY §4: E[J] - J* = d/(2β))`
- `formal/lean/GTAO/Equipartition.lean:19` — SA1b / Corollary SA1c `(CORE §8, THEORY §4)`
- `formal/lean/README.md:97` — `SA1b / Corollary SA1c, d/(2β); CORE §8, THEORY §4`

CORE §8 (`CORE.md:98-100`) is the selection-excess note. It names the excess `d/(2β)`, the premises A1, A2-L, `Nμ ≪ 1`, and SA1–SA1b, and it points at `theory/SELECTION_AXIOMS.md`. THEORY §4 (`THEORY.md:71`) points at that note’s excess formula. SA1b remains the statement of the identity; §8 and §4 are the pointers the review asked for. A search of `formal/lean/` for `CORE §3` now hits only the layer-lifetime header and the three lifetime rows (`LayerLifetime.lean:3`, `formal/lean/README.md:85`, `:86`, `:88`). Those match CORE §3.

## Should-fix 2 — resolved

`REVIEW.md` item 2: the not-formalized list and T19 called the hypothesis “the hypothesis in CORE §3”. In the current one-page `CORE.md` the hypothesis sentence is line 9, above any numbered section:

`**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**`

`6d9af6a` drops `CORE §3` from every hypothesis pointer:

- `formal/lean/README.md:11-12` — “the hypothesis at the top of CORE.md”
- `formal/lean/README.md:105` — the same phrase, in “What is not formalized”
- `OPEN_WORK.md` T19 — “the hypothesis at the top of CORE.md (a claim about the real world)”

T19 contains no `CORE §` citation. It stays **PARTIAL**. The extension is still described as a draft that is not merged. Nothing in the Lean sources, the README, or T19 says the Part 2 hypothesis is proved.

---

## Other CORE section citations

Every `CORE §` under `formal/lean/`, plus the T19 row:

| Location | Cited as | Current `CORE.md` | Judgment |
|---|---|---|---|
| `GTAO/Cost.lean:16` | `CORE.md` §1, the cost `J` | §1 “The cost” (`:13-24`) is that equation | Right |
| `README.md:62` | `FiniteDesignMenu.J`, CORE §1 | Same | Right |
| `GTAO/LayerLifetime.lean:3`, `README.md:85-86`, `:88` | CORE §3, `T*` and `√k` scaling | §3 (`:44-56`) states `T* = √(6k/(wσ²))` and the square-root dependence on re-forming cost | Right |
| `README.md:97`, `Equipartition.lean:4`, `:19` | CORE §8 for `d/(2β)` | §8 (`:100`) | Right, after `6d9af6a` |
| `GTAO/LocalShared.lean:3` | CORE §1 and §4 | §4 (`:58-60`) is local vs shared. §1 does not state the D5 condition | §4 right; §1 wrong (nit 3, unfixed) |
| `README.md:90` | `localCost`, CORE §1/§4 | Same split | §4 right; §1 wrong (nit 3, unfixed) |
| `README.md:93` | `switch_iff`, CORE §1 plus “needs delay on the shared channel only, and a shared lump cheaper than `N` local ones” | That quotation is the unnumbered lead, `CORE.md:11`. §4 (`:60`) uses “latency” and “lumps” | Section number wrong (nit 3, unfixed). LAYER_LIFETIME §5, also cited on the neighbouring rows, is the accurate source |
| `README.md:106`, `GTAO/Hull.lean:26` | Model S convexity of `ε_K` is unproved (CORE §4) | §4 is local vs shared and does not mention `ε_K`. The numerical caveat is the unnumbered status block, `CORE.md:113` (“Convexity inside Model S is numerical (120/120), not proved”), and it does not name `ε_K` | Stale. At `87ec006`, when `Hull.lean` was written, CORE §4 was “The keystone candidate” and did state this. `KEYSTONE_NOTE` §1, also cited on the README bullet, is the current statement |

`Hull.lean` is not in `c92886a..6d9af6a`. The README convexity bullet is the pre-existing line; `6d9af6a` did not edit it.

---

## `6d9af6a` changes comments and docs only

`git show --numstat 6d9af6a`:

| File | Insertions | Deletions |
|---|---|---|
| `OPEN_WORK.md` | 1 | 1 |
| `formal/lean/README.md` | 3 | 3 |
| `formal/lean/GTAO/Equipartition.lean` | 2 | 2 |

The two Lean lines are inside the file header comment and the module doc comment (`CORE §3` → `CORE §8`). Stripping block comments and `--` line comments, `Equipartition.lean` at `6d9af6a` equals the same file at `dc5ee74`. No declaration, theorem, proof, import, or tactic changes.

---

## Part 2 sentence and locked files

The four maintained copies are byte-identical to `c92886a`, one occurrence each, bold markers included:

- `THEORY.md`
- `CORE.md`
- `README.md`
- `theory/SELECTION_AXIOMS.md`

`git diff --name-only c92886a..6d9af6a` is:

`OPEN_WORK.md`, `formal/lean/GTAO.lean`, `formal/lean/GTAO/Equipartition.lean`, `formal/lean/GTAO/HullWalk.lean`, `formal/lean/GTAO/LayerLifetime.lean`, `formal/lean/GTAO/LocalShared.lean`, `formal/lean/README.md`, `formal/lean/scripts/AxiomAudit.lean`, `reviews/lean_core_2026-11-21/REVIEW.md`, `tools/check_lean.sh`.

No path under `tests/` or `prereg/`. No `PREREG`, `PREDICTIONS`, `LOCK`, or `.sha256` file. `CORE.md`, `THEORY.md`, `STATUS.md`, `README.md`, `core/KEYSTONE_NOTE.md`, and `theory/SELECTION_AXIOMS.md` are absent.

---

## Commands

Run from the repo root on `6d9af6a`, at `nice -n 19`, after `git fetch origin main` (`origin/main` = `c92886a`). This environment had no Lean toolchain and no pytest. elan was installed with default toolchain `leanprover/lean4:v4.37.0-rc1` (the pin in `formal/lean/lean-toolchain`). pytest, sympy, pandas, and scipy were installed for the suite and were not added to the repo.

| Command | Result |
|---|---|
| `nice -n 19 tools/check_lean.sh` | exit 0. Mathlib fetched at `31ce06eaadf4a200c0e1407c5f10953cf606b8f8`. `lake build`: 5835 jobs, “Build completed successfully”. `AxiomAudit: OK (312 GTAO declarations; only propext, Classical.choice, Quot.sound)`. `check_lean.sh: OK`. About 56 s after the toolchain download. |
| `python3 tools/check_fresh.py` | exit 0. `STATUS.md` main is `2eeab30`; window `c92886a 2eeab30 c04cedd d34df95 a97887e`. `RESULT: PASS`. |
| `python3 tools/check_consistency.py` | exit 0. 0 wording FAILs, 0 process-rule FAILs, 0 core-rule FAILs. Soft length WARNs only (THEORY main text 10569 words, README 1468). `RESULT: PASS`. |
| `python3 tools/check_open_work.py` | exit 0. 0 missing IDs. `RESULT: PASS`. |
| `nice -n 19 python3 -m pytest -q tools` | **176 passed** in 261 s. `test_lean.py` re-ran `check_lean.sh` on the warm tree as part of the suite. |

---

## Remaining issues

These do not block.

1. **Review nit 3, unfixed.** `GTAO/LocalShared.lean:3` and `formal/lean/README.md:90` still tag the D5 costs “CORE §1” as well as §4. `README.md:93` attributes the lead sentence “needs delay on the shared channel only, and a shared lump cheaper than `N` local ones” to CORE §1. That sentence is `CORE.md:11`. Section 1 is the cost. Section 4 has the same claim in the words “latency” and “lumps”. The proved comparison is the one LAYER_LIFETIME §5 states, and the README rows already cite that note.

2. **Stale CORE §4 on Model S convexity.** `formal/lean/README.md:106` and `GTAO/Hull.lean:26` still say convexity of `ε_K` in Model S is unproved at CORE §4. Current §4 is local vs shared. The claim lives in `core/KEYSTONE_NOTE.md` §1, which the README bullet also cites. `Hull.lean` predates the one-page CORE and is outside this diff. The proved D5 rows that say CORE §4 match §4.

3. **Review nit 4, unfixed.** `GTAO/HullWalk.lean:28-30` says a vertex list for every finite point set “is standard and is not formalized here.” `greedy_isLowerHull` and `hull_increment_test_eq_argmin` formalize it. The README row is the accurate one. `6d9af6a` does not touch this file.

T19’s extension clause still says the draft has had “no independent review yet”. `reviews/lean_core_2026-11-21/REVIEW.md` is that review and is already on the branch. The clause is a dated status lag. T19 remains **PARTIAL**.

---

## Conclusion

READY. The two should-fixes are in `6d9af6a`, and that commit does not change Lean code. `d/(2β)` is cited to CORE §8, where the selection excess is stated. The hypothesis is cited to the sentence at the top of `CORE.md`, and it is no longer called CORE §3. The lifetime rows that say CORE §3 match §3. The build, the axiom audit, and the repo checkers pass. The Part 2 sentence and the locked files match `c92886a`. The three leftovers above are nits. This confirm does not merge the draft.
