import json
from pathlib import Path
from datetime import datetime


# create a storage directory. if already exists, then dont create new one. return path to it
def get_storage_dir() -> Path:
    home = Path.home()
    snapshot_dir = home / ".safe-fs-snapshot"
    snapshot_dir.mkdir(exist_ok=True)
    return snapshot_dir


# given a directory, output the list of snapshot containing dictionaries
def create_snapshot(directory: Path) -> list:
    # check if this directory is actually on computer
    verify_directory(directory)

    # --- Normalize to absolute path ---
    # .resolve() converts relative -> absolute and cleans up ".." and "."
    root_dir = directory.resolve()
    # print("Normalized directory path:", root_dir)

    # --- Iterative directory traversal (depth-first using a stack) ---
    # Stack = list used as a to-do list of directories to scan.
    # pop() from end = depth-first. See python_study.py Concept 6 for details.
    # print("Traversal skeleton:")
    stack = [root_dir]

    files_snapshot = []
    while stack:
        current_dir = stack.pop()

        # print("Scanning:", current_dir)
        # print("Children of  current_dir :")

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

            # print(f"- {kind}: {entry.name}")

    # sort the file snapshot by the value of "relative_path" of each dictionary in the list (alphebetically)
    files_snapshot.sort(key=lambda f: f["relative_path"])

    # print(f"file_snapshot: {files_snapshot}")

    return files_snapshot


# verify that the directory given exists in the os and is actually a directory, not a file
def verify_directory(directory: Path):
    if not directory.exists():
        print(f"Error: path does not exist: {directory}")
        raise SystemExit(1)

    if not directory.is_dir():
        print(f"Error: path is not a directory: {directory}")
        raise SystemExit(1)


# verify that the snapshot file actually exsists
def verify_snapshot_file(snapshot_path: Path):
    if not snapshot_path.exists():
        print(f"the file: {snapshot_path.stem}, doesnt exist")
        raise SystemExit(1)

    # if not snapshot_path.is_dir():
    #     print(f"Error: path is not a directory: {}")
    #     raise SystemExit(1)


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


# print out the data of a single snapshot
def list_snapshots():
    snapshot_storage_path = get_storage_dir()
    # get a list of all files in that snapshot directory
    snapshots = list(snapshot_storage_path.iterdir())
    for snapshot in snapshots:
        print(snapshot.stem)


# show details of a single snapshot
def show_snapshot(snapshot_name: str):
    snapshot_file_path = get_storage_dir() / f"{snapshot_name}.json"
    # check if that snapshot actually
    verify_snapshot_file(snapshot_file_path)
    # open the correct snapshot json, then print out its data
    with open(snapshot_file_path, "r") as f:
        snapshot_data = json.load(f)
        print(snapshot_data)
