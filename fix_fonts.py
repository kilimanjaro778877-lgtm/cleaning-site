import os, re

BASE = r"C:\Users\Admin\cleaning-site"

# Replace font-display → font-sans ONLY for number/stat elements
# Keep font-display for h1/h2/h3 headings
REPLACEMENTS = [
    # Metric stats (like "8 500+", "від 50 ₴", "24/7", "4.9 ★")
    ('class="font-display text-2xl font-extrabold text-gold-400"',
     'class="font-sans text-2xl font-extrabold text-gold-400 tabular-nums"'),
    ('class="font-display text-2xl font-extrabold text-green-600"',
     'class="font-sans text-2xl font-extrabold text-green-600 tabular-nums"'),
    # Calculator price value
    ('class="font-display text-5xl sm:text-6xl font-black text-gray-900" id="price-value"',
     'class="font-sans text-5xl sm:text-6xl font-black text-gray-900 tabular-nums" id="price-value"'),
    # Fixed price block
    ('class="font-display text-5xl sm:text-6xl font-black text-gray-900" id="fixed-price"',
     'class="font-sans text-5xl sm:text-6xl font-black text-gray-900 tabular-nums" id="fixed-price"'),
    # Area value slider
    ('class="font-display text-5xl font-black text-gray-900" id="area-value"',
     'class="font-sans text-5xl font-black text-gray-900 tabular-nums" id="area-value"'),
    # Service pages price display (pg-price)
    ('class="font-display text-5xl sm:text-6xl font-black text-gray-900" id="pg-price"',
     'class="font-sans text-5xl sm:text-6xl font-black text-gray-900 tabular-nums" id="pg-price"'),
    # Trust stats (4.9 ★, 5.0 ★, 98%, 12k+)
    ('class="font-display text-4xl font-black text-gold-400 leading-[1.15]"',
     'class="font-sans text-4xl font-black text-gold-400 tabular-nums"'),
    # Mattress pricing scroll select
    ('class="font-display text-2xl font-black"',
     'class="font-sans text-2xl font-black tabular-nums"'),
    # City page stats
    ('class="font-display text-2xl font-extrabold text-gold-400">',
     'class="font-sans text-2xl font-extrabold text-gold-400 tabular-nums">'),
]

# Add tabular-nums CSS to all pages
TABULAR_CSS = "\n    .tabular-nums { font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }"

total = 0
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        new = html

        for old, nw in REPLACEMENTS:
            new = new.replace(old, nw)

        # Add tabular-nums CSS if not present and page has numbers
        if 'tabular-nums' in new and TABULAR_CSS.strip() not in new:
            new = new.replace('</style>', TABULAR_CSS + '\n  </style>', 1)

        if new != html:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new)
            total += 1
            print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files.")
