import socket
from HandleTerminal import *
import datetime


class TurnToServer:
    IP = "127.0.0.1"
    PORT = 1231
    SIZE = 1024
    SUCCESSFUL_LOGIN = "LOGIN SUCCESSFUL"
    NOT_SUCCESSFUL_LOGIN = "LOGIN FAILED"
    TAKEN_USERNAME = "The username you asked for is taken"

    def __init__(self, username: str):
        self.create_client_connection(username)

    def create_client_connection(self, username: str):
        chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        chat_socket.connect((self.IP, self.PORT))
        chat_socket.send(str(len(username)) + username)
        login_status = chat_socket.recv(self.SIZE).decode()
        if self.NOT_SUCCESSFUL_LOGIN in login_status:
            return False
        else:
            return True

    def send_message(self, msg: str, username: str, client_socket):
        username += "%" * (16 - len(username))
        msg_size = len(msg.encode())
        client_socket.send(username.encode() + int(msg_size).to_bytes(4, "big") + msg.encode())

    def receive_messages(self, client_socket):
        while True:
            client_name = client_socket.recv(16).decode()
            client_name = client_name.replace("%", "")
            size = int.from_bytes(client_socket(4), "big")
            data = client_socket.recv(size)
            HandleTerminal.print_new_msg(client_name, str(datetime.datetime.now()), data)
