#!/usr/bin/env python3
"""Toy-input run of the helpers that swarm27_checks.py calls (launch rule,
process/PREREG_GATE.md section 2). Run from the repo root after the lock:
  nice -n 19 python3 theory/swarm-2026-11-27/checks/toy_smoke.py > theory/swarm-2026-11-27/checks/toy_smoke.out
It prints helper outputs on fixed toy inputs and the wall time of one full
section of the main script, so the time budget comes from a measured toy run.
It scores nothing."""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import swarm27_checks as s  # noqa: E402

print("A(1) = %.12f" % s.A(1.0))
print("A_lat(1, 0.5) = %.12f" % s.A_lat(1.0, 0.5))
print("best_follow(0.1, A) = (%.6f, %.9f)" % s.best_follow(0.1, s.A))
print("g_follow(0.1) = %.9f" % s.g_follow(0.1))
pr = s.Prior("loguniform", 1.0, 100.0)
print("loguniform[1,100] mean = %.9f, m(1,10) = %.9f, P(1,10) = %.9f" % (pr.mean(), pr.m(1, 10), pr.P(1, 10)))
pu = s.Prior("uniform", 1.0, 100.0)
print("uniform[1,100] mean = %.9f, P(1,10) = %.9f" % (pu.mean(), pu.P(1, 10)))
two = s.tp_two(pr, 1.3)
print("tp_two(loguniform, 1.3) = %s" % (None if two is None else ["%.9f" % x for x in two]))
print("tp_two(loguniform, 2.3) = %s" % s.tp_two(pr, 2.3))
if two is not None:
    print("tp_verify(two) = %.3e" % s.tp_verify(pr, 1.3, two, ngrid=500))
    print("tp_value(two) = %.9f" % s.tp_value(pr, two))
q3 = s.tp_equilibrium(pr, 1.1, 3)
print("tp_equilibrium(loguniform, 1.1, 3) = %s" % (None if q3 is None else ["%.6f" % x for x in q3]))
print("L_floor(0.1) = %.9f" % s.L_floor(0.1))
Q = np.array([[-1.0, 1.0], [2.0, -2.0]])
print("stationary([[-1,1],[2,-2]]) = %s" % ["%.9f" % x for x in s.stationary(Q)])
t0 = time.time()
s.section_fold()
print("section A wall time class: %s" % ("under 60 s" if time.time() - t0 < 60 else "60 s or more"))
