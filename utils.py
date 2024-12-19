# utils.py

import os

def get_new_filename():
    """Generate a unique filename to prevent overwriting."""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    i = 1
    while True:
        filename = f"{data_dir}/file{i}.txt"
        if not os.path.exists(filename):
            return filename
        i += 1
