# app/utils/cloud_backup.py
import os
import pickle
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Если измените область доступа, удалите файл токена
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Аутентификация и создание сервиса для работы с Google Drive
def authenticate_google_drive():
    creds = None
    # Файл токена сохраняется для последующих запусков
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Если нет действительных учетных данных, пользователю нужно авторизоваться
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохраняем учетные данные для следующего использования
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

# Загрузка резервной копии базы данных на Google Drive
def upload_backup_to_drive(file_path):
    service = authenticate_google_drive()
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Файл загружен на Google Drive с ID: {file.get('id')}")
    return file.get('id')

# Загрузка резервной копии с Google Drive
def download_backup_from_drive(file_id, destination_path):
    service = authenticate_google_drive()
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Загрузка {int(status.progress() * 100)}% завершена.")
    print(f"Файл скачан в: {destination_path}")
