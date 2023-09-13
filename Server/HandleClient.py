import threading

from ChatServer import *
from TurnToDB import *
from Message import *
import datetime


class HandleClients:
    FAILED_USER_MESSAGE = "Failed to receive data from user"

    @staticmethod
    def start_user_connection():
        while True:
            chat_server = ChatServer()
            client_socket, client_address = chat_server.server_socket.accept()
            user_details = chat_server.receive_message(client_socket)
            client = ChatClient(user_details[0], user_details[1], client_socket)
            chat_server.clients.append(client)

    def receiving_messages(self, client, chat_server):
        while True:
            try:
                message = ChatServer.receive_message(chat_server, client.client_socket)
                client_message = Message(message, client.username, str(datetime.datetime.now()))
                TurnToDB.add_new_message(client_message)  # check this
                self.update_all_users(message, client, chat_server)
            except:
                print(self.FAILED_USER_MESSAGE + client.username)
                chat_server.clients.remove(client)

    @staticmethod
    def update_all_users(msg: str, sender, chat_server):
        for client in chat_server.clients:
            if client != sender:
                ChatServer.send_message(chat_server, client.client_socket, sender.username, msg)
