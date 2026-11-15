"""Referee numerics by deterministic quadrature (no Monte Carlo), independent of the PR #25 code.
(a) Exact stationary MSE of the Wonham filter, symmetric two-state world, closed form MSE/mu^2 = 2K0(k)/(K0(k)+K1(k)),
    k = lam*N/mu^2 (C&M units: k = theta/(2 tau)); checked against direct quadrature of the innovations-form density
    p(L) ∝ cosh^2(L/2) exp(-k cosh L); elasticity eta = dlnMSE/dlnk; Kalman MSE at the same spectrum.
(b) Mean adaptation time after a switch = mean first passage of L (posterior log-odds) from its quasi-stationary law
    under y=+1 to L=0 under y=-1 (no further switch), for the exact Wonham filter and for C&M eq.(20) as printed (Ito).
    1-D diffusion, generator b(L) d/dL + (sigma^2/2) d2/dL2, sigma^2 = 4/theta; theta = 1.
"""
import numpy as np, json
from scipy.special import k0e, k1e
from scipy.integrate import cumulative_trapezoid as ctz

def mse_closed(k):
    return 2*k0e(k)/(k0e(k)+k1e(k))   # exponential scaling cancels

def mse_quad(k):
    Lg = np.linspace(-60, 60, 400001)
    w = np.cosh(Lg/2)**2*np.exp(-k*np.cosh(Lg) + 0.0)
    # rescale to avoid overflow: use log form
    logw = 2*np.log(np.cosh(Lg/2)) - k*np.cosh(Lg)
    w = np.exp(logw - logw.max())
    return np.trapezoid(w/np.cosh(Lg/2)**2, Lg)/np.trapezoid(w, Lg)

def kalman(k):  # C&M units theta=1, tau = 1/(2k): P = theta(-1/tau + sqrt(1/tau^2 + 2/(tau theta)))
    tau = 1/(2*k); return -1/tau + np.sqrt(1/tau**2 + 2/tau)

out = {"mse": []}
for k in [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 9e-4, 3e-4, 2.5e-4, 1e-4, 1.1e-4, 1e-5, 1.7e-6, 1e-8]:
    h = 1e-4
    eta = (np.log(mse_closed(k*(1+h))) - np.log(mse_closed(k*(1-h))))/(np.log(1+h)-np.log(1-h))
    etak = (np.log(kalman(k*(1+h))) - np.log(kalman(k*(1-h))))/(np.log(1+h)-np.log(1-h))
    row = {"kappa": k, "mse_closed": mse_closed(k), "mse_quad": mse_quad(k) if k >= 1e-5 else None,
           "lead_2k_ln(2/k)": 2*k*np.log(2/k), "2k(ln(2/k)-gamma)": 2*k*(np.log(2/k)-np.euler_gamma),
           "eta_bayes": eta, "eta_kalman": etak, "mse_kalman": kalman(k)}
    out["mse"].append(row)

def mfpt(Psi_minus, Psi_plus, Lmax, n=600001, Lmin=-20.0):
    """mean first passage 0 <- L0 for the diffusion with scale exponent Psi_minus (= int 2b/sigma^2, analytic),
    L0 ~ quasi-stationary law exp(Psi_plus) of the pre-switch diffusion. sigma^2 = 4/theta, theta = 1."""
    s2 = 4.0
    L = np.linspace(Lmin, Lmax, n)
    lp = Psi_plus(L); p0 = np.exp(lp - lp.max()); p0 /= np.trapezoid(p0, L)
    pos = L >= 0
    Lp = L[pos]
    psi = Psi_minus(Lp) - Psi_minus(np.array([0.0]))[0]
    # T(x0) = int_0^x0 dy e^{-psi(y)} int_y^inf (2/s2) e^{psi(z)} dz ; compute inner via log-sum to avoid overflow
    # inner(y) = (2/s2) int_y^Lmax e^{psi(z)-psi(y)} dz by stable backward recursion (factor e^{dpsi} per step ~ 1)
    dL = Lp[1]-Lp[0]; d = np.exp(psi[1:] - psi[:-1])
    inner = np.zeros_like(Lp)
    acc = 0.0
    for i in range(len(Lp)-2, -1, -1):
        acc = d[i]*acc + 0.5*dL*(1.0 + d[i])
        inner[i] = acc
    inner *= 2/s2
    T = ctz(inner, Lp, initial=0.0)
    return float(np.trapezoid(p0[pos]*T, Lp)), float(np.trapezoid(p0[pos], Lp))

out["adapt"] = []
for tau in [10, 30, 100, 300, 1000, 3000, 1e4, 1e5, 1e6, 1e8]:
    th = 1.0
    k = th/(2*tau)
    lc = lambda L: 2*np.log(np.cosh(L/2))      # int tanh(L/2) dL
    ex_m = lambda L: -L - k*np.cosh(L)          # 2b/s2 = -1 - k sinh L
    ex_p = lambda L: L - k*np.cosh(L)           # 2b/s2 = +1 - k sinh L
    # printed eq.(20) as Ito mapped to L: drift = 2y/theta - sinh L/tau + 2 tanh(L/2)/theta (R4/R5)
    pr_m = lambda L: -L - k*np.cosh(L) + lc(L)
    pr_p = lambda L: L - k*np.cosh(L) + lc(L)
    Lmax = np.log(4*tau/th) + 12
    tex, mass = mfpt(ex_m, ex_p, Lmax)
    tpr, mass_pr = mfpt(pr_m, pr_p, Lmax + 1)
    out["adapt"].append({"tau": tau, "kappa": th/(2*tau), "tA_exact": tex, "P(L0>0)": mass,
        "C_fit=ln(4tau/theta)-2tA/theta": np.log(4*tau/th) - 2*tex/th,
        "tA_printed_eq20_Ito": tpr, "CM_eq36_(theta/4)ln^2(tau/theta)": th/4*np.log(tau/th)**2,
        "CM_A3_with_ln_term": th/4*(np.log(th/tau)**2 + (2*np.euler_gamma - 2*np.log(2) + 1)*np.log(th/tau))})
# analytic constant (deterministic descent, start law e^L ~ Exp, see REPORT): C0 = gamma + e*E1(1)
from scipy.special import exp1
out["C0_deterministic_descent"] = float(np.euler_gamma + np.e*exp1(1.0))
a = out["adapt"]
lt = np.log([r["tau"] for r in a]); te = np.array([r["tA_exact"] for r in a])
sel = (np.array([r["tau"] for r in a]) >= 300) & (np.array([r["tau"] for r in a]) <= 1e4)
out["slope_exact_vs_lntau_300_1e4"] = float(np.polyfit(lt[sel], te[sel], 1)[0])
q = np.polyfit(lt[:7], te[:7], 2); out["quad_fit_exact_10_1e4"] = list(map(float, q))
tp = np.array([r["tA_printed_eq20_Ito"] for r in a]); out["quad_fit_printed_10_1e4"] = list(map(float, np.polyfit(lt[:7], tp[:7], 2)))
json.dump(out, open("out_quad_ref.json", "w"), indent=1)
for r in out["mse"]: print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})
for r in a: print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
print({k: out[k] for k in ["C0_deterministic_descent", "slope_exact_vs_lntau_300_1e4", "quad_fit_exact_10_1e4", "quad_fit_printed_10_1e4"]})
