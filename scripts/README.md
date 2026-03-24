# 📚 比特币那些事儿 - 章节自动生成工具

这个工具可以帮你快速创建新章节的标准格式文档。

## 🚀 功能特性

- ✅ **自动获取实时区块高度**：从多个API源获取当前比特币网络区块高度
- ✅ **智能文件命名**：自动生成标准格式的文件名
- ✅ **难度等级判断**：根据章节名称智能判断难度级别
- ✅ **完整模板生成**：包含所有必需的徽章、引言、导航链接
- ✅ **交互式操作**：友好的命令行界面
- ✅ **编辑器集成**：支持自动打开VS Code、Cursor、Vim等编辑器

## 📦 安装要求

- **系统**：macOS、Linux 或 Windows (WSL)
- **依赖**：`bash`、`curl`（用于获取区块高度）

## 🛠 使用方法

### 基本用法

```bash
# 进入项目根目录
cd 比特币那些事儿本地版

# 创建新章节
./scripts/create_chapter.sh "章节名称"
```

### 使用示例

```bash
# 创建第二章第一节
./scripts/create_chapter.sh "第一批信徒"

# 创建带编号的章节
./scripts/create_chapter.sh "01_两块披萨的传奇"

# 创建技术类章节（会自动设为高级难度）
./scripts/create_chapter.sh "技术详解：挖矿原理"

# 查看帮助信息
./scripts/create_chapter.sh --help
```

## 📁 生成文件格式

脚本会在 `正文/` 目录下生成如下格式的文件：

```
正文/01_第一批信徒.md
```

### 生成的文件包含：

1. **标准头部**
   - 章节标题
   - 状态徽章（草稿/已完成）
   - 作者徽章
   - 日期+区块高度徽章
   - 难度等级徽章

2. **引言模板**
   - 章节简介占位符
   - 社交媒体链接
   - 项目链接

3. **内容框架**
   - 章节开始
   - 三个子部分模板
   - 结语部分

4. **标准尾部**
   - 导航链接
   - 统一格式

## 🎯 智能功能

### 难度等级自动判断

| 关键词 | 难度级别 | 颜色 |
|--------|----------|------|
| 引子、序言、开始、简介 | 初级 | 🟢 绿色 |
| 技术、算法、密码、协议、代码、挖矿、共识 | 高级 | 🔴 红色 |
| 其他 | 中级 | 🟡 黄色 |

### 文件名生成规则

- **输入**: `"第一批信徒"` → **输出**: `01_第一批信徒.md`
- **输入**: `"05_暗网与争议"` → **输出**: `05_暗网与争议.md`
- **输入**: `"技术原理"` → **输出**: `01_技术原理.md`

### 区块高度获取

脚本会尝试从以下API获取实时区块高度：
1. `blockstream.info`
2. `blockchain.info`  
3. `blockcypher.com`

如果所有API都无法访问，会使用默认值。

## 🎨 生成的文件示例

```markdown
# 第一批信徒

![status](https://img.shields.io/badge/状态-草稿-yellow)
![author](https://img.shields.io/badge/作者-beihaili-blue)
![date](https://img.shields.io/badge/日期-2025-01%20block%20906053-orange)
![difficulty](https://img.shields.io/badge/难度-中级-yellow)

> 💡 【请在这里添加本章节的核心内容简介】这里应该用一两句话概括本章节的主要内容和读者将会了解到什么。
> 
> 欢迎关注我的推特：[@bhbtc1337](https://twitter.com/bhbtc1337)
> 
> 进入微信交流群请填表：[表格链接](https://forms.gle/QMBwL6LwZyQew1tX8)
> 
> 文章开源在 GitHub：[Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3)
> 

## 章节开始

【在这里开始写作本章节的内容】

### 第一部分

【添加第一部分内容】

### 第二部分

【添加第二部分内容】

### 第三部分

【添加第三部分内容】

## 结语

【在这里添加本章节的总结】

---

<div align="center">
<a href="https://github.com/beihaili/Get-Started-with-Web3">🏠 返回主页</a> | 
<a href="https://twitter.com/bhbtc1337">🐦 关注作者</a> | 
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 加入交流群</a>
</div>
```

## 🔧 高级功能

### 覆盖现有文件

如果文件已存在，脚本会询问是否覆盖：

```
⚠️  文件已存在：正文/01_第一批信徒.md
是否覆盖？(y/N):
```

### 自动打开编辑器

创建完成后，脚本会询问是否立即编辑：

```
是否立即打开文件编辑？(y/N):
```

支持的编辑器优先级：
1. **VS Code** (`code`)
2. **Cursor** (`cursor`)  
3. **Vim** (`vim`)

### 彩色输出

脚本使用颜色来增强用户体验：
- 🔵 信息提示
- 🟢 成功操作
- 🟡 警告信息  
- 🔴 错误信息

## ❓ 常见问题

### Q: 无法获取区块高度怎么办？
A: 脚本会自动使用默认值，你也可以后续手动更新。

### Q: 如何修改默认模板？
A: 编辑脚本中的 `generate_chapter_template` 函数。

### Q: 能否批量创建章节？
A: 目前不支持，但可以写一个简单的循环脚本调用此工具。

## 🔄 更新章节状态

创建完成并写作完毕后，记得将徽章状态从"草稿"改为"已完成"：

```markdown
![status](https://img.shields.io/badge/状态-已完成-success)
```

---

## 💡 贡献

如果你有改进建议或发现了bug，欢迎提交issue或PR！

**作者**: beihaili  
**项目**: [Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3) 