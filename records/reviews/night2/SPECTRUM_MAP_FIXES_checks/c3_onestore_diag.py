"""Diagnosis (pick 26), NOT an independent check: executes the committed SPECTRUM_MAP/checks/c3_layers.py model unchanged and
only adds a bounded 1-D optimisation of the single store rate (c3 fits K = 1 on a 5-point grid with no polish). Run from this folder."""
import os; C3=os.path.join(os.path.dirname(os.path.abspath(__file__)),"../SPECTRUM_MAP/checks/")
import sys; sys.argv=["x","1.9"]
src=open(C3+"c3_layers.py").read().split("out={}")[0]; exec(src)
import numpy as np
from scipy.optimize import minimize_scalar
for a,L in ((1.9,2),(1.95,2),(2.05,2),(1.9,4)):
    Sx,Nd,eopt=setup(a,L); e_grid,l=best_K(a,L,1)
    o=minimize_scalar(lambda ll:mse_for_rates([np.exp(ll)],Sx,Nd),bounds=(np.log(10.0**(-L-1)/TAU_C),0),method="bounded",options=dict(xatol=1e-6))
    print(a,L,"c3 grid K=1:",f"{e_grid:.3g}","rate",l,"| polished rate:",f"{(o.fun-eopt)/eopt:.3g}",np.exp(o.x))
