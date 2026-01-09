# 部署指南

## 快速部署

一键部署到 GitHub Pages：

```bash
bash deploy.sh
```

## 部署脚本功能

`deploy.sh` 脚本会自动完成以下步骤：

1. ✅ 检查并切换到main分支
2. ✅ 拉取最新代码
3. ✅ 检查必要的工具（Node.js, npm, honkit）
4. ✅ 构建React首页（new-website）
5. ✅ 构建中文版HonKit（zh/）
6. ✅ 构建英文版HonKit（en/）
7. ✅ 组合所有内容到临时目录
8. ✅ 部署到gh-pages分支
9. ✅ 清理临时文件

## 环境要求

在运行部署脚本之前，确保你的系统已安装：

- **Node.js** (推荐 v18+)
- **npm** (随Node.js一起安装)
- **honkit** (全局安装)

### 安装 honkit

```bash
npm install -g honkit
```

### 检查是否已安装

```bash
node --version
npm --version
honkit --version
```

## 手动部署步骤

如果你想手动部署，可以按照以下步骤：

### 1. 构建React首页

```bash
cd new-website
npm install        # 首次需要安装依赖
npm run build      # 构建，输出到 dist/
cd ..
```

### 2. 构建中文版

```bash
cd zh
honkit build       # 构建，输出到 _book/
cd ..
```

### 3. 构建英文版

```bash
cd en
honkit build       # 构建，输出到 _book/
cd ..
```

### 4. 组合并部署

组合所有构建内容并推送到gh-pages分支（参考 deploy.sh 脚本）。

## 网站结构

部署后的网站结构：

```
https://beihaili.github.io/Stories-about-Bitcoin/
├── index.html          # React首页
├── assets/             # React资源文件
├── zh/                 # 中文版HonKit
│   ├── index.html
│   ├── 00_引子：一束照进现实的理想之光.html
│   ├── 01_创世纪：哈耶克的预言.html
│   └── ...
├── en/                 # 英文版HonKit
│   ├── index.html
│   └── ...
├── img/                # 原始图片
├── img_800px/          # 优化图片(800px)
└── img_webp/           # WebP格式图片
```

## 常见问题

### Q: 部署失败怎么办？

A: 检查以下几点：
1. 确保你有GitHub仓库的推送权限
2. 确保所有必要的工具都已安装
3. 查看终端错误信息，根据提示修复

### Q: 如何只构建不部署？

A: 可以分别运行构建命令，不运行部署脚本：

```bash
# 只构建React首页
cd new-website && npm run build

# 只构建中文版
cd zh && honkit build

# 只构建英文版
cd en && honkit build
```

### Q: 如何本地预览？

A:

**预览React首页：**
```bash
cd new-website
npm run dev
# 访问 http://localhost:5173
```

**预览中文版HonKit：**
```bash
cd zh
honkit serve
# 访问 http://localhost:4000
```

**预览英文版HonKit：**
```bash
cd en
honkit serve
# 访问 http://localhost:4000
```

### Q: 修改内容后需要重新部署吗？

A: 是的。修改以下内容后需要重新运行 `bash deploy.sh`：

- React首页源代码（new-website/src/）
- 中文章节内容（zh/*.md）
- 英文章节内容（en/*.md）
- 图片资源（img/）

## 部署时间线

正常情况下，部署流程耗时：

- 构建React首页：~10秒
- 构建中文版：~3秒
- 构建英文版：~3秒
- 推送到GitHub：~5秒
- **GitHub Pages刷新：1-5分钟**

总计：~2-6分钟后网站更新生效

## 技术栈

- **React首页**: React 19 + Vite 7 + Tailwind CSS + Framer Motion
- **章节页面**: HonKit (GitBook fork)
- **部署**: GitHub Pages (gh-pages分支)
- **CI/CD**: 手动部署（运行 deploy.sh）

## 许可证

MIT License

---

如有问题，请访问：
- GitHub: https://github.com/beihaili/Stories-about-Bitcoin
- Twitter: https://twitter.com/bhbtc1337
