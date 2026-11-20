"""The face map (figures/face_map.py): its decision rule, closed forms, invariance, and placements, checked independently.
Run: nice -n 19 python3 -m pytest -q tools/test_face_map.py      (about a minute)"""
import os, sys, json, re
import numpy as np
import pytest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures'); sys.path.insert(0, FIG)
import face_map as fm
from face_hybrid import mse, mse_fast, best_fast

RNG = np.random.default_rng(20261120)

def brute(XL, XS, nu, kL, kS):
    """Independent argmin of the four costs, written from the definitions (units of h_l, one unit's stake = XL*h_l/G_L etc.)."""
    # costs relative to NONE, per n*h_l: local saves XL and pays 1; shared saves XS/nu and pays 1/nu; both saves XL + kS*XS/nu and pays 1 + 1/nu
    c = [0.0, 1 - XL, (1 - XS) / nu, 1 + 1 / nu - XL - kS * XS / nu]
    return int(np.argmin(np.array(c) - np.array([3, 2, 1, 0]) * 1e-12))

def test_decide_matches_definitions():
    for _ in range(20000):
        XL, XS = 10 ** RNG.uniform(-3, 3, 2); nu = 10 ** RNG.uniform(-3, 3); kL, kS = RNG.uniform(0, 1, 2)
        assert fm.decide(XL, XS, nu, kL, kS) == brute(XL, XS, nu, kL, kS)

def test_quadrant_edges_are_universal():
    """Outside the upper-right quadrant no number other than (X_L, X_S) changes the design: the edges are invariant."""
    for _ in range(4000):
        XL, XS = 10 ** RNG.uniform(-3, 3, 2)
        q = int(fm.quadrant(XL, XS))
        ds = {int(fm.decide(XL, XS, 10 ** RNG.uniform(-4, 4), *RNG.uniform(0, 1, 2))) for _ in range(30)}
        if q < 3: assert ds == {q}
        else: assert ds <= {1, 2, 3}

def test_both_iff_kappa_condition():
    """In the upper-right quadrant: both beats local iff kS*XS > 1 and beats shared iff kL*XL > 1, given kL defined consistently."""
    for _ in range(5000):
        GL, GS = RNG.uniform(0.05, 1, 2); GB = RNG.uniform(max(GL, GS), GL + GS); wu, hl, hc, n = 10 ** RNG.uniform(0, 3), 1.0, 10 ** RNG.uniform(-1, 2), int(10 ** RNG.uniform(0, 3))
        XL, XS, nu = wu * GL / hl, n * wu * GS / hc, n * hl / hc; kL, kS = (GB - GS) / GL, (GB - GL) / GS
        if XL <= 1 or XS <= 1: continue
        V = fm.values(XL, XS, nu, kL, kS)
        assert np.isclose(V[3] - V[1], (kS * XS - 1) / nu); assert np.isclose(V[3] - V[2], kL * XL - 1)

def test_mse_fast_equals_lyapunov():
    for _ in range(40):
        J = RNG.integers(1, 3); a = 10 ** RNG.uniform(-1, 1, J); v = RNG.uniform(0.1, 1, J)
        N, n, rho, lead = 10 ** RNG.uniform(-2, 1), int(RNG.integers(1, 50)), RNG.uniform(0, 1), 10 ** RNG.uniform(-2, 0.5)
        bl = 10 ** RNG.uniform(-1, 1.5, RNG.integers(0, 3)); bc = 10 ** RNG.uniform(-1, 1.5, RNG.integers(0, 3))
        x, y = mse(a, v, N, n, rho, lead, bl, bc), mse_fast(a, v, N, n, rho, lead, bl, bc)
        assert abs(x - y) <= 1e-9 * max(1.0, abs(x))

@pytest.mark.parametrize('seed', range(12))
def test_closed_forms_vs_numeric(seed):
    r = np.random.default_rng(seed); a, v = 10 ** r.uniform(-1, 1), r.uniform(0.2, 2)
    N, n, rho, lead = 10 ** r.uniform(-2, 1), int(r.integers(2, 200)), r.uniform(0, 1), 10 ** r.uniform(-3, 0)
    GL, GS, pi = fm.gains_ou(v, a, N, n, rho, lead)
    eL = best_fast([a], [v], N, n, rho, lead, 1, 0, starts=3)[0]; eS = best_fast([a], [v], N, n, rho, lead, 0, 1, starts=3)[0]
    assert abs((v - eL) - GL) < 1e-7 * v; assert abs((v - eS) - GS) < 1e-6 * v

def test_limits():
    v, a, N = 1.3, 0.7, 0.2
    GL, GS, pi = fm.gains_ou(v, a, N, 1, 0.4, 0.0)
    assert np.isclose(pi, 1.0) and np.isclose(GS, GL)                       # n = 1: nothing to pool, a shared layer is a local one
    GL, GS, pi = fm.gains_ou(v, a, 1e-12, 50, 0.3, 0.0)
    assert np.isclose(GL, v, rtol=1e-4) and np.isclose(pi, 0.3 + 0.7 / 50, rtol=1e-3)   # clean reads: pooling gain = shared share only
    GL, GS1, _ = fm.gains_ou(v, a, N, 10, 1.0, 0.0); _, GS2, _ = fm.gains_ou(v, a, N, 10, 1.0, 1.5)
    assert np.isclose(GS2 / GS1, np.exp(-2 * a * 1.5))                    # delay enters only as exp(-2 l / tau)
    assert np.isclose(fm.P_ou(v, a, N), N * a * (np.sqrt(1 + 2 * v / (N * a)) - 1))
    # single scale, rho = 1: X_S = nu * pi * exp(-2 l/tau) * X_L exactly
    n, hl, hc, wu, l = 20, 1.0, 4.0, 30.0, 0.3; GL, GS, pi = fm.gains_ou(v, a, N, n, 1.0, l)
    assert np.isclose(n * wu * GS / hc, (n * hl / hc) * pi * np.exp(-2 * a * l) * (wu * GL / hl))

def test_subadditive_and_kappa_range():
    """kappa in [0, 1] needs G_B <= G_L + G_S (verified numerically, not proved) and G_B >= max(G_L, G_S)."""
    for s in range(15):
        r = np.random.default_rng(100 + s); a, v = 1.0, 1.0
        N, n, rho, lead = 10 ** r.uniform(-2, 1), int(r.integers(2, 300)), r.uniform(0, 1), 10 ** r.uniform(-3, 0.5)
        GL, GS, _ = fm.gains_ou(v, a, N, n, rho, lead); GB = v - best_fast([a], [v], N, n, rho, lead, 1, 1, starts=3, seed=s)[0]
        assert GB >= max(GL, GS) - 1e-8 and GB <= GL + GS + 1e-8

def test_spend_never_falls_with_stakes():
    """CT33 (ruin slack): along rising stakes the chosen design's upkeep never falls and its error never rises."""
    for s in range(200):
        r = np.random.default_rng(300 + s); GL, GS = r.uniform(0.05, 1, 2); GB = r.uniform(max(GL, GS), GL + GS)
        n, hc = int(10 ** r.uniform(0, 3)), 10 ** r.uniform(-1, 2.5); nu = n / hc; kL, kS = (GB - GS) / GL, (GB - GL) / GS
        up = [0, n, hc, n + hc]; err = [1, 1 - GL, 1 - GS, 1 - GB]; last = None
        for wu in np.logspace(-2, 5, 300):
            d = int(fm.decide(wu * GL, n * wu * GS / hc, nu, kL, kS))
            if last is not None: assert up[d] >= up[last] - 1e-12 and err[d] <= err[last] + 1e-12
            last = d

def test_collapse_records():
    v1 = json.load(open(os.path.join(FIG, 'face_collapse_v1.json')))['summary']
    v1b = json.load(open(os.path.join(FIG, 'face_collapse_v1b.json')))['summary']
    v23 = json.load(open(os.path.join(FIG, 'face_collapse_v23.json')))['summary']
    assert v1['agree'] == 1.0 and v1['M'] >= 3000 and v1['max_rel_err_GL'] < 1e-9 and v1['max_rel_err_GS'] < 1e-8
    assert v1b['agree'] == 1.0 and v1b['M'] >= 1500
    assert v23['v3_greedy_same'] == 1.0 and v23['v3_greedy_regret_max'] == 0.0 and v23['v2_convex_within_tol'] > 0.99

def test_dots_match_notes():
    """Every placement's design in face_dots.json is the one face_placements.md states, and recomputes from its centre."""
    dots = json.load(open(os.path.join(FIG, 'face_dots.json')))
    md = open(os.path.join(FIG, 'face_placements.md')).read()
    rows = {}
    for line in md.splitlines():
        m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|.*\|\s*\*\*(none|local|shared|both)\*\*', line)
        if m: rows[(m.group(1).rstrip('*'), m.group(2))] = m.group(3)
    assert len(rows) == len(dots)
    for d in dots:
        c = d['centre']
        assert rows[(d['system'], d['lab'])] == fm.VALUE_NAMES[c['d']]
        if np.isfinite(c['XS']): assert int(fm.decide(c['XL'], c['XS'], c['nu'], c['kL'], c['kS'])) == c['d']
        else: assert c['d'] == int(c['XL'] > 1)
