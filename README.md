# Safe Filesystem Snapshot

A command-line file integrity monitor. Take snapshots of directories, save them by name, and compare them to detect added, deleted, and changed files.

## Features

- **Scan** directories and save snapshots as named JSON files
- **List** all saved snapshots in a formatted table
- **Show** the details and file listing of any snapshot
- **Diff** two snapshots to see what changed between them

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/Hurayrah-Malik/safe_filesystem_snapshot.git
cd safe_filesystem_snapshot
pip install -e .
```

## Usage

All commands are run through the CLI:

```bash
python -m safe_fs_snapshot.cli <command>
```

### Scan a directory

```bash
# With a custom name
python -m safe_fs_snapshot.cli scan ./my_project --name before-update

# Auto-generated name (uses directory + timestamp)
python -m safe_fs_snapshot.cli scan ./my_project
```

```
Snapshot saved: before-update (42 files)
```

### List all snapshots

```bash
python -m safe_fs_snapshot.cli list
```

```
Name            Created              Files  Directory
--------------------------------------------------------------
before-update   2026-02-07 10:30 AM  42     C:/Users/me/my_project
after-update    2026-02-09 02:15 PM  44     C:/Users/me/my_project
```

### Show snapshot details

```bash
python -m safe_fs_snapshot.cli show before-update
```

```
Snapshot:   before-update
Directory:  C:/Users/me/my_project
Created:    2026-02-07 10:30 AM
Files:      42

  index.html         2.0 KB
  css/style.css      3.4 KB
  js/main.js         1.5 KB
  images/logo.png    43.9 KB
```

### Compare two snapshots

```bash
python -m safe_fs_snapshot.cli diff before-update after-update
```

```
Comparing: before-update vs after-update

- old_config.json
+ js/analytics.js
+ images/hero.png
~ css/style.css (size: 3500 -> 4100)
~ index.html (size: 2048 -> 2300)
  about.html
  js/main.js

Summary: 2 added, 1 deleted, 2 changed, 2 unchanged
```

| Symbol | Meaning |
|--------|---------|
| `+` | File was added |
| `-` | File was deleted |
| `~` | File was changed |
| ` ` | File is unchanged |

## How it works

1. **Scanning** walks the directory tree (depth-first traversal) and collects each file's relative path, size, and modification time
2. **Snapshots** are stored as JSON files in `~/.safe-fs-snapshot/`
3. **Diffing** converts both snapshots to dictionaries keyed by file path, then uses set operations on the keys to find added, deleted, and common files

## Project structure

```
src/safe_fs_snapshot/
    cli.py        # Command-line interface (entry point)
    snapshot.py   # Scanning, saving, listing, and showing snapshots
    diff.py       # Comparing two snapshots
    storage.py    # Shared utilities (storage directory, file validation)
```

## License

MIT
