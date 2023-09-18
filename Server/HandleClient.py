import threading
from ChatServer import *
from ChatClient import *
from TurnToDB import *
from Message import *
import datetime
from ServerVariables import *
from Shared.Encryption import *
from Shared.Hashing import *



class HandleClients:
    def __init__(self):
        self.chat_server = ChatServer()
        self.server_turn_to_db = TurnToDB()

    def login(self, client):
        connection_flag, message = self.server_turn_to_db.authenticate_user(client)
        return connection_flag, message

    def signup(self, client):
        sign_up_flag, message = self.server_turn_to_db.add_new_user(client)
        return sign_up_flag, message

    def start_user_connection(self):
        client_request_flag = False
        client_socket, client_address = self.chat_server.server_socket.accept()
        private_key, public_key = Encryption.create_rsa_keys()
        client = ChatClient('', '', client_socket, shared_key)
        while not client_request_flag:
            username, message_date, password, action = HandleClients.receive_message(client_socket)
            client = ChatClient(username, password, client_socket, shared_key)
            message = ServerVariables.INVALID_ACTION.value
            if action == ServerVariables.LOGIN_USER.value:
                client_request_flag, message = self.login(client)
            elif action == ServerVariables.REGISTER_USER.value:
                client_request_flag, message = self.signup(client)
            if client_request_flag:
                self.chat_server.clients.append(client)

            HandleClients.send_message(client.user_socket, ServerVariables.ADMIN_NAME.value,
                                       datetime.datetime.now().strftime(ServerVariables.DATE_FORMAT.value),  message)
        return client

    def update_history(self, client_socket):
        messages_history = self.server_turn_to_db.get_all_messages()
        for message in messages_history:
            HandleClients.send_message(client_socket, message.username, message.date, message.data)

    def receiving_messages(self, client):
        while True:
            try:
                username, message_date, message, action = self.receive_message(client.user_socket)
                if action == ServerVariables.ADD_MESSAGE.value:
                    client_message = Message(message, client.username, message_date)
                    self.server_turn_to_db.add_new_message(client_message)  # check this
                    self.update_all_users(message, message_date, client)
            except:
                self.chat_server.clients.remove(client)

                HandleClients.send_message(client.user_socket, ServerVariables.ADMIN_NAME.value,
                                           datetime.datetime.now().strftime(ServerVariables.DATE_FORMAT.value),
                                           ServerVariables.GENERAL_ERROR.value)

    def update_all_users(self, msg: str, msg_date: str, sender):
        for client in self.chat_server.clients:
            # if client != sender:
            HandleClients.send_message(client.user_socket, sender.username, msg_date, msg)

    def run(self):
        self.server_turn_to_db.create_table()
        while True:
            client = self.start_user_connection()
            self.update_history(client.user_socket)
            client_handler = threading.Thread(target=self.receiving_messages, args=[client])
            client_handler.start()

    @staticmethod
    def receive_message(client_socket):
        username = client_socket.recv(16).decode()
        username = username.replace("%", "")
        size = int.from_bytes(client_socket.recv(4), "big")
        message_date = client_socket.recv(16).decode()
        message = client_socket.recv(size).decode()
        action = client_socket.recv(16).decode()
        action = action.replace("%", "")
        return username, message_date, message, action

    @staticmethod
    def send_message(client_socket, sender_username, msg_date, msg_data):
        sender_username += "%" * (16 - len(sender_username))
        client_socket.send(sender_username.encode() + int(len(msg_data)).to_bytes(4, "big") +
                           msg_date.encode() + msg_data.encode())

    @staticmethod
    def key_exchange_with_client(client_socket, public_key):
        # key = Encryption.serialize_key(public_key)
        public_key = public_key.to_bytes(256, "big")
        print(public_key)
        # size = int(len(public_key)).to_bytes(4, "big")
        client_socket.send(public_key)
        # size = int.from_bytes(client_socket.recv(4), "big")
        client_public_key = int.from_bytes(client_socket.recv(256), "big")
        # client_public_key = Encryption.deserialize_key(client_socket.recv(size))
        return client_public_key
