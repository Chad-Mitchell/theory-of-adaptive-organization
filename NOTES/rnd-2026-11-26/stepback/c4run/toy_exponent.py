# NON-SCORED: the Draft C exponent observable is blind to the planted effect; R(s) is not.
import subprocess, math, numpy as np
from c4r_decide import parse
from scipy.optimize import minimize_scalar
out={}
for cp in (1.0,1.96):
    for T in (0.25,0.5,1.0):
        lines=[subprocess.run(['./c4r_sprinkle',str(T),'2000000',str(cp),str(s)],capture_output=True,text=True).stdout for s in range(700,708)]
        out[(cp,T)]=parse(lines)
for cp in (1.0,1.96):
    for s in (0.0,0.5,0.9):
        Ts=np.array([0.25,0.5,1.0]); Ls=np.array([np.mean([r['L%.2f'%s] for r in out[(cp,T)]]) for T in Ts]); tau=Ts*math.sqrt(1-s*s)
        b=np.polyfit(np.log(tau),np.log(Ls),1)[0]
        print(f"cp={cp}: Draft C exponent of L vs tau (c=1) at s={s}: {b:.4f}")
# C4'' descriptive: best single c' for the toy lattice R(s)
L=parse(open('toy/lattice_T4000.txt')); rays=[0.25,0.5,0.75,0.9]
Rl={s:np.mean([r['L%.2f'%s]/(r['L0.00']*math.sqrt(1-s*s)) for r in L]) for s in rays}
f=lambda c:sum((Rl[s]-math.sqrt(1-(s/c)**2)/math.sqrt(1-s*s))**2 for s in rays)
m=minimize_scalar(f,bounds=(1.01,5),method='bounded')
print("toy lattice R(s):",{s:round(v,4) for s,v in Rl.items()},f"; best-fit sprinkling light speed c'={m.x:.3f}, residuals",{s:round(Rl[s]-math.sqrt(1-(s/m.x)**2)/math.sqrt(1-s*s),4) for s in rays})
