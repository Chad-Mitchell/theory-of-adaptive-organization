# V141_REVIEW — independent review of PR #15 (THEORY.md v1.4 → v1.4.1; CLAIM_MAP v2.3 → v2.4)

Reviewer: Grok Bot executor `v141-review`, for Chad Mitchell via Ace. Sunday 15 November 2026, about 10:06–10:09 AM ET (America/New_York).
Object: branch `v141-fixes`, head `109529d` (base `b19d213` = origin/main at review time). Checked against the exact text of
`reviews/night2/V14_REVIEW.md` §3 and from first principles. The author's `V141_CHANGES.md` was **not** relied on.
Chad's rule (t1916): "be extra, extra sure before you do a full rewrite of the theory … tread carefully. Causal first principles."
Private. Nothing posted, sent or made public.

## Verdict

**Clean; merge.** Every edit to THEORY.md and CLAIM_MAP_v2.md traces to a V14_REVIEW §3 fix, word for word. Nothing else in either file changed
(71 changed word-diff lines, all accounted for below). No new unsupported claim, no invented citation. Four trivial issues were fixed on the branch
by this review (§6). Nothing substantive was found.

## 1. Fix-by-fix check against V14_REVIEW §3 (line-by-line diff of THEORY.md and CLAIM_MAP_v2.md)

| Fix | Applied text vs V14_REVIEW §3 | Result |
|---|---|---|
| 1 (N12 scope) | Not applied. Status block, "What changed" item 5, §2.5 bullet 2, §8b, §9 sink and CLAIM_MAP N12 byte-identical to main | Correct: N12 is under a separate referee (see §4) |
| 2 (J16, §0) | §0 sentence verbatim. CLAIM_MAP J16 note verbatim plus the review's own parenthetical rationale; status PRIOR ART → OPEN as the review says | Match |
| 3 (causal test) | N6 "How it dies" append verbatim; §9 new separate bullet verbatim, v1.4's first bullet kept | Match |
| 4 (credit) | N6 status append verbatim; §10 entries in the Filtering block, bibliographic data verbatim | Match (quote style normalised, §6) |
| 5 (Regime C) | §0 insertion verbatim at the stated place; N6 "The number" append verbatim | Match |
| 6 (two memory objects) | Paragraph verbatim, placed after "What this regime does not predict" and before Regime C | Match |
| 7 (MATCH1 A1) | Replacement verbatim | Match (", on that proxy" added, §6) |
| 8 (§1 intro, N4) | Both verbatim | Match |
| 9 (N7) | Clause verbatim ("shadow", as the review wrote; v1.3 had "mirror") | Match |
| 10 (opt., N3) | Sentence verbatim; identical to v1.3 (`120c309`) N3 | Match |
| 11 (opt., §2.3) | Replacement verbatim | Match |
| 12 (opt., §2.2) | Append verbatim | Match |
| 13 (changelog) | v1.4 moved below v1.3.1 as instructed, but the resulting list was still out of order (v1.2, v1.3.1, v1.4, v1.4.1, v1.3, v1.2.1, …), so the v1.4.1 entry's claim "chronological" was false | Fixed here (§6) |

Other changed lines: title and date line (v1.4.1), CLAIM_MAP version pointer v2.3 → v2.4, v1.4.1 changelog entry, CLAIM_MAP v2.4 note, counts
sentence and table, the J16 line in the CLAIM_MAP summary list, and ledger entry 20. All are bookkeeping for the fixes above. No other line moved.

## 2. Unsupported claims and citations

- DOIs resolved against Crossref this session: 10.1162/089976698300017403 → DeWeese & Zador, "Asymmetric Dynamics in Optimal Variance Adaptation",
  *Neural Computation* 10(5):1179–1202, 1998. 10.1016/j.neuron.2009.01.019 → Wark, Fairhall & Rieke, "Timescales of Inference in Visual Adaptation",
  *Neuron* 61(5):750–761, 2009. Both match the text. Lundstrom et al. 2008 (N6) and Anderson & Schooler 1991 (Fix 6) were already in §10.
- Fix 6's "power-law in the human information environments measured" is supported by §2.4 (COLLAPSE1/MATCH1 need hazards, 0.6–0.8) and labels the
  GTAO-specific form POST HOC, matching the existing §2.4 paragraph. Fix 5 repeats the "PROOF given those assumptions" status already in §2.2 Regime C.
- Fix 11's two factual pieces are supported in the repo: drift-invariant (e.g. per-nat) pricing gives a = b (`reviews/night1/formal/THEOREMS.md`
  Lemma 1(ix); R2 row a = b = ½), and §2.2's precision row already says any non-linear price exponent changes both elasticities.
- No "law" introduced (the only matches are "power law" and "second-law"). Field results stay "failed/passed on proxy"; vigilance stays **OPEN**
  (status block and §8c VIGIL_ONA).

## 3. Causal core and internal consistency

- Causal chain (§2.1, J15) unchanged. The fixes add back the comparative-statics (causal) kill in N6 and §9, which V14_REVIEW rightly said v1.4 had
  dropped; the equilibrium "sits near" kill is kept beside it. Note for preregs: "after its adjustment lag" must be fixed numerically in each locked
  test, or the causal kill can be escaped by waiting. Not a text defect; the prereg rules already require locked tests.
- J16 is OPEN in the J table; §0 says axiom-in-model, testable-in-world. No other file in the repo still calls J16 "not testable".
- CLAIM_MAP counts recomputed by script from the row tables: over the 167 v2 rows (excluding section N and G23–G29), OPEN = 43 and PRIOR ART = 19,
  matching the updated table; NOT EVIDENCE 13 and PROVED 41 also reproduce. Total 187 unchanged (a status move, no new row).
- §9 now has both the optimality sink and the causal sink; the §2.5 "formal exponent tracks the spectrum" sink is unchanged (Fix 1 pending).
- Regime C is back in §0 and N6 and is consistent with §2.2. "Two memory objects" is consistent with §3 rule 2 (keep rule) and §2.2's statement that
  need hazards are not kernels; Chad's power-law-need view now has an explicit home.

## 4. N12

Untouched in every location, as required. It is marked pending in the v1.4.1 changelog and the CLAIM_MAP v2.4 note, and §2.5 already says
"not refereed". **Open item (not fixed here, by instruction):** until the N12 referee lands, the canonical file still contains the overbroad
"the spectrum enters the formal layer only through constants", which V14_REVIEW §4 showed false (V ∝ N^a and mixed-technology e_u depend on α) and
which contradicts §6. The N12 referee's PR should apply Fix 1 (or its own narrower text) in all five locations.

## 5. Optional fixes 10–12

- **10 (N3 contrast): keep.** Restores v1.3's motivating sentence verbatim; it states the standard critical-slowing-down reading (Scheffer et al.
  2009, already in §4 and §10) and adds no claim.
- **11 (§2.3 physics): keep.** It is more accurate than v1.4's wording, not less: v1.4 implied the physics matters "only" for the onset exponent's
  class; in fact the price structure the physics imposes also sets the tracking layer's effort elasticities. It strengthens, honestly, the stated
  form of Chad's open disagreement without claiming it is settled, and both pieces are supported (§2). It does not depend on the N12 overclaim.
- **12 (framing line): keep.** It disclaims mathematical novelty and names the framing as the thing the bet tests; it adds no claim.

## 6. Trivial fixes made on the branch by this review

1. §13 changelog put in strict reverse-chronological order (v1.4.1 … v1.0); v1.4.1 entry updated to say so.
2. §10: the two new titles in double quotes, like the rest of §10.
3. Fix 7: "it failed as locked" → "it failed as locked, on that proxy" (standing rule: field results are "failed on proxy X"; the proxy is named in
   the same cell).
4. `queue/LEDGER.jsonl` entry 21 (maintenance): this review and the merge.
