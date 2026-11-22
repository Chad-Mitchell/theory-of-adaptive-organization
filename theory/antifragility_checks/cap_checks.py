#!/usr/bin/env python3
"""Admissible precision and turnover. Prereg: PREREG_CAP.md, lock: LOCK_CAP.txt.

Run: nice -n 19 python3 theory/antifragility_checks/cap_checks.py
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "turnover_checks", os.path.join(HERE, "turnover_checks.py")
)
turn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(turn)

N = 4
V = 4.0
W = 1.5
H = 0.5
B_CASH = 0.5
DELTA = 1.0
KT = 1.0
A = 1.0
M = 50000
EPS_CAP = 1.5
P_CAP = 0.05
REF_MF = 15.3972245773
REF_OFF = 15.473978
C_GRID = (1 / 10, 1 / 8, 1 / 6, 1 / 5, 1 / 4, 3 / 10, 3 / 8, 1 / 2, 5 / 8, 3 / 4, 1.0)
S_GRID = (0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 3, 4, 6, 8, 12, 20)
QH, QL, PI, MUT, ETA = 1.0, 0.25, 0.5, 0.25, 0.0

fails = []


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def stock_of(precision_arg):
    return 0.5 * math.log(1.0 + V * precision_arg)


def mf_identical(c, sigma):
    heat = N * KT * A * V * c
    upkeep = N * H
    if sigma == 0.0:
        return heat + upkeep + W * V, {"heat": heat, "build": 0.0, "loss": V, "phi": 0.0}
    r = sigma / (sigma + DELTA)
    phi = N * c * r
    loss = V / (1.0 + V * phi)
    build = N * sigma * (B_CASH + stock_of(c))
    return heat + upkeep + build + W * loss, {
        "heat": heat, "build": build, "loss": loss, "phi": phi,
    }


def stationary():
    probs, bal, _, _ = turn.stationary_select_or_refresh(N, ETA, "select")
    return probs, bal


def mf_hetero(c, sigma, probs, fixed_heat):
    if sigma == 0.0:
        p = turn.binomial_probs(N, PI)
    else:
        p = probs
    ek = turn.expected_k(p)
    if fixed_heat:
        heat = N * KT * A * V * c
        b_unit = B_CASH + stock_of(c)
    else:
        heat = KT * A * V * c * (ek * QH + (N - ek) * QL)
        b_unit = None
    upkeep = N * H
    if sigma == 0.0:
        return heat + upkeep + W * V, {"heat": heat, "build": 0.0, "loss": V, "phi": 0.0, "ek": ek}
    lam_h = turn.lam_of(QH, sigma, ETA, QH)
    lam_l = turn.lam_of(QL, sigma, ETA, QH)
    ah = turn.mean_alpha(lam_h, DELTA)
    al = turn.mean_alpha(lam_l, DELTA)
    phi = ek * c * QH * ah + (N - ek) * c * QL * al
    loss = V / (1.0 + V * phi)
    if fixed_heat:
        flux = ek * lam_h + (N - ek) * lam_l
        build = flux * b_unit
    else:
        # Reuse the locked build accounting at this c by scaling the stock
        # through a local copy of the select expectation.
        bh = B_CASH + 0.5 * math.log(1.0 + V * c * QH)
        bl = B_CASH + 0.5 * math.log(1.0 + V * c * QL)
        build = 0.0
        for k, pk in enumerate(p):
            if pk == 0.0:
                continue
            if k >= 1:
                p_new_h = MUT * PI + (1.0 - MUT) * (k - 1) / (N - 1)
                p_new_l = MUT * (1.0 - PI) + (1.0 - MUT) * (N - k) / (N - 1)
                build += pk * k * lam_h * (p_new_h * bh + p_new_l * bl)
            if N - k >= 1:
                p_new_h = MUT * PI + (1.0 - MUT) * k / (N - 1)
                p_new_l = MUT * (1.0 - PI) + (1.0 - MUT) * (N - k - 1) / (N - 1)
                build += pk * (N - k) * lam_l * (p_new_h * bh + p_new_l * bl)
    return heat + upkeep + build + W * loss, {
        "heat": heat, "build": build, "loss": loss, "phi": phi, "ek": ek,
    }


def draw_quality_mass(uk, U, sigma, probs):
    """Per-draw sum of q*alpha. Identical arm passes probs=None."""
    if sigma == 0.0:
        return np.zeros(M)
    if probs is None:
        beta = sigma / DELTA
        alpha = U ** (1.0 / beta)
        return alpha.sum(axis=1)
    cdf = np.cumsum(probs)
    cdf[-1] = 1.0
    k = np.clip(np.searchsorted(cdf, uk, side="left"), 0, N)
    lam_h = turn.lam_of(QH, sigma, ETA, QH)
    lam_l = turn.lam_of(QL, sigma, ETA, QH)
    mass = np.zeros(M)
    for kk in range(N + 1):
        mask = k == kk
        if not np.any(mask):
            continue
        acc = np.zeros(int(mask.sum()))
        if kk > 0:
            acc = acc + QH * (U[mask, :kk] ** (1.0 / (lam_h / DELTA))).sum(axis=1)
        if kk < N:
            acc = acc + QL * (U[mask, kk:] ** (1.0 / (lam_l / DELTA))).sum(axis=1)
        mass[mask] = acc
    return mass


def arm_seed(seed, probs):
    rng = np.random.Generator(np.random.PCG64(seed))
    uk = rng.random(M)
    U = rng.random((M, N))
    rows = []
    for sigma in S_GRID:
        mass = draw_quality_mass(uk, U, float(sigma), probs)
        for c in C_GRID:
            if probs is None:
                j_mf, meta = mf_identical(c, float(sigma))
            else:
                j_mf, meta = mf_hetero(c, float(sigma), probs, fixed_heat=False)
            loss = V / (1.0 + V * c * mass) if sigma != 0.0 else np.full(M, V)
            # The caller overwrites hetero pricing. This helper is identical-only
            # when probs is None. Hetero is handled in main.
            p_ruin = float(np.mean(loss > EPS_CAP))
            j_off = meta["heat"] + N * H + meta["build"] + W * float(loss.mean())
            se = float(W * loss.std(ddof=1) / math.sqrt(M)) if sigma != 0.0 else 0.0
            rows.append({
                "c": c, "s": float(sigma), "Jmf": j_mf, "J": j_off, "P": p_ruin,
                "se": se, "loss": loss, "adm": p_ruin <= P_CAP + 1e-15,
            })
    return rows


def hetero_arm(seed, probs, fixed_heat):
    rng = np.random.Generator(np.random.PCG64(seed))
    uk = rng.random(M)
    U = rng.random((M, N))
    rows = []
    for sigma in S_GRID:
        mass = draw_quality_mass(uk, U, float(sigma), probs if sigma != 0.0 else turn.binomial_probs(N, PI))
        # At sigma 0, mass is zeros from draw_quality_mass. Types do not affect loss.
        for c in C_GRID:
            j_mf, meta = mf_hetero(c, float(sigma), probs, fixed_heat)
            if sigma == 0.0:
                loss = np.full(M, V)
            else:
                loss = V / (1.0 + V * c * mass)
            p_ruin = float(np.mean(loss > EPS_CAP))
            j_off = meta["heat"] + N * H + meta["build"] + W * float(loss.mean())
            se = float(W * loss.std(ddof=1) / math.sqrt(M)) if sigma != 0.0 else 0.0
            rows.append({
                "c": c, "s": float(sigma), "Jmf": j_mf, "J": j_off, "P": p_ruin,
                "se": se, "loss": loss, "adm": p_ruin <= P_CAP + 1e-15,
            })
    return rows


def paired_se(a, b):
    d = a - b
    return float(W * d.std(ddof=1) / math.sqrt(M))


def report_arm(name, rows):
    print("-- %s" % name)
    for r in rows:
        print("%s c=%.6f s=%.4f Jmf=%.10f J=%.10f P=%.6f adm=%s" % (
            name, r["c"], r["s"], r["Jmf"], r["J"], r["P"], "Y" if r["adm"] else "N"))
    adm = [r for r in rows if r["adm"]]
    best_off = min(adm, key=lambda r: r["J"]) if adm else None
    best_mf = min(adm, key=lambda r: r["Jmf"]) if adm else None
    # Unconstrained official argmin, for the not-a-pass line.
    raw = min(rows, key=lambda r: r["J"])
    if raw["adm"]:
        print("%s unconstrained_official_is_admissible c=%.6f s=%.4f J=%.10f P=%.6f" % (
            name, raw["c"], raw["s"], raw["J"], raw["P"]))
    else:
        print("%s NOT A PASS unconstrained c=%.6f s=%.4f J=%.10f P=%.6f" % (
            name, raw["c"], raw["s"], raw["J"], raw["P"]))
    if best_off is None:
        print("%s admissible none" % name)
    else:
        print("%s admissible_official c=%.6f s=%.4f J=%.10f P=%.6f" % (
            name, best_off["c"], best_off["s"], best_off["J"], best_off["P"]))
        print("%s admissible_meanfield c=%.6f s=%.4f Jmf=%.10f P=%.6f" % (
            name, best_mf["c"], best_mf["s"], best_mf["Jmf"], best_mf["P"]))
    return best_off, best_mf


def main():
    print("CAP CHECKS")
    print("prereg 44c5f9978dc00a03f432c04e2b609e899cd46852")
    print("lock 32e92e5f1450bd35907df5bf8938526f8a99cdce")
    j_ref, _ = mf_identical(0.5, 1.0)
    check("validity_mf", abs(j_ref - REF_MF) < 1e-9, "J=%.10f ref=%.10f" % (j_ref, REF_MF))
    # Identical units: locked heat is kT a v c q with q=1, fixed heat is kT a v c.
    max_gap = 0.0
    for c in C_GRID:
        for s in S_GRID:
            locked_j, _ = mf_identical(c, float(s))
            # Fixed-heat expression written out, not a second call.
            heat = N * KT * A * V * c
            upkeep = N * H
            if float(s) == 0.0:
                fixed_j = heat + upkeep + W * V
            else:
                r = float(s) / (float(s) + DELTA)
                loss = V / (1.0 + V * N * c * r)
                build = N * float(s) * (B_CASH + 0.5 * math.log(1.0 + V * c))
                fixed_j = heat + upkeep + build + W * loss
            max_gap = max(max_gap, abs(locked_j - fixed_j))
    check("identical_pricings_agree", max_gap < 1e-12, "max gap %.3e" % max_gap)

    probs, bal = stationary()
    check("balance", bal, "E[k]=%.10f" % turn.expected_k(probs))

    print("\n== identical")
    ident = arm_seed(20261130, None)
    # Cross-check one mean-field value inside the sampled rows.
    ref_row = next(r for r in ident if abs(r["c"] - 0.5) < 1e-12 and r["s"] == 1.0)
    check("stream_ref_mf", abs(ref_row["Jmf"] - REF_MF) < 1e-9, "Jmf=%.10f" % ref_row["Jmf"])
    best_i, best_i_mf = report_arm("identical", ident)

    print("\n== hetero locked coupling")
    locked = hetero_arm(20261131, probs, False)
    best_l, best_l_mf = report_arm("locked", locked)

    print("\n== hetero fixed heat")
    fixed = hetero_arm(20261132, probs, True)
    best_f, best_f_mf = report_arm("fixed", fixed)

    print("\n== Q1")
    beats_mf = []
    beats_off = []
    for r in ident:
        if not r["adm"]:
            continue
        if r["Jmf"] < REF_MF - 1e-12:
            beats_mf.append(r)
        if r["J"] < REF_OFF:
            gap = ref_row["J"] - r["J"]
            se = paired_se(r["loss"], ref_row["loss"])
            if gap > 2.0 * se and r["J"] < REF_OFF:
                beats_off.append((r, gap, se))
    if beats_mf:
        winner = min(beats_mf, key=lambda r: r["Jmf"])
        print("Q1 mean-field YES c=%.6f s=%.4f Jmf=%.10f P=%.6f n=%d" % (
            winner["c"], winner["s"], winner["Jmf"], winner["P"], len(beats_mf)))
    else:
        print("Q1 mean-field NO")
    if beats_off:
        winner, gap, se = min(beats_off, key=lambda t: t[0]["J"])
        print("Q1 official YES c=%.6f s=%.4f J=%.10f P=%.6f gap=%.6f se=%.6f n=%d" % (
            winner["c"], winner["s"], winner["J"], winner["P"], gap, se, len(beats_off)))
    else:
        print("Q1 official NO")

    def compare(name, rows, best):
        if best is None:
            print("%s no admissible point" % name)
            return
        zero = next(r for r in rows if abs(r["c"] - best["c"]) < 1e-12 and r["s"] == 0.0)
        print("%s vs reference J-15.473978=%.6f vs own zero J-J0=%.6f (zero P=%.6f, not admissible)" % (
            name, best["J"] - REF_OFF, best["J"] - zero["J"], zero["P"]))

    print("\n== Q2 Q3")
    compare("Q2 locked official", locked, best_l)
    if best_l_mf is not None:
        zero = next(r for r in locked if abs(r["c"] - best_l_mf["c"]) < 1e-12 and r["s"] == 0.0)
        print("Q2 locked meanfield Jmf=%.10f vs ref mf %.6f vs own zero %.6f" % (
            best_l_mf["Jmf"], best_l_mf["Jmf"] - REF_MF, best_l_mf["Jmf"] - zero["Jmf"]))
    compare("Q3 fixed official", fixed, best_f)
    if best_f_mf is not None:
        zero = next(r for r in fixed if abs(r["c"] - best_f_mf["c"]) < 1e-12 and r["s"] == 0.0)
        print("Q3 fixed meanfield Jmf=%.10f vs ref mf %.6f vs own zero %.6f" % (
            best_f_mf["Jmf"], best_f_mf["Jmf"] - REF_MF, best_f_mf["Jmf"] - zero["Jmf"]))

    print("\nFAILS %d" % len(fails))
    if fails:
        print("CAP CHECKS FAILED " + ", ".join(fails))
        return 1
    print("ALL CAP CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
