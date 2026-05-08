import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# Remove "24 год / гарантія" metric blocks from service pages
# Pattern: <div><div ...>24 год</div><div ...>гарантія</div></div>
METRIC_RE = re.compile(
    r'<div>\s*<div[^>]*>24 год</div>\s*<div[^>]*>гарантія</div>\s*</div>'
)

# Also the full inline version
INLINE_RE = re.compile(
    r'<div><div class="font-display text-2xl font-extrabold text-gold-400">24 год</div>'
    r'<div class="text-sm text-gray-400 mt-1">гарантія</div></div>'
)

# Remove "Гарантія результату 24 год" row from prices.html table
PRICES_ROW = re.compile(
    r'\s*<tr[^>]*><td[^>]*>Гарантія результату 24 год</td>.*?</tr>',
    re.DOTALL
)

# Remove "з гарантією" from h1 title in prybyrannia-kukhni
# Remove " Гарантія 24 год." from meta descriptions
META_GUARANTEE_RE = re.compile(r'\. Гарантія 24 год\.')

total = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        new = html

        # Remove metric blocks
        new = METRIC_RE.sub('', new)
        new = INLINE_RE.sub('', new)

        # Remove prices.html guarantee row
        new = PRICES_ROW.sub('', new)

        # Remove "з гарантією" from kitchen h1
        new = new.replace('<span class="gold-gradient-text italic"> з гарантією</span>', '')

        # Remove from meta descriptions
        new = META_GUARANTEE_RE.sub('.', new)

        # Remove from dnipro/kyiv/etc inline stats
        # Pattern: <div><div ...>24 год</div><div class="text-sm text-gray-400 mt-1">гарантія</div></div>
        new = re.sub(
            r'<div>\s*<div class="font-display[^"]*"[^>]*>24 год</div>\s*<div class="text-sm[^"]*">гарантія</div>\s*</div>',
            '', new
        )

        if new != html:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            total += 1
            print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files.")
