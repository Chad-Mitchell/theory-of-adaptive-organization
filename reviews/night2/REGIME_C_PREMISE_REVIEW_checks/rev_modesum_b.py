# Reviewer's own mode sum: B(s)=sum_i G(s i^-beta), G from rev_rd json (BA), head beyond table by
# Shannon slope 1/2 per ln u (capped at entropy for discrete shapes). Local exponent d lnB/d ln s at s=1e3.
import numpy as np, json, sys
N=2_000_000; i=np.arange(1,N+1,dtype=float)
for name in sys.argv[1:]:
    d=json.load(open(f'/tmp/rev18/chk/rev_rd_{name}.json'))[name]; us=d['ustar']
    U=np.array([a for a,b in d['G']]); G=np.maximum(np.array([b for a,b in d['G']]),0)
    H={'bern02':-(.8*np.log(.8)+.2*np.log(.2)),'three':-(.3*np.log(.3)+.6*np.log(.6)+.1*np.log(.1))}.get(name,np.inf)
    def g(u):
        out=np.zeros_like(u); m=(u>U[0])&(u<=U[-1]); out[m]=np.interp(np.log(u[m]),np.log(U),G)
        h=u>U[-1]; out[h]=np.minimum(G[-1]+0.5*np.log(u[h]/U[-1]),H); return out
    res={}
    for beta,s0 in ((0.6,1e2),(1.5,1e5),(2.0,1e5),(2.0,1e6)):
        B=lambda s: g(s*i**-beta).sum()
        s=s0; e=np.log(B(1.1*s)/B(s/1.1))/np.log(1.21)
        res[(beta,s0)]=(round(e,4),round(1/beta,4),round(B(s),1))
    print(name,'u*=%.4f'%us,res,flush=True)
