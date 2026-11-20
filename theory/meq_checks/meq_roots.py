import numpy as np
A=np.array([1/3,1/90]); V=np.array([40.0**2,120.0**2]); N=3600.0
# P(x) = N prod(x+a^2) + sum 2 a v prod_{i!=j}(x+a_i^2)
P=N*np.poly1d([1,A[0]**2])*np.poly1d([1,A[1]**2]) + 2*A[0]*V[0]*np.poly1d([1,A[1]**2]) + 2*A[1]*V[1]*np.poly1d([1,A[0]**2])
b=np.sqrt(-P.r)
print("world mode time constants (days):",1/A)
print("Wiener-filter pole time constants 1/b_j (days):",np.sort(1/b))
for Nn in [36.0,360.0,3600.0,36000.0]:
    P=Nn*np.poly1d([1,A[0]**2])*np.poly1d([1,A[1]**2]) + 2*A[0]*V[0]*np.poly1d([1,A[1]**2]) + 2*A[1]*V[1]*np.poly1d([1,A[0]**2])
    print(f" N={Nn}: layer time constants {np.sort(1/np.sqrt(-P.r))}")
