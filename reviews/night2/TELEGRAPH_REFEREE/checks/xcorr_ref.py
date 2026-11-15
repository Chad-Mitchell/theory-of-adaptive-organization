"""C&M's own adaptation-time definition (eq. 27-28): t_A = argmax_t C(t), C(t) = <y(t0) x(t0+t)>, stationary.
Exact filter (discrete HMM forward filter, log-odds) and C&M eq.(20) as printed (Ito; integrated exactly in L-form
with the extra drift 2 tanh(L/2)/theta, Euler in L). theta = 1, dt = 0.01, switching rate 1/(2 tau).
Run length 4000 tau per tau (8 paths x 500 tau), seed 7400+. C(t) by FFT cross-correlation; argmax on a fine lag grid
smoothed by a 5-point moving average; SE by the spread over the 8 paths."""
import numpy as np, json, numba
@numba.njit(cache=True)
def run(tau, th, dt, n, seed):
    np.random.seed(seed)
    lam = 1/(2*tau); k = 0.5*(1-np.exp(-2*lam*dt)); lk = np.log(k); l1k = np.log(1-k)
    y = 1.0; L = 0.0; Lp = 0.0
    ys = np.empty(n); xe = np.empty(n); xp = np.empty(n)
    sq = np.sqrt(th*dt)
    for i in range(n):
        if np.random.random() < k: y = -y
        ds = y*dt + sq*np.random.standard_normal()
        a = np.logaddexp(l1k + L, lk); b = np.logaddexp(lk + L, l1k); L = a - b + 2*ds/th
        # printed eq. (20) read as Ito, mapped exactly to L: dL = (2/th) ds - sinh(L)/tau dt + 2 tanh(L/2)/th dt
        Lp = Lp + 2*ds/th - np.sinh(Lp)/tau*dt + 2*np.tanh(Lp/2)/th*dt
        if Lp > 60: Lp = 60.0
        if Lp < -60: Lp = -60.0
        ys[i] = y; xe[i] = np.tanh(L/2); xp[i] = np.tanh(Lp/2)
    return ys, xe, xp
def xcorr_argmax(y, x, dt, maxlag):
    n = len(y); m = int(maxlag/dt)
    f = np.fft.rfft(y - y.mean(), 2*n); g = np.fft.rfft(x - x.mean(), 2*n)
    c = np.fft.irfft(np.conj(f)*g)[:m]/n   # c[j] = <y(t) x(t+j dt)>
    cs = np.convolve(c, np.ones(5)/5, mode='same')
    return (np.argmax(cs[2:-2]) + 2)*dt
out = []
th, dt = 1.0, 0.01
for tau in [10, 30, 100, 300, 1000]:
    te, tp = [], []
    for p in range(8):
        n = int(500*tau/dt)
        ys, xe, xp = run(float(tau), th, dt, n, 7400 + p + int(tau))
        maxlag = min(40.0, 2*tau)
        te.append(xcorr_argmax(ys, xe, dt, maxlag)); tp.append(xcorr_argmax(ys, xp, dt, max(maxlag, 60.0) if tau >= 100 else maxlag))
    r = {"tau": tau, "tA_xcorr_exact_mean": float(np.mean(te)), "se_exact": float(np.std(te)/np.sqrt(8)),
         "tA_xcorr_printed_mean": float(np.mean(tp)), "se_printed": float(np.std(tp)/np.sqrt(8)),
         "fpt_quadrature_exact_(for_comparison)": None}
    print(r, flush=True); out.append(r)
lt = np.log([r["tau"] for r in out])
out.append({"fit_exact_quadratic_in_lntau": list(map(float, np.polyfit(lt, [r["tA_xcorr_exact_mean"] for r in out], 2))),
            "fit_printed_quadratic_in_lntau": list(map(float, np.polyfit(lt, [r["tA_xcorr_printed_mean"] for r in out[:len(lt)]], 2)))})
print(out[-1]); json.dump(out, open("out_xcorr_ref.json", "w"), indent=1)
