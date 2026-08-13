import GLC0.System

namespace GLC0

universe u v w

/-- Partial traces represent both finite and infinite executions. -/
abbrev Run (State : Type w) := Nat → Option State

def At (ρ : Run State) (n : Nat) (s : State) : Prop :=
  ρ n = some s

def DefinedAt (ρ : Run State) (n : Nat) : Prop :=
  ∃ s, At ρ n s

def Prefix (ρ ρ' : Run State) : Prop :=
  ∀ n s, At ρ n s → At ρ' n s

def ProperPrefix (ρ ρ' : Run State) : Prop :=
  Prefix ρ ρ' ∧ ¬ Prefix ρ' ρ

def Last (ρ : Run State) (n : Nat) : Prop :=
  DefinedAt ρ n ∧ ∀ m, n < m → ¬ DefinedAt ρ m

def Infinite (ρ : Run State) : Prop :=
  ∀ n, DefinedAt ρ n

/-- Valid runs start in an initial state, follow steps, and have no gaps. -/
def RunValid (sys : System Input Output State) (x : Input) (ρ : Run State) : Prop :=
  (∃ s, At ρ 0 s ∧ sys.init x s) ∧
  (∀ n s t, At ρ n s → At ρ (n + 1) t → sys.step x s t) ∧
  (∀ n, ρ n = none → ρ (n + 1) = none)

/-- Fairness remains an uninterpreted policy parameter in Phase 1. -/
structure RunPolicy (Input : Type u) (State : Type w) where
  std : Input → Run State → Prop
  adm : Input → Run State → Prop
  fair : Input → Run State → Prop

def Maximal
    (sys : System Input Output State)
    (policy : RunPolicy Input State)
    (x : Input)
    (ρ : Run State) : Prop :=
  ¬ ∃ ρ', policy.adm x ρ' ∧ RunValid sys x ρ' ∧ ProperPrefix ρ ρ'

/-- Standard-mode interpretation of the shared run-class-nonempty gate. -/
def CanonicalRunFamilyExists
    (task : TaskSpec Input Output)
    (policy : RunPolicy Input State) : Prop :=
  ∀ x, task.dom x → ∃ ρ, policy.std x ρ

/-- Robust-mode interpretation of the shared run-class-nonempty gate. -/
def AdmissibleMaxFairRunFamilyExists
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) : Prop :=
  ∀ x, task.dom x →
    ∃ ρ, policy.adm x ρ ∧ RunValid sys x ρ ∧
      Maximal sys policy x ρ ∧ policy.fair x ρ

def WFStd
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) : Prop :=
  CanonicalRunFamilyExists task policy ∧
  ∀ x ρ, policy.std x ρ → RunValid sys x ρ

def WFRobust
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) : Prop :=
  AdmissibleMaxFairRunFamilyExists task sys policy ∧
  ∀ x ρ, policy.adm x ρ → RunValid sys x ρ

end GLC0
