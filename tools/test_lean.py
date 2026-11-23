#!/usr/bin/env python3
"""Build the Lean 4 formalization if Lean is installed; skip if it is not.

The build runs only in the dedicated checkout at /tmp/gtao-lean (or
$GTAO_LEAN_DIR), never in the clone the test is run from; it skips when that
checkout is missing or its formal/lean sources differ from this clone.

Run:  python3 -m pytest -q tools/test_lean.py
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Same token list as tools/check_lean.sh.
FORBIDDEN_RE = re.compile(
    r"(^|[^A-Za-z_])(sorry|admit|axiom|native_decide|unsafe|implemented_by)([^A-Za-z_]|$)"
)
SKIP_DIRS = {".lake", "lake-packages"}


def _lake_on_path() -> str | None:
    found = shutil.which("lake")
    if found:
        return found
    elan_lake = os.path.expanduser("~/.elan/bin/lake")
    if os.path.isfile(elan_lake) and os.access(elan_lake, os.X_OK):
        return elan_lake
    return None


def _strip_lean_comments(src: str) -> str:
    """Replace Lean line comments (`--`) and nested block comments (`/- ... -/`)
    with spaces, keeping newlines so reported line numbers stay aligned.

    `/--` and `/-!` documentation comments are block comments and are
    stripped.  A `--` that is the start of the block-comment closer `-/`
    is not treated as a line comment (that case is only reached at depth > 0).
    """
    out: list[str] = []
    i = 0
    n = len(src)
    depth = 0
    while i < n:
        if depth > 0:
            if src.startswith("/-", i):
                depth += 1
                out.append("  ")
                i += 2
            elif src.startswith("-/", i):
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if src[i] == "\n" else " ")
                i += 1
        else:
            if src.startswith("/-", i):
                depth = 1
                out.append("  ")
                i += 2
            elif src.startswith("--", i):
                while i < n and src[i] != "\n":
                    out.append(" ")
                    i += 1
            else:
                out.append(src[i])
                i += 1
    return "".join(out)


def test_lean_sources_have_no_sorry():
    """This assertion does not require Lean: no claimed proof may contain
    sorry, admit, axiom, native_decide, unsafe, or implemented_by.

    The name keeps the original test id.  Comments (line and block) are
    stripped before the scan so a word in a docstring is not a hit.
    Cache directories are not walked.
    """
    hits = []
    lean_root = os.path.join(ROOT, "formal", "lean")
    for dirpath, dirnames, filenames in os.walk(lean_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".lean"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                stripped = _strip_lean_comments(fh.read())
            for i, line in enumerate(stripped.splitlines(), 1):
                if FORBIDDEN_RE.search(line):
                    hits.append("%s:%d: %s" % (path, i, line.rstrip()))
    assert hits == [], "forbidden token found in Lean sources:\n" + "\n".join(hits)


# Repo rule: `lake build` runs only in a dedicated checkout at /tmp/gtao-lean
# (override with GTAO_LEAN_DIR), never inside an ordinary clone, because a
# Mathlib cache unpacked into every clone exhausts the disk.
LEAN_HOME = os.environ.get("GTAO_LEAN_DIR", "/tmp/gtao-lean")


def _lean_tree(root: str) -> dict[str, bytes]:
    """Project files under formal/lean, excluding caches, as {relpath: bytes}."""
    base = os.path.join(root, "formal", "lean")
    out: dict[str, bytes] = {}
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = os.path.join(dirpath, name)
            with open(path, "rb") as fh:
                out[os.path.relpath(path, base)] = fh.read()
    return out


def test_lean_build_if_available():
    if _lake_on_path() is None:
        pytest.skip("Lean 4 / lake is not installed")
    script = os.path.join(LEAN_HOME, "tools", "check_lean.sh")
    if not (os.path.isfile(script) and os.path.isdir(os.path.join(LEAN_HOME, "formal", "lean"))):
        pytest.skip(
            "lake runs only in %s (repo rule); no checkout there. "
            "Clone the repo to %s and rerun." % (LEAN_HOME, LEAN_HOME)
        )
    if os.path.realpath(LEAN_HOME) != os.path.realpath(ROOT):
        mine, theirs = _lean_tree(ROOT), _lean_tree(LEAN_HOME)
        # .gitignore and build outputs aside, the Lean sources must match byte for byte.
        diff = sorted(k for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k))
        if diff:
            pytest.skip(
                "formal/lean in %s differs from this clone (%s); sync that checkout "
                "(git -C %s fetch && git -C %s checkout <this commit>) and rerun"
                % (LEAN_HOME, ", ".join(diff[:5]), LEAN_HOME, LEAN_HOME)
            )
    env = os.environ.copy()
    elan_bin = os.path.expanduser("~/.elan/bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    r = subprocess.run(
        [script],
        cwd=LEAN_HOME,
        capture_output=True,
        text=True,
        timeout=1800,
        env=env,
    )
    assert r.returncode != 2, r.stdout + r.stderr
    assert r.returncode == 0, r.stdout + r.stderr
    assert "check_lean.sh: OK" in r.stdout
