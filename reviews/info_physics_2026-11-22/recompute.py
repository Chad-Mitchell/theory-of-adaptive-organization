#!/usr/bin/env python3
"""Independent recomputation for the review of PR #175.

Does not import theory/info_physics_checks. Rates, entropy production,
and information flow are derived in this file.

Run from the repo root:
  nice -n 19 python3 reviews/info_physics_2026-11-22/recompute.py
"""
from __future__ import annotations

import math
import numpy as np

LN2 = math.log(2.0)


def hbin(p):
    p = float(p)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def mi_discrete(pairs):
    """Mutual information in nats from an iterable of (a, b, p)."""
    pa, pb, jab = {}, {}, {}
    for a, b, p in pairs:
        if p <= 0.0:
            continue
        pa[a] = pa.get(a, 0.0) + p
        pb[b] = pb.get(b, 0.0) + p
        jab[(a, b)] = jab.get((a, b), 0.0) + p
    mi = 0.0
    for (a, b), p in jab.items():
        mi += p * math.log(p / (pa[a] * pb[b]))
    return mi


def cmi_from_joint(triples):
    """I(A; B | C) from (a, b, c, p)."""
    # I(A;B|C) = sum p(a,b,c) log p(a,b|c) / (p(a|c)p(b|c))
    pabc, pac, pbc, pc = {}, {}, {}, {}
    for a, b, c, p in triples:
        if p <= 0.0:
            continue
        pabc[(a, b, c)] = pabc.get((a, b, c), 0.0) + p
        pac[(a, c)] = pac.get((a, c), 0.0) + p
        pbc[(b, c)] = pbc.get((b, c), 0.0) + p
        pc[c] = pc.get(c, 0.0) + p
    out = 0.0
    for (a, b, c), p in pabc.items():
        out += p * math.log((p * pc[c]) / (pac[(a, c)] * pbc[(b, c)]))
    return out


def stationary_from_rates(rate):
    """rate(i, j) for i != j. States 0..n-1 inferred from keys."""
    n = 0
    for i, j in rate:
        n = max(n, i + 1, j + 1)
    G = np.zeros((n, n))
    for (i, j), k in rate.items():
        if i == j or k == 0.0:
            continue
        G[i, j] += k
    for i in range(n):
        G[i, i] = -G[i].sum()
    A = G.T.copy()
    A[-1, :] = 1.0
    b = np.zeros(n)
    b[-1] = 1.0
    p = np.linalg.solve(A, b)
    p = np.real(np.real_if_close(p))
    p = np.clip(p, 0.0, None)
    p /= p.sum()
    return p, G


def edge_ep(p, rate):
    """Schnakenberg sum over unordered pairs: (J_ij - J_ji) ln(k_ij/k_ji)."""
    seen = set()
    total = 0.0
    for (i, j), kij in rate.items():
        if i == j or kij <= 0.0:
            continue
        a, b = (i, j) if i < j else (j, i)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        kab = rate.get((a, b), 0.0)
        kba = rate.get((b, a), 0.0)
        if kab <= 0.0 or kba <= 0.0:
            continue
        jab = p[a] * kab
        jba = p[b] * kba
        total += (jab - jba) * math.log(kab / kba)
    return total


def binary_rates(ac, ae, gamma):
    # states: 0=(X0,M0), 1=(X0,M1), 2=(X1,M0), 3=(X1,M1)
    r = {}
    r[(0, 1)] = ae  # error
    r[(1, 0)] = ac  # correction
    r[(3, 2)] = ae
    r[(2, 3)] = ac
    r[(0, 2)] = gamma
    r[(2, 0)] = gamma
    r[(1, 3)] = gamma
    r[(3, 1)] = gamma
    return r


def sensor_observables(ac, ae, gamma, p=None):
    Z = ac + ae + 2.0 * gamma
    err = (ae + gamma) / Z
    rho = ac / ae
    pref = gamma * (ac - ae) / Z
    heat = pref * math.log(rho)
    flow_formula = pref * math.log((ac + gamma) / (ae + gamma))
    # identity: pref = gamma * (1 - 2*err)
    if p is None:
        p, _G = stationary_from_rates(binary_rates(ac, ae, gamma))
    rates = binary_rates(ac, ae, gamma)
    heat_edge = edge_ep(p, rates)
    # information flow from the definition
    # index map: 0=(X=0,M=0), 1=(X=0,M=1), 2=(X=1,M=0), 3=(X=1,M=1)
    masses = {(0, 0): p[0], (0, 1): p[1], (1, 0): p[2], (1, 1): p[3]}
    pm = {0: p[0] + p[2], 1: p[1] + p[3]}
    px_given_m = {}
    for (x, m), mass in masses.items():
        px_given_m[(x, m)] = mass / pm[m]
    flow = 0.0
    # memory jumps
    jumps = [
        ((0, 0), (0, 1), ae),
        ((0, 1), (0, 0), ac),
        ((1, 1), (1, 0), ae),
        ((1, 0), (1, 1), ac),
    ]
    for (x, m), (x2, m2), k in jumps:
        assert x == x2
        mass = masses[(x, m)]
        ratio = px_given_m[(x, m2)] / px_given_m[(x, m)]
        flow += mass * k * math.log(ratio)
    info = LN2 - hbin(err)
    return {
        "p": p,
        "err": err,
        "Z": Z,
        "heat_formula": heat,
        "heat_edge": heat_edge,
        "flow_formula": flow_formula,
        "flow_def": flow,
        "pref": pref,
        "pref_id": gamma * (1.0 - 2.0 * err),
        "info": info,
        "rho": rho,
    }


def tilted_mean_var(G, increments, dz):
    def lam(z):
        T = G.copy()
        for (i, j), d in increments.items():
            T[i, j] = G[i, j] * math.exp(z * d)
        ev = np.linalg.eigvals(T.T)
        return float(np.max(np.real(ev)))

    # 5-point stencil
    zs = [-2 * dz, -dz, 0.0, dz, 2 * dz]
    L = [lam(z) for z in zs]
    mean = (-L[4] + 8 * L[3] - 8 * L[1] + L[0]) / (12 * dz)
    var = (-L[4] + 16 * L[3] - 30 * L[2] + 16 * L[1] - L[0]) / (12 * dz * dz)
    return mean, var, L[2]


def gillespie_current(ac, ae, gamma, n_jump, seed):
    """Net corrective current: +1 on a correction, -1 on an error."""
    rng = np.random.default_rng(seed)
    # state 0..3
    x, m = 0, 0
    t = 0.0
    count = 0.0
    # integrate count over time by recording the integral of the counting process
    # variance per time of the time-integrated current: use batch means
    batches = 40
    per = n_jump // batches
    totals = []
    times = []
    for b in range(batches):
        c0 = count
        t0 = t
        for _ in range(per):
            if m == x:
                k_m = ae
                sign = -1.0
            else:
                k_m = ac
                sign = 1.0
            k_x = gamma
            k = k_m + k_x
            dt = rng.exponential(1.0 / k)
            t += dt
            if rng.random() < k_m / k:
                m = 1 - m
                count += sign
            else:
                x = 1 - x
        totals.append(count - c0)
        times.append(t - t0)
    totals = np.array(totals)
    times = np.array(times)
    rates = totals / times
    # pooled mean and a rough variance-per-time from batch second moments
    T = times.sum()
    mean = totals.sum() / T
    # Var(integral over batch) / batch_time ≈ var rate, average
    var_est = np.mean((totals - mean * times) ** 2 / times)
    return mean, var_est, T


def lyapunov(A, BB):
    n = A.shape[0]
    M = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(M, -BB.reshape(-1))
    return c.reshape(n, n)


def main():
    print("=== closed form, reference point (4, 0.5, 1) ===")
    ac, ae, g = 4.0, 0.5, 1.0
    o = sensor_observables(ac, ae, g)
    print("err", "%.12f" % o["err"])
    print("heat_formula", "%.12f" % o["heat_formula"])
    print("heat_edge", "%.12e" % (o["heat_edge"] - o["heat_formula"]))
    print("flow_formula", "%.12f" % o["flow_formula"])
    print("flow_def", "%.12e" % (o["flow_def"] - o["flow_formula"]))
    print("pref_minus_id", "%.3e" % (o["pref"] - o["pref_id"]))
    print("info", "%.12f" % o["info"])
    print("p", o["p"])

    # identity on a random cloud, including near the boundary
    rng = np.random.default_rng(19)
    max_gap = 0.0
    for _ in range(200):
        rho = math.exp(rng.uniform(math.log(1.05), math.log(1e6)))
        ae_r = math.exp(rng.uniform(math.log(1e-4), math.log(1e3)))
        g_r = math.exp(rng.uniform(math.log(1e-3), math.log(20)))
        ac_r = rho * ae_r
        oo = sensor_observables(ac_r, ae_r, g_r)
        max_gap = max(
            max_gap,
            abs(oo["heat_formula"] - oo["heat_edge"]),
            abs(oo["flow_formula"] - oo["flow_def"]),
            abs(oo["pref"] - oo["pref_id"]),
            abs(oo["heat_formula"] - g_r * (1 - 2 * oo["err"]) * math.log(rho)),
            abs(oo["flow_formula"] - g_r * (1 - 2 * oo["err"]) * math.log((1 - oo["err"]) / oo["err"])),
        )
    print("max identity gap on 200 random designs", "%.3e" % max_gap)

    print("=== fixed error 0.2 ===")
    eps = 0.2
    gamma = 1.0
    floor = gamma * (1 - 2 * eps) * math.log((1 - eps) / eps)
    print("exact floor", "%.15f" % floor)
    print("0.6*ln4", "%.15f" % (0.6 * math.log(4)))
    # grid minimum the way the note constructs it
    rho_eq = (1 - eps) / eps
    rhos = np.exp(np.linspace(math.log(rho_eq * 1.0001), 40.0, 600))
    heats = []
    for rho in rhos:
        s = gamma * (1 - 2 * eps) / (eps * (rho + 1) - 1)
        oo = sensor_observables(rho * s, s, gamma)
        heats.append(oo["heat_formula"])
        if abs(oo["err"] - eps) > 1e-9:
            raise SystemExit("error not held")
    print("grid min", "%.15f" % min(heats))
    print("Q at ln rho=40", "%.15f" % (gamma * (1 - 2 * eps) * 40.0))
    # approach to the floor
    for fac in (1.0000001, 1.001, 1.1, 2.0):
        rho = rho_eq * fac
        s = gamma * (1 - 2 * eps) / (eps * (rho + 1) - 1)
        oo = sensor_observables(rho * s, s, gamma)
        print("rho/rho*", "%.8f" % fac, "Q", "%.12f" % oo["heat_formula"], "flow", "%.12f" % oo["flow_formula"])

    print("=== efficiencies ===")
    for gg, name in ((1e-4, "slow"), (5.0, "fast"), (1.0, "ref")):
        oo = sensor_observables(4.0, 0.5, gg)
        print(name, "eta", "%.15f" % (oo["flow_formula"] / oo["heat_formula"]), "Q", "%.12f" % oo["heat_formula"], "Iflow", "%.12f" % oo["flow_formula"])

    print("=== TUR ===")
    p, G = stationary_from_rates(binary_rates(4.0, 0.5, 1.0))
    inc = {(1, 0): 1.0, (0, 1): -1.0, (2, 3): 1.0, (3, 2): -1.0}
    for dz in (1e-3, 1e-4, 1e-5):
        mean, var, lam0 = tilted_mean_var(G, inc, dz)
        bound = 2 * mean * mean / var
        print("dz", dz, "j", "%.12f" % mean, "var", "%.12f" % var, "TUR", "%.12f" % bound, "lam0", "%.3e" % lam0)
    flux = 1.0 * (4 - 0.5) / (4 + 0.5 + 2)
    print("flux", "%.12f" % flux, "heat", "%.12f" % sensor_observables(4, 0.5, 1)["heat_formula"])
    # slow gamma
    ps, Gs = stationary_from_rates(binary_rates(4.0, 0.5, 0.05))
    mean_s, var_s, _ = tilted_mean_var(Gs, inc, 1e-4)
    slow = sensor_observables(4.0, 0.5, 0.05)
    bound_s = 2 * mean_s * mean_s / var_s
    print("slow j", "%.12f" % mean_s, "var", "%.12f" % var_s, "TUR", "%.12f" % bound_s)
    print("slow heat", "%.12f" % slow["heat_formula"], "flow", "%.12f" % slow["flow_formula"], "sum", "%.12f" % (slow["flow_formula"] + bound_s))
    gm, gv, TT = gillespie_current(4.0, 0.5, 1.0, 400000, 19)
    print("gillespie mean", "%.6f" % gm, "var_est", "%.6f" % gv, "T", "%.3f" % TT)

    print("=== Still step ===")
    eps_gap = 1.5
    p_flip = 0.3
    q = 1.0 / (1.0 + math.exp(eps_gap))
    err_next = q + p_flip * (1 - q) + (1 - p_flip) * 0  # if no flip, mismatch stays q? 
    # signal flips with prob p_flip: mismatch probability becomes
    # P(mismatch after) = (1-q)*p_flip + q*(1-p_flip) = q + p_flip - 2*q*p_flip
    err_next = q + p_flip - 2 * q * p_flip
    i_mem = LN2 - hbin(q)
    i_pred = LN2 - hbin(err_next)
    i_np = i_mem - i_pred
    gap = hbin(err_next) - hbin(q)
    cycle = p_flip * eps_gap * math.tanh(eps_gap / 2.0)
    print("q", "%.12f" % q, "err_next", "%.12f" % err_next)
    print("I_np", "%.15f" % i_np, "gap", "%.15f" % gap, "cycle", "%.15f" % cycle)
    # free-energy check of the one-step identity
    # equilibrated: P(s matches x) = 1-q, energy 0 if match, eps if mismatch
    # After the signal is replaced by an independent draw that equals the old one with prob 1-p_flip
    # W_diss = H(s | x_next) - H(s | x) by the paper's algebra. Recomputed as entropies.
    print("identity residual", "%.3e" % (i_np - gap))

    print("=== CT7 ===")
    sig, w, kT = 1.7, 2.5, 1.0
    exact = sig * math.sqrt(2 * kT * w)
    D = np.exp(np.linspace(math.log(1e-4), math.log(20), 100000))
    got = float(np.min(kT * sig ** 2 / (2 * D) + w * D))
    print("exact", "%.12f" % exact, "grid", "%.12f" % got)

    print("=== sticky past stock ===")
    # X flip 0.2, redraw 0.3, BSC 0.05. State (xp, x, m)
    p_flip, lam, qq = 0.2, 0.3, 0.05

    def idx(xp, x, m):
        return xp * 4 + x * 2 + m

    P = np.zeros((8, 8))
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = idx(xp, x, m)
                for xn in (0, 1):
                    px = (1 - p_flip) if xn == x else p_flip
                    # keep
                    P[i, idx(x, xn, m)] += px * (1 - lam)
                    for mn in (0, 1):
                        pm = (1 - qq) if mn == xn else qq
                        P[i, idx(x, xn, mn)] += px * lam * pm
    ev, evec = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(ev - 1)))
    pi = np.real(evec[:, k])
    pi = np.clip(pi, 0, None)
    pi /= pi.sum()
    pairs_now, pairs_past = [], []
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                mass = float(pi[idx(xp, x, m)])
                pairs_now.append((x, m, mass))
                pairs_past.append((xp * 2 + x, m, mass))
    I_now = mi_discrete(pairs_now)
    I_past = mi_discrete(pairs_past)
    pairs_next = []
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = idx(xp, x, m)
                for j in range(8):
                    mass = float(pi[i] * P[i, j])
                    xn = (j // 2) % 2
                    pairs_next.append((m, xn, mass))
    I_next = mi_discrete(pairs_next)
    print("I_past", "%.12f" % I_past)
    print("I_now", "%.12f" % I_now)
    print("I_next", "%.12f" % I_next)
    print("past excess", "%.12f" % (I_past - I_next))
    print("still gap", "%.12f" % (I_now - I_next))

    print("=== layers: CI and reversal ===")
    # two BSC, conditional on one fair bit
    def bsc_joint(q1, q2):
        triples = []
        pairs = []
        for x, px in ((0, 0.5), (1, 0.5)):
            for m1 in (0, 1):
                p1 = (1 - q1) if m1 == x else q1
                for m2 in (0, 1):
                    p2 = (1 - q2) if m2 == x else q2
                    triples.append((m1 * 2 + m2, x, 0, px * p1 * p2))  # dummy future
                    pairs.append((m1 * 2 + m2, x, px * p1 * p2))
        return mi_discrete(pairs)

    q1, q2 = 0.1, 0.2
    joint = bsc_joint(q1, q2)
    i1 = LN2 - hbin(q1)
    i2 = LN2 - hbin(q2)
    print("BSC joint", "%.12f" % joint, "sum", "%.12f" % (i1 + i2))

    # XOR reversal of mutual information
    xor_j, xor_1, xor_2 = [], [], []
    for m1 in (0, 1):
        for m2 in (0, 1):
            z = m1 ^ m2
            xor_j.append((m1 * 2 + m2, z, 0.25))
            xor_1.append((m1, z, 0.25))
            xor_2.append((m2, z, 0.25))
    print("XOR joint", "%.12f" % mi_discrete(xor_j), "m1", "%.3e" % mi_discrete(xor_1), "m2", "%.3e" % mi_discrete(xor_2))

    # same XOR with a nontrivial future Y correlated with Z
    # M1 fair, M2 = M1 XOR Z, Y flips from Z with prob 0.2
    # I((M1,M2); Z | Y) versus the sum
    triples_j, triples_1, triples_2 = [], [], []
    for m1 in (0, 1):
        for z in (0, 1):
            m2 = m1 ^ z
            for y, py in ((z, 0.8), (1 - z, 0.2)):
                p = 0.25 * py  # m1,z uniform independent, then y
                triples_j.append((m1 * 2 + m2, z, y, p))
                triples_1.append((m1, z, y, p))
                triples_2.append((m2, z, y, p))
    cj = cmi_from_joint(triples_j)
    c1 = cmi_from_joint(triples_1)
    c2 = cmi_from_joint(triples_2)
    print("CMI reversal joint", "%.12f" % cj, "sum", "%.12f" % (c1 + c2))

    # Still gaps for the same law: I(M; Z) - I(M; Y)
    def still_gap_from(triples):
        # triples (m, z, y, p); gap = I(m;z) - I(m;y)
        pz = [(m, z, p) for m, z, y, p in triples]
        py = [(m, y, p) for m, z, y, p in triples]
        return mi_discrete(pz) - mi_discrete(py)

    print("Still-gap reversal joint", "%.12f" % still_gap_from(triples_j), "sum", "%.12f" % (still_gap_from(triples_1) + still_gap_from(triples_2)))

    # two conditionally independent sticky memories: lemma functional vs Still gap
    pf, lam_s, qs = 0.25, 0.35, 0.08

    def sticky_pair():
        # state (xp, x, m1, m2), 16 states
        def id16(xp, x, m1, m2):
            return ((xp * 2 + x) * 2 + m1) * 2 + m2

        P16 = np.zeros((16, 16))
        for xp in (0, 1):
            for x in (0, 1):
                for m1 in (0, 1):
                    for m2 in (0, 1):
                        i = id16(xp, x, m1, m2)
                        for xn in (0, 1):
                            px = (1 - pf) if xn == x else pf
                            for redraw1 in (0, 1):
                                pr1 = lam_s if redraw1 else (1 - lam_s)
                                m1_choices = (0, 1) if redraw1 else (m1,)
                                for mn1 in m1_choices:
                                    p1 = 1.0 if not redraw1 else ((1 - qs) if mn1 == xn else qs)
                                    for redraw2 in (0, 1):
                                        pr2 = lam_s if redraw2 else (1 - lam_s)
                                        m2_choices = (0, 1) if redraw2 else (m2,)
                                        for mn2 in m2_choices:
                                            p2 = 1.0 if not redraw2 else ((1 - qs) if mn2 == xn else qs)
                                            j = id16(x, xn, mn1, mn2)
                                            P16[i, j] += px * pr1 * p1 * pr2 * p2
        rs = P16.sum(axis=1)
        if abs(rs.min() - 1) > 1e-10 or abs(rs.max() - 1) > 1e-10:
            raise SystemExit("sticky pair not stochastic %s %s" % (rs.min(), rs.max()))
        A = P16.T - np.eye(16)
        A[-1, :] = 1.0
        b = np.zeros(16)
        b[-1] = 1.0
        pi16 = np.linalg.solve(A, b)
        pi16 = np.clip(np.real(pi16), 0, None)
        pi16 /= pi16.sum()
        return P16, pi16, id16

    P16, pi16, id16 = sticky_pair()
    # joint and marginal Still gaps, and the lemma functional on (past=(xp,x), future=x_next)
    # Build one-step joints
    rows_j_now, rows_1_now, rows_2_now = [], [], []
    rows_j_next, rows_1_next, rows_2_next = [], [], []
    cmi_j, cmi_1, cmi_2 = [], [], []
    for xp in (0, 1):
        for x in (0, 1):
            for m1 in (0, 1):
                for m2 in (0, 1):
                    i = id16(xp, x, m1, m2)
                    mass = float(pi16[i])
                    rows_j_now.append((m1 * 2 + m2, x, mass))
                    rows_1_now.append((m1, x, mass))
                    rows_2_now.append((m2, x, mass))
                    for j in range(16):
                        pij = mass * float(P16[i, j])
                        if pij <= 0:
                            continue
                        # next state encoding: ((xp' *2 + x')*2 + m1')*2 + m2'
                        # xp' = old x, x' = new x
                        tmp = j
                        mn2 = tmp % 2
                        tmp //= 2
                        mn1 = tmp % 2
                        tmp //= 2
                        xn = tmp % 2
                        rows_j_next.append((m1 * 2 + m2, xn, pij))
                        rows_1_next.append((m1, xn, pij))
                        rows_2_next.append((m2, xn, pij))
                        past = xp * 2 + x
                        cmi_j.append((m1 * 2 + m2, past, xn, pij))
                        cmi_1.append((m1, past, xn, pij))
                        cmi_2.append((m2, past, xn, pij))
    sj = mi_discrete(rows_j_now) - mi_discrete(rows_j_next)
    s1 = mi_discrete(rows_1_now) - mi_discrete(rows_1_next)
    s2 = mi_discrete(rows_2_now) - mi_discrete(rows_2_next)
    lj = cmi_from_joint(cmi_j)
    l1 = cmi_from_joint(cmi_1)
    l2 = cmi_from_joint(cmi_2)
    print("sticky CI Still joint", "%.8f" % sj, "sum", "%.8f" % (s1 + s2), "delta", "%.8e" % (sj - (s1 + s2)))
    print("sticky CI lemma joint", "%.8f" % lj, "sum", "%.8f" % (l1 + l2), "delta", "%.8e" % (lj - (l1 + l2)))

    print("=== redundant sensors ===")
    def redundant(ac, ae, gamma):
        def id8(x, m1, m2):
            return x * 4 + m1 * 2 + m2

        rate = {}
        for x in (0, 1):
            for m1 in (0, 1):
                for m2 in (0, 1):
                    i = id8(x, m1, m2)
                    rate[(i, id8(1 - x, m1, m2))] = gamma
                    r1 = ac if m1 != x else ae
                    rate[(i, id8(x, 1 - m1, m2))] = rate.get((i, id8(x, 1 - m1, m2)), 0.0) + r1
                    r2 = ac if m2 != x else ae
                    rate[(i, id8(x, m1, 1 - m2))] = rate.get((i, id8(x, m1, 1 - m2)), 0.0) + r2
        p, _G = stationary_from_rates(rate)
        # memory edges only
        mem = {}
        for x in (0, 1):
            for m1 in (0, 1):
                for m2 in (0, 1):
                    i = id8(x, m1, m2)
                    j1 = id8(x, 1 - m1, m2)
                    j2 = id8(x, m1, 1 - m2)
                    mem[(i, j1)] = rate[(i, j1)]
                    mem[(i, j2)] = rate[(i, j2)]
        heat = edge_ep(p, mem)
        pairs = []
        for x in (0, 1):
            for m1 in (0, 1):
                for m2 in (0, 1):
                    pairs.append((m1 * 2 + m2, x, float(p[id8(x, m1, m2)])))
        return heat, mi_discrete(pairs)

    h2, ij = redundant(4.0, 0.5, 1.0)
    one = sensor_observables(4.0, 0.5, 1.0)
    print("heat2", "%.12f" % h2, "2*heat", "%.12f" % (2 * one["heat_formula"]))
    print("Ijoint", "%.12f" % ij, "2I", "%.12f" % (2 * one["info"]), "delta", "%.12f" % (ij - one["info"]))

    print("=== sum tracker ===")
    def sum_tracker(ac, ae, gamma):
        def id9(S, M):
            return 3 * S + M

        sig = {(0, 1): 2 * gamma, (2, 1): 2 * gamma, (1, 0): gamma, (1, 2): gamma}
        rate = {}
        for S in range(3):
            for M in range(3):
                i = id9(S, M)
                for (a, b), rr in sig.items():
                    if a == S:
                        rate[(i, id9(b, M))] = rate.get((i, id9(b, M)), 0.0) + rr
                for Mp in (M - 1, M + 1):
                    if Mp < 0 or Mp > 2:
                        continue
                    toward = abs(Mp - S) < abs(M - S)
                    rate[(i, id9(S, Mp))] = rate.get((i, id9(S, Mp)), 0.0) + (ac if toward else ae)
        p, _G = stationary_from_rates(rate)
        mem = {}
        for S in range(3):
            for M in range(3):
                for Mp in range(3):
                    if M != Mp and (id9(S, M), id9(S, Mp)) in rate:
                        mem[(id9(S, M), id9(S, Mp))] = rate[(id9(S, M), id9(S, Mp))]
        heat = edge_ep(p, mem)
        mse = 0.0
        for S in range(3):
            for M in range(3):
                mse += float(p[id9(S, M)]) * (M - S) ** 2
        return heat, mse

    hj, mj = sum_tracker(6.0, 0.4, 0.5)
    one_s = sensor_observables(6.0, 0.4, 0.5)
    # two specialized: MSE = 2*err because errors are 0/1 and independent, mean zero
    mse_pair = 2 * one_s["err"]
    # cross-check by enumeration
    mse_enum = 0.0
    err = one_s["err"]
    for x1 in (0, 1):
        for x2 in (0, 1):
            for e1 in (0, 1):
                for e2 in (0, 1):
                    prob = 0.25 * (err if e1 else 1 - err) * (err if e2 else 1 - err)
                    M1 = x1 if e1 == 0 else 1 - x1
                    M2 = x2 if e2 == 0 else 1 - x2
                    mse_enum += prob * (M1 + M2 - (x1 + x2)) ** 2
    hw, _mw = sum_tracker(1.2, 1.0, 0.5)
    print("joint heat", "%.12f" % hj, "mse", "%.12f" % mj)
    print("pair heat", "%.12f" % (2 * one_s["heat_formula"]), "mse", "%.12f" % mse_pair, "enum", "%.12f" % mse_enum)
    print("weak heat", "%.12f" % hw)

    print("=== OU ===")
    def ou_one(a, lam, v, D):
        A = np.array([[-a, 0.0], [lam, -lam]], dtype=float)
        BB = np.diag([2 * a * v, 2 * D]).astype(float)
        C = lyapunov(A, BB)
        Cxx, Cxm, Cmm = C[0, 0], C[0, 1], C[1, 1]
        det = Cxx * Cmm - Cxm ** 2
        info = 0.5 * math.log(Cxx * Cmm / det)
        Cinv = np.linalg.inv(C)
        b = np.array([lam, -lam]) + D * Cinv[:, 1]
        sigma = float(b @ C @ b) / D
        err = Cxx + Cmm - 2 * Cxm
        # Sekimoto Stratonovich expectation
        seki = (lam ** 2 / D) * err - lam
        return C, info, sigma, err, seki

    C, info, sigma, err, seki = ou_one(1.0, 2.0, 1.0, 0.3)
    print("Cxm", "%.12f" % C[0, 1], "formula", "%.12f" % (2 * 1 / 3))
    print("err", "%.12f" % err, "formula", "%.12f" % (1 * 1 / 3 + 0.3 / 2))
    print("info", "%.12f" % info)
    print("partial EP", "%.12f" % sigma)
    print("Sekimoto analytic", "%.12f" % seki)
    # equilibrium cancellation
    print("eq drift cancel", -2.0 + 0.3 * (2.0 / 0.3))

    modes = [(0.5, 1.0, 1.0, 0.2), (1.5, 3.0, 0.8, 0.4), (4.0, 2.0, 1.2, 0.5)]
    sig = info_sum = 0.0
    parts = []
    for aa, ll, vv, dd in modes:
        _C, ii, ss, _e, _k = ou_one(aa, ll, vv, dd)
        sig += ss
        info_sum += ii
        parts.append((ss, ii))
    print("K3 sigma", "%.12f" % sig, "I", "%.12f" % info_sum, "parts", parts)

    # redundant OU
    a, lam, v, D = 1.0, 2.0, 1.0, 0.3
    A = np.array([[-a, 0, 0], [lam, -lam, 0], [lam, 0, -lam]], dtype=float)
    BB = np.diag([2 * a * v, 2 * D, 2 * D]).astype(float)
    C3 = lyapunov(A, BB)
    Cinv = np.linalg.inv(C3)

    def partial(i_m):
        b = np.zeros(3)
        b[0] = lam
        b[i_m] = -lam
        b = b + D * Cinv[:, i_m]
        return float(b @ C3 @ b) / D

    s1, s2 = partial(1), partial(2)
    CXX = C3[0, 0]
    Cmx = C3[1:, 0:1]
    Cmm = C3[1:, 1:]
    schur = CXX - float(np.asarray(Cmx.T @ np.linalg.inv(Cmm) @ Cmx).reshape(-1)[0])
    Ij = 0.5 * math.log(CXX / schur)
    print("red sigma", "%.12f" % s1, "%.12f" % s2, "sum", "%.12f" % (s1 + s2))
    print("Ijoint", "%.12f" % Ij, "Ione", "%.12f" % info)

    # path, their seed, short, plus a longer independent seed for the mean
    def seki_path(seed, nstep, dt=2e-3, burn=2000):
        rng = np.random.default_rng(seed)
        kappa = lam / D
        x = m = 0.0
        heat = 0.0
        sig_x = math.sqrt(2 * a * v * dt)
        sig_m = math.sqrt(2 * D * dt)
        for t in range(nstep + burn):
            x_new = x - a * x * dt + rng.normal() * sig_x
            m_new = m + (-lam * (m - x)) * dt + rng.normal() * sig_m
            if t >= burn:
                F = -kappa * (0.5 * (m + m_new) - 0.5 * (x + x_new))
                heat += F * (m_new - m)
            x, m = x_new, m_new
        return heat / (nstep * dt)

    print("path seed7 n=20000", "%.8f" % seki_path(7, 20000))
    print("path seed11 n=200000", "%.8f" % seki_path(11, 200000, burn=5000))

    print("=== tangent ===")
    gamma = 1.0
    Fs = np.linspace(0.3, 6.0, 40)
    rs = np.exp(np.linspace(math.log(0.05), math.log(30.0), 40))
    rows = []
    for F in Fs:
        for r in rs:
            ac = r * math.exp(0.5 * F)
            ae = r * math.exp(-0.5 * F)
            oo = sensor_observables(float(ac), float(ae), gamma)
            rows.append((oo["heat_formula"], oo["err"], oo["info"], oo["flow_formula"], float(F), float(r), oo["rho"]))
    rows = np.array(rows)
    w = 8.0
    phys = rows[:, 0] + w * rows[:, 1]
    flow_obj = rows[:, 3] + w * rows[:, 1]
    ip = int(np.argmin(phys))
    iff = int(np.argmin(flow_obj))
    print("phys err", "%.12f" % rows[ip, 1], "heat", "%.12f" % rows[ip, 0], "flow", "%.12f" % rows[ip, 3], "F", rows[ip, 4], "r", rows[ip, 5])
    print("flow obj err", "%.12f" % rows[iff, 1], "heat", "%.12f" % rows[iff, 0], "flow", "%.12f" % rows[iff, 3], "F", rows[iff, 4], "r", rows[iff, 5])
    print("same index", ip == iff, "err gap", abs(rows[ip, 1] - rows[iff, 1]))

    # continuous frontier optimum of Qmin(eps)+w*eps = flow(eps)+w*eps
    def gp(e):
        L = math.log((1 - e) / e)
        return -2 * L - (1 - 2 * e) / (e * (1 - e)) + w

    lo, hi = 1e-4, 0.49
    print("gp(0.05)", gp(0.05), "gp(0.4)", gp(0.4))
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if gp(mid) > 0:
            hi = mid
        else:
            lo = mid
    e_star = 0.5 * (lo + hi)
    q_star = (1 - 2 * e_star) * math.log((1 - e_star) / e_star)
    print("continuous frontier err", "%.12f" % e_star, "Qmin", "%.12f" % q_star, "gp", "%.3e" % gp(e_star))

    def standin_err(kappa):
        jay = kappa * rows[:, 2] + w * rows[:, 1]
        k = int(np.argmin(jay))
        return k, rows[k, 1], rows[k, 0], rows[k, 2]

    for kappa, h in ((1.5, 0.4), (1.0, 0.0), (1.0, 10.0), (5.0, 0.0)):
        k, e, q, I = standin_err(kappa)
        # h does not enter the argmin; record it
        print("kappa", kappa, "h", h, "err", "%.12f" % e, "heat", "%.6f" % q, "I", "%.6f" % I, "index_match_phys", k == ip)

    # kappa that matches the continuous error, and the grid error
    def kappa_for(e):
        return w / math.log((1 - e) / e)

    for label, e in (("continuous", e_star), ("grid phys", rows[ip, 1])):
        kap = kappa_for(e)
        k, ee, q, I = standin_err(kap)
        print(label, "kappa", "%.6f" % kap, "selected err", "%.12f" % ee, "target", "%.12f" % e, "same point as phys", k == ip)

    # best kappa on a grid: closest error, and whether the point matches
    best = None
    for kap in np.linspace(0.2, 30.0, 2000):
        k, ee, q, I = standin_err(float(kap))
        dist = abs(ee - rows[ip, 1])
        if best is None or dist < best[0]:
            best = (dist, float(kap), ee, k == ip, q)
    print("best kappa error-match", best)

    # shape: can kappa*I + h equal Qmin up to a constant, on a dense eps grid?
    es = np.linspace(0.02, 0.45, 400)
    Qmin = (1 - 2 * es) * np.log((1 - es) / es)
    Istock = np.array([LN2 - hbin(e) for e in es])
    # least squares Qmin ≈ kappa * Istock + h
    A = np.column_stack([Istock, np.ones_like(Istock)])
    coef, *_ = np.linalg.lstsq(A, Qmin, rcond=None)
    resid = Qmin - A @ coef
    print("lsq kappa", coef[0], "h", coef[1], "max abs resid", float(np.max(np.abs(resid))), "rms", float(np.sqrt(np.mean(resid ** 2))))

    # J at kappa=1.5, h=0.4, the reported point
    k, e, q, I = standin_err(1.5)
    feas = rows[rows[:, 1] <= e + 1e-12]
    print("J point heat", q, "Qmin among no-worse error", float(feas[:, 0].min()), "ratio", q / float(feas[:, 0].min()))

    # does flow objective's cost equal phys cost at the phys point, and is phys on the frontier?
    print("phys excess heat over flow", rows[ip, 0] - rows[ip, 3])
    print("flow-obj excess heat over its own flow", rows[iff, 0] - rows[iff, 3])

    print("=== one kappa across stakes ===")
    # continuous stand-in eps = 1/(1+exp(w/kappa)); frontier root of gp
    def frontier(wstake):
        a, b = 1e-6, 0.499
        for _ in range(80):
            m = 0.5 * (a + b)
            L = math.log((1 - m) / m)
            gpm = -2 * L - (1 - 2 * m) / (m * (1 - m)) + wstake
            if gpm > 0:
                b = m
            else:
                a = m
        return 0.5 * (a + b)

    kap_match = w / math.log((1 - rows[ip, 1]) / rows[ip, 1])
    print("kappa matched to grid phys at w=8", "%.6f" % kap_match)
    for wstake in (2.0, 8.0, 20.0):
        ef = frontier(wstake)
        es = 1.0 / (1.0 + math.exp(wstake / kap_match))
        es_kT = 1.0 / (1.0 + math.exp(wstake / 1.0))
        print("w", wstake, "frontier", "%.6f" % ef, "stock at matched kappa", "%.6f" % es, "stock at kT", "%.6f" % es_kT)


if __name__ == "__main__":
    main()
