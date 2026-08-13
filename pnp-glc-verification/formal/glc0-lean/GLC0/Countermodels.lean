import GLC0.Core

namespace GLC0
namespace Countermodels

def boolTask : TaskSpec Unit Bool where
  dom _ := True
  spec _ y := y = true

def terminalNoOutputSystem : System Unit Bool Unit where
  init _ _ := True
  step _ _ _ := False
  halt _ _ := True
  emit _ _ _ := False
  halt_no_step := by
    intro x s hHalt
    simp

/-- A halted state need not have any output. -/
theorem terminal_no_output :
    terminalNoOutputSystem.halt () () ∧
      ¬ OutDef terminalNoOutputSystem () () := by
  simp [terminalNoOutputSystem, OutDef]

theorem terminal_no_output_not_good :
    ¬ GoodTerminal boolTask terminalNoOutputSystem () () := by
  simp [GoodTerminal, terminalNoOutputSystem, OutDef]

inductive SplitState where
  | start
  | good
  | bad
  deriving DecidableEq, Repr

def splitSystem : System Unit Bool SplitState where
  init _ s := s = .start
  step _ s t :=
    (s = .start ∧ t = .good) ∨
    (s = .start ∧ t = .bad)
  halt _ s := s = .good ∨ s = .bad
  emit _ s y :=
    (s = .good ∧ y = true) ∨
    (s = .bad ∧ y = false)
  halt_no_step := by
    intro x s hHalt
    rintro ⟨t, hStep⟩
    rcases hHalt with hGood | hBad
    · subst s
      simp at hStep
    · subst s
      simp at hStep

def goodRun : Run SplitState
  | 0 => some .start
  | 1 => some .good
  | _ => none

def badRun : Run SplitState
  | 0 => some .start
  | 1 => some .bad
  | _ => none

def splitPolicy : RunPolicy Unit SplitState where
  std _ ρ := ρ = goodRun
  adm _ ρ := ρ = goodRun ∨ ρ = badRun
  fair _ _ := True

def noDebt : Unit → Run SplitState → Nat → Prop :=
  fun _ _ _ => True

theorem prefix_refl (ρ : Run State) : Prefix ρ ρ := by
  intro n s hAt
  exact hAt

theorem goodRun_valid : RunValid splitSystem () goodRun := by
  refine ⟨⟨.start, rfl, rfl⟩, ?_, ?_⟩
  · intro n s t hs ht
    cases n with
    | zero =>
        simp [At, goodRun] at hs ht
        subst s
        subst t
        exact Or.inl ⟨rfl, rfl⟩
    | succ n =>
        cases n with
        | zero =>
            simp [At, goodRun] at ht
        | succ n =>
            simp [At, goodRun] at hs
  · intro n hn
    cases n with
    | zero =>
        simp [goodRun] at hn
    | succ n =>
        cases n with
        | zero =>
            simp [goodRun] at hn
        | succ n =>
            simp [goodRun]

theorem badRun_valid : RunValid splitSystem () badRun := by
  refine ⟨⟨.start, rfl, rfl⟩, ?_, ?_⟩
  · intro n s t hs ht
    cases n with
    | zero =>
        simp [At, badRun] at hs ht
        subst s
        subst t
        exact Or.inr ⟨rfl, rfl⟩
    | succ n =>
        cases n with
        | zero =>
            simp [At, badRun] at ht
        | succ n =>
            simp [At, badRun] at hs
  · intro n hn
    cases n with
    | zero =>
        simp [badRun] at hn
    | succ n =>
        cases n with
        | zero =>
            simp [badRun] at hn
        | succ n =>
            simp [badRun]

theorem not_prefix_good_bad : ¬ Prefix goodRun badRun := by
  intro hPrefix
  have hAt : At goodRun 1 .good := rfl
  have := hPrefix 1 .good hAt
  simp [At, badRun] at this

theorem not_prefix_bad_good : ¬ Prefix badRun goodRun := by
  intro hPrefix
  have hAt : At badRun 1 .bad := rfl
  have := hPrefix 1 .bad hAt
  simp [At, goodRun] at this

theorem goodRun_maximal :
    Maximal splitSystem splitPolicy () goodRun := by
  rintro ⟨ρ', hAdm, hValid, hProper⟩
  rcases hAdm with hGood | hBad
  · subst ρ'
    exact hProper.2 (prefix_refl goodRun)
  · subst ρ'
    exact not_prefix_good_bad hProper.1

theorem badRun_maximal :
    Maximal splitSystem splitPolicy () badRun := by
  rintro ⟨ρ', hAdm, hValid, hProper⟩
  rcases hAdm with hGood | hBad
  · subst ρ'
    exact not_prefix_bad_good hProper.1
  · subst ρ'
    exact hProper.2 (prefix_refl badRun)

theorem split_wfStd : WFStd boolTask splitSystem splitPolicy := by
  constructor
  · intro x hx
    exact ⟨goodRun, rfl⟩
  · intro x ρ hStd
    simp [splitPolicy] at hStd
    subst ρ
    exact goodRun_valid

theorem split_wfRobust : WFRobust boolTask splitSystem splitPolicy := by
  constructor
  · intro x hx
    exact ⟨goodRun, Or.inl rfl, goodRun_valid, goodRun_maximal, trivial⟩
  · intro x ρ hAdm
    simp [splitPolicy] at hAdm
    rcases hAdm with hGood | hBad
    · subst ρ
      exact goodRun_valid
    · subst ρ
      exact badRun_valid

theorem split_glc0Std :
    GLC0Std boolTask splitSystem splitPolicy noDebt := by
  refine ⟨split_wfStd, ?_⟩
  intro x ρ hx hStd
  simp [splitPolicy] at hStd
  subst ρ
  refine ⟨1, .good, rfl, ?_, trivial⟩
  simp [GoodTerminal, OutDef, OutSound, boolTask, splitSystem]

theorem badRun_never_good
    (n : Nat)
    (s : SplitState)
    (hAt : At badRun n s) :
    ¬ GoodTerminal boolTask splitSystem () s := by
  cases n with
  | zero =>
      simp [At, badRun] at hAt
      subst s
      simp [GoodTerminal, OutDef, splitSystem]
  | succ n =>
      cases n with
      | zero =>
          simp [At, badRun] at hAt
          subst s
          simp [GoodTerminal, OutDef, OutSound, boolTask, splitSystem]
      | succ n =>
          simp [At, badRun] at hAt

/-- The policy is well formed, standard GLC0 holds, and robust GLC0 fails. -/
theorem std_not_robust_countermodel :
    GLC0Std boolTask splitSystem splitPolicy noDebt ∧
      ¬ GLC0Robust boolTask splitSystem splitPolicy noDebt := by
  constructor
  · exact split_glc0Std
  · intro hRobust
    have hSolved :=
      hRobust.2 () badRun trivial (Or.inr rfl) badRun_maximal trivial
    rcases hSolved with ⟨n, s, hAt, hGood, hDebt⟩
    exact (badRun_never_good n s hAt) hGood

end Countermodels
end GLC0
