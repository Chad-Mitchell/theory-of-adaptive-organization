#!/usr/bin/env python3
"""Aggregate T1 and T2 setting labels under PREREG_2 §1 / PREREG_3.

Pure label logic: no search, no numpy. Used by run_t1_v2.py, run_t2_v2.py,
and test_prereg3_scripts.py. Also a command-line reader of the v2 .out files
after a Gate-passed run.
"""
from __future__ import annotations

import argparse
import json
import sys

# Highest first. hit and clean miss sit at the bottom, same level.
PRECEDENCE = (
    "measurement/code",
    "guard-hit",
    "not settled",
    "not run (budget)",
    "inside-resolution",
)

HIT = "hit"
CLEAN = "clean miss"
MIXED = "mixed"
BROKEN = 0.12  # single broken-edge threshold (PREREG_3 / B5)


def _base(label: str) -> str:
    if label.startswith("clean miss"):
        return CLEAN
    return label


def setting_label(flags: dict) -> str:
    """Emit the highest-precedence label from per-setting flags.

    flags may include any of:
      measurement_code, guard_hit, not_settled, not_run_budget,
      and 'classification' in {hit, clean miss, clean miss (no copying),
      inside-resolution}.
    """
    if flags.get("not_run_budget") or flags.get("not_run (budget)"):
        computed = {"not run (budget)"}
    else:
        computed = set()
    if flags.get("measurement_code") or flags.get("measurement/code"):
        computed.add("measurement/code")
    if flags.get("guard_hit") or flags.get("guard-hit"):
        computed.add("guard-hit")
    if flags.get("not_settled") or flags.get("not settled"):
        computed.add("not settled")
    if flags.get("not_run_budget") or flags.get("not_run (budget)"):
        computed.add("not run (budget)")
    classification = flags.get("classification")
    if classification:
        computed.add(_base(classification) if not str(classification).startswith("clean miss")
                     else "clean miss")
        # keep the more specific inside-resolution / hit as themselves
        if classification == "inside-resolution":
            computed.add("inside-resolution")
        elif classification == "hit":
            computed.add("hit")
        elif str(classification).startswith("clean miss"):
            computed.add("clean miss")
    for p in PRECEDENCE:
        if p in computed:
            return p
    if "hit" in computed and "clean miss" not in computed:
        return HIT
    if "clean miss" in computed and "hit" not in computed:
        return CLEAN
    if computed <= {"hit", "clean miss"} and computed:
        # shouldn't happen for a single setting
        return list(computed)[0]
    raise ValueError(f"could not assign a label from flags={flags!r}")


def aggregate_settings(labels) -> str:
    """Test-level label from five setting labels, PREREG_2 :38-42.

    A test is a hit only if all five settings are hits, and a clean miss only
    if all five are clean misses. Otherwise it takes the highest-precedence
    label present. When the five settings are some combination of hits and
    clean misses only, the test is mixed.
    """
    bases = [_base(l) for l in labels]
    if len(bases) != 5:
        raise ValueError(f"need five setting labels, got {len(bases)}")
    for p in PRECEDENCE:
        if p in bases:
            return p
    if all(b == HIT for b in bases):
        return HIT
    if all(b == CLEAN for b in bases):
        return CLEAN
    if set(bases) <= {HIT, CLEAN}:
        return MIXED
    raise ValueError(f"unrecognized setting labels: {labels!r}")


def tform(t1_label: str, leader_cs) -> str:
    """T-form: given a T1 hit, leader c < 0.10 at all five settings.

    No resolution band on the leader's c (PREREG_2 :19, restated in PREREG_3).
    Not applicable if T1 is not a hit.
    """
    if t1_label != HIT:
        return "not applicable"
    if len(leader_cs) != 5:
        raise ValueError("need five leader_c values")
    if any(c is None for c in leader_cs):
        return "miss"
    if all(c < 0.10 for c in leader_cs):
        return HIT
    return "miss"


def tacyclic(t2_label: str, circulation_flags) -> str:
    """T-acyclic: given a T2 hit, every setting is acyclic.

    Circulation at any setting is a miss. A setting with fewer than eight
    broken edges (A_e > 0.12) cannot be a circulation. Not applicable if T2
    is not a hit.
    """
    if t2_label != HIT:
        return "not applicable"
    if len(circulation_flags) != 5:
        raise ValueError("need five circulation flags")
    if any(circulation_flags):
        return "miss"
    return HIT


def is_circulation(Aes, orients, broken=BROKEN):
    """True iff all eight edges are broken (A_e > broken) and all signs agree."""
    if len(Aes) != 8 or len(orients) != 8:
        raise ValueError("need eight edges")
    vals = [0.0 if a is None else a for a in Aes]
    if not all(a > broken for a in vals):
        return False
    signs = [int(o) for o in orients]
    if any(s == 0 for s in signs):
        return False
    return all(s == signs[0] for s in signs)


def _parse_out(path):
    rows, total = [], None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("SETTING_JSON:"):
                rows.append(json.loads(line[len("SETTING_JSON:"):].strip()))
            elif line.startswith("TOTAL_JSON:"):
                total = json.loads(line[len("TOTAL_JSON:"):].strip())
    return rows, total


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("t1_out")
    p.add_argument("t2_out")
    args = p.parse_args(argv)
    t1_rows, t1_total = _parse_out(args.t1_out)
    t2_rows, t2_total = _parse_out(args.t2_out)
    t1_labels = [r["label"] for r in t1_rows]
    t2_labels = [r["label"] for r in t2_rows]
    t1 = aggregate_settings(t1_labels)
    t2 = aggregate_settings(t2_labels)
    form = tform(t1, [r.get("leader_c") for r in t1_rows])
    acyc = tacyclic(t2, [r.get("circulation", False) for r in t2_rows])
    out = {
        "T1": t1,
        "T2": t2,
        "T-form": form,
        "T-acyclic": acyc,
        "T1_settings": t1_labels,
        "T2_settings": t2_labels,
        "T1_cpu": None if t1_total is None else t1_total.get("total_cpu"),
        "T2_cpu": None if t2_total is None else t2_total.get("total_cpu"),
    }
    print(json.dumps(out, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
