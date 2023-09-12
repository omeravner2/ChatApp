import threading
import socket
from User import *


class HandleClients:
    CLIENTS = []

    def client_connection(self, server_socket):
        client_socket, client_address = server_socket.accept()
        client_details = client_socket.recv(1024).decode()
        client_details = client_details.split()
        new_client = User(client_details[0], client_details[1], client_socket)
        self.CLIENTS.append(new_client)

    def update_all_users(self, msg: str):
        for client in self.CLIENTS:
            client.client_socket.send(str(len(msg)).encode())
            client.client_socket.send(msg.encode())

    def receiving_messages(self):
        pass
