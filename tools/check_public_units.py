#!/usr/bin/env python3
"""Public formulas carry a units line (stdlib only).

Added 27 November 2026 after UNITS-PUBLIC-1 (process/FAILURES.md): a formula from
applications/GROK_BOT_MEMORY_2026-11-23.md went public with one symbol in two units.

A formula block that has gone public is marked in its page with
`<!-- public-formula: <where it was posted> -->` and closed with `<!-- /public-formula -->`.
The two marks may sit at the ends of lines, so the page's line numbers do not move. Every
marked block must contain a line part that starts `Units:` naming the units of its symbols.
Scanned: every .md file under applications/ and theory/applications/ (the second after the
layout move). Fails on a marked block with no `Units:`, and on an opening mark with no close.

Run from the repo root:  python3 tools/check_public_units.py
Exit 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import glob
import os
import re
import sys

OPEN = re.compile(r"<!--\s*public-formula\b(?!\s*-->)[^>]*-->")
CLOSE = re.compile(r"<!--\s*/public-formula\s*-->")
UNITS = re.compile(r"(?:^|[\s(])Units:")
DIRS = ("applications", os.path.join("theory", "applications"))


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_text(text, where):
    """Failure strings for one page."""
    out = []
    start = None
    body = []
    for ln, line in enumerate(text.splitlines(), 1):
        o, c = OPEN.search(line), CLOSE.search(line)
        if o and start is not None:
            out.append("%s:%d: public-formula block opened inside the block opened at line %d" % (where, ln, start))
        if o:
            start, body = ln, [line[o.end():]]
            if c and c.start() > o.end():
                body = [line[o.end():c.start()]]
            else:
                continue
        elif start is not None:
            body.append(line[:c.start()] if c else line)
        if c and start is not None:
            if not any(UNITS.search(b) for b in body):
                out.append("%s:%d: public-formula block (lines %d-%d) has no 'Units:' line" % (where, start, start, ln))
            start, body = None, []
    if start is not None:
        out.append("%s:%d: public-formula block is never closed (<!-- /public-formula -->)" % (where, start))
    return out


def check(root):
    out = []
    for d in DIRS:
        for p in sorted(glob.glob(os.path.join(root, d, "**", "*.md"), recursive=True)):
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            out += check_text(open(p, encoding="utf-8").read(), rel)
    return out


def main(argv=None):
    root = repo_root()
    fails = check(root)
    for f in fails:
        print("  FAIL units: " + f)
    print("public formulas: %d FAIL(s)" % len(fails))
    print("RESULT:", "PASS" if not fails else "FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
