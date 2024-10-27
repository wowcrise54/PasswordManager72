# app/auth/user_auth.py
import os
import base64
import sqlite3
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

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
    conn.close()

    print(f"Пользователь {username} успешно зарегистрирован")

# Получение информации о пользователе по имени
def get_user_by_username(username: str):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, username, salt, master_key FROM users WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'id': user[0],
            'username': user[1],
            'salt': user[2],
            'master_key': user[3]
        }
    else:
        print(f"Пользователь {username} не найден")
        return None

# Аутентификация пользователя с проверкой мастер-пароля
def authenticate_user(username: str, master_password: str) -> bool:
    user = get_user_by_username(username)

    if not user:
        return False

    # Генерация мастер-ключа на основе введенного пароля и соли
    input_master_key = generate_master_key(master_password, user['salt'])

    # Проверка совпадения ключей
    if input_master_key == user['master_key']:
        print(f"Пользователь {username} успешно аутентифицирован")
        return True
    else:
        print("Неверный мастер-пароль")
        return False
