#!/usr/bin/env python3
"""The 27 Nov 2026 layout move, driven by tools/movemap.py, run on a clean checkout of the latest main.

  python3 tools/move_layout.py --renames     step 1: every tracked file p goes to movemap.forward(p); bytes unchanged
  python3 tools/move_layout.py --refs BASE   step 2: rewrite path references in editable files (paths only)
  python3 tools/move_layout.py --readmes BASE step 3: write records/README.md (pins BASE) and theory/swarm/README.md

Step 2 edits a file only when it is not locked, not under records/, not THEORY.md (frozen in place) and not a lock or
data file. In a Markdown file each link target and backticked path is resolved the way a reader would (relative to the
file's folder, else from the root) on the BASE tree; if that file or folder moved, or the citing file moved, the
reference is rewritten to the new location, relative if it was relative. In code, root-relative path strings are
rewritten with movemap.rewrite. A reference that resolved to nothing is left as it was.
"""
import os
import posixpath
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import movemap  # noqa: E402

EDIT_EXT = (".md", ".py", ".sh", ".txt", ".lean", ".json", ".toml", ".cfg", ".yml", ".yaml")
NEVER = re.compile(r"(\.sha256$|SHA256SUMS|/LOCKED_BLOBS\.txt$|\.out$|\.log$|\.csv$|\.tsv$)")
MDREF = re.compile(r"(\]\(<?|`)([A-Za-z0-9_.\-~/]+(?:\.[A-Za-z0-9]+|/))((?:#[^)`>\s]*)?)(?=[>)`]|\s)")
CODEREF = re.compile(r"""(["'])([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+/?)\1""")


def git(*a, **k):
    return subprocess.run(["git", *a], cwd=ROOT, check=True, capture_output=True, text=True, **k).stdout


def renames():
    assert not git("status", "--porcelain").strip(), "clean tree only"
    files = git("ls-files", "-z").split("\0")
    n = 0
    for p in files:
        if not p:
            continue
        q = movemap.forward(p)
        if q == p:
            continue
        assert not os.path.exists(os.path.join(ROOT, q)), "target exists: " + q
        os.makedirs(os.path.dirname(os.path.join(ROOT, q)), exist_ok=True)
        os.rename(os.path.join(ROOT, p), os.path.join(ROOT, q))
        n += 1
    for d, _sub, _f in sorted(os.walk(ROOT), key=lambda t: -len(t[0])):
        if ".git" not in d.split(os.sep) and d != ROOT and not os.listdir(d):
            os.rmdir(d)
    git("add", "-A")
    print("moved %d files" % n)


def _locked(base):
    import facts
    return {movemap.forward(p) for p in facts.locked_paths(ROOT)}


def editable(newp, locked):
    return (newp.endswith(EDIT_EXT) and not NEVER.search(newp) and not newp.startswith("records/")
            and newp != "THEORY.md" and newp not in locked)


def _exists_old(base_files, base_dirs, t):
    t = t.rstrip("/")
    return t in base_files or t in base_dirs


def new_md_ref(s, old_file, new_file, base_files, base_dirs):
    """The rewritten reference, or None to keep s."""
    if s.startswith(("http", "/", "~")):
        return None
    rel_old = posixpath.normpath(posixpath.join(posixpath.dirname(old_file), s))
    root_old = posixpath.normpath(s)
    slash = "/" if s.endswith("/") else ""
    if not rel_old.startswith("..") and _exists_old(base_files, base_dirs, rel_old):
        target, relative = rel_old, True
    elif not root_old.startswith("..") and _exists_old(base_files, base_dirs, root_old):
        target, relative = root_old, False
    else:
        return None
    nt = movemap.forward(target)
    if relative:
        if nt == target and new_file == old_file:
            return None
        out = posixpath.relpath(nt, posixpath.dirname(new_file) or ".")
    else:
        if nt == target:
            return None
        out = nt
    out += slash
    return None if out == s else out


def refs(base):
    base_files = set(git("ls-tree", "-r", "--name-only", base).split("\n")) - {""}
    base_dirs = set()
    for f in base_files:
        d = posixpath.dirname(f)
        while d and d not in base_dirs:
            base_dirs.add(d)
            d = posixpath.dirname(d)
    locked = _locked(base)
    changed = 0
    for newp in git("ls-files").split("\n"):
        if not newp or not editable(newp, locked):
            continue
        oldp = movemap.backward(newp)
        path = os.path.join(ROOT, newp)
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if newp.endswith(".md"):
            def sub(m):
                r = new_md_ref(m.group(2), oldp, newp, base_files, base_dirs)
                return m.group(0) if r is None else m.group(1) + r + m.group(3)
            new = MDREF.sub(sub, text)
            # bare root-relative paths in prose and table cells (ledger sources, edges)
            new = movemap.rewrite(new)
        else:
            new = movemap.rewrite(text)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print("rewrote references in %d files" % changed)


RECORDS_README = """# Records

Frozen material: dated runs, preregistrations and their data, reviews, lab notes, the night-2 run, the v1.4.29 theory
and earlier figure views. Nothing here is edited; the ledger (`measurement/CLAIM_MAP_v2.md`) cites it, and the hash
locks under it are checked by `tools/verify_locks.py`.

**Moved on 27 November 2026.** These trees moved here from the top of the repository in one rename-only commit. The
one map from old path to new path is [`tools/movemap.py`](../tools/movemap.py) (`MOVES`); every check reads it.
Links written inside these files before the move use the old paths and resolve at the last commit before the move:
<https://github.com/Chad-Mitchell/theory-of-adaptive-organization/tree/{base}>. To follow an old link by hand, apply
the map to its path.

| folder | what it holds |
|---|---|
| [`tests/`](tests/) | field and simulation tests (index: [`tests/README.md`](tests/README.md), frozen) |
| [`prereg/`](prereg/) | field preregistrations and their data |
| [`reviews/`](reviews/) | dated reviews (index: [`reviews/README.md`](reviews/README.md), frozen); `reviews/theory/` holds the reviews that sat under `theory/` |
| [`notes/`](notes/) | lab notes |
| [`night2/`](night2/) | the night-2 run |
| [`reference/`](reference/) | the theory as it stood at v1.4.29 |
| [`figures/`](figures/) | earlier figure views, off the front page |
"""

SWARM_README = """# The swarm rule

How parts of a whole join, stay, leave and regroup, as one use of the cost of judgment. The status of each clause is
its ledger row (`SWARM-*` in [`measurement/CLAIM_MAP_v2.md`](../../measurement/CLAIM_MAP_v2.md)); this page only
indexes.

| file | what it is |
|---|---|
| [`SWARM_RULE.md`](SWARM_RULE.md) | the rule, its clauses and the results it reuses |
| [`checks/`](checks/) | the rule's numeric checks (`swarm_checks.py`, run by `tools/test_swarm_checks.py`) |
| [`../swarm-2026-11-27/INDEX.md`](../swarm-2026-11-27/INDEX.md) | the 27 November 2026 completion: proofs in named classes, with checks and errata |
| [`../applications/CANCER_DEFECTION_2026-11-23.md`](../applications/CANCER_DEFECTION_2026-11-23.md) | a case: cancer as defection from the tissue |
| [`../applications/AI_AGENT_OVERSIGHT_2026-11-23.md`](../applications/AI_AGENT_OVERSIGHT_2026-11-23.md) | a case: oversight of AI agents |

Cases are listed in the one index of cases, [`../applications/README.md`](../applications/README.md).
"""


def readmes(base):
    full = git("rev-parse", base).strip()
    for path, text in (("records/README.md", RECORDS_README.format(base=full)), ("theory/swarm/README.md", SWARM_README)):
        assert not os.path.exists(os.path.join(ROOT, path)), path + " exists"
        open(os.path.join(ROOT, path), "w", encoding="utf-8").write(text)
    print("wrote records/README.md (pins %s) and theory/swarm/README.md" % full)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--renames"]:
        renames()
    elif a[:1] == ["--refs"] and len(a) == 2:
        refs(a[1])
    elif a[:1] == ["--readmes"] and len(a) == 2:
        readmes(a[1])
    else:
        print(__doc__)
        sys.exit(2)
