#!/usr/bin/env python3
"""Independent review 2: a halo-model-style matched null for the SDSS radius-graph hub statistic (COSMIC_WEB.md section 2b).
Run: nice -n 19 python3 hub_nulls_hm.py > hub_nulls_hm.out   (numpy, scipy; needs sdss_r0.csv from web_hubs_sdss.py's query)
Same data selection, mask rule and statistics as web_hubs_sdss.py. Null "HM": every point traces a SMOOTHED lognormal field
(Gaussian smoothing R = 1.5 Mpc/h on a 256^3 grid in a 192 Mpc/h periodic box, so the field variance stays small and realisations
are not dominated by a few cells), and a fraction of points sit in small Gaussian groups (Thomas clusters, sizes 0.15 to 1.2
Mpc/h) around parents that also trace the field: a two-halo-like term from the field plus a one-halo-like term from the groups.
The field is scaled by one common factor (two passes, 12 mocks each) to the data at r > 4.5 Mpc/h; group amplitudes are fitted
by non-negative least squares to the excess of the data's xi_s over the field at r < 4.5 Mpc/h and rescaled once by a common factor; then FRESH mocks are drawn (seeds not used in calibration).
Because xi fixes only the product (fraction in groups) x (group occupancy), the family has a free occupancy m (mean group
members after thinning to N): three members m = 15, 30 and 60 with the same xi. They show how far the hub statistic moves at
fixed two-point function. Validation as in COSMIC_WEB.md section 8 item 3.
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
rng = np.random.default_rng(777001)
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
    if l is None:
        fk = lambda x: (t.query_ball_point(P, x, return_length=True) - 1).mean() - kmean
        if fk(0.02) > 0: return dict(mean=np.nan, vm=np.nan, kmax=np.nan, top1=np.nan, l=0.02)
        l = brentq(fk, 0.02, 30.0, xtol=1e-3)
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


NG, L, RS = 256, 192.0, 1.5; cell = L / NG
ax = (np.fft.fftfreq(NG, 1.0 / NG) * cell).astype(np.float32)
RR = np.sqrt(ax[:, None, None] ** 2 + ax[None, :, None] ** 2 + ax[None, None, :] ** 2)
kx = (2 * np.pi * np.fft.fftfreq(NG, cell)).astype(np.float32); kz = (2 * np.pi * np.fft.rfftfreq(NG, cell)).astype(np.float32)
K2 = kx[:, None, None] ** 2 + kx[None, :, None] ** 2 + kz[None, None, :] ** 2
pair_d = np.linalg.norm(rng.random((200000, 3)) - rng.random((200000, 3)), axis=1) * cell
def make_xifun(tab):
    lr, lx = np.log(rc), np.log(tab)
    sl_lo = (lx[1] - lx[0]) / (lr[1] - lr[0]); sl_hi = (lx[-1] - lx[-2]) / (lr[-1] - lr[-2])
    def f(r):
        l = np.log(np.maximum(r, 0.05)); out = np.interp(l, lr, lx)
        out = np.where(l < lr[0], lx[0] + sl_lo * (l - lr[0]), out); out = np.where(l > lr[-1], lx[-1] + sl_hi * (l - lr[-1]), out)
        return np.exp(out)
    return f
def field_amp(tab):
    f = make_xifun(tab); xiG = np.log1p(f(RR)).astype(np.float32); xiG[0, 0, 0] = np.mean(np.log1p(f(pair_d))); xiG[RR > L / 2] = 0.0
    P = np.maximum(np.fft.rfftn(xiG).real, 0) * np.exp(-K2 * RS * RS)          # Gaussian smoothing of the Gaussian field
    return np.sqrt(P).astype(np.float32)
def field(seed, amp):
    g = np.random.default_rng(seed)
    dG = np.fft.irfftn(np.fft.rfftn(g.standard_normal((NG, NG, NG)).astype(np.float32)) * amp, s=(NG, NG, NG), axes=(0, 1, 2))
    vG = float(dG.var()); d = np.exp(dG - vG / 2); return d / d.mean(), vG, g
def sample_field(g, dens, n):
    p = dens.ravel() / dens.sum(); cnt = g.poisson(n * p)
    idx = np.repeat(np.arange(cnt.size), cnt)
    return (np.stack(np.unravel_index(idx, (NG, NG, NG)), 1) + g.random((len(idx), 3))) * cell - L / 2
sigj = np.array([0.15, 0.3, 0.6, 1.2])
def hj(r, s): return (4 * np.pi * s * s) ** -1.5 * np.exp(-r * r / (4 * s * s))
def binavg(s):
    out = []
    for a, b in zip(bins[:-1], bins[1:]):
        rr = np.linspace(a, b, 200); w = rr ** 2; out.append(np.sum(hj(rr, s) * w) / np.sum(w))
    return np.array(out)
Hm = np.stack([binavg(s) for s in sigj], 1)
nhi = 3.0 * nbar; Nbox = nhi * L ** 3
def hm_mock(seed, amp, Aj, mpost):
    dens, vG, g = field(seed, amp)
    mj = mpost * nhi / nbar                                       # occupancy before thinning to N
    fj = Aj * nhi / mj                                            # A_j = f_j m_j / n_box
    if fj.sum() > 0.95: return None, vG, fj.sum()
    pts = [sample_field(g, dens, (1 - fj.sum()) * Nbox)]
    for f_, s_ in zip(fj, sigj):
        if f_ <= 0: continue
        par = sample_field(g, dens, f_ * Nbox / mj); nch = g.poisson(mj, len(par))
        pts.append(np.repeat(par, nch, axis=0) + g.normal(scale=s_, size=(nch.sum(), 3)))
    pts = (np.vstack(pts) + L / 2) % L - L / 2
    return select(pts), vG, fj.sum()
def hm_ok(seed, amp, Aj, mpost):
    while True:
        P_, vG, F = hm_mock(seed, amp, Aj, mpost)
        if P_ is not None: return P_, vG, F
        if F > 0.95: raise SystemExit("occupancy too small for this amplitude: F = %.2f" % F)
        SKIP.append(seed); seed += 100000
SKIP = []
# field table: data xi at r >= 3.3 Mpc/h, a much shallower slope below (the groups carry the small scales), so var(G) stays near 1
tab = xi.copy(); i3 = np.searchsorted(rc, 3.0)
tab[:i3] = xi[i3] * (rc[:i3] / rc[i3]) ** -0.3
amp = field_amp(tab)
def field_only(seed, amp):
    d, vG, g = field(seed, amp); return select(sample_field(g, d, Nbox)), vG
far = rc >= 4.5
for it in range(3):
    xs = []; vgs = []
    for s in range(12):
        P_, vG = field_only(300 + 20 * it + s, amp); xs.append(ls_xi(P_)); vgs.append(vG)
    xF = np.mean(xs, 0); eF = np.std(xs, 0, ddof=1) / np.sqrt(len(xs))
    log("field-only pass %d: var(G) = %.2f, mock/data xi_s = %s (+- %s)" % (it, np.mean(vgs), np.round(xF / xi, 3), np.round(eF / xi, 3)))
    if it < 2:
        corr = np.clip(np.mean(xi[far] / xF[far]) ** 0.8, 0.75, 1.35)      # one common factor for the field (less noise than per bin)
        tab[i3:] = tab[i3:] * corr; tab[:i3] = tab[i3] * (rc[:i3] / rc[i3]) ** -0.3; amp = field_amp(tab)
Wt = 1 / xi
near = rc < 4.5
Aj, _ = nnls((Hm * Wt[:, None])[near], (np.maximum(xi - xF, 0) * Wt)[near])
log("group amplitudes A_j = %s for sigma_j = %s (fitted to the small-scale excess of the data over the field)" % (np.round(Aj, 3), sigj))
MCAL = 30.0
for it in range(2):
    xs = []; vgs = []
    for s in range(12):
        P_, vG, F = hm_ok(400 + 20 * it + s, amp, Aj, MCAL); xs.append(ls_xi(P_)); vgs.append(vG)
    r_ = np.mean(xs, 0) / xi
    log("HM check pass %d (m = %.1f): var(G) = %.2f, F = %.3f, mock/data xi_s = %s (%.0f s)" % (it, MCAL, np.mean(vgs), F, np.round(r_, 3), time.time() - t0))
    if it == 0:
        Aj = Aj * np.clip(np.mean(1 / r_[near]) , 0.7, 1.4)               # one common factor for the groups
        log("   groups rescaled: A_j = %s" % np.round(Aj, 3))
NM = 30; FAM = {}
for mpost in (15.0, 30.0, 60.0):
    rows, xs = [], []
    for s in range(NM):
        P_, vG, F = hm_ok(2000 + int(10 * mpost) * 100 + s, amp, Aj, mpost); xs.append(ls_xi(P_)); rows.append(allstats(P_, lfix))
    FAM[mpost] = (rows, np.array(xs), F)
    log("HM m = %4.1f: fraction of points in groups F = %.3f, %d fresh mocks (%.0f s)" % (mpost, F, NM, time.time() - t0))
def summ(rows, key): v_ = np.array([r[key] for r in rows], float); return np.nanmean(v_), np.nanstd(v_, ddof=1)
sel = (rc >= 1.0) & (rc <= 20.0)
log("\n=== VALIDATION (COSMIC_WEB.md section 8 item 3: xi within 10 percent over 1-20 Mpc/h on >= 20 untuned mocks; mean degree at fixed l scatters <= 30 percent)")
OK = {}
for mpost, (rows, xs, F) in FAM.items():
    r_ = xs.mean(0) / xi; err = xs.std(0, ddof=1) / np.sqrt(len(xs)) / xi
    sc = [summ(rows, "kfix%d" % i) for i in (0, 1)]
    ok1 = bool(np.all(np.abs(r_[sel] - 1) <= 0.10)); ok2 = all(s_[1] / s_[0] <= 0.30 for s_ in sc); OK[mpost] = ok1 and ok2
    log("HM m=%4.1f mock/data xi_s (r = %s): %s (+-%s); worst |dev| over 1-20 Mpc/h %.3f; also at r = 0.63, 0.98: %.3f, %.3f" % (mpost, np.round(rc, 2), np.round(r_, 3), np.round(err, 3), np.abs(r_[sel] - 1).max(), r_[0], r_[1]))
    log("HM m=%4.1f mean degree at fixed l = %.2f: %.2f +- %.2f (scatter %.0f%%); at l = %.2f: %.2f +- %.2f (scatter %.0f%%) -> xi check %s, scatter check %s"
        % (mpost, lfix[0], sc[0][0], sc[0][1], 100 * sc[0][1] / sc[0][0], lfix[1], sc[1][0], sc[1][1], 100 * sc[1][1] / sc[1][0], "PASS" if ok1 else "FAIL", "PASS" if ok2 else "FAIL"))
log("\n=== HUB STATISTIC S1 (top-1 percent share of degree) and secondaries: data vs null mean +- sd; z = (data - mean)/sd")
for mpost, (rows, xs, F) in FAM.items():
    log("-- HM m = %.1f (F = %.2f; %d sets; null %s)" % (mpost, F, len(rows), "VALID" if OK[mpost] else "FAILS VALIDATION"))
    for key in ("S1_4", "S1_10", "vm4", "vm10", "kmax4", "kmax10", "l4", "l10", "knn20"):
        m_, s_ = summ(rows, key); log("   %-7s data %8.4f   null %8.4f +- %7.4f   z = %+6.2f   data/null - 1 = %+6.1f%%" % (key, DATA[key], m_, s_, (DATA[key] - m_) / s_, 100 * (DATA[key] / m_ - 1)))
log("\nH_hub rule of section 8 item 5 (S1 above null mean by > 3 sd AND by >= 25 percent, at <k> = 4 and 10), single SDSS arm only:")
for mpost, (rows, xs, F) in FAM.items():
    res = []
    for key in ("S1_4", "S1_10"):
        m_, s_ = summ(rows, key); res.append("exceeds" if (DATA[key] > m_ + 3 * s_ and DATA[key] >= 1.25 * m_) else ("below by > 3 sd" if DATA[key] < m_ - 3 * s_ else "within"))
    log("  m = %4.1f: <k> = 4 %s; <k> = 10 %s" % (mpost, res[0], res[1]))
log("mocks redrawn (fewer than N points in the footprint): %s" % SKIP)
log("elapsed %.0f s" % (time.time() - t0))
