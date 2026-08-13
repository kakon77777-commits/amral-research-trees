# I0 v0.2.3 candidate validation report

## Disposition

本地 disposition：`SELF-TEST PASS / CANDIDATE_UNPROMOTED`。

協作 disposition：`PENDING AI-1/AI-2/AI-3 FROZEN READ-ONLY ACCEPTANCE`。

本報告不授權 promotion、共享 repo、Board success 或任何 P/NP 結論。

## Environment

- CPython 3.14.5
- jsonschema 4.26.0 / Draft 2020-12 + FormatChecker
- cryptography 49.0.0 / Ed25519 test-fixture signatures
- Windows 10.0.19045；single worker
- fixed seed `20260809`

## Commands and observed results

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONPATH=(Resolve-Path src)
python -m unittest discover -s tests -v
python -m unittest discover -s tests_v021 -v
python -m unittest discover -s tests_v022 -v
python -m unittest discover -s tests_v023 -v
python scripts/reproduce_closure_class_v023.py .
python -m pnp_glc_i0.experiment_v023 --project-root . --output i0-run-report.v0.2.3-candidate.json --seed 20260809 --max-parity-n 12
```

觀察結果：14/14 + 11/11 + 15/15 + 16/16 tests PASS；17/17 closure probes conformant；33-fixture manifest 0 mismatch；2-SAT 1500 fixed-seed exhaustive cases PASS；107 個 fixture/artifact outputs 立即重產 byte-identical。live report 含實測時間，所以只把本次輸出納入 frozen manifest，不主張跨執行 byte-identical。

## CLOSURE-CLASS-01 result

- generic EnvelopeShape 在 spec-id dispatch 前執行；
- required member 缺失、空值、錯型與 generic edge malformed 均 `FAIL`；
- 完整但 unsupported 的 envelope 為 `UNKNOWN`；
- `FAIL` 與 `UNKNOWN` 均阻止 admission；
- 兩個 valid-signature end-to-end classification fixtures 均拒絕。

## 保留的正向有限觀察

- uniform streaming PARITY：外部 admission=true，prefix invariant 實際執行並核對；
- per-length truth-table PARITY：答案可正確，但 uniformity/advice/answer-access gates 使 admission=false；
- terminal-only projection 仍刻意無法分辨上述雙族，acceptance 必須由 provenance/uniformity/resource evidence 派生；
- standard/robust × neutral/bounded gate matrix 與 account/budget applicability 未變；
- pinned 2-SAT SAT assignment 與 UNSAT mutual-implication certificates 皆 end-to-end accepted；
- PROV-DERIVE-01 的 states=999 與 fabricated transition digest 仍拒絕；
- REF-TYPE-01 的 receipt-only robust→standard、public-key type confusion 與 valid-signature contract/invariant cross-role substitution 仍拒絕；
- schema bytes、artifact bytes、trace/auth、projection 與 operational reference map 維持 snapshot/hash 綁定。

## 資源帳與失敗前沿

每個 run record 仍保存 time、space、construction、update、decode、lift、verify、restart、parallel、precision、description/advice/proof/output bytes、resource account、semantic-loss debt 與 failure-frontier axes。resource-neutral 只表示沒有 budget threshold，不表示免記帳。

限制：validator 是 bounded executable interface，不是 proof-assistant kernel或 universal interpreter；robust 僅覆蓋 pinned finite deterministic singleton run；test signer 不等於 production measurement authority；2-SAT 不代表 general 3-SAT/CDCL。實驗加速不等於 P=NP，實驗失敗不等於 P≠NP。
