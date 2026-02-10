import json
from pathlib import Path
from datetime import datetime
from safe_fs_snapshot.storage import get_storage_dir, verify_snapshot_file


# given a directory, output the list of snapshot containing dictionaries
def create_snapshot(directory: Path) -> list:
    # check if this directory is actually on computer
    verify_directory(directory)

    # --- Normalize to absolute path ---
    # .resolve() converts relative -> absolute and cleans up ".." and "."
    root_dir = directory.resolve()

    # --- Iterative directory traversal (depth-first using a stack) ---
    # Stack = list used as a to-do list of directories to scan.
    # pop() from end = depth-first. See python_study.py Concept 6 for details.
    stack = [root_dir]

    files_snapshot = []
    while stack:
        current_dir = stack.pop()

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
                stack.append(entry)  # add to stack so it gets scanned later
            elif entry.is_file():
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

    # sort the file snapshot alphabetically by relative_path
    files_snapshot.sort(key=lambda f: f["relative_path"])

    return files_snapshot


# verify that the directory given exists in the os and is actually a directory, not a file
def verify_directory(directory: Path):
    if not directory.exists():
        print(f"Error: path does not exist: {directory}")
        raise SystemExit(1)

    if not directory.is_dir():
        print(f"Error: path is not a directory: {directory}")
        raise SystemExit(1)


# write the snapshot to the file
def write_snapshot(snapshot: list, scanned_directory: Path, snapshot_name: str):
    scanned_directory = scanned_directory.resolve()
    snapshot_storage_path = get_storage_dir()
    created_at = datetime.now().isoformat()
    file_count = len(snapshot)
    wrapper = {
        "scanned_directory": scanned_directory.as_posix(),
        "created_at": created_at,
        "files_count": file_count,
        "files": snapshot,
    }

    with open(snapshot_storage_path / f"{snapshot_name}.json", "w") as f:
        json.dump(wrapper, f, indent=2)


# print a formatted table of all saved snapshots
def list_snapshots():
    snapshot_storage_path = get_storage_dir()
    # get only .json files, sorted alphabetically
    snapshots = sorted(snapshot_storage_path.glob("*.json"))

    if not snapshots:
        print("No snapshots found.")
        return

    # collect info from each snapshot file
    rows = []
    for snap_path in snapshots:
        with open(snap_path, "r") as f:
            data = json.load(f)
        name = snap_path.stem
        created = data.get("created_at", "unknown")
        # format the ISO timestamp into a readable date/time
        if created != "unknown":
            try:
                dt = datetime.fromisoformat(created)
                created = dt.strftime("%Y-%m-%d %I:%M %p")
            except ValueError:
                pass
        files_count = data.get("files_count", "?")
        directory = data.get("scanned_directory", "?")
        rows.append((name, created, str(files_count), directory))

    # calculate column widths so everything lines up
    headers = ("Name", "Created", "Files", "Directory")
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            if len(val) > col_widths[i]:
                col_widths[i] = len(val)

    # print header row and separator
    header_line = "  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # print each snapshot as a row
    for row in rows:
        print("  ".join(val.ljust(col_widths[i]) for i, val in enumerate(row)))


# show formatted details of a single snapshot
def show_snapshot(snapshot_name: str):
    snapshot_file_path = get_storage_dir() / f"{snapshot_name}.json"
    # check if that snapshot actually exists
    verify_snapshot_file(snapshot_file_path)
    # open the correct snapshot json, then print out its data
    with open(snapshot_file_path, "r") as f:
        snapshot_data = json.load(f)

    # print snapshot metadata
    print(f"Snapshot:   {snapshot_name}")
    print(f"Directory:  {snapshot_data.get('scanned_directory', '?')}")
    created = snapshot_data.get("created_at", "unknown")
    if created != "unknown":
        try:
            dt = datetime.fromisoformat(created)
            created = dt.strftime("%Y-%m-%d %I:%M %p")
        except ValueError:
            pass
    print(f"Created:    {created}")
    print(f"Files:      {snapshot_data.get('files_count', '?')}")
    print()

    # print each file with its size
    files = snapshot_data.get("files", [])
    if not files:
        print("  (no files)")
        return

    # calculate column width for aligned output
    max_path_len = max(len(f["relative_path"]) for f in files)
    for file_entry in files:
        path = file_entry["relative_path"]
        size = file_entry["size"]
        # format size in a human-readable way
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        print(f"  {path.ljust(max_path_len)}  {size_str}")
