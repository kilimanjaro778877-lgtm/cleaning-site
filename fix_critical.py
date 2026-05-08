import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# ── 1. Global text-zinc-100 → text-gray-900 in service pages (selects, footers, breadcrumbs)
GLOBAL_REPLACEMENTS = [
    # Invisible select text
    ("outline-none text-zinc-100",      "outline-none text-gray-900"),
    ("outline-none transition text-zinc-100", "outline-none transition text-gray-900"),
    # Footer headings invisible
    ("font-bold text-zinc-100 mb-4",    "font-bold text-gray-800 mb-4"),
    # Footer logo invisible
    ("font-bold text-xl text-zinc-100", "font-bold text-xl text-gray-900"),
    # Breadcrumb active item invisible
    ("text-zinc-100 font-medium",       "text-gray-900 font-medium"),
    ("text-zinc-100\">",               "text-gray-900\">"),
    # Price display in calculator
    ("font-black text-zinc-100\" id=\"pg-price\"",   "font-black text-gray-900\" id=\"pg-price\""),
    ("font-black text-zinc-100\" id=\"price-val\"",  "font-black text-gray-900\" id=\"price-val\""),
    # divide-ink-700 → divide-gray-200 (invisible table row separators)
    ("divide-ink-700",                  "divide-gray-200"),
    # feat-card heavy shadow → lighter
    ("0 12px 32px -8px rgba(0,0,0,0.6)", "0 12px 32px -8px rgba(34,197,94,0.12)"),
    # Secondary CTA blue ghost border → green (service pages)
    ("border-color:rgba(102,128,255,0.35);color:#86efac;background:rgba(102,128,255,0.06)",
     "border-color:rgba(34,197,94,0.35);color:#16a34a;background:rgba(34,197,94,0.06)"),
    # Add Одеса to city selects that are missing it
    ("<option>Харків</option>\n            </select>",
     "<option>Харків</option><option>Одеса</option>\n            </select>"),
    ("<option>Харків</option></select>",
     "<option>Харків</option><option>Одеса</option></select>"),
    # Slider dark track on service pages
    ("background: linear-gradient(to right, #22c55e var(--p, 41%), #262629",
     "background: linear-gradient(to right, #22c55e var(--p, 41%), #e5e7eb"),
    ("background: linear-gradient(to right, #22c55e var(--p, 12%), #262629",
     "background: linear-gradient(to right, #22c55e var(--p, 12%), #e5e7eb"),
    # Slider thumb black border
    ("border: 4px solid #0a0a0b",       "border: 4px solid #ffffff"),
    ("border: 4px solid #0a0a0b;",      "border: 4px solid #ffffff;"),
    # Window note low contrast
    ("text-amber-300/90",               "text-amber-700"),
    ("bg-amber-400/5 border border-amber-400/20", "bg-amber-50 border border-amber-200"),
]

# ── 2. Fix wrong gold palette on 4 service pages
WRONG_GOLD_PAGES = [
    r"services\generalna-prybyrannia.html",
    r"services\pidtrymuyuche-prybyrannia.html",
    r"services\mytia-vikon.html",
    r"services\himchistka-divana.html",
]
WRONG_GOLD = "gold:{50:'#f0f2ff',100:'#d6dbff',200:'#c4ccff',300:'#aab4ff',400:'#99aaff',500:'#6680ff',600:'#4455dd',700:'#2233bb'}"
RIGHT_GOLD = "gold:{50:'#f0fdf4',100:'#dcfce7',200:'#bbf7d0',300:'#4ade80',400:'#22c55e',500:'#16a34a',600:'#15803d',700:'#166534'}"
# Also fix the expanded version
WRONG_GOLD2 = "gold: { 50:'#f0f2ff', 100:'#d6dbff', 200:'#c4ccff', 300:'#aab4ff', 400:'#99aaff', 500:'#6680ff', 600:'#4455dd', 700:'#2233bb' }"
RIGHT_GOLD2 = "gold: { 50:'#f0fdf4', 100:'#dcfce7', 200:'#bbf7d0', 300:'#4ade80', 400:'#22c55e', 500:'#16a34a', 600:'#15803d', 700:'#166534' }"

# ── 3. Fix blog.html dark cards
BLOG_FIXES = [
    ("h1,h2,h3{color:#FFFAFA}",         "h1,h2,h3{color:#111827}"),
    (".blog-card{background:#07091e;border:1px solid #151840",
     ".blog-card{background:#ffffff;border:1px solid #e5e7eb"),
    (".tag{color:#99aaff;background:rgba(102,128,255,0.08);border:1px solid rgba(102,128,255,0.3)}",
     ".tag{color:#16a34a;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25)}"),
    # Blog card text that was white on dark
    ("text-zinc-300 mt-2",              "text-gray-600 mt-2"),
    ("text-zinc-400 text-sm",           "text-gray-500 text-sm"),
]

# ── 4. Fix city pages .city-card dark background
CITY_CARD_FIX_OLD = ".city-card{background:#0d1030;border:1px solid #151840;"
CITY_CARD_FIX_NEW = ".city-card{background:#ffffff;border:1px solid #e5e7eb;"
CITY_CARD_HOVER_OLD = ".city-card:hover{border-color:rgba(34,197,94,0.4);"
# Also fix city card text (was white on dark card)
CITY_CARD_TEXT = [
    ("<div class=\"font-bold text-lg\">",   "<div class=\"font-bold text-lg text-gray-900\">"),
    ("<div class=\"text-sm text-zinc-400 mt-1\">", "<div class=\"text-sm text-gray-500 mt-1\">"),
    ("<div class=\"text-sm mt-1\">",        "<div class=\"text-sm text-gray-500 mt-1\">"),
]

# ── 5. Fix slider on city pages
CITY_SLIDER_FIXES = [
    ("background:linear-gradient(to right,#22c55e var(--p,41%),#151840",
     "background:linear-gradient(to right,#22c55e var(--p,41%),#e5e7eb"),
    ("border:3px solid #03040f",         "border:3px solid #ffffff"),
    ("border:3px solid #03040f;",        "border:3px solid #ffffff;"),
]

# ── 6. Fix index.html btn-3d hover blue shadow
INDEX_BTN_FIX = [
    ("0 8px 0 #1122aa",   "0 8px 0 #052e16"),
    ("rgba(102,128,255,0.6)", "rgba(22,101,52,0.8)"),
    ("0 2px 0 #000066",   "0 2px 0 #052e16"),
]

# ── Collect all HTML files ──────────────────────────────────────────────
def get_html_files():
    result = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
        for f in files:
            if f.endswith('.html'):
                result.append(os.path.join(root, f))
    return result

total = 0
for path in get_html_files():
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new = html

    # Global fixes
    for old, new_val in GLOBAL_REPLACEMENTS:
        new = new.replace(old, new_val)

    rel = os.path.relpath(path, BASE)

    # Wrong gold palette fix
    if rel in WRONG_GOLD_PAGES:
        new = new.replace(WRONG_GOLD, RIGHT_GOLD)
        new = new.replace(WRONG_GOLD2, RIGHT_GOLD2)

    # Blog fixes
    if rel == 'blog.html':
        for old, new_val in BLOG_FIXES:
            new = new.replace(old, new_val)

    # City card fixes
    city_pages = ['kyiv.html','dnipro.html','lviv.html','kharkiv.html','odessa.html']
    if rel in city_pages:
        new = new.replace(CITY_CARD_FIX_OLD, CITY_CARD_FIX_NEW)
        for old, new_val in CITY_CARD_TEXT:
            new = new.replace(old, new_val)
        for old, new_val in CITY_SLIDER_FIXES:
            new = new.replace(old, new_val)

    # index.html btn fix
    if rel == 'index.html':
        for old, new_val in INDEX_BTN_FIX:
            new = new.replace(old, new_val)

    if new != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        total += 1
        print(f"FIXED: {rel}")

print(f"\nDone — {total} files fixed.")
