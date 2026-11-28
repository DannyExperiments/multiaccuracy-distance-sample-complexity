import Std
namespace MultiRepair
/-- The two membership rows and the probability cube in Fig. 1. -/
def feasible (a b c : Rat) :=
  0 ≤ a ∧ a ≤ 1 ∧ 0 ≤ b ∧ b ≤ 1 ∧ 0 ≤ c ∧ c ≤ 1 ∧
  a+b = 1 ∧ b+c = 11/8
def distance (a b c : Rat) :=
  (max (a-3/4) (3/4-a) + max (b-1/4) (1/4-b) + max (c-1) (1-c))/3
theorem sharp : feasible (5/8) (3/8) 1 ∧ distance (5/8) (3/8) 1 = 1/12 ∧
    ∀ a b c, feasible a b c → 1/12 ≤ distance a b c := by
  refine ⟨by unfold feasible; grind, by unfold distance; grind, ?_⟩
  intro a b c h
  unfold feasible at h
  unfold distance
  grind
#print axioms sharp
end MultiRepair
