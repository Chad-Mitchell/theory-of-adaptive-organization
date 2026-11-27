import math, numpy as np, sh_heat_core as C, sh_read_run as S
mm=0; cnt=0; ex=[]
SUB=[0.4,0.1,0.025,0.0035]  # sigma subset (disclosed in §11: full grid too slow)
for s in SUB:
    for n in range(3,32):
        R=C.Rec(n,s)
        if R.p==0: continue
        for x in S.XS:
            for y in S.YS:
                b,jb,dec=S.best_check(R,x,y); cnt+=1
                t=np.arange(1,S.SMAX+1)
                # full scan via HE on all t is slow; scan exactly with vectorised first-order where valid, else HE
                if not hasattr(R,'HH'): R.HH=np.array([R.HE(int(u))[0] for u in t]); R.EE=np.array([R.HE(int(u))[1] for u in t])
                J=(y/R.p+R.HH+x*R.EE)/t
                bf=int(np.argmin(J))+1
                if bf!=b and abs(J[bf-1]*R.p-jb)>1e-10*abs(jb): mm+=1; ex.append((n,s,x,y,b,bf))
print('(a) full scan s<=20000, n<=31: cases %d mismatches %d'%(cnt,mm), ex[:10],flush=True)
# (c) y=0 regression against sh_heat
bad=0
for s in C.SIG:
    for n in range(3,62):
        R=C.Rec(n,s)
        if R.p==0: continue
        for x in S.XS:
            b0,_=R.best_check(x)
            # y=0 with smax 4000
            b1,_,_=S.best_check(R,x,0.0,smax=4000)
            if b0!=b1: bad+=1
print('(c) y=0 regression vs §9 (n<=61): mismatches',bad,flush=True)
