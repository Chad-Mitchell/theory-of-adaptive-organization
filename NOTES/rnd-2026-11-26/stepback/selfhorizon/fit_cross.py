import json, math, numpy as np
R=json.load(open("sh_noise.json"))
def cr(r):
    c=r['cross']; c=eval(c) if isinstance(c,str) else c; return c
for arm in ['primary','ceil','R1']:
  for cfg in ['E-M3h','O','F-M3h','F-mixed']:
    rows=[(r['sigma'],cr(r)) for r in R[arm+'|'+cfg] if cr(r) and cr(r)[1] is not None]
    s=np.array([x[0] for x in rows]); nc=np.array([(x[1][0]+x[1][2])/2 for x in rows])
    slope=[abs((x[1][3]-x[1][1])/(x[1][2]-x[1][0])) for x in rows]
    b=-np.polyfit(np.log(s),np.log(nc),1)[0]
    small=s<=0.05; b2=-np.polyfit(np.log(s[small]),np.log(nc[small]),1)[0] if small.sum()>2 else float('nan')
    C=nc*s*np.sqrt(2*np.log(1/s)); C2=nc*s**2
    print("%-8s %-8s n_c=%s\n   beta(all)=%.3f beta(sigma<=0.05)=%.3f  n_c*s*sqrt(2ln1/s): %.2f..%.2f  n_c*s^2: %.3g..%.3g  |dPhi/dn| median %.1f range %.1f-%.1f"%(arm,cfg,list(zip(s.tolist(),nc.tolist())),b,b2,C.min(),C.max(),C2.min(),C2.max(),np.median(slope),min(slope),max(slope)))
