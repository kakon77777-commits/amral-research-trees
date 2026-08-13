import GLC0.Runs

namespace GLC0

universe u v w

def OutDef
    (sys : System Input Output State)
    (x : Input)
    (s : State) : Prop :=
  ∃ y, sys.emit x s y

def OutSound
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (x : Input)
    (s : State) : Prop :=
  ∀ y, sys.emit x s y → task.spec x y

def GoodTerminal
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (x : Input)
    (s : State) : Prop :=
  sys.halt x s ∧ OutDef sys x s ∧ OutSound task sys x s

theorem good_terminal_unfold
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (x : Input)
    (s : State) :
    GoodTerminal task sys x s ↔
      sys.halt x s ∧ OutDef sys x s ∧ OutSound task sys x s :=
  Iff.rfl

def Solved0
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (zeroDebt : Input → Run State → Nat → Prop)
    (x : Input)
    (ρ : Run State) : Prop :=
  ∃ n s, At ρ n s ∧ GoodTerminal task sys x s ∧ zeroDebt x ρ n

def GLC0Std
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State)
    (zeroDebt : Input → Run State → Nat → Prop) : Prop :=
  WFStd task sys policy ∧
  ∀ x ρ, task.dom x → policy.std x ρ →
    Solved0 task sys zeroDebt x ρ

def GLC0Robust
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State)
    (zeroDebt : Input → Run State → Nat → Prop) : Prop :=
  WFRobust task sys policy ∧
  ∀ x ρ, task.dom x → policy.adm x ρ →
    Maximal sys policy x ρ → policy.fair x ρ →
    Solved0 task sys zeroDebt x ρ

/-- Elementary conditional lemma: universal robust correctness specializes to standard runs. -/
theorem robust_to_std
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State)
    (zeroDebt : Input → Run State → Nat → Prop)
    (hWFStd : WFStd task sys policy)
    (hRobust : GLC0Robust task sys policy zeroDebt)
    (hInclude : ∀ x ρ, task.dom x → policy.std x ρ →
      policy.adm x ρ ∧ Maximal sys policy x ρ ∧ policy.fair x ρ) :
    GLC0Std task sys policy zeroDebt := by
  refine ⟨hWFStd, ?_⟩
  intro x ρ hx hStd
  rcases hInclude x ρ hx hStd with ⟨hAdm, hMax, hFair⟩
  exact hRobust.2 x ρ hx hAdm hMax hFair

end GLC0
