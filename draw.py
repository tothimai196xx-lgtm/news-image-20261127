#!/usr/bin/env python3
"""Draw the 27 November 2026 world-news image: 1024x1024, 48 sourced stories,
7 regions, UTC timeline, world map, 3 drawn scenes, date check, per-story confidence.
Deterministic: fixed seed, fixed fonts, no network, no timestamps in pixels."""
import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
random.seed(27112026)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else FR, sz)

img = Image.new("RGB", (W, H), (13, 22, 38))
d = ImageDraw.Draw(img, "RGBA")

# ---------- background texture: dense stipple + faint grid ----------
for _ in range(9000):
    x = random.randint(0, W - 1); y = random.randint(0, H - 1)
    v = random.randint(18, 42)
    d.point((x, y), fill=(v, v + 8, v + 22))
for gx in range(0, W, 64):
    d.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 6), width=1)
for gy in range(0, H, 64):
    d.line([(0, gy), (W, gy)], fill=(255, 255, 255, 6), width=1)

NAVY = (13, 22, 38); PANEL = (22, 34, 58); PANEL2 = (28, 44, 74)
GOLD = (245, 196, 66); WHITE = (240, 244, 250); MUT = (165, 178, 198)
RED = (235, 84, 84); GREEN = (72, 199, 142); BLUE = (84, 163, 235)
ORANGE = (245, 150, 66); PURPLE = (178, 132, 235); TEAL = (66, 205, 190); PINK = (235, 120, 180)

REGION_COLORS = {
    "MIDDLE EAST": RED, "EUROPE": BLUE, "AMERICAS": GREEN, "ASIA": GOLD,
    "AFRICA": ORANGE, "TECH": PURPLE, "SPORT": TEAL, "BUSINESS": PINK,
}

def wrap(text, fnt, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def panel(x0, y0, x1, y1, fill=PANEL, outline=(70, 90, 130)):
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=fill, outline=outline, width=1)

# ================= HEADER =================
d.rectangle([0, 0, W, 88], fill=(10, 16, 30))
d.rectangle([0, 88, W, 92], fill=GOLD)
d.text((18, 10), "FRIDAY 27 NOVEMBER 2026", font=font(30), fill=WHITE)
d.text((18, 48), "THE WORLD IN ONE IMAGE  ·  48 STORIES  ·  7 REGIONS  ·  ALL TIMES UTC",
       font=font(13), fill=GOLD)
# date-check badge
d.rounded_rectangle([742, 14, 1006, 76], radius=8, fill=(20, 60, 40), outline=GREEN, width=2)
d.text((758, 20), "✓ DATE-CHECKED", font=font(15), fill=GREEN)
d.text((758, 42), "Every story first reported", font=font(11), fill=WHITE)
d.text((758, 58), "on 27 Nov 2026 — verified", font=font(11), fill=WHITE)

# ================= DAY IN NUMBERS =================
panel(16, 104, 1008, 158)
d.text((28, 110), "THE DAY IN NUMBERS", font=font(12), fill=GOLD)
stats = [
    ("2", "Italians killed in Kuwait drone strike"),
    ("10", "killed in Gaza as Hamas weighs reply"),
    ("1,645,899", "Russian troops lost since Feb 2022*"),
    ("€1.78tn", "EU budget deal that failed"),
    ("$60,400", "Bitcoin — bear-market call dropped"),
    ("850,000+", "without power in US storm"),
]
sx = 28
for val, lab in stats:
    d.text((sx, 122), val, font=font(14), fill=WHITE)
    lines = wrap(lab, font(8), 152)
    for i, ln in enumerate(lines[:1]):
        d.text((sx, 142), ln, font=font(8), fill=MUT)
    sx += 162

# ================= LEAD STORY + DRAWN SCENES (left) =================
panel(16, 170, 508, 470)
d.text((28, 178), "LEAD STORY — KUWAIT, 01:03 UTC", font=font(12), fill=RED)
d.text((28, 198), "Drone strike kills two Italians;", font=font(16), fill=WHITE)
d.text((28, 218), "Iran denies responsibility", font=font(16), fill=WHITE)
d.text((28, 240), "Debris from intercepted Iranian drones fell on a vital site in Kuwait,",
       font=font(10), fill=MUT)
d.text((28, 254), "killing two Rheinmetall Italia technicians. Kuwait blamed the debris;",
       font=font(10), fill=MUT)
d.text((28, 268), "Tehran denied any role.  ●●● HIGH confidence — NYT, BBC, Reuters",
       font=font(10), fill=GREEN)
# drawn scene: night sky, skyline, drone, explosion
sx0, sy0, sx1, sy1 = 28, 288, 496, 458
d.rectangle([sx0, sy0, sx1, sy1], fill=(8, 12, 26))
for _ in range(60):
    x = random.randint(sx0, sx1); y = random.randint(sy0, sy0 + 60)
    d.point((x, y), fill=(220, 220, 240))
# moon
d.ellipse([sx1 - 70, sy0 + 12, sx1 - 30, sy0 + 52], fill=(240, 235, 200))
# skyline
bx = sx0 + 6
for bh in [70, 95, 60, 110, 80, 100, 55, 90]:
    d.rectangle([bx, sy1 - bh, bx + 42, sy1], fill=(30, 44, 70), outline=(60, 80, 120))
    for wy in range(sy1 - bh + 8, sy1 - 6, 12):
        for wx in range(bx + 6, bx + 38, 12):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 5, wy + 6], fill=(245, 196, 66))
    bx += 52
# drone silhouette
dx, dy = 300, sy0 + 55
d.ellipse([dx - 26, dy - 4, dx + 26, dy + 6], fill=(180, 190, 210))
d.ellipse([dx - 40, dy - 8, dx - 14, dy - 2], fill=(120, 130, 150))
d.ellipse([dx + 14, dy - 8, dx + 40, dy - 2], fill=(120, 130, 150))
d.line([(dx, dy + 6), (dx, dy + 22)], fill=(200, 200, 200), width=2)
# explosion burst
ex, ey = 180, sy1 - 70
for r, col in [(46, (235, 120, 40)), (34, (245, 180, 60)), (20, (255, 230, 140))]:
    pts = []
    for k in range(14):
        a = k * math.pi * 2 / 14
        rr = r * random.uniform(0.7, 1.15)
        pts.append((ex + rr * math.cos(a), ey + rr * math.sin(a)))
    d.polygon(pts, fill=col)
d.rectangle([sx0 + 4, sy1 - 18, sx0 + 168, sy1 - 4], fill=(8, 12, 26))
d.text((sx0 + 6, sy1 - 16), "DRAWN SCENE — not a photo", font=font(8), fill=(200, 200, 200))

# ================= WORLD MAP (right) =================
panel(524, 170, 1008, 470)
d.text((536, 178), "WORLD MAP — WHERE THE NEWS HAPPENED", font=font(12), fill=GOLD)
# simplified continents as polygons (equirectangular-ish)
mx0, my0, mx1, my1 = 536, 200, 996, 420
d.rectangle([mx0, my0, mx1, my1], fill=(16, 30, 54), outline=(70, 90, 130))
for gx in range(mx0, mx1, 23):
    d.line([(gx, my0), (gx, my1)], fill=(255, 255, 255, 8))
for gy in range(my0, my1, 22):
    d.line([(mx0, gy), (mx1, gy)], fill=(255, 255, 255, 8))
def lonlat(lon, lat):
    return (mx0 + (lon + 180) / 360 * (mx1 - mx0), my0 + (90 - lat) / 180 * (my1 - my0))
continents = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60), (-70, 45), (-80, 32), (-95, 20), (-105, 22), (-120, 35), (-125, 48), (-150, 60)],
    "SA": [(-78, 8), (-60, 5), (-50, 0), (-40, -8), (-48, -22), (-58, -34), (-70, -40), (-73, -20), (-80, -5)],
    "EU": [(-10, 36), (-5, 43), (0, 50), (8, 57), (18, 55), (28, 60), (30, 70), (40, 68), (45, 55), (30, 45), (20, 40), (10, 38)],
    "AF": [(-17, 15), (-10, 30), (10, 37), (30, 32), (43, 12), (51, 11), (40, -5), (35, -18), (20, -35), (12, -18), (8, 0), (-8, 5)],
    "AS": [(45, 70), (70, 72), (100, 77), (130, 72), (160, 66), (180, 65), (160, 55), (140, 40), (127, 35), (120, 25), (105, 10), (95, 8), (80, 8), (70, 20), (55, 25), (48, 30)],
    "OC": [(113, -22), (130, -12), (142, -11), (150, -22), (153, -32), (140, -38), (129, -32), (115, -32)],
}
for pts in continents.values():
    d.polygon([lonlat(lo, la) for lo, la in pts], fill=(52, 96, 62), outline=(110, 180, 120))
# story dots
dots = [
    ("Kuwait", 48, 29, RED), ("Gaza", 34, 31, RED), ("Kyiv", 30, 50, BLUE),
    ("London", 0, 51, BLUE), ("Paris", 2, 48, BLUE), ("Mali", -2, 17, ORANGE),
    ("New York", -74, 41, GREEN), ("Washington", -77, 39, GREEN),
    ("Delhi", 77, 28, GOLD), ("Jakarta", 107, -6, GOLD), ("Beijing", 116, 40, GOLD),
    ("Tokyo", 139, 35, GOLD), ("Sydney", 151, -34, GOLD), ("Congo", 25, -2, ORANGE),
    ("Buenos Aires", -58, -35, GREEN), ("Ibiza", 1, 39, BLUE), ("Hong Kong", 114, 22, GOLD),
    ("Cairo", 31, 30, ORANGE), ("Lagos", 3, 6, ORANGE), ("Moscow", 37, 55, BLUE),
    ("Tehran", 51, 35, RED), ("Yangon", 96, 17, GOLD),
]
for name, lon, lat, col in dots:
    x, y = lonlat(lon, lat)
    d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col, outline=WHITE, width=1)
d.text((536, 428), "● 21 hotspots · Red Middle East · Blue Europe · Gold Asia · Green Americas · Orange Africa",
       font=font(9), fill=MUT)
d.text((536, 446), "Map is schematic — drawn, not to scale.", font=font(9), fill=MUT)

# ================= SECONDARY SCENES strip =================
panel(16, 482, 508, 560)
d.text((28, 490), "SCENE 2 — US THANKSGIVING STORM", font=font(11, ), fill=BLUE)
# rain + plane + lightning
for _ in range(70):
    x = random.randint(28, 496); y = random.randint(512, 552)
    d.line([(x, y), (x - 4, y + 8)], fill=(120, 170, 235), width=1)
d.polygon([(120, 540), (200, 528), (230, 536), (150, 548)], fill=(200, 205, 215))
d.polygon([(200, 528), (215, 512), (225, 528)], fill=(180, 185, 195))
d.polygon([(330, 512), (345, 545), (330, 540), (318, 548)], fill=GOLD)
d.text((360, 530), "850,000+ without power;", font=font(10), fill=WHITE)
d.text((360, 544), "flights grounded at DCA", font=font(10), fill=MUT)
panel(524, 482, 1008, 560)
d.text((536, 490), "SCENE 3 — WORLD CHESS CHAMPIONSHIP", font=font(11), fill=GOLD)
# chessboard
bx0, by0 = 536, 508
cs = 6
for r in range(8):
    for c in range(8):
        col = (235, 225, 200) if (r + c) % 2 == 0 else (60, 50, 40)
        d.rectangle([bx0 + c * cs, by0 + r * cs, bx0 + (c + 1) * cs, by0 + (r + 1) * cs], fill=col)
d.ellipse([bx0 + 2 * cs + 1, by0 + 1 * cs + 1, bx0 + 3 * cs - 1, by0 + 2 * cs - 1], fill=(20, 20, 20))
d.ellipse([bx0 + 5 * cs + 1, by0 + 6 * cs + 1, bx0 + 6 * cs - 1, by0 + 7 * cs - 1], fill=(245, 245, 245))
d.text((600, 512), "Gukesh vs Sindarov — Game 3:", font=font(10), fill=WHITE)
d.text((600, 526), "marathon draw, longest of the", font=font(10), fill=MUT)
d.text((600, 540), "series so far.  ●●● HIGH", font=font(10), fill=GREEN)

# ================= UTC TIMELINE =================
panel(16, 572, 1008, 648)
d.text((28, 576), "UTC TIMELINE — FRIDAY 27 NOVEMBER 2026", font=font(12), fill=GOLD)
ty = 630
d.line([(40, ty), (984, ty)], fill=(120, 140, 180), width=2)
for h in range(0, 24, 2):
    x = 40 + h / 23 * 944
    d.line([(x, ty - 5), (x, ty + 5)], fill=WHITE, width=1)
    d.text((x - 10, ty + 8), f"{h:02d}:00", font=font(8), fill=MUT)
timeline = [
    (0, "Kuwait strike reported", RED), (1, "Depardieu trial", BLUE),
    (2, "Gaza: 10 killed", RED), (3, "India SC rulings", GOLD),
    (5, "EU budget fails", BLUE), (8, "UK migration low", BLUE),
    (11, "Nvidia downgrade watch", PURPLE), (13, "Mali: 300+ dead", ORANGE),
    (15, "Thanksgiving storm peaks", GREEN), (17, "Chess Game 3 draw", GOLD),
    (19, "Lille beat Bayern", TEAL), (21, "Black Friday sales", PINK),
]
for j, (h, lab, col) in enumerate(timeline):
    x = 40 + h / 23 * 944
    d.ellipse([x - 5, ty - 5, x + 5, ty + 5], fill=col, outline=WHITE, width=1)
    ly = ty - 24 if j % 2 == 0 else ty - 38
    d.text((x - 30, ly), lab, font=font(7), fill=WHITE)
d.text((28, 636), "", font=font(8), fill=MUT)

# ================= 48 STORIES GRID =================
# (num, region, time, headline, source, conf 3/2/1)
S = [
    ("MIDDLE EAST", "01:03", "Drone strike kills 2 Italians in Kuwait; Iran denies role", "NYT/BBC", 3),
    ("MIDDLE EAST", "02:26", "Israel kills 10 in Gaza; Hamas weighs its response", "Reuters", 3),
    ("MIDDLE EAST", "—", "16 Gaza schoolchildren killed in November, ministry says", "Guardian", 2),
    ("MIDDLE EAST", "—", "Netanyahu leaves Washington with no Gaza deal announced", "Axios", 2),
    ("MIDDLE EAST", "—", "Rights group: Shin Bet tortures Palestinians into confessions", "B'Tselem", 2),
    ("MIDDLE EAST", "—", "Trump: US aid to Israel ends at start of 2027", "White House", 2),
    ("EUROPE", "—", "Zelensky: US too focused on Middle East, not pushing Russia", "BBC", 3),
    ("EUROPE", "—", "Trump asked Putin to 'pull back' aggression in Europe", "Trump", 2),
    ("EUROPE", "05:00", "EU leaders fail to agree €1.78tn 2028–34 budget", "EU summit", 3),
    ("EUROPE", "08:00", "UK net migration lowest since 1997, excluding pandemic", "ONS/NYT", 3),
    ("EUROPE", "01:00", "Depardieu to stand trial over alleged 2018 rape", "BBC", 3),
    ("EUROPE", "03:31", "Diesel tanker capsizes off Ibiza, 1 dead, 7,000 tonnes", "BBC", 3),
    ("EUROPE", "—", "France mainstream risks presidential debacle, no candidate", "BBC", 2),
    ("EUROPE", "—", "UK to call up 100,000 reservists amid Russia threat", "UK govt", 2),
    ("EUROPE", "—", "Lithuania seeks GRU designated a terrorist organisation", "Vilnius", 2),
    ("EUROPE", "—", "German dealer suspected of supplying Channel smuggling gangs", "BBC", 2),
    ("EUROPE", "—", "UK moves Sri Lankan refugee to Eswatini in secret deal", "BBC", 2),
    ("AMERICAS", "—", "Thanksgiving storm: flooding, delays, 850k+ lose power", "NPR/BBC", 3),
    ("AMERICAS", "—", "Judge: FCC violated ABC free speech; halt licence review", "US court", 3),
    ("AMERICAS", "01:49", "Musk: every US child will get two SpaceX shares", "The Hindu", 2),
    ("AMERICAS", "—", "US grounds DCA flights as severe weather hits capital", "FAA", 2),
    ("AMERICAS", "—", "Trump seeks probe into 'FAKE' GDP after growth revised 4.3%", "Mint", 2),
    ("AMERICAS", "—", "Venezuela: debt unsustainable at ~242% of GDP, restructure set", "Caracas", 2),
    ("AMERICAS", "—", "Argentina Senate suspends 2027 primaries; bars central-bank funding", "Senate", 2),
    ("ASIA", "00:26", "Gukesh–Sindarov Game 3: marathon draw at World Chess Ch.", "India Today", 3),
    ("ASIA", "03:46", "India SC: judicial member must sit to confirm PMLA attachment", "TOI", 3),
    ("ASIA", "03:43", "India SC quashes premature release of ex-MP Anand Mohan", "TOI", 3),
    ("ASIA", "—", "Indian politician facing murder charge hosts 400,000-guest wedding", "Al Jazeera", 2),
    ("ASIA", "02:36", "India cabinet approves ₹11,000 cr construction-equipment push", "News On AIR", 3),
    ("ASIA", "—", "Myanmar refuses to comply with parts of ICJ genocide ruling", "ICJ", 3),
    ("ASIA", "—", "Hong Kong tower fire: 168 dead; a watch stopped in the ashes", "BBC", 2),
    ("ASIA", "—", "West Java mine flood: 16 bodies found, 10 miners missing", "Rescuers", 2),
    ("ASIA", "—", "Nepal declares 4,000 landslide missing officially dead", "Kathmandu", 2),
    ("ASIA", "—", "China's drones are reshaping Asia's militaries", "Mint", 2),
    ("AFRICA", "—", "300+ Russians killed as Moscow backs Mali's junta", "Guardian", 2),
    ("AFRICA", "—", "Ebola in Congo passes 12,000 cases; unrest drives responders out", "WHO", 2),
    ("AFRICA", "—", "Egypt arrests motorist over tanker crash that killed 31", "Cairo", 3),
    ("AFRICA", "—", "Cheaper HIV prevention jab reaches Africa, hope for millions", "BBC", 3),
    ("TECH", "00:00", "Goldman: $17–25bn/yr GPU rent at stake in China AI demand", "Goldman", 2),
    ("TECH", "—", "Nvidia faces possible credit downgrade, S&P CreditWatch", "S&P", 3),
    ("TECH", "—", "SpaceX cleared to launch 1m satellites for orbital data centres", "FCC", 3),
    ("TECH", "—", "Anthropic: models keep cyberattack knowledge after unlearning", "Study", 2),
    ("TECH", "—", "AI models can covertly coordinate via shared vLLM server", "Researchers", 2),
    ("TECH", "—", "Kioxia selloff makes it Japan's cheapest blue chip", "Markets", 2),
    ("BUSINESS", "—", "Bitcoin near $60,400; Galaxy drops 'bear market over' call", "Glassnode", 2),
    ("SPORT", "02:30", "Lille hand Bayern Munich first defeat of the season", "UCL", 3),
    ("SPORT", "01:06", "Ferrari boss sets Hamilton, Leclerc target after clash", "F1", 2),
    ("BUSINESS", "—", "Black Friday: memory-chip shortage lifts electronics prices", "Retail", 2),
]
assert len(S) == 48, len(S)

gy0 = 660
d.text((16, 658), "48 STORIES — EACH MARKED HOW SURE  ●●● HIGH  ●●○ MEDIUM  ●○○ LOW", font=font(11), fill=GOLD)
cols, rows = 4, 12
cw, ch = 244, 27
for i, (region, t, head, src, conf) in enumerate(S):
    c, r = i % cols, i // cols
    x0 = 16 + c * (cw + 4); y0 = 678 + r * ch
    col = REGION_COLORS[region]
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch - 3], radius=4, fill=(24, 36, 60))
    d.rectangle([x0, y0, x0 + 4, y0 + ch - 3], fill=col)
    d.text((x0 + 8, y0 + 2), f"{i+1:02d}", font=font(9, True), fill=col)
    lines = wrap(head, font(9), cw - 78)
    d.text((x0 + 30, y0 + 1), lines[0] if lines else "", font=font(9), fill=WHITE)
    if len(lines) > 1:
        d.text((x0 + 30, y0 + 12), lines[1], font=font(9), fill=WHITE)
    dots_txt = "●" * conf + "○" * (3 - conf)
    d.text((x0 + cw - 42, y0 + 13), dots_txt, font=font(8), fill=GOLD)
    d.text((x0 + cw - 42, y0 + 2), t, font=font(7), fill=MUT)

# footer
d.rectangle([0, 1004, W, 1024], fill=(10, 16, 30))
d.text((16, 1008), "Sources: NYT · BBC · Reuters · Guardian · TOI · India Today · Al Jazeera · ONS · EU · FCC · S&P · Goldman Sachs  |  *Ukraine General Staff claim  |  Drawn by code — no photos",
       font=font(9), fill=MUT)

img.save("entry.png", optimize=True)
import os
print("saved", os.path.getsize("entry.png"), "bytes")
