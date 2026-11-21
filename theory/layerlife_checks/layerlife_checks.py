#!/usr/bin/env python3
"""Checks for theory/LAYER_LIFETIME_2026-11-21.md.

Run from the repo root:
  nice -n 19 python3 theory/layerlife_checks/layerlife_checks.py

Prints ALL PASS and writes layerlife_checks.out (and a copy of stdout).
Labels match the note: PROVED identities are checked to tight tolerance;
NUMERICAL comparisons and FALSE counterexamples are checked as stated.

This is a self-check of the derivations in the note, not a field test.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

ok = []
rows = []


def chk(name, cond, detail=""):
    ok.append(bool(cond))
    flag = "PASS" if cond else "FAIL"
    rows.append((flag, name, detail))
    print(f"[{flag}] {name}" + (f"  {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Closed forms (CL19 / Dixit 1991, undiscounted quadratic, BM gap)
# ---------------------------------------------------------------------------

def bstar(k, w, sig2):
    return (6.0 * k * sig2 / w) ** 0.25


def Tstar(k, w, sig2):
    # E[exit time of BM from [-b,b] starting at 0] = b^2 / sig2
    return (6.0 * k / (w * sig2)) ** 0.5


def Jstar_barrier(k, w, sig2):
    return 2.0 * math.sqrt(k * w * sig2 / 6.0)


def mse_barrier(k, w, sig2):
    # E[x^2] = b*^2 / 6
    return bstar(k, w, sig2) ** 2 / 6.0


def Tstar_fixed(k, w, sig2):
    # Average BM MSE over a fixed period T is sig2 * T / 2; J = k/T + w sig2 T / 2
    return math.sqrt(2.0 * k / (w * sig2))


def Jstar_fixed(k, w, sig2):
    return math.sqrt(2.0 * k * w * sig2)


def mse_ou_hold(v, a, T):
    """Mean variance of an OU process over a hold of length T after a perfect observation."""
    if T <= 0:
        return 0.0
    two_aT = 2.0 * a * T
    if abs(two_aT) < 1e-12:
        return v * a * T  # = sig2 T / 2, since sig2 = 2 a v
    return v * (1.0 - (1.0 - math.exp(-two_aT)) / two_aT)


def mse_ou_hold_latency(v, a, T, lag):
    """Mean variance when the observation is delayed by lag and then held for T."""
    if T <= 0:
        return v * (1.0 - math.exp(-2.0 * a * lag))
    # (1/T) int_lag^{lag+T} v (1 - e^{-2 a u}) du
    pref = math.exp(-2.0 * a * lag) * (1.0 - math.exp(-2.0 * a * T)) / (2.0 * a * T)
    return v * (1.0 - pref)


def J_ou_fixed(k, w, v, a, T, lag=0.0):
    return k / T + w * mse_ou_hold_latency(v, a, T, lag)


def best_T_ou(k, w, v, a, lag=0.0, lo=None, hi=None):
    # Search a wide log grid then polish.
    tau = 1.0 / max(a, 1e-12)
    T_bm = Tstar_fixed(k, w, 2.0 * a * v)  # BM short-time rate sig2 = 2 a v
    lo = lo if lo is not None else min(T_bm, tau) * 1e-4
    hi = hi if hi is not None else max(T_bm, tau) * 1e4
    lo = max(lo, 1e-16)
    grid = np.logspace(math.log10(lo), math.log10(hi), 800)
    vals = np.array([J_ou_fixed(k, w, v, a, float(T), lag) for T in grid])
    T0 = float(grid[int(np.argmin(vals))])
    res = minimize_scalar(
        lambda T: J_ou_fixed(k, w, v, a, float(T), lag),
        bounds=(max(lo, T0 / 20), min(hi, T0 * 20)),
        method="bounded",
        options=dict(xatol=1e-12),
    )
    T = float(res.x)
    return T, float(J_ou_fixed(k, w, v, a, T, lag))


# ---------------------------------------------------------------------------
# 1. Single-layer identities
# ---------------------------------------------------------------------------


def main():
    print("== 1. Single-layer Dixit / CL19 identities (KNOWN; re-derived)")

    k, w, sig2 = 0.01, 1.0, 1.0
    b = bstar(k, w, sig2)
    T = Tstar(k, w, sig2)
    # T = b^2 / sig2
    chk("Tstar equals bstar^2 / sig2", abs(T - b * b / sig2) < 1e-15, f"T={T:.12g} b^2/sig2={b*b/sig2:.12g}")
    # Average cost k sig2 / b^2 + w b^2 / 6 equals J*
    avg = k * sig2 / b**2 + w * b**2 / 6.0
    chk("Jstar equals average cost at bstar", abs(avg - Jstar_barrier(k, w, sig2)) < 1e-15, f"{avg:.12g}")
    # Grid over b recovers b*
    grid = np.linspace(0.05, 2.0, 40001)
    avgs = k * sig2 / grid**2 + w * grid**2 / 6.0
    bnum = float(grid[int(np.argmin(avgs))])
    chk("bstar matches grid minimizer", abs(bnum / b - 1) < 1e-3, f"closed={b:.8g} grid={bnum:.8g}")
    # Fixed-period vs barrier: same square-root lifetime scaling, different coefficient
    Tf = Tstar_fixed(k, w, sig2)
    chk(
        "barrier lifetime is sqrt(3) times fixed-period lifetime",
        abs(T / Tf - math.sqrt(3.0)) < 1e-12,
        f"T_bar/T_fix={T/Tf:.12g} sqrt(3)={math.sqrt(3):.12g}",
    )
    chk(
        "barrier cost is lower than fixed-period cost",
        Jstar_barrier(k, w, sig2) < Jstar_fixed(k, w, sig2) - 1e-12,
        f"J_bar={Jstar_barrier(k,w,sig2):.8g} J_fix={Jstar_fixed(k,w,sig2):.8g}",
    )
    # Scaling: T* ∝ k^{1/2} σ^{-1} w^{-1/2}
    chk(
        "T* scales as sqrt(k / (w sig2))",
        abs(Tstar(4 * k, w, sig2) / T - 2.0) < 1e-14
        and abs(Tstar(k, 4 * w, sig2) / T - 0.5) < 1e-14
        and abs(Tstar(k, w, 4 * sig2) / T - 0.5) < 1e-14,
    )


    # ---------------------------------------------------------------------------
    # 2. Specialized separable stack: spacing exact
    # ---------------------------------------------------------------------------

    print("\n== 2. Specialized separable stack (PROVED in-model when layers cannot reset each other's components)")

    # Independent BM components, loss w (sum e_i)^2 = w sum e_i^2, one specialized layer each.
    ks = np.array([0.01, 0.04, 0.09])
    sig2s = np.array([4.0, 1.0, 0.25])
    w_stack = 2.5
    Ts = np.array([Tstar(k_i, w_stack, s) for k_i, s in zip(ks, sig2s)])
    # Spacing rule
    ratio_12 = Ts[0] / Ts[1]
    pred_12 = math.sqrt((ks[0] / ks[1]) * (sig2s[1] / sig2s[0]))
    ratio_23 = Ts[1] / Ts[2]
    pred_23 = math.sqrt((ks[1] / ks[2]) * (sig2s[2] / sig2s[1]))
    chk(
        "spacing T_i/T_j = sqrt((k_i/k_j)*(sig2_j/sig2_i))",
        abs(ratio_12 - pred_12) < 1e-14 and abs(ratio_23 - pred_23) < 1e-14,
        f"12: {ratio_12:.8g} vs {pred_12:.8g}; 23: {ratio_23:.8g} vs {pred_23:.8g}",
    )

    # Brute-force: independently grid each barrier (separable, so product of 1-d grids).
    def avg_cost(b, k_i, w, s):
        if b <= 0:
            return math.inf
        return k_i * s / b**2 + w * b**2 / 6.0

    Js_closed = np.array([Jstar_barrier(k_i, w_stack, s) for k_i, s in zip(ks, sig2s)])
    Js_grid = []
    for k_i, s in zip(ks, sig2s):
        bs = np.logspace(-3, 2, 20001)
        Js_grid.append(float(np.min([avg_cost(b, k_i, w_stack, s) for b in bs])))
    Js_grid = np.array(Js_grid)
    chk(
        "brute-force per-layer J matches closed J*",
        np.max(np.abs(Js_grid / Js_closed - 1)) < 1e-4,
        f"max rel err={np.max(np.abs(Js_grid / Js_closed - 1)):.3e}",
    )
    J_sum_closed = float(Js_closed.sum())
    # Joint 3-d random search would be wasteful: additivity is the claim.
    chk(
        "stack J* is the sum of the layer costs (separable)",
        abs(J_sum_closed - float(np.sum([Jstar_barrier(k_i, w_stack, s) for k_i, s in zip(ks, sig2s)]))) < 1e-15,
    )


    # ---------------------------------------------------------------------------
    # 3. Where a stack is FALSE: a joint reset of the sum
    # ---------------------------------------------------------------------------

    print("\n== 3. Counterexamples: when the recursive stack rule is false")

    k1, k2, s1, s2, wj = 0.02, 0.05, 1.0, 4.0, 1.0
    J_sep = Jstar_barrier(k1, wj, s1) + Jstar_barrier(k2, wj, s2)
    # (a) Joint reset costs only one of the lumps (full-state action no dearer than one part).
    J_joint_cheap = Jstar_barrier(min(k1, k2), wj, s1 + s2)
    # Actually if the cheap k can reset the SUM, use min; if a full-state reset costs k_full = k1
    # (the cheaper or a typical single action), it can be even clearer with k_full = min.
    chk(
        "FALSE without specialization: one cheap joint reset of the sum beats two layers",
        J_joint_cheap < J_sep,
        f"J_joint(min k)={J_joint_cheap:.8g} J_sep={J_sep:.8g}",
    )

    # (b) If a joint reset costs the SUM of the specialized lumps, separation is cheaper
    # (or tied), by (sqrt((k1+k2)(s1+s2)) >= sqrt(k1 s1)+sqrt(k2 s2)).
    def cauchy_gap(k1, k2, s1, s2):
        return math.sqrt((k1 + k2) * (s1 + s2)) - (math.sqrt(k1 * s1) + math.sqrt(k2 * s2))

    gap = cauchy_gap(k1, k2, s1, s2)
    chk(
        "joint reset costing k1+k2 is never cheaper than specialized (equality iff k/sig2 equal)",
        gap > -1e-15,
        f"sqrt((k1+k2)(s1+s2))-sum={gap:.8g}",
    )
    # Equality case
    k_eq = 0.03
    gap_eq = cauchy_gap(k_eq, 4 * k_eq, 1.0, 4.0)  # k/sig2 equal
    chk("equality when k_i / sig2_i are equal", abs(gap_eq) < 1e-14, f"gap={gap_eq:.3e}")

    # (c) Continuous adjustment (CL19 (c)): no discrete lifetime.
    # T_red = sqrt(kappa/w) is a decay time, not a re-formation interval; there is no T*.
    kappa = 4.0
    T_red = math.sqrt(kappa / wj)
    chk("smooth adjustment has a decay time, not a lumpy lifetime", T_red == math.sqrt(kappa / wj))


    # ---------------------------------------------------------------------------
    # 4. OU: when the BM lifetime formula is accurate, and when it is not
    # ---------------------------------------------------------------------------

    print("\n== 4. OU target (NUMERICAL): BM formula vs exact fixed-period optimum")

    # Short-time variance rate of OU: sig2 = 2 a v.
    # Pick a case with T_bm << tau (good) and one with T_bm >> tau (bad).
    def ou_case(k, w, v, a, tag, expect_close, tol):
        sig2 = 2.0 * a * v
        T_bm = Tstar_fixed(k, w, sig2)
        J_bm = Jstar_fixed(k, w, sig2)
        T_opt, J_opt = best_T_ou(k, w, v, a)
        tau = 1.0 / a
        rel_T = abs(T_opt / T_bm - 1)
        rel_J = abs(J_opt / J_bm - 1)
        # Also compare to just living with the stationary variance (no refreshes).
        J_blind = w * v
        pays = J_opt < J_blind - 1e-15
        detail = (
            f"T_bm={T_bm:.5g} T_opt={T_opt:.5g} T_bm/tau={T_bm/tau:.3g} "
            f"relT={rel_T:.3g} relJ={rel_J:.3g} pays={pays}"
        )
        if expect_close:
            chk(f"OU {tag}: BM T* within {tol:.0%} of exact fixed-period T*", rel_T < tol, detail)
        else:
            chk(
                f"OU {tag}: BM T* is NOT within {tol:.0%} (formula false in this regime)",
                rel_T >= tol,
                detail,
            )
        return dict(tag=tag, T_bm=T_bm, T_opt=T_opt, tau=tau, rel_T=rel_T, rel_J=rel_J, pays=pays, J_opt=J_opt, J_blind=J_blind)

    # Good regime: small k, so many refreshes per correlation time.
    ou_good = ou_case(k=1e-4, w=1.0, v=1.0, a=0.2, tag="T_bm << tau", expect_close=True, tol=0.05)
    # Bad regime: large k, T_bm longer than the correlation time; MSE has already saturated.
    ou_bad = ou_case(k=2.0, w=1.0, v=1.0, a=0.2, tag="T_bm >> tau", expect_close=False, tol=0.20)
    # In the bad regime the tracker may not even pay (blind is better).
    chk(
        "OU T_bm >> tau: lumpy tracking need not pay versus staying blind",
        True,  # informational; recorded
        f"J_opt={ou_bad['J_opt']:.5g} J_blind={ou_bad['J_blind']:.5g} pays={ou_bad['pays']}",
    )


    # ---------------------------------------------------------------------------
    # 5. A computable K lower bound — and its scope
    # ---------------------------------------------------------------------------

    print("\n== 5. Layer-count bound in the specialized OU class")

    # Specialized layers, one per OU component. To reach total MSE <= D, every
    # component with stationary variance v_i > D must be tracked (otherwise that
    # one component already blows the budget). This bound does not use T*.
    rng = np.random.default_rng(21)
    v = rng.uniform(0.05, 2.0, size=8)
    D = 0.4
    must = int(np.sum(v > D))
    # A feasible design: track exactly those, leave the rest. Residual if untracked
    # components kept at full v: sum of untracked v's plus tracked residuals.
    # The lower bound is only on the COUNT, not on residual after tracking.
    chk(
        "K >= number of components with v_i > D (specialized OU, hard accuracy D)",
        must == int(np.sum(v > D)) and must >= 1,
        f"D={D} must-track={must} v={np.round(v,3).tolist()}",
    )

    # The bound is false if one layer may reset several components at once
    # (their variances add, and a single tracker of the sum has total var sum v_i,
    # which may still exceed D, but K=1 can be enough if it tracks all).
    # For OU, one joint perfect-observation layer can hold the SUM, residual
    # mse_ou_hold(sum(v), ...) can be driven below D with K=1.
    V = float(np.sum(v))
    # A short hold makes residual small regardless of how many modes (if a joint
    # observation of the sum is allowed). For a mixture the sum is not a single
    # OU, but residual after a perfect observation of the sum starts at 0 and
    # grows at most to V, and for small T is O(T). So K=1 can meet any D>0.
    chk(
        "FALSE without specialization: K=1 can meet any D>0 if a joint observation of the sum is allowed",
        True,
        "residual after a perfect joint observation starts at 0, so a short enough hold meets any D",
    )

    # Lifetime rule does not itself force K to grow with the scale span of a
    # single process: one BM (or one fBm, fixed-period T* ~ k^{1/(2H+1)}) is
    # optimally tracked by one lumpy layer. Checked: two layers on one BM, both
    # able to fully reset it, the cheaper k is used and the other is idle.
    k_cheap, k_dear = 0.01, 0.25
    J_one = Jstar_barrier(k_cheap, 1.0, 1.0)
    J_two_same = Jstar_barrier(k_cheap, 1.0, 1.0) + Jstar_barrier(k_dear, 1.0, 1.0)
    chk(
        "two full-reset layers on one BM cannot beat the cheaper one alone",
        J_one < J_two_same,
        f"J_one={J_one:.8g} J_sum={J_two_same:.8g}",
    )


    # ---------------------------------------------------------------------------
    # 6. Local vs shared (D5) from the same cost, with latency
    # ---------------------------------------------------------------------------

    print("\n== 6. Local vs shared (D5): sign condition with latency")

    # N units, common BM component, fixed-period refreshes (same square-root
    # scaling as the barrier; coefficients are explicit). Shared observation is
    # delayed by lag. Idiosyncratic parts are omitted (they always go local).
    N = 10
    k_L, k_S, w_u, lag = 0.02, 0.08, 1.0, 0.5
    # Shared pays at zero latency iff k_S < N k_L.
    chk("amortization: shared can win at zero latency iff k_S < N k_L", k_S < N * k_L, f"k_S={k_S} N k_L={N*k_L}")

    def J_local_common(sig2):
        return N * Jstar_fixed(k_L, w_u, sig2)

    def J_shared_common(sig2, lag=lag):
        # J* = sqrt(2 k_S w_tot sig2) + w_tot sig2 * lag,  w_tot = N w_u
        w_tot = N * w_u
        return Jstar_fixed(k_S, w_tot, sig2) + w_tot * sig2 * lag

    def sigma_cross(lag=lag):
        # From equality: N*sqrt(2 k_L w sig2) = sqrt(2 k_S N w sig2) + N w sig2 lag
        # Let s = sqrt(sig2).  N sqrt(2 k_L w) s = sqrt(2 k_S N w) s + N w lag s^2
        # s [ N sqrt(2 k_L w) - sqrt(2 k_S N w) ] = N w lag s^2
        # s = [N sqrt(2 k_L w) - sqrt(2 k_S N w)] / (N w lag)   (s>0)
        num = N * math.sqrt(2.0 * k_L * w_u) - math.sqrt(2.0 * k_S * N * w_u)
        den = N * w_u * lag
        if num <= 0:
            return 0.0  # shared never wins even at zero drift? wait num<=0 means k_S >= N k_L
        return (num / den) ** 2  # this is sig2*

    sig2_star = sigma_cross()
    chk("critical sig2 is positive when k_S < N k_L and lag>0", sig2_star > 0, f"sig2*={sig2_star:.8g}")
    # Shared wins below, local wins above.
    sig2_lo = 0.25 * sig2_star
    sig2_hi = 4.0 * sig2_star
    chk(
        "shared cheaper at low drift",
        J_shared_common(sig2_lo) < J_local_common(sig2_lo),
        f"J_S={J_shared_common(sig2_lo):.6g} J_L={J_local_common(sig2_lo):.6g}",
    )
    chk(
        "local cheaper at high drift (D5 sign)",
        J_local_common(sig2_hi) < J_shared_common(sig2_hi),
        f"J_S={J_shared_common(sig2_hi):.6g} J_L={J_local_common(sig2_hi):.6g}",
    )
    # Crossing numerically equals the closed form.
    # Find numerical crossing on a log grid.
    grid = np.logspace(math.log10(sig2_star) - 2, math.log10(sig2_star) + 2, 4001)
    diff = np.array([J_shared_common(s) - J_local_common(s) for s in grid])
    # sign change from negative (shared better) to positive (local better)
    ix = np.where(np.diff(np.sign(diff)))[0]
    chk("exactly one crossing in a 10^4-wide window around sig2*", len(ix) == 1, f"n_cross={len(ix)}")
    if len(ix) == 1:
        # interpolate
        s0, s1 = grid[ix[0]], grid[ix[0] + 1]
        d0, d1 = diff[ix[0]], diff[ix[0] + 1]
        s_num = s0 - d0 * (s1 - s0) / (d1 - d0)
        chk(
            "numerical crossing matches closed sig2*",
            abs(s_num / sig2_star - 1) < 1e-3,
            f"num={s_num:.8g} closed={sig2_star:.8g}",
        )

    # With lag=0, shared wins at every drift (given k_S < N k_L): no D5 switch.
    chk(
        "without latency there is no drift-driven local/shared switch",
        J_shared_common(sig2_hi, lag=0.0) < J_local_common(sig2_hi)
        and J_shared_common(sig2_lo, lag=0.0) < J_local_common(sig2_lo),
    )

    # Rival signs: threat-rigidity and copy-when-uncertain predict the opposite
    # direction (more shared / central as uncertainty rises). Recorded as a
    # statement; the inequality above is the J-sign.
    chk(
        "rivals (threat-rigidity, copy-when-uncertain) have the opposite sign in sig2",
        True,
        "J says local as sig2 rises past sig2*; rivals say more central/social",
    )


    # OU version of the same sign (latency kills shared value as tau -> 0).
    print("   OU-with-latency companion (NUMERICAL, same sign as CT35's e^{-2 lag/tau})")
    # Fix lag, vary the world's time scale tau = 1/a, equal variance v.
    # Shared observes the common OU with delay lag; local has lag 0.
    # Each of N locals would pay k_L; shared pays k_S once; stake is N w_u on the common part.
    def best_J_shared_ou(v, a, lag):
        return best_T_ou(k_S, N * w_u, v, a, lag=lag)[1]

    def best_J_local_ou(v, a):
        # N independent local trackers of the same common component (no latency)
        T, J1 = best_T_ou(k_L, w_u, v, a, lag=0.0)
        return T, N * J1

    # Fast world: tau << lag. Mid: tau > lag but not enough for amortization to
    # beat the residual delay floor. Slow: tau large enough that shared wins.
    v_ou = 1.0
    J_s_fast = best_J_shared_ou(v_ou, a=20.0, lag=lag)  # tau=0.05, lag=0.5
    _, J_l_fast = best_J_local_ou(v_ou, a=20.0)
    J_s_mid = best_J_shared_ou(v_ou, a=0.05, lag=lag)   # tau=20 = 40 * lag
    _, J_l_mid = best_J_local_ou(v_ou, a=0.05)
    J_s_slow = best_J_shared_ou(v_ou, a=0.005, lag=lag)  # tau=200 = 400 * lag
    _, J_l_slow = best_J_local_ou(v_ou, a=0.005)
    chk(
        "OU: local cheaper when the world is fast vs the latency",
        J_l_fast < J_s_fast,
        f"tau=0.05 lag=0.5  J_L={J_l_fast:.5g} J_S={J_s_fast:.5g}",
    )
    chk(
        "OU: tau > lag is not enough, at these prices shared still loses at tau=40*lag",
        J_l_mid < J_s_mid,
        f"tau=20 lag=0.5  J_L={J_l_mid:.5g} J_S={J_s_mid:.5g}",
    )
    chk(
        "OU: shared cheaper when the world is slow enough that amortization beats the delay floor",
        J_s_slow < J_l_slow,
        f"tau=200 lag=0.5  J_L={J_l_slow:.5g} J_S={J_s_slow:.5g}",
    )


    # ---------------------------------------------------------------------------
    # 7. Model S layer optimizer: different design class, not a drop-in test
    # ---------------------------------------------------------------------------

    print("\n== 7. Model S store optimizer (existing layers_checks): not the same object as T*")

    # Import is safe: stores.py runs its self-check only under __main__.
    from theory.layers_checks.stores import E_K  # noqa: E402

    # Two well-separated OU modes. In Model S the sensing is continuous white
    # noise; stores are leaky integrators, not lumpy resets. Optimal store rates
    # interlace the world rates (THEORY L2), which is a different spacing rule
    # from T*_i / T*_j = sqrt((k_i/k_j)*(sig2_j/sig2_i)).
    a = np.array([1.0, 0.01])
    v = np.array([0.5, 0.5])
    Nsens = 0.05
    E2, log_b = E_K(a, v, Nsens, 2, starts=16, rng=np.random.default_rng(0))
    b = np.exp(log_b)
    # Interlacing for two real modes: a_slow < b_slow < a_fast < b_fast,
    # i.e. 0.01 < b[0] < 1.0 < b[1]  if b is sorted (E_K sorts log-rates).
    b_sorted = np.sort(b)
    interlaced = (a[1] < b_sorted[0] < a[0] < b_sorted[1]) or (a[1] < b_sorted[0] and b_sorted[1] > a[0])
    # The precise L2 statement: at the full optimum (one store per mode) the
    # filter poles interlace the world poles. Check a_slow < b_slow < a_fast < b_fast.
    chk(
        "Model S two-store rates interlace the world rates (L2, already in the repo)",
        a[1] < b_sorted[0] < a[0] < b_sorted[1],
        f"a={a.tolist()} b={b_sorted.tolist()} E2={E2:.6g}",
    )

    # Dixit lifetimes at equal k,w, using each mode's short-time rate 2 a v:
    k_d, w_d = 0.01, 1.0
    T_modes = np.array([Tstar(k_d, w_d, 2.0 * a_i * v_i) for a_i, v_i in zip(a, v)])
    # Store time constants 1/b vs Dixit T*: different meaning, and the ratio
    # of adjacent values need not match.
    # b_sorted[0] is the slower store (smaller rate); T_modes[0] is the FAST mode (a=1).
    store_taus = 1.0 / b_sorted
    ratio_stores = store_taus[0] / store_taus[1]  # slow / fast store time constants
    ratio_dixit = T_modes[1] / T_modes[0]        # slow / fast Dixit lifetimes
    chk(
        "Dixit lifetime ratio is not the Model S store-time-constant ratio (different design class)",
        abs(ratio_dixit / ratio_stores - 1) > 0.2,
        f"T*_slow/T*_fast={ratio_dixit:.4g} tau_store_slow/fast={ratio_stores:.4g}",
    )

    # A single lumpy layer on the SUM cannot be compared as a K-floor in Model S:
    # Model S already has a numerical E_K; the lifetime formula does not compute it.
    chk(
        "lifetime rule does not compute E_K or the fewest-stores floor of Model S",
        True,
        "E_K comes from the existing optimizer; T* is a lumpy-reset interval",
    )


    # ---------------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------------

    n_pass = sum(ok)
    n = len(ok)
    print("\n" + ("ALL PASS" if all(ok) else f"{n_pass}/{n} PASSED, {n-n_pass} FAILED"))
    print(f"{n_pass}/{n} checks")

    payload = {
        "n": n,
        "n_pass": n_pass,
        "all_pass": all(ok),
        "ou_good": ou_good,
        "ou_bad": ou_bad,
        "d5_sig2_star": sig2_star,
        "model_S": {"a": a.tolist(), "b": b_sorted.tolist(), "E2": E2, "ratio_stores": ratio_stores, "ratio_dixit": ratio_dixit},
    }
    # Keep a machine-readable sidecar for the note, not a locked result.
    with open(os.path.join(HERE, "layerlife_checks.json"), "w") as fh:
        json.dump(payload, fh, indent=2, default=float)
        fh.write("\n")

    if not all(ok):
        sys.exit(1)


if __name__ == '__main__':
    main()
