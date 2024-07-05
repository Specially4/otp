from cryptography.fernet import Fernet


def encrypted(secret: str):
    cipher_key = Fernet.generate_key()
    cipher = Fernet(cipher_key)
    encrypted_secret = cipher.encrypt(secret)
    return {"secret": encrypted_secret, "key": cipher_key}


def decrypted(encrypted_secret: str, key: str):
    cipher = Fernet(key)
    decrypted_secret = cipher.decrypt(encrypted_secret)
    return decrypted_secret
