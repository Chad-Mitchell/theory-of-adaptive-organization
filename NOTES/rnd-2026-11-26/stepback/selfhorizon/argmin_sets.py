# A(T) for the five configurations, T=1..400, with tie tolerance 1e-12 relative. Disk included in every menu.
import numpy as np, json
d=np.load("curves_sh.npz"); N=d['n']; M3=d['m3h']; MX=d['mix']
E=np.load("../sr_b4/curves_even.npy"); En=E[:,0].astype(int); EJ=E[:,1:]
T=np.arange(1,401); disk=T*np.sin(np.pi/(2*T))**2
dense_even_max=4000; dense_odd_max=4001
def build(cfg):
    rows=[]; labels=[]
    rule = 'M3h' if 'M3h' in cfg or cfg=='O' else 'MIX'
    for i,n in enumerate(N):
        if cfg.startswith('E') and n%2: continue
        if cfg=='O' and n%2==0: continue
        rows.append((M3 if rule=='M3h' else MX)[i]); labels.append(int(n))
    if rule=='M3h' and cfg[0] in 'EF':   # even grid beyond 4000 (M3h only; mixed-rule even n are >= disk, PIM, so irrelevant)
        for i,n in enumerate(En):
            if n>4000: rows.append(EJ[i]); labels.append(int(n))
    rows.append(disk); labels.append(0)   # 0 = disk
    return np.array(rows), labels
out={}
for cfg in ['E-M3h','E-mixed','O','F-M3h','F-mixed']:
    R,L=build(cfg); mn=R.min(0); A={}
    edge=[]
    for t in range(400):
        idx=np.where(R[:,t]<=mn[t]*(1+1e-12))[0]; A[t+1]=[L[i] for i in idx]
        for i in idx:
            n=L[i]
            if n and ((n%2==0 and n>=dense_even_max-1) or (n%2 and n>=dense_odd_max-1)): edge.append((t+1,n))
        # second best gap for precision check
    gaps=[]
    for t in range(1,400):
        s=np.sort(R[:,t]); gaps.append((s[1]-s[0])/s[0])
    out[cfg]={'A':A,'edge':edge,'min_rel_gap_T2_400':float(min(gaps))}
    sample={t:A[t] for t in [1,2,3,4,5,10,20,50,100,200,300,400]}
    print(cfg,'| sizes>1 at T>=2:',sum(1 for t in range(2,401) if len(A[t])>1),'| edge hits:',len(edge),'| min rel gap 1st-2nd (T>=2): %.3g'%min(gaps))
    print('   ',{t:(v if len(v)<6 else str(len(v))+' tied') for t,v in sample.items()})
    print('    max polygon in any A(T), T>=2:', max(max([x for x in A[t] if x] or [0]) for t in range(2,401)))
json.dump(out,open("argmin_sets.json","w"))
