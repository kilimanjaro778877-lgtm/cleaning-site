import os, glob

BASE = r"C:\Users\Admin\cleaning-site"

FIXES = [
    # ── prices.html: dark price-card + blue colors ──────────────────────
    ("background:#07091e;border:1px solid #151840",
     "background:#ffffff;border:1px solid #e5e7eb"),
    ("border-color:rgba(102,128,255,0.35);box-shadow:0 0 0 1px rgba(102,128,255,0.12)",
     "border-color:rgba(34,197,94,0.35);box-shadow:0 0 0 1px rgba(34,197,94,0.12)"),
    # inline style on featured price card
    ('style="border-color:rgba(102,128,255,0.4);box-shadow:0 0 0 1px rgba(102,128,255,0.15)"',
     'style="border-color:rgba(34,197,94,0.4);box-shadow:0 0 0 1px rgba(34,197,94,0.15)"'),
    # check color
    (".check{color:#99aaff}",    ".check{color:#16a34a}"),
    (".check{color: #99aaff}",   ".check{color:#16a34a}"),

    # ── blog/prybyrannia: dark stage/price-table/checklist ───────────────
    (".stage-card{background:#07091e;",  ".stage-card{background:#ffffff;"),
    (".price-table{",  ".price-table-SKIP{"),  # handle separately below
    ("background:#07091e;border:1px solid #151840", "background:#ffffff;border:1px solid #e5e7eb"),
    (".price-table th{background:#0d1030;",  ".price-table th{background:#f1f5f9;"),
    ("border-top:1px solid #151840",         "border-top:1px solid #e5e7eb"),
    (".checklist{background:#07091e;",       ".checklist{background:#f8fafc;"),

    # ── index.html: blue gradient-bg → green ────────────────────────────
    ("radial-gradient(ellipse 70% 50% at top right, rgba(102,128,255,0.18), transparent)",
     "radial-gradient(ellipse 70% 50% at top right, rgba(34,197,94,0.08), transparent)"),
    ("radial-gradient(ellipse 60% 40% at bottom left, rgba(102,128,255,0.08), transparent)",
     "radial-gradient(ellipse 60% 40% at bottom left, rgba(34,197,94,0.05), transparent)"),

    # ── faq.html: blue sidebar/links ────────────────────────────────────
    ("rgba(102,128,255,0.08)}",   "rgba(34,197,94,0.08)}"),
    ("color:#99aaff;border-left-color:#99aaff;background:rgba(102,128,255,0.1)",
     "color:#16a34a;border-left-color:#16a34a;background:rgba(34,197,94,0.1)"),
    ("rgba(102,128,255,0.12)",    "rgba(34,197,94,0.12)"),

    # ── ALL pages: orb gradient blue fallback → green ────────────────────
    ("rgba(34,197,94,0.12),rgba(51,85,255,0) 70%)",
     "rgba(34,197,94,0.12),rgba(34,197,94,0) 70%)"),
    ("rgba(34,197,94,0.08),rgba(100,51,255,0) 70%)",
     "rgba(34,197,94,0.08),rgba(34,197,94,0) 70%)"),
    ("rgba(34,197,94,0.18),rgba(51,85,255,0) 70%)",
     "rgba(34,197,94,0.18),rgba(34,197,94,0) 70%)"),
    ("rgba(34,197,94,0.10),rgba(34,197,94,0) 70%)",
     "rgba(34,197,94,0.10),rgba(34,197,94,0) 70%)"),

    # ── prices.html table header dark ───────────────────────────────────
    (".price-table-SKIP{",  ".price-table{"),  # undo skip
]

total = 0
for path in glob.glob(BASE + "/**/*.html", recursive=True):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    new = html
    for old, new_val in FIXES:
        new = new.replace(old, new_val)
    if new != html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        total += 1
        print(f"FIXED: {os.path.relpath(path, BASE)}")

print(f"\nDone — {total} files fixed.")
