# Independent MC: full telegraph world + exact log-odds filter (Euler, dt), kappa=0.05 (lam=0.05, mu=N=1).
import numpy as np
rng=np.random.default_rng(143)
lam=0.05; dt=0.0005; C=4000; steps=240000; burn=20000
y=np.where(rng.random(C)<0.5,1.0,-1.0); L=np.zeros(C)
tsw=np.full(C,np.nan); res=[]
for t in range(steps):
    sw=rng.random(C)<lam*dt
    y=np.where(sw,-y,y)
    if t>=burn:
        # a new switch while waiting: discard pending event
        tsw=np.where(sw, t*dt, tsw)
    ds=y*dt+np.sqrt(dt)*rng.standard_normal(C)
    L=L+2*ds-2*lam*np.sinh(L)*dt
    if t>=burn:
        hit=(~np.isnan(tsw))&(np.sign(L)==np.sign(y))
        if hit.any():
            res.extend(((t+1)*dt-tsw[hit]).tolist()); tsw[hit]=np.nan
r=np.array(res); print("n",len(r),"mean",r.mean(),"se",r.std()/np.sqrt(len(r)))
