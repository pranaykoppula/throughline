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


FIGURES = {
    "00-representations": fig00, "01-one-machine-one-program": fig01, "02-one-machine-many-programs": fig02,
    "03-programs-too-big-for-one-head": fig03, "04-data-outlives-programs": fig04,
    "05-machines-need-to-talk": fig05, "06-anyone-can-publish": fig06, "07-strangers-on-the-network": fig07,
    "08-too-many-users-too-much-data": fig08, "09-buying-computers-is-too-slow": fig09,
    "10-many-people-one-codebase": fig10, "11-software-that-must-not-go-down": fig11,
    "12-machines-that-learn-from-data": fig12, "13-everything-still-exists-at-once": fig13,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGURES.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as out:
            out.write(fn().svg())
    print(f"{OUT}: {len(FIGURES)} figures.")


if __name__ == "__main__":
    main()
