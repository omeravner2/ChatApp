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
        size = int.from_bytes(client_socket.recv(4), "big")
        message = client_socket.recv(size).decode()
        return message

    def send_message(self, client_socket, sender_username, msg_data):
        client_socket.send(sender_username.encode() + int(len(msg_data)).to_bytes(4, "big") + msg_data.encode())

    def start_user_connection(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            user_details = self.receive_message(client_socket)
            user_details = user_details.split("$%^")
            client = ChatClient(user_details[0], user_details[1], client_socket)
            self.clients.append(client)


