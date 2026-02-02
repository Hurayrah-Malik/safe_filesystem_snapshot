"""
cli.py

This file is the command-line entry point for your tool.

In this step we introduce argparse:
- argparse is the standard library module for reading command-line arguments
- we create an ArgumentParser object (it describes what args we accept)
- we print the help text to confirm it exists and is configured
"""

# -----------------------------
# Import: argparse (standard library)
# -----------------------------
# argparse is a built-in Python module (no pip install needed).
# It provides tools to define command-line arguments like:
#   mytool snapshot DIR --output manifest.json
import argparse

from pathlib import Path


def main() -> int:
    """
    Program entry point.

    For now, we create the parser and print its help text.
    This lets you SEE what argparse is building before we parse any real arguments.
    """

    # Create the parser object.
    # Think: "a description of what command-line args my program supports".
    parser = argparse.ArgumentParser(
        prog="safe-fs-snapshot",  # the program name shown in help output
        description="Create deterministic filesystem manifests and diff them.",
    )

    # Positional argument:
    # This means the user MUST supply a value, in order.
    parser.add_argument(
        "path",
        type=Path,  # convert string -> Path immediately
        help="Path to the directory to scan",
    )

    args = parser.parse_args()

    # 1) Check that the path exists
    if not args.path.exists():
        print(f"Error: path does not exist: {args.path}")
        raise SystemExit(1)

    # 2) Check that the path is a directory (not a file)
    if not args.path.is_dir():
        print(f"Error: path is not a directory: {args.path}")
        raise SystemExit(1)

    # 3) Normalize to an absolute path for internal use
    root_dir = args.path.resolve()

    print("Normalized directory path:", root_dir)

    # List direct children (top-level only).
    # This does NOT recurse into subfolders.
    print("Direct children:")

    # iterdir() yields Path objects for each entry inside the directory.
    for entry in root_dir.iterdir():
        # entry.name is just the last part (file/folder name), not the full path.
        # is_dir() asks the OS if this entry is a directory.
        # is_file() asks the OS if this entry is a regular file.
        if entry.is_dir():
            kind = "DIR"
        elif entry.is_file():
            kind = "FILE"
        else:
            # This can happen for special filesystem entries.
            kind = "OTHER"

        print(f"- {kind}: {entry.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
