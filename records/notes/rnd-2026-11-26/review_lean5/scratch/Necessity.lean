import GTAO.Rnd.SelfRef.M11Blocks
import GTAO.Rnd.SelfRef.OnsetO
open Matrix GTAORnd.SelfRef.LR3.M11Cube GTAORnd.SelfRef.LR3.M11Blocks

/-- Reviewer check: if `d u * d v = 1`, the off-diagonal symmetric matrix `E_uv + E_vu`
is invariant under conjugation by `diag d`. So the separating condition is necessary for
the Schur step among diagonal families (README claim). -/
example {mA mB : ℕ} (u v : Idx mA mB) (huv : u ≠ v) (d : Idx mA mB → ℝ) (h : d u * d v = 1) :
    (diagonal d)ᵀ * (Matrix.single u v (1:ℝ) + Matrix.single v u 1) * diagonal d =
      Matrix.single u v 1 + Matrix.single v u 1 := by
  ext a b
  rw [diagonal_transpose, Matrix.mul_diagonal, Matrix.diagonal_mul]
  simp only [Matrix.add_apply, Matrix.single_apply]
  split_ifs <;> simp_all <;> nlinarith [mul_comm (d u) (d v)]

#print axioms m11_blocks
#print axioms m11_blocks_polytope
#print axioms m11_blocks_polytope_flips
#print axioms m11_cube_cross_polytope
#print axioms blocks_hyps_consistent
#print axioms GTAORnd.SelfRef.LR3.OnsetO.Setting.kkt
#print axioms GTAORnd.SelfRef.LR3.OnsetO.Setting.projection
#print axioms GTAORnd.SelfRef.LR3.OnsetO.example_values
#check @GTAORnd.SelfRef.LR3.M11Cube.autSet
