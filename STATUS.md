# STATUS (current pointer; rewritten, not appended)

**As of:** Thursday 19 November 2026 (America/New_York): `THEORY.md` v2.1 and `measurement/CLAIM_MAP_v2.md` v2.50 (on the draft branch `v2.1-master-equation`, for Chad's review before merge). The long form of this page, with the done log from 15–18 November, is frozen at `history/2026-11-19_STATUS_long.md`.

## Where the theory stands
The core is THEORY v2.1: the locked one-sentence claim, the master equation (the cost, a definition), the principle that strongly selected systems sit near its minimum (untested, not refuted), and the Master Theorem with its special cases (CT20–CT23, layers L1–L3, proved in-model in the linear-Gaussian class and **not yet independently reviewed**). CLAIM_MAP section O lists every core result. The open theorems that matter most are the coupled-levels case, where system and world co-adapt (CX2), and Theorem P for drifting worlds (CX1). No field test has measured the theory's quantities validly, so every field result is "passed / failed on proxy"; stakes w have never been measured validly, and no tracked world's drift spectrum has been measured validly. Each theorem has been refereed at most once, by the same bot family.

## Canonical files
- `THEORY.md` — the theory (v2.1). The earlier v2.0 and v1.4.29 are frozen at `reference/THEORY_v2.0.md` and `reference/THEORY_v1.4.29.md`; the changelog is `reference/CHANGELOG.md`.
- `measurement/CLAIM_MAP_v2.md` (v2.50; one status per claim) and `measurement/FRAMEWORK.md` (validity gates MV1–MV10, tiers, anti-rescue rule).
- `process/QUEUE.md` + `process/queue/` — live work, ordered by Proposition SG, with a ledger.
- `tools/check_consistency.py` — run before and after any doc change; it must print RESULT: PASS.

## Next
- Independent review of the Master Theorem and L1–L3 (GAPS G8), then the layer killing test N56 on one system where spectrum, stakes and upkeep can all be measured.
- The first real test of the bet: **SAME-SYSTEM-AQN** (CLAIM_MAP N13), gated on a system whose stakes can be estimated (STAKES-PRECISION) and locked under MV1–MV10.
- Theorem P for a drifting world (CX1).
- SENSE-CELL-MATCHED (the physics binding ratio, N24 follow-up). C3b is blocked because the MV10 power gate is not met (`reviews/night2/C3B_GATE_ADDENDUM.md`).
- The pick order is in `process/QUEUE.md`; this list does not override it.

## Standing rules
The repository is public as of 18 November 2026. No posts or other outside acts without Chad's go. Call GTAO a theory. Field results are "passed / failed on proxy X", never field kills. Heavy compute runs at nice 19. Looper README wording needs Chad's approval.
