import datetime
import socket


class TurnToServer:
    IP = "127.0.0.1"
    PORT = 1231

    def __init__(self):
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_socket.connect((self.IP, self.PORT))

    def client_send_message(self, msg: str, username: str, action):
        msg_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        username += "%" * (16 - len(username))
        msg_size = len(msg.encode())
        action += "%" * (16 - len(action))
        self.chat_socket.send(username.encode() + int(msg_size).to_bytes(4, "big") + msg_date.encode() +
                              msg.encode() + action.encode())

    def client_receive_message(self):
        client_name = self.chat_socket.recv(16).decode()
        client_name = client_name.replace("%", "")
        size = int.from_bytes(self.chat_socket.recv(4), "big")
        msg_date = self.chat_socket.recv(16).decode()
        data = self.chat_socket.recv(size).decode()
        return client_name, msg_date, data
