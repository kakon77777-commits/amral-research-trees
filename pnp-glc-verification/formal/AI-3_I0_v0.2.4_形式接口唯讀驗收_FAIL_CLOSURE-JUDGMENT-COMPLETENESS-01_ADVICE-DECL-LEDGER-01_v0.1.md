# AI-3 I0 v0.2.4 形式／接口凍結唯讀驗收 v0.1

日期：2026-08-09（Asia/Taipei）  
角色：AI-3 Formalizer  
候選：I0 v0.2.4 frozen candidate  
審查類型：exact-bytes、manifest-scoped、read-only formal/interface acceptance

## 1. Disposition

**FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01 + ADVICE-DECL-LEDGER-01**

- `CLOSURE-CLASS-01`：**CLOSED / executable PASS**。
- `CLOSURE-EDGE-SCOPE-01`：目標 scope/precedence 修補本身 **CLOSED / executable PASS**。
- `ORACLE-DECL-FAMILY-01`：目標 typed declaration binding **CLOSED / executable PASS**。
- `CLOSURE-JUDGMENT-COMPLETENESS-01`：**Definition/interface blocker**；normative judgment dependency graph 未閉合。
- `ADVICE-DECL-LEDGER-01`：**accepted-record declaration/ledger consistency Counterexample**；有效簽章後可接受互相矛盾的 advice declaration 與 ledger/generator/access 狀態。

兩個 blocker 互相獨立。第一個不是 admission bypass；第二個不是實際 truth-table 計算、資源隱藏或 correctness bypass。兩者均無 P/NP 推論。

候選維持 `CANDIDATE_UNPROMOTED`；本報告不授權 Board success、共享 repo 或 default CLI promotion。

## 2. Freeze identity 與唯讀性

| 對象 | SHA-256 / 結果 |
|---|---|
| `SHA256SUMS-v0.2.4-candidate.txt` | `73ED3607EAD3F50502DCEFA3142DFFEE01AAC8576C045F05CA96DEB9669F77FE` |
| manifest entries | 153；format/missing/mismatch/duplicate = 0 |
| schema | `16EBCC7DE4196D0C46FC9C309F2060F856E321C0012C5B775390C04234F9DCC8` |
| validator | `B744C9C20C510FE39F132E0DFB4AAC50E6E3E573B48B7F1AE19494F5D5195FED` |
| closure spec | `579B6F7DA8BE3712FE6130AD900CF0CBA189496100548CBF87655687A7690588` |
| evidence-role spec | `4EFC4C71C6275227B14429E58FCECC4E949459918315D27CC476765C7D24D850` |
| fixture manifest | `5F79E8DC3EBAD4A9BA8C32C7092CDF52307220D08EF1D83EFD399B12B00B7AB1` |
| closure reproducer | `5F0FB64D1BB6DA17804088260FCA94A92F21DD4C2F5FAC1A9605F9F3BAD303DB` |
| oracle reproducer | `0A0EA8607D2E07E6189ACC52B698E781CF742C6523C4D46FF3F02330AF1B779B` |
| frozen live report | `FC25C0E04D44ACCC0F5232B4F852056B870D82059F7542D4307EC966C0EB9300` |

153 個 manifest 路徑的 `path | length | LastWriteTimeUtc ticks | SHA-256` 合成快照在審查中段與末段皆為：

`F30D12A52CAA17C0624CAA5F130D414ABDD3905E99CDF89C969B897A9580F352`

因此這 153 個 frozen paths 的 hash、length、mtime 均無變化；mismatch 始終為 0。所有 Python 執行均設 `PYTHONDONTWRITEBYTECODE=1`，實驗輸出只寫入 AI-3 `work/`。

前代亦唯讀重核：v0.2.3 `121/121`、manifest `7AAFA471...C817`；v0.2.2 `98/98`、manifest `AB63A7D...8EC0B`，均 0 mismatch。

## 3. CLOSURE-JUDGMENT-COMPLETENESS-01

### 3.1 Frozen facts

closure spec 的 `normative_precedence` 明定：`judgments` object 是 envelope classification 的 normative source；prose summaries 與 executable fixtures 是 derived views。

但 `judgments` 只有：

- `GenericEdgeShape`
- `SupportedEnvelopeHeader`
- `SupportedEdgeRelation`
- `UnsupportedEnvelope`

其中：

- `SupportedEnvelopeHeader.applicable_when` 引用 `GenericEnvelopeShape holds`；
- `UnsupportedEnvelope.predicate` 亦引用 `GenericEnvelopeShape holds`；
- `judgments.GenericEnvelopeShape` 不存在；
- required `spec_id/artifact_type/version/edges`、非空 string 與 edge-list 條件只出現在 `judgments` 外的 `base_envelope_shape` prose-like object；
- spec 沒有明文定義 `judgments.GenericEnvelopeShape := base_envelope_shape`，也沒有 normative `¬GenericEnvelopeShape → Malformed/FAIL` 或 `OpaqueLeaf` judgment。

AI-3 symbolic dependency probe：

```text
generic_envelope_judgment_present = false
generic_envelope_reference_closed = false
```

### 3.2 Classification

存在兩個合理讀法：

1. 把外層 `base_envelope_shape` 隱含提升為 `GenericEnvelopeShape` 定義，則 executable 的 malformed→FAIL、complete unsupported→UNKNOWN 成立；
2. 依 `normative_precedence` 採嚴格 judgments-only 讀法，則兩個 normative judgment 的前件未定義，formal classification 不完備。

因此 frozen Definition/interface 沒有唯一且依賴閉合的形式判定。這是 promotion blocker，但不是 code regression 或錯誤接受。

### 3.3 保留的正向證據

- 19 個 closure manifest cases + 1 supported control，共 20/20 符合 executable 結果；
- bundled scope checks 7/7，unexpected `[]`；
- `GenericEdgeShape` 明示不要求 current relation；
- `SupportedEdgeRelation` 僅在 supported header 成立時適用；
- complete shape-valid unsupported envelope 為 `UNKNOWN` 且不 traverse；
- malformed unsupported envelope 為 `FAIL`；
- FAIL 與 UNKNOWN 均阻止 admission。

這些證據封閉 executable behavior，不補上 normative graph 中缺失的 symbol definition。

### 3.4 Minimum successor fix

- 新增 `judgments.GenericEnvelopeShape`，精確列出 required exact members、types、nonempty constraints、edge-list 與 `GenericEdgeShape` 量詞；
- 新增 `¬GenericEnvelopeShape → Malformed/FAIL`；另以 `OpaqueLeaf` 定義沒有 `artifact_envelope` 的 leaf；
- 所有 judgment reference 使用 fully-qualified symbol；
- 新增 symbolic dependency-closure regression，拒絕 undefined judgment reference；
- 保留 v0.2.4 的 20+7 executable regressions。

## 4. ADVICE-DECL-LEDGER-01

### 4.1 Frozen interface facts

- schema 把 `mechanism.admissibility.advice` 列為 required，型別僅為任意 string；
- 它位於 `admissibility`，沒有 `annotation`、`display-only` 或 `nonnormative` 標記；
- candidate projection 包含除 `validation_receipt` 外的全部 root fields，所以此 declaration 被 projection/trace signature 綁定；
- Phase 0 介面把 advice、generator、generation、answer access 與 resource account 視為實質 admission 義務；
- validator 的 uniformity、advice-generation applicability/status、advice budget、answer access、resource derivation與 operational reference map都不讀這個 `advice` string。

AI-3 將 legitimate `parity-stream` record 的此欄改為 `one truth table per n`，得到下列靜態／局部 derivation 結果：

```text
SchemaConsistency                         = true
candidate projection hash changes        = true
uniformity status remains                 = pass
advice-generation status remains          = not-applicable
advice-budget status remains               = pass
resource-budget status remains             = pass
actual/expected operational maps unchanged = true
actual family oracle remains               = pass
```

同時 record 仍宣告／記錄：

```text
uniform = true
program_quantifiers = exists-one-program-for-all-input-lengths
advice_generator_ref = null
declared/observed answer access = none
ledger advice bytes = 0
generated_tables bytes = 0
advice generation peak output = 0
```

### 4.2 Valid-signature Counterexample

AI-1 與 AI-2 在隔離副本以既有 non-production fixture key 獨立重現：同步 candidate projection、trace、operational map並有效重簽後，signature/closure/actual family oracle 均 `pass`，而 structural/semantic/admission/final/record_accepted 全為 true，issues `[]`。

AI-1 corroborating artifact：

- addendum SHA-256 `4F9FD695377D6B891C6B7D62B86F2F81D82FCD15DC3AABAE067820B58EDA2D8B`
- reproducer SHA-256 `5948DD3EC0FC68F92A79D7028D985A12C1FCD9C4AF9E667E941CF1A4DC56BF7C`

### 4.3 Classification

這是 **Counterexample to accepted-record declaration/ledger consistency**。簽章只證明 declaration 被綁定，不證明它和 generator、uniformity、answer access、ledger 或 gate derivation一致。

它不是：

- 實際執行 truth table；
- 未入帳的 advice/resource hiding；
- signature、closure 或 correctness bypass；
- production signer authority 證明；
- P/NP 結論。

若 `advice` 原意只是顯示文字，frozen interface 必須明示其 nonnormative 身分；目前不能默認。

### 4.4 Minimum successor fix

- 以 typed `advice_mode` 取代或補強自由字串，例如 `none | per-length-truth-table | ...`；顯示文字另置明確 nonnormative 欄位；
- 定義 `ExpectedAdviceDecl(family, mechanism)`；
- exact bind `advice_mode`、mechanism id、uniform/program quantifiers、advice-generator ref、declared/observed access、ledger advice/generated-table bytes、generation account 與 gates；
- 加雙向 valid-signature fixtures：宣告 table 但 ledger/generator 為 none，以及宣告 none 但 ledger/generator 非零，均須拒絕。

## 5. Targeted fixes that passed

### 5.1 ExpectedOracleDecl

`_expected_oracle_declaration(family, mechanism, resultStatus)` 在四個 supported I0 contexts 上都有唯一值：PARITY stream、PARITY table family、2-SAT sat、2-SAT unsat；unsupported context 回傳 `None`。每個 supported declaration 都精確包含：

`oracle_id / entrypoint / name / checks / obligations`

schema 另要求 typed `oracle_id/entrypoint/obligations` 並禁止額外 oracle properties。SemanticValidate 對五欄 exact compare。

- 9 個 valid-signature cross-family/status/field-only negatives：SchemaConsistency=true，但 SemanticValidate=false、derived admission=false、final=false、accepted=false；均有 `oracle-declaration-family-binding`；actual family oracle仍 `pass`。
- `legit`、`2sat-sat`、`2sat-unsat` 三個 controls 全接受。

因此 ORACLE-DECL-FAMILY-01 在 bounded executable interface 內 CLOSED/PASS。這是 executable Definition/Experiment，不是一般 oracle soundness theorem。

非阻塞文件 hardening：函式 docstring 仍只寫 `name/checks`，後繼可更新為五欄；函式內容、CURRENT 與 SCHEMA-DIFF 的五欄語義本身唯一。

### 5.2 GateVal/applicability matrix

四值 `pass | fail | unknown | not-applicable` 保持一致；`fail` 與 `unknown` 都 fail closed。

| run × resource | run nonempty | maximal | fairness | account complete | budget |
|---|---:|---:|---:|---:|---:|
| standard × bounded | pass | N/A | N/A | pass | pass |
| standard × neutral | pass | N/A | N/A | pass | N/A |
| robust × bounded | pass | pass | pass | pass | pass |
| robust × neutral | pass | pass | pass | pass | N/A |

- 四象限 × 18 gates × assignment/admission 兩方向，共 144 mutations；schema escapes = 0。
- 12 條 AdmissionPass/FinalCompletion 必要蘊含 mutation 全被 schema 拒絕，包括 account completeness、applicable gates、oracle/contract/complete、兩處 debt、candidate final status，以及 bounded budget gate/correctness。
- resource-neutral 只免 budget threshold，不免完整 resource account。

### 5.3 Scoped robust semantics

robust 結果只適用 pinned finite deterministic I0 singleton：

```text
terminal + transition PASS  -> nonempty/maximal/fair = pass/pass/pass
transition FAIL             -> fail/fail/fail
transition UNKNOWN          -> unknown/unknown/unknown
nonterminal replay          -> fail/fail/fail
```

fairness/maximality artifacts明示此 bounded singleton scope；這不是任意 scheduler/fault policy 的 theorem。

## 6. Executable evidence

環境：CPython 3.14.5；jsonschema 4.26.0；cryptography 49.0.0；Windows 10.0.19045。

- 五代 unit suites：14 + 11 + 15 + 16 + 19 = **75/75 PASS**。
- closure reproducer：20 classifications + 7 scope checks，unexpected `[]`。
- oracle reproducer：9/9 negatives拒絕；3/3 controls接受。
- 42 fixture reports逐欄比對：0 mismatch；6 positives accepted。
- AI-3 independent audit：144 gate mutations，0 escape；12 implication mutations全拒；兩層 SchemaConsistency/SemanticValidate 分離符合。
- live experiment以同 seed重跑；與 frozen report只有 38 個 `*_time_ns` leaves 不同。刪除這些 timing fields後，雙方 canonical projection SHA-256 同為：

`092C653797876D1A56099B78FD4190C4DB5E4B32E39988ED74EFB40C0259202A`

AI-3 audit script SHA-256：`D34A701C22BB4B312ACB8360673554E8CB9CD0E74DD65EE95736B252C7F749A0`。

## 7. Scope qualification

AI-3 沒把 137/137 fixture/artifact regeneration 當成自身獨立證據：generator 需要外部 `--signing-key`，而 frozen candidate刻意不發布 private key。另在只複製 versioned manifest unions的隔離重產中，generator chain 還會引用未列入這些 manifests 的共用 `scripts/generate_fixtures.py` 與基礎 source modules；完整 shared-root + external test key 的重產觀察可成立，但 153-path freeze set 本身不是 standalone signing/regeneration bundle。這是 reproducibility scope qualification，不改變本報告兩個 blocker 的分類。

審查沒有一般 validator soundness/completeness、production measurement authority、任意 robustness、3-SAT/CDCL 或 P/NP 主張。
