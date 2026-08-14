# v0.5 Exact Census — 本地端 AI 交接文件

**日期：** 2026-08-12  
**階段：** v0.5 Exact Census  
**用途：** 交由本地端 AI / Agent 直接取得 Git repository 的 old/current 巨型輸出檔，完成 entry-level 精確差分與原因 census。  
**原則：** 本文件只整理目前已確認的分析框架與待執行工作；不得把 Git diff 行數、cache 片段或推論值冒充 exact census。

---

# 0. 任務摘要

目前雲端端已經把 v0.5 的問題縮成一個非常明確的資料分析任務：

1. 真正取得 **old / current** 兩個版本中的 giant output files。
2. 將 base elliptic-curve labels 與 twist mappings **物化、完整解析成集合／映射**。
3. 精確計算：
   - 哪些 base curves 被移除／新增；
   - 被移除的 base curves 分別死於哪一個 Algorithm1 gate；
   - 對「old/current 都存在」的 stable base curves，Algorithm2 到底移除了哪些 twists、增加了哪些 twists；
   - 驗證所有總量與逐 entry 原因可以閉合。
4. 產生可供後續數學／程式分析直接使用的 CSV、JSON 與 MD 報告。

最重要的 methodological rule：

> **Algorithm1 造成的 base deletion 與 Algorithm2 的 twist-level delta 必須拆開。**

不能把 upstream base curve 消失後連帶消失的 twists 算成 Algorithm2 的 removals。

---

# 1. 已知檔案

目前已知 giant output 至少包含：

```text
ec_labels_500k.txt
twists_of_ec_labels_500k.json
```

需要取得兩個 Git state：

```text
OLD
CURRENT
```

所以實際分析輸入應是四份內容：

```text
old/ec_labels_500k.txt
new/ec_labels_500k.txt

old/twists_of_ec_labels_500k.json
new/twists_of_ec_labels_500k.json
```

如果 repository 內檔名、路徑或格式略有變更，以實際 Git tree 為準，但在報告中記錄 exact path 與 commit SHA。

---

# 2. 已知 aggregate counts

目前已確認／前序分析採用的 base counts：

```text
old base count     = 40,749
current base count = 36,687
difference         = 4,062
```

因此如果 current 沒有額外新增 base curves，理論上：

$$
|B_{\rm old}\setminus B_{\rm new}| = 4062.
$$

但 **不要直接假定沒有新增**。

必須實際計算：

$$
B_{\rm removed}=B_{\rm old}\setminus B_{\rm new},
$$

$$
B_{\rm added}=B_{\rm new}\setminus B_{\rm old},
$$

$$
B_{\rm stable}=B_{\rm old}\cap B_{\rm new}.
$$

並驗證：

$$
|B_{\rm new}|
=
|B_{\rm old}|
-
|B_{\rm removed}|
+
|B_{\rm added}|.
$$

只有當：

$$
|B_{\rm added}|=0
$$

時，才可以把 4062 直接解讀為 removed base curves 的精確數量。

---

# 3. 核心集合模型

定義：

$$
B_{\rm old}=\text{old base curve label set},
$$

$$
B_{\rm new}=\text{current base curve label set}.
$$

對每一個 base curve $E$，定義 twist sets：

$$
T_{\rm old}(E),
\qquad
T_{\rm new}(E).
$$

全域 twist pair 建議不要只存 twist value，而要存成：

$$
(E,d)
$$

或 repository 實際使用的唯一 pair representation。

這樣才能避免不同 base curve 的 twist value collision。

定義：

$$
\mathcal T_{\rm old}
=
\{(E,d): E\in B_{\rm old}, d\in T_{\rm old}(E)\},
$$

$$
\mathcal T_{\rm new}
=
\{(E,d): E\in B_{\rm new}, d\in T_{\rm new}(E)\}.
$$

---

# 4. 第一層：Base Curve Exact Diff

必須輸出：

```text
base_removed.csv
base_added.csv
base_stable.csv
```

最少欄位：

```text
curve_label
status
```

推薦再加：

```text
old_index
new_index
```

如果原始輸出本身有排序。

統計：

```text
old_base_count
new_base_count
removed_base_count
added_base_count
stable_base_count
```

並驗證集合閉合：

$$
B_{\rm old}
=
B_{\rm removed}\sqcup B_{\rm stable},
$$

$$
B_{\rm new}
=
B_{\rm added}\sqcup B_{\rm stable}.
$$

---

# 5. Algorithm1：4062 Removed Curves Failure-Cause Census

目前分析指出 removed curves 應該來自 Algorithm1 semantic delta。

需要對每一條：

$$
E\in B_{\rm removed}
$$

做逐 entry failure diagnosis。

目前最重要的兩類 gate：

## Gate A — rational 3/5/7-isogeny

記：

$$
I(E)=\{\ell:\ E\text{ admits the relevant rational }\ell\text{-isogeny}\}.
$$

需要判定：

$$
\{3,5,7\}\cap I(E)\neq\varnothing.
$$

輸出 boolean：

```text
has_isogeny_3
has_isogeny_5
has_isogeny_7
fails_isogeny_gate
```

其中：

```text
fails_isogeny_gate = has_isogeny_3 OR has_isogeny_5 OR has_isogeny_7
```

名稱若與 source code semantic 相反，請在最終報告統一修正，但要保留「實際 code condition」與「分析命名」的對應。

## Gate B — local coefficient at 3

目前需測：

$$
|a_3(E)|=3.
$$

輸出：

```text
a3
abs_a3_eq_3
```

---

# 6. Algorithm1 完整性反例 Gate

對所有 removed curves，必須驗證：

$$
\boxed{
B_{\rm removed}
\subseteq
F_{3/5/7}\cup F_{a_3}
}
$$

也就是：

$$
\forall E\in B_{\rm removed},
\qquad
\left(
\{3,5,7\}\cap I(E)\neq\varnothing
\right)
\lor
\left(
|a_3(E)|=3
\right).
$$

建立：

```text
algorithm1_unexplained_removed.csv
```

如果完全閉合，檔案應只有 header 或 0 rows。

如果存在任何 row：

> **立即停止宣稱「Algorithm1 delta 已完全理解」。**

這代表至少有一種可能：

1. 還存在未識別的 semantic delta；
2. gate implementation 與目前理解不同；
3. old/current commit 選錯；
4. elliptic-curve metadata 計算方式不一致；
5. parser / label normalization 有 bug。

---

# 7. Algorithm1 Failure-Cause 分類

每一條 removed curve 建議分類為：

```text
ISOGENY_ONLY
A3_ONLY
BOTH
UNEXPLAINED
```

正式定義：

### ISOGENY_ONLY

$$
F_{3/5/7}(E)=1,\qquad F_{a_3}(E)=0.
$$

### A3_ONLY

$$
F_{3/5/7}(E)=0,\qquad F_{a_3}(E)=1.
$$

### BOTH

$$
F_{3/5/7}(E)=1,\qquad F_{a_3}(E)=1.
$$

### UNEXPLAINED

$$
F_{3/5/7}(E)=0,\qquad F_{a_3}(E)=0.
$$

輸出：

```text
algorithm1_removed_census.csv
```

推薦欄位：

```text
curve_label
has_isogeny_3
has_isogeny_5
has_isogeny_7
isogeny_set_357
a3
abs_a3_eq_3
failure_class
```

統計：

```text
isogeny_only_count
a3_only_count
both_count
unexplained_count
```

並驗證：

$$
4062
=
N_{\rm iso-only}
+
N_{a_3\rm-only}
+
N_{\rm both}
+
N_{\rm unexplained}
$$

前提是 exact removed count 最後確實為 4062。

---

# 8. Algorithm2：必須先建立 Stable Base Domain

Algorithm2 的 twist census **只能**在：

$$
\boxed{
B_{\rm stable}
=
B_{\rm old}\cap B_{\rm new}
}
$$

上執行。

原因：

若：

$$
E\in B_{\rm removed},
$$

則其所有 old twists：

$$
T_{\rm old}(E)
$$

會因 base curve 不再存在而整組從 current JSON 消失。

這是：

$$
\Delta_{\rm upstream\ Algorithm1}
$$

不是：

$$
\Delta_{\rm Algorithm2}.
$$

---

# 9. Twist Delta 的三層拆分

## 9.1 Upstream-removal twists

定義：

$$
R_{\rm upstream}
=
\sum_{E\in B_{\rm removed}}
|T_{\rm old}(E)|.
$$

這是因 Algorithm1 base deletion 連帶消失的 twist pairs。

輸出：

```text
twists_removed_by_upstream_base_deletion.csv
```

欄位：

```text
curve_label
twist
reason = UPSTREAM_BASE_REMOVAL
algorithm1_failure_class
```

## 9.2 Stable-base Algorithm2 removals

對：

$$
E\in B_{\rm stable},
$$

定義：

$$
R_E
=
T_{\rm old}(E)\setminus T_{\rm new}(E).
$$

總量：

$$
R_{\rm stable}
=
\sum_{E\in B_{\rm stable}} |R_E|.
$$

輸出：

```text
algorithm2_removed_twists.csv
```

## 9.3 Stable-base Algorithm2 additions

定義：

$$
A_E
=
T_{\rm new}(E)\setminus T_{\rm old}(E).
$$

總量：

$$
A_{\rm stable}
=
\sum_{E\in B_{\rm stable}} |A_E|.
$$

輸出：

```text
algorithm2_added_twists.csv
```

---

# 10. 每條 Stable Base Curve 的 Algorithm2 分類

對：

$$
E\in B_{\rm stable}
$$

計算：

```text
old_twist_count
new_twist_count
removed_twist_count
added_twist_count
```

然後分類：

### UNCHANGED

```text
removed = 0
added   = 0
```

### SHRINK_ONLY

```text
removed > 0
added   = 0
```

### EXPAND_ONLY

```text
removed = 0
added   > 0
```

### MIXED

```text
removed > 0
added   > 0
```

注意：

> `new_twist_count < old_twist_count` 並不代表沒有 additions。

例如：

```text
old = {1,2,3,4}
new = {2,3,5}
```

雖然 count 從 4 變 3，但實際：

```text
removed = {1,4}
added   = {5}
```

所以一定要做 set diff，不能只比較 counts。

輸出：

```text
algorithm2_stable_curve_census.csv
```

建議欄位：

```text
curve_label
old_twist_count
new_twist_count
removed_twist_count
added_twist_count
net_delta
algorithm2_class
```

其中：

$$
\text{net\_delta}
=
|T_{\rm new}(E)|-|T_{\rm old}(E)|.
$$

---

# 11. 全域 Accounting Identity

最重要的驗證式之一：

$$
\boxed{
|\mathcal T_{\rm old}|
-
|\mathcal T_{\rm new}|
=
R_{\rm upstream}
+
R_{\rm stable}
-
A_{\rm stable}
-
A_{\rm newbase}
}
$$

其中若 new version 存在新增 base curves：

$$
A_{\rm newbase}
=
\sum_{E\in B_{\rm added}}
|T_{\rm new}(E)|.
$$

若：

$$
B_{\rm added}=\varnothing,
$$

則簡化為：

$$
\boxed{
|\mathcal T_{\rm old}|
-
|\mathcal T_{\rm new}|
=
R_{\rm upstream}
+
R_{\rm stable}
-
A_{\rm stable}
}
$$

這比目前早期簡化式更完整，因為它顯式處理 new base curves。

必須在報告中輸出：

```text
old_total_twist_pairs
new_total_twist_pairs
upstream_removed_twist_pairs
stable_removed_twist_pairs
stable_added_twist_pairs
newbase_added_twist_pairs
lhs
rhs
accounting_identity_pass
```

必須要求：

```text
lhs == rhs
```

exact integer equality。

---

# 12. 關於先前 Git Diff 的 +1899 / -53404

先前觀察到 giant twists JSON textual diff 類似：

```text
+1899
-53404
```

**禁止直接解讀成：**

```text
新增 1899 個 twists
刪除 53404 個 twists
```

原因至少包括：

1. JSON formatting / key removal 會改變 textual line count；
2. base curve 整個被刪除，會造成整個 JSON entry 消失；
3. 一行可能包含一個 list、curve 或多個 twists；
4. upstream Algorithm1 deletions 尚未剝離。

v0.5 exact census 的目的之一，就是把 textual diff 完全替換為 parsed set diff。

---

# 13. JSON Parser 要求

不要假定 `twists_of_ec_labels_500k.json` 一定是：

```json
{
  "curve": [1, 2, 3]
}
```

先 inspect schema。

可能型態包括但不限於：

```json
{
  "curve": [...]
}
```

或：

```json
[
  {...},
  {...}
]
```

或 nested metadata。

Parser 必須先輸出：

```text
json_top_level_type
sample_keys
sample_entry
number_of_base_keys
number_of_twist_pairs
```

並確認 old/current 使用同一 semantic schema。

如果 schema changed：

> 先寫 normalization layer，再做集合比較。

統一 normalize 成：

```python
dict[str, set[CanonicalTwist]]
```

---

# 14. Label Canonicalization

Base curve label 必須 canonicalize。

最少：

```python
label = label.strip()
```

並檢查：

```text
duplicate labels
blank lines
unexpected whitespace
case changes
ordering differences
```

如果 label syntax 有 mathematical structure，不要擅自重寫，只做 repository 可證明等價的 normalization。

輸出：

```text
old_duplicate_base_labels
new_duplicate_base_labels
old_unparsed_labels
new_unparsed_labels
```

---

# 15. Twist Canonicalization

Twist representation 可能是：

```text
integer d
string label
structured object
```

必須保留 source semantic。

如果 twist 是整數：

```python
CanonicalTwist = int
```

若是 object，建立 deterministic tuple / canonical JSON serialization。

任何 canonicalization 必須滿足：

$$
x=y\text{ semantically}
\iff
C(x)=C(y).
$$

不要只用 `str(object)` 當數學等價判定，除非 source schema 明確保證。

---

# 16. 建議執行流程

## Step 1 — Repository provenance

記錄：

```text
repo URL
old commit SHA
current commit SHA
old file paths
current file paths
git status
```

建議使用：

```bash
git rev-parse HEAD
git show <OLD>:<path>
git show <CURRENT>:<path>
```

或直接建立兩個 worktree：

```bash
git worktree add ../repo-old <OLD>
git worktree add ../repo-new <CURRENT>
```

## Step 2 — Raw file integrity

取得：

```text
file byte size
SHA256
line count
```

對四個 raw files 都做。

輸出：

```text
raw_file_manifest.json
```

## Step 3 — Parse base sets

建立：

```python
B_old
B_new
B_removed
B_added
B_stable
```

驗證 counts。

## Step 4 — Parse twist maps

建立：

```python
T_old: dict[curve, set[twist]]
T_new: dict[curve, set[twist]]
```

檢查：

```text
all twist-map base labels should be understood
orphan twist keys
missing twist keys
```

注意：不是每一條 base curve 一定必須有 twist JSON key。這要依 source format 判定，不能自行假定。

## Step 5 — Algorithm1 census

對 `B_removed` 逐 curve 求：

```text
3/5/7 rational isogeny status
a3
failure_class
```

資料來源優先順序：

1. repository 已有 metadata / code；
2. project 使用的同一 elliptic-curve library / DB；
3. 若要重新計算，必須與 source implementation 的 convention 對齊。

不要混入另一套資料庫而不記錄版本。

## Step 6 — Stable-base twist diff

對：

```python
for E in B_stable:
    removed = T_old[E] - T_new[E]
    added   = T_new[E] - T_old[E]
```

輸出逐 curve 與逐 pair 檔案。

## Step 7 — Upstream twist removal

對：

```python
for E in B_removed:
    for d in T_old.get(E, set()):
        ...
```

這批全部標記：

```text
UPSTREAM_BASE_REMOVAL
```

不要混進 Algorithm2。

## Step 8 — New-base twists

若：

```python
B_added != empty
```

則 current-only twists全部分開記錄：

```text
NEW_BASE_ADDITION
```

不要算成 stable Algorithm2 addition。

## Step 9 — Accounting identities

至少驗證：

### Base

$$
|B_{\rm old}|
=
|B_{\rm removed}|+|B_{\rm stable}|,
$$

$$
|B_{\rm new}|
=
|B_{\rm added}|+|B_{\rm stable}|.
$$

### Twist

$$
|\mathcal T_{\rm old}|
-
|\mathcal T_{\rm new}|
=
R_{\rm upstream}
+
R_{\rm stable}
-
A_{\rm stable}
-
A_{\rm newbase}.
$$

### Algorithm1 explanation

$$
N_{\rm unexplained}=0
$$

才算完全 closure。

---

# 17. 建議程式結構

```text
v0_5_exact_census/
├─ README.md
├─ inputs/
│  ├─ old/
│  │  ├─ ec_labels_500k.txt
│  │  └─ twists_of_ec_labels_500k.json
│  └─ new/
│     ├─ ec_labels_500k.txt
│     └─ twists_of_ec_labels_500k.json
├─ scripts/
│  ├─ 00_manifest.py
│  ├─ 01_parse_base_sets.py
│  ├─ 02_parse_twist_maps.py
│  ├─ 03_algorithm1_failure_census.py
│  ├─ 04_algorithm2_stable_diff.py
│  ├─ 05_accounting_checks.py
│  └─ 06_build_report.py
├─ results/
│  ├─ raw_file_manifest.json
│  ├─ base_removed.csv
│  ├─ base_added.csv
│  ├─ base_stable.csv
│  ├─ algorithm1_removed_census.csv
│  ├─ algorithm1_unexplained_removed.csv
│  ├─ twists_removed_by_upstream_base_deletion.csv
│  ├─ algorithm2_removed_twists.csv
│  ├─ algorithm2_added_twists.csv
│  ├─ algorithm2_stable_curve_census.csv
│  ├─ new_base_twists.csv
│  ├─ summary.json
│  └─ V0_5_EXACT_CENSUS_REPORT.md
└─ logs/
   └─ run.log
```

---

# 18. `summary.json` 建議 schema

```json
{
  "provenance": {
    "repo": "",
    "old_commit": "",
    "new_commit": ""
  },
  "base": {
    "old": 0,
    "new": 0,
    "removed": 0,
    "added": 0,
    "stable": 0
  },
  "algorithm1": {
    "isogeny_only": 0,
    "a3_only": 0,
    "both": 0,
    "unexplained": 0
  },
  "twists": {
    "old_total_pairs": 0,
    "new_total_pairs": 0,
    "upstream_removed": 0,
    "stable_removed": 0,
    "stable_added": 0,
    "newbase_added": 0
  },
  "algorithm2_curve_classes": {
    "unchanged": 0,
    "shrink_only": 0,
    "expand_only": 0,
    "mixed": 0
  },
  "checks": {
    "base_old_partition": false,
    "base_new_partition": false,
    "algorithm1_all_removed_explained": false,
    "twist_accounting_identity": false
  }
}
```

---

# 19. 最終報告必須回答的問題

## Q1

Base curves exact delta 是多少？

```text
old =
new =
removed =
added =
stable =
```

## Q2

4062（如果 exact diff 最後仍是 4062）removed curves 的 failure-cause histogram 是多少？

```text
ISOGENY_ONLY =
A3_ONLY =
BOTH =
UNEXPLAINED =
```

另外拆出：

```text
3-isogeny count
5-isogeny count
7-isogeny count
all combinations
```

例如：

```text
{3}
{5}
{7}
{3,5}
{3,7}
{5,7}
{3,5,7}
```

## Q3

是否存在任何：

$$
E\in B_{\rm removed}
$$

同時：

$$
\{3,5,7\}\cap I(E)=\varnothing
$$

且：

$$
|a_3(E)|\neq3?
$$

若有，列出全部。

## Q4

因 Algorithm1 base deletion 而連帶消失的 twist pairs 有多少？

$$
R_{\rm upstream}=?
$$

## Q5

在 stable base curves 上，Algorithm2：

```text
removed how many twist pairs?
added how many twist pairs?
net delta?
```

## Q6

Algorithm2 對 stable base curves 的 curve-level 類別：

```text
UNCHANGED =
SHRINK_ONLY =
EXPAND_ONLY =
MIXED =
```

## Q7

到底有哪些 curves 出現「一邊刪、一邊加」？

把所有：

```text
MIXED
```

列出。

這些是後續最值得檢查 Algorithm2 semantic rewrite 的 cases。

## Q8

新增的 twist pairs 是否集中在特定 curve family / conductor / arithmetic feature？

這一項是 exploratory。先只做描述統計，不先因果化。

## Q9

全域 accounting identity 是否 exact pass？

必須：

```text
PASS
```

否則 v0.5 不得標記完成。

---

# 20. 最值得優先人工檢查的 cases

產出四個 top lists：

### A. Algorithm1 unexplained

全部列出，不限數量。

### B. Algorithm2 最大 SHRINK

依：

```text
removed_twist_count
```

descending。Top 50。

### C. Algorithm2 最大 EXPAND

依：

```text
added_twist_count
```

descending。Top 50。

### D. Algorithm2 MIXED

全部列出，若太多則至少先 Top 100 並另附完整 CSV。

---

# 21. 不能做的事情

## 禁止 1

不能再以：

```text
Git textual diff + / -
```

替代 parsed entry delta。

## 禁止 2

不能把：

```text
base deleted -> all its twists gone
```

算成 Algorithm2 removals。

## 禁止 3

不能把 total twist count 的下降直接解釋成「Algorithm2 更嚴格」。

可能同時存在：

```text
大量 removals + 小量 additions
```

## 禁止 4

不能因為 4062 恰好等於 old-new count，就省略 `B_added` 計算。

## 禁止 5

不能把：

```text
UNEXPLAINED = 0
```

在沒有逐 entry metadata 計算前預設成立。

## 禁止 6

如果 old/current giant files 的 schema 不同，不能直接比較 raw JSON values。

必須先 normalize。

---

# 22. 建議的 Python 核心骨架

```python
from pathlib import Path
import json

def load_labels(path):
    labels = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            x = line.strip()
            if x:
                labels.append(x)
    return labels

old_labels_raw = load_labels("inputs/old/ec_labels_500k.txt")
new_labels_raw = load_labels("inputs/new/ec_labels_500k.txt")

B_old = set(old_labels_raw)
B_new = set(new_labels_raw)

B_removed = B_old - B_new
B_added   = B_new - B_old
B_stable  = B_old & B_new

assert len(B_old) == len(B_removed) + len(B_stable)
assert len(B_new) == len(B_added) + len(B_stable)
```

Twist parser 要依實際 JSON schema 寫，不要照抄假 schema。

stable diff：

```python
removed_pairs = []
added_pairs = []

for E in sorted(B_stable):
    old_twists = T_old.get(E, set())
    new_twists = T_new.get(E, set())

    for d in old_twists - new_twists:
        removed_pairs.append((E, d))

    for d in new_twists - old_twists:
        added_pairs.append((E, d))
```

upstream：

```python
upstream_removed_pairs = []

for E in sorted(B_removed):
    for d in T_old.get(E, set()):
        upstream_removed_pairs.append((E, d))
```

newbase：

```python
newbase_pairs = []

for E in sorted(B_added):
    for d in T_new.get(E, set()):
        newbase_pairs.append((E, d))
```

---

# 23. 推薦加入 deterministic reproducibility

所有輸出都：

```text
UTF-8
stable sorted order
explicit column order
no locale-dependent formatting
```

建議 run 結尾生成：

```text
results_sha256.json
```

記錄所有結果檔案 SHA256。

這樣後續雲端／本地 AI 可以確認分析的是同一份 census。

---

# 24. Completion Gate

只有下面全部 PASS，才能標記：

```text
v0.5 EXACT CENSUS COMPLETE
```

Checklist：

```text
[ ] old/current exact commit SHA recorded
[ ] 4 giant raw inputs locally materialized
[ ] 4 raw SHA256 recorded
[ ] base files fully parsed
[ ] twist files fully parsed
[ ] base set partitions exact
[ ] removed curve failure census complete
[ ] Algorithm1 unexplained removed = 0
[ ] upstream twist removals isolated
[ ] stable-base Algorithm2 removals exact
[ ] stable-base Algorithm2 additions exact
[ ] new-base additions isolated
[ ] stable curves classified into unchanged/shrink/expand/mixed
[ ] global twist accounting identity exact PASS
[ ] CSV + JSON + MD report generated
[ ] result hashes generated
```

---

# 25. 本地 AI 完成後回傳的最小資料

後續交回雲端時，不一定需要立刻傳 giant raw files。

最少回傳：

```text
summary.json
V0_5_EXACT_CENSUS_REPORT.md
algorithm1_removed_census.csv
algorithm1_unexplained_removed.csv
algorithm2_stable_curve_census.csv
algorithm2_removed_twists.csv
algorithm2_added_twists.csv
raw_file_manifest.json
```

如果容量允許，再附：

```text
twists_removed_by_upstream_base_deletion.csv
base_removed.csv
base_added.csv
results_sha256.json
```

最好整包：

```text
v0_5_exact_census_results.zip
```

---

# 26. 後續研究接口

v0.5 完成後，下一輪不再研究「Git 改了多少行」，而直接研究：

## A. Algorithm1

新 gate 在 500K universe 裡實際排除了哪些 arithmetic families？

## B. Algorithm2

新的 twist selection rule 是：

```text
純縮減
純擴張
還是 replacement / reclassification
```

以及 change 是否集中在某些 arithmetic structures。

## C. Semantic verification

將 exact census 反向對照 source-code conditional branches，確認：

$$
\text{code delta}
\leftrightarrow
\text{entry delta}
$$

是否逐類吻合。

這才是從「版本 diff」正式提升為：

$$
\boxed{
\text{Semantic Delta Census}
}
$$

---

# 27. 一句話交接

> **先把 old/current 四個 500K giant outputs 真正 checkout 出來；base curves 做 exact set diff，4062 removed curves 做 3/5/7-isogeny 與 $|a_3|=3$ failure census；twists 只在 stable base domain 比較 Algorithm2，upstream base deletion 的 twists 必須另外剝離；最後用 exact integer accounting identity 做閉合。任何 unexplained removed curve 或 accounting mismatch 都視為 v0.5 尚未完成。**

---

**交接狀態：READY FOR LOCAL EXECUTION**
