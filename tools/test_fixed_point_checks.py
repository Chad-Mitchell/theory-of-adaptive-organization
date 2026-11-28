"""Runs the locked T76 fixed-point checks and compares stdout to the stored run."""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "theory", "record_ratio_reframes_checks")
LOCKED_THEORY = "6caadae569116a94a74563398be94cebf6e99e9b"
LOCKED_PREREG = "82d58bdcefca97218ac4b7587a9246850994eedac1c6c372de8f50a75417017b"
FIRST_LOCK = "8e495b7b97bbf254429dc4ed0aeb153944579db9f2230eae769937e98b43fce8"

def _theory_blobs_allowed():
    """The lock-time blob, and the blob of THEORY.md's `frozen:` row in process/LOCKED_BLOBS.txt (THEORY.md is
    frozen in place, 27 Nov 2026; tools/verify_locks.py fails any other edit). Test edit, disclosed in the commit
    that froze it: before, the allowed blobs were read from main refs."""
    allowed = {LOCKED_THEORY}
    with open(os.path.join(ROOT, "process", "LOCKED_BLOBS.txt"), encoding="utf-8") as fh:
        for line in fh:
            parts = line.split(None, 2)
            if len(parts) == 3 and parts[0] == "THEORY.md" and parts[2].startswith("frozen:"):
                allowed.add(parts[1])
    return allowed


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def test_fixed_point_prereg_lock_unchanged():
    assert _sha256(os.path.join(HERE, "PREREG_FIXED_POINTS.md")) == LOCKED_PREREG
    lock = open(os.path.join(HERE, "PREREG_FIXED_POINTS.sha256"), encoding="utf-8").readline().split()[0]
    assert lock == LOCKED_PREREG
    assert _sha256(os.path.join(HERE, "PREREG.md")) == FIRST_LOCK


def test_theory_blob_unchanged_fixed_point():
    r = subprocess.run(
        ["git", "hash-object", os.path.join(ROOT, "THEORY.md")],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() in _theory_blobs_allowed()


def test_fixed_point_checks_match_stored_stdout():
    script = os.path.join(HERE, "fixed_point_checks.py")
    r = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAILS 3" in r.stdout
    with open(os.path.join(HERE, "fixed_point_checks.out"), encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
