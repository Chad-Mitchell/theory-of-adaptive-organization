#!/usr/bin/env python3
"""Numerical checks for theory/LAYER_CONVEXITY.md (W9 / N60 convexity premise).

These checks are NUMERICAL companions to the proofs in the note. They do not
re-run S5, do not touch locked prereg or hash files, and do not change any
Model S result. Sections:

  L1  from-0 count K*_0(R) = leftmost argmin J for all R >= 0 if decrements
      are non-increasing; converse holds under positive, distinct decrements.
  L2  halving / log-convexity are sufficient for convexity (random sequences).
  T3  Ky Fan class: top-K eigenvalue sums are concave in K (random PSD).
  T4  Monge class: exact K-link DP on random Monge (convex-of-gap) costs is
      convex in K; a non-Monge cost can break it.
  T5  Band model B: exact DP over grid breakpoints for monotone spectra
      (OU sums J=1..6, power laws, colored noise with monotone SNR) is convex
      in K = 0..Kmax; the SSE quadrangle and the mixed (terminal zero band)
      inequality hold on random quadruples.
  P6  Failure class: the minimal bump (W = 0,1,0 with weights 2,1,1) is
      non-convex; rhythmic spectra (resonance peak) give non-convex band
      curves; a submodular set value need not give concave best-K value.
  S5  Model S evidence (read-only, from core/keystone_checks/s5_rerun.json):
      halving eps_{K+1} <= eps_K / 2 (screened at eps_K > 1e-4) on every world; max ratios.

Run from the repo root:

    nice -n 19 python3 tools/layer_convexity_checks.py [--quick]

Exit 0 and the line ALL LAYER CONVEXITY CHECKS PASS means every check held.
Writes theory/layer_convexity_checks/layer_convexity_checks.json (full run).
"""
from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "theory", "layer_convexity_checks", "layer_convexity_checks.json")
S5 = os.path.join(ROOT, "core", "keystone_checks", "s5_rerun.json")


def check(ok, detail, name, cond, msg=""):
    ok.append((name, bool(cond)))
    detail.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


# ---------------------------------------------------------------------------
# Sequence helpers
# ---------------------------------------------------------------------------
def decrements(eps):
    e = np.asarray(eps, float)
    return e[:-1] - e[1:]


def is_convex(eps, tol=0.0):
    d = decrements(eps)
    return bool(np.all(d[1:] <= d[:-1] + tol))


def n60_from(eps, R, k0=0):
    """N60 count started at k0: k0 + #{k : R (eps_{k-1}-eps_k) > 1}."""
    d = decrements(eps)
    return k0 + int(np.sum(R * d > 1))


def argmin_J(eps, R, k0=0):
    J = np.array([k0 + k + R * (1.0 + e) for k, e in enumerate(eps)])
    return k0 + int(np.argmin(J))  # leftmost minimizer


# ---------------------------------------------------------------------------
# Band model B: exact DP on a discrete measure (cells ordered low -> high freq)
# E(H) = sum mu_i W_i (1-W_i) + sum mu_i (W_i - H_i)^2, H a K-step staircase
# with free levels on [0, x) and forced level 0 on [x, M).
# ---------------------------------------------------------------------------
def seg_cost_matrix(mu, W):
    """C[i, j] = weighted SSE of W over cells i..j-1 (i < j), inf otherwise."""
    mu = np.asarray(mu, float); W = np.asarray(W, float)
    M = len(mu)
    C = np.full((M + 1, M + 1), np.inf)
    for i in range(M):
        m = mu[i:]; w = W[i:]
        s0 = np.cumsum(m); s1 = np.cumsum(m * w)
        # stable running SSE via Welford-like update
        mean = np.empty_like(s0); sse = np.empty_like(s0)
        mean[0] = w[0]; sse[0] = 0.0
        for t in range(1, len(m)):
            d = w[t] - mean[t - 1]
            mean[t] = mean[t - 1] + m[t] * d / s0[t]
            sse[t] = sse[t - 1] + m[t] * d * (w[t] - mean[t])
        C[i, i + 1:] = np.maximum(sse, 0.0)
    return C


def band_curve(mu, W, Kmax, C=None):
    """Exact E^B_K - E^B_inf (the staircase part) for K = 0..Kmax, at most K free bands."""
    mu = np.asarray(mu, float); W = np.asarray(W, float)
    M = len(mu)
    if C is None:
        C = seg_cost_matrix(mu, W)
    Z = np.r_[np.cumsum((mu * W * W)[::-1])[::-1], 0.0]  # Z[x] = sum_{i>=x} mu W^2
    F = np.full(M + 1, np.inf); F[0] = 0.0               # exactly k free bands covering [0, j)
    best = np.full(M + 1, np.inf); best[0] = 0.0          # at most k bands
    out = [float(np.min(best + Z))]
    for _k in range(1, Kmax + 1):
        F = np.min(F[:, None] + C, axis=0)
        F[0] = np.inf
        best = np.minimum(best, F)
        out.append(float(np.min(best + Z)))
    return np.array(out)


def spectrum_grid(Sfun, Nfun, lo, hi, M):
    """Log-spaced cells on (lo, hi); mu = (S+N) dw / pi; W = S/(S+N)."""
    edges = np.logspace(np.log10(lo), np.log10(hi), M + 1)
    w = np.sqrt(edges[:-1] * edges[1:]); dw = np.diff(edges)
    S = Sfun(w); Nn = Nfun(w)
    mu = (S + Nn) * dw / np.pi
    W = S / (S + Nn)
    Einf = float(np.sum(mu * W * (1 - W)))
    return w, mu, W, Einf


def ou_S(a, v):
    a = np.asarray(a, float); v = np.asarray(v, float)
    return lambda w: np.sum(2 * a[:, None] * v[:, None] / (a[:, None] ** 2 + w[None, :] ** 2), axis=0)


def osc_S(w0, zeta, var):
    """Second-order resonance x'' + 2 zeta w0 x' + w0^2 x = noise, scaled to variance var."""
    q = 4 * zeta * w0 ** 3 * var
    return lambda w: q / ((w0 ** 2 - w ** 2) ** 2 + (2 * zeta * w0 * w) ** 2)


# ---------------------------------------------------------------------------
# Model S, exact optimal filter: closed-loop poles c (interlacing) and residues
# H(s) = 1 - prod(s + a_j) / prod(s + c_i)  (causal Wiener filter, white noise)
# ---------------------------------------------------------------------------
def models_poles(a, v, N):
    """c_k > 0 with -c_k^2 the roots in x = omega^2 of N + sum 2 a_j v_j / (a_j^2 + x)."""
    a = np.asarray(a, float); v = np.asarray(v, float)
    J = len(a)
    num = np.poly1d([N])
    for j in range(J):
        num = num * np.poly1d([1.0, a[j] ** 2])
    for j in range(J):
        p = np.poly1d([2 * a[j] * v[j]])
        for i in range(J):
            if i != j:
                p = p * np.poly1d([1.0, a[i] ** 2])
        num = num + p
    x = np.roots(num.coeffs)
    return np.sort(np.sqrt(-np.real(x)))


def models_residues(a, c):
    a = np.asarray(a, float); c = np.asarray(c, float)
    r = []
    for k in range(len(c)):
        num = np.prod(a - c[k]); den = np.prod(np.delete(c, k) - c[k])
        r.append(-num / den)
    return np.array(r)


def load_stores():
    import importlib.util
    path = os.path.join(ROOT, "theory", "layers_checks", "stores.py")
    spec = importlib.util.spec_from_file_location("stores_lc", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------
def run(quick=False):
    ok, detail, res = [], [], {}
    rng = np.random.default_rng(20261121)

    # ---- L1: from-0 count = leftmost argmin for R >= 0 (converse: >0 distinct d) ----
    n_seq = 300 if quick else 3000
    Rgrid = np.logspace(-2, 4, 241)
    conv_mis, nonconv_hit, n_nonconv = 0, 0, 0
    for _ in range(n_seq):
        K = int(rng.integers(3, 8))
        if rng.random() < 0.5:   # convex: sorted positive decrements
            d = np.sort(rng.exponential(1.0, K))[::-1]
        else:                    # arbitrary distinct positive decrements
            d = rng.exponential(1.0, K)
        eps = np.r_[np.cumsum(d[::-1])[::-1], 0.0]
        convex = is_convex(eps)
        mism = [R for R in Rgrid if n60_from(eps, R) != argmin_J(eps, R)]
        if convex:
            conv_mis += len(mism)
        else:
            n_nonconv += 1
            # converse: some R in a fine grid between decrement values disagrees
            fine = np.sort(np.r_[Rgrid, 1.0 / ((d[:-1] + d[1:]) / 2), 1.0 / (d * 0.999), 1.0 / (d * 1.001)])
            nonconv_hit += any(n60_from(eps, R) != argmin_J(eps, R) for R in fine)
    res["L1"] = dict(sequences=n_seq, convex_mismatches=conv_mis, nonconvex=n_nonconv, nonconvex_with_mismatch=nonconv_hit)
    check(ok, detail, "L1 convex => N60 == argmin (all R)", conv_mis == 0, "mismatches %d" % conv_mis)
    check(ok, detail, "L1 non-convex => some R disagrees", nonconv_hit == n_nonconv, "%d/%d" % (nonconv_hit, n_nonconv))

    # ---- L2: halving and log-convexity => convex ---------------------------
    n2 = 2000 if quick else 20000
    bad_h = bad_l = 0
    for _ in range(n2):
        K = int(rng.integers(2, 8))
        r = rng.uniform(0, 0.5, K)               # halving ratios
        eps = np.cumprod(np.r_[1.0, r])
        bad_h += not is_convex(eps, 1e-15)
        r2 = np.sort(rng.uniform(0, 1, K))         # non-decreasing ratios = log-convex
        eps2 = np.cumprod(np.r_[1.0, r2])
        bad_l += not is_convex(eps2, 1e-15)
    res["L2"] = dict(n=n2, halving_nonconvex=bad_h, logconvex_nonconvex=bad_l)
    check(ok, detail, "L2 halving => convex", bad_h == 0)
    check(ok, detail, "L2 log-convex => convex", bad_l == 0)
    # and the 1/2 is sharp for a three-point tail (eps = 1, r, 0)
    check(ok, detail, "L2 ratio > 1/2 on (1, r, 0) is non-convex", not is_convex([1.0, 0.51, 0.0]) and is_convex([1.0, 0.5, 0.0]))

    # ---- T3: Ky Fan concavity ---------------------------------------------
    n3 = 200 if quick else 2000
    bad = 0
    for _ in range(n3):
        n = int(rng.integers(2, 12))
        A = rng.standard_normal((n, n)); T = A @ A.T
        lam = np.sort(np.linalg.eigvalsh(T))[::-1]
        V = np.r_[0.0, np.cumsum(lam)]
        eps = V[-1] - V   # residual = sum of trailing eigenvalues (Eckart-Young form)
        bad += not is_convex(eps, 1e-9 * V[-1])
    res["T3"] = dict(n=n3, nonconvex=bad)
    check(ok, detail, "T3 Ky Fan / Eckart-Young residual convex", bad == 0)

    # ---- T4: Monge K-link convexity ----------------------------------------
    def klink(Cm, Kmax):
        n = Cm.shape[0] - 1
        F = np.full(n + 1, np.inf); F[0] = 0.0
        outk = []
        for _k in range(1, Kmax + 1):
            F = np.min(F[:, None] + Cm, axis=0); F[0] = np.inf
            outk.append(F[n])
        return np.array(outk)
    n4 = 100 if quick else 600
    bad_m = 0; nonmonge_break = 0
    for _ in range(n4):
        n = int(rng.integers(6, 30))
        x = np.sort(rng.uniform(0, 10, n + 1))
        p = rng.uniform(1.1, 3.0)
        Cm = np.full((n + 1, n + 1), np.inf)
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                Cm[i, j] = (x[j] - x[i]) ** p          # convex of gap => Monge
        f = klink(Cm, min(n, 8))
        bad_m += not is_convex(f, 1e-9 * max(1.0, f[0]))
    # concave-of-gap (anti-Monge) can break convexity
    for _ in range(n4):
        n = int(rng.integers(6, 30))
        x = np.sort(rng.uniform(0, 10, n + 1))
        Cm = np.full((n + 1, n + 1), np.inf)
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                Cm[i, j] = np.sqrt(x[j] - x[i]) + rng.uniform(0, 0.3)
        f = klink(Cm, min(n, 8))
        nonmonge_break += not is_convex(f, 1e-9)
    res["T4"] = dict(n=n4, monge_nonconvex=bad_m, nonmonge_nonconvex=nonmonge_break)
    check(ok, detail, "T4 Monge K-link optimum convex in K", bad_m == 0)
    check(ok, detail, "T4 non-Monge costs can be non-convex", nonmonge_break > 0, "%d/%d" % (nonmonge_break, n4))

    # ---- T5: band model, monotone SNR => convex ----------------------------
    M = 160 if quick else 320
    Kmax = 8
    n5 = 60 if quick else 400
    worlds = []
    bad5 = 0
    for t in range(n5):
        kind = ["ou", "power", "colored"][t % 3]
        if kind == "ou":
            J = int(rng.integers(1, 7))
            sep = 10 ** rng.uniform(np.log10(3), 3, max(J - 1, 0))
            taus = np.cumprod(np.r_[10 ** rng.uniform(-1, 1), sep])
            a = 1 / taus; v = 10 ** rng.uniform(-1.5, 1.5, J); N = 10 ** rng.uniform(-3, 1)
            Sf = ou_S(a, v); Nf = lambda w, N=N: N + 0 * w
            lo, hi = a.min() * 1e-3, a.max() * 1e3 + 100
        elif kind == "power":
            al = rng.uniform(0.3, 3.0); w0 = 10 ** rng.uniform(-3, -1); c = 10 ** rng.uniform(-1, 1)
            N = 10 ** rng.uniform(-3, 0)
            Sf = lambda w, al=al, w0=w0, c=c: c / (w0 ** al + w ** al); Nf = lambda w, N=N: N + 0 * w
            lo, hi = w0 * 1e-3, 1e4
        else:  # colored noise rising with frequency, signal OU: SNR still decreasing
            J = int(rng.integers(1, 5))
            taus = np.cumprod(np.r_[1.0, 10 ** rng.uniform(0.5, 2.5, max(J - 1, 0))])
            a = 1 / taus; v = 10 ** rng.uniform(-1, 1, J); N = 10 ** rng.uniform(-3, 0); g = rng.uniform(0, 1.5)
            Sf = ou_S(a, v); Nf = lambda w, N=N, g=g: N * (1 + w) ** g
            lo, hi = a.min() * 1e-3, 1e4
        w, mu, W, Einf = spectrum_grid(Sf, Nf, lo, hi, M)
        mono = bool(np.all(np.diff(W) <= 1e-12))
        Eb = band_curve(mu, W, Kmax)
        eps = Eb / Einf
        cv = is_convex(eps, 1e-9 * max(1.0, eps[0]))
        bad5 += (mono and not cv)
        worlds.append(dict(kind=kind, monotone=mono, convex=cv, eps=[float(e) for e in eps]))
    n_mono = sum(wd["monotone"] for wd in worlds)
    res["T5"] = dict(n=n5, grid=M, Kmax=Kmax, monotone=n_mono, monotone_nonconvex=bad5,
                     max_ratio=float(max(max((wd["eps"][k + 1] / wd["eps"][k]) for k in range(Kmax) if wd["eps"][k] > 1e-12) for wd in worlds)))
    check(ok, detail, "T5 band model, monotone SNR => convex (K=0..%d)" % Kmax, bad5 == 0 and n_mono == n5, "monotone %d/%d, non-convex %d" % (n_mono, n5, bad5))

    # SSE quadrangle + mixed terminal inequality on random monotone W
    nq = 2000 if quick else 20000
    bad_q = bad_mix = 0
    for _ in range(nq):
        m = int(rng.integers(4, 25))
        mu = rng.exponential(1.0, m); W = np.sort(rng.uniform(0, 1, m))[::-1]
        C = seg_cost_matrix(mu, W)
        i, j, k, l = np.sort(rng.choice(m + 1, 4, replace=True))
        if i < k and j < l and j < k:
            lhs = C[i, k] + C[j, l]; rhs = C[i, l] + C[j, k]
            bad_q += lhs > rhs + 1e-10 * (1 + rhs)
        i, j, k = np.sort(rng.choice(m + 1, 3, replace=False))
        if i < j < k:
            z = lambda x: float(np.sum(mu[x:] * W[x:] ** 2))
            bad_mix += C[i, k] + z(j) > z(i) + C[j, k] + 1e-10 * (1 + z(i))
    res["T5_quadrangle"] = dict(n=nq, sse_violations=int(bad_q), mixed_violations=int(bad_mix))
    check(ok, detail, "T5 SSE quadrangle (monotone W)", bad_q == 0)
    check(ok, detail, "T5 mixed terminal-band inequality (monotone W)", bad_mix == 0)

    # ---- P6: failure class -------------------------------------------------
    e_bump = band_curve([2.0, 1.0, 1.0], [0.0, 1.0, 0.0], 2)
    res["P6_bump"] = dict(mu=[2, 1, 1], W=[0, 1, 0], E=[float(x) for x in e_bump])
    check(ok, detail, "P6 minimal bump (0,1,0; weights 2,1,1) non-convex",
          np.allclose(e_bump, [1.0, 2.0 / 3.0, 0.0]) and not is_convex(e_bump), "E = %s" % np.round(e_bump, 6).tolist())
    # rhythmic spectra: resonance peak over an OU background
    nr = 40 if quick else 240
    rh = []
    for t in range(nr):
        w0 = 10 ** rng.uniform(-1, 1); zeta = 10 ** rng.uniform(-2.5, -0.3)
        vb = 10 ** rng.uniform(-3, 0.5); ab = 10 ** rng.uniform(-3, 0)
        N = 10 ** rng.uniform(-3, -0.5)
        Sb = ou_S([ab], [vb]); So = osc_S(w0, zeta, 1.0)
        Sf = lambda w, Sb=Sb, So=So: Sb(w) + So(w)
        w, mu, W, Einf = spectrum_grid(Sf, lambda w, N=N: N + 0 * w, ab * 1e-3, w0 * 1e3, M)
        eps = band_curve(mu, W, Kmax) / Einf
        mono = bool(np.all(np.diff(W) <= 1e-12))
        # peak contrast: max W after its first local min divided by low-frequency W
        rh.append(dict(w0=w0, zeta=zeta, vb=vb, ab=ab, N=N, monotone=mono,
                       convex=is_convex(eps, 1e-9 * max(1.0, eps[0])), eps=[float(e) for e in eps]))
    n_nc = sum(not r["convex"] for r in rh)
    n_nc_mono = sum((not r["convex"]) and r["monotone"] for r in rh)
    res["P6_rhythm"] = dict(n=nr, nonconvex=n_nc, nonconvex_but_monotone=n_nc_mono,
                            nonmonotone=sum(not r["monotone"] for r in rh))
    check(ok, detail, "P6 rhythmic band curves can be non-convex", n_nc > 0, "%d/%d non-convex" % (n_nc, nr))
    check(ok, detail, "P6 every non-convex rhythmic case has non-monotone W", n_nc_mono == 0)
    # the known Model-S-outside counterexample world (two oscillators, rhythm_counterexample.py)
    ac = np.array([0.015043913155370778 + 0.8245963835269933j, 0.015043913155370778 - 0.8245963835269933j,
                   0.005596688432223706 + 0.05512283118769611j, 0.005596688432223706 - 0.05512283118769611j])
    vc = np.array([0.16591255090832438, 0.16591255090832438, 0.1809360888442601, 0.1809360888442601], dtype=complex)
    Nc = 0.04014640614993535
    Sc = lambda w: np.real(np.sum(vc[:, None] * 2 * ac[:, None] / (ac[:, None] ** 2 + w[None, :] ** 2), axis=0))
    _, muc, Wc, Eic = spectrum_grid(Sc, lambda w: Nc + 0 * w, 1e-4, 1e3, M)
    epc = band_curve(muc, Wc, 6) / Eic
    nonmono_c = bool(np.any(np.diff(Wc) > 1e-9))
    res["P6_counterexample_world"] = dict(W_nonmonotone=nonmono_c, band_eps=[float(e) for e in epc],
                                          band_convex=is_convex(epc, 1e-9), W_max_rise=float(np.max(np.diff(Wc))))
    check(ok, detail, "P6 the two-oscillator counterexample world has non-monotone W", nonmono_c,
          "band curve convex: %s; band eps K=0..6 %s" % (is_convex(epc, 1e-9), np.round(epc, 4).tolist()))
    # submodular set value whose best-K value is not concave
    sets = {"a": {1, 2, 3, 4, 5, 6}, "b": {1, 2, 7, 8}, "c": {3, 4, 9, 10}, "d": {5, 6, 11, 12}}
    f = lambda S: len(set().union(*[sets[s] for s in S])) if S else 0
    g = [max(f(S) for S in itertools.combinations(sets, k)) for k in range(4)]
    res["P6_submodular"] = dict(best_k=g)
    check(ok, detail, "P6 coverage (submodular) best-K value not concave", g == [0, 6, 8, 12] and not is_convex([-x for x in g]), "g = %s" % g)


    # ---- T6: Model S, J = 2 is convex on K = 0, 1, 2 (constructive bound) ----
    st = load_stores()
    n6 = 100 if quick else 1000
    inter_bad = res_bad = bound_bad = yj_bad = 0; worst = 0.0; frac_min = 1.0
    for t in range(n6):
        J = 2 if t % 2 == 0 else int(rng.integers(3, 7))
        a = np.sort(1 / np.cumprod(np.r_[10 ** rng.uniform(-1, 1), 10 ** rng.uniform(0.1, 3, J - 1)]))
        v = 10 ** rng.uniform(-1.5, 1.5, J); N = 10 ** rng.uniform(-3, 1)
        c = models_poles(a, v, N)
        inter_bad += not all(a[k] < c[k] and (k == J - 1 or c[k] < a[k + 1]) for k in range(J))
        r = models_residues(a, c)
        res_bad += not np.all(r > 0)
        Einf, g = st.mse_given_b(a, v, c, N)           # E_J at the Kalman rates = E_inf
        E0 = float(np.sum(v))
        if t < 40:  # cross-check against the Yovits-Jackson integral
            yj = st.E_inf(a, v, N); yj_bad += abs(Einf - yj) > 1e-4 * yj
        E1_designs = [st.mse_given_b(a, v, np.array([ck]), N)[0] for ck in c]
        gain_best = E0 - min(E1_designs)
        frac = gain_best / (E0 - Einf)                  # share of the full gain from one store
        frac_min = min(frac_min, frac)
        if J == 2:
            bound_bad += min(E1_designs) > 0.5 * (E0 + Einf) * (1 + 1e-12)
            worst = max(worst, (min(E1_designs) - Einf) / (E0 - Einf))
        else:
            bound_bad += frac < 1.0 / J - 1e-12
    res["T6"] = dict(n=n6, interlacing_fail=inter_bad, residue_nonpositive=res_bad, bound_fail=bound_bad,
                     yj_mismatch=yj_bad, J2_max_excess_share=worst, min_one_store_share=frac_min)
    check(ok, detail, "T6 Model S poles interlace a_1<c_1<a_2<...<a_J<c_J", inter_bad == 0)
    check(ok, detail, "T6 Model S optimal-filter residues all positive", res_bad == 0)
    check(ok, detail, "T6 E_J at Kalman rates == Yovits-Jackson E_inf", yj_bad == 0)
    check(ok, detail, "T6 J=2: one Kalman-rate store gives E_1 <= (E_0+E_inf)/2 (=> convex on 0..2); J>2: share >= 1/J",
          bound_bad == 0, "J=2 worst (E1-Einf)/(E0-Einf) = %.4f; min one-store share %.4f" % (worst, frac_min))

    # ---- S5 Model S evidence (read-only) ------------------------------------
    if os.path.exists(S5):
        ws = json.load(open(S5))["worlds"]
        halv = 0; mx = {}
        for wd in ws:
            e = wd["eps"]
            okw = all(e[K + 1] <= e[K] / 2 + 1e-6 for K in range(len(e) - 1) if e[K] > 1e-4)
            halv += okw
            for K in range(len(e) - 2):
                if e[K] > 1e-4:
                    key = "J%d_K%d" % (wd["J"], K)
                    mx[key] = max(mx.get(key, 0.0), e[K + 1] / e[K])
        res["S5"] = dict(worlds=len(ws), halving_holds=halv, max_ratio=mx)
        check(ok, detail, "S5 Model S halving eps_{K+1} <= eps_K/2 (K=0..J)", halv == len(ws), "%d/%d; max ratios %s" % (halv, len(ws), {k: round(v, 4) for k, v in mx.items()}))
    return ok, detail, res


def main():
    quick = "--quick" in sys.argv
    ok, detail, res = run(quick=quick)
    for line in detail:
        print(line)
    allok = all(c for _, c in ok)
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w") as fh:
            json.dump(dict(summary={k: v for k, v in res.items()}, all_pass=allok), fh, indent=1, default=float)
    print("ALL LAYER CONVEXITY CHECKS PASS" if allok else "SOME LAYER CONVEXITY CHECKS FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
