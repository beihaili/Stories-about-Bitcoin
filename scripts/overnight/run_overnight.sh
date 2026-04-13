#!/bin/zsh
# run_overnight.sh — 定时启动 overnight iteration system
# 用法: 直接执行，或由 launchd/cron 调度
#
# 功能: 启动 budget-aware 模式，自动跑满 5h 窗口的 token
# 认证: 预检 claude CLI 认证，失败则发系统通知

set -uo pipefail

# 加载用户 shell 环境（PATH、keychain 上下文等）
[[ -f ~/.zshrc ]] && source ~/.zshrc 2>/dev/null || true

REPO_DIR="/Users/beihai/code/Bitcoin/bitcoinstory/Stories-about-Bitcoin"
LOG_DIR="$REPO_DIR/scripts/overnight/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H%M')
LOG_FILE="$LOG_DIR/run_${TIMESTAMP}.log"

# 日志函数
log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Overnight run starting ==="
log "PATH=$PATH"
log "HOME=$HOME"
log "USER=$(whoami)"

cd "$REPO_DIR"

# --- 认证预检 ---
log "Pre-flight: testing claude CLI auth..."
AUTH_TEST=$(echo "respond with just OK" | timeout 30 claude -p --model sonnet --no-session-persistence 2>&1 || true)
if echo "$AUTH_TEST" | grep -qi "OK"; then
    log "Auth OK — proceeding."
else
    log "Auth FAILED — output: $(echo "$AUTH_TEST" | head -3)"
    # 尝试发系统通知
    osascript -e 'display notification "Claude auth failed — run claude /login manually" with title "Overnight Iteration"' 2>/dev/null || true
    log "Aborting run. Please run 'claude' manually to refresh login."
    exit 1
fi

# --- 清理上次残留 ---
log "Cleaning up leftover worktrees and branches..."
git worktree list | grep overnight-wt | awk '{print $1}' | xargs -I{} git worktree remove --force {} 2>/dev/null || true
git branch --list 'overnight/*' | xargs git branch -D 2>/dev/null || true

# --- 启动 budget-aware 模式 ---
log "Launching budget-aware overnight run..."
python3 -m scripts.overnight \
    --budget-aware \
    --rounds 20 \
    --window-hours 5 \
    --timeout 900 \
    >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
log "=== Overnight run finished (exit $EXIT_CODE) ==="

# 发完成通知
if [[ $EXIT_CODE -eq 0 ]]; then
    osascript -e 'display notification "Overnight run completed" with title "Overnight Iteration"' 2>/dev/null || true
else
    osascript -e "display notification \"Overnight run failed (exit $EXIT_CODE)\" with title \"Overnight Iteration\"" 2>/dev/null || true
fi

exit $EXIT_CODE
