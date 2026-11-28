# POST-LOCK exploratory analyses (not preregistered)
import json,collections,datetime as dt,numpy as np,subprocess
exec(open('analyze.py').read().split('# ---------- P1 ----------')[0])
rng=np.random.default_rng(7)
# E1: are change events concentrated near the atom's window? compare event-time distance to window vs uniform time over life
obs=[];exp_=[];n_at=0
for i,vs in by.items():
    t0,end,ev,term=atom_events(vs)
    ws=[v.get('window') for v in vs if v.get('window') and not v.get('repeat')]
    if not ws or len(ev)<2: continue
    n_at+=1
    wd=[T(w if 'T' in w else w+'T23:59') for w in set(ws)]
    def dist(t): return min(abs(days(t,w)) for w in wd)
    for e in ev[1:]: obs.append(dist(e))
    for _ in range(200):
        u=t0+dt.timedelta(days=rng.uniform(0,max(days(t0,end),0.01))); exp_.append(dist(u))
obs=np.array(obs);exp_=np.array(exp_)
E1=dict(atoms=n_at,events=len(obs),frac_within2d_obs=float((obs<=2).mean()),frac_within2d_uniform=float((exp_<=2).mean()),median_dist_obs=float(np.median(obs)),median_dist_uniform=float(np.median(exp_)))
bs=[]
ids=list(range(len(obs)))
for _ in range(2000):
    k=rng.choice(len(obs),len(obs)); bs.append((obs[k]<=2).mean())
E1['frac_within2d_obs_ci']=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))]
# E2: share of change events that are terminal (done/cancelled) vs edits
term_ev=0;tot=0
for i,vs in by.items():
    for v in vs[1:]:
        if v['from'].startswith(ACE): continue
        tot+=1; term_ev+= v['status'] in TERM
E2=dict(nonace_versions=tot,terminal=term_ev)
# E3: P4b reverts / restores in looper git history
log=subprocess.run(['git','-C','<private-app-repo>','log','--all','--format=%s'],capture_output=True,text=True).stdout.splitlines()
rev=[s for s in log if s.lower().startswith('revert') or 'restore' in s.lower() or 'recover' in s.lower()]
E3=dict(commits=len(log),revert_restore=len(rev),per100=100*len(rev)/len(log))
# E4: write ratio
D=[json.loads(l) for l in open('<private-app-repo>/store/discards.jsonl')]
E4=dict(journal_lines=len(J),discards=len(D),discard_reasons=dict(collections.Counter(d['why'] for d in D).most_common()))
o=dict(E1=E1,E2=E2,E3=E3,E4=E4)
json.dump(o,open('explore_postlock.json','w'),indent=1); print(json.dumps(o,indent=1))
