# 比特币那些事儿 - 统一命令入口
# 用法: make <命令> [参数]

SHELL := /bin/bash
STUDIO := python3 -m scripts.writing_studio.studio
PIPELINE := python3 -m scripts.content_pipeline.cli

# ============ 构建 ============

# 从 正文/ 构建 zh/（HonKit 用）
# 用法: make build-zh
build-zh:
	@python3 scripts/build_zh.py

# ============ 写作工作室（推荐） ============

# 从史料库检索相关事实
# 用法: make research TOPIC="中本聪"
research:
	@$(STUDIO) research --topic "$(TOPIC)"

# 分析某章与其他章节的连接关系
# 用法: make connect CH=5
connect:
	@$(STUDIO) connect --chapter $(CH)

# 对草稿做深度优劣分析
# 用法: make critique FILE=draft.md
critique:
	@$(STUDIO) critique --file "$(FILE)"

# 保留灵魂，补充事实细节
# 用法: make enhance FILE=正文/05_创世纪：中本聪创世.md
enhance:
	@$(STUDIO) enhance --file "$(FILE)"

# 检查与已有章节的事实一致性
# 用法: make consistency CH=5
consistency:
	@$(STUDIO) consistency --chapter $(CH)

# 生成带全书上下文的标注初稿（加载全部33章+写作圣经）
# 用法: make draft CH=5 TOPIC="章节主题"
draft:
	@$(STUDIO) draft --chapter $(CH) $(if $(TOPIC),--topic "$(TOPIC)",)

# 轻量评分（6维度+综合分，输出 JSON）
# 用法: make studio-score FILE=正文/08_初出茅庐：价值发现.md
studio-score:
	@$(STUDIO) score --file "$(FILE)"

# 批量评分全部章节（并行，输出评分总表.md）
# 用法: make score-all [WORKERS=4]
score-all:
	@$(STUDIO) score-all $(if $(WORKERS),--workers $(WORKERS),)

# ============ 章节创建 ============

# 创建新章节（自动编号、获取区块高度）
# 用法: make new-chapter TITLE="章节标题"
new-chapter:
	@./scripts/create_chapter.sh "$(TITLE)"

# ============ 内容管道 ============

# AI 重写指定章节（Director-Writer 双 Agent）
# 用法: make rewrite CH=5
rewrite:
	@$(PIPELINE) rewrite $(CH)

# 对章节进行质量评分
# 用法: make score CH=5
score:
	@$(PIPELINE) score $(CH)

# 翻译指定章节（中→英）
# 用法: make translate CH=5
translate:
	@$(PIPELINE) translate $(CH)

# 同步：构建 zh/ + 更新 feed/sitemap
# 用法: make sync CH=5
sync:
	@$(PIPELINE) sync $(CH)

# 同步并自动 commit
# 用法: make sync-commit CH=5
sync-commit:
	@$(PIPELINE) sync $(CH) --commit

# 批量处理（重写→评分→翻译→同步）
# 用法: make batch START=1 END=10
batch:
	@$(PIPELINE) batch $(START) $(END)

# ============ 推文生成 ============

# 生成今日推文素材
tweets-today:
	@cd scripts/twitter_slicer && python3 cli.py today $(if $(LANG),--lang $(LANG),)

# 切割章节为推文
tweets-chapter:
	@cd scripts/twitter_slicer && python3 cli.py chapter $(CH)

# 批量生成 N 天推文队列
tweets-batch:
	@cd scripts/twitter_slicer && python3 cli.py batch $(or $(DAYS),30)

# ============ 其他 ============

calendar:
	@$(PIPELINE) calendar scan

analytics:
	@cd scripts/analytics && python3 analyze.py

# ============ 帮助 ============

help:
	@echo "比特币那些事儿 - 可用命令："
	@echo ""
	@echo "  构建:"
	@echo "    make build-zh                        从正文/构建zh/（HonKit用）"
	@echo ""
	@echo "  写作工作室（Opus驱动）:"
	@echo "    make research TOPIC=\"主题\"          史料检索"
	@echo "    make connect CH=5                   跨章节连接分析"
	@echo "    make critique FILE=draft.md         草稿优劣分析"
	@echo "    make enhance FILE=draft.md          保留灵魂补充事实"
	@echo "    make consistency CH=5               事实一致性检查"
	@echo "    make draft CH=5 TOPIC=\"主题\"        全书上下文初稿"
	@echo "    make studio-score FILE=draft.md     轻量评分（6维度）"
	@echo "    make score-all [WORKERS=4]          批量评分全部章节"
	@echo ""
	@echo "  创作流程:"
	@echo "    make new-chapter TITLE=\"章节标题\"    创建新章节"
	@echo "    make rewrite CH=5                   AI 重写章节"
	@echo "    make score CH=5                     质量评分"
	@echo "    make translate CH=5                 翻译（中→英）"
	@echo "    make sync CH=5                      构建zh/ + 更新feed/sitemap"
	@echo "    make sync-commit CH=5               同步并 commit"
	@echo ""
	@echo "  推广工具:"
	@echo "    make tweets-today                   今日推文素材"
	@echo "    make tweets-chapter CH=5            切割章节为推文"
	@echo "    make tweets-batch DAYS=30           批量生成推文队列"

.PHONY: build-zh \
        research connect critique enhance consistency draft \
        studio-score score-all \
        new-chapter rewrite score translate sync sync-commit batch \
        tweets-today tweets-chapter tweets-batch calendar analytics help
.DEFAULT_GOAL := help
