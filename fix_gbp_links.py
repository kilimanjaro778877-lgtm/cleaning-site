#!/usr/bin/env python3
"""Add Google review badges to all city pages and update sameAs per city."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(path):
    with open(path, encoding='utf-8') as f: return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f: f.write(content)
    print(f"  ✓ {os.path.relpath(path, BASE)}")

# GBP review URLs per city
# Main URL used for all for now; city-specific ones to be updated when user provides
GBP_REVIEW = {
    'kyiv.html':    'https://g.page/r/CcuiKcWaRxt2EAE/review',
    'dnipro.html':  'https://g.page/r/CcuiKcWaRxt2EAE/review',
    'lviv.html':    'https://g.page/r/CcuiKcWaRxt2EAE/review',
    'kharkiv.html': 'https://g.page/r/CcuiKcWaRxt2EAE/review',
    'odesa.html':   'https://g.page/r/CcuiKcWaRxt2EAE/review',
}

GOOGLE_SVG = '<svg width="18" height="18" viewBox="0 0 48 48" style="flex-shrink:0" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9 3.2l6.7-6.7C35.8 2.5 30.3 0 24 0 14.6 0 6.6 5.5 2.7 13.5l7.8 6C12.4 13.1 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.6 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4.1 7.2-10.1 7.2-17z"/><path fill="#FBBC05" d="M10.5 28.6A14.5 14.5 0 0 1 9.5 24c0-1.6.3-3.2.7-4.6l-7.8-6A23.9 23.9 0 0 0 0 24c0 3.9.9 7.5 2.6 10.8l7.9-6.2z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.5-5.8c-2.1 1.4-4.8 2.3-8.4 2.3-6.3 0-11.6-3.6-13.5-9.1l-7.9 6.2C6.6 42.5 14.6 48 24 48z"/></svg>'

BADGE_HTML = '''        <a href="{url}" target="_blank" rel="noopener"
           style="display:inline-flex;align-items:center;gap:8px;margin-top:20px;padding:10px 18px;background:#fff;border:1.5px solid #e5e7eb;border-radius:999px;font-size:13px;font-weight:600;color:#374151;text-decoration:none;transition:box-shadow .2s,border-color .2s"
           onmouseover="this.style.borderColor='#22c55e';this.style.boxShadow='0 2px 10px rgba(34,197,94,.18)'"
           onmouseout="this.style.borderColor='#e5e7eb';this.style.boxShadow=''"
           aria-label="Залишити відгук на Google">
          {svg}
          <span style="color:#f59e0b;letter-spacing:1px">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
          <span style="font-weight:700;color:#111827">4.9</span>
          <span style="color:#6b7280;font-weight:400">&#183; Залишити відгук на Google</span>
        </a>'''

print("Adding Google review badge to city pages:")

for fname, review_url in GBP_REVIEW.items():
    path = os.path.join(BASE, fname)
    content = read(path)

    if 'Залишити відгук на Google' in content:
        print(f"  — {fname}: badge already present")
        continue

    badge = BADGE_HTML.format(url=review_url, svg=GOOGLE_SVG)

    # Insert badge after the stats grid (after </div> that closes the grid)
    # The stats grid ends with </div> before </div> closing the max-w-3xl
    pattern = r'(<div class="mt-10 grid grid-cols-3[^"]*[^>]*>.*?</div>\s*</div>)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + badge + content[insert_pos:]
        write(path, content)
    else:
        # Fallback: insert after the first CTA button block
        fallback_pattern = r'(</a>\s*</div>\s*<div class="mt-10 grid)'
        if re.search(fallback_pattern, content, re.DOTALL):
            content = re.sub(
                r'(<div class="mt-10 grid)',
                badge + r'\n        \1',
                content
            )
            write(path, content)
        else:
            print(f"  ! {fname}: pattern not found, skipping")

print("\nDone.")
