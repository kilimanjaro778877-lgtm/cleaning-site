import os, re, glob, json

BASE = r"C:\Users\Admin\cleaning-site"
SITE = "https://clean-clean.com.ua"

def inject_before_head_close(html, schema_json):
    tag = f'  <script type="application/ld+json">\n  {json.dumps(schema_json, ensure_ascii=False, separators=(",",":"))}\n  </script>'
    return html.replace('</head>', tag + '\n</head>', 1)

def add_og_image(html, img_url):
    if 'og:image' in html:
        return html
    og_site = '<meta property="og:site_name" content="Clean-Clean" />'
    insert = f'<meta property="og:image" content="{img_url}" />'
    return html.replace(og_site, og_site + insert)

total = 0

# ── Blog posts: add BreadcrumbList ────────────────────────────────────────────
for path in glob.glob(BASE + r"\blog\*.html"):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if '"BreadcrumbList"' in html:
        continue

    # Extract headline from Article schema
    m = re.search(r'"headline"\s*:\s*"([^"]+)"', html)
    title = m.group(1) if m else os.path.splitext(os.path.basename(path))[0]

    # Extract canonical URL
    m2 = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    url = m2.group(1) if m2 else ''
    slug = os.path.basename(url)

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Блог", "item": f"{SITE}/blog.html"},
            {"@type": "ListItem", "position": 3, "name": title}
        ]
    }
    html = inject_before_head_close(html, breadcrumb)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    total += 1
    print(f"Blog breadcrumb: {os.path.basename(path)}")

# ── prices.html ───────────────────────────────────────────────────────────────
prices_path = os.path.join(BASE, 'prices.html')
with open(prices_path, encoding='utf-8') as f:
    prices = f.read()

if '"BreadcrumbList"' not in prices:
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Ціни на прибирання"}
        ]
    }
    prices = inject_before_head_close(prices, bc)

if '"WebPage"' not in prices:
    wp = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Ціни на прибирання квартир — Clean-Clean",
        "url": f"{SITE}/prices.html",
        "description": "Актуальні ціни на прибирання квартир, хімчистку диванів і матраців, миття вікон від Clean-Clean.",
        "inLanguage": "uk",
        "isPartOf": {"@type": "WebSite", "url": f"{SITE}/"}
    }
    prices = inject_before_head_close(prices, wp)

prices = add_og_image(prices, "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=1200&h=630&auto=format&fit=crop&q=80")

with open(prices_path, 'w', encoding='utf-8') as f:
    f.write(prices)
total += 1
print("prices.html: schema + OG image")

# ── blog.html ─────────────────────────────────────────────────────────────────
blog_path = os.path.join(BASE, 'blog.html')
with open(blog_path, encoding='utf-8') as f:
    blog = f.read()

if '"BreadcrumbList"' not in blog:
    bc = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Блог"}
        ]
    }
    blog = inject_before_head_close(blog, bc)

if '"Blog"' not in blog:
    blog_schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Блог Clean-Clean",
        "url": f"{SITE}/blog.html",
        "description": "Поради з прибирання квартири, огляди засобів, лайфхаки для підтримання чистоти.",
        "inLanguage": "uk",
        "publisher": {
            "@type": "Organization",
            "name": "Clean-Clean",
            "url": f"{SITE}/"
        }
    }
    blog = inject_before_head_close(blog, blog_schema)

blog = add_og_image(blog, "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&h=630&auto=format&fit=crop&q=80")

with open(blog_path, 'w', encoding='utf-8') as f:
    f.write(blog)
total += 1
print("blog.html: schema + OG image")

print(f"\nTotal: {total} files updated")
