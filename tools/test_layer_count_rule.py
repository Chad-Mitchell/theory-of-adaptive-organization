"""Tests for the layer-counting rule (OPEN_WORK T15; measurement/LAYER_COUNT_RULE.md).

Run: nice -n 19 python3 -m pytest -q tools/test_layer_count_rule.py
"""
import inspect, os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layer_count_rule as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _kernel(nr_taus, pair=None):
    return L._kernel_from_taus(nr_taus, pair)


def _noisy(f, rel, seed, t=None):
    t = L.T_GRID if t is None else t
    g = L.eval_fit(t, f)
    return t, g + np.random.default_rng(seed).normal(0, rel * np.abs(g).max(), len(g))


# --------------------------------------------------------------------------------------
# Prediction side (instant): exactness, hull identity, peaked worlds.
# --------------------------------------------------------------------------------------

def test_n60_equals_argmin_on_convex_sequence():
    eps = [1.0, 0.4, 0.15, 0.05, 0.0]
    assert L.is_convex(eps)
    for R in np.logspace(-2, 3, 250):
        p = L.predict_count(eps, R)
        assert p["method"] == "n60-from-0"
        assert p["K_star"] == p["K_argmin"] == p["K_hull"] == p["K_n60"]


def test_n60_from_zero_closes_the_k0_hole():
    eps = [1.0, 0.4, 0.15, 0.05, 0.0]
    # First decrement is 0.6; at R = 0.5, R*0.6 = 0.3 < 1, so K* = 0.
    assert L.argmin_J(eps, 0.5) == 0
    assert L.n60_from(eps, 0.5, 0) == 0
    assert L.n60_as_written(eps, 0.5) == 1   # the known hole


def test_hull_increment_is_an_identity():
    rng = np.random.default_rng(0)
    for _ in range(400):
        n = int(rng.integers(3, 12))
        eps = rng.uniform(0, 2, n)
        R = float(rng.uniform(0.1, 100))
        assert L.hull_increment(eps, R) == L.argmin_J(eps, R)


def test_peaked_world_uses_hull_not_adjacent_n60():
    """Draft PR #145 minimal example: W = (0,1,0), weights (2,1,1); decrements 1/3 then 2/3."""
    peaked = [1.0, 2.0 / 3.0, 0.0]
    assert not L.is_convex(peaked)
    p = L.predict_count(peaked, 3.0)
    assert p["method"] == "lower-convex-hull"
    assert p["K_argmin"] == p["K_hull"] == 2
    assert p["K_n60"] == 1
    assert p["K_star"] == 2


def test_l1_converse_distinct_ascent():
    """If a decrement later increases, the adjacent count differs from argmin on an open interval of R."""
    peaked = [1.0, 2.0 / 3.0, 0.0]          # d = (1/3, 2/3)
    misses = [R for R in np.linspace(1.1, 5.0, 80)
              if L.n60_from(peaked, R, 0) != L.argmin_J(peaked, R)]
    assert len(misses) > 10


def test_cost_band_contains_argmin_and_near_ties():
    J = {0: 2.0, 1: 1.0, 2: 1.005, 3: 1.2}
    assert L.cost_band(J, 0.01) == [1, 2]
    assert L.in_cost_band(1.005, 1.0, 0.01)
    assert not L.in_cost_band(1.2, 1.0, 0.01)


def test_prediction_never_calls_the_fitter():
    # predict_count / hull / n60 take only a sequence and R
    assert set(inspect.signature(L.predict_count).parameters) == {"eps", "R", "tol"}
    src = inspect.getsource(L.predict_count) + inspect.getsource(L.hull_increment) + inspect.getsource(L.n60_from)
    assert "detect" not in src and "fit_degree" not in src


# --------------------------------------------------------------------------------------
# Observation helpers that do not fit a record (instant).
# --------------------------------------------------------------------------------------

def test_merge_close_reals_by_resolution_factor():
    st = [dict(kind="real", degree=1, tau=10.0, period=None),
          dict(kind="real", degree=1, tau=15.0, period=None),
          dict(kind="real", degree=1, tau=80.0, period=None)]
    m = L.merge_close_states(st, factor=3.0)
    # 15/10 = 1.5 < 3, 80/sqrt(10*15) > 3
    assert len(m) == 2
    assert {round(s["tau"], 5) for s in m} == {round(np.sqrt(10 * 15), 5), 80.0}
    assert sum(s["degree"] for s in m) == 2


def test_merge_does_not_mix_a_rhythm_with_a_real_pole():
    st = [dict(kind="real", degree=1, tau=10.0, period=None),
          dict(kind="pair", degree=2, tau=12.0, period=20.0)]
    m = L.merge_close_states(st, factor=3.0)
    assert len(m) == 2
    assert sum(s["degree"] for s in m) == 3


def test_classify_local_versus_shared():
    local = dict(kind="real", degree=1, tau=5.0, period=None)
    shared = dict(kind="real", degree=1, tau=40.0, period=None)
    units = [[dict(local)], [dict(local)]]          # each isolated unit has only the fast pole
    pooled = [dict(local), dict(shared)]
    c = L.classify_local_shared(units, pooled, factor=3.0)
    assert {s["tau"]: s["class"] for s in c} == {5.0: "local", 40.0: "shared"}


def test_relay_class_is_layer_iff_an_in_band_pole_moves():
    store = dict(kind="real", degree=1, tau=20.0, period=None)
    # Replace a relay with a pure delay: in-band poles unchanged.
    assert L.relay_class([store], [store], factor=3.0) == "relay"
    # Bypass a store: the in-band pole disappears.
    assert L.relay_class([store], [], factor=3.0) == "layer"
    roles, meta = L.relay_test([store], [store], factor=3.0)
    assert meta["classification"] == "relay" and roles[0]["role"] == "layer"
    roles, meta = L.relay_test([store], [], factor=3.0)
    assert meta["classification"] == "layer" and roles[0]["role"] == "layer"


def test_step1_never_sees_prices_or_argmin():
    params = set(inspect.signature(L.detect).parameters)
    assert params == {"t", "y", "band", "k_max", "seed", "merge_factor"}
    params = set(inspect.signature(L.count_layers).parameters)
    assert not params & {"K_star", "J_by_K", "kstar", "argmin", "eps_K", "R"}


# --------------------------------------------------------------------------------------
# Observation on synthetic kernels (a few fits; keep the grid short).
# --------------------------------------------------------------------------------------

def test_counts_well_separated_real_states():
    f = _kernel([(2.0, 1.0), (25.0, 0.8), (80.0, 0.6)])
    t, y = _noisy(f, 1e-3, 1)
    assert L.detect(t, y, L.BAND, k_max=4)["K_det"] == 3


def test_rhythm_counts_two_by_degree():
    f = _kernel([(80.0, 0.7)], pair=(8.0, 12.0, 1.0))
    t, y = _noisy(f, 1e-3, 2)
    d = L.detect(t, y, L.BAND, k_max=4)
    assert d["K_det"] == 3
    assert sum(s["kind"] == "pair" for s in d["states_merged"]) == 1


def test_out_of_band_pole_not_counted():
    f = _kernel([(0.3, 1.0), (30.0, 1.0)])       # tau = 0.3 is below the band's lower edge (1.0)
    t, y = _noisy(f, 1e-3, 3)
    assert L.detect(t, y, L.BAND, k_max=4)["K_det"] == 1


def test_close_states_are_merged_not_overcounted():
    """Known failure mode (Istratov & Vyvenko 1999): close time constants are not
    distinct under the resolution factor.  Ratio 1.5 < 3, so the merge counts one."""
    f = _kernel([(10.0, 1.0), (15.0, 1.0)])
    t, y = _noisy(f, 3e-2, 4)
    assert L.detect(t, y, L.BAND, k_max=4)["K_det"] == 1


def test_mse_kernel_matches_closed_form():
    sys.path.insert(0, os.path.join(ROOT, "theory", "layers_checks"))
    import stores
    a = np.array([0.2, 0.005]); v = np.array([1.0, 1.0]); N = 5.0
    b = np.array([1 / 38.0, 1 / 2.9])
    m, g = stores.mse_given_b(a, v, b, N)
    assert abs(L.mse_kernel(L.kernel_from_stores(b, g), a, v, N) - m) < 1e-3 * m


@pytest.fixture(scope="module")
def taut():
    return L.run_tautology(eps=0.01)


def test_rule_can_disagree_with_argmin(taut):
    """The observation recovers the system's degree, not K*.  Under- and over-built
    designs sit outside the cost band; a design at the two-store minimum sits inside.
    """
    rows = {(r["name"], r["h"]): r for r in taut}
    assert rows[("underbuilt", 0.01)]["in_band"] is False
    assert rows[("overbuilt", 0.01)]["in_band"] is False
    assert rows[("overbuilt", 0.1)]["in_band"] is False
    assert rows[("at_K2", 0.01)]["in_band"] is True
    for r in taut:
        assert r["K_obs"] == r["K_true"]
