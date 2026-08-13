# REF-TYPE-01 v0.2.2 candidate reproduction

狀態：Experiment；候選修補自測，待獨立驗收。

執行：

```powershell
$env:PYTHONUTF8='1'
python scripts/reproduce_ref_type_v022.py
```

預期 exit code：0，且 `all_expected=true`。

## Case 1：receipt-ref-substitution

從 validly signed robust record 出發，只將 receipt `run_spec_ref` 從 robust 換為 standard，重算 resolved closure，不重簽。

- signature：pass
- envelope closure：pass（兩者都是合法 run-spec）
- operational role binding：fail
- record accepted：false

這一例證明 v0.2.2 不以 envelope type 相同取代 mode/id/hash binding。

## Case 2：robust-ref-type-confusion

只將 receipt run/maximal/fairness/sandbox 四個 refs 換成 pinned Ed25519 public-key artifact，重算 closure，不重簽。

- signature：pass
- direct role→type：fail
- operational role binding：fail
- record accepted：false

## Case 3：cross-role-contract-invariant

將 PARITY contract 與 invariant roles 對調，同步 candidate/event/certificate，建立新的 valid signature，並讓 signed trace map 忠實記錄被調換的 actual map。

- signature：pass
- role-bearing closure：fail
- signed map vs validator-derived map：fail
- family/type binding：fail
- record accepted：false

成功拒絕這三例只表示已封閉已知 REF-TYPE attack family；不構成 validator 完整性定理，也沒有 P/NP 含義。

