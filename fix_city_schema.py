#!/usr/bin/env python3
"""Fix schema markup on all 5 city pages."""
import json
import re

BASE_URL = "https://clean-clean.com.ua"
GBP_URL = "https://g.page/r/CcuiKcWaRxt2EAE"
TELEGRAM = "https://t.me/jamboss8"
LOGO = {
    "@type": "ImageObject",
    "url": f"{BASE_URL}/img/logo-cleanclean.svg",
    "width": 200,
    "height": 60
}
OPENING_HOURS = {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
    "opens": "08:00",
    "closes": "21:00"
}
CONTACT_POINT = {
    "@type": "ContactPoint",
    "contactType": "customer service",
    "telephone": "+380731312228",
    "availableLanguage": ["Ukrainian", "Russian"]
}
AGGREGATE_RATING = {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "2"
}
OFFER_CATALOG = {
    "@type": "OfferCatalog",
    "name": "Клінінгові послуги",
    "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Підтримуюче прибирання", "url": f"{BASE_URL}/services/pidtrymuyuche-prybyrannia.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Генеральне прибирання", "url": f"{BASE_URL}/services/generalna-prybyrannia.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Хімчистка диванів", "url": f"{BASE_URL}/services/himchistka-divana.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Миття вікон", "url": f"{BASE_URL}/services/mytia-vikon.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Хімчистка матраців", "url": f"{BASE_URL}/services/himchistka-matratsa.html"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Прибирання після ремонту", "url": f"{BASE_URL}/services/pislia-remontu.html"}}
    ]
}

CITIES = {
    "kyiv": {
        "file": "kyiv.html",
        "city_ua": "Київ",
        "slug": "kyiv",
        "description": "Професійне прибирання квартир у Києві від Clean-Clean. Генеральне, підтримуюче, хімчистка. Від 50 ₴/м². Усі райони столиці. Виїзд за 2 години.",
        "image": f"{BASE_URL}/img/cities/kyiv.webp",
    },
    "dnipro": {
        "file": "dnipro.html",
        "city_ua": "Дніпро",
        "slug": "dnipro",
        "description": "Клінінг у Дніпрі від Clean-Clean. Лівий і правий берег. Генеральне, підтримуюче прибирання, хімчистка, після ремонту. Від 50 ₴/м².",
        "image": f"{BASE_URL}/img/cities/dnipro.webp",
    },
    "lviv": {
        "file": "lviv.html",
        "city_ua": "Львів",
        "slug": "lviv",
        "description": "Прибирання у Львові від Clean-Clean. Ідеально для Airbnb і оренди. Генеральне, підтримуюче, хімчистка. Від 50 ₴/м². Усі райони.",
        "image": f"{BASE_URL}/img/cities/lviv.webp",
    },
    "kharkiv": {
        "file": "kharkiv.html",
        "city_ua": "Харків",
        "slug": "kharkiv",
        "description": "Доступний клінінг у Харкові від Clean-Clean. Для студентів, сімей і бізнесу. Від 50 ₴/м². Салтівка, Центр, Павлове Поле та інші райони.",
        "image": f"{BASE_URL}/img/cities/kharkiv.webp",
    },
    "odesa": {
        "file": "odesa.html",
        "city_ua": "Одеса",
        "slug": "odesa",
        "description": "Професійний клінінг в Одесі від Clean-Clean. Airbnb, після ремонту, квартири. Від 50 ₴/м². Аркадія, Пересип та всі райони. Виїзд за 2 години.",
        "image": f"{BASE_URL}/img/cities/odessa.webp",
    },
}

def build_schema(city_key):
    c = CITIES[city_key]
    schema = {
        "@context": "https://schema.org",
        "@type": "CleaningService",
        "@id": f"{BASE_URL}/{c['slug']}.html#business",
        "name": "Clean-Clean",
        "url": f"{BASE_URL}/{c['slug']}.html",
        "logo": LOGO,
        "image": c["image"],
        "telephone": "+380731312228",
        "priceRange": "₴₴",
        "description": c["description"],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": c["city_ua"],
            "addressCountry": "UA"
        },
        "areaServed": {
            "@type": "City",
            "name": c["city_ua"]
        },
        "aggregateRating": AGGREGATE_RATING,
        "openingHoursSpecification": OPENING_HOURS,
        "contactPoint": CONTACT_POINT,
        "sameAs": [GBP_URL, TELEGRAM],
        "hasOfferCatalog": OFFER_CATALOG
    }
    return schema

def build_breadcrumb(city_key):
    c = CITIES[city_key]
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": c["city_ua"], "item": f"{BASE_URL}/{c['slug']}.html"}
        ]
    }

def schema_to_script(obj):
    return f'<script type="application/ld+json">\n  {json.dumps(obj, ensure_ascii=False, indent=2)}\n  </script>'

# Pattern to match any LocalBusiness or CleaningService script block
SCHEMA_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*\{[^<]*?"@type"\s*:\s*"(?:LocalBusiness|CleaningService)"[^<]*?\}\s*</script>',
    re.DOTALL
)
BREADCRUMB_PATTERN = re.compile(
    r'<script type="application/ld\+json">\s*\{[^<]*?"@type"\s*:\s*"BreadcrumbList"[^<]*?\}\s*</script>',
    re.DOTALL
)

for city_key, city_data in CITIES.items():
    filepath = f"C:/tmp/cleaning-site/{city_data['file']}"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    new_schema = schema_to_script(build_schema(city_key))
    new_breadcrumb = schema_to_script(build_breadcrumb(city_key))

    # Replace existing LocalBusiness/CleaningService schema
    if SCHEMA_PATTERN.search(content):
        content = SCHEMA_PATTERN.sub(new_schema, content, count=1)
    else:
        # Insert before </head>
        content = content.replace("</head>", f"  {new_schema}\n</head>", 1)

    # Replace or add BreadcrumbList
    if BREADCRUMB_PATTERN.search(content):
        content = BREADCRUMB_PATTERN.sub(new_breadcrumb, content, count=1)
    else:
        # Insert after the main schema block
        content = content.replace(new_schema, f"{new_schema}\n  {new_breadcrumb}", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ {city_data['file']} — updated")

print("\nAll city pages updated.")
