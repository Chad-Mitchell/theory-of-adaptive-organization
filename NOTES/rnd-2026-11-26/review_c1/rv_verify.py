# Independent checks of the C1 vacua and entropies (hostile review). OBSERVED numerics.
import sys, itertools, numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spl
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA
def Hreal(L, flux, m, gauge='y', bc=(-1,-1)):
    """Real-space single-particle H on an L x L torus with boundary phases bc. gauge 'y': y-bond sign (-1)^x (as C1);
    gauge 'x': x-bond sign (-1)^y (independent gauge)."""
    idx=lambda x,y:(x%L)+L*(y%L); H=np.zeros((L*L,L*L))
    for x in range(L):
        for y in range(L):
            i=idx(x,y); H[i,i]+=m*(-1)**(x+y)
            tx=((-1)**y if (flux and gauge=='x') else 1.0); ty=((-1)**x if (flux and gauge=='y') else 1.0)
            for (dx,dy,t,b) in [(1,0,tx,bc[0] if x==L-1 else 1),(0,1,ty,bc[1] if y==L-1 else 1)]:
                j=idx(x+dx,y+dy); H[i,j]+=-t*b; H[j,i]+=-t*b
    return H
def Cproj(H, mu=0.0):
    E,U=np.linalg.eigh(H); occ=E<mu
    return U[:,occ]@U[:,occ].T, E
out=[]
pr=lambda *s: (print(*s,flush=True), out.append(' '.join(str(x) for x in s)))
# ---- 1. Many-body exact diagonalisation vs correlation-matrix (Peschel) entropy, 4x4 torus, N=8 ----
L=4; Ns=L*L; T=[(0,0),(1,0),(0,1),(1,1)]
for (flux,m,lab) in [(True,0.5,'pi-flux m=0.5'),(False,0.5,'NN m=0.5'),(True,0.0,'pi-flux m=0 (APBC)')]:
    H1=Hreal(L,flux,m,bc=(-1,-1)); E1=np.linalg.eigvalsh(H1)
    gapN=E1[8]-E1[7]
    states=[s for s in range(1<<Ns) if bin(s).count('1')==8]; pos={s:i for i,s in enumerate(states)}
    rows=[];cols=[];vals=[]
    for a,s in enumerate(states):
        for i in range(Ns):
            for j in range(Ns):
                h=H1[i,j]
                if h==0: continue
                if i==j:
                    if s>>i&1: rows.append(a);cols.append(a);vals.append(h)
                    continue
                # c_i^dag c_j
                if not (s>>j&1) or (s>>i&1): continue
                s2=s^(1<<j); sign=(-1)**bin(s2&((1<<j)-1)).count('1')
                s3=s2|(1<<i); sign*=(-1)**bin(s2&((1<<i)-1)).count('1')
                rows.append(pos[s3]);cols.append(a);vals.append(h*sign)
    Hm=sp.csr_matrix((vals,(rows,cols)),shape=(len(states),)*2)
    w,V=spl.eigsh(Hm,k=2,which='SA'); psi=V[:,np.argmin(w)]
    def S_mb(region):
        # reduced density matrix by tracing complement (fermion ordering: region sites first via Jordan-Wigner reordering)
        reg=[ (x%L)+L*(y%L) for x,y in region]; rest=[i for i in range(Ns) if i not in reg]; order=reg+rest
        rho=np.zeros((1<<len(reg),)*2)
        amp={}
        for a,s in enumerate(states):
            if abs(psi[a])<1e-14: continue
            # permutation sign to reorder modes into 'order'
            occ=[i for i in range(Ns) if s>>i&1]; newpos=[order.index(i) for i in occ]
            perm=np.argsort(newpos); sgn=np.linalg.det(np.eye(len(perm))[perm]) if len(perm) else 1
            ra=sum(1<<k for k,i in enumerate(reg) if s>>i&1); rb=sum(1<<k for k,i in enumerate(rest) if s>>i&1)
            amp.setdefault(rb,{})[ra]=amp.setdefault(rb,{}).get(ra,0)+sgn*psi[a]
        for rb,d in amp.items():
            vec=np.zeros(1<<len(reg))
            for ra,c in d.items(): vec[ra]=c
            rho+=np.outer(vec,vec)
        ev=np.linalg.eigvalsh(rho); ev=ev[ev>1e-14]; return float(-(ev*np.log2(ev)).sum())
    C,_=Cproj(H1); Cg=lambda reg: C[np.ix_([(x%L)+L*(y%L) for x,y in reg],[(x%L)+L*(y%L) for x,y in reg])]
    S6=[(2,0),(0,2)]
    pr(f"[ED 4x4 {lab}] single-particle gap at N=8: {gapN:.3f}; S(T): ED {S_mb(T):.10f} vs corr-matrix {S_bits(Cg(T)):.10f};",
       f"S(T+2 sites): ED {S_mb(T+S6):.10f} vs corr {S_bits(Cg(T+S6)):.10f}")
# ---- 2. C1 k-space vacua vs direct real-space diagonalisation (L=64 sites, APBC), independent gauge for pi-flux ----
regs={'T':T,'T+ring8':T+[(-1,0),(-1,1),(2,0),(2,1),(0,-1),(1,-1),(0,2),(1,2)],'far pair':[(5,3),(-4,2)],'diag strip':[(k,k) for k in range(-3,5)]+[(k+1,k) for k in range(-3,4)]}
for i,(name,(flux,m)) in enumerate(VACUA.items()):
    v=Vacuum(flux,m)
    for gauge in (['y','x'] if flux else ['y']):
        Lr=64; C,E=Cproj(Hreal(Lr,flux,m,gauge=gauge,bc=(-1,-1)))
        # zero-energy degeneracy check for the finite lattice
        zero=(np.abs(E)<1e-9).sum()
        sh=lambda p:((p[0]+20)%Lr)+Lr*((p[1]+20)%Lr)
        res=[]
        for rn,R in regs.items():
            Sk=S_bits(v.P(R)); Sr=S_bits(C[np.ix_([sh(p) for p in R],[sh(p) for p in R])]); res.append(f"{rn}: k {Sk:.6f} / real {Sr:.6f} (d={Sk-Sr:+.1e})")
        pr(f"[k vs real L=64 APBC, gauge {gauge}] {name}: zero modes(real)={zero}; "+'; '.join(res))
# ---- 3. zero modes / filling of the C1 k-grid, and sublattice zeros of C ----
for name,(flux,m) in VACUA.items():
    v=Vacuum(flux,m); pts=[(x,y) for x in range(-4,5) for y in range(-4,5)]
    P=v.P([(0,0)]+pts); row=np.abs(P[0,1:])
    ev=max(row[k] for k,p in enumerate(pts) if (p[0]+p[1])%2==0 and p!=(0,0)); od=max(row[k] for k,p in enumerate(pts) if (p[0]+p[1])%2==1)
    imag=np.abs(v.P(pts).imag).max()
    pr(f"[grid K=256] {name}: min|E|={v.minabsE:.2e}, filling={v.filling:.6f}; max|C(0,r)| even x+y (r!=0): {ev:.2e}, odd: {od:.3f}; max |Im P| (gauge-real check) {imag:.1e}")
for Kc in (64,128,256,512):
    v=Vacuum(False,0.0,K=Kc); pr(f"[V1 zero modes] K={Kc}: min|E|={v.minabsE:.2e}; filling={v.filling:.8f}; S(T)={S_bits(v.P(T)):.8f}")
open('rv_verify.out','w').write('\n'.join(out)+'\n')
