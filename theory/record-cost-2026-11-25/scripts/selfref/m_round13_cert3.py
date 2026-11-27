# Round 13-M: certificate (cert2) plus Lorentz pairings over a larger set W_X of dual vectors: facet effects and the
# unit-circumsphere directions (1, v) for v a vertex (and optionally a facet-normal direction), all in K_X*.
#   (iii') x_g^T J_A x_g' >= 0 for g, g' in W_B  (x_g = (I (x) g^T) x in K_A within L_A); (ii') symmetric.
import sys, numpy as np
from scipy.optimize import linprog
from m_round13_cert import blocks
from m_round12_parts import PARTS, ICO, DOD, CUBOCT, polygon
VERTS={'I':ICO,'D':DOD,'CO':CUBOCT}
def verts(name, E):
    if name in VERTS: return VERTS[name]
    import cdd
    m=cdd.matrix_from_array([list(e) for e in E],rep_type=cdd.RepType.INEQUALITY)
    G=np.array(cdd.copy_generators(cdd.polyhedron_from_matrix(m)).array); return G[:,1:]/G[:,[0]]
def Wset(name,E,mode):
    E=np.array(E); out=[(0,e) for e in E]
    if 'v' in mode: out+=[(1,np.concatenate([[1],v/np.linalg.norm(v)])) for v in verts(name,E)]
    if 'n' in mode: out+=[(2,np.concatenate([[1],e[1:]/np.linalg.norm(e[1:])])) for e in E]
    return out
def cls(W):
    d={}; lab=np.zeros((len(W),len(W)),int)
    for i,(ti,wi) in enumerate(W):
        for j,(tj,wj) in enumerate(W):
            key=(min(ti,tj),max(ti,tj),round(float(wi[1:]@wj[1:]),8)); lab[i,j]=d.setdefault(key,len(d))
    return lab,len(d)
def run(na,nb,mode='vn'):
    EA,EB=np.array(PARTS[na]()),np.array(PARTS[nb]()); dA,dB=EA.shape[1],EB.shape[1]; mA,mB=dA-1,dB-1
    JA=np.diag([1.0]+[-1.0]*mA); JB=np.diag([1.0]+[-1.0]*mB)
    def grp(V,lab,k): return [sum(np.outer(V[i],V[j]) for i in range(len(V)) for j in range(len(V)) if lab[i,j]==p) for p in range(k)]
    lA=np.array([[1 if (a@b)>0 else 0 for b in EA] for a in EA])
    from m_round13_cert import classes
    cA,kA=classes(EA); cB,kB=classes(EB)
    MAs=grp(EA,cA,kA); MBs=grp(EB,cB,kB)
    WA=Wset(na,EA,mode); WB=Wset(nb,EB,mode)
    lWA,kWA=cls(WA); lWB,kWB=cls(WB)
    NA=grp([w for _,w in WA],lWA,kWA); NB=grp([w for _,w in WB],lWB,kWB)
    cols=[blocks(np.kron(MA,MB),dA,dB) for MA in MAs for MB in MBs]
    cols+=[blocks(np.kron((N+N.T)/2,JB),dA,dB) for N in NA]
    cols+=[blocks(np.kron(JA,(N+N.T)/2),dA,dB) for N in NB]
    Mb=np.array(cols).T
    nQ=np.array([mA+mB+mA*mB,-mA,-mB,-mA*mB],float)
    s=np.abs(Mb).max(1); s[s==0]=1; Mn=Mb/s[:,None]; nQn=nQ/s; K=Mb.shape[1]
    c=np.zeros(K+1); c[-1]=-1
    r=linprog(c,A_ub=np.hstack([Mn,np.ones((4,1))]),b_ub=nQn,bounds=[(0,None)]*K+[(None,1)],method='highs')
    t=-r.fun if r.status==0 else float('nan')
    lam=r.x[:-1]; resid=nQ-Mb@lam
    print(f"max({na},{nb}) W={mode}: {K} multipliers; t = {t:+.3e}; residual blocks of S = {np.array2string(resid,precision=4)} -> {'CERTIFICATE' if t>-1e-9 and resid.min()>-1e-9 else 'no certificate of this type'}", flush=True)
if __name__=="__main__":
    for s in (sys.argv[1:] or ['P6xP6','COxCO','IxI','DxD','IxD']):
        for mode in ('v','n','vn'):
            run(*s.split('x'),mode=mode)
