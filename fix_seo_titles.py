import os, re, glob

BASE = r"C:\Users\Admin\cleaning-site"

# Title fixes: file -> new title (max 60 chars)
TITLE_FIXES = {
    "lviv.html":
        "Прибирання квартир у Львові — від 50 ₴/м² | Clean-Clean",
    "services/generalna-prybyrannia.html":
        "Генеральне прибирання квартири — від 70 ₴/м² | Clean-Clean",
    "services\\generalna-prybyrannia.html":
        "Генеральне прибирання квартири — від 70 ₴/м² | Clean-Clean",
    "services/himchistka-divana.html":
        "Хімчистка диванів удома — від 1 100 ₴ | Clean-Clean",
    "services\\himchistka-divana.html":
        "Хімчистка диванів удома — від 1 100 ₴ | Clean-Clean",
    "services/himchistka-matratsa.html":
        "Хімчистка матраців — від 300 ₴ | Clean-Clean",
    "services\\himchistka-matratsa.html":
        "Хімчистка матраців — від 300 ₴ | Clean-Clean",
    "services/klinig-ofisiv.html":
        "Клінінг офісів — ціна після консультації | Clean-Clean",
    "services\\klinig-ofisiv.html":
        "Клінінг офісів — ціна після консультації | Clean-Clean",
    "services/mytia-vikon.html":
        "Миття вікон без розводів — від 80 ₴/м² | Clean-Clean",
    "services\\mytia-vikon.html":
        "Миття вікон без розводів — від 80 ₴/м² | Clean-Clean",
    "services/pidtrymuyuche-prybyrannia.html":
        "Підтримуюче прибирання — від 50 ₴/м² | Clean-Clean",
    "services\\pidtrymuyuche-prybyrannia.html":
        "Підтримуюче прибирання — від 50 ₴/м² | Clean-Clean",
    "services/pislia-remontu.html":
        "Прибирання після ремонту — від 4 500 ₴ | Clean-Clean",
    "services\\pislia-remontu.html":
        "Прибирання після ремонту — від 4 500 ₴ | Clean-Clean",
    "services/prybyrannia-kukhni.html":
        "Прибирання кухні — від 1 800 ₴ | Clean-Clean",
    "services\\prybyrannia-kukhni.html":
        "Прибирання кухні — від 1 800 ₴ | Clean-Clean",
    "services/prybyrannia-vannoi.html":
        "Прибирання ванної кімнати — від 1 300 ₴ | Clean-Clean",
    "services\\prybyrannia-vannoi.html":
        "Прибирання ванної кімнати — від 1 300 ₴ | Clean-Clean",
}

# Add meta description to 404.html
META_DESC_FIXES = {
    "404.html": "Сторінку не знайдено. Повернутись на головну Clean-Clean — клінінг у Києві, Дніпрі, Львові, Харкові та Одесі.",
}

# Enhanced Schema for index.html
ENHANCED_SCHEMA = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Clean Clean",
    "url": "https://clean-clean.com.ua/",
    "logo": "https://clean-clean.com.ua/img/cities/kyiv.webp",
    "image": "https://clean-clean.com.ua/img/cities/kyiv.webp",
    "telephone": "+380731312228",
    "email": "kilimanjaro778877@gmail.com",
    "priceRange": "₴₴",
    "description": "Професійна клінінгова компанія. Прибирання квартир, хімчистка диванів і матраців, миття вікон. Виїзд за 2 години.",
    "areaServed": [
      {"@type": "City", "name": "Київ"},
      {"@type": "City", "name": "Дніпро"},
      {"@type": "City", "name": "Львів"},
      {"@type": "City", "name": "Харків"},
      {"@type": "City", "name": "Одеса"}
    ],
    "openingHoursSpecification": {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "08:00",
      "closes": "21:00"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "Customer Service",
      "telephone": "+380731312228",
      "availableLanguage": ["Ukrainian", "Russian"]
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "1483",
      "bestRating": "5"
    },
    "hasOfferCatalog": {
      "@type": "OfferCatalog",
      "name": "Клінінгові послуги",
      "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Підтримуюче прибирання", "url": "https://clean-clean.com.ua/services/pidtrymuyuche-prybyrannia.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Генеральне прибирання", "url": "https://clean-clean.com.ua/services/generalna-prybyrannia.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Хімчистка диванів", "url": "https://clean-clean.com.ua/services/himchistka-divana.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Миття вікон", "url": "https://clean-clean.com.ua/services/mytia-vikon.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Хімчистка матраців", "url": "https://clean-clean.com.ua/services/himchistka-matratsa.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Прибирання після ремонту", "url": "https://clean-clean.com.ua/services/pislia-remontu.html"}}
      ]
    }
  }
  </script>'''

OLD_SCHEMA_RE = re.compile(
    r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"LocalBusiness"[^<]*</script>',
    re.DOTALL
)

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    rel = os.path.relpath(path, BASE)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new = html

    # Fix titles
    if rel in TITLE_FIXES or rel.replace('\\', '/') in {k.replace('\\', '/') for k in TITLE_FIXES}:
        key = rel if rel in TITLE_FIXES else rel.replace('\\', '/')
        new_title = TITLE_FIXES.get(rel) or TITLE_FIXES.get(rel.replace('\\', '/')) or TITLE_FIXES.get(rel.replace('/', '\\'))
        if new_title:
            new = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', new)

    # Add meta description to 404
    if rel in META_DESC_FIXES and 'meta name="description"' not in new:
        desc = META_DESC_FIXES[rel]
        new = new.replace('<link rel="canonical"',
            f'<meta name="description" content="{desc}" />\n  <link rel="canonical"', 1)

    # Enhance schema on index.html
    if rel == 'index.html' and '"@type": "LocalBusiness"' in new:
        new = OLD_SCHEMA_RE.sub(ENHANCED_SCHEMA, new, count=1)

    if new != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        total += 1
        print(f"FIXED: {rel}")

print(f"\nDone — {total} files.")
