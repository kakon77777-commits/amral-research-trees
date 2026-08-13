import GLC0.TaskSpec

namespace GLC0

universe u v w

/-- A fixed transition system. One value of this structure is one algorithm witness. -/
structure System (Input : Type u) (Output : Type v) (State : Type w) where
  init : Input → State → Prop
  step : Input → State → State → Prop
  halt : Input → State → Prop
  emit : Input → State → Output → Prop
  halt_no_step : ∀ x s, halt x s → ¬ ∃ t, step x s t

end GLC0
