#!/usr/bin/env python3
"""为《比特币那些事儿》封面图添加标题文字"""

from PIL import Image, ImageDraw, ImageFont
import os

# 路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT = os.path.join(PROJECT_DIR, "img", "封皮.png")
OUTPUT = os.path.join(PROJECT_DIR, "img", "封皮_标题.png")

# 字体
SONGTI = "/System/Library/Fonts/Supplemental/Songti.ttc"
HIRAGINO = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def add_gradient(img, y_start, y_end, base_color=(15, 18, 30), max_alpha=190, direction="down"):
    """添加渐变遮罩提升文字可读性"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    height = y_end - y_start
    for y in range(height):
        if direction == "down":
            alpha = int(max_alpha * (1 - y / height) ** 1.5)
        else:
            alpha = int(max_alpha * (y / height) ** 1.5)
        r, g, b = base_color
        draw.line([(0, y_start + y), (img.width, y_start + y)], fill=(r, g, b, alpha))
    return Image.alpha_composite(img, overlay)


def draw_text_shadow(draw, xy, text, font, fill, shadow_blur=3):
    """带阴影的文字绘制"""
    x, y = xy
    # 绘制阴影层
    shadow_color = (0, 0, 0, 120)
    for dx in range(-shadow_blur, shadow_blur + 1):
        for dy in range(-shadow_blur, shadow_blur + 1):
            if abs(dx) + abs(dy) <= shadow_blur + 1:
                draw.text((x + dx, y + dy), text, font=font, fill=shadow_color)
    # 绘制主文字
    draw.text((x, y), text, font=font, fill=fill)


def draw_spaced_text(draw, center_x, y, text, font, fill, spacing=0, shadow=True):
    """带字间距的居中文字"""
    if spacing == 0:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = center_x - tw / 2
        if shadow:
            draw_text_shadow(draw, (x, y), text, font, fill)
        else:
            draw.text((x, y), text, font=font, fill=fill)
        return

    # 计算带间距的总宽度
    char_widths = [font.getlength(c) for c in text]
    total_w = sum(char_widths) + spacing * (len(text) - 1)
    x = center_x - total_w / 2

    for i, char in enumerate(text):
        if shadow:
            draw_text_shadow(draw, (x, y), char, font, fill)
        else:
            draw.text((x, y), char, font=font, fill=fill)
        x += char_widths[i] + spacing


def make_cover():
    img = Image.open(INPUT).convert("RGBA")
    w, h = img.size
    print(f"原图尺寸: {w}x{h}")

    # 加载字体
    title_font = ImageFont.truetype(SONGTI, size=78, index=0)      # Songti SC Black
    subtitle_font = ImageFont.truetype(SONGTI, size=30, index=3)    # Songti SC Light
    author_font = ImageFont.truetype(HIRAGINO, size=22, index=0)    # Hiragino Sans W3

    # 添加顶部渐变（让标题可读）
    img = add_gradient(img, 0, 350, base_color=(15, 18, 30), max_alpha=200, direction="down")
    # 添加底部渐变（让作者名可读）
    img = add_gradient(img, h - 180, h, base_color=(15, 18, 30), max_alpha=180, direction="up")

    draw = ImageDraw.Draw(img)
    cx = w / 2  # 水平居中点

    # === 标题：比特币那些事儿 ===
    title = "比特币那些事儿"
    title_color = (255, 250, 240)  # 暖白色
    draw_spaced_text(draw, cx, 70, title, title_font, title_color, spacing=12)

    # === 分隔线 ===
    line_y = 170
    line_w = 260
    line_color = (212, 165, 90, 200)  # 琥珀色
    draw.line([(cx - line_w / 2, line_y), (cx + line_w / 2, line_y)], fill=line_color, width=2)

    # === 副标题：一束照进现实的理想之光 ===
    subtitle = "一束照进现实的理想之光"
    subtitle_color = (212, 175, 100)  # 琥珀金
    draw_spaced_text(draw, cx, 190, subtitle, subtitle_font, subtitle_color, spacing=6)

    # === 作者 ===
    author = "beihaili  著"
    author_color = (190, 190, 200, 230)
    draw_spaced_text(draw, cx, h - 65, author, author_font, author_color, spacing=4, shadow=False)

    # 保存
    img = img.convert("RGB")
    img.save(OUTPUT, quality=95)
    print(f"封面已保存: {OUTPUT}")


if __name__ == "__main__":
    make_cover()
