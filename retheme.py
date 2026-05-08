import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# ── Color mapping ──────────────────────────────────────────────────────────
# GOLD → GREEN  (keep dark ink backgrounds, only swap accent)
REPLACEMENTS = [
    # Tailwind config gold palette → green
    ("'#fef9e7'", "'#f0fdf4'"),
    ("'#fdf2c8'", "'#dcfce7'"),
    ("'#fbe590'", "'#bbf7d0'"),
    ("'#f7d04d'", "'#4ade80'"),
    ("'#f4c027'", "'#22c55e'"),
    ("'#d4a017'", "'#16a34a'"),
    ("'#a37809'", "'#15803d'"),
    ("'#7a5a08'", "'#166534'"),

    # gold-gradient-text: gold gradient → green gradient
    (
        "linear-gradient(135deg,#f7d04d 0%,#f4c027 50%,#d4a017 100%)",
        "linear-gradient(135deg,#4ade80 0%,#22c55e 50%,#16a34a 100%)"
    ),
    (
        "linear-gradient(135deg, #f7d04d 0%, #f4c027 50%, #d4a017 100%)",
        "linear-gradient(135deg, #4ade80 0%, #22c55e 50%, #16a34a 100%)"
    ),
    # gold-gradient-text on index.html (different gradient)
    (
        "linear-gradient(135deg, #FFFAFA 0%, #b3bbff 50%, #6680ff 100%)",
        "linear-gradient(135deg, #86efac 0%, #22c55e 50%, #16a34a 100%)"
    ),

    # Raw hex gold references
    ("#f4c027", "#22c55e"),
    ("#f7d04d", "#4ade80"),
    ("#d4a017", "#16a34a"),
    ("#F4C027", "#22c55e"),

    # rgba gold → rgba green  (46,204,113 ≈ #2ECC71, close to #22c55e)
    ("rgba(244,192,39,0.9)",  "rgba(34,197,94,0.9)"),
    ("rgba(244,192,39,0.85)", "rgba(34,197,94,0.85)"),
    ("rgba(244,192,39,0.7)",  "rgba(34,197,94,0.7)"),
    ("rgba(244,192,39,0.6)",  "rgba(34,197,94,0.6)"),
    ("rgba(244,192,39,0.45)", "rgba(34,197,94,0.45)"),
    ("rgba(244,192,39,0.4)",  "rgba(34,197,94,0.4)"),
    ("rgba(244,192,39,0.35)", "rgba(34,197,94,0.35)"),
    ("rgba(244,192,39,0.3)",  "rgba(34,197,94,0.3)"),
    ("rgba(244,192,39,0.25)", "rgba(34,197,94,0.25)"),
    ("rgba(244,192,39,0.2)",  "rgba(34,197,94,0.2)"),
    ("rgba(244,192,39,0.18)", "rgba(34,197,94,0.18)"),
    ("rgba(244,192,39,0.15)", "rgba(34,197,94,0.15)"),
    ("rgba(244,192,39,0.12)", "rgba(34,197,94,0.12)"),
    ("rgba(244,192,39,0.1)",  "rgba(34,197,94,0.1)"),
    ("rgba(244,192,39,0.06)", "rgba(34,197,94,0.06)"),
    ("rgba(244,192,39,0.05)", "rgba(34,197,94,0.05)"),

    # rgba gold shadow (used in btn-3d with gold)
    ("rgba(244,192,39,0.25)", "rgba(34,197,94,0.25)"),
    ("rgba(212,160,23,0.05)", "rgba(22,163,74,0.05)"),

    # Blue button → deep forest green button
    ("background:#0022dd",   "background:#166534"),
    ("background: #0022dd",  "background: #166534"),
    ("0 6px 0 #000077",      "0 6px 0 #052e16"),
    ("0 8px 0 #000077",      "0 8px 0 #052e16"),
    ("0 2px 0 #000088",      "0 2px 0 #052e16"),
    ("0 14px 28px -8px rgba(0,34,221,0.6)",  "0 14px 28px -8px rgba(22,101,52,0.7)"),
    ("0 18px 36px -8px rgba(0,34,221,0.7)",  "0 18px 36px -8px rgba(22,101,52,0.8)"),
    ("rgba(0,34,221,0.6)",   "rgba(22,101,52,0.7)"),
    ("rgba(0,34,221,0.7)",   "rgba(22,101,52,0.8)"),
    ("rgba(0,0,80,0.5)",     "rgba(5,46,22,0.5)"),
    ("rgba(0,0,120,0.4)",    "rgba(5,46,22,0.4)"),
    ("rgba(0,0,80,0.5)",     "rgba(5,46,22,0.5)"),

    # Blue link color in nav/buttons
    ("color:#b3bbff",        "color:#86efac"),
    ("color: #b3bbff",       "color: #86efac"),
    ("style=\"border-color:rgba(102,128,255,0.35);color:#b3bbff;background:rgba(102,128,255,0.06)\"",
     "style=\"border-color:rgba(34,197,94,0.35);color:#86efac;background:rgba(34,197,94,0.06)\""),

    # Shadow with gold
    ("shadow-gold-500/10",   "shadow-green-500/10"),
    ("shadow-gold-500/30",   "shadow-green-500/30"),
    ("ring-gold-400/20",     "ring-green-400/20"),

    # SVG stroke gold in icons
    ("stroke=\"rgba(244,192,39,0.9)\"", "stroke=\"rgba(34,197,94,0.9)\""),
]

HTML_GLOB = []
for root, dirs, files in os.walk(BASE):
    # skip node_modules, .git, scripts
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if f.endswith('.html'):
            HTML_GLOB.append(os.path.join(root, f))

total_changed = 0
for path in HTML_GLOB:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    new_html = html
    for old, new in REPLACEMENTS:
        new_html = new_html.replace(old, new)

    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        total_changed += 1
        print(f"UPDATED: {os.path.relpath(path, BASE)}")
    else:
        print(f"clean:   {os.path.relpath(path, BASE)}")

print(f"\nDone — {total_changed} files updated.")
