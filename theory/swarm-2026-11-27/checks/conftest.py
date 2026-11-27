# test_swarm27_checks.py is locked by SHA256SUMS (first lock) and runs the
# unpatched script, whose toy run stopped (DEVIATIONS.md, D1). It is kept
# byte-identical for the lock and not collected; test_swarm27_run.py runs the
# patched script under the second lock (SHA256SUMS_2).
collect_ignore = ["test_swarm27_checks.py"]
