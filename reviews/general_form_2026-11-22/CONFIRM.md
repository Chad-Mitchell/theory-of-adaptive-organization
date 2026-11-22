# Confirm: physics-derived general form, 22 November 2026

Independent read of draft PR #182 at head `26961e8018592d0b98b203451c6dafc92320ffc8` (branch `general-form-physics-2026-11-22`, base `main` `6ca6b452895056372ba5f98f324baf46e196b2bf`). That branch was not edited. This file is the only change against `main`. The text reviewed is `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` at `26961e8`, together with the three accompanying edits (`OPEN_WORK.md`, `theory/DERIVATION_CHAIN.md`, `theory/README.md`). Numbers below were recomputed from the closed forms and from the linear SDEs. Merged sources are `theory/INFO_PHYSICS.md`, `theory/INFO_PHYSICS_ATTAINABILITY.md`, and `theory/INFO_PHYSICS_GENERAL.md`.

## Protected files

`git diff origin/main -- THEORY.md CORE.md README.md` is empty (exit 0) at `26961e8`. The hypothesis sentence is present once in each file, with the same bytes, including the bold markers:

**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

The same bytes appear twice in the note, at the cost display and again in §9. The note does not edit `THEORY.md`.

## Listed items

**B1, formula.** Fixed in the display. §4 states the telegraph information flow, in nats per unit time, as \(\dot I=\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\), the heat as \(kT\,\gamma(1-2\varepsilon)\ln\rho\), and the infimum as \(kT\,\dot I\). That matches `theory/INFO_PHYSICS.md` line 290. The same split is in §1 (rates in nats per unit time; \(kT\) times a rate is the heat bound), in the centered-spring paragraph of §3 (flow from \(a(v-\varepsilon)/\varepsilon\) up to \(av/\varepsilon\); the heat's fast limit and \(kT\) times the Kalman rate differ by \(kT\,a\)), and in the proposed THEORY paragraph (the listed rates have no \(kT\); the heat is at least \(kT\) times the rate). At \(\varepsilon=0.2\), \(\gamma=1\), \(0.6\ln 4=0.831776616671934\), which rounds to the printed \(0.831776616672\).

**B1, the next sentence.** Blocking. The same paragraph says the flow equals \(0.831776616672\) only because \(kT=1\). The flow at those \(\varepsilon\) and \(\gamma\) is \(0.6\ln 4\) at every temperature. The heat infimum is \(kT\) times that flow, so the heat infimum equals \(0.831776616672\) only because \(kT=1\). The sentence assigns the temperature factor to the flow.

**B2.** Fixed. The two proposed sentences state a lower bound, \(kT\) times the learning rate, and say a fast memory approaches that floor in the limit of a diverging rate, at finite heat. They do not state equality. For the shrunk spring at \(a=v=kT=1\), \(\varepsilon=0.2\), \(\lambda=10^6\), the fast fraction is \(\varphi=\lambda/(a+\lambda)=1000000/1000001\) and the heat is exactly \(800000/199999=4.0000200001000005\ldots\), which is the printed \(4.0000200001\). The ratio to \(R=4\) is \(200000/199999=1.000005000025000125\ldots\), strictly above \(1\).

**S1.** Fixed. §0 restricts the bound to an equilibrium Ornstein–Uhlenbeck signal, independent collections of those signals, and the two-state telegraph, and it says a fast memory approaches the floor.

**S2.** Fixed. Recomputed for rates \((1,100)\), variances \((1,1)\).

| Quantity | Value | Printed |
|---|---|---|
| \(\mu\) at sum-error \(0.5\), the positive root of \(\mu^2-101\mu-300=0\) | \(103.887732673339856\) | \(103.887732673340\) |
| Separate heat at that error, errors \(1/22\) and \(10/22\) | \(141\) exactly | \(141\) |
| Ratio \(141/\mu\) | \(1.35723435647\) | \(1.357234\) |
| Spring at \(\lambda=10^6\): heat, learning rate, sum-error | \(103.877719378448\), \(103.856919702138\), \(0.500076936208\) | heat \(103.877719\), sum-error \(0.500077\) |
| Floor \(\mu\) at the realized sum-error | \(103.856919445098\) | \(103.856919\) |

The spring heat sits above that floor. The merged note's learning rate \(103.856920\) is this spring's learning rate rounded to six decimals. It is a different quantity from the floor at the realized error. §4 cites `reviews/heat_floor_general_2026-11-22/recompute.out` for the floor, and that file has \(103.856919445098\).

**S3.** Fixed. The shrunk-spring factor is \(\varphi\varepsilon/(\varphi(v+\varepsilon)-v)\) with \(\varphi=\lambda/(a+\lambda)\). In this note \(\rho\) is the telegraph rate ratio and the ladder ratio.

**N.** Fixed. At \(\lambda=10^6\), decision error \(0.2\), the path rate is \(999.503125010117\) and \(L/\mathcal T=0.004001988488\), which rounds to \(0.004002\). Gorbunov and Pinsker (1973, 1974) are cited with no DOI, in §6 and in §10, with the statement that Crossref returned no work record for either English translation. That matches the review record of PR #180.

## Fresh read

The proved scope in §3 matches the merged class: exogenous equilibrium OU, independent collections, telegraph under Hamming error, memory not feeding back on the signal, and the two losses named there. A coupled diffusion, a joint telegraph memory, a \(K\)-state bath heat, finite-rate equality, and a memory that moves the signal stay on the open list. Stake, a separate acquisition summand, linking, the ruin cap, and H3 are labeled as assumptions. IP5 stays **FALSE**. The cited merge commits resolve to the named pull requests: `2dd04fa` (#161), `01e4415` (#164), `f18f21f` (#175), `5fbf525` (#176), `c9f02df` (#177), `b46bf9f` (#178), `74e02e7` (#179), `d1d6ea5` (#180), `fbf03b7` (#181).

Other recomputed displays match the sources. The centered spring at rate \(10^6\) has heat \(5.000020000080\) at raw error \(0.2\), and heat \(4.000012000036\) with conditional error \(0.200000319999\) at raw error \(0.25\). The second per-mode heat is \(1600000/99998=16.000320006400\) against floor \(16\), the shrunk spring at \((a,v,\varepsilon)=(4,0.5,0.1)\). Stake \(2\) costs \(2\sqrt{2}-1=1.828427124746190\). Three modes at rates \((1,10,100)\), unit variance, stake \(2\), cost \(5.828427124746190\). Four-mode \(w_0=1000/1111\). The gain at rate \(6\) is \(1.2\). The check scripts print the 64-bin learning rate \(4.022937\) at decision error \(0.2\), and the coupled design heat \(7.999913\) against static rate \(8\). CORE states efficiency \(0.9574\) on one world.

One non-blocking gap: §4 states the heats \(4.000020\) and \(16.000320\) without repeating \((a,v,\varepsilon)=(4,0.5,0.1)\). `theory/INFO_PHYSICS_GENERAL.md` states that pair. The numbers match.

## Checks at `26961e8`

| Command | Result |
|---|---|
| `python3 tools/check_consistency.py` | PASS, 0 FAIL |
| `python3 tools/check_open_work.py` | PASS, 0 missing |
| `python3 tools/check_fresh.py` | PASS. STATUS pointer `fbf03b7`; window includes `6ca6b45` |
| `python3 theory/info_physics_checks/info_physics_checks.py` | PASS 61, FAIL 0 |
| `python3 theory/info_physics_checks/attainability_checks.py` | PASS 31, FAIL 0 |
| `python3 theory/info_physics_checks/general_checks.py` | PASS 33, FAIL 0 |
| `python3 -m pytest -q tools` | 255 passed, 1 skipped (`tools/test_lean.py:101`, lake not installed), 342.42 s |

No lake build was run. The check counts 61, 31, and 33 match §11.

CONFIRM: NOT READY (blocking: §4 says the telegraph flow equals \(0.831776616672\) only because \(kT=1\); the flow is \(0.6\ln 4\) at every temperature, and the heat floor equals that number only because \(kT=1\)).

## Addendum, 22 November 2026, head `e233a3f`

Re-read at `e233a3f9e57fe3cae3f8ab92d9b0f8d51374928e` on `general-form-physics-2026-11-22`. That commit's parent is `26961e8`. `git diff --stat 26961e8..e233a3f` is one line in `theory/GENERAL_FORM_PHYSICS_2026-11-22.md` and nothing else. `git diff origin/main e233a3f -- THEORY.md CORE.md README.md` is empty. The proposal branch was not edited from this confirm.

§4 now reads: the flow is \(0.6\ln 4\) nats per unit time at every temperature; the heat infimum equals that number only because \(kT=1\). At \(\varepsilon=0.2\) and \(\gamma=1\), the flow \(\gamma(1-2\varepsilon)\ln((1-\varepsilon)/\varepsilon)\) is \(0.6\ln 4=0.831776616671934\) with no factor of \(kT\). The heat infimum is \(kT\) times that flow, so it equals the printed number only at \(kT=1\). The sentence matches the formulas on the same line and `theory/INFO_PHYSICS.md` line 290. The earlier blocking reading is closed. The non-blocking gap on the unnamed second design \((a,v,\varepsilon)=(4,0.5,0.1)\) is unchanged.

| Command, run on the tree at `e233a3f` | Result |
|---|---|
| `python3 tools/check_consistency.py` | PASS, 0 FAIL |
| `python3 tools/check_open_work.py` | PASS, 0 missing |
| `python3 tools/check_fresh.py` | PASS. STATUS pointer `fbf03b7`; window `6ca6b45 fbf03b7 d1d6ea5 954fc2f 74e02e7` |

CONFIRM: READY
