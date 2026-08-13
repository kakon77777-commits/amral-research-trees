# Schema／validator diff：v0.2.2 → v0.2.3 candidate

分類：Definition/interface candidate + Experiment；不是 theorem adoption。

## Transport schema

v0.2.3 schema 從 frozen v0.2.2 schema 作純版本化轉換，保留：

- 四值 gate 與 GateAssignmentConformant；
- standard/robust、resource-neutral/resource-bounded applicability matrix；
- admission/final 的單向 fail-closed implications；
- candidate-result 與 external validation receipt 分離；
- projection、trace、schema、validator、closure、role、evidence hash bindings；
- resource account 永遠適用、budget 只在 bounded 適用。

artifact bytes 不位於 run-record transport schema 內，因此 `CLOSURE-CLASS-01` 不以 record schema conditional 修補；它由 pinned external validator 與 versioned closure spec 封閉。schema 仍只負責 record 形狀與可表達的跨欄一致性。

## External validator

相對 v0.2.2，將 `_artifact_closure` 的共同形狀判定抽成 `_envelope_shape`，並把它放在 supported/unsupported `spec_id` 分流之前。除版本與 pinned artifact hashes 外，validator 的其他執行語義保持不變。

通用 EnvelopeShape 規則：

- required：`spec_id`、`artifact_type`、`version`、`edges`；
- 三個字串欄均非空，`edges` 為 list；
- edge 精確欄位為 `role`、`expected_type`、`sha256`；
- edge role/type 非空、同一 parent 中 role 唯一、SHA-256 格式有效。

分類順序：Leaf → Malformed/FAIL → Unsupported/UNKNOWN → supported Traverse。只有 supported spec 才檢查目前已知 artifact type、version 與 parent-role-child relation。

## 新增負例面

- unsupported + missing：spec-id、artifact-type、version、edges；
- unsupported + ill-typed：四個 required members；
- empty string：spec-id、artifact-type、version；
- malformed generic edge：缺成員、錯誤 hash、重複 role；
- positive unsupported controls：known-type 與 future-type，兩者皆完整 shape → UNKNOWN；
- supported run-standard control → PASS；
- valid-signature run-record：malformed unsupported 與 shape-valid unsupported 均不得 admission。

## 未變的失敗前沿

I0 只執行 pinned PARITY streaming/table-family 與 deterministic 2-SAT。一般 3-SAT/CDCL、任意 scheduler/fault nondeterminism、production measurement authority 與完整 validator soundness proof 均不在本候選主張內。成功或失敗不得外推 P=NP 或 P≠NP。
