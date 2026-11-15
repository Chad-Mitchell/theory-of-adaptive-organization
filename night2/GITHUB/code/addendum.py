import json, os, sys, math, numpy as np
from scipy import optimize, special, stats
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import analyze as A
def spells(x):
    out=[]; cur=None; L=0; started=False
    for v in x:
        if np.isnan(v): cur=None; L=0; started=False; continue   # gaps censor spells
        if cur is None: cur=v; L=1; started=False; continue
        if v==cur: L+=1
        else:
            if started: out.append(L)
            cur=v; L=1; started=True
    return out   # first spell after a gap is left-censored and dropped; last open spell dropped
def regime(units):
    s=np.array([d for u in units for d in spells(u['x'])],float)
    p=1/s.mean(); llg=np.sum(np.log(p)+(s-1)*np.log(1-p))
    f=lambda a: -(-a*np.sum(np.log(s))-len(s)*np.log(special.zeta(a,1)))
    r=optimize.minimize_scalar(f,bounds=(1.01,10),method='bounded'); llz=-r.fun
    dAIC=(2-2*llg)-(2-2*llz)
    rej=0; tested=0
    for u in units:
        ss=np.array(spells(u['x']),float)
        if len(ss)>=8:
            tested+=1; pp=1/ss.mean()
            if stats.kstest(ss,lambda v:1-(1-pp)**np.floor(v)).pvalue<0.05: rej+=1
    reg='B' if dAIC>10 else ('A' if dAIC<-10 else 'INCONCLUSIVE')
    return dict(n_spells=len(s),mean=float(s.mean()),zeta_alpha=float(r.x),dAIC_geom_minus_zeta=float(dAIC),regime=reg,units_tested=tested,units_reject_geom=rej)
if __name__=='__main__':
    wf,pinned,fu,fo,um=A.build_real(); units=A.to_units(wf,fu); flat=[u for u in units if not u['is_level']]
    res=regime(flat); main=json.load(open(os.path.join(HERE,'..','results_real.json')))
    b=main['gate']['b']; lo,hi=main['gate']['b_ci']
    band=(0.75,1.25) if res['regime']=='B' else (0.35,0.65)
    res['P1R']=A.verdict_band(b,(lo,hi),band) if res['regime']!='INCONCLUSIVE' else 'INCONCLUSIVE-regime'
    res['P1R_vs_regimeB_band_descriptive']=A.verdict_band(b,(lo,hi),(0.75,1.25))
    json.dump(res,open(os.path.join(HERE,'..','results_addendum.json'),'w'),indent=1); print(res)
