"""Hypothesized placements on the map: every system is a chain of components (time scales of its world), fast to slow.
Every input is a RANGE (low, high), drawn log-uniformly (rho uniformly); sources are in face_placements.md.  Nothing here is measured
except where face_placements.md cites a source for a time scale or a delay; every stakes-over-upkeep number is a guess.

Per component (one Ornstein-Uhlenbeck time scale; times in hours):
  tau   time scale of that part of the world             lead  delay before pooled reads reach a shared layer
  n     units that could share one layer                 rho   share of the component common to all units (0..1)
  snr   what one unit's reads over one time scale tell it: Lambda = 2v/(N a)  (large = clean reads)
  R     stakes over upkeep for ONE unit's layer if its reads were perfect: w_u*v/h_l  (guess in every row)
  hc    upkeep of one shared layer over one unit's layer: h_c/h_l (guess)
Coordinates (face_map.py): X_L = R*(1 - P/v), X_S = (n/hc)*R*G_S/v.  n = 1: no shared option (drawn in the bottom band).
stream='one': the components reach the system through ONE read stream (E. coli's receptors), so they are not separate channels; the
coordinates are then the MARGINAL worths of the 1st and 2nd layer, R*(E_0 - E_1) and R*(E_1 - E_2) (THEORY L2; V3 of
face_collapse_v23.py shows the layer-by-layer reading is exact there), with N set by the fast component's snr and R the run row's."""
H, D, W, MO, Y = 1.0, 24.0, 24.0 * 7, 24.0 * 30.4, 24.0 * 365.25
SEC, MIN = 1 / 3600, 1 / 60

SYSTEMS = [
 dict(name='E. coli', strong=True, stream='one', comps=[
   dict(lab='run', tau=(0.5 * SEC, 3 * SEC), lead=(0.1 * SEC, 0.3 * SEC), n=(1, 1), rho=(1, 1), snr=(1, 10), R=(3, 100), hc=(1, 1)),
   dict(lab='background', tau=(30 * SEC, 300 * SEC), lead=(0.1 * SEC, 0.3 * SEC), n=(1, 1), rho=(1, 1), snr=(30, 1000), R=(3, 100), hc=(1, 1))]),
 dict(name='immune system', strong=True, comps=[
   dict(lab='innate', tau=(1 * H, 10 * H), lead=(12 * H, 48 * H), n=(100, 1000), rho=(0.1, 0.5), snr=(1, 30), R=(30, 3000), hc=(3, 100)),
   dict(lab='adaptive', tau=(5 * D, 30 * D), lead=(12 * H, 48 * H), n=(100, 1000), rho=(0.5, 1.0), snr=(0.3, 10), R=(3, 300), hc=(3, 100)),
   dict(lab='memory', tau=(10 * Y, 100 * Y), lead=(1 * D, 7 * D), n=(100, 1000), rho=(0.7, 1.0), snr=(10, 1000), R=(0.3, 30), hc=(3, 100))]),
 dict(name='ant colony', strong=True, comps=[
   dict(lab='patch', tau=(20 * MIN, 3 * H), lead=(15 * MIN, 45 * MIN), n=(100, 1000), rho=(0.0, 0.3), snr=(0.3, 10), R=(3, 300), hc=(1, 30)),
   dict(lab='food supply', tau=(6 * H, 7 * D), lead=(15 * MIN, 45 * MIN), n=(100, 1000), rho=(0.7, 1.0), snr=(0.03, 1), R=(0.3, 30), hc=(1, 30))]),
 dict(name='small team', strong=True, comps=[
   dict(lab='tasks', tau=(1 * D, 5 * D), lead=(2 * H, 12 * H), n=(5, 10), rho=(0.3, 0.8), snr=(1, 30), R=(1, 30), hc=(0.5, 3)),
   dict(lab='goals', tau=(1 * MO, 6 * MO), lead=(1 * D, 7 * D), n=(5, 10), rho=(0.8, 1.0), snr=(3, 100), R=(1, 30), hc=(0.5, 3))]),
 dict(name='firm', strong=True, comps=[
   dict(lab='operations', tau=(1 * D, 7 * D), lead=(1 * W, 5 * W), n=(10, 300), rho=(0.1, 0.5), snr=(1, 30), R=(30, 3000), hc=(3, 30)),
   dict(lab='management', tau=(1 * MO, 6 * MO), lead=(2 * W, 8 * W), n=(10, 300), rho=(0.5, 0.9), snr=(1, 30), R=(3, 300), hc=(3, 30)),
   dict(lab='strategy', tau=(2 * Y, 10 * Y), lead=(1 * MO, 3 * MO), n=(10, 300), rho=(0.7, 1.0), snr=(1, 30), R=(1, 100), hc=(3, 30))]),
 dict(name='city', strong=False, comps=[
   dict(lab='services', tau=(6 * H, 3 * D), lead=(3 * D, 30 * D), n=(10, 100), rho=(0.0, 0.3), snr=(1, 30), R=(10, 1000), hc=(3, 30)),
   dict(lab='budget', tau=(1 * Y, 4 * Y), lead=(1 * MO, 6 * MO), n=(10, 100), rho=(0.5, 0.9), snr=(1, 30), R=(1, 100), hc=(3, 30)),
   dict(lab='land use', tau=(10 * Y, 50 * Y), lead=(6 * MO, 2 * Y), n=(10, 100), rho=(0.5, 1.0), snr=(3, 100), R=(1, 100), hc=(3, 30))]),
 dict(name='nation-state', strong=False, comps=[
   dict(lab='local', tau=(1 * D, 30 * D), lead=(1 * MO, 3 * MO), n=(10, 100), rho=(0.0, 0.3), snr=(1, 30), R=(10, 1000), hc=(3, 100)),
   dict(lab='business cycle', tau=(2 * Y, 8 * Y), lead=(1 * MO, 3 * MO), n=(10, 100), rho=(0.5, 0.9), snr=(1, 30), R=(1, 300), hc=(3, 100)),
   dict(lab='institutions', tau=(20 * Y, 100 * Y), lead=(3 * MO, 2 * Y), n=(10, 100), rho=(0.7, 1.0), snr=(3, 100), R=(1, 100), hc=(3, 100))]),
 dict(name='global economy', strong=False, comps=[
   dict(lab='markets', tau=(1 * H, 7 * D), lead=(1 * MO, 6 * MO), n=(50, 200), rho=(0.0, 0.5), snr=(1, 30), R=(10, 1000), hc=(10, 1000)),
   dict(lab='world cycle', tau=(3 * Y, 10 * Y), lead=(1 * MO, 6 * MO), n=(50, 200), rho=(0.3, 0.8), snr=(1, 30), R=(1, 100), hc=(10, 1000)),
   dict(lab='climate', tau=(30 * Y, 300 * Y), lead=(1 * Y, 5 * Y), n=(50, 200), rho=(0.8, 1.0), snr=(1, 100), R=(0.3, 30), hc=(10, 1000))]),
]
