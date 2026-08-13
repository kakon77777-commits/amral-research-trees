# Schema／validator diff：v0.2.1 → v0.2.2 candidate

分類：Definition/interface candidate + Experiment；不是 theorem adoption。

## 保留

- v0.2.1 schema 與 validator 完全不覆寫。
- 四值 gate：`pass | fail | unknown | not-applicable`。
- run-class-nonempty 與 resource-account 永遠 applicable；budget iff resource-bounded；maximality/fairness iff robust。
- schema 驗形狀與可見欄位蘊含；external validator 才解析 evidence、replay、judge 與導出 aggregate postconditions。

## Schema 新增／收緊

- receipt 新增必填 `evidence_role_spec_ref` 與 `operational_reference_map_sha256`。
- always-applicable gates 改用不含 `not-applicable` 的 `applicableGateStatus`。
- advice-generation 與 proof-verification 的 applicable/N/A 不再只在 admission=true 時檢查；現在對所有 records conditionally conformant。
- standard/robust、resource-neutral/resource-bounded、admission/final implications 維持單向；all constituent gates pass 不反向強迫 aggregate true。

## External validator 新增／收緊

- `validate_record(record, schema, claimed_hash)` 不再是 public API；支援入口只接受 exact record/schema bytes 或 paths，內部產生 SchemaSnapshot。
- strict raw JSON parser 拒絕 duplicate keys、non-finite numbers 與 exact integer token `-0`。
- candidate canonical domain 顯式拒絕 unpaired surrogate，保留 NFC/integer-only 規則。
- direct operational role map 在 validator 內由 family/mode/mechanism/event/certificate 結構唯一導出。
- signed trace 必須包含完全相同的 canonical operational map；receipt map hash 由 validator 重算。
- closure 先驗 envelope required members，再區分 malformed 與 unsupported spec。
- typed wrapper content 驗 id/version/mode/family；robust run 解析 maximal/fairness；sandbox 解析 producer/measurement/budget；contract 與 invariant 綁 family/mechanism。
- builder/run/proof/advice/resource/budget gates 不再採信 trace Boolean：可執行者實際執行，可折疊者重算，raw measurement 只在 authenticated trace 下採入。
- problem size、failure-frontier axes、declared/observed answer access 亦由 validator 導出或核對。

## 明確邊界

- Ed25519 key 是 test-fixture authenticity，不是 production measurement authority。
- raw peak-space／precision 等不能由事件純推導的量，由 signed sandbox measurement receipt 支撐；producer 字串本身不是 authenticity。
- I0 executable semantics 只支援 PARITY streaming/table-family 與 deterministic 2-SAT；其他 family/mechanism 回 `unknown` 或 fail closed。
- 這些結果不外推 general SAT、P=NP 或 P≠NP。

