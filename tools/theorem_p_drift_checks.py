#!/usr/bin/env python3
"""Numerical checks for theory/THEOREM_P_DRIFT.md (PD1-PD7, CE1-CE7).

NUMERICAL: checks of the statements, not the proofs. Units: nats unless a
line says bits. Run from the repo root:

    nice -n 19 python3 tools/theorem_p_drift_checks.py          # quick
    nice -n 19 python3 tools/theorem_p_drift_checks.py --full   # documented run

Exit 0 and the line ALL PD CHECKS PASS means every check held. --full also
writes theory/theorem_p_drift_checks/results_full.json.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ------------------------------------------------------------------ floors
def floor_sharp(r, a, q, n=1):
    """PD1 sharp tier, lead 0: n * N* with N* = N_W e^{-2r/n} / (1 - alpha e^{-2r/n}).
    Scalar: q e^{-2r}/(1 - a^2 e^{-2r}); inf if r <= log|a|."""
    alpha = abs(a) ** (2.0 / n) if n == 1 else a
    e = math.exp(-2.0 * r / n)
    if alpha * e >= 1.0:
        return math.inf
    return n * q * e / (1.0 - alpha * e)


def floor_general(r, q_inn, n=1):
    """PD1 general tier: n * N_inn * e^{-2r/n}."""
    return n * q_inn * math.exp(-2.0 * r / n)


def floor_lead(r, a, q, k):
    """Sharp tier, lead k, scalar: a^{2k} N* + q (a^{2k}-1)/(a^2-1) (k q if a^2 = 1)."""
    Ns = floor_sharp(r, a, q)
    a2 = a * a
    acc = k * q if abs(a2 - 1.0) < 1e-15 else q * (a2**k - 1.0) / (a2 - 1.0)
    return a2**k * Ns + acc


def kalman_steady(a, q, s, iters=20000):
    """Scalar Kalman filter for x' = a x + w (Var q), y = x + v (Var s).
    Returns (P_post, P_prior, r) with r = 1/2 log(P_prior/P_post) = I(X_t; Y_t | Y^{t-1})."""
    P = q
    for _ in range(iters):
        Pp = a * a * P + q
        Pn = Pp * s / (Pp + s)
        if abs(Pn - P) < 1e-15 * max(1.0, P):
            P = Pn
            break
        P = Pn
    Pp = a * a * P + q
    return P, Pp, 0.5 * math.log(Pp / P)


def price_optimum_rw(q, w, c):
    """PD5 closed form for the scalar random walk: minimise w q/(e^{2r}-1) + c r.
    e^{2r*} = 1 + x + sqrt(x^2 + 2x), x = w q / c."""
    x = w * q / c
    z = 1.0 + x + math.sqrt(x * x + 2.0 * x)
    r = 0.5 * math.log(z)
    return r, w * q / (z - 1.0) + c * r


def sparse_look_counterexample(K=16):
    """CE7: X_t = t Z + G_t, Z, G_t ~ N(0,1), observe Y = X + N(0,1) at t = 2^k.

    Memory is the posterior of Z. Between looks, A_t = t E[Z | looks so far].
    Inflow is I(X_t; Y_t | previous looks) at look times and 0 otherwise.
    Stock I(M_T; X_T) uses the Z-posterior after the last look,
    I = (1/2) log(Var(X_T) / (T^2 Var(Z | looks) + 1)).

    Returns a dict: T, n_looks, max_mse, total_r, mean_r, blind_mse, stock_I.
    """
    T = 2 ** K
    v = 1.0
    total_r = 0.0
    max_mse = 0.0
    for k in range(0, K + 1):
        t = 2 ** k
        max_mse = max(max_mse, t * t * v + 1.0)
        total_r += 0.5 * math.log(t * t * v + 2.0)
        v = v * 2.0 / (t * t * v + 2.0)
    varX = T * T + 1.0
    return {
        "T": T,
        "n_looks": K + 1,
        "max_mse": max_mse,
        "total_r": total_r,
        "mean_r": total_r / T,
        "blind_mse": varX,
        "stock_I": 0.5 * math.log(varX / (T * T * v + 1.0)),
    }


# ------------------------------------------------------------------ helpers
def check(ok, lines, name, cond, msg=""):
    ok.append((name, bool(cond)))
    lines.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


def fbm_cov(T, H):
    t = np.arange(1, T + 1, dtype=float)
    return 0.5 * (t[:, None] ** (2 * H) + t[None, :] ** (2 * H) - np.abs(t[:, None] - t[None, :]) ** (2 * H))


def cond_var(C, idx_target, idx_given):
    if len(idx_given) == 0:
        return C[idx_target, idx_target]
    g = np.array(idx_given)
    Cgg = C[np.ix_(g, g)]
    cg = C[idx_target, g]
    return C[idx_target, idx_target] - cg @ np.linalg.solve(Cgg, cg)


# ------------------------------------------------------------------ checks
def run(full):
    ok, lines, res = [], [], {}

    # 1. Tightness of the sharp tier on the scalar Gauss-Markov world (Kalman)
    worst = 0.0
    for a in (0.5, 0.9, 1.0, 1.2, 2.0):
        for s in (0.01, 0.1, 1.0, 10.0):
            P, Pp, r = kalman_steady(a, 1.0, s)
            f = floor_sharp(r, a, 1.0)
            worst = max(worst, abs(P - f) / P)
            if not r > math.log(abs(a)) - 1e-12:
                check(ok, lines, "Kalman rate above log|a| (a=%g,s=%g)" % (a, s), False)
    check(ok, lines, "PD1 sharp tier is met with equality by the Kalman filter (20 worlds)", worst < 1e-9,
          "max relative gap %.2e" % worst)
    res["kalman_tightness_max_rel_gap"] = worst

    # 2. Quantised trackers sit above the floor (random walk and a stable world), Monte Carlo.
    # Fixed-range quantisers overload and diverge in unstable worlds (zoom quantisers are
    # needed there; theory/INTERNAL_MODEL.md section 4), so a = 1.2 is not used here.
    rng = np.random.default_rng(3)
    T = 60000 if full else 15000
    qrows = []
    allabove = True
    for a in (0.9, 1.0):
        for bits in (1, 2, 3):
            L = 2 ** bits
            best = math.inf
            for step in np.linspace(0.2, 3.0, 29):
                levels = (np.arange(L) - (L - 1) / 2.0) * step
                x, xh, se, cnt = 0.0, 0.0, 0.0, 0
                noise = rng.normal(size=T)
                for t in range(T):
                    x = a * x + noise[t]
                    pred = a * xh
                    k = int(np.argmin(np.abs(levels - (x - pred))))
                    xh = pred + levels[k]
                    if t > 500:
                        se += (x - xh) ** 2
                        cnt += 1
                best = min(best, se / cnt)
            r = bits * math.log(2.0)
            f = floor_sharp(r, a, 1.0)
            allabove &= best >= f
            qrows.append({"a": a, "bits": bits, "D_best_quantiser": best, "floor": f})
            lines.append("  quantiser a=%.1f %d bit(s)/step: best D over 29 step sizes=%.4f  floor=%.4f  ratio %.2f" % (a, bits, best, f, best / f))
    check(ok, lines, "PD1: uniform quantised trackers sit above the floor (r <= bits * ln 2)", allabove)
    res["quantisers"] = qrows

    # 3. General tier on fractional Brownian motion (noisy observations, full-history memory)
    Tf = 160 if full else 80
    fb = []
    allok = True
    for H in (0.3, 0.5, 0.7):
        C = fbm_cov(Tf, H)
        for s in (0.05, 0.5):
            Cy = C + s * np.eye(Tf)
            worst_margin = math.inf
            for t in range(1, Tf):
                # posterior and prior variances of X_t given Y^t and Y^{t-1}
                idx = list(range(t + 1))
                Cyy = Cy[np.ix_(idx, idx)]
                cxy = C[t, idx]
                post = C[t, t] - cxy @ np.linalg.solve(Cyy, cxy)
                idxp = list(range(t))
                prior = C[t, t] - C[t, idxp] @ np.linalg.solve(Cy[np.ix_(idxp, idxp)], C[t, idxp])
                r = 0.5 * math.log(prior / post)
                inn = cond_var(C, t, list(range(t)))
                f = inn * math.exp(-2 * r)
                worst_margin = min(worst_margin, post / f)
            allok &= worst_margin >= 1 - 1e-9
            fb.append({"H": H, "s": s, "min_ratio_D_over_floor": worst_margin, "innovation_var_last": inn})
            lines.append("  fBm H=%.1f s=%.2f: min over t of D/floor = %.4f (innovation variance at T: %.4f)" % (H, s, worst_margin, inn))
    check(ok, lines, "PD1 general tier holds on fBm (H = 0.3, 0.5, 0.7) for every t", allok)
    res["fbm"] = fb

    # 4. CE1: the stock I(M_t; X_t) grows without bound for a competent random-walk tracker
    P, Pp, r = kalman_steady(1.0, 1.0, 1.0)
    stock = [0.5 * math.log((t * 1.0) / P) for t in (10, 100, 1000, 10000)]
    check(ok, lines, "CE1: I(M_t; X_t) grows like 1/2 log t (random walk, steady Kalman)",
          all(abs((stock[i + 1] - stock[i]) - 0.5 * math.log(10)) < 1e-12 for i in range(3)),
          "I at t=10,100,1000,10000: %s nats; inflow r stays %.4f nats/step" % (", ".join("%.3f" % v for v in stock), r))
    res["ce1_stock"] = stock

    # 5. PD5 price optimum: closed form vs numerical minimum; continuous-time limit = CT7 form
    allp = True
    for (q, w, c) in ((1.0, 1.0, 0.1), (1.0, 1.0, 1.0), (2.0, 0.5, 5.0), (1.0, 10.0, 0.01)):
        r, J = price_optimum_rw(q, w, c)
        num = minimize_scalar(lambda rr: w * q / math.expm1(2 * rr) + c * rr, bounds=(1e-9, 50), method="bounded",
                              options={"xatol": 1e-12})
        allp &= abs(num.fun - J) < 1e-8 * max(1, J)
    check(ok, lines, "PD5 closed-form optimum matches numerical minimisation", allp)
    sig2, w, c = 1.0, 1.0, 0.3
    vals = []
    for dt in (1e-1, 1e-2, 1e-3, 1e-4):
        # cost per unit time: w D + c r/dt with D = sig2 dt/(e^{2r}-1); same as price_optimum_rw with q=sig2 dt, c->c/dt... scale
        r, Jstep = price_optimum_rw(sig2 * dt, w, c / dt)
        vals.append(Jstep)
    target = math.sqrt(2 * sig2 * w * c)
    check(ok, lines, "PD5 continuous-time limit -> sigma sqrt(2 w c) (CT7 form with kT -> c)", abs(vals[-1] - target) < 2e-3 * target,
          "J*(dt) = %s, limit %.5f" % (", ".join("%.5f" % v for v in vals), target))
    res["pd5_ct_limit"] = {"dt": [1e-1, 1e-2, 1e-3, 1e-4], "J": vals, "target": target}

    # 6. PD7 OU continuous time: sampled bound -> sigma^2/(2D) - theta; Kalman-Bucy meets it
    theta, sig2 = 0.7, 1.0
    allou = True
    for snr_s in (0.05, 0.5, 5.0):  # observation noise intensity
        # Kalman-Bucy steady state: 0 = -2 theta P + sig2 - P^2/s
        s = snr_s
        P = s * (-theta + math.sqrt(theta**2 + sig2 / s))
        info_rate = P / (2 * s)  # Duncan
        bound = sig2 / (2 * P) - theta
        allou &= abs(info_rate - bound) < 1e-12
        dt = 1e-5
        a = math.exp(-theta * dt)
        qd = sig2 * (1 - a * a) / (2 * theta)
        disc = 0.5 * math.log(a * a + qd / P) / dt
        allou &= abs(disc - bound) < 1e-3 * max(1, abs(bound))
    check(ok, lines, "PD7: Kalman-Bucy information rate = sigma^2/(2P) - theta; sampled bound converges", allou)

    # 7. CE3: lattice walk +-1 is tracked exactly with 1 bit/step; the continuous floor is vacuous
    xs = np.cumsum(rng.choice([-1, 1], size=10000))
    xh = np.cumsum(np.sign(np.diff(np.concatenate([[0], xs]))))  # decoder adds the transmitted sign
    check(ok, lines, "CE3: +-1 lattice walk tracked with zero error at r = ln 2 (density-free world)",
          np.all(xh == xs), "D = %.1f; the density bound gives 0 (no density), the right currency is H(step) = ln 2" % float(np.mean((xs - xh) ** 2)))

    # 8. PD4 lead-time cap, random walk q = 1, w = 1, margin 3.5
    margin = 3.5
    kcap = max(k for k in range(0, 50) if floor_lead(50.0, 1.0, 1.0, k) < margin)
    check(ok, lines, "PD4: random-walk lead cap at infinite inflow is floor(margin/(w q))", kcap == 3,
          "k_max = %d for margin 3.5" % kcap)

    # 9. Time-varying inflow (Jensen step): alternating Kalman gains stay above floor(mean r)
    a, q = 1.0, 1.0
    P = 1.0
    Ds, rs = [], []
    for t in range(4000):
        s = 0.05 if t % 2 == 0 else 5.0
        Pp = a * a * P + q
        Pn = Pp * s / (Pp + s)
        rs.append(0.5 * math.log(Pp / Pn))
        Ds.append(Pn)
        P = Pn
    Dbar, rbar = float(np.mean(Ds[1000:])), float(np.mean(rs[1000:]))
    check(ok, lines, "PD1 with time-varying inflow: mean D >= floor(mean r)", Dbar >= floor_sharp(rbar, a, q),
          "mean D %.4f, floor(mean r) %.4f" % (Dbar, floor_sharp(rbar, a, q)))

    # 10. CE5: general tier is loose at low rate in a random walk; ratio sharp/general -> infinity
    ratios = [floor_sharp(r, 1.0, 1.0) / floor_general(r, 1.0) for r in (1.0, 0.1, 0.01, 0.001)]
    check(ok, lines, "CE5: sharp/general floor ratio grows without bound as r -> 0 (random walk)",
          all(ratios[i + 1] > ratios[i] for i in range(3)) and ratios[-1] > 400,
          "ratios %s" % ", ".join("%.1f" % v for v in ratios))

    # 11. PD3: blind action in a random walk has mean squared loss growing without bound
    check(ok, lines, "PD3: blind loss Var(X_t) = t q grows without bound; floor(r -> 0+) -> inf",
          floor_sharp(1e-9, 1.0, 1.0) > 1e8 and floor_sharp(0.0, 1.0, 1.0) == math.inf)

    # 12. CE7: vanishing mean inflow outside the linear class (exact Gaussians, T = 2^16)
    ce7 = sparse_look_counterexample(16)
    check(
        ok, lines,
        "CE7: sparse looks keep MSE <= 7 with mean inflow 2.56e-4 through T=2^16 (rbar=0)",
        ce7["max_mse"] <= 7.00 + 1e-9
        and abs(ce7["total_r"] - 16.8) < 0.05
        and ce7["n_looks"] == 17
        and abs(ce7["mean_r"] - 2.56e-4) < 5e-7
        and abs(ce7["blind_mse"] - 4.29e9) / 4.29e9 < 0.005
        and abs(ce7["stock_I"] - 10.63) < 0.005,
        "MSE <= %.2f; total inflow %.1f nats over %d looks; mean inflow %.2e; "
        "blind MSE %.2e; I(M_T;X_T)=%.2f nats"
        % (ce7["max_mse"], ce7["total_r"], ce7["n_looks"], ce7["mean_r"],
           ce7["blind_mse"], ce7["stock_I"]),
    )
    res["ce7"] = ce7

    return ok, lines, res


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    full = "--full" in argv
    ok, lines, res = run(full)
    print("\n".join(lines))
    if full:
        os.makedirs(os.path.join(ROOT, "theory", "theorem_p_drift_checks"), exist_ok=True)
        with open(os.path.join(ROOT, "theory", "theorem_p_drift_checks", "results_full.json"), "w") as fh:
            json.dump(res, fh, indent=1)
    if all(c for _, c in ok):
        print("ALL PD CHECKS PASS")
        return 0
    print("SOME PD CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
