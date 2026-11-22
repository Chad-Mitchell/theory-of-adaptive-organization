#!/usr/bin/env python3
"""Numerical checks for theory/COADAPTATION.md (T12, CX2 co-adaptation).

NUMERICAL checks of PROVED-in-model statements, plus minimal counterexamples.
Run from the repo root at nice 19:  nice -n 19 python3 tools/coadaptation_checks.py
Every function returns a dict; tools/test_coadaptation_checks.py asserts on them.
Seeds are fixed. Runtime is about half a minute on the box.

Sections (numbering follows COADAPTATION.md):
  s1  exact weak-mutation chain, Moran fixation, two parties: Gibbs in the
      beta-scaled potential (CA1), speed independence, and the mismatch case
  s1c random games: reversibility <=> beta-scaled game is exact potential
  s2  per-party regret d_i/(2 beta_i), potential excess d/2, team excess split
  s3  explicit Moran populations (Monte Carlo) against the Gibbs law
  s4  matching pennies (non-potential cycle): uniform law, excess 1/2 at all beta
  s5  LQ diffusion: potential (speed-free), opposed coupling (speed-dependent,
      virial identity), team with mismatched strengths (CA3 bound),
      cyclic chase (Hopf), world gain g > 1 (saddle), delay (Hayes bound),
      nonlinear virial check, CT34 lift (free energy and factorisation)
"""
from __future__ import annotations

import math
import numpy as np
from scipy.linalg import solve_continuous_lyapunov, null_space


# ---------------------------------------------------------------- helpers
def moran_fix(r_res, r_mut, N):
    """Haploid Moran fixation probability of one mutant (Sella-Hirsh form)."""
    rho = r_res / r_mut
    if abs(rho - 1.0) < 1e-14:
        return 1.0 / N
    return (1.0 - rho) / (1.0 - rho ** N)


def joint_generator(J, sizes, alphas, Ns, us):
    """Weak-mutation substitution chain for parties on path-graph design sets.

    J[i] is an array over the joint grid (shape = sizes) giving party i's cost.
    A move changes one party's design by +-1 at rate u_i * fixation prob.
    Returns (Q, states)."""
    n = len(sizes)
    states = list(np.ndindex(*sizes))
    index = {s: k for k, s in enumerate(states)}
    S = len(states)
    Q = np.zeros((S, S))
    for k, s in enumerate(states):
        for i in range(n):
            for step in (-1, 1):
                t = list(s)
                t[i] += step
                if not (0 <= t[i] < sizes[i]):
                    continue
                t = tuple(t)
                r_res = math.exp(-alphas[i] * J[i][s])
                r_mut = math.exp(-alphas[i] * J[i][t])
                Q[k, index[t]] += us[i] * moran_fix(r_res, r_mut, Ns[i])
        Q[k, k] = -Q[k].sum()
    return Q, states


def stationary(Q):
    v = null_space(Q.T)[:, 0]
    v = np.abs(v)
    return v / v.sum()


def kolmogorov_square_max(Q, states, sizes):
    """Max |log(product of rates around each elementary square / reverse)|."""
    index = {s: k for k, s in enumerate(states)}
    worst = 0.0
    n = len(sizes)
    for s in states:
        for i in range(n):
            for j in range(i + 1, n):
                a = list(s); a[i] += 1
                b = list(a); b[j] += 1
                c = list(s); c[j] += 1
                if a[i] >= sizes[i] or c[j] >= sizes[j]:
                    continue
                p = [s, tuple(a), tuple(b), tuple(c)]
                fwd = sum(math.log(Q[index[p[k]], index[p[(k + 1) % 4]]]) for k in range(4))
                bwd = sum(math.log(Q[index[p[(k + 1) % 4]], index[p[k]]]) for k in range(4))
                worst = max(worst, abs(fwd - bwd))
    return worst


# ---------------------------------------------------------------- s1
def s1_gibbs_two_parties():
    rng = np.random.default_rng(1)
    m1, m2 = 6, 5
    Phi = rng.normal(size=(m1, m2))
    h1 = rng.normal(size=(1, m2)) * np.ones((m1, 1))      # depends on x2 only
    h2 = rng.normal(size=(m1, 1)) * np.ones((1, m2))      # depends on x1 only
    w = (0.7, 2.0)
    Ns = (12, 30)
    gamma = 6.0
    # choose alpha_i so that beta_i * w_i = gamma with beta_i = alpha_i (N_i - 1)
    alphas = tuple(gamma / (w[i] * (Ns[i] - 1)) for i in range(2))
    J = [w[0] * Phi + h1, w[1] * Phi + h2]
    out = {}
    gibbs = np.exp(-gamma * Phi).ravel()
    gibbs /= gibbs.sum()
    errs = []
    for us in [(1.0, 1.0), (1.0, 0.05), (20.0, 1.0)]:
        Q, states = joint_generator(J, (m1, m2), alphas, Ns, us)
        pi = stationary(Q)
        errs.append(float(np.max(np.abs(pi - gibbs) / gibbs)))
        out.setdefault("kolmogorov_matched", kolmogorov_square_max(Q, states, (m1, m2)))
    out["matched_max_rel_err_over_speeds"] = max(errs)
    # mismatch: beta_1 w_1 = 6, beta_2 w_2 = 18
    alphas_mm = (alphas[0], 3 * alphas[1])
    pis = []
    for us in [(1.0, 1.0), (1.0, 0.05)]:
        Q, states = joint_generator(J, (m1, m2), alphas_mm, Ns, us)
        pis.append(stationary(Q))
        out.setdefault("kolmogorov_mismatch", kolmogorov_square_max(Q, states, (m1, m2)))
    # best Gibbs fit exp(-c Phi - f(x1) - g(x2))? test the strict claim: no
    # function Psi with pi = exp(-Psi) has the beta-scaled differences; the
    # speed dependence is the observable sign of non-reversibility.
    Qa, _ = joint_generator(J, (m1, m2), alphas, Ns, (1.0, 1.0))
    Qb, _ = joint_generator(J, (m1, m2), alphas, Ns, (1.0, 0.05))
    out["matched_speed_dependence_tv"] = float(0.5 * np.abs(stationary(Qa) - stationary(Qb)).sum())
    out["mismatch_speed_dependence_tv"] = float(0.5 * np.abs(pis[0] - pis[1]).sum())
    return out


def s1c_random_iff(trials=60):
    rng = np.random.default_rng(2)
    agree = 0
    pot_rev, nonpot_rev = 0, 0
    for t in range(trials):
        sizes = (3, 3, 2)
        betas = rng.uniform(0.5, 3.0, size=3)
        Ns = (5, 9, 7)
        alphas = [betas[i] / (Ns[i] - 1) for i in range(3)]
        make_pot = t % 2 == 0
        if make_pot:
            Psi = rng.normal(size=sizes)
            J = []
            for i in range(3):
                extra = rng.normal(size=tuple(1 if k == i else sizes[k] for k in range(3)))
                J.append(Psi / betas[i] + extra * np.ones(sizes))
        else:
            J = [rng.normal(size=sizes) for _ in range(3)]
        Q, states = joint_generator(J, sizes, alphas, Ns, rng.uniform(0.2, 2, size=3))
        rev = kolmogorov_square_max(Q, states, sizes) < 1e-9
        # direct exact-potential test of the beta-scaled game on squares
        pot = True
        for s in states:
            for i in range(3):
                for j in range(i + 1, 3):
                    a = list(s); a[i] += 1
                    c = list(s); c[j] += 1
                    if a[i] >= sizes[i] or c[j] >= sizes[j]:
                        continue
                    b = list(a); b[j] += 1
                    s0, a, b, c = s, tuple(a), tuple(b), tuple(c)
                    cyc = (betas[i] * (J[i][a] - J[i][s0]) + betas[j] * (J[j][b] - J[j][a])
                           + betas[i] * (J[i][c] - J[i][b]) + betas[j] * (J[j][s0] - J[j][c]))
                    if abs(cyc) > 1e-9:
                        pot = False
        agree += int(rev == pot)
        if make_pot:
            pot_rev += int(rev)
        else:
            nonpot_rev += int(rev)
    return {"trials": trials, "agree": agree, "potential_reversible": pot_rev,
            "random_reversible": nonpot_rev}


# ---------------------------------------------------------------- s2
def s2_regret_and_team(b1=80.0, spacing=0.01, half=0.6):
    """Quadratic weighted-potential game on a fine lattice; exact Gibbs law.
    Weights w = (1, 2.5); beta_2 is set so that beta_1 w_1 = beta_2 w_2 = gamma."""
    g = np.arange(-half, half + 1e-12, spacing)
    X1, X2 = np.meshgrid(g, g, indexing="ij")
    w = (1.0, 2.5)
    gamma = b1 * w[0]
    b2 = gamma / w[1]
    P = np.array([[1.0, 0.4], [0.4, 1.5]])
    Phi = 0.5 * (P[0, 0] * X1 ** 2 + 2 * P[0, 1] * X1 * X2 + P[1, 1] * X2 ** 2)
    # externalities: party 1 also bears e1 * x2^2 + f1*x2 (not its own control)
    J1 = w[0] * Phi + 0.8 * X2 ** 2 + 0.3 * X2
    J2 = w[1] * Phi + 0.5 * X1 ** 2 - 0.6 * X1
    Psi = gamma * Phi
    pi = np.exp(-(Psi - Psi.min()))
    pi /= pi.sum()
    R1 = J1 - J1.min(axis=0, keepdims=True)
    R2 = J2 - J2.min(axis=1, keepdims=True)
    out = {
        "E_regret1": float((pi * R1).sum()), "pred1": 1 / (2 * b1),
        "E_regret2": float((pi * R2).sum()), "pred2": 1 / (2 * b2),
        "E_Psi_excess": float((pi * (Psi - Psi.min())).sum()), "pred_Psi": 1.0,
    }
    JT = J1 + J2
    # continuous formulas: Nash = argmin Phi = 0; team Hessian
    HT = (w[0] + w[1]) * P + np.diag([2 * 0.5, 2 * 0.8])
    lin = np.array([-0.6, 0.3])
    xopt = np.linalg.solve(HT, -lin)
    JT_opt = 0.5 * xopt @ HT @ xopt + lin @ xopt
    poa_gap = 0.0 - JT_opt
    scatter = 0.5 * np.trace(HT @ np.linalg.inv(gamma * P))
    out.update({"E_team_excess": float((pi * JT).sum() - JT_opt),
                "pred_team": float(poa_gap + scatter), "poa_gap": float(poa_gap),
                "team_scatter": float(scatter)})
    return out


# ---------------------------------------------------------------- s3
def s3_moran_population_mc(steps=200000, seed=3):
    rng = np.random.default_rng(seed)
    m = (3, 3)
    w = (1.0, 0.5)
    Ns = (8, 8)
    gamma = 2.0
    alphas = [gamma / (w[i] * (Ns[i] - 1)) for i in range(2)]
    Phi = np.array([[0.0, 0.5, 1.4], [0.3, 0.2, 0.9], [1.1, 0.6, 0.4]])
    J = [w[0] * Phi + np.array([0.2, -0.1, 0.4])[None, :],
         w[1] * Phi + np.array([0.0, 0.7, -0.3])[:, None]]
    us = (1.0, 0.6)
    U = sum(us)

    def fixes(i, s, t):
        N = Ns[i]
        r_res = math.exp(-alphas[i] * J[i][s])
        r_mut = math.exp(-alphas[i] * J[i][t])
        k = 1
        while 0 < k < N:
            # birth proportional to fitness, death uniform (one Moran event)
            pb = k * r_mut / (k * r_mut + (N - k) * r_res)
            born_mut = rng.random() < pb
            dies_mut = rng.random() < k / N
            k += int(born_mut) - int(dies_mut)
        return k == N

    s = (0, 0)
    counts = np.zeros(m)
    for _ in range(steps):
        counts[s] += 1
        i = 0 if rng.random() < us[0] / U else 1
        step = 1 if rng.random() < 0.5 else -1
        t = list(s); t[i] += step
        if 0 <= t[i] < m[i]:
            t = tuple(t)
            # a new mutant arises; it fixes with the Moran probability.
            # Uniformisation: each edge's clock is u_i/U per step, and the
            # factor N (mutants per unit time) is absorbed into the clock.
            if fixes(i, s, t):
                s = t
    emp = counts / counts.sum()
    gibbs = np.exp(-gamma * Phi)
    gibbs /= gibbs.sum()
    return {"tv": float(0.5 * np.abs(emp - gibbs).sum()), "steps": steps}


# ---------------------------------------------------------------- s4
def s4_matching_pennies(betas=(1.0, 5.0, 20.0)):
    out = {}
    J1 = np.array([[0.0, 1.0], [1.0, 0.0]])   # party 1 wants to match
    J2 = 1.0 - J1                               # party 2 wants to mismatch
    for b in betas:
        Q, states = joint_generator([J1, J2], (2, 2), (b / 9, b / 9), (10, 10), (1.0, 1.0))
        pi = stationary(Q).reshape(2, 2)
        idx = {s: k for k, s in enumerate(states)}
        cyc = [(0, 0), (1, 0), (1, 1), (0, 1)]
        flow = [pi[a] * Q[idx[a], idx[b2]] - pi[b2] * Q[idx[b2], idx[a]]
                for a, b2 in zip(cyc, cyc[1:] + cyc[:1])]
        out[b] = {"E_J1": float((pi * J1).sum()), "E_J2": float((pi * J2).sum()),
                  "max_dev_uniform": float(np.abs(pi - 0.25).max()),
                  "cycle_current": float(np.mean(np.abs(flow)))}
    return out


# ---------------------------------------------------------------- s5 (LQ diffusion)
def lyap_sigma(D, B, M):
    A = D @ B @ M
    ev = np.linalg.eigvals(A)
    if np.min(ev.real) <= 0:
        return None, ev
    # A S + S A^T = 2 D
    S = solve_continuous_lyapunov(A, 2 * D)
    return S, ev


def em_sim(grad, D, B, x0, dt, steps, burn, rng, chains=1000):
    d = len(x0)
    x = np.tile(np.asarray(x0, float), (chains, 1))
    acc = []
    sq = np.sqrt(2 * np.diag(D) * dt)
    Dd, Bd = np.diag(D), np.diag(B)
    for k in range(steps):
        x = x - dt * (Dd * Bd) * grad(x) + sq * rng.normal(size=x.shape)
        if k >= burn and k % 10 == 0:
            acc.append(x.copy())
        if not np.all(np.isfinite(x)) or np.abs(x).max() > 1e6:
            return None
    return np.concatenate(acc)


def s5a_potential_speed_free():
    rng = np.random.default_rng(5)
    P = np.array([[2.0, 0.6], [0.6, 1.0]])
    w = np.array([1.0, 3.0]); gamma = 4.0
    B = np.diag(gamma / w)
    M = np.diag(w) @ P          # own-gradient Jacobian: row i = w_i * P[i]
    K = B @ M                   # = gamma P, symmetric
    sigmas = []
    for r in (0.1, 1.0, 10.0):
        S, _ = lyap_sigma(np.diag([1.0, r]), B, M)
        sigmas.append(S)
    target = np.linalg.inv(K)
    return {"max_err_vs_gibbs": float(max(np.abs(S - target).max() for S in sigmas))}


def s5b_opposed_virial(seed=6):
    """J1 = a/2 x1^2 + c x1 x2,  J2 = b/2 x2^2 - c x1 x2: not potential (c != 0)."""
    rng = np.random.default_rng(seed)
    a, b, c = 1.0, 2.0, 1.5
    M = np.array([[a, c], [-c, b]])
    B = np.diag([3.0, 2.0])
    out = {"sigma_by_speed": {}}
    for r in (0.2, 1.0, 5.0):
        D = np.diag([1.0, r])
        S, ev = lyap_sigma(D, B, M)
        K = B @ M
        vir = [float((K @ S)[i, i]) for i in range(2)]   # beta_i E[x_i d_i J_i]
        out["sigma_by_speed"][r] = {"Sigma": S.tolist(), "virial": vir}
    # Monte Carlo at r = 1
    D = np.diag([1.0, 1.0])
    grad = lambda x: x @ M.T
    xs = em_sim(grad, D, B, [0, 0], 2e-3, 30000, 5000, rng, chains=400)
    g = xs @ M.T
    out["mc_virial"] = [float(B[i, i] * np.mean(xs[:, i] * g[:, i])) for i in range(2)]
    S1 = solve_continuous_lyapunov(D @ B @ M, 2 * D)
    out["mc_cov_err"] = float(np.abs(np.cov(xs.T) - S1).max())
    out["mc_cov_scale"] = float(np.abs(S1).max())
    vals = [np.array(v["Sigma"]) for v in out["sigma_by_speed"].values()]
    out["speed_spread"] = float(max(np.abs(vals[0] - v).max() for v in vals))
    return out


def s5c_team_mismatch(trials=3000, seed=7):
    rng = np.random.default_rng(seed)
    viol, worst_lo, worst_hi = 0, 1e9, -1e9
    eq_err = 0.0
    for _ in range(trials):
        d = rng.integers(2, 5)
        Aq = rng.normal(size=(d, d))
        Q = Aq @ Aq.T + 0.1 * np.eye(d)
        c = rng.uniform(0.2, 5.0, size=d)
        D = np.diag(rng.uniform(0.05, 5.0, size=d))
        Sg = solve_continuous_lyapunov(D @ np.diag(c) @ Q, 2 * D)
        ex = 0.5 * np.trace(Q @ Sg)
        lo, hi = d / (2 * c.max()), d / (2 * c.min())
        worst_lo = min(worst_lo, ex / lo)
        worst_hi = max(worst_hi, ex / hi)
        if ex < lo * (1 - 1e-9) or ex > hi * (1 + 1e-9):
            viol += 1
        ce = np.full(d, c[0])
        Se = solve_continuous_lyapunov(D @ np.diag(ce) @ Q, 2 * D)
        eq_err = max(eq_err, abs(0.5 * np.trace(Q @ Se) - d / (2 * c[0])))
    return {"trials": trials, "violations": viol, "min_ratio_to_lower": float(worst_lo),
            "max_ratio_to_upper": float(worst_hi), "equal_strength_err": float(eq_err)}


def s5d_cyclic_chase():
    out = {}
    P = np.roll(np.eye(3), 1, axis=1)   # x_{i+1}
    for c in (1.5, 1.9, 2.1, 3.0):
        M = np.eye(3) + c * P            # d_i J_i for J_i = 1/2 (x_i + c x_{i+1})^2
        ev = np.linalg.eigvals(M)
        out[c] = {"min_real": float(ev.real.min()),
                  "stable": bool(ev.real.min() > 0)}
    return out


def s5e_world_gain():
    out = {}
    for g in (0.5, 0.9, 1.1, 2.0):
        # system J_s = 1/2 (x - th)^2 ; world relaxes on J_w = 1/2 (th - g x)^2
        M = np.array([[1.0, -1.0], [-g, 1.0]])
        bs = 1.0; bw = bs / g        # beta-scaled game is exact potential
        K = np.diag([bs, bw]) @ M
        sym = bool(abs(K[0, 1] - K[1, 0]) < 1e-12)
        ev = np.linalg.eigvals(np.diag([1.0, 3.0]) @ K)
        out[g] = {"potential": sym, "det_hessPsi": float(np.linalg.det(K)),
                  "stable": bool(ev.real.min() > 0)}
    return out


def s5f_delay(g=-2.0, k=1.0):
    """x' = -k (x - g x(t - tau)); g < -1.  Hayes: stable iff k tau < arccos(1/g)/sqrt(g^2-1)."""
    crit = math.acos(1 / g) / math.sqrt(g * g - 1)
    res = {}
    for f in (0.8, 1.2):
        tau = f * crit / k
        dt = tau / 400
        lag = 400
        n = int(120 / dt)
        x = np.zeros(n + lag)
        x[:lag + 1] = 1.0
        for t in range(lag, n + lag - 1):
            x[t + 1] = x[t] - dt * k * (x[t] - g * x[t - lag])
        early = np.abs(x[lag: lag + n // 4]).max()
        late = np.abs(x[-n // 4:]).max()
        res[f] = {"late_over_early": float(late / early)}
    # no delay: always stable for g < 1
    res["k_tau_crit"] = crit
    return res


def s5g_nonlinear_virial(seed=8):
    """Non-potential, nonlinear: J1 = x1^4/4 + x1^2/2 + c x1 x2 ; J2 = x2^2/2 - c x1 x2 + e x1^2 x2."""
    rng = np.random.default_rng(seed)
    c, e = 0.8, 0.4
    B = np.diag([2.0, 3.0])
    D = np.diag([1.0, 0.4])

    def grad(x):
        g1 = x[:, 0] ** 3 + x[:, 0] + c * x[:, 1]
        g2 = x[:, 1] - c * x[:, 0] + e * x[:, 0] ** 2
        return np.stack([g1, g2], axis=1)

    xs = em_sim(grad, D, B, [0, 0], 5e-4, 100000, 20000, rng, chains=400)
    G = grad(xs)
    out = {}
    for ref in (0.0, 1.0):
        out[ref] = [float(B[i, i] * np.mean((xs[:, i] - ref) * G[:, i])) for i in range(2)]
    out["mean_grad"] = [float(np.mean(G[:, i])) for i in range(2)]
    return out


def s5h_ct34_lift():
    """Parent x, team y; J = F(x) + 1/2 h(x) (y - m(x))^2 + J_T*(x).  Equal beta:
    the parent's marginal is Gibbs in F + J_T* + (1/(2 beta)) log h (free energy)."""
    beta = 7.0
    x = np.linspace(-2, 2, 401)
    y = np.linspace(-8, 8, 3201)
    X, Y = np.meshgrid(x, y, indexing="ij")
    F = 0.5 * x ** 2 - 0.3 * x
    h = 1.0 + 0.8 * np.tanh(x) + 0.5
    m = 0.4 * x
    JT = 0.2 * x ** 2 + 0.1
    Jfull = F[:, None] + 0.5 * h[:, None] * (Y - m[:, None]) ** 2 + JT[:, None]
    marg = np.exp(-beta * (Jfull - Jfull.min())).sum(axis=1)
    marg /= marg.sum()
    pred = np.exp(-beta * (F + JT + np.log(h) / (2 * beta)))
    pred /= pred.sum()
    upk = np.exp(-beta * (F + JT))       # the "team as upkeep only" approximation
    upk /= upk.sum()
    out = {"tv_free_energy": float(0.5 * np.abs(marg - pred).sum()),
           "tv_upkeep_only": float(0.5 * np.abs(marg - upk).sum())}
    # theta fixed (h, m, JT constant in x) with mismatched strengths: product law
    bp, bt = 3.0, 11.0
    hx, mx = 1.7, 0.2
    J_par = F[:, None] + 0.0 * Y
    J_team = 0.5 * hx * (Y - mx) ** 2 + 0.0 * X
    Psi = bp * J_par + bt * J_team
    pi = np.exp(-(Psi - Psi.min())); pi /= pi.sum()
    Ey = float((pi * J_team).sum())
    out["team_scatter_fixed_theta"] = Ey
    out["pred_team_scatter"] = 1 / (2 * bt)
    return out


def run_all():
    return {
        "s1": s1_gibbs_two_parties(),
        "s1c": s1c_random_iff(),
        "s2": s2_regret_and_team(),
        "s3": s3_moran_population_mc(),
        "s4": s4_matching_pennies(),
        "s5a": s5a_potential_speed_free(),
        "s5b": s5b_opposed_virial(),
        "s5c": s5c_team_mismatch(),
        "s5d": s5d_cyclic_chase(),
        "s5e": s5e_world_gain(),
        "s5f": s5f_delay(),
        "s5g": s5g_nonlinear_virial(),
        "s5h": s5h_ct34_lift(),
    }


if __name__ == "__main__":
    import json, time
    t0 = time.time()
    res = run_all()
    print(json.dumps(res, indent=1, default=str))
    print(f"elapsed {time.time() - t0:.1f}s")
