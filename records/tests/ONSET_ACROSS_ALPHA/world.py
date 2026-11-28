"""ONSET-ACROSS-ALPHA-SIM world + learners (pick 32). Fresh code; imports nothing from earlier GTAO simulators.
No expected-cost formula appears here. Trackers see only their own exact reads and realized payoffs.
Drift: discrete fBm with Var(x[t+tau]-x[t]) = q * tau^(alpha-1) (H = (alpha-1)/2), by Davies-Harte circulant embedding.
Tech R (reset reads): a read costs C and returns the current value exactly; estimate held until the next read.
Policy = integer read interval T, random phase. Learner = selection on realized cost over a training path
(every T on a grid lives through the same realized training path; the realized cheapest is kept).
"""
import numpy as np

def fgn(rng, L, H, n=1):
    k = np.arange(L + 1, dtype=float)
    g = 0.5 * (np.abs(k + 1) ** (2 * H) - 2 * k ** (2 * H) + np.abs(k - 1) ** (2 * H))
    c = np.concatenate([g, g[-2:0:-1]])          # length 2L
    lam = np.fft.rfft(c).real
    lam = np.clip(lam, 0, None)                  # circulant embedding is PSD for fGn; clip rounding
    m = c.shape[0]
    out = []
    for _ in range(n):
        z = rng.standard_normal(m) + 1j * rng.standard_normal(m)
        w = np.fft.fft(np.sqrt(np.concatenate([lam, lam[-2:0:-1]]) / m) * z)
        out.append(w.real[:L])
    return np.array(out)

def fbm(rng, L, alpha, q=1.0, n=1):
    return np.sqrt(q) * np.cumsum(fgn(rng, L, (alpha - 1) / 2, n), axis=1)

def reset_err(x, T, phase):
    """Reset-read errors on the window starting at the first read (phase); returns (e vector, reads per step)."""
    m = (x.shape[0] - phase) // T
    seg = x[phase:phase + m * T].reshape(m, T)
    return (seg - seg[:, :1]).ravel(), 1.0 / T

TGRID = np.unique(np.round(np.exp(np.linspace(0, np.log(600), 90))).astype(int))

def mse_curve(x, rng):
    """realized mean squared error for every T in TGRID on path x (random phase per T)"""
    return np.array([np.mean(reset_err(x, int(T), int(rng.integers(T)))[0] ** 2) for T in TGRID])

def learn(mse, C, W):
    """selection on realized cost C/T + W*mse over the grid; returns chosen T"""
    return int(TGRID[np.argmin(C / TGRID + W * mse)])
