import json
from safe_fs_snapshot.storage import get_storage_dir, verify_snapshot_file


# convert a files list of dict, to a dict of dict (keys are the paths)
def to_dictionary(files_list: list) -> dict:
    files_dict = {}

    for file_entry in files_list:
        path_name = file_entry["relative_path"]
        files_dict[path_name] = file_entry

    return files_dict


# input the name of the snapshots, output the comparison dictionary
# compare 2 snapshots by getting the common, deleted, and added files. also compare the files that are in common
def compare_snapshots(snapshot1: str, snapshot2: str):
    snapshot1_file_path = get_storage_dir() / f"{snapshot1}.json"
    snapshot2_file_path = get_storage_dir() / f"{snapshot2}.json"
    # check if that snapshot actually
    verify_snapshot_file(snapshot1_file_path)
    verify_snapshot_file(snapshot2_file_path)

    # open the first snapshot and store it
    with open(snapshot1_file_path, "r") as f:
        snap1_data = json.load(f)
        snap1_files = snap1_data["files"]

    # open the second snapshot and store it
    with open(snapshot2_file_path, "r") as f:
        snap2_data = json.load(f)
        snap2_files = snap2_data["files"]

    # convert both lists to dictionary so its easier to compare them
    snap1_dict = to_dictionary(snap1_files)
    snap2_dict = to_dictionary(snap2_files)

    file_changes(snap1_dict, snap2_dict)


# compare the size of the common files of the snapshots
def file_changes(snap1_dict: dict, snap2_dict: dict):
    deleted_files = snap1_dict.keys() - snap2_dict.keys()
    added_files = snap2_dict.keys() - snap1_dict.keys()
    common_files = snap1_dict.keys() & snap2_dict.keys()

    # print all the deleted files
    for deleted_file in deleted_files:
        print(f"- {deleted_file}")

    # print all the added files
    for added_file in added_files:
        print(f"+ {added_file}")

    changed_files = []
    unchanged_files = []
    for file_path in common_files:
        if snap1_dict[file_path] != snap2_dict[file_path]:
            changed_files.append(file_path)
            print(
                f"~ {file_path} (size: {snap1_dict[file_path]['size']} -> {snap2_dict[file_path]['size']})"
            )
        else:
            unchanged_files.append(file_path)
            print(f"  {file_path}")

    # print summary line
    print()
    print(
        f"Summary: {len(added_files)} added, {len(deleted_files)} deleted, "
        f"{len(changed_files)} changed, {len(unchanged_files)} unchanged"
    )
