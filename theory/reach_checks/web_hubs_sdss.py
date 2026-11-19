#!/usr/bin/env python3
"""REACH check 5 (own computation; NOT the published pipelines): degree / hub statistics of a proximity graph of real
galaxies against matched nulls.   Run: nice -n 19 python3 web_hubs_sdss.py > web_hubs_sdss.out   (numpy, scipy; network on first run)
Data: SDSS DR17 legacy main sample from the public SkyServer SQL service (no login), saved as sdss_r0.csv in the working dir:
  SELECT s.ra, s.dec, s.z, p.petroMag_r - p.extinction_r AS r0 FROM SpecObj AS s JOIN PhotoObjAll AS p ON p.objID = s.bestObjID
  WHERE s.class='GALAXY' AND s.zWarning=0 AND s.sciencePrimary=1 AND s.survey='sdss' AND s.z BETWEEN 0.005 AND 0.03
Sample: volume-limited so the mean density is uniform: M_r - 5 log h < MCUT, using M = r0 - 25 - 5 log10((1+z) D_C), no K-correction
  (<= ~0.05 mag at z <= 0.03), and D <= DMAX with the flux limit r = 17.77 leaving >= 0.5 mag margin.
Assumptions: flat LCDM, Om = 0.3; distances in Mpc/h; redshift-space positions (no peculiar-velocity correction).
Footprint mask: random sky points kept if >= 10 data galaxies lie within 3 degrees (same mask for every point set).
Nulls (same mask, same D range, same N):
  P  = Poisson points, uniform in the cone volume (geometry only)
  LN = lognormal-field points in a periodic box (observer at the centre), Poisson-sampled; the input correlation function is
       set to the data's measured redshift-space xi_s(r) (Landy-Szalay table, log-interpolated) after ONE calibration correction from
       6 mocks; the final mocks' xi_s is then checked. Approximately two-point matched, each mock subsampled to exactly N,
       no higher-order structure, no halos.
STATUS OF THE LN NULL: the lognormal mocks have var(G) about 4, scatter strongly from realisation to realisation, and over-cluster at
       r < 7 Mpc/h after the one calibration pass (see the printed check), so radius-graph comparisons with LN are INCONCLUSIVE here.
       The kNN in-degree comparison is stable across mocks and is reported.
Graphs: undirected radius graph, linking length tuned to a target mean degree in EACH point set, AND at a fixed physical length
       equal to the data's tuned value; statistics: var/mean of the degree, max degree, top-1% share of total degree,
       Hill tail index of the top 1% of degrees (informal, noisy, not used). Directed k-nearest-neighbour in-degree (Coutinho's M3 rule).
"""
import os, sys, numpy as np
from scipy.spatial import cKDTree
from scipy.integrate import quad
from scipy.optimize import brentq
import urllib.request, urllib.parse
MCUT, DMAX, DMIN = -17.5, 85.0, 15.0
CSV = os.path.join(os.getcwd(), "sdss_r0.csv")
Q = ("SELECT s.ra, s.dec, s.z, p.petroMag_r - p.extinction_r AS r0 FROM SpecObj AS s JOIN PhotoObjAll AS p ON p.objID = s.bestObjID "
     "WHERE s.class='GALAXY' AND s.zWarning=0 AND s.sciencePrimary=1 AND s.survey='sdss' AND s.z BETWEEN 0.005 AND 0.03")
if not os.path.exists(CSV):
    url = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch?" + urllib.parse.urlencode({"cmd": Q, "format": "csv"})
    open(CSV, "wb").write(urllib.request.urlopen(url, timeout=300).read())
A = np.array([[float(x) for x in l.split(",")] for l in open(CSV) if not l.startswith("#") and not l.startswith("ra")])
print("rows from SkyServer: %d; with a usable r0 (10 < r0 < 20): %d" % (len(A), ((A[:, 3] > 10) & (A[:, 3] < 20)).sum()))
A = A[(A[:, 3] > 10) & (A[:, 3] < 20)]
C_KMS, Om = 299792.458, 0.3
def Dc(zz): return (C_KMS / 100.0) * quad(lambda x: 1 / np.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, zz)[0]
zg = np.linspace(0, 0.031, 400); Dg = np.array([Dc(x) for x in zg])
D_all = np.interp(A[:, 2], zg, Dg)
M = A[:, 3] - 25 - 5 * np.log10((1 + A[:, 2]) * D_all)
k = (M < MCUT) & (D_all <= DMAX) & (D_all >= DMIN)
A, D = A[k], D_all[k]
ra, dec = np.radians(A[:, 0]), np.radians(A[:, 1])
def sph2cart(r, a, d): return np.c_[r * np.cos(d) * np.cos(a), r * np.cos(d) * np.sin(a), r * np.sin(d)]
X = sph2cart(D, ra, dec); N = len(D)
print("volume-limited sample (M_r-5logh < %.1f, %.0f <= D <= %.0f Mpc/h): N = %d" % (MCUT, DMIN, DMAX, N))
u = sph2cart(1.0, ra, dec); utree = cKDTree(u)
rng = np.random.default_rng(20261118)
ANG = 2 * np.sin(np.radians(3.0) / 2)
def in_mask(v): return utree.query_ball_point(v, ANG, return_length=True) >= 10
def rand_sky(n):
    out, have = [], 0
    while have < n:
        v = rng.normal(size=(4 * n, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; v = v[in_mask(v)]
        out.append(v); have += len(v)
    return np.vstack(out)[:n]
v = rng.normal(size=(200000, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; frac = in_mask(v).mean()
print("footprint mask covers %.3f of the sphere (%.0f deg^2)" % (frac, frac * 41253))
Vcone = frac * 4 * np.pi / 3 * (DMAX ** 3 - DMIN ** 3); nbar = N / Vcone
print("cone volume %.3g (Mpc/h)^3, mean density %.4f per (Mpc/h)^3" % (Vcone, nbar))
def poisson_null(n):
    Dn = (DMIN ** 3 + rng.random(n) * (DMAX ** 3 - DMIN ** 3)) ** (1 / 3.0); return rand_sky(n) * Dn[:, None]

def ls_xi(Xd, Xr, bins):
    td, tr = cKDTree(Xd), cKDTree(Xr); nd, nr = len(Xd), len(Xr)
    dd = np.diff(td.count_neighbors(td, bins)) / (nd * (nd - 1.0))
    rr = np.diff(tr.count_neighbors(tr, bins)) / (nr * (nr - 1.0))
    dr = np.diff(td.count_neighbors(tr, bins)) / (nd * nr)
    return (dd - 2 * dr + rr) / rr
bins = np.array([0.5, 0.8, 1.2, 1.8, 2.7, 4, 6, 9, 13, 20.0]); rc = np.sqrt(bins[1:] * bins[:-1])
Xr = poisson_null(5 * N)
xi = ls_xi(X, Xr, bins)
print("xi_s(r) of the data (Landy-Szalay, 5N Poisson randoms, no weights, no integral-constraint correction):")
for r_, x_ in zip(rc, xi): print("  r = %5.2f  xi = %.3f" % (r_, x_))

def make_xifun(tab):
    lr, lx = np.log(rc), np.log(tab)
    sl_lo = (lx[1] - lx[0]) / (lr[1] - lr[0]); sl_hi = (lx[-1] - lx[-2]) / (lr[-1] - lr[-2])
    def f(r):
        l = np.log(np.maximum(r, 0.3)); out = np.interp(l, lr, lx)
        out = np.where(l < lr[0], lx[0] + sl_lo * (l - lr[0]), out); out = np.where(l > lr[-1], lx[-1] + sl_hi * (l - lr[-1]), out)
        return np.exp(out)
    return f

NG, L = 384, 320.0
ax = np.fft.fftfreq(NG, 1.0 / NG) * (L / NG)
RR = np.sqrt(ax[:, None, None] ** 2 + ax[None, :, None] ** 2 + ax[None, None, :] ** 2).astype(np.float32)
def lognormal_mock(seed, xif, nhi):
    g = np.random.default_rng(seed)
    xiG = np.log1p(xif(RR)).astype(np.float32); xiG[RR > L / 2] = 0.0
    P = np.maximum(np.fft.rfftn(xiG).real, 0).astype(np.float32); del xiG
    w = g.normal(size=(NG, NG, NG)).astype(np.float32)
    dG = np.fft.irfftn(np.fft.rfftn(w) * np.sqrt(P), s=(NG, NG, NG), axes=(0, 1, 2)); del w, P
    vG = dG.var(); ln = np.exp(dG - dG.mean() - 0.5 * vG); ln /= ln.mean(); del dG
    cell = L / NG
    cnt = g.poisson(nhi * cell ** 3 * ln); idx = np.repeat(np.arange(cnt.size), cnt.ravel())
    pts = (np.stack(np.unravel_index(idx, cnt.shape), 1) + g.random((len(idx), 3))) * cell - L / 2
    r = np.linalg.norm(pts, axis=1); kk = (r <= DMAX) & (r >= DMIN); pts, r = pts[kk], r[kk]
    kk = in_mask(pts / r[:, None]); pts = pts[kk]
    keep = g.random(len(pts)) < min(1.0, 2.0 * nbar / nhi)    # thin, leaving more than N points (nhi >= 3 nbar) ...
    pts = pts[keep]; assert len(pts) >= N, len(pts)
    return pts[g.choice(len(pts), N, replace=False)], vG       # ... then draw exactly N, as for the data and the Poisson null
nhi = 3.0 * nbar
tab = xi.copy()
print("calibration: the lognormal input table is corrected ONCE by (data xi_s / mean mock xi_s) from 6 mocks (seeds 900-905), clipped to 0.5-1.4")
xif0 = make_xifun(tab)
xm0 = np.mean([ls_xi(lognormal_mock(900 + sd, xif0, nhi)[0], poisson_null(5 * N), bins) for sd in range(6)], axis=0)
print("  mock/data xi_s before correction:", np.round(xm0 / xi, 2))
tab = tab * np.clip(xi / np.maximum(xm0, 1e-3 * xi), 0.5, 1.4)
print("final input xi table:", np.round(tab, 3))

def stats_deg(k):
    ks = np.sort(k)[::-1]; n = len(k); top = ks[: max(1, n // 100)]
    lt = np.mean(np.log(top / top[-1])) if top[-1] > 0 else 0
    return dict(mean=k.mean(), vm=k.var() / k.mean(), kmax=int(k.max()), top1=top.sum() / k.sum(), iso=(k == 0).mean(), hill=(1 / lt if lt > 0 else np.nan))
def radius_stats(P, kmean=None, l=None):
    t = cKDTree(P)
    if l is None: l = brentq(lambda x: (t.query_ball_point(P, x, return_length=True) - 1).mean() - kmean, 0.05, 30.0, xtol=1e-3)
    s = stats_deg(t.query_ball_point(P, l, return_length=True) - 1.0); s["l"] = l; return s
def knn_stats(P, kk):
    t = cKDTree(P); _, nb = t.query(P, kk + 1); ind = np.bincount(nb[:, 1:].ravel(), minlength=len(P)); return ind.var() / ind.mean(), int(ind.max())
def ms_(rows, key): return np.nanmean([r[key] for r in rows]), np.nanstd([r[key] for r in rows])
def report(name, sets, lfix):
    print("\n== %s  (%d point set%s; N = %s)" % (name, len(sets), "s" if len(sets) > 1 else "", sorted(set(len(P) for P in sets))[:3]))
    for km in (4, 10):
        rows = [radius_stats(P, kmean=km) for P in sets]
        f = lambda key: "%.3g+-%.2g" % ms_(rows, key)
        print("  radius graph tuned to <k> = %2d: l = %s  var/mean = %s  kmax = %s  top-1%% share = %s  isolated = %s  Hill = %s" % (km, f("l"), f("vm"), f("kmax"), f("top1"), f("iso"), f("hill")))
    for lf in lfix:
        rows = [radius_stats(P, l=lf) for P in sets]
        f = lambda key: "%.3g+-%.2g" % ms_(rows, key)
        print("  radius graph at fixed l = %.2f Mpc/h: <k> = %s  var/mean = %s  kmax = %s  top-1%% share = %s  isolated = %s  Hill = %s" % (lf, f("mean"), f("vm"), f("kmax"), f("top1"), f("iso"), f("hill")))
    for kk in (1, 4, 20):
        rows = [knn_stats(P, kk) for P in sets]
        print("  directed kNN in-degree, k = %2d: var/mean = %.2f+-%.2f  max in-degree = %.0f+-%.0f" % (kk, np.mean([r[0] for r in rows]), np.std([r[0] for r in rows]), np.mean([r[1] for r in rows]), np.std([r[1] for r in rows])))
lfix = [radius_stats(X, kmean=4)["l"], radius_stats(X, kmean=10)["l"]]
NS = 8
report("DATA (SDSS legacy main, volume-limited)", [X], lfix)
report("NULL P: Poisson points in the same cone", [poisson_null(N) for _ in range(NS)], lfix)
xif = make_xifun(tab); lns = []; vgs = []
for sd in range(NS):
    p_, v_ = lognormal_mock(100 + sd, xif, nhi); lns.append(p_); vgs.append(v_)
print("\nlognormal mocks: N per mock = %s, var(G) = %.2f" % ([len(c) for c in lns], np.mean(vgs)))
xm = np.mean([ls_xi(c, poisson_null(5 * len(c)), bins) for c in lns[:4]], axis=0)
print("final check (4 other mocks), mock vs data xi_s:"); [print("  r = %5.2f  data %.3f  mock %.3f" % (r_, a_, b_)) for r_, a_, b_ in zip(rc, xi, xm)]
report("NULL LN: lognormal field matched to the data's xi_s", lns, lfix)

# ---- reference graphs with the same N (needs networkx; skipped if absent): scale for the hub statistic
try:
    import networkx as nx
    print("\n== REFERENCE GRAPHS, N = %d (not point sets; for scale only)" % N)
    for name, G in (("Barabasi-Albert m=2", nx.barabasi_albert_graph(N, 2, seed=1)), ("Barabasi-Albert m=5", nx.barabasi_albert_graph(N, 5, seed=1)),
                    ("Erdos-Renyi <k>=4", nx.gnp_random_graph(N, 4.0 / N, seed=1))):
        s_ = stats_deg(np.array([d for _, d in G.degree()], float))
        print("  %-22s <k> = %.2f  var/mean = %.2f  kmax = %d  top-1%% share = %.3f" % (name, s_["mean"], s_["vm"], s_["kmax"], s_["top1"]))
except ImportError:
    print("networkx not available; reference graphs skipped")
