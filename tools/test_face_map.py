"""The face map (figures/face_map.py): its decision rule, closed forms, invariance, and placements, checked independently.
Run: nice -n 19 python3 -m pytest -q tools/test_face_map.py      (about a minute)"""
import os, sys, json, re
import numpy as np
import pytest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'records', 'figures'); sys.path.insert(0, FIG)
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

def test_quadrant_edges_under_subadditivity():
    """With 0 <= kappa <= 1 (subadditive value), outside the top-right quadrant no number other than (X_L, X_S) changes the design."""
    for _ in range(4000):
        XL, XS = 10 ** RNG.uniform(-3, 3, 2)
        q = int(fm.quadrant(XL, XS))
        ds = {int(fm.decide(XL, XS, 10 ** RNG.uniform(-4, 4), *RNG.uniform(0, 1, 2))) for _ in range(30)}
        if q < 3: assert ds == {q}
        else: assert ds <= {1, 2, 3}

def test_quadrant_fails_without_subadditivity():
    """kappa > 1 (joint value): BOTH can win where neither layer pays alone, and where only one does; X_B decides (exact identity)."""
    XL, XS, nu = 0.95, 0.95, 1.0
    kS = 1.2; kL = 1 + (kS - 1) * XS / (nu * XL)              # consistent pair: (1 - kS) G_S = (1 - kL) G_L
    assert fm.quadrant(XL, XS) == 0 and fm.decide(XL, XS, nu, kL, kS) == 3 and fm.XB(XL, XS, nu, kS) > 1
    assert not fm.subadditive(kL, kS)
    for _ in range(3000):                                     # in general: NONE iff max(X_L, X_S, X_B) <= 1, for any kappa
        XL, XS = 10 ** RNG.uniform(-1, 1, 2); nu = 10 ** RNG.uniform(-2, 2); kS = 10 ** RNG.uniform(-1, 1.5)
        kL = 1 + (kS - 1) * XS / (nu * XL)
        if kL < 0: continue
        assert (fm.decide(XL, XS, nu, kL, kS) == 0) == (max(XL, XS, fm.XB(XL, XS, nu, kS)) <= 1 + 1e-12)

def test_suppression_identity():
    """Fixed rates: (G_B - G_L - G_S)/Var = rLS((rL^2 + rS^2) rLS - 2 rL rS)/(1 - rLS^2) for two linear predictors (exact)."""
    r = np.random.default_rng(5)
    for _ in range(300):
        A = r.normal(size=(3, 3)); C = A @ A.T + 0.1 * np.eye(3); d = np.sqrt(np.diag(C)); C = C / np.outer(d, d)
        rL, rS, rLS = C[0, 1], C[0, 2], C[1, 2]
        R2B = C[0, 1:] @ np.linalg.solve(C[1:, 1:], C[0, 1:])
        assert np.isclose(R2B - rL ** 2 - rS ** 2, fm.excess_fixed(rL, rS, rLS), atol=1e-10)
    assert fm.excess_fixed(0.6, 0.5, 0.30) <= 0            # predictors independent given the target (rLS = rL rS): subadditive
    assert fm.excess_fixed(0.6, 0.05, 0.9) > 0             # a reference that shares the nuisance, not the target: joint value

def _priced(n, rho, l, wu, c):
    """Review 26 counterexample A machinery: reading priced at c/N per unit, N chosen per design; returns (W_L, W_S, W_B) and best errors."""
    from scipy.optimize import minimize_scalar
    a = v = 1.0
    def err(kind, lnN):
        N = np.exp(lnN)
        if kind == 'L': return v - fm.gains_ou(v, a, N, n, rho, l)[0]
        if kind == 'S': return v - fm.gains_ou(v, a, N, n, rho, l)[1]
        return min(best_fast([a], [v], N, n, rho, l, 1, 1, starts=3, seed=0)[0], v - max(fm.gains_ou(v, a, N, n, rho, l)[:2]))
    out = {k: minimize_scalar(lambda x: n * c / np.exp(x) + n * wu * err(k, x), bounds=(-12, 12), method='bounded', options=dict(xatol=1e-6)).fun for k in 'LSB'}
    base = n * wu * v
    return base - out['L'], base - out['S'], base - out['B'], out

def test_review26_counterexample_A_priced_reading():
    """Priced reading: net worths are superadditive (reads paid once by 'both'); at X_L = X_S = 0.95 the best design is BOTH, not NONE."""
    n, wu = 11, 8.6724
    WL, WS, WB, out = _priced(n, 0.4885, 0.0011, wu, 4.0794)
    assert WB - WL - WS > 1.5
    hl, hc = WL / n / 0.95, WS / 0.95
    cost = {'none': n * wu, 'local': n * hl + out['L'], 'shared': hc + out['S'], 'both': n * hl + hc + out['B']}
    assert fm.quadrant(WL / (n * hl), WS / hc) == 0 and min(cost, key=cost.get) == 'both'
    assert cost['none'] < cost['local'] and cost['none'] < cost['shared']        # no single addition pays: greedy stops at NONE

def test_review26_counterexample_B_scales_one_stream():
    """No reading price, independent noise: a fast common part and a slow idiosyncratic part on one stream give kappa_L > 1; BOTH wins
    in the NONE corner (X = 0.99) and in the LOCAL quadrant (X_L = 3, X_S = 0.97); greedy stops short, the pairwise look-ahead does not."""
    sys.path.insert(0, FIG); import face_subadd as fs
    n = 384; GL, GS, GB, V = fs.gains([1.0, 0.0029], [0.6719, 0.3281], 7.8613, n, [1.0, 0.0], 5.0031)
    assert GB - GL - GS > 0.006 and (GB - GS) / GL > 1.02
    for XL, XS in ((0.99, 0.99), (3.0, 0.97)):
        wu = 1.0; hl = wu * GL / XL; hc = n * wu * GS / XS
        cost = {(0, 0): n * wu * V, (1, 0): n * hl + n * wu * (V - GL), (0, 1): hc + n * wu * (V - GS), (1, 1): n * hl + hc + n * wu * (V - GB)}
        assert min(cost, key=cost.get) == (1, 1) and fm.quadrant(XL, XS) in (0, 1)
    assert cost[(1, 0)] < cost[(0, 0)]                      # at X_L = 3 greedy adds local and then...
    assert cost[(1, 1)] < cost[(1, 0)]                      # ...the shared layer pays on top: greedy reaches BOTH here
    XL = XS = 0.99; hl = GL / XL; hc = n * GS / XS
    c0, cl, cs, cb = n * V, n * hl + n * (V - GL), hc + n * (V - GS), n * hl + hc + n * (V - GB)
    assert cl > c0 and cs > c0 and cb < c0                  # NONE corner: greedy stops at NONE, the pair (local + shared) pays

def test_subadditivity_by_class():
    s = json.load(open(os.path.join(FIG, 'face_subadd.json')))['summary']
    assert s['base']['superadditive'] == 0 and s['base_adversarial']['max_excess'] < 1e-5
    assert s['cnoise']['superadditive'] > 0 and s['scales']['superadditive'] > 0 and s['priced_v1b']['superadditive'] > 0

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
        Nc = 0.0 if RNG.uniform() < 0.5 else 10 ** RNG.uniform(-2, 1)
        x, y = mse(a, v, N, n, rho, lead, bl, bc, Nc), mse_fast(a, v, N, n, rho, lead, bl, bc, Nc)
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

def test_subadditive_in_separate_channel_class():
    """Separate-channel class (one OU component, independent noise, unpriced): G_B <= G_L + G_S in every world sampled (not proved)."""
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
    assert v23['v2_convex_within_tol'] > 0.99 and v23['M3'] >= 800
    a = v23['v3_all']; assert a['pair_same'] >= a['greedy_same'] and a['pair_regret_max'] <= a['greedy_regret_max'] + 1e-12

def test_dots_match_notes():
    """Every placement's design in face_dots.json is the one face_placements.md states, and recomputes from its centre."""
    dots = json.load(open(os.path.join(FIG, 'face_dots.json')))
    md = open(os.path.join(FIG, 'face_placements.md')).read()
    rows = {}
    for line in md.splitlines():
        m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|.*\|\s*\*\*(none|local|shared|both)\*\*', line)
        if m: rows[(m.group(1).rstrip('*'), m.group(2))] = m.group(3)
    dots = [d for d in dots if not d.get('measured')]          # E. coli is a proxy strip, off the map
    assert len(rows) == len(dots) and 'off the map (proxy)' in md
    for d in dots:
        c = d['centre']
        assert d['joint_share'] == 0 and not c['joint'] and np.isclose(c['XB'], fm.XB(c['XL'], c['XS'], c['nu'], c['kS']))
        assert rows[(d['system'], d['lab'])] == fm.VALUE_NAMES[c['d']]
        if np.isfinite(c['XS']): assert int(fm.decide(c['XL'], c['XS'], c['nu'], c['kL'], c['kS'])) == c['d']
        else: assert c['d'] == int(c['XL'] > 1)

def test_inputs_frozen():
    """face_systems.py is the preregistered prediction (face_placements.md §4 step 9): a change voids the comparison for that class."""
    import hashlib
    h = hashlib.sha256(open(os.path.join(FIG, 'face_systems.py'), 'rb').read()).hexdigest()
    assert h == '00f6f25d796bbd1862f6ad9f04ef53bd986185f1177052339632e20b15095377' and h in open(os.path.join(FIG, 'face_placements.md')).read(), 'face_systems.py changed after the freeze'

def test_conditioning_guard_review26_seed34():
    """Near-coincident stores (review 26 round 2, seed 34): both evaluators now agree, and the optimizer keeps stores >= 1% apart."""
    sys.path.insert(0, FIG); import face_hybrid as fh
    a, v, rho = np.array([1.0, 5e-3]), np.array([0.5, 0.5]), 0.5
    bl = np.array([18.968661, 18.968958, 19.173794]); bc = np.array([0.1, 0.01])
    x, y = fh.mse_fast(a, v, 0.3, 8, rho, 1.0, bl, bc), fh.mse(a, v, 0.3, 8, rho, 1.0, bl, bc)
    assert abs(x - y) < 1e-8 * v.sum()
    r = fh._rates(np.log(bl)); assert np.all(np.diff(np.log(r)) >= np.log(1.01) - 1e-12)
    e, xopt = fh.best_fast(a, v, 0.3, 8, rho, 1.0, 2, 1, starts=2)
    assert e >= fh.confirm(a, v, 0.3, 8, rho, 1.0, 2, 1, xopt) - 1e-12

def test_review26_seed40_three_scale_greedy_miss():
    """Review 26's three-scale world (figures/face_seed40.py): greedy and greedy + pairwise look-ahead both stop at 3 local + 2 shared
    stores, while 2 local + 3 shared is cheaper (regret 2.8e-4 of total cost). The stored rates must reproduce the stored costs (Lyapunov)."""
    sys.path.insert(0, FIG); import face_hybrid as fh, face_seed40 as s40
    R = json.load(open(os.path.join(FIG, 'face_seed40.json'))); W = R['world']
    a, v, rho = (np.array(W[k]) for k in ('a', 'v', 'rho'))
    assert R['exact'] == [2, 3] and R['greedy'] == [3, 2] and R['lookahead'] == [3, 2] and 2e-4 < R['regret_greedy'] < 4e-4
    for key in ('2,3', '3,2'):
        d = R['designs'][key]; kl, kc = map(int, key.split(','))
        E = fh.mse(a, v, W['N'], W['n'], rho, W['lead'], d['bl'], d['bc'])
        assert abs(s40.cost(kl, kc, E) - d['cost']) < 0.01
    C = {k: d['cost'] for k, d in R['designs'].items()}
    assert C['2,3'] < C['3,2'] < C['3,1'] < C['3,0'] < C['2,0'] and C['2,1'] > C['2,0'] and C['3,3'] > C['3,2']
