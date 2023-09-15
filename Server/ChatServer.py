import socket


class ChatServer:
    IP = "127.0.0.1"
    PORT = 1231

    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(10)


