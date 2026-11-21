"""GRID-CROSS: locked gates, permutation p-values, and verdict rules."""
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GC = ROOT / "theory/measured/grid_cross_2026-11-21"
sys.path.insert(0, str(GC))

from grid_cross_lib import (  # noqa: E402
    ALPHA, EFFECT_SIZE_BAR, N_MIN, NO_TIE_CRIT_RHO, d1_from_spectrum,
    diagnostic_verdict, midranks, permutation_p, robustness_tables,
    spearman_rho, validate_score,
)
from grid_cross_robustness_dev_20261121 import (  # noqa: E402
    robustness_tables_prereg,
)


def test_prereg_states_locked_bars_and_is_not_a_rescore():
    text = (GC / "PREREG.md").read_text()
    assert "new prereg, not a re-score" in text
    assert "P25 stays **UNTESTED**" in text
    assert "ρ ≤ −0.5" in text or "rho <= -0.5" in text or "ρ ≤ −0.5" in text
    assert "n < 5" in text or "n_min = 5" in text or "n ≥ 5" in text
    assert "NOT A TEST" in text
    assert "hash-lock" in text.lower() or "hash-locked" in text.lower()
    assert "closed-loop" in text.lower()
    assert "MISSING" in text and "lower bound" in text
    # No status label may use the word "law".
    for line in text.splitlines():
        if "headline" in line.lower() and "law" in line.lower():
            assert "not a test" in line.lower() or "not used" in line.lower()


def test_reachability_log_does_not_invent_annual_aemo_series():
    text = (GC / "DATA_SOURCES_REACHABILITY.md").read_text()
    assert "not included" in text.lower() or "**not included**" in text.lower()
    assert "403" in text
    assert "data.fingrid.fi/files/339" in text
    assert "Schedule of reliability settings" in text or "reliability settings" in text
    assert "DS3-SS-Protocol-v4.1-October-2024.pdf" in text
    # Independent-review S6 addendum (post-lock; not a d1 rescue).
    assert "nemweb.com.au/Reports/Current" in text
    assert "data.fingrid.fi/en/datasets/397" in text
    assert "ACE open loop" in text
    assert "www.ercot.com/mp/data-products" in text
    assert "not a missed ready d1 series" in text or "not a missed ready d1" in text


def test_midrank_spearman_known_values():
    # Distinct increasing ranks: rho = 1; reversed: rho = -1.
    assert abs(spearman_rho([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) - 1.0) < 1e-12
    assert abs(spearman_rho([1, 2, 3, 4, 5], [50, 40, 30, 20, 10]) + 1.0) < 1e-12
    # Ties: midranks of [1,1,2] are 1.5, 1.5, 3.
    assert midranks([1, 1, 2]) == [1.5, 1.5, 3.0]
    # Zero variance in ranks.
    assert spearman_rho([1, 1, 1], [3, 2, 1]) == 0.0


def _enumerate_no_tie_critical(n):
    """Max attainable no-tie Spearman rho with exact one-sided p <= ALPHA.

    Enumerates all n! assignments of distinct ranks 1..n. One-sided p at a
    value rho is (# permutations with mid-rank Spearman <= rho) / n!.
    Returns (rho_crit, p_crit, n_hits_crit, rho_next, p_next, n_hits_next).
    """
    s = list(range(1, n + 1))
    nfac = math.factorial(n)
    # Round to 12 decimals so identical algebraic values group together.
    counts = {}
    for perm in itertools.permutations(s):
        rho = round(spearman_rho(s, list(perm)), 12)
        counts[rho] = counts.get(rho, 0) + 1
    cum = 0
    crit = None
    nxt = None
    for rho in sorted(counts):
        cum += counts[rho]
        p = cum / nfac
        if p <= ALPHA:
            crit = (rho, p, cum)
        elif nxt is None:
            nxt = (rho, p, cum)
            break
    assert crit is not None and nxt is not None
    return crit + nxt


def test_no_tie_critical_values_match_locked_table():
    # Exact enumeration, not a lookup of the locked constant. This is the
    # check that would have failed on the n=9 typo (review S1).
    expected = {
        5: (-0.800000, 8, 120, -0.700000, 14),
        6: (-0.657143, 63, 720, -0.600000, 87),
        7: (-0.571429, 504, 5040, -0.535714, 594),
        8: (-0.523810, 3964, 40320, -0.500000, 4358),
        9: (-0.483333, 35163, 362880, -0.466667, 38560),
    }
    for n, (rho_c, hits_c, nfac, rho_n, hits_n) in expected.items():
        crit_rho, crit_p, crit_hits, next_rho, next_p, next_hits = (
            _enumerate_no_tie_critical(n)
        )
        assert crit_hits == hits_c
        assert next_hits == hits_n
        assert abs(crit_rho - rho_c) < 5e-7
        assert abs(next_rho - rho_n) < 5e-7
        assert abs(crit_p - hits_c / nfac) < 1e-15
        assert abs(next_p - hits_n / nfac) < 1e-15
        assert crit_p <= ALPHA < next_p

    # Locked informational table is correct at n=5-8 and wrong at n=9.
    assert abs(NO_TIE_CRIT_RHO[5] + 0.800000) < 1e-9
    assert abs(NO_TIE_CRIT_RHO[6] + 0.657143) < 5e-7
    assert abs(NO_TIE_CRIT_RHO[7] + 0.571429) < 5e-7
    assert abs(NO_TIE_CRIT_RHO[8] + 0.523810) < 5e-7
    # The typo: locked constant stores the next (non-critical) rho, -0.466667,
    # whose exact p is 38560/362880 = 0.106261, above alpha. The official
    # permutation p is computed by permutation_p, not by this table, and is
    # unchanged (D1 in DEVIATIONS_2026-11-21.md).
    assert abs(NO_TIE_CRIT_RHO[9] + 0.466667) < 5e-7
    assert abs(NO_TIE_CRIT_RHO[9] + 0.483333) > 1e-4
    s = list(range(1, 10))
    # A representative permutation is not required here; official p on a
    # fully anti-aligned pair uses the locked exact enumerator.
    pval = permutation_p(s, list(reversed(s)), spearman_rho(s, list(reversed(s))), direction="le")
    assert pval["method"] == "exact"
    assert pval["n_perm"] == 362880
    assert pval["n_hits"] == 1
    assert abs(pval["p"] - 1 / 362880) < 1e-18


def test_d1_rule():
    d, tag = d1_from_spectrum(4, gamma=2.09, spectrum_available=True, is_power_law=True)
    assert (d, tag) == (3, "ok")
    d, tag = d1_from_spectrum(4, spectrum_available=False)
    assert (d, tag) == (None, "UNTESTED")
    d, tag = d1_from_spectrum(4, gamma=1.2, spectrum_available=True, is_power_law=True)
    assert tag == "UNTESTED"  # power law outside [1.7, 2.3] and no mode count
    d, tag = d1_from_spectrum(4, n_separated_modes=2, spectrum_available=True)
    assert (d, tag) == (2, "ok_multimode")
    d, tag = d1_from_spectrum(1, spectrum_available=True, is_single_mode=True)
    assert (d, tag) == (0, "ok")


def test_score_validation_lower_bound_rule():
    ok = {
        "status": "scored",
        "S_mkt": 1, "S_pen": 1, "S_rel": 2, "S_own": 1,
        "S": 5,
        "S_mkt_status": "ok", "S_pen_status": "ok",
        "S_rel_status": "ok", "S_own_status": "ok",
        "S_is_lower_bound": False,
    }
    assert validate_score(ok) == []
    missing_not_flagged = dict(ok)
    missing_not_flagged["S_pen_status"] = "MISSING"
    assert validate_score(missing_not_flagged)
    flagged = dict(ok)
    flagged["status"] = "scored_lower_bound"
    flagged["S_pen_status"] = "MISSING"
    flagged["S_is_lower_bound"] = True
    flagged["S_pen"] = 0
    flagged["S"] = 4
    assert validate_score(flagged) == []


def _pair(name, S, d1, lower=False, untested=False, binding=False):
    return {
        "name": name,
        "S": S,
        "status": "scored_lower_bound" if lower else "scored",
        "S_is_lower_bound": lower,
        "d1": None if untested else d1,
        "d1_status": "UNTESTED" if untested else "ok",
        "binding_ruin": binding,
    }


def test_verdict_untested_when_n_lt_5():
    pairs = [_pair("GB", 5, 3, binding=True)]
    v = diagnostic_verdict(pairs)
    assert v["verdict"] == "UNTESTED"
    assert v["n"] == 1


def test_verdict_not_applicable_when_s_flat():
    pairs = [_pair(f"g{i}", 1, i) for i in range(5)]
    v = diagnostic_verdict(pairs)
    assert v["verdict"] == "NOT APPLICABLE"
    assert v["n"] == 5


def test_verdict_pass_on_strong_negative():
    # n=5, S = 1..5, d = 5..1, rho = -1, p = 1/120, effect size holds.
    pairs = [_pair(f"g{s}", s, 6 - s) for s in range(1, 6)]
    v = diagnostic_verdict(pairs)
    assert v["n"] == 5
    assert abs(v["rho"] + 1.0) < 1e-12
    assert v["p_neg"] == 1 / 120
    assert v["verdict"] == "PASS on diagnostic"


def test_verdict_fail_on_strong_positive():
    pairs = [_pair(f"g{s}", s, s) for s in range(1, 6)]
    v = diagnostic_verdict(pairs)
    assert abs(v["rho"] - 1.0) < 1e-12
    assert v["p_pos"] == 1 / 120
    assert v["verdict"] == "FAIL on diagnostic"


def test_verdict_neither_when_effect_size_misses():
    # rho = -0.3, p_neg = 0.342: negative but misses both locked bars.
    pairs = [
        _pair("a", 1, 5),
        _pair("b", 2, 1),
        _pair("c", 3, 4),
        _pair("d", 4, 2),
        _pair("e", 5, 3),
    ]
    v = diagnostic_verdict(pairs)
    assert v["n"] == 5
    assert abs(v["rho"] + 0.3) < 1e-9
    assert v["verdict"] == "NEITHER"


def test_lower_bound_scores_are_not_official_complete():
    pairs = [_pair(f"g{s}", s, 6 - s) for s in range(1, 5)]
    pairs.append(_pair("lb", 1, 0, lower=True))
    v = diagnostic_verdict(pairs)
    assert v["n"] == 4
    assert v["verdict"] == "UNTESTED"


def test_robustness_inconclusive_when_leave_one_out_flips():
    # n=6 is the smallest n at which leave-one-out can change a scored label.
    # Five perfectly anti-aligned grids (S=1..5, d=5..1) would PASS on their
    # own (rho=-1, p=1/120). A sixth complete concordant point (S=6, d=6)
    # makes the official six-point verdict NEITHER; dropping that sixth
    # point flips the scored label to PASS, so the headline is INCONCLUSIVE.
    pairs = [_pair(f"g{s}", s, 6 - s) for s in range(1, 6)]
    pairs.append(_pair("x", 6, 6))
    headline, official, loo, extremes, bounds, binding = robustness_tables(pairs)
    assert official["n"] == 6
    assert official["verdict"] == "NEITHER"
    dropped_x = [row for row in loo if row["dropped"] == "x"]
    assert len(dropped_x) == 1
    assert dropped_x[0]["n"] == 5
    assert dropped_x[0]["verdict"] == "PASS on diagnostic"
    assert abs(dropped_x[0]["rho"] + 1.0) < 1e-12
    assert headline == "INCONCLUSIVE"


def test_robustness_fill_zero_vs_min_can_disagree():
    # Review S2: when every complete d1 is >= 1, {0, max} and {min, max}
    # can disagree. Five anti-aligned complete pairs with d in {2..6}
    # plus an UNTESTED grid at S=2: official is PASS. Locked {min, max}
    # fills (2 and 6) both stay PASS, so the locked headline stays PASS.
    # The governing {0, max} fill is INCONCLUSIVE, because fill d=0 is NEITHER.
    pairs = [_pair(f"g{s}", s, 7 - s) for s in range(1, 6)]  # d=6,5,4,3,2
    pairs.append(_pair("U", 2, None, untested=True))
    locked_h, locked_off, _loo, locked_ext, _b, _bind = robustness_tables(pairs)
    gov_h, gov_off, _loo2, gov_ext, _b2, _bind2 = robustness_tables_prereg(pairs)
    assert locked_off["verdict"] == gov_off["verdict"] == "PASS on diagnostic"
    assert {row["fill_d"] for row in locked_ext} == {2, 6}
    assert all(row["verdict"] == "PASS on diagnostic" for row in locked_ext)
    assert locked_h == "PASS on diagnostic"
    assert {row["fill_d"] for row in gov_ext} == {0, 6}
    fill0 = [row for row in gov_ext if row["fill_d"] == 0]
    assert len(fill0) == 1
    assert fill0[0]["verdict"] == "NEITHER"
    assert gov_h == "INCONCLUSIVE"


def test_deviation_helper_hash_is_recorded():
    dev = (GC / "grid_cross_robustness_dev_20261121.py").read_bytes()
    digest = hashlib.sha256(dev).hexdigest()
    note = (GC / "DEVIATIONS_2026-11-21.md").read_text()
    assert digest in note
    assert "f189de0e6d53deb42ab9c850c7e9a37e1f25e136bbb455d7981349e4c3f01a57" == digest
    # Locked files still match LOCK.txt (this PR must not edit them).
    lock = (GC / "LOCK.txt").read_text()
    for name in ("PREREG.md", "run_grid_cross.py", "grid_cross_lib.py"):
        assert hashlib.sha256((GC / name).read_bytes()).hexdigest() in lock


def test_n_min_and_alpha_constants():
    assert N_MIN == 5
    assert ALPHA == 0.10
    assert EFFECT_SIZE_BAR == -0.50


def test_lock_hashes_match_and_runner_agrees():
    import hashlib
    import subprocess
    import sys
    lock = (GC / "LOCK.txt").read_text()
    assert "01:55:05 AM EST" in lock or "1:55:05 AM EST" in lock
    assert "America/New_York" in lock
    assert "54a4562" in lock
    for name in ("PREREG.md", "run_grid_cross.py", "grid_cross_lib.py"):
        digest = hashlib.sha256((GC / name).read_bytes()).hexdigest()
        assert f"{name}" in lock
        assert digest in lock
    proc = subprocess.run(
        [sys.executable, str(GC / "run_grid_cross.py"), "lock-check"],
        cwd=str(GC), check=True, capture_output=True, text=True,
    )
    assert "lock-check PASS" in proc.stdout
