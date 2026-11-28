# Records

Frozen material: dated runs, preregistrations and their data, reviews, lab notes, the night-2 run, the v1.4.29 theory
and earlier figure views. Nothing here is edited; the ledger (`measurement/CLAIM_MAP_v2.md`) cites it, and the hash
locks under it are checked by `tools/verify_locks.py`.

**Moved on 27 November 2026.** These trees moved here from the top of the repository in one rename-only commit. The
one map from old path to new path is [`tools/movemap.py`](../tools/movemap.py) (`MOVES`); every check reads it.
Links written inside these files before the move use the old paths and resolve at the last commit before the move:
<https://github.com/Chad-Mitchell/theory-of-adaptive-organization/tree/dd4c3f93d66c1c1a16f0e4ca76792c4e141ef0b7>. To follow an old link by hand, apply
the map to its path.

| folder | what it holds |
|---|---|
| [`tests/`](tests/) | field and simulation tests (index: [`tests/README.md`](tests/README.md), frozen) |
| [`prereg/`](prereg/) | field preregistrations and their data |
| [`reviews/`](reviews/) | dated reviews (index: [`reviews/README.md`](reviews/README.md), frozen); `reviews/theory/` holds the reviews that sat under `theory/` |
| [`notes/`](notes/) | lab notes |
| [`night2/`](night2/) | the night-2 run |
| [`reference/`](reference/) | the theory as it stood at v1.4.29 |
| [`figures/`](figures/) | earlier figure views, off the front page |
