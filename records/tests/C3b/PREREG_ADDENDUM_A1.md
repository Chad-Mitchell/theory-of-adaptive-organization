# Addendum A1 (2026-11-14 ~22:30 ET): frame expansion, before any post-shock or outcome data

Status when written: PREREG.md hashed and committed (f1ba564, 22:23 ET). Stage 1 (pre-shock PyPI screen) had processed
about 14,600 of the 71,900 Valiev packages. Seen so far: only pre-shock counts (status, pinned-out/depends flags per
shock). No post-shock release, tau, GitHub or outcome data have been fetched for any dependent.

Why: the Valiev frame yielded pinned-out dependents at roughly 0.7% of packages (17 of 2,468 in the first batch),
projecting ~300-500 Arm P rows before GitHub filters, i.e. power about 0.3-0.65 for the theory-sized effect (PREREG 5).

Change:
1. Frame = Valiev 2018 packages UNION, per shock, all packages whose latest version in the last sethmlarson/pypi-data
   snapshot published before R has an unconditional (non-extra) dependency on the shocked lib, and that list a
   github.com/owner/repo URL in that snapshot (most frequent one). Snapshots: sqlalchemy 2023.01.25, pandas 2023.03.19,
   urllib3 2023.04.16, pydantic 2023.06.16, numpy 2024.04.24; Arm W adds packages with a cp311 wheel in 2023.09.28.
   Snapshots predate their shocks, so the frame is not selected on post-shock survival. Built by
   code/build_frame_snapshot.py -> data/frame_snapshot.csv. Every frame package is screened for every shock with the
   unchanged PREREG rules (the snapshot only nominates candidates; pinned-out status comes from the actual last pre-shock
   release's per-version metadata).
2. Arm P cap: if more than 5,000 rows pass stage 1, a simple random sample of 5,000 (seed 20261114) before any GitHub call.
3. New sensitivity S10: H1 on the Valiev-frame subset only (the original frame).
Everything else in PREREG.md is unchanged, including all hypotheses, models, SESOI and verdict rules.
Limitation added: the numpy snapshot is ~2 months pre-shock; packages first created after it are not in the frame
(packages that existed and added a numpy<2 pin later are still caught, since the screen reads their actual last
pre-shock release).
