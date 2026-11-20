"""Phase diagram in a concrete model. nice -n 19 python3 phase.py
World: two OU modes tau=1 and 100, equal variance (Var=1), sensing noise N=0.05 (units: fastest tau=1, h=1).
Designs: none (act blind: loss w*Var); central tracker with K=1 or 2 layers whose readings arrive late by latency l
(cost hK + w*E_K(l)); federate (local trackers, zero latency, extra coordination cost h_f=20h: h_f + hK + w*E_K(0));
not viable if the cheapest design costs more than income y=200h (Theorem P0: negative mean margin => certain ruin)."""
import numpy as np, sys, json
sys.path.insert(0,'/workspace/gtao-spine/checks')
from lead import E_opt, E_K_lead
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
a=np.array([1.0,1/100]); v=np.array([0.5,0.5]); N=0.05; Var=v.sum(); h=1.0; hf=20.0; y=200.0
lat=np.logspace(-2,np.log10(30),44)
E1=np.array([E_K_lead(a,v,N,1,l,starts=6) for l in lat]); E2=np.array([E_opt(a,v,N,l) for l in lat])
E1_0=E_K_lead(a,v,N,1,0.0,starts=6); E2_0=E_opt(a,v,N,0.0)
print("E1(l):",np.round(E1,4)); print("E2(l):",np.round(E2,4)); print("E(0):",E1_0,E2_0)
R=np.logspace(-1,3.6,500)   # R = w*Var/h
W=R*h/Var
lab=np.zeros((len(lat),len(R)),int)
for i in range(len(lat)):
    C=np.vstack([W*Var, h+W*E1[i], 2*h+W*E2[i], np.minimum(hf+h+W*E1_0, hf+2*h+W*E2_0)])
    best=C.min(0); k=C.argmin(0); k[best>y]=4; lab[i]=k
names=['no model','one layer','two layers','federate','not viable']
cols=['#d9d9d9','#9ecae1','#3182bd','#fdae6b','#de2d26']
fig,ax=plt.subplots(figsize=(7.2,4.8),dpi=150)
X,Y=np.meshgrid(R,lat)
ax.pcolormesh(X,Y,lab,cmap=ListedColormap(cols),vmin=-0.5,vmax=4.5,shading='nearest')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel(r'stakes ratio  $w\,\mathrm{Var}(s)/h$'); ax.set_ylabel(r'latency  $\ell/\tau_{\rm fast}$')
for k,nm in enumerate(names):
    if (lab==k).any():
        ii,jj=np.argwhere(lab==k).mean(0).astype(int)
        ax.text(R[jj],lat[ii],nm,ha='center',va='center',fontsize=9,weight='bold')
ax.set_title('Optimal design in one model world (illustrative, not measured)',fontsize=10)
fig.text(0.01,0.01,r'World: OU modes $\tau$=1, 100, equal variance, noise N=0.05. Upkeep h per layer, federation overhead 20h, income 200h.',fontsize=6.5)
fig.tight_layout(rect=(0,0.03,1,1)); fig.savefig('/workspace/gtao-meq/phase.png')
# report boundaries
for i in [0,14,29,43]:
    row=lab[i]; ch=[(round(R[j],2),names[row[j]]) for j in range(1,len(R)) if row[j]!=row[j-1]]
    print(f"latency {lat[i]:.3f}: starts {names[row[0]]}; changes at {ch}")
json.dump({'lat':lat.tolist(),'E1':E1.tolist(),'E2':E2.tolist()},open('phase.json','w'))
