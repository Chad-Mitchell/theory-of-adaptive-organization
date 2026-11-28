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
degree: a component's McMillan degree (default 1); it is held by that many stores (a rhythm or an integrated signal counts 2).
measured=True (E. coli only): X_L is taken from the measured benefit/upkeep proxy, not computed from guessed stakes."""
H, D, W, MO, Y = 1.0, 24.0, 24.0 * 7, 24.0 * 30.4, 24.0 * 365.25
SEC, MIN = 1 / 3600, 1 / 60

SYSTEMS = [
 dict(name='E. coli', strong=True, measured=True, comps=[
   # MEASURED (PR #110, branch v2.5-measure, theory/measured/measured.json, Mattingly et al. 2021 conditions): the world is ONE OU signal
   # (the swim's log-concentration gradient, tau_v = 1.16 s) read through its integral, McMillan degree 2, so it is ONE component of
   # degree 2 and gets 2 stores (counted by degree; the measured kernel has 2 poles).  Its ratio is a measured PROXY, benefit / signalling share
   # (fitness benefit of chemotaxis in poor carbon, Ni et al. 2019 (PNAS, issued 23 Dec 2019), over the signalling machinery's proteome share): log10 -0.26 .. 1.89,
   # central 0.81 (v2.5 read this as X_L itself; withdrawn, see below).
   # Latency l/tau_fast: log10 -0.76 (-1.47 .. -0.58), snr 0.0043-0.103 (arm B); both are already inside the measured benefit.
   # n = 1: no shared option.  v2.5.1 (review 26): this is a PLAUSIBILITY PROXY, not X_L -- the benefit is of motility plus chemotaxis
   # (it needs the flagella) while the cost is the signalling proteome share only, a proteome share is not a fitness cost (growth law
   # conversion about 2x), and B.11 covers one layer per component while this component has degree 2.  Drawn apart from the map.
   dict(lab='gradient signal', degree=2, logXL=(-0.263, 1.893), logXL_c=0.815, tau=(1.16 * SEC, 1.16 * SEC),
        lead=(10 ** -1.468 * 1.16 * SEC, 10 ** -0.582 * 1.16 * SEC), n=(1, 1), rho=(1, 1), snr=(0.0043, 0.103), R=(10 ** -0.263, 10 ** 1.893), hc=(1, 1))]),
 dict(name='immune system', strong=True, comps=[
   dict(lab='innate', tau=(1 * H, 10 * H), lead=(12 * H, 48 * H), n=(100, 1000), rho=(0.1, 0.5), snr=(1, 30), R=(30, 3000), hc=(3, 100)),
   dict(lab='adaptive', tau=(5 * D, 30 * D), lead=(12 * H, 48 * H), n=(100, 1000), rho=(0.5, 1.0), snr=(0.3, 10), R=(3, 300), hc=(3, 100)),
   dict(lab='memory', tau=(10 * Y, 100 * Y), lead=(1 * D, 7 * D), n=(100, 1000), rho=(0.7, 1.0), snr=(10, 1000), R=(0.3, 30), hc=(3, 100))]),
 dict(name='ant colony', strong=True, comps=[
   # One species throughout: the trail-recruiting black garden ant Lasius niger (v2.5.1; v2.5 mixed in harvester ants).
   # patch: where food is now.  Shared physical store: the pheromone trail (Beckers, Deneubourg & Goss 1993, 10.1007/bf01201674; the often
   #   cited ~47 min trail lifetime is NOT checked against the full text, so tau is kept wide).  Local store: each forager's private route
   #   memory (Grueter, Czaczkes & Ratnieks 2011 (online 2010), 10.1007/s00265-010-1020-2).  rho = 0-0.3, the v2.5 range, restored
   #   (review 26 round 2: inputs are frozen; v2.5.1 had raised it to 0.3-0.9 with a reason that argued the other way).  A trail marks one
   #   route and serves only the foragers working that patch, so little of what one forager meets is met by all (guess).
   dict(lab='patch', tau=(20 * MIN, 3 * H), lead=(15 * MIN, 45 * MIN), n=(100, 1000), rho=(0.0, 0.3), snr=(0.3, 10), R=(3, 300), hc=(1, 30)),
   # food supply: the colony's nutritional state.  Hypothesized shared store: food held in nestmates' crops and passed by trophallaxis
   #   (named, not measured as a store; no source used).  rho high: the colony's intake is common to all its workers (guess).
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
