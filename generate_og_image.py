#!/usr/bin/env python3
"""Generate og-image.png 1200x630 for clean-clean.com.ua"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BASE = os.path.dirname(os.path.abspath(__file__))

# Colors (brand palette)
BG       = (22, 101, 52)   # #166534 dark green
ACCENT   = (34, 197, 94)   # #22c55e light green
WHITE    = (255, 255, 255)
LIGHT    = (220, 252, 231) # #dcfce7

img  = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# ─── background decoration ───────────────────────────────────────────────
# subtle circle top-right
for r in range(320, 80, -40):
    alpha = int(15 + (320 - r) * 0.05)
    draw.ellipse([(W - r, -r), (W + r, r)], outline=(*ACCENT, alpha))

# bottom-left circle
for r in range(260, 60, -40):
    draw.ellipse([(-r, H - r), (r, H + r)], outline=(*ACCENT, 8))

# ─── logo square (top-left) ──────────────────────────────────────────────
logo_x, logo_y, logo_sz = 80, 80, 72
draw.rounded_rectangle(
    [(logo_x, logo_y), (logo_x + logo_sz, logo_y + logo_sz)],
    radius=14, fill=ACCENT
)

# "CC" text in logo
try:
    font_logo = ImageFont.truetype("arialbd.ttf", 30)
except:
    font_logo = ImageFont.load_default()

draw.text((logo_x + 10, logo_y + 18), "CC", fill=WHITE, font=font_logo)

# ─── brand name ──────────────────────────────────────────────────────────
try:
    font_brand  = ImageFont.truetype("arialbd.ttf", 34)
    font_title  = ImageFont.truetype("arialbd.ttf", 72)
    font_sub    = ImageFont.truetype("arial.ttf",   34)
    font_badge  = ImageFont.truetype("arialbd.ttf", 24)
    font_small  = ImageFont.truetype("arial.ttf",   22)
except:
    font_brand = font_title = font_sub = font_badge = font_small = ImageFont.load_default()

draw.text((logo_x + logo_sz + 16, logo_y + 18), "Clean-Clean", fill=WHITE, font=font_brand)

# ─── main headline ───────────────────────────────────────────────────────
draw.text((80, 195), "Професійний", fill=LIGHT, font=font_title)
draw.text((80, 278), "клінінг", fill=ACCENT, font=font_title)
draw.text((80, 361), "у 5 містах України", fill=WHITE, font=font_sub)

# ─── badges row ──────────────────────────────────────────────────────────
badges = [
    "4.9 Google",
    "Виїзд за 2 год",
    "Гарантія повернення",
]

bx = 80
by = 455
for badge in badges:
    tw = draw.textlength(badge, font=font_badge)
    pad_x, pad_y = 16, 8
    draw.rounded_rectangle(
        [(bx - pad_x, by - pad_y), (bx + tw + pad_x, by + 28 + pad_y)],
        radius=8, fill=(20, 83, 45)
    )
    draw.text((bx, by), badge, fill=ACCENT, font=font_badge)
    bx += int(tw) + pad_x * 2 + 20

# ─── cities strip (bottom) ───────────────────────────────────────────────
draw.rectangle([(0, H - 66), (W, H)], fill=(15, 70, 35))
cities = "Київ  •  Дніпро  •  Львів  •  Харків  •  Одеса"
cw = draw.textlength(cities, font=font_small)
draw.text(((W - cw) / 2, H - 46), cities, fill=LIGHT, font=font_small)

# ─── right side phone ────────────────────────────────────────────────────
phone = "+38 073 131 22 28"
try:
    font_phone = ImageFont.truetype("arialbd.ttf", 28)
except:
    font_phone = ImageFont.load_default()
pw = draw.textlength(phone, font=font_phone)
draw.text((W - pw - 80, 195), phone, fill=ACCENT, font=font_phone)

site = "clean-clean.com.ua"
sw = draw.textlength(site, font=font_small)
draw.text((W - sw - 80, 240), site, fill=LIGHT, font=font_small)

# ─── save ────────────────────────────────────────────────────────────────
out = os.path.join(BASE, 'og-image.png')
img.save(out, 'PNG', optimize=True)
print(f"✓ Saved {out}  ({os.path.getsize(out) // 1024} KB)")
