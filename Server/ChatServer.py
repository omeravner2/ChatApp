import socket
from ChatClient import ChatClient


class ChatServer:
    IP = "127.0.0.1"
    PORT = 1231

    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(10)

    def receive_message(self, client_socket):
        username = client_socket.recv(16)
        size = int.from_bytes(client_socket.recv(4), "big")
        message = client_socket.recv(size).decode()
        return message

    def send_message(self, client_socket, sender_username, msg_data):
        client_socket.send(sender_username.encode() + int(len(msg_data)).to_bytes(4, "big") + msg_data.encode())



