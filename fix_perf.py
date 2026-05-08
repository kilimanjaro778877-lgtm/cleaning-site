import os

BASE = r"C:\Users\Admin\cleaning-site"

# index.html: pravatar lazy + city photos lazy
idx = os.path.join(BASE, "index.html")
with open(idx, encoding="utf-8") as f:
    html = f.read()

# Avatars lazy (avoid double-adding)
if 'loading="lazy" src="https://i.pravatar.cc' not in html:
    html = html.replace(
        'src="https://i.pravatar.cc/80?img=',
        'loading="lazy" src="https://i.pravatar.cc/80?img='
    )

# City photos lazy (all except kyiv)
for city in ["dnipro", "lviv", "kharkiv", "odessa"]:
    old = f'src="img/cities/{city}.'
    new = f'loading="lazy" src="img/cities/{city}.'
    if new not in html:
        html = html.replace(old, new, 1)

with open(idx, "w", encoding="utf-8") as f:
    f.write(html)
print("FIXED: index.html (lazy loading)")

# Service pages: remove loading=lazy from FIRST img (hero = LCP element)
svc_dir = os.path.join(BASE, "services")
for fn in os.listdir(svc_dir):
    if not fn.endswith(".html"):
        continue
    path = os.path.join(svc_dir, fn)
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # Remove lazy from first unsplash hero image only
    new = html.replace(
        '<img loading="lazy" src="https://images.unsplash.com',
        '<img fetchpriority="high" src="https://images.unsplash.com',
        1
    )
    # Also kitchen local hero
    new = new.replace(
        '<img loading="lazy" src="../img/kitchen-hero',
        '<img fetchpriority="high" src="../img/kitchen-hero',
        1
    )
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"FIXED: services/{fn} (hero img priority)")

# Create robots.txt
robots = os.path.join(BASE, "robots.txt")
with open(robots, "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: https://clean-clean.com.ua/sitemap.xml\n")
print("CREATED: robots.txt")

# Update sitemap.xml with missing pages
sitemap_path = os.path.join(BASE, "sitemap.xml")
with open(sitemap_path, encoding="utf-8") as f:
    sitemap = f.read()

missing_pages = [
    ("https://clean-clean.com.ua/prices.html", "monthly", "0.8"),
    ("https://clean-clean.com.ua/faq.html", "monthly", "0.8"),
    ("https://clean-clean.com.ua/services/himchistka-matratsa.html", "monthly", "0.8"),
    ("https://clean-clean.com.ua/services/prybyrannia-kukhni.html", "monthly", "0.8"),
    ("https://clean-clean.com.ua/services/prybyrannia-vannoi.html", "monthly", "0.8"),
    ("https://clean-clean.com.ua/blog/generalna-chy-pidtrymuyuche.html", "monthly", "0.6"),
    ("https://clean-clean.com.ua/blog/poryadok-mizh-prybyranniamy.html", "monthly", "0.6"),
    ("https://clean-clean.com.ua/blog/yak-myty-vikna.html", "monthly", "0.6"),
    ("https://clean-clean.com.ua/blog/khimiia-dlia-prybyrannnia.html", "monthly", "0.6"),
    ("https://clean-clean.com.ua/blog/pylovi-klishi.html", "monthly", "0.6"),
]

new_entries = ""
for url, freq, priority in missing_pages:
    if url not in sitemap:
        new_entries += f"""  <url>
    <loc>{url}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

if new_entries:
    sitemap = sitemap.replace("</urlset>", new_entries + "</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"UPDATED: sitemap.xml ({new_entries.count('<url>')} pages added)")

print("\nDone.")
