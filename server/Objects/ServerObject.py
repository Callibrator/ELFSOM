#This is the server, it is responsible for handling clients!

import socket
import config

from Client import Client

from get_files_tree import get_files_tree
from get_file_details import get_file_details

class ServerObject:
    def __init__(self):

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((config.host,config.port))

        self.s.listen(config.max_clients_in_queue)

        self.clients = []

        self.file_details = []

    def get_all_files(self):
        self.file_details = []
        for f in get_files_tree(config.minecraft_files_path):
            self.file_details.append(get_file_details(f))

    def start_client_handler(self):

        while True:
            c, a = self.s.accept()
            co = Client(c, a,self.clients,self.file_details)
            co.start()
            self.clients.append(co)





