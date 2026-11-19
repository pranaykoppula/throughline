"""Check that the families hang together: every concept page is reachable from the spine, and every family index is complete.

Run from the repo root: python3 scripts/check_links.py
Fails if
- a folder of pages isn't listed in families.py,
- a concept page isn't linked from any spine page's body (the guide pages in GUIDES are exempt),
- a family's README.md doesn't list every page in its folder exactly once, or lists one that isn't there.
"""

import glob
import os
import posixpath
import re
import sys

from families import FAMILIES

GUIDES = {"dsa/choosing.md"}
LINK = re.compile(r"\]\(([^)\s]+)\)")


def links(path, text):
    for href in LINK.findall(text):
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        yield posixpath.normpath(posixpath.join(posixpath.dirname(path), href.split("#")[0]))


def main():
    errors = []

    folders = {p.split("/")[0] for p in glob.glob("*/*.md")}
    for folder in sorted(folders - set(FAMILIES)):
        errors.append(f"{folder}/ has pages but isn't a family in scripts/families.py")

    from_spine = set()
    for path in glob.glob("[0-9][0-9]-*.md"):
        body = open(path).read().split("## The model so far", 1)[0]
        from_spine.update(links(path, body))

    for folder in FAMILIES:
        pages = sorted(p for p in glob.glob(f"{folder}/*.md") if not p.endswith("/README.md"))
        for page in pages:
            if page not in from_spine and page not in GUIDES:
                errors.append(f"{page} isn't linked from any spine page")

        index = f"{folder}/README.md"
        if not os.path.exists(index):
            errors.append(f"{index} is missing")
            continue
        listed = [p for p in links(index, open(index).read()) if posixpath.dirname(p) == folder]
        for page in pages:
            n = listed.count(page)
            if n != 1:
                errors.append(f"{index} lists {page} {n} times, not once")
        for page in sorted(set(listed) - set(pages)):
            errors.append(f"{index} lists {page}, which doesn't exist")

    for e in errors:
        print(e)
    if errors:
        sys.exit(1)
    print(f"Links: {len(FAMILIES)} families, every concept page reachable from the spine, every index complete.")


if __name__ == "__main__":
    main()
