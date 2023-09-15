import threading
from ChatServer import *
from ChatClient import *
from TurnToDB import *
from Message import *
import datetime
from ServerVariables import *


class HandleClients:

    @staticmethod
    def login(server_turn_to_db, client):
        connection_flag = server_turn_to_db.authenticate_user(client)
        return connection_flag

    @staticmethod
    def signup(server_turn_to_db, client):
        sign_up_flag = server_turn_to_db.add_new_user(client)
        return sign_up_flag

    @staticmethod
    def start_user_connection(chat_server, server_turn_to_db):
        client_request_flag = False
        client_socket, client_address = chat_server.server_socket.accept()
        username, password, action = HandleClients.receive_message(client_socket)
        client = ChatClient(username, password, client_socket)
        message = ServerVariables.INVALID_ACTION.value
        if action == ServerVariables.LOGIN_USER.value:
            client_request_flag, message = HandleClients.login(server_turn_to_db, client)
        elif action == ServerVariables.REGISTER_USER.value:
            client_request_flag, message = HandleClients.signup(server_turn_to_db, client)
        if client_request_flag:
            chat_server.clients.append(client)
        admin_name = "Admin%%%%%%%%%%%"
        HandleClients.send_message(client_socket, admin_name, message)
        return client

    @staticmethod
    def receiving_messages(client, chat_server):  # needs to go over!!!!
        while True:
            try:
                username, message, action = HandleClients.receive_message(client.user_socket)
                if action == ServerVariables.ADD_MESSAGE.value:
                    print("HERE")
                    client_message = Message(message, client.username, str(datetime.datetime.now()))
                    TurnToDB.add_new_message(client_message)  # check this
                    HandleClients.update_all_users(message, client, chat_server)
            except:
                chat_server.clients.remove(client)
                admin_name = "Admin%%%%%%%%%%%"
                HandleClients.send_message(client.user_socket, admin_name, ServerVariables.GENERAL_ERROR.value)

    @staticmethod
    def update_all_users(msg: str, sender, chat_server):
        for client in chat_server.clients:
            # if client != sender:
            HandleClients.send_message(client.user_socket, sender.username, msg)

    @staticmethod
    def run():
        chat_server = ChatServer()
        server_turn_to_db = TurnToDB()
        server_turn_to_db.create_db()
        while True:
            client = HandleClients.start_user_connection(chat_server, server_turn_to_db)
            client_handler = threading.Thread(target=HandleClients.receiving_messages, args=(client, chat_server))
            client_handler.start()

    @staticmethod
    def receive_message(client_socket):
        username = client_socket.recv(16).decode()
        username = username.replace("%", "")
        size = int.from_bytes(client_socket.recv(4), "big")
        message = client_socket.recv(size).decode()
        action = client_socket.recv(16).decode()
        action = action.replace("%", "")
        return username, message, action

    @staticmethod
    def send_message(client_socket, sender_username, msg_data):
        client_socket.send(sender_username.encode() + int(len(msg_data)).to_bytes(4, "big") + msg_data.encode())


if __name__ == "__main__":
    HandleClients.run()
