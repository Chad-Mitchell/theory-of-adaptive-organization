# C3 data notes

All data are public. Pulled 2026-11-13 (ET) with the box's authenticated `gh` CLI (read-only).

| Stage | File | Source | When (ET) |
|---|---|---|---|
| Frame | data/package_urls.csv | Valiev et al. 2018, Zenodo 1297925, dataset_minimal_Jan_2018.zip | before prereg |
| Prereg | PREREG.md (sha256 23240b59…, git 1a9ad7e) | — | 14:34 |
| Screen | data/screen.jsonl → screen_passed.csv, sample_screen.csv, sample_repos.txt | GitHub GraphQL: isFork, createdAt, owner type, default-branch commit counts 2021 and 2022-07..2023-06 | 14:34–14:56 |
| Issues | data/issues.jsonl → measures.csv | GitHub REST `/issues?state=all&since=2021-01-01&sort=created&direction=asc` (issues + PRs created ≤ 2021-12-31 and updated since 2021-01-01) | 15:00–16:08 |
| Outcome | data/outcome.jsonl | GitHub GraphQL: isArchived, archivedAt, last default-branch committedDate | 16:10–16:12 |
| Analysis | data/analysis_dataset.csv, results.json, deviation_results.json, literal_boot.json, analysis_output.txt | code/ | 16:12– |

## Sample flow
- Frame: 71,903 package→GitHub URLs; 66,202 resolved (5,701 gone/renamed beyond redirect); 65,721 unique repos.
- Rule 1 (not fork, created < 2020): 63,333. Rule 2 (≥12 commits in 2021): 5,740. Rule 3 commit part (≥1 commit in gap): 4,743.
- Random sample of 2,500 (seed 20261113), per prereg cap.
- Issues pulled for all 2,500; 3 incomplete (pandas, sentry, superset: GitHub refuses page-number pagination past page 100) → excluded.
- Rule 4 (≥12 non-bot issues opened in 2021): 905. Rule 5 (σ, B, τ > 0): 899. Archived before t0: 3 dropped. **Analysis n = 896.**
- Events: 137 as coded by analyze.py; 105 under the literal PREREG text (see RESULTS, deviation D0).

## Measure notes
- Median σ = 2.5 items/month, B = 4.5 closures/month, τ (KM median time-to-close) = 44 days; 189 repos τ-capped at 546 d (KM median not reached).
- corr(ln σ, ln B) = 0.79 (collinearity, as anticipated in prereg §7).
- Spot check: of 40 random censored repos, 1 had only bot commits in the last 12 months, 1 had none since 2025-11-01 (consistent with its censoring date), so bot-kept-alive misclassification looks small (~3%).
- `state_reason` exists only for closes after mid-2022, so S3 (not_planned censored) is nearly identical to primary.
