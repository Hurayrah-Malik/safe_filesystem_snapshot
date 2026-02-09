import os

def get_file_size(path):
    return os.path.getsize(path)

def is_hidden(filename):
    return filename.startswith(".")