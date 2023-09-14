from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class Encryption:

    @staticmethod
    def create_rsa_keys():
        key = RSA.generate(2048)
        public_key = key.public_key()
        public_key = public_key.export_key('PEM')
        return key, public_key

    @staticmethod
    def rsa_encrypt(public_key, data):
        cipher = PKCS1_OAEP.new(public_key)
        cipher_text = cipher.encrypt(data)
        return cipher_text

    @staticmethod
    def rsa_decrypt(private_key, data):
        cipher = PKCS1_OAEP.new(private_key)
        clear_text = cipher.decrypt(data)
        return clear_text

    @staticmethod
    def aes_encrypt(key, data):
        cipher = AES.new(key, AES.MODE_CBC)
        plain_text = pad(data.encode(), AES.block_size)
        cipher_text = cipher.encrypt(plain_text)
        return cipher_text, cipher.iv

    @staticmethod
    def aes_decrypt(key, data, iv):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plain_text = unpad(cipher.decrypt(data), AES.block_size).decode()
        return plain_text

    @staticmethod
    def generate_rsa_key():
        return get_random_bytes(16)  # 128 bits

