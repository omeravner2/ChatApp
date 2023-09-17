import sqlite3
from ServerVariables import *
from Message import *


class TurnToDB:

    def __init__(self):
        self.db_connection = self.connect_to_db(ServerVariables.USERS_DB_NAME.value)

    def create_table(self):
        db_cursor = self.db_connection.cursor()
        db_cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT, Password TEXT)")
        self.db_connection.commit()

    def authenticate_user(self, client):
        if self.check_if_user_exist(client):
            try:
                db_cursor = self.db_connection.cursor()
                db_cursor.execute("SELECT Password From users WHERE Username = ?", [client.username])
                stored_password = db_cursor.fetchall()[0][0]
                print(stored_password, client.password)
                if TurnToDB.compare_passwords(stored_password, client.password):
                    return True, ServerVariables.LOGIN_SUCCESSFUL.value
                else:
                    return False, ServerVariables.CREDENTIALS_ERROR.value
            except:
                return False, ServerVariables.GENERAL_ERROR.value

    def add_new_user(self, client):
        if self.check_if_user_exist(client):
            return False, ServerVariables.TAKEN_USERNAME.value
        else:
            try:
                db_cursor = self.db_connection.cursor()
                db_cursor.execute("INSERT INTO users (Username, Password) VALUES(?,?)", [client.username,
                                                                                         client.password])
                self.db_connection.commit()

                return True, ServerVariables.SIGNUP_SUCCESS.value
            except:
                return False, ServerVariables.GENERAL_ERROR.value

    @staticmethod
    def add_new_message(message):
        with open(ServerVariables.MESSAGES_FILE.value, "a") as file:
            file.write(f"{message.date}|||{message.username}|||{message.data}" + '\n')

    @staticmethod
    def compare_passwords(stored_password, entered_password):
        if stored_password == entered_password:
            return True
        return False

    @staticmethod
    def get_all_messages():
        messages_list = open(ServerVariables.MESSAGES_FILE.value).readlines()
        print(messages_list)
        list_of_messages = []
        for i in range(len(messages_list)):
            line_info = messages_list[i].split('|||')
            print(line_info)
            client_message = Message(line_info[2].replace("\n", ""), line_info[1], line_info[0])
            list_of_messages.append(client_message)
        return list_of_messages

    @staticmethod
    def connect_to_db(db_name):
        db_connection = sqlite3.connect(db_name)
        return db_connection

    def check_if_user_exist(self, client):
        db_cursor = self.db_connection.cursor()
        query = "SELECT * FROM users WHERE Username = ?"
        print("client name:" + client.username)
        db_cursor.execute(query, [client.username])
        if len(db_cursor.fetchall()) > 0:
            return True
        else:
            return False
