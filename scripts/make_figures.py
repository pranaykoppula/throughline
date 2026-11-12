"""Draw the wiki's figures into images/figures/: diagrams of a page's problem or its solution.

Run from the repo root: python3 scripts/make_figures.py
Every figure is drawn by code here, never by hand and never by an image generator, so a number
in a story and the picture of it can't drift apart. Each SVG carries its own light and dark
colours, and any animation stops for readers who ask for reduced motion.
"""

import math
import os

OUT = "images/figures"
W = 760

STYLE = """
<style>
  .bg { fill: #ffffff; }
  .t { fill: #1f2328; } .tm { fill: #59636e; }
  .f-ink { fill: #1f2328; } .s-ink { stroke: #1f2328; }
  .f-line { fill: #d0d7de; } .s-line { stroke: #d0d7de; }
  .f-faint { fill: #f6f8fa; } .s-faint { stroke: #f6f8fa; }
  .f-accent { fill: #2a78d6; } .s-accent { stroke: #2a78d6; }
  .f-warn { fill: #d64a4a; } .s-warn { stroke: #d64a4a; }
  .f-ok { fill: #1baa7a; } .s-ok { stroke: #1baa7a; }
  .f-amber { fill: #e09a1a; } .s-amber { stroke: #e09a1a; }
  .f-soft-accent { fill: #ddeaf9; } .f-soft-warn { fill: #f8dede; } .f-soft-ok { fill: #d8f1e8; } .f-soft-amber { fill: #faecd2; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #0d1117; }
    .t { fill: #e6edf3; } .tm { fill: #9198a1; }
    .f-ink { fill: #e6edf3; } .s-ink { stroke: #e6edf3; }
    .f-line { fill: #3d444d; } .s-line { stroke: #3d444d; }
    .f-faint { fill: #161b22; } .s-faint { stroke: #161b22; }
    .f-accent { fill: #4c9aff; } .s-accent { stroke: #4c9aff; }
    .f-warn { fill: #ff7b72; } .s-warn { stroke: #ff7b72; }
    .f-ok { fill: #3fb950; } .s-ok { stroke: #3fb950; }
    .f-amber { fill: #e3b341; } .s-amber { stroke: #e3b341; }
    .f-soft-accent { fill: #102a4a; } .f-soft-warn { fill: #4a1c1c; } .f-soft-ok { fill: #0f3a2a; } .f-soft-amber { fill: #3d2e0e; }
  }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
  text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
</style>
"""

COLOURS = ["ink", "accent", "warn", "ok", "amber", "line"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def num(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


class Fig:
    def __init__(self, h, title, desc):
        self.h, self.title, self.desc, self.parts = h, title, desc, []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, cls="f-faint", rx=4, extra=""):
        self.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" class="{cls}" {extra}/>')

    def line(self, x1, y1, x2, y2, colour="ink", width=1.5, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#arrow-{colour})"' if arrow else ""
        self.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" class="s-{colour}" '
                 f'stroke-width="{width}" fill="none"{d}{a}/>')

    def path(self, d, colour="ink", width=1.5, fill="none", dash=None, arrow=False, extra=""):
        f = f'class="s-{colour}"' if fill == "none" else f'class="s-{colour} {fill}"'
        da = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#arrow-{colour})"' if arrow else ""
        self.add(f'<path d="{d}" {f} stroke-width="{width}" fill="{"none" if fill == "none" else ""}"'
                 f'{da}{a} {extra}/>'.replace(' fill=""', ""))

    def poly(self, pts, colour="ink", width=2):
        d = "M " + " L ".join(f"{num(x)} {num(y)}" for x, y in pts)
        self.path(d, colour, width)

    def circle(self, x, y, r, cls="f-accent", extra=""):
        self.add(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r)}" class="{cls}" {extra}/>')

    def text(self, x, y, s, cls="t", size=13, anchor="start", weight="normal", italic=False):
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{num(x)}" y="{num(y)}" class="{cls}" font-size="{size}" text-anchor="{anchor}" '
                 f'font-weight="{weight}"{st}>{esc(s)}</text>')

    def box(self, x, y, w, h, label, cls="f-faint", tcls="t", size=13, sub=None):
        self.rect(x, y, w, h, cls, rx=6)
        self.rect(x, y, w, h, "s-line", rx=6, extra='fill="none" stroke-width="1"')
        ty = y + h / 2 + (size / 3 if sub is None else -2)
        self.text(x + w / 2, ty, label, tcls, size, "middle", "600")
        if sub:
            self.text(x + w / 2, ty + size + 2, sub, "tm", size - 2, "middle")

    def heading(self, x, y, s, sub=None):
        self.text(x, y, s, "t", 15, "start", "600")
        if sub:
            self.text(x, y + 19, sub, "tm", 12.5)

    def svg(self):
        markers = "".join(
            f'<marker id="arrow-{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" class="f-{c}"/></marker>'
            for c in COLOURS)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {self.h}" width="{W}" height="{self.h}" '
                f'role="img" aria-labelledby="t d">\n<title id="t">{esc(self.title)}</title>\n'
                f'<desc id="d">{esc(self.desc)}</desc>\n{STYLE}<defs>{markers}</defs>\n'
                f'<rect width="{W}" height="{self.h}" class="bg"/>\n' + "\n".join(self.parts) + "\n</svg>\n")


def axes(f, x0, y0, w, h, xlabel, ylabel, xticks, yticks, xr, yr):
    """Draw axes; return a function mapping data (x, y) to picture coordinates."""
    def p(x, y):
        return (x0 + (x - xr[0]) / (xr[1] - xr[0]) * w, y0 + h - (y - yr[0]) / (yr[1] - yr[0]) * h)
    for v, lab in yticks:
        _, yy = p(xr[0], v)
        f.line(x0, yy, x0 + w, yy, "line", 1)
        f.text(x0 - 8, yy + 4, lab, "tm", 11.5, "end")
    for v, lab in xticks:
        xx, _ = p(v, yr[0])
        f.text(xx, y0 + h + 17, lab, "tm", 11.5, "middle")
    f.line(x0, y0 + h, x0 + w, y0 + h, "ink", 1.2)
    f.text(x0 + w / 2, y0 + h + 36, xlabel, "tm", 12, "middle")
    f.text(x0 - 46, y0 - 12, ylabel, "tm", 12)
    return p


class Rng:
    """A tiny fixed-seed generator, so illustrative paths are the same on every run."""
    def __init__(self, seed):
        self.s = seed

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % (2 ** 31)
        return self.s / 2 ** 31


# --------------------------------------------------------------------------- spine figures

def fig00():
    f = Fig(380, "Truncating instead of rounding",
            "Two lines over 22 months from an index value of 1000. With each recalculation rounded, the index "
            "ends near 1098. With each recalculation cut off at three decimal places, the same trades end near 520.")
    f.heading(30, 32, "Vancouver Stock Exchange index, 1982 to 1983",
              "The same trades, with each recalculation rounded or cut off at three decimal places")
    p = axes(f, 90, 80, 520, 230, "Months since launch", "Index", [(m, str(m)) for m in range(0, 23, 2)],
             [(v, str(v)) for v in range(400, 1201, 200)], (0, 22), (400, 1200))
    r = Rng(7)
    n = 220
    walk = [0.0]
    for _ in range(n):
        walk.append(walk[-1] + (r.next() - 0.5) * 14)
    drift = [(98.9 - walk[-1]) * i / n for i in range(n + 1)]
    correct = [1000 + walk[i] + drift[i] for i in range(n + 1)]
    truncated = [correct[i] - (1098.9 - 524.8) * (i / n) for i in range(n + 1)]
    f.poly([p(22 * i / n, correct[i]) for i in range(n + 1)], "ok", 2.2)
    f.poly([p(22 * i / n, truncated[i]) for i in range(n + 1)], "warn", 2.2)
    x, y = p(22, correct[-1])
    f.text(x + 8, y + 4, "rounded: about 1098", "t", 12)
    x, y = p(22, truncated[-1])
    f.text(x + 8, y + 4, "cut off: about 520", "t", 12)
    f.text(90, 368, "The path between start and end is illustrative; the start and end values are from the story.",
           "tm", 11.5, italic=True)
    return f


def fig01():
    f = Fig(400, "Walking a grid by column or by row",
            "A grid stored row by row, each row on its own page of memory. Walking down a column touches a "
            "different page at every step; walking along a row stays on one page until it ends.")
    for side, (x0, title, sub, colour) in enumerate([
            (30, "Down each column", "Every step lands on a different page", "warn"),
            (400, "Along each row", "Each page is used fully, then left", "ok")]):
        f.heading(x0, 32, title, sub)
        cw, ch, gx, gy = 40, 30, x0 + 40, 80
        for row in range(8):
            f.text(gx - 8, gy + row * ch + 20, f"page {row + 1}", "tm", 10.5, "end")
            for col in range(7):
                f.rect(gx + col * cw + 1, gy + row * ch + 1, cw - 2, ch - 2,
                       "f-soft-accent" if row % 2 == 0 else "f-faint", 3)
        if side == 0:
            pts = [(gx + 20, gy + 15 + r * ch) for r in range(8)]
            for i in range(7):
                f.line(*pts[i], *pts[i + 1], colour, 1.8, arrow=True)
            f.line(gx + 20, gy + 15 + 7 * ch, gx + 60, gy + 15, colour, 1.2, dash="4 4", arrow=True)
            f.text(gx + 140, gy + 8 * ch + 30, "8 pages fetched for 8 numbers, then again for the next column",
                   "t", 12, "middle")
        else:
            for r in range(2):
                y = gy + 15 + r * ch
                f.line(gx + 12, y, gx + 7 * cw - 12, y, colour, 1.8, arrow=True)
            f.line(gx + 7 * cw - 12, gy + 15, gx + 12, gy + 15 + ch, colour, 1.2, dash="4 4", arrow=True)
            f.text(gx + 140, gy + 8 * ch + 30, "1 page fetched for 7 numbers in a row", "t", 12, "middle")
    f.text(30, 385, "Joan's grid was larger than core. Swapping the two loops took her run from all night to fifty minutes.",
           "tm", 12, italic=True)
    return f


def fig02():
    f = Fig(430, "Sharing the processor, and the circle that stops everything",
            "Top: one job alone keeps the processor busy about a fifth of the time; three jobs fill each other's "
            "waits. Bottom: two jobs each hold one tape drive and wait for the other's, a circle that never ends; "
            "asking for drives in number order makes the circle impossible.")
    f.heading(30, 30, "Filling the waiting", "Processor time, left to right: busy (blue) and waiting on a device (grey)")
    x0, y0, unit = 140, 64, 23
    one = [1, 4] * 6
    f.text(x0 - 10, y0 + 15, "one job", "t", 12, "end")
    x = x0
    for i, d in enumerate(one[:10]):
        f.rect(x, y0, d * unit - 2, 22, "f-accent" if i % 2 == 0 else "f-line", 3)
        x += d * unit
    f.text(x0 + 575, y0 - 6, "busy 1 in 5", "tm", 11.5, "end")
    for j, name in enumerate(["job A", "job B", "job C"]):
        y = y0 + 40 + j * 26
        f.text(x0 - 10, y + 15, name, "t", 12, "end")
        x = x0 + j * unit
        f.rect(x0, y, j * unit, 22, "f-faint", 3) if j else None
        for k in range(7):
            f.rect(x, y, unit - 2, 22, "f-accent", 3)
            if x + 4 * unit <= x0 + 600:
                f.rect(x + unit, y, 2 * unit - 2, 22, "f-line", 3)
            x += 3 * unit
    f.text(x0 + 600, y0 + 130, "the processor is almost never idle", "tm", 11.5, "end")

    f.heading(30, 230, "The circle", "Black: holds a drive. Red: waits for a drive")
    f.box(110, 270, 120, 46, "job 1", "f-soft-amber")
    f.box(110, 360, 120, 46, "job 2", "f-soft-amber")
    f.box(330, 270, 120, 46, "tape drive 1", "f-faint")
    f.box(330, 360, 120, 46, "tape drive 2", "f-faint")
    f.line(330, 293, 232, 293, "ink", 1.6, arrow=True)
    f.line(330, 383, 232, 383, "ink", 1.6, arrow=True)
    f.line(230, 305, 330, 372, "warn", 1.8, arrow=True)
    f.line(230, 372, 330, 305, "warn", 1.8, arrow=True)
    f.heading(500, 290, "The rule that breaks it")
    f.text(500, 314, "Ask for drives in number order,", "t", 12.5)
    f.text(500, 332, "lowest first. Nobody holding drive 2", "t", 12.5)
    f.text(500, 350, "can be waiting for drive 1, so the", "t", 12.5)
    f.text(500, 368, "circle can't close.", "t", 12.5)
    return f


def fig03():
    f = Fig(360, "Dividing by step, or by decision",
            "Top: five modules, one per step of the flowchart, and every one knows the part-number format, so a "
            "change to the format changes all five. Bottom: one catalogue module hides the format, and the others "
            "only ask it to find, check or print a part, so a change touches one module.")
    steps = ["read orders", "validate", "look up parts", "price", "print lists"]
    f.heading(30, 30, "Divided by step", "Every module knows what a part number looks like")
    for i, s in enumerate(steps):
        x = 30 + i * 146
        f.box(x, 58, 130, 52, s, "f-soft-warn", sub="knows the format")
        if i < 4:
            f.line(x + 130, 84, x + 146, 84, "ink", 1.4, arrow=True)
    f.text(30, 134, "Part numbers change from six digits to nine characters: all five change, over three months.",
           "t", 12.5)
    f.heading(30, 184, "Divided by decision", "One module hides the format; the others only ask it questions")
    for i, s in enumerate(steps):
        if s == "look up parts":
            continue
        x = 30 + i * 146
        f.box(x, 212, 130, 44, s, "f-faint")
        f.line(x + 65, 256, 380, 300, "accent", 1.2, arrow=True)
    f.box(270, 300, 220, 44, "parts catalogue", "f-soft-ok", sub="the only code that knows the format")
    f.text(500, 330, "A later change: one module, two weeks.", "t", 12.5)
    return f


def fig04():
    f = Fig(360, "A tree shaped for one question, and tables with an index",
            "Left: customers, then policies, then claims, then payments, in a tree. Asking which hospitals send "
            "the most claims means walking the whole tree. Right: the same facts as tables, linked by values, "
            "with an index on the hospital column, so the question reads only the matching rows.")
    f.heading(30, 30, "Shaped for statements", "To count claims by hospital, walk everything")
    levels = [("customer", 1), ("policy", 2), ("claim", 4), ("payment", 8)]
    for depth, (name, count) in enumerate(levels):
        y = 70 + depth * 64
        for k in range(count):
            span = 300 / count
            x = 40 + span * k + span / 2
            bw = min(60, span - 6)
            f.rect(x - bw / 2, y, bw, 26, "f-soft-warn" if depth >= 2 else "f-faint", 4)
            f.text(x, y + 17, name if bw >= 50 else "pay", "t", 10.5, "middle")
            if depth:
                parent = 40 + (300 / (count // 2)) * (k // 2) + (300 / (count // 2)) / 2
                f.line(parent, y - 38, x, y, "line", 1.2)
    f.text(190, 345, "Two nights to answer one new question", "t", 12, "middle")
    f.heading(400, 30, "Facts as tables", "Linked by values; an index on hospital")
    f.rect(400, 70, 160, 120, "f-faint", 6)
    f.text(480, 90, "claims", "t", 12.5, "middle", "600")
    for i, (hosp, hl) in enumerate([("St Mary's", True), ("General", False), ("St Mary's", True), ("Mercy", False)]):
        y = 102 + i * 20
        f.rect(408, y, 144, 16, "f-soft-ok" if hl else "f-faint", 2)
        f.text(416, y + 12, f"claim {101 + i}  ·  {hosp}", "t", 10.5)
    f.rect(600, 70, 130, 120, "f-soft-accent", 6)
    f.text(665, 90, "index: hospital", "t", 12, "middle", "600")
    for i, h in enumerate(["General", "Mercy", "St Mary's"]):
        f.text(612, 116 + i * 22, h, "t", 11)
    f.line(600, 160, 553, 108, "accent", 1.3, arrow=True)
    f.line(600, 160, 553, 148, "accent", 1.3, arrow=True)
    f.text(400, 222, "The hospital question: a few lines, under a minute.", "t", 12.5)
    f.text(400, 244, "But every index is also updated on every write:", "t", 12.5)
    f.text(400, 262, "with fourteen of them, the nightly load went", "t", 12.5)
    f.text(400, 280, "from one hour to six.", "t", 12.5)
    return f


def fig05():
    f = Fig(330, "Waiting for every reply, or sending ahead",
            "Two timelines of the same transfer across a long link. Top: send one block, wait a whole round trip "
            "for the confirmation, then send the next. Bottom: send eight numbered blocks before waiting; the "
            "confirmations come back while more blocks are going out.")
    rtt, send, x0, scale = 8.0, 1.0, 140, 22
    for row, (label, window, y) in enumerate([("one at a time", 1, 70), ("eight in flight", 8, 200)]):
        f.heading(30, y - 30, label.capitalize(),
                  "Blue: sending a block. Grey: waiting for its confirmation" if row == 0 else
                  "Numbered blocks; the line is never idle for long")
        t, sent, k = 0.0, 0, 0
        while t < 26:
            for _ in range(window):
                if t + send > 26:
                    break
                f.rect(x0 + t * scale, y, send * scale - 2, 26, "f-accent", 3)
                f.text(x0 + t * scale + send * scale / 2 - 1, y + 17, str(sent + 1), "t", 10, "middle")
                t += send
                sent += 1
            wait = rtt - (window - 1) * send if window > 1 else rtt
            if wait > 0 and t + wait <= 26.5:
                f.rect(x0 + t * scale, y, wait * scale - 2, 26, "f-line", 3)
            t += max(wait, 0)
            k += 1
        f.text(x0 - 10, y + 17, f"{sent} blocks", "t", 12, "end")
    f.line(x0, 120, x0 + 26 * scale, 120, "ink", 1)
    f.text(x0 + 13 * scale, 140, "the same stretch of time", "tm", 11.5, "middle")
    f.text(30, 300, "Lin's transfer went eight times faster. The cost of moving data was the number of round trips,",
           "tm", 12, italic=True)
    f.text(30, 318, "not its size. Numbering the blocks also let the receiver throw away duplicates.", "tm", 12, italic=True)
    return f


def fig06():
    f = Fig(400, "Two copies of the day, and one owner of the truth",
            "A server and two receptionists' browsers. Both browsers show ten o'clock as free, from copies loaded "
            "that morning. Both book it. Before: the server saves both bookings. After: the server checks the slot "
            "is still free and refuses the second, which is told the slot was just taken.")
    cols = {"A": 110, "server": 380, "B": 650}
    for name, x in cols.items():
        label = "receptionist A" if name == "A" else "receptionist B" if name == "B" else "server"
        f.box(x - 75, 20, 150, 38, label, "f-soft-accent" if name == "server" else "f-faint")
        f.line(x, 58, x, 380, "line", 1.2, dash="4 4")
    f.text(cols["A"], 82, "copy: 10:00 free", "tm", 11.5, "middle")
    f.text(cols["B"], 82, "copy: 10:00 free", "tm", 11.5, "middle")
    f.line(cols["A"], 110, cols["server"] - 4, 130, "ink", 1.5, arrow=True)
    f.text((cols["A"] + cols["server"]) / 2, 108, "book 10:00", "t", 11.5, "middle")
    f.line(cols["B"], 140, cols["server"] + 4, 160, "ink", 1.5, arrow=True)
    f.text((cols["B"] + cols["server"]) / 2, 138, "book 10:00", "t", 11.5, "middle")
    f.rect(225, 190, 310, 70, "f-soft-warn", 6)
    f.text(380, 212, "Before: the server saved both", "t", 12.5, "middle", "600")
    f.text(380, 232, "two patients, one ten o'clock filling", "t", 12, "middle")
    f.rect(225, 280, 310, 90, "f-soft-ok", 6)
    f.text(380, 302, "After: the server checks first", "t", 12.5, "middle", "600")
    f.text(380, 322, "A's booking: accepted", "t", 12, "middle")
    f.text(380, 340, "B's booking: refused, \"that slot was just taken\"", "t", 12, "middle")
    f.line(cols["server"] + 155, 345, cols["B"] - 4, 345, "ok", 1.5, arrow=True)
    f.text(cols["B"], 368, "refreshes the day", "tm", 11.5, "middle")
    return f


def fig07():
    f = Fig(330, "Hashing, then salting",
            "Three accounts whose passwords are shown with what is stored. Plain hashes: two accounts with the "
            "same password store the same hash, and one guess cracks both. Salted hashes: a random salt per "
            "account makes every stored value different, so each guess has to be tried against each account.")
    rows = [("anna", "fishplate"), ("ben", "dragon42"), ("cara", "fishplate")]
    hashes = {"fishplate": "5f1c…a90e", "dragon42": "c27d…41b8"}
    salted = ["9b3e…07ad", "e81a…5c32", "41f0…d96b"]
    for side, (x0, title, sub) in enumerate([
            (30, "Hashed", "Same password, same hash"),
            (400, "Salted and hashed", "A random salt per account")]):
        f.heading(x0, 32, title, sub)
        f.text(x0, 82, "account", "tm", 11.5)
        f.text(x0 + 90, 82, "password", "tm", 11.5)
        f.text(x0 + 200, 82, "stored", "tm", 11.5)
        for i, (user, pw) in enumerate(rows):
            y = 94 + i * 40
            same = side == 0 and pw == "fishplate"
            f.rect(x0, y, 330, 30, "f-soft-warn" if same else "f-faint", 4)
            f.text(x0 + 8, y + 20, user, "t", 12.5)
            f.text(x0 + 90, y + 20, pw, "tm", 12.5)
            f.text(x0 + 200, y + 20, hashes[pw] if side == 0 else salted[i], "t", 12.5)
    f.text(30, 240, "One guess, \"fishplate\", hashed once,", "t", 12.5)
    f.text(30, 258, "matches two accounts at the same time.", "t", 12.5)
    f.text(400, 240, "The same guess has to be hashed again", "t", 12.5)
    f.text(400, 258, "with each account's salt. And a slow hash", "t", 12.5)
    f.text(400, 276, "makes every one of those guesses expensive.", "t", 12.5)
    f.text(30, 314, "Hash values are shortened and invented for the picture.", "tm", 11.5, italic=True)
    return f


def fig08():
    f = Fig(360, "Building feeds when posts are written, with an exception",
            "Left: an ordinary climber posts, and the post is added to each of about two hundred followers' "
            "ready-made feeds. Right: an account with 1.8 million followers is left out of that; its posts are "
            "fetched and mixed in when a follower opens their feed.")
    f.heading(30, 30, "Most accounts: write to every follower's feed", "About two hundred small writes per post")
    f.box(40, 160, 120, 44, "a climber posts", "f-soft-accent")
    for i in range(8):
        y = 70 + i * 30
        f.rect(250, y, 110, 22, "f-faint", 4)
        f.text(305, y + 15, "a follower's feed", "tm", 10, "middle")
        f.line(160, 182, 248, y + 11, "accent", 1.1, arrow=True)
    f.text(305, 325, "Opening the app: one lookup", "t", 12, "middle")
    f.heading(400, 30, "A few huge accounts: read at opening time", "1.8 million writes per post was too many")
    f.box(410, 90, 150, 44, "the champion posts", "f-soft-amber")
    f.text(485, 156, "stored once", "tm", 11.5, "middle")
    f.box(600, 200, 130, 60, "a follower opens", "f-faint", sub="the app")
    f.line(560, 120, 650, 198, "amber", 1.4, arrow=True)
    f.text(640, 150, "fetched", "tm", 11, "start")
    f.text(640, 164, "on opening", "tm", 11, "start")
    f.rect(420, 200, 150, 60, "f-soft-accent", 6)
    f.text(495, 226, "ready-made feed", "t", 11.5, "middle")
    f.text(495, 242, "from everyone else", "tm", 10.5, "middle")
    f.line(570, 230, 598, 230, "accent", 1.4, arrow=True)
    f.text(570, 325, "Mixed together: nobody waits", "t", 12, "middle")
    return f


def fig09():
    f = Fig(380, "Buying capacity, or renting it",
            "Demand over two weeks with a sudden spike. Bought servers stay flat until new ones arrive five weeks "
            "later, so the spike is lost. Rented capacity rises within minutes to follow the spike and falls after it.")
    f.heading(30, 32, "Capacity against demand", "Servers needed, around the day a blog wrote about Tariq's company")
    p = axes(f, 90, 80, 600, 230, "Days", "Servers", [(d, str(d)) for d in range(0, 15, 2)],
             [(v, str(v)) for v in range(0, 61, 20)], (0, 14), (0, 60))
    demand = []
    for i in range(141):
        d = i / 10
        base = 5 + 1.5 * math.sin(d * 2 * math.pi)
        spike = 48 * math.exp(-((d - 4) ** 2) / 0.4) + 12 * math.exp(-((d - 5.5) ** 2) / 2)
        demand.append((d, base + spike))
    rented = [(d, v * 1.15 + 1) for d, v in demand]
    f.poly([p(d, v) for d, v in demand], "ink", 2)
    f.poly([p(0, 6), p(14, 6)], "warn", 2.2)
    f.poly([p(d, v) for d, v in rented], "ok", 1.8)
    for i, (label, colour) in enumerate([("demand", "ink"), ("rented: started in minutes", "ok"),
                                         ("bought: six servers, more in five weeks", "warn")]):
        f.line(420, 96 + i * 20, 446, 96 + i * 20, colour, 2.2)
        f.text(454, 100 + i * 20, label, "t", 12)
    f.text(30, 365, "Illustrative shape. Renting removed the wait; it also made every design decision a line on a bill.",
           "tm", 11.5, italic=True)
    return f


def fig10():
    f = Fig(330, "Long branches, or merging every day",
            "Top: three teams branch in January, February and March and merge in September; the branches drift "
            "and the merge takes three weeks. Bottom: everyone merges small changes into the shared code every "
            "day, so the lines never drift far apart.")
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep".split()
    x0, step = 110, 70
    f.heading(30, 30, "Branches merged once", "Payroll, reporting and invoicing, built against code the others no longer had")
    ymain = 80
    f.line(x0, ymain, x0 + 8 * step + 20, ymain, "ink", 2.4)
    for i, m in enumerate(months):
        f.text(x0 + i * step, ymain - 10, m, "tm", 11, "middle")
    for k, (name, colour) in enumerate([("payroll", "accent"), ("reporting", "amber"), ("invoicing", "ok")]):
        y = ymain + 28 + k * 22
        sx = x0 + k * step
        f.path(f"M {sx} {ymain} Q {sx + 10} {y} {sx + 30} {y} L {x0 + 8 * step - 30} {y} "
               f"Q {x0 + 8 * step - 10} {y} {x0 + 8 * step} {ymain}", colour, 2)
        f.text(sx + 34, y - 4, name, "tm", 10.5)
    f.circle(x0 + 8 * step, ymain, 8, "f-warn")
    f.text(x0 + 8 * step + 14, ymain + 30, "three weeks", "t", 12)
    f.text(x0 + 8 * step + 14, ymain + 46, "to merge", "t", 12)
    f.heading(30, 210, "Merged every day", "Small changes, each reviewed and tested before it goes in")
    ymain = 270
    f.line(x0, ymain, x0 + 8 * step + 20, ymain, "ink", 2.4)
    for i in range(32):
        sx = x0 + i * 17.5
        colour = ["accent", "amber", "ok"][i % 3]
        f.path(f"M {sx} {ymain} Q {sx + 4} {ymain + 18} {sx + 9} {ymain + 18} Q {sx + 13} {ymain + 18} {sx + 16} {ymain}",
               colour, 1.6)
    f.text(x0 + 8 * step + 20, ymain + 42, "no big merge day", "t", 12, "end")
    return f


def fig11():
    f = Fig(360, "Are the machines on, or can people buy tickets?",
            "Left: a grid of servers, all green, at twelve minutes past ten. Right: the share of checkouts that "
            "succeeded, falling sharply from ten past ten while every server stays up.")
    f.heading(30, 30, "What the wall showed", "Every server up, at 10:12")
    for r in range(5):
        for c in range(8):
            f.rect(40 + c * 36, 70 + r * 36, 30, 30, "f-ok", 4)
    f.text(180, 280, "Are the machines on? Yes.", "t", 12.5, "middle")
    f.heading(400, 30, "What customers saw", "Share of checkouts succeeding")
    p = axes(f, 440, 70, 290, 180, "Time, 10:00 to 10:30", "", [(0, "10:00"), (10, "10:10"), (20, "10:20"), (30, "10:30")],
             [(0, "0%"), (50, "50%"), (100, "100%")], (0, 30), (0, 100))
    pts = []
    for i in range(61):
        t = i / 2
        v = 98 if t < 10 else max(8, 98 - (t - 10) * 30) if t < 14 else 8 + (t - 14) * 0.4
        pts.append(p(t, v))
    f.poly(pts, "warn", 2.2)
    f.text(585, 316, "Can people buy tickets? Barely.", "t", 12.5, "middle")
    f.text(30, 345, "Rosa's fix: measure from the customer's side, with a robot buying a real ticket every minute.",
           "tm", 11.5, italic=True)
    return f


def fig12():
    f = Fig(370, "A filter that decays, and one that keeps learning",
            "The share of spam caught over three years. A filter trained once starts at ninety-nine in a hundred "
            "and falls to eighty-five by 2004 as spammers change tactics. A filter retrained every week on fresh "
            "reports dips each time spammers change, then recovers.")
    f.heading(30, 32, "Spam caught, out of every hundred", "Nadia's filter, trained once in 2002, and retrained every week")
    p = axes(f, 90, 80, 600, 220, "", "Caught", [(0, "2002"), (1, "2003"), (2, "2004")],
             [(v, str(v)) for v in range(80, 101, 5)], (0, 2), (80, 100))
    once = [p(i / 100, 99 - 14 * (i / 200) ** 1.3) for i in range(201)]
    f.poly(once, "warn", 2.2)
    weekly = []
    for i in range(201):
        t = i / 100
        phase = (t * 6) % 1
        weekly.append(p(t, 98.6 - 2.2 * math.exp(-phase * 6) * (1 if t > 0.3 else 0)))
    f.poly(weekly, "ok", 1.8)
    x, y = p(1.97, 85)
    f.text(x, y + 20, "trained once", "t", 12, "end")
    x, y = p(1.97, 98.6)
    f.text(x, y - 12, "retrained weekly", "t", 12, "end")
    f.text(30, 350, "The end points are from the story; the dips are illustrative.", "tm", 11.5, italic=True)
    return f


def fig13():
    f = Fig(390, "Moving one kind of payment at a time",
            "A thin routing layer sends each kind of payment to the old system or the new one. Standing orders "
            "move first; each night both systems process them and the results are compared, and only after a "
            "month of exact matches does the switch happen. Other kinds follow over years; settlement stays.")
    f.box(300, 24, 160, 40, "payments", "f-faint")
    f.line(380, 64, 380, 92, "ink", 1.5, arrow=True)
    f.box(230, 94, 300, 40, "routing layer", "f-soft-accent", sub=None)
    f.box(60, 200, 220, 60, "old system", "f-faint", sub="COBOL, since 1979")
    f.box(480, 200, 220, 60, "new system", "f-soft-ok", sub="moved one kind at a time")
    f.line(330, 134, 200, 198, "ink", 1.4, arrow=True)
    f.line(430, 134, 560, 198, "ok", 1.4, arrow=True)
    f.line(280, 245, 478, 245, "amber", 1.4, dash="5 4")
    f.text(380, 238, "both run every night", "t", 11.5, "middle")
    f.text(380, 272, "results compared", "tm", 11.5, "middle")
    kinds = [("standing orders", "moved first, in four months", "f-soft-ok"),
             ("most other kinds", "moved over four years", "f-soft-ok"),
             ("core settlement", "stayed, by choice", "f-faint")]
    f.text(60, 312, "Each mismatch was a rule nobody had written down, found one at a time.", "t", 12.5)
    for i, (k, when, cls) in enumerate(kinds):
        x = 60 + i * 220
        f.rect(x, 330, 200, 40, cls, 5)
        f.text(x + 100, 347, k, "t", 12, "middle", "600")
        f.text(x + 100, 363, when, "tm", 11, "middle")
    return f


# --------------------------------------------------------------------------- dsa figures

def fig_dsa_growth():
    f = Fig(400, "Four ways work can grow",
            "A chart of how much work four kinds of code do as the data grows from 1 to 100 items. Work that grows "
            "in step with the data rises as a straight line. Work that grows as n log n rises slightly faster. Work "
            "that grows with the square of the data curves steeply upwards, and work that doubles with each extra "
            "item shoots off the top of the chart almost at once.")
    f.heading(30, 32, "Steps of work, as the data grows", "Every curve fits on the chart at small sizes; only some survive at 100")
    top = 1000
    p = axes(f, 90, 80, 470, 240, "Items of data (n)", "Steps", [(n, str(n)) for n in range(0, 101, 20)],
             [(v, str(v)) for v in range(0, top + 1, 250)], (0, 100), (0, top))
    curves = [("n", lambda n: n, "ok"), ("n log n", lambda n: n * math.log2(n) if n > 1 else 0, "accent"),
              ("n²", lambda n: n * n, "amber"), ("2ⁿ", lambda n: 2 ** n, "warn")]
    for label, fn, colour in curves:
        pts, last = [], None
        for i in range(0, 1001):
            n = i / 10
            v = fn(n)
            if v > top:
                pts.append(p(n, top))
                last = n
                break
            pts.append(p(n, v))
        f.poly(pts, colour, 2.4)
        if last is None:
            x, y = pts[-1]
            f.text(x - 4, y - 8, label, "t", 13, "end", "600")
        else:
            x, y = p(last, top)
            if label == "2ⁿ":
                f.text(x - 6, y + 14, label, "t", 12.5, "end", "600")
            else:
                f.text(x + 6, y + 14, label + "  (both leave the chart)", "t", 12.5, "start", "600")
    f.text(600, 120, "From 10 items to 100:", "t", 12, "start", "600")
    for i, (lab, m) in enumerate([("n", "10 times the work"), ("n log n", "about 20 times"),
                                  ("n²", "100 times"), ("2ⁿ", "a 1 with 27 zeros")]):
        f.text(600, 142 + i * 20, f"{lab}: {m}", "tm", 11.5)
    f.text(30, 385, "Ruairí's customer list grew like n; his duplicate check grew like n².", "tm", 11.5, italic=True)
    return f


def fig_dsa_amortised():
    f = Fig(360, "Paying in lumps, or in small steps",
            "Two panels. Left: the cost of each operation over time, nearly zero most of the time with tall, rare "
            "spikes, and a flat dashed line showing the low average. Right: the same work done in many small steps, "
            "with no tall spikes and a slightly higher average.")
    for side, (x0, title, sub) in enumerate([
            (30, "Rare, large lumps", "Cheapest in total; the deadline sees the spikes"),
            (400, "Many small steps", "A little more in total; no spikes")]):
        f.heading(x0, 32, title, sub)
        base = 290
        f.line(x0, base, x0 + 330, base, "ink", 1.2)
        deadline_y = base - 120
        f.line(x0, deadline_y, x0 + 330, deadline_y, "warn", 1.2, dash="5 4")
        f.text(x0 + 330, deadline_y - 6, "deadline", "tm", 11, "end")
        costs = []
        for i in range(60):
            if side == 0:
                costs.append(190 if i in (11, 29, 47) else 4)
            else:
                costs.append(4 + 11.5 if i % 2 == 0 else 4 + 9)
        for i, c in enumerate(costs):
            cls = "f-warn" if c > 120 else "f-accent"
            f.rect(x0 + 4 + i * 5.4, base - c, 4, c, cls, 1)
        avg = sum(costs) / len(costs)
        f.line(x0, base - avg, x0 + 330, base - avg, "ok", 1.6, dash="3 3")
        f.text(x0 + 4, base - avg - 6, "average", "t", 11)
    f.text(30, 330, "Operations, left to right. Height: the cost of each one.", "tm", 11.5, italic=True)
    f.text(30, 348, "Illustrative numbers.", "tm", 11.5, italic=True)
    return f


def fig_dsa_sorting():
    f = Fig(360, "Splitting around a bad pivot, and a good one",
            "Two diagrams of quicksort on eight records that are already in order. Left: taking the first record as "
            "the pivot puts nothing on one side and everything else on the other, so eight levels of splitting are "
            "needed. Right: taking the middle value splits the records in half each time, so three levels are enough.")
    for side, (x0, title, sub) in enumerate([
            (30, "Pivot: the first record", "On sorted data, each split removes one record"),
            (400, "Pivot: a middle value", "Each split halves what's left")]):
        f.heading(x0, 32, title, sub)
        unit, y = 38, 70
        if side == 0:
            for level in range(8):
                n = 8 - level
                f.rect(x0 + level * unit, y + level * 30, unit - 4, 22, "f-amber", 3)
                f.rect(x0 + (level + 1) * unit, y + level * 30, (n - 1) * unit - 4 if n > 1 else 0, 22,
                       "f-soft-warn", 3)
            f.text(x0, y + 8 * 30 + 16, "8 levels: grows with n, so n² work in all", "t", 12.5)
        else:
            segs = [[(0, 8)]]
            while segs[-1][0][1] - segs[-1][0][0] > 1:
                nxt = []
                for a, b in segs[-1]:
                    m = (a + b) // 2
                    nxt += [(a, m), (m, b)]
                segs.append(nxt)
            for level, row in enumerate(segs):
                for a, b in row:
                    f.rect(x0 + a * unit, y + level * 30, (b - a) * unit - 4, 22,
                           "f-soft-ok" if b - a > 1 else "f-ok", 3)
            f.text(x0, y + 8 * 30 + 16, "3 levels below the top: grows with log n, so n log n in all", "t", 12.5)
    f.text(30, 345, "Margit's 1974 night: the orders arrived already sorted, and the first-record pivot did the worst thing possible.",
           "tm", 11.5, italic=True)
    return f



def fig_dsa_divide():
    f = Fig(400, "Finding one bad commit among 400 by halving",
            "A row of 400 commits. Each of nine steps tests the middle of the commits still in doubt and rules out "
            "half of them, until one commit is left.")
    f.heading(30, 32, "Nine builds instead of four hundred", "Each test of the middle commit rules out half of what's left")
    def tests(c):
        lo, hi, t = 0, 400, 0
        while hi - lo > 1:
            m = (lo + hi) // 2
            lo, hi = (lo, m) if c < m else (m, hi)
            t += 1
        return t
    culprit = next(c for c in range(280, 400) if tests(c) == 9)
    x0, w = 120, 560
    lo, hi, step, y = 0, 400, 0, 72
    while True:
        f.text(x0 - 10, y + 14, "start" if step == 0 else f"test {step}", "t", 11.5, "end")
        f.rect(x0, y, w, 18, "f-faint", 3)
        f.rect(x0 + lo / 400 * w, y, max((hi - lo) / 400 * w, 2), 18, "f-soft-amber" if hi - lo > 1 else "f-warn", 3)
        f.text(x0 + w + 8, y + 14, f"{hi - lo} left", "tm", 11)
        if hi - lo <= 1:
            break
        mid = (lo + hi) // 2
        f.line(x0 + mid / 400 * w, y + 22, x0 + mid / 400 * w, y + 30, "ink", 1.2)
        if culprit < mid:
            hi = mid
        else:
            lo = mid
        step += 1
        y += 30
    f.text(30, 392, "Commit positions are illustrative. 400 commits always take at most 9 tests, because 2⁹ = 512.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_dp():
    a, b = "ABCBDAB", "BDCABA"
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            t[i][j] = t[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(t[i - 1][j], t[i][j - 1])
    path, i, j = set(), n, m
    while i and j:
        path.add((i, j))
        if a[i - 1] == b[j - 1]:
            i, j = i - 1, j - 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    common = "".join(a[i - 1] for (i, j) in sorted(path) if a[i - 1] == b[j - 1] and t[i][j] == t[i - 1][j - 1] + 1)
    f = Fig(450, "A table of answers to smaller questions",
            "A table comparing two short words letter by letter, one along the top and one down the side. Each cell "
            "holds the length of the longest common run of letters for those two prefixes. A highlighted path runs "
            "from the bottom-right corner back to the top-left, marking the letters the two words share.")
    f.heading(30, 32, "The longest run two sequences share, in order",
              f"{a} against {b}: each cell answers one smaller question, once")
    cw, x0, y0 = 40, 90, 80
    for j in range(m + 1):
        f.text(x0 + (j + 1) * cw + cw / 2, y0 + 16, b[j - 1] if j else "–", "t", 13, "middle", "600")
    for i in range(n + 1):
        f.text(x0 + cw / 2, y0 + (i + 1) * 36 + 22, a[i - 1] if i else "–", "t", 13, "middle", "600")
        for j in range(m + 1):
            x, y = x0 + (j + 1) * cw, y0 + (i + 1) * 36
            on = (i, j) in path
            match = on and i and j and a[i - 1] == b[j - 1] and t[i][j] == t[i - 1][j - 1] + 1
            f.rect(x + 1, y + 1, cw - 2, 34, "f-ok" if match else "f-soft-ok" if on else "f-faint", 3)
            f.text(x + cw / 2, y + 22, str(t[i][j]), "t", 12.5, "middle", "600" if on else "normal")
    tx = x0 + (m + 2) * cw + 30
    f.text(tx, 120, "How each cell is filled:", "t", 12.5, "start", "600")
    for k, line in enumerate(["If the two letters match:", "  the cell up and to the left, plus one.",
                              "If they don't:", "  the larger of the cell above", "  and the cell to the left.",
                              "", f"Bottom-right: {t[n][m]}, the length of", f"the common run, here \"{common}\"."]):
        f.text(tx, 144 + k * 19, line, "tm", 12)
    return f


def fig_dsa_greedy():
    r = Rng(208)
    pts = [(0.5, 0.5)] + [(r.next(), r.next()) for _ in range(12)]

    def dist(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def length(route):
        return sum(dist(pts[route[k]], pts[route[(k + 1) % len(route)]]) for k in range(len(route)))
    route, left = [0], set(range(1, len(pts)))
    while left:
        nxt = min(left, key=lambda k: dist(pts[route[-1]], pts[k]))
        route.append(nxt)
        left.remove(nxt)
    greedy = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                cand = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if length(cand) < length(route) - 1e-9:
                    route, improved = cand, True
    f = Fig(400, "A nearest-first route, and the same route with its crossings removed",
            "Two delivery routes through the same twelve stops. Left: the nearest-stop route, efficient at first "
            "and then crossing back over itself with long final legs. Right: the same route after removing every "
            "crossing, shorter, with no legs crossing.")
    gl, il = length(greedy), length(route)
    for side, (x0, title, rt, colour) in enumerate([
            (30, "Nearest stop first", greedy, "warn"), (400, "Then remove every crossing", route, "ok")]):
        f.heading(x0, 32, title, f"Route length: {100 * length(rt) / il:.0f}" + (" (the improved route is 100)" if side == 0 else ""))
        def xy(k):
            return x0 + 20 + pts[k][0] * 300, 70 + pts[k][1] * 290
        d = "M " + " L ".join(f"{num(xy(k)[0])} {num(xy(k)[1])}" for k in rt + [rt[0]])
        f.path(d, colour, 2)
        for k in range(len(pts)):
            x, y = xy(k)
            if k == 0:
                f.rect(x - 7, y - 7, 14, 14, "f-ink", 2)
            else:
                f.circle(x, y, 5, "f-accent")
        x, y = xy(0)
        f.text(x + 10, y - 8, "depot", "tm", 11)
    f.text(30, 390, f"Computed from the same twelve randomly placed stops; the greedy route is {100 * (gl / il - 1):.0f}% longer.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_heaps():
    vals = [3, 8, 5, 12, 9, 7, 15, 20, 14, 11]
    f = Fig(390, "A heap as a tree and as an array",
            "A heap of timers drawn two ways: as a tree, with the soonest-due timer at the top and every timer due no "
            "later than the ones below it, and as the array it's actually stored in, with arrows showing that each "
            "item's children sit at twice its position and one more.")
    f.heading(30, 32, "Seconds until each timer is due", "Every timer is due no later than the ones below it")
    pos = {}
    for i, v in enumerate(vals):
        level = int(math.log2(i + 1))
        idx = i - (2 ** level - 1)
        span = 680 / (2 ** level)
        pos[i] = (40 + span * idx + span / 2, 80 + level * 52)
    for i in range(len(vals)):
        for c in (2 * i + 1, 2 * i + 2):
            if c < len(vals):
                f.line(pos[i][0], pos[i][1], pos[c][0], pos[c][1], "line", 1.4)
    for i, v in enumerate(vals):
        x, y = pos[i]
        f.circle(x, y, 17, "f-ok" if i == 0 else "f-soft-accent")
        f.text(x, y + 5, str(v), "t", 13, "middle", "600")
    f.text(400, 72, "the next to fire", "t", 11.5, "start")
    y = 290
    f.text(30, y + 76, "Stored as an array: the children of position i are at 2i + 1 and 2i + 2", "tm", 12)
    for i, v in enumerate(vals):
        x = 30 + i * 52
        f.rect(x, y, 48, 30, "f-ok" if i == 0 else "f-soft-accent", 4)
        f.text(x + 24, y + 20, str(v), "t", 13, "middle", "600")
        f.text(x + 24, y + 46, str(i), "tm", 11, "middle")
    f.path(f"M {30 + 1 * 52 + 24} {y} Q {30 + 2.2 * 52} {y - 40} {30 + 3 * 52 + 24} {y - 2}", "accent", 1.4, arrow=True)
    f.path(f"M {30 + 1 * 52 + 24} {y} Q {30 + 2.7 * 52} {y - 52} {30 + 4 * 52 + 24} {y - 2}", "accent", 1.4, arrow=True)
    f.text(560, y + 20, "position 1's children:", "tm", 11.5)
    f.text(560, y + 36, "positions 3 and 4", "tm", 11.5)
    return f



def fig_dsa_tries():
    words = ["paracetamol", "paroxetine", "parafon", "hydralazine", "hydrochlorothiazide", "hydroxyzine"]
    f = Fig(440, "A trie, plain and compressed",
            "A tree of medicine names stored by their letters. Names sharing a beginning share a path from the top. "
            "Left: one node per letter, with long single-file chains. Right: the same names with each single-file "
            "chain merged into one node, branching only where names differ.")

    def build(ws):
        root = {}
        for w in ws:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node["$"] = {}
        return root

    def compress(node):
        out = {}
        for ch, child in node.items():
            if ch == "$":
                out["$"] = {}
                continue
            label, cur = ch, child
            while len(cur) == 1 and "$" not in cur:
                (k, v), = cur.items()
                label += k
                cur = v
            out[label] = compress(cur)
        return out

    def count(node):
        return sum(1 + count(c) for k, c in node.items() if k != "$")

    def width(label, node, small):
        own = 40 if small else 6.6 * len(label) + 12
        kids = sum(width(k, c, small) for k, c in node.items() if k != "$")
        return max(own, kids)

    def draw(node, x0, y, px, py, small):
        x = x0
        for k, c in [(k, c) for k, c in node.items() if k != "$"]:
            w = width(k, c, small)
            cx = x + w / 2
            f.line(px, py + 8, cx, y - 8, "line", 1)
            bw = 12 if small else 6.6 * len(k) + 8
            f.rect(cx - bw / 2, y - 8, bw, 16, "f-ok" if "$" in c else "f-soft-accent", 4)
            f.text(cx, y + 4, k, "t", 9.5 if small else 10.5, "middle", "600")
            draw(c, x, y + (17 if small else 44), cx, y, small)
            x += w

    plain, comp = build(words), compress(build(words))
    f.heading(30, 30, "One node per letter", f"{count(plain)} nodes for {len(words)} names")
    wp = sum(width(k, c, True) for k, c in plain.items())
    f.circle(30 + wp / 2, 62, 6, "f-ink")
    draw(plain, 30, 84, 30 + wp / 2, 54, True)
    f.heading(330, 30, "Single-file chains merged", f"{count(comp)} nodes for the same names")
    wc = sum(width(k, c, False) for k, c in comp.items())
    f.circle(330 + wc / 2, 62, 6, "f-ink")
    draw(comp, 330, 100, 330 + wc / 2, 54, False)
    f.text(330, 400, "Green: where a whole name ends.",
           "tm", 11.5, italic=True)
    f.text(330, 418, "Built by the script from the story's names.", "tm", 11.5, italic=True)
    return f


def fig_dsa_logs():
    f = Fig(360, "A balance, and a ledger",
            "Two ways to store a wallet. Left: one balance per account, overwritten by each change, with a corrupted "
            "value and no way back. Right: a ledger of entries, each written once, with a duplicate bonus corrected "
            "by a reversing entry, and the balance worked out as the sum of the entries.")
    f.heading(30, 32, "Overwrite the balance", "Each change replaces the last")
    vals = [("top-up", "500"), ("payment", "380"), ("bonus", "430"), ("bonus again (bug)", "480"), ("corrupted write", "9,104")]
    for i, (what, v) in enumerate(vals):
        y = 70 + i * 40
        last = i == len(vals) - 1
        f.rect(30, y, 300, 30, "f-soft-warn" if last else "f-faint", 4)
        f.text(42, y + 20, what, "tm" if not last else "t", 12)
        f.text(318, y + 20, f"balance: {v}", "t", 12, "end", "600" if last else "normal")
        if not last:
            f.line(320, y + 30, 320, y + 40, "line", 1)
    f.text(30, 290, "Only the last row exists. The earlier ones are gone,", "t", 12)
    f.text(30, 308, "so nobody can say what the balance should be.", "t", 12)
    f.heading(400, 32, "Append to a ledger", "Each entry written once; the balance is their sum")
    entries = [("top-up", "+500"), ("payment", "−120"), ("bonus", "+50"), ("bonus again (bug)", "+50"),
               ("reversal of the duplicate", "−50")]
    for i, (what, v) in enumerate(entries):
        y = 70 + i * 40
        cls = "f-soft-amber" if "bug" in what else "f-soft-ok" if "reversal" in what else "f-faint"
        f.rect(400, y, 330, 30, cls, 4)
        f.text(412, y + 20, what, "t", 12)
        f.text(718, y + 20, v, "t", 12, "end", "600")
    f.text(400, 290, "Balance: 500 − 120 + 50 + 50 − 50 = 430,", "t", 12, "start", "600")
    f.text(400, 308, "and every step of how it got there.", "t", 12)
    f.text(30, 345, "Pesos; illustrative entries.", "tm", 11.5, italic=True)
    return f


def fig_dsa_approx():
    f = Fig(380, "Memory for an exact count and an approximate one",
            "A chart of memory against the number of different readers counted. Remembering every reader exactly "
            "grows in a straight line, from kilobytes to gigabytes. The approximate summary stays flat at about "
            "twelve kilobytes however many readers there are, with an error of about one per cent.")
    f.heading(30, 32, "Memory to count distinct readers", "Exact set against a 12 KB summary, on a log scale")
    p = axes(f, 100, 80, 520, 230, "Different readers counted", "Memory",
             [(3, "1,000"), (4, "10,000"), (5, "100,000"), (6, "1 million"), (7, "10 million"), (8, "100 million")],
             [(3, "1 KB"), (4, "10 KB"), (5, "100 KB"), (6, "1 MB"), (7, "10 MB"), (8, "100 MB"), (9, "1 GB"), (10, "10 GB")],
             (3, 8), (3, 10))
    f.poly([p(x / 10, x / 10 + math.log10(16)) for x in range(30, 81)], "warn", 2.4)
    f.poly([p(x / 10, math.log10(12 * 1024)) for x in range(30, 81)], "ok", 2.4)
    x, y = p(5.2, 5.2 + math.log10(16))
    f.text(x - 10, y - 12, "exact: about 16 bytes per reader", "t", 12, "end")
    x, y = p(8, math.log10(12 * 1024))
    f.text(x - 6, y - 10, "HyperLogLog: 12 KB, about ±1%", "t", 12, "end")
    f.text(30, 365, "Assumes 16 bytes per stored reader ID; real sets use more once overheads are counted.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_search():
    docs = {1: "flood closes Kirkstall bypass", 2: "council debates flood defences", 3: "bypass vote delayed again"}
    index = {}
    for d, text in docs.items():
        for w in text.split():
            index.setdefault(w.lower(), []).append(d)
    f = Fig(420, "An inverted index",
            "An inverted index. Three short articles on the left. In the middle, a table from each word to the "
            "articles containing it, in order. On the right, a two-word search fetching two lists and keeping only "
            "the articles in both.")
    f.heading(30, 32, "Articles", "Headlines stand in for the text")
    for i, (d, text) in enumerate(docs.items()):
        y = 66 + i * 52
        f.rect(30, y, 210, 40, "f-faint", 5)
        f.text(40, y + 16, f"article {d}", "tm", 11)
        f.text(40, y + 32, text, "t", 11.5)
    f.heading(270, 32, "Inverted index", "Word: the articles containing it")
    for i, w in enumerate(sorted(index)):
        y = 66 + i * 24
        hl = w in ("flood", "bypass")
        f.rect(270, y, 220, 20, "f-soft-accent" if hl else "f-faint", 3)
        f.text(280, y + 14, w, "t", 11.5, "start", "600" if hl else "normal")
        f.text(480, y + 14, ", ".join(str(n) for n in index[w]), "t", 11.5, "end")
    f.heading(520, 32, "Search: flood bypass", "Walk both lists together")
    a, b = index["flood"], index["bypass"]
    f.text(520, 90, f"flood:   {', '.join(map(str, a))}", "t", 12.5)
    f.text(520, 112, f"bypass: {', '.join(map(str, b))}", "t", 12.5)
    both = sorted(set(a) & set(b))
    f.rect(520, 130, 210, 34, "f-soft-ok", 5)
    f.text(530, 152, f"in both: article {', '.join(map(str, both))}", "t", 12.5, "start", "600")
    f.text(520, 196, "Then rank: rare words such as", "t", 12)
    f.text(520, 214, "\"Kirkstall\" count for more than", "t", 12)
    f.text(520, 232, "common ones such as \"flood\".", "t", 12)
    return f


FIGURES = {
    "00-representations": fig00, "01-one-machine-one-program": fig01, "02-one-machine-many-programs": fig02,
    "03-programs-too-big-for-one-head": fig03, "04-data-outlives-programs": fig04,
    "05-machines-need-to-talk": fig05, "06-anyone-can-publish": fig06, "07-strangers-on-the-network": fig07,
    "08-too-many-users-too-much-data": fig08, "09-buying-computers-is-too-slow": fig09,
    "10-many-people-one-codebase": fig10, "11-software-that-must-not-go-down": fig11,
    "12-machines-that-learn-from-data": fig12, "13-everything-still-exists-at-once": fig13,
    "dsa-growth": fig_dsa_growth, "dsa-amortised-cost": fig_dsa_amortised, "dsa-sorting": fig_dsa_sorting,
    "dsa-divide-and-conquer": fig_dsa_divide, "dsa-dynamic-programming": fig_dsa_dp,
    "dsa-greedy": fig_dsa_greedy, "dsa-heaps": fig_dsa_heaps,
    "dsa-tries": fig_dsa_tries, "dsa-append-only-logs": fig_dsa_logs,
    "dsa-exact-or-approximate": fig_dsa_approx, "dsa-search": fig_dsa_search,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGURES.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as out:
            out.write(fn().svg())
    print(f"{OUT}: {len(FIGURES)} figures.")


if __name__ == "__main__":
    main()
