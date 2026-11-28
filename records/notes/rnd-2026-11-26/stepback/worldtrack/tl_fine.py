from tl_run_funcs import *
import json
Ts=[2,3,4,5,6,8,10,12,16,20]; lams=[2,5,10,30,100,1000]
al=np.linspace(0,1,1001); bad=[]
for T in Ts:
    P=build(T)
    for lam in lams:
        D=[]
        for a in al:
            cd,_=disk_C(a,lam,T)
            D.append(cd-min((mv+lam*(a*lp+(1-a)*lr)).min() for mv,lp,lr,phi in P.values()))
        W=np.array(D)>1e-12; ch=int((W[1:]!=W[:-1]).sum())
        if not(W[0] and ch==1): bad.append((T,lam,ch))
print("fine grid (step 0.001) cells not single-crossing:",bad)
