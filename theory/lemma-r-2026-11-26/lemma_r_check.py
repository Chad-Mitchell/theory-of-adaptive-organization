# Sanity checks for LEMMA_R.md (OBSERVED numerical, float with tolerance 1e-9; not a proof)
import numpy as np, itertools, sys
def poly(n):  # homogeneous vertex vectors (1, cos, sin) of a regular n-gon; n=2 -> segment (classical bit)
    if n==2: return [np.array([1.,1.]),np.array([1.,-1.])]   # K=2
    return [np.array([1.,np.cos(2*np.pi*k/n),np.sin(2*np.pi*k/n)]) for k in range(n)]
def simplex(n): return [np.eye(n)[k] for k in range(n)]        # classical n-level, K=n
def octa(): return [np.array([1.]+list(s*np.eye(3)[i])) for i in range(3) for s in (1,-1)]  # K=4
def prod(A,B): return [(i,j,np.kron(a,b)) for i,a in enumerate(A) for j,b in enumerate(B)]
def rank(M): return np.linalg.matrix_rank(np.array(M),tol=1e-9)
def d4(A,B):
    P=prod(A,B); bad=0; tot=0
    for Y in itertools.combinations(P,4):
        I={y[0] for y in Y}; J={y[1] for y in Y}
        if len(I)>1 and len(J)>1:
            tot+=1
            if rank([y[2] for y in Y])<4: bad+=1
    return tot,bad
def lin_aut(X):
    X=[np.asarray(x) for x in X]; N=len(X); d=len(X[0])
    G=sum(np.outer(x,x) for x in X); Gi=np.linalg.inv(G)
    K=np.array([[X[i]@Gi@X[j] for j in range(N)] for i in range(N)])
    base=[]; 
    for i in range(N):
        if rank([X[b] for b in base]+[X[i]])>len(base): base.append(i)
        if len(base)==d: break
    Bm=np.array([X[b] for b in base]).T; Bi=np.linalg.inv(Bm)
    Xm=np.array(X)
    cnt=0; elems=[]
    def rec(k,img):
        nonlocal cnt
        if k==d:
            T=np.array([X[j] for j in img]).T@Bi
            Y=(T@Xm.T).T
            perm=[]
            for y in Y:
                m=np.where(np.abs(Xm-y).max(1)<1e-7)[0]
                if len(m)!=1: return
                perm.append(m[0])
            if len(set(perm))==N: cnt+=1; elems.append(perm)
            return
        b=base[k]
        for c in range(N):
            if c in img: continue
            if abs(K[c,c]-K[b,b])>1e-9: continue
            if any(abs(K[c,img[t]]-K[b,base[t]])>1e-9 for t in range(k)): continue
            rec(k+1,img+[c])
    rec(0,[]); return cnt,elems
def classify(A,B,elems,nA,nB):
    # count elements mapping every row to a row/col and every col to a row/col  (local-or-swap shape)
    P=[(i,j) for i in range(nA) for j in range(nB)]
    loc=0
    for perm in elems:
        img=[P[p] for p in perm]
        ok=True; ra=None
        rows_to=set(); 
        for i in range(nA):
            S={img[i*nB+j] for j in range(nB)}
            if len({s[0] for s in S})==1: rows_to.add('row')
            elif len({s[1] for s in S})==1: rows_to.add('col')
            else: ok=False
        for j in range(nB):
            S={img[i*nB+j] for i in range(nA)}
            if not(len({s[0] for s in S})==1 or len({s[1] for s in S})==1): ok=False
        if ok: loc+=1
    return loc
cases=[("square^2",poly(4),poly(4)),("pentagon^2",poly(5),poly(5)),("hexagon^2",poly(6),poly(6)),
       ("pentagon x heptagon",poly(5),poly(7)),("square x pentagon",poly(4),poly(5)),
       ("heptagon^2",poly(7),poly(7)),
       ("bit x pentagon (n_A=2, excluded)",poly(2),poly(5)),("trit x pentagon (n_A=3, excluded)",simplex(3),poly(5)),
       ("octahedron^2 (K=4, not a polygon)",octa(),octa()),("bit^2",poly(2),poly(2))]
for name,A,B in cases:
    tot,bad=d4(A,B)
    cnt,el=lin_aut([p[2] for p in prod(A,B)])
    loc=classify(A,B,el,len(A),len(B))
    print(f"{name:36s} mixed4-sets={tot:6d} dependent={bad:4d} | #linear maps with T(P)=P = {cnt:6d} | of which rows/cols->rows/cols = {loc}")
    sys.stdout.flush()
