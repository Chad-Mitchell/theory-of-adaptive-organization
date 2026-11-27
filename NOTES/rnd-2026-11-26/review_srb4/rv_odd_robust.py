# Odd polygons only: does some odd n beat the disk under each weight (M3h J*, mixed J*, 1/(T disk), 1/T, 1)? n odd 3..999 + 1121, 2305, 3841.
import numpy as np
TM=400; A=np.load("rv_curves.npy"); ns=A[:,0].astype(int); J=A[:,1:]; Ja=np.load("rv_curves_antipode.npy")[:,1:]
T=np.arange(1,TM+1); dk=T*np.sin(np.pi/(2*T))**2; odd=ns%2==1
Js=np.minimum(J[ns<=1000].min(0),dk); Jm=np.minimum(np.minimum(J[odd].min(0),Ja.min(0)),dk)
for H in (100,150,200,300,400):
    row=[]
    for name,w in (("J*M3h",1/(T*Js)),("J*mixed",1/(T*Jm)),("1/(T disk)",1/(T*dk)),("1/T",1/T),("1",np.ones(TM))):
        p=(J[odd][:,:H]*w[:H]).sum(1); d=(dk[:H]*w[:H]).sum(); j=int(np.argmin(p)); row.append(f"{name}: n={ns[odd][j]} {'+' if p[j]<d else '-'}{abs(d-p[j])/d:.2e}")
    print(f"H={H}: "+" | ".join(row))
