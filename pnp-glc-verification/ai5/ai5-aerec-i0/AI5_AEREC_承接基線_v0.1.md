# AI-5｜AEREC × P/NP 四層閉合工程承接基線 v0.1

日期：2026-08-09（Asia/Taipei）  
狀態：**Engineering Experiment / unpromoted candidate continuation**

## 1. 四個任務實際在做什麼

### `Clarify WTF issue`：AI-1 整合與驗收中樞

名稱看似臨時澄清，實際內容是四 AI 的架構整合、版本裁定與獨立驗收。它把 AI-3
Phase 1 Lean 4 判為限定範圍 PASS，並把 AI-4 frozen v0.2 因
`PROV-DERIVE-01` 判為 FAIL。它不以 Board 討論、編譯成功或測試通過替代主張採納。

### AI-2：紅隊與障礙審計

AI-2 建立 pointwise-infimum/nonuniformity 反例、PARITY streaming/table separation、
schema cross-field 反例，並以可重放 mutation 證明 v0.2 的 `states=999` 與 fabricated
transition digest 仍可被接受。核心作用是把「看起來自洽」打回「可被外部導出」。

### AI-3：形式化與定理重建

AI-3 把 resource regime 與 run quantifier 拆成兩軸，建立 GLC0、standard/robust、
gate applicability 與 theorem ladder。Phase 1 Lean 4 在明示範圍內可重建、可編譯，
但 `SemanticValidate`、`DerivesRecord`、一般 fairness/maximality/zero-debt 仍是義務，
四層大箭頭及 P/NP 結論仍是 Open Problem。

### AI-4：演算法與工程現實審計

AI-4 已落地 `I0 = Claim-Ledger + PARITY Admission + 2-SAT`。frozen v0.2 的
14 tests 與算法實驗通過，但 provenance 不成立，所以只保留為 `StructuralReplay`
反例基線。v0.2.1 另加 Ed25519 fixture authenticity、pinned PARITY/2-SAT transition
execution、resource/debt derivation、typed transitive closure 與 SAT/UNSAT 端到端紀錄；
v0.2.1 隨後因 `REF-TYPE-01` 正式 FAIL：receipt-only 的 run-spec 類引用可被換成錯誤
角色的既有 artifact，重算 closure 後仍通過。它現在是 frozen 反例基線；AI-4 已另起
v0.2.2 修補 role/type/version/mode 與 operational-reference binding。AI-1 正式報告
SHA-256 為 `889E8C2D22B628D810B660A9C9064EABA55A392709C5432C1E7A6DE5AACFD2B4`。

## 2. AEREC 的真實可用邊界

授權資料的理論閉環可直接沿用：穩定 identity、contract、候選族、觀測、驗證、
benchmark、Pareto/no-change、commit/rollback、history learning。

RC1 程式本身不能直接當 P/NP production engine：核心候選與投影大量特例化
`sum_squares`；驗證仍依 baseline-as-oracle 與有限隨機域；rollback 主要是 metadata
切換；Windows CPython 3.14.5 全套 47 tests 有 8 個 `os.posix_spawn` portability errors。
因此 AI-5 抽取 AEREC 方法，不把 RC1 backend 的成熟度標籤外推到本研究。

## 3. AI-5 第一個實戰迭代

父代身份固定為 AI-4 v0.2.1 frozen hashes；任何位元漂移都停止並選 no-change。
AI-5 在本任務只讀快照中完成：

- 搬移 `pnp-glc-i0` 單一目錄後，原 14/14 與 11/11 suites 各出現 1 個
  `FileNotFoundError`：兩者都把 v0.1 schema 寫死在
  `ROOT.parent/run-record.schema.json`。
- 補上 hash 精確為 `3B50247D…CAF4` 的相容父層後，14/14 與 11/11 全 PASS。
- AI-5 probe 自身 4/4 PASS。
- 控制組與 batch-snapshot 組都對 22/22 manifest fixtures 得到同樣結果；跑前／跑後
  七個核心 hashes 均穩定。
- 控制組每 record 重建整棵 `ArtifactIndex`；22 個 fixture medians 合計
  `1682.701 ms`。
- AI-5 先把 138 files / 1,177,012 bytes 讀成一次不可變 content-addressed snapshot，
  schema、records、refs 全從同一 bytes universe 驗證；合計 `222.530 ms`，即
  **7.56× validation-throughput speedup**。

這個提升只屬驗證批次吞吐，不是 PARITY/2-SAT 求解複雜度改善。

## 4. 遞歸演化規則

1. **Observe**：記錄每個 gate/fixture 的失敗率、wall time、資源與攻擊來源。
2. **Diagnose**：分開 structural、integrity、authenticity、transition、resource、oracle。
3. **Generate**：只生成針對 failure frontier 的小候選；舊 frozen bytes 不覆寫。
4. **Verify**：正例與攻擊例混跑，避免 reject-all 假解；`unknown` 與 `fail` 都 fail closed。
5. **Benchmark**：construction/verification/deployment 成本與 solver runtime 分帳。
6. **Select**：correctness/provenance 是硬 gate；其內才比較 latency、memory、描述長度與恢復成本。
7. **Commit**：AI-1/AI-2 獨立驗收前維持 unpromoted；no-change 永遠合法。
8. **Learn**：歷史中曾抓到 mismatch 且成本低的 probes，在下一代 fail-fast 排序提前；full
   acceptance 仍跑完整 corpus。

## 5. 下一個工程切片

AI-5 已把 `REF-TYPE-01` 加入外部合成負例：v0.2.1 的原 22/22 manifest 仍通過，
但新負例未被拒絕，因此 AEREC 選擇已從 pending 自動退回 `no-change-control`。這正是
「歷史反例不被下一代遺忘」的第一次遞歸演化。

待 v0.2.2 frozen 後，先要求 role-aware refs 與 signed/derived operational map 通過，
再處理效能演化：

把目前 monolithic validator 拆成有依賴的可觀測 gate graph，使用
`expected downstream cost avoided × failure probability / gate cost` 排序 ready gates；
同時保留一次 immutable bundle snapshot。之後才按 AI-4 原路線擴到 Horn-SAT、
XOR-SAT、bounded-treewidth SAT、general 3-SAT/CDCL，各自有固定 baseline、獨立 oracle、
完整構造/驗證成本與 failure frontier。

## 6. 非主張

- 本地 PASS 不等於獨立採納。
- validation throughput 提升不等於 solver speedup。
- 任一實驗成功不推出 `P=NP`；任一實驗失敗不推出 `P≠NP`。
- 本文件沒有替四層大等價或類終極認知動力學完成性背書。
