/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
`#print axioms` for the 91 exported theorems of the record-cost side R&D
(`GTAO/Rnd/`, `theory/RECORD_COST_CHAIN_2026-11-25.md`; then 19, `SelfRef.R78.*`, for
`theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10; then 4, `SelfRef.R10.*`, for
`theory/RECORD_COST_ROUND10_2026-11-25.md` §11; then `SelfRef.LR3.*`, Lean round 3, for
the rounds 4–9 note §10 item L5 and later items, labels in `formal/lean/README.md`).
Run from `formal/lean/`:  `lake env lean scripts/RndAxioms.lean`
Expected: each line lists only `propext`, `Classical.choice`, `Quot.sound` (or a subset),
or says the theorem depends on no axioms.
-/
import GTAO
open GTAORnd
#print axioms CopyModel.lemmaB1_k
#print axioms CopyModel.clone2_to_k
#print axioms CopyModel.lemmaB1
#print axioms square_capacity_le_two
#print axioms square_B1_hypotheses
#print axioms square_no_clone
#print axioms discrete_oneParam_trivial
#print axioms dihedral_oneParam_trivial
#print axioms simplexPerm_oneParam_trivial
#print axioms disk_oneParam
#print axioms ring_closed_form
#print axioms ring_bound
#print axioms factor_ge_two
#print axioms ring_ratio_indep
#print axioms ring_cost_lower_bound
#print axioms disk_strictly_cheaper
#print axioms Spekkens.forced
#print axioms Spekkens.no_injective_clone
#print axioms Spekkens.no_perm_clone
#print axioms Spekkens.disjoint_pair_clonable
#print axioms Spekkens.singletons_clonable
#print axioms SelfRef.liar_half
#print axioms SelfRef.sharp_flip_no_fixed
#print axioms SelfRef.exists_fixedPointFree
#print axioms SelfRef.sharpCopy_facts
#print axioms SelfRef.no_linear_clone_orbit
#print axioms SelfRef.no_linear_clone_moved
#print axioms SelfRef.measure_prepare_clones
#print axioms SelfRef.measure_prepare_covariant
#print axioms SelfRef.distinguishable_affineIndependent
#print axioms SelfRef.dim_bound
#print axioms SelfRef.dim_bound_one_bit
#print axioms SelfRef.Jdial_hasDerivAt
#print axioms SelfRef.Jdial_stationary_iff
#print axioms SelfRef.Jdial_midpoint
#print axioms SelfRef.Jdial_midpoint_60
#print axioms SelfRef.inv_sqrt3_bracket
#print axioms SelfRef.Jdial_rho_zero
#print axioms unitModel_clones
#print axioms SelfRef.top_coeff_zero
#print axioms SelfRef.circle_top_zero
#print axioms SelfRef.circle_all_zero
#print axioms SelfRef.no_linear_clone_circle
#print axioms SelfRef.normal_fixer_bot
#print axioms SelfRef.normal_nontrivial_fixes_nothing
#print axioms SelfRefRun.liar_half
#print axioms SelfRefRun.exists_derangement
#print axioms SelfRefRun.four_point
#print axioms SelfRefRun.no_copier_four_point
#print axioms SelfRefRun.perm_periodic
#print axioms SelfRefRun.path_sq_one_const
#print axioms SelfRefRun.midpoint_rho
#print axioms SelfRefRun.no_zero_drift_while_recording
#print axioms SelfRefRun.normal_fixer_trivial
#print axioms SelfRef.fourier_core
#print axioms SelfRef.no_linear_clone_gpt
#print axioms SelfRef.F1_cycle_count
#print axioms SelfRef.R3_full
#print axioms Composition.P1
#print axioms Composition.log_additive_iff
#print axioms Composition.P2_entries
#print axioms Composition.gbit_no_local_write
#print axioms SelfRef.R78.jordan_derangement
#print axioms SelfRef.R78.finite_transitive_not_SFP
#print axioms SelfRef.R78.simplex_not_SFP
#print axioms SelfRef.R78.square_rotation_moves_all
#print axioms SelfRef.R78.square_not_SFP
#print axioms SelfRef.R78.SO_odd_fixes_unit
#print axioms SelfRef.R78.SO_odd_fixes_poles
#print axioms SelfRef.R78.SO3_fixes_poles
#print axioms SelfRef.R78.odd_ball_SFP
#print axioms SelfRef.R78.SO2_nonid_no_fixed
#print axioms SelfRef.R78.disk_not_SFP
#print axioms SelfRef.R78.even_ball_not_SFP
#print axioms SelfRef.R78.ball_record_bound
#print axioms SelfRef.R78.chord
#print axioms SelfRef.R78.disk_record_error
#print axioms SelfRef.R78.disk_error_linear
#print axioms SelfRef.R78.disk_exceeds_ball
#print axioms SelfRef.R78.mixture_copy_core
#print axioms SelfRef.R78.no_copy_mixture
#print axioms SelfRef.R10.continuous_line_discrete_const
#print axioms SelfRef.R10.finite_group_no_continuous_motion
#print axioms SelfRef.R10.continuous_change_infinite_group
#print axioms SelfRef.R10.never_returns_infinite_order
#print axioms SelfRef.LR3.amplify
#print axioms SelfRef.LR3.L5_asymptotic
#print axioms SelfRef.LR3.L5_perfect
#print axioms SelfRef.LR3.L5_pairwise
#print axioms SelfRef.LR3.bit_achSet
#print axioms SelfRef.LR3.L5_control
