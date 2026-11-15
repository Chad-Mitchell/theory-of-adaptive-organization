# Reviewer's own check (pick-18 review). Independent of the author's ba_rd.py/modesum.py.
import numpy as np, json, sys
np.seterr(all='ignore')
def shape(name):
    if name=='gauss':
        z=np.linspace(-7,7,281); p=np.exp(-z**2/2)
    elif name=='uniform':
        z=np.linspace(-1,1,201); p=np.ones_like(z)
    elif name=='bern02':
        z=np.array([0.,1.]); p=np.array([.8,.2])
    elif name=='three':   # new asymmetric 3-point shape, not used by author
        z=np.array([-1.,0.,3.]); p=np.array([.3,.6,.1])
    elif name.startswith('lap'):
        L=float(name[3:]); z=np.linspace(-L,L,int(10*L)+1); p=np.exp(-np.abs(z))
    p=p/p.sum(); z=z-(p*z).sum(); z=z/np.sqrt((p*z*z).sum()); return z,p
def vstar(z,p):
    t=np.concatenate([np.linspace(1e-3,5,5000),np.linspace(5,80,20000)])
    a=np.log(np.exp(np.outer(t,z)-np.max(np.outer(t,z),1,keepdims=True))@p)+np.max(np.outer(t,z),1)
    b=np.log(np.exp(np.outer(-t,z)-np.max(np.outer(-t,z),1,keepdims=True))@p)+np.max(np.outer(-t,z),1)
    return max((2*a/t**2).max(),(2*b/t**2).max())
def maxc(z,p,u,y):  # KKT test at output law delta_0
    e=-u*(z[None,:]-y[:,None])**2+u*z[None,:]**2
    return (np.exp(e)@p).max()
def ba(z,p,u,y,it=6000):
    A=np.exp(-u*(z[:,None]-y[None,:])**2); Q=np.ones(len(y))/len(y)
    for _ in range(it):
        den=A@Q; Q=Q*(A.T@(p/den)); Q/=Q.sum()
    den=A@Q; W=A*Q[None,:]/den[:,None]
    D=(p[:,None]*W*(z[:,None]-y[None,:])**2).sum()
    PY=p@W; M=(W>0)&(PY[None,:]>0); R=np.where(M,p[:,None]*W*np.log(np.where(M,W,1)/np.where(M,PY[None,:],1)),0).sum()
    c=(A.T@(p/den)); low=-(p*np.log(den)).sum()-np.log(c.max())  # weak-duality bound on L
    return R,D,R+u*D-low,u-low,u-(R+u*D)
out={}
for name in sys.argv[1:]:
    z,p=shape(name); v=vstar(z,p); us=1/(2*v)
    y=np.linspace(z.min()-1,z.max()+1,601)
    r={'vstar':v,'ustar':us}
    r['maxc_at_0.98us']=maxc(z,p,0.98*us,y); r['maxc_at_1.02us']=maxc(z,p,1.02*us,y)
    for f in (0.9,1.1,1.3):
        R,D,gap,gub,gach=ba(z,p,f*us,y,5000); r[f'BA_at_{f}us(R,D,gap,gainUB,gainAch)']=(R,D,gap,gub,gach)
    # G(u) table for exponent check
    yu=np.linspace(z.min()-0.5,z.max()+0.5,max(301,len(z)))
    U=np.geomspace(us*1.001,60,28); G=[]
    for u in U:
        R,D,gap,_,_=ba(z,p,u,yu,2000); G.append(R)
    r['G']=list(zip(U.tolist(),G)); r['max_R_over_u']=max(g/u for u,g in zip(U,G))
    out[name]=r; print(name,json.dumps({k:v for k,v in r.items() if k!='G'}),flush=True)
json.dump(out,open('/tmp/rev18/chk/rev_rd_'+'_'.join(sys.argv[1:])+'.json','w'))
