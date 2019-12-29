# Client Class, It contains all functions that will be used for the client/server communication

import threading
import json
from check_server_file import check_server_file
import os

from send_file import send_file

class Client(threading.Thread):
    def __init__(self, client, address, clients, file_details):
        super(Client, self).__init__()

        self.s = client
        self.addr = address
        self.clients = clients
        self.file_details = file_details

    def compare_files(self,files):
        status = []

        for f in self.file_details:
            f["launcher_path"] = f["launcher_path"].replace("/", os.sep).replace("\\", os.sep)

        for lf in self.file_details:
            found = False
            needs_update = True

            for sf in files:

                if sf["launcher_path"] == lf["launcher_path"]:
                    found = True
                    if sf["sha256"] == lf["sha256"]:
                        needs_update = False
                    break

            s = lf
            if found:

                if needs_update:
                    s["status"] = "update"
                else:
                    s["status"] = "ok"

            else:
                s["status"] = "update"

            status.append(s)


        remove_files =[]
        for i in range(len(files)):
            f = files[i]
            found = False
            for fs in status:
                if f["launcher_path"] == fs["launcher_path"]:
                    found = True
            if not found:
                f["status"] = "remove"
                remove_files.append(f)
        status += remove_files


        return status



    def run(self):
        while True:
            data = self.s.recv(2048).decode()
            if data == "":
                break #Socket Closed!

            dataLength = int(data)

            self.s.sendall(b"ok")

            serializedData = ""
            while len(serializedData) < dataLength:
                serializedData += self.s.recv(dataLength)

            data = json.loads(serializedData.decode())

            if "details" in data:
                ret = self.compare_files(data["files"])
                serializedRet = json.dumps(ret).encode()

                self.s.sendall(str(len(serializedRet)).encode())
                data = self.s.recv(2048).decode()
                if data == "ok":
                    self.s.sendall(serializedRet)
                else:
                    break

            elif "file" in data:
                fileData = data["file"]
                if check_server_file(fileData, self.file_details):
                    self.s.sendall(b"sending_file")
                    send_file(self.s, fileData["launcher_path"])

                else:
                    self.s.sendall(b"file_not_found")

        self.clients.remove(self)
        del self
