import datetime
import pickle
import rsa
import socket
from ClientVariables import *
from Shared.Encryption import *
from Shared.Hashing import *


class TurnToServer:
    IP = "127.0.0.1"
    PORT = 1231

    def __init__(self):
        self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_socket.connect((self.IP, self.PORT))
        self.aes_key = Encryption.generate_aes_key()

    def client_send_message(self, msg: str, username: str, action):
        msg_date = datetime.datetime.now().strftime(ClientVariables.DATE_FORMAT.value)
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

    def get_server_public_key(self):
        size = int.from_bytes(self.chat_socket.recv(4), "big")
        public_key = self.chat_socket.recv(size)
        print(public_key)
        public_key = rsa.PublicKey.load_pkcs1(public_key)
        action = self.chat_socket.recv(16).decode()
        return public_key, action

    def send_shared_key(self, public_key):
        aes_key = Encryption.rsa_encryption(public_key, self.aes_key)
        size = int(len(aes_key)).to_bytes(4, "big")
        self.chat_socket.send(size + aes_key)
