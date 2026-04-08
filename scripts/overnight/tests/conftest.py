"""Shared fixtures for overnight tests."""
import json
import pytest
from pathlib import Path


@pytest.fixture
def tmp_run_dir(tmp_path):
    """A temporary run directory with standard structure."""
    run_dir = tmp_path / "runs" / "2026-04-08"
    run_dir.mkdir(parents=True)
    return run_dir


@pytest.fixture
def sample_findings():
    """Sample findings data for testing planner."""
    return {
        "code": [
            {
                "type": "code-lint",
                "severity": 8,
                "target": "new-website/src/App.jsx",
                "description": "3 ESLint errors",
                "details": "no-unused-vars (2), react/prop-types (1)",
            },
            {
                "type": "code-test",
                "severity": 6,
                "target": "new-website/src/components/home/Timeline.jsx",
                "description": "No test file exists",
                "details": "Component has 120 lines, 0% coverage",
            },
        ],
        "content": [
            {
                "type": "content-refine",
                "severity": 7,
                "target": "正文/11_风起云涌：第一次泡沫.md",
                "chapter_num": 11,
                "description": "readability: 5/10",
                "weaknesses": ["段落长度单一", "开头缺乏画面感"],
                "suggestions": ["增加句式变化", "用具体场景开头"],
                "scores": {"readability": 5, "style_consistency": 7, "factual_accuracy": 8,
                           "chapter_coherence": 7, "terminology_accuracy": 8},
                "average": 7.0,
                "weakest_dimension": "readability",
                "weakest_score": 5,
            },
        ],
    }


@pytest.fixture
def sample_findings_md(tmp_run_dir, sample_findings):
    """Write sample findings to findings.md and return path."""
    lines = ["# Findings — 2026-04-08\n"]
    for category in ("code", "content"):
        lines.append(f"\n## {category.title()} Issues\n")
        for f in sample_findings[category]:
            lines.append(f"### [{f['severity']}] {f['type']}: {f['target']}")
            lines.append(f"- **Description**: {f['description']}")
            lines.append(f"- **Details**: {f.get('details', 'N/A')}")
            lines.append("")
    path = tmp_run_dir / "findings.md"
    path.write_text("\n".join(lines))

    json_path = tmp_run_dir / "findings.json"
    json_path.write_text(json.dumps(sample_findings, ensure_ascii=False, indent=2))
    return path
