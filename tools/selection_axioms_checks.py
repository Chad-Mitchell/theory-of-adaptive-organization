#!/usr/bin/env python3
"""Numerical checks for theory/SELECTION_AXIOMS.md (SA1b equipartition, CL19
occupation and excess rates, SA2 addition of means).

These checks are NUMERICAL. They are not a substitute for the proofs in the
note, they do not re-run T27, and they do not touch locked hashes.

Run from the repo root:

    nice -n 19 python3 tools/selection_axioms_checks.py

Exit 0 and the line ALL SA CHECKS PASS means every identity below held.
"""
from __future__ import annotations

import math
import sys

import numpy as np

rng = np.random.default_rng(20261121)
ok = []
detail = []


def check(name, cond, msg=""):
    ok.append((name, bool(cond)))
    detail.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


# ---------------------------------------------------------------------------
# SA1b: equipartition E[ (1/2) x^T H x ] = d/(2 beta) under Boltzmann.
# ---------------------------------------------------------------------------
def equipartition_mc(d, beta, n=200_000):
    # J = (1/2) ||x||^2, so H = I, Sigma = I/beta, E[J] = d/(2 beta)
    x = rng.normal(0.0, 1.0 / math.sqrt(beta), size=(n, d))
    j = 0.5 * np.sum(x * x, axis=1)
    return float(j.mean()), d / (2.0 * beta)


for d, beta in ((1, 2.0), (1, 8.0), (2, 4.0), (3, 10.0), (5, 3.0)):
    got, want = equipartition_mc(d, beta)
    rel = abs(got - want) / want
    check(
        "SA1b d=%d beta=%g" % (d, beta),
        rel < 0.03,
        "mc=%.6f exact=%.6f rel=%.4f" % (got, want, rel),
    )

# Exact trace identity, no sampling: (1/2) Tr(H (beta H)^{-1}) = d/(2 beta)
for d, beta in ((1, 1.0), (4, 7.5), (8, 0.5)):
    H = np.diag(np.linspace(0.5, 2.0, d))
    Sigma = np.linalg.inv(beta * H)
    got = 0.5 * float(np.trace(H @ Sigma))
    want = d / (2.0 * beta)
    check(
        "SA1b-trace d=%d beta=%g" % (d, beta),
        abs(got - want) < 1e-12,
        "got=%.12f want=%.12f" % (got, want),
    )


# ---------------------------------------------------------------------------
# CL19 / SA2-C: occupation of BM reset at +/- b is triangular; E[w x^2] = w b^2/6
# At b* = (6 k sigma^2 / w)^{1/4}:
#   operational excess = sqrt(k w sigma^2 / 6)
#   total rate (incl. lumps) = 2 * that
# ---------------------------------------------------------------------------
def triangular_occupation_sample(b, n):
    # density rho(x) = (b - |x|) / b^2 on [-b, b].
    # CDF on [0, b] of |X|: P(|X| <= t) = 1 - (b-t)^2 / b^2, so |X| = b (1 - sqrt(U)).
    u = rng.random(n)
    mag = b * (1.0 - np.sqrt(u))
    sign = rng.choice(np.array([-1.0, 1.0]), size=n)
    return sign * mag


b = 2.0
w = 3.0
xs = triangular_occupation_sample(b, 300_000)
got_ex = w * float(np.mean(xs ** 2))
want_ex = w * b * b / 6.0
check(
    "Dixit occupation E[w x^2]",
    abs(got_ex - want_ex) / want_ex < 0.02,
    "mc=%.6f exact=%.6f" % (got_ex, want_ex),
)

# Density integrates to 1 and is nonnegative: already by construction.
# Mean cycle time identity: exit time b^2/sigma^2, used below only algebraically.

k, sigma2, w = 0.4, 0.9, 2.0
bstar = (6.0 * k * sigma2 / w) ** 0.25
op = w * bstar * bstar / 6.0
lumps = k * sigma2 / (bstar * bstar)
total = op + lumps
want_op = math.sqrt(k * w * sigma2 / 6.0)
want_total = 2.0 * want_op
check("CL19 b* operational identity", abs(op - want_op) < 1e-12, "op=%.12f want=%.12f" % (op, want_op))
check("CL19 b* lumps equal operational", abs(lumps - op) < 1e-12, "lumps=%.12f op=%.12f" % (lumps, op))
check("CL19 b* total identity", abs(total - want_total) < 1e-12, "total=%.12f want=%.12f" % (total, want_total))

# Formula k sigma^2 / b^2 + w b^2 / 6 has derivative zero at b*
def rate(b):
    return k * sigma2 / (b * b) + w * b * b / 6.0

# numerical derivative
eps = 1e-6
dleft = (rate(bstar) - rate(bstar - eps)) / eps
dright = (rate(bstar + eps) - rate(bstar)) / eps
check(
    "CL19 first-order condition at b*",
    abs(dleft) < 1e-5 and abs(dright) < 1e-5,
    "dleft=%.3e dright=%.3e" % (dleft, dright),
)


# ---------------------------------------------------------------------------
# SA2: addition of means. J - J* = w x^2 + (1/2) y^T y, x ~ Dixit occupation,
# y ~ Boltzmann (H = I). E = operational Dixit + d/(2 beta).
# ---------------------------------------------------------------------------
d, beta = 3, 5.0
n = 200_000
x = triangular_occupation_sample(bstar, n)
y = rng.normal(0.0, 1.0 / math.sqrt(beta), size=(n, d))
excess = w * x * x + 0.5 * np.sum(y * y, axis=1)
got = float(excess.mean())
want = w * bstar * bstar / 6.0 + d / (2.0 * beta)
check(
    "SA2 addition of means",
    abs(got - want) / want < 0.02,
    "mc=%.6f exact=%.6f" % (got, want),
)


# ---------------------------------------------------------------------------
# SA3 curvature cancellation (algebra only): E[w L^2] = sigma_theta^2 / (4 alpha V_G)
# ---------------------------------------------------------------------------
alpha, w, VG, sig_th2 = 0.8, 1.7, 0.25, 0.5
lam = 2.0 * alpha * w * VG
var_L = sig_th2 / (2.0 * lam)
got = w * var_L
want = sig_th2 / (4.0 * alpha * VG)
check("SA3 curvature cancellation", abs(got - want) < 1e-12, "got=%.12f want=%.12f" % (got, want))


# ---------------------------------------------------------------------------
# SA1 Moran ratio algebra: phi_ji / phi_ij = rho^{N-1}
# ---------------------------------------------------------------------------
def phi(rho, N):
    if abs(rho - 1.0) < 1e-15:
        return 1.0 / N
    return (1.0 - rho) / (1.0 - rho ** N)


N = 11
for rho in (0.4, 0.9, 1.0, 1.2, 2.5):
    ratio = phi(1.0 / rho, N) / phi(rho, N) if rho != 1.0 else 1.0
    want = rho ** (N - 1) if rho != 1.0 else 1.0
    check(
        "SA1 fixation ratio rho=%g" % rho,
        abs(ratio - want) / max(want, 1e-12) < 1e-10,
        "got=%.12g want=%.12g" % (ratio, want),
    )


nfail = sum(1 for _, c in ok if not c)
for line in detail:
    print(line)
if nfail:
    print("SOME SA CHECKS FAILED (%d)" % nfail)
    returncode = 1
else:
    print("ALL SA CHECKS PASS (%d)" % len(ok))
    returncode = 0
sys.exit(returncode)
