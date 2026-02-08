"""
python_study.py - Concepts Learned While Building the Snapshot Tool

This file is a living reference of Python concepts you've learned.
Each section explains a concept, shows examples, and notes WHY it matters.
Review this file anytime you need a refresher.
"""


# ============================================================
# CONCEPT 1: THE DOT OPERATOR (Attribute Access)
# ============================================================
#
# The dot (.) in Python means: "look inside this object and get the thing
# with this name." This is called ATTRIBUTE ACCESS.
#
# Think of an object like a backpack. The dot is you reaching inside the
# backpack to grab something by its label:
#
#   backpack.water_bottle   -> reach in, grab the water bottle
#   backpack.notebook       -> reach in, grab the notebook
#
# You can use the dot on ANY Python object (not just special ones).

# --- Example ---
from pathlib import Path

my_path = Path("./src/cli.py")

# .name is an ATTRIBUTE of the Path object - it holds the filename
print(my_path.name)       # Output: "cli.py"      (type: str)

# .parent is an ATTRIBUTE - it holds the parent directory
print(my_path.parent)     # Output: WindowsPath('src')  (type: Path)

# .exists() is a METHOD (a function attached to the object)
# Methods use the dot too, but you call them with ()
print(my_path.exists())   # Output: True or False  (type: bool)


# ============================================================
# CONCEPT 2: ARGPARSE AND THE NAMESPACE OBJECT
# ============================================================
#
# argparse is Python's built-in module for reading command-line arguments.
#
# HOW IT WORKS (3 steps):
#   1. Create a parser:      parser = argparse.ArgumentParser(...)
#   2. Define arguments:      parser.add_argument("name", type=..., help=...)
#   3. Parse the input:       args = parser.parse_args()
#
# parse_args() returns a NAMESPACE object. A Namespace is just a container
# where each argument is stored with the NAME you gave it.
#
# KEY INSIGHT:
#   When you write: parser.add_argument("path", type=Path)
#   The string "path" is the NAME (label) for this argument.
#   The type=Path is the CONVERSION applied to the user's input.
#   These are TWO SEPARATE THINGS that happen to look similar!
#
#   "path" (lowercase, in quotes) = the name/label
#   Path (uppercase, no quotes) = the pathlib.Path class used for conversion

# --- Example (conceptual - don't actually run this, it needs CLI args) ---
#
# parser = argparse.ArgumentParser(prog="my-tool")
# parser.add_argument("path", type=Path)       # name="path", convert to Path
# parser.add_argument("count", type=int)        # name="count", convert to int
# parser.add_argument("--verbose", action="store_true")  # optional flag
#
# args = parser.parse_args()
#
# Accessing arguments using the dot and their NAMES:
#   args.path      -> Path object (because type=Path)
#   args.count     -> int (because type=int)
#   args.verbose   -> True or False
#
# If you printed args, you'd see:
#   Namespace(path=WindowsPath('src'), count=5, verbose=True)
#
# IMPORTANT:
#   - If the user provides NO arguments, argparse prints an error and exits
#     AUTOMATICALLY. Your validation code never even runs.
#   - argparse does NOT check if a path exists. It only converts the string.
#     That's why WE check .exists() manually after parsing.


# ============================================================
# CONCEPT 3: .exists() vs argparse - WHO CHECKS WHAT?
# ============================================================
#
# There are TWO layers of validation in our program:
#
# LAYER 1: argparse (automatic)
#   - Checks: Did the user provide the required arguments?
#   - If not: argparse prints "error: the following arguments are required: path"
#             and exits. Our code never runs.
#   - Also handles: type conversion (string -> Path)
#
# LAYER 2: Our manual checks (lines 50-57 in cli.py)
#   - .exists(): Asks the OS "does this path point to something real?"
#     A Path object can be created from ANY string, even nonsense.
#     Path("./fake_folder") is valid Python - it just points to nothing.
#   - .is_dir(): Asks the OS "is this path a directory?"
#     We need a directory, not a file. Our tool scans directory TREES.
#
# ANALOGY:
#   Layer 1 (argparse): "Did you write something on the envelope?" (any address)
#   Layer 2 (.exists): "Does this address point to a real building?"
#   Layer 2 (.is_dir): "Is that building a warehouse? (not a single mailbox)"


# ============================================================
# CONCEPT 4: OBJECTS AND TYPES
# ============================================================
#
# In Python, EVERYTHING is an object. Every value has a TYPE.
# The type determines what you can DO with that value.
#
# TYPE          | EXAMPLE VALUE           | WHAT YOU CAN DO WITH IT
# -------------|-------------------------|---------------------------
# str          | "hello"                 | .upper(), .split(), .strip()
# int          | 42                      | +, -, *, / (math)
# float        | 3.14                    | same as int, but with decimals
# bool         | True / False            | logic: and, or, not
# list         | [1, 2, 3]              | .append(), .pop(), indexing [0]
# dict         | {"key": "value"}       | ["key"], .items(), .keys()
# Path         | Path("./src")          | .exists(), .is_dir(), .name
# Namespace    | Namespace(path=...)    | .path, .count (dot access)
#
# You can check any value's type with type():
#   type(42)        -> <class 'int'>
#   type("hello")   -> <class 'str'>
#   type(Path(".")) -> <class 'pathlib.WindowsPath'>

# --- Example ---
x = 42
print(type(x))           # <class 'int'>

name = "hello"
print(type(name))         # <class 'str'>

p = Path(".")
print(type(p))            # <class 'pathlib.WindowsPath'>

my_list = [1, 2, 3]
print(type(my_list))      # <class 'list'>


# ============================================================
# CONCEPT 5: TRUTHY AND FALSY VALUES
# ============================================================
#
# In Python, every value can be treated as True or False.
# This is used in if statements and while loops.
#
# FALSY (treated as False):
#   - False
#   - 0
#   - "" (empty string)
#   - [] (empty list)
#   - {} (empty dict)
#   - None
#
# TRUTHY (treated as True):
#   - Everything else! Any non-zero number, non-empty string, non-empty list, etc.
#
# WHY THIS MATTERS:
#   In cli.py, we write: while stack:
#   This means: "while stack is not empty"
#   Because an empty list [] is falsy, the loop stops when the stack is empty.

# --- Example ---
my_list = [1, 2, 3]
if my_list:          # True, because the list is not empty
    print("List has items!")

empty_list = []
if empty_list:       # False, because the list IS empty
    print("This will NOT print")

if not empty_list:   # "not False" = True
    print("List is empty!")


# ============================================================
# CONCEPT 6: ITERATIVE vs RECURSIVE TRAVERSAL
# ============================================================
#
# When you need to visit every item in a tree structure (like directories),
# there are two approaches:
#
# RECURSIVE: A function that calls ITSELF.
#   def scan(directory):
#       for item in directory:
#           if item.is_dir():
#               scan(item)  # <- calls itself! Goes deeper.
#
#   Problem: Python has a limit of ~1000 nested calls. If you have
#   a folder nested 1001 levels deep, Python crashes (RecursionError).
#
# ITERATIVE: A loop with an explicit stack (a list used as a to-do list).
#   stack = [root_dir]
#   while stack:
#       current = stack.pop()
#       for item in current:
#           if item.is_dir():
#               stack.append(item)  # <- adds to the to-do list
#
#   No crash risk! The stack lives in heap memory, which is much larger.
#   This is the approach we use in our snapshot tool.
#
# FOR SYSTEMS PROGRAMMING:
#   Iterative is almost always preferred because:
#   - No stack overflow risk
#   - More control over traversal order
#   - Easier to add features (like pause/resume)


# ============================================================
# CONCEPT 7: try/except (Error Handling)
# ============================================================
#
# When something can go wrong, we use try/except to handle it
# gracefully instead of crashing.
#
# SYNTAX:
#   try:
#       risky_code_here()
#   except SomeErrorType:
#       what_to_do_if_it_fails()
#
# You can catch SPECIFIC error types:
#   except PermissionError:   # only catches permission problems
#   except FileNotFoundError: # only catches missing file/dir
#   except OSError as e:      # catches any OS error, saves it as `e`
#
# IMPORTANT KEYWORDS:
#   continue - skip the rest of THIS loop iteration, go to next one
#   break    - exit the entire loop immediately

# --- Example ---
try:
    result = 10 / 0  # This will cause a ZeroDivisionError
except ZeroDivisionError:
    print("Cannot divide by zero!")  # Handle it gracefully

# With "as e" to capture the error message:
try:
    Path("/nonexistent/path").iterdir()
except OSError as e:
    print(f"Error occurred: {e}")


# ============================================================
# CONCEPT 8: NAMESPACE vs DICTIONARY - What's the difference?
# ============================================================
#
# CONFUSION THAT CAME UP:
#   "Is a Namespace kind of like a dictionary, where there are labels (keys)
#   and corresponding values for each label?"
#
# ANSWER: YES! They are very similar. Both store labeled values.
# The difference is just HOW you access the data:
#
#   DICTIONARY:  uses square brackets + string key
#     my_dict = {"path": Path("src"), "count": 5}
#     my_dict["path"]       # -> Path("src")
#     my_dict["count"]      # -> 5
#
#   NAMESPACE:   uses dot + attribute name
#     args = Namespace(path=Path("src"), count=5)
#     args.path             # -> Path("src")
#     args.count            # -> 5
#
# You can even CONVERT a Namespace to a dictionary:
#     vars(args)  # -> {"path": Path("src"), "count": 5}
#
# WOULD YOU EVER CREATE A NAMESPACE YOURSELF?
#   Almost never. Namespace is something argparse creates for you
#   behind the scenes. In practice, you'll use:
#   - Dictionaries ({})  -> the most common "labeled container" you create
#   - Classes            -> when you want custom objects (we'll learn later)
#   - Namespace          -> basically only from argparse, never manually
#
# WHY THIS MATTERS:
#   Understanding that Namespace is "just argparse's dictionary with dot access"
#   removes the mystery. It's not a special or complex thing - it's just a
#   simple container that argparse chose to use instead of a regular dict.

# --- Example ---
# Showing that dict and Namespace hold the same data, just accessed differently:

my_dict = {"name": "cli.py", "size": 1024}
print(my_dict["name"])     # "cli.py"  - accessed with ["key"]
print(my_dict["size"])     # 1024      - accessed with ["key"]

# If args were a Namespace from argparse:
# args.path   -> accessed with .attribute
# args.count  -> accessed with .attribute
# Same data, different syntax for accessing it.


# ============================================================
# (More concepts will be added as we learn them!)
# ============================================================
