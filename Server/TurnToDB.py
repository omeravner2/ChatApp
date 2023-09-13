import sqlite3


class TurnToDB:
    USERS_DB_NAME = "UserDB.db"
    CREDENTIALS_ERROR = "The username or password are incorrect"
    LOGIN_SUCCESSFUL = "login success"
    MESSAGES_FILE = "ServerMessages.txt"

    def create_db(self):
        db_cursor = self.connect_to_db(self.USERS_DB_NAME)
        db_cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT, Password TEXT)")

    def authenticate_user(self, client):
        db_cursor = self.connect_to_db(self.USERS_DB_NAME)
        db_cursor.execute("SELECT Password From users WHERE Username = ?", client.username)
        stored_password = db_cursor.fetchall()
        if not stored_password:
            return self.CREDENTIALS_ERROR
        elif self.compare_passwords(stored_password, client.username):
            return self.LOGIN_SUCCESSFUL
        else:
            return self.CREDENTIALS_ERROR

    def add_new_user(self, client):
        db_cursor = self.connect_to_db(self.USERS_DB_NAME)
        db_cursor.execute("INSERT INTO users (Username, Password) VALUES(?,?)", (client.username, client.password))

    def add_new_message(self, message):
        file = open(self.MESSAGES_FILE)
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

