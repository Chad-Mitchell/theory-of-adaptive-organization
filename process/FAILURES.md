# FAILURES: process-miss log

*Started Tuesday 24 November 2026 (America/New_York). A maintained log of process misses of every kind, not only memory ones. Rules: [`PROCESS.md`](PROCESS.md) §2–§4, row format: [`MISS_LOG_TEMPLATE.md`](MISS_LOG_TEMPLATE.md). Model and measurement misses stay in each test's `DEVIATIONS.md`. A process miss gets one entry here.*

Each entry records:
- the date;
- the locked prediction (what the process said would hold);
- the outcome;
- the miss, with its size and cost;
- the cause;
- the location;
- the update, scaled to size, repetition and stake (`PROCESS.md` §1 items 2–3).

Low-stake entries stop at the ledger row. Medium and high entries add the short block below the row. Entries are appended and are not edited after the fact. A correction is a new entry that points back to the earlier one.

## Ledger

The columns are the eight fields of [`MISS_LOG_TEMPLATE.md`](MISS_LOG_TEMPLATE.md) (`prediction_id`, `locked_prediction`, `outcome`, `miss`, `location`, `stake_x_info`, `update`, `breach_check`). `date` and `cause` are the two extra columns.

| date | prediction_id | locked_prediction | outcome | miss (size, cost) | cause | location | stake_x_info | update | breach_check |
|---|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | `REPO-CURRENT-1` | `STATUS.md` and `OPEN_WORK.md` match `main`, and reviewed work is merged or listed as waiting. `check_fresh.py` passing was taken as evidence of that. | `STATUS.md` said 757 Lean declarations at `d2aeb81`. 757 was the correct count for `main` until PR #260 merged. Reviewed Lean batch 1 (926 AxiomAudit constants at `d12642b`) and batch 2 (1,185 at `6663d0e`) sat unmerged on the fork, and `STATUS.md` did not say so. Four later merges (#261, #262, #264, #265) left the pointer unchanged. The `OPEN_WORK.md` header still named `4594eef`. | Reviewed work worth 428 more constants (757 against 1,185) was unmerged and unmentioned, and the pointer was four merges behind. Cost: the reliability of every status answer that day, and the hours spent rebuilding the pages. | Ace answered from a compressed summary without opening the files. `check_fresh.py` compared `STATUS.md` only with `main`, with a five-merge window. It never looked at open PRs or the fork, nor at the Lean count. The repo has no CI, so checks ran only by hand. | process | high | `tools/check_pending.py` (pointer window 3, Lean total against `formal/lean/AUDIT.json`, reviewed-but-unmerged PRs older than 24 h, STATUS open-PR list against the live list) and the `PROCESS.md` §4 rule: refresh `STATUS.md` and run the check after every merge. Lean batches merged as #260 and #266. `STATUS.md` and `OPEN_WORK.md` rebuilt in #270. | none |
| 2026-11-24 | `REPO-CURRENT-2` | The rebuilt `STATUS.md` (#270) states the open PRs as they are. | The first draft said #253 had 2 review blockers. The delta review of `49a2ee8` had ended with 0 blockers, and Forge's pre-check on #253 had said so. | One stale status line, caught by the independent review of #270 before merge. Cost: one review round. | The line was written from the earlier review of `9af966c`, not from the live PR. The check that would catch it (STATUS open-PR list against the live list) did not exist yet. | process | medium | Repeat of `REPO-CURRENT-1` within hours. Update: re-pull live PR state right before every push of a status line, and `check_pending.py` now fails when the STATUS open-PR list differs from the live list. | none |

### 2026-11-24 `REPO-CURRENT-1` (high)

1. **Locked prediction and risk.** The repo rule was that `STATUS.md` is a current pointer (`STATUS.md:1`) and `tools/check_fresh.py` keeps it fresh. The rival reading was that the check covers only one pointer and nothing about pending work. No one checked that rival.
2. **Miss and location.** The location is process, with no model or measurement part. The Lean proofs were correct and passed their audits. The pages and the person answering did not track them. `PROCESS.md:30` already names both stale `STATUS.md` summaries and answering without opening the file as process misses. This entry is a repeat of both.
3. **Update.** The update is structural, not a reminder, because the miss repeated and the stake was high. A check now fails on all three gaps: a stale pointer, a wrong Lean total, and reviewed work left waiting. One rule ties a refresh and that check to every merge. A daily CI run of the same check is proposed in the description of #272. It waits on a token with the `workflow` scope, or on adding the file in the GitHub web UI.
