"""Numerical check of the cross-field map (theory/CROSS_FIELD_MAP_2026-11-21.md, section 2).

Model (Chow 1974 form): K levels; level k has capacity s_k and access time t_k.
World law  : fraction of references missing a store of capacity s, m(s) = (s/s0)^(-theta), m(s_0)=1.
Technology : cost per unit capacity c(t) = a * t^(-gamma).
J = T + lam * C,  T = sum_k m(s_{k-1}) t_k,  C = sum_k a t_k^(-gamma) s_k.
Boundary: s_0 = 1 (the reference unit), s_K = S fixed (the backing store holds everything); all t_k free.
Prediction (closed form, derived in the note): interior ratios converge to
   ln r_s = -(1+gamma) ln(gamma*theta) / (1 - gamma*theta)
   ln r_t = -(1+theta) ln(gamma*theta) / (1 - gamma*theta)
   adjacent cost ratio C_{k+1}/C_k = delay ratio D_{k+1}/D_k = 1/(gamma*theta)  (exact for all finite K, S)
   delay share = gamma * cost share (Chow 1974 Eq. 36 / Welch 1978 form: D_k / (lam C_k) = gamma)
"""
import numpy as np
from scipy.optimize import minimize

def J(x, K, theta, gamma, lam, a, S):
    if not np.all(np.isfinite(x)) or np.max(np.abs(x)) > 600:
        return 1e300, None, None, None, None, None
    ls = np.concatenate([[0.0], x[:K-1], [np.log(S)]])   # log s_0..s_K
    lt = x[K-1:]                                          # log t_1..t_K
    m = np.exp(-theta*ls[:-1])
    T = np.sum(m*np.exp(lt))
    C = np.sum(a*np.exp(-gamma*lt)*np.exp(ls[1:]))
    return T + lam*C, T, C, ls, lt, m

from scipy.special import logsumexp
def logJ(x, K, theta, gamma, lam, a, S):
    ls = np.concatenate([[0.0], x[:K-1], [np.log(S)]])
    lt = x[K-1:]
    terms = np.concatenate([lt - theta*ls[:-1], np.log(lam*a) - gamma*lt + ls[1:]])
    return logsumexp(terms)

def solve(K, theta, gamma, lam=1.0, a=1.0, S=1e12):
    # start from an even log ladder (NOT the predicted ratios) plus jitter; t-scale from 1-level balance
    lt0 = np.log(gamma*lam*a)/(1+gamma)
    x0 = np.concatenate([np.linspace(0, np.log(S), K+1)[1:-1], lt0 + np.linspace(0, np.log(S)*0.5, K)])
    best = None
    with np.errstate(all="ignore"):
      for jitter in range(8):
        rng = np.random.default_rng(jitter)
        # J is a posynomial, so log J is convex in (log s, log t) (geometric program, as in Chow 1974):
        # minimize log J (well conditioned); any stationary point is the global minimum.
        r = minimize(lambda x: logJ(x, K, theta, gamma, lam, a, S), x0 + rng.normal(0, 0.3, x0.size),
                     method="BFGS", options={"gtol": 1e-13, "maxiter": 100000})
        if best is None or r.fun < best.fun:
            best = r
    return best

def predicted(theta, gamma):
    g = gamma*theta
    lrs = -(1+gamma)*np.log(g)/(1-g)
    lrt = -(1+theta)*np.log(g)/(1-g)
    return lrs, lrt, 1/g

if __name__ == "__main__":
    print("theta gamma K | mid-level ln r_s (num, pred) | ln r_t (num, pred) | cost ratio (num, pred) | D/(lam C) (num, pred)")
    worst = 0.0
    for theta, gamma in [(0.5, 0.5), (0.3, 1.0), (0.7, 0.8), (0.5, 1.5), (0.4, 0.4)]:
        for K in (9,):
            # choose S = exp(K * ln r_s) so every level sits at the fixed point (no boundary mismatch)
            lrs, lrt, q = predicted(theta, gamma)
            S = float(np.exp(lrs*K))
            r = solve(K, theta, gamma, S=S)
            _, T, C, ls, lt, m = J(r.x, K, theta, gamma, 1.0, 1.0, S)
            D = m*np.exp(lt); Ck = np.exp(-gamma*lt)*np.exp(ls[1:])
            k = K//2
            num = (ls[k+1]-ls[k], lt[k]-lt[k-1], Ck[k]/Ck[k-1], D[k]/Ck[k])
            pred = (lrs, lrt, q, gamma)
            rel = max(abs(n-p)/abs(p) for n, p in zip(num, pred))
            if q <= 4.0 + 1e-9:   # well-conditioned: lowest-level terms are not swamped (see note section 2.4)
                worst = max(worst, rel)
            else:
                print("      (diagnostic only: q = 1/(theta*gamma) > 4, lower levels carry < q^-K of J and BFGS on log J leaves them loose; the exact FOC check is Part 2)")
            print(f"{theta} {gamma} {K:2d} | {num[0]:.4f} {pred[0]:.4f} | {num[1]:.4f} {pred[1]:.4f} | {num[2]:.4f} {pred[2]:.4f} | {num[3]:.4f} {pred[3]:.4f} | relerr {rel:.2e}")
            welch = np.max(np.abs(D/Ck - gamma))
            print(f"      Welch identity D_k/(lam C_k)=gamma at every level: max dev {welch:.2e}")
    print("WORST mid-level relative error (well-conditioned cases)", f"{worst:.2e}")
    assert worst < 1e-3, worst

# ---- Part 2: exact first-order-condition recurrence (no optimizer; GP convexity makes any FOC point the global min)
# FOCs: d/d ln t_k : D_k = gamma*lam*C_k ;  d/d ln s_k : lam*C_k = theta*D_{k+1}.
# In log ratios x_k = ln(s_k/s_{k-1}), y_k = ln(t_{k+1}/t_k):  y_k = ln q + theta*x_k ;  x_{k+1} = ln q + gamma*y_k,
# so x_{k+1} - x* = (theta*gamma)(x_k - x*): boundary deviations decay by the factor theta*gamma per level.
def recurrence_check():
    print("\nPart 2: FOC recurrence from a boundary value 2x off the fixed point")
    for theta, gamma in [(0.5, 0.5), (0.3, 1.0), (0.4, 0.4), (0.7, 0.8), (0.6, 1.2)]:
        lrs, lrt, q = predicted(theta, gamma)
        x = 2*lrs; devs = []
        for k in range(8):
            y = np.log(q) + theta*x
            devs.append(abs(x-lrs)/lrs)
            x = np.log(q) + gamma*y
        print(f"theta={theta} gamma={gamma} theta*gamma={theta*gamma:.2f}  rel dev of ln r_s by level: " + " ".join(f"{d:.3f}" for d in devs))
        assert abs(devs[-1] - (theta*gamma)**7) < 1e-9
    print("recurrence contraction verified: deviation_k = (theta*gamma)^k * deviation_0")

# ---- Part 3: direct convex GP solve with mismatched S != exp(K * ln r_s), plus theta*gamma = 1 and > 1
def finite_k_boundary_check():
    print("\nPart 3: direct GP solve with mismatched boundary S (one-sided decay and exact C_{k+1}/C_k = q)")
    K = 6
    worst_gp = 0.0
    for theta, gamma in [(0.5, 0.5), (0.7, 0.8), (1.0, 1.0), (1.2, 1.2)]:
        g = theta * gamma
        if abs(g - 1.0) > 1e-9:
            lrs, _, q = predicted(theta, gamma)
            S = float(1e2 * np.exp(lrs * K))
            x1_diff = (1.0 - g) / (1.0 - g**K) * (np.log(S) - K * lrs)
            xs_exact = lrs + x1_diff * (g ** np.arange(K))
        else:
            q = 1.0
            S = float(np.exp(10.0))
            xs_exact = np.full(K, np.log(S) / K)
        r = solve(K, theta, gamma, S=S)
        _, _, _, ls, lt, _ = J(r.x, K, theta, gamma, 1.0, 1.0, S)
        xs_num = np.diff(ls)
        Ck = np.exp(-gamma*lt) * np.exp(ls[1:])
        c_ratios = Ck[1:] / Ck[:-1]
        x_err = float(np.max(np.abs(xs_num - xs_exact)))
        q_err = float(np.max(np.abs(c_ratios - q) / q))
        worst_gp = max(worst_gp, x_err, q_err)
        print(f"theta={theta} gamma={gamma} theta*gamma={g:.2f} | max|x_num-x_exact|={x_err:.2e} | max|C_ratio/q - 1|={q_err:.2e}")
        assert x_err < 1e-3 and q_err < 1e-3
    print(f"WORST mismatched-S GP error {worst_gp:.2e}")

if __name__ == "__main__":
    recurrence_check()
    finite_k_boundary_check()
    print("RESULT: PASS")
