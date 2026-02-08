"""
cli.py - Command-Line Interface (entry point)

Runs when a user types: python -m safe_fs_snapshot.cli ./some_directory
See python_study.py for detailed explanations of every concept used here.
"""

import argparse  # Built-in module for reading command-line arguments
from pathlib import Path  # Object-oriented filesystem paths
from collections import deque  # Double-ended queue (reserved for future use)
from . import snapshot


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

    root_dir = args.path

    # get the snapshot list
    files_snapshot = snapshot.create_snapshot(root_dir)

    # write the snapshot list to a json file
    snapshot.write_snapshot(files_snapshot, root_dir)

    # print(f"file_snapshot: {files_snapshot}")

    return 0


# Runs main() only when executed directly (not when imported).
# raise SystemExit passes the exit code to the OS.
if __name__ == "__main__":
    raise SystemExit(main())
