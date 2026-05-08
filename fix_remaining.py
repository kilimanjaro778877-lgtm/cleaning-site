import os, re

BASE = r"C:\Users\Admin\cleaning-site"

def get_html_files():
    result = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
        for f in files:
            if f.endswith('.html'):
                result.append(os.path.join(root, f))
    return result

FIXES = [
    # ── 1. Logo: blue → green ──────────────────────────────────────────
    ("background:linear-gradient(135deg,#3355ff,#0011ee)",
     "background:linear-gradient(135deg,#22c55e,#16a34a)"),
    ("background: linear-gradient(135deg,#3355ff,#0011ee)",
     "background: linear-gradient(135deg,#22c55e,#16a34a)"),
    ("style=\"background:linear-gradient(135deg,#3355ff,#0011ee)\"",
     "style=\"background:linear-gradient(135deg,#22c55e,#16a34a)\""),

    # ── 2. Google Fonts → non-blocking ────────────────────────────────
    ("<link href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Raleway:wght@600;700;800;900&display=swap\" rel=\"stylesheet\" />",
     "<link rel=\"preload\" as=\"style\" href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Raleway:wght@700;800;900&display=swap\" onload=\"this.onload=null;this.rel='stylesheet'\" /><noscript><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Raleway:wght@700;800;900&display=swap\" /></noscript>"),
    # variant without spaces
    ("<link href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;family=Raleway:wght@600;700;800;900&display=swap\" rel=\"stylesheet\" />",
     "<link rel=\"preload\" as=\"style\" href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Raleway:wght@700;800;900&display=swap\" onload=\"this.onload=null;this.rel='stylesheet'\" /><noscript><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Raleway:wght@700;800;900&display=swap\" /></noscript>"),

    # ── 3. Aria labels: Telegram + phone buttons ──────────────────────
    ("href=\"https://t.me/jamboss8\" target=\"_blank\" rel=\"noopener noreferrer\"",
     "href=\"https://t.me/jamboss8\" target=\"_blank\" rel=\"noopener noreferrer\" aria-label=\"Написати в Telegram\""),
    ("href=\"tel:+380731312228\"\n       class=\"w-14 h-14",
     "href=\"tel:+380731312228\" aria-label=\"Зателефонувати\"\n       class=\"w-14 h-14"),

    # ── 4. Aria: mobile menu button ───────────────────────────────────
    ("id=\"mobile-menu-btn\" class=\"md:hidden p-2 text-gray-500 hover:text-gray-900 transition\" aria-label=\"Відкрити меню\"",
     "id=\"mobile-menu-btn\" class=\"md:hidden p-2 text-gray-500 hover:text-gray-900 transition\" aria-label=\"Меню\" aria-expanded=\"false\" aria-controls=\"mobile-nav\""),

    # ── 5. Одеса in city select on service pages ──────────────────────
    ("<option>Харків</option>\n            </select>",
     "<option>Харків</option>\n            <option>Одеса</option>\n            </select>"),
    ("<option>Харків</option></select>",
     "<option>Харків</option><option>Одеса</option></select>"),

    # ── 6. prefers-reduced-motion for orb animations ─────────────────
    # Will add after main loop

    # ── 7. Breadcrumb separators aria-hidden ─────────────────────────
    ("<span class=\"mx-2\">/</span>",
     "<span class=\"mx-2\" aria-hidden=\"true\">/</span>"),

    # ── 8. Window warning note better contrast (amber) ────────────────
    ("text-amber-300/90",   "text-amber-700"),
    ("bg-amber-400/5 border border-amber-400/20",
     "bg-amber-50 border border-amber-200"),

    # ── 9. Summary/details role for FAQ ──────────────────────────────
    ("<summary class=\"flex items-center justify-between p-6 cursor-pointer font-semibold list-none\">",
     "<summary class=\"flex items-center justify-between p-6 cursor-pointer font-semibold list-none\" role=\"button\">"),
    ("<summary class=\"flex items-center justify-between p-5 cursor-pointer font-semibold list-none\">",
     "<summary class=\"flex items-center justify-between p-5 cursor-pointer font-semibold list-none\" role=\"button\">"),

    # ── 10. Remove duplicate .feat-card CSS ───────────────────────────
    # handled separately

    # ── 11. prefers-reduced-motion ────────────────────────────────────
    # Add to style blocks that contain @keyframes od1
]

REDUCED_MOTION = """
    @media (prefers-reduced-motion: reduce) {
      .orb-1, .orb-2 { animation: none; }
    }"""

total = 0
for path in get_html_files():
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = html

    for old, new_val in FIXES:
        new = new.replace(old, new_val)

    # Add prefers-reduced-motion if orb animation exists and not already added
    if "@keyframes od1" in new and "prefers-reduced-motion" not in new:
        new = new.replace("@keyframes od1{", REDUCED_MOTION + "\n    @keyframes od1{")

    # Remove duplicate .feat-card CSS (appears twice in a row)
    new = re.sub(
        r'(\.feat-card\{[^}]+\}\.feat-card:hover\{[^}]+\})\s*\.feat-card\{[^}]+\}\.feat-card:hover\{[^}]+\}',
        r'\1',
        new
    )

    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        total += 1
        print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files fixed.")
