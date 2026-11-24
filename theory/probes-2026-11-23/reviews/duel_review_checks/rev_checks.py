"""Independent reviewer checks for the tracking duel (DUEL_REVIEW.md)."""
import json, numpy as np, collections, sys
sys.path.insert(0, '.')
import duel_core as d
rows = json.load(open('../fresh/checks/grid_results.json'))
print("R1 strict variant: is a1 (frozen) ever feasible in D/S1? (if never, strict 'WIN' = b feasible only)")
for reg in ['D','S1','S2']:
    c = collections.Counter((r['a1']['feas'], r['b']['feas']) for r in rows if r['reg']==reg)
    print(f"  {reg}: (a1 feas, b feas) counts {dict(c)}")

print("R2 FC2 D R-Hol: the 6 LOSE cells - which competitor?")
for r in rows:
    if r['reg']!='D' or not r['b']['feas'] or not r['a3']['feas']: continue
    for lam in [1e-4,1e-3,1e-2,1e-1]:
        Jb = lam*np.log(r['b']['K_used']) + r['b']['stake']; Ja = lam*np.log(r['N']) + r['a3']['stake']
        if Ja - Jb < -(0.01*max(Ja,Jb)):
            print(f"  T={r['T']} N={r['N']} eps={r['eps']} lam={lam}: J_b={Jb:.4f} J_a3={Ja:.4f}  stake b {r['b']['stake']:.4f} a3 {r['a3']['stake']:.4f}")

print("R3 a3 stake vs b stake: any cell where a3 has lower stake (P3 mechanism)?")
n=0
for r in rows:
    if r['b']['feas'] and r['a3']['feas'] and r['a3']['stake'] < r['b']['stake']: n+=1
print("  count:", n)

print("R4 S2 strict variant run literally per PREREG sec 6 (exclude a3 only; keep a1, c1)")
def lnK(k): return 0.0 if k<=1 else np.log(k)
def cmpJ(Jb,Jx):
    if Jb is None and Jx is None: return None
    if Jb is None: return 'LOSE'
    if Jx is None: return 'WIN'
    tol=0.01*max(Jb,Jx)+1e-12; dJ=Jx-Jb
    return 'WIN' if dJ>tol else ('LOSE' if dJ<-tol else 'TIE')
for readdef in ['R-Hol','R-Hardy']:
    for pricing in ['FC1','FC2']:
        cells=collections.Counter(); byT=collections.defaultdict(collections.Counter)
        for r in rows:
            if r['reg']!='S2': continue
            N=r['N']; kb = N*N if pricing=='FC1' else r['b'].get('K_used',2*N-1)
            for lam in [1e-4,1e-3,1e-2,1e-1]:
                Jb = lam*lnK(kb)+r['b']['stake'] if r['b']['feas'] else None
                Ja = lam*lnK(N)+r['a1']['stake'] if r['a1']['feas'] else None
                res=[cmpJ(Jb,Ja)]
                if readdef=='R-Hol':
                    Jc = lam*lnK(2*N-1)+r['b']['stake'] if r['b']['feas'] else None
                    res.append(cmpJ(Jb,Jc))
                v=[x for x in res if x is not None]
                if not v: continue
                o='LOSE' if 'LOSE' in v else ('WIN' if all(x=='WIN' for x in v) else 'TIE')
                cells[o]+=1; byT[r['T']][o]+=1
        n=sum(cells.values())
        lab='WIN' if cells['WIN']/n>=0.9 and cells['LOSE']==0 else ('LOSE' if cells['LOSE']/n>=0.5 else ('TIE' if cells['TIE']/n>=0.9 else 'MIXED'))
        print(f"  S2 {readdef} {pricing} strict: {lab} {dict(cells)} | by tau {dict((k,dict(v)) for k,v in sorted(byT.items()))}")

print("R5 a3 with a constant offset (PREREG sec 4 says 'offset optimized'; code uses offset 0) and a finer rate grid, regime D, exact bin arithmetic")
def a3_exact(N, r, delta, T):
    ts = np.unique(np.concatenate([np.linspace(0,T,2001), np.geomspace(1e-5*T,T,800)]))
    z = np.exp(r*ts*(np.exp(-2j*np.pi/N)-1.0))*np.exp(2j*np.pi*ts)*np.exp(-1j*delta)
    stake = 1 - np.trapezoid(np.sinc(1.0/N)*np.real(z), ts)/T
    w = 2*np.pi/N
    def L(c):  # fraction of uniform [c-w/2,c+w/2] (wrapped) with |x|>pi/2
        a=c-w/2; b=c+w/2; tot=0
        for sh in (-2*np.pi,0,2*np.pi):
            lo=np.maximum(a+sh,-np.pi/2); hi=np.minimum(b+sh,np.pi/2); tot+=np.clip(hi-lo,0,None)
        return 1-tot/w
    tt = np.unique(np.concatenate([[0.0], np.geomspace(1e-3*T,T,60), np.linspace(0,T,60)]))
    tail=0
    for t in tt:
        q = d.a_jump_dist(N, r, t); cen = d.wrap(2*np.pi*t-2*np.pi*np.arange(N)/N - delta)
        tail=max(tail, float(np.sum(q*np.array([L(c) for c in cen]))))
    return stake, tail
NS=[2,3,4,5,6,8,12,16,24,32,48,64]; flips=0; checked=0
for T in [0.25, 1, 10]:
    for N in NS:
        rstar = 2*np.pi/np.sin(2*np.pi/N) if N>=3 else 2*np.pi*N
        cands=[]
        for f in np.geomspace(0.2,5,25):
            for delta in np.linspace(-np.pi/N, np.pi/N, 9) + (0 if True else 0):
                cands.append((f*rstar,delta)+a3_exact(N,f*rstar,delta,T))
        for eps in [0.05,1e-2,1e-3]:
            row=[r for r in rows if r['reg']=='D' and r['T']==T and r['N']==N and r['eps']==eps][0]
            feas=[c for c in cands if c[3]<=eps]
            best = min(feas,key=lambda c:c[2]) if feas else None
            old = row['a3']
            checked+=1
            newf = best is not None
            if newf != old['feas'] or (newf and best[2] < old['stake']-0.01*old['stake']):
                flips+=1
                print(f"  CHANGE T={T} N={N} eps={eps}: old feas={old['feas']} stake={old['stake']:.4f} -> new feas={newf} stake={(best[2] if best else float('nan')):.4f} (r/r*={(best[0]/rstar if best else 0):.2f}, delta={(best[1] if best else 0):.3f}); b feas={row['b']['feas']} stake={row['b']['stake']}")
print(f"  rows checked {checked}, rows where offset/finer-rate a3 changes feasibility or improves stake >1%: {flips}")
