"""Render entry.png (1024x1024) for news-image-20261125, dense 50 stories."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (245, 240, 230)
NAVY = (16, 32, 64)
RED = (192, 0, 32)
INK = (20, 20, 20)
GREY = (100, 100, 100)
GOLD = (176, 141, 0)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSI = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, label, bg, fg=(255, 255, 255)):
    ft = f(FB, 10)
    w = int(d.textlength(label, font=ft)) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=bg)
    d.text((x + 5, y + 2), label, font=ft, fill=fg)
    return w


def badge(d, x, y, n, r=13):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED, outline=(255, 255, 255), width=2)
    ft = f(FB, 13)
    s = str(n)
    d.text((x + r - d.textlength(s, font=ft) / 2, y + 5), s, font=ft, fill=(255, 255, 255))


def scene(d, box, kind, bg, num):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "tariff":
        for i in range(4):
            d.rectangle([x0 + 8 + i * 30, y1 - 34, x0 + 34 + i * 30, y1 - 12], fill=(200, 60, 40) if i % 2 else (40, 90, 160))
        d.rectangle([x0 + 8, y1 - 52, x0 + 128, y1 - 36], fill=(60, 60, 60))
    elif kind == "chips":
        pts = [(x0 + 8, y0 + 18), (x0 + 40, y0 + 26), (x0 + 70, y0 + 20), (x0 + 100, y0 + 38), (x0 + 128, y0 + 58)]
        d.line(pts, fill=RED, width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        d.text((x0 + 8, y0 + 4), "-6.2%", font=f(FB, 16), fill=RED)
    elif kind == "space":
        d.polygon([(cx, y0 + 8), (cx + 12, y0 + 44), (cx - 12, y0 + 44)], fill=(255, 255, 255))
        d.ellipse([cx - 22, y0 + 44, cx + 22, y0 + 62], fill=(255, 180, 60))
        d.ellipse([x1 - 26, y0 + 8, x1 - 12, y0 + 22], fill=(240, 240, 240))
    elif kind == "refinery":
        for i in range(3):
            d.rectangle([x0 + 10 + i * 36, y1 - 40, x0 + 30 + i * 36, y1 - 10], fill=(90, 90, 90))
        d.polygon([(x0 + 118, y1 - 10), (x0 + 128, y1 - 52), (x0 + 134, y1 - 10)], fill=(200, 120, 40))
    elif kind == "tanker":
        d.rectangle([x0 + 10, cy - 4, x0 + 120, cy + 14], fill=(120, 40, 30))
        d.rectangle([x0 + 90, cy - 22, x0 + 108, cy - 4], fill=(160, 160, 160))
        d.polygon([(cx - 8, cy - 30), (cx + 8, cy - 30), (cx, cy - 12)], fill=(255, 160, 40))
    elif kind == "fire":
        d.polygon([(cx, y0 + 8), (cx + 18, y0 + 36), (cx + 8, y0 + 52), (cx - 10, y0 + 52), (cx - 18, y0 + 36)], fill=(255, 120, 20))
        d.rectangle([x0 + 10, y1 - 12, x1 - 10, y1 - 6], fill=(60, 60, 60))
    elif kind == "hostage":
        d.rectangle([x0 + 8, y0 + 12, x1 - 8, y1 - 10], fill=(255, 255, 255))
        d.text((x0 + 16, y0 + 16), "EXIT", font=f(FB, 14), fill=(0, 120, 60))
        d.text((x0 + 16, y0 + 34), "76 FREE", font=f(FB, 12), fill=RED)
    elif kind == "gaza":
        d.rectangle([x0 + 14, y0 + 14, x0 + 54, y1 - 10], fill=(120, 110, 100))
        d.rectangle([x0 + 62, y0 + 26, x0 + 96, y1 - 10], fill=(90, 85, 80))
        d.line([x0 + 100, y0 + 8, x1 - 8, y0 + 30], fill=(80, 80, 80), width=3)
    elif kind == "chip":
        d.rectangle([cx - 26, cy - 18, cx + 26, cy + 18], fill=(30, 60, 120))
        d.text((cx - 18, cy - 8), "NVDA", font=f(FB, 12), fill=(255, 255, 255))
        d.text((x0 + 8, y0 + 4), "-3.9%", font=f(FB, 13), fill=RED)
    elif kind == "treaty":
        d.rectangle([x0 + 10, y0 + 12, x0 + 60, y1 - 12], fill=(0, 90, 160))
        d.rectangle([x0 + 66, y0 + 12, x1 - 10, y1 - 12], fill=(200, 40, 40))
        d.text((x0 + 14, y0 + 18), "AU", font=f(FB, 13), fill=(255, 255, 255))
        d.text((x0 + 70, y0 + 18), "SB", font=f(FB, 13), fill=(255, 255, 255))
    elif kind == "blast":
        d.ellipse([cx - 24, cy - 20, cx + 24, cy + 20], fill=(255, 200, 80))
        d.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(255, 120, 20))
    elif kind == "parade":
        d.ellipse([cx - 30, cy - 16, cx + 30, cy + 16], fill=(255, 200, 60))
        d.text((cx - 14, cy - 8), "100th", font=f(FB, 11), fill=NAVY)
    elif kind == "mine":
        d.rectangle([cx - 4, y0 + 8, cx + 4, y1 - 8], fill=(60, 50, 40))
        d.ellipse([cx - 18, y1 - 22, cx + 18, y1 - 2], fill=(255, 180, 40))
        d.text((x0 + 6, y0 + 4), "100m", font=f(FB, 11), fill=(255, 255, 255))
    else:
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 255, 255))
        d.text((cx - 8, cy - 8), str(num), font=f(FB, 14), fill=NAVY)


REG = {"GLOBAL": (90, 90, 90), "EAST ASIA": (192, 0, 32), "MIDDLE EAST": (180, 110, 0), "AFRICA": (0, 120, 90), "LATIN AMERICA": (0, 110, 180), "NORTH AMERICA": (16, 32, 64), "OCEANIA": (120, 60, 160), "SOUTHEAST ASIA": (0, 140, 140), "SOUTH ASIA": (200, 80, 160), "EUROPE": (60, 90, 200)}

CHIPCOL = {"C": (0, 120, 60), "R": (16, 32, 64), "CL": (200, 90, 0)}
# (num, region, chip, scene, kicker, headline, deck, why, source)
HEROES = [
    (1, "GLOBAL", "R", "tariff", "WASHINGTON - TRADE", "Trump tariffs hit 14 partners", "China 20%, EU 15%, Vietnam 20%, India 17%; 18% for Indonesia and others.", "WHY IT MATTERS: New duties reshape global trade.", "Reuters - USTR"),
    (2, "EAST ASIA", "R", "chips", "SEOUL - MARKETS", "AI chips selloff: Kospi -6.2%", "Kospi 4,697.51, -308.52; SK Hynix -11.05%, Samsung -9.87%; sidecar halted at 09:08.", "WHY IT MATTERS: AI doubts erase a day of gains.", "Korea Exchange - Reuters"),
    (3, "EAST ASIA", "C", "space", "JIUQUAN - SPACE", "Shenzhou-24 docks at Tiangong", "Launched 08:18; first foreign astronaut aboard: Pakistan's Ali, 40.", "WHY IT MATTERS: China opens its station abroad.", "Xinhua - Reuters"),
]
CARDS = [
    (4, "MIDDLE EAST", "CL", "refinery", "RAS TANURA - SAUDI ARABIA", "Houthis claim refinery strike", "Houthis claim Ras Tanura hit; 4 drones intercepted.", "Reuters"),
    (5, "MIDDLE EAST", "CL", "tanker", "STRAIT OF HORMUZ", "Two tankers hit mines, on fire", "IRGC says two tankers hit mines and caught fire; no ships named.", "Reuters - IRNA"),
    (6, "AFRICA", "R", "fire", "CAIRO - EGYPT", "Fuel tanker blast kills 31", "Tanker overturns; 31 dead, 21 hurt; 27 vehicles burn.", "AP - CNN"),
    (7, "LATIN AMERICA", "R", "hostage", "CARTAGENA - COLOMBIA", "76 hostages freed unharmed", "Forces storm Exito store after 18 hours; 1 captor killed, 4 held.", "Reuters - BBC"),
    (8, "MIDDLE EAST", "R", "gaza", "GAZA CITY", "Hamas security chief killed", "Shati camp strike kills Col. Abuelouf, wife, two daughters.", "Reuters"),
    (9, "NORTH AMERICA", "R", "chip", "NEW YORK - MARKETS", "S&P puts Nvidia on downgrade watch", "S&P watch on NVDA rating; shares -3.9% at $149.30.", "Reuters"),
    (10, "OCEANIA", "C", "treaty", "CANBERRA - PACIFIC", "Australia-Solomons pact signed", "Australia primary partner; $740m, no foreign base.", "pm.gov.au - Reuters"),
    (11, "NORTH AMERICA", "C", "blast", "IOWA - USA", "Army blows up 5 tons of explosives", "9,500 lbs of lead azide blown up; EPA reads 0.0 lead.", "AP"),
    (12, "NORTH AMERICA", "C", "parade", "NEW YORK - USA", "Macy's parade delayed 100 years on", "100th parade moved to Sat 28 Nov; first weather delay ever.", "Reuters - AP"),
    (13, "SOUTHEAST ASIA", "R", "mine", "BOGOR - INDONESIA", "9 dead, 17 trapped in gold mine", "Flooded mine, 100 m deep; 9 dead, 17 trapped.", "AP - Reuters"),
]
# ALSO: (num, region, chip, place, headline, source)
ALSO = [
    (14, "MIDDLE EAST", "R", "Brent", "Oil +3.5% to $94.81 on Gulf attacks", "Reuters"),
    (15, "MIDDLE EAST", "R", "Hodeidah", "Coalition strikes Yemen port", "Reuters"),
    (16, "MIDDLE EAST", "R", "Jazan", "Minor damage at Jazan port confirmed", "SPA"),
    (17, "MIDDLE EAST", "R", "Riyadh", "Missiles toward capital intercepted", "Reuters"),
    (18, "EAST ASIA", "R", "Beijing", "China tariff 20%, could rise to 40%", "Reuters"),
    (19, "EUROPE", "R", "Brussels", "EU tariff capped at 15%", "Reuters"),
    (20, "SOUTHEAST ASIA", "R", "Hanoi", "Vietnam 20%, 35% if talks fail", "Reuters"),
    (21, "SOUTH ASIA", "R", "New Delhi", "India 17%, 25% if talks fail", "Reuters"),
    (22, "SOUTHEAST ASIA", "R", "Jakarta", "Indonesia tariff set at 18%", "Reuters"),
    (23, "SOUTHEAST ASIA", "R", "Singapore", "Singapore tariff lowest at 10%", "Reuters"),
    (24, "LATIN AMERICA", "R", "Brasilia", "Brazil Embraer jets face 10% tariff", "Reuters"),
    (25, "NORTH AMERICA", "R", "Washington", "Tariff hearing set for 25 January", "USTR"),
    (26, "NORTH AMERICA", "R", "Wall Street", "S&P 500 closes down 0.25%", "Reuters"),
    (27, "NORTH AMERICA", "C", "Washington", "US Q3 GDP revised up to 4.3%", "Reuters"),
    (28, "NORTH AMERICA", "R", "Washington", "Confidence near 2-year high", "Reuters"),
    (29, "EAST ASIA", "R", "Taipei", "Taiex falls 4.8% in chip rout", "Reuters"),
    (30, "EAST ASIA", "R", "Tokyo", "Nikkei drops 2.8%", "Reuters"),
    (31, "EAST ASIA", "R", "Seoul", "Foreigners sell W1.95tn of shares", "Korea Exchange"),
    (32, "EAST ASIA", "R", "Seoul", "Kospi sidecar halt at 09:08", "Korea Exchange"),
    (33, "EUROPE", "R", "Madrid", "Abrego Garcia lands in Spain, free", "Reuters"),
    (34, "AFRICA", "R", "Damazin", "RSF drone strikes reported, 19 dead", "Reuters"),
    (35, "AFRICA", "R", "Tripoli", "Libya vows retaliation after officers die", "Reuters"),
    (36, "MIDDLE EAST", "R", "Gaza City", "Second Gaza strike kills 1 in Karama", "Reuters"),
    (37, "MIDDLE EAST", "R", "Ras Tanura", "Refinery capacity 550,000 bpd", "Reuters"),
    (38, "EAST ASIA", "C", "Tiangong", "Tang Hongbo makes third station visit", "Xinhua"),
    (39, "NORTH AMERICA", "R", "New York", "NVDA value down to $3.6tn from $5tn", "Reuters"),
    (40, "NORTH AMERICA", "R", "New York", "Parade winds 30-40 mph, gusts 65 mph", "NWS"),
    (41, "LATIN AMERICA", "R", "Cartagena", "Flights diverted to Barranquilla", "Reuters"),
    (42, "AFRICA", "R", "Cairo", "39 ambulances sent to tanker fire", "AP"),
    (43, "SOUTHEAST ASIA", "R", "Bogor", "Mine shaft 100 m deep, river flooded", "AP"),
    (44, "SOUTHEAST ASIA", "R", "Bogor", "11 miners escaped the flooded shaft", "AP"),
    (45, "OCEANIA", "R", "Honiara", "Solomons 2022 China pact may lapse", "Reuters"),
    (46, "NORTH AMERICA", "R", "Washington", "62% say tariffs hurt economy", "Reuters/Ipsos"),
    (47, "GLOBAL", "R", "Washington", "Mexico, Norway excluded for now", "Reuters"),
    (48, "EAST ASIA", "R", "Tokyo", "Japan among the 14 tariff partners", "Reuters"),
    (49, "EAST ASIA", "R", "Seoul", "South Korea among the 14 partners", "Reuters"),
    (50, "SOUTHEAST ASIA", "R", "Bangkok", "Thailand tariff set at 18%", "Reuters"),
]
NUMBERS = [("20%", "top tariff on China"), ("-6.2%", "Kospi fall to 4,697.51"), ("31", "dead in Cairo tanker fire"), ("76", "hostages freed in Cartagena"), ("9", "dead in Bogor gold mine"), ("$740m", "Australia-Solomons pact")]
UTC = [("00:18", "Shenzhou-24 launch"), ("06:35", "Crew enters Tiangong"), ("08:18", "Launch, Beijing time"), ("09:08", "Kospi sidecar halts"), ("11:56", "Shenzhou docks"), ("21:00", "Cairo toll at 31")]

PINS = {1: (-77, 39), 2: (127, 37), 3: (98, 40), 4: (50, 26), 5: (56, 26), 6: (31, 30), 7: (-75, 10), 8: (34, 31), 9: (-74, 41), 10: (149, -35), 11: (-91, 41), 12: (-73, 40), 13: (106, -6)}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    all_stories = HEROES + CARDS + [(n, r, c, "", "", h, "", s) for (n, r, c, p, h, s) in ALSO]
    counts = {}
    for s in all_stories:
        counts[s[1]] = counts.get(s[1], 0) + 1
    total = sum(counts.values())
    assert total == 50, total
    # kicker bar
    d.rectangle([0, 0, W, 20], fill=NAVY)
    d.text((8, 4), "THE WORLD IN ONE DAY", font=f(FB, 11), fill=(255, 255, 255))
    rk = "50 STORIES - %d REGIONS - EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026" % len(counts)
    d.text((W - 8 - d.textlength(rk, font=f(FB, 11)), 4), rk, font=f(FB, 11), fill=(255, 220, 100))
    # masthead
    d.text((8, 24), "Wednesday, 25 November 2026", font=f(FS, 48), fill=NAVY)
    d.line([8, 84, W - 8, 84], fill=NAVY, width=1)
    d.text((8, 88), "Trump tariffs on 14 partners  -  AI chips sell off  -  Shenzhou-24 docks", font=f(FSI, 17), fill=RED)
    # NUMBERS strip
    y = 110
    for i, (num, lab) in enumerate(NUMBERS):
        x = 8 + i * 169
        d.text((x, y), num, font=f(FB, 30), fill=RED)
        for j, ln in enumerate(wrap(d, lab, f(FR, 11), 78)):
            d.text((x + 88, y + 4 + j * 13), ln, font=f(FR, 11), fill=INK)
    d.line([8, 152, W - 8, 152], fill=(200, 200, 200), width=1)
    # UTC strip
    d.rectangle([8, 156, W - 8, 172], fill=NAVY)
    d.text((14, 159), "WEDNESDAY IN UTC", font=f(FB, 10), fill=(255, 220, 100))
    for i, (t, ev) in enumerate(UTC):
        x = 170 + i * 142
        d.text((x, 159), t + "  " + ev, font=f(FR, 10), fill=(255, 255, 255))
    # region bar
    x = 8
    for reg, cnt in counts.items():
        wseg = int(1008 * cnt / total)
        d.rectangle([x, 176, x + wseg - 2, 192], fill=REG[reg])
        lab = "%s %d" % (reg, cnt)
        # small segments: label may spill over the next dark segment, still legible
        d.text((x + 3, 179), lab, font=f(FB, 8), fill=(255, 255, 255))
        x += wseg
    # heroes
    for i, (n, reg, ch, kind, kick, head, deck, why, src) in enumerate(HEROES):
        x0 = 8 + i * 340
        x1 = x0 + 328
        y0, y1 = 198, 398
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(200, 200, 200))
        scene(d, (x0 + 1, y0 + 1, x1 - 1, y0 + 81), kind, REG[reg], n)
        badge(d, x0 + 8, y0 + 8, n)
        chip(d, x1 - 52, y0 + 8, ch, CHIPCOL[ch])
        yy = y0 + 86
        d.text((x0 + 8, yy), kick, font=f(FB, 11), fill=RED)
        yy += 16
        hl = wrap(d, head, f(FB, 24), 312)
        yy = draw_lines(d, hl[:2], x0 + 8, yy, f(FB, 24), INK, 27)
        yy = draw_lines(d, wrap(d, deck, f(FR, 12), 312)[:2], x0 + 8, yy + 2, f(FR, 12), INK, 14)
        yy = draw_lines(d, wrap(d, why, f(FR, 11), 312)[:1], x0 + 8, yy + 3, f(FR, 11), GREY, 13)
        d.text((x0 + 8, y1 - 16), src, font=f(FR, 10), fill=GREY)
    # cards
    for i, (n, reg, ch, kind, kick, head, deck, src) in enumerate(CARDS):
        col, row = i % 5, i // 5
        x0 = 8 + col * 202
        x1 = x0 + 194
        y0 = 404 + row * 132
        y1 = y0 + 126
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(200, 200, 200))
        scene(d, (x0 + 1, y0 + 1, x1 - 1, y0 + 41), kind, REG[reg], n)
        badge(d, x0 + 6, y0 + 6, n, r=11)
        chip(d, x1 - 46, y0 + 6, ch, CHIPCOL[ch])
        yy = y0 + 44
        d.text((x0 + 6, yy), kick, font=f(FB, 9), fill=RED)
        yy += 13
        yy = draw_lines(d, wrap(d, head, f(FB, 15), 182)[:2], x0 + 6, yy, f(FB, 15), INK, 17)
        yy = draw_lines(d, wrap(d, deck, f(FR, 11), 182)[:2], x0 + 6, yy + 1, f(FR, 11), INK, 13)
        d.text((x0 + 6, y1 - 13), src, font=f(FR, 9), fill=GREY)
    # section header
    d.text((8, 668), "WHERE IT HAPPENED - pins 1-13", font=f(FB, 12), fill=NAVY)
    d.text((344, 668), "ALSO ON WEDNESDAY 25 NOVEMBER - STORIES 14-50", font=f(FB, 12), fill=NAVY)
    # map
    mx0, my0, mx1, my1 = 8, 688, 335, 818
    d.rectangle([mx0, my0, mx1, my1], fill=(220, 232, 240), outline=(180, 180, 180))
    for (cx, cy, rx, ry) in [(80, 730, 55, 22), (150, 790, 40, 18), (200, 730, 45, 20), (260, 740, 60, 30), (290, 800, 18, 10), (130, 760, 22, 26)]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(170, 180, 150))
    for n, (lon, lat) in PINS.items():
        px = mx0 + int((lon + 180) / 360 * (mx1 - mx0))
        py = my0 + int((90 - lat) / 180 * (my1 - my0))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3, py - 6), str(n), font=f(FB, 9), fill=(255, 255, 255))
    d.text((8, 822), "Map: original drawing, equirectangular pins.", font=f(FR, 9), fill=GREY)
    d.text((8, 834), "C = OFFICIAL  R = REPORTED  CL = CLAIM", font=f(FB, 10), fill=NAVY)
    d.text((8, 848), "OFFICIAL = on the record. REPORTED = wires.", font=f(FR, 10), fill=INK)
    d.text((8, 860), "CLAIM = one side's account, unverified.", font=f(FR, 10), fill=INK)
    d.text((8, 876), "Sources: Reuters, AP, Xinhua, BBC, CNN,", font=f(FR, 10), fill=INK)
    d.text((8, 888), "Korea Exchange, pm.gov.au, USTR, NWS.", font=f(FR, 10), fill=INK)
    # ALSO two columns, one line each
    for idx, (n, reg, ch, place, head, src) in enumerate(ALSO):
        col = idx // 19
        row = idx % 19
        x = 344 + col * 340
        y = 688 + row * 12
        ft = f(FR, 10)
        txt = "%d. %s: %s (%s) [%s]" % (n, place, head, src, ch)
        while d.textlength(txt, font=ft) > 332 and len(txt) > 20:
            txt = txt[:-5] + "..."
        d.text((x, y), txt, font=ft, fill=INK)
    # legend + date check
    d.text((344, 920), "HOW SURE: C OFFICIAL - on the record  |  R REPORTED - wires  |  CL CLAIM - one side only", font=f(FB, 10), fill=NAVY)
    d.rectangle([8, 936, W - 8, 1010], outline=RED, width=2)
    d.rectangle([8, 936, 130, 1010], fill=RED)
    d.text((16, 962), "DATE", font=f(FB, 16), fill=(255, 255, 255))
    d.text((16, 982), "CHECK", font=f(FB, 16), fill=(255, 255, 255))
    dc1 = "LEFT OUT - happened other days. Mon 23 Nov: PIF Tower strike, 11 hurt; Kospi +6% on Huang return; 3 tankers hit mines."
    dc2 = "Tue 24 Nov: Huawei guilty verdict; Chen Jining probed; Gaza official Naeem Abu Nahel killed; Sudan RSF strikes reported Wed."
    d.text((138, 946), dc1, font=f(FR, 11), fill=INK)
    d.text((138, 966), dc2, font=f(FR, 11), fill=INK)
    d.text((138, 988), "Compiled after Wednesday ended in UTC. Pictures drawn in code, not photos.", font=f(FR, 10), fill=GREY)
    d.text((8, 1014), "50 stories - 10 regions - Wednesday 25 November 2026", font=f(FR, 9), fill=GREY)
    img.save("entry.png")
    print("regions:", counts, "total:", total)


if __name__ == "__main__":
    main()
