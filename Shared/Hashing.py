from hashlib import sha256


def create_256_key(key):
    print(type(sha256(key)))
    return sha256(key)
