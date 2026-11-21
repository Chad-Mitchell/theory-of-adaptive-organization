#!/usr/bin/env python3
"""Build the Lean 4 formalization if Lean is installed; skip if it is not.

Run:  python3 -m pytest -q tools/test_lean.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lake_on_path() -> str | None:
    found = shutil.which("lake")
    if found:
        return found
    elan_lake = os.path.expanduser("~/.elan/bin/lake")
    if os.path.isfile(elan_lake) and os.access(elan_lake, os.X_OK):
        return elan_lake
    return None


def test_lean_sources_have_no_sorry():
    """This assertion does not require Lean: no claimed proof may contain sorry."""
    hits = []
    lean_root = os.path.join(ROOT, "formal", "lean")
    for dirpath, dirnames, filenames in os.walk(lean_root):
        dirnames[:] = [d for d in dirnames if d not in {".lake", "lake-packages"}]
        for name in filenames:
            if not name.endswith(".lean"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as fh:
                for i, line in enumerate(fh, 1):
                    # Token `sorry`, not the word inside a comment identifier.
                    stripped = line.split("--", 1)[0]
                    if "sorry" in stripped:
                        hits.append("%s:%d: %s" % (path, i, line.rstrip()))
    assert hits == [], "sorry found in Lean sources:\n" + "\n".join(hits)


def test_lean_build_if_available():
    if _lake_on_path() is None:
        pytest.skip("Lean 4 / lake is not installed")
    script = os.path.join(ROOT, "tools", "check_lean.sh")
    env = os.environ.copy()
    elan_bin = os.path.expanduser("~/.elan/bin")
    if os.path.isdir(elan_bin):
        env["PATH"] = elan_bin + os.pathsep + env.get("PATH", "")
    r = subprocess.run(
        [script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=1800,
        env=env,
    )
    assert r.returncode != 2, r.stdout + r.stderr
    assert r.returncode == 0, r.stdout + r.stderr
    assert "check_lean.sh: OK" in r.stdout
