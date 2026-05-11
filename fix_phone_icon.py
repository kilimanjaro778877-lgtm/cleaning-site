import os, glob

BASE = r"C:\Users\Admin\cleaning-site"
OLD = "M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 10.8 19.79 19.79 0 01.0 2.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"
NEW = "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"

REPLACEMENTS = [
    ('fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + OLD,
     'fill="white"><path d="' + NEW),
    ('fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + OLD,
     'fill="currentColor"><path d="' + NEW),
    ('fill="none" stroke="#0a0a0b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + OLD,
     'fill="white"><path d="' + NEW),
]

fixed = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if OLD not in html:
        continue
    new = html
    for old_s, new_s in REPLACEMENTS:
        new = new.replace(old_s, new_s)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        fixed += 1
        print("FIXED:", os.path.basename(path))
print("Total:", fixed)
