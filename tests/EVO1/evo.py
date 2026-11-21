#!/usr/bin/env python3
"""EVO1 simulator: designed worlds + mutation/selection on realized outcomes.  Imports NO theory code: no predict_evo, no
stores.py, no face_hybrid, no PREDICTIONS_EVO.json.  Fitness is built only from what happened in each agent's life:
upkeep paid per store, a price per unit store speed, the stake times the realized squared error of its estimate of the
realized signal, and death if its reserve hits zero.
Run:  nice -n 19 python3 evo.py WORLD SEED [--null] [--out DIR]
World definitions: worlds.json (the experimenter's settings: spectrum, noise, prices; the same file the prediction reads)."""
import os, sys, json, time, argparse
import numpy as np
import numba as nb
HERE = os.path.dirname(os.path.abspath(__file__))
KMAX = 4                        # stores per class (local, shared) a genome can carry

# ------------------------------------------------------------------ world realization (shared by every agent: common
# random numbers, one world per generation, as all members of a population live in the same world)
def make_world(p, T, rng):
    n = p.get('n', 1)
    if p['kind'] == 'rw':
        inc = np.sqrt(p['q']) * rng.standard_normal(T)
        s = np.cumsum(inc)[None, :].repeat(n, 0)
    else:
        a = np.asarray(p['a'] if p['kind'] == 'ou' else [p['lam']], float)
        v = np.asarray(p['v'] if p['kind'] == 'ou' else [p['sigma2']], float)
        rho = np.asarray(p.get('rho', [1] * len(a)), float)
        s = np.zeros((n, T))
        for j in range(len(a)):
            phi = np.exp(-a[j]); sd = np.sqrt(v[j] * (1 - phi * phi))
            m = 1 if rho[j] >= 1 else n
            e = rng.standard_normal((m, T)) * sd
            e[:, 0] = rng.standard_normal(m) * np.sqrt(v[j])            # stationary start
            x = _ar1(e, phi)
            s += x if m == n else x.repeat(n, 0)
    N = p.get('N', 0.0); Nc = p.get('Nc', 0.0)
    y = s + np.sqrt(N) * rng.standard_normal((n, T)) + np.sqrt(Nc) * rng.standard_normal(T)[None, :]
    return s, y, y.mean(0)

@nb.njit(cache=True)
def _ar1(e, phi):
    x = np.empty_like(e)
    for i in range(e.shape[0]):
        x[i, 0] = e[i, 0]
        for t in range(1, e.shape[1]): x[i, t] = phi * x[i, t - 1] + e[i, t]
    return x

# ------------------------------------------------------------------ one generation: every agent lives once in the world
@nb.njit(parallel=True, cache=True)
def live(s, y, ybar, nl, bl, gl, nc, bc, gc, h, hc, h1, w, lead, burn, sn_on, sn_s, sn_V0, sn_tau0, income, buffer, seed0):
    P = nl.shape[0]; n = s.shape[0]; T = s.shape[1]
    cost = np.zeros(P); alive = np.ones(P, np.bool_); mse = np.zeros(P)
    for p in nb.prange(P):
        np.random.seed(seed0 + p)
        kl = nl[p]; kc = nc[p]
        betal = 1.0 - np.exp(-bl[p, :kl]); betac = 1.0 - np.exp(-bc[p, :kc])
        zl = np.zeros((n, kl)); zc = np.zeros(kc)
        # store noise (Model S+ world arm): AR(1) at the store's own rate, stationary variance V0 (tau0 b)^(2-2s)
        phil = np.exp(-bl[p, :kl]); sdl = np.zeros(kl); xil = np.zeros((n, kl))
        if sn_on:
            for k in range(kl):
                V = sn_V0 * (sn_tau0 * bl[p, k]) ** (2.0 - 2.0 * sn_s)
                sdl[k] = np.sqrt(V * (1.0 - phil[k] ** 2))
                for i in range(n): xil[i, k] = np.sqrt(V) * np.random.standard_normal()
        L = lead + 1; ring = np.zeros(L)
        up = n * h * kl + hc * kc
        for k in range(kl): up += h1 * n * bl[p, k]
        for k in range(kc): up += h1 * bc[p, k]
        R = buffer; acc = 0.0; acce = 0.0; cnt = 0; dead = False
        for t in range(T):
            sh = 0.0
            for k in range(kc):
                zc[k] += betac[k] * (ybar[t] - zc[k]); sh += gc[p, k] * zc[k]
            ring[t % L] = sh
            shd = ring[(t - lead) % L] if t >= lead else 0.0
            se = 0.0
            for i in range(n):
                est = shd
                for k in range(kl):
                    zl[i, k] += betal[k] * (y[i, t] - zl[i, k])
                    out = zl[i, k]
                    if sn_on:
                        xil[i, k] = phil[k] * xil[i, k] + sdl[k] * np.random.standard_normal()
                        out += xil[i, k]
                    est += gl[p, k] * out
                d = s[i, t] - est; se += d * d
            if t >= burn:
                c = up + w * se
                acc += c; acce += se / n; cnt += 1
                R += income - c
                if R < 0.0: dead = True; break
        cost[p] = acc / max(cnt, 1); mse[p] = acce / max(cnt, 1); alive[p] = not dead
    return cost, alive, mse

# ------------------------------------------------------------------ genome
class Pop:
    def __init__(s, P):
        s.nl = np.zeros(P, np.int64); s.nc = np.zeros(P, np.int64)
        s.bl = np.full((P, KMAX), 1e-3); s.gl = np.zeros((P, KMAX)); s.bc = np.full((P, KMAX), 1e-3); s.gc = np.zeros((P, KMAX))
    def take(s, idx):
        o = Pop(0)
        for k in ('nl', 'nc', 'bl', 'gl', 'bc', 'gc'): setattr(o, k, getattr(s, k)[idx].copy())
        return o

def init_pop(p, E, P, start, rng):
    pop = Pop(P); lo, hi = np.log(E['init_rate_range'][0]), np.log(E['init_rate_range'][1])
    shared_ok = p.get('n', 1) > 1
    for i in range(P):
        if start == 'low':
            pop.nl[i] = 1; pop.bl[i, 0] = np.exp(rng.uniform(lo, hi)); pop.gl[i, 0] = 1.0
        else:
            k = KMAX if not shared_ok else E['high_start_local']
            pop.nl[i] = k; pop.bl[i, :k] = np.sort(np.exp(rng.uniform(lo, hi, k))); pop.gl[i, :k] = 1.0 / k
            if shared_ok:
                kc = E['high_start_shared']; pop.nc[i] = kc
                pop.bc[i, :kc] = np.sort(np.exp(rng.uniform(lo, hi, kc))); pop.gc[i, :kc] = 1.0 / (k + kc)
                pop.gl[i, :k] = 1.0 / (k + kc)
    return pop

def mutate(pop, p, E, rng):
    P = len(pop.nl); M = E['mutation']; shared_ok = p.get('n', 1) > 1
    rmin, rmax = E['rate_bounds']
    for i in range(P):
        for cls in (('nl', 'bl', 'gl'), ('nc', 'bc', 'gc')):
            nk, bk, gk = cls; k = getattr(pop, nk)[i]; b = getattr(pop, bk)[i]; g = getattr(pop, gk)[i]
            if k:
                b[:k] = np.clip(b[:k] * np.exp(M['sd_lograte'] * rng.standard_normal(k)), rmin, rmax)
                g[:k] = g[:k] + M['sd_weight'] * (np.abs(g[:k]) + M['weight_floor']) * rng.standard_normal(k)
        # structural mutations, one class picked at random (shared only in group worlds)
        cls = ('nc', 'bc', 'gc') if (shared_ok and rng.random() < 0.5) else ('nl', 'bl', 'gl')
        nk, bk, gk = cls; k = getattr(pop, nk)[i]; b = getattr(pop, bk)[i]; g = getattr(pop, gk)[i]
        u = rng.random()
        if u < M['p_dup']:
            if 0 < k < KMAX:          # duplicate-split: the copy starts nearly neutral (half the weight on each)
                j = rng.integers(k); b[k] = np.clip(b[j] * np.exp(M['sd_dup_lograte'] * rng.standard_normal()), rmin, rmax)
                g[j] *= 0.5; g[k] = g[j]; getattr(pop, nk)[i] = k + 1
            elif k == 0:              # a new store from nothing, weight zero
                b[0] = np.exp(rng.uniform(np.log(E['init_rate_range'][0]), np.log(E['init_rate_range'][1]))); g[0] = 0.0
                getattr(pop, nk)[i] = 1
        elif u < M['p_dup'] + M['p_del'] and k > 0:
            j = rng.integers(k)
            if k > 1:                 # its weight moves to the nearest store of the same class
                others = [x for x in range(k) if x != j]; m = min(others, key=lambda x: abs(np.log(b[x] / b[j]))); g[m] += g[j]
            b[j:k - 1] = b[j + 1:k].copy(); g[j:k - 1] = g[j + 1:k].copy(); b[k - 1] = 1e-3; g[k - 1] = 0.0
            getattr(pop, nk)[i] = k - 1
        elif shared_ok and u < M['p_dup'] + M['p_del'] + M['p_switch'] and k > 0:
            ok_, ob_, og_ = ('nl', 'bl', 'gl') if nk == 'nc' else ('nc', 'bc', 'gc')
            ko = getattr(pop, ok_)[i]
            if ko < KMAX:             # a store changes class (local <-> shared), keeping its rate and weight
                j = rng.integers(k); getattr(pop, ob_)[i][ko] = b[j]; getattr(pop, og_)[i][ko] = g[j]; getattr(pop, ok_)[i] = ko + 1
                b[j:k - 1] = b[j + 1:k].copy(); g[j:k - 1] = g[j + 1:k].copy(); b[k - 1] = 1e-3; g[k - 1] = 0.0
                getattr(pop, nk)[i] = k - 1
    # keep stores sorted by rate within class (bookkeeping only)
    for nk, bk, gk in (('nl', 'bl', 'gl'), ('nc', 'bc', 'gc')):
        for i in range(P):
            k = getattr(pop, nk)[i]
            if k > 1:
                o = np.argsort(getattr(pop, bk)[i][:k]); getattr(pop, bk)[i][:k] = getattr(pop, bk)[i][:k][o]; getattr(pop, gk)[i][:k] = getattr(pop, gk)[i][:k][o]
    return pop

def run(world, seed, null=False, outdir=None, gens=None, quiet=False):
    cfg = json.load(open(os.path.join(HERE, 'worlds.json'))); p = cfg['worlds'][world]; E = dict(cfg['evolution']); E.update(p.get('evolution', {}))
    P, beta, G = E['P'], (0.0 if null else E['beta']), (gens or E['generations'])
    burn, T = p['burn'], p['burn'] + p['T_score']
    start = 'low' if seed % 2 == 0 else 'high'
    rng = np.random.default_rng([seed, sum(map(ord, world)), int(null)])
    pop = init_pop(p, E, P, start, rng)
    sn = p['kind'] == 'storenoise'
    income = p['income']; buffer = p['buffer_steps'] * income
    log = []; snaps = []; t0 = time.time()
    for g in range(G):
        s, y, ybar = make_world(p, T, rng)
        cost, alive, mse = live(s, y, ybar, pop.nl, pop.bl, pop.gl, pop.nc, pop.bc, pop.gc, p['h'], p.get('hc', p['h']),
                                p.get('h1', 0.0), p['w'], int(p.get('lead', 0)), burn, sn, p.get('s', 0.5), p.get('V0', 0.0),
                                p.get('tau0', 1.0), (1e18 if null else income), (1e18 if null else buffer), int(rng.integers(1, 2**31 - P)))
        if null:
            alive[:] = True
        med = np.median(cost[alive]) if alive.any() else 1.0
        f = np.where(alive, np.exp(-beta * (cost - med) / med), 0.0)
        if f.sum() <= 0: f = np.ones(P)
        # record the generation (before reproduction)
        struct = [f'{a}L{b}S' for a, b in zip(pop.nl, pop.nc)]
        vals, cnts = np.unique(struct, return_counts=True)
        log.append(dict(g=g, med_cost=float(med), mean_cost=float(cost[alive].mean()) if alive.any() else None,
                        dead=int((~alive).sum()), modal=str(vals[cnts.argmax()]), modal_frac=float(cnts.max() / P)))
        if g >= int(G * (1 - E['consensus_window'])):
            for i in np.flatnonzero(alive):
                snaps.append(dict(nl=int(pop.nl[i]), nc=int(pop.nc[i]), bl=pop.bl[i, :pop.nl[i]].tolist(), gl=pop.gl[i, :pop.nl[i]].tolist(),
                                  bc=pop.bc[i, :pop.nc[i]].tolist(), gc=pop.gc[i, :pop.nc[i]].tolist(), cost=float(cost[i])))
        idx = rng.choice(P, size=P, p=f / f.sum())
        pop = mutate(pop.take(idx), p, E, rng)
        if not quiet and (g % 50 == 0 or g == G - 1):
            print(f'{world} seed {seed} {"NULL " if null else ""}g{g} med {med:.5f} dead {(~alive).sum()} modal {log[-1]["modal"]} '
                  f'({log[-1]["modal_frac"]:.2f}) {time.time() - t0:.0f}s', flush=True)
    res = dict(world=world, seed=seed, null=null, start=start, P=P, beta=beta, G=G, log=log, consensus=consensus(snaps),
               secs=time.time() - t0)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        fn = os.path.join(outdir, f'{world}_s{seed}{"_null" if null else ""}.json')
        json.dump(res, open(fn, 'w'))
        # final-window genomes, compressed
        np.savez_compressed(fn.replace('.json', '_snaps.npz'), snaps=np.array([json.dumps(x) for x in snaps[-20000:]]))
    return res

def consensus(snaps):
    """The evolved design: the modal store structure over the last window, then the median log-rate and median weight
    of each rate-ordered store within that structure."""
    if not snaps: return None
    keys = [f'{x["nl"]}L{x["nc"]}S' for x in snaps]; vals, cnts = np.unique(keys, return_counts=True)
    mk = str(vals[cnts.argmax()]); sel = [x for x, k in zip(snaps, keys) if k == mk]
    out = dict(structure=mk, structure_frac=float(cnts.max() / len(snaps)), n_genomes=len(snaps),
               structure_dist={str(v): int(c) for v, c in zip(vals, cnts)})
    for cls in ('l', 'c'):
        k = sel[0]['n' + cls]
        B = np.array([x['b' + cls] for x in sel]).reshape(len(sel), k); Gm = np.array([x['g' + cls] for x in sel]).reshape(len(sel), k)
        out['b' + cls] = np.exp(np.median(np.log(B), 0)).tolist() if k else []
        out['g' + cls] = np.median(Gm, 0).tolist() if k else []
        out['b' + cls + '_iqr_log'] = (np.percentile(np.log(B), 75, 0) - np.percentile(np.log(B), 25, 0)).tolist() if k else []
    return out

def evaluate(world, bl, gl, bc, gc, reps, seed=0, T_score=None):
    """Realized mean cost of a FIXED design over `reps` independent worlds (calibration only; no selection)."""
    cfg = json.load(open(os.path.join(HERE, 'worlds.json'))); p = cfg['worlds'][world]
    burn = p['burn']; T = burn + (T_score or p['T_score']); rng = np.random.default_rng([seed, 777])
    D = len(bl)  # list of designs
    nl = np.array([len(x) for x in bl]); nc = np.array([len(x) for x in bc])
    BL = np.full((D, KMAX), 1e-3); GL = np.zeros((D, KMAX)); BC = np.full((D, KMAX), 1e-3); GC = np.zeros((D, KMAX))
    for i in range(D):
        BL[i, :nl[i]] = bl[i]; GL[i, :nl[i]] = gl[i]; BC[i, :nc[i]] = bc[i]; GC[i, :nc[i]] = gc[i]
    out = []
    for r in range(reps):
        s, y, ybar = make_world(p, T, rng)
        c, a, m = live(s, y, ybar, nl, BL, GL, nc, BC, GC, p['h'], p.get('hc', p['h']), p.get('h1', 0.0), p['w'], int(p.get('lead', 0)),
                       burn, p['kind'] == 'storenoise', p.get('s', 0.5), p.get('V0', 0.0), p.get('tau0', 1.0), 1e18, 1e18, int(rng.integers(1, 2**31 - D)))
        out.append(c)
    return np.array(out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('world'); ap.add_argument('seed', type=int)
    ap.add_argument('--null', action='store_true'); ap.add_argument('--out', default=os.path.join(HERE, 'runs')); ap.add_argument('--gens', type=int)
    a = ap.parse_args()
    run(a.world, a.seed, a.null, a.out, a.gens)
