import sys,json,numpy as np,pandas as pd,glob
sys.path.insert(0,'layers'); from layerlib import *
for p in sorted(glob.glob("layers/curve_*.csv")):
    c=pd.read_csv(p); t=c.t.values; f=c.f.values
    if len(t)<5: continue
    row=[]
    for s in (1,1.5,2,2.5,3):
        m=t<=t.min()*10**s
        if t[m].max()<t.min()*10**(s-0.1): break
        rms=[fitK(t[m],f[m],K)[0] for K in range(1,9)]
        def ks(tol): 
            for i,r in enumerate(rms):
                if r<=tol: return i+1
            return 9
        row.append((s,ks(0.02),ks(0.03),ks(0.05),round(min(rms),3)))
    print(p.split('curve_')[1][:-4],row)
