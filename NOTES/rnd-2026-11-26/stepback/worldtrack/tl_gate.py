from tl_core import *
for n,T,ref in [(6,2,0.5),(7,3,0.5942),(9,4,0.4825)]:
    m,d0=poly_move(n,T); val=m[np.abs(d0-1)<1e-9].min()
    print(f"gate n={n} T={T} J={val:.4f} ref={ref} {'OK' if abs(val-ref)<6e-5 else 'FAIL'}")
# even closed forms check
for n in [8,10,12]:
    D=dist_matrix(n); k=np.arange(n)
    cf=np.where(((k-n//2)%2)==0,np.sin(np.pi*k/n),np.sin(np.pi*k/n)/np.cos(np.pi/n))
    print("even closed form n",n,"maxdiff",np.abs(D[0]-cf).max())
# disk formula vs grid DP
for T in [2,3,4,6,10]:
    ang,m=disk_grid_dp(T,M=1440)
    sel=ang<=np.pi+1e-12
    f=disk_D(ang[sel],T)
    print("disk T",T,"min(DP-formula) =",(m[sel]-f).min(),"max",(m[sel]-f).max())
