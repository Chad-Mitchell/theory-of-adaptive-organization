"""Counterexample check for SCALE_ENDS E3 as first written ('zero entropy production => no held information
about a drifting variable'). Two-state receptor (state 1 = bound), energy of bound state e(t) = A*sin(w t) in kT,
relaxation rate g. The driver does work; dissipated work per cycle W_diss = W - dF (dF = 0 over a cycle).
Expect W_diss -> 0 as w/g -> 0 while the mutual information between state and phase stays finite.
Run: nice -n 19 python3 e3_counterexample.py"""
import numpy as np
A,g=2.0,1.0
def run(w,cycles=20,n=20000):
    T=2*np.pi/w; t=np.linspace(0,cycles*T,cycles*n); dt=t[1]-t[0]
    e=A*np.sin(w*t); peq=1/(1+np.exp(e)); p=np.empty_like(t); p[0]=peq[0]
    for i in range(1,len(t)): p[i]=p[i-1]+dt*g*(peq[i-1]-p[i-1])
    de=np.diff(e); W=np.sum(p[:-1]*de)           # work = sum p * d(energy of bound state)
    last=slice((cycles-1)*n,cycles*n); Wc=np.sum(p[last][:-1]*np.diff(e[last]))
    # MI between state and phase (phase uniform over the last cycle)
    pp=p[last]; H=lambda x: -(x*np.log(x)+(1-x)*np.log(1-x))
    pm=pp.mean(); MI=H(pm)-np.mean(H(pp))
    return Wc,MI
for w in [1.0,0.3,0.1,0.03,0.01]:
    Wc,MI=run(w); print(f"w/g={w:<5} dissipated work per cycle = {Wc:.5f} kT ; I(state;phase) = {MI:.4f} nats")
