import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(pswd: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=salt,
        length=32,
        iterations=10000
    )
    return base64.urlsafe_b64encode(kdf.derive(pswd.encode()))


def encrypt(data: str, pswd: str) -> bytes:
    salt = os.urandom(16)
    cipher_suite = Fernet(derive_key(pswd, salt))
    encrypted_data = cipher_suite.encrypt(data.encode())
    return salt + encrypted_data


def decrypt(encrypted_data: bytes, pswd: str) -> str:
    salt = encrypted_data[:16]
    cipher_suite = Fernet(derive_key(pswd, salt))
    return cipher_suite.decrypt(encrypted_data[16:]).decode()
