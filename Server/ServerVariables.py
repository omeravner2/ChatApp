from enum import Enum


class ServerVariables(Enum):
    ADD_MESSAGE = '/ADD_MESSAGE'
    REGISTER_USER = '/REGISTER_USER'
    LOGIN_USER = '/LOGIN_USER'
    FAILED_USER_MESSAGE = "Failed to receive data from user"
    USERS_DB_NAME = "UserDB.db"
    CREDENTIALS_ERROR = "The username or password are incorrect"
    GENERAL_ERROR = "Something went wrong... try closing the chat and connecting again"
    TAKEN_USERNAME = "The username you chose is taken, try choosing a different one"
    LOGIN_SUCCESSFUL = "login succeeded, Enjoy The chat "
    SIGNUP_SUCCESS = "Sign up successfully! Enjoy!"
    MESSAGES_FILE = "ServerMessages.txt"
    INVALID_ACTION = "invalid action was requested"



