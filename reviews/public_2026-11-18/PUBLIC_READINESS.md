# PUBLIC READINESS REVIEW (honesty and newcomer lens)

Reviewer: independent, skeptical, read-only. Wednesday 18 November 2026, evening ET (America/New_York).
Target: https://github.com/Chad-Mitchell/theory-of-adaptive-organization at main `abd56e5` (merge of PR #87; THEORY v1.4.21, CLAIM_MAP v2.41). Fresh clone in /tmp/rev-public (deleted after this report). Compute at nice 19. Nothing was posted, sent, edited or pushed.

## Verdict: READY-WITH-FIXES. No BLOCKERS found.

The repo is honest to a fault: no "law", no "theory of everything" outside negations, field results are "passed/failed on proxy", "untested, not refuted" appears on the first screen, and in-model proofs are labelled. Privacy scan is clean. Links are clean. Checker and tests pass. I recommend fixing SHOULD S1–S6 before midnight because each is a one-line edit. The rest can wait.

## Checks run
| Check | Result |
|---|---|
| `python3 tools/check_consistency.py` | RESULT: PASS (FAIL 0; 28 INFO hits in frozen records; 35 N rows, 170 N references, 0 mismatches) |
| `pytest tools/` | 50 passed |
| Link script over README, THEORY, BRIEF, STATUS, BOOKENDS, QUEUE (relative links plus backticked paths) | 0 broken from README, THEORY, BRIEF, BOOKENDS. STATUS.md:9 names three off-repo files (see N4). QUEUE.md:58 and :110 name two non-repo paths (see N4) |
| CLAIM_MAP status spot check (N7, N13, N16, N24–N35, J3, J6, J9, J16, K4, K12, K13, H2, H9, H11, H12, H17–H19, M2, G13, G15) | Every status quoted in README/THEORY/BRIEF/BOOKENDS matches CLAIM_MAP |
| Wording scan: "law", "theory of everything" in README, THEORY, BRIEF, STATUS, BOOKENDS | Every use is a negation ("not a law", "not a theory of everything"), the second law, a conservation law, or "power law"/"the world's law" (a statistical law of the process) |
| Withdrawn L^{2/3} | Every occurrence is marked withdrawn: README:71, THEORY:43/:141/:549, BOOKENDS:79/:306/:374, theory/THEOREMS.md:197 (struck through) |
| Privacy scan of 1,514 tracked files: emails, phones, keys/tokens, street addresses, abs paths, Nelnet/StudentAid/loans/finance, family names, health, Looper content | Clean. See "Privacy" below |
| X handle in README:3 | `@torusflow` matches the authenticated X account (read-only `get_users_me`) |

## BLOCKERS
None.

## SHOULD (fix before posting; each is a small edit)

**S1. README presents the physical-pricing scope as settled; THEORY says the disagreement is open, and the wording conflicts.**
- README.md:11: "The costs are physically priced from atoms to the cosmic horizon (Chad, 18 Nov 2026, t1927)" and "The physical floors are literal at every scale, but above the cell they do not bind".
- THEORY.md:126: "**Not literal above the cell.** kT ln 2 per bit does not bind for neurons, people or firms ... Above the cell the exponents come from information theory plus network transport costs, not from the second law."
- THEORY.md:128: "in the formal layer, the energy / second-law framing is **decorative**. No conserved quantity, entropy production or Landauer-type bound enters any proof".
- THEORY.md:129: "**Open disagreement, stated (Chad, t1908)** ... so this disagreement stays open" (N24 INCONCLUSIVE). BOOKENDS.md:404: "The t1908 disagreement (is the physics decorative?) stays OPEN."
- README.md:7 calls the second law "the backbone" with no hint that no proof uses it.
- Why it matters: a newcomer who opens THEORY §2.3 from the README finds "decorative" and "Not literal above the cell". They will read that as a hidden concession.
- Minimal fix: at README.md:11 replace "literal at every scale" with "literal as floors at every scale". After "(Chad, 18 Nov 2026, t1927)" add "a scope decision, not a finding; whether the physics does work in the proofs is an open disagreement (`THEORY.md` §2.3)". In README:7 add one clause: "the second law frames the theory; no proof in the formal layer depends on it".

**S2. The first screen leads with a superseded video, and "GTAO" is used before it is defined.**
- README.md:5: "Video: [an earlier draft explainer](video/gtao_v7.mp4), **superseded**; a new video is on hold".
- Pointing a new visitor at a video the repo itself calls superseded is the second thing they see. The fact-check (`video/FACTCHECK.md:3`) was run against v1.4.19, before the v1.4.20 narrowing of N26 and N28.
- README.md:7 and :11 use "GTAO" and README.md:15 defines it ("Working name: GTAO").
- Minimal fix: delete line 5 or move it under "Applications". Replace the title line with "# A Theory of Adaptive Organization (GTAO)". Whether to keep the mp4 in a public repo is Chad's call.

**S3. README has no plain "what/why/untested" lead.**
- README.md:7 is one ~190-word paragraph. It is good but dense, and the untested status first appears at README.md:9, the second paragraph of body text.
- Minimal fix (one added line above line 5, no rewrite): "**In one breath:** a theory of how anything that must stay matched to a changing world (a cell, an ant colony, a firm, a city) decides what to remember, what to check and what to let go. The math is proved only inside the model; whether real systems follow it is **untested, not refuted**."
- README.md:11 repeats the "not a theory of everything" and "(Chad, 18 Nov 2026, t1927)" material. The internal turn ids (t1927) are jargon on the first screen. Drop the id there; it stays in THEORY.

**S4. Stale "private" and "pending PR" text in files a newcomer is sent to.**
- BRIEF.md:3 (linked from README.md:19 "Start here"): "Private. Nothing was posted, sent or made public."
- BRIEF.md:93: "THEORY status block and §0 still read '15 November' and 'from cells to cities' for the empirical bet | Headline text; proposed in a separate PR for independent review (see §9)". BRIEF.md:98: "is drafted in a separate pull request and **needs an independent reviewer before merge**". That work merged (THEORY.md:12 and :528).
- measurement/CLAIM_MAP_v2.md:3: "Grok Bot executor for Chad Mitchell, via Ace. Private. Nothing was posted, sent or made public." measurement/FRAMEWORK.md:3: "Private working file."
- LICENSE.md:5 and :10 (linked from README.md:112 and :127): "This tree is a private working copy" and "**TODO (Chad):** pick a license before this repository is made public".
- prereg/*/PREREG.md say "private repo `Chad-Mitchell/theory-of-adaptive-organization`" (e.g. prereg/WIKIDATA-BAND/PREREG.md:4, prereg/vigil-ona/PREREG.md:3, prereg/SENSE-CELL/PREREG.md:3, reviews/night2/SELF/RESULTS.md:6). These are dated lock records and can stay, but they read oddly. A single sentence under README "How this should be read" fixes them: "Files written before 18 November say 'private'; the repository was private then."
- Minimal fix: BRIEF.md:3 delete "Private."; BRIEF.md:93 and :98 mark as DONE (merged v1.4.19); CLAIM_MAP:3 and FRAMEWORK:3 delete "Private."; LICENSE.md: reword to "No license has been chosen. All rights reserved by the author until one is added" and delete the TODO line (Chad's decision whether to pick one now).

**S5. Internal agent jargon appears unexplained, and nothing says AI agents helped write the files.**
- "Ace" appears in THEORY.md (2 times), STATUS.md:9 and :19 ("Ace's working folder `<local>/gtao/` on the box"), BRIEF.md:3 and :7, BOOKENDS.md:3, QUEUE.md:3 ("Ace's working folder holds only a pointer to this file") and many test files. "Grok Bot executor" appears in BRIEF.md:3, BOOKENDS.md:3, CLAIM_MAP:3, FRAMEWORK:3.
- Turn ids "t1908", "t1927", "pt1928u" appear about 29 times in THEORY.md (e.g. :10, :13, :15) and 7 to 8 times in BRIEF, STATUS and BOOKENDS.
- README.md says nothing about who Ace is. A newcomer cannot tell what "Chad, t1927" is.
- Minimal fix: add 2 lines to README "How this should be read": "Parts of this repository were drafted and checked by AI agents working for the author ('Ace' is the author's assistant; 'tNNNN' are chat turn numbers that mark the author's decisions). Every claim status is in CLAIM_MAP." Honesty-wise it is better to disclose than to leave it to be discovered.

**S6. BOOKENDS review claims are not verifiable from the repo.**
- STATUS.md:3 and THEORY.md:528: "after two rounds of three independent reviews (math/logic, physics, biology/prior art; round 2 all PASS-WITH-FIXES, every item fixed)". BOOKENDS.md:16: "Three independent reviews of revision 1 were held outside the repo".
- `git ls-files` shows no BOOKENDS review files. The SCALE_ENDS review is in the repo, but these six are not. Meanwhile README.md:32 and BRIEF cite the independent-review label as support.
- BOOKENDS.md:32 does say "the round-3 edits themselves have not been re-reviewed", which is the honest part.
- Minimal fix: either add the six review files under `reviews/night2/` or append "(review files are not in this repository)" at STATUS.md:3, THEORY.md:528 and BOOKENDS.md:16.

## NIT
**N1.** README.md:42: "**Update, 18 Nov 2026 (v1.4.20):**" while THEORY is v1.4.21 (README.md:19 and :101 say v1.4.21). The checker does not catch this. Change to v1.4.21.
**N2.** README.md:80 and THEORY.md:251: "gives them an **external timestamp only from today**". "Today" was 14 November 2026 (commit 2026-11-14 23:15 -0500). Written now it is ambiguous. Replace with "from 14 November 2026".
**N3.** README.md:74: "Proved and self-checked; novelty unconfirmed, probably folklore." Add "in-model" after "Proved" to match the required labelling.
**N4.** Off-repo names: STATUS.md:9 names `CURRENT_BRIEF.md`, `STATE.md`, `MEMORY_BRIEF.md` (marked as stale pointers; fine). QUEUE.md:58 `outcomes.jsonl` and QUEUE.md:110 `checks/d3s_shuffle_repro.py` do not exist in the tree. STATUS.md:19 says `<local>/gtao/` on the box. None of this is harmful, only noise.
**N5.** THEORY.md:12 heading: "Status at a glance (15 November 2026, about 10:00 AM ET; ...; ends of the scale ... added in v1.4.19, 18 November 2026 ...)". It is a patchwork stamp and is hard to read. STATUS.md:3 is a single ~450-word paragraph of stamps. Cosmetic.
**N6.** BRIEF.md:94 says a 12 Nov X post "says atoms have 'nothing to maintain'" and that a correction needs Chad's go. This is accurate and honest, but it is public text about his own post. Chad may want to word it deliberately before the midnight post links to the repo.
**N7.** Third-party data redistributed in `night2/GITHUB/data`, `tests/LFK_SPF/data`, `tests/F1/data` and similar: all public sources (GitHub metadata, SPF, SEC). No personal data. A one-line "sources and terms" note would help; not urgent.
**N8.** README.md:43/THEORY: first-screen jargon such as "Tier-1", "MV1–MV10", "prereg", "Axiom 5; CLAIM_MAP J16" appears at README.md:30 and :42 without a gloss. That is fine below the fold.

## Overclaim review (question 1)
I checked README, THEORY (status block, §0, §1, §2.3, §6, §8, §8b), BRIEF, STATUS and BOOKENDS against CLAIM_MAP. I found no sentence that claims more than the map supports, apart from the S1 framing. Specific items that hold up:
- README.md:9, "proved only inside the model ... untested, not refuted ... passed / failed on a proxy". Matches THEORY.md:8, :15, :16.
- README.md:32 and THEORY.md:13 give N25 and N26 as "PROVED (in-model)", with N25 "partly definitional" and N26 conditional on lateness-as-error and limited to pre-Page-time holes. Matches CLAIM_MAP N25 and N26. N28 and N27 are OPEN, and N29 WITHDRAWN as framing.
- THEORY.md:36 and :129 keep the bet as "untested" and J16 as an axiom that the model alone cannot test.
- THEORY.md:221 and README.md:36 ("No one in charge is narrowed ... J9 OPEN") match CLAIM_MAP J9 OPEN and "Hypothesis, not a consequence".
- BOOKENDS.md:34: "not a 'law' and not a theory of everything ... **untested, not refuted**". BOOKENDS.md:32 states its own review limits.
- README.md:84–96 scoreboard leads with the literal verdicts (K4 PROXY-FAIL; H9 PROXY-PASS with "substance prior art").
- BOOKENDS.md:87 to :104 (the plain-words "Keep / Burn / Know" picture) is written in a flat voice ("There are three answers."). Its hedges are in §0 and in the labelled sections, and README.md:7 repeats it flatly. That is acceptable given README.md:9, but see S1 and S3.

## Internal contradictions (question 2)
- Versions: README, THEORY, BRIEF, STATUS and BOOKENDS agree on THEORY v1.4.21 and CLAIM_MAP v2.41, except README.md:42 (N1). BOOKENDS.md:50 says "THEORY.md v1.4.19" as the version it read; that is a historical source note and fine.
- Dates: weekdays are consistent (14 Nov Saturday, 15 Sunday, 18 Wednesday). THEORY.md:3 explains the unused v1.4.12.
- "Private": see S4. THEORY.md and README no longer call the repo private (THEORY.md:4 is "public working draft").
- Withdrawn claims: L^{2/3} correctly flagged everywhere. "V ≥ 2" is flagged as wrong as stated everywhere I looked (README:44, THEORY:17, :283, BRIEF:43).
- Real tension: the second-law backbone versus "decorative" and "Not literal above the cell" (S1).

## Privacy (question 3)
No findings. Details:
- Emails in file content are only `research@example.invalid` and `box@example.invalid` placeholders (e.g. tests/F1/DATA.md:19). The `*@np.linalg` and `*@users.noreply.github.com` strings are code and bot noreply addresses.
- No phone numbers, street addresses, tokens, API keys, private keys, `/home/`, `/Users/` or `C:\Users` paths.
- Matches for "Nelnet", "StudentAid", "student loan", "Laura", spouse, family or finances: none. The word hits were all technical ("token" in dataset names; "paypal" in a GitHub repo name in a data list).
- Looper: README.md:118 says no Looper code, store contents or personal data. In the tree, Looper appears only as aggregate counts in reviews/night2/SELF/RESULTS.md:11–14 ("98 items", "264 versions", "1,201 commits"; "Aggregate statistics only; no personal content"). reviews/night2/SELF/explore_postlock.json holds generic discard-reason strings, including "A historical excerpt. It does not change a later cue about Chad's life beyond the store." No store text. The DRIFT1 person arm is redacted (tests/DRIFT1/REDACTION.md). README.md:118 is accurate, but "store contents" is a slightly strong negative given the aggregate stats. Fine if Chad is fine with them.
- Commit metadata: Chad Mitchell / Chad-Mitchell with chad39@gmail.com and the GitHub noreply address, plus `box <box@localhost>`. No other identities.
- No raw clinical, survey-microdata or email corpora tracked (no Enron, PIAAC, glucose data files). tests/README.md says so.

## Links (question 4)
Script: extracted every `](relative)` link and every backticked `*.md|py|json|txt|mp4|csv|...` path from README, THEORY, BRIEF, STATUS, BOOKENDS and QUEUE; resolved each against the file's folder, the repo root, and a bare-filename search. README, THEORY, BRIEF and BOOKENDS: 0 missing. STATUS: 3 names that are deliberate off-repo stale-pointer mentions. QUEUE: 2 (N4). All external links were not fetched.

## First screen (question 5) — what a newcomer sees in 30 seconds
- Strong: line 7 says what it is in plain words; line 9 says what is proved (in-model), what is untested, and what "passed/failed on proxy" means; line 11 says "not a theory of everything".
- Weak: lines 1 to 5 hold an author line and a superseded video before any substance; "GTAO" is unexplained until line 15; line 7 is one dense paragraph; line 11 repeats line 9 and carries a turn id.
- Minimal fixes (no rewrite): S2 (drop line 5, expand GTAO in title), S3 (one-breath line), S1 (second-law framing clause), S5 (two-line disclosure).

## Delete note
Clone at /tmp/rev-public removed after writing this file; /tmp/linkcheck.py removed.
