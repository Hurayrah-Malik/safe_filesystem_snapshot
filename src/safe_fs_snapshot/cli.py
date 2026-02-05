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

from collections import deque


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

    # if input was ./src , this prints ./src ... its a pathlib.Path object
    # printing objects utilizes their .__str__() function. so Path.__str__() is used to show string of path object
    # print(f"args.path: {args.path}")

    # 3) .resolve "normalizes" meaning it changes from relative path to absolute, so its more consistent and usable
    # think of root_dir as “A pointer to a location in the filesystem”
    # still a pathlib.Path object

    root_dir = args.path.resolve()

    # prints absolute path
    print("Normalized directory path:", root_dir)

    # Next step: iterative traversal skeleton.

    # We are NOT recursing yet. We are NOT listing files yet.
    # We are only proving how a "stack of directories to scan" works.
    print("Traversal skeleton:")

    # A stack is just a Python list we use as "work left to do".
    # Start with ONE directory: the root directory the user provided.
    stack = [root_dir]

    # Safety: limit how many directories we scan during learning,
    # so we don't print thousands of lines.
    max_dirs_to_scan = 3
    dirs_scanned = 0

    # While there is still work left, keep going.
    while stack:
        # pop() removes and returns the LAST item in the list.
        current_dir = stack.pop()

        dirs_scanned += 1
        if dirs_scanned > max_dirs_to_scan:
            break

        print("Scanning:", current_dir)

        # NEW: list the entries inside the directory we are scanning.
        # This is the same idea as your old "Direct children" code,
        # but now it runs for whatever directory we popped from the stack.
        print("Children of current_dir :")

        # Try to list entries in the directory.
        # This can fail due to permissions or because the directory disappears.
        try:
            entries = list(current_dir.iterdir())
        except PermissionError:
            print(f"WARNING: permission denied reading: {current_dir}")
            # Skip this directory and move on to the next one in the stack.
            continue
        except FileNotFoundError:
            print(f"WARNING: directory disappeared : {current_dir}")
            continue
        except OSError as e:
            # Catch-all for other OS-level issues.
            print(f"WARNING: failed to read: {current_dir} ({e})")
            continue

        for entry in entries:
            if entry.is_dir():
                kind = "DIR"
                stack.append(entry)  # schedule directory to be scanned later
            elif entry.is_file():
                kind = "FILE"
            else:
                kind = "OTHER"

            print(f"- {kind}: {entry.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
