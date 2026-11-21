#!/usr/bin/env python3
"""Official run for RHYTHM_PREREG.md.

Order (required): write IMP-N60 predictions + SHA-256, then SANITY, Part A,
cymatics, fractal, Model S extended-library subset. nice 19, ~2.5 h cap.

Run: nice -n 19 python3 run_rhythm_im.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR))

import resonant_layers as rl
import rhythm_rule as rr

DEADLINE_S = int(os.environ.get("RHYTHM_DEADLINE_S", str(int(2.2 * 3600))))
N_WORKERS = 6
BASE_SEED = rl.BASE_SEED
R_GRID = list(rl.R_GRID)
S5_R_GRID = np.logspace(-1, 7, 161)

PREREG = DIR / "RHYTHM_PREREG.md"
PRED_PATH = DIR / "imp_n60_predictions.json"
RUN_PATH = DIR / "rhythm_im_run.json"
LOG_PATH = DIR / "rhythm_im_run.log"

T0 = time.time()


def remaining():
    return DEADLINE_S - (time.time() - T0)


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def to_py(x):
    if isinstance(x, dict):
        return {str(k): to_py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_py(v) for v in x]
    if isinstance(x, np.ndarray):
        return to_py(x.tolist())
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, complex):
        return [float(x.real), float(x.imag)]
    return x


def save_run(run):
    tmp = RUN_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(to_py(run), f, indent=1)
    tmp.replace(RUN_PATH)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- worlds ----------
def part_a_worlds():
    worlds = rr.world_list()
    for i, w in enumerate(worlds):
        w["index"] = i
        w["a"] = np.asarray(w["a"])
        w["v"] = np.asarray(w["v"])
    return worlds


def s5_worlds():
    data = json.loads((DIR / "s5_rerun.json").read_text())
    return data["worlds"]


def fractal_spec(alpha, Gamma, per_decade, tau_min=1.0, N=0.05):
    # same construction as stores.scalefree_world
    J = max(2, int(round(per_decade * np.log10(Gamma))) + 1)
    tau = tau_min * np.logspace(0, np.log10(Gamma), J)
    v = tau ** (alpha - 1)
    v = v / v.sum()
    a = 1.0 / tau
    return dict(alpha=float(alpha), Gamma=float(Gamma), per_decade=int(per_decade),
                tau_min=float(tau_min), N=float(N), J=int(J),
                a=a, v=v, taus=tau)


def fractal_primary():
    specs = []
    for gi, Gamma in enumerate([10, 100, 1000, 10000]):
        for ai, alpha in enumerate([0.5, 1.0, 1.5]):
            s = fractal_spec(alpha, Gamma, per_decade=1)
            s["arm"] = "primary"
            s["Gamma_index"] = gi
            s["alpha_index"] = ai
            s["id"] = f"frac_a{alpha}_G{Gamma:g}_pd1"
            specs.append(s)
    return specs


def fractal_extra():
    specs = []
    for gi, Gamma in enumerate([10, 100, 1000]):
        s = fractal_spec(1.0, Gamma, per_decade=2)
        s["arm"] = "per_decade_2"
        s["Gamma_index"] = gi
        s["alpha_index"] = 0
        s["id"] = f"frac_a1_G{Gamma:g}_pd2"
        specs.append(s)
    return specs


# ---------- predictions (no optimizer) ----------
def build_predictions():
    prereg_sha = sha256_file(PREREG)
    worlds = part_a_worlds()
    part_a = []
    for w in worlds:
        Einf = rl.E_inf_YJ(w["a"], w["v"], w["N"])
        per_R = []
        for R in R_GRID:
            pred = rl.imp_n60(w["a"], w["v"], w["N"], R, E_inf=Einf)
            per_R.append(dict(R=float(R), C_star=pred["C_star"],
                              n_res=pred["n_res"], n_first=pred["n_first"],
                              included=pred["included"], modes=pred["modes"]))
        part_a.append(dict(
            id=w["id"], index=w["index"], n=w["n"], N=float(w["N"]),
            E_inf=float(Einf), var0=rl.var0(w["v"]),
            modes=rl.imp_n60(w["a"], w["v"], w["N"], 1.0, E_inf=Einf)["modes"],
            per_R=per_R,
        ))

    # Model S closed-form vs later comparison; predictions only here
    s5 = []
    for w in s5_worlds():
        a = np.asarray(w["a"], float)
        v = np.asarray(w["v"], float)
        N = float(w["N"])
        Einf = float(w["Einf_YJ"])
        # sanity: don't trust a stale Einf; use stored (closed form already)
        preds = []
        # store compact: list of C* aligned with S5_R_GRID; plus mode Vs once
        base = rl.imp_n60(a, v, N, 1.0, E_inf=Einf)
        C_star = []
        included = []
        for R in S5_R_GRID:
            take = [i for i, m in enumerate(base["modes"]) if (R * m["V"]) > 1]
            C_star.append(len(take))  # c_m=1
            included.append(take)
        s5.append(dict(
            seed=int(w["seed"]), J=int(w["J"]), N=N, E_inf=Einf,
            var0=float(w["E0"]) if "E0" in w else rl.var0(v),
            modes=base["modes"],
            C_star=C_star,
        ))

    # fractal closed-form IMP-N60 (first-order modes)
    frac_R = [1, 3, 10, 30, 100, 300]
    fractal = []
    for s in fractal_primary() + fractal_extra():
        Einf = rl.E_inf_YJ(s["a"], s["v"], s["N"])
        per_R = []
        for R in frac_R:
            pred = rl.imp_n60(s["a"], s["v"], s["N"], R, E_inf=Einf)
            per_R.append(dict(R=float(R), C_star=pred["C_star"],
                              included=pred["included"], modes=pred["modes"]))
        fractal.append(dict(
            id=s["id"], arm=s["arm"], alpha=s["alpha"], Gamma=s["Gamma"],
            per_decade=s["per_decade"], J=s["J"], N=s["N"], E_inf=float(Einf),
            var0=rl.var0(s["v"]), per_R=per_R,
        ))

    # cymatics frequency-sweep worlds (closed form, before those opts)
    freq_points = np.logspace(np.log10(0.1), np.log10(8.0), 31)
    cym_freq = []
    for i, w2 in enumerate(freq_points):
        a, v, N = rr.osc_world([0.05, float(w2)], [0.02, 0.02], [0.5, 0.5], 0.04)
        Einf = rl.E_inf_YJ(a, v, N)
        pred = rl.imp_n60(a, v, N, 3.0, E_inf=Einf)
        cym_freq.append(dict(
            i=i, omega2=float(w2), E_inf=float(Einf), var0=rl.var0(v),
            C_star=pred["C_star"], n_res=pred["n_res"], included=pred["included"],
            modes=pred["modes"],
        ))

    stake_points = np.logspace(np.log10(0.25), np.log10(200), 41)
    # predictions for 2osc_sep15_light_light at dense R (same world as Part A)
    w_stakes = next(w for w in worlds if w["id"] == "2osc_sep15_light_light")
    Einf_s = rl.E_inf_YJ(w_stakes["a"], w_stakes["v"], w_stakes["N"])
    cym_stakes = []
    for i, R in enumerate(stake_points):
        pred = rl.imp_n60(w_stakes["a"], w_stakes["v"], w_stakes["N"], float(R), E_inf=Einf_s)
        cym_stakes.append(dict(i=i, R=float(R), C_star=pred["C_star"],
                               n_res=pred["n_res"], included=pred["included"]))

    payload = dict(
        locked_note="IMP-N60 predictions from poles, variances, N, R only. "
                    "No library optimizer was called to produce this file.",
        written_et=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        prereg_sha256=prereg_sha,
        prereg_path=str(PREREG),
        BASE_SEED=BASE_SEED,
        R_GRID=R_GRID,
        S5_R_GRID=S5_R_GRID.tolist(),
        part_a=part_a,
        s5=s5,
        fractal=fractal,
        cymatics_frequency_sweep=cym_freq,
        cymatics_stakes_sweep=cym_stakes,
        formula="include mode m iff R * (sigma_m^2 - E_inf^{(m)}) / E_inf > c_m",
    )
    tmp = PRED_PATH.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(to_py(payload), f, indent=1)
    tmp.replace(PRED_PATH)
    return payload, sha256_file(PRED_PATH), prereg_sha


# ---------- optimizer worker ----------
def _opt_task(payload):
    """payload: id, a, v, N, n_res, n_first, seed, use_de, n_rand, extra_inits?"""
    a = np.asarray(payload["a"], dtype=complex if np.iscomplexobj(np.asarray(payload["a"]))
                   or any(isinstance(x, complex) or (isinstance(x, list) and len(x)==2)
                          for x in (payload["a"] if not isinstance(payload["a"], np.ndarray)
                                    else payload["a"].tolist())) else float)
    # recover complex poles stored as [re, im]
    a_in = payload["a"]
    if isinstance(a_in, list) and a_in and isinstance(a_in[0], (list, tuple)):
        a = np.array([complex(x[0], x[1]) for x in a_in], dtype=complex)
    else:
        a = np.asarray(payload["a"], complex)
    v_in = payload["v"]
    if isinstance(v_in, list) and v_in and isinstance(v_in[0], (list, tuple)):
        v = np.array([complex(x[0], x[1]) for x in v_in], dtype=complex)
    else:
        v = np.asarray(payload["v"], complex)
    extra = payload.get("extra_inits")
    out = rl.optimize_design(
        a, v, float(payload["N"]),
        int(payload["n_first"]), int(payload["n_res"]),
        seed=int(payload["seed"]),
        n_rand=int(payload.get("n_rand", 16)),
        use_de=bool(payload.get("use_de", True)),
        de_maxiter=payload.get("de_maxiter"),
        extra_inits=extra,
    )
    out["id"] = payload.get("id")
    out["tag"] = payload.get("tag")
    return out


def encode_av(a, v):
    a = np.asarray(a)
    v = np.asarray(v)
    return ([[float(z.real), float(z.imag)] for z in a],
            [[float(z.real), float(z.imag)] for z in v])


def run_pool(tasks, label):
    """Run optimize tasks; skip if remaining time is tight."""
    results = []
    if not tasks:
        return results
    if remaining() < 30:
        log(f"SKIP {label}: no time left ({remaining():.0f}s)")
        return [dict(tag=t.get("tag"), id=t.get("id"), skipped=True, reason="deadline") for t in tasks]
    workers = min(N_WORKERS, len(tasks), max(1, os.cpu_count() or 1))
    log(f"START {label}: {len(tasks)} tasks, {workers} workers, remaining {remaining():.0f}s")
    # If few tasks, still pool
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_opt_task, t): t for t in tasks}
        done = 0
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = dict(id=t.get("id"), tag=t.get("tag"), error=str(e),
                         traceback=traceback.format_exc(), E=float("inf"))
            results.append(r)
            done += 1
            if done % 5 == 0 or done == len(tasks):
                ev = r.get("E")
                log(f"  {label} {done}/{len(tasks)} last={r.get('id')} {r.get('tag')} "
                    f"E={ev} t={r.get('elapsed', 0):.1f}s rem={remaining():.0f}s")
            if remaining() < 20:
                log(f"DEADLINE during {label}; cancelling remainder")
                for f in futs:
                    f.cancel()
                break
    return results


# ---------- scoring helpers ----------
def argmin_from_designs(designs, E_inf, R, tie=1e-9):
    """designs: list of dicts with C, E. Leftmost min J."""
    best = None
    scored = []
    for d in designs:
        E, C = d.get("E"), d.get("C")
        if E is None or not np.isfinite(E) or C is None:
            continue
        J = rl.J_of_E(C, E, E_inf, R)
        scored.append((J, C, d))
    if not scored:
        return None, []
    scored.sort(key=lambda t: (t[0], t[1]))
    Jmin = scored[0][0]
    winners = [t for t in scored if abs(t[0] - Jmin) <= tie * max(1.0, abs(Jmin))]
    best = winners[0]  # leftmost already by C after J
    # among co-minima, lowest C
    best = min(winners, key=lambda t: (t[1], t[0]))
    return dict(J=float(best[0]), C=int(best[1]),
                n_res=best[2].get("n_res"), n_first=best[2].get("n_first"),
                tag=best[2].get("tag"), E=float(best[2]["E"]),
                co_minima_C=[int(w[1]) for w in winners]), scored


def first_order_designs_from_rr(row):
    """K=0..Kmax first-order designs already in rhythm_rule.json."""
    out = []
    E = row["E"]  # includes K=0
    for K, e in enumerate(E):
        out.append(dict(C=K, E=float(e), n_res=0, n_first=K,
                        tag=f"first_only_K{K}", first=row.get("stores", [None]*len(E))[K]
                        if K < len(row.get("stores", [])) else None,
                        resonants=[], method=row.get("methods", [None]*len(E))[K]
                        if K < len(row.get("methods", [])) else "stored"))
    return out


# ---------- main ----------
def main():
    if LOG_PATH.exists():
        # append a restart marker
        log("==== run_rhythm_im start / continue ====")
    else:
        log("==== run_rhythm_im start ====")

    # (1) predictions first, never overwrite if already hashed mid-run
    if PRED_PATH.exists():
        pred_sha = sha256_file(PRED_PATH)
        log(f"predictions already exist sha256={pred_sha} (not overwritten)")
        pred = json.loads(PRED_PATH.read_text())
        prereg_sha = pred.get("prereg_sha256") or sha256_file(PREREG)
    else:
        log("writing IMP-N60 predictions (no optimizer)...")
        pred, pred_sha, prereg_sha = build_predictions()
        log(f"wrote {PRED_PATH.name} sha256={pred_sha}")
        log(f"prereg sha256={prereg_sha}")

    run = dict(
        started_et=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
        prereg_sha256=prereg_sha,
        predictions_sha256=pred_sha,
        deadline_s=DEADLINE_S,
        sanity={},
        part_a={},
        cymatics={},
        fractal={},
        s5_regression={},
        s5_extended={},
    )
    if RUN_PATH.exists():
        try:
            prev = json.loads(RUN_PATH.read_text())
            # keep completed sections
            for k in ("sanity", "part_a", "cymatics", "fractal", "s5_regression", "s5_extended"):
                if prev.get(k):
                    run[k] = prev[k]
            log("resumed prior run file")
        except Exception as e:
            log(f"could not resume run file: {e}")

    worlds = part_a_worlds()
    rr_json = json.loads((DIR / "rhythm_rule.json").read_text())
    rr_by_id = {row["id"]: row for row in rr_json["results"]}

    # (2) SANITY
    if not run.get("sanity", {}).get("done"):
        log("SANITY: one resonant layer on each 1-oscillator world")
        tasks = []
        for w in worlds:
            if w["n"] != 1:
                continue
            a, v = encode_av(w["a"], w["v"])
            tasks.append(dict(
                id=w["id"], a=a, v=v, N=w["N"], n_res=1, n_first=0,
                seed=rl.opt_seed(w["index"], 1, 0), use_de=True, n_rand=16,
                tag="sanity_nres1",
            ))
        res = run_pool(tasks, "sanity")
        rows = []
        kill = False
        for r in res:
            wid = r.get("id")
            w = next(x for x in worlds if x["id"] == wid)
            Einf = next(p["E_inf"] for p in pred["part_a"] if p["id"] == wid)
            E = r.get("E", np.inf)
            eps = float(E / Einf - 1) if np.isfinite(E) and Einf > 0 else np.inf
            # matched-pole report (not a kill)
            m = w["meta"]
            mp = rl.lyapunov_mse(w["a"], w["v"], w["N"], [],
                                 [(float(m["zetas"][0]) * float(m["omegas"][0]),
                                   float(m["omegas"][0]))])
            below = bool(np.isfinite(E) and E < Einf - 1e-9)
            rows.append(dict(
                id=wid, E=E, E_inf=Einf, eps=eps, below_Einf=below, pass_=(eps < 1e-3 and not below),
                resonants=r.get("resonants"), method=r.get("method"),
                elapsed=r.get("elapsed"),
                matched_pole_E=mp["mse"],
                matched_pole_eps=float(mp["mse"] / Einf - 1) if Einf else None,
            ))
            if not (eps < 1e-3) or below:
                kill = True
        run["sanity"] = dict(done=True, kill=kill, rows=rows)
        save_run(run)
        log(f"SANITY done kill={kill} n={len(rows)}")
    else:
        log("SANITY already done")

    # (3) Part A optimizations
    pa = run.get("part_a") or {}
    if not pa.get("done"):
        done_tags = set(pa.get("done_tags", []))
        tasks = []
        for w in worlds:
            for n_res, n_first in rl.part_a_compositions(w["n"]):
                if n_res == 0 and n_first == 0:
                    continue  # closed form
                tag = f"{w['id']}::nr{n_res}_nf{n_first}"
                if tag in done_tags:
                    continue
                a, v = encode_av(w["a"], w["v"])
                dim = n_first + 2 * n_res
                tasks.append(dict(
                    id=w["id"], a=a, v=v, N=w["N"], n_res=n_res, n_first=n_first,
                    seed=rl.opt_seed(w["index"], n_res, n_first),
                    use_de=(dim <= 6), n_rand=16,
                    tag=tag,
                ))
        log(f"Part A remaining tasks: {len(tasks)}")
        # run in chunks so we can save
        chunk = 8
        acc = list(pa.get("opts", []))
        for i in range(0, len(tasks), chunk):
            if remaining() < 60:
                log("Part A stopped for deadline before fractal/cymatics reserved time")
                break
            # reserve ~45 min for cymatics freq + fractal + s5 extended if Part A is large
            # but prereg order is Part A before those, MUST world first among Part A.
            part = tasks[i:i + chunk]
            acc.extend(run_pool(part, f"partA[{i}:{i+len(part)}]"))
            pa["opts"] = acc
            pa["done_tags"] = [r["tag"] for r in acc if r.get("tag")]
            run["part_a"] = pa
            save_run(run)
        # mark done if all tasks finished (or there were none left)
        finished_tags = set(pa.get("done_tags", []))
        all_tags = {t["tag"] for t in tasks} | finished_tags
        planned = []
        for w in worlds:
            for n_res, n_first in rl.part_a_compositions(w["n"]):
                if n_res == 0 and n_first == 0:
                    continue
                planned.append(f"{w['id']}::nr{n_res}_nf{n_first}")
        pa["done"] = all(t in finished_tags for t in planned)
        pa["planned"] = planned
        run["part_a"] = pa
        save_run(run)
        log(f"Part A done={pa['done']} n_opts={len(pa.get('opts', []))}")
    else:
        log("Part A already done")

    # Score Part A (cheap)
    opts_by_id = {}
    for r in run.get("part_a", {}).get("opts", []):
        opts_by_id.setdefault(r.get("id"), []).append(r)

    comparisons = []
    for w in worlds:
        prow = next(p for p in pred["part_a"] if p["id"] == w["id"])
        Einf = prow["E_inf"]
        designs = first_order_designs_from_rr(rr_by_id[w["id"]])
        designs.append(dict(C=0, E=prow["var0"], n_res=0, n_first=0, tag="blind"))
        for r in opts_by_id.get(w["id"], []):
            if r.get("E") is None or not np.isfinite(r.get("E", np.nan)):
                continue
            designs.append(dict(C=r["C"], E=r["E"], n_res=r.get("n_res"),
                                n_first=r.get("n_first"), tag=r.get("tag"),
                                first=r.get("first"), resonants=r.get("resonants"),
                                method=r.get("method")))
        # unique by (tag or C,n_res,n_first,E)
        per_R = []
        for R in R_GRID:
            arg, _ = argmin_from_designs(designs, Einf, R)
            predR = next(x for x in prow["per_R"] if abs(x["R"] - R) < 1e-12)
            match = False
            if arg is not None:
                match = (predR["C_star"] == arg["C"]) or (predR["C_star"] in arg.get("co_minima_C", []))
            per_R.append(dict(R=R, predicted_C=predR["C_star"], predicted_n_res=predR["n_res"],
                              argmin=arg, match=match))
        comparisons.append(dict(id=w["id"], n=w["n"], E_inf=Einf, per_R=per_R,
                                n_designs=len(designs)))
    n_comp = sum(len(c["per_R"]) for c in comparisons)
    n_match = sum(1 for c in comparisons for r in c["per_R"] if r["match"])
    must = next(r for c in comparisons if c["id"] == "seed2_two_light"
                for r in c["per_R"] if r["R"] == 3.0)
    run["part_a_score"] = dict(
        n_comparisons=n_comp, n_match=n_match,
        rate=(n_match / n_comp if n_comp else None),
        pass_primary=(n_comp == 189 and n_match >= 180),
        must_seed2_R3=must,
        must_pass=bool(must.get("match")),
        comparisons=comparisons,
        incomplete=not run.get("part_a", {}).get("done", False),
    )
    save_run(run)
    log(f"Part A score: {n_match}/{n_comp} must_R3={must}")

    # (4) Cymatics (a) from Part A n_res=n fits
    lock_rows = []
    light_medians = []
    for w in worlds:
        n = w["n"]
        # find n_res=n, n_first=0
        cands = [r for r in opts_by_id.get(w["id"], [])
                 if r.get("n_res") == n and r.get("n_first") == 0 and r.get("resonants")]
        if not cands:
            continue
        r = min(cands, key=lambda d: d.get("E", np.inf))
        omegas = w["meta"]["omegas"]
        lock = rl.locking_errors(r["resonants"], omegas)
        zetas = w["meta"]["zetas"]
        light = all(z <= 0.08 for z in zetas)
        lock_rows.append(dict(id=w["id"], light=light, zetas=zetas, omegas=omegas,
                              resonants=r["resonants"], E=r["E"], lock=lock))
        if light and lock["median"] is not None:
            light_medians.append(lock["median"])
    # overall median of per-world medians, and also pooled? prereg: median relative
    # locking error ... is < 0.05. We'll report median-of-medians and pooled median.
    pooled = [e for row in lock_rows if row["light"] for e in row["lock"]["errors"]]
    cym_a = dict(
        rows=lock_rows,
        light_n=len(light_medians),
        median_of_world_medians=float(np.median(light_medians)) if light_medians else None,
        pooled_median=float(np.median(pooled)) if pooled else None,
        pass_=(float(np.median(pooled)) < 0.05 if pooled else False),
    )
    run["cymatics"]["a"] = cym_a
    save_run(run)
    log(f"Cymatics (a) pooled_median={cym_a['pooled_median']} pass={cym_a['pass_']}")

    # (4b) stakes sweep: no new opts; dense R on 2osc_sep15_light_light
    wid = "2osc_sep15_light_light"
    w = next(x for x in worlds if x["id"] == wid)
    prow = next(p for p in pred["part_a"] if p["id"] == wid)
    Einf = prow["E_inf"]
    designs = first_order_designs_from_rr(rr_by_id[wid])
    designs.append(dict(C=0, E=prow["var0"], n_res=0, n_first=0, tag="blind"))
    for r in opts_by_id.get(wid, []):
        if r.get("E") is None or not np.isfinite(r.get("E", np.nan)):
            continue
        designs.append(dict(C=r["C"], E=r["E"], n_res=r.get("n_res"),
                            n_first=r.get("n_first"), tag=r.get("tag")))
    stake_points = np.logspace(np.log10(0.25), np.log10(200), 41)
    stake_trace = []
    for i, R in enumerate(stake_points):
        arg, _ = argmin_from_designs(designs, Einf, float(R))
        predR = pred["cymatics_stakes_sweep"][i]
        stake_trace.append(dict(
            i=i, R=float(R), argmin=arg,
            predicted_C=predR["C_star"],
            match=(arg is not None and (predR["C_star"] == arg["C"] or predR["C_star"] in arg.get("co_minima_C", []))),
        ))
    # jumps: places where composition changes
    jumps = []
    for a, b in zip(stake_trace, stake_trace[1:]):
        ca = (None if a["argmin"] is None else (a["argmin"]["C"], a["argmin"].get("n_res"), a["argmin"].get("n_first")))
        cb = (None if b["argmin"] is None else (b["argmin"]["C"], b["argmin"].get("n_res"), b["argmin"].get("n_first")))
        if ca != cb:
            jumps.append(dict(between_R=[a["R"], b["R"]], from_=ca, to=cb,
                              J_from=None if a["argmin"] is None else a["argmin"]["J"],
                              J_to=None if b["argmin"] is None else b["argmin"]["J"]))
    run["cymatics"]["stakes"] = dict(world=wid, n_points=len(stake_trace),
                                     n_jumps=len(jumps), jumps=jumps, trace=stake_trace)
    save_run(run)
    log(f"Cymatics stakes: {len(jumps)} jumps")

    # (4b) frequency sweep — re-optimize
    freq_points = np.logspace(np.log10(0.1), np.log10(8.0), 31)
    freq_run = run["cymatics"].get("frequency") or {}
    done_pts = set(freq_run.get("done_i", []))
    freq_opts = list(freq_run.get("opts", []))
    if remaining() > 90:
        tasks = []
        # compositions for n=2
        comps = [c for c in rl.part_a_compositions(2) if not (c == (0, 0))]
        # first-order only also needed: n_first=1..6 (2n+2)
        for nf in range(1, 7):
            if (0, nf) not in comps:
                comps.append((0, nf))
        for i, w2 in enumerate(freq_points):
            if i in done_pts:
                continue
            a, v, N = rr.osc_world([0.05, float(w2)], [0.02, 0.02], [0.5, 0.5], 0.04)
            ae, ve = encode_av(a, v)
            for n_res, n_first in comps:
                dim = n_first + 2 * n_res
                # warm start from previous point's same composition if we have it
                extra = None
                prev = [o for o in freq_opts
                        if o.get("i") == i - 1 and o.get("n_res") == n_res
                        and o.get("n_first") == n_first and o.get("first") is not None]
                if prev and prev[-1].get("resonants") is not None:
                    try:
                        extra = [rl.pack_params(prev[-1]["first"], prev[-1]["resonants"]).tolist()]
                    except Exception:
                        extra = None
                tasks.append(dict(
                    id=f"freq_{i}", i=i, omega2=float(w2),
                    a=ae, v=ve, N=N, n_res=n_res, n_first=n_first,
                    seed=BASE_SEED + 90000 + i + 17 * rl.composition_key(n_res, n_first),
                    use_de=(dim <= 4 and remaining() > 600),  # DE only early/cheap
                    n_rand=10, de_maxiter=20,
                    tag=f"freq_{i}::nr{n_res}_nf{n_first}",
                    extra_inits=extra,
                    _i=i, _nr=n_res, _nf=n_first, _w2=float(w2),
                ))
        # attach i into returned via tag; also stash map
        meta = {t["tag"]: t for t in tasks}
        log(f"Frequency sweep tasks: {len(tasks)}")
        # chunk
        acc = freq_opts
        for i0 in range(0, len(tasks), 10):
            if remaining() < 120:
                log("freq sweep stopped to leave time for fractal")
                break
            part = tasks[i0:i0 + 10]
            got = run_pool(part, f"freq[{i0}:{i0+len(part)}]")
            for r in got:
                t = meta.get(r.get("tag"), {})
                r["i"] = t.get("_i")
                r["omega2"] = t.get("_w2")
                if r.get("n_res") is None:
                    r["n_res"] = t.get("_nr")
                    r["n_first"] = t.get("_nf")
                    if r.get("C") is None and r.get("n_res") is not None:
                        r["C"] = rl.degree_cost(r["n_first"], r["n_res"])
            acc.extend(got)
            done_i = sorted({r["i"] for r in acc if r.get("i") is not None})
            # a point is done if all comps present
            freq_run = dict(opts=acc, done_i=done_i)
            run["cymatics"]["frequency"] = freq_run
            save_run(run)
    else:
        log("skip freq sweep (no time)")

    # score frequency sweep for completed points
    freq_opts = run["cymatics"].get("frequency", {}).get("opts", [])
    freq_trace = []
    for i, w2 in enumerate(freq_points):
        opts_i = [o for o in freq_opts if o.get("i") == i and np.isfinite(o.get("E", np.nan))]
        if not opts_i:
            continue
        a, v, N = rr.osc_world([0.05, float(w2)], [0.02, 0.02], [0.5, 0.5], 0.04)
        Einf = pred["cymatics_frequency_sweep"][i]["E_inf"]
        designs = [dict(C=0, E=pred["cymatics_frequency_sweep"][i]["var0"],
                        n_res=0, n_first=0, tag="blind")]
        for o in opts_i:
            designs.append(dict(C=o.get("C"), E=o["E"], n_res=o.get("n_res"),
                                n_first=o.get("n_first"), tag=o.get("tag"),
                                resonants=o.get("resonants"), first=o.get("first")))
        arg, _ = argmin_from_designs(designs, Einf, 3.0)
        # locking if winner has resonants
        lock = None
        if arg and arg.get("tag"):
            win = next((d for d in designs if d.get("tag") == arg["tag"]), None)
            if win and win.get("resonants"):
                lock = rl.locking_errors(win["resonants"], [0.05, float(w2)])
        predC = pred["cymatics_frequency_sweep"][i]["C_star"]
        freq_trace.append(dict(
            i=i, omega2=float(w2), n_designs=len(designs), argmin=arg, lock=lock,
            predicted_C=predC,
            match=(arg is not None and (predC == arg["C"] or predC in arg.get("co_minima_C", []))),
        ))
    fjumps = []
    for a, b in zip(freq_trace, freq_trace[1:]):
        ca = (None if a["argmin"] is None else (a["argmin"]["C"], a["argmin"].get("n_res"), a["argmin"].get("n_first")))
        cb = (None if b["argmin"] is None else (b["argmin"]["C"], b["argmin"].get("n_res"), b["argmin"].get("n_first")))
        if ca != cb:
            fjumps.append(dict(between_omega2=[a["omega2"], b["omega2"]], from_=ca, to=cb))
    run["cymatics"]["frequency_score"] = dict(
        n_points=len(freq_trace), n_jumps=len(fjumps), jumps=fjumps, trace=freq_trace,
        incomplete=len(freq_trace) < 31,
    )
    save_run(run)
    log(f"Cymatics freq scored points={len(freq_trace)} jumps={len(fjumps)}")

    # (5) Fractal
    if remaining() > 60 and not run.get("fractal", {}).get("done"):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "stores_merged_frac",
            str(DIR.parents[1] / "theory" / "layers_checks" / "stores.py"),
        )
        st = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(st)

        def opt_first_only(a, v, N, K, seed):
            # reviewer multi-start using merged mse_given_b (s5 style)
            from scipy.optimize import minimize, differential_evolution
            a = np.asarray(a, float)
            v = np.asarray(v, float)
            rng = np.random.default_rng(seed)
            la = np.log(a)
            lo, hi = float(la.min() - 3), float(la.max() + 6)

            def safe(x, sep=1.02):
                x = np.sort(np.clip(np.asarray(x, float), -40, 40))
                for i in range(1, len(x)):
                    x[i] = max(x[i], x[i - 1] + np.log(sep))
                return x

            def obj(x):
                e, _ = st.mse_given_b(a, v, np.exp(safe(x)), N)
                return e if np.isfinite(e) else 1e12

            inits = [np.linspace(lo + 1, hi - 1, K), np.linspace(lo, hi, K)]
            for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
                pts = np.log(a * scale)
                if K > len(pts):
                    pts = np.r_[pts, pts[:K - len(pts)] + 0.2]
                inits.append(np.sort(pts[:K]))
            for _ in range(12):
                inits.append(np.sort(rng.uniform(lo, hi, K)))
            ranked = []
            for x0 in inits:
                try:
                    r = minimize(obj, x0, method="Nelder-Mead",
                                 options=dict(xatol=1e-8, fatol=1e-14, maxiter=2500 * K))
                    ranked.append((obj(r.x), r.x, "NM"))
                except Exception:
                    pass
            ranked.sort(key=lambda t: t[0])
            for x0 in [t[1] for t in ranked[:5]] + inits[:3]:
                try:
                    r = minimize(obj, x0, method="L-BFGS-B",
                                 bounds=[(lo - 2, hi + 2)] * K,
                                 options=dict(ftol=1e-14, maxiter=2000 * K))
                    ranked.append((obj(r.x), r.x, "LBFGS"))
                except Exception:
                    pass
            if K <= 6:
                try:
                    r = differential_evolution(obj, bounds=[(lo - 2, hi + 2)] * K,
                                               popsize=8, mutation=0.5, recombination=0.7,
                                               seed=int(seed) % (2**31 - 1), polish=True,
                                               workers=1, atol=1e-12, maxiter=25)
                    ranked.append((obj(r.x), r.x, "DE"))
                except Exception:
                    pass
            ranked.sort(key=lambda t: t[0])
            x = ranked[0][1]
            e, _ = st.mse_given_b(a, v, np.exp(safe(x)), N)
            return dict(E=float(e), stores=np.exp(safe(x)).tolist(), method=ranked[0][2], C=K)

        frac_specs = fractal_primary() + fractal_extra()
        frac_rows = list(run.get("fractal", {}).get("rows", []))
        done_ids = {r["id"] for r in frac_rows}
        for s in frac_specs:
            if s["id"] in done_ids:
                continue
            if remaining() < 40:
                log("fractal stopped on deadline")
                break
            log(f"fractal {s['id']} J={s['J']}")
            Einf = rl.E_inf_YJ(s["a"], s["v"], s["N"])
            E0 = rl.var0(s["v"])
            E = [E0]
            stores = [[]]
            methods = ["closed"]
            for K in range(1, s["J"] + 1):
                seed = BASE_SEED + 10000 + 100 * s["Gamma_index"] + 10 * s["alpha_index"] + K
                if s["arm"] != "primary":
                    seed = BASE_SEED + 20000 + 100 * s["Gamma_index"] + K
                r = opt_first_only(s["a"], s["v"], s["N"], K, seed)
                E.append(r["E"])
                stores.append(r["stores"])
                methods.append(r["method"])
                log(f"  K={K} E={r['E']:.8g} meth={r['method']} rem={remaining():.0f}s")
            eps = [e / Einf - 1 for e in E]
            dec = [eps[k] - eps[k + 1] for k in range(len(eps) - 1)]
            convex = all(dec[i] >= dec[i + 1] - 1e-4 for i in range(max(0, len(dec) - 1)))
            # CV of J decrements k=1..J (eps0-eps1, ..., eps_{J-1}-eps_J)
            dec_J = dec[:s["J"]] if len(dec) >= s["J"] else dec
            cv = None
            if dec_J and np.mean(dec_J) != 0:
                cv = float(np.std(dec_J, ddof=0) / abs(np.mean(dec_J)))
            per_R = []
            for R in [1, 3, 10, 30, 100, 300]:
                arg, _ = argmin_from_designs(
                    [dict(C=k, E=e, n_res=0, n_first=k, tag=f"K{k}") for k, e in enumerate(E)],
                    Einf, R,
                )
                # N60-from-0
                n60_0 = sum(1 for k in range(1, len(eps)) if R * (eps[k - 1] - eps[k]) > 1)
                per_R.append(dict(R=R, argmin=arg, n60_from0=n60_0,
                                  match_n60=(arg is not None and arg["C"] == n60_0)))
            frac_rows.append(dict(
                id=s["id"], arm=s["arm"], alpha=s["alpha"], Gamma=s["Gamma"],
                per_decade=s["per_decade"], J=s["J"], N=s["N"], E_inf=float(Einf),
                E=E, eps=eps, decrements=dec, convex=convex, cv_decrements=cv,
                stores=stores, methods=methods, per_R=per_R,
            ))
            run["fractal"] = dict(rows=frac_rows, done=False)
            save_run(run)
        planned_ids = [s["id"] for s in frac_specs]
        run["fractal"]["done"] = all(i in {r["id"] for r in frac_rows} for i in planned_ids)
        run["fractal"]["rows"] = frac_rows
        save_run(run)
        log(f"fractal done={run['fractal']['done']} n={len(frac_rows)}")
    else:
        log(f"fractal skipped or already present rem={remaining():.0f}")

    # (6) S5 closed-form regression (cheap)
    s5w = s5_worlds()
    n_tot = n_match = n_hole_true = n_hole_pred_ok = n_n60raw_match = 0
    misses = []
    for pw, w in zip(pred["s5"], s5w):
        assert pw["seed"] == w["seed"]
        Einf = float(w["Einf_YJ"])
        E = [float(w["E0"])] + [float(e) for e in w["E"]]  # E in s5 is K=1..J
        # confirm length
        eps = [e / Einf - 1 for e in E]
        for iR, R in enumerate(S5_R_GRID):
            J = [k + R * (1 + e) for k, e in enumerate(eps)]
            # leftmost min
            jmin = min(J)
            winners = [k for k, jv in enumerate(J) if abs(jv - jmin) <= 1e-9 * max(1.0, abs(jmin))]
            argC = min(winners)
            predC = pw["C_star"][iR]
            n_tot += 1
            if argC == 0:
                n_hole_true += 1
                if predC == 0:
                    n_hole_pred_ok += 1
            if predC == argC or predC in winners:
                n_match += 1
            else:
                if len(misses) < 40:
                    misses.append(dict(seed=w["seed"], R=float(R), pred=predC, arg=argC,
                                       winners=winners, J=[float(x) for x in J],
                                       V=[m["V"] for m in pw["modes"]]))
            # N60 as written (from 1)
            n60 = 1 + sum(1 for k in range(1, len(eps) - 0 - 1) if R * (eps[k] - eps[k + 1]) > 1) if len(eps) > 1 else 1
            # wait: N60 as written uses eps from K=1: 1 + #{k>=2: R(eps_{k-1}-eps_k)>1}
            if len(eps) >= 2:
                eps1 = eps[1:]  # K=1..
                n60_raw = 1 + sum(1 for k in range(1, len(eps1)) if R * (eps1[k - 1] - eps1[k]) > 1)
            else:
                n60_raw = 1
            if n60_raw == argC or n60_raw in winners:
                n_n60raw_match += 1
    run["s5_regression"] = dict(
        n_comparisons=n_tot, n_match=n_match, rate=(n_match / n_tot if n_tot else None),
        pass_=(n_match / n_tot >= 0.95 if n_tot else False),
        n_argmin0=n_hole_true, n_argmin0_predicted=n_hole_pred_ok,
        n_n60raw_match=n_n60raw_match,
        n_miss=n_tot - n_match,
        miss_examples=misses,
        done=True,
    )
    save_run(run)
    log(f"S5 regression: {n_match}/{n_tot} = {n_match/n_tot:.4f}  argmin0 {n_hole_pred_ok}/{n_hole_true}")

    # (7) 12-world Model S extended library
    ext_seeds = [0, 1, 2, 3, 4, 5, 50, 51, 52, 53, 54, 55]
    if remaining() > 40 and not run.get("s5_extended", {}).get("done"):
        ext_opts = list(run.get("s5_extended", {}).get("opts", []))
        done_tags = {o.get("tag") for o in ext_opts}
        tasks = []
        s5_by_seed = {int(w["seed"]): w for w in s5w}
        for seed in ext_seeds:
            w = s5_by_seed[seed]
            a, v, N = np.asarray(w["a"], float), np.asarray(w["v"], float), float(w["N"])
            ae, ve = encode_av(a, v)
            for n_res, n_first in [(1, 0), (2, 0), (1, 1)]:
                tag = f"s5_{seed}::nr{n_res}_nf{n_first}"
                if tag in done_tags:
                    continue
                dim = n_first + 2 * n_res
                tasks.append(dict(
                    id=f"s5_{seed}", seed_world=seed, a=ae, v=ve, N=N,
                    n_res=n_res, n_first=n_first,
                    seed=BASE_SEED + 30000 + 100 * seed + 17 * rl.composition_key(n_res, n_first),
                    use_de=(dim <= 6), n_rand=12, tag=tag,
                ))
        log(f"S5 extended tasks: {len(tasks)}")
        for i0 in range(0, len(tasks), 6):
            if remaining() < 20:
                break
            got = run_pool(tasks[i0:i0 + 6], f"s5ext[{i0}]")
            ext_opts.extend(got)
            run["s5_extended"] = dict(opts=ext_opts, done=False)
            save_run(run)
        run["s5_extended"]["opts"] = ext_opts
        run["s5_extended"]["done"] = all(
            f"s5_{seed}::nr{nr}_nf{nf}" in {o.get("tag") for o in ext_opts}
            for seed in ext_seeds for nr, nf in [(1, 0), (2, 0), (1, 1)]
        )
        save_run(run)
        log(f"S5 extended done={run['s5_extended']['done']} n={len(ext_opts)}")
    else:
        log(f"S5 extended skip rem={remaining():.0f}")

    # score 12-world extended vs first-order argmin on rhythm R grid
    ext_opts = run.get("s5_extended", {}).get("opts", [])
    ext_rows = []
    s5_by_seed = {int(w["seed"]): w for w in s5w}
    for seed in ext_seeds:
        w = s5_by_seed[seed]
        Einf = float(w["Einf_YJ"])
        Efo = [float(w["E0"])] + [float(e) for e in w["E"]]
        designs_fo = [dict(C=k, E=e, n_res=0, n_first=k, tag=f"fo{k}") for k, e in enumerate(Efo)]
        designs_all = list(designs_fo)
        for o in ext_opts:
            if o.get("id") != f"s5_{seed}" and o.get("tag", "").split("::")[0] != f"s5_{seed}":
                # also match seed_world
                if o.get("seed_world") != seed and not (o.get("tag") or "").startswith(f"s5_{seed}"):
                    continue
            if o.get("E") is None or not np.isfinite(o.get("E", np.nan)):
                continue
            if not (o.get("tag") or "").startswith(f"s5_{seed}"):
                continue
            designs_all.append(dict(C=o["C"], E=o["E"], n_res=o.get("n_res"),
                                    n_first=o.get("n_first"), tag=o.get("tag")))
        per_R = []
        changed = 0
        for R in R_GRID:
            arg_fo, _ = argmin_from_designs(designs_fo, Einf, R)
            arg_all, _ = argmin_from_designs(designs_all, Einf, R)
            ch = (arg_all is not None and arg_fo is not None and
                  (arg_all["C"] != arg_fo["C"] or (arg_all.get("n_res") or 0) != 0
                   and arg_all["J"] < arg_fo["J"] - 1e-9 * max(1, abs(arg_fo["J"]))))
            # "change argmin relative to first-order-only"
            changed_here = False
            if arg_all and arg_fo:
                # if the winner is a resonant design with strictly better J than fo winner
                fo_tags = {d["tag"] for d in designs_fo}
                if arg_all.get("tag") not in fo_tags and arg_all["J"] < arg_fo["J"] - 1e-9 * max(1, abs(arg_fo["J"])):
                    changed_here = True
                    changed += 1
            per_R.append(dict(R=R, fo=arg_fo, ext=arg_all, changed=changed_here))
        ext_rows.append(dict(seed=seed, J=w["J"], n_changed=changed, per_R=per_R,
                             n_ext_designs=sum(1 for o in ext_opts if (o.get("tag") or "").startswith(f"s5_{seed}"))))
    run["s5_extended"]["score"] = dict(rows=ext_rows,
                                       n_worlds_with_change=sum(1 for r in ext_rows if r["n_changed"]))
    run["finished_et"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    run["elapsed_s"] = time.time() - T0
    save_run(run)
    log(f"ALL sections flushed. elapsed={run['elapsed_s']:.1f}s rem={remaining():.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
