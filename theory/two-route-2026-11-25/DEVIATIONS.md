# Deviations from the locked prereg

*Appended lines only. Lock: `theory/two-route-2026-11-25/PREREG.md`, sha256 `9e42fe0a581a271f5c09a6dd7064304f8aaab43dd21ed7d509feaad13cd29e54`, lock commit `b159d0f`. Format: date and time (America/New_York), what changed from the prereg, why, and whether any scored number had been seen.*

- 2026-11-25 (ET): none so far.
- 2026-11-25 09:05 ET: A-T2 optimizer tolerance was 1e-10 (tighter than the locked 1e-6), and the resolution check compared 1e-5 against 1e-10 instead of halving the tolerance; rho moved by 2e-6, far inside the locked 0.01. The scored number had not been seen when the script was written; it was seen only in the one run logged in `checks/route_a_w2.out`.
- 2026-11-25 09:05 ET: the Lyapunov cross-check simulation (Euler, step 1e-3, 4e5 steps, one seed) agrees to 3.6% of the largest covariance entry, inside its own sampling error at that length (about 7% for a correlation time near 1 over 360 time units). Not a scored number.
