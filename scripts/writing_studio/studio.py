#!/usr/bin/env python3
"""
写作工作室 (Writing Studio)

不产出内容，产出上下文和分析。每个命令独立运行，通过 claude CLI 调用 Opus。
所有命令加载写作圣经作为基础上下文，按需加载章节和史料。

用法:
    python -m scripts.writing_studio.studio research --topic "中本聪"
    python -m scripts.writing_studio.studio connect --chapter 5
    python -m scripts.writing_studio.studio critique --file draft.md
    python -m scripts.writing_studio.studio enhance --file draft.md
    python -m scripts.writing_studio.studio consistency --chapter 5
    python -m scripts.writing_studio.studio draft --chapter 5
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
CHAPTERS_DIR = PROJECT_ROOT / "正文"
RESOURCES_DIR = PROJECT_ROOT / "资料"
BIBLE_FILE = PROJECT_ROOT / "写作圣经.md"
THOUGHTS_FILE = PROJECT_ROOT / "AI模型" / "我的思考库.json"
STYLE_DNA_FILE = PROJECT_ROOT / "AI模型" / "风格DNA.txt"
OUTPUT_DIR = PROJECT_ROOT / "scripts" / "writing_studio" / "output"


def claude_call(prompt: str, model: str = "opus", timeout: int = 600) -> str:
    """调用 claude CLI，使用 Max 计划额度"""
    cmd = ["claude", "-p", "--model", model, "--output-format", "text", "--no-session-persistence"]
    try:
        result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            print(f"⚠️ claude 错误: {result.stderr.strip()[:200]}", file=sys.stderr)
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"⚠️ claude 超时 ({timeout}s)", file=sys.stderr)
        return ""
    except FileNotFoundError:
        print("❌ 未找到 claude 命令", file=sys.stderr)
        return ""


def load_bible() -> str:
    """加载写作圣经"""
    if BIBLE_FILE.exists():
        return BIBLE_FILE.read_text(encoding="utf-8")
    return ""


def load_style_dna() -> str:
    """加载风格指南"""
    if STYLE_DNA_FILE.exists():
        return STYLE_DNA_FILE.read_text(encoding="utf-8")
    return ""


def load_thoughts() -> str:
    """加载思想库"""
    if THOUGHTS_FILE.exists():
        return THOUGHTS_FILE.read_text(encoding="utf-8")
    return ""


def find_chapter_file(chapter_num: int) -> Path | None:
    """根据章节号找到对应文件"""
    pattern = f"{chapter_num:02d}_*.md"
    matches = sorted(CHAPTERS_DIR.glob(pattern))
    # 排除历史版本目录中的文件
    matches = [m for m in matches if "历史版本" not in str(m)]
    return matches[0] if matches else None


def load_chapter(chapter_num: int) -> str:
    """加载指定章节内容"""
    f = find_chapter_file(chapter_num)
    if f:
        return f.read_text(encoding="utf-8")
    return ""


def load_all_chapters() -> str:
    """加载全部章节（用于全书上下文）"""
    files = sorted(CHAPTERS_DIR.glob("*.md"))
    files = [f for f in files if "历史版本" not in str(f) and "README" not in f.name]
    parts = []
    for f in files:
        content = f.read_text(encoding="utf-8")
        parts.append(f"=== {f.name} ===\n{content}\n")
    return "\n".join(parts)


def search_resources(topic: str, max_results: int = 5) -> str:
    """从资料库中搜索与主题相关的内容"""
    tokens = [t for t in re.split(r"[\s,;，。：]", topic.lower()) if len(t) > 1]
    if not tokens:
        return ""

    scored = []
    for f in sorted(RESOURCES_DIR.glob("*.json")):
        if "index" in f.name:
            continue
        try:
            text = f.read_text(encoding="utf-8")[:20000]
            score = sum(text.lower().count(tok) for tok in tokens)
            if score > 0:
                scored.append((score, f.name, text[:5000]))
        except Exception:
            pass

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, name, text in scored[:max_results]:
        results.append(f"--- {name} (相关度:{score}) ---\n{text}\n")
    return "\n".join(results)


# ==================== 命令实现 ====================

def cmd_research(args):
    """从史料库检索与主题相关的事实"""
    topic = args.topic
    print(f"🔍 检索主题: {topic}")

    resources = search_resources(topic, max_results=8)
    if not resources:
        print("未找到相关史料")
        return

    bible = load_bible()
    prompt = f"""你是《比特币那些事儿》的史料研究员。

【写作圣经（了解全书背景）】
{bible[:3000]}

【从资料库检索到的相关史料】
{resources}

【任务】
针对主题"{topic}"，从上述史料中提取：
1. 关键事实清单（时间、人名、数字、事件经过）
2. 可以使用的直接引语或原始文档摘录
3. 不同来源之间的矛盾或需要进一步核实的地方
4. 与已有章节可能产生的呼应关系

请输出结构化的研究报告。"""

    result = claude_call(prompt, timeout=300)
    print(result)

    # 保存结果
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"research_{topic.replace(' ', '_')[:30]}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n📄 已保存: {out_file}")


def cmd_connect(args):
    """分析某章与其他章节的潜在连接点"""
    ch = args.chapter
    print(f"🔗 分析第{ch}章的跨章节连接")

    chapter_content = load_chapter(ch)
    if not chapter_content:
        print(f"未找到第{ch}章")
        return

    bible = load_bible()
    prompt = f"""你是《比特币那些事儿》的编辑。

【写作圣经】
{bible}

【当前章节（第{ch}章）】
{chapter_content[:8000]}

【任务】
分析第{ch}章与全书其他章节的连接关系：

1. **已有的呼应**：这章已经引用或呼应了哪些前文内容？列出具体位置
2. **遗漏的呼应**：根据写作圣经中的隐喻体系和人物弧线，这章应该但没有呼应哪些内容？
3. **为后文铺垫**：这章为后续章节埋了哪些伏笔？有没有遗漏的铺垫机会？
4. **隐喻连续性**：这章使用了哪些核心意象？是否与全书的意象体系一致？
5. **具体建议**：给出3-5条具体的修改建议，说明在哪个位置添加什么样的呼应

请输出结构化分析。"""

    result = claude_call(prompt, timeout=300)
    print(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"connect_ch{ch:02d}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n📄 已保存: {out_file}")


def cmd_critique(args):
    """对草稿做优劣分析"""
    filepath = Path(args.file)
    if not filepath.exists():
        filepath = PROJECT_ROOT / args.file
    if not filepath.exists():
        print(f"文件不存在: {args.file}")
        return

    print(f"📝 分析草稿: {filepath.name}")
    draft = filepath.read_text(encoding="utf-8")
    bible = load_bible()
    style_dna = load_style_dna()

    prompt = f"""你是《比特币那些事儿》的资深编辑。

【写作圣经（了解全书标准）】
{bible[:6000]}

【风格指南】
{style_dna}

【待分析草稿】
{draft[:12000]}

【任务】
对这篇草稿进行深度分析：

1. **优点**（具体引用原文说明哪些地方写得好，为什么好）
2. **AI味检测**（逐段扫描，标记任何AI味重的表达、堆砌的修辞、虚假的第一人称）
3. **事实密度**（哪些段落缺少具体的时间/人名/数字？）
4. **灵魂时刻**（这篇有没有能让读者停下来的"灵魂时刻"？如果没有，建议在哪里加？）
5. **跨章节连接**（与已有章节的呼应是否充分？遗漏了什么？）
6. **结构节奏**（段落长短交错是否自然？有没有全部一样长的问题？）
7. **综合评分**（1-10，附理由）

请具体到段落和句子级别，不要泛泛而谈。"""

    result = claude_call(prompt, timeout=300)
    print(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"critique_{filepath.stem}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n📄 已保存: {out_file}")


def cmd_enhance(args):
    """在保留灵魂的前提下补充事实细节"""
    filepath = Path(args.file)
    if not filepath.exists():
        filepath = PROJECT_ROOT / args.file
    if not filepath.exists():
        print(f"文件不存在: {args.file}")
        return

    print(f"✨ 增强草稿: {filepath.name}")
    draft = filepath.read_text(encoding="utf-8")

    # 从标题中提取主题用于检索
    topic = ""
    for line in draft.split("\n")[:5]:
        if line.startswith("#"):
            topic = line.lstrip("# ").strip()
            break

    resources = search_resources(topic, max_results=5) if topic else ""
    style_dna = load_style_dna()

    prompt = f"""你是《比特币那些事儿》的事实编辑。你的工作不是重写，而是在保留原文灵魂的前提下补充事实。

【风格指南】
{style_dna}

【原文】
{draft[:12000]}

【可用的补充史料】
{resources[:8000]}

【任务】
逐段审查原文，找出可以补充的事实细节：

1. 对每个段落，判断是否需要补充（"灵魂段落"不动，"骨架段落"可以丰富）
2. 给出具体的补充建议：在哪个位置插入什么事实（时间、人名、数字、引语）
3. 建议的表述方式（要自然融入，不要贴标签）
4. 不要改动原文的核心比喻、情感表达、哲学思考

输出格式：
对每个需要修改的段落，给出：
- 原文位置（引用前几个字）
- 建议操作（补充/替换/删除）
- 具体内容
- 理由"""

    result = claude_call(prompt, timeout=300)
    print(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"enhance_{filepath.stem}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n📄 已保存: {out_file}")


def cmd_consistency(args):
    """检查与已有章节的事实一致性"""
    ch = args.chapter
    print(f"🔍 检查第{ch}章的事实一致性")

    chapter_content = load_chapter(ch)
    if not chapter_content:
        print(f"未找到第{ch}章")
        return

    # 加载相邻章节作为对照
    adjacent = []
    for adj_ch in range(max(0, ch - 2), min(33, ch + 3)):
        if adj_ch == ch:
            continue
        content = load_chapter(adj_ch)
        if content:
            adjacent.append(f"=== 第{adj_ch}章 ===\n{content[:3000]}")

    prompt = f"""你是《比特币那些事儿》的事实核查员。

【当前章节（第{ch}章）】
{chapter_content[:8000]}

【相邻章节（对照用）】
{"".join(adjacent[:4])}

【任务】
检查第{ch}章的事实一致性：

1. **时间线一致性**：本章提到的日期、时间是否与相邻章节矛盾？
2. **人物一致性**：人物的身份、职位、行为描述是否前后一致？
3. **事件一致性**：同一事件在不同章节的描述是否有出入？
4. **数据一致性**：价格、数量、比例等数字是否前后矛盾？
5. **称呼一致性**：同一人物/机构的称呼是否统一？

对每个发现的不一致，给出：
- 具体位置（章节号+引用文字）
- 矛盾内容
- 建议修正方案"""

    result = claude_call(prompt, timeout=300)
    print(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"consistency_ch{ch:02d}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n📄 已保存: {out_file}")


def cmd_draft(args):
    """生成带全书上下文的初稿"""
    ch = args.chapter
    topic = args.topic or f"第{ch}章"
    print(f"📝 生成初稿: 第{ch}章 — {topic}")
    print("   加载全书上下文...")

    all_chapters = load_all_chapters()
    bible = load_bible()
    style_dna = load_style_dna()
    thoughts = load_thoughts()

    # 检索相关史料
    resources = search_resources(topic, max_results=5)

    print(f"   全书: {len(all_chapters)} 字符")
    print(f"   圣经: {len(bible)} 字符")
    print(f"   史料: {len(resources)} 字符")
    print("   生成中（Opus，预计2-4分钟）...")

    prompt = f"""你是《比特币那些事儿》的写作搭档。你要为第{ch}章生成一份**带标注的初稿**。

【写作圣经】
{bible}

【风格指南】
{style_dna}

【作者思想库（只有这些经历可以用第一人称）】
{thoughts[:3000]}

【已有的全部章节（你的全书上下文）】
{all_chapters[:200000]}

【可用的补充史料】
{resources[:8000]}

【任务】
为第{ch}章（主题：{topic}）生成初稿。

这不是最终稿，而是一份**带标注的草稿**，标注需要作者做创意决策的地方。

格式要求：
1. 用正常的Markdown写正文部分
2. 在需要作者决策的地方，用 `> [决策点]` 标注，给出2-3个选项
3. 在"灵魂段落"的位置用 `> [灵魂时刻]` 标注，说明这里需要什么样的表达
4. 必须包含至少2处与已有章节的明确呼应（标注来源章节号）
5. 必须遵循写作圣经中本章的定位和叙事弧线

写作规则：
- 严格遵循风格DNA.txt中的约束
- 事实骨架部分尽量详实（时间、人名、数字）
- 灵魂部分留给作者，用标注说明需要什么
- 结尾必须有趣味冷知识 + 向下一章的过渡钩子

请直接输出初稿（Markdown格式）："""

    result = claude_call(prompt, timeout=600)

    if not result:
        print("❌ 生成失败")
        return

    # 清理开头的思考文字
    lines = result.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            result = "\n".join(lines[i:])
            break

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"draft_ch{ch:02d}.md"
    out_file.write_text(result, encoding="utf-8")
    print(f"\n✅ 初稿已保存: {out_file}")
    print(f"   长度: {len(result)} 字符")
    print(f"   预览: {result[:300]}...")


def _load_ai_patterns() -> str:
    """加载 AI味模式速查表"""
    patterns_file = Path.home() / "claude-workspace" / "skills" / "chapter-polish" / "references" / "ai-patterns.md"
    if patterns_file.exists():
        return patterns_file.read_text(encoding="utf-8")
    return ""


def _build_score_prompt(draft: str, filename: str) -> str:
    """构建评分 prompt（共享逻辑）"""
    bible = load_bible()
    style_dna = load_style_dna()
    ai_patterns = _load_ai_patterns()

    return f"""你是《比特币那些事儿》的严格评分编辑。你的评分直接决定哪些章节需要重写。

【写作圣经（摘要）】
{bible[:4000]}

【风格指南】
{style_dna[:2000]}

【AI味检测清单】
{ai_patterns[:3000]}

【待评分章节】
{draft[:15000]}

【评分维度与标准】
1. 事实准确性 (accuracy): 日期/人名/数字是否正确？事实密度如何？有无具体引语/帖子/邮件？
2. 叙事品质 (narrative): 是否以人物行动推动叙事？有无张力和悬念？还是只在罗列事件？
3. AI味控制 (ai_control): 逐段检查上面的 AI味检测清单，每命中一条扣1分。有 bullet list 直接≤5分。
4. 灵魂时刻 (soul_moment): 是否有至少1个让读者停下来的画面？评分标准：
   - ≤4分：无具体感官描写，只有抽象感慨或概念
   - 5分：有视觉描写但只有一种感官，或铺垫/反差不足
   - 6分：有感官画面但缺第二种感官，或升华超过1句
   - 7分：有铺垫+感官爆发+升华，但感官种类或情绪反差可以更好
   - 8分：完整的铺垫→触发→感官爆发(≥2种感官)→升华(仅1句)结构
5. 跨章节连接 (connection): 与前后章是否有明确的人物/事件呼应？有无伏笔？结尾是否为下章铺垫？
6. 结构节奏 (rhythm): 段落长度是否有变化（短句冲击+长段深潜）？高潮是否充分展开？

每项 1-10 分。校准锚点：
- 大多数未经优化的AI辅助写作章节应在 4-6 分区间
- 7分意味着该维度已经比较好，只有小问题
- 8分意味着该维度接近专业水平
- 9-10分极为罕见，意味着该维度几乎无可挑剔

【输出格式】
严格输出以下 JSON，不要输出任何其他内容：
```json
{{{{
  "chapter": "{filename}",
  "scores": {{{{
    "accuracy": N,
    "narrative": N,
    "ai_control": N,
    "soul_moment": N,
    "connection": N,
    "rhythm": N
  }}}},
  "weighted_avg": N.N,
  "comment": "一句话总评（不超过50字）",
  "weakest": "最弱维度的英文key",
  "strongest": "最强维度的英文key"
}}}}
```

加权平均计算：narrative×0.25 + ai_control×0.25 + accuracy×0.15 + soul_moment×0.15 + connection×0.10 + rhythm×0.10

请直接输出 JSON："""


def _calc_weighted_avg(scores: dict) -> float:
    """计算加权平均分"""
    return round(
        scores.get("narrative", 0) * 0.25
        + scores.get("ai_control", 0) * 0.25
        + scores.get("accuracy", 0) * 0.15
        + scores.get("soul_moment", 0) * 0.15
        + scores.get("connection", 0) * 0.10
        + scores.get("rhythm", 0) * 0.10,
        1,
    )


def cmd_score(args):
    """轻量评分：6维度打分 + 一句话点评，输出 JSON"""
    filepath = Path(args.file)
    if not filepath.exists():
        filepath = PROJECT_ROOT / args.file
    if not filepath.exists():
        print(f"文件不存在: {args.file}")
        return

    print(f"📊 评分: {filepath.name}")
    draft = filepath.read_text(encoding="utf-8")
    prompt = _build_score_prompt(draft, filepath.name)
    result = claude_call(prompt, timeout=180)

    if not result:
        print("❌ 评分失败")
        return

    score_data = _extract_json(result)
    if score_data:
        score_data["chapter"] = filepath.name
        score_data["weighted_avg"] = _calc_weighted_avg(score_data.get("scores", {}))
        formatted = json.dumps(score_data, ensure_ascii=False, indent=2)
        print(formatted)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_file = OUTPUT_DIR / f"score_{filepath.stem}.json"
        out_file.write_text(formatted, encoding="utf-8")
        print(f"\n📄 已保存: {out_file}")
        return score_data
    else:
        print("⚠️ 无法解析 JSON，原始输出：")
        print(result[:500])
        return None


def _extract_json(text: str) -> dict | None:
    """从文本中提取 JSON 对象"""
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 尝试从 ```json ... ``` 中提取
    m = re.search(r"```json\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # 尝试找到第一个 { 到最后一个 }
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass
    return None


def _score_single_file(filepath: Path) -> dict | None:
    """评分单个文件（用于并行调用）"""
    print(f"📊 开始评分: {filepath.name}")
    draft = filepath.read_text(encoding="utf-8")
    prompt = _build_score_prompt(draft, filepath.name)
    result = claude_call(prompt, timeout=180)

    if not result:
        print(f"❌ 评分失败: {filepath.name}")
        return None

    score_data = _extract_json(result)
    if score_data:
        score_data["chapter"] = filepath.name
        score_data["weighted_avg"] = _calc_weighted_avg(score_data.get("scores", {}))
        print(f"✅ {filepath.name}: {score_data['weighted_avg']}")
        return score_data
    else:
        print(f"⚠️ 无法解析: {filepath.name}")
        return None


def cmd_score_all(args):
    """批量评分全部章节，输出评分总表"""
    workers = args.workers
    print(f"📊 批量评分全部章节（并行数: {workers}）")

    # 找到所有正文章节
    files = sorted(CHAPTERS_DIR.glob("*.md"))
    files = [f for f in files if "历史版本" not in str(f) and "README" not in f.name]
    print(f"   找到 {len(files)} 个章节文件")

    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_file = {executor.submit(_score_single_file, f): f for f in files}
        for future in as_completed(future_to_file):
            filepath = future_to_file[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
            except Exception as e:
                print(f"❌ 异常: {filepath.name}: {e}")

    # 按章节号排序
    def sort_key(d):
        name = d.get("chapter", "")
        m = re.match(r"(\d+)", name)
        return int(m.group(1)) if m else 999
    results.sort(key=sort_key)

    # 生成评分总表
    if not results:
        print("❌ 没有成功的评分结果")
        return

    lines = ["# 评分总表", ""]
    lines.append(f"评分时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"评分章节数: {len(results)}/{len(files)}")
    lines.append("")

    # 总览统计
    avgs = [r["weighted_avg"] for r in results]
    lines.append(f"**全书平均分: {sum(avgs)/len(avgs):.1f}**")
    lines.append(f"**最高分: {max(avgs)}** | **最低分: {min(avgs)}**")
    lines.append("")

    # 详细表格
    lines.append("| # | 章节 | 事实 | 叙事 | AI味 | 灵魂 | 连接 | 节奏 | **综合** | 点评 |")
    lines.append("|---|------|------|------|------|------|------|------|---------|------|")
    for r in results:
        s = r.get("scores", {})
        name = r["chapter"]
        # 从文件名提取章节号和标题
        m = re.match(r"(\d+)_(.*?)\.md", name)
        if m:
            num, title = m.group(1), m.group(2)
        else:
            num, title = "-", name.replace(".md", "")

        avg = r["weighted_avg"]
        # 标注高分和低分
        flag = ""
        if avg >= 8.0:
            flag = " ⭐"
        elif avg < 6.0:
            flag = " ⚠️"

        comment = r.get("comment", "")[:40]
        lines.append(
            f"| {num} | {title} "
            f"| {s.get('accuracy', '-')} "
            f"| {s.get('narrative', '-')} "
            f"| {s.get('ai_control', '-')} "
            f"| {s.get('soul_moment', '-')} "
            f"| {s.get('connection', '-')} "
            f"| {s.get('rhythm', '-')} "
            f"| **{avg}**{flag} "
            f"| {comment} |"
        )

    lines.append("")
    lines.append("## 维度说明")
    lines.append("- 事实: 事实准确性（日期/人名/数字）×15%")
    lines.append("- 叙事: 叙事品质（人物驱动 vs 事件罗列）×25%")
    lines.append("- AI味: AI味控制（bullet list/排比/空泛升华）×25%")
    lines.append("- 灵魂: 灵魂时刻（让读者停下来的画面）×15%")
    lines.append("- 连接: 跨章节连接（呼应/伏笔/人物连续性）×10%")
    lines.append("- 节奏: 结构节奏（段落长短交错/高潮展开）×10%")
    lines.append("")
    lines.append("## 图例")
    lines.append("- ⭐ 综合≥8.0（优秀）")
    lines.append("- ⚠️ 综合<6.0（需重点改进）")

    # 高分/低分汇总
    high = [r for r in results if r["weighted_avg"] >= 8.0]
    low = [r for r in results if r["weighted_avg"] < 6.0]
    if high:
        lines.append("")
        lines.append(f"## 高分章节（{len(high)}篇，综合≥8.0）")
        for r in sorted(high, key=lambda x: -x["weighted_avg"]):
            lines.append(f"- {r['chapter']}: **{r['weighted_avg']}** — {r.get('comment', '')}")
    if low:
        lines.append("")
        lines.append(f"## 低分章节（{len(low)}篇，综合<6.0）")
        for r in sorted(low, key=lambda x: x["weighted_avg"]):
            lines.append(f"- {r['chapter']}: **{r['weighted_avg']}** — {r.get('comment', '')}")

    table_text = "\n".join(lines)
    print("\n" + table_text)

    # 保存评分总表和原始 JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table_file = PROJECT_ROOT / "评分总表.md"
    table_file.write_text(table_text, encoding="utf-8")
    print(f"\n📄 评分总表已保存: {table_file}")

    json_file = OUTPUT_DIR / "scores_all.json"
    json_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📄 原始数据已保存: {json_file}")


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="写作工作室 — AI辅助写作工具集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="可用命令")

    # research
    p = sub.add_parser("research", help="从史料库检索相关事实")
    p.add_argument("--topic", "-t", required=True, help="检索主题")

    # connect
    p = sub.add_parser("connect", help="分析跨章节连接")
    p.add_argument("--chapter", "-c", type=int, required=True, help="章节号")

    # critique
    p = sub.add_parser("critique", help="对草稿做优劣分析")
    p.add_argument("--file", "-f", required=True, help="草稿文件路径")

    # enhance
    p = sub.add_parser("enhance", help="保留灵魂，补充事实")
    p.add_argument("--file", "-f", required=True, help="草稿文件路径")

    # consistency
    p = sub.add_parser("consistency", help="事实一致性检查")
    p.add_argument("--chapter", "-c", type=int, required=True, help="章节号")

    # draft
    p = sub.add_parser("draft", help="生成带标注的初稿")
    p.add_argument("--chapter", "-c", type=int, required=True, help="章节号")
    p.add_argument("--topic", "-t", default="", help="章节主题")

    # score（单章评分）
    p = sub.add_parser("score", help="轻量评分（6维度+综合分）")
    p.add_argument("--file", "-f", required=True, help="章节文件路径")

    # score-all（批量评分）
    p = sub.add_parser("score-all", help="批量评分全部章节")
    p.add_argument("--workers", "-w", type=int, default=4, help="并行数（默认4）")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "research": cmd_research,
        "connect": cmd_connect,
        "critique": cmd_critique,
        "enhance": cmd_enhance,
        "consistency": cmd_consistency,
        "draft": cmd_draft,
        "score": cmd_score,
        "score-all": cmd_score_all,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
