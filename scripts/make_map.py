"""Draw images/map.svg: the spine as a line with fourteen stops, and the families each page's Connections reach.

Run from the repo root: python3 scripts/make_map.py
Nothing to edit by hand: the dots are read from each spine page's Connections, and the families from families.py.
"""

import glob
import re

from families import FAMILIES

TITLES = [
    "Representations",
    "One machine,|one program",
    "One machine,|many programs",
    "Programs too big|for one head",
    "Data outlives|programs",
    "Machines need|to talk",
    "Anyone can|publish",
    "Strangers on|the network",
    "Too many users,|too much data",
    "Buying computers|is too slow",
    "Many people,|one codebase",
    "Software that must|not go down",
    "Machines that learn|from data",
    "Everything still|exists at once",
]

W, H = 1200, 560
LEFT, RIGHT = 90, W - 150
ROWS = (130, 360)
PER_ROW = 7
INK, MUTED, LINE = "#1f2328", "#59636e", "#1f2328"


def stop_xy(i):
    row, col = divmod(i, PER_ROW)
    step = (RIGHT - LEFT) / (PER_ROW - 1)
    x = LEFT + col * step if row == 0 else RIGHT - col * step
    return x, ROWS[row]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def families_reached(path):
    text = open(path).read()
    connections = re.search(r"^## Connections\n(.*?)(?=^## )", text, re.S | re.M).group(1)
    return [f for f in FAMILIES if re.search(rf"\]\({f}/", connections)]


def main():
    pages = sorted(glob.glob("[0-9][0-9]-*.md"))
    assert len(pages) == len(TITLES), "add the new spine page's title to TITLES"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{LEFT - 40}" y="52" font-size="22" font-weight="600" fill="{INK}">The throughline</text>',
        f'<text x="{LEFT - 40}" y="76" font-size="14" fill="{MUTED}">Read the stops in order. '
        "The dots are the families each page connects to.</text>",
    ]

    (x1, y1), (x2, y2) = stop_xy(PER_ROW - 1), stop_xy(PER_ROW)
    r = (y2 - y1) / 2
    path = f"M {stop_xy(0)[0]} {y1} H {x1} A {r} {r} 0 0 1 {x2} {y2} H {stop_xy(len(TITLES) - 1)[0]}"
    out.append(f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')

    for i, (title, page) in enumerate(zip(TITLES, pages)):
        x, y = stop_xy(i)
        out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{LINE}" stroke-width="4"/>')
        out.append(f'<text x="{x}" y="{y + 5}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{i}</text>')
        for j, part in enumerate(title.split("|")):
            out.append(f'<text x="{x}" y="{y + 40 + j * 17}" font-size="13" text-anchor="middle" fill="{INK}">{esc(part)}</text>')
        hubs = families_reached(page)
        dot_y = y + 40 + len(title.split("|")) * 17 + 4
        start = x - (len(hubs) - 1) * 7
        for k, hub in enumerate(hubs):
            out.append(f'<circle cx="{start + k * 14}" cy="{dot_y}" r="5" fill="{FAMILIES[hub][2]}"/>')

    lx, ly = LEFT - 40, H - 34
    for _, label, colour in FAMILIES.values():
        width = 28 + len(label) * 7.4
        assert lx + width <= W, "the legend no longer fits on one line"
        out.append(f'<circle cx="{lx + 6}" cy="{ly}" r="6" fill="{colour}"/>')
        out.append(f'<text x="{lx + 18}" y="{ly + 5}" font-size="14" fill="{INK}">{esc(label)}</text>')
        lx += width

    out.append("</svg>")
    with open("images/map.svg", "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
