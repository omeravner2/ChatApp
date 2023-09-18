from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization


class Encryption:

    @staticmethod
    def create_rsa_keys():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.public_key().export_key()
        return private_key, public_key

    @staticmethod
    def rsa_encrypt(recipient_public_key, data):
        cipher = PKCS1_OAEP.new(RSA.importKey(recipient_public_key))
        cipher_text = cipher.encrypt(data.encode())
        return cipher_text

    @staticmethod
    def rsa_decrypt(private_key, data):
        cipher = PKCS1_OAEP.new(RSA.importKey(private_key))
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
    def generate_aes_key():
        return get_random_bytes(16)  # 128 bits

    @staticmethod
    def generate_diffie_hellman_keys():
        parameters = dh.generate_parameters(generator=2, key_size=1024)
        print("parameters")
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()
        print("Generated public key is ")
        print(public_key)
        return private_key, public_key

    @staticmethod
    def serialize_key(public_key):
        key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return key_bytes

    @staticmethod
    def deserialize_key(public_key):
        key = serialization.load_pem_public_key(public_key)
        return key
