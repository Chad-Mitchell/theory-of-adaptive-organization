#!/usr/bin/env python3
"""Fail if STATUS.md's stated main SHA has drifted too far from HEAD.

The stated SHA is the current-pointer form (`main` is `abc1234`). It must
be one of the last 5 first-parent commits of HEAD (HEAD itself counts).
That window is wide enough for a short PR branch or a couple of merges
before the pointer is rewritten, and tight enough to catch the failure
mode where STATUS still said a65b64e after five later first-parent
merges.

Run from the repo root:  python3 tools/check_fresh.py
Exit 0 = the pointer is in the window (or the tree is not a git repo
and this check is skipped with a message). Exit 1 = stale or unparsable
when git is present.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

# Same current-pointer family as tools/brief.py, but this check only
# cares about the "main is SHA" form in STATUS.md.
STATUS_MAIN_RE = re.compile(
    r"`main`\s+is\s+`([0-9a-f]{7,40})`|main\s+is\s+`?([0-9a-f]{7,40})`?",
    re.I,
)

WINDOW = 5


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )


def stated_main_sha(text):
    """Return the first 'main is SHA' pointer in STATUS.md, or None."""
    m = STATUS_MAIN_RE.search(text)
    if not m:
        return None
    return next(g for g in m.groups() if g)


def first_parent_window(root, head="HEAD", n=WINDOW):
    r = git(root, "rev-list", "--first-parent", "-n", str(n), head)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "git rev-list failed")
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


def expand_sha(root, short):
    r = git(root, "rev-parse", "--verify", short + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def is_git_repo(root):
    r = git(root, "rev-parse", "--is-inside-work-tree")
    return r.returncode == 0 and r.stdout.strip() == "true"


def check(root=None, window=WINDOW):
    """Return a list of failure strings (empty means pass)."""
    root = root or repo_root()
    path = os.path.join(root, "STATUS.md")
    if not os.path.exists(path):
        return ["freshness: STATUS.md is missing"]
    text = open(path, encoding="utf-8").read()
    stated = stated_main_sha(text)
    if not stated:
        return ["freshness: STATUS.md has no 'main is SHA' pointer"]
    if not is_git_repo(root):
        # Mutation copies used by tools/test_check_consistency.py have no
        # .git; skip rather than fail those clean-copy checks.
        return []
    full = expand_sha(root, stated)
    if not full:
        return ["freshness: STATUS.md main SHA %s is not a commit in this repo" % stated]
    try:
        window_shas = first_parent_window(root, "HEAD", window)
    except RuntimeError as e:
        return ["freshness: %s" % e]
    if full not in window_shas:
        return [
            "freshness: STATUS.md main is %s, which is not among the last %d "
            "first-parent commits of HEAD (%s)"
            % (stated, window, " ".join(s[:7] for s in window_shas))
        ]
    return []


def main(argv=None):
    argv = sys.argv if argv is None else argv
    root = argv[1] if len(argv) > 1 else repo_root()
    if not is_git_repo(root):
        print("freshness: not a git work tree; skipped")
        print("RESULT: PASS")
        return 0
    fails = check(root)
    if fails:
        for f in fails:
            print("  FAIL " + f)
        print("RESULT: FAIL")
        return 1
    stated = stated_main_sha(open(os.path.join(root, "STATUS.md"), encoding="utf-8").read())
    window_shas = first_parent_window(root, "HEAD", WINDOW)
    print("STATUS.md main is %s; window: %s" % (stated, " ".join(s[:7] for s in window_shas)))
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
