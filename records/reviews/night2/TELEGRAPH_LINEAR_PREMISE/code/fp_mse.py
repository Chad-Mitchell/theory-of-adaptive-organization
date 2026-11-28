"""TELEGRAPH-LINEAR-PREMISE: stationary MSE of the exact (Wonham) filter by solving the stationary Fokker-Planck equations
(method B, deterministic), vs the linear Kalman filter on the same spectrum (analytic). In-model only. C&M units as adapt_mc.py.
Joint density p_+(L) (true y = +1), p_-(L) = p_+(-L). Generator for y = +1: drift A(L) = 2/theta - sinh(L)/tau,
diffusion D = 2/theta (dL noise (2/sqrt(theta)) dW), switching r = 1/(2 tau).
0 = -d/dL[A p_+] + D p_+'' + r (p_- - p_+). Finite volume, Scharfetter-Gummel flux, zero-flux walls.
MSE_B = E[(y - tanh(L/2))^2]; kappa = lambda N / mu^2 = theta/(2 tau)."""
import numpy as np, json, scipy.sparse as sps, scipy.sparse.linalg as spl
theta = 1.0
def solve(tau, NL=6000, pad=8.0):
    Lmax = np.log(4 * tau / theta) + pad
    edges = np.linspace(-Lmax, Lmax, NL + 1); h = edges[1] - edges[0]; Lc = 0.5 * (edges[1:] + edges[:-1])
    D = 2 / theta; r = 1 / (2 * tau)
    def B(z):
        z = np.asarray(z, float); out = np.empty_like(z); small = np.abs(z) < 1e-8
        out[small] = 1 - z[small] / 2; zz = z[~small]; out[~small] = zz / np.expm1(zz); return out
    def op(sign):
        # Scharfetter-Gummel (exponentially fitted) flux at interior edges, stable for any cell Peclet number:
        # F_{j+1/2} = (D/h) [B(-Pe) p_j - B(Pe) p_{j+1}],  Pe = A_e h / D
        Ae = sign * 2 / theta - np.sinh(edges[1:-1]) / tau
        Pe = Ae * h / D
        cj = D / h * B(-Pe); cj1 = -D / h * B(Pe)
        j = np.arange(NL - 1)
        rows = np.concatenate([j, j, j + 1, j + 1]); cols = np.concatenate([j, j + 1, j, j + 1])
        vals = np.concatenate([-cj / h, -cj1 / h, cj / h, cj1 / h])
        return sps.csr_matrix((vals, (rows, cols)), shape=(NL, NL))
    Mp, Mm = op(1), op(-1)
    I = sps.identity(NL, format="csr")
    M = sps.bmat([[Mp - r * I, r * I], [r * I, Mm - r * I]], format="csr")
    # replace one equation by normalisation
    M = M.tolil(); M[0, :] = np.ones(2 * NL) * h; M = M.tocsr()
    rhs = np.zeros(2 * NL); rhs[0] = 1.0
    p = spl.spsolve(M, rhs); pp, pm = p[:NL], p[NL:]
    xhat = np.tanh(Lc / 2)
    mse = float(h * (np.sum(pp * (1 - xhat) ** 2) + np.sum(pm * (-1 - xhat) ** 2)))
    sym = float(np.max(np.abs(pp - pm[::-1])) / np.max(pp))
    neg = float(min(p.min(), 0) / p.max())
    return mse, sym, neg, float(h * pp.sum())

def kalman(tau):
    return theta * (-1 / tau + np.sqrt(1 / tau ** 2 + 2 / (tau * theta)))

out = {"rows": []}
taus = np.geomspace(30, 3e5, 23)
for tau in taus:
    m, sym, neg, massp = solve(tau)
    m2, *_ = solve(tau, NL=12000)
    kap = theta / (2 * tau)
    out["rows"].append({"tau": float(tau), "kappa": kap, "mse_bayes": m, "mse_bayes_2xgrid": m2, "mse_kalman": float(kalman(tau)),
                        "lead_2k_ln(2/k)": float(2 * kap * np.log(2 / kap)), "asym": sym, "minneg": neg, "mass_plus": massp})
    print(f"tau {tau:9.1f} kappa {kap:.2e} B {m:.5e} (2x {m2:.5e}) K {kalman(tau):.5e} lead {2*kap*np.log(2/kap):.5e}", flush=True)
k = np.array([r["kappa"] for r in out["rows"]]); mb = np.array([r["mse_bayes_2xgrid"] for r in out["rows"]])
mk = np.array([r["mse_kalman"] for r in out["rows"]])
lk = np.log(k)
etaB = np.gradient(np.log(mb), lk); etaK = np.gradient(np.log(mk), lk)
for r, eb, ek in zip(out["rows"], etaB, etaK):
    r["eta_bayes"] = float(eb); r["eta_kalman"] = float(ek)
print(json.dumps([(round(r["kappa"], 7), round(r["eta_bayes"], 3), round(r["eta_kalman"], 3)) for r in out["rows"]]))
json.dump(out, open("../out_fp.json", "w"), indent=1)
