#!/usr/bin/env python3
"""Fix 1 for swarm27_checks.py (DEVIATIONS.md, D1), kept separate so the first
lock (SHA256SUMS) still verifies the locked bytes.

The toy run of the first lock stopped in tp_next: brentq's lower bracket
q_k (1 + 1e-15) can round so that f(a) is not negative. The fix brackets at
q_k itself, where m(q_k, q_k) - target = q_k - target < 0 because target > q_k.
Nothing else changes.

Run from the repo root:
  nice -n 19 python3 -u theory/swarm-2026-11-27/checks/swarm27_fix1.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swarm27_checks as s  # noqa: E402
from scipy.optimize import brentq  # noqa: E402


def tp_next(pr, kappa, q_prev, q_k):
    """Next boundary from q_k = kappa sqrt(m_k m_{k+1}); None if no solution
    (chain cannot continue), inf if it overshoots hi."""
    mk = pr.m(q_prev, q_k)
    target = q_k * q_k / (kappa * kappa * mk)
    if target <= q_k:
        return None
    if target >= pr.m(q_k, pr.hi):
        return math.inf
    return brentq(lambda x: pr.m(q_k, x) - target, q_k, pr.hi, xtol=1e-15, rtol=1e-15)


s.tp_next = tp_next

if __name__ == "__main__":
    s.main()
