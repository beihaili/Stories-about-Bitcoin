# Stories about Bitcoin - Official Website 🪙

这是《比特币那些事儿》的全新官方网站，采用叙事沉浸式设计，为读者呈现完整的比特币历史画卷。

## ✨ 特性

- 📖 **叙事沉浸式设计** - 像翻开一本历史书
- ⏳ **交互式时间轴** - 串联25个重要历史事件
- 📚 **精美章节卡片** - 1976-2025年、39章、9个时期完整展示
- 👥 **关键人物画廊** - 10位传奇人物介绍
- 🌐 **双语支持** - 中文/English无缝切换
- 🎨 **Bitcoin Orange主题** - 温暖的金色调设计
- ⚡ **Framer Motion动画** - 流畅的页面过渡效果
- 📱 **响应式设计** - 完美适配所有设备

## 🛠️ 技术栈

- **框架**: React 18 + Vite 7
- **样式**: Tailwind CSS
- **动画**: Framer Motion
- **路由**: React Router v6
- **国际化**: react-i18next
- **图标**: React Icons
- **部署**: Vercel

## 🚀 快速开始

### 环境要求

⚠️ **重要**: 需要 Node.js 20.19+ 或 22.12+（Vite 7 要求）

### 安装依赖

```bash
npm install
```

### 开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 📦 部署到 Vercel

### 方法一：一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/beihaili/Stories-about-Bitcoin/tree/main/new-website)

### 方法二：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录 Vercel
vercel login

# 部署
vercel

# 生产部署
vercel --prod
```

### 方法三：通过 Git 集成

1. 将代码推送到 GitHub/GitLab/Bitbucket
2. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
3. 点击 "Import Project"
4. 选择你的仓库
5. Vercel 会自动检测 Vite 配置
6. 点击 "Deploy"

## 📁 项目结构

```
new-website/
├── public/                      # 静态资源
├── src/
│   ├── components/
│   │   ├── common/              # 通用组件
│   │   │   └── LanguageSwitcher.jsx
│   │   └── home/                # 首页组件
│   │       ├── Hero.jsx         # 英雄区
│   │       ├── Timeline.jsx     # 交互式时间轴
│   │       ├── ChapterCard.jsx  # 章节卡片
│   │       ├── ChapterGrid.jsx  # 章节网格
│   │       └── FiguresGallery.jsx  # 人物画廊
│   ├── data/                    # 数据文件
│   │   ├── chapters.js          # 39章节数据
│   │   ├── figures.js           # 10人物数据
│   │   └── timeline.js          # 25事件数据
│   ├── App.jsx                  # 主应用
│   ├── main.jsx                 # 入口
│   └── index.css                # 全局样式
├── tailwind.config.js           # Tailwind配置
├── postcss.config.js            # PostCSS配置
├── vercel.json                  # Vercel部署配置
└── package.json
```

## 🎨 设计系统

### 颜色主题

```javascript
Bitcoin Orange: #F7931A  // 主色调
Gold:           #FFD700  // 强调色
Dark Gold:      #B8860B  // 深色金
Light Gold:     #FFF8DC  // 浅色金
Parchment:      #F4ECD8  // 羊皮纸
Sepia:          #704214  // 棕褐色
Antique:        #8B7355  // 古典色
```

### 字体系统

- **衬线字体**: Georgia, Cambria, Times New Roman (正文和标题)
- **无衬线字体**: Inter, system-ui (界面元素)

## 📊 数据文件说明

### chapters.js - 章节数据

包含39章完整元数据，分为9个时期：
- 序言
- 创世纪 (1976-2009)
- 初出茅庐 (2009-2010)
- 风起云涌 (2011-2012)
- 暗潮汹涌 (2013-2016)
- 内战与独立 (2017)
- 西装革命 (2018-2021)
- 未来可期 (2021-2025)
- 特别篇

### figures.js - 人物数据

10位关键人物：
- 哈耶克 (货币理论先驱)
- 大卫·乔姆 (数字现金之父)
- 中本聪 (比特币创造者)
- 哈尔·芬尼 (第一个信徒)
- 加文·安德烈森 (首席开发者)
- 罗杰·沃 (比特币耶稣)
- 罗斯·乌布利希 (丝绸之路创始人)
- 温克莱沃斯兄弟 (机构投资先驱)
- 迈克尔·塞勒 (企业比特币化先驱)
- 纳伊布·布克尔 (比特币法币化先驱)

### timeline.js - 时间轴数据

25个重要历史事件，包含：
- 事件类别：理论、技术、商业、社区、监管、危机等
- 重要性级别：关键、重要、一般

## 🌐 国际化

当前支持：
- 🇨🇳 简体中文 (zh)
- 🇬🇧 English (en)

语言切换器位于页面右上角，实时切换所有内容。

## 🚧 后续计划

- [ ] 章节详情页（阅读器）
- [ ] 阅读进度追踪
- [ ] 全文搜索功能
- [ ] PDF下载集成
- [ ] 评论系统
- [ ] SEO优化
- [ ] 性能优化
- [ ] 更多语言支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 原项目: [beihaili/Stories-about-Bitcoin](https://github.com/beihaili/Stories-about-Bitcoin)
- 设计灵感: 《明朝那些事儿》
- 技术栈: React, Vite, Tailwind CSS, Framer Motion

## 📧 联系方式

- GitHub: [@beihaili](https://github.com/beihaili)
- Twitter: [@bhbtc1337](https://twitter.com/bhbtc1337)

---

Made with ❤️ and React · © 2024 Stories about Bitcoin
