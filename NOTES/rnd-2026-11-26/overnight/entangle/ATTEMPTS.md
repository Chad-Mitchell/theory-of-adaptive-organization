# Round E attempts log (2026-11-26)
- E-A1 01:00 Read selfref R10b-M.2, R11-M, R12-M, forces-gravity NOTE, composition Q1/Q3. Plan: routes 3 → 1 → 2 → 4.
- E-A2 01:02 e1_interaction.py v1 (VF2 enumeration of all automorphisms) too slow on triangle² (9! maps). Killed and
  rewritten as a stabiliser chain (orbit-stabiliser with individualisation-refinement). All runs finish; max oct² 261 s.
- E-A3 01:05 Crossref: the brief's PNAS DOI is the wrong paper (information-unit postulate). The Bloch-ball paper is JMP
  2014 (10.1063/1.4903510). Read the MMPA premises: balls + connected group + LT, so it lives after U. Route 3 as
  briefed ("interaction ⇒ entanglement (MMPA) ⇒ U") is circular. Switched to: (a) derive I from tracking (E-L0);
  (b) derive E from tracking in a pure world (Theorem E1) for the U route.
- E-A4 01:10 E1 results: irreducible non-classical NR polytopes give only trivial maps (ratio 1); classical gives
  controlled maps.
- E-A5 01:12 E1b: square⊕square and the pyramid have controlled non-entangling interactions, so I alone does not exclude
  reducible parts. Theorem E1 (pure start) does. Stabilizer control: entangling found.
- E-A6 01:14 E2: lemma checks, CHSH table, octahedron read task (E4).
- E-A7 01:20 Steering message: hostile review. Wrote PREMISE_GRAPH.md and premise_graph.py (acyclic; I/E not assumed
  upstream). Found and stated that E1 and E-L0 are equivalences, so the residue is premise P. Adopted one RV rule
  (extends to composites); qubit SO(3) under RV.
- E-A8 01:30 Checked MMPA's CR text: the group is connected, so I ⇒ Ic. Chain α needs only Pprod (mixed allowed), not P.
- Dropped: claiming chain α derives U (it assumes B and CR); claiming E is derived outright (it is re-expressed).
