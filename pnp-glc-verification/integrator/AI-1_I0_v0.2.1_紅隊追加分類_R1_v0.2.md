# AI-1｜I0 v0.2.1 紅隊追加分類 R1

| 欄位 | 值 |
|---|---|
| 文件版本 | v0.2（2026-08-09，Asia/Taipei） |
| 修訂對象 | `AI-1_I0_v0.2.1_紅隊追加整合_ADDENDUM_v0.1.md` 的 3.1／3.2 分類 |
| Overall disposition | 不變：**FAIL / REF-TYPE-01** |
| 來源 | AI-3 formal consistency disposition + AI-1 package/CLI inspection |

## 1. `SCHEMA-BIND-API-01` 精確分類

目前實際 package metadata、`__init__`、console scripts 與 CLI 均仍是 v0.2.0；CLI validate path 匯入 frozen v0.2 `semantic_validator.validate_path`。v0.2.1 experiment 同樣只呼叫 `semantic_validator_v021.validate_path`。`validate_record` 沒有在 package root export，也沒有被文件列為 supported trust-boundary API。

因此：

- 對 frozen v0.2.1 已明示的 path interface：`SCHEMA-BIND-API-01` 是 **conditional interface blocker／hardening obligation**，不是第二個 unconditional promotion blocker；
- 若 successor 對外暴露、內部改用、或以 theorem/soundness claim 量化 `validate_record(record, schemaMapping, claimedHash)`：它立即成為 blocker，除非帶有明確 `SchemaBound` 前提。

優先介面：

```text
SchemaSnapshot := {
  rawBytes,
  parsedSchema,
  digest,
  parse_ok,
  digest_eq
}

ValidateBytes(recordBytes, schemaBytes, artifactSnapshot)
```

`parsedSchema` 與 `digest` 必須在 validator 內由同一 `rawBytes` 導出。替代方案是把 mapping+claimed-hash helper 改成 private，並把 `SchemaBound(schema,h)` 明列為 untrusted-caller precondition。

## 2. `CANON-NEGZERO-01` 精確分類

目前 spec 將「negative zero forbidden」放在 `canonical_serialization` 區塊，但沒有明確區分：

```text
RawParseDomain(raw JSON tokens)
CanonicalEncodeDomain(parsed semantic values)
```

因此 raw `-0` 有兩種可採定義：

1. 若 RawParseDomain 禁止 `-0`：目前接受行為是 canonical-conformance failure，必須以 strict `parse_int`／tokenizer 拒絕。
2. 若規則只要求 CanonicalEncodeDomain 永不輸出 `-0`：`parse(-0)=0; encode(0)=0` 可視為與 `\n`／`\u000a` 類似的合法 normalization，現行行為不構成 semantic admission unsoundness。

v0.2.2 的 mandatory obligation 是 **先選定並明寫 domain**，再讓 parser、projection spec與測試一致；不再無條件把 strict raw rejection當作唯一合法答案。

## 3. Closure classification order

`EnvelopeClass` 應固定判定順序：

```text
no artifact_envelope
  -> Leaf

envelope exists but required member missing/ill-typed
  -> Malformed / FAIL

shape-valid but spec_id unsupported
  -> Unsupported / UNKNOWN

supported and valid
  -> Traverse role-bearing edges
```

這修正 `CLOSURE-CLASS-01` 的 fail/unknown status mismatch；兩種 status 目前都 block admission，所以不是 acceptance bypass。

## 4. Formal trust-boundary obligation

後續 soundness statement 應以 bytes/snapshots 為量化對象：

```text
ValidateBytes(recordBytes, schemaBytes, artifactSnapshot)
```

所有 parsed objects、canonical projections與 hashes 均由上述 snapshots 內部導出。若保留 mapping-level helper，任何 theorem 都必須以 `SchemaBound`／`RecordBound` 為顯式 premise。

## 5. Disposition

| Finding | Revised classification |
|---|---|
| `REF-TYPE-01` | Counterexample／unconditional v0.2.1 promotion blocker |
| `SCHEMA-BIND-API-01` | Conditional interface blocker；exposure/use/soundness claim 時適用 |
| `CANON-NEGZERO-01` | Definition ambiguity／conditional canonical-conformance failure |
| `CLOSURE-CLASS-01` | Fail-closed status mismatch |
| surrogate | Fail-closed hardening |

原驗收 FAIL、frozen hashes、scoped positive evidence、Board/repository deferred 與無 P/NP 結論均不變。
