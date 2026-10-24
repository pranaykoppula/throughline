"""Check that every copy of the model matches the-model.md.

The model's sentences live in the-model.md, in SPEC.md section 4, and at the
end of every spine page, which carries sentences 0 to its own number with its
own sentence in bold. This script reports any copy that has drifted.

Run from the repo root: python3 scripts/check_model.py
Exits 1 if anything differs.
"""

import glob
import re
import sys

ITEM = re.compile(r"^(\d+)\. (.*)$", re.M)


def items(text):
    return {int(n): body.strip() for n, body in ITEM.findall(text)}


def opening_after(text, marker):
    labelled = re.search(r"^\*\*Opening\.\*\* (.*)$", text, re.M)
    if labelled:
        return labelled.group(1).strip()
    for line in text.split(marker, 1)[1].splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "New on this page", "Last reviewed", "This is what")):
            return line.removeprefix("**Opening.** ")
    return ""


def canonical():
    text = open("the-model.md").read()
    body = text.split("\n", 1)[1]
    sentences = {n: re.sub(r" \(\[\d+\]\([^)]+\)\)$", "", s) for n, s in items(body).items()}
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    opening = next(p for p in paras if not p.startswith(("Last reviewed", "This is what")) and not ITEM.match(p))
    return opening, sentences


def check(name, opening, got_opening, sentences, got, bold=None):
    problems = []
    if got_opening != opening:
        problems.append(f"{name}: opening differs")
    for n, want in sentences.items():
        if n not in got:
            problems.append(f"{name}: sentence {n} missing")
            continue
        text = got[n]
        marked = text.startswith("**") and text.endswith("**")
        if text.startswith("**") != text.endswith("**"):
            problems.append(f"{name}: sentence {n} has unbalanced bold markers")
        elif bold is not None and marked != (n == bold):
            problems.append(f"{name}: sentence {n} should {'' if n == bold else 'not '}be bold")
        if text.strip("*") != want:
            problems.append(f"{name}: sentence {n} differs\n    want: {want}\n    got:  {text.strip('*')}")
    for n in sorted(set(got) - set(sentences)):
        problems.append(f"{name}: unexpected sentence {n}")
    return problems


def main():
    opening, sentences = canonical()
    problems = []

    spec = open("SPEC.md").read()
    section = spec.split("## 4. The model", 1)[1].split("\n## ", 1)[0]
    problems += check("SPEC.md", opening, opening_after(section, "\n"), sentences, items(section))

    for path in sorted(glob.glob("[0-9][0-9]-*.md")):
        number = int(path[:2])
        text = open(path).read()
        if "## The model so far" not in text:
            problems.append(f"{path}: no 'The model so far' section")
            continue
        section = text.split("## The model so far", 1)[1]
        want = {n: s for n, s in sentences.items() if n <= number}
        problems += check(path, opening, opening_after(section, "\n"), want, items(section), bold=number)

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"Model consistent: the-model.md, SPEC.md and {len(glob.glob('[0-9][0-9]-*.md'))} spine pages.")


if __name__ == "__main__":
    main()
