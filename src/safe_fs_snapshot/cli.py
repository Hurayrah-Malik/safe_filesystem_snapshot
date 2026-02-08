"""
cli.py - Command-Line Interface (entry point)

Runs when a user types: python -m safe_fs_snapshot.cli ./some_directory
The "front door" of the program: reads input, validates, traverses directories.
See python_study.py for detailed explanations of every concept used here.
"""

import argparse  # Built-in module for reading command-line arguments
from pathlib import Path  # Object-oriented filesystem paths
from collections import deque  # Double-ended queue (reserved for future use)


def main() -> int:
    """Program entry point. Returns 0 on success, 1 on error (exit code convention)."""

    # --- Argument parsing ---
    # Create parser, define one required positional arg named "path"
    # "path" = the label/name, type=Path = auto-convert string -> Path object
    parser = argparse.ArgumentParser(
        prog="safe-fs-snapshot",
        description="Create deterministic filesystem manifests and diff them.",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the directory to scan",
    )

    # parse_args() reads CLI input, returns a Namespace (container with dot access)
    # If user provides no args, argparse auto-prints error and exits before our code runs
    args = parser.parse_args()

    # --- Path validation ---
    # argparse does NOT check if the path exists on disk, only converts the string.
    # We must verify: 1) path exists, 2) it's a directory (not a file)
    if not args.path.exists():
        print(f"Error: path does not exist: {args.path}")
        raise SystemExit(1)

    if not args.path.is_dir():
        print(f"Error: path is not a directory: {args.path}")
        raise SystemExit(1)

    # --- Normalize to absolute path ---
    # .resolve() converts relative -> absolute and cleans up ".." and "."
    root_dir = args.path.resolve()
    print("Normalized directory path:", root_dir)

    # --- Iterative directory traversal (depth-first using a stack) ---
    # Stack = list used as a to-do list of directories to scan.
    # pop() from end = depth-first. See python_study.py Concept 6 for details.
    print("Traversal skeleton:")
    stack = [root_dir]

    # Safety limit for learning (will be removed later)
    max_dirs_to_scan = 3
    dirs_scanned = 0

    files_snapshot = []
    while stack:
        current_dir = stack.pop()

        dirs_scanned += 1
        if dirs_scanned > max_dirs_to_scan:
            break

        print("Scanning:", current_dir)
        print("Children of  current_dir :")

        # List directory contents. Can fail due to permissions or race conditions.
        # try/except prevents one bad directory from crashing the whole scan.
        # "continue" skips to the next directory in the stack.
        try:
            entries = list(current_dir.iterdir())
        except PermissionError:
            print(f"WARNING: permission denied  reading: {current_dir}")
            continue
        except FileNotFoundError:
            print(f"WARNING: directory disappeared: {current_dir}")
            continue
        except OSError as e:
            print(f"WARNING: failed to read: {current_dir} ({e})")
            continue

        # Classify each entry and schedule subdirectories for later scanning
        for entry in entries:
            if entry.is_dir():
                kind = "DIR"
                stack.append(entry)  # add to stack so it gets scanned later
            elif entry.is_file():
                kind = "FILE"

                try:
                    relative_path = entry.relative_to(root_dir)
                    entry_stats = entry.stat()
                    entry_size = entry_stats.st_size
                    entry_mtime = entry_stats.st_mtime
                except PermissionError:
                    print(f"WARNING: permission denied  reading: {entry}")
                    continue
                except FileNotFoundError:
                    print(f"WARNING: file disappeared: {entry}")
                    continue
                except OSError as e:
                    print(f"WARNING: failed to read: {entry} ({e})")
                    continue

                files_snapshot.append(
                    {
                        "relative_path": relative_path.as_posix(),
                        "size": entry_size,
                        "mtime": entry_mtime,
                    }
                )

            else:
                kind = "OTHER"

            print(f"- {kind}: {entry.name}")

    # sort the file snapshot by the value of "relative_path" of each dictionary in the list (alphebetically)
    files_snapshot.sort(key=lambda f: f["relative_path"])

    print(f"file_snapshot: {files_snapshot}")

    return 0


# Runs main() only when executed directly (not when imported).
# raise SystemExit passes the exit code to the OS.
if __name__ == "__main__":
    raise SystemExit(main())
