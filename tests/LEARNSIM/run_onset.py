"""Stage B: emergent onset.  For each (arm, cell, seed): members and the level LEARN their policies from
realized payoffs only (world.es_learn / world.pop_learn); then flat vs levelled organisations are run on
fresh paths and their realized per-member costs compared.  No expected-cost formula is used.
N-grid centres come from GRID_CENTERS.json (fixed in the prereg; used only to place a wide x/÷16 grid).
Usage: python run_onset.py OUT.jsonl [learner=es|pop] [seeds] [which=scan|fact|all]"""
import sys, json, os, numpy as np
from multiprocessing import Pool
import world as w

P = 2500            # warm-up prefix (>= max T)
LEVAL = 400000      # counted steps per evaluation path
M_EVAL = 64         # members simulated in evaluation (stakes N enter only through the level's realized loss)
M_LEARN = 16        # independently learning members per arm
M_IND = 32          # members in the independent (no common-random-numbers) flat evaluation
NG = 17             # N grid: centre * 2**((j-8)/2), j = 0..16

ARMS = {'RR': ('R', 'R', 0.0), 'RRh': ('R', 'R', 40.0), 'AA': ('A', 'A', 0.0),
        'AR': ('A', 'R', 0.0), 'RA': ('R', 'A', 0.0)}

def track(tech, eff, x, rng):
    """run one tracker with a fixed learned policy over path x; return (errors on [P:], spend per step)."""
    if tech == 'R':
        T = int(eff); ph = int(rng.integers(T))
        t = np.arange(P, x.shape[0])
        last = ph + ((t - ph) // T) * T
        nr = np.count_nonzero(((t - ph) % T) == 0)
        return x[t] - x[last], w.C_R * nr / t.shape[0]
    y = x + np.sqrt(w.SIG2 / eff) * rng.standard_normal(x.shape[0])
    al = w.tune_alpha(y, P)
    return w._errs(y, x, al)[P:], w.C_A * eff

def learn(tech, Wt, q, rng, learner):
    return w.es_learn(tech, Wt, q, rng) if learner == 'es' else w.pop_learn(tech, Wt, q, rng)

def job(a):
    arm, cell, qg, qu, centre, seed, learner = a
    lev, mem, h = ARMS[arm]
    tag = sum(map(ord, arm + cell))
    rl = np.random.default_rng([11, tag, seed, learner == 'pop'])
    re = np.random.default_rng([13, tag, seed, learner == 'pop'])
    Ns = [centre * 2 ** ((j - 8) / 2) for j in range(NG)]
    flat_eff = [learn(mem, 1.0, qg + qu, rl, learner) for _ in range(M_LEARN)]
    res_eff = [learn(mem, 1.0, qu, rl, learner) for _ in range(M_LEARN)]
    lev_eff = [learn(lev, N, qg, rl, learner) for N in Ns]
    Lt = P + LEVAL
    g = w.bm(re, Lt, qg)
    eg, sg = zip(*[track(lev, e, g, re) for e in lev_eff])
    sum_eu = np.zeros(LEVAL); flat_c = []; res_c = []
    for i in range(M_EVAL):
        u = w.bm(re, Lt, qu)
        ef, sf = track(mem, flat_eff[i % M_LEARN], g + u, re)
        flat_c.append(sf + np.dot(ef, ef) / LEVAL)
        er, sr = track(mem, res_eff[i % M_LEARN], u, re)
        sum_eu += er
        res_c.append(sr + np.dot(er, er) / LEVAL)
    ebar = sum_eu / M_EVAL
    flat_pm = float(np.mean(flat_c)); res_pm = float(np.mean(res_c))
    lev_rows = []
    for N, e, s in zip(Ns, eg, sg):
        lg = float(np.dot(e, e) / LEVAL); cross = float(2 * np.dot(e, ebar) / LEVAL)
        lev_rows.append(dict(N=N, spend=float(s), loss_g=lg, cross=cross, level_pm=(s + h) / N + lg + cross + res_pm))
    # independent-world flat evaluation (no common random numbers)
    g2 = w.bm(re, Lt, qg); f2 = []
    for i in range(M_IND):
        u = w.bm(re, Lt, qu)
        ef, sf = track(mem, flat_eff[i % M_LEARN], g2 + u, re)
        f2.append(sf + np.dot(ef, ef) / LEVAL)
    flat2 = float(np.mean(f2))
    for r in lev_rows:
        r['D_rel'] = (flat_pm - r['level_pm']) / flat_pm
        r['D_rel_ind'] = (flat2 - r['level_pm']) / flat2
    return dict(arm=arm, cell=cell, qg=qg, qu=qu, h=h, centre=centre, seed=seed, learner=learner,
                flat_eff=[float(x) for x in flat_eff], res_eff=[float(x) for x in res_eff],
                lev_eff=[float(x) for x in lev_eff], flat_pm=flat_pm, flat2_pm=flat2, res_pm=res_pm, rows=lev_rows)

def joblist(learner, seeds, which):
    C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GRID_CENTERS.json')))
    J = []
    if which in ('scan', 'all'):
        for arm in ARMS:
            for rho, c in zip(C['rhos'], C['scan'][arm]):
                for s in range(seeds):
                    J.append((arm, 'rho=%g' % rho, rho * 1.0, 1.0, c, s, learner))
    if which in ('fact', 'all'):
        for arm, cells in C['fact'].items():
            for cell, (qg, qu, c) in cells.items():
                for s in range(seeds):
                    J.append((arm, 'fact:' + cell, qg, qu, c, s, learner))
    return J

def work(a):
    r = job(a)
    return json.dumps(r)

if __name__ == '__main__':
    os.nice(19)
    out = sys.argv[1]; learner = sys.argv[2] if len(sys.argv) > 2 else 'es'
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 16; which = sys.argv[4] if len(sys.argv) > 4 else 'all'
    done = set()
    if os.path.exists(out):
        for line in open(out):
            d = json.loads(line); done.add((d['arm'], d['cell'], d['seed'], d['learner']))
    J = [a for a in joblist(learner, seeds, which) if (a[0], a[1], a[5], a[6]) not in done]
    # A-heavy jobs first so the tail is short
    J.sort(key=lambda a: -('A' in a[0]))
    print('jobs to run', len(J), flush=True)
    with Pool(int(os.environ.get('NPROC', '3'))) as p, open(out, 'a') as f:
        for i, line in enumerate(p.imap_unordered(work, J, chunksize=1)):
            f.write(line + '\n'); f.flush()
            if i % 20 == 0: print('done', i + 1, '/', len(J), flush=True)
