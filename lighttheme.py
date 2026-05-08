import os, re

BASE = r"C:\Users\Admin\cleaning-site"

REPLACEMENTS = [
    # ── Body background & text color ─────────────────────────────────────
    ("background-color:#03040f",     "background-color:#f8fafc"),
    ("background-color:#02020f",     "background-color:#f8fafc"),
    ("background-color: #03040f",    "background-color: #f8fafc"),
    ("background-color: #02020f",    "background-color: #f8fafc"),
    # body text
    ("color: #f0ede8",               "color: #111827"),
    ("color:#f0ede8",                "color:#111827"),
    ("color: #FFFAFA",               "color: #111827"),
    # headings
    ("color:#f0ede8;overflow:visible","color:#111827;overflow:visible"),
    ("color: #f0ede8; }",            "color: #111827; }"),

    # ── Background dot pattern → subtle green dots ───────────────────────
    ("rgba(102,128,255,0.04)",       "rgba(34,197,94,0.04)"),

    # ── Orbs → light green/teal ──────────────────────────────────────────
    ("rgba(51,85,255,0.2)",          "rgba(34,197,94,0.12)"),
    ("rgba(100,51,255,0.16)",        "rgba(34,197,94,0.08)"),
    # orb colors in gradient
    ("radial-gradient(circle,rgba(51,85,255,0.2),rgba(51,85,255,0) 70%)",
     "radial-gradient(circle,rgba(34,197,94,0.18),rgba(34,197,94,0) 70%)"),
    ("radial-gradient(circle,rgba(100,51,255,0.16),rgba(100,51,255,0) 70%)",
     "radial-gradient(circle,rgba(34,197,94,0.10),rgba(34,197,94,0) 70%)"),

    # ── Tailwind ink palette → light grays ──────────────────────────────
    # index.html style
    ("900:'#03040f',800:'#07091e',700:'#0d1030',600:'#151840',500:'#1e2254'",
     "900:'#ffffff',800:'#f8fafc',700:'#f1f5f9',600:'#e2e8f0',500:'#cbd5e1'"),
    # service pages style
    ("900:'#02020f',800:'#06061c',700:'#0b0b2a',600:'#121238',500:'#1a1a4a'",
     "900:'#ffffff',800:'#f8fafc',700:'#f1f5f9',600:'#e2e8f0',500:'#cbd5e1'"),
    # other variants
    ("900: '#03040f', 800: '#07091e', 700: '#0d1030', 600: '#151840', 500: '#1e2254'",
     "900: '#ffffff', 800: '#f8fafc', 700: '#f1f5f9', 600: '#e2e8f0', 500: '#cbd5e1'"),

    # ── feat-card (used in service pages) ────────────────────────────────
    ("background:#111113;border:1px solid #1e1e21;",
     "background:#ffffff;border:1px solid #e5e7eb;"),

    # ── Header ────────────────────────────────────────────────────────────
    ("bg-ink-900/90 backdrop-blur-lg border-b border-ink-700",
     "bg-white/95 backdrop-blur-lg border-b border-gray-200"),
    ("bg-ink-900/95 backdrop-blur-lg border-b border-ink-700",
     "bg-white/95 backdrop-blur-lg border-b border-gray-200"),

    # ── Tailwind text classes → dark equivalents ─────────────────────────
    ("text-zinc-100 antialiased",    "text-gray-900 antialiased"),
    ('"text-zinc-100"',              '"text-gray-900"'),
    ("text-zinc-300 leading-relaxed","text-gray-700 leading-relaxed"),
    ("text-zinc-300",                "text-gray-700"),
    ("text-zinc-400 leading-relaxed","text-gray-500 leading-relaxed"),
    ("text-zinc-400",                "text-gray-500"),
    ("text-zinc-500",                "text-gray-400"),
    ("text-warm-100",                "text-gray-900"),

    # ── Background classes ────────────────────────────────────────────────
    ("bg-ink-900",  "bg-white"),
    ("bg-ink-800",  "bg-gray-50"),
    ("bg-ink-700",  "bg-white"),
    ("bg-ink-600",  "bg-gray-100"),

    # ── Border classes ────────────────────────────────────────────────────
    ("border-ink-700",  "border-gray-200"),
    ("border-ink-600",  "border-gray-200"),
    ("border-ink-500",  "border-gray-300"),

    # ── Form inputs ───────────────────────────────────────────────────────
    ("bg-ink-700 border border-ink-600 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-zinc-100",
     "bg-white border border-gray-300 focus:border-green-400 focus:ring-2 focus:ring-green-400/20 outline-none transition text-gray-900"),
    ("bg-ink-700 border border-ink-600 focus:border-green-400 outline-none text-zinc-100",
     "bg-white border border-gray-300 focus:border-green-400 outline-none text-gray-900"),

    # ── Hardcoded dark section backgrounds ──────────────────────────────
    ("bg-gradient-to-br from-ink-800 to-ink-900",
     "bg-gradient-to-br from-gray-50 to-white"),

    # ── gradient-bg stays light ──────────────────────────────────────────
    # already transparent — ok

    # ── Reviews carousel cards ───────────────────────────────────────────
    ("bg-ink-800 border border-ink-600 rounded-2xl p-6 w-80 shrink-0",
     "bg-white border border-gray-200 rounded-2xl p-6 w-80 shrink-0 shadow-sm"),
    ("bg-ink-800 border border-ink-600 rounded-2xl p-8",
     "bg-white border border-gray-200 rounded-2xl p-8 shadow-sm"),

    # ── Section divider (subtle) ─────────────────────────────────────────
    ("background: linear-gradient(to right, transparent, rgba(96,165,250,0.3), transparent)",
     "background: linear-gradient(to right, transparent, rgba(34,197,94,0.3), transparent)"),

    # ── Slider blue → green ──────────────────────────────────────────────
    ("background: linear-gradient(to right, #3355ff var(--p",
     "background: linear-gradient(to right, #22c55e var(--p"),
    ("background: linear-gradient(to right, #3355ff var(--p, 12%), #262629",
     "background: linear-gradient(to right, #22c55e var(--p, 12%), #e5e7eb"),
    ("background: #3355ff;",  "background: #22c55e;"),
    ("background: #3355ff\n",  "background: #22c55e\n"),
    ("box-shadow: 0 0 0 2px #3355ff",  "box-shadow: 0 0 0 2px #22c55e"),

    # ── Navigation text ───────────────────────────────────────────────────
    ("text-sm font-medium text-zinc-400\">",
     "text-sm font-medium text-gray-600\">"),

    # ── Noise overlay opacity (lighter on white) ─────────────────────────
    ("opacity: 0.025;", "opacity: 0.012;"),
]

HTML_GLOB = []
for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'img']]
    for f in files:
        if f.endswith('.html'):
            HTML_GLOB.append(os.path.join(root, f))

total = 0
for path in HTML_GLOB:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new_html = html
    for old, new in REPLACEMENTS:
        new_html = new_html.replace(old, new)
    if new_html != html:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        total += 1
        print(f"UPDATED: {os.path.relpath(path, BASE)}")
    else:
        print(f"clean:   {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files updated.")
