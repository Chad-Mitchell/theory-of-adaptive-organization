"""Round 11-M (Conjecture C) checks: theory/record-cost-2026-11-25/scripts/selfref/m_round11*.py.

Needs numpy, sympy and networkx; the max-tensor checks also need the lrs and redund programs from lrslib.
Every test skips cleanly when a dependency is missing.
"""
import os
import shutil
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "theory", "record-cost-2026-11-25", "scripts", "selfref")


def _need_python_deps():
    for mod in ("numpy", "sympy", "networkx"):
        pytest.importorskip(mod)


def _need_lrs():
    if shutil.which("lrs") is None or shutil.which("redund") is None:
        pytest.skip("lrslib (lrs, redund) not installed")


def _run(name, timeout):
    r = subprocess.run([sys.executable, os.path.join(HERE, name + ".py")], capture_output=True, text=True,
                       timeout=timeout, cwd=HERE)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def test_stabilizer_positive_control():
    _need_python_deps()
    out = _run("m_round11_control", 300)
    assert "ENTANGLING AUTOMORPHISM FOUND" in out
    assert "exact linear map reproduces the permutation on all extreme points: True" in out
    with open(os.path.join(HERE, "m_round11_control.stdout"), encoding="utf-8") as f:
        assert out == f.read()


def test_square_max_certified():
    _need_python_deps()
    _need_lrs()
    sys.path.insert(0, HERE)
    import m_round11_lib as L
    V = L.max_tensor_vertices(L.S["square"], L.S["square"])
    assert len(V) == 24
    status = L.analyse("max squarexsquare", L.S["square"], L.S["square"], V)[0]
    assert status.startswith("CERTIFIED")


def test_reducible_part_matches_stdout():
    _need_python_deps()
    _need_lrs()
    out = _run("m_round11_pyramid", 300)
    assert out.count("CERTIFIED") == 3
    with open(os.path.join(HERE, "m_round11_pyramid.stdout"), encoding="utf-8") as f:
        assert out == f.read()
