#!/usr/bin/env python3
"""Every not-DONE queue item ID must appear in OPEN_WORK.md.

Run from the repo root:  python3 tools/check_open_work.py
Exit 0 = every not-DONE ID from history/2026-11-20_queue/QUEUE.md and history/2026-11-20_queue/queue/items.json
appears in OPEN_WORK.md as a whole token (so SENSE-CELL does not count as a
hit inside SENSE-CELL-MATCHED).

An items.json row is not-DONE when its status is missing or is not "DONE".
A QUEUE.md item is not-DONE unless its heading or bullet is marked DONE
(an em-dash "DONE", or the ID struck through as ~~**ID**~~). Q-headings
and leading bold IDs on bullets are collected; mid-sentence verdicts such
as PASS-WITH-FIXES are ignored.
"""
from __future__ import annotations

import json, os, re, sys

ROOT_FILES = ("history/2026-11-20_queue/QUEUE.md", "history/2026-11-20_queue/queue/items.json", "OPEN_WORK.md")

# All-caps verdict / label words that appear bold in QUEUE.md but are not item IDs.
NOT_IDS = {
    "DONE", "OPEN", "PASS", "FAIL", "FAILED", "PASSED", "KILL", "HIT",
    "INCONCLUSIVE", "INVALID", "UNTESTED", "PASS-WITH-FIXES",
    "READY-WITH-FIXES", "NOT-READY", "READY", "PROXY-PASS", "PROXY-FAIL",
    "NOT-EVIDENCE", "MATH-CORRECTED", "PRIOR-ART", "NEW", "RULE",
}

HEADING_RE = re.compile(r"^###\s+Q\d+\.\s+([A-Z][A-Z0-9_.-]+)\b(.*)$")
# Leading bullet ID: - **ID**  or  - ~~**ID**~~
BULLET_RE = re.compile(
    r"^-\s+(~~)?\*\*([A-Z][A-Z0-9][A-Z0-9_.-]*)\*\*(~~)?"
)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def items_not_done(items):
    """Return item IDs whose status is not the string DONE."""
    out = []
    for it in items:
        if it.get("status") != "DONE":
            out.append(it["id"])
    return out


def _is_done_suffix(rest: str) -> bool:
    # "— DONE", "- DONE", "DONE 18 Nov", struck-through already handled by caller
    return bool(re.search(r"(—\s*DONE|\bDONE\b)", rest))


def queue_entries(text: str):
    """Yield (id, done) for item IDs declared in QUEUE.md."""
    seen = set()
    for line in text.splitlines():
        m = HEADING_RE.match(line)
        if m:
            ident, rest = m.group(1), m.group(2)
            if ident in NOT_IDS:
                continue
            done = _is_done_suffix(rest)
            if ident not in seen:
                seen.add(ident)
                yield ident, done
            continue
        m = BULLET_RE.match(line.lstrip())
        if not m:
            continue
        struck, ident, struck2 = m.group(1), m.group(2), m.group(3)
        if ident in NOT_IDS:
            continue
        # Require a hyphen, or a later items.json check, happens in queue_not_done
        rest = line[m.end():]
        done = bool(struck or struck2) or _is_done_suffix(rest)
        if ident not in seen:
            seen.add(ident)
            yield ident, done


def queue_not_done(text: str, item_ids=None):
    """Not-DONE IDs from QUEUE.md.

    Keep a heading/bullet ID if it is in items.json, or it looks like a
    queue item (contains a hyphen) and is not a verdict label.
    """
    item_ids = set(item_ids or [])
    out = []
    for ident, done in queue_entries(text):
        if done:
            continue
        if ident in item_ids or ("-" in ident):
            out.append(ident)
    return out


def token_present(text: str, ident: str) -> bool:
    """True iff ident appears as a whole token, not as a prefix of a longer ID."""
    pat = re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(ident) + r"(?![A-Za-z0-9_-])")
    return bool(pat.search(text))


def missing_ids(open_work: str, queue_text: str, items) -> list:
    item_nd = items_not_done(items)
    queue_nd = queue_not_done(queue_text, [it["id"] for it in items])
    # Preserve a stable unique order: items.json order, then extra QUEUE IDs.
    ordered = list(item_nd)
    seen = set(item_nd)
    for ident in queue_nd:
        if ident not in seen:
            ordered.append(ident)
            seen.add(ident)
    return [ident for ident in ordered if not token_present(open_work, ident)]


def check(root=None):
    root = root or repo_root()
    queue = open(os.path.join(root, "history/2026-11-20_queue/QUEUE.md"), encoding="utf-8").read()
    items = json.load(open(os.path.join(root, "history/2026-11-20_queue/queue/items.json"), encoding="utf-8"))
    open_work = open(os.path.join(root, "OPEN_WORK.md"), encoding="utf-8").read()
    missing = missing_ids(open_work, queue, items)
    return missing, items_not_done(items), queue_not_done(queue, [it["id"] for it in items])


def main(argv=None):
    argv = sys.argv if argv is None else argv
    root = argv[1] if len(argv) > 1 else repo_root()
    os.chdir(root)
    missing, item_nd, queue_nd = check(root)
    print("items.json not-DONE: %d; QUEUE.md not-DONE: %d; union missing from OPEN_WORK.md: %d"
          % (len(item_nd), len(queue_nd), len(missing)))
    if missing:
        for ident in missing:
            print("  MISSING " + ident)
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
