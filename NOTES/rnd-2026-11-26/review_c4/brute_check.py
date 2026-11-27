# Independent brute-force check of C4 section 1 (closure == nearest-neighbour increasing paths)
# and of the DP used in c4_lpp.c, built from the literal dependency rule.
import random, itertools
def instance(W,T,seed):
    R=random.Random(seed); recs=[(0.0,0)]  # origin record at site 0, time 0
    for i in range(-W,W+1):
        t=0.0
        while True:
            t+=R.expovariate(1.0)
            if t>T: break
            recs.append((t,i))
    recs.sort(); return recs
def closure_longest(recs):
    n=len(recs); idx={r:k for k,r in enumerate(recs)}
    # literal dependency: latest earlier record at site-1, site, site+1
    deps=[[] for _ in range(n)]
    for k,(t,i) in enumerate(recs):
        for j in (i-1,i,i+1):
            cand=[m for m in range(k) if recs[m][1]==j]
            if cand: deps[k].append(cand[-1])
    # transitive closure (ancestors) as sets
    anc=[set() for _ in range(n)]
    for k in range(n):
        for d in deps[k]: anc[k]|=anc[d]|{d}
    o=idx[(0.0,0)]
    # longest chain from origin in the poset: DP over closure relation
    L=[0]*n
    for k in range(n):
        if k==o: L[k]=1; continue
        if o in anc[k]:
            L[k]=1+max(L[m] for m in anc[k] if m==o or o in anc[m])
    return recs,anc,L,o
def path_relation(recs,a,b):
    # e<e' iff increasing-time path with |dsite|<=1 through records
    reach={a}; 
    for k in range(a+1,len(recs)):
        if any(abs(recs[k][1]-recs[m][1])<=1 for m in reach if recs[m][0]<recs[k][0]): reach.add(k)
    return b in reach
def dp_longest(recs):
    best={}; best[0]=1; out={}
    for (t,i) in recs[1:]:
        m=max(best.get(i-1,0),best.get(i,0),best.get(i+1,0))
        if m>0: best[i]=m+1; out[(t,i)]=m+1
    return out
bad=0
for seed in range(40):
    recs=instance(3,4.0,seed); recs,anc,L,o=closure_longest(recs)
    n=len(recs)
    for a in range(n):
        for b in range(a+1,n):
            if (a in anc[b])!=path_relation(recs,a,b): bad+=1
    out=dp_longest(recs)
    for k,r in enumerate(recs):
        if k==o: continue
        if L[k]!=out.get(r,0): bad+=1
print("instances=40 mismatches=",bad)
