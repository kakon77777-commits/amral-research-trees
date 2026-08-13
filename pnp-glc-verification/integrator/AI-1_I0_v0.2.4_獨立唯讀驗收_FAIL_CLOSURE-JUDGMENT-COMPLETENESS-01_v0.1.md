# AI-1 I0 v0.2.4 獨立唯讀驗收

## Disposition

- 整體：`FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01`
- `CLOSURE-CLASS-01`：`CLOSED / PASS`
- `CLOSURE-EDGE-SCOPE-01` 的 targeted executable/scope fix：`CLOSED / PASS`
- `ORACLE-DECL-FAMILY-01` 的 targeted executable/semantic fix：`CLOSED / PASS`
- 候選狀態：維持 `CANDIDATE_UNPROMOTED`
- 分類：Definition/interface promotion blocker；不是 admission bypass、correctness failure 或 P/NP 結論。

## Frozen identity 與唯讀邊界

- candidate root：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-engineering\outputs\pnp-glc-i0`
- manifest：`SHA256SUMS-v0.2.4-candidate.txt`
- manifest SHA-256：`73ED3607EAD3F50502DCEFA3142DFFEE01AAC8576C045F05CA96DEB9669F77FE`
- entries：153；format / missing / mismatch / duplicate 均為 0。
- AI-1 隔離根：`C:\Users\kakon\Documents\Codex\2026-08-09\pnp-glc-integrator\work\v024-acceptance-ai1-20260809`
- 審查前後 153 個 candidate paths 的 SHA-256、length、mtime 均無變化；`candidate_root_writes=0`。
- 並行或後繼版本路徑未納入 v0.2.4 provenance domain。

核心 hashes 全部精確一致：

| Artifact | SHA-256 |
|---|---|
| schema | `16EBCC7DE4196D0C46FC9C309F2060F856E321C0012C5B775390C04234F9DCC8` |
| validator | `B744C9C20C510FE39F132E0DFB4AAC50E6E3E573B48B7F1AE19494F5D5195FED` |
| closure spec | `579B6F7DA8BE3712FE6130AD900CF0CBA189496100548CBF87655687A7690588` |
| evidence role spec | `4EFC4C71C6275227B14429E58FCECC4E949459918315D27CC476765C7D24D850` |
| fixture manifest | `5F79E8DC3EBAD4A9BA8C32C7092CDF52307220D08EF1D83EFD399B12B00B7AB1` |
| closure reproducer | `5F0FB64D1BB6DA17804088260FCA94A92F21DD4C2F5FAC1A9605F9F3BAD303DB` |
| oracle reproducer | `0A0EA8607D2E07E6189ACC52B698E781CF742C6523C4D46FF3F02330AF1B779B` |
| frozen live report | `FC25C0E04D44ACCC0F5232B4F852056B870D82059F7542D4307EC966C0EB9300` |

## Executable與資料一致性結果

環境：CPython 3.14.5、jsonschema 4.26.0、cryptography 49.0.0。

1. 五套 unittest：14/14 + 11/11 + 15/15 + 16/16 + 19/19，合計 75/75 PASS。
2. Closure classification：20/20；scope checks：7/7；`unexpected=[]`。
3. Oracle declaration：9/9 有效簽章 negative cases 均拒絕；3/3 controls 接受；所有 negative cases 的實際 family oracle 仍為 PASS，並出現 `oracle-declaration-family-binding`。
4. Fixture manifest：42/42，0 mismatch；六筆正向 record 被接受。
5. Schema、fixtures 與 artifacts 在隔離副本重產後，全部 153 manifest paths 仍 exact，0 mismatch；因此聲明的 137 個 deterministic fixture/artifact outputs 亦保持 byte-identical。
6. 新 live report 與 frozen report raw hash 因 `*_time_ns` 不同；移除 timing fields 後完全相同，兩者 normalized SHA-256 均為 `092C653797876D1A56099B78FD4190C4DB5E4B32E39988ED74EFB40C0259202A`。
7. 八種有效 fixture context × 18 gates = 144 個 applicability mutations，schema acceptance 為 0。
8. 前代 frozen manifests：v0.2.3 121/121 exact；v0.2.2 98/98 exact。
9. PROV-DERIVE、REF-TYPE、schema snapshot、raw `-0`、Unicode scalar、resource/context derivation及 gate matrix regressions均維持 fail closed。

以上證據支持兩個 v0.2.3 blocker 的實作修補；未發現錯誤 record acceptance。

## 新 blocker：CLOSURE-JUDGMENT-COMPLETENESS-01

Exact frozen closure spec 在 `normative_precedence` 明定：

> The judgments object in this artifact is normative for envelope classification. Prose summaries and executable fixtures are derived views.

但 `judgments` 只有：

- `GenericEdgeShape`
- `SupportedEnvelopeHeader`
- `SupportedEdgeRelation`
- `UnsupportedEnvelope`

其中兩個規範條款直接引用未在 `judgments` 定義的符號：

- `$.judgments.SupportedEnvelopeHeader.applicable_when`：`GenericEnvelopeShape holds ...`
- `$.judgments.UnsupportedEnvelope.predicate`：`GenericEnvelopeShape holds ...`

完整 envelope 的 required members、nonempty string、edges list 等條件只出現在 `judgments` 外的頂層 `base_envelope_shape` prose-like object。Frozen bytes 沒有明定該物件等同於 normative `judgments.GenericEnvelopeShape`；也沒有在 normative judgments 內給出 `GenericEnvelopeShape fails ⇒ Malformed/FAIL` 或 opaque-leaf classification。

因此有兩個合理形式讀法：

1. 將頂層 `base_envelope_shape` 隱式視為 `GenericEnvelopeShape` 定義，得到目前 executable 的 malformed→FAIL、complete unsupported→UNKNOWN。
2. 依 `normative_precedence` 採 judgments-only 讀法，則 `GenericEnvelopeShape` 是未定義前件，`SupportedEnvelopeHeader` 與 `UnsupportedEnvelope` 的 applicability 無法判定，classification relation 不完備。

現有 7 個 scope checks 只確認 `normative_precedence` 非空及 edge relation scope，沒有檢查 normative judgment symbol dependency closure。AI-1 exact-byte reproducer顯示：

- closure spec hash exact；
- `generic_envelope_shape_defined_in_judgments=false`；
- 兩個未閉合引用存在；
- `normative_dependency_closed=false`；
- executable controls 仍為 complete unsupported=`unknown`、malformed unsupported=`fail`。

故此 blocker 只阻止 formal/Definition-interface promotion；它不否定 executable regression，也不形成 admission bypass。

## 最低後繼修正義務

1. 在 normative `judgments` 內明確加入 `GenericEnvelopeShape`，完整定義 required members、extra-member policy、nonempty strings、edges list及 `∀ edge, GenericEdgeShape(edge)`。
2. 明定 `¬GenericEnvelopeShape ⇒ Malformed/FAIL`；若 closure spec 聲稱涵蓋完整分類，亦應定義沒有 envelope 的 `OpaqueLeaf` judgment。
3. 將所有前件寫成明確的 `judgments.GenericEnvelopeShape holds`，不依賴隱含的跨欄名稱映射。
4. 新增 symbolic judgment dependency-closure regression：每個 normative judgment reference 都必須解析到同一 normative namespace。
5. 保留 v0.2.4 的 20+7、9+3、75 tests、42 fixtures、144 gate mutations及 deterministic regeneration regressions；另起後繼版本，不覆寫 frozen v0.2.4。

## Scope與可攜性觀察

153-path manifest 是版本 identity set，不是獨立執行 bundle。隔離執行舊測試與 generator 仍需明確補入 parent root 的前代 manifests、runtime modules及 transitive legacy artifacts。首次 manifest-only 測試出現的 `SHA256SUMS-v0.2.1.txt` 缺件是 packaging/path portability observation；補入 frozen dependency 後 75/75 PASS，故未升格為另一個 semantic promotion blocker。

本驗收僅涵蓋 versioned v0.2.4 schema、validator、spec、fixtures與實驗介面；不宣稱 unversioned CLI 已切換，也不證明四層框架、P=NP 或 P≠NP。
