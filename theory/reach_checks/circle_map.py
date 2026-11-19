#!/usr/bin/env python3
"""REACH check 3: two coupled cycles. Where is the torus, where is locking?  (textbook sine circle map)
theta' = theta + Omega - (K/2pi) sin(2 pi theta)   (mod 1); the rotation number w(Omega) is the lifted mean advance per step.
K = 0: free quasi-periodic winding (the torus, with irrational w). 0 < K < 1: Arnold tongues (plateaus w = p/q) between
quasi-periodic stretches. K = 1: tongues fill all of Omega up to a measure-zero set (devil's staircase).
Run: nice -n 19 python3 circle_map.py > circle_map.out"""
import numpy as np
from fractions import Fraction
def rotation(Om, K, n_tr=2000, n=6000):
    th = np.zeros_like(Om)
    for _ in range(n_tr): th = th + Om - K / (2 * np.pi) * np.sin(2 * np.pi * th)
    x = th.copy(); s = np.zeros_like(Om)
    for _ in range(n):
        step = Om - K / (2 * np.pi) * np.sin(2 * np.pi * x); x = x + step; s += step
    return s / n
Om = np.linspace(0, 1, 4001)[:-1]
rats = sorted({Fraction(p, q) for q in range(1, 13) for p in range(0, q + 1)})
rv = np.array([float(r) for r in rats])
print("sine circle map, 4000 Omega values in [0,1); 'locked' = rotation number within 1e-4 of p/q, q<=12 (the 1e-4 band can only be reached on a plateau)")
print("%5s %14s %22s" % ("K", "locked share", "0:1 tongue width (Om)"))
for K in (0.0, 0.25, 0.5, 0.75, 1.0):
    w = rotation(Om, K)
    near = np.min(np.abs(w[:, None] - rv[None, :]), axis=1)
    locked = (near < 1e-4).mean()
    z = np.where((np.abs(w) < 1e-4) | (np.abs(w - 1) < 1e-4))[0]   # the plateau straddles Omega = 0 = 1
    width = (len(z)) / len(Om) * 1.0 if K > 0 else 0.0
    print("%5.2f %14.3f %12.4f (theory K/pi = %.4f)" % (K, locked, width, K / np.pi))
print("\nReading: with phase coupling the staircase appears and the locked share grows with K, as in textbooks (Adler 1946; Pikovsky, Rosenblum & Kurths 2001).")
print("A test that finds 'no staircase' in a system whose coupling is not phase coupling (e.g. trigger-and-reset events) has not tested this.")
