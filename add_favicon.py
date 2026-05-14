import os, glob

BASE = r"C:\Users\Admin\cleaning-site"

ROOT_FAVICON = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
SUB_FAVICON  = '<link rel="icon" href="../favicon.svg" type="image/svg+xml">'

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    rel = os.path.relpath(path, BASE)
    if rel in ['googlee912f6ea7d841dc1.html', '404.html']:
        continue  # skip non-user pages

    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'rel="icon"' in html or "rel='icon'" in html:
        continue

    depth = rel.count(os.sep)
    favicon_tag = SUB_FAVICON if depth > 0 else ROOT_FAVICON

    # Insert after <meta charset>
    html = html.replace(
        '<meta charset="UTF-8" />',
        '<meta charset="UTF-8" />\n  ' + favicon_tag,
        1
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    total += 1
    print(f"Added favicon: {rel}")

print(f"\nTotal: {total} files")
