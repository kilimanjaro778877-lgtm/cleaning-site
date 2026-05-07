import re, os

BASE = r"C:\Users\Admin\cleaning-site"

PAGES = [
    r"services\generalna-prybyrannia.html",
    r"services\pidtrymuyuche-prybyrannia.html",
    r"services\mytia-vikon.html",
    r"services\himchistka-divana.html",
    r"services\himchistka-matratsa.html",
    r"services\klinig-ofisiv.html",
    r"services\prybyrannia-kukhni.html",
    r"services\prybyrannia-vannoi.html",
    r"services\pislia-remontu.html",
]

FULL_NAV = '<nav class="hidden md:flex items-center gap-7 text-sm font-medium text-zinc-400"><a href="../index.html#services" class="hover:text-warm-100 transition">Послуги</a><a href="../prices.html" class="hover:text-warm-100 transition">Ціни</a><a href="../blog.html" class="hover:text-warm-100 transition">Блог</a><a href="../faq.html" class="hover:text-warm-100 transition">FAQ</a></nav>'

# Match any broken nav in header (hidden md:flex) that is missing Ціни/Блог/FAQ
NAV_RE = re.compile(
    r'<nav class="hidden md:flex items-center gap-7 text-sm font-medium text-zinc-400">.*?</nav>',
    re.DOTALL
)

for rel in PAGES:
    path = os.path.join(BASE, rel)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    m = NAV_RE.search(html)
    if not m:
        print(f"NO NAV: {os.path.basename(path)}")
        continue

    current = m.group(0)
    if 'Ціни' in current and 'Блог' in current and 'FAQ' in current:
        print(f"OK: {os.path.basename(path)}")
        continue

    new_html = html[:m.start()] + FULL_NAV + html[m.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"RESTORED: {os.path.basename(path)}")

print("Done.")
