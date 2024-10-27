# app/auth/mfa.py
import pyotp
import sqlite3

# Генерация нового секретного ключа для MFA
def generate_mfa_secret():
    return pyotp.random_base32()

# Сохранение секретного ключа для пользователя
def save_mfa_secret(user_id: int, secret_key: str):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO mfa (user_id, secret_key)
        VALUES (?, ?)
    ''', (user_id, secret_key))

    conn.commit()
    conn.close()

# Получение секретного ключа MFA для пользователя
def get_mfa_secret(user_id: int) -> str:
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()

    cursor.execute('SELECT secret_key FROM mfa WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None

# Проверка одноразового MFA-кода
def verify_mfa_code(user_id: int, code: str) -> bool:
    secret_key = get_mfa_secret(user_id)

    if secret_key:
        totp = pyotp.TOTP(secret_key)
        return totp.verify(code)
    else:
        return False
