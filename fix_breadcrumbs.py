import re, os

BASE = r"C:\Users\Admin\cleaning-site"

# Remove extra nav links (Ціни, Блог, FAQ) from breadcrumb navs on service pages
# Pattern: these links appear in breadcrumb area (text-zinc-500 nav) but shouldn't be there

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

# Remove these nav link patterns from breadcrumbs
REMOVE_PATTERNS = [
    r'<a href="\.\./prices\.html"[^>]*>Ціни</a>',
    r'<a href="\.\./blog\.html"[^>]*>Блог</a>',
    r'<a href="\.\./faq\.html"[^>]*>FAQ</a>',
]

for rel in PAGES:
    path = os.path.join(BASE, rel)
    with open(path, encoding='utf-8') as f:
        html = f.read()

    new_html = html
    for pattern in REMOVE_PATTERNS:
        new_html = re.sub(pattern, '', new_html)

    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"FIXED: {os.path.basename(path)}")
    else:
        print(f"CLEAN: {os.path.basename(path)}")

print("Done.")
