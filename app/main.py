# app/main.py
from app.storage.db_init import initialize_database
from app.auth.user_auth import register_user, authenticate_user
from app.storage.password_store import add_password, get_password
from app.utils.backup import create_backup, restore_from_backup
from app.utils.cloud_backup import upload_backup_to_drive, download_backup_from_drive
import os
from datetime import datetime

# Инициализация базы данных
initialize_database()

# Проверка времени последней резервной копии
def should_create_backup(backup_dir="backups", interval_days=1):
    if not os.path.exists(backup_dir):
        return True  # Если директория не существует, создаем резервную копию

    # Получаем список файлов резервных копий
    backup_files = os.listdir(backup_dir)
    if not backup_files:
        return True  # Если файлов нет, создаем резервную копию

    # Сортируем файлы по дате создания
    backup_files.sort(reverse=True)

    # Получаем дату последней резервной копии
    latest_backup = backup_files[0]
    latest_backup_time = datetime.strptime(latest_backup.split('_')[3], '%Y%m%d%H%M%S')

    # Проверяем, прошло ли достаточно времени с последнего бэкапа
    if (datetime.now() - latest_backup_time).days >= interval_days:
        return True
    return False

# Регистрация пользователя
username = "user1"
master_password = "strong_password"
register_user(username, master_password)

# Аутентификация пользователя
mfa_code = input("Введите MFA-код: ")
if authenticate_user(username, master_password, mfa_code):
    # Если аутентификация прошла успешно, добавляем пароль для сайта
    add_password(1, "example.com", "user_password_for_site", master_password)

    # Получаем и выводим расшифрованный пароль
    retrieved_password = get_password(1, "example.com", master_password)
    print(f"Расшифрованный пароль для example.com: {retrieved_password}")

    # Автоматическое создание резервной копии
    if should_create_backup():
        backup_filepath = create_backup()
        if backup_filepath:
            upload_backup_to_drive(backup_filepath)

else:
    print("Аутентификация не удалась")

# Восстановление базы данных из облачной резервной копии
file_id = input("Введите ID файла на Google Drive для восстановления: ")
destination_path = "password_manager.db"
download_backup_from_drive(file_id, destination_path)
