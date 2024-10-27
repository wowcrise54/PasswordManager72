# app/auth/user_auth.py
import sqlite3
from app.auth.mfa import verify_mfa_code, generate_mfa_secret, save_mfa_secret
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os

# Генерация мастер-ключа на основе пароля пользователя и соли
def generate_master_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

# Создание соли для генерации ключа
def generate_salt() -> bytes:
    return os.urandom(16)

# Регистрация нового пользователя
def register_user(username: str, master_password: str):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Генерация соли и мастер-ключа
    salt = generate_salt()
    master_key = generate_master_key(master_password, salt)

    # Сохранение пользователя в базу данных
    cursor.execute('''
        INSERT INTO users (username, salt, master_key)
        VALUES (?, ?, ?)
    ''', (username, salt, master_key))

    conn.commit()

    # Генерация и сохранение MFA-секрета
    user_id = cursor.lastrowid  # Получаем ID только что созданного пользователя
    mfa_secret = generate_mfa_secret()
    save_mfa_secret(user_id, mfa_secret)

    conn.close()

    print(f"Пользователь {username} успешно зарегистрирован. Настройте MFA с этим секретом: {mfa_secret}")

# Аутентификация пользователя с проверкой мастер-пароля и MFA
def authenticate_user(username: str, master_password: str, mfa_code: str) -> bool:
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, salt, master_key FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        print(f"Пользователь {username} не найден")
        return False

    user_id, salt, stored_master_key = user

    # Генерация мастер-ключа на основе введенного пароля и соли
    input_master_key = generate_master_key(master_password, salt)

    # Проверка совпадения ключей
    if input_master_key == stored_master_key:
        print(f"Пользователь {username} успешно аутентифицирован на этапе мастер-пароля")

        # Проверка MFA-кода
        if verify_mfa_code(user_id, mfa_code):
            print("MFA успешно пройдена")
            return True
        else:
            print("Неверный MFA-код")
            return False
    else:
        print("Неверный мастер-пароль")
        return False
