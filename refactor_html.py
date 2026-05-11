#!/usr/bin/env python3
"""
Refactor HTML files in cleaning-site:
1. Remove emoji from H1/H2/H3 heading tags only
2. Replace "за 5 хвилин" callback promises with "протягом дня"
3. Remove emoji from hero section inline-flex badges (but keep badge itself)
"""

import re
import os

# Broad emoji pattern covering most Unicode emoji blocks
EMOJI_PATTERN = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F9FF"  # transport, misc symbols, supplemental
    u"\U0001F1E0-\U0001F1FF"  # flags
    u"\U00002702-\U000027B0"  # dingbats
    u"\U000024C2-\U0001F251"  # enclosed chars, misc
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text: str) -> str:
    """Remove all emoji characters and clean up surrounding whitespace."""
    result = EMOJI_PATTERN.sub("", text)
    # Collapse multiple spaces/newlines into one, but preserve intentional newlines
    result = re.sub(r"[ \t]{2,}", " ", result)
    return result.strip()


def process_heading_tag(match: re.Match) -> str:
    """Called for each <h1>…</h1>, <h2>…</h2>, <h3>…</h3> match.
    Strips emoji from the inner content while keeping all HTML tags intact."""
    full = match.group(0)
    open_tag = match.group(1)   # e.g. <h2 class="...">
    inner = match.group(2)      # everything between open and close tag
    close_tag = match.group(3)  # e.g. </h2>

    # We only strip emoji from text nodes — not from inside attribute values.
    # Strategy: split on child HTML tags, strip emoji from text pieces only.
    def strip_text_nodes(html: str) -> str:
        # Split into alternating text / tag segments
        parts = re.split(r"(<[^>]+>)", html)
        cleaned = []
        for part in parts:
            if part.startswith("<"):
                cleaned.append(part)  # keep tags verbatim
            else:
                cleaned.append(strip_emoji(part) if EMOJI_PATTERN.search(part) else part)
        return "".join(cleaned)

    new_inner = strip_text_nodes(inner)
    return open_tag + new_inner + close_tag


# Regex: captures open tag, inner HTML (non-greedy), close tag.
# re.DOTALL so inner content can span multiple lines.
HEADING_RE = re.compile(
    r"(<h[123][^>]*>)(.*?)(</h[123]>)",
    flags=re.DOTALL | re.IGNORECASE,
)


def process_file(path: str) -> tuple[bool, list[str]]:
    """Process a single HTML file. Returns (changed, list_of_changes)."""
    with open(path, encoding="utf-8") as f:
        original = f.read()

    content = original
    changes = []

    # ------------------------------------------------------------------ #
    # 1. Remove emoji from H1 / H2 / H3 headings                         #
    # ------------------------------------------------------------------ #
    def heading_replacer(m: re.Match) -> str:
        result = process_heading_tag(m)
        if result != m.group(0):
            changes.append(f"  [heading emoji] stripped emoji from: {m.group(0)[:80].strip()!r}")
        return result

    content = HEADING_RE.sub(heading_replacer, content)

    # ------------------------------------------------------------------ #
    # 2. Remove emoji from hero inline-flex badge divs                    #
    #    Pattern: <div class="inline-flex ...">EMOJI text</div>           #
    #    We only target divs whose class starts with "inline-flex" and    #
    #    that contain emoji — keep the badge div, strip the emoji.        #
    # ------------------------------------------------------------------ #
    BADGE_RE = re.compile(
        r'(<div\s[^>]*class="inline-flex[^"]*"[^>]*>)\s*'
        r'((?:' + EMOJI_PATTERN.pattern + r'\s*)+)'
        r'(.*?)(</div>)',
        flags=re.DOTALL | re.UNICODE,
    )

    def badge_replacer(m: re.Match) -> str:
        open_div = m.group(1)
        # emoji part is group 2, text is group 3, close_div is group 4
        text_part = m.group(3).strip()
        close_div = m.group(4)
        result = open_div + "\n            " + text_part + "\n          " + close_div
        changes.append(f"  [badge emoji] removed badge emoji, kept: {text_part!r}")
        return result

    content = BADGE_RE.sub(badge_replacer, content)

    # ------------------------------------------------------------------ #
    # 3. Replace callback "5 хвилин" promises with "протягом дня"         #
    #                                                                      #
    #    Patterns found in the codebase:                                  #
    #      "Передзвонимо протягом 5 хвилин"                               #
    #      "відповімо протягом 5 хвилин"                                  #
    #      "Розрахунок за 5 хвилин"                                       #
    # ------------------------------------------------------------------ #
    replacements_5min = [
        # "Передзвонимо протягом 5 хвилин" → "Передзвонимо протягом дня"
        (
            re.compile(r"Передзвонимо протягом 5 хвилин", re.UNICODE),
            "Передзвонимо протягом дня",
        ),
        # "відповімо протягом 5 хвилин" → "відповімо протягом дня"
        (
            re.compile(r"відповімо протягом 5 хвилин", re.UNICODE),
            "відповімо протягом дня",
        ),
        # "Розрахунок за 5 хвилин" → "Розрахунок протягом дня"
        (
            re.compile(r"Розрахунок за 5 хвилин", re.UNICODE),
            "Розрахунок протягом дня",
        ),
    ]

    for pattern, replacement in replacements_5min:
        new_content, n = pattern.subn(replacement, content)
        if n:
            changes.append(f"  [5min→день] replaced {n}x: {pattern.pattern!r} → {replacement!r}")
            content = new_content

    changed = content != original
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return changed, changes


def collect_target_files(root: str) -> list[str]:
    """Collect all target HTML files as specified in the task."""
    targets = []

    # Root-level files
    for name in ["blog.html", "faq.html", "prices.html",
                 "kyiv.html", "dnipro.html", "lviv.html",
                 "kharkiv.html", "odessa.html"]:
        p = os.path.join(root, name)
        if os.path.isfile(p):
            targets.append(p)

    # All files under services/
    services_dir = os.path.join(root, "services")
    if os.path.isdir(services_dir):
        for name in os.listdir(services_dir):
            if name.endswith(".html"):
                targets.append(os.path.join(services_dir, name))

    return sorted(targets)


def main():
    root = r"C:\Users\Admin\cleaning-site"
    files = collect_target_files(root)

    print(f"Processing {len(files)} HTML files...\n")
    total_changed = 0

    for path in files:
        rel = os.path.relpath(path, root)
        changed, changes = process_file(path)
        if changed:
            total_changed += 1
            print(f"CHANGED  {rel}")
            for c in changes:
                print(c)
        else:
            print(f"no-op    {rel}")

    print(f"\nDone. {total_changed}/{len(files)} files modified.")


if __name__ == "__main__":
    main()
