"""Tests for prompt template builder."""


def test_build_code_lint_prompt():
    from scripts.overnight.prompts import build_prompt
    task = {
        "type": "code-lint",
        "target": "new-website/src/App.jsx",
        "description": "3 ESLint errors",
        "details": "no-unused-vars (2), react/prop-types (1)",
    }
    prompt = build_prompt(task, file_contents={"App.jsx": "const x = 1;"})
    assert "lint" in prompt.lower() or "ESLint" in prompt
    assert "App.jsx" in prompt
    assert "no-unused-vars" in prompt


def test_build_content_refine_prompt():
    from scripts.overnight.prompts import build_prompt
    task = {
        "type": "content-refine",
        "target": "正文/11_test.md",
        "chapter_num": 11,
        "weakest_dimension": "readability",
        "weakest_score": 5,
        "weaknesses": ["段落长度单一", "开头缺乏画面感"],
        "suggestions": ["增加句式变化", "用具体场景开头"],
        "scores": {"readability": 5, "style_consistency": 7},
    }
    prompt = build_prompt(task, file_contents={"11_test.md": "# 章节内容"})
    assert "readability" in prompt
    assert "5" in prompt
    assert "段落长度单一" in prompt
    assert "20%" in prompt  # Modification limit


def test_build_code_test_prompt():
    from scripts.overnight.prompts import build_prompt
    task = {
        "type": "code-test",
        "target": "new-website/src/components/home/Timeline.jsx",
        "description": "No test file exists",
    }
    prompt = build_prompt(task, file_contents={"Timeline.jsx": "export default function Timeline() {}"})
    assert "test" in prompt.lower()
    assert "Timeline" in prompt


def test_all_prompts_include_constraint():
    from scripts.overnight.prompts import build_prompt
    for task_type in ("code-lint", "code-test", "code-refactor", "content-refine", "pipeline-fix"):
        task = {"type": task_type, "target": "test.js", "description": "test"}
        prompt = build_prompt(task, file_contents={})
        # Must tell Claude to only modify specified files
        assert "only" in prompt.lower() or "不要" in prompt or "specified" in prompt.lower() or "CONSTRAINT" in prompt
