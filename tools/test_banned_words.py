#!/usr/bin/env python3
"""Tests for tools/banned_words.py. Run: python3 -m pytest -q tools/test_banned_words.py"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import banned_words as bw  # noqa: E402


def test_each_word_is_caught():
    for w in ("puzzle", "puzzles", "bill", "billed", "kill", "killed", "dead", "verdict", "VERDICT"):
        assert bw.hits("This is a %s here." % w), w


def test_plain_words_are_not_caught():
    assert bw.hits("The miss is open; the cost is small; the outcome is a result.") == []
    assert bw.hits("Dedicated deadline, skilled billet.") == []


def test_quoted_and_backticked_are_exempt():
    assert bw.hits("Never say `puzzle` or \"kill\" or “dead” or ‘verdict’.") == []
    assert bw.hits("It is a \"quoted\" line, but the verdict is not.") == ["verdict"]


def test_escape_marker_needs_a_reason():
    assert bw.hits("kill rule <!-- banned-ok: locked-test term from the prereg -->") == []
    assert bw.hits("kill rule <!-- banned-ok: -->") == ["kill"]


def test_rule_files_exempt_tables_lists_and_ban_statements_only():
    assert bw.hits("| a | puzzle | b |", "process/PROCESS.md") == []
    assert bw.hits("| a | puzzle | b |", "STATUS.md") == ["puzzle"]
    assert bw.hits("Use no kill, verdict or puzzle wording.", "process/FAILURES.md") == []
    assert bw.hits("These words are banned: dead.", "process/VOCABULARY.md") == []
    assert bw.hits("It was a verdict.", "process/PROCESS.md") == ["verdict"]


def test_puzzle_check_ignores_rule_statements():
    assert bw.puzzle_hits("An open puzzle.", "STATUS.md") == ["puzzle"]
    assert bw.puzzle_hits("'puzzle' is banned.", "process/PROCESS.md") == []


def _git(cwd, *a):
    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def _repo(tmp_path):
    d = str(tmp_path)
    _git(d, "init", "-q", "-b", "main")
    open(os.path.join(d, "a.md"), "w").write("old kill rule stays\nplain\n")
    _git(d, "add", "-A"); _git(d, "commit", "-qm", "base")
    _git(d, "update-ref", "refs/remotes/origin/main", "HEAD")
    return d


def test_only_added_lines_fail(tmp_path):
    d = _repo(tmp_path)
    assert bw.check_added(d) == ([], None)          # old "kill" line is not rescanned
    with open(os.path.join(d, "a.md"), "a") as f:
        f.write("a new verdict line\nclean line\n")
    fails, note = bw.check_added(d)
    assert note is None and len(fails) == 1 and "a.md:3" in fails[0]


def test_changed_old_line_counts_as_added(tmp_path):
    d = _repo(tmp_path)
    open(os.path.join(d, "a.md"), "w").write("old kill rule stays, edited\nplain\n")
    fails, _ = bw.check_added(d)
    assert len(fails) == 1 and "a.md:1" in fails[0]


def test_committed_added_lines_fail_too(tmp_path):
    d = _repo(tmp_path)
    open(os.path.join(d, "b.md"), "w").write("the dead end\n")
    _git(d, "add", "-A"); _git(d, "commit", "-qm", "b")
    fails, _ = bw.check_added(d)
    assert len(fails) == 1 and "b.md:1" in fails[0]


def test_no_origin_main_is_reported_not_passed(tmp_path):
    d = str(tmp_path)
    _git(d, "init", "-q", "-b", "main")
    open(os.path.join(d, "a.md"), "w").write("x\n")
    _git(d, "add", "-A"); _git(d, "commit", "-qm", "base")
    fails, note = bw.check_added(d)
    assert fails == [] and note and "skipped" in note


def test_non_markdown_files_are_ignored(tmp_path):
    d = _repo(tmp_path)
    open(os.path.join(d, "x.py"), "w").write("# verdict\n")
    assert bw.check_added(d) == ([], None)


def test_maintained_docs_have_no_puzzle():
    import re
    s = open(os.path.join(ROOT, "tools", "check_consistency.py")).read()
    block = s[s.index("MAINTAINED = ["): s.index("MAINTAINED = [f for f")]
    files = re.findall(r'"([^"]+\.md)"', block)
    assert files and bw.check_puzzle(ROOT, files) == []
