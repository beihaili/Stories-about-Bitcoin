#!/bin/bash

# 比特币那些事儿 - 完整部署脚本
# 部署React首页 + 中英文HonKit到GitHub Pages
# 作者: beihaili
# 用法: bash deploy.sh

set -e  # 遇到错误立即退出

# 加载nvm并使用Node 20
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 20 > /dev/null 2>&1 || nvm use default > /dev/null 2>&1

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_step() {
    echo -e "${BLUE}👉 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 获取脚本所在目录（项目根目录）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "🚀 开始部署 比特币那些事儿 到 GitHub Pages"
echo "============================================================"
echo ""

# 1. 确保在main分支
print_step "确保在main分支..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "当前在分支 $CURRENT_BRANCH，切换到main分支"
    git checkout main
fi
print_success "已在main分支"

# 2. 拉取最新代码
print_step "拉取最新代码..."
git pull origin main
print_success "代码已更新"

# 3. 检查必要的工具
print_step "检查必要的工具..."

if ! command -v node &> /dev/null; then
    print_error "Node.js 未安装，请先安装 Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm 未安装，请先安装 npm"
    exit 1
fi

if ! command -v honkit &> /dev/null; then
    print_error "honkit 未安装，请运行: npm install -g honkit"
    exit 1
fi

print_success "所有必要工具已就绪"

# 4. 构建React首页
print_step "构建React首页..."
cd "$SCRIPT_DIR/new-website"

# 检查依赖是否已安装
if [ ! -d "node_modules" ]; then
    print_warning "node_modules不存在，安装依赖..."
    npm install
fi

# 构建
npm run build

if [ ! -d "dist" ]; then
    print_error "React构建失败，dist目录不存在"
    exit 1
fi

print_success "React首页构建完成"

# 5. 构建中文版HonKit
print_step "构建中文版HonKit..."
cd "$SCRIPT_DIR/zh"
honkit build

if [ ! -d "_book" ]; then
    print_error "中文版构建失败"
    exit 1
fi

print_success "中文版构建完成"

# 6. 构建英文版HonKit
print_step "构建英文版HonKit..."
cd "$SCRIPT_DIR/en"
honkit build

if [ ! -d "_book" ]; then
    print_error "英文版构建失败"
    exit 1
fi

print_success "英文版构建完成"

# 7. 创建临时目录并组合所有内容
print_step "组合所有构建内容..."
cd "$SCRIPT_DIR"

TEMP_DIR=$(mktemp -d)
echo "📁 临时目录: $TEMP_DIR"

# 复制React首页到根目录
cp -r new-website/dist/* "$TEMP_DIR/"
print_success "React首页已复制到根目录"

# 复制中文版HonKit
cp -r zh/_book "$TEMP_DIR/zh"
print_success "中文版已复制到 zh/"

# 复制英文版HonKit
cp -r en/_book "$TEMP_DIR/en"
print_success "英文版已复制到 en/"

# 复制图片资源
for img_dir in img img_800px img_webp; do
    if [ -d "$img_dir" ]; then
        cp -r "$img_dir" "$TEMP_DIR/"
        print_success "${img_dir}/ 已复制"
    fi
done

# 创建.nojekyll文件（防止GitHub Pages忽略下划线开头的文件）
touch "$TEMP_DIR/.nojekyll"
print_success ".nojekyll 文件已创建"

# 8. 部署到gh-pages分支
print_step "部署到gh-pages分支..."

# 创建临时分支名
TIMESTAMP=$(date +%s)
TEMP_BRANCH="temp-deploy-$TIMESTAMP"

print_step "创建临时分支: $TEMP_BRANCH"
git checkout -b "$TEMP_BRANCH"

print_step "清理当前分支..."
git rm -rf . > /dev/null 2>&1 || true
git clean -fdx > /dev/null 2>&1 || true

print_step "复制构建内容..."
cp -r "$TEMP_DIR/"* .
cp "$TEMP_DIR/.nojekyll" .

print_step "提交更改..."
git add .
COMMIT_MSG="Deploy: React homepage + HonKit content ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit -m "$COMMIT_MSG"

print_step "推送到gh-pages..."
git push -f origin "$TEMP_BRANCH":gh-pages

if [ $? -eq 0 ]; then
    print_success "成功推送到gh-pages!"
else
    print_error "推送失败"
    exit 1
fi

# 9. 清理
print_step "清理临时文件..."
git checkout main
git branch -D "$TEMP_BRANCH"
rm -rf "$TEMP_DIR"
print_success "清理完成"

echo ""
echo "============================================================"
echo "✅ 部署完成!"
echo "============================================================"
echo ""
echo "🌐 网站将在几分钟后更新:"
echo "    🏠 主页(React): https://beihaili.github.io/Stories-about-Bitcoin/"
echo "    📚 中文版: https://beihaili.github.io/Stories-about-Bitcoin/zh/"
echo "    📖 英文版: https://beihaili.github.io/Stories-about-Bitcoin/en/"
echo ""
echo "============================================================"
