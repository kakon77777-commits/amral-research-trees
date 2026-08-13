# ORACLE-DECL-FAMILY-01：v0.2.3 反例與 v0.2.4 回歸

分類：accepted-record declaration/provenance counterexample；不是 correctness、oracle execution、signature或closure bypass，也不是 P/NP 結果。

## Frozen v0.2.3 反例

PARITY record 可把 `mechanism.oracle` 換成 2-SAT 的 `name/checks`，重算 projection/trace/operational map並用既有 test-fixture key有效簽名。兩族共用同一 pinned `oracles.py` hash，因此 v0.2.3 只驗 hash/version/independent時仍接受。

validator實際仍按 `problem.family=PARITY` 執行 `parity_oracle` 且答案正確；缺陷只在已接受 record 的 oracle declaration不真。schema把 name/checks列為required，candidate report又聲明 family-bound oracle，因此不能把 checks事後降為無規範 annotation。

AI-3 formal classification addendum：`517A1A31DFB4294A67C343011E1AA20BF088F76A31D483FD0439003913616BA6`。
AI-2 combined bounded review：`4029F719B0B38C276A53854659D094B14A62D45D934913EF9A5FAEB7ED5B6661`。
AI-1 independent reproduction addendum：`AC8AD8ED69079842CC96EE736137BFD35C92B74B1FB189965438C3303D64BF29`。

## v0.2.4 修補

- schema新增 required `oracle_id`、`entrypoint` 與 `obligations`；
- `ExpectedOracleDecl(family, mechanism, resultStatus)` 導出 exact oracle-id、entrypoint、name、checks及obligations；
- 共用 source hash只證 code bytes，不再替代 family/result declaration binding；
- SemanticValidate不符即產生 `oracle-declaration-family-binding`。

## Executable regression

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_oracle_decl_family_v024.py .
```

本地觀察：exit 0；9 negative probes、3 positive controls、unexpected `[]`。

負例涵蓋：PARITY↔2-SAT完整 declaration、2-SAT SAT↔UNSAT、oracle-id only、entrypoint only、name only、checks only、obligations only。每個負例均 valid signature，且 actual family oracle status=`pass`，但 record accepted=`false`。reproducer SHA-256：`0A0EA8607D2E07E6189ACC52B698E781CF742C6523C4D46FF3F02330AF1B779B`。

以上只建立 bounded I0 declaration binding；不是任意 oracle framework 的 soundness theorem，亦不改變一般 SAT/P/NP 狀態。
