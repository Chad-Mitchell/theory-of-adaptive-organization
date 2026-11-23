#!/usr/bin/env python3
"""Checks for theory/ANTIFRAGILE_LOOP_2026-11-23.md (T50, closed loop with payoff).

Run from the repo root:
  nice -n 19 python3 theory/antifragile_loop_checks/antifragile_loop_checks.py
  nice -n 19 python3 theory/antifragile_loop_checks/antifragile_loop_checks.py --crossref

The memory reads an exogenous world X = mu + sigma*Z, acts, and is paid
u(action, X). Cost J = memory heat - w E[u], under a ruin cap. Every check is
a closed form, a Gauss-Hermite quadrature, an exact Gaussian steady state
(Lyapunov equation), a linear program, or a seeded Monte Carlo cross-check.
None is a measurement of a real system. A failure sets a nonzero exit code.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

import numpy as np
from numpy.polynomial.hermite_e import hermegauss
from scipy import linalg, optimize, special

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
HYP = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
NOTE = os.path.join(ROOT, "theory", "ANTIFRAGILE_LOOP_2026-11-23.md")

checks_failed = []
n_checks = [0]

XS, WS = hermegauss(160)
WS = WS / WS.sum()
PHI = special.ndtr


def phi(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def check(name, ok, detail):
    n_checks[0] += 1
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def fmt(x):
    return "%.6g" % x


# ---------------------------------------------------------------- S1
def ou_spring(a, D, gamma, s2):
    """Exact steady state of world dX=-aX dt+sqrt(2D)dW, spring memory
    dM=-gamma(M-X)dt+sqrt(2 gamma s2)dW_M at kT=1. Returns (heat, learning rate, Bayes MSE)."""
    A = np.array([[-a, 0.0], [gamma, -gamma]])
    Q = np.diag([2.0 * D, 2.0 * gamma * s2])
    C = linalg.solve_continuous_lyapunov(A, -Q)
    cxx, cxm, cmm = C[0, 0], C[0, 1], C[1, 1]
    eyf = -a * (cxm - cxx)  # E[(M-X) f(X)], f=-aX
    heat = (D - eyf) / s2
    alpha = cxm / cxx
    sc2 = cmm - cxm ** 2 / cxx
    learn = D * alpha ** 2 / sc2
    mmse = cxx - cxm ** 2 / cmm
    return heat, learn, mmse


def section_scale():
    print("S1 amplitude invariance of the cost of knowing (Theorem AF-scale)")
    a = 1.0
    for gamma in (2.0, 20.0, 2000.0):
        for s0 in (0.3, 1.0):
            vals = []
            for sig in (0.5, 1.0, 3.0, 10.0):
                D = a * sig ** 2
                h, L, e = ou_spring(a, D, gamma, (s0 * sig) ** 2)
                vals.append((h, L, e / sig ** 2))
            v = np.array(vals)
            spread = np.max(np.abs(v - v[0]), axis=0) / np.abs(v[0])
            check("S1 heat, learning rate, error fraction invariant gamma=%g s0=%g" % (gamma, s0),
                  bool(np.all(spread < 1e-9)), "max rel spread %s" % fmt(spread.max()))
            check("S1 heat >= kT x learning rate gamma=%g s0=%g" % (gamma, s0),
                  bool(np.all(v[:, 0] >= v[:, 1] * (1 - 1e-12))), "Q=%s I=%s" % (fmt(v[0, 0]), fmt(v[0, 1])))
    # fast limit: heat -> kappa(1/r-1), the OU floor a(theta/eps-1) at the Bayes error
    for sig in (1.0, 4.0):
        D = a * sig ** 2
        h, L, e = ou_spring(a, D, 1e7, (0.5 * sig) ** 2)
        floor = a * (sig ** 2 / e - 1.0)
        check("S1 fast spring attains floor a(theta/eps-1) sigma=%g" % sig, abs(h / floor - 1) < 1e-5,
              "heat %s floor %s" % (fmt(h), fmt(floor)))


# ---------------------------------------------------------------- S2
def V_bet(theta, kap=1.0, beta=0.5):
    return max(0.0, math.sqrt(beta * theta) - math.sqrt(kap)) ** 2


def section_option():
    print("S2 closed loop with a payoff convex in the world (Theorem AF-convex)")
    kap, beta = 1.0, 0.5
    # (a) closed form of the bet class against direct maximization of the floor-cost
    errs = []
    for th in (0.5, 2.0, 2.5, 5.0, 20.0, 100.0):
        f = lambda e: -(beta * (th - e) - kap * (th / e - 1.0))
        res = optimize.minimize_scalar(f, bounds=(1e-9, th), method="bounded", options={"xatol": 1e-12})
        num = max(0.0, -res.fun)
        errs.append(abs(num - V_bet(th)))
    check("S2a bet class V*=(sqrt(beta theta)-sqrt(kappa))_+^2 matches direct maximization",
          max(errs) < 1e-7, "max abs err %s" % fmt(max(errs)))
    th = np.linspace(0.1, 50, 2000)
    V = np.array([V_bet(t) for t in th])
    d2 = np.diff(V, 2)
    check("S2a bet class V* convex in theta", bool(np.all(d2 >= -1e-12)), "min 2nd diff %s" % fmt(d2.min()))
    check("S2a bet class V* nondecreasing in theta", bool(np.all(np.diff(V) >= -1e-12)), "")
    thc = kap / beta
    check("S2a learning threshold theta_c=kappa/beta (=2kTa c/w)", V_bet(thc * 0.999) == 0.0 and V_bet(thc * 1.01) > 0,
          "theta_c %s; r* at theta=8: %s" % (fmt(thc), fmt(math.sqrt(kap / (beta * 8.0)))))
    # joining identity: V* = beta theta - J*_track(theta), with J*_track = 2 sqrt(kappa beta theta) - kappa (concave)
    t = 8.0
    jt = 2 * math.sqrt(kap * beta * t) - kap
    check("S2a V* = full-information payoff - minimized tracking cost (T49 A4/A5 form)",
          abs(V_bet(t) - (beta * t - jt)) < 1e-12, "theta=8: %s = %s - %s" % (fmt(V_bet(t)), fmt(beta * t), fmt(jt)))
    # (b) act-or-abstain (degree 1): convex in sigma, concave in theta at high volatility
    def V_call(sig, w=1.0):
        f = lambda x: -(w * sig * math.sqrt(1 - math.exp(x)) / math.sqrt(2 * math.pi) - kap * (math.exp(-x) - 1))
        res = optimize.minimize_scalar(f, bounds=(-30, 0), method="bounded", options={"xatol": 1e-12})
        return max(0.0, -res.fun)
    sig = np.linspace(1.0, 60.0, 400)
    Vc = np.array([V_call(s) for s in sig])
    d2s = np.diff(Vc, 2)
    check("S2b act-or-abstain V* convex in sigma (Gaussian spring family)", bool(np.all(d2s >= -1e-9)),
          "min 2nd diff %s" % fmt(d2s.min()))
    thg = np.linspace(400.0, 3600.0, 200)
    Vt = np.array([V_call(math.sqrt(x)) for x in thg])
    d2t = np.diff(Vt, 2)
    check("S2b act-or-abstain V* concave in theta at high volatility", bool(np.all(d2t < 0)),
          "max 2nd diff %s on theta in [400,3600]" % fmt(d2t.max()))
    # (c) random convex menus u(a,x)=al x+be+ga (x-K)_+, ga>=0; Gaussian channel family
    rng = np.random.default_rng(50)
    worst = 0.0
    worst_mono = 0.0
    span = 0.0
    for inst in range(12):
        nA = 4
        al = rng.normal(0, 1, nA); be = rng.normal(0, 0.5, nA); ga = rng.uniform(0, 1, nA); K = rng.normal(0, 1, nA)
        mu = rng.normal(0, 0.5)
        rs = np.exp(np.linspace(math.log(1e-3), 0, 60))
        sigs = np.linspace(0.2, 4.0, 40)
        Vs = []
        for s in sigs:
            best = -np.inf
            for r in rs:
                m = mu + s * math.sqrt(1 - r) * XS
                sp = s * math.sqrt(r)
                if sp > 0:
                    d = (m[:, None] - K[None, :]) / sp
                    callv = sp * phi(d) + (m[:, None] - K[None, :]) * PHI(d)
                else:
                    callv = np.maximum(m[:, None] - K[None, :], 0)
                pay = al[None, :] * m[:, None] + be[None, :] + ga[None, :] * callv
                gross = WS @ pay.max(axis=1)
                val = gross - kap * (1 / r - 1)
                best = max(best, val)
            Vs.append(best)
        Vs = np.array(Vs)
        worst = min(worst, np.diff(Vs, 2).min())
        span = max(span, float(Vs[-1] - Vs[0]))
        worst_mono = min(worst_mono, np.diff(Vs).min())
    check("S2c 12 random convex menus: V* convex in sigma", worst >= -1e-9, "min 2nd diff %s; max V* range %s" % (fmt(worst), fmt(span)))
    check("S2c 12 random convex menus: V* nondecreasing in sigma", worst_mono >= -1e-9, "min diff %s" % fmt(worst_mono))
    # (d) Jensen with per-regime redesign
    vbar = V_bet(4.0)
    vmix = 0.5 * (V_bet(1.0) + V_bet(9.0))
    check("S2d two regimes sigma in {1,3}: E V*(sigma) > V*(E sigma)", vmix > vbar,
          "E V* %s against V*(2) %s; calm regime abstains (V*(1)=%s)" % (fmt(vmix), fmt(vbar), fmt(V_bet(1.0))))


# ---------------------------------------------------------------- S3
def section_homeostatic():
    print("S3 pay-to-stay-correct losses (Theorem AF-homeostatic)")
    kap, w = 1.0, 1.0
    th = np.linspace(1.5, 60, 500)
    J = 2 * np.sqrt(kap * w * th) - kap
    # direct minimization
    errs = []
    for t in (2.0, 10.0, 50.0):
        f = lambda e: kap * (t / e - 1) + w * e
        res = optimize.minimize_scalar(f, bounds=(1e-9, t), method="bounded", options={"xatol": 1e-12})
        errs.append(abs(res.fun - (2 * math.sqrt(kap * w * t) - kap)))
    check("S3 squared error: J*=2 sqrt(kappa w theta)-kappa (w theta>=kappa)", max(errs) < 1e-7, "err %s" % fmt(max(errs)))
    check("S3 squared error: J* concave and increasing in theta (level loses, spread gains with redesign)",
          bool(np.all(np.diff(J, 2) <= 1e-12) and np.all(np.diff(J) > 0)), "")
    sig = np.linspace(0.2, 10, 300)
    Ja = []
    for s in sig:
        f = lambda x: kap * (math.exp(-x) - 1) + w * s * math.sqrt(2 * math.exp(x) / math.pi)
        res = optimize.minimize_scalar(f, bounds=(-30, 0), method="bounded", options={"xatol": 1e-12})
        Ja.append(min(res.fun, w * s * math.sqrt(2 / math.pi)))
    Ja = np.array(Ja)
    check("S3 absolute error (degree 1): J* concave and increasing in sigma", bool(np.all(np.diff(Ja, 2) <= 1e-9) and np.all(np.diff(Ja) > 0)),
          "max 2nd diff %s" % fmt(np.diff(Ja, 2).max()))


# ---------------------------------------------------------------- S4
def section_rate():
    print("S4 rate of change at fixed amplitude (Theorem AF-rate)")
    beta, k = 0.5, 1.0
    f = lambda s, a: max(0.0, s * math.sqrt(beta) - math.sqrt(k * a)) ** 2
    a = np.linspace(0.05, 8, 400)
    V = np.array([f(3.0, x) for x in a])
    check("S4 bet class V*(a) convex and nonincreasing in the world's rate a",
          bool(np.all(np.diff(V, 2) >= -1e-12) and np.all(np.diff(V) <= 1e-12)), "")
    # joint convexity: Hessian determinant in the learning region
    dets = []
    for s in np.linspace(1.0, 6.0, 11):
        for x in np.linspace(0.05, 4.0, 11):
            if s * math.sqrt(beta) <= math.sqrt(k * x) * 1.001:
                continue
            fss = 2 * beta
            fsa = -math.sqrt(beta * k / x)
            faa = s * math.sqrt(beta * k) / (2 * x ** 1.5)
            dets.append(fss * faa - fsa ** 2)
            # finite-difference cross-check of faa
            h = 1e-4
            fd = (f(s, x + h) - 2 * f(s, x) + f(s, x - h)) / h ** 2
            if abs(fd - faa) > 1e-3 * max(1.0, abs(faa)):
                dets.append(-1.0)
    check("S4 V*(sigma,a) jointly convex where the memory learns", min(dets) >= -1e-12, "min det %s over %d points" % (fmt(min(dets)), len(dets)))
    # per-decorrelation harvest: payoff w*a*F_D against heat a*Q_D gives V*(a) = a V*(1)
    g = lambda s, x: x * f(s, 1.0)
    lin = [g(3.0, x) for x in (0.5, 1.0, 1.5)]
    check("S4 harvest per decorrelation time: V*(a)=a V*(1), linear in a (neutral in curvature)",
          abs(lin[0] + lin[2] - 2 * lin[1]) < 1e-12 and lin[1] > 0, "V*(1)=%s" % fmt(lin[1]))


# ---------------------------------------------------------------- S5
def ruin_bet(sig, r, lam, B):
    th = sig ** 2
    m = math.sqrt(th * (1 - r)) * XS
    mu = (lam - lam ** 2 / 2) * m ** 2
    s = np.maximum(lam * np.abs(m) * math.sqrt(th * r), 1e-300)
    return float(WS @ PHI((-B - mu) / s))


def lam_max(sig, r, B, eta):
    if ruin_bet(sig, r, 1.0, B) <= eta:
        return 1.0
    g = lambda l: ruin_bet(sig, r, l, B) - eta
    if g(1e-9) > 0:
        return 0.0
    return optimize.brentq(g, 1e-9, 1.0, xtol=1e-14)


def V_capped(sig, B, eta, kap=1.0, beta=0.5):
    val = lambda r, l: 2 * beta * (l - l * l / 2) * sig ** 2 * (1 - r) - kap * (1 / r - 1)
    lr = np.linspace(math.log(1e-5), 0, 241)
    vals = []
    for x in lr:
        r = math.exp(x)
        l = lam_max(sig, r, B, eta)
        vals.append(val(r, l) if l > 0 else -np.inf)
    vals = np.array(vals)
    i = int(np.argmax(vals))
    lo, hi = lr[max(i - 1, 0)], lr[min(i + 1, len(lr) - 1)]
    g = lambda x: -val(math.exp(x), lam_max(sig, math.exp(x), B, eta))
    res = optimize.minimize_scalar(g, bounds=(lo, hi), method="bounded", options={"xatol": 1e-10})
    best = max(-res.fun, vals[i], 0.0)
    return best


def section_ruin():
    print("S5 ruin cap in the bet class (Propositions AF-ruin)")
    # (a) sign-error law P(mX<0)=arcsin(sqrt r)/pi and P(U<0)=arctan(1/k)/pi
    rng = np.random.default_rng(7)
    worst = 0.0
    for r in (0.01, 0.1, 0.5):
        for lam in (0.0, 0.5, 1.0):
            n = 400000
            m = math.sqrt(1 - r) * rng.standard_normal(n)
            e = math.sqrt(r) * rng.standard_normal(n)
            X = m + e
            if lam == 0.0:
                p_mc = np.mean(m * X < 0)
                p_th = math.asin(math.sqrt(r)) / math.pi
            else:
                p_mc = np.mean(lam * m * X - lam ** 2 * m ** 2 / 2 < 0)
                k = (1 - lam / 2) * math.sqrt((1 - r) / r)
                p_th = math.atan(1 / k) / math.pi
            worst = max(worst, abs(p_mc - p_th))
    check("S5a sign-error laws arcsin(sqrt r)/pi and arctan(1/k)/pi (Monte Carlo, seeded)", worst < 3e-3, "max abs dev %s" % fmt(worst))
    # (b) precision threshold r_eta = sin^2(pi eta) and its heat kappa cot^2(pi eta)
    for eta in (0.05, 0.01):
        re = math.sin(math.pi * eta) ** 2
        check("S5b precision threshold eta=%g: r_eta=sin^2(pi eta), heat kappa cot^2(pi eta)" % eta,
              abs(math.asin(math.sqrt(re)) / math.pi - eta) < 1e-12 and abs((1 / re - 1) - 1 / math.tan(math.pi * eta) ** 2) < 1e-6,
              "r_eta %s heat %s" % (fmt(re), fmt(1 / re - 1)))
    # bounded gross for coarse designs: lam sigma^2 <= B/q_r
    sig_list = (4.0, 8.0, 16.0)
    r, B, eta = 0.5, 1.0, 0.01
    W = (math.sqrt(1 - r) * XS)[:, None] * 1.0
    # q_r: P(m X < -q) = eta for unit world (quadrature over m, conditional normal over e)
    def pW(q):
        m = math.sqrt(1 - r) * XS
        mu = m * m
        s = np.maximum(np.abs(m) * math.sqrt(r), 1e-300)
        return float(WS @ PHI((-q - mu) / s))
    q = optimize.brentq(lambda z: pW(z) - eta, 1e-9, 50)
    gross = []
    for s in sig_list:
        l = lam_max(s, r, B, eta)
        gross.append(2 * 0.5 * (l - l * l / 2) * s ** 2 * (1 - r))
    check("S5b coarse design r=0.5: gross payoff bounded by B(1-r)/q_r as sigma grows",
          max(gross) <= B * (1 - r) / q * (1 + 1e-9), "gross %s, bound %s" % (", ".join(fmt(g) for g in gross), fmt(B * (1 - r) / q)))
    # (c) slack bound sigma_hi
    kap, beta = 1.0, 0.5
    for eta in (0.05,):
        sh = math.sqrt(kap / beta) * (1 + 4 / math.tan(math.pi * eta) ** 2)
        rs = math.sqrt(kap / (beta * sh ** 2))
        pr = ruin_bet(sh, rs, 1.0, 1.0)
        check("S5c above sigma_hi the slack optimum meets the cap (eta=%g)" % eta, pr <= eta,
              "sigma_hi %s, ruin at slack optimum %s" % (fmt(sh), fmt(pr)))
    # (d) value under the cap: nondecreasing; concave window; slack region
    for B, eta, lab in ((1.0, 0.01, "B=1 eta=0.01"), (4.0, 0.01, "B=4 eta=0.01")):
        sigs = np.arange(1.6, 12.01, 0.4)
        V = np.array([V_capped(s, B, eta) for s in sigs])
        S = np.array([V_bet(s * s) for s in sigs])
        mono = bool(np.all(np.diff(V) >= -1e-9))
        check("S5d %s: capped V* nondecreasing in sigma" % lab, mono, "V(1.6)=%s V(12)=%s" % (fmt(V[0]), fmt(V[-1])))
        d2 = np.diff(V, 2)
        neg = sigs[1:-1][d2 < -1e-7]
        if lab.startswith("B=1"):
            check("S5d %s: concave window under the binding cap" % lab, len(neg) >= 10,
                  "2nd diff < 0 at sigma in [%s, %s]; V(7.6)=%s against slack %s" % (fmt(neg.min()), fmt(neg.max()), fmt(V[sigs.searchsorted(7.6 - 1e-9)]), fmt(S[sigs.searchsorted(7.6 - 1e-9)])))
            v2, v3, v4 = (V_capped(x, B, eta) for x in (2.0, 3.0, 4.0))
            check("S5d %s: in the window a spread of sigma lowers the value (sigma in {2,4} against 3)" % lab,
                  0.5 * (v2 + v4) < v3, "mean %s against %s" % (fmt(0.5 * (v2 + v4)), fmt(v3)))
            jump = d2.max()
            check("S5d %s: switch to the precise branch is a convex kink" % lab, jump > 1e-2, "max 2nd diff %s" % fmt(jump))
        else:
            check("S5d %s: cap binds yet V* stays convex on the grid" % lab, len(neg) == 0 and np.any(V < S - 1e-6),
                  "min 2nd diff %s" % fmt(d2.min()))
    # (e) bounded downside (stop-loss) keeps convexity: u(b,x)=max(bx-b^2/2,-Bs)
    Bs = 0.3
    bgrid = np.linspace(0.0, 40.0, 1601)  # fixed action set, not scaled with sigma
    def gross_stop(sig, r):
        p = sig * sig * r
        sp = math.sqrt(p)
        m = np.abs(math.sqrt(sig * sig * (1 - r)) * XS)
        b = bgrid[None, :]
        with np.errstate(divide="ignore", invalid="ignore"):
            Kp = np.where(b > 0, (b * b / 2 - Bs) / np.where(b > 0, b, 1), 0.0)
        d = (Kp - m[:, None]) / sp
        put = (Kp - m[:, None]) * PHI(d) + sp * phi(d)
        val = b * m[:, None] - b * b / 2 + b * put
        val = np.where(b > 0, val, 0.0)
        return float(WS @ val.max(axis=1))
    sigs = np.linspace(0.5, 4.0, 36)
    rs = np.exp(np.linspace(math.log(1e-3), 0, 50))
    Vst = []
    for s in sigs:
        Vst.append(max(gross_stop(s, r) - (1 / r - 1) for r in rs))
    Vst = np.array(Vst)
    check("S5e stop-loss payoff (downside <= B): cap never binds, V* convex and nondecreasing in sigma",
          bool(np.all(np.diff(Vst, 2) >= -1e-9) and np.all(np.diff(Vst) >= -1e-9)), "V*(0.5)=%s V*(4)=%s, min 2nd diff %s" % (fmt(Vst[0]), fmt(Vst[-1]), fmt(np.diff(Vst, 2).min())))


# ---------------------------------------------------------------- S6
def prior_call(K, s):
    k = K / s
    return s * phi(k) - K * PHI(-k)


def post_call(K, m, p):
    sp = math.sqrt(p)
    d = (m - K) / sp
    return sp * phi(d) + (m - K) * PHI(d)


KS = np.linspace(-4, 8, 1201)


def VB(m, sig, p, B):
    m = abs(m)
    R = post_call(KS * sig, m, p) / prior_call(KS * sig, sig)
    return B * max(0.0, R.max() - 1)


def VL(m, p, B, eta):
    m = abs(m)
    if eta <= 0:
        return 0.0
    z = -special.ndtri(eta)
    g = z * math.sqrt(p) - m
    n = 1.0 if g <= 0 else min(1.0, B / g)
    return n * m


def section_barbell():
    print("S6 barbell (Propositions AF-barbell)")
    # (a) LP: reserve plus at most one claim
    rng = np.random.default_rng(11)
    ok = True
    for inst in range(200):
        n = 8
        price = rng.uniform(0.1, 1.0, n)
        ev = price * rng.uniform(0.5, 2.0, n)
        res = optimize.linprog(-(ev - price), A_ub=[price], b_ub=[0.2], bounds=[(0, None)] * n, method="highs")
        nz = int(np.sum(res.x > 1e-12))
        if nz > 1:
            ok = False
    check("S6a hard cap, linear stake: optimum is reserve plus at most one claim (200 random LPs)", ok, "")
    # (b) fair prior pricing: barbell value amplitude-neutral
    B = 0.2
    vals = []
    for sig in (0.5, 1.0, 2.0, 5.0):
        r = 0.2
        p = sig * sig * r
        ms = math.sqrt(sig * sig * (1 - r)) * XS
        vals.append(WS @ np.array([VB(m, sig, p, B) for m in ms]))
    vals = np.array(vals)
    check("S6b claims priced at the prior: barbell value independent of sigma", float(np.ptp(vals)) < 1e-9 * vals[0],
          "E V_B %s at sigma 0.5..5" % fmt(vals[0]))
    # (c) eta>0: share of memory states where a capped linear position beats the best barbell
    lines = []
    shares = {}
    for r in (0.5, 0.2, 0.05):
        for eta in (0.0, 1e-4, 1e-3, 1e-2, 5e-2):
            sig = 1.0
            p = sig * sig * r
            ms = math.sqrt(sig * sig * (1 - r)) * XS
            vb = np.array([VB(m, sig, p, B) for m in ms])
            vl = np.array([VL(m, p, B, eta) for m in ms])
            sh = float(WS @ (vl > vb + 1e-12))
            shares[(r, eta)] = sh
            edge = np.abs(XS[vl <= vb + 1e-12]).min() if np.any(vl <= vb + 1e-12) else float("nan")
            lines.append("r=%g eta=%g share=%s  E V_B=%s E V_L=%s E max=%s ratio=%.3f  barbell keeps |m|/sd >= %s"
                         % (r, eta, fmt(sh), fmt(WS @ vb), fmt(WS @ vl), fmt(WS @ np.maximum(vb, vl)), (WS @ np.maximum(vb, vl)) / (WS @ vb), fmt(edge)))
    for ln in lines:
        print("  " + ln)
    check("S6c eta=0: no linear exposure admissible (share 0 for every r)", all(shares[(r, 0.0)] == 0 for r in (0.5, 0.2, 0.05)), "")
    check("S6c eta=0.01: capped linear beats the best barbell in >25% of memory states for every r",
          all(shares[(r, 1e-2)] > 0.25 for r in (0.5, 0.2, 0.05)), "shares %s" % ", ".join(fmt(shares[(r, 1e-2)]) for r in (0.5, 0.2, 0.05)))


# ---------------------------------------------------------------- S7
BANNED = ["solved", "solves", " bill", "theory of everything", "kill", "verdict", "refute", "falsif", "debunk"]


def section_text():
    print("S7 text")
    with open(os.path.join(ROOT, "THEORY.md"), encoding="utf-8") as fh:
        th = fh.read()
    check("S7 hypothesis sentence byte-identical in THEORY.md", HYP in th, "")
    if os.path.exists(NOTE):
        with open(NOTE, encoding="utf-8") as fh:
            nt = fh.read()
        check("S7 hypothesis sentence byte-identical in the note", HYP in nt, "")
        low = nt.lower()
        hits = [b for b in BANNED if b in low]
        check("S7 note wording (no banned words)", not hits, ",".join(hits))
        stripped = low.replace(HYP.lower(), "")
        bad_law = [i for i in range(len(stripped)) if stripped.startswith("law", i)
                   and (i == 0 or not stripped[i - 1].isalpha()) and not stripped[i + 3:i + 4].isalpha()]
        check("S7 'law' appears only in the hypothesis sentence", not bad_law, "%d other uses" % len(bad_law))
    else:
        check("S7 note present", False, NOTE)


# ---------------------------------------------------------------- crossref
DOIS = [
    ("10.1016/0022-0531(70)90038-4", "Increasing risk"),
    ("10.1016/S0304-3932(03)00029-1", "rational inattention"),
    ("10.1098/rsta.1899.0003", "normal correlation"),
    ("10.1080/14697688.2013.800219", "fragility"),
    ("10.3390/e17063724", "Tail Risk Constraints"),
    ("10.1016/0022-5193(66)90188-3", "Optimizing reproduction"),
    ("10.1016/0169-5347(89)90138-9", "Hedging one"),
    ("10.1002/j.1538-7305.1956.tb03809.x", "Information Rate"),
    ("10.1287/mnsc.38.11.1562", "Growth Versus Security"),
    ("10.2307/1907687", "Price Instability"),
    ("10.1016/0022-0531(72)90105-6", "price and cost uncertainty"),
    ("10.1016/0165-1889(84)90047-2", "uncertainty on investment"),
    ("10.2307/1884175", "Value of Waiting"),
    ("10.1515/9781400830176", "Investment under Uncertainty"),
    ("10.1086/260062", "Pricing of Options"),
    ("10.2307/3003143", "Rational Option Pricing"),
    ("10.1088/0305-4470/14/11/006", "stochastic resonance"),
    ("10.1103/RevModPhys.70.223", "Stochastic resonance"),
    ("10.1126/science.1114383", "Phenotypic Diversity"),
    ("10.1007/s10955-011-0166-2", "Value of Information"),
    ("10.1111/j.1600-0706.2009.17781.x", "fitness value of information"),
    ("10.1103/PhysRevLett.115.238102", "Fluctuation Relations"),
    ("10.1103/PhysRevE.96.012402", "information-thermodynamic"),
    ("10.1088/1742-5468/2016/04/043403", "gambling"),
    ("10.1103/PhysRevX.4.031015", "Continuous Information Flow"),
    ("10.1103/PhysRevLett.109.120604", "Thermodynamics of Prediction"),
    ("10.1063/1.4940236", "Evaluating gambles"),
    ("10.1214/aoms/1177729032", "Equivalent Comparisons"),
]


def crossref():
    print("crossref")
    lines = ["Crossref API resolutions, 23 November 2026, America/New_York.",
             "Queried https://api.crossref.org/works/{doi}. OK means HTTP 200 and the expected title words.", ""]
    ua = {"User-Agent": "gtao-t50 (mailto:chad39@gmail.com)"}
    for doi, needle in DOIS:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        ok, title, err = False, "", ""
        for attempt in range(5):
            try:
                req = urllib.request.Request(url, headers=ua)
                with urllib.request.urlopen(req, timeout=40) as resp:
                    msg = json.load(resp)["message"]
                title = (msg.get("title") or [""])[0]
                authors = "; ".join(x.get("family", "") for x in msg.get("author", [])[:4])
                year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
                cont = (msg.get("container-title") or [""])[0]
                ok = needle.lower() in title.lower()
                lines.append("%s\t%s\t%s\t%s\t%s\t%s" % ("OK" if ok else "MISMATCH", doi, year, authors, title, cont))
                err = ""
                break
            except Exception as exc:  # network
                err = str(exc)
                time.sleep(2.0 * (attempt + 1))
        if err and not title:
            lines.append("FAIL\t%s\t%s" % (doi, err))
        check("Crossref %s" % doi, ok, (title or err)[:80])
        time.sleep(0.5)
    with open(os.path.join(HERE, "crossref.out"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv):
    section_scale()
    section_option()
    section_homeostatic()
    section_rate()
    section_ruin()
    section_barbell()
    section_text()
    if "--crossref" in argv:
        crossref()
    print("CHECKS %d" % n_checks[0])
    print("FAILS %d" % len(checks_failed))
    if checks_failed:
        for n in checks_failed:
            print("FAILED " + n)
        return 1
    print("ALL ANTIFRAGILE-LOOP CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
