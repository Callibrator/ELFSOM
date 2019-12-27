import json
import os

def download_file(socket,file, minecraft_path):

    data = {
        "file":file
    }

    dataSerialized = json.dumps(data).encode()
    socket.sendall(str(len(dataSerialized)).encode())

    ret = socket.recv(2048).decode()

    if ret != "ok":
        return False


    socket.sendall(dataSerialized)

    ret = socket.recv(2048).decode()

    if ret != "sending_file":
        return False
    socket.sendall(b"ok")

    file_size = int(socket.recv(2048).decode())

    socket.sendall(b"ok")

    current_size = 0

    filepath = minecraft_path + file["launcher_path"]

    dirPath = os.path.dirname(filepath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    fl = open(filepath, "wb")

    while current_size < file_size:
        data = socket.recv(2048)
        current_size += len(data)
        fl.write(data)
    fl.close()


    socket.sendall(b"ok")
