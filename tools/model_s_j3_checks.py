#!/usr/bin/env python3
"""Numerical checks for theory/MODEL_S_J3.md (N67, N68).

NUMERICAL, not the proof of the weak-third-mode subclass. They check:
  (1) a nondegenerate two-mode world has a strict convexity gap, and a
      sufficiently weak third mode keeps the decrements non-increasing;
  (2) a low-SNR three-mode world stays convex (the known halving miss is the
      four-mode example in LAYER_CONVEXITY.md, not this draw);
  (3) a screen of three-mode worlds. The certificate is one-sided: a positive
      value of E1 - 2 E2 + E_inf, after replacing a grid value E2 > E1 by E1
      (two stores can copy one store), certifies d2 >= d3. It does not certify
      d1 >= d2, because a high grid E2 inflates E0 - 2 E1 + E2. A negative
      one-sided value is re-optimised before it can count as a counterexample.
      Clipping E2 up to E_inf when a value undercuts the floor makes the
      one-sided gap smaller, not larger.

    nice -n 19 python3 tools/model_s_j3_checks.py
    nice -n 19 python3 tools/model_s_j3_checks.py --full
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def spectral_cs(a, v, N):
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    J = len(a)
    base = np.poly(-(a ** 2)).astype(float)
    P = N * base
    for j in range(J):
        others = np.delete(-(a ** 2), j)
        pj = np.poly(others) if J > 1 else np.array([1.0])
        term = np.zeros(J + 1)
        term[-len(pj):] = 2.0 * a[j] * v[j] * pj
        P = P + term
    rts = np.roots(P)
    c2 = [-float(r.real) for r in rts if abs(r.imag) < 1e-7 and r.real < -1e-14]
    if len(c2) != J:
        return None
    return np.sqrt(np.sort(np.array(c2, float)))


def mse_many(a, v, B, N, rcond=1e-12):
    """MSE of the optimal gains at each row of rates B (n, K)."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    B = np.atleast_2d(np.asarray(B, float))
    n, K = B.shape
    bi = B[:, :, None]
    bj = B[:, None, :]
    Ms = np.zeros((n, K, K))
    rr = np.zeros((n, K))
    for j in range(len(a)):
        Ms += v[j] * (bi * bj) / (bi + bj) * (1.0 / (a[j] + bi) + 1.0 / (a[j] + bj))
        rr += v[j] * B / (a[j] + B)
    M = Ms + N * (bi * bj) / (bi + bj)
    scale = np.sqrt(np.clip(np.diagonal(M, axis1=1, axis2=2), 1e-30, None))
    Ms = M / (scale[:, :, None] * scale[:, None, :])
    rs = rr / scale
    lam, U = np.linalg.eigh(Ms)
    # keep well-conditioned modes; a near-tie of rates must not undercut E_inf
    thresh = rcond * np.maximum(lam.max(axis=1), 1e-30)
    keep = lam > thresh[:, None]
    captured = np.zeros(n)
    for i in range(n):
        ui = U[i]
        ci = ui.T @ rs[i]
        kk = keep[i]
        captured[i] = np.sum(ci[kk] ** 2 / lam[i][kk]) if np.any(kk) else 0.0
    out = float(np.sum(v)) - captured
    out = np.where(np.isfinite(out), out, np.sum(v))
    return out


def mse_one_design(a, v, b, N):
    return float(mse_many(a, v, np.atleast_2d(b), N)[0])


def best_one(a, v, N, ngrid=800):
    lo = np.log(a.min()) - 4.0
    hi = np.log(a.max()) + 6.0
    grid = np.exp(np.linspace(lo, hi, ngrid))
    vals = mse_many(a, v, grid[:, None], N)
    j = int(np.argmin(vals))
    res = minimize(lambda x: mse_one_design(a, v, np.exp(x), N), [np.log(grid[j])],
                   method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=400))
    return min(float(vals[j]), float(res.fun))


def best_two_grid(a, v, N, ngrid):
    lo = np.log(a.min()) - 3.0
    hi = np.log(a.max()) + 5.0
    g = np.exp(np.linspace(lo, hi, ngrid))
    b1, b2 = np.meshgrid(g, g, indexing="ij")
    mask = b2 >= b1 * (1.0 + 1e-9)
    B = np.stack([b1[mask], b2[mask]], axis=1)
    best = np.inf
    step = 25000
    for s in range(0, len(B), step):
        vals = mse_many(a, v, B[s:s + step], N)
        best = min(best, float(np.min(vals)))
    return best


def best_two_polish(a, v, N, starts, seed):
    rng = np.random.default_rng(seed)
    lo = np.log(a.min()) - 3.0
    hi = np.log(a.max()) + 5.0
    cs = spectral_cs(a, v, N)
    inits = [np.linspace(lo + 0.5, hi - 0.5, 2)]
    if cs is not None and len(cs) >= 2:
        from itertools import combinations
        for comb in combinations(range(len(cs)), 2):
            inits.append(np.log(cs[list(comb)]))
    for _ in range(starts):
        inits.append(np.sort(rng.uniform(lo, hi, 2)))
    best = np.inf

    def obj(x):
        return mse_one_design(a, v, np.exp(np.sort(x)), N)

    for x0 in inits:
        res = minimize(obj, np.sort(x0), method="Nelder-Mead",
                       options=dict(xatol=1e-9, fatol=1e-13, maxiter=2000, adaptive=True))
        if res.fun < best:
            best = float(res.fun)
    return best


def curve(a, v, N, n2, polish_starts=0, seed=0):
    # Sort rates only. Variances stay in input order, so a vector built as
    # v_j proportional to sqrt(a_j) before this sort is not that pairing after it.
    a = np.sort(np.asarray(a, float))
    v = np.asarray(v, float)
    cs = spectral_cs(a, v, N)
    if cs is None:
        return None
    E0 = float(np.sum(v))
    Einf = mse_one_design(a, v, cs, N)
    E1 = best_one(a, v, N)
    E2 = best_two_grid(a, v, N, n2)
    if polish_starts:
        E2 = min(E2, best_two_polish(a, v, N, polish_starts, seed))
    # One-sided certificate for d2 >= d3. Copying the one-store rate shows
    # E2 <= E1, so a grid value above E1 may be replaced by E1. Raising a
    # value that undercuts E_inf makes E1 - 2 E2 + E_inf smaller.
    E2_cert = min(E2, E1)
    if E2_cert < Einf:
        E2_cert = Einf
    Es = np.array([E0, E1, E2_cert, Einf], float)
    dec = Es[:-1] - Es[1:]
    sd = dec[:-1] - dec[1:]
    return {"E": Es, "dec": dec, "sd": sd, "slack": float(sd.min()),
            "rel": float(sd.min()) / max(E0, 1e-30), "a": a, "v": v, "N": float(N), "cs": cs}


def check(ok, lines, name, cond, msg=""):
    ok.append((name, bool(cond)))
    lines.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


def screen(full):
    """Return list of certified curve dicts. Pessimistic grid first."""
    worlds = []
    # weak third mode, the subclass
    worlds.append((np.array([1.0, 30.0, 30.0 * 4.0]), np.array([1.0, 0.4, 1e-8]), 0.1))
    # comparable three
    worlds.append((np.array([1.0, 10.0, 100.0]), np.ones(3), 0.05))
    worlds.append((np.array([1.0, 1e3, 1e6]), np.array([1.0, 1.0, 1.0]), 1.0))
    # Three-mode draw written as v proportional to sqrt(a) on this input order.
    # curve sorts the rates and does not reorder v, so the scored world is not
    # that pairing. The halving miss remains the four-mode example, not this row.
    a = np.array([1.0, 1e-3, 1e-6])
    worlds.append((a, (10 ** -6.5) * np.sqrt(a), 1.0))
    if full:
        rng = np.random.default_rng(7)
        for _ in range(80):
            aa = np.sort(10 ** rng.uniform(-3, 3, 3))
            aa = aa * np.exp(np.linspace(0, 1e-8, 3))
            vv = 10 ** rng.uniform(-2, 1, 3)
            NN = float(10 ** rng.uniform(-3, 2))
            worlds.append((aa, vv, NN))
        # targeted: one large mode, two smaller and closer
        for sep in (2.0, 4.0):
            for ratio in (0.2, 1.0, 5.0):
                aa = np.array([1.0, 10 ** sep, 10 ** sep * 1.4])
                worlds.append((aa, np.array([1.0, ratio, ratio]), 0.05))
                worlds.append((aa, np.array([1.0, ratio, ratio]), 10.0))
    n2 = 36 if full else 24
    out = []
    for i, (a, v, N) in enumerate(worlds):
        # pessimistic certificate
        r = curve(a, v, N, n2=n2, polish_starts=0, seed=i)
        if r is None:
            continue
        if r["rel"] < 1e-8:
            r = curve(a, v, N, n2=n2, polish_starts=(16 if full else 8), seed=1000 + i)
        r["index"] = i
        out.append(r)
    return out


def main(argv=None):
    argv = sys.argv if argv is None else argv
    full = "--full" in argv
    ok, lines = [], []
    rows = screen(full)
    # subclass illustration is row 0
    r0 = rows[0]
    check(ok, lines, "weak third mode convex", r0["slack"] >= -1e-10 * r0["E"][0],
          "rel %.3e E %s" % (r0["rel"], np.array2string(r0["E"], precision=4)))
    # two-mode strict gap, recovered by dropping the third variance
    a = np.array([1.0, 30.0])
    v = np.array([1.0, 0.4])
    N = 0.1
    two = curve(a, v, N, n2=30, polish_starts=0)
    check(ok, lines, "two-mode strict gap", two["sd"][0] > 1e-6 and two["dec"][1] > 1e-8,
          "sd %s dec %s" % (two["sd"], two["dec"]))
    # halving can miss while convexity holds: the J=3 low-SNR world, row 3
    low = rows[3]
    # ratio of excesses eps2/eps1 = (E2/Einf - 1) / (E1/Einf - 1)
    E = low["E"]
    if E[3] > 0 and E[1] > E[3]:
        ratio = (E[2] / E[3] - 1.0) / (E[1] / E[3] - 1.0)
    else:
        ratio = 0.0
    check(ok, lines, "low-SNR world convex", low["slack"] >= -1e-8 * low["E"][0],
          "rel %.3e" % low["rel"])
    # not a claim that halving fails on this particular draw; just record the ratio
    lines.append("low-SNR excess ratio eps2/eps1 = %.4f (halving would need <= 0.5)" % ratio)
    neg = [r for r in rows if r["rel"] < -1e-7]
    check(ok, lines, "no certified counterexample in %d worlds" % len(rows), len(neg) == 0,
          "negatives %d" % len(neg))
    rels = [r["rel"] for r in rows]
    lines.append("screen n=%d min relative slack %.6e" % (len(rows), min(rels)))
    nfail = sum(1 for _, c in ok if not c)
    lines.append("%d checks, %d failed" % (len(ok), nfail))
    if nfail == 0:
        lines.append("ALL J3 CHECKS PASS")
    text = "\n".join(lines)
    print(text)
    if full:
        out_dir = os.path.join(ROOT, "theory", "model_s_j3_checks")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "results_full.json")
        dumped = []
        for r in rows:
            dumped.append({
                "rel": r["rel"], "slack": r["slack"],
                "E": r["E"].tolist(), "dec": r["dec"].tolist(), "sd": r["sd"].tolist(),
                "a": r["a"].tolist(), "v": r["v"].tolist(), "N": r["N"], "index": r["index"],
            })
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"n": len(rows), "min_rel": min(rels), "negatives": len(neg),
                       "rows": dumped, "log": text}, fh, indent=1)
        print("wrote", path)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
