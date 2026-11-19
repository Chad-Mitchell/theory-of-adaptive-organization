import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import norm
rng=np.random.default_rng(7)
# --- N47 (a): event-driven sim of per-target staleness with failure, compare mean age
def age_sim(s,T=1.0,n=200000):
    # deliveries at t=jT of reading taken at jT; success prob s
    succ=rng.random(n)<s
    t_last=-np.inf; tot=0.0; cnt=0
    idx=np.flatnonzero(succ)
    # time-average of age over [idx0, end): piecewise between successes: from success at a to next success at b, age goes 0..(b-a)T
    gaps=np.diff(idx)*T
    return (gaps**2/2).sum()/gaps.sum()
for s in (1,0.9,0.5,0.25):
    print("age s=%.2f sim %.4f formula %.4f"%(s,age_sim(s),(2-s)/(2*s)))
# brute-force threshold: cost(T)=(c+N*d_eff)/T + N*q*E[age](T)
def central(N,dc,s,retry,q=1.0,c=1.0):
    if retry: f=lambda T:(c+N*dc*c/s)/T+N*q*T/2
    else: f=lambda T:(c+N*dc*c)/T+N*q*T*(2-s)/(2*s)
    return minimize_scalar(f,bounds=(1e-6,1e5),method='bounded').fun
def local(N,q=1.0,c=1.0): return N*np.sqrt(2*c*q)
bad=0;tot=0
for N in (3,10,50,200):
  for s in (1,0.97,0.8,0.6,0.3):
    for retry in (0,1):
      thr= s*(1-1/N) if retry else s/(2-s)-1/N
      # bisection on win boundary
      g=lambda dc: central(N,dc,s,retry)-local(N)
      if thr>0:
        b=brentq(g,0,5) if g(0)<0 else -1
      else: b=None
      tot+=1
      if thr>0 and abs(b-thr)>1e-4: bad+=1; print("mismatch",N,s,retry,b,thr)
      if thr<=0 and g(0)<0: bad+=1; print("mismatch-neg",N,s,retry)
print("N47a boundary root vs closed form: %d bad of %d"%(bad,tot))
# (b) outages: continuous-time sim. reading every T; up/down alternating; delivered when up (newest at reopen)
def outage_sim(T=1.0,upm=10.0,dist='exp',theta=2.0,cv2=1.0,horizon=2e5):
    t=0.0; ages=0.0; up=True
    # construct timeline of down intervals
    downs=[];tt=0.0
    while tt<horizon:
        tt+=rng.exponential(upm)
        if dist=='exp': x=rng.exponential(theta)
        elif dist=='const': x=theta
        elif dist=='gamma': k=1/cv2; x=rng.gamma(k,theta/k)
        elif dist=='ln':
            s2=np.log(1+cv2); x=rng.lognormal(np.log(theta)-s2/2,np.sqrt(s2))
        downs.append((tt,tt+x)); tt+=x
    downs=np.array(downs)
    # numerically: sample random times, compute age
    ts=rng.random(400000)*downs[-2,1]
    # find whether in down interval
    i=np.searchsorted(downs[:,0],ts)-1
    indown=(i>=0)&(ts<downs[np.maximum(i,0),1])
    # if down: last delivered reading is latest reading time <= down start (delivered immediately at reading time when up)
    last_read=np.floor(ts/T)*T
    lastdel=np.where(indown, np.floor(downs[np.maximum(i,0),0]/T)*T, last_read)
    # but if up and the last reading was during preceding down interval, it was delivered at reopening (newest) -> lastdel=last_read ok
    age=ts-lastdel
    A=upm/(upm+theta)
    return age.mean(), T/2+(1-A)*theta*(1+cv2)/2
for d,cv in (('exp',1),('const',0),('gamma',0.25),('ln',3.2)):
    print("outage %s sim %.4f formula(nominal) %.4f"%((d,)+outage_sim(dist=d,cv2=cv)))
# (d) invariance and q^-1/2, reach exponent
for q in (0.25,1,16):
    N,dc=16,0.5
    lc=np.sqrt(2/q)*(1-np.sqrt((1+N*dc)/N))
    # brute: largest l such that central+N q l < local
    lb=(local(N,q)-central(N,dc,1,0,q))/(N*q)
    print("q=%5.2f l_crit closed %.5f brute %.5f  l*sqrt(q)=%.4f"%(q,lc,lb,lc*np.sqrt(q)))
for a in (2,3):
  for b in (0.5,1,1.5,2):
    m=np.array([1,10.]); L=m*(1/(m**b))**(1/(a-1))
    print("alpha=%d beta=%.1f  reach exponent numeric %.3f formula %.3f"%(a,b,np.log(L[1]/L[0])/np.log(10),1-b/(a-1)))
# ---- N49 circle-map with general PRC (asymmetric) and invertibility
def rot(Om,eps,Z,n=3000):
    th=0.0
    for _ in range(n): th=th+Om+eps*Z(th)
    return th/n
Zs=lambda th: -0.5*np.sin(2*np.pi*th)
Za=lambda th: 0.3*np.sin(2*np.pi*th)**2-0.2*np.cos(2*np.pi*th)  # asymmetric PRC
for name,Z in (("sine",Zs),("asym",Za)):
    th=np.linspace(0,1,20001); zmin,zmax=Z(th).min(),Z(th).max()
    for eps in (0.1,):
        Oms=np.linspace(-0.2,0.2,4001); locked=np.array([abs(rot(o,eps,Z,800))<2e-3 for o in Oms])
        lo,hi=Oms[locked].min(),Oms[locked].max()
        print("PRC %s eps=%.2f locked Omega in [%.4f,%.4f] width %.4f ; predicted [%.4f,%.4f] width %.4f; centre %.4f"%(name,eps,lo,hi,hi-lo,-eps*zmax,-eps*zmin,eps*(zmax-zmin),-eps*(zmax+zmin)/2))
# N49 optimum: U(a)=V P(|Om|<a)-c a, Om~N(mu,sig)
def astar(mu,c,V=1,sig=1):
    a=np.linspace(0,8,80001); U=V*(norm.cdf((a-mu)/sig)-norm.cdf((-a-mu)/sig))-c*a
    return a[np.argmax(U)]
for mu in (0,0.5,0.9,1.0,1.1,1.5):
    cs=np.linspace(0.02,1.2,1200); A=np.array([astar(mu,c) for c in cs])
    print("mu=%.1f max jump %.3f"%(mu,np.abs(np.diff(A)).max()))
c0=2/np.sqrt(2*np.pi)
for c in (0.05*c0,0.5*c0,0.95*c0):
    print("mu=0 c/c0=%.2f numeric %.4f closed %.4f"%(c/c0,astar(0,c),np.sqrt(2*np.log(c0/c))))
# cusp exponent at mu=sigma: c0(mu)=2 phi(mu) V/sig
c0s=2*norm.pdf(1.0)
for dlt in (1e-3,1e-4,1e-5):
    a=brentq(lambda a: norm.pdf(a-1)+norm.pdf(a+1)-(c0s-dlt),1e-6,1.0)
    print("mu=sigma: c0-c=%.0e a*=%.5f a*/(dc)^0.25=%.4f"%(dlt,a,a/dlt**0.25))
