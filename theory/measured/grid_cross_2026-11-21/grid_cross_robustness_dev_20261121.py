"""GRID-CROSS dated deviation helper (21 November 2026).

Not a locked file. PREREG.md, run_grid_cross.py, and grid_cross_lib.py are
unchanged. This module implements the UNTESTED-fill robustness sweep as
written in the locked PREREG §8: assign every UNTESTED grid a single common
fill d in {0, max observed complete d}.

The locked library fills with {min, max} of the complete d values. That
procedure is not the governing rule (see DEVIATIONS_2026-11-21.md, D2).
Official Pass 2 UNTESTED-fill robustness uses this module. Leave-one-out,
lower-bound 0/8, and BINDING-RUIN sensitivity remain those of the locked
library; only the fill set and the resulting headline are recomputed here.
"""
from __future__ import annotations

from grid_cross_lib import N_MIN, diagnostic_verdict, robustness_tables


def untested_extreme_fills(pairs):
    """PREREG §8 fill: every UNTESTED grid gets one common d in {0, max}."""
    complete_d = [
        p["d1"]
        for p in pairs
        if p.get("d1_status") in ("ok", "ok_multimode") and p["d1"] is not None
    ]
    extremes = []
    if not complete_d:
        return extremes
    fills = []
    for fill in (0, max(complete_d)):
        if fill not in fills:
            fills.append(fill)
    untested = [
        p
        for p in pairs
        if p.get("d1_status") not in ("ok", "ok_multimode") or p.get("d1") is None
    ]
    if not untested:
        return extremes
    for fill in fills:
        filled = []
        for p in pairs:
            q = dict(p)
            if q.get("d1_status") not in ("ok", "ok_multimode") or q.get("d1") is None:
                q = dict(q)
                q["d1"] = fill
                q["d1_status"] = "ok"
                q["filled_for_robustness"] = True
            filled.append(q)
        v = diagnostic_verdict(filled)
        extremes.append(
            {"fill_d": fill, "verdict": v["verdict"], "n": v["n"], "rho": v["rho"]}
        )
    return extremes


def robustness_tables_prereg(pairs):
    """Locked robustness tables, with the governing {0, max} UNTESTED fill.

    Returns (headline, official, loo, extremes, bounds, binding_note),
    the same layout as grid_cross_lib.robustness_tables.
    """
    _locked_headline, official, loo, _locked_ext, bounds, binding_note = (
        robustness_tables(pairs)
    )
    extremes = untested_extreme_fills(pairs)
    headline = official["verdict"]
    scored_labels = {"PASS on diagnostic", "FAIL on diagnostic", "NEITHER"}
    if headline in scored_labels:
        swept = [row["verdict"] for row in loo + extremes + bounds]
        if binding_note["n"] >= N_MIN:
            swept.append(binding_note["verdict"])
        if any(
            v != headline and v in scored_labels | {"NOT APPLICABLE"}
            for v in swept
        ):
            headline = "INCONCLUSIVE"
    return headline, official, loo, extremes, bounds, binding_note
