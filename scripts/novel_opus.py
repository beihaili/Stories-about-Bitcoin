#!/usr/bin/env python3
"""Call Claude Opus for the novel workflow without storing secrets in code."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORY_ROOT = PROJECT_ROOT / "我给中本聪送外卖"
SOURCE_CHAPTERS_ROOT = PROJECT_ROOT / "正文"

DEFAULT_BASE_URL = "https://api.derouter.ai/proxy"
DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TIMEOUT = 180

BASE_CONTEXT_FILES = [
    "我给中本聪送外卖/CLAUDE.md",
    "我给中本聪送外卖/设定/结构/故事骨架.md",
    "我给中本聪送外卖/设定/结构/38章分工表.md",
    "我给中本聪送外卖/设定/规则/穿越规则.md",
    "我给中本聪送外卖/设定/暗线/中本聪账号.md",
    "我给中本聪送外卖/设定/人物/李觉.md",
    "我给中本聪送外卖/设定/人物/陈浩.md",
    "我给中本聪送外卖/设定/人物/母亲.md",
    "我给中本聪送外卖/设定/人物/赵晴.md",
]


def project_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_env_file(path_value: str | None) -> None:
    if not path_value:
        return

    path = project_path(path_value)
    if not path.exists():
        raise SystemExit(f"Env file not found: {path}")

    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def first_match(directory: Path, pattern: str) -> str | None:
    matches = sorted(directory.glob(pattern))
    if not matches:
        return None
    try:
        return str(matches[0].relative_to(PROJECT_ROOT))
    except ValueError:
        return str(matches[0])


def default_context_files(chapter: int | None, previous_chapters: int) -> list[str]:
    files = list(BASE_CONTEXT_FILES)

    if chapter:
        source = first_match(SOURCE_CHAPTERS_ROOT, f"{chapter:02d}_*.md")
        if source:
            files.append(source)

        anchor = first_match(STORY_ROOT / "设定" / "历史锚点", f"{chapter:02d}_*.md")
        if anchor:
            files.append(anchor)

        start = max(1, chapter - previous_chapters)
        for index in range(start, chapter):
            previous = first_match(STORY_ROOT / "正文", f"{index:02d}_*.md")
            if previous:
                files.append(previous)

    return files


def context_block(paths: list[str]) -> str:
    blocks = []
    seen = set()

    for value in paths:
        if value in seen:
            continue
        seen.add(value)

        path = project_path(value)
        if not path.exists():
            blocks.append(f'<file path="{value}" missing="true" />')
            continue

        blocks.append(
            f'<file path="{value}">\n{read_text(path).rstrip()}\n</file>'
        )

    return "\n\n".join(blocks)


def build_draft_prompt(
    chapter: int,
    contract: str,
    beats: str,
    context_files: list[str],
) -> str:
    return f"""你是《我给中本聪送外卖》的正文起草 Agent，由 Claude Opus 承担。

<任务>
根据章节合同和 scene beats 写第 {chapter:02d} 章正文初稿。
只输出小说正文，不输出解释、提纲、审稿报告或 Markdown 标题。
</任务>

<风格>
- 第三人称限知，镜头跟着李觉。
- 番茄小说段落节奏：段落短，叙事推进快，但不要口号化。
- 现实段冷峻一点，允许黑色幽默；历史段要有现场感。
- 不自夸，不煽情，不讲课。
- 少用“他意识到 / 他明白了 / 这意味着”，用动作、账单、物件、对话体现变化。
</风格>

<硬约束>
- 不改变历史走向。
- 不让李觉告诉历史人物未来。
- 每章最多带回一件合规小物件；如果合同写明无物件，就不能新增。
- 人物说话必须符合人物档案。
- 中本聪账号出现频率要克制，按章节合同执行。
</硬约束>

<必要上下文>
{context_block(context_files)}
</必要上下文>

<章节合同>
{contract.rstrip()}
</章节合同>

<scene_beats>
{beats.rstrip()}
</scene_beats>

现在开始写正文。"""


def build_edit_prompt(draft: str, context_files: list[str]) -> str:
    return f"""你是《我给中本聪送外卖》的文学编辑 Agent，由 Claude Opus 承担。

<任务>
在不改变剧情事实、不新增重大情节的前提下，润色下面正文。
只输出润色后的完整正文。
</任务>

<编辑目标>
- 去掉解释腔和 AI 腔。
- 把抽象判断改成可感知细节。
- 让现实段更冷，穿越段更有现场感。
- 保持第三人称限知。
- 保持番茄小说段落节奏。
- 不要把人物改成观点传声筒。
</编辑目标>

<禁止>
- 禁止新增重大设定。
- 禁止改变历史事实。
- 禁止让李觉说出他不该知道的信息。
- 禁止把陈浩、赵晴、母亲写成工具人。
</禁止>

<必要上下文>
{context_block(context_files)}
</必要上下文>

<正文>
{draft.rstrip()}
</正文>"""


def split_text_by_chars(text: str, max_chars: int) -> list[str]:
    if max_chars <= 0 or len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    size = 0

    for line in text.splitlines(keepends=True):
        if current and size + len(line) > max_chars:
            chunks.append("".join(current).rstrip())
            current = []
            size = 0
        current.append(line)
        size += len(line)

    if current:
        chunks.append("".join(current).rstrip())

    return [chunk for chunk in chunks if chunk.strip()]


def redact(text: str, secret: str | None) -> str:
    if secret:
        text = text.replace(secret, "[REDACTED_API_KEY]")
    return text


def api_key_from_env() -> str:
    key = (
        os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("DEROUTER_API_KEY")
        or os.environ.get("OPUS_API_KEY")
    )
    if not key:
        raise SystemExit(
            "Missing API key. Set ANTHROPIC_API_KEY in .env.local or the shell."
        )
    return key


def text_from_anthropic_message(message: object) -> str:
    parts = []
    for item in getattr(message, "content", []):
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts).strip()


def call_with_sdk(
    prompt: str,
    *,
    api_key: str,
    base_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> str | None:
    try:
        import anthropic  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        return None

    client = anthropic.Anthropic(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
    )
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return text_from_anthropic_message(message)


def call_with_http(
    prompt: str,
    *,
    api_key: str,
    base_url: str,
    model: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> str:
    url = base_url.rstrip("/") + "/v1/messages"
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": os.environ.get(
                "ANTHROPIC_USER_AGENT",
                "anthropic-python/0.0 novel-opus-local",
            ),
            "x-api-key": api_key,
            "authorization": f"Bearer {api_key}",
            "anthropic-version": os.environ.get(
                "ANTHROPIC_VERSION", "2023-06-01"
            ),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Anthropic HTTP {exc.code}: {redact(body, api_key)}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Anthropic request failed: {exc.reason}") from exc

    parsed = json.loads(raw)
    parts = [
        item.get("text", "")
        for item in parsed.get("content", [])
        if item.get("type") == "text" or "text" in item
    ]
    return "\n".join(part for part in parts if part).strip()


def auth_headers(api_key: str) -> dict[str, str]:
    return {
        "accept": "application/json",
        "user-agent": os.environ.get(
            "ANTHROPIC_USER_AGENT",
            "anthropic-python/0.0 novel-opus-local",
        ),
        "x-api-key": api_key,
        "authorization": f"Bearer {api_key}",
    }


def list_provider_models(timeout: int) -> object:
    api_key = api_key_from_env()
    base_url = os.environ.get("ANTHROPIC_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    candidates = [base_url + "/providers/models"]
    if base_url.endswith("/proxy"):
        candidates.append(base_url[: -len("/proxy")] + "/providers/models")

    last_error = None
    for url in candidates:
        request = urllib.request.Request(
            url,
            headers=auth_headers(api_key),
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            last_error = f"HTTP {exc.code} from {url}: {redact(body, api_key)}"
        except urllib.error.URLError as exc:
            last_error = f"Request failed for {url}: {exc.reason}"

    raise RuntimeError(last_error or "Could not fetch provider models.")


def iter_model_rows(payload: object) -> list[dict[str, object]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ("data", "models", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def call_anthropic(
    prompt: str,
    *,
    model: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> str:
    api_key = api_key_from_env()
    base_url = os.environ.get("ANTHROPIC_BASE_URL", DEFAULT_BASE_URL)

    sdk_result = call_with_sdk(
        prompt,
        api_key=api_key,
        base_url=base_url,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
    )
    if sdk_result is not None:
        return sdk_result

    return call_with_http(
        prompt,
        api_key=api_key,
        base_url=base_url,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
    )


def run_prompt(prompt: str, args: argparse.Namespace) -> None:
    if args.prompt_only:
        print(prompt)
        return

    model = args.model or os.environ.get("OPUS_MODEL") or DEFAULT_MODEL
    max_tokens = args.max_tokens or DEFAULT_MAX_TOKENS
    text = call_anthropic(
        prompt,
        model=model,
        max_tokens=max_tokens,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    output = getattr(args, "output", None)
    if output:
        write_text(project_path(output), text)
    else:
        print(text)


def command_ping(args: argparse.Namespace) -> None:
    prompt = "请用一句中文回复：Opus 接口可用。"
    run_prompt(prompt, args)


def command_models(args: argparse.Namespace) -> None:
    payload = list_provider_models(args.timeout)
    rows = iter_model_rows(payload)
    needle = (args.filter or "").lower()

    if not rows:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    for row in rows:
        values = [str(value) for value in row.values() if value is not None]
        haystack = " ".join(values).lower()
        if needle and needle not in haystack:
            continue

        model_id = row.get("id") or row.get("model") or row.get("name")
        provider = row.get("provider") or row.get("owner") or row.get("type")
        label = row.get("display_name") or row.get("label") or row.get("name")
        parts = [str(model_id)]
        if label and label != model_id:
            parts.append(str(label))
        if provider:
            parts.append(str(provider))
        print(" | ".join(parts))


def command_draft(args: argparse.Namespace) -> None:
    context_files = []
    if not args.no_default_context:
        context_files.extend(default_context_files(args.chapter, args.previous_chapters))
    context_files.extend(args.context_file or [])

    prompt = build_draft_prompt(
        args.chapter,
        read_text(project_path(args.contract_file)),
        read_text(project_path(args.beats_file)),
        context_files,
    )
    run_prompt(prompt, args)


def command_edit(args: argparse.Namespace) -> None:
    context_files = []
    if not args.no_default_context:
        context_files.extend(default_context_files(args.chapter, args.previous_chapters))
    context_files.extend(args.context_file or [])

    draft = read_text(project_path(args.draft))
    if args.input_chars:
        draft = draft[: args.input_chars].rstrip()

    if args.chunk_chars and not args.prompt_only:
        chunks = split_text_by_chars(draft, args.chunk_chars)
        outputs = []
        for index, chunk in enumerate(chunks, start=1):
            prompt = build_edit_prompt(chunk, context_files)
            text = call_anthropic(
                prompt,
                model=args.model or os.environ.get("OPUS_MODEL") or DEFAULT_MODEL,
                max_tokens=args.max_tokens or DEFAULT_MAX_TOKENS,
                temperature=args.temperature,
                timeout=args.timeout,
            )
            outputs.append(text)
            if args.output:
                write_text(project_path(args.output), "\n\n".join(outputs))
            print(f"edited chunk {index}/{len(chunks)}", file=sys.stderr)

        if not args.output:
            print("\n\n".join(outputs))
        return

    prompt = build_edit_prompt(draft, context_files)
    run_prompt(prompt, args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Claude Opus for the Bitcoin delivery novel workflow."
    )
    parser.add_argument("--env-file", help="Local env file, e.g. .env.local")
    parser.add_argument("--model", help="Override OPUS_MODEL for this run")
    parser.add_argument("--max-tokens", type=int, help="Response token budget")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="Print the prompt instead of calling the API",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    ping = subparsers.add_parser("ping", help="Verify API connectivity")
    ping.set_defaults(func=command_ping)

    models = subparsers.add_parser("models", help="List provider models")
    models.add_argument("--filter", default="", help="Case-insensitive model filter")
    models.set_defaults(func=command_models)

    draft = subparsers.add_parser("draft", help="Draft a chapter from contract/beats")
    draft.add_argument("--chapter", type=int, required=True)
    draft.add_argument("--contract-file", required=True)
    draft.add_argument("--beats-file", required=True)
    draft.add_argument("--output", help="Write response to this file")
    draft.add_argument("--context-file", action="append", default=[])
    draft.add_argument("--previous-chapters", type=int, default=2)
    draft.add_argument("--no-default-context", action="store_true")
    draft.set_defaults(func=command_draft)

    edit = subparsers.add_parser("edit", help="Style-edit an existing chapter")
    edit.add_argument("--draft", required=True)
    edit.add_argument("--chapter", type=int)
    edit.add_argument("--output", help="Write response to this file")
    edit.add_argument("--context-file", action="append", default=[])
    edit.add_argument("--previous-chapters", type=int, default=2)
    edit.add_argument("--no-default-context", action="store_true")
    edit.add_argument(
        "--input-chars",
        type=int,
        help="Only edit the first N characters; useful for short API tests",
    )
    edit.add_argument(
        "--chunk-chars",
        type=int,
        help="Split long drafts into paragraph-preserving chunks",
    )
    edit.set_defaults(func=command_edit)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    load_env_file(args.env_file)

    try:
        args.func(args)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
