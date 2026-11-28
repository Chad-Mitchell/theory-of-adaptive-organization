import numpy as np
def need_counts(day_lists, Lmax, end=None):
    """day_lists: iterable of sorted unique day ints per item. Returns num, den arrays (index=lag)."""
    num=np.zeros(Lmax+1); den=np.zeros(Lmax+1)
    for d in day_lists:
        d=np.asarray(d)
        if len(d)==0: continue
        g=np.diff(d)
        if len(g):
            m=np.minimum(g,Lmax)
            # den[1..m] += 1 for each gap: use cumulative trick
            cnt=np.bincount(m,minlength=Lmax+1); den+= cnt[::-1].cumsum()[::-1]; den[0]-=0
            gg=g[g<=Lmax]; num+=np.bincount(gg,minlength=Lmax+1)
        if end is not None:
            m=min(end-d[-1],Lmax)
            if m>0: den[1:m+1]+=1
    return num,den
def fit(lag,num,den,weights=None):
    ok=(num>0)&(den>num)
    p=num[ok]/den[ok]; y=np.log(p/(1-p)); w=num[ok] if weights is None else weights[ok]
    out={}
    for name,x in (("power",np.log(lag[ok])),("exp",lag[ok].astype(float))):
        A=np.vstack([x,np.ones_like(x)]).T; W=np.sqrt(w)
        c,*_=np.linalg.lstsq(A*W[:,None],y*W,rcond=None); r=y-A@c
        sse=float(np.sum(w*r**2)); r2=1-sse/float(np.sum(w*(y-np.average(y,weights=w))**2))
        out[name]=dict(slope=float(c[0]),intercept=float(c[1]),sse=sse,r2=r2)
    out["exponent"]=-out["power"]["slope"]; out["power_wins"]=out["power"]["sse"]<out["exp"]["sse"]
    return out
def spectral_beta(series_list, fmin, fmax):
    """mean periodogram over series (each 1D counts), slope of log P vs log f in [fmin,fmax] (cycles/day)."""
    P=None;n=None
    for s in series_list:
        s=np.asarray(s,float); s=s-s.mean()
        if n is None: n=len(s)
        if len(s)!=n: continue
        ps=np.abs(np.fft.rfft(s))**2
        P=ps if P is None else P+ps
    f=np.fft.rfftfreq(n,1.0); ok=(f>=fmin)&(f<=fmax)&(P>0)
    # log-bin average
    lf=np.log10(f[ok]); lp=np.log10(P[ok]); bins=np.linspace(lf.min(),lf.max(),30)
    idx=np.digitize(lf,bins); X=[];Y=[]
    for b in np.unique(idx):
        X.append(lf[idx==b].mean()); Y.append(np.log10(np.mean(10**lp[idx==b])))
    return -float(np.polyfit(X,Y,1)[0])
