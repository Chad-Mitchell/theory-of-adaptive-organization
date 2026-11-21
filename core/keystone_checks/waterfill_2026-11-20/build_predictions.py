#!/usr/bin/env python3
"""Write WF-HSV predictions for all fresh worlds, BEFORE any E_K run."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wf_rule import predict
from worlds import all_worlds, restore_av, sanity_worlds, R_GRID_S, R_GRID_R, model_s_world

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def avN_of(w):
    if w.get("cls") == "model_s" or w["id"].startswith("sane_") or w["id"].startswith("ms_"):
        a = np.asarray(w["a"], float)
        v = np.asarray(w["v"], float)
        return a, v, float(w["N"])
    return restore_av(w)


def predict_world(w, R_grid):
    a, v, N = avN_of(w)
    # one ARE per world; R only changes the threshold
    base = predict(a, v, N, R_grid[0])
    rows = []
    for R in R_grid:
        if base["status"] != "OK":
            rec = dict(R=float(R), status=base["status"], K_star=None, reason=base.get("reason"))
        else:
            delta = np.asarray(base["delta"], float)
            rec = dict(R=float(R), status="OK", K_star=int(np.sum(float(R) * delta > 1.0)))
        rows.append(rec)
    world_out = {k: w[k] for k in w if k not in ("_a", "_v")}
    # drop bulky intermediate if any
    world_out.update(
        status=base["status"],
        reason=base.get("reason"),
        n=base.get("n"),
        var_s=base.get("var_s"),
        E_inf_ARE=base.get("E_inf_ARE"),
        delta=base.get("delta"),
        gamma=base.get("gamma"),
        sigma=base.get("sigma"),
        sum_gamma=base.get("sum_gamma"),
        target_h2=base.get("target_h2"),
        observer_poles=base.get("observer_poles"),  # diagnostic only, not scored
        Pi_minus_P_residual=base.get("Pi_minus_P_residual"),
        consistency_note=base.get("consistency_note"),
        per_R=rows,
    )
    return world_out


def main():
    t0 = time.time()
    ms, rh, mx = all_worlds()
    # collision / id checks
    ids = [w["id"] for w in ms + rh + mx]
    assert len(ids) == len(set(ids)) == 64
    assert all(w["id"] == f"ms_{i:04d}" for i, w in enumerate(ms))
    # sanity predictions (implementation check already passed; recorded)
    sane = []
    for w in sanity_worlds():
        a, v, N = w["a"][0], w["v"][0], w["N"]
        P = N * (np.sqrt(a * a + 2 * a * v / N) - a)
        Rstar = P / (v - P)
        grid = [0.2, 1.0, float(Rstar + 1)]
        rec = predict_world({**w, "cls": "sanity", "a": [a], "v": [v], "N": N}, grid)
        rec["Rstar"] = float(Rstar)
        rec["P"] = float(P)
        sane.append(rec)

    pred_ms = [predict_world(w, R_GRID_S) for w in ms]
    pred_rh = [predict_world(w, R_GRID_R) for w in rh]
    pred_mx = [predict_world(w, R_GRID_R) for w in mx]

    n_indet = sum(1 for w in pred_ms + pred_rh + pred_mx if w["status"] != "OK")
    payload = dict(
        locked_note=(
            "WF-HSV predictions from poles, variances, N, R only, plus the unique "
            "full-order Kalman-Bucy ARE and innovations-form Gramians. Written "
            "before any reduced-order E_K optimisation on these worlds. "
            "Observer poles are diagnostic and are not scored. The rule predicts "
            "a count K*, not process-band placement."
        ),
        prereg_sha256=sha256(ROOT / "PREREG.md"),
        math_sha256=sha256(ROOT / "MATH.md"),
        wf_rule_sha256=sha256(HERE / "wf_rule.py"),
        worlds_sha256=sha256(HERE / "worlds.py"),
        R_GRID_S=list(R_GRID_S),
        R_GRID_R=list(R_GRID_R),
        n_model_s=len(pred_ms),
        n_rhythm=len(pred_rh),
        n_mixed=len(pred_mx),
        n_indeterminate_worlds=n_indet,
        sanity=sane,
        model_s=pred_ms,
        rhythm=pred_rh,
        mixed=pred_mx,
        elapsed=time.time() - t0,
    )
    out = HERE / "wf_predictions.json"
    out.write_text(json.dumps(payload, indent=1))
    digest = sha256(out)
    (HERE / "PREDICTIONS.sha256").write_text(digest + "  wf_predictions.json\n")
    print(f"wrote {out}  sha256 {digest}")
    print(f"worlds: ms={len(pred_ms)} rh={len(pred_rh)} mx={len(pred_mx)}  indeterminate={n_indet}  elapsed={payload['elapsed']:.2f}s")
    print(f"prereg sha256 {payload['prereg_sha256']}")
    # print a few K* paths
    for w in pred_ms[:2] + pred_rh[:2] + pred_mx[:1]:
        ks = [r["K_star"] for r in w["per_R"]]
        print(f"  {w['id']} status={w['status']} K* path unique={sorted(set(k for k in ks if k is not None))} n={w.get('n')}")


if __name__ == "__main__":
    main()
