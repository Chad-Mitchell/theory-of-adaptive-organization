import json, math, numpy as np
L=json.load(open("level_tau.json")); A=json.load(open("argmin_sets.json"))
SIG=[0.4,0.3,0.2,0.15,0.1,0.07,0.05,0.035,0.025,0.018,0.012,0.008,0.005,0.0035]; DEL=['0.1','0.2','0.3','0.5']
def dmin(n):
    if n%2: return math.sin(math.pi/n)/math.cos(math.pi/(2*n))
    S=n//2; return math.sin(math.pi/n)/(math.cos(math.pi/n) if (1-S)%2 else 1.0)
CFG={'E-M3h':lambda n:n%2==0,'E-mixed':lambda n:n%2==0,'O':lambda n:n%2==1,'F-M3h':lambda n:True,'F-mixed':lambda n:True}
print("disk check (Nystrom vs Siegmund):",L['disk_check'])
summary={}
for cfg,ok in CFG.items():
    As={int(k):v for k,v in A[cfg]['A'].items()}
    for dl in DEL:
        rows=[]
        for s in SIG:
            ns=[n for n in range(3,1202) if ok(n)]
            T={}; openn=0
            for n in ns:
                kind,tau=L['poly']["%d|%g"%(n,s)][dl]
                t=math.floor(tau) if tau<1e18 else 10**18
                if t>400:
                    T[n]=None
                    if not t>math.pi**2/(4*dmin(n)): openn+=1
                else: T[n]=t
            td=math.floor(L['disk']["%g|%s"%(s,dl)][0])
            sc=[n for n in ns if T[n] and T[n]>=2 and n in As[T[n]]]
            cyc=sorted({tuple(sorted((a,b))) for a in ns if T[a] and T[a]>=2 for b in As[T[a]] if b and b!=a and b in T and T[b] and T[b]>=2 and a in As[T[b]] and a not in sc and b not in sc})
            dsc = td>=2 and (cfg=='E-mixed' or (td<=400 and 0 in As[td]))
            prev=None; cross=None
            for n in ns:
                if not T[n] or T[n]<2: continue
                phi=min([x for x in As[T[n]] if x] or [None]) if any(As[T[n]]) else None
                if phi is None: continue
                if prev and prev[1]-prev[0]>0 and phi-n<=0: cross=(prev[0],prev[1],n,phi); break
                prev=(n,phi)
            rows.append((s,sc,cyc,dsc,td,openn,cross))
        summary[cfg+'|'+dl]=rows
        print("==",cfg,"delta=",dl)
        for r in rows: print("   s=%-7g SC=%s cyc=%s disk_sc=%s T(disk)=%s open=%d cross=%s"%(r[0],r[1][:8]+(['+%d'%(len(r[1])-8)] if len(r[1])>8 else []),r[2][:3]+(['+%d'%(len(r[2])-3)] if len(r[2])>3 else []),r[3],r[4],r[5],r[6]))
json.dump(summary,open("level_summary.json","w"),default=str)
