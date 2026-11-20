"""theory/HT_INDEX.md: fast checks of N58 (ht vs n), N59 (Gaussian blindness) and the saved headline numbers (N60-N63)."""
import json, os, sys
import numpy as np
from scipy.stats import norm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "theory", "ht_checks")
sys.path.insert(0, D)
import htlib as H  # noqa: E402


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


def test_saved_headlines():
    s = load("summary.json")
    b = s["per_n"]["200000"]
    for e in ("ht_absdy_t05", "ht_per", "ht_cross"):
        assert all(v == 0.0 for v in b[e]["exact_kstar"].values())
    assert s["plugin_exact_kstar"]["10"] == 1.0 and s["plugin_exact_kstar"]["100"] == 1.0
    assert s["plugin_exact_kstar"]["1000"] > 0.9 and s["plugin_exact_kstar"]["1000000"] < 0.6
    assert 0.6 < b["whittle"]["spearman_J"] < 0.75
    d = load("arm_D.json")
    opt3 = [r for r in d["records"] if r["label"] == "opt_K3"]; rnd3 = [r for r in d["records"] if r["label"] == "rand_K3"]
    assert all(r["interlaced"] for r in opt3) and not any(r["interlaced"] for r in rnd3) and len(rnd3) == 9
    opt = [r for r in d["records"] if r["label"].startswith("opt")]
    assert all(r["whittle_record"] == 3 for r in opt)
    assert sum(r["io_count"] == r["K_agent"] for r in opt) == 11
    c = load("arm_C.json")
    right = sum(r["classify_then_merge"] == 3 for r in c if r["n_true_components"] == 3)
    assert right == 8 and all(r["sum_of_record_counts"] >= 12 for r in c)
