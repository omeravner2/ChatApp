from TurnToServer import TurnToServer


class HandleTerminal:
    FIRST_MSG = "Hi peps! Welcome to the most amazing chat app ever :)\n Please enter 1 for login and 2 for sign up"
    LOGIN_MSG_USERNAME = "Please enter your username"
    LOGIN_MSG_PASSWORD = "Please enter your password"
    LOGIN_ERROR_MSG_USERNAME = "Please re-enter a username"
    LOGIN_ERROR_MSG_PASSWORD = "Please re-enter the password"

    def start_app(self):
        action = input(self.FIRST_MSG)
        username = ''
        if action == 1:
            username = input(self.LOGIN_MSG_USERNAME)
            while len(username) > 16 or len(username) <= 0:
                username = input(self.LOGIN_ERROR_MSG_USERNAME)
            password = input(self.LOGIN_MSG_PASSWORD)
            while len(password) > 30 or len(password) <= 0:
                password = input(self.LOGIN_ERROR_MSG_PASSWORD)

    def print_new_msg(self, username: str, date: str, msg: str):
        print(username + "    " + date + "    " + msg)
