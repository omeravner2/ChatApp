import socket
from Shared.Encryption import *


class ChatServer:
    IP = "0.0.0.0"
    PORT = 1231

    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(10)
        self.private_key, self.public_key = Encryption.generate_rsa_keys()




