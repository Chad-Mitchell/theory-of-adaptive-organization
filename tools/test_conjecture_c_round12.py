"""Round 12-M (Conjecture C beyond (star)) checks: theory/record-cost-2026-11-25/scripts/selfref/m_round12_*.py.

Needs numpy, pycddlib (module cdd) and, for the LP search, scipy. Every test skips cleanly when a dependency is missing.
Vertex enumeration is in floating point; outputs are compared with the committed .stdout files.
"""
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "theory", "record-cost-2026-11-25", "scripts", "selfref")


def _need(*mods):
    for mod in mods:
        pytest.importorskip(mod)


def _run(args):
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, cwd=HERE)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def _stdout(name):
    with open(os.path.join(HERE, name + ".stdout"), encoding="utf-8") as f:
        return f.read()


def test_disk_inequalities_match_stdout():
    _need("numpy", "cdd")
    out = _run(["m_round12_disk_check.py"])
    assert "VIOLATED" not in out
    assert out == _stdout("m_round12_disk_check")


def test_diamond_small_pairs_match_stdout():
    _need("numpy", "cdd")
    out = _run(["m_round12_diamond.py", "sqxsq", "P5xP5", "P6xP6", "sqxP5"])
    full = _stdout("m_round12_diamond").splitlines()
    for line in out.splitlines():
        assert line in full
        assert "diamond HOLDS" in line
