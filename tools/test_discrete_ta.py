"""Tests for tools/discrete_ta.py (run: python3 -m pytest -q tools/test_discrete_ta.py)."""
import json, math, os, subprocess, sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import discrete_ta as d

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MC = os.path.join(ROOT, "reviews", "night2", "DISCRETE_TA", "checks", "mc_discrete.json")


def riccati_iter(mu, lam, N, D):
    a = 2 * lam; phi = math.exp(-a * D); Q = mu * mu * (1 - phi * phi); R = N / D; P = mu * mu
    for _ in range(200000):
        M = phi * phi * P + Q; K = M / (M + R); Pn = (1 - K) * M
        if abs(Pn - P) < 1e-16 * P:
            break
        P = Pn
    return (1 - K) * phi


@pytest.mark.parametrize("lam,N,D", [(0.01, 1, 0.5), (0.05, 1, 2.0), (0.002, 9, 1), (0.3, 0.1, 3.0)])
def test_linear_closed_form_matches_riccati(lam, N, D):
    z = riccati_iter(1.0, lam, N, D)
    assert d.kalman_steady(1.0, lam, N, D)["pole"] == pytest.approx(z, rel=1e-10)
    assert d.linear_ta_grid(1.0, lam, N, D) == pytest.approx(-D / math.log(z), rel=1e-9)


def test_linear_continuous_limit_and_series():
    lam, N = 0.01, 1.0
    tc = d.linear_ta_cont(1.0, lam, N)
    assert d.linear_ta_grid(1.0, lam, N, 1e-4) == pytest.approx(tc, rel=1e-8)
    for D in (0.5, 2.0, 5.0):
        r = tc / D; a = 2 * lam
        series = 1 + (1 - (a * tc) ** 2) ** 2 / (24 * r * r)
        assert d.linear_ta_grid(1.0, lam, N, D) / tc == pytest.approx(series, abs=4e-3 / r ** 4)  # next term O(r^-4)


def test_continuous_exact_tends_to_plugin():
    for kap in (1e-4, 1e-6):
        for law in ("switch", "quiet"):
            assert d.bayes_ta_cont(1, kap, 1, law=law) == pytest.approx(d.bayes_ta_plugin(1, kap, 1), rel=2e-3)
    # the two pre-switch laws differ visibly at moderate kappa, in the stated direction
    assert d.bayes_ta_cont(1, 0.03, 1, law="quiet") > d.bayes_ta_cont(1, 0.03, 1, law="switch") * 1.02


def test_lattice_converged_in_h():
    a = d.bayes_ta_grid(1, 0.002, 9, 1, h=0.05)
    b = d.bayes_ta_grid(1, 0.002, 9, 1, h=0.025)
    assert a == pytest.approx(b, rel=1e-3)


def test_lattice_matches_independent_mc():
    mc = json.load(open(MC))
    picked = [e for e in mc["bayes"] if e["hold"] and e["Delta"] >= 0.2 and e["N"] <= 2.25]
    assert len(picked) >= 5
    for e in picked:
        g = d.bayes_ta_grid(e["mu"], e["lam"], e["N"], e["Delta"], start=None if e["law"] == "switch" else "quiet")
        assert abs(e["t_A"] - g) < 3.5 * e["se_t"], e


def test_small_grid_overshoot_constant():
    # (T_grid - T_cont)/sqrt(Delta theta) approaches C1 = 0.5826 (plus ~0.25 sqrt(rho))
    kap, D = 1e-4, 0.01
    tc = d.bayes_ta_cont(1, kap, 1, h=1e-3, law="quiet")
    g = (d.bayes_ta_grid(1, kap, 1, D, start="quiet") - tc) / math.sqrt(D)
    assert d.C1 == pytest.approx(0.58259716, abs=1e-6)
    assert g == pytest.approx(d.C1 + 0.25 * math.sqrt(D), abs=0.02)


def test_approximation_within_stated_band():
    for kap, D in ((1e-2, 0.2), (1e-3, 1.0), (1e-4, 0.05)):
        g = d.bayes_ta_grid(1, kap, 1, D, start="quiet")
        assert d.bayes_asymptotic(1, kap, 1, D, law="quiet") == pytest.approx(g, rel=0.012)


def test_start_ordering_and_referee_definition():
    # switch-time law < quiet law < noiseless resting point (AQN_REFEREE V8 values sit at the quiet law)
    s = d.bayes_ta_grid(1, 0.01, 9, 1)
    q = d.bayes_ta_grid(1, 0.01, 9, 1, start="quiet")
    r = d.bayes_ta_grid(1, 0.01, 9, 1, start="resting")
    assert s < q < r
    assert abs(q - 9.90) < 2.5 * 0.19     # referee: 9.90 +- 0.19 (sigma 3, lam 0.01)
    assert abs(s - 9.90) > 5 * 0.19


def test_cli_json():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "discrete_ta.py"), "linear", "--lam", "0.01",
                          "--N", "1", "--Delta", "0.5"], capture_output=True, text=True, check=True).stdout
    assert json.loads(out)["ratio"] > 1.0
