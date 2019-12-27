import os
import socket
from get_files_tree import get_files_tree
from get_file_details import get_file_details
from download_file import download_file
from remove_empty_folders import  remove_empty_folders
import json

class Client:
    def __init__(self,host,port,minecraft_folder, skip_files,mc_files_only_download):

        self.host = host
        self.port = port

        self.minecraft_folder = minecraft_folder
        self.socket = None

        self.skip_files_on_update = skip_files
        self.download_only_files = mc_files_only_download

        if not os.path.isdir(minecraft_folder):
            os.mkdir(minecraft_folder)

    def get_all_files(self):
        file_details = []
        for f in get_files_tree(self.minecraft_folder):
            file_details.append(get_file_details(f,self.minecraft_folder))

        return file_details

    def connect(self):

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def get_updates(self):
        file_details = self.get_all_files()

        data = {
            "details":True,
            "files":file_details
        }

        serializedData = json.dumps(data).encode()

        self.socket.sendall(str(len(serializedData)).encode())
        ret = self.socket.recv(2048).decode()

        if ret != "ok":
            return False

        self.socket.sendall(serializedData)

        ret = self.socket.recv(2048).decode()
        self.socket.sendall(b"ok")

        new_data = self.socket.recv(int(ret)).decode()

        return json.loads(new_data)

    def do_upgrades(self, files, progressBar=None):

        i = 1
        if progressBar != None:
            progressBar.emit(i, len(files))

        skip_files_path = []
        for f in self.skip_files_on_update:
            skip_files_path.append(os.path.abspath(self.minecraft_folder + f).lower())

        skip_files_before_update = []
        for f in self.download_only_files:
            skip_files_before_update.append(os.path.abspath(self.minecraft_folder + f).lower())


        for f in files:
            fpath = self.minecraft_folder + f["launcher_path"]

            abs_path = os.path.abspath(fpath).lower()

            if f["status"] == "remove":

                skip = False

                for skip_path in skip_files_path:
                    if abs_path.startswith(skip_path):
                        skip = True
                        break

                if not skip:
                    if os.path.isfile(fpath):
                        os.remove(fpath)

            elif f["status"] == "update":
                skip = False
                for skip_path in skip_files_before_update:
                    if abs_path.startswith(skip_path):
                        skip = True
                        break
                if not os.path.isfile(fpath):
                    download_file(self.socket, f, self.minecraft_folder)
                else:
                    if not skip:
                        download_file(self.socket, f, self.minecraft_folder)

            if progressBar != None:
                progressBar.emit(i,len(files))
            i += 1

        remove_empty_folders(self.minecraft_folder)










