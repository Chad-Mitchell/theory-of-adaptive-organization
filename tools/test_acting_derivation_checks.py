#!/usr/bin/env python3
"""Run the acting-derivation algebra checks. Does not run the locked comparison."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_acting_derivation_checks():
    script = os.path.join(ROOT, "theory", "acting_derivation_checks", "acting_derivation_checks.py")
    proc = subprocess.run([sys.executable, script], cwd=ROOT, check=False)
    assert proc.returncode == 0


if __name__ == "__main__":
    test_acting_derivation_checks()
