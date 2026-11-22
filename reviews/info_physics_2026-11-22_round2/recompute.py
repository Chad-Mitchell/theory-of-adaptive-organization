#!/usr/bin/env python3
"""Independent recomputation for the second review of draft PR #175.

Nothing in this file imports theory/info_physics_checks or any other module
from the repository. Rates, the stationary law, the entropy production, the
information flow, the spring covariances, and the stake minima are derived
here. Crossref lookups are optional and run only when --crossref is passed.
"""

from __future__ import annotations

import json
import math
import sys
import urllib.request

import numpy as np


def binary_entropy(p):
    p = float(p)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def telegraph_generator(alpha_c, alpha_e, gamma):
    """Row generator on states (X, M) = 00, 01, 10, 11.

    X flips at rate gamma either way. M moves toward X at alpha_c and away
    from X at alpha_e. The undirected graph is the 4-cycle
    00—01—11—10—00.
    """
    G = np.zeros((4, 4))
    G[0, 1] = alpha_e
    G[0, 2] = gamma
    G[1, 0] = alpha_c
    G[1, 3] = gamma
    G[2, 0] = gamma
    G[2, 3] = alpha_c
    G[3, 1] = gamma
    G[3, 2] = alpha_e
    G[np.arange(4), np.arange(4)] = -G.sum(axis=1)
    return G


def stationary(G):
    A = G.T.copy()
    A[-1, :] = 1.0
    b = np.zeros(G.shape[0])
    b[-1] = 1.0
    p = np.linalg.solve(A, b)
    p = np.real(p)
    p = np.clip(p, 0.0, None)
    p /= p.sum()
    return p


def edge_entropy_production(p, G):
    """Schnakenberg sum over directed edges, nats per unit time, kT = 1."""
    total = 0.0
    n = len(p)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            kij = G[i, j]
            kji = G[j, i]
            if kij > 0.0 and kji > 0.0:
                total += p[i] * kij * math.log(kij / kji)
    return total


def memory_edge_production(p, G):
    """Same sum restricted to the two memory edges."""
    pairs = ((0, 1), (1, 0), (2, 3), (3, 2))
    total = 0.0
    for i, j in pairs:
        kij = G[i, j]
        kji = G[j, i]
        if kij > 0.0 and kji > 0.0:
            total += p[i] * kij * math.log(kij / kji)
    return total


def signal_edge_production(p, G):
    pairs = ((0, 2), (2, 0), (1, 3), (3, 1))
    total = 0.0
    for i, j in pairs:
        kij = G[i, j]
        kji = G[j, i]
        if kij > 0.0 and kji > 0.0:
            total += p[i] * kij * math.log(kij / kji)
    return total


def mutual_information_binary(p):
    """I(X; M) from the four-state law. State order 00, 01, 10, 11."""
    px = np.array([p[0] + p[1], p[2] + p[3]])
    pm = np.array([p[0] + p[2], p[1] + p[3]])
    joint = np.array([[p[0], p[1]], [p[2], p[3]]])
    info = 0.0
    for x in (0, 1):
        for m in (0, 1):
            mass = joint[x, m]
            if mass > 0.0:
                info += mass * math.log(mass / (px[x] * pm[m]))
    return info


def learning_rate_from_jumps(p, G):
    """Information flow carried by memory jumps.

    For a bipartite continuous-time chain the memory's contribution to the
    mutual-information balance is

        sum_{x,m,m'} p(x,m) W(m -> m' | x) ln( p(x | m') / p(x | m) ).

    In stationarity this equals the rate at which signal jumps destroy
    mutual information. It is the quantity bounded by the memory-edge
    entropy production.
    """
    # p(x | m): m = 0 collects states 00 and 10; m = 1 collects 01 and 11.
    pm = np.array([p[0] + p[2], p[1] + p[3]])
    # conditional p(x=1 | m)
    p_x1_given_m = np.array([
        p[2] / pm[0],
        p[3] / pm[1],
    ])

    def ln_ratio(x, m_from, m_to):
        # p(x | m) for x in {0, 1}
        def pc(x_value, m_value):
            return (1.0 - p_x1_given_m[m_value]) if x_value == 0 else p_x1_given_m[m_value]
        a = pc(x, m_to)
        b = pc(x, m_from)
        return math.log(a / b)

    # State index: x * 2 + m, with the generator's order 00, 01, 10, 11
    # which is (x, m) = (0,0), (0,1), (1,0), (1,1). Index = x * 2 + (1 if m else 0)? 
    # 00 -> 0, 01 -> 1, 10 -> 2, 11 -> 3, so index = x * 2 + m.
    total = 0.0
    for x in (0, 1):
        for m in (0, 1):
            i = x * 2 + m
            for m2 in (0, 1):
                if m2 == m:
                    continue
                j = x * 2 + m2
                rate = G[i, j]
                if rate <= 0.0:
                    continue
                total += p[i] * rate * ln_ratio(x, m, m2)
    return total


def closed_forms(alpha_c, alpha_e, gamma):
    Z = alpha_c + alpha_e + 2.0 * gamma
    eps = (alpha_e + gamma) / Z
    pref = gamma * (alpha_c - alpha_e) / Z
    heat = pref * math.log(alpha_c / alpha_e)
    flow = pref * math.log((alpha_c + gamma) / (alpha_e + gamma))
    return eps, heat, flow, pref


def cycle_facts(alpha_c, alpha_e, gamma):
    """One directed cycle 00 -> 01 -> 11 -> 10 -> 00 and its reverse.

    Forward rates: alpha_e, gamma, alpha_e, gamma.
    Reverse rates: alpha_c, gamma, alpha_c, gamma.
    """
    forward = alpha_e * gamma * alpha_e * gamma
    reverse = alpha_c * gamma * alpha_c * gamma
    affinity = math.log(reverse / forward)  # corrective direction
    # undirected edges and vertices
    n_vertices = 4
    n_edges = 4  # the square
    cycle_dim = n_edges - n_vertices + 1
    return {
        "cycle_dimension": cycle_dim,
        "affinity_corrective": affinity,
        "edge_log_ratio": math.log(alpha_c / alpha_e),
    }


def fixed_error_rates(eps, rho, gamma):
    """alpha_e, alpha_c realizing Hamming error eps at rate ratio rho."""
    alpha_e = gamma * (1.0 - 2.0 * eps) / (eps * (rho + 1.0) - 1.0)
    alpha_c = rho * alpha_e
    return alpha_c, alpha_e


def frontier_error(w):
    """Root of d/dε [(1-2ε) ln((1-ε)/ε) + w ε] = 0."""
    lo, hi = 1e-12, 0.5 - 1e-15
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        L = math.log((1.0 - mid) / mid)
        slope = -2.0 * L - (1.0 - 2.0 * mid) / (mid * (1.0 - mid)) + w
        if slope > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def stock_error(w, kappa):
    return 1.0 / (1.0 + math.exp(w / kappa))


# ---------------------------------------------------------------- spring
def lyapunov_covariance(A, diffusion):
    """Solve A C + C A^T + diffusion = 0. diffusion is the noise covariance rate."""
    n = A.shape[0]
    M = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(M, -diffusion.reshape(-1))
    C = c.reshape(n, n)
    return 0.5 * (C + C.T)


def spring_moments(a, lam, v, D):
    """Stationary law of dX = -a X dt + sqrt(2 a v) dW,
    dM = -lam (M - X) dt + sqrt(2 D) dB, kT = 1.

    The Sekimoto heat into the memory bath is the steady expectation of
    F ∘ dM, with F = -(lam/D) (M - X). The Ito drift contributes
    (lam^2/D) E[(M-X)^2]; the quadratic covariation of F with M contributes
    -lam. The information flow is the memory current contracted with the
    gradient of the pointwise mutual information,

        E[ v_m * d/dM ln(p / (p_X p_M)) ],

    and the Fokker-Planck partial entropy production is E[v_m^2] / D.
    """
    A = np.array([[-a, 0.0], [lam, -lam]])
    BB = np.diag([2.0 * a * v, 2.0 * D])
    C = lyapunov_covariance(A, BB)
    Cxx, Cxm, Cmm = C[0, 0], C[0, 1], C[1, 1]
    err = Cxx + Cmm - 2.0 * Cxm
    det = Cxx * Cmm - Cxm ** 2
    info = 0.5 * math.log(Cxx * Cmm / det)
    Cinv = np.linalg.inv(C)
    # v_m = f_m - D d(ln p)/dM, f_m = lam X - lam M, d(ln p)/dM = -(Cinv z)_M
    alpha = np.array([lam, -lam]) + D * Cinv[:, 1]
    beta = -Cinv[:, 1].copy()
    beta[1] += 1.0 / Cmm
    flow = float(alpha @ C @ beta)
    sigma = float(alpha @ C @ alpha) / D
    heat = (lam ** 2 / D) * err - lam
    return {
        "Cxx": Cxx,
        "Cxm": Cxm,
        "Cmm": Cmm,
        "err": err,
        "info": info,
        "heat": heat,
        "flow": flow,
        "sigma": sigma,
    }


def spring_at_error(a, lam, v, eps):
    slack = eps - (a * v) / (a + lam)
    if slack <= 1e-15:
        return None
    D = lam * slack
    row = spring_moments(a, lam, v, D)
    row["D"] = D
    row["lam"] = lam
    return row


def heat_fixed_error_formula(a, lam, v, eps):
    return lam * a * v / (eps * (a + lam) - a * v)


def heat_derivative_sign_factor(eps, v):
    """dQ/dλ has the sign of (ε - v), for ε above the lag floor."""
    return eps - v


def kalman_inflow(a, v, eps):
    """Duncan / PD7 rate for dX = -a X dt + sqrt(2 a v) dW.

    The diffusion coefficient satisfies σ^2 = 2 a v and the relaxation is a,
    so σ^2 / (2 ε) - a = a (v - ε) / ε.
    """
    return a * (v - eps) / eps


def ou_design(a, v, w):
    """Minimize av/ε + w ε against the blind corner (heat 0, error v)."""
    blind_cost = w * v
    e_star = math.sqrt(a * v / w)
    track_cost = a * v / e_star + w * e_star
    if e_star >= v or track_cost >= blind_cost:
        return v, 0.0, blind_cost, "blind"
    return e_star, a * v / e_star, track_cost, "track"


def path_sekimoto(a, lam, v, D, seed, dt, nstep, burn):
    """Stratonovich (midpoint) integral of F dM, same noise construction
    as a seeded normal increment. Written here, not imported.
    """
    rng = np.random.default_rng(seed)
    kappa = lam / D
    x = 0.0
    m = 0.0
    heat = 0.0
    sig_x = math.sqrt(2.0 * a * v * dt)
    sig_m = math.sqrt(2.0 * D * dt)
    for t in range(nstep + burn):
        dWx = rng.normal() * sig_x
        dBm = rng.normal() * sig_m
        x_new = x - a * x * dt + dWx
        m_new = m + (-lam * (m - x)) * dt + dBm
        if t >= burn:
            F = -kappa * (0.5 * (m + m_new) - 0.5 * (x + x_new))
            heat += F * (m_new - m)
        x, m = x_new, m_new
    return heat / (nstep * dt)


def conditional_mutual_information(triples):
    """I(A; B | C) from a list of (a, b, c, probability)."""
    pabc, pac, pbc, pc = {}, {}, {}, {}
    for a, b, c, p in triples:
        pabc[(a, b, c)] = pabc.get((a, b, c), 0.0) + p
        pac[(a, c)] = pac.get((a, c), 0.0) + p
        pbc[(b, c)] = pbc.get((b, c), 0.0) + p
        pc[c] = pc.get(c, 0.0) + p
    out = 0.0
    for (a, b, c), p in pabc.items():
        out += p * math.log((p * pc[c]) / (pac[(a, c)] * pbc[(b, c)]))
    return out


def xor_future():
    joint, one, two = [], [], []
    for m1 in (0, 1):
        for z in (0, 1):
            m2 = m1 ^ z
            for y, py in ((z, 0.8), (1 - z, 0.2)):
                p = 0.25 * py
                joint.append((m1 * 2 + m2, z, y, p))
                one.append((m1, z, y, p))
                two.append((m2, z, y, p))
    return (
        conditional_mutual_information(joint),
        conditional_mutual_information(one),
        conditional_mutual_information(two),
    )


def sticky_numbers(p_flip=0.2, lam=0.3, q=0.05):
    """Discrete-time sticky memory. X flips with probability p_flip.
    With probability lam the memory is redrawn as a binary channel of X
    with flip probability q; otherwise it is kept.
    """
    def idx(xp, x, m):
        return xp * 4 + x * 2 + m

    P = np.zeros((8, 8))
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = idx(xp, x, m)
                for xn in (0, 1):
                    px = (1.0 - p_flip) if xn == x else p_flip
                    P[i, idx(x, xn, m)] += px * (1.0 - lam)
                    for mn in (0, 1):
                        pm = (1.0 - q) if mn == xn else q
                        P[i, idx(x, xn, mn)] += px * lam * pm
    ev, evec = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(ev - 1.0)))
    pi = np.real(evec[:, k])
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()

    def mi(label_a, label_b):
        masses, pa, pb = {}, {}, {}
        for xp in (0, 1):
            for x in (0, 1):
                for m in (0, 1):
                    p = float(pi[idx(xp, x, m)])
                    a = label_a(xp, x, m)
                    b = label_b(xp, x, m)
                    masses[(a, b)] = masses.get((a, b), 0.0) + p
                    pa[a] = pa.get(a, 0.0) + p
                    pb[b] = pb.get(b, 0.0) + p
        out = 0.0
        for (a, b), p in masses.items():
            if p > 0.0:
                out += p * math.log(p / (pa[a] * pb[b]))
        return out

    I_now = mi(lambda xp, x, m: x, lambda xp, x, m: m)
    I_past = mi(lambda xp, x, m: xp * 2 + x, lambda xp, x, m: m)
    masses = {}
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = idx(xp, x, m)
                for j in range(8):
                    p = float(pi[i] * P[i, j])
                    if p <= 0.0:
                        continue
                    xn = (j // 2) % 2
                    masses[(m, xn)] = masses.get((m, xn), 0.0) + p
    pa, pb = {}, {}
    I_next = 0.0
    for (a, b), p in masses.items():
        pa[a] = pa.get(a, 0.0) + p
        pb[b] = pb.get(b, 0.0) + p
    for (a, b), p in masses.items():
        I_next += p * math.log(p / (pa[a] * pb[b]))
    return I_past, I_now, I_next


def printed_grid(gamma=1.0):
    Fs = np.linspace(0.3, 6.0, 40)
    rs = np.exp(np.linspace(math.log(0.05), math.log(30.0), 40))
    rows = []
    for F in Fs:
        for r in rs:
            alpha_c = float(r * math.exp(0.5 * F))
            alpha_e = float(r * math.exp(-0.5 * F))
            G = telegraph_generator(alpha_c, alpha_e, gamma)
            p = stationary(G)
            heat = memory_edge_production(p, G)
            flow = learning_rate_from_jumps(p, G)
            err = p[1] + p[2]
            info = mutual_information_binary(p)
            rows.append((heat, err, info, flow, float(F), float(r)))
    return np.array(rows)


def stock_fit_residual():
    es = np.linspace(0.02, 0.45, 400)
    Q = (1.0 - 2.0 * es) * np.log((1.0 - es) / es)
    I = np.array([math.log(2.0) - binary_entropy(float(e)) for e in es])
    A = np.column_stack([I, np.ones_like(I)])
    coef, *_ = np.linalg.lstsq(A, Q, rcond=None)
    resid = Q - A @ coef
    return float(np.max(np.abs(resid))), coef


DOIS = [
    "10.1147/rd.53.0183",
    "10.1103/RevModPhys.48.571",
    "10.1137/0119020",
    "10.1103/PhysRevLett.102.250602",
    "10.1103/PhysRevLett.106.189901",
    "10.1209/0295-5075/95/40004",
    "10.1103/PhysRevLett.109.120604",
    "10.1103/PhysRevLett.109.180602",
    "10.1038/nphys2276",
    "10.1073/pnas.1207814109",
    "10.1088/0034-4885/75/12/126001",
    "10.1103/PhysRevLett.111.180603",
    "10.1088/1367-2630/16/10/103024",
    "10.1103/PhysRevLett.113.258102",
    "10.1103/PhysRevX.4.031015",
    "10.1371/journal.pcbi.1003974",
    "10.1109/TAC.2004.834430",
    "10.1103/PhysRevLett.114.158101",
    "10.1038/nphys3230",
    "10.1103/PhysRevLett.116.120601",
    "10.1103/PhysRevX.7.021004",
    "10.1103/PhysRevLett.118.158103",
    "10.1103/PhysRevLett.124.050601",
]


def crossref_one(doi):
    url = "https://api.crossref.org/works/" + doi
    req = urllib.request.Request(url, headers={"User-Agent": "info-physics-review-round2/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.status
        payload = json.loads(resp.read().decode("utf-8"))
    msg = payload["message"]
    title = msg.get("title", [""])[0]
    year = None
    issued = msg.get("issued", {}).get("date-parts", [[None]])
    if issued and issued[0]:
        year = issued[0][0]
    authors = []
    for person in msg.get("author", []):
        authors.append(person.get("family", ""))
    container = msg.get("container-title", [""])
    container = container[0] if container else ""
    return status, year, title, authors, container


def main():
    np.set_printoptions(precision=16)
    out = []

    def emit(key, value):
        if isinstance(value, float):
            line = "%s\t%.12g" % (key, value)
        else:
            line = "%s\t%s" % (key, value)
        out.append(line)
        print(line)

    # ----- telegraph identity on random designs -----
    rng = np.random.default_rng(19)
    max_gap = 0.0
    for _ in range(200):
        alpha_e = float(rng.uniform(0.05, 3.0))
        alpha_c = alpha_e * float(rng.uniform(1.1, 30.0))
        gamma = float(rng.uniform(0.05, 5.0))
        G = telegraph_generator(alpha_c, alpha_e, gamma)
        p = stationary(G)
        eps_num = p[1] + p[2]
        heat = memory_edge_production(p, G)
        flow = learning_rate_from_jumps(p, G)
        eps_c, heat_c, flow_c, pref = closed_forms(alpha_c, alpha_e, gamma)
        pref_id = gamma * (1.0 - 2.0 * eps_num)
        max_gap = max(
            max_gap,
            abs(eps_num - eps_c),
            abs(heat - heat_c),
            abs(flow - flow_c),
            abs(pref - pref_id),
            abs(edge_entropy_production(p, G) - heat),
            abs(signal_edge_production(p, G)),
        )
    emit("random_identity_max_gap", max_gap)

    # reference point
    G = telegraph_generator(4.0, 0.5, 1.0)
    p = stationary(G)
    emit("ref_err", p[1] + p[2])
    emit("ref_heat", memory_edge_production(p, G))
    emit("ref_flow", learning_rate_from_jumps(p, G))
    emit("ref_info", mutual_information_binary(p))
    emit("ref_signal_ep", signal_edge_production(p, G))
    cyc = cycle_facts(4.0, 0.5, 1.0)
    emit("cycle_dimension", cyc["cycle_dimension"])
    emit("cycle_affinity", cyc["affinity_corrective"])
    emit("edge_log_ratio", cyc["edge_log_ratio"])
    emit("ln64", math.log(64.0))
    emit("ln8", math.log(8.0))

    # fixed error
    eps, gamma = 0.2, 1.0
    rho_star = (1.0 - eps) / eps
    floor = gamma * (1.0 - 2.0 * eps) * math.log(rho_star)
    emit("floor_exact", floor)
    emit("floor_0.6_ln4", 0.6 * math.log(4.0))
    emit("floor_rounded_12dp", round(floor, 12))
    # excess identity
    excess_gap = 0.0
    for rho in (4.01, 8.0, math.exp(2.0), math.exp(40.0)):
        ac, ae = fixed_error_rates(eps, rho, gamma)
        G = telegraph_generator(ac, ae, gamma)
        p = stationary(G)
        heat = memory_edge_production(p, G)
        flow = learning_rate_from_jumps(p, G)
        excess = gamma * (1.0 - 2.0 * eps) * math.log(rho / rho_star)
        excess_gap = max(
            excess_gap,
            abs(heat - gamma * (1.0 - 2.0 * eps) * math.log(rho)),
            abs(flow - floor),
            abs(heat - flow - excess),
            abs((p[1] + p[2]) - eps),
        )
    emit("excess_identity_max_gap", excess_gap)
    ac, ae = fixed_error_rates(eps, math.exp(40.0), gamma)
    G = telegraph_generator(ac, ae, gamma)
    p = stationary(G)
    emit("heat_lnrho_40", memory_edge_production(p, G))
    emit("info_err_0.2", mutual_information_binary(p))
    # 600-point ray
    rho_grid0 = rho_star * 1.0001
    emit("grid_min_closed_form", gamma * (1.0 - 2.0 * eps) * math.log(rho_grid0))
    rhos = np.exp(np.linspace(math.log(rho_grid0), 40.0, 600))
    heats = []
    for rho in rhos:
        ac, ae = fixed_error_rates(eps, float(rho), gamma)
        Gc = telegraph_generator(ac, ae, gamma)
        pc = stationary(Gc)
        heats.append(memory_edge_production(pc, Gc))
    emit("grid_min_600_from_generator", float(min(heats)))
    emit("grid_min_minus_floor", float(min(heats)) - floor)

    # ratios at the printed speeds
    for gamma_r, name in ((1e-4, "slow"), (5.0, "fast")):
        Gc = telegraph_generator(4.0, 0.5, gamma_r)
        pc = stationary(Gc)
        h = memory_edge_production(pc, Gc)
        f = learning_rate_from_jumps(pc, Gc)
        emit("eta_" + name, f / h)

    # stake table and printed grid
    rows = printed_grid(1.0)
    w = 8.0
    ip = int(np.argmin(rows[:, 0] + w * rows[:, 1]))
    iff = int(np.argmin(rows[:, 3] + w * rows[:, 1]))
    emit("grid_heat_err", float(rows[ip, 1]))
    emit("grid_flow_err", float(rows[iff, 1]))
    emit("grid_argmin_gap", abs(float(rows[ip, 1] - rows[iff, 1])))
    emit("grid_heat_at_argmin", float(rows[ip, 0]))
    emit("grid_flow_at_heat_argmin", float(rows[ip, 3]))
    emit("grid_r_at_heat_argmin", float(rows[ip, 5]))
    e_phys = float(rows[ip, 1])
    kappa = w / math.log((1.0 - e_phys) / e_phys)
    emit("kappa", kappa)
    kmatch = int(np.argmin(kappa * rows[:, 2] + w * rows[:, 1]))
    emit("kappa_selects_heat_argmin", int(kmatch == ip))
    for wstake in (2.0, 8.0, 20.0, 50.0):
        ef = frontier_error(wstake)
        es = stock_error(wstake, kappa)
        emit("front_w%g" % wstake, ef)
        emit("stock_w%g" % wstake, es)
    resid, coef = stock_fit_residual()
    emit("stock_fit_max_resid", resid)
    emit("stock_fit_kappa", float(coef[0]))
    emit("stock_fit_h", float(coef[1]))

    # constant upkeep does not move the argmin
    e0 = float(rows[int(np.argmin(1.0 * rows[:, 2] + 0.0 + w * rows[:, 1])), 1])
    e10 = float(rows[int(np.argmin(1.0 * rows[:, 2] + 10.0 + w * rows[:, 1])), 1])
    emit("upkeep_err_h0", e0)
    emit("upkeep_err_h10", e10)

    # ----- spring -----
    ref = spring_moments(1.0, 2.0, 1.0, 0.3)
    emit("ou_err", ref["err"])
    emit("ou_Cxm", ref["Cxm"])
    emit("ou_heat", ref["heat"])
    emit("ou_flow", ref["flow"])
    emit("ou_sigma", ref["sigma"])
    emit("ou_info", ref["info"])
    emit("ou_heat_minus_flow_minus_sigma", ref["heat"] - ref["flow"] - ref["sigma"])

    # identity on a cloud of parameters, and where sigma falls below the flow
    id_gap = 0.0
    sigma_below = 0
    heat_below_flow = 0
    ncloud = 0
    for a in (0.3, 1.0, 2.5):
        for lam in (0.2, 1.0, 4.0, 20.0):
            for v in (0.5, 1.0, 2.0):
                for D in (0.05, 0.3, 1.5):
                    row = spring_moments(a, lam, v, D)
                    id_gap = max(id_gap, abs(row["heat"] - row["flow"] - row["sigma"]))
                    if row["sigma"] < row["flow"] - 1e-9:
                        sigma_below += 1
                    if row["heat"] + 1e-9 < row["flow"]:
                        heat_below_flow += 1
                    ncloud += 1
    emit("spring_identity_max_gap", id_gap)
    emit("spring_cloud_n", ncloud)
    emit("spring_sigma_below_flow_count", sigma_below)
    emit("spring_heat_below_flow_count", heat_below_flow)

    # fixed error: monotonicity, limit, Kalman gap
    a, v, eps = 1.0, 1.0, 0.2
    lams = np.array([1.0, 3.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0])
    # minimal lam with positive D: av/(a+lam) < eps => lam > a(v/eps - 1) = 4
    prev_heat = None
    decreasing = True
    for lam in lams:
        if lam <= a * (v / eps - 1.0):
            continue
        row = spring_at_error(a, lam, v, eps)
        formula = heat_fixed_error_formula(a, lam, v, eps)
        emit("spring_lam_%g_heat" % lam, row["heat"])
        emit("spring_lam_%g_flow" % lam, row["flow"])
        emit("spring_lam_%g_formula_gap" % lam, abs(row["heat"] - formula))
        emit("spring_lam_%g_Q_minus_I" % lam, row["heat"] - row["flow"])
        emit("spring_lam_%g_I_minus_floor" % lam, row["flow"] - a * v / eps)
        emit("spring_lam_%g_kalman" % lam, kalman_inflow(a, v, eps))
        if prev_heat is not None and row["heat"] > prev_heat + 1e-9:
            decreasing = False
        prev_heat = row["heat"]
    emit("spring_eps_0.2_heat_decreases_in_lam", int(decreasing))
    emit("floor_av_over_eps", a * v / eps)
    emit("kalman_rate", kalman_inflow(a, v, eps))
    emit("floor_minus_kalman", a * v / eps - kalman_inflow(a, v, eps))

    # ε = v and ε > v: the fast limit is not the infimum
    for eps_bad, tag in ((1.0, "eq_v"), (1.5, "above_v")):
        heats_bad = []
        for lam in (0.05, 0.2, 1.0, 10.0, 1000.0):
            row = spring_at_error(1.0, lam, 1.0, eps_bad)
            heats_bad.append(row["heat"])
            emit("spring_%s_lam_%g_heat" % (tag, lam), row["heat"])
        emit("spring_%s_min_heat_on_sample" % tag, float(min(heats_bad)))
        emit("spring_%s_av_over_eps" % tag, 1.0 / eps_bad)
        emit("spring_%s_dQ_sign_factor" % tag, heat_derivative_sign_factor(eps_bad, 1.0))

    # analytic derivative sign at ε = 0.2
    emit("dQ_sign_factor_eps0.2", heat_derivative_sign_factor(0.2, 1.0))

    # does the flow on ε < v ever fall below av/ε?
    flow_below_floor = 0
    flow_below_kalman = 0
    ntrack = 0
    worst_flow_minus_floor = 0.0
    for eps_t in (0.05, 0.2, 0.5, 0.9):
        lam_min = 1.0 * (1.0 / eps_t - 1.0)
        for lam in np.geomspace(lam_min * 1.01, 1e5, 24):
            row = spring_at_error(1.0, float(lam), 1.0, eps_t)
            gap = row["flow"] - 1.0 / eps_t
            worst_flow_minus_floor = min(worst_flow_minus_floor, gap)
            if gap < -1e-6:
                flow_below_floor += 1
            if row["flow"] + 1e-6 < kalman_inflow(1.0, 1.0, eps_t):
                flow_below_kalman += 1
            ntrack += 1
    emit("track_samples", ntrack)
    emit("flow_below_av_over_eps", flow_below_floor)
    emit("flow_below_kalman", flow_below_kalman)
    emit("worst_flow_minus_floor", worst_flow_minus_floor)

    # stake designs
    for wstake in (2.0, 8.0, 20.0, 50.0):
        e_pick, q_pick, cost, kind = ou_design(1.0, 1.0, wstake)
        emit("ou_design_w%g_err" % wstake, e_pick)
        emit("ou_design_w%g_heat" % wstake, q_pick)
        emit("ou_design_w%g_kind" % wstake, kind)
    # tie at w = 4a/v
    e_tie, q_tie, cost_tie, kind_tie = ou_design(1.0, 1.0, 4.0)
    emit("ou_tie_w4_err", e_tie)
    emit("ou_tie_w4_heat", q_tie)
    emit("ou_tie_w4_kind", kind_tie)
    emit("ou_tie_w4_cost", cost_tie)
    emit("blind_cost_w4", 4.0 * 1.0)

    # The fast-limit value av/ε is a lower bound on the heat and an upper
    # bound on the information flow. The flow's lower envelope is the
    # Kalman rate. The two objectives therefore do not share a corner.
    a, v = 1.0, 1.0
    lam_min = a * (v / 0.2 - 1.0)
    edge = spring_at_error(a, lam_min * (1.0 + 1e-6), v, 0.2)
    emit("slow_edge_flow", edge["flow"])
    emit("slow_edge_heat", edge["heat"])
    emit("slow_edge_flow_minus_kalman", edge["flow"] - kalman_inflow(a, v, 0.2))
    for wstake in (2.0, 8.0, 20.0, 50.0):
        e_heat, q_heat, cost_heat, kind_heat = ou_design(a, v, wstake)
        e_flow = math.sqrt(a * v / wstake)
        if e_flow < v:
            i_flow = kalman_inflow(a, v, e_flow)
            cost_flow = i_flow + wstake * e_flow
            kind_flow = "track" if cost_flow < wstake * v else "blind"
            if cost_flow >= wstake * v:
                e_flow, i_flow, cost_flow, kind_flow = v, 0.0, wstake * v, "blind"
        else:
            e_flow, i_flow, cost_flow, kind_flow = v, 0.0, wstake * v, "blind"
        emit("flow_obj_w%g_err" % wstake, e_flow)
        emit("flow_obj_w%g_I" % wstake, i_flow)
        emit("flow_obj_w%g_cost" % wstake, cost_flow)
        emit("flow_obj_w%g_kind" % wstake, kind_flow)
        emit("heat_obj_w%g_kind" % wstake, kind_heat)
        emit("objectives_same_kind_w%g" % wstake, int(kind_heat == kind_flow))

    # path
    sim = path_sekimoto(1.0, 2.0, 1.0, 0.3, seed=7, dt=2e-3, nstep=20000, burn=2000)
    emit("path_heat_seed7", sim)
    emit("numpy", np.__version__)

    # XOR and sticky
    cj, c1, c2 = xor_future()
    emit("xor_joint", cj)
    emit("xor_m1", c1)
    emit("xor_m2", c2)
    emit("h_0.2", binary_entropy(0.2))
    I_past, I_now, I_next = sticky_numbers()
    emit("sticky_past", I_past)
    emit("sticky_now", I_now)
    emit("sticky_next", I_next)
    emit("sticky_past_excess", I_past - I_next)
    emit("sticky_still_gap", I_now - I_next)

    if "--crossref" in sys.argv:
        for doi in DOIS:
            status, year, title, authors, container = crossref_one(doi)
            emit(
                "DOI",
                "%s\t%d\t%s\t%s\t%s\t%s" % (doi, status, year, "|".join(authors), container, title),
            )

    print("LINES", len(out))


if __name__ == "__main__":
    main()
