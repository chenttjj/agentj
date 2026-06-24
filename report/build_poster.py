#!/usr/bin/env python3
"""Build Mood Beat 專題海報.png (portrait 2:3) via Pillow composite."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPORT_DIR = Path("report")
ASSETS = REPORT_DIR / "assets"
OUT = ASSETS / "專題海報.png"

# 2:3 portrait poster
W, H = 1200, 1800
SAGE = (135, 150, 115)
TERRACOTTA = (200, 106, 79)
CREAM = (245, 239, 228)
DARK = (51, 51, 51)
WHITE = (255, 255, 255)

canvas = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(canvas)

# 嘗試找中文字型
def get_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\msjh.ttc",
        r"C:\Windows\Fonts\msjhbd.ttc",
        r"C:\Windows\Fonts\NotoSansCJK-Bold.ttc",
        r"C:\Windows\Fonts\NotoSansCJK-Regular.ttc",
        r"C:\Windows\Fonts\kaiu.ttf",
        r"C:\Windows\Fonts\mingliu.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_h1 = get_font(96, bold=True)
font_h2 = get_font(40, bold=True)
font_h3 = get_font(32, bold=True)
font_body = get_font(22)
font_small = get_font(18)

# 上方 terracotta 橫條
draw.rectangle([0, 0, W, 16], fill=TERRACOTTA)

# 標題區
y = 80
draw.text((W // 2, y), "Mood Beat", fill=TERRACOTTA, font=font_h1, anchor="mm")
y += 110
draw.text((W // 2, y), "心情 × 呼吸 × 音樂", fill=SAGE, font=font_h2, anchor="mm")
y += 55
draw.text((W // 2, y), "你的專屬節奏", fill=DARK, font=font_body, anchor="mm")
y += 35
draw.text((W // 2, y), "馬公高中 Agent Studio 專題", fill=DARK, font=font_small, anchor="mm")

# 簡介區塊
y += 50
draw.rectangle([60, y, W - 60, y + 4], fill=SAGE)
y += 30
intro_lines = [
    "「Mood Beat」讓使用者輸入心情值、壓力值與音樂偏好，",
    "透過呼吸穩定節奏，再由 AI 推薦專屬音樂風格，",
    "幫助面臨壓力、心情低落的使用者達到紓壓與放鬆。",
]
for line in intro_lines:
    draw.text((W // 2, y), line, fill=DARK, font=font_body, anchor="mm")
    y += 36

# Server 拓撲圖
y += 20
draw.text((W // 2, y), "■ 學校 Server 環境", fill=TERRACOTTA, font=font_h3, anchor="mm")
y += 30
img = Image.open(ASSETS / "server-topology.png")
ratio = min((W - 160) / img.width, 460 / img.height)
new_w, new_h = int(img.width * ratio), int(img.height * ratio)
img_resized = img.resize((new_w, new_h), Image.LANCZOS)
canvas.paste(img_resized, ((W - new_w) // 2, y))
y += new_h + 20

# 個人架構圖
draw.text((W // 2, y), "■ Mood Beat 個人架構", fill=TERRACOTTA, font=font_h3, anchor="mm")
y += 30
img = Image.open(ASSETS / "project-architecture.png")
ratio = min((W - 160) / img.width, 460 / img.height)
new_w, new_h = int(img.width * ratio), int(img.height * ratio)
img_resized = img.resize((new_w, new_h), Image.LANCZOS)
canvas.paste(img_resized, ((W - new_w) // 2, y))
y += new_h + 20

# Demo 截圖
if y < H - 380:
    draw.text((W // 2, y), "■ Demo 截圖", fill=TERRACOTTA, font=font_h3, anchor="mm")
    y += 30
    img = Image.open(ASSETS / "demo-02.png")
    ratio = min((W - 160) / img.width, 380 / img.height)
    new_w, new_h = int(img.width * ratio), int(img.height * ratio)
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas.paste(img_resized, ((W - new_w) // 2, y))
    y += new_h + 20

# 下方頁尾
draw.rectangle([0, H - 16, W, H], fill=TERRACOTTA)
draw.text((W // 2, H - 60), "成果 · 創新 · 技術",
          fill=DARK, font=font_h3, anchor="mm")
draw.text((W // 2, H - 28), "結合情緒紀錄、呼吸穩定、音樂推薦於一體",
          fill=DARK, font=font_small, anchor="mm")

canvas.save(OUT, "PNG", optimize=True)
print(f"OK: {OUT}")
