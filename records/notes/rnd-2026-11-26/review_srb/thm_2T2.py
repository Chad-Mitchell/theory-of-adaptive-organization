# Review check (OBSERVED + exact arithmetic): the (2T+2)-gon beats the disk at every T>=2.
# Path: T unit vertex steps from v0 to v_{T}=v_{n/2-1}, n=2T+2; d(v0,v_{n/2-1})=1 (edge-parallel effect).
# Unit step d = sin(pi/n) if n/2 odd (T even), tan(pi/n) if n/2 even (T odd).  Disk optimum T sin^2(pi/2T).
import math, mpmath as mp
mp.mp.dps=40
worst=None
for T in range(2,200001):
    n=2*T+2; x=mp.pi/n
    u = mp.sin(x) if (n//2)%2==1 else mp.tan(x)
    poly=T*u**2; disk=T*mp.sin(mp.pi/(2*T))**2
    rel=(disk-poly)/disk
    if worst is None or rel<worst[1]: worst=(T,rel)
    if poly>=disk: print("FAIL",T); break
print("all T=2..200000: (2T+2)-gon strictly below disk; smallest relative margin",worst[0],mp.nstr(worst[1],6))
for T in [2,3,4,5,10,100,1000]:
    n=2*T+2; x=math.pi/n; u=math.sin(x) if (n//2)%2 else math.tan(x)
    print(T,n,round(T*u*u,6),round(T*math.sin(math.pi/(2*T))**2,6), "rel gain",round(1-T*u*u/(T*math.sin(math.pi/(2*T))**2),5),"~2/T",round(2/T,5))
# condition used in the proof for T>=3: pi^2 (T+1) < 6 T^2
print("pi^2(T+1)<6T^2 holds from T=3:", all(math.pi**2*(T+1)<6*T*T for T in range(3,10**6)), "fails at T=2:", math.pi**2*3<24)
