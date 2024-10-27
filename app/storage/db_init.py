# app/storage/db_init.py
import sqlite3

# Инициализация базы данных
def initialize_database():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            salt BLOB NOT NULL,
            master_key BLOB NOT NULL
        )
    ''')

    # Создание таблицы для паролей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            site_name TEXT NOT NULL,
            encrypted_password BLOB NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Создание таблицы для хранения секретных ключей MFA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mfa (
            user_id INTEGER PRIMARY KEY,
            secret_key TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
