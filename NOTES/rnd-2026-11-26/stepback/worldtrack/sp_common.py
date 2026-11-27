import numpy as np
from scipy.ndimage import minimum_filter
def n_profile_minima(J,tol):
    d=np.diff(J); sg=np.sign(np.where(np.abs(d)<tol,0,d)); sg=sg[sg!=0]
    if len(sg)==0: return 1
    m=int(np.sum((sg[:-1]<0)&(sg[1:]>0)))
    if sg[0]>0: m+=1
    if sg[-1]<0: m+=1
    return m
def u1(J,ax0,ax1):
    i,k=np.unravel_index(np.argmin(J),J.shape); Jmin=J[i,k]
    lm=(J==minimum_filter(J,size=3,mode='nearest'))&(J<=Jmin*(1+1e-3))
    ii,kk=np.nonzero(lm)
    far=[(float(ax0[p]),float(ax1[q])) for p,q in zip(ii,kk) if max(ax0[p]/ax0[i],ax0[i]/ax0[p])>1.2 or max(ax1[q]/ax1[k],ax1[k]/ax1[q])>1.2]
    return i,k,Jmin,far
