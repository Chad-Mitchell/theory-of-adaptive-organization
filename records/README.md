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
| [`records/tests/`](./tests/) | field and simulation tests (index: [`records/tests/README.md`](./tests/README.md), frozen) |
| [`records/prereg/`](./prereg/) | field preregistrations and their data |
| [`records/reviews/`](./reviews/) | dated reviews (index: [`records/reviews/README.md`](./reviews/README.md), frozen); `records/reviews/theory/` holds the reviews that sat under `theory/` |
| [`records/notes/`](./notes/) | lab notes |
| [`records/night2/`](./night2/) | the night-2 run |
| [`records/reference/`](./reference/) | the theory as it stood at v1.4.29 |
| [`records/figures/`](./figures/) | earlier figure views, off the front page |
