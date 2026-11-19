#!/usr/bin/env python3
"""REACH check 7: candidate price -> K map (N45) and the shape of the locking optimum.   Run: nice -n 19 python3 price_maps.py > price_maps.out
(A) K = 2 pi Z eps: a sine phase-response curve of peak sensitivity Z (phase cycles per unit stimulus) driven by a stimulus of
    amplitude eps per cycle gives the sine circle map with K/2pi = eps Z; the 0:1 tongue half-width is eps Z, so its width is 2 eps Z = K/pi.
(B) Interior optimum, ASSUMPTIONS: benefit V per unit time while locked (locked = |Omega| < a, a = K/2pi = eps Z), Omega ~ Normal(mu, sigma^2) across
    the targets or over time, price c per unit of a (linear in K).   maximise  U(a) = V P(|Omega| < a) - c a.
    mu = 0:  interior optimum a* = sigma sqrt(2 ln(2V/(c sigma sqrt(2 pi)))) for c < c0 = 2V/(sigma sqrt(2 pi)), else a* = 0 (continuous onset).
    P'(a) = phi(a - mu) + phi(a + mu) is unimodal on a >= 0 iff |mu| <= sigma, so U is concave (unique interior optimum, continuous in c) iff |mu| <= sigma;
    for |mu| > sigma the benefit is convex at small a and the optimum jumps between 0 and a large value (first-order, all-or-nothing).
"""
import numpy as np
from scipy.special import erf

print("(A) circle map: measured 0:1 tongue width vs 2 eps Z (Z = 0.5 phase cycles per unit stimulus)")
def rot(Om, K, ntr=2000, n=4000):
    th = np.zeros_like(Om)
    for _ in range(ntr): th = th + Om - K / (2 * np.pi) * np.sin(2 * np.pi * th)
    s = np.zeros_like(Om); x = th.copy()
    for _ in range(n):
        st = Om - K / (2 * np.pi) * np.sin(2 * np.pi * x); x = x + st; s += st
    return s / n
Z = 0.5
for eps in (0.05, 0.1, 0.2):
    K = 2 * np.pi * Z * eps
    Om = np.linspace(-0.4, 0.4, 8001); r = rot(Om, K); wdt = (np.abs(r) < 1e-4).sum() * (Om[1] - Om[0])
    print("  eps = %.2f  K = %.4f  measured width %.4f   2 eps Z = %.4f   K/pi = %.4f" % (eps, K, wdt, 2 * eps * Z, K / np.pi))

print("\n(B) optimum a(c) for V = 1, sigma = 1; closed form for mu = 0, and the largest jump of the optimum as the price c varies, for several mu")
V, sig = 1.0, 1.0
def P(a, mu): return 0.5 * (erf((a - mu) / (np.sqrt(2) * sig)) + erf((a + mu) / (np.sqrt(2) * sig)))
agrid = np.linspace(0, 8, 80001)
c0 = 2 * V / (sig * np.sqrt(2 * np.pi))
print("  c0 = 2V/(sigma sqrt(2 pi)) = %.4f" % c0)
print("  mu = 0:   c/c0   a* (numeric)  a* (closed form)")
for fr in (0.05, 0.2, 0.5, 0.8, 0.95, 1.05):
    c = fr * c0; U = V * P(agrid, 0.0) - c * agrid; a_num = agrid[np.argmax(U)]
    a_cf = sig * np.sqrt(2 * np.log(c0 / c)) if c < c0 else 0.0
    print("            %5.2f   %9.4f   %9.4f" % (fr, a_num, a_cf))
for mu in (0.0, 0.5, 0.9, 1.0, 1.1, 1.5, 2.5):
    cs = np.linspace(0.01, 1.6, 800) * c0; best = []
    for c in cs:
        U = V * P(agrid[::10], mu) - c * agrid[::10]; best.append(agrid[::10][np.argmax(U)])
    best = np.array(best); jump = np.max(np.abs(np.diff(best)))
    print("  mu = %.1f sigma: largest jump of a*(c) between neighbouring prices = %.3f   (%s)" % (mu, jump, "continuous" if jump < 0.2 else "steep or discontinuous (at mu = sigma exactly: a fourth-root cusp, still continuous)"))
