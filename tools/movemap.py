#!/usr/bin/env python3
"""The one move map of the 27 Nov 2026 layout: old path prefix -> new path prefix, in the order of the move plan.

Every check that compares paths across the move imports this module, so the map has one home. Until the move lands
nothing here changes any file: forward() and backward() are the identity on paths the map does not name, and on a
tree that has not moved, forward(p) simply names where p will go.

  forward(path)      old repository path -> new path
  backward(path)     new path -> old path
  rewrite(text)      every root-relative mention of an old path -> the new path (relative `../` paths are left alone:
                     they are rewritten per file by the move PR, which knows each file's folder)
  unrewrite(text)    the inverse of rewrite on text that names no new path
  resolve_lock_line(lock_file, line_path)
                     a hash line is relative to its lock file's folder before the move; resolve it there, then map it

  python3 tools/movemap.py --check                      the map is one-to-one and round-trips
  python3 tools/movemap.py --verify-rewrite BASE FILE…   each FILE at HEAD equals rewrite(its BASE bytes): a path-only change
"""
from __future__ import annotations

import os
import posixpath
import re
import subprocess
import sys

# (old, new). A prefix ending in "/" is a folder; one without is a file, or a file-name prefix (figures/face).
MOVES = (
    ("reviews/night1/formal/", "theory/axioms/"),
    ("theory/SWARM_RULE_2026-11-23.md", "theory/swarm/SWARM_RULE.md"),
    ("theory/swarm_checks/", "theory/swarm/checks/"),
    ("applications/", "theory/applications/"),
    ("core/KEYSTONE_NOTE.md", "theory/KEYSTONE_NOTE.md"),
    ("core/bridge_2026-11-21/", "theory/bridge_2026-11-21/"),
    ("core/keystone_checks/", "theory/keystone_checks/"),
    ("core/sim1_2026-11-21/", "theory/sim1_2026-11-21/"),
    ("theory/reviews/", "records/reviews/theory/"),
    ("reviews/", "records/reviews/"),
    ("night2/", "records/night2/"),
    ("NOTES/", "records/notes/"),
    ("reference/", "records/reference/"),
    ("tests/", "records/tests/"),
    ("prereg/", "records/prereg/"),
    ("drafts/PIN_DRAFT.md", "process/drafts/PIN_DRAFT.md"),
    ("figures/derivation_map.png", "records/figures/derivation_map.png"),
    ("figures/derivation_map.py", "records/figures/derivation_map.py"),
    ("figures/face", "records/figures/face"),
)
_FWD = sorted(MOVES, key=lambda m: -len(m[0]))
_BWD = sorted(((n, o) for o, n in MOVES), key=lambda m: -len(m[0]))


def _norm(p):
    p = p.replace(os.sep, "/")
    return p[2:] if p.startswith("./") else p


def _map(path, table):
    p = _norm(path)
    for a, b in table:
        if p == a.rstrip("/") and a.endswith("/"):
            return b.rstrip("/")
        if p.startswith(a):
            return b + p[len(a):]
    return p


def forward(path):
    return _map(path, _FWD)


def backward(path):
    return _map(path, _BWD)


_LEAD = r"(?<![\w./\-])"


def _rx(table):
    return re.compile(_LEAD + "(" + "|".join(re.escape(a) for a, _ in table) + ")")


_RX_F, _RX_B = _rx(_FWD), _rx(_BWD)


def _sub(text, rx, table):
    d = dict(table)
    return rx.sub(lambda m: d[m.group(1)], text)


def rewrite(text):
    return _sub(text, _RX_F, _FWD)


def unrewrite(text):
    return _sub(text, _RX_B, _BWD)


def resolve_lock_line(lock_file, line_path):
    """Candidate repository paths for a hash line, in order: as written relative to the lock file's present folder,
    as root-relative, then both against the lock file's pre-move folder, mapped forward."""
    p = _norm(line_path)
    here = posixpath.dirname(_norm(lock_file))
    old = posixpath.dirname(backward(lock_file))
    out = []
    for c in (posixpath.normpath(posixpath.join(here, p)), posixpath.normpath(p),
              forward(posixpath.normpath(posixpath.join(old, p))), forward(posixpath.normpath(p))):
        if c not in out:
            out.append(c)
    return out


def check_map():
    """[problems] with the map itself: duplicate sources or targets, or a path that does not round-trip."""
    errs = []
    olds, news = [o for o, _ in MOVES], [n for _, n in MOVES]
    for name, xs in (("source", olds), ("target", news)):
        dup = {x for x in xs if xs.count(x) > 1}
        if dup:
            errs.append("duplicate %s prefix: %s" % (name, sorted(dup)))
    for o, n in MOVES:
        probe = o + ("x/y.md" if o.endswith("/") else "")
        if forward(probe) != n + ("x/y.md" if o.endswith("/") else ""):
            errs.append("forward(%s) = %s, expected under %s" % (probe, forward(probe), n))
        if backward(forward(probe)) != probe:
            errs.append("%s does not round-trip (got %s)" % (probe, backward(forward(probe))))
    return errs


def verify_rewrite(root, base, files):
    """[(file, ok)]: ok when the file at HEAD equals rewrite() of its pre-move version at base."""
    out = []
    for f in files:
        old = backward(f)
        b = subprocess.run(["git", "show", "%s:%s" % (base, old)], cwd=root, capture_output=True)
        now = open(os.path.join(root, f), encoding="utf-8", errors="surrogateescape").read() if os.path.isfile(
            os.path.join(root, f)) else None
        ok = b.returncode == 0 and now is not None and rewrite(b.stdout.decode("utf-8", "surrogateescape")) == now
        out.append((f, ok))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if argv[:1] == ["--verify-rewrite"] and len(argv) >= 3:
        res = verify_rewrite(root, argv[1], argv[2:])
        for f, ok in res:
            print("  %s %s" % ("OK  " if ok else "FAIL", f))
        bad = [f for f, ok in res if not ok]
        print("movemap: %d path-only, %d not; RESULT: %s" % (len(res) - len(bad), len(bad), "FAIL" if bad else "PASS"))
        return 1 if bad else 0
    errs = check_map()
    for e in errs:
        print("  FAIL " + e)
    print("movemap: %d moves; RESULT: %s" % (len(MOVES), "FAIL" if errs else "PASS"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
