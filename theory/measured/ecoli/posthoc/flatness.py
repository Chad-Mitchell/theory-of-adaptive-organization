#!/usr/bin/env python3
"""POST HOC: how costly is the measured memory (9.9 s) under each noise model? Fraction of the optimum's explained
variance of u that a single store with memory tau captures (free gain), at g = 0.1 and 0.4 /mm."""
import numpy as np
lam, av, G, t1, t2, sn, tn = 0.862, 157.1, 1.73, 0.22, 9.9, 0.092, 11.75
K0 = G * t2 * t2 / (t1 + t2); Ns = 2 * sn * sn * tn / K0 ** 2; V0 = sn ** 2 / K0 ** 2
taus = np.logspace(-2, 3, 20001)
for g in (0.1, 0.4):
    s2 = (g * 1e-3) ** 2 * av; A = 1 / (1 + lam * taus)
    for name, Vx in (("B fixed density", Ns / (2 * taus)), ("C fixed variance", V0 * (t2 / taus) ** 2)):
        ev = (s2 * A) ** 2 / (s2 * A + Vx)
        i = np.argmax(ev); j = np.argmin(abs(taus - t2))
        print(f"g={g} {name}: tau*={taus[i]:.2f} s; measured 9.9 s captures {ev[j]/ev[i]:.2f} of the optimum's explained variance")
