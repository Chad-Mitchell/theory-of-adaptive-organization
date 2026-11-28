# Reviewer's ODD analogue of Proposition SR-b4 (new here; PIM-candidate, needs its own hostile review).
# Claim: n odd >= 5, S'=(n-1)/2, T>=2 dividing S'  =>  J(n,T) < T sin^2(pi/2T). Target v_{S'} (d=1; same under M3c and M3h).
# Bound used: d(v0,vj) <= |v0-vj|/w_min = sin(pi j/n)/cos^2(pi/2n)   (w_min = 1+cos(pi/n), vertex to opposite edge).
# (a) exact check of every proof step with breakpoint distances (60 digits) for the (2T+1)-gon, T=2..300, and odd lcm family H=2..9;
# (b) reviewer DP (rv_dp) on n = 1+2m*lcm(1..H), H=2..9; (c) bound-only chain for n = 1+2*lcm(1..H), H up to 60.
import math, subprocess, mpmath as mp
mp.mp.dps=60
def dist(n,k):
    vx=lambda i: mp.cos(2*mp.pi*i/n); vy=lambda i: mp.sin(2*mp.pi*i/n)
    best=mp.mpf(0)
    for j in range(2*n):
        a=2*mp.pi*(j%n+mp.mpf(1)/2)/n; tx,ty=mp.cos(a),mp.sin(a)
        if j>=n: tx,ty=-tx,-ty
        # width of regular odd n-gon in a direction offset alpha from nearest vertex: cos(alpha)+cos(pi/n-alpha); at an edge normal alpha=pi/n
        w=1+mp.cos(mp.pi/n)
        r=((1-vx(k))*tx+(0-vy(k))*ty)/w
        if r>best: best=r
    return best
def chain(n,T,exact=True):
    Sp=(n-1)//2; j=Sp//T; assert j*T==Sp
    x=mp.pi/(2*T); y=x*(1-mp.mpf(1)/n); dk=T*mp.sin(x)**2
    bound=mp.sin(y)/mp.cos(mp.pi/(2*n))**2
    c2= mp.sin(y)<=mp.sin(x)-(x/n)*mp.cos(x)
    c3= mp.sin(mp.pi/(2*n))**2<=mp.pi**2/(4*n**2)
    c4= x*mp.cot(x)>=mp.pi/4
    c5= mp.pi**2/(4*n**2)<mp.pi/(4*n)
    ok=c2 and c3 and c4 and c5 and T*bound**2<dk
    if exact:
        d=dist(n,j); dt=dist(n,Sp)
        ok = ok and d<=bound*(1+mp.mpf(10)**-50) and abs(dt-1)<mp.mpf(10)**-40
    return ok, (dk-T*bound**2)/dk
print("(a) (2T+1)-gon, exact distances:", all(chain(2*T+1,T)[0] for T in range(2,301)), " min n*rel-margin of the bound:",
      mp.nstr(min((2*T+1)*chain(2*T+1,T,False)[1] for T in range(2,301)),6))
for H in range(2,10):
    n=1+2*math.lcm(*range(1,H+1))
    print(f"(a) odd lcm H={H} n={n}: every proof step holds at every T in 2..H (exact distances):",all(chain(n,T,exact=(n<1000))[0] for T in range(2,H+1)), "(exact distance check only for n<1000)")
def disk(T): return T*math.sin(math.pi/(2*T))**2
for H in range(2,10):
  for m in ((1,2) if H<9 else (1,)):
    n=1+2*m*math.lcm(*range(1,H+1))
    J=list(map(float,subprocess.run(["./rv_dp",str(n),str(H)],capture_output=True,text=True).stdout.split()[1:]))
    mg=[(disk(T)-J[T-1])/disk(T) for T in range(2,H+1)]
    print(f"(b) DP H={H} m={m} n={n}: J(1)={J[0]:.15f}; cheaper than disk at all T in 2..H: {all(x>0 for x in mg)}; min rel margin {min(mg):.4e}")
bad=0
for H in range(2,61):
    n=1+2*math.lcm(*range(1,H+1))
    bad+=sum(not chain(n,T,False)[0] for T in range(2,H+1))
print("(c) bound-only chain, n=1+2 lcm(1..H), H=2..60, failures:",bad)
