"""Run every exercise's solution, in every language, against its tests.

Run from the repo root: python3 scripts/test_exercises.py [slug ...] [--lang python,cpp,java,go,rust]
Each exercises/<area>/code/<slug>/ holds:
- the five solutions shown on the page (solution.py, solution.cpp, Solution.java, solution.go, solution.rs);
- a small driver per language that reads one test from standard input, calls the solution and prints
  the answer (driver.py, driver.cpp, Main.java, main.go, driver.rs); drivers aren't shown on the page;
- tests.json: a list of {"name", "input", "output"}, with input and output as plain text.
Outputs are compared after trimming trailing whitespace on each line. Exits non-zero on any failure.
Needs python3, g++, javac and java, go, and rustc on the PATH.
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

ALL = ["python", "cpp", "java", "go", "rust"]


def build(lang, src, out):
    """Compile one exercise's solution and driver; return the command that runs it."""
    if lang == "python":
        return [sys.executable, os.path.join(src, "driver.py")]
    if lang == "cpp":
        exe = os.path.join(out, "cpp")
        subprocess.run(["g++", "-std=c++17", "-O2", "-o", exe, os.path.join(src, "driver.cpp")], check=True)
        return [exe]
    if lang == "java":
        cls = os.path.join(out, "java")
        os.makedirs(cls, exist_ok=True)
        subprocess.run(["javac", "-d", cls, os.path.join(src, "Solution.java"), os.path.join(src, "Main.java")],
                       check=True, stderr=subprocess.DEVNULL if os.environ.get("QUIET") else None)
        return ["java", "-cp", cls, "Main"]
    if lang == "go":
        exe = os.path.join(out, "go")
        subprocess.run(["go", "build", "-o", exe, os.path.join(src, "main.go"), os.path.join(src, "solution.go")],
                       check=True, env={**os.environ, "GO111MODULE": "off"})
        return [exe]
    if lang == "rust":
        exe = os.path.join(out, "rust")
        subprocess.run(["rustc", "-O", "--edition", "2021", "-A", "dead_code", "-o", exe, os.path.join(src, "driver.rs")],
                       check=True)
        return [exe]
    raise ValueError(lang)


def norm(text):
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--lang", default=",".join(ALL))
    args = ap.parse_args()
    langs = args.lang.split(",")

    dirs = sorted(d for d in glob.glob("exercises/*/code/*") if os.path.isdir(d))
    if args.slugs:
        dirs = [d for d in dirs if os.path.basename(d) in args.slugs]
    failures, runs = [], 0
    for src in dirs:
        slug = os.path.basename(src)
        tests = json.load(open(os.path.join(src, "tests.json")))
        for lang in langs:
            out = tempfile.mkdtemp()
            try:
                cmd = build(lang, src, out)
            except subprocess.CalledProcessError:
                failures.append(f"{slug} [{lang}]: did not compile")
                continue
            for t in tests:
                runs += 1
                r = subprocess.run(cmd, input=t["input"], capture_output=True, text=True, timeout=60)
                if r.returncode != 0 or norm(r.stdout) != norm(t["output"]):
                    got = r.stdout.strip()[:200] or r.stderr.strip()[:200]
                    failures.append(f"{slug} [{lang}] {t['name']}: expected {t['output'].strip()[:200]!r}, got {got!r}")
            shutil.rmtree(out, ignore_errors=True)
    for f in failures:
        print(f)
    if failures:
        sys.exit(1)
    print(f"exercises: {len(dirs)} exercises, {len(langs)} languages, {runs} test runs passed.")


if __name__ == "__main__":
    main()
