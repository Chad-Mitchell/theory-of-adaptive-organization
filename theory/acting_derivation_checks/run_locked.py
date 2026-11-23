#!/usr/bin/env python3
"""Carry out theory/acting_derivation_checks/PREREG.md. Do not change the protocol."""
from __future__ import annotations

import hashlib
import importlib.util
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "acting_derivation_checks_mod",
    ROOT / "theory" / "acting_derivation_checks" / "acting_derivation_checks.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
closed_rates = _mod.closed_rates

DT = 0.0002
T_BURN = 40.0
T_REC = 800.0
N_BURN = int(round(T_BURN / DT))
N_REC = int(round(T_REC / DT))
N = N_BURN + N_REC
GRID = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0)
B = GAMMA = C = D = DM = 1.0
SEED0 = 20261122


def trajectory(seed: int, K: float, cubic: bool):
    rng = np.random.Generator(np.random.PCG64(seed))
    z = rng.standard_normal(N * 2)
    x = 0.0
    m = 0.0
    bK = B * K
    sdx = (2.0 * D * DT) ** 0.5
    sdm = (2.0 * DM * DT) ** 0.5
    sum_x2 = 0.0
    sum_srx = 0.0
    sum_srm = 0.0
    for i in range(N):
        if cubic:
            fx = -(x + x * x * x + bK * m)
            dfx = -(1.0 + 3.0 * x * x)
        else:
            fx = -(x + bK * m)
            dfx = -1.0
        fm = -GAMMA * m + GAMMA * C * x
        dfm = -GAMMA
        if i >= N_BURN:
            sum_x2 += x * x
            sum_srx += fx * fx + D * dfx
            sum_srm += fm * fm + DM * dfm
        zx = z[2 * i]
        zm = z[2 * i + 1]
        x = x + fx * DT + sdx * zx
        m = m + fm * DT + sdm * zm
        if not np.isfinite(x) or not np.isfinite(m):
            raise FloatingPointError(f"non-finite state at step {i} K={K} cubic={cubic}")
    n = float(N_REC)
    sr_x = (sum_srx / n) / D
    sr_m = (sum_srm / n) / DM
    mean_x2 = sum_x2 / n
    return mean_x2, sr_x, sr_m


def argmin(values):
    best = 0
    for i, v in enumerate(values):
        if v < values[best] or (v == values[best] and GRID[i] < GRID[best]):
            best = i
    return best


def main():
    prereg = (ROOT / "theory" / "acting_derivation_checks" / "PREREG.md").read_bytes()
    digest = hashlib.sha256(prereg).hexdigest()
    lock = (ROOT / "theory" / "acting_derivation_checks" / "LOCK.txt").read_text()
    if digest not in lock:
        raise SystemExit("preregistration hash does not match LOCK.txt")
    t0 = time.time()
    print(f"N_BURN {N_BURN} N_REC {N_REC} sha256 {digest}")
    mx, sx, sm = trajectory(SEED0 + 0, 1.0, cubic=False)
    sr_hat = sx + sm
    sr_lg = sum(closed_rates(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)[:2])
    rel = abs(sr_hat - sr_lg) / abs(sr_lg)
    gate = rel <= 0.05
    print(f"GATE sr_hat {sr_hat:.12f} sr_lg {sr_lg:.12f} rel {rel:.6e} holds {gate}")
    je = []
    jh = []
    rows = []
    for index, K in enumerate(GRID):
        mean_x2, sr_x, sr_m = trajectory(SEED0 + index, K, cubic=True)
        e = mean_x2
        h = mean_x2 + sr_x + sr_m
        je.append(e)
        jh.append(h)
        rows.append((K, mean_x2, sr_x, sr_m, e, h))
        print(f"K {K:.2f} x2 {mean_x2:.12f} srX {sr_x:.12f} srM {sr_m:.12f} JE {e:.12f} JH {h:.12f}")
    i_e = argmin(je)
    i_h = argmin(jh)
    k_e = GRID[i_e]
    k_h = GRID[i_h]
    gap = k_e - k_h
    print(f"K_E {k_e:.2f} K_H {k_h:.2f} gap {gap:.2f}")
    if not gate:
        outcome = "measurement-puzzle"
    elif gap >= 0.25:
        outcome = "met"
    else:
        outcome = "miss"
    print(f"OUTCOME {outcome}")
    print(f"SECONDS {time.time() - t0:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
