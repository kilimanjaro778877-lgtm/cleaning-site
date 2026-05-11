import os, re, glob

BASE = r"C:\Users\Admin\cleaning-site"

# Remove TikTok pixel block
TIKTOK_RE = re.compile(
    r'\n?<!-- TikTok Pixel Code Start -->.*?<!-- TikTok Pixel Code End -->',
    re.DOTALL
)
# Remove ttq tracking script (the second inline block)
TTQ_SCRIPT_RE = re.compile(
    r'\n?<script>\s*\(function\(\)\{[^}]*ttq\.track[^<]*</script>',
    re.DOTALL
)

fixed = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = TIKTOK_RE.sub("", html)
    new = TTQ_SCRIPT_RE.sub("", new)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        fixed += 1
        print(f"Removed TikTok: {os.path.basename(path)}")

print(f"\nDone — {fixed} files cleaned.")
