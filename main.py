#!/usr/bin/env python3
"""Print a pretty tree view of a directory.

Usage:
    python3 main.py <folder> [--max-depth 3] [--dirs-only] [--show-size]
"""
import argparse
from pathlib import Path


def format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{num_bytes}B"


def tree(path: Path, prefix: str = "", depth: int = 0, max_depth: int = 0,
         dirs_only: bool = False, show_size: bool = False,
         show_hidden: bool = False) -> int:
    """Print one level and return the number of entries printed."""
    try:
        entries = sorted(path.iterdir(),
                         key=lambda p: (not p.is_dir(), p.name.lower()))
    except OSError as exc:
        print(f"{prefix}└── [unreadable: {exc}]")
        return 0
    if not show_hidden:
        entries = [e for e in entries if not e.name.startswith(".")]
    if dirs_only:
        entries = [e for e in entries if e.is_dir()]
    count = 0
    for i, entry in enumerate(entries):
        last = i == len(entries) - 1
        branch = "└── " if last else "├── "
        label = entry.name + ("/" if entry.is_dir() else "")
        if show_size and entry.is_file():
            try:
                label += f" ({format_size(entry.stat().st_size)})"
            except OSError:
                pass
        print(f"{prefix}{branch}{label}")
        count += 1
        if entry.is_dir() and (max_depth == 0 or depth + 1 < max_depth):
            extension = "    " if last else "│   "
            count += tree(entry, prefix + extension, depth + 1, max_depth,
                          dirs_only, show_size, show_hidden)
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Print a pretty tree view of a directory.")
    parser.add_argument("folder", type=Path, nargs="?", default=Path("."),
                        help="Directory to print (default: current directory)")
    parser.add_argument("--max-depth", type=int, default=0,
                        help="Limit depth (0 = unlimited)")
    parser.add_argument("--dirs-only", action="store_true",
                        help="Show directories only")
    parser.add_argument("--show-size", action="store_true",
                        help="Show file sizes")
    parser.add_argument("--show-hidden", action="store_true",
                        help="Include hidden files and folders")
    args = parser.parse_args()
    if not args.folder.is_dir():
        parser.error(f"not a directory: {args.folder}")
    if args.max_depth < 0:
        parser.error("--max-depth must be 0 or more")
    print(f"{args.folder}/")
    total = tree(args.folder, max_depth=args.max_depth,
                 dirs_only=args.dirs_only, show_size=args.show_size,
                 show_hidden=args.show_hidden)
    print(f"\n{total} entr{'y' if total == 1 else 'ies'} listed.")


if __name__ == "__main__":
    main()
