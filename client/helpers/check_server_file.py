#Returns True if a filepath is actual file of server!

import os
import config

def check_server_file(file,files):

    for f in files:
        if f["launcher_path"] == file["launcher_path"]:
            filepath = config.minecraft_files_path + f["launcher_path"]
            if os.path.isfile(filepath):
                return True

    return False
