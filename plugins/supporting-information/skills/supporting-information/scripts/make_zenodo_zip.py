# SPDX-License-Identifier: MIT
"""Build a Zenodo deposit as several archives that unpack into one folder.

    python make_zenodo_zip.py --name NAME --part trajectories='systems/**/*.xtc' [--part ...]

- `<name>-<part>-<id>.zip` per `--part`: untracked large files matching its globs.
- `<name>-<version>-<commit>.zip`: everything committed.

`<id>` is drawn from the contents, so an unchanged part keeps its name and a new Zenodo version can
import it instead of uploading it again. Each archive carries its own checksum manifest
(SHA256SUMS, SHA256SUMS-<part>) so unpacking them together overwrites nothing. Archives
must match one commit, so the script refuses to run with uncommitted changes.
"""

import argparse
import hashlib
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

# Already compressed: deflating again costs time and saves nothing.
STORED = {
    ".xtc",
    ".trr",
    ".dcd",
    ".npz",
    ".gz",
    ".bz2",
    ".xz",
    ".zip",
    ".png",
    ".jpg",
    ".pdf",
}


def git(root, *args):
    """Run git in `root` and return stdout."""
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout


def sha256(path):
    """Hex SHA256 of a file, read in chunks so large trajectories fit in memory."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_id(sums):
    """Short id from member paths and checksums; stable across rebuilds of identical data."""
    text = "".join(f"{digest}  {name}\n" for name, digest in sorted(sums.items()))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def version(root):
    """Project version from pyproject.toml, else 'untagged'."""
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        with pyproject.open("rb") as f:
            return tomllib.load(f).get("project", {}).get("version", "untagged")
    return "untagged"


def write(out, root, prefix, files, sums, manifest):
    """Write one archive of `files` under `prefix/`, plus a checksum manifest, then verify it."""
    listing = "".join(f"{sums[p]}  {p}\n" for p in sorted(sums))
    with zipfile.ZipFile(out, "w", allowZip64=True) as archive:
        archive.writestr(
            f"{prefix}/{manifest}", listing, compress_type=zipfile.ZIP_DEFLATED
        )
        for name in files:
            path = root / name
            method = (
                zipfile.ZIP_STORED if path.suffix in STORED else zipfile.ZIP_DEFLATED
            )
            archive.write(path, f"{prefix}/{name}", compress_type=method)
    with zipfile.ZipFile(out) as archive:
        for name in files:
            digest = hashlib.sha256()
            with archive.open(f"{prefix}/{name}") as member:
                for chunk in iter(lambda: member.read(1 << 20), b""):
                    digest.update(chunk)
            if digest.hexdigest() != sums[name]:
                sys.exit(f"checksum mismatch for {name} in {out}")


def parse_part(text):
    """Split 'label=glob1,glob2' into (label, [globs])."""
    label, sep, globs = text.partition("=")
    if not sep or not label or not globs:
        raise argparse.ArgumentTypeError(f"expected label=glob[,glob], got {text!r}")
    return label, globs.split(",")


def main(argv=None):
    """Build the archives and print their names and sizes."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--name", required=True, help="deposit name; archives unpack into it"
    )
    parser.add_argument(
        "--part",
        type=parse_part,
        action="append",
        default=[],
        help="label=glob[,glob] of untracked files, relative to the repo root",
    )
    parser.add_argument(
        "--out", type=Path, default=Path("dist"), help="output directory"
    )
    args = parser.parse_args(argv)

    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
    if git(root, "status", "--porcelain", "--untracked-files=no").strip():
        sys.exit("uncommitted changes: commit first so the archives match one commit")
    tracked = set(git(root, "ls-files").splitlines())
    out = args.out if args.out.is_absolute() else root / args.out
    out.mkdir(parents=True, exist_ok=True)

    archives = []
    for label, globs in args.part:
        files = sorted(
            {
                p.relative_to(root).as_posix()
                for g in globs
                for p in root.glob(g)
                if p.is_file()
            }
            - tracked
        )
        if not files:
            sys.exit(f"part {label!r}: no untracked files match {globs}")
        sums = {name: sha256(root / name) for name in files}
        path = out / f"{args.name}-{label}-{content_id(sums)}.zip"
        write(path, root, args.name, files, sums, f"SHA256SUMS-{label}")
        archives.append(path)

    files = sorted(n for n in tracked if (root / n).is_file())
    sums = {name: sha256(root / name) for name in files}
    commit = git(root, "rev-parse", "--short", "HEAD").strip()
    path = out / f"{args.name}-{version(root)}-{commit}.zip"
    write(path, root, args.name, files, sums, "SHA256SUMS")
    archives.append(path)

    for path in archives:
        print(f"{path.stat().st_size / 1e6:10.1f} MB  {path.relative_to(root)}")


if __name__ == "__main__":
    main()
