import sys


sys.path.append("./config/")
sys.path.append("./helpers/")
sys.path.append("./Objects/")

from ServerObject import ServerObject
import config
from send_file import send_file

s = ServerObject()



if __name__ == "__main__":
    s.get_all_files()
    #print(s.file_details)
    #send_file(None,"\\mods\\Dragon-Mounts-Mod-1.7.10.jar")
    s.start_client_handler()

