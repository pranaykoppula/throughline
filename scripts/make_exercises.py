"""Copy each exercise's solutions into its page, as a box with one tab per language.

Run from the repo root: python3 scripts/make_exercises.py
Each exercise page exercises/<area>/<slug>.md has its code in exercises/<area>/code/<slug>/:
solution.py, solution.cpp, Solution.java, solution.go and solution.rs, plus the test drivers
that scripts/test_exercises.py uses. Between the markers

    <!-- code:start -->
    <!-- code:end -->

this script writes one collapsible block per language. On GitHub they show as five sections you
can open; on the published site, _includes/head-custom.html turns them into tabs. Never edit the
code on the page: edit the files and run this again. CI fails if a page is out of date.
"""

import glob
import os
import re
import sys

LANGUAGES = [
    ("Python", "python", "solution.py"),
    ("C++", "cpp", "solution.cpp"),
    ("Java", "java", "Solution.java"),
    ("Go", "go", "solution.go"),
    ("Rust", "rust", "solution.rs"),
]
START, END = "<!-- code:start -->", "<!-- code:end -->"


def shown(lang, text):
    """The part of a solution file a reader should see: drop Go's package line, which LeetCode supplies."""
    lines = text.rstrip("\n").split("\n")
    if lang == "go" and lines and lines[0].startswith("package "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines)


def block(code_dir):
    out = [START, '<div class="code-tabs" markdown="1">', ""]
    for name, lang, filename in LANGUAGES:
        path = os.path.join(code_dir, filename)
        if not os.path.exists(path):
            sys.exit(f"{path} is missing")
        out += [f'<details markdown="1"><summary>{name}</summary>', "", f"```{lang}",
                shown(lang, open(path).read()), "```", "", "</details>", ""]
    out += ["</div>", END]
    return "\n".join(out)


def main():
    pages = sorted(glob.glob("exercises/*/*.md"))
    count = 0
    for page in pages:
        if page.endswith("/README.md"):
            continue
        text = open(page).read()
        if START not in text:
            continue
        area, slug = page.split("/")[1], os.path.basename(page)[:-3]
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block(f"exercises/{area}/code/{slug}"),
                     text, flags=re.S)
        if new != text:
            open(page, "w").write(new)
        count += 1
    print(f"exercises: {count} pages with code.")


if __name__ == "__main__":
    main()
