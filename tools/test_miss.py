"""Tests for tools/miss.py: one format, one place, a root cause on every row, corrections carry rows."""
import os
import shutil
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import miss  # noqa: E402

ROOT = miss.ROOT


def _tree():
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "process"))
    shutil.copy(os.path.join(ROOT, miss.FAILURES), os.path.join(d, miss.FAILURES))
    return d


ROW = dict(id="ZZ-TEST", prediction="p", outcome="o", miss="m", cause="R2: a rule kept in memory")


def test_real_ids_are_read_including_annotated_ids():
    ids = miss.existing_ids(ROOT)
    assert "FORGE-GATE-1" in ids and "NOTTESTED-13M" in ids


def test_row_lands_after_the_last_ledger_row_with_ten_columns():
    d = _tree()
    try:
        miss.log(d, [dict(ROW, date="2026-11-27")])
        L = open(os.path.join(d, miss.FAILURES), encoding="utf-8").read().split("\n")
        i = next(i for i, l in enumerate(L) if "`ZZ-TEST`" in l)
        assert L[i].count(" | ") == 9 and L[i - 1].startswith("| 20")
    finally:
        shutil.rmtree(d)


@pytest.mark.parametrize("bad,msg", [
    (dict(cause="no code"), "R1 to R7"),
    (dict(id="FORGE-GATE-1"), "already used"),
    (dict(id="bad id"), "upper case"),
    (dict(stake="huge"), "stake"),
    (dict(stake="medium"), "three-item block"),
    (dict(location="model"), "DEVIATIONS"),
    (dict(miss=""), "missing miss"),
])
def test_bad_rows_write_nothing(bad, msg):
    d = _tree()
    try:
        before = open(os.path.join(d, miss.FAILURES), encoding="utf-8").read()
        with pytest.raises(miss.MissError, match=msg):
            miss.log(d, [dict(ROW, id="ZZ-OK"), dict(ROW, **bad)])
        assert open(os.path.join(d, miss.FAILURES), encoding="utf-8").read() == before
    finally:
        shutil.rmtree(d)


def test_pipe_in_a_cell_is_escaped():
    assert "a \\| b" in miss.failures_line(miss.validate(dict(ROW, outcome="a | b"), set()))


def test_medium_entry_adds_its_block_at_the_end():
    d = _tree()
    try:
        miss.log(d, [dict(ROW, stake="medium", date="2026-11-27", block=["a", "b", "c"])])
        t = open(os.path.join(d, miss.FAILURES), encoding="utf-8").read()
        assert t.rstrip().endswith("3. **Update.** c") and "### 2026-11-27 `ZZ-TEST` (medium)" in t
    finally:
        shutil.rmtree(d)


def test_model_miss_goes_to_an_existing_test_folder_deviations():
    d = _tree()
    try:
        with pytest.raises(miss.MissError, match="existing test folder"):
            miss.log(d, [dict(ROW, location="model", deviations="tests/X/DEVIATIONS.md")])
        os.makedirs(os.path.join(d, "tests", "X"))
        miss.log(d, [dict(ROW, location="model", deviations="tests/X/DEVIATIONS.md")])
        t = open(os.path.join(d, "tests/X/DEVIATIONS.md"), encoding="utf-8").read()
        assert "| `ZZ-TEST` |" in t and "R2" in t
        assert "ZZ-TEST" in miss.existing_ids(d)
    finally:
        shutil.rmtree(d)


def test_correction_commit_without_a_row_fails_and_with_one_passes():
    d = _tree()
    try:
        g = lambda *a: subprocess.run(["git", *a], cwd=d, check=True, capture_output=True)
        c = ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m"]
        g("init", "-q")
        g(*c, "base")
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True, text=True).stdout.strip()
        g(*c, "Add a page")
        assert miss.corrections_without_rows(d, base) == []
        g(*c, "Fix the count on the front page")
        assert len(miss.corrections_without_rows(d, base)) == 1
        g(*c, "Correct the cite\n\nLogged as FORGE-GATE-1.")
        g(*c, "fix: typo\n\nMiss: none (a typo caught before review)")
        assert len(miss.corrections_without_rows(d, base)) == 1
    finally:
        shutil.rmtree(d)


# ---------------------------------------------------------------- every logged process miss has a FAILURES row
def _logged_tree():
    d = _tree()
    os.makedirs(os.path.join(d, "NOTES"))
    shutil.copy(os.path.join(ROOT, "NOTES", "MISSES-LEDGER.md"), os.path.join(d, "NOTES", "MISSES-LEDGER.md"))
    return d


def test_logged_process_misses_pass_on_the_repo():
    assert miss.logged_without_row(ROOT) == []


def test_a_misses_ledger_process_row_with_no_failures_row_fails():
    d = _logged_tree()
    p = os.path.join(d, miss.FAILURES)
    t = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(t.replace("(MISSES-LEDGER S7)", ""))
    bad = miss.logged_without_row(d)
    shutil.rmtree(d)
    assert len(bad) == 1 and "S7 is a process miss" in bad[0]


def test_a_research_miss_row_is_not_required():
    d = _logged_tree()
    bad = miss.logged_without_row(d)
    shutil.rmtree(d)
    assert not [b for b in bad if " M1 " in b]


def test_a_deviations_row_located_in_process_needs_a_failures_row():
    d = _logged_tree()
    os.makedirs(os.path.join(d, "tests", "X"))
    dev = os.path.join(d, "tests", "X", "DEVIATIONS.md")
    open(dev, "w", encoding="utf-8").write(
        "| prediction_id | locked_prediction | outcome | miss | location | stake_x_info | update | breach_check |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| `X-P1` | p | o | m | process | low | u | none |\n"
        "| `X-M1` | p | o | m | model | low | u | none |\n")
    bad = miss.logged_without_row(d)
    assert bad == ["tests/X/DEVIATIONS.md: X-P1 has location process and no FAILURES row"]
    miss.log(d, [dict(ROW, id="X-P1-PROC", outcome="see X-P1 in tests/X/DEVIATIONS.md")])
    assert miss.logged_without_row(d) == []
    shutil.rmtree(d)
