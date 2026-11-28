"""C1 (own code, pick 37): reset-read (hold-last-value) interval optimum under power loss |e|^p, Monte Carlo fBm.
Cost rate J(T) = c/T + w * (1/T) * int_0^T E|X(t)-X(0)|^p dt, drift level q scales X by sqrt(q).
Claim checked: read rate 1/T* has elasticities a_p = 2/(2+p(alpha-1)) in w/c and b_p = p/(2+p(alpha-1)) in q
(p = 2 gives 1/alpha, 1/alpha, THEORY 2.2)."""
import numpy as np, json
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(37001)

def fgn(n, H, rng):
    # Davies-Harte circulant embedding of fractional Gaussian noise (unit variance increments)
    k = np.arange(n + 1)
    g = 0.5 * ((k + 1.0) ** (2 * H) - 2 * k ** (2.0 * H) + np.abs(k - 1.0) ** (2 * H))
    r = np.concatenate([g, g[-2:0:-1]])
    lam = np.fft.fft(r).real
    lam[lam < 0] = 0
    m = len(r)
    z = rng.normal(size=m) + 1j * rng.normal(size=m)
    w = np.fft.fft(np.sqrt(lam / (2 * m)) * z)
    return w.real[:n]

def moments(alpha, p_list, maxlag=4096, reps=60, n=2 ** 16):
    H = (alpha - 1) / 2
    lags = np.unique(np.round(np.logspace(0, np.log10(maxlag), 120)).astype(int))
    acc = {p: np.zeros(len(lags)) for p in p_list}
    for _ in range(reps):
        x = np.cumsum(fgn(n, H, rng))
        for i, L in enumerate(lags):
            d = np.abs(x[L:] - x[:-L])
            for p in p_list:
                acc[p][i] += np.mean(d ** p)
    return lags, {p: acc[p] / reps for p in p_list}

def topt(lags, m, w, c=1.0):
    # cumulative mean loss via log-log interpolation of m(t), integrate on fine grid
    lt = np.log(lags); lm = np.log(m)
    tt = np.logspace(-3, np.log10(lags[-1]), 4000)
    mm = np.exp(np.interp(np.log(np.maximum(tt, 1)), lt, lm))
    # below lag 1 extrapolate with exact self-similarity m(t) = m(1) t^{pH}
    return mm, tt

res = {}
for alpha in (1.5, 2.0, 2.5):
    ps = (0.5, 1.0, 2.0, 4.0)
    lags, M = moments(alpha, ps)
    H = (alpha - 1) / 2
    for p in ps:
        m = M[p]
        # empirical self-similarity exponent of the moment (should be p*H)
        slope_m = np.polyfit(np.log(lags[lags >= 4]), np.log(m[lags >= 4]), 1)[0]
        cum_t = np.concatenate([[0.0], lags.astype(float)])
        # cumulative integral of m on [0, T] by trapezoid over lags, m(0)=0
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (np.concatenate([[0.0], m[:-1]]) + m) * np.diff(cum_t))])
        def J(lT, w, q):
            T = np.exp(lT)
            I = np.interp(T, cum_t, cum) * q ** (p / 2)
            return 1.0 / T + w * I / T
        def Tstar(w, q):
            r = minimize_scalar(J, bounds=(np.log(3), np.log(lags[-1] * 0.9)), args=(w, q), method="bounded",
                                options={"xatol": 1e-6})
            return np.exp(r.x)
        # pick w0 so that T* ~ 60 at q=1
        T0 = 60.0
        w0 = 1.0 / (np.interp(T0, cum_t, cum) * (pH := 0) + 1e-12) if False else None
        # find w0 by bisection in log space
        lo, hi = -40, 40
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if Tstar(np.exp(mid), 1.0) > T0: lo = mid
            else: hi = mid
        w0 = np.exp(0.5 * (lo + hi))
        fac = np.exp(np.linspace(-1.2, 1.2, 9))
        rw = [1 / Tstar(w0 * f, 1.0) for f in fac]
        rq = [1 / Tstar(w0, f) for f in fac]
        a_hat = np.polyfit(np.log(fac), np.log(rw), 1)[0]
        b_hat = np.polyfit(np.log(fac), np.log(rq), 1)[0]
        a_th = 2 / (2 + p * (alpha - 1)); b_th = p / (2 + p * (alpha - 1))
        res[f"alpha={alpha},p={p}"] = {"moment_slope": round(slope_m, 4), "moment_slope_theory": p * H,
                                       "a_hat": round(a_hat, 4), "a_theory": round(a_th, 4),
                                       "b_hat": round(b_hat, 4), "b_theory": round(b_th, 4),
                                       "onset_sep_hat": round(-(1 - b_hat) / (1 - a_hat), 3),
                                       "onset_sep_theory": round(-(1 - b_th) / (1 - a_th), 3),
                                       "quadratic_rival_a=b": round(1 / alpha, 4)}
        print(alpha, p, res[f"alpha={alpha},p={p}"], flush=True)
json.dump(res, open("c1_resetread_powerloss.json", "w"), indent=1)
