#!/bin/bash
# run_overnight.sh — 定时启动 overnight iteration system
# 用法: 直接执行，或由 launchd 调度
#
# 功能: 启动 budget-aware 模式，自动跑满 5h 窗口的 token

set -euo pipefail

REPO_DIR="/Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin"
LOG_DIR="$REPO_DIR/scripts/overnight/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H%M')
LOG_FILE="$LOG_DIR/run_${TIMESTAMP}.log"

echo "=== Overnight run starting at $(date) ===" | tee "$LOG_FILE"

cd "$REPO_DIR"

# 清理上次残留
git worktree list | grep overnight-wt | awk '{print $1}' | xargs -I{} git worktree remove --force {} 2>/dev/null || true
git branch --list 'overnight/*' | xargs git branch -D 2>/dev/null || true

# 启动 budget-aware 模式 (caffeinate 内置在 __main__.py 里)
python3 -m scripts.overnight \
    --budget-aware \
    --rounds 20 \
    --window-hours 5 \
    --timeout 900 \
    >> "$LOG_FILE" 2>&1

echo "=== Overnight run finished at $(date) ===" | tee -a "$LOG_FILE"
