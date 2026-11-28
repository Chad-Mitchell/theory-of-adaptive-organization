# Checks (a)-(d) of SELF_HORIZON §8.9, plus kernel normalisation.
import math, numpy as np, warnings, sh_heat_core as C
warnings.simplefilter('error')
print("kernel normalisation and a-range:")
worst=0; amax=0
for s in C.SIG:
    for n in list(range(3,62))+[100,101,400,401,802,1201]:
        q=C.kernel(n,s); worst=max(worst,abs(q.sum()-1)); R=C.Rec(n,s); amax=max(amax,R.a.max())
print("  max |sum q - 1| = %.2e ; max (1-lambda) = %.4f"%(worst,amax))
# (b) FFT H and closed-form E vs direct matrix power
print("(b),(c) FFT entropy and closed-form E vs direct matrix powers, n<=15:")
eb=0; ec=0
for s in C.SIG[:8]:
    for n in range(3,16):
        R=C.Rec(n,s); q=C.kernel(n,s)
        P=np.array([[q[(j-i)%n] for j in range(n)] for i in range(n)])
        M=np.eye(n); E=0.0
        for t in range(1,61):
            E+=1-M[0,0]; M=M@P
            if R.p>0 and t*R.p>=1e-6:
                row=np.clip(M[0],0,None); H=-(row[row>0]*np.log(row[row>0])).sum()
                h,e,_=R.HE(t); eb=max(eb,abs(h*R.p-H)/max(H,1e-300)); ec=max(ec,abs(e*R.p-E)/max(E,1e-300))
print("  max rel err H = %.2e ; E = %.2e"%(eb,ec))
# (d) first-order vs exact at the boundary
print("(d) first-order vs exact near t*p = 1e-6:")
dd=0
for s,n in [(0.1,7),(0.05,9),(0.02,21),(0.012,41),(0.0035,101)]:
    R=C.Rec(n,s)
    if R.p<=0: continue
    t=max(1,int(1e-6/R.p)); 
    for tt in [t, t+1, 2*t+1]:
        R.cache={}; fo=(tt*(1-math.log(tt)-R.logp+R.hq), tt*(tt-1)/2)
        sv=R.p; R.cache={}
        # force exact
        a=R.a[1:]; m=tt-1
        lam_t=C.lampow(R.a,tt); row=np.clip(np.fft.fft(lam_t).real/n,0,None); row/=row.sum(); H=-(row[row>0]*np.log(row[row>0])).sum()/R.p
        print("   n=%d s=%g t=%d p=%.2e  H/p fo=%.6g exact=%.6g"%(n,s,tt,R.p,fo[0],H))
# (a) full integer scan vs grid search
print("(a) full scan s<=4000 vs grid search, n<=61, all sigma, all x:")
mism=[]; cnt=0
for s in C.SIG:
    for n in range(3,62):
        R=C.Rec(n,s)
        for x in C.XS:
            b,jb=R.best_check(x); cnt+=1
            J=[(R.HE(t)[0]+x*R.HE(t)[1])/t for t in range(1,C.SMAX+1)]
            bf=int(np.argmin(J))+1
            if bf!=b and abs(J[bf-1]-jb)>1e-12*abs(jb): mism.append((n,s,x,b,bf,jb,J[bf-1]))
print("  cases %d, mismatches %d"%(cnt,len(mism)))
for m in mism[:15]: print("   ",m)
