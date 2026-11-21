"""GRID-CROSS locked library: Spearman test, d1 rule, and diagnostic verdict.

Official gates are those in PREREG.md §8. This module must not be edited after
LOCK.txt is written (T27 standing rule), except for a typo that does not change
a criterion, which would itself be a dated deviation.
"""
from __future__ import annotations

import hashlib
import itertools
import math
import random
from pathlib import Path

# Locked constants (PREREG.md §8).
N_MIN = 5
ALPHA = 0.10
RHO_BAR = -0.50
N_EXACT_MAX = 10
N_MC = 100_000
MC_SEED = 20261121137
EFFECT_SIZE_BAR = RHO_BAR

# Mid-rank Spearman, no-tie exact one-sided reference (informational; official
# p is always the permutation test on the observed values, including ties).
NO_TIE_CRIT_RHO = {
    5: -0.800000,
    6: -0.657143,
    7: -0.571429,
    8: -0.523810,
    9: -0.466667,
}

GAMMA_LO = 1.7
GAMMA_HI = 2.3

SCORE_COMPONENTS = ("S_mkt", "S_pen", "S_rel", "S_own")
SCORE_VALUES = (0, 1, 2)

DIR = Path(__file__).resolve().parent
REPO_ROOT = DIR.parents[2]
LOCKED_FILES = ("PREREG.md", "run_grid_cross.py", "grid_cross_lib.py")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def midranks(values):
    """1-based midranks; ties take the average of their ordinal positions."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman_rho(xs, ys):
    """Mid-rank Spearman correlation. Returns 0.0 if a rank variance is zero."""
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("spearman_rho needs two series of equal length >= 2")
    rx, ry = midranks(list(xs)), midranks(list(ys))
    n = len(rx)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(
        sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)
    )
    return 0.0 if den == 0.0 else num / den


def permutation_p(s_vals, d_vals, observed_rho, direction="le", n_mc=N_MC, seed=MC_SEED):
    """Share of permutations of d against fixed S with rho on the named side.

    direction 'le' is the predicted side (rho <= observed); 'ge' is the opposite.
    Exact enumeration if n <= N_EXACT_MAX; otherwise n_mc draws with the locked seed.
    """
    s_vals = list(s_vals)
    d_vals = list(d_vals)
    n = len(s_vals)
    if n != len(d_vals):
        raise ValueError("S and d must have the same length")
    if n < 2:
        return {"p": None, "n_perm": 0, "method": "undefined"}

    def count_and_total(iterable, total):
        hits = 0
        for perm in iterable:
            r = spearman_rho(s_vals, perm)
            if direction == "le" and r <= observed_rho + 1e-12:
                hits += 1
            elif direction == "ge" and r >= observed_rho - 1e-12:
                hits += 1
        return hits, total

    if n <= N_EXACT_MAX:
        hits, total = count_and_total(itertools.permutations(d_vals), math.factorial(n))
        method = "exact"
    else:
        rng = random.Random(seed)
        def draws():
            for _ in range(n_mc):
                perm = list(d_vals)
                rng.shuffle(perm)
                yield perm
        hits, total = count_and_total(draws(), n_mc)
        method = "monte_carlo"
    return {"p": hits / total, "n_perm": total, "n_hits": hits, "method": method}


def validate_score(entry):
    """Check a Pass 1 score dict. Returns a list of error strings (empty = ok)."""
    errors = []
    status = entry.get("status")
    if status == "UNTESTED":
        return errors
    if status not in ("scored", "scored_lower_bound"):
        errors.append(f"bad status {status!r}")
        return errors
    for k in SCORE_COMPONENTS:
        if k not in entry:
            errors.append(f"missing {k}")
            continue
        if entry[k] not in SCORE_VALUES:
            errors.append(f"{k}={entry[k]!r} not in {{0,1,2}}")
        miss = entry.get(f"{k}_status")
        if miss not in (None, "ok", "MISSING"):
            errors.append(f"bad {k}_status {miss!r}")
    if "S" in entry:
        expected = sum(entry[k] for k in SCORE_COMPONENTS if k in entry)
        if entry["S"] != expected:
            errors.append(f"S={entry['S']} != sum of components {expected}")
    missing = [
        k for k in SCORE_COMPONENTS
        if entry.get(f"{k}_status") == "MISSING"
    ]
    lower = entry.get("S_is_lower_bound", False)
    if missing and not lower and status != "scored_lower_bound":
        errors.append("MISSING component but S not flagged as a lower bound")
    if (lower or status == "scored_lower_bound") and not missing:
        errors.append("lower-bound flag set but no component is MISSING")
    return errors


def d1_from_spectrum(k_obs, gamma=None, n_separated_modes=None, spectrum_available=False,
                     is_power_law=False, is_single_mode=False):
    """Apply the locked d1 rule. Returns (d1 or None, tag).

    tag is one of: 'ok', 'UNTESTED', 'ok_multimode'.
    """
    if not spectrum_available:
        return None, "UNTESTED"
    if k_obs is None or k_obs < 0:
        return None, "UNTESTED"
    if is_power_law and gamma is not None and GAMMA_LO <= gamma <= GAMMA_HI:
        return max(0, int(k_obs) - 1), "ok"
    if is_single_mode:
        return max(0, int(k_obs) - 1), "ok"
    if n_separated_modes is not None and n_separated_modes >= 0:
        return max(0, int(k_obs) - int(n_separated_modes)), "ok_multimode"
    return None, "UNTESTED"


def is_complete_pair(score_entry, distance_entry):
    """A complete official pair: integer S that is not a lower bound, and a scored d1."""
    if score_entry.get("status") not in ("scored",):
        return False
    if score_entry.get("S_is_lower_bound"):
        return False
    if any(score_entry.get(f"{k}_status") == "MISSING" for k in SCORE_COMPONENTS):
        return False
    if distance_entry.get("d1_status") not in ("ok", "ok_multimode"):
        return False
    if distance_entry.get("d1") is None:
        return False
    return True


def diagnostic_verdict(pairs, include_lower_bounds=False):
    """Compute the locked diagnostic verdict.

    pairs: iterable of dicts with keys
      name, S, S_is_lower_bound, d1, d1_status, binding_ruin (bool)
    Only complete pairs enter the official n, unless include_lower_bounds is True
    (used in the robustness sweep, not as the official n).
    """
    official = []
    untested = []
    lower = []
    for p in pairs:
        if p.get("d1_status") not in ("ok", "ok_multimode") or p.get("d1") is None:
            untested.append(p)
            continue
        if p.get("S_is_lower_bound") or p.get("status") == "scored_lower_bound":
            lower.append(p)
            if include_lower_bounds:
                official.append(p)
            continue
        official.append(p)

    result = {
        "n": len(official),
        "rho": None,
        "p_neg": None,
        "p_pos": None,
        "method": None,
        "verdict": "UNTESTED",
        "reason": "",
        "names": [p["name"] for p in official],
    }

    if len(official) < N_MIN:
        result["reason"] = f"n={len(official)} < n_min={N_MIN}"
        result["verdict"] = "UNTESTED"
        return result

    s_vals = [p["S"] for p in official]
    d_vals = [p["d1"] for p in official]
    if len(set(s_vals)) == 1:
        result["rho"] = spearman_rho(s_vals, d_vals)
        result["verdict"] = "NOT APPLICABLE"
        result["reason"] = "no variation in S among complete pairs"
        return result

    rho = spearman_rho(s_vals, d_vals)
    p_neg = permutation_p(s_vals, d_vals, rho, direction="le")
    p_pos = permutation_p(s_vals, d_vals, rho, direction="ge")
    result["rho"] = rho
    result["p_neg"] = p_neg["p"]
    result["p_pos"] = p_pos["p"]
    result["method"] = p_neg["method"]
    result["n_perm"] = p_neg["n_perm"]

    if rho <= EFFECT_SIZE_BAR and p_neg["p"] <= ALPHA:
        label = "PASS on diagnostic"
    elif rho > 0 and p_pos["p"] <= ALPHA:
        label = "FAIL on diagnostic"
    else:
        label = "NEITHER"
    result["verdict"] = label
    result["reason"] = (
        f"rho={rho:.6f}, p_neg={p_neg['p']:.6f}, p_pos={p_pos['p']:.6f}"
    )
    return result


def robustness_tables(pairs):
    """Leave-one-out, UNTESTED extreme-d, and lower-bound 0/8 sweeps.

    Returns (headline_if_changed, official, loo, extremes, bounds, binding).
    Headline becomes INCONCLUSIVE if any sweep changes PASS/FAIL/NEITHER.
    UNTESTED and NOT APPLICABLE are not flipped to a scored label by a sweep
    that merely drops below n_min; the official UNTESTED stands, and a
    BINDING-RUIN drop below n_min is reported as UNTESTED on that sensitivity.
    """
    official = diagnostic_verdict(pairs)
    base = official["verdict"]
    scored_labels = {"PASS on diagnostic", "FAIL on diagnostic", "NEITHER"}

    loo = []
    for i, p in enumerate(pairs):
        sub = [q for j, q in enumerate(pairs) if j != i]
        v = diagnostic_verdict(sub)
        loo.append({"dropped": p.get("name"), "verdict": v["verdict"], "n": v["n"],
                    "rho": v["rho"]})

    complete_d = [
        p["d1"] for p in pairs
        if p.get("d1_status") in ("ok", "ok_multimode") and p["d1"] is not None
    ]
    extremes = []
    if complete_d:
        d_lo, d_hi = min(complete_d), max(complete_d)
        untested = [p for p in pairs if p.get("d1_status") not in ("ok", "ok_multimode")
                    or p.get("d1") is None]
        if untested:
            for fill in (d_lo, d_hi):
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
                extremes.append({"fill_d": fill, "verdict": v["verdict"], "n": v["n"],
                                 "rho": v["rho"]})

    bounds = []
    lower = [p for p in pairs if p.get("S_is_lower_bound") or p.get("status") == "scored_lower_bound"]
    if lower:
        for repl in (0, 8):
            filled = []
            for p in pairs:
                q = dict(p)
                if q.get("S_is_lower_bound") or q.get("status") == "scored_lower_bound":
                    q = dict(q)
                    q["S"] = repl
                    q["S_is_lower_bound"] = False
                    q["status"] = "scored"
                filled.append(q)
            v = diagnostic_verdict(filled)
            bounds.append({"S_fill": repl, "verdict": v["verdict"], "n": v["n"],
                           "rho": v["rho"]})

    binding_pairs = [p for p in pairs if not p.get("binding_ruin")]
    binding = diagnostic_verdict(binding_pairs)
    binding_note = {
        "n": binding["n"],
        "verdict": binding["verdict"],
        "rho": binding["rho"],
        "dropped": [p["name"] for p in pairs if p.get("binding_ruin")],
    }

    headline = base
    if base in scored_labels:
        swept = [row["verdict"] for row in loo + extremes + bounds]
        if binding["n"] >= N_MIN:
            swept.append(binding["verdict"])
        if any(v != base and v in scored_labels | {"NOT APPLICABLE"} for v in swept):
            headline = "INCONCLUSIVE"
        if binding["n"] < N_MIN and any(p.get("binding_ruin") for p in pairs):
            # Official n may still be >= 5; the sensitivity is UNTESTED. If the
            # official label is a scored one, the headline becomes INCONCLUSIVE
            # only when the sensitivity is required to confirm it; the prereg
            # says: if the sensitivity leaves n < 5, the diagnostic is UNTESTED
            # on that sensitivity; if it leaves n >= 5 and changes the label,
            # the headline is INCONCLUSIVE. Official headline stays `base`
            # with the sensitivity reported, unless we treat n<5 drop as
            # changing a scored label. The prereg: "if that leaves n < 5, the
            # diagnostic is UNTESTED on the sensitivity (and the headline
            # follows §8)." Official n still governs the headline; the
            # sensitivity is reported. No extra flip here for n<5.
            pass
    return headline, official, loo, extremes, bounds, binding_note
