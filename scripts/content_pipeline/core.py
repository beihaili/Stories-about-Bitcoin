"""
Core classes for the content pipeline.

Extracted and refactored from AI模型/advanced_rewrite_framework.py.
Replaces hardcoded paths with config-based paths.
"""

import json
import os
import re
import glob as glob_module
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from . import config


class ClaudeCodeClient:
    """
    通过 claude CLI 调用 Claude 模型，使用 Max 计划额度，无需 API Key。
    """
    def __init__(self, model="sonnet"):
        self.model = model

    def generate(self, prompt: str, timeout: int = 600) -> str:
        """发送 prompt 到 claude CLI，返回文本响应"""
        cmd = [
            "claude", "-p",
            "--model", self.model,
            "--output-format", "text",
            "--no-session-persistence",
        ]
        try:
            result = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
            )
            if result.returncode != 0:
                print(f"  Warning: claude CLI error: {result.stderr.strip()[:200]}")
                return ""
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print(f"  Warning: claude CLI timed out ({timeout}s)")
            return ""
        except FileNotFoundError:
            print("  Error: claude command not found")
            return ""


class ContextLoader:
    """Utility for loading text files."""

    @staticmethod
    def load_file(path):
        path = str(path)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""


class ChunkSummarizer:
    """Compresses history materials into condensed summaries for indexing."""

    def __init__(self, client, model):
        self.client = client
        self.model = model
        self._use_claude = isinstance(client, ClaudeCodeClient)

    def summarize(self, text: str) -> str:
        if not text.strip():
            return ""
        prompt = (
            "请用中文 50-120 字总结下列材料的关键信息，保留人名、事件名、时间节点，"
            "禁止列点、禁止 markdown 代码块：\n\n"
            f"{text[:2000]}"
        )
        try:
            if self._use_claude:
                return self.client.generate(prompt, timeout=120)
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"  Warning: summarization failed, using truncation: {e}")
            return text[:180] + "..."

    def summarize_chunks(self, chunks: List[str]) -> List[Dict]:
        index = []
        for i, ch in enumerate(chunks):
            summary = self.summarize(ch)
            index.append({"id": i, "summary": summary, "text": ch})
            if (i + 1) % 10 == 0:
                print(f"  Summarized {i + 1}/{len(chunks)} chunks")
        return index


class HistoryManager:
    """
    History library manager with tiered loading.

    Priority order:
    1. User-written draft chapters (正文初稿)
    2. Core JSON files (Tier 1)
    3. Supplementary JSON files
    4. Markdown syntheses
    """

    def __init__(self, summarizer: Optional[ChunkSummarizer] = None):
        self.directory = str(config.KEY_RESOURCES_DIR)
        self.draft_directory = str(config.CHAPTERS_DIR)
        self.full_history = ""
        self.history_chunks: List[str] = []
        self.chunk_meta: List[Dict] = []
        self.history_index: List[Dict] = []
        self.summarizer = summarizer
        self.index_path = str(config.HISTORY_INDEX_FILE)

    def load_all_history(self):
        """Load all history sources with intelligent prioritization."""
        print("Loading history library...")
        draft_count = core_count = extra_count = md_count = 0

        # 0. Load user drafts (highest priority)
        if os.path.isdir(self.draft_directory):
            draft_files = sorted(glob_module.glob(os.path.join(self.draft_directory, "*.txt")))
            draft_files += sorted(glob_module.glob(os.path.join(self.draft_directory, "*.md")))
            for file in draft_files:
                text = ContextLoader.load_file(file)
                filename = Path(file).name
                if len(text) > 100:
                    self._append_content(text, f"draft:{filename}")
                    draft_count += 1

        # Also load from 正文/ directory
        chapters_dir = str(config.CHAPTERS_DIR)
        if os.path.isdir(chapters_dir):
            ch_files = sorted(glob_module.glob(os.path.join(chapters_dir, "*.txt")))
            ch_files += sorted(glob_module.glob(os.path.join(chapters_dir, "*.md")))
            for file in ch_files:
                text = ContextLoader.load_file(file)
                filename = Path(file).name
                if len(text) > 100:
                    self._append_content(text, f"chapter:{filename}")
                    draft_count += 1

        # 1. Load core JSON (Tier 1)
        loaded_files = set()
        for filename in config.CORE_HISTORY_FILES:
            file_path = os.path.join(self.directory, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        json_str = json.dumps(data, ensure_ascii=False, indent=2)
                        self._append_content(json_str[:20000], f"core:{filename}")
                        loaded_files.add(filename)
                        core_count += 1
                except Exception:
                    pass

        # 2. Load supplementary JSON
        all_json = sorted(glob_module.glob(os.path.join(self.directory, "*.json")))
        for file_path in all_json:
            filename = Path(file_path).name
            if filename in loaded_files or "index" in filename:
                continue
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    json_str = json.dumps(data, ensure_ascii=False, indent=2)
                    self._append_content(json_str[:10000], f"supplementary:{filename}")
                    extra_count += 1
            except Exception:
                pass

        # 3. Load markdown syntheses
        for filename in ["史料深度分析与叙事框架.md", "终极整理报告.md"]:
            file_path = os.path.join(self.directory, filename)
            if os.path.exists(file_path):
                text = ContextLoader.load_file(file_path)
                if text:
                    self._append_content(text[:20000], f"synthesis:{filename}")
                    md_count += 1

        self._build_index()
        print(
            f"  History loaded: {draft_count} drafts, {core_count} core, "
            f"{extra_count} supplementary, {md_count} syntheses; "
            f"{len(self.history_chunks)} chunks total"
        )
        self.full_history = f"Chunks: {len(self.history_chunks)}, Index: {len(self.history_index)}"
        return self.full_history

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks for retrieval."""
        size = config.CHUNK_SIZE
        overlap = config.CHUNK_OVERLAP
        chunks = []
        start = 0
        while start < len(text):
            end = min(len(text), start + size)
            chunks.append(text[start:end])
            if end == len(text):
                break
            start = end - overlap
        return chunks

    def _append_content(self, text: str, source: str):
        """Chunk text and track source metadata."""
        chunks = self._chunk_text(text)
        for ch in chunks:
            self.history_chunks.append(ch)
            self.chunk_meta.append({"source": source, "text": ch})

    def _build_index(self):
        """Build or load chunk summary index."""
        if not self.history_chunks:
            return

        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        self.history_index = data
                        print(f"  Loaded existing index: {len(self.history_index)} entries")
                        return
            except Exception:
                pass

        if not self.summarizer:
            self.history_index = [
                {"id": i, "summary": ch[:160] + "...", "text": ch}
                for i, ch in enumerate(self.history_chunks)
            ]
        else:
            print("  Building chunk summary index (this takes a while)...")
            self.history_index = self.summarizer.summarize_chunks(self.history_chunks)

        try:
            with open(self.index_path, "w", encoding="utf-8") as f:
                json.dump(self.history_index, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_relevant_history(self, topic: str) -> str:
        """Keyword-based retrieval with source weighting."""
        if not self.history_chunks:
            return ""
        tokens = [t for t in re.split(r"[\s,;，。]", topic.lower()) if t]
        scored = []

        source_list = self.history_index if self.history_index else [
            {"id": i, "summary": "", "text": ch}
            for i, ch in enumerate(self.history_chunks)
        ]

        for idx, item in enumerate(source_list):
            summary = item.get("summary", "")
            ch = item.get("text", "")
            score = sum(summary.lower().count(tok) for tok in tokens)
            score += sum(ch.lower().count(tok) for tok in tokens)

            if idx < len(self.chunk_meta):
                src = self.chunk_meta[idx].get("source", "")
                if "draft:" in src or "chapter:" in src:
                    score *= 1.5

            if score >= config.MIN_RELEVANCE_SCORE:
                scored.append((score, idx, ch))

        if not scored:
            scored = [(0, i, ch) for i, ch in enumerate(self.history_chunks[:5])]

        scored.sort(key=lambda x: x[0], reverse=True)

        selected = []
        total = 0
        for score, meta_idx, ch in scored:
            if total + len(ch) > config.MAX_CONTEXT_CHARS:
                break
            # 不添加来源标签，避免泄漏到最终输出
            selected.append(ch)
            total += len(ch)

        return "\n---\n".join(selected)


class StyleManager:
    """Manages Ming Dynasty writing style reference and DNA extraction."""

    def __init__(self):
        self.path = str(config.STYLE_BOOK)
        self.style_content = ""
        self.style_dna = ""

    def load(self):
        """Load the style reference book."""
        self.style_content = ContextLoader.load_file(self.path)
        if self.style_content:
            print(f"  Style library loaded: {len(self.style_content)} chars")
        return self.style_content

    def load_dna(self):
        """Load hand-crafted style guide (风格DNA.txt). Core file for controlling AI flavor."""
        dna_path = str(config.STYLE_DNA_FILE)
        if os.path.exists(dna_path):
            self.style_dna = ContextLoader.load_file(dna_path)
            if self.style_dna:
                return self.style_dna

        # Minimal fallback — no hardcoded catchphrases
        self.style_dna = (
            "【风格提示】\n"
            "参考《明朝那些事儿》的叙事方式：用聊天的口气讲严肃的历史，\n"
            "重视具体细节和画面感，控制修辞密度，让事实自己说话。\n"
        )
        return self.style_dna

    def get_prompt(self):
        """Get the best available style prompt (DNA preferred over full text)."""
        return self.style_dna or self.style_content[:8000]


class ThoughtsLibrary:
    """Author's personal thoughts and experiences, structured for writing guidance."""

    def __init__(self):
        self.path = str(config.THOUGHTS_FILE)
        self.data = {}

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        return self.data

    def get_all_str(self):
        return json.dumps(self.data, ensure_ascii=False, indent=2)

    def get_writing_guidance(self) -> str:
        """Convert thoughts library into structured writing guidance."""
        if not self.data:
            return self.get_all_str()

        sections = []

        for key, label in [
            ("我的经历", "【作者真实经历 — 只有以下经历可以用第一人称】"),
            ("情感共鸣点", "【作者情感共鸣点 — 可用于匹配章节情绪】"),
            ("我的思考", "【作者核心观点 — 可自然融入叙述评价中】"),
            ("具体故事案例", "【可引用的具体故事 — 融入时必须保持真实细节】"),
        ]:
            data = self.data.get(key, {})
            if data:
                lines = [label]
                for k, v in data.items():
                    lines.append(f"· {k}：{v}")
                sections.append("\n".join(lines))

        sections.append(
            "【思想库使用规则】\n"
            "1. 只有上面列出的经历才可以用第一人称叙述，禁止虚构假经历\n"
            "2. 融入方式：自然穿插在叙述中，不要用括号隔离\n"
            "3. 如果本章主题与作者经历没有直接关联，用第三人称叙述即可\n"
            "4. 情感共鸣点用于决定叙述基调，不是直接引用的文字"
        )

        return "\n\n".join(sections)


class StoryDirector:
    """
    AI Agent #1: Chapter planning and scriptwriting.
    Produces a structured JSON plan for each chapter.
    """

    def __init__(self, client, model):
        self.client = client
        self.model = model
        self._use_claude = isinstance(client, ClaudeCodeClient)

    def plan_chapter(
        self, topic: str, source_material: str, history_context: str, thoughts: str
    ) -> Dict:
        """Generate a chapter plan/script based on topic and context."""
        print(f"  Director planning: {topic}")

        prompt = f"""你是《比特币那些事儿》的编辑。现在要为主题"{topic}"设计章节结构。

【你的工作方式】
你不写正文，你只规划结构。你要做的是：
1. 从【史料】中找出与主题相关的具体事实（时间、人名、数字、事件经过）
2. 把这些事实组织成一条有因果逻辑的叙事线
3. 决定哪些地方可以融入作者的真实经历（见【作者背景】），哪些地方不能

【作者背景】
{thoughts[:3000]}

【核心素材】
{source_material[:4000]}

【史料背景】
{history_context[:6000]}

【规划要求】
- narrative_arc 必须由具体事件驱动，不是由观点或情绪驱动
- 每个叙事节点必须对应至少一条可查证的史料事实
- analogy_map 最多2个类比，必须具体（不要空泛比喻）
- personal_insertion_points 标记可融入作者真实经历的位置，如无关联则为空数组

请以 JSON 格式输出，包含：
title, core_emotion, narrative_arc (数组，每个元素包含 section_name 和 key_facts),
analogy_map (最多2个), personal_insertion_points (数组，每个元素包含 position 和
source_from_thoughts), opening_hook, sections (数组，每个包含 title 和 key_points)"""

        try:
            if self._use_claude:
                content = self.client.generate(prompt, timeout=300)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                content = response.choices[0].message.content
            if not content:
                return {}
            return self._safe_parse_json(content)
        except Exception as e:
            print(f"  Director error: {e}")
            return {}

    def _safe_parse_json(self, content: str) -> Dict:
        """Tolerant JSON parsing from LLM output."""
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            match = re.search(r"\{.*\}", content, re.S)
            if match:
                content = match.group(0)
            return json.loads(content)
        except Exception:
            return {}


class MingWriter:
    """
    AI Agent #2: Chapter drafting in Ming Dynasty narrative style.
    """

    def __init__(self, client, model):
        self.client = client
        self.model = model
        self._use_claude = isinstance(client, ClaudeCodeClient)

    def write(self, plan: Dict, style_prompt: str) -> str:
        """Write a chapter based on director's plan and style reference."""
        print("  Writer drafting chapter...")

        prompt = f"""你是一个历史写作者，正在写《比特币那些事儿》的一个章节。

【写作风格指南】
{style_prompt[:8000]}

【章节结构】
{json.dumps(plan, ensure_ascii=False, indent=2)}

【写作要求】

叙述方式：
- 用第三人称讲述历史事件，让事实推动叙述
- 每个段落必须包含具体的事实（时间、人名、数字、对话、事件经过）
- 先把事情讲清楚，再给评价；不要用评价代替叙述
- 用具体场景或细节开头，不要用抽象抒情

作者视角：
- 作者评价穿插在叙述中，用自然的口语表达
- 如果 personal_insertion_points 中标记了作者经历，自然融入对应位置
- 如果没有标记，用第三人称叙述 + 作者观点评价，不要虚构第一人称经历

语言：
- 口语化但不油腻，幽默但不硬造段子
- 段落长度由内容决定，避免所有段落一样长

结尾：
- 用具体的悬念或事实钩子引向下一章
- 章节结尾前加一条趣味冷知识（斜体，一两句话）

【坚决不要做的事】
1. 不要使用【来源：...】【核心史料】【参考底稿】等标签
2. 不要虚构假的第一人称经历
3. 不要在一个段落中堆砌2个以上口头禅或修辞
4. 不要在相邻段落重复同一个句式
5. 不要用设问-自答连击（"这叫什么？这就叫XXX"）
6. 不要在缺乏论证时强行哲学升华
7. 不要用括号插入感想
8. 不要让所有段落长度差不多
9. 不要在一段话里堆砌多个强调词
10. 不要用套路结尾（"让我们拭目以待"）

请直接输出正文（Markdown格式），包含 H1 标题和分节："""

        try:
            if self._use_claude:
                content = self.client.generate(prompt, timeout=600)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.75,
                )
                content = response.choices[0].message.content
            if not content:
                return "Writer error: empty response"
            # Strip markdown code block wrappers if present
            content = content.strip()
            if content.startswith("```markdown"):
                content = content[len("```markdown"):].strip()
            if content.startswith("```"):
                content = content[3:].strip()
            if content.endswith("```"):
                content = content[:-3].strip()
            return content
        except Exception as e:
            return f"Writer error: {e}"


def create_client(api_key=None, base_url=None, backend=None):
    """
    创建 AI 客户端。
    backend="claude-code" 时返回 ClaudeCodeClient（使用 Max 计划额度）。
    backend="openrouter" 时返回 OpenAI client（API 付费）。
    默认读取环境变量 REWRITE_BACKEND，未设置则使用 claude-code。
    """
    backend = backend or os.environ.get("REWRITE_BACKEND", "claude-code")

    if backend == "claude-code":
        return ClaudeCodeClient  # 返回类本身，由调用方实例化时指定 model
    else:
        from openai import OpenAI
        return OpenAI(
            base_url=base_url or config.OPENROUTER_BASE_URL,
            api_key=api_key or config.OPENROUTER_API_KEY,
        )
