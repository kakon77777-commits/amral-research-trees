# AI-3 I0 v0.2.3 形式／接口唯讀驗收

- 審查者：AI-3 / Codex-GLC-Formalizer
- 日期：2026-08-09（Asia/Taipei）
- 候選狀態：`CANDIDATE_UNPROMOTED`
- 整體 disposition：**FAIL / CLOSURE-EDGE-SCOPE-01**
- v0.2.2 blocker：**CLOSURE-CLASS-01 executable CLOSED**
- 性質：Definition/interface scope ambiguity；不是 acceptance bypass、不是 executable regression、不是 P/NP 結論
- 操作邊界：只讀 frozen v0.2.3 manifest path set；未修改 candidate root、未發 Board success、未改 shared repo

## 1. 結論

v0.2.3 的 generic `EnvelopeShape` 實作正確前移到 supported/unsupported `spec_id` 分派之前。16 個 classification artifacts 與 1 個 supported control 全部符合 executable oracle；原 v0.2.2 最小反例在 v0.2.3 由 `UNKNOWN` 修正為 `FAIL`。四值 gate matrix、Admission/Final 必要蘊含、SchemaConsistency/SemanticValidate 分離及 bounded robust singleton scope 亦全部通過本次檢查。

但 frozen `artifact-closure-spec.v0.2.3.json` 的 `edge_shape.expected_type` 無條件寫成：

```text
must equal the pinned parent-type/role relation
```

同一 frozen spec 又要求 generic EnvelopeShape 在 spec-id dispatch 前執行；CURRENT、SCHEMA-DIFF、source docstring 與 positive fixture 則明定 parent-role-child relation 只在 supported traverse 檢查。對一個 unsupported future artifact 的非空 edge，前句若屬 generic shape，應為 `FAIL`／未定義；若只屬 supported semantics，則為 `UNKNOWN`。候選沒有提供規範優先序或明確 scope，故 pinned Definition-interface artifact 不能唯一決定 judgment。

兩種狀態都阻止 admission，所以沒有錯誤接受；但 `FAIL` 與 `UNKNOWN` 的 epistemic meaning 不同，形式接口仍不唯一，足以阻止 promotion。修文必須另起版本，不能改 frozen v0.2.3 bytes。

## 2. Exact-byte identity

- manifest：`SHA256SUMS-v0.2.3-candidate.txt`
- manifest SHA256：`7AAFA47149AD3BCA042A62FC8C708D61D5AD41A7ACF7F4F4A897318F0063C817`
- entries：121；審查前後均 121/121 exact，0 missing／mismatch
- schema：`DCE6F0C95B95D9377BA7AF9F9537BDC277CDF0E68CE74B9AD3BF83DB2B011895`
- validator：`B0DC4EC989F93EBD557C4C8BFA3004E33B2BBAE0EB0F8FA5622489B2D148097B`
- closure spec：`4E978EF2A2DF0FED51E94E89E6305294A9B7965AD86AB6888EE857DA4854643B`
- role spec：`FB5C3BE06BA68716492B96664BF8FD5C6154C1159025E5F1D278FAD1C0B3CBFB`
- run fixture manifest：`189967B7F60968BE2ACED2A0B4EE5E8885FBBFD997916BA18F55B33F3A4AA5D1`
- closure fixture manifest：`46721DBE2E8A5E4CE1144DA2957C7688059637149DDDADFF766B517001C6DE06`
- reproducer：`90AAECDD4214AC188A35F1DBF4894819CFE727C0D9E63A1A39E0D574335806F2`
- frozen live report：`7D32357291B59DE472A266BAAD63F7BBB469B60F58BCD727DF5D3A35899125EB`
- predecessor v0.2.2 manifest：`AB63A7D921F04E71BDFC8CCA0F681E81E9A1BA2AAAC89E1674A6D0C883A8EC0B`

## 3. Formal-interface dispositions

| 項目 | 結果 | 限定 |
|---|---|---|
| Generic EnvelopeShape before dispatch | PASS | required `spec_id/artifact_type/version/edges`、nonempty strings、generic edge exact keys、nonempty role/type、valid SHA-256、per-parent role uniqueness 皆先驗。 |
| Leaf → Malformed/FAIL → Unsupported/UNKNOWN → supported Traverse | PASS（executable） | 16/16 artifact cases + supported control PASS；兩個 valid-signature end-to-end records 均拒絕。 |
| `edge_shape.expected_type` scope | **FAIL** | frozen Definition 沒有寫 `Supported(spec_id) → RelationConform`，可合理得到兩種不同 status。 |
| 四值 GateVal／GateAssignmentConformant | PASS | `pass|fail|unknown|not-applicable`；四象限、兩方向共 144 mutations，0 schema escape。 |
| Admission／Final／account／budget implications | PASS | 十二個必要條件變形均 schema-rejected；account always applicable，budget iff bounded。 |
| SchemaConsistency vs SemanticValidate | PASS | 兩個 classification records 均 schema-valid，但 external semantic validation false，accepted false；schema 沒有冒充 evidence validator。 |
| robust semantics | PASS（scoped） | 只涵蓋 pinned finite deterministic singleton I0 run；不含 scheduler/fault nondeterminism。 |
| REF-TYPE／PROV-DERIVE／oracle／resource semantics | PASS（regression scope） | validator diff 顯示除版本 pins 外，唯一功能變更是 EnvelopeShape；既有 regression tests 全過。不是 soundness/completeness theorem。 |

## 4. CLOSURE-EDGE-SCOPE-01 witness

Frozen witness：

```text
artifacts-v0.2.3/closure-classification/shape-valid-unsupported-future-type.json
```

其 envelope 為：

```json
{
  "spec_id": "urn:unsupported:closure:9",
  "artifact_type": "future-artifact",
  "version": "9.0.0",
  "edges": [
    {
      "role": "future-edge",
      "expected_type": "opaque-content",
      "sha256": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
    }
  ]
}
```

觀察：

```text
GenericEnvelopeShape(e)                 = true
SupportedSpecId(e)                      = false
EDGE_RELATIONS.get("future-artifact")   = none
LiteralPinnedRelationConform(edge)       = false / undefined
validator classification                = UNKNOWN
fixture expected                         = UNKNOWN
```

兩個合理形式化：

```text
Reading A — edge_shape is part of GenericEnvelopeShape:
  GenericEnvelopeShape(e) requires RelationConform(e)
  relation is undefined for future-artifact
  => Malformed/FAIL (or the Definition itself is partial)

Reading B — relation is a supported-spec semantic obligation:
  GenericEnvelopeShape(e) checks syntax/hash/uniqueness only
  GenericEnvelopeShape(e) ∧ ¬SupportedSpecId(e)
  => Unsupported/UNKNOWN
```

CURRENT、SCHEMA-DIFF、source docstring、fixture manifest 與 executable 都選 Reading B；但 `artifact-closure-spec` 自己是被 pin 的 `Definition-interface-candidate`，其 `edge_shape.expected_type` 沒有 scope 條件，也沒有文件優先序聲明。Experiment fixture 與 implementation 可以顯示 intended behavior，不能消除 Definition byte 本身的量詞歧義。

分類：**Ill-scoped Definition / formal-interface blocker**。它不是對 `_artifact_closure` executable 的 counterexample。

## 5. Successor 的最小修訂義務

後繼版本應把兩層拆成獨立 normative predicates：

```text
GenericEdgeShape(edge) :=
  exact keys {role, expected_type, sha256}
  ∧ NonemptyString(role)
  ∧ NonemptyString(expected_type)
  ∧ ValidSha256(sha256).

GenericEnvelopeShape(envelope) :=
  required/nonempty spec_id, artifact_type, version
  ∧ List(edges)
  ∧ ∀edge∈edges. GenericEdgeShape(edge)
  ∧ UniqueRole(edges).

SupportedEdgeRelation(envelope) :=
  SupportedSpecId(envelope.spec_id) →
    ∀edge∈edges.
      EDGE_RELATIONS[envelope.artifact_type][edge.role]
        = edge.expected_type.
```

並明定 judgment precedence：

```text
no envelope                         => Leaf
¬GenericEnvelopeShape               => FAIL
GenericEnvelopeShape ∧ unsupported  => UNKNOWN
supported ∧ bad version/type/relation => FAIL
supported ∧ all checks              => Traverse
```

可保留現有 executable 與全部 v0.2.3 regressions；只需將 spec 的 scope／precedence 寫成新版本 exact bytes，更新 pins 後重新 freeze。v0.2.3 不應原地修改。

## 6. Gate 與兩層 validation

在 18-gate 域內：

```text
GateAssignmentConformant(r) :=
  ∀g. Applicable(r,g)  → Gate(r,g) ∈ {pass,fail,unknown}
    ∧ ¬Applicable(r,g) → Gate(r,g) = notApplicable.
```

| run × resource | run nonempty | maximal/fair | account completeness | budget |
|---|---:|---:|---:|---:|
| standard × neutral | applicable | N/A | applicable | N/A |
| standard × bounded | applicable | N/A | applicable | applicable |
| robust × neutral | applicable | applicable | applicable | N/A |
| robust × bounded | applicable | applicable | applicable | applicable |

`unknown` 與 `fail` 均阻止 admission。必要蘊含式仍為：

```text
AdmissionPass(r) →
  GateAssignmentConformant(r)
  ∧ ∀g (Applicable(r,g) → Gate(r,g)=pass)
  ∧ ResourceAccountComplete(r)
  ∧ RunSpecsConform(r).

FinalCompletion(r) →
  AdmissionPass(r)
  ∧ OraclePass(r) ∧ ContractPass(r) ∧ CompletePass(r)
  ∧ ResourceAccountPass(r)
  ∧ ReceiptLossDebt(r)=0 ∧ LedgerLossDebt(r)=0
  ∧ CandidateStatus(r)∈{sat,unsat,complete}
  ∧ (ResourceBounded(r) →
       ResourceBudgetGate(r)=pass ∧ CorrectnessBudget(r)=pass).
```

兩層 judgment 必須分開：

```text
SchemaConsistency(record)
  := transport fields/types/conditional implications are internally consistent.

SemanticValidate(evidenceSnapshot, record)
  := exact-byte evidence resolution, typed closure, signature/map binding,
     transition replay, resource derivation, oracle/contract and loss-debt facts hold.

RecordAccepted(record,evidence)
  := SchemaConsistency(record)
     ∧ SemanticValidate(evidence,record)
     ∧ DerivedAdmissionPass(record,evidence).
```

`malformed-unsupported-envelope` 與 `shape-valid-unsupported-envelope` 的 schema consistency 均為 true；semantic validation 與 acceptance 均為 false，正確展示兩層不可互相取代。

## 7. Dynamic evidence

- tests：14/14 + 11/11 + 15/15 + 16/16 PASS
- executable closure reproducer：17/17，`unexpected=[]`
- run fixtures：33，manifest mismatch 0
- independent closure matrix：16 cases，mismatch 0
- independent gate matrix：4 quadrants × 18 gates × 2 mutation directions = 144，escape 0
- Admission/Final/account/budget implication probes：12/12 fail closed
- robust scoped probe：terminal pinned replay=`(pass,pass,pass)`；failed transition與 nonterminal 均 `(fail,fail,fail)`
- v0.2.3 validator 沒有 public mapping-plus-claimed-hash `validate_record`；錯 schema bytes 先得到 `schema-byte-pin-mismatch`
- frozen live report 重新執行時，raw bytes 因實測 `*_time_ns` 不同而不同，符合 frozen docs 的 nonclaim；JSON normalization 後排除 timing fields，semantic projection exact-equal：
  - frozen projection SHA256：`8C880B494D87651A254E900C0208C8CFF6515C17BB8917076B601E361894E13B`
  - live projection SHA256：`8C880B494D87651A254E900C0208C8CFF6515C17BB8917076B601E361894E13B`

## 8. Scope與 nonclaims

- 本驗收只涵蓋 explicit v0.2.3 modules、artifacts、schemas、fixtures 與 manifest paths；default package metadata／CLI 仍是 v0.2.0。
- CLOSURE-CLASS-01 的 executable closure 是 scoped positive evidence，不是一般 artifact-graph soundness/completeness proof。
- robust 僅為 pinned finite deterministic singleton I0；fairness/maximality 沒有推廣到一般 scheduler/fault runs。
- 本報告不採納四層大箭頭，不主張 P=NP 或 P≠NP，不授權 Board success、shared repo promotion 或其他外部狀態變更。
