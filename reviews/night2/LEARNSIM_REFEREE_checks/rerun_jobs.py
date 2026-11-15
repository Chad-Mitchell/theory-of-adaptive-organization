"""Rerun a subset of locked onset jobs and compare to saved jsonl (nice 19)."""
import json, os, sys, time
sys.path.insert(0, '/workspace/gtao/night2/LEARNSIM')
os.chdir('/workspace/gtao/night2/LEARNSIM')
os.nice(19)
import run_onset as ro

C = json.load(open('GRID_CENTERS.json'))
C2 = json.load(open('GRID_CENTERS_2.json'))

def centre(arm, rho):
    rho=float(rho)
    if rho in C['rhos']:
        return C['scan'][arm][C['rhos'].index(rho)]
    return C2['ext'][arm][str(rho) if str(rho) in C2['ext'].get(arm,{}) else ('%g'%rho)]

# load saved
saved={}
for path in ['results_es.jsonl','results_ext.jsonl']:
    for line in open(path):
        d=json.loads(line)
        saved[(d['arm'],d['cell'],d['seed'],d['learner'])]=d

jobs=[
    ('RR','rho=0.16',0.16,1.0,centre('RR',0.16),0,'es'),
    ('RA','rho=0.16',0.16,1.0,centre('RA',0.16),0,'es'),
    ('AA','rho=0.16',0.16,1.0,centre('AA',0.16),0,'es'),
    ('RA','rho=0.64',0.64,1.0,centre('RA',0.64),0,'es'),
]
out=[]
for a in jobs:
    t0=time.time()
    print('START', a[0], a[1], 'seed', a[5], flush=True)
    r=ro.job(a)
    dt=time.time()-t0
    key=(r['arm'],r['cell'],r['seed'],r['learner'])
    s=saved[key]
    def arr(xs): return [float(x) for x in xs]
    cmp={
        'arm':r['arm'],'cell':r['cell'],'seed':r['seed'],'seconds':dt,
        'flat_pm_new':r['flat_pm'],'flat_pm_old':s['flat_pm'],'flat_pm_rel': (r['flat_pm']-s['flat_pm'])/s['flat_pm'],
        'flat2_rel': (r['flat2_pm']-s['flat2_pm'])/s['flat2_pm'],
        'res_rel': (r['res_pm']-s['res_pm'])/s['res_pm'],
        'flat_eff_match': arr(r['flat_eff'])==arr(s['flat_eff']),
        'res_eff_match': arr(r['res_eff'])==arr(s['res_eff']),
        'lev_eff_match': arr(r['lev_eff'])==arr(s['lev_eff']),
        'max_abs_D_rel': max(abs(a['D_rel']-b['D_rel']) for a,b in zip(r['rows'],s['rows'])),
        'max_rel_D_rel': max(abs(a['D_rel']-b['D_rel'])/max(1e-12,abs(b['D_rel'])) for a,b in zip(r['rows'],s['rows'])),
        'D_rel_new': [x['D_rel'] for x in r['rows']],
        'D_rel_old': [x['D_rel'] for x in s['rows']],
    }
    print('DONE', cmp['arm'], cmp['cell'], 'sec', round(dt,1), 'flat_eff_match', cmp['flat_eff_match'],
          'max_abs_D_rel', cmp['max_abs_D_rel'], 'flat_pm_rel', cmp['flat_pm_rel'], flush=True)
    out.append(cmp)
json.dump(out, open('/tmp/learnsim_ref/sim_rerun.json','w'), indent=1)
print('wrote sim_rerun.json')
