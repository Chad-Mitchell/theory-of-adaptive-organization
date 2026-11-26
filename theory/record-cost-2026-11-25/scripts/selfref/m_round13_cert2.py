# Round 13-M: stronger certificate for (diamond) on max(A,B). Valid quadratic inequalities on max (circumradius 1, so each
# part's cone lies in the Lorentz cone L with J = diag(1,-1,...,-1)):
#   (i)  (e(x)f)(x) (e'(x)f')(x) >= 0                          [products of facet values]
#   (ii) y_e^T J_B y_e' >= 0, y_e = (e^T (x) I) x in K_B within L_B   [conditional states of B lie in its Lorentz cone]
#   (iii) x_f^T J_A x_f' >= 0, x_f = (I (x) f^T) x in K_A within L_A
# Certificate: -Q = sum lam_k M_k + sum nu_k N_k + S, lam, nu >= 0, S PSD; multipliers constant on angle classes; Schur => LP.
# t >= -1e-9 is a certificate (products are tight, so t <= 0 always).
import sys, numpy as np
from scipy.optimize import linprog
from m_round13_cert import classes, blocks
from m_round12_parts import PARTS
def run(na,nb):
    EA,EB=np.array(PARTS[na]()),np.array(PARTS[nb]()); dA,dB=EA.shape[1],EB.shape[1]; mA,mB=dA-1,dB-1
    cA,kA=classes(EA); cB,kB=classes(EB)
    JA=np.diag([1.0]+[-1.0]*mA); JB=np.diag([1.0]+[-1.0]*mB)
    MAs=[sum(np.outer(EA[i],EA[j]) for i in range(len(EA)) for j in range(len(EA)) if cA[i,j]==p) for p in range(kA)]
    MBs=[sum(np.outer(EB[i],EB[j]) for i in range(len(EB)) for j in range(len(EB)) if cB[i,j]==q) for q in range(kB)]
    cols=[blocks(np.kron(MA,MB),dA,dB) for MA in MAs for MB in MBs]
    cols+=[blocks(np.kron((MA+MA.T)/2,JB),dA,dB) for MA in MAs]
    cols+=[blocks(np.kron(JA,(MB+MB.T)/2),dA,dB) for MB in MBs]
    Mb=np.array(cols).T
    nQ=np.array([mA+mB+mA*mB,-mA,-mB,-mA*mB],float)
    s=np.abs(Mb).max(1); s[s==0]=1; Mn=Mb/s[:,None]; nQn=nQ/s; K=Mb.shape[1]
    c=np.zeros(K+1); c[-1]=-1
    r=linprog(c,A_ub=np.hstack([Mn,np.ones((4,1))]),b_ub=nQn,bounds=[(0,None)]*K+[(None,1)],method='highs')
    t=-r.fun if r.status==0 else float('nan')
    print(f"max({na},{nb}): {K} multipliers (facet-pair + Lorentz); best min block slack t = {t:+.3e} -> {'CERTIFICATE (diamond holds on all of max)' if t>-1e-9 else 'no certificate of this type'}", flush=True)
    return t, r
if __name__=="__main__":
    for s in (sys.argv[1:] or ['sqxsq','P5xP5','P6xP6','P7xP7','P8xP8','P5xP6','cube3xcube3','oct3xoct3','IxI','DxD','COxCO','IxD']):
        run(*s.split('x'))
