
class ChatClient:
    def __init__(self, username: str, password: str, user_socket, shared_key):
        self.username = username
        self.password = password
        self.user_socket = user_socket
        self.connected = False
        self.shared_key = shared_key


