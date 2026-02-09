import json


# load the file and print it
def main():
    print()

    # open the first snapshot and store it
    with open("snapshot_1.json", "r") as f:
        snapshot1 = json.load(f)
        snap1_files = snapshot1["files"]

    # open the second snapshot and store it
    with open("snapshot_2.json", "r") as f:
        snapshot2 = json.load(f)
        snap2_files = snapshot2["files"]

    # compare the snapshots
    compare_snapshots(snap1_files, snap2_files)

    # files_dictionary = to_dictionary(files)


# convert a files list of dict, to a dict of dict (keys are the paths)
def to_dictionary(files_list: list) -> dict:
    files_dict = {}

    for file_entry in files_list:
        path_name = file_entry["relative_path"]
        files_dict[path_name] = file_entry

    return files_dict


# compare 2 snapshots by getting the common, deleted, and added files. also compare the files that are in common
def compare_snapshots(snapshot1: list, snapshot2: list) -> dict:
    snap1_dict = to_dictionary(snapshot1)
    snap2_dict = to_dictionary(snapshot2)
    deleted_files = snap1_dict.keys() - snap2_dict.keys()
    added_files = snap2_dict.keys() - snap1_dict.keys()
    common_files = snap1_dict.keys() & snap2_dict.keys()

    file_changes(snap1_dict, snap2_dict, common_files)

    # print(f"deleted files: {deleted_files}\n")
    # print(f"added files: {added_files}\n")
    # print(f"common files: {common_files}\n")

    return {
        "common_files": common_files,
        "deleted_files": deleted_files,
        "added_files": added_files,
    }


# compare the size of the common files of the snapshots
def file_changes(snap1_dict: dict, snap2_dict: dict, common_files: set) -> dict:
    changed_files = []
    unchanged_files = []
    for file_path in common_files:
        if snap1_dict[file_path] != snap2_dict[file_path]:
            changed_files.append(file_path)
            print(
                f"{file_path} was changed. size before change: {snap1_dict[file_path]['size']} ... size after change: {snap2_dict[file_path]['size']}"
            )
        else:
            unchanged_files.append(file_path)
            print(f"{file_path} was unchanged ")

    return {"changed_files": changed_files, "unchanged_files": unchanged_files}
