#!/usr/bin/env python3
"""STATUS: this run STOPPED. The LN2 calibration diverged (var(G) 6.5 -> 15.3 -> 22.6 over three passes; see hub_nulls_v2.out) and a
final mock was so clustered that no linking length gave <k> = 4; the CP part never ran. Kept as evidence that a fine-grid lognormal
cannot be calibrated to this xi_s. The working null is hub_nulls_hm.py.
Independent review 2, improved matched nulls for the SDSS radius-graph hub statistic (COSMIC_WEB.md section 2b).
Run: nice -n 19 python3 hub_nulls_v2.py > hub_nulls_v2.out   (numpy, scipy; needs sdss_r0.csv from web_hubs_sdss.py's query)
Same data selection as web_hubs_sdss.py (volume-limited SDSS DR17 main sample, N = 16,535), same mask rule, same statistics.
Nulls built here (both are fitted to the data's measured xi_s monopole; neither has redshift-space anisotropy):
 LN2  lognormal field, FIXED versus web_hubs_sdss.py: (i) finer grid, 512^3 cells in a 192 Mpc/h periodic box (cell 0.375 Mpc/h,
      against 0.83); (ii) the zero-lag Gaussian variance is the cell average of ln(1+xi) over pairs of points inside one cell, not
      ln(1+xi(0.3 Mpc/h)), which is what made the first version over-cluster below one cell; (iii) the input table is calibrated by
      three damped passes (8 mocks each, seeds 500+), then 50 FRESH mocks (seeds 1000+) are used both for the validation required
      by COSMIC_WEB.md section 8 item 3 and for the statistic.
 CP   Thomas cluster processes (Neyman-Scott, Poisson offspring, Gaussian offsets) whose pair correlation is fitted EXACTLY in form
      to the data's xi_s by non-negative least squares over six cluster sizes; three members of the family with the same xi but
      different occupancy (clustered fraction F = 0.9, 0.5, 0.25 of points, occupancy proportional to cluster volume). They show
      how much the hub statistic depends on structure beyond two-point.
"""
import os, sys, time, numpy as np
from scipy.spatial import cKDTree
from scipy.integrate import quad
from scipy.optimize import brentq, nnls
import scipy.fft as sfft
t0 = time.time()
def log(*a):
    print(*a); sys.stdout.flush()
MCUT, DMAX, DMIN = -17.5, 85.0, 15.0
A = np.array([[float(x) for x in l.split(",")] for l in open("sdss_r0.csv") if not l.startswith("#") and not l.startswith("ra")])
A = A[(A[:, 3] > 10) & (A[:, 3] < 20)]
C_KMS, Om = 299792.458, 0.3
def Dc(zz): return (C_KMS / 100.0) * quad(lambda x: 1 / np.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, zz)[0]
zg = np.linspace(0, 0.031, 400); Dg = np.array([Dc(x) for x in zg]); D_all = np.interp(A[:, 2], zg, Dg)
M = A[:, 3] - 25 - 5 * np.log10((1 + A[:, 2]) * D_all)
k = (M < MCUT) & (D_all <= DMAX) & (D_all >= DMIN); A, D = A[k], D_all[k]
ra, dec = np.radians(A[:, 0]), np.radians(A[:, 1])
def sph2cart(r, a, d): return np.c_[r * np.cos(d) * np.cos(a), r * np.cos(d) * np.sin(a), r * np.sin(d)]
X = sph2cart(D, ra, dec); N = len(X)
utree = cKDTree(sph2cart(1.0, ra, dec)); ANG = 2 * np.sin(np.radians(3.0) / 2)
def in_mask(v): return utree.query_ball_point(v, ANG, return_length=True) >= 10
rng = np.random.default_rng(424242)
def rand_sky(n):
    out, have = [], 0
    while have < n:
        v = rng.normal(size=(4 * n, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; v = v[in_mask(v)]; out.append(v); have += len(v)
    return np.vstack(out)[:n]
v = rng.normal(size=(200000, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; frac = in_mask(v).mean()
Vcone = frac * 4 * np.pi / 3 * (DMAX ** 3 - DMIN ** 3); nbar = N / Vcone
log("data N = %d, mask %.0f deg^2, nbar = %.4f (h/Mpc)^3" % (N, frac * 41253, nbar))
def poisson_null(n):
    Dn = (DMIN ** 3 + rng.random(n) * (DMAX ** 3 - DMIN ** 3)) ** (1 / 3.0); return rand_sky(n) * Dn[:, None]
Xr = poisson_null(5 * N); trr = cKDTree(Xr)
bins = np.array([0.5, 0.8, 1.2, 1.8, 2.7, 4, 6, 9, 13, 20.0]); rc = np.sqrt(bins[1:] * bins[:-1])
RRc = np.diff(trr.count_neighbors(trr, bins)) / (len(Xr) * (len(Xr) - 1.0))
def ls_xi(Xd):
    td = cKDTree(Xd); nd, nr = len(Xd), len(Xr)
    dd = np.diff(td.count_neighbors(td, bins)) / (nd * (nd - 1.0)); dr = np.diff(td.count_neighbors(trr, bins)) / (nd * nr)
    return (dd - 2 * dr + RRc) / RRc
xi = ls_xi(X)
log("data xi_s:", np.round(xi, 3))
def select(pts):
    r = np.linalg.norm(pts, axis=1); kk = (r <= DMAX) & (r >= DMIN); pts, r = pts[kk], r[kk]
    pts = pts[in_mask(pts / r[:, None])]
    if len(pts) < N: return None
    return pts[rng.choice(len(pts), N, replace=False)]
def stats_deg(kd):
    ks = np.sort(kd)[::-1]; top = ks[: max(1, len(kd) // 100)]
    return dict(mean=kd.mean(), vm=kd.var() / kd.mean(), kmax=kd.max(), top1=top.sum() / kd.sum())
def radius_stats(P, kmean=None, l=None):
    t = cKDTree(P)
    if l is None: l = brentq(lambda x: (t.query_ball_point(P, x, return_length=True) - 1).mean() - kmean, 0.05, 30.0, xtol=1e-3)
    s = stats_deg(t.query_ball_point(P, l, return_length=True) - 1.0); s["l"] = l; return s
def knn_vm(P, kk=20):
    _, nb = cKDTree(P).query(P, kk + 1); ind = np.bincount(nb[:, 1:].ravel(), minlength=len(P)); return ind.var() / ind.mean()
def allstats(P, lfix):
    out = {}
    for km in (4, 10):
        s = radius_stats(P, kmean=km); out.update({"l%d" % km: s["l"], "vm%d" % km: s["vm"], "kmax%d" % km: s["kmax"], "S1_%d" % km: s["top1"]})
    for i, lf in enumerate(lfix): out["kfix%d" % i] = radius_stats(P, l=lf)["mean"]
    out["knn20"] = knn_vm(P); return out
lfix = [radius_stats(X, kmean=4)["l"], radius_stats(X, kmean=10)["l"]]
DATA = allstats(X, lfix)
log("DATA:", {k_: round(float(v_), 4) for k_, v_ in DATA.items()})

# ------------------------------------------------------------------ LN2: corrected lognormal
NG, L = 512, 192.0; cell = L / NG
ax = (np.fft.fftfreq(NG, 1.0 / NG) * cell).astype(np.float32)
RR = np.sqrt(ax[:, None, None] ** 2 + ax[None, :, None] ** 2 + ax[None, None, :] ** 2)
pair_d = np.linalg.norm(rng.random((200000, 3)) - rng.random((200000, 3)), axis=1) * cell   # separations inside one cell
def make_xifun(tab):
    lr, lx = np.log(rc), np.log(tab)
    sl_lo = (lx[1] - lx[0]) / (lr[1] - lr[0]); sl_hi = (lx[-1] - lx[-2]) / (lr[-1] - lr[-2])
    def f(r):
        l = np.log(np.maximum(r, 0.05)); out = np.interp(l, lr, lx)
        out = np.where(l < lr[0], lx[0] + sl_lo * (l - lr[0]), out); out = np.where(l > lr[-1], lx[-1] + sl_hi * (l - lr[-1]), out)
        return np.exp(out)
    return f
def ln_power(tab):
    f = make_xifun(tab); xiG = np.log1p(f(RR)).astype(np.float32)
    xiG[0, 0, 0] = np.mean(np.log1p(f(pair_d)))            # cell-averaged zero lag
    xiG[RR > L / 2] = 0.0
    P = sfft.rfftn(xiG, workers=4).real; del xiG
    return np.sqrt(np.maximum(P, 0)).astype(np.float32)
def ln_mock(seed, sqP, nhi):
    g = np.random.default_rng(seed)
    w = g.standard_normal((NG, NG, NG), dtype=np.float32)
    dG = sfft.irfftn(sfft.rfftn(w, workers=4) * sqP, s=(NG, NG, NG), workers=4); del w
    vG = float(dG.var()); dens = np.exp(dG - vG / 2); dens /= dens.mean(); del dG
    cnt = g.poisson(nhi * cell ** 3 * dens).ravel(); del dens
    idx = np.repeat(np.arange(cnt.size), cnt); del cnt
    pts = (np.stack(np.unravel_index(idx, (NG, NG, NG)), 1) + g.random((len(idx), 3))) * cell - L / 2
    return select(pts), vG
def ln_mock_ok(seed, sqP, nhi):
    while True:
        P_, vg = ln_mock(seed, sqP, nhi)
        if P_ is not None: return P_, vg
        SKIP.append(seed); seed += 100000
nhi = 5.0 * nbar
SKIP = []
tab = xi.copy()
for it in range(3):
    sqP = ln_power(tab); xs = []; vgs = []
    for sd in range(8):
        P_, vg = ln_mock_ok(500 + 10 * it + sd, sqP, nhi); xs.append(ls_xi(P_)); vgs.append(vg)
    ratio = np.mean(xs, axis=0) / xi
    log("LN2 calibration pass %d: var(G) = %.2f, mean mock/data xi_s = %s  (%.0f s)" % (it, np.mean(vgs), np.round(ratio, 2), time.time() - t0))
    tab = tab * np.clip((1 / ratio) ** 0.7, 0.6, 1.6)
sqP = ln_power(tab)
log("LN2 final input table:", np.round(tab, 3))
NM = 50; LNrows = []; LNxi = []
for sd in range(NM):
    P_, vg = ln_mock_ok(1000 + sd, sqP, nhi); LNxi.append(ls_xi(P_)); LNrows.append(allstats(P_, lfix))
    if sd % 10 == 9: log("  LN2 mock %d done (%.0f s)" % (sd + 1, time.time() - t0))
LNxi = np.array(LNxi)
np.save("LN2_xi.npy", LNxi)

# ------------------------------------------------------------------ CP: Thomas cluster processes fitted to xi_s
sig = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0])
def h(r, s): return (4 * np.pi * s * s) ** -1.5 * np.exp(-r * r / (4 * s * s))
# fit bin-averaged xi (pair-weighted average over each bin, r^2 dr) to the data
def binavg(s):
    out = []
    for a, b in zip(bins[:-1], bins[1:]):
        rr = np.linspace(a, b, 200); w = rr ** 2; out.append(np.sum(h(rr, s) * w) / np.sum(w))
    return np.array(out)
Hm = np.stack([binavg(s) for s in sig], 1)
Wt = 1 / xi                                                       # fit in relative error
Acoef, _ = nnls(Hm * Wt[:, None], xi * Wt)
log("CP fit: A_j = %s for sigma_j = %s; fitted/data xi = %s" % (np.round(Acoef, 3), sig, np.round(Hm @ Acoef / xi, 3)))
def cp_mock(F, nbox):
    # occupancy m_j proportional to sigma_j^3, scaled so the clustered fraction sum_j f_j = F, with f_j = A_j nbox / m_j
    use = Acoef > 0; kap = nbox * np.sum(Acoef[use] / sig[use] ** 3) / F; m = kap * sig ** 3
    pts = []
    nclust = 0
    for Aj, sj, mj in zip(Acoef, sig, m):
        if Aj <= 0: continue
        pj = Aj * nbox ** 2 / mj ** 2                              # parent density: p m^2 / n^2 = A
        npar = rng.poisson(pj * L ** 3); par = rng.random((npar, 3)) * L - L / 2
        nch = rng.poisson(mj, npar); ch = np.repeat(par, nch, axis=0) + rng.normal(scale=sj, size=(nch.sum(), 3))
        pts.append(ch); nclust += nch.sum()
    nf = rng.poisson(max(nbox * L ** 3 - nclust, 0)); pts.append(rng.random((nf, 3)) * L - L / 2)
    pts = np.vstack(pts); pts = (pts + L / 2) % L - L / 2
    return select(pts), m
def cp_mock_ok(F, nbox):
    while True:
        P_, m = cp_mock(F, nbox)
        if P_ is not None: return P_, m
        SKIP.append(("CP", F))
CP = {}
for F in (0.9, 0.5, 0.25):
    rows, xs = [], []
    for sd in range(20):
        P_, m = cp_mock_ok(F, 2.0 * nbar); xs.append(ls_xi(P_)); rows.append(allstats(P_, lfix))
    CP[F] = (rows, np.array(xs), m)
    log("CP F = %.2f: occupancy m_j = %s  (%.0f s)" % (F, np.round(m, 2), time.time() - t0))

# ------------------------------------------------------------------ report
def summ(rows, key): v_ = np.array([r[key] for r in rows], float); return v_.mean(), v_.std(ddof=1)
log("\n=== VALIDATION (COSMIC_WEB.md section 8 item 3: xi within 10%% over 1-20 Mpc/h on >= 20 untuned mocks; mean degree at fixed l scatters <= 30%%)")
sel = (rc >= 1.0) & (rc <= 20.0)
def validate(name, xs, rows):
    r_ = xs.mean(0) / xi; err = xs.std(0, ddof=1) / np.sqrt(len(xs)) / xi
    sc = [summ(rows, "kfix%d" % i) for i in (0, 1)]
    ok1 = np.all(np.abs(r_[sel] - 1) <= 0.10); ok2 = all(s[1] / s[0] <= 0.30 for s in sc)
    log("%-10s mock/data xi_s by bin (r = %s): %s (+-%s)" % (name, np.round(rc, 2), np.round(r_, 3), np.round(err, 3)))
    log("%-10s mean degree at fixed l = %.2f: %.2f +- %.2f (scatter %.0f%%); at l = %.2f: %.2f +- %.2f (scatter %.0f%%)   -> xi check %s, scatter check %s"
        % (name, lfix[0], sc[0][0], sc[0][1], 100 * sc[0][1] / sc[0][0], lfix[1], sc[1][0], sc[1][1], 100 * sc[1][1] / sc[1][0], "PASS" if ok1 else "FAIL", "PASS" if ok2 else "FAIL"))
    return ok1 and ok2
okLN = validate("LN2", LNxi, LNrows)
okCP = {F: validate("CP F=%.2f" % F, CP[F][1], CP[F][0]) for F in CP}
log("\n=== HUB STATISTIC S1 (top-1%% share) and secondaries; data vs null mean +- sd (z = (data - mean)/sd; excess = data/mean - 1)")
def comp(name, rows, ok):
    log("-- %s (%d sets; null %s)" % (name, len(rows), "VALID" if ok else "FAILS VALIDATION"))
    for key in ("S1_4", "S1_10", "vm4", "vm10", "kmax4", "kmax10", "l4", "l10", "knn20"):
        m_, s_ = summ(rows, key); log("   %-7s data %8.4f   null %8.4f +- %7.4f   z = %+6.2f   excess %+6.1f%%" % (key, DATA[key], m_, s_, (DATA[key] - m_) / s_, 100 * (DATA[key] / m_ - 1)))
comp("LN2 corrected lognormal", LNrows, okLN)
for F in CP: comp("CP Thomas mixture, clustered fraction F = %.2f" % F, CP[F][0], okCP[F])
log("\nH_hub as specified (S1 > null mean + 3 sd AND >= 25%% above, at <k> = 4 and 10): ")
for name, rows in [("LN2", LNrows)] + [("CP F=%.2f" % F, CP[F][0]) for F in CP]:
    res = []
    for key in ("S1_4", "S1_10"):
        m_, s_ = summ(rows, key); res.append(DATA[key] > m_ + 3 * s_ and DATA[key] >= 1.25 * m_)
    log("  %-9s %s" % (name, "EXCEEDS at both" if all(res) else ("exceeds at one" if any(res) else "does not exceed")))
log("mocks redrawn because fewer than N points fell in the footprint (seeds or CP members): %s" % SKIP)
log("elapsed %.0f s" % (time.time() - t0))
