import sqlite3
from ServerVariables import *

class TurnToDB:

    @staticmethod
    def create_db():
        db_cursor = TurnToDB.connect_to_db(ServerVariables.USERS_DB_NAME.value)
        db_cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT, Password TEXT)")

    @staticmethod
    def authenticate_user(client):
        db_cursor = TurnToDB.connect_to_db(ServerVariables.USERS_DB_NAME.value)
        db_cursor.execute("SELECT Password From users WHERE Username = ?", client.username)
        stored_password = db_cursor.fetchall()
        if not stored_password:
            return ServerVariables.CREDENTIALS_ERROR.value
        elif TurnToDB.compare_passwords(stored_password, client.username):
            return True
        else:
            return False

    @staticmethod
    def add_new_user(client):
        try:
            db_cursor = TurnToDB.connect_to_db(ServerVariables.USERS_DB_NAME.value)
            db_cursor.execute("INSERT INTO users (Username, Password) VALUES(?,?)", (client.username, client.password))
            return True
        except:
            return False

    @staticmethod
    def add_new_message(message):
        file = open(ServerVariables.MESSAGES_FILE.value)
        file.write(f'{message.date} : {message.username} > {message.data}')
        file.close()

    @staticmethod
    def compare_passwords(stored_password, entered_password):
        if stored_password == entered_password:
            return True
        return False

    @staticmethod
    def connect_to_db(db_name):
        db_connection = sqlite3.connect(db_name)
        db_pointer = db_connection.cursor()
        return db_pointer

