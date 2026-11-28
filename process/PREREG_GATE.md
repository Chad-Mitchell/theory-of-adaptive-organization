# PREREG GATE: no run unless the prediction can miss

*Tuesday 24 November 2026 (America/New_York). Maintained process rule, in the same family as [`PROCESS.md`](PROCESS.md) and [`MISS_LOG_TEMPLATE.md`](MISS_LOG_TEMPLATE.md). It adds no result. `THEORY.md` and `CORE.md` are not edited. Locked preregistrations keep their text. The process miss that prompted it is logged in [`misses/2026-11-24_T84_T84b_T85.md`](misses/2026-11-24_T84_T84b_T85.md).*

> **The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.** (`CORE.md:7`)

## 1. Why, from the cost

Apply the cost to our own research (`process/PROCESS.md:9-13`). A hit carries information only in proportion to its risk: a sure-thing hit gives \(-\ln p\to 0\) bits and still pays read and review cost \(A+L\) (`process/PROCESS.md:28`). A run whose outcome is fixed by the formulas it starts from therefore has expected information about 0 and a positive cost. Spend goes where expected miss size times stake is largest (`CORE.md:54`). Stake rises with reach: our own toy setup, then a stated claim in `CORE.md` or `THEORY.md`, then a real system or external data.

A line that says "Can it fail: yes" is not enough. T84, T84b and T85 each had one (`theory/dephasing-crossover-2026-11-24/PREREG.md:5`, `theory/dephasing-refresh-2026-11-24/PREREG.md:5`, `theory/ctc-fixed-point-2026-11-24/PREREG.md:5`, all on Forge's fork) and the scored bars of T84 and T84b, and five of T85's ten, still could not miss inside the locked cost (independent review, fork PRs #24, #28, #29). The gate below asks for the things that line skipped.

## 2. The gate (a section titled `Gate`, at the top of every new prereg, before any code or data)

| Field | What to write | Stops the run when |
|---|---|---|
| **G1. Miss** | The outcome, as a number, band or sign, that counts as a miss; and rough odds of a miss where feasible | No outcome is named, or the honest odds of a miss are about 0 |
| **G2. Not an identity** | What the outcome depends on that the locked formulas, definitions and known theorems do not already fix: external data, a selection run on realized outcomes (the EVO1 pattern, `records/tests/EVO1/PREREG_EVO.md`), dynamics with no closed form, or a statement not yet proved. If the scored value can be computed by hand from the locked cost before the run, compute it on paper | The value follows from the starting formulas, a definition, or a known theorem. Then the item is labeled `CONSISTENCY_CHECK` in its title, gets one ledger line, and is not run or reviewed as a test |
| **G3. Named rival** | A named alternative (prior art, or the simplest null) and the value it predicts for the same quantity; the gap between the two, and the resolution of the measurement | The rival predicts the same value, or the gap is inside the resolution |
| **G4. Reach** | Which level the outcome touches: (a) a toy setup we built, (b) a cited line of `CORE.md` or `THEORY.md`, (c) a real system or external data. For (a), name the result that would carry it to (b) or (c) | Level (a) with no route to (b) or (c) |
| **G5. Next step** | What we do differently after a hit and after a miss | Both outcomes lead to the same next step |

**Gate check.** Before the run, a separate reviewer reads only the `Gate` section and the formulas it cites, and answers pass or stop on G1–G5. That is a paper check, not a full review. The full independent review comes after the run, as now. A gate that stops a run is logged as one ledger line (`gate: stopped`, with the field), not as a miss. The gate read is a committed `gate_read*.md` file that names the PREREG it reads, committed before the results; a rescore needs a new or updated gate read; a consistency check says `gate: none (CONSISTENCY_CHECK)` in the PREREG, before the run. `tools/check_pending.py` fails each of these, except that a skipped gate read passes with an `EXCEPTION <miss id>` line when a `gate_read_retro_*.md` that names the PREREG is committed after the results, `process/FAILURES.md` has a row naming the folder, and the PREREG was committed before the results; a silent skip still fails.

**Launch rule (written here 27 November 2026; in use since `e496428ccfb36f223528f2654315a252b46f113e`, 26 November 2026, after record-cost rounds 14–15 and QM-selection 1).** Before the lock, every helper the scored path calls runs on toy inputs and its output is hashed with the lock. The lock is pushed, and `git ls-remote` shows it, before the run. The run starts from a fresh GitHub clone at that commit. A run that breaks this rule is logged in `process/FAILURES.md`.

## 3. Labels

- `TEST`: passed G1–G5. Scored and reviewed as now.
- `CONSISTENCY_CHECK`: failed G2. Allowed as a logged entry, labeled in the title and the headline, with information about 0. It never carries a support headline.
- Gate status words follow `measurement/FRAMEWORK.md` §2.3 and `process/PROCESS.md` §2. `NOT A TEST` stays the formal gate status for the same thing.

## 4. Old work

Work already scored before this gate keeps its locks. Before it is opened upstream, its memo and its row in the README open tables state, at the top, `TEST` or `CONSISTENCY_CHECK` by G2, without editing the lock.
