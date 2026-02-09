"""
cli.py - Command-Line Interface (entry point)

Runs when a user types: python -m safe_fs_snapshot.cli <command>
Example commands:
    python -m safe_fs_snapshot.cli scan ./my_project
    python -m safe_fs_snapshot.cli list
    python -m safe_fs_snapshot.cli diff before-update after-update
    python -m safe_fs_snapshot.cli show before-update
"""

import argparse  # Built-in module for reading command-line arguments
from pathlib import Path  # Object-oriented filesystem paths


def main() -> int:
    """Program entry point. Returns 0 on success, 1 on error (exit code convention)."""

    # =============================================
    # MAIN PARSER (the receptionist)
    # =============================================
    # This creates the top-level parser for our program.
    # Its only job is to figure out which SUBCOMMAND the user typed (scan, list, diff, show)
    # and then hand off to the right subparser.
    # prog= is just cosmetic - it only affects what name shows in help/error messages.
    parser = argparse.ArgumentParser(
        prog="safe-fs-snapshot",
        description="A file integrity monitor. Take snapshots of directories and compare them.",
    )

    # =============================================
    # SUBPARSERS CONTAINER
    # =============================================
    # This creates a "container" that will hold all our subcommands.
    # dest="command" means: whatever subcommand the user types, store its name
    # in args.command. So if user types "scan", then args.command == "scan".
    subparsers = parser.add_subparsers(dest="command")

    # =============================================
    # SCAN subparser (specialist #1)
    # =============================================
    # This creates a subparser just for the "scan" command.
    # It only activates when the user types: safe-fs-snapshot scan ...
    scan_parser = subparsers.add_parser("scan", help="Take a snapshot of a directory")

    # This argument belongs to scan_parser (NOT the main parser).
    # So only the "scan" command expects a directory path.
    # Example: safe-fs-snapshot scan ./my_project
    scan_parser.add_argument(
        "path",
        type=Path,
        help="Path to the directory to scan",
    )

    # add an optional flag for "scan" argument, --name (what you want to name the snapshot file)
    scan_parser.add_argument("--name", help="Name for this snapshot")

    # =============================================
    # LIST subparser (specialist #2)
    # =============================================
    # No arguments needed - it just shows all saved snapshots.
    # Example: safe-fs-snapshot list
    list_parser = subparsers.add_parser("list", help="Show all saved snapshots")

    # =============================================
    # DIFF subparser (specialist #3)
    # =============================================
    # Needs TWO arguments: the names of the two snapshots to compare.
    # Example: safe-fs-snapshot diff before-update after-update
    diff_parser = subparsers.add_parser("diff", help="Compare two snapshots")

    diff_parser.add_argument(
        "name1",
        help="Name of the first snapshot",
    )
    diff_parser.add_argument(
        "name2",
        help="Name of the second snapshot",
    )

    # =============================================
    # SHOW subparser (specialist #4)
    # =============================================
    # Needs ONE argument: the name of the snapshot to display.
    # Example: safe-fs-snapshot show before-update
    show_parser = subparsers.add_parser("show", help="View details of a snapshot")

    show_parser.add_argument(
        "name",
        help="Name of the snapshot to view",
    )

    # =============================================
    # PARSE & ROUTE
    # =============================================
    # parse_args() reads what the user typed and fills in args.command
    # plus whatever arguments belong to that subcommand.
    args = parser.parse_args()

    # If user typed no command at all, show the help message.
    # (args.command will be None if they just typed: safe-fs-snapshot)
    if args.command is None:
        parser.print_help()
        return 0

    # Route to the right function based on which command was typed.
    # This is the if/elif chain we talked about!
    if args.command == "scan":
        print(f"Scanning directory: {args.path}")
        print(f"name of snapshot created: {args.name}")

    elif args.command == "list":
        print("Listing all snapshots...")

    elif args.command == "diff":
        print(f"Comparing snapshots: {args.name1} vs {args.name2}")

    elif args.command == "show":
        print(f"Showing snapshot: {args.name}")

    return 0


# Runs main() only when executed directly (not when imported).
# raise SystemExit passes the exit code to the OS.
if __name__ == "__main__":
    raise SystemExit(main())
