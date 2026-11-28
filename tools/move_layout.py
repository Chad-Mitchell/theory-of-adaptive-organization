#!/usr/bin/env python3
"""The 27 Nov 2026 layout move, driven by tools/movemap.py, run on a clean checkout of the latest main.

  python3 tools/move_layout.py --renames     step 1: every tracked file p goes to movemap.forward(p); bytes unchanged
  python3 tools/move_layout.py --refs BASE   step 2: rewrite path references in editable files (paths only)
  python3 tools/move_layout.py --report BASE print what step 2 changed and what it left (frozen files)

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


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--renames"]:
        renames()
    elif a[:1] == ["--refs"] and len(a) == 2:
        refs(a[1])
    else:
        print(__doc__)
        sys.exit(2)
