import re, os

BASE = r"C:\Users\Admin\cleaning-site"

PAGES = [
    r"services\himchistka-matratsa.html",
    r"services\prybyrannia-kukhni.html",
    r"services\prybyrannia-vannoi.html",
    r"services\pislia-remontu.html",
]

NAV_HTML = '<nav class="hidden md:flex items-center gap-7 text-sm font-medium text-zinc-400"><a href="../index.html#services" class="hover:text-warm-100 transition">Послуги</a><a href="../prices.html" class="hover:text-warm-100 transition">Ціни</a><a href="../blog.html" class="hover:text-warm-100 transition">Блог</a><a href="../faq.html" class="hover:text-warm-100 transition">FAQ</a></nav>'

# Insert nav before the <div class="flex items-center gap-3"> in header
INSERT_RE = re.compile(r'(<div class="flex items-center gap-3">.*?</header>)', re.DOTALL)
BEFORE_RE = re.compile(r'(<div class="flex items-center gap-3">)')

for rel in PAGES:
    path = os.path.join(BASE, rel)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'hidden md:flex' in html:
        print(f"SKIP (already has nav): {os.path.basename(path)}")
        continue

    # Find the right section header button div
    header_start = html.find('<header ')
    header_end = html.find('</header>') + 9
    header = html[header_start:header_end]

    m = BEFORE_RE.search(header)
    if not m:
        print(f"NO MATCH: {os.path.basename(path)}")
        continue

    new_header = header[:m.start()] + NAV_HTML + '\n      ' + header[m.start():]
    new_html = html[:header_start] + new_header + html[header_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"ADDED NAV: {os.path.basename(path)}")

print("Done.")
