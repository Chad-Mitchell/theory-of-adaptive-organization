#!/usr/bin/env python3
"""Confirmation run for WF-HSV: reduced-order argmin on fresh worlds.

Official start is after wf_predictions.json is written and hashed.
Resume-safe. nice 19. Writes waterfill/wf_run.json incrementally and
RESULTS.md when complete.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
MERGED_STORES = REPO / "theory" / "layers_checks" / "stores.py"
RL_PATH = REPO / "core" / "keystone_checks" / "resonant_layers.py"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RL_PATH.parent))

from worlds import R_GRID_S, R_GRID_R, restore_av  # noqa: E402
from wf_rule import predict  # noqa: E402

N_WORKERS = 4
TIE_J = 1e-8
PRED = HERE / "wf_predictions.json"
RUN = HERE / "wf_run.json"
LOG = HERE / "run_wf.log"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_stores():
    spec = importlib.util.spec_from_file_location("stores_merged_wf", MERGED_STORES)
    stores = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stores)
    return stores


def load_rl():
    import resonant_layers as rl
    return rl


def safe_log_rates(x, sep=1.02):
    x = np.sort(np.clip(np.asarray(x, float), -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i - 1] + np.log(sep))
    return x


def informed_inits(K, a, lo, hi, rng, n_rand=12):
    freqs = np.sort(np.unique(np.abs(np.asarray(a, float))))
    inits = [np.linspace(lo + 1, hi - 1, K), np.linspace(lo, hi, K)]
    for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
        pts = [np.log(max(f * scale, 1e-18)) for f in freqs]
        if K > len(pts):
            pts = pts + [
                pts[i % len(pts)] + 0.2 * ((i // len(pts)) + 1)
                for i in range(K - len(pts))
            ]
        inits.append(np.asarray(pts[:K], float))
    for _ in range(n_rand):
        inits.append(np.sort(rng.uniform(lo, hi, K)))
    out, seen = [], set()
    for x in inits:
        key = tuple(np.round(np.asarray(x, float), 5))
        if key not in seen and len(x) == K:
            seen.add(key)
            out.append(np.asarray(x, float))
    return out


def optimize_K_model_s(a, v, N, K, seed=0, n_rand=12, use_de=True, de_maxiter=25):
    stores = load_stores()
    rng = np.random.default_rng(seed)
    la = np.log(np.abs(np.asarray(a, float)))
    lo, hi = float(la.min() - 3), float(la.max() + 6)

    def obj(x):
        e, _g = stores.mse_given_b(a, v, np.exp(safe_log_rates(x)), N)
        return float(e)

    inits = informed_inits(K, a, lo, hi, rng, n_rand=n_rand)
    t0 = time.time()
    ranked = []
    for x0 in inits:
        try:
            r = minimize(obj, x0, method="Nelder-Mead",
                         options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000 * K))
            ranked.append((obj(r.x), safe_log_rates(r.x), "Nelder-Mead"))
        except Exception:
            pass
    if ranked:
        ranked.sort(key=lambda t: t[0])
        polish = [t[1] for t in ranked[:4]] + list(inits[:2])
        for x0 in polish:
            try:
                r = minimize(obj, x0, method="L-BFGS-B",
                             bounds=[(lo - 2, hi + 2)] * K,
                             options=dict(ftol=1e-14, maxiter=2000 * K))
                ranked.append((obj(r.x), safe_log_rates(r.x), "L-BFGS-B"))
            except Exception:
                pass
    if use_de and K <= 4:
        try:
            r = differential_evolution(
                obj, bounds=[(lo - 2, hi + 2)] * K,
                popsize=8, mutation=0.5, recombination=0.7,
                seed=int(seed) % (2**31 - 1), polish=True, workers=1,
                atol=1e-12, maxiter=de_maxiter,
            )
            ranked.append((obj(r.x), safe_log_rates(r.x), "DE"))
        except Exception:
            pass
    if not ranked:
        return dict(E=float("inf"), stores=None, method="none",
                    n_inits=len(inits), elapsed=time.time() - t0)
    ranked.sort(key=lambda t: t[0])
    best = ranked[0]
    b = np.exp(best[1])
    E, _g = stores.mse_given_b(a, v, b, N)
    return dict(E=float(E), stores=[float(x) for x in b], method=best[2],
                n_inits=len(inits), elapsed=time.time() - t0)


def compositions(n):
    """Prereg §7. n = world degree."""
    comps = [(0, 0)]
    for k in range(1, n + 1):
        comps.append((0, k))  # (n_res, n_first)
    import math
    for r in range(1, int(math.ceil(n / 2)) + 2):
        if 2 * r <= n + 2:
            comps.append((r, 0))
    comps.extend([(1, 1), (1, 2)])
    if n >= 4:
        comps.append((2, 1))
    if n >= 6:
        comps.extend([(2, 2), (3, 1)])
    out, seen = [], set()
    for nr, nf in comps:
        C = nf + 2 * nr
        if C > n + 2:
            continue
        key = (nr, nf)
        if key not in seen:
            seen.add(key)
            out.append(key)
    return out


def run_model_s_world(item):
    w, seed_i = item
    stores = load_stores()
    a = np.asarray(w["a"], float)
    v = np.asarray(w["v"], float)
    N = float(w["N"])
    J = int(w["J"])
    t0 = time.time()
    E0 = float(np.sum(v))
    Einf = float(stores.E_inf(a, v, N))
    designs = {0: dict(E=E0, stores=[], method="closed", C=0)}
    flags = []
    for K in range(1, J + 1):
        seed = 50_000 + 17 * seed_i + K
        rec = optimize_K_model_s(a, v, N, K, seed=seed, n_rand=12, use_de=True, de_maxiter=25)
        rec["C"] = K
        designs[K] = rec
        if np.isfinite(rec["E"]) and rec["E"] < Einf - 1e-9:
            flags.append(f"E_{K}<E_inf")
    Es = {int(k): float(d["E"]) for k, d in designs.items()}
    floor = Einf
    floor_flag = False
    finite = [e for e in Es.values() if np.isfinite(e)]
    if finite and min(finite) < Einf - 1e-12:
        floor = min(Einf, min(finite))
        floor_flag = True
        flags.append("E_inf_floor_min")
    return dict(
        id=w["id"], cls="model_s", J=J, N=N, a=a.tolist(), v=v.tolist(),
        E_inf_YJ=Einf, E_inf_used=float(floor), floor_flag=floor_flag,
        E0=E0, designs={str(k): d for k, d in designs.items()},
        flags=flags, elapsed=time.time() - t0,
    )


def run_extended_world(item):
    w, world_index, base_extra = item
    import resonant_layers as rl
    a, v, N = restore_av(w)
    # restore_av expects pair encoding; our pred file has that for rh/mx
    n = int(w["degree"])
    t0 = time.time()
    E0 = float(np.real(np.sum(v)))
    Einf = float(rl.E_inf_YJ(a, v, N))
    comps = compositions(n)
    designs = {}
    flags = []
    for n_res, n_first in comps:
        C = n_first + 2 * n_res
        seed = 20261120 + 1000 * world_index + 17 * (n_res * 100 + n_first) + base_extra
        if n_res == 0 and n_first == 0:
            rec = dict(E=E0, first=[], resonants=[], method="closed", C=0,
                       n_first=0, n_res=0, elapsed=0.0)
        else:
            rec = rl.optimize_design(a, v, N, n_first, n_res, seed=seed,
                                    n_rand=16, use_de=True)
            rec["C"] = int(rec.get("C", C))
        key = f"r{n_res}_f{n_first}"
        designs[key] = rec
        if not np.isfinite(rec.get("E", np.inf)):
            flags.append(f"discard_{key}")
    finite_E = [d["E"] for d in designs.values() if np.isfinite(d.get("E", np.nan))]
    floor = Einf
    floor_flag = False
    if finite_E and min(finite_E) < Einf - 1e-12:
        floor = min(Einf, min(finite_E))
        floor_flag = True
        flags.append("E_inf_floor_min")
    # best E at each cost
    best_by_C = {}
    for d in designs.values():
        e, C = d.get("E", np.inf), int(d.get("C", -1))
        if not np.isfinite(e):
            continue
        if C not in best_by_C or e < best_by_C[C]["E"]:
            best_by_C[C] = dict(E=float(e), key=None, n_first=d.get("n_first"),
                                n_res=d.get("n_res"), first=d.get("first"),
                                resonants=d.get("resonants"), method=d.get("method"))
    # fill keys
    for key, d in designs.items():
        C = int(d.get("C", -1))
        if C in best_by_C and np.isfinite(d.get("E", np.nan)) and d["E"] == best_by_C[C]["E"]:
            best_by_C[C]["key"] = key
    return dict(
        id=w["id"], cls=w["cls"], degree=n, N=N,
        a=w["a"], v=w["v"],
        n_osc=w.get("n_osc"), n_ou=w.get("n_ou"),
        E_inf_YJ=Einf, E_inf_used=float(floor), floor_flag=floor_flag,
        E0=E0, compositions=[list(c) for c in comps],
        designs=designs, best_by_C={str(k): v for k, v in best_by_C.items()},
        flags=flags, elapsed=time.time() - t0, world_index=world_index,
    )


def argmin_from_E(E_by_C, E_inf, R, tie=TIE_J):
    """E_by_C: dict int->E including 0. Returns list of minimizing C (ties)."""
    Js = {}
    for C, E in E_by_C.items():
        if not np.isfinite(E) or not (E_inf > 0):
            continue
        Js[int(C)] = int(C) + float(R) * (float(E) / float(E_inf))
    if not Js:
        return dict(C_star=None, J=None, ties=[], Js=Js)
    m = min(Js.values())
    ties = sorted(C for C, J in Js.items() if abs(J - m) <= tie)
    return dict(C_star=int(ties[0]) if ties else None, J=float(m), ties=ties, Js=Js)


def n60_from0(E_by_C, E_inf, R):
    Cs = sorted(int(c) for c in E_by_C if np.isfinite(E_by_C[c]))
    if 0 not in Cs:
        return None
    eps = {C: E_by_C[C] / E_inf - 1.0 for C in Cs}
    # walk adjacent present costs? For Model S, C=0..J contiguous.
    # For extended library, costs may skip (e.g. only even if only resonators).
    # N60-from-0 as used in Model S is on K=0,1,...,J. For identity diagnostic
    # we only apply it on Model S where C is contiguous.
    if Cs != list(range(min(Cs), max(Cs) + 1)):
        # still define increments along the sorted present costs
        pass
    kstar = 0
    for i in range(1, len(Cs)):
        dec = eps[Cs[i - 1]] - eps[Cs[i]]
        # only count a unit step? For contiguous integer C, add (Cs[i]-Cs[i-1])
        # if the increment *per state* ... Official N60 is per integer K.
        if Cs[i] == Cs[i - 1] + 1 and R * dec > 1:
            kstar = Cs[i]
        elif Cs[i] == Cs[i - 1] + 1 and R * dec <= 1:
            break
        elif Cs[i] > Cs[i - 1] + 1:
            # gap: stop if we cannot walk unit steps (Model S identity uses unit K)
            break
    # If first increment 0->1 does not pay, kstar stays 0. If later ones pay
    # after a fail, convexity would have stopped. This is N60-from-0 on the
    # unit-step prefix.
    return int(kstar)


def load_run():
    if RUN.is_file():
        return json.loads(RUN.read_text())
    return dict(worlds={}, started=None, finished=None)


def save_run(data):
    tmp = RUN.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=1, default=str))
    tmp.replace(RUN)


def score_all(pred, run):
    # re-apply predict for tautology
    taut_ok = True
    taut_mism = []
    results = dict(model_s=[], rhythm=[], mixed=[])

    def E_map_ms(row):
        em = {0: row["E0"]}
        for k, d in row["designs"].items():
            em[int(k)] = d["E"]
        return em

    def E_map_ext(row):
        em = {}
        for C, d in row["best_by_C"].items():
            em[int(C)] = d["E"]
        if 0 not in em:
            em[0] = row["E0"]
        return em

    for group, key, grid, is_ms in (
        ("model_s", "model_s", pred["R_GRID_S"], True),
        ("rhythm", "rhythm", pred["R_GRID_R"], False),
        ("mixed", "mixed", pred["R_GRID_R"], False),
    ):
        for pw in pred[key]:
            wid = pw["id"]
            if wid not in run["worlds"]:
                continue
            row = run["worlds"][wid]
            # re-apply
            if is_ms:
                a, v, N = np.asarray(pw["a"], float), np.asarray(pw["v"], float), float(pw["N"])
            else:
                a, v, N = restore_av(pw)
            for pr in pw["per_R"]:
                rec = predict(a, v, N, pr["R"])
                if rec["status"] != pr["status"] or rec.get("K_star") != pr.get("K_star"):
                    taut_ok = False
                    taut_mism.append((wid, pr["R"], pr, rec.get("status"), rec.get("K_star")))
            E_inf = row["E_inf_used"]
            em = E_map_ms(row) if is_ms else E_map_ext(row)
            cells = []
            for pr in pw["per_R"]:
                R = float(pr["R"])
                am = argmin_from_E(em, E_inf, R)
                pred_k = pr["K_star"]
                status = pr["status"]
                match = (status == "OK" and pred_k in am["ties"]) if am["ties"] else False
                n60 = n60_from0(em, E_inf, R) if is_ms else None
                cells.append(dict(
                    R=R, predicted=pred_k, pred_status=status,
                    argmin=am["C_star"], ties=am["ties"], match=match,
                    n60_from0=n60, J_min=am["J"],
                ))
            # decrements for identity diagnostic
            Cs = sorted(em)
            eps = [em[C] / E_inf - 1.0 for C in Cs] if E_inf > 0 else []
            dec = [eps[i] - eps[i + 1] for i in range(len(eps) - 1)] if eps else []
            results[group].append(dict(
                id=wid, floor_flag=row.get("floor_flag"), flags=row.get("flags"),
                E_inf_YJ=row.get("E_inf_YJ"), E_inf_used=E_inf,
                costs=Cs, E=[em[C] for C in Cs], eps=eps, decrements=dec,
                predicted_delta=pw.get("delta"),
                cells=cells,
                n_match=sum(1 for c in cells if c["match"]),
                n_det=sum(1 for c in cells if c["pred_status"] == "OK"),
                n_cells=len(cells),
                elapsed=row.get("elapsed"),
            ))
    return results, taut_ok, taut_mism


def write_results(pred, run, results, taut_ok, taut_mism, start_ts, pred_sha):
    def gate_stats(rows):
        n_match = n_det = n_cells = n_indet = 0
        hole_true = hole_hit = 0
        for r in rows:
            for c in r["cells"]:
                n_cells += 1
                if c["pred_status"] != "OK":
                    n_indet += 1
                    continue
                n_det += 1
                if c["match"]:
                    n_match += 1
                if c["argmin"] == 0:
                    hole_true += 1
                    if c["predicted"] == 0:
                        hole_hit += 1
        rate = (n_match / n_det) if n_det else None
        hole_rate = (hole_hit / hole_true) if hole_true else None
        return dict(n_match=n_match, n_det=n_det, n_cells=n_cells, n_indet=n_indet,
                    rate=rate, hole_true=hole_true, hole_hit=hole_hit, hole_rate=hole_rate)

    g_ms = gate_stats(results["model_s"])
    g_rm = gate_stats(results["rhythm"] + results["mixed"])
    g_all_r = gate_stats(results["rhythm"])
    g_all_m = gate_stats(results["mixed"])

    # identity diagnostic on Model S J>=3 (all of them)
    tautology_identity = False
    n_ms_all_count_match = 0
    n_ms = 0
    dec_equal_worlds = 0
    dec_notes = []
    for r in results["model_s"]:
        n_ms += 1
        # count match all R?
        all_count = all(
            (c["pred_status"] == "OK" and c["predicted"] == c["n60_from0"])
            for c in r["cells"]
        )
        if all_count:
            n_ms_all_count_match += 1
        delta = np.asarray(r["predicted_delta"] or [], float)
        dec = np.asarray(r["decrements"] or [], float)
        # pad
        L = max(len(delta), len(dec))
        d1 = np.zeros(L); d2 = np.zeros(L)
        d1[:len(delta)] = np.sort(delta)[::-1] if len(delta) else d1
        d2[:len(dec)] = dec  # already in K=0->1, 1->2, ... order, not necessarily sorted
        # prereg: sorted decreasing delta vs joint decrements entrywise 1e-8 relative
        rel = np.abs(np.sort(delta)[::-1][:len(dec)] - dec) / np.maximum(np.abs(dec), 1e-18) if len(dec) and len(delta) else np.array([np.inf])
        close = bool(len(delta) == len(dec) and np.all(rel <= 1e-8))
        if close:
            dec_equal_worlds += 1
        dec_notes.append(dict(id=r["id"], all_count_match=all_count, decrements_equal=close,
                              n_delta=len(delta), n_dec=len(dec),
                              max_rel=float(np.max(rel)) if rel.size else None))
    if n_ms > 0 and n_ms_all_count_match == n_ms and dec_equal_worlds == n_ms:
        tautology_identity = True

    # SANITY from predictions file
    sanity_pass = True
    sanity_rows = []
    for s in pred["sanity"]:
        P = s["P"]
        v = s["v"][0]
        for pr in s["per_R"]:
            # closed form already in file via K_star vs R(v-P)/P
            closed = 1 if pr["R"] * (v - P) / P > 1 else 0
            ok = s["status"] == "OK" and pr["K_star"] == closed
            sanity_rows.append(dict(id=s["id"], R=pr["R"], closed=closed, pred=pr["K_star"], ok=ok))
            if not ok:
                sanity_pass = False
    ks_seen = set(x["pred"] for x in sanity_rows)
    if not (0 in ks_seen and 1 in ks_seen):
        sanity_pass = False

    ms_pass = (g_ms["rate"] is not None and g_ms["rate"] >= 0.95)
    rm_pass = (g_rm["rate"] is not None and g_rm["rate"] >= 0.90)
    hole_pass = (g_ms["hole_rate"] is None) or (g_ms["hole_rate"] >= 0.95)

    not_a_test = tautology_identity
    taut_test_ok = taut_ok and (not tautology_identity)

    def pct(x):
        return "n/a" if x is None else f"{100*x:.2f}%"

    lines = []
    lines.append("# WF-HSV results")
    lines.append("")
    lines.append(f"**Scored:** {time.strftime('%A %d %B %Y, %I:%M %p %Z')} (America/New_York), strictly against `PREREG.md` locked 20 November 2026, 9:54:48 PM ET.")
    lines.append(f"**Integrity:** prereg SHA-256 `9592042bc2932acec025315c5f34d401ad896a76f16940ee12c43d4be5a7bb05`. Predictions SHA-256 `{pred_sha}`, written before official start {start_ts}. Official start recorded in `waterfill/START.txt`. Deviation D1 (exclusion parser, before start) in `waterfill/DEVIATIONS_2026-11-20.md`. No push.")
    lines.append("**Rule:** \(K^*_{\\mathrm{WF}}=\\#\{i:R\\delta_i>1\}\), \(\\delta_i\) the \(H_2\) split of the unique Kalman–Bucy estimate (innovations form). Count only; not a process-band placement prediction.")
    lines.append("All findings below are **in-model, numerical**. Nothing here is **PROVED**.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Headline verdict (prereg gates)")
    lines.append("")
    lines.append("| Gate | Criterion | Result | Verdict |")
    lines.append("|---|---|---|---|")
    taut_verdict = "NOT A TEST (identity diagnostic triggered)" if tautology_identity else ("PASS" if taut_ok else "FAIL / test invalid")
    lines.append(f"| TAUTOLOGY (test validity) | §3 items 1–4; item 5 not triggered | re-apply {'OK' if taut_ok else 'FAIL'} ({len(taut_mism)} mismatches); identity diagnostic {'TRIGGERED' if tautology_identity else 'not triggered'} ({n_ms_all_count_match}/{n_ms} Model S worlds match N60-from-0 at every R; {dec_equal_worlds}/{n_ms} have \(\\delta=\) joint decrements to \(10^{{-8}}\)) | **{taut_verdict}** |")
    lines.append(f"| SANITY (implementation) | 9 one-OU cells match L1; both \(K^*=0\) and \(1\) occur | {sum(1 for x in sanity_rows if x['ok'])}/9; K* seen {sorted(ks_seen)} | **{'PASS' if sanity_pass else 'FAIL'}** |")
    ms_ver = "NOT A TEST" if not_a_test else ("PASS" if ms_pass else "FAIL")
    rm_ver = "NOT A TEST" if not_a_test else ("PASS" if rm_pass else "FAIL")
    hole_ver = "NOT A TEST" if not_a_test else ("PASS" if hole_pass else "FAIL")
    lines.append(f"| PRIMARY Model S | \(\\ge 95\%\) of determinate cells | **{g_ms['n_match']}/{g_ms['n_det']} = {pct(g_ms['rate'])}** ({g_ms['n_indet']} INDETERMINATE of {g_ms['n_cells']}) | **{ms_ver}** |")
    lines.append(f"| PRIMARY rhythmic+mixed | \(\\ge 90\%\) of determinate cells | **{g_rm['n_match']}/{g_rm['n_det']} = {pct(g_rm['rate'])}** (rhythm {g_all_r['n_match']}/{g_all_r['n_det']}, mixed {g_all_m['n_match']}/{g_all_m['n_det']}; {g_rm['n_indet']} INDETERMINATE of {g_rm['n_cells']}) | **{rm_ver}** |")
    lines.append(f"| HOLE | \(\\ge 95\%\) of Model S cells with true argmin \(0\) predicted \(0\) | **{g_ms['hole_hit']}/{g_ms['hole_true']} = {pct(g_ms['hole_rate'])}** | **{hole_ver}** |")
    lines.append("")
    if not_a_test:
        lines.append("The identity diagnostic triggered, so the official confirmation gates are **NOT A TEST**. Numbers are reported anyway.")
        lines.append("")
    lines.append("## Mapping")
    lines.append("")
    if not taut_ok:
        lines.append("The tautology re-application failed; confirmation is invalid.")
    elif tautology_identity:
        lines.append("WF-HSV reproduced N60-from-0 *and* the joint decrements on every Model S world, so it may be an identity rather than a prediction. See the diagnostic table.")
    elif ms_pass and rm_pass:
        lines.append("The derived count rule passed both primary gates. The mapping of the keystone to reverse water-filling holds in the translated form of MATH.md §7 (discrete water-filling on the joint Kalman estimate's \(H_2\) energies), as a *count*, in-model and numerical, on these fresh worlds. It is not a process-band placement rule, and it is not a proof.")
    elif ms_pass and not rm_pass:
        lines.append("WF-HSV recovers Model S (where N60 is already exact) but misses the 90% bar on fresh rhythmic and mixed worlds. The translation works for real-pole worlds and is not the missing predictive rhythm rule.")
    elif (not ms_pass) and rm_pass:
        lines.append("Unexpected pattern: rhythmic+mixed passed and Model S failed. This is suspicious and is not read as support for the mapping.")
    else:
        lines.append("WF-HSV failed the Model S primary gate, so this translation of reverse water-filling does not recover the class the keystone already has. The mapping, as stated in MATH.md §7, does not hold as a predictive layer-count rule. The predictive rhythm count stays open.")
    lines.append("")
    lines.append("## Identity diagnostic (Model S)")
    lines.append("")
    lines.append(f"Worlds in which \(K^*_{{WF}}=\) N60-from-0 at every R: {n_ms_all_count_match}/{n_ms}.")
    lines.append(f"Worlds in which sorted \(\\delta_i\) equal the optimised joint decrements to \(10^{{-8}}\) relative: {dec_equal_worlds}/{n_ms}.")
    if dec_notes:
        rels = [d["max_rel"] for d in dec_notes if d["max_rel"] is not None]
        if rels:
            lines.append(f"Max relative discrepancy between \(\\delta\) and joint decrements, over worlds: {max(rels):.4g} (median {float(np.median(rels)):.4g}).")
    lines.append("")
    lines.append("## Suspicious points")
    lines.append("")
    flags = []
    for r in results["model_s"] + results["rhythm"] + results["mixed"]:
        if r.get("floor_flag") or r.get("flags"):
            flags.append(f"- `{r['id']}`: floor_flag={r.get('floor_flag')} flags={r.get('flags')}")
    if flags:
        lines.append("Floor / optimiser flags:")
        lines.extend(flags[:40])
        if len(flags) > 40:
            lines.append(f"- … and {len(flags)-40} more")
    else:
        lines.append("No E_inf floor flags.")
    # mismatches examples
    miss = []
    for r in results["model_s"] + results["rhythm"] + results["mixed"]:
        for c in r["cells"]:
            if c["pred_status"] == "OK" and not c["match"]:
                miss.append((r["id"], c))
    lines.append(f"Mismatches (determinate): {len(miss)}.")
    for wid, c in miss[:15]:
        lines.append(f"- `{wid}` at R={c['R']}: predicted {c['predicted']}, argmin {c['argmin']} (ties {c['ties']})")
    if len(miss) > 15:
        lines.append(f"- … and {len(miss)-15} more")
    lines.append("")
    lines.append("Related, not confirmation: the T20 fair fractal test found \(K^*\) growing roughly linearly in \(\\log R\) and store rates on the *observer* (fast) side, not on process bands. This test did not score those worlds and did not predict placement.")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- `PREREG.md`, `MATH.md`, `RESULTS.md` (this file) in `theory/keystone_checks/waterfill_2026-11-20/`.")
    lines.append("- `waterfill/wf_predictions.json`, `PREDICTIONS.sha256`, `LOCK.txt`, `START.txt`, `wf_run.json`, `DEVIATIONS_2026-11-20.md`.")
    lines.append("")
    Path(HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    # also dump score json
    (HERE / "wf_score.json").write_text(json.dumps(dict(
        g_ms=g_ms, g_rm=g_rm, g_rhythm=g_all_r, g_mixed=g_all_m,
        taut_ok=taut_ok, taut_mism_n=len(taut_mism),
        tautology_identity=tautology_identity,
        n_ms_all_count_match=n_ms_all_count_match, n_ms=n_ms,
        dec_equal_worlds=dec_equal_worlds,
        sanity_pass=sanity_pass, ms_pass=ms_pass, rm_pass=rm_pass, hole_pass=hole_pass,
        not_a_test=not_a_test,
        n_mismatch=len(miss),
    ), indent=2, default=str))
    return HERE / "RESULTS.md"


def main():
    pred_sha = sha256(PRED)
    expected = (HERE / "PREDICTIONS.sha256").read_text().split()[0]
    assert pred_sha == expected, (pred_sha, expected)
    pred = json.loads(PRED.read_text())
    start_path = HERE / "START.txt"
    if not start_path.is_file():
        ts = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        start_path.write_text(
            f"Official start: {ts} (America/New_York)\n"
            f"predictions sha256 {pred_sha}\n"
            f"prereg sha256 {pred['prereg_sha256']}\n"
            "No E_K work before this start.\n"
        )
        start_ts = ts
    else:
        start_ts = start_path.read_text().splitlines()[0]
    run = load_run()
    if run.get("started") is None:
        run["started"] = start_ts
        run["pred_sha256"] = pred_sha
        save_run(run)

    # Phase 1: Model S
    ms_todo = [w for w in pred["model_s"] if w["id"] not in run["worlds"]]
    print(f"Model S todo {len(ms_todo)} / {len(pred['model_s'])}", flush=True)
    if ms_todo:
        items = [(w, w["i"]) for w in ms_todo]
        with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
            futs = {ex.submit(run_model_s_world, it): it[0]["id"] for it in items}
            for fut in as_completed(futs):
                wid = futs[fut]
                try:
                    row = fut.result()
                except Exception as e:
                    row = dict(id=wid, cls="model_s", error=str(e),
                               traceback=traceback.format_exc())
                    print(f"ERROR {wid}: {e}", flush=True)
                run["worlds"][wid] = row
                save_run(run)
                print(f"done {wid} elapsed={row.get('elapsed')} flags={row.get('flags')}", flush=True)

    # Phase 2: rhythm + mixed
    rh_todo = [w for w in pred["rhythm"] if w["id"] not in run["worlds"]]
    mx_todo = [w for w in pred["mixed"] if w["id"] not in run["worlds"]]
    print(f"rhythm todo {len(rh_todo)} / {len(pred['rhythm'])}; mixed todo {len(mx_todo)} / {len(pred['mixed'])}", flush=True)
    items = [(w, w["i"], 0) for w in rh_todo] + [(w, w["i"], 100) for w in mx_todo]
    if items:
        with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
            futs = {ex.submit(run_extended_world, it): it[0]["id"] for it in items}
            for fut in as_completed(futs):
                wid = futs[fut]
                try:
                    row = fut.result()
                except Exception as e:
                    row = dict(id=wid, cls="extended", error=str(e),
                               traceback=traceback.format_exc())
                    print(f"ERROR {wid}: {e}", flush=True)
                run["worlds"][wid] = row
                save_run(run)
                print(f"done {wid} elapsed={row.get('elapsed')} flags={row.get('flags')}", flush=True)

    n_ok = sum(1 for w in run["worlds"].values() if "error" not in w)
    n_all = len(pred["model_s"]) + len(pred["rhythm"]) + len(pred["mixed"])
    print(f"completed {n_ok}/{n_all} worlds; scoring…", flush=True)
    if n_ok == n_all:
        results, taut_ok, taut_mism = score_all(pred, run)
        path = write_results(pred, run, results, taut_ok, taut_mism, start_ts, pred_sha)
        run["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
        run["scored"] = True
        save_run(run)
        print(f"wrote {path}", flush=True)
    else:
        print("incomplete; not writing official RESULTS.md", flush=True)


if __name__ == "__main__":
    main()
