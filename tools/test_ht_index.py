"""theory/HT_INDEX.md: fast checks of N58 (ht vs n), N59 (Gaussian blindness) and the saved headline numbers (N60-N63)."""
import json, os, sys
import numpy as np
from scipy.stats import norm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "theory", "ht_checks")
sys.path.insert(0, D)
import htlib as H  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "theory", "layers_checks"))
from stores import E_K, E_inf, mse_given_b  # noqa: E402


def load(name):
    return json.load(open(os.path.join(D, name)))


def test_ht_definition_matches_jiang_ma_example():
    assert H.ht_index(1 / np.arange(1, 11)) == 3


def test_n58_pareto_fraction_and_log_n_growth():
    assert abs(H.p_pareto(2.0) - 0.25) < 1e-12 and abs(H.p_pareto(1e6) - np.exp(-1)) < 1e-6
    rng = np.random.default_rng(0)
    m = [np.mean([H.ht_index(rng.pareto(2.0, n) + 1) for _ in range(12)]) for n in (10**3, 10**5)]
    slope = (m[1] - m[0]) / 2
    assert abs(slope - np.log(10) / np.log(4)) < 0.45   # 1.66 per decade


def test_n58_gaussian_knife_edge():
    assert abs(2 * norm.sf(np.sqrt(2 / np.pi)) - 0.42494) < 1e-4
    rng = np.random.default_rng(1)
    assert H.ht_index(np.abs(rng.standard_normal(10**5))) == 1
    assert H.ht_index(np.abs(rng.standard_normal(10**5)), 0.5) > 8


def test_n59_ou_records_blind():
    rng = np.random.default_rng(2)
    for taus in ([10.0], [1.0, 10.0], [1.0, 10.0, 100.0]):
        y = H.ou_modes_fast(taus, np.ones(len(taus)) / len(taus), 50000, 0.1, rng).sum(0)
        assert H.ht_index(np.abs(np.diff(y))) == 1 and H.ht_index(np.abs(y - y.mean())) == 1


def test_whittle_counts_two_separated_modes():
    rng = np.random.default_rng(3)
    y = H.ou_modes_fast([1.0, 30.0], [0.5, 0.5], 60000, 0.1, rng).sum(0) + 0.3 * rng.standard_normal(60000)
    c, taus, K, _ = H.whittle_pole_count(y, 0.1, band=(0.1, 600), rng=rng)
    assert c == 2 and 0.5 < taus[0] < 2 and 15 < taus[1] < 60


def test_store_optimizer_never_below_causal_minimum():
    """Regression for the PR #116 review (S1): two stores sharing a rate made the store matrix singular, and E_K
    returned an MSE below the causal minimum E_inf (eps_4 = -1.1e-4 in this world before the fix)."""
    taus = np.array([1.2681414227381704, 1.432139253304822, 30.85142888049504, 244.23250352181506])
    v = np.array([0.2634443990937494, 0.7001043427184624, 8.585079742319136e-05, 0.03636540739036495]); N = 0.05004346949559107
    a = 1 / taus; ei = E_inf(a, v, N)
    e4, lb = E_K(a, v, N, 4, starts=8)
    assert e4 >= ei * (1 - 1e-6)
    assert abs(e4 - mse_given_b(a, v, np.exp(np.sort(lb)) * (1 + 1e-9 * np.arange(4)), N)[0]) < 1e-12   # value is the returned design's MSE
    b = np.array([0.5, 0.5 * (1 + 1e-9), 0.05])   # exactly-coincident pair = one store
    assert mse_given_b(a, v, b, N)[0] >= mse_given_b(a, v, np.array([0.5, 0.05]), N)[0] - 1e-9


def test_ht_v2_readings():
    assert H.ht_index_v2(1 / np.arange(1, 11)) == 3 and H.ht_index_v2(1 / np.arange(1, 11), reading="prefix") == 3
    x = np.abs(np.random.default_rng(4).standard_normal(10**5))
    assert H.ht_index_v2(x) == 1 and H.ht_index_v2(x, reading="prefix") > 8
    h2 = load("arm_H2.json")
    assert all(r["v2_stepwise"] == 1.0 for r in h2["halfnormal"]) and h2["halfnormal"][-1]["v2_prefix"] > 12


def test_mfdfa_width_does_not_vanish():
    m = load("arm_M.json")
    w = [r["width"] for r in m if r["n"] == 2000000 and len(r["taus"]) == 1]
    assert len(w) == 3 and min(w) > 0.05


def test_saved_headlines():
    s = load("summary.json")
    b = s["per_n"]["200000"]
    for e in ("ht_absdy_t05", "ht_per", "ht_cross"):
        assert all(v == 0.0 for v in b[e]["exact_kstar"].values())
    assert s["plugin_exact_kstar"]["10"] == 1.0 and s["plugin_exact_kstar"]["100"] == 1.0
    assert s["plugin_exact_kstar"]["1000"] > 0.9 and s["plugin_exact_kstar"]["1000000"] < 0.6
    assert s["plugin_n_records"] == 54 and s["plugin_negative_eps"] == 0
    assert s["kstar_distribution_n200k"]["10"] == {"1": 54}   # R = 10 is trivial
    bc, wh, pl = s["best_constant_exact_n200k"], s["whittle_as_kstar_exact_n200k"], s["plugin_exact_kstar"]
    assert pl["10000"] == wh["10000"] and pl["1000000"] == wh["1000000"] and pl["1000"] > wh["1000"]
    assert all(pl[R] >= bc[R] for R in ("100", "1000", "10000", "1000000"))
    assert 0.6 < b["whittle"]["spearman_J"] < 0.75
    # arm D (pilot): the withdrawn numbers are still what the file says, so the text's description of them is checkable
    d = load("arm_D.json")
    opt3 = [r for r in d["records"] if r["label"] == "opt_K3"]
    assert len({tuple(r["store_taus"]) for r in opt3}) == 1   # one design, four seeds (pseudo-replication)
    # arm D2 (redo): many worlds, read from data
    d2 = load("arm_D2.json"); R2 = d2["records"]
    opt = [r for r in R2 if r["label"].startswith("opt")]; rnd = [r for r in R2 if r["label"].startswith("rand")]
    assert len({tuple(r["world_taus"]) for r in R2}) == 12 and len(opt) == 72 and len(rnd) == 72
    assert sum(r["whittle_record"] == r["whittle_input"] for r in opt) == 67
    assert sum(r["io_count"] == r["K_agent"] for r in opt) == 56 and sum(r["io_count"] == r["K_agent"] for r in rnd) == 59
    di = [(r["interlaced_data"], r["interlaced_params"]) for r in R2 if r["interlaced_data"] is not None and r["K_agent"] == 3]
    assert len(di) == 15 and all(a == p for a, p in di)
    m3 = [m for m in d2["designs"] if m["K"] == 3]
    assert all(m["interlaced_params"] for m in m3 if m["kind"] == "opt")
    assert any(m["kind"] == "rand" and m["eps"] < 0.01 and not m["interlaced_params"] for m in m3)
    c = load("arm_C.json")
    right = sum(r["classify_then_merge"] == 3 for r in c if r["n_true_components"] == 3)
    assert right == 8 and all(r["sum_of_record_counts"] >= 12 for r in c)
