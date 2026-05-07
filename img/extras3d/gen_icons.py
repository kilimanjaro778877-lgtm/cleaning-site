from PIL import Image, ImageDraw, ImageFilter
import math

PY = "C:\\Users\\Admin\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"

SIZE = 256
BG = (245, 248, 255)       # near-white blue-tint bg
ACCENT = (100, 160, 230)   # pastel blue
ACCENT2 = (70, 130, 200)   # darker blue
SHADOW = (180, 200, 220)   # shadow color
WHITE = (255, 255, 255)
LIGHT = (210, 230, 250)    # light face

def new_img():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)
    return img, d

def isometric_box(d, cx, cy, w, h, depth,
                  top_color=LIGHT, front_color=ACCENT, side_color=ACCENT2):
    """Draw a simple isometric box centered at (cx, cy)."""
    hw = w // 2
    hh = h // 2
    # Top face (parallelogram)
    top = [
        (cx, cy - hh - depth),
        (cx + hw, cy - depth),
        (cx, cy + depth // 2 - depth + 10),  # roughly
        (cx - hw, cy - depth),
    ]
    # Simpler: just use flat top
    top = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw + depth, cy - hh - depth),
        (cx - hw + depth, cy - hh - depth),
    ]
    front = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw, cy + hh),
        (cx - hw, cy + hh),
    ]
    right = [
        (cx + hw, cy - hh),
        (cx + hw + depth, cy - hh - depth),
        (cx + hw + depth, cy + hh - depth),
        (cx + hw, cy + hh),
    ]
    d.polygon(top, fill=top_color)
    d.polygon(front, fill=front_color)
    d.polygon(right, fill=side_color)
    # Outline
    for poly in [top, front, right]:
        d.polygon(poly, outline=WHITE)

def rounded_rect(d, x0, y0, x1, y1, r, fill, outline=None):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline)

def save(img, name):
    path = f"C:\\Users\\Admin\\cleaning-site\\img\\extras3d\\{name}.jpg"
    img = img.filter(ImageFilter.SMOOTH)
    img.save(path, "JPEG", quality=92)
    print(f"Saved {name}.jpg")

# === VYTIAZHKA (range hood) ===
def make_vytiazhka():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2
    # Hood body - trapezoid
    d.polygon([(cx-70, cy-20), (cx+70, cy-20), (cx+50, cy+40), (cx-50, cy+40)],
              fill=ACCENT, outline=WHITE)
    # Top box
    rounded_rect(d, cx-60, cy-70, cx+60, cy-20, 8, LIGHT, WHITE)
    # Vent lines
    for i in range(3):
        x = cx - 30 + i * 30
        d.line([(x, cy+5), (x, cy+35)], fill=WHITE, width=3)
    # Isometric depth on top box
    d.polygon([(cx+60, cy-70), (cx+75, cy-85), (cx+75, cy-35), (cx+60, cy-20)],
              fill=ACCENT2, outline=WHITE)
    save(img, "vytiazhka")

# === SHAFKY (cabinet interior) ===
def make_shafky():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2
    # Cabinet box
    isometric_box(d, cx, cy+10, 110, 100, 30)
    # Shelf line
    d.line([(cx-55, cy+10), (cx+55, cy+10)], fill=WHITE, width=3)
    # Handle dot front
    d.ellipse([(cx+15, cy+30), (cx+25, cy+40)], fill=WHITE)
    d.ellipse([(cx+15, cy-10), (cx+25, cy)], fill=WHITE)
    # Items on shelf (small boxes)
    rounded_rect(d, cx-45, cy-40, cx-25, cy-12, 3, WHITE)
    rounded_rect(d, cx-20, cy-42, cx-5, cy-12, 3, LIGHT)
    save(img, "shafky")

# === DUSHOVA (shower cabin) ===
def make_dushova():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2
    # Cabin walls - box
    isometric_box(d, cx, cy+10, 100, 110, 25, top_color=LIGHT, front_color=(180,210,240), side_color=ACCENT2)
    # Glass door - lighter
    rounded_rect(d, cx-48, cy-45, cx+5, cy+55, 5, (200,225,250,180), WHITE)
    # Shower head
    d.ellipse([(cx+10, cy-55), (cx+35, cy-30)], fill=ACCENT2, outline=WHITE)
    # Water drops
    for dx, dy in [(-20, -15), (-5, 0), (-30, 10)]:
        d.ellipse([(cx+dx, cy+dy), (cx+dx+8, cy+dy+12)], fill=(150,190,240))
    save(img, "dushova")

# === PLYTKA (tiles) ===
def make_plytka():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2
    # Draw tile grid
    tile_size = 38
    grout = 4
    for row in range(4):
        for col in range(4):
            x0 = cx - 80 + col * (tile_size + grout)
            y0 = cy - 80 + row * (tile_size + grout)
            x1 = x0 + tile_size
            y1 = y0 + tile_size
            rounded_rect(d, x0, y0, x1, y1, 3, LIGHT, WHITE)
    # Cleaning brush
    d.rectangle([(cx+30, cy-30), (cx+55, cy+30)], fill=ACCENT, outline=WHITE)
    d.ellipse([(cx+25, cy+25), (cx+60, cy+50)], fill=ACCENT2, outline=WHITE)
    save(img, "plytka")

# === BALKON (balcony) ===
def make_balkon():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2 + 10
    # Floor isometric
    floor = [(cx-80, cy+20), (cx+80, cy+20), (cx+110, cy-10), (cx-50, cy-10)]
    d.polygon(floor, fill=LIGHT, outline=WHITE)
    # Railing posts
    for x in range(cx-70, cx+80, 30):
        d.rectangle([(x, cy-60), (x+6, cy+20)], fill=ACCENT, outline=WHITE)
    # Railing top bar
    d.rectangle([(cx-70, cy-64), (cx+82, cy-56)], fill=ACCENT2, outline=WHITE)
    # Wall behind
    d.rectangle([(cx-80, cy-90), (cx+80, cy-60)], fill=SHADOW, outline=WHITE)
    save(img, "balkon")

# === GARDEROBNA (wardrobe) ===
def make_garderobna():
    img, d = new_img()
    cx, cy = SIZE//2, SIZE//2
    # Wardrobe box
    isometric_box(d, cx, cy+5, 120, 115, 30)
    # Door division line
    d.line([(cx, cy-53), (cx, cy+53)], fill=WHITE, width=3)
    # Left door handle
    d.ellipse([(cx-18, cy-3), (cx-8, cy+7)], fill=WHITE)
    # Right door handle
    d.ellipse([(cx+8, cy-3), (cx+18, cy+7)], fill=WHITE)
    # Hanging clothes hint (arcs)
    for ox in [-25, 0, 20]:
        d.arc([(cx-45+ox, cy-40), (cx-25+ox, cy-20)], 0, 180, fill=WHITE, width=2)
    save(img, "garderobna")

make_vytiazhka()
make_shafky()
make_dushova()
make_plytka()
make_balkon()
make_garderobna()
print("All 6 icons generated!")
