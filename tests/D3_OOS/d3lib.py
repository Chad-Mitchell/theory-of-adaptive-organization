"""D3-TWO-EXPONENT-OOS library (written before the lock; no real data of the new sample read when written).
Statistics per 'repo' (a set of event-day lists, one per file/article, each with >= 50 distinct event days):
  beta_orig  spectral_beta of binary daily series, band 1/730-0.5 c/d (MATCH1 aslib, unchanged)
  beta_shuf  same after permuting each file's inter-event gaps (first day kept), mean of 5 shuffles (= D3S 'renewal-implied beta')
  delta      beta_orig - beta_shuf
  a_need     MATCH1 need-odds exponent (Lmax 365), alive/dead split as in D3S (git only; for wiki all items are 'alive')
  M_raw      pooled corr of consecutive log gaps (D3S S3 'M_loggaps')
  M_w        pooled corr of consecutive log gaps after subtracting each file's mean log gap (primary discriminator)
  M_w_null   200 within-file gap shuffles -> null quantiles of M_w; exceed = M_w > null 97.5% quantile
"""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../MATCH1"))
from aslib import need_counts, fit, spectral_beta
FMIN, FMAX = 1/730, 0.5

def series(d, n):
    s = np.zeros(n); s[d] = 1; return s

def shuffle_gaps(d, rng):
    g = np.diff(d); rng.shuffle(g); return np.concatenate([[d[0]], d[0] + np.cumsum(g)])

def mw(files, demean=True):
    x = []; y = []
    for d in files:
        lg = np.log(np.diff(d).astype(float))
        if len(lg) < 3: continue
        if demean: lg = lg - lg.mean()
        x.append(lg[:-1]); y.append(lg[1:])
    x = np.concatenate(x); y = np.concatenate(y)
    return float(np.corrcoef(x, y)[0, 1])

def repo_stats(files, n, rng, a_need=None, nnull=200):
    files = [np.asarray(sorted(set(int(v) for v in d))) for d in files]
    files = [d for d in files if len(d) >= 50]
    if len(files) < 5: return None
    b0 = spectral_beta([series(d, n) for d in files], FMIN, FMAX)
    bs = [spectral_beta([series(shuffle_gaps(d, rng), n) for d in files], FMIN, FMAX) for _ in range(5)]
    m_w = mw(files); m_raw = mw(files, demean=False)
    null = np.array([mw([shuffle_gaps(d, rng) for d in files]) for _ in range(nnull)])
    q = np.quantile(null, [0.025, 0.5, 0.975])
    return dict(n_files=len(files), beta_orig=round(b0, 4), beta_shuf=round(float(np.mean(bs)), 4),
                beta_shuf_sd=round(float(np.std(bs)), 4), delta=round(b0 - float(np.mean(bs)), 4),
                a_need=None if a_need is None else round(a_need, 4),
                M_raw=round(m_raw, 4), M_w=round(m_w, 4), M_w_null_q=[round(float(v), 4) for v in q],
                M_w_exceed=bool(m_w > q[2]), M_w_p=round(float((1 + np.sum(null >= m_w)) / (nnull + 1)), 4))

def need_exponent(alive, dead, end):
    n1, d1 = need_counts(alive, 365, end=end); n2, d2 = need_counts(dead, 365, end=None)
    lag = np.arange(366)
    return fit(lag[1:], (n1 + n2)[1:], (d1 + d2)[1:])["exponent"]
