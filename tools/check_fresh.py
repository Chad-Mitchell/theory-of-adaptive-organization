#!/usr/bin/env python3
"""Fail if STATUS.md's stated main SHA has drifted too far from main.

The stated SHA is the current-pointer form (`main` is `abc1234`). It must
be one of the last 5 first-parent commits of a main ref: origin/main,
upstream/main when that remote exists, else local main, else HEAD. Either
window is enough, so a fork whose origin/main is behind an upstream main
the branch merged still passes. The width is wide enough for a few merges
before the pointer is rewritten, and tight enough that a65b64e fails once
the six later first-parent merges through #114 are on main.

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
    r"`main`\s+is\s+`([0-9a-f]{7,40})`|"
    r"\bmain\s+is\s+(?:`([0-9a-f]{7,40})`|([0-9a-f]{7,40})\b)",
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
    # A nested copy has no .git of its own. git would walk up to the
    # parent repo and grade that copy against the parent HEAD.
    if not os.path.exists(os.path.join(root, ".git")):
        return False
    r = git(root, "rev-parse", "--is-inside-work-tree")
    return r.returncode == 0 and r.stdout.strip() == "true"


def history_tips(root):
    """Refs whose first-parent history the STATUS pointer may match.

    Prefer origin/main, then upstream/main, then local main, then HEAD.
    A fork clone's origin/main can sit behind the upstream main a branch
    has merged. The pointer is fresh if it is in either window. Commits
    that exist only on a feature branch are not main moving. Five of them
    push a correct main SHA out of a HEAD window. PRs #114 and #133–#137
    were 7–10 first-parent commits.
    """
    tips = []
    for ref in (
        "refs/remotes/origin/main",
        "refs/remotes/upstream/main",
        "refs/heads/main",
    ):
        r = git(root, "rev-parse", "--verify", ref)
        if r.returncode == 0:
            sha = r.stdout.strip()
            if sha not in tips:
                tips.append(sha)
    return tips or ["HEAD"]


def history_tip(root):
    """First main ref. Kept for the one-line status print."""
    return history_tips(root)[0]


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
    tips = history_tips(root)
    windows = []
    try:
        for tip in tips:
            windows.append((tip, first_parent_window(root, tip, window)))
    except RuntimeError as e:
        return ["freshness: %s" % e]
    if any(full in shas for _, shas in windows):
        return []
    tip, window_shas = windows[0]
    return [
        "freshness: STATUS.md main is %s, which is not among the last %d "
        "first-parent commits of %s (%s)"
        % (stated, window, tip[:7], " ".join(s[:7] for s in window_shas))
    ]


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
    full = expand_sha(root, stated)
    matched = None
    for tip in history_tips(root):
        window_shas = first_parent_window(root, tip, WINDOW)
        if full in window_shas:
            matched = (tip, window_shas)
            break
    tip, window_shas = matched
    print(
        "STATUS.md main is %s; window of %s: %s"
        % (stated, tip[:7], " ".join(s[:7] for s in window_shas))
    )
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
