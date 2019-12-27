import os
import config

def send_file(socket,filepath):
    ready_check = socket.recv(2048).decode()
    if ready_check != "ok":
        return False

    filepath = config.minecraft_files_path+filepath

    file_size = os.path.getsize(filepath)

    socket.sendall(str(int(file_size)).encode())


    buff_size = config.file_buffer_size

    iterations = int(file_size / buff_size)

    if file_size % buff_size > 0:
        iterations += 1

    fl = open(filepath, "rb")

    ready_check = socket.recv(2048).decode()
    if ready_check != "ok":
        return False

    for i in range(iterations):
        data = fl.read(buff_size)
        socket.send(data)

    fl.close()

    ready_check = socket.recv(2048).decode()
    if ready_check != "ok":
        return False

    return True