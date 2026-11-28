# LOCK_ERRATA: hash locks that do not verify as the tree stands

*Tuesday 24 November 2026 (America/New_York). Checked by [`tools/verify_locks.py`](../tools/verify_locks.py), which runs inside `tools/check_consistency.py`. No locked file is edited by this page or by that script, and git history is not rewritten.*

A lock is a `*.sha256`, `SHA256SUMS*` or `LOCK*.txt` file made before a result was computed. When this page was written (24 November 2026) there were 222 lock lines: **163 verify**, **17 do not match** and **42 name files that are not in the repository**. This page accounts for the 17 and the 42. A plain `sha256sum -c` shows the 17 as mismatches, which looks like editing after the lock. For 13 of them the cause is one commit that changed only box paths. The other 4 and the 42 are described plainly below.

## 1. Scrub only: 13 files, proved

The public-readiness scrub `d513528` (18 November 2026, "tree only") replaced box paths in these files: `<local>` stands for `/workspace` and `<repo>` for `/workspace/theory-of-adaptive-organization`. Reversing exactly that substitution in memory gives back the locked sha256 for all 13 (`python3 tools/verify_locks.py` does this on every run). The original bytes also sit in git history at the commit in the last column.

| file | lock file | locked sha256 (first 16) | current sha256 (first 16) | locked bytes in history |
|---|---|---|---|---|
| `records/prereg/WIKIDATA-BAND/PREREG.md` | `records/prereg/WIKIDATA-BAND/LOCK.txt` | `068528225b72d5ad` | `64627432b4b12d0d` | `7cffd93` |
| `records/prereg/vigil-ona/ona_analyze.py` | `records/prereg/vigil-ona/LOCK.txt` | `3328161ccbe0b7e7` | `b5cb4b6ca1754035` | `52a624a` |
| `records/tests/C3b/PREREG_ADDENDUM_A2.md` | `records/tests/C3b/PREREG.sha256` | `42deb7bca4bf04af` | `6064d4ee311c5cf8` | `54ae2ce` |
| `records/tests/C3b/PREREG_ADDENDUM_A3.md` | `records/tests/C3b/PREREG.sha256` | `5a3384e52ba4561c` | `c8a18dc13fd0e890` | `bf8a4a3` |
| `records/tests/DECISIVE/banks/PREREG.md` | `records/tests/DECISIVE/banks/PREREG.sha256` | `b7ea310e30d4afe4` | `af9294797fa321dd` | `54ae2ce` |
| `records/tests/F1/code/analyze.py` | `records/tests/F1/PREREG.sha256` | `55ac2d8d01609076` | `0ba5193988c35e3b` | `54ae2ce` |
| `records/tests/F1/code/analyze_E.py` | `records/tests/F1/PREREG.sha256` | `4a77b3c80a4bd8f2` | `971bd3ea01e78fbf` | `54ae2ce` |
| `records/tests/F1/code/build_dataset.py` | `records/tests/F1/PREREG.sha256` | `89f8e84e137aa961` | `96912e652825b6d6` | `54ae2ce` |
| `records/tests/F1/code/covid.py` | `records/tests/F1/PREREG.sha256` | `3b494ee3017b179a` | `736409743dc82011` | `54ae2ce` |
| `records/tests/F1/code/extract.py` | `records/tests/F1/PREREG.sha256` | `b0a40771db2ee2b7` | `1ba5d70aeefc9684` | `54ae2ce` |
| `records/tests/F1/code/measures.py` | `records/tests/F1/PREREG.sha256` | `296a2e25e181bdca` | `0843c9bbf0880dfd` | `54ae2ce` |
| `records/tests/F1/code/power.py` | `records/tests/F1/PREREG.sha256` | `5684cd5d1e0bb66d` | `df68b55bc22a7d57` | `54ae2ce` |
| `records/tests/F1/code/sim_dataset.py` | `records/tests/F1/PREREG.sha256` | `a7c462befcb4c82e` | `5358e7b264bff655` | `54ae2ce` |

## 2. Changed after the lock: 2 files, declared

| file | locked version | later version | declaration |
|---|---|---|---|
| `records/night2/GITHUB/code/pull.py` | commit `86aa1cc`, blob `44563ed7`, lock hash `a6c218e0…` | commit `d9152f2`, blob `ee4f718e` (current) | The commit message reads "post-lock I/O fix (declared): pull.py waits for rate-limit reset instead of giving up; analysis code unchanged", and the file marks the lines "POST-LOCK I/O FIX (declared)". The diff changes `tries` from 4 to 40 and the rate-limit wait. |
| `theory/layers_checks/stores.py` | commit `e50e92f`, blob `c7c1e06b`, lock hash `df6b7039…` (listed in `records/tests/EVO1/PREREG_EVO.sha256`) | commit `a1a98aa`, blob `71a113e0` (current) | PR #116, "v2.8-htindex". The function `mse_given_b` gained a numerical guard (21 lines added, 6 removed); the commit text calls it a "store-optimizer fix + regression test". The change is not marked as post-lock in the file or in the commit message. Which EVO1 results ran on which version is not recorded here. |

`verify_locks.py` confirms, when git history is present, that the committed version at the locked commit hashes to the lock.

## 3. No committed version matches: 2 files, unverifiable

| file | lock hash | committed versions | finding |
|---|---|---|---|
| `records/tests/DECISIVE/glucose/code/analyze.py` | `8822a118…` | one, `54ae2ce` (blob `1c9a5051`) | Neither it nor its reverse substitution hashes to the lock. The locked bytes were not committed. |
| `records/tests/F1/code/outcome.py` | `35640274…` | two, `54ae2ce` (blob `7f4876fe`) and `d513528` (blob `3126c5e0`) | Neither version, with or without the reverse substitution, hashes to the lock. The locked bytes were not committed. |

For these two the lock cannot be checked from this repository, so nothing here says whether the file was edited after the lock. A result that depends on either file keeps the label it already has, with this limit added.

## 4. Raw data never committed: 42 lock lines

These lock hashes of external data files (downloads, API pulls). The data are not in the repository, so the hashes cannot be checked here.

| lock file | lines |
|---|---|
| `records/prereg/vigil-ona/SHA256SUMS_raw.txt` | 30 |
| `records/night2/GITHUB/data/SHA256SUMS` | 5 |
| `records/prereg/WIKIDATA-BAND/data/SHA256SUMS` | 2 |
| `theory/measured/ecoli/LOCK.txt` | 2 |
| `records/prereg/SENSE-CELL/data/SHA256SUMS` | 1 |
| `records/tests/F1/raw/companyfacts.sha256` | 1 |
| `records/tests/F1/raw/submissions.sha256` | 1 |

Added 28 November 2026, when the name pattern was widened: `records/tests/LFK_SPF/data/RAW_SHA256.txt` has 50 lines of raw data that were never committed. The pinned missing total is 85.

## What the counts mean

- 13 of 17 mismatches are explained exactly. 2 more are declared edits with the locked version in history. 4 cannot be checked: outcome.py and the glucose analyze.py, plus `waterfill_2026-11-20/worlds.py` (changed before the official start, `DEVIATIONS_2026-11-20.md` D1) and `theory/measured/ecoli/ecoli_calc.py` (`DEVIATIONS.md` item 1, the Riccati cross-check; it cites commit `6903de9`, which is not in this repository). 85 lock lines point at data that is not here (the previous 35, plus 50 in `records/tests/LFK_SPF/data/RAW_SHA256.txt` once that file was read as a lock).
- The locks are real: they were committed before the results they protect, and the original blobs are in the public history except for the two in section 3.
- `tools/verify_locks.py` pins the non-OK counts (13 scrub-only, 2 changed after the lock, 4 unverifiable, 85 missing) and the missing totals by lock file. OK has no upper pin: new locks that verify are free, and the test floor is 163 OK (`tools/test_verify_locks.py`). It also pins the **current git blob** of the three files that no lock covers and whose lock does not verify: `theory/layers_checks/stores.py` (`71a113e0`), `records/tests/F1/code/outcome.py` (`3126c5e0`) and `records/tests/DECISIVE/glucose/code/analyze.py` (`1c9a5051`). A later edit to any of the three fails. The later git blob of each post-lock file is always checked, including when this clone has no lock-time history: `records/night2/GITHUB/code/pull.py` is pinned at `ee4f718e`, and `theory/layers_checks/stores.py` at `71a113e0`. The 13 scrub-only files are protected by the reverse-substitution proof. A new lock that does not verify, a pinned file that starts to verify, a change in the 85, or an edit to a pinned file fails `tools/check_consistency.py` until this page and the script are updated together.

## Which locks the script reads

It reads every 64-hex hash in `*.sha256`, `SHA256SUMS*`, `LOCK*.txt`, `SHA256*.txt` and `*SHA256.txt` files and ties it to a file in whichever format the lock uses (`<hex>  <path>`, `<path>  sha256 <hex>`, `sha256: <hex>` under a path, `<name>_sha256` with `<name>_path`, or a bare hash in a sidecar named for its file). A hash no format ties to a file is reported as a note, not dropped. The name pattern does not include `*.sha` before-image snapshots (`records/notes/rnd-2026-11-26/stepback/selfhorizon/pre6_file_before.sha` and `pre8_file_before.sha`), JSON hash lists (`records/tests/DIR1/data/POOL_SHA256.json`), or prose hash quotes (`theory/keystone_checks/waterfill_2026-11-20/START.txt`). Until 27 November 2026 it read only `<hex>  <path>` lines (222 of them) and missed the rest; the first full read found no failing lock beyond the declared set above (`LOCK-PARSE-1` in process/FAILURES.md). On 28 November 2026 the name pattern was widened to include `SHA256*.txt` and `*SHA256.txt`, which brought in `records/tests/LFK_SPF/data/RAW_SHA256.txt` (50 missing) and `records/tests/SPF_RIGIDITY_OOS/data/SHA256.txt` (those hashes verify). A file that changed or never matched its lock must be named in a record: this page, or the `DECLARED_IN` table in the script.

## Not done, on purpose

No locked file was restored, re-hashed or edited, and no lock file was rewritten. Restoring the box paths would change the public tree; re-hashing would replace a lock with a new one. A reviewer who wants the original bytes can take them from the commits above.

## Moved line citations (27 November 2026)

`CORE.md:169` in files dated 24–25 Nov 2026 means https://github.com/Chad-Mitchell/theory-of-adaptive-organization/blob/7a5f33d8cbcf45b32aab2945555823afa6cbb243/CORE.md#L169 (the status-word definitions, now at `CORE.md` §Status words).

## Path scrubs in unlocked dated records (27 November 2026, PR #297)

Five records that no lock file covers had raw local `/workspace` paths replaced in place by `<local>`, the same substitution as `d513528`. No other byte of those lines changed, and no hash-locked file was touched (`python3 tools/verify_locks.py`). The original bytes are in git history (`git log -p` on each file).

- `theory/qm-selection-3-2026-11-26/RESULTS.md:8`, the launch line of a scored record ("Fresh clone from GitHub into `<local>/qmsel3-run`"). The clone path is provenance, not a score; the outcome lines are unchanged.
- `theory/hutter-2026-11-25/RESULTS.md:82`, the path of the independent gate read. This file also gained appended lines in this PR: a "Ledger rows (appended 27 Nov 2026; lines above unchanged)" section with rows P1–P4 after line 82. Those lines are new, not edits of old ones.
- `theory/RECORD_COST_ERRATA_R1316_2026-11-26.md:7`, the run directory in M1.
- `records/notes/rnd-2026-11-26/MANIFEST.md:3`, `:8-10`, `:23` and `records/notes/rnd-2026-11-26-late/MANIFEST.md:3`, `:41`, the source folders of the snapshot. These MANIFEST files are not listed in their `SHA256SUMS`.

The miss row is `ERRATA-SCRUB-1` in `process/FAILURES.md`.
