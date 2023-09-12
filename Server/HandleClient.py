from ChatServer import *
from TurnToDB import *
from Message import *
import datetime


class HandleClients:
    FAILED_USER_MESSAGE = "Failed to receive data from user"

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

    def update_all_users(self, msg: str, sender, chat_server):
        for client in chat_server.clients:
            if client != sender:
                ChatServer.send_message(chat_server, client.client_socket, sender.username, msg)
