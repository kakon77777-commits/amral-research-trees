# AI-2 I0 v0.2.4 唯讀研究記錄一致性審查

## Disposition

**FAIL / CLOSURE-JUDGMENT-COMPLETENESS-01 + ADVICE-DECL-LEDGER-01**

本裁定只適用於 frozen I0 v0.2.4 research-record schema／validator／interface candidate。候選維持 `CANDIDATE_UNPROMOTED`。

## Frozen identity 與完成的計數

- v0.2.4 manifest：153/153 exact，0 format error、0 missing、0 mismatch、0 duplicate；manifest SHA-256：`73ED3607EAD3F50502DCEFA3142DFFEE01AAC8576C045F05CA96DEB9669F77FE`。
- predecessor snapshots：v0.2.3 為 121/121 exact；v0.2.2 為 98/98 exact。
- tests：14/14 + 11/11 + 15/15 + 16/16 + 19/19，合計 75/75 PASS。
- closure executable classifications：20/20；scope checks：7/7；unexpected：0。
- oracle declaration：9/9 valid-signature negative records rejected；3/3 positive controls accepted；negative records 的 actual family oracle 仍為 PASS。
- run-record fixtures：42，outcome mismatch：0；其中 6 個 positive records accepted。
- gate applicability：8 profiles × 18 gates = 144 mutations；schema acceptance：0。
- admission／final／resource-account／budget implications：12/12 rejected as required。
- deterministic fixture／artifact outputs：137/137 immediate regeneration byte-identical。
- frozen provenance domain：153 manifest paths 加 manifest 本身；before／after hash、length、mtime delta：0；`candidate_root_writes=0`。

## Blocker 1：CLOSURE-JUDGMENT-COMPLETENESS-01

### 類型

Definition／interface normative-dependency completeness blocker。不是 executable regression，也沒有 admission bypass。

### 最小差異

Frozen closure specification 的 `normative_precedence` 指定 `judgments` object 為 envelope classification 的規範來源；但 `judgments` 沒有定義 `GenericEnvelopeShape`，而 `SupportedEnvelopeHeader.applicable_when` 與 `UnsupportedEnvelope.predicate` 都直接引用它。完整 required-member／type constraints 位於 `judgments` 外的 `base_envelope_shape` prose-like object。

因此至少存在兩個合理讀法：把外層欄位隱含視為 `GenericEnvelopeShape` 的定義，或嚴格依 `judgments`-only precedence 而得到未封閉、不可判定的規範依賴。現有程式與 fixtures 採第一種讀法並 fail-closed；問題是 frozen Definition/interface 本身沒有唯一且完整的 formal judgment graph。

### 最低修正義務

在 `judgments` 內明確定義 `GenericEnvelopeShape`，補上 generic false → Malformed/FAIL 與 OpaqueLeaf 分類，使用 fully-qualified judgment references，並加入 symbolic dependency-closure regression。

## Blocker 2：ADVICE-DECL-LEDGER-01

### 類型

Accepted-record declaration／ledger consistency Counterexample。不是實際 truth-table resource hiding、correctness、signature 或 closure failure。

### 最小差異

以合法 PARITY record 為基底，只把 required、signed 的 `mechanism.admissibility.advice` 改為既有 truth-table fixture 的 `one truth table per n`。同一 record 仍宣告：

- `uniform=true`；
- `exists-one-program-for-all-input-lengths`；
- `advice_generator_ref=null`；
- declared／observed answer access 均為 `none`；
- advice 與 generated-table ledger bytes 均為 0；
- advice-generation time／space／output account 均為 0。

同步 candidate projection、trace、operational map，以既有 non-production Ed25519 fixture key 有效簽章並重算 closure 後，schema、signature、closure、actual family oracle、structural、semantic、admission、final 與 `record_accepted` 全部為 PASS，`issues=[]`。

Schema 將 `advice` 放在 `admissibility` 並列為 required，只限制為 string，未標記 annotation／nonnormative；external validator 的 uniformity、advice-generation、access、ledger 與 reference derivations皆未讀取該欄位。故同一 accepted record 可同時帶有互斥的 advice declaration 與 resource account。

### 最低修正義務

以 typed `advice_mode` 取代自由文字，導出 `ExpectedAdviceDecl(family, mechanism)`，並與 generator ref、uniformity、program quantifier、answer access、ledger bytes 及 generation account 作雙向一致性檢查；若該字串只供顯示，則明確移入 nonnormative annotation。

## Scoped positives

- `CLOSURE-CLASS-01`：bounded executable fix CLOSED/PASS。
- `CLOSURE-EDGE-SCOPE-01`：bounded executable／scope fix CLOSED/PASS。
- `ORACLE-DECL-FAMILY-01`：bounded valid-signature executable／semantic fix CLOSED/PASS。
- 其餘成功計數只構成 frozen I0 範圍內的 Observation／Experiment，不升格為 validator soundness 或 completeness theorem。

## Nonclaims

- 不表示實際 answer table、answer oracle 或未記帳資源已通過執行驗證。
- 不表示 production signer authority、一般硬體量測可信性或任意機制的完整驗證。
- 不授權 promotion、AI Board success 或 shared-repository publication。
- 不對 `P=NP`、`P≠NP` 或任何一般 complexity-theory 命題作外推。

Frozen v0.2.4 bytes 保持不變；修正應另起 successor version。
