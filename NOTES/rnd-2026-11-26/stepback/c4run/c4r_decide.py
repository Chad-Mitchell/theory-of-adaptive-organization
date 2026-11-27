# C4R decision rule (draft §4), shared by toy and scored analyses.
import re, math, numpy as np
RAYS=[0.25,0.5,0.75,0.9]
def parse(lines):
    out=[]
    for ln in lines:
        d=dict(re.findall(r'(\S+)=(\S+)',ln)); 
        if 'L0.00' not in d: continue
        out.append({k:float(v) for k,v in d.items() if k!='seed'}|{'seed':d['seed']})
    return out
def R(rec,s,c=1.0):
    return rec['L%.2f'%s]/(rec['L0.00']*math.sqrt(1-(s/c)**2))
def decide(treat,ctrl,c_treat=None):
    res={}; 
    for s in RAYS:
        a=np.array([R(r,s,c_treat(r) if c_treat else 1.0) for r in treat]); b=np.array([R(r,s) for r in ctrl])
        d=a.mean()-b.mean(); se=math.sqrt(a.var(ddof=1)/len(a)+b.var(ddof=1)/len(b))
        res[s]=dict(Rt=a.mean(),Rc=b.mean(),sdt=a.std(ddof=1),sdc=b.std(ddof=1),dR=d,z=d/se if se>0 else float('inf'))
    valid=all(abs(res[s]['Rc']-1)<=0.02 for s in RAYS)
    hit=res[0.9]['dR']>=0.20 and res[0.9]['z']>=5 and all(res[s]['dR']>0 and res[s]['z']>=3 for s in (0.5,0.75,0.9))
    miss=all(abs(res[s]['dR'])<=0.02 for s in RAYS)
    out='OPEN (control invalid)' if not valid else ('HIT' if hit else ('MISS' if miss else 'OPEN'))
    return out,res
