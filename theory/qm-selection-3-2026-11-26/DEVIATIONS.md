# Deviations from PREREG.md

None so far (lock commit).

## After the run (appended 2026-11-26, 09:00 ET)

- F4 timestamp note (gate read of e496428): the lock commit e496428 was committed at 06:50:23 ET, inside the "06:47–07:00 ET" window stated in the PREREG header, and pushed at 07:11:45 ET. PREREG.md is not edited. No deviation from the method: the locked command ran once from a fresh clone (see RESULTS.md).

- 2026-11-27 (ET): two measurement/code misses found in the run itself (RESULTS Surprises 2–3). (i) `rank2_bodies` built the 5⊕10 vectors from two different maximal tori, so the 128 bodies are not the locked family: scored `not tested`, not MISS. (ii) `sfp_rank_test` reports rank 1 at three adjoint singular directions where the true rank is 2 (KNOWN): bodies 249, 250, 914 are measurement/code, not MISS on SFP. The overall INCONCLUSIVE is unchanged. Neither moves any body to HIT (§6).
