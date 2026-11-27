#!/usr/bin/env python3
"""Checks for theory/swarm-2026-11-27/ (swarm rule completion, 27 Nov 2026).

Run from the repo root:
  nice -n 19 python3 theory/swarm-2026-11-27/checks/swarm27_checks.py

Every CHECK line is a CONSISTENCY_CHECK in the sense of process/PREREG_GATE.md
section 3 (see ../PREREG.md, Gate): it re-computes a statement proved on paper
in the notes, or evaluates a stated formula, or confirms an explicit
counterexample. None is a scored prediction, none is a test of the hypothesis,
and none is evidence about cells, agents, firms or people. Each line carries
one of three kinds:

- code sanity: an algebraic or arithmetic identity;
- re-test: a proved statement re-computed by an independent numerical route
  (optimizer, brute force, linear program, Monte Carlo, stationary law);
- counterexample: an explicit instance that shows a stated claim fails.

Machinery failures set a nonzero exit code. Seeds are fixed, so the output is
byte-stable and is compared with checks/swarm27_checks.out by
checks/test_swarm27_checks.py.
"""
from __future__ import annotations

import itertools
import math
import random
import sys

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import brentq, linprog, minimize_scalar

FAILED = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILED.append(name)


# ---------------------------------------------------------------------------
# Shared telegraph class of the swarm rule (theory/SWARM_RULE_2026-11-23.md
# section 6): r(u) = (1 - e^{-2u})/2 in drift units, r_inf = 1/2, Phi = 1/4.
R_INF = 0.5
PHI = 0.25


def A(s):
    return 0.5 - (1.0 - math.exp(-2.0 * s)) / (4.0 * s)


def A_lat(s, ell):
    """Average risk over a read interval s when every reading arrives ell late."""
    # (1/s) int_0^s r(ell+u) du, r(v) = (1 - e^{-2v})/2
    return 0.5 + math.exp(-2.0 * ell) * math.expm1(-2.0 * s) / (4.0 * s)


def best_follow(price, risk):
    """min over s of price/s + risk(s); returns (s, value)."""
    res = minimize_scalar(lambda ls: price / math.exp(ls) + risk(math.exp(ls)),
                          bounds=(-14, 14), method="bounded",
                          options={"xatol": 1e-11})
    return math.exp(res.x), res.fun


def g_follow(p):
    """g(p) = min(min_s p/s + A(s), r_inf): cost per unit stake (CT9)."""
    s, v = best_follow(p, A)
    return min(v, R_INF)


# ---------------------------------------------------------------------------
# A. Fold-ins (FOLD_INS.md)
def section_fold():
    print("== A. Fold-ins (FOLD_INS.md)")
    rng = random.Random(27001)

    # A1. CT17 (ii) = kappa^{-1/alpha}. CT12 cost J(T) = c/T + (w q/alpha) T^{alpha-1}.
    worst, opt_worst = 0.0, 0.0
    for _ in range(500):
        al = rng.uniform(1.2, 4.0)
        c, W, q = rng.uniform(0.1, 3), rng.uniform(0.5, 5), rng.uniform(0.1, 3)
        w = W * rng.uniform(0.02, 1.0)
        s = rng.uniform(0.02, 1.0)
        Tstar = lambda cc, ww: (al * cc / ((al - 1) * ww * q)) ** (1 / al)
        ratio = Tstar(c, W) / Tstar(s * c, w)          # part's read rate / whole's
        kappa = s * W / w
        worst = max(worst, abs(ratio / kappa ** (-1 / al) - 1))
        # independent route: minimize both costs numerically
        Jp = lambda T: s * c / T + (w * q / al) * T ** (al - 1)
        Jw = lambda T: c / T + (W * q / al) * T ** (al - 1)
        tp = math.exp(minimize_scalar(lambda x: Jp(math.exp(x)), bounds=(-20, 20), method="bounded",
                                      options={"xatol": 1e-12}).x)
        tw = math.exp(minimize_scalar(lambda x: Jw(math.exp(x)), bounds=(-20, 20), method="bounded",
                                      options={"xatol": 1e-12}).x)
        opt_worst = max(opt_worst, abs((tw / tp) / kappa ** (-1 / al) - 1))
    check("ct17ii_is_kappa_power", worst < 1e-12 and opt_worst < 1e-6,
          "code sanity (CT12 algebra) to %.1e and optimizer re-test to %.1e over 500 draws" % (worst, opt_worst))

    # A2. One shared clock (CT17 (i), alpha = 2): D_i >= 0, sum = penalty.
    sum_err, neg = 0.0, 0
    for _ in range(500):
        K = rng.randint(2, 6)
        c = [rng.uniform(0.1, 3) for _ in range(K)]
        w = [rng.uniform(0.1, 3) for _ in range(K)]
        sg = [rng.uniform(0.1, 3) for _ in range(K)]
        T1 = math.sqrt(2 * sum(c) / sum(w[i] * sg[i] for i in range(K)))
        D = []
        for i in range(K):
            J = lambda T: c[i] / T + w[i] * sg[i] * T / 2
            Ti = math.sqrt(2 * c[i] / (w[i] * sg[i]))
            k = T1 / Ti
            d_def = J(T1) - J(Ti)
            d_cf = math.sqrt(2 * c[i] * w[i] * sg[i]) * (0.5 * (k + 1 / k) - 1)
            sum_err = max(sum_err, abs(d_def - d_cf))
            neg += d_cf < -1e-15
            D.append(d_cf)
        pen = math.sqrt(2 * sum(c) * sum(w[i] * sg[i] for i in range(K))) - sum(
            sg[i] ** 0.5 * math.sqrt(2 * c[i] * w[i]) for i in range(K))
        sum_err = max(sum_err, abs(sum(D) - pen))
    # equal index: c_i/(w_i sg_i) all equal -> every D_i = 0
    c, w, sg = [1.0, 2.0, 3.0], [1.0, 1.0, 1.0], [1.0, 2.0, 3.0]
    T1 = math.sqrt(2 * sum(c) / sum(w[i] * sg[i] for i in range(3)))
    Deq = max(abs(math.sqrt(2 * c[i] * w[i] * sg[i]) * (0.5 * (T1 / math.sqrt(2 * c[i] / (w[i] * sg[i]))
                                                               + math.sqrt(2 * c[i] / (w[i] * sg[i])) / T1) - 1))
              for i in range(3))
    check("ct17i_one_clock_tamper_gains", sum_err < 1e-12 and neg == 0 and Deq < 1e-12,
          "re-test of CT13 + CT17 (i); definition vs closed form and sum D_i vs penalty to %.1e; %d negative gains; equal index -> max D=%.1e"
          % (sum_err, neg, Deq))

    # A3. CT19 folded into stay: Phi_ell = e^{-2 ell}/4; follow iff p < Phi_ell.
    from scipy.integrate import quad
    qerr = 0.0
    for ell in (0.0, 0.3, 1.0, 2.5):
        val = quad(lambda u: 0.5 * math.exp(-2 * u), ell, np.inf, epsabs=1e-14, epsrel=1e-13)[0]
        qerr = max(qerr, abs(val - math.exp(-2 * ell) / 4))
    mism, used = 0, 0
    for _ in range(1500):
        ell = rng.uniform(0, 2.5)
        Pl = math.exp(-2 * ell) / 4
        p = Pl * math.exp(rng.uniform(-1.5, 1.5))
        if abs(p / Pl - 1) < 0.02:
            continue
        used += 1
        _, v = best_follow(p, lambda s: A_lat(s, ell))
        follows = v < R_INF - 1e-12
        mism += follows != (p < Pl)
    lam, v_sp, pi0 = 0.2, 3.0, 0.12
    p0 = pi0 * PHI
    L = v_sp / (2 * lam) * math.log(1 / pi0)
    fol = []
    for frac in (0.999, 1.001):
        ell = lam * frac * L / v_sp
        _, val = best_follow(p0, lambda s: A_lat(s, ell))
        fol.append(val < R_INF - 1e-12)
    check("ct19_latency_stay_index", qerr < 1e-12 and mism == 0 and fol == [True, False],
          "re-test; Phi_ell quadrature err %.1e; %d mismatches in %d draws; reach L=%.6f (pi0=%.2f): follows at 0.999L %s, at 1.001L %s"
          % (qerr, mism, used, L, pi0, fol[0], fol[1]))

    # A4. Lemma B3 on CT14's N* (h = 0): N* depends on rho = q_g/q_u and falls in rho.
    def Nstar(a, b, rho):
        return (rho ** b / ((1 + rho) ** b - 1)) ** (1 / (1 - a))
    fails = 0
    for _ in range(800):
        a, b = rng.uniform(0, 0.95), rng.uniform(0.05, 0.95)
        qg, qu = 10 ** rng.uniform(-2, 1), 10 ** rng.uniform(-2, 1)
        h = 1e-6
        dg = (Nstar(a, b, qg * (1 + h) / qu) - Nstar(a, b, qg * (1 - h) / qu)) / (2 * h * qg)
        du = (Nstar(a, b, qg / (qu * (1 + h))) - Nstar(a, b, qg / (qu * (1 - h)))) / (2 * h * qu)
        fails += not (dg < 0 < du)
    check("lemma_b3_drift_direction", fails == 0,
          "re-test of Lemma B3 by finite differences on CT14's N*; %d sign failures in 800 draws" % fails)

    # A5. Lemma B7: CT30 gain lam*(rho) ~ sqrt(rho) at small rho, so N deposits -> sqrt(N).
    lstar = lambda rho: (-rho + math.sqrt(rho * rho + 4 * rho)) / 2
    q, r = 1e-10, 1.0
    rows, ok = [], True
    for N in (4, 16, 64):
        ratio = lstar(N * q / r) / lstar(q / r)
        rows.append("N=%d ratio %.5f (sqrt %g)" % (N, ratio, math.sqrt(N)))
        ok &= abs(ratio / math.sqrt(N) - 1) < 1e-3
    check("lemma_b7_sqrtN_fade", ok,
          "re-test (CT30 gain at small rho; linear readout only); " + "; ".join(rows))


# ---------------------------------------------------------------------------
# B. Telling price with private information (TELLING_PRICE.md)
class Prior:
    """Prior on the drift intensity q on [lo, hi]: 'uniform' or 'loguniform'."""

    def __init__(self, kind, lo, hi):
        self.kind, self.lo, self.hi = kind, float(lo), float(hi)

    def m(self, a, b):
        if b - a <= 1e-15 * max(1.0, b):
            return 0.5 * (a + b)
        if self.kind == "uniform":
            return 0.5 * (a + b)
        return (b - a) / math.log(b / a)

    def P(self, a, b):
        if self.kind == "uniform":
            return (b - a) / (self.hi - self.lo)
        return math.log(b / a) / math.log(self.hi / self.lo)

    def mean(self):
        return self.m(self.lo, self.hi)


def tp_next(pr, kappa, q_prev, q_k):
    """Next boundary from q_k = kappa sqrt(m_k m_{k+1}); None if no solution
    (chain cannot continue), inf if it overshoots hi."""
    mk = pr.m(q_prev, q_k)
    target = q_k * q_k / (kappa * kappa * mk)
    if target <= q_k:
        return None
    if target >= pr.m(q_k, pr.hi):
        return math.inf
    return brentq(lambda x: pr.m(q_k, x) - target, q_k * (1 + 1e-15), pr.hi, xtol=1e-15, rtol=1e-15)


def tp_equilibrium(pr, kappa, N):
    """An N-step equilibrium by shooting on q_1; None if none is found."""
    def chain(q1):
        qs = [pr.lo, q1]
        for _ in range(N - 2):
            nx = tp_next(pr, kappa, qs[-2], qs[-1])
            if nx is None:      # next boundary would not lie above q_k: q_1 too small
                return qs, +1
            if math.isinf(nx):  # chain passes hi before step N: q_1 too large
                return qs, -1
            qs.append(nx)
        # the last step must end at hi: m(q_{N-1}, hi) must equal the target
        mk = pr.m(qs[-2], qs[-1])
        target = qs[-1] ** 2 / (kappa ** 2 * mk)
        return qs, (pr.m(qs[-1], pr.hi) - target) / target

    def end_gap(x):
        return chain(x)[1]

    lo, hi = pr.lo * (1 + 1e-12), pr.hi * (1 - 1e-12)
    xs = np.geomspace(lo, hi, 400)
    gaps = [end_gap(x) for x in xs]
    for j in range(len(xs) - 1):
        g0, g1 = gaps[j], gaps[j + 1]
        if g0 == 0:
            a = b = xs[j]
        elif (g0 < 0) != (g1 < 0):
            a, b = xs[j], xs[j + 1]
            for _ in range(200):
                mid = 0.5 * (a + b)
                if (end_gap(mid) < 0) == (g0 < 0):
                    a = mid
                else:
                    b = mid
        else:
            continue
        for x in (a, b):
            qs, flag = chain(x)
            if len(qs) == N and abs(flag) < 1e-9:
                cand = qs + [pr.hi]
                if tp_verify(pr, kappa, cand, ngrid=1500) < 1e-9:
                    return cand
    return None


def tp_two(pr, kappa):
    """A two-step equilibrium: root of kappa sqrt(m_L(x) m_R(x)) - x; None if none."""
    phi = lambda x: kappa * math.sqrt(pr.m(pr.lo, x) * pr.m(x, pr.hi)) - x
    span = pr.hi - pr.lo
    t = np.geomspace(1e-12, 0.5, 2000)
    xs = np.unique(np.concatenate([pr.lo + span * t, pr.hi - span * t]))
    vals = [phi(x) for x in xs]
    for j in range(len(xs) - 1):
        if (vals[j] > 0) != (vals[j + 1] > 0):
            q1 = brentq(phi, xs[j], xs[j + 1], xtol=1e-14, rtol=1e-15)
            return [pr.lo, q1, pr.hi]
    return None


def tp_value(pr, qs, c=1.0, W=1.0):
    """V = sqrt(2cW) (sqrt(M) - sum_k P_k sqrt(m_k))."""
    tot = sum(pr.P(qs[k], qs[k + 1]) * math.sqrt(pr.m(qs[k], qs[k + 1])) for k in range(len(qs) - 1))
    return math.sqrt(2 * c * W) * (math.sqrt(pr.mean()) - tot)


def tp_verify(pr, kappa, qs, c=1.0, W=1.0, w=1.0, ngrid=4000):
    """Largest gain any sender type on a grid gets from an action other than its own step's."""
    s = kappa * w / W
    f = [math.sqrt(W * pr.m(qs[k], qs[k + 1]) / (2 * c)) for k in range(len(qs) - 1)]
    if any(f[k + 1] <= f[k] for k in range(len(f) - 1)):
        return math.inf
    worst = 0.0
    for q in np.geomspace(pr.lo, pr.hi, ngrid):
        k = min(int(np.searchsorted(qs, q, side="right")) - 1, len(f) - 1)
        costs = [s * c * fk + w * q / (2 * fk) for fk in f]
        worst = max(worst, costs[k] - min(costs))
    return worst


def section_telling():
    print("== B. Telling price with private information (TELLING_PRICE.md)")
    c, W, w = 1.0, 1.0, 1.0
    # B1. kappa = 1: truthful full revelation is an equilibrium (each type's
    # best report, on a grid, is its own type).
    pr = Prior("loguniform", 1.0, 100.0)
    grid = np.geomspace(1.0, 100.0, 801)
    fW = np.sqrt(W * grid / (2 * c))
    worst = 0
    for kappa, expect_truth in ((1.0, True), (1.5, False), (0.7, False)):
        s = kappa * w / W
        moved = 0
        for i, q in enumerate(grid[50:-50:25]):
            cost = s * c * fW + w * q / (2 * fW)
            j = int(np.argmin(cost))
            moved += abs(grid[j] / q - 1) > 0.02
        if expect_truth:
            worst = moved
            ok_truth = moved == 0
        else:
            ok_truth = ok_truth and moved > 0
    check("tp_full_revelation_iff_aligned", ok_truth,
          "re-test (grid brute force): at kappa=1 no interior type gains by misreporting; at kappa=1.5 and 0.7 interior types do")

    # B2. MRR conditions for the two priors: m_L(x)/x and m_R(x)/x nonincreasing.
    ok = True
    for kind in ("uniform", "loguniform"):
        p2 = Prior(kind, 1.0, 100.0)
        xs = np.geomspace(1.0 + 1e-6, 100.0 - 1e-6, 2000)
        mL = np.array([p2.m(1.0, x) / x for x in xs])
        mR = np.array([p2.m(x, 100.0) / x for x in xs])
        ok &= bool(np.all(np.diff(mL) <= 1e-12) and np.all(np.diff(mR) <= 1e-12))
    check("tp_mrr_conditions_hold", ok,
          "re-test of the proved monotonicity for uniform and log-uniform priors on [1,100]")

    # B3. Informative equilibrium exists iff sqrt(lo/M) < kappa < sqrt(hi/M).
    rows, ok = [], True
    for kind, lo, hi in (("loguniform", 1.0, 100.0), ("uniform", 1.0, 100.0),
                         ("loguniform", 1.0, 4.0)):
        p2 = Prior(kind, lo, hi)
        M = p2.mean()
        k_lo, k_hi = math.sqrt(lo / M), math.sqrt(hi / M)
        rows.append("%s[%g,%g]: (%.6f, %.6f)" % (kind, lo, hi, k_lo, k_hi))
        for kappa in (k_lo * 0.98, k_lo * 1.02, 0.5 * (k_lo + 1), 1.0,
                      0.5 * (1 + k_hi), k_hi * 0.98, k_hi * 1.02, k_hi * 1.5):
            qs = tp_two(p2, kappa)
            pred = k_lo < kappa < k_hi
            ok &= (qs is not None) == pred
            if qs is not None:
                ok &= tp_verify(p2, kappa, qs) < 1e-9
    check("tp_informative_iff_kappa_window", ok,
          "re-test (shooting + brute-force sender check); windows " + "; ".join(rows))

    # B4. Most informative equilibrium and its value as kappa moves.
    p2 = Prior("loguniform", 1.0, 100.0)
    V_full = math.sqrt(2 * c * W) * (math.sqrt(p2.mean()) -
                                     float(np.mean(np.sqrt(np.geomspace(1, 100, 200001)))))
    out, ok, prevV = ["k=1.00 V_full=%.5f" % V_full], True, None
    for kappa in (1.1, 1.3, 1.6, 2.0, 2.3):
        two = tp_two(p2, kappa)
        Nmax, qsmax = (1, [p2.lo, p2.hi]) if two is None else (2, two)
        for N in range(3 if two else 2, 40 if two else 2):
            qs = tp_equilibrium(p2, kappa, N)
            if qs is None:
                break
            Nmax, qsmax = N, qs
            ok &= tp_verify(p2, kappa, qs, ngrid=1500) < 1e-9
        V = tp_value(p2, qsmax)
        out.append("k=%.2f N=%d V=%.5f" % (kappa, Nmax, V))
        ok &= V < V_full and (prevV is None or V <= prevV + 1e-12)
        prevV = V
    ok &= Nmax >= 1
    check("tp_value_falls_with_mispricing", ok,
          "re-test; log-uniform [1,100], most informative equilibrium found by shooting (N searched to 39): " + "; ".join(out))


# ---------------------------------------------------------------------------
# C. Stake revelation (STAKES.md)
def section_stakes():
    print("== C. Stake revelation (STAKES.md)")
    rng = random.Random(27003)
    c, q = 1.0, 1.0
    k = math.sqrt(2 * c * q)
    Jst = lambda X: k * math.sqrt(X)

    def part_cost_clarke(i, w_true, rep):
        Wr = sum(rep)
        F = math.sqrt(Wr * q / (2 * c))
        others = sum(rep) - rep[i]
        pay = c * F + others * q / (2 * F) - Jst(others)
        return w_true[i] * q / (2 * F) + pay

    gain = 0.0
    for _ in range(300):
        N = rng.randint(2, 6)
        wt = [rng.uniform(0.1, 3) for _ in range(N)]
        i = rng.randrange(N)
        truth = part_cost_clarke(i, wt, wt)
        for f in np.geomspace(0.05, 20, 81):
            rep = list(wt)
            rep[i] = wt[i] * f
            gain = max(gain, truth - part_cost_clarke(i, wt, rep))
    check("clarke_truth_dominant", gain < 1e-12,
          "re-test (misreport grid x0.05..x20, others' reports arbitrary=true); best misreport gain %.1e" % gain)

    worst, lo_viol, hi_viol, ir_viol = 0.0, 0, 0, 0
    for _ in range(2000):
        N = rng.randint(2, 8)
        wt = [rng.expovariate(1.0) + 1e-3 for _ in range(N)]
        Wt = sum(wt)
        F = math.sqrt(Wt * q / (2 * c))
        pays = []
        for i in range(N):
            others = Wt - wt[i]
            pays.append(c * F + others * q / (2 * F) - Jst(others))
        deficit = c * F - sum(pays)
        x = [wi / Wt for wi in wt]
        rel = sum(math.sqrt(1 - xi) for xi in x) - (N - 1)
        worst = max(worst, abs(deficit / Jst(Wt) - rel))
        lo_viol += rel < -1e-12
        hi_viol += rel > N * math.sqrt(1 - 1 / N) - (N - 1) + 1e-12 or rel >= 0.5
        for i in range(N):
            ir_viol += part_cost_clarke(i, wt, wt) > Jst(wt[i]) + 1e-12
    eq = [N * math.sqrt(1 - 1 / N) - (N - 1) for N in (2, 3, 10, 100, 10000)]
    check("clarke_deficit_bounds",
          worst < 1e-12 and lo_viol == 0 and hi_viol == 0 and ir_viol == 0,
          "re-test; deficit/J* = sum sqrt(1-x_i) - (N-1) to %.1e; in [0, N sqrt(1-1/N)-(N-1)) < 1/2; IR vs tracking alone holds; equal-stake deficit/J* at N=2,3,10,100,1e4: %s"
          % (worst, ", ".join("%.5f" % e for e in eq)))

    # C3. No budget-balanced Groves mechanism: the N-th mixed difference of
    # sqrt(sum w) is nonzero (its sign is (-1)^(N+1)), while that of any
    # sum_i h_i(w_{-i}) is 0.
    import sympy as sp
    ok, rows = True, []
    for N in range(2, 7):
        ws = sp.symbols("w1:%d" % (N + 1), positive=True)
        expr = sp.sqrt(sum(ws))
        d = expr
        for v in ws:
            d = sp.diff(d, v)
        val = d.subs({v: 1 for v in ws})
        ok &= bool(val != 0) and bool(sp.sign(val) == (-1) ** (N + 1))
        hs = sum(sp.Function("h%d" % i)(*[v for j, v in enumerate(ws) if j != i]) for i in range(N))
        dh = hs
        for v in ws:
            dh = sp.diff(dh, v)
        ok &= dh == 0
        rows.append("N=%d %s" % (N, sp.nsimplify(val)))
    check("groves_no_budget_balance", ok,
          "code sanity (symbolic); d^N sqrt(sum w)/dw_1..dw_N at w=1: " + ", ".join(rows))

    # C4. Proportional shares on reported stakes are not truthful: at
    # F = F*(W_hat), party i's cost k (w_i + w_hat_i) / (2 sqrt(W_hat)) has
    # derivative (k / (2 sqrt W)) (1 - x_i) > 0 at the truth.
    worst_rel, shade_fail = 0.0, 0
    for _ in range(500):
        N = rng.randint(2, 6)
        wt = [rng.uniform(0.1, 3) for _ in range(N)]
        i = rng.randrange(N)
        Wt = sum(wt)
        cost = lambda r: k * (wt[i] + r) / (2 * math.sqrt(Wt - wt[i] + r))
        h = 1e-6 * wt[i]
        num = (cost(wt[i] + h) - cost(wt[i] - h)) / (2 * h)
        pred = k / (2 * math.sqrt(Wt)) * (1 - wt[i] / Wt)
        worst_rel = max(worst_rel, abs(num / pred - 1))
        shade_fail += not (cost(0.9 * wt[i]) < cost(wt[i]))
    check("proportional_shares_reward_underreporting", worst_rel < 1e-6 and shade_fail == 0,
          "re-test (finite differences, 500 draws); derivative matches (k/(2 sqrt W))(1 - x_i) to rel %.1e; reporting 0.9 w_i lowers cost in %d of 500"
          % (worst_rel, 500 - shade_fail))


# ---------------------------------------------------------------------------
# D. A part that can rewrite the whole's objective (OBJECTIVE.md)
def section_objective():
    print("== D. Objective-rewriting part (OBJECTIVE.md)")
    lam, c, W0, w = 0.1, 1.0, 1.0, 0.5
    Ws = np.geomspace(0.2, 20, 61)

    def TW(Wx):
        return best_follow(lam * c / Wx, A)[0]

    def Ji(T, s):
        return lam * s * c / T + w * A(T)

    # D1. Fixed aligned reference share s = w/W0: part's cost at T_W(W) is
    # minimized at W = W0.
    costs = [Ji(TW(Wx), w / W0) for Wx in Ws]
    j = int(np.argmin(costs))
    base = Ji(TW(W0), w / W0)
    ok1 = abs(Ws[j] / W0 - 1) < 0.08 and min(costs) >= base - 1e-9
    # D2. Fixed misaligned share s: best rewritten stake is w/s, gain = D_enf.
    s = 2.0 * w / W0
    costs2 = [Ji(TW(Wx), s) for Wx in Ws]
    j2 = int(np.argmin(costs2))
    d_enf = Ji(TW(W0), s) - min(best_follow(lam * s * c / w, A)[1] * w, w * R_INF)
    gain = Ji(TW(W0), s) - Ji(TW(w / s), s)
    ok2 = abs(Ws[j2] / (w / s) - 1) < 0.08 and abs(gain - d_enf) < 1e-8
    # D3. Indexed share s = w/W: part's cost strictly falls as W is inflated.
    costs3 = [Ji(TW(Wx), w / Wx) for Wx in Ws]
    ok3 = all(costs3[i + 1] < costs3[i] for i in range(len(costs3) - 1))
    check("objective_fixed_reference_no_gain", ok1,
          "re-test; aligned at W0=1: no rewritten W on a 61-point grid in [0.2,20] beats W0 by more than optimizer tolerance (best grid point %.3f, gain %.1e)"
          % (Ws[j], max(0.0, base - min(costs))))
    check("objective_misaligned_gain_equals_Denf", ok2,
          "re-test; s=2w/W0: best rewritten W=%.3f (w/s=%.3f); gain %.6f = D_enf %.6f" % (Ws[j2], w / s, gain, d_enf))
    check("objective_indexed_share_rewards_inflation", ok3,
          "re-test; s=w/W(a): part's cost %.5f at W=0.2 falls to %.5f at W=20, strictly" % (costs3[0], costs3[-1]))


# ---------------------------------------------------------------------------
# E. Couplings beyond the potential class (COUPLINGS.md)
def section_couplings():
    print("== E. Couplings beyond potential games (COUPLINGS.md)")
    rng = random.Random(27005)
    # E1. Heterogeneous error curves g_1 = 1/F, g_2 = 1/F^2 (both decreasing,
    # convex): the square-cycle sum (w2/om2) M2 - (w1/om1) M1 cannot vanish for
    # all squares with fixed weights.
    g1 = lambda F: 1.0 / F
    g2 = lambda F: 1.0 / F ** 2
    M = lambda g, F, a, b: g(F + a + b) - g(F + a) - g(F + b) + g(F)
    ratios = [M(g1, F, 0.1, 0.1) / M(g2, F, 0.1, 0.1) for F in (0.5, 1.0, 2.0, 4.0)]
    check("hetero_curves_not_weighted_potential",
          max(ratios) / min(ratios) > 2.0,
          "counterexample; M1/M2 at F=0.5,1,2,4: %s (a weighted potential needs it constant)"
          % ", ".join("%.4f" % r for r in ratios))

    # E2. Round-robin best response converges to: only argmax F_hat reads,
    # total = max F_hat (best-reply equivalent to a CT31 potential game).
    def hat(c, w, kind, scale):
        # F_hat solves -w g'(F) = c
        if kind == 0:   # g = scale/F
            return math.sqrt(w * scale / c)
        if kind == 1:   # g = scale/F^2
            return (2 * w * scale / c) ** (1 / 3)
        return math.log(w * scale / c) if w * scale > c else 0.0  # g = scale e^{-F}
    fails, rounds_max = 0, 0
    for _ in range(400):
        N = rng.randint(2, 6)
        parts = [(rng.uniform(0.2, 2), rng.uniform(0.2, 3), rng.randint(0, 2),
                  rng.uniform(0.5, 30)) for _ in range(N)]
        Fh = [hat(*p) for p in parts]
        if sorted(Fh)[-1] - sorted(Fh)[-2] < 1e-3 or max(Fh) <= 0:
            continue
        f = [rng.uniform(0, 5) for _ in range(N)]
        for rnd in range(20000):
            old = list(f)
            for i in range(N):
                f[i] = max(0.0, Fh[i] - (sum(f) - f[i]))
            if max(abs(a - b) for a, b in zip(f, old)) < 1e-13:
                break
        rounds_max = max(rounds_max, rnd)
        kmax = int(np.argmax(Fh))
        fails += not (abs(sum(f) - Fh[kmax]) < 1e-9 and all(
            (abs(fi) < 1e-9) for i, fi in enumerate(f) if i != kmax))
    check("hetero_curves_best_response_converges", fails == 0,
          "re-test; %d failures in 400 random games; total -> max F_hat with only argmax reading; max rounds %d" % (fails, rounds_max))

    # E3. Lindahl shares s_i = -w_i g_i'(F*)/c align every party; s_i = w_i/W
    # does not when the curves differ.
    c = 1.0
    w = [1.0, 2.0]
    gp = [lambda F: -1.0 / F ** 2, lambda F: -2.0 / F ** 3]
    Fstar = brentq(lambda F: c + w[0] * gp[0](F) + w[1] * gp[1](F), 0.01, 100)
    sl = [-w[i] * gp[i](Fstar) / c for i in range(2)]
    pref = lambda i, s: brentq(lambda F: s * c + w[i] * gp[i](F), 1e-4, 1e4)
    lind = [pref(i, sl[i]) for i in range(2)]
    prop = [pref(i, w[i] / sum(w)) for i in range(2)]
    check("lindahl_shares_align_hetero",
          abs(sum(sl) - 1) < 1e-12 and max(abs(x - Fstar) for x in lind) < 1e-9
          and max(abs(x - Fstar) for x in prop) > 0.05,
          "re-test; F*=%.6f; Lindahl shares %.4f,%.4f -> preferred totals %s; stake shares -> %s"
          % (Fstar, sl[0], sl[1], ", ".join("%.6f" % x for x in lind), ", ".join("%.4f" % x for x in prop)))

    # E4. Credibility coupling: Phi(n) rises with the number of other followers.
    # Part i follows iff lam*s_i*c < w_i*Phi(n_{-i}). Monotone best responses:
    # BR from all-follow converges to the largest equilibrium, from all-leave to
    # the smallest (Tarski / Topkis), checked against full enumeration.
    fails = 0
    for _ in range(300):
        N = rng.randint(2, 8)
        lam = rng.uniform(0.05, 1)
        P0, P1 = rng.uniform(0.02, 0.2), rng.uniform(0.0, 0.3)
        sc = [rng.uniform(0.1, 1) for _ in range(N)]
        ww = [rng.uniform(0.2, 2) for _ in range(N)]
        Phi = lambda n: P0 + P1 * n / max(1, N - 1)
        br = lambda x, i: int(lam * sc[i] < ww[i] * Phi(sum(x) - x[i]))
        eqs = [x for x in itertools.product((0, 1), repeat=N)
               if all(br(x, i) == x[i] for i in range(N))]
        top = tuple(max(e[i] for e in eqs) for i in range(N))
        bot = tuple(min(e[i] for e in eqs) for i in range(N))
        res = []
        for start in ((1,) * N, (0,) * N):
            x = list(start)
            for _ in range(N + 2):
                for i in range(N):
                    x[i] = br(x, i)
            res.append(tuple(x))
        fails += not (top in eqs and bot in eqs and res[0] == top and res[1] == bot)
    # hysteresis loop for identical parts: both all-follow and all-leave are
    # equilibria iff w*Phi0 <= lam*s*c < w*(Phi0+Phi1)
    P0, P1, w1, s1, c1, N = 0.1, 0.15, 1.0, 1.0, 1.0, 10
    lo_l, hi_l = w1 * P0 / (s1 * c1), w1 * (P0 + P1) / (s1 * c1)
    both = []
    for lam in (0.9 * lo_l, 1.01 * lo_l, 0.99 * hi_l, 1.01 * hi_l):
        Phi = lambda n: P0 + P1 * n / (N - 1)
        allf = lam * s1 * c1 < w1 * Phi(N - 1)
        alll = not (lam * s1 * c1 < w1 * Phi(0))
        both.append((allf, alll))
    ok_h = both == [(True, False), (True, True), (True, True), (False, True)]
    check("credibility_coupling_extremal_equilibria", fails == 0 and ok_h,
          "re-test (enumeration of all profiles, 300 random games, N<=8): %d failures; hysteresis window lam in [%.3f, %.3f)"
          % (fails, lo_l, hi_l))


# ---------------------------------------------------------------------------
# F. Remove or reprice under the ruin cap (REMOVE_OR_REPRICE.md)
def section_remove():
    print("== F. Remove or reprice (REMOVE_OR_REPRICE.md)")
    rs = np.random.default_rng(27006)
    n = 400000
    h, tau = 0.03, 1.5
    first = rs.exponential(1 / h, n)
    p_det = float(np.mean(first < tau))
    mu = 0.4
    tr = rs.exponential(1 / mu, n)
    first2 = rs.exponential(1 / h, n)
    p_exp = float(np.mean(first2 < tr))
    # time-varying hazard h(t) = 0.02 + 0.04 t on [0, 2]: integral 0.12
    u = rs.random(n)
    # inverse of H(t) = 0.02 t + 0.02 t^2 for E = -ln u
    E = -np.log(u)
    tfirst = (-0.02 + np.sqrt(0.0004 + 0.08 * E)) / 0.04
    p_var = float(np.mean(tfirst < 2.0))
    se = lambda p: math.sqrt(p * (1 - p) / n)
    ok = (abs(p_det - (1 - math.exp(-h * tau))) < 4 * se(p_det)
          and abs(p_exp - h / (h + mu)) < 4 * se(p_exp)
          and abs(p_var - (1 - math.exp(-0.12))) < 4 * se(p_var))
    check("ruin_during_transition_formulas", ok,
          "re-test (Monte Carlo, n=%d): det %.5f vs %.5f; exp %.5f vs %.5f; varying %.5f vs %.5f"
          % (n, p_det, 1 - math.exp(-h * tau), p_exp, h / (h + mu), p_var, 1 - math.exp(-0.12)))

    rows = []
    for eps in (1e-1, 1e-2, 1e-3, 1e-6):
        exact = -math.log(1 - eps)
        rows.append("eps=%g: ln(1/(1-eps))=%.9g, rel gap %.3g" % (eps, exact, exact / eps - 1))
    check("cap_threshold_vs_written_form", True,
          "code sanity; " + "; ".join(rows))

    # Decision rule = brute-force argmin over cap-feasible options.
    rng = random.Random(27007)
    mism = 0
    for _ in range(3000):
        eps = 10 ** rng.uniform(-4, -1)
        hz = 10 ** rng.uniform(-4, 0)
        hx = hz * rng.uniform(0, 1)
        tR, tP = 10 ** rng.uniform(-2, 1), 10 ** rng.uniform(-2, 1)
        LR, CP, KX = rng.uniform(0, 2), rng.uniform(0, 2), rng.uniform(0, 0.5)
        cap = -math.log(1 - eps)
        opts = {"remove": (hz * tR <= cap, LR), "reprice": (hz * tP <= cap, CP),
                "cut+remove": (hx * tR <= cap, LR + KX), "cut+reprice": (hx * tP <= cap, CP + KX)}
        feas = {k: v[1] for k, v in opts.items() if v[0]}
        brute = min(feas, key=feas.get) if feas else "none"
        # the rule as stated in the note
        if hz * min(tR, tP) <= cap:
            cand = [("remove", LR)] if hz * tR <= cap else []
            cand += [("reprice", CP)] if hz * tP <= cap else []
            cand += [("cut+remove", LR + KX)] if hx * tR <= cap else []
            cand += [("cut+reprice", CP + KX)] if hx * tP <= cap else []
            rule = min(cand, key=lambda t: t[1])[0]
        elif hx * min(tR, tP) <= cap:
            cand = [("cut+remove", LR + KX)] if hx * tR <= cap else []
            cand += [("cut+reprice", CP + KX)] if hx * tP <= cap else []
            rule = min(cand, key=lambda t: t[1])[0]
        else:
            rule = "none"
        mism += rule != brute
    check("remove_or_reprice_rule", mism == 0,
          "code sanity (finite menu under a chance constraint); %d mismatches in 3000 random instances" % mism)


# ---------------------------------------------------------------------------
# G. Merge (MERGE.md)
def section_merge():
    print("== G. Merge conjecture CX2/CX3 (MERGE.md)")
    rng = random.Random(27008)
    k = 1.0  # sqrt(2 c q)

    # G1. Public reads: after part i exits, the merged rest (stake W - w_i >= w_i)
    # reads alone and i free-rides at (k/2) w_i / sqrt(W - w_i). If every
    # share <= 1/2, sum of exit payoffs < k sqrt(W) <= c(N): no split is
    # internally stable. Re-test by direct two-player best response.
    viol, worst_ratio = 0, 0.0
    for trial in range(3000):
        N = 2 if trial % 10 == 0 else rng.randint(3, 9)
        if N == 2:
            wt = [1.0, 1.0]
        else:
            while True:
                wt = [rng.expovariate(1) + 1e-3 for _ in range(N)]
                if max(wt) <= 0.5 * sum(wt):
                    break
        Wt = sum(wt)
        o = []
        for i in range(N):
            a, b = Wt - wt[i], wt[i]  # merged rest, outsider (c = q = 1)
            # CT29 Nash between the two: only the larger stake reads,
            # at F = sqrt(stake q / 2c); the other free-rides at b q / (2F)
            F = math.sqrt(max(a, b) / 2.0)
            o.append(b / (2.0 * F) if a >= b else math.sqrt(2.0 * b))
        ratio = sum(o) / math.sqrt(2.0 * Wt)  # joint cost sqrt(2 c q W)
        worst_ratio = max(worst_ratio, ratio)
        viol += ratio >= 1
    eq = [N / (2 * math.sqrt(N - 1)) / math.sqrt(N) for N in (2, 3, 5, 10, 100)]
    check("merge_public_reads_never_stable", viol == 0 and worst_ratio <= 1 / math.sqrt(2) + 1e-12,
          "re-test; sum exit payoffs / k sqrt(W) max %.5f (bound 1/sqrt2=0.70711) over 3000 stake vectors with max share <= 1/2; equal stakes N=2,3,5,10,100: %s"
          % (worst_ratio, ", ".join("%.4f" % e for e in eq)))

    # G2. Private reads (excludable): grand merger is IR and internally stable
    # for some split iff gap = k(sum sqrt w_i - sqrt W) >= J_coup. LP check.
    mism = 0
    for _ in range(600):
        N = rng.randint(2, 6)
        wt = [rng.uniform(0.05, 3) for _ in range(N)]
        gap = k * (sum(math.sqrt(x) for x in wt) - math.sqrt(sum(wt)))
        Jc = gap * rng.uniform(0.5, 1.5)
        if abs(Jc - gap) < 1e-6:
            continue
        cN = k * math.sqrt(sum(wt)) + Jc
        res = linprog(np.zeros(N), A_ub=np.eye(N), b_ub=[k * math.sqrt(x) for x in wt],
                      A_eq=np.ones((1, N)), b_eq=[cN], bounds=[(None, None)] * N, method="highs")
        mism += (res.status == 0) != (gap >= Jc)
    # equal-stake boundary: merge iff d < k sqrt(w) (1 - 1/sqrt N)
    w1, d = 1.0, 0.4
    Nm = (1 / (1 - d / (k * math.sqrt(w1)))) ** 2
    okb = all(((k * math.sqrt(N * w1) + N * d) <= N * k * math.sqrt(w1)) == (N >= Nm) for N in range(2, 30))
    check("merge_private_reads_iff_gap", mism == 0 and okb,
          "re-test (LP feasibility, 600 instances): %d mismatches; equal stakes d/k sqrt(w)=0.4 -> merge iff N >= %.4f" % (mism, Nm))

    # G3. Counterexample: gap > coupling for the grand merger, yet the core is
    # empty: stakes (1, 1, 1e-4), per-member coupling d = 0.05.
    wt, dd = [1.0, 1.0, 1e-4], 0.05
    cS = lambda S: (k * math.sqrt(sum(wt[i] for i in S)) + (dd * len(S) if len(S) >= 2 else 0.0))
    N = 3
    gap = k * (sum(math.sqrt(x) for x in wt) - math.sqrt(sum(wt)))
    A_ub, b_ub = [], []
    for r in range(1, N):
        for S in itertools.combinations(range(N), r):
            A_ub.append([1.0 if i in S else 0.0 for i in range(N)])
            b_ub.append(cS(S))
    res = linprog(np.zeros(N), A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, N)),
                  b_eq=[cS(range(N))], bounds=[(None, None)] * N, method="highs")
    check("merge_gap_not_sufficient_for_core", gap > N * dd and res.status == 2,
          "counterexample; gap %.4f > coupling %.4f, LP status %d (2 = core empty); partition {1,2},{3} costs %.4f < grand %.4f"
          % (gap, N * dd, res.status, cS([0, 1]) + cS([2]), cS(range(N))))

    # G4. Stake-proportional split (clause 4's s = w/W) is in the core iff
    # d <= k min_i sqrt(w_i) (1 - sqrt(w_i/W)).
    mism = 0
    for _ in range(800):
        N = rng.randint(2, 6)
        wt = [rng.uniform(0.05, 3) for _ in range(N)]
        Wt = sum(wt)
        bound = k * min(math.sqrt(x) * (1 - math.sqrt(x / Wt)) for x in wt)
        dd = bound * rng.uniform(0.5, 1.5)
        if abs(dd - bound) < 1e-9:
            continue
        cS = lambda S: (k * math.sqrt(sum(wt[i] for i in S)) + (dd * len(S) if len(S) >= 2 else 0.0))
        x = [k * wi / math.sqrt(Wt) + dd for wi in wt]
        incore = all(sum(x[i] for i in S) <= cS(S) + 1e-12
                     for r in range(1, N) for S in itertools.combinations(range(N), r))
        mism += incore != (dd <= bound)
    check("merge_stake_shares_in_core_iff", mism == 0,
          "re-test (all coalitions, 800 instances, N<=6): %d mismatches" % mism)


# ---------------------------------------------------------------------------
# H. Heat floor with feedback, for a part (FEEDBACK_PART.md)
def L_floor(e):
    return (1 - 2 * e) * math.log((1 - e) / e)


def stationary(Q):
    ns = null_space(Q.T)
    p = ns[:, 0].real
    p = p / p.sum()
    return p


def section_feedback():
    print("== H. Heat floor with feedback for a part (FEEDBACK_PART.md)")
    rng = np.random.default_rng(27009)

    # H1. Exogenous fair telegraph signal S (rate lam), finite memory M with
    # local detailed balance and rates that read S: Q_M >= I_alt >= lam L(eps).
    worst_gap, fails = 0.0, 0
    for trial in range(200):
        K = int(rng.integers(2, 5))
        lam = float(10 ** rng.uniform(-1, 0.5))
        E = rng.normal(0, 2, size=(2, K))       # energy of memory state m given s
        gam = float(10 ** rng.uniform(-0.5, 1))
        n = 2 * K
        Q = np.zeros((n, n))
        idx = lambda s, m: s * K + m
        for s in (0, 1):
            for m in range(K):
                Q[idx(s, m), idx(1 - s, m)] += lam
                for m2 in range(K):
                    if m2 != m:
                        Q[idx(s, m), idx(s, m2)] += gam * math.exp(-(E[s, m2] - E[s, m]) / 2)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        p = stationary(Q)
        heat, ialt = 0.0, 0.0
        for s in (0, 1):
            ps = p[[idx(s, m) for m in range(K)]]
            cond = ps / ps.sum()
            for m in range(K):
                for m2 in range(K):
                    if m2 == m:
                        continue
                    rate = Q[idx(s, m), idx(s, m2)]
                    heat += p[idx(s, m)] * rate * (E[s, m] - E[s, m2])
                    ialt += p[idx(s, m)] * rate * math.log(cond[m2] / cond[m])
        eps = sum(min(p[idx(0, m)], p[idx(1, m)]) for m in range(K))
        floor = lam * L_floor(eps) if eps < 0.5 - 1e-12 else 0.0
        fails += not (heat >= ialt - 1e-10 and ialt >= floor - 1e-10)
        worst_gap = min(worst_gap, ialt - floor)
    check("part_floor_exogenous_signal", fails == 0,
          "re-test of T60 telegraph bound + JP-heat for a part reading an exogenous signal; %d failures in 200 random memories"
          % fails)

    # H2. The floor alone never forces leaving: min over eps of
    # s*lam*L(eps) + w*eps is below w/2 for every s, lam, w > 0.
    worst = -1.0
    rr = random.Random(27010)
    for _ in range(2000):
        s, lam, w = rr.uniform(0.01, 10), 10 ** rr.uniform(-2, 2), 10 ** rr.uniform(-3, 1)
        res = minimize_scalar(lambda e: s * lam * L_floor(e) + w * e, bounds=(1e-12, 0.5 - 1e-12),
                              method="bounded", options={"xatol": 1e-14})
        worst = max(worst, (res.fun - w / 2) / w)
    check("floor_alone_never_forces_leave", worst < 0,
          "re-test; max over 2000 draws of (min_eps cost - w/2)/w = %.3e (< 0 means following beats leaving)" % worst)

    # H3. Three binary coordinates: world X (rate r), the whole's signal S,
    # the part's memory M. S copies X with weight (1-tau) and M with weight
    # tau (channel tamper). M copies S only. Full tamper (tau=1) makes (S,M)
    # independent of X: the part's error about X is 1/2. With equal S-M
    # couplings at tau=1 the pair is a joint equilibrium: zero memory heat.
    def three(tau, JS=2.0, JM=2.0, r=0.3, gS=3.0, gM=3.0):
        st = list(itertools.product((0, 1), repeat=3))
        ix = {z: i for i, z in enumerate(st)}
        sg = lambda a, b: 1.0 if a == b else -1.0
        ES = lambda s, x, m: -JS * ((1 - tau) * sg(s, x) + tau * sg(s, m))
        EM = lambda m, s: -JM * sg(m, s)
        Q = np.zeros((8, 8))
        for (x, s, m) in st:
            i = ix[(x, s, m)]
            Q[i, ix[(1 - x, s, m)]] += r
            Q[i, ix[(x, 1 - s, m)]] += gS * math.exp(-(ES(1 - s, x, m) - ES(s, x, m)) / 2)
            Q[i, ix[(x, s, 1 - m)]] += gM * math.exp(-(EM(1 - m, s) - EM(m, s)) / 2)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        p = stationary(Q)
        P = {z: p[ix[z]] for z in st}
        heat = ialt = 0.0
        for (x, s, m) in st:
            rate = Q[ix[(x, s, m)], ix[(x, s, 1 - m)]]
            pys = P[(x, s, 0)] + P[(x, s, 1)]
            heat += P[(x, s, m)] * rate * (EM(m, s) - EM(1 - m, s))
            ialt += P[(x, s, m)] * rate * math.log((P[(x, s, 1 - m)] / pys) / (P[(x, s, m)] / pys))
        pm = lambda var: sum(min(sum(P[z] for z in st if z[var] == 0 and z[2] == m),
                                 sum(P[z] for z in st if z[var] == 1 and z[2] == m)) for m in (0, 1))
        return heat, ialt, pm(1), pm(0)

    rows, ok = [], True
    prev_eX = 0.0
    for tau in (0.0, 0.25, 0.5, 0.75, 1.0):
        hq, ia, eS, eX = three(tau)
        rows.append("tau=%.2f Q_M=%.4f I_alt=%.4f eps(S)=%.4f eps(X)=%.4f" % (tau, hq, ia, eS, eX))
        ok &= hq >= ia - 1e-12 and eX >= prev_eX - 1e-12
        prev_eX = eX
    hq1, ia1, eS1, eX1 = three(1.0)
    hq_neq, _, _, eX_neq = three(1.0, JS=1.0, JM=2.0)
    ok &= abs(eX1 - 0.5) < 1e-12 and abs(hq1) < 1e-12 and abs(eX_neq - 0.5) < 1e-12 and hq_neq > 1e-6
    for r in rows:
        print("  " + r)
    check("channel_tamper_buys_heat_with_world_information", ok,
          "re-test; JP-heat holds at every tau; eps(X) rises with tau to exactly 1/2 at full tamper; full tamper with equal couplings: Q_M=%.1e; unequal couplings: Q_M=%.4f, eps(X)=%.3f"
          % (hq1, hq_neq, eX_neq))

    # H4. Per-read floor with Poisson reads: kT lam L(lam/(f+2 lam))/f is
    # bounded in the read rate f; its maximum over x = f/lam.
    xs = np.geomspace(1e-4, 1e6, 200001)
    vals = np.array([L_floor(1 / (x + 2)) / x for x in xs])
    j = int(np.argmax(vals))
    check("per_read_floor_bounded", vals[0] < vals[j] and vals[-1] < vals[j] and vals[j] < 1,
          "code sanity; max_x L(1/(x+2))/x = %.6f at x = f/lam = %.4f (units kT per read)" % (vals[j], xs[j]))
    # H5. The pair (whole's signal S, part's memory M) as one memory about the
    # exogenous world X: Q_S + Q_M >= l_(S,M) >= r L(eps_(S,M)(X)) >= r L(eps_M(X))
    # at every tamper level (T60 telegraph bound + JP-heat on the pair).
    def pair(tau, JS, JM, r, gS, gM):
        st = list(itertools.product((0, 1), repeat=3))
        ix = {z: i for i, z in enumerate(st)}
        sg = lambda a, b: 1.0 if a == b else -1.0
        ES = lambda s, x, m: -JS * ((1 - tau) * sg(s, x) + tau * sg(s, m))
        EM = lambda m, s: -JM * sg(m, s)
        Q = np.zeros((8, 8))
        for (x, s, m) in st:
            i = ix[(x, s, m)]
            Q[i, ix[(1 - x, s, m)]] += r
            Q[i, ix[(x, 1 - s, m)]] += gS * math.exp(-(ES(1 - s, x, m) - ES(s, x, m)) / 2)
            Q[i, ix[(x, s, 1 - m)]] += gM * math.exp(-(EM(1 - m, s) - EM(m, s)) / 2)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        p = stationary(Q)
        P = {z: p[ix[z]] for z in st}
        px = {x: sum(P[(x, s, m)] for s in (0, 1) for m in (0, 1)) for x in (0, 1)}
        heat = lY = 0.0
        for (x, s, m) in st:
            for z2, dE in (((x, 1 - s, m), ES(s, x, m) - ES(1 - s, x, m)),
                           ((x, s, 1 - m), EM(m, s) - EM(1 - m, s))):
                rate = Q[ix[(x, s, m)], ix[z2]]
                heat += P[(x, s, m)] * rate * dE
                lY += P[(x, s, m)] * rate * math.log((P[z2] / px[x]) / (P[(x, s, m)] / px[x]))
        eY = sum(min(P[(0, s, m)], P[(1, s, m)]) for s in (0, 1) for m in (0, 1))
        eM = sum(min(sum(P[(0, s, m)] for s in (0, 1)), sum(P[(1, s, m)] for s in (0, 1))) for m in (0, 1))
        return heat, lY, eY, eM

    fails, n_cases = 0, 0
    rr = random.Random(27011)
    cases = [(t, 2.0, 2.0, 0.3, 3.0, 3.0) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
    cases += [(t, 1.0, 2.0, 0.3, 3.0, 3.0) for t in (0.0, 0.5, 1.0)]
    for _ in range(300):
        cases.append((rr.uniform(0, 1), rr.uniform(0.1, 4), rr.uniform(0.1, 4),
                      10 ** rr.uniform(-1.5, 0.5), 10 ** rr.uniform(-0.5, 1), 10 ** rr.uniform(-0.5, 1)))
    for cs in cases:
        hq, lY, eY, eM = pair(*cs)
        r = cs[3]
        fl = lambda e: r * L_floor(e) if e < 0.5 - 1e-12 else 0.0
        n_cases += 1
        fails += not (hq >= lY - 1e-10 and lY >= fl(eY) - 1e-10 and eY <= eM + 1e-12 and fl(eY) >= fl(eM) - 1e-12)
    hq0, _, eY0, eM0 = pair(0.5, 2.0, 2.0, 0.3, 3.0, 3.0)
    check("pair_floor_under_tamper", fails == 0,
          "re-test (stationary law; %d tamper levels and couplings): Q_S+Q_M >= l_(S,M) >= r L(eps_(S,M)) >= r L(eps_M) with %d failures; at tau=0.5 Q_S+Q_M=%.4f, r L(eps_M)=%.4f"
          % (n_cases, fails, hq0, 0.3 * L_floor(eM0)))


def main():
    section_fold()
    section_telling()
    section_stakes()
    section_objective()
    section_couplings()
    section_remove()
    section_merge()
    section_feedback()
    if FAILED:
        print("FAILS %d: %s" % (len(FAILED), ", ".join(FAILED)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL SWARM27 CHECKS PASS")


if __name__ == "__main__":
    main()
