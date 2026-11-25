#!/usr/bin/env python3
"""Banned-word lint for maintained docs and for every line a change adds (stdlib only).

Words: puzzle, bill, kill, dead, verdict (and their plain forms: puzzles, bills,
billed, billing, kills, killed, killing, verdicts). GTAO says miss, cost, open
question, result, and outcome instead (process/PROCESS.md section 2).

Two checks, both run from tools/check_consistency.py:

  A. `puzzle` anywhere in a maintained doc fails (the maintained docs are clean
     after the 24 November 2026 sweep);
  B. any line ADDED to a `.md` file, compared with `origin/main`, that contains one
     of the five words fails. Old lines are not rescanned (many dated records
     use "kill rule" as a locked-test term); a changed line counts as added.

Exempt: text inside backticks, straight double quotes or curly quotes (the word is
quoted, not used); a line with `<!-- banned-ok: reason -->` (reviewable escape);
and, in process/PROCESS.md, process/VOCABULARY.md and process/FAILURES.md only,
table rows, lines that list two or more of the words, and lines that say the
word is banned.
"""
from __future__ import annotations

import os
import re
import subprocess

WORD = re.compile(r"\b(puzzles?|bills?|billed|billing|kill(?:s|ed|ing)?|dead|verdicts?)\b", re.I)
PUZZLE = re.compile(r"\bpuzzles?\b", re.I)
QUOTED = re.compile(r"`[^`]*`|\"[^\"]*\"|“[^”]*”|‘[^’]*’")
ESCAPE = re.compile(r"<!--\s*banned-ok:\s*\S.*?-->")
RULE_FILES = {"process/PROCESS.md", "process/VOCABULARY.md", "process/FAILURES.md"}
RULE_SAYS = re.compile(r"\b(banned|bans?|never say|do not say|don't say|not say|wording rule|no \w+ wording)\b", re.I)


def unquoted(line):
    return QUOTED.sub(" ", line)


def hits(line, path=""):
    """The banned words used (not quoted) on this line, or []."""
    if ESCAPE.search(line):
        return []
    found = [m.group(0).lower() for m in WORD.finditer(unquoted(line))]
    if not found:
        return []
    if path in RULE_FILES:
        distinct = {re.sub(r"(s|ed|ing)$", "", f) for f in found}
        if line.lstrip().startswith("|") or len(distinct) >= 2 or RULE_SAYS.search(line):
            return []
    return found


def puzzle_hits(line, path=""):
    if ESCAPE.search(line):
        return []
    if path in RULE_FILES and (line.lstrip().startswith("|") or RULE_SAYS.search(line)):
        return []
    return [m.group(0).lower() for m in PUZZLE.finditer(unquoted(line))]


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def base_ref(root):
    """origin/main if present, else None (shallow or detached checkouts)."""
    r = git(root, "rev-parse", "--verify", "-q", "origin/main")
    return "origin/main" if r.returncode == 0 else None


def added_lines(root, base):
    """{path: [(lineno, text)]} for .md lines added or changed since the merge base with `base`,
    including uncommitted edits."""
    mb = git(root, "merge-base", "HEAD", base)
    if mb.returncode != 0:
        return None
    r = git(root, "diff", "-U0", "--no-color", mb.stdout.strip(), "--", "*.md")
    if r.returncode != 0:
        return None
    out, path, ln = {}, None, 0
    for line in r.stdout.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("@@"):
            m = re.match(r"@@ -\S+ \+(\d+)", line)
            ln = int(m.group(1)) if m else 0
        elif line.startswith("+") and not line.startswith("+++") and path:
            out.setdefault(path, []).append((ln, line[1:]))
            ln += 1
    return out


def check_added(root, base=None):
    """(fails, note). note is a string when the comparison could not run."""
    base = base or base_ref(root)
    if base is None:
        return [], "banned-word check on added lines skipped: no origin/main to compare with (run `git fetch origin main`)"
    added = added_lines(root, base)
    if added is None:
        return [], "banned-word check on added lines skipped: could not diff against %s" % base
    fails = []
    for path, rows in sorted(added.items()):
        for ln, text in rows:
            h = hits(text, path)
            if h:
                fails.append("banned word %s added at %s:%d: %s" % (sorted(set(h)), path, ln, text.strip()[:140]))
    return fails, None


def check_puzzle(root, maintained):
    fails = []
    for p in maintained:
        fp = os.path.join(root, p)
        if not os.path.exists(fp):
            continue
        for i, text in enumerate(open(fp, encoding="utf-8", errors="replace"), 1):
            if puzzle_hits(text, p):
                fails.append("puzzle in maintained doc %s:%d: %s" % (p, i, text.strip()[:140]))
    return fails
