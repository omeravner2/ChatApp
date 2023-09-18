import socket


class ChatServer:
    IP = "0.0.0.0"
    PORT = 1231

    def __init__(self, private_key, public_key):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(10)
        self.private_key = private_key
        self.public_key = public_key


