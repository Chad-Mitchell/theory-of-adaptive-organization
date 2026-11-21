#!/usr/bin/env python3
"""Fast identities for T27: detailed balance, equipartition on a quadratic,
qualification-band consistency, seed non-collision, lock hashes.

Run: python3 core/bridge_2026-11-21/math_checks.py
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(DIR))
from bridge_lib import (
    moran_fixation, exact_boltzmann, seed_collides, qualification_consistency,
    lattice_4_edges, tv_distance,
)


def check_landauer_units():
    """kT ln 2 per bit = kT per nat. Floor on κ is kT * update rate for I_mem in nats."""
    kT = 1.0
    per_bit = kT * math.log(2)
    per_nat = kT  # 1 nat = 1/ln(2) bits, so kT ln2 / ln2 = kT
    bits_per_nat = 1.0 / math.log(2)
    assert abs(per_bit * bits_per_nat - per_nat) < 1e-15
    # stakes ratio: first bit pays only if w * Δℓ > κ_floor * 1 bit
    # with κ_floor = (kT ln 2) * ν, i.e. ρ = (w Δℓ / ν) / kT and threshold ln 2.
    return True


def check_moran_detailed_balance():
    N = 201
    rng = np.random.default_rng(0)
    for _ in range(200):
        ri, rj = np.exp(rng.normal(0, 1, size=2))
        p_ij = moran_fixation(rj, ri, N)  # j invades i
        p_ji = moran_fixation(ri, rj, N)
        if p_ij <= 0 or p_ji <= 0:
            # extreme fitness ratios underflow one side to 0; identity holds in the limit
            continue
        ratio = p_ij / p_ji
        log_want = (N - 1) * (math.log(rj) - math.log(ri))
        err = abs(math.log(ratio) - log_want)
        assert err < 1e-8, (ri, rj, ratio, log_want, err)
    # equal fitness
    assert abs(moran_fixation(1.0, 1.0, N) - 1.0 / N) < 1e-15
    return True


def check_equipartition_quadratic():
    """Exact Boltzmann on a fine whitened quadratic should give β-excess ≈ 1
    (d=2) within a few percent, well inside the 20% official bar."""
    # J = (1/2)(y1^2 + y2^2) on linspace(-3.5, 3.5, 51)
    ys = np.linspace(-3.5, 3.5, 51)
    Y = np.array([(y1, y2) for y1 in ys for y2 in ys])
    J = 0.5 * np.sum(Y * Y, axis=1)
    for beta in (8.0, 10.0, 12.0):
        pi = exact_boltzmann(J, beta)
        excess = float(np.dot(pi, J) - J.min())
        bex = beta * excess
        assert abs(bex - 1.0) <= 0.05, (beta, bex)
    return True


def check_qualification_band():
    d = 2
    sigma, Ne = 0.1, 1000.0
    out = qualification_consistency(sigma, Ne, d, Jstar=1.0)
    assert abs(out["band_frac"] - 10.0 / (sigma * Ne)) < 1e-15
    assert abs(out["typical_frac"] - d / (2.0 * sigma * Ne)) < 1e-15
    assert abs(out["formula_typical_over_band"] - d / 20.0) < 1e-15
    assert abs(out["typical_over_band"] - d / 20.0) < 1e-12
    return True


def check_official_seeds_clean():
    base = 2026112100
    seeds = [base + i for i in range(16)]
    assert not any(seed_collides(s) for s in seeds)
    # published S5 / search seeds do collide
    assert seed_collides(1000)
    assert seed_collides(0)
    assert seed_collides(20261120)
    assert seed_collides(2026112020)
    return True


def check_lock_hashes():
    lock = (DIR / "LOCK.txt").read_text()
    for name in ("PREREG.md", "predictions.json"):
        digest = hashlib.sha256((DIR / name).read_bytes()).hexdigest()
        assert digest in lock, (name, digest)
    pred = hashlib.sha256((DIR / "predictions.json").read_bytes()).hexdigest()
    if (DIR / "PREDICTIONS.sha256").exists():
        assert (DIR / "PREDICTIONS.sha256").read_text().strip() == pred
    return True


def check_lattice_degrees():
    e = lattice_4_edges(51)
    assert len(e) == 51 * 50 * 2  # horizontal + vertical
    return True


def main():
    checks = [
        ("landauer_units", check_landauer_units),
        ("moran_detailed_balance", check_moran_detailed_balance),
        ("equipartition_quadratic", check_equipartition_quadratic),
        ("qualification_band", check_qualification_band),
        ("official_seeds_clean", check_official_seeds_clean),
        ("lock_hashes", check_lock_hashes),
        ("lattice_degrees", check_lattice_degrees),
    ]
    fails = []
    for name, fn in checks:
        try:
            fn()
            print(f"OK  {name}")
        except Exception as exc:
            print(f"FAIL  {name}: {exc}")
            fails.append(name)
    if fails:
        print("SOME FAILED")
        return 1
    print("ALL OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
