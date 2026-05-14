import os, re, glob

BASE = r"C:\Users\Admin\cleaning-site"

CDN_SCRIPT = '<script src="https://cdn.tailwindcss.com"></script>'
CONFIG_PATTERN = re.compile(r'\s*<script>tailwind\.config\s*=\s*\{.*?\}</script>', re.DOTALL)

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    rel = os.path.relpath(path, BASE)
    depth = rel.count(os.sep)
    css_path = "../tw.css" if depth > 0 else "tw.css"
    css_link = f'<link rel="stylesheet" href="{css_path}">'

    with open(path, encoding='utf-8') as f:
        html = f.read()

    if CDN_SCRIPT not in html:
        continue

    new = html.replace(CDN_SCRIPT, css_link)
    new = CONFIG_PATTERN.sub('', new)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new)
    total += 1
    print(f"FIXED ({css_path}): {rel}")

print(f"\nTotal: {total} files updated")
