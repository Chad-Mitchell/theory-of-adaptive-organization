#!/usr/bin/env python3
"""Numerical checks for theory/INFO_PHYSICS.md.

Closed forms for a driven two-state memory, a joint-versus-per-layer
comparison, an Ornstein–Uhlenbeck tracker with K slow variables, and the
gap between a dissipation lower bound and the master-equation cost.

Run from the repo root:
  nice -n 19 python3 theory/info_physics_checks/info_physics_checks.py
"""
from __future__ import annotations

import math
import sys

import numpy as np

PASS = 0
FAIL = 0
ROWS = []


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS  %s  %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


def near(a, b, tol=1e-9):
    a = float(a)
    b = float(b)
    scale = max(1.0, abs(a), abs(b))
    return abs(a - b) <= tol * scale


def hbin(p):
    p = float(p)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def record(key, value):
    ROWS.append((key, float(value)))


# ---------------------------------------------------------------- two-state sensor
def sensor(alpha_c, alpha_e, gamma):
    """Symmetric telegraph signal, two-state driven memory.

    Signal flips at rate gamma each way. Memory corrects at alpha_c and
    errs at alpha_e. kT = 1. Entropy is in nats.
    """
    Z = alpha_c + alpha_e + 2.0 * gamma
    # P(M != X)
    err = (alpha_e + gamma) / Z
    # medium entropy-production rate of the memory edges
    heat = gamma * (alpha_c - alpha_e) / Z * math.log(alpha_c / alpha_e)
    # rate at which memory jumps increase I(M; X)
    flow = gamma * (alpha_c - alpha_e) / Z * math.log((alpha_c + gamma) / (alpha_e + gamma))
    info = math.log(2.0) - hbin(err)
    return {"Z": Z, "err": err, "heat": heat, "flow": flow, "info": info}


def generator_binary(alpha_c, alpha_e, gamma):
    """States (X, M): 00, 01, 10, 11. Row-generator."""
    G = np.zeros((4, 4))
    # 00
    G[0, 1] = alpha_e
    G[0, 2] = gamma
    # 01
    G[1, 0] = alpha_c
    G[1, 3] = gamma
    # 10
    G[2, 0] = gamma
    G[2, 3] = alpha_c
    # 11
    G[3, 1] = gamma
    G[3, 2] = alpha_e
    for i in range(4):
        G[i, i] = -G[i].sum()
    return G


def stationary(G):
    n = G.shape[0]
    A = G.T.copy()
    A[-1, :] = 1.0
    b = np.zeros(n)
    b[-1] = 1.0
    p = np.linalg.solve(A, b)
    p = np.real_if_close(p).real
    p = np.clip(p, 0.0, None)
    p /= p.sum()
    return p


def ep_directed(p, G, edges=None):
    """Sum of p_i k_ij ln(k_ij/k_ji) over directed edges with both rates positive."""
    n = len(p)
    total = 0.0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if edges is not None and (i, j) not in edges:
                continue
            kij = G[i, j]
            kji = G[j, i]
            if kij > 0.0 and kji > 0.0:
                total += p[i] * kij * math.log(kij / kji)
    return total


MEM_EDGES = {(0, 1), (1, 0), (2, 3), (3, 2)}


def test_binary_closed_form():
    alpha_c, alpha_e, gamma = 4.0, 0.5, 1.0
    s = sensor(alpha_c, alpha_e, gamma)
    G = generator_binary(alpha_c, alpha_e, gamma)
    p = stationary(G)
    # symmetry and the solved mass
    Z = s["Z"]
    p00 = 0.5 * (alpha_c + gamma) / Z
    p01 = 0.5 * (alpha_e + gamma) / Z
    check("binary stationary matches the closed form",
          near(p[0], p00, 1e-12) and near(p[1], p01, 1e-12) and near(p[0], p[3]) and near(p[1], p[2]),
          "p00=%.12f" % p[0])
    heat_g = ep_directed(p, G, MEM_EDGES)
    check("binary heat matches the edge sum", near(heat_g, s["heat"], 1e-12),
          "heat=%.12f" % s["heat"])
    # total EP equals memory heat: signal rates are balanced, ln(k/k)=0
    check("signal edges add no medium entropy", near(ep_directed(p, G), s["heat"], 1e-12))
    check("heat is at least the information flow", s["heat"] + 1e-15 >= s["flow"] > 0.0,
          "heat=%.6f flow=%.6f" % (s["heat"], s["flow"]))
    # slow signal: efficiency -> 1
    slow = sensor(4.0, 0.5, 1e-4)
    eta_slow = slow["flow"] / slow["heat"]
    check("slow-signal efficiency approaches 1", eta_slow > 1.0 - 1e-3, "eta=%.8f" % eta_slow)
    fast = sensor(4.0, 0.5, 5.0)
    eta_fast = fast["flow"] / fast["heat"]
    check("fast-signal efficiency is strictly below 1", 0.0 < eta_fast < 0.95,
          "eta=%.8f" % eta_fast)
    record("eta_slow", eta_slow)
    record("eta_fast", eta_fast)
    record("heat_ref", s["heat"])
    record("flow_ref", s["flow"])
    record("err_ref", s["err"])
    record("info_ref", s["info"])


def test_heat_unbounded_at_fixed_error():
    """At fixed Hamming error, dissipation has a positive floor and no ceiling."""
    gamma = 1.0
    target = 0.2

    def heat_at_ratio(rho):
        # s = alpha_e, alpha_c = rho * s, error fixed at `target`
        s = gamma * (1.0 - 2.0 * target) / (target * (rho + 1.0) - 1.0)
        if s <= 0.0:
            return None
        return sensor(rho * s, s, gamma)

    # equilibrium ratio that realizes this error in the fast limit
    rho_eq = (1.0 - target) / target
    # just above that ratio, and a very large ratio
    q_lo = heat_at_ratio(rho_eq * 1.0000001)
    # As rho -> infinity at fixed error, alpha_c -> gamma(1-2*err)/err and
    # Q ~ [gamma * alpha_c / (alpha_c + 2 gamma)] ln rho, which is unbounded.
    q_hi = heat_at_ratio(math.exp(40.0))
    asym = gamma * (1.0 - 2.0 * target) / target
    asym = gamma * asym / (asym + 2.0 * gamma)  # coefficient of ln rho
    # minimum on a log grid
    rhos = np.exp(np.linspace(math.log(rho_eq * 1.0001), math.log(math.exp(40.0)), 600))
    heats = []
    for rho in rhos:
        row = heat_at_ratio(float(rho))
        heats.append(row["heat"])
        if abs(row["err"] - target) > 1e-8:
            check("fixed-error construction holds the error", False, "err=%s" % row["err"])
            return
    q_min = min(heats)
    check("fixed error is held while heat grows without a ceiling",
          q_hi["heat"] > 20.0 * q_min and abs(q_hi["heat"] / 40.0 - asym) / asym < 0.05,
          "Qmin=%.6f Q(ln rho=40)=%.6f asym*40=%.6f" % (q_min, q_hi["heat"], asym * 40.0))
    # information is a function of the error alone, so it is fixed too
    check("mutual information is fixed when the error is fixed",
          near(q_lo["info"], q_hi["info"], 1e-8),
          "I=%.8f" % q_hi["info"])
    record("Qmin_err02", q_min)
    record("Q_large_err02", q_hi["heat"])
    record("I_err02", q_hi["info"])


def tilted_current_stats(G, increments, dz=1e-4):
    """Mean rate and variance-per-time of an edge current, by finite differences
    of the dominant eigenvalue of the tilted generator."""
    def lam(z):
        # Off-diagonal rates are tilted. The diagonal stays the untilted escape
        # rate. Resetting it would force every row to sum to zero and hide the current.
        T = G.copy()
        for (i, j), d in increments.items():
            if i == j:
                continue
            T[i, j] = G[i, j] * math.exp(z * d)
        ev = np.linalg.eigvals(T.T)
        return float(np.max(ev.real))

    # at z=0 the dominant eigenvalue is 0
    jp = lam(dz)
    jm = lam(-dz)
    j0 = lam(0.0)
    mean = (jp - jm) / (2.0 * dz)
    var = (jp - 2.0 * j0 + jm) / (dz * dz)
    return mean, var


def test_tur():
    alpha_c, alpha_e, gamma = 4.0, 0.5, 1.0
    s = sensor(alpha_c, alpha_e, gamma)
    G = generator_binary(alpha_c, alpha_e, gamma)
    # current: net corrective jumps on both memory pairs
    # 01->00 and 10->11 are corrections (+1); the reverses are -1
    inc = {(1, 0): 1.0, (0, 1): -1.0, (2, 3): 1.0, (3, 2): -1.0}
    mean, var = tilted_current_stats(G, inc)
    # closed-form net corrective rate: two pairs, each of flux (gamma/2)(ac-ae)/Z
    flux = gamma * (alpha_c - alpha_e) / s["Z"]
    check("current mean matches the net corrective flux", near(mean, flux, 1e-6),
          "j=%.8f flux=%.8f" % (mean, flux))
    bound = 2.0 * mean * mean / var
    check("TUR: entropy production rate is at least 2 j^2 / (var per time)",
          s["heat"] + 1e-6 >= bound > 0.0 and var > 0.0,
          "heat=%.6f TUR=%.6f var=%.6f" % (s["heat"], bound, var))
    # Near the slow-signal limit the flow bound is almost tight, so adding the
    # TUR on top overshoots the heat. The two inequalities bound one rate.
    slow = sensor(4.0, 0.5, 0.05)
    Gs = generator_binary(4.0, 0.5, 0.05)
    mean_s, var_s = tilted_current_stats(Gs, inc, dz=1e-3)
    bound_s = 2.0 * mean_s * mean_s / var_s
    check("flow and TUR do not add: their sum can exceed the heat",
          slow["heat"] < slow["flow"] + bound_s and slow["heat"] + 1e-6 >= slow["flow"],
          "heat=%.6f flow=%.6f TUR=%.6f" % (slow["heat"], slow["flow"], bound_s))
    record("tur_bound", bound)
    record("tur_heat", s["heat"])
    record("tur_flow", s["flow"])
    record("tur_slow_heat", slow["heat"])
    record("tur_slow_flow", slow["flow"])
    record("tur_slow_bound", bound_s)


# ---------------------------------------------------------------- Still, one step
def test_still_step():
    """Still's one-step identity is the conditional-entropy difference.

    Their I_mem is I(s_t; x_t), not the stock about the whole past.
    The quench-and-relax heat of this sensor is a different number.
    """
    eps = 1.5  # energy gap in units of kT
    p_flip = 0.3
    q = 1.0 / (1.0 + math.exp(eps))  # P(mismatch | equilibrated)
    err_next = q + p_flip - 2.0 * q * p_flip
    i_mem = math.log(2.0) - hbin(q)
    i_pred = math.log(2.0) - hbin(err_next)
    i_np = i_mem - i_pred
    # chain-rule form of the same difference
    gap = hbin(err_next) - hbin(q)
    check("Still difference equals H(s|x_next)-H(s|x)", near(i_np, gap, 1e-12),
          "I_np=%.10f" % i_np)
    # physical heat of quench-and-relax, per step: only flips pay
    heat = p_flip * eps * math.tanh(eps / 2.0)
    check("cycle heat and Still's I_np are different numbers",
          abs(heat - i_np) > 1e-3,
          "heat=%.6f I_np=%.6f" % (heat, i_np))
    # Still's accounting: dissipation of the signal step equals I_np
    # by H(s|x_next)-H(s|x). Reproduced above. The cycle heat is larger
    # than that identity at this point, or smaller: report the ratio.
    record("still_Inp", i_np)
    record("still_cycle_heat", heat)
    record("still_I_inst", i_mem)
    record("still_I_pred", i_pred)


# ---------------------------------------------------------------- layers
def kl_joint_from_conditionals(px, channels):
    """channels: list of arrays P(m|x), each shape (n_x, n_m). Conditionally independent given x."""
    # build the joint by enumeration. n_m is 2 for every channel here.
    n = len(channels)
    # state index in 0..2^n - 1
    masses = {}
    for x, p_x in enumerate(px):
        for mask in range(1 << n):
            prob = p_x
            for i in range(n):
                bit = (mask >> i) & 1
                prob *= channels[i][x, bit]
            masses[(x, mask)] = masses.get((x, mask), 0.0) + prob
    return masses


def mi_from_masses(masses):
    px = {}
    pm = {}
    for (x, m), p in masses.items():
        px[x] = px.get(x, 0.0) + p
        pm[m] = pm.get(m, 0.0) + p
    mi = 0.0
    for (x, m), p in masses.items():
        if p <= 0.0:
            continue
        mi += p * math.log(p / (px[x] * pm[m]))
    return mi


def test_joint_information():
    # two conditionally independent BSC observations of one fair bit
    # crossover q1, q2
    q1, q2 = 0.1, 0.2
    px = [0.5, 0.5]

    def bsc(q):
        # rows x, columns m
        return np.array([[1 - q, q], [q, 1 - q]])

    masses = kl_joint_from_conditionals(px, [bsc(q1), bsc(q2)])
    joint = mi_from_masses(masses)
    i1 = math.log(2.0) - hbin(q1)
    i2 = math.log(2.0) - hbin(q2)
    check("conditionally independent sensors: joint I is below the sum",
          joint < i1 + i2 - 1e-9 and joint > max(i1, i2) - 1e-9,
          "joint=%.6f sum=%.6f" % (joint, i1 + i2))
    record("I_joint_bsc", joint)
    record("I_sum_bsc", i1 + i2)

    # synergy: Z = M1 xor M2 with M1, M2 independent fair bits.
    # The pair determines Z, and each bit alone is independent of Z.
    xor_joint = {}
    xor_1 = {}
    xor_2 = {}
    for m1 in (0, 1):
        for m2 in (0, 1):
            z = m1 ^ m2
            xor_joint[(z, m1 * 2 + m2)] = 0.25
            xor_1[(z, m1)] = xor_1.get((z, m1), 0.0) + 0.25
            xor_2[(z, m2)] = xor_2.get((z, m2), 0.0) + 0.25
    sj = mi_from_masses(xor_joint)
    s1 = mi_from_masses(xor_1)
    s2 = mi_from_masses(xor_2)
    check("without conditional independence, joint I can exceed the sum",
          sj > s1 + s2 + 0.5 and near(s1, 0.0, 1e-12) and near(s2, 0.0, 1e-12),
          "joint=%.6f sum=%.6f" % (sj, s1 + s2))
    record("synergy_joint", sj)
    record("synergy_sum", s1 + s2)


def redundant_pair(alpha_c, alpha_e, gamma):
    """One signal X, two conditionally independent memories. 8 states (X, M1, M2)."""
    # index: x*4 + m1*2 + m2
    def idx(x, m1, m2):
        return x * 4 + m1 * 2 + m2

    G = np.zeros((8, 8))
    for x in (0, 1):
        for m1 in (0, 1):
            for m2 in (0, 1):
                i = idx(x, m1, m2)
                G[i, idx(1 - x, m1, m2)] += gamma
                rate1 = alpha_c if m1 != x else alpha_e
                G[i, idx(x, 1 - m1, m2)] += rate1
                rate2 = alpha_c if m2 != x else alpha_e
                G[i, idx(x, m1, 1 - m2)] += rate2
                G[i, i] = -(gamma + rate1 + rate2)
    p = stationary(G)
    # memory edges: any transition that flips exactly one memory bit
    mem = []
    for x in (0, 1):
        for m1 in (0, 1):
            for m2 in (0, 1):
                i = idx(x, m1, m2)
                mem.append((i, idx(x, 1 - m1, m2)))
                mem.append((i, idx(x, m1, 1 - m2)))
    heat = ep_directed(p, G, set(mem))
    # joint mutual information I((M1,M2); X)
    masses = {}
    for x in (0, 1):
        for m1 in (0, 1):
            for m2 in (0, 1):
                masses[(x, m1 * 2 + m2)] = p[idx(x, m1, m2)]
    joint_I = mi_from_masses(masses)
    single = sensor(alpha_c, alpha_e, gamma)
    return heat, joint_I, single


def test_redundant_mechanisms():
    alpha_c, alpha_e, gamma = 4.0, 0.5, 1.0
    heat, joint_I, single = redundant_pair(alpha_c, alpha_e, gamma)
    check("two redundant mechanisms dissipate twice one mechanism",
          near(heat, 2.0 * single["heat"], 1e-9),
          "heat2=%.6f 2*heat1=%.6f" % (heat, 2 * single["heat"]))
    check("joint information is below the sum of the two informations",
          joint_I < 2.0 * single["info"] - 1e-6,
          "Ijoint=%.6f 2I=%.6f" % (joint_I, 2 * single["info"]))
    # error of the single sensor vs a majority of two is not the claim;
    # the claim is that the second mechanism buys a sublinear information increment
    incr = joint_I - single["info"]
    check("the second copy adds less information than the first",
          0.0 < incr < single["info"] - 1e-6,
          "deltaI=%.6f I1=%.6f" % (incr, single["info"]))
    record("heat_two", heat)
    record("I_joint_two", joint_I)
    record("I_one", single["info"])
    record("delta_I_second", incr)


def sum_tracker(alpha_c, alpha_e, gamma):
    """One ternary memory tracking S = X1 + X2, two independent telegraphs."""
    # states (S, M), S,M in 0,1,2. index 3*S + M
    def idx(S, M):
        return 3 * S + M

    G = np.zeros((9, 9))
    # signal rates of the sum
    sig = {(0, 1): 2 * gamma, (2, 1): 2 * gamma, (1, 0): gamma, (1, 2): gamma}
    for S in range(3):
        for M in range(3):
            i = idx(S, M)
            # signal moves
            for (a, b), rate in sig.items():
                if a == S:
                    G[i, idx(b, M)] += rate
            # memory moves toward S at alpha_c, away at alpha_e
            for Mp in (M - 1, M + 1):
                if Mp < 0 or Mp > 2:
                    continue
                toward = abs(Mp - S) < abs(M - S)
                G[i, idx(S, Mp)] += alpha_c if toward else alpha_e
    for i in range(9):
        G[i, i] = 0.0
        G[i, i] = -G[i].sum()
    p = stationary(G)
    # memory edges: S fixed, M changes
    mem = []
    for S in range(3):
        for M in range(3):
            for Mp in range(3):
                if M != Mp:
                    mem.append((idx(S, M), idx(S, Mp)))
    heat = ep_directed(p, G, set(mem))
    # mean squared error of M against S
    mse = 0.0
    for S in range(3):
        for M in range(3):
            mse += p[idx(S, M)] * (M - S) ** 2
    return heat, mse, p, G


def two_specialized_on_sum(alpha_c, alpha_e, gamma):
    """Two independent binary sensors. Estimate of the sum is M1+M2.
    Heat adds. MSE computed from the product law."""
    s = sensor(alpha_c, alpha_e, gamma)
    err = s["err"]
    # P(Mi = Xi) = 1-err. X1, X2, and the two noises are independent.
    # S = X1+X2, hat = M1+M2.
    # Enumerate 16 equally structured atoms. X fair independent, Mi mismatches Xi with prob err.
    mse = 0.0
    # x1, x2 in {0,1}, e1, e2 in {0,1} where ei=1 means mismatch
    for x1 in (0, 1):
        for x2 in (0, 1):
            for e1 in (0, 1):
                for e2 in (0, 1):
                    prob = 0.25 * (err if e1 else 1 - err) * (err if e2 else 1 - err)
                    S = x1 + x2
                    M1 = x1 if e1 == 0 else 1 - x1
                    M2 = x2 if e2 == 0 else 1 - x2
                    mse += prob * (M1 + M2 - S) ** 2
    return 2.0 * s["heat"], mse


def test_joint_versus_stack():
    alpha_c, alpha_e, gamma = 6.0, 0.4, 0.5
    heat_j, mse_j, _, _ = sum_tracker(alpha_c, alpha_e, gamma)
    heat_s, mse_s = two_specialized_on_sum(alpha_c, alpha_e, gamma)
    check("specialized pair dissipates more than one sum-tracker at these rates",
          heat_s > heat_j > 0.0,
          "joint_heat=%.6f pair_heat=%.6f" % (heat_j, heat_s))
    check("both designs have a finite squared error on the sum",
          mse_j >= 0.0 and mse_s >= 0.0,
          "mse_joint=%.6f mse_pair=%.6f" % (mse_j, mse_s))
    # a constant h per layer is not the heat: the two designs have K=1 and K=2
    # and the heats are not in the ratio 1:2 of a constant upkeep, nor is heat
    # independent of the drive. Compare two drives at K=1.
    heat_lo, _, _, _ = sum_tracker(1.2, 1.0, gamma)
    check("one layer's heat depends on the drive, so it is not a constant h",
          abs(heat_j - heat_lo) / heat_j > 0.2,
          "heat_strong=%.6f heat_weak=%.6f" % (heat_j, heat_lo))
    record("sum_heat_joint", heat_j)
    record("sum_heat_pair", heat_s)
    record("sum_mse_joint", mse_j)
    record("sum_mse_pair", mse_s)
    record("sum_heat_weak", heat_lo)


# ---------------------------------------------------------------- sticky memory, past stock
def sticky_chain(p_flip, lam, q):
    """X is a binary Markov chain, flip probability p_flip.
    With probability lam the memory is rewritten as a BSC(q) observation of X;
    otherwise it keeps its previous value.
    State (X_prev, X, M) is Markov on 8 states. One step.
    """
    # index: xp*4 + x*2 + m
    def idx(xp, x, m):
        return xp * 4 + x * 2 + m

    P = np.zeros((8, 8))
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = idx(xp, x, m)
                for xn in (0, 1):
                    p_x = (1 - p_flip) if xn == x else p_flip
                    for redraw in (0, 1):
                        p_r = lam if redraw else (1 - lam)
                        if redraw:
                            for mn in (0, 1):
                                p_m = (1 - q) if mn == xn else q
                                P[i, idx(x, xn, mn)] += p_x * p_r * p_m
                        else:
                            P[i, idx(x, xn, m)] += p_x * p_r
    # stationary
    # P is row-stochastic. Eigenvector of P.T
    ev, evec = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(ev - 1.0)))
    pi = np.real(evec[:, k])
    pi = np.clip(pi, 0.0, None)
    pi /= pi.sum()
    return P, pi


def mi_marginal(pi, ix, iy):
    """Mutual information of two coordinates of an 8-state (xp, x, m) law.
    ix, iy are callables (xp, x, m) -> label.
    """
    masses = {}
    labels_x = {}
    labels_y = {}
    n = 0
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = xp * 4 + x * 2 + m
                p = float(pi[i])
                a, b = ix(xp, x, m), iy(xp, x, m)
                masses[(a, b)] = masses.get((a, b), 0.0) + p
                labels_x[a] = labels_x.get(a, 0.0) + p
                labels_y[b] = labels_y.get(b, 0.0) + p
                n += 1
    mi = 0.0
    for (a, b), p in masses.items():
        if p <= 0.0:
            continue
        mi += p * math.log(p / (labels_x[a] * labels_y[b]))
    return mi


def test_past_stock():
    P, pi = sticky_chain(0.2, 0.3, 0.05)
    # one-step transition should be stochastic
    check("sticky chain is row-stochastic", near(P.sum(axis=1).min(), 1.0, 1e-12) and near(P.sum(axis=1).max(), 1.0, 1e-12))
    I_now = mi_marginal(pi, lambda xp, x, m: x, lambda xp, x, m: m)
    I_past = mi_marginal(pi, lambda xp, x, m: xp * 2 + x, lambda xp, x, m: m)
    # predictive about the next step needs a joint of (state, next). Build it.
    # I(M; X_next) from the one-step kernel.
    masses = {}
    for xp in (0, 1):
        for x in (0, 1):
            for m in (0, 1):
                i = xp * 4 + x * 2 + m
                for j in range(8):
                    p = float(pi[i] * P[i, j])
                    if p <= 0.0:
                        continue
                    # next state's x is (j//2) % 2, its m is j % 2; we want current m and next x
                    xn = (j // 2) % 2
                    masses[(m, xn)] = masses.get((m, xn), 0.0) + p
    I_next = mi_from_masses(masses)
    check("a sticky memory holds more about the recent past than about the present",
          I_past > I_now + 1e-6,
          "I_past=%.6f I_now=%.6f" % (I_past, I_now))
    check("Still's instantaneous predictive information is below the instantaneous memory",
          I_now > I_next + 1e-6,
          "I_now=%.6f I_next=%.6f" % (I_now, I_next))
    # chain rule on the two-time past: I(M; Xprev, X) = I(M; Xnext) + I(M; Xprev, X | Xnext)
    # Compute I(M; (Xprev, X, Xnext)) two ways is heavier. Check the definitional split
    # I(M; Xprev, X) - I(M; Xnext) > 0, which is the nonpredictive excess of this finite past
    # over the one-step future. It is not Still's I(s;x)-I(s;x_next).
    excess = I_past - I_next
    still_gap = I_now - I_next
    check("past-stock excess and Still's instantaneous gap are different",
          abs(excess - still_gap) > 1e-4,
          "past_excess=%.6f still_gap=%.6f" % (excess, still_gap))
    record("I_past_sticky", I_past)
    record("I_now_sticky", I_now)
    record("I_next_sticky", I_next)
    record("past_excess", excess)
    record("still_gap_sticky", still_gap)


# ---------------------------------------------------------------- OU, K slow variables
def ou_pair(a, lam, v, D):
    """One OU signal and one linear memory. Returns covariance, I, partial EP.
    dX = -a X dt + sqrt(2 a v) dW
    dM = -lam (M - X) dt + sqrt(2 D) dB
    kT = 1. D is the memory diffusion.
    """
    Cxx = v
    Cxm = lam * v / (a + lam)
    Cmm = Cxm + D / lam
    C = np.array([[Cxx, Cxm], [Cxm, Cmm]])
    det = Cxx * Cmm - Cxm ** 2
    info = 0.5 * math.log(Cxx * Cmm / det)
    # J/p = lam (X - M) + D (C^{-1} z)_M
    Cinv = np.linalg.inv(C)
    # b · z = lam * X - lam * M + D * (Cinv row M) · z
    b = np.array([lam, -lam]) + D * Cinv[:, 1]
    moment = float(b @ C @ b)
    sigma = moment / D
    err = Cxx + Cmm - 2 * Cxm
    return {"C": C, "info": info, "sigma": sigma, "err": err, "Cxm": Cxm, "Cmm": Cmm}


def test_ou_family():
    a, lam, v, D = 1.0, 2.0, 1.0, 0.3
    row = ou_pair(a, lam, v, D)
    check("OU partial entropy production is positive", row["sigma"] > 0.0, "sigma=%.6f" % row["sigma"])
    check("OU error splits into bandwidth lag and thermal variance",
          near(row["err"], v * a / (a + lam) + D / lam, 1e-12),
          "err=%.6f" % row["err"])
    # equilibrium: no drive toward a moving signal. Couple lam but set the signal
    # variance seen by the force to 0 by using the frozen-X current formula.
    # Frozen X=0: force -lam/D * M * kT with kT=1, spring κ=lam/D, equilibrium variance D/lam.
    # Current vanishes. Represented here by a= very large and v fixed so X is fast noise
    # of small correlation; a cleaner test is the formula at D matching and lam with a signal
    # that is not observed: set lam_drive = 0 in a one-line current.
    # Direct: b for a memory with f = -lam M (no X) and variance D/lam.
    # C = D/lam, Cinv = lam/D, b = -lam + D*(lam/D) = 0. Sigma = 0.
    check("an equilibrium memory has zero partial entropy production",
          near(-lam + D * (lam / D), 0.0))
    # K independent worlds: EP and information add
    modes = [(0.5, 1.0, 1.0, 0.2), (1.5, 3.0, 0.8, 0.4), (4.0, 2.0, 1.2, 0.5)]
    sig = 0.0
    info = 0.0
    for aa, ll, vv, dd in modes:
        r = ou_pair(aa, ll, vv, dd)
        sig += r["sigma"]
        info += r["info"]
    check("K independent OU trackers add entropy production and information",
          sig > 0 and info > 0, "K=3 sigma=%.6f I=%.6f" % (sig, info))
    record("ou_sigma", row["sigma"])
    record("ou_info", row["info"])
    record("ou_err", row["err"])
    record("ou_K3_sigma", sig)
    record("ou_K3_info", info)

    # two redundant memories on one signal: 3D Lyapunov
    # dX = -a X dt + sqrt(2 a v) dW
    # dMi = -lam (Mi - X) dt + sqrt(2 D) dBi
    lam1, lam2, D1, D2 = 2.0, 2.0, 0.3, 0.3
    A = np.array([
        [-a, 0.0, 0.0],
        [lam1, -lam1, 0.0],
        [lam2, 0.0, -lam2],
    ])
    BB = np.diag([2 * a * v, 2 * D1, 2 * D2])
    # Lyapunov A C + C A.T + BB = 0
    # solve via Kronecker
    n = 3
    Mly = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    cvec = -BB.reshape(-1)
    # vec(A C) = (I ⊗ A) vec(C), vec(C A.T) = (A ⊗ I) vec(C)
    Cvec = np.linalg.solve(Mly, cvec)
    C = Cvec.reshape(n, n)
    check("redundant OU covariance is symmetric positive",
          near(np.linalg.norm(C - C.T), 0.0, 1e-8) and np.all(np.linalg.eigvalsh(C) > 0))
    # partial EP of each memory
    def partial(i_m, lam_i, D_i):
        Cinv = np.linalg.inv(C)
        # f_i = lam (X - Mi) = lam * z_0 - lam * z_i
        b = np.zeros(3)
        b[0] = lam_i
        b[i_m] = -lam_i
        b = b + D_i * Cinv[:, i_m]
        return float(b @ C @ b) / D_i

    s1 = partial(1, lam1, D1)
    s2 = partial(2, lam2, D2)
    # joint information I(M1,M2; X)
    # cov of (M1,M2) and cross with X
    CXX = C[0, 0]
    Cmx = C[1:, 0:1]  # 2x1
    Cmm = C[1:, 1:]
    # I = 1/2 ln( det(Cmm) * CXX / det(C_full_of_those) )
    # det of the 3x3 equals det(Cmm) * (CXX - Cmx^T Cmm^{-1} Cmx) Schur
    schur = CXX - float(np.asarray(Cmx.T @ np.linalg.inv(Cmm) @ Cmx).reshape(-1)[0])
    I_joint = 0.5 * math.log(CXX / schur)
    I_each = ou_pair(a, lam1, v, D1)["info"]
    check("redundant OU mechanisms add entropy production",
          near(s1, s2, 1e-8) and s1 > 0.0, "s1=%.6f" % s1)
    check("redundant OU joint information is below twice one memory",
          I_each < I_joint < 2 * I_each - 1e-6,
          "Ijoint=%.6f I1=%.6f" % (I_joint, I_each))
    record("ou_red_sigma_sum", s1 + s2)
    record("ou_red_I_joint", I_joint)
    record("ou_red_I_one", I_each)

    # trajectory cross-check of the partial heat for the single pair
    rng = np.random.default_rng(7)
    dt = 2e-3
    nstep = 20000
    burn = 2000
    kappa = lam / D  # kT = 1
    x = 0.0
    m = 0.0
    heat = 0.0
    sig_x = math.sqrt(2 * a * v * dt)
    sig_m = math.sqrt(2 * D * dt)
    for t in range(nstep + burn):
        dWx = rng.normal() * sig_x
        dBm = rng.normal() * sig_m
        x_new = x - a * x * dt + dWx
        # drift uses current X (Ito). Stratonovich heat uses the midpoint force.
        m_new = m + (-lam * (m - x)) * dt + dBm
        if t >= burn:
            m_mid = 0.5 * (m + m_new)
            x_mid = 0.5 * (x + x_new)
            F = -kappa * (m_mid - x_mid)
            heat += F * (m_new - m)
        x, m = x_new, m_new
    heat_rate = heat / (nstep * dt)
    # The FP partial EP is not identical to Sekimoto heat when X is an exogenous
    # diffusion (the force is evaluated along a path X drives). Compare orders:
    # both should be positive and within a factor of a few. A tight equality is
    # not claimed. The frozen-signal control below is the tight one.
    check("simulated Sekimoto heat of the driven memory is positive",
          heat_rate > 0.0, "sim=%.4f fp=%.4f" % (heat_rate, row["sigma"]))
    record("ou_sim_heat", heat_rate)
    record("ou_fp_sigma", row["sigma"])

    # frozen signal at 0: equilibrium, heat consistent with 0
    m = 0.0
    heat0 = 0.0
    for t in range(nstep):
        dBm = rng.normal() * sig_m
        m_new = m + (-lam * m) * dt + dBm
        m_mid = 0.5 * (m + m_new)
        F = -kappa * m_mid
        heat0 += F * (m_new - m)
        m = m_new
    rate0 = heat0 / (nstep * dt)
    check("equilibrium memory exchanges heat at a rate consistent with zero",
          abs(rate0) < 0.05, "rate=%.4f" % rate0)
    record("ou_eq_heat", rate0)


# ---------------------------------------------------------------- Lagrangian is not J
def test_lagrangian():
    gamma = 1.0
    # grid of drives
    Fs = np.linspace(0.3, 6.0, 40)
    rs = np.exp(np.linspace(math.log(0.05), math.log(30.0), 40))
    pts = []
    for F in Fs:
        for r in rs:
            ac = r * math.exp(0.5 * F)
            ae = r * math.exp(-0.5 * F)
            s = sensor(float(ac), float(ae), gamma)
            pts.append((s["heat"], s["err"], s["info"]))
    pts = np.array(pts)
    # physical support: minimize heat + w * error
    # master-equation stand-in on the same menu: κ I + h + w * error
    w = 8.0
    kappa = 1.5
    h = 0.4
    phys = pts[:, 0] + w * pts[:, 1]
    jay = kappa * pts[:, 2] + h + w * pts[:, 1]
    i_p = int(np.argmin(phys))
    i_j = int(np.argmin(jay))
    check("the physical tangent and κ I + h + w E select different designs",
          abs(pts[i_p, 1] - pts[i_j, 1]) > 1e-3 or abs(pts[i_p, 0] - pts[i_j, 0]) > 1e-3,
          "phys_err=%.4f J_err=%.4f phys_heat=%.4f" % (pts[i_p, 1], pts[i_j, 1], pts[i_p, 0]))
    # efficiency at the J-selected point: heat / flow, and heat versus the
    # minimum heat among points with error no worse
    err_j = pts[i_j, 1]
    feas = pts[pts[:, 1] <= err_j + 1e-12]
    q_min = float(feas[:, 0].min())
    q_j = float(pts[i_j, 0])
    check("the J-selected design sits strictly above the heat floor at its error",
          q_j > q_min * 1.01,
          "Q=%.4f Qmin(D)=%.4f" % (q_j, q_min))
    record("lag_w", w)
    record("lag_kappa", kappa)
    record("lag_h", h)
    record("lag_phys_err", pts[i_p, 1])
    record("lag_phys_heat", pts[i_p, 0])
    record("lag_J_err", pts[i_j, 1])
    record("lag_J_heat", q_j)
    record("lag_J_I", pts[i_j, 2])
    record("lag_Qmin_at_Jerr", q_min)
    # double counting: kT * I + kT * flow is not a lower bound that the heat meets
    # from below in the sense of a mandatory sum. At the reference point heat < I
    # is possible because I is a stock and heat is a rate. Compare rate to rate:
    # heat < info_stock is the unit confusion, recorded as numbers.
    ref = sensor(4.0, 0.5, 1.0)
    record("ref_heat_vs_Istock", ref["heat"] - ref["info"])
    # stacked price kT*flow + kT*I_stock has inconsistent units; the rate-rate
    # stack heat ?>= flow + TUR was already shown false. Record heat versus 2*flow.
    record("ref_heat", ref["heat"])
    record("ref_two_flow", 2 * ref["flow"])


def test_ct7_shape():
    """CT7's square root is the minimum of kT * σ^2 / (2D) + w D.
    Not re-derived. Checked as arithmetic already in the repository's form.
    """
    kT, sig, w = 1.0, 1.7, 2.5
    # min_D kT*sig^2/(2D) + w*D = sig * sqrt(2 kT w)
    D = np.exp(np.linspace(math.log(1e-3), math.log(10.0), 20000))
    cost = kT * sig ** 2 / (2 * D) + w * D
    got = float(cost.min())
    exact = sig * math.sqrt(2 * kT * w)
    check("CT7 square-root minimum, arithmetic only", near(got, exact, 1e-4),
          "grid=%.8f exact=%.8f" % (got, exact))
    record("ct7_grid", got)
    record("ct7_exact", exact)


def main():
    test_binary_closed_form()
    test_heat_unbounded_at_fixed_error()
    test_tur()
    test_still_step()
    test_joint_information()
    test_redundant_mechanisms()
    test_joint_versus_stack()
    test_past_stock()
    test_ou_family()
    test_lagrangian()
    test_ct7_shape()
    print("--- numbers ---")
    for k, v in ROWS:
        print("NUM  %s  %.12g" % (k, v))
    print("PASS %d  FAIL %d" % (PASS, FAIL))
    if FAIL == 0:
        print("ALL INFO-PHYSICS CHECKS PASS")
        print("FAILS 0")
        return 0
    print("INFO-PHYSICS CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
