"""Draw images/map.svg and map.html: an interactive transit map of the spine and its concept hubs.

Run from the repo root: python3 scripts/make_map.py
Edit PAGES when a page's Connections change.
"""

import glob
import html
import json
import os
import posixpath
import re

HUBS = {
    "Data": "#2a78d6",
    "DSA": "#1baa7a",
    "Trust": "#d64a4a",
    "Latency": "#e09a1a",
    "Cost": "#8a5cd6",
}

HUB_FOLDERS = {
    "Data": "data",
    "DSA": "dsa",
    "Trust": "auth",
    "Latency": "latency",
    "Cost": "cost",
}

HUB_DEFAULT_PAGE = {
    "Data": "data/access-patterns.md",
    "DSA": "dsa/hashing.md",
    "Trust": "auth/least-privilege.md",
    "Latency": "latency/round-trips.md",
    "Cost": "cost/cloud-bills.md",
}

FAMILY_META = {
    "data": ("Data", "#2a78d6"),
    "dsa": ("DSA", "#1baa7a"),
    "auth": ("Trust & Auth", "#d64a4a"),
    "latency": ("Latency", "#e09a1a"),
    "cost": ("Cost", "#8a5cd6"),
    "math": ("Math", "#0969da"),
    "runtimes": ("Runtimes", "#bf3989"),
    "tooling": ("Tooling", "#cf222e"),
    "vendors": ("Vendors", "#9a6700"),
    "cloud": ("Cloud", "#1a7f37"),
    "ai": ("AI", "#8250df"),
    "writing": ("Writing", "#57606a"),
}

PAGES = [
    ("Representations", ["DSA"], "00-representations.md"),
    ("One machine,|one program", ["Data", "DSA", "Latency", "Cost"], "01-one-machine-one-program.md"),
    ("One machine,|many programs", ["DSA", "Latency"], "02-one-machine-many-programs.md"),
    ("Programs too big|for one head", ["Data", "DSA"], "03-programs-too-big-for-one-head.md"),
    ("Data outlives|programs", ["Data", "DSA", "Trust", "Cost"], "04-data-outlives-programs.md"),
    ("Machines need|to talk", ["Data", "DSA", "Trust", "Latency"], "05-machines-need-to-talk.md"),
    ("Anyone can|publish", ["Data", "Trust"], "06-anyone-can-publish.md"),
    ("Strangers on|the network", ["DSA", "Trust"], "07-strangers-on-the-network.md"),
    ("Too many users,|too much data", ["Data", "DSA", "Latency"], "08-too-many-users-too-much-data.md"),
    ("Buying computers|is too slow", ["Trust", "Cost"], "09-buying-computers-is-too-slow.md"),
    ("Many people,|one codebase", ["DSA", "Trust"], "10-many-people-one-codebase.md"),
    ("Software that must|not go down", ["Latency", "Cost"], "11-software-that-must-not-go-down.md"),
    ("Machines that learn|from data", ["Data", "Trust", "Latency", "Cost"], "12-machines-that-learn-from-data.md"),
    ("Everything still|exists at once", list(HUBS), "13-everything-still-exists-at-once.md"),
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
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def strip_md(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def extract_section(text, heading):
    pattern = rf"^## {re.escape(heading)}\n+([\s\S]*?)(?=\n## |\Z)"
    m = re.search(pattern, text, re.M)
    return m.group(1).strip() if m else ""


def resolve_rel_path(source_path, target_href):
    target_clean = target_href.split("#")[0]
    if not target_clean or target_clean.startswith(("http://", "https://")):
        return target_href
    base_dir = posixpath.dirname(source_path)
    joined = posixpath.normpath(posixpath.join(base_dir, target_clean)) if base_dir else posixpath.normpath(target_clean)
    return joined


def parse_connections(source_path, text):
    sec = extract_section(text, "Connections")
    if not sec:
        return []
    edges = []
    for line in sec.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", body)
        because = ""
        if ", because " in body:
            because = strip_md(body.split(", because ", 1)[1])
        elif " because " in body:
            because = strip_md(body.split(" because ", 1)[1])
        else:
            because = strip_md(body)
        if links:
            label, raw_href = links[0]
            resolved = resolve_rel_path(source_path, raw_href)
            edges.append({
                "label": label,
                "href": resolved,
                "raw_href": raw_href,
                "because": because,
            })
        else:
            edges.append({
                "label": "Earlier pages",
                "href": "00-representations.md",
                "raw_href": "00-representations.md",
                "because": because,
            })
    return edges


def parse_all_pages():
    pages = {}
    md_files = sorted(glob.glob("[0-9][0-9]-*.md")) + ["the-model.md", "forces.md", "pushback.md"]
    for folder in FAMILY_META:
        md_files += sorted(glob.glob(f"{folder}/*.md"))

    model_text = open("the-model.md").read() if os.path.exists("the-model.md") else ""
    model_sentences = {}
    for num_str, body in re.findall(r"^(\d+)\. (.*)$", model_text, re.M):
        clean_s = re.sub(r" \(\[\d+\]\([^)]+\)\)$", "", body.strip())
        model_sentences[int(num_str)] = clean_s

    for path in md_files:
        if not os.path.exists(path):
            continue
        raw = open(path).read()
        title_m = re.search(r"^# (.*)$", raw, re.M)
        full_title = title_m.group(1).strip() if title_m else path
        problem = strip_md(extract_section(raw, "Problem"))
        what_survived = strip_md(extract_section(raw, "What survived") or extract_section(raw, "What it is"))
        go_and_look = strip_md(extract_section(raw, "Go and look"))
        connections = parse_connections(path, raw)

        if re.match(r"^\d\d-", path):
            num = int(path[:2])
            kind = "spine"
            family = "spine"
            clean_title = re.sub(r"^\d+\.\s*", "", full_title)
            model_sentence = model_sentences.get(num, "")
        elif "/" in path:
            num = None
            kind = "concept"
            family = path.split("/", 1)[0]
            clean_title = full_title
            model_sentence = ""
        else:
            num = None
            kind = "reference"
            family = "reference"
            clean_title = full_title
            model_sentence = ""

        pages[path] = {
            "path": path,
            "number": num,
            "kind": kind,
            "family": family,
            "title": clean_title,
            "full_title": full_title,
            "problem": problem,
            "what_survived": what_survived,
            "go_and_look": go_and_look,
            "model_sentence": model_sentence,
            "connections": connections,
            "backlinks": [],
        }

    for src_path, page in pages.items():
        for edge in page["connections"]:
            target = edge["href"].split("#")[0]
            if target in pages and target != src_path:
                pages[target]["backlinks"].append({
                    "from_path": src_path,
                    "from_title": page["full_title"],
                    "from_kind": page["kind"],
                    "label": edge["label"],
                    "because": edge["because"],
                })

    return pages


def hub_target_for_page(page_data, hub_name):
    folder = HUB_FOLDERS[hub_name]
    matches = []
    for edge in page_data.get("connections", []):
        target = edge["href"].split("#")[0]
        if target.startswith(folder + "/"):
            matches.append((edge["label"], target))
    if matches:
        return matches[0][1], [m[0] for m in matches]
    if hub_name == "Latency":
        for edge in page_data.get("connections", []):
            if edge["href"].startswith("ai/tokens.md"):
                return "ai/tokens.md", [edge["label"]]
    return HUB_DEFAULT_PAGE[hub_name], [hub_name]


def build_svg(pages):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
        "<style>",
        "  .stop { cursor: pointer; text-decoration: none; }",
        "  .stop circle.node { transition: transform 0.15s ease, fill 0.15s ease, stroke-width 0.15s ease; transform-box: fill-box; transform-origin: center; }",
        "  .stop:hover circle.node { fill: #f6f8fa; stroke-width: 5px; transform: scale(1.12); }",
        "  .stop:hover text.label { text-decoration: underline; fill: #0969da; }",
        "  .hub-dot { cursor: pointer; }",
        "  .hub-dot circle { transition: transform 0.15s ease, stroke 0.15s ease; transform-box: fill-box; transform-origin: center; }",
        "  .hub-dot:hover circle { transform: scale(1.45); stroke: #1f2328; stroke-width: 1.5px; }",
        "  .legend-item { cursor: pointer; text-decoration: none; }",
        "  .legend-item:hover text { text-decoration: underline; fill: #0969da; }",
        "  .legend-item:hover circle { transform: scale(1.25); transform-box: fill-box; transform-origin: center; }",
        "</style>",
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{LEFT - 40}" y="52" font-size="22" font-weight="600" fill="{INK}">The throughline</text>',
        f'<text x="{LEFT - 40}" y="76" font-size="14" fill="{MUTED}">Read the stops in order. '
        "Click any stop or hub dot to open its page.</text>",
    ]

    (x1, y1), (x2, y2) = stop_xy(PER_ROW - 1), stop_xy(PER_ROW)
    r = (y2 - y1) / 2
    path = f"M {stop_xy(0)[0]} {y1} H {x1} A {r} {r} 0 0 1 {x2} {y2} H {stop_xy(len(PAGES) - 1)[0]}"
    out.append(f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')

    for i, (title, hubs, md_path) in enumerate(PAGES):
        x, y = stop_xy(i)
        page_data = pages.get(md_path, {})
        full_title = page_data.get("full_title", f"{i}. {title.replace('|', ' ')}")
        summary = page_data.get("what_survived") or page_data.get("problem") or ""
        tooltip = f"{full_title}" + (f" — {summary}" if summary else "")
        out.append(f'<a class="stop" href="../{md_path}" target="_top">')
        out.append(f'  <title>{esc(tooltip)}</title>')
        out.append(f'  <circle class="node" cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{LINE}" stroke-width="4"/>')
        out.append(f'  <text x="{x}" y="{y + 5}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{i}</text>')
        for j, part in enumerate(title.split("|")):
            out.append(
                f'  <text class="label" x="{x}" y="{y + 40 + j * 17}" font-size="13" text-anchor="middle" fill="{INK}">{esc(part)}</text>'
            )
        out.append("</a>")

        dot_y = y + 40 + len(title.split("|")) * 17 + 4
        start = x - (len(hubs) - 1) * 7
        for k, hub in enumerate(hubs):
            target_md, concept_names = hub_target_for_page(page_data, hub)
            dot_title = f"{hub}: {', '.join(concept_names)} ({target_md})"
            out.append(f'<a class="hub-dot" href="../{target_md}" target="_top">')
            out.append(f'  <title>{esc(dot_title)}</title>')
            out.append(f'  <circle cx="{start + k * 14}" cy="{dot_y}" r="5" fill="{HUBS[hub]}"/>')
            out.append("</a>")

    lx = LEFT - 40
    for hub, colour in HUBS.items():
        default_md = HUB_DEFAULT_PAGE[hub]
        folder = HUB_FOLDERS[hub]
        concept_Count = len([p for p in pages if p.startswith(folder + "/")])
        out.append(f'<a class="legend-item" href="../{default_md}" target="_top">')
        out.append(f'  <title>{esc(f"{hub} hub ({concept_Count} concept pages in {folder}/)")}</title>')
        out.append(f'  <circle cx="{lx + 6}" cy="{H - 34}" r="6" fill="{colour}"/>')
        out.append(f'  <text x="{lx + 18}" y="{H - 29}" font-size="14" fill="{INK}">{hub}</text>')
        out.append("</a>")
        lx += 30 + len(hub) * 9

    out.append("</svg>")
    with open("images/map.svg", "w") as f:
        f.write("\n".join(out) + "\n")


def build_html(pages):
    stops_payload = []
    for i, (title, hubs, md_path) in enumerate(PAGES):
        x, y = stop_xy(i)
        page_data = pages[md_path]
        hub_dots = []
        dot_y = y + 40 + len(title.split("|")) * 17 + 4
        start = x - (len(hubs) - 1) * 7
        for k, hub in enumerate(hubs):
            target_md, concept_names = hub_target_for_page(page_data, hub)
            hub_dots.append({
                "hub": hub,
                "color": HUBS[hub],
                "cx": start + k * 14,
                "cy": dot_y,
                "target": target_md,
                "concepts": concept_names,
            })
        stops_payload.append({
            "index": i,
            "path": md_path,
            "lines": title.split("|"),
            "hubs": hubs,
            "x": x,
            "y": y,
            "dots": hub_dots,
        })

    (x1, y1), (x2, y2) = stop_xy(PER_ROW - 1), stop_xy(PER_ROW)
    r = (y2 - y1) / 2
    svg_path_d = f"M {stop_xy(0)[0]} {y1} H {x1} A {r} {r} 0 0 1 {x2} {y2} H {stop_xy(len(PAGES) - 1)[0]}"

    data_json = json.dumps(
        {
            "pages": pages,
            "stops": stops_payload,
            "hubs": HUBS,
            "hubFolders": HUB_FOLDERS,
            "families": {k: {"label": v[0], "color": v[1]} for k, v in FAMILY_META.items()},
        },
        ensure_ascii=False,
    )

    stops_svg_markup = []
    for s in stops_payload:
        i = s["index"]
        x, y = s["x"], s["y"]
        md_path = s["path"]
        p = pages[md_path]
        stops_svg_markup.append(
            f'<g class="map-stop" data-path="{html.escape(md_path)}" data-hubs="{html.escape(",".join(s["hubs"]))}" tabindex="0" role="button" aria-label="Stop {i}: {html.escape(p["title"])}">'
        )
        stops_svg_markup.append(
            f'  <a href="{html.escape(md_path)}" class="stop-link" data-path="{html.escape(md_path)}">'
        )
        stops_svg_markup.append(f'    <title>{html.escape(p["full_title"])}</title>')
        stops_svg_markup.append(
            f'    <circle class="stop-ring" cx="{x}" cy="{y}" r="21" fill="none" stroke="#0969da" stroke-width="3" opacity="0"/>'
        )
        stops_svg_markup.append(
            f'    <circle class="stop-circle" cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{LINE}" stroke-width="4"/>'
        )
        stops_svg_markup.append(
            f'    <text class="stop-num" x="{x}" y="{y + 5}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">{i}</text>'
        )
        for j, part in enumerate(s["lines"]):
            stops_svg_markup.append(
                f'    <text class="stop-label" x="{x}" y="{y + 40 + j * 17}" font-size="13" text-anchor="middle" fill="{INK}">{html.escape(part)}</text>'
            )
        stops_svg_markup.append("  </a>")
        for d in s["dots"]:
            dot_tip = f'{d["hub"]}: {", ".join(d["concepts"])}'
            stops_svg_markup.append(
                f'  <a href="{html.escape(d["target"])}" class="dot-link" data-path="{html.escape(d["target"])}" data-hub="{html.escape(d["hub"])}">'
            )
            stops_svg_markup.append(f'    <title>{html.escape(dot_tip)}</title>')
            stops_svg_markup.append(
                f'    <circle class="hub-dot-circle" cx="{d["cx"]}" cy="{d["cy"]}" r="5.5" fill="{d["color"]}"/>'
            )
            stops_svg_markup.append("  </a>")
        stops_svg_markup.append("</g>")

    legend_svg_markup = []
    lx = LEFT - 40
    for hub, colour in HUBS.items():
        default_md = HUB_DEFAULT_PAGE[hub]
        legend_svg_markup.append(
            f'<g class="map-legend-item" data-hub="{html.escape(hub)}" role="button" tabindex="0">'
            f'<circle cx="{lx + 6}" cy="{H - 34}" r="6" fill="{colour}"/>'
            f'<text x="{lx + 18}" y="{H - 29}" font-size="14" fill="{INK}">{html.escape(hub)}</text>'
            f"</g>"
        )
        lx += 30 + len(hub) * 9

    spine_cards_html = []
    for s in stops_payload:
        p = pages[s["path"]]
        badges = "".join(
            f'<span class="hub-pill" style="--pill-color:{HUBS[h]}">{html.escape(h)}</span>' for h in s["hubs"]
        )
        spine_cards_html.append(
            f'<div class="spine-card" data-path="{html.escape(p["path"])}">'
            f'  <div class="spine-card-head">'
            f'    <button type="button" class="select-node-btn" data-path="{html.escape(p["path"])}">#{s["index"]} {html.escape(p["title"])}</button>'
            f'    <a class="direct-md-link" href="{html.escape(p["path"])}">Open .md &rarr;</a>'
            f"  </div>"
            f'  <p class="spine-card-desc">{html.escape(p["what_survived"] or p["problem"])}</p>'
            f'  <div class="spine-card-pills">{badges}</div>'
            f"</div>"
        )

    family_sections_html = []
    for folder, (label, color) in FAMILY_META.items():
        concept_pages = [p for p in pages.values() if p["family"] == folder]
        items_html = []
        for cp in concept_pages:
            items_html.append(
                f'<li class="concept-item" data-path="{html.escape(cp["path"])}">'
                f'  <button type="button" class="concept-select-btn" data-path="{html.escape(cp["path"])}">{html.escape(cp["title"])}</button>'
                f'  <a class="concept-md-link" href="{html.escape(cp["path"])}" title="Open {html.escape(cp["path"])}">{html.escape(cp["path"])}</a>'
                f"</li>"
            )
        family_sections_html.append(
            f'<div class="family-card" data-family="{html.escape(folder)}">'
            f'  <div class="family-card-header" style="border-left: 4px solid {color}">'
            f'    <h3>{html.escape(label)} <span class="folder-tag">{html.escape(folder)}/</span></h3>'
            f'    <span class="count-badge">{len(concept_pages)}</span>'
            f"  </div>"
            f'  <ul class="concept-list">{"".join(items_html)}</ul>'
            f"</div>"
        )

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Throughline — Interactive Map</title>
  <style>
    :root {{
      --ink: #1f2328;
      --muted: #59636e;
      --border: #d0d7de;
      --surface: #f6f8fa;
      --accent: #0969da;
      --bg: #ffffff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.5;
    }}
    header {{
      border-bottom: 1px solid var(--border);
      padding: 20px 32px;
      display: flex;
      flex-wrap: wrap;
      align-items: baseline;
      justify-content: space-between;
      gap: 16px;
      background: var(--surface);
    }}
    header h1 {{
      margin: 0;
      font-size: 22px;
      font-weight: 650;
    }}
    header p {{
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 14px;
    }}
    .ref-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}
    .ref-links a, .ref-links button {{
      font-size: 13px;
      color: var(--ink);
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 11px;
      text-decoration: none;
      cursor: pointer;
      font-family: inherit;
    }}
    .ref-links a:hover, .ref-links button:hover {{
      border-color: var(--accent);
      color: var(--accent);
    }}
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px 32px 64px;
    }}
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}
    .hub-filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }}
    .filter-label {{
      font-size: 13px;
      color: var(--muted);
      font-weight: 500;
      margin-right: 4px;
    }}
    .hub-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--border);
      background: #fff;
      color: var(--ink);
      border-radius: 999px;
      padding: 5px 12px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.12s ease;
    }}
    .hub-btn:hover {{
      border-color: var(--ink);
    }}
    .hub-btn.active {{
      background: var(--ink);
      color: #fff;
      border-color: var(--ink);
    }}
    .hub-swatch {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      display: inline-block;
    }}
    .search-box {{
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 13px;
      min-width: 240px;
    }}
    .workspace {{
      display: grid;
      grid-template-columns: minmax(0, 1.55fr) minmax(340px, 1fr);
      gap: 24px;
      align-items: start;
    }}
    @media (max-width: 1024px) {{
      .workspace {{
        grid-template-columns: 1fr;
      }}
    }}
    .map-frame {{
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #fff;
      padding: 8px;
      overflow-x: auto;
      box-shadow: 0 1px 3px rgba(31,35,40,0.04);
    }}
    .map-frame svg {{
      width: 100%;
      height: auto;
      display: block;
    }}
    .map-stop {{
      cursor: pointer;
      transition: opacity 0.18s ease;
    }}
    .map-stop.dimmed {{
      opacity: 0.22;
    }}
    .map-stop .stop-circle {{
      transition: transform 0.15s ease, fill 0.15s ease, stroke 0.15s ease;
      transform-box: fill-box;
      transform-origin: center;
    }}
    .map-stop:hover .stop-circle {{
      transform: scale(1.12);
      fill: #f0f6ff;
    }}
    .map-stop.selected .stop-ring {{
      opacity: 1;
    }}
    .map-stop.selected .stop-circle {{
      fill: #0969da;
      stroke: #0969da;
    }}
    .map-stop.selected .stop-num {{
      fill: #ffffff;
    }}
    .map-stop.selected .stop-label {{
      fill: #0969da;
      font-weight: 600;
    }}
    .map-stop.connected .stop-ring {{
      opacity: 0.45;
      stroke-dasharray: 3 2;
    }}
    .hub-dot-circle {{
      transition: transform 0.15s ease, stroke 0.15s ease;
      transform-box: fill-box;
      transform-origin: center;
    }}
    .dot-link:hover .hub-dot-circle {{
      transform: scale(1.5);
      stroke: #1f2328;
      stroke-width: 1.5px;
    }}
    .map-legend-item {{
      cursor: pointer;
    }}
    .map-legend-item:hover text {{
      fill: var(--accent);
      text-decoration: underline;
    }}
    .inspector {{
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #fff;
      padding: 20px 22px;
      position: sticky;
      top: 16px;
      box-shadow: 0 1px 3px rgba(31,35,40,0.04);
    }}
    .inspector-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
      margin-bottom: 14px;
    }}
    .inspector-kicker {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
      margin-bottom: 4px;
    }}
    .inspector-title {{
      margin: 0;
      font-size: 18px;
      font-weight: 650;
    }}
    .open-page-btn {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--accent);
      color: #fff;
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      padding: 6px 12px;
      border-radius: 6px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .open-page-btn:hover {{
      background: #0550ae;
    }}
    .inspector-section {{
      margin-bottom: 14px;
    }}
    .inspector-section h4 {{
      margin: 0 0 4px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--muted);
    }}
    .inspector-section p {{
      margin: 0;
      font-size: 13.5px;
      color: var(--ink);
    }}
    .model-quote {{
      background: var(--surface);
      border-left: 3px solid var(--ink);
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      font-size: 13px;
    }}
    .edge-list {{
      list-style: none;
      padding: 0;
      margin: 6px 0 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 280px;
      overflow-y: auto;
    }}
    .edge-item {{
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 13px;
      background: #fff;
    }}
    .edge-item-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 3px;
    }}
    .edge-focus-btn {{
      background: none;
      border: none;
      padding: 0;
      color: var(--accent);
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      text-align: left;
      font-family: inherit;
    }}
    .edge-focus-btn:hover {{
      text-decoration: underline;
    }}
    .edge-file-link {{
      font-size: 11.5px;
      color: var(--muted);
      text-decoration: none;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      flex-shrink: 0;
    }}
    .edge-file-link:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}
    .edge-because {{
      color: var(--muted);
      font-size: 12.5px;
      margin: 0;
    }}
    .section-heading {{
      margin: 36px 0 14px;
      font-size: 18px;
      font-weight: 650;
      display: flex;
      align-items: baseline;
      justify-content: space-between;
    }}
    .section-heading span {{
      font-size: 13px;
      font-weight: 400;
      color: var(--muted);
    }}
    .spine-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 12px;
    }}
    .spine-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      background: #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
    }}
    .spine-card.selected {{
      border-color: var(--accent);
      box-shadow: 0 0 0 1px var(--accent);
    }}
    .spine-card.hidden, .family-card.hidden, .concept-item.hidden {{
      display: none;
    }}
    .spine-card-head {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
    }}
    .select-node-btn {{
      background: none;
      border: none;
      padding: 0;
      font-size: 14px;
      font-weight: 600;
      color: var(--ink);
      cursor: pointer;
      text-align: left;
      font-family: inherit;
    }}
    .select-node-btn:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}
    .direct-md-link {{
      font-size: 12px;
      color: var(--accent);
      text-decoration: none;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .direct-md-link:hover {{
      text-decoration: underline;
    }}
    .spine-card-desc {{
      margin: 0;
      font-size: 12.5px;
      color: var(--muted);
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .spine-card-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }}
    .hub-pill {{
      font-size: 11px;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--pill-color) 14%, transparent);
      color: var(--pill-color);
      border: 1px solid color-mix(in srgb, var(--pill-color) 35%, transparent);
    }}
    .families-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 14px;
    }}
    .family-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
      overflow: hidden;
    }}
    .family-card-header {{
      padding: 10px 14px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .family-card-header h3 {{
      margin: 0;
      font-size: 14px;
      font-weight: 600;
    }}
    .folder-tag {{
      font-weight: 400;
      font-size: 12px;
      color: var(--muted);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    .count-badge {{
      font-size: 11px;
      background: #fff;
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 1px 7px;
      color: var(--muted);
    }}
    .concept-list {{
      list-style: none;
      margin: 0;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }}
    .concept-item {{
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      font-size: 13px;
      padding: 3px 4px;
      border-radius: 4px;
    }}
    .concept-item:hover {{
      background: var(--surface);
    }}
    .concept-select-btn {{
      background: none;
      border: none;
      padding: 0;
      font-size: 13px;
      color: var(--ink);
      cursor: pointer;
      text-align: left;
      font-family: inherit;
    }}
    .concept-select-btn:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}
    .concept-md-link {{
      font-size: 11.5px;
      color: var(--muted);
      text-decoration: none;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    .concept-md-link:hover {{
      color: var(--accent);
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Throughline — Interactive Map</h1>
      <p>Fourteen problems in the order they appeared, and the concept hubs they keep returning to.</p>
    </div>
    <nav class="ref-links" aria-label="Reference pages">
      <a href="README.md">README</a>
      <button type="button" class="select-node-btn-nav" data-path="the-model.md">The Model</button>
      <a href="the-model.md">the-model.md</a>
      <button type="button" class="select-node-btn-nav" data-path="forces.md">Forces</button>
      <a href="forces.md">forces.md</a>
      <button type="button" class="select-node-btn-nav" data-path="pushback.md">Pushback</button>
      <a href="pushback.md">pushback.md</a>
      <a href="SPEC.md">SPEC.md</a>
    </nav>
  </header>

  <main>
    <div class="controls-bar">
      <div class="hub-filters" role="toolbar" aria-label="Filter by hub">
        <span class="filter-label">Filter by hub:</span>
        <button type="button" class="hub-btn active" data-hub="all">All stops</button>
        <button type="button" class="hub-btn" data-hub="Data"><span class="hub-swatch" style="background:#2a78d6"></span>Data</button>
        <button type="button" class="hub-btn" data-hub="DSA"><span class="hub-swatch" style="background:#1baa7a"></span>DSA</button>
        <button type="button" class="hub-btn" data-hub="Trust"><span class="hub-swatch" style="background:#d64a4a"></span>Trust</button>
        <button type="button" class="hub-btn" data-hub="Latency"><span class="hub-swatch" style="background:#e09a1a"></span>Latency</button>
        <button type="button" class="hub-btn" data-hub="Cost"><span class="hub-swatch" style="background:#8a5cd6"></span>Cost</button>
      </div>
      <input type="search" id="search-input" class="search-box" placeholder="Search stops, concepts, or problems..." aria-label="Search pages">
    </div>

    <div class="workspace">
      <div class="map-frame">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">
          <rect width="{W}" height="{H}" fill="#ffffff"/>
          <text x="{LEFT - 40}" y="52" font-size="22" font-weight="600" fill="{INK}">The throughline</text>
          <text x="{LEFT - 40}" y="76" font-size="14" fill="{MUTED}">Click a stop or dot to inspect its connections, or Ctrl/Cmd-click to open the page directly.</text>
          <path d="{svg_path_d}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>
          {"".join(stops_svg_markup)}
          {"".join(legend_svg_markup)}
        </svg>
      </div>

      <aside class="inspector" id="inspector" aria-live="polite">
        <div class="inspector-header">
          <div>
            <div class="inspector-kicker" id="ins-kicker">Spine Page</div>
            <h2 class="inspector-title" id="ins-title">0. Humans need representations before they need machines</h2>
          </div>
          <a class="open-page-btn" id="ins-open-link" href="00-representations.md">Read page &rarr;</a>
        </div>

        <div class="inspector-section" id="ins-problem-sec">
          <h4>Problem</h4>
          <p id="ins-problem"></p>
        </div>

        <div class="inspector-section" id="ins-survived-sec">
          <h4 id="ins-survived-heading">What survived</h4>
          <p id="ins-survived"></p>
        </div>

        <div class="inspector-section" id="ins-model-sec">
          <h4>Added to the model</h4>
          <div class="model-quote" id="ins-model"></div>
        </div>

        <div class="inspector-section" id="ins-connections-sec">
          <h4>Connections (<span id="ins-conn-count">0</span>)</h4>
          <ul class="edge-list" id="ins-connections"></ul>
        </div>

        <div class="inspector-section" id="ins-backlinks-sec">
          <h4>Connected from (<span id="ins-back-count">0</span>)</h4>
          <ul class="edge-list" id="ins-backlinks"></ul>
        </div>
      </aside>
    </div>

    <h2 class="section-heading">The Spine (0&ndash;13) <span>Click a card to inspect connections, or "Open .md" to read the story</span></h2>
    <div class="spine-grid" id="spine-grid">
      {"".join(spine_cards_html)}
    </div>

    <h2 class="section-heading">Concept Hubs &amp; Branches <span>{sum(1 for p in pages.values() if p["kind"] == "concept")} concept pages across {len(FAMILY_META)} folders</span></h2>
    <div class="families-grid" id="families-grid">
      {"".join(family_sections_html)}
    </div>
  </main>

  <script>
    const DATA = {data_json};
    let activeHub = "all";
    let selectedPath = "00-representations.md";

    function selectNode(rawPath, updateHash = true) {{
      const cleanPath = rawPath.split("#")[0];
      const page = DATA.pages[cleanPath];
      if (!page) return;
      selectedPath = cleanPath;
      if (updateHash) {{
        history.replaceState(null, "", "#" + cleanPath);
      }}

      const kicker = document.getElementById("ins-kicker");
      if (page.kind === "spine") {{
        kicker.textContent = `Spine Stop #${{page.number}} · ${{page.path}}`;
      }} else if (page.kind === "concept") {{
        const fam = DATA.families[page.family];
        kicker.textContent = `${{fam ? fam.label : page.family}} Concept · ${{page.path}}`;
      }} else {{
        kicker.textContent = `Reference · ${{page.path}}`;
      }}

      document.getElementById("ins-title").textContent = page.full_title;
      const openLink = document.getElementById("ins-open-link");
      openLink.href = page.path;
      openLink.textContent = `Open ${{page.path}} →`;

      const probSec = document.getElementById("ins-problem-sec");
      if (page.problem) {{
        probSec.style.display = "";
        document.getElementById("ins-problem").textContent = page.problem;
      }} else {{
        probSec.style.display = "none";
      }}

      const survSec = document.getElementById("ins-survived-sec");
      if (page.what_survived) {{
        survSec.style.display = "";
        document.getElementById("ins-survived-heading").textContent =
          page.kind === "concept" ? "What it is" : "What survived";
        document.getElementById("ins-survived").textContent = page.what_survived;
      }} else {{
        survSec.style.display = "none";
      }}

      const modelSec = document.getElementById("ins-model-sec");
      if (page.model_sentence) {{
        modelSec.style.display = "";
        document.getElementById("ins-model").textContent = page.model_sentence;
      }} else {{
        modelSec.style.display = "none";
      }}

      const connList = document.getElementById("ins-connections");
      connList.innerHTML = "";
      document.getElementById("ins-conn-count").textContent = page.connections.length;
      document.getElementById("ins-connections-sec").style.display =
        page.connections.length ? "" : "none";

      const connectedPaths = new Set();
      page.connections.forEach((edge) => {{
        const targetClean = edge.href.split("#")[0];
        connectedPaths.add(targetClean);
        const li = document.createElement("li");
        li.className = "edge-item";
        const top = document.createElement("div");
        top.className = "edge-item-top";

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "edge-focus-btn";
        btn.textContent = edge.label;
        btn.addEventListener("click", () => selectNode(targetClean));

        const link = document.createElement("a");
        link.className = "edge-file-link";
        link.href = edge.href;
        link.textContent = edge.href;

        top.appendChild(btn);
        top.appendChild(link);
        li.appendChild(top);

        if (edge.because) {{
          const p = document.createElement("p");
          p.className = "edge-because";
          p.textContent = "Because " + edge.because;
          li.appendChild(p);
        }}
        connList.appendChild(li);
      }});

      const backList = document.getElementById("ins-backlinks");
      backList.innerHTML = "";
      document.getElementById("ins-back-count").textContent = page.backlinks.length;
      document.getElementById("ins-backlinks-sec").style.display =
        page.backlinks.length ? "" : "none";

      page.backlinks.forEach((back) => {{
        connectedPaths.add(back.from_path);
        const li = document.createElement("li");
        li.className = "edge-item";
        const top = document.createElement("div");
        top.className = "edge-item-top";

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "edge-focus-btn";
        btn.textContent = back.from_title;
        btn.addEventListener("click", () => selectNode(back.from_path));

        const link = document.createElement("a");
        link.className = "edge-file-link";
        link.href = back.from_path;
        link.textContent = back.from_path;

        top.appendChild(btn);
        top.appendChild(link);
        li.appendChild(top);

        if (back.because) {{
          const p = document.createElement("p");
          p.className = "edge-because";
          p.textContent = "Because " + back.because;
          li.appendChild(p);
        }}
        backList.appendChild(li);
      }});

      document.querySelectorAll(".map-stop").forEach((el) => {{
        const p = el.getAttribute("data-path");
        el.classList.toggle("selected", p === cleanPath);
        el.classList.toggle("connected", p !== cleanPath && connectedPaths.has(p));
      }});

      document.querySelectorAll(".spine-card").forEach((el) => {{
        el.classList.toggle("selected", el.getAttribute("data-path") === cleanPath);
      }});
    }}

    function setHubFilter(hub) {{
      activeHub = hub;
      document.querySelectorAll(".hub-btn").forEach((btn) => {{
        btn.classList.toggle("active", btn.getAttribute("data-hub") === hub);
      }});
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById("search-input").value.trim().toLowerCase();
      document.querySelectorAll(".map-stop").forEach((el) => {{
        const hubs = (el.getAttribute("data-hubs") || "").split(",");
        const path = el.getAttribute("data-path");
        const page = DATA.pages[path];
        const matchesHub = activeHub === "all" || hubs.includes(activeHub);
        const matchesQuery =
          !query ||
          page.full_title.toLowerCase().includes(query) ||
          page.problem.toLowerCase().includes(query) ||
          page.what_survived.toLowerCase().includes(query);
        el.classList.toggle("dimmed", !(matchesHub && matchesQuery));
      }});

      document.querySelectorAll(".spine-card").forEach((el) => {{
        const path = el.getAttribute("data-path");
        const stop = DATA.stops.find((s) => s.path === path);
        const page = DATA.pages[path];
        const matchesHub = activeHub === "all" || (stop && stop.hubs.includes(activeHub));
        const matchesQuery =
          !query ||
          page.full_title.toLowerCase().includes(query) ||
          page.problem.toLowerCase().includes(query) ||
          page.what_survived.toLowerCase().includes(query);
        el.classList.toggle("hidden", !(matchesHub && matchesQuery));
      }});

      const targetFolder = activeHub === "all" ? null : DATA.hubFolders[activeHub];
      document.querySelectorAll(".family-card").forEach((card) => {{
        const folder = card.getAttribute("data-family");
        const matchesHub = !targetFolder || folder === targetFolder;
        let visibleCount = 0;
        card.querySelectorAll(".concept-item").forEach((item) => {{
          const path = item.getAttribute("data-path");
          const page = DATA.pages[path];
          const matchesQuery =
            !query ||
            page.full_title.toLowerCase().includes(query) ||
            page.problem.toLowerCase().includes(query) ||
            page.what_survived.toLowerCase().includes(query) ||
            path.toLowerCase().includes(query);
          const show = matchesHub && matchesQuery;
          item.classList.toggle("hidden", !show);
          if (show) visibleCount++;
        }});
        card.classList.toggle("hidden", visibleCount === 0);
      }});
    }}

    document.querySelectorAll(".stop-link, .dot-link").forEach((link) => {{
      link.addEventListener("click", (e) => {{
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
        e.preventDefault();
        const target = link.getAttribute("data-path");
        if (target) selectNode(target);
      }});
    }});

    document.querySelectorAll(".map-legend-item").forEach((el) => {{
      el.addEventListener("click", () => {{
        const hub = el.getAttribute("data-hub");
        setHubFilter(activeHub === hub ? "all" : hub);
      }});
    }});

    document.querySelectorAll(".hub-btn").forEach((btn) => {{
      btn.addEventListener("click", () => setHubFilter(btn.getAttribute("data-hub")));
    }});

    document.querySelectorAll(".select-node-btn, .concept-select-btn, .select-node-btn-nav").forEach((btn) => {{
      btn.addEventListener("click", () => {{
        selectNode(btn.getAttribute("data-path"));
        document.getElementById("inspector").scrollIntoView({{ behavior: "smooth", block: "nearest" }});
      }});
    }});

    document.getElementById("search-input").addEventListener("input", applyFilters);

    const initialHash = window.location.hash.replace(/^#/, "");
    if (initialHash && DATA.pages[initialHash]) {{
      selectNode(initialHash, false);
    }} else {{
      selectNode("00-representations.md", false);
    }}
  </script>
</body>
</html>
"""
    with open("map.html", "w") as f:
        f.write(html_doc)


def main():
    pages = parse_all_pages()
    build_svg(pages)
    build_html(pages)


if __name__ == "__main__":
    main()
