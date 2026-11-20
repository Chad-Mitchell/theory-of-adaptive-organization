"""Phase diagram in a concrete model. nice -n 19 python3 phase.py
World: two OU modes tau=1 and 100, equal variance (Var=1), sensing noise N=0.05 (units: fastest tau=1, h=1).
Designs: none (act blind: loss w*Var); central tracker with K=1 or 2 layers whose readings arrive late by latency l
(cost hK + w*E_K(l)); federate (local trackers, zero latency, extra coordination cost h_f=20h: h_f + hK + w*E_K(0));
not viable if the cheapest design costs more than income y=200h (Theorem P0: negative mean margin => certain ruin)."""
import numpy as np, sys, json
import os as _os; sys.path.insert(0,_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','layers_checks'))
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
names=['no model','one layer','two layers','federate','not viable\n(income fixed)']
cols=['#d9d9d9','#9ecae1','#3182bd','#fdae6b','#de2d26']
fig,ax=plt.subplots(figsize=(7.2,5.2),dpi=150)
X,Y=np.meshgrid(R,lat)
ax.pcolormesh(X,Y,lab,cmap=ListedColormap(cols),vmin=-0.5,vmax=4.5,shading='nearest')
# measurable dimensionless share: upkeep (holding) share of the optimal cost = d ln J*/d ln h (CT24), by region
share=np.zeros_like(lab,float)
for i in range(len(lat)):
    Jn=W*Var; J1=h+W*E1[i]; J2=2*h+W*E2[i]; Jf=np.where(hf+h+W*E1_0<=hf+2*h+W*E2_0, hf+h+W*E1_0, hf+2*h+W*E2_0)
    Kf=np.where(hf+h+W*E1_0<=hf+2*h+W*E2_0,1,2)
    up=np.vstack([0*R, h+0*R, 2*h+0*R, hf+Kf*h]); tot=np.vstack([Jn,J1,J2,Jf])
    k=np.minimum(lab[i],3); share[i]=up[k,np.arange(len(R))]/tot[k,np.arange(len(R))]
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel(r'stakes ratio  $w\,\mathrm{Var}(s)/h$'); ax.set_ylabel(r'latency  $\ell/\tau_{\rm fast}$')
for kreg in (1,2,3):
    m=np.ma.masked_where(lab!=kreg,share)
    try:
        cs=ax.contour(X,Y,m,levels=[0.1,0.3,0.5],colors='k',linewidths=0.6,linestyles=':')
        ax.clabel(cs,fmt=lambda v:f'{v:.0%}',fontsize=6)
    except Exception: pass
for k,nm in enumerate(names):
    if (lab==k).any():
        ii,jj=np.argwhere(lab==k).mean(0).astype(int)
        xx,yy=(7.5,0.03) if nm=='one layer' else (R[jj],lat[ii])
        ax.text(xx,yy,nm,ha='center',va='center',fontsize=9,weight='bold')
ax.set_title('Optimal design in one model world (illustrative, not measured)',fontsize=10)
ax.plot([],[],'k:',lw=0.8,label='dotted: upkeep share of the optimal cost (a measurable, currency-free number)'); ax.legend(loc='upper center',bbox_to_anchor=(0.5,-0.16),fontsize=6.5,frameon=False)
fig.text(0.01,0.005,r'World: OU modes $\tau$=1, 100, equal variance, noise N=0.05. Upkeep h per layer, federation overhead 20h, income fixed at 200h (the red region is an artifact of that; two time scales cap the layers at two).',fontsize=6.5)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'phase.png'))
# report boundaries
for i in [0,14,29,43]:
    row=lab[i]; ch=[(round(R[j],2),names[row[j]]) for j in range(1,len(R)) if row[j]!=row[j-1]]
    print(f"latency {lat[i]:.3f}: starts {names[row[0]]}; changes at {ch}")
json.dump({'lat':lat.tolist(),'E1':E1.tolist(),'E2':E2.tolist()},open('phase.json','w'))
