# 仓库清理与章节重构提交 实施计划

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Stories-about-Bitcoin 仓库的大量未提交变更（章节重构、脚本改进、分支清理）整理并安全提交。

**Architecture:** 按逻辑分组依次提交——先同步远程，再按"章节内容 → 英文翻译 → 图片资源 → 网站/脚本 → gitignore 修复 → 分支清理"的顺序分批 commit，确保每次提交都是原子性的、可回溯的。

**背景:** 仓库经历了一次重大章节重构——新增 3 章（27 闪电降临、30 多米诺崩塌、32 铭文风暴），全书从 34 章扩展到 37 章，涉及正文/、en/、img/、网站数据等全面重新编号。

---

### Task 1: 同步远程 main

**目的:** 本地 main 落后 origin/main 4 个 commit，需要先拉取。

- [ ] **Step 1: 拉取远程更新**

```bash
cd /Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin
git pull origin main
```

Expected: Fast-forward merge，拉取 ParticleBackground.test.jsx 和 TypewriterQuotes.test.jsx 的更新。

- [ ] **Step 2: 验证同步成功**

```bash
git log --oneline -3
```

Expected: 最新 commit 应该是远程的 merge commit。

---

### Task 2: 提交章节重构（正文/）

**目的:** 这是核心变更——3 章新增 + 全面重新编号。

**Files:**
- Delete (tracked): `正文/27_未来可期：萨尔瓦多先驱.md` 到 `正文/34_未来可期：光未熄灭.md`（8 个旧文件）
- Create (untracked): `正文/27_西装革命：闪电降临.md` 到 `正文/37_未来可期：光未熄灭.md`（11 个新文件）
- Modify: `正文/11_风起云涌：第一次泡沫.md`（内容优化）

- [ ] **Step 1: Stage 正文/ 所有变更**

```bash
git add 正文/11_风起云涌：第一次泡沫.md
git add 正文/27_西装革命：闪电降临.md
git add 正文/28_未来可期：萨尔瓦多先驱.md
git add 正文/29_未来可期：地缘政治新变量.md
git add 正文/30_未来可期：多米诺崩塌.md
git add 正文/31_未来可期：信任再次破碎.md
git add 正文/32_未来可期：铭文风暴.md
git add 正文/33_未来可期：ETF历史性突破.md
git add 正文/34_未来可期：大选与战略储备.md
git add 正文/35_未来可期：十万美元突破.md
git add 正文/36_未来可期：缺席的人.md
git add 正文/37_未来可期：光未熄灭.md
# Stage deletions of old files
git add 正文/27_未来可期：萨尔瓦多先驱.md
git add 正文/28_未来可期：地缘政治新变量.md
git add 正文/29_未来可期：信任再次破碎.md
git add 正文/30_未来可期：ETF历史性突破.md
git add 正文/31_未来可期：大选与战略储备.md
git add 正文/32_未来可期：十万美元突破.md
git add 正文/33_未来可期：缺席的人.md
git add 正文/34_未来可期：光未熄灭.md
```

- [ ] **Step 2: 验证 staging 正确**

```bash
git diff --cached --stat
```

Expected: 应该只看到正文/ 目录下的文件变更。

- [ ] **Step 3: Commit**

```bash
git commit -m "feat(正文): 章节重构——新增3章，全书扩展至37章

新增章节：
- 27_西装革命：闪电降临（闪电网络发展史）
- 30_未来可期：多米诺崩塌（Luna/3AC/FTX 连环崩盘）
- 32_未来可期：铭文风暴（Ordinals 与 BRC-20）

原27-34章重新编号为28-37章，内容不变。
同时优化了第11章（第一次泡沫）的内容。"
```

---

### Task 3: 提交英文翻译重构（en/）

**Files:**
- Delete (tracked): `en/27_future_promise_the_el_salvador_pioneer.md` 到 `en/34_future_promise_the_light_still_burns.md`（8 个旧文件）
- Create (untracked): `en/27_suit_revolution_lightning_strikes.md` 到 `en/37_future_promise_the_light_still_burns.md`（11 个新文件）
- Modify: `en/SUMMARY.md`

- [ ] **Step 1: Stage en/ 所有变更**

```bash
# 新文件
git add en/27_suit_revolution_lightning_strikes.md
git add en/28_future_promise_the_el_salvador_pioneer.md
git add en/29_future_promise_the_new_geopolitical_variable.md
git add en/30_future_promise_the_domino_collapse.md
git add en/31_future_promise_trust_shattered_again.md
git add en/32_future_promise_the_inscription_storm.md
git add en/33_future_promise_the_historic_etf_breakthrough.md
git add en/34_future_promise_the_election_and_strategic_reserve.md
git add en/35_future_promise_the_100k_breakthrough.md
git add en/36_future_promise_the_absent_ones.md
git add en/37_future_promise_the_light_still_burns.md
# 旧文件删除 + SUMMARY
git add en/27_future_promise_the_el_salvador_pioneer.md
git add en/28_future_promise_the_new_geopolitical_variable.md
git add en/29_future_promise_trust_shattered_again.md
git add en/30_future_promise_the_historic_etf_breakthrough.md
git add en/31_future_promise_the_election_and_strategic_reserve.md
git add en/32_future_promise_the_100k_breakthrough.md
git add en/33_future_promise_the_absent_ones.md
git add en/34_future_promise_the_light_still_burns.md
git add en/SUMMARY.md
```

- [ ] **Step 2: Commit**

```bash
git commit -m "feat(en): 英文翻译同步章节重构，新增3章翻译

对齐正文/章节重构：
- 新增 ch27 Lightning Strikes, ch30 Domino Collapse, ch32 Inscription Storm
- 原27-34重新编号为28-37
- 更新 SUMMARY.md 目录"
```

---

### Task 4: 提交图片资源重新编号

**Files:**
- `img/27.png` 到 `img/34.png`：重新编号 + 新增 35-37
- `img/ch27.png` 到 `img/ch37.png`：重新编号 + 新增 35-37
- `img_800px/ch27.png` 到 `img_800px/ch37.png`：同上
- `img_webp/ch27.webp` 到 `img_webp/ch37.webp`：同上

- [ ] **Step 1: Stage 所有图片变更**

```bash
git add img/27.png img/28.png img/29.png img/30.png img/31.png img/32.png img/33.png img/34.png
git add img/35.png img/36.png img/37.png
git add img/ch27.png img/ch28.png img/ch29.png img/ch30.png img/ch31.png img/ch32.png img/ch33.png img/ch34.png
git add img/ch35.png img/ch36.png img/ch37.png
git add img_800px/ch27.png img_800px/ch28.png img_800px/ch29.png img_800px/ch30.png img_800px/ch31.png img_800px/ch32.png img_800px/ch33.png img_800px/ch34.png
git add img_800px/ch35.png img_800px/ch36.png img_800px/ch37.png
git add img_webp/ch27.webp img_webp/ch28.webp img_webp/ch29.webp img_webp/ch30.webp img_webp/ch31.webp img_webp/ch32.webp img_webp/ch33.webp img_webp/ch34.webp
git add img_webp/ch35.webp img_webp/ch36.webp img_webp/ch37.webp
```

- [ ] **Step 2: Commit**

```bash
git commit -m "assets(img): 图片资源重新编号，新增ch35-37配图

配合章节重构，所有 img/、img_800px/、img_webp/ 下的
ch27-ch34 图片重新编号为 ch27-ch37。"
```

---

### Task 5: 提交网站数据和脚本改进

**Files:**
- Modify: `new-website/src/data/chapters.js`（章节数据更新至 37 章）
- Modify: `scripts/build_ebook.py`（图片查找逻辑优化）
- Modify: `scripts/overnight/run_overnight.sh`（认证预检、日志改进）
- Modify: `ebook/metadata-en.yaml`（年份更新）
- Create: `scripts/make_cover.py`（封面图生成脚本）

- [ ] **Step 1: Stage 文件**

```bash
git add new-website/src/data/chapters.js
git add scripts/build_ebook.py
git add scripts/overnight/run_overnight.sh
git add scripts/make_cover.py
git add ebook/metadata-en.yaml
```

- [ ] **Step 2: Commit**

```bash
git commit -m "chore: 更新网站数据、脚本改进、新增封面工具

- chapters.js 对齐37章新结构
- build_ebook.py 优先使用 chNN.png 格式图片
- run_overnight.sh 增加认证预检和系统通知
- make_cover.py 新增封面图文字生成脚本
- metadata-en.yaml 年份更新至2026"
```

---

### Task 6: 修复 .gitignore 并清理运行时产物

**目的:** `scripts/overnight/logs/` 和 `scripts/overnight/runs/` 是运行时产物，不应进入仓库。`docs/superpowers/` 是 brainstorming 产物，决定是否保留。

**Files:**
- Modify: `.gitignore`
- Ignore: `scripts/overnight/logs/`, `scripts/overnight/runs/`

- [ ] **Step 1: 在 .gitignore 末尾添加规则**

在 `.gitignore` 的 Python 部分之前添加：

```
# Overnight 运行时产物
scripts/overnight/logs/
scripts/overnight/runs/
```

- [ ] **Step 2: Stage 并 commit**

```bash
git add .gitignore
git commit -m "chore(gitignore): 忽略 overnight 运行时日志和记录"
```

---

### Task 7: 清理已合并分支

**目的:** 清理本地和远程的废旧分支。

**本地已合并分支:**
- `phase3.5/repo-merge`

**远程已合并分支:**
- `origin/overnight/round-1-no-test-file-for-achievementto`
- `origin/overnight/round-2-no-test-file-for-typewriterquo`（未在 merged 列表但也是 overnight 旧分支）
- `origin/overnight/round-1-eslint-errors-in-particlebackg`（同上）
- `origin/overnight/round-3-no-test-file-for-errorboundary`
- `origin/overnight/round-3-no-test-file-for-particlebackg`
- `origin/overnight/round-4-no-test-file-for-giscuscomment`
- `origin/overnight/round-5-no-test-file-for-figuresgaller`
- `origin/overnight/round-7-no-test-file-for-timelinejsx`
- `origin/phase3.5/repo-merge`

- [ ] **Step 1: 删除本地已合并分支**

```bash
git branch -d phase3.5/repo-merge
```

- [ ] **Step 2: 删除远程已合并分支**

```bash
git push origin --delete overnight/round-1-no-test-file-for-achievementto
git push origin --delete overnight/round-2-no-test-file-for-typewriterquo
git push origin --delete overnight/round-1-eslint-errors-in-particlebackg
git push origin --delete overnight/round-3-no-test-file-for-errorboundary
git push origin --delete overnight/round-3-no-test-file-for-particlebackg
git push origin --delete overnight/round-4-no-test-file-for-giscuscomment
git push origin --delete overnight/round-5-no-test-file-for-figuresgaller
git push origin --delete overnight/round-7-no-test-file-for-timelinejsx
git push origin --delete phase3.5/repo-merge
```

- [ ] **Step 3: 验证清理完成**

```bash
git branch -a
```

Expected: 只剩 `main`、`gh-pages` 和对应的 remotes。

---

### Task 8: 重新构建 zh/ 并推送到远程

- [ ] **Step 1: 运行 build-zh 重新生成**

```bash
make build-zh
```

Expected: zh/ 目录下的文件应该更新到 37 章。

- [ ] **Step 2: 推送所有 commit 到远程**

```bash
git push origin main
```

- [ ] **Step 3: 最终验证**

```bash
git status
git log --oneline -8
```

Expected: 工作目录干净（除了 gitignored 的文件），commit 历史清晰。
