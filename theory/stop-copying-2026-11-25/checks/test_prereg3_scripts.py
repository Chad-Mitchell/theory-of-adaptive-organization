"""Unit tests for the PREREG_3 v2 scripts. No T1/T2 search, no --execute, no minimize()."""
from __future__ import annotations

import os
import sys

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import aggregate as agg
import run_t2_v2 as t2


# --- B1: settled check -------------------------------------------------------

def _uniform_plus_noise(seed, scale=1e-7, w=10, wx=1):
    c = t2.C_SYM[(w, wx)]
    x = t2.pack(np.full(8, 5.0), np.full(8, c), np.full(8, c))
    rng = np.random.default_rng(seed)
    return x + np.r_[np.zeros(8), rng.normal(0, scale, 16)]


def test_uniform_ring_plus_1e7_noise_counts_as_settled():
    """The v2 probe case: reciprocal designs with 1e-7 c-noise must count as settled."""
    recs = []
    for seed in (0, 1, 2):
        Aes, orients, ev = t2.edge_A(_uniform_plus_noise(seed))
        assert max(0.0 if a is None else a for a in Aes) < 1e-5
        recs.append((Aes, orients))
    assert t2.pairwise_settled(recs)
    assert t2.dihedral_match(recs[0][0], recs[0][1], recs[1][0], recs[1][1])
    assert t2.dihedral_match(recs[1][0], recs[1][1], recs[2][0], recs[2][1])
    assert t2.dihedral_match(recs[0][0], recs[0][1], recs[2][0], recs[2][1])


def test_pairwise_settled_requires_every_pair_not_just_the_first():
    """Three A_e patterns: 0 matches 1 and 0 matches 2, but 1 does not match 2."""
    # Within 0.01 of a reference, but 0.02 apart from each other, no dihedral helps.
    # packed[0] sits between the other two, so a "compare to the first" check
    # would pass, but the outer pair is 0.02 apart.
    A0 = [0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    A1 = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    A2 = [0.02, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    o = [0] * 8
    assert t2.dihedral_match(A0, o, A1, o)
    assert t2.dihedral_match(A0, o, A2, o)
    assert not t2.dihedral_match(A1, o, A2, o)
    assert not t2.pairwise_settled([(A0, o), (A1, o), (A2, o)])


def test_orientations_ignored_below_threshold_compared_above():
    # Both A_e <= 0.02: orientations may disagree.
    Aa = [0.02] * 8
    Ab = [0.02] * 8
    oa, ob = [1] * 8, [-1] * 8
    assert t2.dihedral_match(Aa, oa, Ab, ob)
    # Both A_e > 0.02: a single sign flip is not a dihedral image of a circulation.
    Aa = [0.20] * 8
    Ab = [0.20] * 8
    assert not t2.dihedral_match(Aa, [1] * 8, Ab, [1] * 7 + [-1])
    # A circulation and its reverse (reflection) do match.
    assert t2.dihedral_match(Aa, [1] * 8, Ab, [-1] * 8)


# --- B3: relative window -----------------------------------------------------

def test_relative_tolerance_is_one_e_minus_6_times_abs_best():
    assert t2.close_to_best(0.0715 + 7.0e-8, 0.0715)
    assert not t2.close_to_best(0.0715 + 1e-6, 0.0715)
    assert t2.close_to_best(2.7517 + 2.75e-6, 2.7517)
    assert not t2.close_to_best(2.7517 + 3e-6, 2.7517)


# --- B5 / T-acyclic circulation ---------------------------------------------

def test_broken_threshold_is_0_12_everywhere():
    assert agg.BROKEN == 0.12
    assert t2.BROKEN == 0.12
    Aes = [0.12] * 8
    orients = [1] * 8
    # A_e == 0.12 is not strictly above the threshold.
    assert not agg.is_circulation(Aes, orients)
    Aes = [0.1201] * 8
    assert agg.is_circulation(Aes, orients)
    # One edge only 0.10: not a circulation under the locked threshold.
    Aes = [0.20] * 7 + [0.10]
    assert not agg.is_circulation(Aes, orients)


# --- B2 / B6: aggregation ----------------------------------------------------

def test_setting_label_precedence():
    # measurement/code beats guard-hit, not settled, and a hit classification.
    assert agg.setting_label({"measurement_code": True, "guard_hit": True,
                              "not_settled": True, "classification": "hit"}) == "measurement/code"
    assert agg.setting_label({"guard_hit": True, "not_settled": True,
                              "classification": "hit"}) == "guard-hit"
    assert agg.setting_label({"not_settled": True, "classification": "clean miss"}) == "not settled"
    assert agg.setting_label({"not_run_budget": True}) == "not run (budget)"
    assert agg.setting_label({"classification": "inside-resolution"}) == "inside-resolution"
    assert agg.setting_label({"classification": "hit"}) == "hit"
    assert agg.setting_label({"classification": "clean miss (no copying)"}) == "clean miss"


def test_aggregate_settings_all_hit_or_all_clean_or_mixed():
    assert agg.aggregate_settings(["hit"] * 5) == "hit"
    assert agg.aggregate_settings(["clean miss"] * 5) == "clean miss"
    assert agg.aggregate_settings(["clean miss (no copying)"] * 5) == "clean miss"
    assert agg.aggregate_settings(["hit", "hit", "clean miss", "hit", "hit"]) == "mixed"
    assert agg.aggregate_settings(["hit", "clean miss", "clean miss", "clean miss", "clean miss"]) == "mixed"


def test_aggregate_settings_highest_precedence_wins():
    assert agg.aggregate_settings(["hit", "hit", "measurement/code", "hit", "hit"]) == "measurement/code"
    assert agg.aggregate_settings(["clean miss", "guard-hit", "not settled", "hit", "hit"]) == "guard-hit"
    assert agg.aggregate_settings(["clean miss"] * 4 + ["not settled"]) == "not settled"
    assert agg.aggregate_settings(["hit"] * 4 + ["not run (budget)"]) == "not run (budget)"
    assert agg.aggregate_settings(["clean miss"] * 4 + ["inside-resolution"]) == "inside-resolution"


def test_tform_all_five_and_not_applicable():
    assert agg.tform("clean miss", [0.0] * 5) == "not applicable"
    assert agg.tform("hit", [0.0, 0.05, 0.09, 0.02, 0.01]) == "hit"
    assert agg.tform("hit", [0.0, 0.05, 0.10, 0.02, 0.01]) == "miss"  # c >= 0.10 at any setting
    assert agg.tform("hit", [0.0, 0.05, 0.20, 0.02, 0.01]) == "miss"
    # No resolution band: c = 0.099 is a hit, c = 0.10 is a miss.
    assert agg.tform("hit", [0.099] * 5) == "hit"
    assert agg.tform("hit", [0.10] * 5) == "miss"


def test_tacyclic_given_t2_hit():
    assert agg.tacyclic("clean miss", [False] * 5) == "not applicable"
    assert agg.tacyclic("hit", [False] * 5) == "hit"
    assert agg.tacyclic("hit", [False, False, True, False, False]) == "miss"
    assert agg.tacyclic("hit", [True] * 5) == "miss"
