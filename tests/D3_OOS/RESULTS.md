# D3-TWO-EXPONENT-OOS — results (pick 8, uniform slot; ledger 45–48)

Run 15 Nov 2026, 12:22 PM ET, by executor queue-pick8 (for Ace; Chad t1914), against `PREREG.md` locked at commit `83aba94` (11:56 AM ET), before
any new repo was cloned or any Wikipedia revision fetched. Outputs: `run_oos.out`, `results.json`. Synthetic power check: `power_check.out` (pre-lock).
Raw data (clones, `wiki_revs.jsonl`) were in box scratch and deleted after the run; `fetch_git.sh` / `fetch_wiki.py` re-fetch (HEAD and live
revisions move, so a re-fetch is not byte-identical).

## Post-lock changes (complete list)
- **A1 (code, no effect on any statistic):** `run_oos.py` crashed on a non-UTF-8 file name in sharkdp/bat (`UnicodeDecodeError`, after 11 repos had printed).
  Fix: `errors="replace"` when decoding `git log`. The 11 repos printed before the crash were identical in the rerun.
- **Data shortfalls, handled by the locked rules:** Wikipedia "Category:Capitals in Europe" returned 0 pages (no group); "Programming languages created in the 1990s"
  (3 pages) and "Rivers of Germany" (< 5 pages with ≥ 50 edit days) excluded. 5 Wikipedia groups valid. All 27 GitHub repos valid (reserves not used).

## Locked verdicts

| | GitHub (n = 27, primary) | Wikipedia (n = 5 groups) |
|---|---|---|
| P1 Spearman(β_orig, β_shuf) > 0.3 (non-discriminating) | 0.863 → **passed on proxy** | 0.60 → passed on proxy |
| P2 median Δβ in [−0.03, 0.05] (non-discriminating) | 0.046 → **passed on proxy** | 0.007 → passed on proxy |
| **P3** fraction of repos with M_w above its renewal null (≥ 0.50 rejects) | **27/27 = 1.00 → renewal REJECTED** | **5/5 → renewal REJECTED** |
| P4 Wilcoxon Δβ > 0 (p < 0.01 and median > 0.01) | p = 0.00027, median 0.046 → **Δβ > 0 detected** | n < 6, not computed (as locked) |
| Report: median M_w (null median ≈ −0.01) | 0.225 (range 0.130–0.418) | 0.223 (0.177–0.292) |
| Report: median M_raw (D3S S3) | 0.370 | 0.283 |
| Report: Spearman(β_orig, a_need) (D3 replication) | +0.645 | n/a |
| Report: Spearman(β_shuf, a_need) | +0.636 | n/a |

Every repo and group had M_w above every one of its 200 shuffles (p = 1/201, the floor).

**Reading.** Hypothesis R (each file's edits form a renewal process) **failed on proxy "within-file consecutive log-gap correlation, binary daily edit series"**,
out of sample, in all 27 new repos and all 5 Wikipedia groups, with a test that had power against the R6 Cox worlds and correct size on renewal controls.
The item's own statistics (P1, P2) pass again, but as the referee showed (R6) and the power check confirms, they pass under renewal and Cox alike, so the passes carry no
weight. P4 adds that gap order carries low-frequency power (median Δβ 0.046, the size R6 found for pure Cox worlds at β ≈ 0.2). D3's positive sign replicates out of
sample (+0.645; MATCH1 +0.57), which the referee showed is expected under both renewal and Cox (R7), so it supports neither.

**What this does not say.** P3 cannot tell rate modulation (Cox) from file life-cycle trends or self-excitation (Hawkes); all three are rejected as renewal in the power
check. One post hoc check (below) makes the pure early-life-burst reading unlikely. No GTAO §0/§2 claim depends on this item; THEORY.md is not edited.

## Post hoc (exploratory; written after the locked results were seen; `posthoc_lifecycle.py`, `.out`)
Dropping each file's first 365 days and the repo's last 365 days (files keep ≥ 20 events): M_w still exceeds its null in **27/27** repos (median 0.196). So the
gap-order structure is not only an early-life burst. Cox-vs-Hawkes-vs-trend is not resolved (new item EDIT-MODULATION-SOURCE).

## Surprises (rule 4)
- **Weak:** two units show strongly **negative** Δβ (lodash −0.107, Wikipedia dog breeds −0.110) while M_w is high (0.35, 0.27): gap order lowers band power there,
  which neither pure Cox nor Hawkes in the power check produced (all Δβ ≥ 0). Possibly long dormant periods after a busy phase (a file "retired"); unexplained.
- **Weak:** the raw S3 statistic of D3S (M_raw 0.28–0.47) was mostly real structure, not between-file scale heterogeneity: M_w is about 60% of M_raw here.

## Consequences
- New CLAIM_MAP row **N17** (PROXY-FAIL for pure renewal; P1/P2 PROXY-PASS non-discriminating). **H19** stays MATH-CORRECTED; **N10** stays PROXY-PASS
  (non-discriminating) and gains a pointer: its renewal explanation is now contradicted on proxy out of sample.
- D3-DISCRIMINATE: its renewal-vs-Cox question is answered on this proxy by P3 (M_w with a within-file shuffle null), with synthetic power shown; what remains is
  Cox vs Hawkes vs trend → folded into EDIT-MODULATION-SOURCE (D3-DISCRIMINATE marked DONE, covered here).
- New items: EDIT-MODULATION-SOURCE; NEG-DELTA-BETA (weak surprise).
