# SH-noise analysis per SELF_HORIZON §6 (pre-statement hash in WORKLOG 13:13).
import json, math, numpy as np, mpmath as mp, sys
mp.mp.dps=50
A=json.load(open("argmin_sets.json"))
SIG=[0.4,0.3,0.2,0.15,0.1,0.07,0.05,0.035,0.025,0.018,0.012,0.008,0.005,0.0035]
CFG=['E-M3h','E-mixed','O','F-M3h','F-mixed']
d=np.load("curves_sh.npz"); NALL=[int(x) for x in d['n']]
E=np.load("../sr_b4/curves_even.npy"); NE_BIG=[int(x) for x in E[:,0] if x>4000]
def menu(cfg):
    if cfg.startswith('E'): return [n for n in NALL if n%2==0]+(NE_BIG if 'M3h' in cfg else [])
    if cfg=='O': return [n for n in NALL if n%2]
    return NALL+(NE_BIG if 'M3h' in cfg else [])
def dmin(n): # PIM closed forms (SR_B §8.6 even; odd: sin(pi/n)/cos(pi/2n), see §7)
    if n%2: return math.sin(math.pi/n)/math.cos(math.pi/(2*n))
    S=n//2; return math.sin(math.pi/n)/(math.cos(math.pi/n) if (1-S)%2 else 1.0)
def p_conf(n,s):  # wrapped-normal P(|theta| > pi/n)
    a=mp.pi/n; s=mp.mpf(s); inside=mp.mpf(0)
    for k in range(-3,4):
        inside+= mp.ncdf((a+2*mp.pi*k)/s)-mp.ncdf((-a+2*mp.pi*k)/s)
    return 1-inside
def analyse(cfg,taufun,taudisk,rounding=math.floor,tag=''):
    Aset={int(k):v for k,v in A[cfg]['A'].items()}
    res=[]
    for s in SIG:
        ns=menu(cfg); T={}; excl=0; openn=[]
        for n in ns:
            tau=taufun(n,s)
            t=rounding(tau) if tau<1e18 else 10**18
            if t>400:
                if t> math.pi**2/(4*dmin(n)): excl+=1; T[n]=None
                else: openn.append(n); T[n]=None
            else: T[n]=int(t)
        td=taudisk(s); tdisk=rounding(td) if td<1e18 else 10**18
        sc=[n for n in ns if T[n] is not None and T[n]>=2 and n in Aset[T[n]]]
        vac=sum(1 for n in ns if T[n]==1)
        disk_sc = (2<=tdisk<=400 and 0 in Aset[tdisk])
        disk_note = 'T(disk)=%s'%tdisk
        if tdisk>400: disk_note+=' (>400: SH1 applies only if odd or M3h-even polygons present)'
        cyc=set()
        for a in ns:
            ta=T[a]
            if ta is None or ta<2: continue
            for b in Aset[ta]:
                if b==0 or b==a: continue
                tb=T.get(b)
                if tb is not None and tb>=2 and a in Aset[tb] and a not in sc and b not in sc: cyc.add(tuple(sorted((a,b))))
        # crossing of Phi(n)-n over polygons with T in [1,400]; Phi = min polygon in A(T(n)) (T=1 -> all tied: Phi undefined)
        cross=None; prev=None
        for n in ns:
            if T[n] is None or T[n]<2: 
                if T[n]==1 and prev is not None and cross is None: cross=(prev[0],None,n,None)
                continue
            phi=min(x for x in Aset[T[n]] if x) if any(Aset[T[n]]) else None
            if phi is None: continue
            if prev is not None and (prev[1]-prev[0])>0 and (phi-n)<=0 and cross is None: cross=(prev[0],prev[1],n,phi)
            prev=(n,phi)
        res.append(dict(sigma=s,sc=sc,cycles=sorted(cyc),excluded=excl,open_n=openn[:5],n_open=len(openn),vacuous=vac,disk_sc=disk_sc,disk=disk_note,cross=cross))
    return res
def report(name,res):
    print("==",name)
    for r in res:
        print("  sigma=%-7g SC=%-14s cycles=%-22s disk_sc=%s %s | excl(proved)=%d open=%d vacuous(T=1)=%d | crossing(n,Phi)->(n',Phi')=%s"%(
            r['sigma'],r['sc'],r['cycles'][:4]+(['...%d'%len(r['cycles'])] if len(r['cycles'])>4 else []),r['disk_sc'],r['disk'],r['excluded'],r['n_open'],r['vacuous'],r['cross']))
# cache p
PC={}
def tau_primary(n,s):
    k=(n,s)
    if k not in PC: PC[k]=p_conf(n,s)
    p=PC[k]; return float(1/p) if p>1e-18 else 1e19
def tau_R1(n,s):
    r=1-math.exp(-s*s/2); return 1/(r*(1-1/n))
taud_primary=lambda s:1.0
taud_R1=lambda s:1/(1-math.exp(-s*s/2))
ALL={}
for cfg in CFG:
    ALL[('primary',cfg)]=analyse(cfg,tau_primary,taud_primary); report('PRIMARY '+cfg,ALL[('primary',cfg)])
for cfg in CFG:
    ALL[('ceil',cfg)]=analyse(cfg,tau_primary,taud_primary,rounding=math.ceil); report('CEIL '+cfg,ALL[('ceil',cfg)])
for cfg in CFG:
    ALL[('R1',cfg)]=analyse(cfg,tau_R1,taud_R1); report('R1 '+cfg,ALL[('R1',cfg)])
json.dump({"%s|%s"%k:v for k,v in ALL.items()},open("sh_noise.json","w"),default=str)
