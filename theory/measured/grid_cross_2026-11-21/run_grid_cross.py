#!/usr/bin/env python3
"""GRID-CROSS runner (locked). Compute at nice 19.

Commands:
  lock-check   verify sha256 of PREREG.md, this file, and grid_cross_lib.py
  table        print the locked no-tie reference table (not an official gate)
  verdict      read Pass 1 / Pass 2 JSON and print the locked diagnostic verdict

This file does not download evaluation data. Official verdicts refuse to run
if LOCK.txt is missing or if a locked file's hash does not match.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from grid_cross_lib import (
    ALPHA, DIR, EFFECT_SIZE_BAR, LOCKED_FILES, N_MIN, NO_TIE_CRIT_RHO,
    diagnostic_verdict, robustness_tables, sha256_file, validate_score,
)

LOCK_PATH = DIR / "LOCK.txt"


def parse_lock(path: Path):
    """Read sha256 lines of the form '  sha256: <hex>' after a filename header."""
    if not path.is_file():
        raise SystemExit("LOCK.txt is missing; official commands refuse to run.")
    text = path.read_text()
    hashes = {}
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in LOCKED_FILES or stripped.endswith(".md") or stripped.endswith(".py"):
            # filename header (possibly with trailing spaces already stripped)
            name = stripped
            if name in LOCKED_FILES:
                current = name
            continue
        if stripped.startswith("sha256:") and current:
            hashes[current] = stripped.split(":", 1)[1].strip()
            current = None
    return hashes


def lock_check(strict=True):
    recorded = parse_lock(LOCK_PATH)
    ok = True
    lines = []
    for name in LOCKED_FILES:
        path = DIR / name
        actual = sha256_file(path)
        expected = recorded.get(name)
        match = expected is not None and actual == expected
        ok = ok and match
        lines.append(f"{name}: recorded={expected} actual={actual} match={match}")
    if strict and not ok:
        raise SystemExit("lock-check FAILED\n" + "\n".join(lines))
    print("lock-check PASS" if ok else "lock-check FAIL")
    print("\n".join(lines))
    return ok


def print_table():
    print("No-tie exact one-sided reference (informational; official p uses observed ties).")
    print(f"alpha={ALPHA}, effect-size bar rho <= {EFFECT_SIZE_BAR}, n_min={N_MIN}")
    print("n  rho_crit  (see PREREG.md §8)")
    for n, rho in NO_TIE_CRIT_RHO.items():
        print(f"{n}  {rho:.6f}")


def load_pairs(scores_path: Path, distances_path: Path):
    scores = json.loads(scores_path.read_text())
    distances = json.loads(distances_path.read_text())
    grids = scores.get("grids") or scores
    dist = distances.get("grids") or distances
    pairs = []
    errors = []
    names = sorted(set(list(grids) + list(dist)))
    for name in names:
        s = grids.get(name, {"status": "UNTESTED", "name": name})
        d = dist.get(name, {"d1_status": "UNTESTED", "d1": None})
        if s.get("status") not in (None, "UNTESTED"):
            errors.extend(f"{name}: {e}" for e in validate_score(s))
        pairs.append({
            "name": name,
            "S": s.get("S"),
            "status": s.get("status"),
            "S_is_lower_bound": bool(s.get("S_is_lower_bound")),
            "d1": d.get("d1"),
            "d1_status": d.get("d1_status", "UNTESTED"),
            "binding_ruin": bool(d.get("binding_ruin")),
        })
    if errors:
        raise SystemExit("score validation failed:\n" + "\n".join(errors))
    return pairs


def run_verdict(scores_path: Path, distances_path: Path):
    lock_check(strict=True)
    pairs = load_pairs(scores_path, distances_path)
    headline, official, loo, extremes, bounds, binding = robustness_tables(pairs)
    out = {
        "headline": headline,
        "official": official,
        "leave_one_out": loo,
        "untested_extremes": extremes,
        "lower_bound_sweep": bounds,
        "binding_ruin_sensitivity": binding,
    }
    print(json.dumps(out, indent=2, sort_keys=False, default=str))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="GRID-CROSS locked runner")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("lock-check")
    sub.add_parser("table")
    v = sub.add_parser("verdict")
    v.add_argument("--scores", type=Path, required=True)
    v.add_argument("--distances", type=Path, required=True)
    args = p.parse_args(argv)
    if args.cmd == "lock-check":
        lock_check(strict=True)
    elif args.cmd == "table":
        print_table()
    elif args.cmd == "verdict":
        run_verdict(args.scores, args.distances)
    else:
        raise SystemExit(f"unknown command {args.cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
