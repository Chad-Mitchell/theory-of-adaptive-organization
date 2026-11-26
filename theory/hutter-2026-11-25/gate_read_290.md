*Committed 26 November 2026 from the reader's session file. Changes from that file: machine paths written `<local>`, and the banned-word list in row 6a elided. Nothing else changed.*

# Gate read: PR #290 (head 671e535, mitchell-moving:forge-hutter-test), theory/hutter-2026-11-25/

Reader: independent paper check, Wed 25 Nov 2026 ~12:15-12:45 ET. Gate spec: draft PR #263, `process/PREREG_GATE.md` at `8c4b3c0` (fetched as pull/263/head; identical to the commit the prereg cites). Clone at `<local>/gate-hutter` (nothing pushed). Primary sources re-read: hutter1.net `hrules.htm` and `index.htm` (curl, sha256 match PREREG §1 exactly: `e55d9f96…dc163`, `aed08e09…69f56`); LTCB `mattmahoney.net/dc/text.html` (curl hits a bot wall, read via web fetch, so its HTML sha256 `4d1224b7…b38889` could not be reproduced); record repo `astOwOlfo/fx2-cmix-transformer-v1` at `83f2603` (cloned to `<local>/gate-hutter-src/rec`); arXiv API for 1910.00762 and 2309.10668. E1 was not run.

PREREG sha256 recomputed: `501a82ded728e6616393ca88d2bf92114287061e219ecd25cd58680893771a77`, which matches `PREREG.sha256`.

## Table

| # | Item | Result | file:line | Note |
|---|---|---|---|---|
| 1a | Lock commit holds only the PREREG files | PASS | git `4a0d5e9` | Only `PREREG.md` (+123) and `PREREG.sha256` (+1). |
| 1b | Lock predates reading the design sources | PASS (self-reported, can't verify independently) | PREREG.md:3; RESULTS.md:3; crossref.out:3 | Author and committer times are the same: lock 11:29:09 ET, scoring 11:35:11 ET. RESULTS says the design sources were opened at about 11:31 ET. Crossref was queried 11:33 ET. I could not get a public push event for the fork. The clone's file mtimes are checkout times, so they show nothing. Nothing contradicts the order. The prize pages read before the lock don't contain "transformer" (I checked, comments included). |
| 1c | Scoring rules fixed before the sources were read | PASS | PREREG.md:111-117 | The hit/miss rule, the not-scorable rule, the overall rule and the DATA-ONE call are all in the lock. |
| 1d | Gate section placed "at the top" (G spec §2) | FAIL (minor) | PREREG.md:37 | The gate is §3, after the prize facts and the map. Its content is there. |
| 1e | Gate check done before scoring | PASS (disclosed) | PREREG.md:113; DEVIATIONS.md:5 | The spec asks for a gate check before a *run*. P1-P4 are readings of sources. The gap is disclosed. |
| P1-G1 | Can miss, odds stated | PASS | PREREG.md:47 | Bar f_max<0.40, miss odds 0.45. |
| P1-G2/G3 | Not an identity; rival predicts the same quantity with a gap | PASS | PREREG.md:48-49 | R-ENG predicts ~1/n, below 0.40. The text says R-RI is the same as J and R-MDL is silent. |
| P2-G1 | Can miss, odds stated | PASS | PREREG.md:61 | Bar s_ship>0.01, odds 0.12. Labeled low information. |
| P2-G3 | Rival and gap | PASS | PREREG.md:63 | R-SHIP predicts >0.01, the exact complement. Measured in exact bytes. |
| P3-G1/G3 | Can miss; rival | PASS (low information) | PREREG.md:74,76 | Odds 0.25. The single-model rival is a weak contender for a fork of the cmix line, which §0 says the author already knew mixes many models. |
| P4-G1/G3 | Can miss; rivals on both sides | PASS | PREREG.md:87,89 | Band 0.001-0.02, odds 0.25. R-SHIP predicts >0.02. R-ENG with a code-only decoder predicts <0.001. |
| P2/P4 | Independent items | FAIL (minor) | PREREG.md:61,87 | One fact, the shipped 2.93 MB of weights, decides both misses. The odds were set separately, not jointly. |
| 2-P2 | Re-score P2 | PASS (miss confirmed) | RESULTS.md:33-34 | `models/6m-q4-fp32.tfwc2` is 2,930,652 B: 0.02918 of S. **S counts it twice.** `build_and_construct_comp.sh` writes `cat cmix_orig comp_dict comp_order comp_tfweights header.dat > cmix`, which puts the weights in the compressor (3,428,474). `src/runner.cpp:1083-1086` builds archive9 as decomp_bin + dict + tfweights + output, which puts them in archive9 too. The writeup says "2.9MB each binary (or 5.9MB combined)" (writeup.md:9). Two copies: 0.05837. The locked quantity is "inside the decompressor", one copy, so 0.0292 is the right scored value. Miss of +0.0192 either way. Leaving out the fitted article order makes the score more conservative, not less. |
| 2-P4 | Re-score P4 | PASS (miss confirmed; wording) | RESULTS.md:48-49 | LTCB `.0969` row: 96,996,198 + 3,428,474 = 100,424,672, so 3,428,474/S = 0.03414. The prereg defines S1 as the *decompressor* (PREREG.md:83). The prize page and LTCB call the 3,428,474 the *compressor*. The decompressor inside archive9 is at least the 2,930,652 B of weights, so at least 0.0292. "0.0341 is a lower bound" holds only if S1 means all program bytes. The miss holds under every reading. |
| 2-P3 | Re-score P3 | PASS (hit confirmed) | RESULTS.md:41-43 | `predictor.cpp:248-260,263-277`: the inputs are bracket, fxcm, 1 direct, 15 indirect-ns (1+10+4), 10 match (5+5), 1 run, PPMD and the byte mixer, so ≥31. 23 `AddMixer(0,…)` calls at `:394-416`, one layer-1 mixer at `:421`, SSE at `:501`. The transformer feeds the byte mixer. |
| 2-P1 | P1 really not scorable? | FAIL | RESULTS.md:26-27; PREREG.md:43,53 | (i) RESULTS.md:27 says the allocation-based share "is not the locked quantity". But PREREG.md:43 names "summed from allocation constants in its source" as the locked fallback. (ii) RESULTS.md:26 invokes the one-hour reading limit. By the git times, under 5 minutes passed between opening the sources (~11:31) and the scoring commit (11:35:11), so the hour had not run out. (iii) A bound from cited sources points to a **hit**. The PPMD allocation is 14000 MiB (`predictor.cpp:302`, `ppmd.cpp:140`). All other tables must fit in the measured 9547 MB of D-RAM, *assuming they are RAM-resident and not mmapped*. That gives f_max ≥ 14000/(14000+9105) ≈ 0.61 ≥ 0.40. With P1 a hit, condition (i) of the overall rule (two hits) would be met. Condition (ii) still is not, so "open miss" stands. |
| 3a | Record 100,424,672 | PASS | PREREG.md:18 | index.htm: fx2-cmix-T, Vladimir Ivanov, 24.Jul 2026, 100'424'672. Task box: "S:=S1+S2 < L := 100'424'672". |
| 3b | Threshold < 99,420,425 | PASS | PREREG.md:19 | index.htm top row "<99'420'425 … >1% … >5'000€". 0.99·L = 99,420,425.28. (L−99,420,425)/L = 1.0000028%. The one-byte gap is reported correctly. |
| 3c | Caps | PASS | PREREG.md:20-21 | hrules: "70'000/T hours … at most 10GB RAM and 100GB HDD … No GPU usage". T≈1427 and T=1310 single-core give 49.05 h and 53.44 h. index.htm: "≲50 hours using a single CPU core and <10GB RAM and <100GB HDD". The 2× relaxation and the command-line-length rule are quoted correctly. The 116MB vs 100MB header mismatch is real. |
| 4-G1 | E1 bar and miss odds | PASS | PREREG.md:104-105 | ρ≤1.005 and u_B≤0.70, odds 0.55. (My lean: Arm B caps confidence near 0.95 on near-deterministic bits, so a ρ miss looks more likely than 0.55. The bar is still honest.) |
| 4-G2 | E1 not an identity | PASS | PREREG.md:106 | Data-dependent run with no closed form. |
| 4-G3 | E1 rival predicts the same quantity with a gap | FAIL | PREREG.md:107 | The R-ENG and R-RI "every step updates, so ρ>1.005" claim is unsourced. The real engineering prior art predicts what J predicts. In the record itself, fxcm gates training with an adaptive band, and that skip *does* save the loop (see 4-PA). selective backprop (arXiv:1910.00762) skips low-loss work because it is cheap. No rival value is given for u_B. In effect the named rival is a strawman. |
| 4-G4 | E1 reach | PASS | PREREG.md:108 | Level (a), with a route to (c) named. |
| 4-G5 | E1 next steps differ | PASS | PREREG.md:109 | Hit leads to a reinvestment test. Miss leads to an open miss. |
| 4-B | E1 budget and stop rule | FAIL | PREREG.md:102 | Stated: "single run each, deterministic, C, under a minute". Missing: an explicit stop rule (what happens after a crash, a bug fix or a rerun; a ban on tuning the 0.05 threshold or the rates) and a compute cap. Left open to the implementer: the hash function, the initial probabilities, the stretch clamp, the 16-bit rounding and the update order. Those choices can move ρ by more than 0.5%. |
| 4-PA | E1 prior-art claim "half used" | FAIL | RESULTS.md:63-64; MEMO.md:36; DEVIATIONS.md:6 | **Wrong in two places.** (1) RESULTS says "the training loop still runs with err = 0 (`:555`)". The `train()` it read at `fxcmv1.cpp:536-544` is inside a comment block (`:520-545`). The live `train()` at `:504-517` opens with `if (e) {`, so in-band bits skip the weight loop entirely, which matches the code comment "less updates and better speed" (`:4698-4699`). (2) RESULTS says "outer cmix mixers update on every bit (`mixer.cpp:74`)". The very next lines, `mixer.cpp:75-77`, read `if(fabs(update)<0.000000000005f && extra_inputs_size_>0) { return; }`: an early-return skip, though with a near-zero width. So the record already uses a time-saving inaction band, with adaptive width, in the inner mixers. E1's novelty shrinks to "a wider band in the outer mixers". That fails the "not used by the record" premise of overall-rule (ii) (PREREG.md:115). Citation 1910.00762 checked: title and authors match the arXiv API. |
| 4-T | E1 "binding time cap" premise | FAIL (minor) | PREREG.md:100; RESULTS.md:58 | LTCB D-time is 131,561 s (36.5 h) against a cap of ~49-53 h. With slack time, J's own band logic gives update time a shadow price near 0. |
| 5 | Not-DATA-ONE call | PASS | PREREG.md:117; RESULTS.md:68-70; MEMO.md:47 | DATA-ONE (`OPEN_WORK.md:251` at lock) needs a band that excludes a named rival, a cost-to-fitness map, a population proxy and a redesign time. Here the map is the identity J=S, which equals R-MDL. There is no population proxy and no redesign time. P3 doesn't exclude R-ENG or R-MDL. The P2 and P4 misses went to R-SHIP. Correct. |
| 6a | Banned words | PASS | all four files | grep finds none of the words on the repository's banned-word list (`tools/banned_words.py`). [List elided in the committed copy so the banned-word check passes.] |
| 6b | "law" only in the hypothesis sentence | PASS | PREREG.md:5; MEMO.md:5 | The sentence matches CORE.md:7 byte for byte. No other "law". |
| 6c | Memo labeled hypothesis | PASS | MEMO.md:1,3 | Title says "(HYPOTHESIS)", and line 3 says nothing in it is a field result. |
| 6d | No public claim | PASS | PREREG.md:3; MEMO.md:3 | "no prize entry, no email, no public claim". The OPEN_WORK row says "self-check, not an independent review". |
| 7 | PR scope | NOTE | git 66640ab..671e535 | The PR also edits STATUS.md in 2 commits, outside the test folder. STATUS still says `main` is `fa91b59`. |

**Counts:** 33 rows: 25 PASS (one of them, 1b, is self-reported and could not be verified independently), 7 FAIL, 1 NOTE. Outside the table: 4 BLOCKING and 10 NON-BLOCKING.

## BLOCKING

1. **E1 prior-art reading is wrong** (RESULTS.md:63-64, MEMO.md:36, DEVIATIONS.md:6, OPEN_WORK HUTTER-J "half used"). The live fxcm `train()` skips the loop when err=0 (`fxcmv1.cpp:504-506`; the one cited, `:536`, is commented out). `mixer.cpp:75-77` also returns early on tiny updates. So the record uses a time-saving inaction band, and E1 fails the "not used by the record" premise of rule (ii). Fix with an appended correction.
2. **E1 G3 fails.** The rival's "ρ>1.005" is unsourced and contradicted by the prior art: fxcm's band and selective backprop both predict what J predicts. u_B has no rival value at all. As written, E1 is a gate STOP.
3. **E1 has no stop rule, and its implementation is underspecified** (PREREG.md:102). The hash, the initial values, the clamp and the rounding are free, and reruns and tuning are not ruled out. A new appended prereg must close these before any run.
4. **P1 "not scorable" misstates the lock** (RESULTS.md:26-27). The allocation-constant fallback *is* locked (PREREG.md:43), and the one-hour limit could not have elapsed (11:31 to 11:35 ET). The cited allocations give f_max ≥ ~0.61, a likely hit, assuming the non-PPMD tables are RAM-resident. Append either a finished allocation sum with a score, or a corrected reason. The "one TEST hit" count (RESULTS.md:21, OPEN_WORK row) may change to two. The overall "open miss" stands either way, because of rule (ii).

## NON-BLOCKING

- The Gate is §3, not at the top as `PREREG_GATE.md` §2 asks (PREREG.md:37).
- P2 and P4 are one observation, the shipped weights, counted as two misses. Their miss odds were not set jointly.
- P4's S1 is ambiguous. The prereg defines it as the decompressor, while the prize page and LTCB's 3,428,474 are the compressor. The decompressor's share is ≥0.0292, so "0.0341 is a lower bound" needs the "all program bytes" reading. The miss is robust.
- P2: state outright that S counts the weights twice (compressor + archive9). The scored one-copy value of 0.0292 is the locked quantity.
- P3 carries little information given §0's prior knowledge of the cmix line. Odds of 0.25 are generous.
- The timeline can only be checked from git commit times (the times look consistent, about 6 minutes from lock to results). I could not reproduce the LTCB HTML hash because curl hits a bot wall; the figures do match the page text.
- The E1 "binding time cap" premise is weakened by the 36.5 h decode time (RESULTS.md:58).
- Scoring P1-P4 before a gate check is disclosed (DEVIATIONS.md:5). The spec only requires a check before runs.
- The scored source is the September `83f2603`, not the July submission. This is disclosed (DEVIATIONS.md:8), and the writeup's "2.9MB each binary" covers July.
- The PR touches STATUS.md outside the test folder, and STATUS's `main` pointer (`fa91b59`) is stale.

## E1 gate status

**GATE STOP, not a GATE PASS.** G1, G2, G4 and G5 pass on paper. G3 fails, and so do the budget and stop-rule check and the not-used premise. E1 was not run.
