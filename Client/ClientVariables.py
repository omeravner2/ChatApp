from enum import Enum


class ClientVariables(Enum):
    FIRST_MSG = "Hi peps! Welcome to the most amazing chat app ever :)\n Please enter 1 for login and 2 for sign up"
    LOGIN_MSG_USERNAME = "Please enter username"
    LOGIN_MSG_PASSWORD = "Please enter password"
    LOGIN_ERROR_MSG_USERNAME = "Please re-enter a username"
    LOGIN_ERROR_MSG_PASSWORD = "Please re-enter the password"
    SIGNUP_MSG_USERNAME = "Please enter the username you want to have :)"
    SIGNUP_MSG_PASSWORD = "Enter the password you would like to user"
    SIGNUP_MSG_PASSWORD_RE_ENTER = "Now, please enter the password again"
    SIGNUP_ERROR_MSG_USERNAME = "Name does not fit demands, make sure it's not empty and has up to 16 chars :)"
    SIGNUP_ERROR_MSG_PASSWORD = "Password does not fit demands, make sure it's not empty and has up to 30 chars :)"
    SIGNUP_ERROR_MSG_PASSWORDS_DONT_MATCH = "Passwords don't much, renter the password one more time"
    START_ERROR = "No valid input, make sure you've entered 1 or 2."
    CONNECTED_SUCCESSFUL = "Entering chat..."
    CONNECTION_ERROR = "Something Failed. try closing the app and re-ran it"
    ADD_MESSAGE = '/ADD_MESSAGE'
    REGISTER_USER = '/REGISTER_USER'
    LOGIN_USER = '/LOGIN_USER'



