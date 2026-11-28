# §10.4 key question, §10.5 triviality, Claim W row 12; reads sh_read_cells.json and sh_read_modes.pkl.
import json, math, pickle, numpy as np
import sh_heat_core as C
Cc=json.load(open('sh_read_cells.json')); M=pickle.load(open('sh_read_modes.pkl','rb'))
XS=C.XS; YS=[0.1,1.0,10.0]; SIG=C.SIG; SC=['E-M3h','O','F-M3h','F-mixed']
def g(r,rn,cfg,x,y,s): return Cc['%s|%s|%s|%g|%g|%g'%(r,rn,cfg,x,y,s)]
# (b) edge check
tot=0; dec=0; p0=0
for k,o in M.items():
    for kk,m in o.items():
        if isinstance(m,dict) and m['s_star']>=20000:
            c={'keep':m['keep'],'check':m['check'],'fade':m['fade']}
            if min(c,key=c.get)=='check':
                tot+=1; dec+=m['dec_at_edge']; p0+=m['p0']
print('(b) check-mode designs with s*=20000: %d; J decreasing at edge: %d; p underflow (decreasing by first-order form): %d'%(tot,dec,p0))
for reading in ['W','I']:
    print('==== reading',reading)
    for cfg in ['F-M3h','O']:
        # elasticities over the grid where nc exists
        rows=[]
        for x in XS:
            for y in YS:
                for s in SIG:
                    c=g(reading,'floor',cfg,x,y,s)
                    if c['nc'] is not None and c['nc']>4: rows.append((math.log(s),math.log(x),math.log(y),math.log(c['nc']),c['s_c']))
        if len(rows)<5: print(' ',cfg,'too few crossings',len(rows)); continue
        R=np.array([r[:4] for r in rows]); X=np.c_[np.ones(len(R)),R[:,0],R[:,1],R[:,2]]
        coef,*_=np.linalg.lstsq(X,R[:,3],rcond=None)
        sl=np.array([abs(r[4]) for r in rows if r[4] is not None])
        print('  %s: crossings %d; beta=%.3f e_x=%.3f e_y=%.3f ; median |s_c|=%.2f (IQR %.2f-%.2f); frac |s_c|>1: %.2f'%(cfg,len(rows),-coef[1],coef[2],coef[3],np.median(sl),np.percentile(sl,25),np.percentile(sl,75),(sl>1).mean()))
        # per (x,y) beta and constancy of nc*sigma*sqrt(2ln1/s)
        for y in YS:
            line=[]
            for x in XS:
                pts=[(s,g(reading,'floor',cfg,x,y,s)['nc']) for s in SIG if g(reading,'floor',cfg,x,y,s)['nc'] is not None and g(reading,'floor',cfg,x,y,s)['nc']>4]
                if len(pts)>=3:
                    ss=np.array([p[0] for p in pts]); nn=np.array([p[1] for p in pts])
                    b=-np.polyfit(np.log(ss),np.log(nn),1)[0]; inv=nn*ss*np.sqrt(2*np.log(1/ss))
                    line.append('x=%g:b=%.2f,inv=%.1f-%.1f(n=%d)'%(x,b,inv.min(),inv.max(),len(pts)))
                else: line.append('x=%g:-'%x)
            print('    y=%g '%y+' | '.join(line))
    # HIT cells and triviality
    H=[(k,v) for k,v in Cc.items() if k.startswith(reading+'|floor|') and v['status']=='HIT' and k.split('|')[2] in SC]
    gen=[]
    for k,v in H:
        _,_,cfg,x,y,s=k.split('|'); x=float(x); s=float(s); n=v['sc'][0]
        nref=4/(s*math.sqrt(2*math.log(1/s))); nst=4/x+2
        if not (nref/1.5<=n<=1.5*nref) and not (nst/1.5<=n<=1.5*nst): gen.append((k,n,round(nref,1),nst))
    print('  HIT cells (floor, scored):',len(H),'; genuine by §10.5:',len(gen),gen[:12])
    # equal x/y comparison (row 12)
    print('  row 12, equal x/y = 0.1: (x,y)=(0.01,0.1),(0.1,1),(1,10); n_c and n* per sigma, F-M3h:')
    for s in SIG:
        print('    s=%g'%s,[(g(reading,'floor','F-M3h',x,y,s)['nc'],g(reading,'floor','F-M3h',x,y,s)['sc'][:1] if g(reading,'floor','F-M3h',x,y,s)['nsc']==1 else g(reading,'floor','F-M3h',x,y,s)['nsc']) for x,y in [(0.01,0.1),(0.1,1.0),(1.0,10.0)]])
