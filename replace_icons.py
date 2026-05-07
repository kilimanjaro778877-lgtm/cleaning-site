import re, os

BASE = r"C:\Users\Admin\cleaning-site"

EMOJI_TO_ICON = {
    '🪣': 'layers',
    '🔦': 'lightbulb',
    '🚪': 'archive',
    '📐': 'ruler',
    '🛁': 'droplets',
    '🪟': 'grid-2x2',
    '🌀': 'rotate-cw',
    '🚿': 'droplets',
    '🍳': 'flame',
    '🪞': 'maximize',
    '🗑': 'trash-2',
    '🏙': 'building-2',
    '🖼': 'image',
    '🪴': 'leaf',
    '🔍': 'search',
    '💧': 'droplets',
    '🌸': 'sparkles',
    '💨': 'wind',
    '🖥': 'monitor',
    '🍽': 'utensils',
    '📋': 'clipboard-list',
    '🔥': 'flame',
    '🧴': 'shield',
    '🔲': 'grid-2x2',
    '🚽': 'circle-dot',
    '🌫': 'wind',
    '🎨': 'paintbrush',
    '🔧': 'wrench',
    '✅': 'check-circle',
}

LUCIDE_SCRIPT = '<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>\n'
LUCIDE_INIT   = '<script>if(window.lucide)lucide.createIcons();</script>\n'

ICON_DIV_RE = re.compile(
    r'(<div class="w-11 h-11 rounded-xl flex items-center justify-center text-xl"'
    r' style="background:rgba\(244,192,39,0\.12\);border:1px solid rgba\(244,192,39,0\.3\)">'
    r')([\s\S]*?)(</div>)'
)

def replace_emoji_in_div(m):
    prefix, content, suffix = m.group(1), m.group(2), m.group(3)
    content = content.strip()
    icon = EMOJI_TO_ICON.get(content)
    if icon:
        return (
            prefix.replace('text-xl', 'overflow-hidden') +
            f'<i data-lucide="{icon}" class="w-6 h-6" style="color:rgba(244,192,39,0.9)"></i>' +
            suffix
        )
    return m.group(0)  # leave unchanged if emoji not mapped

def process_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'data-lucide' in html:
        print(f"SKIP (already processed): {os.path.basename(path)}")
        return

    new_html = ICON_DIV_RE.sub(replace_emoji_in_div, html)

    if new_html == html:
        print(f"NO CHANGE: {os.path.basename(path)}")
        return

    # Add Lucide script to <head> if not present
    if 'lucide' not in new_html:
        new_html = new_html.replace('</head>', LUCIDE_SCRIPT + '</head>', 1)

    # Add lucide.createIcons() before </body>
    new_html = new_html.replace('</body>', LUCIDE_INIT + '</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"UPDATED: {os.path.basename(path)}")

service_pages = [
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

for rel in service_pages:
    process_file(os.path.join(BASE, rel))

print("Done.")
