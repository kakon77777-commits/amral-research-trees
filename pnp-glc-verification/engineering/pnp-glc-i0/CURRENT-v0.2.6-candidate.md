# P/NP GLC I0 v0.2.6 candidate

狀態：`CANDIDATE_UNPROMOTED / pending AI-1 managed bounded acceptance`。

父版是 frozen v0.2.5：`SHA256SUMS-v0.2.5-candidate.txt` 166/166，manifest SHA-256 `9D759DB19360E9716E372B7791C251626F658E5C4A185A297EEF6EA01DE9531E`。本版沒有覆寫父版或更早 bytes，也沒有建立 v0.2.7。

本版只處理三項既定 blocker：

1. `CLOSURE-SUPPORTED-RELATION-RESULT-01`：normative judgments graph 內明列 supported header/relation 的 false terminal、true transition，以及 traversal fixed-point 的 PASS/FAIL/UNKNOWN terminal trichotomy。
2. `ACCEPTANCE-MANIFEST-RUNTIME-CLOSURE-01`：以 AST 導出 20 個 Python source paths 與 29 條 local import edges；以 validator 的 direct-reference/fixed-point closure 再導出 legacy opaque evidence；209 個 runtime/evidence/build-input paths 全部必須受 top-level manifest 覆蓋；六條官方命令在只含 manifest paths 的新隔離 snapshot 以 `python -I -B` 執行。
3. `FROZEN-LIVE-REPORT-SCOPE-01`：v0.2.6 自身以 seed `20260809` 真正執行 6×250=1500 個 2-SAT cases；frozen JSON 明列生成命令、seed、逐層 SAT/UNSAT/count、零 mismatch、零 certificate failure、evidence pointer 與 digest `2F472DB6486459BC6502AA0ABDF1B79FD361D274F41DFE461E14C197F414EBEF`。

Freeze path set 為 216 entries。Manifest-only 隔離重播 `all_pass=true`：六條官方命令全 exit 0，guard 全通過，snapshot extra/missing/changed files皆為空，且輸出不含 original root。

保留的 bounded positives：`CLOSURE-JUDGMENT-COMPLETENESS-01 CLOSED/PASS`、`ADVICE-DECL-LEDGER-01 CLOSED/PASS`。

本候選不發布 Board、不建立 shared repo、不作 P=NP 或 P≠NP 外推。
