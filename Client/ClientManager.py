from HandleTerminal import *
from TurnToServer import *
from ClientVariables import *
import datetime


class ClientManager:

    def starting_the_client_connection(self):
        handling_terminal = HandleTerminal()
        username, password, action = handling_terminal.start_app_terminal()
        client_turn_to_server = TurnToServer()
        client_turn_to_server.client_send_message(password, username, client_turn_to_server.chat_socket, action)
        client_username, status = client_turn_to_server.client_receive_message(client_turn_to_server.chat_socket)
        if int(status) == 2000:
            handling_terminal.print_admin_msg(ClientVariables.CONNECTED_SUCCESSFUL.value)
        else:
            handling_terminal.print_admin_msg(ClientVariables.CONNECTION_ERROR.value)

    def receiving_chat_messages(self, client_turn_to_server, client_handling_terminal):
        while True:
            client_username, message = client_turn_to_server.client_receive_message(client_turn_to_server.chat_socket)
            client_handling_terminal.print_new_message(client_username, message)

    def sending_chat_messages(self, client_turn_to_server, client_handling_terminal, username):
        client_message, action = client_handling_terminal.get_message_from_terminal()
        client_turn_to_server.client_send_message(client_message, client_turn_to_server.chat_socket, username, action)
