"""Diagnosis (pick 26), NOT an independent check: executes the committed SPECTRUM_MAP/checks/c3_layers.py model unchanged and
only adds a bounded 1-D optimisation of the single store rate (c3 fits K = 1 on a 5-point grid with no polish). Run from this folder."""
import os; C3=os.path.join(os.path.dirname(os.path.abspath(__file__)),"../SPECTRUM_MAP/checks/")
import sys,json; sys.argv=["x","1.5"]
src=open(C3+"c3_layers.py").read().split("out={}")[0]; exec(src)
import numpy as np
from scipy.optimize import minimize_scalar
res={}
for a in (1.5,2.5):
    com=json.load(open(C3+f"c3_layers_{a}.json"))
    for L in (1,2,3,4):
        Sx,Nd,eopt=setup(a,L)
        o=minimize_scalar(lambda ll:mse_for_rates([np.exp(ll)],Sx,Nd),bounds=(np.log(10.0**(-L-1)/TAU_C),0),method="bounded",options=dict(xatol=1e-6))
        e1=max((o.fun-eopt)/eopt,0); ex=com[f"alpha{a}_L{L}"]["rel_excess"]; ex2=[min(e1,ex[0])]+ex[1:]
        ks={str(p):int(np.argmin([p*x+K for K,x in zip(range(1,7),ex2)]))+1 for p in (1e2,1e3,1e4,1e5)}
        ko={str(p):com[f"alpha{a}_L{L}"][f"Kstar_psi{p:.0e}"] for p in (1e2,1e3,1e4,1e5)}
        res[f"a{a}_L{L}"]=dict(K1_committed=ex[0],K1_polished=float(f"{e1:.3g}"),Kstar_committed=ko,Kstar_with_polished_K1=ks)
        print(f"a{a}_L{L}",json.dumps(res[f"a{a}_L{L}"]))
json.dump(res,open("c3_kstar_diag.json","w"),indent=1)
