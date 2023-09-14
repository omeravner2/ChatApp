from enum import Enum


class ServerVariables(Enum):
    ADD_MESSAGE = '/ADD_MESSAGE'
    REGISTER_USER = '/REGISTER_USER'
    LOGIN_USER = '/LOGIN_USER'
    FAILED_USER_MESSAGE = "Failed to receive data from user"
    USERS_DB_NAME = "UserDB.db"
    CREDENTIALS_ERROR = "The username or password are incorrect"
    LOGIN_SUCCESSFUL = "login success"
    MESSAGES_FILE = "ServerMessages.txt"



