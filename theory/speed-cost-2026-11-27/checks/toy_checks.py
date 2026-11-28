"""Toy-input checks of every helper the scored path calls (launch rule, process/PREREG_GATE.md section 2).
All inputs are OFF the scored grid. Prints booleans and n=2 numbers only; it prints no n=3 or n=4 heat or excess.
Run: nice -n 19 python3 toy_checks.py"""
import numpy as np
from sc_lib import *
from sc_run import work, MASTER_SEED
from sc_score import best_by

ok = True
def check(name, cond):
    global ok
    ok &= bool(cond)
    print(f'{name}: {"PASS" if cond else "FAIL"}')

# 1. CORE's telegraph number (theory/GENERAL_FORM_PHYSICS_2026-11-22.md:66): L(0.2) = 0.6 ln 4 = 0.831776616672
check('floor at eps=0.2 equals 0.6 ln 4', abs(floor_heat(0.2) - 0.6 * np.log(4)) < 1e-12)

# 2. stationary solver on a random 3-state memory: normalization, balance, world marginal 1/2
rng = np.random.default_rng(3)
W = rng.uniform(0.2, 2.0, size=(2, 3, 3)); W[:, np.arange(3), np.arange(3)] = 0
p = stationary(W)
A_ = build_generator(W)
check('stationary sums to 1', abs(p.sum() - 1) < 1e-12)
check('stationary balance', np.abs(p.ravel() @ A_).max() < 1e-12)
check('world marginal is 1/2', np.abs(p.sum(axis=1) - 0.5).max() < 1e-12)

# 3. two-state closed form against the generic heat and error code, at off-grid points
for G, e in ((7.0, 0.35), (50.0, 0.15)):
    h, am, ap = two_state_closed(G, e)
    W2 = np.zeros((2, 2, 2))
    for x in (0, 1):
        for i in (0, 1):
            W2[x, i, 1 - i] = am if i == x else ap
    p2 = stationary(W2)
    check(f'two-state closed form matches generic code at G={G}, eps={e}',
          abs(heat(W2, p2) - h) < 1e-10 and abs(error(p2, (0, 1)) - e) < 1e-12)
    print(f'  n=2 heat {h:.9f} floor {floor_heat(e):.9f} E2 {h / floor_heat(e) - 1:.9f}')

# 4. large-G limit of the two-state excess is small and follows (1-2e)/(e G L)
G, e = 1e6, 0.15
E2 = two_state_closed(G, e)[0] / floor_heat(e) - 1
check('large-G excess matches the asymptotic form to 1%', abs(E2 / ((1 - 2 * e) / (e * G * np.log((1 - e) / e))) - 1) < 0.01)

# 5. optimizer at n=2 reproduces the closed form (embedded and random starts), cap binding
for G, e in ((7.0, 0.35), (50.0, 0.15)):
    h = two_state_closed(G, e)[0]
    for s in (-1, 0, 1, 2):
        pi = 99
        t = ('A', pi, G, e, 2, 0, (0, 1), s)
        r = work(t)
        check(f'optimizer n=2 start {s} reproduces closed form at G={G}, eps={e}', r is not None and r['ok'] and abs(r['heat'] - h) / h < 1e-6)

# 6. n=3 code gate (boolean only): embedded start guarantees a result no worse than n=2; cap and error respected
G, e = 7.0, 0.35
h2 = two_state_closed(G, e)[0]
rs = [work(('A', 98, G, e, 3, 0, labelings(3)[0], s)) for s in (-1, 0, 1, 2, 3, 4)]
rs = [r for r in rs if r is not None and r['ok']]
check('n=3: at least one admissible design returned', len(rs) > 0)
check('n=3: the embedded start is admissible and within 1e-5 (relative) of the two-state optimum or better', any(r['s'] == -1 and r['heat'] <= h2 * (1 + 1e-5) for r in rs))
check('n=3: exit cap respected (capviol <= 1e-7) and error <= target + 1e-7', all(r['capviol'] <= 1e-7 and r['eps'] <= e + 1e-7 for r in rs))

# 7. edge-cap arm runs and is admissible (boolean only)
rB = [work(('B', 97, G, e, 3, 0, labelings(3)[0], s)) for s in (-1, 0, 1)]
rB = [r for r in rB if r is not None and r['ok']]
check('edge-cap arm returns admissible designs', len(rB) > 0 and all(r['eps'] <= e + 1e-7 for r in rB))

# 8. scoring helper: best_by keeps the lowest E per key and ignores inadmissible rows
fake = [{'ok': True, 'E': 0.3, 'pi': 0, 'n': 2}, {'ok': True, 'E': 0.1, 'pi': 0, 'n': 2}, {'ok': False, 'E': 0.0, 'pi': 0, 'n': 2}]
check('best_by picks the lowest admissible E', best_by(fake, lambda r: (r['pi'], r['n']))[(0, 2)]['E'] == 0.1)

print('ALL TOY CHECKS PASS' if ok else 'TOY CHECKS FAILED')
