"""Draw images/map.svg: the spine as a line with fourteen stops, and the hubs each page touches.

Run from the repo root: python3 scripts/make_map.py
Edit PAGES when a page's Connections change.
"""

HUBS = {
    "Data": "#2a78d6",
    "DSA": "#1baa7a",
    "Trust": "#d64a4a",
    "Latency": "#e09a1a",
    "Cost": "#8a5cd6",
}

PAGES = [
    ("Representations", ["DSA"]),
    ("One machine,|one program", ["DSA", "Latency", "Cost"]),
    ("One machine,|many programs", ["DSA", "Latency"]),
    ("Programs too big|for one head", ["DSA"]),
    ("Data outlives|programs", ["Data", "DSA", "Trust", "Cost"]),
    ("Machines need|to talk", ["Data", "DSA", "Trust", "Latency"]),
    ("Anyone can|publish", ["Trust"]),
    ("Strangers on|the network", ["Trust"]),
    ("Too many users,|too much data", ["Data", "Latency", "Cost"]),
    ("Buying computers|is too slow", ["Trust", "Cost"]),
    ("Many people,|one codebase", ["DSA", "Trust"]),
    ("Software that must|not go down", ["Cost"]),
    ("Machines that learn|from data", ["Data", "Trust", "Latency", "Cost"]),
    ("Everything still|exists at once", list(HUBS)),
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


def main():
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{LEFT - 40}" y="52" font-size="22" font-weight="600" fill="{INK}">The throughline</text>',
        f'<text x="{LEFT - 40}" y="76" font-size="14" fill="{MUTED}">Read the stops in order. '
        "The dots are the hubs each page comes back to.</text>",
    ]

    (x1, y1), (x2, y2) = stop_xy(PER_ROW - 1), stop_xy(PER_ROW)
    r = (y2 - y1) / 2
    path = f"M {stop_xy(0)[0]} {y1} H {x1} A {r} {r} 0 0 1 {x2} {y2} H {stop_xy(len(PAGES) - 1)[0]}"
    out.append(f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')

    for i, (title, hubs) in enumerate(PAGES):
        x, y = stop_xy(i)
        out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{LINE}" stroke-width="4"/>')
        out.append(f'<text x="{x}" y="{y + 5}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{i}</text>')
        for j, part in enumerate(title.split("|")):
            out.append(f'<text x="{x}" y="{y + 40 + j * 17}" font-size="13" text-anchor="middle" fill="{INK}">{esc(part)}</text>')
        dot_y = y + 40 + len(title.split("|")) * 17 + 4
        start = x - (len(hubs) - 1) * 7
        for k, hub in enumerate(hubs):
            out.append(f'<circle cx="{start + k * 14}" cy="{dot_y}" r="5" fill="{HUBS[hub]}"/>')

    lx = LEFT - 40
    for hub, colour in HUBS.items():
        out.append(f'<circle cx="{lx + 6}" cy="{H - 34}" r="6" fill="{colour}"/>')
        out.append(f'<text x="{lx + 18}" y="{H - 29}" font-size="14" fill="{INK}">{hub}</text>')
        lx += 30 + len(hub) * 9

    out.append("</svg>")
    with open("images/map.svg", "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
