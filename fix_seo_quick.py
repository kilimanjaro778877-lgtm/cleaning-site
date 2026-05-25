#!/usr/bin/env python3
"""Quick SEO fixes for clean-clean.com.ua"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── helpers ───────────────────────────────────────────────────────────────

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {os.path.relpath(path, BASE)}")

# ─── 1. collect all HTML files ─────────────────────────────────────────────

html_files = (
    glob.glob(os.path.join(BASE, '*.html')) +
    glob.glob(os.path.join(BASE, 'blog', '*.html')) +
    glob.glob(os.path.join(BASE, 'services', '*.html'))
)

print(f"\nFound {len(html_files)} HTML files")

# ─── 2. fix each HTML file ──────────────────────────────────────────────────

for path in sorted(html_files):
    original = read(path)
    content = original

    # a) Remove hreflang tags (monolingual site — they add noise)
    content = re.sub(
        r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n?',
        '\n',
        content
    )

    # b) og:image SVG → PNG
    content = content.replace(
        'content="https://clean-clean.com.ua/og-image.svg"',
        'content="https://clean-clean.com.ua/og-image.png"'
    )

    # c) ratingCount "2" → "7"
    content = content.replace('"ratingCount": "2"', '"ratingCount": "7"')

    if content != original:
        write(path, content)

# ─── 3. index.html specific fixes ──────────────────────────────────────────

index_path = os.path.join(BASE, 'index.html')
content = read(index_path)

# c1) Remove Telegram from sameAs, keep only GBP
content = content.replace(
    '"sameAs": [\n      "https://g.page/r/CcuiKcWaRxt2EAE",\n      "https://t.me/jamboss8"\n    ]',
    '"sameAs": ["https://g.page/r/CcuiKcWaRxt2EAE"]'
)

# c2) Add FAQPage schema before closing </head>
faq_schema = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Скільки коштує прибирання квартири?",
        "acceptedAnswer": {"@type": "Answer", "text": "Скористайтеся калькулятором на сайті — він покаже орієнтовну ціну за 10 секунд. Підтримуюче прибирання — від 50 ₴/м², генеральне — від 70 ₴/м². Точну суму погодимо після дзвінка."}
      },
      {
        "@type": "Question",
        "name": "Чи привозите хімію та обладнання?",
        "acceptedAnswer": {"@type": "Answer", "text": "Так. Привозимо все необхідне — професійну хімію Clinex, пилососи, пароочисники, тряпки. Вам нічого готувати не треба."}
      },
      {
        "@type": "Question",
        "name": "Що, якщо результат не сподобається?",
        "acceptedAnswer": {"@type": "Answer", "text": "Переробимо безкоштовно. Якщо проблема залишиться — повернемо гроші повністю. Гарантія якості на кожне замовлення."}
      },
      {
        "@type": "Question",
        "name": "Як швидко приїде бригада?",
        "acceptedAnswer": {"@type": "Answer", "text": "У робочий день з 8:00 до 21:00 — у середньому через 2 години після підтвердження заявки."}
      },
      {
        "@type": "Question",
        "name": "Чи можна оплатити карткою?",
        "acceptedAnswer": {"@type": "Answer", "text": "Так — приймаємо готівку, переказ на картку Mono/Privat, або через Apple/Google Pay після прибирання."}
      }
    ]
  }
  </script>
</head>'''

if '"FAQPage"' not in content:
    content = content.replace('</head>', faq_schema)
    print("\n  ✓ index.html — FAQPage schema added")

write(index_path, content)

# ─── 4. city pages — add parentOrganization ────────────────────────────────

city_files = {
    'kyiv.html':    'Clean-Clean — Київ',
    'dnipro.html':  'Clean-Clean — Дніпро',
    'lviv.html':    'Clean-Clean — Львів',
    'kharkiv.html': 'Clean-Clean — Харків',
    'odesa.html':   'Clean-Clean — Одеса',
}

print("\nCity pages — adding parentOrganization:")
for fname, city_name in city_files.items():
    path = os.path.join(BASE, fname)
    content = read(path)

    if '"parentOrganization"' not in content:
        # Insert parentOrganization after the @id line on the city schema
        content = re.sub(
            r'("@id": "https://clean-clean\.com\.ua/' + re.escape(fname) + r'#business",)',
            r'\1\n    "parentOrganization": {"@id": "https://clean-clean.com.ua/#business"},',
            content
        )
        write(path, content)
    else:
        print(f"  — {fname} already has parentOrganization")

# ─── 5. contacts.html — add @id to CleaningService ─────────────────────────

contacts_path = os.path.join(BASE, 'contacts.html')
content = read(contacts_path)

if '"@id"' not in content.split('<script type="application/ld+json">')[1].split('</script>')[0]:
    content = content.replace(
        '{"@context":"https://schema.org","@type":"CleaningService","name":"Clean-Clean"',
        '{"@context":"https://schema.org","@type":"CleaningService","@id":"https://clean-clean.com.ua/#business","name":"Clean-Clean"'
    )
    write(contacts_path, content)
    print("\n  ✓ contacts.html — @id added to CleaningService")

# ─── 6. sitemap.xml — remove BOM, update blog.html lastmod ─────────────────

sitemap_path = os.path.join(BASE, 'sitemap.xml')
with open(sitemap_path, 'rb') as f:
    raw = f.read()

# Remove UTF-8 BOM if present
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
    print("\n  ✓ sitemap.xml — BOM removed")

sitemap = raw.decode('utf-8')

# Update blog.html lastmod to today
sitemap = re.sub(
    r'(<loc>https://clean-clean\.com\.ua/blog\.html</loc>\s*<lastmod>)[^<]*(</lastmod>)',
    r'\g<1>2026-05-25\g<2>',
    sitemap
)

with open(sitemap_path, 'w', encoding='utf-8', newline='') as f:
    f.write(sitemap)
print("  ✓ sitemap.xml — blog.html lastmod updated to 2026-05-25")

print("\n✅ Done! All quick SEO fixes applied.")
print("\nRemaining manual tasks:")
print("  1. Create og-image.png (1200×630) — running generate_og_image.py next")
print("  2. Register Google My Business")
print("  3. Add real street address to schema")
