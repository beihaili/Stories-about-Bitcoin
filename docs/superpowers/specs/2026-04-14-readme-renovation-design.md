# README 门面改造 设计文档

**日期:** 2026-04-14
**目的:** 将 README 更新到 39 章结构，改造为推广级门面，同时发布 ebook v3.0

## 背景

仓库刚完成章节重构（34→37 章，共 39 个文件），但 README 仍然写着 "36 chapters"，目录链接全部错位。接下来要向 Lopp.net、bitcoinonly.io 等 Bitcoin 社区提交收录，需要专业的"门面"。

## 核心定位

**差异化卖点：文学叙事风格**——"Bitcoin's history, told as literature — not textbook."

## 设计决策

### README 结构：英文在前 + 中文完整镜像（方案 A）

```
=== English ===
1. Hero（标题 + 一句话定位 + badges + 快捷链接）
2. Writing Sample（第三章摘录：雷曼破产→创世区块）
3. Quick Links 表格（精简版，Lightning 在首屏，BTC 全地址移到页底）
4. Table of Contents（折叠，39 章按 9 个 period 概览，不逐章列链接）
5. Contributing（两行，细节留给 CONTRIBUTING.md）
6. Development（代码块，保持现有）
7. Contributors（contrib.rocks）
8. License + 完整捐赠地址

--- 分隔线 ---

=== 中文版 ===
1. 标题
2. 介绍（提及《明朝那些事儿》风格参照，非逐字翻译英文）
3. Writing Sample（同一段的中文原文）
4. Quick Links 表格
5. 目录（折叠，中文版）
6. 参与贡献（精简）
7. 许可证
```

### 写作样本选择

第三章《危机与创世》——雷曼破产 → 政府印钱 → "Chancellor on brink" 被刻入创世区块。

理由：
- 全书最有力的 "hook"，普通人也能理解
- 完美展示文学叙事风格
- 中英文都有对应高质量版本

### CONTRIBUTING.md 更新

- "36 chapters" → "39 chapters"
- "1976-2024" → "1976-2025"

### Ebook v3.0 Release

- 重新构建中英文 PDF + EPUB（37 章版本）
- 发布 GitHub Release v3.0

### CLAUDE.md (in-repo) 更新

- "36 chapters (00-34 + special)" → "39 chapters (00-37 + special)"
- 其他过时引用同步修正

## 不做的事

- 不改 CONTRIBUTING.md 的整体结构（已经足够好）
- 不改网站本身
- 不重新设计 badges
