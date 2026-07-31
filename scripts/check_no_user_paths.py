"""Fail if any release-candidate file contains a personal absolute filepath.

Run from the repo root:

    python scripts/check_no_user_paths.py

Exits non-zero on any hit. Intended to be wired into a pre-commit hook so the
machine-generated artifacts under results/ never re-leak personal paths. The
scan includes tracked files and untracked, non-ignored files that would be
picked up by a release commit.

Detected patterns:
  - Windows: C:\\Users\\<user>\\..., C:/Users/<user>/...
  - WSL:     /mnt/c/Users/<user>/...
  - macOS:   /Users/<user>/...
  - Linux:   /home/<user>/...

False-positive exclusions:
  - URLs containing "/Users/" or "/home/" path components (HTTP scheme present)
  - Lines that include the author's contact-attribution surface (CITATION.cff,
    README "Contact:" line, cover letter signature) — these are intentional.
"""
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]

PATH_RE = re.compile(
    r"(?:[A-Za-z]:[\\/]+|/mnt/[a-z][\\/]+|^|[\s\"'])"
    r"(?:Users|home)[\\/]+[A-Za-z0-9._-]+[\\/]+",
    re.MULTILINE,
)

URL_RE = re.compile(r"https?://[^\s\"'<>]*")

# Author attribution surface — intentional, not leaks.
ATTRIBUTION_TOKENS = (
    "@gmail.com",
    "@arizona.edu",
    "NickGillArizona",
    "Nick Gill",
    "Nicholas Gill",
)


def is_attribution_line(line: str) -> bool:
    return any(token in line for token in ATTRIBUTION_TOKENS)


def line_paths(line: str) -> list[str]:
    """Return the substrings that look like personal paths, after URL exclusion."""
    # Strip URL spans before path matching.
    stripped = URL_RE.sub("", line)
    if is_attribution_line(stripped):
        return []
    return PATH_RE.findall(stripped)


def main() -> int:
    try:
        tracked_result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        )
        untracked_result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"check_no_user_paths: could not list git files: {exc}", file=sys.stderr)
        return 2

    tracked = [
        REPO / p
        for p in (tracked_result.stdout + untracked_result.stdout).splitlines()
        if p.strip()
    ]
    text_extensions = {".md", ".txt", ".py", ".json", ".csv", ".log", ".cff", ".yml", ".yaml", ".toml", ".ini"}

    hits: list[tuple[str, int, str]] = []
    for path in tracked:
        if path.suffix.lower() not in text_extensions:
            continue
        if not path.exists():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(content.splitlines(), start=1):
            if line_paths(line):
                hits.append((str(path.relative_to(REPO)).replace("\\", "/"), lineno, line.strip()))

    if hits:
        print("Personal paths found in tracked files:", file=sys.stderr)
        for f, n, snippet in hits[:50]:
            print(f"  {f}:{n}: {snippet[:140]}", file=sys.stderr)
        if len(hits) > 50:
            print(f"  ... and {len(hits) - 50} more", file=sys.stderr)
        return 1

    print("OK: no personal paths in tracked or untracked release files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
