#!/bin/bash

# 比特币那些事儿 - 章节自动生成脚本
# 作者：beihaili
# 用法：./create_chapter.sh "章节名称"

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 获取当前比特币区块高度
get_current_block_height() {
    # 尝试多个API端点
    local apis=(
        "https://blockstream.info/api/blocks/tip/height"
        "https://blockchain.info/q/getblockcount"
        "https://api.blockcypher.com/v1/btc/main"
    )
    
    for api in "${apis[@]}"; do
        if [[ "$api" == *"blockcypher"* ]]; then
            # BlockCypher返回JSON，需要解析height字段
            local height=$(curl -s --connect-timeout 5 "$api" 2>/dev/null | grep -o '"height":[0-9]*' | cut -d':' -f2 | head -1)
        else
            # 其他API直接返回数字
            local height=$(curl -s --connect-timeout 5 "$api" 2>/dev/null)
        fi
        
        # 检查是否获取到有效的数字
        if [[ "$height" =~ ^[0-9]+$ ]] && [ "$height" -gt 0 ]; then
            echo "$height"
            return 0
        fi
    done
    
    # 使用默认值
    echo "908800"  # 默认值
}

# 生成文件名
generate_filename() {
    local chapter_name="$1"
    local counter
    local base_name
    
    # 如果章节名包含数字编号，提取它
    if [[ "$chapter_name" =~ ^([0-9]+)[_：:-]*(.+)$ ]]; then
        counter="${BASH_REMATCH[1]}"
        base_name="${BASH_REMATCH[2]}"
        # 清理base_name前面的分隔符
        base_name=$(echo "$base_name" | sed 's/^[_：:-]*//')
    else
        # 如果没有数字编号，需要自动生成一个
        # 检查正文目录中已有的文件，找到下一个编号
        local max_num=5  # 从05开始，因为前面已有00-05
        if [ -d "正文" ]; then
            for file in 正文/[0-9][0-9]_*.md; do
                if [[ -f "$file" && $(basename "$file") =~ ^([0-9]+)_ ]]; then
                    local num="${BASH_REMATCH[1]}"
                    # 去掉前导零
                    num=$((10#$num))
                    if [ "$num" -gt "$max_num" ]; then
                        max_num="$num"
                    fi
                fi
            done
        fi
        counter=$((max_num + 1))
        base_name="$chapter_name"
    fi
    
    # 简单地保留中文、字母和数字，移除其他字符
    base_name=$(echo "$base_name" | tr -d '：·，。！？""''（）()[]{}|\\/<>@#$%^&*+=~`')
    
    # 格式化编号（两位数）
    printf "%02d_%s.md" "$counter" "$base_name"
}

# 确定难度级别
determine_difficulty() {
    local chapter_name="$1"
    
    # 根据关键词判断难度
    if [[ "$chapter_name" =~ (引子|序言|开始|简介) ]]; then
        echo "初级-green"
    elif [[ "$chapter_name" =~ (技术|算法|密码|协议|代码|挖矿|共识) ]]; then
        echo "高级-red"
    else
        echo "中级-yellow"
    fi
}

# 生成章节模板
generate_chapter_template() {
    local chapter_name="$1"
    local block_height="$2"
    local difficulty="$3"
    local current_date=$(date +"%Y-%m")
    
    cat << EOF
# $chapter_name

![status](https://img.shields.io/badge/状态-草稿-yellow)
![author](https://img.shields.io/badge/作者-beihaili-blue)
![date](https://img.shields.io/badge/日期-$current_date%20block%20$block_height-orange)
![difficulty](https://img.shields.io/badge/难度-$difficulty)

> 💡 【请在这里添加本章节的核心内容简介】这里应该用一两句话概括本章节的主要内容和读者将会了解到什么。
> 
> 欢迎关注我的推特：[@bhbtc1337](https://twitter.com/bhbtc1337)
> 
> 进入微信交流群请填表：[表格链接](https://forms.gle/QMBwL6LwZyQew1tX8)
> 
> 文章开源在 GitHub：[Get-Started-with-Web3](https://github.com/beihaili/Get-Started-with-Web3)
> 


<div align="center">
<a href="https://github.com/beihaili/Get-Started-with-Web3">🏠 返回主页</a> | 
<a href="https://twitter.com/bhbtc1337">🐦 关注作者</a> | 
<a href="https://forms.gle/QMBwL6LwZyQew1tX8">📝 加入交流群</a>
</div>
EOF
}

# 主函数
main() {
    local chapter_name="$1"
    
    # 检查参数
    if [ -z "$chapter_name" ]; then
        print_error "请提供章节名称"
        echo -e "\n${YELLOW}用法：${NC}"
        echo "  $0 \"章节名称\""
        echo -e "\n${YELLOW}示例：${NC}"
        echo "  $0 \"第一批信徒\""
        echo "  $0 \"01_两块披萨的传奇\""
        echo "  $0 \"暗网与争议\""
        exit 1
    fi
    
    print_info "开始创建新章节：$chapter_name"
    
    # 创建正文目录（如果不存在）
    mkdir -p "正文"
    
    # 生成文件名
    local filename=$(generate_filename "$chapter_name")
    local filepath="正文/$filename"
    
    # 检查文件是否已存在
    if [ -f "$filepath" ]; then
        print_warning "文件已存在：$filepath"
        read -p "是否覆盖？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "取消操作"
            exit 0
        fi
    fi
    
    # 获取当前区块高度
    print_info "正在获取当前比特币区块高度..."
    local block_height=$(get_current_block_height)
    print_success "获取到区块高度：$block_height"
    
    # 确定难度级别
    local difficulty=$(determine_difficulty "$chapter_name")
    print_info "设置难度级别：${difficulty%-*}"
    
    # 生成文件
    print_info "正在生成文件：$filepath"
    generate_chapter_template "$chapter_name" "$block_height" "$difficulty" > "$filepath"
    
    print_success "章节文件创建成功！"
    echo -e "\n${BLUE}文件路径：${NC}$filepath"
    echo -e "${BLUE}区块高度：${NC}$block_height"
    echo -e "${BLUE}难度级别：${NC}${difficulty%-*}"
    
    # 询问是否立即编辑
    echo
    print_info "文件已创建完成，您可以开始编辑：$filepath"
    
    # 如果在支持的环境中，可以选择自动打开
    if command -v code &> /dev/null || command -v cursor &> /dev/null; then
        read -p "是否立即打开文件编辑？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command -v cursor &> /dev/null; then
                cursor "$filepath"
            elif command -v code &> /dev/null; then
                code "$filepath"
            fi
        fi
    fi
    
    print_success "脚本执行完成！"
}

# 显示帮助信息
show_help() {
    echo -e "${BLUE}📚 比特币那些事儿 - 章节自动生成脚本${NC}"
    echo -e "${BLUE}==================================${NC}"
    echo
    echo -e "${YELLOW}功能：${NC}"
    echo "  • 自动获取当前比特币区块高度"
    echo "  • 生成标准格式的章节文档"
    echo "  • 智能判断章节难度等级"
    echo "  • 自动生成文件名和编号"
    echo
    echo -e "${YELLOW}用法：${NC}"
    echo "  $0 \"章节名称\""
    echo "  $0 --help        显示此帮助信息"
    echo
    echo -e "${YELLOW}示例：${NC}"
    echo "  $0 \"第一批信徒\""
    echo "  $0 \"01_两块披萨的传奇\""
    echo "  $0 \"技术详解：挖矿原理\""
    echo
    echo -e "${YELLOW}难度判断规则：${NC}"
    echo "  • 包含'引子|序言|开始|简介' → 初级"
    echo "  • 包含'技术|算法|密码|协议|代码|挖矿|共识' → 高级"
    echo "  • 其他 → 中级"
    echo
    echo -e "${YELLOW}输出文件：${NC}"
    echo "  正文/XX_章节名称.md"
}

# 检查命令行参数
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

# 执行主函数
main "$1" 