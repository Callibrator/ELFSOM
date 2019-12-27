import os
import config

from get_sha256 import get_sha256

def get_file_details(file_path):

    sha = get_sha256(file_path)
    filename = file_path.split(os.sep)[-1]
    launcher_path = file_path.replace(config.minecraft_files_path, "")

    data = {
        "sha256": sha,
        "filename": filename,
        "launcher_path": launcher_path,
    }

    return data
