# app/utils/backup.py
import shutil
import os
from datetime import datetime

# Функция для создания резервной копии базы данных
def create_backup(backup_dir: str = "backups"):
    # Проверяем, существует ли директория для резервных копий, если нет — создаем ее
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Генерируем имя файла резервной копии с временной меткой
    backup_filename = f"password_manager_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.db"

    # Полный путь к файлу резервной копии
    backup_filepath = os.path.join(backup_dir, backup_filename)

    try:
        # Копируем файл базы данных
        shutil.copyfile("password_manager.db", backup_filepath)
        print(f"Резервная копия успешно создана: {backup_filepath}")
        return backup_filepath
    except Exception as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return None

# Функция для восстановления базы данных из резервной копии
def restore_from_backup(backup_filepath: str):
    try:
        # Копируем резервную копию обратно как основную базу данных
        shutil.copyfile(backup_filepath, "password_manager.db")
        print(f"База данных успешно восстановлена из резервной копии: {backup_filepath}")
    except Exception as e:
        print(f"Ошибка при восстановлении базы данных: {e}")
