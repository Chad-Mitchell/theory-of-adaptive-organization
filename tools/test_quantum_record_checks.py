"""Runs the locked T76 quantum-record checks and compares stdout to the stored run."""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "theory", "record_ratio_reframes_checks")
LOCKED_THEORY = "6caadae569116a94a74563398be94cebf6e99e9b"
LOCKED_PREREG = "1ac92e314705b3378e3b6a1bd665d36ec6dc9f7f812760a20bc4556617b817d3"


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def test_quantum_prereg_lock_unchanged():
    assert _sha256(os.path.join(HERE, "PREREG_QUANTUM.md")) == LOCKED_PREREG
    lock = open(os.path.join(HERE, "PREREG_QUANTUM.sha256"), encoding="utf-8").readline().split()[0]
    assert lock == LOCKED_PREREG


def test_theory_blob_unchanged_quantum():
    r = subprocess.run(
        ["git", "hash-object", os.path.join(ROOT, "THEORY.md")],
        capture_output=True, text=True, cwd=ROOT, timeout=30,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == LOCKED_THEORY


def test_quantum_record_checks_match_stored_stdout():
    script = os.path.join(HERE, "quantum_record_checks.py")
    r = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAILS 2" in r.stdout
    assert "Q-reuse FAIL" in r.stdout
    assert "Q-coh FAIL" in r.stdout
    with open(os.path.join(HERE, "quantum_record_checks.out"), encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
