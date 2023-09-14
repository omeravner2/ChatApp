import threading

from ChatServer import *
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
    def start_user_connection():
        chat_server = ChatServer()
        server_turn_to_db = TurnToDB()
        while True:
            client_request_flag = False
            client_socket, client_address = chat_server.server_socket.accept()
            user_details, action = chat_server.receive_message(client_socket)
            client = ChatClient(user_details[0], user_details[1], client_socket)
            if action == ServerVariables.LOGIN_USER.value:
                client_request_flag = HandleClients.login(server_turn_to_db, client)
            elif action == ServerVariables.REGISTER_USER.value:
                client_request_flag = HandleClients.signup(server_turn_to_db, client)
            if client_request_flag:
                chat_server.clients.append(client)
            return client_request_flag

    def receiving_messages(self, client, chat_server):  # needs to go over!!!!
        while True:
            try:
                message = ChatServer.receive_message(client.client_socket)
                client_message = Message(message, client.username, str(datetime.datetime.now()))
                TurnToDB.add_new_message(client_message)  # check this
                self.update_all_users(message, client, chat_server)
            except:
                print(ServerVariables.FAILED_USER_MESSAGE.value + client.username)
                chat_server.clients.remove(client)

    @staticmethod
    def update_all_users(msg: str, sender, chat_server):
        for client in chat_server.clients:
            if client != sender:
                ChatServer.send_message(client.client_socket, sender.username, msg)

