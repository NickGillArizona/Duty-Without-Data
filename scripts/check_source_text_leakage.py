"""Fail if a release candidate contains non-distributed opinion text.

The public archive publishes an opinion-source manifest, identifiers, URLs, and
normalized hashes. It intentionally does not distribute the underlying case texts.
This guard checks tracked files plus untracked, non-ignored files for:

1. forbidden source-text directory names;
2. filenames matching a registered source-file identifier; and
3. raw or LF-normalized SHA-256 values matching a registered opinion-text hash.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = REPO / "opinion_sources.csv"
FORBIDDEN_PARTS = {
    "case_texts",
    "case-texts",
    "opinion_texts",
    "opinion-texts",
    "source_texts",
    "source-texts",
}


def git_release_files() -> list[pathlib.Path]:
    commands = (
        ["git", "ls-files", "-z"],
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
    )
    paths: set[pathlib.Path] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=REPO,
            capture_output=True,
            check=True,
        )
        for raw_path in result.stdout.split(b"\0"):
            if raw_path:
                paths.add(REPO / raw_path.decode("utf-8", errors="surrogateescape"))
    return sorted(paths)


def registered_sources() -> tuple[set[str], set[str]]:
    names: set[str] = set()
    hashes: set[str] = set()
    with SOURCE_MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            source_file = (row.get("source_file") or "").strip()
            digest = (row.get("sha256_lf") or "").strip().lower()
            if source_file:
                names.add(source_file.casefold())
            if len(digest) == 64 and all(char in "0123456789abcdef" for char in digest):
                hashes.add(digest)
    return names, hashes


def content_hashes(path: pathlib.Path) -> set[str]:
    data = path.read_bytes()
    lf_data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {
        hashlib.sha256(data).hexdigest(),
        hashlib.sha256(lf_data).hexdigest(),
    }


def path_reason(relative: pathlib.PurePath, source_names: set[str]) -> str | None:
    folded_parts = {part.casefold() for part in relative.parts}
    forbidden = folded_parts & FORBIDDEN_PARTS
    if forbidden:
        return f"forbidden source-text path component: {sorted(forbidden)[0]}"
    if relative.stem.casefold() in source_names:
        return "filename matches a registered opinion source"
    return None


def run_selftest() -> int:
    fake_names = {"001 - example opinion"}
    assert path_reason(pathlib.PurePosixPath("case_texts/example.txt"), fake_names)
    assert path_reason(pathlib.PurePosixPath("001 - example opinion.txt"), fake_names)
    sample = b"example\r\nopinion\r\n"
    digest = hashlib.sha256(sample.replace(b"\r\n", b"\n")).hexdigest()
    assert digest in {
        hashlib.sha256(sample).hexdigest(),
        hashlib.sha256(sample.replace(b"\r\n", b"\n")).hexdigest(),
    }
    print("OK: source-text leakage guard self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()

    try:
        source_names, source_hashes = registered_sources()
        files = git_release_files()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"source-text leakage guard could not prepare its inputs: {exc}", file=sys.stderr)
        return 2

    hits: list[tuple[str, str]] = []
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        relative = path.relative_to(REPO)
        reason = path_reason(relative, source_names)
        if reason:
            hits.append((relative.as_posix(), reason))
            continue
        if relative.as_posix() == "opinion_sources.csv":
            continue
        try:
            if content_hashes(path) & source_hashes:
                hits.append((relative.as_posix(), "content hash matches a registered opinion source"))
        except OSError as exc:
            print(f"could not hash {relative.as_posix()}: {exc}", file=sys.stderr)
            return 2

    if hits:
        print("Non-distributed opinion text may be present:", file=sys.stderr)
        for path, reason in hits:
            print(f"  {path}: {reason}", file=sys.stderr)
        return 1

    print(
        "OK: no source-text paths, registered source filenames, or registered "
        f"opinion-text hashes in {len(files)} release files."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
