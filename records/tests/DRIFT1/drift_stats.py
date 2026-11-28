"""DRIFT1 analysis functions. Written before any new data was pulled (see PREREG.md)."""
import numpy as np
from sklearn.mixture import GaussianMixture
import diptest
import statsmodels.api as sm


def rate_tests(log10_rates, seed=0):
    u = np.asarray(log10_rates, float)
    u = u[np.isfinite(u)]
    n = len(u)
    q05, q50, q95 = np.quantile(u, [0.05, 0.5, 0.95])
    span = q95 - q05
    # dip test (on lightly jittered data to break ties from integer counts)
    rng = np.random.default_rng(seed)
    uj = u + rng.uniform(-0.005, 0.005, n)
    dip, dip_p = diptest.diptest(uj)
    # Gaussian mixtures k=1..6 by BIC
    X = uj.reshape(-1, 1)
    best = None
    bics = []
    for k in range(1, 7):
        g = GaussianMixture(k, n_init=5, random_state=seed).fit(X)
        b = g.bic(X); bics.append(b)
        if best is None or b < best[0]:
            best = (b, k, g)
    _, kbest, g = best
    w = g.weights_; mu = g.means_.ravel(); sd = np.sqrt(g.covariances_.ravel())
    order = np.argsort(mu); w, mu, sd = w[order], mu[order], sd[order]
    sep_pairs = []
    big = [i for i in range(kbest) if w[i] >= 0.10]
    for a in range(len(big)):
        for b in range(a + 1, len(big)):
            i, j = big[a], big[b]
            D = abs(mu[i] - mu[j]) / np.sqrt((sd[i] ** 2 + sd[j] ** 2) / 2)
            sep_pairs.append((float(mu[i]), float(mu[j]), float(D)))
    well_sep = any(D >= 2 for _, _, D in sep_pairs)
    # shape of the central 90%: Poisson GLM on 0.1-decade bins, linear vs quadratic log-density
    c = u[(u >= q05) & (u <= q95)]
    edges = np.arange(q05, q95 + 0.1, 0.1)
    cnt, _ = np.histogram(c, edges)
    mid = (edges[:-1] + edges[1:]) / 2
    z = mid - mid.mean()
    X1 = sm.add_constant(z); X2 = sm.add_constant(np.column_stack([z, z * z]))
    m1 = sm.GLM(cnt, X1, family=sm.families.Poisson()).fit()
    m2 = sm.GLM(cnt, X2, family=sm.families.Poisson()).fit()
    k1, k2 = 2, 3
    bic1 = -2 * m1.llf + k1 * np.log(len(cnt)); bic2 = -2 * m2.llf + k2 * np.log(len(cnt))
    a, b1, b2 = m2.params
    vertex = -b1 / (2 * b2) + mid.mean() if b2 != 0 else np.nan
    f = lambda x: np.exp(a + b1 * (x - mid.mean()) + b2 * (x - mid.mean()) ** 2)
    peaked = bool((bic1 - bic2 > 10) and b2 < 0 and (q05 + 0.5 <= vertex <= q95 - 0.5)
                  and f(vertex) / f(q05) >= 2 and f(vertex) / f(q95) >= 2)
    slope_lin = m1.params[1] / np.log(10)   # d log10(density) / d log10(rate) in the central range
    # decision (PREREG rule)
    if span < 2:
        verdict = "NARROW"
    elif dip_p < 0.01 and kbest >= 2 and well_sep:
        verdict = "BUNCHED"
    elif peaked:
        verdict = "BROAD_PEAKED"
    else:
        verdict = "SCALE_FREE"
    return dict(n=n, q05=float(q05), q50=float(q50), q95=float(q95), span_decades=float(span), dip=float(dip),
                dip_p=float(dip_p), gmm_k=int(kbest), gmm_w=w.round(3).tolist(), gmm_mu=mu.round(3).tolist(),
                gmm_sd=sd.round(3).tolist(), sep_pairs=sep_pairs, dBIC_quad_vs_lin=float(bic1 - bic2),
                vertex=float(vertex), peak_to_edge=(float(f(vertex) / f(q05)), float(f(vertex) / f(q95))),
                central_loglog_slope=float(slope_lin), verdict=verdict)


def spectrum_tests(counts, dt_hours, calendar_periods_hours, seed=0):
    """counts: evenly spaced event counts. Removes calendar cycles by subtracting the mean profile for each
    calendar period (phase-folded), then Welch-free raw periodogram, log-binned (20 bins/decade).
    Fits single vs broken power law on log-binned power by BIC; flags non-calendar peaks."""
    y = np.asarray(counts, float).copy()
    n = len(y)
    t = np.arange(n)
    for P in calendar_periods_hours:
        L = int(round(P / dt_hours))
        if 2 <= L < n // 2:
            ph = t % L
            prof = np.bincount(ph, y, L) / np.bincount(ph, minlength=L)
            y = y - prof[ph] + prof.mean()
    mean_count = float(np.mean(counts))
    y = y - y.mean()
    win = np.hanning(n)
    F = np.fft.rfft(y * win)
    P = (np.abs(F) ** 2)[1:]
    shot = mean_count * np.sum(win ** 2)        # expected periodogram level of Poisson counting noise
    f = np.fft.rfftfreq(n, d=dt_hours)[1:]          # cycles per hour
    keep = f >= 4.0 / (n * dt_hours)
    f, P = f[keep], P[keep]
    # mask calendar harmonics (+-2 bins)
    df = f[1] - f[0]
    mask = np.ones(len(f), bool)
    for Pc in calendar_periods_hours:
        for h in range(1, 50):
            fc = h / Pc
            if fc > f[-1]:
                break
            mask &= np.abs(f - fc) > 2.5 * df
    # fit only where the binned power is >= 3x the Poisson shot-noise floor (else the floor makes a fake break)
    lf = np.log10(f)
    bins = np.arange(lf.min(), lf.max() + 0.05, 0.05)
    idx = np.digitize(lf, bins)
    xb, yb = [], []
    for i in np.unique(idx):
        s = (idx == i) & mask
        if s.sum() >= 1 and P[s].mean() >= 3 * shot:
            xb.append(lf[s].mean()); yb.append(np.log10(P[s].mean() - shot))
    xb, yb = np.array(xb), np.array(yb)
    nb = len(xb)
    if nb < 15:
        return dict(n=n, verdict='TOO_NOISY', n_fit_bins=nb)
    def bic(res, k):
        return nb * np.log(np.mean(res ** 2)) + k * np.log(nb)
    p1 = np.polyfit(xb, yb, 1); r1 = yb - np.polyval(p1, xb); b1 = bic(r1, 2)
    best = (np.inf, None)
    for j in range(5, nb - 5):
        A = np.column_stack([np.ones(nb), xb, np.maximum(xb - xb[j], 0)])
        coef, *_ = np.linalg.lstsq(A, yb, rcond=None)
        r = yb - A @ coef
        b = bic(r, 4)
        if b < best[0]:
            best = (b, (xb[j], coef[1], coef[1] + coef[2]))
    b2, (brk, s_lo, s_hi) = best
    broken = bool((b1 - b2 > 10) and abs(s_hi - s_lo) >= 0.3)
    # non-calendar peaks: raw periodogram vs local smooth (running median over 41 bins); chi2_2 tail
    from scipy.ndimage import median_filter
    sm_ = median_filter(P, size=41, mode="nearest") / np.log(2)   # median of exp(1) = ln2 * mean
    ratio = P / sm_
    thr = np.log(mask.sum() / 0.001)                 # Bonferroni p=0.01 for exp(1)-distributed ratios
    peaks = np.where(mask & (ratio > thr) & (f < 0.9 * f[-1]))[0]
    peak_periods_h = sorted(set(np.round(1 / f[peaks], 1).tolist()))[:20]
    return dict(n=n, slope_single=float(p1[0]), dBIC_broken=float(b1 - b2), break_log10_f=float(brk),
                slope_low=float(s_lo), slope_high=float(s_hi), broken=broken, n_noncal_peaks=int(len(peaks)),
                peak_periods_h=peak_periods_h, fit_freq_decades=float(xb.max() - xb.min()) if nb else 0.0, n_fit_bins=nb,
                verdict=("BROKEN_SCALE" if broken else "SINGLE_POWER_LAW") + ("+PEAKS" if len(peaks) else ""))
