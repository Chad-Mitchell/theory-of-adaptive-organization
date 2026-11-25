#!/usr/bin/env python3
"""Fail if a live page hand-keeps a fact that has another single source.

Since 25 November 2026 (history/2026-11-25_DRIFT_MEMO.md) no page carries the
current `main` SHA or the open-PR list: those change at every merge, so a
committed copy is stale as soon as it lands. `tools/brief.py` prints them live.
Versions have one source (the THEORY.md title, the latest CLAIM_MAP note) and the
Lean total has one (formal/lean/AUDIT.json). This check fails on a hand copy of
any of them on a live page. Text between `<!-- history:begin` and
`<!-- history:end -->` is a dated record and is skipped, as are the two
copies in files this repo may not edit (ALLOW).

Run from the repo root:  python3 tools/check_fresh.py
Exit 0 = no hand pointer. Exit 1 = at least one.
"""
import glob
import os
import re
import sys

LIVE = ["README.md", "ONE_PAGER.md", "OPEN_WORK.md", "CORE.md", "THEORY.md", "theory/README.md",
        "formal/lean/README.md", "measurement/FRAMEWORK.md", "applications/README.md"]
LIVE_GLOBS = ["process/*.md"]
SKIP = {"process/FAILURES.md"}  # append-only log of past states
SHA = r"`?[0-9a-f]{7,40}\b`?"
# "on/beside `main` `SHA`" is a pointer only in an As-of header; table rows use the words historically.
ASOF = re.compile(r"^\*\*As of:\*\*.*(?:\n(?!\n|#|\|).*)*", re.M)
ASOF_SHA = re.compile(r"(?:on|beside)\s+`main`\s+`[0-9a-f]{7,40}`", re.I)
RULES = [
    ("main SHA pointer", re.compile(r"`main`\s+is\s+" + SHA + r"|\bmain\s+is\s+" + SHA
                                    + r"|current to\s+`?\bmain\b`?\s+" + SHA, re.I)),
    ("open-PR list", re.compile(r"\bopen\s+(?:upstream\s+|fork\s+)?(?:PRs?|pull requests?)\b[^.\n]{0,40}?:\s*(?:PR\s*)?#\d+", re.I)),
    ("version string", re.compile(r"`?THEORY(?:\.md)?`?\s*\(?v\d+\.\d+(?:\.\d+)?[a-z]?\s+draft|`THEORY\.md`\s+v\d+\.\d+"
                                  r"|CLAIM_MAP_v2\.md`?\s*\(v2\.\d+|\(v\d+\.\d+(?:\.\d+)?[a-z]?\s+draft\)")),
    ("Lean total", re.compile(r"\*\*\d[\d,]*\s+declarations\*\*|machine-checks\s+\**\d[\d,]*", re.I)),
]
# Copies in files that may not be edited here; check_consistency.py keeps them equal to their source.
ALLOW = {
    ("CORE.md", "is the canonical statement (v"),
    ("THEORY.md", "Claim statuses: `measurement/CLAIM_MAP_v2.md` (v"),
}
HIST = re.compile(r"<!-- history:begin.*?<!-- history:end -->", re.S)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def live_pages(root):
    pages = [p for p in LIVE if os.path.isfile(os.path.join(root, p))]
    for g in LIVE_GLOBS:
        pages += sorted(os.path.relpath(p, root) for p in glob.glob(os.path.join(root, g)))
    return [p for p in pages if p not in SKIP]


def hand_pointers(text, path=""):
    """[(line number, rule, excerpt)] for hand-kept live facts in text."""
    text = HIST.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        for name, rx in RULES:
            m = rx.search(line)
            if not m or any(path == p and frag in line for p, frag in ALLOW):
                continue
            out.append((i, name, line[max(0, m.start() - 30):m.end() + 30].strip()))
    for para in ASOF.finditer(text):
        for m in ASOF_SHA.finditer(para.group(0)):
            out.append((text.count("\n", 0, para.start() + m.start()) + 1, "main SHA pointer", m.group(0)))
    return sorted(out)


def check(root=None):
    root = root or repo_root()
    fails = []
    for p in live_pages(root):
        with open(os.path.join(root, p), encoding="utf-8") as fh:
            for ln, name, ex in hand_pointers(fh.read(), p):
                fails.append("hand pointer (%s) at %s:%d: %s; read it live or from its one source" % (name, p, ln, ex))
    return fails


def main(argv=None):
    argv = sys.argv if argv is None else argv
    fails = check(argv[1] if len(argv) > 1 else None)
    for f in fails:
        print("  FAIL " + f)
    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
