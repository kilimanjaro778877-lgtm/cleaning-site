import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# Mobile nav HTML to insert after the header closing tag
# We'll inject it right after </header>
MOBILE_NAV = '''
  <!-- Mobile nav drawer -->
  <div id="mobile-nav" class="hidden md:hidden sticky top-16 z-40 bg-white/98 backdrop-blur-lg border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col gap-1">
      <a href="{prefix}index.html#services" class="px-4 py-3 rounded-xl text-gray-700 hover:text-gray-900 hover:bg-gray-50 font-medium transition">Послуги</a>
      <a href="{prefix}prices.html" class="px-4 py-3 rounded-xl text-gray-700 hover:text-gray-900 hover:bg-gray-50 font-medium transition">Ціни</a>
      <a href="{prefix}blog.html" class="px-4 py-3 rounded-xl text-gray-700 hover:text-gray-900 hover:bg-gray-50 font-medium transition">Блог</a>
      <a href="{prefix}faq.html" class="px-4 py-3 rounded-xl text-gray-700 hover:text-gray-900 hover:bg-gray-50 font-medium transition">FAQ</a>
      <div class="border-t border-gray-100 pt-2 mt-1">
        <a href="tel:+380731312228" class="flex items-center gap-2 px-4 py-3 rounded-xl text-gray-900 font-semibold hover:bg-gray-50 transition">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 10.8 19.79 19.79 0 010 2.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>
          +38 073 131 22 28
        </a>
      </div>
    </div>
  </div>
  <script>
    (function(){
      var btn = document.getElementById('mobile-menu-btn');
      var nav = document.getElementById('mobile-nav');
      if(!btn || !nav) return;
      btn.addEventListener('click', function(){
        var open = nav.classList.toggle('hidden');
        btn.setAttribute('aria-expanded', !open);
      });
      nav.querySelectorAll('a').forEach(function(a){
        a.addEventListener('click', function(){ nav.classList.add('hidden'); btn.setAttribute('aria-expanded','false'); });
      });
    })();
  </script>'''

# Hamburger button HTML to inject before the nav closing or after logo
HAMBURGER = '<button id="mobile-menu-btn" class="md:hidden p-2 text-gray-500 hover:text-gray-900 transition" aria-label="Меню" aria-expanded="false" aria-controls="mobile-nav"><svg id="icon-menu" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg></button>'

# Pages that need mobile nav (not index.html - it already has it)
NEEDS_MOB_NAV = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if not f.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(root, f), BASE)
        if rel == 'index.html' or rel == '404.html' or rel.startswith('blog\\gen') or rel.startswith('blog\\kh') or rel.startswith('blog\\por') or rel.startswith('blog\\pyl') or rel.startswith('blog\\yak'):
            continue
        NEEDS_MOB_NAV.append((os.path.join(root, f), rel))

total = 0
for path, rel in NEEDS_MOB_NAV:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Skip if already has mobile-nav
    if 'id="mobile-nav"' in html:
        continue

    # Determine path prefix (services/ pages need ../, root pages need nothing)
    prefix = "../" if "\\" in rel and rel.count("\\") >= 1 else ""

    # Add hamburger button before the phone/button div in header
    # Find: <div class="flex items-center gap-3"> in header
    mob_btn = HAMBURGER
    old_flex = '<div class="flex items-center gap-3">'
    if old_flex in html[:html.find('</header>')] and mob_btn not in html:
        header_end = html.find('</header>')
        header_part = html[:header_end]
        # Insert hamburger before the flex div
        header_part = header_part.replace(old_flex, mob_btn + '\n      ' + old_flex, 1)
        html = header_part + html[header_end:]

    # Insert mobile nav after </header>
    mob_nav_html = MOBILE_NAV.replace("{prefix}", prefix)
    if '</header>' in html and 'id="mobile-nav"' not in html:
        html = html.replace('</header>', '</header>' + mob_nav_html, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    total += 1
    print(f"ADDED mobile nav: {rel}")

print(f"\nDone — {total} pages updated.")
