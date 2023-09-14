from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class Encryption:

    def create_rsa_keys(self):
        key = RSA.generate(2048)
        public_key = key.public_key()
        public_key = public_key.export_key('PEM')
        return key, public_key

    def rsa_encrypt(self, public_key, data):
        cipher = PKCS1_OAEP.new(public_key)
        cipher_text = cipher.encrypt(data)
        return cipher_text

    def rsa_decrypt(self, private_key, data):
        cipher = PKCS1_OAEP.new(private_key)
        clear_text = cipher.decrypt(data)
        return clear_text
