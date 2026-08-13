namespace GLC0

universe u v

/-- A task contract separates the legal input domain from output correctness. -/
structure TaskSpec (Input : Type u) (Output : Type v) where
  dom : Input → Prop
  spec : Input → Output → Prop

end GLC0
