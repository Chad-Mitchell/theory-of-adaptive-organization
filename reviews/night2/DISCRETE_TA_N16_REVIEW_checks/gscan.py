import numpy as np, json
from bayes import grid_ta, cont_ta, C1, plugin
res={}
for k in [1e-4,1e-2]:
    T=cont_ta(k,'quiet'); res[k]={}
    for rho in [0.0025,0.005,0.01,0.02,0.04,0.08]:
        vals=[]
        for pf,m in [(0.4,10),(0.4,14)]:
            t,_=grid_ta(k,rho,'quiet',pf,m,9.0); vals.append(t)
        g=(vals[-1]-T)/np.sqrt(rho)
        res[k][rho]=dict(t=vals,g=g)
        print(k,rho,"t=%.9f (p-ref diff %.1e) g=%.5f g-C1=%.5f (g-C1)/sqrt(rho)=%.4f"%(vals[-1],vals[-1]-vals[0],g,g-C1,(g-C1)/np.sqrt(rho)),flush=True)
    r=np.array(sorted(res[k])); g=np.array([res[k][x]['g'] for x in r])
    A=np.c_[np.ones_like(r),np.sqrt(r),r]
    co=np.linalg.lstsq(A,g,rcond=None)[0]
    A2=np.c_[np.ones_like(r),np.sqrt(r)]; co2=np.linalg.lstsq(A2[:4],g[:4],rcond=None)[0]
    print("kappa",k,"fit g=c0+c1 sqrt(rho)+c2 rho:",co,"  2-term fit on 4 finest:",co2," C1=",C1,flush=True)
json.dump({str(k):{str(r):v for r,v in d.items()} for k,d in res.items()},open('gscan.json','w'),indent=1)
