"""R2: model uncertainty and the reserve (theory/ROBUSTNESS.md §4).

R2-a  reserve-and-check design under an ambiguity set on the shock scale (sympy + numeric).
R2-b  plug-in versus predictive buffer when sigma is estimated from n observations (exact t distribution).
R2-c  plug-in versus predictive copy count when the copy failure rate p is estimated (Beta posterior);
      PRIOR ART: the state-of-knowledge correlation (Apostolakis & Kaplan 1981).
R2-d  tail ambiguity: Student-t at fixed variance, and the moment-only (Cantelli) worst case.
"""
import math
import numpy as np
import sympy as sp
from scipy import stats
from scipy.optimize import minimize_scalar


# ---------- R2-a ----------
def design_a(c, w, sig_hat, r, z, u, worst_case_objective=False):
    """min_tau c/tau + w*sig_obj^2*tau/2 + r*B, B = z*sig_max*sqrt(tau) (constraint binds since r > 0)."""
    smax = sig_hat * (1 + u)
    sobj = smax if worst_case_objective else sig_hat
    f = lambda lt: c / math.exp(lt) + w * sobj ** 2 * math.exp(lt) / 2 + r * z * smax * math.exp(lt / 2)
    o = minimize_scalar(f, bounds=(-30, 30), method="bounded", options={"xatol": 1e-12})
    tau = math.exp(o.x)
    return tau, z * smax * math.sqrt(tau), o.fun


def symbolic_a():
    """d ln x / d ln a in (-1/3, 0] at the interior optimum, x = sqrt(tau), a = r z sigma_max."""
    x, a, c, A = sp.symbols("x a c A", positive=True)
    # J(x) = c/x^2 + A x^2 + a x  (A = w sig_hat^2/2); FOC: G = -2c/x^3 + 2A x + a = 0
    G = -2 * c / x ** 3 + 2 * A * x + a
    dxda = -sp.diff(G, a) / sp.diff(G, x)
    elas = sp.simplify(dxda * a / x)  # d ln x / d ln a
    # on the FOC, 2c/x^3 = 2A x + a, so G_x = 6c/x^4 + 2A = 3(2A x + a)/x + 2A
    elas_on_foc = sp.simplify(elas.subs(c, (2 * A * x + a) * x ** 3 / 2))
    lower = sp.simplify(elas_on_foc + sp.Rational(1, 3))
    return elas_on_foc, lower


# ---------- R2-b ----------
def predictive_factor(n, eps):
    """Buffer multiplier (in units of the sample s.d.) for exact one-sided coverage 1-eps of a new
    Gaussian shock, mean and variance estimated from n iid draws: t_{n-1} quantile * sqrt(1+1/n)."""
    return stats.t.ppf(1 - eps, n - 1) * math.sqrt(1 + 1 / n)


def plugin_exceedance(n, eps):
    """True chance that a new shock exceeds the plug-in buffer xbar + z_eps*s (averaged over samples)."""
    z = stats.norm.ppf(1 - eps)
    return stats.t.sf(z / math.sqrt(1 + 1 / n), n - 1)


def mc_plugin_exceedance(n, eps, reps=400000, seed=3):
    rng = np.random.default_rng(seed)
    z = stats.norm.ppf(1 - eps)
    x = rng.standard_normal((reps, n))
    xb, s = x.mean(1), x.std(1, ddof=1)
    new = rng.standard_normal(reps)
    return float(np.mean(new > xb + z * s))


# ---------- R2-c ----------
def beta_moment_pn(a, b, n):
    """E[p^n] for p ~ Beta(a, b)."""
    out = 1.0
    for i in range(n):
        out *= (a + i) / (a + b + i)
    return out


def copies_plugin(k, m, e1):
    p = k / m
    return math.ceil(math.log(e1) / math.log(p) - 1e-12)


def copies_predictive(k, m, e1, prior=(1.0, 1.0)):
    a, b = prior[0] + k, prior[1] + m - k
    n = 1
    while beta_moment_pn(a, b, n) > e1:
        n += 1
        if n > 10 ** 6:
            return None
    return n


# ---------- R2-d ----------
def t_quantile_unit_var(nu, eps):
    return stats.t.ppf(1 - eps, nu) * math.sqrt((nu - 2) / nu)


def cantelli_factor(eps):
    return math.sqrt((1 - eps) / eps)


def run():
    res = {}
    elas, lower = symbolic_a()
    res["a_elasticity_on_foc"] = str(elas)
    res["a_elas_plus_third"] = str(lower)
    us = np.linspace(0, 2, 41)
    for wc in (False, True):
        D = [design_a(1.0, 1.0, 1.0, 0.2, 3.09, u, wc) for u in us]
        tau = [d[0] for d in D]; B = [d[1] for d in D]; J = [d[2] for d in D]
        tag = "wc" if wc else "nom"
        res[f"a_{tag}_tau_decreasing"] = all(b < a for a, b in zip(tau, tau[1:]))
        res[f"a_{tag}_B_increasing"] = all(b > a for a, b in zip(B, B[1:]))
        res[f"a_{tag}_J_increasing"] = all(b > a for a, b in zip(J, J[1:]))
        ratio = [B[i] / B[0] for i in range(len(us))]
        res[f"a_{tag}_B_ratio_at_u=1"] = round(ratio[20], 4)
        if not wc:
            res["a_nom_ratio_in_[(1+u)^(2/3),(1+u)]"] = all((1 + u) ** (2 / 3) - 1e-6 <= q <= (1 + u) + 1e-6 for u, q in zip(us, ratio))
    # slack an observer with the fitted model sees: per-window ruin chance of the robust buffer
    z = 3.09
    res["a_fitted_chance_of_robust_design_u=0.2,0.5"] = [float(stats.norm.sf(z * (1 + u))) for u in (0.2, 0.5)]
    # R2-b
    eps = 1e-3
    res["b_factor_vs_n"] = {n: round(predictive_factor(n, eps) / stats.norm.ppf(1 - eps), 4) for n in (5, 10, 20, 50, 200, 1000)}
    res["b_plugin_true_exceedance_n20"] = plugin_exceedance(20, eps)
    res["b_plugin_mc_n20"] = mc_plugin_exceedance(20, eps)
    facs = [predictive_factor(n, eps) for n in range(3, 400)]
    res["b_factor_decreasing_in_n"] = all(b < a for a, b in zip(facs, facs[1:]))
    # R2-c: E[p^n] >= (E p)^n (Jensen) => predictive copies >= plug-in copies
    e1 = 1e-6
    rows = {}
    viol = 0
    for k, m in [(1, 12), (5, 50), (50, 500), (500, 5000), (2, 100), (20, 1000)]:
        npl, npr = copies_plugin(k, m, e1), copies_predictive(k, m, e1)
        # plug-in with the posterior mean, for a like-for-like Jensen comparison
        a, b = 1 + k, 1 + m - k
        npm = math.ceil(math.log(e1) / math.log(a / (a + b)) - 1e-12)
        rows[(k, m)] = (npl, npm, npr)
        viol += npr < npm
    res["c_copies_(plugin_mle, plugin_postmean, predictive)"] = rows
    res["c_viol_predictive_below_postmean_plugin"] = viol
    # R2-d
    nus = [2.5, 3, 4, 5, 8, 15, 30, 100, 1000]
    q = [t_quantile_unit_var(nu, eps) for nu in nus]
    res["d_t_unitvar_quantiles_eps1e-3"] = dict(zip(nus, [round(v, 3) for v in q]))
    res["d_gauss_quantile"] = round(stats.norm.ppf(1 - eps), 3)
    res["d_cantelli_factor_eps1e-3"] = round(cantelli_factor(eps), 3)
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k, "=", v)
