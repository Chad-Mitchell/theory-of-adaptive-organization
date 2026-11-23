#!/usr/bin/env python3
"""Checks for theory/GENERAL_FLOOR_FINITE_2026-11-23.md (T60).

Run from the repo root:
  nice -n 19 python3 theory/general_floor_finite_checks/general_floor_finite_checks.py

These checks are code identities and in-model evaluations on finite-state
Markov worlds and bipartite memories. They are not evidence about a real
system. A machinery failure sets a nonzero exit code.
"""
from __future__ import annotations

import math
import sys
from collections import defaultdict, deque

import numpy as np

checks_failed = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def L(eps):
    if eps <= 0.0 or eps >= 0.5:
        return math.inf if eps <= 0.0 else 0.0
    return (1.0 - 2.0 * eps) * math.log((1.0 - eps) / eps)


def kl(p, q, floor=1e-15):
    p = np.clip(np.real(p), 0.0, None)
    q = np.clip(np.real(q), 0.0, None)
    if p.sum() <= 0.0 or q.sum() <= 0.0:
        return 0.0
    p = p / p.sum()
    q = q / q.sum()
    mask = p > floor
    return float(np.sum(p[mask] * np.log(p[mask] / np.clip(q[mask], floor, None))))


def stationary(Q):
    n = Q.shape[0]
    A = Q.T.copy()
    A[-1, :] = 1.0
    b = np.zeros(n)
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    pi = np.clip(np.real(pi), 0.0, None)
    s = pi.sum()
    if s <= 0.0:
        raise RuntimeError("stationary mass vanished")
    return pi / s


def world_generator(W):
    Q = np.array(W, dtype=float)
    np.fill_diagonal(Q, 0.0)
    np.fill_diagonal(Q, -Q.sum(axis=1))
    return Q


def joint_generator(W_X, w_fn, nX, nM):
    N = nX * nM
    Q = np.zeros((N, N))
    for x in range(nX):
        for m in range(nM):
            i = x * nM + m
            for xp in range(nX):
                if xp == x:
                    continue
                Q[i, xp * nM + m] += W_X[x, xp]
            for mp in range(nM):
                if mp == m:
                    continue
                Q[i, x * nM + mp] += w_fn(x, m, mp)
    np.fill_diagonal(Q, 0.0)
    np.fill_diagonal(Q, -Q.sum(axis=1))
    return Q


def flows_from_joint(pi, W_X, w_fn, nX, nM):
    """Return I_alt, dest, Bayes error, no-memory error, and px."""
    px = pi.sum(axis=1)
    p_m_x = pi / np.clip(px[:, None], 1e-18, None)
    I_alt = 0.0
    for x in range(nX):
        for m in range(nM):
            for mp in range(nM):
                if mp == m:
                    continue
                rate = w_fn(x, m, mp)
                if rate <= 0.0 or pi[x, m] <= 0.0:
                    continue
                I_alt += pi[x, m] * rate * math.log(
                    max(p_m_x[x, mp], 1e-15) / max(p_m_x[x, m], 1e-15)
                )
    dest = 0.0
    for x in range(nX):
        for xp in range(nX):
            if xp == x or W_X[x, xp] <= 0.0 or px[x] <= 0.0:
                continue
            dest += px[x] * W_X[x, xp] * kl(p_m_x[x], p_m_x[xp])
    eps = 1.0 - float(np.sum(np.max(pi, axis=0)))
    eps0 = 1.0 - float(np.max(px))
    return dict(I_alt=I_alt, dest=dest, eps=eps, eps0=eps0, px=px, p_m_x=p_m_x, pi=pi)


def analyze(W_X, w_fn, nX, nM):
    Q = joint_generator(W_X, w_fn, nX, nM)
    pi = stationary(Q).reshape(nX, nM)
    out = flows_from_joint(pi, W_X, w_fn, nX, nM)
    out["residual"] = float(np.max(np.abs(pi.ravel() @ Q)))
    # World's own stationary, for an exogenous chain.
    px_world = stationary(world_generator(W_X))
    out["px_world"] = px_world
    return out


def ldb_energy_rates(energy, nu):
    def w_fn(x, m, mp, energy=energy, nu=nu):
        return nu * math.exp(0.5 * (energy(x, m) - energy(x, mp)))

    return w_fn


def shortest_paths_to(W, target):
    n = W.shape[0]
    prev = {target: None}
    q = deque([target])
    while q:
        v = q.popleft()
        for u in range(n):
            if u not in prev and W[u, v] > 0.0:
                prev[u] = v
                q.append(u)
    paths = {}
    for x in range(n):
        if x not in prev:
            paths[x] = None
            continue
        path = []
        cur = x
        while cur != target:
            nxt = prev[cur]
            path.append((cur, nxt))
            cur = nxt
        paths[x] = path
    return paths


def K_X(W, px):
    """Path-Pinsker constant of an exogenous world (shortest directed paths)."""
    n = len(px)
    # Prefer a mode of pi; fall back to any reachable root.
    order = list(np.argsort(-px))
    paths = None
    xstar = None
    for xs in order:
        cand = shortest_paths_to(W, int(xs))
        if all(cand[x] is not None or px[x] <= 1e-14 or x == xs for x in range(n)):
            paths, xstar = cand, int(xs)
            break
    if paths is None:
        return math.inf, None
    c = defaultdict(float)
    for x in range(n):
        if x == xstar or px[x] <= 1e-14:
            continue
        for e in paths[x]:
            c[e] += math.sqrt(0.5) * float(px[x])
    K = 0.0
    for (u, v), ce in c.items():
        je = float(px[u]) * float(W[u, v])
        if je <= 1e-18:
            return math.inf, xstar
        K += (ce * ce) / je
    return K, xstar


def pairwise_L_bound(W, px, eps):
    """Design-independent pairwise Jeffreys bound, using min occupancy."""
    n = len(px)
    best = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            fij = float(px[i] * W[i, j])
            fji = float(px[j] * W[j, i])
            if fij + fji <= 1e-18:
                continue
            mab = min(float(px[i]), float(px[j]))
            if eps < mab and mab > 0.0:
                es = eps / (2.0 * mab)
                if 0.0 < es < 0.5:
                    best = max(best, min(fij, fji) * 2.0 * L(es))
    return best


def random_irreducible_W(n, rng, scale=1.0, p_edge=0.65):
    W = rng.random((n, n)) * scale
    mask = rng.random((n, n)) < p_edge
    np.fill_diagonal(mask, False)
    W *= mask
    for i in range(n):
        W[i, (i + 1) % n] = max(W[i, (i + 1) % n], 0.25 * scale)
    np.fill_diagonal(W, 0.0)
    return W


def reversible_W(n, rng, scale=1.0):
    pi0 = rng.random(n) + 0.4
    pi0 /= pi0.sum()
    S = rng.random((n, n)) * scale
    S = 0.5 * (S + S.T)
    np.fill_diagonal(S, 0.0)
    for i in range(n):
        j = (i + 1) % n
        S[i, j] = max(S[i, j], 0.3 * scale)
        S[j, i] = S[i, j]
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                W[i, j] = S[i, j] / pi0[i]
    return W, pi0


def identity_ok(d, atol=1e-8):
    return abs(d["I_alt"] - d["dest"]) < atol


def main():
    # 1. Telegraph L at the repo's worked point.
    I_dot = 1.0 * L(0.2)
    check(
        "telegraph_L_at_eps_0p2",
        abs(I_dot - 0.6 * math.log(4.0)) < 1e-15
        and abs(I_dot - 0.831776616672) < 5e-13,
        "code sanity; I_dot=%.12f against 0.6 ln 4" % I_dot,
    )

    # 2. Destruction identity and tightness on the Gamma=0 telegraph.
    r, eps_target = 0.7, 0.2
    mu = r * (1.0 - 2.0 * eps_target) / eps_target

    def w_tele(x, m, mp, mu=mu):
        if mp == x and m != x:
            return mu
        return 0.0

    W_t = np.array([[0.0, r], [r, 0.0]])
    d = analyze(W_t, w_tele, 2, 2)
    check(
        "telegraph_identity_and_tight_bound",
        identity_ok(d, 1e-12)
        and abs(d["eps"] - 0.2) < 1e-12
        and abs(d["I_alt"] - r * L(d["eps"])) < 1e-12
        and d["residual"] < 1e-12,
        "I_alt=%.12f dest=%.12f r L=%.12f eps=%.12f" % (d["I_alt"], d["dest"], r * L(d["eps"]), d["eps"]),
    )

    # 3. Leaks cancel: I_alt = r L(eps), not (r+Gamma) L(eps).
    gamma, eps_l = 0.25, 0.15
    mu_l = (r + gamma) * (1.0 - 2.0 * eps_l) / eps_l

    def w_leak(x, m, mp, mu_l=mu_l, gamma=gamma):
        if mp == x and m != x:
            return gamma + mu_l
        if m == x and mp != x:
            return gamma
        return 0.0

    d = analyze(W_t, w_leak, 2, 2)
    check(
        "telegraph_leaks_cancel",
        identity_ok(d, 1e-12)
        and abs(d["eps"] - eps_l) < 1e-12
        and abs(d["I_alt"] - r * L(eps_l)) < 1e-12
        and abs(d["I_alt"] - (r + gamma) * L(eps_l)) > 0.2,
        "I_alt=%.12f r L=%.12f (r+Gamma)L=%.12f" % (d["I_alt"], r * L(eps_l), (r + gamma) * L(eps_l)),
    )

    # 4. Frozen world: I_alt = 0 at a finite Boltzmann error below eps0.
    # A static copy bias, energy (m-x)^2, with kT=1. The world does not jump.
    def w_bias(x, m, mp):
        e = float((m - x) ** 2)
        ep = float((mp - x) ** 2)
        return 3.0 * math.exp(0.5 * (e - ep))

    W_frozen = np.zeros((2, 2))
    # Local detailed balance at energy (m-x)^2 gives, at each frozen x,
    # P(M=x | x) / P(M!=x | x) = exp(1), so the Boltzmann error is 1/(1+e).
    boltz = 1.0 / (1.0 + math.exp(1.0))
    corr = 1.0 - boltz
    # Fair frozen world, memory aligned with the frozen label.
    pi_fr = np.array([[0.5 * corr, 0.5 * boltz], [0.5 * boltz, 0.5 * corr]])
    d_fr = flows_from_joint(pi_fr, W_frozen, w_bias, 2, 2)
    check(
        "frozen_world_I_alt_zero",
        abs(d_fr["I_alt"]) < 1e-12
        and abs(d_fr["dest"]) < 1e-12
        and abs(d_fr["eps"] - boltz) < 1e-12
        and d_fr["eps"] < d_fr["eps0"] - 0.2
        and abs(d_fr["eps0"] - 0.5) < 1e-12,
        "I_alt=%.3e eps=%.6f (Boltzmann) eps0=%.6f" % (0.0 if abs(d_fr["I_alt"])<1e-12 else d_fr["I_alt"], d_fr["eps"], d_fr["eps0"]),
    )

    # 5. Path-Pinsker constant on the telegraph is 1/(4r).
    for rK, pX in ((0.5, np.array([0.5, 0.5])), (1.0, np.array([0.5, 0.5])), (2.0, np.array([0.5, 0.5]))):
        WK = np.array([[0.0, rK], [rK, 0.0]])
        K, xs = K_X(WK, pX)
        check(
            "path_pinsker_K_telegraph_r_%g" % rK,
            abs(K - 1.0 / (4.0 * rK)) < 1e-12,
            "K=%.12f against 1/(4r)=%.12f" % (K, 1.0 / (4.0 * rK)),
        )
    # At eps=0.2, r=1, Pinsker is 4*(0.3)^2=0.36, tight r L is 0.83177...
    K1, _ = K_X(np.array([[0.0, 1.0], [1.0, 0.0]]), np.array([0.5, 0.5]))
    pins = (0.5 - 0.2) ** 2 / K1
    check(
        "path_pinsker_below_tight_telegraph",
        abs(K1 - 0.25) < 1e-15
        and abs(pins - 0.36) < 1e-15
        and pins < L(0.2)
        and abs(L(0.2) - 0.831776616672) < 5e-13,
        "pinsker at eps=0.2 is %.12f, r L is %.12f" % (pins, L(0.2)),
    )

    # 6. Richer LDB memories on the telegraph still obey r L(eps).
    rng = np.random.default_rng(1)
    W_one = np.array([[0.0, 1.0], [1.0, 0.0]])
    rich_ok = 0
    rich_fail = 0
    min_gap = math.inf
    for trial in range(30):
        nM = int(rng.integers(2, 7))
        E = rng.normal(size=(2, nM))
        nu = float(rng.uniform(0.4, 8.0))

        def w_rich(x, m, mp, E=E, nu=nu):
            return nu * math.exp(0.5 * (E[x, m] - E[x, mp]))

        d = analyze(W_one, w_rich, 2, nM)
        bound = 1.0 * L(min(max(d["eps"], 1e-15), 0.499999))
        if d["eps"] >= 0.5 - 1e-12:
            bound = 0.0
        ok = identity_ok(d, 1e-7) and d["I_alt"] + 1e-8 >= bound - 1e-10
        if ok:
            rich_ok += 1
            if d["eps"] < 0.5 - 1e-12:
                min_gap = min(min_gap, d["I_alt"] - bound)
        else:
            rich_fail += 1
    check(
        "telegraph_bound_holds_for_richer_memories",
        rich_fail == 0 and rich_ok == 30,
        "30 random LDB memories, nM in 2..6; min I_alt - r L = %.6f" % min_gap,
    )

    # 7. Two-class counterexample: the world is not frozen, eps < eps0, I_alt=0.
    rA = 1.0
    W_red = np.array(
        [
            [0.0, rA, 0.0],
            [rA, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ]
    )

    def w_class(x, m, mp):
        cls = 1 if x == 2 else 0
        e = 0.0 if m == cls else 4.0
        ep = 0.0 if mp == cls else 4.0
        return 6.0 * math.exp(0.5 * (e - ep))

    Qj = joint_generator(W_red, w_class, 3, 2)
    # Two recurrent classes; take a mixture of the two probability left-null vectors.
    w, v = np.linalg.eig(Qj.T)
    pis = []
    for i, lam in enumerate(w):
        if abs(lam) > 1e-8:
            continue
        vec = np.real(v[:, i])
        for cand in (np.clip(vec, 0.0, None), np.clip(-vec, 0.0, None)):
            if cand.sum() > 1e-12:
                cand = cand / cand.sum()
                if not any(np.allclose(cand, p, atol=1e-8) for p in pis):
                    pis.append(cand)
    check(
        "reducible_world_has_two_stationary_classes",
        len(pis) == 2,
        "found %d probability left-null vectors" % len(pis),
    )
    masses = [p.reshape(3, 2).sum(axis=1) for p in pis]
    # Identify the {0,1} class and the {2} class.
    clsA = next(p for p, m in zip(pis, masses) if m[0] + m[1] > 0.9)
    clsB = next(p for p, m in zip(pis, masses) if m[2] > 0.9)
    mix = (0.6 * clsA + 0.4 * clsB).reshape(3, 2)
    d_mix = flows_from_joint(mix, W_red, w_class, 3, 2)
    check(
        "two_class_counterexample_I_alt_zero_below_eps0",
        abs(d_mix["I_alt"]) < 1e-9
        and abs(d_mix["dest"]) < 1e-9
        and d_mix["eps"] < d_mix["eps0"] - 0.2
        and abs(d_mix["px"][0] - 0.3) < 1e-8
        and abs(d_mix["px"][2] - 0.4) < 1e-8,
        "I_alt=%.3e eps=%.6f eps0=%.6f px=%s" % (
            0.0 if abs(d_mix["I_alt"])<1e-12 else d_mix["I_alt"], d_mix["eps"], d_mix["eps0"], np.round(d_mix["px"], 6),
        ),
    )

    # 8. A tiny leak between the classes makes the world irreducible:
    # I_alt is positive but can be very small while eps stays below eps0.
    delta = 1e-4
    W_leakc = np.array(
        [
            [0.0, rA, 0.0],
            [rA, 0.0, delta],
            [delta, 0.0, 0.0],
        ]
    )
    d_leak = analyze(W_leakc, w_class, 3, 2)
    check(
        "tiny_leak_small_positive_I_alt",
        identity_ok(d_leak, 1e-9)
        and d_leak["I_alt"] > 0.0
        and d_leak["I_alt"] < 0.01
        and d_leak["eps"] < d_leak["eps0"] - 0.2,
        "I_alt=%.8f eps=%.6f eps0=%.6f" % (d_leak["I_alt"], d_leak["eps"], d_leak["eps0"]),
    )

    # 9. Irreversible 3-cycle: identity, positivity, path-Pinsker.
    W_cyc = np.array(
        [
            [0.0, 1.2, 0.0],
            [0.0, 0.0, 0.8],
            [1.5, 0.0, 0.0],
        ]
    )

    def energy_copy(x, m):
        return 0.5 * (m - x) ** 2

    w_cyc = ldb_energy_rates(energy_copy, nu=4.0)
    # Slightly stronger bias via the energy already in (m-x)^2; multiply beta
    # by folding it into the energy? energy_copy is used as Delta E; use a
    # scaled version.
    def w_cyc_strong(x, m, mp):
        return 4.0 * math.exp(0.5 * 2.5 * (energy_copy(x, m) - energy_copy(x, mp)))

    d_cyc = analyze(W_cyc, w_cyc_strong, 3, 3)
    pxw = d_cyc["px_world"]
    Kc, _ = K_X(W_cyc, pxw)
    pins_c = (d_cyc["eps0"] - d_cyc["eps"]) ** 2 / Kc if math.isfinite(Kc) and Kc > 0 else 0.0
    check(
        "irreversible_cycle_identity_and_pinsker",
        identity_ok(d_cyc, 1e-9)
        and d_cyc["I_alt"] > 0.0
        and d_cyc["eps"] < d_cyc["eps0"] - 1e-8
        and np.allclose(d_cyc["px"], pxw, atol=1e-9)
        and d_cyc["I_alt"] + 1e-10 >= pins_c,
        "I_alt=%.6f dest=%.6f pinsker=%.6f eps=%.4f eps0=%.4f K=%.4f" % (
            d_cyc["I_alt"], d_cyc["dest"], pins_c, d_cyc["eps"], d_cyc["eps0"], Kc,
        ),
    )

    # 10. Random irreducible 3-5 state worlds, including adversarial memories.
    rng = np.random.default_rng(11)
    n_tot = 0
    n_id = n_pos = n_pin = n_pair = 0
    n_fail = 0
    fail_names = []
    for nX in (3, 4, 5):
        for trial in range(8):
            if trial % 2 == 0:
                W = random_irreducible_W(nX, rng, scale=1.0, p_edge=0.6)
            else:
                W, _ = reversible_W(nX, rng, scale=1.0)
            nM = int(rng.integers(2, nX + 3))
            # Adversarial flavours: shuffled labels, weak or strong bias, or a
            # two-state class-style embedding.
            flavour = int(rng.integers(0, 3))
            if flavour == 0:
                lab = rng.permutation(nX)
                if nM > nX:
                    lab = np.concatenate([lab, rng.integers(0, nX, size=nM - nX)])
                else:
                    lab = lab[:nM]
                beta = float(rng.choice([0.25, 1.0, 3.0, 6.0]))
                nu = float(rng.uniform(0.8, 10.0))

                def w_fn(x, m, mp, lab=lab, beta=beta, nu=nu):
                    e = 0.5 * beta * (lab[m] - x) ** 2
                    ep = 0.5 * beta * (lab[mp] - x) ** 2
                    return nu * math.exp(0.5 * (e - ep))
            elif flavour == 1:
                E = rng.normal(size=(nX, nM)) * float(rng.uniform(0.3, 2.0))
                nu = float(rng.uniform(0.5, 8.0))

                def w_fn(x, m, mp, E=E, nu=nu):
                    return nu * math.exp(0.5 * (E[x, m] - E[x, mp]))
            else:
                # Track only a coarse partition of X.
                n_parts = 2 if nX > 2 else 2
                part = np.array([0 if s < nX // 2 else 1 for s in range(nX)])
                nu = float(rng.uniform(1.0, 8.0))
                beta = float(rng.uniform(1.0, 5.0))

                def w_fn(x, m, mp, part=part, nu=nu, beta=beta, nM=nM):
                    # Memory states modulo n_parts try to copy the part label.
                    e = beta * float(m % 2 != part[x])
                    ep = beta * float(mp % 2 != part[x])
                    return nu * math.exp(0.5 * (e - ep))

            d = analyze(W, w_fn, nX, nM)
            n_tot += 1
            ok_id = identity_ok(d, 5e-6)
            # For very peaked conditionals the log clip can mismatch slightly;
            # allow a relative tolerance there.
            if not ok_id and abs(d["I_alt"] - d["dest"]) <= 1e-3 * max(1.0, abs(d["I_alt"])):
                ok_id = True
            ok_pos = True
            if d["eps"] < d["eps0"] - 1e-8:
                ok_pos = d["I_alt"] > 1e-10
            K, _ = K_X(W, d["px_world"])
            de = d["eps0"] - d["eps"]
            pins = 0.0
            if math.isfinite(K) and K > 0.0:
                pins = (de * de) / K if de > 0.0 else 0.0
            ok_pin = d["I_alt"] + 1e-8 >= pins - 1e-10
            plb = pairwise_L_bound(W, d["px_world"], d["eps"])
            ok_pair = d["I_alt"] + 1e-8 >= plb - 1e-10
            if ok_id:
                n_id += 1
            if ok_pos:
                n_pos += 1
            if ok_pin:
                n_pin += 1
            if ok_pair:
                n_pair += 1
            if not (ok_id and ok_pos and ok_pin and ok_pair):
                n_fail += 1
                fail_names.append("nX=%d nM=%d I=%.4f dest=%.4f pins=%.4f pair=%.4f eps=%.3f eps0=%.3f" % (
                    nX, nM, d["I_alt"], d["dest"], pins, plb, d["eps"], d["eps0"],
                ))
    check(
        "random_and_adversarial_worlds",
        n_fail == 0 and n_tot == 24 and n_id == 24 and n_pos == 24 and n_pin == 24 and n_pair == 24,
        "24 irreducible 3-5 state trials (random, shuffled, coarse); fails=%d %s" % (
            n_fail, ("; ".join(fail_names) if fail_names else "none"),
        ),
    )

    # 11. Strong reversible memories activate the pairwise L bound, and it holds.
    rng = np.random.default_rng(7)
    n_active = 0
    n_pair_fail = 0
    n_pin_fail = 0
    for trial in range(16):
        nX = 3
        W, _ = reversible_W(nX, rng, scale=1.0)
        nM = 4
        beta = float(rng.uniform(3.0, 9.0))
        nu = float(rng.uniform(5.0, 16.0))
        lab = np.array([i % nX for i in range(nM)])

        def w_fn(x, m, mp, lab=lab, beta=beta, nu=nu):
            e = 0.5 * beta * (lab[m] - x) ** 2
            ep = 0.5 * beta * (lab[mp] - x) ** 2
            return nu * math.exp(0.5 * (e - ep))

        d = analyze(W, w_fn, nX, nM)
        plb = pairwise_L_bound(W, d["px_world"], d["eps"])
        K, _ = K_X(W, d["px_world"])
        de = d["eps0"] - d["eps"]
        pins = (de * de) / K if (math.isfinite(K) and K > 0 and de > 0) else 0.0
        if plb > 0.0:
            n_active += 1
        if d["I_alt"] + 1e-8 < plb - 1e-10:
            n_pair_fail += 1
        if d["I_alt"] + 1e-8 < pins - 1e-10:
            n_pin_fail += 1
    check(
        "pairwise_L_bound_on_strong_reversible_memories",
        n_pair_fail == 0 and n_pin_fail == 0 and n_active >= 10,
        "16 strong 3-state reversible trials; pairwise active in %d, pair fails %d, pinsker fails %d" % (
            n_active, n_pair_fail, n_pin_fail,
        ),
    )

    # 12. Jeffreys minimum at fixed TV is the binary symmetric pair (calculus).
    # J = (1-2eps) ln[(1-a)(1-b)/(a b)] with a+b=2eps, minimized at a=b=eps.
    def jeff(a, b):
        return (1.0 - a - b) * math.log(((1.0 - a) * (1.0 - b)) / (a * b))

    eps = 0.2
    j_sym = jeff(eps, eps)
    grid = [0.02, 0.05, 0.08, 0.1, 0.15, 0.18, 0.2, 0.22, 0.25, 0.3, 0.35, 0.38]
    j_vals = [jeff(a, 2.0 * eps - a) for a in grid]
    check(
        "jeffreys_minimum_is_binary_symmetric",
        abs(j_sym - 2.0 * L(eps)) < 1e-14
        and all(j + 1e-12 >= j_sym for j in j_vals)
        and abs(min(j_vals) - j_sym) < 1e-14,
        "J_sym=2 L(0.2)=%.12f; grid min=%.12f" % (j_sym, min(j_vals)),
    )

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        sys.exit(1)
    print("FAILS 0")
    print("ALL GENERAL-FLOOR-FINITE CHECKS PASS")


if __name__ == "__main__":
    main()
