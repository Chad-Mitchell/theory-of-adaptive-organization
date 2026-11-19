# NARRATIVE: does the README make the idea click, and how should GTAO be told?

Wednesday 18 November 2026, late evening ET (America/New_York). Grok Bot executor for Chad Mitchell, via Ace (pt1957u). Not independent. The README rewrite described here is applied in the same PR; the old README is recoverable with `git show 601344e:README.md`.

## 1. Diagnosis of the old README (at 601344e)

**Measured, not guessed.** The first screen (title to "Start here") was five paragraphs and about 900 words. They opened five different ways: "In one breath", "The spine", "One sentence on viruses", "The claim is…", and "Working repository for…". The reader met eleven hedges ("proved only inside the model", "untested, not refuted", "not a theory of everything", "the author's scope choice", "an open disagreement", "known mathematics", and others) before meeting one thing the theory *says*. The first concrete implication came at line 27. The second paragraph a newcomer read was about viruses, the one result the repo itself labels a restatement of published work.

**What each cold reader would have done:**
- **Physicist.** Sees "second law", "black holes" and "cosmic horizon" in the first screen and expects physics. Finds classifications given published physics, and a note that the second-law framing is "decorative" in the proofs (THEORY §2.3, night-1 review). Likely reaction: "physics vocabulary on a decision model." The fix is to say early and plainly that GTAO adds no new physics and that the ends of the scale are *classifications*, then let §2.3's honest split (literal floors at the cell, not binding above it) earn trust.
- **Biologist.** Recognizes Mora & Nemenman, Lee–Flack–Krakauer, Forterre and Eigen, and will judge the project on how honestly it credits them. The old README credited them well, but halfway down the page. The virus paragraph near the top reads as "they rediscovered the virocell", which costs credibility up front.
- **Organization theorist or economist.** Recognizes Marschak & Radner, Simon, Hayek and EOQ, and asks one question: what is here beyond team theory and inventory pooling? The old README's answer, "the open bet across scales", was in paragraph 4 of "In plain words", after the spectrum bullets.
- **Curious generalist.** Never reaches the idea. The clearest statement of it in the whole repo, *keep / burn / know* (`theory/BOOKENDS.md` §1), is not linked from the first screen.

**The deeper problem, said plainly.** Chad asked whether the README makes "the profound, verifiable profoundness" click. Right now no single claim is both profound and verified:
- The **profound** parts (the spine; keep / burn / know; black holes as the frozen extreme; "alive" as a ledger) are framings and classifications. BOOKENDS says so itself: "no data could fail them."
- The **verifiable** parts (the design exponents, the formal layer) are proved in-model, and most of the mathematics is classical.
- The part that is **both profound and testable** is the bet: the same relations, with inputs measured on each system, hold from cells to cities. That bet is untested.

So the honest goal for the README is not to make a verified result click. It is to make **the frame** click in thirty seconds and **the bet** click in two minutes, and to show the reader exactly how the bet could die. Overselling the frame as a finding would be the one mistake that kills the project's credibility with every expert reader above. Ace's past framing ("the virus redefines life", "the theory has importance for cosmology") pushed in that direction; the repo's own labels pushed back, and the labels are right.

## 2. Recommended arc (for the README, a post, a talk, or the video when it resumes)

1. **The hook.** "An atom never has to guess. A cell always does. Why?" (adapted from the opening line already written in `theory/SCALE_ENDS_SUMMARY_FOR_CHAD.md`).
2. **Keep / burn / know.** Three ways to last under the second law. Only the third needs a model, and only once acting late is costly. That is judgment.
3. **The bill.** Holding memory, being wrong or late, and reads. The currency changes; the bill does not.
4. **Four consequences.** How often to look (set by the world's spectrum); when to share a model (levels); who must be in charge (shared fate or enforcement); how big one tracker can be (light delay, so federation).
5. **The bet and how it dies.** Measured inputs, the same relations at every scale, two systems to kill it, and a named rival.
6. **Credit up front.** Most of the math is known (Kalman, EOQ, team theory). Saying so early is a strength: it tells experts the authors know the field.
7. **The evidence, honestly.** No valid field test yet. The τ tests failed on proxies. Everything is labelled.
8. **The invitation.** "Here is the first test anyone with the right data can run" (SAME-SYSTEM-AQN; the attention test in `LOOSE_ENDS.md` L1).

The ends of the scale (atoms, black holes, the horizon) belong in step 2 as *placements*, not as headline results. Viruses, the cosmic web, wormholes and the torus belong in a "Reach" section after the bet.

## 3. The README rewrite (applied)

| Old (601344e) | New |
|---|---|
| Five openings, ≈ 900 words of mixed claim and caveat before "Start here" | One bold sentence with the idea, then one sentence of status: proved in-model, much of it known, untested, not refuted, not a law, not a theory of everything |
| Spine as a dense paragraph | "The idea in one table": keep / burn / know, with what each pays, whether a model pays, examples, and the CLAIM_MAP status inline |
| Implications scattered across "In plain words", "The ends of the scale" and "Two corrections" | "What the bill implies, inside the model": five bullets, each with its status in brackets |
| Kill conditions only in THEORY §1 and §9 | "The bet, and how it dies": the bet plus three kill conditions on the first two screens |
| Prior art in two lists further down | "What is new, and what is not": one table by layer (frame, design exponents, Regime C, formal layer, ends of the scale, internal-model bound, the bet) |
| Virus sentence in paragraph 2 | Moved to "Reach", labelled a restatement with a common ledger |
| No reading guide | "Start here" with reading paths for a physicist, a biologist, an organization theorist, a generalist and a skeptic |
| "Update, 18 Nov 2026 (v1.4.22)" status heading | "Honest status, in detail", undated; adds the caveat that no review has covered the whole theory, and no human expert has read it |
| v1.0 "What still looks new" list in the main flow | Kept verbatim inside a collapsed `<details>` block, marked as history |
| Scoreboard, layout, applications, how to read, license | Kept; C3b's power-gate status added; scoreboard dates corrected to 13–15 Nov |

**Nothing true was dropped.** A token check compared old and new: every author–year citation, every CLAIM_MAP id and every number in the old README is still present. The removed pieces are the stale version heading and some duplicated sentences. The README is longer (175 lines against 133) because the reading paths and tables were added; the first screen is shorter and leads with the idea.

## 4. Other recommendations (not applied here; each needs its own review)

- **Split THEORY.md at v1.5.** It is 192 KB in 563 lines; single lines reach 25 KB (the §2.2 premise bullets). Nobody reads that cold. Keep THEORY.md to the claims, statuses, regimes and kill conditions (about 15 pages), and move premise bullets and test-design detail into `theory/` notes cited by section. That is a structural change, so it should get an independent review.
- **One canonical spine.** The spine and scope paragraphs exist by hand in README, THEORY (status block, §0, §2.3), BRIEF, BOOKENDS and REACH (LOCK_AUDIT S18). Keep one in THEORY §0 and link to it, or let the checker compare the copies.
- **Rename THEORY §1 rows to C1–C7** at v1.5, so "N6" means one thing (LOCK_AUDIT N3).
- **Lead public posts with the bet and the invitation, not with reach.** Black holes and viruses draw attention, but an expert reader judges the project on whether it says how it could be wrong.
