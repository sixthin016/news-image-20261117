#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: one 1024x1024 PNG that sums up the
world news of Tuesday 17 November 2026.

A newspaper front-page infographic. Everything is drawn with Pillow from
hand-written layout code -- no photo, no network, no copied artwork -- so
the picture is entirely this session's own work.

Run:  python3 generate_image.py   (writes entry.png next to this file)
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

PAPER = (246, 241, 231)      # warm newsprint
INK = (22, 24, 29)           # near-black text
MUTED = (74, 74, 68)         # grey-brown secondary text
NAVY = (16, 36, 62)          # masthead / footer band
GOLD = (201, 162, 39)        # date + rules
RED = (180, 35, 24)          # top-story accent
CARD = (255, 255, 255)       # story cards
CARD_EDGE = (216, 210, 196)  # card border
SKY = (214, 228, 240)        # pictogram sky
SEA = (46, 111, 164)         # pictogram sea
ORANGE = (232, 122, 30)      # explosion / flame

DEJAVU = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(DEJAVU + name, size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_KICKER = font("DejaVuSans-Bold.ttf", 24)
F_HERO = font("DejaVuSans-Bold.ttf", 54)
F_HEAD = font("DejaVuSans-Bold.ttf", 36)
F_HEAD3 = font("DejaVuSans-Bold.ttf", 29)
F_SUB = font("DejaVuSans.ttf", 28)
F_SUB3 = font("DejaVuSans.ttf", 24)
F_FOOT = font("DejaVuSans.ttf", 26)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 26)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, x0, y0, x1, y1, accent=None):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                           fill=CARD, outline=CARD_EDGE, width=2)
    if accent:
        draw.rectangle([x0, y0 + 10, x0 + 9, y1 - 10], fill=accent)


# ---------------------------------------------------------------- pictograms
def pic_bridge(draw, x, y, s):
    """Kerch / Crimea bridge, broken in the middle, blast above the gap."""
    # sky + sea
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    sea_y = y + int(s * 0.78)
    draw.rectangle([x, sea_y, x + s, y + s], fill=SEA)
    for i in range(3):
        wy = sea_y + 12 + i * 14
        draw.arc([x + 8, wy, x + s - 8, wy + 18], 200, 340,
                 fill=(255, 255, 255), width=3)
    # towers
    tw, th = int(s * 0.07), int(s * 0.42)
    for tx in (x + int(s * 0.18), x + int(s * 0.75)):
        draw.rectangle([tx, y + int(s * 0.30), tx + tw, y + int(s * 0.30) + th],
                       fill=INK)
    # cables
    draw.line([x + int(s * 0.18) + tw // 2, y + int(s * 0.30),
               x + int(s * 0.50), y + int(s * 0.62)], fill=INK, width=3)
    draw.line([x + int(s * 0.75) + tw // 2, y + int(s * 0.30),
               x + int(s * 0.50), y + int(s * 0.62)], fill=INK, width=3)
    # deck, broken at the middle
    dy = y + int(s * 0.62)
    draw.rectangle([x + 10, dy, x + int(s * 0.44), dy + 12], fill=INK)
    draw.rectangle([x + int(s * 0.56), dy, x + s - 10, dy + 12], fill=INK)
    # tilted fallen span
    draw.polygon([(x + int(s * 0.44), dy + 4), (x + int(s * 0.56), dy + 4),
                  (x + int(s * 0.52), dy + 34), (x + int(s * 0.42), dy + 30)],
                 fill=(90, 90, 90))
    # blast starburst over the gap
    cx, cy, r = x + s // 2, y + int(s * 0.42), int(s * 0.16)
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rr = r if i % 2 == 0 else r // 2
        pts.append((cx + rr * 0.9 * math.cos(ang),
                    cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)
    draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                 fill=(255, 214, 64))


def pic_flags(draw, x, y, s):
    """Three small flags on poles: US, China, Russia."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    fw, fh = int(s * 0.26), int(s * 0.20)
    gap = int(s * 0.045)
    total = 3 * fw + 2 * gap
    x0 = x + (s - total) // 2
    fy = y + int(s * 0.30)
    pole_y0, pole_y1 = y + int(s * 0.18), y + int(s * 0.86)
    for i, kind in enumerate(("us", "cn", "ru")):
        fx = x0 + i * (fw + gap)
        draw.line([fx + fw // 2, pole_y0, fx + fw // 2, pole_y1],
                  fill=INK, width=4)
        if kind == "us":
            for stripe in range(5):
                col = (178, 34, 52) if stripe % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx, fy + stripe * fh // 5,
                                fx + fw, fy + (stripe + 1) * fh // 5], fill=col)
            draw.rectangle([fx, fy, fx + fw * 2 // 5, fy + fh * 3 // 5],
                           fill=(60, 59, 110))
        elif kind == "cn":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            draw.ellipse([fx + 6, fy + 5, fx + 18, fy + 17], fill=(255, 222, 0))
        else:
            for j, col in enumerate(((255, 255, 255), (0, 57, 166),
                                     (213, 0, 50))):
                draw.rectangle([fx, fy + j * fh // 3,
                                fx + fw, fy + (j + 1) * fh // 3], fill=col)
        draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
    # ground line
    draw.line([x + 14, pole_y1, x + s - 14, pole_y1], fill=INK, width=4)


def pic_tanker(draw, x, y, s):
    """Oil tanker with a flame above it, on waves."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    sea_y = y + int(s * 0.72)
    draw.rectangle([x, sea_y, x + s, y + s], fill=SEA)
    for i in range(2):
        wy = sea_y + 12 + i * 16
        draw.arc([x + 8, wy, x + s - 8, wy + 18], 200, 340,
                 fill=(255, 255, 255), width=3)
    # hull
    hx0, hx1 = x + int(s * 0.10), x + int(s * 0.90)
    hy0, hy1 = y + int(s * 0.52), y + int(s * 0.74)
    draw.polygon([(hx0, hy0), (hx1, hy0), (hx1 - 14, hy1), (hx0 + 26, hy1)],
                 fill=(40, 40, 48))
    # deck structures + funnel
    draw.rectangle([x + int(s * 0.62), y + int(s * 0.38),
                    x + int(s * 0.80), hy0], fill=(200, 200, 200))
    draw.rectangle([x + int(s * 0.66), y + int(s * 0.30),
                    x + int(s * 0.76), y + int(s * 0.38)], fill=RED)
    # flame (teardrop above the deck)
    fx, fy = x + int(s * 0.30), y + int(s * 0.42)
    draw.polygon([(fx - 15, fy + 12), (fx, fy - 28), (fx + 15, fy + 12)],
                 fill=ORANGE)
    draw.ellipse([fx - 7, fy - 4, fx + 7, fy + 12], fill=(255, 214, 64))


def pic_aid(draw, x, y, s):
    """Aid crate with a red cross, on the ground."""
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    draw.line([x + 10, y + int(s * 0.82), x + s - 10, y + int(s * 0.82)],
              fill=INK, width=4)
    bx0, by0 = x + int(s * 0.22), y + int(s * 0.34)
    bx1, by1 = x + int(s * 0.78), y + int(s * 0.82)
    draw.rectangle([bx0, by0, bx1, by1], fill=(233, 220, 196),
                   outline=INK, width=3)
    cx, cy = (bx0 + bx1) // 2, (by0 + by1) // 2
    cw = int(s * 0.09)
    draw.rectangle([cx - cw, cy - cw * 2, cx + cw, cy + cw * 2], fill=RED)
    draw.rectangle([cx - cw * 2, cy - cw, cx + cw * 2, cy + cw], fill=RED)
    # small second crate
    draw.rectangle([x + int(s * 0.66), y + int(s * 0.60),
                    x + int(s * 0.86), y + int(s * 0.82)],
                   fill=(210, 196, 168), outline=INK, width=2)


def pic_jets(draw, x, y, s):
    """Two fighter jets (side view) with dashed contrails.

    All geometry scales with s, so the jets stay inside their box at any
    size (the bottom-row cards use s=66).
    """
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    # contrails
    for yy in (int(s * 0.28), int(s * 0.60)):
        for i in range(5):
            sx = x + 10 + i * int(s * 0.18)
            draw.line([sx, y + yy, sx + 10, y + yy], fill=(255, 255, 255),
                      width=3)

    def jet(jx, jy, L):
        # tail fin
        draw.polygon([(jx + int(L * 0.12), jy + int(L * 0.24)),
                      (jx + int(L * 0.26), jy),
                      (jx + int(L * 0.34), jy + int(L * 0.24))], fill=INK)
        # fuselage, nose pointing right
        draw.polygon([(jx, jy + int(L * 0.24)),
                      (jx + L, jy + int(L * 0.17)),
                      (jx + L, jy + int(L * 0.29)),
                      (jx, jy + int(L * 0.36))], fill=INK)
        # main wing
        draw.polygon([(jx + int(L * 0.42), jy + int(L * 0.29)),
                      (jx + int(L * 0.72), jy + int(L * 0.58)),
                      (jx + int(L * 0.52), jy + int(L * 0.58))], fill=INK)

    jet(x + int(s * 0.10), y + int(s * 0.16), int(s * 0.72))
    jet(x + int(s * 0.16), y + int(s * 0.50), int(s * 0.60))


def pic_virus(draw, x, y, s):
    """Spiky virus ball (measles) with a cracked shield behind it."""
    import math
    draw.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=SKY)
    cx, cy, r = x + s // 2, y + int(s * 0.52), int(s * 0.26)
    for i in range(12):
        ang = i * math.pi / 6
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + (r + 16) * math.cos(ang), cy + (r + 16) * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=RED, width=5)
        draw.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=RED)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(222, 60, 48))
    for dx, dy in ((-14, -10), (12, 8), (2, -18)):
        draw.ellipse([cx + dx - 6, cy + dy - 6, cx + dx + 6, cy + dy + 6],
                     fill=(178, 35, 24))


def pic_globe(draw, cx, cy, r):
    """Small globe for the masthead: circle, meridians, latitudes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 outline=GOLD, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                 outline=GOLD, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=GOLD, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
             fill=GOLD, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 20, 160,
             fill=GOLD, width=3)


# ------------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 128], fill=NAVY)
    pic_globe(d, 54, 64, 30)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2 + 18, 14), title, font=F_TITLE, fill=(255, 255, 255))
    date = "TUESDAY  •  17 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2 + 18, 78), date, font=F_DATE, fill=GOLD)
    d.rectangle([0, 128, W, 132], fill=GOLD)

    # --- hero: Crimea bridge ------------------------------------------
    card(d, MARGIN, 144, W - MARGIN, 432, accent=RED)
    pic_bridge(d, 52, 168, 236)
    tx = 316
    d.text((tx, 162), "WAR IN UKRAINE — TOP STORY", font=F_KICKER, fill=RED)
    hero_lines = wrap(d, "UKRAINE STRIKES THE CRIMEA BRIDGE",
                      F_HERO, W - MARGIN - tx - 24)
    y = draw_lines(d, hero_lines, tx, 196, F_HERO, INK, 60)
    sub = wrap(d, "Kerch link partly collapses after a missile and drone "
                  "attack; Russia hits Kyiv bridges in reply.",
               F_SUB, W - MARGIN - tx - 24)
    draw_lines(d, sub, tx, y + 12, F_SUB, MUTED, 34)

    # --- middle row: summit + Gulf --------------------------------------
    # pictogram in a fixed left column, text on the right: nothing overlaps
    mid_y0, mid_y1 = 442, 690
    mid_cards = [(MARGIN, 506), (518, W - MARGIN)]
    mid = [
        ("SUMMIT IN CHINA", "TRUMP, XI & PUTIN MEET",
         "First three-way talks in Shenzhen as APEC gathers.",
         pic_flags),
        ("GULF CRISIS", "U.S. STRIKES IRAN",
         "Missile site hit on Qeshm Island; tankers struck in Hormuz.",
         pic_tanker),
    ]
    for (x0, x1), (kick, head, sub, pic) in zip(mid_cards, mid):
        card(d, x0, mid_y0, x1, mid_y1)
        pic(d, x0 + 14, mid_y0 + 64, 120)
        tx = x0 + 150
        text_w = x1 - tx - 18
        d.text((tx, mid_y0 + 16), kick, font=F_KICKER, fill=RED)
        head_lines = wrap(d, head, F_HEAD, text_w)
        y = draw_lines(d, head_lines, tx, mid_y0 + 48, F_HEAD, INK, 41)
        sub_lines = wrap(d, sub, F_SUB, text_w)
        draw_lines(d, sub_lines, tx, y + 10, F_SUB, MUTED, 32)

    # --- bottom row: Gaza, jets, measles --------------------------------
    # pictogram top-right in its own corner; headline width avoids it
    bot_y0, bot_y1 = 704, 934
    bw = (W - 2 * MARGIN - 2 * 12) // 3
    bottom = [
        ("GAZA", "AID CALL TO ISRAEL",
         "Four nations urge Israel to open Gaza crossings; settlers "
         "kill a 72-year-old.", pic_aid),
        ("JAPAN", "JETS SCRAMBLED",
         "Japan sends fighters up after suspected Russian planes "
         "enter its airspace.", pic_jets),
        ("HEALTH", "MEASLES STATUS LOST",
         "U.S. loses elimination status after 26 years: 5,400 cases.",
         pic_virus),
    ]
    for i, (kick, head, sub, pic) in enumerate(bottom):
        x0 = MARGIN + i * (bw + 12)
        x1 = x0 + bw
        card(d, x0, bot_y0, x1, bot_y1)
        pic(d, x1 - 80, bot_y0 + 10, 66)
        d.text((x0 + 16, bot_y0 + 12), kick, font=F_KICKER, fill=RED)
        head_lines = wrap(d, head, F_HEAD3, x1 - x0 - 32 - 78)
        y = draw_lines(d, head_lines, x0 + 16, bot_y0 + 44, F_HEAD3, INK, 34)
        sub_lines = wrap(d, sub, F_SUB3, x1 - x0 - 32)
        draw_lines(d, sub_lines, x0 + 16, y + 8, F_SUB3, MUTED, 28)

    # --- footer ticker ---------------------------------------------------
    # two short lines, each shrunk until it fits the band
    d.rectangle([0, 948, W, H], fill=NAVY)
    foot_lines = [
        "ALSO ON 17 NOVEMBER: Nvidia's bumper earnings  •  146,000 march "
        "in France",
        "Mongolia's president quits  •  19 die in plane crash  •  "
        "Depardieu admits assault",
    ]
    for i, line in enumerate(foot_lines):
        fnt = F_FOOT
        while d.textlength(line, font=fnt) > W - 2 * MARGIN and fnt.size > 18:
            fnt = font("DejaVuSans.ttf", fnt.size - 1)
        lw = d.textlength(line, font=fnt)
        d.text(((W - lw) / 2, 954 + i * 33), line, font=fnt,
               fill=(255, 255, 255))
    return img


if __name__ == "__main__":
    out = build()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
