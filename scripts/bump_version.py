#!/usr/bin/env python3
"""
Bump/set project version safely (SemVer) without manual plist editing.

Single source of truth:
- VERSION (text file)
- workflow/info.plist (key: version)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import pathlib
import plistlib
import re
import sys


SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def _read_version_file(path: pathlib.Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _write_text(path: pathlib.Path, content: str) -> None:
    path.write_text(content + "\n", encoding="utf-8")


def _parse_semver(version: str) -> tuple[int, int, int]:
    m = SEMVER_RE.match(version)
    if not m:
        raise ValueError(f"Version invalide (SemVer attendu) : {version!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _bump(version: str, part: str) -> str:
    major, minor, patch = _parse_semver(version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"Partie inconnue : {part}")


def _load_plist(path: pathlib.Path) -> dict:
    with path.open("rb") as f:
        return plistlib.load(f)


def _save_plist(path: pathlib.Path, data: dict) -> None:
    with path.open("wb") as f:
        plistlib.dump(data, f, sort_keys=False)


def _update_changelog(changelog_path: pathlib.Path, version: str) -> None:
    today = _dt.date.today().isoformat()
    if not changelog_path.exists():
        _write_text(
            changelog_path,
            "\n".join(
                [
                    "# Changelog",
                    "",
                    "Le projet suit **SemVer** : `MAJOR.MINOR.PATCH`.",
                    "",
                    f"## [{version}] - {today}",
                    "",
                    "### Changed",
                    "- TODO",
                    "",
                ]
            ),
        )
        return

    content = changelog_path.read_text(encoding="utf-8")
    header = "Le projet suit **SemVer** : `MAJOR.MINOR.PATCH`."
    if header not in content:
        # On n'altère pas agressivement : on laisse le changelog tel quel.
        return

    # Ajoute une section en haut (après le header + une ligne vide) si elle n'existe pas déjà.
    marker = header + "\n\n"
    new_section = f"## [{version}] - {today}\n\n### Changed\n- TODO\n\n"
    if f"## [{version}]" in content:
        return
    content = content.replace(marker, marker + new_section, 1)
    changelog_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--set", dest="set_version", help="Fixer explicitement la version (SemVer)."
    )
    group.add_argument(
        "--bump",
        choices=["major", "minor", "patch"],
        help="Incrémenter la version courante.",
    )
    parser.add_argument(
        "--no-changelog", action="store_true", help="Ne pas modifier CHANGELOG.md."
    )
    args = parser.parse_args()

    root = _repo_root()
    version_path = root / "VERSION"
    plist_path = root / "workflow" / "info.plist"
    changelog_path = root / "CHANGELOG.md"

    current = _read_version_file(version_path) or "0.0.0"

    if args.set_version:
        new_version = args.set_version.strip()
        _parse_semver(new_version)
    else:
        _parse_semver(current)
        new_version = _bump(current, args.bump)

    # Update VERSION
    _write_text(version_path, new_version)

    # Update workflow/info.plist version
    plist = _load_plist(plist_path)
    plist["version"] = new_version
    _save_plist(plist_path, plist)

    # Optionally update CHANGELOG
    if not args.no_changelog:
        _update_changelog(changelog_path, new_version)

    print(new_version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
