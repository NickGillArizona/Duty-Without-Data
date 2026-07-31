"""Fail if release-candidate Markdown links point to missing local files or
missing section anchors.

External URLs are ignored. File targets and anchor targets are both validated:
same-file "#section" links and cross-file "FILE.md#section" links must resolve
to a heading (or explicit HTML anchor) in the target Markdown file, using
GitHub's heading-slug convention (lowercase; punctuation dropped; spaces to
hyphens; duplicate headings suffixed -1, -2, ...). HTML src=/href=/srcset=
attribute targets (picture sources, inline images, HTML links) are validated
the same way, line by line; an attribute split across source lines is not
seen. The scan includes tracked files and untracked, non-ignored files that
would be picked up by a release commit.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from urllib.parse import unquote

REPO = pathlib.Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
HTML_ATTR_RE = re.compile(r"""(?:src|href|srcset)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HTML_ANCHOR_RE = re.compile(r"<a\s+(?:name|id)=\"([^\"]+)\"")
CHECK_SUFFIXES = {".md", ".csv", ".cff", ".yml", ".yaml"}
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "doi:",
    "urn:",
)

_anchor_cache: dict[pathlib.Path, set[str]] = {}


def candidate_files() -> list[pathlib.Path]:
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
        print(f"check_internal_links: could not list git files: {exc}", file=sys.stderr)
        sys.exit(2)
    return [
        REPO / p
        for p in (tracked_result.stdout + untracked_result.stdout).splitlines()
        if p.strip()
    ]


def github_slug(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)  # markdown links -> label
    t = t.replace("`", "")
    t = re.sub(r"[^\w\- ]", "", t)  # drop punctuation; keep letters/digits/_/-/space
    return t.replace(" ", "-")


def anchors_for(path: pathlib.Path) -> set[str]:
    """Anchor set for a Markdown file: heading slugs (fence-aware, with GitHub's
    duplicate suffixes) plus explicit HTML name/id anchors."""
    cached = _anchor_cache.get(path)
    if cached is not None:
        return cached
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        _anchor_cache[path] = anchors
        return anchors
    in_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            slug = github_slug(m.group(2))
            n = counts.get(slug, 0)
            counts[slug] = n + 1
            anchors.add(slug if n == 0 else f"{slug}-{n}")
        for am in HTML_ANCHOR_RE.finditer(line):
            anchors.add(am.group(1))
    _anchor_cache[path] = anchors
    return anchors


def split_target(raw: str) -> tuple[str | None, str | None]:
    """Return (path_part, anchor_part); (None, None) for external/empty targets,
    (None, anchor) for same-file anchors."""
    target = raw.strip().strip("<>")
    target = re.sub(r"\s+\"[^\"]*\"$", "", target)  # drop optional link title
    if not target:
        return None, None
    if target.lower().startswith(EXTERNAL_PREFIXES):
        return None, None
    if target.startswith("#"):
        return None, unquote(target[1:])
    path_part, _, anchor_part = target.partition("#")
    return unquote(path_part), (unquote(anchor_part) if anchor_part else None)


def main() -> int:
    broken: list[tuple[str, int, str, str]] = []
    for path in candidate_files():
        if path.suffix.lower() not in CHECK_SUFFIXES or not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(lines, start=1):
            targets = [m.group(1) for m in LINK_RE.finditer(line)]
            for am in HTML_ATTR_RE.finditer(line):
                # srcset may carry "url 1x, url 2x" candidate lists
                for piece in am.group(1).split(","):
                    token = piece.strip().split()[0] if piece.strip() else ""
                    if token:
                        targets.append(token)
            for raw_target in targets:
                path_part, anchor_part = split_target(raw_target)
                if path_part is None and anchor_part is None:
                    continue
                if path_part is None:
                    # same-file anchor
                    if path.suffix.lower() == ".md" and anchor_part not in anchors_for(path):
                        broken.append((path.relative_to(REPO).as_posix(), lineno,
                                       raw_target, "missing anchor"))
                    continue
                resolved = (path.parent / path_part).resolve()
                try:
                    resolved.relative_to(REPO)
                except ValueError:
                    broken.append((path.relative_to(REPO).as_posix(), lineno,
                                   raw_target, "escapes repository"))
                    continue
                if not resolved.exists():
                    broken.append((path.relative_to(REPO).as_posix(), lineno,
                                   raw_target, "missing file"))
                    continue
                if anchor_part and resolved.suffix.lower() == ".md" and resolved.is_file():
                    if anchor_part not in anchors_for(resolved):
                        broken.append((path.relative_to(REPO).as_posix(), lineno,
                                       raw_target, "missing anchor"))

    if broken:
        print("Broken internal links found:", file=sys.stderr)
        for filename, lineno, target, why in broken[:100]:
            print(f"  {filename}:{lineno}: {target} ({why})", file=sys.stderr)
        if len(broken) > 100:
            print(f"  ... and {len(broken) - 100} more", file=sys.stderr)
        return 1

    print("OK: no broken internal file links or section anchors in tracked or "
          "untracked release files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
