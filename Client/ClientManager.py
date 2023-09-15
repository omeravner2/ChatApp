import threading
from HandleTerminal import *
from TurnToServer import *
from ClientVariables import *


class ClientManager:

    def __init__(self):
        self.handling_terminal = HandleTerminal()
        self.client_turn_to_server = TurnToServer()

    def starting_the_client_connections(self):
        username, password, action = self.handling_terminal.start_app_terminal()
        self.client_turn_to_server.client_send_message(password, username, self.client_turn_to_server.chat_socket,
                                                       action)
        client_username, status = self.client_turn_to_server.client_receive_message(
            self.client_turn_to_server.chat_socket)
        print(client_username, status)
        if client_username == 'Admin':
            HandleTerminal.print_admin_msg(status)
        else:
            HandleTerminal.print_admin_msg(ClientVariables.CONNECTION_ERROR.value)
        return username

    @staticmethod
    def receiving_chat_messages(client_turn_to_server, client_handling_terminal):
        while True:
            client_username, message = client_turn_to_server.client_receive_message(client_turn_to_server.chat_socket)
            client_handling_terminal.print_new_msg(client_username, message)

    @staticmethod
    def sending_chat_messages(client_turn_to_server, client_handling_terminal, username):
        while True:
            client_message, action = client_handling_terminal.get_message_from_terminal()
            client_turn_to_server.client_send_message(client_message, username, client_turn_to_server.chat_socket,
                                                      action)

    def client_run(self):
        client_username = self.starting_the_client_connections()
        send_messages_thread = threading.Thread(target=self.sending_chat_messages,
                                                args=(self.client_turn_to_server, self.handling_terminal,
                                                      client_username))
        receive_messages_thread = threading.Thread(target=self.receiving_chat_messages, args=(self.client_turn_to_server
                                                                                              , self.handling_terminal))
        send_messages_thread.start()
        receive_messages_thread.start()


