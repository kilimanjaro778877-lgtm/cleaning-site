import os, re, glob

BASE = r"C:\Users\Admin\cleaning-site"

EMOJI_RE = re.compile("["
    "\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F9FF\U00002702-\U000027B0"
    "\U000024C2-\U0001F251\U0001F900-\U0001F9FF"
    "☀-⛿✀-➿"
    "]+", flags=re.UNICODE)

TIKTOK_START = "<!-- TikTok Pixel Code Start -->"
TIKTOK_END = "<!-- TikTok Pixel Code End -->"

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = html

    # 1. Move TikTok pixel from <head> to before </body>
    if TIKTOK_START in new and TIKTOK_END in new:
        start_idx = new.find(TIKTOK_START)
        end_idx = new.find(TIKTOK_END) + len(TIKTOK_END)
        tiktok_block = new[start_idx:end_idx]
        # Check if it's in head (before </head>)
        head_end = new.find("</head>")
        if head_end > 0 and start_idx < head_end:
            new = new[:start_idx] + new[end_idx:]
            # Also remove the extra ttq.track script block right after it
            # Find and remove the second script block that references ttq
            new = new.replace("</body>", tiktok_block + "\n</body>", 1)

    # 2. Remove emojis from <p> and <li> content only (not buttons/badges)
    def strip_emoji_from_tags(html, tag):
        pattern = re.compile(r'(<' + tag + r'(?:\s[^>]*)?>)(.*?)(</' + tag + r'>)', re.DOTALL)
        def replacer(m):
            open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
            # Skip if inside button, tag badge, or floating action div
            if any(x in open_tag for x in ['btn', 'upsell', 'filter']):
                return m.group(0)
            cleaned = EMOJI_RE.sub('', content).strip()
            # Clean up double spaces
            cleaned = re.sub(r'  +', ' ', cleaned)
            return open_tag + cleaned + close_tag
        return pattern.sub(replacer, html)

    new = strip_emoji_from_tags(new, 'p')
    new = strip_emoji_from_tags(new, 'li')

    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        total += 1
        print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files.")
