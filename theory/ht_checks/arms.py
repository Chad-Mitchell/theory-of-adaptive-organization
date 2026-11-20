"""Arms A-E for theory/HT_INDEX.md. Run from this directory:  nice -n 19 python3 arms.py [A B C D E]
Writes arm_<X>.json. Seeds fixed; everything is in-model (simulated worlds), nothing about nature."""
import sys, json, os, time
import numpy as np
from multiprocessing import Pool
import htlib as H

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'layers_checks'))
from stores import E_K, E_inf, mse_given_b  # the repo's own Model S optimizer (theory/LAYERS.md)

NPROC = 6


def dump(name, obj):
    json.dump(obj, open(os.path.join(HERE, name), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))


# ------------------------------------------------------------------ A: what ht measures for one distribution
def armA():
    rng = np.random.default_rng(101)
    dists = {
        'pareto_1.5': lambda n: rng.pareto(1.5, n) + 1, 'pareto_2': lambda n: rng.pareto(2.0, n) + 1,
        'pareto_2.5': lambda n: rng.pareto(2.5, n) + 1, 'pareto_3': lambda n: rng.pareto(3.0, n) + 1,
        'exponential': lambda n: rng.exponential(size=n), 'lognormal_1': lambda n: rng.lognormal(0, 1, n),
        'halfnormal': lambda n: np.abs(rng.standard_normal(n)),
    }
    p_th = {'pareto_1.5': H.p_pareto(1.5), 'pareto_2': H.p_pareto(2.0), 'pareto_2.5': H.p_pareto(2.5),
            'pareto_3': H.p_pareto(3.0), 'exponential': np.exp(-1)}
    ns = [100, 1000, 10**4, 10**5, 10**6]
    out = {}
    for d, g in dists.items():
        rows = []
        for n in ns:
            for thr in (0.4, 0.5):
                v = [H.ht_index(g(n), thr) for _ in range(30)]
                rows.append(dict(n=n, thr=thr, mean=float(np.mean(v)), sd=float(np.std(v))))
        m4 = [r['mean'] for r in rows if r['thr'] == 0.4]
        slope = float(np.polyfit(np.log10(ns[1:]), m4[1:], 1)[0])
        out[d] = dict(rows=rows, slope_per_decade_thr04=slope,
                      predicted_slope=(float(np.log(10) / np.log(1 / p_th[d])) if d in p_th else None),
                      p_theory=(float(p_th[d]) if d in p_th else None))
        print(d, 'slope/decade', round(slope, 2), 'pred', out[d]['predicted_slope'], flush=True)
    # cascade world: K levels, sizes r^k, counts m^-k (the case head/tail breaks is built for), within-level lognormal spread sigma
    casc = []
    for K in (1, 2, 3, 4, 5):
        for sig in (0.1, 0.5, 1.0):
            for n0 in (10**3, 10**4, 10**5):
                v = []
                for _ in range(20):
                    x = np.concatenate([10.0 ** k * rng.lognormal(0, sig, max(1, int(n0 * 5.0 ** -k))) for k in range(K)])
                    v.append(H.ht_index(x))
                casc.append(dict(K=K, sigma=sig, n_base=n0, ht_mean=float(np.mean(v)), ht_sd=float(np.std(v))))
    out['cascade'] = casc
    dump('arm_A.json', out)


# ------------------------------------------------------------------ B: 1-D records of separated and scale-free worlds
DT = 0.1


def one_record_stats(y, dt, band):
    c, merged, K, fit = H.whittle_pole_count(y, dt, band=band, rng=np.random.default_rng(7))
    pk, _ = H.spectral_peak_count(y, dt, prom=0.1)
    _, _, h = H.mfdfa(y, qs=(-3, 2, 5))
    return dict(ht_absdy=H.ht_index(np.abs(np.diff(y))), ht_absy=H.ht_index(np.abs(y - y.mean())),
                ht_absdy_t05=H.ht_index(np.abs(np.diff(y)), 0.5),
                ht_per=H.ht_index(H.periodogram(y)), ht_cross=H.ht_index(H.crossing_durations(y)),
                whittle=int(c), whittle_taus=merged, whittle_fit=dict(taus=fit[0], vs=fit[1], N=float(fit[2])), peaks=int(pk), dfa_h=float(h[1]), mf_width=float(h[0] - h[2]))


def b_job(args):
    kind, par, n, noise, seed = args
    rng = np.random.default_rng(seed)
    if kind == 'ou':
        taus = np.array(par, float)
        y = H.ou_modes_fast(taus, np.ones(len(taus)) / len(taus), n, DT, rng).sum(0) + noise * rng.standard_normal(n)
    elif kind == 'band':   # repo's scale-free band: dense Lorentzian mixture, 8 per decade, alpha, span
        alpha, span = par
        a, v = scalefree(alpha, span)
        y = H.ou_modes_fast(1 / a, v, n, DT, rng).sum(0) + noise * rng.standard_normal(n)
    else:                  # fGn with Hurst exponent par (no time scale at all)
        y = H.fgn(par, n, rng) + noise * rng.standard_normal(n)
    st = one_record_stats(y, DT, (DT, n * DT / 10))
    return dict(kind=kind, par=par, n=n, noise=noise, seed=seed, **st)


def scalefree(alpha, span, per_decade=8, tau_min=1.0):
    J = max(2, int(round(per_decade * np.log10(span))) + 1)
    tau = tau_min * np.logspace(0, np.log10(span), J)
    v = tau ** (alpha - 1); v /= v.sum()
    return 1 / tau, v


def armB():
    jobs = []
    worlds = [[10.0], [1, 10], [1, 10, 100], [1, 10, 100, 1000], [1, 3], [1, 3, 9], [1, 3, 9, 27], [1, 100], [1, 100, 1e4 / 10]]
    seed = 1000
    for w in worlds:
        for n in (20000, 200000):
            for noise in (0.3, 1.0):
                for s in range(3):
                    jobs.append(('ou', w, n, noise, seed)); seed += 1
    for par in ((1.0, 1e3), (1.5, 1e3)):
        for n in (20000, 200000):
            for s in range(3):
                jobs.append(('band', par, n, 0.3, seed)); seed += 1
    for Hh in (0.3, 0.5, 0.7, 0.9):
        for n in (20000, 200000):
            for s in range(3):
                jobs.append(('fgn', Hh, n, 0.0, seed)); seed += 1
    t = time.time()
    with Pool(NPROC) as p:
        res = p.map(b_job, jobs, chunksize=1)
    print('B done', len(res), round(time.time() - t), 's', flush=True)
    dump('arm_B.json', res)


# ------------------------------------------------------------------ K*: the repo's optimizer on the arm-B / D worlds
def kstar_profile(taus, noise_sd, dt=DT, Kmax=4):
    taus = np.asarray(taus, float); a = 1 / taus; v = np.ones(len(a)) / len(a)
    N = noise_sd ** 2 * dt                 # discrete white noise of sd sigma at step dt <-> density N = sigma^2 dt
    ei = E_inf(a, v, N); rows = []
    for K in range(1, min(Kmax, len(a) + 1) + 1):
        e, lb = E_K(a, v, N, K, starts=8)
        rows.append(dict(K=K, eps=(e - ei) / ei, taus=sorted((1 / np.exp(lb)).tolist())))
    ks = {}
    for R in (1, 10, 100, 1e3, 1e4, 1e6):
        costs = [r['K'] + R * (1 + r['eps']) for r in rows]
        ks[str(int(R))] = rows[int(np.argmin(costs))]['K']
    return dict(taus=taus.tolist(), noise=noise_sd, Einf=ei, rows=rows, kstar=ks)


def k_job(args):
    return kstar_profile(*args)


def armK():
    worlds = [[10.0], [1, 10], [1, 10, 100], [1, 10, 100, 1000], [1, 3], [1, 3, 9], [1, 3, 9, 27], [1, 100], [1, 100, 1e3]]
    jobs = [(w, nz) for w in worlds for nz in (0.3, 1.0)]
    with Pool(NPROC) as p:
        res = p.map(k_job, jobs, chunksize=1)
    dump('arm_K.json', res)
    for r in res:
        print(r['taus'], r['noise'], r['kstar'], [round(x['eps'] * 100, 3) for x in r['rows']], flush=True)



# ------------------------------------------------------------------ C: many coupled records (multivariate arm)
def coherence_at(Y, dt, f0, per_decade=4):
    """Mean pairwise magnitude-squared coherence of records Y (M, n) in the log-frequency bin containing f0."""
    M, n = Y.shape
    F = np.fft.rfft(Y - Y.mean(1, keepdims=True), axis=1)[:, 1:]
    f = np.arange(1, F.shape[1] + 1) / (n * dt)
    lo, hi = f0 * 10 ** (-0.5 / per_decade), f0 * 10 ** (0.5 / per_decade)
    sel = (f >= lo) & (f < hi)
    if sel.sum() < 4:
        return np.nan, int(sel.sum())
    Fs = F[:, sel]
    C = Fs @ Fs.conj().T / sel.sum()
    d = np.real(np.diag(C)); cs = []
    for i in range(M):
        for k in range(i + 1, M):
            cs.append(abs(C[i, k]) ** 2 / (d[i] * d[k]))
    return float(np.mean(cs)), int(sel.sum())


def multi_world(name, M, n, dt, rng, noise=0.3):
    """Returns Y (M, n) and the truth: components as (class, tau)."""
    Y = noise * rng.standard_normal((M, n)); comps = []
    def add_local(tau, v):
        for i in range(M):
            Y[i] += H.ou_modes_fast([tau], [v], n, dt, rng)[0]
        comps.append(('local', tau))
    def add_shared(tau, v):
        s = H.ou_modes_fast([tau], [v], n, dt, rng)[0]
        load = 0.7 + 0.6 * rng.random(M)
        Y[:] += load[:, None] * s
        comps.append(('shared', tau))
    v = 1 / 3
    if name == 'C1_independent':   # every signal has its own drivers at the same three rates
        for t in (1, 10, 100): add_local(t, v)
    elif name == 'C2_common_slow':  # one common-mode slow driver, local fast and middle
        add_local(1, v); add_local(10, v); add_shared(100, v)
    elif name == 'C3_both_same_rate':  # a shared and a local driver at the SAME rate (map's "both"), plus local fast
        add_local(1, v); add_local(10, v / 2); add_shared(10, v / 2)
    elif name == 'C4_all_shared':  # three common-mode drivers, nothing local
        for t in (1, 10, 100): add_shared(t, v)
    elif name == 'C5_independent_rates':  # each signal has drivers at its OWN rates (no shared rate)
        for i in range(M):
            for t in (1, 10, 100):
                Y[i] += H.ou_modes_fast([t * 2 ** (i / M * 1.5)], [v], n, dt, rng)[0]
        comps += [('local', 'per-signal rates')]
    return Y, comps


def c_job(args):
    name, seed = args
    rng = np.random.default_rng(seed)
    M, n, dt = 6, 200000, 0.1
    Y, comps = multi_world(name, M, n, dt, rng)
    band = (dt, n * dt / 10)
    per = []
    for i in range(M):
        c, merged, K, _ = H.whittle_pole_count(Y[i], dt, band=band, rng=np.random.default_rng(seed + i))
        per.append(dict(count=int(c), taus=merged.tolist(), ht_absy=H.ht_index(np.abs(Y[i] - Y[i].mean())),
                        ht_per=H.ht_index(H.periodogram(Y[i]))))
    all_taus = np.concatenate([np.array(p['taus']) for p in per if p['taus']]) if any(p['taus'] for p in per) else np.array([])
    union_count, union_taus = H.merge_count(1 / all_taus if all_taus.size else [], (0, np.inf))
    # classify each merged scale by cross-record coherence, then count per class ("both" counts 2)
    classes = []
    for t in union_taus:
        coh, m = coherence_at(Y, dt, 1 / (2 * np.pi * t))
        cl = 'shared' if coh > 0.6 else ('local' if coh < 0.2 else 'both')
        classes.append(dict(tau=float(t), coherence=coh, n_ord=m, cls=cl))
    classified = sum(2 if c['cls'] == 'both' else 1 for c in classes)
    pooled = Y.mean(0)
    pc, ptaus, _, _ = H.whittle_pole_count(pooled, dt, band=band, rng=np.random.default_rng(seed + 99))
    # integrated: multivariate Hankel DMD (stride 10 -> step 1.0, 30 lags), Gavish-Donoho rank, rates merged
    rates, rank, sv = H.hankel_dmd_rates(Y, dt, lags=30, stride=10, max_rank=60)
    dmd_count, dmd_taus = H.merge_count(rates, band)
    return dict(world=name, seed=seed, truth=comps, n_true_components=len(comps) if name != 'C5_independent_rates' else None,
                per_record=per, sum_of_record_counts=int(sum(p['count'] for p in per)),
                median_record_count=float(np.median([p['count'] for p in per])),
                median_ht_absy=float(np.median([p['ht_absy'] for p in per])), median_ht_per=float(np.median([p['ht_per'] for p in per])),
                union_merged=int(union_count), union_taus=union_taus.tolist(), classes=classes, classify_then_merge=int(classified),
                pooled_count=int(pc), pooled_taus=ptaus.tolist(), dmd_rank=int(rank), dmd_count=int(dmd_count), dmd_taus=dmd_taus.tolist(),
                ht_singular_values=H.ht_index(sv), ht_dmd_rates=H.ht_index(rates) if len(rates) > 1 else 1)


def armC():
    jobs = [(w, 5000 + 10 * s + i) for i, w in enumerate(['C1_independent', 'C2_common_slow', 'C3_both_same_rate', 'C4_all_shared', 'C5_independent_rates']) for s in range(3)]
    with Pool(NPROC) as p:
        res = p.map(c_job, jobs, chunksize=1)
    dump('arm_C.json', res)
    for r in res:
        print(r['world'], 'true', r['n_true_components'], 'sum', r['sum_of_record_counts'], 'median', r['median_record_count'], 'union', r['union_merged'],
              'classified', r['classify_then_merge'], [c['cls'] for c in r['classes']], 'pooled', r['pooled_count'], 'dmd_rank', r['dmd_rank'],
              'dmd_count', r['dmd_count'], 'ht_rec', r['median_ht_absy'], r['median_ht_per'], 'ht_sv', r['ht_singular_values'], 'ht_rates', r['ht_dmd_rates'], flush=True)


# ------------------------------------------------------------------ D: records made by sub-agents (nested hypothesis)
D_TAUS = np.array([1.0, 30.0, 900.0]); D_DT = 0.25; D_N = 400000; D_NOISE = 0.5


def agent_record(y, b, g, dt):
    from scipy.signal import lfilter
    rec = np.zeros_like(y)
    for bk, gk in zip(b, g):
        c = 1 - np.exp(-bk * dt)
        rec += gk * lfilter([c], [1, -(1 - c)], y)
    return rec


def io_pole_count(y, rec, dt, Kmax=4):
    """Identify the agent from its input y and output record (the counting rule's I/O pair): fit
    H(f) = sum_k g_k c_k / (1 - (1-c_k) e^{-iw}) to the empirical transfer function, K = 1..Kmax, ΔBIC >= 10."""
    from scipy.optimize import least_squares
    n = len(y); Fy = np.fft.rfft(y)[1:]; Fr = np.fft.rfft(rec)[1:]
    f = np.arange(1, len(Fy) + 1) / (n * dt)
    lf = np.log10(f); edges = np.arange(lf.min(), lf.max() + 1 / 24, 1 / 24); idx = np.digitize(lf, edges)
    fb, Hb, mb = [], [], []
    for bb in np.unique(idx):
        s = idx == bb
        Syy = np.mean(np.abs(Fy[s]) ** 2); Sry = np.mean(Fr[s] * np.conj(Fy[s]))
        fb.append(np.exp(np.mean(np.log(f[s])))); Hb.append(Sry / Syy); mb.append(s.sum())
    fb, Hb, mb = np.array(fb), np.array(Hb), np.array(mb)
    z = np.exp(-2j * np.pi * fb * dt)
    def model(x, K):
        Hm = np.zeros_like(Hb)
        for k in range(K):
            bk = np.exp(x[k]); c = 1 - np.exp(-bk * dt)
            Hm = Hm + x[K + k] * c / (1 - (1 - c) * z)
        return Hm
    wts = np.sqrt(mb)
    best_bic, bestK, fits = np.inf, 0, {}
    rng = np.random.default_rng(3)
    for K in range(1, Kmax + 1):
        bestr = None
        for s in range(6):
            x0 = np.concatenate([np.sort(rng.uniform(np.log(1 / 3000), np.log(5), K)), np.full(K, 1.0 / K)])
            r = least_squares(lambda x: np.concatenate([wts * (model(x, K) - Hb).real, wts * (model(x, K) - Hb).imag]), x0)
            if bestr is None or r.cost < bestr.cost:
                bestr = r
        rss = 2 * bestr.cost; m = 2 * len(Hb)
        bic = m * np.log(rss / m + 1e-300) + 2 * K * np.log(m)
        fits[K] = (bic, np.sort(1 / np.exp(bestr.x[:K])))
        if bic < best_bic - 10:
            best_bic, bestK = bic, K
    return bestK, fits[bestK][1] if bestK else np.array([])


def interlaced(store_taus, mode_taus):
    """CT21/B.9 signature for K = J: sorted store j is faster than mode j and slower than mode j-1."""
    s = np.sort(store_taus); m = np.sort(mode_taus)
    if len(s) != len(m):
        return None
    return bool(all(s[j] < m[j] and (j == 0 or s[j] > m[j - 1]) for j in range(len(m))))


def d_job(args):
    label, b, g, seed = args
    rng = np.random.default_rng(seed)
    y = H.ou_modes_fast(D_TAUS, np.ones(3) / 3, D_N, D_DT, rng).sum(0) + D_NOISE * rng.standard_normal(D_N)
    rec = agent_record(y, b, g, D_DT) + 0.01 * rng.standard_normal(D_N)
    c, merged, K, _ = H.whittle_pole_count(rec, D_DT, band=(D_DT, D_N * D_DT / 10), rng=np.random.default_rng(seed))
    _, _, h = H.mfdfa(rec, qs=(-3, 2, 5))
    kio, tio = io_pole_count(y, rec, D_DT)
    return dict(label=label, K_agent=len(b), store_taus=sorted((1 / np.asarray(b)).tolist()), seed=seed,
                ht_absdrec=H.ht_index(np.abs(np.diff(rec))), ht_absrec=H.ht_index(np.abs(rec - rec.mean())),
                ht_per=H.ht_index(H.periodogram(rec)), ht_cross=H.ht_index(H.crossing_durations(rec)),
                whittle_record=int(c), whittle_taus=merged.tolist(), dfa_h=float(h[1]), mf_width=float(h[0] - h[2]),
                io_count=int(kio), io_taus=np.asarray(tio).tolist(), interlaced=interlaced(1 / np.asarray(b), D_TAUS))


def armD():
    a = 1 / D_TAUS; v = np.ones(3) / 3; N = D_NOISE ** 2 * D_DT
    ei = E_inf(a, v, N)
    designs = {}
    for K in (1, 2, 3):
        e, lb = E_K(a, v, N, K, starts=10)
        b = np.exp(lb); _, g = mse_given_b(a, v, b, N)
        designs[K] = dict(b=b, g=g, eps=(e - ei) / ei)
    ks = {}
    for R in (1, 10, 100, 1e3, 1e4, 1e6):
        ks[str(int(R))] = min(designs, key=lambda K: K + R * (1 + designs[K]['eps']))
    print('D: K* by R', ks, 'eps', {K: round(d['eps'] * 100, 3) for K, d in designs.items()}, 'store taus', {K: np.round(1 / d['b'], 2).tolist() for K, d in designs.items()}, flush=True)
    jobs = []; seed = 9000
    for K in (1, 2, 3):
        for s in range(4):
            jobs.append((f'opt_K{K}', designs[K]['b'], designs[K]['g'], seed)); seed += 1
    rng = np.random.default_rng(77); null_meta = []
    for i in range(24):
        K = int(rng.integers(1, 4))
        b = np.exp(rng.uniform(np.log(1 / (3 * D_TAUS.max())), np.log(3 / D_TAUS.min()), K))
        _, g = mse_given_b(a, v, b, N)
        e, _ = mse_given_b(a, v, b, N)
        null_meta.append(dict(K=K, eps=(e - ei) / ei))
        jobs.append((f'rand_K{K}', b, g, seed)); seed += 1
    with Pool(NPROC) as p:
        res = p.map(d_job, jobs, chunksize=1)
    dump('arm_D.json', dict(kstar=ks, designs={K: dict(store_taus=(1 / d['b']).tolist(), g=d['g'].tolist(), eps=d['eps']) for K, d in designs.items()},
                            null_eps=null_meta, records=res))
    for r in res:
        print(r['label'], 'ht', r['ht_absdrec'], r['ht_absrec'], r['ht_per'], r['ht_cross'], 'whittle', r['whittle_record'], np.round(r['whittle_taus'], 2),
              'io', r['io_count'], np.round(r['io_taus'], 2), 'H', round(r['dfa_h'], 2), 'mfw', round(r['mf_width'], 2), 'interl', r['interlaced'], flush=True)


if __name__ == '__main__':
    for a in (sys.argv[1:] or ['A', 'B', 'K', 'C', 'D']):
        globals()['arm' + a]()
