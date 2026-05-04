# 第1章开篇 DeepSeek 样章重写 Goal

创建时间：2026-05-04
状态：in_progress

## Goal

把《我给中本聪送外卖》的重写优化变成可持续流程：先用 `deepseek-v4-pro` 生成第1章开篇样章，再由 GPT 做二次改写，最后用统一评分表比较“原文 / DeepSeek 版 / GPT 再改写版”，决定是否把该方法扩展到全书。

## 当前执行范围

- 不覆盖 `我给中本聪送外卖/正文/01_中本聪下单了.md`。
- DeepSeek 样章输出到本地草稿：`我给中本聪送外卖/草稿/deepseek_rewrite/01_开篇样章_deepseek.md`。
- GPT 再改写版后续输出到本地草稿：`我给中本聪送外卖/草稿/deepseek_rewrite/01_开篇样章_gpt再改写.md`。
- 评分对比报告后续输出到：`我给中本聪送外卖/设定/结构/章节评分/01_开篇样章三版对比.md`。

## 安全配置

- 真实 API key 只写入本地 `.env.deepseek`，该文件被 `.gitignore` 的 `.env.*` 规则忽略。
- 仓库只提交脚本、模板、计划和评分报告，不提交密钥和模型原始草稿，除非后续明确决定把某一版纳入正文。
- 默认配置：
  - `DEEPSEEK_BASE_URL=https://key.bigsong.site/v1`
  - `DEEPSEEK_MODEL=deepseek-v4-pro`

## 执行步骤

1. 配置 DeepSeek 环境变量：
   - 运行 `scripts/configure_deepseek_env.sh`
   - 按提示输入 API key，脚本会写入 `.env.deepseek`
2. 生成 DeepSeek 样章：
   - 运行 `python3 scripts/deepseek_rewrite_sample.py`
3. GPT 读取原文和 DeepSeek 样章，做再改写：
   - 强化现实压力、外卖平台压迫感、家庭/债务刺点。
   - 保留中本聪订单的冷感神秘，不写成玄幻外挂。
   - 压低讲解腔，增强动作和物件。
4. 三版评分：
   - 原文
   - DeepSeek 版
   - GPT 再改写版
5. 决策：
   - 如果 GPT 再改写版综合分高于原文 0.5 分以上，进入第1-3章开篇重写。
   - 如果只在钩子/节奏上提升，采用局部嫁接，不整章替换。
   - 如果 DeepSeek 版改动破坏人物或规则，只提取句子节奏和冲突密度，不采用设定改动。

## 三版评分模板

| 版本 | facts_terms | chapter_loop | narrative_drive | style_readability | ai_control | soul_moment | continuity_rules | connection_theme | 加权分 | 结论 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 原文开篇 |  |  |  |  |  |  |  |  |  |  |
| DeepSeek 版 |  |  |  |  |  |  |  |  |  |  |
| GPT 再改写版 |  |  |  |  |  |  |  |  |  |  |

## 评估重点

- 第一屏是否有强现实压力。
- “中本聪下单”是否足够早、足够冷、足够抓人。
- 李觉是否仍是普通人，而不是被改成爽文天命主角。
- 是否保留本书核心气质：现实刺点、历史照面、认知改写、现实动作。
- 是否减少解释腔、口号腔和 AI 味。
