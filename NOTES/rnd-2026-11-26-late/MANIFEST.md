# Manifest: late 26 November 2026 notes (Forge)

*Copied Thursday 26 November 2026 at about 20:24–20:28 ET from the box folders `<local>/gtao-notes/rnd/` and `<local>/gtao-notes/WORKLOG.md`, for the Friday handoff update. Copied byte for byte; nothing in this folder was edited after the copy. Every copied file is listed with its SHA-256 in `SHA256SUMS` beside this file (`sha256sum -c SHA256SUMS` from this folder). Those lock lines are also what keeps the repo's word check from reading these notes as new prose: they are a record, written under the day's working vocabulary, and are kept as they were.*

This folder is a new dated copy. It does not overwrite `NOTES/rnd-2026-11-26/`. Paths below are relative to this folder.

## 1. What was copied

- **29 files**, listed in `SHA256SUMS`.
- The memory-rebuild set `context/` (five files). `WALLS.md` in this folder includes an append of three proposed walls at 20:24:05 ET; the first 18627 bytes are byte-identical to the 19:29:18 EST file (SHA-256 `475c129405a0ed264a57a3d35039ee9087325188ad019cc2ce8a39011dfe8276`). The whole file after the append is `6d207712623982408fc2998d2a9d2086378e87d2f5cf34cd2626903e8deedb78`.
- Updated `stepback/WORLD_TRACK.md` (Step 3 results and §4 review fixes).
- New or updated `stepback/worldtrack/` artifacts for Step 3 (the first snapshot had a mid-run `sp_reg.jsonl` / `sp_reg.log`).
- Completed T1 run artifacts `stepback/trackfirst/t1/t1_run.log` and `t1_run.jsonl` (the first snapshot copied a mid-run prefix: 76 of 154 jsonl lines, log stopped after the f=1 cells). `TRACKING_FIRST.md` itself is unchanged and is not recopied (`edd9bb00866cfd5d127d8b62c4921301929f23a83bd2680f6e6c65c484e3497f`).
- `stepback/NEXT_ROUTES_2026-11-26.md` and `stepback/nextroutes/` (Crossref outputs and the 20:14:38 main-block copy).
- `stepback/TRACKABLE_WORLD.md` and `stepback/trackable/` (pre-statement block, checks, Crossref).
- `review_worldtrack/REVIEW_WORLDTRACK.md` (independent review, not in the first snapshot) and two later review outputs.
- `WORKLOG.md`, the box work log with late hash lines through 20:24:05 ET. The first snapshot's `overnight/WORKLOG.md` is a prefix of this file.

## 2. Key hashes (also in the WORKLOG, timed to the second)

| item | time (ET) | SHA-256 |
|---|---|---|
| `context/WORKING_CONTEXT.md` | 19:29:18 | `c86996debec27b5f5ef825ae331174a6a64683c6904e5dd8e991338b8e63feb2` |
| `context/WALLS.md` (before proposals) | 19:29:18 | `475c129405a0ed264a57a3d35039ee9087325188ad019cc2ce8a39011dfe8276` |
| `context/MEMORY_CHALLENGE.md` | 19:29:18 | `af1323220cbd1f38ba15c52f5d518b01bba5187b8beb10173bf7bdc7f20fc525` |
| `context/FADED.md` | 19:29:18 | `2e160bdc6c918455ffb32a1d0115483489bf386ae41e116d144e1d619bbfd27e` |
| `context/SELF_REVIEW.md` | 19:29:18 | `bbc028790222660199a6b5e30da6b9d536e0de15bf52f3d7128f489fcd8d9e98` |
| `stepback/WORLD_TRACK.md` §3.6–3.14 | 20:01:48 | `949aee6dd7df582f56f1e4fb37c9d12e3cbec229fb85410ea32b109c92ef2b01` |
| `stepback/WORLD_TRACK.md` after §4 (all 9 fixes; this copy) | 20:01:52 | `5d1cb2b6e377f42ed5ef2a176b4f8ee00197f7a6afec4a466d5a6467729a7831` |
| `stepback/NEXT_ROUTES_2026-11-26.md` (final, after §5) | 20:15:37 | `ac43abe518c1e8edec0eb2ce13083cc7507beb0ef260fe604e8dba9ee6d3ff49` |
| `stepback/trackable/prestatement_block.md` (route A lock) | 20:18:37 | `a22962467bfb2b1df1c33d512a39cb783ab81bd86a7686b681a6fa9475f3fec6` |
| `stepback/TRACKABLE_WORLD.md` (final) | 20:20:12 | `7ad194c983f87382697fa0acc38d91ea871e8a5dc923b0dab5b85f3bbecdf9e2` |
| `context/WALLS.md` after proposed walls (this copy) | 20:24:05 | `6d207712623982408fc2998d2a9d2086378e87d2f5cf34cd2626903e8deedb78` |

The NEXT_ROUTES main block at 20:14:38 (111 lines, SHA-256 `4ff41038bde692e8d73765ae264b5a99c291ceec7584245bdf190d3b0b77b240`) is copied as `stepback/nextroutes/NEXT_ROUTES_main_block.md`. After review, A and D survived; B and C were dropped.

## 3. Withheld (4 files; on the box, not committed)

Same reasons as `NOTES/rnd-2026-11-26/MANIFEST.md` §3: scripts that contain an email address (a mailbox in a Crossref User-Agent or contact string), and a third-party paper excerpt (cite by DOI or arXiv id instead). Hashes are given so a later copy can be checked.

| path (under `<local>/gtao-notes/rnd/`) | bytes | SHA-256 | reason |
|---|---|---|---|
| `review_worldtrack/rv_tl.py` | 2476 | `2f50b9b48802def28b8b253d1622a0f128e4ddaadcc8b9e7f0e10b7ae95ce566` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo; same hash as in the first snapshot's withheld table |
| `review_worldtrack/kge_excerpt.txt` | 3468 | `2c09dd3bd7a3899e8892290c30f6ff482fea5633aa6da5e76eb2770343f679f6` | third-party paper excerpt (Kipnis–Goldsmith–Eldar, arXiv 1608.04679 / 10.1109/tit.2018.2878446); cite by DOI or arXiv id instead |
| `stepback/worldtrack/tl_core.py` | 1101 | `5d14c0b8661513a04f07cf005f313812ba328640393e1a81c298a10fe35af075` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo; same hash as in the first snapshot's withheld table |
| `stepback/nextroutes/crossref_nr.sh` | 1021 | `373097c29ddffb83c454a32e5a4144dda6fc7216de7483bca0a5ac06098336cb` | contains an email address (a mailbox in a User-Agent or contact string); withheld to keep addresses out of the public repo |
