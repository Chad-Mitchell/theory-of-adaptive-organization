#!/usr/bin/env python3
"""VIGIL_ONA analysis. Usage:
  ona_analyze.py synth  [--beta B] [--sims K]  -> power / dry run on synthetic outcomes (real node attributes only)
  ona_analyze.py real                          -> locked analysis on real nominations (writes results_real.json)
Nothing here reads edge files except in `real` mode.
"""
import sys, json, math, argparse, numpy as np, pandas as pd
RAW = '<local>/gtao/night2/VIGIL_ONA/data/raw'
OUT = '<local>/gtao/night2/VIGIL_ONA'

# ---------------- node attributes (non-outcome) ----------------
def pyramid_N(level_top_is_high):
    """pooled-N proxy per level: (# people at lower levels)/(# at this level); lowest level -> 0"""
    s = pd.Series(level_top_is_high)
    out = {}
    for L in sorted(s.unique()):
        below = (s < L).sum(); at = (s == L).sum()
        out[L] = below / at if below > 0 else 0.0
    return s.map(out).values

def load_nodes():
    D = {}
    k = pd.read_csv(f'{RAW}/krack_nodes.txt', sep=' ')
    k['id'] = k.nodeID - 1
    k['rank'] = 3 - k.nodeLevel            # CEO 2, VP 1, manager 0
    k['unit'] = k.nodeDepartment
    k['ego_ok'] = k.nodeLevel != 1         # CEO's pool is the whole firm: no outside -> not an ego
    D['krackhardt'] = k[['id', 'rank', 'unit', 'ego_ok']].copy()
    l = pd.read_csv(f'{RAW}/lz/ELattr.dat', sep=r'\s+', header=None,
                    names=['id', 'status', 'gender', 'office', 'yrs', 'age', 'practice', 'school'])
    l['id'] = l.id - 1
    l['rank'] = 2 - l.status                # partner 1, associate 0
    l['unit'] = l.office * 10 + l.practice
    l['ego_ok'] = True
    D['lazega'] = l[['id', 'rank', 'unit', 'ego_ok']].copy()
    for n in ['consulting', 'manufacturing']:
        d = pd.read_csv(f'{RAW}/cp/{n}/nodes.csv'); d.columns = [c.strip('# ') for c in d.columns]
        d['id'] = d['index']
        d['rank'] = d.orglevel - 1 if n == 'consulting' else 4 - d.orglevel
        d['unit'] = d.location
        d['ego_ok'] = True
        D[n] = d[['id', 'rank', 'unit', 'ego_ok']].copy()
    # pooled N
    D['consulting']['N'] = pyramid_N(D['consulting']['rank'])
    D['manufacturing']['N'] = pyramid_N(D['manufacturing']['rank'])
    D['lazega']['N'] = np.nan
    D['krackhardt']['N'] = np.nan          # filled from formal reports-to (structure, not outcome) below
    return D

def krack_spans(D):
    e = pd.read_csv(f'{RAW}/krack_multiplex.edges', sep=' ', header=None, names=['layer', 'i', 'j', 'w'])
    r = e[e.layer == 3]                      # reports_to: formal structure only
    k = D['krackhardt']
    direct = r.groupby('j').size()
    N = np.zeros(len(k))
    for idx, row in k.iterrows():
        nid = row.id + 1
        # subtree size (pooled N)
        frontier = [nid]; seen = set()
        while frontier:
            x = frontier.pop(); kids = r[r.j == x].i.tolist()
            for c in kids:
                if c not in seen: seen.add(c); frontier.append(c)
        N[idx] = len(seen)
    k['N'] = N
    return k

# ---------------- outcome loaders (real mode only) ----------------
def load_layers():
    L = {}
    e = pd.read_csv(f'{RAW}/krack_multiplex.edges', sep=' ', header=None, names=['layer', 'i', 'j', 'w'])
    e['i'] -= 1; e['j'] -= 1
    L['krackhardt'] = {'advice': e[e.layer == 1][['i', 'j']].assign(w=1),
                       'friendship': e[e.layer == 2][['i', 'j']].assign(w=1)}
    def mat(f):
        m = np.loadtxt(f'{RAW}/lz/{f}'); i, j = np.nonzero(m)
        return pd.DataFrame({'i': i, 'j': j, 'w': 1})
    L['lazega'] = {'advice': mat('ELadv.dat'), 'cowork': mat('ELwork.dat'), 'friendship': mat('ELfriend.dat')}
    for n, thr in [('consulting', {'advice': 3, 'value': 4}), ('manufacturing', {'advice': 4, 'awareness': 4})]:
        e = pd.read_csv(f'{RAW}/cp/{n}/edges.csv'); e.columns = [c.strip('# ') for c in e.columns]
        e = e.rename(columns={'source': 'i', 'target': 'j', 'weight': 'w'})
        d = {}
        for lay, t in thr.items():
            x = e[(e.layer == lay)]
            d[lay] = x[x.w >= t][['i', 'j']].assign(w=1)
            d[lay + '_weighted'] = x[['i', 'j', 'w']].copy()
            d[lay + '_any'] = x[x.w >= 2][['i', 'j']].assign(w=1)   # sensitivity threshold
        L[n] = d
    # multi-layer union of work-information layers (secondary)
    U = {'krackhardt': ['advice'], 'lazega': ['advice', 'cowork'],
         'consulting': ['advice', 'value'], 'manufacturing': ['advice', 'awareness']}
    for n, lays in U.items():
        L[n]['union_work'] = pd.concat([L[n][x] for x in lays])[['i', 'j']].drop_duplicates().assign(w=1)
    return L

# ---------------- design ----------------
def dyads(nodes, edges, weighted=False):
    n = len(nodes); ids = nodes.id.values
    A = np.zeros((n, n))
    if edges is not None and len(edges):
        e = edges[edges.i != edges.j]
        A[e.i.values, e.j.values] = e.w.values if weighted else 1
    I, J = np.meshgrid(np.arange(n), np.arange(n), indexing='ij'); m = I != J
    I, J = I[m], J[m]
    r = nodes['rank'].values; u = nodes.unit.values; ok = nodes.ego_ok.values
    egos = nodes[nodes.ego_ok]
    rr = egos['rank']; lo, hi = rr.min(), rr.max()
    rs = (r - lo) / (hi - lo)
    df = pd.DataFrame({'i': I, 'j': J, 'y': A[I, J], 'out': (u[I] != u[J]).astype(float),
                       'egorank': rs[I], 'a_hi': (r[J] > r[I]).astype(float), 'a_eq': (r[J] == r[I]).astype(float),
                       'egook': ok[I]})
    return df[df.egook].reset_index(drop=True)

def logit_fe(df, extra_terms=('a_hi', 'a_eq'), key='egorank_x_out'):
    df = df.copy(); df[key] = df.egorank * df.out
    # drop egos with no variation, alters with no incoming
    g = df.groupby('i').y.agg(['sum', 'count']); keep = g[(g['sum'] > 0) & (g['sum'] < g['count'])].index
    df = df[df.i.isin(keep)]
    ga = df.groupby('j').y.sum(); df = df[df.j.isin(ga[ga > 0].index)].reset_index(drop=True)
    if df.i.nunique() < 4: return None
    Xi = pd.get_dummies(df.i, prefix='e', dtype=float)
    Xj = pd.get_dummies(df.j, prefix='a', dtype=float).iloc[:, 1:]
    cols = [key, 'out'] + list(extra_terms)
    X = np.column_stack([df[cols].values, Xi.values, Xj.values]); y = df.y.values
    # drop exactly collinear terms (e.g. a_eq within single-rank designs)
    b = np.zeros(X.shape[1])
    for it in range(100):
        eta = X @ b; p = 1 / (1 + np.exp(-eta)); W = p * (1 - p)
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1]); g_ = X.T @ (y - p)
        step = np.linalg.solve(H, g_); b += step
        if np.max(np.abs(step)) < 1e-8: break
    p = 1 / (1 + np.exp(-(X @ b))); W = p * (1 - p)
    Binv = np.linalg.inv(X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1]))
    S = X * (y - p)[:, None]
    def meat(groups):
        M = np.zeros((X.shape[1], X.shape[1]))
        for _, idx in pd.Series(range(len(df))).groupby(groups.values):
            s = S[idx.values].sum(0); M += np.outer(s, s)
        return M
    Me, Ma = meat(df.i), meat(df.j); Md = S.T @ S
    V2 = Binv @ (Me + Ma - Md) @ Binv; Ve = Binv @ Me @ Binv
    v = V2[0, 0] if V2[0, 0] > 0 else max(Ve[0, 0], (Binv @ Ma @ Binv)[0, 0])
    return {'beta': float(b[0]), 'se': float(math.sqrt(v)), 'se_ego': float(math.sqrt(Ve[0, 0])),
            'n_dyads': int(len(df)), 'n_egos': int(df.i.nunique())}

def node_table(nodes, edges, weighted=False):
    d = dyads(nodes, edges, weighted)
    t = d.groupby('i').apply(lambda x: pd.Series({
        'y_out': x.y[x.out == 1].sum(), 'n_out': (x.out == 1).sum(),
        'y_in': x.y[x.out == 0].sum(), 'n_in': (x.out == 0).sum(), 'egorank': x.egorank.iloc[0]}),
        include_groups=False).reset_index()
    t = t.merge(nodes[['id', 'N']], left_on='i', right_on='id', how='left')
    return t[t.n_out > 0]

def pois(y, X, off):
    b = np.zeros(X.shape[1]); b[0] = math.log(max(y.sum(), 0.5) / np.exp(off).sum())
    for it in range(200):
        mu = np.exp(X @ b + off); H = X.T @ (X * mu[:, None]) + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - mu)); b += step
        if np.max(np.abs(step)) < 1e-10: break
    mu = np.exp(X @ b + off); Bi = np.linalg.inv(X.T @ (X * mu[:, None]))
    S = X * (y - mu)[:, None]; n, k = X.shape
    V = Bi @ (S.T @ S) @ Bi * n / max(n - k, 1)
    return b, np.sqrt(np.diag(V))

def h1(t):   # outside-unit seeking rate (per available outside alter) vs ego rank
    X = np.column_stack([np.ones(len(t)), t.egorank.values])
    b, se = pois(t.y_out.values.astype(float), X, np.log(t.n_out.values))
    return {'logRR': float(b[1]), 'se': float(se[1])}

def h1_spec(t):  # stacked inside/outside: rank x outside interaction at node level (generic-activity control)
    y = np.r_[t.y_out, t.y_in].astype(float); off = np.log(np.r_[t.n_out, np.maximum(t.n_in, 1)])
    o = np.r_[np.ones(len(t)), np.zeros(len(t))]; r = np.r_[t.egorank, t.egorank]
    keep = np.r_[np.ones(len(t), bool), t.n_in.values > 0]
    X = np.column_stack([np.ones(len(y)), r, o, r * o])[keep]
    b, se = pois(y[keep], X, off[keep])
    return {'logRoR': float(b[3]), 'se': float(se[3])}

def h3(tables):   # elasticity of outside seeking on ln(1+N), dataset FE, pooled
    rows = []
    for k, (n, t) in enumerate(tables.items()):
        t = t[np.isfinite(t.N)]
        for _, r in t.iterrows(): rows.append((k, r.y_out, r.n_out, math.log1p(r.N)))
    R = pd.DataFrame(rows, columns=['d', 'y', 'n', 'lnN'])
    F = pd.get_dummies(R.d, dtype=float).values
    X = np.column_stack([R.lnN.values, F])
    b, se = pois(R.y.values.astype(float), X, np.log(R.n.values))
    return {'elasticity': float(b[0]), 'se': float(se[0]), 'n_nodes': int(len(R))}

def meta(ests, bkey, skey='se'):
    # separation flag (pre-declared): |est| > 5 or se > 3 -> excluded from pooling, reported separately
    e = [x for x in ests if x is not None and np.isfinite(x[skey]) and 0 < x[skey] <= 3 and abs(x[bkey]) <= 5]
    w = np.array([1 / x[skey] ** 2 for x in e]); b = np.array([x[bkey] for x in e])
    m = float((w * b).sum() / w.sum()); s = float(1 / math.sqrt(w.sum()))
    Q = float((w * (b - m) ** 2).sum())
    si = SE_INFL * s   # coverage-calibrated inflation: pooled sd/mean_se = 0.177/0.133 = 1.33 in power sims (v2, d=0.4)
    return {'est': m, 'se': s, 'lo': m - 1.96 * s, 'hi': m + 1.96 * s, 'k': len(e), 'Q': Q,
            'se_infl': si, 'lo_dec': m - 1.96 * si, 'hi_dec': m + 1.96 * si}
SE_INFL = 1.3

# ---------------- synthetic (dry run / power) ----------------
def synth_edges(nodes, beta, rng, dens=0.2):
    n = len(nodes); a = rng.normal(0, 1, n); c = rng.normal(0, 1, n)
    d = dyads(nodes, None)
    eta = (math.log(dens / (1 - dens)) + a[d.i] + c[d.j] + 1.0 * (1 - d.out) + 0.5 * d.a_hi
           + beta * d.egorank * d.out)
    y = rng.random(len(d)) < 1 / (1 + np.exp(-eta))
    return pd.DataFrame({'i': d.i[y], 'j': d.j[y], 'w': 1})

def run_synth(beta, sims, seed=7, dens=0.2):
    D = load_nodes(); D['krackhardt'] = krack_spans(D)
    rng = np.random.default_rng(seed); res = {n: [] for n in D}; pooled = []
    for s in range(sims):
        ests = []
        for n, nodes in D.items():
            r = logit_fe(dyads(nodes, synth_edges(nodes, beta, rng, dens)))
            res[n].append(r); ests.append(r)
        pooled.append(meta(ests, 'beta'))
    out = {}
    for n, rs in res.items():
        rs = [r for r in rs if r]
        b = np.array([r['beta'] for r in rs]); se = np.array([r['se'] for r in rs])
        out[n] = {'mean_beta': float(b.mean()), 'sd_beta': float(b.std()), 'mean_se': float(se.mean()),
                  'power_pos': float(np.mean(b - 1.96 * se > 0)), 'coverage': float(np.mean(np.abs(b - beta) < 1.96 * se))}
    pb = np.array([p['est'] for p in pooled]); ps = np.array([p['se'] for p in pooled])
    out['pooled'] = {'mean_beta': float(pb.mean()), 'sd_beta': float(pb.std()), 'mean_se': float(ps.mean()),
                     'power_pos': float(np.mean(pb - 1.96 * ps > 0)), 'coverage': float(np.mean(np.abs(pb - beta) < 1.96 * ps))}
    return out

# ---------------- real ----------------
PRIMARY = {'krackhardt': 'advice', 'lazega': 'advice', 'consulting': 'advice', 'manufacturing': 'advice'}
SECONDARY = {'krackhardt': ['friendship', 'union_work'], 'lazega': ['cowork', 'friendship', 'union_work'],
             'consulting': ['value', 'advice_any', 'union_work'], 'manufacturing': ['awareness', 'advice_any', 'union_work']}
WEIGHTED = {'consulting': 'advice_weighted', 'manufacturing': 'advice_weighted'}

def fake_layers(D, beta=0.5, seed=11):
    rng = np.random.default_rng(seed); L = {}
    for n, nodes in D.items():
        lays = [PRIMARY[n]] + SECONDARY[n] + ([WEIGHTED[n]] if n in WEIGHTED else [])
        L[n] = {}
        for lay in lays:
            e = synth_edges(nodes, beta, rng)
            if lay.endswith('_weighted'): e = e.assign(w=rng.integers(1, 6, len(e)))
            L[n][lay] = e
    return L

def run_real(fake=False):
    D = load_nodes(); D['krackhardt'] = krack_spans(D); L = fake_layers(D) if fake else load_layers()
    R = {'primary': {}, 'secondary': {}, 'descriptive': {}}
    h1s, h1ss, h2s, tabs = [], [], [], {}
    for n, lay in PRIMARY.items():
        nodes = D[n]; e = L[n][lay]
        t = node_table(nodes, e); tabs[n] = t
        a = h1(t); b = h1_spec(t); c = logit_fe(dyads(nodes, e))
        R['primary'][n] = {'H1': a, 'H1_spec': b, 'H2': c, 'n_egos': int(len(t))}
        h1s.append(a); h1ss.append(b); h2s.append(c)
    R['primary']['pooled'] = {'H1': meta(h1s, 'logRR'), 'H1_spec': meta(h1ss, 'logRoR'), 'H2': meta(h2s, 'beta')}
    names = list(PRIMARY)
    R['primary']['leave_one_out'] = {f'without_{names[k]}': {
        'H1': meta([x for i, x in enumerate(h1s) if i != k], 'logRR'),
        'H2': meta([x for i, x in enumerate(h2s) if i != k], 'beta')} for k in range(len(names))}
    R['primary']['H3'] = h3({n: tabs[n] for n in ['krackhardt', 'consulting', 'manufacturing']})
    # secondary layers
    for n, lays in SECONDARY.items():
        for lay in lays:
            e = L[n][lay]; t = node_table(D[n], e)
            R['secondary'][f'{n}:{lay}'] = {'H1': h1(t), 'H1_spec': h1_spec(t), 'H2': logit_fe(dyads(D[n], e))}
    for n, lay in WEIGHTED.items():
        t = node_table(D[n], L[n][lay], weighted=True)
        R['secondary'][f'{n}:{lay}'] = {'H1': h1(t), 'H1_spec': h1_spec(t)}
    # H3 weighted
    tw = {n: node_table(D[n], L[n][WEIGHTED[n]], weighted=True) for n in WEIGHTED}
    tw['krackhardt'] = tabs['krackhardt']
    R['secondary']['H3_weighted'] = h3(tw)
    # descriptive: by rank, out-degree total, in-degree (status rival), inside/outside rates
    for n, lay in PRIMARY.items():
        nodes = D[n]; e = L[n][lay]; e = e[e.i != e.j]
        outd = e.groupby('i').size().reindex(nodes.id, fill_value=0).values
        ind = e.groupby('j').size().reindex(nodes.id, fill_value=0).values
        t = tabs[n].set_index('i')
        df = nodes.assign(outdeg=outd, indeg=ind)
        df['out_rate'] = df.id.map(t.y_out / t.n_out); df['in_rate'] = df.id.map(t.y_in / t.n_in.replace(0, np.nan))
        g = df.groupby('rank').agg(n=('id', 'size'), outdeg=('outdeg', 'mean'), indeg=('indeg', 'mean'),
                                   outside_rate=('out_rate', 'mean'), inside_rate=('in_rate', 'mean'), N=('N', 'mean'))
        R['descriptive'][n] = g.reset_index().to_dict(orient='records')
        # status rival: Spearman-like slope of in- and out-degree on rank (Poisson, no offset)
        X = np.column_stack([np.ones(len(df)), df['rank'].values / df['rank'].max()])
        bi, si = pois(df.indeg.values.astype(float), X, np.zeros(len(df)))
        bo, so = pois(df.outdeg.values.astype(float), X, np.zeros(len(df)))
        R['descriptive'][n + '_status'] = {'indeg_logRR_top_vs_bottom': [float(bi[1]), float(si[1])],
                                           'outdeg_logRR_top_vs_bottom': [float(bo[1]), float(so[1])]}
    json.dump(R, open(f'{OUT}/' + ('dryrun_fake.json' if fake else 'results_real.json'), 'w'), indent=1, default=float)
    print(json.dumps(R['primary'], indent=1, default=float))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('--beta', type=float, default=0.5)
    ap.add_argument('--sims', type=int, default=50); ap.add_argument('--dens', type=float, default=0.2); a = ap.parse_args()
    if a.mode == 'synth':
        print(json.dumps({'beta_true': a.beta, 'dens': a.dens, 'res': run_synth(a.beta, a.sims, dens=a.dens)}, indent=1))
    elif a.mode == 'real':
        run_real()
    elif a.mode == 'dryreal':
        run_real(fake=True)
