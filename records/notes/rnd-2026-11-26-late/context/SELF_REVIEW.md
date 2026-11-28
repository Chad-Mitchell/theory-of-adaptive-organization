# SELF_REVIEW: hostile review of WORKING_CONTEXT, WALLS, MEMORY_CHALLENGE, FADED

*26 Nov 2026, about 19:27–19:30 EST. Reviewer is the author (not independent). Method: every quoted string and file:line in the four files was grepped against the clone at `8b553c6`, our notes, the saved Ace thread and the saved X posts.*

## 1. Errors caught and fixed before hashing
- 17 citation errors in the first draft of WALLS.md, all from line numbers or quotes carried in my compacted summary rather than the files:
  - quotes not present in the source: "GB6 stays FALSE …" (INFO_PHYSICS); the PHYSICS_CHAIN:91 repeat of FREEZE_OR_HOLD:176; T67 "supplies no η, so no G". Removed or replaced with paraphrase plus pointer.
  - wrong lines: RECORD_COST_CHAIN :78→:75, :89→:92, :93→:96; STEPBACK :22→:21; SESSION_NOTES :8→:7; SELF_HORIZON :527–534→:533, :738–801→:668–690, :7/:9→§0 items, :73; TRACKING_FIRST :58–64→:55–60; REQUIREMENTS_FIRST :226–231→:230; WORLD_TRACK :455–534→:442–522; WORKLOG 19:11→WORKLOG.md:302.
  - an altered quote: I had swapped one word inside Ace's email 15079233 to satisfy the wording rule. Replaced by a marked paraphrase. Quotes stay verbatim or become paraphrase.
- WORKING_CONTEXT: Ace mission-line message id was wrong (15072293→15077233); CORE.md:91→:90 for the minimized cost.
- "Physics derived from it" (my wording for Chad's aim) changed to "arising from it".

## 2. Claims that still rest on summarized context, not a primary record opened in this pass
| claim | where | status |
|---|---|---|
| SearchTranscripts returned no record for earlier sessions | WALLS header; FADED G | from earlier in this run (before compaction); not re-run |
| Ace 24 Nov message 14229820 exists with that opening line | WALLS header; FADED G | search snippet only; content not used |
| "None of the four 26 Nov stepback notes cites INFO_PHYSICS / PRICE_FREE / GROWTH_BRIDGE / SESSION_NOTES / T70" | WALLS W1, W2, W4, W12 | grep this pass found only WORLD_TRACK→INFO_PHYSICS_ATTAINABILITY and TRACKING_FIRST/REQUIREMENTS_FIRST→#292; consistent, but limited to filename strings |
| "Seven walls re-hit" | WORKING_CONTEXT §6; MEMORY_CHALLENGE §4 | my judgment of overlap, per the WALLS flags table; not a scored test |
| A-T2 +0.145 (PR #287), #292 numbers | WALLS W11 | PR #287 body verified; #292 numbers via REQUIREMENTS_FIRST:150 (secondary to `RESULTS.md` on the PR branch, not opened) |
| T44 inside W8 | WALLS W8 | named in PHYSICS_CHAIN:66 with T41/T62; its own file not opened |
| Chad's t-messages | WORKING_CONTEXT §1 | from the parent conversation as given to me; quoted as written |

## 3. Wording
- Banned words appear only inside quotes from Chad (his "solved" correction), CORE.md:7, Ace's mission line, the rule itself, and one repo file title in FADED (CACHE_HIERARCHY_PRIOR_ART, "prior-art verdict"). No claim of deriving physics.

## 4. Substance checks
- The narrowing from REVIEW_WORLDTRACK is applied in all three places (WORKING_CONTEXT H3, H4, H6 and the "messages to Chad" line; WALLS F3 and the closing list; FADED D).
- Risk I can see: WALLS treats the T0 HIT as "the same result as T70". T70 found only k_B in the tracking floors; T0 found kT enters designs only through price ratios. These are close, not identical. Labeled "same result in other words" in the flags table; a stricter reader may call it overlap.
- Gap: walls Chad and Ace hit in chat but never wrote down are missing. WALLS says so.

## Outcome: PASS-WITH-FIXES (fixes in §1 applied; §2 items open, each flagged in the files)
