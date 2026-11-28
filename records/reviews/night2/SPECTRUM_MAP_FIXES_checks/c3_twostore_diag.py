"""Diagnosis (pick 26), NOT an independent check: executes the committed SPECTRUM_MAP/checks/c3_layers.py model unchanged and
only adds a bounded 1-D optimisation of the single store rate (c3 fits K = 1 on a 5-point grid with no polish). Run from this folder."""
import os; C3=os.path.join(os.path.dirname(os.path.abspath(__file__)),"../SPECTRUM_MAP/checks/")
import sys,json; sys.argv=["x","2"]
src=open(C3+"c3_layers.py").read().split("out={}")[0]; exec(src)
import numpy as np
from scipy.optimize import minimize_scalar
r={}
for a in (1.95,2.05):
  for L in (2,3,4):
    Sx,Nd,eopt=setup(a,L)
    o=minimize_scalar(lambda ll:mse_for_rates([np.exp(ll)],Sx,Nd),bounds=(np.log(10.0**(-L-1)/TAU_C),0),method="bounded",options=dict(xatol=1e-6))
    e1=(o.fun-eopt)/eopt; e2=best_K(a,L,2)[0]
    r[f"a{a}_L{L}"]=dict(e1=float(f"{e1:.3g}"),e2=float(f"{e2:.3g}"),Kstar_psi1e4=1 if 1e4*e1+1<=1e4*e2+2 else 2,psi_for_two=float(f"{1/(e1-e2):.3g}"))
    print(f"a{a}_L{L}",r[f"a{a}_L{L}"])
json.dump(r,open("c3_twostore_diag.json","w"),indent=1)
