"""
Prompt template builder for the overnight iteration system.

Builds self-contained prompts for Claude CLI based on task type.
Each prompt includes: task context, file contents, and a CONSTRAINTS block.

The executor (Task 5) passes these prompts via stdin to Claude CLI.
"""

from typing import Any


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_prompt(task: dict[str, Any], file_contents: dict[str, str]) -> str:
    """
    Dispatch to type-specific prompt builder and append shared CONSTRAINTS block.

    Args:
        task: Task dict with at minimum {"type": str, "target": str}.
        file_contents: Mapping of filename → file text to embed in the prompt.

    Returns:
        A fully self-contained prompt string ready to pass to Claude CLI.
    """
    task_type = task.get("type", "")

    builders = {
        "code-lint": _build_code_lint,
        "code-ruff": _build_code_lint,   # same fix logic: address reported lint errors
        "code-test": _build_code_test,
        "code-refactor": _build_code_refactor,
        "content-refine": _build_content_refine,
        "pipeline-fix": _build_pipeline_fix,
    }

    builder = builders.get(task_type)
    if builder is None:
        raise ValueError(f"Unknown task type: {task_type!r}")

    body = builder(task, file_contents)
    constraints = _constraints_block(task)
    return f"{body}\n\n{constraints}"


# ---------------------------------------------------------------------------
# Type-specific builders
# ---------------------------------------------------------------------------


def _build_code_lint(task: dict, file_contents: dict) -> str:
    """Build prompt for ESLint error fixes."""
    target = task.get("target", "")
    description = task.get("description", "")
    details = task.get("details", "")

    files_section = _file_section(file_contents)

    return f"""You are a JavaScript/React developer. Fix all ESLint errors in the specified file.

## Task
Fix ESLint errors in `{target}`.

Summary: {description}
Errors: {details}

## Instructions
- Fix ONLY the reported ESLint errors listed above
- Do not change any logic or behavior
- Do not refactor or reorganize code beyond what is needed to fix the errors
- Preserve all existing comments

{files_section}"""


def _build_code_test(task: dict, file_contents: dict) -> str:
    """Build prompt for writing unit tests for a component."""
    target = task.get("target", "")
    description = task.get("description", "")

    # Extract component name from path (e.g. Timeline.jsx → Timeline)
    component = target.split("/")[-1].replace(".jsx", "").replace(".tsx", "").replace(".js", "")

    files_section = _file_section(file_contents)

    return f"""You are a frontend test engineer. Write unit tests for the specified React component.

## Task
Write unit tests for `{target}` ({component} component).

Reason: {description}

## Instructions
- Use Vitest + React Testing Library + jsdom
- Place the test file in `__tests__/` next to the source file
- Cover: rendering, user interactions, edge cases
- Mock `framer-motion` if the component uses animations (import from `__mocks__/framer-motion`)
- Each test should have a clear, descriptive name
- Tests must be independent and not rely on execution order

{files_section}"""


def _build_code_refactor(task: dict, file_contents: dict) -> str:
    """Build prompt for code readability refactoring."""
    target = task.get("target", "")
    description = task.get("description", "")

    files_section = _file_section(file_contents)

    return f"""You are a senior software engineer. Refactor the specified file for readability.

## Task
Refactor `{target}` to improve code readability.

Context: {description}

## Instructions
- Keep ALL existing functionality intact — behavior must not change
- All existing tests must continue to pass after refactoring
- Focus on: naming clarity, reducing nesting, extracting helpers, adding comments where helpful
- Do not add new features or change the public API

{files_section}"""


def _build_content_refine(task: dict, file_contents: dict) -> str:
    """Build prompt for Chinese chapter content refinement."""
    target = task.get("target", "")
    chapter_num = task.get("chapter_num", "")
    weakest_dim = task.get("weakest_dimension", "")
    weakest_score = task.get("weakest_score", "")
    weaknesses = task.get("weaknesses", [])
    suggestions = task.get("suggestions", [])
    scores = task.get("scores", {})

    # Format scores as readable list
    scores_text = "\n".join(f"  - {dim}: {score}/10" for dim, score in scores.items())

    # Format weaknesses and suggestions as bullet lists
    weaknesses_text = "\n".join(f"  - {w}" for w in weaknesses)
    suggestions_text = "\n".join(f"  - {s}" for s in suggestions)

    files_section = _file_section(file_contents)

    return f"""你是一位经验丰富的文学编辑，专门精修中文历史叙事类文章。

## 任务
精修第 {chapter_num} 章：`{target}`

## 当前评分
{scores_text}

## 最弱维度
**{weakest_dim}**：{weakest_score}/10（需要重点改善）

## 具体问题
{weaknesses_text}

## 修改建议
{suggestions_text}

## 操作要求
- 只针对上述具体问题进行修订，不要重写整章
- 修改幅度控制在 20% 以内
- 保持原有的叙事风格和整体结构
- 不要改变历史事实和核心观点
- 不要添加新的章节或大段内容

{files_section}"""


def _build_pipeline_fix(task: dict, file_contents: dict) -> str:
    """Build prompt for fixing a bug in a pipeline/script."""
    target = task.get("target", "")
    description = task.get("description", "")
    details = task.get("details", description)  # Fall back to description if no details

    files_section = _file_section(file_contents)

    return f"""You are a Python developer. Fix the described bug in the specified script.

## Task
Fix bug in `{target}`.

Problem description: {details}

## Instructions
- Fix ONLY the described issue
- Do not refactor unrelated code
- Do not change the public interface or behavior for other cases
- Add a brief inline comment explaining the fix if the root cause is non-obvious

{files_section}"""


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _file_section(file_contents: dict[str, str]) -> str:
    """
    Format a dict of {filename: content} as markdown code blocks.

    Returns an empty string if file_contents is empty.
    """
    if not file_contents:
        return ""

    parts = ["## File Contents"]
    for filename, content in file_contents.items():
        # Guess language from extension for syntax highlighting
        ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
        lang = _ext_to_lang(ext)
        parts.append(f"### `{filename}`\n```{lang}\n{content}\n```")

    return "\n\n".join(parts)


def _ext_to_lang(ext: str) -> str:
    """Map file extension to markdown code fence language tag."""
    mapping = {
        "js": "javascript",
        "jsx": "jsx",
        "ts": "typescript",
        "tsx": "tsx",
        "py": "python",
        "md": "markdown",
        "json": "json",
        "css": "css",
        "html": "html",
        "sh": "bash",
        "yaml": "yaml",
        "yml": "yaml",
    }
    return mapping.get(ext.lower(), "")


def _constraints_block(task: dict) -> str:
    """
    Return the shared CONSTRAINTS block appended to every prompt.

    Tells Claude to only touch specified files and avoid noise.
    """
    target = task.get("target", "")
    return f"""## CONSTRAINTS
- Use the Edit or Write tool to modify files directly. Do NOT just output file contents as text.
- Only modify the specified file(s): `{target}`. Do not touch any other files.
- Do not add comments describing what you changed (no "// Fixed:", "# Changed:" etc.)
- Do not refactor beyond what is needed for this specific task"""
