import os, re, glob
from datetime import datetime

BASE = r"C:\Users\Admin\cleaning-site"

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new = html

    # 1. Remove unverified AggregateRating from Schema (Google policy violation)
    new = re.sub(
        r',?\s*"aggregateRating":\s*\{[^}]+\}',
        '', new
    )

    # 2. Fix city card links: #order → city pages
    new = new.replace('href="#order" class="city" data-city="kyiv"',   'href="kyiv.html" class="city" data-city="kyiv"')
    new = new.replace('href="#order" class="city" data-city="dnipro"', 'href="dnipro.html" class="city" data-city="dnipro"')
    new = new.replace('href="#order" class="city" data-city="lviv"',   'href="lviv.html" class="city" data-city="lviv"')
    new = new.replace('href="#order" class="city" data-city="kharkiv"','href="kharkiv.html" class="city" data-city="kharkiv"')
    new = new.replace('href="#order" class="city" data-city="odessa"', 'href="odessa.html" class="city" data-city="odessa"')

    # 3. Brand: "Clean Clean" (without dash) → "Clean-Clean"
    new = new.replace('"name": "Clean Clean"', '"name": "Clean-Clean"')
    new = new.replace("'name': 'Clean Clean'", "'name': 'Clean-Clean'")
    new = new.replace('>Clean Clean<', '>Clean-Clean<')

    if new != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        total += 1
        print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nHTML fixes: {total} files")

# 4. Add <lastmod> to sitemap.xml
sitemap_path = os.path.join(BASE, 'sitemap.xml')
with open(sitemap_path, encoding='utf-8') as f:
    sitemap = f.read()

today = datetime.now().strftime('%Y-%m-%d')
# Add lastmod after each <loc>
new_sitemap = re.sub(
    r'(<loc>[^<]+</loc>)\s*(<changefreq>)',
    rf'\1\n    <lastmod>{today}</lastmod>\n    \2',
    sitemap
)
if new_sitemap != sitemap:
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_sitemap)
    print("sitemap.xml: added lastmod dates")

# 5. FAQPage schema on faq.html
faq_path = os.path.join(BASE, 'faq.html')
with open(faq_path, encoding='utf-8') as f:
    faq = f.read()

if 'FAQPage' not in faq:
    faq_schema = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Скільки коштує прибирання квартири?",
        "acceptedAnswer": {"@type": "Answer", "text": "Підтримуюче від 50 ₴/м², генеральне від 70 ₴/м². Точну ціну розрахуйте в калькуляторі або замовте безкоштовний дзвінок."}
      },
      {
        "@type": "Question",
        "name": "Чи привозите ви хімію та обладнання?",
        "acceptedAnswer": {"@type": "Answer", "text": "Так. Привозимо професійну хімію Clinex та Karpax, пилососи, пароочисники. Вам нічого не потрібно готувати."}
      },
      {
        "@type": "Question",
        "name": "Що якщо результат не сподобається?",
        "acceptedAnswer": {"@type": "Answer", "text": "Переробимо безкоштовно. Якщо проблема залишиться — повернемо гроші повністю."}
      },
      {
        "@type": "Question",
        "name": "Як швидко ви приїдете?",
        "acceptedAnswer": {"@type": "Answer", "text": "У середньому через 2 години після підтвердження заявки. Працюємо з 8:00 до 21:00 щодня."}
      },
      {
        "@type": "Question",
        "name": "У яких містах ви працюєте?",
        "acceptedAnswer": {"@type": "Answer", "text": "Київ, Дніпро, Львів, Харків та Одеса. Виїзд по всіх районах."}
      }
    ]
  }
  </script>'''
    faq = faq.replace('</head>', faq_schema + '\n</head>', 1)
    with open(faq_path, 'w', encoding='utf-8') as f:
        f.write(faq)
    print("faq.html: FAQPage schema added")

print("Done!")
