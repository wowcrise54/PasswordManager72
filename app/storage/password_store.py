# app/storage/password_store.py
import sqlite3
from app.encryption.encrypt import encrypt_password, decrypt_password

# Добавление зашифрованного пароля в базу данных
def add_password(user_id: int, site_name: str, password: str, key: bytes):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Шифрование пароля
    encrypted_password = encrypt_password(password, key)

    # Вставка зашифрованного пароля в базу данных
    cursor.execute('''
        INSERT INTO passwords (user_id, site_name, encrypted_password)
        VALUES (?, ?, ?)
    ''', (user_id, site_name, encrypted_password))

    conn.commit()
    conn.close()

# Получение и расшифровка пароля из базы данных
def get_password(user_id: int, site_name: str, key: bytes) -> str:
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT encrypted_password FROM passwords
        WHERE user_id = ? AND site_name = ?
    ''', (user_id, site_name))

    encrypted_password = cursor.fetchone()[0]
    conn.close()

    # Дешифрование пароля
    return decrypt_password(encrypted_password, key)
