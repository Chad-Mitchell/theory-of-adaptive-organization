#!/usr/bin/env python3
"""REGIME-C-GAUSSIAN-PREMISE check 2 (pick 18). Many independent modes X_i = sqrt(lam_i) Z_i, lam_i = i^-beta, all of
one unit-variance shape Z. Minimise w*sum D_i + kappa*sum R_i (kappa per nat). Mode i sits where |R_Z'(d_i)| = s*lam_i,
s = w/kappa, so its rate is G(s*lam_i), G(u) = R_Z at slope u (from check 1, rd_*.json). Total bits B(s) = sum_i G(s lam_i).
Claim checked: B(s) ~ s^(1/beta) for every shape (same exponent as Gaussian, different constant), and the
represented-mode count n*(s) = #{i: s lam_i > u*} with u* = 1/(2 v*) (v* = optimal sub-Gaussian variance proxy).
Also checks G(u) <= u (convexity bound). Writes modesum.json."""
import json, numpy as np
H = {"gauss": None, "uniform": None, "laplace": None, "bern02": -(0.2*np.log(0.2)+0.8*np.log(0.8))}
DKL = {"gauss": 0.0, "uniform": 0.5*np.log(np.pi*np.e/6), "laplace": 0.5*np.log(2*np.pi*np.e) - (1+np.log(2**0.5)), "bern02": None}
def table(name):
    r = sorted(json.load(open(f"rd_{name}.json"))["rows"], key=lambda r: r["u"])
    u = np.array([x["u"] for x in r]); G = np.array([0.0 if x["zero_rate_cmax"] <= 1 + 1e-9 else x["R_up"] for x in r])
    return u, G, r
def Gfun(name, tail="zero"):
    u0, G0, _ = table(name); umax = u0[-1]
    def G(u):
        u = np.asarray(u, float); g = np.interp(np.log(u), np.log(u0), G0)
        hi = u > umax
        g[hi] = H[name] if H[name] is not None else 0.5*np.log(2*u[hi]) - DKL[name]
        lo = u < u0[0]
        g[lo] = 0.0 if tail == "zero" else u[lo]*G0[0]/u0[0]
        return np.maximum(g, 0)
    return G
if __name__ == "__main__":
    res = {"bound_G_le_u": {}, "join_at_umax": {}, "fits": {}}
    for n in H:
        u0, G0, r = table(n)
        res["bound_G_le_u"][n] = float(np.max(G0 - u0))
        if H[n] is None: res["join_at_umax"][n] = float(G0[-1] - (0.5*np.log(2*u0[-1]) - DKL[n]))
        else: res["join_at_umax"][n] = float(G0[-1] - H[n])
        zr = [x["u"] for x in r if x["zero_rate_cmax"] <= 1 + 1e-9]
        res.setdefault("u_star_numeric", {})[n] = max(zr) if zr else None
    N = 2_000_000; i = np.arange(1, N + 1, dtype=float)
    for beta in (0.6, 0.9, 1.5, 2.0):
        lam = i**-beta; s = 0.5*np.geomspace(1e2, 1e4, 9)**beta      # Gaussian n* from 1e2 to 1e4
        for n in H:
            for tail in ("zero", "linear"):
                G = Gfun(n, tail); B = np.array([G(sv*lam).sum() for sv in s])
                sl = np.polyfit(np.log(s), np.log(B), 1)[0]
                loc = np.diff(np.log(B))/np.diff(np.log(s))
                res["fits"][f"{n}|beta={beta}|tail={tail}"] = {"fit": round(float(sl), 4), "local_last": round(float(loc[-1]), 4),
                                                              "theory": round(1/beta, 4), "B_last_nats": float(B[-1])}
    print(json.dumps(res, indent=1)); json.dump(res, open("modesum.json", "w"), indent=1)
