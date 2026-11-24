"""Validate reviewer bin-arithmetic tail against the memo's Fourier tail at delta=0."""
import numpy as np, duel_core as d
def Lnoise_fn(N, v, k):
    mass = d.convolve_noise(d.uniform_mix_density([0.0],[1.0],2*np.pi/N), v, k)
    return np.real(np.fft.ifft(np.conj(np.fft.fft(mass))*np.fft.fft(d.TAILMASK.astype(float))))
worst=0
for N,f,t,s,k in [(8,1.0,0.3,0,None),(32,0.7,0.9,0.01,None),(12,1.4,0.1,0.001,100.0),(64,1.0,0.2,0.0,None),(5,0.0,0.2,0.01,100.0)]:
    rstar=2*np.pi/np.sin(2*np.pi/N); r=f*rstar
    L=Lnoise_fn(N,s*t,k); q=d.a_jump_dist(N,r,t) if r>0 else np.eye(N)[0]
    cen=2*np.pi*t-2*np.pi*np.arange(N)/N; j=np.round((cen%(2*np.pi))/(2*np.pi)*d.M).astype(int)%d.M
    mine=(q*L[j]).sum(); theirs=d.a_tail_fourier(N,r,t,s*t,k); worst=max(worst,abs(mine-theirs))
    print(f"N={N} r/r*={f} t={t} s={s} k={k}: reviewer {mine:.6f} memo-Fourier {theirs:.6f}")
print("max abs diff", worst)
