import os, re

BASE = r"C:\Users\Admin\cleaning-site"

def get_html(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def save_html(path, html):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

total = 0

# ── 1. Invisible headings: color:#FFFAFA → color:#111827 ─────────────
for fn in ['blog.html', 'faq.html', 'prices.html']:
    path = os.path.join(BASE, fn)
    html = get_html(path)
    new = html.replace(
        'h1,h2,h3{letter-spacing:-0.02em;color:#FFFAFA}',
        'h1,h2,h3{letter-spacing:-0.02em;color:#111827}'
    ).replace(
        'h1,h2,h3{color:#FFFAFA}',
        'h1,h2,h3{color:#111827}'
    )
    if new != html:
        save_html(path, new)
        total += 1
        print(f"FIXED headings: {fn}")

# ── 2. text-ink-900 on green bg → text-gray-900 (white→dark for contrast) ─
# Affected: step badges in index.html, table headers in service pages
ALL_HTML = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if f.endswith('.html'):
            ALL_HTML.append(os.path.join(root, f))

for path in ALL_HTML:
    html = get_html(path)
    new = html
    # bg-gold-400 text-ink-900 → bg-gold-400 text-gray-900
    new = new.replace('bg-gold-400 text-ink-900', 'bg-gold-400 text-gray-900')
    # thead bg-gold-400 text-ink-900
    new = new.replace('"bg-gold-400 text-ink-900"', '"bg-gold-400 text-gray-900"')
    if new != html:
        save_html(path, new)
        total += 1
        print(f"FIXED ink-900 contrast: {os.path.relpath(path, BASE)}")

# ── 3. Odessa.html: add missing hamburger button ─────────────────────
odessa = os.path.join(BASE, 'odessa.html')
html = get_html(odessa)
HAMBURGER = '<button id="mobile-menu-btn" class="md:hidden p-2 text-gray-500 hover:text-gray-900 transition" aria-label="Меню" aria-expanded="false" aria-controls="mobile-nav"><svg id="icon-menu" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg></button>'

if 'mobile-menu-btn' not in html[:html.find('</header>')]:
    # Find the flex items div with phone and button
    old = '<div class="flex items-center gap-3">'
    header_end = html.find('</header>')
    header = html[:header_end]
    if old in header:
        new_header = header.replace(old, HAMBURGER + '\n      ' + old, 1)
        html = new_header + html[header_end:]
        save_html(odessa, html)
        total += 1
        print("FIXED: odessa.html hamburger button")

# ── 4. Remove redirect blog stubs from sitemap ───────────────────────
sitemap = os.path.join(BASE, 'sitemap.xml')
html = get_html(sitemap)
# Remove entries for blog redirect stubs (they redirect to blog.html anyway)
REMOVE_URLS = [
    'blog/generalna-chy-pidtrymuyuche.html',
    'blog/poryadok-mizh-prybyranniamy.html',
    'blog/yak-myty-vikna.html',
    'blog/khimiia-dlia-prybyrannnia.html',
    'blog/pylovi-klishi.html',
]
new_sitemap = html
for url_part in REMOVE_URLS:
    new_sitemap = re.sub(
        r'\s*<url>\s*<loc>[^<]*' + re.escape(url_part) + r'[^<]*</loc>\s*<changefreq>[^<]*</changefreq>\s*<priority>[^<]*</priority>\s*</url>',
        '', new_sitemap
    )
if new_sitemap != html:
    save_html(sitemap, new_sitemap)
    total += 1
    print("FIXED: sitemap.xml (removed redirect stubs)")

print(f"\nDone — {total} fixes applied.")
