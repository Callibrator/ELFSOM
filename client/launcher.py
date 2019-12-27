import os
import sys
import json

sys.path.append("./Objects")
sys.path.append("./config")
sys.path.append("./helpers")


from GUI import GUI
from PyQt5.QtWidgets import *

import time

config = json.loads(open("config"+os.sep+"config.json").read())
minecraft_folder = "./minecraft"





if __name__ == "__main__":

    app = QApplication([])

    g = GUI(config["window_title"], config["server_url"], minecraft_folder, config["server_host"], config["port"], config["minecraft_files_skip_checks"], config["launcher_extra_buttons"], config["minecraft_server_details"],config["minecraft_files_download_only"])

    app.exec_()



