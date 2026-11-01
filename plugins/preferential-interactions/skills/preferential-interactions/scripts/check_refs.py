#!/usr/bin/env python3
"""Check cross-references, file links and DOIs in this skill.

Run after editing any reference file:  python3 scripts/check_refs.py
Exit status 1 on any problem.

Conventions it enforces (they keep file links and paper citations apart):
- A link to another file is written "file.md §N".
- A bare "§N" means a section of the same file.
- A section of a cited paper is written with its year: "Ploetz & Smith 2013, §16".
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
YEAR = re.compile(r"(?:19|20)\d\d[a-z]?\)?,?\s*$")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s;,)|`\]]+")


def sections(path):
    return {int(m) for m in re.findall(r"(?m)^## (\d+)\.", path.read_text())}


def main():
    problems = []
    md = sorted(REFS.glob("*.md"))
    secs = {p.name: sections(p) for p in md}
    bib = (REFS / "references.bib").read_text().lower()
    skill = (ROOT / "SKILL.md").read_text()

    for name in secs:
        if f"references/{name}" not in skill:
            problems.append(f"SKILL.md: references/{name} is not listed")
    for name in set(re.findall(r"references/([\w.-]+\.(?:md|bib))", skill)):
        if not (REFS / name).exists():
            problems.append(f"SKILL.md: references/{name} does not exist")

    for path in [ROOT / "SKILL.md", *md]:
        own = secs.get(path.name, set())
        for i, line in enumerate(path.read_text().splitlines(), 1):
            where = f"{path.relative_to(ROOT)}:{i}"
            for m in re.finditer(r"([\w-]+\.md) §(\d+)(\.\d+)?", line):
                target, n = m.group(1), int(m.group(2))
                if m.group(3):
                    problems.append(f"{where}: {target} has no subsections; '§{n}{m.group(3)}' "
                                    "is probably a paper section")
                if re.search(r"(?:[A-Z][a-zé-]+|et al\.|(?:19|20)\d\d[a-z]?|[\w-]+\.md),? $",
                             line[: m.start()]):
                    problems.append(f"{where}: '{m.group(0)}' follows an author, year or file name; "
                                    "probably a paper section rewritten as a file link")
                if target not in secs:
                    problems.append(f"{where}: link to unknown file {target}")
                elif n not in secs[target]:
                    problems.append(f"{where}: {target} has no §{n}")
            for m in re.finditer(r"(?<!§)§(\d+)", line):
                before = line[: m.start()]
                if re.search(r"[\w-]+\.md $", before):
                    continue  # file link, checked above
                if YEAR.search(before):
                    continue  # paper section: "Author 2013, §16"
                n = int(m.group(1))
                if path.name == "SKILL.md":
                    # index rows: "§N" labels a section of a file named on the same line
                    named = re.findall(r"references/([\w-]+\.md)", line)
                    if any(n in secs.get(f, ()) for f in named):
                        continue
                if path.name == "SKILL.md" or n not in own:
                    problems.append(
                        f"{where}: bare §{n} is not a section of this file; "
                        "write 'file.md §N' or 'Author Year, §N'"
                    )
            for doi in DOI.findall(line):
                doi = doi.rstrip(".")
                if doi.lower() not in bib:
                    problems.append(f"{where}: DOI {doi} not in references.bib")

    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
