import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# Targeted fixes for remaining white text on light backgrounds
REPLACEMENTS = [
    # Form inputs/selects/textareas - text-zinc-100 → text-gray-900
    ("bg-white border border-gray-200 focus:border-gold-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-zinc-100",
     "bg-white border border-gray-200 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-gray-900"),
    ("bg-white border border-gray-200 focus:border-gold-400 focus:ring-2 focus:ring-green-400/20 outline-none text-zinc-100",
     "bg-white border border-gray-200 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none text-gray-900"),
    # Service pages form inputs (../prices)
    ("bg-white border border-gray-300 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-gray-900",
     "bg-white border border-gray-300 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-gray-900"),
    # Fixed price display (calculator non-slider panel)
    ("text-5xl sm:text-6xl font-black text-white\" id=\"fixed-price\"",
     "text-5xl sm:text-6xl font-black text-gray-900\" id=\"fixed-price\""),
    # Review names
    ("font-semibold text-sm text-zinc-100\">",
     "font-semibold text-sm text-gray-800\">"),
    # Mobile menu phone link
    ("bg-white text-zinc-100 font-semibold",
     "bg-gray-50 text-gray-900 font-semibold"),
    # Mobile menu hover
    ("hover:text-zinc-100",
     "hover:text-gray-900"),
    # Any remaining text-zinc-100 in forms/cards (not on photos)
    # Only replace when NOT inside city card photo overlays
    # Review cards text
    ("text-zinc-300 text-sm leading-relaxed",
     "text-gray-600 text-sm leading-relaxed"),
    # Remaining text-zinc-100 in service detail and misc
    ("id=\"sd-title\"\>", "id=\"sd-title\">"),

    # Service details section dark bg
    ("section id=\"service-details\" class=\"py-16 bg-gray-50\"",
     "section id=\"service-details\" class=\"py-16 bg-gray-50\""),

    # Calculator label text
    ("text-sm text-gray-500\" id=\"calc-label\"",
     "text-sm text-gray-600\" id=\"calc-label\""),
    ("text-sm text-zinc-400\" id=\"calc-label\"",
     "text-sm text-gray-600\" id=\"calc-label\""),
    ("text-2xl text-zinc-300 font-bold\" id=\"calc-unit\"",
     "text-2xl text-gray-700 font-bold\" id=\"calc-unit\""),

    # Price result right panel
    ("bg-gradient-to-br from-gray-50 to-white border border-green-400/20",
     "bg-white border border-green-400/20"),

    # Остальные text-zinc-100 которые не на фото
    # (city cards have text-white which is correct for photo overlay)
    # service-name in JS cards
    ("text-zinc-100\">${s.name}",
     "text-gray-900\">${s.name}"),
    ("'text-zinc-100'", "'text-gray-900'"),

    # Mobile nav bg dark
    (" bg-white\">", " bg-white\">"),

    # hero section text colors
    ("text-5xl font-black text-zinc-100",
     "text-5xl font-black text-gray-900"),
    ("text-4xl font-black text-zinc-100",
     "text-4xl font-black text-gray-900"),

    # Remaining hardcoded in service pages
    ("color: #111827;\n    line-height: 1.2;\n    overflow: visible;\n    letter-spacing: -0.025em;\n    color: #111827;",
     "color: #111827;\n    line-height: 1.2;\n    overflow: visible;\n    letter-spacing: -0.025em;"),

    # feat-card text
    ("mt-4 font-bold\">",  "mt-4 font-bold text-gray-900\">"),
    ("mt-2 text-sm text-gray-500\">", "mt-2 text-sm text-gray-500\">"),
]

# Global: any remaining text-zinc-100 → text-gray-900 EXCEPT in inline style with color:#ffffff
# We'll do a regex replacement to catch remaining ones

HTML_GLOB = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if f.endswith('.html'):
            HTML_GLOB.append(os.path.join(root, f))

total = 0
for path in HTML_GLOB:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new_html = html
    for old, new in REPLACEMENTS:
        new_html = new_html.replace(old, new)

    # Fix service card JS template text color
    new_html = new_html.replace(
        "class=\"service-name font-bold text-zinc-100\"",
        "class=\"service-name font-bold text-gray-900\""
    )
    new_html = new_html.replace(
        "class=\"service-name font-bold text-gray-900\">${s.name}",
        "class=\"service-name font-bold text-gray-900\">${s.name}"
    )

    # Fix text-zinc-100 in form elements (not in city card overlays)
    # Replace remaining text-zinc-100 that's NOT in photo overlay context
    # City cards have text-white (different class) so those are safe

    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        total += 1
        print(f"UPDATED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files updated.")
