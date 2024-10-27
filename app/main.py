# app/main.py
from app.storage.db_init import initialize_database
from app.auth.user_auth import register_user, authenticate_user
from app.storage.password_store import add_password, get_password

# Инициализация базы данных
initialize_database()

# Регистрация пользователя
username = "user1"
master_password = "strong_password"
register_user(username, master_password)

# Аутентификация пользователя
if authenticate_user(username, master_password):
    # Если аутентификация прошла успешно, добавляем пароль для сайта
    add_password(1, "example.com", "user_password_for_site", master_password)

    # Получаем и выводим расшифрованный пароль
    retrieved_password = get_password(1, "example.com", master_password)
    print(f"Расшифрованный пароль для example.com: {retrieved_password}")
else:
    print("Аутентификация не удалась")
