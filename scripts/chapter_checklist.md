# 章节质量检查清单

每个章节发布前，请逐项检查以下内容。

---

## 格式检查

### 必需元素
- [ ] **H1标题**：章节标题使用单个 `#`
- [ ] **状态徽章**：`![status](https://img.shields.io/badge/状态-已完成-success)`
- [ ] **作者徽章**：`![author](https://img.shields.io/badge/作者-beihaili-blue)`
- [ ] **日期徽章**：包含区块高度，格式：`日期-YYYY--MM%20block%20HEIGHT`
- [ ] **难度徽章**：初级(green) / 中级(yellow) / 高级(red)
- [ ] **核心内容简介**：`> 💡 【核心内容简介】...`
- [ ] **社交链接**：推特、微信群、GitHub 链接

### 结尾元素
- [ ] **趣味小知识**：格式 `*[有趣的历史细节]*`
- [ ] **页脚链接**：返回主页 | 关注作者 | 加入交流群

### 格式示例
```markdown
# 章节标题

![status](https://img.shields.io/badge/状态-已完成-success)
![author](https://img.shields.io/badge/作者-beihaili-blue)
![date](https://img.shields.io/badge/日期-2025--01%20block%20880000-orange)
![difficulty](https://img.shields.io/badge/难度-中级-yellow)

> 💡 【核心内容简介】...

[正文内容...]

---

*[趣味小知识]*

---

<div align="center">
<a href="https://github.com/beihaili/Get-Started-with-Web3">🏠 返回主页</a> |
<a href="https://twitter.com/bhbtc1337">🐦 关注作者</a> |
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 加入交流群</a>
</div>
```

---

## 内容检查

### 叙事质量
- [ ] **具体人物**：有名有姓的人物出场
- [ ] **具体日期**：关键事件有明确时间
- [ ] **人物对话**：包含对话或引用
- [ ] **故事性**：以叙事方式展开，而非事件罗列
- [ ] **情感共鸣**：读者能感受到人物的喜怒哀乐

### 史料运用
- [ ] **原文引用**：邮件、论坛帖子等原始资料
- [ ] **引用标注**：标明引用来源
- [ ] **事实准确**：重要历史事实经过验证
- [ ] **多元视角**：包含支持者和质疑者观点

### 技术准确性
- [ ] **术语正确**：技术术语使用准确
- [ ] **解释清晰**：复杂概念有通俗解释
- [ ] **数据核实**：价格、日期、数量等数据准确

---

## 难度等级判断

| 关键词 | 难度 | 颜色 |
|--------|------|------|
| 引子、序言、开始、简介 | 初级 | green |
| 一般叙事内容 | 中级 | yellow |
| 技术、算法、密码、协议、代码、挖矿、共识 | 高级 | red |

---

## 发布流程

1. **完成检查清单**所有项目
2. **更新状态徽章**为"已完成"
3. **更新正文/README.md**添加新章节
4. **移动草稿版本**到 `正文/历史版本/` 目录

---

## 快速检查命令

```bash
# 检查徽章是否完整
head -10 章节文件.md | grep -E "(status|author|date|difficulty)"

# 检查页脚是否存在
tail -10 章节文件.md | grep "返回主页"

# 检查趣味小知识
grep -E "^\*\[" 章节文件.md
```
