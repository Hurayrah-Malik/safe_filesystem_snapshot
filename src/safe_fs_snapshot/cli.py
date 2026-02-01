"""
cli.py

This file will become the command-line entry point for your tool.

For now, it only prints a message so we can confirm:
1) the file is in the right place
2) Python can import/run it as a module
"""

# No imports yet. We don't need any.


def main() -> int:
    """
    This is the function we will treat as the program's "main" entry point.

    Return value:
      - 0 means "success" (standard convention for command-line programs)
      - non-zero means "error"
    """
    print("cli.py ran successfully")
    return 0


# This block runs only when you execute this file directly (or with -m).
# It does NOT run when the file is imported from somewhere else.
if __name__ == "__main__":
    # SystemExit makes the process exit with the integer code returned by main().
    raise SystemExit(main())
