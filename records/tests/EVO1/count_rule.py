#!/usr/bin/env python3
"""THEORY §3 layer-counting rule (v2.5.2 text, frozen for EVO1), applied identically to the PREDICTED design and to each
EVOLVED design.  In silico the response kernel is known from the design; the 'measurement' adds fixed Gaussian noise.
Steps used: (1) band of time scales fixed per world; (2) step responses on an isolated unit (shared stores cut off) and
pooled (common step to all units); (3) fit sums of exponentials K = 0..KFIT, accept K+1 over K only if dBIC >= 10,
ignore poles outside the band; (4) classify before merging: local if in the isolated response, shared if only in the
pooled response (a pooled pole within x3 of an isolated pole is that local pole); merge within a class poles < x3 apart;
(5) count by degree (all poles here are real, degree 1); (6) relay test: not applicable (no relay stores exist in the
genome); (7)-(9) dot scoring: not applicable (the comparison is to PREDICTIONS_EVO.json, frozen by hash)."""
import numpy as np
from scipy.optimize import minimize
KFIT = 5; DBIC = 10.0; NPTS = 240; MEAS_SD = 0.01; MERGE = 3.0

def step_resp(t, b, g, lead=0):
    t = np.asarray(t, float)[:, None]; b = np.asarray(b, float)[None, :]; g = np.asarray(g, float)[None, :]
    if b.size == 0: return np.zeros(t.shape[0])
    tt = np.clip(t - lead, 0, None)
    return (g * (1 - np.exp(-b * tt))).sum(1)

def fit(t, y, K, seed=0):
    if K == 0: return float(np.sum(y ** 2)), []
    lt = np.log(t); rng = np.random.default_rng(seed)
    def rss(x):
        r = np.exp(x); X = 1 - np.exp(-np.outer(t, r))
        A, *_ = np.linalg.lstsq(X, y, rcond=None); return float(np.sum((y - X @ A) ** 2))
    best = (np.inf, None)
    inits = [-np.linspace(lt.min() + 0.5, lt.max() - 0.5, K)] + [-np.sort(rng.uniform(lt.min() - 1, lt.max() + 1, K)) for _ in range(10)]
    for x0 in inits:
        r = minimize(rss, x0, method='Nelder-Mead', options=dict(xatol=1e-6, fatol=1e-14, maxiter=3000 * K))
        if r.fun < best[0]: best = (r.fun, r.x)
    return best[0], list(np.exp(best[1]))

def poles(t, y, band):
    n = len(t); prev = None; chosen = []
    for K in range(0, KFIT + 1):
        R, r = fit(t, y, K)
        bic = n * np.log(max(R, 1e-300) / n) + 2 * K * np.log(n)
        if prev is not None and prev[0] - bic < DBIC: break
        prev = (bic, r); chosen = r
    lo, hi = band
    return sorted(x for x in chosen if lo <= 1 / x <= hi)

def merge(rs):
    rs = sorted(rs); groups = []
    for r in rs:
        if groups and r / groups[-1][-1] < MERGE: groups[-1].append(r)
        else: groups.append([r])
    return [float(np.exp(np.mean(np.log(g)))) for g in groups]

def count(design, band, lead=0, seed=2026):
    """design: dict(bl, gl, bc, gc). band: (tau_min, tau_max) in steps. Returns counted local and shared poles (rates)."""
    rng = np.random.default_rng(seed)
    t = np.exp(np.linspace(np.log(band[0] / 3), np.log(band[1] * 3), NPTS))
    scale = (np.sum(np.abs(design['gl'])) + np.sum(np.abs(design.get('gc', [])))) or 1.0
    yi = step_resp(t, design['bl'], design['gl']) + MEAS_SD * scale * rng.standard_normal(NPTS)
    L = poles(t, yi, band)
    if len(design.get('bc', [])):
        yp = step_resp(t, design['bl'], design['gl']) + step_resp(t, design['bc'], design['gc'], lead) + MEAS_SD * scale * rng.standard_normal(NPTS)
        Pp = poles(t, yp, band)
    else:
        Pp = list(L)
    S = [p for p in Pp if not any(max(p, l) / min(p, l) < MERGE for l in L)]
    Lm, Sm = merge(L), merge(S)
    return dict(local=Lm, shared=Sm, structure=f'{len(Lm)}L{len(Sm)}S', K=len(Lm) + len(Sm))
