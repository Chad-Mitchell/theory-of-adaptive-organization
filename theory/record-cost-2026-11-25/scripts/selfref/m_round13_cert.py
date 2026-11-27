# Round 13-M: copositivity-style certificate for condition (diamond) on max(A,B), without vertex enumeration.
# Want x^T(-Q)x >= 0 on the cone {x : (e(x)f)(x) >= 0 for all facet effects e, f}, -Q = diag(mA+mB+mAmB, -mA I, -mB I, -mAmB I)
# (so x^T Q x = Phi when x0 = 1). Sufficient: -Q = F^T Lam F + S with Lam >= 0 entrywise, S PSD. Restrict Lam to be
# constant on classes of facet pairs (angle class of (e,e') in A) x (angle class of (f,f') in B) - still a valid certificate.
# Invariant matrices are block-scalar (Schur), so S PSD <=> 4 scalars >= 0: an LP. Maximise the smallest slack t.
import sys, numpy as np
from scipy.optimize import linprog
from m_round12_parts import PARTS
def classes(E):
    N=np.array([e[1:] for e in E]); G=np.round(N@N.T,8); vals=sorted(set(G.flatten().tolist()))
    return np.vectorize({v:k for k,v in enumerate(vals)}.get)(G), len(vals)
def blocks(M,dA,dB):
    M4=M.reshape(dA,dB,dA,dB); mA,mB=dA-1,dB-1
    return np.array([M4[0,0,0,0], np.trace(M4[1:,0,1:,0])/mA, np.trace(M4[0,1:,0,1:])/mB,
                     np.einsum('ijij->',M4[1:,1:,1:,1:])/(mA*mB)])
def run(na,nb):
    EA,EB=np.array(PARTS[na]()),np.array(PARTS[nb]()); dA,dB=EA.shape[1],EB.shape[1]; mA,mB=dA-1,dB-1
    cA,kA=classes(EA); cB,kB=classes(EB)
    cols=[]
    for p in range(kA):
        MA=sum(np.outer(EA[i],EA[j]) for i in range(len(EA)) for j in range(len(EA)) if cA[i,j]==p)
        for q in range(kB):
            MB=sum(np.outer(EB[i],EB[j]) for i in range(len(EB)) for j in range(len(EB)) if cB[i,j]==q)
            cols.append(blocks(np.kron(MA,MB),dA,dB))
    Mb=np.array(cols).T
    nQ=np.array([mA+mB+mA*mB,-mA,-mB,-mA*mB],float)
    s=np.abs(Mb).max(1); s[s==0]=1; Mn=Mb/s[:,None]; nQn=nQ/s
    K=Mb.shape[1]
    c=np.zeros(K+1); c[-1]=-1
    A_ub=np.hstack([Mn, np.ones((4,1))]); b_ub=nQn
    r=linprog(c,A_ub=A_ub,b_ub=b_ub,bounds=[(0,None)]*K+[(None,1)],method='highs')
    t=-r.fun if r.status==0 else float('nan')
    print(f"max({na},{nb}): {K} invariant multipliers; best min block slack t = {t:+.6g} -> {'CERTIFICATE: diamond holds on all of max' if t>1e-7 else ('boundary (t ~ 0): inconclusive' if abs(t)<=1e-7 else 'no certificate of this type')}", flush=True)
if __name__=="__main__":
    for s in (sys.argv[1:] or ['sqxsq','P5xP5','P6xP6','P7xP7','P8xP8','cube3xcube3','oct3xoct3','IxI','DxD','COxCO','IxD']):
        run(*s.split('x'))
