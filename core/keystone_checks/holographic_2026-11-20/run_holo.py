#!/usr/bin/env python3
"""T20 fair holographic / fractal test runner.

Reads locked predictions.json (and refuses to run if PREREG.md or
predictions.json hashes drift from LOCK.txt). Optimizes E_K with the
merged #116 solver and an s5_rerun.py-style multi-start. Scores strictly
against PREREG.md gates. No patching.

Run: nice -n 19 python3 -u run_holo.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize

DIR = Path(__file__).resolve().parent
REPO = DIR.parents[2]
MERGED_STORES = REPO / "theory" / "layers_checks" / "stores.py"
PRED_PATH = DIR / "predictions.json"
PREREG_PATH = DIR / "PREREG.md"
LOCK_SHA_PATH = DIR / "PREDICTIONS.sha256"
OUT_PATH = DIR / "run_holo.json"
LOG_FLUSH = True

DEADLINE_S = 3 * 60 * 60 - 10 * 60  # 2h50m, leave a little room under 3h
N_WORKERS = 4
SEP = 1.02
TOL = 1e-4
TIE = 1e-9
E_BELOW_ABS = 1e-9
E_BELOW_REL = 1e-8

# Locked hashes (also verified against PREDICTIONS.sha256 at start).
LOCKED = {
    "PREREG.md": "6eda4c82f06711fe1d5b282aa12124a1be2aa6048c4d117ece7e54dee552b1f8",
    "predictions.json": "0d877908b190cdcd287a960e87c2658c489a730d7124c964d7b45dbb106b8791",
}

spec = importlib.util.spec_from_file_location("stores_merged_t20_run", MERGED_STORES)
stores = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stores)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_locked():
    for name, expected in LOCKED.items():
        got = sha256_file(DIR / name)
        if got != expected:
            raise SystemExit(
                f"REFUSING TO RUN: {name} hash drifted.\n"
                f"  locked  {expected}\n"
                f"  current {got}\n"
                f"This would violate the prereg. Stop."
            )
    # also agree with the sidecar
    for line in LOCK_SHA_PATH.read_text().splitlines():
        h, name = line.strip().split()
        if sha256_file(DIR / name) != h:
            raise SystemExit(f"REFUSING TO RUN: {name} disagrees with PREDICTIONS.sha256")


def log(msg: str) -> None:
    print(msg, flush=True)


# ---- Family objectives ----------------------------------------------------

def kalman_P(a, v, N):
    a = float(a)
    v = float(v)
    N = float(N)
    return N * (np.sqrt(a * a + 2.0 * a * v / N) - a)


def E_inf_world(family, a, v, N):
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    if family == "M":
        return float(sum(kalman_P(ai, vi, N) for ai, vi in zip(a, v)))
    return float(stores.E_inf(a, v, N))


def mse_at(family, a, v, b, N):
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    b = np.asarray(b, float)
    if family == "M":
        tot = 0.0
        for ai, vi in zip(a, v):
            e, _g = stores.mse_given_b(np.array([ai]), np.array([vi]), b, N)
            tot += float(e)
        return float(tot)
    e, _g = stores.mse_given_b(a, v, b, N)
    return float(e)


def safe_log_rates(x, sep=SEP):
    x = np.sort(np.clip(np.asarray(x, float), -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i - 1] + np.log(sep))
    return x


def informed_inits(K, a, lo, hi, rng, n_rand=12, continuation=None):
    freqs = np.sort(np.unique(np.abs(np.asarray(a, float))))
    inits = [np.linspace(lo + 1, hi - 1, K), np.linspace(lo, hi, K)]
    # exact log-spaced grid across the world's rates (holographic start)
    inits.append(np.linspace(np.log(freqs.min()), np.log(freqs.max()), K))
    for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
        pts = [np.log(max(f * scale, 1e-18)) for f in freqs]
        if K > len(pts):
            pts = pts + [
                pts[i % len(pts)] + 0.2 * ((i // len(pts)) + 1)
                for i in range(K - len(pts))
            ]
        inits.append(np.sort(np.asarray(pts[:K], float)))
    logs = np.log(np.clip(freqs, 1e-18, None))
    if K <= len(logs):
        # evenly subsample the mode rates
        idx = np.linspace(0, len(logs) - 1, K)
        inits.append(logs[np.round(idx).astype(int)])
        if K >= 2:
            mids = 0.5 * (logs[:-1] + logs[1:])
            take = np.r_[logs, mids]
            pick = np.linspace(0, len(take) - 1, K)
            inits.append(np.sort(take[np.round(pick).astype(int)]))
    else:
        extra = np.linspace(lo, hi, K - len(logs))
        inits.append(np.sort(np.r_[logs, extra]))
    if continuation is not None:
        prev = np.sort(np.asarray(continuation, float))
        if len(prev) == K - 1 and K >= 1:
            # insert a rate in the largest log-gap, or just below/above the ends
            if len(prev) == 0:
                inits.append(np.array([(lo + hi) / 2.0]))
            else:
                anchors = np.r_[prev[0] - np.log(10), prev, prev[-1] + np.log(10)]
                gaps = np.diff(anchors)
                j = int(np.argmax(gaps))
                inserted = 0.5 * (anchors[j] + anchors[j + 1])
                inits.append(np.sort(np.r_[prev, inserted]))
                # also: prev plus a copy shifted slightly at the fast end
                inits.append(np.sort(np.r_[prev, prev[-1] + np.log(SEP) * 3]))
    for _ in range(n_rand):
        inits.append(np.sort(rng.uniform(lo, hi, K)))
    out, seen = [], set()
    for x in inits:
        x = np.asarray(x, float).reshape(-1)
        if x.size != K or not np.all(np.isfinite(x)):
            continue
        key = tuple(np.round(x, 5))
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out


def optimize_K(family, a, v, N, K, seed, continuation=None, use_de=True, de_maxiter=25, n_rand=12):
    rng = np.random.default_rng(seed)
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    la = np.log(np.abs(a))
    lo, hi = float(la.min() - 3), float(la.max() + 6)

    def obj(x):
        b = np.exp(safe_log_rates(x))
        e = mse_at(family, a, v, b, N)
        if not np.isfinite(e):
            return 1e300
        return float(e)

    inits = informed_inits(K, a, lo, hi, rng, n_rand=n_rand, continuation=continuation)
    t0 = time.time()
    ranked = []
    for x0 in inits:
        try:
            r = minimize(
                obj,
                x0,
                method="Nelder-Mead",
                options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000 * K),
            )
            ranked.append((obj(r.x), safe_log_rates(r.x), "Nelder-Mead"))
        except Exception:
            pass
    if ranked:
        ranked.sort(key=lambda t: t[0])
        polish = [t[1] for t in ranked[:4]] + list(inits[:2])
        for x0 in polish:
            try:
                r = minimize(
                    obj,
                    x0,
                    method="L-BFGS-B",
                    bounds=[(lo - 2, hi + 2)] * K,
                    options=dict(ftol=1e-14, maxiter=2000 * K),
                )
                ranked.append((obj(r.x), safe_log_rates(r.x), "L-BFGS-B"))
            except Exception:
                pass
    if use_de:
        try:
            r = differential_evolution(
                obj,
                bounds=[(lo - 2, hi + 2)] * K,
                popsize=8,
                mutation=0.5,
                recombination=0.7,
                seed=int(seed) % (2**31 - 1),
                polish=True,
                workers=1,
                atol=1e-12,
                maxiter=de_maxiter,
            )
            ranked.append((obj(r.x), safe_log_rates(r.x), "DE"))
        except Exception:
            pass
    if not ranked:
        return dict(
            E=float("inf"),
            stores=None,
            method="none",
            n_inits=len(inits),
            elapsed=time.time() - t0,
        )
    ranked.sort(key=lambda t: t[0])
    best = ranked[0]
    b = np.exp(best[1])
    E = mse_at(family, a, v, b, N)
    return dict(
        E=float(E),
        stores=b.tolist(),
        method=best[2],
        n_inits=len(inits),
        elapsed=time.time() - t0,
    )


# ---- scoring primitives (also used after the run) -------------------------

def n60_from0(eps, R):
    return int(sum(1 for k in range(1, len(eps)) if R * (eps[k - 1] - eps[k]) > 1))


def J_of(K, eps_K, R):
    return K + R * (1.0 + eps_K)


def argmin_and_ties(eps, R, k0=0):
    Js = [J_of(k0 + k, e, R) for k, e in enumerate(eps)]
    finite = [(i, jv) for i, jv in enumerate(Js) if np.isfinite(jv)]
    if not finite:
        return None, Js, []
    best = min(jv for _, jv in finite)
    scale = max(1.0, abs(best))
    winners = [k0 + i for i, jv in finite if abs(jv - best) <= TIE * scale]
    leftmost = winners[0]
    return int(leftmost), Js, [int(w) for w in winners]


def convexity_flags(eps, tol=TOL):
    if any(not np.isfinite(e) for e in eps):
        return dict(convex=False, decreasing=False, viol=[], increasing_at=[], dec=[], finite=False)
    dec = [eps[k] - eps[k + 1] for k in range(len(eps) - 1)]
    increasing_at = [k + 1 for k, d in enumerate(dec) if d < -tol]
    viol = [k for k in range(len(dec) - 1) if dec[k + 1] - dec[k] > tol]
    decreasing = len(increasing_at) == 0
    convex = decreasing and len(viol) == 0 and all(np.isfinite(dec))
    return dict(
        convex=bool(convex),
        decreasing=bool(decreasing),
        viol=viol,
        increasing_at=increasing_at,
        dec=[float(d) for d in dec],
        finite=True,
    )


def hausdorff_log10(x, y):
    x = np.log10(np.clip(np.asarray(x, float), 1e-300, None))
    y = np.log10(np.clip(np.asarray(y, float), 1e-300, None))
    if x.size == 0 or y.size == 0:
        return float("inf")

    def one_way(a, b):
        return float(max(np.min(np.abs(ai - b)) for ai in a))

    return max(one_way(x, y), one_way(y, x))


def score_A(k_i, logR):
    k = np.asarray(k_i, float)
    x = np.asarray(logR, float)
    monotone = bool(np.all(np.diff(k) >= -1e-12))
    growth = float(k[-1] - k[0])
    distinct = int(len(set(int(v) for v in k)))
    jumps = np.diff(k)
    max_jump = float(jumps.max()) if len(jumps) else 0.0
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, k, rcond=None)
    a, b = float(coef[0]), float(coef[1])
    pred = a + b * x
    mae = float(np.mean(np.abs(k - pred)))
    passed = (
        monotone
        and growth >= 3
        and distinct >= 4
        and max_jump <= 2
        and (0.25 <= b <= 2.0)
        and mae <= 1.0
    )
    return dict(
        pass_=bool(passed),
        monotone=monotone,
        growth=growth,
        distinct=distinct,
        max_jump=max_jump,
        slope=b,
        intercept=a,
        mae=mae,
        k= [int(v) for v in k],
    )


def score_B(taus, n_dec, n_bands, mid, span, tilted=False):
    taus = np.sort(np.asarray(taus, float))
    if len(taus) != n_bands or not np.all(np.isfinite(taus)) or np.any(taus <= 0):
        return dict(pass_strict=False, pass_tilted=False, error="bad_taus", taus=taus.tolist())
    delta = n_dec / (n_bands - 1) if n_bands > 1 else float("nan")
    if n_bands == 1:
        return dict(pass_strict=False, pass_tilted=False, error="n_bands=1", taus=taus.tolist())
    spacings = np.diff(np.log10(taus))
    mean_s = float(np.mean(spacings))
    std_s = float(np.std(spacings, ddof=0))
    cv = float(std_s / mean_s) if mean_s > 0 else float("inf")
    coverage = float(np.log10(taus[-1] / taus[0]))
    H_mid = hausdorff_log10(taus, mid)
    H_span = hausdorff_log10(taus, span)
    spacing_ok = (0.5 * delta <= mean_s <= 2.0 * delta)
    cov_ok = coverage >= (n_dec - 1.5)
    strict = (cv <= 0.5 and spacing_ok and cov_ok and (H_mid <= 0.75 or H_span <= 0.50))
    tilt = (cv <= 0.75 and spacing_ok and cov_ok and (H_mid <= 1.00 or H_span <= 0.75))
    return dict(
        pass_strict=bool(strict),
        pass_tilted=bool(tilt),
        cv=cv,
        mean_spacing=mean_s,
        delta=float(delta),
        coverage=coverage,
        H_mid=float(H_mid),
        H_span=float(H_span),
        taus=taus.tolist(),
    )


# ---- per-world run --------------------------------------------------------

def run_world(world, base_seed, t_start, deadline_s):
    t0 = time.time()
    wid = world["id"]
    family = world["family"]
    a = np.asarray(world["a"], float)
    v = np.asarray(world["v"], float)
    N = float(world["N"])
    J = int(world["J"])
    K_cap = int(world["K_cap"])
    idx = int(world["index"])
    E0 = float(np.sum(v))
    try:
        Einf = E_inf_world(family, a, v, N)
    except Exception as e:
        return dict(id=wid, error=f"E_inf failed: {e}", traceback=traceback.format_exc())

    fits = {0: dict(E=E0, stores=[], method="blind", n_inits=0, elapsed=0.0)}
    continuation = None
    for K in range(1, K_cap + 1):
        if time.time() - t_start > deadline_s:
            break
        seed = base_seed + 1000 * idx + 17 * K
        use_de = K <= 6
        try:
            fit = optimize_K(
                family,
                a,
                v,
                N,
                K,
                seed=seed,
                continuation=continuation,
                use_de=use_de,
                de_maxiter=25,
            )
        except Exception as e:
            fit = dict(
                E=float("inf"),
                stores=None,
                method="exception",
                n_inits=0,
                elapsed=0.0,
                error=str(e),
            )
        fits[K] = fit
        if fit.get("stores"):
            continuation = np.log(np.asarray(fit["stores"], float))
        log(
            f"    {wid} K={K}/{K_cap} E={fit['E']:.8g} method={fit['method']} "
            f"elapsed={fit['elapsed']:.1f}s"
        )

    completed_K = sorted(fits)
    if completed_K[-1] < K_cap:
        # unfinished
        pass
    E = [fits[k]["E"] if k in fits else float("nan") for k in range(0, K_cap + 1)]
    # if some K missing, trim to completed prefix
    max_done = max(k for k in fits if np.isfinite(fits[k]["E"]) or k == 0)
    # include trailing missing as nan; scoring will see unfinished if any official K missing
    unfinished = any(k not in fits or not np.isfinite(fits[k]["E"]) for k in range(0, K_cap + 1))

    below = []
    for k, e in enumerate(E):
        if k >= 1 and np.isfinite(e) and np.isfinite(Einf):
            if e < Einf - E_BELOW_ABS and (Einf - e) / max(Einf, 1e-18) > E_BELOW_REL:
                below.append(k)

    eps = [
        float(e / Einf - 1.0) if (Einf > 0 and np.isfinite(e) and np.isfinite(Einf)) else float("nan")
        for e in E
    ]
    flags = convexity_flags(eps, TOL)

    # official R grid from the locked predictions (passed in)
    R_grid = world.get("_R_grid")
    per_R = []
    last_pays_at_top = False
    for R in R_grid:
        ks, Js, winners = argmin_and_ties(eps, float(R), k0=0)
        n60 = n60_from0(eps, float(R)) if all(np.isfinite(eps)) else None
        match = None
        if ks is not None and n60 is not None:
            match = (n60 == ks) or (n60 in winners)
        rec = dict(
            R=float(R),
            argmin=ks,
            winners=winners,
            n60_from0=n60,
            match_n60=match,
            J= [float(j) for j in Js] if Js is not None else None,
        )
        per_R.append(rec)
    if (
        all(np.isfinite(eps))
        and len(eps) >= 2
        and R_grid
        and (R_grid[-1] * (eps[-2] - eps[-1]) > 1)
        and np.isfinite(Einf)
        and E[K_cap] > Einf + 1e-8
    ):
        last_pays_at_top = True

    stores_k = {str(k): fits[k].get("stores") for k in fits}
    methods = {str(k): fits[k].get("method") for k in fits}
    elapsed_k = {str(k): fits[k].get("elapsed") for k in fits}

    # first-store value share (diagnosis, not a gate)
    frac_first = None
    if np.isfinite(E0) and np.isfinite(Einf) and np.isfinite(E[1] if len(E) > 1 else np.nan):
        denom = E0 - Einf
        if denom > 0:
            frac_first = float((E0 - E[1]) / denom)

    R_need = []
    if all(np.isfinite(eps)):
        for k in range(1, len(eps)):
            dec = eps[k - 1] - eps[k]
            R_need.append(None if dec <= 0 else float(1.0 / dec))

    return dict(
        id=wid,
        index=idx,
        family=family,
        role=world["role"],
        alpha=world.get("alpha"),
        N=N,
        Gamma=world.get("Gamma"),
        J=J,
        n_dec=world.get("n_dec"),
        n_bands=world.get("n_bands"),
        K_cap=K_cap,
        B_strict_world=world.get("B_strict"),
        A_must_not_pass=world.get("A_must_not_pass"),
        B_is_not_a_test=world.get("B_is_not_a_test"),
        predicted_K_set=world.get("predicted_K_set"),
        band_centres_mid=world.get("band_centres_mid"),
        band_centres_span=world.get("band_centres_span"),
        E0=E0,
        E_inf=float(Einf),
        E=E,
        eps=eps,
        stores=stores_k,
        methods=methods,
        elapsed_k=elapsed_k,
        unfinished=bool(unfinished),
        below_causal=below,
        convex_0K=flags,
        per_R=per_R,
        censored=bool(last_pays_at_top),
        frac_first=frac_first,
        R_need=R_need,
        elapsed=time.time() - t0,
        error=None,
    )


def apply_gates(row, R_grid):
    """Score one world against locked gates. Pure function of the row + R grid."""
    out = dict(A=None, B=None, C=None, NC_K_ok=None, sanity_bits={})
    if row.get("error") or row.get("unfinished"):
        out["unscored"] = True
        out["reason"] = "error" if row.get("error") else "unfinished"
        return out

    logR = [float(np.log10(R)) for R in R_grid]
    k_i = [p["argmin"] for p in row["per_R"]]
    if any(k is None for k in k_i):
        out["unscored"] = True
        out["reason"] = "missing argmin"
        return out

    A = score_A(k_i, logR)
    out["A"] = A

    B = None
    if row.get("B_is_not_a_test"):
        out["B"] = dict(not_a_test=True)
    else:
        n_bands = int(row["n_bands"])
        key = str(n_bands)
        st = row.get("stores", {}).get(key)
        if not st:
            out["B"] = dict(pass_strict=False, pass_tilted=False, error="no stores at K=n_bands")
        else:
            taus = [1.0 / b for b in st]
            B = score_B(
                taus,
                float(row["n_dec"]),
                n_bands,
                row["band_centres_mid"],
                row["band_centres_span"],
            )
            out["B"] = B

    # C
    conv = row["convex_0K"]["convex"]
    if not conv:
        out["C"] = dict(pass_=None, not_a_test=True, reason="not convex", n_cells=0, n_match=0)
    else:
        cells = row["per_R"]
        n = len(cells)
        n_match = sum(1 for p in cells if p["match_n60"])
        out["C"] = dict(pass_=n_match == n, not_a_test=False, n_cells=n, n_match=n_match)

    # NC set
    if row.get("predicted_K_set") is not None:
        allowed = set(row["predicted_K_set"])
        ks = [p["argmin"] for p in row["per_R"]]
        out["NC_K_ok"] = all(k in allowed for k in ks)
        out["NC_K_values"] = sorted(set(ks))

    out["unscored"] = False
    return out


def family_verdicts(rows, R_grid):
    """Apply family-level and VALIDITY / overall gates."""
    scored = {}
    for r in rows:
        scored[r["id"]] = dict(row=r, gates=apply_gates(r, R_grid))

    def primary(fam):
        return [
            scored[r["id"]]
            for r in rows
            if r.get("family") == fam and r.get("role") == "primary"
        ]

    def family_AB_C(fam):
        items = primary(fam)
        n = len(items)
        A_pass = [it for it in items if it["gates"].get("A") and it["gates"]["A"].get("pass_")]
        B_strict_pass = [
            it
            for it in items
            if it["gates"].get("B") and it["gates"]["B"].get("pass_strict")
        ]
        alpha1 = [
            it
            for it in items
            if it["row"].get("B_strict_world") or (
                it["row"].get("alpha") is not None and abs(it["row"]["alpha"] - 1.0) < 1e-12
            )
        ]
        alpha1_B = [
            it
            for it in alpha1
            if it["gates"].get("B") and it["gates"]["B"].get("pass_strict")
        ]
        convex = [
            it
            for it in items
            if it["row"].get("convex_0K") and it["row"]["convex_0K"].get("convex")
        ]
        C_fail = [
            it
            for it in convex
            if it["gates"].get("C") and it["gates"]["C"].get("pass_") is False
        ]
        unfinished = [it for it in items if it["gates"].get("unscored")]
        fam_A = (len(A_pass) >= 5 and n == 6 and not unfinished)
        # if some unfinished, family A is not a pass
        if unfinished:
            fam_A = False
            fam_B = False
        else:
            fam_B = (len(alpha1) == len(alpha1_B) and len(alpha1) == 2 and len(B_strict_pass) >= 4)
        fam_C = (len(convex) >= 5 and len(C_fail) == 0 and n == 6 and not unfinished)
        return dict(
            n=n,
            unfinished=[it["row"]["id"] for it in unfinished],
            A_pass_ids=[it["row"]["id"] for it in A_pass],
            A_n=len(A_pass),
            A=fam_A,
            B_strict_pass_ids=[it["row"]["id"] for it in B_strict_pass],
            B_n=len(B_strict_pass),
            alpha1_ids=[it["row"]["id"] for it in alpha1],
            alpha1_B_n=len(alpha1_B),
            B=fam_B,
            convex_n=len(convex),
            C_fail_ids=[it["row"]["id"] for it in C_fail],
            C=fam_C,
        )

    S = family_AB_C("S")
    M = family_AB_C("M")

    # VALIDITY
    nc_ids = ["NC_single_N1e-4", "NC_single_N1e-6", "NC_narrow_N1e-4"]
    nc = [scored[i] for i in nc_ids if i in scored]
    sanity_fail = []
    validity_notes = []
    validity = True
    if len(nc) != 3 or any(it["gates"].get("unscored") for it in nc):
        validity = False
        validity_notes.append("NC unfinished or missing")
    else:
        for it in nc:
            r, g = it["row"], it["gates"]
            if g.get("A") and g["A"].get("pass_"):
                validity = False
                validity_notes.append(f"{r['id']} passed (A) (must not)")
            if not g.get("NC_K_ok"):
                validity = False
                validity_notes.append(
                    f"{r['id']} K*={g.get('NC_K_values')} not in {r.get('predicted_K_set')}"
                )
            c = g.get("C") or {}
            if c.get("pass_") is False and not c.get("not_a_test"):
                validity = False
                validity_notes.append(f"{r['id']} C failed")

    # SANITY from NC_single Kalman and below-causal flags, E0
    sanity = dict(pass_=True, bits=[])
    for r in rows:
        bits = {}
        if abs(r.get("E0", 0.0) - 1.0) > 1e-12 and r["id"].startswith("NC_single"):
            # E0 should be 1 on every variance-normalized world; NC_single is v=1
            pass
        if r.get("E0") is not None and abs(r["E0"] - 1.0) > 1e-12:
            # all official worlds have total variance 1
            sanity["pass_"] = False
            sanity["bits"].append(f"{r['id']} E0={r['E0']} != 1")
        if r.get("below_causal"):
            sanity["pass_"] = False
            sanity["bits"].append(f"{r['id']} E below causal at K={r['below_causal']}")
        if r["id"].startswith("NC_single") and not r.get("unfinished") and not r.get("error"):
            a = 1.0
            v = 1.0
            N = r["N"]
            P = float(kalman_P(a, v, N))
            E1 = r["E"][1] if len(r["E"]) > 1 else float("nan")
            Einf = r["E_inf"]
            def close(x, y):
                return abs(x - y) <= max(1e-8, 1e-8 * max(abs(y), 1e-18))
            ok1 = close(E1, P)
            okinf = close(Einf, P)
            bits["kalman_P"] = P
            bits["E1"] = E1
            bits["E_inf"] = Einf
            bits["E1_ok"] = bool(ok1)
            bits["Einf_ok"] = bool(okinf)
            if not (ok1 and okinf):
                sanity["pass_"] = False
                sanity["bits"].append(
                    f"{r['id']} Kalman identity fail P={P} E1={E1} Einf={Einf}"
                )
        r.setdefault("sanity_world", bits)

    if not sanity["pass_"]:
        validity = False
        validity_notes.append("SANITY failed")

    overall = "INVALID"
    if not validity:
        overall = "INVALID"
    elif S["A"] and S["B"] and M["A"] and M["B"]:
        overall = "SUPPORTED (in-model, numerical)"
    else:
        overall = "NOT SUPPORTED"

    return dict(
        Family_S=S,
        Family_M=M,
        SANITY=sanity,
        VALIDITY=dict(pass_=bool(validity and sanity["pass_"]), notes=validity_notes),
        overall=overall,
        per_world={wid: scored[wid]["gates"] for wid in scored},
    )


def load_predictions():
    assert_locked()
    pred = json.loads(PRED_PATH.read_text())
    return pred


def save_run(run):
    tmp = OUT_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(run, f, indent=1)
        f.write("\n")
    tmp.replace(OUT_PATH)


def world_order(pred):
    """PREREG compute order: SANITY / NC, Family S primary, Family M primary, secondary."""
    worlds = pred["worlds"]
    def key(w):
        if w["family"] == "NC":
            return (0, w["index"])
        if w["family"] == "S" and w["role"] == "primary":
            return (1, w["index"])
        if w["family"] == "M" and w["role"] == "primary":
            return (2, w["index"])
        return (3, w["index"])
    return sorted(worlds, key=key)


def main():
    t_start = time.time()
    pred = load_predictions()
    R_grid = pred["R_grid"]
    base_seed = pred["BASE_SEED"]
    log(
        f"T20 run start. prereg={LOCKED['PREREG.md'][:16]}… "
        f"pred={LOCKED['predictions.json'][:16]}… "
        f"n_worlds={len(pred['worlds'])} workers={N_WORKERS} deadline={DEADLINE_S}s"
    )
    planned = world_order(pred)
    # attach R grid so workers have it
    for w in planned:
        w["_R_grid"] = R_grid

    run = dict(
        started_s=t_start,
        prereg_sha256=LOCKED["PREREG.md"],
        predictions_sha256=LOCKED["predictions.json"],
        BASE_SEED=base_seed,
        R_grid=R_grid,
        solver=str(MERGED_STORES),
        n_workers=N_WORKERS,
        deadline_s=DEADLINE_S,
        worlds=[],
        verdict=None,
        done=False,
    )
    # resume if a partial file exists
    done_ids = set()
    if OUT_PATH.exists():
        try:
            old = json.loads(OUT_PATH.read_text())
            if (
                old.get("prereg_sha256") == LOCKED["PREREG.md"]
                and old.get("predictions_sha256") == LOCKED["predictions.json"]
            ):
                for row in old.get("worlds", []):
                    if row.get("id") and not row.get("error"):
                        run["worlds"].append(row)
                        done_ids.add(row["id"])
                log(f"resuming; already have {len(done_ids)} worlds: {sorted(done_ids)}")
        except Exception as e:
            log(f"could not resume ({e}); starting fresh")
            run["worlds"] = []
            done_ids = set()

    remaining = [w for w in planned if w["id"] not in done_ids]
    # Process in waves so we can flush after each world and honour the order
    # (NC first). Within a wave of the same priority, use the pool.
    from collections import defaultdict

    waves = defaultdict(list)
    order_keys = []
    for w in remaining:
        if w["family"] == "NC":
            k = 0
        elif w["family"] == "S" and w["role"] == "primary":
            k = 1
        elif w["family"] == "M" and w["role"] == "primary":
            k = 2
        else:
            k = 3
        if k not in order_keys:
            order_keys.append(k)
        waves[k].append(w)

    for k in order_keys:
        wave = waves[k]
        if time.time() - t_start > DEADLINE_S:
            log(f"deadline before wave {k}; leaving {len(wave)} worlds unfinished")
            break
        log(f"wave {k}: {len(wave)} worlds, {N_WORKERS} workers")
        # For wave 0 (NC, tiny) just run inline to get SANITY fast.
        if k == 0 or len(wave) == 1:
            for w in wave:
                if time.time() - t_start > DEADLINE_S:
                    break
                log(f"  start {w['id']}")
                row = run_world(w, base_seed, t_start, DEADLINE_S)
                run["worlds"].append(row)
                save_run(run)
                log(f"  wrote {w['id']} unfinished={row.get('unfinished')} err={row.get('error')}")
            continue
        # parallel for S, M, secondary — but cap workers so we don't oversubscribe
        with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
            futs = {
                ex.submit(run_world, w, base_seed, t_start, DEADLINE_S): w["id"]
                for w in wave
            }
            for fut in as_completed(futs):
                wid = futs[fut]
                try:
                    row = fut.result()
                except Exception as e:
                    row = dict(id=wid, error=str(e), traceback=traceback.format_exc())
                run["worlds"].append(row)
                save_run(run)
                log(
                    f"  wrote {wid} unfinished={row.get('unfinished')} "
                    f"err={row.get('error')} elapsed={row.get('elapsed')}"
                )

    # score whatever we have
    run["verdict"] = family_verdicts(run["worlds"], R_grid)
    run["wall_s"] = time.time() - t_start
    planned_ids = [w["id"] for w in planned]
    have = {r["id"] for r in run["worlds"] if not r.get("error") and not r.get("unfinished")}
    run["done"] = all(i in have for i in planned_ids)
    run["completed_ids"] = sorted(have)
    run["missing_ids"] = [i for i in planned_ids if i not in have]
    save_run(run)
    log(json.dumps({
        "done": run["done"],
        "wall_s": run["wall_s"],
        "overall": run["verdict"]["overall"],
        "VALIDITY": run["verdict"]["VALIDITY"],
        "Family_S": {k: run["verdict"]["Family_S"][k] for k in ("A", "B", "C", "A_n", "B_n")},
        "Family_M": {k: run["verdict"]["Family_M"][k] for k in ("A", "B", "C", "A_n", "B_n")},
        "SANITY": run["verdict"]["SANITY"],
        "missing": run["missing_ids"],
    }, indent=2))
    log(f"wrote {OUT_PATH} wall={run['wall_s']:.1f}s done={run['done']}")


if __name__ == "__main__":
    main()
