import re, os

BASE = r"C:\Users\Admin\cleaning-site"

# Phone wrapper to inject before </header>
# Replaces the lone "Замовити" button with phone + button group
PHONE_WITH_BTN = '<div class="flex items-center gap-3"><a href="tel:+380731312228" class="hidden sm:flex items-center gap-1.5 text-sm font-semibold hover:text-gold-400 transition"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 10.8 19.79 19.79 0 010 2.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>+38 073 131 22 28</a>{btn}</div>'

# Pages and their order href (relative to file location)
ALL_PAGES = [
    # city pages (root level)
    "kyiv.html",
    "dnipro.html",
    "lviv.html",
    "kharkiv.html",
    "odessa.html",
    # service pages (services/ subfolder)
    r"services\generalna-prybyrannia.html",
    r"services\pidtrymuyuche-prybyrannia.html",
    r"services\mytia-vikon.html",
    r"services\himchistka-divana.html",
    r"services\himchistka-matratsa.html",
    r"services\klinig-ofisiv.html",
    r"services\prybyrannia-kukhni.html",
    r"services\prybyrannia-vannoi.html",
    r"services\pislia-remontu.html",
    # other pages
    "prices.html",
    "blog.html",
    "faq.html",
]

# Regex: match the lone "Замовити" button (not already inside a flex div)
# Handles various btn-3d variants
BTN_RE = re.compile(
    r'(?<!gap-3">)(<a href="[^"]*" class="btn-3d[^"]*"[^>]*>Замовити</a>)'
)

def process(rel):
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f"SKIP (not found): {rel}")
        return

    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Already has phone in header?
    if '073 131 22 28' in html[:html.find('</header>')]:
        print(f"SKIP (already has phone): {os.path.basename(path)}")
        return

    # Find the btn inside the header only
    header_start = html.find('<header ')
    header_end = html.find('</header>')
    if header_start == -1:
        print(f"SKIP (no header): {os.path.basename(path)}")
        return

    header_html = html[header_start:header_end + 9]

    # Find the btn-3d Замовити in header
    m = BTN_RE.search(header_html)
    if not m:
        print(f"NO BTN FOUND: {os.path.basename(path)}")
        return

    original_btn = m.group(1)
    replacement = PHONE_WITH_BTN.replace('{btn}', original_btn)
    new_header = header_html[:m.start()] + replacement + header_html[m.end():]
    new_html = html[:header_start] + new_header + html[header_end + 9:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"UPDATED: {os.path.basename(path)}")

for p in ALL_PAGES:
    process(p)

print("Done.")
