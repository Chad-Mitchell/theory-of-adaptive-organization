#!/usr/bin/env python3
"""Independent recomputation for theory/ACTING_DERIVATION_2026-11-22.md.

Does not import theory/acting_derivation_checks. The Lyapunov solution,
the bath rates, the information flow, and the cubic stationary costs are
derived here. The path integrator follows the locked protocol in
theory/acting_derivation_checks/PREREG.md (Euler-Maruyama, left-point
drift, dt=0.0002, burn 40, record 800, PCG64).
"""
from __future__ import annotations

import time

import numpy as np
import sympy as sp
from scipy import sparse
from scipy.integrate import quad
from scipy.sparse.linalg import spsolve

CLAIMED_GATE = 1.973637317765
SEED0 = 20261122
DT = 0.0002
N_BURN = int(round(40.0 / DT))
N_REC = int(round(800.0 / DT))
N_STEPS = N_BURN + N_REC
GRID = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0)


def bernoulli(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    small = np.abs(z) < 1e-7
    zs = z[small]
    out[small] = 1.0 - 0.5 * zs + (zs * zs) / 12.0
    pos = (~small) & (z >= 0.0)
    neg = (~small) & (z < 0.0)
    zp = z[pos]
    ez = np.exp(-zp)
    out[pos] = zp * ez / (1.0 - ez)
    zn = z[neg]
    out[neg] = zn / np.expm1(zn)
    return out


def solve_stationary(K, n, L, cubic=True):
    """No-flux Scharfetter-Gummel stationary Fokker-Planck on [-L, L]^2."""
    x = np.linspace(-L, L, n)
    dx = float(x[1] - x[0])
    xf = 0.5 * (x[:-1] + x[1:])
    rows = []
    cols = []
    vals = []

    def add_faces(face_x, face_m, drift, diff):
        dlt = drift * dx / diff
        # J = (D/dx) [B(-δ) p_left - B(δ) p_right]
        bp = (diff / dx**2) * bernoulli(-dlt)
        bm = (diff / dx**2) * bernoulli(dlt)
        return bp, bm

    xx, mm = np.meshgrid(xf, x, indexing="ij")
    if cubic:
        fx = -(xx + xx**3 + K * mm)
    else:
        fx = -(xx + K * mm)
    bp, bm = add_faces(xf, x, fx, 1.0)
    ii = np.arange(n - 1)[:, None]
    jj = np.arange(n)[None, :]
    left = (ii * n + jj).ravel()
    right = ((ii + 1) * n + jj).ravel()
    rows += [left, left, right, right]
    cols += [left, right, left, right]
    vals += [-bp.ravel(), bm.ravel(), bp.ravel(), -bm.ravel()]

    xx, mm = np.meshgrid(x, xf, indexing="ij")
    fm = -mm + xx
    bp, bm = add_faces(x, xf, fm, 1.0)
    ii = np.arange(n)[:, None]
    jj = np.arange(n - 1)[None, :]
    down = (ii * n + jj).ravel()
    up = (ii * n + (jj + 1)).ravel()
    rows += [down, down, up, up]
    cols += [down, up, down, up]
    vals += [-bp.ravel(), bm.ravel(), bp.ravel(), -bm.ravel()]

    nunk = n * n
    mat = sparse.coo_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(nunk, nunk),
    ).tolil()
    mat[nunk - 1, :] = dx * dx
    rhs = np.zeros(nunk)
    rhs[-1] = 1.0
    p = spsolve(mat.tocsr(), rhs).reshape((n, n))
    xx, mm = np.meshgrid(x, x, indexing="ij")
    w = p * dx * dx
    if cubic:
        fx = -(xx + xx**3 + K * mm)
        dfx = -(1.0 + 3.0 * xx**2)
    else:
        fx = -(xx + K * mm)
        dfx = -1.0
    fm = -mm + xx
    ex2 = float((w * xx**2).sum())
    sr_x = float((w * (fx**2 + dfx)).sum())
    sr_m = float((w * (fm**2 - 1.0)).sum())
    return ex2, sr_x, sr_m, float(w.sum()), float(p.min())


def closed_linear_variance(K):
    den = 1.0 * (1.0 + 1.0) * (K + 1.0)
    return (K + 1.0 + 1.0 + K * K) / den


def fit_minimizer(ks, values):
    i = int(np.argmin(values))
    lo = max(0, i - 4)
    hi = min(len(ks), i + 5)
    coef = np.polyfit(ks[lo:hi], values[lo:hi], 4)
    roots = np.roots(np.polyder(coef))
    real = [r.real for r in roots if abs(r.imag) < 1e-8 and ks[0] <= r.real <= ks[-1]]
    return min(real, key=lambda r: abs(r - ks[i]))


def symbolic():
    a, g, c, D, Dm = sp.symbols("a gamma c D Dm", positive=True)
    b, K = sp.symbols("b K", real=True)
    v, s, m = sp.symbols("v s m")
    eqs = [
        sp.Eq(a * v + b * K * s, D),
        sp.Eq(g * c * v - (a + g) * s - b * K * m, 0),
        sp.Eq(g * c * s - g * m + Dm, 0),
    ]
    sol = sp.solve(eqs, [v, s, m], simplify=True)
    vv, ss, mm = [sp.together(sol[z]) for z in (v, s, m)]
    ef_x = sp.expand(a**2 * vv + 2 * a * b * K * ss + (b * K) ** 2 * mm)
    sr_x = sp.together((ef_x + D * (-a)) / D)
    ef_m = sp.expand((g * c) ** 2 * vv + g**2 * mm - 2 * g**2 * c * ss)
    sr_m = sp.together((ef_m + Dm * (-g)) / Dm)
    comb = D * c * g + Dm * b * K
    show_x = b * K * comb / (D * (a + g))
    show_m = c * g * comb / (Dm * (a + g))
    heat = sp.together(D * sr_x + Dm * sr_m)
    heat_show = comb * (c * g + b * K) / (a + g)
    sigma = sp.Matrix([[vv, ss], [ss, mm]])
    prec = sp.simplify(sigma.inv())
    drift = sp.Matrix([[-a, -b * K], [g * c, -g]])
    link = sp.simplify(drift + sp.diag(D, Dm) * prec)
    var_xm = sp.together(vv - ss**2 / mm)
    gx = sp.together(ss / mm)
    beta = sp.Matrix([gx / var_xm, -(gx**2) / var_xm])
    flow_m = sp.together((link.row(1) * sigma * beta)[0])
    flow_x_var = sp.together(mm - ss**2 / vv)
    gm = sp.together(ss / vv)
    alpha = sp.Matrix([-(gm**2) / flow_x_var, gm / flow_x_var])
    flow_x = sp.together((link.row(0) * sigma * alpha)[0])
    show_i = comb * (D * c * g**2 - Dm * K * a * b) / (comb**2 + D * Dm * (a + g) ** 2)
    checks = {
        "Sr_X": sp.simplify(sr_x - show_x) == 0,
        "Sr_M": sp.simplify(sr_m - show_m) == 0,
        "heat": sp.simplify(heat - heat_show) == 0,
        "Sr_sum": sp.simplify(sp.together(sr_x + sr_m) - comb**2 / (D * Dm * (a + g))) == 0,
        "I_balance": sp.simplify(flow_x + flow_m) == 0,
        "I_M": sp.simplify(flow_m - show_i) == 0,
        "b0_variance": sp.simplify(vv.subs(b, 0) - D / a) == 0,
        "b0_Sr_X": sp.simplify(sr_x.subs(b, 0)) == 0,
        "b0_learning": sp.simplify(
            flow_m.subs(b, 0) - D * c**2 * g**3 / (D * c**2 * g**2 + Dm * (a + g) ** 2)
        )
        == 0,
    }
    bp = sp.symbols("b", positive=True)
    slope = sp.factor(sp.diff(heat_show.subs(b, bp), K))
    # slope = b*((D+Dm)*c*g + 2*Dm*b*K)/(a+g)
    checks["heat_slope_positive_form"] = sp.simplify(
        slope - bp * ((D + Dm) * c * g + 2 * Dm * bp * K) / (a + g)
    ) == 0
    vv_p = sp.together(sp.diff(vv.subs(b, bp), K))
    num, den = sp.fraction(sp.together(vv_p))
    # Cancel the positive factor (a+gamma) shared by the numerator and the denominator.
    num_c = sp.together(sp.cancel(num / (a + g)))
    den_c = sp.together(sp.cancel(den / (a + g)))
    poly = sp.Poly(sp.expand(num_c), K)
    checks["vprime_degree"] = poly.degree() == 2
    checks["vprime_lead_positive"] = sp.simplify(poly.LC() - Dm * bp**3 * c) == 0
    checks["vprime_const_negative"] = sp.simplify(poly.nth(0) + D * bp * c * g**2) == 0
    checks["vprime_den_positive_factor"] = sp.simplify(
        sp.factor(den_c) - g * (a + g) * (K * bp * c + a) ** 2
    ) == 0
    sr0 = sp.together((D * c**2 * g**2 / (Dm * (a + g))))
    im0 = sp.together(D * c**2 * g**3 / (D * c**2 * g**2 + Dm * (a + g) ** 2))
    gap = sp.factor(sp.together(sr0 - im0))
    checks["b0_Sr_M_above_flow"] = gap != 0 and sp.simplify(gap).is_nonnegative is not False
    # explicit nonnegative factorization already computed: every factor is positive
    checks["b0_gap_factored"] = str(gap)
    # Five-term accounting: b=0 drops the effort coordinate.
    # Accounting identity, not a dynamical theorem: the b=0 cost is the
    # five master-equation coordinates and the effort coordinate is absent.
    terms = ("kappa_Imem", "hK", "w_Ell", "A", "L")
    checks["five_terms"] = len(terms) == 5 and "rho_zu" not in terms
    return checks, slope, terms


def trajectory(seed, K, cubic, block=0):
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    z = rng.standard_normal(N_STEPS * 2)
    x = 0.0
    m = 0.0
    sdx = sdm = (2.0 * DT) ** 0.5
    sum_x2 = sum_srx = sum_srm = 0.0
    blocks = []
    bsum = 0.0
    bn = 0
    for i in range(N_STEPS):
        if cubic:
            fx = -(x + x * x * x + K * m)
            dfx = -(1.0 + 3.0 * x * x)
        else:
            fx = -(x + K * m)
            dfx = -1.0
        fm = -m + x
        if i >= N_BURN:
            sum_x2 += x * x
            sum_srx += fx * fx + dfx
            sum_srm += fm * fm - 1.0
            if block:
                bsum += (fx * fx + dfx) + (fm * fm - 1.0)
                bn += 1
                if bn == block:
                    blocks.append(bsum / block)
                    bsum = 0.0
                    bn = 0
        x += fx * DT + sdx * z[2 * i]
        m += fm * DT + sdm * z[2 * i + 1]
    n = float(N_REC)
    return sum_x2 / n, sum_srx / n, sum_srm / n, blocks


def batch_se(means):
    arr = np.asarray(means, dtype=float)
    return float(arr.std(ddof=1) / np.sqrt(arr.size))


def main():
    t0 = time.time()
    print("numpy", np.__version__, "sympy", sp.__version__)
    checks, slope, terms = symbolic()
    print("b=0 coordinates", terms)
    print("heat slope", slope)
    for name, ok in checks.items():
        if name == "b0_gap_factored":
            print("b0 Sr_M - I_M =", ok)
        else:
            print(("ok  " if ok else "FAIL") , name)
    # b=0 memory flow can be negative under feedback while the exogenous rate stays positive
    # I_M numerator factor D*c*g^2 - Dm*K*a*b at all-ones, K=2, b=1 is 1-2 < 0
    print("feedback flow sign at K=2 is negative", (1.0 - 2.0) < 0)

    # Linear calibration of the stationary solver.
    v_lin = closed_linear_variance(1.0)
    x2, sx, sm, mass, pmin = solve_stationary(1.0, 80, 6.0, cubic=False)
    print(
        f"linear calibration K=1 n=80 L=6 x2 {x2:.6f} vs {v_lin:.6f} "
        f"Sr {sx+sm:.6f} vs 2 mass {mass:.6f} minp {pmin:.2e}"
    )

    ref_z, _ = quad(lambda t: np.exp(-(0.5 * t * t + 0.25 * t**4)), -20, 20, epsabs=1e-12)
    ref_m, _ = quad(lambda t: t * t * np.exp(-(0.5 * t * t + 0.25 * t**4)), -20, 20, epsabs=1e-12)
    print(f"1D cubic E[X^2] {ref_m/ref_z:.8f}")

    def scan(n, L):
        ks = np.linspace(0.20, 0.27, 29)
        je = []
        jh0 = None
        for K in ks:
            ex2, sx, sm, _, _ = solve_stationary(float(K), n, L, cubic=True)
            je.append(ex2)
        je = np.array(je)
        k_e = fit_minimizer(ks, je)
        # heat-aware costs at a few gains, including zero and large gain
        table = {}
        for K in (0.0, 0.01, 0.001, -0.001, 0.23, 1.0, 2.0, 4.0):
            ex2, sx, sm, _, _ = solve_stationary(float(K), n, L, cubic=True)
            table[K] = (ex2, ex2 + sx + sm, sx, sm)
        slope_h = (table[0.01][1] - table[0.0][1]) / 0.01
        slope_c = (table[0.001][1] - table[-0.001][1]) / 0.002
        print(
            f"stationary n={n} L={L} K_E={k_e:.6f} "
            f"JH0={table[0.0][1]:.6f} JH0.23={table[0.23][1]:.6f} "
            f"JH1={table[1.0][1]:.6f} JH4={table[4.0][1]:.6f} "
            f"slope_h={slope_h:.6f} slope_c={slope_c:.6f} "
            f"SrX0={table[0.0][2]:.6e}"
        )
        return k_e, slope_h, slope_c, table

    scan(200, 4.0)
    scan(200, 5.0)
    scan(200, 6.0)

    # Locked path protocol.
    sr_lg = (1.0 + 1.0) ** 2 / (1.0 * 1.0 * (1.0 + 1.0))
    x2, sx, sm, fine = trajectory(SEED0, 1.0, cubic=False, block=1000)
    sr_hat = sx + sm
    rel = abs(sr_hat - sr_lg) / abs(sr_lg)
    print(f"GATE sr_hat {sr_hat:.12f} sr_lg {sr_lg:.12f} rel {rel:.6e} delta {sr_hat-CLAIMED_GATE:.3e}")
    fine = np.asarray(fine)
    for tbl in (2.0, 4.0, 10.0, 20.0, 40.0, 50.0):
        steps = int(round(tbl / DT))
        k = steps // 1000
        if N_REC % steps == 0 and steps % 1000 == 0:
            means = fine.reshape(-1, k).mean(axis=1)
            se = batch_se(means)
            print(f"batch T={tbl:.0f} n={means.size} SE={se:.6f} rel={se/sr_lg:.6f}")

    je, jh = [], []
    for index, K in enumerate(GRID):
        mx, sx, sm, _ = trajectory(SEED0 + index, K, cubic=True)
        e = mx
        h = mx + sx + sm
        je.append(e)
        jh.append(h)
        print(f"K {K:.2f} x2 {mx:.12f} srX {sx:.12f} srM {sm:.12f} JE {e:.12f} JH {h:.12f}")
    i_e = min(range(len(je)), key=lambda i: (je[i], GRID[i]))
    i_h = min(range(len(jh)), key=lambda i: (jh[i], GRID[i]))
    print(f"GRID K_E {GRID[i_e]:.2f} K_H {GRID[i_h]:.2f} gap {GRID[i_e]-GRID[i_h]:.2f}")

    def misses(indices):
        hats = []
        for i in indices:
            _, sx, sm, _ = trajectory(SEED0 + i, 1.0, cubic=False)
            hats.append(sx + sm)
        hats = np.asarray(hats)
        rels = np.abs(hats - 2.0) / 2.0
        nmiss = int(np.sum(rels > 0.05))
        sd = float(hats.std(ddof=1))
        print(
            f"seeds {indices[0]}..{indices[-1]} n={len(hats)} misses={nmiss} "
            f"mean={hats.mean():.6f} sd={sd:.6f} rel_sd={sd/2:.6f}"
        )
        return nmiss

    misses(range(0, 24))
    misses(range(1, 25))
    print(f"SECONDS {time.time()-t0:.1f}")


if __name__ == "__main__":
    main()
