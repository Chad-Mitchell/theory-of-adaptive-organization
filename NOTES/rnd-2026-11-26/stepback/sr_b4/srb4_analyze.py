# SR-b4 (D): primary R_H (log-uniform average of rho = J/J*), per-H selection (P), with robustness checks; secondaries S1, S2.
import json, math, numpy as np
TM=400
A=np.load("curves_even.npy"); ns=A[:,0].astype(int); Je=A[:,1:]           # exact even-n DP, T=1..400
odd=json.load(open("../sr_b/srb_all.json")); on=[]; Jo=[]
for k,v in odd.items():
  if int(k)%2: v=list(v)+[v[-1]]*(TM-len(v)); on.append(int(k)); Jo.append(v[:TM])
on=np.array(on); Jo=np.array(Jo)
T=np.arange(1,TM+1); disk=T*np.sin(np.pi/(2*T))**2
Jstar=np.minimum(np.minimum(Je.min(0),Jo.min(0)),disk)
Jstar_half=np.minimum(np.minimum(Je[ns<=2000].min(0),Jo.min(0)),disk)   # doubling check: n-set for J* halved
print("J* check: min over T of J*·T =",(Jstar*T).min()," (>=1 by SR-b1(a)); J*·T at T=10,100,400:",(Jstar*T)[[9,99,399]],"pi^2/4=",math.pi**2/4)
print("J* doubling check: max rel diff J*(n<=2000 set) vs J*(full set), T<=400:",np.max(Jstar_half/Jstar-1))
nstar=[ (np.concatenate([ns,on])[np.argmin(np.concatenate([Je[:,t],Jo[:,t]]))]) for t in range(TM)]
print("argmin n of J*(T) at T=2,5,10,50,100,200,400:",[nstar[t-1] for t in (2,5,10,50,100,200,400)])
allJ=np.vstack([Je,Jo]); alln=np.concatenate([ns,on])
def crit(w,H): return (allJ[:,:H]*w[:H]).sum(1), (disk[:H]*w[:H]).sum()
print("\n(P) primary R_H; margin = R_H(disk) - min_n R_H(n) (polygon cheaper if +); also R_H(disk)-1 and rel margin")
print("H  R_H(disk)  best_n  R_H(best)  margin  rel_margin  interior  dominates_pointwise_2..H  sign[J*half, w=1/(T disk), w=1/T^... raw S1, w=1]")
rows=[]
for H in (2,3,4,5,6,8,10,15,20,30,50,75,100,150,200,300,400):
  L=(1/T[:H]).sum(); res={}
  for name,J_ in (("prim",Jstar),("half",Jstar_half)):
    w=1/(T*J_); p,dk=crit(w,H); res[name]=(p/L,dk/L)
  p,dk=res["prim"]; j=int(np.argmin(p)); nb=alln[j]
  evenmask=alln%2==0; interior = nb< ns.max() and nb>ns.min()
  dom=bool(np.all(allJ[j,1:H]<disk[1:H]) ) if H>1 else None
  signs=[]
  for w in (1/(T*Jstar_half), 1/(T*disk), 1/T, np.ones(TM)):
    pp,dd=crit(w,H); signs.append("+" if pp.min()<dd else "-")
  rows.append((H,dk,nb,p[j],dk-p[j]))
  print(f"{H:3d} {dk:.10f} {nb:6d} {p[j]:.10f} {dk-p[j]:+.3e} {(dk-p[j])/dk:+.3e} {interior} {dom} {''.join(signs)}")
r=np.array(rows,dtype=float)
print("\nscaling: n*/H^2 :",np.round(r[:,2]/r[:,0]**2,3).tolist())
print("scaling: margin*H^2 :",np.round(r[:,4]*r[:,0]**2,3).tolist())
print("scaling: margin*L_H*H^2/ln H (H>=10):",[round(m*sum(1/np.arange(1,int(h)+1))*h*h/math.log(h),3) for h,_,_,_,m in rows if h>=10])
print("R_H(disk)-1 :",np.round(r[:,1]-1,5).tolist())
# (F) fixed designs: R_H(n) as H grows (trivial divergence, SR-b1(e)); show for a few n
print("\n(F) fixed-design R_H(n) for H=10,50,100,200,400 (disk last)")
for n in (6,22,102,402,1002,4002):
  i=int(np.where(alln==n)[0][0]); w=1/(T*Jstar)
  print(n,[round(float((allJ[i,:H]*w[:H]).sum()/(1/T[:H]).sum()),4) for H in (10,50,100,200,400)])
print("disk",[round(float((disk[:H]/(T[:H]*Jstar[:H])).sum()/(1/T[:H]).sum()),4) for H in (10,50,100,200,400)])
