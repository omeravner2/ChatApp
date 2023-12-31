import threading
from HandleTerminal import *
from TurnToServer import *
from ClientVariables import *


class ClientManager:

    def __init__(self):
        self.handling_terminal = HandleTerminal()
        self.client_turn_to_server = TurnToServer()
        self.Running = True

    def starting_the_client_connections(self):
        username, password, action = self.handling_terminal.start_app_terminal()
        self.client_turn_to_server.client_send_message(password, username,
                                                       action)
        server_public_key, action = self.client_turn_to_server.get_server_public_key()
        client_username, status = self.getting_status_from_server()
        while status in ClientVariables.ERRORS_LIST.value:
            if action == ClientVariables.LOGIN_USER.value:
                username, password = self.handling_terminal.get_login_credentials()
            elif action == ClientVariables.REGISTER_USER.value:
                username, password = self.handling_terminal.get_signup_credentials()
            self.client_turn_to_server.client_send_message(password, username,
                                                           action)
            username, status = self.getting_status_from_server()
        return username

    def receiving_chat_messages(self):
        while True:
            client_username, message_date, message = self.client_turn_to_server.client_receive_message()
            self.handling_terminal.print_new_msg(client_username, message_date, message)

    def sending_chat_messages(self, username):
        while True:
            client_message, action = self.handling_terminal.get_message_from_terminal()
            self.client_turn_to_server.client_send_message(client_message, username
                                                           , action)

    def client_run(self):
        client_username = self.starting_the_client_connections()
        send_messages_thread = threading.Thread(target=self.sending_chat_messages,
                                                args=[client_username])
        receive_messages_thread = threading.Thread(target=self.receiving_chat_messages)
        send_messages_thread.start()
        receive_messages_thread.start()

    def getting_status_from_server(self):
        client_username, message_date, status = self.client_turn_to_server.client_receive_message()
        if client_username == ClientVariables.ADMIN_NAME.value:
            HandleTerminal.print_admin_msg(status)
        else:
            HandleTerminal.print_admin_msg(ClientVariables.CONNECTION_ERROR.value)
        return client_username, status


