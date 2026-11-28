"""C3B-GATE-ADDENDUM (pick 31): MV10 status of the locked C3b mechanism verdict at the real pre-shock n.
Own code (does not import tests/C3b/code). Re-implements the locked decision rules of tests/C3b/PREREG.md sec. 6
(mechanism verdict): HIT = H1 beta_tau 95% lo > 0 AND H2 interaction 95% lo > 0 AND S9 beta_tau 90% lo > 0;
MISS = K1 (H1 beta_tau 95% hi < 0.15) OR K2 (H2 interaction 95% hi < 0). Data-generating process: the prereg's own
assumed covariate structure (PREREG sec. 5 / power.py), written out independently here, with a switch for the
latent-activity confounder. Plain (non-clustered) SEs: 2,116 unique repos in 2,294 rows, so clustering changes little
and can only widen CIs (lowers P(HIT) and P(K1); the gate verdict below would not improve).
Usage: python3 gate_sim.py N REPS SEED  -> JSON line per scenario."""
import sys, json, numpy as np, pandas as pd, statsmodels.formula.api as smf, warnings
warnings.filterwarnings('ignore')
N, REPS, SEED = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
L365 = np.log(365)
def draw(rng, n, bt, bi, conf=True, p0=0.30):
    shock = rng.choice(['numpy', 'pydantic', 'sqlalchemy', 'pandas', 'urllib3'], n)
    lB = np.log(rng.integers(1, 15, n)); lE = np.log(np.clip(rng.beta(1, 4, n), 0.005, None))
    act = rng.normal(0, 1, n) if conf else np.zeros(n)
    ltau = np.clip(4.0 - 0.6 * act + rng.normal(0, 1.1, n), 0, L365)
    lcom = np.clip(3 + 0.9 * act + rng.normal(0, .8, n), 0, None); lrel = np.clip(1.5 + .5 * act + rng.normal(0, .5, n), 0, None)
    lage = rng.normal(8, .5, n)
    eta = np.log(p0 / (1 - p0)) + bt * (ltau - 4) - .4 * (lB - 1.5) + .1 * (lE + 2) - .3 * act
    lEB = lE - lB
    p = 1 / (1 + np.exp(-eta)) + bi * (ltau - ltau.mean()) * (lEB - lEB.mean())
    D = (rng.random(n) < np.clip(p, .01, .99)).astype(int)
    llat = np.clip(ltau - rng.exponential(.5, n), 0, L365)
    df = pd.DataFrame(dict(D=D, ltau=ltau, lE=lE, lB=lB, lcommits=np.log1p(np.round(np.expm1(lcom))),
                           lrel=np.log1p(np.round(np.expm1(lrel))), lage=lage, llat=llat, shock=shock))
    df['c_ltau'] = df.ltau - df.ltau.mean(); df['c_lEB'] = (df.lE - df.lB) - (df.lE - df.lB).mean()
    return df
CTRL = 'lcommits + lrel + lage + C(shock)'
def verdict(df):
    h1 = smf.logit(f'D ~ ltau + lE + lB + {CTRL}', df).fit(disp=0, maxiter=200)
    lo1, hi1 = h1.conf_int().loc['ltau']; se1 = h1.bse['ltau']
    h2 = smf.ols(f'D ~ c_ltau * c_lEB + {CTRL}', df).fit(cov_type='HC1')
    lo2, hi2 = h2.conf_int().loc['c_ltau:c_lEB']
    s9 = smf.logit(f'D ~ ltau + llat + lE + lB + {CTRL}', df).fit(disp=0, maxiter=200)
    lo9 = s9.conf_int(alpha=0.10).loc['ltau'][0]
    hit = lo1 > 0 and lo2 > 0 and lo9 > 0
    k1, k2 = hi1 < 0.15, hi2 < 0
    return dict(hit=hit, miss=k1 or k2, k1=k1, k2=k2, h1=lo1 > 0, h2=lo2 > 0, s9=lo9 > 0, se1=se1, b1=h1.params['ltau'])
scen = [('theory', .25, .03, True), ('sesoi', .15, .015, True), ('null_conf', 0, 0, True), ('null_noconf', 0, 0, False),
        ('theory_noconf', .25, .03, False)]
for name, bt, bi, conf in scen:
    rng = np.random.default_rng(SEED + hash(name) % 1000)
    acc = []
    for _ in range(REPS):
        try: acc.append(verdict(draw(rng, N, bt, bi, conf)))
        except Exception: pass
    a = pd.DataFrame(acc)
    out = {'n': N, 'scenario': name, 'b_tau': bt, 'b_int': bi, 'confounder': conf, 'reps_ok': len(a)}
    out.update({f'P_{k}': round(float(a[k].mean()), 3) for k in ['hit', 'miss', 'k1', 'k2', 'h1', 'h2', 's9']})
    out['median_se_btau'] = round(float(a.se1.median()), 4); out['mean_btau_hat'] = round(float(a.b1.mean()), 4)
    print(json.dumps(out), flush=True)
