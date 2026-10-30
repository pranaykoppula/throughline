"""Draw graph.html: every page as a node and every link between pages as an edge, in the style of Obsidian's graph view.

Run from the repo root: python3 scripts/make_graph.py
Nothing to edit by hand: the graph is read from the pages' links. Rerun after adding a page or a link.
Links to pages that don't exist yet are drawn as hollow nodes: the frontier.
"""

import glob
import json
import os
import posixpath
import re
import subprocess

FAMILIES = {
    "spine": ("Spine", "#e6edf3"),
    "reference": ("Reference", "#f0b72f"),
    "data": ("Data", "#2a78d6"),
    "dsa": ("DSA", "#1baa7a"),
    "auth": ("Trust", "#d64a4a"),
    "latency": ("Latency", "#e09a1a"),
    "cost": ("Cost", "#8a5cd6"),
    "math": ("Math", "#4fb3d9"),
    "runtimes": ("Runtimes", "#d6559f"),
    "tooling": ("Tooling", "#7fbf3f"),
    "vendors": ("Vendors", "#b08a5a"),
    "cloud": ("Cloud", "#5ac8b8"),
    "ai": ("AI", "#a371f7"),
    "writing": ("Writing", "#8b949e"),
}

REFERENCE = ["the-model.md", "forces.md", "pushback.md"]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def blob_base():
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""
    m = re.match(r"(?:https://github\.com/|git@github\.com:)([^/]+/[^/.]+)", url)
    return f"https://github.com/{m.group(1)}/blob/HEAD/" if m else ""


def family_of(path):
    if re.match(r"^\d\d-", path):
        return "spine"
    if path in REFERENCE:
        return "reference"
    return path.split("/", 1)[0]


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\n+([\s\S]*?)(?=\n## |\Z)", text, re.M)
    return m.group(1).strip() if m else ""


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"\*+|`|<!--.*?-->", "", text).strip()


def first_sentence(text):
    text = plain(text).split("\n\n")[0].replace("\n", " ")
    m = re.match(r"(.+?[.?!])(\s|$)", text)
    return m.group(1) if m else text


def main():
    paths = sorted(glob.glob("[0-9][0-9]-*.md")) + REFERENCE
    paths += sorted(p for f in FAMILIES if f not in ("spine", "reference") for p in glob.glob(f"{f}/*.md"))

    nodes, links = {}, set()
    for path in paths:
        text = open(path).read()
        title = re.search(r"^# (.*)$", text, re.M).group(1).strip()
        nodes[path] = {
            "id": path,
            "title": title,
            "family": family_of(path),
            "summary": first_sentence(section(text, "Problem")),
            "exists": True,
        }
        body = text.split("## The model so far", 1)[0]
        for href in LINK.findall(body):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), href.split("#")[0]))
            if not target.endswith(".md") or target == path or target in ("README.md", "SPEC.md"):
                continue
            links.add(tuple(sorted((path, target))))

    for a, b in links:
        for end in (a, b):
            if end not in nodes:
                nodes[end] = {
                    "id": end,
                    "title": posixpath.basename(end)[:-3].replace("-", " "),
                    "family": family_of(end) if "/" in end else "reference",
                    "summary": "Not written yet.",
                    "exists": os.path.exists(end),
                }

    spine = sorted(p for p in nodes if nodes[p]["family"] == "spine")
    data = {
        "base": blob_base(),
        "families": {k: {"label": v[0], "color": v[1]} for k, v in FAMILIES.items()},
        "nodes": list(nodes.values()),
        "links": [{"source": a, "target": b} for a, b in sorted(links)],
        "trunk": [{"source": a, "target": b} for a, b in zip(spine, spine[1:])],
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = open("scripts/graph_template.html").read()
    with open("graph.html", "w") as f:
        f.write(template.replace("/*DATA*/null", payload))
    print(f"graph.html: {len(nodes)} pages, {len(links)} links.")


if __name__ == "__main__":
    main()
