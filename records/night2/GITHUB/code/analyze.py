"""GITHUB-UPSTREAM locked analysis. Usage: python analyze.py [real|synthetic SPEC]
All inference: cluster bootstrap, B=999, SEED=20261115, percentile 95% CIs.
"""
import json, os, sys, math, collections, datetime as dt
import numpy as np
from scipy import optimize, stats
SEED=20261115; B=999
HERE=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(HERE,'..','data')
sys.path.insert(0,HERE)
W0=dt.date(2025,11,16); NW=52

# ---------------------------------------------------------------- interval regression
def bounds_from_grid(y):
    g=np.unique(np.round(y,4))
    lo={};hi={}
    for i,v in enumerate(g):
        lo[v]= v*math.sqrt(v/g[i+1]) if i==0 and len(g)>1 else (math.sqrt(v*g[i-1]) if i>0 else v/2)
        hi[v]= v*math.sqrt(v/g[i-1]) if i==len(g)-1 and len(g)>1 else (math.sqrt(v*g[i+1]) if i<len(g)-1 else v*2)
    r=np.round(y,4)
    # open-ended extreme bins (left/right censoring): the lowest and highest observed values absorb the tails
    lo[g[0]]=1e-12; hi[g[-1]]=1e12
    return np.log([lo[v] for v in r]), np.log([hi[v] for v in r])
def intreg(L,U,X,start=None):
    ols=np.linalg.lstsq(X,(L+U)/2,rcond=None)[0]
    s0=np.std((L+U)/2-X@ols)+1e-3
    th0=np.r_[ols,math.log(s0)] if start is None else start
    def nll(th):
        b=th[:-1]; s=math.exp(th[-1]); m=X@b
        p=stats.norm.cdf((U-m)/s)-stats.norm.cdf((L-m)/s)
        return -np.sum(np.log(np.clip(p,1e-300,None)))
    r=optimize.minimize(nll,th0,method='BFGS')
    return r.x
# ---------------------------------------------------------------- weekly state series
def week_series(runs):
    last={}
    for c,concl,sha,a,b in runs:
        if concl not in ('success','failure'): continue
        d=dt.date.fromisoformat(c[:10]); w=(d-W0).days//7
        if 0<=w<NW and (w not in last or c>last[w][0]): last[w]=(c,1.0 if concl=='failure' else 0.0)
    x=np.full(NW,np.nan)
    for w,(c,s) in last.items(): x[w]=s
    return x
def deblip(x):
    y=x.copy()
    for w in range(1,NW-1):
        if not np.isnan(x[w-1]) and not np.isnan(x[w+1]) and not np.isnan(x[w]) and x[w-1]==x[w+1]!=x[w]: y[w]=x[w-1]
    return y
def drift(x, idx=None):
    d=np.diff(x); ok=~np.isnan(d)
    if idx is not None: ok&=idx
    k=np.nansum(np.abs(d[ok])); m=ok.sum()
    return (k+0.5)/(m+1), m
# ---------------------------------------------------------------- build units
def build_real():
    import pull
    files=json.load(open(f'{D}/files.json')); runs=json.load(open(f'{D}/runs.json'))
    repos=json.load(open(f'{D}/repos.json')); ups=json.load(open(f'{D}/upstreams.json'))
    frame_up=collections.Counter(); frame_owner=collections.Counter(); wf={}; pinned=[]
    for k,r in files.items():
        if r.get('_bad') or r.get('fork') or not r['crons']: continue
        c=pull.classify(r)
        for u in c['ext_unpinned']: frame_up[u]+=1
        if c['ext_unpinned']: frame_owner[r['repo'].split('/')[0].lower()]+=1
        if k not in runs or not c['nominal_pw'] or not (1<=c['nominal_pw']<=168): continue
        rm=repos.get(r['repo'],{})
        if rm.get('_bad') or rm.get('archived') or rm.get('fork'): continue
        x=week_series(runs[k]['runs'])
        if np.sum(~np.isnan(x))<8: continue
        durs=[ (dt.datetime.fromisoformat(b.replace('Z','+00:00'))-dt.datetime.fromisoformat(a.replace('Z','+00:00'))).total_seconds()/60
               for _,cc,_,a,b in runs[k]['runs'] if a and b and cc in ('success','failure')]
        rec=dict(key=k,repo=r['repo'],owner=r['repo'].split('/')[0].lower(),nom=c['nominal_pw'],ups=c['ext_unpinned'],pinned=c['ext_pinned'],
                 n_members=c['n_members'],members=c['members'],x=x,dur=float(np.median(durs)) if durs else np.nan,
                 nsched=len(runs[k]['runs']),stars=rm.get('stargazers_count'),forks=rm.get('forks_count'),commits=rm.get('commits_window'),
                 recent=sum(1 for rr in runs[k]['runs'] if rr[0][:10]>='2026-08-23'))
        if c['ext_unpinned']: wf[k]=rec
        elif c['ext_pinned']: pinned.append(rec)
    return wf,pinned,frame_up,frame_owner,ups
def to_units(wf,frame_up):
    by=collections.defaultdict(list)
    for r in wf.values(): by[r['repo']].append(r)
    units=[]
    for repo,L in by.items():
        prim=max(L,key=lambda r:(r['nsched'],r['key']))
        level=[r for r in L if r['n_members']>=2]
        pu=max(prim['ups'],key=lambda u:(frame_up[u],u))
        units.append(dict(repo=repo,owner=prim['owner'],E=min(168.0,sum(r['nom'] for r in L)),prim=prim,pu=pu,
                          ups=sorted({u for r in L for u in r['ups']}),is_level=bool(level),level_wf=level[0] if level else None,
                          stars=prim['stars'],forks=prim['forks'],commits=prim['commits'],dur=prim['dur'],x=prim['x'],recent=prim['recent'],nom_prim=prim['nom']))
    return units
# ---------------------------------------------------------------- class gate
def design(units, qkey):
    X=np.c_[np.ones(len(units)),[math.log(u['stars']+1) for u in units],[math.log(u[qkey]) for u in units],
            [math.log((u['commits'] or 0)+1) for u in units],[math.log(max(u['dur'],0.5)) if not np.isnan(u['dur']) else 0.0 for u in units],
            [1.0 if np.isnan(u['dur']) else 0.0 for u in units]]
    return X
def fit_gate(units):
    for u in units:
        u['q'],u['m']=drift(u['x'])
        d=np.diff(u['x']); n=len(d)
        u['q1'],_=drift(u['x'],np.arange(n)%2==0); u['q2'],_=drift(u['x'],np.arange(n)%2==1)
    y=np.array([u['E'] for u in units]); L,U=bounds_from_grid(y)
    X=design(units,'q'); th=intreg(L,U,X)
    # split-half partial reliability of ln q given other covariates
    Z=np.delete(X,2,axis=1)
    def resid(v): return v-Z@np.linalg.lstsq(Z,v,rcond=None)[0]
    h1=resid(np.log([u['q1'] for u in units])); h2=resid(np.log([u['q2'] for u in units]))
    r=np.corrcoef(h1,h2)[0,1]; rel=max(2*r/(1+r),0.05) if r>0 else 0.05
    return dict(a=th[1],b_naive=th[2],b=th[2]/rel,rel=rel,r_half=r,sigma=math.exp(th[-1]),coef=th.tolist())
def boot(units, fn, cluster, seed=SEED, B=B):
    rng=np.random.default_rng(seed); cl=collections.defaultdict(list)
    for i,u in enumerate(units): cl[cluster(u)].append(i)
    keys=list(cl); out=[]
    for bi in range(B):
        pick=rng.choice(len(keys),len(keys),replace=True)
        samp=[dict(units[i]) for k in pick for i in cl[keys[k]]]
        try: out.append(fn(samp))
        except Exception: pass
    return out
def ci(v): v=np.array([x for x in v if x is not None and np.isfinite(x)]); return [float(np.percentile(v,2.5)),float(np.percentile(v,97.5))] if len(v) else [None,None]
def verdict_band(pt,lohi,band=(0.35,0.65)):
    lo,hi=lohi
    if lo is None: return 'INCONCLUSIVE'
    if hi<band[0] or lo>band[1]: return 'KILL-CONDITION'
    if band[0]<=pt<=band[1] and lo>0: return 'PASS-CONDITION'
    return 'INCONCLUSIVE'
# ---------------------------------------------------------------- decomposition (rho, kappa)
def decomp(units, frame_up, frame_owner):
    n=len(units); X=np.abs(np.array([np.diff(u['x']) for u in units])); M=~np.isnan(X)
    # change indicators c=|dx| (binary-state signs desynchronize across repos, so signed increments cannot show shared change); centred per unit
    mu=np.array([X[i][M[i]].mean() if M[i].any() else 0.0 for i in range(n)]); X=X-mu[:,None]; X0=np.where(M,X,0.0)
    cnt=M.astype(float)@M.T.astype(float); S=X0@X0.T
    nul=np.zeros_like(S); nc=np.zeros_like(S)
    for s in (13,26,39):
        Xs=np.roll(X0,s,axis=1); Ms=np.roll(M,s,axis=1).astype(float)
        nul+=X0@Xs.T; nc+=M.astype(float)@Ms.T
    with np.errstate(invalid='ignore',divide='ignore'):
        cov=S/cnt; covn=nul/nc; exc=cov-covn
    var=np.array([np.mean(X[i][M[i]]**2) for i in range(n)])
    ow=np.array([u['owner'] for u in units]); rp=np.array([u['repo'] for u in units])
    allup=sorted({x for u in units for x in u['ups']}); ix={x:k for k,x in enumerate(allup)}
    A=np.zeros((n,len(allup)));
    for i,u in enumerate(units):
        for x in u['ups']: A[i,ix[x]]=1
    share=(A@A.T)>0; sameo=ow[:,None]==ow[None,:]; samer=rp[:,None]==rp[None,:]
    iu=np.triu(np.ones((n,n),bool),1); ok=iu&(cnt>=20)&np.isfinite(exc)&~samer   # bootstrap duplicates never pair with themselves
    so=exc[ok&sameo&share]; su=exc[ok&~sameo&share]; g=exc[ok&~sameo&~share]
    V=float(np.mean(var)); CG=float(np.mean(g)) if len(g) else np.nan; CSU=float(np.mean(su)) if len(su) else np.nan; CSO=float(np.mean(so)) if len(so)>=10 else np.nan
    shared_pool=np.nanmean([CSU]) ; rho=(CSU)/(V-CSU) if np.isfinite(CSU) else np.nan
    comp={'private':V-(CSO if np.isfinite(CSO) else CSU),'owner':(CSO-CSU) if np.isfinite(CSO) else np.nan,'upstream':CSU-CG,'global':CG}
    nsz={'private':1.0,'owner':float(np.mean([frame_owner[u['owner']] for u in units if frame_owner[u['owner']]>=2])) if any(frame_owner[u['owner']]>=2 for u in units) else np.nan,
         'upstream':float(np.mean([frame_up[u['pu']] for u in units])),'global':float(sum(frame_owner.values()))}
    pts=[(math.log(nsz[k]),math.log(comp[k])) for k in comp if np.isfinite(comp[k]) and comp[k]>0 and np.isfinite(nsz[k])]
    kappa=-np.polyfit([p[0] for p in pts],[p[1] for p in pts],1)[0] if len(pts)>=3 else np.nan
    return dict(V=V,C_G=CG,C_SU=CSU,C_SO=CSO,n_pairs=[len(so),len(su),len(g)],rho=rho,comp=comp,nsz=nsz,kappa=float(kappa),n_scopes=len(pts))
# ---------------------------------------------------------------- vigilance
def vigilance(units, rho):
    flat=[u for u in units if not u['is_level']]; lev=[u for u in units if u['is_level']]
    pairs=[]
    for L in lev:
        U=max(L['level_wf']['ups'],key=lambda x:x)  # any upstream of level wf with comparators
        best=None
        for up in L['level_wf']['ups']:
            comp=[f for f in flat if up in f['ups'] and f['repo'].lower() not in L['level_wf']['members']]
            if len(comp)>=3 and (best is None or len(comp)>len(best[1])): best=(up,comp)
        if best: pairs.append((L,best[0],best[1]))
    return pairs
def vig_stat(pairs):
    return float(np.mean([math.log(L['level_wf']['nom'])-np.mean([math.log(f['E']) for f in comp]) for L,up,comp in pairs]))
# ---------------------------------------------------------------- main
def run(units, pinned, frame_up, frame_owner, ups_meta):
    res={'n_units':len(units)}
    flat=[u for u in units if not u['is_level']]; res['n_flat']=len(flat); res['n_level']=len(units)-len(flat)
    res['E_dist']=dict(collections.Counter(round(u['E'],2) for u in flat).most_common(12))
    g=fit_gate(flat); res['gate']=g
    bs=boot(flat,fit_gate,lambda u:u['pu'])
    for k in ('a','b','b_naive'): res['gate'][k+'_ci']=ci([x[k] for x in bs])
    res['gate']['a_minus_b_ci']=ci([x['a']-x['b'] for x in bs])
    res['gate']['se_b']=float(np.std([x['b'] for x in bs]))
    res['P1_drift_matching']=verdict_band(g['b'],res['gate']['b_ci'])
    res['P2_stakes_a']=verdict_band(g['a'],res['gate']['a_ci'])
    lo,hi=res['gate']['a_minus_b_ci']; res['P3_a_eq_b']='CONSISTENT' if lo<=0<=hi else 'CLASS-NOT-R'
    # selection gate
    kres=math.exp(0.674*g['sigma']); eps=(kres+1/kres)/2-1
    sdq=float(np.std(np.log([u['q'] for u in flat]))); kp=math.exp(0.5*sdq); prize=(kp+1/kp)/2-1
    res['selection_gate']=dict(eps=eps,prize=prize,sd_lnq=sdq,passed=prize>eps)
    res['power_gate']=dict(se_b=res['gate']['se_b'],required=0.18,passed=res['gate']['se_b']<=0.18)
    # convergent / known groups
    for u in flat: u['qL']=None
    byU=collections.defaultdict(list)
    for u in flat: byU[u['pu']].append(u)
    for u in flat:
        o=[v['q'] for v in byU[u['pu']] if v is not u]
        if len(o)>=2: u['qL']=float(np.mean(o))
    cu=[u for u in flat if u['qL']]
    res['MV5_q_own_vs_LOO_spearman']=float(stats.spearmanr([u['q'] for u in cu],[u['qL'] for u in cu])[0]) if len(cu)>10 else None
    cc=[u for u in flat if ups_meta.get(u['pu'],{}).get('commits_window')]
    res['MV5_q_own_vs_upcommits_spearman']=float(stats.spearmanr([u['q'] for u in cc],[ups_meta[u['pu']]['commits_window'] for u in cc])[0]) if len(cc)>10 else None
    res['MV5_stars_forks_spearman']=float(stats.spearmanr([u['stars'] for u in flat],[u['forks'] for u in flat])[0])
    act=[u for u in flat if u['recent']>0]
    res['MV7_E_nominal_vs_actual_recent_spearman']=float(stats.spearmanr([u['nom_prim'] for u in act],[u['recent'] for u in act])[0]) if len(act)>10 else None
    if len(pinned)>=10:
        qp=np.log([drift(p['x'])[0] for p in pinned]); qf=np.log([u['q'] for u in flat])
        rng=np.random.default_rng(SEED); d=[np.mean(rng.choice(qp,len(qp)))-np.mean(rng.choice(qf,len(qf))) for _ in range(B)]
        res['MV7_pinned_vs_unpinned_q_ratio']=dict(n_pinned=len(pinned),ratio=float(math.exp(qp.mean()-qf.mean())),ci=[math.exp(x) for x in ci(d)],
                                                  passed=bool(math.exp(ci(d)[1])<1))
    else: res['MV7_pinned_vs_unpinned_q_ratio']=dict(n_pinned=len(pinned),passed=None)
    # secondary IV-style: LOO q in place of own q
    if len(cu)>=30:
        for u in cu: u['qLx']=u['qL']
        y=np.array([u['E'] for u in cu]); L,U=bounds_from_grid(y); th=intreg(L,U,design(cu,'qLx'))
        bs2=boot(cu,lambda s:(lambda yy:intreg(*bounds_from_grid(yy),design(s,'qLx'))[2])(np.array([u['E'] for u in s])),lambda u:u['pu'],B=299)
        res['secondary_b_LOO']=dict(n=len(cu),b=float(th[2]),ci=ci(bs2))
    # decomposition
    dc=decomp(flat,frame_up,frame_owner); res['decomp']=dc
    bsd=boot(flat,lambda s:decomp(s,frame_up,frame_owner),lambda u:u['repo'],B=199)
    res['decomp']['rho_ci']=ci([x['rho'] for x in bsd]); res['decomp']['kappa_ci']=ci([x['kappa'] for x in bsd])
    # vigilance
    rho=dc['rho'] if np.isfinite(dc['rho']) and dc['rho']>0 else 0.0
    floor=1+(1+rho)**-0.5
    pairs=vigilance(units,rho); res['vig_n_levels_with_comparators']=len(pairs)
    if len(pairs)>=10:
        lv=vig_stat(pairs); rng=np.random.default_rng(SEED)
        bv=[vig_stat([pairs[i] for i in rng.choice(len(pairs),len(pairs))]) for _ in range(B)]
        V=math.exp(lv); vci=[math.exp(x) for x in ci(bv)]
        # adjusted (MV6): interval reg on all units with level dummy
        allu=[u for u in units]
        for u in allu: u['q'],_=drift(u['x'])
        y=np.array([u['E'] for u in allu]); L,U=bounds_from_grid(y)
        X=np.c_[design(allu,'q'),[1.0 if u['is_level'] else 0.0 for u in allu]]; th=intreg(L,U,X)
        bva=boot(allu,lambda s:(lambda yy:intreg(*bounds_from_grid(yy),np.c_[design(s,'q'),[1.0 if u['is_level'] else 0.0 for u in s]])[-2])(np.array([u['E'] for u in s])),lambda u:u['pu'],B=299)
        Va=math.exp(th[-2]); vaci=[math.exp(x) for x in ci(bva)]
        def vv(V,c):
            if c[1]/floor<0.8 or (c[1]<1 and g['a']>=g['b']): return 'KILL-CONDITION'
            if c[0]/floor>=0.8 and c[0]>1: return 'PASS-CONDITION'
            return 'INCONCLUSIVE'
        res['P6_vigilance']=dict(floor=floor,V_adj=Va,V_adj_ci=vaci,verdict_primary=vv(Va,vaci),V_raw=V,V_raw_ci=vci,verdict_raw=vv(V,vci))
        levs=[L for L,_,_ in pairs]; nm=[L['level_wf']['n_members'] for L in levs]
        if len(levs)>=10 and max(nm)/min(nm)>=4:
            sl=np.polyfit(np.log(nm),np.log([L['level_wf']['nom'] for L in levs]),1)[0]
            pred=g['a']-dc['kappa']*g['b'] if np.isfinite(dc['kappa']) else None
            res['P5_rank_gradient']=dict(slope=float(sl),pred=pred,verdict=('PASS-CONDITION' if pred is not None and abs(sl-pred)<=0.15 else 'NOT-MET'))
        else: res['P5_rank_gradient']='NOT ANALYSED (fewer than 10 levels or <4x range in members)'
    else:
        res['P6_vigilance']=f'NOT ANALYSED: {len(pairs)} levels with >=3 same-upstream flat comparators (<10 required)'
        res['P5_rank_gradient']='NOT ANALYSED'
    return res

# ---------------------------------------------------------------- synthetic dry run
def synthetic_shared(n=300,nup=30,qs=0.03,qp=0.06,seed=3):
    """known-groups for decomposition: per-upstream shared flips (rate qs) + private flips (rate qp); true rho ~ qs/qp"""
    rng=np.random.default_rng(seed); ev=rng.random((nup,NW))<qs; units=[]
    for i in range(n):
        up=rng.integers(nup); st=0.0; x=np.empty(NW)
        for w in range(NW):
            if ev[up,w]: st=1-st
            if rng.random()<qp: st=1-st
            x[w]=st
        units.append(dict(repo=f'o{i}/r',owner=f'o{i}',E=1.0,pu=f'u{up}',ups=[f'u{up}'],is_level=False,x=x))
    return units
def synthetic(a,b,n=500,nup=60,seed=1,sigma=1.0,grid=(1,2,7,14,28,168)):
    rng=np.random.default_rng(seed); units=[]
    upq=rng.normal(-3.0,0.6,nup)
    for i in range(n):
        up=rng.integers(nup); lnq=upq[up]+rng.normal(0,0.6); q=min(math.exp(lnq),0.45)
        lnW=rng.normal(3,2); com=rng.integers(0,500)
        lat=math.log(2.6)+a*(lnW-3)+b*(math.log(q)+3)+0.1*(math.log(com+1)-5)+rng.normal(0,sigma)
        E=min(grid,key=lambda gv:abs(math.log(gv)-lat))
        st=float(rng.random()<0.3); x=np.empty(NW)
        for w in range(NW):
            if rng.random()<q: st=1-st
            x[w]=st
        x[rng.random(NW)<0.08]=np.nan
        units.append(dict(repo=f'o{i}/r',owner=f'o{i}',E=float(E),pu=f'u{up}',ups=[f'u{up}'],is_level=False,stars=int(math.exp(lnW)),forks=1,commits=int(com),dur=10.0,x=x,recent=1,nom_prim=E))
    return units
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='synthetic':
        out={}
        for a,b in [(0.5,0.5),(0.5,0.0),(0.5,1.0),(0.0,0.5)]:
            u=synthetic(a,b); g=fit_gate(u); bs=boot(u,fit_gate,lambda z:z['pu'],B=99)
            out[f'a{a}_b{b}']=dict(a=g['a'],b=g['b'],b_naive=g['b_naive'],rel=g['rel'],b_ci=ci([x['b'] for x in bs]),a_ci=ci([x['a'] for x in bs]))
            print(a,b,out[f'a{a}_b{b}'],flush=True)
        for qs,qp in [(0.0,0.06),(0.03,0.06),(0.06,0.03)]:
            u=synthetic_shared(qs=qs,qp=qp); fu=collections.Counter(x['pu'] for x in u); fo=collections.Counter(x['owner'] for x in u)
            d=decomp(u,fu,fo); out[f'decomp_qs{qs}_qp{qp}']=dict(rho=d['rho'],C_SU=d['C_SU'],C_G=d['C_G'],V=d['V']); print(qs,qp,out[f'decomp_qs{qs}_qp{qp}'],flush=True)
        json.dump(out,open(os.path.join(HERE,'..','dryrun_synthetic.json'),'w'),indent=1)
    else:
        wf,pinned,fu,fo,um=build_real(); units=to_units(wf,fu)
        res=run(units,pinned,fu,fo,um)
        json.dump(res,open(os.path.join(HERE,'..','results_real.json'),'w'),indent=1,default=float)
        print(json.dumps(res,indent=1,default=float))
