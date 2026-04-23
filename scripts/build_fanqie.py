#!/usr/bin/env python3
"""
将 正文/ 下所有章节转换为番茄小说纯文本格式。

用法:
    python3 scripts/build_fanqie.py              # 基础转换（删markdown，拼接）
    python3 scripts/build_fanqie.py --merge       # 基础转换 + AI段落合并
    python3 scripts/build_fanqie.py --merge --ch 1 5  # 只合并第1和第5章（其余用缓存）
"""

import argparse
import re
import os
import glob
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SOURCE_DIR = PROJECT_ROOT / '正文'
OUTPUT_FILE = PROJECT_ROOT / '番茄小说版.txt'
CACHE_DIR = PROJECT_ROOT / '番茄版'

MERGE_PROMPT = """请将以下番茄小说章节的段落按语意合并，使其更适合手机阅读。

合并规则：
1. 小节标题保留独立成行（如"3000册书"、"第一个接棒的人"）
2. 戏剧短句不独立成段，融入前后叙事流（如"差一点。""谈判破裂了。"应并入相邻段落）
3. 引文/金句不独立成段，融入引出它的段落
4. 每段应是一个完整叙事单元，目标100-250字
5. 同场景/同话题的连续短段必须合并
6. 章节末尾的冷知识注脚和收束段合并为一段
7. 章节标题行（第X章 ...）保持不变

严格要求：
- 不要修改、删除或添加任何文字内容，只调整段落的合并
- 不要添加任何标记、注释或说明文字
- 直接输出合并后的纯文本，不要用代码块包裹

以下是需要合并的章节内容：

"""


def get_chapter_files():
    """按编号排序返回所有章节文件，特别篇放最后。"""
    files = glob.glob(str(SOURCE_DIR / '*.md'))
    files = [f for f in files if os.path.basename(f) != 'README.md']

    numbered = []
    special = []
    for f in files:
        basename = os.path.basename(f)
        if basename.startswith('特别篇'):
            special.append(f)
        else:
            match = re.match(r'(\d+)_', basename)
            if match:
                numbered.append((int(match.group(1)), f))

    numbered.sort(key=lambda x: x[0])
    return numbered, special


def make_title(num, filepath):
    """从文件名生成番茄章节标题。"""
    basename = os.path.splitext(os.path.basename(filepath))[0]

    if num == 0:
        title = re.sub(r'^\d+_引子[：:]', '', basename)
        return f'序章 {title}'
    else:
        # 去掉编号前缀，简化"篇章名：章名"为"章名"（如果有冒号）
        title = re.sub(r'^\d+_', '', basename)
        # "创世纪：预言与失败" → "预言与失败"
        if '：' in title:
            title = title.split('：', 1)[1]
        elif ':' in title:
            title = title.split(':', 1)[1]
        return f'第{num}章 {title}'


def make_special_title(filepath):
    basename = os.path.splitext(os.path.basename(filepath))[0]
    return basename


def clean_body(content):
    """清理 markdown 格式，提取纯文本正文。"""
    lines = content.split('\n')
    result = []
    skip_header = True
    in_intro_quote = False

    for line in lines:
        stripped = line.strip()

        # --- 跳过文件头部区域 ---
        if skip_header:
            if stripped.startswith('#') and not stripped.startswith('#批注'):
                continue
            if stripped.startswith('!['):
                continue
            if stripped.startswith('>'):
                in_intro_quote = True
                continue
            if in_intro_quote and stripped == '':
                continue
            if in_intro_quote and not stripped.startswith('>'):
                in_intro_quote = False
                skip_header = False
                if stripped == '':
                    continue
            elif stripped == '':
                continue
            else:
                skip_header = False

        # --- 跳过批注行 ---
        if stripped.startswith('#批注'):
            continue

        # --- 处理正文 ---

        # 删除 HTML 块（页脚）
        if re.match(r'</?div', stripped) or re.match(r'<a\s+href', stripped):
            continue

        # 分隔线 → 空行
        if stripped == '---':
            if result and result[-1] != '':
                result.append('')
            continue

        # ## 小节标题 → 纯文本
        if stripped.startswith('## '):
            stripped = stripped[3:]
            line = stripped

        # > 引用 → 去掉引用符号
        if stripped.startswith('> '):
            line = stripped[2:]
        elif stripped == '>':
            line = ''

        # 删除加粗 **text**
        line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)

        # 删除斜体 *text*（不误删 **）
        line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', line)

        # 删除链接 [text](url) → 保留 text
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)

        # 删除行尾的 markdown 硬换行
        line = line.rstrip()

        result.append(line)

    # 清理尾部空行
    while result and result[-1] == '':
        result.pop()

    # 压缩连续空行
    cleaned = []
    prev_empty = False
    for line in result:
        if line == '':
            if prev_empty:
                continue
            prev_empty = True
        else:
            prev_empty = False
        cleaned.append(line)

    return '\n'.join(cleaned)


def merge_paragraphs(text, chapter_id):
    """调用 Claude CLI 按语意合并段落，结果缓存到 番茄版/ 目录。"""
    cache_file = CACHE_DIR / f'{chapter_id}.txt'

    prompt = MERGE_PROMPT + text
    cmd = [
        'claude', '-p',
        '--model', 'sonnet',
        '--output-format', 'text',
        '--no-session-persistence',
    ]
    try:
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            print(f'    Warning: merge failed for {chapter_id}: {result.stderr[:200]}')
            return text
        merged = result.stdout.strip()
        if not merged:
            print(f'    Warning: empty merge result for {chapter_id}, using original')
            return text
    except subprocess.TimeoutExpired:
        print(f'    Warning: merge timed out for {chapter_id}, using original')
        return text
    except FileNotFoundError:
        print('    Error: claude command not found, skipping merge')
        return text

    # 缓存结果
    cache_file.write_text(merged, encoding='utf-8')
    return merged


def main():
    parser = argparse.ArgumentParser(description='Build 番茄小说版')
    parser.add_argument('--merge', action='store_true', help='AI段落合并（调用Claude）')
    parser.add_argument('--ch', type=int, nargs='*', help='只合并指定章节（其余用缓存），如 --ch 1 5 10')
    args = parser.parse_args()

    numbered, specials = get_chapter_files()
    CACHE_DIR.mkdir(exist_ok=True)

    # 确定哪些章节需要重新合并
    merge_set = None
    if args.ch is not None:
        merge_set = set(args.ch)

    parts = []

    for num, filepath in numbered:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        title = make_title(num, filepath)
        body = clean_body(content)
        chapter_text = f'{title}\n\n{body}'

        if args.merge:
            chapter_id = f'ch{num:02d}'
            cache_file = CACHE_DIR / f'{chapter_id}.txt'

            if merge_set is not None and num not in merge_set:
                # 不在指定列表中，用缓存
                if cache_file.exists():
                    chapter_text = cache_file.read_text(encoding='utf-8')
                    print(f'  ch{num:02d}: 使用缓存')
                else:
                    print(f'  ch{num:02d}: 无缓存，执行合并...')
                    chapter_text = merge_paragraphs(chapter_text, chapter_id)
            else:
                # 需要合并
                print(f'  ch{num:02d}: 合并中...')
                chapter_text = merge_paragraphs(chapter_text, chapter_id)

        parts.append(chapter_text)

    for filepath in specials:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
        title = make_special_title(filepath)
        body = clean_body(content)
        chapter_text = f'{title}\n\n{body}'

        if args.merge:
            chapter_id = 'special'
            cache_file = CACHE_DIR / f'{chapter_id}.txt'

            if merge_set is not None and -1 not in merge_set:
                if cache_file.exists():
                    chapter_text = cache_file.read_text(encoding='utf-8')
                    print(f'  特别篇: 使用缓存')
                else:
                    print(f'  特别篇: 无缓存，执行合并...')
                    chapter_text = merge_paragraphs(chapter_text, chapter_id)
            else:
                print(f'  特别篇: 合并中...')
                chapter_text = merge_paragraphs(chapter_text, chapter_id)

        parts.append(chapter_text)

    output = '\n\n\n'.join(parts) + '\n'

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'\n已生成: {OUTPUT_FILE}')
    print(f'共 {len(parts)} 章')
    total_chars = sum(len(p) for p in parts)
    print(f'总字符数: {total_chars:,}')


if __name__ == '__main__':
    main()
