import base64
import os
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES, PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class Encryption:

    @staticmethod
    def create_rsa_keys():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.public_key().export_key()
        return private_key, public_key

    @staticmethod
    def generate_rsa_keys():
        public_key, private_key = rsa.newkeys(512)
        return private_key.save_pkcs1(), public_key.save_pkcs1()

    @staticmethod
    def rsa_encrypt(key, data):
        cipher = PKCS1_v1_5.new(RSA.importKey(key))
        cipher_text = cipher.encrypt(data)
        return base64.b64encode(cipher_text)

    @staticmethod
    def rsa_decrypt(private_key, data):
        cipher = PKCS1_v1_5.new(RSA.importKey(private_key))
        data = base64.b64decode(data)
        clear_text = cipher.decrypt(data, get_random_bytes(16), expected_pt_len=16)
        return clear_text

    @staticmethod
    def rsa_encryption(public_key, data):
        return rsa.encrypt(data, public_key)

    @staticmethod
    def rsa_decryption(private_key, data):
        return rsa.decrypt(data, private_key)

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
    def serialize_key(public_key):
        key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return key_bytes

    @staticmethod
    def deserialize_key(public_key):
        key = serialization.load_pem_public_key(public_key, backend=default_backend())
        return key
