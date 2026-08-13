import GLC0.Core

namespace GLC0

inductive RunMode where
  | standard
  | robust
  deriving DecidableEq, Repr

inductive ResourceRegime where
  | neutral
  | bounded
  deriving DecidableEq, Repr

inductive Gate where
  | provenance
  | runClassNonempty
  | maximality
  | fairness
  | accountCompleteness
  | budget
  deriving DecidableEq, Repr

/-- Evidence insufficiency is distinct from a proved violation. -/
inductive GateVal where
  | pass
  | fail
  | unknown
  | notApplicable
  deriving DecidableEq, Repr

def ApplicableRun (mode : RunMode) (gate : Gate) : Prop :=
  match gate with
  | .provenance | .runClassNonempty => True
  | .maximality | .fairness => mode = .robust
  | .accountCompleteness | .budget => False

def ApplicableResource (regime : ResourceRegime) (gate : Gate) : Prop :=
  match gate with
  | .accountCompleteness => True
  | .budget => regime = .bounded
  | _ => False

def Applicable (mode : RunMode) (regime : ResourceRegime) (gate : Gate) : Prop :=
  ApplicableRun mode gate ∨ ApplicableResource regime gate

/-- Applicable gates begin unknown until evidence validation derives pass or fail. -/
def InitialGateVal
    (mode : RunMode)
    (regime : ResourceRegime)
    (gate : Gate) : GateVal :=
  match gate with
  | .provenance | .runClassNonempty => .unknown
  | .maximality | .fairness =>
      match mode with
      | .standard => .notApplicable
      | .robust => .unknown
  | .accountCompleteness => .unknown
  | .budget =>
      match regime with
      | .neutral => .notApplicable
      | .bounded => .unknown

def GatePass (value : GateVal) : Prop :=
  value = .pass

def AllApplicablePass
    (mode : RunMode)
    (regime : ResourceRegime)
    (value : Gate → GateVal) : Prop :=
  ∀ gate, Applicable mode regime gate → GatePass (value gate)

/-- The shared gate has mode-indexed semantics, rather than one ambiguous meaning. -/
def RunClassNonempty
    (mode : RunMode)
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) : Prop :=
  match mode with
  | .standard => CanonicalRunFamilyExists task policy
  | .robust => AdmissibleMaxFairRunFamilyExists task sys policy

@[simp] theorem runClass_applicable
    (mode : RunMode)
    (regime : ResourceRegime) :
    Applicable mode regime .runClassNonempty := by
  cases mode <;> simp [Applicable, ApplicableRun]

@[simp] theorem standard_maximality_not_applicable
    (regime : ResourceRegime) :
    ¬ Applicable .standard regime .maximality := by
  cases regime <;>
    simp [Applicable, ApplicableRun, ApplicableResource]

@[simp] theorem standard_fairness_not_applicable
    (regime : ResourceRegime) :
    ¬ Applicable .standard regime .fairness := by
  cases regime <;>
    simp [Applicable, ApplicableRun, ApplicableResource]

@[simp] theorem robust_maximality_applicable
    (regime : ResourceRegime) :
    Applicable .robust regime .maximality := by
  cases regime <;> simp [Applicable, ApplicableRun]

@[simp] theorem robust_fairness_applicable
    (regime : ResourceRegime) :
    Applicable .robust regime .fairness := by
  cases regime <;> simp [Applicable, ApplicableRun]

@[simp] theorem accountCompleteness_applicable
    (mode : RunMode)
    (regime : ResourceRegime) :
    Applicable mode regime .accountCompleteness := by
  cases mode <;> cases regime <;>
    simp [Applicable, ApplicableResource]

@[simp] theorem neutral_budget_not_applicable
    (mode : RunMode) :
    ¬ Applicable mode .neutral .budget := by
  cases mode <;>
    simp [Applicable, ApplicableRun, ApplicableResource]

@[simp] theorem bounded_budget_applicable
    (mode : RunMode) :
    Applicable mode .bounded .budget := by
  cases mode <;>
    simp [Applicable, ApplicableResource]

@[simp] theorem fail_fails_closed : ¬ GatePass .fail := by
  simp [GatePass]

@[simp] theorem unknown_fails_closed : ¬ GatePass .unknown := by
  simp [GatePass]

theorem unknown_blocks_admission
    (mode : RunMode)
    (regime : ResourceRegime)
    (value : Gate → GateVal)
    (gate : Gate)
    (hApplicable : Applicable mode regime gate)
    (hUnknown : value gate = .unknown) :
    ¬ AllApplicablePass mode regime value := by
  intro hAll
  have hPass := hAll gate hApplicable
  rw [hUnknown] at hPass
  exact unknown_fails_closed hPass

@[simp] theorem standard_runClass_meaning
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) :
    RunClassNonempty .standard task sys policy =
      CanonicalRunFamilyExists task policy :=
  rfl

@[simp] theorem robust_runClass_meaning
    (task : TaskSpec Input Output)
    (sys : System Input Output State)
    (policy : RunPolicy Input State) :
    RunClassNonempty .robust task sys policy =
      AdmissibleMaxFairRunFamilyExists task sys policy :=
  rfl

end GLC0
