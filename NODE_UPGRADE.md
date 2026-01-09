# Node.js 升级说明

## ✅ 已完成的升级

你的开发环境已经成功升级到 Node.js 20！

- **旧版本**: Node.js 18.17.0 + npm 9.6.7
- **新版本**: Node.js 20.19.6 + npm 10.8.2

## 🔧 自动加载配置

为了确保每次打开终端都自动使用 Node.js 20，请按照以下步骤配置：

### 对于 Zsh (macOS 默认)

编辑 `~/.zshrc` 文件，添加以下内容：

```bash
# 加载 nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

然后重新加载配置：

```bash
source ~/.zshrc
```

### 对于 Bash

编辑 `~/.bashrc` 或 `~/.bash_profile` 文件，添加相同的内容，然后：

```bash
source ~/.bashrc
# 或
source ~/.bash_profile
```

### 验证配置

重新打开终端，运行：

```bash
node --version
# 应该显示: v20.19.6

npm --version
# 应该显示: 10.8.2
```

## 📦 已安装的全局包

已为 Node.js 20 重新安装以下全局包：

- **honkit** v6.1.4 - GitBook构建工具

## 🚀 部署脚本已更新

`deploy.sh` 脚本已更新，会自动使用 Node.js 20，无需手动配置。

## 🎯 日常使用

### 构建项目时

现在构建 React 项目时不会再看到 Node.js 版本警告：

```bash
cd new-website
npm install
npm run build
```

### 运行部署脚本

直接运行即可，脚本会自动使用正确的 Node.js 版本：

```bash
bash deploy.sh
```

## 🔄 版本管理

### 查看已安装的 Node.js 版本

```bash
nvm list
```

### 切换版本 (如果需要)

```bash
# 切换到 Node.js 20
nvm use 20

# 切换到其他版本
nvm use 18
```

### 安装其他版本 (如果需要)

```bash
# 安装最新的 LTS 版本
nvm install --lts

# 安装特定版本
nvm install 22
```

## ⚙️ 常见问题

### Q: 为什么新终端中还是显示旧版本？

A: 需要在 shell 配置文件中添加 nvm 加载脚本（见上方"自动加载配置"）。

### Q: 如何卸载旧版本？

A:
```bash
nvm uninstall 18.17.0
```

### Q: 部署时出现 Node.js 版本相关错误怎么办？

A:
1. 确认 deploy.sh 已更新（包含 nvm 加载代码）
2. 手动运行 `nvm use 20` 确认可以切换
3. 如果还有问题，重新运行：
   ```bash
   nvm install 20
   npm install -g honkit
   ```

## 📝 技术细节

### 为什么需要升级？

项目依赖的一些包（特别是 Vite、React Router 等）要求 Node.js 20+：

- **Vite 7.x**: 要求 Node.js 20.19+ 或 22.12+
- **React Router 7.x**: 要求 Node.js 20+
- **ESLint 9.x**: 要求 Node.js 18.18+

### Node.js 20 的优势

- 更好的性能
- 更新的 V8 引擎
- 改进的 npm (v10)
- 更好的 ES Module 支持
- 长期支持（LTS）直到 2026年4月

---

升级完成！现在可以享受更快、更稳定的开发体验了 🎉
