"""Forking-path and reproduction checks for LEARNSIM RA / RR / AA (referee)."""
import json, sys, os
import numpy as np
sys.path.insert(0, '<local>/gtao/night2/LEARNSIM')
os.chdir('<local>/gtao/night2/LEARNSIM')
import analyze as A

R = A.load('results_es.jsonl')
for k,v in A.load('results_ext.jsonl').items():
    R[k] = v
P2 = json.load(open('PREDICTIONS_2.json'))
TH = json.load(open('THEORY_PREDICTIONS.json'))
out = {}

def run_scan(arm, rhos, seed=2027, key='D_rel'):
    rng = np.random.default_rng(seed)
    o, data, est, boots = A.scan(R, 'es', arm, rhos, key, rng)
    bs = o.pop('boot_slopes', None)
    return o, data, est, bs

def verdict(e, lo, hi, pred, tol=0.15):
    if abs(e - pred) <= tol * abs(pred):
        return 'PASS'
    if not (lo <= pred <= hi):
        return 'MISS'
    return 'INCONCLUSIVE'

def rival_killed(e, lo, hi, er):
    return bool(not (lo <= er <= hi) and abs(e - er) > 0.3)

# ---- Official RA gated set (locked) ----
ra_rhos = P2['arms']['RA']['gated_rhos']
o, data, est, bs = run_scan('RA', ra_rhos, 2027)
out['RA_official'] = {k: o.get(k) for k in ['e_hat','e_ci','valid_rhos','Nstar_hat','nseeds','boot_dropped']}
idx = [ra_rhos.index(x) for x in o['valid_rhos']]
ep = float(np.polyfit(np.log(o['valid_rhos']), np.log([P2['arms']['RA']['Nstar_pred'][i] for i in idx]), 1)[0])
er = float(np.polyfit(np.log(o['valid_rhos']), np.log([P2['arms']['RA']['Nstar_rival'][i] for i in idx]), 1)[0])
se = float(np.std(bs))
out['RA_official'].update(e_pred=ep, e_rival=er, se=se,
    verdict=A.verdict(o['e_hat'], *o['e_ci'], ep),
    rival_killed=rival_killed(o['e_hat'], *o['e_ci'], er),
    MV8=bool(se <= abs(ep-er)/2.8),
    abs_err=abs(o['e_hat']-ep), tol=0.15*abs(ep),
    Nstar_pred={str(r): P2['arms']['RA']['Nstar_pred'][ra_rhos.index(r)] for r in o['valid_rhos']})

# leave-one-rho-out on official valid set
loor = {}
valid = list(o['valid_rhos'])
for drop in valid:
    sub = [r for r in ra_rhos if r != drop]
    o2,_,_,bs2 = run_scan('RA', sub, 2027)
    if 'e_hat' not in o2 or len(o2['valid_rhos']) < 2:
        loor[str(drop)] = dict(status='too few', valid=o2.get('valid_rhos'))
        continue
    v = o2['valid_rhos']
    id2 = [ra_rhos.index(x) for x in v]
    ep2 = float(np.polyfit(np.log(v), np.log([P2['arms']['RA']['Nstar_pred'][i] for i in id2]), 1)[0])
    er2 = float(np.polyfit(np.log(v), np.log([P2['arms']['RA']['Nstar_rival'][i] for i in id2]), 1)[0])
    span = np.log10(max(v)/min(v))
    loor[f'drop_{drop}'] = dict(e_hat=o2['e_hat'], e_ci=o2['e_ci'], valid=v, span_dec=span,
        e_pred=ep2, verdict=verdict(o2['e_hat'], *o2['e_ci'], ep2),
        rival_killed=rival_killed(o2['e_hat'], *o2['e_ci'], er2),
        gate_ok=bool(len(v)>=3 and span>=0.6),
        se=float(np.std(bs2)), MV8=bool(np.std(bs2) <= abs(ep2-er2)/2.8))
out['RA_leave_one_rho'] = loor

# include 0.08 (below the locked A-member gate 0.12) and 0.04
for extra, label in [([0.08]+ra_rhos, 'plus_0.08'), ([0.04,0.08]+ra_rhos, 'plus_0.04_0.08')]:
    o2,_,_,bs2 = run_scan('RA', extra, 2027)
    v=o2.get('valid_rhos',[])
    # predictions only defined on gated rhos in P2; for extra, compute slope only on those in P2, or skip pred
    if 'e_hat' in o2 and len(v)>=2:
        # window pred from measured laws via P2 where available; else report e_hat only
        common=[r for r in v if r in ra_rhos]
        rec=dict(e_hat=o2['e_hat'], e_ci=o2['e_ci'], valid=v, n_valid=len(v))
        if len(common)>=2:
            id2=[ra_rhos.index(x) for x in common]
            # if valid != common, e_hat is over a different set; also compute over common only already in official
        rec['rival_killed_vs_locked_rival']=rival_killed(o2['e_hat'], *o2['e_ci'], P2['arms']['RA']['e_rival_window'])
        rec['verdict_vs_locked_window_pred']=verdict(o2['e_hat'], *o2['e_ci'], P2['arms']['RA']['e_pred_window'])
        rec['verdict_vs_asym_level']=verdict(o2['e_hat'], *o2['e_ci'], P2['arms']['RA']['e_asym_level_class'])
        out[f'RA_{label}']=rec

# alternative estimators on official rhos
lnN_store = {}
alt = {}
# no PAVA: raw mean crossing
def crossing_raw(lnN, m):
    if m[0] >= 0 or m[-1] < 0: return None
    neg = np.where(m < 0)[0]
    if len(neg)==0: return None
    j = neg[-1]
    if j >= len(m)-1: return None
    return lnN[j] + (0-m[j])/(m[j+1]-m[j]) * (lnN[j+1]-lnN[j])

def scan_custom(arm, rhos, crossfn, seed=2027):
    rng=np.random.default_rng(seed)
    data={}
    for r in rhos:
        runs=R.get(('es',arm,'rho=%g'%r),[])
        if not runs: continue
        lnN=np.log([x['N'] for x in runs[0]['rows']])
        M=A.mat(runs,'D_rel')
        data[r]=(lnN,M)
    est={r: crossfn(lnN, M.mean(0)) for r,(lnN,M) in data.items()}
    B=2000
    boots={r:[] for r in data}
    for b in range(B):
        for r,(lnN,M) in data.items():
            idx=rng.integers(M.shape[0], size=M.shape[0])
            boots[r].append(crossfn(lnN, M[idx].mean(0)))
    valid=[r for r in data if est[r] is not None and np.mean([x is not None for x in boots[r]])>=0.9]
    rec={'Nstar_hat':{str(r):(float(np.exp(est[r])) if est[r] is not None else None) for r in data}, 'valid':valid}
    if len(valid)>=2:
        e=float(np.polyfit(np.log(valid), [est[r] for r in valid], 1)[0])
        bs=[]
        for b in range(B):
            ys=[boots[r][b] for r in valid]
            if any(y is None for y in ys): continue
            bs.append(float(np.polyfit(np.log(valid), ys, 1)[0]))
        rec.update(e_hat=e, e_ci=A.ci(bs), n_boot=len(bs))
    return rec

alt['no_PAVA'] = scan_custom('RA', ra_rhos, crossing_raw)
# first upward crossing of RAW (non-isotonic) seed-mean, no 90% validity (just point)
# already above
# logistic N50 slope
rng=np.random.default_rng(2027)
l50={}
for r in ra_rhos:
    runs=R.get(('es','RA','rho=%g'%r),[])
    if not runs: continue
    lnN=np.log([x['N'] for x in runs[0]['rows']])
    M=A.mat(runs)
    l50[r]=A.logistic_n50(lnN, M>0)
vv=[r for r in ra_rhos if l50.get(r) is not None]
if len(vv)>=2:
    alt['logistic_N50']=dict(N50={str(r):(float(np.exp(l50[r])) if l50[r] is not None else None) for r in ra_rhos},
                             slope=float(np.polyfit(np.log(vv),[l50[r] for r in vv],1)[0]), valid=vv)
# D_rel_ind (no CRN)
o_ind,_,_,_ = run_scan('RA', ra_rhos, 2027, 'D_rel_ind')
alt['no_CRN']= {k:o_ind.get(k) for k in ['e_hat','e_ci','valid_rhos','Nstar_hat']}
if 'e_hat' in o_ind:
    alt['no_CRN']['verdict_vs_official_pred']=verdict(o_ind['e_hat'], *o_ind['e_ci'], ep)
    alt['no_CRN']['rival_killed']=rival_killed(o_ind['e_hat'], *o_ind['e_ci'], er)
out['RA_alt_estimators']=alt

# alternative predictions: asymptotic class, Stage-A measured, theory closed form
pred_alts = {
    'measured_window (locked)': ep,
    'asym_level_effort_class': P2['arms']['RA']['e_asym_level_class'],
    'asym_member_class (rival)': P2['arms']['RA']['e_asym_member_class'],
    'theory_window_PREREG': TH['arms']['RA']['e_g_window'],
    'theory_asym_R': TH['arms']['RA']['e_g_asym'],
    'StageA_levelR_cost': -(1-json.load(open('MEASURED_AB.json'))['R']['b'])/(1-json.load(open('MEASURED_AB.json'))['R']['a']),
}
pred_tab={}
for name,p in pred_alts.items():
    pred_tab[name]=dict(pred=p, abs_err=abs(o['e_hat']-p),
        within_15=bool(abs(o['e_hat']-p)<=0.15*abs(p)),
        verdict=verdict(o['e_hat'], *o['e_ci'], p),
        rival_if_this_were_rival=rival_killed(o['e_hat'], *o['e_ci'], p))
out['RA_pred_alternatives']=pred_tab

# seed-count sensitivity: first 8 of 16 seeds
def scan_nseeds(arm, rhos, nseeds, seed=2027):
    rng=np.random.default_rng(seed)
    # temporarily shrink by copying subset into a fake R? easier: custom
    data={}
    for r in rhos:
        runs=R.get(('es',arm,'rho=%g'%r),[])
        runs=runs[:nseeds]
        if not runs: continue
        lnN=np.log([x['N'] for x in runs[0]['rows']])
        M=A.mat(runs)
        data[r]=(lnN,M)
    est={r: A.crossing(lnN, M.mean(0)) for r,(lnN,M) in data.items()}
    B=2000; boots={r:[] for r in data}
    for b in range(B):
        for r,(lnN,M) in data.items():
            idx=rng.integers(M.shape[0], size=M.shape[0])
            boots[r].append(A.crossing(lnN, M[idx].mean(0)))
    valid=[r for r in data if est[r] is not None and np.mean([x is not None for x in boots[r]])>=0.9]
    rec={'nseeds':nseeds,'valid':valid,'Nstar':{str(r):(float(np.exp(est[r])) if est[r] is not None else None) for r in data}}
    if len(valid)>=2:
        e=float(np.polyfit(np.log(valid),[est[r] for r in valid],1)[0])
        bs=[float(np.polyfit(np.log(valid),[boots[r][b] for r in valid],1)[0])
            for b in range(B) if all(boots[r][b] is not None for r in valid)]
        rec.update(e_hat=e, e_ci=A.ci(bs))
        if len(valid)>=3:
            rec['verdict_vs_locked_pred']=verdict(e, *A.ci(bs), ep)
            rec['rival_killed']=rival_killed(e, *A.ci(bs), er)
    return rec
out['RA_first8seeds']=scan_nseeds('RA', ra_rhos, 8)

# odd vs even seeds
def scan_idx(arm, rhos, which, seed=2027):
    rng=np.random.default_rng(seed)
    data={}
    for r in rhos:
        runs=R.get(('es',arm,'rho=%g'%r),[])
        runs=[runs[i] for i in which if i < len(runs)]
        lnN=np.log([x['N'] for x in runs[0]['rows']])
        M=A.mat(runs)
        data[r]=(lnN,M)
    est={r: A.crossing(lnN, M.mean(0)) for r,(lnN,M) in data.items()}
    B=2000; boots={r:[] for r in data}
    for b in range(B):
        for r,(lnN,M) in data.items():
            idx=rng.integers(M.shape[0], size=M.shape[0])
            boots[r].append(A.crossing(lnN, M[idx].mean(0)))
    valid=[r for r in data if est[r] is not None and np.mean([x is not None for x in boots[r]])>=0.9]
    rec={'valid':valid,'n':len(which)}
    if len(valid)>=2:
        e=float(np.polyfit(np.log(valid),[est[r] for r in valid],1)[0])
        bs=[float(np.polyfit(np.log(valid),[boots[r][b] for r in valid],1)[0])
            for b in range(B) if all(boots[r][b] is not None for r in valid)]
        rec.update(e_hat=e, e_ci=A.ci(bs),
                   verdict=verdict(e,*A.ci(bs),ep) if len(valid)>=3 else 'n/a',
                   rival_killed=rival_killed(e,*A.ci(bs),er) if len(valid)>=3 else None)
    return rec
out['RA_even_seeds']=scan_idx('RA', ra_rhos, list(range(0,16,2)))
out['RA_odd_seeds']=scan_idx('RA', ra_rhos, list(range(1,16,2)))

# AR official + if we ignored MV8
ar_rhos=P2['arms']['AR']['gated_rhos']
oa,_,_,bsa=run_scan('AR', ar_rhos, 2027)
idxa=[ar_rhos.index(x) for x in oa['valid_rhos']]
epa=float(np.polyfit(np.log(oa['valid_rhos']), np.log([P2['arms']['AR']['Nstar_pred'][i] for i in idxa]),1)[0])
era=float(np.polyfit(np.log(oa['valid_rhos']), np.log([P2['arms']['AR']['Nstar_rival'][i] for i in idxa]),1)[0])
out['AR_official']=dict(e_hat=oa.get('e_hat'), e_ci=oa.get('e_ci'), valid=oa.get('valid_rhos'),
    e_pred=epa, e_rival=era, se=float(np.std(bsa)),
    verdict_without_MV8=A.verdict(oa['e_hat'], *oa['e_ci'], epa),
    rival_killed=rival_killed(oa['e_hat'], *oa['e_ci'], era),
    MV8=bool(np.std(bsa)<=abs(epa-era)/2.8),
    MV8_threshold=abs(epa-era)/2.8)

# RR / AA official primary (PREREG rhos) and PREREG_2 gated
for arm, rhos_primary in [('RR',[0.01,0.02,0.04,0.08,0.16,0.32]),
                          ('AA',[0.01,0.02,0.04,0.08,0.16,0.32])]:
    o1,_,_,_=run_scan(arm, rhos_primary, 2026)  # note: official analyze uses one running rng; this is isolated
    out[f'{arm}_primary_isolated_seed2026']={k:o1.get(k) for k in ['e_hat','e_ci','valid_rhos','Nstar_hat']}
    # monotonicity of Nhat
    nh=o1['Nstar_hat']
    seq=[(r, nh[str(r)]) for r in o1['valid_rhos']]
    logs=[np.log(n) for _,n in seq if n]
    mono=all(logs[i]>=logs[i+1] for i in range(len(logs)-1))  # expected decreasing in rho
    out[f'{arm}_primary_isolated_seed2026']['Nhat_decreasing_in_rho']=mono
    out[f'{arm}_primary_isolated_seed2026']['Nhat_valid_seq']=seq

# PREREG_2 RR/AA
for arm in ['RR','AA']:
    rh=P2['arms'][arm]['gated_rhos']
    o2,_,_,bs2=run_scan(arm, rh, 2027)
    v=o2['valid_rhos']
    id2=[rh.index(x) for x in v]
    ep2=float(np.polyfit(np.log(v), np.log([P2['arms'][arm]['Nstar_pred'][i] for i in id2]),1)[0])
    out[f'{arm}_prereg2']={k:o2.get(k) for k in ['e_hat','e_ci','valid_rhos','Nstar_hat']}
    out[f'{arm}_prereg2'].update(e_pred=ep2, verdict=A.verdict(o2['e_hat'], *o2['e_ci'], ep2) if 'e_hat' in o2 else None,
        se=float(np.std(bs2)) if bs2 is not None else None,
        Nhat_seq=[(r, o2['Nstar_hat'][str(r)]) for r in v])

# C1 robustness: drop each valid rho; also drop the non-monotone RR 0.08
def slope_ci(arm, rhos, seed=2026):
    o2,_,_,bs2=run_scan(arm, rhos, seed)
    return o2, bs2

c1={}
for label, rhos in [('valid_0.04_0.32',[0.04,0.08,0.16,0.32]),
                    ('drop_0.08',[0.04,0.16,0.32]),
                    ('drop_0.04',[0.08,0.16,0.32]),
                    ('only_0.16_0.32',[0.16,0.32])]:
    oRR,_,estRR,bsRR=(*run_scan('RR', rhos, 2026),) if False else (None,None,None,None)
    oRR,_,_,bsRR=run_scan('RR', rhos, 2026)
    oAA,_,_,bsAA=run_scan('AA', rhos, 2026)
    if 'e_hat' in oRR and 'e_hat' in oAA and bsRR is not None and bsAA is not None:
        n=min(len(bsRR),len(bsAA))
        d=np.array(bsAA[:n])-np.array(bsRR[:n])
        dh=oAA['e_hat']-oRR['e_hat']
        lo,hi=A.ci(d)
        c1[label]=dict(diff=dh, ci=[lo,hi], RR=oRR['e_hat'], AA=oAA['e_hat'],
                       valid_RR=oRR['valid_rhos'], valid_AA=oAA['valid_rhos'],
                       rival_killed=bool(hi < -0.4),
                       RR_Nhat=oRR['Nstar_hat'], AA_Nhat=oAA['Nstar_hat'])
out['C1_robustness']=c1

# RR Nhat anomaly detail
rr = run_scan('RR', [0.01,0.02,0.04,0.08,0.16,0.32], 2026)[0]
out['RR_all_Nhat']=rr['Nstar_hat']
out['RR_valid']=rr['valid_rhos']

json.dump(out, open('/tmp/learnsim_ref/robust.json','w'), indent=1, default=float)
print('wrote robust.json')
# brief
print('RA official', out['RA_official']['e_hat'], out['RA_official']['e_ci'], out['RA_official']['verdict'], 'pred', out['RA_official']['e_pred'])
print('LOO', {k:{kk:v[kk] for kk in ('e_hat','verdict','rival_killed','valid','gate_ok') if kk in v} for k,v in out['RA_leave_one_rho'].items()})
print('alts', {k:{kk:v.get(kk) if not isinstance(v,dict) else v.get('e_hat',v.get('slope')) for kk in v} if isinstance(v,dict) else v for k,v in out['RA_alt_estimators'].items()})
print('pred alts', {k:v['verdict'] for k,v in out['RA_pred_alternatives'].items()})
print('C1', {k:{kk:v[kk] for kk in ('diff','ci','rival_killed','RR','AA')} for k,v in out['C1_robustness'].items()})
