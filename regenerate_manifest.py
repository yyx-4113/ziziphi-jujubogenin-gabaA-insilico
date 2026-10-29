#!/usr/bin/env python3
"""Regenerate MANIFEST.md row table from `git ls-files` (SHA-256 + bytes).

The header (introduction + table header) and footer are preserved verbatim;
only the data rows are rebuilt so every deposited file is SHA-256 listed,
including the six newly tracked tleap-built mutant starting coordinates.
"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MF = os.path.join(HERE, "MANIFEST.md")


def sha256_bytes_index(path):
    """Hash the exact content git will COMMIT (the index blob), so the SHA and
    byte count are independent of working-tree line-ending conversion
    (autocrlf). This is the content a fresh clone checks out, so MANIFEST stays
    valid on every machine. `path` must be repository-relative.
    """
    raw = subprocess.check_output(["git", "cat-file", "blob", ":" + path], cwd=HERE)
    return hashlib.sha256(raw).hexdigest(), len(raw)


def main():
    files = subprocess.check_output(
        ["git", "ls-files"], cwd=HERE).decode("utf-8").splitlines()
    rows = []
    for f in sorted(files):
        fp = os.path.join(HERE, f)
        if not os.path.isfile(fp):
            print("SKIP (not a file):", f, file=sys.stderr)
            continue
        sha, size = sha256_bytes_index(f)
        rows.append((f, sha, size))

    old = open(MF, encoding="utf-8").read().splitlines()
    sep = next(i for i, l in enumerate(old) if l.startswith("|---"))
    footer_start = old.index(
        "This manifest does not list itself. Verify with "
        "`sha256sum` over the rows above.")
    header = "\n".join(old[:sep + 1])
    footer = "\n".join(old[footer_start:])

    out = header + "\n"
    for f, h, b in rows:
        out += "| %s | %s | %d |\n" % (f, h, b)
    out += footer + "\n"

    with open(MF, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    print("Wrote %d manifest rows" % len(rows))


if __name__ == "__main__":
    main()
