#!/bin/bash

# 更新GitHub Pages脚本
# 使用方法: bash deploy-gh-pages.sh [提交信息]

# 如果没有提供提交信息，使用默认信息
COMMIT_MSG=${1:-"Update GitHub Pages content"}

# 确保我们在主分支上
git checkout main

# 确保本地代码是最新的
echo "正在拉取最新代码..."
git pull origin main

# 将所有更改添加到暂存区
echo "正在暂存更改..."
git add .

# 提交更改
echo "正在提交更改: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# 推送到GitHub
echo "正在推送到GitHub..."
git push origin main

echo "GitHub Pages已更新!"
echo "请访问 https://beihaili.github.io/Stories-about-Bitcoin/ 查看效果"
