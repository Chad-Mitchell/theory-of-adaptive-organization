/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Axiom audit for the GTAO Lean project (OPEN_WORK T19).

Run from `formal/lean/`:  `lake env lean scripts/AxiomAudit.lean`
(`tools/check_lean.sh` runs it after `lake build`).

Every declaration defined in a `GTAO.*` module may depend only on Lean's
three standard axioms (`propext`, `Classical.choice`, `Quot.sound`).  A
declaration that used `sorry` would depend on `sorryAx` and fail here.
-/
import GTAO

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut bad : Array (Name × Array Name) := #[]
  let mut count : Nat := 0
  for (n, _) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? n then
      let mod := env.header.moduleNames[idx.toNat]!
      if (`GTAO).isPrefixOf mod then
        count := count + 1
        let axs ← liftCoreM <| collectAxioms n
        if axs.any (fun a => !allowed.contains a) then
          bad := bad.push (n, axs)
  if count == 0 then
    throwError "AxiomAudit: no GTAO declarations found"
  if bad.isEmpty then
    logInfo m!"AxiomAudit: OK ({count} GTAO declarations; only propext, Classical.choice, Quot.sound)"
  else
    throwError m!"AxiomAudit: non-standard axioms in {bad}"
