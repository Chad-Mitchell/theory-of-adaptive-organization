Reviewer's own exploratory checks for DECISIVE_F1_REVIEW.md (not preregistered).
rev_banks.py, rev_pop.py, rev_pop_sim.py: run from a COPY of tests/DECISIVE (cwd = the copy root) with
tests/DECISIVE/.venv/bin/python; they only read data. rev_f1_outcome.py: python3, reads F1 data read-only.
Do not run the original analyze.py scripts inside tests/ — they overwrite results files in place.
