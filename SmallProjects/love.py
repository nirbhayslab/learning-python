import math as m
import random as r
import time
import tkinter as tk
import tkinter.font as tkf

# ─────────────────────────── WINDOW & DISPLAY ───────────────────────────
root = tk.Tk()
root.title("I Love You — 85+ Languages Kinetic Heart")
BG = "#040108"
root.configure(bg=BG)

# Auto-scale to ~90% of screen height for a massive viewport
SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()
H = int(SH * 0.88)
W = int(min(SW * 0.92, H * 1.15))
root.geometry(f"{W}x{H}+{(SW - W) // 2}+{(SH - H) // 2}")

cv = tk.Canvas(
    root, width=W, height=H, bg=BG, highlightthickness=0,
    scrollregion=(-W // 2, -H // 2, W // 2, H // 2)
)
cv.pack(fill="both", expand=True)

is_fullscreen = False
def toggle_fullscreen(_event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(_event=None):
    global is_fullscreen
    if is_fullscreen:
        is_fullscreen = False
        root.attributes("-fullscreen", False)

def on_resize(event):
    if event.width > 100 and event.height > 100:
        cv.configure(scrollregion=(-event.width // 2, -event.height // 2,
                                   event.width // 2, event.height // 2))

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)
cv.bind("<Configure>", on_resize)

# ─────────────────────────── 85+ LANGUAGES CORPUS ───────────────────────
PHRASES = [
    # South Asian / Indian Scripts
    "मैं तुमसे प्यार करता हूँ", "त्वयि स्निह्यामि", "আমি তোমাকে ভালোবাসি",
    "நான் உன்னை காதலிக்கிறேன்", "నేను నిన్ను ప్రేమిస్తున్నాను", "मी तुझ्यावर प्रेम करतो",
    "હું તને પ્રેમ કરું છું", "ਮੈਂ ਤੈਨੂੰ ਪਿਆਰ ਕਰਦਾ ਹਾਂ", "ನಾನು ನಿನ್ನನ್ನು ಪ್ರೀತಿಸುತ್ತೇನೆ",
    "ഞാൻ നിന്നെ സ്നേഹിക്കുന്നു", "میں تم سے محبت کرتا ہوں", "म तिमीलाई माया गर्छु",
    "මම ඔයාට ආදරෙයි", "मूँ तव्हां खे प्यार थो करियां",
    # East & Southeast Asian
    "我爱你", "我愛你", "愛してる", "大好きだよ", "사랑해", "사랑해요",
    "ฉันรักเธอ", "รักนะ", "Anh yêu em", "Em yêu anh", "Aku cinta kamu",
    "Saya cinta padamu", "Mahal kita", "ချစ်တယ်", "ខ្ញុំស្រឡាញ់អ្នក",
    "ຂ້ອຍຮັກເຈົ້າ", "Би чамд хайртай",
    # European (Romance, Germanic, Slavic, Celtic, Finno-Ugric, Baltic, Hellenic)
    "I love you", "Te amo", "Te quiero", "Je t'aime", "Ti amo",
    "Eu te amo", "Amo-te", "Ich liebe dich", "Ik hou van jou",
    "Jag älskar dig", "Jeg elsker deg", "Jeg elsker dig", "Ég elska þig",
    "Minä rakastan sinua", "Rakastan sinua", "Ma armastan sind", "Szeretlek",
    "Kocham cię", "Miluji tě", "Ľúbim ťa", "Я тебя люблю",
    "Я тебе кохаю", "Кохаю тебе", "Я цябе кахаю", "Обичам те",
    "Волим те", "Volim te", "Ljubim te", "Те сакам", "Σ' αγαπώ",
    "Te iubesc", "Të dua", "Myliu tave", "Es tevi mīlu",
    "Gráím thú", "Tha gaol agam ort", "Rwy'n dy garu di", "Maite zaitut",
    "T'estimo", "Quérote", "Mi amas vin",
    # Middle Eastern, Caucasian & Central Asian
    "Seni seviyorum", "Səni sevirəm", "Men seni sevaman", "Мен сені сүйемін",
    "أحبك", "أنا أحبك", "دوستت دارم", "عاشقتم", "אני אוהב אותך",
    "მიყვარხარ", "Ես քեզ սիրում եմ", "Սիրում եմ քեզ", "Ez ji te hez dikim",
    # African & Oceanic
    "Nakupenda", "Ngiyakuthanda", "Ndiyakuthanda", "Mo nifẹ rẹ",
    "Ahụrụ m gị n'anya", "Ina son ku", "እወድሻለሁ", "Waan ku jeclahay",
    "Ek het jou lief", "Tiako ianao", "Aloha Au Ia 'Oe", "Aroha ahau ki a koe",
]

# Naturally compact "I love you" sentences/verbs for tight lobe & tip geometry
COMPACT_PHRASES = [
    "我爱你", "사랑해", "愛してる", "أحبك", "รักนะ", "Te amo", "Ti amo",
    "Të dua", "Amo-te", "Gráím thú", "Quérote", "T'estimo", "Волим те",
    "Volim te", "Ljubim te", "Σ' αγαπώ", "Szeretlek", "მიყვარხარ",
    "Nakupenda", "Mahal kita", "Кохаю тебе", "I love you", "Je t'aime",
]

# ─────────────────────────── CONFIGURATION ──────────────────────────────
SC = min(W, H) / 34.5
OY = -min(W, H) * 0.025
BUILD_DURATION = 6.8
TICK = 16
ANIM_FRAMES = 34
FONT = "Arial"

CORE_SIZES = (13, 14, 15, 16)
BODY_SIZES = (9, 10, 11, 12)
MICRO_SIZES = (8, 7, 6, 5)
ALL_SIZES = CORE_SIZES + BODY_SIZES + MICRO_SIZES

PALETTE = [
    (0.32, 0.02, 0.16),  # Deep velvet core
    (0.68, 0.02, 0.16),  # Rich ruby
    (0.95, 0.06, 0.20),  # Electric crimson
    (1.00, 0.24, 0.40),  # Neon rose
    (1.00, 0.55, 0.68),  # Warm coral pink
    (1.00, 0.86, 0.90),  # Specular blush rim
]
FLASH = (1.0, 0.95, 0.90)
GOLD_FLASH = (1.0, 0.88, 0.72)
BGC = tuple(int(BG[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
rng = r.Random(11)

# ─────────────────────────── MATH & COLOR UTILS ─────────────────────────
def clamp(v, lo=0.0, hi=1.0):
    return lo if v < lo else (hi if v > hi else v)

def hx(c):
    return "#%02x%02x%02x" % (
        int(clamp(c[0]) * 255),
        int(clamp(c[1]) * 255),
        int(clamp(c[2]) * 255),
    )

def mix(a, b, k):
    k = clamp(k)
    return (
        a[0] + (b[0] - a[0]) * k,
        a[1] + (b[1] - a[1]) * k,
        a[2] + (b[2] - a[2]) * k,
    )

def sample_palette(t):
    t = clamp(t) * (len(PALETTE) - 1)
    idx = int(t)
    if idx >= len(PALETTE) - 1:
        return PALETTE[-1]
    return mix(PALETTE[idx], PALETTE[idx + 1], t - idx)

def ease_out_back(u):
    s = 1.18
    u1 = u - 1.0
    return 1.0 + u1 * u1 * ((s + 1.0) * u1 + s)

# ─────────────────────────── O(1) FONT CACHE & GEOMETRY ─────────────────
_fonts = {}
_width_cache = {}

def font_for(size):
    if size not in _fonts:
        _fonts[size] = tkf.Font(root=cv, family=FONT, size=size, weight="bold")
    return _fonts[size]

def measure_text(text, size):
    key = (text, size)
    if key not in _width_cache:
        _width_cache[key] = font_for(size).measure(text)
    return _width_cache[key]

for _s in ALL_SIZES:
    font_for(_s)

def heart(a):
    x = 16.0 * (m.sin(a) ** 3)
    y = (
        13.0 * m.cos(a)
        - 5.0 * m.cos(2.0 * a)
        - 2.0 * m.cos(3.0 * a)
        - m.cos(4.0 * a)
    )
    return x * SC, -y * SC + OY

POLY = [heart(m.tau * i / 1000) for i in range(1000)]
EDGES = list(zip(POLY, POLY[1:] + POLY[:1]))
YMIN = min(p[1] for p in POLY)
YMAX = max(p[1] for p in POLY)
CY = (YMAX + YMIN) / 2.0

def spans(y):
    xs = []
    for (x1, y1), (x2, y2) in EDGES:
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return list(zip(xs[0::2], xs[1::2]))

def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 10:
                out.append((lo, hi))
    return out

def norm_dist(x, y):
    return m.hypot(x / (16.0 * SC), (y - CY) / (14.5 * SC))

def phrase_cycle():
    while True:
        order = PHRASES[:]
        rng.shuffle(order)
        yield from order

# ─────────────────────────── BACKGROUND & RIM HALO ──────────────────────
def draw_ambient_field():
    steps = 26
    glow_col = (0.16, 0.01, 0.08)
    max_rx = 18.5 * SC
    max_ry = 17.0 * SC
    for i in range(steps, 0, -1):
        k = i / steps
        rx = max_rx * k
        ry = max_ry * k
        col = hx(mix(BGC, glow_col, (1.0 - k) ** 1.9))
        cv.create_oval(-rx, CY - ry, rx, CY + ry, fill=col, outline="")

RIM_NODES = []
def init_rim_halo(count=220):
    for i in range(count):
        ang = m.tau * i / count
        bx, by = heart(ang)
        r_sz = rng.uniform(1.2, 2.5)
        col = sample_palette(rng.uniform(0.65, 1.0))
        cid = cv.create_oval(bx - r_sz, by - r_sz, bx + r_sz, by + r_sz,
                             fill=hx(mix(BGC, col, 0.25)), outline="")
        RIM_NODES.append({
            "id": cid, "ang": ang, "r": r_sz,
            "speed": rng.uniform(0.12, 0.28),
            "phase": rng.uniform(0, m.tau),
            "col": col
        })

def update_rim_halo(t_sec, pulse):
    for node in RIM_NODES:
        a = node["ang"] + t_sec * node["speed"]
        bx, by = heart(a)
        nx = bx / (16.0 * SC + 0.001)
        ny = (by - CY) / (14.5 * SC + 0.001)
        disp = pulse * 6.0 + m.sin(t_sec * 3.0 + node["phase"]) * 2.5
        px = bx + nx * disp
        py = by + ny * disp
        r_sz = node["r"] * (1.0 + 0.35 * pulse)
        alpha = clamp(0.28 + 0.45 * pulse + 0.2 * m.sin(t_sec * 4.0 + node["phase"]))
        cv.coords(node["id"], px - r_sz, py - r_sz, px + r_sz, py + r_sz)
        cv.itemconfig(node["id"], fill=hx(mix(BGC, node["col"], alpha)))

# ─────────────────────────── POLYGLOT SCANLINE SOLVER ───────────────────
def build():
    cycle = phrase_cycle()
    row_h = font_for(11).metrics("linespace") + 2
    half = row_h / 2.0
    placed = []
    y = YMIN + half * 0.55

    while y < YMAX - half * 0.35:
        band = half * 0.42 if abs(y - CY) > 11.2 * SC else half * 0.82
        row = intersect(spans(y - band), spans(y + band))
        for lo, hi in row:
            lo += 2.0
            hi -= 2.0
            if hi - lo < 12.0:
                continue

            cur = lo
            line = []
            while True:
                rem_span = hi - cur
                if rem_span < 12.0:
                    break

                mid_x = cur + min(rem_span * 0.5, 45.0)
                r_est = norm_dist(mid_x, y)
                size_pool = CORE_SIZES + BODY_SIZES if r_est < 0.46 else BODY_SIZES

                fit = None
                # 1. Try full-diversity polyglot cycle first
                for _ in range(14):
                    text = next(cycle)
                    s_try = rng.choice(size_pool)
                    w = measure_text(text, s_try)
                    if w <= rem_span:
                        fit = (text, s_try, w)
                        break

                # 2. Fallback: compact conjugated "I love you" phrases for narrow edges/tips
                if fit is None:
                    for _ in range(12):
                        text = rng.choice(COMPACT_PHRASES)
                        s_try = rng.choice(BODY_SIZES + MICRO_SIZES)
                        w = measure_text(text, s_try)
                        if w <= rem_span:
                            fit = (text, s_try, w)
                            break

                # 3. Micro-vertex lock for the razor-sharp bottom point
                if fit is None:
                    for s_try in MICRO_SIZES:
                        for text in ("我爱你", "사랑해", "أحبك", "Te amo", "Ti amo"):
                            w = measure_text(text, s_try)
                            if w <= rem_span:
                                fit = (text, s_try, w)
                                break
                        if fit is not None:
                            break

                if fit is None:
                    break

                text, fit_size, w = fit
                gap = 6.0 if fit_size >= 11 else 4.0
                line.append([cur + w / 2.0, text, fit_size, w])
                cur += w + gap

            if not line:
                continue

            if len(line) > 1:
                slack = hi - (line[-1][0] + line[-1][3] / 2.0)
                for i, it in enumerate(line):
                    it[0] += slack * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2.0

            for i, (x, text, size, w) in enumerate(line):
                edge = (i == 0) or (i == len(line) - 1)
                placed.append(dict(x=x, y=y, text=text, size=size, edge=edge))

        y += row_h

    for p in placed:
        dx = p["x"]
        dy = p["y"] - CY
        rad = min(1.0, norm_dist(dx, p["y"]))
        ang = m.atan2(dy, dx)
        z_bulge = m.sqrt(max(0.0, 1.0 - rad * rad))

        t_col = (rad ** 1.1) * 0.76 + (0.22 if p["edge"] else 0.0) + rng.uniform(-0.06, 0.07)
        p["color"] = sample_palette(t_col)
        p["rad"] = rad
        p["z"] = z_bulge
        p["ang"] = ang
        p["nx"] = m.cos(ang)
        p["ny"] = m.sin(ang)

    edges = [p for p in placed if p["edge"]]
    inner = [p for p in placed if not p["edge"]]
    edges.sort(key=lambda p: (m.atan2(p["x"], -(p["y"] - CY)) % m.tau))
    inner.sort(key=lambda p: -p["rad"] + rng.uniform(-0.04, 0.04))
    return edges + inner

# ─────────────────────────── INTERACTIVE STATE ──────────────────────────
draw_ambient_field()
init_rim_halo()

ORDER = build()
items = iter(ORDER)
RATE = len(ORDER) / (BUILD_DURATION * 1000.0 / TICK)
acc = 0.0
spawning = True
active = []
settled = []
shockwaves = []
start_time = time.perf_counter()

mouse_pos = [9999.0, 9999.0]
def to_canvas_coords(event):
    return event.x - cv.winfo_width() / 2.0, event.y - cv.winfo_height() / 2.0

def on_mouse_move(event):
    mouse_pos[0], mouse_pos[1] = to_canvas_coords(event)

def on_mouse_leave(_event):
    mouse_pos[0], mouse_pos[1] = 9999.0, 9999.0

def on_click(event):
    cx, cy = to_canvas_coords(event)
    shockwaves.append({"x": cx, "y": cy, "r": 0.0, "max_r": min(W, H) * 0.75})

cv.bind("<Motion>", on_mouse_move)
cv.bind("<Leave>", on_mouse_leave)
cv.bind("<Button-1>", on_click)

# ─────────────────────────── ANIMATION PIPELINE ─────────────────────────
def spawn(p):
    x, y = p["x"], p["y"]
    size, text, c = p["size"], p["text"], p["color"]
    font = (FONT, size, "bold")

    dist_offset = (55.0 + 35.0 * p["rad"]) * (SC / 22.0)
    tangent_angle = p["ang"] + 0.65
    ox = m.cos(tangent_angle) * dist_offset
    oy = m.sin(tangent_angle) * dist_offset

    shadow = cv.create_text(x + ox + 2, y + oy + 3, text=text, font=font, fill=BG)
    main = cv.create_text(x + ox, y + oy, text=text, font=font, fill=BG)

    p.update(shadow=shadow, main=main, f=0, ox=ox, oy=oy, shimmer=0.0)
    active.append(p)

def animate_spawn(p):
    p["f"] += 1
    u = clamp(p["f"] / ANIM_FRAMES)
    e = ease_out_back(u)
    alpha = clamp(u * 1.4) ** 1.35

    c = p["color"]
    x, y = p["x"], p["y"]
    px = x + p["ox"] * (1.0 - e)
    py = y + p["oy"] * (1.0 - e)

    flash = 0.75 * m.sin(m.pi * clamp((u - 0.45) / 0.55))
    col = mix(mix(BGC, c, alpha), FLASH, flash)
    sh_col = mix(BGC, (c[0] * 0.25, c[1] * 0.12, c[2] * 0.20), alpha)

    cv.coords(p["shadow"], px + 2, py + 3)
    cv.itemconfig(p["shadow"], fill=hx(sh_col))
    cv.coords(p["main"], px, py)
    cv.itemconfig(p["main"], fill=hx(col))

    if u >= 1.0:
        cv.coords(p["shadow"], x + 2, y + 3)
        cv.coords(p["main"], x, y)
        cv.itemconfig(p["main"], fill=hx(c))
        settled.append(p)
        return False
    return True

def heartbeat_wave(t_sec):
    cycle = (t_sec % 0.86) / 0.86
    lub = m.exp(-(((cycle - 0.14) / 0.045) ** 2))
    dub = 0.60 * m.exp(-(((cycle - 0.31) / 0.060) ** 2))
    return lub + dub, cycle

def step():
    global spawning, acc
    now = time.perf_counter() - start_time
    pulse, cycle = heartbeat_wave(now)
    update_rim_halo(now, pulse)

    if spawning:
        acc += RATE
        try:
            while acc >= 1.0:
                acc -= 1.0
                spawn(next(items))
        except StopIteration:
            spawning = False

    if active:
        active[:] = [p for p in active if animate_spawn(p)]

    for sw in shockwaves:
        sw["r"] += 18.0
    shockwaves[:] = [sw for sw in shockwaves if sw["r"] < sw["max_r"]]

    if settled:
        if rng.random() < 0.45:
            rng.choice(settled)["shimmer"] = 0.80

        mx, my = mouse_pos[0], mouse_pos[1]
        repulse_rad = 115.0 * (SC / 22.0)
        repulse_sq = repulse_rad * repulse_rad

        for p in settled:
            rad = p["rad"]
            z = p["z"]
            local_wave = m.exp(-(((cycle - 0.14 - rad * 0.19) / 0.085) ** 2))
            disp = (pulse * 6.5 * (0.35 + 0.65 * rad) + local_wave * 4.5) * (SC / 22.0)

            px = p["x"] + p["nx"] * disp
            py = p["y"] + p["ny"] * disp - (pulse * z * 4.0)

            mdx = px - mx
            mdy = py - my
            mdist_sq = mdx * mdx + mdy * mdy
            cursor_glow = 0.0
            if mdist_sq < repulse_sq:
                mdist = m.sqrt(mdist_sq) + 0.001
                falloff = (1.0 - mdist / repulse_rad) ** 2
                push = falloff * 18.0 * (SC / 22.0)
                px += (mdx / mdist) * push
                py += (mdy / mdist) * push
                cursor_glow = falloff * 0.80

            sw_glow = 0.0
            for sw in shockwaves:
                sdx = px - sw["x"]
                sdy = py - sw["y"]
                sdist = m.hypot(sdx, sdy) + 0.001
                band_diff = abs(sdist - sw["r"])
                if band_diff < 48.0:
                    fade = 1.0 - (sw["r"] / sw["max_r"])
                    w_strength = ((1.0 - band_diff / 48.0) ** 2) * fade
                    px += (sdx / sdist) * w_strength * 16.0
                    py += (sdy / sdist) * w_strength * 16.0
                    sw_glow = max(sw_glow, w_strength * 0.95)

            if p["shimmer"] > 0.01:
                p["shimmer"] *= 0.88
            else:
                p["shimmer"] = 0.0

            glow = clamp(local_wave * 0.42 + p["shimmer"] + cursor_glow + sw_glow)
            target_flash = GOLD_FLASH if sw_glow > 0.2 else FLASH
            col = mix(p["color"], target_flash, glow)

            cv.coords(p["main"], px, py)
            cv.coords(p["shadow"], px + 2, py + 3)
            cv.itemconfig(p["main"], fill=hx(col))

    cv.after(TICK, step)

try:
    cv.after(120, step)
    root.mainloop()
except Exception:
    pass
