"""R4: what the fixed-world theory says about antifragility (theory/ROBUSTNESS.md §6).

World: one OU mode with variance a (the 'volatility' scale) and rate lam, read through white noise
of density N; design K in {0, 1}; K = 1 is a first-order store x_hat' = b (y - x_hat), b in [bmin, bmax],
cost h + w Var(e). K = 0 (blind) costs w a. Ruin is absent (slack)."""
import math
import numpy as np
from scipy.linalg import solve_continuous_lyapunov

LAM, N, H, W = 1.0, 0.5, 0.3, 1.0
BS = np.exp(np.linspace(math.log(0.01), math.log(100), 400))


def err_var(a, b):
    A = np.array([[-LAM, 0.0], [b, -b]])
    Q = np.array([[2 * LAM * a, 0.0], [0.0, b * b * N]])
    P = solve_continuous_lyapunov(A, -Q)
    return P[0, 0] - 2 * P[0, 1] + P[1, 1]


def J_design(a, b):
    return H + W * err_var(a, b) if b is not None else W * a


def J_star(a):
    return min(W * a, min(J_design(a, b) for b in BS))


def run():
    res = {}
    # affine in a at a fixed design
    b = 2.0
    v = [err_var(a, b) for a in (0.0, 1.0, 2.0)]
    res["affine_in_a_at_fixed_design"] = abs(v[2] - 2 * v[1] + v[0]) < 1e-10
    As = np.linspace(0.0, 6.0, 121)
    Js = np.array([J_star(a) for a in As])
    d2 = Js[2:] - 2 * Js[1:-1] + Js[:-2]
    res["Jstar_nondecreasing"] = bool(np.all(np.diff(Js) >= -1e-12))
    res["Jstar_concave_max_second_diff"] = float(d2.max())
    gap = W * As - Js
    res["gap_vs_blind_nonneg"] = bool(np.all(gap >= -1e-12))
    res["gap_nondecreasing"] = bool(np.all(np.diff(gap) >= -1e-12))
    res["gap_convex_min_second_diff"] = float((gap[2:] - 2 * gap[1:-1] + gap[:-2]).min())
    # volatility of volatility: two regimes a1, a2 (half the time each), mean a_bar
    a1, a2 = 0.5, 4.5; ab = (a1 + a2) / 2
    redesign = 0.5 * J_star(a1) + 0.5 * J_star(a2)
    fixed = min(min(0.5 * J_design(a1, b) + 0.5 * J_design(a2, b) for b in BS), W * ab)
    res["regimes_Jstar(abar)"] = round(J_star(ab), 6)
    res["regimes_fixed_design_cost"] = round(fixed, 6)
    res["regimes_redesign_cost"] = round(redesign, 6)
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k, "=", v)
