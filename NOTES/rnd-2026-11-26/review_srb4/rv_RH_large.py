# Reviewer: R_H, per-H selection (P), robustness, and odd-only under BOTH target conventions, from rv_curves*.npy (own DP).
import math, numpy as np
TM=400; A=np.load("rv_curves.npy"); ns=A[:,0].astype(int); J=A[:,1:]
Aa=np.load("rv_curves_antipode.npy"); Ja=Aa[:,1:]
T=np.arange(1,TM+1); dk=T*np.sin(np.pi/(2*T))**2
dense=ns<=1000
Js=np.minimum(J[dense].min(0),dk)                       # M3h J*, all n<=1000
Js_half=np.minimum(J[ns<=500].min(0),dk)
print("T*J* at T=10,100,400:",np.round((T*Js)[[9,99,399]],8).tolist(),"; min_T T*J* =",(T*Js).min())
print("argmin n of J*(T) at T=2,5,10,50,100,200,400:",[int(ns[dense][np.argmin(J[dense][:,t-1])]) for t in (2,5,10,50,100,200,400)])
print("J*(n<=500) vs J*(n<=1000): max rel diff",np.max(Js_half/Js-1))
def R(Jm,w,H): L=(1/T[:H]).sum(); return (Jm[:,:H]*w[:H]).sum(1)/L, (dk[:H]*w[:H]).sum()/L
print("\n(P), M3h rule. H, R_H(disk), best n (over all computed n), R_H(best), margin, interior-of-dense?, signs[J*half, 1/(T disk), 1/T, 1]")
for H in (2,3,4,5,6,8,10,15,20,30,50,75,100,150,200,300,400):
    w=1/(T*Js); p,d=R(J,w,H); j=int(np.argmin(p)); nb=ns[j]
    sg="".join("+" if R(J,ww,H)[0].min()<R(J,ww,H)[1] else "-" for ww in (1/(T*Js_half),1/(T*dk),1/T,np.ones(TM)))
    # local check around claimed winner: is best n a local min among computed neighbours?
    print(f"{H:4d} {d:.10f} {nb:5d} {p[j]:.10f} {d-p[j]:+.3e} {'dense' if nb<=1000 else 'spot-grid'} {sg}")
for H,nc in ((200,1122),(300,2306),(400,3842)):
    w=1/(T*Js); p,d=R(J,w,H); i=np.where(ns==nc)[0][0]
    loc=[(int(ns[k]),round(float(p[k]),10)) for k in range(len(ns)) if abs(ns[k]-nc)<=6]
    print(f"claimed winner H={H} n={nc}: R_H={p[i]:.10f} (claim table) neighbours {loc}")
# Odd-only, two J* conventions
odd=ns%2==1
Js_mixed=np.minimum(np.minimum(J[odd].min(0),Ja.min(0)),dk)   # mixed (M3c) rule: odd any-d=1, even antipode
print("\nJ*: M3h vs mixed rule, T*J* at T=2,5,10,100,400:",np.round((T*Js)[[1,4,9,99,399]],4).tolist(),np.round((T*Js_mixed)[[1,4,9,99,399]],4).tolist())
print("Odd polygons only (n=3..999). Columns: H | J* M3h: disk, best odd n, margin | J* mixed rule: disk, best odd n, margin | even-antipode best margin (mixed)")
for H in (2,3,5,10,20,50,100,150,200,300,400):
    out=[]
    for Jst in (Js,Js_mixed):
        w=1/(T*Jst); p,d=R(J[odd],w,H); j=int(np.argmin(p)); out.append(f"{d:.6f} n={ns[odd][j]} {d-p[j]:+.3e}")
    w=1/(T*Js_mixed); pa,da=R(Ja,w,H); ja=int(np.argmin(pa))
    print(f"{H:4d} | {out[0]} | {out[1]} | even-antipode best n={int(Aa[ja,0])} {da-pa[ja]:+.3e}")
# R_H(disk)-1 trend
print("\nR_H(disk)-1 at H=10,100,200,400:",[round(float(R(J,1/(T*Js),H)[1]-1),5) for H in (10,100,200,400)])
