#!/usr/bin/env python3
"""Tests for tools/check_pending.py (offline; the GitHub API is faked).

Run:  python3 -m pytest -q tools/test_check_pending.py
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_pending as cp  # noqa: E402

NOW = datetime(2026, 11, 26, 12, 0, tzinfo=timezone.utc)


def ts(hours_ago):
    return (NOW - timedelta(hours=hours_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- (b) Lean
def _lean_tree(tmp_path, status_count=10, record=10):
    root = tmp_path / "r"
    (root / "formal" / "lean" / "GTAO").mkdir(parents=True)
    (root / "formal" / "lean" / "GTAO.lean").write_text("import GTAO.A\n")
    (root / "formal" / "lean" / "GTAO" / "A.lean").write_text("theorem t : True := trivial\n")
    (root / "STATUS.md").write_text("machine-checks **%d declarations** (AxiomAudit)\n" % status_count)
    if record is not None:
        cp.record_audit(str(root), record, commit="abc1234")
    return root


def test_real_repo_lean_count_matches_audit():
    assert cp.check_lean(ROOT) == []


def test_lean_count_match_passes(tmp_path):
    root = _lean_tree(tmp_path)
    assert cp.check_lean(str(root)) == []


def test_status_count_mismatch_fails(tmp_path):
    # The 24 November miss: STATUS kept 757 after the audit count moved.
    root = _lean_tree(tmp_path, status_count=757, record=1185)
    fails = cp.check_lean(str(root))
    assert any("757" in f and "1185" in f for f in fails)


def test_lean_source_change_without_new_audit_fails(tmp_path):
    root = _lean_tree(tmp_path)
    (root / "formal" / "lean" / "GTAO" / "B.lean").write_text("theorem u : True := trivial\n")
    fails = cp.check_lean(str(root))
    assert any("sources changed" in f for f in fails)


def test_missing_audit_file_fails(tmp_path):
    root = _lean_tree(tmp_path, record=None)
    assert any("AUDIT.json is missing" in f for f in cp.check_lean(str(root)))


def test_status_without_lean_total_fails(tmp_path):
    root = _lean_tree(tmp_path)
    (root / "STATUS.md").write_text("no total here\n")
    assert any("no '**N declarations**'" in f for f in cp.check_lean(str(root)))


def test_status_count_parses_commas():
    assert cp.status_lean_count("checks **1,185 declarations** today") == 1185


# ---------------------------------------------------------------- (a) OPEN_WORK
def _git(repo, *a):
    e = dict(os.environ, GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@e", GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@e")
    r = subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True, env=e)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def _repo(tmp_path, n):
    repo = str(tmp_path / "g")
    os.makedirs(repo)
    _git(repo, "init", "-b", "main")
    shas = []
    for i in range(n):
        open(os.path.join(repo, "f%d" % i), "w").write(str(i))
        _git(repo, "add", ".")
        _git(repo, "commit", "-m", str(i))
        shas.append(_git(repo, "rev-parse", "HEAD"))
    return repo, shas


def test_open_work_pointer_in_window_passes(tmp_path):
    repo, shas = _repo(tmp_path, 4)
    open(os.path.join(repo, "STATUS.md"), "w").write("`main` is `%s`\n" % shas[-1][:7])
    open(os.path.join(repo, "OPEN_WORK.md"), "w").write("# OW\n\n**As of:** x, on `main` `%s` (PR #1).\n" % shas[0][:7])
    assert cp.check_pointers(repo) == []


def test_open_work_pointer_out_of_window_fails(tmp_path):
    repo, shas = _repo(tmp_path, cp.OPEN_WORK_WINDOW + 2)
    open(os.path.join(repo, "STATUS.md"), "w").write("`main` is `%s`\n" % shas[-1][:7])
    open(os.path.join(repo, "OPEN_WORK.md"), "w").write("# OW\n\n**As of:** x, on `main` `%s`.\n" % shas[0][:7])
    fails = cp.check_pointers(repo)
    assert any("OPEN_WORK.md header" in f for f in fails)


# ---------------------------------------------------------------- (c) pending
def _pr(repo, n, title, head_ref, head_sha, base_ref, created, owner=None):
    owner = owner or repo.split("/")[0]
    return {"number": n, "title": title, "created_at": created,
            "head": {"ref": head_ref, "sha": head_sha, "repo": {"owner": {"login": owner}, "full_name": "%s/x" % owner}},
            "base": {"ref": base_ref, "repo": {"owner": {"login": repo.split("/")[0]}}}}


def fake_api(review_text, review_age_h, comments=None, upstream=None):
    fork = cp.FORK
    pulls = {
        cp.UPSTREAM: upstream or [],
        fork: [
            _pr(fork, 30, "Lean batch 2", "batch2", "6663d0e" + "0" * 33, "batch1", ts(30)),
            _pr(fork, 32, "Independent review of Lean batch 2", "batch2-review", "295c968" + "0" * 33, "batch2", ts(review_age_h)),
        ],
    }
    content = base64.b64encode(review_text.encode()).decode()

    def api(path):
        if "/pulls?state=open" in path:
            return pulls[path.split("/repos/")[1].split("/pulls")[0]]
        if path.endswith("/pulls/32/files?per_page=100"):
            return [{"filename": "formal/lean/reviews/BATCH2_REVIEW.md", "status": "added"}]
        if "/contents/" in path:
            return {"content": content}
        if "/comments" in path:
            return (comments or {}).get(path, [])
        return []
    return api


def test_reviewed_unmerged_over_24h_is_listed():
    api = fake_api("Reviewed head `caea9c0` on x.\n\nBlockers remaining: 0\n", 30)
    items = cp.pending_items(api, now=NOW)
    assert len(items) == 1 and "#30" in items[0] and "head moved" in items[0]


def test_reviewed_under_24h_is_not_listed():
    api = fake_api("Reviewed head `6663d0e` on x.\n\nBlockers remaining: 0\n", 3)
    assert cp.pending_items(api, now=NOW) == []


def test_review_with_blockers_is_not_listed():
    api = fake_api("Reviewed head `6663d0e`.\n\nBlockers remaining: 2\n", 30)
    assert cp.pending_items(api, now=NOW) == []


def test_latest_review_governs():
    # An old passing review is superseded by a later comment with a blocker.
    path = "/repos/%s/issues/30/comments?per_page=100" % cp.FORK
    api = fake_api("Blockers remaining: 0\n", 40, comments={path: [{"body": "Blockers remaining: 1", "created_at": ts(26)}]})
    assert cp.pending_items(api, now=NOW) == []


def test_passing_review_comment_counts():
    path = "/repos/%s/issues/30/comments?per_page=100" % cp.FORK
    api = fake_api("no result line\n", 40, comments={path: [{"body": "Head `6663d0e`\nBlockers remaining: 0", "created_at": ts(25), "html_url": "u"}]})
    items = cp.pending_items(api, now=NOW)
    assert len(items) == 1 and "head moved" not in items[0]


def test_no_network_is_a_warning_not_a_failure():
    def api(path):
        raise cp.Offline("no network")
    fails, warns = cp.check_pending_work(api)
    assert fails == [] and warns and "skipped" in warns[0]


def test_api_error_is_a_warning_not_a_failure():
    def api(path):
        raise OSError("boom")
    fails, warns = cp.check_pending_work(api)
    assert fails == [] and "skipped" in warns[0]
