import datetime
import shutil
from ClientVariables import *


class HandleTerminal:

    def start_app_terminal(self):
        action = input(ClientVariables.FIRST_MSG.value)
        while action != 1 or action != 2:
            print(ClientVariables.START_ERROR.value)
            action = input(ClientVariables.FIRST_MSG.value)
        if action == 1:
            username, password = self.get_login_credentials()
            return username, password, ClientVariables.LOGIN_USER.value
        else:
            username, password = self.get_signup_credentials()
            return username, password, ClientVariables.REGISTER_USER.value

    @staticmethod
    def get_login_credentials():
        username = input(ClientVariables.LOGIN_MSG_USERNAME.value)
        while len(username) > 16 or len(username) <= 0:
            username = input(ClientVariables.LOGIN_ERROR_MSG_USERNAME.value)
        password = input(ClientVariables.LOGIN_MSG_PASSWORD.value)
        while len(password) > 30 or len(password) <= 0:
            password = input(ClientVariables.LOGIN_ERROR_MSG_PASSWORD.value)
        return username, password

    @staticmethod
    def get_signup_credentials():
        username = input(ClientVariables.SIGNUP_MSG_USERNAME.value)
        while len(username) > 16 or len(username) <= 0:
            username = input(ClientVariables.SIGNUP_ERROR_MSG_USERNAME.value)
        password = input(ClientVariables.SIGNUP_MSG_PASSWORD.value)
        while len(password) > 30 or len(password) <= 0:
            password = input(ClientVariables.LOGIN_ERROR_MSG_PASSWORD.value)
        verified_password = input(ClientVariables.SIGNUP_MSG_PASSWORD_RE_ENTER.value)
        while verified_password != password:
            verified_password = input(ClientVariables.SIGNUP_ERROR_MSG_PASSWORDS_DONT_MATCH.value)
        return username, password

    @staticmethod
    def print_new_msg(username: str, msg: str):
        print(f'{datetime.datetime.now()} : {username} > {msg}')

    @staticmethod
    def print_admin_msg(msg):
        columns = shutil.get_terminal_size().columns
        print(msg.center(columns))

    @staticmethod
    def get_message_from_terminal():
        message = input()
        return message, "add_message"
