# Schema／validator／closure-spec diff：v0.2.3 → v0.2.4

分類：Definition/interface candidate + Experiment；不是 theorem adoption。

## Transport schema

v0.2.4 schema 從 frozen v0.2.3 版本化，並在 `mechanism.oracle` 新增 required typed `oracle_id`、`entrypoint` 與義務集合 `obligations`；其餘 gate applicability、AdmissionPass、FinalCompletion、resource-account／budget、candidate/receipt 分離與 conditionals均不變。

artifact bytes 不在 run-record transport schema 內，因此本輪修補位於 versioned closure spec，不以 record schema 偽裝封閉。

## External validator

validator 保留 v0.2.3 closure ordering及其他執行語義，新增 `ExpectedOracleDecl(family, mechanism, resultStatus)`；SemanticValidate exact 比對 `oracle_id/entrypoint/name/checks/obligations`。實際 correctness oracle仍由 problem family選擇，宣告不符是獨立 provenance failure。

## Normative closure spec

移除 v0.2.3 無適用域的 `edge_shape.expected_type = must equal pinned parent-type/role relation`，改成四個明確 judgment：

- `GenericEdgeShape(e)`：所有 envelope、spec-id dispatch 前；只驗 generic syntax/hash/role uniqueness。
- `SupportedEnvelopeHeader(e)`：generic shape + current spec-id；再驗 current version 與 artifact-type domain。
- `SupportedEdgeRelation(e)`：適用若且唯若 SupportedEnvelopeHeader holds；再驗 parent-role-child relation。
- `UnsupportedEnvelope(e)`：generic shape + unsupported spec-id；結果 UNKNOWN、不 traverse、relation 不適用。

`normative_precedence` 明定 closure artifact 的 `judgments` 是分類依據，prose summary 與 executable fixtures 是衍生視圖。

## 新增對照面

- unsupported future-type + nonempty future-edge → UNKNOWN；
- supported spec-id + wrong version → FAIL；
- supported spec-id + future artifact type → FAIL；
- supported run-spec + generic-valid but relation-invalid edge → FAIL；
- 原 14 malformed、2 unsupported、1 supported control 全部保留。
- PARITY↔2-SAT、2-SAT SAT↔UNSAT 的完整 oracle declaration swaps → FAIL；
- oracle-id、entrypoint、name、checks、obligations 各自單欄 swap → FAIL；
- 上述 oracle negatives 保持 valid signature 且 actual family oracle PASS，證明測的是 declaration binding，不是 correctness bypass。

## 適用域與失敗前沿

這只封閉目前 artifact-envelope interface 的量詞。I0 仍只執行 pinned PARITY 與 deterministic 2-SAT；一般 3-SAT/CDCL、任意 scheduler/fault nondeterminism、production measurement authority與完整 validator proof不在主張內。不得外推 P=NP 或 P≠NP。
