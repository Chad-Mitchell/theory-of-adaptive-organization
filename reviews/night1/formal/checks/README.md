# Formal-layer check scripts (s1–s12)

These are the scripts behind `reviews/night1/formal/THEOREMS.md` (Lemma 1, Theorems 1–8, Propositions 9–11) and the adversarial pass in `FIXES.md`. Both files cite them by name as `checks/s1_classes.py` … `checks/s12_mc_base.py`.

**Provenance (19 Nov 2026, ET; added with THEORY v2.0 work, LOAD_BEARING X2).** They were not in the repository: the night-1 work was done in an off-repo working copy, and only the Markdown was committed. They were recovered unchanged from that working copy on the project's shared machine (`night1/FORMAL/checks/`). The file times there reflect a later copy, not authorship.

**Re-run, 19 Nov 2026, about 12:40 AM ET** (Python 3, sympy, numpy, scipy; `nice -n 19`): all twelve scripts exit 0, and every `.out` file reproduced **byte for byte** (s1 9 s, s6 28 s, s7 about 2 min, the rest a few seconds each). The `.out` files committed here are the originals, identical to the re-run.

```
for s in s1_classes s2_onset s3_bundling s4_lattice s5_phase s6_depth s7_misc s8_broadcast s9_attack s10_extremes s11_vclosed s12_mc_base; do python3 $s.py > $s.out; done
```

These are the authors' own checks (same bot family), not an independent review.
