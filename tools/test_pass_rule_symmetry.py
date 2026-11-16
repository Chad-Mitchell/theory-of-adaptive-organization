"""Tests for tools/pass_rule_symmetry.py (run: python3 -m pytest -q tools/test_pass_rule_symmetry.py).

Report-only: these check the symmetry helpers and the locked-number re-reads.
They do not write RESULTS, THEORY, CLAIM_MAP or FRAMEWORK."""
import os, sys, math
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pass_rule_symmetry as prs


def test_causal_aklmt_exp1_flips_under_mirror():
    # tests/LAB_AKLMT_TAU/results.json: D 0.5182, sigma 0.0479, P 0.9835, kappa 1/2
    D, s, P = 0.5182, 0.0479, 0.9835
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=False) == "PASS"
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=True) == "INCONCLUSIVE"
    assert D - 1.96 * s == pytest.approx(0.424316, abs=1e-6)
    assert 0.424316 < 0.5 * P < D + 1.96 * s


def test_causal_aklmt_exp3_flips_under_mirror():
    D, s, P = 0.6287, 0.0941, 1.0274
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=False) == "PASS"
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=True) == "INCONCLUSIVE"


def test_causal_null_invariance_stays_passed():
    # lo = 0.290 - 1.96*0.029 = 0.23216 > kill 0.1752
    D, s, P = 0.290, 0.029, 0.3504
    assert D - 1.96 * s == pytest.approx(0.23316, abs=1e-5)
    assert D - 1.96 * s > 0.5 * P
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=False) == "PASS"
    assert prs.verdict_causal(D, s, P=P, kappa=0.5, mirror=True) == "PASS"
    # seven-replicate mean
    assert prs.verdict_causal(0.347, 0.012, P=P, kappa=0.5, mirror=True) == "PASS"


def test_stakes_shift_stays_inconclusive_either_rule():
    D, s, eps = -0.08792916573905762, 0.3424861359294935, 0.05
    assert prs.verdict_causal(D, s, eps=eps, mirror=False) == "INCONCLUSIVE"
    assert prs.verdict_causal(D, s, eps=eps, mirror=True) == "INCONCLUSIVE"


def test_learnsim_ra_and_aa_flip_under_tost():
    # PREREG_2 RA: point inside the 15% band, CI is not
    ra = dict(est=-0.7355540919210248, lo=-1.031065704554559, hi=-0.5199174767590031,
              pred=-0.7585444318425878)
    assert prs.verdict_relband(**ra, frac=0.15, tost=False) == "PASS"
    assert prs.verdict_relband(**ra, frac=0.15, tost=True) == "INCONCLUSIVE"
    aa = dict(est=-1.537602253555922, lo=-1.7703836968844853, hi=-1.3306722843507006,
              pred=-1.6496890003007756)
    assert prs.verdict_relband(**aa, frac=0.15, tost=False) == "PASS"
    assert prs.verdict_relband(**aa, frac=0.15, tost=True) == "INCONCLUSIVE"


def test_onset_secondary_stays_pass_under_tost():
    a15 = dict(est=-0.9501980267829581, lo=-1.052915459447678, hi=-0.8740302093693711,
               pred=-0.9623862581091926)
    assert prs.verdict_relband(**a15, frac=0.15, tost=False) == "PASS"
    assert prs.verdict_relband(**a15, frac=0.15, tost=True) == "PASS"


def test_learnsim_V_rr_rrh_flip_under_tost():
    rr = dict(est=1.0107526319204174, lo=0.8516088834885466, hi=1.1996362446914173)
    assert prs.verdict_ratio_band(**rr, m=1.15, tost=False) == "PASS"
    assert prs.verdict_ratio_band(**rr, m=1.15, tost=True) == "INCONCLUSIVE"
    rrh = dict(est=1.0576372239306957, lo=0.8895232809367087, hi=1.257523576297964)
    assert prs.verdict_ratio_band(**rrh, m=1.15, tost=False) == "PASS"
    assert prs.verdict_ratio_band(**rrh, m=1.15, tost=True) == "INCONCLUSIVE"


def test_onset_primary_stays_pass_under_either_fail_rule():
    est, lo, hi = 0.012893782836077339, -0.07218679356393873, 0.11795570737280624
    pred, delta = -0.0002076717006254114, 0.267
    assert prs.verdict_onset(est, lo, hi, pred, delta, tost_fail=False) == "PASS"
    assert prs.verdict_onset(est, lo, hi, pred, delta, tost_fail=True) == "PASS"


def test_kernel_primary_stays_pass():
    # RESULTS.md: D -0.017, sigma_D 0.049, W21 0.260 ± 0.041; rivals 0, 0.012, 0.725
    assert prs.verdict_kernel(-0.017, 0.049, 0.260, 0.041) == "PASS"
    # free-noise sensitivity was INCONCLUSIVE (sigma_D 0.072, D -0.059)
    assert prs.verdict_kernel(-0.059, 0.072, 0.260, 0.041) == "INCONCLUSIVE"


def test_eiv_already_symmetric_stays_pass():
    # r_night -0.202 [-0.325, -0.079] vs midpoint -0.483
    assert prs.verdict_midpoint(-0.325, -0.079, -0.483) == "PASS"


def test_banks_sign_hit_would_not_clear_a_0_2_floor():
    assert prs.verdict_hit_floor(0.20, 0.11, 0.29, 0.2, mirror=False) == "HIT"
    assert prs.verdict_hit_floor(0.20, 0.11, 0.29, 0.2, mirror=True) == "INCONCLUSIVE"


def test_self_p2_inconclusive_both_ways():
    # 0.30 [-0.01, 0.60]: contains 0.5, does not exclude 0
    assert prs.verdict_includes_pred(-0.01, 0.60, 0.5, also_exclude=0.0) == "INCONCLUSIVE"


def test_analytic_mirror_at_mv10_minimum():
    # Φ((1-kappa)SNR - z) = Φ(0.5*5.6 - 1.96) = Φ(0.84) ≈ 0.7995
    p = prs.analytic_causal_pass(1.0, 5.6, kappa=0.5, mirror=True)
    assert p == pytest.approx(0.7995, abs=5e-4)
    # wrong-pass at r=0.40, SNR 9.7: Φ((0.40-0.5)*9.7 - 1.96) = Φ(-2.93) ≈ 0.0017
    assert prs.analytic_causal_pass(0.40, 9.7, kappa=0.5, mirror=True) < 0.01
    # R0 at the same point is large: thresh = max(1.96/9.7, 0.5-1.96/9.7)=max(0.202, 0.298)=0.298
    # Φ((0.40-0.298)*9.7) = Φ(0.989) ≈ 0.84
    assert prs.analytic_causal_pass(0.40, 9.7, kappa=0.5, mirror=False) == pytest.approx(0.839, abs=0.02)


def test_reread_table_recomputes_and_flags_flips():
    rows = prs.reread_all()
    by = {r["id"]: r for r in rows}
    assert by["LAB-AKLMT-TAU Exp 1"]["recomputed_locked"] == "PASS"
    assert by["LAB-AKLMT-TAU Exp 1"]["under_mirror"] == "INCONCLUSIVE"
    assert by["CAUSAL-NULL-INVARIANCE (author)"]["under_mirror"] == "PASS"
    assert by["LEARNSIM PREREG_2 RA"]["recomputed_locked"] == "PASS"
    assert by["LEARNSIM PREREG_2 RA"]["under_mirror"] == "INCONCLUSIVE"
    assert by["LEARNSIM V RR"]["under_mirror"] == "INCONCLUSIVE"
    assert by["ONSET-ACROSS-ALPHA primary Δ"]["under_mirror"] == "PASS"
    assert by["KERNEL-MEASURE primary"]["under_mirror"] == "PASS"
    assert by["STAKES-REFEREE R-EIV night"]["under_mirror"] == "PASS"
