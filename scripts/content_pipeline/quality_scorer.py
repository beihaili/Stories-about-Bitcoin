"""
Quality scoring gate for the content pipeline.

Scores chapters on 5 dimensions (1-10 each):
1. Factual accuracy — cross-checked against reference data
2. Style consistency — "Ming Dynasty" narrative voice
3. Readability — flow, pacing, sentence variety
4. Chapter coherence — structure, transitions, narrative arc
5. Terminology accuracy — Bitcoin/crypto terms used correctly

Average >= 7.0 → auto-proceed to translation
Average < 7.0 → flagged for human review
"""

import json
import re
from typing import Dict, List, Optional

from . import config


SCORING_PROMPT = """你是《比特币那些事儿》的质量审核编辑。请对以下章节进行五维评分。

【评分维度】（每项 1-10 分）
1. **factual_accuracy** — 事实准确性：日期、人物、事件是否与史料一致？是否有虚构或错误？
2. **style_consistency** — 风格一致性：是否保持"明朝那些事儿"风格？有无突然变调？用词是否口语化、有人味？
3. **readability** — 可读性：节奏是否流畅？句式是否多变？是否有冗长段落？开头是否吸引人？
4. **chapter_coherence** — 章节连贯性：结构是否清晰？过渡是否自然？叙事弧线是否完整？
5. **terminology_accuracy** — 术语准确性：比特币/加密货币专业术语是否使用正确？技术描述是否准确？

【评分标准】
- 9-10: 出版级别，几乎无需修改
- 7-8: 质量良好，小修即可
- 5-6: 需要较大改动
- 3-4: 需要大幅重写
- 1-2: 基本不可用

{reference_section}

【待评章节】
```
{chapter_text}
```

请严格以 JSON 格式输出，包含：
- scores: 包含5个维度的分数（整数）
- average: 平均分（保留1位小数）
- strengths: 优点列表（2-3条）
- weaknesses: 缺点列表（2-3条）
- suggestions: 改进建议列表（2-3条）
- verdict: "pass"（平均>=7）或 "review"（平均<7）"""


def build_reference_section(chapter_num: Optional[int] = None) -> str:
    """Build a reference section from available history data for fact-checking."""
    if chapter_num is None:
        return ""

    # Try to load relevant reference materials
    refs = []

    # Load timeline data for cross-checking
    timeline_path = config.KEY_RESOURCES_DIR / "bitcoin_complete_timeline.json"
    if timeline_path.exists():
        try:
            with open(timeline_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Extract just event summaries to keep prompt manageable
                events = []
                for key, val in data.items():
                    if isinstance(val, dict):
                        for ev in val.get("events", val.get("periods", [])):
                            if isinstance(ev, dict):
                                events.append(
                                    f"- {ev.get('date', '?')}: {ev.get('event', ev.get('title', '?'))}"
                                )
                if events:
                    refs.append("【时间线参考】\n" + "\n".join(events[:30]))
        except Exception:
            pass

    # Load key figures for name verification
    figures_path = config.KEY_RESOURCES_DIR / "key_figures.json"
    if figures_path.exists():
        try:
            with open(figures_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                refs.append(f"【人物参考】\n{json.dumps(data, ensure_ascii=False)[:2000]}")
        except Exception:
            pass

    if refs:
        return "【事实核查参考材料】\n" + "\n\n".join(refs)
    return ""


def score_chapter(
    client,
    model: str,
    chapter_text: str,
    chapter_num: Optional[int] = None,
) -> Dict:
    """
    Score a chapter using LLM-based quality assessment.

    Returns dict with scores, average, strengths, weaknesses, suggestions, verdict.
    """
    reference_section = build_reference_section(chapter_num)
    prompt = SCORING_PROMPT.format(
        reference_section=reference_section,
        chapter_text=chapter_text[:12000],  # Limit to avoid token overflow
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Low temperature for consistent scoring
        )
        content = response.choices[0].message.content
        result = _parse_score_response(content)

        # Validate and enforce threshold
        avg = result.get("average", 0)
        result["verdict"] = "pass" if avg >= config.QUALITY_AUTO_PASS else "review"
        result["threshold"] = config.QUALITY_AUTO_PASS

        return result

    except Exception as e:
        return {
            "error": str(e),
            "scores": {},
            "average": 0,
            "verdict": "error",
        }


def _parse_score_response(content: str) -> Dict:
    """Parse the scoring LLM's JSON response."""
    try:
        # Extract JSON from potential markdown wrapping
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        match = re.search(r"\{.*\}", content, re.S)
        if match:
            content = match.group(0)

        result = json.loads(content)

        # Validate scores
        scores = result.get("scores", {})
        for dim in config.QUALITY_DIMENSIONS:
            if dim in scores:
                scores[dim] = max(1, min(10, int(scores[dim])))

        # Recalculate average from actual scores
        if scores:
            result["average"] = round(sum(scores.values()) / len(scores), 1)

        return result

    except Exception:
        return {
            "scores": {},
            "average": 0,
            "strengths": [],
            "weaknesses": ["Failed to parse scoring response"],
            "suggestions": ["Retry scoring"],
            "raw_response": content[:500],
        }


def format_score_report(result: Dict, chapter_title: str = "") -> str:
    """Format scoring results as a readable report."""
    lines = []
    lines.append(f"# Quality Score Report{f': {chapter_title}' if chapter_title else ''}")
    lines.append("")

    verdict = result.get("verdict", "unknown")
    avg = result.get("average", 0)
    threshold = result.get("threshold", config.QUALITY_AUTO_PASS)
    status = "PASS" if verdict == "pass" else "NEEDS REVIEW" if verdict == "review" else "ERROR"
    lines.append(f"**Verdict: {status}** (average {avg}/10, threshold {threshold})")
    lines.append("")

    scores = result.get("scores", {})
    if scores:
        lines.append("## Dimension Scores")
        lines.append("")
        dim_labels = {
            "factual_accuracy": "Factual Accuracy",
            "style_consistency": "Style Consistency",
            "readability": "Readability",
            "chapter_coherence": "Chapter Coherence",
            "terminology_accuracy": "Terminology Accuracy",
        }
        for dim, label in dim_labels.items():
            score = scores.get(dim, "?")
            bar = "█" * int(score) + "░" * (10 - int(score)) if isinstance(score, (int, float)) else ""
            lines.append(f"- {label}: **{score}/10** {bar}")
        lines.append("")

    for section, label in [
        ("strengths", "Strengths"),
        ("weaknesses", "Weaknesses"),
        ("suggestions", "Improvement Suggestions"),
    ]:
        items = result.get(section, [])
        if items:
            lines.append(f"## {label}")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

    return "\n".join(lines)


def save_score(result: Dict, chapter_num: int, output_dir=None):
    """Save score result to JSON file."""
    out_dir = output_dir or config.SCORE_OUTPUT
    out_dir.mkdir(parents=True, exist_ok=True)

    filepath = out_dir / f"score_ch{chapter_num:02d}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Also save markdown report
    report = format_score_report(result, f"Chapter {chapter_num}")
    md_path = out_dir / f"score_ch{chapter_num:02d}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)

    return filepath
