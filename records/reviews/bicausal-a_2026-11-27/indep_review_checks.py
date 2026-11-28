"""Independent reviewer checks for PR #305 (no sympy, no ba_lib). Fractions for exact Lyapunov; mpmath for FD."""
from fractions import Fraction as Fr
import math, mpmath as mp
import numpy as np
from scipy.optimize import minimize

def solve_lin(A, b):  # exact Gaussian elimination over Fractions (or mpf)
    n = len(A); M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def lyap(F, Dg, zero=0):
    n = len(F); idx = [(i, j) for i in range(n) for j in range(i, n)]; pos = {p: k for k, p in enumerate(idx)}
    def k(i, j): return pos[(min(i, j), max(i, j))]
    A = []; b = []
    for (i, j) in idx:  # (F S + S F^T)_{ij} + 2 D_ij = 0
        row = [zero] * len(idx)
        for l in range(n):
            row[k(l, j)] += F[i][l]; row[k(i, l)] += F[j][l]
        A.append(row); b.append(-2 * Dg[i] if i == j else zero)
    s = solve_lin(A, b); return [[s[k(i, j)] for j in range(n)] for i in range(n)]

# ---- BA-T1: Delta by mpmath central differences of independently solved W2 costs
mp.mp.dps = 60
def w2(par, gam, c, g):
    a, D, DM, w, ww, wx = par
    S = lyap([[-a, a * g], [gam * c, -gam]], [D, DM], mp.mpf(0))
    sxx, sxm, smm = S[0][0], S[0][1], S[1][1]
    ex = sxx - 2 * g * sxm + g * g * smm; em = smm - 2 * c * sxm + c * c * sxx
    Jm = gam ** 2 * em - DM * gam + w * (sxx - 2 * sxm + smm) + wx * sxx
    Jw = a ** 2 * ex - D * a + ww * ex + wx * sxx
    return Jm, Jw
def cross(f, x, y, h=mp.mpf('1e-12')):
    return (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h * h)
def delta(par, gam, c, g):
    gam, c, g = map(mp.mpf, (gam, c, g))
    Pm = [cross(lambda u, v: w2(par, u, c, v)[0], gam, g), cross(lambda u, v: w2(par, gam, u, v)[0], c, g)]
    Pw = [cross(lambda u, v: w2(par, u, c, v)[1], gam, g), cross(lambda u, v: w2(par, gam, u, v)[1], c, g)]
    return Pm[0] * Pw[1] - Pm[1] * Pw[0], Pm, Pw
one = mp.mpf(1)
for wx, exact in [(0.5, Fr(27462244677, 1506922300)), (1, Fr(5789210497, 301384460)), (2, Fr(31913668101, 1506922300)), (0, Fr(71962429, 4174300))]:
    d, _, _ = delta((one, one, one, 10, 10, mp.mpf(wx)), mp.mpf(19) / 7, -0.5, 3)
    print("BA-T1 w_x=%s: FD Delta %s  exact %s  rel.diff %.2e" % (wx, mp.nstr(d, 15), float(exact), float(abs(d - mp.mpf(exact.numerator) / exact.denominator) / abs(d))))
d, Pm, Pw = delta((one, one, one, 0, 0, 0), 10, mp.mpf(-17) / 10, mp.mpf(7) / 5)
print("BA-T1 heats only at (10,-17/10,7/5): FD Delta %s exact %s" % (mp.nstr(d, 15), -28 / 1331))

# ---- BA-T2: exact Fraction evaluation of designs rounded from the printed 3-decimal logs
def pooled_exact(K, w, b0, D0, b1, D1):
    a = v = Fr(1)
    F = [[-a, 0, 0], [b0, -b0, 0], [0, b1, -b1]]
    S = lyap(F, [a * v, D0, D1], Fr(0))
    e0 = S[1][1] - 2 * S[0][1] + S[0][0]; e1 = S[2][2] - 2 * S[1][2] + S[1][1]
    Q0 = b0 * b0 * e0 / D0 - b0; Q1 = b1 * b1 * e1 / D1 - b1
    eps1 = v - S[0][2] ** 2 / S[2][2]
    QX = a * a * S[0][0] / (a * v) - a
    return Q0 / K + Q1 + w * eps1, Q0, Q1, eps1, QX
for K, w, x in [(32, 3, (0.943, -2.103, 12.0, 10.792)), (24, 10, (1.736, -1.819, 12.0, 10.134)), (24, 100, (3.069, -1.716, 12.0, 8.894))]:
    des = [Fr(math.exp(xi)).limit_denominator(10 ** 12) for xi in x]
    P, Q0, Q1, eps1, QX = pooled_exact(K, w, *des)
    Jd = 2 * math.sqrt(w) - 1
    print("BA-T2 w=%d K=%d (3-dec rounded design): exact per-member %.9f  J_dir %.9f  ratio %.6f  QX=%s  Q0 closed-form check %.3e"
          % (w, K, float(P), Jd, float(P) / Jd, QX, float(Q0) - float(des[0] ** 2 / ((1 + des[0]) * des[1]))))

# ---- direct member in class LINK cannot beat J_dir (sanity) ; free mobility
def direct(x, w):
    b1, D1 = np.exp(np.clip(x, -10, 25))
    S = lyap([[-1.0, 0], [b1, -b1]], [1.0, D1], 0.0)
    e1 = S[1][1] - 2 * S[0][1] + S[0][0]
    return b1 * b1 * e1 / D1 - b1 + w * (1 - S[0][1] ** 2 / S[1][1])
for w in (3, 10, 100):
    best = min((minimize(direct, x0, args=(w,), method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-12, maxfev=20000)) for x0 in [(0, 0), (5, 3), (10, 8), (15, 13)]), key=lambda r: r.fun)
    print("direct LINK w=%d: best %.6f at ln b1=%.2f ln D1=%.2f vs J_dir %.6f" % (w, best.fun, *best.x, 2 * math.sqrt(w) - 1))
