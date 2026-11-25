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


def fig_dsa_arrays():
    f = Fig(370, "A linked list and an array, laid out in memory",
            "Memory drawn as a row of cells. Top: six particles of a linked list, each allocated wherever memory "
            "was free, so walking from one to the next jumps back and forth across memory, and almost every jump "
            "misses the cache. Bottom: the same particles in an array, side by side, read in one straight line, with "
            "each fetch from memory bringing several particles at once.")
    cells, x0, cw = 34, 30, 20

    def row(y, filled, cls):
        for i in range(cells):
            f.rect(x0 + i * cw, y, cw - 2, 26, cls if i in filled else "f-faint", 3)

    f.heading(30, 32, "Linked list", "Each particle allocated wherever memory was free")
    order = [3, 21, 9, 30, 14, 26]
    row(100, set(order), "f-soft-warn")
    for k, i in enumerate(order):
        f.text(x0 + i * cw + 9, 118, str(k + 1), "t", 11, "middle", "600")
    for a, b in zip(order, order[1:]):
        xa, xb = x0 + a * cw + 9, x0 + b * cw + 9
        f.path(f"M {xa} 98 Q {(xa + xb) / 2} {98 - 8 - abs(xb - xa) * 0.08} {xb} 98", "warn", 1.4, arrow=True)
    f.text(30, 148, "Every step to the next particle is a jump, and almost every jump is a trip to slow memory.", "t", 12)

    f.heading(30, 186, "Array", "The same particles side by side")
    row(226, set(range(6)), "f-soft-ok")
    for k in range(6):
        f.text(x0 + k * cw + 9, 244, str(k + 1), "t", 11, "middle", "600")
    for start in (0, 4):
        f.rect(x0 + start * cw - 3 + (2 if start else 0), 222, 4 * cw - (2 if start else 0), 34, "s-ok", 4, 'fill="none" stroke-width="1.5"')
    f.line(x0, 270, x0 + 6 * cw, 270, "ok", 1.6, arrow=True)
    f.text(x0, 290, "One straight line: each fetch from memory brings several particles, and the processor fetches", "t", 12)
    f.text(x0, 307, "the next ones before they're needed. Marta's update ran about eight times faster.", "t", 12)
    f.text(30, 350, "Six particles of Marta's thirty thousand; positions in memory illustrative.", "tm", 11.5, italic=True)
    return f


def fig_dsa_hashing():
    rng = Rng(1955)
    cars = []
    while len(cars) < 20000:
        r = rng.next()
        if r < 0.04:
            pick = rng.next()
            ends = 0 if pick < 0.45 else 500 if pick < 0.75 else 100
        elif r < 0.1:
            ends = int(rng.next() * 10) * 100
        else:
            ends = int(rng.next() * 1000)
        cars.append(int(rng.next() * 900 + 100) * 1000 + ends)

    def mixed(n):
        return ((n * 2654435761) % 2 ** 32) * 1000 >> 32

    f = Fig(450, "Twenty thousand freight cars in a thousand slots, two ways",
            "Two bar charts of how many freight cars land in each of a thousand slots. Top: slot chosen by the "
            "car number's last three digits, with tall spikes at slots 0, 100 and 500 holding hundreds of cars, and "
            "most other slots far below average. Bottom: slot chosen by mixing all the digits, with every slot close "
            "to the average of twenty.")
    for k, (title, sub, slot, cls) in enumerate([
            ("Last three digits", "Slot 000 holds every car whose number ends in 000", lambda n: n % 1000, "f-warn"),
            ("Every digit mixed", "Similar numbers land far apart", mixed, "f-ok")]):
        y0 = 32 + k * 190
        counts = [0] * 1000
        for c in cars:
            counts[slot(c)] += 1
        f.heading(30, y0, title, f"{sub}; fullest slot: {max(counts)} cars")
        top, h, x0, wd = 400, 120, 60, 680
        base = y0 + 40 + h
        for i, n in enumerate(counts):
            bh = min(n, top) / top * h
            f.rect(x0 + i * wd / 1000 - 0.5, base - bh, 1.6, bh, cls, 0)
        f.line(x0, base, x0 + wd, base, "ink", 1)
        ay = base - 20 / top * h
        f.line(x0, ay, x0 + wd, ay, "accent", 1, dash="4 3")
        f.text(x0 - 6, ay + 4, "20", "tm", 11, "end")
        f.text(x0 - 6, base - h + 4, f"{top}+", "tm", 11, "end")
        for v in (0, 500, 999):
            f.text(x0 + v * wd / 1000, base + 14, str(v), "tm", 10.5, "middle")
    f.text(30, 432, "Illustrative car numbers, issued in blocks as in the story; the dashed line is the average, 20 per slot.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_hash_tables():
    f = Fig(330, "Growing a hash table all at once, and a little at a time",
            "Two timelines of a game server over ninety seconds. Top: the table doubles all at once at the thirtieth "
            "second, moving four million entries, and the server answers nothing for nearly two seconds. Bottom: "
            "the same four million entries are moved a few at a time with every request, spread over a minute, and "
            "the server keeps answering throughout.")
    x0, wd, span = 40, 680, 90

    def x(t):
        return x0 + t / span * wd

    for k, (title, sub) in enumerate([("All at once", "Allocate a table twice the size, then move every entry"),
                                      ("A little at a time", "Every request also moves a few entries across")]):
        y = 32 + k * 125
        f.heading(30, y, title, sub)
        by = y + 36
        f.rect(x(0), by, wd, 26, "f-soft-ok", 4)
        if k == 0:
            f.rect(x(30), by - 4, x(32) - x(30), 34, "f-warn", 2)
            f.text(x(30), by + 50, "nearly two seconds: 4 million entries moved at once, no answers, every player frozen",
                   "t", 11.5)
        else:
            f.rect(x(30), by + 9, x(90) - x(30), 8, "f-amber", 2)
            f.text(x(30), by + 50, "the same 4 million entries, microseconds per request, over a minute: nobody noticed",
                   "t", 11.5)
    for t in range(0, 91, 15):
        f.text(x(t), 300, f"{t}s", "tm", 11, "middle")
    f.text(30, 322, "Green: the server answering. The table fills past three-quarters at the thirtieth second.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_btrees():
    f = Fig(400, "Twenty-one reads, or three",
            "Two ways to index two million part numbers on disk. Left: a binary tree with one part number per node, "
            "about twenty-one levels deep, so a lookup reads twenty-one places on the disk. Right: a B-tree whose "
            "nodes are whole disk blocks of about two hundred keys each: one block at the top, two hundred below "
            "it, forty thousand below those, enough for eight million parts in three reads.")
    f.heading(30, 32, "One key per node", "About 21 levels for 2 million parts")
    for lvl in range(21):
        y = 70 + lvl * 14
        x = 150 + (18 if lvl % 2 else -18)
        if lvl:
            f.line(px, py, x, y, "line", 1.2)
        f.circle(x, y, 4.5, "f-warn")
        px, py = x, y
    f.text(200, 70 + 10 * 14, "21 reads,", "t", 12.5, "start", "600")
    f.text(200, 70 + 10 * 14 + 17, "one seek each", "t", 12)

    f.heading(330, 32, "A disk block per node", "About 200 keys in each")
    levels = [(1, "1 block"), (200, "200 blocks"), (40000, "40,000 blocks")]
    for lvl, (n, label) in enumerate(levels):
        y = 80 + lvl * 92
        shown = min(n, 5)
        bw = 210 if n == 1 else 46
        total = shown * bw + (shown - 1) * 10 + (30 if n > 5 else 0)
        sx = 330 + (300 - total) / 2
        for b in range(shown):
            bx = sx + b * (bw + 10) + (30 if n > 5 and b == shown - 1 else 0)
            f.rect(bx, y, bw, 26, "f-soft-ok", 3)
            ticks = 40 if n == 1 else 10
            for t in range(1, ticks):
                tx = bx + t * bw / ticks
                f.line(tx, y + 6, tx, y + 20, "ok", 0.8)
            if lvl < 2:
                cx = bx + bw / 2
                f.line(cx, y + 26, cx, y + 92, "line", 1.1)
        if n > 5:
            f.text(sx + 4 * (bw + 10) + 8, y + 18, "…", "t", 14, "middle", "600")
        f.text(648, y + 18, label, "t", 12, "start", "600" if lvl == 2 else "normal")
    f.text(330, 340, "3 reads: 200 × 200 × 200 = 8 million parts", "t", 12.5, "start", "600")
    f.text(30, 385, "Leonard's index: about 21 seeks for a binary search or a balanced binary tree; 3 for the B-tree.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_bloom():
    k = 3
    bits = k / -math.log(1 - 0.01 ** (1 / k))

    def wrong(x, size=1):
        return (1 - math.exp(-k * x / (bits * size))) ** k

    f = Fig(350, "A Bloom filter as the crawl outgrew it",
            "A line chart of how often the crawler's filter wrongly answered 'probably seen', against the number of "
            "URLs it held, as a multiple of the number it was sized for. At the size it was built for, one in a "
            "hundred. When the crawl tripled, about one in seven, with the curve still climbing. A second, flat line "
            "near zero shows the filter resized for twice the new crawl.")
    f.heading(30, 32, "Wrong \"probably seen\" answers", "The filter was never wrong about \"no\"; its \"yes\" got worse as it filled")
    p = axes(f, 90, 84, 620, 176, "URLs held, as a multiple of what the filter was sized for", "wrong yes",
             [(0, "0"), (1, "1×"), (2, "2×"), (3, "3×")], [(0, "0"), (0.05, "5%"), (0.10, "10%"), (0.15, "15%"), (0.2, "20%")],
             (0, 3.3), (0, 0.2))
    f.poly([p(i / 50, wrong(i / 50)) for i in range(166)], "warn", 2.5)
    f.poly([p(i / 50, wrong(i / 50, 6)) for i in range(166)], "ok", 2.5)
    for x, label, dx in [(1, "1 in 100: the size it was built for", -8), (3, "about 1 in 7: three more countries", -8)]:
        px, py = p(x, wrong(x))
        f.line(px, py, px, p(x, 0)[1], "line", 1, dash="3 3")
        f.circle(px, py, 4.5, "f-warn")
        f.text(px + dx, py - 9, label, "t", 12, "start" if dx > 0 else "end", "600")
    f.text(p(3, 0)[0] - 8, p(3, wrong(3, 6))[1] - 8, "resized for twice the new crawl", "t", 12, "end")
    f.text(30, 336, "Three hash functions, an illustrative choice that matches the story's one in a hundred and one in seven.",
           "tm", 11.5, italic=True)
    return f


def fig_dsa_lsm():
    f = Fig(390, "Writing where the data belongs, or writing in order",
            "Two ways of writing monitoring data to one disk. Top: a B-tree index updated in place, where points "
            "from thousands of servers arrive interleaved and each write lands on a different page, so the disk "
            "jumps back and forth. Bottom: points are sorted in memory and written out in long sequential runs as "
            "unchangeable files, which a background process later merges into fewer, larger files.")
    f.heading(30, 32, "Update the index in place", "Points from thousands of servers arrive interleaved; each lands on a different page")
    f.rect(40, 94, 680, 28, "f-faint", 4)
    f.rect(40, 94, 680, 28, "s-line", 4, 'fill="none" stroke-width="1"')
    rng = Rng(2008)
    xs = [50 + rng.next() * 660 for _ in range(14)]
    for a, b in zip(xs, xs[1:]):
        f.path(f"M {num(a)} 92 Q {num((a + b) / 2)} {num(92 - abs(b - a) / 24 - 8)} {num(b)} 92", "line", 1.1)
    for x in xs:
        f.rect(x - 2, 96, 4, 24, "f-warn", 1)
    f.text(40, 142, "The disk spends its time seeking, to change a few bytes here and a few bytes there.", "t", 12)

    f.heading(30, 172, "Sort in memory, write in order, merge later", "When memory holds a few hundred megabytes, write it out in one pass")
    f.box(40, 214, 150, 40, "memory", "f-soft-accent", sub="sorted, filling")
    f.line(194, 234, 226, 234, "ink", 1.5, arrow=True)
    for i in range(5):
        x = 232 + i * 98
        f.rect(x, 220, 92, 28, "f-soft-ok", 3)
        for t in range(1, 12):
            f.line(x + t * 92 / 12, 226, x + t * 92 / 12, 242, "ok", 0.8)
        f.text(x + 46, 264, f"file {i + 1}", "tm", 11, "middle")
    for i in range(3):
        f.line(278 + i * 98, 272, 380, 306, "amber", 1.2)
    f.rect(330, 308, 190, 24, "f-soft-amber", 3)
    f.text(425, 324, "merged, in the background", "t", 11.5, "middle")
    f.text(540, 324, "the cost paid later", "t", 12, "start", "600")
    f.text(40, 356, "Writes became long runs, which the disk is fast at. Reads now check memory and several files, newest first.", "t", 12)
    f.text(30, 380, "Neha's system: 150,000 points a second. Positions on the disk are illustrative.", "tm", 11.5, italic=True)
    return f


def fig_dsa_merkle():
    f = Fig(420, "Following the hashes that differ",
            "A tree of hashes for a file server: one hash at the top, four folders, three files in each folder, "
            "and the blocks of two files. Comparing top-down, the top hash differs, so the four folder hashes are "
            "compared; two differ and two match. Only the files inside the two differing folders are compared, then "
            "only the blocks of the two differing files, which finds three corrupted blocks. Matching branches are "
            "never opened.")
    f.heading(30, 32, "Start at the top, open only what differs", "One comparison when nothing has changed; a few more for each level when something has")
    bad, ok, skip = "f-warn", "f-ok", "f-line"
    root = (380, 84)
    folders = [(110, ok), (290, bad), (470, ok), (650, bad)]
    bad_files = {(1, 1): [False, True, False, True], (3, 0): [False, False, True, False]}
    f.circle(*root, 10, bad)
    f.text(root[0] + 16, root[1] + 4, "the whole server", "tm", 11.5)
    count = 1
    for fi, (fx, fcls) in enumerate(folders):
        f.line(root[0], root[1] + 10, fx, 150, "line", 1.2)
        f.circle(fx, 160, 9, fcls)
        count += 1
        for j in range(3):
            x = fx - 50 + j * 50
            f.line(fx, 169, x, 222, "line", 1.1)
            if fcls == ok:
                f.circle(x, 230, 7, skip)
                continue
            count += 1
            blocks = bad_files.get((fi, j))
            f.circle(x, 230, 7, bad if blocks else ok)
            if blocks:
                for b, broken in enumerate(blocks):
                    bx = x - 39 + b * 26
                    f.line(x, 237, bx + 10, 290, "line", 1)
                    f.rect(bx, 290, 20, 20, bad if broken else ok, 3)
                    count += 1
    f.text(110, 196, "matches: stop", "tm", 11, "middle")
    f.text(470, 196, "matches: stop", "tm", 11, "middle")
    for i, (cls, label) in enumerate([(bad, "hash differs: look inside"), (ok, "hash matches: everything below matches"),
                                      (skip, "never compared")]):
        f.circle((48, 248, 540)[i], 346, 6, cls)
        f.text((60, 260, 552)[i], 350, label, "t", 12)
    f.text(40, 382, f"{count} comparisons find the 3 bad blocks here; among Ingrid's two terabytes, a few hundred did.", "t", 12.5, "start", "600")
    f.text(30, 408, "An illustrative tree: the real one had millions of blocks under the same shape.", "tm", 11.5, italic=True)
    return f


def fig_dsa_queues():
    f = Fig(390, "One line, or three",
            "Two ways of queuing outgoing email in front of the same workers. Top: one first-in, first-out queue, "
            "where a retailer's two million newsletters arrived first and a password reset waits behind all of them, "
            "for hours. Bottom: three queues, urgent mail first, then receipts, then bulk, with bulk guaranteed a share "
            "of the workers and each bulk customer served in turn, so the reset waits seconds.")
    f.heading(30, 32, "One queue, first in, first out", "Tuesday morning: the newsletter went in first")
    f.rect(40, 76, 560, 34, "f-faint", 4)
    f.rect(130, 80, 460, 26, "f-soft-amber", 3)
    f.text(360, 98, "2,000,000 newsletters, one retailer", "t", 12, "middle", "600")
    f.rect(52, 80, 66, 26, "f-warn", 3)
    f.text(85, 98, "reset", "t", 11.5, "middle", "600")
    f.line(604, 93, 630, 93, "ink", 1.5, arrow=True)
    f.box(636, 72, 84, 42, "workers")
    f.text(40, 132, "The reset waits behind every newsletter: hours, with the workers as fast as ever.", "t", 12)

    f.heading(30, 172, "Three queues, and who goes next decided on purpose", "Urgent first, then receipts; bulk always gets a share, one customer at a time")
    lanes = [("Urgent", [("reset", "f-warn"), ("code", "f-warn")], "first"),
             ("Receipts", [("receipt", "f-soft-accent")] * 3, "next"),
             ("Bulk", [("retailer", "f-soft-amber"), ("shop B", "f-faint"), ("retailer", "f-soft-amber"),
                       ("shop C", "f-faint")], "always a share")]
    for i, (name, items, rule) in enumerate(lanes):
        y = 210 + i * 46
        f.text(40, y + 22, name, "t", 12.5, "start", "600")
        f.rect(130, y, 470, 34, "f-faint", 4)
        for j, (label, cls) in enumerate(items):
            x = 588 - (j + 1) * 82
            f.rect(x, y + 4, 76, 26, cls, 3)
            f.text(x + 38, y + 22, label, "t", 11.5, "middle")
        f.line(604, y + 17, 630, y + 17, "ink", 1.5, arrow=True)
        f.text(140, y + 22, rule, "tm", 11.5)
    f.box(636, 206, 84, 126, "workers")
    f.text(40, 362, "The reset waits seconds. The newsletter still goes out, and no one sender holds up another.", "t", 12)
    f.text(30, 382, "Yusuf's mail service; queue lengths are not to scale.", "tm", 11.5, italic=True)
    return f


def edge_point(a, b, w, h):
    """Where the line from the centre of box a towards point b leaves a box of size w by h."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    s = min(w / 2 / abs(dx) if dx else 1e9, h / 2 / abs(dy) if dy else 1e9)
    return a[0] + dx * s, a[1] + dy * s


def fig_dsa_graphs():
    import heapq
    f = Fig(400, "Store every distance, or store the roads",
            "Left: bars on a logarithmic scale comparing what each design stores. A few thousand addresses mean "
            "millions of pairs; forty thousand addresses mean eight hundred million; the road network for the whole "
            "city is ninety thousand stretches of road. Right: a small grid of junctions and roads, with one road "
            "closed. A search from A spreads out in order of distance, and stops when it reaches B, having explored "
            "only the junctions nearer than B; the shortest route avoids the closed road.")
    f.heading(30, 32, "What gets stored", "Every pair of addresses, or the roads between junctions")
    rows = [("4,000 addresses: pairs", 4000 * 3999 / 2, "f-soft-warn"), ("40,000 addresses: pairs", 40000 * 39999 / 2, "f-warn"),
            ("The city's roads", 90000, "f-ok")]
    for i, (label, n, cls) in enumerate(rows):
        y = 84 + i * 62
        bw = (math.log10(n) - 3) / 6 * 250
        f.text(40, y, label, "t", 12, "start", "600")
        f.rect(40, y + 8, bw, 22, cls, 3)
        f.text(46 + bw, y + 24, f"{n / 1e6:,.0f} million" if n >= 1e6 else f"{n:,.0f}", "t", 12)
    for v, lab in [(3, "1,000"), (6, "1 million"), (9, "1 billion")]:
        x = 40 + (v - 3) / 6 * 250
        f.line(x, 268, x, 274, "ink", 1)
        f.text(x, 288, lab, "tm", 11, "middle")
    f.line(40, 268, 290, 268, "ink", 1)
    f.text(40, 306, "Logarithmic scale: each step is a thousand times more.", "tm", 11.5)

    cols, rws, x0, y0, step = 12, 7, 384, 78, 32
    rng = Rng(1998)
    adj = {}
    closed = ((3, 3), (4, 3))
    for c in range(cols):
        for r in range(rws):
            for d in ((1, 0), (0, 1)):
                o = (c + d[0], r + d[1])
                if o[0] < cols and o[1] < rws:
                    wt = 1 + rng.next()
                    if ((c, r), o) != closed:
                        adj.setdefault((c, r), []).append((o, wt))
                        adj.setdefault(o, []).append(((c, r), wt))
    src, dst = (2, 3), (5, 3)
    dist, prev, heap, done = {src: 0}, {}, [(0, src)], []
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.append(u)
        if u == dst:
            break
        for v, wt in adj.get(u, []):
            if d + wt < dist.get(v, 1e9):
                dist[v], prev[v] = d + wt, u
                heapq.heappush(heap, (d + wt, v))
    route, u = [dst], dst
    while u != src:
        u = prev[u]
        route.append(u)

    def pt(n):
        return x0 + n[0] * step, y0 + n[1] * step

    f.heading(380, 32, "Search the roads when asked", "Explore outward in order of distance; stop at B")
    for u, outs in adj.items():
        for v, _ in outs:
            if u < v:
                f.line(*pt(u), *pt(v), "line", 1.2)
    a, b = pt(closed[0]), pt(closed[1])
    f.line(*a, *b, "warn", 2, dash="3 3")
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    f.text(mx, my + 5, "×", "f-warn", 16, "middle", "700")
    f.text(mx, my + 20, "closed", "tm", 10.5, "middle")
    f.poly([pt(n) for n in route], "accent", 3)
    explored = set(done)
    for c in range(cols):
        for r in range(rws):
            n = (c, r)
            f.circle(*pt(n), 5, "f-ok" if n in explored else "f-line")
    for n, lab in ((src, "A"), (dst, "B")):
        f.circle(*pt(n), 9, "f-accent")
        f.text(pt(n)[0], pt(n)[1] + 4, lab, "bg", 11, "middle", "700")
    f.circle(388, 330, 5, "f-ok")
    f.text(398, 334, f"explored: {len(explored)} of {cols * rws} junctions", "t", 12)
    f.line(570, 330, 594, 330, "accent", 3)
    f.text(600, 334, "shortest route", "t", 12)
    f.text(30, 386, "Ruth's numbers on the left; the grid is illustrative. Her city had about ninety thousand stretches of road, "
           "and a query explored a few thousand.", "tm", 11.5, italic=True)
    return f


def fig_dsa_state_machines():
    f = Fig(400, "Flags that allow anything, or states that allow only what's real",
            "Left: five yes-or-no fields on an order make thirty-two combinations, and code could set any of them; "
            "three impossible combinations Chloe found are marked: cancelled and shipped, on forty orders; refunded "
            "but not paid, on eleven; paid, cancelled and awaiting stock at once, on three. Right: nine states and "
            "the moves the business allowed between them. Placed goes to paid or cancelled; paid to awaiting stock, "
            "packing, or cancelled and refunded; awaiting stock to packing; packing to shipped; shipped to delivered "
            "or returned. There is no arrow from cancelled to shipped.")
    f.heading(30, 32, "Five flags", "32 combinations, all reachable")
    for i in range(32):
        r, c = divmod(i, 4)
        x, y = 40 + c * 50, 76 + r * 28
        f.rect(x, y, 44, 22, "f-faint", 3)
    found = [(1, 2, "40", "cancelled and shipped"), (3, 0, "11", "refunded, not paid"), (5, 3, "3", "paid, cancelled, awaiting stock")]
    for r, c, n, _ in found:
        x, y = 40 + c * 50, 76 + r * 28
        f.rect(x, y, 44, 22, "f-warn", 3)
        f.text(x + 22, y + 15, n, "bg", 11.5, "middle", "700")
    for k, (_, _, n, label) in enumerate(found):
        f.text(40, 320 + k * 17, f"{n} orders: {label}", "t", 12)

    f.heading(290, 32, "Nine states, and only the allowed moves", "One function makes every move, or refuses it")
    bw, bh = 116, 30
    pos = {"placed": (350, 92), "paid": (490, 92), "awaiting stock": (640, 92),
           "cancelled": (350, 172), "cancelled and refunded": (490, 172), "packing": (640, 172),
           "shipped": (640, 252), "delivered": (540, 322), "returned": (690, 322)}
    moves = [("placed", "paid"), ("placed", "cancelled"), ("paid", "awaiting stock"), ("paid", "cancelled and refunded"),
             ("paid", "packing"), ("awaiting stock", "packing"), ("packing", "shipped"), ("shipped", "delivered"),
             ("shipped", "returned")]
    for a, b in moves:
        p1 = edge_point(pos[a], pos[b], bw + 4, bh + 4)
        p2 = edge_point(pos[b], pos[a], bw + 10, bh + 10)
        f.line(*p1, *p2, "ink", 1.4, arrow=True)
    p1 = edge_point(pos["cancelled"], pos["shipped"], bw + 4, bh + 4)
    p2 = edge_point(pos["shipped"], pos["cancelled"], bw + 10, bh + 10)
    f.line(*p1, *p2, "warn", 1.4, dash="4 3")
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    f.text(mx, my + 5, "×", "f-warn", 16, "middle", "700")
    f.text(mx - 12, my + 22, "no such move", "tm", 11, "end")
    for name, (x, y) in pos.items():
        w = bw + 26 if name == "cancelled and refunded" else bw
        cls = "f-soft-warn" if name.startswith("cancelled") else "f-soft-accent"
        f.box(x - w / 2, y - bh / 2, w, bh, name, cls, size=11.5)
    f.text(30, 390, "Chloe's order system. Which flag combinations sit where in the grid is illustrative.", "tm", 11.5, italic=True)
    return f


def fig_dsa_power():
    f = Fig(360, "Two engines, one pattern, one line that almost matches",
            "A line chart on a logarithmic time scale. As the line of text that almost matches gets longer, a "
            "backtracking engine's time doubles with every extra character, from microseconds to more than ten "
            "minutes at thirty characters. A linear-time engine's time grows in step with the length and stays in "
            "microseconds. A dashed line marks a ten-millisecond time budget per message.")
    f.heading(30, 32, "Time to give up on one line", "A repetition inside a repetition, against text that fails only at the end")
    p = axes(f, 100, 80, 600, 200, "characters in the line that almost matches", "time",
             [(0, "0"), (10, "10"), (20, "20"), (30, "30")],
             [(-6, "1 µs"), (-3, "1 ms"), (0, "1 s"), (math.log10(60), "1 min"), (3, "17 min")], (0, 31), (-6.3, 3.2))
    f.poly([p(n, math.log10(1e-6 * 2 ** n)) for n in range(0, 31)], "warn", 2.5)
    f.poly([p(n, math.log10(1e-6 * max(n, 1))) for n in range(0, 31)], "ok", 2.5)
    by = p(0, -2)[1]
    f.line(100, by, 700, by, "amber", 1.2, dash="5 4")
    f.text(104, by - 6, "a 10 ms budget per message", "tm", 11)
    f.text(p(1, 1.6)[0], p(1, 1.6)[1], "backtracking: doubles with every character", "t", 12, "start", "600")
    f.text(p(30, 0)[0] - 6, p(30, -4.2)[1], "one pass: grows with the length", "t", 12, "end", "600")
    f.text(30, 346, "Illustrative timings: a microsecond per step. Real engines differ in speed, not in shape.", "tm", 11.5, italic=True)
    return f


def fig_dsa_computability():
    f = Fig(400, "Choosing which way to be wrong",
            "A flow chart of Viktor's scanner. Every program first meets the signature list: a known virus is "
            "blocked, fast and certain. The rest meet a scanner that flags anything suspicious, accepting false "
            "alarms; unflagged programs pass. Flagged programs run in an isolated sandbox with a time limit: one "
            "that does harm is blocked, one that finishes harmlessly passes, and one still running at the limit is "
            "held as unknown.")
    f.heading(30, 32, "No program can decide this for every program", "So each stage chooses its mistakes, and everything has a time limit")
    stages = [("Signature list", "fast, certain, only the known", 84), ("Suspicious?", "flags freely: false alarms accepted", 176),
              ("Sandbox", "run it, watch it, with a time limit", 268)]
    for label, sub, y in stages:
        f.box(40, y, 230, 52, label, "f-soft-accent", sub=sub)
    f.line(155, 136, 155, 172, "ink", 1.5, arrow=True)
    f.text(163, 158, "not known", "tm", 11)
    f.line(155, 228, 155, 264, "ink", 1.5, arrow=True)
    f.text(163, 250, "flagged", "tm", 11)
    outs = [(110, "blocked", "a known virus", "f-soft-warn"), (202, "passed", "nothing suspicious", "f-soft-ok"),
            (264, "blocked", "it did harm", "f-soft-warn"), (306, "passed", "it finished harmlessly", "f-soft-ok"),
            (348, "held: unknown", "still running at the limit", "f-soft-amber")]
    src = {110: 110, 202: 202, 264: 282, 306: 294, 348: 306}
    for y, label, why, cls in outs:
        f.line(274, src[y], 470, y, "ink", 1.4, arrow=True)
        f.box(478, y - 19, 180, 38, label, cls, size=12, sub=why)
    f.text(666, 345, "neither safe", "tm", 11)
    f.text(666, 359, "nor dangerous", "tm", 11)
    f.text(30, 392, "Viktor's scanner. Each stage can still be wrong; what changed is that he chose how.", "tm", 11.5, italic=True)
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
    "dsa-arrays-and-linked-lists": fig_dsa_arrays, "dsa-hashing": fig_dsa_hashing,
    "dsa-hash-tables": fig_dsa_hash_tables, "dsa-b-trees": fig_dsa_btrees,
    "dsa-bloom-filters": fig_dsa_bloom, "dsa-lsm-trees": fig_dsa_lsm,
    "dsa-merkle-dags": fig_dsa_merkle, "dsa-queues": fig_dsa_queues,
    "dsa-graphs": fig_dsa_graphs, "dsa-state-machines": fig_dsa_state_machines,
    "dsa-power-and-predictability": fig_dsa_power, "dsa-computability": fig_dsa_computability,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in FIGURES.items():
        with open(os.path.join(OUT, name + ".svg"), "w") as out:
            out.write(fn().svg())
    print(f"{OUT}: {len(FIGURES)} figures.")


if __name__ == "__main__":
    main()
