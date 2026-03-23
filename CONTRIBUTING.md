# Contributing | 贡献指南

[English](#english) | [中文](#中文)

---

## English

Thank you for your interest in contributing to **Stories about Bitcoin**! This project tells Bitcoin's 48-year history in an engaging web novel style.

### Ways to Contribute

- **Report Bugs** — Found a broken link, typo, or rendering issue? [Open a bug report](https://github.com/beihaili/Stories-about-Bitcoin/issues/new?template=bug_report.yml)
- **Suggest Features** — Have an idea for the website or ebook? [Open a feature request](https://github.com/beihaili/Stories-about-Bitcoin/issues/new?template=feature_request.yml)
- **Submit a PR** — Fix a bug, improve the UI, or add translations
- **Improve Content** — Correct historical facts, improve writing, or add references

### Development Setup

```bash
# Prerequisites: Node.js 20+
git clone https://github.com/beihaili/Stories-about-Bitcoin.git
cd Stories-about-Bitcoin/new-website
npm install
npm run dev       # Start dev server at localhost:5173
npm run test:run  # Run tests
npm run build     # Production build
npm run lint      # ESLint check
```

### Project Structure

```
Stories-about-Bitcoin/
├── new-website/          # React SPA homepage (Vite + Tailwind)
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── data/         # Chapter data
│   │   └── test/         # Test utilities & mocks
│   └── public/           # Static assets (feed.xml, robots.txt, etc.)
├── zh/                   # Chinese ebook (HonKit markdown)
├── en/                   # English ebook (HonKit markdown)
└── img/                  # Chapter images
```

### Code Standards

- **Linting**: ESLint with React + Hooks plugins. Run `npm run lint` before committing.
- **Testing**: Vitest + React Testing Library. Aim to add tests for new components.
- **Commits**: Use clear, descriptive commit messages in English.
- **Components**: Follow existing patterns — `lang` prop for i18n, `{ zh, en }` data objects.
- **Styling**: Tailwind CSS with custom tokens (`bitcoin-orange`, `bitcoin-gold`, `historical-parchment`).

### Pull Request Process

1. Fork the repo and create a feature branch from `main`
2. Make your changes, add tests if applicable
3. Ensure `npm run lint` and `npm run test:run` pass
4. Ensure `npm run build` succeeds
5. Open a PR with a clear description of changes

---

## 中文

感谢你有兴趣为 **比特币那些事儿** 做贡献！本项目以网文笔法讲述比特币 48 年历史。

### 贡献方式

- **报告 Bug** — 发现坏链接、错别字或渲染问题？[提交 Bug 报告](https://github.com/beihaili/Stories-about-Bitcoin/issues/new?template=bug_report.yml)
- **建议功能** — 对网站或电子书有想法？[提交功能请求](https://github.com/beihaili/Stories-about-Bitcoin/issues/new?template=feature_request.yml)
- **提交 PR** — 修复 Bug、改进 UI 或添加翻译
- **改进内容** — 修正历史事实、改善文笔或添加参考资料

### 开发环境

```bash
# 前提：Node.js 20+
git clone https://github.com/beihaili/Stories-about-Bitcoin.git
cd Stories-about-Bitcoin/new-website
npm install
npm run dev       # 启动开发服务器 localhost:5173
npm run test:run  # 运行测试
npm run build     # 生产构建
npm run lint      # ESLint 检查
```

### 代码规范

- **代码检查**：ESLint，提交前运行 `npm run lint`
- **测试**：Vitest + React Testing Library，新组件请添加测试
- **提交信息**：清晰描述性的英文提交信息
- **组件规范**：遵循现有模式 — `lang` prop 用于国际化，`{ zh, en }` 数据对象
- **样式**：Tailwind CSS，使用项目自定义 token

### PR 流程

1. Fork 仓库，从 `main` 创建功能分支
2. 进行修改，如适用请添加测试
3. 确保 `npm run lint` 和 `npm run test:run` 通过
4. 确保 `npm run build` 成功
5. 提交 PR，清晰描述变更内容
