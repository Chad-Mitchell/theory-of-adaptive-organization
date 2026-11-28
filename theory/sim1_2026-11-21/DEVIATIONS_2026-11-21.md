# Deviations: T28 SIM-1 rehearsal test, 21 November 2026

These are post-result housekeeping notes. They do not change any official number, gate, or locked file. The official record remains **PASSED** (P1 PASS 3/3, P2 PASS 3/3, P3 PASS 3/3, P4 PASS 3/3), in-model. `PREREG.md`, `predictions.json`, `LOCK.txt`, `run_sim1.py`, `sim1_lib.py`, and the official `run_sim1.json` / `run_sim1.log` bytes are not edited.

Locked hashes, unchanged, remain those in `LOCK.txt`:

| File | SHA-256 |
|---|---|
| `PREREG.md` | `f24d54271875a326947c7a17fc6114a0d8b0a7864c5ff17dc0eca2300260de8c` |
| `predictions.json` | `40c14cb4f991bee864b8bf74ab7f4583766cfb2ccab6aaf712deb692d2f33b09` |
| `run_sim1.py` | `9f3f41700aee9335f5f50f6612712fb87dee95b7a56fc732b418df917641181f` |
| `sim1_lib.py` | `2f20672665503aa6b0d48ef907ae3f24edded5ac935d191474b42ee383846559` |

## D1 (hygiene, recorded after the official run): official world-0 chain seeds collide with the first eight pilot world seeds

This is a hygiene miss, not a scoring miss. It is stated plainly. It is not a rule change, and it is not a rescoring.

**What collided.** Pilot world seeds, used only before lock and disclosed in `PILOT.md`, are `20261122800..20261122819`. Official Moran chain seeds are computed by the locked runner as

`CHAIN_SEED_BASE + 1000·world_index + 10·β + c`

with `CHAIN_SEED_BASE = 20261122400` (from the locked `predictions.json`), official P4 cell \(\beta=40\), and chain index \(c=0..7\). For official world 0 (`world_index=0`) that produces **20261122800–20261122807**, which are exactly the first eight pilot world seeds.

Official *candidate* / world seeds `20261122000..20261122015` (official worlds 0–2 used 20261122000–20261122002) do not collide with the pilots, nor with the prior-set lists checked by `seed_collides` (S5 rng 1000–1119, convexity_search 0–119, wide 5000–5119, named seeds 20261120 / 2026112020, T27 official 2026112100–2115, T27 chain block 20261121500–21999).

**Why this is not a scoring miss.** The shared integers were used for different RNGs: the pilots used them to draw world parameters (`draw_world`); the official run used them as Moran jump seeds on different (official) worlds. Official worlds are not the pilot worlds. The official numbers remain reproducible from the committed, hash-locked runner and library. `seed_collides` and `check_official_seeds_clean` only test prior-set lists; they never check intra-test disjointness of this test's own pilot and chain blocks.

**What is not done.** The locked runner and library are not patched. The official occupation, gates, and PASSED verdict are not recomputed or rescored. `PILOT.md`'s pre-lock sentence claiming that pilot seeds do not collide with the reserved official/chain blocks of this test is false; it is corrected by an appended erratum on that page, not by a silent edit of the pre-lock text.

**Standing rule (future tests).** Future preregs should treat the test's own pilot and chain blocks as reserved in the collision check, not only the seeds of prior tests.
