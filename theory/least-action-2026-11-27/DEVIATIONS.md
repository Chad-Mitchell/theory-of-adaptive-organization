# Deviations from the locked prereg

*Appended lines only. Lock: `theory/least-action-2026-11-27/PREREG.md`, sha256 `e19bc66cbaa67bee5703e8a2ebb398a574b80f674abe5fe3bbf3a4763f5987f4`, lock commit `b6ed7d84a879a69187d85ffc457a063495e8a4f2` (`LOCK.txt`).*

- 2026-11-27 23:20 ET: **Clock times in `LOCK.txt` and `gate_read.md` (`LA-TIME-1`, process).** Both files were committed at 23:15 ET (`b6ed7d84a879`, `35a4e0d84249`) but state 23:19 and 23:20 ET. The order that matters holds by git: lock `b6ed7d8`, then gate read `35a4e0d`, then the checks (`02c528e`, 23:16 ET) and Lean (`c31293a`, 23:17 ET). Neither file is edited. Logged in `process/FAILURES.md`.
- 2026-11-27 23:20 ET: **Lean file location (disclosure).** `checks/LeastAction.lean` was compiled with `lake env lean` inside `/tmp/gtao-lean/formal/lean` from a scratch folder that was then deleted; it is kept in this folder, not in `formal/lean`, so `tools/check_lean.sh` does not build it. Its module docstring states `discrete_heat_ge` in the divided form; the theorem is stated in the equivalent multiplied form (\(n\cdot\) heat \(\ge\) \((\gamma/dt)(\sum d_i)^2\)).
