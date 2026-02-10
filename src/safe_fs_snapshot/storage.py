"""
storage.py - Shared storage utilities

Functions used by both snapshot.py and diff.py for accessing
the snapshot storage directory and validating snapshot files.
"""

from pathlib import Path


# create a storage directory. if already exists, then dont create new one. return path to it
def get_storage_dir() -> Path:
    home = Path.home()
    snapshot_dir = home / ".safe-fs-snapshot"
    snapshot_dir.mkdir(exist_ok=True)
    return snapshot_dir


# verify that the snapshot file actually exists
def verify_snapshot_file(snapshot_path: Path):
    if not snapshot_path.exists():
        print(f"Error: snapshot '{snapshot_path.stem}' not found.")
        raise SystemExit(1)
