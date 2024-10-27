# app/encryption/encrypt.py
from cryptography.fernet import Fernet

# Функция для шифрования пароля
def encrypt_password(password: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

# Функция для дешифрования пароля
def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

# Генерация ключа шифрования (мастер-ключ)
def generate_key() -> bytes:
    return Fernet.generate_key()
