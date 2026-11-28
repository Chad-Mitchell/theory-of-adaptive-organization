"""Pre-lock power check on SYNTHETIC data only (no real data). Settings follow the referee's R6 check
(reviews/night2/SPECTRUM_MAP_REFEREE_checks/r6_d3s_power.py): renewal = iid discretized Weibull gaps; Cox = daily
edit prob min(1, r*exp(s*g_t)), g_t unit-variance 1/f^gamma Gaussian. Here F = 20 files/repo (fewer than R6's 40, conservative),
n = 5000 days, 20 synthetic repos per setting (the planned real n). Reports beta_orig, delta, M_w exceed rate, and the locked
decision rules applied to each synthetic batch. Also a 'lifecycle' renewal-with-trend control (rate decays with file age:
a Cox world with a deterministic trend) and a Hawkes-like self-exciting control."""
import json, numpy as np
from scipy.stats import wilcoxon, spearmanr
from d3lib import repo_stats
rng = np.random.default_rng(20261115); n = 5000; F = 20; R = 20
def powerlaw_gp(gamma):
    f = np.fft.rfftfreq(2*n); A = np.zeros_like(f); A[1:] = f[1:]**(-gamma/2)
    z = (rng.normal(size=f.size) + 1j*rng.normal(size=f.size))*A; x = np.fft.irfft(z)[:n]; return (x - x.mean())/x.std()
def gen(kind, par):
    files = []
    while len(files) < F:
        if kind == "renewal":
            k, scale = par; g = np.maximum(1, np.round(scale*rng.weibull(k, size=4000))).astype(int)
            d = np.cumsum(g) + rng.integers(0, 1000); d = d[d < n]
        elif kind == "renewal_het":  # file-specific gap scale (lognormal), iid gaps within a file
            k, scale = par; sc = scale*np.exp(rng.normal(0, 1)); g = np.maximum(1, np.round(sc*rng.weibull(k, size=4000))).astype(int)
            d = np.cumsum(g) + rng.integers(0, 1000); d = d[d < n]
        elif kind == "cox":
            gamma, s, r = par; p = np.minimum(1, r*np.exp(s*powerlaw_gp(gamma))); d = np.nonzero(rng.random(n) < p)[0]
        elif kind == "lifecycle":   # rate r0*(1+t/T)^-1 from a random birth day
            r0, T = par; b = rng.integers(0, 2500); t = np.arange(n) - b
            p = np.where(t >= 0, r0/(1 + np.maximum(t, 0)/T), 0); d = np.nonzero(rng.random(n) < p)[0]
        elif kind == "hawkes":      # discrete-time: p_t = mu + eta * sum_k exp(-(t-t_k)/tau)/tau, capped at 1
            mu, eta, tau = par; d = []; ex = 0.0
            for t in range(n):
                p = min(1.0, mu + eta*ex/tau)
                if rng.random() < p: d.append(t); ex += 1
                ex *= np.exp(-1/tau)
            d = np.array(d)
        if len(d) >= 50: files.append(d)
    return files
def decide(rows):
    ex = np.mean([r["M_w_exceed"] for r in rows]); md = float(np.median([r["delta"] for r in rows]))
    p = wilcoxon([r["delta"] for r in rows], alternative="greater").pvalue
    P3 = "RENEWAL REJECTED" if ex >= 0.5 else ("RENEWAL RETAINED" if ex <= 0.15 else "PARTIAL")
    P4 = "DELTA>0 DETECTED" if (p < 0.01 and md > 0.01) else "not detected"
    rho = spearmanr([r["beta_orig"] for r in rows], [r["beta_shuf"] for r in rows])[0]
    return dict(exceed_frac=round(float(ex), 3), median_delta=round(md, 4), wilcoxon_p=float(f"{p:.3g}"),
                median_beta=round(float(np.median([r["beta_orig"] for r in rows])), 3),
                median_M_w=round(float(np.median([r["M_w"] for r in rows])), 3),
                median_M_raw=round(float(np.median([r["M_raw"] for r in rows])), 3), spearman_orig_shuf=round(float(rho), 3), P3=P3, P4=P4)
settings = [("renewal_het", (0.4, 10)), ("renewal", (0.5, 20)), ("renewal", (0.35, 10)), ("renewal", (0.25, 5)),
            ("cox", (1.0, 1.0, 0.03)), ("cox", (1.0, 0.6, 0.04)), ("cox", (0.6, 1.5, 0.02)), ("cox", (0.4, 1.0, 0.03)),
            ("cox", (1.0, 0.3, 0.04)), ("lifecycle", (0.3, 200)), ("hawkes", (0.01, 0.5, 5))]
out = {}
for kind, par in settings:
    rows = [repo_stats(gen(kind, par), n, rng, nnull=200) for _ in range(R)]
    out[f"{kind}{par}"] = decide(rows); print(kind, par, out[f"{kind}{par}"], flush=True)
json.dump(out, open("power_check.json", "w"), indent=1)
