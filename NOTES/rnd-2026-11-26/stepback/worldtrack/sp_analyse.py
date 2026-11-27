import json,sys,numpy as np,collections
for fn in sys.argv[1:]:
    R=[json.loads(l) for l in open(fn)]
    C=collections.defaultdict(list)
    for r in R: C[(r['cls'],r['smin'],r['c'],r['arm'])].append(r)
    worst=[]
    for k,v in sorted(C.items()):
        n=len(v); u1f=sum(r['nfar']>0 for r in v if not r['blind']); u2=sum(r['nprof']==1 for r in v); e=sum(r['edge'] for r in v); b=sum(r['blind'] for r in v)
        print(f"{k}: cells {n} blind {b} U1-fail {u1f} U2-one-min {u2}/{n} ({u2/n:.4f}) edge {e}")
        worst+= [ (k,r['sig'],r['x'],r['G'],r['nprof'],r['nfar'],r['far']) for r in v if r['nprof']!=1 or (r['nfar']>0 and not r['blind'])]
    print("failing cells (first 15):"); [print("  ",w) for w in worst[:15]]; print("total failing",len(worst))
